# Plan — Fix modal "Xem serials" rỗng (KH > tab Danh sách thiết bị)

## Bối cảnh
Màn Quản lý khách hàng → tab "Danh sách trang thiết bị" → nút "Xem serials" mở modal "Danh sách serial" rỗng dù thiết bị có serial trong DB.

## Root cause (đã xác minh trên DB erp_new)
- Serial của thiết bị lưu `invoiceable_id` trỏ tới phiếu xuất (product_export_requests) **đã bị xóa** (vd serial 5005/9859/9872 của product 4519 KH 13850 trỏ request 53214/59013/59016 — không còn tồn tại).
- Thiết bị hiện hiển thị trong danh sách qua phiếu khác (PYCXH-17768, 17855).
- `CustomerCareReportService::getProductForReport()` build `$product_['serials']` (data modal) bằng cách gộp serial load **theo từng phiếu** (lọc `invoiceable_id = request_id hiện tại`) → serial mồ côi không match → rỗng.
- Đã loại trừ giả thuyết "code lưu sai detail_id": 0/164 serial có detail trùng product_id (chỉ trùng id ngẫu nhiên giữa 2 bảng). Code SAVE (`SerialController::addSerialToInvoiceable:220`) và LOAD đều dùng đúng request id.

## Reference đúng
Endpoint báo giá `CustomerManagerController::getListProductOfCustomer` (STEP 5, dòng 456-470) load serial bằng `getSerialForProductOfCustomer(..., is_used, invoice=null, getAllSerial=true)` → lấy TẤT CẢ serial của product+customer, KHÔNG lọc theo phiếu → hiển thị đúng cả serial mồ côi.

## Tasks
- [x] Điều tra root cause + xác minh DB
- [x] Đối chiếu endpoint báo giá để chốt cách sửa đúng
- [x] Sửa `CustomerCareReportService::getProductForReport()`: build `$product_['serials']` bằng `getSerialForProductOfCustomer(product_id, product_name, 'tp', null, customer_id, null, false, null, true)` (getAllSerial), giữ nguyên `productExportAndBorrow` per-phiếu
- [x] Re-inject thông tin bảo hành (`$serial['product']`) để cột Ngày nghiệm thu/Thời gian bảo hành vẫn hiển thị
- [x] `php -l` kiểm tra cú pháp
- [x] Verify tinker: call mới trả về đủ 3 serial cho thiết bị máy nén khí (KH 13850)
- [x] Commit + push nhánh `fix-xem-serials-khach-hang-mo-coi`
- [x] Merge vào `master` + push (merge commit, master HEAD `e58cc78f94`)
- [ ] User test browser xác nhận lần cuối + deploy pull code server (không có migration)

## Phạm vi sửa
- `app/Services/CustomerCare/CustomerCareReportService.php` (nhánh `productGroupTp`, ~dòng 719-737)
- KHÔNG sửa hàm dùng chung `Serial::getSerialForProductOfCustomer`, KHÔNG sửa FE.

### Checkpoint — 2026-06-23
Vừa hoàn thành: Sửa service (getAllSerial + re-inject bảo hành), php -l sạch, verify tinker 3 serial, commit + merge vào master + push (HEAD e58cc78f94).
Đang làm dở: không.
Bước tiếp theo: User test browser lần cuối + pull code server. Không có migration.
Blocked:
