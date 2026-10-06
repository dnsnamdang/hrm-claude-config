# Đề nghị tra soát admin — tra soát theo phiếu (Redmine #11523) — @namdangit

Nhánh `task_11523` (checkout từ `origin/gop_db`) ở cả 2 repo, worktree `HRM/worktrees/task_11523-api|client`.

## Quyết định đã chốt (30/09/2026)
- Loại "Tra soát ca làm việc": GIỮ logic cũ — ẩn ô Ca/phiếu, admin vẫn tra soát nhiều NV khác ca được.
- 5 loại phiếu: phải chọn NV trước, ô Ca/phiếu chỉ liệt kê phiếu CHUNG (cùng loại + cùng id phiếu) của mọi NV đã chọn trong ngày làm việc.
- Tách thân `TimekeeperController::listTimesheetTypes` sang `TimesheetService::listTimesheetTypesOf()` (không đổi hành vi app).

## Phase 1 — BE
- [x] Migration thêm `timesheet_type`, `timesheet_type_id`, `job_assign_id`, `timesheet_type_name` vào `admin_request_update_workings`
- [x] Tách `listTimesheetTypesOf()` ra `TimesheetService`, controller app gọi lại
- [x] API `GET timesheet/admin-request-update-working/timesheet-types?date=&employee_ids[]=` trả ca/phiếu chung
- [x] FormRequest: validate loại + ca/phiếu bắt buộc theo loại + kiểm phiếu chung của các NV
- [x] Store: lượt chấm công tra soát theo phiếu ghi `type=1, accept=1, job_type/job_id/job_assign_id` như lúc duyệt đề nghị của NV

## Phase 2 — FE
- [x] Màn Thêm: ô Loại tra soát, Ca/phiếu (hiện khi chọn loại phiếu), Phiếu công việc được giao (phiếu kỹ thuật)
- [x] Màn Chi tiết: hiện Loại tra soát + Ca/phiếu
- [x] Sửa: sai "Phiếu công việc được giao" báo lỗi dưới đúng ô job_assign_id (trước báo dưới Ca/phiếu)
- [x] Test API 46 case (5 loại phiếu lưu thật + 7 case nghịch + hồi quy app listTimesheetTypes so với bản gop_db cổng 8003) + UI Playwright luồng phiếu kỹ thuật + chi tiết bản ghi mới/cũ; đã xoá dữ liệu test 1693-1700 và tính công lại

### Checkpoint — 2026-09-30
Vừa hoàn thành: commit + push nhánh task_11523 (api f57af5249, client 17dc3e5e5), merge vào develop và push (api 9f8967e0c, client 82d9650cc)
Đang làm dở: —
Bước tiếp theo: deploy develop lên server dev + chạy migration 2026_09_30_000001 + route:cache; chưa merge về gop_db
Blocked:
