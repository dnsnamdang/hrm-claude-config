# Bước 4.5 (ERP) — popup chọn hàng còn lại + gỡ code cũ — khảo sát 14/10/2026 (chỉ đọc)

> ERP `wt-erp-2d1` @ `4a0b8a60e3` (nhánh chung `feat/2d1-erp-khong-loi`, đã có popup mới `productPicker` từ 4.4). Chưa đụng source.

## 1. Popup còn lại
| Popup | Màn còn sống | Hành vi | Popup mới làm được? |
|---|---|---|---|
| `searchProductEquivalent` (Hàng công ty tương đương) | CSKH Chi tiết KH (`customermanager/show_`), Báo giá DV CSKH (tạo/sửa) — hiện khi tick "Hàng công ty không bán" | danh sách Đang KD, bảng giá 1, chọn 1 | **Được ngay** (`priceTypeId:1`, `multiple:false`) — callback đổi sang đóng `#searchProduct` |
| `searchServiceProduct` (Thiết bị TP / thiết bị KH) | Báo giá DV CSKH (2 nút trong popup thiết bị) | như trên | **Được ngay** — mở chồng lên popup thiết bị (modal lồng) |
| `searchProductPromotions` (hàng KM của HĐ) | PL HĐ mua TN v2 — **tạo** (màn **sửa** đang hỏng sẵn: không include partial) | chỉ hàng KM của HĐ gốc còn SL > 0 | **Được ngay** — `LegacyPickerScope` đã có nhánh `inland_buy_contract_promotion_id`; màn sửa tự chạy luôn |
| `searchProduct2` | YC đặt hàng gốc (`orders/root_order_requests`) | khoá thương hiệu (+ hãng SX theo dòng đầu); ô "Xem tồn" theo **kho / nhóm kho** hiện cột tồn chi tiết; lọc Còn tồn / **Hết tồn**; bấm dòng thêm, popup không đóng | **Một phần** — thiếu cột tồn theo kho KHÔNG giới hạn danh sách, thiếu lọc "Hết tồn"; trang có modal `#searchProduct` riêng trùng id |
| `searchProductForUpdate` | 0 (2 màn đã chuyển HRM / không có route) | — | **Gỡ** |

## 2. Picker tự viết khác (không thuộc 2 partial, cùng endpoint cũ)
6 màn đặt hàng (`order_requests`, `order_request2`, `inland_order_request2`, `inland_order_request_new`, `inland_order_requests`, `delivery_cost_asking_requests`) · Cảnh báo kho (`warehouse_warnings`) · Lỗi thiết bị (`device_errors` ×2 + `CreateDeviceErrorModal` ×2). Đều tự dựng modal `#searchProduct*` + bộ lọc phân loại CŨ. Spec §8 không liệt kê; plan 4.5 chưa tính.

Dữ liệu giacty (14/10): YC đặt hàng gốc 7.500 phiếu (4.453 từ 2026, mới nhất 15/09) · YC đặt hàng NK 2: 3.793 (1.940) · YC đặt hàng TN mới: 4.990 (3.334) ·
YC đặt hàng TN: 899 (442) · Lỗi thiết bị: 2.886 (455) · YC hỏi chi phí VC: 1 (05/2026) · YC đặt hàng NK / TN 2 / Cảnh báo kho: **0**.

## 3. Code chết (N94)
- 19 view báo cáo include `js/searchProductQuotationJs` không modal, không gọi (mỗi trang ~10 truy vấn `@json` thừa) + `products_approve/list` (đã chuyển HRM).
- File 0 include: `js/searchProductRepairJs`, `js/searchProductWarrtyJs`, `searchProductPromotion.blade.php` (số ít).
- `js/searchProductPromotionJs` — 5 include (HĐ bán, đơn bán, HĐ thanh lý) nhưng không trang nào có modal / gọi ⇒ chết.
- `searchProductWarranty.blade.php` (Phiếu CSKH) — markup chết, không gì mở.
- `customermanager/show.blade.php` — bản sao không render.
- Sau khi chuyển §1: catalog `@json` + `$scope.search` + `availableGroup` + nhánh KM trong `searchProductJs`/`searchProductQuotationJs` hết người dùng (trừ `manufactures`, `cates` mà popup tạo barcode/model đọc — giữ hoặc chuyển).
- GIỮ: `searchProductWarrantyNew` (sống, chọn theo HĐ/serial), 4 method SearchController (`PriceSnapshotCommand` + API HRM gọi).

## 4. Chốt của user 14/10
| # | Câu | Chốt |
|---|---|---|
| Q1 | YC đặt hàng gốc: Xem tồn theo kho / nhóm kho + Hết tồn | **Giữ** — popup mới thêm ô chọn kho / nhóm kho (chỉ chế độ đặt hàng), cột tồn = tồn tại kho đã chọn do ERP tính, KHÔNG giới hạn danh sách; lọc tồn 3 trạng thái (Tất cả / Còn tồn / Hết tồn) |
| Q2 | 10 picker tự viết | **Đưa 5 màn còn dùng vào 4.5**: YC đặt hàng NK 2, YC đặt hàng TN mới, YC đặt hàng TN, Lỗi thiết bị (4 chỗ: `device_errors` ×2 + `CreateDeviceErrorModal` ×2), YC hỏi chi phí VC. 3 màn 0 phiếu (YC đặt hàng NK, TN 2, Cảnh báo kho) để nguyên |

## 5. Tự chốt
- Lọc Còn tồn / Hết tồn tính theo **tồn bán được công ty** (HRM, đã đối chiếu ERP lệch 0) — cột "Tồn tại kho" chỉ để XEM. Popup cũ lọc theo tồn kế toán kho của công ty; lệch nhỏ ở hàng đang giữ/YC xuất. Cost: hàng có tồn kế toán nhưng đã giữ hết ⇒ nay vào "Hết tồn".
- YC đặt hàng TN có ô lọc **Nhà cung cấp** (`supplier` ⇒ `ProductSupplier`) — giữ: ERP tính tập id theo NCC (nhánh mới `LegacyPickerScope`), popup hiện ô NCC ở chế độ này.
- 4 popup đặt hàng: bấm dòng thêm 1, popup không đóng (như cũ); khoá thương hiệu (`form.brand_id`) / hãng SX (dòng đầu hoặc `form.manufacture_id`).
- Lỗi thiết bị "Thiết bị" (`for_update_list_products`, có ô tick) ⇒ `multiple:true`; "Vật tư thay thế" (`is_service_quotation`) ⇒ `serviceQuotationOnly`.
