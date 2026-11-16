# Hạ tầng quyền dùng chung cho các màn duyệt phiếu (HRM) — @cuong61n

Ngày 16/11/2026. Chỉ đọc code `hrm-api` (nhánh `gop_db`, repo con `HRM/hrm-api`), không chạy lệnh ghi, không truy vấn DB. Mục đích: thiết kế bảng gom `approval_inbox_items` trả lời đúng "người X có được duyệt phiếu Y ở cấp hiện tại không".

Quy ước ghi chú: đường dẫn tính từ `hrm-api/`. "Chưa xác minh" = chỉ suy từ code, chưa đối chiếu dữ liệu DB thật.

---

## 0. Kết luận nhanh (đọc trước)

1. Cách HRM nhận biết "quản lý" là **phân công nhiều–nhiều** ở bảng `employee_manage_departments`, KHÔNG phải một cột `manager_id` trên phòng. Cột `departments.department_lead_id` / `parts.part_lead_id` (trưởng phòng / trưởng bộ phận) là khái niệm KHÁC, gần như không dùng để chốt quyền duyệt.
2. Phân quyền hiện hành = **mã quyền + Vai trò thuộc công ty + `PermissionChecker`**. Quyền **Duyệt không có phạm vi** (chỉ quyền Xem có phạm vi 1–4). Phạm vi "phòng ban" của một bước duyệt nằm ở **code từng màn** (AND với quản lý phòng), không nằm trong bảng quyền.
3. **Không có Super Admin vượt quyền** trong code đang chạy. Phần "Super admin (role 18) vượt quyền ở ~20 luồng" của `inventory-hrm.md` đã **lỗi thời**.
4. Công ty đang làm = `employee_infos.company_role ?: company_id`, lưu DB, dùng chung mọi tab/thiết bị. Quyền, vai trò, phòng quản lý đều tính **theo công ty đó**.
5. Có hàm sẵn **"ai có mã P ở công ty C"** (`PermissionChecker::holders`) và **"mã nào tôi có ở công ty C"** (`PermissionChecker::grants` / `CurrentPermission::map`) — đủ để dựng gate (a) bằng SQL hoặc bằng danh sách mã nạp trước.
6. Có **3 biến thể "phòng tôi quản lý"** đang chạy song song, kết quả khác nhau (mục 1.6). Bảng registry phải khai rõ từng loại phiếu dùng biến thể nào.

---

## 1. "Quản lý" của phòng ban / bộ phận / công ty

### 1.1 Nguồn dữ liệu

| Khái niệm | Bảng · cột | Bằng chứng |
|---|---|---|
| Người **quản lý** phòng/bộ phận (có thể nhiều phòng, nhiều công ty) | `employee_manage_departments` (`employee_id`, `company_id`, `department_id`, `part_ids` chuỗi CSV, `all_department`) | `Modules/Timesheet/Entities/EmployeeManageDepartment.php:12-18`; ghi: `app/Services/Admin/EmployeeRoleService.php:710-745` |
| Cờ **quản lý tất cả phòng ban** của công ty chính | `company_employees.all_department` (chỉ có tác dụng với công ty chính của nhân viên) | `app/Helper/PermissionHelper.php:62-90` |
| Cờ quản lý tất cả phòng ban ở công ty **kiêm nhiệm** | dòng `employee_manage_departments` có `department_id = NULL`, `all_department = 1` | `EmployeeRoleService.php:716-724`, `PermissionHelper.php:69-73` |
| **Trưởng** phòng / bộ phận (đúng 1 người) | `departments.department_lead_id`, `parts.part_lead_id` — lưu `employees.id`, cast sang `employee_infos.id` ở Model | `app/Casts/EmployeeIdAsInfoIdCast.php:8-30`, `app/Models/Department.php:11-27`, `Modules/Timesheet/Entities/Department.php:15` |
| **Phó** phòng | `departments.department_assistants` (JSON) | `database/migrations/2025_04_08_150755_add_column_department_assistant_id_in_departments_table.php:17`; accessor `app/Models/Department.php:28-31` |
| Phòng cha | `departments.parent_id` | `app/Models/Department.php:19-22` |
| Phòng/bộ phận của chính nhân viên | `employee_infos.department_id`, `employee_infos.part_id`, `employee_infos.company_id` | `HrmScopeContext.php:99-100` |
| Phòng kiêm nhiệm | `employee_concurrently_departments` | `Modules/Human/Entities/EmployeeConcurrentlyDepartment.php` — chưa thấy bộ kiểm quyền/duyệt nào đọc (grep trong `PermissionHelper`, `PermissionChecker`, `HrmScopeContext` không có) |

Cột `all_department` của `company_employees` và `employee_manage_departments` **không có migration trong hrm-api** (bảng do ERP/dump gộp tạo; chỉ thấy dùng ở `database/e2e_provision.php:183`). Chưa xác minh kiểu cột trên prod.

### 1.2 Hàm chính

| Hàm | Dòng | Việc làm |
|---|---|---|
| `employeeManagesAllDepartmentsIn($employeeId, $companyId)` | `app/Helper/PermissionHelper.php:62` | true nếu dòng `employee_manage_departments(E, C).all_department=1`, hoặc (C = công ty chính của E **và** `company_employees(E, C).all_department=1`) |
| `manageDepartmentIdsOf($employeeId, $companyId)` | `PermissionHelper.php:98` | Quản lý tất cả ⇒ **mọi** phòng của công ty C; ngược lại ⇒ các `department_id` NOT NULL ở C |
| `managePartIdsOf($employeeId, $companyId)` | `PermissionHelper.php:121` | Quản lý tất cả ⇒ mọi bộ phận của C; ngược lại ⇒ gộp `part_ids` (CSV) các dòng ở C |
| `employeeIdsManagingDepartment($departmentId, $companyId)` | `PermissionHelper.php:150` | **Ngược lại**: ai quản lý phòng D (gồm người có cờ tổng) — dùng cho thông báo/duyệt |
| `listManageDepartmentIds()` / `listManagePartIds()` | `PermissionHelper.php:209`, `:238` | bọc hàm trên cho người đăng nhập + công ty đang làm |
| `listManageDepartmentIdsWithOwn()` | `PermissionHelper.php:220` | như trên **cộng phòng của chính mình** |
| `listManageCompanyIdsForCurrentEmployee()` | `PermissionHelper.php:188` → `Modules/Timesheet/Entities/Employee.php:81` | các công ty trong `company_employees` của người đăng nhập |
| accessor `manager_departments` | `app/Models/TpEmployee.php:116` | = `manageDepartmentIdsOf(auth id, current_company_role)` |

### 1.3 Có phân biệt trưởng phòng / phó phòng / quản lý bộ phận / giám đốc không?

- **Chốt quyền duyệt KHÔNG phân biệt chức vụ.** Mọi cấp "Trưởng phòng duyệt …" thực chất là: **có mã quyền duyệt của cấp đó** AND **phòng của phiếu ∈ phòng mình quản lý**. Ví dụ `Modules/Training/Entities/TrainingRequest.php:60-68` (`training.de_xuat_dao_tao_truong_phong.approve` + `in_array($this->department_id, auth()->user()->manager_departments)`), `Modules/Finance/Entities/PrepickExtend/PrepickExtendRequest.php:229-240`.
- "Giám đốc / Tổng giám đốc / Ban giám đốc" **không có khái niệm riêng** trong dữ liệu tổ chức; chỉ là **mã quyền** kiểu `... ban giám đốc duyệt ...` gán cho Vai trò (vd `training.de_xuat_dao_tao_quan_ly_dao_tao.approve` ở `TrainingRequest.php:78-90`). Không kiểm phòng.
- `department_lead_id` được dùng cho: gửi thông báo cho trưởng đơn vị (`Modules/Assign/Services/IssueService.php:692-740`, `Modules/Timesheet/Services/OvertimeRequirementService.php:188-205`), tra người hạch toán (`Modules/Assign/Services/Accounting/SupportAccountingTrait.php:232-290`, `Modules/Finance/Services/ProductImportAccountingService.php:466-490`), đồng bộ CRM (`Modules/CRM/Jobs/SyncLeadDepartmentToCrm.php:44-59`). **Không thấy gate duyệt nào dựa vào nó** (grep `department_lead_id`/`part_lead_id` toàn `app` + `Modules`).
- `department_assistants` (phó phòng): grep không thấy gate nào đọc.

### 1.4 Một người quản lý nhiều phòng?

Có. Mỗi phòng một dòng `employee_manage_departments`; `EmployeeRoleService::saveManageDepartments` chèn nhiều dòng (`:737-745`). Cũng quản lý được phòng ở **nhiều công ty** (mỗi công ty một nhóm dòng; dòng công ty khác giữ nguyên khi lưu — `:704-709`).

### 1.5 Quản lý cấp trên có tự quản lý phòng con không?

**Không.** `manageDepartmentIdsOf` chỉ trả đúng các `department_id` được phân công hoặc **toàn bộ phòng của công ty** khi có cờ tổng (`PermissionHelper.php:98-113`). Không đi qua `departments.parent_id`. Muốn quản nhiều phòng phải được phân công từng phòng hoặc bật "quản lý tất cả phòng ban".

### 1.6 Ba biến thể "phòng tôi quản lý" đang chạy song song (điểm dễ sai)

| Biến thể | Công ty dùng | Cờ `all_department` | Cộng phòng của chính mình | Dòng |
|---|---|---|---|---|
| **V1** `manageDepartmentIdsOf` / `manager_departments` | `current_company_role` (công ty đang làm) | **Có** | Không | `PermissionHelper.php:98`; `TrainingRequest.php:68` |
| **V2** `listManageDepartmentIdsWithOwn` | công ty đang làm | Có | **Có** | `PermissionHelper.php:220` (vd `Handover`, `Task`, theo `inventory-hrm.md` AS5/AS12, chưa kiểm lại từng dòng) |
| **V3** `ChecksEmployeePermission::manageableDepartmentIds` (và bản chép trong `PrepickExtendRequest`) | `auth()->user()->info->company_id` = công ty **gốc**, không phải công ty đang làm | **Không** (chỉ `pluck department_id`, kèm NULL) | **Có** | `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php:51-56, 100-114`; `PrepickExtendRequest.php:289-305` |

Hệ quả cho thiết kế: (i) với người có cờ "quản lý tất cả phòng ban", V3 không thấy gì còn V1 thấy mọi phòng; (ii) nhân viên **kiêm nhiệm** làm việc ở công ty phụ: V3 so `sameCompanyAsCurrent($this->company_id)` bằng công ty gốc (`ChecksEmployeePermission.php:117-121`) nên phiếu công ty phụ bị loại dù quyền (qua `PermissionChecker`) tính theo công ty đang làm — **lệch nội bộ ngay trong một hàm duyệt** (`PrepickExtendRequest.php:229-239`). Đây là suy luận từ code, chưa chạy thử.
→ `approval_inbox_items` cần cột/khai báo `manager_variant` (`manage` | `manage_with_own` | `home_company_manage`) trong Definition từng loại, đừng gộp một cách tính.

---

## 2. Hệ phân quyền hiện hành

### 2.1 Mã quyền vs tên cũ

- Danh mục: `app/Support/Permissions/Catalog/*.php` (18 file phân hệ, ~948 mã); đồng bộ vào bảng `permissions` bằng `permission:catalog-sync` (`app/Support/Permissions/CatalogSync.php:97-118`; cột `allowed_scopes` JSON từ `scopes`). Phân loại `kind`: `view` 441 · `action` 368 · `approve` 139 (đếm bằng grep `'kind' =>` trên Catalog).
- Mã dạng `phan_he.doi_tuong.hanh_dong`, regex `/^[a-z0-9_]+(\.[a-z0-9_]+){2,}$/D` (`PermissionCode.php:30`).
- **Tên cũ tiếng Việt** vẫn được gọi trong code cũ; tra sang mã qua bảng `permission_aliases` (`legacy_name`, `legacy_guard` = `api`|`web`, `permission_id`, `min_scope`) — `PermissionChecker.php:283-302`. Chuỗi "trông như mã" (có dấu chấm, chỉ `[A-Za-z0-9_.-]`) luôn đi nhánh mã; còn lại đi nhánh tên cũ (`CurrentPermission.php:44-70`, `PermissionCode.php:53-61`).
- Mã sai/ngừng dùng: `local`/`testing` ném `UnknownPermissionCode`; môi trường khác log kênh `permission` + trả `false` (`PermissionCode.php:127-141`).
- Tài liệu chính thức: `docs/huong-dan-phan-quyen.md`.

### 2.2 Vai trò và `role_has_permissions.company_id`

**Mâu thuẫn với tài liệu nền.** `inventory-hrm.md:16-26` mô tả kiểu cũ (spatie, lọc `role_has_permissions.company_id`, khe `model_type = App\Employee`, trait CEP query thẳng 3 bảng). Code hiện hành khác:

- Vai trò **thuộc một công ty**: `roles.company_id` (migration `2026_11_01_000003_add_company_id_and_base_name_to_roles_table.php`); tên = `{mã công ty}_{base_name}`.
- `PermissionChecker` (docblock `app/Support/Permissions/PermissionChecker.php:9-27`): "**KHÔNG đọc `role_has_permissions.company_id`**"; chỉ lấy Vai trò gán cho nhân viên (`employee_has_roles`, **bỏ qua `model_type`**) mà `roles.company_id = công ty` và `roles.status = 1`.
- `role_has_permissions` thêm cột `scope` (1 Bộ phận · 2 Phòng ban · 3 Công ty · 4 Tổng công ty; NULL = quyền không phạm vi) — `database/migrations/2026_11_01_000005_add_scope_to_role_has_permissions_table.php`. Migration ghi PK còn gồm `company_id` cho tới khi `rbac:convert` dựng lại bảng; chưa xác minh `rbac:convert` đã chạy trên DB prod.
- Quyền gán thẳng nhân viên (`employee_has_permissions`) **không còn tác dụng** (`Modules/Timesheet/Entities/Employee.php:107-111`; `ChecksEmployeePermission.php:5-9`).
- Trait CEP không còn query thẳng: `ChecksEmployeePermission.php:19-24` gọi `PermissionLookup::currentHas`.

### 2.3 Công thức "quyền của người X trong công ty C"

`PermissionChecker::loadGrants` (`app/Support/Permissions/PermissionChecker.php:246-281`):

```
works  = EXISTS company_employees(employee_id = X, company_id = C)      -- không có ⇒ trả rỗng
rows   = employee_has_roles ehr
         JOIN roles r ON r.id = ehr.role_id AND r.company_id = C AND r.status = 1
         JOIN role_has_permissions rhp ON rhp.role_id = r.id
         JOIN permissions p ON p.id = rhp.permission_id
         WHERE ehr.employee_id = X AND p.deprecated_at IS NULL AND p.code IS NOT NULL
         GROUP BY p.code  SELECT p.code, MAX(rhp.scope)
grants = [code => scope]  -- scope > 3 bị hạ về 3 nếu GroupScopeConfig::allows(C) = false
```

- **Mã + phạm vi**: `PermissionChecker::for($x, $c)->grants()` hoặc `CurrentPermission::map()` (người đăng nhập, `CurrentPermission.php:87-91`).
- **Tên (cũ) + mã + nhóm**: `CurrentPermission::listFor($employeeId, $companyId)` trả `Collection<Fluent{id,name,code,group}>` (`CurrentPermission.php:112-143`); `CurrentPermission::list()` cho người đăng nhập; `names()` chỉ tên cũ guard `api`.
- **Tên mới của mã** (hiển thị): cột `permissions.name`, nguồn Catalog `'name'` (`finance.php:13` mẫu). Sau `rbac:convert`, `permissions.name` đã đổi thành tên hiển thị mới (`PermissionLookup.php:8-12`).
- Có đệm tĩnh theo `employeeId|companyId` trong tiến trình (`PermissionChecker.php:53-62`); `flush()` sau khi đổi quyền.
- `PermissionChecker::allows($code, $minScope)` / `scope($code)` / `has($code)` (`:82-107`); `hasLegacy($tên, $guard)` (`:110-116`).
- **Ai có mã P ở công ty C** (đảo chiều): `PermissionChecker::holders($nameOrCode, $guard, $companyId, $minScope)` (`:150`, truy vấn thật `:167-215`), `PermissionLookup::holders($name, $companyId)` (`PermissionLookup.php:96`, nhận cả mã lẫn tên cũ, gộp guard `api`+`web`), `holdersAmong` (`:115`), `holdersAnyCompany` (`:129`, chỉ dùng khi vốn không gắn công ty).

### 2.4 Phạm vi (tổng công ty / công ty / phòng ban / bộ phận)

- Hằng số: `PermissionScope` `PART=1, DEPARTMENT=2, COMPANY=3, GROUP=4` (`app/Support/Permissions/PermissionScope.php:12-15`); số lớn bao số nhỏ, luôn so `>=` (`docs/huong-dan-phan-quyen.md:104`).
- **Chỉ quyền Xem có phạm vi.** `docs/huong-dan-phan-quyen.md:17,22`: "Thao tác và Duyệt không có phạm vi. Mỗi bước duyệt là một mã riêng". Catalog khớp: các mã `.view` khai `'scopes' => [1,2,3,4]` (vd `finance.php:159,180,251,396`), mã duyệt `'scopes' => []`.
  ⇒ **Với gate duyệt, "gate_scope = department" trong `database.md` mục 2 không phải phạm vi của quyền; nó là điều kiện AND ở code từng màn (phòng của phiếu ∈ quản lý phòng).** Cần ghi lại trong thiết kế để khỏi nhầm với `role_has_permissions.scope`.
- Công ty chưa được bật "Tổng công ty" (`companies.allow_group_scope = 0`) ⇒ phạm vi 4 bị hạ về 3 (`PermissionChecker.php:269-275`, `GroupScopeConfig.php:14-17,36-49`). Chỉ ảnh hưởng quyền Xem.
- Lọc danh sách theo phạm vi của mã **Xem**: `DataScope` + `HrmScopeContext` (mục 5).
- Cũ (còn nhiều chỗ gọi): `checkPermissionList(...)` truyền mảng 4–7 tên quyền theo thứ tự tổng công ty → công ty → phòng ban → bộ phận (`PermissionHelper.php:245-298`). Doc cấm truyền mã vào hàm này (`docs/huong-dan-phan-quyen.md:96`).

### 2.5 Các cửa kiểm quyền (đều quy về `PermissionChecker`)

| Cửa | Dòng |
|---|---|
| `isCurrentEmployeeHasPermission($p)` (helper toàn cục) | `app/Helper/PermissionHelper.php:20` → `CurrentPermission::has` |
| `BaseModel::isCurrentEmployeeHasPermission` | `app/Models/BaseModel.php:198-201` |
| `PermissionService::isCurrentEmployeeHasPermission` | `app/CommonServices/PermissionService.php:19-23` |
| Middleware `checkPermission:a|b` (có 1 mã là qua) | `app/Http/Middleware/CheckPermission.php:17-41`; alias `Kernel.php:71` |
| `PermissionLookup::currentHas / currentHasCode / currentHasAt / employeeHasAt` | `PermissionLookup.php:26,37,50,61` |
| trait `ChecksEmployeePermission::currentEmployeeHasPermission` | `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php:19` → `PermissionLookup::currentHas` |
| `Employee::getPermissionsViaRoles()` | `Modules/Timesheet/Entities/Employee.php:112-120` |

`currentHasAt` / `employeeHasAt` cho phép hỏi quyền của **người bất kỳ ở công ty bất kỳ** (không cần là người đăng nhập) — cần cho job `sync()` và bulk duyệt.

---

## 3. Công ty đang làm việc và kiêm nhiệm

- **Công ty đang làm** = `TpEmployee::getCurrentCompanyRoleAttribute` → `employee_infos.company_role ?: employee_infos.company_id` (`app/Models/TpEmployee.php:97-114`), đệm `RequestCache` theo request. Lưu **DB**, không nằm trong JWT (claims chỉ có `email`, `token_version`: `TpEmployee.php:62-66`).
- Đổi công ty: `POST human/employee-infos/{id}/update-company-role` ghi `company_role` (`Modules/Human/Services/EmployeeInfoService.php:1681-1686`; route `Modules/Human/Routes/api.php:149`; FE `components/BasicSubsystem.vue:659`). Không có kiểm tra ở service rằng công ty đó nằm trong `company_employees` của người này — chưa xác minh chặn ở nơi khác (FormRequest/route).
- Header `X-Company-Id`: FE gửi công ty lúc tải trang (`hrm-client/plugins/company-guard.js:8`, `utils/companyGuard.js:10`); middleware `EnsureSameCompany` trả 409 khi lệch (`app/Http/Middleware/EnsureSameCompany.php:23-56`, đăng ký `Kernel.php:50`). Header **không** quyết định công ty xử lý, chỉ để phát hiện tab cũ; công ty xử lý luôn là cột DB. Request không có header (app mobile) thì cho qua (`:25-28`).
- **Kiêm nhiệm** (làm việc ở nhiều công ty): `company_employees` có UNIQUE `(employee_id, company_id)` (`database/migrations/2026_11_01_000004_add_unique_to_company_employees_table.php`). Mỗi công ty có **Vai trò riêng** (`roles.company_id`, gán qua `employee_has_roles`) và **dòng quản lý phòng riêng** (`employee_manage_departments.company_id`). Quyền tại một thời điểm = quyền của **một công ty (đang làm)**; chuyển công ty thì quyền đổi theo. Không có hợp nhất quyền các công ty.
- Công ty "chính" (để áp cờ `company_employees.all_department`) = `employee_infos.company_id` (`PermissionHelper.php:75-85`).
- Kiêm nhiệm **phòng ban** (`employee_concurrently_departments`) không tham gia kiểm quyền (xem 1.1).
- Hàm hỏi quyền ở công ty chứng từ thay vì công ty đang làm: `PermissionLookup::currentHasAt($name, $companyId)`. Các endpoint duyệt hiện tại chủ yếu kiểm công ty đang làm (`TrainingRequest.php:104-112` so `current_company_role == company_id`) ⇒ registry nên lọc **đúng công ty đang làm** để khớp.

