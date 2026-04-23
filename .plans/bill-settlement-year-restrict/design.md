# Design: Cắt năm tương lai khỏi dropdown Năm form Quyết toán thưởng NS quý

## Bối cảnh

Form "Quyết toán thưởng năng suất quý" (TanPhatDev) có dropdown "Năm" load từ `Company::getYears()` — helper dùng chung trả về năm 1970 → năm-hiện-tại + 25. Yêu cầu: không cho chọn năm tương lai, mặc định năm hiện tại khi tạo mới.

## Quy tắc

- Dropdown "Năm" chỉ hiển thị từ 1970 → năm hiện tại (cắt sạch năm tương lai, không exception cho record cũ lỡ có năm tương lai)
- Tạo mới: field "Năm" default = năm hiện tại (logic đã có sẵn ở `formJs.blade.php:98-104`)
- Edit/Show: giữ nguyên hành vi hiện tại

## Thay đổi

### ERP (TanPhatDev)

- `resources/views/accounting/bill_productivity_settlement_quarters/formJs.blade.php`: sau dòng `$scope.years = @json(Company::getYears())`, thêm 2 dòng filter client-side `$scope.years = $scope.years.filter(y => y.id <= new Date().getFullYear())`

## Không thay đổi

- `Company::getYears()` — helper dùng chung, không sửa
- `form.blade.php` — template giữ nguyên
- Backend, controller, model, migration, API
- Logic default năm hiện tại (`formJs.blade.php:98-104`) — giữ nguyên
- Các form khác dùng `Company::getYears()` — không ảnh hưởng
