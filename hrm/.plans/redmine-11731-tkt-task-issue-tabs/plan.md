# Redmine #11731 — Dự án TKT: tab Nhiệm vụ / Vấn đề + lọc nhanh Nhiệm vụ (@manhcuong)

## Phase 1 — Fix
- [x] BE: `TaskService` — keyword ở tab Nhiệm vụ của dự án/meeting chỉ tìm mã, tên nhiệm vụ (bỏ khách hàng khi có `prospective_project_id`/`meeting_id`)
- [x] FE: `TaskListTab` placeholder "Tìm theo mã, tên nhiệm vụ"
- [x] FE: `solutions/components/manager/IssueTab` — tách cột Mã / Tên vấn đề, nút về cột Hành động cuối (V2BaseRowActions, khuôn /assign/issues), gộp cấu hình cột bằng `mergeColumnCustomization`
- [x] FE: `/assign/tasks` tooltip lọc nhanh "Task tôi …" → "Nhiệm vụ tôi …"
