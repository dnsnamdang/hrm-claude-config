# GĐ7 Chat — Panel phải "Tệp · Ảnh · Link · Nhiệm vụ" + 2 sửa nhỏ giao diện

> Ngày: 13/11/2026 · Phụ trách @namdangit · Trạng thái: **THIẾT KẾ — chờ user duyệt, CHƯA code**
> Gốc: user 13/11 "Cửa sổ chat thêm panel bên phải như cửa sổ Agent: hiện 3 loại thông tin File, task, link ⇒ mỗi cửa sổ
> hiện 5 đối tượng mới tạo gần nhất ⇒ click xem thêm sẽ mở về tab tương ứng".
> Nguyên tắc chung nhóm: quy mô 1.000–2.000 người + đa nền tảng (README §0).

## 1. Mục đích

Khung chat đang rộng thừa (1094px trên màn 1440). Người dùng muốn **nhìn nhanh tài nguyên của hội thoại** — tệp, ảnh, link
đã gửi và nhiệm vụ mới của nhóm — mà không phải cuộn ngược lịch sử tin. Đồng thời sửa 2 điểm giao diện nhỏ.

## 2. Phạm vi

### 2.1 Sửa nhỏ (làm cùng đợt, chỉ FE `hrm-client`)

| # | Việc | Đã đo (Playwright, 1440×860, conv 99) | Cách sửa |
|---|---|---|---|
| S1 | Nút Đính kèm lệch | nút top 812 vs các nút 816; `.cc__attach` cao 38 do Bootstrap `label{margin-bottom:8px}` trên `<label class="v2-file">`; viền `#cbd5e1`/bo 5px/icon 12.8px khác `.v2-icon-btn` (`#e2e8f0`/8px/14px/màu `#4b5563`); nút Chụp màn hình bị flex co còn 28px | CSS `ChatComposer.vue`: `margin:0` cho label, khoác kiểu giống `.v2-icon-btn--md` (cả hover), `.cc__tools > * { flex-shrink:0 }` |
| S2 | Panel trái hẹp | 288px ⇒ 4 tên bị cắt "…", ô tìm 74px; 320/360 ⇒ 0 tên bị cắt; placeholder cần 226px | **Chờ user chọn** 1) 360px + placeholder "Tìm nhóm, tên, mã NV" (đề xuất) · 2) 400px · 3) kéo giãn + lưu |

### 2.2 Panel phải (GĐ7 chính)

**Mục hiện theo loại hội thoại** (user chốt):

| Mục | Nhóm trao đổi | Chat 1–1 |
|---|---|---|
| Ảnh — lưới thu nhỏ | ✔ | ✔ |
| Tệp (không phải ảnh) | ✔ | ✔ |
| Link | ✔ | ✔ |
| Nhiệm vụ | ✔ chỉ khi nhóm bật tab Nhiệm vụ (`enabled_tabs` có `tasks`) | ✘ bỏ |

Mỗi mục: **5 đối tượng mới nhất** + số tổng (nếu rẻ) + nút "Xem thêm".

**"Xem thêm"** (user chốt):
- **Link**: mở rộng ngay trong panel phải — panel chuyển sang chế độ danh sách đầy đủ của Link (có nút ← quay lại),
  cuộn tải thêm theo con trỏ.
- **Ảnh**: *(quyết định của Claude)* giống Link — lưới đầy đủ trong panel, cuộn tải thêm; bấm ảnh mở `ChatImageViewer` có sẵn.
- **Tệp**: đích đến là **tab File của nhóm (làm tương tự tab Nhiệm vụ)** — user ghi nhận làm SAU. Đợt này: *(quyết định của
  Claude)* tạm mở rộng trong panel giống Link để không có nút chết; khi có tab File thì nhóm trao đổi chuyển sang mở tab,
  chat 1–1 vẫn mở rộng trong panel.
- **Nhiệm vụ**: mở tab Nhiệm vụ có sẵn của nhóm (`panel = 'tasks'`, `?panel=tasks`).

**Hiển thị panel** (user ok đề xuất):
- Luôn hiện khi màn đủ rộng; nút thu gọn/mở ở đầu khung chat. Trạng thái thu gọn **lưu BE theo người dùng** (đồng bộ nhiều
  thiết bị). Màn hẹp (< ~1280px khung trình duyệt) tự thu gọn.
- Kiểu dáng theo cột phải Agent (`components/agent/AgentSidePanel.vue`, class `.agp`: nền `#fcfdfe`, viền `#e5e7eb`, bo 8px,
  thanh cuộn mảnh). Rộng *(quyết định của Claude)* ~300px.
- Chỉ hiện ở panel "Trao đổi" của nhóm (`panel === 'chat'`) và ở chat 1–1 `/assign/messages?c=`; không hiện ở Thành viên /
  Cấu hình / Nhiệm vụ / khung Agent.

**Từng dòng** *(quyết định của Claude, theo dạng có sẵn trong chat)*:
- Ảnh: ô vuông thu nhỏ, lưới 3 cột (5 ảnh + ô "Xem thêm" nếu còn).
- Tệp: icon loại (`fileIcon` trong `utils/chat/chatFormat`) · tên · dung lượng · người gửi · ngày; bấm ⇒ tải/xem như bấm tệp trong tin.
- Link: favicon chung/icon `ri-link` · tên miền + đường dẫn rút gọn · người gửi · ngày; bấm ⇒ mở tab mới. Có nút nhỏ "Tới tin
  nhắn" nhảy tới tin gốc (dùng cơ chế nhảy tin của tìm kiếm tin nhắn đang có) — *quyết định của Claude, bỏ được*.
- Nhiệm vụ: mã · tên · badge trạng thái · hạn; bấm ⇒ mở panel chi tiết nhiệm vụ (TaskPanel) như tab Nhiệm vụ.

## 3. Dữ liệu & BE (`hrm-api`)

### 3.1 Nguồn

- **Tệp + Ảnh**: bảng chung `files` với `table='chat_messages'`, `table_id = chat_messages.id` (index `files(table, table_id)`).
  Phân loại ảnh theo `file_type`/đuôi giống `isImageFile` FE (logic phân loại đặt ở BE để app dùng chung).
- **Link**: hiện chỉ nằm trong `chat_messages.body` ⇒ **bảng mới `chat_message_links`** (id, conversation_id, message_id,
  url, host, created_at; index `(conversation_id, id)`), ghi khi gửi / sửa tin (sửa ⇒ xoá link cũ của tin rồi ghi lại)
  **và khi Chuyển tiếp** — `MessageService::forward()` tạo tin bằng `ChatMessage::create` không qua `send()`
  (`MessageService.php:246-252`, đã kiểm 13/11) ⇒ phải móc ghi link ở cả đây. Tệp chuyển tiếp đã có dòng `files` mới nên không thiếu.
  Không quét body lúc xem (chịu tải). Regex tách URL ở BE khớp regex FE đang làm link bấm được
  `/(https?:\/\/[^\s<]+)/g` (`components/chat/ChatMessageItem.vue:326`).
  - Backfill link cho tin cũ: lệnh artisan chạy lẻ, theo lô 1.000 tin (quyết định của Claude; chạy prod phải hỏi user).
- **Nhiệm vụ**: nhiệm vụ của nhóm theo đúng tập & quyền của tab Nhiệm vụ (bỏ Nháp của người khác — như `my_open_task_count`),
  sắp theo `created_at` giảm dần, lấy 5.

### 3.2 Lọc bắt buộc (giống lịch sử tin người xem đang thấy)

Bỏ tin đã thu hồi (`recalled_at`), tin người xem đã "Xóa phía tôi" (`chat_message_hides`), tin trước
`cleared_before_message_id` của thành viên; chỉ thành viên hội thoại được gọi (`ConversationAccess`). Tin hệ thống không có tệp/link.

### 3.3 API (dùng chung web / mobile / desktop)

- `GET assign/chat/conversations/{id}/side-panel` ⇒ `{ images:{items[5], has_more}, files:{…}, links:{…}, tasks:{…}|null }`
  — 1 request khi mở hội thoại; mỗi mục 1 query có `LIMIT 6` (lấy 6 để biết `has_more`, không đếm tổng — tránh COUNT trên
  hội thoại lớn; *quyết định của Claude*).
- `GET assign/chat/conversations/{id}/resources?kind=images|files|links&before_id=&limit=30` ⇒ phân trang con trỏ cho "Xem thêm".
- Cài đặt thu gọn panel: lưu BE theo người dùng (bảng/cột cài đặt chat sẵn có nếu có, không thì bảng cài đặt người dùng chung —
  builder kiểm chỗ lưu cài đặt GĐ4 âm thanh/thông báo).

### 3.4 Cập nhật trực tiếp

Socket `chat` đã bắn `message.created` / sửa / thu hồi cho thành viên. FE panel tự chèn đầu mục khi tin mới có tệp/ảnh/link
(dữ liệu đã có trong payload tin — không gọi lại API), bỏ khi thu hồi/Xóa phía tôi. **Không thêm sự kiện socket mới.** Nhiệm vụ:
nạp lại mục Nhiệm vụ khi trang nhóm nhận `tasks-changed` đang có.

## 4. Mục tiêu / Không làm / Thất bại nếu

- Mục tiêu: mở hội thoại thấy ngay 5 tệp/ảnh/link/nhiệm vụ mới; "Xem thêm" đúng đích đã chốt; mở hội thoại thêm đúng 1 request.
- Không làm đợt này: **tab File của nhóm** (làm sau, ghi nhận) · tìm kiếm trong panel · ghim tài nguyên · xem trước nội dung
  link (tiêu đề/ảnh OG — cần gọi ra ngoài, để sau).
- Thất bại dù chạy được: panel lộ tệp/link của tin đã thu hồi / đã Xóa phía tôi / trước mốc xoá lịch sử · lộ nhiệm vụ người
  xem không có quyền · mở hội thoại chậm hẳn đi (N query / quét body) · khung chat bị bóp hẹp hơn mức đọc thoải mái trên màn 1366.

## 5. Ràng buộc kỹ thuật

- Nhánh mới tách `origin/gop_db` (2 repo), worktree `wt-nhom-trao-doi`; merge khi user báo.
- Migration `chat_message_links` (+ có thể cài đặt panel) — chạy local phải nêu tên + hỏi theo CLAUDE.md.
- Không chạy e2e tới khi user yêu cầu; xong mỗi lượt mở app cho user check (memory 13/11). Vẫn đo DOM bằng Playwright.
- Sửa `ChatPane` / `ChatShell` ⇒ khi user cho chạy e2e: chạy cả e2e chat + `agent-chat` + `agent-chat-pin` (Agent nhúng trong Tin nhắn).

## 6. Quyết định đã chốt (user 13/11/2026)

| # | Câu | Chốt |
|---|---|---|
| Q1 | "Xem thêm" Link | Mở rộng ngay trong panel phải |
| Q2 | "Xem thêm" Tệp | Đích là tab File của nhóm (như tab Nhiệm vụ) — **làm sau**, ghi nhận |
| Q3 | Chat 1–1 | Chỉ Ảnh + Tệp + Link, bỏ Nhiệm vụ |
| Q4 | Hiện panel | Luôn hiện khi đủ rộng, có nút thu gọn, màn hẹp tự thu gọn |
| Q5 | Ảnh | Tách mục Ảnh riêng, lưới thu nhỏ |
| Q6 | Tập Nhiệm vụ | **Chỉ việc chưa đóng** (cùng tập với `my_open_task_count`), 5 việc mới tạo nhất, bỏ Nháp của người khác |
| Q7 | Cập nhật Nhiệm vụ | Nạp lại mục Nhiệm vụ khi hội thoại nhận tin hệ thống / thẻ nhiệm vụ mới qua socket `chat` có sẵn; không thêm sự kiện socket. Việc người khác sửa mà không sinh tin ⇒ cập nhật khi mở lại hội thoại (chấp nhận) |
| Q8 | Lưu thu gọn panel | **localStorage theo trình duyệt** như GĐ4 (`utils/chat/chatNotifier.js`) — không migration; gom cài đặt chat lên BE sau khi làm app mobile/desktop. (Thay cho §2.2 / §3.3 "lưu BE") |

Quyết định của Claude (user xem lại khi đọc): Ảnh "Xem thêm" mở rộng trong panel · Tệp tạm mở rộng trong panel tới khi có
tab File · không trả số tổng, dùng `has_more` (LIMIT 6) · panel rộng ~300px · nút "Tới tin nhắn" ở dòng Link · backfill link
tin cũ bằng lệnh artisan theo lô · ghi link cả ở luồng Chuyển tiếp.

## 7. Để builder tự quyết

Tên component (gợi ý `components/chat/ChatSidePanel.vue`), cách chia service BE, regex URL cụ thể, vị trí nút thu gọn,
breakpoint chính xác, kiểu skeleton lúc tải.
