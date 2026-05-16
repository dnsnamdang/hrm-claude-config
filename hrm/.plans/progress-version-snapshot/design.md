# Progress Version Snapshot — Design Tóm tắt

**Spec chi tiết:** `docs/superpowers/specs/2026-04-29-progress-version-snapshot-design.md`

## Mục tiêu
Khi tạo version mới cho giải pháp/hạng mục, snapshot lại `weight` + `progress_percent` của version cũ vào bản ghi version tương ứng (lịch sử, không hiển thị UI). Tab Tiến độ giải pháp có hạng mục chỉ hiện hạng mục thuộc version giải pháp hiện tại.

## Scope
- BE only — không thay đổi FE
- 2 migration, 2 service file

## Quyết định chính
- Thêm `progress_percent` vào `solution_versions`
- Thêm `weight` + `progress_percent` vào `solution_module_versions`
- Không tạo bảng mới, không thay đổi logic đọc/ghi weight hiện tại
- Filter module theo `solution_module_versions.solution_version_id = current_version_id`
