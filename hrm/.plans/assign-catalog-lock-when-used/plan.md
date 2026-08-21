# Plan — Cho phép khóa/mở khóa danh mục dự án dù đã được sử dụng

**Owner:** @junfoke
**Nhánh:** tpe (API + Client)
**Phạm vi:** Module Giao việc (Assign) — 3 màn danh mục còn chặn khóa khi đã dùng.

## Bối cảnh
5 màn được yêu cầu: Hạng mục dự án, Giai đoạn dự án, Loại meeting, Lý do thất bại, Loại tài liệu.
- Hạng mục dự án + Lý do thất bại: `isCanLockUpdate = status==ACTIVE` → đã cho khóa tự do, KHÔNG sửa.
- Giai đoạn dự án + Loại meeting + Loại tài liệu: đang chặn khóa khi đã dùng (BE + FE) → sửa.
- **Giữ chặn Xóa** (`is_can_delete`) như cũ; chỉ mở khóa/mở khóa.

## Backend (hrm-api)
- [x] `MeetingType::isCanLockUpdate()` → `status == STATUS_ACTIVE` (bỏ `!meetings()->exists()`)
- [x] `ProjectPhases::isCanLockUpdate()` → `status == STATUS_ACTIVE` (bỏ `!prospectiveProjects()->exists()`)
- [x] `AttachmentType::isCanLockUpdate()` → `status == STATUS_ACTIVE` (bỏ `files()->count()==0`)
  - Cờ `is_can_lock_update` ở resource tự đúng theo status sau khi sửa.

## Frontend (hrm-client)
- [x] `meeting_type/index.vue`: bỏ `:disabled="!item.is_can_delete"` trên nút khóa; title theo trạng thái
- [x] `project_phase/index.vue`: bỏ `:disabled="item.prospective_projects_count > 0"` trên nút khóa; title theo trạng thái
- [x] `attachment-type/index.vue`: bỏ `:disabled="status===1 && !is_can_lock_update"` trên nút khóa; title theo trạng thái

## Giữ nguyên (KHÔNG đụng)
- Nút Xóa + checkbox chọn dòng (vẫn chặn khi đã dùng — an toàn FK)
- Nút Sửa/Edit; hằng số STATUS; luồng confirm modal

### Checkpoint — 2026-08-13
Vừa hoàn thành: Sửa 3 model BE + 3 màn FE bỏ chặn khóa/mở khóa theo usage.
Đang làm dở: (không)
Bước tiếp theo: User verify UI 3 màn (khóa/mở khóa item đã dùng), xác nhận xóa vẫn bị chặn.
Blocked:
