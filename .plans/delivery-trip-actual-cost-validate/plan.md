# Plan: Validate cước vận chuyển thực tế chuyến xe theo CP xăng + cầu đường + công tác phí + CP khác

## Trạng thái
- Bắt đầu: 2026-04-16
- Tiến độ: ✅ Hoàn thành 2026-04-29 (4 task code + 6 manual test)

## Phase 1: JS class

### DeliveryTrip.blade.php
- [x] Task 1: Thêm getters `fuel_cost`, `other_cost`, `actual_cost_by_formula`, `cost_formula_plus_additional`, `max_total_cost_transition`, `total_cost_transition_tooltip`. Sửa setter `total_cost_transition` để cap theo `max_total_cost_transition`. Guard: chỉ apply logic mới cho xe Tân Phát

## Phase 2: View approveForm

### approveForm.blade.php
- [x] Task 2: Gán `$scope.form.priceListDeliveryVehiclePayload = $scope.priceListDeliveryVehiclePayload` + thêm helper `recalcMaxCostTransition()`

### approve/company.blade.php
- [x] Task 3: Thêm `title` tooltip cho `total_cost_transition`. Thêm 2 field read-only "CP xăng xe" + "CP khác (mai lộ)". Thêm `ng-change="recalcMaxCostTransition()"` vào `toll_cost`, `business_trip_cost`, `price_additional`
- [x] Task 4: Xe ngoài (`approve/other.blade.php`) không có `toll_cost`/`business_trip_cost` → không áp dụng logic mới (guard trong JS class)

## Phase 3: Manual test

- [x] Test xe Tân Phát — nhập toll_cost + business_trip_cost lớn (vd formula=100k, actual=150k):
  - TH2: cước thực tế = formula (100k), tooltip = "Cước vận chuyển theo công thức + cước vượt trội thực tế"
  - Cho sửa nhỏ hơn 100k OK
  - Sửa lớn hơn 100k → auto cap về 100k
- [x] Test xe Tân Phát — nhập ít chi phí (vd formula=200k, actual=100k):
  - TH1: cước thực tế = actual (100k), tooltip = "CP xăng + cầu đường + CP khác + công tác phí"
  - Cho sửa nhỏ hơn 100k OK
  - Sửa lớn hơn 100k → cap về 100k
- [x] Kiểm tra CP xăng xe + CP khác hiển thị đúng (= vehicle.fuel.price × payload.fuel × km_approved, payload.bribery_cost × km_approved)
- [x] Thay đổi `price_additional`, `toll_cost`, `business_trip_cost` → `total_cost_transition` auto cập nhật
- [x] Xe ngoài → giữ nguyên logic cũ (cap theo `delivery_recipe + price_additional`)
- [x] Kiểm tra sum_transition_cost (phân bổ cho activities) vẫn hoạt động đúng

## Checkpoint

### Checkpoint — 2026-04-16
Vừa hoàn thành: 4/4 task code — 3 files modified (JS class, approveForm, approve/company view)
- JS: +6 getters, sửa setter total_cost_transition
- View company: +2 field CP xăng/CP khác, +tooltip, +ng-change trigger recalc
- Approve form: pass priceListDeliveryVehiclePayload vào form, +helper recalcMaxCostTransition
Đang làm dở: Chờ user manual test + tự commit
Bước tiếp theo: User test → commit → báo lại
Blocked: không

### Checkpoint — 2026-04-29
Vừa hoàn thành: ✅ Toàn bộ 6 case manual test pass. Đóng feature.
Đang làm dở: không
Bước tiếp theo: không
Blocked: không
