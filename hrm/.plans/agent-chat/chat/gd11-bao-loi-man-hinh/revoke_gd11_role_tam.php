$rid = DB::table('roles')->where('name','TMP_GD11_BaoLoi')->value('id');
if ($rid) { DB::table('employee_has_roles')->where('role_id',$rid)->delete(); DB::table('role_has_permissions')->where('role_id',$rid)->delete(); DB::table('roles')->where('id',$rid)->delete(); }
app(\Spatie\Permission\PermissionRegistrar::class)->forgetCachedPermissions();
echo "revoked role $rid (permission row giữ lại — catalog đã khai)", PHP_EOL;
