# elearning-tracking-fix — Plan

Owner: @junfoke · Bắt đầu: 2026-06-02

## Phase 1 — Hiển thị thời gian 3:12 (BE + FE)

- [x] BE-1.1: `LearningSessionResource` thêm `'duration' => (int) $lesson->duration` (giây) vào lesson payload
- [x] FE-1.1: `SubjectLearnView.vue` thêm computed `durationLabel` (formatLessonDuration(duration), fallback minutes+"p"), thay `{{ minutes }}p`
- [x] FE-1.2: `LessonItem.vue` (sidebar outline) thêm `durationLabel` tương tự

## Phase 2 — Hint completion theo config (FE)

- [x] FE-2.1: `completionHint` đọc `completion_rule.video_watch_percent` / `text_min_read_seconds` / `file_min_read_seconds` (fallback default); SCORM giữ nguyên

## Phase 3 — Video tracking thật bằng YouTube IFrame Player API (FE)

- [x] FE-3.1: Composable `useYoutubeApi.js` — singleton loader script `youtube.com/iframe_api`
- [x] FE-3.2: `YoutubePlayer.vue` dùng `new YT.Player`, cộng giây chỉ khi PLAYING + chống tua (delta 0..2s), watchedPercent = round(played/getDuration()*100); emit progress
- [x] FE-3.3: `LessonViewer.vue` truyền `video_id` + `:key="subject_lesson_id"` (remount khi đổi bài)
- [x] FE-3.4: Cleanup player khi unmount (destroy + clearInterval + cờ destroyed)

## Phase 4 — Tối ưu heartbeat scale (FE)

- [x] FE-4.1: `useHeartbeat` — keepalive `fetch` khi `pagehide` + `visibilitychange→hidden`; export `ELEARNING_API_BASE`; `teardown()` gọi từ view onBeforeUnmount (composable tạo sau await nên không tự đăng ký lifecycle)
- [x] FE-4.2: `handleProgress` return sớm khi `status === 'done'` → cắt request thừa
- [x] FE-4.3: Đường nâng cấp scale (Redis buffer/queue) ghi ở design.md mục Out of scope

## Phase 5 — Fix trạng thái cập nhật chậm (phát hiện khi test)

- [x] FE-5.1: `handleProgress` — lần đầu có tiến độ của bài `todo` → optimistic `status='learning'` + flush heartbeat ngay (không chờ nhịp 30s). Áp dụng cả video/tài liệu/bài viết. Bug: xem video <30s vẫn "Chưa học" vì heartbeat đầu tiên đợi 30s.
- [x] FE-5.2: Toast "Hoàn thành bài học!" bắn nhầm khi quay lại bài đã xong. Fix: bỏ `watch(currentLesson.status)` (đổi bài learning→done cũng bắn), thay bằng store `completionSignal` tăng khi BE trả `just_completed=true` (đúng lúc bài VỪA done; áp dụng cả heartbeat + SCORM commit).

## Phase 6 — Tính toàn vẹn tracking: chống tua video & rời tab khi đọc tài liệu

- [x] FE-6.1: YoutubePlayer nới ngưỡng seek `SEEK_THRESHOLD = 4` (cho tốc độ 1.5x/2x tính theo giây-video thật; vẫn chặn kéo tua). Sửa lỗi `< 2` chặn nhầm 2x.
- [x] FE-6.2: Composable `useReadingTracker.js` — chỉ đếm khi tab visible (Page Visibility); rời tab→quay lại dựng cờ `needsResume`. KHÔNG dùng hasFocus (tránh dừng nhầm khi bấm vào iframe PDF/Office cross-origin).
- [x] FE-6.3: Component `ReadingGateOverlay.vue` — overlay mờ + nút "Tiếp tục học".
- [x] FE-6.4: ArticleViewer + DocumentViewer bỏ setInterval cũ, dùng `useReadingTracker` + overlay (root thêm `relative`).

Quyết định với user: tài liệu/bài viết = pause + overlay xác nhận; video = cho tua nhanh tính giây-video thật. Video tab-switch không cần overlay (YouTube tự pause, người dùng tự nhận biết).

## Phase 7 — Fix loop heartbeat 1s/lần (phát hiện khi test)

- [x] FE-7.1: `handleProgress` đổi flush-khi-đạt-ngưỡng sang **edge-triggered** (`thresholdFlushedFor`): chỉ flush 1 lần đúng lúc VỪA vượt ngưỡng, thay vì flush mỗi tick khi đã ≥ ngưỡng mà bài chưa/không done → trước đó gây loop heartbeat 1 giây/lần.

## Phase 8 — Fix "Tiếp tục học" vào sai bài (phát hiện khi test)

- [x] FE-8.1: `learningSession` store thêm action `resumeLessonId()` — chọn bài tiếp tục: (1) bài `learning` chưa khoá mới nhất → (2) bài chưa xong đầu tiên chưa khoá → (3) fallback `firstUnlockedId`
- [x] FE-8.2: `SubjectLearnView.vue` onMounted khi không có `lessonId` trên URL → dùng `resumeLessonId()` thay `firstUnlockedId()`. Bug: nhấn "Tiếp tục học" (chỉ push slug, không kèm lessonId) luôn mở bài đầu thay vì bài đang học dở.

## Verify

- [ ] Test browser: video 3:12 hiện đúng; play thật mới tăng %, pause thì dừng; đạt ngưỡng config → "Đã xong"; tài liệu/bài viết đếm giây + done theo config; đổi bài/đóng tab không mất tiến độ

---

### Checkpoint — 2026-06-02

Vừa hoàn thành: CODE DONE cả 4 phase (8 file: 1 BE + 7 FE).
- BE: LearningSessionResource trả thêm `duration` (giây).
- FE: SubjectLearnView (durationLabel + completionHint theo config + guard done), LessonItem (durationLabel), YoutubePlayer (rewrite IFrame Player API), LessonViewer (truyền video_id + key), useYoutubeApi (mới), useHeartbeat (keepalive + teardown), api.js (export base).

Đang làm dở: Không. Chờ verify trên browser (trong Docker, Node ≥18).
Bước tiếp theo: User chạy/refresh dev server elearning + test theo mục Verify; nếu PASS → wrap up (fill spec chi tiết) + merge.
Blocked: Không build/lint local được do Node local = 14, Vite 5 cần ≥18 (chạy trong container).

### Checkpoint — 2026-06-03

Vừa hoàn thành: Phase 8 — fix nút "Tiếp tục học" vào sai bài (2 file FE).
- `stores/learningSession.js`: thêm action `resumeLessonId()` (ưu tiên bài đang học chưa khoá mới nhất → bài chưa xong đầu tiên → fallback `firstUnlockedId`).
- `views/subject/SubjectLearnView.vue`: onMounted khi URL không có `lessonId` → dùng `resumeLessonId()` thay `firstUnlockedId()`.
- Nguyên nhân: `handleStartLearn()` chỉ push route kèm `slug`, không kèm `lessonId` → view luôn mở bài mở đầu tiên.

Đang làm dở: Không.
Bước tiếp theo: Verify trên browser — vào khoá đang học dở (vd 83%) → nhấn "Tiếp tục học" → phải mở đúng bài đang học, không về bài đầu. Logic dựa vào field `status` từng lesson từ API `/subjects/{slug}/learn`.
Blocked: Không build/lint local được (Node local = 14, Vite 5 cần ≥18 — chạy trong Docker).

## Phase 9 — Fix "Chặn tua video" không có hiệu lực (BE + FE)

Bug: (1) cấu hình "Cho tua video = Không" không chặn được tua; (2) tua tới cuối video → bài chuyển "Hoàn thành".

- [x] BE-9.1: `SubjectBuilderRequest` thêm `prepareForValidation()` chuẩn hoá boolean trong `tracking_completion_override` (cả `chapters.*.subject_lessons.*` và `subject_lessons.*`) — copy pattern đã có ở `LessonRequest`
- [x] FE-9.1: `YoutubePlayer.vue` — `blockSeek()` / `requireActiveTab()` parse được cả boolean lẫn chuỗi "true"/"false" (dữ liệu override cũ đã lưu dạng chuỗi trong DB)
- [x] FE-9.2: `YoutubePlayer.vue` — ENDED chỉ snap 100% khi đã thực sự phát gần hết (`played >= duration - SEEK_THRESHOLD`); nếu đang chặn tua mà ENDED do nhảy cóc → kéo về `maxReached`
- [x] FE-9.3: `YoutubePlayer.vue` — khoá cứng thanh tua (user chốt 2026-07-16, thay vì chỉ snap-back): bài cấm tua → `playerVars.controls = 0` + `disablekb = 1` (bỏ hẳn thanh tua + phím tắt), tự render control riêng (Play/Pause + thanh tiến độ read-only + mm:ss + icon khoá). Bài cho phép tua giữ nguyên control YouTube. Snap-back giữ làm lớp phòng thủ cuối.
- [x] FE-9.4: Control tự vẽ bổ sung tốc độ phát 0.5x/1x/1.25x/1.5x/2x — PM chỉ cấm kéo tua, KHÔNG cấm xem nhanh. Trần 2x nằm dưới `SEEK_THRESHOLD` (4) nên tiến độ vẫn cộng đúng khi phát nhanh. Sync ngược qua `onPlaybackRateChange`.
- [x] FE-9.6: Gom tốc độ vào menu nút bánh răng (thay vì 1 hàng nút) — popup có header "Tốc độ" + tick mốc đang chọn, click ra ngoài tự đóng. KHÔNG có mục chất lượng: YouTube đã deprecate `setPlaybackQuality()` (chất lượng auto theo băng thông) → thêm nút sẽ là nút chết. Chỉ làm được nếu sau này video self-host (mp4/HLS).
- [x] FE-9.5: Control tự vẽ bổ sung nút toàn màn hình (ẩn `controls` làm mất luôn nút fullscreen gốc) — `requestFullscreen()` trên wrapper để control tự vẽ vẫn hiện khi toàn màn hình

## Verify Phase 9

- [x] Bài cấm tua (lesson 7, khoá `sa-tai-sao-lai-co-thong-tin-sai-lech`) → iframe có `controls=0&disablekb=1`, không còn thanh tua YouTube
- [x] Control tự vẽ chạy đúng: Play/Pause đổi trạng thái, đồng hồ chạy `0:39 / 3:12`, thanh tiến độ 20.3% khớp 39/192
- [x] Ép `seekTo(170)` qua JS API của iframe → vị trí KHÔNG nhảy tới 2:50, phát tiếp bình thường từ mốc đã xem
- [x] Chọn 2x → đồng hồ chạy 0:41 → 0:51 trong 5 giây thật (đúng 2x), nút 2x sáng
- [x] Menu bánh răng: mở ra đủ 5 mốc `0.5x / 1x / 1.25x / 1.5x / 2x`, tick đúng mốc đang chọn, click ra ngoài đóng menu
- [x] Nút toàn màn hình → `document.fullscreenElement` = wrapper, video cao 824/876px, control bar vẫn hiện, nút đổi thành "Thoát toàn màn hình"; thoát về lại bình thường
- [ ] Override cấp môn học "Cho tua video = Không" → lưu lại → DB lưu boolean false (BE đã verify bằng unit-run, chưa test qua UI admin)
- [ ] Tua thẳng tới cuối video → KHÔNG chuyển "Hoàn thành" (chưa test tay)
- [ ] Xem hết video bình thường → vẫn đạt 100% → "Hoàn thành" (chưa test tay)

### Checkpoint — 2026-07-16

Vừa hoàn thành: Phase 9 — fix "chặn tua không có hiệu lực" (1 file BE + 1 file FE).
- Nguyên nhân 1: `SubjectBuilderRequest` thiếu chuẩn hoá boolean → select2 gửi chuỗi `"false"` → lưu thẳng vào cột JSON → FE so sánh `=== false` không khớp. Bằng chứng: `subject_lessons` id 30 lưu `"true"` kiểu STRING trong khi `lessons` lưu `false` kiểu BOOLEAN.
- Nguyên nhân 2: `YoutubePlayer` handler ENDED gán `played = getDuration()` vô điều kiện; kéo tua tới cuối làm YouTube bắn ENDED mà không qua PLAYING → vòng poll chặn tua không kịp chạy.
- Giải pháp cuối (user chốt): khoá cứng bằng `controls: 0` + control tự vẽ, thay vì chỉ snap-back.

Đang làm dở: Không.
Bước tiếp theo: Test tay 3 mục Verify còn lại (luồng ENDED + lưu override qua UI admin).
Blocked: Không.
