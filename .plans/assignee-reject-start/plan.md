# Plan: Assignee từ chối triển khai khi task chưa có kết quả

## Trạng thái
- Bắt đầu: 2026-04-10
- Hoàn thành: 2026-04-10
- Tiến độ: 6/6 task + 13/13 manual test ✅

## Phase 1: Backend (hrm-api)

### Task.php — state machine
- [x] Task 1: Thêm `hasAnyResult(): bool` ngay sau `canViewResult()` — body độc lập check 4 nguồn (`result_text`, `actual_hours` với `!empty`, `progressLogs->exists`, `resultAttachments->exists`), không delegate canViewResult để tránh drift nghĩa
- [x] Task 2: Case `TODO` trong `getAllowedNextStatuses()` — append `REJECTED_START` khi `$isAssignee && !$this->hasAnyResult()`
- [x] Task 3: Case `IN_PROGRESS` — append `REJECTED_START` trong nhánh `$isAssignee` khi chưa có kết quả (sau block DONE/REVIEW)
- [x] Task 4: Case `PAUSED` — thêm guard `if ($isAssignee && !$this->hasAnyResult())` append `REJECTED_START`

### TaskService.php — defensive
- [x] Task 5: Trong `update()`, sau block validate `allowed_next_statuses`, thêm check trả `['status'=>'422','message'=>'Không thể từ chối triển khai vì task đã có kết quả.']` khi `$newStatus == REJECTED_START && $oldStatus != PENDING_APPROVAL && $task->hasAnyResult()`

### TaskController.php — response 422
- [x] Task 6: Trong action `update()`, thêm nhánh forward `$result['status'] === '422'` qua `$this->responseUnprocessableEntity($result['message'])` (helper có sẵn ở `ApiController:118`)

## Phase 2: Manual test (13/13 PASS)

- [x] Happy: assignee ở TODO/IN_PROGRESS/PAUSED task trắng → thấy option, chuyển thành công
- [x] Chặn: có `result_text` / progress log / result attachment → không thấy option
- [x] Edge: `actual_hours = 0` vẫn cho từ chối (0 coi là rỗng)
- [x] Defensive: API call trực tiếp với status=10 khi đã có kết quả → 422
- [x] No regression: approver PENDING_APPROVAL → REJECTED_START, creator re-assign từ REJECTED_START, assignee ở REVIEW/DONE không thấy option

## Checkpoint

### Checkpoint — 2026-04-10
Vừa hoàn thành: 6/6 task code + 13/13 manual test case. 3 file edited trong hrm-api:
- `Modules/Assign/Entities/Task/Task.php` (+40/-1)
- `Modules/Assign/Services/TaskService.php` (+10)
- `Modules/Assign/Http/Controllers/Api/V1/TaskController.php` (+4)

Frontend không đổi. Syntax pass, 2-stage code review pass, manual test pass.

Đang làm dở: không
Bước tiếp theo: user commit + merge
Blocked: không
