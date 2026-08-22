# Testcase — Yêu cầu kiểm tra sửa chữa - bảo hành (cổng ERP)

Người phụ trách: @namdangit

## Phase 1 — Viết testcase màn ERP
- [x] Đọc lại code màn ERP để lấy đúng hành vi: `WarrantyRepairRequestsController`, `WarrantyRepairStoreRequest`, `Model/Customers/WarrantyRepairRequest`, các blade `customercare/warranty_repair_requests/*`, `partials/modals/js/searchCustomerJs`, `CustomerManagerController@getListProductOfCustomer`, menu ở `layouts/topmenubar`.
- [x] Sinh `testcase.xlsx` — **69 test case**, P0 chiếm 64%, bằng `gen_testcase.py` (dùng engine chung `tc_engine.py` của bộ skill HRM). Đủ 4 khối chuẩn, không trùng mã TC, bộ kiểm tra thuật ngữ in "sạch".
- [x] Ghi rõ trong tài liệu các đặc thù của cổng ERP mà bản HRM không có / khác:
  - 2 lối vào menu khác nhau (phiếu của tôi ↔ tất cả) dùng chung một màn.
  - Nút **Lưu** và **Lưu & Gửi duyệt** dùng CHUNG một bộ ràng buộc — "Lưu" không phải lưu nháp tự do.
  - Nút **Không duyệt** (từ chối) chỉ có ở màn xem chi tiết, không có ngoài danh sách.
  - Từ chối **không gửi thông báo** cho người lập.
  - Popup chọn khách hàng tách 2 tab; tab khách cá nhân bắt buộc nhập đúng số điện thoại mới ra kết quả.
  - Chức năng **Thêm trang thiết bị của khách hàng** ngay trong form (2 loại: Thiết bị Tân Phát CC / Thiết bị mua NCC khác) + cập nhật số lượng.
  - Bảng danh sách 11 cột, bộ lọc nằm ngay dưới dòng tiêu đề bảng.
