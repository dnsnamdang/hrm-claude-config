# Fix: Màn Chuyến xe khác (ERP) lỗi khi load danh sách — chủ xe không còn trong `customers`

@junfoke · Repo `TanPhatDev` nhánh `gop_db` · ngày 31/10/2026

## Bug
Vào màn Chuyến xe khác trên dev-erp báo lỗi, bảng không load. `OtherDeliveryTripController::searchData`
(dòng ~147-153) gọi thẳng `$object->vehicle_owner->fullname` cho xe thuê ngoài; model `Supplier` chỉ lấy
`is_supplier = 1`, không thấy chủ xe → null → lỗi cả bảng.

## Root cause dữ liệu (DB local `gop_db`)
- 198/198 chuyến xe thuê ngoài trỏ tới chủ xe không có trong `customers` (vd id 14059, 7040).
- `customers` chỉ còn id ≥ 14849 (12.675 dòng) trong khi `erp_dev_24_09` ~38 nghìn → dữ liệu KH/NCC cũ mất hoặc đổi id khi gộp DB.
- Cùng lỗi: 116 `vehicles.owner` + 2.390 `delivery_trips` trỏ chủ xe không tồn tại.

## Ngày 31/10/2026 (@junfoke)
- [x] 31/10/2026 — Xử lý lỗi màn Chuyến xe khác ERP không load: dùng `optional(...)` cho `employee_create`, `vehicle`, `vehicle_company`, `vehicle_owner` (`1f2007a111` gop_db → `develop_02` `6d7bd77c87`). Dòng thiếu chủ xe để trống ô "Nhà cung cấp".
- [ ] Chờ user xác nhận việc gộp DB có cố ý bỏ KH/NCC id < 14849 không — nếu không thì phải bổ sung / ánh xạ lại `vehicle_owner_id`, `vehicles.owner`.
