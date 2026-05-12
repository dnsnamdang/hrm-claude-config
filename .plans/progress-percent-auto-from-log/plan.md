# Plan: progress-percent-auto-from-log

## Phase 1 — FE ImportResultModal.vue

- [x] FE: Thêm computed `latestLogProgressPct` (filter logs có progress_pct, sort desc theo report_date, lấy dòng đầu)
- [x] FE: Sửa field "Tiến độ hoàn thành (%)" Mode B — đổi v-model → :value, thêm disabled khi is_active, thêm hint text
- [x] FE: Sửa handleSave — progress_percent dùng latestLogProgressPct khi Mode B, result.progress_percent khi Mode A
- [x] FE: Thêm computed progressLogValidationErrors — tiến độ từng kỳ phải tăng dần, không được nhỏ hơn kỳ trước
- [x] FE: Hiển thị lỗi inline per row + block save nếu vi phạm
