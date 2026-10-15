# Brief C — Báo giá (Tạo mới / Chỉnh sửa / Sao chép): Tổng hợp giá trị · VAT · Giảm giá · Điều khoản/Ghi chú · Lưu nháp/Gửi duyệt · Sao chép · Quy tắc sửa

> Nguồn: CHỈ đọc code (nhánh gop_db). Viết tắt đường dẫn:
> - `EDIT` = `hrm-client/pages/assign/quotations/_id/edit.vue` (form dùng chung Tạo mới / Sửa / Sao chép)
> - `CREATE` = `hrm-client/pages/assign/quotations/create.vue` (chỉ `extends EDIT`, ghi đè `isCreateMode = !item.id`, CREATE:1-13)
> - `SVC` = `hrm-api/Modules/Assign/Services/QuotationService.php`
> - `CTL` = `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`
> - `REQ_S` / `REQ_U` = `Modules/Assign/Http/Requests/Quotation/QuotationStoreRequest.php` / `QuotationUpdateRequest.php`
> - `COPYMX` = `hrm-client/utils/mixins/Assign/QuotationCopyMixin.js`
> - `SUBMIT_MODAL` = `hrm-client/components/assign/quotation/QuotationSubmitModal.vue`
> - `LANG` = `hrm-api/resources/lang/vi/validation.php`
>
> Đường dẫn route FE: Tạo mới = `/assign/quotations/create`; Sửa = `/assign/quotations/{id}/edit`; Sao chép = `/assign/quotations/create?copy_from={id}` (tài liệu SRS KHÔNG ghi URL — chỉ để người viết định vị).

---

## 0. Bối cảnh chung của form (cần biết để hiểu các mục dưới)

- **3 chế độ dùng chung 1 form** (EDIT):
  - Tạo mới: `initCreateMode()` EDIT:2301-2375 — dựng bản ghi tạm: Mã báo giá hiển thị `(Chưa tạo)`, trạng thái `Đang tạo`, loại tự lập (type 2), VAT vận chuyển mặc định **8%**, phương thức GG = Không GG, loại tiền mặc định **VNĐ** nếu không chọn dự án (`applyDefaultVndCurrency` EDIT:2399-2406). Tiêu đề trang: **"Tạo báo giá"** (EDIT:1614-1616).
  - Sửa: `fetchData()` → `applyDetail()` EDIT:3413-3529. Tiêu đề: **"Làm giá: <Mã> (Trạng thái)"** (EDIT:1617-1623).
  - Sao chép: màn Tạo mới có `?copy_from=` → `initCopyMode()` EDIT:2416-2497 (xem mục 6). Có thêm dòng **"Sao chép từ: <mã nguồn> — báo giá mới chỉ được tạo sau khi bấm Lưu"** trong Thông tin chung (EDIT:38-46).
- **Bảng hàng hoá** có 2 phần: **A — Hàng hoá** (nhóm, cha–con) và **B — Dịch vụ & Chi phí khác** (EDIT:476-930); dòng **TỔNG** cuối bảng (EDIT:930-943). Bảng này KHÔNG gồm chi phí vận chuyển — vận chuyển chỉ nằm ở khối Tổng hợp.
- **Toolbar trên bảng** (EDIT:284-370): `VAT: [ô %] [Tất cả] [VAT=0]` · `GG: [Không GG | GG mặt hàng | GG tổng]` · `Làm tròn [select] [Áp dụng]` · nút `Xóa giảm giá` / `Xóa phân bổ` · (ngoại tệ) `Tỷ giá: 1 <mã> = x VND (ngày tạo) - Bảng giá bán lẻ`.
- **Quyền giá vốn**: cờ `canViewCostPrice` (= quyền **"Xem giá vốn hàng hoá"**; màn Sửa lấy từ `item.can_view_import_price` do BE trả). Không có quyền ⇒ mọi cột/ô "Thành tiền nhập", TSLN, cấp duyệt ở footer hiển thị `—` hoặc ẩn.

---

## 1. Khối "Tổng hợp giá trị báo giá"

### 1.1 Vị trí & cấu trúc (EDIT:1038-1150)
Tiêu đề khối: **"Tổng hợp giá trị báo giá"** (icon biểu đồ). Là 1 bảng, cột:

| Cột (chữ đúng UI) | Hiện khi |
|---|---|
| STT | luôn |
| Nhóm chi phí | luôn |
| Thành tiền nhập | luôn (giá trị `—` nếu không có quyền "Xem giá vốn hàng hoá", trừ ô nhập giá nhập vận chuyển — xem dưới) |
| Thành tiền trước VAT | luôn |
| Giảm giá | chỉ khi phương thức GG ≠ "Không GG" |
| Thành tiền sau GG (trước VAT) | chỉ khi phương thức GG ≠ "Không GG" |
| Thuế VAT | luôn |
| Thành tiền sau VAT | luôn |

Các dòng:
| STT | Nhóm chi phí | Ghi chú |
|---|---|---|
| I | **Hàng hoá** | chỉ cộng dòng CHA / hàng độc lập (dòng con không cộng — giá cha đã bao gồm con) |
| II | **Dịch vụ** | dịch vụ/chi phí từ danh mục có "tính doanh thu" (revenue_calculation ≠ 0) hoặc dòng không gắn danh mục |
| III | **Chi phí** | dịch vụ/chi phí từ danh mục có `revenue_calculation = 0` |
| IV | **Chi phí vận chuyển** | dòng NHẬP TAY ngay trong bảng (xem 1.3) |
| V | **Tổng giá trị báo giá** | cộng I..IV theo từng cột; ô cuối "Thành tiền sau VAT" in đậm màu xanh kèm mã tiền tệ (VD `4,102,000 VND`); ô "Giảm giá" tổng in chữ đỏ |

Dưới bảng (chỉ hiện khi có quyền "Xem giá vốn hàng hoá", EDIT:1141-1148):
- **TSLN trước GG: x%** (xanh nếu ≥ 0, đỏ nếu < 0)
- **TSLN sau GG: x%**

FE: computed `summaryBreakdown` EDIT:2152-2192. BE bản đối chiếu: `computeSummaryBreakdown()` SVC:3112-3228 (cùng công thức, dùng ở màn chi tiết/in).

### 1.2 Công thức từng ô (theo dòng)
Ký hiệu: `SL` = số lượng; `GN` = đơn giá nhập; `GB` = đơn giá bán; `GG_dv` = GG(₫) trên 1 đơn vị (GG mặt hàng); `PB` = số tiền "Phân bổ GG" của dòng (GG tổng).

- **Thành tiền nhập (dòng)** = `GN × SL` (EDIT:2556). Với cha có con là hàng tạm, GN của cha tự cộng dồn (roll-up) từ con.
- **Thành tiền trước VAT (dòng)** = `GB × SL` (EDIT:2558-2560).
- **Giảm giá (dòng)**:
  - Không GG: 0
  - GG mặt hàng: `GG_dv × SL`
  - GG tổng: `PB` (số tiền phân bổ của cả dòng)  (EDIT:2561-2569)
- **Thành tiền sau GG (trước VAT)** = Thành tiền trước VAT − Giảm giá.
- **Thuế VAT (dòng)** = Thành tiền sau GG × VAT% / 100 (EDIT:2570-2572) ⇒ **VAT tính SAU giảm giá**.
- **Thành tiền sau VAT** = Thành tiền sau GG + Thuế VAT (EDIT:2573-2575).
- Mỗi nhóm I–IV = tổng các dòng thuộc nhóm; dòng V = tổng I+II+III+IV (EDIT:2182-2190).

### 1.3 Dòng IV — Chi phí vận chuyển (EDIT:1088-1128; computed EDIT:2119-2151)
Nhập trực tiếp trong khối Tổng hợp (cấp toàn báo giá, không phải dòng hàng):
- **Thành tiền nhập**: ô nhập "giá nhập vận chuyển" — người đang được sửa báo giá nhập được **kể cả khi không có quyền xem giá vốn** (EDIT:1092-1097). Lỗi < 0: **"Giá nhập không hợp lệ"**.
- **Thành tiền trước VAT**: ô nhập chi phí vận chuyển (giá bán). Lỗi < 0: **"Chi phí vận chuyển không hợp lệ"**.
- **Giảm giá**:
  - GG mặt hàng: 2 ô liên động `[% ] % [₫]` (nhập % ⇒ tự tính ₫ = chi phí × % làm tròn 2 số lẻ; nhập ₫ ⇒ tự tính %) (EDIT:2132-2141). Lỗi: **"GG vận chuyển không được lớn hơn chi phí"** (khi < 0 hoặc > chi phí).
  - GG tổng: 1 ô "phân bổ GG" cho vận chuyển (khoá khi Tổng GG = 0) (EDIT:1112-1115).
- **Thuế VAT**: `[8] % [số tiền]` — **cố định 8%, luôn khoá không cho sửa** (EDIT:1119-1125, mặc định `shippingVatPercent: 8` EDIT:1517). Tiền VAT VC = (chi phí − GG VC) × 8%.
- **Thành tiền sau VAT** = chi phí − GG VC + VAT VC.
- Vận chuyển chỉ được tính vào tổng khi chi phí > 0 (EDIT:2174; SVC:3076, 3200).
- Vận chuyển **có** tham gia: TSLN tổng, cơ sở % của GG tổng, phân bổ GG tổng, cấp duyệt (giá trị đơn hàng). **Không** nằm trong bảng hàng hoá phía trên và không nằm trong dòng TỔNG/TSLN dòng TỔNG của bảng đó (`marginPercentGoods` EDIT:1919-1925 loại VC).

