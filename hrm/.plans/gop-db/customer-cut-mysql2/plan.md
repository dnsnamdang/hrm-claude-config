# Plan — Khách hàng: cắt `mysql2`, dùng bảng `customers` trên DB gộp

Nhánh: `gop_db` (worktree `gop_db-api` :8003 / `gop_db-client` :3002)
Mục tiêu: mọi logic khách hàng đọc/ghi thẳng `local_hrm_erp` qua connection **default**, không còn qua `mysql2` (DB ERP cũ).
Màn chuẩn: `/assign/customers` (KHÔNG phải `/human/customers`).

Quy tắc chuyển:
- `DB::connection('mysql2')` → `DB::connection()` (default)
- `env('DB_DATABASE_SECOND')` → `env('DB_DATABASE')`
- Model `Tp*`: bỏ `protected $connection = 'mysql2'` + bỏ prefix tên DB trong `__construct`
- Comment ghi "đọc từ ERP (mysql2), không dùng bảng customers HRM" → sửa lại cho đúng hiện trạng

---

## Phase 1 — Model Tp* khách hàng (13 file)

- [x] BE `app/Models/TpCustomer.php` — bỏ `$connection`, bỏ prefix DB, 9 chỗ `DB::connection('mysql2')`
- [x] BE `TpCustomerContact`, `TpCustomerGroup`, `TpCustomerDeputy` — bỏ `$connection` + prefix
- [x] BE `TpCustomerBankAccount`, `TpCustomerContactBankAccount` — bỏ `$connection` + prefix
- [x] BE `TpCustomerGallery`, `TpCustomerVideo` — bỏ `$connection` + prefix
- [x] BE `TpDeliveryPlace`, `TpVehicleManufact` — bỏ `$connection` + prefix
- [x] BE `TpEquipmentOld`, `TpExternalEquipment`, `TpSerial` — bỏ `$connection` + prefix

## Phase 2 — Service / Helper thuần khách hàng (9 file)

- [x] BE `Modules/Assign/Services/CustomerService.php` (66 chỗ)
- [x] BE `Modules/Assign/Services/CustomerManagerService.php` (21 chỗ, có `erpDb()`)
- [x] BE `Modules/Assign/Http/Requests/Customer/SaveCustomerRequest.php` (4 chỗ)
- [x] BE `Modules/Assign/Http/Requests/Customer/UpdateCustomerRequest.php` (4 chỗ)
- [x] BE `app/Helper/CustomerOwnership.php` (2 chỗ, có `erpDb()`)
- [x] BE `app/Helpers/ErpPermissionHelper.php` (10 chỗ — tầng quyền của chính màn này)
- [x] BE `Modules/Assign/Helpers/CustomerCodeHelper.php` (5 chỗ — sinh mã KH, tra provinces/wards)
- [x] BE `Modules/Timesheet/Services/CustomerService.php` (5 chỗ)
- [x] BE `Modules/Human/Services/CustomerService.php` (3 chỗ)

## Phase 3 — Chỗ lẻ trong file trộn (chỉ sửa phần khách hàng)

- [x] BE `Modules/Assign/Services/QuotationErpSyncService.php` — `findErpCustomer()` (customers) + `getFirstDeliveryPlace()` (delivery_places). GIỮ nguyên phần `tmp_products` / `costs`
- [x] BE `Modules/Assign/Http/Controllers/Api/V1/ReportController.php:1177` — `$erpConnection` dùng chung cho query có `customers`

## Phase 4 — Comment sai lệch (không đổi logic)

- [x] BE sửa comment "đọc từ ERP (mysql2), không dùng bảng customers HRM" ở 8 file: 2 MeetingResource, DetailProspectiveProjectResource, DetailBomListResource, MeetingController, ProspectiveProjectController, MeetingService, BomList, ProspectiveProject, BomListService

## Phase 5 — FE

- [x] FE `components/subsystem-menu/master-data.js` — Danh mục đối tác (KH - NCC) → Khách hàng: `/human/customers` → `/assign/customers`

## Phase 6 — Verify

- [x] `php -l` toàn bộ file đã sửa
- [x] Không còn `mysql2` trong luồng khách hàng (grep)
- [ ] Chạy thật: đăng nhập, mở `/assign/customers`, kiểm tra danh sách / chi tiết / bộ lọc / phân quyền
- [ ] Đối chiếu số dòng danh sách với `SELECT COUNT(*) FROM local_hrm_erp.customers`

---

## Ngoài phạm vi (đã báo user)

- `Modules/Human/Entities/TpSupplier.php` — Nhà cung cấp, cùng menu "Danh mục đối tác (KH - NCC)" nhưng không phải khách hàng
- ~90 model `Tp*` khác + `mysql2` của luồng hàng hóa / báo giá / giao việc (BomListService, QuotationService, AuthController…)

---

### Checkpoint — 2026-08-01
Vừa hoàn thành: Phase 1-5 + verify mức truy vấn. 35 file BE + 1 file FE. Không còn `mysql2` trong luồng khách hàng.
Verify đã chạy: `php -l` 35/35 sạch; TpCustomer → `local_hrm_erp.customers` 43.520 dòng; `ErpPermissionHelper` trả đúng erpEmployeeId=13 + 4 quyền KH true; `CustomerService::index()` 17.542 dòng có join tỉnh/phường; `show()` 74 field + 2 delivery_places; `CustomerManagerService` 4 danh mục OK; `CustomerOwnership` 32 id; `CustomerCodeHelper` sinh mã không trùng.
Đang làm dở: (không)
Bước tiếp theo: user chạy browser `/assign/customers` để nghiệm thu (chưa chạy — theo quy ước chỉ verify browser khi được yêu cầu).
Blocked:

---

## Phase 7 — Xoá 6 bảng `hrm_*` khách hàng cũ (2026-08-01)

- [x] Backup `backup/hrm_customer_tables_2026-08-01.sql` (223K, đủ 6 bảng)
- [x] Đối chiếu cấu trúc 6 cặp bảng `hrm_*` ↔ bản ERP → GIỐNG HỆT 6/6
- [x] Trỏ 37 chỗ code sang bảng ERP: `Modules/Timesheet/Services/CustomerService.php` (16), `Modules/Human/Services/CustomerService.php` (14), `Modules/Human/Entities/Customer.php` (7)
- [x] Kiểm tra không còn tham chiếu (toàn repo API + Client) + không có khoá ngoại
- [x] `DROP TABLE` 6 bảng → còn 18 bảng `hrm_*` (từ 24)
- [x] Smoke test 10 phép sau khi xoá: đều OK

Bảng đã xoá và lý do an toàn:

| Bảng | Dòng | Mồ côi (KH không tồn tại) | Trùng bản ERP | Duy nhất |
| --- | ---: | ---: | ---: | ---: |
| hrm_customer_business_fields | 1245 | 995 | 249 | 1 |
| hrm_customer_activity_types | 856 | 673 | 182 | 1 |
| hrm_delivery_places | 770 | 280 | ~490 | 0 |
| hrm_customer_has_vehicle_manufacts | 144 | 82 | 62 | 0 |
| hrm_customer_has_bank_accounts | 52 | 26 | 26 | 0 |
| hrm_customer_contact_has_bank_accounts | 0 | 0 | 0 | 0 |

Nguyên nhân mồ côi: `customer_id` trong các bảng này thuộc **dải id HRM CŨ** (tới 553064) trong khi `customers` sau gộp chỉ có id ≤ 232387 → không khớp bản ghi nào. Các dòng còn lại trùng khít nội dung với pivot ERP (đã spot-check KH 46/59/60: cặp scope_group/scope y hệt).

### Checkpoint — 2026-08-01 (Phase 7)
Vừa hoàn thành: xoá 6 bảng `hrm_*` khách hàng + trỏ 37 chỗ code sang bảng ERP dùng chung.
Đang làm dở: (không)
Bước tiếp theo: user nghiệm thu browser `/assign/customers` và `/human/customers`.
Blocked:

---

## Phase 8 — Gỡ toàn bộ tầng đồng bộ 2 chiều (2026-08-01)

**Lý do: sau khi gộp DB, sync trở thành lỗi hỏng dữ liệu.** `syncSimpleData` đọc `customers` rồi ghi
ngược vào chính `customers` (khớp theo `code` → cùng một dòng), và trong đó có
`DELETE customer_contacts WHERE customer_id=... ` + `insertGetId()` → **người liên hệ bị cấp id MỚI mỗi lần lưu KH**.
`customer_contacts.id` đang được 38.000+ bản ghi trỏ tới (firm_quotations 33.069, customer_registers 1.541,
assembly_requests 1.315, firm_contracts 1.113, prospective_projects 124, meetings 20) → mỗi lần sửa 1 KH là
làm mồ côi toàn bộ tham chiếu người liên hệ của KH đó. `Human\CustomerService::sync_data()` là bản hàng loạt
của cùng lỗi (chạy cho toàn bộ 43k KH).

- [x] BE `Modules/Assign/Services/CustomerService.php` — bỏ 2 lời gọi `syncToHrm($code)` + xoá hàm
- [x] BE xoá 6 hàm: `Timesheet\CustomerService::{sync_data,syncSimpleData}`, `Timesheet\CustomerController::{sync_data,syncSimpleData}`, `Human\CustomerService::sync_data`, `Human\CustomerController::sync_data`, `Assign\CustomerController::syncFromErp`
- [x] BE gỡ 3 route: `POST timesheet/customers/sync_data`, `POST timesheet/customers/sync-simple-data`, `POST assign/customers/sync-from-erp`
- [x] FE gỡ nút "Đồng bộ dữ liệu" (`pages/timesheet/setting/customers/index.vue`) + nút "Đồng bộ từ ERP" đã comment (`pages/assign/customers/index.vue`) + 2 hàm JS
- [x] Verify: `php -l` sạch; không còn route nào khớp `customer.*sync`; index 17.542 / show 74 field / contacts KH46 = 48 / accessor Human OK

## Phase 9 — Bỏ màn `/human/customers`, chuyển 8 picker sang luồng mới (XONG 2026-08-01)

⚠️ **Phát hiện chặn:** `GET human/customers` KHÔNG chỉ phục vụ màn đó — nó là **API chọn khách hàng của 8 màn Assign đang sống**:
`pages/assign/quotations/index.vue` (2 chỗ), `pages/assign/bom-list/index.vue`, `pages/assign/meeting/index.vue`,
`pages/assign/settlement_contract/index.vue`, `pages/assign/my-job/components/{MeetingsTab,MeetingUpcomingModal}.vue`,
`pages/assign/report/solutions-work-summary-by-department/index.vue`, `components/modals/AddRelatedUnitModal.vue`.

Khác biệt 2 API (không thay thẳng được):

| | `human/customers` | `assign/customers` |
| --- | --- | --- |
| Số dòng | toàn bộ 43.520 | 17.542 (lọc theo quyền ERP) |
| SĐT | trả thẳng | che `-` nếu KH không phải của mình |
| Field địa chỉ | `place`, `province`, `ward`, `nation` | `address` ghép sẵn, `province_name` |
| Field thêm | `place_lat/lng`, `company`, `stt` | `tax_code`, `register_locked`, `status`, `is_can_edit` |

- [x] User chốt: chuyển 8 picker sang `assign/customers`
- [x] Xoá màn: `pages/human/customers/**`, link menu `components/human-components/human-slidebar.vue:306`, `components/human-components/customer/CustomerForm.vue`, action `store/actions.js:1038,1043`
- [x] Xoá BE: `POST/DELETE human/customers` + `Human\CustomerService` (giữ `Human\Entities\Customer` — 18 file dùng)
- [ ] CÒN LẠI: màn `pages/timesheet/setting/customers/index.vue` vẫn là luồng cũ (chỉ còn xem, route `GET timesheet/customers` + `Timesheet\CustomerService::index`) — chưa xử lý

### Checkpoint — 2026-08-01 (Phase 8)
Vừa hoàn thành: gỡ sạch tầng sync 2 chiều → hết lỗi mồ côi `customer_contacts`.
Đang làm dở: (không)
Bước tiếp theo: user quyết hướng Phase 9 (picker) rồi mới xoá màn `/human/customers`.
Blocked: Phase 9 chờ quyết định về 8 picker.

### Bổ sung BE cho luồng mới
- [x] Thêm `GET /assign/customers/search` (select2) — `Assign\CustomerService::searchForSelect2()` + `CustomerController::search()`, đặt TRƯỚC `/{id}`. Dùng lại đúng bộ lọc quyền của `index()`, mặc định `all_business=1`, limit 20, shape `{id, text, code, fullname, short_name}`.

