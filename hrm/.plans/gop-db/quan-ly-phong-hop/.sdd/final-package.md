# Review package — TOÀN BỘ Phase 1 (nhánh feat/quan-ly-phong-hop)

## BE — git status + danh sách file mới
 M Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
 M modules_statuses.json
?? Modules/Meeting/
?? tests/Unit/MeetingRoomConfigTest.php

Modules/Meeting/Config/.gitkeep
Modules/Meeting/Config/config.php
Modules/Meeting/Console/.gitkeep
Modules/Meeting/Database/Migrations/.gitkeep
Modules/Meeting/Database/Migrations/2026_09_17_000001_create_meeting_room_amenities_table.php
Modules/Meeting/Database/Migrations/2026_09_17_000002_create_meeting_rooms_table.php
Modules/Meeting/Database/Migrations/2026_09_17_000003_create_meeting_room_room_amenity_table.php
Modules/Meeting/Database/Migrations/2026_09_17_000004_create_meeting_room_bookings_table.php
Modules/Meeting/Database/Migrations/2026_09_17_000005_create_meeting_room_booking_participants_table.php
Modules/Meeting/Database/Migrations/2026_09_17_000006_create_meeting_room_booking_recurrences_table.php
Modules/Meeting/Database/Migrations/2026_09_17_000007_add_meeting_room_id_to_meetings_table.php
Modules/Meeting/Database/Migrations/2026_09_17_000008_add_meeting_room_config_to_general_regulations_table.php
Modules/Meeting/Database/Seeders/.gitkeep
Modules/Meeting/Database/Seeders/MeetingDatabaseSeeder.php
Modules/Meeting/Database/factories/.gitkeep
Modules/Meeting/Entities/.gitkeep
Modules/Meeting/Entities/MeetingRoom.php
Modules/Meeting/Entities/MeetingRoomAmenity.php
Modules/Meeting/Http/Controllers/.gitkeep
Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomAmenityController.php
Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php
Modules/Meeting/Http/Middleware/.gitkeep
Modules/Meeting/Http/Requests/.gitkeep
Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php
Modules/Meeting/Http/Requests/MeetingRoomAmenity/MeetingRoomAmenityRequest.php
Modules/Meeting/Providers/.gitkeep
Modules/Meeting/Providers/MeetingServiceProvider.php
Modules/Meeting/Providers/RouteServiceProvider.php
Modules/Meeting/Resources/lang/.gitkeep
Modules/Meeting/Routes/.gitkeep
Modules/Meeting/Routes/api.php
Modules/Meeting/Routes/web.php
Modules/Meeting/Services/MeetingRoomAmenityService.php
Modules/Meeting/Services/MeetingRoomService.php
Modules/Meeting/Tests/Feature/.gitkeep
Modules/Meeting/Tests/Unit/.gitkeep
Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php
Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
Modules/Meeting/Transformers/MeetingRoomAmenity/DetailMeetingRoomAmenityResource.php
Modules/Meeting/Transformers/MeetingRoomAmenity/MeetingRoomAmenityResource.php
Modules/Meeting/composer.json
Modules/Meeting/module.json

## BE — diff file đã theo dõi
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
diff --git a/modules_statuses.json b/modules_statuses.json
index 0215290c2..fc500c704 100644
--- a/modules_statuses.json
+++ b/modules_statuses.json
@@ -25,5 +25,6 @@
     "Warehouse": true,
     "Transport": true,
     "CustomerCare": true,
-    "Finance": true
+    "Finance": true,
+    "Meeting": true
 }

## FE — git status
 M components/modal/V2BaseModal.vue
 M components/subsystem-menu/meeting.js
?? pages/meeting/room-amenities/
?? pages/meeting/rooms/

## FE — diff file đã theo dõi
diff --git a/components/modal/V2BaseModal.vue b/components/modal/V2BaseModal.vue
index 5c1dcdaba..dd1f3f5f5 100644
--- a/components/modal/V2BaseModal.vue
+++ b/components/modal/V2BaseModal.vue
@@ -125,6 +125,14 @@ export default {
         close() {
             this.$bvModal.hide(this.modalId)
         },
+        // Alias của close() — `utils/mixins/unsavedModalMixin.js` gọi `this.$refs[ref].hide()`
+        // sau khi user xác nhận "Thoát" (khuôn cũ dùng <b-modal ref="modal"> nên có sẵn .hide()
+        // gốc của BootstrapVue). V2BaseModal bọc b-modal nên thiếu method này — bổ sung thêm (không
+        // đổi hành vi show()/close() hiện có) để modal MỚI dựng trên V2BaseModal dùng được mixin
+        // cảnh báo "chưa lưu" theo đúng quy định CLAUDE.md, không phải tự viết beforeRouteLeave riêng.
+        hide() {
+            this.close()
+        },
     },
 }
 </script>
diff --git a/components/subsystem-menu/meeting.js b/components/subsystem-menu/meeting.js
index 5af57690e..9bdb15512 100644
--- a/components/subsystem-menu/meeting.js
+++ b/components/subsystem-menu/meeting.js
@@ -33,6 +33,11 @@ export const meetingItems = [
                 link: '/assign/meeting_cancel_reason',
                 isShow: ['Quản lý danh mục lý do hủy cuộc họp', 'Xem danh mục lý do hủy cuộc họp'],
             },
+            {
+                label: 'Tiện nghi phòng họp',
+                link: '/meeting/room-amenities',
+                isShow: ['Quản lý danh mục tiện nghi phòng họp', 'Xem danh mục tiện nghi phòng họp'],
+            },
         ],
     },
     {
@@ -47,8 +52,12 @@ export const meetingItems = [
         icon: 'ri-door-open-line',
         isMenuCollapsed: false,
         subItems: [
-            // Sheet bôi vàng cả 2 mục = chưa xây dựng, dự kiến làm sau.
-            { label: 'Danh sách phòng họp' },
+            // Sheet bôi vàng: "Đăng ký phòng họp" chưa xây dựng, dự kiến làm sau (Phase 2).
+            {
+                label: 'Danh sách phòng họp',
+                link: '/meeting/rooms',
+                isShow: ['Quản lý danh mục phòng họp', 'Xem danh mục phòng họp'],
+            },
             { label: 'Đăng ký phòng họp' },
         ],
     },

pages/meeting/dashboard/index.vue
pages/meeting/room-amenities/components/RoomAmenityModal.vue
pages/meeting/room-amenities/index.vue
pages/meeting/rooms/components/MeetingRoomModal.vue
pages/meeting/rooms/index.vue

## e2e — spec của phân hệ
_auth-smoke.spec.ts
meeting-room.api.spec.ts
meeting-room.spec.ts
room-amenity.api.spec.ts
