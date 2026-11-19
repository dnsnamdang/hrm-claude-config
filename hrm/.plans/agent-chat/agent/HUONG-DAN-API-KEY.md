# Tạo API key Claude cho TPE SMART AGENT (tài khoản công ty DNS MEDIA — dùng DEV)

> 11/11/2026. Giao diện Console có thể đổi tên nút đôi chút; làm theo ý từng bước.
> KHÔNG dán key vào chat / Redmine / git. Key chỉ nằm trong `.env` trên máy / server.

## A. Tạo tài khoản + tổ chức
1. Vào **https://platform.claude.com** (Claude Console — tên cũ console.anthropic.com) → **Sign up** bằng email công ty (vd `dev@dnsmedia...`), không dùng email cá nhân.
2. Xác minh email → đặt tên **Organization**: `DNS MEDIA`. Điền thông tin công ty khi được hỏi (mục đích: tích hợp trợ lý AI vào phần mềm ERP).
3. **Settings → Members**: mời thêm người quản trị thứ 2 (tránh mất quyền khi 1 người nghỉ). Vai trò: Admin cho người quản lý chi phí, Developer cho người code.

## B. Thanh toán + giới hạn chi tiêu
4. **Settings → Billing**: thêm thẻ / thông tin thanh toán của công ty → **mua credit** khoảng **$10–20** để dev.
5. Tắt tự động nạp (auto-reload) trong giai đoạn dev, hoặc đặt mức nạp nhỏ.
6. **Settings → Limits**: xem hạng (tier) hiện tại — tài khoản mới giới hạn số lần gọi / phút thấp, đủ cho dev.

## C. Workspace + key
7. **Settings → Workspaces → Create workspace**: tên `tpe-agent-dev`.
8. Trong workspace đó đặt **spend limit tháng** (vd `$20`) ⇒ code chạy lỗi lặp cũng không vượt số này.
9. **API Keys → Create Key** → chọn workspace `tpe-agent-dev` → tên `hrm-dev-local` → **Create**.
10. **Copy key ngay** (dạng `sk-ant-…`) — Console chỉ hiện 1 lần. Mất thì xoá key đó và tạo key mới.

## D. Gắn vào dự án (máy dev)
11. Mở `.env` của hrm-api đang chạy Agent (worktree): `websites/wt-tpe-agent/hrm-api/.env` — thêm cuối file:
    ```
    ANTHROPIC_API_KEY=sk-ant-...
    AGENT_MODEL=claude-sonnet-5-5
    ```
    (`.env` không commit lên git.)
12. Kiểm key chạy được — lệnh này chỉ liệt kê model, **không tốn tiền**, không in key ra màn hình:
    ```bash
    cd ~/Documents/DNSMEDIA/websites/wt-tpe-agent/hrm-api
    KEY=$(grep '^ANTHROPIC_API_KEY=' .env | cut -d= -f2-)
    curl -s https://api.anthropic.com/v1/models -H "x-api-key: $KEY" -H "anthropic-version: 2026-10-21" | head -c 300; echo
    ```
    Ra danh sách có `claude-sonnet-5-5` là đúng. Ra `authentication_error` ⇒ copy sai key; `permission_error` / `billing` ⇒ chưa nạp credit.
13. Báo Claude "đã có key" (không gửi key) để chạy thử 1 câu (~200 ₫).

## E. Lưu ý an toàn
- Mỗi môi trường 1 key riêng (dev local / dev server / prod). Key lộ ⇒ **API Keys → Disable/Delete** ngay rồi tạo key mới.
- Tài khoản DEV chưa có ZDR ⇒ chỉ thử trên DB local, **không hỏi về lương thật của nhân viên** qua key này.
- Prod sau này: workspace / tổ chức riêng (Tân Phát hoặc DNS MEDIA đứng tên — chốt sau), xin **ZDR** qua Anthropic sales trước khi bật công cụ lương.
- Cuối tháng đối soát: Console → **Usage / Cost** (theo key, theo model) so với màn Thống kê của Agent.
