---
name: run-hrm
description: Khởi động / chạy local toàn bộ dự án HRM (MySQL + API Laravel :8000 + client Nuxt :3000) và mở trên trình duyệt. Dùng khi user nói "chạy HRM", "run HRM", "khởi động HRM", "mở HRM trên trình duyệt". Đã chốt đúng phiên bản Node + thứ tự khởi động + các bẫy đã trả giá.
---

# Chạy HRM ở local

Stack native (KHÔNG dùng Docker — máy này Docker thường không bật). 3 tầng: **MySQL → API :8000 → client :3000**.

## Chạy nhanh (1 lệnh)

```bash
bash /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.claude/skills/run-hrm/run-hrm.sh
```

Script tự: bật MySQL nếu chưa, chạy API nếu `:8000` trống, chạy client Nuxt (Node 14) nếu `:3000` trống, rồi chờ client compile xong. Idempotent — gọi lại khi đã chạy thì bỏ qua tầng đã lên. Log ghi ở `/tmp` (xem dòng cuối script in ra).

## Thông số đã chốt (QUAN TRỌNG)

| Tầng | Lệnh | Cổng | Ghi chú |
|---|---|---|---|
| MySQL 8.0 | `brew services start mysql@8.0` | `127.0.0.1:3306` | DB `erp_hrm_check`; `brew services list` xem trạng thái |
| API Laravel 8 | `cd HRM/hrm-api && php artisan serve --host=0.0.0.0 --port=8000` | `:8000` | PHP 7.4 |
| Client Nuxt 2 | `cd HRM/hrm-client && npm run dev` | `:3000` | **BẮT BUỘC Node 14.21.3** |

- **Node phải là 14.21.3** — `export PATH="$HOME/.nvm/versions/node/v14.21.3/bin:$PATH"` trước khi `npm run dev`.
  `node_modules/node-sass` được build cho ABI Node 14 (`darwin-x64-83`). Chạy Node 12 → màn ra lỗi build `node-sass Missing binding ... darwin-x64-72` (overlay đỏ trên trình duyệt). Chạy Node 20/24 cũng sai ABI. **Ghi chú "Node mặc định máy là 12" trong CLAUDE.md gốc là lệch — Nuxt phải chạy Node 14.** (Node 20 chỉ dùng cho bộ e2e Playwright.)
- Compile client lần đầu mất **vài phút** (RAM ~2–3 GB). Chờ marker `Waiting for file changes` / `Listening on: http://localhost:3000/` trong log. Request `:3000` đầu tiên lúc đang compile sẽ bị **treo** — đừng tưởng chết, cứ chờ compile xong.

## Mở trên trình duyệt (Playwright MCP)

- Luôn mở **`http://127.0.0.1:3000`**, KHÔNG dùng `localhost:3000` (origin khác → localStorage rỗng → đẩy về `/login`).
- Nếu vẫn ra `/login` (token trong `HRM/e2e/.auth/user.json` hết hạn) → làm mới phiên:
  ```bash
  cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test --project=setup
  ```
  rồi mở lại `http://127.0.0.1:3000`.

## Env client (tham chiếu)

`hrm-client/.env`: `BASE_API_URL=http://localhost:8000`, `SOCKET_URL=http://localhost:8891`, client ở `:3000`. Khớp với API serve ở `:8000`.

## Dừng

```bash
pkill -f "node_modules/.bin/nuxt"              # client
pkill -f "artisan serve --host=0.0.0.0 --port=8000"  # API
brew services stop mysql@8.0                   # MySQL (chỉ dừng nếu muốn; brew services tự bật lại sau reboot)
```
