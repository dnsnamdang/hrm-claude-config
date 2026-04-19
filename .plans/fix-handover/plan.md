# Plan: Fix Bàn giao công việc

## Trạng thái
- Bắt đầu: 2026-03-31
- Tiến độ: 7/7 task done (Task 4 FE đã thử nhưng revert intentional). Test OK 2026-04-18.

## Danh sách task

[x] Task 1: Fix mất ngày bàn giao khi edit — convert DD/MM/YYYY → YYYY-MM-DD trước khi truyền vào HandoverForm
[x] Task 2: Fix checkbox _selected mặc định checked — đổi thành false khi load edit

### Bug fix V2 (2026-04-18) — Branch: tpe-develop-assign (merge thẳng)
[x] Task 3: BE HandoverService.syncItems — đổi exception code 422→423 (lỗi nghiệp vụ); đổi text "Các mục sau đã nằm trong phiếu bàn giao khác chưa hoàn tất" → "Có task đã được bàn giao trong 1 phiếu khác chưa hoàn tất"; lấy `task.code` / `issue.issue_code` thay vì `Task #id`/`Issue #id`
[~] Task 4: FE handover/add.vue — đã thử bổ sung fallback `data.message` cho 422 nhưng bị revert (intentional). Bug vẫn fix được nhờ Task 3 (BE đổi 422→423 → FE 423 handler đã đọc `data.message` đúng). Defense-in-depth FE chưa có — chấp nhận.
[x] Task 5: Verify — test thực tế OK (2026-04-18): cả V2 (duplicate task message) + V3 (reject sau TP duyệt → chuyển task về TP) đều pass

### Update logic V3 (2026-04-18) — Reject sau khi TP duyệt → chuyển task về TP
[x] Task 6: BE HandoverService.rejectItem — khi receiver từ chối:
      - Throw exception 423 nếu `handover->approved_by` null (data integrity check — đáng lẽ APPROVED phải có approved_by)
      - Set `itemable->assignee_id = handover->approved_by` (chuyển task về TP đã duyệt)
      - Log: thêm câu "Task được chuyển sang <TP_name>"
      - Notify thêm cho TP qua helper `sendTaskTransferredToApproverNotification`: "Bạn vừa được giao <code> do <receiver> từ chối tiếp nhận từ phiếu bàn giao <handover_code>"
[x] Task 7: Cập nhật design.md — sửa Business Rule #6

## Checkpoint
- 2026-03-31: 2 bug fix done, merge fix_handover → tpe-develop-assign, pushed GitHub

### Checkpoint — 2026-04-18
Vừa hoàn thành: Bug fix V2 — đổi exception code BE; FE giữ nguyên (Task 4 fallback đã revert intentional)
- BE `HandoverService.syncItems`: 422 → 423; text mới + lookup task.code/issue.issue_code
- FE add.vue: defense-in-depth bị revert, không sao vì 423 handler đã đọc data.message đúng

### Checkpoint — 2026-04-18 (Update logic V3)
Vừa hoàn thành: Reject sau khi TP duyệt → chuyển task về TP (Task 6 + 7)
- BE `HandoverService.rejectItem` (line 519-568):
  + Guard: throw 423 nếu `handover->approved_by` null (data integrity)
  + Set `itemable->assignee_id = handover->approved_by`
  + Log thêm "Task được chuyển sang <TP_name>"
  + Notify thêm cho TP qua helper mới `sendTaskTransferredToApproverNotification` (line 765-800)
- Helper `sendTaskTransferredToApproverNotification`: lookup `Employee->employee_info_id`, content "Bạn vừa được giao <code> do <receiver> từ chối tiếp nhận từ phiếu bàn giao <handover_code>", try-catch tránh bể flow
- design.md: Business Rule #6 update từ "assignee giữ nguyên" → "chuyển về TP đã duyệt phiếu"

Đang làm dở: Task 5 — chờ user test thực tế cả 2 luồng (V2 + V3)
Bước tiếp theo:
  1. **Test V2**: 2 tab cùng chọn 1 task → tab 1 "Lưu nháp" → tab 2 "Lưu và gửi" → toast "Có task đã được bàn giao trong 1 phiếu khác chưa hoàn tất: <code>"
  2. **Test V3 happy path**: TP đã duyệt phiếu → receiver từ chối item → task chuyển sang TP + log hiện tên TP + TP nhận noti + creator nhận noti
  3. **Test V3 edge case**: Giả lập `approved_by` null → toast 423 "Phiếu bàn giao thiếu thông tin người duyệt"
  4. **Test regression**: Validate form (thiếu ngày bàn giao) → vẫn hiện "Bạn chưa nhập đầy đủ thông tin"
Blocked: không có
