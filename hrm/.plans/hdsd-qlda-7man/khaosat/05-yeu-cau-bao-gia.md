# Khảo sát — YÊU CẦU BÁO GIÁ

## 0. Bản đồ màn hình
| Màn | URL | Menu | File |
|---|---|---|---|
| Yêu cầu xây dựng giá (YCBG) | `/assign/pricing-requests` | Giao việc > **Yêu cầu báo giá** | `pages/assign/pricing-requests/index.vue` |
| Chi tiết / Sửa YCBG | `/assign/pricing-requests/{id}` · `/{id}/edit` | – | `_id/index.vue`, `_id/edit.vue` |
| Danh sách báo giá | `/assign/quotations` | **Quản lý báo giá** | `quotations/index.vue` |
| Tạo báo giá | `/assign/quotations/create` | (nút "Tạo báo giá") | `create.vue` (13 dòng, `extends` edit.vue) |
| Sửa / Làm giá | `/assign/quotations/{id}/edit` | – | `_id/edit.vue` (4986 dòng) |
| Chi tiết báo giá | `/assign/quotations/{id}` | – | `_id/index.vue` |
| Báo giá chờ duyệt | `/assign/quotations/pending-approval` | Phê duyệt > **Báo giá chờ duyệt** | `pending-approval/index.vue` |
| Cấu hình duyệt giá | `/assign/settings/price-approval` | **Cấu hình duyệt giá** | `settings/price-approval/index.vue` |
| Loại giảm giá | `/assign/discount-types` | Danh mục > **Loại giảm giá** | `discount-types/index.vue` |
| Tab Báo giá trong dự án TKT | `/assign/prospective-projects/{id}` | – | `ProspectiveProjectQuotationsTab.vue` |

> ⚠️ Lệch nhãn: menu ghi **"Yêu cầu báo giá"** nhưng tiêu đề màn là **"Yêu cầu xây dựng giá"**.

**2 luồng vào báo giá:**
1. **Từ YCBG** (dự án triển khai chéo phòng / theo phòng): Sale lập *Yêu cầu xây dựng giá* → người có quyền xây dựng giá bấm **Tạo báo giá** từ YCBG.
2. **Sale tự lập** (dự án Tự triển khai): Sale bấm **Tạo báo giá** ở tab Báo giá của dự án, hoặc nút **Tạo báo giá** ở màn danh sách.

## A. TẠO MỚI BÁO GIÁ
Màn Tạo và Sửa **dùng chung 1 file**, phân biệt bằng `isCreateMode` và `isDirectQuotation`.

### A1. "Thông tin chung" — từng trường
| Nhãn | Control | Bắt buộc / message | Mặc định – điền sẵn | Ẩn/hiện – readonly | Options |
|---|---|---|---|---|---|
| `Mã báo giá` | text | – | Tạo: **`(Chưa tạo)`**; Sửa: `BG-YYYY-NNNNN` | readonly | – |
| `YCBG` | link mở popup | – | mã YCBG, rỗng → `—` | chỉ khi báo giá từ YCBG | `PricingRequestDetailModal` |
| `Dự án` * | V2BaseSelect | Toast **"Vui lòng chọn dự án trước khi tạo báo giá"** | trống; có `?project_id=` thì tự chọn | Select khi Tạo hoặc báo giá sao chép đang tạo; còn lại readonly | `GET assign/prospective-projects/getAll?per_page=50&main_sale_mine=1` |
| `BOM tổng hợp` | V2BaseSelect | – | Dự án có **đúng 1** BOM đã duyệt → tự chọn + tự nạp hàng | **chỉ ở màn Tạo**; chưa chọn dự án → **"Chọn dự án trước"**; không có BOM → **"Không có BOM tổng hợp đã duyệt"** | `GET assign/bom-lists/getAll?...&bom_list_type=2&status=4&only_aggregate_solution_level=1` |
| `Giải pháp` / `Hạng mục` / `BOM` | link | – | từ dữ liệu | chỉ màn Sửa | – |
| `Khách hàng` | text | – | **snapshot từ dự án TKT** | readonly | – |
| `MST` | text | – | snapshot dự án | readonly | – |
| `Email khách hàng` | V2BaseInput email | không | kế thừa dự án, **sửa tay được** | `disabled` khi không được sửa | – |
| `Địa chỉ`, `SĐT liên hệ`, `Người liên hệ` | text | – | snapshot dự án | readonly | – |
| `Giao hàng (ngày)` * | number | **"Vui lòng nhập thời gian giao hàng"** | null | disabled khi không sửa được | – |
| `Hiệu lực báo giá` | text tính | – | = hôm nay + `configs.quotation_valid_days` của ERP (mặc định **30 ngày**), **rút ngắn** nếu hàng ERP sắp đổi giá | readonly; khác bản đã lưu → hiện `(đã lưu: dd/mm/yyyy)` | `POST assign/quotations/erp-price-change-dates` |
| `Loại tiền tệ` * | V2BaseSelect | **"Vui lòng chọn loại tiền tệ"** | theo `currency_id` của dự án | **khoá hoàn toàn ở màn Sửa** | `GET assign/bom-lists/currencies` |
| `Bảo hành (tháng)` | number | không | null | disabled khi không sửa | – |
| `Bảng giá` * | V2BaseSelect | "Vui lòng chọn bảng giá" | **`price_type_id = 1`** (Bán lẻ) | khoá ở màn Sửa | `GET assign/quotations/price-types` (ERP price_types 1–6) |
| `Điều khoản báo giá` * | CompactReviewEditor + select **`Mẫu điều khoản báo giá`** | **"Vui lòng nhập điều khoản thanh toán"** (strip HTML trước khi kiểm) | rỗng | disabled khi không sửa | `GET assign/quotations/term-templates` |
| `Ghi chú nội bộ (chỉ nội bộ)` | rich text | không | rỗng | – | – |

**Không tồn tại trên form:** `Ngày báo giá`, `Người lập`, `Tỷ giá`, `VAT mặc định`.
- **Tỷ giá** chỉ hiển thị readonly ở toolbar: `Tỷ giá: 1 {mã} = {số} VND (dd/mm/yyyy) - Bảng giá bán lẻ`, **chỉ khi không phải VNĐ**. Tỷ giá **đóng băng** lúc tạo báo giá.
- **VAT mặc định**: hàng ERP lấy VAT từ danh mục ERP (khoá); hàng tạm mặc định **0**. VAT chi phí vận chuyển **cố định 8%, khoá cứng**.
- Cảnh báo khi không được sửa: **"Báo giá ở trạng thái (…) — không cho phép sửa."** Điều kiện sửa (`canEdit`): status = 1 **và** người đăng nhập = người tạo.

### A2. Bảng hàng hoá / dịch vụ
**Thêm dòng** (chỉ báo giá tự lập mới thêm/xoá được hàng):
| Nút | Vị trí | Điều kiện | Mở gì |
|---|---|---|---|
| `Thêm nhóm` / `Thêm nhóm con` | header phần A / trong nhóm | báo giá tự lập + sửa được | modal `Thêm nhóm sản phẩm` (trường `Tên nhóm *`) |
| `Thêm mới` | header phần A / trong từng nhóm | như trên | **`QuotationProductSearchModal.vue`** tab `Hàng hoá` |
| `Thêm con` | dưới tên hàng cha | hàng **không phải ERP** | cùng modal, gán cha |
| `Nhân bản` | dưới tên hàng | hàng tạm, không có con | nhân bản dòng (dùng chung mã) |
| `Thêm mới` (phần B) | header phần B | sửa được | cùng modal, tab `Dịch vụ & Chi phí` |

Mọi nút chặn trước bằng: **"Vui lòng chọn loại tiền tệ trước khi thêm sản phẩm."** / `… thêm dịch vụ.` / `… thêm.`

**Cột bảng (đúng thứ tự):**
| # | Cột | Nhập tay? | Công thức |
|---|---|---|---|
| 1 | `Thao tác` | – | kéo thả + xoá (chỉ báo giá tự lập) |
| 2 | `STT` | tự | cha `1`, con `1.1` |
| 3 | `Mã` | tự | icon cảnh báo **"Giá bán thay đổi ngày dd/mm/yyyy"** |
| 4 | `Tên hàng` | tự | badge `DV` nếu là dịch vụ |
| 5-9 | `Model`, `Thương hiệu`, `Xuất xứ`, `Thông số kỹ thuật`, `Ghi chú` | chỉ `Ghi chú` nhập tay | toggle bằng nút `Hiện/Ẩn cột chi tiết` |
| 10 | `SL` | nhập tay (báo giá tự lập) | con recipe: `SL = SL đơn vị × SL cha` |
| 11 | `ĐVT` | select (hàng ERP) | đổi ĐVT ⇒ **đổi cả giá**: `quoted = retail/rate`, `estimated = cost/rate` |
| 12 | `Giá nhập ({tiền})` | nhập tay với hàng tạm; **khoá** với hàng ERP và cha-có-con | cha tạm roll-up = `Σ(giá vốn con × SL con)/SL cha` |
| 13 | `Thành tiền nhập` | tự | `giá nhập × SL` |
| 14 | `Giá bán ({tiền})` | nhập tay; **khoá** hàng ERP | – |
| 15-17 | `GG(%)`, `GG(₫)`, `Đơn giá sau GG` | 15-16 nhập tay, 2 chiều | `GG₫ = giá bán × %/100`; `Đơn giá sau GG = giá bán − GG₫` |
| 18 | `GG phân bổ tự động` (tooltip *"Tham khảo — tự tính theo tỷ lệ giá trị"*) | tự | Largest Remainder theo tỷ trọng doanh thu |
| 19 | `Phân bổ GG` (+ dòng `Còn: …`) | **nhập tay** | disabled khi tổng GG ≤ 0 |
| 20 | `Thành tiền bán` | tự | GG mặt hàng: `giá×SL − GG₫×SL`; GG tổng: `giá×SL − phân bổ`; không GG: `giá×SL` |
| 21 | `Tỷ suất LN` | tự | `(bán − nhập)/nhập × 100`, màu theo ngưỡng `Tỷ suất lợi nhuận mức sàn` |
| 22 | `VAT(%)` (tooltip *"VAT chỉ áp dụng trên dòng CHA hoặc SP độc lập. SP con được cộng gộp vào CHA."*) | nhập tay; khoá hàng ERP | – |
| 23 | `Tiền VAT` | tự | `Thành tiền bán × VAT/100` |
| 24 | `Thành tiền sau VAT` | tự | `Thành tiền bán + Tiền VAT` |

Hàng **con** chỉ điền tới `Thành tiền nhập`, các cột bán/VAT để `—`.
Cột **giá vốn ẩn theo quyền `Xem giá vốn hàng hoá`**: không có quyền → Giá nhập / Thành tiền nhập / Tỷ suất LN của hàng ERP hiện `—`; hàng tạm tự tạo vẫn nhập được.

**Dòng Dịch vụ / Chi phí** khác hàng hoá: SL cố định 1, không ĐVT, không cây cha-con, **không áp VAT hàng loạt**; giá vốn tự tính `= giá bán × rate_value_capital%`; phân loại vào nhóm **II Dịch vụ** hoặc **III Chi phí** theo `revenue_calculation`.

### A3. Khối tổng
Bảng **"Tổng hợp giá trị báo giá"**: `STT | Nhóm chi phí | Thành tiền nhập | Thành tiền trước VAT | Giảm giá | Thành tiền sau GG (trước VAT) | Thuế VAT | Thành tiền sau VAT`; 5 dòng: `I Hàng hoá`, `II Dịch vụ`, `III Chi phí`, `IV Chi phí vận chuyển` (4 ô nhập tay: giá nhập VC, thành tiền, GG %↔₫, VAT khoá 8%), `V Tổng giá trị báo giá`.

Công thức BE (`QuotationService::computeTotals`):
```
total_sale                = Σ(giá bán×SL hàng cha) + Σ(giá bán×SL dịch vụ) + shipping_cost
total_discount            = Σ CK dòng + CK vận chuyển
total_sale_after_discount = total_sale − total_discount
total_vat                 = Σ (thành tiền sau CK × VAT%)      ← VAT tính TRÊN GIÁ SAU CK
total_after_vat           = total_sale_after_discount + total_vat
profit_margin %           = (total_sale_after_discount − total_import)/total_import × 100
total_sale_vnd            = total_sale_after_discount × exchange_rate
```

Toolbar phụ: `VAT: [ô] Tất cả / VAT=0` (áp VAT hàng loạt, bỏ qua hàng ERP), `GG:` (Không GG / GG mặt hàng / GG tổng), `Làm tròn` (Mặc định 2 số lẻ / -3 / -2 / -1 / 0 / 1 / 2 + nút `Áp dụng`; VNĐ khoá về Số nguyên).

**Chiết khấu tổng (GG tổng)** — khối `Giảm giá tổng đơn hàng`: bảng `# | Loại GG | Kiểu | Giá trị %/₫ | Thành tiền GG`, nút `Thêm khoản GG`, `Phân bổ tự động` / `Phân bổ lại`. Base tính % = **tổng trước VAT gồm cả chi phí vận chuyển**. Confirm phân bổ: *"Thao tác này sẽ ghi đè toàn bộ giá trị cột "Phân bổ GG" bằng giá trị phân bổ tự động (theo tỷ lệ giá trị). Bạn có chắc chắn?"*

## B. LẤY DỮ LIỆU TỪ BOM SANG BÁO GIÁ
**Không có nút riêng.** Chỉ có **select `BOM tổng hợp`, CHỈ ở màn Tạo**.
1. Chọn **Dự án** → nạp danh sách BOM: chỉ **BOM tổng hợp (`bom_list_type=2`) trạng thái Đã duyệt (`status=4`), cấp giải pháp**.
2. Phân nhánh:
   - **1 BOM duyệt** → tự chọn + **tự nạp hàng ngay** (chưa chọn tiền tệ thì báo *"Dự án này có BOM. Vui lòng chọn loại tiền tệ trước để tính tỷ giá quy đổi khi tải sản phẩm từ BOM."*)
   - **>1 BOM** → tự chọn trong select
   - **0 BOM** → báo giá tự lập (`type = 2`)
3. Chọn/đổi BOM khi đã có hàng → confirm **"Việc chọn lại BOM sẽ xoá toàn bộ thông tin hàng hoá/dịch vụ trên báo giá!"** (title `Xác nhận thay đổi BOM`, `Đồng ý`/`Huỷ`).

**GHI ĐÈ TOÀN BỘ — không merge**: `products = []`, `directGroups = []`, `serviceItems = []` rồi nạp lại.

**Map dữ liệu:**
| BOM | → Báo giá |
|---|---|
| nhóm BOM | nhóm báo giá (giữ cây cha-con) |
| `erp_product_id, code, name, model/brand/origin, unit, qty_needed, product_attributes` | copy nguyên; `product_attributes → Thông số kỹ thuật` |
| giá ERP `cost_price` | `Giá nhập` = `round(cost/tỷ giá, 2)` |
| giá ERP `retail_price` theo Bảng giá | `Giá bán` = `round(retail/tỷ giá, 2)` |
| VAT ERP | `VAT(%)` |
| hàng tạm (không có `erp_product_id`) | giá nhập = giá bán = **0** |
| Dịch vụ & Chi phí BOM | copy tên + VAT, **giá nhập = giá bán = 0** → phải nhập lại |

**Sau khi lấy về sửa được gì**: báo giá kế thừa BOM bị **khoá cấu trúc** — mất cột `Thao tác`, mất nút `Thêm nhóm`/`Thêm mới`/`Thêm con`/`Nhân bản`/`Sửa`. **Chỉ sửa được: Giá nhập, Giá bán, VAT, Ghi chú, Chiết khấu, Chi phí vận chuyển, và thêm/xoá dòng Dịch vụ.**

**Lưu**: nút `Lưu nháp` (footer) → `POST assign/quotations` (toast `Đã tạo báo giá`) hoặc `PUT assign/quotations/{id}` (toast `Đã lưu báo giá`), rồi về danh sách.

Luồng BE riêng `POST assign/quotations/create-from-bom` (nút `Tạo báo giá` ở tab **Hồ sơ trình duyệt** của dự án) — chỉ **dự án Tự triển khai**, BOM phải **Tổng hợp** + **Đã duyệt**. Lỗi: *"Chỉ tạo báo giá từ BOM tổng hợp."*, *"BOM phải ở trạng thái Đã duyệt."*, *"Chỉ dự án Tự triển khai mới được tạo báo giá trực tiếp."*

## C. GỬI DUYỆT GIÁ
**Không có "phiếu yêu cầu duyệt" riêng** — dùng nút **`Gửi duyệt`** ở footer màn Sửa báo giá.
- **Điều kiện**: status = 1 Đang tạo + là người tạo.
- Bấm `Gửi duyệt` → **lưu ngầm với validate đầy đủ** (điều khoản báo giá, giao hàng, tiền tệ, giá bán > 0, giá nhập hàng tạm > 0, thành tiền > 0, giá bán cha ≥ tổng con, giá vốn cha ≥ tổng con) — lỗi **inline** tại ô, tự cuộn tới ô lỗi đầu → mở **modal `Gửi duyệt báo giá`**.

**Modal `Gửi duyệt báo giá`** gọi `POST /calculate-level`, hiển thị: `Tổng giá nhập` (chỉ khi có quyền xem giá vốn) · `Tổng giá bán` · `Tổng giảm giá` · `Tổng bán sau GG` · `Tỷ suất LN` · **`Cấp duyệt dự kiến: Cấp N`**:
| Cấp | Thông điệp | Nút | Hành động |
|---|---|---|---|
| 1 | **"Theo quy chế, bạn có thể tự duyệt báo giá này."** | `Xác nhận duyệt` | `submit` + `self-approve` → **Đã duyệt**; toast `Đã tự duyệt báo giá` |
| 2 | **"Theo quy chế, báo giá cần gửi tới Trưởng phòng duyệt."** | `Xác nhận gửi` | `submit` → **Chờ TP duyệt**; toast `Đã gửi duyệt báo giá` |
| 3 | **"Theo quy chế, báo giá cần gửi qua 2 cấp duyệt:"** + sơ đồ `1 Trưởng phòng duyệt & chuyển BGĐ → 2 Ban giám đốc duyệt` | `Xác nhận gửi` | `submit` → **Chờ TP duyệt** |

### Quy tắc tính CẤP DUYỆT
```
V = Tổng bán sau CK × tỷ giá        (quy về VNĐ, trước thuế)
M = (Tổng bán sau CK − Tổng giá vốn) / Tổng giá vốn × 100   (%)
Cấp = MAX( cấp theo V , cấp theo M )       ← lấy cấp CAO HƠN
Không khớp cấu hình nào → mặc định Cấp 3
```
Tổng giá vốn = Σ giá nhập hàng hoá (cha có con lấy tổng con) + Σ giá nhập dịch vụ + giá nhập vận chuyển.

Cấu hình tại **`Cấu hình duyệt giá`** (`/assign/settings/price-approval`), 3 khối: `Tỷ suất lợi nhuận mức sàn`, `Theo giá trị đơn hàng (VNĐ) trước thuế`, `Theo tỷ suất lợi nhuận (%)`, cột `Cấp duyệt | Từ | Đến | Người duyệt | Mô tả` + `Lịch sử thay đổi`. Nhãn người duyệt: `Người làm giá (tự duyệt)` / `Trưởng phòng` / `Ban giám đốc`.

Seed mặc định:
| Tiêu chí | Cấp 1 | Cấp 2 | Cấp 3 |
|---|---|---|---|
| Giá trị đơn hàng (VNĐ) | 0 – 1 tỷ | 1 tỷ – 20 tỷ | > 20 tỷ |
| Tỷ suất lợi nhuận (%) | ≥ 20% | 10% – 20% | < 10% |

Màn Sửa báo giá hiển thị **cấp duyệt dự kiến real-time** ở footer: badge `C1 — Tự duyệt` / `C2 — TP` / `C3 — TP & BGĐ` (chỉ khi có quyền xem giá vốn).

### Duyệt / Từ chối
Người duyệt vào **`Báo giá chờ duyệt`** → cột `Mã BG • BOM` → icon mắt tooltip **`Xem và duyệt`** → màn chi tiết báo giá. **Không duyệt được từ danh sách.**
| Nút (footer chi tiết) | Điều kiện | Xác nhận | Kết quả |
|---|---|---|---|
| `Duyệt` (cấp 2) hoặc **`Duyệt & chuyển BGĐ`** (cấp 3) | quyền `Trưởng phòng duyệt giá Bom giải pháp` + status=2 + **quản lý phòng ban của báo giá** | title `Xác nhận duyệt`, msg **"Duyệt báo giá?"** / **"Duyệt & chuyển BGĐ?"**, nút `Duyệt`/`Huỷ` | cấp 2 → **Đã duyệt**; cấp 3 → **Chờ BGĐ duyệt**. Toast `Đã duyệt báo giá` |
| `BGĐ duyệt` | quyền `Ban giám đốc duyệt giá Bom giải pháp` + status=3 + **cùng công ty** | msg **"BGĐ duyệt báo giá?"** | → **Đã duyệt**. Toast `BGĐ đã duyệt báo giá` |
| `Từ chối` | (TP & status 2) hoặc (BGĐ & status 3) | modal **`Từ chối báo giá`**, **`Lý do từ chối`** (bắt buộc, textarea, `Nhập lý do từ chối...`), lỗi **"Vui lòng nhập lý do từ chối"**, nút `Xác nhận từ chối`/`Huỷ` | → **Đang tạo**, xoá `submitted_at`, `tp_approved_*`, `approved_*`, `price_approval_level`; lưu lý do. Chi tiết BG hiện alert đỏ `Đã bị từ chối: {lý do}` |

