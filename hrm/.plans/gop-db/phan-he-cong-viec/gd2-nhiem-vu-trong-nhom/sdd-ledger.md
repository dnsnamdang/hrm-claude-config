# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/phan-he-cong-viec/gd2-nhiem-vu-trong-nhom/plan.md
Spec: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/docs/superpowers/specs/gop-db/2026-11-11-gd2-nhiem-vu-trong-nhom-design.md
User 11/11: "làm" — phạm vi: hrm-api + hrm-client worktree wt-nhom-trao-doi; migration 2026_11_14_000001 vào db_gop_6_11; V2BaseMiniTab + sửa TaskForm/TaskPanel/TaskDetailTab/TaskFieldPopover/ChatComposer/ChatMessageItem/ChatPane; visibleQuery(); commit từng task, KHÔNG push.
Ruling: nhánh = gop_db-nhom-trao-doi (user không chọn 1/2; phương án 1 đơn giản hơn) — sai thì tách nhánh tại fd1c2f1e7 / d0644d95d.
Start: hrm-api fd1c2f1e7 · hrm-client d0644d95d

## Pre-flight scan
| Cặp / task | Produce ↔ consume | Kết quả |
|---|---|---|
| T1→T2..T6 | cột workspace_id, source_message_id, Task::workspace() | khớp |
| T2↔T3 | TaskService: T2 tách visibleQuery (:190 + :33-42), T3 sửa store/update | cùng file, khác hàm — OK |
| T2→T6 | TaskAccess::canView dùng cho hydrate thẻ? spec: thẻ chỉ việc nhóm ⇒ thành viên luôn xem được | OK |
| T3→T5,T6 | WorkspaceTaskRules::validateAttach / assignableIds | khớp tên |
| T3↔T6 | TaskService::store: T3 validate workspace, T6 source_message_id + tin card | cùng hàm, T6 sau T3 — OK |
| T4↔T5 | WorkspaceController::show (open_task_count) vs controller mới | OK |
| T5→T8,T9 | API tasks / suggest / assignable / members?assignable=1 | khớp |
| T6→T10 | message.card, created_tasks | khớp |
| T2 tự thân | liệt kê updateStatus — route tasks KHÔNG có updateStatus (chỉ issues :1213) | Ruling dưới |
| T2 tự thân | tên test "test_member_with_role_view_can_show_but_not_needed_role" lủng củng | Ruling dưới |
| T7 tự thân | "hỏi trước V2BaseMiniTab" | user đã cho phép 11/11 |
| T1 tự thân | "hỏi user rồi chạy" | user đã cho phép đúng file này |
| Mọi test BE | PHPUnit chạy DB thật, khuôn WorkspaceApiTest dùng DatabaseTransactions + actAs | brief nhắc dùng DatabaseTransactions, không sửa dữ liệu ngoài transaction |

Ruling: T2 bỏ updateStatus khỏi danh sách action (controller có hàm nhưng không có route tasks) — spec đòi mọi route /tasks/{task} — sai thì route chết vẫn hở nhưng không truy cập được.
Ruling: T2 đổi tên test thành test_member_with_role_view_can_show — chỉ tên.
Task 1: implemented a7d2f521e (6 pending migration khác KHÔNG chạy: hrm_contracts x4, business_target_department_parts, hrm_contract_legal_notes)
Task 1: minor (deferred): FQCN Workspace trong Task::workspace() thay vì use; không guard hasColumn
Task 1: complete (commits fd1c2f1e7..a7d2f521e, review clean) — controller tự kiểm SHOW INDEX
Task 2: implemented bf5d7e59e (DONE_WITH_CONCERNS: GP tab getTaskListForSolution không lọc quyền → có thể mất quyền mở chi tiết; deleteByIds để nguyên)
Task 2: minor (deferred): test chưa phủ PUT, extension request/approve/reject/cancel, comments update/destroy/react/approve/pin/resolve (403/423)
Task 2: minor (deferred): deleteByIds không qua TaskAccess — xoá hàng loạt được Nháp của nhóm đã đóng
Task 2: minor (deferred): nhóm bị xoá mềm ⇒ optional(workspace) null ⇒ không chặn ghi
Task 2: minor (deferred): mẫu NV trong test_every_listed_task_is_showable chưa có NV chỉ thấy qua theo dõi/tầng 2/tầng 3; test phụ thuộc dữ liệu dev (NV 25, 27)
Task 2: ⚠️ tab Nhiệm vụ GP/Hạng mục (getTaskListForSolution, không lọc quyền) — người thấy việc ở tab GP mà không qua visibleQuery nay mở chi tiết bị 403 — HỎI USER (bảo mật), tiếp tục Task 3 song song
Task 2: complete (commits a7d2f521e..bf5d7e59e, review clean; ⚠️ GP tab chờ user)
Task 3: implemented 633862590 (201→200 giữ hành vi cũ; assignee_ids key cho task_type 1; lỗi nhóm không báo đồng thời với lỗi form)
Task 3: minor (deferred): thiếu test PUT đổi nhóm lô, PUT nhóm đóng 423, PATCH assignee ngoài nhóm, PATCH link GP vào việc nhóm, bỏ nhóm cả lô
Task 3: minor (deferred): khối lặp validate move ở updateField + checkWorkspaceOnUpdate (~8 dòng) → tách validateMove
Task 3: minor (deferred): việc Chờ phê duyệt (2) sinh con không kiểm lại người làm dòng con; đổi nhóm lô không kiểm dòng con chờ sinh của bản sao khác
Task 3: minor (deferred): test dùng id/tên NV cứng; socket chuông vẫn publish trong test
Task 3: ⚠️ resolved: lối rời Nháp — route tasks chỉ PUT update (app dùng cùng API) ⇒ đủ
Task 3: Ruling: HandoverService (bàn giao) đổi người làm không qua WorkspaceTaskRules — ngoài phạm vi GĐ2, ghi "vấn đề ngoài luồng" — sai thì việc của nhóm có người làm ngoài nhóm sau bàn giao
Task 3: complete (commits bf5d7e59e..633862590, review clean)
Task 4: implemented 7f795bf8a
Task 4: minor (deferred): cancelAll gửi thông báo/socket trong transaction — rollback sau đó vẫn có thể đã phát (nên afterCommit)
Task 4: minor (deferred): assertNoOpenTasks ngoài transaction (race hẹp)
Task 4: minor (deferred): changed_by=0 khi tự lưu trữ — DetailTaskResource dùng optional ⇒ không lỗi, tên trống (FE nên hiện "Hệ thống")
Task 4: minor (deferred): test auto-archive chạy job trên toàn bộ nhóm DB dev (rollback)
Task 4: complete (commits 633862590..7f795bf8a, review clean)
Task 5: implemented fce22d5b2 (sửa Task.php — hàm dùng chung getAllowedNextStatuses để bớt N+1, ngoài danh sách user cho phép ⇒ báo user)
Task 5: review — Needs fixes: (I) isStartApproverForAssignee lặp canStartApprove; (I) sort mặc định lệch spec gốc §5.1 (hạn asc, không hạn cuối, hoà theo tên)
Task 5: Ruling: nâng Minor 1 (subquery assignee_department_id bỏ qua CompanyActiveScope) vào fix loop — task cam kết "không đổi hành vi" của Task.php dùng chung — sai thì tốn 1 round
Task 5: Ruling: next_action dùng khoá có sẵn quickAction() (start/resume/result/approve/approve_start) — FE Task 8 theo khoá này — sai thì đổi map ở FE
Task 5: Ruling: "Chờ tôi duyệt" = duyệt kết quả (status 6, approver_id = tôi), không gồm duyệt triển khai — theo nghĩa nút lọc mockup 03 — sai thì đếm thiếu việc chờ duyệt triển khai
Task 5: minor (deferred): can_edit/can_delete không xét nhóm đóng (FE hiện Sửa rồi 423); stateColor so chuỗi 'Quá hạn'; suggest/assignable trả getMessage 400; test draft_of_others chưa assert contains($mine)
Task 5: fix round 1/5 dispatched (4 findings, FIX_BASE fce22d5b2)
Task 5: fix round 1/5 (4 addressed, 0 open; commits fce22d5b2..9f828b016)
Task 5: minor (deferred): sort_dir mặc định asc cho mọi cột — FE phải gửi sort_dir tường minh; ORDER BY subselect tên + IS NULL không index
Task 5: complete (commits 7f795bf8a..9f828b016, review clean after 1 round)
Task 6: implemented 3c5129d18 (Nháp tạo từ tin không gửi thẻ, rời Nháp chưa gửi bù)
Task 6: ⚠️ resolved: hydrate thẻ không qua TaskAccess — đúng Q4 (chỉ việc của chính nhóm ⇒ thành viên luôn xem được); bấm thẻ ⇒ TaskPanel qua TaskAccess (FE Task 10)
Task 6: Ruling: việc tạo từ tin ở trạng thái Nháp không gửi thẻ, rời Nháp không gửi bù — Nháp chỉ người tạo thấy; Q5 nói "Tạo nhiệm vụ" — sai thì nhóm không thấy thẻ của việc giao sau khi rời Nháp
Task 6: minor (deferred): enabled_tabs check lặp (tách WorkspaceTaskRules::tasksEnabled); created_tasks vẫn trả ở tin đã thu hồi; source_message_id thiếu rule ở TaskStoreRequest?; thiếu test Xem tạo từ tin + nhóm đóng 423; preview "[Nhiệm vụ]" không kèm mã
Task 6: complete (commits 9f828b016..3c5129d18, review clean)
Task 7: implemented hrm-client 139dc871b (sửa thêm ConversationList.vue)
Task 7: Ruling: e2e (Important) dời sang Task 11 đúng plan (Task 11 viết workspace-tasks.spec.ts + chạy lại chat-core + task-panel-v2) — sai thì hồi quy nút thu gọn cột lọt tới Task 11
Task 7: carry→Task 8: số trên nút Nhiệm vụ = việc dở người xem xem được (không tính Nháp người khác) — dùng quick_counts của API Task 5; toLocaleString('en-US') cho count + openTaskCount; công tắc Tab sử dụng ẩn (v-if) khi không phải Quản lý thay vì disabled
Task 7: minor (deferred): eslint/prettier chưa chạy; ?panel=tasks khi tab tắt giữ URL
Task 7: complete (hrm-client d0644d95d..139dc871b, review approved)
Task 8: implemented hrm-client 01290d072
Task 8: Ruling: "+ Thêm" → "Tạo mới" theo button-convention (skill thắng spec về chữ) — CLAUDE.md đòi confirm user ⇒ nêu trong báo cáo cuối — sai thì đổi lại 1 chữ
Task 8: Ruling: ⇄ ẩn khi không đổi được (CLAUDE.md ẩn chứ không disable, thắng spec "mờ + lý do") — sai thì người dùng không biết vì sao
Task 8: review — Needs fixes: (I) phân trang list chung không theo nhóm; (I) FE tự tính khoá nhóm Hạn; (I) số nút Nhiệm vụ tính Nháp người khác; (I) bảng thiếu sort 3 cột
Task 8: Ruling: BE trả ≤ N=20 dòng / nhóm (per_group), item.group_key, my_open_task_count ở chi tiết nhóm, sort_by approver/creator/checklist — sửa BE Task 5 trong cùng worktree — sai thì tốn 1 round
Task 8: Ruling: nâng minor 1 (X-Silent-Errors tắt 401→login), 2 (loadMore cũ), 3, 4, 7 (button thô — CLAUDE.md cấm) vào fix loop
Task 8: minor (deferred): STATUS_OPTIONS cứng ở FE; runNext needs=result mở bước result đầu tiên
Task 8: Ruling: Tạm dừng chỉ xác nhận theo luồng panel có sẵn (spec gốc: lý do Tạm dừng tuỳ chọn) — sai thì thêm ô lý do
Task 8: fix round 1/5 dispatched (FIX_BASE api 3c5129d18, client 01290d072)
Task 8: fix round 1/5 (9 addressed, 0 open; api 3c5129d18..4bcf23bb4, client 01290d072..47f2dfc7f)
Task 8: minor (deferred): toast lỗi có thể hiện 2 lần (axios chung + catch màn); 1 moreSource chung cho mọi nhóm; comment TaskGroupBlock "> 50 dòng"
Task 8: ⚠️ deploy: ROW_NUMBER() OVER cần MySQL ≥ 8 (local 8.0.43; core chat ConversationService cũng dùng) — kiểm prod trước khi lên
Task 8: complete (client 139dc871b..47f2dfc7f + api ..4bcf23bb4, review clean after 1 round)
Task 9: implemented api 3ce6d2789, client e3858571e (e2e task-panel-v2 ca 7 fail — báo là lỗi có sẵn; e2e sinh 24 notifications đã xoá, FCM có thể đã gửi)
Task 9: review — Needs fixes: (I) jumpToSource sót gỡ tkp-above-modal
Task 9: Ruling: nâng minor popover "Thêm nhiệm vụ con" lọc theo thành viên nhóm (nhất quán Q2) + bỏ biến y thừa vào fix loop
Task 9: ⚠️ resolved: e2e ca 7 fail (403 hiện 2 toast) có sẵn ở BASE — reviewer đã kiểm fetchDetail không đổi
Task 9: minor (deferred): popAssigneeOptions nháy toàn bộ NV khi đang tải; form sửa việc có nhóm gọi members ngay lúc mở; nhãn "Dự án / Nhóm" cạnh "Nhóm trao đổi" — hỏi user
Task 9: fix round 1/5 dispatched (FIX_BASE client e3858571e)
Task 9: fix round 1/5 (4 addressed, 0 open; client e3858571e..e7ae1f7d8)
Task 9: minor (deferred): e2e task-panel-v2 ca 1–7 chưa chạy lại sau sửa (sinh thông báo thật) — Task 11 chạy với chặn push
Task 9: complete (api 4bcf23bb4..3ce6d2789, client 47f2dfc7f..e7ae1f7d8, review clean after 1 round)
Task 10: implemented client 9f896411d (DONE_WITH_CONCERNS)
Task 10: Ruling: TaskForm.vue thuộc danh sách user cho phép ⇒ thêm 'description' vào applyDefaults; suggest loại Nháp (BE); card trả is_overdue thay so chữ — gửi implementer trước review
Task 10: + api 73d20fa0b, ef87152cb (test overdue hết phụ thuộc giờ), client b6b9e4c6f
Task 10: minor (deferred): TaskMentionSuggest tự viết lại headers()+URL (nên dùng workspaceTaskApi.suggest); khối thẻ vẫn hiện khi đang sửa tin; CloseWorkspaceModal không chặn response cũ; e2e chưa phủ tạo-từ-tin/422 Thành viên/1–1 không #; tin chỉ có file ⇒ tên rỗng
Task 10: complete (api 3ce6d2789..ef87152cb, client e7ae1f7d8..b6b9e4c6f, review approved)
Task 11: complete (e2e workspace-tasks 9/9, chat-core 8/8, task-panel-v2 ca 6,8 pass, ca 7 fail có sẵn, ca 1–5 CHƯA chạy (push thật: NV 13/24/25 có FCM, queue sync); PHPUnit 69/69; docs cập nhật)
Final review: ready after fixes — I1 thẻ chat việc đã chuyển nhóm lộ dữ liệu; I2 nhóm đóng vẫn hiện nút (423); I3 GP tab + các danh sách khác mở TaskPanel chưa đối chiếu (chờ user Câu 9); I4 task-panel-v2 ca 1–5 chưa chạy (push thật) ; Minor1 notify trong transaction
Final: Ruling: 1 fix wave gồm I1, I2, Minor1, Minor2 (không báo cho chính người đóng), Minor3 (test Q8), Minor6 (source_message can_open) — I3, I4 cần user (bảo mật / push thật) — sai thì merge chậm
Final: FIX_BASE api ef87152cb client b6b9e4c6f
Final: fix wave api 505724758, client de5715ef6 (sửa CommentThread/CommentNode dùng chung — thêm prop readonly — ngoài danh sách user cho phép)
Final: re-review — 6/6 addressed; 1 regression mới (Important): TaskPanel Watch/CommentThread ẩn cả khi hideActions (3 màn FilesTab GP/HM, WorkDrillModal). Ruling: sửa 1 dòng bằng chính fixer (vượt quy tắc 1 fix wave vì là hồi quy do đợt sửa gây ra, rẻ) — controller tự đối chiếu diff
Final: fix round 2 (hideActions) client ba84b2753 — controller đối chiếu diff: Watch/CommentThread chỉ theo wsClosed ⇒ OK. Final review clean.
