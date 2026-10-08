# Plan — Dự án TKT: chỉ người tạo được sửa

## Phase 1 — Thu quyền sửa về người tạo

### BE (hrm-api)
- [x] `ProspectiveProject::canEdit()` chỉ còn so `created_by` với `auth()->id()`
- [x] Bỏ `isInPermissionScope()` + 3 subquery `is_in_permission_scope` trong `ProspectiveProjectService`
- [x] Cập nhật comment middleware `CheckProspectiveProjectCanEdit` + route

### FE (hrm-client)
- [x] Cập nhật comment `index.vue` / `_id/edit.vue` (logic đã đọc `can_edit` từ BE)

### Kiểm
- [x] API thật: không phải người tạo (quyền tổng công ty) → detail/list `can_edit=false`, PUT 403, save-form-answers 403
- [x] API thật: người tạo → `can_edit=true`, PUT lọt middleware (422 validate)
- [x] Playwright MCP: không phải người tạo → `/edit` chuyển `/manager`, chi tiết không có Sửa/Lưu, 10/10 dòng danh sách không có Sửa;
      người tạo → ở lại form, có "Lưu nháp" + "Lưu"
- [x] Spec mới `e2e/tests/assign/prospective-project-can-edit.api.spec.ts` — 6/6 passed (chạy riêng)

- [x] Commit + push `gop_db`: hrm-api `b7083c389` · hrm-client `72a537559` (đặt sau commit mới của remote, không stash việc dở session khác)

### Checkpoint — 2026-10-08 (wrap up)
Vừa hoàn thành: code + kiểm API/UI + spec e2e + push gop_db cả 2 repo; sau đó commit+push toàn bộ theo yêu cầu
  (kèm code CSKH tiềm năng của session khác: hrm-api `c448133eb`, hrm-client `fb0e46bc9`; plans `c63a255`)
Đang làm dở: —
Bước tiếp theo: cập nhật SRS Dự án TKT (mục Chỉnh sửa + BR-10 trong srs-man-docs/prospective-projects/gen_srs.py) nếu user yêu cầu
Blocked:
