# Design (tóm tắt) — Hợp đồng (Sale Contract)

> Spec đầy đủ: `docs/superpowers/specs/2026-06-27-contract-design.md`
> Plan chi tiết: `.plans/contract/plan.md`

## Mục tiêu
Thêm **Hợp đồng** trong phân hệ Kinh doanh (Modules/Sale), lập từ **báo giá đã duyệt**, quy trình duyệt giống báo giá, thông tin Bên A (KH) / Bên B (Công ty) đầy đủ, và **mẫu in tuỳ chỉnh** (tái dùng cơ chế print_templates của phân hệ Quyết định).

## Quyết định chốt
- **Module**: `Modules/Sale` + FE `pages/sale/contract` (menu sidebar Kinh doanh "Hợp đồng").
- **Bên A/B**: **snapshot** lên hợp đồng (copy lúc tạo, pre-fill, sửa được — độc lập danh mục).
- **Báo giá → HĐ**: **1-1** (`unique(quotation_id)` + check service).
- **Dòng hàng hoá**: **khoá** (copy nguyên từ báo giá, totals giữ nguyên).
- **Người tạo**: **chỉ created_by của báo giá** mới tạo HĐ từ báo giá đó.
- **Mẫu in**: thêm type "Hợp đồng kinh tế" + bộ biến; bảng hàng hoá render tự động qua `{{BANG_HANG_HOA}}`.
- **Danh mục mở rộng**: +Số TK (KH); +Số TK & người đại diện (Công ty).

## Trạng thái (dùng lại bộ báo giá)
1 Nháp · 2 Chờ duyệt · 3 Đã duyệt · 4 Từ chối. Workflow submit/approve/reject giống báo giá.

## DB
- `sale_contracts` (master): code HD-YYYY-NNNNN, quotation_id unique, customer_id, contract_date, status, approved_at/by, snapshot A (a_*) + B (b_*), discount/totals (copy khoá), print_template_id/type_id/print_template, terms, warranty_time, tổ chức/audit.
- `sale_contract_items` (copy khoá).
- +`bank_account` (category_customers); +`bank_account`,`representative` (companies).

## Permission
Group "Hợp đồng" (type 4), id 1115-1122: Xem tất cả/công ty/phòng ban/bộ phận, Thêm, Sửa, Xóa, Duyệt.

## Tái dùng
- Mẫu in: `print_templates` + `PrintTemplateVariable` + `fillReport()` (`app/Helper/FormatHelper.php`) + FE `FormPrintTemplateComponent` + print page.
- Workflow/phân quyền: pattern `SaleQuotationService`.

## Phase
1. DB + Entities. 2. BE CRUD + workflow + permission + móc tạo-từ-báo-giá. 3. Mẫu in (type + biến + buildPrintData + {{BANG_HANG_HOA}} + /print). 4. FE (menu/list/detail/form+mẫu in/print/nút tạo HĐ). 5. Danh mục mở rộng (Số TK, người đại diện).
