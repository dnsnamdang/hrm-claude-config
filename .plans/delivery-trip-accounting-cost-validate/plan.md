# Plan: Validate cước vận chuyển thực tế trên phiếu hạch toán chuyến xe

## Trạng thái
- Bắt đầu: 2026-04-16
- Tiến độ: ✅ Hoàn thành 2026-04-29 (5 task code + migration + 5 manual test)

## Phase 1: DB
- [x] Task 1: Migration thêm `total_cost_transition decimal(16,2) nullable` vào `delivery_trip_accounting`

## Phase 2: Backend
- [x] Task 2: `DeliveryTripAccountingController::store()` + `update()` — nhận `total_cost_transition` từ request, lưu vào accounting (nếu null fallback từ trip)

## Phase 3: Frontend JS class
- [x] Task 3: `DeliveryTripAccounting.blade.php` — thêm getters `fuel_cost`, `other_cost`, `actual_cost_by_formula`, `cost_formula_plus_additional`, `all_activities_company_sp`, `max_total_cost_transition`, `total_cost_transition_tooltip`. Setter `total_cost_transition` cap theo max. Thêm `total_cost_transition` vào `submit_data`

## Phase 4: Frontend view
- [x] Task 4: `approve/company.blade.php` — enable header `total_cost_transition` (bỏ disabled, dùng ng-model), thêm tooltip + 2 field "CP xăng xe" + "CP khác". Thêm `recalcMaxCostTransition()` vào ng-change của checkbox `is_company_sp`, `is_bulky`

## Phase 5: Wire scope
- [x] Task 5: `create.blade.php` + `edit.blade.php` — gán `form.formDeliveryTrip = formDeliveryTrip` + `form.priceListDeliveryVehiclePayload`. Thêm helper `$scope.recalcMaxCostTransition()`

## Phase 6: Manual test

- [x] Chạy migration: `php artisan migrate`
- [x] Tạo phiếu hạch toán từ chuyến xe đã duyệt:
  - Header "Cước vận chuyển thực tế" cho phép sửa
  - Tick/untick "Công ty hỗ trợ" tất cả activities → tooltip hiện, cước thực tế cap theo max
  - Bỏ tick 1 activity → fallback logic cũ (cap theo delivery_recipe + price_additional)
- [x] Edit phiếu hạch toán đã lưu → giá trị `total_cost_transition` load đúng
- [x] Show phiếu hạch toán (mode show) → header disabled, giá trị hiển thị đúng
- [x] Submit form → BE lưu `total_cost_transition` vào bảng `delivery_trip_accounting`, không ghi đè `delivery_trips`

## Checkpoint

### Checkpoint — 2026-04-16
Vừa hoàn thành: 5/5 task code — 6 files (1 migration + 5 modified)
- Migration: thêm `total_cost_transition` vào `delivery_trip_accounting`
- Controller: nhận total_cost_transition từ request, save riêng trên accounting
- JS class: +7 getters tính logic TH1/TH2, setter cap, submit_data
- View company: enable header input, tooltip, 2 field CP xăng/khác, ng-change trigger recalc
- create + edit blade: gán formDeliveryTrip + priceListDeliveryVehiclePayload vào form, +helper recalcMaxCostTransition
Đang làm dở: Chờ user migrate + test + tự commit
Bước tiếp theo: User test → commit → báo lại
Blocked: không

### Checkpoint — 2026-04-29
Vừa hoàn thành: ✅ Migration chạy + 5 case manual test pass. Đóng feature.
Đang làm dở: không
Bước tiếp theo: không
Blocked: không
