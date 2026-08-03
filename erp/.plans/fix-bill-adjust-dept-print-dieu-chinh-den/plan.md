# Fix: mẫu in phiếu điều chỉnh công nợ không hiện phần "Điều chỉnh đến"

## Bối cảnh
- URL: `admin/income-expenditure/bill_adjust_dept_requests/9128/print`
- Mẫu in (`ReportTemplate::PHIEU_YEU_CAU_DIEU_CHINH_CONG_NO`) đổ dữ liệu từ accessor `BillAdjustDeptRequest::print_data` → `CHI_TIET` = `bill_adjust_dept_request_table`.

## Root cause
`buildCustomerPrintTable()` lặp `$this->details` và đọc field "đến" (`customer_new_name`, `contract_new_code`, `contract_new_created_by`, `money_new`) **ở cấp detail**. Nhưng các field này nằm ở cấp **item** (`BillAdjustDeptRequestDetailItem`, quan hệ `details.items`). Detail chỉ có field "old/từ". → Cột "Điều chỉnh đến" luôn rỗng.
Bảng NCC `buildSupplierPrintTable()` đã đúng (lặp `$detail->items` cho phần "đến").

## Fix
Sửa `buildCustomerPrintTable()` (file `app/Model/IncomeExpenditure/BillAdjustDeptRequest.php`):
- Lặp từng `$detail` (`$this->details`).
- Phần "từ" (customer_old_name, contract_old_code, contract_old_created_by, money_old) ở cấp detail, dùng `rowspan` = số item.
- Phần "đến" lặp `$detail->items`, đọc customer_new_name/contract_new_code/contract_new_created_by/money_new ở cấp item.
- Guard `$item` null khi detail chưa có item (collect([null])).

## Tasks
- [x] Sửa `buildCustomerPrintTable()` lặp items cho phần "đến"
- [ ] User test in lại phiếu 9128 (KH) + 1 phiếu NCC để chắc không hồi quy
- [ ] (tùy) kiểm tra request_type phiếu 9128 = customer

## Checkpoint — 2026-06-17
Vừa hoàn thành: fix buildCustomerPrintTable.
Bước tiếp theo: user test in.
Blocked:
