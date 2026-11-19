# Hướng dẫn deploy TPE SMART AGENT — cổng TPE

> Viết 12/11/2026, cập nhật 12/11 tối sau khi gộp nhánh chat. Code: nhánh `gop_db-tpe-smart-agent` — hrm-api `e598c9a81`, hrm-client `bb6a572a7` (gồm commit sửa lỗi bấm thẻ khi "busy", e2e 25/25). **ĐÃ push origin 12/11 tối, chưa merge `gop_db`**.
> Nhánh agent đã chứa trọn nhánh chat `gop_db-nhom-trao-doi` (api `4749f0165`, client `26cd19d42`) — nhánh chat đã lên `gop_db` trước ⇒ merge agent vào `gop_db` sau, thử `merge-tree` 12/11: **không xung đột**.
> Chỉ deploy cổng **TPE** (`/var/www/tpe`, PHP 8.1). Các cổng khác cập nhật sau.
> Lệnh trên VPS do người deploy tự chạy (Claude không ssh deploy).
> Topology: `ssh -p 2225 erp_tpe@124.158.4.24`; artisan chạy bằng user `erp_tpe`.

## 0. Đã kiểm trước (12/11, máy local)

| Mục | Kết quả |
|---|---|
| composer | **Không đổi** (gọi Claude qua REST bằng Guzzle có sẵn) |
| Cú pháp PHP | 150 file PHP thêm/sửa so với `origin/gop_db` (`Modules/Agent`, 2 service Assign, auth, config): `php -l` **0 lỗi trên cả 7.4 và 8.1** ⇒ cổng 7.4 kéo `gop_db` về không vỡ (kiểm lại 12/11 tối sau gộp chat) |
| Build client | `nuxt build` bản sau gộp chat: **thành công**, có route `/agent`, `/agent/stats` |
| Hiện cho ai | Menu, lối tắt topbar và API đều cần mã `assign.tpe_agent.use` ⇒ **chưa cấp quyền thì không ai thấy** |
| Sửa code chung | `AssignBusinessService` / `AssignJobService` tách `applyListScope` (đã so 40 phép với bản cũ: tập id + thứ tự giống hệt) · `server_node/server.js` thêm kênh `agent` · `config/queue.php` thêm connection `agent` · `Kernel.php` thêm `agent:prune` 03:15 |
| PHPUnit | `Modules/Agent/Tests` **218/218** · `tests/Feature/Auth/LogoutSsoTest` 3/3 (`php -d memory_limit=1G`, 12/11 tối). `Modules/Assign/Tests`: mọi test chat / tab Nhiệm vụ đạt; 241/611 lỗi đều ở test Hợp đồng / kho / xuất hàng / danh bạ — code không thuộc nhánh này, DB local thiếu 8 migration HĐ (chưa đối chiếu với `gop_db` gốc) |

## 1. Chuẩn bị (trước ngày deploy)

1. **API key prod** — làm theo `HUONG-DAN-API-KEY.md`, nhưng tạo **workspace riêng cho prod** (vd `tpe-agent-prod`), đặt spend limit tháng, key riêng. Không dùng lại key dev.
2. Chốt với lãnh đạo:
   - Nhóm dùng thử (role nào được cấp `Dùng TPE SMART AGENT`).
   - Hạn mức câu/ngày theo chức vụ (mặc định **CẤM**: chức vụ chưa cài hạn mức thì không hỏi được).
   - Ngân sách tháng (₫). Để `0` / trống = **không giới hạn ngân sách** (vẫn chịu hạn mức câu/ngày).
   - Người nhận cảnh báo ngân sách (ngưỡng mặc định 80%).
3. Merge `gop_db-tpe-smart-agent` → `gop_db` cho cả 2 repo (khi user báo). ⚠️ Kiểm các script build cổng khác có kéo `gop_db` không — nếu có thì cổng đó cũng nhận 7 migration + module (an toàn vì ẩn theo quyền, nhưng nên biết).

## 2. `.env` của `/var/www/tpe/hrm-api`

Thêm cuối file (không commit):

```
# TPE SMART AGENT
ANTHROPIC_API_KEY=sk-ant-...           # key prod
AGENT_MODEL=claude-haiku-5-5           # BẮT BUỘC đặt — mặc định trong code là sonnet (đắt ~20 lần)
AGENT_EFFORT=low
AGENT_MAX_TOOL_ROUNDS=5
AGENT_FAKE=false
AGENT_PAYROLL_TOOLS=false              # công cụ lương TẮT tới khi có ZDR
# AGENT_CACHE_TTL=1h                   # (từ nhánh gop_db-agent-cache-1h) không đặt = 1h. Đông người hỏi liên tục ⇒ đặt 5m
```

Prompt cache (từ nhánh `gop_db-agent-cache-1h`): mặc định giữ **1 giờ** — ghi cache 2× giá input (5 phút là 1.25×), đọc vẫn 0.1×. Hợp giai đoạn ít người dùng thử, câu hỏi cách nhau > 5 phút. Chi phí lượt hỏi tự tính phần ghi 1 giờ theo 2× input (không cần dòng giá mới). Đổi mức: sửa `AGENT_CACHE_TTL` + `php artisan config:clear` + restart `tpe-agent-worker`.

`QUEUE_CONNECTION=database` trên TPE giữ nguyên. Job Agent luôn đi connection riêng `agent` (bảng `jobs`, queue `agent`) ⇒ **worker hiện có `tpe-worker` KHÔNG chạy job này** — phải thêm worker ở bước 4.

## 3. Kéo code + build

```bash
~/build_tpe.sh
```

Script đã làm: kéo `gop_db` 2 repo · `migrate` · `route:cache` · `permission:catalog-sync` · build client rồi tráo `.nuxt`.

> ⚠️ **`migrate` trong script chạy MỌI migration đang chờ của `gop_db`, không chỉ 7 bản Agent.** `gop_db` hiện còn có migration của feature khác (vd nhóm Hợp đồng `2026_10_27_…` → `2026_11_08_…`: thêm cột/index/bảng `hrm_contracts*`) và 5 migration chat nếu prod chưa nhận. TRƯỚC khi chạy `~/build_tpe.sh`, sau khi kéo code:
> ```bash
> cd /var/www/tpe/hrm-api
> php artisan migrate:status | grep -E "\| No"     # danh sách sẽ chạy
> php artisan migrate --pretend                     # SQL thật sẽ chạy
> ```
> Có bản ngoài danh sách đã duyệt (7 Agent + chat) ⇒ dừng, hỏi chủ feature đó trước.

Kiểm sau khi chạy:

```bash
cd /var/www/tpe/hrm-api
php artisan migrate:status | grep agent          # 7 dòng Ran
php artisan route:list | grep -c "api/v1/agent"  # > 0
```

7 migration (`Modules/Agent/Database/Migrations/`):

| File | Việc làm |
|---|---|
| `…000001_create_agent_conversations_table` | tạo bảng hội thoại |
| `…000002_create_agent_turns_table` | tạo bảng lượt hỏi |
| `…000003_create_agent_tool_calls_table` | tạo bảng lời gọi công cụ |
| `…000004_create_agent_prices_table` | tạo bảng giá + **INSERT 2 dòng** giá sonnet-5-5 / haiku-5-5 (USD/MTok, tỉ giá 26,000) |
| `…000005_create_agent_company_settings_table` | tạo bảng cài đặt ngân sách theo công ty |
| `…000006_create_agent_quota_rules_table` | tạo bảng hạn mức theo chức vụ |
| `…000007_update_agent_company_settings_for_position_rules` | thêm cột `exhausted_position_ids`, đổi enum `on_budget_exhausted` (bảng mới ⇒ chưa có dữ liệu để UPDATE) |

`permission:catalog-sync` thêm 3 quyền (phân hệ Công việc → TPE SMART AGENT):
`Dùng TPE SMART AGENT` · `Xem thống kê sử dụng TPE SMART AGENT` (phạm vi 2/3/4) · `Cài hạn mức TPE SMART AGENT`.

## 4. Worker hàng đợi `agent` (supervisor)

Tạo `/etc/supervisor/conf.d/tpe-agent-worker.conf` (theo khuôn `tpe-worker.conf` có sẵn — mở file đó ra so user, đường dẫn log):

```ini
[program:tpe-agent-worker]
command=php /var/www/tpe/hrm-api/artisan queue:work agent --queue=agent --tries=1 --timeout=150 --max-time=3600
directory=/var/www/tpe/hrm-api
user=erp_tpe
numprocs=2
process_name=%(program_name)s_%(process_num)02d
autostart=true
autorestart=true
stopwaitsecs=160
redirect_stderr=true
stdout_logfile=/var/www/tpe/hrm-api/storage/logs/agent-worker.log
```

```bash
sudo supervisorctl reread && sudo supervisorctl update
sudo supervisorctl status | grep agent      # 2 tiến trình RUNNING
```

- `--timeout=150` > `$timeout=120` của job, `retry_after` connection `agent` = 180 > 150 ⇒ không chạy trùng.
- `numprocs=2`: 2 câu hỏi chạy song song; người thứ 3 chờ vài giây. Tăng khi đông người dùng.
- **Mỗi lần kéo code mới** phải `sudo supervisorctl restart tpe-agent-worker:*` (worker giữ code cũ trong bộ nhớ).

## 5. Socket realtime (`server_node`)

`server.js` đổi: tin có `kind: "agent"` đi kênh `agent` (chữ chạy từng đoạn), không bật chuông thông báo.

0. `server.js` sau gộp có cả 2 kênh `agent` + `chat` ⇒ **1 lần khởi động lại dùng chung** cho Tin nhắn và Agent.
1. Kiểm `server_node` của TPE đang chạy thế nào **trước khi đụng** (không dùng `pm2 list` để dò — sinh daemon):
   ```bash
   ps aux | grep -v grep | grep "server_node/server.js"
   ```
2. Khởi động lại đúng tiến trình đó theo cách nó đang chạy (supervisor / nohup / init.d).
3. Không khởi động lại ⇒ Agent **vẫn trả lời được** nhưng không thấy chữ chạy — câu trả lời hiện khi tải lại trang; tin Agent rơi vào kênh chuông cũ.

## 6. Cấu hình trong app (tài khoản quản trị)

1. `/admin/roles`: cấp `Dùng TPE SMART AGENT` cho role nhóm thử; `Xem thống kê…` + `Cài hạn mức…` cho người quản lý chi phí.
2. Vào **Công việc → Báo cáo → Thống kê TPE SMART AGENT** → nút **Cài hạn mức**:
   - Hạn mức câu/ngày theo nhóm chức vụ / chức vụ (để trống = không giới hạn; không cài = không được dùng).
   - Ngân sách tháng, ngưỡng + người nhận cảnh báo, khi hết ngân sách: chặn hết / chỉ các chức vụ chọn.
3. Nếu muốn ẩn hẳn với user thường trong lúc thử: **Cài đặt phân hệ** thêm key `assign::TPE SMART AGENT` và `assign::Báo cáo::Thống kê TPE SMART AGENT`.

## 7. Kiểm sau deploy

1. Tài khoản đã cấp quyền: thấy icon robot trên topbar + menu Công việc → TPE SMART AGENT.
2. Hỏi 1 câu nhẹ: "Hôm nay tôi có việc gì?" ⇒ chữ chạy dần, có thẻ kết quả, bấm thẻ mở panel.
3. Đối chiếu DB (1 dòng, nhập mật khẩu 1 lần):
   ```bash
   mysql -h 192.168.122.103 -u hrm_tpe -p --table hrm_erp_gop -e "SELECT id,employee_id,status,model,cost_vnd,created_at FROM agent_turns ORDER BY id DESC LIMIT 5; SELECT queue,COUNT(*) FROM jobs GROUP BY queue;"
   ```
   - `status = done`, `model = claude-haiku-5-5`, `cost_vnd` ~10–20 ₫.
   - `jobs` không còn dòng queue `agent` tồn đọng (còn ⇒ worker chưa chạy).
4. Tài khoản KHÔNG có quyền: không thấy menu; gọi `/agent` ⇒ báo không có quyền.
5. Log: `storage/logs/laravel.log` (tìm `[Agent]`) + `storage/logs/agent-worker.log`.
6. Console Anthropic → Usage: có lượt gọi từ key prod.

## 8. Rút lui (nếu cần)

- Tắt nhanh không cần deploy: gỡ quyền `Dùng TPE SMART AGENT` khỏi các role (hoặc xoá hạn mức) ⇒ không ai hỏi được.
- Hoặc xoá `ANTHROPIC_API_KEY` khỏi `.env` + `sudo supervisorctl stop tpe-agent-worker:*`.
- Bảng `agent_*` để nguyên (không ảnh hưởng chức năng khác).

## 9. Vận hành

- `agent:prune` chạy 03:15 hằng ngày (cron `schedule:run` sẵn có) — xoá dữ liệu Agent quá 12 tháng.
- Đổi model / giá: thêm dòng `agent_prices` (model, giá USD/MTok, `effective_from`) rồi đổi `AGENT_MODEL` + `php artisan config:clear` + restart worker.
- Cuối tháng đối soát Console Anthropic → Usage/Cost với màn Thống kê.
- Công cụ lương (`AGENT_PAYROLL_TOOLS=true`) chỉ bật sau khi có ZDR với Anthropic.

## 10. Chọn model + so sánh model (nhánh `gop_db-agent-chon-model`, 15/11/2026)

> **CHẶN — DeepSeek CHƯA từng được gọi bằng key hợp lệ.** Toàn bộ tích hợp DeepSeek (usage keys, vòng thinking, `effort`, giá) mới kiểm bằng fixture/client giả, chưa có phản hồi thật. **Trước khi bất kỳ ai chọn model DeepSeek trên prod**, chạy với key thật: `php artisan agent:eval --models=claude-sonnet-5-5,deepseek-flash` rồi so sánh câu trả lời + chi phí giữa 2 model, và kiểm: (1) các khoá usage (`input_tokens`, `output_tokens`, `cache_read_input_tokens`…) có đủ/đúng, chi phí không ra 0 bất thường; (2) vòng thinking gửi lại nguyên khối được DeepSeek chấp nhận (không lỗi 400 ở lượt gọi tool thứ 2); (3) tham số `output_config.effort` được chấp nhận. Chưa đạt ⇒ để trống `DEEPSEEK_API_KEY`.

Spec: `docs/superpowers/specs/agent-chat/2026-11-15-agent-chon-model-design.md`. Deploy cùng quy trình `~/build_tpe.sh` ở mục 3 (sau khi nhánh đã merge `gop_db` theo lời user).

**a. `.env` của `/var/www/tpe/hrm-api`** — thêm (không commit, KHÔNG dán key vào chat/log):

```
DEEPSEEK_API_KEY=sk-...                # key DeepSeek prod (dạng sk-…); để trống ⇒ 2 model DeepSeek hiện "Chưa khai API key", không chọn được
```

- `AGENT_MODEL` giữ nguyên (`claude-haiku-5-5`) — đây là **mặc định của máy chủ** khi chưa ai chọn model (DB `model = NULL`).
- Sửa `.env` xong: `php artisan config:clear` (build_tpe đã `config:cache`/`route:cache` thì chạy lại đúng lệnh cache script dùng).

**b. 2 migration mới** (`Modules/Agent/Database/Migrations/`) — kiểm bằng `migrate:status` + `migrate --pretend` như mục 3 trước khi chạy:

| File | Việc làm |
|---|---|
| `2026_11_22_000001_add_deepseek_prices_to_agent_prices` | **INSERT 2 dòng** `agent_prices`: `deepseek-flash` (input 0.30 · output 1.20 · cache_read 0.006 USD/MTok) và `deepseek-v4-pro` (1.32 · 3.96 · 0.044), `cache_write = 0`, `effective_from = 2026-11-15`, tỉ giá lấy theo dòng sonnet mới nhất (không có ⇒ 26,000). Không đụng dòng có sẵn. |
| `2026_11_22_000002_create_agent_system_settings_table` | tạo bảng `agent_system_settings` (1 dòng id 1, cột `model` nullable — dòng tự tạo lần lưu đầu) + `agent_system_settings_history` (lịch sử đổi model). Bảng mới, không có UPDATE/DELETE dữ liệu. |

Kiểm sau: `php artisan migrate:status | grep 2026_11_22` ⇒ 2 dòng `Ran`; `SELECT model, effective_from FROM agent_prices WHERE model LIKE 'deepseek%';` ⇒ 2 dòng.

**c. Quyền — KHÔNG có quyền mới.** Dùng lại `Cài hạn mức TPE SMART AGENT`. ⚠️ Ai có quyền này sẽ thấy nút **Cấu hình model** trên màn Thống kê và **đổi được model cho TOÀN hệ thống, mọi công ty** (không phụ thuộc công ty đang làm). Rà lại danh sách vai trò có quyền này trước khi deploy.

**d. Worker hàng đợi** — `~/build_tpe.sh` đã `queue:restart` ⇒ `tpe-agent-worker` nạp code + `.env` mới. Nếu sửa `.env` SAU khi chạy script: `php artisan queue:restart` (hoặc `sudo supervisorctl restart tpe-agent-worker:*`). Model đang chọn được cache 5 phút (`agent.current_model`), lưu ở popup là xoá cache ngay ⇒ lượt hỏi kế tiếp (kể cả qua worker) dùng model mới; lượt đang chạy dở giữ model lúc bắt đầu.

**e. Kiểm sau deploy**

1. Tài khoản có `Cài hạn mức…`: **Công việc → Báo cáo → Thống kê TPE SMART AGENT** ⇒ nút **Cấu hình model** ⇒ popup có "Dùng mặc định của máy chủ (Claude Haiku 5.5)" + 4 model kèm giá; 2 model DeepSeek KHÔNG báo "Chưa khai API key" (báo ⇒ thiếu `DEEPSEEK_API_KEY` / chưa `config:clear`).
2. Muốn thử DeepSeek: chọn → Lưu → Xác nhận ⇒ hỏi 1 câu nhẹ ⇒ `SELECT id, model, cost_vnd FROM agent_turns ORDER BY id DESC LIMIT 3;` có `model = deepseek-flash`. Xong đổi lại "mặc định" nếu chưa định dùng chính thức. Nút **Lịch sử** trong popup ghi ai đổi, lúc nào.
3. Ô lọc model trên màn Thống kê + bảng "Theo model": chọn 1 model ⇒ khối Chi phí ghi "Chỉ tính model đang lọc", ẩn ngân sách / dự báo.
4. Tài khoản chỉ có quyền xem thống kê: không thấy nút **Cấu hình model**.

**f. Rút lui**: chọn lại "Dùng mặc định của máy chủ" trong popup (không cần deploy). Gỡ hẳn DeepSeek: xoá `DEEPSEEK_API_KEY` + `config:clear` + `queue:restart` — model đang chọn mất key thì máy chủ tự rơi về `AGENT_MODEL`, không làm lỗi câu hỏi. 2 bảng mới + 2 dòng giá để nguyên.
