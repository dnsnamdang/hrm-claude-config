# App — Việc của tôi: lọc chọn nhiều + sắp xếp (tab Danh sách) — @namdang

Yêu cầu 02/11/2026: "Bộ lọc cho phép chọn nhiều ở Loại việc và Trạng thái · Thêm tuỳ chọn sort như màn tasks".

## Quyết định đã chốt (02/11)
- Trạng thái = 4 nhóm như tab Lịch (Chưa làm · Đang làm · Hoàn thành · Dừng/Huỷ) — BE `WorkItemStatusGroup`. Không chọn = "Chưa xong" như cũ.
- Kiểu xếp: Hạn hoàn thành (mặc định) · Cập nhật gần nhất · Tạo gần nhất · Ưu tiên cao trước · Tên A→Z. Giữ nhóm theo hạn, xếp trong nhóm. Nhớ lựa chọn trên máy.
- Claude tự chọn: nhóm Hoàn thành / Dừng-Huỷ của 5 loại phiếu chỉ lấy bản cập nhật trong 30 ngày (PENDING_LOOKBACK_DAYS). Việc cá nhân đã xong không giới hạn (như lọc "Đã xong" cũ). Phiếu chấm công chỉ có Đang làm (chưa nhập KQ) / Hoàn thành (đã nhập KQ).

## Task
### BE (hrm-api, gop_db local → đẩy develop + gop_db qua worktree khi được cho push)
- [x] `WorkItemStatusGroup::ALL` + `statusesOf()`
- [x] `MyTodoService::normalizeItem()` trả `status_group`, `created_at`, `updated_at`
- [x] `getAll()` nhận `status_groups[]` → `collectByStatusGroups()` + `getClosedItems()`; không gửi = y như cũ
- [x] `TimesheetWorkItems::listItem()` trả `status_group`, `created_at`, `updated_at`
- [x] `MyTodoController::index` nhận `status_groups`
- [x] Kiểm tinker: U13/U341 todo+doing = pending cũ; done/stopped đúng (setTestNow 15/09 cho task status 8)
### App (TPE_APP develop)
- [x] `WorkItem`: createdAt / updatedAt / priority + priorityRank
- [x] `MyTodoApiService.fetchItems(statusGroups)`
- [x] `ui/my_todo/my_todo_sort.dart`
- [x] `my_todo_list_view.dart`: Loại + Trạng thái chọn nhiều, nút ⇅, nhớ kiểu xếp
- [x] Bấm thử simulator tpeLocal (namdangit): lọc Meeting+Cá nhân × Chưa làm+Hoàn thành ra 5 = số BE; xếp Tên A→Z đúng; restart vẫn nhớ kiểu xếp

### Checkpoint — 02/11/2026
Vừa hoàn thành: BE + app, đã kiểm tinker + simulator tpeLocal. Chưa commit (user tự báo).
Bước tiếp theo: user cho commit/push → hrm-api đẩy develop (+ gop_db) qua worktree tách origin (KHÔNG kèm rbac); TPE_APP develop.
Lưu ý: việc Hoàn thành vẫn chia theo hạn nên meeting đã xong có hạn cũ nằm ở nhóm "Quá hạn" (chưa xử lý, chờ user quyết).

## Task phụ 02/11 — thứ tự menu "Tạo mới" (create_menu_sheet.dart)
- [x] Nhắc việc cá nhân · Nhiệm vụ · Meeting · Phiếu đi công tác (CC) · Phiếu giao việc (CC) · Vấn đề — analyze sạch, simulator đúng thứ tự
- [x] Sửa sheet tràn đáy 2.4px: thêm isScrollControlled: true — simulator hết dải tràn, bấm Vấn đề mở đúng form

## Task phụ 02/11 — nhóm "Quá hạn" xuống cuối (app + web)
- [x] App `my_todo_list_view.dart` `_groups`: overdue cuối — simulator: Hôm nay → Ngày mai → Tuần này → Quá hạn
- [x] Web `TodoMainList.vue` `groupOrder`: overdue cuối — Playwright (Nuxt trỏ API dev) đo top: 243 / 658 / 710 / Quá hạn 762
- [x] e2e `my-todo-grouping.spec.ts` thêm ca "nhóm Quá hạn nằm CUỐI" (chưa chạy — chỉ chạy khi user yêu cầu)

## Task phụ 02/11 — nền màn Đăng nhập + Chọn phân hệ theo Pencil "Wrap 00b · Chọn phân hệ (app)"
- [x] `custom_view/entry_background.dart`: bỏ gradient + 4 vệt sáng, dùng ảnh `assets/images/image.png` (trùng MD5 `images/app-login-bg.png` của design) cover trên `#020B1D`
- [x] Simulator: Chọn phân hệ (tpeLocal + tpeDev) + Đăng nhập (tpeDev, đăng xuất rồi đăng nhập lại thuydt) đều nền sóng xanh

### Checkpoint — 02/11/2026 (đã push)
- TPE_APP develop: 579b08d (Việc của tôi) + 3b57558 (nền màn cửa vào)
- hrm-api: origin/gop_db 86a53d26e · origin/develop c438e8798 (cherry-pick qua worktree, không rbac)
- hrm-client: origin/gop_db 5903edace (Quá hạn xuống cuối)
Bước tiếp theo: deploy hrm-api develop lên dev → kiểm lọc trạng thái trên app tpeDev.

### Checkpoint — 02/11/2026 (kết phiên)
- Simulator 1 + 2 đều chạy tpeDev (API dev-hrm.eteksofts.com): máy 1 namdangit, máy 2 thuydt.
- Còn chờ: deploy hrm-api develop lên dev → kiểm lọc Trạng thái trên tpeDev + chạy lại nhắc giờ họp M1/M2/M3.
- Chờ user quyết: nhóm riêng "Đã kết thúc" cho việc xong/dừng (hiện meeting xong có hạn cũ nằm ở Quá hạn); chạy e2e my-todo-grouping; 4 file menu hrm-client chưa commit (không phải của phiên này); worktree HRM/wt-rsvp.
