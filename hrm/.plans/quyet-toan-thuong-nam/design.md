# Design: Port "Quyết toán thưởng năm" ERP → HRM

> Bắt đầu 2026-11-04 · @nguyentrancu97 · User yêu cầu port nguyên nghiệp vụ, **bỏ qua hỏi đáp** ("cứ làm đi")
> → mọi quyết định dưới đây là quyết định của AI (đánh dấu **[AI]**), user đọc lại khi nghiệm thu.
>
> **Màn anh em đã port** (bám sát khuôn này): `.plans/qt-thuong-ns-quy-moi/` — "Quyết toán thưởng năng suất
> quý (mới)" (`BillProductivitySettlementQuarter`). Cùng phân hệ Kế toán, cùng module `Modules/Finance`,
> cùng kiểu phiếu kế toán theo phòng ban. KHÁC BIỆT CHÍNH: màn năm (a) **không ghi sổ account_details**
> (chỉ đọc để lấy doanh số thực); (b) chi tiết theo **phòng ban** (không theo nhân viên); (c) có **bước BGĐ
> duyệt riêng** (status 2 → 3/4) + quyền duyệt riêng; (d) có **màn cấu hình quỹ thưởng theo công ty**
> (`CompanyBonusEndYearConfig`) thay cho regulation-config.

## 1. Nguồn ERP (TanPhatDev)

| Thành phần | File |
|---|---|
| Controller | `app/Http/Controllers/Accounting/BonusEndYearSettlementsController.php` (394 dòng — index :28, searchData, create, store :110, edit, update :175, show :205, approve :222 = redirect show, **processApprove :227**, delete :268, **getDepartments :282**, syncDetails :303, handleAttachments, checkDuplicateDepartments) |
| Model | `app/Model/Accounting/BonusEndYearSettlement.php` (207 dòng — STATUS/TYPE const, generateCode, canEdit/canDelete/canApprove, searchByFilter, boot creating) |
| Model con | `BonusEndYearSettlementDetail.php` (`bonus_end_year_settlement_details`), `BonusEndYearSettlementFile.php` (`bonus_end_year_settlement_files`) |
| Model cấu hình | `CompanyBonusEndYearConfig.php` (`company_bonus_end_year_configs`) |
| Service nguồn số | `app/Services/Accounting/BonusEndYearSettlementService.php` (142 dòng — getRegisteredRevenue :20, getActualRevenue :45, calculateBonusFundDSTC, calculateBonusFundProfit, calculateReserveFundDeduction, calculateRemainingBonus, calculateDepartmentDetail, getDepartmentsBySettlementType) |
| Request | `Http/Requests/.../BonusEndYearSettlementStoreRequest.php` |
| View phiếu | `resources/views/accounting/bonus_end_year_settlements/{index,create,edit,show,form,formJs}.blade.php` + `partials/BonusEndYearSettlement.blade.php` + `partials/BonusEndYearSettlementDetail.blade.php` (class JS tính client-side) |
| View cấu hình | `resources/views/common/companies/bonus_end_year.blade.php` + `partials/classes/common/ConfigBonusEndYear.blade.php` |
| Controller cấu hình | `app/Http/Controllers/Common/CompaniesController.php` — `configBonusEndYear` :771, `storeConfigBonusEndYear` :779 |
| Route phiếu | `routes/web.php` :4799-4822 (prefix `admin/accounting/bonus_end_year_settlements`, KHÔNG có checkPermission inline) |
| Route cấu hình | `routes/web.php` :493 (`company.storeConfigBonusEndYear`), :499 (`company.configBonusEndYear`) |
| Menu ERP | Kế toán → (mục "Quyết toán thưởng năm"); cấu hình vào từ danh sách Công ty → link "Cấu hình thưởng cuối năm" |

## 2. Bảng (DB chung — GHI THẲNG bảng ERP có sẵn, KHÔNG tạo migration bảng mới)

- `bonus_end_year_settlements` — phiếu.
- `bonus_end_year_settlement_details` — chi tiết theo phòng ban.
- `bonus_end_year_settlement_files` — file đính kèm (giữ bảng riêng của ERP, **không** dùng bảng `files` chung — bám quy chế gộp DB + để ERP đọc được).
- `company_bonus_end_year_configs` — cấu hình quỹ thưởng theo công ty × phòng ban. **ĐÃ CÓ MODEL + ĐÃ PORT MÀN CẤU HÌNH** (xem §3 cuối) → màn này **chỉ đọc**, không ghi.
- `sales_department_plans` — **CHƯA có model HRM** → tạo mới (`extends Model`, bảng ERP có sẵn trên DB gộp). **Chỉ đọc.**
- **CHỈ ĐỌC khác**: `account_details` + `accounts` (doanh số thực đạt — model đã có: `Modules/Finance/Entities/Accounting/AccountDetail.php`, `Account/Account.php`), `companies`, `departments` (model đã có).
- Màn này **KHÔNG ghi `account_details`** → không có `invoiceable_type`, không bút toán.
- Model cần **tạo mới**: `bonus_end_year_settlements`, `bonus_end_year_settlement_details`, `bonus_end_year_settlement_files`, `sales_department_plans` — tất cả `extends Model` (không BaseModel), service tự gán `created_by/updated_by = auth()->id()` ở mọi đường ghi (vì không có hook BaseModel).

## 3. Nghiệp vụ (bám ERP 1:1)

### Trạng thái (model `BonusEndYearSettlement`)
| Số | Const | Nhãn | Màu HRM (BE trả `status_color`) |
|---|---|---|---|
| 1 | STATUS_CREATING | Đang tạo | `#64748B` xám nháp (ERP tô đỏ — HRM theo bảng 9 màu) |
| 2 | STATUS_WAITING_APPROVE | Chờ BGĐ duyệt | `#D97706` vàng |
| 3 | STATUS_APPROVED | Đã duyệt | `#16A34A` xanh |
| 4 | STATUS_REJECTED | Không duyệt | `#DC2626` đỏ |

### Loại quyết toán (SETTLEMENT_TYPES)
| Số | Const | Nhãn |
|---|---|---|
| 1 | TYPE_DSTC | DSTC quyết toán |
| 2 | TYPE_DEPARTMENT_PROFIT | Lợi nhuận phòng |
| 3 | TYPE_COMPANY_PROFIT | Lợi nhuận công ty |

### Luồng
- **Tạo/Sửa**: chọn Công ty + Năm + Loại quyết toán + Từ ngày/Đến ngày/Ngày hạch toán → nút **"Lập quyết toán"** gọi `getDepartments` nạp bảng phòng ban theo cấu hình công ty + tự tính. **Lưu** → status 1. **Lưu và gửi duyệt** → status 2.
- **Chi tiết (show)**: Sửa (canEdit) · **Duyệt** / **Không duyệt** (canApprove) · Xóa (canDelete) · Quay lại. Không có In/Xuất ở màn ERP gốc (HRM thêm Xuất Excel + Lịch sử theo chuẩn bắt buộc — xem §4).
- **Duyệt (processApprove)**: chỉ khi status==2. `approve` → status 3 + `approved_by/approved_at` + cập nhật `approval_rate`+`total_approved` từng phòng (BGĐ chỉnh tỉ lệ duyệt). `reject` → status 4 + approved_by/at. **Không ghi sổ.**
- **Mã** (`generateCode`): `{mã cty}.QTN.{year}.{5 số}`. **[AI]** sinh trong transaction `lockForUpdate` theo khuôn `BillAdjustDept::generateCode` (ERP không khoá — HRM chống trùng mã khi lưu đồng thời).
- **canEdit/canDelete**: `status ∈ {1 Đang tạo, 4 Không duyệt}` **AND** `created_by == auth id`.
- **canApprove**: `status == 2` **AND** quyền `BGĐ duyệt quyết toán năm`.
- **Chống trùng** (`checkDuplicateDepartments`): cùng `department_id` mà khoảng [date_from, date_to] **giao nhau** với phiếu khác ở status ∈ {1,2,3} → chặn lưu (loại chính nó khi sửa).
- **Xóa** = xoá cứng phiếu + chi tiết + file (điều kiện canDelete). **[AI]** giữ nguyên điều kiện ERP, không tự thêm.

### Validate (BE + FE — `BonusEndYearSettlementStoreRequest`)
`company_id` required|exists · `year` required|integer|min:2020 · `date_from`/`date_to`/`date_accounting` required|date_format d/m/Y · `settlement_type` required|in:1,2,3 · `details` required. **[AI]** thêm `date_from ≤ date_to` (bám sibling).

### Form (create/edit)
- **Công ty**: mặc định công ty người đăng nhập; người xem tổng công ty chọn được công ty khác.
- **Năm**: select năm ≤ năm hiện tại, mặc định năm nay.
- **Loại quyết toán**: select 3 loại. Đổi loại/năm/công ty/ngày → **xoá bảng phòng ban** (phải bấm Lập lại).
- **Từ ngày / Đến ngày / Ngày hạch toán**: datepicker d/m/Y.
- **Ghi chú** (`note`). **File đính kèm** pdf/xlsx/xls/jpeg/png (S3 folder `bonus_end_year_settlement`, bảng `bonus_end_year_settlement_files`).
- Nút **"Lập quyết toán"** → `getDepartments(company_id, settlement_type, year, date_from, date_to)` → với mỗi phòng có cấu hình loại đó, gọi `calculateDepartmentDetail` nạp số. Rỗng → toast báo không có phòng cấu hình.

### Bảng chi tiết theo phòng ban (cột đổi theo `settlement_type`)
Cột chung mọi loại: **STT · Phòng ban**, rồi:
- **Loại 1 (DSTC)**: `DSTC đăng ký` (auto, readonly), `DSTC thực đạt` (auto, readonly), `Quỹ thưởng` (auto = calculateBonusFundDSTC, readonly).
- **Loại 2 (Lợi nhuận phòng)**: `Lợi nhuận phòng` (nhập), `Quỹ thưởng` (auto = profit×bonus_rate/100, readonly).
- **Loại 3 (Lợi nhuận công ty)**: `Lợi nhuận công ty` (nhập), `Quỹ thưởng` (auto tương tự loại 2, readonly).

Cột giảm trừ (mọi loại, nhập tay): `Nợ rủi ro` · `Tồn quá hạn` · `Giảm trừ khác` · `Quỹ năm trước` (previous_year_fund). Cột tính: `Trích quỹ dự phòng` (auto = calculateReserveFund) · `Còn lại thưởng` (auto = calculateRemaining).
Cột duyệt (hiện khi canApprove hoặc status==3): `Tỷ lệ %` (approval_rate, BGĐ nhập) · `Tổng được hưởng` (total_approved, 2 chiều với tỉ lệ).

Tổng phiếu (`total_fund`) = Σ `total_approved` các phòng.

### Công thức (BE là nguồn sự thật; port `BonusEndYearSettlementService`)
- **getRegisteredRevenue(deptId, year)** = `SUM(sales_department_plans.standard_sale)` WHERE `department_id=deptId AND year=year AND status=3`.
- **getActualRevenue(deptId, from, to)**: tập mã TK `['511','5211','5212','5213']` + mọi TK con (theo `identify_number_parent`); từ `account_details`: `SUM(money_value_exchange khi type=2) − SUM(khi type=1)` WHERE `employee_department_id=deptId AND invoiceable_date_accounting ∈ [from,to]`.
- **calculateBonusFundDSTC**: `actual ≥ registered ? round(actual×0.01) : round(actual×0.01×0.9)`.
- **calculateBonusFundProfit(profit, bonus_rate)**: `round(profit×bonus_rate/100)`.
- **calculateReserveFund(bonusFund, reserve_fund_percent, max_risk_reserve_fund, previous_year_fund)**: nếu `maxRisk>0 && prevFund≥maxRisk` → 0; `deduction = round(bonusFund×reservePercent/100)`; nếu `maxRisk>0 && prevFund+deduction>maxRisk` → `deduction = maxRisk−prevFund`; kết quả `max(0, deduction)`. **Chỉ dùng `reserve_fund_percent` + `max_risk_reserve_fund`; cột `reserve_fund_value` của config KHÔNG tham gia tính** (ERP service bỏ qua — port đúng vậy).
- **calculateRemaining** = `bonus_fund − risk_debt − overdue_inventory − other_deductions − reserve_fund_deduction`; mặc định `total_approved = remaining`, `approval_rate = 100`.
- **changeApprovalRate** (BGĐ nhập %): `total_approved = remaining × rate/100`. **changeTotalApproved**: `approval_rate = round(total_approved/remaining×10000)/100`.
- **[AI]** BE **tính lại** các cột auto (registered/actual/bonus_fund/reserve/remaining) từ input + config khi lưu, **không tin** số FE gửi cho các cột đó; chỉ nhận input tay (department_profit, risk_debt, overdue_inventory, other_deductions, previous_year_fund) và (khi duyệt) approval_rate/total_approved.

### Phạm vi dữ liệu (port `searchByFilter`)
- **Xem...tổng công ty** → tất cả (có ô lọc Công ty, `meta.is_all_company=true`).
- **Xem...công ty** → `created_company_id` = cty người đăng nhập.
- **Xem...phòng ban** → `created_department_id` ∈ phòng mình quản lý/đang ngồi (HRM rộng hơn ERP — chủ ý, ghi spec).
- Không quyền nào → chỉ `created_by = mình`.
- Sort mặc định `created_at desc`. **[AI]** phiếu status 1 chỉ người tạo thấy; người đã duyệt/từ chối vẫn thấy phiếu. `canView` mirror y hệt (chi tiết/xuất).
- Lọc (port): Công ty, Năm, Loại quyết toán, Trạng thái, Người tạo, Người duyệt, Phòng ban, khoảng Ngày duyệt, khoảng Quỹ (total_fund).

### Màn cấu hình quỹ thưởng theo công ty (`CompanyBonusEndYearConfig`) — ĐÃ PORT, NGOÀI PHẠM VI
- Model `Modules/MasterData/Entities/CompanyBonusEndYearConfig.php` đã tồn tại; màn cấu hình đã port vào
  **Khai Quy chế – Cấu hình** → tab `thuongnam` (`components/regulation-config/data.js`, shape `SHAPE_DEPT_GRID`
  trong `Modules/MasterData/Support/RegulationTabRegistry.php`, lưu qua `RegulationConfigService::saveDeptGrid`).
- Màn quyết toán **chỉ ĐỌC** config này để biết: phòng nào thuộc loại quyết toán nào (`getDepartmentsBySettlementType`),
  `bonus_rate`, `reserve_fund_percent`, `reserve_fund_value`, `max_risk_reserve_fund`.
- 6 cột config (tham chiếu): `department_id` · `bonus_rate` (Tỉ lệ chia thưởng %) · `settlement_type` (1/2/3) ·
  `reserve_fund_percent` · `reserve_fund_value` · `max_risk_reserve_fund`. (reserve_fund_percent vs value loại trừ nhau.)
- → **Không port lại màn cấu hình, không tạo route/quyền cấu hình.**

## 4. HRM

### Module & phân hệ
- BE: **`Modules/Finance`** (cùng module màn anh em quý, bám khuôn `BillAdjustDept`/`ServiceAccounting`).
- FE phân hệ: **`finance`** (Kế toán). `pages/finance/bonus-end-year-settlements`.

### Quyền mới (guard `api`, type **8** = Tài chính) — **[AI]**, không dùng lại quyền ERP
5 quyền, đúng bộ ERP (ERP không có cấp "bộ phận" cho màn này):
| Tên quyền | Dùng cho |
|---|---|
| `Tạo quyết toán thưởng năm` | create/store/update/destroy/calculate(getDepartments)/upload |
| `BGĐ duyệt quyết toán năm` | processApprove (duyệt/từ chối) |
| `Xem tất cả quyết toán thưởng năm của tổng công ty` | phạm vi |
| `Xem tất cả quyết toán thưởng năm của công ty` | phạm vi |
| `Xem tất cả quyết toán thưởng năm của phòng ban` | phạm vi |

Khai 1 dòng `$this->perm([...])` **không `id`** trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`,
group `'Quyết toán thưởng năm'`, `type=8` — chèn cạnh nhóm Tài chính (quanh dòng 1197+). Không gán cho vai trò cũ — admin tự gán.

### Route
- API `finance/bonus-end-year-settlements` (`Modules/Finance/Routes/api.php`): index · show · store · update · destroy ·
  `{id}/approve` (processApprove) · `calculate` (getDepartments) · `form-options` (công ty/năm/loại) · `upload-files` ·
  `export-rows` (danh sách). Gắn `checkPermission:<Tên quyền>`. **Không** có route cấu hình (đã có ở regulation-config).
- FE `/finance/bonus-end-year-settlements`: `index.vue` · `add.vue` · `_id/index.vue` (chi tiết+duyệt) · `_id/edit.vue`.
- Menu: thêm `link` cho mục ở `components/subsystem-menu/finance.js` (kiểm xem đã có mục "Quyết toán thưởng năm" chưa —
  có thì chỉ gắn `link`, **không đổi nhãn**; chưa có thì thêm mục mới kèm `isShow` theo quyền). **[AI]** trang không đọc `?type` → link không gắn tham số.

### Khuôn bám (Bước 5b)
- **`pages/finance/bill-payments`** + BE `Modules/Finance/Entities/BillPayment/*` (`BillPaymentWriteService`/`ApprovalFlowService`/`HistoryService`, `ApproveBillPaymentModal.vue`) — **khuôn chính cho luồng duyệt** (có modal duyệt).
- `pages/finance/bill-adjust-depts` (phiếu kế toán theo phòng, generateCode lock, lịch sử).
- `pages/assign/settlement_contract` (phiếu "quyết toán" có duyệt + `HistoryApproveSettlementModal` + `SettlementCalcMixin`) — mẫu đặt tên/chia mixin tính toán.
- `.plans/qt-thuong-ns-quy-moi/` (màn anh em — form chọn năm/phòng, bảng chi tiết theo phòng, phạm vi dữ liệu 3 cấp).
- Config đọc: `RegulationConfigService::saveDeptGrid` + `CompanyBonusEndYearConfig` cho cách đọc cấu hình phòng×loại.

## 5. Quyết định đã chốt / cần xác nhận
- **[AI]** Nhãn "Người tạo"/"Ngày tạo" (không "Người lập"/"Ngày lập").
- **[AI]** BE tính lại toàn bộ cột auto khi lưu, không tin FE.
- **[AI]** Status 1 "Đang tạo" tô xám (không đỏ như ERP).
- **[AI]** Thêm Xuất Excel danh sách + Lịch sử (entity-history) — bắt buộc HRM; ERP không có.
- **[AI]** Sinh mã có lockForUpdate.
- **[AI]** Phân hệ chính = **Tài chính (type 8)**, khớp màn anh em quý. (Agent khảo sát nêu Bán hàng type 23 là lựa chọn thay thế — nếu user muốn đổi, chỉ cần sửa `type` quyền + file menu.)
- **[ĐÃ XÁC NHẬN]** `reserve_fund_value` KHÔNG tham gia tính quyết toán (ERP service chỉ dùng percent + maxRisk) — port đúng vậy.
- **[#12044]** Công ty khoá theo công ty đang làm việc, kể cả người có quyền xem tổng công ty (ticket ghi rõ); BE chặn bằng `Rule::in`.
- **[#12044]** Năm trước tự điền tới 31/12, năm nay tới hôm nay — theo `changeYear` của ERP. Ngày hạch toán khoá, luôn bằng Đến ngày như ERP.
- **[#12044]** Nháp để trống: BE điền mặc định (loại DSTC, năm hiện tại, ngày theo năm) vì các cột NOT NULL.
- **[#12047]** Tag trạng thái + bỏ Mã phiếu áp cả màn Chi tiết vì dùng chung form.

## 6. Ngoài phạm vi
- **Màn cấu hình quỹ thưởng năm** — đã port sẵn (regulation-config tab `thuongnam`).
- Ghi sổ kế toán (màn này không có bút toán).
- In phiếu (ERP không có bản in cho màn năm — chỉ thêm nếu user yêu cầu).
- Màn cũ ERP giữ nguyên, không đụng.
