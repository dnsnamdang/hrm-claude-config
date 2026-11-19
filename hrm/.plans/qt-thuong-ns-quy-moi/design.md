# Design: Port "Quyết toán thưởng năng suất quý (mới)" ERP → HRM

> Bắt đầu 2026-11-04 · @nguyentrancu97 · User yêu cầu port nguyên nghiệp vụ, **bỏ qua hỏi đáp** → các quyết định
> dưới đây là quyết định của AI (đánh dấu **[AI]**), user đọc lại khi nghiệm thu.

## 1. Nguồn ERP (TanPhatDev)

| Thành phần | File |
|---|---|
| Model | `app/Model/Accounting/BillProductivitySettlementQuarter.php` (862 dòng — `searchByFilter` :212, `syncEmployees` :327, `saveAccounting` :528, `calculateSettlementCombined` :573–862) |
| Model con | `BillProductivitySettlementQuarterEmployee.php` (accessor `sum_tns_luy_tien`, `base_commission_bonus`), `...Contract` |
| Service nguồn số | `app/Services/BillCommissionSettlementQuarter/BillCommissionSettlementQuarterService.php` (`getDataAdBonusByContract`, `getDataAdBonusByContractEmployee`) |
| Controller | `app/Http/Controllers/Accounting/BillProductivitySettlementQuartersController.php` (`buildExportData` :334, `buildPrintHtml` :453) |
| Request | `Http/Requests/Accounting/BillCommissionSettlementQuarterStoreRequest.php`, `CalculateSettlementRequest.php` |
| View | `resources/views/accounting/bill_productivity_settlement_quarters/*` + JS class `partials/classes/accounting/BillProductivitySettlementQuarter*.blade.php` |
| Menu ERP | Kế toán bán hàng → Quyết toán → `?_type=all` |

## 2. Bảng (DB chung, GHI THẲNG bảng ERP, KHÔNG tạo bảng mới)

`bill_productivity_settlement_quarters` · `bill_productivity_settlement_quarter_employees` · `bill_productivity_settlement_quarter_contracts`.
Kế toán ghi `account_details` với `invoiceable_type = 'App\Model\Accounting\BillProductivitySettlementQuarter'` (chuỗi class ERP — để ERP mở được chứng từ, link `list_detail_debt_employee.blade.php:503`).

## 3. Nghiệp vụ (bám ERP 1:1)

### Trạng thái
| Số | Nhãn | Màu HRM (BE trả) |
|---|---|---|
| 1 | Đang tạo | `#64748B` nháp (ERP tô đỏ — HRM theo bảng 9 màu) |
| 2 | Chờ duyệt | `#D97706` (luồng mới không dùng; lọc trạng thái ẩn) |
| 3 | Đã hạch toán | `#16A34A` |

### Luồng
- Tạo / Sửa: **Lưu** → status 1. **Lưu và duyệt** → status 3 + `approved_by/approved_at` + ghi sổ ngay.
- Chi tiết: In · Xuất Excel · Sửa (status 1 & người tạo) · Duyệt (status 1 & người tạo → status 3 + ghi sổ) · Xóa (status 1 & người tạo — xoá cứng phiếu + nhân viên + hợp đồng) · Quay lại.
- Route `deny` của ERP (3→1) không có nút → **[AI] không port**.
- Mã: `{mã cty}.QTHHQ{mmyy}.{4 số}` — sinh trong transaction có `lockForUpdate` (khuôn `BillAdjustDept::generateCode`).
- Duy nhất 1 phiếu / (year, period, department_id), mọi trạng thái, sửa thì loại chính nó. Message: `Phòng ban '<tên>' đã có bản quyết toán thưởng năng suất quý cho Kỳ <P> năm <Y> (mã: <code>)`.

### Validate (BE + FE)
year, period, date_from, date_to, date_accounting, department_id (exists), employees (≥1), status bắt buộc.
`date_from ≤ date_to`; `date_accounting ≥ date_to`; kỳ phải đã kết thúc (`now > date_to`) — giữ nguyên câu ERP.
Endpoint tính: bắt buộc date_from, date_to, department_id.

### Form
- Năm: select các năm ≤ năm hiện tại, mặc định năm nay. Kỳ: lấy `companies.config_settlement_period` của **công ty người đăng nhập** (`[{year, details:[{date_from,date_to,period}]}]`, như `Company::getAllPeriods`).
- Từ ngày / Đến ngày tự điền từ kỳ (khoá). Ngày hạch toán = Đến ngày (khoá).
- Phòng ban bắt buộc; Bộ phận tuỳ chọn, lọc theo phòng. Ghi chú. File đính kèm pdf/xlsx/xls/jpeg/png (S3 folder `bill_productivity_settlement_quarter`, cột `files` nối `, ` như ERP).
- Đổi năm/kỳ/phòng/bộ phận → xoá bảng nhân viên.
- Nút **Quy chế** (khi có phòng): popup thang `conditions_quarter_bonus` của phòng ("Lớn hơn"/"Lớn hơn bằng" … "và Nhỏ hơn"/"Nhỏ hơn bằng", %) + tỉ lệ TP/TBP/NV.
- Nút **Lập quyết toán thưởng năng suất quý** → gọi tính; rỗng: toast `Không có dữ liệu tạo quyết toán`; có: `Lấy dữ liệu thành công`.

### Bảng chi tiết (2 tầng tiêu đề)
STT · Nhân viên (badge TP/TBP; bấm mở popup hợp đồng) · DS tiêu chuẩn · Thưởng TH HĐ · Thưởng NS tháng (NV/TBP/TP) · Thưởng NS quý (NV/TBP/TP) · Tổng TNS lũy tiến · Thưởng thêm (ⓘ công thức `bonus_base_formula`) · Phân chia thưởng thêm (NV/TBP/TP) · Tổng thu nhập. Dòng **Tổng cộng đứng đầu**. Chỉ hiện/lưu NV có `sum_commission_employee > 0`.
Ô NV/TBP/TP: dòng nhân viên → NV = của mình, TBP/TP = phần đóng góp (>0, còn lại `-`); dòng trưởng → số của mình ở cột vai trò.

Popup hợp đồng: STT · Số HĐ (link) · Khách hàng (mã − tên) · DS tiêu chuẩn · Thưởng TH HĐ · cột tháng/quý theo vai trò · Tổng TNS lũy tiến.

### Công thức (BE là nguồn sự thật; FE chỉ hiển thị kết quả BE)
- Nguồn: `account_details` TK 117, work code TTHHD/TNST/TNSQ, Có (type 2) − Nợ (type 1), trừ invoiceable BillPayment/BillPaymentAuthorization/ClosingEntry, `invoiceable_date_accounting` trong [date_from, date_to]; nhóm theo HĐ & theo HĐ-nhân viên (port `getDataAdBonusByContract*`).
- Phòng chưa cấu hình `conditions_quarter_bonus` → lỗi `Vui lòng cài đặt quy chế thưởng thêm hoa hồng quý cho phòng ban`; phải có TK 3351.
- NV hỗ trợ hạch toán: firm + wr; doanh số thực: `settlement_contract_employees`. Trưởng nhận phần NV cấp dưới × `commission_sale_percent`. Thứ tự dòng: TP → TBP → NV.
- `sum_commission_employee` = month + quarter. `sum_tns_luy_tien` = của mình (+ phần TBP/TP đóng góp tháng & quý nếu là NV).
- `base_commission_bonus` (chỉ NV) lũy tiến: thang sort theo money_from, mỗi bậc cộng `(min(sum, to) − from) × percent/100` khi sum > from; `to` rỗng = ∞.
- NV: bonus = base × rate_nv%; đóng góp TBP = base × rate_tbp%; TP = base × rate_tp%. TBP = Σ đóng góp từ NV cùng part_id; TP = Σ mọi đóng góp TP.
- income = cost + own + bonus; calculate_percent = bonus / tns × 100.

