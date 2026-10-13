# Danh mục Vụ việc (HRM) — port từ ERP

**Trạng thái:** Design đã duyệt (2026-07-31). Chờ writing-plans.
**Nhánh:** `gop_db` (hrm-api + hrm-client).
**Spec đầy đủ:** `docs/superpowers/specs/2026-07-31-danh-muc-vu-viec-hrm-design.md`

## Mục tiêu
Đưa "Danh mục vụ việc" (bảng `works`, mã vụ việc kế toán) từ ERP sang HRM, menu ở phân hệ **Tài chính**. Nằm trong lộ trình Gộp DB (hợp nhất 2 app, dùng chung 1 DB gộp).

## Quyết định chốt (brainstorm 2026-07-31)
- **DB/nhánh:** `gop_db`, DB đã gộp. Entity `Work` connection mặc định (KHÔNG mysql2). Dùng thẳng bảng `works`, không thêm cột.
- **Module BE:** `Modules/Finance` (stub có sẵn, route `/v1/finance`).
- **Phân cấp:** toàn cục — không `company_id`, không phân cấp.
- **Permission:** 2 quyền — `Xem danh mục vụ việc`, `Quản lý danh mục vụ việc`.
- **Rule xóa/khóa:** port y hệt ERP — đã dùng trong hạch toán (`account_details.work_id`) → không xóa, không khóa.
- **FE:** V2Base (skill `list-page`): FilterPanel (keyword + trạng thái) + DataTable + Pagination + modal thêm/sửa.
- **Menu:** Tài chính › Danh mục - kế toán › Danh mục vụ việc → `/finance/works`.

## Nguồn ERP
- `app/Model/Accounting/Work.php`, `app/Http/Controllers/Accounting/WorksController.php`, view `resources/views/accounting/works/`.
- Bảng `works`: code(unique)/name(required)/note/status(1/2)/created_by/updated_by. canDelete = không có `account_details.work_id`.
