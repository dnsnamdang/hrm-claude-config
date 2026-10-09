### git diff --stat
 Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | 8 ++++++++
 1 file changed, 8 insertions(+)

### git diff -U6 (seeder)
diff --git a/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php b/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
index 63ca39588..0190a1dfd 100644
--- a/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
+++ b/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
@@ -1391,8 +1391,16 @@ class PermissionsTableSeeder extends Seeder
         // ⚠️ ĐỔI ID 1543–1546 -> 1561–1564 khi rebase lên gop_db (lý do như khối Đề nghị nhập kho
         // ở trên). Gate so theo TÊN quyền nên đổi id KHÔNG ảnh hưởng phân quyền.
         Permission::create(['id' => 1561, 'guard_name' => 'api', 'name' => 'Xem phiếu nhập hàng theo tổng công ty', 'display_name' => 'Xem phiếu nhập hàng theo tổng công ty', 'group' => 'Phiếu nhập hàng', 'type' => 8, 'sort_order' => 1]);
         Permission::create(['id' => 1562, 'guard_name' => 'api', 'name' => 'Xem phiếu nhập hàng theo công ty', 'display_name' => 'Xem phiếu nhập hàng theo công ty', 'group' => 'Phiếu nhập hàng', 'type' => 8, 'sort_order' => 2]);
         Permission::create(['id' => 1563, 'guard_name' => 'api', 'name' => 'Xem phiếu nhập hàng theo phòng ban', 'display_name' => 'Xem phiếu nhập hàng theo phòng ban', 'group' => 'Phiếu nhập hàng', 'type' => 8, 'sort_order' => 3]);
         Permission::create(['id' => 1564, 'guard_name' => 'api', 'name' => 'Xem phiếu nhập hàng theo bộ phận', 'display_name' => 'Xem phiếu nhập hàng theo bộ phận', 'group' => 'Phiếu nhập hàng', 'type' => 8, 'sort_order' => 4]);
+
+        // ===== Phiếu yêu cầu xuất bán hàng mượn (BorrowSellRequest) — Phase 1 =====
+        // Trùng tên với quyền guard 'web' của ERP để hiện đúng tab phân hệ + cross-guard whereIn id khi check quyền.
+        Permission::create(['id' => 1565, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của tổng công ty', 'display_name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của tổng công ty', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 1]);
+        Permission::create(['id' => 1566, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của công ty', 'display_name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của công ty', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 2]);
+        Permission::create(['id' => 1567, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của phòng ban', 'display_name' => 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của phòng ban', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 3]);
+        Permission::create(['id' => 1568, 'guard_name' => 'api', 'name' => 'Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ', 'display_name' => 'Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 4]);
+        Permission::create(['id' => 1569, 'guard_name' => 'api', 'name' => 'Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ', 'display_name' => 'Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ', 'group' => 'Yêu cầu xuất bán hàng mượn', 'type' => 8, 'sort_order' => 5]);
     }
 }
