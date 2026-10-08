# Dự án TKT — chỉ người tạo được sửa

Người phụ trách: @namdangit · Spec: `docs/superpowers/specs/gop-db/2026-10-08-du-an-tkt-chi-nguoi-tao-duoc-sua-design.md` · Nhánh: `gop_db` (hrm-api + hrm-client) · Chốt: 2026-10-08

## Quyết định đã chốt

- **Sửa form chính (PUT) + Lưu phiếu thu thập thông tin** → CHỈ người tạo (`prospective_projects.created_by`).
- 4 quyền "Xem danh sách dự án tiền khả thi theo tổng công ty | công ty | phòng ban | bộ phận" → chỉ còn là quyền XEM.
- KD hỗ trợ / Phòng KD hỗ trợ → chỉ xem (như trước).
- **Đóng dự án, Đóng dự án cha, Chốt giải pháp, Gửi đề xuất gia hạn** → GIỮ NGUYÊN quy tắc riêng: chỉ NV KD phụ trách
  (`main_sale_employee_id`), kiểm ở service. Không đi qua `canEdit()`.
- Xoá → giữ nguyên `canDelete()` (người tạo + trạng thái Đang tạo + không có dự án con).

## Lịch sử

- 29/12/2025 (khoipv) — màn ra đời, PUT không gate gì, ai thấy dự án là sửa được.
- 10/09/2026 (Manh Cuong, `6fdec08de` / `e554e0e2f`) — thêm `canEdit()` + middleware `prospectiveProjectCanEdit`:
  người tạo HOẶC trong phạm vi 4 quyền Xem; KD hỗ trợ chỉ xem.
- 08/10/2026 — thu về chỉ người tạo (task này). Push `gop_db`: hrm-api `b7083c389` · hrm-client `72a537559`.

## Thay đổi

- `ProspectiveProject::canEdit()` → `created_by === auth()->id()`. Bỏ `isInPermissionScope()` + 3 subquery
  `is_in_permission_scope` ở `ProspectiveProjectService` (index / getAll / getForMeeting) vì không còn ai đọc.
- `scopeByViewPermission()` GIỮ — vẫn dùng để lọc danh sách.
- Middleware, Resource (`can_edit`), FE (ẩn nút Sửa / Lưu phiếu, chuyển `/edit` → `/manager`) không đổi logic, chỉ sửa comment.

## Còn tồn

- SRS Dự án TKT (`srs-man-docs/prospective-projects/gen_srs.py` — mục Chỉnh sửa + BR-10) còn ghi quy tắc cũ
  "người tạo HOẶC phạm vi quyền xem" → cần cập nhật + sinh lại docx.