**Thông báo:**
| Sự kiện | Người nhận | Nội dung |
|---|---|---|
| Gửi duyệt (cấp 2/3) | tất cả người có quyền `Trưởng phòng duyệt giá Bom giải pháp` | `{Tên} gửi duyệt báo giá (cấp TP / cấp TP + BGĐ) {Mã BG}` → link `/assign/quotations/pending-approval` |
| TP duyệt & chuyển BGĐ | người có quyền `Ban giám đốc duyệt giá Bom giải pháp` | `{Tên} TP đã duyệt & chuyển BGĐ {Mã BG}` |
| Duyệt xong | **người lập báo giá + NV KD phụ trách dự án + tất cả người có quyền TP duyệt giá** | `{Tên} đã duyệt báo giá {Mã BG}` |
| Từ chối | **người lập báo giá** + TP đã duyệt | `{Tên} từ chối báo giá {Mã}. Lý do: {reason}` |

Duyệt xong cascade: dự án TKT → `Thương thảo giá`, giải pháp → `Đã duyệt giá`, YCBG → `Đã có báo giá`.

## D. TRẠNG THÁI BÁO GIÁ
| Mã | Nhãn | Màu | Khi nào |
|---|---|---|---|
| 1 | **Đang tạo** | #9E9E9E | **mặc định khi tạo mới** (mọi đường); cũng là trạng thái sau khi bị từ chối |
| 2 | **Chờ TP duyệt** | #673AB7 | sau `Gửi duyệt` cấp 2 hoặc 3 |
| 3 | **Chờ BGĐ duyệt** | #E91E63 | cấp 3, sau khi TP bấm `Duyệt & chuyển BGĐ` |
| 4 | **Đã duyệt** | #009688 | tự duyệt / TP duyệt / BGĐ duyệt; hoặc sau `Hủy chốt` |
| 5 | **Đóng** | #6B7280 | **cascade tự động** khi dự án TKT bị đóng |
| 6 | **Dừng** | #EF4444 | **cascade tự động** khi có yêu cầu điều chỉnh giải pháp (không mở lại được) |
| 7 | **Trúng thầu** | #D4AF37 | Sale bấm `Chốt báo giá (Trúng thầu)` |

**"Trúng thầu" đặt ở đâu**: **tab Báo giá trong màn chi tiết Dự án tiền khả thi** (không có ở màn chi tiết báo giá).
- Nút **`Chốt báo giá (Trúng thầu)`** — hiện khi: status=4 **và** người dùng là **Sale phụ trách dự án** **và** dự án chưa có BG trúng thầu.
- Modal `Xác nhận chốt báo giá`, message **"Chốt báo giá {code} thành Trúng thầu? Mỗi dự án chỉ có 1 báo giá trúng thầu."**, nút `Chốt`/`Huỷ`. Lỗi BE: *"Dự án đã có báo giá trúng thầu, vui lòng hủy chốt trước."*
- Nút **`Hủy chốt`** (status=7 + Sale phụ trách): text `Hủy chốt báo giá {code} — báo giá sẽ quay lại trạng thái "Đã duyệt".`, **`Lý do hủy chốt`** bắt buộc (**"Vui lòng nhập lý do hủy chốt."**), nút `Xác nhận hủy chốt`.

**Trúng thầu mở ra gì:**
1. **Đồng bộ hàng tạm sang ERP** — banner ở tab Báo giá, nút `Gửi duyệt hàng tạm` / `Cập nhật kết quả duyệt` (chỉ Sale phụ trách).
2. **Lập hợp đồng ERP** — banner `Lập hợp đồng ERP` khi đủ điều kiện (xem tài liệu 04, mục D).

