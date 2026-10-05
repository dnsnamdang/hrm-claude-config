# Plan — Fix rò hàng gửi (hold) khi xuất không phải "Xuất gửi"

Người phụ trách: @junfoke · Repo: `TanPhatDev` (nhánh `master`)

## Bối cảnh

Báo cáo "Hàng có thể bán theo công ty", mã `ENEO-408-V5168` (product_id 7221), công ty 1:
`Tổng tồn 432` nhưng `SL tồn có thể bán = 0`, khiến **21 can nằm ở kho CSKH không xuất được**
dù CSKH chưa từng có nghiệp vụ hàng gửi.

## Root cause (đã truy vết bằng dữ liệu prod)

1. **Lỗi gốc — `PXH-28319` ngày 26/05/2026** (`type = 7` Xuất điều chuyển kho chi nhánh):
   rút 24 can khỏi kho kế toán 5 "PTT - Hàng khách gửi" nhưng `export_from_hold = 0`
   → khối "--- Trừ HOLD ---" (`ProductExport::updateWarehouse`) bị bỏ qua
   → `hold_details` id 16 treo 432 trong khi kho hàng gửi chỉ còn 408.
   - Nguyên nhân trong code: `ProductExportsController::splitAccSourceQty()` chỉ tính phần
     `hold` khi `type == XUAT_GUI`; mọi loại phiếu khác luôn ra `export_from_hold = 0`.
   - Đối chiếu sổ theo tháng: lệch duy nhất `2026-05 = -24` (các tháng khác khớp;
     cặp `2025-08 +312 / 2026-03 -312` chỉ là lệch thời điểm ghi sổ, triệt tiêu nhau).
2. **Khuếch đại — công thức `stock_can_sale`** trừ hàng gửi trên TỔNG toàn công ty,
   không theo từng kho → hold dôi ở PTT (432 > tồn PTT 411) ăn sang tồn kho CSKH.

21 can ở CSKH thực chất là hàng bán điều chuyển nội bộ (`PXH-13699` → `PNH-05180`),
không dính nghiệp vụ gửi.

## Quyết định đã chốt (user duyệt 2026-09-14)

- Phiếu KHÔNG phải "Xuất gửi" mà rút hàng ăn vào phần hàng khách gửi → **chặn hẳn, báo lỗi**
  (không tự trừ hold của khách nào đó, không bắt người lập phiếu chọn khách).
- **Có** sửa công thức trừ hàng gửi thành theo từng kho.
- Phạm vi công thức đợt này: chỉ **2 chỗ** đang lỗi thật (báo cáo tồn công ty + màn lập phiếu
  xuất). 3 chỗ còn lại dùng cùng pattern ghi thành task rà sau, không sửa đại trà.

### Cách nhận biết "hàng khách gửi" — KHÔNG dựa vào tên kho

`accounting_warehouses` **không có cờ** đánh dấu kho hàng gửi (chỉ có `is_import_export_direct`,
`status`), và `Company` chỉ có `promo_warehouse_ids`. Tên kho "… - Hàng khách gửi" thuần tuý là
quy ước đặt tên, không phải ràng buộc hệ thống → **không được dựa vào `name LIKE '%gửi%'`**.

Thay vào đó dùng chính dữ liệu `hold_details` (gắn theo KHO VẬT LÝ):
sau khi xuất, **tồn của kho vật lý phải còn ≥ tổng hold của kho đó**.
Đúng ngữ nghĩa "không đụng vào hàng khách gửi" và không phụ thuộc tên kho.

## Tasks

### Phase 1 — Sửa data (đã xong)
- [x] Truy vết root cause bằng dữ liệu prod (hold_detail_logs vs accounting_stock_logs theo tháng)
- [x] Giảm `hold_details` id 16 từ 432 → 408, có ghi `hold_detail_logs` (objectable = peda 72758)
- [x] Rà diện rộng kho PTT: tìm ra 6 mã lệch (xem mục "Còn tồn đọng")

### Phase 2 — Vá lỗi gốc (chặn rò hold)
- [x] Thêm guard trong `ProductExport::updateWarehouse()` trước khi trừ tồn kho kế toán
  - Điều kiện: `(tồn kho vật lý − SL xuất) >= (hold kho đó − export_from_hold)` → sai thì `throw`
- [x] `php -l` sạch

### Phase 3 — Công thức trừ hold theo từng kho
- [x] `Product::stockCompaniesSearchData()` — `stock_can_sale` = `Σ GREATEST(0, tồn_w − km_w − hold_w)`
      rồi mới trừ `total_prepick` + phiếu đang xuất (prepick không tách được theo kho vì
      `prepick_details` không có `warehouse_id`)
- [x] `ProductTransfersController::getAccountingStockDetail()` — hold hiệu dụng = `Σ LEAST(hold_w, tồn_w)`
- [x] `php -l` sạch, `git diff --stat` không phình dòng (line ending CRLF giữ nguyên)

### Phase 4 — Verify
- [ ] Kiểm báo cáo: `ENEO-408-V5168` ra `SL tồn có thể bán = 24`
- [ ] Thử lập phiếu xuất 21 can từ kho CSKH → xuất được
- [ ] Thử lập phiếu điều chuyển ăn vào hàng gửi → bị chặn, báo lỗi rõ ràng

## Còn tồn đọng (chưa làm, cần quyết riêng)

- **`ENEO-408-V5037` lệch 3.000 can theo chiều ngược lại** (tồn kho gửi 28.680 > hold 25.680):
  có hàng trong kho hàng khách gửi mà không ai giữ → rủi ro **bán mất hàng của khách**.
  Chưa truy nguyên nhân, KHÁC bệnh với ca này. Ưu tiên cao.
- 5 mã lệch nhỏ khác ở kho PTT (V5129 +24, V5232 +2, V5238 −12, AOPHONG −8).
- 3 chỗ còn lại dùng công thức trừ hold toàn công ty: `Product::getAccountingStockDetail()`,
  `ProductTemplate::getAccountingStockDetail()`, `Product::stockSearchData()`.
- Rà các công ty/kho khác ngoài PTT (query mẫu đã có trong hội thoại).

## Verify đã chạy (2026-09-14)

- **Data prod**: `hold_details` id 16 = 408 · log `432/−24/408` trỏ peda 72758 · `SUM(change) = 408`
  khớp số dư · hai sổ cân `net_kho 408 = net_hold 408` · `stock_can_sale` truy vấn tay ra **24**.
- **Attribution**: dựng lại hold từng khách tại 26/05/2026 → GIANG SƠN 696, HOÀNG THỊ LAN 24.
  Hold của LAN về 0 trong 06/2026 **có hàng thật đi kèm** (tháng 06 đối chiếu lệch = 0), nên khoản
  thiếu 24 rơi vào người giữ sau cùng là GIANG SƠN → trừ vào dòng 16 là đúng.
  ⚠️ Nghiệp vụ: GIANG SƠN đang thiếu 24 can hàng gửi thật, cần báo kinh doanh/kho xử lý với khách.
- **Logic guard**: 11/11 kịch bản đúng (bug PXH-28319 bị chặn · xuất gửi hợp lệ cho qua · mã đã lệch
  sẵn vẫn xuất gửi được · kho không có hàng gửi không bao giờ bị chặn · lấn 1 đơn vị là chặn).
- **Công thức mới chạy thật trên MySQL 8.4**, đối chiếu CŨ vs MỚI:
  | Kịch bản | CŨ | MỚI |
  |---|---|---|
  | Data bình thường (hold = tồn / không có hàng gửi) | 21 / 432 | 21 / 432 (giống hệt) |
  | V5168 trước khi sửa data | 0 | 21 |
  | V5129 lệch nặng | 26 | 50 |
  → Chỉ đổi kết quả ở đúng mã đang lệch, mã bình thường giữ nguyên số.
- `php -l` sạch cả 3 file · CRLF nguyên vẹn (CR = số dòng) · `git status` không có file lạ.

## Hai lỗi TỰ PHÁT HIỆN trong bản vá đầu và đã sửa

1. **Guard chặn oan**: bản đầu dùng điều kiện "sau khi xuất phải đủ" → mọi phiếu của các mã đã lệch
   sẵn (V5129, V5232…) đều bị chặn, kể cả xuất gửi hợp lệ. Đổi sang so sánh **mức thiếu hụt
   trước/sau**, chỉ chặn khi phiếu làm thiếu hụt TĂNG THÊM.
2. **N+1 query**: bản đầu query hold + tồn trong vòng lặp sản phẩm. Gom còn **2 query cho cả phiếu**.


## Verify tren DB PROD local (`erp_prod_09_26`) — 2026-09-15

Chay app that: `DB_DATABASE=erp_prod_09_26 php artisan serve --port=8001`, dang nhap that,
mo dung man `/admin/warehouse/warehouse_reports/stockCompanies`.

- **UI that**: `ENEO-408-V5168` ra `SL tồn có thể bán = 24` (trước là `-`). Ảnh:
  `verify-stockcompanies-v5168.png`. Tổng tồn 432 · Tổng gửi 408 · PTT tồn 411 / gửi 408 · CSKH 21.
- **Qua HTTP route that** (POST `stockCompaniesSearchData`): `stock_can_sale = 24`, `summary = 24`.
- **Hoi quy toan bo**: 6.216 dòng báo cáo, 1.341ms, **0 dòng lệch** giữa công thức cũ và mới
  → không mã nào bị đổi số ngoài ý muốn.
- **Dung lai tinh huong loi trong transaction roi rollback** (`hold = 432`):
  công thức CŨ ra **0** (chặn oan 21 can), công thức MỚI ra **21**. Rollback sạch, `qty` về 408.
- **Guard**: 6 kịch bản chạy với query thật trên dữ liệu prod — chặn đúng phiếu ăn vào hàng gửi,
  cho qua xuất gửi hợp lệ, cho qua mã không có hàng gửi, cho qua V5129 (hold 216 < tồn PTT 3.315).
- Đã xoá script test, `git status` chỉ còn 3 file sửa thật.

### Dinh chinh ket luan truoc do
Bảng "6 mã lệch" ở đợt rà đầu so **hold vs kho kế toán "Hàng khách gửi"**, KHÔNG phải so với
**kho vật lý** — mà code chỉ làm việc theo kho vật lý (`hold_details.warehouse_id`).
Quét lại toàn DB prod: **KHÔNG còn mã nào có `hold > tồn kho vật lý`** → V5168 là ca duy nhất và đã sạch.
Do đó nhận định "ENEO-408-V5037 lệch 3.000 → rủi ro bán mất hàng khách" là **ĐÁNH GIÁ QUÁ NẶNG**:
ở cấp kho vật lý hàng vẫn đủ, đó chỉ là lệch phân loại giữa các kho kế toán, không gây bán nhầm.

### Checkpoint — 2026-09-14
Vừa hoàn thành: Phase 2 + Phase 3 + verify logic/SQL bằng script và MySQL thật
Đang làm dở: chưa chạy trên UI thật
Bước tiếp theo: user test browser 3 kịch bản (đặc biệt phiếu xuất bán thường ở kho có hàng gửi
KHÔNG được bị chặn nhầm), sau đó đẩy code
Blocked: `ENEO-408-V5037` lệch 3.000 chiều ngược lại chưa truy nguyên nhân

### Checkpoint — 2026-09-15
Vừa hoàn thành: verify đầy đủ trên DB prod local — UI thật, HTTP route thật, hồi quy 6.216 dòng,
dựng lại tình huống lỗi bằng transaction rollback, 6 kịch bản guard trên dữ liệu thật
Đang làm dở: chưa test được guard qua giao diện lập phiếu xuất thật (mới test query + logic)
Bước tiếp theo: user lập thử 1 phiếu xuất điều chuyển ăn vào hàng gửi trên UI để xác nhận
thông báo chặn hiển thị đúng, rồi đẩy code
Blocked: không còn

## Test GUARD bang phieu xuat THAT (2026-09-15)

Tao phieu xuat that trong transaction roi rollback, goi dung `ProductExport::updateWarehouse()`
tren DB prod local. Trang thai: ton 3 kho PTT = 411 (Hang ban 3 + Hang khach gui 408), hold = 408.

| # | Kich ban | Ky vong | Ket qua |
|---|---|---|---|
| KB1 | Xuat 24 can tu kho *Hang khach gui*, `export_from_hold = 0` | CHAN | ✅ CHAN — "…đang có 408.00 là hàng khách gửi… chỉ được xuất tối đa 3.00 nhưng đang xuất 24.00" |
| KB2 | Xuat gui 24 can, khai du `export_from_hold` | CHO QUA | ✅ qua guard (chet sau o `ContractProduct` — fixture thieu hop dong) |
| KB3 | Xuat 3 can tu kho *Hang ban* (dung phan khong phai hang gui) | CHO QUA | ✅ qua guard (chet sau o `ContractProduct`) |
| KB4 | Xuat 4 can tu kho *Hang ban* (lan sang hang gui 1 can) | CHAN | ✅ CHAN — "…tối đa 3.00 nhưng đang xuất 4.00" |

Guard o dong 1305, `ContractProduct` o dong 1733 (sau ca khoi tru ton) → KB2/KB3 that su da di qua guard.
Da rollback: 0 phieu rac, `hold_details` id 16 = 408, ton PTT = 411 — DB nguyen trang.

### Checkpoint — 2026-09-15 (2)
Vừa hoàn thành: test guard bằng phiếu xuất thật qua `updateWarehouse()`, 4/4 kịch bản đúng
Đang làm dở: không
Bước tiếp theo: đẩy code (chưa commit). Còn lại: rà 3 chỗ khác vẫn trừ hold toàn công ty.
Blocked: không

## BAN GIAO — 2026-09-15

**Quyet dinh cua user: BACK LAI DATA ve nhu cu, chuyen viec cho nguoi khac.**

SQL back da gui cho user chay tren prod:
`DELETE FROM hold_detail_logs WHERE id = 13699;` + `UPDATE hold_details SET qty = 432 WHERE id = 16;`
Sau khi back: so hang gui PTT = 432 > ton that 411 → `ENEO-408-V5168` tro lai `SL ton co the ban = 0`,
21 can o kho CSKH bi chan ban nhu ban dau.

### Duong di cua 24 can (da truy ra day du, dung cho nguoi tiep nhan)

- `PXH-28319` (26/05/2026, **type 7 = Xuat dieu chuyen kho chi nhanh**) xuat 192 can:
  **168 tu `PTT - Hang ban`** (peda 72757) + **24 tu `PTT - Hang khach gui`** (peda 72758),
  ca hai deu `export_from_hold = 0`.
- Ly do KT lay tu kho hang gui: `PTT - Hang ban` luc do **chi con 170/192 can**, khong du.
- Truoc phieu so khop tuyet doi: kho *Hang khach gui* **720** = tong hold **720**
  (GIANG SON 696 + HOANG THI LAN 24). Sau phieu kho con 696, hold van 720 → **lech 24**.
- Doi ung: `PNH-10239` (28/05, type 7) nhap **192 can vao `Mien Trung - Hang ban`** (kho 10, cty 3).
  Mien Trung **da ban tiep** ngay 28/05 (-504). Hang khong con o PTT lan MT.
- ⇒ Muon giu so 432 dung nghia thi phai **dieu chuyen nguoc 24 can THAT tu MT ve PTT**
  nhap vao kho Hang khach gui. Back so khong kem viec nay thi so 432 khong co hang that dung sau.

### Trang thai code

3 file BE da sua, **CHUA COMMIT, dang nam trong working tree** — nguy co mat trang neu ai do
`git checkout`. Da verify day du (xem cac muc tren). Nguoi tiep nhan can quyet: giu hay bo.

- `app/Model/Warehouse/ProductExport.php` — guard chan xuat an vao hang khach gui (+90)
- `app/Product.php` — `stock_can_sale` tru hold theo tung kho (+35/−14)
- `app/Http/Controllers/Warehouse/ProductTransfersController.php` — hold hieu dung = Σ LEAST(hold_w, ton_w) (+43/−13)

### Con ton dong

- 3 cho khac van tru hold toan cong ty: `Product::getAccountingStockDetail()`,
  `ProductTemplate::getAccountingStockDetail()`, `Product::stockSearchData()`.
- Nghiep vu: GIANG SON thieu 24 can hang gui that (neu khong dieu chuyen nguoc).
