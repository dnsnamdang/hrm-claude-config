# elearning-tracking-fix — Design (tóm tắt)

**Owner:** @junfoke
**Ngày:** 2026-06-02
**Tiếp nối:** [learning-session-api], [elearning-lesson-viewer]

## Mục tiêu

Sửa cơ chế theo dõi & đánh dấu "đã xong" bài học trên màn học (elearning), cho 3 loại nội dung video / tài liệu / bài viết — để phản ánh việc học THẬT thay vì đếm thời gian mở trang.

## Hiện trạng (vấn đề phát hiện)

1. **Hiển thị thời gian làm tròn**: video 3:12 hiện "4p". Do `total_minutes = ceil(duration/60)` và BE `/learn` chỉ trả `minutes`, FE hiển thị `{{ minutes }}p`. Helper `formatLessonDuration(seconds)` đã có nhưng learn view không dùng. DB đã lưu `lessons.duration` (giây).
2. **Đánh "đã xong" — backend ĐÚNG theo config** (`checkCompletion` đọc `getEffectiveTracking`: override subject_lesson → lesson.tracking_completion → default). Nhưng:
   - (A) Video tracking GIẢ: `YoutubePlayer` là iframe thường + `setInterval` đếm wall-clock, không đọc playback thật → mở tab là tự xong; lại lấy `minutes` (đã ceil) làm mẫu số.
   - (B) `completionHint` hardcode "≥80%"/"≥30s", không đọc `completion_rule` BE gửi (riêng SCORM đọc đúng).
   - (C) Nhiều key config (`*_min_scroll_percent`, `*_require_scroll_end`, `video_require_active_tab`, `video_allow_seek`...) chưa được enforce. → Ngoài scope đợt này, ghi nhận cho sau.
3. **Heartbeat scale**: 30s/lần, 500 user ≈ 17 req/s — rất nhẹ. Unique index đã có; `recalculateCourseProgress` chỉ chạy khi `justCompleted`. Chưa cần Redis/queue. Điểm cần sửa: heartbeat cuối bị mất khi đóng tab (axios async), và FE vẫn gửi request thừa sau khi bài đã done.

## Quyết định

- Video: dùng **YouTube IFrame Player API** (MIỄN PHÍ, không cần API key/quota — khác YouTube Data API) để đếm giây PLAYING thật + `getDuration()` thật.
- Hiển thị thời gian: BE trả thêm `duration` (giây) → FE `formatLessonDuration`.
- Hint: đọc từ `completion_rule`.
- Scale: thêm flush qua `fetch(keepalive:true)` lúc `pagehide`; dừng đếm khi bài đã done. KHÔNG thêm Redis/queue (premature cho 500). Ghi chú đường nâng cấp khi scale nghìn.
- Tài liệu/bài viết: giữ cơ chế đếm giây hiện tại đợt này (B/(C) phần focus+scroll defer), chỉ đảm bảo hiển thị + hint + scale.

## Scope đợt này

| # | Hạng mục | Phía |
|---|---|---|
| 1 | Hiển thị 3:12 thay vì "4p" | BE + FE |
| 2 | Hint completion theo config | FE |
| 3 | Video tracking thật (IFrame API) | FE |
| 4 | Tối ưu heartbeat (keepalive unload + dừng khi done) | FE |

## Out of scope (ghi nhận sau)

- Enforce đầy đủ các tiêu chí config nâng cao (scroll %, dwell/trang). `require_active_tab` + `allow_seek` đã enforce ở Phase 9.
- Siết tracking tài liệu theo focus+visible (Page Visibility) — đề xuất nhưng chưa làm.
- Redis buffer / queue cho heartbeat (chỉ khi scale lên hàng nghìn concurrent).
- Chỉnh **chất lượng video**: không khả thi với YouTube embed (API `setPlaybackQuality` đã bị deprecate, chất lượng auto theo băng thông). Chỉ làm được nếu chuyển sang video self-host (mp4/HLS).

---

## Phase 9 — Chặn tua video "cứng" (BE + FE) — 2026-07-16/17

**Bug:** cấu hình "Cho tua video = Không" không có hiệu lực; tua thẳng tới cuối vẫn tính "Hoàn thành".

**Root cause 1 (BE):** `SubjectBuilderRequest` (cấu hình override cấp môn học) thiếu `prepareForValidation()` chuẩn hoá boolean → select2 gửi chuỗi `"false"` được ghi thẳng vào cột JSON `tracking_completion_override`. FE so sánh `=== false` với chuỗi `"false"` → trượt → coi như chưa cấu hình. (Bằng chứng DB: `subject_lessons` lưu `"true"` kiểu STRING trong khi `lessons` lưu `false` kiểu BOOLEAN — vì `LessonRequest` đã có normalize, còn `SubjectBuilderRequest` thì chưa.)

**Root cause 2 (FE):** handler `ENDED` gán `played = getDuration()` vô điều kiện; kéo tua tới cuối làm YouTube bắn ENDED mà không qua PLAYING → vòng poll chặn tua không kịp chạy.

**Quyết định (user chốt):** khoá cứng thay vì chỉ snap-back.
- Bài cấm tua → `playerVars.controls = 0` + `disablekb = 1` (bỏ hẳn thanh tua + phím tắt của YouTube), thay bằng **control tự vẽ**: Play/Pause, thanh tiến độ read-only, mm:ss, icon khoá, menu bánh răng chọn tốc độ (0.5/1/1.25/1.5/2x), nút toàn màn hình (`requestFullscreen` trên wrapper để control tự vẽ còn hiện).
- Cấm tua **KHÔNG** cấm xem nhanh (PM yêu cầu). Trần 2x nằm dưới `SEEK_THRESHOLD` (4) nên tiến độ vẫn cộng đúng.
- Bài cho phép tua giữ nguyên control gốc YouTube.
- Snap-back (kéo về `maxReached`) giữ làm lớp phòng thủ cuối; `blockSeek()`/`requireActiveTab()` parse được cả boolean lẫn chuỗi cũ trong DB.

## Phase 10 — Resume vị trí xem video (FE) — 2026-07-17

**Bug:** mở lại bài video luôn phát từ 0.

**Giải pháp:** tận dụng `read_seconds` (BE đã lưu qua heartbeat, trả trong payload lesson) — **KHÔNG đổi DB**.
- `LessonViewer` truyền `:resume-seconds` = `lesson.read_seconds`; bài `done` → 0 (phát lại từ đầu, **user chốt**).
- `YoutubePlayer` dùng **playerVar `start`** (áp lúc tạo player, không gọi API động): video cued sẵn tại mốc resume, hiện thumbnail, không tự phát; `seedResume()` seed `played`/`maxReached`/`curTime` để tính tiếp + chặn tua vẫn đúng.
- **Lý do KHÔNG dùng `seekTo`/`pauseVideo` động:** bản đầu gọi `seekTo`+`pauseVideo` lúc onReady → trên prod có extension chặn quảng cáo phá iframe YouTube (`postMessage origin mismatch` + `ERR_BLOCKED_BY_CLIENT`), player ở trạng thái lỗi → seekTo để lại **màn đen** khi tắt tab vào lại. `start` playerVar né hoàn toàn vì không đụng player sau khi tạo.

**Files:** BE `Modules/Training/Http/Requests/Subject/SubjectBuilderRequest.php`; FE `components/learning/viewers/YoutubePlayer.vue` + `components/learning/LessonViewer.vue`.
