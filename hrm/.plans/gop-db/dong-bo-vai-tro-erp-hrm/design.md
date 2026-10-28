# Đồng bộ vai trò ERP ↔ HRM (1 ô gán dùng chung) — @cuong61n

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-22-dong-bo-vai-tro-erp-hrm-design.md`

## Mục tiêu
Gán vai trò cho nhân viên ở ERP hay HRM đều là MỘT lần gán, hiệu lực cả 2 hệ; gỡ ở bên nào cũng gỡ cả 2.
Mỗi hệ chỉ đếm quyền của guard mình (HRM = `api`, ERP = `web`).

## Hiện trạng (đo prod hrm_erp_gop 22/10/2026)
- `employee_has_roles` tách theo `model_type`: ERP `App\Employee` 1.351 dòng / 1.025 NV; HRM `Modules\Timesheet\Entities\Employee` 502 dòng / 366 NV / 54 vai trò. Chỉ 2 cặp gán trùng.
- HRM kiểm quyền (middleware `checkPermission`, `PermissionService`/`BaseModel::isCurrentEmployeeHasPermission`, `AuthNewController`) gom theo TÊN, KHÔNG lọc guard.
- ERP: spatie 3.18, `can()` resolve quyền theo tên + guard `web` (quyền api không lọt), NHƯNG `Gate::before` → `hasRole('Super Admin')` so TÊN không so guard.
- ERP màn Nhân viên: select vai trò chỉ liệt kê guard `web`; `Employee::syncRolesByCompany` xoá mọi vai trò `App\Employee` không có trong payload.
- 18 vai trò ERP đang mang quyền HRM (api); 0 vai trò HRM mang quyền ERP.

## Quyết định đã chốt (22/10/2026, user)
- 1 ô gán duy nhất, đồng bộ 2 chiều (gán/gỡ ở đâu cũng áp cả 2 bên).
- Được sửa hàm kiểm quyền dùng chung; rà danh sách vai trò ERP mang quyền HRM TRƯỚC khi bật.
- 18 vai trò ERP đang mang quyền HRM: GIỮ NGUYÊN (user 22/10).
- "Super Admin"/"Admin" trùng tên: KHÔNG đổi tên vai trò nào — ghi đè `App\Employee::hasRole` bên ERP để so theo tên chỉ tính guard `web` (+ sửa `Employee.php:1382`). Lý do: đổi tên ERP phải sửa ~20 chỗ ERP + chỗ HRM port, sót = 23 Super Admin mất quyền.
- Màn Nhân viên ERP: select vai trò hiện CẢ vai trò HRM (guard api) để Lưu không xoá mất.
- Thứ tự deploy: ERP trước (vô hại khi chưa chuyển dữ liệu) → HRM (migration chuyển dòng gán).

## Rủi ro phải xử lý trước khi bật
1. HRM chỉ đếm guard `api` (nếu không: 783 NV nhận quyền HRM ngầm qua 145 tên trùng).
2. Vai trò HRM "Super Admin" (100125, 4 NV) thành dòng chung → ERP `hasRole('Super Admin')` = toàn quyền ERP. Cần đổi tên vai trò HRM hoặc sửa Gate::before ERP so cả guard.
3. ERP lưu Nhân viên sẽ xoá vai trò HRM (select chỉ có guard web) → sửa ERP giữ nguyên vai trò khác guard.
4. Không dùng morphMap toàn cục (đổi model_type mọi quan hệ morph của Employee HRM) → chỉ đổi quan hệ roles.
5. Chuyển 502 dòng HRM → `App\Employee` (gộp trùng), có backup + rollback.

## Cách làm đã chọn (22/10/2026) — thay cho "chuyển hết về 1 model_type"
Audit ERP: chuyển dòng HRM sang `App\Employee` làm vai trò HRM lọt vào ~60 chỗ ERP đọc `$employee->roles`
(chức vụ người duyệt/ký, in `roles[0]`, JWT, "Chờ phân quyền"…). Đổi sang:
- **Vai trò lưu theo guard**: web ↔ dòng `App\Employee`, api ↔ dòng `Modules\Timesheet\Entities\Employee`. Không chuyển dữ liệu.
- **HRM tính quyền** từ cả 2 loại dòng (`Employee::permissionRoles()` — dòng ERP chỉ tính ở đúng công ty được gán), CHỈ đếm quyền guard api (`getAllPermissions`/`getPermissionsViaRoles` ghi đè, `isCurrentEmployeeHasPermission` ×2, `AuthNewController` ×2).
- **Phạm vi công ty/dữ liệu** (roles → company_roles) vẫn chỉ đọc vai trò HRM như cũ — không nới phạm vi dữ liệu.
- **Màn Nhân viên 2 bên**: 1 ô gồm cả 2 loại; thêm/gỡ ghi/xoá đúng loại dòng (HRM: `Employee::syncRolesInCompany/grantRoles/revokeRoles`, chỉ công ty gốc; ERP: `syncRolesByCompany`/`syncDataByCompany` + EmployeesController@edit).
- ERP `roles()`/`hasRole` KHÔNG đổi → không cần ghi đè hasRole (Super Admin HRM không thành Super Admin ERP — đã test).
- Thứ tự deploy: không phụ thuộc nhau.

## Tác động đã đo trên prod
- 2 NV (212, 1191) mất phạm vi rộng màn Khảo sát đào tạo — đang có nhờ quyền ERP trùng tên lọt sang (đúng là phải mất).
- 21 dòng (18 NV, 8 vai trò ERP) được gán từ HRM theo kiểu dòng HRM → ERP chưa tính. → User chốt CHUẨN HOÁ (migration 2026_10_22_000001). Quyền của vai trò vẫn tick riêng mỗi bên (ERP /admin/roles = web, HRM Phân quyền = api); chỉ phần gán vai trò là chung.
