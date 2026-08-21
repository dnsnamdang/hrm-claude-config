# Plan — Chuyển quyền Quản lý khách hàng sang phân hệ Danh mục chung

Phụ trách: @khoipv — nhánh `gop_db` (hrm-api). FE không đụng.
Chốt 2026-08-20: làm HẾT trong `PermissionsTableSeeder`, KHÔNG viết migration.

## Phase 1 — Dọn nhóm quyền khách hàng ở phân hệ Hành chính nhân sự

- [x] P1.1 Rà 166-169 xem quyền nào thật sự chết (grep `hrm-api` + `hrm-client`)
- [x] P1.2 Phát hiện 167 KHÔNG chết: tên trùng nguyên văn quyền ERP 100170, mà `ErpPermissionHelper`
      so theo `name` không lọc guard → 14 dòng gán vẫn đang có hiệu lực
- [x] P1.3 Xóa 4 dòng `Permission::create` id 166-169 (nhóm `Danh mục khách hàng`) khỏi seeder

## Phase 2 — Khai 11 quyền KH ở phân hệ Danh mục chung (type 9)

- [x] P2.1 Khai 11 dòng `Permission::create` ở cuối `run()`: id 1517-1526 + **167 giữ lại**,
      `group => 'Quản lý khách hàng'`, `type => 9`, `sort_order => 1..11`, tên NGUYÊN VĂN của ERP
- [x] P2.3 Gỡ bỏ migration đã viết ở lần làm trước (xóa file + xóa bản ghi trong bảng `migrations`)
- [x] P2.4 Khôi phục 14 dòng gán của quyền 167 mà migration cũ đã xóa nhầm (lấy từ file snapshot)

## Phase 3 — Kiểm chứng

- [x] P3.1 `php -l` sạch; `PermissionService::getLists()` trả đúng 11 quyền `type=9` theo đúng `sort_order`
- [x] P3.2 `permissions` còn 0 dòng 166/168/169 và 0 dòng nhóm `Danh mục khách hàng`
- [x] P3.3 Xác nhận helper bắt cả 2 guard: `Xem khách hàng` → id [1517, 100057] / 64 role;
      `Xem tất cả khách hàng` → id [167, 100170] / 32 role
- [x] P3.4 Trả 11 quyền ERP `guard=web` về `type = NULL` (cách làm mới không đụng tới chúng)
- [ ] P3.5 User mở màn Thiết lập → Phân quyền, xác nhận tab "Danh mục chung" có nhóm "Quản lý khách hàng"
      với 11 checkbox và tab "Hành chính nhân sự" không còn nhóm "Danh mục khách hàng"

### Checkpoint — 2026-08-20 18:35
Vừa hoàn thành: toàn bộ Phase 1-2 và P3.1-P3.4. Đã đổi cách làm 3 lần theo yêu cầu user: bỏ migration,
khai quyền bằng `Permission::create` thường thay vì `UPDATE` qua method riêng, rồi bỏ nốt khối dọn
pivot và khai báo `GROUP_ORDER` thừa để `run()` chỉ thuần khai quyền như các phân hệ khác.
Chỉ còn đụng 1 file: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
Đang làm dở: không có.
Bước tiếp theo: P3.5 — user mở trình duyệt xác nhận 2 tab.
Blocked: seeder có sẵn lỗi trùng id 1117/1118 (dòng ~1130-1131) → chạy seeder thật sẽ crash TRƯỚC khi
tới 11 quyền mới ở cuối file. Cần user quyết có bỏ 1 cặp không (quyền dùng chung, theo CLAUDE.md phải hỏi).

## Phase 4 — Fix khối quyền không hiện trên màn Phân quyền (2026-08-21)

Triệu chứng user báo: đã khai 11 quyền, DB có đủ, nhưng vào Phân quyền → "Danh mục chung"
KHÔNG thấy nhóm "Quản lý khách hàng".

- [x] P4.1 Khoanh vùng: DB có đủ 11 quyền `type=9 guard=api`; `PermissionService::getLists()`
      cũng trả về đủ → lỗi nằm ở khâu hiển thị, không phải khâu khai quyền
- [x] P4.2 Tìm ra nguyên nhân: `components/setting/Permission.vue:138` gộp quyền **chỉ theo tên
      `group`, bỏ qua `type`**. `getLists()` không lọc guard nên 11 quyền ERP `guard=web`
      `type=NULL` cùng tên group `Quản lý khách hàng` được sort lên trước (NULL < 9) → khối được
      tạo với `type=NULL`, 11 quyền `type=9` bị nhét chung vào đó → `filterPermission(9)` rỗng,
      mà `type=NULL` không phân hệ nào khai `permissionType` nên khối biến mất khỏi màn
- [x] P4.3 Quét toàn bảng: đúng **2** nhóm bị đè kiểu này (`Quản lý khách hàng` type 9 và
      `Quản lý quyết toán hợp đồng` type 4); trong riêng guard `api` không có nhóm nào 2 type
- [x] P4.4 User chốt: dùng bộ quyền mới bên HRM → `PermissionService::getLists()` lọc
      `guard_name = 'api'` (bỏ 965 quyền ERP `web` khỏi payload màn Phân quyền)
- [x] P4.5 Xác nhận không mất gán quyền cũ: `RoleDetailResource` vẫn trả đủ `permission_ids`
      của role (kể cả id guard `web`) nên chúng nằm trong v-model và `syncPermissionsByCompany`
      chỉ xóa id có trong danh sách cũ mà KHÔNG có trong danh sách gửi lên → id `web` được giữ
- [x] P4.6 Kiểm chứng: `getLists()` trả 680 quyền, 0 quyền guard ≠ api; mô phỏng thuật toán gộp
      của FE → `Quản lý khách hàng` ra `type=9` đủ 11 quyền đúng `sort_order`,
      `Quản lý quyết toán hợp đồng` ra `type=4` đủ 6 quyền

### Checkpoint — 2026-08-21
Vừa hoàn thành: P4.1-P4.6. Sửa 1 file: `Modules/Timesheet/Services/PermissionService.php`
(thêm `->where('guard_name', 'api')` + PHPDoc giải thích bẫy gộp theo tên group).
Đang làm dở: không có.
Bước tiếp theo: user hard-refresh màn Thiết lập → Phân quyền, xác nhận khối "Danh mục chung"
có nhóm "Quản lý khách hàng" 11 checkbox.
Blocked: (vẫn tồn tại từ trước, chưa đụng) seeder trùng id 1117/1118 → chạy seeder thật sẽ crash.

## Phase 5 — Màn Khách hàng chuyển sang dùng bộ quyền HRM (2026-08-21)

Yêu cầu user: màn danh sách khách hàng dùng **bộ quyền mới bên HRM** (guard `api`, type 9)
cho TẤT CẢ thao tác — xem / thêm / sửa / xóa / xuất / lịch sử / cấp xem theo tổ chức,
thay cho cơ chế `erpPermission` (tra bảng quyền ERP theo tên, không phân biệt guard).

- [x] P5.1 Khảo sát cơ chế hiện tại: middleware `erpPermission` → `ErpPermissionHelper::userCan()`
      (tra `permissions` theo `name` KHÔNG lọc guard, employee = ERP `employees.id` map qua
      `employee_info_id`) vs cơ chế HRM `checkPermission` / `isCurrentEmployeeHasPermission()`
- [x] P5.2 Đo mức độ ảnh hưởng: đếm role đang gán quyền bản `api` vs bản `web`
- [x] P5.3 Viết `App\Helpers\CustomerPermissionHelper` — kiểm quyền theo cơ chế HRM
      (role HRM của employee + `role_has_permissions.company_id = current_company_role`
      + `permissions.guard_name = 'api'`), cache theo request
- [x] P5.4 Đổi 30 route `erpPermission:*` → `checkPermission:*` trong `Modules/Assign/Routes/api.php`
- [x] P5.5 `CustomerController::myPermissions()` trả quyền theo helper mới, bổ sung đủ 11 cờ
      (thêm `history`, `registered`)
- [x] P5.6 `CustomerService`: 5 chỗ kiểm quyền (`Xem khách hàng` + 4 cấp xem tổ chức) đổi sang
      helper mới; GIỮ NGUYÊN `ErpPermissionHelper::erpEmployeeId()` ở các chỗ dùng làm ĐỊNH DANH
      (`created_by`), vì `customers.created_by` lưu ERP employee id
- [x] P5.7 FE `pages/assign/customers/index.vue`: thêm cờ `history` (fail-closed) gate nút "Lịch sử",
      cập nhật chú thích "quyền ERP" → "quyền HRM"
- [x] P5.8 FE `middleware/checkCustomerPermission.js`: cập nhật chú thích
- [x] P5.9 Kiểm chứng: `php -l` sạch, không còn `erpPermission` ở nhóm route customers,
      compile FE, đối chiếu số quyền helper trả về

### Checkpoint — 2026-08-21 (Phase 5)
Vừa hoàn thành: toàn bộ P5.1-P5.9. Màn Khách hàng đã chạy hoàn toàn bằng bộ quyền HRM.

File đã sửa — `hrm-api`:
- `app/Helpers/CustomerPermissionHelper.php` (MỚI) — kiểm quyền theo cơ chế HRM
- `Modules/Assign/Routes/api.php` — 30 route `erpPermission:` → `checkPermission:`
- `Modules/Assign/Http/Controllers/Api/V1/CustomerController.php` — `myPermissions()` trả 11 cờ
- `Modules/Assign/Services/CustomerService.php` — 5 chỗ kiểm quyền + đổi tên
  `applyErpVisibilityScope` → `applyVisibilityScope`
- `Modules/CustomerCare/Services/WarrantyRepairRequestService.php` — chú thích

File đã sửa — `hrm-client`:
- `pages/assign/customers/index.vue` — cờ `history` (fail-closed) gate nút "Lịch sử"
- `components/assign-components/customer/CustomerForm.vue` — `canViewErpCustomer` →
  `canViewCustomer`, `loadErpViewPermission` → `loadCustomerPermission`
- `middleware/checkCustomerPermission.js` — chú thích

Kiểm chứng đã chạy: `php -l` sạch 5 file; template + script FE parse sạch;
smoke test HTTP kernel với JWT thật (employee 13 / role 18):
- `GET my-permissions` → 200, đủ 11 cờ
- `GET export-csv` → 403 (role 18 CHƯA có quyền api 1522)
- cấp thử 1517+1522 trong transaction → `view=true export=true`, `export-csv` → 200,
  rollback xong DB còn 0 dòng (đã verify)

Đang làm dở: không có.
Bước tiếp theo: **user phải cấp lại quyền cho các role trên màn Phân quyền** — xem mục
Blocked bên dưới, không cấp thì màn Khách hàng mất hết nút với mọi tài khoản.
Blocked: bộ quyền HRM (guard `api`) hiện gần như CHƯA gán cho role nào — chỉ id 167
(`Xem tất cả khách hàng`) có 14 role. 10 quyền còn lại: **0 role**. Toàn bộ gán thực tế đang
nằm ở bản ERP guard `web` (Xem 64 role / Thêm 49 / Sửa 14 / Xóa 4 / Xuất 24 / Lịch sử 19).

## Phase 6 — Dùng hàm chung `checkPermissionList()` cho 4 cấp xem (2026-08-21)

User chỉ ra: `app/Helper/PermissionHelper.php` đã có sẵn hàm chung cho phân quyền theo cấp
(`checkPermissionList()` — 80 màn đang dùng), sao màn KH tự viết logic riêng.

- [x] P6.1 Rà hàm chung: `checkPermissionList($query, [tổng_cty, cty, phòng, bộ_phận, own], $table)`
      + `isCurrentEmployeeHasPermission()` (727 chỗ dùng)
- [x] P6.2 Đo dữ liệu 3 cột tổ chức của `customers`: 22 / 52 / 3 có giá trị trên **43.522** dòng
      → báo cáo user rủi ro thu hẹp phạm vi. **User chốt: vẫn chuyển sang `checkPermissionList()`**
- [x] P6.3 Viết lại `CustomerService::applyVisibilityScope()` dùng `checkPermissionList()`,
      GIỮ nguyên các nhánh OR đặc thù (KH mình tạo / mình đăng ký - tương tác / SĐT khớp đúng /
      popup `all_business`)
- [x] P6.4 Bắt bug ghép hàm: cấp "Xem tất cả khách hàng" làm `checkPermissionList()` trả query
      KHÔNG thêm điều kiện, mà closure rỗng thì Laravel bỏ luôn nhánh `orWhere` → thành ra lọc mất
      thay vì mở hết (đo được 196/43.522 KH). Sửa bằng early return trước khi bọc closure,
      truyền `null` vào `$permissions[0]`
- [x] P6.5 `CustomerPermissionHelper` bỏ tự query + bỏ lọc `guard_name = 'api'`, chuyển sang gọi
      hàm chung `isCurrentEmployeeHasPermission()` — đúng hàm mà `checkPermissionList()` dùng bên
      trong, để cả màn chỉ có MỘT chuẩn kiểm quyền. Giữ memo theo request để 11 quyền không bắn
      11 query
- [x] P6.6 Kiểm chứng bằng dữ liệu thật (xem checkpoint)

### Checkpoint — 2026-08-21 (Phase 6)
Vừa hoàn thành: P6.1-P6.6. File sửa: `Modules/Assign/Services/CustomerService.php`,
`app/Helpers/CustomerPermissionHelper.php`.

Kiểm chứng (employee 13, công ty 1):
- Có `Xem tất cả khách hàng` → thấy **43.522/43.522** KH (đúng, sau khi sửa bug P6.4)
- Chỉ có cấp **công ty** (mô phỏng trong transaction rồi rollback):
  logic MỚI **200 KH** vs logic CŨ (suy phạm vi qua báo giá) **7.622 KH**
- `GET my-permissions` → 200, đủ 11 cờ; `GET /assign/customers` → 200

Đang làm dở: không có.
Bước tiếp theo: user xác nhận trên trình duyệt.
Blocked: 2 việc chờ user quyết —
1. Cấp lại quyền cho role trên màn Phân quyền (bộ quyền `api` gần như chưa gán cho role nào).
2. Phạm vi cấp công ty/phòng ban/bộ phận thu hẹp mạnh vì `customers.company_id/department_id/part_id`
   gần như rỗng. Muốn khôi phục thì phải backfill 3 cột này (sửa dữ liệu nghiệp vụ — cần user duyệt).

## Phase 7 — Ẩn lối vào chi tiết/Quản lý khi thiếu quyền "Xem khách hàng" (2026-08-21)

User phát hiện: nút **Quản lý** vẫn hiện dù tài khoản không có quyền xem, bấm vào chỉ ra trang
rỗng (BE trả 403).

- [x] P7.1 Xác nhận bằng API: thiếu `Xem khách hàng` thì `GET /assign/customers/{id}` → **403**
      (do `CustomerService::isVisible()`) và `GET /assign/customers/{id}/equipment` → **403**
      (middleware `checkPermission`) → 2 màn chi tiết + Quản lý đều vô dụng
- [x] P7.2 `pages/assign/customers/index.vue`: thêm computed `canView`; gate `visible` cho hành
      động **Quản lý**; ô **Mã KH** chỉ render `nuxt-link` khi có quyền, không thì để chữ thường
- [x] P7.3 `middleware/checkCustomerPermission.js`: chặn luôn truy cập thẳng URL màn chi tiết
      `/assign/customers/{id}` và `/assign/customers/{id}/manager` khi thiếu `view`
      (middleware vốn đã được khai ở cả 5 page nên không phải sửa page nào)
- [x] P7.4 Bắt bug regex: `^/assign/customers/[^/]+$` khớp luôn `/assign/customers/add` → người
      có quyền Thêm nhưng không có quyền Xem sẽ bị đá khỏi màn tạo mới. Thêm `!path.endsWith('/add')`
- [x] P7.5 Kiểm chứng: bảng route 5 đường dẫn phân loại đúng; template + script parse sạch

### Checkpoint — 2026-08-21 (Phase 7)
Vừa hoàn thành: P7.1-P7.5. File sửa: `pages/assign/customers/index.vue`,
`middleware/checkCustomerPermission.js`.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt xác nhận nút Quản lý ẩn khi chưa cấp quyền.
Blocked: (giữ nguyên từ Phase 5-6) cấp lại quyền cho role; quyết định có backfill 3 cột tổ chức
của `customers` không.

**Còn tồn đọng, CHƯA sửa (chờ user quyết):** hành động **Sửa** mới chỉ gate bằng `Sửa khách hàng`.
Tài khoản có `Sửa` mà không có `Xem` sẽ vào được `/edit` rồi form trắng (vì `show` 403). Trên thực
tế đây là cấu hình quyền sai, nhưng muốn chắc thì đổi thành `canEdit && canView`.
