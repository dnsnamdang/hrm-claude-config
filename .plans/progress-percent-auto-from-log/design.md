# Design: Tự động tính Tiến độ hoàn thành từ nhật ký

**Feature:** progress-percent-auto-from-log  
**Module:** Giao việc — ImportResultModal  
**Spec đầy đủ:** docs/superpowers/specs/2026-05-04-progress-percent-auto-from-log-design.md

## Mục tiêu

Khi task có `progress_report.is_active = true` (Mode B), field "Tiến độ hoàn thành (%)" không cho nhập tay mà tự động lấy `progress_pct` từ dòng nhật ký có `report_date` gần nhất và có giá trị.

## Quyết định

- Dùng computed property `latestLogProgressPct` (không dùng watcher)
- Chỉ thay đổi FE, BE không đổi
- Field disabled khi Mode B, hiển thị hint text

## Scope

1 file: `hrm-client/pages/assign/tasks/components/ImportResultModal.vue`
