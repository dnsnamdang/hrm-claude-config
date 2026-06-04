# Plan — elearning-completion-criteria (Hướng A + option SCORM)

> Owner: @junfoke · Spec: docs/superpowers/specs/2026-06-04-elearning-completion-criteria-enforcement-design.md

## Phase 1 — BE: SCORM browsed/viewed

- [x] 1.1 `LessonRequest.php`: mở rộng enum `scorm_completion` → thêm `browsed,viewed`
- [x] 1.2 `LearningSessionService::checkScormCompletion`: thêm nhánh `browsed` (completed|browsed|passed + scoreOk) và `viewed` (scoreOk)

## Phase 2 — FE elearning: đọc trạng thái browsed

- [x] 2.1 `elearning/src/utils/scorm.js` `readScorm12`: map `lesson_status='browsed'` → `completion_status:'browsed'`

## Phase 3 — FE hrm-client: form tạo bài

- [x] 3.1 `LessonForm.vue`: thêm input "Min thời gian đọc (giây)" cho Bài viết (`text_min_read_seconds`) + Tài liệu (`file_min_read_seconds`)
- [x] 3.2 `LessonForm.vue`: gắn nhãn "(chưa áp dụng)" cho field % (text/file), "Cho tua video", "Cho phép tải xuống"
- [x] 3.3 `LessonForm.vue`: thêm 2 option `browsed`/`viewed` vào dropdown "Hoàn thành khi SCORM báo" + hint

## Phase 4 — FE hrm-client: form ghi đè cấp khoá

- [x] 4.1 `SubjectLessonCompletionOverride.vue`: gắn nhãn "(chưa áp dụng)" cho mọi field chưa enforce
- [x] 4.2 `SubjectLessonCompletionOverride.vue`: thêm 2 option `browsed`/`viewed` vào dropdown SCORM + hint

## Phase 5 — Verify
- [ ] 5.1 User verify (xem spec §6) trong Docker (elearning Node ≥18) + hrm-client/hrm-api

## Phase 6 — Bỏ `browsed`, chỉ giữ `viewed` (2026-06-04, sau test)
Lý do: `browsed` chỉ kích hoạt khi gói chạy browse-mode (gần như không xảy ra) → test mãi không xong; đã bị `viewed` (mở là xong, cho cả 1.2 + 2004) bao trùm.
- [x] 6.1 Bỏ option `browsed` khỏi `LessonForm.vue` + `SubjectLessonCompletionOverride.vue`
- [x] 6.2 `LessonRequest.php`: enum bỏ `browsed` → `completed,passed,completed_or_passed,viewed`
- [x] 6.3 `LearningSessionService::checkScormCompletion`: bỏ nhánh `browsed`
- [x] 6.4 `elearning/src/utils/scorm.js`: revert `readScorm12` về nguyên bản (browsed → incomplete)
- [x] 6.5 `SubjectLearnView.vue` `completionHint`: thêm nhánh `viewed` → "YC: mở bài học" (trước rơi nhầm về "completed/passed")

## Phase 7 — `viewed` có ngưỡng "Min giây mở" (đếm giây như tài liệu)
Field tuỳ chọn `scorm_min_view_seconds` (trống = mở là xong). Đếm giây mở bài, tạm dừng + gate "Tiếp tục" khi rời tab. Tận dụng cột `read_seconds` (không migration).
- [x] 7.1 BE `Lesson::getDefaultTrackingCompletion`: thêm key `scorm_min_view_seconds`
- [x] 7.2 BE `LessonRequest`: validate `scorm_min_view_seconds` (nullable|numeric|min:0)
- [x] 7.3 BE `LearningSessionResource::extractCompletionRule` (SCORM): gửi `scorm_min_view_seconds`
- [x] 7.4 BE `ScormCommitRequest` + Controller `only()`: nhận `read_seconds`
- [x] 7.5 BE `processScormCommit`: lưu `read_seconds` (max); `checkScormCompletion` viewed → `viewOk = read_seconds ≥ ngưỡng`
- [x] 7.6 FE `ScormPlayer.vue`: timer `useReadingTracker` + `ReadingGateOverlay`, đính `read_seconds` vào commit, flush khi đạt ngưỡng
- [x] 7.7 FE `SubjectLearnView.completionHint`: viewed có ngưỡng → "YC: mở bài ≥ Ns"
- [x] 7.8 FE hrm-client `LessonForm` + `SubjectLessonCompletionOverride`: input "Min giây mở" + default key
- [x] 7.9 FIX: `viewed` chưa chuyển "Đang học" khi vào (gói stub không gọi Initialize) → `ScormPlayer.finalizeReady` commit ngay khi mở nếu rule=viewed (độc lập gói SCORM). Overlay hiện lúc alt-tab là đúng thiết kế (hidden→visible).