### 8 picker đã chuyển
| File | Đổi gì |
| --- | --- |
| `pages/assign/meeting/index.vue` | url + `limit`→`per_page` + `all_business=1` |
| `pages/assign/my-job/components/MeetingsTab.vue` | như trên |
| `pages/assign/my-job/components/MeetingUpcomingModal.vue` | như trên |
| `pages/assign/bom-list/index.vue` | url + `all_business=1` |
| `pages/assign/report/solutions-work-summary-by-department/index.vue` | url + `all_business=1` |
| `pages/assign/quotations/index.vue` | `search?q=` + `/{id}` sang assign |
| `pages/assign/settlement_contract/index.vue` | url select2 ajax |
| `components/modals/AddRelatedUnitModal.vue` | url + `limit`→`per_page` + `total`→`meta.total` + tự đánh `stt` + cột `province`→`province_name`, bỏ 2 cột Quận/Huyện + Phường/Xã (đã nằm trong `address`) |

### ⚠️ Thay đổi hành vi nhìn thấy được
- Picker KH tổ chức: **12.289 → 11.330** dòng. Chênh lệch đúng bằng 960 bản ghi `customer_type=2` nhưng `is_customer<>1` (nhà cung cấp / nhà sản xuất) — bản Assign loại đúng khỏi picker khách hàng.
- SĐT của KH không phải "của mình" hiển thị `-` (quy tắc ownership của luồng Assign).
- KH cá nhân "tự do" chỉ hiện khi search khớp đúng full SĐT (quy tắc B2C sẵn có của luồng Assign).

### Checkpoint — 2026-08-01 (Phase 9)
Vừa hoàn thành: 1 luồng khách hàng duy nhất. Xoá màn `/human/customers` (4 page + CustomerForm + menu + 2 action store; BE: route group + Controller + Service + 2 Transformer). Giữ `Human\Entities\Customer` (18 file dùng).
Verify: `php -l` sạch; 0 route `human/customers`; 0 tham chiếu FE còn sót; assign index 17.542 / search 20 / popup type=2 11.330 / show 74 field / accessor Human OK.
Bước tiếp theo: user nghiệm thu browser 8 màn picker + `/assign/customers`.
Blocked:

---

## Phase 10 — Còn đúng 1 luồng khách hàng + migration (2026-08-01)

### 10a. Xoá màn khách hàng cũ cuối cùng
- [x] FE xoá `pages/timesheet/setting/customers/**` + mục menu trong `components/SettingSlidebar.vue`
- [x] BE gỡ route group `/timesheet/customers` + xoá `Timesheet\CustomerController`, `Timesheet\CustomerService`, `Timesheet\Transformers\CustomerResource\CustomerListResource`

### 10b. Chuyển 2 modal chọn KH dùng chung (phát hiện thêm)
`components/modals/AddCustomer.vue` **được 33 file dùng** (giao việc, đào tạo, chấm công, meeting, dự án TKT…)
và `components/modal/AddCustomerModal.vue` (4 file) đều chạy trên `GET timesheet/customers` — luồng cũ.
- [x] Làm `assign/customers` thành SUPERSET thay vì cắt cột từng nơi: `index()` thêm leftJoin `nations` + `districts`; `CustomerListResource` thêm `nation`, `province`, `district`, `ward`, `place`
- [x] Chuyển 2 modal sang `assign/customers` (`limit`→`per_page`, `total`→`meta.total`, `all_business=1`)
- [x] Hoàn lại 2 cột Quận/Huyện + Phường/Xã cho `AddRelatedUnitModal` (không cần cắt nữa)

### 10c. Sửa bug đọc nhầm bảng — Quyết toán hợp đồng
`SettlementContract` trỏ `hrm_settlement_contracts` (4 dòng, HRM) nhưng model con `SettlementContractEmployee`
KHÔNG khai `$table` → Laravel suy ra `settlement_contract_employees` = **bảng ERP 81.759 dòng**.
Màn Quyết toán hiển thị **12 dòng nhân viên của hợp đồng ERP khác**.
- [x] Khai tường minh `protected $table = 'hrm_settlement_contract_employees'` + comment cảnh báo
- [x] Verify: QTHD-00001 giờ trả đúng 1 NV (Đồng Hữu Long), trước đó 12 dòng sai

⚠️ Bài học: bảng `hrm_*` có `code=0` KHÔNG có nghĩa là bỏ được — có thể là bảng ĐÚNG mà code chưa trỏ tới.
Phải kiểm tra model con của mọi bảng `hrm_*` trước khi xoá.

### 10d. Migration
- [x] `database/migrations/2026_08_01_000001_drop_hrm_customer_tables.php`
  - `up()`: `dropIfExists` 6 bảng (idempotent — chạy được cả DB đã xoá tay lẫn chưa)
  - `down()`: dựng lại CẤU TRÚC (dữ liệu phục hồi từ `backup/hrm_customer_tables_2026-08-01.sql`)
  - KHÔNG bọc `DB::transaction` (DDL MySQL implicit-commit)
- [x] Test thật: `migrate --path=` chạy OK → `down()` dựng lại 6 bảng, đối chiếu cấu trúc **KHỚP 6/6** → `up()` xoá lại
- [x] Trạng thái cuối: 0 bảng `hrm_customer*`, tổng `hrm_*` = 18, migration đã ghi vào bảng `migrations`

### 18 bảng `hrm_*` còn lại — KHÔNG được xoá
Đã rà tham chiếu code từng bảng: tất cả đều còn dùng.
`hrm_employees` (114 file), `hrm_role_has_permissions` (12), `hrm_employee_has_roles` (11), `hrm_scopes` (11),
`hrm_nations` (10), `hrm_permissions` (8), `hrm_company_employees` (7), `hrm_roles` (7),
`hrm_employee_manage_departments` (6), `hrm_company_roles` (5), `hrm_notifications` (4), `hrm_print_templates` (4),
`hrm_files` (3), `hrm_groups` (3), `hrm_module_mappings` (1 — CRM ModuleMapping),
`hrm_settlement_contracts` (1), `hrm_employee_has_permissions` (config/permission.php),
`hrm_settlement_contract_employees` (0 trước khi sửa → nay 1, xem 10c).

### Checkpoint — 2026-08-01 (Phase 10)
Vừa hoàn thành: chỉ còn 1 luồng khách hàng (`/assign/customers`); migration xoá 6 bảng đã test round-trip.
Verify: `php -l` sạch; 0 route khách hàng luồng cũ; 0 tham chiếu FE còn sót; assign index 17.542 / search 20 /
popup 11.330 / lọc mobile 1 / show 74 field; accessor Human OK; quyết toán HD 1 NV (đúng).
Bước tiếp theo: user nghiệm thu browser — ưu tiên modal AddCustomer (33 màn dùng) + `/assign/customers` + Quyết toán HĐ.
Blocked:

---

## Phase 11 — Test toàn diện HTTP + browser (2026-08-01)

Môi trường: worktree API `:8003` + client `:3002`, đăng nhập thật (namdangit@gmail.com).

### Kết quả cuối
- **43/43 endpoint HTTP** xanh (27 endpoint luồng KH + 7 màn liên quan + 4 endpoint luồng cũ phải 404)
- **9 màn browser** kiểm chứng thật, 0 request thất bại
- Màn chi tiết KH: 22 request API, 0 lỗi

### 6 LỖI THẬT tìm được và đã sửa

| # | Lỗi | Nguyên nhân | Sửa |
| --- | --- | --- | --- |
| 1 | `GET customer-groups` → **400** | `customer_groups` giữ bản ERP, KHÔNG có cột `code`; service vẫn `select('id','name','code')` | Bỏ `code` khỏi select |
| 2 | `GET {id}/contacts` → **400** | Lặp qua 4 bảng báo giá lấy `customer_contact_id`, nhưng `quotations` nay là bản HRM (bản ERP đã drop) — bản HRM dùng `customer_contact_name/phone` | Bỏ `quotations` khỏi vòng lặp, gom SĐT ở khối (b) |
| 3 | `training/master-select?table=customers` → **500 fatal** (mất cả header CORS) | `DB::table('customers')->get()` không LIMIT: 43.520 dòng = 137 MB > memory_limit 128M. Trước gộp HRM chỉ ~469 KH | Bỏ `getAllCustomers()` khỏi `JobRequestForm` — nó nạp cho một Select2 **đã bị comment** |
| 4 | Popup chọn KH trả **0 dòng** | FE gửi `keyword=null` (chuỗi); luồng Assign không chặn, luồng Human cũ có chặn `!= 'null'` | Chặn `'null'/'undefined'` cho keyword/tax_code/mobile ở `index()` + sửa FE gửi `''` |
| 5 | Bộ lọc KH màn **Báo giá + Quyết toán HĐ** trả 0 | Tôi dùng nhầm `apiGetList` cho endpoint `search`: helper này `collect()` mảng tuần tự → trải thành `{"0":…,"1":…}` thay vì `data:[…]` | Đổi sang `responseJson` như các endpoint khác |
| 6 | `per_page=10000` → **500 fatal** (bom-list, report) | `CustomerListResource` tính ownership theo TỪNG dòng → chết ở 5.000 dòng. Đo: 100→1.1s, 2000→5.3s, 5000→500 | Chuyển 5 màn sang `assign/customers/search?limit=` (không qua Resource): 17.542 mục / 0.9s |

⚠️ Lỗi #3 và #6 cùng một gốc: **truy vấn không LIMIT trên bảng `customers`** — trước gộp DB bảng HRM chỉ vài trăm dòng nên vô hại, sau gộp là 43.520 dòng. Cần rà các chỗ khác còn `->get()` trần trên bảng đã gộp.

### Hiệu năng sau khi chuyển sang endpoint `search`
| Màn | Trước | Sau |
| --- | --- | --- |
| Meeting (KH tổ chức) | 6.5s / chỉ 1.000 KH | 3.3s / đủ 11.330 KH |
| BOM list | **chết (500)** | 17.542 KH |
| Báo cáo solutions-work-summary | **chết (500)** | 2.0s / 17.542 KH |

### Màn đã kiểm chứng trên browser
`/assign/customers` (10 dòng, đủ cột) · `/assign/customers/46` (22 request, 0 lỗi) · Dự án TKT (popup chọn KH + tìm "TOYOTA" 10/10 khớp + chọn KH + dropdown Người liên hệ) · `/assign/job_requests/add` (AddCustomerModal 17.542) · `/timesheet/jobassignment/add` (AddCustomer — modal của 33 màn — 17.542, đủ cột) · `/assign/quotations` (filter 20 kết quả) · `/assign/settlement_contract` (select2 20 kết quả) · `/assign/bom-list` (17.542) · `/assign/meeting` (11.330) · `/assign/my-job` · báo cáo solutions-work-summary · `AddRelatedUnitModal` (totalRows 17.542, stt đúng, đủ province/district/ward)

### Lỗi console CÓ SẴN (không do thay đổi này — đã đối chiếu git diff)
- `[Vue warn] computed "fields"/"permissions" already defined in data` — mẫu cũ ở `AddCustomer`, `AddCustomerModal`, `AddEmployee`, `ChooseErpCustomerModal`, `ConfirmJobAssignmentNote`, `settlement_contract/index.vue`
- `currentPage is not defined` + `CompanyDepartmentFilter: prop "permissions" Expected Object, got Array` — `settlement_contract/index.vue`
- `TypeError: Cannot read properties of undefined (reading '_normalized')` — 7 mục menu trong `subsystem-menu/master-data.js` không có `link` (các mục "còn bên ERP")
- `/assign/customers` gọi API danh sách **2 lần** mỗi lần vào màn (mẫu double-emit của `V2BaseDataTable`, đã ghi trong STATUS.md)

### Việc dọn dẹp
- 7 file client bị Python ghi làm đổi CRLF→LF (diff phình vô nghĩa) → đã khôi phục CRLF. Diff cuối cùng: 16 file sửa (tổng +42/-87 dòng) + 6 file xoá.

### Checkpoint — 2026-08-01 (Phase 11)
Vừa hoàn thành: test HTTP 43/43 + browser 12 màn; tìm và sửa 6 lỗi thật.
Đang làm dở: (không)
Bước tiếp theo: user tự nghiệm thu; server test vẫn chạy (API :8003, client :3002).
Blocked:

---

## Phase 12 — Rà nốt + test luồng GHI (2026-08-01)

### Lỗi #7 — validate quốc gia chặn không cho lưu KH
`SaveCustomerRequest` + `UpdateCustomerRequest` yêu cầu `nation_id => exists:hrm_nations,id`
(bảng HRM, **3 dòng**), nhưng dropdown FE lấy từ `assign/customers/nations` → bảng ERP `nations` (**32 dòng**),
và dữ liệu đang lưu cũng là id ERP. Hậu quả: chọn bất kỳ quốc gia nào ngoài id 1-3 là **trượt validate,
không lưu được**; **14 KH hiện có** đã mang `nation_id > 3` nên không sửa được. Tệ hơn, id 1-3 ở hai bảng
là hai nước khác nhau (ERP id 2 = Việt Nam, hrm_nations id 2 = Japan) → qua được validate nhưng sai nghĩa.
- [x] Sửa 3 rule `exists:hrm_nations,id` → `exists:nations,id` (Save 1 + Update 2)
- [x] Verify: nation_id 1/3/8/32 đều hợp lệ (trước fix 8 và 32 trượt)
- [x] GIỮ NGUYÊN `hrm_nations` cho màn Danh mục quốc gia `/human/nations` (`Human\Entities\Nation`, `NationService`) — màn đó vẫn sống, HTTP 200

### Dọn code mồ côi
- [x] Xoá `Modules/Human/Http/Requests/{Save,Create,Update}CustomerRequest.php` — 0 chỗ dùng sau khi bỏ màn Human

### Quét truy vấn không LIMIT (cùng gốc lỗi #3/#6)
- [x] Quét toàn bộ `->get()/->pluck()/->all()` trên 10 bảng lớn đã gộp: 17 điểm nghi ngờ, rà tay từng cái
  → còn lại đều an toàn (command CLI limit 512M, hoặc đã `where('customer_id', …)` giới hạn theo 1 KH)

### Test luồng GHI (chạy trong transaction, rollback — không đụng dữ liệu thật)
- [x] **Tạo KH**: id 232388, sinh mã tự động, ghi kèm 1 contact + 1 deputy; 43.520 → 43.521 → rollback về 43.520
- [x] **Sửa KH 46**: ✅ **48 id người liên hệ GIỮ NGUYÊN** sau khi lưu — đây là test hồi quy quan trọng nhất
  của việc gỡ sync ở Phase 8 (trước đó mỗi lần lưu là xoá + cấp id mới cho cả 48, làm mồ côi 38.000+ tham chiếu)
- [x] **Thêm nhanh người liên hệ**: 48 → 49, `created_by` ghi đúng ERP employee id = 13 (lỗi map id đã hết)

### Ngưỡng tải endpoint (đo lại sau khi thêm join nations/districts)
`per_page`: 100→0.9s · 200→1.0s · 500→1.8s · 1000→3.4s · 1500→4.4s · 2000→5.5s (ổn định 200).
Thực tế mọi màn đều ≤100 (dropdown số dòng/trang). Cú 500 gặp 1 lần là do chạy liền sau 2 request
`search?limit=20000` (3.5 MB) làm `php -S` đơn luồng dồn bộ nhớ — không tái hiện khi chạy riêng.

### CHỨC NĂNG BỊ MẤT khi bỏ màn `/human/customers`
**Xuất Excel danh sách khách hàng** — màn cũ có `GET human/customers/export`; màn `/assign/customers`
không có nút Xuất Excel và BE cũng không có route tương ứng. Các export con vẫn còn
(`{id}/documents/export`, `{id}/equipment/export`).
→ **User đã quyết (2026-08-01): KHÔNG port sang luồng mới.** Chấp nhận bỏ chức năng này.

### Kết quả cuối
- **52/52 endpoint HTTP** xanh (48 phải 200 + 4 phải 404)
- `/assign/customers` trên browser: 15 request API, **0 thất bại**, 0 lỗi console

### Checkpoint — 2026-08-01 (Phase 12)
Vừa hoàn thành: rà truy vấn không LIMIT, test luồng ghi (tạo/sửa/thêm liên hệ) có rollback, sửa lỗi #7.
Tổng cộng **7 lỗi thật** tìm và sửa qua 2 phase test.
Đang làm dở: (không)
Bước tiếp theo: (không còn) — user chốt không port Xuất Excel. Feature hoàn tất, chờ nghiệm thu cuối.
Blocked:

---

## Phase 13 — Chứng minh luồng KH độc lập `DB_CONNECTION_SECOND` (2026-08-01)

User chốt: **mục tiêu là bỏ hẳn `DB_CONNECTION_SECOND`** → đã ghi vào `.plans/gop-db/design.md` mục 0.

### Phép thử quyết định
Đổi `DB_DATABASE_SECOND` trong `.env` thành DB **không tồn tại** → `config:clear` → restart API → chạy luồng KH.
Lần 1: **8/32 endpoint CHẾT** (`SQLSTATE[HY000] [1049] Unknown database`) — gồm cả danh sách + chi tiết KH,
dù `CustomerService` đã sạch `mysql2` từ Phase 2.

### Nguyên nhân — dạng phụ thuộc THỨ HAI, rất dễ bỏ sót
Không phải `DB::connection('mysql2')`, mà là **model tự gắn tiền tố tên bảng**:
```php
public function __construct(array $attributes = []) {
    $this->table = env('DB_DATABASE_SECOND') . '.' . $this->table;   // ← query sang DB cũ
}
```
cộng với `protected $connection = 'mysql2'` còn sót ở model danh mục (`TpDistrict`, `TpHamlet`,
`Human\Entities\TpEmployee`…). Chính `app/Models/TpEmployee` — **model auth** — cũng dính.

### Đã sửa
- [x] Bỏ tiền tố `env('DB_DATABASE_SECOND') . '.'` khỏi **79 model** (75 bỏ trọn constructor, 4 chỉ bỏ 1 dòng)
- [x] Bỏ `protected $connection = 'mysql2'` khỏi **77 model**
- [x] Verify trước khi sửa: **66/66 bảng** các model đó trỏ tới đều đã có trên DB gộp
- [x] 2 chỗ cuối trong luồng KH: `MeetingController::getListCustomer`, `ProspectiveProjectService` (pivot loại hình/lĩnh vực)

### Kết quả — chạy lại phép thử với `DB_DATABASE_SECOND` = DB không tồn tại
- **32/32 endpoint luồng KH: OK**
- Browser: `/assign/customers` 15 request 0 lỗi · **Quản lý khách hàng 5/5 tab, 33 request, 0 lỗi** ·
  popup `AddCustomer` tìm "TOYOTA" → 114 bản ghi, 10/10 khớp
- Đã khôi phục `.env` về `dev_erp` sau khi test

### Không vỡ luồng khác
19 endpoint các module khác (báo giá, BOM, meeting, dự án, quyết toán, giao việc, job request, giải pháp,
danh mục Human, quyết định, đào tạo, auth) + 5 endpoint chi tiết (`quotations/80`, `bom-lists/22`,
`prospective-projects/146`, `meeting/35`, `settlement-contract/1`) đều 200.

### Trạng thái `mysql2` sau đợt này
| | Trước | Sau |
| --- | ---: | ---: |
| Model khai `$connection = 'mysql2'` | 77 | **0** |
| Model gắn tiền tố `DB_DATABASE_SECOND` | 79 | **0** |
| File còn `DB::connection('mysql2')` raw | 19 | **18** |

**Luồng khách hàng: sạch 100%.** 18 file còn lại thuộc luồng **báo giá / BOM / hàng hoá / thưởng** —
chưa đụng vì user yêu cầu ưu tiên khách hàng trước.
⚠️ Lưu ý trạng thái hỗn hợp hiện tại: model đã đọc DB gộp, còn 18 file đó vẫn đọc DB ERP cũ. Ids trùng nhau
(bảng ERP trong DB gộp giữ nguyên id) nên chưa gây sai, nhưng cần dứt điểm trước khi xoá connection.

### Checkpoint — 2026-08-01 (Phase 13)
Vừa hoàn thành: chứng minh bằng thực nghiệm luồng KH chạy được khi KHÔNG có `DB_CONNECTION_SECOND`.
Bước tiếp theo: chuyển nốt 18 file raw `DB::connection('mysql2')` (báo giá/BOM/hàng hoá) để bỏ hẳn connection.
Blocked:
