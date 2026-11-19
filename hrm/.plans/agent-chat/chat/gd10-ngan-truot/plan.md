# GĐ10 — Chat / Agent mở dạng NGĂN TRƯỢT trên trang đang làm (PA 2) · PLAN

Lý do: icon Chat / Agent trên topbar là link sang `/assign/messages` · `/agent` (khai trong menu Giao việc) ⇒ người đang ở
phân hệ khác bị đổi menu trái sang Giao việc (resolveSubsystem theo URL + ghi đè sessionStorage active_subsystem_key).
User 14/11: "làm PA2 luôn" (đánh giá PA2 trong hội thoại). Phạm vi: CHỈ hrm-client, nhánh `gop_db-chat-drawer` (tách
origin/gop_db 6a459ecd4), không BE / migration.

## Thiết kế (Claude chốt khi làm — rulings ghi cuối)
- Ở trang KHÔNG phải chat (`/assign/messages`, `/assign/workspaces/*`) và không phải `/agent*`: bấm icon Chat / Agent ⇒ mở ngăn
  phải (top 60px dưới topbar, rộng min(1100px, 100vw − 120px)), nền mờ phía sau; bấm lại icon / ✕ / nền mờ / Esc ⇒ đóng.
  Ctrl/⌘ + bấm icon ⇒ mở tab mới như link thường. Ở trang chat / agent: icon giữ hành vi link cũ.
- Trong ngăn: ConversationList (thu gọn 68px khi ngăn < 980px) + ChatPane (có đầu khung cả chat nhóm, ẩn panel Tài nguyên)
  hoặc AgentWorkspace nhúng (không ghi query lên URL trang). Đầu ngăn: tiêu đề · "Mở toàn màn hình" · ✕.
- Toast tin mới ở trang không phải chat ⇒ mở ngăn đúng hội thoại.
- Trạng thái ngăn ở store `chat.drawer` (mở / view chat|agent / hội thoại / người nhận 1–1) — đóng mở lại về hội thoại cũ.
- Đổi trang (link trong ngăn: meeting, nhóm, Mở toàn màn hình) ⇒ đóng ngăn.

## Tasks
- [x] D1 store chat: state.drawer + mutations openDrawer / closeDrawer
- [x] D2 ConversationList: prop agentActive (override), ChatPane: props hideSide + routeSync, AgentWorkspace: queryKey rỗng ⇒ không đọc/ghi URL
- [x] D3 ChatDrawer.vue (portal body, nền mờ, Esc, header, list + pane/agent/empty, chọn người, tạo nhóm)
- [x] D4 BasicSubsystem: icon Chat / Agent mở ngăn ngoài trang chat; toast mở ngăn; gắn ChatDrawer (lazy)
- [x] D5 Playwright đo: menu trái không đổi, form không mất, z-index popup trên ngăn, Esc, màn hẹp
- [x] D6 e2e `chat-drawer.spec.ts` + chạy lại bộ chat/agent

## Kết quả đo (Playwright MCP, 14/11)
- /human/banks (phân hệ khác): bấm Chat ⇒ ngăn 1100px ở 1507px (x=407, top 60, z 1035, gắn <body>); URL giữ `/human/banks`,
  sessionStorage active_subsystem_key giữ `master-data`; ô tìm trang giữ "OCB" sau mở/đóng; Esc · nền mờ · bấm lại icon đều đóng;
  mở lại về hội thoại cũ (962). Nhóm mở trong ngăn: đầu khung có "Mở nhóm", không cột Tài nguyên, ô soạn đáy 741 < 773.
- Popup "Tin nhắn mới" từ ngăn: z 1050, elementFromPoint giữa popup = popup.
- LỖI tái hiện + sửa: Esc khi đang mở popup đóng LUÔN ngăn (b-modal gỡ `show` trước khi listener bubble kiểm) ⇒ nghe pha capture.
- 1100px: Agent trong ngăn có cột Phân quyền riêng ⇒ cột giữa ~320px (thẻ gợi ý vỡ dòng) ⇒ mở Agent thì cột hội thoại thu 68px
  (đo lại: list 68, Agent 912).
- E2E mới `chat-drawer.spec.ts` 5/5. `agent-chat.spec.ts` ca "có quyền use" sửa: bấm icon ngoài trang chat ⇒ ngăn Agent.

## Rulings
- Ngăn KHÔNG mở ở trang Tin nhắn / nhóm / Agent — icon giữ link cũ (tránh 2 khung chat cùng nhận socket).
- Chat nhóm trong ngăn KHÔNG có "#" chèn nhiệm vụ / Tạo nhiệm vụ từ tin (danh sách hội thoại không mang enabled_tabs của nhóm) —
  dùng đầy đủ qua "Mở nhóm". Sai thì: BE trả enabled_tabs trong conversation list.
- Đổi trang bất kỳ (link trong ngăn) ⇒ đóng ngăn. Tạo nhóm mới từ ngăn ⇒ sang trang nhóm.
- Ctrl/⌘/Shift/chuột giữa trên icon ⇒ mở tab mới như link.

## Đi kèm (14/11)
- Tin của mình bên PHẢI kiểu bong bóng (user bỏ D2 GĐ8): `components/chat/ChatMessageItem.vue` — khối CSS cuối file + `placeActions` nhánh `is_mine`. E2E `chat-giao-dien.spec.ts` dòng 106–116 (kiểm canh trái) CHƯA sửa, sẽ fail.

## Kết quả e2e cuối (14/11)
- `chat-drawer` 5/5 (mới) · topbar-shortcuts 3/3 · chat-core 8/8 · chat-thong-bao-emoji 10/10 (E4 sửa: bấm toast ở trang khác ⇒ ngăn) ·
  chat-giao-dien 5/5 · chat-toolbar-zalo 8/8 · chat-panel-phai 6/6 · chat-bo-sung 6/6 · chat-gd2-polish 7/7 · workspace-tasks 12/12 ·
  workspace-meetings 5/5 · agent-chat 19/19 (ca "có quyền use" sửa: icon ngoài trang chat ⇒ ngăn Agent; :8080 AGENT_FAKE=1 tạm, đã trả về thường) ·
  agent-chat-pin 6/6 (lần 3 — lần 1 lỗi mạng `ERR_NETWORK_IO_SUSPENDED` khi Back, lần 2 trang đầu tải quá 90s lúc máy thiếu RAM; không do code).
- CHƯA commit — nhánh `gop_db-chat-drawer` (hrm-client).

## Đợt 2 (14/11 trưa — user: bỏ menu Agent + Tin nhắn ở phân hệ Công việc; ngăn dùng ĐỦ tab + chức năng như trang; ngăn đẩy tới sát sidebar thu nhỏ)
- [x] E1 `menu-sidebar.js`: bỏ mục "TPE SMART AGENT" (/agent) + "Tin nhắn" (/assign/messages). Key Cài đặt phân hệ cũ vẫn được đọc
      (agentAccess, BasicSubsystem.chatEnabled) nhưng KHÔNG còn hiện ở màn Cài đặt phân hệ để bật/tắt.
- [x] E2 Tách thân trang nhóm ⇒ `components/chat/workspace/WorkspaceView.vue` (props workspaceId · requestedPanel · assignee; emits
      panel · open-tasks · leave · direct · loaded). Trang `/assign/workspaces/{id}` còn vỏ nối URL. MembersPanel phát `open-tasks`;
      TaskGroupListView nhận prop `initialAssignee`.
- [x] E3 Ngăn: chat nhóm = WorkspaceView (đủ tab Nhiệm vụ / Meeting / Thành viên / ⚙, `#`, Tạo nhiệm vụ, panel Tài nguyên); chat 1–1 có
      panel Tài nguyên; store `chat.drawer.panel/assignee`; "Mở toàn màn hình" sang đúng mục (?panel=).
- [x] E4 Hình học: bỏ nền mờ; ngăn từ mép phải tới mép trái `.content-page` (= sidebar thu gọn 58px); sidebar đang bung ⇒ tự thu khi mở,
      đóng ⇒ trả lại; body.chat-drawer-open nâng rail + panel menu hub (1036–1038) lên trên ngăn (1035).
- Đo MCP 1440: ngăn x=58 w=1377; sidebar bung 220 ⇒ mở ngăn condensed ⇒ đóng trả null; nhóm trong ngăn: header + tab tasks/meetings/
  members + ⚙, Tài nguyên có, tab Nhiệm vụ ⇒ cột hội thoại 68; URL trang giữ `/human/banks`; menu Công việc không còn 2 mục.
- E2E chat-drawer 5/5 (viết lại N1/N2/N5; N3 chờ popup hiện xong mới đo — lần đầu đo lúc popup đang hiện dần).
- ⚠ Phát hiện: phiên KHÁC đã sửa `components/chat/ChatMessageItem.vue` lúc 09:52 (đổi tin sang kiểu BONG BÓNG — "user bỏ D2") trên CÙNG
  worktree / nhánh này. Không phải việc GĐ10 — khi commit KHÔNG gộp file đó vào commit GĐ10.
- E2E đợt 2: chat-drawer 5/5 · chat-core 8/8 (sửa: rail KHÔNG còn mục Tin nhắn) · workspace-tasks 12/12 · workspace-meetings 5/5 ·
  chat-gd2-polish 7/7 · chat-panel-phai 6/6 · chat-bo-sung 6/6 · chat-thong-bao-emoji 10/10 · topbar-shortcuts 3/3 · agent-chat-pin 6/6 ·
  chat-giao-dien G2–G5 4/4. FAIL do thay đổi kiểu BONG BÓNG của phiên khác (không phải GĐ10): chat-giao-dien G1 (tin dạng luồng),
  chat-toolbar-zalo Z1 (vị trí thanh thao tác) — phiên đó cần sửa 2 ca này.

## Đợt 3 + push (14/11)
- User: giữ kiểu BONG BÓNG (quyết ở phiên khác, gộp vào phiên này) ⇒ sửa e2e G1 (bong bóng: mình phải nền #dff3ec, người khác trái #f1f4f8,
  tin mình ẩn avatar) + Z1 (giữa thanh thao tác nằm trong chiều cao bong bóng).
- Bỏ nút "Mở toàn màn hình" (ngăn đã sát sidebar; trang đầy đủ đổi menu sang Giao việc). Nhóm mới tạo trong ngăn mở luôn trong ngăn.
- Đổi tên "Tin nhắn" ⇒ "Không gian trao đổi công việc" (tiêu đề ngăn, tooltip icon topbar, tiêu đề trang /assign/messages).
- E2E: chat-drawer 5/5 · chat-giao-dien 5/5 · chat-toolbar-zalo 8/8 · topbar-shortcuts 3/3.
- Push: 1 commit client, rebase lên origin/gop_db (5 commit mới của người khác, không trùng file) ⇒ `f0a0e778b`. Chưa deploy.
