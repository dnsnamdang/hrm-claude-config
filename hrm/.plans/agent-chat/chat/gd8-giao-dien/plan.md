# GĐ8 Chat — Giao diện mới Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (hoặc subagent-driven-development). Checkbox `- [ ]`.

**Goal:** đổi giao diện Chat theo `mockup-v2.html` (kiểu tin A dạng luồng, thanh lọc F2, 1 dải tab chủ đề ở đầu nhóm) — giữ bố cục,
giữ hành vi, không migration.

**Architecture:** gần như toàn FE `hrm-client` (restyle + 2 component nhỏ mới cho Chat); BE chỉ thêm `sender_role` vào payload tin
(ChatPresenter, 1 query cho cả trang). **Giữ nguyên class / testid mà e2e đang bám** — chỉ đổi cách vẽ.

**Tech Stack:** Nuxt 2 / Vue 2, SCSS scoped, V2Base*; Laravel 8 + PHPUnit; Playwright e2e (Node 20).

**Spec:** `design.md` (cùng thư mục, mục 2 = quyết định D1–D11) + `mockup-v2.html` (số đo / màu lấy từ đây).

## Global Constraints

- Nhánh mới `gop_db-chat-giao-dien` tách `origin/gop_db` (api + client), worktree `wt-nhom-trao-doi`. Code chỉ khi user cho phép rõ ràng.
- KHÔNG sửa component dùng chung (`V2BaseSegmented`, `V2BaseMiniTab`, `V2BaseIconButton`…): phần riêng của Chat làm component trong `components/chat/`.
- GIỮ class `.cm`, `.cm--mine`, `.cm__av`, `.cm__bubble`, `.cm__mention`, `.cr`, `.cl-agent` và testid `chat-msg-*`, `chat-msg-more-*`,
  `ws-panel-chat`, `ws-panel-members`, `ws-panel-settings`, `ws-tool-tasks`, `ws-search`, `ws-title`, `chat-agent-pin`, `chat-new-direct`, `chat-new-group`.
- Màu: teal `#1abc9c` (đậm `#149a86`, nền `#f2fbf8`), navy `#14417e`, chữ `#0f172a` / phụ `#64748b`, viền `#e5e7eb`, hover `#f6f8fb`.
- Avatar: người tròn; nhóm vuông bo = `round(size × 0.28)` px. Avatar tin giữ **32px** (e2e chat-bo-sung B1 đo 32 × 32).
- Badge trạng thái việc vẫn `V2BaseBadge :color="status_color"` (BE trả màu).
- Không chạy e2e khi user chưa yêu cầu; xong mỗi task FE đo DOM bằng Playwright + `open` app cho user check.
- Giữ hành vi cũ: ở tab chủ đề cột hội thoại vẫn tự thu gọn (`ChatShell :force-collapsed="panel !== 'chat'"`) — mockup vẽ mở là minh hoạ.
- API local chạy `PHP_CLI_SERVER_WORKERS=4` khi chạy e2e (memory php-s-mot-luong-lam-e2e-fail-gia).

## Review Focus

1. Tin của mình chuyển sang canh trái: nút ⋮ / thanh rê / trích dẫn / sửa / thu hồi / "Xóa phía tôi" vẫn bấm được và đúng vị trí (G5 đo DOM + e2e cũ).
2. Nhóm tắt tab Nhiệm vụ ⇒ không còn tab Nhiệm vụ, `?panel=tasks` cũ vẫn tự về chat (logic `staleTasksQuery` giữ nguyên) (G7).
3. Vai trò Xem / nhóm đã đóng: tab Thành viên và ⚙ vẫn vào được như nút Thành viên / Cấu hình cũ (G7 + e2e chat-core "Đóng nhóm").
4. Dải "Tin chưa đọc" không nhảy khi tin mới tới lúc đang xem (đặt theo mốc đọc lúc MỞ hội thoại) và không hiện khi không có tin chưa đọc (G6).
5. Ctrl K không cướp phím khi đang gõ trong ô khác ngoài trang chat, và gỡ listener khi rời trang (G3).

---

### Task G1: BE — `sender_role` trong payload tin

**Files:** Modify `hrm-api/Modules/Assign/Services/Chat/ChatPresenter.php` (`messages()` :32) · Test `hrm-api/Modules/Assign/Tests/Feature/Workspace/ChatGiaoDienTest.php` (khung theo `ChatSidePanelTest.php`)

**Interfaces — Produces:** mỗi tin có `sender_role: int|null` = `workspace_members.role` của người gửi trong nhóm của hội thoại
(1 Quản lý · 2 Thành viên · 3 Xem); `null` với chat 1–1, tin hệ thống, người không còn trong nhóm. Lấy 1 query `whereIn` cho cả trang.

- [ ] Test hỏng: `test_sender_role_in_group_messages` (A tạo nhóm = Quản lý, B thành viên; danh sách tin ⇒ tin A `sender_role` 1, tin B 2) · `test_sender_role_null_in_direct`.
- [ ] Chạy ⇒ FAIL. Code. Chạy ⇒ PASS; chạy lại `ChatApiTest`, `ChatForwardTest`, `ChatSidePanelTest`.

### Task G2: Avatar nhóm vuông bo

**Files:** Modify `hrm-client/components/chat/ChatAvatar.vue` (prop + CSS `.chat-av`, `.chat-av-wrap`, `.chat-av--group` :90-125) · `ConversationRow.vue:12` · `pages/assign/workspaces/_id/index.vue:11`

**Interfaces — Produces:** prop `shape: 'circle' | 'square'` (mặc định `'circle'`); `square` ⇒ bo `Math.round(size * 0.28)`px cho cả ảnh ghép thành viên.
Hội thoại `type === 'space'` dùng `shape="square"` ở dòng danh sách và đầu nhóm.

- [ ] Code. Playwright: đo `border-radius` avatar nhóm 44px = `12px`, người = `50%`.

### Task G3: Cột hội thoại — đầu cột, thanh lọc chip F2, Ctrl K, thẻ Agent, dòng đang mở

**Files:** Create `hrm-client/components/chat/ChatFilterChips.vue` · Modify `ConversationList.vue` (đầu cột :5-31, CSS `.cl-agent*`, `.cl__block-title`) · `ConversationRow.vue` (CSS `.cr--active`, `.cr--unread`, số chưa đọc)

**Interfaces:** `ChatFilterChips` props `value: string`, `options: [{value, label, icon, count}]` · emit `input`. Icon: Tất cả `ri-inbox-line` · Chưa đọc `ri-mail-unread-line` · Nhóm `ri-team-line` · Cá nhân `ri-user-3-line`; count chỉ hiện ở Chưa đọc (chip đỏ `#ef4444`). Chip chọn: nền `#14417e`, chữ trắng, icon `#9fd8ff`; chip thường viền `#e2e8f0`, cao 28px, bo 14px.

- [ ] Ô tìm: nền `#eef2f6`, không viền, bo 8px, cao 32px, gợi ý `Ctrl K` (Mac `⌘ K` — xét `navigator.platform`) ở cuối ô. Vẫn `V2BaseInput` (bọc class riêng), placeholder giữ "Tìm nhóm, tên, mã NV".
- [ ] Thay 2 nút "Tin nhắn mới" / "Tạo nhóm" bằng 1 nút **"+ Mới"** navy mở menu 2 mục (copy cách mở menu của `V2BaseRowActions` đang dùng ở `cl__notify-menu`); 2 mục giữ testid `chat-new-direct`, `chat-new-group`.
- [ ] `Ctrl/⌘ + K`: listener `keydown` trên `window` gắn ở `mounted`, gỡ ở `beforeDestroy`; `preventDefault` + focus ô tìm; thu gọn cột thì mở cột trước.
- [ ] Thẻ ghim Agent: nền `radial-gradient(80% 140% at 100% 0%, rgba(53,210,223,.45), transparent 60%), linear-gradient(120deg, #0e2f5f, #1a5aa0)`, chữ trắng, bo 12px, bóng `0 6px 16px rgba(20,65,126,.25)`; đang mở thêm viền `#35d2df`.
- [ ] Dòng đang mở: nền trắng, viền `0 0 0 1px #e5e7eb`, vạch teal 4px bên trái; số chưa đọc nền teal; tiêu đề khối có icon (Đã ghim `ri-pushpin-2-line`, còn lại `ri-chat-3-line` "Gần đây").
- [ ] Playwright: 4 chip, chip chọn nền rgb(20,65,126); Ctrl K ⇒ `document.activeElement` là ô tìm; gõ Ctrl K trong ô soạn tin vẫn focus ô tìm (chỉ trang chat có listener).

### Task G4: Ô soạn 1 khối

**Files:** Modify `hrm-client/components/chat/ChatComposer.vue` (template `.cc__input-wrap` / `.cc__bar` + CSS)

- [ ] Khối viền `#dbe2ea` bo 12px chứa ô chữ (không viền riêng) + hàng công cụ; nút công cụ trơn (ghost, không viền — giữ `V2BaseIconButton`, thêm class bỏ viền trong scoped CSS); nút Gửi teal đặc + ký hiệu ↵.
- [ ] Dòng nhắc dưới khối (11px `#94a3b8`): "Enter gửi · Shift + Enter xuống dòng · @ nhắc tên" + "· # chèn nhiệm vụ" chỉ khi có `taskWorkspaceId`. Không có gợi ý `/` (D8).
- [ ] Giữ mọi testid ô soạn (`chat-composer-input`, `chat-send`, `chat-capture`, `chat-emoji-toggle`, `chat-insert-task`…). Playwright: nút công cụ cùng hàng, cách đều, ô chữ không còn viền riêng.

### Task G5: Tin dạng luồng (kiểu A)

**Files:** Modify `hrm-client/components/chat/ChatMessageItem.vue` (template :14-90 + CSS) · `ChatPane.vue` (truyền `isSpace`)

**Interfaces — Consumes:** `m.sender_role` (G1). Prop mới `isSpace: Boolean` từ ChatPane.

- [ ] Mọi tin canh trái, kể cả tin mình. Tin đầu cụm: avatar 32px + dòng đầu `tên · [Quản lý] · giờ`; tin trong cụm thụt theo avatar. Tên mình màu teal `#149a86`. Nhãn "Quản lý" (nền `#f2fbf8`, chữ `#149a86`, 10.5px) chỉ khi `isSpace && m.sender_role === 1` (D9).
- [ ] `.cm__bubble` giữ class nhưng **không nền / không bóng / không bo**; tin rê ⇒ nền dòng `#fafbfc`; thanh thao tác nổi góc phải dòng (giữ testid `chat-msg-more-*`).
- [ ] Tệp: thẻ viền `#e5e7eb` bo 10px, icon theo loại; ảnh bo 10px; thẻ nhiệm vụ (`TaskCard`) viền trái 3px `#2563eb`; trích dẫn trả lời giữ, viền trái teal; cảm xúc chip bo 11px (chip của mình viền `#9fe3cf`); `@nhắc` nền `#eef4fc` chữ `#1a5aa0`.
- [ ] Tin hệ thống, sticker, tin thu hồi giữ hành vi, chỉ chỉnh khoảng cách.
- [ ] Playwright: tin mình `left` ≈ tin người khác; avatar tin mình hiện ở đầu cụm; `.cm__bubble` `background-color` rgba(0,0,0,0); nhãn "Quản lý" đúng người; ⋮ của tin mình bấm được.

### Task G6: Dải ngày + "Tin chưa đọc" trong ChatPane

**Files:** Modify `hrm-client/components/chat/ChatPane.vue` (computed dựng dòng — nơi tạo `row.kind === 'day'`, template :84)

**Interfaces:** chốt `unreadFromId` = id tin đầu tiên **của người khác** có `id > detail.last_read_message_id` **lúc mở hội thoại** (không đổi khi tin mới tới / khi markRead); thêm `row.kind === 'unread'` trước tin đó; testid `chat-unread-divider`.

- [ ] Dải ngày: viên viền `#e5e7eb` giữa đường kẻ `#eef1f5`. Dải "Tin chưa đọc": chữ đỏ in hoa 11px + kẻ `#fca5a5`.
- [ ] Không hiện khi không có tin chưa đọc lúc mở. Playwright: B gửi 2 tin ⇒ A mở ⇒ dải nằm ngay trên tin đầu của B; A gửi thêm ⇒ dải không di chuyển.

### Task G7: Đầu nhóm — 1 dải tab chủ đề + về chat

**Files:** Create `hrm-client/components/chat/workspace/WorkspaceTopicTabs.vue` · Modify `pages/assign/workspaces/_id/index.vue` (header :10-50, `panelOptions`, `toolTabs` :146-180)

**Interfaces:** `WorkspaceTopicTabs` props `active: string|null`, `tabs: [{key, label, icon, color, count, testid}]` · emit `select(key)`.
Tabs: `tasks` (chỉ khi `tasksEnabled`, `my_open_task_count`, icon `ri-task-line` `#2563eb`, testid `ws-tool-tasks`) · `members` (`member_count`, `ri-team-line` `#0ea5e9`, testid `ws-panel-members`). Meeting / Issue KHÔNG có (D6).

- [ ] Bỏ `V2BaseSegmented` Trao đổi / Thành viên / Cấu hình và `V2BaseMiniTab` cũ. ⚙ = `V2BaseIconButton` testid `ws-panel-settings` ⇒ `panel = 'settings'`. Tìm tin (`ws-search`) chỉ hiện khi `panel === 'chat'`.
- [ ] Vùng avatar + tên (`ws-title`) là nút về chat: `panel = 'chat'`, testid `ws-panel-chat`; hover nền `#f6f8fb`.
- [ ] `panel !== 'chat'` ⇒ nút **"← Trò chuyện"** trước tên (nền `#f2fbf8`, chữ `#149a86`, viền `#c8eee2`), số = `unread_count` của hội thoại nhóm trong store chat (`chat/byId`), testid `ws-back-chat`.
- [ ] Giữ nguyên: dòng phụ dưới tên, thanh "nhóm đã đóng", `staleTasksQuery`, query `?panel=`. Dải tab: nền `#f3f5f8` bo 10px, tab chọn nền trắng + bóng nhẹ, số ở tab chọn nền teal.
- [ ] Playwright: nhóm tắt Nhiệm vụ ⇒ chỉ 1 tab; bấm Nhiệm vụ ⇒ có `ws-back-chat`; bấm tên ⇒ về chat; vai trò Xem vẫn vào Thành viên + ⚙.

### Task G8: Panel phải + đầu 1–1 tinh chỉnh, e2e

**Files:** Modify `ChatSidePanel.vue` (CSS: nền `#fbfcfd`, ảnh bo 10px, tiêu đề mục `#94a3b8`) · `ChatPane.vue` (`.cp__head` 1–1: tên đậm 15px, dòng phụ phòng · mã — không thêm ⓘ, D11) · e2e `e2e/tests/assign/chat-giao-dien.spec.ts` (mới) + sửa ca cũ bám bố cục cũ

- [ ] Ca e2e mới (có quyền + không quyền): chip lọc Chưa đọc lọc đúng · Ctrl K focus ô tìm · nhãn "Quản lý" chỉ ở quản lý · dải "Tin chưa đọc" · đầu nhóm: tab / ⚙ / về chat bằng tên + `ws-back-chat` · vai trò Xem không có tab Nhiệm vụ khi nhóm tắt.
- [ ] **Chỉ khi user yêu cầu chạy e2e** (memory chat-task-nho-khong-e2e-mo-app-cho-user) — chạy TOÀN BỘ: chat-panel-phai, chat-giao-dien, chat-core, chat-bo-sung, chat-gd2-polish, chat-thong-bao-emoji, chat-toolbar-zalo, workspace-tasks, agent-chat-pin, agent-chat (API 4 worker; đọc dòng tổng kết — serial "did not run" ≠ passed). Sửa ca cũ chỉ khi đổi do thiết kế mới (ghi lại từng ca sửa trong ledger).
- [ ] Cập nhật README §1/§3, STATUS, memory agent-chat-trang-thai.

## Ledger (executing-plans tại chỗ, KHÔNG commit)
- 13/11 tối user: "Làm" + "Phiên này cho phép tự chạy e2e theo đề xuất của bạn, tôi đi nghỉ". Nhánh `gop_db-chat-giao-dien` (api + client) tách origin/gop_db.
- Task G1: complete — ChatGiaoDienTest 2/2 · ChatApiTest 10/10 · ChatForwardTest 7/7 · ChatSidePanelTest 20/20 · ChatRealtimeTest 3/3.
- Task G2+G3: complete — Playwright 1440: chip 28px, chip chọn rgb(20,65,126), 4 chip vừa 335px kể cả '99+' (đã thu đệm 7px + flex chia đều — lần đầu tràn 7px); avatar nhóm bo 12px / người 50%; dòng mở nền trắng + vạch teal; ô tìm nền rgb(238,242,246); Ctrl/⌘K focus ô tìm; thẻ Agent gradient navy. Ruling: nút '+ Mới' tự dựng menu nhỏ trong ConversationList (V2BaseRowActions không có trigger tuỳ biến) — giữ testid chat-new-direct/chat-new-group trên 2 mục menu — sai thì đổi sang component dropdown khác.
- Task G4: complete — Playwright nhóm 1612: khối 1px rgb(219,226,234) bo 12px, ô chữ viền 0, 5 nút công cụ cùng top 790, bước 32px, viền trong suốt; nút Gửi trong khối; dòng nhắc 'Enter gửi | Shift + Enter xuống dòng | @ nhắc tên | # chèn nhiệm vụ'.
- Task G5+G6: complete — Playwright nhóm 1612: tin mình + người khác cùng left 480; tin mình có avatar 32px, tên rgb(20,154,134); nhãn Quản lý đúng NV 13 (DB: 13 role 1, 34 role 2); .cm__bubble nền trong suốt, pad 0; nền khung #fff; dải 'Tin chưa đọc' rgb(239,68,68) ngay trên tin đầu chưa đọc của NV 34, chèn tin mới ⇒ không dịch; thanh thao tác tin mình top -14 trong dòng, có ⋮. Sửa lỗi build: Sass không hiểu min(760px,100%) ⇒ max-width 760px. Dữ liệu thử: 4 tin của NV 34 trong nhóm 1612 (conv 962).
- Task G7: complete — Playwright nhóm 1612: chat ⇒ tab 'Nhiệm vụ 0' · 'Thành viên 2', không còn segmented/mini-tab cũ, không nút về; bấm Nhiệm vụ ⇒ ?panel=tasks + ws-back-chat + tab sáng; bấm tên (ws-panel-chat) ⇒ chat; ⚙ (ws-panel-settings) ⇒ ?panel=settings, gear teal; Thành viên ⇒ ?panel=members sáng; ws-back-chat ⇒ về chat; đầu nhóm không tràn. Ruling: tab Thành viên đếm member_count (mockup có số) — sai thì bỏ số.
- Task G8: tinh chỉnh panel phải (nền #fbfcfd, ảnh bo 10, tiêu đề mục #94a3b8) + đầu 1–1 (tên 700, dòng phụ #64748b); e2e mới `chat-giao-dien.spec.ts` 4/4 (G1 dải chưa đọc + luồng + nhãn Quản lý · G2 chip + Ctrl K · G3 đầu nhóm · G4 không quyền).
- Ruling: ô tìm thu đệm phải 38px / trái 6px để placeholder "Tìm nhóm, tên, mã NV" (119px) vừa ô (124px) cạnh nhãn ⌘ K — sai thì rút placeholder.
- E2E lượt 1 (API 4 worker + AGENT_FAKE=1, --timeout=120000): chat-giao-dien 4/4 · chat-panel-phai 6/6 · chat-core 8/8 · chat-bo-sung 6/6 · chat-gd2-polish 7/7 · chat-thong-bao-emoji 10/10 · workspace-tasks 12/12 · agent-chat-pin 6/6 · agent-chat 19/19 · chat-toolbar-zalo Z1 FAIL (đo thanh "cạnh bong bóng" — hành vi cũ đổi có chủ đích) + 7 did not run.

### Final review (opus) — 0 Critical · 3 Important · 6 Minor; đã tự kiểm lại trong code
- Final: fixed #1 router.replace trùng URL reject NavigationDuplicated (Nuxt chỉ vá push) — setter `panel` chặn `v === this.panel` + `.catch`; Playwright: bấm tên ở chat, ⚙ 2 lần ⇒ 0 unhandledrejection.
- Final: fixed #2 nút 👍 tràn ngang — tái hiện: vùng 702px, scrollWidth 712 khi rê tin dài ⇒ neo 👍 theo dòng (`.cm__bubble` static, `.cm__like` right 12 / bottom 2) ⇒ 702 = 702.
- Final: fixed #3 + #4 + #5 dải "Tin chưa đọc" chốt sai khi >1 trang chưa đọc / mở bằng around — `pinUnread()` chỉ chốt khi thấy ranh giới (có tin ≤ mốc phía trên hoặc hết tin cũ), gọi lại sau tải `before` / `around`; bỏ tin đã thu hồi; reset() xoá mốc.
- Final: fixed #6 Ctrl/⌘K: không giành phím khi đang mở popup (.modal.show / defaultPrevented); mở rộng cột TẠM, không ghi đè lựa chọn thu gọn đã lưu.
- Final: fixed #7 a11y: vùng tên bắt cả Space; "+ Mới" aria-haspopup / aria-expanded / Esc; chip + tab chủ đề bỏ role tablist/tab ⇒ role=group + aria-pressed.
- Final: fixed #8 code chết: bỏ computed `shortTime`, luật CSS trùng `.cr--collapsed.cr--active::before`, chú thích cũ nhắc V2BaseMiniTab.
- Final: Ruling: #9 `sender_role` = vai trò HIỆN TẠI (hạ quyền / rời nhóm ⇒ tin cũ mất nhãn) — chấp nhận theo D9, ghi vào design §2 — sai thì cần lưu vai trò lúc gửi vào tin.
- Final: minor (deferred): menu "+ Mới" chưa đóng khi focus rời đi (chỉ đóng khi bấm ngoài / Esc).
- E2E: sửa ca Z1 `chat-toolbar-zalo` theo thiết kế mới (thanh nổi góc trên-phải DÒNG tin, top = dòng − 14px, trong bề ngang dòng) thay cho "bên phải bong bóng".
- E2E lượt 2 (sau fix review): 9/10 — chat-thong-bao-emoji E3 FAIL do fix #2 (neo 👍 góc dưới-phải dòng ⇒ tin 1 dòng bị thanh thao tác che, rê không mở hàng emoji). Final: Ruling: đổi cách sửa #2 — 👍 về cạnh khối chữ như cũ + `.cm__row { padding-right: 34px }` chừa chỗ; Playwright: tin ngắn & tin dài 👍 không chồng thanh thao tác, vùng cuộn 702 = 702 — sai thì chữ hẹp đi 34px.
- E2E lượt 3: chat-thong-bao-emoji 10/10 · chat-toolbar-zalo 8/8 · chat-giao-dien 4/4 · chat-panel-phai 6/6 · chat-bo-sung 6/6 · chat-gd2-polish 7/7 · workspace-tasks 12/12 · agent-chat-pin 6/6 · agent-chat 19/19 · chat-core 7/8 (GĐ2: NV 24 bị đẩy sang trang 404 "không được cấp quyền truy cập trang" — chạy lại riêng chat-core **8/8**; nguyên nhân 404 thoáng qua CHƯA kiểm xong, không thấy 401/5xx trong log API, không thuộc phần code GĐ8 đụng).
- Dọn dữ liệu: 4 nhóm "[e2e] Nhóm chat …" (48 tin) + 4 tin thử NV 34 ở nhóm 1612 (đặt lại last_message của conv 962). API :8080 về chế độ thường (không AGENT_FAKE, 4 worker). KHÔNG commit.

## Sau GĐ8 — chỉnh theo góp ý (14/11)
- Thanh thao tác khi rê tin: từ góc trên-phải dòng (xa, khó bấm) ⇒ NGAY CUỐI DÒNG TIN (sau nút 👍, căn giữa dòng chữ cuối).
  `ChatMessageItem.placeActions()` đo dòng cuối bằng Range; dòng cuối sát mép phải ⇒ lùi vào trong, nhấc lên trên dòng cuối;
  không đè 👍 (tin tệp/ảnh). Đo Playwright 1440px: tin 1 dòng thanh cách 👍 2px, tin nhiều dòng thanh nằm sau chữ cuối dòng
  cuối, vùng cuộn 702 = scrollWidth 702 (không tràn). Cập nhật ca Z1 `chat-toolbar-zalo` — CHƯA chạy e2e (task nhỏ).
- 14/11 · Popup "Tin nhắn mới" (`DirectoryModal`): mặc định công ty THEO HỒ SƠ (`employee_infos.company_id`, không phải công
  ty đang chọn) — FE gửi `default_company=1` lần mở, BE trả `meta.company_id` để gán ô chọn; lọc công ty đổi từ bảng kiêm nhiệm
  `company_employees` sang `employee_infos.company_id` (tái hiện: CN Hải Phòng ra 15 người, 8 thuộc công ty khác ⇒ nay 7).
  Gom theo phòng ban như cũ; chế độ "Tất cả công ty" tiêu đề nhóm kèm tên công ty (cắt "…" khi dài). PHPUnit
  `ChatGiaoDienTest` +2 ca (RED→GREEN) + `ChatApiTest::test_danh_ba_*` đạt. E2E thêm G5 `chat-giao-dien` — CHƯA chạy (task nhỏ).