## E. CÁC THAO TÁC KHÁC
| Thao tác | Nút / vị trí | Điều kiện | Kết quả |
|---|---|---|---|
| **Sao chép báo giá** | icon `ri-file-copy-line` ở danh sách, nút `Sao chép` ở chi tiết, và tab Báo giá của dự án | **mọi trạng thái**; BG từ YCBG → theo quyền xây dựng giá; BG tự lập → Sale phụ trách | `copy-preview`: không thay đổi → copy thẳng; có → modal **`Phát hiện thay đổi dữ liệu từ ERP`** (bảng `Loại thay đổi \| Mã / Tên vật tư \| Thông tin cũ (V1) \| Thông tin mới (Cập nhật) \| Hành động hệ thống`, badge `Thay đổi giá` / `Thay đổi VAT` / `Thay đổi cấu trúc`, nút `Xác nhận Sao chép báo giá` / `Hủy bỏ`). Tạo bản mới **Đang tạo**, mã mới, **lấy lại giá + VAT ERP hiện hành + tỷ giá hiện tại**, reset vết duyệt và liên kết ERP, chuyển sang màn Sửa bản mới. Toast `Đã sao chép sang báo giá {mã}` |
| **Tạo phiên bản mới** | – | – | Không có chức năng riêng; **Sao chép chính là cách tạo phiên bản mới** (lưu `copied_from_quotation_id`). Bản sao **được phép đổi Dự án** khi còn Đang tạo — confirm `Đổi dự án và lưu`, lưu ngay, thay snapshot khách hàng, tính lại hiệu lực, **ngắt liên kết BOM** |
| **In báo giá** | icon `ri-printer-line` (danh sách), nút `In` (chi tiết) | luôn | Modal **`Cấu hình in báo giá`**: checkbox `Hiện hàng hoá cấp con`, `Chọn tất cả`, danh sách cột (`STT, Tên hàng hoá, Mã hàng hoá, Model, Thương hiệu, Xuất xứ, Đơn vị tính, Thông số kỹ thuật, Ghi chú, Số lượng, Đơn giá bán, Thành tiền bán, [GG (%), GG (₫), Đơn giá sau GG] hoặc [GG phân bổ], VAT (%), Tiền VAT, Thành tiền sau VAT, Hình ảnh, Thời gian bảo hành`; mặc định tích hết trừ `Mã hàng hoá`); lỗi `Vui lòng chọn ít nhất 1 cột để in`; nút `Xem trước` |
| **Xuất Excel** | nút `Xuất Excel` (footer chi tiết + header bảng màn Sửa) | luôn / `!isCreateMode` | Tải `{Mã BG}_{dd-mm-yyyy}.xlsx`; bộ cột đổi theo Loại GG (22 cột Không GG / 25 cột GG mặt hàng / 24 cột GG tổng). Lỗi → **"Không xuất được file Excel. Vui lòng thử lại."** |
| **Import Excel** | nút `Import Excel` (header bảng, màn Sửa) | sửa được + báo giá đã lưu (chưa lưu → **"Vui lòng lưu báo giá trước khi import."**) | Modal **`Import báo giá từ Excel`**: `Chọn file Excel`, `Tải file mẫu`, `Load lên bảng`, `Validate`, `Chỉ dòng lỗi`, footer `Import` / `Làm mới` / `Đóng`. Bấm Import → popup **`Chọn phương thức import`**: **`Import từng phần`** hoặc **`Thay thế hoàn toàn`** (chỉ báo giá tự lập; *"Thao tác không thể hoàn tác"*). BG kế thừa BOM: *"Báo giá kế thừa BOM có cấu trúc cố định — chỉ hỗ trợ cập nhật từng phần."* Lỗi → popup 3 cột `Dòng Excel \| Tên cột sai \| Mô tả chi tiết` + `Sao chép lỗi` / `Tải File lỗi`. Import chỉ đổ lưới, **phải bấm Lưu mới ghi DB** |
| **Gửi khách hàng** | – | – | **KHÔNG có chức năng gửi email/gửi khách.** Chỉ In / Xuất Excel để gửi thủ công |
| **Ghi chú Kinh doanh** | ô ở chi tiết BG + nút `Sửa ghi chú kinh doanh` ở tab Báo giá của dự án | status=4 **và** là Sale phụ trách | textarea + nút `Lưu ghi chú` → toast `Đã lưu ghi chú` |
| **Lịch sử** | nút `Lịch sử` (chi tiết), icon `ri-history-line` (danh sách) | luôn | Modal **`Lịch sử báo giá`** — timeline: Tạo báo giá / Lưu nháp / Gửi duyệt / Tự duyệt / TP duyệt / TP duyệt & chuyển BGĐ / BGĐ duyệt / Từ chối / Cập nhật ghi chú KD / Áp dụng VAT đồng loạt / Import giá / Đóng theo dự án / Cập nhật giảm giá / Chốt báo giá / Hủy chốt |
| **Xoá** | icon thùng rác, nút `Xoá` (chi tiết) | status=1 **và** là người tạo | Confirm `Xác nhận xoá`, **"Bạn có chắc muốn xoá báo giá '{code}'?"** → toast `Đã xoá báo giá` |
| **Cấu hình cột hiển thị** | icon `ri-layout-column-line` | luôn | Modal tuỳ biến cột |
| Đồng bộ báo giá sang ERP (`retrySync`) | – | – | **Đang TẮT** — luôn trả lỗi *"Tính năng đồng bộ báo giá đang tạm tắt."* |

## F. PHÂN QUYỀN
| id | Tên quyền | Dùng ở đâu |
|---|---|---|
| 1080 | **`Xây dựng giá bán theo công ty`** | Tạo BG từ YCBG của dự án triển khai chéo phòng; sao chép BG; hiện menu `Yêu cầu báo giá` |
| 1091 | **`Xây dựng giá bán theo phòng`** | Như trên, cho dự án triển khai theo phòng; **kèm điều kiện YCBG phải cùng phòng ban** |
| 1081 | **`Trưởng phòng duyệt giá Bom giải pháp`** | Duyệt cấp 2/3, Từ chối, màn `Báo giá chờ duyệt`; **kèm điều kiện quản lý phòng ban của báo giá** |
| 1082 | **`Ban giám đốc duyệt giá Bom giải pháp`** | Duyệt cấp 3 bước 2, Từ chối; **kèm điều kiện cùng công ty** |
| 1083 | **`Xem tất cả danh sách Báo giá`** | Phạm vi xem danh sách |
| 1084–1086 | **`Xem danh sách Báo giá theo công ty / phòng ban / bộ phận`** | nt |
| 1092 | **`Xem giá vốn hàng hoá`** | Ẩn/hiện Giá nhập, Thành tiền nhập, Tỷ suất LN, cấp duyệt dự kiến |
| 1090 | **`Quản lý danh mục loại giảm giá`** | Màn `/assign/discount-types` |

**Route gắn `checkPermission`:**
| Route | Middleware |
|---|---|
| `GET /assign/quotations/pending-approval` | `checkPermission:Trưởng phòng duyệt giá Bom giải pháp\|Ban giám đốc duyệt giá Bom giải pháp` |
| `POST /assign/quotations/{id}/tp-approve` | `checkPermission:Trưởng phòng duyệt giá Bom giải pháp` |
| `POST /assign/quotations/{id}/bgd-approve` | `checkPermission:Ban giám đốc duyệt giá Bom giải pháp` |
| `POST /assign/quotations/{id}/reject` | `checkPermission:Trưởng phòng...\|Ban giám đốc...` |

Các route còn lại (`store`, `update`, `destroy`, `submit`, `self-approve`, `finalize`, `unfinalize`, `copy`, `import/export`, `allocate-discount`, `apply-vat-bulk`, `service-items`, `create-from-bom`, toàn bộ route `pricing-requests`) **không gắn middleware** — gate nằm trong Controller/Service.

**Gate theo VAI TRÒ DỮ LIỆU (không phải permission):**
| Điều kiện | Cho phép |
|---|---|
| `project.main_sale_employee_id == người đăng nhập` (**Sale phụ trách dự án**) | Tạo YCBG; Tạo báo giá tự lập; **Chốt / Hủy chốt (Trúng thầu)**; sửa Ghi chú kinh doanh; gửi duyệt hàng tạm ERP |
| `creator_id == người đăng nhập` **và** status=1 | Sửa / Làm giá, Xoá, Gửi duyệt, Import, áp VAT hàng loạt |
| TP: quản lý `department_id` của báo giá | Duyệt cấp 2/3 |
| BGĐ: cùng `company_id` với báo giá | Duyệt cấp 3 bước 2 |

**Phân quyền theo cấp:**
- **Báo giá**: `checkPermissionListWithColumn(..., 'created_by')` (list, chi tiết → ngoài scope trả **404**, copy-preview/copy/export).
- **Báo giá chờ duyệt** — logic riêng: TP thấy `status=2` ∩ `department_id ∈ employee_manage_departments`; BGĐ thấy `status=3` ∩ `company_id` = công ty mình; có cả 2 → union; không quyền nào → `whereRaw('1=0')`.
- **Yêu cầu XD giá**: có "theo phòng" → YCBG `department_id` = phòng mình ∩ dự án `implementation_type=2`; có "theo công ty" → YCBG của dự án `implementation_type ∈ {1,3,null}`; **không có quyền nào → chỉ thấy YCBG `created_by = mình`**.