---

## 4. Super Admin / vai trò đặc biệt

- **Không có vượt quyền** ở cơ chế kiểm quyền: `PermissionChecker.php:9-27` không có nhánh Super Admin; `docs/huong-dan-phan-quyen.md:9` cấm; `ChecksEmployeePermission.php:5-9` "không còn nhánh Super admin"; Catalog ghi "Ruling R21 (25/10/2026)… thay nhánh Super admin đã bỏ" (`finance.php:1158`, `warehouse.php:190,218`); `CustomerService.php:2610` "Nhánh Super Admin bỏ 25/10/2026".
- Grep `isSuperAdmin|hasRole\(|Gate::before|id 18` trong `app`, `Modules`, `routes` ngoài test/convert: **không có nhánh bypass**. Còn vài **docblock/comment lỗi thời** nhắc Super admin (`ProductExportRequestController.php:1503`, `WaitingAssignTaskService.php:96,529`, `DeliveryContractService.php:139`) — chưa xác minh phần thân hàm của từng chỗ.
- Super Admin chỉ được "đủ mã" do `rbac:convert` cấp một lần; **mã mới thêm sau chưa ai có, kể cả Super Admin** (`docs/huong-dan-phan-quyen.md:61`). Ví dụ `approval_center.phieu_cho_duyet.view` phải cấp ở `/admin/roles`; design.md ghi "cấp rộng cho mọi vai trò" — việc cấp này là dữ liệu, không phải code.
- Ngoại lệ không thuộc quyền: `GroupScopeConfig::admins()` (danh sách `employees.id` trong `config('rbac.group_scope_admins')`) chỉ để bật/tắt phạm vi Tổng công ty; mã giả `admin.pham_vi_tong_cong_ty.configure` (`GroupScopeConfig.php:27,77-90`). Không liên quan duyệt phiếu.
- `inventory-hrm.md:361` ("Vượt quyền super admin (role 18) có ở nhiều luồng… F1…F22") và `:293` ("CEP… currentEmployeeIsSuperAdmin()=role 18") **mâu thuẫn code hiện tại**. Kết luận trong README.md mục 22/10 "Bỏ ngoại lệ Super Admin" là đúng.

---

## 5. Helper dùng chung để lọc theo phạm vi người xem

| Hàm | Dòng | Cách dùng |
|---|---|---|
| `HrmScopeContext::applyCurrent($query, $maXem, $cols, $aggregate=false)` | `app/Support/Permissions/HrmScopeContext.php:57` | Lọc danh sách theo phạm vi mã **Xem**. `$cols`: `company`, `department`, `part`, `owner` (mặc định `created_by`), `mode` bắt buộc `record_unit` hoặc `owner_members`. Ví dụ dùng thật: `Modules/Sale/Services/HandoverProductRecordService.php:270` |
| `DataScope::apply($query, $code, $cols, ScopeContext $ctx, $aggregate)` | `app/Support/Permissions/DataScope.php:49` | Bản không phụ thuộc người đăng nhập (dựng `new HrmScopeContext($employeeId, $companyId)`) |
| `DataScope::allowsRecord($code, $record, $cols, $ctx)` | `DataScope.php:75` | Kiểm 1 bản ghi (mảng cột→giá trị) có trong phạm vi không; cùng bộ luật với `apply` |
| `new HrmScopeContext($employeeId, $companyId)` | `HrmScopeContext.php:29` | `departmentIds()` = V1 (mục 1.6), `partIds()`, `departmentMemberIds()`, `partMemberIds()`, `companyMemberIds()` (đệm trong đối tượng) |
| `CurrentPermission::scope($code)` | `CurrentPermission.php:74` | Mức 1..4 của người đăng nhập; `null` = không có quyền hoặc quyền không phạm vi |
| `checkPermissionList / ...WithColumn / ...WithCompanyFilter / ...NotAllCompany` | `PermissionHelper.php:245, 301, 349, 425` | Cũ, theo mảng tên quyền. Chỉ để đọc hiểu màn cũ |
| `PermissionLookup::holders / holdersAmong / infoIdsOf` | `PermissionLookup.php:96, 115, 148` | Người nhận thông báo, danh sách người có quyền; `infoIdsOf` đổi `employees.id` → `employee_infos.id` |

Luật `DataScope` (`DataScope.php:97-158`): scope 4 ⇒ không lọc; 3 ⇒ `company = công ty`; 2 ⇒ `department ∈ departmentIds() OR part ∈ partIds() OR owner = tôi`; 1 ⇒ `part ∈ partIds() OR owner = tôi`; mã không phạm vi ⇒ chỉ bản ghi tôi tạo; không có mã ⇒ `1 = 0`. Chỉ dùng được cho mã có `permissions.allowed_scopes` khác rỗng — mã Duyệt gọi vào sẽ bị coi là dùng sai (`:113-115`, ném ở local/testing).

**Kết luận**: `DataScope` dành cho quyền **Xem**. Màn "Phiếu chờ duyệt" không dùng nó để quyết định duyệt, chỉ có thể dùng cho quyền xem màn nếu sau này đặt phạm vi.

---

## 6. Truy vấn "phiếu mà người X có quyền duyệt" — 3 kiểu gate

Giả định registry có `company_id`, `department_id`, `gate_type`, `required_permission` (đã quy ra **mã**), `state = 1`. Mọi so sánh dùng `employees.id` (ghi rõ nếu cột nguồn là `employee_infos.id`).

### 6.1 (a) Có mã quyền P trong công ty — dùng danh sách mã nạp trước, không join

```php
$checker = PermissionChecker::for($employeeId, $companyId);   // đệm theo nhân viên|công ty
$codes   = array_keys($checker->grants());                    // PermissionChecker.php:73 — [] nếu không thuộc công ty
$q->where('company_id', $companyId)
  ->where('gate_type', 'permission')
  ->whereIn('required_permission', $codes);                   // index (state, required_permission, company_id)
```

- 1 truy vấn nạp quyền (đệm) + 1 truy vấn danh sách. Nếu `$codes` rỗng thì trả `1 = 0`, đừng bỏ điều kiện (fail-closed).
- Nếu muốn thuần SQL (job, báo cáo): 
```sql
EXISTS (SELECT 1 FROM company_employees ce
        JOIN employee_has_roles ehr ON ehr.employee_id = ce.employee_id
        JOIN roles r ON r.id = ehr.role_id AND r.company_id = ce.company_id AND r.status = 1
        JOIN role_has_permissions rhp ON rhp.role_id = r.id
        JOIN permissions p ON p.id = rhp.permission_id AND p.deprecated_at IS NULL
        WHERE ce.employee_id = :me AND ce.company_id = i.company_id AND p.code = i.required_permission)
```
  (không lọc `ehr.model_type`, không đọc `rhp.company_id` — khớp `loadGrants`).
- **Điểm KHÔNG gọn**:
  1. **Tên quyền cũ**: phiếu có thể gate bằng tên tiếng Việt (`permission_kind = name`). Phải quy sang mã **lúc `sync()`** bằng `permission_aliases` (`legacy_name` + `legacy_guard` → `permission_id` → `permissions.code`) và lưu `required_permission` = mã. Alias có `min_scope` thì kiểm `scope >= min_scope` (`PermissionChecker.php:233-244`) — với mã Duyệt thường `null`; chưa đếm có alias Duyệt nào có `min_scope`.
  2. Một quyền mà code gốc nhận **tên ở cả 2 guard** (`api` và `web`): `PermissionLookup::checkerHas` thử cả hai (`PermissionLookup.php:81-85`); alias dùng chung bảng nên một tên cho một mã, nhưng 2 tên khác nhau có thể cùng trỏ một mã. `alt_permissions` (điều kiện HOẶC) → `whereIn` trên danh sách mã.
  3. Mã **hợp lệ** nhưng chưa ai có (mã mới) ⇒ danh sách rỗng ⇒ phiếu không ai thấy; cần cảnh báo ở lệnh đối soát.
  4. Mã ngừng dùng (`deprecated_at`): `grants()` đã loại; code gốc gọi mã đã ngừng sẽ `false` (+ log) — registry cũng phải coi là không ai duyệt.

### 6.2 (b) Là quản lý phòng của phiếu — nạp danh sách trước, so bằng `IN`

```php
$deptIds = manageDepartmentIdsOf($employeeId, $companyId);   // V1; đã gồm cờ "tất cả" → mọi phòng của công ty
$partIds = managePartIdsOf($employeeId, $companyId);
$q->where('gate_type', 'dept_manager')
  ->where(function ($w) use ($deptIds, $partIds) {
      $w->whereIn('department_id', $deptIds)             // $deptIds rỗng ⇒ bỏ nhánh, KHÔNG bỏ cả điều kiện
        ->orWhereIn('part_id', $partIds);
  });
```

- Gate loại `permission` **kèm** quản lý phòng (Đề xuất đào tạo, Hàng giữ…) = (a) **AND** (b). Registry cần cột kết hợp (vd `gate_type = permission_and_dept`), không phải 2 loại tách nhau; `database.md` mục 5 hiện chỉ có OR giữa các loại.
- Thuần SQL (nếu cần): 
```sql
EXISTS (SELECT 1 FROM employee_manage_departments m
        WHERE m.employee_id = :me AND m.company_id = i.company_id
          AND (m.department_id = i.department_id OR m.all_department = 1))
OR EXISTS (SELECT 1 FROM company_employees ce
        JOIN employees e ON e.id = ce.employee_id
        JOIN employee_infos ei ON ei.id = e.employee_info_id
        WHERE ce.employee_id = :me AND ce.company_id = i.company_id
          AND ce.all_department = 1 AND ei.company_id = i.company_id)
```
- **Điểm KHÔNG gọn bằng SQL**:
  1. **`part_ids` là chuỗi CSV có dấu cách** (`"1, 2"`, `EmployeeRoleService.php:742` dùng `implode(', ', ...)`). `FIND_IN_SET(part_id, part_ids)` **sai** nếu có khoảng trắng; phải `REPLACE(part_ids,' ','')` hoặc tách ở PHP (như `managePartIdsOf`, `PermissionHelper.php:121-141`). Không index được ⇒ nên nạp danh sách ở PHP.
  2. **Cờ "tất cả phòng ban"** có 2 nguồn khác nhau tùy công ty chính/kiêm nhiệm (mục 1.1); bản PHP đã xử lý, bản SQL phải sao chép đúng logic như trên.
  3. **3 biến thể V1/V2/V3** (mục 1.6): V2/V3 cộng thêm phòng của chính mình (`employee_infos.department_id`); V3 không tính cờ tổng và dùng công ty gốc. Dùng một hàm cho cả ba sẽ lệch với endpoint duyệt thật. Đề xuất: Definition khai `manager_variant`; `ApprovalInboxQuery` gọi 3 hàm tương ứng và hợp `IN`.
  4. **Phiếu mà `department_id` NULL**: V3 chặn tường minh (`$this->department_id !== null`, `PrepickExtendRequest.php:238`); `whereIn` với NULL tự không khớp nên an toàn, nhưng cần ghi ở Definition.
  5. Phòng của **phiếu** có nhiều cách xác định tùy loại (phòng người yêu cầu / phòng người xử lý / phòng nhận / `objectable` polymorphic của hạch toán). `sync()` phải quy về **một** `department_id` theo đúng gate của màn gốc (ví dụ Task: phòng của người xử lý, `inventory-hrm.md` AS12). Đây là việc của Definition, không thể suy ra bằng SQL.

### 6.3 (c) Người đích danh ghi trên phiếu

```sql
EXISTS (SELECT 1 FROM approval_inbox_assignees a WHERE a.item_id = i.id AND a.employee_id = :me)
```

- **Điểm cần chú ý**:
  1. **Hai hệ id người**: DB gộp lưu `employees.id` ở `department_lead_id`/`part_lead_id` (qua cast thành `employee_infos.id` khi đọc Model) nhưng nhiều cột `approver_id`, `created_by` có thể là `employees.id` hoặc `employee_infos.id` tùy bảng. Bảng `approval_inbox_assignees.employee_id` phải thống nhất `employees.id` (đổi bằng `EmployeeIdAsInfoIdCast::toEmployeeId/toInfoId`, hoặc `PermissionLookup::infoIdsOf` chiều ngược). Chưa xác minh từng cột `approver_id` của ~55 loại.
  2. Đích danh **không có phép thử quyền**: người đích danh có thể đã chuyển công ty/nghỉ việc ⇒ nên đối chiếu `company_employees` của người đó khi `sync()` (hoặc để lệnh `backfill` dọn dòng thừa).
  3. Đích danh có thể **thay đổi không qua `saved` của phiếu** (đổi thủ kho, phân công NV mua hàng). Cần hook ở nguồn dữ liệu phân công đó hoặc `backfill`, không chỉ trait trên phiếu.
  4. "Người đích danh" kiểu **vai trò động** (thủ kho của kho trên phiếu, NV mua hàng theo hãng) cần tính ra danh sách người lúc `sync()` ⇒ khi thủ kho đổi, registry **cũ** cho tới lần `sync`/`backfill` kế tiếp (chu kỳ 30 phút theo `database.md` mục 6).

### 6.4 Những điểm KHÔNG biểu diễn thuần SQL gọn + đề xuất

| Điểm | Vì sao | Đề xuất |
|---|---|---|
| Điều kiện nghiệp vụ ngoài gate (đã quá mốc, trùng lịch, người duyệt ≠ người tạo, vượt hạn mức) | Nằm trong `canApprove*()` từng Entity | `sync()` tính sẵn `approvable` + `blocked_reason` (đã có trong `database.md` mục 12); với điều kiện phụ thuộc **người xem** (≠ người tạo) thì lọc ở PHP trên trang kết quả |
| Alias tên cũ + `min_scope` + `alt_permissions` HOẶC | Cần bảng `permission_aliases` | Quy ra **danh sách mã** lúc `sync()`; lưu `required_permission` (mã) + `alt_permissions` (mã) |
| 3 biến thể "phòng tôi quản lý" | Mục 1.6 | Khai `manager_variant` trong Definition; dựng danh sách phòng theo biến thể rồi `IN` |
| Phạm vi phòng ở cấp **bộ phận** | `part_ids` là CSV | Nạp `managePartIdsOf` ở PHP, so `part_id IN` |
| Gate là **AND** (quyền + quản lý phòng) rồi **OR** với đích danh | `database.md` mục 5 chỉ có OR | Thêm cột cờ AND hoặc `gate_type` ghép; SQL: `(perm AND dept) OR assignee` |
| Công ty chứng từ ≠ công ty đang làm (kiêm nhiệm) | Endpoint gốc đa số kiểm công ty đang làm; V3 kiểm công ty gốc | Lọc registry theo công ty đang làm (khớp endpoint); ghi rõ lệch của V3 để sửa nguồn khi cần |
| Kiểm lại lúc duyệt (TOCTOU) | Quyền đổi giữa lúc xem và bấm | Bulk/Duyệt vẫn đi ĐÚNG hàm duyệt lẻ của màn gốc; registry chỉ để hiện danh sách (đã chốt ở `database.md` mục 9–10) |
| Đếm badge theo phân hệ | `GROUP BY source_subsystem` cùng điều kiện | Cùng một query-builder `visibleTo($employee, $company)` dùng cho danh sách và đếm (tránh lệch số) |

Thứ tự đề xuất cho `ApprovalInboxQuery::visibleTo(employeeId, companyId)`:
1. `$grants = PermissionChecker::for(e, c)->grants()` → `$codes`.
2. `$deptIds`/`$partIds` theo biến thể (gọi `manageDepartmentIdsOf` / `managePartIdsOf` + phòng của mình nếu V2/V3).
3. `WHERE state = 1 AND approvable = 1 AND company_id = c AND (assignee OR (permission AND ...) OR (permission_and_dept AND ...) OR dept_manager)`.
4. Mọi nhánh rỗng ⇒ `0 = 1`, **không** bỏ điều kiện (fail-closed, như `DataScope.php:55-57`).

---

## 7. Mâu thuẫn với tài liệu nền (cần sửa trong `inventory-hrm.md` / `design.md` / `database.md`)

| # | Tài liệu nền nói | Code đang chạy | Chỗ sửa |
|---|---|---|---|
| 1 | `inventory-hrm.md:16-26,292-300`: kiểm quyền spatie, lọc `role_has_permissions.company_id`, khe `model_type`, CEP query thẳng 3 bảng | Mọi cửa quy về `PermissionChecker`; **không** đọc `rhp.company_id`; vai trò thuộc công ty (`roles.company_id`); bỏ qua `model_type`; gán thẳng nhân viên không còn tác dụng (`PermissionChecker.php:9-27`, `ChecksEmployeePermission.php:5-24`) | Cập nhật mục "Các kiểu chốt quyền"; cột "Thấy role App\Employee" không còn là rủi ro |
| 2 | `inventory-hrm.md:16,293,361,412`: Super admin (role 18) vượt quyền ở ~20 luồng | Không còn nhánh bypass; Super Admin chỉ "đủ mã" khi `rbac:convert` (`docs/huong-dan-phan-quyen.md:9,61`) | Xoá/đóng câu hỏi mở số 1 của mục 412 |
| 3 | `design.md` mục 5/99: tập quyền tính "vai trò của U (`employee_has_roles`, mọi `model_type`) ⋈ `role_has_permissions` với `company_id` = công ty đang làm" | Join qua `roles.company_id` + `roles.status = 1` + `company_employees`; **không** `rhp.company_id` | Đổi câu; dùng `PermissionChecker::grants()` |
| 4 | `database.md` mục 2: `gate_scope` = `company/department/part` "phạm vi áp quyền" | Quyền Duyệt không có phạm vi; "department" là điều kiện quản lý phòng AND mã | Đổi tên cột/ghi chú thành `gate_unit`; thêm `manager_variant` |
| 5 | `database.md` mục 5: các gate nối bằng OR | Nhiều màn là **AND** (mã + quản lý phòng) | Thêm gate ghép |
| 6 | Mục 5 truy vấn "`company_id = công ty đang làm`" gọi `manageDepartmentIdsOf(tôi, công ty)` như một | Có 3 biến thể (mục 1.6) | Khai `manager_variant` ở Definition |
| 7 | `inventory-hrm.md:363`: "TP duyệt … không kiểm phòng: F5, F20" | Trait V3 `manageableDepartmentIds` có sẵn để áp, nhưng chưa xác minh F5/F20 hiện đã áp chưa (chưa mở Entity) | Chưa xác minh |
| 8 | `inventory-hrm.md:16` "`H/HLP` có lọc `role_has_permissions.company_id = current_company_role`" | Lọc đã chuyển sang `roles.company_id` | Theo #1 |

## 8. Chưa xác minh / cần làm tiếp

- Trạng thái `rbac:convert` + `catalog-sync` trên DB prod/dev (code giả định đã chạy; nếu chưa, `role_has_permissions.scope` NULL hết).
- `approver_id` của từng loại phiếu là `employees.id` hay `employee_infos.id` (cần duyệt từng bảng nguồn khi viết Definition).
- Kiểu cột `all_department` ở `company_employees` / `employee_manage_departments` (không có migration ở hrm-api).
- Có alias Duyệt nào có `min_scope` khác NULL không (cần SELECT `permission_aliases` join `permissions.kind = 'approve'`).
- Danh sách chính xác loại phiếu dùng V1/V2/V3 (mới đối chiếu 3 ví dụ: Đề xuất đào tạo = V1, Gia hạn hàng giữ = V3, Task/Handover = V2 theo `inventory-hrm.md`).
- Quyền `approval_center.phieu_cho_duyet.view`: Catalog **chưa có** file `approval_center.php` (thư mục `Catalog/` chỉ có 18 file, không có phân hệ này) — phải tạo khi làm.
