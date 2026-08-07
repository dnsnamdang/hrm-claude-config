# Plan — Chuyển code màn sang phân hệ mới (Danh mục chung & Bảo hiểm)

> Phụ trách: @junfoke · Tạo 2026-08-04 · Nhánh: `gop_db`
> Design: `.plans/gop-db/chuyen-code-phan-he/design.md`
> Spec: `docs/superpowers/specs/gop-db/2026-08-04-chuyen-code-phan-he-master-data-insurance-design.md`

## Ràng buộc toàn feature

- Nhánh `gop_db` (cả 2 repo). Code mới **không** dùng `mysql2` / `DB_CONNECTION_SECOND`.
- Không commit / push (rule project). Chỉ sửa file.
- Permission: sửa trực tiếp `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`,
  **không** tạo migration riêng cho permission — trừ trường hợp feature này: DB local đã có dữ liệu
  nên **cần thêm 1 migration `UPDATE`** để đổi `type`/`group` bản ghi sẵn có, đồng thời sửa seeder
  cho khớp. (Đây là ngoại lệ có chủ đích, ghi rõ lý do trong file migration.)
- Mỗi màn đi qua đủ 7 bước của quy trình chuẩn (design.md mục "Quy trình chuẩn 7 bước").
- Sau mỗi phase BE: chạy `php artisan route:list --path=<prefix>` để xác nhận route mới nạp được,
  và `composer dump-autoload`.

---

## Phase 0 — Chuẩn bị

- [x] Xác nhận nhánh: cả `hrm-api` và `hrm-client` đều đang ở `gop_db`
- [x] Đọc `.plans/gop-db/design.md` (7 gotcha khi làm trên nhánh gộp DB)
- [x] Tạo file `hrm-client/config/route-redirects.js` — nơi duy nhất khai bảng ánh xạ route cũ → mới
      (rỗng ở phase này, các phase sau append). Export `export const ROUTE_REDIRECTS = []`
- [x] Nối vào `hrm-client/nuxt.config.js::router.extendRoutes` — giữ nguyên `routes.push({path:'/'…})`
      hiện có, thêm vòng lặp `ROUTE_REDIRECTS.forEach(r => routes.push({ path: r.from, redirect: r.to }))`
- [x] Query DB lấy **đủ** id quyền bảo hiểm → **20 quyền**, nhiều hơn 16 quyền suy từ menu:
      thêm 956-959 (`Bảo hiểm nhân viên`) và **961-964** (`Báo cáo quyết định` — group này còn
      969-970 thang bảng lương ở lại Decision nên 961-964 phải đổi group thành `Báo cáo bảo hiểm`).
      Chi tiết ở Phase 9.

```sql
SELECT id, name, `group`, type FROM hrm_permissions
WHERE `group` IN ('Bảo hiểm nhân viên', 'Quản lý loại bảo hiểm',
                  'Quản lý gói bảo hiểm', 'Bảo hiểm ngoài công ty')
ORDER BY id;
```

- [x] Rà phạm vi dùng của `Tp{Nation,Province,Ward,Area,Bank,BankBranch}`: **chỉ dùng bên trong
      chính các entity/service đang chuyển** (`Nation`, `Area`, `Province`, `Ward`, `BankService`).
      Phát hiện: commit `931a192d6` đã gỡ `mysql2` + tiền tố DB khỏi 6 model này → `Ward`/`TpWard`
      cùng trỏ bảng `wards`, `BankBranch`/`TpBankBranch` cùng trỏ `bank_branches`, mà
      `master_settings.use_erp = '1'` nên hook đồng bộ vẫn chạy → ghi log lỗi trùng khóa mỗi lần tạo,
      riêng `BankService::addBankBranches` không có try/catch nên nhiều khả năng văng 500.
      **User chốt: gỡ hẳn lớp `Tp*`** → đưa vào Phase 1.

---

## Phase 1 (A1) — BE: 7 danh mục địa lý - ngân hàng → `Modules/MasterData`

Nguồn: `Modules/Human`. Đích: `Modules/MasterData` (hiện chỉ có skeleton, `Routes/api.php` 17 dòng).

- [x] Tạo cây thư mục `Modules/MasterData/{Entities,Http/Controllers/Api/V1,Http/Requests,Services}`
      nếu skeleton chưa có (bám cấu trúc `Modules/Finance` — module mới nhất làm đúng chuẩn)
- [x] Chuyển 8 Entity: `Nation, Area, Province, District, Ward, Hamlet, Bank, BankBranch`
      → `Modules\MasterData\Entities\*`
- [x] Chuyển 7 Controller: `{Nation,Area,Province,District,Ward,Hamlet,Bank}Controller`
      → `Modules\MasterData\Http\Controllers\Api\V1\*`
- [x] Chuyển 8 Request: `Create{Nation,Areas,Province,District,Ward,Hamlet,Bank,BankBranches}Request`
      → `Modules\MasterData\Http\Requests\*`
- [x] Chuyển `Services/BankService.php` → `Modules\MasterData\Services\BankService`
- [x] **Gỡ lớp đồng bộ `Tp*`** (user chốt 2026-08-04 — địa chỉ đã dùng chung 1 bảng trên DB gộp,
      không còn gì để đồng bộ; xem spec mục 4.1):
  - [x] Xóa 6 model `Modules/Human/Entities/Tp{Nation,Province,Ward,Area,Bank,BankBranch}.php`
  - [x] Gỡ hook `boot()` đồng bộ (`self::created` + `self::updated` trong nhánh `use_erp`) ở
        `Nation.php`, `Area.php` (dòng ~39-59), `Province.php` (~40-62), `Ward.php` (~29-71)
  - [x] Gỡ 4 nhánh `if ($useErp && $useErp->content)` trong `BankService.php`
        (`addBankBranches` ~111-133, `createBank` ~137+) — nhánh `TpBankBranch::forceCreate`
        không có try/catch, đang là bug 500 khi thêm chi nhánh ngân hàng
  - [x] Bỏ `use` + import `MasterSetting` nếu file không còn dùng
  - [x] `grep -rn "TpNation\|TpProvince\|TpWard\|TpArea\|TpBank\|TpBankBranch" hrm-api` → rỗng
- [x] Khai route trong `Modules/MasterData/Routes/api.php`: nhóm ngoài `['prefix' => '/v1', 'middleware' => 'auth:api']`,
      7 nhóm con `master-data/{nations,areas,provinces,wards,districts,hamlets,banks}` — **copy nguyên
      danh sách endpoint** từ `Human/Routes/api.php` dòng ~375-452 (banks có 10 endpoint gồm
      `/bank-branches/*`, nations/areas/provinces/wards có 8, districts/hamlets có 6)
- [x] Xóa 7 khối `Route::group` cũ khỏi `Modules/Human/Routes/api.php` + xóa `use` của 7 controller
- [x] `grep -rn "Modules\\\\Human\\\\Entities\\\\\(Nation\|Area\|Province\|District\|Ward\|Hamlet\|Bank\)"
      hrm-api/Modules hrm-api/app` → sửa hết sang namespace mới (chú ý `Employee`, `EmployeeInfo`,
      `Customer` đều có quan hệ tới `Bank`/`Province`/`Ward`)
- [x] `composer dump-autoload` → **54 route** `/api/v1/master-data/*` (banks 10, nations/areas/
      provinces/wards 8, districts/hamlets 6), **0 route** `human/{nations,…}` còn lại
- [x] `php -l` 48 file MasterData: không lỗi cú pháp; 21 class then chốt đều `class_exists`;
      đọc DB qua model mới OK (nations 32, wards 13.465, banks 19)

**Lệch so với plan (có chủ đích):**

- Controller đặt ở `Http/Controllers/V1` (không phải `Api/V1`) — theo đúng skeleton module mới và
  `Modules/Finance`. Vẫn `extends ApiController` của Human (`use Modules\Human\Http\Controllers\
  Api\V1\ApiController`) để không đổi hành vi; hợp nhất `ApiController` là việc riêng.
- Chuyển thêm **7 Service** (`{Nation,Area,Province,District,Ward,Hamlet,Bank}Service`) và
  **7 thư mục Transformer** (15 file) — plan ban đầu chỉ ghi `BankService`. 5 service `extends
  HumanService` nên phải thêm `use Modules\Human\Services\HumanService`.
- `Modules\Human\Transformers\ApiResource` và `Modules\Human\Helper\Helper` **giữ nguyên** không
  chuyển: đây là lớp dùng chung, `Modules/Finance` cũng import từ Human.

⚠️ `php artisan route:list` đang **crash sẵn** (không do feature này): `PermissionHelper.php:22`
gọi `auth()->user()->employee_info_id` khi chạy CLI (không có user) qua constructor của
`Modules/Timesheet/.../RequestUpdateTimeSheetController`. Đã đếm route bằng `app('router')
->getRoutes()` trong tinker thay thế.

---

## Phase 2 (A1) — FE: 7 màn địa lý - ngân hàng

- [x] `git mv hrm-client/pages/human/{nations,areas,provinces,districts,wards,hamlets,banks}`
      → `hrm-client/pages/master-data/` (17 file)
- [x] Đổi `layout: 'subsystem'` — kiểm lại từng file `index.vue`, hiện đã là `'subsystem'` nên
      **chỉ cần xác nhận, không sửa**
- [x] Sửa endpoint trong 17 file: `human/{nations,…}` → `master-data/{nations,…}`
- [x] Sửa comment `$router.push('/human/banks/…')` bị comment sẵn ở
      `areas/index.vue:267`, `nations/index.vue:261`, `provinces/index.vue:283`
- [x] Sửa nơi gọi API ngoài màn:
  - [x] `hrm-client/store/optionsSelect.js`
  - [x] `components/human-components/employee_info/EmployeeInfoForm.vue`
  - [x] `components/human-components/employee_info/EmployeeInfoShow.vue`
  - [x] `components/human-components/employee_info/request-update/EmployeeInfoForm.vue`
  - [x] `components/human-components/employee_info/request-update/EditEmployeeInfoForm.vue`
  - [x] `components/human-components/employee_info/my-info-request/EmployeeInfoForm.vue`
- [x] Cập nhật comment nhắc `/human/banks` ở `components/subsystem-menu/finance.js:40`
- [x] Thêm 7 cặp redirect vào `config/route-redirects.js`:
      `/human/nations → /master-data/nations` … `/human/banks → /master-data/banks`
- [x] Sửa 7 `link` trong `components/subsystem-menu/master-data.js`
- [x] `grep -rn "human/\(nations\|areas\|provinces\|wards\|banks\|districts\|hamlets\)" hrm-client
      --include=*.vue --include=*.js` (bỏ `node_modules`) → chỉ còn `route-redirects.js`

**Sự cố tự gây trong phase này — đã xử lý xong:**

Script đổi namespace đầu tiên viết bằng `xargs sed -i` quét **toàn bộ** file PHP của `Modules/` +
`app/`. Chạy quá chậm nên bị kill giữa chừng, nhưng phần đã chạy ghi lại file với **LF** (repo dùng
CRLF) → đổi kích thước file → `git status` gắn cờ `M` cho **3325 file không liên quan**, user nhìn
vào Source Control thấy 3380 thay đổi.
Chẩn đoán: `git diff --name-only` (so nội dung, có normalize EOL) chỉ ra 55 file, lệch hẳn với
`git status --short`. Đã trả lại 3325 file bằng `git checkout --` phần chênh lệch.
`git update-index --refresh` KHÔNG cứu được vì kích thước file đã đổi.
→ Bài học đã ghi memory: [[feedback_no_bulk_sed_on_windows]] — đổi chuỗi hàng loạt phải dùng script
Node đọc mỗi file 1 lần và **chỉ ghi khi nội dung thực sự khác**.

**Nợ kỹ thuật phát hiện khi test — user chốt GIỮ NGUYÊN, không sửa trong đợt này:**

5 route trỏ tới method không tồn tại, **có sẵn từ commit `2822cb2ae add danh mục địa chỉ`**
(copy nguyên sang module mới):

- `PUT /master-data/{nations,areas,provinces,wards}/{id}` → gọi `update()`, 4 controller đều
  không có method này
- `GET /master-data/wards/list` → gọi `getListWards()`, method thật trong `WardController` tên là
  `getListProvince` (lỗi copy-paste từ ProvinceController)

4 màn này sửa bản ghi qua đường khác (`POST /` dùng chung cho thêm và sửa) nên FE không lộ lỗi.

---

## Phase 3 (A1) — Verify

- [x] HTTP thật: **23/24 case PASS**. Không token → 401. 7/7 route cũ `/v1/human/{danh mục}` → 404.
      7/7 danh sách mới → 200. 6 endpoint `/list` → 5 PASS (`wards/list` FAIL 500 — **lỗi có sẵn**,
      xem mục nợ kỹ thuật cuối Phase 2). Chi tiết + `banks/{id}/branches` → 200.
- [x] Luồng ghi trên `nations` (có rollback): CREATE 200 → LOCK 200 → UNLOCK 200 → SHOW 200 →
      DELETE 200. Ghi nhận: **"xóa" ở đây là khóa mềm** (`NationService::deleteNation` chỉ set
      `status = 0`), không xóa bản ghi — hành vi có sẵn.
- [x] Redirect 7/7 chạy: `/human/{nations,areas,provinces,wards,districts,hamlets,banks}` đều tự
      nhảy sang `/master-data/*`, giữ đúng title màn.
- [x] Browser 7 màn: sidebar hiện **"DANH MỤC CHUNG"**, số liệu khớp DB —
      quốc gia 29, tỉnh/TP 45, phường/xã 3.336, quận/huyện 732, đường/phố 11.644, ngân hàng 10 dòng/trang.
      **Khu vực = 0 là đúng: bảng `areas` rỗng thật (0 dòng trong DB)**, không phải lỗi.
- [x] Form Thông tin nhân viên (`/human/employee_info/add`): dropdown **Ngân hàng** gọi
      `/api/v1/master-data/banks?limit=10000` → 200. Dropdown địa chỉ (Tỉnh/Phường) **không dùng**
      các endpoint vừa chuyển mà dùng `/api/v1/addresses` riêng → không bị ảnh hưởng.
- [x] DB trả nguyên trạng: `nations` 32 dòng (29 hoạt động / 3 khóa) — đúng như trước khi test.
      Bản ghi test đã xóa cứng (vì delete chỉ khóa mềm).
- [x] Ghi checkpoint vào plan này

### Test browser thật (Playwright) — phát hiện + sửa 1 lỗi nghiêm trọng

- [x] **Thêm chi nhánh ngân hàng** (BAOVIETBANK, 0 chi nhánh): dropdown Tỉnh/TP nạp đủ **45 tỉnh**
      (đúng `master-data/provinces/list`), lưu → dòng hiện ra kèm Tỉnh/TP, cột Chi nhánh 0 → 1
- [x] **Sửa chi nhánh**: modal nạp sẵn tên cũ, đổi tên → lưu → danh sách cập nhật đúng
- [x] **Xóa chi nhánh**: có hộp xác nhận, xóa xong về 0
- [x] **Tạo Quận/Huyện**: dropdown 45 tỉnh, lưu → DB ghi đúng `province_id=2`, `created_by=13`
- [x] **Sửa Quận/Huyện** (`PUT /master-data/districts/{id}`): 200, đổi được cả tên lẫn `province_id`
- [x] **Xóa Quận/Huyện**: 200 — cũng là **khóa mềm** (`status = 0`), không xóa bản ghi
- [x] DB trả nguyên trạng: `bank_branches` 126 dòng, `districts` 736 dòng, không còn bản ghi test/rỗng

🐛 **LỖI NGHIÊM TRỌNG TỰ GÂY — ĐÃ SỬA**: sau khi gỡ lớp `Tp*`, thêm chi nhánh ngân hàng trả 200
nhưng **ghi ra bản ghi RỖNG** (`name=''`, `bank_id=0`, `province_id=null`).

Nguyên nhân gốc **có sẵn từ commit `e63c49e18 add ngan hang`**: `BankBranch::__construct()` bị comment
`parent::__construct($attributes)` → `fill()` không bao giờ chạy → `BankBranch::create()` luôn tạo bản
ghi rỗng. Trước đây triệu chứng bị che vì **dữ liệu thật do `TpBankBranch::forceCreate()` ghi sang DB
ERP** (model đó có constructor bình thường). Gộp DB xong, 2 model cùng trỏ `bank_branches`; gỡ lớp Tp
đi thì đường ghi dữ liệu duy nhất biến mất → lỗi lộ ra.

→ Sửa: khôi phục `parent::__construct($attributes)` trong `Modules/MasterData/Entities/BankBranch.php`.
Đã test lại end-to-end trên browser: thêm/sửa/xóa chi nhánh đều đúng.
**7 entity còn lại đã kiểm: constructor bình thường, không dính lỗi này.**

⚠️ **Cảnh báo Vue có sẵn (không do feature này)**: cả 7 màn đều log
`[Vue warn] The computed property "fields" is already defined in data` khi render `b-table`.
File không có block `computed` nào → đến từ mixin/base dùng chung. Không ảnh hưởng chức năng.

### Checkpoint — 2026-08-04

Vừa hoàn thành: **Phase 0 → 3 (toàn bộ bước A1)**. 7 danh mục địa lý - ngân hàng đã chạy hoàn toàn
ở phân hệ Danh mục chung: BE `Modules/MasterData` (54 route), FE `pages/master-data`, redirect URL cũ,
gỡ xong lớp đồng bộ `Tp*`.

Đang làm dở: (không)

Bước tiếp theo: **Phase 4 — BE 3 màn đối tác** (`customers`, `customer-scopes`,
`customer-scope-groups`) từ `Modules/Assign` sang `Modules/MasterData`.
⚠️ Trước khi làm: `Modules/Assign/Services/CustomerService` + `CustomerManagerService` đang gọi
`app/Helpers/ErpPermissionHelper.php` — helper này **vẫn đọc qua `mysql2`** (nợ đã ghi ở
`.plans/gop-db/design.md` mục 0b). Chuyển service sang module mới thì phụ thuộc này đi theo,
cần quyết định xử lý thế nào.

Blocked: (không)

---

## Phase 4 (A2) — BE: 3 màn đối tác → `Modules/MasterData`

Nguồn: `Modules/Assign`.

- [x] Chuyển Controller: `CustomerController`, `CustomerManagerController`, `CustomerScopeController`,
      `CustomerScopeGroupController`
- [x] Chuyển Service: `CustomerService`, `CustomerManagerService`, `CustomerScopeService`,
      `CustomerScopeGroupService`
- [x] Chuyển Request: `Customer/{SaveCustomerRequest,UpdateCustomerRequest}`,
      `CustomerScope/CustomerScopeRequest`, `CustomerScopeGroup/CustomerScopeGroupRequest`
- [x] Chuyển Entity: `CustomerScope/CustomerScope`, `CustomerScopeGroup/CustomerScopeGroup`
- [x] Chuyển Transformer: `CustomerResource/{CustomerDetailResource,CustomerListResource}`
- [x] Chuyển Export: `CustomerDocumentsExport`, `CustomerEquipmentExport`
- [x] Chuyển Helper: `CustomerCodeHelper`
- [x] **Để lại `Modules/Assign`**: `CustomerDevelopmentReportController` +
      `Services/Report/CustomerDevelopmentReportService` (thuộc phân hệ Bán hàng) — sửa `use` của
      2 file này sang namespace MasterData nếu chúng dùng model/service vừa chuyển
- [x] Khai route `master-data/customers`, `master-data/customer-scopes`,
      `master-data/customer-scope-groups` trong `Modules/MasterData/Routes/api.php` — copy nguyên
      danh sách endpoint từ `Assign/Routes/api.php`, **nhớ `assign/customers/search`** (thêm ở
      feature `customer-cut-mysql2`) và `customers/my-permissions`
- [x] Xóa khối route cũ khỏi `Modules/Assign/Routes/api.php`
- [x] `grep -rn "Modules\\\\Assign\\\\\(Entities\\\\CustomerScope\|Services\\\\Customer\|Http\\\\Requests\\\\Customer\|Transformers\\\\CustomerResource\|Helpers\\\\CustomerCodeHelper\)"
      hrm-api` → sửa hết
- [x] `composer dump-autoload` + `php artisan route:list --path=master-data/customer`

---

## Phase 5 (A2) — FE: 3 màn đối tác

- [x] `git mv hrm-client/pages/assign/{customers,customer-scopes,customer-scope-groups}`
      → `hrm-client/pages/master-data/` (9 file)
- [x] Đổi `layout: 'default-sidebar'` → `layout: 'subsystem'` ở 3 `index.vue` + các file con
      (đồng bộ với 7 màn phase 2)
- [x] Sửa endpoint `assign/customers*` → `master-data/customers*` trong 9 file
- [x] Sửa link nội bộ:
  - [x] `pages/master-data/customers/index.vue` — 4 `$router.push` + 3 `to:` (dòng ~719-781)
  - [x] `components/assign-components/customer/CustomerForm.vue` — 2 `url-back`, 1 computed trả
        `/assign/customers` (dòng ~1612), 2 `$router.push` (dòng ~2654, ~2681)
  - [x] `pages/assign/solutions/components/InfoTab.vue` (dòng ~528, ~532)
  - [x] `pages/assign/solutions/components/manager/ProjectInfoTab.vue` (dòng ~244, ~248)
  - [x] `pages/assign/settlement_contract/index.vue` (dòng ~450 — url `assign/customers/search`)
  - [x] `components/modals/ChooseErpCustomerModal.vue` (endpoint + comment)
  - [x] `components/modals/QuickAddCustomerModal.vue`
- [x] Thêm redirect: `/assign/customers`, `/assign/customers/add`, `/assign/customers/:id`,
      `/assign/customers/:id/edit`, `/assign/customers/:id/manager`, `/assign/customer-scopes`,
      `/assign/customer-scope-groups` (khai cụ thể trước, `:id` sau)
- [x] Sửa 3 `link` trong `components/subsystem-menu/master-data.js`
- [x] `grep -rn "/assign/customer" hrm-client --include=*.vue --include=*.js` → chỉ còn
      `route-redirects.js` và các comment mô tả

---

## Phase 6 (A2) — Quyền + Verify giai đoạn A

- [x] Migration `2026_08_04_000001_move_customer_scope_permissions_to_master_data.php`:
      `UPDATE permissions SET type = 9, group = 'Danh mục đối tác' WHERE id IN (996, 1006, 1093, 1094)`;
      `down()` trả về `type = 4, group = 'Danh mục'`
- [x] Sửa 4 dòng tương ứng trong `PermissionsTableSeeder.php` (dòng 939, 950, 1055, 1056)
- [x] Chạy migration trên DB local
- [x] Màn Phân quyền: khối **"Phân hệ danh mục chung — 4"** hiện nhóm `Danh mục đối tác`;
      group `Danh mục` của type 4 vẫn còn 22 quyền; **0 group nào nằm ở 2 `type`**
