# GĐ35 — Tạo nhanh Vấn đề từ tin nhắn trong Nhóm trao đổi

> 18/11/2026 · @namdangit · Trạng thái: THIẾT KẾ (chưa có lệnh code)

## 1. Mục đích

Trong nhóm chat đã có "Tạo nhiệm vụ" từ một tin nhắn (GĐ2 §6.4). User muốn có **"Tạo vấn đề"** y như vậy: thấy một tin
báo lỗi / vướng mắc trong nhóm ⇒ bấm 1 nút ra phiếu Vấn đề, cả nhóm thấy thẻ vấn đề ngay dưới tin gốc và biết tin nào đã
thành vấn đề. Làm **cả web lẫn app mobile** trong cùng đợt (user chọn 18/11).

## 2. Mục tiêu / không làm / không được xảy ra

**Mục tiêu** — ngang hàng "Tạo nhiệm vụ":
1. Nút "Tạo vấn đề" trên tin (web: thanh công cụ tin; app: menu nhấn giữ).
2. Form Vấn đề mở ở chế độ tạo, điền sẵn: Nhóm (khoá), Tên, Mô tả có dòng "— Từ tin nhắn của X lúc hh:mm dd/mm".
3. Lưu xong: BE gửi **thẻ vấn đề** trả lời tin gốc (đứng tên người tạo), tin gốc có **nhãn mã vấn đề**.
4. Panel / màn chi tiết vấn đề có dòng "Tạo từ tin nhắn của … · dd/mm hh:mm", bấm nhảy về tin gốc (như TaskPanel).
5. Thẻ vấn đề tự đổi khi vấn đề đổi trạng thái / người xử lý / hạn (realtime, như thẻ nhiệm vụ GĐ25).
6. Danh sách hội thoại, thanh ghim, banner/push hiện đúng chữ "[Vấn đề <mã>] …" (không phải "[Nhiệm vụ]").

**Không làm đợt này**
- Chèn vấn đề bằng `#` trong ô soạn (hiện `#` chỉ cho nhiệm vụ).
- Tạo vấn đề từ chat 1–1 (nhiệm vụ cũng không có).
- Chép tệp của tin sang vấn đề (nhiệm vụ cũng không chép — chỉ ghi tên tệp vào Mô tả).
- Đồng bộ nút vào nhóm Dự án TKT (nhóm TKT không có tab Vấn đề — GĐ34).

**Không được xảy ra**
- App hiểu nhầm thẻ vấn đề là thẻ nhiệm vụ (bấm mở nhầm nhiệm vụ cùng id). Hiện app coi mọi `card` là nhiệm vụ ⇒ BẮT BUỘC
  sửa app trước khi phát hành app chat lên store (app chat chưa phát hành 18/11 ⇒ chưa máy nào dính).
- Lộ mã / tên vấn đề cho người không còn quyền thấy (thẻ đã xoá ⇒ hiện "đã xoá", như thẻ nhiệm vụ).
- Làm hỏng luồng "Tạo nhiệm vụ" đang chạy.

## 3. Hiện trạng (đã đọc code origin/gop_db 18/11)

| Phần | Nhiệm vụ (đã có) | Vấn đề (hiện tại) |
|---|---|---|
| Nối tin gốc | `tasks.source_message_id` (migration 2026_11_14_000001) | **chưa có cột** |
| Nhận ở API tạo | `TaskStoreRequest` `source_message_id`; `TaskService::store` kiểm tin gốc (`MessageService` dòng ~155: cùng nhóm, không phải tin hệ thống, chưa thu hồi, người tạo gửi được tin) rồi `postSourceCard` | `IssueStoreRequest` có `workspace_id` (GĐ34), chưa có `source_message_id` |
| Tin thẻ | `ChatMessage` type `card`, `attachable_type = 'task'` (`ATTACH_TASK`), `MessageService::postTaskCard` | chưa có loại `issue` |
| Dựng thẻ | `ChatPresenter::taskCard` (deleted / moved), trả `card.type = 'task'` | — |
| Nhãn tin gốc | `created_tasks` (bỏ Nháp) | — |
| Dòng xem trước | `ChatPresenter::preview` + `cardCodes` ⇒ "[Nhiệm vụ <mã>] …" — **chỉ biết task** | — |
| Realtime thẻ | `Task::updated` ⇒ `TaskChatSync` ⇒ `task.updated` | chưa có |
| Web nút | `ChatMessageItem` emit `create-task` khi `canCreateTask`; `ChatPane.createTaskFrom` mở `TaskPanel.create(defaults)` | `IssuePanel.create(defaults)` có sẵn (GĐ34 `IssueGroupListView` dùng: điền nhóm, nhóm GP điền + khoá GP) |
| Web điều kiện | `taskTools` = chat nhóm + tab Nhiệm vụ bật + `can_send` | tab Vấn đề bật: `WorkspaceView.issuesEnabled` (không có ở nhóm TKT) |
| App | `MessageActionsSheet` `createTask` khi `isSpace && tasksEnabled && canSend && live`; `work_task_form_page` gửi `source_message_id`; `ChatCard.type` có parse nhưng bubble / ghim / banner / danh sách luôn ghi "[Nhiệm vụ]" và mở nhiệm vụ | form tạo vấn đề có sẵn (đã thử lưu thật 18/11) |
| Quyền tạo vấn đề trong nhóm | — | Quản lý + Thành viên nhóm (role 1, 2), BE kiểm lại (GĐ34 C1) ≈ `can_send` |

## 4. Cách làm (đã chọn)

**Phương án đã chọn (user, 18/11):** làm đầy đủ như Nhiệm vụ — thẻ + nhãn + dòng nguồn + realtime — trên **cả web và app**.

Phương án đã cân nhắc:
1. **Đầy đủ như Nhiệm vụ** (chọn). Tốn 3 repo + 1 migration, đổi lại người trong nhóm thấy ngay tin nào đã thành vấn đề.
2. Chỉ nút tắt mở form điền sẵn, không thẻ / nhãn / migration — loại vì chat không còn dấu vết tin nào đã thành vấn đề.
3. App chỉ hiển thị đúng thẻ, nút tạo trên app để đợt sau — loại, user muốn web và app đồng nhất.

**Hướng kỹ thuật (Claude chọn — tổng quát hoá luồng thẻ, không nhân bản):** loại thẻ là `attachable_type`; mọi chỗ đang
ngầm hiểu "card = task" đổi sang xét `card.type`. Thêm `ATTACH_ISSUE = 'issue'`.

## 5. Thiết kế

### 5.1 BE (hrm-api)

1. **Migration** `issues.source_message_id` (unsigned bigint, nullable, index) — chỉ thêm cột, không đụng dữ liệu cũ.
2. **API tạo vấn đề** nhận `source_message_id` (nullable integer). Khi có:
   - Bắt buộc có `workspace_id` và tin gốc phải: thuộc hội thoại của **đúng nhóm đó**, không phải tin hệ thống / tin thẻ,
     chưa thu hồi, người tạo gửi được tin; nhóm bật tab Vấn đề. Sai ⇒ 422 ở `source_message_id` (dùng chung hàm kiểm của
     nhiệm vụ, tách ra nếu đang gắn riêng cho task).
   - Kiểm tin gốc TRƯỚC khi tạo; `Issue::create` + thẻ chung 1 transaction, thông báo sau đó (xem C7): ghi `source_message_id`, gửi tin thẻ (`type = card`, `attachable_type = 'issue'`,
     `reply_to_id` = tin gốc, đứng tên người tạo), phát `message.created` (thẻ) + `message.updated` (tin gốc, để nhãn hiện
     ngay). Không ghi `notifications` (như thẻ nhiệm vụ).
   - Sửa vấn đề KHÔNG đổi được `source_message_id`.
3. **Dựng thẻ vấn đề** (`ChatPresenter`): 1 truy vấn `whereIn` cho cả trang như thẻ nhiệm vụ. Trường:
   `type: 'issue'`, `id`, `code` (= `issue_code`), `title`, `status_text`, `status_color` (từ `Issue::STATUS_DATA`),
   `assignee {id, name}` (người phụ trách), `priority`/`priority_text`/`priority_color` (`PRIORITY_DATA`), `due_date`,
   `due_time`, `is_overdue`, `due_state_text`/`due_state_color` (luật C6), `deleted`. Không có `progress_pct`, `moved` luôn `false` (vấn đề chỉ gán nhóm lúc tạo — GĐ34).
   Vấn đề đã xoá ⇒ thẻ `deleted: true`, không lộ mã / tên.
4. **Nhãn tin gốc**: thêm `created_issues` (mảng `{id, code}`) cạnh `created_tasks`, 1 truy vấn theo
   `issues.source_message_id`, bỏ vấn đề đã xoá. Tin thu hồi ⇒ rỗng (như `created_tasks`).
5. **Dòng xem trước / push / banner**: `preview` + `cardCodes` xét `attachable_type` ⇒ "[Vấn đề <mã>] …" cho thẻ vấn đề.
   Rà mọi chỗ còn ghi cứng "[Nhiệm vụ]" cho tin `card` (preview, nội dung push FCM, thông báo web) và đổi theo loại.
6. **Realtime thẻ**: `Issue::updated` đổi trường hiện trên thẻ (trạng thái, tên, người phụ trách, hạn, ưu tiên) ⇒ phát
   `issue.updated` `{issue_id, card}` vào hội thoại của nhóm (sau commit, nuốt lỗi + log như `TaskChatSync`). Chỉ phát khi
   vấn đề có `workspace_id`. Đóng nhóm (huỷ hàng loạt không qua model) cũng phát — xem C8.
7. **Chi tiết vấn đề** trả `source_message_id` + `source_message {id, workspace_id, conversation_id, sender_name,
   created_at, can_open}` giống `DetailTaskResource::sourceMessagePayload`.

### 5.2 Web (hrm-client)

1. `ChatMessageItem`: thêm nút "Tạo vấn đề" (icon riêng, tooltip) cạnh "Tạo nhiệm vụ", hiện khi cha cho `canCreateIssue`
   và tin chưa thu hồi. Emit `create-issue`.
2. `ChatPane`: prop mới `issuesWorkspaceId` (WorkspaceView truyền khi `issuesEnabled`); `issueTools` = chat nhóm +
   `issuesWorkspaceId` + `can_send`. `createIssueFrom(m)` mở `IssuePanel.create(...)` với cùng cách điền như
   `createTaskFrom` (Tên = 80 ký tự đầu cắt theo từ, tin chỉ có tệp ⇒ tên tệp; Mô tả = toàn văn + "Tệp: …" + dòng nguồn),
   nhóm khoá; nhóm GP ⇒ điền + khoá GP như `IssueGroupListView` đang làm. Gửi `source_message_id`.
   `ChatPane` của chat nhóm cần gắn thêm 1 `IssuePanel` (hiện chỉ có `TaskPanel`).
3. **Thẻ vấn đề** trong luồng tin: component thẻ chọn theo `card.type` (task giữ nguyên `TaskCard`; issue ⇒ thẻ vấn đề cùng
   khuôn: mã · tên · trạng thái màu · người phụ trách · hạn · ưu tiên). Bấm thẻ ⇒ `IssuePanel.view`.
4. **Nhãn tin gốc**: dưới bong bóng hiện cả `created_tasks` ("📋 NV-…") và `created_issues` (icon vấn đề + mã), mỗi loại
   1 cụm, bấm mở panel tương ứng.
5. Nghe `issue.updated` ⇒ thay `card` của tin thẻ cùng id (như `onTaskUpdated`); tab Vấn đề của nhóm đang mở tự nạp lại
   (gom 800ms như GĐ27).
6. `IssuePanel`: dòng "Tạo từ tin nhắn của … · dd/mm hh:mm" (khi `source_message.can_open`), bấm ⇒ mở nhóm và nhảy tới tin
   — y như TaskPanel.
7. Thanh ghim / trích dẫn trả lời: tin thẻ vấn đề hiện "[Vấn đề] <tên>".

### 5.3 App (TPE_APP)

1. `ChatCard` đã có `type`; mọi chỗ vẽ / ghi chữ / mở thẻ (`message_bubble`, `pin_bar`, `message_actions_sheet` chữ sao chép,
   `chat_banner_overlay`, `chat_list_bloc` xem trước, cập nhật thẻ theo id ở `chat_room_bloc`) xét `type`:
   `issue` ⇒ khuôn thẻ vấn đề + mở màn chi tiết vấn đề; loại lạ ⇒ thẻ trung tính không bấm được (phòng loại thẻ sau này).
   Cập nhật thẻ realtime khớp CẢ `type` lẫn `id` (task 5 và issue 5 không đè nhau).
2. `ChatMessage` parse `created_issues`; bong bóng hiện nhãn như web.
3. Hub nghe `issue.updated`.
4. Menu nhấn giữ: `MessageAction.createIssue` khi `isSpace && issuesEnabled && canSend && live` ⇒ form tạo vấn đề điền sẵn
   (nhóm khoá, tên, mô tả) + gửi `source_message_id`, theo khuôn `work_task_form_page` (`_sourceSent` chống gửi lại).
5. Chi tiết vấn đề trên app: dòng "Tạo từ tin nhắn…" bấm mở phòng chat tại tin (nếu màn chi tiết task app đang có dòng này;
   không có thì bỏ — ngang hàng app task).

### 5.4 Quy mô / tải

- Không truy vấn trong vòng lặp: thẻ vấn đề, `created_issues` mỗi loại 1 `whereIn` mỗi trang tin.
- `issue.updated` chỉ bắn vào 1 hội thoại của nhóm (không theo người) ⇒ tải như `task.updated`.

## 6. Kiểm

- PHPUnit: tạo vấn đề có `source_message_id` (đúng ⇒ thẻ + nhãn; sai nhóm / tin hệ thống / thu hồi / người Xem / nhóm tắt tab
  Vấn đề / nhóm đã đóng ⇒ 422); thẻ deleted; preview "[Vấn đề …]"; `issue.updated` chỉ khi đổi trường thẻ; luồng nhiệm vụ
  cũ giữ nguyên (chạy lại bộ Workspace + Issue + Task).
- e2e web (`workspace-issues.spec` thêm ca) + chạy lại chat-core, workspace-tasks, chat-drawer; ca có quyền / không quyền
  (người Xem không thấy nút).
- Playwright đo DOM: nút, thẻ, nhãn, dòng nguồn.
- App: test đơn vị (parse `type`, actions sheet có/không `createIssue`, cập nhật thẻ khớp type+id) + chạy máy ảo tpeLocal.

## 7. Để người làm tự quyết

Icon nút / nhãn vấn đề, tên component thẻ, tách hàm kiểm tin gốc dùng chung, tên migration, thứ tự task trong plan.

## 8. Claude tự chốt (user soát)

- C1. Hướng tổng quát hoá theo `attachable_type` thay vì nhân bản luồng thẻ.
- C2. Thẻ vấn đề không có tiến độ; `moved` luôn false.
- C3. Nhãn tin gốc tách 2 cụm (nhiệm vụ / vấn đề), không gộp chung một dòng mã.
- C4. App gặp loại thẻ lạ ⇒ thẻ trung tính không bấm được.
- C5. Vấn đề có Nháp? — Issue không có trạng thái Nháp (STATUS_DATA 8 trạng thái, không Nháp) ⇒ không cần lọc như task.
- C6 (sau soát). Hạn trên thẻ theo đúng luật tab Vấn đề `WorkspaceIssueItemResource` (dòng 53–88): `due_date` + `due_time`,
  quá hạn tính tới giờ (không giờ ⇒ 23:59:59), trả thêm `due_time`, `due_state_text`, `due_state_color`. Không dùng cột
  `deadline` cũ. ⇒ thẻ và tab Vấn đề không lệch chữ "Quá hạn".
- C7 (sau soát). `IssueService::store` hiện KHÔNG có transaction và gửi thông báo (trưởng phòng xử lý, người phụ trách) ngay sau
  `Issue::create`. Cách làm: (1) kiểm tin gốc TRƯỚC khi tạo (sai ⇒ 422, chưa có tác dụng phụ nào); (2) bọc riêng
  `Issue::create` + gửi thẻ trong 1 transaction; (3) thông báo giữ nguyên vị trí, chạy SAU transaction đó. Vấn đề không có
  `source_message_id` chạy y như cũ ⇒ luồng tạo vấn đề ngoài chat không đổi hành vi (vẫn chạy lại bộ test Issue).
- C8 (sau soát). Đóng nhóm ⇒ `WorkspaceIssueCanceller` huỷ vấn đề bằng `DB::table('issues')->update` (không qua model ⇒
  `Issue::updated` không chạy). Thêm: sau khi huỷ, phát `issue.updated` cho các vấn đề vừa huỷ CÓ thẻ trong hội thoại nhóm
  (1 truy vấn lấy thẻ, dựng card hàng loạt) ⇒ thẻ đổi sang "Đã đóng" ngay. Thẻ nhiệm vụ khi đóng nhóm: chưa kiểm, ngoài phạm vi
  — ghi vào danh sách ngoài luồng nếu có lệch.
