# Plan — Danh mục Khách hàng (Assign)

> Phụ trách: @dnsnamdang · Spec: docs/superpowers/specs/2026-06-09-customer-catalog-design.md
> Module: Modules/Assign (BE) + pages/assign (FE). Ghi 2 nơi: ERP (mysql2) + HRM, link bằng `code`.

---

## Phase 1 — BE: Hạ tầng ghi ERP & sinh mã

### BE
- [x] `app/Models/TpCustomerGroup.php` (mới): connection `mysql2`, table `customer_groups` (dropdown Nhóm KH)
- [x] `app/Models/TpCustomer.php`: thêm `syncGroups($model, $groupIds)` ghi pivot `customer_has_groups` (xóa cũ → insert mới)
- [x] `Modules/Assign/Helpers/CustomerCodeHelper.php`: `generateCustomerCode($provinceId, $wardId)` — port `getPlaceCode`+`convertVNToLatin`+`generateUniqueCodeInTable` (đúng định dạng `base` / `base-01`), đọc geo từ `mysql2`, unique trên ERP
- [x] Fallback khi tỉnh thiếu `license_plate` (2 ký tự đầu tên tỉnh) + Log::warning

## Phase 2 — BE: API danh mục khách hàng

### BE
- [x] `Modules/Timesheet/.../PermissionsTableSeeder.php`: thêm `Quản lý danh mục khách hàng` (id 1099), `Xem danh mục khách hàng` (id 1100), group 'Danh mục', type 4
- [x] `Modules/Assign/Routes/api.php`: group `/assign/customers` (index, customer-groups, show, store POST `/` + `/{id}`) + middleware `checkPermission` (customer-groups đặt trước `/{id}`)
- [x] `CustomerController` (index, show, store, customerGroups) + header `isManagerCustomer`
- [x] `Http/Requests/Customer/SaveCustomerRequest` + `UpdateCustomerRequest`: rule theo `customer_type`, `groups` required min1, unique tax_code/email/mobile/identity trên ERP, address required, **bỏ rule code (auto-gen)**, rethrow qua `failedValidation`
- [x] `Services/CustomerService::index()` — query HRM `customers` + filter (keyword/loại/MST/SĐT/tên đơn vị), phân trang (không phân quyền cấp)
- [x] `Services/CustomerService::save()` — sinh code (create) + `created_by=employee_info_id` (chặn null) → ghi ERP (TpCustomer + sync deputies/contacts/groups, cờ mặc định) → ghi HRM (transaction, rollback + log nếu lỗi); fix contacts.customer_id=$tp->id
- [x] `Services/CustomerService::show()` — HRM customer + deputies/contacts + map geo + group_ids từ ERP theo code
- [x] `Services/CustomerService::customerGroups()` — đọc ERP `customer_groups` (TpCustomerGroup)
- [x] `Transformers/CustomerResource/{CustomerListResource,CustomerDetailResource}.php`
- [x] Uppercase `fullname/account_name/bank_name` khi ghi (cả ERP + HRM)

> **Rủi ro cần test Phase 5** (ghi thẳng ERP):
> - ERP `customers` có nhiều cột NOT NULL — nếu insert thiếu cột nào (vd `type_calculate_interest`, `apartment_number`...) sẽ lỗi "doesn't have a default value" → bổ sung set field khi gặp.
> - `contacts.*.phones` (mảng nhiều SĐT) vs cột ERP `customer_contacts.phones` (chuỗi) — FE/service cần chuẩn hóa định dạng (vd implode `,`). Xác minh khi test KH Tổ chức.

## Phase 3 — FE: Danh sách

### FE
- [x] `store/actions.js`: `getAssignCustomers`, `getAssignCustomer`, `saveAssignCustomer`, `getAssignCustomerGroups`
- [x] `components/menu-sidebar.js`: thêm "Danh mục Khách hàng" ngay TRÊN "Lĩnh vực khách hàng" (isShow Quản lý|Xem) — line 314-318 ✓ AC1
- [x] `pages/assign/customers/index.vue`: `V2BaseFilterPanel` (auto-search deep watcher) + `V2BaseDataTable` (Mã, Tên KH, Loại, MST, SĐT, Email, Nhóm KH, Hành động Xem/Sửa) + nút Tạo mới (ẩn theo quyền `canManage`)

## Phase 4 — FE: Form thêm/sửa

### FE
- [x] `pages/assign/customers/add.vue` + `pages/assign/customers/_id/edit.vue` (wrapper) + `components/assign-components/customer/CustomerForm.vue` (clone+adapt từ Human form)
- [x] Section Thông tin chung: Tên KH*, Loại KH*, Mã (readonly, "Tự sinh khi lưu"), Nhóm KH* (multiselect từ ERP, bind `form.groups[]`)
- [x] Section Cá nhân (type=1): tên đơn vị*, CCCD, ngày/nơi cấp, SĐT*, email, sinh nhật, TK ngân hàng
- [x] Section Tổ chức (type=2): tên viết tắt, công ty mẹ, MST*, email, SĐT bàn*, fax, người đại diện* (bảng), người liên hệ* (bảng), địa chỉ xuất hóa đơn*
- [x] Section Địa chỉ: Quốc gia*, Tỉnh*, Phường/Xã*, Số nhà (dropdown tái dùng action HRM)
- [x] Validate inline: `touched` + `is-invalid` + `invalid-feedback` + map lỗi 422 (`error_messages`/`error_mobiles`)
- [x] Submit → saveAssignCustomer → về danh sách + toast
- [x] Fix `:deep()` → `/deep/` (Vue 2 node-sass)

## Phase 5 — Test thủ công (AC)

- [ ] AC1: menu đúng vị trí (trên Lĩnh vực khách hàng)
- [ ] AC2: form mở đầy đủ trường (cả 2 loại KH) khi Thêm/Sửa
- [ ] AC3: Lưu thành công → kiểm tra bản ghi đúng trong `dev_erp.customers` + bảng con (deputies/contacts/groups) và HRM `customers`
- [ ] Kiểm tra `php -l`, lint FE, build FE

---

### Checkpoint — 2026-06-09 (code xong)
Vừa hoàn thành: Phase 1-4 (BE + FE) code xong, `php -l` sạch toàn bộ, fix `:deep()→/deep/`.
- Phase 1: TpCustomerGroup, TpCustomer::syncGroups, CustomerCodeHelper (sinh mã khớp ERP).
- Phase 2: permission + route + controller + 2 FormRequest + service (save ghi 2 DB) + transformer.
- Phase 3: 4 store action + menu (AC1 ✓) + index.vue.
- Phase 4: CustomerForm.vue + add.vue + _id/edit.vue.
Đang làm dở: Chưa test runtime. Branch `tpe-develop-assign` (cả 2 repo).
Bước tiếp theo: Phase 5 — test browser (cần chạy ERP + hrm-api + hrm-client + seed lại permission). Test AC1/2/3.
Rủi ro chính cần test (ghi thẳng ERP): cột ERP NOT NULL thiếu giá trị; `contacts.phones` mảng vs chuỗi (KH Tổ chức); restore groups/province/ward khi edit; parent_id kiểu số.
Blocked:

## Phase 6 — BE: mở rộng ghi ERP đầy đủ (bám sát ERP tối đa)

### BE
- [ ] Models ERP mới (mysql2): `TpCustomerBankAccount` (customer_has_bank_accounts), `TpCustomerContactBankAccount` (customer_contact_has_bank_accounts), `TpDeliveryPlace` (delivery_places), `TpVehicleManufact` (vehicle_manufacts - read), `TpDistrict`/`TpHamlet` (read)
- [ ] `TpCustomer`: thêm `syncBankAccounts` (customer_has_bank_accounts), `syncVehicleManufacts` (pivot customer_has_vehicle_manufacts), `syncDeliveryPlaces`
- [ ] `applyErpFields` mở rộng: `district_id, hamlet_id, website, note, is_supplier, is_manufacturer` (từ checkbox), `mobile = join(', ', phones[])` (cá nhân), `limit_*/type_calculate_interest` default, `employee_agent_id/level_agent` (edit)
- [ ] `syncErpSubEntities` mở rộng: vehicle_manufacts, customer_accounts, contacts (phones join + contact bank accounts), deputies, delivery_places (edit)
- [ ] Dropdown endpoint ERP mới: `GET /assign/customers/districts?province_id=`, `/hamlets?ward_id=`, `/vehicle-manufacts` (đọc mysql2)
- [ ] FormRequest: thêm/chỉnh rule `customer_accounts[]`, `vehicle_manufacts[]`, `phones[]` (array), `district_id/hamlet_id` nullable, `contacts.*.customer_contact_accounts[]`
- [ ] HRM write: thêm district_id/hamlet_id/website/note; map TK dòng đầu → cột account_*/bank_*; mobile=join phones. Bỏ qua vehicle/multi-bank/delivery phía HRM

## Phase 7 — FE: form đầy đủ đúng thứ tự ERP

### FE
- [ ] Sắp xếp lại CustomerForm.vue theo đúng thứ tự ERP (xem map): Section "Thông tin khách hàng" → checkbox is_supplier/is_manufacturer → fullname, Đối tượng, [Hãng xe nếu is_manufacturer], Nhóm KH
- [ ] Cá nhân: CCCD, Ngày cấp, Nơi cấp, Tên đơn vị → SĐT (phones[] dynamic), Email, Website, Sinh nhật → bảng Địa chỉ KH (Quốc gia/Tỉnh/Quận-Huyện/Phường-Xã/Đường-Thôn/Số nhà) → bảng Tài khoản cá nhân (dynamic, bank select)
- [ ] Tổ chức: Tên viết tắt, Công ty mẹ, MST, Email, SĐT bàn, Website, Địa chỉ xuất HĐ → bảng Người đại diện → bảng Địa chỉ công ty → bảng Tài khoản công ty (dynamic)
- [ ] Ghi chú (note) cuối section chung
- [ ] Section "Người liên hệ" (Tổ chức): contacts accordion (Họ tên, Chức vụ, Sinh nhật, Email, CCCD, SĐT phones[] dynamic) + bảng Tài khoản cá nhân của contact (dynamic)
- [ ] Section "Địa chỉ giao hàng" (chỉ khi sửa): bảng + thêm/sửa/xóa
- [ ] Dropdown: Ngân hàng/Chi nhánh từ `/human/banks` + `/branches`; Quận-Huyện/Đường-Thôn/Hãng xe từ endpoint ERP mới; cascade Quốc gia→Tỉnh→Quận→Phường→Thôn
- [ ] Validate inline V2 cho field required theo loại

### Checkpoint — 2026-06-09 (fix runtime + chuyển form sang V2Base)
- Fix BE: `CustomerService::index()` trả query builder (bỏ `->paginate` thừa) → hết lỗi `Collection::paginate`.
- Fix FE list: thêm mixin `CheckPermission` (thiếu → `hasAPermission` undefined làm vỡ render).
- Đổi form sang V2Base (yêu cầu user): `CustomerForm.vue` viết lại bằng V2BaseInput/Select/SelectInModal/DatePicker/IconButton + validate inline kiểu V2 (`text-small-error`, map `error_messages`). 6 section card. Giữ logic load dropdown/groups/parent/payload/submit.
- Cần test browser: (1) list render V2; (2) form add/edit V2; (3) **Nhóm KH dùng V2BaseSelectInModal trên TRANG** — verify dropdown mở đúng (nếu lỗi → đổi sang V2BaseSelect multiple); (4) cascade tỉnh→xã + pre-select khi edit; (5) AC3 ghi ERP (rủi ro cột NOT NULL / contacts.phones).

### Checkpoint — 2026-06-09 (Phase 6+7: bám sát ERP tối đa)
Code xong (subagent-driven), `php -l` BE sạch:
- Phase 6a: models ERP mới (TpCustomerBankAccount, TpCustomerContactBankAccount, TpDeliveryPlace, TpVehicleManufact, TpDistrict) + TpCustomer sync (BankAccounts/VehicleManufacts/DeliveryPlaces) + endpoint districts/hamlets/vehicle-manufacts.
- Phase 6b: applyErpFields mở rộng (district/hamlet/website/note/is_supplier/is_manufacturer, mobile=join phones) + syncErpSubEntities đầy đủ (vehicle, bank accounts, contacts+contact accounts ghi trực tiếp lấy id, deputies, delivery) + HRM write 1 phần (map TK đầu, district/hamlet/website/note) + FormRequest (phones[] cá nhân, customer_accounts/vehicle/contacts.*.accounts).
- Phase 7: CustomerForm.vue viết lại đầy đủ đúng thứ tự ERP (2021 dòng): checkbox NCC/hãng, hãng xe, phones[] động, địa chỉ phân cấp đầy đủ (district/hamlet cascade), bảng TK ngân hàng động (bank→branch), người đại diện, người liên hệ (phones[] + TK động), địa chỉ giao hàng (khi sửa). Dropdown: tỉnh/xã + banks HRM; district/hamlet/vehicle từ ERP.
Lưu ý: tất cả subagent từ giờ dùng Opus 4.8 (theo yêu cầu user).
Bước tiếp: TEST BROWSER (chưa chạy). Rủi ro: (1) cascade district↔ward — HRM wards key theo province hay district? kiểm `addresses?level=3&parent_id=` nhận district hay province; (2) bank→branch có data; (3) cột ERP NOT NULL khi insert; (4) phones/contacts KH Tổ chức; (5) edit pre-select cascade.

### Checkpoint — 2026-06-09 (Loại hình tổ chức + Lĩnh vực KH)
Áp thay đổi từ feature customer-org-type-and-scope sang form Assign:
- "Đối tượng" → "Loại hình tổ chức" 5 loại (1 Cá nhân, 2 DN tư nhân, 3 DN nước ngoài, 4 DN FDI, 5 Cơ quan nhà nước). Loại 2-5 dùng layout/logic tổ chức (FE `isOrganization`, BE `isOrganization()`).
- Bỏ trường "Nhóm khách hàng" (groups) khỏi form + payload.
- Thêm 2 trường bắt buộc: Nhóm lĩnh vực KH (`customer_scope_group_id`) + Lĩnh vực KH (`customer_scope_id`) — V2BaseSelect searchable, đồng bộ 2 chiều client-side (Top-Down lọc theo nhóm; Bottom-Up auto-fill nhóm: 1 nhóm→điền, nhiều nhóm→bắt chọn). Nguồn: `assign/customer-scope-groups` + `assign/customer-scopes/getAll` (mỗi scope có `customer_scope_group_ids`).
- BE: FormRequest customer_type in:1-5, scope_group_id/scope_id required + check scope thuộc nhóm (pivot customer_scope_group_members); Service ghi 2 cột vào HRM customers (cột đã có sẵn qua migration Human 2026_06_09), map ERP customer_type (1→1, 2-5→2); CustomerDetailResource trả scope_group_id/scope_id để prefill. List filter + render: 5 loại + nhãn "Loại hình tổ chức".
- Cần test browser: scope dropdown nạp đúng (field `customer_scope_group_ids`), đồng bộ 2 chiều, prefill edit, lưu ghi đúng 2 cột HRM. Cần chạy migration Human 2026_06_09 nếu chưa.
