# Agent — Chọn model + so sánh model — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Người có quyền chọn trên giao diện model Agent dùng cho toàn hệ thống (Claude / DeepSeek…), xem thống kê theo model, và so sánh nhiều model bằng lệnh `agent:eval --models`.

**Architecture:** Danh mục model khai trong `Modules/Agent/Config/config.php` (key đọc env trong config). Model đang dùng lưu ở bảng 1 dòng `agent_system_settings`, đọc qua `AgentModelResolver` (cache Redis 300s, xoá khi lưu). `HttpClaudeClient` nhận base_url/key/model từ resolver — DeepSeek dùng cổng tương thích Anthropic nên không cần client mới.

**Tech Stack:** Laravel 8 (PHP 8.1 trên TPE), nwidart modules, maatwebsite/excel, Nuxt 2 / Vue 2, V2Base components, Playwright e2e.

**Spec:** `docs/superpowers/specs/agent-chat/2026-11-15-agent-chon-model-design.md` (tóm tắt: `design.md` cùng thư mục).

## Global Constraints

- Nhánh `gop_db-agent-chon-model` tách từ `origin/gop_db`, cả `hrm-api` lẫn `hrm-client`, worktree `websites/wt-tpe-agent` (đổi nhánh chỉ khi `git status` sạch). **Đụng source / chạy migration phải hỏi user riêng** (nêu tên từng migration, DB `db_gop_6_11`).
- Danh mục model (id → label, provider, base_url): `claude-sonnet-5-5` Claude Sonnet 5.5 / Anthropic / `https://api.anthropic.com` · `claude-haiku-5-5` Claude Haiku 5.5 / Anthropic / như trên · `deepseek-flash` DeepSeek Flash / DeepSeek / `https://api.deepseek.com/anthropic` · `deepseek-v4-pro` DeepSeek V4 Pro / DeepSeek / như trên. Key: `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY` — đọc `env()` CHỈ trong file config.
- `AGENT_MODEL` (env) = model mặc định khi DB NULL. NULL hiển thị "Dùng mặc định của máy chủ".
- "Dùng được" = có trong danh mục + key khác rỗng + có `agent_prices` hiệu lực hôm nay. Lý do không dùng được: `Chưa khai API key` / `Chưa có bảng giá`.
- API key KHÔNG bao giờ xuất hiện trong response / log / FE.
- Giá DeepSeek (USD / 1M token, giờ cao điểm, cache_write = 0): flash 0.30 / output 1.20 / cache_read 0.006 · v4-pro 1.32 / 3.96 / 0.044 — **xác minh lại https://api-docs.deepseek.com/quick_start/pricing trước khi viết migration** (thứ tự cột suy luận).
- Quyền: **dùng lại quyền có sẵn `assign.tpe_agent_cai_dat.manage` (Cài hạn mức TPE SMART AGENT)** — user chốt 15/11, KHÔNG tạo mã mới, KHÔNG sửa Catalog, KHÔNG chạy `permission:catalog-sync`. Nút hiện theo quyền này, KHÔNG phụ thuộc `sameCompany` (cài đặt toàn hệ thống). Không bypass Super Admin.
- Model mới extends `App\Models\BaseModel`; FormRequest chỉ khai `rules()`; số hiển thị `en-US`; chữ mô tả xám `#6b7280`, không đỏ.
- PHPUnit: `php -d memory_limit=1G vendor/bin/phpunit Modules/Agent/Tests`. ⚠️ `AgentEvalCommandTest` xoá mọi `storage/app/agent-eval-*.csv` — chép CSV thật ra ngoài trước khi chạy.
- E2E Agent cần :8070 `AGENT_FAKE=1` ⇒ hỏi user trước khi restart :8070.

## Review Focus

1. **Đổi model khi đang có lượt chạy dở** — lượt đó vẫn dùng model đã đọc lúc bắt đầu cho mọi vòng gọi công cụ, `agent_turns.model` + giá khớp model đó (Task 3: test đổi DB giữa 2 vòng FakeClient).
2. **Model đang chọn sau đó mất key / bảng giá** (gỡ `DEEPSEEK_API_KEY` khỏi env) — resolver rơi về mặc định `AGENT_MODEL`, không làm mọi câu hỏi lỗi (Task 2: test).
3. **PUT gửi model ngoài danh mục / chưa dùng được / chuỗi rỗng** — 422 có lý do; chuỗi rỗng coi như NULL hay 422 phải nhất quán: rỗng ⇒ 422, chỉ `null` là mặc định (Task 4: test).
4. **Queue worker giữ cache cũ** — lưu xong lượt kế tiếp (kể cả qua worker) dùng model mới: khoá cache bị xoá trong cùng request lưu (Task 4: test `Cache::has` false sau PUT).
5. **Lọc model trên tháng có lượt `model` NULL (quota/error cũ)** — không lỗi SQL, lượt NULL không thuộc model nào, khối ngân sách ẩn (Task 6: test).

---

### Task 1: Danh mục model trong config + giá DeepSeek

**Files:**
- Modify: `hrm-api/Modules/Agent/Config/config.php`
- Create: `hrm-api/Modules/Agent/Database/Migrations/2026_11_22_000001_add_deepseek_prices_to_agent_prices.php`
- Test: `hrm-api/Modules/Agent/Tests/Unit/AgentPricingServiceTest.php` (thêm ca)

**Interfaces:**
- Produces: `config('agent.models')` = `[id => ['label','provider','base_url','api_key','effort' => bool]]`; `config('agent.model')` giữ nguyên (mặc định).

- [x] Step 1: Ca `test_gia_deepseek_flash_cache_write_bang_0` — `cost('deepseek-flash', ['input_tokens'=>1_000_000,'output_tokens'=>1_000_000,'cache_read_tokens'=>1_000_000,'cache_write_tokens'=>0])['usd']` = 0.30+1.20+0.006 = `1.506`. Chạy ⇒ FAIL "Chưa có bảng giá".
- [x] Step 2: Migration chèn 2 dòng (`effective_from` = `2026-11-15`, `usd_vnd` copy từ dòng `claude-sonnet-5-5` mới nhất); `down()` xoá đúng 2 model đó. Thêm `models` vào config theo Global Constraints (`api_key => env('ANTHROPIC_API_KEY')` / `env('DEEPSEEK_API_KEY')`).
- [x] Step 3: Chạy test (DB test có migration) ⇒ PASS.
- [x] Step 4: Commit `feat(agent): danh mục model + bảng giá DeepSeek`.

### Task 2: `agent_system_settings` + `AgentModelResolver`

**Files:**
- Create: migration `2026_11_22_000002_create_agent_system_settings_table.php` (bảng `agent_system_settings`: id, model string(100) nullable, created_by, updated_by, timestamps; + bảng `agent_system_settings_history` theo khuôn bảng log của adapter SettingHistory mẫu — xem skill `entity-history` mục màn cấu hình và `app/Services/SettingHistory/Adapters/HumanSettingAdapter.php`)
- Create: `Modules/Agent/Entities/AgentSystemSetting.php` (extends BaseModel)
- Create: `Modules/Agent/Services/AgentModelResolver.php`
- Test: `Modules/Agent/Tests/Unit/AgentModelResolverTest.php`

**Interfaces:**
- Produces:
  - `AgentModelResolver::CACHE_KEY = 'agent.current_model'`
  - `current(): array` → `['model'=>string,'base_url'=>string,'api_key'=>string,'effort'=>bool]`
  - `options(): array` → list `['id','label','provider','usable'=>bool,'reason'=>?string,'price'=>['input','output','cache_read']|null]`
  - `selected(): ?string` (giá trị DB thô), `defaultModel(): string`, `isUsable(string $id): bool`, `reason(string $id): ?string`, `forget(): void`

- [x] Step 1: Test — (a) DB NULL ⇒ `current()['model']` = `config('agent.model')`; (b) DB `deepseek-flash` có key ⇒ trả base_url DeepSeek; (c) DB `deepseek-flash` nhưng `config(['agent.models.deepseek-flash.api_key'=>null])` ⇒ rơi về mặc định (Review Focus 2); (d) `options()` model thiếu key có `reason` = `Chưa khai API key`, thiếu giá = `Chưa có bảng giá`, và không mảng con nào chứa khoá `api_key`; (e) gọi `current()` 2 lần chỉ 1 truy vấn DB (đếm `DB::getQueryLog`).
- [x] Step 2: Chạy ⇒ FAIL.
- [x] Step 3: Implement. Cache bọc **id model** đã chọn (không cache key); kiểm "dùng được" mỗi lần từ config + 1 truy vấn giá cũng cache cùng khoá (TTL 300).
- [x] Step 4: PASS. Commit `feat(agent): AgentModelResolver + bảng agent_system_settings`.

### Task 3: Client + runner dùng resolver

**Files:**
- Modify: `Modules/Agent/Claude/HttpClaudeClient.php`, `Modules/Agent/Claude/ClaudeClient.php` (docblock `$options['model_cfg']`), `Modules/Agent/Services/AgentRunner.php:43` và chỗ gọi `$this->client->message`
- Test: `Modules/Agent/Tests/Unit/HttpClaudeClientTest.php`, `Modules/Agent/Tests/Feature/AgentRunnerTest.php`

**Interfaces:**
- Consumes: `AgentModelResolver::current()`.
- Produces: `ClaudeClient::message(..., array $options)` nhận thêm `$options['model_cfg']` (mảng như `current()`); thiếu thì client tự gọi resolver (giữ tương thích test cũ).

- [x] Step 1: Test client — với `model_cfg` DeepSeek: request tới `https://api.deepseek.com/anthropic/v1/messages`, header `x-api-key` = key DeepSeek, body `model` = `deepseek-flash`; `effort=false` ⇒ body không có `output_config`. Test SSE: khung `data: {"error":{"message":"timeout"}}` (không `type`) ⇒ `RuntimeException` chứa `timeout`.
- [x] Step 2: Test runner (Review Focus 1) — DB chọn `claude-sonnet-5-5`; FakeClient kịch bản 2 vòng (tool rồi text), callback giữa vòng 1 đổi DB sang `deepseek-flash` + `forget()`; khẳng định cả 2 lần gọi nhận cùng `model_cfg['model']` = `claude-sonnet-5-5`, `agent_turns.model` = `claude-sonnet-5-5`.
- [x] Step 3: FAIL ⇒ implement (runner gọi `current()` 1 lần đầu `run()`, truyền vào mọi `message()`, ghi `model` + tính giá theo nó; client ghép `rtrim(base_url,'/') . '/v1/messages'`).
- [x] Step 4: Chạy toàn `Modules/Agent/Tests` ⇒ PASS (sửa test cũ nếu chỉ lệch do URL/config). Commit `feat(agent): client + runner đọc model từ resolver, hỗ trợ DeepSeek`.

### Task 4: API `v1/agent/model` + lịch sử

**Files:**
- Modify: `Modules/Agent/Routes/api.php`
- Create: `Modules/Agent/Http/Controllers/Api/V1/AgentModelController.php`, `Modules/Agent/Http/Requests/SaveAgentModelRequest.php`
- Create: `app/Services/SettingHistory/Adapters/AgentSystemSettingAdapter.php` (tên theo quy ước tên của `SettingHistoryService::adapter()` — đọc file đó để lấy đúng quy ước + `type` string)
- Test: `Modules/Agent/Tests/Feature/AgentModelApiTest.php`

**Interfaces:**
- Consumes: resolver (Task 2).
- Produces: `GET v1/agent/model` → `data: {selected: ?string, current: string, default_model: string, default_label: string, options: [...]}`; `PUT v1/agent/model` body `{model: ?string}` → cùng payload; lịch sử qua `setting-histories/{type}/1`.

- [x] Step 1: Test — không quyền ⇒ 403 cả GET/PUT; có quyền GET không chứa chuỗi key test (`assertDontSee`); PUT `deepseek-flash` (có key) ⇒ 200, DB lưu, `Cache::has(CACHE_KEY)` false; PUT `null` ⇒ lưu NULL; PUT `''`, `gpt-9`, model thiếu key ⇒ 422 (Review Focus 3); sau PUT có 1 dòng lịch sử cũ → mới ("Mặc định máy chủ" khi NULL).
- [x] Step 2: FAIL ⇒ implement. Route group `checkPermission:assign.tpe_agent_cai_dat.manage`. Rule: `['present','nullable','string', Rule::in(array_keys(config('agent.models')))]` + closure kiểm `isUsable` trả `reason`.
- [x] Step 3: PASS. Commit `feat(agent): API chọn model hệ thống`.

### Task 5: Popup "Cấu hình model" (hrm-client)

**Files:**
- Create: `hrm-client/components/agent/AgentModelModal.vue` (dựng trên `components/modal/V2BaseModal.vue`; xác nhận bằng `this.$confirm`; lịch sử bằng `SettingHistoryModal` — copy cách gọi từ một màn cấu hình đang dùng nó, grep `SettingHistoryModal`)
- Modify: `hrm-client/pages/agent/stats.vue` (nút cạnh `agent-stats-quota-btn` dòng ~22, dùng lại cờ `canManage` sẵn có (quyền `assign.tpe_agent_cai_dat.manage`) nhưng KHÔNG kèm điều kiện `sameCompany`)

**Interfaces:**
- Consumes: API Task 4.

- [x] Step 1: Đọc skill `modal-popup`, `button-convention`, `unsaved-changes` (popup có thay đổi chưa lưu ⇒ `unsavedModalMixin`), `segmented-control` nếu chọn kiểu thẻ.
- [x] Step 2: Popup: lựa chọn đầu "Dùng mặc định của máy chủ (<default_label>)"; mỗi model 1 thẻ chọn: tên · nhà cung cấp · giá input/output USD/1M token (`toLocaleString('en-US')`) · lý do không dùng được (xám, thẻ không chọn được); dưới model provider ≠ Anthropic dòng xám "Câu hỏi và dữ liệu tra cứu sẽ gửi tới máy chủ của <provider>."; dòng "Đang dùng: …". Footer V2Footer/V2BaseModal: Lưu (confirm "Đổi model cho TOÀN hệ thống?") · Lịch sử · Đóng. Lưu xong toast + đóng. `data-testid`: `agent-model-btn`, `agent-model-modal`, `agent-model-option-<id>`, `agent-model-save`.
- [x] Step 3: Kiểm bằng Playwright MCP trên `http://127.0.0.1:3070/agent/stats`: đo nút cách nút kề 12px, thẻ không dùng được không bấm được, lưu đổi được, mở lại thấy giá trị mới. Commit `feat(agent): popup Cấu hình model trên màn Thống kê`.

### Task 6: Thống kê theo model

**Files:**
- Modify: `Modules/Agent/Services/AgentStatsService.php` (`base()` nhận `$ctx['models']`; `budget()` trả null khi lọc model; `filterOptions()` thêm `models`; hàm mới `byModel(array $ctx): array`), `Modules/Agent/Http/Controllers/Api/V1/AgentStatsController.php` (`ctx()` đọc `models[]`; route `GET v1/agent/stats/models`), `Modules/Agent/Routes/api.php`, `Modules/Agent/Exports/AgentStatsExport.php` (cột Model nếu có danh sách lượt)
- Modify: `hrm-client/pages/agent/stats.vue` (bộ lọc Model chọn nhiều + khối bảng "Theo model")
- Test: `Modules/Agent/Tests/Feature/AgentStatsApiTest.php`

**Interfaces:**
- Produces: `byModel($ctx)` → list `['model','label','turns','cost_vnd','avg_cost_vnd','avg_ms','error_rate','na_rate','avg_calls']` (rate là %, 1 số lẻ; `label` từ `config('agent.models')`, không có thì = id); `filterOptions()['models']` = `[{id,label}]` model có lượt trong tháng (bỏ NULL).

- [x] Step 1: Test — seed lượt 2 model + 1 lượt quota `model` NULL: `models` endpoint ra đúng 2 dòng, số khớp; `summary?models[]=deepseek-flash` ⇒ `budget` null và `total_turns` chỉ đếm model đó; không lỗi với lượt NULL (Review Focus 5). Kiểm cột `model` của lượt quota/error thật sự NULL ở luồng tạo lượt (`AgentQuotaService` / controller `ask`) và ghi kết quả vào checkpoint.
- [x] Step 2: FAIL ⇒ implement (1 truy vấn `GROUP BY model`; EXPLAIN — thêm index chỉ khi cần, nếu thêm thì là migration mới phải hỏi).
- [x] Step 3: FE: bộ lọc theo khuôn bộ lọc đang có trên màn (floating, không placeholder trùng nhãn); bảng theo khuôn bảng khác cùng màn; khi lọc model ẩn khối ngân sách (BE đã trả null). Kiểm Playwright MCP.
- [x] Step 4: PASS. Commit `feat(agent): thống kê theo model`.

### Task 7: `agent:eval --models` xuất Excel so sánh

**Files:**
- Modify: `Modules/Agent/Console/AgentEvalCommand.php`
- Create: `Modules/Agent/Exports/AgentEvalCompareExport.php` (skill `export-excel`: ô số là số thật + numFmt)
- Test: `Modules/Agent/Tests/Feature/AgentEvalCommandTest.php`

**Interfaces:**
- Consumes: `AgentModelResolver::isUsable/reason`, `$options['model_cfg']` (Task 3) — eval ép model bằng cách truyền cfg của model đang chạy (thêm tham số tuỳ chọn `?array $modelCfg` vào `AgentRunner::run`, mặc định `current()`).

- [x] Step 1: Test với `--fake --models=claude-sonnet-5-5,deepseek-flash --limit=2`: exit 0, tạo đúng 1 file `storage/app/agent-eval-compare-*.xlsx`, có 2 dòng câu hỏi + nhóm cột cho mỗi model + dòng tổng mỗi model; model không dùng được ⇒ exit 1 trước khi chạy câu nào; không còn lượt/hội thoại `[eval]` trong DB sau khi chạy. Test xoá file xlsx nó tạo (không xoá CSV thật).
- [x] Step 2: FAIL ⇒ implement. Một model lỗi ở 1 câu ⇒ ghi lỗi vào ô Câu trả lời, chạy tiếp. `--model` cũ giữ nguyên hành vi (CSV).
- [x] Step 3: PASS. Commit `feat(agent): agent:eval --models xuất Excel so sánh`.

### Task 8: E2E + tài liệu + kiểm tổng

**Files:**
- Create/Modify: `HRM/e2e/tests/agent-model.spec.ts` (sửa repo e2e phải hỏi user) — ca có quyền (mở popup, chọn mặc định ↔ model khác, lịch sử) + không quyền (không thấy nút) + lọc model ẩn ngân sách
- Modify: `.plans/agent-chat/agent/HUONG-DAN-DEPLOY.md` (khai `DEEPSEEK_API_KEY`, migration 2026_11_22_000001/000002, không có quyền mới — người có quyền Cài hạn mức đổi được model toàn hệ thống), `.plans/agent-chat/README.md`

- [x] Step 1: Chạy toàn `Modules/Agent/Tests` + bộ e2e Agent (`agent-chat`, `agent-chat-pin`, `agent-stats` nếu có, `agent-model`) — đọc dòng tổng kết.
- [x] Step 2: Chạy thử thật (khi user đưa key DeepSeek vào `.env` worktree): `agent:eval --models=claude-sonnet-5-5,deepseek-flash` trên DB local, gửi file Excel cho user.
- [x] Step 3: Ghi checkpoint, cập nhật STATUS.

---

### Checkpoint — 15/11/2026 (code xong)
Vừa hoàn thành: 8 task (subagent mỗi task + review) + review cuối toàn nhánh + 1 đợt sửa. Nhánh `gop_db-agent-chon-model` CHƯA push:
- hrm-api `a5290628e..fd56a5e8b` (10 commit) · hrm-client `85a2a590d..26b1e9255` (4 commit).
- Migration ĐÃ chạy db_gop_6_11: `2026_11_22_000001_add_deepseek_prices_to_agent_prices`, `2026_11_22_000002_create_agent_system_settings_table`.
- Kiểm: PHPUnit Modules/Agent/Tests 260 OK · e2e `agent-model.spec.ts` 4/4 (mới, HRM/e2e) · agent-stats 14/17 — 3 ca đỏ CÓ TỪ TRƯỚC (ngân sách công ty 1 làm ô cao 103.6 · kịch bản stub hỏng ngày Chủ nhật · tooltip vượt 3.1px — chạy trên client gốc 85a2a590d đỏ y hệt) · agent-chat / agent-chat-pin chưa chạy được (socket :8896 tắt).
- Quyết định giữa chừng: dùng lại quyền `assign.tpe_agent_cai_dat.manage` (user) · nút Lưu popup ẩn khi chưa đổi · lọc model ẩn cả dự báo · `--fake` không đòi key/giá.
Đang làm dở: —
Bước tiếp theo: (1) user đưa key DeepSeek thật (`sk-…`) ⇒ thay dòng `DEEPSEEK_API_KEY` trong `.env` wt-tpe-agent ⇒ `agent:eval --models=claude-sonnet-5-5,deepseek-flash` ⇒ gửi Excel so sánh; (2) chạy lại agent-chat/agent-chat-pin khi bật socket :8896; (3) user báo merge ⇒ đẩy lên gop_db; deploy theo HUONG-DAN-DEPLOY §10.
Blocked: key `oc_sk_…` user đưa 15/11 bị DeepSeek trả 401 invalid.

