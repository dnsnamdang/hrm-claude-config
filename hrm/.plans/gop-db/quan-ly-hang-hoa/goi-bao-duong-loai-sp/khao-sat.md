# N100 — Gói bảo dưỡng: `service_has_products.group_id` → Loại SP (khảo sát 15/10/2026, chỉ đọc)

User chốt 14/10: thay nhóm hàng cũ bằng id Loại SP; 15/10: làm code trước, mapping nạp sau (lệnh đọc CSV, có dry-run).

## Dữ liệu (hrm_erp_giacty)
- `service_has_products(id, service_id, group_id, product_id, timestamps)` — cả 3 id NOT NULL + FK (`groups`/`products`/`services`), không unique (service_id, product_id).
- 4.896 dòng · 210 gói · 1.940 hàng · 129 nhóm. Mỗi dòng = 1 HÀNG cụ thể + nhóm của nó (không phải "nhóm áp vào gói").
- 16 dòng nhóm bảng nối ≠ `products.group_id` (hàng 13526 gói 77/78/121; 14563, 15199 gói 104/105/106/122/126; 4088 gói 21; 16398 gói 63; 17016 gói 66).
- 123 gói đã dùng ở báo giá — chứng từ chỉ lưu `service_id` ⇒ số liệu chứng từ không đổi.
- `product_types` 0 dòng, `products.product_type_id` NULL cả 45.890 hàng (B6) ⇒ chưa thử chuyển dữ liệu thật được.

## Không luồng nào LỌC theo group_id
Báo giá bảo dưỡng, lọc thiết bị có gói, chặn xoá hàng đều theo `product_id`. group_id chỉ để gom hiển thị, lịch sử, validate, import Excel; ERP form có nút "chọn theo Nhóm hàng".

## Chỗ đọc/ghi
- hrm-api: `CustomerCare/Http/Requests/Service/ServiceRequest.php` :39-73 fillProductGroupIds, :139-140 rule `required|exists:groups,id` (nguồn 422) · `ServiceService.php` :366-370 log "Nhóm hàng", :697-726 dataForEdit, :937 xoá, :1467-1472 syncProducts · `Entities/Service/Service.php:92-93` withPivot · `ServiceImportService.php` :103, :497-510, :678-688 · test `ServiceAppliedProductTypeTest.php`.
- hrm-client: `pages/customer-care/services/components/ServiceFormComponent.vue` :568-573 (đã gom theo Loại SP), :1204-1208, :1461-1480, :1601-1606 · `ServiceImportModal.vue:312`.
- ERP: màn `admin/services` CÒN CHẠY (`routes/web.php:3658-3675`, menu `topmenubar.blade.php:63`) · `ServiceStoreRequest.php:34`, `ServiceUpdateRequest.php:34` · `Sale/ServiceController.php:156-159, 209-212` · `Model/Sale/Service.php:56-70` (`$product->group->id` ⇒ lỗi non-object khi hàng HRM không nhóm), :253-283 · `views/sale/services/{create,edit,formJs}.blade.php`.

## Phương án đề xuất (A)
Thêm cột `product_type_id` nullable + index; `group_id` → nullable (giữ FK, giữ nghĩa cũ). Sửa ~6 file hrm-api + 1 command + 1 migration, 2 file client, ERP 5-6 file hoặc chặn màn `admin/services` bằng `productMovedToHrm`.
Lệnh: `customer-care:backfill-service-product-types {csv} --dry-run` (khuôn `MasterData/Console/BackfillCompanyPricesCommand.php`), chỉ đụng dòng product_type_id NULL, báo nhóm thiếu mapping.

## Rủi ro / câu cần chốt
1. Nguồn Loại SP: CSV theo nhóm hay `products.product_type_id` của hàng (sau quy đổi B6)? Nhóm cũ tách nhiều Loại SP thì mapping theo nhóm sai.
2. 16 dòng lệch nhóm.
3. ERP màn Gói bảo dưỡng: sửa cho chạy hay chặn chuyển sang HRM.
4. Lịch sử cũ ghi "Nhóm hàng" — đổi khoá log sinh dòng "sửa" giả lần lưu đầu.
5. Import Excel: cột "Nhóm hàng" → "Loại sản phẩm" hay bỏ.
