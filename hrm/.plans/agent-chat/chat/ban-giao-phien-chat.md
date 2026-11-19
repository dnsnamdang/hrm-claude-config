# Bàn giao cho phiên CHAT (Nhóm trao đổi + chat 1–1) — viết 11/11/2026

> **CẬP NHẬT 11/11 tối — ĐỌC TRƯỚC:** core chat ĐÃ XONG + push nhánh `gop_db-nhom-trao-doi` (hrm-api `fd1c2f1e7`,
> hrm-client `d0644d95d`), chưa merge `gop_db`. Trạng thái, checkpoint, server demo, token thử, bẫy đã gặp:
> `gd1-core-chat/plan.md` (mục Checkpoint cuối + "Ghi chú Phase 1…4"). Spec triển khai: spec §11. Phần dưới là bàn giao gốc.

> Đọc file này ĐẦU PHIÊN. Phiên chat chạy SONG SONG với phiên TPE SMART AGENT (trợ lý AI) — 2 phiên khác nhau, cùng máy,
> cùng DB local. Mục đích file: để 2 phiên không giẫm lên nhau.

## 1. Phiên chat làm gì

- Feature: **Phân hệ Công việc — Nhóm trao đổi + chat 1–1** (phần "core chat"), KHÔNG gồm Trợ lý AI.
- Tài liệu (đọc theo thứ tự):
  1. `HRM/.plans/gop-db/phan-he-cong-viec/plan.md` — mục **"▶ 09/11/2026 — ĐỔI LOGIC LỚN"**, **"✅ CHỐT 10/11/2026"**,
     Checkpoint 11/11, rồi GĐ1 / GĐ2 / GĐ3.
  2. Spec: `HRM/docs/superpowers/specs/gop-db/2026-11-02-phan-he-cong-viec-design.md` (§3.0–3.5, §3.11, §3.12, §4.4b, §4.6, §5.1).
  3. Mockup đã chốt: `HRM/.plans/gop-db/phan-he-cong-viec/gd0-mockup/` (mở qua `python3 -m http.server`, KHÔNG mở file://)
     — màn 01, 03, 04, 05, 08, 11–13, 15–21, 31, 32 + `_build/dm.js`, `dm.css`, `qsel.*`, `sb2.js` (v=9).
     Dự án KH (09, 10, 14, 23, 25–30) KHÔNG thuộc bản chốt (N2p, làm sau).
- Trạng thái 11/11: mockup web Nhóm trao đổi đã chốt; **chưa có plan code GĐ1 theo mô hình mới** (việc C1 — mục GĐ1
  trong plan.md còn viết theo mô hình cũ Phòng làm việc / Mở-Kín, phải viết lại theo N4); **chưa có lệnh code**.
- Việc đầu tiên hợp lý: viết plan code GĐ1 (nền Nhóm trao đổi + thành viên + quyền) theo mô hình mới → user duyệt →
  hỏi "làm" riêng (CLAUDE.md "Đụng source code phải được user cho phép RÕ RÀNG").

## 2. Nhánh + worktree — TÁCH RIÊNG

- KHÔNG dùng `websites/wt-tpe-agent/*` (của phiên Agent, đang có code chưa commit + đang chạy test/eval).
- KHÔNG làm thẳng trên `ERP-HRM/HRM/hrm-api` / `hrm-client` (checkout chính, :8000/:3000 — dùng chung).
- Tạo nhánh mới từ **`origin/gop_db`** (11/11 đầu nhánh `5d13365e3`), worktree riêng cho CẢ 2 repo, ví dụ:
  ```bash
  cd ~/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-api   && git fetch origin && git worktree add -b gop_db-nhom-trao-doi ../../../wt-nhom-trao-doi/hrm-api origin/gop_db
  cd ~/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-client && git fetch origin && git worktree add -b gop_db-nhom-trao-doi ../../../wt-nhom-trao-doi/hrm-client origin/gop_db
  ```
  (tên nhánh / thư mục do user chốt; hỏi trước khi tạo). Worktree không có `.plans/`, `.claude/`, `docs/` — tài liệu luôn
  ghi về `HRM/.plans/gop-db/phan-he-cong-viec/`.
- Merge về `gop_db` chỉ khi user báo (memory "Feature mới: nhánh riêng, merge khi user báo").
- `.env` worktree: copy từ checkout chính, đổi cổng (mục 3). Vendor / node_modules: copy hoặc symlink như các worktree
  `wt-*` khác (xem memory hub "Môi trường dev / local / git").

## 3. Cổng — tránh đụng

Đang bận 11/11: :3000/:8000 (checkout chính) · **:3070/:8070 (phiên Agent — KHÔNG tắt)** · :3060/:3061/:8060/:8061 (worktree
HĐ bán) · :8770/:8772/:8793 (http.server mockup) · :6379 Redis · :3306 MySQL.
- Đề xuất phiên chat: API **:8080**, Nuxt **:3080** (`DEV_SERVER_PORT=3080`, `BASE_API_URL=http://127.0.0.1:8080`).
  Kiểm trước bằng `lsof -nP -iTCP:<cổng> -sTCP:LISTEN`.
- Tắt server: kill ĐÚNG PID theo cổng. **KHÔNG `pkill -f nuxt` / `pkill -f php`** (giết server của phiên kia).
- Socket node (`server_node/server.js`) và Redis dùng chung: nếu phiên chat cần chạy socket riêng để thử, chạy cổng khác,
  không tắt socket đang chạy.

## 4. File phiên Agent ĐÃ sửa (chưa commit) — dễ xung đột khi merge

Phiên Agent sửa ở nhánh `gop_db-tpe-smart-agent` (worktree `wt-tpe-agent`), chưa commit:

| File | Phiên Agent thêm gì | Phiên chat lưu ý |
|---|---|---|
| `hrm-client/components/BasicSubsystem.vue` | Icon TPE SMART AGENT trên topbar (giữa Phóng to và chọn phân hệ) + `this.socket.on('agent', d => this.$root.$emit('agent-event', d))` | Icon **Tin nhắn** (spec §4.6) cũng nằm ở cụm này ⇒ THÊM cạnh, không viết lại khối `<ul>` / khối socket |
| `hrm-client/components/menu-sidebar.js` | Mục menu "TPE SMART AGENT" (`/agent`, mã `assign.tpe_agent.use`) trong `menuItemsAssign` | Thêm mục Nhóm trao đổi / Tin nhắn thì chèn dòng mới, không sắp xếp lại mảng |
| `hrm-api/server_node/server.js` | Phát sự kiện `'agent'` khi tin Redis có `kind: 'agent'` (kênh `user_notification_{employees.id}`) | GĐ3 cần tách sự kiện chat khỏi `notification` ⇒ thêm nhánh `kind: 'chat'` theo cùng kiểu, giữ nhánh `agent` |
| `hrm-api/config/queue.php` | Connection `agent` | Chat cần queue riêng thì thêm connection khác, không đổi `agent` |
| `hrm-api/app/Console/Kernel.php` | Lịch `agent:prune` 03:15 | Thêm dòng, không sửa dòng cũ |
| `hrm-api/app/Support/Permissions/Catalog/assign.php` | 3 mã `assign.tpe_agent.*` | Mã quyền chat thêm khối mới; đồng bộ bằng `permission:catalog-sync` (skill `permission-seeder`) |

Agent nằm trọn trong `hrm-api/Modules/Agent/` + `hrm-client/pages/agent/`, `components/agent/`, `utils/agentSocket.js`,
`utils/agentFormat.js` — phiên chat KHÔNG đụng các đường này.

## 5. DB local dùng chung (`db_gop_6_11`)

- Phiên Agent đã chạy migration `Modules/Agent/Database/Migrations/2026_11_12_000001…000007` (bảng `agent_*`). Phiên chat
  KHÔNG rollback / `migrate:fresh` / `migrate` cả loạt.
- Chạy migration của chat: liệt kê đúng từng file (`migrate:status`, `migrate --pretend`), hỏi user, chạy lẻ bằng `--path`
  (CLAUDE.md mục "Chạy migrate").
- Dữ liệu thử của Agent: các hội thoại tiêu đề "[thử]" / "[eval]" và bảng `agent_*` — không xoá, không dùng để thử chat.
- `.env` worktree chat trỏ cùng DB thì cẩn thận cache: `php artisan cache:clear` ảnh hưởng cả phiên kia (Redis chung) — hạn
  chế, nếu cần thì báo user.

## 6. Chỗ nối chat ↔ Agent — CHƯA làm ở phiên nào

Mockup 33 ghim "TPE SMART AGENT" ở đầu mọi danh sách hội thoại (`sb2.js` v=9) và `@TPE SMART AGENT` trong chat nhóm (AI1b).
Phần này làm SAU khi chat GĐ3 có bảng tin nhắn + socket ổn định, và chỉ 1 phiên làm (thống nhất với user lúc đó). Phiên chat
cứ thiết kế danh sách hội thoại có chỗ cho 1 "hội thoại hệ thống" ghim đầu (không cần code Agent). Trang Agent hiện tại:
`/agent` (worktree Agent), API `GET/POST api/v1/agent/conversations…`.

## 7. Quy tắc chung nhắc lại

- Mọi code / migration / quyền / commit: hỏi user "làm" kèm phạm vi (repo · nhánh · file · DB).
- Không `git stash` trên repo dùng chung; không commit/push khi user chưa báo.
- Task FE: kiểm bằng Playwright (đo DOM) trước khi báo xong; e2e chạy với `BASE_URL=http://127.0.0.1:3080` và file auth
  riêng, KHÔNG chạy project `setup` mặc định (ghi đè `.auth/user.json` của checkout chính).
- Lỗ hổng quyền đọc phát hiện được: ghi vào `HRM/.plans/gop-db/va-lo-hong-quyen-doc/ghi-chu.md` (đang có #1–#16), không vá lẻ.
- Trạng thái phiên Agent: `HRM/.plans/agent-chat/agent/plan.md` (mục "⏸ VIỆC CHỜ") + `de-xuat-kd-truoc-ban.md`.
