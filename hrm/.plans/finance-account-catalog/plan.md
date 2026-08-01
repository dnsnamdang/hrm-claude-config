# Plan — finance-account-catalog

> Tóm tắt: `.plans/finance-account-catalog/design.md`
> Spec: `docs/superpowers/specs/2026-07-30-finance-account-catalog-design.md`

## Phase 0 — Khảo sát (DONE)

- [x] Đọc `AccountController` + `TypeAccountsController` + Model `Account` / `TypeAccount` bên ERP
- [x] Đọc 2 blade index + form + history, xác định cột bảng / bộ lọc / field form
- [x] Xác định `ListAccountRoot`, `ListTypeAccount`, `AccountImport`, `TypeAccountImport`, template In id 459
- [x] Soi `gop_db`: schema + số dòng `accounts` / `type_accounts` / version / history / `account_details`
- [x] Xác định quy ước DB gộp: bảng trùng tên ưu tiên ERP, HRM prefix `hrm_*` (24 bảng)
- [x] Xác định `Modules/Finance` + `pages/finance` đang rỗng, phân hệ `finance` đã có trong `subsystems.js`
- [x] Chốt 4 quyết định với user (quyền / created_by / phạm vi / loại tài khoản)

## Phase 1 — BE: Danh mục loại tài khoản (`type-accounts`)

- [x] **Checkout branch `gop_db` cả 2 repo** — nền tảng gộp phân hệ (`Modules/Finance`, `components/subsystems.js`, `pages/finance`) chỉ có ở branch này; trước đó cả 2 repo đứng ở `tpe` nên không có gì
- [x] `Modules/Finance/Entities/TypeAccount/TypeAccount.php` — table `type_accounts`, connection default, `$fillable` = code/name/note/status/created_by/updated_by, const `STATUS_ACTIVE=1` / `STATUS_INACTIVE=2`
- [x] **KHÔNG kế thừa `App\Models\BaseModel`** — BaseModel có hook `creating`/`saving` tự ghi đè `created_by`/`updated_by` = `Auth::user()->id` (HRM user id), sẽ phá quyết định #2. Kế thừa `Model` thuần, tự gán trong Service
- [x] `Modules/Finance/Entities/ErpEmployee.php` — model mới, table `employees` (ERP) trên connection **mặc định**; khác `TpEmployee`/`TpEmployee2` (đọc qua `mysql2` = DB ERP cũ)
- [x] Relation `createdByEmployee` / `updatedByEmployee` trỏ **ERP `employees`** + accessor `created_by_name` / `updated_by_name` (join `employee_infos` lấy `code - fullname`)
- [x] `isCanDelete()` — chặn khi tồn tại `accounts.type = id` (giữ logic ERP); `isCanLock()` / `isCanUnlock()`
- [x] `Entities/TypeAccount/TypeAccountVersion.php` + `TypeAccountHistory.php` + `createHistory()`
- [x] `Services/FinanceService.php` — base service, `requireErpEmployeeId()`
- [x] `Services/TypeAccountService.php` — index (filter keyword/code/name/status/created_by/updated_by/updated_from/updated_to + sort), getAll, store, update (ghi version + diff), destroy, histories
- [x] ⚠️ **`created_by/updated_by` KHÔNG dùng `ErpPermissionHelper::erpEmployeeId()`** — helper đó đọc `mysql2` → `DB_DATABASE_SECOND` (DB ERP CŨ) nên trả id không tồn tại trong DB gộp. Tự query `employees` trên connection mặc định. Null → 400
- [x] `Http/Requests/TypeAccount/TypeAccountRequest.php` — code required + unique (ignore chính nó), name required, chuẩn hóa uppercase/trim ở `prepareForValidation`
- [x] `Transformers/TypeAccountResource/TypeAccountResource.php` (bỏ `DetailTypeAccountResource` — entity đơn giản, dùng chung 1 resource cho cả list và show)
- [x] `app/ExcelExport/TypeAccountExport.php` + `resources/views/exports/type_accounts.blade.php` (9 cột)
- [x] Import Excel: `validateImportData()` + `import()` + 2 route `POST /import/validate`, `POST /import` (theo skill `import-excel`, không dùng `$request->validate()`)
- [x] `Http/Controllers/V1/TypeAccountController.php` (mỏng, gọi Service) — theo convention của skeleton phân hệ mới (`Http/Controllers/V1`, không phải `Http/Controllers/Api/V1` như Assign)
- [x] `Modules/Finance/Routes/api.php` — prefix `/v1/finance/type-accounts` + `auth:api`: `GET /`, `GET /getAll`, `GET /export`, `POST /`, `PUT /{id}`, `DELETE /{id}`, `GET /{id}/lock`, `GET /{id}/unlock`, `GET /{id}/histories`, `GET /{id}`
- [x] Verify: `php -l` 12 file sạch; 10 route nạp đúng; script tinker 9 nhóm test PASS (create chuẩn hóa code/trim, update sinh đúng 1 version + 2 dòng history, update không đổi gì → 0 version, lịch sử trả đúng nhãn cột + tên người sửa, isCanDelete/isCanLock đúng cả 2 chiều, chặn khóa khi đang dùng, 6 bộ lọc, payload Resource, delete dọn sạch version+history); blade export render 7 dòng OK; đã xóa file test tạm; DB trả về đúng trạng thái đầu (7 / 0 / 0)

> ⚠️ `php artisan route:list` **crash sẵn** trong repo (không do feature này): `RequestUpdateTimeSheetController:51`
> gọi `isCurrentEmployeeHasPermission()` trong constructor khi chưa có auth. Dùng
> `php artisan tinker --execute="collect(Route::getRoutes())..."` để liệt kê route thay thế.

## Phase 2 — BE: Danh mục tài khoản (`accounts`)

- [x] `Entities/Account/Account.php` — `$fillable` **KHÔNG có `note`** (cột không tồn tại); const `TYPES` (7 loại, giữ như ERP) + `STATUSES` + `LEVELS`; kế thừa `Model` thuần
- [x] `buildRoot()` — port nguyên `getRootOrder()` (`substr(0,3)` + `.` + `substr(3,5)` → float). Verify: 999 → `999`, 9991 → `999.1`
- [x] `isCanLock/isCanUnlock/isCanDelete` — port theo ERP, so `created_by` với ERP employee id; `isCanDelete` check `accounts.identify_number_parent` + `account_details.account_id` (bảng 965k dòng, đã xác nhận có index `account_details_account_id_index`)
- [x] `Entities/Account/AccountVersion.php` + `AccountHistory.php` + `createHistory()` (map `type` → `TYPES[...]`, `is_account_follow_dept` → Có/Không, `status` → nhãn)
- [x] `Services/AccountService.php` — index (keyword, identify_number **prefix**, name **`%name%`** đã fix lỗi ERP, level, type, is_account_follow_dept dùng `strlen` để nhận giá trị 0, status, created_by, updated_by, updated_from/to; sort mặc định `root` rồi `identify_number`), getAll, store, update (version + diff), destroy, histories, `buildPrintTable()`, `companyHeader()`
- [x] `Http/Requests/Account/AccountRequest.php` — port `AccountStoreRequest`; sửa 2 chỗ của ERP: `is_account_follow_dept` đổi `required` → `nullable|boolean` (checkbox false sẽ trượt `required`), `identify_number_parent` chỉ bắt buộc + `exists` khi `level != 1`
- [x] `Transformers/AccountResource/AccountResource.php` — `level_1/2/3` theo `level`, `type_name`, `status_name`, cờ `is_can_edit/lock/unlock/delete`. **Cờ quyền tốn 2 query/dòng nên chỉ tính khi controller bật `with_permission_flags`** (export/print không bật → tránh N+1 trên 308 dòng)
- [x] `app/ExcelExport/AccountExport.php` + `resources/views/exports/accounts.blade.php` (12 cột, cấp 1 in đậm, `columnWidths` port từ `ListAccountRoot`)
- [x] Import Excel: port `AccountImport` (6 cột; validate tài khoản mẹ tồn tại / loại TK theo code-or-name / trùng `identify_number`). **Nới hơn ERP 1 điểm**: tài khoản mẹ được phép nằm ngay trong file import (ERP chỉ tra DB) và `import()` sắp xếp theo bậc 1→2→3 nên import cả cây trong một file vẫn chạy
- [x] Endpoint **In danh sách** — `Entities/ErpReportTemplate.php` (bảng `report_templates` ERP trên connection mặc định) id **459** + `fillReport()` (đã có sẵn ở `app/Helper/FormatHelper.php`). Template dùng 3 placeholder `{{HEADER}}` `{{CHI_TIET}}` `{{NGUOI_LAP}}`; `HEADER` lấy `companies.header` theo `employee_infos.company_id`
- [x] `Http/Controllers/V1/AccountController.php` + route prefix `/v1/finance/accounts` — 12 route, có thêm `GET /types` (loại TK cho **bộ lọc**, lấy từ hằng `TYPES`) và `GET /print` so với type-accounts
- [x] Verify: `php -l` 11 file sạch; 12 route nạp đúng; **21 case HTTP thật PASS** — 4 case validate (rỗng / cấp 2 thiếu TK mẹ / TK mẹ không tồn tại / trùng số TK), create cấp 1 (trim, bỏ `identify_number_parent` khi cấp 1, `root`=999, `created_by`=13 ERP), create cấp 2 (`root`=999.1), chặn xóa tài khoản cha khi còn con, update sinh đúng 3 dòng history với nhãn tiếng Việt, update không đổi gì → 0 version, lock/lock lại/unlock, chặn lock bản ghi người khác tạo, 8 bộ lọc, export xlsx 80KB, print fill đúng template 459 (không sót placeholder, có letterhead + dữ liệu), cờ quyền đúng cho cả bản ghi của mình và của người khác, xóa con rồi xóa cha thành công. DB trả về nguyên trạng (308 / 0 / 0)

## Phase 3 — Quyền HRM

- [x] Thêm 4 quyền **trực tiếp vào `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`** (rule project: KHÔNG tạo migration riêng cho permission): id 1107-1110, `group = 'Danh mục'`, **`type = 8`** (phân hệ Tài chính — type mới)
- [x] Gắn `middleware('checkPermission:...')` lên route type-accounts: `index/show/histories/export` = Quản lý|Xem; `store/update/delete/lock/unlock` = chỉ Quản lý; `getAll` để mở (dropdown)
- [x] Thêm khối accordion thứ 8 "Phân hệ tài chính" (`filterPermission(8)`) vào `components/setting/Permission.vue` — **user duyệt 2026-07-31**. Thuần bổ sung, không sửa 7 khối cũ. Không có nó thì quyền `type = 8` không hiện trên màn phân quyền → không ai cấp được
- [x] Insert 4 quyền vào `hrm_permissions` DB local + cấp cho vai trò `Super admin` (id 18) đủ 5 company_id. **Không chạy seeder** vì `PermissionsTableSeeder::run()` `truncate` cả bảng `hrm_permissions` → mất toàn bộ phân quyền local
- [x] Verify HTTP thật (php -S + JWT): 12 case PASS — 401 khi không token; 422 validate rỗng + trùng mã; 201 create (`created_by` = 13 ERP, `created_by_name` = "DNS01 - DNS Admin"); 200 update + histories đúng diff; lock/unlock 200; lock+delete loại đang dùng → 400; getAll; export trả file xlsx 80KB đúng content-type; delete 200
- [x] Verify 403: user có vai trò nhưng thiếu quyền Tài chính → 403 cả `index` lẫn `store`
- [x] **Verify browser (Playwright MCP)**: bật `php -S :8000` + `npm run dev :3000`, vào `/human/roles/add/52`
      → khối accordion thứ 8 "Phân hệ tài chính" hiện đúng, mở ra thấy nhóm "Danh mục tài chính"
      với đủ 4 checkbox quyền; tick checkbox binding chạy. Đối chiếu cả 8 khối: type 1-7 giữ nguyên
      số nhóm và tên nhóm cũ (type 4 vẫn còn nhóm "Danh mục" của Giao việc). Không bấm Lưu để
      không đổi vai trò thật. Đã tắt 2 server, xóa screenshot + `.playwright-mcp/`
- [x] 🐛 **Fix phát sinh — `group` KHÔNG được đặt là 'Danh mục'**: `Permission.vue::initListPermissions()`
      gom nhóm **CHỈ theo `group`**, không theo `(group, type)`. Lần đầu để `group = 'Danh mục'` (trùng
      phân hệ Giao việc type 4) → 4 quyền bị gộp vào tab Giao việc, tab Tài chính rỗng dù API trả
      đủ 4 dòng `type = 8`. Đã đổi thành **`'Danh mục tài chính'`** (seeder + DB local) thay vì sửa
      hàm dùng chung. Đối chiếu payload: trước fix có đúng 1 group nằm ở 2 type ('Danh mục' → [4, 8]),
      sau fix 0 group nào bị trùng type

### Bổ sung 2026-08-01 — sắp xếp màn Phân quyền theo thứ tự phân hệ

Yêu cầu user: "phân hệ tài chính theo thứ tự thì nằm tít bên dưới, nhưng màn permission đang là số 8;
làm sẵn các phân hệ mới, đi theo thứ tự từ trên xuống".

- [x] Khai `permissionType` + `permissionLabel` cho **cả 24 phân hệ** trong `components/subsystems.js`
      (registry là nguồn khai báo duy nhất). Type 1-8 giữ nguyên số vì DB đã có dữ liệu
      (`hrm_permissions` 1→78 quyền, 2→57, 3→79, 4→167, 5→112, 6→78, 7→17, 8→4); 16 phân hệ mới cấp 9-24
- [x] Thêm `getPermissionSubsystemGroups()` — gom khối quyền theo nhóm sơ đồ v1.6, giữ nguyên thứ tự
      mảng `SUBSYSTEMS`. **Số `type` không còn quyết định vị trí hiển thị** → Tài chính vẫn `type = 8`
      nhưng nằm cuối màn (nhóm "4. KINH DOANH - TÀI CHÍNH")
- [x] Viết lại `components/setting/Permission.vue` từ 8 khối accordion copy tay (~500 dòng) thành 1
      `v-for` data-driven (~170 dòng). Markup bên trong giữ y nguyên; `accordion-<type>` giữ nguyên id.
      Thêm: tiêu đề nhóm sơ đồ, icon phân hệ, badge số quyền, trạng thái rỗng
      "Phân hệ này chưa khai báo quyền nào". Bỏ `console.log` trong `filterPermission()`
- [x] Ghi bảng ánh xạ 24 type vào comment `PermissionsTableSeeder.php` + trỏ về `subsystems.js`
- [x] 🐛 **4 icon phân hệ không có trong font Remix Icon local** (v2.4.0) nên đang render sai glyph ở cả
      màn chọn phân hệ: `ri-shield-check-line`→`ri-shield-user-line`, `ri-verified-badge-line`→`ri-award-line`,
      `ri-flow-chart`→`ri-git-merge-line`, `ri-graduation-cap-line`→`ri-book-read-line`.
      Đã rà đủ 24 icon với `_remixicon.scss`, còn lại hợp lệ
- [x] Verify: chạy `getPermissionSubsystemGroups()` bằng node → đúng 24 khối, đúng thứ tự, không trùng
      type; `vue-template-compiler` compile `Permission.vue` → 0 error/0 tip; Nuxt build không phát sinh
      warning mới ở file này
- [ ] ⏳ **Chưa verify bằng mắt trên browser** — phiên Playwright đã mất đăng nhập, không tự tạo token
      được (bị chặn). Cần user mở `/human/roles/add/{id}` xem lại thứ tự + khối rỗng

## Phase 4 — FE: menu phân hệ Tài chính

> **Style FE toàn bộ dùng bộ V2Base** (user chốt 2026-07-30) — dựng giao diện mới theo chuẩn HRM,
> KHÔNG port markup/DATATABLE/AngularJS của ERP. Chi tiết bảng component + skill: spec §4.6.
> Select **trong modal** bắt buộc `V2BaseSelectInModal`, không dùng `V2BaseSelect`.
> Đọc trước khi code: `list-page`, `modal-popup`, `button-convention`, `entity-history`,
> `import-excel`, `print-page` (trong `.claude/skills/`).


- [x] `hrm-client/components/subsystem-menu/finance.js` — `financeItems`: mục "Tổng quan" + nhóm **"Danh mục"** (icon `ri-list-check-2`) chứa `Danh mục tài khoản` + `Danh mục loại tài khoản`, mỗi mục gate `isShow: [...]`
- [x] `components/subsystems.js` — đổi `menu: dashboardOnlyMenu('finance')` → `menu: financeItems` + import
- [x] Icon dùng lại class đã có trong project (`ri-list-check-2`, `ri-dashboard-line`) — không thêm class `ri-*` mới
- [x] Verify: mở `/finance/accounts` + `/finance/type-accounts` chạy đúng layout `default-sidebar`

## Phase 5 — FE: màn Danh mục loại tài khoản

- [x] `pages/finance/type-accounts/index.vue` — V2BaseFilterPanel (keyword + code/name/status/created_by/updated_by/updated_from/updated_to) + V2BaseDataTable 7 cột (gộp Người tạo/Ngày lập vào cột Tên và Người cập nhật/Ngày cập nhật vào cột Cập nhật bằng `V2BaseTitleSubInfo`, theo cách trình bày của các màn danh mục HRM hiện có)
- [x] `components/modal/finance/type-account-modal.vue` — 4 field code/name/note/status, `V2BaseSelectInModal` cho select, validate inline + cờ `touched`
- [x] `components/modal/finance/finance-history-modal.vue` — modal lịch sử **dùng chung cho cả 2 màn**: bộ lọc client-side (trường/người/từ-đến ngày), cũ ĐỎ → mới XANH, footer chỉ nút Đóng tertiary
- [x] Nút Xuất Excel + Import Excel + Lịch sử; `utils/download-excel.js` (helper dùng chung, tự gắn `Authorization`) + `utils/mixins/FinanceImportMixin.js` (luồng import dùng chung)
- [x] Ẩn nút theo quyền (`canManage`)
- [x] Verify browser: màn render đúng, dữ liệu 7 dòng, nút/cờ quyền đúng

## Phase 6 — FE: màn Danh mục tài khoản

- [x] `pages/finance/accounts/index.vue` — 8 bộ lọc + bảng 10 cột (Cấp 1/2/3 tách cột theo `level`, cấp 1 in đậm, sort theo cây)
- [x] `pages/finance/accounts/components/AccountFormComponent.vue` + `add.vue` + `_id/edit.vue` — 6 field: Số TK, Bậc, Tài khoản mẹ (dropdown lọc theo bậc cha, disable khi cấp 1), Tên TK, Loại TK (dropdown từ `type_accounts`), Trạng thái, checkbox Theo dõi công nợ. **KHÔNG có field Ghi chú**. Tự suy bậc theo độ dài số TK khi thêm mới
- [x] `pages/finance/accounts/print.vue` — `v-html` HTML do BE fill sẵn từ template 459, `id="content"` + `$printContent({styles, pageMargin})`
- [x] Nút Xuất Excel + In danh sách + Import Excel + Lịch sử
- [x] Nút Khóa/Mở khóa/Xóa hiện theo cờ `is_can_*` từ Resource
- [x] Verify browser: thêm (id 311, `root`=988, người tạo đúng) → sửa (sinh 1 version, 2 dòng history) → modal lịch sử hiện đỏ/xanh → In fill đúng template 459

## Phase 7 — Đối chiếu 2 cổng

- [ ] Tạo 1 tài khoản + 1 loại TK từ HRM → mở màn ERP kiểm tra hiện **đúng tên người tạo** (xác nhận quyết định `created_by` = ERP `employees.id`)
- [ ] Sửa từ HRM → ERP xem lịch sử thấy diff; sửa từ ERP → HRM xem lịch sử thấy diff
- [ ] Xóa/khóa từ HRM → ERP phản ánh đúng

## Checkpoint — 2026-07-30

**Vừa hoàn thành:** Phase 0 khảo sát đầy đủ 2 phía. Chốt 7 quyết định với user. Viết đủ 3 tài liệu.

**Bước tiếp theo:** Phase 1 — BE `type-accounts`.

**Blocked:** không.

## Checkpoint — 2026-07-31

**Vừa hoàn thành:** Phase 1 (BE `type-accounts`) + Phase 3 phần seeder/middleware. 11 file mới,
2 file sửa. Toàn bộ verify PASS (xem chi tiết ở Phase 1). Đã dọn file test tạm, DB trả về nguyên trạng.

Files mới: `Modules/Finance/Entities/ErpEmployee.php`, `Entities/TypeAccount/{TypeAccount,TypeAccountVersion,TypeAccountHistory}.php`,
`Services/{FinanceService,TypeAccountService}.php`, `Http/Requests/TypeAccount/TypeAccountRequest.php`,
`Transformers/TypeAccountResource/TypeAccountResource.php`, `Http/Controllers/V1/TypeAccountController.php`,
`app/ExcelExport/TypeAccountExport.php`, `resources/views/exports/type_accounts.blade.php`.
Files sửa: `Modules/Finance/Routes/api.php`, `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.

**3 phát hiện quan trọng trong lúc code:**

1. **Branch**: nền tảng gộp phân hệ chỉ có ở branch `gop_db`; cả 2 repo đang đứng ở `tpe`.
   Đã checkout `gop_db` (user duyệt), working tree lúc đó sạch nên không mất gì.
2. **`App\Models\BaseModel` không dùng được cho bảng ERP**: hook `creating`/`saving` ghi đè
   `created_by`/`updated_by` = `Auth::user()->id` (HRM user id) → phá quyết định #2. Phải kế thừa
   `Model` thuần và tự gán ERP employee id trong Service.
3. **`ErpPermissionHelper::erpEmployeeId()` trả sai id trên DB gộp**: helper đọc qua `mysql2`
   → `DB_DATABASE_SECOND = erp_dev_24_09` (DB ERP CŨ). Với `employee_info_id = 6`, DB cũ có **8 dòng**
   `employees` (413/654/750/793/796/797/798/799) và helper lấy bừa dòng đầu = **413**; trong `gop_db`
   người đó chỉ có **1 dòng id = 13**. Ghi 413 vào `type_accounts.created_by` làm tên người tạo rỗng.
   Đã tự query `employees` trên connection mặc định trong `FinanceService::requireErpEmployeeId()`.
   ⚠️ Suy ra **màn Khách hàng (`Modules/Assign`) đã port trước đây cũng đang lệch id trên DB gộp** —
   ngoài phạm vi feature này, chưa sửa, cần báo team.

**Phase 3 cũng xong**: user duyệt thêm khối accordion thứ 8 "Phân hệ tài chính" vào
`components/setting/Permission.vue`; đã insert 4 quyền + cấp cho vai trò Super admin ở DB local.
Verify HTTP thật 12 case PASS + 403 đúng cho user thiếu quyền. Đã tắt server test, xóa file tạm,
DB sạch (7 / 0 / 0, không còn bản ghi ZZ*).

⚠️ **KHÔNG chạy `PermissionsTableSeeder`** trên DB có dữ liệu: `run()` `truncate` cả bảng
`hrm_permissions` → mất toàn bộ phân quyền. Insert tay 4 dòng khi cần.

**Verify browser (Playwright MCP) PASS** + phát hiện thêm 1 bug: `Permission.vue::initListPermissions()`
gom nhóm **chỉ theo `group`**, không theo `(group, type)`. Đặt `group = 'Danh mục'` (trùng phân hệ
Giao việc type 4) làm 4 quyền Tài chính bị gộp sang tab Giao việc, tab Tài chính rỗng dù API trả đủ.
Đã đổi `group` → **`'Danh mục tài chính'`** thay vì sửa hàm dùng chung. Đây là bẫy cho MỌI phân hệ
mới sau này: **tên `group` phải là duy nhất toàn hệ thống, không được trùng giữa 2 `type`.**

**Đang làm dở:** không.

**Blocked:** không.

**Bước tiếp theo:** Phase 2 — BE `accounts` (Danh mục tài khoản).

## Checkpoint — 2026-07-31 (2)

**Vừa hoàn thành:** Phase 2 — BE `accounts`. 8 file mới + 1 file sửa (`Routes/api.php`),
`FinanceService` thêm `erpEmployeeId()` (bản không ném lỗi, cho luồng chỉ đọc).
12 route nạp đúng. **21 case HTTP thật PASS**, DB trả về nguyên trạng (308 / 0 / 0).

Files mới: `Entities/Account/{Account,AccountVersion,AccountHistory}.php`,
`Entities/ErpReportTemplate.php`, `Services/AccountService.php`,
`Http/Requests/Account/AccountRequest.php`,
`Transformers/AccountResource/AccountResource.php`,
`Http/Controllers/V1/AccountController.php`, `app/ExcelExport/AccountExport.php`,
`resources/views/exports/accounts.blade.php`.

**3 chỗ chủ động lệch khỏi ERP (đều là sửa lỗi, đã ghi rõ comment trong code):**

1. Bộ lọc `name`: ERP `like "%$name"` (thiếu `%` cuối, chỉ khớp hậu tố) → HRM `%name%`.
2. `is_account_follow_dept`: ERP để `required` nhưng đây là checkbox — giá trị `false`/`0`
   sẽ trượt validate → HRM đổi `nullable|boolean`.
3. `identify_number_parent`: ERP luôn ghi giá trị người dùng gửi; HRM ép `null` khi `level = 1`
   và chỉ bắt buộc + `exists` khi `level != 1`.

**Tối ưu thêm so với ERP:** cờ `is_can_*` tốn 2 query/dòng nên Resource chỉ tính khi controller
bật `with_permission_flags` — export/print (308 dòng) không bật, tránh 616 query thừa.

**Đang làm dở:** không.

**Blocked:** không.

**Bước tiếp theo:** Phase 4 — FE menu phân hệ Tài chính (`components/subsystem-menu/finance.js`),
rồi Phase 5 (màn Loại tài khoản) và Phase 6 (màn Tài khoản).

## Phase 8 — Sửa bug phân trang + trau chuốt UI form (2026-07-31)

- [x] 🐛 **Phân trang loop + nhảy về trang 1** — 3 nguyên nhân chồng nhau:
  1. `page` / `per_page` để trong `filters` → deep watcher coi đổi trang là đổi bộ lọc → reset trang 1 → gọi lại → loop. Đã tách hẳn ra `pagination`, ghép lại khi gọi API qua `buildParams()`.
  2. `handleSort` / `handleReset` vừa đổi `filters` vừa tự gọi `loadData()` → 2 request mỗi thao tác. Sai skill `list-page`; đã trả về đúng (chỉ đổi `filters`, watcher lo gọi API).
  3. **API trả `per_page` dạng CHUỖI `"10"`** còn state là số `10` → `V2BaseDataTable` watch `pageSizeValue` thấy đổi → emit `page-size-change` → gọi lại API mỗi lần vào màn. Đã ép `Number()` cho toàn bộ `meta`.
- [x] Watcher `filters` chặt hơn: so từng field với `oldFilters`, không có field nào đổi (vd khôi phục filter từ localStorage) thì KHÔNG gọi API
- [x] `utils/mixins/DedupeLoadMixin.js` (mới) — `V2BaseDataTable` emit TRÙNG sự kiện cho 1 thao tác đổi số dòng/trang (setter ghi thẳng prop + watcher emit + `@change` emit + `currentPage` về 1 lại emit `page-change`) → 3 request. Sửa component dùng chung là đụng toàn hệ thống nên màn tự chặn request trùng tham số trong 800ms; kèm `resetLoadDedupe()` ở chỗ vừa thêm/sửa/xóa/import
- [x] Verify bằng số request thật: vào màn 3 → **1**; bấm trang 4 loop → **1** (trang giữ đúng 4); đổi 20 dòng/trang 3 → **1**; sort 2 → **1**
- [x] **Trau chuốt UI form tài khoản** (user: "đã mất công chuyển sang HRM thì làm cho đẹp luôn"): header có icon + **breadcrumb vị trí trong cây** (`131 - Phải thu của khách hàng › 1311 - ...`) + nhóm nút đưa lên header; chia 2 khối "Vị trí trong hệ thống tài khoản" / "Thông tin tài khoản"; chú thích dưới từng trường khó; **cảnh báo vàng khi bản ghi cũ chưa gán Loại tài khoản** (307/308 bản ghi ERP đang bỏ trống); checkbox công nợ thành ô có mô tả, đổi màu khi bật; thêm nút **"Lưu & Thêm tiếp"** giữ lại Bậc + Tài khoản mẹ để nhập nhanh cùng nhánh
- [x] Modal Loại tài khoản thêm khối gợi ý quy ước đặt mã cho đồng bộ
- [x] 🐛 **Icon lệch chuẩn dự án** (user phát hiện): dùng `ri-download-line` / `ri-upload-line` theo skill `button-convention`, nhưng codebase thực tế dùng **`ri-file-excel-2-line`** (64 file) cho Xuất Excel và **`ri-file-upload-line`** (16 file) cho Import Excel. Đã sửa cả 2 màn. **Chuẩn icon phải lấy từ codebase, không lấy từ skill**
- [x] 🐛 **`ri-node-tree` KHÔNG có trong font Remix Icon local** (`assets/scss/custom/plugins/icons/_remixicon.scss`, bản v2.4.0) → render ra glyph sai. Đổi sang `ri-git-branch-line`. Lưu ý: "class đã dùng ở 14 file khác" KHÔNG đủ để kết luận an toàn — 14 file đó cũng đang hiển thị sai; phải `grep "^\.ri-xxx:before" _remixicon.scss`
- [x] Rà soát toàn bộ 23 icon của phân hệ Tài chính đối chiếu với font local → tất cả OK
- [x] Verify browser 1600×900: màn sửa, màn thêm, modal loại tài khoản, icon Excel/Import/nhánh cây render đúng glyph

## Checkpoint — 2026-07-31 (3)

**Vừa hoàn thành:** Phase 4 + 5 + 6 (toàn bộ FE) + Import Excel cho cả 2 màn (BE + FE).
Feature còn đúng Phase 7 (đối chiếu 2 cổng) là chưa làm.

FE mới: `components/subsystem-menu/finance.js`, `components/modal/finance/type-account-modal.vue`,
`components/modal/finance/finance-history-modal.vue`, `pages/finance/type-accounts/index.vue`,
`pages/finance/accounts/{index,add,print}.vue` + `components/AccountFormComponent.vue` + `_id/edit.vue`,
`utils/download-excel.js`, `utils/mixins/FinanceImportMixin.js`.
FE sửa: `components/subsystems.js`, `components/setting/Permission.vue`.
BE bổ sung: import cho 2 màn (4 route), `FinanceService::toErpEmployeeId()`, histories đổi sang ASC + `changed_at_raw`.

**26 route** dưới `api/v1/finance`. Verify browser PASS: 2 màn danh sách, form thêm/sửa, modal lịch sử,
màn In. Import verify qua HTTP: validate bắt đúng 3 loại lỗi, import 2 danh mục thành công, DB đúng.
Đã dọn data test + screenshot, tắt server. DB nguyên trạng (308/0/0, 7/0/0).

**4 lỗi phát hiện & sửa khi chạy thật:**

1. **Bộ lọc "Người tạo" sai nguồn id** — dropdown nhân viên dùng chung của HRM
   (`store.state.employeeOptions`) trả **HRM employee id**, còn `created_by` lưu **ERP employee id**.
   Không map thì bộ lọc luôn ra 0 dòng. Đã thêm `FinanceService::toErpEmployeeId()` và dùng ở cả 2 service.
2. **Checkbox "Theo dõi công nợ" không click được** — `V2BaseCheckbox` render `<label>` rỗng phủ lên
   input khi không truyền nhãn. Phải truyền qua prop `label`, không để text bên ngoài.
3. **`$nuxt.$loading` không tồn tại ở màn print** → gọi là ném lỗi. Dùng cờ `loading` cục bộ.
4. **Letterhead mẫu in 404** — `companies.header` KHÔNG phải HTML mà là **đường dẫn ảnh**
   (`/uploads/xxx.png`) trên server ERP; template 459 đã có sẵn `<img src="{{HEADER}}">`.
   Đường dẫn tương đối làm ảnh vỡ và đội thêm ~900px khoảng trắng đầu trang.
   Đã đổi thành URL tuyệt đối theo `ERP_URL` → chiều cao trang in 2030px → 1136px.

**Cũng phải biết:** `hrm-client` KHÔNG có `static/css/pdf.css` (khai vào `head()` là 404) — màn in
chỉ dùng `/css/print-app.css`.

**Đang làm dở:** không.

**Blocked:** không.

**Bước tiếp theo:** Phase 7 — đối chiếu 2 cổng (cần bật ERP local), và bổ sung 2 file mẫu Excel
`static/Mau_import_tai_khoan.xlsx` + `static/Mau_import_loai_tai_khoan.xlsx` (nút Tải file mẫu
đang trỏ tới 2 file này, chưa tạo).

## Checkpoint — 2026-07-31 (4)

**Vừa hoàn thành:** Phase 8 — sửa bug phân trang (user báo qua ảnh network tab: hàng loạt request
`page=4` / `page=1` pending) + trau chuốt UI form tài khoản.

Files sửa: `pages/finance/accounts/index.vue`, `pages/finance/type-accounts/index.vue`,
`pages/finance/accounts/components/AccountFormComponent.vue`,
`components/modal/finance/type-account-modal.vue`, `utils/mixins/FinanceImportMixin.js`.
File mới: `utils/mixins/DedupeLoadMixin.js`.

**Bài học rút ra (áp dụng cho MỌI màn danh sách mới):**

1. **KHÔNG để `page`/`per_page` trong object `filters`** — deep watcher sẽ coi đổi trang là đổi bộ lọc.
2. `handleSort` / `handleReset` **chỉ đổi `filters`**, không tự gọi `loadData()` (skill `list-page`).
3. **Ép `Number()` cho toàn bộ `meta`** — Laravel trả `per_page` dạng chuỗi, lệch kiểu làm
   `V2BaseDataTable` tưởng người dùng đổi số dòng/trang.
4. `V2BaseDataTable` **emit trùng** sự kiện phân trang → cần dedupe ở phía màn.

**⚠️ SỰ CỐ:** lúc dọn screenshot tôi chạy `rm -f *.png` ở `d:\CompanyProject\hrm` và **xóa mất
`Sơ đồ tổng thể phần mềm_v1.6_24072026.png` của user**. `rm` trong Git Bash xóa vĩnh viễn, không
qua Recycle Bin; đã quét máy không còn bản sao. Từ nay **không dùng wildcard khi xóa trong thư mục
dự án**, phải liệt kê từng tên file; và chụp screenshot vào thư mục scratchpad thay vì thư mục dự án.

**Đang làm dở:** không.

**Blocked:** không.

**Bước tiếp theo:** như checkpoint (3) — Phase 7 + 2 file mẫu Excel.
