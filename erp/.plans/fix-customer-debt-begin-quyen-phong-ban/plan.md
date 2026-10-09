# Fix: Số dư đầu kỳ báo cáo công nợ chi tiết KH = 0 với user quyền phòng ban

## Bug
`admin/sale/reports/customer-debt-details`. NV Hồ Thị Xuân (emp 83, phòng 5) có quyền "xem theo phòng ban", lọc chính mình → **số dư đầu kỳ = 0**. User quyền tổng công ty lọc cùng NV → **38.285.601**.

## Root cause (verify prod erp_new)
- `AccountDetail::getDeptBegin` nhánh is_department chỉ `whereIn('department_id', <phòng user QUẢN LÝ qua EmployeeManageDepartment>)`.
- Hồ Thị Xuân KHÔNG quản lý phòng nào (EmployeeManageDepartment rỗng) → whereIn([]) → 0. Dù dòng đầu kỳ có department_id=5 (đúng phòng cô ấy) và contract_created_by=83.
- Báo cáo CHÍNH (permissionsAndApplyReportDataFilter, dòng 1188-1191) áp `(department_id IN managed) OR contract_created_by=self` → nên in-period vẫn hiện. getDeptBegin THIẾU vế `orWhere('contract_created_by', self)`.

## Fix
- [x] getDeptBegin (nhánh else, is_company + is_department): bọc where(function) thêm `orWhere('contract_created_by', auth id)` — khớp báo cáo chính.
- [x] Verify prod: sau fix logic → 38.285.601 (khớp tổng cty). php -l sạch.
- [x] Verify full query trước/sau fix: 0 → 38.285.601 (khớp tổng cty).
- [x] User chốt Hướng A: mỗi cấp quyền LUÔN thấy HĐ của chính mình (contract_created_by=self) → 38tr là ĐÚNG. Fix giữ nguyên.
- [ ] User reload xác nhận trên browser.

## Không làm: không đụng nhánh debt-employee (báo cáo khác).