- [x] `role_has_permissions` giữ nguyên **50 dòng** cho 4 quyền (id không đổi)
- [x] HTTP thật: **13/13 PASS** — 3 route cũ `/assign/customer*` → 404; `master-data/customers`,
      `my-permissions`, `search`, `customer-groups`, `provinces`, `banks`,
      `customer-scopes[/getAll]`, `customer-scope-groups[/getAll]` → 200
- [x] Browser: `/assign/customers` → `/master-data/customers` (10 dòng KH thật, sidebar
      "DANH MỤC CHUNG"); 2 màn lĩnh vực/nhóm lĩnh vực render đủ dữ liệu;
      `/assign/customers/14849/manager` → redirect đúng, mở đủ 5 tab
- [x] **Luồng tạo/sửa khách hàng (test Playwright + HTTP, có rollback)**:
  - Form `/master-data/customers/add`: cả **6 dropdown** gọi endpoint mới → 200
    (`customers/nations`, `customers/provinces`, `customer-scope-groups/getAll`,
    `customer-scopes/getAll`, `customers/vehicle-manufacts`, `customers/banks`);
    multiselect "Loại hình hoạt động" nạp đủ 23 nhóm; validate client chặn đúng khi thiếu trường
  - `POST master-data/customers`: 422 đúng chuẩn khi thiếu trường; đủ payload → **200**,
    tạo id 232388, **mã tự sinh `50TPHAPH`** (`CustomerCodeHelper` chạy đúng) + 1 người đại diện
    + 1 người liên hệ
  - `POST master-data/customers/{id}`: 200, đổi được `fullname`/`short_name`, `updated_by=13`
  - Màn chi tiết `/master-data/customers/14849`: render đầy đủ dữ liệu thật (tên, loại hình,
    ngày cấp, SĐT, quốc gia/tỉnh/phường)
  - DB trả nguyên trạng: `customers` 12.675 dòng, 0 bản ghi `ZZ TEST`, 0 deputy/contact mồ côi
- [x] **Picker KH dùng chung**: mở 6 màn (`quotations`, `bom-list`, `meeting`,
      `settlement_contract`, `report/solutions-work-summary-by-department`, `my-job`) →
      `master-data/customers/search` trả 200, không màn nào báo "Có lỗi xảy ra"

⚠️ **Lỗi 500 CÓ SẴN gặp khi test** (không do feature này):
`GET /api/v1/assign/prospective-projects/getAll` → 500 `Trying to get property 'employee_info_id'
of non-object` từ `app/Helper/PermissionHelper.php:22`. Đây đúng là lỗi đã làm crash
`php artisan route:list` từ Phase 1 — trước khi đụng tới `Modules/Assign`. Các file trong đường đi
lỗi (`PermissionHelper`, `ProspectiveProjectController`, `ProspectiveProjectService`) đều **không**
nằm trong danh sách file đã sửa.

💡 **Bài học đo đạc**: 2 lần tôi kết luận nhầm "màn trống/không có dữ liệu" chỉ vì đo quá sớm —
server dev là `php artisan serve` (đơn luồng) nên 5-6 request song song xếp hàng, màn KH cần ~15s.
Phải chờ tới khi hết "Đang tải dữ liệu" rồi mới đọc, và **đọc state component qua `$nuxt`**
thay vì `querySelector` (form có input ẩn trùng placeholder).
- [x] Redirect route con theo id chạy đúng · ghi checkpoint

🐛 **Lỗi tự gây khi làm Phase 4 — đã sửa: script đổi namespace hỏng 120 file Assign.**
Bản script đầu gộp chung "đổi tham chiếu" và "đổi dòng `namespace`" vào 1 danh sách chạy trên toàn
repo. Cặp `namespace Modules\Assign\Services;` → khớp **MỌI** service của Assign (TaskService,
QuotationService…), biến chúng thành `Modules\MasterData\Services`. Đã `git checkout --` hoàn tác
và viết lại thành **2 pha**: pha tham chiếu (có tên class cụ thể, chạy toàn repo) và pha namespace
(chỉ chạy trên `Modules/MasterData`). Kết quả đúng: 8 file tham chiếu thay vì 142.

⚠️ **Hệ quả dây chuyền của lệnh revert**: `git checkout -- Modules/Human` cũng hoàn tác luôn thay
đổi Phase 1 ở `Modules/Human/Routes/api.php` + 3 file `use` — đã làm lại. Nhân đó phát hiện Phase 1
**quét sót thư mục `database/`** (chỉ quét `Modules` + `app`), còn 2 seeder trỏ
`Modules\Human\Entities\Bank[Branch]`; đã sửa nốt.

🐛 **Migration chạy nhầm bảng — đã sửa.** Bản đầu `UPDATE hrm_permissions`: DB báo thành công,
`hrm_role_has_permissions` đếm ra 50 dòng hợp lý, nhưng màn Phân quyền vẫn trống.
Nguyên nhân: DB gộp có **2 bảng quyền** — `permissions` (1567 dòng, **bảng SỐNG**:
`App\Models\Permission::$table`, `config('permission.table_names.permissions')` và API
`/timesheet/permissions` đều trỏ vào đây) và `hrm_permissions` (600 dòng, tàn dư của lần gộp DB).
Đã rollback, đổi migration sang `permissions`, chạy lại → màn Phân quyền hiện đúng.
Memory `[[project_permissions_seeder_table_mismatch]]` đã được cập nhật (bản cũ ghi ngược).

---

## Phase 7 (B) — BE: Bảo hiểm → `Modules/Insurance`

- [x] Chuyển 4 Controller: `Insurance`, `InsuranceOutCompany`, `InsurancePackage`, `InsuranceType`
      Controller → `Modules\Insurance\Http\Controllers\V1\*`
- [x] Chuyển 4 Service: `Insurance/InsuranceService`, `InsuranceOutCompany/InsuranceOutCompanyService`,
      `InsurancePackage/InsurancePackageService`, `InsuranceType/InsuranceTypeService`
- [x] Chuyển Request: `Insurance/{InsuranceRequest,ReportInsuranceRequest}`,
      `InsuranceOutCompany/InsuranceOutCompanyRequest`,
      `InsurancePackage/{InsurancePackageRequest,InsurancePackageSearchRequest}`,
      `InsuranceType/InsuranceTypeRequest`
- [x] Chuyển Entity: `InsuranceType`, `InsuranceTypeLog`, `InsurancePackage`, `InsurancePackageDetail`,
      `InsurancePackageDetailInclude`, `InsurancePackageLog`, `InsurancePackageProgramRelation`,
      `InsurancePackageProgramRelationDetail`, `InsuranceRegister/*` (4), `InsuranceOutCompany/*` (6)
- [x] Chuyển `Transformers/Insurance/*` và `Export/ReportInsuranceRegister.php`
- [x] **Để lại Decision**: `Entities/Regulation/RegulationInsurance*` (6),
      `Entities/Benefit/BenefitInsurance*` (5), `Benefit/InsuranceConditionController`,
      `Services/Benefit/InsuranceConditionService`,
      `Transformers/BenefitGeneral/{BenefitInsuranceResource,InsurancePackageResource}`
      → sửa `use` của các file này sang `Modules\Insurance\Entities\*`
- [x] Tạo `Modules/Insurance/Http/Controllers/V1/InsuranceDeclarationReportController.php` — chuyển
      2 phương thức `reportInsuranceDeclaration` + `exportInsuranceDeclaration` từ
      `RegulationGeneralController`, query sang entity `Regulation*` bên Decision
- [x] Xóa 2 route `/report/insurance-declaration` (+ `/export`) khỏi nhóm `/v1/regulations/general`
      trong `Decision/Routes/api.php` (dòng ~523-524)
- [x] Khai route `Modules/Insurance/Routes/api.php` dưới `['prefix' => '/v1/insurance']`:
      `insurance-type`, `insurance-packages`, `insurance`, `insurance-out-company`,
      `report/insurance-register` (+ `/export`), `report/insurance-declaration` (+ `/export`)
      — copy nguyên endpoint từ `Decision/Routes/api.php` (dòng 162-169, 210-220, 452-479)
- [x] Xóa các khối route cũ khỏi `Decision/Routes/api.php` + `use` thừa
- [x] Giữ nguyên `Route::get('/insurance-types', [MasterDataController::class,'getInsuranceTypes'])`
      ở `/v1/decision/master-data` (dòng ~85) **nếu** còn màn Quyết định dùng — kiểm bằng grep FE;
      nếu chỉ màn bảo hiểm dùng thì chuyển sang Insurance
- [x] `composer dump-autoload` + `php artisan route:list --path=v1/insurance`
- [x] `grep -rn "Modules\\\\Decision\\\\Entities\\\\Insurance" hrm-api` → chỉ còn Regulation/Benefit
      trỏ sang namespace mới

---

## Phase 8 (B) — FE: 7 màn Bảo hiểm

- [x] `git mv` 6 thư mục:
  - `pages/decision/insurance` → `pages/insurance/insurance` (8 file)
  - `pages/decision/insurance-out-companies` → `pages/insurance/insurance-out-companies` (7 file)
  - `pages/decision/category/insurance-types` → `pages/insurance/category/insurance-types` (2 file)
  - `pages/decision/category/insurance-packages` → `pages/insurance/category/insurance-packages` (10 file)
  - `pages/decision/reports/insurance-register` → `pages/insurance/reports/insurance-register` (4 file)
  - `pages/regulations/insurance-declaration` → `pages/insurance/insurance-declaration` (2 file)
- [x] Đổi `layout: 'subsystem'` — 6 thư mục đầu đã là `'subsystem'`, xác nhận lại;
      `insurance-declaration` kiểm riêng
- [x] Sửa endpoint: `decision/insurance-type` → `insurance/insurance-type`,
      `decision/insurance-packages` → `insurance/insurance-packages`,
      `decision/insurance` → `insurance/insurance`,
      `decision/insurance-out-company` → `insurance/insurance-out-company`,
      `decision/report/insurance-register` → `insurance/report/insurance-register`,
      `regulations/general/report/insurance-declaration` → `insurance/report/insurance-declaration`
      (chú ý 2 URL export dựng chuỗi: `category/insurance-types/index.vue:379`,
      `category/insurance-packages/index.vue:373`)
- [x] Sửa link nội bộ:
  - [x] `insurance/index.vue` — `to="/decision/insurance/add"`, 3 `:to` theo id, 2 `pathsToKeep`
  - [x] `insurance/waiting-approve.vue` — `to`, 3 `:to`, 2 `pathsToKeep`
  - [x] `insurance/add.vue`, `insurance/_id/edit.vue` — `$router.push`
  - [x] `insurance-out-companies/index.vue` — `to`, 3 `:to`, 1 `pathsToKeep`
  - [x] `insurance-out-companies/add.vue`, `_id/edit.vue` — `$router.push`
  - [x] `insurance-declaration/index.vue:239` — `baseUrl` cho màn in
  - [x] `pages/human/self-notification/components/SelfNotificationForm.vue:306` —
        `link_register` đổi sang `/insurance/insurance/add`
- [x] Thêm redirect (khai theo thứ tự: cụ thể → có `:id` → tổng quát):
      `/decision/insurance/waiting-approve`, `/decision/insurance/add`,
      `/decision/insurance/:id/edit`, `/decision/insurance/:id/approve`, `/decision/insurance/:id`,
      `/decision/insurance`, cùng bộ tương tự cho `insurance-out-companies`,
      `/decision/category/insurance-types`, `/decision/category/insurance-packages`,
      `/decision/reports/insurance-register`, `/regulations/insurance-declaration`
- [x] Sửa 7 `link` trong `components/subsystem-menu/insurance.js`
- [x] `grep -rn "/decision/insurance\|/regulations/insurance-declaration" hrm-client
      --include=*.vue --include=*.js` → chỉ còn `route-redirects.js`

---

## Phase 9 (B) — Quyền + Verify giai đoạn B

- [x] Migration `2026_08_04_000002_move_insurance_permissions_to_insurance_subsystem.php` —
      ⚠️ **24 quyền, không phải 20** (Phase 0 ghi nhầm: 20 quyền ở 4 nhóm **cộng thêm** 4 quyền
      báo cáo 961-964):
  - [x] `UPDATE permissions SET type = 11` cho 20 id (404-406, 897-898, 887-891, 947-951, 955-959)
        — giữ nguyên `group`
  - [x] Riêng **961-964**: thêm `group = 'Báo cáo bảo hiểm'` (đang là `Báo cáo quyết định`, group đó
        còn 969-970 thang bảng lương **ở lại** Decision → giữ tên cũ sẽ làm 1 group nằm ở 2 `type`)
  - [x] `down()`: trả `type = 6` cho cả 24, `group = 'Báo cáo quyết định'` cho 961-964
  - [x] Nhắm bảng **`permissions`** ngay từ đầu (rút kinh nghiệm Phase 6)
- [x] Sửa `PermissionsTableSeeder.php`: 20 dòng giữ group + 4 dòng đổi group
- [x] **Không** đụng id 386-390, 806, 808 (`Xem bảo hiểm theo tháng/năm`, type 3, group `Báo cáo`)
      — báo cáo của phân hệ Nhân sự, không thuộc menu Bảo hiểm
- [x] Chạy migration: 24 quyền về `type=11` trong 5 nhóm; 969-970 vẫn `type=6`;
      **0 group nằm ở 2 type**; 130 dòng `role_has_permissions` giữ nguyên
- [x] HTTP thật: **12/12 PASS** — 6 route cũ (`decision/insurance-type`, `insurance-packages`,
      `insurance`, `insurance-out-company`, `report/insurance-register`,
      `regulations/general/report/insurance-declaration`) → 404; 6 route mới → 200
- [x] Redirect **7/7** chạy, đúng title: `/decision/insurance` → `/insurance/insurance`
      (10 dòng), `waiting-approve`, `insurance-out-companies` (2), `category/insurance-types` (3),
      `category/insurance-packages` (3), `reports/insurance-register`, `insurance-declaration`
- [x] Toàn bộ API bảo hiểm trên browser trỏ `/v1/insurance/*` → 200; chỉ còn đúng 1 lời gọi
      `decision/master-data/insurance-types` — là chỗ **cố ý giữ lại** ở Decision

**Vòng kiểm bổ sung (Playwright) — đã làm nốt:**

- [x] **Báo cáo đăng ký bảo hiểm chạy thật**: chọn Loại bảo hiểm → bấm tìm → cả **3 phần** gọi
      `/v1/insurance/report/{insurance-register, out-company-single-employee-insurance,
      out-company-group-employee-insurance}` → 200, bảng ra 18 dòng có số tiền.
      Màn này **không tự gọi API** khi mở, phải chọn Loại BH hoặc Gói BH rồi bấm tìm →
      "0 dòng" lúc mới vào là đúng thiết kế.
- [x] **Xuất Excel 3/4 OK**: `report/insurance-register/export` (14 KB, ms-excel),
      `report/insurance-declaration/export` (82 KB, xlsx), `insurance-type/export` (81 KB).
- [x] **Màn in**: `category/insurance-types/print` + `category/insurance-packages/print` render
      đủ tiêu đề + bảng.
- [x] **Quy chế chung** (`/regulations/general`) — chỗ có phụ thuộc chéo Decision → Insurance —
      load **103 dòng**, không lỗi.
- [x] **Màn Phân quyền**: khối **"Phân hệ bảo hiểm xã hội — 24"** đủ **5 nhóm** (Quản lý loại BH,
      Quản lý gói BH, BH ngoài công ty, BH nhân viên, Báo cáo bảo hiểm); "Danh mục chung — 4";
      "Quyết định — 54" vẫn giữ nhóm `Báo cáo quyết định` (969-970).
- [x] Form **Tạo gói bảo hiểm** / **Tạo đăng ký BH ngoài công ty** mở bình thường.
- [x] `waiting-approve` 0 dòng là **đúng dữ liệu**: `insurance_registers` có 718 bản ghi nhưng
      **không có** `status=2` (màn lọc theo status=2).

🐛 **BUG THẬT DO CHUYỂN — ĐÃ SỬA: màn Tạo phiếu đăng ký BH bị chặn.**
`pages/insurance/insurance/{add,_id/edit}.vue` dùng `middleware: 'checkLinkRegister'`, middleware
này gọi `human/self-notifications/check-link-register` với `window.location.origin + $route.path`,
còn `SelfNotificationService::checkLinkRegister` so **khớp tuyệt đối** với cột
`self_notifications.link_register`. Trong DB có **6 bản ghi** trỏ `/decision/insurance/add` → sau
khi đổi route thì không bao giờ khớp, user bị đá về `/pages/extras/404` kèm "Đã hết hạn đăng ký!".
Redirect FE **không cứu được** vì so sánh xảy ra ở BE trên đường dẫn thật.
→ Thêm migration `2026_08_04_000003_update_self_notification_link_register_to_insurance_subsystem`
(REPLACE đuôi đường dẫn, giữ nguyên scheme + domain nên chạy được mọi môi trường). Đã chạy: 6/6 dòng
đổi sang `/insurance/insurance/add`.
⚠️ **Chưa mở được màn Tạo trên máy local** để xác nhận end-to-end: 6 thông báo đó trỏ domain
`hrm.eteksofts.com` (không phải `127.0.0.1:3000`) và **đều đã hết hạn** (`register_end_date`
mới nhất là 2026-07-10). Cần verify trên môi trường có thông báo đăng ký còn hiệu lực.

🐛 **BUG CÓ SẴN, chưa sửa (theo quyết định "giữ nguyên" của user):**
`insurance-packages/export` trả **500** vì trong `InsurancePackageController::export()` còn sót
`dd($data);` — có từ commit `a4890ae92 xuất excel`, không liên quan tới lần chuyển này.
Sửa = xoá đúng 1 dòng.

**Lệch so với spec (có chủ đích):**

- `getInsuranceTypes` + `Transformers/MasterData/InsuranceTypeResource` **ở lại Decision**:
  nằm trong `MasterDataController` dùng chung với ranks/missions/titles/general-regulations, và
  `MasterDataService` là service dùng chung — rule project là hỏi trước khi sửa hàm dùng chung.
  Màn Báo cáo đăng ký bảo hiểm vẫn gọi `decision/master-data/insurance-types`.
- Spec viết "chiều Insurance → Decision không được phép", nhưng thực tế **không tránh được**:
  phiếu đăng ký bảo hiểm dựng trên nền Quyết định — `InsuranceRequest`/`InsuranceOutCompanyRequest`/
  `InsurancePackageRequest` đều `extends DecisionRequest`, `InsuranceService` dùng `Decision` và
  `DecisionLaborContract`. Đây là ràng buộc nghiệp vụ, gỡ được phải thiết kế lại.

---

## Phase 10 — Dọn & tổng kết

- [x] Chạy lại audit menu: `master-data` và `insurance` về **0 mục link route cũ**;
      chỉ còn `sale` **29 mục** (đúng dự kiến — đợt sau)
- [x] Bất biến "mỗi link chỉ thuộc 1 phân hệ": **0 link trùng**
- [x] Layout đồng nhất: `pages/master-data` 15/15 file `layout: 'subsystem'`,
      `pages/insurance` 18/18 file `layout: 'subsystem'`
- [x] **35 cặp redirect** trong `config/route-redirects.js`
- [x] Cập nhật `STATUS.md`
- [x] Ghi memory: [[project_permissions_seeder_table_mismatch]] (viết lại — bản cũ ghi ngược bảng),
      [[feedback_no_bulk_sed_on_windows]], [[project_bank_branch_constructor_bug]],
      [[project_chuyen_code_phan_he_quy_trinh]]

**Việc còn nợ sau feature này:**

1. **Phân hệ Bán hàng (`sale`) — 29 mục** vẫn ở `/assign/*`, là đợt lớn nhất còn lại.
2. **7 màn địa lý - ngân hàng không có permission nào** — ai đăng nhập cũng vào được (chưa xử lý,
   chờ user quyết).
3. ~~5 route trỏ method không tồn tại~~ → **ĐÃ SỬA**, xem Phase 11.
4. **Xuất Excel gói bảo hiểm vẫn chưa chạy** — đã gỡ `dd($data)` nhưng lộ ra nguyên nhân sâu hơn:
   **view `resources/views/exports/insurance_package.blade.php` chưa từng được tạo**. Xem Phase 11.
5. **`CustomerService` + `CustomerManagerService` vẫn gọi `ErpPermissionHelper`** (qua `mysql2`) —
   phụ thuộc đi theo sang `Modules/MasterData`.

---

## Phase 11 — Dọn lỗi có sẵn (2026-08-04, sau khi user duyệt)

- [x] **Xóa `dd($data);`** trong `Modules/Insurance/.../InsurancePackageController::export()`
      (có sẵn từ commit `a4890ae92 xuất excel`)
- [x] **Đổi tên `WardController::getListProvince` → `getListWards`** — tên cũ là lỗi copy-paste từ
      `ProvinceController` trong khi route `GET master-data/wards/list` trỏ `getListWards`; thân hàm
      vốn đã gọi đúng `wardsService->getListWards()`. → endpoint **500 → 200**
- [x] **Bỏ 4 route chết** `PUT master-data/{nations,areas,provinces,wards}/{id}` — 4 controller đều
      không có `update()`, FE dùng `POST /` cho cả thêm lẫn sửa (kiểm trong
      `{Nation,Areas,Province,Ward}Model.vue`). Thay bằng comment giải thích. → `PUT` trả **405**
- [x] Verify: `master-data` **118 route** (122 − 4), `insurance` 38 route, **0 route trỏ method
      không tồn tại** ở cả 2 phân hệ; 6/6 endpoint `/list` trả 200

🔍 **Phát hiện thêm khi gỡ `dd()`**: xuất Excel gói bảo hiểm trả **400
`View [exports.insurance_package] not found`** — file view **chưa từng tồn tại**, tức tính năng
làm dở chứ không chỉ sót dòng debug (`dd()` là dấu vết dev đang làm giữa chừng).

- [x] **Đã dựng `resources/views/exports/insurance_package.blade.php`** (user chốt: xuất **tất cả
      cột trên màn danh sách**). 9 cột đúng thứ tự màn: STT · Mã gói bảo hiểm · Gói bảo hiểm ·
      Loại bảo hiểm · Nhà cung cấp · Thời gian áp dụng · Người tạo · Ngày tạo · Trạng thái.
      Bám mẫu `exports/insurance_type.blade.php` (logo TPE + tiêu đề + khối ký tên).
- [x] **Cột "Trạng thái" phải TÍNH LẠI trong blade** — API không trả nhãn này, FE tự tính từ
      `status` + `effective_date` + `expiry_date` (`getStatusText()` ở
      `pages/insurance/category/insurance-packages/index.vue:469`). Đã replicate y hệt 4 nhánh:
      `status=1` → "Đang tạo"; `status=2` + đã tới ngày hiệu lực + chưa hết hạn → "Có hiệu lực";
      + đã hết hạn → "Hết hiệu lực"; + chưa tới ngày hiệu lực → "Đã duyệt".
- [x] Verify: `GET insurance-packages/export` → **200**, `application/vnd.ms-excel`, 82 KB.
      Đọc lại file bằng PhpSpreadsheet: header đủ 9 cột, 3 dòng dữ liệu khớp màn hình
      (BH26004 "Có hiệu lực", 2 gói BH25003 "Hết hiệu lực", người tạo Ngô Thị Lý).
- [x] Render blade với dữ liệu giả để kiểm cả 4 nhánh trạng thái + vị trí cột → đúng hết.

⚠️ **Cột "Nhà cung cấp" rỗng trên DB local** — không phải lỗi code: `InsurancePackageResource`
tra `TpSupplier` (bảng `customers`), mà `supplier_id` của 3 gói (36447, 37927, 11803) **không có
trong bảng `customers` local** (id lớn nhất chỉ 32200). DB local là snapshot thiếu dữ liệu
(xem [[feedback_local_db_differs_prod]]). Trên môi trường của user cột này có dữ liệu — ảnh chụp
màn hình đã xác nhận. Đã kiểm cột map đúng vị trí bằng cách render blade với dữ liệu giả.

⚠️ Ghi chú môi trường: BE dev server của user tắt giữa chừng nên tôi bật tạm 1 server ở **port 8010**
để verify rồi tắt đúng 2 PID của mình (30636, 53304), giữ nguyên server của user ở port 8000.
6. **Verify màn Tạo phiếu đăng ký BH** trên môi trường có thông báo đăng ký còn hiệu lực
   (local không kiểm được, xem ghi chú Phase 9).
7. Cảnh báo Vue có sẵn `The computed property "fields" is already defined in data` ở nhiều màn.

---

## Checkpoint — 2026-08-04

Vừa hoàn thành: **toàn bộ Phase 0-10**. Hai phân hệ **Danh mục chung** (10 màn, 122 route) và
**Bảo hiểm xã hội** (7 màn, 38 route) đã chạy hoàn toàn ở phân hệ của mình — BE, FE, redirect,
quyền. Audit menu về 0 mục lệch, 0 link trùng, layout đồng nhất.

Đang làm dở: (không)

Bước tiếp theo: phân hệ **Bán hàng** — 29 mục `/assign/*` → `/sale/*`. Áp lại đúng quy trình 7 bước
đã định hình ở feature này (xem memory `project_chuyen_code_phan_he_quy_trinh`).

Blocked: (không)

---

## Phase 12 — Bán hàng, đợt 1: nhóm Danh mục + Thiết lập (11 màn) — 2026-08-05

Đợt đầu của phân hệ **Bán hàng** (29 mục `/assign/*` → `/sale/*`). Chọn nhóm Danh mục làm
trước vì thuần CRUD, ít ràng buộc, dùng để kiểm lại quy trình trên tiền tố route mới.

**11 màn:** industry-groups (Nhóm ngành), solution-groups (Nhóm giải pháp), application,
project_items, project_phase, project_role, reason_project_failure, attachment-type,
discount-types, form-templates, settings/price-approval (Cấu hình duyệt giá).

### Đã làm

- [x] **BE**: `git mv` 22 Entity + 11 Controller + 11 Service + 10 thư mục Request +
      10 thư mục Transformer từ `Modules/Assign` → `Modules/Sale`.
      Cắt 11 khối route sang `Modules/Sale/Routes/api.php` → **110 route `/api/v1/sale/*`**,
      0 route `/api/v1/assign/*` cũ còn sót.
      Đuôi route giữ nguyên tên cũ (`/sale/scopes`, `/sale/industries`…) để đối chiếu.
- [x] **FE**: `git mv` 30 file page `pages/assign/*` → `pages/sale/*`;
      đổi endpoint + link nội bộ ở **52 file** (kể cả `store/actions.js`,
      `store/optionsSelect.js`, 7 modal dùng chung, 18 màn Giao việc còn ở lại).
- [x] **Redirect**: thêm 19 cặp vào `config/route-redirects.js`. Verify 13/13 URL cũ nhảy đúng.
- [x] **Menu**: `sale-hub.js` + `sale.js` tự cập nhật theo (22 dòng mỗi file).
- [x] **Quyền**: migration `2026_08_05_000001_...` chuyển 18 id (983-1090) `type 4 → 23`,
      `group 'Danh mục' → 'Danh mục bán hàng'`. Verify màn Phân quyền: tab
      **"Phân hệ bán hàng 18"** có nhóm **"Danh mục bán hàng"**; không group nào trải 2 `type`.
- [x] **Verify**: 11/11 endpoint trả 200; 13/13 redirect đúng; sidebar `SaleHubSidebar`
      ("BÁN HÀNG" + 10 nhóm) hiện đúng ở `/sale/*`; console 0 lỗi sau khi vá.

### ⚠️ Khác biệt so với 2 phân hệ trước: KHÔNG đổi `layout`

Danh mục chung / Bảo hiểm dùng `layout: 'subsystem'`. Bán hàng thì **không** — phân hệ này có
sidebar riêng kiểu MISA (`SaleHubSidebar`), chỉ render khi layout là `default-sidebar`
(xem `layouts/default-sidebar.vue`: `v-if="isSaleSubsystem"`). Đổi sang `subsystem` là mất
sidebar Bán hàng. → **Giữ nguyên `layout: 'default-sidebar'` cho toàn bộ màn `/sale/*`.**

### 🐞 Bẫy MỚI: class cùng namespace gọi KHÔNG có `use`

`Entities\DiscountType` gọi `QuotationDiscount::class` mà không khai `use` — trước đây tự phân
giải nhờ cùng namespace `Modules\Assign\Entities`. Đổi namespace sang `Modules\Sale\Entities` →
PHP đi tìm `Modules\Sale\Entities\QuotationDiscount` → **"Class not found"** lúc chạy, `php -l`
KHÔNG bắt được. Tìm thấy 6 chỗ:

| Class thiếu | Xử lý |
|---|---|
| `FormGroupSnapshot`, `FormQuestionOptionSnapshot`, `ProjectPhaseItems` | chuyển luôn sang Sale (thuộc cùng nghiệp vụ) |
| `QuotationDiscount` (Báo giá), `SurveyQuestion` (Câu hỏi khảo sát) | ở lại Giao việc → thêm `use` tường minh |

Script quét: `scratchpad/find_unqualified.js` — với mỗi file trong module đích, tìm tên class
được dùng mà (a) không có `use`, (b) không tồn tại trong module đích, (c) **có** tồn tại trong
module nguồn. **Phải chạy script này sau mỗi lần đổi namespace.**

### 🐞 Lỗi có sẵn đã vá: `hrm_scopes` vs `scopes`

Màn **Ứng dụng** trả 500 `Unknown column 's.code'`. Nguyên nhân từ đợt gộp DB, không phải do
chuyển code: entity `Scope` trỏ bảng `hrm_scopes` (quy ước prefix `hrm_`, xem
[[project_gop_db_table_prefix_convention]]) nhưng 2 câu query thô vẫn `join('scopes as s')` —
`scopes` là bảng của ERP, không có cột `code`. Đã sửa 2 chỗ:
`Modules/Sale/Entities/Applications.php::industryPairs()` và
`Modules/Sale/Services/ApplicationService.php::loadIndustryScopeSet()`. Sau khi vá: 200.

### ✅ Đã tách quyền 211 (user chốt 2026-08-05)

Trước đây 1 quyền id 211 `Cấu hình phân hệ giao việc/ công tác` gate CẢ 2 màn ở 2 phân hệ:
`/assign/settings` (Giao việc, ở lại) và `/sale/settings/price-approval` (Bán hàng, đã chuyển)
→ admin không thể mở quyền cho bên này mà không mở luôn bên kia.

Migration `2026_08_05_000002_split_bom_price_approval_permission_from_assign_config.php`:

- Thêm quyền **id 1121** `Cấu hình duyệt giá BOM giải pháp`, group `Thiết lập bán hàng`, `type 23`.
- Copy nguyên **12 cặp (role, company)** đang giữ 211 sang 1121 → **không ai mất quyền đang có**.
  ⚠️ `role_has_permissions` phân quyền theo TỪNG CÔNG TY (cột `company_id`), phải copy đủ cặp,
  không chỉ `role_id`.
- Làm rõ `display_name` của 211 thành *"Cấu hình phân hệ Giao việc/Công tác (không bao gồm cấu
  hình duyệt giá BOM)"* để người dùng sau nhìn màn Phân quyền là hiểu. Cột `name` giữ nguyên vì
  đó là khoá `checkPermission` đang dùng ở FE/BE. `Permission.vue` hiển thị `display_name`.
- FE: `sale.js` đổi gate sang quyền mới. BE: **thêm middleware `checkPermission` cho 3 route**
  `/sale/bom-price-approval-configs/*` — trước đây 3 route này KHÔNG có gate nào, chỉ ẩn/hiện menu.
- Verify: user có quyền → 200; user không có → **403**.

### Chưa xử lý (cần user quyết)

1. **`FormAnswerHistoryService`** vẫn ở `Modules/Assign` vì `ProspectiveProjectService` và
   `MeetingService` cũng dùng → Sale phụ thuộc ngược lại Assign. Sẽ hết khi chuyển nhóm Dự án TKT.
2. Vài entity ở lại Assign (`RequestSolution`, `SurveyQuestion`, `QuotationDiscount`,
   `ProspectiveProject`) nhưng bị Sale tham chiếu — chấp nhận tạm, giải quyết ở đợt Dự án TKT.
3. **Chuẩn layout mới** (user chốt 2026-08-05): layout Bán hàng (`SaleHubSidebar` kiểu MISA qua
   `default-sidebar`) là chuẩn chung cho phân hệ mới. Danh mục chung + Bảo hiểm hiện vẫn ở
   `layouts/subsystem.vue` → có chuyển 2 phân hệ này sang chuẩn mới không, và bao giờ?
   Muốn tổng quát hoá thì phải sửa `isSaleSubsystem` trong `layouts/default-sidebar.vue`
   (hàm dùng chung → cần user đồng ý) + dựng file `<slug>-hub.js` cho từng phân hệ.
   Xem memory [[project_subsystem_layout_standard_sale]].

### Còn lại của phân hệ Bán hàng (18 mục)

| Đợt | Nhóm | Số mục |
|---|---|---|
| 2 | Dự án TKT + Phê Duyệt (2 màn pending nằm trong `request-solution`/`quotations`) | 8 |
| 3 | Báo cáo Dự án TKT (`/assign/report/*` — chỉ 8/12 thư mục chuyển, 4 ở lại Giao việc) | 8 |

⚠️ Đợt 3 **không** `git mv` cả thư mục `report/` được: `assign_task_by_province.vue`,
`assign_task_department_by_customer.vue`, `work_and_performance.vue`, `meeting-by-*` ở lại
Giao việc. Phải chuyển từng thư mục con.

---

## Phase 13 — Chuẩn hoá layout + dọn quyền khách hàng — 2026-08-05

### A. Layout hub thành chuẩn chung (user chốt)

Trước: `SaleHubSidebar` gắn cứng phân hệ Bán hàng; Danh mục chung + Bảo hiểm dùng
`layouts/subsystem.vue` (menu dọc UBold). Sau: **1 kiểu sidebar cho mọi phân hệ đã chuyển.**

| File | Thay đổi |
|---|---|
| `components/subsystem-menu/hub.js` *(mới)* | `HUB_SUBSYSTEMS` = danh sách phân hệ dùng chuẩn hub; `hubGroupsFor()` trả nhóm |
| `components/sale/SaleHubSidebar.vue` | Bỏ hằng số cứng: tên/`/[key]/dashboard`/màu nhóm/key localStorage đều suy từ `resolveSubsystem()` |
| `layouts/default-sidebar.vue` | `isSaleSubsystem` → `HUB_SUBSYSTEMS.includes(key)` |
| 33 page `master-data` + `insurance` | `layout: 'subsystem'` → `'default-sidebar'` |

**Không viết file hub thứ hai cho mỗi phân hệ.** `deriveHubGroups()` suy nhóm thẳng từ cây menu
2 cấp có sẵn trong registry → giữ nguyên tắc 1 phân hệ = 1 nguồn menu. Chỉ Bán hàng khai tay
(`sale-hub.js`) vì menu 4 cấp và có màn chưa có link.

Hai chi tiết phải xử lý khi tổng quát hoá:

- **Icon 2 dạng**: `sale-hub.js` dùng inline SVG, cây menu các phân hệ khác dùng class Remix →
  thêm `isSvgIcon()`, render `<svg v-html>` hoặc `<i :class>` + style `.cat-ic-font`.
- **Tiêu đề lặp**: nhóm suy ra có đúng 1 mục trùng tên nhóm → `flatHtml` bỏ tiêu đề cấp 2,
  render thẳng danh sách màn.

Verify browser: Danh mục chung ("DANH MỤC CHUNG", 2 nhóm, icon font, panel 7 màn, không lặp tiêu
đề), Bảo hiểm ("BẢO HIỂM XÃ HỘI", 4 nhóm, màu `#2E71C3` của nhóm Nhân sự, Tổng quan →
`/insurance/dashboard`), **hồi quy Bán hàng** (13 nhóm, màu `#6B54B8`, 13 icon SVG, panel nav-mode
vẫn chạy). 0 lỗi console mới.

### B. Dọn phần khách hàng "chuyển hẳn sang HRM"

Khảo sát cho thấy **ghi chú cũ đã lỗi thời**: `CustomerService`/`CustomerManagerService` KHÔNG
còn dùng `mysql2` — `ErpPermissionHelper` đọc connection mặc định trên DB gộp, cùng bộ bảng
`permissions`/`employee_has_*`/`role_has_permissions` mà spatie dùng. Vấn đề thật là 2 chỗ khác:

1. **10 quyền khách hàng vô hình trên màn Phân quyền HRM** (`type = NULL` nên không thuộc tab
   phân hệ nào) → admin không cấp được "Xem tất cả khách hàng của công ty/phòng ban/bộ phận".
   Migration `2026_08_05_000003_...` đưa về `type = 9` (Danh mục chung), giữ nguyên `id`/`name`
   nên `role_has_permissions` và mọi chỗ kiểm quyền theo tên không đổi.
   Id 100228 (màn báo cáo còn ở ERP) tách sang group riêng để group không trải 2 `type`.
   Verify: tab "Phân hệ danh mục chung" **4 → 14 quyền**, nhóm `Quản lý khách hàng` hiện ra.
2. **`erpEmployeeId()` đi vòng thừa** `employee_info_id → employees.employee_info_id → id`.
   Kiểm cả 1085 nhân sự: **0 lệch, 0 trùng, 0 rỗng** → thay bằng `auth()->user()->id`.
   Bỏ 1 query mỗi lần gọi (riêng `CustomerService` gọi 5 lần/request).
   Verify: `/master-data/customers` 200, `/master-data/customers/my-permissions` trả đúng
   `view/create/edit/delete + is_all_company/is_company/is_department/is_part`.

⚠️ **Đừng thay `ErpPermissionHelper::userCan()` bằng `isCurrentEmployeeHasPermission()`** —
helper khớp theo tên, KHÔNG lọc `role_has_permissions.company_id`, và có tính quyền cấp trực tiếp
cho employee; hàm HRM thì ngược lại. Đã ghi rõ trong docblock.

**Còn nợ:** bộ quyền khách hàng CŨ của HRM (id 166-169, group `Danh mục khách hàng`, type 3) tồn
tại song song; id 167 trùng tên với 100170 nên `userCan()` khớp cả hai. Gộp/bỏ là quyết định
nghiệp vụ, cần user chốt.

---

## Phase 14 — Bán hàng, đợt 2: nhóm Báo cáo Dự án TKT (8 màn) — 2026-08-05

**8 màn:** prospective-projects, customer-development, performance-by-employee,
performance-by-solutions, solution-requests-by-department, solutions-work-summary-by-department,
solution-versions, task-manager-by-employees.

### Đã làm

- [x] **BE**: 8 Controller + 7 Service `Services/Report` + 5 thư mục Transformer → `Modules/Sale`.
      7 nhóm route `/assign/report/<tên>` → `/sale/report/<tên>`.
      **136 route** `/api/v1/sale/*` (đợt 1: 110 → +26), 0 route cũ sót.
- [x] **FE**: 38 file page → `pages/sale/report/*`; 20 file đổi endpoint + link.
- [x] **Redirect**: 16 cặp (mỗi màn có thêm route con `/print`). Verify 16/16 + 2 báo cáo ở lại
      Giao việc không bị đụng.
- [x] **Verify**: 8/8 endpoint 200, 3 dropdown lọc có dữ liệu, 0 lỗi console.

### ⚠️ 2 cái bẫy riêng của đợt này

1. **`performance-by-employee` KHÔNG có nhóm route riêng** — 2 route của nó nằm lẫn trong nhóm
   `/assign/reports` (số nhiều) dùng chung với báo cáo meeting / work-and-performance **ở lại**
   Giao việc → phải cắt theo TỪNG DÒNG, không cắt cả khối. Đuôi giữ nguyên:
   `/sale/reports/performance-by-employee`.
2. **Tiền tố `/assign/report` dùng chung** với 5 màn ở lại (`meeting-by-*`, `work_and_performance`,
   `assign_task_*`) → redirect và script đổi endpoint phải khớp theo TỪNG TÊN MÀN,
   tuyệt đối không thay cả tiền tố.

### 🐞 Lỗi ĐỢT 1 lọt lưới, phát hiện ở đợt này (nghiêm trọng nhất)

`/assign/prospective-projects/getAll` và `/assign/solutions/getAll` **500** sau đợt 1.
Nguyên nhân: script quét `find_unqualified.js` chỉ soi **module ĐÍCH** (file chuyển đi gọi class
ở lại) mà **sót chiều ngược lại** — file **Ở LẠI** `Modules/Assign` gọi class **đã chuyển đi**
không có `use` (trước tự phân giải nhờ cùng namespace). **17 chỗ gãy trên 11 file**, `php -l`
không bắt, chỉ 500 lúc chạy:

| File ở lại Assign | Class đã chuyển bị gọi trần |
|---|---|
| `Entities/ProspectiveProject.php` | FormTemplateSnapshot, Industries, ProjectPhases, ReasonProjectFailure |
| `Entities/Solution.php` | Applications, Industries |
| `Entities/ProjectPhase{Applications,Industries,Scopes}.php` | ProjectPhases, Applications, Industries |
| `Entities/{FormAnswerHistory,QuotationDiscount,RequestSolution,SolutionManagerLog}.php` | FormTemplateSnapshot, DiscountType, Industries, ProjectRoles |
| `Services/Quotation{Import,}Service.php` | DiscountTypeService, BomPriceApprovalConfigService |

→ Script mới `scratchpad/find_unqualified2.js` quét **CẢ 2 CHIỀU**. **Bắt buộc chạy sau mỗi lần
chuyển class giữa 2 module.**

Ngoài ra: sau khi `git mv` file PHP phải chạy **`composer dump-autoload`** — classmap còn trỏ
đường dẫn cũ nên lỗi hiện ra dưới dạng `include(...): failed to open stream` gây hiểu nhầm.

⚠️ Script đổi namespace pha 2 khớp cả chuỗi `namespace Modules\Assign\` nằm trong **comment** →
làm hỏng nghĩa 2 comment ở `DiscountType.php` / `FormQuestion.php` (chỉ comment, không phải code).
Đã sửa tay. Lần sau neo regex vào đầu dòng (`/^namespace .../m`).

### 🐞 2 lỗi có sẵn đã vá (chặn màn vừa chuyển)

1. **`filter-options` trả 400** `Unknown column 'scope_id'` → **cả 3 dropdown lọc trống**.
   Từ đợt refactor nhiều-nhiều, `industries` / `applications` không còn cột FK trực tiếp; liên kết
   nằm ở `industry_scopes` và `application_industries`. Sửa BE trả **mảng** `scope_ids` /
   `industry_ids` (1 ngành thuộc nhiều nhóm ngành), FE lọc tầng bằng `includes()` thay vì so 1 id.
2. **`prospective-projects/getAll` 500** `Trying to get property 'employee_info_id' of non-object`:
   `ProspectiveProjectResource` gọi `Employee::find(...)->employee_info_id` không guard null,
   trong khi nhánh `solution_employee_id` ngay dưới đã guard. Nhân viên KD chính bị xóa là văng
   cả endpoint. Đã guard theo đúng kiểu code bên cạnh.

### Ghi chú

`components/assign-components/assign-slidebar.vue` (sidebar Giao việc cũ) có 1 link tới
"Báo cáo hiệu suất làm việc theo Giải pháp" — nay trỏ `/sale/report/performance-by-solutions`.
File này KHÔNG nằm trong registry `subsystems.js` nên không ảnh hưởng `resolveSubsystem`,
nhưng là 1 lối tắt từ Giao việc sang Bán hàng — cần user quyết có bỏ khỏi menu Giao việc không.

### Còn lại: đợt 3 — Dự án TKT + Phê Duyệt (8 mục)

prospective-projects, request-solution (+ `/pending`), solutions, solution-modules,
product-project, bom-list, pricing-requests, quotations (+ `/pending-approval`).
Đợt này sẽ gỡ nốt phụ thuộc chéo Sale ↔ Assign còn lại (`FormAnswerHistoryService`,
`ProspectiveProject`, `RequestSolution`, `SurveyQuestion`, `QuotationDiscount`).

---

## Phase 15 — Bán hàng, đợt 3: Dự án TKT + Phê Duyệt (8 màn) — 2026-08-05

Đợt cuối và lớn nhất: prospective-projects, request-solution (+ `/pending`), solutions,
solution-modules, product-project, bom-list, pricing-requests, quotations (+ `/pending-approval`).

### Đã làm

- [x] **BE**: 34 Entity + 12 Service + 11 Controller + 7 thư mục Request + 5 thư mục Transformer
      + 8 file Transformer lẻ → `Modules/Sale` (202 → tổng file module Sale).
      11 nhóm route + 4 nhóm route lẻ → `/sale/*`. **313 route** `/api/v1/sale/*`.
- [x] **FE**: 111 file page `pages/assign/*` → `pages/sale/*`; 116 file đổi endpoint/link;
      3 thư mục component (`pricing-request`, `prospective-project`, `quotation`)
      `components/assign/` → `components/sale/`.
- [x] **Redirect**: nâng bảng lên **98 cặp**. Kiểm bằng script: 0 trùng `from`,
      0 sai thứ tự (route cụ thể luôn đứng trước route `:id`), 0 sai định dạng.
- [x] **Verify BE**: 11/11 endpoint mới 200; hồi quy 12 endpoint Giao việc còn lại đều OK.
- [x] Quét class gãy **2 chiều**: sạch. `composer dump-autoload` đã chạy.

### ⚠️ Endpoint tích hợp ERP→HRM GIỮ NGUYÊN URL

`/v1/assign/quotations/erp-contract/*` (3 route) là hợp đồng tích hợp với **codebase ERP nằm
ngoài repo này** — đổi URL là ERP gọi hỏng. Đã chuyển *định nghĩa route* sang
`Modules/Sale/Routes/api.php` cho đúng phân hệ nhưng **giữ nguyên đường dẫn `/assign/...`**,
có ghi chú tại chỗ. Đây là 3 route `/assign/*` duy nhất còn lại của nhóm Dự án TKT.

### 🐞 Lỗi tự gây, đã sửa: script đổi endpoint ăn cả đường dẫn IMPORT

Rule `assign/pricing-request(?![A-Za-z0-9_-])` khớp luôn chuỗi trong
`@/components/assign/pricing-request/PricingRequestDetailModal.vue` (ký tự sau là `/`, không bị
lookahead chặn) → import trỏ `components/sale/...` trong khi thư mục vẫn ở `components/assign/`
→ màn Yêu cầu báo giá **trắng trang**: `Cannot find module`.

Sửa: chuyển luôn 3 thư mục component sang `components/sale/` (đúng nghĩa vì chúng thuộc các màn
vừa chuyển) rồi đồng bộ nốt các import còn trỏ `components/assign/`.

**Bài học** — sau mỗi lần đổi chuỗi hàng loạt ở FE, chạy script kiểm **mọi import alias
(`@/`, `~/`) có trỏ tới file CÓ THẬT không**. Quét 1883 file: chỉ còn 4 import hỏng có sẵn từ
trước (`@/state/helpers` ×3, `@/api/modules/training/career-progression`), không liên quan.

### Phụ thuộc chéo còn lại (chấp nhận, có chủ đích)

| Sale gọi Assign | Lý do |
|---|---|
| `assign/priority-levels/getAll` | Mức độ ưu tiên do màn Cấu hình Giao việc quản lý, `Task` cũng dùng |
| `ErpProductSearchService` | tra hàng hoá ERP, dùng chung |
| `FormAnswerService` | dùng chung với Meeting |
| `TpGroupProduct`, `ErpCostController` | mirror ERP dùng chung |

Chiều ngược lại: `Assign\Entities\Issue` và `MeetingService` tham chiếu entity/service của Sale —
đã khai `use` tường minh.

### ✅ Verify trình duyệt (sau khi user restart `npm run dev`)

| Hạng mục | Kết quả |
|---|---|
| 10 màn danh sách | 10/10 `matched=1`, gọi đúng endpoint `/sale/*` trả **200**, bảng render đủ cột |
| 6 màn chi tiết / sửa | 6/6 OK (`prospective-projects/146` + `/edit`, `solutions/30`, `bom-list/22`, `quotations/80`, `request-solution/20`) — 0 request nào ≥ 400 |
| Redirect URL cũ | **20/20** đúng, gồm cả `:id` và `:id/edit`, `:id/manager`; 3 màn ở lại Giao việc (`tasks`, `issues`, `settings`) không bị đụng |
| Màn Yêu cầu báo giá | đã render đủ 12 cột sau khi vá lỗi import |

**Sự cố dev server (đã qua)**: rebuild 111 file làm Nuxt treo — RAM ~3.2 GB, `.nuxt/router.js`
dừng ghi, route mới `matched: 0` nhưng server vẫn trả HTTP 200 (vỏ SPA) nên dễ tưởng đã chạy.
Dấu hiệu nhận biết: **mtime của `.nuxt/router.js` đứng im**. Restart xong: 5354 route, hết lỗi.

Lỗi `layouts/default.vue` (`Cannot read properties of undefined (reading '_normalized')` trong
`getSubItems`) chỉ xuất hiện trong lúc server hỏng (route `matched: 0` → rơi về layout mặc định),
**không tái hiện** sau restart. Không phải hồi quy.

Các cảnh báo Vue còn lại (`Invalid prop`, `computed "fields" already defined in data`,
`Property "menu"/"employees"/"receiveDeptOptions" is not defined`, `Missing required prop "project"`)
là **có sẵn**: `git diff -M` các file đó chỉ đổi đường dẫn import + chuỗi endpoint, không đụng logic.

---

## Phase 16 — Màn Tổng quan dùng chung cho phân hệ chuẩn hub — 2026-08-05

Phase 13A mới chuẩn hoá **sidebar**; màn Tổng quan của Danh mục chung + Bảo hiểm vẫn là
`SubsystemDashboardPlaceholder` ("Dashboard của phân hệ sẽ được xây dựng ở giai đoạn sau"),
lệch hẳn với Bán hàng.

### Đã làm

- [x] Tách nội dung `/sale/dashboard` thành component dùng chung
      **`components/subsystem/SubsystemHubOverview.vue`**; bỏ hết chỗ gắn cứng Bán hàng:
      tên, nhóm màu, key localStorage suy từ `resolveSubsystem()`; nhóm chức năng lấy qua
      `hubGroupsFor()`.
- [x] Icon nhận **cả 2 dạng** như bên sidebar — inline SVG (`sale-hub.js`) và class Remix
      (phân hệ suy từ cây menu) qua `isSvgIcon()` + style `.gcard-ic-font`.
- [x] 3 màn dashboard (`sale`, `master-data`, `insurance`) rút còn wrapper ~15 dòng.
      13 phân hệ chưa tới lượt vẫn giữ placeholder.

### Verify

| Phân hệ | Số nhóm | Màu nhận diện | Bấm nhóm mở panel |
|---|---|---|---|
| Danh mục chung | 2 | `#4A5B6E` (Lõi hệ thống) | ✔ 7 màn |
| Bảo hiểm xã hội | 4 | `#2E71C3` (Nhân sự) | ✔ 2 màn |
| Bán hàng | 10 | `#6B54B8` (Kinh doanh) | ✔ 8 màn — không hồi quy |

### Ghi chú

- `components/sale/SaleMenuHub.vue` (333 dòng) là **code chết**, không nơi nào import — không đụng.
- Sau khi `git mv` file page rồi tạo lại file cùng đường dẫn, webpack cache vẫn nhớ trạng thái
  file bị mất → báo `ENOENT: no such file or directory` dù file có thật. `touch` lại file là hết.
- Thêm phân hệ vào chuẩn hub = khai `key` trong `HUB_SUBSYSTEMS` + đổi wrapper dashboard +
  đổi `layout` các page sang `default-sidebar`. Không phải copy màn.

---

## Phase 17 — Đưa CSKH + Tài chính vào chuẩn hub — 2026-08-06

Phase 13A/16 chuẩn hoá sidebar + Tổng quan cho 3 phân hệ (Bán hàng, Danh mục chung, Bảo hiểm).
CSKH và Tài chính vẫn dùng sidebar dọc kiểu cũ + `SubsystemDashboardPlaceholder`.

Vướng: `deriveHubGroups()` suy 1 nhóm rail cho mỗi mục cấp 1, mà `finance.js` có **24 mục cấp 1**
(thứ tự theo dòng sheet `Gộp phân hệ ERP-HRM`) → rail dài gấp 2,5 lần Bán hàng, phải cuộn.

### Đã làm

- [x] **Gom nhóm rail bám cây ERP.** Các màn Tài chính vốn chuyển từ mega-menu `Kế toán` của ERP
      (`TanPhatDev/resources/views/layouts/topmenubar.blade.php` dòng 933-1325) — cấu trúc 3 cấp
      của ERP (`li` → `h3.ruby-list-heading` → `li`) trùng khớp cấu trúc hub, nên lấy nguyên
      thay vì tự nghĩ cách gom. `deriveHubGroups()` thêm hỗ trợ `hubGroup` / `hubIcon`: nhiều mục
      cấp 1 cùng `hubGroup` dồn vào 1 nhóm rail, mỗi mục thành 1 mục cấp 2 trong panel.
      **Vẫn 1 nguồn menu duy nhất** — không sinh file `finance-hub.js` như `sale-hub.js`.
- [x] `finance.js`: sắp lại thứ tự mục cấp 1 theo cây ERP + gắn `hubGroup` → **24 nhóm còn 11**
      (Khởi tạo · Khai báo đầu kỳ · Quản lý tiền · Hàng hoá - Dịch vụ - Vận chuyển · Kiểm kê ·
      Kế toán bán hàng · Kế toán công nợ · Kết chuyển cuối kỳ · Sổ tổng hợp · Danh mục · Chờ duyệt).
      Không mất mục nào: 130 nhãn + 6 `erpPath` khớp hệt bản cũ.
- [x] `customer-care.js` **không sửa** — 4 nhóm sẵn có đã khớp 4 nhóm cấp 2 của ERP > CSKH.
- [x] `HUB_SUBSYSTEMS` += `customer-care`, `finance`; 2 wrapper dashboard đổi sang
      `SubsystemHubOverview` + `layout: 'default-sidebar'` (mọi màn con 2 phân hệ đã dùng layout này).
- [x] **Fix `erpPath` bị nuốt.** `deriveHubGroups()` cũ chỉ chép `label`/`link`/`isShow` → 6 màn
      ERP của Tài chính (Tách - ghép, Kiểm kê) sẽ thành mục chết. Nay chép cả `erpPath`
      (`openScreen()` cả 2 phía đều đã xử lý sẵn).
- [x] **Fix icon rail gắn cứng.** `SaleHubSidebar` hardcode SVG túi mua sắm của Bán hàng nên
      Danh mục chung + Bảo hiểm cũng hiện icon túi. Nay lấy `subsystem.image`
      (`assets/images/icon_*.svg`, đủ cho cả 5 phân hệ hub), rơi về `subsystem.icon` nếu thiếu.
      Dùng file SVG chứ không dùng class `ri-*` để né xung đột 2 bản Remix Icon (local 2.4.0 + CDN 4.3.0).

### Verify

`deriveHubGroups()` chạy thật trên 4 cây menu (node + bản copy `.mjs`):

| Phân hệ | Nhóm rail | Màn | Ghi chú |
|---|---|---|---|
| Tài chính | 11 | 103 | nhóm `Hàng hoá - Dịch vụ - Vận chuyển` 10 mục → tự vào nav-mode |
| CSKH | 4 | 17 | — |
| Danh mục chung | 2 | 15 | **không hồi quy** (giữ nguyên như Phase 16) |
| Bảo hiểm | 4 | 7 | **không hồi quy** |

- `vue-template-compiler` parse 4 file `.vue` đã sửa: 0 lỗi.
- 5 route `/…/dashboard` trên dev server (cổng 3000) trả 200.
- 26 class `ri-*` của 2 cây menu + 5 icon phân hệ: đều có trong `_remixicon.scss` (bản local 2.4.0).
- ⚠️ **Chưa verify bằng mắt trên trình duyệt** — profile Chrome của Playwright đang bị phiên khác
  giữ. Cần user mở `/finance/dashboard` + `/customer-care/dashboard` xem rail và lưới nhóm.

### Ghi chú

- 2 chỗ cố ý lệch ERP: nhóm `Quản lý giá - CTKM` của ERP không kéo về (sheet gộp xếp các màn đó
  sang phân hệ khác); `Chức năng chính > Hoạt động kế toán` không có trong mega-menu Kế toán ERP
  nên xếp tạm vào nhóm rail `Sổ tổng hợp`.
- Đổi thứ tự mục cấp 1 của `finance.js` **không ảnh hưởng sidebar dọc cũ** vì phân hệ đã vào
  `HUB_SUBSYSTEMS` → `default-sidebar` render `SaleHubSidebar` chứ không render `Sidebar.vue`.
- `hubGroup` là tuỳ chọn: phân hệ không khai (CSKH, Danh mục chung, Bảo hiểm) giữ nguyên hành vi cũ.

---

## Phase 18 — Trải chuẩn hub ra toàn bộ phân hệ mới — 2026-08-06

Sau Phase 17 còn **12 phân hệ** dùng `layout: 'subsystem'` (menu dọc kiểu UBold +
`SubsystemDashboardPlaceholder`). Mỗi phân hệ chỉ có đúng 1 file page là màn dashboard —
toàn bộ chức năng còn bên ERP.

### Đã làm

- [x] Chuyển **9 phân hệ** sang chuẩn hub: `admin`, `asset`, `iso`, `kpi`, `legal`,
      `operation`, `production`, `recruitment`, `tax`. Mỗi phân hệ = thêm `key` vào
      `HUB_SUBSYSTEMS` + wrapper dashboard đổi sang `SubsystemHubOverview` +
      `layout: 'default-sidebar'`. **Không đụng file menu nào** — cả 9 menu đều 2 cấp,
      `deriveHubGroups()` suy thẳng.
- [x] Ghi chú lý do loại 3 phân hệ còn lại ngay trong `hub.js`.

### Không chuyển — 3 phân hệ

`purchase`, `warehouse`, `transport` dùng `dashboardOnlyMenu()` (chỉ có mục Tổng quan → **0 nhóm**)
nên rail và lưới Tổng quan sẽ rỗng, xấu hơn placeholder hiện tại. Cả 3 đều `hidden: true` +
`erpGhost: true` — quy hoạch ở lại ERP. Có menu thật thì thêm `key` là xong.

### Verify

`deriveHubGroups()` chạy thật trên cả 14 key trong `HUB_SUBSYSTEMS` (không trùng key):

| Phân hệ | Nhóm | Màn | Nhóm rail |
|---|---|---|---|
| admin | 5 | 15 | Cấu hình ERP · Mẫu in · Hướng dẫn sử dụng · Log hệ thống · API Key |
| production | 2 | 7 | Khởi tạo phiếu yêu cầu · Chức năng chính |
| legal | 1 | 9 | Chức năng chính |
| iso | 1 | 6 | Chức năng chính |
| recruitment | 1 | 6 | Chức năng chính |
| kpi | 1 | 5 | Chức năng chính |
| tax | 1 | 5 | Chức năng chính |
| asset | 1 | 4 | Chức năng chính |
| operation | 1 | 2 | Chức năng chính |

5 phân hệ của Phase 16/17 giữ nguyên số liệu — **không hồi quy**.

- `vue-template-compiler` parse 11 file dashboard: 0 lỗi.
- 17 route `/…/dashboard` trả 200 (kể cả 3 phân hệ không chuyển).
- Icon nhóm của 9 menu đều có trong `_remixicon.scss` (bản local 2.4.0); 9 file
  `assets/images/icon_*.svg` cho brand icon rail đều tồn tại.
- `git status`: đúng 10 file đổi, không dính file lạ do EOL.
- ⚠️ **Chưa verify bằng mắt** — Playwright vẫn bị phiên khác giữ profile Chrome.

### Ghi chú — lỗi có sẵn phát hiện, CHƯA sửa

`isShow` (mảng tên quyền) của mục cấp 2 được `deriveHubGroups()` chép vào nhưng
**`SaleHubSidebar.rowsHtml()` và `SubsystemHubOverview` không hề lọc theo nó** → sidebar hub
hiện đủ mọi màn bất kể quyền, khác `Sidebar.vue` cũ (`isShowSubItemMenu()` có gate).
Đây là lỗi có từ Phase 13A, đang ảnh hưởng cả 5 phân hệ đã chuyển code — cần user quyết
có gate lại không (mới chỉ là ẩn/hiện mục menu, BE vẫn chặn bằng `checkPermission`).

---

## Phase 19 — Sidebar hub lọc theo quyền — 2026-08-06

Lỗi ghi ở cuối Phase 18: `deriveHubGroups()` chép `isShow` vào nhóm hub nhưng
`SaleHubSidebar.rowsHtml()` và `SubsystemHubOverview` không lọc theo nó → **hiện đủ mọi màn
bất kể quyền**, khác `Sidebar.vue` dọc vốn có gate. Lỗi từ Phase 13A.

### Đã làm

- [x] `hub.js` thêm `isScreenVisible(screen, permissions)` + `filterHubGroups(groups, permissions)`;
      `hubGroupsFor(subsystem, permissions)` nhận thêm tham số — **bỏ trống thì không lọc**
      (giữ tương thích cho test / chỗ chỉ đếm menu).
      Ngữ nghĩa khớp `hasMultiplePermission()` của `utils/mixins/CheckPermission.js`: khai mảng →
      khớp 1 trong số đó là hiện; không khai → hiện. Lọc xong bỏ luôn mục cấp 2 / nhóm rỗng để
      rail và lưới Tổng quan không còn nhóm bấm vào trống trơn.
- [x] `SaleHubSidebar` + `SubsystemHubOverview` truyền `$store.state.permissions` vào —
      dùng chung 1 nguồn nên số nhóm và số "chức năng" trên thẻ luôn khớp rail.
- [x] **Bịt nốt lỗ Bán hàng.** Đo lại thấy `sale-hub.js` có 29 màn link mà **0 màn khai `isShow`**
      → fix cơ chế xong vẫn hiện full. Nguyên nhân: map gate `SALE_LINK_PERMISSIONS` (14 link)
      nằm ở `sale.js`, chỉ tree dọc dùng. Đã **chuyển map sang `sale-hub.js`** + hàm
      `withPermissions()` gắn `isShow` vào màn lúc export; `sale.js` import lại đúng map đó.
      1 nguồn cho cả 2 bề mặt, **không nhân bản map**.

### Xác minh trước khi gate Bán hàng

Không tự nghĩ tên quyền — đối chiếu `Modules/Sale/Routes/api.php`: cả 11 route danh mục/thiết lập
đều gate ngay ở `GET /` nên mục menu đó vốn đã chết với người không quyền (403).

⚠️ 2 quyền **cố ý không đưa vào menu**: `Tiếp nhận yêu cầu làm giải pháp` chỉ gate
`PUT /{id}/receive`, `Quản lý giải pháp` chỉ gate `PUT /{id}/close` — gate cả màn là ẩn nhầm.
⚠️ Tên FE lệch tên BE 2 chỗ (đã kiểm bằng endpoint thật trong page, không đoán theo tên):
`/sale/solution-groups` (Nhóm giải pháp) → BE `/sale/industries`;
`/sale/industry-groups` (Nhóm ngành) → BE `/sale/scopes`.

### Verify

| Kịch bản | Kết quả |
|---|---|
| Tree sidebar dọc Bán hàng trước/sau | `JSON.stringify` **giống hệt** — không hồi quy |
| Bán hàng, quyền rỗng | 205 → 191 màn; mục `Danh mục › Dự án - Giải pháp` + `Danh mục chung` biến mất, `Quy chế - Thiết lập` giữ lại `Quy chế bán hàng` (không gate) |
| Bảo hiểm, quyền rỗng | 4 nhóm/7 màn → 2 nhóm/2 màn |
| Bảo hiểm, có `Duyệt phiếu đăng ký bảo hiểm` | 3 nhóm/3 màn |
| Tài chính, quyền rỗng | 11 nhóm/103 màn → 10 nhóm/96 màn (mất nhóm `Danh mục`) |
| Tài chính, có `Quản lý danh mục tiền tệ` | 11 nhóm/97 màn |

Độ phủ gate sau khi sửa (màn có link / trong đó gate quyền): sale 29/14, finance 7/7,
insurance 7/5, customer-care 5/4, master-data 10/2. 9 phân hệ Phase 18 chưa có màn nào có link.

- `vue-template-compiler` 2 file `.vue`: 0 lỗi. Route dashboard 6 phân hệ: 200.
- 14 phân hệ derive giữ nguyên số nhóm/màn khi không lọc — **không hồi quy**.
- ⚠️ Vẫn chưa verify bằng mắt (Playwright bị phiên khác giữ profile Chrome).

### Còn nợ

`master-data` mới gate 2/10 màn: 7 màn địa lý-ngân hàng **chưa có permission nào trong DB**
(đã ghi ở phần "Còn nợ" của Phase 13A) nên không có gì để gate; 1 màn Khách hàng dùng quyền ERP.

### Verify trình duyệt (Playwright) — 2026-08-06, gỡ nợ của Phase 17/18/19

Tài khoản DNS Admin (573 quyền), dev server cổng 3000. **0 console error** ở mọi màn.

- [x] **Tài chính** `/finance/dashboard`: rail 11 nhóm, lưới 11 thẻ, icon phân hệ ra **icon tiền**
      (không còn túi mua sắm). Nhóm `Hàng hoá - Dịch vụ - Vận chuyển` vào **nav-mode** đúng như
      panel `Báo cáo` của Bán hàng — 10 mục cấp 2 cột trái, nội dung cột phải, 48 chức năng
      nhìn không hề quá tải (bỏ lo ngại ghi ở phần Rủi ro của spec).
- [x] **Lọc quyền chạy thật**: thẻ `Danh mục` hiện **6 chức năng** trong khi menu khai 7.
      Đọc `$store.state.permissions` → thiếu đúng **1 quyền** `Quản lý danh mục tài khoản ngân hàng`,
      và đúng mục đó biến mất. Gọi API xác nhận gate hợp lý:
      `sale/bom-price-approval-configs` → **403**, `sale/discount_types` + `sale/scopes` → **200**.
- [x] **Bán hàng**: đối chiếu 14 link trong `SALE_LINK_PERMISSIONS` với quyền thật —
      **14/14 khớp, 0 sai**. Thiếu `Cấu hình duyệt giá BOM giải pháp` → nhóm `Quy chế - Thiết lập`
      từ 2 xuống **1 chức năng**, tổng 205 → **204 màn**.
- [x] **`erpPath` sống nguyên**: `allScreens` của Tài chính còn đủ 6 màn ERP
      (2 Tách - ghép + 4 Kiểm kê).
- [x] Điều hướng thật: tìm "tiền tệ" → bấm kết quả → `/finance/currencies` mở đúng, **rail giữ
      nguyên ở màn con** (đồng nhất Tổng quan ↔ màn con). Ô tìm kiếm trả breadcrumb đúng
      (`Hàng hoá - Dịch vụ - Vận chuyển › Tách - ghép`).
- [x] **12 phân hệ hub còn lại** render đủ, rail = lưới, tên + icon SVG riêng đúng từng phân hệ:
      CSKH 4 nhóm · admin 5 · production 2 · master-data 2 · insurance 4 · legal 1 · iso 1 ·
      recruitment 1 · kpi 1 · tax 1 · asset 1 · operation 1.
      Bảo hiểm và Danh mục chung nay hiện icon riêng (khiên / thư mục) thay vì túi mua sắm.
