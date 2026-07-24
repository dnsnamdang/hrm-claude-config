# Plan — Bỏ tự sinh Phụ lục HĐLĐ

## Phase 1 — Bỏ tự sinh khi duyệt quyết định

### BE
- [x] Xóa lời gọi `autogenousAppendixLaborContract` trong `SalaryChangeController::toggleApprove`
- [x] Xóa lời gọi `autogenousAppendixLaborContract` trong `TransferPersonnelController::toggleApprove`
- [x] Xóa lời gọi `autogenousAppendixLaborContract` trong `AppointPersonnelController::toggleApprove`
- [x] Xóa lời gọi `autogenousAppendixLaborContract` trong `IncreaseSeniorityController::toggleApprove`
- [x] Lint 4 file PHP — pass
- [ ] Giữ nguyên cron `decision:sync-data-appendix-labor-contract` (không đụng)
- [ ] Giữ lại method `autogenousAppendixLaborContract` trong Service làm dead code (không xóa)

### FE
- [ ] Không thay đổi (màn tạo tay đã có sẵn)

### Checkpoint — 2026-07-13
Vừa hoàn thành: Xóa 4 lời gọi tự sinh phụ lục trong toggleApprove, lint pass.
Đang làm dở: (không)
Bước tiếp theo: Test tay — duyệt 1 quyết định, xác nhận không phát sinh phụ lục; tạo phụ lục tay OK.
Blocked:
