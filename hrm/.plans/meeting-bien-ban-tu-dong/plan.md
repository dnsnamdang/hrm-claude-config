# Meeting — AI tạo biên bản (thử nghiệm) — Kế hoạch triển khai

> **Cho người thực hiện:** dùng superpowers:executing-plans, đánh `[x]` từng bước.
> CHƯA được phép code: mỗi phần đụng source / DB / VPS phải có câu "làm" riêng của user (CLAUDE.md gốc).

**Mục tiêu:** tab "AI tạo biên bản" ở màn chi tiết Meeting: ghi âm/tải file → Whisper (CPU VPS) chuyển chữ
→ Claude sinh Nội dung chi tiết / Tóm tắt / Kết luận / Gợi ý nhiệm vụ → user sửa, chọn, gửi nhiệm vụ.

**Kiến trúc:** Laravel lưu file + bản ghi `meeting_ai_minutes`, xếp job vào queue riêng `meeting_ai`
(1 worker); job gọi script Python faster-whisper. 4 phần sinh bằng job queue `agent` gọi
`Modules\Agent\Claude\ClaudeClient::message()` với `model_cfg` cố định Claude. FE hỏi trạng thái mỗi 15 s.

**Tech:** Laravel 8 / PHP 7.4 (dev) · Nuxt 2 · faster-whisper 1.2.1 + ffmpeg · Claude Sonnet qua REST.

**Spec:** `HRM/.plans/meeting-bien-ban-tu-dong/design.md`

**Nhánh:** `meeting-ai-bien-ban` tách từ `origin/gop_db` ở CẢ `hrm-api` và `hrm-client`, worktree riêng
(`HRM/wt-meeting-ai-api`, `HRM/wt-meeting-ai-client`). Merge khi user báo. Không commit hộ — user tự báo.

## Ràng buộc chung

- Quyền: `Meeting::canEdit()` (người tạo / chủ trì) VÀ **theo Cài đặt phân hệ của Meeting** (user chốt 20/11):
  tab ẩn khi phân hệ `meeting` hoặc mục menu "Tổng hợp meeting" bị tắt — key
  `buildSubsystemKey('meeting')` / `buildMenuKey('meeting', ['Tổng hợp meeting'])`, đọc getter
  `effectiveMenuHiddenKeys` (NV "xem đầy đủ" bỏ qua). Copy khuôn `utils/agentAccess.js` → `utils/meetingAiAccess.js`.
  KHÔNG có cờ .env bật/tắt. BE: rà xem Agent có kiểm menu ẩn ở BE không (middleware menu) — có thì áp y vậy.
  ⚠️ Hệ quả: code lên cổng nào thì tab hiện cho mọi người tạo/chủ trì ở cổng đó ⇒ cổng chưa cài Whisper phải
  báo rõ "Máy chủ chưa cài chuyển giọng nói" (BE kiểm `config('meeting_ai.python')` tồn tại) thay vì lỗi mờ.
- Model mới `extends BaseModel`; FE màn mới chỉ dùng `V2Base*`, popup `V2BaseModal`, xác nhận `$confirm`,
  khối `V2BaseFormSection`, chọn NV theo `employeeOptionText`, không chữ đỏ ngoài lỗi.
- Model AI cố định Claude (`config('meeting_ai.model')`, mặc định `claude-sonnet-5-5`), không qua resolver.
- Queue `meeting_ai`: `retry_after` 14400, job `timeout` 10800, `tries` 1.
- Whisper: large-v3 int8, beam 5, 4 thread, VAD, `nice -n 19`; lọc câu bịa cuối.

## Điểm dễ hỏng (mỗi điểm có test ở task tương ứng)

1. Job dài bị bốc lại chạy lặp ⇒ Task 2 kiểm connection/timeout/tries.
2. Gửi bản mới khi bản cũ đang `transcribing` ⇒ 409, bản cũ giữ nguyên (Task 3).
3. Người không phải tạo/chủ trì gọi API ⇒ 403; cờ tắt ⇒ 404 (Task 3).
4. Script Python lỗi / hết thời gian ⇒ status `failed` + `error`, FE hiện lỗi + cho gửi lại (Task 2, 6).
5. Gợi ý nhiệm vụ: người làm ngoài danh sách nhân viên / hạn trống ⇒ không gửi được dòng đó (Task 4, 7).

---

### Task 1: Hạ tầng — bảng, model, cấu hình, script Python

**Files:**
- Create: `hrm-api/database/migrations/2026_11_20_000001_create_meeting_ai_minutes_table.php`
- Create: `hrm-api/Modules/Assign/Entities/Meeting/MeetingAiMinute.php`
- Create: `hrm-api/config/meeting_ai.php`
- Modify: `hrm-api/config/queue.php` (thêm connection `meeting_ai` cạnh `agent`)
- Create: `hrm-api/scripts/meeting-ai/transcribe.py`, `hrm-api/scripts/meeting-ai/README.md`

**Interfaces – Produces:**
- Bảng `meeting_ai_minutes`: `id, meeting_id (index), is_current tinyint, audio_path, audio_name, audio_size,
  duration_sec, status tinyint (1 uploaded, 2 transcribing, 3 done, 4 failed), error text, transcript_json
  longtext, transcript_text longtext, detail longtext, summary longtext, conclusion longtext,
  task_suggestions_json longtext, parts_status json (`{"detail":"idle|running|done|failed",...}`),
  usage_json json, started_at, finished_at, timestamps, created_by, updated_by`.
- `MeetingAiMinute` const `UPLOADED=1, TRANSCRIBING=2, DONE=3, FAILED=4`; `$casts` cho json; `meeting()`.
- `config('meeting_ai')`: `python, script, model, max_tokens (16000), disk_dir ('meeting-ai'),
  max_upload_mb (200)`.
- CLI: `python transcribe.py IN OUT_JSON --prompt "..." --threads 4 --beam 5` → JSON
  `{"duration": float, "segments": [{"start": float, "end": float, "text": str}]}`; exit≠0 khi lỗi.
  Script tự gọi ffmpeg với bộ lọc của design §5.3, tự bỏ segment khớp regex câu bịa
  (`subscribe|đăng ký kênh|cảm ơn các bạn đã (theo dõi|xem)`) nằm trong 30 s cuối.

- [x] Viết migration + model + config; `php artisan migrate --pretend --path=...` xem SQL.
- [x] Viết script; chạy trên máy dev (VPS) với `~/whisper-test/clip5m.wav` ⇒ JSON có segment, không câu "subscribe".
- [x] (Hỏi riêng) chạy migration vào DB local + DB dev hrm_crm, đúng `--path` file trên.

### Task 2: Job chuyển chữ

**Files:** Create `hrm-api/Modules/Assign/Jobs/TranscribeMeetingAudio.php`,
`hrm-api/Modules/Assign/Services/MeetingAi/WhisperRunner.php`; Test
`hrm-api/Modules/Assign/Tests/Unit/MeetingAi/TranscribeMeetingAudioTest.php`

**Interfaces – Produces:** `WhisperRunner::run(string $absPath, string $prompt): array` (mảng JSON của script,
ném `RuntimeException` khi exit≠0); `TranscribeMeetingAudio::__construct(int $minuteId)`, `$connection='meeting_ai'`,
`$queue='meeting_ai'`, `$timeout=10800`, `$tries=1`. `failed()` ghi status FAILED + error.
Prompt = tên thành phần họp phía công ty + khách + tiêu đề meeting (≤ 800 ký tự).

- [x] Test `test_job_dung_hang_doi_rieng_va_khong_chay_lai`: assert connection `meeting_ai`, tries 1, timeout 10800,
  `config('queue.connections.meeting_ai.retry_after') >= 14400`.
- [x] Test `test_thanh_cong_luu_transcript_va_status_done` (mock WhisperRunner trả 2 segment) ⇒ status DONE,
  `transcript_text` có dạng `[00:00:05] ...`, `duration_sec` đúng, `finished_at` có.
- [x] Test `test_runner_loi_thi_failed_co_error`.
- [x] Viết code cho tới khi xanh: `php artisan test Modules/Assign/Tests/Unit/MeetingAi`.

### Task 3: API tab AI

**Files:** Create `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingAiMinuteController.php`,
`.../Http/Requests/MeetingAi/UploadAudioRequest.php`, `.../Transformers/MeetingAiMinuteResource.php`;
Modify `hrm-api/Modules/Assign/Routes/Meeting/api.php`; Test
`hrm-api/Modules/Assign/Tests/Feature/MeetingAi/MeetingAiMinuteApiTest.php`

