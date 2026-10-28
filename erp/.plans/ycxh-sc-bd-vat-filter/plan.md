# YCXH loại sc-bd (type 17) — lọc hàng theo Nhóm VAT

## Bối cảnh
Màn YCXH (`product_export_requests/create`), loại xuất **sc-bd (type 17 = sửa chữa-bảo dưỡng-bảo trì)**:
hiện chọn hợp đồng xong đổ **toàn bộ** hàng → 1 phiếu gom nhiều nhóm VAT khác nhau.

**Yêu cầu:** cho chọn **Nhóm VAT**, chỉ xuất hàng cùng 1 VAT trên 1 phiếu.
Luồng: chọn hợp đồng → **chưa hiện hàng** → chọn nhóm VAT → hàng tự hiện theo VAT đã chọn.

**Chốt với user:**
- Chỉ áp cho **type 17**. Type 16 (bảo hành) giữ nguyên (hàng bảo hành không có `vat_percent`).
- Phiếu cũ (đã gom nhiều VAT) **để nguyên**, chỉ cần xem chi tiết/sửa vẫn chạy — `edit.blade.php` nạp hàng từ `@json($data)` của phiếu, không gọi lại HĐ nên không ảnh hưởng.
- Lọc ở **FE (client-side)**, **không sửa BE** — `getDataRepairMaintain()` (`WrServiceContract.php:2975`) đã trả sẵn `vat_percent` từng dòng.

## Tham chiếu khuôn có sẵn
- Dropdown "Nhóm VAT" của firm: `form.blade.php:129-143`
- Nhánh JS type 16/17 hiện tại: `create.blade.php:201-216`

## Tasks
- [x] T1. `form.blade.php`: thêm dropdown "Nhóm VAT" gate `ng-if="form.type == 17 && form.parent.code && !form.id"`, bind `form.wr_vat_percent`, options `form.parent.vat_percent_options`, `ng-change="selectWrVatPercent()"`
- [x] T2. `create.blade.php` `getParentInfo()`: tách nhánh type 17 khỏi 16 — type 17 gom `vat_percent_options`, giữ full list ở `form.wr_products_all`, để `form.products = []`
- [x] T3. `create.blade.php`: thêm `selectWrVatPercent()` lọc `wr_products_all` theo VAT → gán `form.products` + `updateStock(form)`
- [x] T4. Verify Playwright (HĐ test 6633, 15 dòng, VAT 8+10): chọn HĐ → bảng trống; VAT 10 → 1 dòng; VAT 8 → 14 dòng; về rỗng → 0 dòng. Chi tiết phiếu cũ (show 35660) hàng vẫn đủ, không lòi dropdown. Console chỉ 404 ảnh, không lỗi JS.
- [x] T5. Commit + push **develop_02** (a549fd1491) để test, rồi cherry-pick + push sang **gop_db** (a22f4a140c). Đang ở nhánh gop_db.

### Quyết định đã chốt
- Gate dropdown thêm `&& !form.id` để màn Sửa/xem phiếu cũ không lòi dropdown VAT trống.
- Options VAT bind `form.parent.vat_percent_options` (không phải `wr_service_contract`) vì `form.parent` luôn là HĐ hiện tại sau khi load (cả luồng URL lẫn chọn qua modal).
- Lọc client-side, không sửa BE.

### Checkpoint — 2026-10-28
Vừa hoàn thành: T1-T4 (code + verify browser trên erp_hrm_check).
Đang làm dở: không.
Bước tiếp theo: chờ user duyệt để commit (hiện CHƯA commit).
Blocked: không.
