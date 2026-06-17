# SCORM LMS Runtime — Plan

**Owner:** @junfoke
**Date:** 2026-05-30

> Plan chi tiết đầy đủ (code + verify): `docs/superpowers/plans/2026-05-30-scorm-lms-runtime.md`
> Spec: `docs/superpowers/specs/2026-05-30-scorm-lms-runtime-design.md`

## Tổng quan

14 tasks, 5 phases — BE (Training + Elearning) + FE (Vue 3 elearning). Học bài SCORM type=4: reverse-proxy S3 same-origin + scorm-again (1.2+2004) + endpoint scorm-commit + resume.

## Phase 1: Database + Entity (Training)
- [x] Task 1: Migration thêm 9 cột `scorm_*` vào `enrollment_lesson_progress`
- [x] Task 2: Casts decimal trong Entity `EnrollmentLessonProgress`

## Phase 2: Backend Elearning
- [x] Task 3: `LearningSessionResource` — completion_rule + scorm_state cho type=4
- [x] Task 4: `ScormCommitRequest` — validation
- [x] Task 5: `LearningSessionService` — processScormCommit + checkScormCompletion
- [x] Task 6: Controller `scormCommit` + route `POST /learn/scorm-commit`

## Phase 3: Frontend hạ tầng
- [x] Task 7: Vite proxy `/scorm-proxy` + env `VITE_SCORM_S3_BASE`
- [x] Task 8: Cài `scorm-again` (v3.0.5 — export Scorm12API/Scorm2004API, event LMSCommit/LMSFinish + Commit/Terminate, loadFromJSON: đều khớp plan)
- [x] Task 9: Util `scorm.js` — toScormProxyUrl + normalize cmi (1.2/2004)

## Phase 4: Frontend viewer + wiring
- [x] Task 10: `ScormPlayer.vue` — viewer SCORM
- [x] Task 11: `LessonViewer.vue` — nhánh scorm + emit commit
- [x] Task 12: Composable `useScormCommit.js`
- [x] Task 13: `SubjectLearnView.vue` — typeLabel/completionHint/wiring commit

## Phase 5: Migration + Verify
- [x] Task 14: Migration chạy + test resume/completion trên browser — PASS (gói Run-Time SCORM 2004 đạt "Đã xong", resume OK)

## Phase 6: Fix phát sinh khi test browser (2026-05-30)
- [x] Sửa host S3 → `tanphat.s3.cloud.cmctelecom.vn` (proxy target + env)
- [x] `toScormProxyUrl` strip origin tổng quát (giữ query/hash)
- [x] `:key` trên ScormPlayer → fix đổi bài SCORM→SCORM không reload
- [x] Proxy inject `window.confirm=()=>true` chặn 2 hộp thoại confirm gốc của gói
- [x] Popup resume "Tiếp tục bài học?" (Học tiếp / Học lại) trong ScormPlayer
- [x] Proxy: no-store + bỏ If-None-Match/If-Modified-Since cho HTML (tránh cache bản chưa inject)
- [x] Cài scorm-again trong container + note Node ≥18

## Phase 7: Fix chiều cao không đồng bộ (2026-06-01)
- [x] Đồng bộ chiều cao SCORM = 620px ở MỌI trạng thái: trạng thái loading + initError đang hardcode `h-[400px]` → đổi sang dùng `heightClass` (620px responsive như iframe ready), tránh khung nhảy khi init xong

## Phase 8: Toast khi Exit (2026-06-01)
- [x] Bấm Exit trong gói SCORM → toast "Đã lưu tiến độ học" (thay native confirm "save progress" đã bị chặn). Dùng useToast, hook vào event Terminate/LMSFinish; bỏ qua khi unmount (đổi bài) để tránh nhiễu

## Phase 9: Hoàn thiện UX + fix resume (2026-06-01)
- [x] Fix 500 stale-socket khi proxy load launchpage: `https.Agent({keepAlive:false})` + error handler 502
- [x] Fix resume sai sau khi commit: thêm `store.updateScormState` (cập nhật scorm_state trong store ngay mỗi commit, không đợi /learn re-fetch)
- [x] Fix đổi bài giữa chừng không lưu vị trí: commit gắn đúng `subject_lesson_id` của bài (capture lúc init trong ScormPlayer + prop subject-lesson-id), handleScormCommit dùng slid từ payload + flush ngay (commit SCORM thưa)
- [x] Overlay "Đã kết thúc bài học" sau Exit (chặn click nút chết của gói → hết SCORM Error 133) + nút "Mở lại bài học" (restart)
- [x] Việt hoá + restyle 3 nút điều hướng của gói (onIframeLoad, guard theo id Rustici, an toàn gói khác)
- [x] Bọc nội dung SCORM trong khối có viền (tách với nav bài học), KHÔNG header (đồng bộ viewer khác)
- [x] Gỡ toàn bộ log [SCORM DEBUG]

## Phase 10: Fix bug completion + độ trễ learning (2026-06-01)
- [x] BUG điểm: `checkScormCompletion` chỉ áp `min_score` cho nhánh `passed` → rule `completed` (+min_score) bị bỏ qua điểm → score 27 vẫn "Đã xong" dù YC ≥60. Fix: tách `scoreOk` thành gate AND áp cho MỌI rule (khớp config "X & điểm ≥ Y" + FE hint). File: `LearningSessionService.php::checkScormCompletion`
- [x] Độ trễ "Đang học": status chỉ đổi khi có scorm-commit đầu tiên (autocommit ~30s). Fix: hook event Initialize/LMSInitialize trong `ScormPlayer.vue` → emit commit ngay khi gói init → BE mark learning tức thì

## Phase 11: UX "chưa đạt điểm" + giữ điểm cao nhất (2026-06-01)
- [x] BE giữ điểm cao nhất: `processScormCommit` áp `max()` cho `score_raw`/`score_scaled` (lần làm lại điểm thấp không ghi đè điểm cao). File: `LearningSessionService.php`
- [x] FE banner "chưa đạt": `ScormPlayer.vue` thêm computed `notPassed` (completed nhưng score < min, ẩn khi status=done) → banner amber "Điểm X/Y — làm lại" + nút "Làm lại bài" (restart fresh). Overlay kết thúc phiên cũng đổi text/màu khi chưa đạt.
- [x] `restart()` thêm cờ `forceFresh` → bỏ qua popup resume khi "Làm lại"
- [x] Truyền prop `status` từ `LessonViewer.vue` xuống ScormPlayer (ẩn banner khi done)

## Phase 12: Fix banner còn hiện khi đang làm lại + iframe không reset (2026-06-01)
- [x] Banner chuyển sang EVENT-DRIVEN (`showRetryBanner` ref + `evaluateRetry(payload)` gọi trong emitCommit) thay vì derive từ `scormState` lưu trữ → bấm "Làm lại" + đang làm dở (chưa nộp) thì banner KHÔNG hiện. Chỉ bật khi commit báo completed mà điểm < ngưỡng; tắt khi commit báo đang làm dở hoặc đạt điểm.
- [x] Fix "Làm lại" không reset gói (đáp án cũ còn nguyên): thêm `:key="frameKey"` trên iframe, `restart()` bump frameKey → ép iframe tạo mới hoàn toàn (gói SCORM init lại). Fix riêng SCORM 1.2 (restart sync ready false→true cùng tick không remount iframe).
- [x] Reset `showRetryBanner` trong `restart()` + `onResumeRestart()`
- [x] Banner hiện NGAY khi nộp (không đợi commit): hook event `SetValue`/`LMSSetValue` → `refreshRetryFromApi()` đánh giá banner từ cmi sống. Lý do: nhiều gói chỉ Commit ở autocommit ~30s / lật trang / thoát nên banner bị trễ sau khi nộp.
- [x] Fix loop overlay "Đã kết thúc / Mở lại bài học" sau khi bấm Làm lại: iframe CŨ lúc bị gỡ (remount) gọi `window.API.LMSFinish()` nhưng `window.API` đã trỏ api MỚI → bật `onTerminate` → sessionEnded=true ngay. Fix: cờ `suppressTerminate` (set true trong `restart()`, clear trong `onInitialized()` của gói mới) → bỏ qua Terminate "ma".
- [x] Fix banner còn 27/60 sau khi đề đã reset trắng: iframe cũ lúc unload còn gọi `SetValue` (score+completed) → vì `restart()` đồng bộ nên `window.API` đã trỏ api MỚI → api mới bị nhiễm → SetValue hook bật lại banner. Fix: `restart()` thành `async` — cleanupApi (xoá window.API) + gỡ iframe cũ + `await nextTick()` rồi MỚI tạo api mới (lúc iframe cũ unload, window.API=undefined → no-op). Thêm guard `suppressTerminate` cho `refreshRetryFromApi`.

## Phase 13: Cập nhật "Đã xong" tức thì khi nộp đạt điểm (2026-06-01)
- [x] Khi gói báo làm xong bài (SetValue → completed/passed/failed) → `refreshRetryFromApi` chủ động `emitCommit()` lên BE NGAY (debounce 400ms để gói ghi đủ score+completion) → BE đánh giá → đạt thì trả status `done` → pill "Đã xong" tức thì, không chờ autocommit ~30s. Trước đó chỉ banner "chưa đạt" cập nhật ngay (FE), còn pass phải chờ commit.
- [x] Dọn `completionCommitTimer` trong `cleanupApi`

### Làm rõ (không phải bug)
- `score_min` (payload) = `cmi.score.min` = điểm sàn thang điểm bài (gói báo 0). KHÁC `scorm_min_score` (config = ngưỡng đạt 60). Commit KHÔNG ghi đè ngưỡng config.

### Checkpoint — 2026-06-01 (Phase 10+11)
Vừa hoàn thành: BE min_score AND-gate + giữ điểm max; FE commit-on-init (hết trễ "Đang học") + banner "chưa đạt + Làm lại".
Đang làm dở: (không có)
Bước tiếp theo: User restart dev server (elearning FE + API) + test: (1) mở bài → "Đang học" ngay; (2) làm bài <60 → banner "chưa đạt" + làm lại; (3) làm lại ≥60 → "Đã xong". Record "Đã xong" cũ không tự revert (BE early-return) — cần bài/enrollment mới hoặc reset row.
Blocked: (không có)

## Trạng thái
DONE — feature SCORM chạy đúng end-to-end trên browser (completion + resume + popup). Chi tiết debug: spec mục 11.

### Checkpoint — 2026-05-30
Vừa hoàn thành: Toàn bộ feature SCORM LMS Runtime + 7 fix phát sinh khi test browser. Verify: gói Run-Time SCORM 2004 (scorm.com) học → "Đã xong", resume qua popup của app, không còn native confirm.
Đang làm dở: (không có)
Bước tiếp theo: Note OPS cấu hình nginx prod (proxy /scorm-proxy + sub_filter inject confirm + no-store — xem spec mục 2 & 11). Merge khi sẵn sàng.
Blocked: (không có)
