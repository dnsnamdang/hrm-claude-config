# Phân tích ERP "Báo cáo thưởng năng suất tháng" (commission-month) để port sang HRM

Chỉ đọc. SELECT trên `erp_hrm_check` (127.0.0.1, DB local, lấy từ HRM `.env`; ERP `.env` đang trỏ DB remote nên không dùng). Ngày phân tích 16/11/2026.

Đường dẫn ERP (gốc `ERP/TanPhatDev`):
- Service: `app/Services/Reports/CommissionMonthReportService.php` (730 dòng)
- Controller: `app/Http/Controllers/ReportController.php:4352-4430`
- Routes: `routes/web.php:3250-3254` (`/admin/reports/commission-month`, `/searchData`, `/searchDetailData`, `/print`, `/export`)
- View + JS angular nằm chung: `resources/views/reports/commission_month.blade.php` (572 dòng, controller `Contract`; popup `#detailModal`)
- Class JS dựng dòng: `partials/classes/reports/BonusBusinessDepartment`
- Mẫu in: `ReportTemplate::BAO_CAO_THUONG_NANG_SUAT_THANG = 311` (`app/Model/Common/ReportTemplate.php:373`)

## 1. Nguồn số

Nguồn duy nhất là sổ `account_details` của TK 117 (= 3351 "Chi phí phải trả ngắn hạn", `accounts.id=117`), không dùng `cost_employees` hay bảng quyết toán trực tiếp (quyết toán chỉ gián tiếp, vì bút toán TNST do phiếu quyết toán HĐ sinh ra).

**Thưởng năng suất tháng** (`commission_month`), service `getCostEmployees()` dòng 276-370:
- `account_id = 117`, `invoiceable_type` NOT IN (BillPayment, BillPaymentAuthorization, ClosingEntry), `contractable_id` và `employee_id` NOT NULL.
- Mỗi (`contractable_id`, `contractable_type`, `contractable_code`, `employee_id`): `SUM(Có type=2 của work TNST) - SUM(Nợ type=1 của work TNST)` trên `money_value_exchange`. Work TNST id=13 (tra `Work::getByCode()`).
- Chỉ lấy 2 loại HĐ, UNION ALL:
  - `FirmContract` (HĐ hãng): join `firm_contracts` (+ `customers.code`, + `firm_support_accounting`), join INNER `departments` theo `firm_contracts.department_id`.
  - `WrServiceContract` (HĐ dịch vụ): join `wr_service_contracts` (+ `wr_support_accounting`), cũng INNER `departments`.
  - HĐ HRM (`Modules\Assign\Entities\Contract\Contract`), `ServiceContract`, `ProjectContract`...: KHÔNG có. (Các `use` ở đầu file thừa.) Trong DB local TNST hiện chỉ có Firm (46.270 dòng) và Wr (3.965 dòng).
- Dòng HĐ có `commission_month = 0` bị bỏ khi dựng bảng (dòng 424, `!= 0`).

**DS tiêu chuẩn tính thưởng NS tháng** (`getDoanhSoTieuChuan()` dòng 568-660), không đọc từ sổ mà tính từ HĐ/quyết toán, 3 nhánh:
1. HĐ hãng đã quyết toán (`status = 10 DA_QUYET_TOAN`): `settlement_contract_employees.commission_sale` của (HĐ, NV), qua `settlement_contract_departments` -> `firm_settlement_contract_detail.type = 2`. Lấy `[0]` (dòng đầu), không có thì 0. Không nhân tỷ lệ tháng, không chia theo kỳ.
2. HĐ hãng chưa quyết toán: `tnst_NV / tnst_tổng_HĐ * (commission_sale_HĐ / ti_le_huong_nv)`.
   - `commission_sale_HĐ` = `firm_support_accounting.commission_sale` (join theo `contractable_id`, KHÔNG theo type).
   - `tnst_tổng_HĐ` = tổng `commission_month` mọi NV của HĐ trong kỳ lọc (từ `$cost_employees`, không bị lọc theo quyền/NV).
   - `ti_le_huong_nv` = 100 nếu NV là `department_lead_id` của PHÒNG HIỆN TẠI đang xét (`$department`, không phải phòng của HĐ), còn lại là `commission_sale_percent` ở `firm_support_accounting_employees`.
3. HĐ dịch vụ: luôn đi công thức nhánh 2 (không xét quyết toán), nguồn `wr_support_accounting.commission_sale` + `wr_support_accounting_employees.commission_sale_percent`.
   - Chia cho `ti_le` (không nhân `ti_le/100`) - xem §5 mục 6.

**Bộ lọc & ý nghĩa**
- Lọc ngày (`filterDate`, dòng 372-390) trên `account_details.invoiceable_date_accounting` (ngày hạch toán của phiếu gốc), chặn `>= date_from 00:00:00`, `<= date_to 23:59:59`.
- FE cho 2 kiểu: (a) Năm + Tháng (`whereYear` + `whereMonth`), (b) Từ ngày - Đến ngày. 2 kiểu loại trừ nhau trên UI (`ng-disabled`). Bắt buộc: có (year hoặc month) HOẶC có cả 2 ngày (`checkConditionSearch`). Back-end KHÔNG kiểm gì (không bắt buộc).
- Có thể chọn riêng Tháng không Năm: `whereMonth` quét mọi năm.
- `Số hợp đồng` = `contractable_code` của sổ (so `=` chính xác, không LIKE). `Khách hàng` = `customer_id` của HĐ (`where customer_id`).
- Hiển thị dòng KH: `customer_code - customer_name`; firm: `customers.code` (live) - `firm_contracts.customer_name` (snapshot); wr: `wr_service_contracts.customer_code - customer_name` (snapshot).
- Bộ lọc tổ chức (công ty/phòng/bộ phận/NV, include `company-department-filter-singer`) không lọc sổ mà lọc `departments` + `employee_infos` hiện tại (xem §3).
- Hiển thị chỉ 2 cột số: DS tiêu chuẩn và Thưởng NS tháng. Không có cột TTHHD/TNSQ/TVC.

## 2. Cấu trúc bảng + popup

Bảng 5 cột: STT | Nhân viên (cột 2 cũng là mã HĐ ở dòng con) | Khách hàng | DS tiêu chuẩn tính thưởng NS tháng | Thưởng năng suất tháng.
- Dòng 1 (thead): Tổng cộng. `total.doanh_so_tieu_chuan`, `total.commission_month`.
- Dòng PHÒNG (in đậm, STT `n`): `department_code - department_name`, 2 số tổng.
- Dòng NV (STT `n.m`, tên là link mở popup): `employee_code - employee_name`, 2 số tổng.
- Dòng HĐ (STT `n.m.k`, chỉ khi bật checkbox "Show chi tiết" `form.expand`): mã HĐ | `customer_code - customer_name` | DSTC | thưởng.
- Phòng -> NV lấy theo PHÒNG HIỆN TẠI của NV (`employee_infos.department_id`, phòng `status = 1`), không theo phòng HĐ hay phòng ghi trên bút toán. NV có 0 HĐ vẫn hiện (0 / 0) nếu có bất kỳ bút toán TNST thuần khác 0 trong sổ nhưng tổng sau join = 0 (vd Có = Nợ): xem `rows` đã gom ở `getCostEmployees` (không HAVING).
- Phân trang theo PHÒNG: `per_page = 10`, `forPage` trên collection đã tính xong toàn bộ (`$data->forPage(...)`), tức mỗi lần đổi trang tính lại toàn bộ.
- Dòng Tổng cộng: dòng 56-59 cộng `total_commission_month` / `total_doanh_so_tieu_chuan` của TẤT CẢ phòng (toàn bộ tập, không chỉ trang). Nếu rỗng thì `$total = []` (xem §5).

**Popup chi tiết** (bấm tên NV; `commissionMonthSearchDetailData` -> `getDetailByEmployee`, dòng 460-536):
- Tham số JS gửi: `employee_id`, `date_from`, `date_to`, `contract_code`, `invoiceable_code`, `per_page`, `current_page`. (KHÔNG gửi `year`, `month`, `customer_id`.)
- Truy vấn `AccountDetail` (TK 117, loại trừ 3 invoiceable type, NV đó) group by (`contractable_id`, `contractable_type`, `invoiceable_id`, `invoiceable_type`) tính `commission_month` TNST. Sau đó `groupBy('contractable_id')` trong PHP, tức mỗi HĐ nhiều phiếu (invoiceable).
- Cột popup: STT | Tên hàng | Mã hàng | SL | Đơn giá tiêu chuẩn | Doanh số tiêu chuẩn | Thưởng NS tháng. Dòng HĐ (mã `contractable->code`), dòng phiếu (`invoiceable->code` + thưởng của phiếu), dòng mặt hàng (qty, price, qty*price).
- Mặt hàng chỉ lấy khi `invoiceable_type` là `ProductExport` (cột `price`) hoặc `ProductImport` (cột `supplier_price`). Các loại khác để mảng rỗng.
- Phân trang theo HĐ (`forPage` trên nhóm HĐ).
- DB local: `invoiceable_type` của sổ TNST ngoài ClosingEntry chỉ còn `SettlementContract` (25.700) và `BillAdjustDept` (61). Không có PXK/PNK nên phần "mặt hàng" của popup LUÔN RỖNG trong dữ liệu thực. Popup thực chất chỉ liệt kê HĐ -> phiếu quyết toán + thưởng.

## 3. Phân quyền (mã `accounting.bao_cao_thuong_nang_suat_thang.view`, scope 1-4)

Mã đã có trong HRM catalog `hrm-api/app/Support/Permissions/Catalog/accounting.php:629` nhưng `platforms => ['erp']` (chưa có `'hrm'`).

Hằng: `PermissionScope::PART=1, DEPARTMENT=2, COMPANY=3, GROUP=4`. Cờ CỘNG DỒN: `is_all_company = scope>=4`, `is_company >=3`, `is_department >=2`, `is_part >=1`. Màn không gate (ai cũng vào được); mã chỉ mở rộng phạm vi.

`getDataDepartment` (dòng 164-283, hàm đang dùng) áp lên `departments` JOIN `employee_infos` hiện tại (không áp lên bút toán):
| Cấp | Điều kiện |
|---|---|
| 4 Tổng công ty | không giới hạn thêm |
| 3 Công ty | `departments.company_id = info.company_id` HOẶC `emp.id = tôi` |
| 2 Phòng ban | `departments.id` IN (`employee_manage_departments` của tôi, cùng `company_id` hồ sơ) HOẶC `emp.id = tôi` |
| 1 Bộ phận | `parts.id = info.part_id` HOẶC `emp.id = tôi` |
| không quyền (0) | `emp.id = tôi` |
Cộng thêm: luôn `emp.id IN (nhân viên có số trong kỳ)`, `departments.status = 1`; `request.company_id/department_id/part_id/employee_id` lọc thêm.

Lưu ý: `$cost_employees` (cũng dùng làm mẫu số `tnst_tổng_HĐ` của DSTC) KHÔNG bị áp quyền, chỉ áp quyền ở danh sách NV/phòng. Tổng đúng, nhưng số NV khác hiện bằng hiệu ứng DSTC (không lộ tiền).

`getDataDepartment_` (có dấu `_`, dòng 71-162, bản Eloquent cũ): KHÔNG còn nơi nào gọi (grep toàn `app/`, `routes/`). Code chết, bỏ qua khi port.

## 4. In / Excel

- In (`commissionMonthPrint`): view `print_landscape`, mẫu 311 (954 ký tự: `{{HEADER}}` ảnh, tiêu đề "BÁO CÁO THƯỞNG NĂNG SUẤT THÁNG", `{{CHI_TIET}}`, chân "Ngày ... Tháng ... Năm ... Người lập"). Truyền thêm `NGAY/THANG/NAM/TU_NGAY/DEN_NGAY` nhưng mẫu không dùng (mẫu không in khoảng ngày).
- Bảng `printListData()` (dòng 662-728): thead 5 cột (STT 70px | Nhân viên 250 | Khách hàng 450 | DSTC 180 | Thưởng NS tháng 180), dòng thứ 2 của thead = Tổng cộng (colspan 3 + 2 số). Dòng phòng (đậm, colspan=2 ở cột 2-3), dòng NV (chữ xanh `#1abc9c`, cột KH trống), dòng HĐ chỉ khi `request.expand`. Số 0 -> `-`. Dùng `formatCurrency`.
- Excel (`commissionMonthExport`): dùng `PositionInventoryReportList` (class của báo cáo khác), cùng bảng HTML ở trên, `TITLE`, `TU_NGAY`, `DEN_NGAY`, `HEADER`, `COLSPAN = 5`, file `bao_cao_thuong_nang_suat_thang.xlsx`.
- In/Excel gọi `commissionMonthSearchData` KHÔNG phân trang (không có `per_page`) nên in toàn bộ; cùng quyền.
- Nút In/Excel chỉ bật khi `data.length` có (bảng trang hiện tại), nhưng URL lấy `form` (kể cả `expand`).

## 5. Nghi lỗi ERP (đã đối chiếu SELECT trên `erp_hrm_check`)

1. **NV/tổng bị nhân lên theo số bộ phận của phòng** (`getDataDepartment` dòng 168-171: `leftJoin parts on parts.department_id = departments.id`, sau đó `groupBy('id')` rồi `'employees' => $dep`). Mỗi dòng NV lặp `số_parts` lần: phòng id 47 (6 bộ phận) tháng 05/2026: 16 NV thật -> 96 dòng; id 50 (2 bộ phận): 3 -> 6; id 67 (4): 2 -> 8. Tổng phòng/Tổng cộng cũng nhân theo. Chỉ có 8 phòng có bộ phận nhưng là các phòng lớn nhất. Đây là lỗi nặng nhất, port phải gom đúng 1 dòng/NV.
2. **Cờ quyền cộng dồn làm lọc bộ phận áp cho cả cấp cao** (dòng 190-192: `if ($permissions['is_part'] && $user->info->part_id) where ei.part_id = ...`). `is_part` là true với mọi scope >= 1, nên người có quyền Phòng/Công ty/Tổng công ty mà hồ sơ có `part_id` chỉ thấy NV cùng bộ phận (mất NV khác). Vi phạm ý quyền cấp cao.
3. **HĐ nhân đôi dòng do join hỗ trợ kế toán theo `contractable_id` thôi** (dòng 281-285 `leftJoin firm_support_accounting sp on frc.id = sp.contractable_id`, wr tương tự 332-335): thiếu `contractable_type`/DISTINCT. `firm_support_accounting` có 2 dòng cùng id cho HĐ hãng 13 và 15 (1 dòng FirmContract + 1 dòng `Modules\Assign\Entities\Contract\Contract` cùng id); `wr_support_accounting` có HĐ 3948 với 2 dòng thật. Các HĐ này có sổ TNST (13: 4 dòng, 15: 4, 3948: 4) nên trong kỳ chỉ nhìn 1 nửa (vd 13: Có 30/09/2025 17.645 + 2.406, Nợ 31/12/2025 cùng số) thưởng NV hiện NHÂN ĐÔI (cost_employees trả 2 dòng). Cộng thêm `commission_sale` hiện cùng số nhưng ghép nhầm HĐ HRM. Đã gặp 2 HĐ hãng và 1 HĐ dịch vụ trong DB local.
4. **Crash khi NV không có dòng hỗ trợ kế toán** (dòng 618, 649: `$spa_employee->commission_sale_percent` trên `null`; hoặc `/ 0`): chỉ NV không phải trưởng phòng của phòng đang xét, không có `*_support_accounting_employees`. Local 2026: HĐ dịch vụ có 658 cặp (HĐ,NV) không phải trưởng phòng, 3 cặp không có dòng -> khi lọc đúng kỳ chứa chúng, PHP 7 bắn "Trying to get property of non-object" (ErrorException), controller bắt `\ErrorException` rồi `dd($e)` (ReportController:4372) = trả trang debug / vỡ màn. HĐ hãng hiện đã quyết toán gần hết nên nhánh crash này ít lộ (status<>10, không có cặp thiếu trong 2026).
5. **`dd($e)` + `throw new Exception` không import** (ReportController:4371-4374): lỗi trả dump HTML ở production; ngoài `ErrorException` thì lỗi khác bay thẳng.
6. **Công thức DSTC nhánh chưa quyết toán/DV chia cho tỷ lệ**: `tnst_NV / tnst_tổng * (commission_sale / ti_le)`. Với tỷ lệ 100 (21.599/22.2xx dòng `firm_support_accounting_employees`) ra `commission_sale/100 * share`, tức bằng `1%` DS, trùng đúng số thưởng khi TNST = 1% (vd HĐ 937 tháng 05/2026: share 0,35 x 2.822.450.000/100 = 9.878.575 = đúng tiền thưởng NV 263). Với tỷ lệ khác 100 (50%: 264 dòng, 30%: 154, 70%: 148...) chia thay vì nhân nên DSTC bị đảo (50% -> x2). Nghi sai công thức/đơn vị; cần xác nhận nghiệp vụ trước khi port (có thể ý đồ "DSTC quy theo thưởng").
7. **Nhánh đã quyết toán lấy `[0]` bừa**: `settlementContractEmployees[$key][0]`. Local có 12.125 khóa (HĐ,NV) có nhiều dòng quyết toán loại 2 (bản nháp `settlement_contract_id NULL` + bản chính), 357 khóa giá trị khác nhau. Giá trị `[0]` phụ thuộc thứ tự không `ORDER BY`. Còn DSTC nhánh này là CẢ giá trị quyết toán của NV, lặp lại ở MỌI tháng HĐ có TNST (không quy theo kỳ) - cộng nhiều tháng sẽ cộng trùng.
8. **Key map gom `groupBy` dùng `CONCAT(contractable_id,'-',type,'-',employee_id)` trên `FirmSupportAccountingEmployee::groupBy(...)->get()`** (dòng 408-417): `select id, ..., groupBy` không có aggregate, chỉ chạy được khi tắt ONLY_FULL_GROUP_BY (ERP prod có thể tắt, DB local đang BẬT: truy vấn này sẽ lỗi 1055 nếu chạy ở HRM). Chọn dòng ngẫu nhiên khi NV có nhiều dòng (nhiều phòng).
9. **N+1 / O(N²) nặng**: `renderDataBonusBusinessDepartments` quét `$cost_employees->flatten()` cho từng NV (dòng 426), rồi mỗi HĐ gọi `getDoanhSoTieuChuan` tự `flatten()->toArray()` + 2 `array_filter` trên TOÀN tập (dòng 586-594, 636-644), + `spa_employees->filter` mỗi lần. Số cặp (HĐ,NV) có TNST thật (đo SELECT): tháng 05/2026 = 2.756 (1.352 HĐ, 128 NV); cả năm 2026 = 14.563 (7.135 HĐ, 164 NV); cả năm 2025 = 11.114. Ước ~10^8-10^9 phép với 1 năm -> timeout/ngốn RAM. Ngoài ra `FirmSupportAccounting::select(...)->get()` lấy cả bảng (21k) mỗi lần và `settlement_contract_employees` toàn bộ không lọc kỳ. In/Excel chạy lại toàn bộ tính.
10. **Phân trang giả**: tính hết rồi mới `forPage`; mỗi lần đổi trang chạy lại toàn bộ.
11. **Mất tiền khi NV không thuộc phòng active**: join INNER `departments status=1` + `whereIn emp.id` qua `ei.department_id`. NV chuyển phòng / phòng đóng thì thưởng biến khỏi bảng và khỏi tổng (local tháng 05/2026: 0 NV bị rớt, nhưng cơ chế có thật). Tương tự HĐ không có `department_id` (INNER JOIN `departments d`) bị loại.
12. **Tổng phòng**: `$item['total_*']` chỉ gán trong vòng NV; nếu phòng không còn NV (sau `forPage`/lọc) -> `Undefined index` (dòng 77-78 `$item['total_commission_month'] ?? 0` đã đỡ phần cộng nhưng view hiển thị trống). In: `$data['total']['doanh_so_tieu_chuan']` khi `$total = []` (kết quả rỗng) -> Undefined index (dòng 721-722).
13. **Popup không kiểm quyền** (`getDetailByEmployee`): nhận `employee_id` bất kỳ, không áp scope -> rò thưởng của người khác (cùng lỗi đã ghi trong plan `bc-thuong-theo-nhan-vien` §6 mục 3).
14. **Popup gom HĐ chỉ theo `contractable_id`** (dòng 487 `groupBy('contractable_id')`): HĐ hãng và HĐ DV trùng id bị trộn, mã HĐ/ loại lấy từ phần tử đầu.
15. **Popup mất điều kiện năm/tháng**: JS chỉ gửi `date_from/date_to` (không `year/month`) -> khi người dùng lọc theo Năm/Tháng, popup lấy TOÀN BỘ thời gian (số tổng popup khác bảng). Cũng không gửi `customer_id`.
16. **Popup phân trang lỗi**: `uib-pagination` của modal dùng `total-items="total_items"` + `ng-model="current.page"` của bảng chính (`$scope.total_ = response.total` gán sai tên, response không có `total`), nên đổi trang popup đổi cả `current.page` bảng chính.
17. **Popup N+1 + null**: mỗi phiếu truy vấn chi tiết mặt hàng riêng; `$invoice->invoiceable->code` và `$item[0]->contractable->code` vỡ nếu phiếu/HĐ đã xóa. Cột "Đơn giá tiêu chuẩn / DS tiêu chuẩn" thực ra là đơn giá phiếu xuất/nhập (không liên quan DSTC tính thưởng).
18. **Lọc**: Tháng không Năm quét mọi năm; `contract_code` so bằng `=` (HRM báo cáo anh em dùng LIKE); không kiểm ngày ở back-end; `date_from` ngày sai định dạng ném `InvalidArgumentException`.
19. **Mã thừa**: bảng phụ `fs` (`firm_settlement_contract_detail` SUM) leftJoin nhưng không dùng; join `customers c` ở nhánh wr không dùng; `use` thừa nhiều lớp; `getDataDepartment_` chết (§3).
20. **So khớp type-bị-lệch**: `firm_support_accounting` join không có `contractable_type` (xem mục 3) và `FirmSupportAccounting::select(...)` ($firm_support_accounting) nạp nhưng không dùng.

## 6. Gợi ý cho HRM

Khuôn gần nhất đã port: `hrm-api/Modules/Finance/Services/BonusEmployee/*` (Phòng -> NV theo phòng hiện tại `employee_infos.department_id`, `rows()/tree()/totals()/search()` phân trang theo phòng 10/trang, `detailRows()` popup + `employeeInScope`, `BonusEmployeePrintTable`, Scope kế thừa `SalesIncomeScope`). Màn "Thưởng theo hợp đồng" dùng `BonusContractReport/BonusLedger::sums()` (sổ `identify_number='3351'`, 4 cột TTHHD/TNST/TNSQ/TVC, index `idx_ad_identify_date_ctype`).

Khuyến nghị:
- Số TNST: tái dùng `BonusLedger::sums()` (hoặc `entriesQuery` của BonusEmployee) với `groupBy` (`ad.contractable_type`, `ad.contractable_id`, `ad.contractable_code`, `ad.employee_id`); chỉ cần cột `commission_month` (cắt 3 cột khác khỏi select/having, nhưng đổi HAVING còn `commission_month != 0` để khớp ERP dòng 424). Lọc ngày dùng `start_date/end_date` (Y-m-d) như BonusLedger; năm/tháng của ERP có thể quy về 2 ngày để bỏ `whereYear/whereMonth` (giữ index).
- Phạm vi: BonusLedger/BonusContractScope áp lên cột tổ chức của BÚT TOÁN, còn ERP commission-month áp lên PHÒNG/BỘ PHẬN HIỆN TẠI của NV. Để giống ERP và sửa lỗi 2 (cờ cộng dồn), dùng khuôn `BonusEmployeeScope` / `SalesIncomeScope` (theo `employee_infos`), thêm mã `accounting.bao_cao_thuong_nang_suat_thang.view` làm `CODE`. Cần user chốt (plan chị em đã chọn khác nhau: HĐ = cột bút toán, NV = phòng hiện tại; màn này ở ERP thuộc loại "NV theo phòng hiện tại").
- DB: cần thêm `'hrm'` vào `platforms` ở `accounting.php:629-640` + `permission:catalog-sync` khi deploy. Menu: placeholder chuỗi `'Thưởng năng suất tháng'` ở `hrm-client/components/subsystem-menu/sale-hub.js:~266` (nhóm "Thưởng - Thu nhập"), đổi sang `{ n: ..., link: '/sale/commission-month' }`, KHÔNG khai `codes/isShow` như 2 màn kia.
- Nguồn HĐ: UNION 3 nguồn bằng LEFT JOIN theo cả `contractable_type` + `contractable_id` (tránh lỗi 3, 14):
  - `firm_contracts` + `customers.code`, `wr_service_contracts` (mã KH + tên snapshot),
  - THÊM `hrm_contracts` (type `Modules\Assign\Entities\Contract\Contract`, cùng cách bên `BonusEmployeeReportService::detailRows` dòng 145-190 đã có join `hrm_contracts h` + `customers c`).
  - ERP hiện chỉ UNION firm + wr; HĐ HRM chưa có bút toán TNST (plan chị em cũng ghi vậy), cần nhánh chạy khi bắt đầu có số. DSTC của HĐ HRM = 0 như plan HĐ (không có công thức nguồn).
- DSTC: cần quyết định nghiệp vụ trước (mục 5.6, 5.7). Gom `firm_support_accounting`, `wr_support_accounting`, `*_employees`, `settlement_contract_employees` thành JOIN/array map 1 lần (không O(N²)), key = (type, id[, employee]). Nếu bám ERP 1:1: nhánh đã quyết toán lấy dòng nào (nên SUM hay dòng bản chính `settlement_contract_id` NOT NULL, ghi rõ trong §lệch); nhánh chưa QT bảo vệ chia 0 / thiếu dòng (coi 0).
- Chính sách lỗi nên sửa ở HRM (ghi vào design mục lệch): 5.1 (nhân dòng theo bộ phận), 5.2 (cờ quyền cộng dồn), 5.3 (join thiếu type), 5.4 (thiếu dòng SPA -> 0), 5.13 (kiểm quyền popup), 5.14 (gom theo type+id), 5.15/5.16 (popup đúng kỳ + phân trang riêng), 5.9 (tính 1 lần).
- Popup: ERP phần mặt hàng gần như luôn rỗng (chỉ PXK/PNK; sổ TNST thật là SettlementContract/BillAdjustDept). Đề xuất HRM popup liệt kê HĐ -> phiếu (invoiceable) + thưởng (+ mã phiếu), có link; chỉ port tầng mặt hàng nếu user muốn (hỏi). Cần xác nhận với user.
- In: dùng lại mẫu 311, truyền `CHI_TIET`, `HEADER` (mẫu không dùng ngày). Excel FE khuôn `export-excel.js` + cột 5 như bảng; tên file `bao_cao_thuong_nang_suat_thang.xlsx`.
- Chi phí: dùng 1 truy vấn sổ + 1 truy vấn NV/phòng + 1 truy vấn HĐ (IN theo trang cho popup).

## 7. Độ lớn dữ liệu (DB local `erp_hrm_check`)

- `account_details` TK 117: 146.706 dòng tổng; work TNST (id 13): ~50k dòng (Firm 46.270, Wr 3.965), ngày từ 02/2025 tới 11/2026; 52 dòng thiếu ngày hạch toán.
- Theo tháng (TNST, đã loại 3 invoiceable type, có employee + HĐ): 940 - 3.964 dòng/tháng, 78 - 150 NV, 439 - 1.944 HĐ. Tháng 05/2026: 2.756 dòng, 1.352 HĐ, 128 NV. Tháng cao nhất 12/2025: 3.964.
- Cặp (HĐ, NV) có TNST thuần khác 0 (hàng ERP phải lặp): tháng 05/2026 = 2.756; năm 2026 = 14.563 (7.135 HĐ, 164 NV); năm 2025 = 11.114 (5.503 HĐ, 156 NV).
- Phiếu nguồn: chỉ `SettlementContract` 25.700 + `BillAdjustDept` 61 (ngoài ClosingEntry 24.474 bị loại).
- Phòng/NV: 128 NV/tháng chia ~dưới 40 phòng; 8 phòng active có `parts` (phòng 47 có 6).
- `firm_support_accounting` 21.405 dòng, `wr_support_accounting` 2.471, `firm_support_accounting_employees` ~22k (đa số 100%). Cặp (HĐ,NV) không phải trưởng phòng và không có SPA: HĐ hãng đã QT 156/1.373 (tháng 05/2026) - nhánh QT nên không crash; HĐ DV 3/658 (2026).
- Báo cáo 1 năm ERP có thể chậm/timeout vì O(N²); HRM với 1 truy vấn gom (~15k dòng/năm) nhẹ.
