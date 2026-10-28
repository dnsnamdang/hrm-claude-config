# Khuôn đổi phân hệ sang kiểm quyền theo mã (GĐ3)

Mỗi agent phân hệ/repo ghi 1 mục riêng; nối thêm, không ghi đè.

## hrm-api / hrm-client (warehouse)

Task 7b-HRM, 28/10/2026. Đổi cách gọi, không đổi kết quả: mốc 7a 90 ô hrm-api (18 route × 5 tài khoản) chụp lại sau khi đổi ⇒ khác 0 ô.

### Khuôn đổi gặp phải
1. **Hằng tên cũ trong Entity/Service** (scanner KHÔNG thấy — chỉ bắt chuỗi trong lời gọi): cặp hằng
   `PERMISSION_VIEW_ALL_COMPANY` / `PERMISSION_VIEW_COMPANY` (tên "… theo tổng công ty" min 4 / "… theo công ty" min 3)
   ⇒ gộp 1 hằng `PERMISSION_VIEW = '<mã>'`; `isAllCompany()` = `CurrentPermission::scope(PERMISSION_VIEW) >= PermissionScope::GROUP`,
   `canViewCompany()` = `… >= PermissionScope::COMPANY`. Mọi chỗ `currentEmployeeHasPermission(self::PERMISSION_VIEW_COMPANY)`
   đổi thành `self::canViewCompany()`; thân nhánh lọc giữ nguyên. Grep `::PERMISSION_VIEW_` toàn repo trước khi xoá hằng
   (ExcShortageService gọi từ ngoài).
2. **Hằng không phạm vi** (tạo / duyệt / xử lý / thủ kho / quản lý kho): chỉ đổi giá trị hằng sang mã. Cửa
   `currentEmployeeHasPermission` (PermissionLookup::currentHas) và `employeeInfoIdsHavingPermission` (holders) nhận mã
   sẵn ⇒ người nhận thông báo giữ nguyên (tên cũ min_scope null ⇒ holders(mã) cùng tập người).
3. **Mảng tên trộn phân hệ** (`TransportCostByStaffReportService::PERMISSIONS_*`: tên sale + tên kho): chỉ rút tên kho ra
   thành `scope(warehouse.bao_cao_van_chuyen.view) >= 4/3`, chèn đúng vị trí ưu tiên cũ (all → company → department);
   tên sale để nguyên cho đợt sale.
4. **Hằng alias sang service khác** (`StockDetailByProductReportService::PERMISSION_* = WarehouseStockReportService::…`):
   đổi theo, kiểm không còn ai gọi hằng cũ.
5. **Route middleware** `checkPermission:Quản lý kho` / `checkPermission:Khai báo tồn kho đầu kỳ` (không phạm vi) ⇒ mã.
6. **FE**: `hasAPermission('… theo công ty')` ⇒ `permissionScope(mã) >= 3`; chuỗi 3 cấp ⇒ đọc `permissionScope` 1 lần rồi so
   `>= 4/3/2`. `catalogManagePermission: 'Quản lý kho'` (mixin gọi `hasAPermission`) ⇒ mã. Menu `warehouse.js` (hub — hiểu
   `codes`) thêm `codes: [mã]`, GIỮ `isShow` (AND với codes, 2 điều kiện tương đương).

### DataScope: KHÔNG dùng chỗ nào ở hrm-api warehouse — vì sao
Không màn nào khớp tuyệt đối một mode:
- PositionTransfer / PositionInventoryResult / SelfInventory / ExcShortage / InventoryAuditReport: mức 3 = `company_id = công ty
  ∪ created_by = tôi` — DataScope `record_unit` mức 3 KHÔNG kèm `∪ owner = tôi`; `owner_members` lọc theo thành viên chứ không
  theo cột company_id. Một số màn còn cộng nhánh duyệt (phiếu Chờ duyệt) / nhánh thủ kho (kho mình) / ẩn phiếu Đang tạo của
  người khác.
- WarehouseInventoryImport: mức 3 = `company_id` (khớp record_unit) nhưng nhánh không quyền = phiếu mình tạo (DataScope ⇒ `1 = 0`)
  và cộng nhánh Kế toán kho ⇒ không khớp.
- Thêm: Entity lấy công ty từ `employee_infos.company_id` (`currentCompanyId()`), DataScope lấy `current_company_role` — lệch khi
  người làm 2 công ty. Giữ nhánh cũ + so phạm vi.

### Bẫy
- **Tên chỉ có alias guard `web`**: BE Entity/Service đi `PermissionLookup::currentHas` (tra cả api + web) ⇒ đổi sang mã không đổi
  kết quả. Nhưng FE `hasAPermission(tên)` so `state.permissions` = `CurrentPermission::list()` = CHỈ tên guard `api` ⇒ tên chỉ có
  bản web (vd "Xem phiếu xuất kho theo …") ở FE luôn false; đổi sang mã sẽ bật cờ cho người có mã. Kiểm guard của alias
  (`permission_aliases.legacy_guard`) trước khi đổi ở FE.
- Mã đưa vào phải có dòng `permissions` còn hiệu lực ở DB test: DB `hrm_erp_rbac_test` CHƯA có mã `warehouse.*` ⇒ test tự tạo dòng
  (kèm `allowed_scopes`); test cũ dựng alias cho tên cũ (AllCompanyViewCodesTest) phải đổi sang dòng mã, không thì ném
  `UnknownPermissionCode`.
- `null >= 3` = false ở cả PHP lẫn JS ⇒ có mã không phạm vi / không mã đều rơi nhánh hẹp nhất, đúng như tên cũ min_scope.
- `permission:scan` vẫn báo `isShow: ['Quản lý kho' …]` ở menu vì luật 7b giữ isShow — xoá ở Task 12.

## ERP (warehouse)

Repo `wt-rbac/TanPhatDev` nhánh `rbac` (Task 7b, 28/10). 77 file sửa + 3 file test mới. Đổi CÁCH GỌI, không đổi kết quả.

### Khuôn đổi
- **Tên không phạm vi** (alias `min_scope` NULL — `Thủ kho`, `Quản lý kho`, `Duyệt giá vận chuyển`…): thay chuỗi bằng mã ở
  mọi cửa: `->can('mã')`, `@can('mã')`, `checkPermission:mã` (warehouse không có danh sách trộn tên phân hệ khác; nếu phân hệ sau gặp thì tên phân hệ khác giữ
  nguyên), `Employee::withPermission('mã', $c)`, `Employee::permission('mã')`, `NotificationHelper/Notification::sendNotifyWithPermission('mã', …)`,
  biến JS `searchEmployeeType = 'mã'` (SearchController::searchEmployee → `withPermissionCompany` → `PermissionChecker::holders`
  nhận mã). Đều đi `PermissionChecker` nên cùng luật với tên cũ.
- **Tên có phạm vi** (min_scope m): `->can('… theo công ty')` ⇒ `->permissionScope('mã') >= PermissionScope::COMPANY`.
  Có `!` phía trước thì bọc ngoặc: `!(… >= …)` (`!` ưu tiên cao hơn `>=` trong PHP). `null >= m` = false ⇒ có mã không phạm
  vi / không mã rơi đúng nhánh hẹp nhất như tên cũ.
- **Chuỗi phạm vi**: đọc 1 lần ngay trước `if` — `$scope = $user->permissionScope('mã');` rồi `if ($scope >= GROUP) … elseif
  ($scope >= COMPANY) … elseif ($scope >= DEPARTMENT)`. Giữ nguyên thân từng nhánh (company_id / department_members /
  `∪ created_by` / status≠3 …). Trộn tên phân hệ khác trong cùng điều kiện (vd báo cáo vận chuyển + "chi phí vận chuyển theo
  NVKD" của sale) ⇒ chỉ đổi phần warehouse: `$scope >= GROUP || can('Xem báo cáo chi phí … theo tổng công ty')`.
- **"Có 1 trong N tên Xem"** (canView): mọi tên là biến thể của CÙNG 1 mã, không biến thể nào min_scope NULL ⇒ gộp thành
  `permissionScope(mã) >= min(min_scope)` (vd phiếu xuất kho 4|3|2 ⇒ `>= DEPARTMENT`). Kiểm Catalog trước khi gộp: nếu có
  biến thể NULL thì phải là `can(mã)`.
- **Mảng tên trong model** (`$permissions = ['is_all_company' => 'Tên…', 'is_company' => …]` rồi `can($permissions['…'])` —
  scanner KHÔNG bắt): bỏ mảng, đọc `$scope` NGAY TRONG nhánh `type == 'all'` (nơi `can()` cũ chạy — đọc sớm hơn có thể chạy
  `auth()->user()->…` ở job không đăng nhập), khoá nào trỏ mã khác (vd `is_warehouse` → `dieu_chuyen_vi_tri_theo_kho.view`)
  thì `can('mã đó')`. 2 nhánh khai 2 mảng (PositionInventory plan/result) ⇒ `$scopeCode = 'mã'` ở mỗi nhánh, đọc 1 lần trong
  `type == 'all'` (giữ cả lỗi "biến chưa khai" khi `$request_type` lạ như cũ).
- **Cờ blade/JS**: giữ tên cờ, đổi điều kiện sinh cờ: `is_big_boss: @json(Auth::user()->permissionScope('mã') >=
  \App\Support\Permissions\PermissionScope::GROUP)`. `@json` tách tham số theo dấu phẩy ⇒ biểu thức không được có `,`.
  Cờ controller (`'is_department' => …`) đọc `$scope` 1 lần ở đầu hàm.
- **`Warehouse::getForFilterByCompany/ForCurrentUser('Tên … tổng công ty')`** (bộ lọc kho ở 7 màn): nơi gọi warehouse truyền
  bool đã tính `(permissionScope('mã') >= GROUP)`; `canFilterAllCompanyWarehouses` nhận thêm bool (giữ đường tên cũ cho nơi
  gọi phân hệ khác — finance/accounting chưa đổi).
- Import `use App\Support\Permissions\PermissionScope;` ở file PHP; blade dùng FQCN.

### DataScope — KHÔNG dùng chỗ nào ở ERP warehouse
Không chuỗi nào khớp tuyệt đối một mode: (a) nhánh "không quyền" của ERP hầu hết là `created_by = tôi` HOẶC không lọc gì
(BeginningStock, getForSelectCompanies, báo cáo bốc xếp `e.id = tôi`, hold detail `hd.employee_id`), trong khi DataScope
U8 (có mã không phạm vi ⇒ owner = tôi) chỉ khớp khi nhánh else đúng là `owner = tôi`; (b) nhánh 3 của ERP là `company_id =`
(DataScope `owner_members` 3 = `created_by ∈ thành viên công ty ∪ tôi`, `record_unit` 3 không `∪ tôi`) và thường kèm
`status≠3 ∪ created_by=tôi` ở nhánh 4; (c) nhánh 2 dùng `employee_manage_departments` theo công ty, `dept.id`, `department_id`
cột bản ghi… không phải `department_members` thuần. ⇒ giữ nhánh cũ + so phạm vi ở mọi chỗ.

### Bẫy
- `hrm_erp_rbac_test` chưa có mã `warehouse.*` ⇒ mọi test ERP chạm code warehouse (render `topmenubar`, `canView`) ném
  `UnknownPermissionCode`. Seed bằng `Tests\Feature\Rbac\Concerns\WarehouseCatalog::seed()` (chép Catalog web alias);
  `ErpGateSideEffectsTest::grantLegacy` nay cấp đúng mã thật ở `min_scope` của tên khi tên đã có alias.
- Script đổi hàng loạt: regex chuỗi `(['"])(.*?)\1` nuốt `"{{ can('Tên') }}"` (nháy kép bọc nháy đơn) ⇒ sót 1 chỗ
  (`arriving_report.blade.php`) — chạy lại scan sau khi đổi.
- Scanner sót: mảng tên trong model, `getForFilterBy*('Tên')`, `sendNotifyWithPermission`, `Employee::permission('Tên')`,
  `searchEmployeeType` — grep cả repo theo danh sách tên alias của phân hệ, không chỉ tin `permission:scan`.
- Kiểm "không đổi hành vi": `WarehouseScopeConversionTest` chạy 46 đường đọc × 6 mức quyền, so với bản chụp sinh từ code
  HEAD (env `RBAC_LEGACY_SRC` nạp bản HEAD của file đã đổi trước composer + `RBAC_SNAPSHOT_OUT`). Khuôn này dùng lại được
  cho phân hệ khác: export `git show HEAD:<file>` các file `app/` đã đổi vào 1 thư mục, chạy test ở chế độ legacy ra golden.

## lookup (Task 8.1)
- Chỉ 1 mã (`lookup.phieu_bao_hang_ve_mua_nhap_khau.view`, 4/3/2). Scanner chỉ thấy ERP; hrm-api giấu tên trong 3 hằng `PERMISSION_IMPORT_ALL/COMPANY/DEPARTMENT` của `ProductArrivedNotifySummaryService` (module Finance, nhưng thuộc lookup) ⇒ gộp 1 hằng `PERMISSION_IMPORT_VIEW`, đọc `CurrentPermission::scope` 1 lần. Phân hệ khác cũng nên grep tên alias toàn repo.
- Không dùng DataScope: ERP nhánh 2 là `department_id ∈ employee_manage_departments`, nhánh không quyền là `id ∈ ids ∪ created_by`; hrm-api nhánh không quyền là created_by ∪ cặp thương hiệu-hãng.
- Route HRM `product-arrived-notifies` không gác quyền (giữ). Menu lookup.js không có isShow/codes ⇒ không đổi FE.
- Test whereIn rỗng sinh `0 = 1`: fixture phải cho người dùng quản lý 1 phòng mới thấy nhánh department_id.

## admin (Task 8.2)
- 5 mã, đều min_scope NULL ⇒ chỉ thay chuỗi (luật 1/4). Không chuỗi phạm vi, không DataScope.
- **Mã gộp 2 tên khác guard** (`admin.phan_quyen.manage` = web "Quản lý chức vụ" + api "Quản lý phân quyền"): đổi cả 2 phía
  sang 1 mã không đổi hành vi vì checker đã quy tên → mã từ GĐ1; FE `hasAPermission(tên api)` = `CurrentPermission::list()`
  (alias api của mã đang giữ) nên tương đương `hasAPermission(mã)`.
- Scanner sót: `SettingHistory/Adapters/*::permissions()` trả mảng tên (controller gọi `isCurrentEmployeeHasPermission` từng
  phần tử) — grep `return ['Tên']`.
- **Bẫy test:** fixture GĐ2 (`AdminRoleFixture`, `BulkRoleGrantTest`, `HrmGateSideEffectsTest`) cấp quyền quản trị bằng mã giả
  `zz.*.manage` + alias 'Quản lý phân quyền' ⇒ sau đổi route kiểm thẳng mã, 21 test 403/UnknownPermissionCode. Thêm
  `GateFixture::ensureCode(mã)` (dùng lại/ tạo dòng mã thật) và cho fixture cấp `admin.phan_quyen.manage`.
- Mốc khi không có đường đọc theo phạm vi: route gác × (đủ mã / 1 phần mã / không mã); ô dashboard ERP đọc bằng
  `extract.path` (`data.data.HE_THONG`) vì "mảng lớn nhất" không bắt được ô chỉ có/không.
- `menu.js` (Chấm công › Cấu hình › Cài đặt phân hệ, sidebar training-components chưa hiểu `codes`): giữ `isShow`, để đợt timesheet.

## meeting (Task 8.3)
- Chỉ hrm-api + hrm-client (ERP 0 hit). 8 mã; 1 chuỗi phạm vi 4 mức (`danh_sach_meeting.view` 4/3/2/1) + 1 tên min_scope 4 (`Xem tất cả phiếu đặt phòng họp` ⇒ `scope(phieu_dat_phong_hop.view) >= GROUP`, KHÔNG `has`).
- **`checkPermissionList($q, [4 tên, true], 'meetings')` (helper dùng chung ở PermissionHelper)**: không truyền mã vào được (helper gọi `has` từng tên). Chép nguyên 5 nhánh của helper vào nơi gọi (MeetingCriteria) với điều kiện `$scope >= 4/3/2/1`, else = created_by (cờ [4]). Không dùng DataScope: `record_unit` khớp mức 1–4 + "có mã không phạm vi" nhưng nhánh KHÔNG mã của DataScope là `1 = 0`, helper là `created_by = tôi` ⇒ không khớp tuyệt đối (dù kết quả cuối giống vì criteria đã OR created_by bên ngoài). Phân hệ khác gọi checkPermissionList cũng làm khuôn này.
- Scanner sót: `const PERMISSION_VIEW_ALL = 'Tên'` ở FE (bookings/index.vue) và mảng tên trong `checkPermissionList([...])` (scanner chỉ bắt 1 hit scope_chain ở Entity) — grep tên alias toàn repo.
- **Bẫy test cũ (ngoài tests/Feature/Rbac)**: ~9 lớp test meeting chạy KHÔNG transaction trên `hrm_erp_rbac_test` (DB chưa đồng bộ Catalog: chưa có dòng mã `meeting.*`, 0 alias) ⇒ sau đổi ném UnknownPermissionCode. Thêm `AdoptsLegacyRbacFixture::adoptCatalogCodes()` (tests/Concerns): dựng dòng mã thật theo Catalog + alias tên cũ (min_scope Catalog), tự gọi đầu `adoptLegacyRbac()` (adoptAliases sẵn có sẽ tick mã thật ở đúng min_scope cho người fixture tick tên cũ), lớp test có ca "chưa cấp quyền" gọi trong setUp; gỡ ở `undoAdoptLegacyRbac()`. Danh sách phân hệ trong hàm hiện chỉ `['meeting']` — phân hệ sau gặp lỗi tương tự thì thêm tên vào đó. So kết quả trước/sau từng file (danh sách ca đỏ sẵn y hệt).
- FE: menu meeting.js (hub — hiểu `codes`) thêm `codes` cạnh isShow; trang không vào được do menu-settings ẩn (`/feature-unavailable?reason=hidden`, vd Đăng ký phòng họp với 145/110/207) là cấu hình phân hệ, không phải quyền.

## rice (Task 8.4)
- Chỉ hrm-api + hrm-client (ERP 0 hit; 3 hit Dart ở TPE_APP — để Task 9). 11 mã; 3 mã Xem 4/3/2, còn lại không phạm vi.
- **Helper lọc riêng của phân hệ** (`app/Helper/RiceHelper.php::checkRicePermissionList`, chỉ rice gọi, 14 chỗ): scanner KHÔNG thấy
  (mảng tên truyền vào helper — chỉ bắt 3 scope_chain ở FE). Đổi tham số 2 từ mảng tên sang MÃ, helper đọc `CurrentPermission::scope`
  1 lần, giữ nguyên thân 3 nhánh; nhánh [3] cũ (bộ phận) mọi nơi gọi truyền `false` nên bỏ. Nơi gọi dạng `$type == 'detail' ? tên A : tên B`
  ⇒ hàm `reportViewCode($type)`. Giữ cả chỗ "lạ" của code cũ (báo cáo tổng hợp khách lọc phần dài ngày bằng tên CHI TIẾT) + comment.
- Không DataScope: nhánh 3 = `rice_company_id` (công ty CƠM qua findRiceCompany) ∪ của mình, nhánh 2 = phòng CƠM (rice_departments ↔
  department quản lý), nhánh không mã = của mình (DataScope `1 = 0`) ⇒ không khớp mode nào.
- **Bẫy test**: bảng rice_* ở kết nối `mysql_tpe`, `.env`/phpunit không có DB_*_TPE ⇒ test cho `mysql_tpe` = config `mysql` rồi
  `setPdo(DB::connection('mysql')->getPdo())` để dùng chung transaction (rollback sạch). Đừng gọi đường code mở transaction riêng trên
  mysql_tpe trong test. `RiceSheetRegistration::status` accessor đổi phiếu khách quá giờ thành 3 ⇒ test is_can_cancel dùng giờ tương lai.
- Menu `components/default-menu/rice.js` render qua Topbar (layout default) — đã hiểu `codes` ⇒ thêm `codes` cạnh isShow.

## timesheet (Task 8.5)
- Chỉ hrm-api + hrm-client (ERP 0 hit). 30 mã; ~50 file BE. Nhiều tên dùng chung ngoài module: `Thiết lập thông số` (= `timesheet.thong_so.configure`) gác cả Cấu hình nhân sự / Bảo hiểm / Định biên / lịch sử cấu hình (routes/api.php master-settings, Human InsuranceConfig, 10 adapter SettingHistory, HumanSettingHistoryController, GeneralRegulationController) ⇒ đổi đúng tên đó ở mọi nơi; tên phân hệ khác trong cùng mảng (`Thiết lập thông số lương`, `Cấu hình phân hệ giao việc/ công tác`) giữ nguyên.
- **Hàm kiểm quyền tự viết** `TimesheetService::isCurrentEmployeeHasPermission` (≈50 service kế thừa, kể cả ReportService được Entity gọi `$reportService->…`): `Employee::firstOrNew(employee_info_id)->getAllPermissions()` + `in_array(tên)` — tên guard api ở công ty đang làm việc, KHÔNG nhận mã (luôn false). Đổi thân thành `CurrentPermission::has()` (tương đương cho người đăng nhập; rehearsal 0 employee_info_id trùng). Phải sửa TRƯỚC khi đổi tên→mã trong service con.
- **`checkPermissionList($q, [4 tên, true], $t)` ở 6 màn đơn** ⇒ thêm `TimesheetService::applyViewScope($q, mã, $t)` (chép nguyên 5 nhánh helper, điều kiện = phạm vi đọc 1 lần) thay vì chép vào từng nơi gọi (khác meeting: ở đây 6 nơi cùng khuôn, cùng lớp cha). `checkPermissionListNotAllCompany` (1 nơi — bảng phân ca chi tiết) chép tại chỗ, GIỮ cả lỗi cũ `whereIn(phòng) AND whereIn(bộ phận)` ở nhánh 2.
- **Helper riêng nhận mảng tên** `ShiftDetailEmployeeDateService::checkPermissionShiftByDate($q, [3 tên Phân ca])` (8 nơi gọi, có 1 ở Modules/Human) ⇒ đổi tham số 2 sang MÃ (như rice). Scanner không thấy.
- **Cờ `permissions` 4 khoá** (`is_all_company/is_company/is_department/is_part` = 4 tên min 4/3/2/1 của cùng mã) ở 8 controller ⇒ `TimesheetService::viewScopeFlags(mã)` (đọc phạm vi 1 lần). Cờ 2–3 khoá lệch khuôn (bảng tổng hợp tháng 3/2, ca làm việc chỉ is_all_company) đổi tại chỗ.
- Chuỗi `if/elseif` mỗi nhánh 1 lời gọi tên ⇒ script: chèn `$scope = CurrentPermission::scope(mã);` trước `if` đầu, đổi điều kiện; chuỗi dạng nhiều `if … return` liên tiếp (lịch sử phân ca, WorkingShiftAdapter) phải gộp lại 1 lần đọc (dedupe).
- Script đổi hàng loạt: regex có nhiều nhóm thì `\1` trỏ sai nhóm khi ghép chuỗi pattern — đánh số lại / dùng nhóm có tên.
- **Middleware danh sách đủ biến thể** (`Quản lý ca làm việc|Xem danh mục ca … tổng công ty|… công ty`, `Phân ca theo công ty|phòng ban|bộ phận`) ⇒ `manage|view` / mã (U8). FE giữ đúng điều kiện cũ (`hasAPermission(manage) || permissionScope(view) >= 3`).
- **Menu**: `components/menu.js` (Chấm công / Thông tin NS / Tính lương) render qua Topbar (layout default) — đã hiểu `codes`; thêm hỗ trợ `codes` cho `training-components/Sidebar.vue` (isShowMenuParent + isShowSubItemMenu, AND như Topbar) vì sidebar này cũng dựng menu theo phân hệ. KHÔNG khai `codes` ở mục cha có `subItems` mà `isShow` cha là OR với con (Topbar `showMenuParent`: con hiện thì cha hiện) — khai `codes` ở cha sẽ ẩn cha dù con được phép. Mục cha `isShow` trộn tên phân hệ khác (`Thiết lập thông số lương`) cũng không khai.
- `groups: ['Bảng chấm công tổng hợp']` / `hasGroup(...)` (PayrollMenu) là NHÓM quyền, không phải tên — scanner vẫn báo legacy, không đổi.
- Không dùng DataScope: nhánh không mã = `created_by`/bản thân (DataScope `1 = 0`), nhánh công ty có/không `∪ bản thân` tuỳ màn, nhánh phòng = cột bản ghi ∪ bộ phận.
- Mốc: ô có cột ngày null mà Resource trả `now()` (overtime-assignment) ⇒ băm id thay băm nội dung.

## human (Task 8.6)
- hrm-api + 1 chỗ ERP + hrm-client. 31 mã. Nhiều tên human nằm NGOÀI Modules/Human: Payroll (`SalaryController`/`SalaryService` — báo cáo bảo hiểm tháng/năm, bảng nhân sự và quỹ lương), `routes/api.php` + `Admin/AccountController` (màn tài khoản GĐ2b), MasterData (`Cài đặt cấu hình` = `human.cau_hinh.configure` gác cả Khai Quy chế – Cấu hình của finance/assign/sale), ERP `Employee::HRM_ACCOUNT_SCREEN_PERMISSIONS` (mục menu ERP trỏ màn tài khoản HRM).
- **Helper chung ở lớp cha**: thêm `HumanService::applyViewScope($q, mã, $bảng)` (chép 5 nhánh checkPermissionList [4 tên, true]) + `static viewScopeFlags(mã)` như timesheet; Payroll gọi `HumanService::viewScopeFlags` (static) cho cờ bảo hiểm. EmployeeService bỏ hằng `ACCOUNT_VIEW_PERMISSIONS` (4 tên) ⇒ `ACCOUNT_VIEW_CODE`.
- **2 override tự viết** (MissionService, DepartmentManpowerService — `Employee::firstOrNew(employee_info_id)->getAllPermissions()` + in_array) ⇒ thân `CurrentPermission::has` như timesheet; giữ hàm (không ai gọi từ ngoài nhưng giữ chữ ký). Chuỗi trong 2 service đổi thẳng sang `CurrentPermission::scope`.
- **Chuỗi phạm vi dùng biến trong closure** (CompanyService::getDataReport — chuỗi thứ 2 nằm trong `->map(function ($comp) use ($request)`) ⇒ đọc `$scope` 1 lần ở đầu hàm và thêm vào `use (...)`.
- **Chuỗi "chết"**: DepartmentManpowerService::report chuỗi quỹ lương gán `$employee_info_ids` nhưng builder mức 3/2/else không bao giờ chạy (chỉ mức 4 gọi `EmployeeInfo::all()` thật) — đổi điều kiện, giữ nguyên; test đo bằng có/không câu `all()`.
- **Hằng tên trong controller dùng làm khoá tra trong test** (`RegulationConfigController::PERM_EDIT`): đổi hằng sang mã thì 4 test MasterData (tra `Permission::where('name', PERM_EDIT)`) vỡ ⇒ test tra tên cũ literal + thêm `'human'` vào `adoptCatalogCodes()` để có dòng mã. Grep `::HẰNG` trong tests trước khi đổi giá trị hằng.
- **ERP gọi mã HRM**: `canOpenHrmAccountScreen` đổi từ `hasLegacy(tên, 'api')` ⇒ `hasLegacyPermission(mã)` (có mã view ở mọi mức hoặc manage). Mọi trang ERP render topmenubar nay cần dòng mã `human.tai_khoan_nhan_vien.*` — DB thiếu (DB test cũ) ⇒ UnknownPermissionCode ở local/testing (ErpGateSideEffectsTest phải dựng mã thật).
- **Menu**: menu.js (human/payroll), menu-sidebar.js (assign), admin.js, finance.js, operation-hub.js đều render qua Topbar / training Sidebar / hub đã hiểu `codes` ⇒ thêm `codes` cạnh isShow. `operation.js::buildTree` trước đây BỎ `codes` của nhóm-có-link (mục 1 cấp) ⇒ thêm `codes: group.codes`. HumanMenu.vue (layout human) không đọc isShow ⇒ không đụng. 4 mục cha isShow 'Thiết lập thông số' giữ như ruling timesheet.
- Không dùng DataScope: nhánh không mã = created_by / bản thân / phòng của mình (DataScope `1 = 0`), nhánh 3 không ∪ bản thân, nhánh 2 tuỳ màn (department_id cột bản ghi / whereHas departments / department ∪ part).
- Mốc: thêm route kiểu `lists` cạnh route `auto` (cùng url) để chụp cờ `permissions.is_*`; cờ bool cấp đỉnh không bắt đầu bằng is_/can_ (`hasPermissionEmployeeAccount`, `permissionResigned`) chụp bằng script riêng.

## decision (Task 8.7)
- hrm-api + 1 chỗ ERP (3 middleware mẫu in `decision.mau_in.manage`) + hrm-client. 38 mã. Không chuỗi `if/elseif` tự viết: mọi lọc phạm vi đi qua `checkPermissionList` (14 nơi, mảng tên + cờ đuôi khác nhau: `true` = created_by, `[…, false, false, true]` = `labor_contract_employee_info_id`, toàn `false` = `id is null`, kèm `$queryBuilder` ở filterDecision) và `checkPermissionListWithCompanyFilter` (24 lời gọi trong DashboardService).
- **Helper tĩnh dùng chung của module** `Modules/Decision/Services/DecisionViewScope` (`apply` / `applyWithCompanyFilter`): chép nguyên thân 2 helper PermissionHelper, 4 vị trí tên đổi thành CỜ bool (`['Tên tổng', 'Tên công ty', false, false, true]` ⇒ `[true, true, false, false, true]`), phạm vi mã đọc 1 lần. Đổi nơi gọi bằng script parse đối số (tên → `true`, chèn mã làm đối số 2) — giữ nguyên vị trí `false` và đuôi. Services decision kế thừa `Modules\Training\Services\BaseService` (phân hệ khác) nên không nhét vào lớp cha.
- **Vị trí truyền tên lạ** (reward-mode / reward-title truyền 'theo phòng ban/bộ phận' — mã chỉ phạm vi 3/4, alias không tồn tại ⇒ cũ luôn false) ⇒ cờ `false` + comment, KHÔNG `true` (dù kết quả như nhau vì phạm vi tối đa 3/4).
- **Mảng cũ thiếu biến thể dù mã có đủ phạm vi** (gói bảo hiểm, loại sự cố: mã 1–4 nhưng mảng chỉ 2 tên tổng/công ty) ⇒ phạm vi 2/1 vẫn rơi về phiếu mình — giữ đúng, test khoá ca này.
- Dashboard: `getDashboardPermissions()` trả cờ, `hasDashboardPermission()` = `scope >= DEPARTMENT`, thay 24 lời gọi `checkPermissionListWithCompanyFilter(` bằng `$this->dashboardScope(` (wrapper giữ nguyên chữ ký).
- Cờ `is_all_company/is_company` của 6 controller danh mục: tính trong `index()` (không constructor) từ `$scope` đọc 1 lần.
- **Bẫy test**: paginate tổng 0 dòng thì Laravel bỏ câu lấy dòng ⇒ so số lần `created_by` phải lấy câu `count` đầu tiên, không nối cả log. filterDecision join `decisions` vào bảng loại quyết định ⇒ tìm truy vấn theo `from \`department_establishments\``. Màn chờ duyệt từng loại = `?type=waiting-approve` trên index.
- FE: `operation.js::toLeaf` nay bê `codes` của màn (trước bỏ ⇒ codes khai ở operation-hub không có tác dụng ở sidebar cây). Menu operation-hub / insurance / admin (mẫu in) / sale-hub (quy chế lương) thêm `codes` cạnh isShow. `groups: ['Quyết định']` là nhóm quyền — không đổi.
- Không dùng DataScope: nhánh không mã = created_by / HĐLĐ của mình / `id is null` / customBuilder đối tượng bị tác động (DataScope `1 = 0`), nhánh 3 không ∪ bản thân, nhánh 4 của dashboard = công ty quản lý được (manageCompanyIds) chứ không phải "không lọc".

## presale (Task 8.8)
- Chỉ hrm-api + hrm-client (ERP 0 hit). 38 mã; code nằm hết trong `Modules/Assign` (màn `/assign/...`) + 1 lệnh `app/Console/Commands/Assign`. 101 tên trong middleware `Modules/Assign/Routes/api.php` đều min_scope null ⇒ đổi bằng script theo từng token của `checkPermission:a|b` (tên phân hệ khác cùng danh sách giữ nguyên).
- **Helper tĩnh `Modules/Assign/Services/PresaleViewScope`** (`apply` = checkPermissionList, `applyWithColumn` = checkPermissionListWithColumn): mọi nơi gọi presale truyền đủ 4 tên + `true` nên helper chỉ nhận MÃ (không mảng cờ như DecisionViewScope). Dùng ở báo giá (list + `scopedQuotationQuery` chi tiết/sao chép), YC giải pháp, dự án TKT (`ProspectiveProject::scopeByViewPermission`, hằng `VIEW_PERMISSIONS` ⇒ `VIEW_CODE`), báo cáo tổng hợp GP.
- **Chuỗi `if (tên tổng) … if (tên công ty) … if (tên phòng ban)` ở 11 báo cáo** ⇒ script tìm hàm bao quanh: ≥ 2 lần kiểm cùng mã thì chèn `$viewScope = CurrentPermission::scope(mã)` đầu hàm, 1 lần thì inline. Bẫy: (a) hàm có đệm (`permissionLevel()` với `$this->…Cache`) — đặt dòng đọc phạm vi SAU khối return đệm; (b) hàm có return sớm trước lần kiểm đầu (Meeting::canViewByPotentialCustomerTracking: không có nhu cầu ⇒ false) — đặt ngay trước lần kiểm đầu, giữ thứ tự cũ (không gọi ensure khi không cần). `hasReportPermission()` = OR đủ 3 tên ⇒ `scope >= DEPARTMENT`.
- **Hằng tên trong service bị nơi khác dùng** (`PotentialCustomerTrackingService::PERM_*`, `ServiceDemandReportService::PERM_*` dùng trong `Meeting.php` của meeting): gộp thành 1 hằng `PERM_VIEW = mã`, đổi cả nơi dùng ngoài file. Test cũ khai hằng `PERM_ALL` RIÊNG trong lớp test (không tham chiếu service) ⇒ không vỡ.
- **Câu báo lỗi chứa tên quyền** (`ensurePermission($p)` ⇒ `'Bạn không có quyền "' . $p . '"'` ở QuotationService và ProspectiveProjectExtensionService): thêm hằng `PERMISSION_LABELS [mã => tên cũ]` để câu báo lỗi giữ nguyên chữ.
- **FE**: khối `this.permissions = { is_all_company: has(tên tổng), … }` ⇒ `const viewScope = this.permissionScope(mã)` ngay trước khối rồi `viewScope >= 4/3/2/1`. `[4 tên].some(hasAPermission)` ⇒ `permissionScope(mã) >= 1`. `hasMultiplePermission([tên…])` ⇒ `hasAnyPermission([mã…])`. `state.permissions.some(p => p.name === tên)` ⇒ `hasAPermission(mã)`.
- **Menu**: presale.js (hub + sidebar cây), sale-hub.js, menu-sidebar.js thêm `codes` cạnh isShow. `sale.js` (sidebar cây Bán hàng) có map `SALE_LINK_PERMISSIONS` (tên) ⇒ thêm map `SALE_LINK_CODES` song song + `toLeaf` nay bê `codes` inline của màn khi dùng isShow inline (finding Minor 2 của review 8.7). 5 danh mục dự án ở presale.js / sale-hub.js không khai isShow ⇒ KHÔNG thêm codes (sẽ ẩn thêm).
- **Bẫy test**: test cũ báo cáo (MeetingByEmployees / MeetingByProjects / PotentialCustomerTracking / ServiceDemand) có ca "không quyền" không cấp tên nào ⇒ UnknownPermissionCode. Gọi `adoptCatalogCodes()` trong `actAs()` của fixture (idempotent, gỡ ở undo) thay vì sửa setUp từng lớp; thêm `'presale'` vào danh sách phân hệ. `HrmPermissionLookupTest` dùng mã giả `zz.gate_test.view` + alias tên presale ⇒ thêm `useRealCode(mã)` đổi `code` của dòng fixture thành mã thật.
- **Bẫy test route**: `$route->gatherMiddleware()` dựng controller của MỌI route (controller timesheet gọi `CurrentPermission::scope` trong constructor ⇒ ném) — duyệt route chỉ đọc `$route->middleware()`.
- **Bẫy mốc**: báo cáo meeting lọc theo `now()` (#11145) ⇒ meeting qua giờ giữa 2 lần chụp làm lệch ô (xem presale-so-sanh.md). Chụp trước/sau cách nhau ngắn, lệch thì tra `meetings.start_date` trong khoảng 2 lần chụp.
- Không dùng DataScope: nhánh không mã = created_by / NV KD / chủ trì / thành viên meeting / `e.id = tôi` (DataScope `1 = 0`), nhánh 3 có/không `∪ created_by` tuỳ báo cáo, nhánh 2 dùng `department_id`/`part_id` cột bản ghi hoặc hồ sơ NV.

## accounting (Task 8.9)
- Gần hết ở ERP (~95 file app + 23 blade + routes/web.php); hrm-api chỉ 2 tên không phạm vi ("Kế toán kho", "Kế toán") ở Assign (YCXH/ĐNXK/PXH, 4 middleware ĐNXK) và hằng `PERMISSION_*` của 16 Entity Finance; hrm-client 3 trang finance + 1 mục finance.js. 45 mã, 27 có phạm vi.
- **Script đổi ERP có hoist** (`scratchpad/acc/conv.py`): lexer PHP bỏ chuỗi/comment, dựng ngăn xếp ngoặc; mỗi `RECV->can|hasPermissionTo('tên phạm vi')` gom theo (RECV, mã, thân hàm/closure gần nhất); nhóm ≥ 2 chỗ ⇒ chèn `$<maCamel>Scope = RECV->permissionScope('mã');` ngay trước CÂU LỆNH chứa chỗ đầu (lùi qua `} else if` về đầu chuỗi if), các chỗ sau phải nằm trong cùng khối `{}` (không qua closure) mới dùng chung biến; 1 chỗ ⇒ inline. Tên biến theo mã (`$quyetToanHoaHongQuyScope`) để 2 chuỗi lồng nhau khác mã không đè nhau. `!` phía trước ⇒ bọc ngoặc. Hậu kỳ: `($s >= GROUP || $s >= COMPANY)` trong ngoặc ⇒ `($s >= COMPANY)`. Blade luôn inline FQCN. Ghi ra thư mục bóng (`--out=`) để đọc diff trước khi ghi thật.
- Khuôn mới: **mảng `$permissions = ['is_all_company' => auth()->user()->can(...), ...]` ở controller/service báo cáo** (≈ 60 chỗ) ⇒ 1 dòng đọc phạm vi ngay trước mảng; mảng tên trong model (`WrAccountingService(Request)::searchByFilter` `$permissions['is_company']` là CHUỖI tên) ⇒ bỏ mảng, đọc `$scope` trong nhánh `type == 'all'`.
- **Golden ERP có báo cáo nặng**: `account_details` ~1,2 triệu dòng, `analysisProfitContract/searchData` và `account_details/searchData*` > 60 s trên rehearsal làm SẬP `php -S` (fatal "60+2 seconds (terminated)" giết cả cha lẫn worker) ⇒ bỏ khỏi mốc HTTP, phủ bằng golden. Golden chạy báo cáo nặng trong `DB::pretend()` (cả `mysql` lẫn `hrm`): nạp sẵn đệm quyền (`permissionScope` mọi mã + `can` mọi alias + `loadMissing('info')`) rồi pretend ⇒ chỉ ghi câu SQL. Báo cáo cần bảng tra (works TNST/TTHHD/TVC, khách hàng, tài khoản) vỡ trước nhánh quyền khi pretend ⇒ chạy thật với khoảng ngày 1 tháng (`REAL_HEAVY`, ~3 phút/8 mức). Câu SQL > 400 ký tự lưu 200 ký tự đầu + sha1 (golden 330 KB thay 1,5 MB).
- Bẫy: `ReportController::commissionMonthSearchData` có `catch (\ErrorException $e) { dd($e); }` ⇒ dừng cả tiến trình PHPUnit — gọi thẳng service. Golden sinh khi cây ERP còn = HEAD (chưa sửa), đối chứng lại bằng `RBAC_LEGACY_SRC` sau khi sửa: trùng từng byte.
- Bẫy test: mọi test ERP render topmenubar / chạm code kho (WarehouseScopeConversionTest, ErpGateSideEffectsTest, AdminCodesTest, DecisionCodesTest) phải seed thêm `AccountingCatalog::seed()` vì "Kế toán kho"… nay là mã.
- Tên lạ ⇒ `false` + comment: `Xem báo doanh thu tính hoa hồng của tổng công ty` (gõ sai) và `Xem báo cáo doanh thu tính hoa hồng của công ty` (danh mục chỉ có phòng ban/bộ phận, bản "của của công ty" đã bỏ) ở `revenueCommission`, `revenueCommissionSearchData`, `RevenueCommissionPrint`.
- `Quản lý chi phí` ở hrm-api/hrm-client (CostTraining, cost_trainings, training-sidebar, menu-sidebar) là `training.chi_phi.manage` (alias api) — scanner gán nhầm accounting vì tra alias theo tên bỏ qua guard; KHÔNG đổi ở 8.9, để đợt training.
- Không dùng DataScope: nhánh 4 thường `không lọc` / `status≠đang tạo ∪ tôi`, nhánh 3 `company_id` ∪ `created_by` tuỳ màn (WrAccounting có ∪ tôi, quyết toán không), nhánh 2 `department_id ∈ employee_manage_departments` theo công ty, nhánh không mã = `created_by` ⇒ không khớp mode nào.

## payroll (Task 8.10)
- Chỉ hrm-api + hrm-client (ERP 0 hit, TPE_APP 0 hit). Nhỏ: 2 chuỗi `bang_luong.view` (4/3) ở SalaryService, 1 chuỗi `bao_cao_bang_chi_tra.view` (4/3/2/1) nằm ở **Modules/Timesheet** (ReportService::payroll_info + cờ ReportsController) — tên payroll nằm ngoài Modules/Payroll; tìm bằng grep tên alias, không theo thư mục.
- **Mảng "mã HOẶC tên"** do đợt trước để lại (`['timesheet.thong_so.configure', 'Thiết lập thông số lương']` ở GeneralRegulationController::FIELD_PERMISSIONS, HumanSettingAdapter::permissions, HumanSettingHistoryController, middleware general-regulations, FE salary-config) — scanner KHÔNG báo các mảng này (chỉ báo middleware) ⇒ grep tên. Chỉ đổi phần tên của phân hệ mình; tên phân hệ khác (`Cấu hình phân hệ giao việc/ công tác`) giữ.
- Chuỗi trong vòng lặp 12 tháng (payroll_info) ⇒ đọc `$scope` 1 lần trước `for`.
- Cờ 4 khoá ⇒ dùng lại `TimesheetService::viewScopeFlags(mã)` (static, đã có từ 8.5).
- Menu menu.js (Topbar + training Sidebar hiểu `codes`): leaf `isShow: ['Thiết lập thông số', 'Thiết lập thông số lương']` (OR 2 tên 2 phân hệ) ⇒ `codes: [2 mã]` (passesCodes = có 1 trong các mã, AND isShow ⇒ tương đương). `groups:` / `hasGroup` (PayrollMenu.vue, menu.js) là nhóm quyền — không đổi.
- Không dùng DataScope: danh sách bảng lương nhánh < 3 = `company_id` + (đã chốt ∪ created_by); nhân viên bảng lương nhánh else = bản thân (`employee_infos.id`); báo cáo nhánh 2 = phòng ∪ bộ phận quản lý theo cột hồ sơ NV, else = bản thân ⇒ không khớp mode nào.

## training (Task 8.11)
- Chỉ hrm-api + hrm-client (ERP 0 hit, TPE_APP 0 hit). 58 mã (20 có phạm vi), mọi alias guard api. Không route nào gác middleware — mọi kiểm quyền nằm trong controller/service/Entity.
- **Helper tĩnh `Modules/Training/Services/TrainingViewScope`**: `apply` = checkPermissionList với mảng CỜ (như DecisionViewScope, vì training có mảng lệch khuôn: `[tổng, công ty, false, false]` kết quả khảo sát của phòng; `[4 tên, false, true]` lộ trình thăng tiến = nhánh vị trí công việc rồi vẫn `id is null` như cũ), `applyEmployeeInfo` = checkPermissionEmployeeInfo. 16 nơi gọi đổi bằng script parse mảng (bỏ qua lời gọi nằm trong comment `//`).
- **Mảng `$permissions` tên cũ truyền vào `Entity::can*($permissions)`** (12 Resource dựng `Employee::firstOrNew(employee_info_id)->getAllPermissions()->pluck('name')`, Entity `in_array('Tên', $permissions)`): scanner chỉ thấy phần Entity. Đổi Resource sang `array_keys(CurrentPermission::map())` (danh sách MÃ đang có) và Entity `in_array('mã', …)` — chỉ đúng khi mọi tên trong Entity là min_scope null (training: đúng). Grep `->canX($permissions)` toàn repo trước khi đổi (không nơi nào khác truyền mảng tên).
- **Override nằm ở FormRequest::authorize()** (Store/UpdateTrainingSurveyRequest: getAllPermissions + in_array) và ở lớp cha `Modules/Training/Http/Controllers/V1/ApiController` (35 controller kế thừa) + SubjectController + TrainingRequestController ⇒ thân `CurrentPermission::has`.
- **Helper lọc riêng nhận mảng tên trong service** (`CapacityReportService::checkPermission[TrainingPlan|Courses]($q, [tổng, công ty, false, false])`) ⇒ đổi chữ ký nhận MÃ, đọc phạm vi 1 lần. `CareerProgressionService::checkPermissionList` (method) là code chết — mọi nơi gọi hàm toàn cục; không đụng.
- **`'isShow' => [tên]` trong response API** (DashboardService::getJobWaitingApprove lọc bằng `array_intersect(isShow, getAllCurrentPermission())`): đổi giá trị sang mã + so với `array_keys(CurrentPermission::map())`. FE không đọc `isShow` của mục con này.
- Tên lạ đổi `false` + comment: "… theo theo công ty" (5 chỗ Entity), "Duyệt đề xuất đào tạo", vị trí "… phòng ban  " (2 dấu cách cuối) trong mảng kỳ thi ĐGNL.
- Menu: training dùng hub (`SaleHubSidebar`, layout default-sidebar, `HUB_SUBSYSTEMS` có training) đọc `menuItemsTraining` (menu-sidebar.js) — đã hiểu `codes` ⇒ thêm `codes` cạnh isShow ở 26 mục lá. `training-components/training-sidebar.vue` KHÔNG được import ở đâu (code chết) ⇒ không đổi. Đo menu hub bằng `vm.allScreens` của SaleHubSidebar (link nằm trong panel bay ra, không có `<a>` trong DOM khi panel đóng); khoá theo link ĐẦY ĐỦ (có `?type=waiting`) vì cùng path có mục gate và mục không gate.
- Mốc: công cụ riêng `snap.py` băm mọi cờ bool (cả cờ từng dòng `canEdit/canDelete…` theo id) — ScopeSnapshot chỉ bắt is_/can_ cấp đỉnh. Báo cáo `training-status-by-personnel` không ORDER BY ⇒ trang đầu dao động.
- Không dùng DataScope: nhánh không mã = created_by / vị trí công việc / `id is null` / bản thân (DataScope `1 = 0`), nhánh 3 không ∪ bản thân, CourseService nhánh không mã = mình tạo ∪ phụ trách ∪ giảng viên ⇒ không khớp mode nào.

## assign (Task 8.12)
- Chỉ hrm-api + hrm-client (ERP 0 hit thật — grep chuỗi con ra 'Duyệt hồ sơ thanh toán phiếu công tác' là tên web của customer_care, nhãn blade). 60 mã, 21 có phạm vi. Tên assign nằm cả ở **Modules/Timesheet** (BusinessTripAssign/JobAssignmentNote: 'Quản lý phiếu đi công tác/giao việc', 'Gia hạn, kết thúc sớm…'), **app/Services/SettingHistory/Adapters** (5 adapter `permissions()` = 'Cấu hình phân hệ giao việc/ công tác'), middleware POST general-regulations (Timesheet/Routes) và mảng FIELD_PERMISSIONS của GeneralRegulationController.
- **Script tokenizer PHP** (`scratchpad/assign/conv.php`, `token_get_all`): literal = tên assign (a) trong `isCurrentEmployeeHasPermission(...)` (mọi receiver: hàm toàn cục, `$this->`, `self::`, `BaseModel::`, `$this->xService->`) min null ⇒ đổi chuỗi; min m ⇒ `$<maCamel>Scope >= PermissionScope::X`, hoist khi ≥2 chỗ cùng thân hàm/closure tại đầu câu lệnh của KHỐI CHUNG THẤP NHẤT chứa mọi chỗ (lùi qua `} else if` về đầu chuỗi if), 1 chỗ inline; `!` ⇒ bọc ngoặc; (b) ngữ cảnh khác min null (listEmployeeInfoHasPermission/ByPermissionAndDepartment, holdersAmong, `in_array('tên', $permissions)`, `'isShow' => [...]`, `return ['tên']` adapter) ⇒ đổi chuỗi + in ngữ cảnh để duyệt (bỏ qua bằng danh sách skip: `'Quản lý giải pháp'` làm nhãn fallback ở SolutionMemberService); (c) tên có phạm vi ngoài lời gọi ⇒ MANUAL. Bẫy: thụt lề dòng chèn phải tính bằng cách ghép token lùi tới `\n` (token comment `// …\n` đứng trước làm mất thụt lề).
- **checkPermissionList[WithColumn] mảng tên** (BOM List, giải pháp, báo cáo hiệu suất GP, bàn giao) ⇒ dùng lại `PresaleViewScope::apply/applyWithColumn` (cùng module Assign, chép nguyên helper). Thêm tham số `$lowestScope` (mặc định PART) cho `applyWithColumn`: bàn giao truyền `[3 tên, null, true]` (vị trí bộ phận trống ⇒ helper bỏ nhánh) ⇒ `lowestScope = DEPARTMENT`, phạm vi 1 (nếu có) rơi về nhánh created_by như cũ (mã chỉ cho phép 2–4 nhưng checker không kẹp phạm vi).
- **Mảng `$permissions` tên cho `AssignRequest::can*($permissions)`** (AssignBusinessListResource, MyJobAssignBusinessResource: `Employee::firstOrNew(...)->getAllPermissions()->pluck('name')`) ⇒ `array_keys(CurrentPermission::map())` như training; mọi tên Entity so là min null. `count($permissions) == 0` ⇒ đi cửa chung — cùng kết quả.
- **Override** AssignBusinessService / JobRequestService ⇒ thân `CurrentPermission::has`. DashboardService "công việc chờ duyệt": isShow mang mã + so `array_keys(CurrentPermission::map())` thay `getAllCurrentPermission()`.
- **Không đổi**: `checkDueConfigsManager:Duyệt hồ sơ thanh toán` (PaymentProfile route) là TÊN HÀNH ĐỘNG gửi ERP `due-configs/check-manager-block`, không phải quyền. `components/assign-components/assign-slidebar.vue` (layout `assign` không page nào dùng — code chết).
- **FE**: `this.permissions[i].name == 'tên'` (5 trang timesheet jobassignment/business_trip_assigns, `state.permissions`) ⇒ `return this.hasAPermission('mã')` (mixin toàn cục). Menu: menu-sidebar.js (hub), master-data.js (hub), presale.js, menu.js (Topbar) thêm `codes` cạnh isShow; sale.js thêm 3 link vào `SALE_LINK_CODES`.
- **Bẫy test**: thêm `'assign'` vào `adoptCatalogCodes()`; `tests/Feature/EmployeeWorkPerformance/ReportApiTest` ca "không quyền" không cấp gì ⇒ gọi `adoptCatalogCodes()` trong setUp (thiếu ⇒ UnknownPermissionCode bị controller nuốt thành 400). Middleware nhiều mã dùng chung (general-regulations) ⇒ test phân hệ khác gọi route đó (PayrollScopeCodesTest) phải `ensureCode` mã assign. **Không chạy 2 lớp phpunit song song** trên `hrm_erp_rbac_test`: dòng `ZZADOPT catalog …` của lớp kia làm PermissionMergerTest đỏ giả.
- **Bẫy mốc**: `assign/my-job/assign-business-list` 55–59 s/ô — bỏ khỏi mốc HTTP (gần ngưỡng 60 s sập php -S), phủ bằng PHPUnit. Nhiều route cần tham số (employee-work-performance `company_id`, task-manager-by-employees `from_date/to_date`).
- Không dùng DataScope: nhánh 2 = phòng ∪ bộ phận ∪ created_by ∪ id phiếu mình tham gia (AssignRequestEmployee/JobRequestEmployee…), nhánh không mã = created_by ∪ tham gia (DataScope `1 = 0`), nhánh 3 không ∪ bản thân, báo cáo nhánh không mã = `firm_employee_id`/`employee_info_id` ⇒ không khớp mode nào.

## customer_care (Task 8.13)
- Gần hết ở ERP (~50 file app + 30 blade + routes/web.php); hrm-api = module CustomerCare (4 Entity + 6 Service + 70 token middleware) + `Modules/Assign/Services/CustomerManagerService` (báo giá/hợp đồng dịch vụ trong màn khách hàng); hrm-client 9 trang danh mục CSKH + 2 menu. 67 mã (25 có phạm vi). Scanner sót ~140 hit (mảng tên `$permissions = ['is_all_company' => 'Tên…']` trong model, biến `$perm_all = 'Tên'`, `$permission = 'Tên'` truyền `Employee::permission`, `'permission' => 'Tên'` của partial `searchEmployee_v2`, hằng `PERM_*` ở Entity hrm-api, `PERM_MAP` CustomerManagerService) ⇒ grep tên alias Catalog có dấu phân cách.
- **Mảng tên 1 mã trong model** (7 model + CustomerCareReportService ×2): script `scratchpad/cc/arr.py` bỏ mảng, đọc `$<ma>Scope` ngay trước lần `can($permissions['is_*'])` đầu (trong nhánh `type == 'all'`, kể cả trong closure — bỏ `use ($permissions)`), mỗi khoá → `>= mức min_scope của tên`.
- **Mảng/biến tên theo loại chứng từ** (WrServiceContract 4 loại, WrAssignTask phiếu giao việc/duyệt kết quả, WrServiceQuotation CCTT/báo giá): nhánh khai `$viewCode = 'mã'`, đọc `$viewScope` 1 lần ở chỗ `can()` đầu tiên chạy. Loại lạ: cũ "Undefined variable/index" ⇒ mới "Undefined variable $viewCode" / TypeError (`$viewCode = null`) — vẫn lỗi như cũ.
- **`hasAnyPermission([tên có phạm vi, mã khác…])`** (ServiceExportRequest ×4 + show.blade): tách `(permissionScope(mã) >= COMPANY || hasAnyPermission([phần còn lại]))`. `hasAnyPermission([tên 4, tên 3, …])` cùng mã (báo cáo báo giá) ⇒ `scope >= mức thấp nhất danh sách`.
- **Partial dùng chung** `partials/classes/base/Datatable(SearchModal).blade.php` (cờ `this.is_big_boss = @json(can('Xem tất cả phiếu…'))` — mọi màn ERP dùng DATATABLE) và `FilterDepartmentHelper` (≈10 model kho/đơn hàng): tên thuộc customer_care (`customer_care.phieu.view`) ⇒ đổi; test ERP render màn bất kỳ nay cần dòng mã `customer_care.*` (seed `CustomerCareCatalog`). ScopeSnapshot không bắt cờ dạng `this.x = …` ⇒ golden render partial lấy cờ.
- **Override hrm-api `WarrantyRepairPermission::has`** (getAllPermissions + in_array tên) ⇒ thân `CurrentPermission::has` (nhận mã; tên sale "Xem hợp đồng ẩn giá" vẫn đi đường tên như cũ). 4 Entity: 3 hằng tên ⇒ 1 hằng mã (`PERM_VIEW`, `PERM_QT_VIEW`, `PERM_HD_VIEW`), `viewPermissions()` (mảng 3 tên) ⇒ `viewCode()`.
- **ErpPermissionHelper::userCan (guard web) ở hrm-api** nhận mã sẵn (employeeHasAt ⇒ checker); CustomerManagerService `PERM_MAP` loại wr ⇒ `'code' => mã` + `CurrentPermission::scope` (cùng người = employees.id, cùng current_company_role), loại firm (tên sale) giữ.
- Tên có phạm vi ở cửa holders (`sendNotifyWithPermission('Xem yêu cầu làm dịch vụ')` — min 3): `Employee::permission` không nhận min_scope cho mã ⇒ GIỮ tên (đổi sang mã sẽ thêm người nhận có mã ở phạm vi 1–2). Cần cửa holders(mã, minScope) — Task 12.
- `checkDueConfigsManager:Tạo phiếu giao việc` (routes/web.php) là tên hành động `due_configs`, không phải quyền — giữ (như 8.12).
- Golden ERP `CustomerCareScopeConversionTest`: 148 ca × 8 mức (searchByFilter builder, canView 3 biến thể phòng/công ty, trang/cờ, partial, báo cáo pretend). Bẫy: controller báo cáo thời gian chăm sóc bọc `catch → dd()` ⇒ gọi thẳng service; `HomeController::approveList` kiểm mã mọi phân hệ (admin…) chưa seed ở DB test ⇒ bỏ khỏi golden, phủ bằng mốc HTTP.
- Không dùng DataScope: nhánh 3 = `company_id` ∪/không ∪ `created_by` tuỳ màn, nhánh 2 = `employee_manage_departments` theo công ty (có màn cộng phòng đang làm, có màn `department_id = phòng mình`), nhánh không mã = `created_by` / người thực hiện / phòng tiếp nhận ⇒ không khớp mode nào.
