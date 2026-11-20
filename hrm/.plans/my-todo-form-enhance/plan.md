# Plan — Cải tiến form Nhắc việc cá nhân

**Phụ trách:** @khoipv | **Ngày:** 2026-07-17
**Spec:** `docs/superpowers/specs/2026-07-17-my-todo-form-enhance-design.md`
**Plan chi tiết (step-by-step):** `docs/superpowers/plans/2026-07-17-my-todo-form-enhance.md`
**Tóm tắt:** `.plans/my-todo-form-enhance/design.md`

## Tasks

### Phase 1 — BE
- [x] Task 1: `UpdatePersonalTodoRequest` — `list_id` nullable → required + message (đồng nhất Store) — php -l + tinker `LIST_ID_REQUIRED_OK` — review clean

### Phase 2 — FE
- [x] Task 2: Giờ hạn → `vue2-datepicker type=time format=HH:mm value-type=HH:mm` (TodoFormModal.vue) — parse OK — review clean
- [x] Task 3: Danh sách bắt buộc — label*, placeholder "-- Chọn danh sách --", `listState`, invalid-feedback, chặn `onSave` (TodoFormModal.vue) — parse OK — review clean
- [x] Task 4: Nút "Lưu và tiếp tục" (secondary, chỉ Tạo mới) — `onSave(continueAfter)` + `resetForm()` + `saving` chống double-submit (TodoFormModal.vue) + `onSaveTodo({payload,continueAfter})` + `ref="todoModal"` (index.vue) — parse OK — review clean
- [x] Fix 2 Minor (final review): guard re-entry `onSaveTodo` + refocus Tiêu đề sau `resetForm` — parse OK

### Verify (AC) — chờ user chạy browser
- [x] AC1 (code): sao đỏ Danh sách + giờ 24h — ⏳ verify hiển thị "14:00" trên browser
- [x] AC2: bỏ trống Danh sách → chặn (FE inline + BE required)
- [x] AC3 (code): "Lưu và tiếp tục" → toast + lưu DB + modal mở + reset trống + focus Tiêu đề — ⏳ verify UI
- [x] AC4: "Lưu" → lưu + đóng modal
- [x] AC5: màn Sửa đồng nhất (Update required + giờ 24h)

## Checkpoint
### Checkpoint — 2026-07-17 (2)
Vừa hoàn thành: CODE DONE Task 1-4 + fix 2 Minor (subagent-driven, Opus). Từng task review clean (spec ✅ / quality Approved). Final whole-branch review: READY, không Critical/Important. Verify: php -l + tinker (BE), parse-check vue-template-compiler + @babel/parser (FE) — tất cả pass. KHÔNG commit (theo rule).
Đang làm dở: —
Bước tiếp theo: user bật FE dev server (3000) verify browser AC1 (giờ hiển thị 24h "14:00" theo locale) + AC3 (reset field trống + focus Tiêu đề sau "Lưu và tiếp tục"). Có thể nhờ Claude drive Playwright nếu server chạy.
Blocked:

### Checkpoint — 2026-07-17 (1)
Vừa hoàn thành: Brainstorming + Spec + Plan chi tiết (brainstorming → writing-plans).
Bước tiếp theo: bắt đầu Task 1 (BE UpdatePersonalTodoRequest).

## Nhắc việc thường lưu Bắt đầu vào start_* (2026-11-20) — @cuong61n
Nghiệp vụ: form tạo/sửa nhắc việc THƯỜNG chỉ có "Ngày/Giờ bắt đầu"; khi tick "Báo lịch làm việc lãnh đạo" mới có thêm cặp "Ngày/Giờ kết thúc". Nhắc việc thường lưu ở start_date/start_time (due_* = NULL); lịch lãnh đạo giữ Bắt đầu = start_*, Kết thúc = due_*.
- [x] 2026-11-20 FE `TodoFormModal.vue`: hàng Bắt đầu luôn hiện, hàng Kết thúc chỉ khi tick lãnh đạo; payload thường gửi start_*, due_* = null; nạp form sửa theo loại (thường: due_* chỉ là bản sao nên không đổ vào ô Kết thúc).
- [x] 2026-11-20 BE ghi: `MyTodoService::timeColumns()` (create / copies nhiều người / update); client cũ (app) chỉ gửi due_* ⇒ coi là Bắt đầu. Lịch lãnh đạo mất quyền sửa (không gửi cờ) giữ nguyên Bắt đầu.
- [x] 2026-11-20 BE đọc: mốc chính qua `PersonalTodo::effDateSql/effTimeSql` + accessor `effective_date/effective_time` (lãnh đạo = due_*, thường = start_*) ở normalizeItem (due_date/due_time trong payload = mốc chính nên web/app đọc như cũ), WorkCalendarService (SQL + payload), WorkItemPeriod, WorkReminderService (nhắc trước hạn/quá hạn), PersonalContactService (next_due, sắp xếp), thông báo giao nhắc việc ("Hạn:" → "Bắt đầu:").
- [x] 2026-11-20 Migration `2026_11_26_000001_move_personal_todo_due_to_start` (chuyển due_* → start_* cho nhắc việc gốc không phải lịch lãnh đạo; chạy local: 23 dòng).
- [x] 2026-11-20 Câu lỗi lịch lãnh đạo đổi "hạn" → "kết thúc" (Store/UpdatePersonalTodoRequest) + cập nhật 4 test fixture/assert; thêm test nhắc việc thường lưu start_* và client cũ gửi due_*.
- Kiểm: phpunit LeaderSchedule 59 + MyTodo 9 + PersonalContact 35 + Unit 35 qua; Playwright 3002: tạo nhắc việc thường 21/11 09:30 → DB start_*=21/11 09:30, due_* NULL, hiện nhóm "Ngày mai", mở sửa nạp lại đúng (đã xoá bản ghi test).
- Trạng thái: sửa trên worktree gop_db-api / gop_db-client, chưa commit. ⚠️ Deploy phải chạy migration TRƯỚC khi dùng FE mới.
- [ ] Chưa rà: TPE_APP (còn gửi due_*, BE đã ánh xạ; nhãn "Hạn" trong app chưa đổi), các báo cáo/export ngoài module MyTodo nếu có đọc personal_todos.due_*.
- [x] 2026-11-20 Hiển thị lại sau phản hồi: (1) web `PersonalTodoResource` trả due_* = mốc chính (màn danh sách theo loại không mất ngày); (2) lịch lãnh đạo trả `start_at` → thẻ app/web hiện "bắt đầu → kết thúc" 1 dòng (WorkItemPeriod trải đủ ngày trên lịch); (3) nhắc tự động: chữ thông báo "Nhắc việc, bắt đầu …" / "Lịch lãnh đạo, kết thúc …", nhãn cấu hình "trước giờ bắt đầu".
- [x] 2026-11-20 Gộp ngày + giờ thành 1 ô: nhắc việc thường = "Thời gian nhắc việc"; lịch lãnh đạo = "Thời gian bắt đầu" + "Thời gian kết thúc". Web `TodoFormModal.vue` (date-picker type=datetime, computed startAt/dueAt ghép-tách start_*/due_*); app `personal_todo_form_page.dart` + `leader_schedule_section.dart` (showAppDateTimePicker). BE không đổi (vẫn nhận ngày/giờ tách). Bật/tắt công tắc lãnh đạo chuyển giá trị qua lại Bắt đầu ↔ Nhắc việc.
- [x] 2026-11-20 App TPE_APP (iPhone 15, tpeLocal API 8003): form thường lưu start_*, lịch lãnh đạo (bắt buộc, lỗi đỏ đúng ô, xác nhận báo cả công ty), thẻ danh sách, chi tiết, sửa nạp lại, cảnh báo chưa lưu — đã bấm thật; nhãn "Hạn" → "Bắt đầu"/"Kết thúc" ở thẻ + danh bạ. Đã xoá dữ liệu test.
- ⚠️ Đổi ô gộp = giờ luôn đi kèm ngày (trước đây giờ tuỳ chọn); dữ liệu cũ chỉ có ngày hiện 00:00 nhưng không bị ghi đè nếu không sửa ô.
- [x] 2026-11-20 Thẻ nhắc việc thường (app) hiện giờ như cũ, bỏ chữ "Hạn"/"Bắt đầu" ("17:00 hôm nay 20/11", "21/11 09:00"); có khoảng thời gian (lịch lãnh đạo) hiện "20/11 08:00–23:00 · Đang diễn ra…" / "26/11 → 27/11". Local: tạo 5 nhắc việc mẫu "[MẪU] …" cho namdangit (id 13, vốn đã có quyền lãnh đạo) để xem UI — xoá bằng `DELETE FROM personal_todos WHERE title LIKE '[MẪU]%'`.
- [x] 2026-11-20 TEST LẠI TOÀN BỘ (web + app + BE): BE phpunit LeaderSchedule 64 + MyTodo 9 + PersonalContact 35 qua (thêm test: sửa/đổi giờ, client cũ chỉ gửi due_*, đổi loại thường↔lãnh đạo, kết thúc<bắt đầu, hiển thị danh sách/lịch/nhóm, nhắc cho nhiều người). Web (Playwright :3002): tạo thường, lỗi trống + kết thúc<bắt đầu, tạo lãnh đạo, sửa thường, sửa lãnh đạo + bỏ tick, tab lịch. App (iPhone 15): tạo thường, lãnh đạo (lỗi trống, lỗi kết thúc<bắt đầu, lưu), sửa thường, sửa lãnh đạo + tắt công tắc, thẻ/chi tiết/tab lịch. Đã xoá dữ liệu QA.
- [x] 2026-11-20 2 LỖI BẮT ĐƯỢC KHI TEST LẠI, ĐÃ SỬA: (1) nhắc việc giao cho NGƯỜI KHÁC (bản sao) mất ngày giờ vì chưa ghi start_* → thêm timeColumns cho bản sao; (2) tab lịch hiện lịch lãnh đạo 1 ngày chỉ "17:00" thay vì "08:00 – 17:00" → WorkItemPeriod dùng start_time thật.
- [x] 2026-11-20 Khoảng thời gian nhiều ngày: (1) việc có start_at (lịch lãnh đạo, phiếu giao việc/công tác) đã bắt đầu mà chưa kết thúc → cũng hiện ở nhóm "Hôm nay" (web `TodoMainList.vue` + thẻ thống kê `index.vue`, app `my_todo_list_view.dart`), vẫn giữ ở nhóm theo ngày kết thúc; (2) tab lịch app bỏ "ngày x/y": "19/11 08:00 → 22/11 17:00" hoặc "Cả ngày · 19/11 → 22/11"; (3) thẻ danh sách web + app ghi cả giờ khi lịch lãnh đạo nhiều ngày có giờ kết thúc. Đã xem thật trên app + web. Local: 2 mẫu "[MẪU] Lịch lãnh đạo — nhiều ngày chứa hôm nay".
- [x] 2026-11-20 Màu dòng khoảng thời gian (user chốt): XÁM cả dòng (kể cả chữ "Đang diễn ra"), chỉ ĐỎ khi quá hạn — bỏ màu xanh `#2563EB` ở app (`work_item_card.dart`, cả lịch lãnh đạo lẫn phiếu giao việc/công tác) và web (`TodoItem.vue` bỏ `.ongoing-text` xanh, thêm `.overdue-meta` đỏ). Đã đo màu thật: web xám `rgb(142,153,164)` / đỏ `rgb(226,92,92)`, app xem trực tiếp. Local có thêm mẫu "[MẪU] Lịch lãnh đạo — quá hạn".
