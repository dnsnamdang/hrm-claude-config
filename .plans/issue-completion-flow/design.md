# Issue Completion Flow — Tóm tắt thiết kế

**Người phụ trách:** @khoipv
**Module:** Assign / Issues
**Spec chi tiết:** [docs/superpowers/specs/2026-04-28-issue-completion-flow-design.md](../../hrm-api/docs/superpowers/specs/2026-04-28-issue-completion-flow-design.md)

## Mục tiêu

Bổ sung 2 trạng thái mới `completed` (Hoàn thành) và `rejected` (Từ chối) vào flow quản lý Issue, hỗ trợ luồng duyệt đóng bởi approver.

## Scope

### Luồng KHÔNG có người duyệt đóng
- Assignee chuyển trực tiếp: `in_progress` → `completed`
- Không cần thêm bước nào

### Luồng CÓ người duyệt đóng
- Assignee: `in_progress` → `resolved` (gửi kết quả)
- Approver duyệt: `resolved` → `completed`
- Approver từ chối: `resolved` → `rejected` (bắt buộc nhập lý do)
- Assignee nhận lại: `rejected` → `in_progress` (tiếp tục xử lý rồi gửi lại)

### Quyết định lớn
- Giữ cả 2 trạng thái `closed` (Creator đóng) và `completed` (kết thúc qua flow duyệt)
- Creator có thể đóng (`closed`) từ mọi trạng thái trừ `completed`
- Cả `completed` và `closed` đều có thể `reopened` bởi Creator
- Approver không cần ghi chú khi duyệt (chỉ cần click)
- Notification tự động cho approver khi issue chuyển resolved, và cho assignee khi bị rejected

## Thay đổi chính

| Layer | File | Thay đổi |
|-------|------|----------|
| Migration | `2026_04_28_000001_add_completion_fields_to_issues_table.php` | Thêm `completed_at`, `rejected_at`, `rejected_reason` |
| Entity | `Issue.php` | 2 const + STATUS_DATA + casts + `isApprover()` + `hasApprover()` + cập nhật `canEdit/canHandle/getAllowedNextStatuses` |
| Service | `IssueService.php` | Timestamp handling trong `update()` + `changeStatus()` + notification methods |
| Request | `IssueUpdateStatusRequest.php` | Validate `reason` required khi rejected |
| Resource | `DetailIssueResource.php` | Thêm fields + ENUM_MAPS + DATE_FIELDS |
| Controller | `IssueController.php` | Thêm `completed` vào overdue exclusion |
| FE Index | `index.vue` | Filter + label + color cho 2 status mới |
| FE Modal | `CreateIssueModal.vue` | Rejected reason display/input + validation + payload |
