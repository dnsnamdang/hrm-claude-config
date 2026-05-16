# Design: Validate cước vận chuyển thực tế trên phiếu hạch toán chuyến xe

## Bối cảnh

Tái áp dụng logic TH1/TH2 (từ feature `delivery-trip-actual-cost-validate`) lên màn phiếu hạch toán chuyến xe (`delivery_trip_accounting`). Khác màn duyệt ở 2 điểm:
- Header `total_cost_transition` cho edit (lưu riêng, không ghi đè `delivery_trips.total_cost_transition`)
- `is_company_sp` user tick được → trigger recalc

## Quy tắc

Logic mới kích hoạt khi **TẤT CẢ** điều kiện thoả:
1. Xe Tân Phát (`formDeliveryTrip.vehicle.is_tanphat`)
2. Có `priceListDeliveryVehiclePayload`
3. Khoảng cách ≤ `config.company_pay_km` (1 chiều) hoặc 2× (2 chiều)
4. Tất cả `activities` có `is_company_sp = 1`
5. Tất cả `activities` có `is_bulky = true` và `cost_contract ≥ config.pay_value_order`

Khi user tick/untick `is_company_sp` hoặc `is_bulky` → recalc `total_cost_transition` theo max mới.

## Thay đổi

### Migration
- Thêm `total_cost_transition decimal(16,2) nullable` vào `delivery_trip_accounting`

### Backend — Model
- `DeliveryTripAccounting.php`: thêm `total_cost_transition` vào `$fillable`
- `getDataForShow()`: fallback về `delivery_trip.total_cost_transition` nếu `total_cost_transition` null

### Backend — Controller
- `DeliveryTripAccountingController::store()` + `update()`: thêm `total_cost_transition` vào dữ liệu save

### Frontend — JS class `DeliveryTripAccounting`
Thêm getters (copy pattern từ `DeliveryTrip` class):
- `fuel_cost` = `formDeliveryTrip.vehicle.fuel.price × priceListDeliveryVehiclePayload.fuel × form.km_approved`
- `other_cost` = `priceListDeliveryVehiclePayload.bribery_cost × form.km_approved`
- `actual_cost_by_formula` = fuel + other + `formDeliveryTrip.toll_cost` + `formDeliveryTrip.business_trip_cost`
- `cost_formula_plus_additional` = `formDeliveryTrip.delivery_recipe + formDeliveryTrip.price_additional`
- `all_exports_company_sp` (check từ `this.activities`)
- `max_total_cost_transition`, `total_cost_transition_tooltip`

Setter `total_cost_transition` cap theo `max_total_cost_transition`. Nếu chưa có giá trị (mode create) → fallback từ `formDeliveryTrip.total_cost_transition`.

### Frontend — View `approve/company.blade.php` (accounting)
- Header "Cước vận chuyển thực tế": đổi `disabled` → `ng-disabled="mode == 'show'"`, bind `ng-model="form.total_cost_transition"`, thêm `title` tooltip
- Thêm 2 field read-only "CP xăng xe" + "CP khác (mai lộ)"
- Thêm `recalcMaxCostTransition()` vào `ng-change` của checkbox `is_company_sp` và `is_bulky` per activity

### Frontend — Controller JS
Trong `create.blade.php` / `edit.blade.php`: sau khi load formDeliveryTrip → gán `form.priceListDeliveryVehiclePayload = $scope.priceListDeliveryVehiclePayload` + init `form.total_cost_transition` từ `formDeliveryTrip.total_cost_transition` (nếu chưa có).

## Không thay đổi
- Bảng `delivery_trips` — giữ nguyên giá trị gốc, không ghi đè
- Màn duyệt chuyến xe — không đụng
- Logic `DeliveryTripAccountingActivity` (`changeBulky`, `changeCompanySp`) — giữ nguyên
- Logic hạch toán / bút toán kế toán — không đổi
