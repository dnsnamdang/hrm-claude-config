# GĐ16 — Tạo nhanh nhắc việc từ tin nhắn chat · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (native). Steps dùng `- [ ]`.

**Goal:** Rê chuột vào tin chat ⇒ nút "Tạo nhắc việc" ⇒ mở form nhắc việc có sẵn, điền trước tiêu đề + mô tả từ tin ⇒ lưu thành nhắc việc cá nhân.

**Architecture:** Chỉ hrm-client. `ChatMessageItem` phát `create-reminder` ⇒ `ChatPane` (có mặt ở trang chat, ngăn trượt, trang nhóm) gắn 1 `TodoFormModal`, tải loại nhắc việc lazy, gọi API sẵn có `POST assign/my-todo/todos`. `TodoFormModal` thêm 2 prop điền sẵn (chỉ khi TẠO).

**Tech Stack:** Nuxt 2 / Vue 2, bootstrap-vue, store `apiGet` / `apiPostMethod`.

**Spec:** `.plans/agent-chat/chat/gd16-nhac-viec-tu-tin/design.md` (user duyệt 15/11/2026).

**Nhánh / nơi làm:** worktree `wt-nhom-trao-doi/hrm-client`, nhánh MỚI `gop_db-chat-nhac-viec` tách từ `origin/gop_db` — ⚠️ nhánh `gop_db-chat-active-row` (GĐ15) chưa merge: hỏi user tách từ GĐ15 hay từ origin/gop_db trước khi tạo. Không BE, không migration. Code chỉ bắt đầu khi user trả lời "làm" kèm phạm vi.

## Global Constraints
- Nút: `V2BaseIconButton size="sm"`, icon `ri-alarm-line`, tooltip `v-b-tooltip.hover.top="'Tạo nhắc việc'"`, đứng NGAY SAU nút "Tạo nhiệm vụ", testid `chat-msg-reminder-${m.id}`.
- Hiện khi: tin không thu hồi (`!m.recalled`), không phải tin hệ thống (tin hệ thống đã render nhánh riêng `cm-sys`), KHÔNG phụ thuộc `canSend` / tab Nhiệm vụ / loại hội thoại.
- Tiêu đề điền sẵn: toàn văn tin gộp khoảng trắng, tối đa **200** ký tự cắt ở ranh giới từ; tin không chữ ⇒ tên các tệp nối `, `; tin chỉ ảnh không tên ⇒ `[Ảnh]`; sticker ⇒ `[Sticker]`.
- Mô tả điền sẵn: `Từ tin của <người gửi> · <tiêu đề hội thoại> · <dd/mm/yyyy HH:mm>` + `\n` + toàn văn tin (+ `\nTệp: a, b` nếu có tệp).
- Loại nhắc việc mặc định = `loaiMacDinhId` sẵn có của form; ngày/giờ hạn trống.
- Lưu thành công: toast `Đã tạo nhắc việc` (success), đóng form, KHÔNG ghi gì vào hội thoại. 422 xử lý y như `pages/assign/my-todo/index.vue` `onSaveTodo` (setServerErrors → toast câu máy chủ).
- `TodoFormModal` là component dùng chung (my-todo, danh bạ, Agent): thêm prop KHÔNG đổi hành vi khi không truyền.

## Review Focus
1. Mở form trước khi tải xong loại nhắc việc ⇒ `list_id` null, bấm Lưu báo đỏ "Loại nhắc việc" — phải tải `lists` XONG rồi mới bật `show` (watcher `show` đọc `loaiMacDinhId` lúc mở). Kiểm ở Task 3.
2. Bấm "Lưu và tạo tiếp" (`continueAfter`) ⇒ `resetForm()` — form tạo tiếp phải TRỐNG (không lặp lại tiêu đề tin cũ). Kiểm ở Task 1 + 3.
3. Tin rất dài (> 500 ký tự BE) ⇒ tiêu đề đã cắt 200, mô tả toàn văn (`description` nullable|string, không giới hạn) — không 422. Kiểm ở Task 3.
4. Người chỉ có quyền xem nhóm (`can_send=false`) vẫn thấy nút và tạo được. Kiểm ở Task 3.
5. Mở form từ tin A, đóng, mở tin B ⇒ form mang nội dung tin B (preset đổi giữa 2 lần mở). Kiểm ở Task 3.

---

### Task 1: `TodoFormModal` nhận tiêu đề / mô tả điền sẵn

**Files:**
- Modify: `pages/assign/my-todo/components/TodoFormModal.vue` (props ~264–282; watcher `show` nhánh `else` ~378–381)

**Interfaces:**
- Produces: props `presetTitle: { type: String, default: '' }`, `presetDescription: { type: String, default: '' }` — chỉ áp ở nhánh TẠO của watcher `show` (`form.title = presetTitle`, `form.description = presetDescription`). `resetForm()` giữ nguyên (tạo tiếp ⇒ form trống).

- [x] Step 1: thêm 2 prop + gán trong nhánh `else` của watcher `show` (sau `this.form = formTrong()`).
- [x] Step 2: kiểm không hồi quy — Playwright mở `/assign/my-todo` (:3080), bấm tạo nhắc việc ⇒ tiêu đề + mô tả rỗng, loại = mặc định; sửa 1 nhắc việc ⇒ form mang đúng dữ liệu cũ.

### Task 2: dựng nội dung điền sẵn từ tin

**Files:**
- Modify: `utils/chat/chatFormat.js` — thêm `titleFromText(text, max)` (chuyển thân `taskTitleFrom` của ChatPane sang, tham số `max`) và `reminderPrefill(message, conversationTitle) -> { title, description }`.
- Modify: `components/chat/ChatPane.vue:207-219` — bỏ hàm cục bộ `taskTitleFrom`, `createTaskFrom` dùng `titleFromText(body, 80)` (giữ nguyên hành vi nhiệm vụ).

**Interfaces:**
- Produces: `titleFromText(text: string, max: number): string`; `reminderPrefill(m, convTitle): {title: string, description: string}` — đọc `m.body`, `m.files[].name`, `m.type` (`sticker`, ảnh), `m.sender.fullname`, `m.created_at` (dùng `parseDateTime`), theo Global Constraints.

- [x] Step 1: viết 2 hàm.
- [x] Step 2: kiểm bằng node (Node 20) import thử module với 5 mẫu: chữ ngắn · chữ 600 ký tự · chỉ tệp · chỉ ảnh · sticker ⇒ tiêu đề / mô tả đúng quy tắc; `titleFromText(x, 80)` cho kết quả như `taskTitleFrom` cũ.

### Task 3: nút trên tin + form trong ChatPane

**Files:**
- Modify: `components/chat/ChatMessageItem.vue` (~186–193 sau nút Tạo nhiệm vụ) — nút theo Global Constraints, `@click="$emit('create-reminder')"`.
- Modify: `components/chat/ChatPane.vue` — gắn `<TodoFormModal ref="reminderModal" :show="reminder.show" :lists="reminderLists" :preset-title="reminder.title" :preset-description="reminder.description" @save="saveReminder" @list-added="loadReminderLists" @close="reminder.show = false" />` cạnh `<ForwardModal>`; `@create-reminder="createReminderFrom(row.m)"` trên `ChatMessageItem`.

**Interfaces:**
- Consumes: Task 1 props, Task 2 `reminderPrefill`.
- Produces: methods `createReminderFrom(m)` (đóng toolbar, `await loadReminderLists()` nếu chưa có, set preset từ `reminderPrefill(m, detail.title)`, rồi `reminder.show = true`), `loadReminderLists()` (`apiGet 'assign/my-todo/lists'`), `saveReminder({ payload, continueAfter })` (copy luồng `onSaveTodo` nhánh TẠO + xử lý 422; không reload danh sách my-todo).

- [x] Step 1: nút + emit.
- [x] Step 2: modal + 3 method.
- [x] Step 3: Playwright (:3080, NV 13, nhóm thử `[e2e] Nhắc việc …` tạo qua API, xoá sau) đo: nút có ở tin chữ / tin tệp, KHÔNG có ở tin thu hồi; bấm ⇒ form tiêu đề + mô tả đúng, loại = mặc định; đặt ngày hạn ⇒ Lưu ⇒ POST 200, toast, có bản ghi `personal_todos` mới của NV 13 (đọc API `assign/my-todo`); 5 mục Review Focus; ngăn trượt + trang nhóm đều chạy. Xoá nhắc việc thử + nhóm thử.
- [x] Step 4: mở trang cho user xem. e2e chỉ khi user yêu cầu.

