# Plan: Fix Bàn giao công việc

## Trạng thái
- Bắt đầu: 2026-03-31
- Tiến độ: V5 bug fix done (Task 13-18). Chờ user test Task 19.


## Danh sách task

[x] Task 1: Fix mất ngày bàn giao khi edit — convert DD/MM/YYYY → YYYY-MM-DD trước khi truyền vào HandoverForm
[x] Task 2: Fix checkbox _selected mặc định checked — đổi thành false khi load edit
[x] Task 3: Sinh bộ testcase Excel — 108 TC, 10 section (DS/Tạo-Sửa/Chi tiết/Tiếp nhận/Chờ duyệt/Chờ tiếp nhận/Phân quyền/BR E2E/Notification/Edge), script `generate_testcase.py`, output `Testcase_Ban_Giao_Cong_Viec.xlsx`

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

### Bug fix V4 (2026-04-25) — Màn chi tiết phiếu bàn giao
[x] Task 8: FE HandoverInfoCard.vue — redesign sang dạng bảng (table) + thêm dòng "Người nhận bàn giao" gộp unique từ items
[x] Task 9: BE HandoverItemResource — thêm `solution_module_id` từ itemable
[x] Task 10: BE DetailHandoverResource + getAvailableItems — trả `receiver_options_by_module` (bổ sung, không dùng FE hiện tại)
[ ] Task 12: Test thủ công — kiểm tra `/assign/handover/:id` hiển thị đúng + người duyệt thay đổi receiver

### Bug fix V5 (2026-04-29) — Receiver hiện nhân sự hạng mục khác
[x] Task 13: FE add.vue — lưu thêm `receiverOptionsByModule` từ response BE (cả loadHandover + loadMyItems) + truyền prop xuống HandoverItemsTable + fix cả _id/index.vue (màn chi tiết/duyệt)
[x] Task 14: FE HandoverItemsTable.vue — thêm prop `receiverOptionsByModule`, helper `getItemRawOptions`, ưu tiên module-level khi item có `solution_module_id`, fallback solution-level. Cả `getItemSelectOptions` + `bulkReceiverSelectOptions` đều dùng logic mới
[x] Task 15: Xoá console.log debug còn sót trong getItemSelectOptions
[x] Task 16: BE DetailHandoverResource — ép `(object)` cho `receiver_options` và `receiver_options_by_module` để giữ key khi Laravel serialize (root cause: Resource serialize mất numeric key → FE lookup bằng solution_id/module_id bị undefined)
[x] Task 17: Test thủ công — tạo + sửa phiếu bàn giao, task thuộc hạng mục A chỉ hiện nhân sự hạng mục A (user confirmed tạo OK)
[x] Task 18: Bug tiến độ không lưu — FE `buildPayload` thiếu `item_progress_pct` + BE `syncItems` không cập nhật progress vào Task. Fix: FE gửi thêm field, BE cập nhật Task.progress_pct trong syncItems (cùng logic approve)
[ ] Task 19: Test thủ công — tạo + sửa phiếu, nhập tiến độ → lưu → reload kiểm tra giá trị

## Checkpoint
- 2026-03-31: 2 bug fix done, merge fix_handover → tpe-develop-assign, pushed GitHub

### Checkpoint — 2026-04-18
Vừa hoàn thành: Bug fix V2 + V3 done. Test OK cả 2 luồng.

### Checkpoint — 2026-04-29
Vừa hoàn thành: V5 — 2 bug fix:
1. Receiver hiện nhân sự hạng mục khác → FE dùng `receiver_options_by_module` ưu tiên module-level + BE ép `(object)` giữ key trong DetailHandoverResource
2. Tiến độ không lưu khi tạo/sửa → FE thêm `item_progress_pct` vào payload + BE `syncItems` cập nhật Task.progress_pct
Đang làm dở: không
Bước tiếp theo: User test Task 19 (tạo + sửa phiếu, kiểm tra tiến độ lưu đúng)
Blocked: không

### Checkpoint — 2026-04-14
Vừa hoàn thành: Sinh `Testcase_Ban_Giao_Cong_Viec.xlsx` (108 TC, prefix HDV)
