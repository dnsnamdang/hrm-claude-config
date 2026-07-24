# Bỏ tự sinh Phụ lục HĐLĐ — Tóm tắt

**Người phụ trách:** @namdangit
**Ngày:** 2026-07-13

## Mục tiêu
Khi duyệt (approve) 4 loại quyết định, hệ thống KHÔNG còn tự tạo bản ghi Phụ lục HĐLĐ nữa. Phụ lục HĐLĐ chỉ được tạo thủ công qua màn `/decision/appendix-labor-contract`.

## Hiện trạng (trước khi sửa)
Việc tự sinh chạy khi `status == STATUS_APPROVED` trong hàm `toggleApprove` của từng loại quyết định:
- Điều chỉnh lương — `SalaryChangeController::toggleApprove`
- Điều chuyển — `TransferPersonnelController::toggleApprove`
- Bổ nhiệm — `AppointPersonnelController::toggleApprove`
- Tăng lương thâm niên — `IncreaseSeniorityController::toggleApprove`

Mỗi nơi gọi `autogenousAppendixLaborContract(...)` → `updateOrCreate`/`create` bản ghi phụ lục (status = Đã duyệt).

## Quyết định
- Bỏ tự sinh cho **cả 4 loại**.
- **Giữ nguyên** cron `decision:sync-data-appendix-labor-contract` (01:00 hằng ngày) — phụ lục tạo tay, đã duyệt, đến hạn hiệu lực vẫn tự đồng bộ vào dữ liệu nhân sự/lương.
- **Giữ lại** các method `autogenousAppendixLaborContract(...)` trong Service làm dead code (không xóa) để dễ khôi phục nếu cần bật lại; DI service inject giữ nguyên.
- Không đụng frontend.

## Cách làm
Chỉ backend: xóa đúng 1 dòng gọi `autogenousAppendixLaborContract(...)` trong mỗi block `if ($request->status == STATUS_APPROVED)` của 4 controller; giữ lại phần ghi lịch sử phê duyệt.

## Rủi ro
Rất thấp — chỉ xóa lời gọi bên trong transaction, phần còn lại của luồng duyệt không đổi.
