# Plan — 2 danh mục bảo dưỡng (phân hệ CSKH)

> Phụ trách: @junfoke · Tạo 2026-08-03
> Design: `.plans/gop-db/customer-care-maintenance-catalogs/design.md`

## Phase 0 — Khảo sát ERP

- [x] Route `levels` + `note_maintenances`, 2 controller `Sale\LevelController` /
      `Sale\NoteMaintenanceController`, 2 model, 5 file view, 4 request class
- [x] Soi bảng: `levels` 29 dòng (không audit), `note_maintenances` 11 dòng (có
      `created_by`/`updated_by` varchar lưu ERP employee id)
- [x] Xác định phân hệ đích: **CSKH** (`customer-care`, `permissionType = 24`) theo sheet gộp
- [x] Đếm ràng buộc xóa thật: `level_id` ở 6 bảng, `note_maintenance_id` ở 1 bảng (9/11 đang dùng)
- [x] Phát hiện 4 lỗi/thiếu sót bản ERP (xem design.md)

## Phase 1 — Gỡ bỏ lớp map ERP employee (user báo giữa chừng)

- [x] ~~Tách `app/Helper/ErpEmployeeHelper.php`~~ → **user báo đã gộp `employees` +
      `employee_infos`, chỉ còn 1 bảng** nên helper là thừa. Đã xóa hẳn + revert `composer.json`
- [x] Kiểm chứng trước khi gỡ: commit `gộp bảng employees: HRM đọc lại bảng employees chung`,
      `TpEmployee::$table = 'employees'`, bảng tạo lại 2026-08-03 08:48; `hrm_employees` là bản cũ
      (lệch 290 id, 164 `employee_info_id`) → **không dùng nữa**
- [x] `FinanceService`: 3 hàm map → 1 hàm `currentEmployeeId()` = `auth()->user()->id`
- [x] Xóa `Modules\Finance\Entities\ErpEmployee`, chuyển 4 quan hệ sang
      `Modules\Human\Entities\Employee` (cùng bảng `employees`)
- [x] Model dùng chung không có accessor `display_name` → thêm `employeeDisplayName()` vào
      `Account` / `TypeAccount` để ghép `"MÃ - Họ tên"`, **không sửa model dùng chung**
- [x] Đổi request attribute `erp_employee_id` → `current_employee_id`
- [x] Bộ lọc Người tạo/Người cập nhật 2 màn tài khoản: bỏ bước map, dùng thẳng id
- [x] Verify 3 màn Tài chính cũ vẫn chạy: tên người tạo hiện đúng
      (`created_by=34` → `11710160 - Đào Thị Thúy`), 39 route Finance còn nguyên
- [x] Không còn tham chiếu `hrm_employees` nào trong `app/` và `Modules/`

## Phase 2 — BE: dựng nội dung `Modules/CustomerCare` (module trước đó rỗng hoàn toàn)

- [x] `Entities/Level/Level.php` — `USED_BY` **6 bảng**, `usedIn()` / `isCanDelete()`
- [x] `Entities/NoteMaintenance/NoteMaintenance.php` — `USED_BY` 1 bảng; `created_by`/`updated_by`
      là **varchar** nên ép chuỗi khi ghi
- [x] 2 Resource, 2 Service, 2 Request, 2 Controller
- [x] `Routes/api.php` — **16 route** dưới `/v1/customer-care`
- [x] 2 lớp Excel export + 2 blade

## Phase 3 — Quyền (4 quyền ĐẦU TIÊN của phân hệ CSKH, `type = 24`)

- [x] id **1115-1118** vào seeder, `group = 'Danh mục dịch vụ bảo dưỡng'` (duy nhất toàn hệ thống)
- [x] Insert tay vào DB local + cấp cho cùng bộ vai trò/công ty của quyền 1107
- [x] Khối "Phân hệ CSKH" trên màn Phân quyền **đã có sẵn** nhờ đợt sắp xếp theo registry
      (xem [[project_permission_screen_subsystem_order]]) — không phải sửa `Permission.vue`

## Phase 4 — FE

- [x] Mở khóa 2 mục trong `components/subsystem-menu/customer-care.js`
- [x] `pages/customer-care/levels/index.vue` + `components/modal/customer-care/level-modal.vue`
- [x] `pages/customer-care/note-maintenances/index.vue` +
      `components/modal/customer-care/note-maintenance-modal.vue`
- [x] Áp sẵn 3 bài học đã rút: `key` cột sortable trùng tên trường BE, ép `Number()` cho `meta`,
      `page`/`per_page` tách khỏi `filters` + `DedupeLoadMixin`

## Phase 5 — Verify

- [x] Chặn xóa trên dữ liệu thật: `Cấp 1 (6T)` → *Gói bảo dưỡng, Cấp bảo dưỡng của gói dịch vụ,
      Báo giá dịch vụ*; ghi chú id 1 → *Cấp bảo dưỡng của gói dịch vụ*; tìm được cả bản ghi
      xóa được (`Cấp 2 (6T)`, 4 ghi chú)
- [x] CRUD round-trip cả 2 màn, `key_name` tự viết HOA, `description` rỗng → NULL
- [x] Validate: rỗng / trùng tên / trùng ký hiệu / mô tả > 255 ký tự
- [x] Lọc + sort + getAll + export xlsx (80KB mỗi file)
- [x] 16 route CSKH + 39 route Finance đăng ký đủ
- [x] `php -l` toàn bộ + compile 4 file Vue
- [x] DB nguyên trạng: `levels` 29, `note_maintenances` 11
- [ ] ⏳ Chưa verify bằng mắt trên browser (chưa đăng nhập được phiên Playwright)

## Việc còn lại

- [ ] ⚠️ **Rà `ErpPermissionHelper` sau khi gộp bảng**: `app/Helpers/ErpPermissionHelper.php` vẫn
      đọc qua `mysql2` (DB ERP cũ), còn được gọi ở `Modules/Assign` (CustomerService,
      MeetingController, ProductProjectController, CustomerManagerService) và
      `app/Helper/CustomerOwnership.php`. Gộp bảng xong thì phần này nên bỏ luôn — ngoài phạm vi
      2 màn này
- [ ] Chạy seeder quyền trên môi trường thật (local đã insert tay)