## Phase 8 — Hướng B: enforce thật (4 nhóm khả thi)
DB không migration (tái dụng watched_percent/read_seconds theo loại bài). Spec §7B.
- [x] 8.1 BE `LearningSessionResource::extractCompletionRule`: mở rộng field video/text/file
- [x] 8.2 BE `LearningSessionService::checkCompletion`: video (min_watch_seconds) + text (scroll needScroll)
- [x] 8.3 FE `LessonViewer.vue`: truyền `completion-rule` cho Youtube/Article/Document
- [x] 8.4 FE `YoutubePlayer.vue`: emit readSeconds(played) + require_active_tab pause/auto-resume + chặn tua (allow_seek)
- [x] 8.5 FE `ArticleViewer.vue`: scroll listener → emit watchedPercent(scroll%), snap 100 gần đáy
- [x] 8.6 FE `DocumentViewer.vue`: nhận completion-rule, ẩn nút tải khi allow_download=false
- [x] 8.7 FE `useHeartbeat.js`: interval cấu hình được; `SubjectLearnView` set theo video_heartbeat_seconds
- [x] 8.8 FE hrm-client: gỡ nhãn "(chưa áp dụng)" cho field đã enforce (giữ: file view%/scroll%, dwell x2, max_seek%)
- [x] 8.9 completionHint video (+min giây) / text (+cuộn %)
- [x] 8.10 FIX: edge-trigger flush heartbeat theo TỪNG ngưỡng (thời gian/scroll/%xem/min giây) thay vì chỉ 1 lần/bài (`flushedThresholds` map) → đạt điều kiện cuối là done ngay, không chờ 30s

## Backlog — chưa làm (bất khả thi với kiến trúc hiện tại, giữ nhãn "(chưa áp dụng)")
- [ ] File `view_percent` / `min_scroll_percent`: viewer Google/Office cross-origin → cần thay PDF.js (feature riêng)
- [ ] Dwell/trang (text + file): không có khái niệm "trang" / cross-origin
- [ ] Video `max_seek_percent`: phức tạp, giá trị thấp

### Checkpoint — 2026-06-04
Vừa hoàn thành: CODE DONE Hướng B (Phase 8, 10 file). BE 2 (pass php -l) + FE elearning 7 + FE hrm-client 2. DB không migration (tái dụng watched_percent/read_seconds theo loại bài).
Đang làm dở: (không)
Bước tiếp theo: User rebuild + verify browser. Kịch bản: video pause khi rời tab + tự phát lại; chặn tua; min giây xem; heartbeat theo config; text cuộn % + kéo cuối; file ẩn nút tải khi allow_download=Không.
Blocked:

---
### Checkpoint — 2026-06-04
Vừa hoàn thành: CODE DONE Hướng A + option SCORM (Phase 1-4, 5 file). BE pass `php -l`. BE: LessonRequest enum + checkScormCompletion (browsed/viewed). FE elearning: scorm.js readScorm12 (browsed). FE hrm-client: LessonForm (input min_read_seconds text/file + nhãn "(chưa áp dụng)" + 2 option SCORM), SubjectLessonCompletionOverride (nhãn "(chưa áp dụng)" + 2 option SCORM).
Đang làm dở: (không)
Bước tiếp theo: User verify browser 5 kịch bản (spec §6). elearning cần Docker Node ≥18; hrm-client/hrm-api test riêng.
Blocked:
