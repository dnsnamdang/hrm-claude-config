# Review package — Task 4 (5 quyền mới)

## git diff seeder
diff --git a/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php b/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
index 45b964125..177231878 100644
--- a/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
+++ b/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
@@ -947,6 +947,12 @@ class PermissionsTableSeeder extends Seeder
         // Redmine #11357 — danh mục lý do hủy cuộc họp (id nối tiếp 1181 là id lớn nhất đang có)
         Permission::create(['id' => 1184, 'guard_name' => 'api', 'name' => 'Quản lý danh mục lý do hủy cuộc họp', 'display_name' => 'Quản lý danh mục lý do hủy cuộc họp', 'group' => 'Danh mục', 'type' => 4]);
         Permission::create(['id' => 1185, 'guard_name' => 'api', 'name' => 'Xem danh mục lý do hủy cuộc họp', 'display_name' => 'Xem danh mục lý do hủy cuộc họp', 'group' => 'Danh mục', 'type' => 4]);
+        // Quản lý phòng họp (phân hệ Meeting) — id nối tiếp 1573 là id lớn nhất đang có
+        Permission::create(['id' => 1574, 'guard_name' => 'api', 'name' => 'Quản lý danh mục phòng họp', 'display_name' => 'Quản lý danh mục phòng họp', 'group' => 'Danh mục', 'type' => 4]);
+        Permission::create(['id' => 1575, 'guard_name' => 'api', 'name' => 'Xem danh mục phòng họp', 'display_name' => 'Xem danh mục phòng họp', 'group' => 'Danh mục', 'type' => 4]);
+        Permission::create(['id' => 1576, 'guard_name' => 'api', 'name' => 'Quản lý danh mục tiện nghi phòng họp', 'display_name' => 'Quản lý danh mục tiện nghi phòng họp', 'group' => 'Danh mục', 'type' => 4]);
+        Permission::create(['id' => 1577, 'guard_name' => 'api', 'name' => 'Xem danh mục tiện nghi phòng họp', 'display_name' => 'Xem danh mục tiện nghi phòng họp', 'group' => 'Danh mục', 'type' => 4]);
+        Permission::create(['id' => 1578, 'guard_name' => 'api', 'name' => 'Xem báo cáo hiệu quả sử dụng phòng họp', 'display_name' => 'Xem báo cáo hiệu quả sử dụng phòng họp', 'group' => 'Báo cáo phòng họp', 'type' => 4]);
         Permission::create(['id' => 1006, 'guard_name' => 'api', 'name' => 'Xem danh mục lĩnh vực khách hàng', 'display_name' => 'Xem danh mục lĩnh vực khách hàng', 'group' => 'Danh mục', 'type' => 4]);
 
         Permission::create(['id' => 1007, 'guard_name' => 'api', 'name' => 'Xem danh sách yêu cầu làm giải pháp theo tổng công ty', 'display_name' => 'Xem danh sách yêu cầu làm giải pháp theo tổng công ty', 'group' => 'Yêu cầu làm giải pháp', 'type' => 4]);

## Trạng thái DB (người điều phối tự truy vấn)
```
id	guard_name	name	group	type
1574	api	Quản lý danh mục phòng họp	Danh mục	4
1575	api	Xem danh mục phòng họp	Danh mục	4
1576	api	Quản lý danh mục tiện nghi phòng họp	Danh mục	4
1577	api	Xem danh mục tiện nghi phòng họp	Danh mục	4
1578	api	Xem báo cáo hiệu quả sử dụng phòng họp	Báo cáo phòng họp	4
permission_id	role_id	company_id
1574	18	1
1575	18	1
1576	18	1
1577	18	1
1578	18	1
tong_quyen_api
745
tong_grant
15993
```
