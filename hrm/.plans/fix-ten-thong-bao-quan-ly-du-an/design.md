# Design — Fix thứ tự Họ Tên trong thông báo phân hệ Quản lý dự án

## Mục tiêu
Thông báo (notification) phân hệ quản lý dự án (Modules/Assign) hiển thị tên nhân viên sai chuẩn tiếng Việt: đang "Tên trước Họ", cần "Họ Tên".

## Root cause (đã xác minh)
- `EmployeeInfo.first_name` = **Họ và đệm**, `last_name` = **Tên** (theo label form + validation message).
- Chuẩn đúng "Họ Tên" = `first_name . ' ' . last_name` — cũng chính là cách field `fullname` được lưu → dùng `->fullname` là ĐÚNG.
- Bug: vài chỗ ghép ngược `last_name . ' ' . first_name` = "Tên trước Họ".

## Scope (BE, Modules/Assign) — sửa 3 chỗ (đổi thành `first_name . ' ' . last_name`)
- `Services/QuotationService.php:2518` — `currentEmployeeName()` (thông báo báo giá/duyệt/từ chối).
- `Services/ProspectiveProjectService.php:1547` — `currentEmployeeName()` (thông báo đóng dự án/chốt giải pháp).
- `Http/Controllers/Api/V1/BomPriceApprovalConfigController.php:53` — `changed_by_name` (log lịch sử đổi config; không phải notification nhưng cùng lỗi → gộp fix).

## Quyết định
- **Không** đụng field `fullname` global (blast radius lớn); chỉ sửa các chỗ ghép tay bị ngược.
- Audit toàn Modules/Assign (agent Explore + grep `last_name.*first_name`): 16 chỗ tên trong notification đều đúng (dùng `fullname` / helper đã sửa); 0 chỗ còn ghép ngược sau fix.

## Trạng thái
CODE DONE 2026-07-13. Chờ user build + restart queue worker (nếu notification qua queue) + test.
