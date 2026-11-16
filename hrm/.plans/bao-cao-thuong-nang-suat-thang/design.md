# Báo cáo thưởng năng suất tháng — port ERP → HRM (+ HĐ HRM, + vá ERP)

Ngày: 16/11/2026 · Trạng thái: chờ user duyệt · Nhánh: HRM `develop` (hrm-api + hrm-client, làm trong worktree), ERP `develop_02` (worktree riêng).

## 1. Mục đích

Đưa màn ERP `report.commissionMonth` ("Báo cáo thưởng năng suất tháng", menu Báo cáo thu nhập) sang HRM. Màn chỉ đọc. Mỗi phòng → nhân viên → hợp đồng, màn cho xem:
- **Thưởng NS tháng:** tiền thưởng đã ghi sổ 3351 (mã công việc TNST) trong kỳ.
- **Doanh số tiêu chuẩn tính thưởng NS tháng:** tương ứng với tiền thưởng đó.

Màn HRM tự nhận thêm hợp đồng bán của HRM (`hrm_contracts`) khi các HĐ này bắt đầu có bút toán TNST.

ERP đang có nhiều lỗi làm sai số và rò quyền (xem §6). Theo yêu cầu của user, **lỗi sai số và lỗi quyền được sửa ở cả HRM lẫn ERP**, để hai bên ra cùng một số đúng.

## 2. Quyết định đã chốt (user 16/11/2026)

1. **Nguồn:** bám ERP và gộp thêm HĐ HRM. Có 3 nguồn: HĐ hãng (`firm_contracts`), HĐ dịch vụ (`wr_service_contracts`) và HĐ HRM (`hrm_contracts`, morph `Modules\Assign\Entities\Contract\Contract`).
2. **Port đủ chi tiết:** bảng Phòng → NV → HĐ/KH (tích "Show chi tiết"), cùng popup NV có **cả tầng mặt hàng** như ERP.
3. **Lỗi rõ ràng của ERP:** sửa cả 2 bên. Ở ERP chỉ sửa **lỗi sai số và lỗi quyền**, không viết lại phần hiệu năng.
4. **Công thức DSTC** cho HĐ chưa quyết toán và HĐ DV: **nhân** tỷ lệ hưởng thay vì chia (xem §5 "DSTC"). Sửa cả 2 bên.
5. **HĐ hãng đã quyết toán:**
   - Lấy **dòng quyết toán chính thức**, không lấy dòng ngẫu nhiên.
   - Giữ cách ERP hiện cả giá trị ở mọi tháng có bút toán TNST, không chia theo kỳ.

## 3. Mục tiêu / Không làm / Phản mục tiêu

**Mục tiêu**
- Màn HRM `/sale/bonus-month-report` có:
  - bộ lọc;
  - bảng 3 cấp, dòng Tổng cộng;
  - phân trang theo phòng;
  - popup NV (HĐ → phiếu → mặt hàng);
  - In và Xuất Excel.
- Menu: thay chuỗi placeholder `'Thưởng năng suất tháng'` ở `hrm-client/components/subsystem-menu/sale-hub.js` (nhóm "Thưởng - Thu nhập") bằng `{ n: 'Thưởng năng suất tháng', link: '/sale/bonus-month-report' }`.
- Chạy 1 năm vẫn nhanh: tính gom trong vài câu truy vấn, không O(N²).
- ERP `develop_02`: vá các lỗi ở §6A trong `CommissionMonthReportService`, `ReportController` và view `commission_month.blade.php`.

**Không làm**
- Không thêm cột, không đổi bố cục bảng hay mẫu in.
- Không tạo bút toán TNST cho HĐ HRM.
- Không tối ưu hiệu năng ERP (§6B giữ nguyên ở ERP).
- Không gop_db (trừ khi user bảo).

**Phản mục tiêu**
- Sau khi vá, số HRM lệch ERP ở bất kỳ ô nào, khi cùng kỳ và cùng phạm vi.
- Người không có quyền thấy số của người khác. Áp cho bảng, tổng, popup, In và Excel.
- Một NV hiện nhiều lần, hoặc tổng bị cộng trùng.

## 4. Nguồn ERP

Gốc `ERP/TanPhatDev`:
- Service: `app/Services/Reports/CommissionMonthReportService.php` (dùng `getCostEmployees`, `getDataDepartment`, `renderDataBonusBusinessDepartments`, `getDoanhSoTieuChuan`, `getDetailByEmployee`, `printListData`). `getDataDepartment_` là code chết, không ai gọi.
- Controller: `app/Http/Controllers/ReportController.php:4352-4430`.
- Routes: `routes/web.php:3250-3254`.
- View và JS angular: `resources/views/reports/commission_month.blade.php`.
- Mẫu in: `ReportTemplate::BAO_CAO_THUONG_NANG_SUAT_THANG = 311`.

Phân tích đầy đủ (kèm SELECT đối chiếu): `.plans/bao-cao-thuong-nang-suat-thang/erp-analysis.md`.

## 5. Hành vi

### Số liệu "Thưởng NS tháng"

Lấy từ sổ `account_details`:
- **Điều kiện:**
  - Sổ 3351: ERP lọc `account_id = 117`, HRM lọc `identify_number = '3351'` như `BonusLedger`.
  - `invoiceable_type` không thuộc BillPayment, BillPaymentAuthorization, ClosingEntry.
  - `contractable_id` và `employee_id` khác NULL.
- **Gom và giá trị:** gom theo (`contractable_type`, `contractable_id`, `contractable_code`, `employee_id`). Giá trị = Σ Có (type 2) − Σ Nợ (type 1) của `money_value_exchange`, chỉ tính work TNST.
- **Bỏ dòng:** bỏ cặp (HĐ, NV) có giá trị = 0.
- **Lọc ngày:** theo `invoiceable_date_accounting`.
- **Tái dùng HRM:** dùng `Modules/Finance/Services/BonusContractReport/BonusLedger` (đã có index `idx_ad_identify_date_ctype`). Builder thêm biến thể chỉ lấy cột TNST nếu cần; không đổi hành vi cho màn BC thưởng theo HĐ.

### Số liệu "DS tiêu chuẩn" (DSTC) cho mỗi cặp (HĐ, NV)

- **HĐ hãng, `status = 10` (đã quyết toán):**
  - Lấy `settlement_contract_employees.commission_sale` của (HĐ, NV) thuộc quyết toán loại 2 (qua `settlement_contract_departments` → `firm_settlement_contract_detail.type = 2`).
  - **Chỉ lấy dòng chính thức** (`settlement_contract_id IS NOT NULL`). Nếu còn nhiều dòng chính thức, lấy dòng `id` lớn nhất (quyết định của Claude).
  - Không có dòng thì DSTC = 0.
  - Không quy theo kỳ: tháng nào có TNST thì hiện cả giá trị.
- **HĐ hãng chưa quyết toán, và HĐ DV:**
  - **Công thức:** `DSTC = (tnst_NV / tnst_tổng_HĐ) × commission_sale_HĐ × tỷ_lệ_hưởng / 100`.
  - `tnst_tổng_HĐ` = tổng TNST của mọi NV trên HĐ đó trong kỳ lọc, **không áp quyền** (giống ERP).
    - Lọc Số HĐ và lọc KH giữ nguyên cả HĐ, nên không ảnh hưởng mẫu số.
    - Lọc tổ chức (Công ty/Phòng/Bộ phận/NV) **không** áp vào mẫu số, giống ERP `getCostEmployees`.
  - `commission_sale_HĐ` lấy từ `firm_support_accounting` hoặc `wr_support_accounting`, join theo **cả** `contractable_type` và `contractable_id`.
  - `tỷ_lệ_hưởng` = 100 nếu NV là `department_lead_id` của phòng hiện tại của NV (phòng mà dòng NV nằm dưới). Ngược lại lấy `commission_sale_percent` ở `*_support_accounting_employees` (khớp type + id + NV).
  - Không có dòng tỷ lệ: tỷ lệ = 0, nên DSTC = 0, không crash.
  - `tnst_tổng_HĐ = 0` thì DSTC = 0.
- **HĐ HRM:** DSTC = 0, như BC thưởng theo HĐ.

### Bảng

- **5 cột:** STT | Nhân viên | Khách hàng | DS tiêu chuẩn tính thưởng NS tháng | Thưởng năng suất tháng.
- **Dòng Tổng cộng ở đầu:** cộng toàn tập, không chỉ trang hiện tại.
- **Dòng Phòng (đậm):** STT `n`, nội dung `mã - tên phòng`, 2 số tổng.
- **Dòng NV:** STT `n.m`, nội dung `mã - tên NV`. Tên là link mở popup.
- **Dòng HĐ:** STT `n.m.k`, chỉ hiện khi tích "Show chi tiết". Cột 2 là mã HĐ (link chi tiết HĐ theo nguồn, như BC thưởng theo HĐ), cột 3 là `mã KH - tên KH`:
  - HĐ hãng: `customers.code` - `firm_contracts.customer_name`.
  - HĐ DV và HĐ HRM: mã + tên snapshot trên HĐ.
- **Phòng của NV:** lấy phòng **hiện tại** (`employee_infos.department_id`, phòng `status = 1`). **Mỗi NV chỉ 1 dòng** (sửa lỗi nhân theo bộ phận).
- **Phân trang:** theo phòng, 10 phòng/trang.

### Bộ lọc (bám ERP)

- **Kỳ:**
  - Năm + Tháng, hoặc Từ ngày - Đến ngày. Hai kiểu loại trừ nhau, bắt buộc có một kiểu.
  - Back-end có kiểm (khác ERP): 422 nếu thiếu cả hai kiểu hoặc ngày sai định dạng.
  - HRM quy Năm/Tháng về khoảng ngày để dùng index.
  - Chọn Tháng mà không chọn Năm: ERP quét mọi năm. HRM bắt buộc phải có Năm khi chọn Tháng (quyết định của Claude, ghi §6C).
- **Số hợp đồng:** khớp chính xác `contractable_code`, giống ERP.
- **Khách hàng:** lọc theo `customer_id` của HĐ.
- **Tổ chức:** Công ty / Phòng / Bộ phận / NV. Lọc theo hồ sơ NV hiện tại, nằm trong phạm vi quyền.

### Phân quyền

- **Mã quyền:** `accounting.bao_cao_thuong_nang_suat_thang.view` (đã có trong catalog `hrm-api/app/Support/Permissions/Catalog/accounting.php`, scope 1-4). Thêm `'hrm'` vào `platforms`, deploy chạy `permission:catalog-sync`.
  - **Lưu ý:** phiên làm "BC thưởng theo quý" (`.plans/bc-thuong-theo-quy`) dùng chung mã này và cũng thêm `'hrm'`. Bên nào gộp sau thì xử lý xung đột, giữ 1 lần thêm.
- **Màn không gate** (như ERP). Mã chỉ mở rộng phạm vi; không có mã thì chỉ thấy mình.
- **Phạm vi theo hồ sơ NV hiện tại**, đúng ý ERP nhưng dùng **đúng cấp cao nhất** (sửa lỗi cờ cộng dồn):

| Cấp | Thấy NV |
|---|---|
| 4 Tổng công ty | tất cả |
| 3 Công ty | NV thuộc phòng có `company_id` = công ty hồ sơ của tôi, + chính tôi |
| 2 Phòng ban | NV thuộc phòng trong `employee_manage_departments` của tôi (cùng công ty hồ sơ), + chính tôi |
| 1 Bộ phận | NV cùng `part_id` với tôi, + chính tôi. Tôi không có bộ phận thì chỉ thấy mình |
| 0 | chính tôi |

- **Khuôn:** `Modules/Finance/Services/BonusEmployee/BonusEmployeeScope.php` (cũng theo hồ sơ NV hiện tại). Builder đối chiếu: chỗ nào khuôn khác bảng trên thì theo bảng trên.
- **Popup, In, Excel** áp cùng phạm vi. Popup với NV ngoài phạm vi trả 403.

### Popup NV (bấm tên NV)

- **Tham số:** cùng kỳ của bảng (Năm/Tháng hoặc ngày), Số HĐ, KH, cộng thêm ô lọc "Phiếu hạch toán" (mã phiếu, khớp chính xác như ERP).
- **Cấu trúc:** HĐ (gom theo type + id) → phiếu (`invoiceable`, mã phiếu, thưởng của phiếu) → mặt hàng.
- **Mặt hàng (giữ như ERP):**
  - **Khi nào có:**
    - Phiếu xuất kho: lấy chi tiết dòng hàng với `price`.
    - Phiếu nhập kho: lấy với `supplier_price`.
    - Phiếu loại khác: không có dòng hàng. Dữ liệu thật hiện chỉ có phiếu quyết toán, nên tầng này thường trống. Đây là đúng như ERP.
  - **Cột:** STT | Tên hàng | Mã hàng | SL | Đơn giá tiêu chuẩn | Doanh số tiêu chuẩn (= SL × đơn giá) | Thưởng NS tháng.
  - **HRM:** builder tìm model PXK/PNK tương ứng ở HRM. Morph type trên sổ có thể là class ERP (`App\Model\...ProductExport`), nên phải khớp đúng chuỗi type có trong `account_details`.
- **Phân trang:** theo HĐ, độc lập với bảng chính.
- **Dữ liệu bị xoá:** HĐ hoặc phiếu đã xoá thì hiện mã trên sổ (`contractable_code` / `invoiceable_code`), không crash.

### In / Excel

- **In:** bố cục như `printListData` ERP:
  - thead 5 cột, dòng 2 là Tổng cộng;
  - dòng phòng đậm, dòng NV chữ `#1abc9c`;
  - dòng HĐ chỉ khi tích "Show chi tiết";
  - số 0 hiện `-`.
  - Mẫu và tiêu đề: "BÁO CÁO THƯỞNG NĂNG SUẤT THÁNG", header công ty. Khuôn HRM: `BonusEmployeePrintTable` / `BonusContractPrintTable` cùng endpoint `print-list-data`.
- **Excel:** khuôn `export-excel.js` FE như `pages/sale/bonus-contract-report`, file `bao_cao_thuong_nang_suat_thang.xlsx`, cùng cột với bảng.
- In và Excel lấy toàn tập, không phân trang, cùng phạm vi quyền.

## 6. Danh sách lệch / sửa (user kiểm khi đọc)

### 6A. Lỗi sửa ở CẢ HRM và ERP (`develop_02`)

1. NV lặp theo số bộ phận của phòng (join `parts`), làm tổng phòng và Tổng cộng bị nhân lên. Ví dụ phòng 47 tháng 05/2026: 16 NV hiện thành 96 dòng.
2. Cờ quyền cộng dồn (`is_part` đúng với mọi scope ≥ 1): người cấp Phòng/Công ty/Tổng công ty có `part_id` chỉ thấy NV cùng bộ phận. Sửa thành chỉ áp đúng cấp cao nhất.
3. Join `*_support_accounting` thiếu `contractable_type`, làm nhân đôi thưởng ở HĐ hãng 13, 15 và HĐ DV 3948.
4. NV không có dòng tỷ lệ hưởng làm crash, sau đó gặp `dd($e)` trong controller. Sửa: tỷ lệ = 0; bỏ `dd`, trả lỗi bình thường.
5. Công thức DSTC chia tỷ lệ, sửa thành nhân tỷ lệ/100 (user chốt). Số đổi với NV hưởng < 100%.
6. Nhánh đã quyết toán lấy `[0]` ngẫu nhiên, sửa thành lấy dòng chính thức `id` lớn nhất.
7. Popup không kiểm quyền: thêm kiểm phạm vi.
8. Popup bỏ lọc Năm/Tháng và KH: gửi đủ tham số kỳ như bảng.
9. Popup phân trang dùng chung `current.page` với bảng chính: tách biến riêng.
10. Popup gom HĐ chỉ theo `contractable_id`: gom theo type + id.
11. In khi kết quả rỗng lỗi `Undefined index` ở total: cho total mặc định 0.
12. Query `FirmSupportAccountingEmployee::groupBy` không aggregate, lỗi khi bật ONLY_FULL_GROUP_BY. Ở ERP sửa nếu đụng phải khi vá mục 3/5. Ở HRM viết đúng từ đầu.

### 6B. Chỉ HRM làm khác (ERP giữ nguyên, không đổi số)

- Tính gom bằng vài câu truy vấn và map theo khoá, không O(N²) / N+1. Phân trang sau khi tính một lần mỗi request. ERP giữ nguyên cách cũ.
- Back-end kiểm điều kiện kỳ và định dạng ngày (422).
- Lọc ngày bằng khoảng thay cho `whereYear/whereMonth`. Kết quả không đổi.

### 6C. Quyết định của Claude (user xem)

- Lấy dòng quyết toán chính thức `id` lớn nhất khi có nhiều dòng.
- Chọn Tháng phải kèm Năm ở HRM. ERP vẫn cho Tháng không Năm (quét mọi năm); ERP giữ nguyên vì đây không phải lỗi sai số.
- NV ở phòng đã đóng, hoặc không có phòng: giống ERP, không hiện, và tổng cũng không tính. Ghi lại để QA biết đây là cố ý.
- Route FE `/sale/bonus-month-report`, API prefix `/api/v1/finance/bonus-month-report` (`/`, `/meta`, `/detail`, `/export-rows`, `/print-list-data`), `auth:api`, không gate.

## 7. HRM — vị trí và khuôn

- **Backend:** `hrm-api/Modules/Finance/Services/BonusMonthReport/` (Scope, ReportService, PrintTable) + `Http/Controllers/V1/BonusMonthReportController.php`, routes trong `Modules/Finance/Routes/api.php`.
- **Khuôn gần nhất:** `Services/BonusEmployee/*` (Phòng → NV, popup, phạm vi theo hồ sơ) và `Services/BonusContractReport/BonusLedger` (sổ 3351, 3 nguồn).
- **Frontend:** `hrm-client/pages/sale/bonus-month-report/index.vue` + `components/export-excel.js`, khuôn `pages/sale/bonus-contract-report`.
- **Tests:** `Modules/Finance/Tests/Feature/BonusMonth*Test.php`, tái dùng `Concerns/BuildsBonusLedgerFixtures.php`.
- **e2e:** `HRM/e2e/tests/bonus-month-report.spec.ts`.
- **ERP:** sửa trong worktree từ `develop_02`, ERP là Laravel 6.

## 8. Để người làm tự quyết

- Tách class và tên hàm nội bộ.
- Dùng lại hay tách biến thể của `BonusLedger`, miễn không đổi số của màn BC thưởng theo HĐ.
- Cách map morph type PXK/PNK giữa ERP và HRM cho popup.
- Giao diện FE theo khuôn report-styles hiện có.

## 9. Kiểm thử / nghiệm thu

- **Test BE:**
  - Mỗi nhánh DSTC: đã quyết toán (nhiều dòng, nháp + chính thức), chưa quyết toán tỷ lệ 100/50, trưởng phòng, thiếu dòng tỷ lệ, tổng TNST = 0, HĐ HRM.
  - Phòng nhiều bộ phận ra 1 dòng/NV.
  - 5 cấp quyền, trong đó có cấp Phòng có `part_id`.
  - Popup ngoài phạm vi trả 403.
  - Validate kỳ.
- **Đối số:** sau khi vá ERP, so HRM với ERP đã vá trên `erp_hrm_check`, 2 kỳ (05/2026 và cả năm 2026), phạm vi Tổng công ty. Tổng, 1 phòng có nhiều bộ phận, 1 NV hưởng 50%: **0 lệch**.
- **So ERP cũ:** ghi lại chênh lệch trước/sau vá ERP cho các mục 6A.1/3/5/6, để user biết số nào đổi.
- **ERP:** kiểm tay màn đã vá (bảng, popup, In, Excel) trên local. Không ghi DB.
- **Playwright HRM:** lọc, mở chi tiết, popup, In, Excel.
- **Chạy 1 năm:** mục tiêu dưới 15s, ngang màn BC thưởng theo HĐ.