### Ghi sổ (port `saveAccounting`)
Mỗi dòng NV: Nợ 6411 / Có 3351 = `sum_commission_bonus_employee`, work id 9, employee_department_id, employee_company_id = company của phòng, contractable = HĐ có `sum_commission_employee` lớn nhất của NV. Khuôn `BillAdjustDeptAccountingService` (buildEntries thuần + persist).

### Phạm vi dữ liệu (port `searchByFilter` `_type=all`)
- Tổng công ty → tất cả (có ô lọc Công ty, `meta.is_all_company`). Công ty → `created_company_id` = cty mình. Phòng ban → phòng mình quản lý/đang ngồi. Còn lại → `created_by = mình`.
- Mọi cấp: phiếu status 1 chỉ người tạo thấy. `canView` mirror y hệt (chi tiết/in/xuất).

## 4. HRM

### Quyền mới (guard api, type **8** = Kế toán) — **[AI]**
| Tên | Dùng cho |
|---|---|
| `Tạo/Duyệt quyết toán thưởng năng suất quý` | store, update, approve, destroy, calculate, upload |
| `Xem tất cả quyết toán thưởng năng suất quý của tổng công ty` | phạm vi |
| `Xem tất cả quyết toán thưởng năng suất quý của công ty` | phạm vi |
| `Xem tất cả quyết toán thưởng năng suất quý của phòng ban` | phạm vi |

Không gán cho vai trò cũ — admin tự gán.

### Route
- API `finance/bill-productivity-settlement-quarters` (index, show, store, update, destroy, approve, calculate, form-options, regulation, print-data, export, export-rows, upload-files).
- FE `/finance/bill-productivity-settlement-quarters` (index, add, `_id`, `_id/edit`, `_id/print`). Menu: thêm `link` cho mục có sẵn `Quyết toán thưởng năng suất quý (mới)` ở `components/subsystem-menu/finance.js:375` — **không đổi nhãn**. **[AI]** Trang không đọc `?type` nên link không gắn tham số (phạm vi do quyền quyết).

### Khuôn bám
Màn HRM mẫu: `pages/finance/bill-adjust-depts` (cùng phân hệ, phiếu kế toán ghi sổ) + `pages/finance/service-accounting`.

## 5. Quyết định đã chốt
- **[AI]** Nhãn "Người lập"/"Ngày lập" → "Người tạo"/"Ngày tạo" (list, export, bản in chữ ký).
- **[AI]** BE tính lại toàn bộ khi lưu (không tin số FE gửi) — như `syncEmployees` ERP.
- **[AI]** Màn cũ "Quyết toán thưởng năng suất quý" giữ nguyên, không đụng.
- **[AI]** Xoá = xoá cứng như ERP (điều kiện ERP: status 1 + người tạo) — giữ nguyên điều kiện ERP, không tự đặt thêm.
- **[AI]** Lịch sử: HRM bắt buộc mục Lịch sử → dùng khuôn entity-history nếu bill-adjust-depts có; nếu không có thì để phase sau.

- **#12035 Excel 1 phiếu — giữ logo (user chốt 06/11/2026):** ticket ghi "ẩn logo Tân Phát" nhưng CLAUDE.md bắt buộc file Excel chứng từ có letterhead theo công ty trên phiếu → giữ logo theo quy định, chỉ ẩn dòng Trạng thái. Cần báo lại người viết ticket.
- **#12033 popup hợp đồng:** rộng tối đa 1400px, chừa 70px mỗi bên để không đè menu trái; phân trang phía client (dữ liệu đã có sẵn trong dòng nhân viên), mặc định 25 dòng.

## 6. Ngoài phạm vi
Route deny; sửa màn cũ; thay đổi cấu hình quy chế (đã có ở regulation-config tab `themquy`).
