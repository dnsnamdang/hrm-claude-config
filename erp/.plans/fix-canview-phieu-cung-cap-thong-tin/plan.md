# Fix: người yêu cầu không xem được chi tiết phiếu cung cấp thông tin làm báo giá

**Mục tiêu:** Người yêu cầu (tạo phiếu SC) xem được chi tiết "Phiếu cung cấp thông tin làm báo giá" — đồng nhất với list "Chờ tạo báo giá".

## Bối cảnh
- Màn: `admin/customer-care/warranty_repair_information_requests?permission=waiting_create_quotation`.
- Case: Vũ Ngọc Nam (emp 84) thấy phiếu + nút "Từ chối tiếp nhận" ở list, nhưng bấm chi tiết → "không có quyền" (view not_found).

## Root cause
Bất nhất giữa list và detail:
- **List** `WrServiceQuotation::searchByFilter` nhánh `waiting_create_quotation` (dòng 452-456): lọc theo `warranty_repair_request.created_by = user` (người yêu cầu).
- **Detail** `WrServiceQuotation::canView()` (dòng 299): chỉ true nếu `created_by == user` (người LẬP phiếu) hoặc có quyền "Xem phiếu cung cấp thông tin theo tổng/cty/phòng". KHÔNG xét người yêu cầu.
- Phiếu 9090: `created_by`=371 (người lập, Đỗ Trung Tuấn), `warranty_repair_request.created_by`=84 (Nam). Nam không có quyền "Xem" → canView=FALSE.

## Tasks
- [x] `canView()`: thêm nhánh — type=INFORMATION + status != STATUS_CREATING + `warranty_repair_request.created_by == user` → true.
- [x] Verify (prod erp_new): Nam(84) canView(9090) FALSE → TRUE. `php -l` sạch.

### Checkpoint — 2026-06-16
Vừa hoàn thành: fix canView cho người yêu cầu phiếu cung cấp thông tin.
Bước tiếp theo: user test bấm chi tiết phiếu bằng tài khoản Nam.
Blocked:
