use Illuminate\Support\Facades\DB;
$c1 = DB::selectOne("SELECT COUNT(*) c FROM employees e JOIN employee_infos ei ON ei.id=e.employee_info_id LEFT JOIN company_employees ce ON ce.employee_id=e.id AND ce.company_id=ei.company_id WHERE e.status=1 AND ei.company_id IS NOT NULL AND ce.id IS NULL")->c;
echo "1 thieu company_employees: $c1\n";
if ($c1 != 0) { echo "DUNG: khac 0\n"; return; }
$rows = DB::select("SELECT ehr.*, r.name AS role_name, c.code AS company_code, e.id IS NOT NULL AS con_tai_khoan FROM employee_has_roles ehr LEFT JOIN company_employees ce ON ce.employee_id=ehr.employee_id AND ce.company_id=ehr.company_id LEFT JOIN roles r ON r.id=ehr.role_id LEFT JOIN companies c ON c.id=ehr.company_id LEFT JOIN employees e ON e.id=ehr.employee_id WHERE ce.id IS NULL");
file_put_contents(storage_path('app/rbac-convert/golive/employee-has-roles-mo-coi.json'), json_encode($rows, JSON_UNESCAPED_UNICODE));
$live = count(array_filter($rows, function ($r) { return (int) $r->con_tai_khoan === 1; }));
echo "2a mo coi: " . count($rows) . " dong, con tai khoan: $live\n";
$del = DB::delete("DELETE ehr FROM employee_has_roles ehr LEFT JOIN company_employees ce ON ce.employee_id=ehr.employee_id AND ce.company_id=ehr.company_id WHERE ce.id IS NULL");
echo "2b da xoa: $del\n";
$c3 = DB::selectOne("SELECT COUNT(*) c FROM (SELECT ehr.employee_id, rhp.company_id FROM bak_rbac_employee_has_roles ehr JOIN bak_rbac_role_has_permissions rhp ON rhp.role_id=ehr.role_id JOIN bak_rbac_permissions p ON p.id=rhp.permission_id AND p.guard_name='web' AND p.name IN ('Quản lý tài khoản','Quản lý tài khoản theo tổng công ty','Quản lý tài khoản theo công ty') WHERE ehr.company_id IS NULL OR ehr.company_id=rhp.company_id GROUP BY 1,2) old JOIN employees e ON e.id=old.employee_id AND e.status=1 JOIN company_employees ce ON ce.employee_id=old.employee_id AND ce.company_id=old.company_id WHERE NOT EXISTS (SELECT 1 FROM employee_has_roles h JOIN roles r ON r.id=h.role_id AND r.company_id=h.company_id AND r.status=1 JOIN role_has_permissions rhp2 ON rhp2.role_id=r.id JOIN permissions p2 ON p2.id=rhp2.permission_id AND p2.code='human.tai_khoan_nhan_vien.manage' AND p2.deprecated_at IS NULL WHERE h.employee_id=old.employee_id AND h.company_id=old.company_id)")->c;
echo "3 mat quyen quan ly tai khoan: $c3\n";
\App\Support\Permissions\PermissionChecker::flush(); cache()->forget("spatie.permission.cache");
echo "khoi5 role_has_permissions.company_id con: " . count(DB::select("SHOW COLUMNS FROM role_has_permissions LIKE 'company_id'")) . "\n";
echo "roles khong cong ty: " . DB::table('roles')->whereNull('company_id')->count() . " | roles: " . DB::table('roles')->count() . " | map: " . DB::table('rbac_role_map')->count() . " | alias: " . DB::table('permission_aliases')->count() . " | ma: " . DB::table('permissions')->whereNotNull('code')->whereNull('deprecated_at')->count() . "\n";
