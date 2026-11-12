# Port "Bảng tổng hợp thu nhập từ bán hàng" ERP → HRM

Ngày: 09/11/2026 · Trạng thái: chờ user duyệt

## 1. Mục đích

Đưa màn báo cáo ERP `report.commission_settlement_quarter` ("Bảng tổng hợp thu nhập từ bán hàng") sang HRM, **bám ERP 1:1** (user chốt), với **một thay đổi duy nhất**: bỏ 2 cột "DS tính thưởng năng suất tháng" và "DS tiêu chuẩn tính thưởng năng suất quý", thay bằng **1 cột "DSTC quyết toán"**.

### Kiểm chứng cột DSTC (user nhờ tự check — ĐÚNG)
- ERP `app/Services/Reports/CommissionSettlementQuarterReportService.php:170-171` (nhánh HĐ hãng) và `:327-328` (nhánh YCSC/BD): cả `standard_month` lẫn `standard_quarter` đều là `round(settlement_firm.commission_sale)` → hai cột luôn bằng nhau.
- ERP `app/Services/BonusVariableAggregatorService.php:97-110`: biến `dstc_quyet_toan_nv` lấy từ `standard_quarter`.
- ⇒ "DSTC quyết toán" = `standard_quarter`, đổi tên. Gộp không mất dữ liệu.

## 2. Mục tiêu / Không làm / Phản mục tiêu

**Mục tiêu**
- Màn HRM cho ra **cùng số liệu** với ERP trên cùng DB gộp, cùng bộ lọc, cùng người xem có cùng quyền.
- Đủ các phần ERP có: bộ lọc, bảng tổng phòng → NV (có dòng tổng), popup chi tiết theo HĐ, In + Xuất Excel cho cả bảng tổng và popup chi tiết.
- Cột DSTC quyết toán thay 2 cột cũ ở cả 4 nơi: bảng, popup, bản in, Excel (và dòng tổng).

**Không làm**
- Không đổi công thức bất kỳ cột thưởng nào; không sửa ERP (màn ERP giữ nguyên).
- Không thêm cột/lọc mới ngoài ERP.

**Phản mục tiêu (dù chạy được vẫn là hỏng)**
- Số lệch ERP ở bất kỳ cột nào.
- Người không quyền thấy được thu nhập của người khác (ở bảng, dòng tổng, popup, in, Excel — mọi truy vấn phải qua phạm vi quyền).

## 3. Nguồn ERP cần bám (đọc kỹ trước khi làm)

ERP repo: `ERP/TanPhatDev` (Laravel 6).
- Routes `routes/web.php:3395-3417` → `ReportController@commissionSettlementQuarter*` (`ReportController.php:4587-4760`): index, searchData (tổng + phân trang trong PHP + `indexData` đánh STT phòng/NV), commissionSettlementQuarterGetDetail (popup), print, export, printDetail, exportDetail.
- Service `app/Services/Reports/CommissionSettlementQuarterReportService.php`: `getDataFirm` (HĐ hãng) UNION ALL `getDataWr` (YCSC/BD), `getData` gom theo NV; khi có `period` thì leftJoin `bill_commission_settlement_quarter_employees` (phiếu QT quý status CREATED) lấy `progressive_approval_percent`; `filterAcc` (lọc ngày theo `ac.invoiceable_date_accounting`, mã HĐ, KH, công ty/phòng/bộ phận, NV + phạm vi quyền); `render`.
- View `resources/views/reports/commission_settlement_quarter.blade.php` (AngularJS): bộ lọc, bảng, popup, cách hiển thị.
- In/Excel: `app/Services/PrintTemplate/CommissionSettlementQuarterPrint.php`, `CommissionSettlementQuaterDetailPrint.php`, `resources/views/reports/exports/commission_settlement_quater.blade.php`, `commission_settlement_quater_detail.blade.php`.

## 4. Mô tả màn HRM

### Bộ lọc (như ERP)
- Công ty / Phòng ban / Bộ phận (+ Nhân viên nếu ERP partial có) — dùng `V2BaseCompanyDepartmentFilter` như các báo cáo đã port.
- Năm + Kỳ quyết toán: danh sách kỳ lấy từ `companies.config_settlement_period` (JSON theo năm → `details[{period,date_from,date_to}]`) của **công ty đang chọn** (`current_company_role`), không phải "công ty nhà" của NV. Chọn kỳ → tự điền Từ/Đến ngày và khoá 2 ô ngày (như ERP). Mặc định năm hiện tại.
- Từ ngày / Đến ngày: bắt buộc.
- Xuất hoá đơn: Tất cả / Xuất hoá đơn (=1) / Không xuất hoá đơn (=0 hoặc NULL).
- Nút Lọc, Làm mới, In, Xuất Excel.

### Bảng tổng
Nhóm theo phòng → NV (STT phòng / STT NV như `indexData` ERP), có dòng Tổng cộng tính trên **toàn bộ** kết quả (không chỉ trang hiện tại). Cột:
STT · Nhân viên · **DSTC quyết toán** (`standard_quarter`) · Thưởng NS tháng · Thưởng NS quý · Tổng thưởng NS lũy tiến · Thưởng thêm · Thưởng thực hiện HĐ · Tiền vận chuyển · Tổng thu nhập từ bán hàng · Lãi quá hạn · Thưởng NS bị trừ quá hạn.
(Ánh xạ field và công thức cột suy diễn — lũy tiến, tổng thu nhập — lấy đúng như view/`render` ERP.)

### Popup chi tiết (bấm vào NV)
Lọc thêm: Hợp đồng (mã), Khách hàng. Cột: STT · Hợp đồng · Khách hàng · Số quyết toán · Ngày bàn giao · Ngày thanh toán · **DSTC quyết toán** · các cột thưởng như bảng tổng. Có In + Xuất Excel của chi tiết. Popup dùng `V2BaseModal`.

### In / Xuất Excel
Bố cục bám mẫu ERP, chỉ thay 2 cột DSTC bằng 1 cột. Cách dựng file theo khuôn các báo cáo HRM đã port (xem §6).

### Menu
Gắn link vào cả 2 placeholder đang có (quyết định của Claude, bám ERP vốn đặt màn ở 2 menu):
- `hrm-client/components/subsystem-menu/finance.js:398` (Kế toán › Báo cáo bán hàng).
- `hrm-client/components/subsystem-menu/sale-hub.js:266` (Thưởng - Thu nhập › "Tổng hợp thu nhập từ bán hàng").
Không khai `isShow` (ai cũng vào được).

## 5. Quyền (như ERP)

- Màn **không gate**: ai cũng vào được; không quyền nào thì chỉ thấy số của **chính mình** (`ac.employee_id = mình` — ERP lọc theo NV hưởng, KHÔNG theo người tạo HĐ).
- 4 quyền mở rộng phạm vi, ưu tiên cấp cao nhất user có:
  - tổng công ty: không giới hạn
  - công ty: `employee_company_id` = công ty đang chọn, HOẶC của mình
  - phòng ban: `employee_department_id` ∈ phòng mình quản lý, HOẶC của mình
  - bộ phận: `employee_part_id` ∈ bộ phận mình quản lý, HOẶC của mình
- Phạm vi áp cho **mọi** truy vấn: hai nhánh UNION, subquery phiếu QT quý (`csq_employee.*`), dòng tổng, popup, in, Excel.
- Tên quyền giữ nguyên tên ERP (đã có trong DB gộp, guard `web`, id 100308-100311): "Xem báo cáo tổng thu nhập từ bán hàng - tổng công ty / - công ty / - phòng ban / - bộ phận". Thêm 4 dòng guard `api` vào `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (`$this->perm([... 'group' => 'Báo cáo tổng thu nhập từ bán hàng', 'type' => 23])`) + `permission_legacy_ids.php`, theo đúng cách các quyền báo cáo công nợ KH đã làm (dòng ~1718).
- Phòng/bộ phận quản lý lấy theo chuẩn HRM `listManageDepartmentIds()` / `listManagePartIds()`, công ty = `current_company_role` (giống `CustomerDebtScope`).
- 09/11/2026 user chốt: cấp **bộ phận** gồm cả bộ phận CỦA MÌNH (`info->part_id`) như ERP `filterAcc` is_part, cộng thêm bộ phận mình quản lý. Cấp phòng ban giữ `listManageDepartmentIds()`. Push develop api e08285357.

## 6. Ràng buộc kỹ thuật

- HRM đọc thẳng bảng ERP trong DB gộp (`account_details`, `settlement_firm`, `firm_support_accounting_employees`, `bill_commission_settlement_quarter*`, `works`…), port lại SQL của ERP, chỉ bỏ cột trùng `standard_month`.
- Khuôn tham chiếu trong HRM: báo cáo "Tổng hợp công nợ KH theo NV" — `hrm-api/Modules/Finance/Http/Controllers/V1/CustomerDebtByEmployeeController.php`, `Modules/Finance/Services/CustomerDebt/CustomerDebtByEmployeeReportService.php`, `CustomerDebtScope.php`, route `Modules/Finance/Routes/api.php:1924`, client `hrm-client/pages/sale/customer-debt-by-employee/index.vue`.
- `CustomerDebtScope` hard-code cột "của mình" là `contract_created_by` nên **không dùng thẳng** được. CLAUDE.md HRM: sửa hàm dùng chung phải hỏi trước → **quyết định của Claude**: viết scope riêng cho báo cáo này (hoặc lớp con), không sửa `CustomerDebtScope`.
- Đặt code ở module Finance; URL client đề xuất `/sale/sales-income-summary` (quyết định của Claude, builder có thể đổi cho khớp quy ước).
- Form/popup dùng V2Base*.
- Bẫy gộp DB đã biết: đọc config theo công ty phải lọc đúng công ty (không lấy dòng đầu); query nối nhiều bảng phải qualify cột (`company_id`, `employee_id` ambiguous).

## 7. Kiểm thử / nghiệm thu

- Test feature API: phạm vi 5 mức (không quyền / bộ phận / phòng / công ty / tổng công ty) — dòng, tổng, popup đều bị lọc; lọc kỳ/ngày/xuất HĐ; response chỉ có một trường DSTC quyết toán.
- Đối chiếu số: chọn ít nhất 1 kỳ có dữ liệu trên DB local, so tổng từng cột HRM với ERP (`standard_quarter` ERP = DSTC quyết toán HRM; các cột còn lại bằng nhau).
- Trình duyệt: mở màn từ cả 2 menu, lọc, mở popup, In, Xuất Excel. Tài khoản local thiếu quyền → có thể cần giả lập response.

## 8. Để builder tự quyết
Tên class/route/file cụ thể, cách chia component FE, phân trang server hay client (miễn dòng tổng đúng toàn bộ), cách dựng file In/Excel theo khuôn HRM hiện có.
