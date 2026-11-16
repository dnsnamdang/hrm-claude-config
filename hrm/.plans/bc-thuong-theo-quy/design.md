# Port "Báo cáo thưởng theo quý" ERP → HRM

Ngày: 16/11/2026 · Trạng thái: user bảo "làm đi" (bỏ hỏi) — các quyết định ở §6 là của Claude, xem khi nghiệm thu.

## 1. Mục đích

Đưa màn ERP `report.commissionQuarter` ("Báo cáo thưởng theo quý", menu Báo cáo thu nhập) sang HRM.
Số liệu phải giống ERP trên DB gộp. Màn chỉ đọc.

## 2. Mục tiêu / Không làm / Phản mục tiêu

**Mục tiêu**
- Có đủ như ERP:
  - bộ lọc;
  - bảng 3 cấp Phòng → NV → HĐ, có dòng Tổng cộng;
  - popup chi tiết theo NV;
  - In và Xuất Excel.
- Phạm vi quyền 4 cấp theo mã `accounting.bao_cao_thuong_nang_suat_thang.view` (mã ERP đang dùng cho màn này).

**Không làm**
- Không đổi công thức 6 cột.
- Không thêm cột.
- Không vá ERP (khác đợt "thưởng theo NV"). Lỗi ERP tìm thấy ghi ở §7, để user quyết.

**Phản mục tiêu**
- Số HRM lệch ERP ở bất kỳ dòng hoặc cột nào, cùng khoảng ngày và cùng phạm vi.
- Người không có quyền thấy số của người khác. Áp cho bảng, dòng tổng, popup, In, Excel.

## 3. Nguồn ERP

Repo `ERP/TanPhatDev`:
- **Service** `app/Services/Reports/CommissionQuarterReportService.php`: `getDataFirm`, `getDataWr`, `getData`, `render`, `filterAcc`, `printListData`.
- **Controller** `ReportController.php:4431-4587`:
  - `commissionQuarter`, `commissionQuarterSearchData`, print, export.
  - Popup gọi lại searchData với `employee_id` + `detail=1`.
- **View** `resources/views/reports/commission_quarter.blade.php`.
- **In:** `report_templates.id = 360` (`BAO_CAO_THUONG_THEO_QUY`), khổ ngang.
  - Biến: `CHI_TIET`, `TU_NGAY`, `DEN_NGAY`, `HEADER`.
- **Excel:** tiêu đề "Báo cáo thưởng theo quý", file `bao_cao_thuong_theo_quy.xlsx`.

## 4. Số liệu (bám ERP 1:1)

**Một dòng gốc = 1 (HĐ, NV hưởng).** Gồm 2 nhánh UNION ALL:
- HĐ hãng: `FirmContract`, mã và khách lấy từ `firm_contracts` + `customers`.
- HĐ dịch vụ: `WrServiceContract`, lấy từ `wr_service_contracts.customer_code/customer_name`.

**Bút toán gốc** (`account_details ac`):
- Điều kiện: `account_id = 117`; `invoiceable_type` không thuộc BillPayment / BillPaymentAuthorization / ClosingEntry; `contractable_id` và `employee_id` khác NULL.
- Ngày `invoiceable_date_accounting` (theo ngày) nằm trong [Từ, Đến].
- Gom theo `(contractable_id, employee_id)`.
- **Phòng của dòng** = `ac.employee_department_id` (phòng ghi trên bút toán). Khác màn "thưởng theo NV", vốn xếp theo phòng hiện tại.

**6 cột:**

| Cột | Công thức |
|---|---|
| DS tiêu chuẩn tính thưởng NS quý `commission_sale` | `round(COALESCE(sf.commission_sale, lead.commission_sale))` |
| Thưởng thực hiện HĐ `diff_employee_amount` | Σ Có − Σ Nợ của `money_value_exchange`, work `TTHHD` |
| Thưởng NS quý theo dự toán `commission_quarter_estimate` | `round(COALESCE(sf.estimate, lead.estimate))` |
| Thưởng NS quý thực tế `commission_quater_real` | `round(COALESCE(sf.real, lead.real))` |
| Tổng thưởng theo quý `total` | `diff_employee_amount + round(real)` |
| Thưởng NS quý bị trừ quá hạn `overdue` | `round(estimate) − round(real)` |

Tên `commission_quater_real` cố ý giữ đúng lỗi chính tả của ERP.

**Subquery `sf`** — phần của NV. Ghép với dòng gốc theo `contractable_id` + `employee_id`.
- Chuỗi bảng: `settlement_contract_employees sce` → `settlement_contract_departments scd` → `firm_settlement_contract_detail fscd` (với HĐ DV là `wr_settlement_contract_details`) → `settlement_contracts sc`.
- Ghép thêm `firm_support_accounting_departments fsad` (HĐ DV: `wr_support_accounting_departments`) theo `contractable_id` + `department_id`.
- Lọc: `type = 2`; `sc.date_accounting` trong [Từ, Đến].
- Gom theo `(sce.contractable_id, sce.employee_id)`.
- Các cột:
  - `commission_sale = sce.commission_sale`
  - `real = scd.after_settlement_employee_amount × sce.commission_sale_percent / 100`
  - `estimate = sce.commission_sale × fsad.after_commission_percent / 100 × fsad.after_settlement_employee_percent / 100`

**Subquery `lead`** — phần trưởng phòng. Ghép theo `contractable_id` + `ac.department_id`.
- Gom theo `(scd2.contractable_id, scd2.department_id)`.
- Các cột:
  - `commission_sale = scd2.commission_sale`
  - `real = scd2.after_settlement_department_lead_amount`
  - `estimate = scd2.commission_sale × fsad2.after_commission_percent / 100 × fsad2.after_settlement_department_lead_percent / 100`

**Bộ lọc của ERP:**
- Công ty / Phòng / Bộ phận → `ac.employee_company_id/department_id/part_id`.
- NV → `ac.employee_id`.
- Số HĐ → `ac.contractable_code LIKE`.
- Khách hàng → `ac.contract_customer_id`.
- Từ ngày / Đến ngày.

**Dòng Tổng cộng** tính trên toàn bộ dòng gốc, kể cả dòng không có phòng (như ERP).

## 5. Quyền

Màn không gate: không có quyền thì chỉ thấy số của chính mình. Phạm vi áp trên cột tổ chức của bút toán (`ac.employee_*`), giống ERP `filterAcc`.

| Cấp | Thấy |
|---|---|
| Tổng công ty | tất cả |
| Công ty | `ac.employee_company_id` = công ty đang chọn, HOẶC chính mình |
| Phòng ban | `ac.employee_department_id` thuộc phòng mình quản lý, HOẶC chính mình |
| Bộ phận | `ac.employee_part_id` = bộ phận của mình, HOẶC chính mình |

- Dùng `SalesIncomeScope` qua lớp con `BonusQuarterScope`: `CODE` = mã trên, `apply($q, 'ac.employee_')`.
- Catalog `accounting.bao_cao_thuong_nang_suat_thang.view`: thêm `hrm` vào `platforms`.

## 6. Quyết định của Claude (user chưa xác nhận)

- **Nguồn HĐ:** chỉ HĐ hãng + HĐ DV, như ERP.
  - HĐ HRM (`hrm_contracts`) chưa có quyết toán trên `settlement_contracts`.
  - Local cũng không có bút toán TK117 nào của HĐ HRM.
  - → để lại (§8).
- **Phân trang theo PHÒNG** (10 phòng/trang), giống màn "thưởng theo NV".
  - ERP cắt theo dòng gốc rồi mới dựng cây, nên một phòng hoặc một NV có thể bị chia sang 2 trang. Đây là lỗi hiển thị.
  - Số tổng không đổi.
- **Dòng gốc không có phòng** (`ac.employee_department_id` NULL hoặc phòng đã xoá) không hiện trong bảng, nhưng vẫn vào dòng Tổng cộng. Giữ đúng ERP và giải thích ở tooltip ⓘ của dòng Tổng cộng.
- **Từ/Đến ngày bắt buộc** (`Y-m-d`).
  - Thêm ô Năm + Kỳ quyết toán (như màn Tổng hợp thu nhập BH) để chọn nhanh quý: chọn kỳ thì tự điền Từ/Đến.
  - Bỏ ô "Tháng" của ERP vì ở ERP ô này không lọc gì.
