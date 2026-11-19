# Việc ngoài luồng — Vai trò & Quyền

> Lỗi/thiếu sót CÓ SẴN phát hiện trong lúc làm phân quyền mới, không thuộc phạm vi đợt đang làm. Theo quy ước: ghi lại, sửa
> tại chức năng đó sau, rà hết danh sách trước khi merge prod. Gom 03/11/2026 từ checkpoint `gd3b-doi-vai-tro-sang-ma/plan.md`
> và ledger SDD (`wt-rbac/hrm-api/.superpowers/sdd/plan-gd3b-doi-vai-tro-sang-ma/progress.md`).

| # | Nơi | Vấn đề | Phát hiện | Trạng thái |
|---|---|---|---|---|
| 1 | ~~TPE_APP mục "Duyệt đề nghị thanh toán công tác phí"~~ | ~~Không bao giờ hiện~~ — **đính chính 03/11: KHÔNG phải lỗi.** Cả 2 chỗ nằm sau `env.isThanhAnGroup` (chỉ bản Thành An, backend riêng); hrm-api TPE không có API `working-fee` | 03/11 | Đóng |
| 2 | TPE_APP `filter_org_scope.dart` | Ô lọc tổ chức lọc phòng ban theo `currentUser.companyId` (công ty hồ sơ), quyền tính theo công ty đang làm ⇒ lệch với NV làm khác công ty hồ sơ (rehearsal: 1 NV) | 03/11 | Mở |
| 3 | ERP `WarrantyReport::searchByFilter` | Danh sách báo cáo bảo hành 500 khi không có mã (`whereHas('employees')` không có quan hệ) | Task 12 | **Đã sửa 03/11** (`b4f666abe1`): mình tạo + việc được giao |
| 4 | ERP `HomeController::saleByYear` | Nhánh Công ty lọc nhầm `$quotations` ⇒ hợp đồng mọi công ty | Task 5 | **Đã sửa 03/11** (`b4f666abe1`) |
| 5 | ERP `reports/marketAnalysisLocation` (+ marketAnalysis) | Khối ô lọc nằm trong comment HTML ⇒ không ai thấy; `:83` còn `isRole` (giữ, không phải kiểm quyền) | Task 5, 12 | Mở |
| 6 | ERP `/admin/quotations/searchData` | Lỗi 1054 `q.payed_cost` trên rehearsal (lệch schema) | Task 12 | Mở — kiểm migration trước khi sửa code |
| 7 | ERP `department-filter` (partial) | Không view nào include | Task 5, 12 | Mở |
| 8 | ERP `employee_infos/create` | Controller trả "không có quyền"/not_found ngay đầu hàm với mọi tài khoản | Task 5, 12 | Mở |
| 9 | ERP `Team::searchByFilter` | Select `teams.status` không có cột + `company_id` mơ hồ | Task 5 | Mở |
| 10 | ERP 6 job mail báo cáo vận chuyển | Nhận `$userIsBoss` nhưng không đọc | Task 5 | Mở |
| 11 | ERP `CustomerCareBill` / `CustomerCareQuestion` / `DeviceError` `searchByFilter` | Trang "Tất cả" phạm vi 3 không lọc công ty ⇒ thấy mọi công ty | Task 1b | Mở |
| 12 | hrm-api `PrepickTrackingScope` | `ownCompanyId = info->company_id` (công ty hồ sơ — hrm-api không có accessor session) trong khi FE dùng `company_role` | Task 1b | Mở |
| 13 | ERP `WarehouseReportsController:1323/1327`, `Product:3626`, `ProductTemplate:3129` | Tên quyền 2023 không có bí danh (`legacy_or_unknown`) ⇒ kiểm theo tên không tra được mã | Task 12 | Mở — tồn GĐ3 |
| 14 | hrm-client training dashboard | Layout đã lưu không lọc theo quyền; `currentEmployee()` chết | Task 4 | Mở |
| 15 | Môi trường dev | `vendor/composer/autoload_classmap.php` ở checkout ERP chính (08/2025) còn `RolesController` đã xoá ⇒ `ErpGateSideEffectsTest` lỗi; DB test `hrm_erp_rbac_test` thiếu bảng `inherited_price_factors` (migration Kế thừa giá đợt 2) ⇒ 1 test hrm-api đỏ | Task 11 (03/11) | Mở — môi trường, không phải code; deploy `composer install` sinh lại classmap |

Góp ý nhỏ của final review GĐ3b (M1–M9): `wt-rbac/hrm-api/.superpowers/sdd/plan-gd3b-doi-vai-tro-sang-ma/final-review.md`.

## 04/11 (diễn tập dump prod 03/11)
- hrm-api kiểm 5 tên quyền không tồn tại trong DB prod (luôn false, có sẵn trước rbac): "Quản lý danh mục khách hàng" (Assign CustomerController:43),
  "Xem danh sách hạng mục dự án theo …" (SolutionModuleService:102–117), "Xem danh sách loại HĐLĐ theo …" (LaborContractTypeController:31),
  "Duyệt thông báo nội bộ" (SelfNotifications:87), "Quản lý thân nhân" (EmployeeController:208).
- Prod sinh tên quyền guard `api` mới theo mỗi lần deploy gop_db ⇒ sáng G phải dò lại tên DB vs legacy Catalog trước dry-run.

## 06/11 (go-live)
- Code origin mới còn nhánh Super Admin: `WarrantyRepairPermission::isSuperAdmin` (6 service CustomerCare/Assign), `ServiceAccounting::isSuperAdmin`, `WrAccountingService::isSuperAdmin`. Không chặn vì Super Admin có đủ mã, nhưng trái nguyên tắc bỏ đặc quyền.
- `.tp-card` không có trong CSS toàn cục: 47 page dùng, mới đo 5 màn admin. Page nào không nạp `V2BaseSmartFilterPanel` sẽ mất style khi F5 trên bản build.
- Route mới của origin còn ghi tên quyền cũ ⇒ 2 ca test đỏ (`CustomerCareScopeCodesTest`, `SaleScopeConversionTest`); chạy đúng qua alias.
- Golden ERP cần chụp lại theo nghiệp vụ mới: `service_accounting_request.all`, `approveList`.
- `server_node` ERP chạy nohup, không có trình quản lý, VPS khởi động lại sẽ không tự lên.

## 07/11 (sau go-live)
- [x] Fix: xoá vai trò trên prod báo 500 ("Thủ kho 1"). `RoleManagementService::destroy()` không dọn `company_roles` (khoá ngoại NO ACTION). Đã sửa local gop_db + ca `test_xoa_vai_tro_co_dong_company_roles_thi_duoc_va_don_dong_nay`; chưa commit.
- Chưa kiểm xong: `RoleManagementService::store()` không ghi `company_roles`, mà `Modules/Timesheet/Services/RoleService::index` join bảng này ⇒ vai trò tạo sau go-live có thể không hiện ở chỗ dùng danh sách đó.
- [x] Màn Phân quyền: tiêu đề phân hệ/chức năng hiện "Đã cấp x/y"; chọn hết thì nút thành "Đã chọn cả" (primary, bấm không đổi gì — ngoại lệ quy tắc ẩn nút, user chốt 07/11). Sửa `PermissionTree.vue`, thêm ca e2e `admin-roles.spec.ts`; chưa commit, ca e2e chưa chạy.
- [x] Màn Vai trò nhân viên: hiện mặc định cột Trạng thái tài khoản; tài khoản `status <> 1` (user chốt 07/11, gồm cả status 3) ẩn Sửa + link Mã NV, URL thẳng về danh sách, PUT 423 (middleware `employeeAccountNotLocked`). Chưa commit; ca e2e chưa chạy. Lưu ý: 481 NV không hoạt động còn giữ 521 lượt vai trò (local), muốn gỡ phải mở khoá trước.
- [x] Màn Vai trò: vai trò đang được chứng từ dùng thì ẩn Xóa (`markReferenced` gom theo cột, chỉ dò dòng đang hoạt động + 0 người giữ), câu báo dùng tên màn (`role_id_labels` trong role-references.php). Chưa commit.
- Chưa xử lý: `RawPermissionLookupGuardTest` đỏ 81 dòng ở file khác (Super Admin + code origin), không dính việc này.
