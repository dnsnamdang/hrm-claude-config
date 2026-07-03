# ERP Cost Catalog — Quản lý Dịch vụ & Chi phí từ danh mục ERP (BOM + Quotation) — Tóm tắt

## Mục tiêu

Chuẩn hoá dòng **dịch vụ & chi phí** trong **BOM** và **Quotation** về **một danh mục ERP duy nhất** (bảng `costs`, mysql2), thay vì nhập tay tên free-text. Nếu mục chưa có → **tạo nhanh** ghi thẳng vào danh mục ERP rồi dùng luôn.

## Scope

- Chọn dịch vụ/chi phí từ danh mục `costs` ERP (cả `kind_of=2` Dịch vụ + `kind_of=1` Chi phí khác).
- Tạo nhanh mục mới → ghi trực tiếp `costs` (+ `company_costs` cho chiết khấu) trên mysql2 (mirror popup ERP).
- Áp dụng cho **cả BOM và Quotation** (component FE + endpoint BE dùng chung).
- Backward-compat: dòng cũ nhập tay (`cost_id=null`) vẫn chạy.

## Hiện trạng ERP (DB `erp2326`, đã xác minh)

- Bảng `costs`: `id, name, en_name, type, status, kind_of, rate_value_capital, revenue_calculation, vat_percent, created_by, updated_by, timestamps`. **Không có `code`, không có ĐVT.**
- **Chỉ dùng `status=1 && kind_of=2`, `type=null`.** Phân 2 loại bằng `revenue_calculation`:
  - `revenue_calculation=1` → **Dịch vụ có tính doanh thu**
  - `revenue_calculation=0` → **Chi phí khác**
- (kind_of=1 / cột `type` của ERP KHÔNG dùng trong feature này.)
- Chiết khấu → bảng `company_costs` (theo `company_id`).
- Popup gốc tham chiếu: `TanPhatDev/app/Http/Controllers/Accounting/CostsController.php` + `resources/views/accounting/costs/index.blade.php`.
- Tiền lệ HRM ghi mysql2: `Modules/Assign/.../AssignBusinessController::update` → `syncAssignBusinessErp`.

## Quyết định lớn (chốt qua brainstorming)

| Hạng mục | Quyết định |
|---|---|
| Nguồn danh mục | Bảng `costs` ERP; hiện cả kind_of=1 & 2, có badge + filter loại |
| Liên kết HRM | Thêm `cost_id` (nullable) vào `quotation_service_items` + `bom_list_products` |
| Tự điền khi chọn | Lấy `name` + `vat_percent` từ catalog; **VAT cho sửa**; **bỏ ĐVT** (unit_id=null); giá nhập tay |
| Cấu trúc dòng | Giữ đầy đủ: SL + giá nhập + giá bán + CK + VAT → thành tiền (chỉ bỏ ĐVT). **SL mặc định = 1, KHÓA không cho sửa** |
| Tạo nhanh | Form gọn: **Loại** (selectbox, mặc định chưa chọn: "Dịch vụ có tính doanh thu" rev=1 / "Chi phí khác" rev=0) + **Tên** + **%VAT**. Đều ghi `kind_of=2, type=null, revenue_calculation` tương ứng. Bỏ chiết khấu / tỷ lệ giá vốn / tên TA / loại chi phí / checkbox |
| Ghi ERP | Ghi trực tiếp mysql2 vào `costs` qua model `TpCost`; `created_by` resolve qua `TpEmployee` (employee_info_id) |
| Quyền tạo nhanh | Mọi user sửa được báo giá/BOM (KHÔNG thêm permission riêng) |
| Validate tên | Unique theo `type` (giống ERP); BE rethrow `ValidationException`; FE lỗi inline |
| Phạm vi | Cả BOM và Quotation |

## Spec chi tiết

- Backend: `design-phase1.md`
- Frontend: `design-phase2.md`

## Liên quan

- Branch: `tpe-develop-assign`
- Kế thừa từ: `Bomlist-Quotation` (BOM + báo giá), `quotation-redesign` (báo giá độc lập)
- Người phụ trách: @dnsnamdang
