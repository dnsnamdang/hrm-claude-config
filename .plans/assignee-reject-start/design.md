# Design: Assignee từ chối triển khai khi task chưa có kết quả

## Bối cảnh

`REJECTED_START` (10 - "Từ chối triển khai") hiện chỉ approver set được từ `PENDING_APPROVAL`. Assignee không có cách nào từ chối task đã giao. Yêu cầu: cho phép assignee tự chuyển sang `REJECTED_START` khi chưa bắt tay làm (chưa nhập kết quả).

## Quy tắc

Assignee được từ chối khi **cả 3** thoả:
1. User = `assignee_id`
2. Status hiện tại ∈ {`TODO`, `IN_PROGRESS`, `PAUSED`}
3. Task chưa có kết quả: `result_text` rỗng + `actual_hours` rỗng/0 + `progressLogs` empty + `resultAttachments` empty

Không cần nhập lý do. Sau `REJECTED_START`, luồng creator re-assign giữ nguyên.

## Thay đổi

### Backend (hrm-api)
- `Task.php`: thêm `hasAnyResult(): bool` (body độc lập với `canViewResult` để tránh drift), mở rộng 3 case `TODO`/`IN_PROGRESS`/`PAUSED` trong `getAllowedNextStatuses()` append `REJECTED_START` khi assignee + chưa có kết quả
- `TaskService::update()`: defensive check trả 422 nếu `REJECTED_START` từ trạng thái ≠ `PENDING_APPROVAL` mà task đã có kết quả
- `TaskController::update()`: thêm nhánh forward response `'422'` qua `responseUnprocessableEntity`

### Frontend (hrm-client)
Không đổi. Cả `CreateTaskModal.vue` và `ImportResultModal.vue` đã đọc `allowed_next_statuses` từ backend và render dropdown tự động.

## Không thay đổi
- Luồng approver `PENDING_APPROVAL` → `REJECTED_START` giữ nguyên
- Luồng creator re-assign từ `REJECTED_START` giữ nguyên
- Không notification mới, không field `reject_reason` mới
