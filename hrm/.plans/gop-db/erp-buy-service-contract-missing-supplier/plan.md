# Fix: Danh sách Hợp đồng mua dịch vụ (ERP) nổ khi NCC không tồn tại — @khoipv

Màn: `dev-erp.dnsmedia.vn/admin/orders/buy-service-contract?type=all`
Lỗi: `DataTables warning ... No query results for model [App\Model\Sale\Supplier] 37961`
Nguyên nhân: `BuyServiceContractController@searchData` dùng `Supplier::findOrFail($object->supplier_id)` → 1 hợp đồng trỏ NCC không còn trong `customers` làm sập cả danh sách.

## Tasks
- [x] BE (repo erp): `findOrFail` → `find`, không thấy NCC thì hiện `supplier_name` lưu trên hợp đồng
- [ ] Dữ liệu: rà `buy_service_contracts.supplier_id` không khớp `customers.id` trên DB dev (user quyết định có map lại không)

### Checkpoint — 2026-10-22
Vừa hoàn thành: sửa cột NCC ở searchData
Đang làm dở:
Bước tiếp theo: user mở lại màn trên dev sau khi deploy; chạy query rà dữ liệu lệch
Blocked:
