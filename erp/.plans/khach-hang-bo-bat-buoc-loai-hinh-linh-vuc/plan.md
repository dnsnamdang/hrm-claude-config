# Khách hàng — bỏ bắt buộc Loại hình hoạt động / Lĩnh vực kinh doanh (ERP + HRM) — @cuong61n

Yêu cầu (chị Lệ nhờ qua chat 02/11/2026): màn quản lý khách hàng bỏ bắt buộc 2 trường
"Loại hình hoạt động khách hàng" và "Lĩnh vực kinh doanh khách hàng".

## Phase 1
- [x] 02/11/2026 — Rà HRM (`hrm-client` CustomerForm.vue, `hrm-api` Save/UpdateCustomerRequest): 2 trường đã `nullable`, nhãn không có `(*)`, cờ `scopeTouched` không bao giờ bật → không còn bắt buộc, KHÔNG phải sửa.
- [x] 02/11/2026 — Rà ERP BE `Sale/CustomersController` (store + update): rule đã `nullable` → không chặn; các message `.required` còn lại là code chết, để nguyên.
- [x] 02/11/2026 — ERP FE: bỏ dấu `(*)` đỏ trên nhãn 2 trường ở `customercare/customermanager/show_.blade.php` (màn trong ảnh) và `partials/modals/searchCustomer.blade.php` (popup tạo nhanh khách hàng). Nhánh `gop_db`, chưa commit.
- Kiểm: grep không còn `(*)` cạnh 2 nhãn; chưa chạy trình duyệt (chỉ đổi nhãn).
- [x] 02/11/2026 — Đã đẩy `gop_db` (commit cb2f99ff04) và pull lên PROD ERP (/var/www/html/TanPhatDev, nhánh gop_db).
- Trạng thái: đã deploy PROD ERP 02/11/2026.
