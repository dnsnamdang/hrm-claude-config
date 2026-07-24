# Plan — Bỏ bắt buộc Loại hình + Lĩnh vực KH (form Khách hàng, ERP+HRM)

Người phụ trách: @manhcuong

Bỏ `required` + dấu `*` cho 2 trường "Loại hình hoạt động khách hàng" (customer_scope_group) và "Lĩnh vực kinh doanh khách hàng" (customer_scope) ở form tạo/sửa Khách hàng, đồng bộ 3 form (ERP + HRM Human + HRM Assign).

## FE (3 file)
- [x] HRM Human `components/human-components/customer/CustomerScopeSelect.vue` (dòng 5,25): bỏ `<span class="field-required">(*)</span>` (nhãn "Nhóm lĩnh vực khách hàng" + "Lĩnh vực khách hàng")
- [x] HRM Assign `components/assign-components/customer/CustomerForm.vue`: bỏ 2 `<Required />` (dòng 88,181); bỏ block chặn submit client-side trong `submitSave()` (kiểm tra ≥1 phần tử); `scopeTouched` giờ luôn false → cờ đỏ bắt buộc tự tắt, giữ lỗi quan hệ BE (Lĩnh vực không thuộc loại hình)
- [x] ERP `TanPhatDev/resources/views/partials/customers/customerForm.blade.php` (dòng 64,77): bỏ `<span class="text-danger">(*)</span>`

## BE (5 file — required → nullable, giữ closure exists/quan hệ)
- [x] HRM Human `Modules/Human/Http/Requests/SaveCustomerRequest.php` (35,36): customer_scope_group_id + customer_scope_id
- [x] HRM Human `UpdateCustomerRequest.php` (36,37)
- [x] HRM Assign `Modules/Assign/Http/Requests/Customer/SaveCustomerRequest.php` (24,27,28,29): customer_scope_group_ids + customer_business_fields + .* subfields
- [x] HRM Assign `Customer/UpdateCustomerRequest.php` (27,30,31,32)
- [x] ERP `TanPhatDev/app/Http/Controllers/Sale/CustomersController.php` store(280,293,322,323) + update(690,703,732,733)

Không đụng service lưu (Human syncCustomerScopes / Assign / ERP syncActivityTypes+syncBusinessFields — đều idempotent với mảng/giá trị rỗng). Không migration/permission.

## Verify
- [x] php -l sạch 5 file BE; grep xác nhận không còn rule `required` cho 2 trường
- [x] Tinker HRM: SaveCustomerRequest (Human) + Customer/SaveCustomerRequest (Assign) — scope rỗng → KHÔNG lỗi cho các key đó (AC2 validation)
- [x] ERP: `nullable|array` + closure foreach an toàn khi rỗng (tinker ERP không chạy được do bootstrap PHP version; xác nhận qua php -l + reasoning)
- [x] Playwright AC1: HRM Human form (/human/customers/add) "Nhóm lĩnh vực khách hàng" + "Lĩnh vực khách hàng" KHÔNG `*`; HRM Assign form (/assign/customers/add) "Loại hình hoạt động khách hàng" + "Lĩnh vực kinh doanh khách hàng" KHÔNG `*` (các field khác vẫn `*`), 0 lỗi console (customer-scope-no-star.png)
- [ ] User E2E: lưu KH để trống 2 trường trên cả ERP + HRM; ERP verify live (ERP app không chạy local)

### Checkpoint — 2026-07-14
Vừa hoàn thành: Bỏ required + `*` cho 2 trường scope ở 3 form (8 file: 3 FE + 5 BE). Verify php -l + tinker HRM + Playwright AC1 2 form HRM.
Bước tiếp: User verify browser (lưu khi trống) + kiểm ERP live.
