# Plan — Fix thứ tự Họ Tên trong thông báo phân hệ Quản lý dự án (2026-07-13)

## Bối cảnh / Root cause
- Data model: `EmployeeInfo.first_name` = **Họ và đệm**, `last_name` = **Tên** (xác nhận qua label form + validation message).
- Chuẩn hiển thị đúng: **Họ Tên** = `first_name . ' ' . last_name` (chính là cách `fullname` được lưu → dùng `->fullname` là ĐÚNG).
- BUG: code ghép `last_name . ' ' . first_name` = **Tên trước Họ** (sai chuẩn user báo).

## Các chỗ SAI cần fix (grep `last_name.*first_name` trong Modules/Assign — đúng 3 chỗ)
- [x] `Modules/Assign/Services/QuotationService.php:2518` — `currentEmployeeName()` (nội dung thông báo báo giá)
- [x] `Modules/Assign/Services/ProspectiveProjectService.php:1547` — `currentEmployeeName()` (thông báo đóng dự án)
- [x] `Modules/Assign/Http/Controllers/Api/V1/BomPriceApprovalConfigController.php:53` — `changed_by_name` (log lịch sử — không phải notification nhưng cùng lỗi, gộp fix)

## Cách fix
Đổi `last_name . ' ' . first_name` → `first_name . ' ' . last_name` (giữ null-safe `?? ''` + `trim`).

## Xác nhận đầy đủ
- [x] Agent Explore rà soát toàn Modules/Assign: 16 chỗ dùng tên trong notification đều ĐÚNG (dùng `fullname` hoặc helper `currentEmployeeName`/`getCurrentEmployeeName` đã sửa). Ngoài 3 chỗ đã fix, KHÔNG có chỗ nào ghép sai thứ tự.
- [x] Grep verify cuối: `last_name.*first_name` trong Modules/Assign = 0 chỗ.

### Checkpoint — 2026-07-13
Vừa hoàn thành: Fix 3 chỗ ghép tên sai thứ tự (Tên→Họ thành Họ→Tên) trong Assign; audit toàn module xác nhận sạch.
Đang làm dở: (không)
Bước tiếp theo: User build lại queue/worker (nếu notification qua queue) + test đóng dự án / thao tác báo giá → kiểm tra tên hiển thị Họ Tên.
Blocked: (không)
