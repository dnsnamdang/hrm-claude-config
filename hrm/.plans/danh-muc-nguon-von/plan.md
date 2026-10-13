# Danh mục nguồn vốn (port ERP → HRM) — plan

Port `source_capitals` (ERP SourceCapital) sang HRM Modules/Finance.
Khác vụ việc/mã phí: CHỈ field `name`; "Xóa" = khóa mềm (status 1→0, mirror ERP,
KHÔNG check tham chiếu); danh sách chỉ hiện status=1 (đang hoạt động).
Toàn cục, 1 quyền "Quản lý danh mục nguồn vốn". Route source-capitals.

## Tasks
- [x] BE Entity `SourceCapital` (name, status; STATUS_ACTIVE=1/BLOCK=0)
- [x] BE Service (list status=1 + filter name; create; update name; block=xóa mềm)
- [x] BE Controller V1
- [x] BE Request (name required|unique)
- [x] BE Resource List + Detail
- [x] BE Routes group source-capitals gate "Quản lý danh mục nguồn vốn"
- [x] BE Seeder permission
- [x] FE pages/finance/source-capitals/{index.vue, SourceCapitalModal.vue} (chỉ name)
- [x] FE finance.js: "Danh mục nguồn vốn" → /finance/source-capitals
- [x] DB erp_hrm_check: tạo + gán quyền role 18
- [x] php -l + verify

### Checkpoint — 2026-08-04
Vừa hoàn thành: BE+FE nguồn vốn (chỉ name, xóa=khóa mềm) + quyền, push gop_db. Bước tiếp: user verify.
Blocked:

---

## Bugfix — 405 khi bấm Sửa (proactive, cùng pattern)
**Root cause:** route group `source-capitals` thiếu `GET /{id}` (show); FE `SourceCapitalModal:68` gọi `GET finance/source-capitals/{id}` → sẽ 405 (chưa report nhưng chắc chắn lỗi).
**Fix (BE):** `SourceCapitalService::getSourceCapital` + `SourceCapitalController::show` + route `GET /{id}` (checkPermission:Quản lý danh mục nguồn vốn). Verified.