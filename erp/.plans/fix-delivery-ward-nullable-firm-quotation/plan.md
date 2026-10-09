# Fix: Copy báo giá HĐ hãng lỗi delivery_ward cannot be null

## Bug
Copy firm_quotation (create?copy=48209) → INSERT fail: `SQLSTATE[23000] Column 'delivery_ward' cannot be null`.

## Root cause
- Địa chỉ giao mới (sau sáp nhập 2025, vd "Hạnh Thông") không map bảng `wards` cũ → `delivery_place.ward_id = null`.
- FE `FirmQuotation.chooseDeliveryPlace` set `delivery_ward = delivery_place.ward_id` (null).
- Cột `firm_quotations.delivery_ward` NOT NULL (migration 2022, bị sót) — trong khi `project_quotations` đã nullable từ 2021.
- (service_quotations cũng NOT NULL → dính lỗi tương tự khi copy.)

## Fix (Phương án A)
Migration set `firm_quotations.delivery_ward` + `service_quotations.delivery_ward` **nullable** (đồng bộ project_quotations). Địa chỉ text vẫn ở `delivery_place`.

## Tasks
- [x] Migration nullable cho firm_quotations + service_quotations
- [x] Commit + push master (f89663da28)
- [ ] Deploy chạy migrate trên prod

### Checkpoint — 2026-07-15
Migration `2026_07_15_100000_set_nullable_delivery_ward_firm_service_quotations.php` (raw ALTER, giữ FK service_quotations). Đã push origin/master. **Chờ: deploy chạy `php artisan migrate` trên prod.**