**Routes** (trong group `v1/assign/meeting`, prefix `/{meeting}/ai-minutes`):
- `GET /` → lượt `is_current` (hoặc null) + `can_use`.
- `POST /upload` (multipart `audio`, mimes webm,mp3,m4a,wav,ogg,mp4, max `max_upload_mb`) → tạo lượt mới,
  tắt `is_current` lượt cũ, dispatch job. Lượt hiện tại đang TRANSCRIBING ⇒ 409.
- `POST /{minute}/generate/{part}` (`part` ∈ detail|summary|conclusion|tasks) → dispatch Task 4 job, 202.
- `PUT /{minute}/parts` (detail, summary, conclusion, task_suggestions) → lưu bản user sửa.
- `GET /{minute}/transcript` → `transcript_json`.
- `GET /{minute}/audio` → tải file (stream).
Mọi route: `!$meeting->canEdit()` ⇒ 403; phân hệ/menu Meeting bị tắt (nếu BE có cơ chế) ⇒ 403. Upload khi
máy chủ chưa cài Whisper ⇒ 503 + câu báo rõ. Show meeting trả thêm `ai_minutes_can_use` (= canEdit).

- [x] Test 403 với NV không phải tạo/chủ trì; 503 khi `meeting_ai.python` không tồn tại; 409 khi đang transcribing;
  upload thành công ⇒ `Queue::assertPushed(TranscribeMeetingAudio::class)` + lượt cũ `is_current=0`;
  `generate/abc` ⇒ 422.
- [x] Code cho tới khi xanh.

### Task 4: Sinh 4 phần bằng Claude

**Files:** Create `hrm-api/Modules/Assign/Services/MeetingAi/MinutesWriter.php`,
`.../Services/MeetingAi/Prompts.php`, `hrm-api/Modules/Assign/Jobs/GenerateMeetingAiPart.php`;
Test `hrm-api/Modules/Assign/Tests/Unit/MeetingAi/MinutesWriterTest.php`

**Interfaces – Produces:** `MinutesWriter::__construct(ClaudeClient $client)`;
`MinutesWriter::write(MeetingAiMinute $m, string $part): array{text?:string, tasks?:array, usage:array}`.
Job `GenerateMeetingAiPart(int $minuteId, string $part)` — connection `agent`, timeout 170; cập nhật
`parts_status[$part]` running→done/failed, cộng dồn `usage_json`.
- Ngữ cảnh gửi Claude: tiêu đề + ngày meeting, danh sách người dự (tên, chức danh, phía), danh sách NV được
  phép giao (id, tên, mã phòng), bản chữ có mốc giờ. Bản chữ > ~60k ký tự ⇒ chia đoạn, tóm từng đoạn rồi gộp.
- `tasks`: yêu cầu Claude trả JSON `[{content, assignee_employee_ids, due_date, quote, timestamp}]`;
  `MinutesWriter` LỌC `assignee_employee_ids` chỉ giữ id có trong danh sách được phép, `due_date` không
  parse được ⇒ null. Mỗi dòng thêm `id` (uuid), `status:'suggested'`, `task_ids: []`.
- Quy tắc prompt chung: không bịa, chỗ không rõ ghi `[không nghe rõ mm:ss]`, giữ mốc giờ, tiếng Việt,
  gạch đầu dòng xuống dòng.

- [x] Test (ClaudeClient giả): `tasks` lọc bỏ id NV lạ; due_date sai ⇒ null; `detail` trả text;
  transcript dài ⇒ client được gọi > 1 lần.
- [x] Code cho tới khi xanh.

### Task 5: FE — khung tab + ghi âm/tải lên

**Files:** Create `hrm-client/pages/assign/meeting/components/MeetingAiMinutes.vue`,
`hrm-client/utils/audioRecorder.js`; Modify `hrm-client/pages/assign/meeting/components/MeetingForm.vue`
(tabs(): thêm `{key:'ai_minutes', label:'AI tạo biên bản', icon:'ri-sparkling-line'}` khi
`isShow && form.id && form.ai_minutes_can_use && canUseMeetingAi(this.$store)`; thêm panel `v-if` lazy).

- `audioRecorder.js`: `start()`, `stop(): Promise<Blob>`, `elapsed`, MediaRecorder `audio/webm;codecs=opus`.
- Dòng nhắc đồng ý ghi âm (chữ xám). Nút: Ghi âm / Dừng / Nghe lại / Lưu file về máy / Gửi xử lý / Ghi lại /
  Tải file ghi âm lên (`V2BaseFile`). Đang ghi ⇒ `beforeunload` cảnh báo. Gửi lỗi ⇒ toast + giữ Blob.
- Trạng thái: badge theo `status_text`/`status_color` BE trả; đang chuyển chữ ⇒ hỏi `GET` mỗi 15 s (dừng khi
  rời tab/huỷ component). Gửi bản mới khi đã có ⇒ `$confirm`.
- [x] Code; kiểm Playwright (ghi âm giả bằng `--use-fake-device-for-media-stream`): tab chỉ hiện với
  người tạo; upload file `clip5m.wav` ⇒ request 200, trạng thái "Đang chuyển chữ".

### Task 6: FE — 4 phần kết quả

**Files:** Modify `MeetingAiMinutes.vue`; Create
`hrm-client/pages/assign/meeting/components/ai/AiPartViewer.vue`.

- 4 nút chọn phần; chưa có ⇒ bấm là `POST generate`, hiện "Đang tạo…", hỏi lại 5 s tới khi done/failed.
- Có rồi ⇒ hiện nội dung (CKEditor có sẵn của tab Biên bản — rà và tái dùng), nút Lưu / Tạo lại (`$confirm`) / Copy.
- Xem bản chữ: modal `V2BaseModal` danh sách segment + mốc giờ.
- [x] Playwright: bấm Tóm tắt (BE local `AGENT_FAKE` hoặc client giả) ⇒ nội dung hiện, Lưu ⇒ reload còn.

### Task 7: FE — Gợi ý nhiệm vụ → gửi

**Files:** Create `hrm-client/pages/assign/meeting/components/ai/AiTaskSuggestions.vue`.

- Bảng (`V2BaseTableScroll`): chọn · Nội dung (`V2BaseTextarea`) · Người làm (`V2BaseSelect` nhiều, NV) ·
  Hạn (`V2BaseDatePicker`, bắt buộc) · Số giờ (mặc định 1) · Ưu tiên (mặc định Bình thường) · Trích dẫn + mốc giờ.
- **Gửi các nhiệm vụ đã chọn**: validate cùng lúc mọi dòng chọn (hạn, người làm, nội dung); hợp lệ ⇒ gọi
  tuần tự `POST assign/tasks` (đúng payload TaskPanel.vue:509: `meeting_id`, `title`, `assignee_ids`,
  `due_date`, `estimated_hours`, `priority`, `task_type` thường, `status` TODO) — dùng lại API có sẵn để giữ
  nguyên validate + thông báo; xong mỗi dòng ghi `status:'sent', task_ids` rồi `PUT parts` 1 lần.
  Dòng lỗi giữ lại kèm lỗi inline; dòng đã gửi khoá, có link nhiệm vụ.
- [x] Playwright: 2 dòng, 1 dòng thiếu hạn ⇒ cả 2 lỗi hiện cùng lúc, không gọi API; sửa xong ⇒ 2 task tạo,
  tab Nhiệm vụ của meeting hiện 2 dòng; bấm Gửi lại không tạo trùng. Ca không quyền: NV tham gia (không tạo)
  ⇒ không thấy tab.

### Task 8: Đưa lên VPS dev (mỗi mục hỏi riêng)

- [ ] Cài ffmpeg (`apt install ffmpeg`) trên devhrmnew.
- [ ] Chuyển venv + model từ `~/whisper-test` sang `/opt/meeting-ai/` (hoặc trỏ thẳng), chép `transcribe.py`.
- [ ] `.env` hrm_crm: `MEETING_AI_PYTHON`, `MEETING_AI_SCRIPT`.
- [ ] Worker: `php artisan queue:work meeting_ai --queue=meeting_ai --timeout=10800 --tries=1` (pm2, user
  thường) + kiểm worker `agent` đã chạy trên dev.
- [ ] Merge nhánh vào `gop_db-xuat-hang-cha-con` (môi trường tester) + deploy dev theo skill deploy-hrm;
  chạy migration đúng 1 file.
- [ ] Thử thật bằng `~/Desktop/test 4.webm` trên dev-hrm; đo thời gian + độ trễ site.

### Checkpoint — 20/11/2026 14:00
Vừa hoàn thành: Task 1–7 (code local, worktree `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-meeting-ai/{hrm-api,hrm-client}`,
nhánh `meeting-ai-bien-ban` cả 2 repo, CHƯA commit). Migration `2026_11_20_000001_create_meeting_ai_minutes_table` đã chạy
vào DB local `db_gop_6_11`. PHPUnit 16/16 xanh (Unit 9 + Feature 7). User xem giao diện: "Giao diện ổn".
Kiểm Playwright (MCP, :3000/:8000 của worktree): tab hiện với người tạo; NV tham gia không thấy tab + API 403; gửi khi
thiếu người làm/hạn ⇒ 6 dòng đỏ cùng lúc, 0 request; gửi 2 dòng ⇒ 3 task (1 + 2 người), reload còn "Đã giao", nút Gửi về 0.
Lệch so với plan: (1) sinh nội dung chạy connection `meeting_ai` queue RIÊNG `meeting_ai_text` (không phải `agent`) để
không chờ sau 1 lượt chuyển chữ; (2) không sửa MeetingTransformer — đã có sẵn `can_edit`; (3) script đọc WAV bằng numpy,
bỏ PyAV (PyAV mới lỗi `metadata_errors` trên Python 3.14); (4) thêm luật prompt "tên được nhắc ≠ người nói / giao việc".
Lỗi tìm thấy khi kiểm & đã sửa: ô "chọn tất cả" phát lại input khi đổi ⇒ bỏ 1 dòng là bỏ hết; `errors` trùng vee-validate.
Local dùng script giả `scratchpad/fake_transcribe.py` (bản chữ thật test 4) qua `.env` worktree.
Đang làm dở: —
Bước tiếp theo: Task 8.
Blocked: —

### Checkpoint — 20/11/2026 14:25 — ĐÃ DEPLOY dev-hrm.eteksofts.com
User đổi đích: KHÔNG dùng hrm_crm (nhánh tester gop_db-xuat-hang-cha-con thiếu module Agent, cũ từ 11/11) mà dùng
**dev-hrm.eteksofts.com = /var/www/tpe trên VPS dev (-p 2230), nhánh `develop`, DB `hrm_erp_test`**.
- Cherry-pick 2 commit lên `origin/develop`: api `dddca3c45` · client `d8d233fed` (kèm 1 commit #12225 của người khác, không migration).
- Migration: chỉ `2026_11_20_000001_create_meeting_ai_minutes_table` (--path). route:cache.
- Client: build tay ra shared/nuxt-build → tráo .nuxt → `sudo env PM2_HOME=/root/.pm2 pm2 reload hrm-client-tpe`
  (KHÔNG dùng ~/build_tpe.sh vì init.d restart = pm2 kill cả 8 bộ). last_deployed_client_commit đã ghi.
- ffmpeg 4.4.2 (apt), numpy vào venv. Venv + model CHUYỂN từ ~/whisper-test sang **/var/www/tpe/shared/meeting-ai**
  (www-data không vào được /home/erp_tpe 750); ~/whisper-test là symlink.
- .env (bản sao `.env.bak_truoc_meeting_ai_20261120`): ANTHROPIC_API_KEY chép từ prod TPE (user chọn) + MEETING_AI_PYTHON/MODEL_DIR.
- Supervisor `/etc/supervisor/conf.d/tpe-meeting-ai.conf`: tpe-meeting-ai (queue meeting_ai) + tpe-meeting-ai-text
  (queue meeting_ai_text), user www-data, log /var/log/laravel/tpe-meeting-ai*.log.
- Giới hạn tải lên NÂNG 200 MB (user yêu cầu 20/11 14:25): dev-hrm chạy **PHP 8.1** fpm ⇒ sửa
  `/etc/php/8.1/fpm/conf.d/90-hrm-custom.ini` (upload 200M, post 210M; bản sao `/etc/php/8.1/fpm/90-hrm-custom.ini.bak_truoc_200m_20261120`)
  + nginx `sites-enabled/dev-hrm.eteksofts.com` client_max_body_size 50M→210M (bản sao `/etc/nginx/dev-hrm.eteksofts.com.bak_truoc_200m_20261120`).
  Cũng đã sửa `/etc/php/7.4/fpm/php.ini` (upload 200M, post 210M — ảnh hưởng các site 7.4; bản sao `.bak_truoc_200m_20261120`).
  `.env` MEETING_AI_MAX_UPLOAD_MB=200. Kiểm: file 28.6 MB qua được (409 vì đang có lượt chạy).
- Việc nhỏ còn lại: supervisor tpe-meeting-ai* đang gọi /usr/bin/php7.4, web + tpe-worker dùng `php` (8.1) ⇒ đổi sang `php`
  SAU khi lượt chuyển chữ đang chạy xong (đổi giữa chừng = giết lượt).
- Thử thật: meeting 2335 (namdangit), test4 nén opus 32k 7.7 MB, tải lên 14:22:33.

### Checkpoint — 20/11/2026 15:00 — THỬ THẬT TRÊN dev-hrm XONG
- Meeting 2335, test4 (30'30", opus 32k 7.7 MB): Whisper large-v3 int8 beam5 4 thread trên VPS dev chạy 14:22:38 → 14:50:56
  = **28'18" (RTF 0.93)**, 376 đoạn, câu bịa cuối file đã lọc. Độ trễ API meeting trong lúc chạy tb 0.376 s, max 0.806 s
  (lúc nghỉ 0.31–0.37 s); load 4–5.3 / 8 nhân.
- Claude qua worker `meeting_ai_text`: Tóm tắt + Gợi ý nhiệm vụ xong trong 21 s; 6 nhiệm vụ gợi ý đúng nội dung.
- 2 worker đã đổi sang /usr/bin/php8.1 (cùng web) sau khi lượt chạy xong.
Bước tiếp theo: user thử trên giao diện dev (ghi âm web, tải file, gửi nhiệm vụ); sau đó bàn đưa lên prod TPE (cài Whisper prod, gop_db).

### Checkpoint — 20/11/2026 ~15:20 — Giao diện gọn + tách Tên công việc / Mô tả
User góp ý: nội dung các phần đẹp, dễ xem; chỉ bấm Sửa mới hiện văn bản thuần; nút chọn phần đẹp + màu ấn tượng nhưng
NHỎ GỌN (phong cách phần mềm). Mockup `mockup-ket-qua-ai.html` (bản gọn) user duyệt. User hỏi nội dung nhiệm vụ vào
trường nào ⇒ chốt phương án 2: AI tách "title" (≤100, ghi tasks.title varchar 255, bộ đếm /255, vượt báo đỏ, không cắt
ngầm) + "description" (ghi tasks.description, nối câu trích + mốc giờ).
- api `bf9b8f2da` (nhánh) → develop `2dfb533a3`; client `3cd0fc8d1` → develop `0efcd7ade`. Không migration.
- Kiểm local Playwright: pill 30px gap 6px, màu icon đúng; thanh đầu 39px; doc 51 chip/7 tiêu đề/3 nhãn, không lọt ##/**;
  Sửa ⇒ textarea thuần, Huỷ ⇒ về xem; nhiệm vụ: 260 ký tự ⇒ 260/255 đỏ + lỗi, Lưu nháp/Gửi 0 request; gửi thật ⇒
  description đúng + câu trích (task thử đã xoá). PHPUnit 17/17.
- dev-hrm: pull api + route:cache + `php artisan queue:restart` (chạy bằng erp_tpe — www-data lỗi quyền cache);
  build client tay + reload hrm-client-tpe.

### Checkpoint — 20/11/2026 ~18:55 — Gợi ý nhiệm vụ dạng thẻ + bỏ bắt buộc Số giờ
- User: bảng 8 cột "rối" ⇒ mockup `mockup-goi-y-nhiem-vu.html` (thẻ) duyệt, bổ sung: (1) Số giờ được giao KHÔNG bắt
  buộc — áp cho cả module Nhiệm vụ; (2) chọn Ưu tiên giống form tạo task. User chọn "làm 2" = gộp chung nhánh meeting-ai-bien-ban.
- hrm-api `877ec6a44`: TaskStoreRequest/TaskUpdateRequest/TaskFieldUpdateRequest estimated_hours nullable|numeric|min:0
  (+3 ca TaskV2ApiTest, 35/35). Báo cáo/Agent cộng SUM/COALESCE/?? 0 — đã kiểm. Hệ quả nghiệp vụ: tỉ lệ giờ giao/giờ
  thực tế (báo cáo hiệu suất giải pháp) thấp đi với task không nhập giờ.
- hrm-client `8154176a1` (TaskForm bỏ * ; TaskDetailTab sửa nhanh xoá trống được) + `40db442cc` (thẻ: V2BaseInput tên
  — b-form-textarea ép ≥2 dòng; V2BaseSegmented .tkp-prio-seg nạp task-panel.scss như IssuePanel; Mô tả & căn cứ thu gọn).
- Playwright local: 6 thẻ, chip ưu tiên 30px/13px/8px = form tạo task; lỗi 4 thẻ cùng lúc, 0 request; số giờ trống không lỗi;
  nhãn "Số giờ được giao" không còn *.
- develop: api `4b5913836` · client `1f2d4f8d2` (kèm 9/7 commit người khác, không migration/package). dev-hrm deploy.
⚠️ Khi đưa lên prod: thay đổi "Số giờ không bắt buộc" là luật chung module Nhiệm vụ — đang nằm trong nhánh meeting-ai-bien-ban.

### Checkpoint — 20/11/2026 ~20:35 — So sánh file nén vs file gốc trên dev-hrm (meeting 2335)
Vừa hoàn thành: thử lượt 2 bằng FILE GỐC `test 4.webm` 28,6 MB (lượt 1 = bản nén opus 32k 7,7 MB), cùng 30'30".
- Chuyển chữ: lượt 1 28'18" · 376 đoạn / 4.411 từ · **mất 46 s đầu** · 9 khoảng trống ≥20 s (302 s) · lặp "Ừ." ×13, "Cháu bảo anh Nam rồi" ×5.
  Lượt 2 22'38" · 486 đoạn / 4.935 từ (+12%) · bắt từ 00:01 · 7 khoảng trống (185 s) · còn lặp "Ngoại lý ra đây" ×3 cuối file.
  (Lượt 2 nhanh hơn có thể do tải máy dev buổi tối thấp — chưa tách nguyên nhân.)
- Claude: lượt 1 có 3 phần (không có Kết luận) 65.157 in / 7.294 out ≈ 0,20 USD; lượt 2 đủ 4 phần 90.521 / 10.301 ≈ 0,28 USD
  (giá Sonnet 5.5 $2/$10 per MTok; usage_json cộng dồn, có thể gồm cả lần Tạo lại). ≈ 0,4 USD / giờ họp.
- Chất lượng lượt 2 tốt hơn: thêm chủ đề "Kế toán duyệt + Ban Lãnh đạo duyệt YC xuất hàng" (46 s đầu), thêm nhiệm vụ
  "Thêm bước BLĐ duyệt" + "Chuẩn hoá mã phòng"; Tóm tắt không còn ý sai "trừ hạn mức" (từ chữ nghe nhầm "trừng hạn").
- Lỗi phát hiện ở lượt 2: (1) Kết luận TỰ MÂU THUẪN — "Đã thống nhất: người nhận phải tạo nhiệm vụ mới" nhưng "Vấn đề
  còn mở" + Nội dung chi tiết ghi "chưa chốt" (lượt 1 lại ghi "Chốt: được đổi + thông báo") ⇒ cần nghe lại băng 22'–25';
  (2) chữ nghe nhầm lọt vào kết quả ("đèn xe kho" = đề nghị xuất kho, "danh mục phòng 3"); (3) mốc giờ lẫn 00:00:26 / 02:52.
- Nhiệm vụ gợi ý cả 2 lượt: chưa có người nhận / hạn (biên bản không gọi tên).
Đang làm dở: —
Bước tiếp theo: (a) bỏ hoặc nâng mức nén phía trình duyệt (32k làm mất đầu file + lặp câu); (b) prompt: ý đã ở "Vấn đề còn mở"
thì không được vào "Đã thống nhất", thống nhất định dạng mốc giờ; (c) danh sách thuật ngữ nghiệp vụ cho Whisper initial_prompt
+ Claude. Đụng code ⇒ hỏi phạm vi riêng, chờ "làm".
Blocked: —
