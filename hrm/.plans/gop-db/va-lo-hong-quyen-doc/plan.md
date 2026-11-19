# Vá lỗ hổng quyền đọc — Plan

Phương án + quyết định: `phuong-an-6-17-xem-task-issue.md`. Danh sách lỗ hổng: `ghi-chu.md`.

## Đợt 1 — #6 xem Nhiệm vụ + #17 xem Vấn đề — BƯỚC 1 "chỉ ghi log" (user cho phép 11/11)
Nhánh `gop_db-va-quyen-xem-task-issue` (từ origin/gop_db 5d13365e3 / 9fd34c8d9), worktree `websites/wt-quyen-xem-task/{hrm-api,hrm-client}`, API :8071, Nuxt :3071, DB local `db_gop_6_11`. Không migration / seeder / quyền / commit.

- [x] BE: `TaskService::applyListScope` / `IssueService::applyListScope` (public, tách từ index — index gọi lại, không đổi hành vi)
- [x] BE: `Task::canView()` — (a) phạm vi danh sách · (b) meeting gốc `Meeting::canView` · (c) bàn giao hẹp · (d) báo cáo hiệu suất NV (drill lọc theo `assignee_id` ∈ `applyEmployeeScope`)
- [x] BE: `Issue::canView()` — (a) · (c) · (d) · (e) trưởng bộ phận / trưởng phòng xử lý (vấn đề chưa có người xử lý, khớp `notifyHandlingDepartmentLead`)
- [x] BE: `Modules/Assign/Support/WorkItemViewAccess` (viaHandover, viaPerformanceReport, allow ghi log `[QUYEN_XEM_CHI_TIET]` kèm người xem / id / route / referer / user agent). Bật chặn = cấu hình `assign.enforce_item_view` (env `ASSIGN_ENFORCE_ITEM_VIEW`, mặc định false) — `Modules/Assign/Config/config.php`.
- [x] BE: rà route GET đọc theo id — chỉ có 4: `GET assign/tasks/{task}`, `/{task}/comments`, `GET assign/issues/{issue}`, `/{issue}/comments` (lịch sử nạp trong show) ⇒ gắn `allow()` ở `TaskController::show`, `IssueController::show`, `TaskCommentController::index`, `IssueCommentController::index` (không đụng `CommentModeration::commentIndex` dùng chung).
- [x] FE: `CreateIssueModal::fetchIssueDetail` lỗi ⇒ đóng popup; 403 không báo lặp (store đã báo câu BE), lỗi khác giữ câu cũ. Tái hiện trước khi sửa trên :3070 (popup vẫn mở form trống + 2 thông báo).
- [x] PHPUnit `Modules/Assign/Tests/Feature/WorkItemViewAccessTest.php` 15/15 (mỗi nhánh có / không quyền, nháp, danh sách không đổi, API bước 1 200 + log, bật cấu hình ⇒ 403 đúng câu). Hồi quy: `TaskV2ApiTest` 31/31, `MyTodo` 9/9. Không chạy cả `Modules/Assign/Tests` vì một số test kho không dùng transaction.
- [x] Đo hiệu năng `Task::canView` trên dữ liệu thật: 2.8–5.7 ms, 2–20 query / lần mở.
- [x] Playwright: spec MỚI `e2e/tests/assign/issue-detail-access.spec.ts` 4/4 (403 đóng + 1 thông báo · 500 đóng + câu cũ · có quyền mở đủ · không quyền bước 1 vẫn 200 + log đúng người). Hồi quy `task-panel-v2.spec.ts` 6/6 trên :3071. API thật :8071: NV 39 đọc task 532 / vấn đề tạm ⇒ 200 + 3 dòng log; NV 13 không log.
- [ ] Bước 2 (bật 403) — HỎI LẠI sau ~1 tuần đọc log prod (`grep "[QUYEN_XEM_CHI_TIET]" storage/logs/laravel-*.log`)
- [ ] App mobile (TPE_APP) xử lý 403 ở `work_task_detail_page.dart` / `work_issue_detail_page.dart` — hỏi riêng trước bước 2

- [x] (11/11, user chọn cách 1) Bỏ thông báo lặp khi tải chi tiết lỗi: `utils/apiErrorToasted.js` (MỚI — lỗi đã được `plugins/axios.js` tự báo chưa: mất mạng / 401 / 403 / 428 / 500 / 504; silentErrors ⇒ chưa) dùng ở `TaskPanel.vue::fetchDetail` + `CreateIssueModal::fetchIssueDetail`. Tái hiện trên :3070: TaskPanel 403 / 500 hiện 2 thông báo; sau sửa (:3071) còn 1, 404 vẫn câu riêng. E2E: `task-panel-v2.spec.ts` thêm ca 7 ⇒ 7/7; `issue-detail-access.spec.ts` ca 500 + 404 ⇒ 4/4.
- ⚠️ Trước BƯỚC 2: `task-panel-v2.spec.ts` ca 5 cho người ngoài (NV 34) mở xem + tự theo dõi nhiệm vụ — đúng hành vi lỗ hổng #6; bật chặn thì ca này (và nút "Theo dõi" của người ngoài) phải xem lại.

Ngoài luồng (ghi lại, chưa sửa): `GateFixture::grant` (tests/Feature/Rbac) còn ghi `role_has_permissions.company_id` đã bị gỡ khỏi DB gộp ⇒ test dùng hàm này sẽ lỗi.

### Checkpoint — 12/11/2026 (wrap up)
Vừa hoàn thành: Đợt 1 bước 1 (#6 + #17 chỉ ghi log) + bỏ thông báo lặp TaskPanel / popup vấn đề — PHPUnit WorkItemViewAccessTest 15/15, TaskV2Api 31/31, MyTodo 9/9; e2e issue-detail-access 4/4, task-panel-v2 7/7.
Đang làm dở: — (CHƯA commit; worktree `websites/wt-quyen-xem-task` nhánh `gop_db-va-quyen-xem-task-issue`, API :8071 / Nuxt :3071 có thể còn chạy)
Bước tiếp theo: user báo commit / merge; deploy prod TPE bước 1 → ~1 tuần đọc log `[QUYEN_XEM_CHI_TIET]` → hỏi bật 403 (bước 2, xem lại ca 5 task-panel-v2 người ngoài theo dõi) · app TPE_APP xử lý 403 (hỏi riêng) · #18 bàn giao, #19 #20 phiếu ở đợt sau.
Blocked: —