- **Bộ lọc giữ đủ như ERP:** Công ty/Phòng/Bộ phận (theo cờ quyền), NV, Số HĐ, Khách hàng.
- **Bảng:**
  - 3 cấp như bản in ERP: Phòng `n` → NV `n.m` (code - tên) → HĐ `n.m.k` (mã HĐ, tên KH).
  - Có nút "Hiện chi tiết HĐ" (bật sẵn) để thu gọn về Phòng → NV.
  - Bấm tên NV mở popup.
- **Popup:**
  - Danh sách HĐ phẳng của NV đó (cùng bộ lọc màn chính), có dòng tổng.
  - BE kiểm lại phạm vi, nên gửi `employee_id` ngoài phạm vi thì nhận về rỗng.
  - ERP popup có ô lọc Số HĐ riêng. HRM bỏ ô này vì màn chính đã có ô Số HĐ.
- **Số 0 hiện `-`**, như ERP.
- **In:**
  - Dùng nguyên mẫu 360, không sửa vì sửa là đổi luôn bản in ERP.
  - `HEADER` lấy theo công ty đang chọn, như màn "thưởng theo NV".
  - `TU_NGAY`/`DEN_NGAY` in dạng d/m/Y.
- **Thứ tự:** theo `department_id` rồi `employee_id`, như ERP.

## 7. Lỗi ERP thấy khi đọc (KHÔNG vá đợt này)

1. Phân trang theo dòng gốc làm một phòng hoặc một NV bị chia sang 2 trang (đã nêu ở §6).
2. Ghép subquery `sf`/`lead` chỉ theo `contractable_id`, trong khi mỗi subquery đã lọc theo loại. Không lệch số.
3. Ở cấp Công ty, ERP dùng `info->company_id` (công ty gốc của user), không phải công ty đang chọn. HRM theo chuẩn `SalesIncomeScope` là công ty đang chọn. Nếu user chọn đúng công ty gốc thì hai bên cho cùng số.
4. **Tổng thưởng theo quý = `diff + round(real)` không bọc COALESCE ngoài**: HĐ có thưởng thực hiện HĐ nhưng chưa có quyết toán trong kỳ → `real` NULL → cả cột Tổng ra NULL (hiện `-`), mất luôn phần thưởng thực hiện HĐ. HRM giữ y ERP (test `test_settlement_outside_range_is_ignored` ghim hành vi này). Muốn vá thì đổi thành `diff + COALESCE(round(real), 0)` ở CẢ 2 bên.

## 8. Để lại

- Gắn HĐ HRM khi quyết toán HRM ghi sang bảng chung, hoặc khi có bảng quyết toán riêng của HRM.
- Có vá ERP theo §7 hay không: chờ user.

## 9. HRM — vị trí và khuôn

- **FE** `/sale/bonus-quarter-report`.
  - Menu: thay placeholder 'Thưởng theo quý' ở `hrm-client/components/subsystem-menu/sale-hub.js` (nhóm "Thưởng - Thu nhập").
- **API** `finance/bonus-quarter-report/{meta,/,detail,export,print-list-data}`.
- **BE** `Modules/Finance/Services/BonusQuarter/{BonusQuarterReportService,BonusQuarterScope,BonusQuarterPrintTable}.php`.
  - Controller `Modules/Finance/Http/Controllers/V1/BonusQuarterReportController.php`.
- **Khuôn copy:**
  - BE: `BonusBusinessEmployeeController` + `BonusEmployeeReportService`; câu SQL theo `SalesIncomeReportService`.
  - FE: `pages/sale/bonus-business-employee/index.vue`; ô Năm/Kỳ theo `pages/sale/sales-income-summary/index.vue`.
- **Kiểm chứng:**
  - Chạy cùng SQL ERP trên `erp_hrm_check` cho quý 2/2026 và so tổng 6 cột, cùng 1 phòng và 1 NV.
  - Feature test quyền.
  - Playwright màn HRM.
