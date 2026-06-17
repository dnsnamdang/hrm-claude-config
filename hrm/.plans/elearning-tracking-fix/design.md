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

- Enforce đầy đủ các tiêu chí config nâng cao (scroll %, dwell/trang, require active tab, seek limit).
- Siết tracking tài liệu theo focus+visible (Page Visibility) — đề xuất nhưng chưa làm.
- Redis buffer / queue cho heartbeat (chỉ khi scale lên hàng nghìn concurrent).
