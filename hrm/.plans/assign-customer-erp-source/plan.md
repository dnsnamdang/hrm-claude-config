# Plan — Luồng dự án Assign đọc Khách hàng từ ERP (không dùng bảng customers HRM)

Phụ trách: @namdangit — Worktree: HRM-tpe (nhánh tpe)

**Bối cảnh:** KH của luồng dự án (meeting → dự án TKT → BOM → báo giá) là customer_id ERP (nguồn màn /assign/customers = CustomerService đọc trực tiếp ERP qua App\Models\TpCustomer, connection mysql2). Bảng `customers` HRM chỉ chứa tập KH đã sync → đọc HRM trả null cho KH chưa sync. Directive: mọi chỗ luồng dự án đọc KH phải từ ERP (TpCustomer/mysql2).

**Scope lần này:** CHỈ lõi luồng dự án. Ngoài scope (giao việc, báo cáo, quyết toán HĐ) để sau.

## Phase 1 — Chuẩn bị model ERP
- [x] BE: Thêm relation `contacts()` (hasMany TpCustomerContact, mysql2) vào `App\Models\TpCustomer` — phục vụ các chỗ `->with(['contacts'])`

## Phase 2 — Thay nguồn KH ở lõi luồng dự án
- [x] BE: `Entities/BomList.php` — relation `customer()` → TpCustomer (ảnh hưởng BomListListResource customer_name/code)
- [x] BE: `Entities/ProspectiveProject.php` — relation `customer()` → TpCustomer
- [x] BE: `Transformers/MeetingResource/MeetingResource.php` + `MeetingTransformer.php` — `Customer::with(['contacts'])` → TpCustomer
- [x] BE: `Transformers/ProspectiveProjectResource/DetailProspectiveProjectResource.php` — block `$customers` (dòng 19) → TpCustomer (đồng bộ với customer_type đã đọc ERP sẵn)
- [x] BE: `Http/Controllers/.../MeetingController.php::getListCustomer` → TpCustomer
- [x] BE: `Http/Controllers/.../ProspectiveProjectController.php::searchCustomers` → TpCustomer
- [x] BE: `Http/Requests/Meeting/MeetingCreateApiRequest.php` + `MeetingUpdateApiRequest.php` — `optional(Customer::find)->customer_type` → TpCustomer
- [x] BE: `Http/Requests/ProspectiveProject/ProspectiveProjectRequest.php` — 3 chỗ `Customer::find->customer_type` → TpCustomer
- [x] BE: `Services/QuotationService.php` — 3 chỗ `Customer::find($project->customer_id)` → TpCustomer
- [x] BE: `Services/MeetingService.php:316` — fallback `Customer::find` → TpCustomer (đồng bộ fix email trước đó)

## Verify
- [ ] Meeting detail: KH + người liên hệ hiển thị đúng (kể cả KH chưa sync HRM)
- [ ] Dự án TKT detail: KH, loại hình, người liên hệ đúng
- [ ] BomList list: customer_name/code đúng; update BomList đổi KH → log hiện tên KH
- [ ] Báo giá tạo từ dự án: snapshot customer_name/email/... đúng

## Ghi chú
- `CUSTOMER_TYPES` là hằng PHP (map id→tên), KHÔNG phải đọc bảng HRM → giữ nguyên.
- `RequestSolution` import Customer HRM nhưng không thực dùng → bỏ qua.

### Checkpoint — 2026-07-17
Vừa hoàn thành: Phase 1 + Phase 2 — chuyển toàn bộ lõi luồng dự án đọc KH sang ERP (TpCustomer/mysql2). Đã sửa 13 file (2 entity relation, 2 meeting resource, detail PP resource, 2 controller picker, 3 request, QuotationService, MeetingService, + thêm relation contacts() vào TpCustomer). getListCustomer rewrite join provinces/wards dựng địa chỉ ERP. QuotationService đổi $customer->name→fullname. Lint OK toàn bộ. Verify tinker: BomList/PP->customer->fullname resolve đúng KH ERP chưa sync HRM; TpCustomer->contacts hoạt động.
Đang làm dở: Không
Bước tiếp theo: User test UI (meeting detail, dự án TKT detail, BomList list/update, báo giá) trên :3001. Ngoài scope: giao việc/báo cáo/quyết toán HĐ vẫn đọc HRM (chưa đụng).
Blocked: Không

### Review self-audit — 2026-07-17
Đọc toàn luồng. Kết luận: fix ĐÚNG & AN TOÀN. Bằng chứng: không có whereHas/join('customers') trên relation đã đổi (chỉ ReportController join HRM — ngoài scope); eager with('customer') chạy cross-connection (tinker OK); resources (BomList list, PP detail/list, Meeting) đều dùng field ERP có sẵn; FE meeting chỉ đọc form.customer.contacts (TpCustomer đã cấp); không còn `Customer::` trần undefined.
Phát hiện phụ (KHÔNG do migration gây ra, chưa tự sửa — cần hỏi):
- RequestSolution.php:148 `$project->customer->type` → HRM Customer cũng không có `type`/accessor (chỉ customer_type) nên VỐN null → mã YCP luôn 'TC'. Migration giữ nguyên hành vi. Nên đổi `->type` → `->customer_type` để CN/TC đúng (đổi hành vi production → hỏi).
- DetailProspectiveProjectResource.customerTypeText dùng Human::CUSTOMER_TYPES (5 loại) trong khi ERP customer_type = 1 Cá nhân / 2 Tổ chức → type=2 hiện "Doanh nghiệp tư nhân" thay vì "Tổ chức" (pre-existing).
Thay đổi hành vi có chủ đích: getListCustomer đổi filter status=1 → is_customer=1 (khớp CustomerService /assign/customers).
Khuyến nghị nhỏ: searchCustomers (PP) nên thêm ->where('is_customer',1) cho nhất quán.

## Bug fix — Lưu KH vỡ FK customer_registers (2026-07-21)
- [x] BE: `Modules/Assign/Services/CustomerService.php` — thay `syncErpContacts` xóa-hết-tạo-lại bằng UPSERT theo id giống hệt ERP `Customer::syncContacts`; thêm helper `erpDeletableOldContactIds` (xóa có giới hạn theo quyền ERP) + `erpEmployeeRoleNames` (đọc employee_has_roles→roles trên mysql2). Chỉ xóa contact bị bỏ khỏi form & trong phạm vi quyền → không đụng contact bị customer_registers/báo giá trỏ tới → hết lỗi FK 1451.
- [x] FE: `components/assign-components/customer/CustomerForm.vue` — payload contact gửi kèm `id` để BE diff/upsert (trước đó bị cắt mất id nên BE buộc xóa hết).

### Checkpoint — 2026-07-21
Vừa hoàn thành: Fix lỗi SQLSTATE 23000 (FK customer_registers) khi lưu /assign/customers/{id}/edit — chuyển sync contact sang upsert theo id giống ERP, quyền xóa lấy từ ERP. Lint BE OK.
Đang làm dở: Không
Bước tiếp theo: User test UI lưu KH #34 (và KH có contact đang bị đăng ký) trên môi trường dev.
Blocked: Không