### 1.4 Tỷ suất lợi nhuận (TSLN) — tính trên GIÁ VỐN (markup), không phải trên doanh thu
- **TSLN trước GG** = (Tổng Thành tiền trước VAT − Tổng Thành tiền nhập) / Tổng Thành tiền nhập × 100, làm tròn 2 số lẻ (EDIT:1904-1910). Tổng nhập = 0 ⇒ 0%.
- **TSLN sau GG** = (Tổng Thành tiền sau GG − Tổng Thành tiền nhập) / Tổng Thành tiền nhập × 100 (EDIT:1911-1918). Đây cũng là "LN" ở footer và dùng tính cấp duyệt.
- **TSLN dòng** (cột "Tỷ suất LN" của từng dòng hàng/dịch vụ) = (Thành tiền sau GG của dòng − Thành tiền nhập của dòng) / Thành tiền nhập × 100; Thành tiền nhập = 0 ⇒ hiện `—` (EDIT:2589-2601). Hàng ERP mà user không có quyền xem giá vốn ⇒ `—`.
- **Màu TSLN dòng / dòng TỔNG / footer LN**: so với cấu hình "Tỷ suất lợi nhuận mức sàn" (`$store.state.profit_margin_threshold`): < ngưỡng ⇒ đỏ, ≥ ngưỡng ⇒ xanh (EDIT:2602-2608).
- ⇒ Giảm giá làm GIẢM TSLN dòng (GG mặt hàng: trừ `GG_dv × SL`; GG tổng: trừ số Phân bổ GG của dòng) và giảm TSLN tổng (TSLN sau GG).
- BE (gửi duyệt/cấp duyệt): `calculateTotals()` SVC:3585-3683 — `margin = (total_sale_after_discount − total_import)/total_import × 100` (2 số lẻ). **Lưu ý lệch nhỏ**: BE tính tổng giá nhập của cha-có-con = Σ giá nhập các con (SVC:3600-3611), FE tính theo giá nhập dòng cha (roll-up). Với cha là hàng tạm hai số bằng nhau (cha tự cộng từ con); với cha ERP (combo) có thể khác ⇒ TSLN ở popup Gửi duyệt có thể khác TSLN trên màn.

### 1.5 Footer giá (thanh dính đáy, EDIT:1201-1234)
Từ trái sang:
- **Nhập:** tổng thành tiền nhập + mã tiền (`—` nếu không có quyền xem giá vốn)
- **Bán:** tổng thành tiền trước VAT (GỒM vận chuyển)
- **GG:** tổng giảm giá (chữ đỏ) — chỉ khi có phương thức GG
- **Sau GG:** tổng sau GG — chỉ khi có phương thức GG
- **~VND:** = Tổng sau GG × tỷ giá — chỉ khi tỷ giá ≠ 1 (ngoại tệ) (EDIT:1799 `totalSaleVnd`)
- **LN:** TSLN sau GG % (chỉ khi có quyền xem giá vốn)
- **Cấp duyệt:** badge `C1 — Tự duyệt` / `C2 — TP` / `C3 — TP & BGĐ` / `—` (chỉ khi có quyền xem giá vốn). Tính tạm ở FE: MAX(cấp theo giá trị đơn hàng quy VND, cấp theo TSLN) theo bảng cấu hình duyệt giá (EDIT:1816-1821, `findLevelByConfig` EDIT:3302-3312: min ≤ giá trị < max; không khớp cấu hình nào ⇒ cấp 3). Chưa có doanh thu ⇒ `—`.
  - **Lệch FE/BE cần ghi chú**: BE còn xét thêm tiêu chí thứ 3 "tỷ suất lợi nhuận của dòng hàng tạm thấp nhất" (Redmine #10898) và luật "tự động duyệt" (SVC:3524-3583) ⇒ cấp hiển thị ở footer chỉ là THAM KHẢO; cấp chính thức là cấp ở popup Gửi duyệt.

### 1.6 Làm tròn & định dạng số
- Hiển thị số: định dạng quốc tế `1,234,567.89`, số chữ số lẻ theo chế độ "Làm tròn" đang chọn (`formatMoney` EDIT:2549-2554; `roundingPrecision` EDIT:2073-2076: chưa chọn ⇒ tối đa 2 số lẻ).
- Select **"Làm tròn"** (EDIT:322-344): `Mặc định (tối đa 2 số lẻ)` · `Hàng nghìn (-3)` · `Hàng trăm (-2)` · `Hàng chục (-1)` · `Số nguyên (0)` · `1 số lẻ (1)` · `2 số lẻ (2)`. Tooltip ⓘ: *"Khi bấm Áp dụng, hệ thống tự động tính toán giá trị làm tròn dựa trên cấu hình, giá trị làm tròn áp dụng với các cột GIÁ NHẬP, GIÁ BÁN"*.
  - Tiền **VNĐ**: khoá cứng "Số nguyên (0)", select bị disable, tooltip *"Đồng VNĐ mặc định làm tròn đến số nguyên"* (EDIT:1779-1783, watcher EDIT:2265-2267). JPY/KRW: mặc định Số nguyên nhưng vẫn đổi được. Ngoại tệ khác: mặc định 2 số lẻ.
  - Nút **"Áp dụng"** (ẩn tác dụng khi chưa chọn) → popup xác nhận: tiêu đề **"Xác nhận làm tròn giá"**, nội dung **"Bạn có chắc muốn làm tròn đến <hàng nghìn|hàng trăm|hàng chục|số nguyên|1 số thập phân|2 số thập phân> cho toàn bộ đơn giá? Thao tác này không thể hoàn tác."**, nút **"Áp dụng"** (EDIT:3245-3255). Đồng ý ⇒ làm tròn: giá nhập của dòng không có con + giá bán của dòng cha/độc lập + giá nhập/giá bán dịch vụ; toast **"Đã làm tròn đơn giá"** (EDIT:3256-3287). Giá trị làm tròn được lưu (`rounding_mode`).
- Ví dụ tính đã kiểm theo công thức ở mục 1.7.

### 1.7 Ví dụ minh hoạ (VNĐ)
Dữ liệu: Hàng A SL 2, GN 1,000,000, GB 1,300,000, VAT 10% · Hàng B SL 1, GN 500,000, GB 600,000, VAT 8% · Dịch vụ lắp đặt SL 1, GN 200,000, GB 400,000, VAT 8% · Vận chuyển: giá nhập 100,000, chi phí 150,000, VAT 8%.

**(a) Không GG**
| | Thành tiền nhập | Trước VAT | Thuế VAT | Sau VAT |
|---|---|---|---|---|
| I Hàng hoá | 2,500,000 | 3,200,000 | 308,000 (260,000 + 48,000) | 3,508,000 |
| II Dịch vụ | 200,000 | 400,000 | 32,000 | 432,000 |
| III Chi phí | 0 | 0 | 0 | 0 |
| IV Vận chuyển | 100,000 | 150,000 | 12,000 | 162,000 |
| V Tổng | 2,800,000 | 3,750,000 | 352,000 | **4,102,000 VND** |
TSLN = (3,750,000 − 2,800,000)/2,800,000 = **33.93%**.

**(b) GG tổng: 1 khoản 10%** → cơ sở % = 3,200,000 + 400,000 + 150,000 = 3,750,000 ⇒ Thành tiền GG = **375,000**. Bấm "Phân bổ tự động": A 260,000 · B 60,000 · DV 40,000 · VC 15,000 (theo tỷ lệ thành tiền trước VAT).
- Sau GG = 3,375,000; VAT = 234,000 + 43,200 + 28,800 + 10,800 = 316,800; Tổng sau VAT = **3,691,800**.
- TSLN trước GG 33.93% · TSLN sau GG = (3,375,000 − 2,800,000)/2,800,000 = **20.54%**. TSLN dòng A = (2,340,000 − 2,000,000)/2,000,000 = 17%.

**(c) GG mặt hàng: A giảm 10%** ⇒ GG(₫) = 130,000/đơn vị, Đơn giá sau GG = 1,170,000, Giảm giá dòng = 260,000; VAT A = 2,340,000 × 10% = 234,000.

---

## 2. VAT

### 2.1 VAT theo DÒNG, không có VAT chung cho cả báo giá
- Cột **"VAT(%)"** ở từng dòng, tooltip ⓘ: *"VAT chỉ áp dụng trên dòng CHA hoặc SP độc lập. SP con được cộng gộp vào CHA."* (EDIT:449-456). Thêm 2 cột **"Tiền VAT"**, **"Thành tiền sau VAT"**.
- **Hàng ERP**: ô VAT **khoá**, tooltip *"VAT lấy từ danh mục hàng hoá ERP"* (EDIT:677-690 trong bảng). BE luôn ghi đè VAT hàng ERP bằng `products.vat_percent` của ERP khi lưu (`enforceErpProductVat` SVC:3253-3279) — FE gửi gì cũng bị thay.
- **Hàng tạm (tự nhập)**: nhập tay 0–100.
- **Dịch vụ & Chi phí khác**: ô VAT nhập tay được (EDIT:907-912). Khi thêm từ danh mục chi phí ERP, VAT lấy theo danh mục; BE: FE gửi giá trị nào thì giữ, thiếu thì lấy VAT danh mục, không có ⇒ 0 (`resolveServiceVat` SVC:3230-3243).
- **Vận chuyển**: cố định 8%, khoá (mục 1.3).
- Ràng buộc: 0 ≤ VAT ≤ 100; lỗi inline **"VAT phải trong 0–100%"** (EDIT:2834-2843). Kiểm ở **cả Lưu nháp lẫn Gửi duyệt** (EDIT:3761-3770 `validateVat`). BE: `vat_percent: nullable|numeric|min:0|max:100` (REQ_S:61,93; REQ_U:60,96) → message chuẩn LANG "Không được lớn hơn 100." / "Không được nhỏ hơn 0.".

### 2.2 "Áp dụng VAT hàng loạt" — toolbar `VatBulkApplyToolbar` (hrm-client/components/assign/quotation/VatBulkApplyToolbar.vue; gắn ở EDIT:286-290)
- Giao diện: nhãn **"VAT:"** + ô số (placeholder **"%"**, 0–100, bước 0.01) + 2 nút: **"Tất cả"** (primary) và **"VAT=0"** (light). **Không có danh sách mức VAT cố định** — user tự gõ số %.
- Nút chỉ bấm được khi ô có giá trị hợp lệ 0–100 và báo giá đang sửa được (toolbar disable khi `!canEdit`) (VatBulkApplyToolbar.vue:57-64).
- Phạm vi áp:
  - **Tất cả**: ghi VAT cho MỌI dòng CHA/độc lập là **hàng tạm** (bỏ qua dòng con, bỏ qua hàng ERP).
  - **VAT=0**: chỉ những dòng hàng tạm cha/độc lập đang có VAT = 0.
  - **Dịch vụ & Chi phí khác KHÔNG được áp** (VAT lấy từ danh mục ERP), vận chuyển không áp (EDIT:4138-4152).
- Kết quả: toast **"Đã áp {x}% cho {n} dòng"** (EDIT:4132-4137). Ô nhập tự xoá trống.
- **Chỉ thay đổi trên màn hình** — chưa lưu DB cho tới khi bấm Lưu nháp/Gửi duyệt. Endpoint BE `POST assign/quotations/{id}/apply-vat-bulk` (CTL:1357-1366, SVC:4212-4279, rules REQ `QuotationApplyVatBulkRequest`: vat_percent required 0–100, mode `all|zero_only`; message riêng: "Vui lòng nhập VAT %", "VAT phải là số", "VAT không được âm", "VAT không được vượt quá 100%", "Thiếu phạm vi áp dụng", "Phạm vi áp dụng không hợp lệ"; service: "Báo giá đã gửi, không thể sửa VAT", "Chỉ người tạo báo giá mới được áp VAT") **hiện KHÔNG được màn này gọi** (chỉ còn action `quotation/applyVatBulk` trong `store/quotation.js` mà không nơi nào dispatch). Endpoint đó cũng chỉ chạy cho báo giá lập từ BOM (đọc `bomList`). ⇒ SRS mô tả theo hành vi FE.

### 2.3 Gợi ý áp VAT lần đầu — `VatFirstEntryPromptModal` (EDIT:4100-4131)
- Khi user lần ĐẦU (trong phiên) đổi VAT của 1 dòng hàng từ 0 sang số dương, và còn dòng cha/độc lập khác đang VAT = 0 ⇒ popup:
  - Tiêu đề **"Áp dụng VAT đồng loạt?"**
  - Nội dung **"Áp dụng {x}% VAT cho {n} sản phẩm còn đang để 0%?"**
  - Nút **"Chỉ dòng này"** (bỏ qua) · **"Áp dụng tất cả dòng còn 0%"**.
- Áp dụng ⇒ giống chế độ "VAT=0" ở trên (bỏ qua hàng ERP), toast **"Đã áp {x}% cho {n} dòng"**. Đóng popup bằng Esc/nền = bỏ qua. Chỉ hỏi 1 lần mỗi phiên mở màn.

### 2.4 Đổi VAT thì số nào tính lại
Tức thời trên màn (computed): Tiền VAT dòng, Thành tiền sau VAT dòng, dòng TỔNG bảng (Tiền VAT, Thành tiền sau VAT), khối Tổng hợp cột "Thuế VAT" + "Thành tiền sau VAT" của nhóm và dòng V. **Không đổi**: thành tiền trước VAT, giảm giá, TSLN, cấp duyệt (VAT không tham gia TSLN/cấp duyệt). BE khi lưu: `recomputeTotals()` ghi lại `total_vat_amount`, `total_after_vat` (SVC:3450-3458).

---

## 3. Giảm giá

### 3.1 Chọn phương thức — select **"GG:"** trên toolbar (EDIT:294-317)
Giá trị: **"Không GG"** · **"GG mặt hàng"** (=1) · **"GG tổng"** (=2). Lưu theo cả báo giá (`discount_method`).
- **Khoá select** khi:
  - Báo giá thuộc **dự án con**: kế thừa phương thức GG của dự án cha, icon 🔒 tooltip *"Kế thừa từ dự án cha, không sửa được"*. BE cũng ghi đè theo dự án (SVC:139-141 create; SVC:1900-1909 update).
  - User **không có quyền "Cho phép thêm giảm giá trong báo giá"**: icon 🔒 tooltip *"Bạn không có quyền áp dụng giảm giá trong báo giá"* (EDIT:1722-1727). Báo giá mới ⇒ mặc định Không GG.
- Đổi phương thức khi đang có dữ liệu GG (GG dòng > 0 hoặc có khoản GG tổng) ⇒ popup xác nhận (EDIT:2610-2631):
  - Tiêu đề **"Xác nhận đổi phương thức giảm giá"**, nội dung **"Thay đổi phương thức sẽ xóa dữ liệu giảm giá hiện tại. Tiếp tục?"**, nút **"Xác nhận"** (màu nguy hiểm).
  - Đồng ý ⇒ xoá toàn bộ GG(%), GG(₫), phân bổ của mọi dòng hàng/dịch vụ + phân bổ vận chuyển + toàn bộ khoản GG tổng (EDIT:2632-2650). Huỷ ⇒ select trả về giá trị cũ.
  - BE khi lưu đổi phương thức cũng tự xoá dữ liệu GG cũ (`clearDiscountData` SVC:4694-4717).

### 3.2 GG mặt hàng (phương thức 1)
- Bảng hàng thêm 3 cột: **"GG(%)"**, **"GG(₫)"**, **"Đơn giá sau GG"** (EDIT:428-430). Dịch vụ có cùng 3 cột. Vận chuyển nhập ở khối Tổng hợp.
- GG(%) và GG(₫) liên động 2 chiều, tính trên **1 đơn vị**:
  - Nhập % ⇒ GG(₫) = đơn giá bán × % / 100 (làm tròn 2 số lẻ) (EDIT:2711-2716).
  - Nhập ₫ ⇒ GG(%) = GG(₫) / đơn giá bán × 100 (4 số lẻ) (EDIT:2717-2722).
  - Hệ thống nhớ ô nào user nhập (`discount_input_mode` percent/amount) — dùng khi sao chép/đổi giá.
- Đơn giá sau GG = đơn giá bán − GG(₫). Thành tiền bán (sau GG) = (đơn giá bán − GG(₫)) × SL.
- Dòng TỔNG bảng cột GG(%) hiện **tổng tiền GG** = Σ GG(₫) × SL của dòng cha + dịch vụ (EDIT:2019-2027) (không gồm vận chuyển).
- Ràng buộc + thông báo (inline dưới ô):
  - **"GG (%) phải trong 0–100%"** — kiểm cả Lưu nháp lẫn Gửi duyệt (EDIT:2844-2849, 3699-3709).
  - **"GG không được lớn hơn đơn giá bán"** — kiểm khi Gửi duyệt (EDIT:2829-2833, 3851-3855; `validateDiscountPerItem` EDIT:2870-2893).
  - Vận chuyển: **"GG vận chuyển không được lớn hơn chi phí"** — khi Gửi duyệt (EDIT:3843-3846).
  - BE khi gửi duyệt: GG > đơn giá bán ⇒ gộp vào lỗi chung **"Có {n} sản phẩm/dịch vụ chưa hợp lệ (giá bán > 0, số lượng > 0, giảm giá ≤ đơn giá bán)."** (SVC:4729-4785). BE Request: `discount_percent` 0–100, `discount_amount` ≥ 0.

### 3.3 GG tổng (phương thức 2)
- Bảng hàng thêm 2 cột:
  - **"GG phân bổ tự động"** (ⓘ *"Tham khảo — tự tính theo tỷ lệ giá trị"*) — chỉ đọc, số gợi ý.
  - **"Phân bổ GG"** — ô nhập số tiền GG gán cho dòng (lưu DB). Tiêu đề cột kèm dòng nhỏ **"Còn: {Tổng GG − Đã phân bổ}"** (xanh khi khớp, đỏ khi lệch) (EDIT:432-445). Ô bị khoá khi Tổng GG = 0.
- Khối **"Giảm giá tổng đơn hàng"** (EDIT:955-1036), hiện khi phương thức = GG tổng VÀ (user có quyền giảm giá HOẶC báo giá đã có khoản GG — để người không quyền vẫn xem được) (EDIT:1735-1737):
  - Bảng cột: **"#"**, **"Loại GG"** (select danh mục Loại giảm giá, mỗi loại chỉ chọn 1 lần, option đầu "— Chọn loại GG —"), **"Kiểu"** (`%` / `₫`), **"Giá trị %" / "Giá trị ₫" / "Giá trị"** (nhãn đổi theo kiểu của các dòng, EDIT:2001-2009), **"Thành tiền GG"**, nút xoá dòng (thùng rác). Dòng cuối **"Tổng GG"**.
  - Nút **"Thêm khoản GG"** (dòng mới mặc định kiểu %, giá trị 0).
  - **Thành tiền GG** của khoản:
    - Kiểu %: = (Tổng thành tiền trước VAT của hàng hoá + dịch vụ + chi phí **+ chi phí vận chuyển**) × % / 100, làm tròn 2 số lẻ (EDIT:2735-2742).
    - Kiểu ₫: = số tiền nhập.
  - Validate từng khoản (inline, EDIT:2748-2759): **"Vui lòng chọn loại GG"**; giá trị ≤ 0 ⇒ **"Giá trị phải > 0"**; % > 100 ⇒ **"Giá trị tối đa 100%"**. Kiểm ở cả Lưu nháp và Gửi duyệt; riêng **Lưu nháp bỏ qua các dòng do hệ thống tự dựng theo Báo giá Mỏ neo mà Sale chưa nhập số** (EDIT:2760-2777).
  - Dòng trạng thái: **"Đã phân bổ: {đã phân bổ} / {Tổng GG} ✓"** (xanh, khi lệch < 1) hoặc **"… — Chênh lệch: {x}"** (đỏ) (EDIT:1028-1035; `allocationMatch` EDIT:2069-2071).
- **Phân bổ GG xuống dòng** (FE tự tính, EDIT:2078-2108 `autoAllocationMap` + `applyAutoAllocation` EDIT:2803-2815):
  - Nút **"Phân bổ tự động"** — hiện khi Tổng GG > 0 và chưa phân bổ đồng nào. Nút **"Phân bổ lại"** — hiện khi đã phân bổ nhưng lệch tổng, hoặc giá bán vừa thay đổi. Trong lúc chạy: "Đang phân bổ...".
  - Popup xác nhận: tiêu đề **"Phân bổ giảm giá tự động"**, nội dung **"Thao tác này sẽ ghi đè toàn bộ giá trị cột "Phân bổ GG" bằng giá trị phân bổ tự động (theo tỷ lệ giá trị). Bạn có chắc chắn?"**, nút **"Phân bổ"** (EDIT:2816-2828). Xong: toast **"Đã cập nhật cột Phân bổ GG theo phân bổ tự động"**.
  - **Công thức**: tập dòng = mọi dòng hàng CHA/độc lập + mọi dòng dịch vụ/chi phí + vận chuyển (nếu chi phí > 0). Phân bổ dòng = Tổng GG × (Thành tiền trước VAT của dòng / Tổng thành tiền trước VAT các dòng). Làm tròn theo **phương pháp phần dư lớn nhất** (Largest Remainder) ở mức 0.01 (FE tính theo "xu") để tổng phân bổ khớp CHÍNH XÁC Tổng GG: lấy phần nguyên trước, phần còn thiếu chia lần lượt cho các dòng có phần lẻ lớn nhất.
  - User có thể sửa tay từng ô "Phân bổ GG" sau khi phân bổ.
  - Đổi giá bán khi đã phân bổ ⇒ toast lỗi **"Giá bán đã thay đổi, vui lòng phân bổ lại giảm giá"** + hiện nút "Phân bổ lại" (EDIT:2894-2899). Đổi bảng giá làm đổi giá ERP cũng bật cờ phân bổ lại (EDIT:3601-3605).
  - BE có endpoint `POST {id}/allocate-discount` (CTL:1368-1378, SVC:4586-4692, cùng thuật toán nhưng làm tròn đến **đồng** — floor số nguyên) — **màn này KHÔNG gọi** (chỉ chạy được cho báo giá từ BOM). Thông báo của endpoint: "Báo giá không áp dụng giảm giá theo tổng.", "Tổng giá bán = 0, không thể phân bổ giảm giá. Vui lòng nhập giá bán trước.", thành công "Đã phân bổ giảm giá".
  - **Không có ràng buộc chặn "đã phân bổ ≠ Tổng GG"** khi Lưu/Gửi duyệt (chỉ cảnh báo màu đỏ). Số "Giảm giá" thực tế được tính bằng TỔNG CÁC Ô PHÂN BỔ (không phải Tổng GG) ⇒ nếu chưa phân bổ, Giảm giá trong Tổng hợp = 0 dù khối GG tổng có Tổng GG > 0. ⇒ cần ghi rõ trong SRS/test.
  - Báo giá dự án con có Báo giá Mỏ neo: hệ thống tự dựng sẵn các dòng "Loại GG" giống Mỏ neo (giá trị 0) và hiện banner (EDIT:258-282, `applyAnchorOnCreate` EDIT:2925-2950; BE `seedDiscountLinesFromAnchor` SVC:242).

### 3.4 Xoá giảm giá — nút **"Xóa giảm giá"** / **"Xóa phân bổ"** (Redmine #10900; EDIT:346-360, 2686-2710)
- Hiện khi có quyền sửa GG và đã chọn phương thức GG; bấm được khi có dữ liệu để xoá (GG mặt hàng: có dòng nào GG% hoặc GG₫ > 0; GG tổng: tổng đã phân bổ > 0).
- Nhãn: GG mặt hàng ⇒ **"Xóa giảm giá"**; GG tổng ⇒ **"Xóa phân bổ"**.
- Popup:
  - GG mặt hàng: tiêu đề **"Xóa dữ liệu giảm giá"**, nội dung **"Bạn có chắc chắn muốn xóa toàn bộ dữ liệu giảm giá?"**, nút **"Xóa giảm giá"**. ⇒ GG(%) và GG(₫) của mọi dòng hàng + dịch vụ về 0 (**không** đụng GG vận chuyển). Toast **"Đã xóa toàn bộ dữ liệu giảm giá"**.
  - GG tổng: tiêu đề **"Xóa phân bổ giảm giá"**, nội dung **"Bạn có chắc chắn muốn xóa toàn bộ giá trị phân bổ giảm giá? Tất cả giá trị tại cột Phân bổ GG sẽ được đặt về 0"**, nút **"Xóa phân bổ"**. ⇒ cột Phân bổ GG của mọi dòng + vận chuyển về 0, **GIỮ NGUYÊN** bảng khoản GG tổng. Toast **"Đã xóa toàn bộ phân bổ giảm giá"**.
- Chỉ thay đổi trên màn, lưu khi bấm Lưu nháp/Gửi duyệt.

### 3.5 Quyền **"Cho phép thêm giảm giá trong báo giá"** (#10789)
- FE (EDIT:1722-1737): không quyền ⇒ khoá select phương thức; các ô GG%/GG₫/Phân bổ GG/khoản GG tổng chuyển sang chỉ đọc (`canEditDiscount = canEdit && có quyền`); nút Thêm khoản GG / Phân bổ / Xóa ẩn; khối GG tổng ẩn nếu báo giá chưa có khoản GG.
  - Ngoại lệ đáng chú ý: ô GG vận chuyển (GG mặt hàng) và ô phân bổ vận chuyển chỉ gate theo `canEdit` (EDIT:1105-1113) — FE vẫn cho người không quyền gõ, nhưng BE sẽ chặn khi lưu.
- BE (SVC:4804-4884 `assertCanChangeDiscount`, gọi ở `create` SVC:53 và `update` SVC:1807): không có quyền mà payload **làm THAY ĐỔI** phương thức GG hoặc bất kỳ số GG nào (GG dòng hàng, dịch vụ, vận chuyển, phân bổ, khoản GG tổng) so với số đang lưu ⇒ chặn HTTP 403 **"Bạn không có quyền áp dụng giảm giá trong báo giá"**. Giữ nguyên GG cũ thì vẫn lưu được.
- Toast lỗi 403 do interceptor axios hiển thị (EDIT:3972-3976 không bắn trùng).

---

## 4. Điều khoản báo giá · Ghi chú nội bộ · Ghi chú kinh doanh

### 4.1 Mục "Thanh toán & Ghi chú nội bộ" (khối thu gọn được, EDIT:1155-1198)
- **Điều khoản báo giá** (nhãn có dấu `*` bắt buộc):
  - Select **"Mẫu điều khoản báo giá"** (cho xoá) — chỉ hiện khi đang sửa được (EDIT:1166-1174). Danh sách lấy từ danh mục ERP "Mẫu điều khoản báo giá" loại *Báo giá dự án*, sắp xếp theo tiêu đề (CTL:954-966 → `TpQuotationTerm::getForSelect` Modules/Human/Entities/TpQuotationTerm.php:28-34). Hiển thị theo `title`.
  - Ô soạn thảo rich text (cao 180px) chứa nội dung điều khoản.
  - Chọn mẫu ⇒ **điền nhanh / GHI ĐÈ** nội dung ô (EDIT:2976-3006). Nếu ô đang có nội dung (bỏ thẻ HTML vẫn còn chữ) ⇒ popup: tiêu đề **"Xác nhận thay đổi mẫu điều khoản"**, nội dung **"Nếu bạn thay đổi mẫu điều khoản, thông tin điều khoản báo giá sẽ bị thay đổi! Bạn có chắc chắn muốn thực hiện?"**, nút **"Xác nhận"**. Huỷ ⇒ select quay về mẫu trước, nội dung giữ nguyên. Ô trống ⇒ điền luôn không hỏi.
  - Mẫu chỉ hỗ trợ điền — **không lưu mẫu nào đã chọn**, chỉ lưu nội dung (`payment_terms`) (comment EDIT:1478). Sau khi điền vẫn sửa tay được.
  - Nội dung được giữ nguyên các biến `{{TOKEN}}` khi lưu; chỉ thay giá trị khi hiển thị/in (`hrm-client/utils/assign/quotation-term.js`: VAT_NOTE → "Giá trên đã bao gồm thuế VAT"/"Giá trên chưa bao gồm thuế VAT", VAN_CHUYEN_NOTE → "đã bao gồm chi phí vận chuyển"/"chưa bao gồm chi phí vận chuyển", NGAY/THANG/NAM, SO_BAO_GIA, NGAY_BAO_GIA, HIEU_LUC_BAO_GIA…; token lạ ⇒ để trống).
  - Bắt buộc **khi Gửi duyệt** (Lưu nháp cho trống): FE lỗi inline **"Vui lòng nhập điều khoản thanh toán"** (EDIT:3678-3681); BE **"Vui lòng nhập điều khoản thanh toán trước khi gửi duyệt."** (SVC:3799-3801).
  - In ra bản in báo giá (mục "Điều khoản báo giá:" — QuotationPrintPreview.vue:225-227).
- **Ghi chú nội bộ (chỉ nội bộ)** — rich text cao 140px, không bắt buộc (EDIT:1187-1196). Lưu vào `note`. **Không in ra bản in báo giá gửi khách** (QuotationPrintPreview chỉ in `payment_terms` và `sales_note`). Hiện ở màn Chi tiết dòng "Ghi chú nội bộ" khi có nội dung (pages/assign/quotations/_id/index.vue:636-641) — ai mở được báo giá đều xem được (không có gate riêng). Sao chép báo giá ⇒ copy sang.
- Ô bị khoá (disabled) khi báo giá không sửa được.
- (Khác) Mỗi dòng hàng ERP có "Ghi chú nội bộ" của hàng hoá do BE lấy từ ERP, chỉ đọc (`InternalNoteLine`, `enforceErpInternalNote` SVC:3281) — không thuộc mục này.

### 4.2 Ghi chú Kinh doanh (`sales_note`) — KHÔNG có trên màn Tạo/Sửa
- Chỉ có ở **màn Chi tiết** khi báo giá **Đã duyệt** (status 4): dòng **"Ghi chú Kinh doanh"** (pages/assign/quotations/_id/index.vue:642-660); NV Kinh doanh phụ trách dự án được sửa (textarea placeholder "Nhập ghi chú kinh doanh..."), người khác chỉ xem. Lưu ⇒ `PUT {id}/sales-note`, toast "Đã lưu ghi chú" (index.vue:1588-1601). Cũng sửa được từ tab Báo giá của dự án (ProspectiveProjectQuotationsTab.vue:547-554).
- BE `updateSalesNote` SVC:4281-4319: chỉ khi Đã duyệt ("Chỉ có thể sửa ghi chú khi báo giá đã duyệt."); báo giá có dự án ⇒ chỉ NV KD phụ trách ("Chỉ NV Kinh doanh phụ trách dự án mới có thể cập nhật ghi chú."); không dự án ⇒ chỉ người lập ("Chỉ người lập báo giá mới có thể cập nhật ghi chú."). Thành công "Đã cập nhật ghi chú". Có ghi lịch sử.
- **In ra bản in** (mục "Ghi chú:" — QuotationPrintPreview.vue:229-233).
- Sao chép báo giá ⇒ **không** copy (reset null, SVC:369).

---

## 5. Lưu nháp / Gửi duyệt

### 5.1 Nút ở footer (EDIT:1235-1248) — giống nhau ở Tạo mới, Sửa, Sao chép
| Nút (chữ UI) | Kiểu | Hiện khi | Hành động |
|---|---|---|---|
| **Quay lại** | light, icon mũi tên trái | luôn | về danh sách báo giá |
| **Lưu nháp** | secondary, icon đĩa | `canEdit` | `handleSaveDraft()` |
| **Gửi duyệt** | primary, icon máy bay giấy | `canEdit` | `openSubmit()` |
- `canEdit` (EDIT:1715-1720): Tạo mới ⇒ luôn true. Sửa ⇒ chỉ khi **trạng thái = Đang tạo** VÀ **người đang đăng nhập là người tạo** báo giá.
- Lưu ý: footer là khối tự dựng `pricing-footer`, KHÔNG dùng `V2Footer` (lệch quy ước dự án — chỉ ghi nhận).
- Đang lưu: nút Lưu nháp hiện loading, cả 2 nút không bấm được.

### 5.2 Validate — ma trận Lưu nháp vs Gửi duyệt (FE `save()` EDIT:3761-3984)
Mọi lỗi hiển thị **inline tại ô** (viền đỏ + chữ đỏ), không toast; màn tự cuộn tới ô lỗi đầu tiên (EDIT:3744-3760).

| Kiểm tra | Lưu nháp | Gửi duyệt | Thông báo nguyên văn (FE) |
|---|---|---|---|
| VAT dòng hàng/dịch vụ/vận chuyển 0–100 | ✔ | ✔ | "VAT phải trong 0–100%" |
| GG(%) dòng 0–100 (GG mặt hàng); % khoản GG tổng 0–100 | ✔ | ✔ | "GG (%) phải trong 0–100%" / "Giá trị tối đa 100%" |
| Khoản GG tổng: chọn loại + giá trị > 0 | ✔ (bỏ qua dòng Mỏ neo chưa nhập) | ✔ | "Vui lòng chọn loại GG" / "Giá trị phải > 0" |
| Báo giá không dự án phải chọn Khách hàng (chỉ Tạo mới) | ✔ | ✔ | inline "Bắt buộc phải nhập" + toast "Vui lòng chọn dự án hoặc khách hàng trước khi tạo báo giá" (EDIT:3933-3938) |
| Giao hàng (ngày) > 0 | — | ✔ | "Vui lòng nhập thời gian giao hàng" |
| Loại tiền tệ | — | ✔ | "Vui lòng chọn loại tiền tệ" |
| Bảng giá | — | ✔ | "Vui lòng chọn bảng giá" |
| Điều khoản báo giá (có chữ) | — | ✔ | "Vui lòng nhập điều khoản thanh toán" |
| Giai đoạn dự án (khi có dự án) | — | ✔ | "Vui lòng chọn giai đoạn dự án" |
| Giá bán dòng cha/độc lập > 0 | — | ✔ | "Giá / thành tiền bán phải > 0" |
| Giá nhập > 0 với **hàng tạm** không có con (hàng ERP được = 0) | — | ✔ | "Giá nhập phải > 0" |
| Dịch vụ: có tên, SL > 0, giá bán > 0 | — | ✔ | (ô đỏ) |
| Thành tiền bán SAU GG mỗi dòng hàng/dịch vụ > 0 | — | ✔ | "Giá / thành tiền bán phải > 0" |
| Giá bán cha (hàng tạm có con) ≥ Σ giá bán con | — | ✔ | "Giá bán hàng cha phải ≥ tổng giá bán hàng con" |
| Giá vốn cha (hàng tạm có con) ≥ Σ giá vốn con (chỉ khi có quyền xem giá vốn) | — | ✔ | "Giá vốn cha phải ≥ tổng giá vốn con" |
| Vận chuyển: chi phí, giá nhập ≥ 0 | — | ✔ | "Chi phí vận chuyển không hợp lệ" / "Giá nhập không hợp lệ" |
| GG vận chuyển ≤ chi phí (GG mặt hàng) | — | ✔ | "GG vận chuyển không được lớn hơn chi phí" |
| GG(₫) dòng ≤ đơn giá bán (GG mặt hàng) | — | ✔ | "GG không được lớn hơn đơn giá bán" |
- **KHÔNG có** kiểm tra "phải có ít nhất 1 hàng hoá" ở FE. BE khi gửi duyệt cũng không chặn báo giá rỗng (chỉ không cho "tự động duyệt" báo giá rỗng — SVC:3568-3569).
- **KHÔNG chặn giá bán < giá vốn**: chỉ thể hiện qua TSLN âm (màu đỏ) và đẩy cấp duyệt lên cao.
- Cảnh báo **đơn giá bán ≤ 1,000** (mục 5.4) — không chặn.

**BE — Request (Lưu nháp + nền cho Gửi duyệt)** — REQ_S:17-99, REQ_U:17-102, không khai `messages()` ⇒ dùng câu chuẩn LANG:
- `price_type_id`: **bắt buộc khi tạo** (`required|in:1..6`) — "Bắt buộc phải nhập" / "Không hợp lệ" (LANG:99, 60). Khi sửa: không bắt buộc.
- `customer_id`: bắt buộc khi không có cả dự án lẫn YCBG (`required_without_all`) — "Bắt buộc phải nhập" (LANG:105); phải tồn tại — "Không tồn tại".
- `project_id`, `project_phase_id`, `pricing_request_id`, `copied_from_quotation_id`: `exists` — "Không tồn tại".
- `customer_email`: email, ≤ 255 — "Định dạng email không hợp lệ" / "Vui lòng nhập tối đa 255 ký tự.".
- Số tiền/SL (`qty_needed`, `estimated_price`, `quoted_price`, `discount_amount`, `allocated_discount_amount`, `shipping_*`): `numeric|min:0` — "Không hợp lệ" / "Không được nhỏ hơn 0.".
- VAT, GG%: `min:0|max:100` — "Không được lớn hơn 100.".
- `rounding_mode`: `between:-3,2` — "Phải nằm trong khoảng -3 đến 2.".
- Tên nhóm (`groups.*.name`) và tên dịch vụ (`service_items.*.name`): bắt buộc, ≤ 255.
- Khoản GG tổng: `discount_type_id` + `input_mode` (`percent|amount`) bắt buộc khi có dòng.
- Chọn **dự án cha** ⇒ lỗi **"Dự án cha không lập báo giá riêng. Vui lòng tạo báo giá trên dự án con, hoặc dùng Báo giá tổng ở màn dự án cha."** (Concerns/RejectsParentProject.php:28-41).
- Lỗi lưu khác: toast = message BE hoặc **"Lỗi lưu"** (EDIT:3972-3976). Update trả message validate đầu tiên (CTL:614-617).

**BE — chốt quyền khi Tạo (Lưu nháp / Xem trước / Tạo+Gửi)** — `prepareStoreData` CTL:246-300:
- Lập từ Yêu cầu xây dựng giá (YCBG): dự án triển khai theo phòng ⇒ cần quyền **"Xây dựng giá bán theo phòng"** (403 "Bạn không có quyền xây dựng giá bán theo phòng.") và YCBG phải cùng phòng (403 "Yêu cầu xây dựng giá này không thuộc phòng ban của bạn."); ngược lại cần **"Xây dựng giá bán theo công ty"** (403 "Bạn không có quyền xây dựng giá bán theo công ty.").
- Báo giá tự lập có dự án: chỉ **Sale phụ trách dự án** (403 **"Bạn không phải Sale phụ trách dự án này"**).
- Không dự án: ai vào được màn đều tạo được.
- Route tạo/sửa/gửi duyệt **không gắn middleware checkPermission** (Modules/Assign/Routes/api.php:634-646).

**BE — chốt khi Sửa** — `ensureEditableByCreator` SVC:4719-4727: **"Báo giá không ở trạng thái Đang tạo, không thể sửa."** · **"Chỉ người tạo báo giá mới có thể sửa."**

**BE — chốt khi Gửi duyệt** — `assertSubmittable` SVC:3796-3812 (chạy ở submit, preview-submit, create-and-submit):
1. Đang tạo + người tạo (2 câu trên).
2. **"Vui lòng nhập điều khoản thanh toán trước khi gửi duyệt."**
3. Có dự án mà chưa chọn giai đoạn: **"Vui lòng chọn giai đoạn dự án trước khi gửi duyệt."**
4. `ensureAllPricesPositive` SVC:4729-4785: **"Có {n} sản phẩm/dịch vụ chưa hợp lệ (giá bán > 0, số lượng > 0, giảm giá ≤ đơn giá bán)."** — ⚠️ phần HÀNG HOÁ của kiểm tra này join `bom_list_products` nên **chỉ có tác dụng với báo giá lập từ BOM**; báo giá tự lập chỉ được BE kiểm phần dịch vụ (hàng hoá dựa vào FE). Ghi nhận như rủi ro.
5. **"Giá bán hàng cha "{tên}" phải ≥ tổng giá bán hàng con."** (SVC:2326-2369; bỏ qua cha ERP).
6. **"Giá vốn hàng cha "{tên}" đang nhỏ hơn tổng giá vốn hàng con."** (SVC:2376-2418; bỏ qua cha ERP).
7. Lệch Báo giá Mỏ neo: **"KHÔNG THỂ TRÌNH DUYỆT — báo giá không khớp với Báo giá Mỏ neo {mã}, không đủ điều kiện tổng hợp hợp đồng.\n• {lỗi 1}\n• {lỗi 2}…"** (SVC:3767-3794).
- Ngoài ra mọi lần lưu: cha là hàng tạm mà gắn con là hàng ERP khi không có quyền "Xem giá vốn hàng hoá" ⇒ **"Bạn không có quyền "Xem giá vốn hàng hoá" nên không thể chọn hàng ERP làm hàng con."** (SVC:2281-2319).

### 5.3 Luồng **Lưu nháp**
- Tạo mới / Sao chép (chưa có id): `POST assign/quotations` (CTL:304-317 → `create()` SVC:50-270). Thành công: toast **"Đã tạo báo giá"** → về **danh sách báo giá** (EDIT:3958-3972).
- Sửa: `PUT assign/quotations/{id}` (CTL:608-626 → `update()` SVC:1804-2113). Thành công: toast **"Đã lưu báo giá"** → về **danh sách báo giá** (EDIT:3962-3966).
- Sau Lưu nháp: nếu báo giá lệch Báo giá Mỏ neo ⇒ toast cảnh báo mềm **"Lưu ý: {lỗi đầu tiên} Hệ thống vẫn lưu nháp, nhưng cần đồng bộ trước khi Trình duyệt."** (EDIT:4004-4011). (Thực tế đã điều hướng về danh sách nên toast có thể kịp/không kịp hiện.)
- Báo giá được tạo luôn ở trạng thái **Đang tạo**; nếu dự án đang ở trạng thái thấp hơn "Dự toán" ⇒ dự án tự chuyển sang **Dự toán** (SVC:236-238). Lưu nháp **không** đồng bộ Giai đoạn dự án về dự án (chỉ làm lúc Gửi duyệt).
- **Mã báo giá**: sinh lúc tạo bản ghi, dạng **`BG-YYYY-NNNNN`** = `BG-` + năm hiện tại + (id lớn nhất hiện có + 1) đệm 5 số (Quotation.php:342-346). Do Xem trước gửi duyệt tạo bản ghi tạm rồi huỷ, số thứ tự có thể bị nhảy (SVC:3819-3822). Mã dòng dịch vụ: **`DV-<mã báo giá>-NNN`** (QuotationServiceItem.php:62-71). Mã hàng tạm: `HHBG…` do BE sinh lúc lưu; trước khi lưu cột Mã của hàng tạm để trống (EDIT:3997-4002).
- Hiệu lực báo giá (`validity_date`) BE tính lại mỗi lần lưu = MIN(hôm nay + số ngày hiệu lực cấu hình ERP (mặc định 30), ngày điều chỉnh giá gần nhất trong tương lai của hàng ERP cha) (SVC:5141-5180).
- Lịch sử: tạo ⇒ "create"; sửa ⇒ 1 dòng "Thay đổi thông tin" chỉ gồm trường/dòng đã đổi (SVC:2097-2098).
- Mở màn Sửa mà giá ERP đã đổi so với giá đã lưu ⇒ popup **"Đơn giá hàng hoá đã thay đổi"**: *"Có sự thay đổi về đơn giá của một số hàng hóa. Bạn có muốn cập nhật đơn giá theo thời giá hiện tại không?"* + danh sách tối đa 10 dòng "Tên: giá cũ → **giá mới** VNĐ" (+ "… và n hàng hoá khác"), nút **"Đồng ý"** / **"Từ chối"** (EDIT:3531-3608). Từ chối ⇒ khi lưu BE giữ nguyên đơn giá đã lưu (`keep_saved_erp_prices`); Đồng ý ⇒ áp giá mới, VAT ERP mới. (Không chọn gì vẫn ⇒ khi lưu BE luôn áp giá ERP hiện hành — `enforceErpProductPrice` SVC:2268-2272.)

### 5.4 Luồng **Gửi duyệt**
**A. Màn Sửa (đã có id)** — `openSubmit()` EDIT:4012-4038:
1. Validate đầy đủ (mục 5.2) rồi **LƯU luôn** (`PUT`, không toast, không điều hướng) — tức là bấm Gửi duyệt đã ghi dữ liệu xuống DB kể cả khi sau đó user bấm Huỷ ở popup.
2. Kiểm Mỏ neo: lệch ⇒ popup **"Không thể trình duyệt — vi phạm quy tắc đồng bộ"**: *"Báo giá này không khớp với Báo giá Mỏ neo {mã}, không đủ điều kiện để tổng hợp hợp đồng. Vui lòng sửa các lỗi sau:"* + danh sách lỗi; nút **"Đóng"** (EDIT:1280-1296).
3. Có dòng hàng (cha hoặc con) có **đơn giá bán ≤ 1,000** ⇒ tô nền cam các dòng đó + popup cảnh báo `QuotationLowPriceWarningModal`: tiêu đề **"Cảnh báo: Tồn tại mặt hàng có đơn giá <= 1.000 vnđ"**, nội dung **"Hệ thống phát hiện báo giá đang chứa {n} mặt hàng chưa được cập nhật giá bán hoặc là hàng khuyến mãi/giảm giá."** + bảng STT / Mã hàng hóa / Tên hàng hóa / Đơn giá bán; nút **"Tiếp tục gửi duyệt"** (cam) / **"Quay lại"** (EDIT:1742-1754; component hrm-client/components/assign/quotation/QuotationLowPriceWarningModal.vue). Không chặn.
4. Mở popup **"Gửi duyệt báo giá"** (SUBMIT_MODAL) — gọi `POST {id}/calculate-level` (CTL:640-648 → `calculateLevel` SVC:3524-3545).

**B. Màn Tạo mới / Sao chép (chưa có id)** — `openSubmitOnCreate()` EDIT:4049-4090 (Redmine "quotation-submit-no-draft"):
1. Validate đầy đủ, dựng payload, **chưa ghi DB**.
2. Cảnh báo đơn giá ≤ 1,000 (như trên).
3. `POST assign/quotations/preview-submit` (CTL:324-336 → `previewSubmit` SVC:3824-3849): BE tạo báo giá tạm + chạy toàn bộ chốt Gửi duyệt + tính cấp rồi **huỷ (rollback)**. Lỗi ⇒ popup **"Không thể gửi duyệt báo giá"** hiện nguyên văn lý do BE (nhiều dòng), nút **"Đóng"** (EDIT:1261-1270); mặc định "Không thể gửi duyệt báo giá". Không có dữ liệu cấp ⇒ toast **"Không tính được cấp duyệt. Vui lòng kiểm tra giá sản phẩm."**
4. Mở popup "Gửi duyệt báo giá" với số liệu xem trước.

**Popup "Gửi duyệt báo giá"** (SUBMIT_MODAL:1-62, 96-117):
- Đang tải: "Đang tính cấp duyệt...". Không tính được: khung đỏ **"Không tính được cấp duyệt. Vui lòng kiểm tra giá sản phẩm."**
- Ô số liệu: **Tổng giá nhập** (chỉ khi có quyền xem giá vốn) · **Tổng giá bán** · **Tổng giảm giá** + **Tổng bán sau GG** (khi có GG) · **Tỷ suất LN** (khi có quyền; xanh ≥ 20%, cam ≥ 10%, đỏ < 10% — ngưỡng cứng trong popup, khác ngưỡng màu trên màn) · **Cấp duyệt dự kiến** ("Cấp 1/2/3" hoặc "Tự động duyệt"). Các số kèm mã tiền.
  - Lưu ý: "Tổng giá bán" ở popup = tổng thành tiền trước VAT gồm cả vận chuyển (`total_sale` SVC:3626).
- Thông điệp theo cấp:
  - Tự động duyệt: **"Báo giá chỉ gồm hàng hoá/dịch vụ đã khai báo trên ERP, đơn giá bán > 1.000 đ và không có giảm giá — hệ thống tự động duyệt."**
  - Cấp 1: **"Theo quy chế, bạn có thể tự duyệt báo giá này."**
  - Cấp 2: **"Theo quy chế, báo giá cần gửi tới Trưởng phòng duyệt."**
  - Cấp 3: **"Theo quy chế, báo giá cần gửi qua 2 cấp duyệt:"** + 2 bước "① Trưởng phòng duyệt & chuyển BGĐ → ② Ban giám đốc duyệt".
- Nút: **"Xác nhận duyệt"** (cấp 1) hoặc **"Xác nhận gửi"** (cấp 2/3) · **"Huỷ"**.
- **Cách tính cấp** (SVC:3524-3545 + BomPriceApprovalConfigService::calculateApprovalLevel): cấp = MAX( cấp theo **giá trị đơn hàng sau GG quy VND**, cấp theo **TSLN sau GG**, cấp theo **TSLN thấp nhất của các dòng hàng tạm** ) tra bảng cấu hình duyệt giá (min ≤ giá trị < max; không khớp ⇒ cấp 3). Dòng hàng tạm có giá nhập = 0 ⇒ TSLN dòng = 0% (không lách được). **Tự động duyệt** (ép cấp 1) khi: không chọn phương thức GG, không có tiền GG, không có khoản GG tổng; mọi dòng hàng là hàng ERP và mọi dịch vụ từ danh mục; mọi đơn giá bán > 1,000; báo giá không rỗng (SVC:3558-3583).
- Bấm xác nhận:
  - Màn Sửa: cấp 1 ⇒ `POST {id}/submit` rồi `POST {id}/self-approve` ⇒ toast **"Đã tự duyệt báo giá"**; cấp 2/3 ⇒ `POST {id}/submit` ⇒ toast **"Đã gửi duyệt báo giá"**. Lỗi ⇒ toast message BE hoặc "Không thể gửi duyệt".
  - Màn Tạo mới/Sao chép: `POST create-and-submit` (CTL:342-360 → SVC:3855-3881) — tạo + gửi (+ tự duyệt nếu cấp 1) trong **1 giao dịch**, lỗi thì không để lại báo giá nào. Nếu lúc này cấp thực tế đổi thành cấp 1 mà popup chưa chọn tự duyệt ⇒ lỗi **"Cấp duyệt của báo giá vừa thay đổi thành cấp 1 (tự duyệt). Vui lòng bấm Gửi duyệt lại để xác nhận."**
  - Thành công ⇒ đóng popup, về **danh sách báo giá** (EDIT:4096-4098).
- **Kết quả trạng thái** (SVC:3883-3921, 3923-3958):
  - Cấp 1: gán cấp 1 ⇒ tự duyệt ⇒ trạng thái **Đã duyệt**, ghi người duyệt/thời gian, YCBG (nếu có) chuyển "Đã có báo giá", đồng bộ lên ERP, thông báo "đã duyệt".
  - Cấp 2/3: trạng thái **Chờ TP duyệt**, ghi `submitted_at`, xoá lý do từ chối cũ, lưu cấp duyệt.
  - Mọi cấp: **đồng bộ Giai đoạn dự án của báo giá về dự án gốc** (SVC:3888-3891); tính lại tổng + hiệu lực.
- **Thông báo khi gửi duyệt** (SVC:3914-3917, 5054-5075): gửi tới **những người có quyền "Trưởng phòng duyệt giá Bom giải pháp" thuộc/quản lý đúng phòng ban của báo giá (cùng công ty)**; nội dung: **"<b>{Tên người gửi}</b> gửi duyệt báo giá (cấp TP) <b>{Mã BG}</b>"** hoặc **"(cấp TP + BGĐ)"** với cấp 3; link tới màn **Báo giá chờ duyệt**. Cấp 1 tự duyệt ⇒ không gửi thông báo "gửi duyệt" mà gửi thông báo "đã duyệt": **"<b>{Tên}</b> đã duyệt báo giá <b>{Mã}</b>"** tới người lập + NV KD phụ trách dự án + TP duyệt giá của phòng (SVC:5077-5110), link tới chi tiết báo giá.

### 5.5 Cảnh báo thoát khi chưa lưu
- Dùng `unsavedChangesMixin` (EDIT:1411) nhưng chỉ theo dõi khi là **bản sao chép chưa lưu** (`unsavedSnapshotSource` trả null ở mọi chế độ khác — EDIT:2499-2518). ⇒ **Tạo mới thường và Sửa KHÔNG cảnh báo** khi thoát; chỉ màn Sao chép (chưa bấm Lưu) mới hỏi. Dấu vân tay theo dõi: thông tin chung, dự án, email KH, phương thức GG, làm tròn, vận chuyển, số dòng hàng/dịch vụ/nhóm/khoản GG, tổng sau VAT.
- Sau khi tạo thành công gọi `markFormSaved()` (EDIT:3955). (Nội dung popup cảnh báo do mixin dùng chung quyết định — xem skill unsaved-changes.)

---

## 6. Sao chép báo giá

### 6.1 Nút & điều kiện hiện
- **Màn danh sách**: hành động dòng **"Sao chép báo giá"** (icon copy) — `visible: canCopyQuotation(item)` (pages/assign/quotations/index.vue:1153-1159).
- **Màn chi tiết**: nút **"Sao chép"** (secondary) ở footer, khi đang xử lý hiện **"Đang sao chép..."** (pages/assign/quotations/_id/index.vue:704-713, `canCopy` 1083-1091).
- **Tab Báo giá của dự án** (ProspectiveProjectQuotationsTab.vue) cũng dùng chung mixin.
- **Sao chép được ở MỌI trạng thái báo giá** (index.vue:1083) — gate chỉ theo quyền/vai trò:
  - Báo giá lập từ YCBG: cần quyền **"Xây dựng giá bán theo phòng"** (dự án triển khai theo phòng) hoặc **"Xây dựng giá bán theo công ty"**; BE còn bắt YCBG cùng phòng với user (COPYMX:78-91; BE `ensureBuildPricePermission` SVC:4904-4922).
  - Báo giá tự lập có dự án: chỉ **Sale phụ trách dự án** (BE 403 "Bạn không phải Sale phụ trách dự án này", SVC:292-301).
  - Báo giá không dự án: chỉ **người lập** (BE 403 **"Chỉ người lập báo giá mới được sao chép."**, SVC:288-291).
  - BE còn yêu cầu báo giá nằm trong phạm vi xem của user (4 quyền "Xem … danh sách Báo giá …" hoặc do mình lập) — ngoài phạm vi ⇒ 404 **"Không tìm thấy báo giá."** (CTL:392-401, 444-447, 484-487).
  - FE chỉ xấp xỉ gate (có thể hiện nút thừa rồi BE chặn) — COPYMX:48-77.

### 6.2 Luồng (COPYMX:103-158)
1. Bấm Sao chép ⇒ `GET assign/quotations/{id}/copy-preview` (CTL:438-466 → `getCopyPreview` SVC:1158-1412). Lỗi ⇒ toast message BE hoặc **"Không kiểm tra được thay đổi từ ERP"**.
2. Không có thay đổi ⇒ **mở thẳng** màn Tạo mới đã điền sẵn (không hiện popup).
3. Có thay đổi ⇒ popup `QuotationCopyPreviewModal` (pages/assign/quotations/components/QuotationCopyPreviewModal.vue):
   - Header icon cảnh báo cam, tiêu đề **"Phát hiện thay đổi dữ liệu từ ERP"**, dòng phụ **"Báo giá này kế thừa cấu trúc từ {mã nguồn}. Hệ thống đã tự động cập nhật giá mới nhất và phát hiện các thay đổi sau"**.
   - Bảng cột: **"Loại thay đổi"** (badge: **"Thay đổi giá"** cam / **"Thay đổi VAT"** cam / **"Thay đổi cấu trúc"** xanh / "Thay đổi khác" xám) · **"Mã / Tên vật tư"** (mã đậm + tên; dịch vụ không mã thì hiện tên) · **"Thông tin cũ (V1)"** · **"Thông tin mới (Cập nhật)"** · **"Hành động hệ thống"**. Rỗng: "Không có thay đổi nào."
   - Nội dung dòng do BE dựng (SVC:1268-1340, 1380-1395):
     - Giá: 2 dòng tách "{tên} (Giá vốn)" và "{tên} (Giá bán)", hành động **"Đã cập nhật giá mới"**. Dòng **giá vốn bị ẩn** nếu user không có quyền "Xem giá vốn hàng hoá" (CTL:451-455).
     - VAT (hàng ERP và dịch vụ danh mục): hành động **"Đã cập nhật VAT mới"**.
     - Cấu trúc combo ERP đổi số vật tư con: "{tên} (Vật tư con)", cũ "n vật tư con", mới "m vật tư con (+/−…)", hành động **"(Bỏ qua) — Giữ nguyên cấu trúc V1"**.
   - Không có lựa chọn từng dòng — chỉ nút **"Xác nhận Sao chép báo giá"** (khi chờ: "Đang sao chép...") và **"Hủy bỏ"**.
4. Xác nhận ⇒ mở màn **Tạo mới `?copy_from={id}`**. **Không ghi DB ở bước này** (chốt 2026-08-21).
5. Màn tạo mới gọi `GET {id}/copy-draft` (CTL:478-498 → `buildCopyDraft` SVC:469-561): BE chạy toàn bộ logic sao chép trong giao dịch rồi huỷ, trả dữ liệu điền sẵn. Lỗi ⇒ toast message BE hoặc **"Không tải được dữ liệu sao chép"** và quay về danh sách (EDIT:2488-2493).
6. Form hiện: Mã **"(Chưa tạo)"**, dòng **"Sao chép từ: {mã nguồn} — báo giá mới chỉ được tạo sau khi bấm Lưu"**. User sửa tuỳ ý; **chỉ khi bấm Lưu nháp / Gửi duyệt mới tạo báo giá** (đi `POST assign/quotations` hoặc `create-and-submit` kèm `copied_from_quotation_id`).
7. Có cảnh báo thoát khi chưa lưu (mục 5.5).

### 6.3 Copy gì / không copy gì (SVC:304-460 `copy()`, 469-561 `buildCopyDraft()`, FE `initCopyMode` EDIT:2416-2497)
**Copy nguyên**: dự án, khách hàng + toàn bộ thông tin KH snapshot (mã, tên, MST, địa chỉ, email, người liên hệ, SĐT), giai đoạn dự án, mô tả, deadline, giao hàng (ngày), bảo hành (tháng), **điều khoản báo giá**, **ghi chú nội bộ**, loại tiền tệ, bảng giá, phương thức giảm giá, chế độ làm tròn, chi phí vận chuyển (chi phí, VAT, GG, giá nhập), nhóm hàng (cả nhóm cha-con), thứ tự dòng, cấu trúc cha-con, ẩn/hiện hàng con, mã/tên/model/thương hiệu/xuất xứ/ĐVT/SL/thông số/ghi chú của hàng, dịch vụ & chi phí khác, khoản GG tổng, ghi chú nội bộ hàng ERP.

**Tính lại / thay mới**:
- **Giá hàng ERP** (giá vốn + giá bán) = **giá ERP hiện hành** theo bảng giá + ĐVT của dòng; báo giá ngoại tệ quy đổi theo **tỷ giá hiện hành** (không dùng tỷ giá đóng băng của bản gốc) (SVC:1040-1068, 382-388).
- **VAT hàng ERP** = VAT hiện hành trên ERP; **VAT dịch vụ từ danh mục** = VAT danh mục hiện hành (SVC:672-708).
- **Hàng tạm**: giữ nguyên giá/VAT bản gốc; **giữ nguyên mã hàng tạm** của bản gốc khi lưu (`keepTempProductCodes` SVC:55-56).
- **Cấu trúc combo**: đóng băng theo bản gốc (thay đổi trên ERP chỉ được thông báo).
- **GG mặt hàng**: giữ vế user đã nhập — nhập % thì giữ %, tính lại ₫ theo giá mới; nhập ₫ thì giữ ₫, tính lại % (SVC:1069-1078).
- **GG tổng**: khoản kiểu ₫ giữ nguyên số tiền; khoản kiểu % giữ %, tính lại số tiền theo tổng mới (SVC:752-797); **phân bổ GG tổng tính lại tự động** theo giá mới (Largest Remainder, làm tròn đồng — SVC:799-946).
- Giá nhập dịch vụ có hệ số giá vốn = giá bán × hệ số (`enforceServiceCostsFromRate`).
- Hiệu lực báo giá tính lại.
- Báo giá nguồn lập từ BOM ⇒ bản sao **luôn chuyển thành báo giá TỰ LẬP**, ngắt BOM, bỏ giải pháp/hạng mục (SVC:479-505).

**Không copy / reset**: mã báo giá (cấp mới lúc Lưu), trạng thái (về **Đang tạo**), người tạo (= người đang sao chép), **Yêu cầu xây dựng giá (YCBG) — không kế thừa** (SVC:540-545; FE cố ý không gửi EDIT:3944-3948), mã dòng dịch vụ (cấp mới), thông tin duyệt (người/thời gian duyệt TP, BGĐ, ngày gửi, lý do từ chối, cấp duyệt), đồng bộ ERP (báo giá/hợp đồng chính thức ERP, trạng thái sync, yêu cầu hàng tạm), **Ghi chú kinh doanh**, lịch sử (bản mới có 1 dòng "Tạo" ghi vết nguồn `copied_from`/`copied_from_code` — SVC:446-457), file đính kèm (không có bước copy file nào).

### 6.4 Đổi dự án trên bản sao
- Bản sao (chưa lưu hoặc đã lưu nhưng còn Đang tạo, có `copied_from_quotation_id`) **được chọn dự án khác** (`canChangeProject` EDIT:1637-1643; BE SVC:1828-1890). Dropdown **ẩn các dự án đã có BOM tổng hợp đã duyệt**; giữ dự án gốc thì hợp lệ.
- BE chặn: **"Dự án "{tên}" đã có BOM tổng hợp đã duyệt nên không thể chọn cho báo giá sao chép. Vui lòng chọn dự án khác hoặc tạo báo giá mới từ BOM của dự án đó."** (SVC:72-75, 1855-1857).
- Đổi dự án ⇒ khách hàng nạp lại theo dự án mới (email sửa tay cũ bị ghi đè), cắt YCBG, cắt BOM/giải pháp; tiền tệ/bảng giá: dự án con kế thừa dự án cha, dự án độc lập lấy theo form; tỷ giá tính lại; **GIỮ NGUYÊN** dòng hàng/dịch vụ/nhóm/GG đã copy.

---

## 7. Chỉnh sửa — trạng thái, người sửa, khoá

- **Chỉ sửa được khi trạng thái = "Đang tạo" (status 1) VÀ người đăng nhập là người tạo báo giá** (FE `canEdit` EDIT:1715-1720; BE `ensureEditableByCreator` SVC:4719-4727 cho update, destroy, submit, selfApprove).
- Danh sách: nút **"Sửa / Làm giá"** chỉ hiện với báo giá Đang tạo do mình lập (pages/assign/quotations/index.vue:1137-1146). Màn chi tiết cũng gate `status === 1 && creator` (index.vue:1080-1082).
- Mở URL Sửa khi không đủ điều kiện: **không chuyển hướng**; màn vẫn hiện nhưng có băng vàng **"Báo giá ở trạng thái ({tên trạng thái}) — không cho phép sửa."** (EDIT:7-11), mọi ô khoá, ẩn Lưu nháp/Gửi duyệt, ẩn toolbar GG/Làm tròn, toolbar VAT disable. (Lệch quy ước CLAUDE.md "vào màn Sửa bằng URL thì chuyển về Chi tiết" — chỉ ghi nhận.)
- Trạng thái báo giá (Quotation.php:62-82): Đang tạo (#64748B) · Chờ TP duyệt (#D97706) · Chờ BGĐ duyệt (#D97706) · Đã duyệt (#16A34A) · Đóng (#6B7280) · Dừng (#DC2626) · Trúng thầu (#7C3AED).
- **Bản đã gửi duyệt / đã duyệt KHÔNG sửa được** và **không có cơ chế tự về nháp hay tạo phiên bản khi sửa**. Muốn thay đổi báo giá đã duyệt ⇒ dùng **Sao chép** (tạo báo giá mới Đang tạo, ghi vết nguồn). Báo giá bị **Từ chối** (TP hoặc BGĐ, khi đang Chờ TP/Chờ BGĐ duyệt) ⇒ **quay về "Đang tạo"**, lưu lý do từ chối (`reject()` SVC:4069-4105, dòng 4090) ⇒ người tạo sửa lại rồi gửi duyệt lại được (lý do cũ bị xoá khi gửi lại — SVC:3911).
- Sau khi Đã duyệt chỉ còn sửa được **Ghi chú Kinh doanh** (mục 4.2). Chốt (Trúng thầu)/Huỷ chốt là thao tác riêng (finalize/unfinalize) — ngoài phạm vi.
- Các trường **khoá theo nghiệp vụ** khi đang sửa: Loại tiền tệ + Bảng giá chỉ đổi được ở màn Tạo mới (hoặc khi bản sao vừa đổi dự án), khoá ở màn Sửa và khi kế thừa dự án cha (EDIT:194-226); phương thức GG khoá khi dự án con; VAT hàng ERP, giá hàng ERP khoá; VAT vận chuyển khoá 8%.
- Đổi loại tiền tệ (khi được phép) có hàng đã nhập giá ⇒ popup **"Xác nhận đổi loại tiền tệ"**: *"Các giá trị tiền tệ đã nhập sẽ không thay đổi khi bạn đổi loại tiền tệ ! Bạn có chắc chắc muốn đổi?"* (EDIT:3630-3661) — nguyên văn có lỗi chính tả "chắc chắc".
- Đổi bảng giá khi có hàng ERP ⇒ popup **"Xác nhận đổi bảng giá"**: *"Đổi bảng giá sẽ cập nhật lại đơn giá bán của các hàng hoá ERP theo bảng giá mới. Chiết khấu và hàng tạm giữ nguyên. Bạn có chắc muốn đổi?"* (EDIT:3610-3629).
- Xoá báo giá: chỉ Đang tạo + người tạo (SVC:1783-1802); nếu YCBG không còn báo giá nào ⇒ YCBG về "Chờ xây dựng giá".

---

## 8. Danh sách thông báo nguyên văn (tổng hợp)

**Toast thành công**: "Đã tạo báo giá" · "Đã lưu báo giá" · "Đã gửi duyệt báo giá" · "Đã tự duyệt báo giá" · "Đã làm tròn đơn giá" · "Đã áp {x}% cho {n} dòng" · "Đã cập nhật cột Phân bổ GG theo phân bổ tự động" · "Đã xóa toàn bộ dữ liệu giảm giá" · "Đã xóa toàn bộ phân bổ giảm giá" · "Đã lưu ghi chú" (màn chi tiết).

**Toast lỗi/cảnh báo**: "Vui lòng chọn dự án hoặc khách hàng trước khi tạo báo giá" · "Lỗi lưu" · "Không thể gửi duyệt" · "Không tính được cấp duyệt" · "Không tính được cấp duyệt. Vui lòng kiểm tra giá sản phẩm." · "Giá bán đã thay đổi, vui lòng phân bổ lại giảm giá" · "Lưu ý: {lỗi} Hệ thống vẫn lưu nháp, nhưng cần đồng bộ trước khi Trình duyệt." · "Không tải được báo giá" · "Không tải được dữ liệu sao chép" · "Không kiểm tra được thay đổi từ ERP".

**Lỗi inline FE**: "VAT phải trong 0–100%" · "GG (%) phải trong 0–100%" · "GG không được lớn hơn đơn giá bán" · "GG vận chuyển không được lớn hơn chi phí" · "Giá nhập không hợp lệ" · "Chi phí vận chuyển không hợp lệ" · "Giá nhập phải > 0" · "Giá vốn cha phải ≥ tổng giá vốn con" · "Giá / thành tiền bán phải > 0" · "Giá bán hàng cha phải ≥ tổng giá bán hàng con" · "Vui lòng chọn loại GG" · "Giá trị phải > 0" · "Giá trị tối đa 100%" · "Vui lòng nhập thời gian giao hàng" · "Vui lòng chọn loại tiền tệ" · "Vui lòng chọn bảng giá" · "Vui lòng nhập điều khoản thanh toán" · "Vui lòng chọn giai đoạn dự án" · "Bắt buộc phải nhập" (khách hàng).

**Popup xác nhận** (tiêu đề / nội dung / nút): xem 1.6 (làm tròn), 3.1 (đổi phương thức GG), 3.3 (phân bổ tự động), 3.4 (xóa GG/xóa phân bổ), 4.1 (mẫu điều khoản), 5.3 (đơn giá đã thay đổi), 7 (đổi tiền tệ, đổi bảng giá).

**Popup thông tin**: "Áp dụng VAT đồng loạt?" (2.3) · "Cảnh báo: Tồn tại mặt hàng có đơn giá <= 1.000 vnđ" (5.4) · "Gửi duyệt báo giá" (5.4) · "Không thể gửi duyệt báo giá" (5.4) · "Không thể trình duyệt — vi phạm quy tắc đồng bộ" (5.4) · "Phát hiện thay đổi dữ liệu từ ERP" (6.2).

**Lỗi BE**: liệt kê ở 5.2 (Request + quyền tạo + sửa + gửi duyệt), 3.5 (quyền GG), 6.1/6.4 (sao chép), 4.2 (ghi chú KD), 2.2 (apply-vat-bulk – không dùng).

---

## 9. Điểm lệch / rủi ro cần lưu ý khi viết SRS (code là chuẩn, ghi chú để QA biết)
1. Endpoint `apply-vat-bulk` và `allocate-discount` tồn tại ở BE nhưng màn KHÔNG gọi; VAT hàng loạt và phân bổ GG đều tính ở FE, chỉ ghi DB khi Lưu.
2. GG tổng: "Giảm giá" thực tế = tổng ô Phân bổ GG, không phải Tổng GG khai báo; không chặn lưu/gửi khi chưa phân bổ hoặc phân bổ lệch.
3. BE `ensureAllPricesPositive` không kiểm hàng hoá của báo giá tự lập (join BOM) — giá bán ≤ 0 của hàng tự lập chỉ bị FE chặn.
4. Cấp duyệt ở footer (FE) chỉ xét 2 tiêu chí; BE xét 3 tiêu chí + luật tự động duyệt ⇒ có thể khác cấp ở popup.
5. Tổng giá nhập cha-có-con: FE theo giá cha, BE (popup/cấp duyệt) theo Σ con ⇒ có thể lệch với cha ERP combo.
6. Màn Sửa bấm Gửi duyệt ⇒ dữ liệu đã được lưu trước khi popup hiện (Huỷ popup không hoàn tác).
7. Cảnh báo thoát chưa lưu chỉ áp cho bản sao chép.
8. Màn Sửa mở bằng URL khi không đủ quyền không chuyển hướng (chỉ khoá + băng vàng).
9. Màu TSLN trong popup Gửi duyệt dùng ngưỡng cứng 20%/10%, khác ngưỡng cấu hình trên màn.
10. Footer nút tự dựng, không dùng V2Footer; thông báo "Cảnh báo: … <= 1.000 vnđ" dùng dấu chấm ngăn nghìn (lệch chuẩn số quốc tế).
