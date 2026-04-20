# Design: Bỏ ô checkbox chọn nhân viên form Quyết toán thưởng NS quý

## Bối cảnh

Form "Quyết toán thưởng năng suất quý" (TanPhatDev) có cột checkbox cho phép chọn/bỏ nhân viên ra khỏi quyết toán (`employee.need_settlement`). Yêu cầu: bỏ UI checkbox, toàn bộ nhân viên trong danh sách đều được quyết toán.

## Quy tắc

- Bỏ cột checkbox trong header bảng (checkAll) và mỗi dòng nhân viên
- Sửa `colspan` dòng "Tổng cộng" từ 3 → 2 để khớp số cột mới
- `employee.need_settlement` default `true` (trong `BillProductivitySettlementQuarterEmployee.blade.php:24-25`) → không đụng logic class, mọi nhân viên tự động được tính vào sums + submit
- Bỏ luôn class `ng-class="!employee.need_settlement ? 'text-muted' : ''"` (dead code sau khi bỏ checkbox, vì điều kiện luôn false)

## Thay đổi

### ERP (TanPhatDev) — Frontend

- `resources/views/accounting/bill_productivity_settlement_quarters/form.blade.php`:
  - Xoá `<th>` checkbox header (~line 192-199) chứa `id="checkAll"` + `form.check_all`
  - Xoá `<td>` checkbox per-row (~line 245-253) chứa `employee.need_settlement`
  - `<td colspan="3" class="text-center">Tổng cộng</td>` → `colspan="2"`
  - Xoá `ng-class="!employee.need_settlement ? 'text-muted' : ''"` khỏi `<tr ng-repeat="employee ...">`

## Không thay đổi

- `BillProductivitySettlementQuarter.blade.php` class — giữ nguyên logic sums/submit filter theo `need_settlement` (vì default true → filter không loại ai)
- `BillProductivitySettlementQuarterEmployee.blade.php` — giữ default `need_settlement = true`
- Backend, controller, model, migration
- Form view khác (`bill_commission_settlement_quarters/form.blade.php`) — có checkbox tương tự nhưng KHÔNG trong scope