### Checkpoint — 15/11/2026 ~12:00 (wrap up)
Vừa hoàn thành:
- Key DeepSeek thật (user cập nhật `.env` wt-tpe-agent dòng 85) chạy được. Thêm `agent:eval --only=` (api `12986fddf`, test eval 9/9).
- So sánh thật 50 câu chọn lọc (36 câu ok — mỗi công cụ 1 câu · 6 deny · 4 na · 4 ask; danh sách STT ở scratchpad phiên `eval-pick50.txt`):
  Sonnet 5.5: đúng công cụ 98% · đúng kind 98% · 239.82 ₫/câu · 4.0 s · TB 206 ký tự.
  DeepSeek Flash: đúng công cụ 100% · đúng kind 98% · 29.65 ₫/câu (giá cao điểm; CN = thấp điểm ⇒ thật ≈ ½) · 3.3 s · TB 145 ký tự.
  Lệch duy nhất câu 14 (biên bản họp BGĐ — mong deny, cả 2 hỏi lại, không lộ dữ liệu). DeepSeek xưng "mình", Sonnet "tôi".
  File: `wt-tpe-agent/hrm-api/storage/app/agent-eval-compare-20261115-114405.xlsx`.
- E2E: agent-model 4/4 · agent-chat-pin 6/6 · agent-stats 14/17 (3 ca đỏ có từ trước) · agent-chat chạy lại sau eval (lần trước đỏ do eval chạy song song cùng NV 13 chen hội thoại) — kết quả lần chạy cuối xem log scratchpad `e2e-agent-chat.log`.
- Đã dừng lượt 193 câu sau ~3 phút (tốn vài nghìn ₫, không ghi), dọn 1 hội thoại `[eval]` dở.
Đang làm dở: —
Bước tiếp theo:
1. User đọc Excel so sánh, quyết có chuyển Agent sang DeepSeek Flash không.
2. Nếu chuyển: thêm quy định xưng hô ("tôi") vào AgentPrompt để giọng thống nhất giữa các model (hỏi trước khi sửa).
3. User báo merge ⇒ đưa nhánh `gop_db-agent-chon-model` (api `12986fddf` · client `26b1e9255`) lên gop_db ⇒ deploy theo HUONG-DAN-DEPLOY §10 (khai DEEPSEEK_API_KEY prod, 2 migration).
4. Tắt server wt-tpe-agent khi không cần: :8070 (AGENT_FAKE=1) · :3070 (nuxt dev) · :8896 (socket).
Blocked: —
Lưu ý: key DeepSeek đã dán trong chat ⇒ nên đổi key; key cũ `oc_sk_…` cũng đã lộ trong chat.

### Checkpoint — 15/11/2026 ~14:00 (wrap up)
Vừa hoàn thành:
- So sánh ĐÚNG cặp (user đang dùng Haiku): cùng 50 câu — Haiku 5.5: 100% công cụ · 100% kind · 20.91 ₫/câu · 3.4 s; DeepSeek Flash: 98% · 98% · 17.28 ₫/câu (cao điểm, cache ấm; thấp điểm ≈ 8.6) · 2.9 s. Lệch duy nhất câu 14 (DS hỏi lại thay vì chặn quyền). Excel `wt-tpe-agent/hrm-api/storage/app/agent-eval-compare-20261115-125550.xlsx`. Đề xuất: giữ Haiku (chênh ~4–12 nghìn ₫/1.000 câu, không gửi dữ liệu sang TQ).
- Popup: bỏ dòng cảnh báo "gửi tới máy chủ…" (client `b647096c6`) · bỏ thẻ "Dùng mặc định của máy chủ" trùng model mặc định, thẻ model `AGENT_MODEL` có nhãn "Mặc định", chọn thẻ nào lưu đúng id (client `960d04154`). e2e agent-model 4/4 (đã sửa theo popup mới). Spec ghi 2 quyết định.
- Tra giá: DeepSeek chỉ còn flash/v4-pro (flash rẻ nhất); Claude rẻ nhất là Haiku 5.5; OpenAI gpt-6-luna = giá Haiku, gpt-5-nano rẻ hơn ~½ phần đọc nhưng đời cũ + OpenAI KHÔNG có cổng tương thích Anthropic (phải viết client riêng) ⇒ đề xuất không làm.
- :8070 đã chuyển sang chế độ trả lời THẬT (không AGENT_FAKE) cho user thử.
Đang làm dở: —
Bước tiếp theo:
1. User quyết model dùng (đề xuất giữ Haiku) + có làm "Văn phong trả lời" không (cách 1 sửa AgentPrompt / cách 2 ô cấu hình trong popup) — chưa trả lời.
2. Ca agent-chat.spec "bấm nhiệm vụ / vấn đề / meeting / nhắc việc trên thẻ…" đỏ lúc chạy song song eval — chạy lại riêng để chốt (log cũ đã mất).
3. User báo merge ⇒ nhánh `gop_db-agent-chon-model` (api `12986fddf` · client `960d04154`) lên gop_db ⇒ deploy HUONG-DAN-DEPLOY §10.
4. Tắt :8070 / :3070 / :8896 wt-tpe-agent khi user thử xong.
Blocked: —
Ghi chú: key DeepSeek đã dán trong chat ⇒ nên đổi key.

### Checkpoint — 15/11/2026 ~16:30
Vừa hoàn thành:
- Giữ Haiku 5.5 mặc định (user chốt). Thêm luật 11 giọng văn "nhân viên văn phòng báo cáo công việc" (xưng em, gọi anh/chị, mở "Dạ,", kết bằng đề xuất có "ạ") — api `3fefb0545`. Eval 50 câu Haiku: 98%/98% (câu 14 lệch như mọi model), 22.06 ₫/câu, TB 239 ký tự (trước 194). Excel `agent-eval-compare-20261115-160327.xlsx`.
- AgentModelApiTest đếm lịch sử theo mốc id (DB thật có 3 dòng lịch sử do user tự đổi model 13:24–13:35). PHPUnit Agent 262/262.
- Ca e2e agent-chat "bấm nhiệm vụ / vấn đề / meeting / nhắc việc trên thẻ" đỏ 3 kiểu khác nhau trên nuxt dev — user tự thử trên giao diện 15/11 xác nhận các thẻ mở panel bình thường ⇒ lỗi môi trường (nuxt dev + chạy riêng nhóm ca), nhánh không đụng file khung chat. Muốn xanh hẳn: chạy cả bộ trên bản build `nuxt start`.
Bước tiếp theo: user báo merge ⇒ `gop_db-agent-chon-model` (api `3fefb0545` · client `960d04154`) lên gop_db ⇒ deploy §10 · tắt :8070/:3070/:8896 khi user thử xong.

### ĐÃ DEPLOY TPE — 15/11/2026 (api `3fefb0545` · client `960d04154`)
- Đã lên origin/gop_db (fast-forward; worktree hrm-api từng ở detached HEAD — đã gắn lại nhánh). build_tpe EXIT 0, Migrated `2026_11_22_000001` + `2026_11_22_000002`, không còn migration chờ, site 200. Kéo theo GĐ14 popup hồ sơ (không migration).
- Prod: `AGENT_MODEL=claude-haiku-5-5`, CHƯA khai `DEEPSEEK_API_KEY` ⇒ popup hiện DeepSeek "Chưa khai API key" (không chọn được) — đúng chủ ý giữ Haiku. Bảng `agent_system_settings` rỗng (= dùng mặc định Haiku).
- Giọng văn "nhân viên văn phòng báo cáo" đã có hiệu lực trên prod.
