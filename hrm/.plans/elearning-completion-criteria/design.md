# elearning-completion-criteria — Tóm tắt

> Owner: @junfoke · Ngày: 2026-06-04
> Spec đầy đủ: `docs/superpowers/specs/2026-06-04-elearning-completion-criteria-enforcement-design.md`

## Mục tiêu
Đợt này làm **Hướng A** (khớp form cấu hình với enforcement thật) + **thêm option SCORM** `browsed`/`viewed` để gói content single-page hoàn thành được.

## Bối cảnh
Audit cho thấy chỉ 4 nhóm tiêu chí thực sự enforce: video `watch%`, text/file `min_read_seconds`, SCORM `completion rule + min_score`. Các tiêu chí scroll/dwell/seek/active-tab chỉ lưu config, player bỏ qua. Bug: form tạo bài text/file chỉ cho nhập "%" (không enforce) còn trường thực dùng `min_read_seconds` lại nằm ở form override → bài luôn xong sau 30s mặc định.

## Quyết định chốt
- Trường chưa enforce: **giữ + nhãn "(chưa áp dụng)"**, vẫn nhập được.
- Form tạo bài text/file: **giữ % + thêm "Min thời gian đọc (giây)"**.
- SCORM: **thêm `browsed` + `viewed`**; `viewed` = hoàn thành ngay khi Initialize (opened).
- Không migration. Không sửa enforce hiện có của video/text/file.

## Phạm vi
5 file: 1 FE elearning (`scorm.js`), 2 FE hrm-client (LessonForm, SubjectLessonCompletionOverride), 2 BE (LessonRequest, LearningSessionService).

## Hướng B (sau)
Implement scroll/dwell/seek-block/active-tab/heartbeat-config/allow-download → gỡ dần nhãn "(chưa áp dụng)".
