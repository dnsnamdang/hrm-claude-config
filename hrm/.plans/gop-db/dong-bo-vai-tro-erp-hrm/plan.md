# Plan — Đồng bộ vai trò ERP ↔ HRM

## Phase 0 — Rà soát (chờ user duyệt)
- [x] Đo hiện trạng prod + rà đường kiểm quyền 2 bên (design.md)
- [x] User duyệt 18 vai trò ERP đang mang quyền HRM → giữ nguyên
- [x] Super Admin trùng tên: không đổi tên (cách lưu theo guard không làm ERP thấy vai trò HRM) · được sửa ERP

## Phase 1 — HRM (hrm-api + hrm-client, nhánh gop_db)
- [x] Employee: erpRoles, permissionRoles, ghi đè getAllPermissions/getPermissionsViaRoles (chỉ api), grantRoles/revokeRoles/syncRolesInCompany/rolesInCompany
- [x] isCurrentEmployeeHasPermission (PermissionHelper + PermissionService), AuthNewController ×2: vai trò 2 bên + guard api
- [x] EmployeeService storeRole/snapshot/index (lọc vai trò), BulkPermissionService, EmployeeResource List/Detail (bỏ erp_roles)
- [x] FE màn Nhân viên: bỏ dòng "Vai trò gán từ ERP"

## Phase 2 — ERP (TanPhatDev, nhánh gop_db)
- [x] Employee::ROLE_MODEL_TYPES, syncRolesByCompany/syncDataByCompany đọc-xoá cả dòng HRM, vai trò api ghi dòng HRM, lịch sử display_name ?: name
- [x] EmployeesController@edit: option + vai trò đã chọn + công ty gồm cả vai trò HRM

## Phase 3 — Test
- [x] tinker rollback DB local: HRM 19/19, ERP 9/9
- [x] Chuẩn hoá (user chốt 22/10): migration `2026_10_22_000001_normalize_erp_roles_assigned_from_hrm` đổi dòng HRM của vai trò web → App\Employee, sao lưu bảng `bak_20261022_employee_has_roles_erp_from_hrm`; test local up/up lần 2/down khôi phục y nguyên
- [x] Migration bổ sung cách B (user chốt): tạo 8 vai trò "<tên> - HRM" giữ quyền HRM của 18 NV từng dùng quyền ERP trùng tên
- [x] Test 22/10: hồi quy local 8.730 cặp NV×cty (code = định nghĩa, 0 mất quyền api) · bản sao prod 633 NV: 0 mất quyền HRM, 0 đổi ô chuyển công ty, down() khớp checksum 4 bảng · HTTP HRM 35/35 · Playwright ERP 11/11 · Playwright HRM 11/11 · phpunit MasterData 26/26, Finance 17 fail có sẵn (giống hệt code gốc)
- [x] Commit/push gop_db: hrm-api d1705d101, hrm-client 2cfd94a2c, TanPhatDev d002aa5a00 · deploy 22/10: HRM build_tpe.sh (migration batch 430), ERP git pull erp-prod
- [x] Kiểm prod sau deploy: chuẩn hoá 38 dòng (16 đổi kiểu, 22 bỏ dòng thừa — có người gán thêm vai trò ERP từ HRM trước giờ deploy), 8 vai trò "- HRM"; dựng lại trạng thái cũ từ bảng sao lưu → 0/633 NV mất quyền HRM
- [ ] Lỗi có sẵn: màn Khảo sát đào tạo (TrainingSurveyController::getListEmployeeWithPermission) kiểm 3 tên quyền chỉ có ở ERP → 21 NV từng có phạm vi rộng nhờ lọt quyền ERP nay về "cá nhân"; chờ user chốt có đổi sang quyền HRM "Xem danh sách phiếu khảo sát đào tạo theo …" không

## Phase 4 — Test nhiều tài khoản 2 bên + deploy

## Phase 4 — Gộp 8 vai trò "- HRM" vào vai trò ERP gốc (user chốt cách E, 22/10)
- [x] Migration `2026_10_22_000003_merge_hrm_companion_roles_into_erp_roles`: tick quyền HRM vào vai trò gốc theo công ty, gán vai trò gốc (dòng ERP) ở mọi công ty áp dụng của vai trò "- HRM" cho người đang giữ, xoá vai trò "- HRM"; sao lưu `bak_20261022_merge_companion_roles`
- [x] `Employee::manageCompanyIds()` = company_roles vai trò HRM ∪ công ty dòng gán ERP; dùng ở AuthNew (ô chuyển công ty), listManageCompanyIdsForCurrentEmployee, checkPermissionListWithCompanyFilter, FilterByCompanyManagerScope
- [x] Mô phỏng bản sao prod: 0 mất quyền HRM, 0 thu hẹp công ty, +66 dòng gán ERP (26 NV, ~4.000 lượt quyền ERP), 63 NV thêm quyền HRM, 223 NV thêm công ty (30 thêm cty khác cty gốc); down() khớp checksum · local HTTP 40/40, ERP UI 11/11, HRM UI 11/11
- [x] Deploy 22/10 11:49 (af49c4f45)

## Fix 23/10 — ERP Sửa tài khoản báo "Phòng không tồn tại" (cob@tanphat.com)
- [x] ERP `EmployeesController::edit` lấy phòng quản lý thêm `whereNotNull('department_id')` — dòng "Quản lý tất cả phòng ban" do HRM ghi (department_id NULL, all_department=1) lọt vào form → Lưu gửi [null] → validate exists chặn; Lưu ERP không xoá dòng cờ HRM (syncDepartmentsByCompany so qua join departments)
- [x] Commit 26bb754cae, push gop_db, git pull erp-prod 23/10

## Phase 5 — Gỡ 66 lần gán ERP do gộp thêm ở công ty khác (user chốt cách 1, 23/10)
- [x] Migration `2026_10_23_000002_remove_erp_assignments_added_by_role_merge` (sao lưu `bak_20261023_removed_merge_assignments`, down() khôi phục) — mô phỏng prod: gỡ 66, 0 mất quyền HRM, 26 NV thu hẹp ô chuyển công ty (đã duyệt), down() khớp checksum · local HTTP 40/40, ERP 11/11, HRM 11/11
- [x] Sao lưu trước deploy: hrm-prod `~/backup/phanquyen_truoc_gopvaitro_b3_20261023_1721.sql.gz` + máy local `~/backup-hrm/` (4 bảng phân quyền + 3 bảng bak_), đã thử nạp lại khớp số dòng
- [x] Deploy 23/10 (35d97586e): đã gỡ 66 dòng, NV 1189 chỉ còn công ty 9 bên ERP
- [x] 23/10 sửa dữ liệu prod: vai trò 100005 "Kế toán bán hàng" mất 5 công ty áp dụng do người dùng bỏ ở màn Phân quyền HRM (lịch sử #145, 15:55) rồi tick lại quyền ở ERP /admin/roles (17:11) mà không thêm lại công ty → thêm lại company_roles 2,3,4,8,9 (sao lưu `bak_20261023_company_roles_100005`)
- [ ] Đề xuất (chờ user): ERP /admin/roles chặn tick quyền ở công ty không có trong ô Công ty; HRM màn Phân quyền hỏi xác nhận khi bỏ công ty (xoá luôn quyền công ty đó)

## Phase 6 — Khách báo "phân quyền rồi lại mất" (23/10)
- [x] Gốc: ERP /admin/roles Lưu → Role::syncPermissionsByCompany xoá mọi quyền không có trên form (form chỉ có quyền web) ⇒ xoá sạch quyền HRM. Sửa chỉ đồng bộ guard web (TanPhatDev 82ed80146f, deploy erp-prod). Test UI: code mới 4/4, code cũ đối chứng bắt được lỗi; chiều HRM lưu giữ quyền ERP 3/3
- [x] Khôi phục 340 quyền HRM từ lịch sử HRM: 100005 theo #139 (311), 100025 theo #130 (29); sao lưu `~/backup/rhp_100005_100025_truoc_khoiphuc_20261023_1918.sql.gz` (+ `~/backup-hrm/`), danh sách đã thêm ở `bak_20261023_restore_hrm_perms`
- [x] Rà rủi ro khác: permission:cleanup chỉ báo cáo; cache spatie không ảnh hưởng (ERP 0s, HRM tính trực tiếp DB); UpdateDB chạy tay
- [ ] Chờ user: (a) HRM màn Phân quyền hỏi xác nhận khi bỏ công ty (xoá quyền cả 2 bên ở công ty đó); (b) HRM chặn Xoá vai trò ERP (bỏ qua luật chặn xoá của ERP); (c) dữ liệu lệch: 100077 "Nhân viên nhân sự" có quyền ở cty 6 nhưng không áp dụng cty 6 → lần Lưu kế tiếp ở bất kỳ màn nào sẽ xoá
- [x] (a) Hỏi xác nhận khi bỏ công ty khỏi vai trò: HRM (timesheet/setting/roles + màn cũ human/roles) popup $confirm kèm số quyền HRM/ERP sẽ mất, Hủy trả lại công ty; BE RoleController::store chặn 422 nếu bỏ công ty còn quyền ERP mà thiếu confirmed_remove_company_ids (RoleService::unconfirmedErpCompanyRemovals); ERP /admin/roles popup swal (nạp sweetalert). Sửa thêm lỗi màn cũ human/roles handleEvent (= gán → tick 1 công ty ghi đè quyền mọi công ty). Test: ERP 5/5, HRM API+UI 9/9, màn cũ code cũ FAIL/code mới PASS, hồi quy 40+11+11+4+3 PASS
- [x] Deploy 24/10: hrm-api 175d967f3, hrm-client 29ad6646b (build xong), TanPhatDev 8f68946372 (+ view:clear). Kiểm prod chỉ đọc: chốt chặn BE trả đúng công ty chưa xác nhận; bundle FE 2 màn có code mới
- [ ] Còn chờ user: (b) chặn Xoá vai trò ERP ở HRM; (c) vai trò 100077 có quyền cty 6 ngoài DS áp dụng
