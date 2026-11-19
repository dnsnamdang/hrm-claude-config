# AGENT + CHAT — trang đầu phiên (đọc TRƯỚC)

> Từ 13/11/2026: **TPE SMART AGENT** (trợ lý AI) và **Chat** (Nhóm trao đổi + chat 1–1) phát triển trong **CÙNG MỘT phiên**,
> tài liệu gom về đây. Không còn "phiên Agent" / "phiên Chat" riêng.
> Nhóm này nằm NGOÀI `.plans/gop-db/` theo chốt của user: `gop-db/` chỉ dành cho các tính năng chuyển ERP → HRM.
> (Code vẫn tách nhánh từ `origin/gop_db` và merge về `gop_db` — chỉ tài liệu là để ngoài.) Trạng thái ghi ở `.plans/STATUS.md`.
> Phụ trách: @namdangit

## 0. Nguyên tắc chung (user chốt 13/11/2026)

- **Quy mô 1.000–2.000 người**: mọi tính năng AI/CHAT phải chịu tải — gom lô / queue, không query trong vòng lặp theo người, index + phân trang con trỏ, tính trước số người nhận × tần suất khi bắn socket / FCM.
- **Đa nền tảng**: sẽ có app mobile + app desktop ⇒ logic và dữ liệu cấu hình đặt ở BE / API dùng chung, web chỉ hiển thị; cài đặt người dùng cần đồng bộ nhiều thiết bị thì lưu BE.

## 1. Bản đồ tài liệu

| Phần | Ở đâu |
|---|---|
| **Agent** — plan (checkpoint cuối ở cuối file) | `agent/plan.md` |
| Agent — design tóm tắt · spec đầy đủ | `agent/design.md` · `docs/superpowers/specs/agent-chat/2026-11-11-tpe-smart-agent-design.md` |
| Agent — deploy · API key · thêm công cụ | `agent/HUONG-DAN-DEPLOY.md` · `agent/HUONG-DAN-API-KEY.md` · `agent/huong-dan-them-cong-cu.md` |
| Agent — đề xuất / tư vấn theo đợt | `agent/de-xuat-*.md`, `agent/tu-van-*.md`, `agent/y-tuong.md` |
| Agent — script kiểm (eval nhóm, hỏi thật, đối chiếu số) | `agent/scripts/README.md` |
| Agent — mockup topbar / ghim Agent | `agent/mockup-an-tuong/` · `agent/de-xuat-ghim-agent-trong-chat.md` |
| **Chat** — GĐ1 core chat (Nhóm trao đổi + 1–1) | `chat/gd1-core-chat/plan.md` |
| Chat — GĐ3 chat bổ sung (đang soạn, trực tuyến, avatar, Xóa phía tôi) | `chat/gd3-chat-bo-sung/plan.md` |
| Chat — GĐ4 thông báo tin nhắn + Emoji + Sticker (13/11, code xong chưa commit) | `chat/gd4-thong-bao-emoji-sticker/plan.md` |
| Chat — GĐ5 chụp màn hình + chỉnh ảnh + nén ảnh (13/11, code xong chưa commit) · demo `chat/demo-chup-man-hinh/` | `chat/gd5-chup-man-hinh/plan.md` |
| Chat — GĐ6 bản nháp tin đang soạn theo hội thoại (13/11, đã lên gop_db a108b98e2) | `chat/gd6-ban-nhap/plan.md` |
| Chat — GĐ7 panel phải (Ảnh · Tệp · Link · Nhiệm vụ) + sửa nút đính kèm + nới panel trái (13/11, ĐÃ lên gop_db api 7d69641da · client 8be3a27dc, ĐÃ deploy TPE + backfill xong 14/11) | `chat/gd7-panel-phai/design.md` |
| Chat — GĐ8 giao diện mới (thoát kiểu Zalo; tin dạng luồng, thanh lọc chip, 1 dải tab chủ đề) — 14/11 ĐÃ lên origin/gop_db (api `78bcd32f3` · client `6a459ecd4`, chung commit với GĐ9), CHƯA deploy | `chat/gd8-giao-dien/design.md` · `mockup-v2.html` |
| Chat — GĐ9 tab Meeting trong nhóm (14/11 ĐÃ lên origin/gop_db api `78bcd32f3` · client `6a459ecd4`, CHƯA deploy — deploy phải chạy migration `2026_11_18_000001_add_workspace_id_to_meetings_table`) | `chat/gd9-tab-meeting/design.md` · `mockup.html` |
| Chat — GĐ10 Chat / Agent mở dạng NGĂN TRƯỢT trên trang đang làm (14/11, code xong + đo Playwright, CHƯA commit; còn D6 e2e `chat-drawer.spec.ts` + chạy lại bộ chat/agent) — nhánh client `gop_db-chat-drawer` (wt-nhom-trao-doi), KÈM sửa "tin của mình bên PHẢI kiểu bong bóng" (user bỏ D2 GĐ8) | `chat/gd10-ngan-truot/plan.md` |
| Chat — GĐ10 ngăn trượt Chat/Agent + tin kiểu bong bóng + đổi tên "Không gian trao đổi công việc" (14/11 ĐÃ lên origin/gop_db client `f0a0e778b`, CHƯA deploy) | `chat/gd10-ngan-truot/plan.md` |
| Chat — GĐ11 **Báo lỗi màn hình** (tab "Báo lỗi" mép phải mọi màn ⇒ chụp + gom lỗi API ⇒ tin vào nhóm hỗ trợ theo công ty) — 14/11 ĐÃ DEPLOY TPE 14/11 (api `86fcb16ba` · client `814664a79`) — đổi tên hiển thị "YC hỗ trợ / Yêu cầu hỗ trợ"; ghi chú deploy cuối plan.md | `chat/gd11-bao-loi-man-hinh/design.md` · `mockup.html` |
| Chat — GĐ12 **Nhóm trao đổi gắn Dự án KH** (nhóm "Là dự án KH" gắn Dự án TKT / GP, thêm nhân sự 1 lần lúc tạo, nhiệm vụ/meeting về manager, thành viên mọi công ty) — 15/11 ĐÃ lên origin/gop_db (api `72f929f76` · client `9f5014f3b`, chung commit với GĐ13), ĐÃ DEPLOY TPE 15/11 | `chat/gd12-nhom-du-an-kh/design.md` · `plan.md` · `ledger-sdd.md` |
| Chat — GĐ13 **@all nhắc tất cả thành viên nhóm** (ai cũng @all được, tôn trọng tắt thông báo, cờ `chat_messages.mention_all`) — 15/11 ĐÃ lên origin/gop_db cùng GĐ12 (api `72f929f76` · client `9f5014f3b`), ĐÃ DEPLOY TPE 15/11 | `chat/gd13-mention-all/design.md` · `plan.md` |
| Chat — GĐ14 **bấm vào người ⇒ popup thông tin cá nhân + Nhắn tin** (chức vụ, SĐT, email; V2BaseModal) — 15/11 ĐÃ lên origin/gop_db (api `a5290628e` · client `85a2a590d`), CHƯA deploy (không migration) | `chat/gd14-ho-so-nguoi-dung/design.md` · `plan.md` |
| Chat — GĐ35 **Tạo vấn đề từ tin nhắn** (như Tạo nhiệm vụ: thẻ vấn đề + nhãn + realtime, web + app; migration `issues.source_message_id`) — 18/11 ĐÃ MERGE (api gop_db e395dc12d · client gop_db 623f7ece8 · app develop 98ec972), CHƯA deploy; migration 2026_11_25_000001; đã chạy thử máy ảo | `chat/gd35-tao-van-de-tu-tin/design.md` · `plan.md` |
| Chat — GĐ36 **app: chữ tin đậm + Bình luận thành tab** (thân tin #0F172A w500; header chi tiết NV/VĐ ưu tiên nút Chat icon forum; Bình luận thành tab nhúng) + chip lọc web gọn hơn — 18/11 ĐÃ MERGE app develop 1cf5872 (chip lọc trong client 623f7ece8), CHƯA build app | `chat/gd36-giao-dien-tin-app/plan.md` |
| **Agent — chọn model (Claude / DeepSeek) + thống kê theo model + eval so sánh** (15/11, CODE XONG, nhánh `gop_db-agent-chon-model` api `12986fddf` · api `3fefb0545` · client `960d04154`, ĐÃ DEPLOY TPE 15/11; giữ Haiku + giọng văn nhân viên báo cáo; prod chưa khai DEEPSEEK_API_KEY) | `agent/chon-model/design.md` · `plan.md` (checkpoint cuối) · spec `docs/superpowers/specs/agent-chat/2026-11-15-agent-chon-model-design.md` |
| Chat — GĐ15 tô rõ hội thoại đang mở + tooltip khi thu gọn + giữ chưa đọc khi ngăn đóng · GĐ16 **tạo nhanh nhắc việc từ tin** — 15/11 ĐÃ lên origin/gop_db client `828d88245` (merge của e9dbcb6cf + b9de02317), CHƯA deploy, không BE / migration | `chat/gd15-dong-dang-mo/plan.md` · `chat/gd16-nhac-viec-tu-tin/design.md` · `plan.md` |
| **Chat + Agent trên APP MOBILE** — 17/11 mockup 60+ màn ĐÃ VẼ (`meeting-mobile.pen` x 30600) + plan 17 task / 7 giai đoạn — CHƯA CODE, chờ user duyệt plan | `app-mobile/design.md` · `plan.md` · `phan-tich-app-web.md` |
| Chat — **gọi thoại / video như Zalo** — 14/11 ĐỀ XUẤT 3 phương án, user bảo LƯU TRIỂN KHAI SAU | `chat/goi-thoai-video/de-xuat.md` |
| Chat — bàn giao gốc 11/11 (bẫy 2 phiên song song — nay đã gộp phiên) | `chat/ban-giao-phien-chat.md` |
| Chat — **spec gốc + mockup + Nhiệm vụ trong nhóm (GĐ2)** — để nguyên chỗ cũ vì thuộc Phân hệ Công việc | `.plans/gop-db/phan-he-cong-viec/` (`plan.md`, `design.md`, `gd0-mockup/`, `gd2-nhiem-vu-trong-nhom/`) · spec `docs/superpowers/specs/gop-db/2026-11-02-phan-he-cong-viec-design.md` §3, §11 |

Việc mới: Agent ⇒ append vào `agent/plan.md`; Chat ⇒ tạo `chat/gd{N}-<ten>/plan.md`; việc đụng CẢ HAI (vd "@Agent" trong nhóm chat) ⇒ `chat-agent/<ten>/plan.md` hoặc ghi ở `agent/plan.md` kèm link.

## 2. Môi trường dùng chung

| | Agent | Chat |
|---|---|---|
| Worktree | `websites/wt-tpe-agent/{hrm-api,hrm-client}` | `websites/wt-nhom-trao-doi/{hrm-api,hrm-client}` |
| Nhánh gần nhất (13/11) | api `gop_db-agent-cache-1h` (đã lên gop_db `dcd4a37f6`) · client `gop_db-tpe-smart-agent` (đã merge) | api `gop_db-chat-bo-sung` (đã lên gop_db `337060dca`) · client detached |
| API · Nuxt · socket | :8070 (php8.1 `-S`) · :3070 · :8896 | :8080 · :3080 · :8895 |
| DB local | `db_gop_6_11` (chung) | như bên |

- Việc mới: **nhánh riêng tách từ `origin/gop_db`**, merge khi user báo. Có thể dùng lại 1 trong 2 worktree (kiểm `git status` sạch trước khi đổi nhánh — server đang chạy từ worktree đó sẽ chạy theo nhánh mới).
- Deploy TPE: `~/build_tpe.sh` từ 13/11 TỰ `queue:restart` (mọi worker tpe) + restart socket `hrm-tpe-socket` khi `server_node/` đổi (ép `RESTART_SOCKET=1`) — không cần bước restart tay.
- `server_node/server.js` dùng chung: rẽ 3 nhánh kind `agent` → `agent`, chat → `chat`, còn lại `notification`. Prod: socket là pm2 ROOT id 10 (`pm2 restart hrm-tpe-socket`).
- Agent nhúng trong Tin nhắn (`?agent=1&ac=`, `AgentWorkspace` dùng chung `/agent`) ⇒ sửa `AgentWorkspace`/`AgentChat` phải chạy cả e2e `agent-chat` + `agent-chat-pin`.
- E2E Agent cần :8070 `AGENT_FAKE=1` ⇒ HỎI user trước khi restart. :8070 `QUEUE_CONNECTION=sync` + có FIREBASE ⇒ e2e chat có ghi có thể bắn push thật.
- PHPUnit: `php -d memory_limit=1G vendor/bin/phpunit Modules/Agent/Tests` (221) · `Modules/Assign/Tests/.../Workspace` (107) + Task (31).

## 3b. Trạng thái 16/11/2026 (wrap up)

- **17/11 — Agent câu hỏi thị trường theo báo cáo "Phát triển thị trường - Khách hàng"** (`agent/phat-trien-thi-truong/` design · plan; spec `docs/superpowers/specs/agent-chat/2026-11-17-agent-phat-trien-thi-truong-design.md`): user DUYỆT thiết kế 17/11 (cách 1 công cụ mới `phat_trien_thi_truong`, Q1 công ty đang làm + `tap_doan`). Task 1–7 XONG 17/11 tối: api 8e9d017e8 + client ab194e229 nhánh `gop_db-agent-phat-trien-thi-truong` (wt-tpe-agent). **ĐÃ DEPLOY TPE 17/11** api b9faa6266 · client fe8b42f97. Deploy api + client cùng lúc. Checkpoint cuối plan.md.
- **17/11 khuya — Agent Dự án TKT (ĐÃ DEPLOY TPE 18/11 api 3ae239a02 · client 883eaed3c) theo báo cáo "Kết quả thực hiện dự án TKT"** (`agent/du-an-giai-phap/` design · plan; spec `docs/superpowers/specs/agent-chat/2026-11-17-agent-ket-qua-du-an-tkt-design.md`): nâng cấp `ket_qua_du_an_tkt` (3 tiêu chí, cây, chi tiết, tập đoàn), `thong_ke_du_an_tkt` +5 chiều, luật 6 "hỏi gì trả lời đó / không có đáp án ⇒ 1 câu rồi dừng" + luật 16. Nhánh `gop_db-agent-ket-qua-du-an-tkt` (api 89996d7d4 · client 9a5b2c3f2) đã push + merge gop_db. Phần Giải pháp (18/11): công cụ mới `tong_hop_giai_phap` theo báo cáo "Tổng hợp GP theo phòng ban" + `thong_ke_giai_phap` đếm người tham gia 4 vai trò + luật 17; spec `docs/superpowers/specs/agent-chat/2026-11-18-agent-tong-hop-giai-phap-design.md`; ĐÃ DEPLOY TPE 18/11 api 9e8361620 (client không đổi).

- **17/11 — Vấn đề v2 + GĐ34 tab Vấn đề trong nhóm** (`../gop-db/phan-he-cong-viec/van-de-v2/` design V1–V18 + plan · `chat/gd34-tab-van-de/`): IssuePanel thay CreateIssueModal ở 13 màn (nút bước theo `allowed_next_statuses`/`requires`, gia hạn, theo dõi, tệp, thông báo các bước, required FE+BE); tab Vấn đề trong nhóm thường + GP (TKT không), đóng nhóm thường ⇒ vấn đề mở tự "Đã đóng". e2e `assign/issue-panel-v2` + `assign/workspace-issues` tự bật API tạm QUEUE_CONNECTION=null (không push). ĐÃ DEPLOY TPE 17/11 (prod api `5eba99ce1` · client `21a383016`, migration 2026_11_23_000001 + 2026_11_24_000001/000002). 18/11: BE chặn hạng mục không thuộc GP (3 Request Vấn đề, mọi nơi chứ không riêng nhóm GP) + Nhiệm vụ (`solution_module_id`) — ĐÃ DEPLOY TPE 18/11 (api `52b93ae17`).
- **17/11 — GĐ33 tự rời nhóm** (`chat/gd33-roi-nhom/`): mọi vai trò, cả nhóm đóng; nhóm Dự án KH chưa hỗ trợ. API `POST workspaces/{id}/leave`, 3 lối vào (⋮ dòng hội thoại · ⚙ Cấu hình · tab Thành viên). ĐÃ DEPLOY TPE 17/11 (prod api `b796c8f86` · client `7394e4c47`, cùng GĐ32).
- **17/11 — GĐ32 tin trạng thái nhiệm vụ gọn + mờ** (`chat/gd32-tin-nhiem-vu-gon/plan.md`): "Nhiệm vụ <mã> đã được <người> cập nhật từ: <cũ> → <mới>", bỏ tên việc + ghi chú, viên xám mờ, trạng thái tô màu BE. Tin cũ giữ nguyên. ĐÃ DEPLOY TPE 17/11 cùng GĐ33.
- **17/11 — GĐ31 người khác công ty hiện họ tên + nhãn MÃ công ty** (`chat/gd31-ma-cong-ty/plan.md`): lỗi nhãn tên công ty đầy đủ ép họ tên về 0px. API trả `company_code`; dòng hội thoại + đầu cửa sổ chat có nhãn mã. ĐÃ DEPLOY TPE 17/11 (prod api `f95e246e6` · client `04995de37`, Nothing to migrate, site 200). Ngoài luồng: chat-drawer N7 chập chờn có sẵn (mã gốc cũng đỏ 1/3).
- **17/11 — GĐ29 toast lặp + GĐ30 việc nhỏ** (`chat/gd29-toast-lap/`, `chat/gd30-viec-nho-17-11/`): Agent `so_luong` 18 công cụ + luật 14, bộ đếm 5,000 ký tự ô soạn, 5 minor GĐ28. ĐÃ DEPLOY TPE 17/11 (prod api `53c72b441` · client `848e8d4eb`, Nothing to migrate, site 200). User bỏ: gán vai trò Agent 3 chị, YC hỗ trợ Q7, e2e K1.
- **16/11 khuya (wrap up)**: prod TPE = api `a33a6963e` · client `12a065598` (GĐ26 cột 320px · GĐ27 tab Nhiệm vụ tự nạp · GĐ28 vai trò hàng loạt). gop_db không còn gì chưa deploy. Việc chờ: mục 3 "TaskPanel 403 hiện 2 toast" — bản sửa FE đã có ở worktree `wt-quyen-xem-task` (chưa commit, đợt vá quyền đọc) ⇒ hỏi user tách riêng hay chờ; e2e workspace-kh-project K1 đỏ có sẵn (API php -S kẹt worker sau reload); minor GĐ28 (ledger "Final: minor").
- **16/11 khuya — GĐ28 chọn thành viên theo vai trò + đổi vai trò / mời ra hàng loạt** (`chat/gd28-chon-vai-tro-hang-loat/` design · mockup v2 · plan · ledger): ĐÃ DEPLOY TPE 16/11 khuya (prod api `a33a6963e` · client `12a065598`, gồm GĐ26 + GĐ27; Nothing to migrate, site 200).
- **16/11 tối — GĐ27 tab Nhiệm vụ của nhóm tự nạp lại** (`chat/gd27-tab-nhiem-vu-realtime/plan.md`): `WorkspaceView` nghe `task.updated` /
  tin hệ thống-thẻ khi đang ở tab Nhiệm vụ ⇒ gom 800ms nạp lại. ĐÃ DEPLOY TPE 16/11 khuya (client `97c97a86f`).
- **16/11 cuối ngày — GĐ26 cột hội thoại 360 ⇒ 320px** (`chat/gd26-cot-lien-he-hep/plan.md`): commit client `067de626b` trên nhánh
  `gop_db-chat-cot-lien-he-hep` — **CHƯA push / merge gop_db / deploy** (user: "commit rồi wrap up", tối mở phiên mới). Prod vẫn api `5db19c28b` · client `fe3ff8755`.
- **16/11 khuya — Chat GĐ22–25 (ĐÃ DEPLOY TPE api `5db19c28b` · client `fe3ff8755`)**:
  - GĐ22 `chat/gd22-ctv-cong-viec/plan.md`: phân hệ Công việc chọn được NV phòng cộng tác viên (store bỏ `assign` khỏi lọc; API `assign/tasks/employees?kem_ctv=1` cho TaskPanel, màn kho giữ lọc).
  - GĐ23 `chat/gd23-tin-trang-thai-nhiem-vu/plan.md`: nhiệm vụ trong nhóm đổi sang mốc chính (`Task::WORKSPACE_ANNOUNCE_STATUSES`) ⇒ tin hệ thống bấm mở TaskPanel.
  - GĐ24 `chat/gd24-tab-thanh-vien-phan-trang/plan.md`: tab Thành viên phân trang trên máy, mặc định 20.
  - GĐ25 `chat/gd25-nhiem-vu-realtime/plan.md`: `Task::updated` ⇒ `task.updated` realtime ⇒ thẻ nhiệm vụ trong tin + panel Tài nguyên tự đổi.
  - Ngoài luồng ghi lại: TaskPanel 403 hiện 2 toast (e2e task-panel-v2 ca 7 đỏ trên gop_db); e2e meeting-host cần .auth :3000; tab Nhiệm vụ của nhóm chưa tự nạp theo task.updated; nhãn quá hạn không tự đổi theo thời gian.
- **16/11 chiều–tối — Agent (5 đợt, ĐÃ DEPLOY TPE api `76dbd1641` · client `09c8a4489`)** — chi tiết `agent/thanh-phan-meeting/plan.md`:
  1. Tool `thanh_phan_meeting` (2 phía, điểm danh, không SĐT khách) + lọc `trang_thai`.
  2. Luật 12 "hỏi gì lấy đúng số liệu" + tham số lọc cho 8 tool (tinh_hinh nhom, lich_meeting tu_khoa/trang_thai, cham_cong chi_ngay, việc status/uu_tien/tu_khoa, phiếu đặt phòng trang_thai, biên bản viec).
  3. Nhớ đối tượng đã tra ("[đã tra: Tên = mã <loại> CODE]"), `meeting_cua_phong` tu_khoa, luật 13 phạm vi, ẩn thẻ bước trung gian.
  4. Câu trả lời: câu dẫn + gạch đầu dòng, **đậm**, ==nổi bật== (prompt luật 6/11 + FE `utils/agentAnswerFormat.js`).
  5. Rà soát toàn bộ tool: nhớ mọi loại (nhiệm vụ, dự án TKT, giải pháp), link /{id}/manager, don_cua_phong nhan_vien_id, bang_cong chi_ngay, tinh_hinh pham_vi, tool mới `viec_cua_phong` (47 tool).
  Kiểm: Haiku thật local từng đợt (đúng công cụ + tham số), PHPUnit Agent 279/282 (3 lỗi phòng họp do DB local chưa chạy migration `sort_order` của người khác), e2e ca liên quan xanh. CHƯA chạy lại toàn bộ `agent-chat.spec` (cần API AGENT_FAKE cho worktree wt-nhom-trao-doi).
- **Còn treo Agent:** công cụ danh sách chưa có tham số số lượng ("1 dự án mới nhất", "top 5"); xưng hô "anh" / "anh/chị" chưa đều; trên prod chỉ DNS Admin có quyền dùng Agent (vai trò "TPE_Thử nghiệm AI + GROUP CHAT") — chị Ngô Thị Lý / Thu Huyền / Lệ đã cài hạn mức nhưng CHƯA gán vai trò.
- **Local wt-nhom-trao-doi/hrm-api/.env**: đã chép ANTHROPIC_API_KEY / AGENT_MODEL / DEEPSEEK_API_KEY từ wt-tpe-agent (sao lưu `.env.bak_truoc_agent_key_20261116`) ⇒ :8080 hỏi AI THẬT (tốn tiền).
- **Thông báo người dùng**: `agent-chat/Cap-nhat-Chat-Agent-16-11-2026.docx` (chưa gồm các đợt Agent chiều–tối 16/11).
- **GĐ21** Esc khi xem ảnh trong ngăn chat đóng luôn ngăn ⇒ `ChatDrawer.onKey` nhường khi có `[data-testid="chat-image-viewer"]`. e2e N8 thêm bước Esc, drawer 10/10. ĐÃ DEPLOY TPE client `ddbcb7343` (api `4d694d95a`, Nothing to migrate, site 200). `chat/gd21-esc-xem-anh/plan.md`
- **Prod `.env`**: đã chép `DEEPSEEK_API_KEY` (từ `wt-tpe-agent/hrm-api/.env`), sao lưu `.env.bak_truoc_deepseek_20261116`, queue:restart. Model hệ thống vẫn Haiku (`agent_system_settings` prod trống). Chưa gọi thử DeepSeek từ prod. Lượt DeepSeek "hôm qua" user thấy là ở LOCAL (db_gop_6_11, 15/11 13:2x), prod không có lượt agent nào từ 13/11.
- **YC hỗ trợ không tự chọn nhóm (prod)**: KHÔNG phải lỗi code — chỉ công ty 1 có cài (nhóm "TPE - Hỗ trợ phần mềm", ws 3, conv 11, 395 thành viên); popup chỉ điền sẵn khi người mở là thành viên gửi được (Q7 GĐ11). namdangit (id 13) không trong nhóm ⇒ trống. Chờ user: (1) thêm người vào nhóm, hay (2) đổi luật cho mọi NV công ty gửi vào nhóm mặc định.
- **Chat giới hạn 5.000 ký tự/tin** (BE `SendMessageRequest`), ô soạn không có maxlength / bộ đếm — đề xuất thêm, chờ user.
- **Thông báo người dùng**: file Word `agent-chat/Cap-nhat-Chat-Agent-16-11-2026.docx` (Chat 9 mục · Agent 3 mục gồm cài quyền dùng AI theo người · phụ lục quản trị). Script dựng: scratchpad `docx/gen.js` (tạm). Còn kiểm: cài đặt YC hỗ trợ các công ty khác, migration tab Meeting.

## 3a. Trạng thái 15/11/2026 (wrap up)

- **15/11 tối (3)**: ĐÃ DEPLOY TPE (Claude chạy build_tpe.sh, EXIT 0, Nothing to migrate, site 200): prod api `3fefb0545` · client `87a115c9a` ⇒ GĐ15 + GĐ16 + GĐ17 đã lên prod. (Log có đoạn `pm2 Unknown command argument` — script tự gọi lại restart OK, tật có sẵn.)
- **15/11 tối (4)**: GĐ18 — xem ảnh trong ngăn kéo: tên người gửi + nút Ảnh trước bị menu trái che ⇒ `ChatImageViewer` portal ra body. e2e N8 + drawer 8/8 · emoji 10/10 · giao-diện 5/5. ĐÃ lên origin/gop_db client `37dcfc173`, CHƯA deploy. `chat/gd18-xem-anh-trong-ngan/plan.md`
- **15/11 tối (5)**: GĐ18+GĐ19 ĐÃ DEPLOY TPE (api `4d694d95a` · client `bb1340929`); worker `chat-push` ĐÃ BẬT (supervisor tpe-chat-push-worker + env CHAT_PUSH_QUEUE) — nhóm đông ~600: "đã đọc" phát cho cả nhóm (thừa), push FCM tuần tự 1 job vượt timeout 60s worker `hrm`, mỗi máy gọi unread-count sau mỗi tin. `chat/gd19-nhom-dong/design.md`
- **15/11 tối (6)**: GĐ20 — đóng ngăn khi nhóm chưa tải xong ⇒ activeId kẹt (nhóm "câm") ⇒ ChatPane trong ngăn chỉ setActive khi ngăn mở (provide/inject). e2e N10, drawer 10/10. ĐÃ DEPLOY TPE client `8ba077abb`. `chat/gd20-ngan-dong-som/plan.md`
- **15/11 tối (2)**: GĐ17 thanh thao tác tin to cạnh bong bóng + chữ chat 15px + khung soạn ĐÃ lên origin/gop_db client `87a115c9a` (chưa deploy, chỉ client). `chat/gd17-thanh-thao-tac/plan.md`.
- **15/11 tối**: GĐ15 + GĐ16 ĐÃ push origin/gop_db client `828d88245` (chưa deploy; chỉ client, không migration). Prod đang ở api `3fefb0545` · client `960d04154` (gồm GĐ14 + Agent chọn model — 2 dòng "chưa push / chưa deploy" bên dưới đã CŨ). Socket local :8895 phải bật từ `hrm-api/` (`SOCKET_PORT=8895 node server_node/server.js`).

- **Prod TPE ĐÃ deploy 15/11 chiều tới api `3fefb0545` · client `960d04154`** (GĐ14 popup hồ sơ + Agent chọn model + giọng văn báo cáo; migration 2026_11_22_000001/000002).

- **Agent chọn model (15/11 chiều)**: code xong 8 task + review cuối, nhánh `gop_db-agent-chon-model` (wt-tpe-agent, api + client) CHƯA push. Migration `2026_11_22_000001/000002` đã chạy db_gop_6_11. So sánh thật 50 câu Haiku 5.5 (đang dùng) vs DeepSeek Flash: 100%/98% đúng công cụ, 20.91 vs 17.28 ₫/câu — đề xuất giữ Haiku; Excel `agent-eval-compare-20261115-125550.xlsx`. Chờ user quyết + báo merge. :8070 chạy trả lời THẬT. Ngoài luồng: 3 ca agent-stats.spec đỏ có từ trước (ngân sách công ty 1 · stub Chủ nhật · tooltip 3.1px). wt-tpe-agent :8070 (thật) + :3070 (nuxt dev) + :8896 (socket) đang bật.

- **Prod TPE**: ĐÃ deploy tới api `72f929f76` · client `9f5014f3b` (15/11, Claude chạy `build_tpe.sh` — EXIT 0, migration 2026_11_20_000001 + 2026_11_21_000001 batch 478, site 200) ⇒ GĐ12 Nhóm gắn Dự án KH + GĐ13 @all (gợi ý, cờ `mention_all`, tô nền @ trong ô soạn) đã lên prod.
- **origin/gop_db CHƯA deploy**: GĐ14 popup thông tin cá nhân (api `a5290628e` · client `85a2a590d`, không migration).
- **Deploy**: dùng skill cá nhân `deploy-hrm` (`~/.claude/skills/deploy-hrm/SKILL.md`) — ssh nháy kép `ssh -o BatchMode=yes -o ConnectTimeout=15 -p 2225 erp_tpe@124.158.4.24 "<lệnh>"`; rule allow phải do user thêm qua `/permissions`.
- **Local**: wt-nhom-trao-doi api + client nhánh `gop_db-chat-ho-so` (= origin/gop_db); :8080 API (php8.1, 4 worker) · :3080 Nuxt · :8895 socket đang chạy (khởi động 15/11 sáng, log ở scratchpad phiên). Nhóm thử 93 (conv 96) dùng để kiểm; 2 tab Nhiệm vụ/Meeting của nhóm này đang tắt (giữ nguyên).
- **Chờ user**: deploy GĐ14 · e2e @all + popup hồ sơ (`chat-core.spec.ts`) khi user yêu cầu · 6 ruling GĐ12 · việc chờ cũ (gọi thoại/video, tạo vấn đề từ tin, @Agent, Agent "đi muộn hôm nay").
- **Đã chốt 15/11**: công tắc tab Nhiệm vụ/Meeting chỉ Quản lý nhóm thấy — đúng quyền, không sửa.

## 3. Trạng thái 14/11/2026 (wrap up ~13:00)

- **Prod TPE — ĐÃ deploy hết tới origin/gop_db client `f0a0e778b` · api `78bcd32f3` (user báo 14/11)**: Agent + core chat + chat bổ sung ·
  GĐ4 thông báo/emoji/sticker · GĐ5 chụp màn hình · GĐ6 bản nháp · Agent hạn mức theo người · GĐ7 panel phải (backfill link xong, 1 link) ·
  GĐ8 giao diện mới · GĐ9 tab Meeting trong nhóm (migration `2026_11_18_000001_add_workspace_id_to_meetings_table` — user chưa báo riêng
  đã chạy, nếu tab Meeting lỗi thì kiểm `migrate:status`) · GĐ10 ngăn trượt Chat/Agent + tin kiểu bong bóng + tên "Không gian trao đổi công việc"
  + bỏ mục Tin nhắn / TPE SMART AGENT khỏi menu Công việc · popup Tin nhắn mới lọc công ty theo hồ sơ.
- **Lưu ý prod**: mục "Tin nhắn" / "TPE SMART AGENT" đã bỏ khỏi menu ⇒ không còn dòng bật/tắt ở Cài đặt phân hệ; key cũ đã lưu vẫn có hiệu lực.
- **Đợt sau (đã ghi plan GĐ4)**: chia lô push FCM nhóm đông · cờ notify theo người thay `muted_ids` · API sticker dùng chung cho app.
- **Đề xuất lưu làm sau**: gọi thoại / video (`chat/goi-thoai-video/de-xuat.md`, chưa chọn phương án).
- **Môi trường local**: worktree `wt-nhom-trao-doi` — client nhánh `gop_db-chat-drawer` (= origin/gop_db), api nhánh `gop_db-chat-tab-meeting`
  (= origin/gop_db 78bcd32f3); :3080 Nuxt · :8080 API thường (4 worker, không AGENT_FAKE) · :8895 socket.
- **GĐ11 Yêu cầu hỗ trợ / báo lỗi màn hình (14/11 tối)**: ĐÃ DEPLOY TPE 14/11 (api 86fcb16ba · client 814664a79). Còn: cấp quyền "Cài nhóm tiếp nhận yêu cầu hỗ trợ" + tạo nhóm hỗ trợ từng công ty + cài nhóm mặc định. wt-nhom-trao-doi đứng nhánh `gop_db-chat-bao-loi` (= origin/gop_db). 
- **GĐ12 Nhóm trao đổi gắn Dự án KH (15/11 rạng sáng)**: CODE XONG 10 task + final review, CHƯA commit. wt-nhom-trao-doi (:8080/:3080) nay đứng nhánh `gop_db-chat-nhom-du-an-kh` (api + client). Migration `2026_11_20_000001` đã chạy db_gop_6_11. Ruling cần user soát: cuối `chat/gd12-nhom-du-an-kh/plan.md`.
- **Chờ user**:
  - Agent: câu "đi muộn hôm nay" không ra người — nguồn là `timesheet_summaries.is_late` (chỉ có sau khi `calc:timesheet` chạy cron) ⇒ cần thông tin prod (Agent trả lời gì · giờ hỏi · dashboard HCNS · crontab).
  - Agent: chia nhóm công cụ (ước 8–9 ₫/câu) · góc nhìn lãnh đạo B4/D3/D4/A6 · đề eval #51/#52 · cờ "đã qua" meeting · dọn dữ liệu thử local (AGPH, grants role 18).
  - Chat: tạo vấn đề từ tin (HOÃN — bảng issues chưa có workspace_id/source_message_id) · Dự án KH thêm tab nhóm chat (N2p) · "@Agent" trong nhóm chat (cần spec riêng).
- Ngoài luồng đã ghi: 2 ca PHPUnit `WorkspaceTaskTest` fail sẵn trên origin/gop_db (13/11) · lỗ hổng quyền đọc `.plans/gop-db/va-lo-hong-quyen-doc/ghi-chu.md` (#6 Task, #15 manager GP, #17 Issue, #19/#20 phiếu) · MyTodo getUrl · `AgentEvalCommandTest` xoá CSV eval thật.
