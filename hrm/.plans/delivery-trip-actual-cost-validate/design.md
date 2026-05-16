# Design: Validate cước vận chuyển thực tế chuyến xe theo chi phí xăng + cầu đường + công tác phí + CP khác

## Bối cảnh

Màn duyệt chuyến xe chở hàng (TanPhatDev) hiện tính `total_cost_transition` = `delivery_recipe + price_additional`, chỉ cap bởi delivery_recipe. Yêu cầu: so sánh với CP thực tế (xăng + cầu đường + công tác phí + CP khác) — nếu công thức >= thực tế thì lấy thực tế, ngược lại lấy công thức, cho phép user sửa nhỏ hơn.

## Quy tắc

- CP xăng = `vehicle.fuel.price × vehicle.payload.fuel × km_approved` (copy pattern từ màn hạch toán)
- CP khác (mai lộ) = `vehicle.payload.bribery_cost × km_approved`
- `formulaPlus = delivery_recipe + price_additional`
- `actualCosts = CP_xang + CP_khac + toll_cost + business_trip_cost`
- **TH1**: `formulaPlus >= actualCosts` → `total_cost_transition = actualCosts`. Tooltip: "CP xăng + cầu đường + CP khác + công tác phí"
- **TH2**: `formulaPlus < actualCosts` → `total_cost_transition = formulaPlus`. Tooltip: "Cước vận chuyển theo công thức + cước vượt trội thực tế"
- User sửa được nhưng không vượt max

## Thay đổi

### ERP (TanPhatDev) — Backend

- `DeliveryTripController::show()` + `approveForm()`: eager load `vehicle.fuel`, `vehicle.payload` (để JS có đủ dữ liệu tính CP xăng + CP khác)
- `DeliveryTripController::approve()`: validate `total_cost_transition <= maxAllowed` (tính lại từ vehicle + request)

### ERP — Frontend (JS class `DeliveryTrip`)

- Thêm computed: `fuel_cost`, `other_cost`, `actual_cost_by_formula` (tổng 4 CP), `cost_formula_plus_additional`, `max_total_cost_transition`, `total_cost_transition_tooltip`
- Sửa setter `total_cost_transition`: cap theo `max_total_cost_transition` thay vì `delivery_recipe`
- Khi field cost thay đổi (`toll_cost`, `business_trip_cost`, `price_additional`, `km_approved`) → reset `total_cost_transition = max_total_cost_transition`

### ERP — View

- `approve/company.blade.php`: thêm 2 field read-only "CP xăng xe" + "CP khác"; thêm `title` tooltip cho input `total_cost_transition`
- `approve/other.blade.php`: tương tự (xe ngoài cũng áp dụng cùng logic)
- `approveForm.blade.php`: có thể thêm block hiển thị breakdown (tuỳ UX)

## Không thay đổi

- Schema DB — không thêm cột mới
- Màn hạch toán chuyến xe — giữ nguyên
- Logic `changeTotalCostTransition()` phân bổ cho activities — giữ nguyên
- Các công thức hiện tại (`delivery_recipe`, `cost_need_allocation`, `company_pay`) — giữ nguyên
- Màn "gửi hàng" (ischeck=3) — không áp dụng, giữ nguyên (chỉ nhập `total_cost_shipping`)
