# Danh mục phương tiện — tách Phòng phụ trách (1 phòng) / Phòng sử dụng (nhiều phòng) — @khoipv

> Bắt đầu: 17/11/2026 · Liên quan: [danh-muc-phuong-tien](../danh-muc-phuong-tien/plan.md), [cham-cong-chon-phuong-tien](../cham-cong-chon-phuong-tien/plan.md)

## Yêu cầu (user 17/11/2026)
- Phòng phụ trách: chỉ **1 phòng**.
- Bổ sung **Phòng sử dụng**: chọn **nhiều phòng**.
- App mobile chỉ cho chọn xe mà **phòng của NV được phép sử dụng** (trước: phòng phụ trách). Chỉ sửa API, **không sửa code app**.

## Hiện trạng (trước khi sửa)
- `vehicle_departments` (nhiều phòng) = "Phòng phụ trách"; app gọi `GET timekeeper/vehicles` → `TimekeeperService::vehiclesForEmployee()` lọc xe có phòng phụ trách = `employee_info.department_id`.
- Validate xe khi chấm/tra soát (`resolveBusinessTripVehicle`) cũng dùng `vehiclesForEmployee()`.
- Dữ liệu local: xe 4 (90,87,85), xe 5 (90,86,84), xe 6 (84), xe 7 (90).

## Phương án
- Đổi tên bảng `vehicle_departments` → `vehicle_use_departments` (= **Phòng sử dụng**) — giữ nguyên dữ liệu ⇒ app thấy đúng các xe như trước.
- Thêm cột `vehicles.department_id` (**Phòng phụ trách**), điền từ dòng pivot đầu tiên (id nhỏ nhất) của mỗi xe.
- App: `vehiclesForEmployee()` lọc theo Phòng sử dụng ⇒ endpoint/response giữ nguyên, app không đổi.
- Web (`pages/timesheet/vehicles`): popup thêm ô Phòng sử dụng (chọn nhiều), Phòng phụ trách chọn 1; danh sách thêm cột + lọc Phòng sử dụng.

## Task
### BE (`hrm-thanhan-api/Modules/Timesheet`)
- [x] Migration `2026_11_17_100000_split_vehicle_departments` (rename bảng + thêm `department_id` + điền dữ liệu)
- [x] Entity `Vehicle`: `department()` (phụ trách), `useDepartments()` (sử dụng)
- [x] `VehicleRequest`: `department_id` required 1 phòng, `use_department_ids` required mảng ≥ 1
- [x] `VehicleService`: index (lọc `department_id` / `use_department_id`, sort phòng phụ trách), show, store, update
- [x] `VehicleController`: nhận `department_id`, `use_department_ids`
- [x] `VehicleResource`: `department_id`, `department_name`, `use_departments`, `use_department_ids`, `use_department_names`
- [x] `TimekeeperService::vehiclesForEmployee()` lọc theo Phòng sử dụng
- [x] Chạy migrate local + test

### FE web (`hrm-thanhan-client/pages/timesheet/vehicles`)
- [x] `VehicleModal.vue`: Phòng phụ trách chọn 1 + ô Phòng sử dụng chọn nhiều
- [x] `index.vue`: cột Phòng phụ trách (1 phòng) + cột Phòng sử dụng (mỗi phòng 1 dòng); bộ lọc Phòng sử dụng

### Bàn giao
### Bổ sung — 17/11/2026 (user: "phòng phụ trách có được sử dụng xe nhé")
- [x] `TimekeeperService::vehiclesForEmployee()`: xe hiện với NV khi phòng NV là **Phòng phụ trách** HOẶC thuộc **Phòng sử dụng**
- [x] Test lại `vehiclesForEmployee` (scratchpad `test_owner.php`, rollback): xe test phụ trách 84 / sử dụng 86 → phòng 84 và 86 đều thấy, phòng khác không; xe đã khóa không ai thấy

### Bổ sung — 17/11/2026 (user: "phòng phụ trách, phòng sử dụng cho lên cùng 1 hàng")
- [x] `VehicleModal.vue`: 2 ô Phòng phụ trách + Phòng sử dụng cùng 1 hàng (`col-md-6` mỗi ô)

### Test E2E Playwright — 17/11/2026 (user yêu cầu)
- [x] `e2e/tests/timesheet/vehicles-phong-su-dung.spec.js` + `e2e/pages/VehiclePage.js` — chạy `--headed` cho user xem
  - Kết quả 17/11/2026: **7/7 pass** (3.7m, SLOW_MO=500): bỏ trống báo 2 lỗi · tạo xe 2 cột đúng · app không thấy xe khi phòng NV không liên quan · lọc Phòng sử dụng · thêm phòng NV vào Phòng sử dụng → app thấy · phòng NV là Phòng phụ trách (không có trong sử dụng) → app vẫn thấy. afterAll đã xóa xe test (DB còn 0 xe `99E-%`).
  - Chạy lại: `cd e2e; $env:SLOW_MO='500'; .\pw.cmd test tests/timesheet/vehicles-phong-su-dung.spec.js --headed`
  - Lưu ý môi trường: bật 4 php-cgi (cổng 9101–9104) + `npm run dev` client; lần đầu Nuxt dev biên dịch lâu, chờ log "Waiting for file changes" rồi mới chạy test

- [ ] Môi trường khác: `php artisan migrate` (hoặc `module:migrate Timesheet`, như nhau)
- [ ] User test tay màn web `/timesheet/vehicles` + chọn xe trên app

## Kết quả test local — 17/11/2026
- Migrate OK; rollback (`down`) rồi migrate lại OK. Dữ liệu sau migrate: xe 4 phụ trách 85 / sử dụng 85,87,90 · xe 5 phụ trách 84 / sử dụng 84,86,90 · xe 6: 84/84 · xe 7: 90/90.
- Script boot app (user 13, transaction rollback, scratchpad `test_vehicle.php`):
  - List 200 trả `department_name` + `use_department_names`; lọc `use_department_id=87` → xe 4; lọc `department_id=84` → xe 5, 6
  - Tạo thiếu 2 ô → 422 "Vui lòng chọn phòng phụ trách" / "Vui lòng chọn phòng sử dụng"; tạo `use_department_ids [86,87,87]` → lưu 86,87 (bỏ trùng)
  - Sửa đổi phòng OK; phòng không tồn tại → 422 `department_id`, `use_department_ids.0`
  - `vehiclesForEmployee` (API app `GET timekeeper/vehicles` + validate khi chấm/tra soát) lọc đúng theo Phòng sử dụng: phòng 84 thấy 29A-00435, 30H-999.88; phòng 90 thấy 29A-00435, 30A-91200, 30B-00126 (+ xe test)
- FE: compile template + parse script 2 file OK (vue-template-compiler / @babel/parser).

## File đã sửa
- API: `Database/Migrations/2026_11_17_100000_split_vehicle_departments.php` (mới), `Entities/Vehicle.php`, `Http/Requests/Vehicle/VehicleRequest.php`, `Http/Controllers/Api/V1/VehicleController.php`, `Services/VehicleService.php`, `Transformers/VehicleResource/VehicleResource.php`, `Services/TimekeeperService.php` (`vehiclesForEmployee`), `Http/Controllers/Api/V1/TimekeeperController.php` (chỉ comment)
- Client: `pages/timesheet/vehicles/components/VehicleModal.vue`, `pages/timesheet/vehicles/index.vue`
- App mobile: **không sửa** — endpoint `GET timekeeper/vehicles` giữ nguyên response `{id, brand, license_plate}`.

## Ghi chú
- API đổi field: `department_ids` (mảng) → `department_id` (1 phòng) + `use_department_ids` (mảng). Response bỏ `departments/department_ids/department_names`, thêm `department_id/department_name/use_departments/use_department_ids/use_department_names`.
- ~~App lọc chỉ theo Phòng sử dụng~~ → đổi 17/11/2026: Phòng phụ trách cũng được dùng xe (phụ trách OR sử dụng).
- Lọc danh sách: `department_id` = Phòng phụ trách, `use_department_id` = Phòng sử dụng.

## Hỏi đáp — 17/11/2026: "mobile app đã lấy các xe mà phòng mình được sử dụng chưa?"
- Code: rồi — app (`TPE_APP` `user_api_service_profile_ext.dart:88`) gọi `GET v1/timekeeper/vehicles` → `TimekeeperService::vehiclesForEmployee()` đã lọc theo Phòng phụ trách HOẶC Phòng sử dụng. App không cần build lại.
- Mới chạy trên **BE local** (:8001). Server thật chưa có: code API chưa commit/push, chưa deploy + chưa chạy migrate (`php artisan migrate` là đủ — `TimesheetServiceProvider.php:30` có `loadMigrationsFrom`).
- Chưa test trực tiếp trên app mobile (chỉ test qua API bằng Playwright/script).

## Push code — 17/11/2026
- [x] API: commit `8ac8ddca` → `origin/master` (8 file Modules/Timesheet, gồm migration)
- [x] Client: commit `4d495c2c` → `origin/master` (VehicleModal.vue, index.vue)
- [ ] Deploy API + client **cùng lúc** (field API đổi: `department_ids` → `department_id` + `use_department_ids`), rồi chạy `php artisan migrate`
- [ ] Test tay trên web + app mobile ở server thật

### Checkpoint — 17/11/2026
Vừa hoàn thành: push API `8ac8ddca` + client `4d495c2c` lên master
Đang làm dở: —
Bước tiếp theo: deploy cả 2 repo, chạy `php artisan migrate`, test tay web + app
Blocked:
