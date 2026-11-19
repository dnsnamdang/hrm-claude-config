# Ghim TPE SMART AGENT trong Tin nhắn — đặc tả (chốt 12/11/2026)

Nguồn: mockup `phan-he-cong-viec/gd0-mockup/screens/33-tro-ly-erp.html` + ghi chú `sb2.js` (11/11 "mọi màn có cột Hội thoại
đều có dòng TPE SMART AGENT ghim trên cùng khối Đã ghim"). Bàn giao phiên GĐ2 (12/11): việc ghim chuyển sang phiên Agent.
Nhánh: `gop_db-tpe-smart-agent` (đã merge `gop_db-nhom-trao-doi` 12/11 — api 3621a8c66, client 601e76370).

## Chốt 5 câu (user 12/11)
1. **Đúng mockup 33, giữ /agent**: tách logic trang `/agent` (pages/agent/index.vue ~900 dòng: hội thoại, hỏi, socket/poll,
   thẻ chọn, mở panel Task/Issue/Meeting/nhắc việc/phiếu, in, xin quyền) thành component dùng chung; `/agent` và màn Tin nhắn
   cùng dùng. Lý do giữ /agent: Tin nhắn đang ẩn trên prod (key Cài đặt phân hệ), Agent có thể lên trước.
2. **Dòng ghim ở cả 2 màn có cột Hội thoại** (`/assign/messages`, `/assign/workspaces/{id}`): ở Tin nhắn mở Agent ngay trong
   khung; ở màn nhóm ⇒ chuyển `/assign/messages?agent=1` (link chia sẻ / Back được).
3. **Lịch sử trên đầu khung Agent**: nút "Hội thoại mới" + "Lịch sử" (thả xuống hội thoại gần đây, chọn để mở lại). Cột trái
   chat không đổi.
4. **Điều kiện hiện**: quyền "Dùng TPE SMART AGENT" (`assign.tpe_agent.use`) VÀ key Cài đặt phân hệ `assign::TPE SMART AGENT`
   không bị tắt. Mặc định ẩn (fail-closed); `?agent=1` khi không đủ điều kiện ⇒ không mở (về màn trống Tin nhắn).
5. **"@TPE SMART AGENT" trong chat nhóm (AI1b) để NGOÀI đợt này** — Agent trả lời theo quyền người hỏi, đăng vào nhóm sẽ lộ
   dữ liệu cho thành viên không có quyền. Việc sau, cần spec riêng (tin chỉ người hỏi thấy / chỉ dữ liệu mọi thành viên xem được).

## Tự chốt theo mockup (điểm thuần UI)
- Dòng ghim: avatar robot `TpeAgentMascot` head, tên "TPE SMART AGENT" + nhãn AI, dòng phụ = tiêu đề hội thoại Agent gần nhất
  (= câu hỏi đầu của hội thoại đó; lấy từ `GET agent/conversations` có sẵn, không thêm API) hoặc "Hỏi về nhiệm vụ, lịch họp, tiến độ…", không badge chưa đọc, không menu ⋯ (không bỏ ghim / tắt thông báo được).
  Nằm TRÊN khối "Đã ghim" (khối hiện cả khi người dùng chưa ghim hội thoại nào). Cột thu gọn 68px ⇒ chỉ avatar.
- Khung Agent trong Tin nhắn: đầu khung 64px như ChatPane (avatar + tên + "Trả lời theo quyền của người hỏi"), cột phải
  "Phân quyền của Agent" có nút ẩn/hiện như /agent.
- Không đổi BE (API `v1/agent/*` có sẵn).

## Ngoài luồng (ghi lại, không sửa đợt này)
- Nút robot topbar (`BasicSubsystem.vue` `canUseAgent`) chỉ xét quyền, không xét key `assign::TPE SMART AGENT` ⇒ tắt Agent ở
  Cài đặt phân hệ vẫn còn nút robot.
- Socket :8895 (worktree chat) chạy server.js chưa gộp nhánh `agent` ⇒ gói agent tới client nối :8895 thành `notification`.

## Đã code (12/11/2026, hrm-client nhánh gop_db-tpe-smart-agent, CHƯA commit)
- MỚI `components/agent/AgentWorkspace.vue` (toàn bộ logic cũ của pages/agent/index.vue; prop `embedded`, `queryKey` c|ac;
  chế độ nhúng: nút Hội thoại mới + Lịch sử thả xuống trên đầu khung, cột phải có viền trái, khung phẳng).
- MỚI `utils/agentAccess.js` (`canUseAgentInChat`: mã `assign.tpe_agent.use` + key `assign::TPE SMART AGENT` / phân hệ
  `assign` không tắt, theo getter `effectiveMenuHiddenKeys`).
- `pages/agent/index.vue` còn vỏ kiểm quyền + 404 như cũ. `ConversationList.vue` dòng ghim `chat-agent-pin` (emit
  `open-agent`). `ChatShell.vue` `openAgent` ⇒ `/assign/messages?agent=1`. `pages/assign/messages/index.vue` `?agent=1` ⇒
  `AgentWorkspace embedded query-key="ac"`, không đủ điều kiện ⇒ bỏ `agent`/`ac` khỏi URL.
- **Thêm ngoài danh sách file đã báo**: `components/agent/AgentChat.vue` — 1 `<slot name="actions">` ở đầu khung + `display:flex`
  cho cụm nút phải (để đặt nút Hội thoại mới / Lịch sử, không dựng đầu khung thứ 2).
- Kiểm: Playwright MCP 1440×900 (dòng ghim y=180 h=66; khung Agent 1094×840 lấp khung chat, đầu 64, cột phải 320, trang
  không cuộn; Lịch sử 320×300 trong màn hình, nằm trên cùng; hỏi trong khung 6.6 s qua socket :8896 step→delta→done; màn nhóm
  ⇒ /assign/messages?agent=1, Back về nhóm; thu gọn 68px avatar giữa; NV 1345 không dòng ghim, URL bỏ ?agent, 0 request
  agent; tắt key ⇒ ẩn). e2e MỚI `HRM/e2e/tests/agent/agent-chat-pin.spec.ts` 6/6.
- Hồi quy (12/11, user chọn 1): agent-chat + agent-stats 30/30 (AGENT_FAKE=1); chat-core + workspace-tasks 20/20 (queue
  database, jobs = 0). Chi tiết ở plan.md.