## Checkpoint — 15/11/2026 17:30
Vừa hoàn thành: Task 1–3 (nhánh `gop_db-chat-nhac-viec` tách từ origin/gop_db 960d04154; GĐ15 đã commit e9dbcb6cf ở `gop_db-chat-active-row`, chưa push). User chọn tách từ origin/gop_db + "commit rồi làm tiếp".
Kiểm Playwright (:3080, NV 13 + NV 24, nhóm thử `[e2e] Nhắc việc GĐ16` đã xoá): form điền đúng tiêu đề + mô tả, loại = "Việc cá nhân"; mở tin A rồi B ⇒ nội dung B (198 ký tự, mô tả 848); "Lưu và tiếp tục" ⇒ POST 200 + form trống; "Tạo nhắc việc" ⇒ 200, đóng form, toast; trang nhóm đầy đủ chạy; my-todo form tạo vẫn trống; NV 24 chỉ xem nhóm 93 vẫn thấy nút (không có nút Trả lời); tin thu hồi 21533 không có nút. DB: 2 personal_todos đúng user 13 list 2 — đã xoá. Task 2 kiểm bằng node: 5 mẫu tin + titleFromText(x,80) trùng taskTitleFrom cũ.
Ngoài luồng: console `[Vue warn] computed "errors" already defined in data` ở CreateIssueModal.vue (file không đụng, có sẵn).
Reviewer độc lập: không lỗi chặn. Đã sửa điểm 1 (bấm tin A rồi B lúc loại nhắc việc đang tải ⇒ form mang tin bấm SAU CÙNG — cờ `reminderSeq`; đo bằng chặn API lists 1,5s ⇒ form = M2, 1 modal; chạy lại toàn bộ ca: đạt). Điểm 2 (tải loại lỗi ⇒ form mở với ô Loại trống, interceptor đã báo lỗi 500/403) — để nguyên.
Hỏi user: lỗi CÓ SẴN ở TodoFormModal.resetForm() — "Lưu và tiếp tục" đặt list_id = null (không về loại mặc định) ⇒ lần lưu sau báo thiếu Loại; trang my-todo bị y hệt. Hàm dùng chung ⇒ chưa sửa.
User 15/11: "Tuyệt đối không làm ảnh hưởng luồng nhắc việc trên app/web" ⇒ KHÔNG sửa resetForm (để nguyên lỗi có sẵn, ghi ngoài luồng). Bằng chứng không ảnh hưởng: (1) hrm-api không đổi gì ⇒ app chỉ gọi API, không bị ảnh hưởng; (2) diff TodoFormModal = 2 prop mặc định '' + 2 dòng gán ở nhánh TẠO, `formTrong()` vốn title/description '' ⇒ không truyền prop thì giống hệt; nhánh SỬA không đổi; (3) chạy thật màn Việc của tôi :3080: form tạo trống, loại "Việc cá nhân", POST payload đủ khoá như cũ (title, description, list_id, due_*, sub_items, is_leader_schedule, start_*, leader_show_title), DB có 1 việc + 1 bước (đã xoá).
e2e my-todo UI (18 spec) chạy tạm trên :3080/:8080: 10 đạt · 8 đỏ · 39 không chạy — đỏ do spec cũ tìm nút "Tạo nhắc việc cá nhân" (origin/gop_db đã đổi chữ thành "Tạo nhắc việc" ở 92ca3a93c), fetch sang :8000 (Failed to fetch), dữ liệu nhóm Đã kết thúc ⇒ môi trường/spec cũ, KHÔNG phải do diff (diff không đổi chữ nút, không đổi luồng tải). Chưa so được với bản gốc vì không đổi nhánh worktree đang chạy.
Ngoài luồng: (a) resetForm "Lưu và tiếp tục" để list_id null (có sẵn) · (b) màn Việc của tôi bấm Tạo trước khi tải xong loại ⇒ ô Loại trống (có sẵn) · (c) spec my-todo dùng chữ nút cũ.
Đã commit 15/11: client b9de02317 (nhánh gop_db-chat-nhac-viec, chưa push). GĐ15: e9dbcb6cf (gop_db-chat-active-row, chưa push).
Bước tiếp theo: user báo merge 2 nhánh lên gop_db + deploy.
ĐÃ DEPLOY TPE 15/11 tối: prod client 87a115c9a (gồm GĐ15+16+17), api 3fefb0545.
Blocked:
