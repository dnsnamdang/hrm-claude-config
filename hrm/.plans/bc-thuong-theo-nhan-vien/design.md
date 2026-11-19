# Port "Báo cáo thưởng theo nhân viên" ERP → HRM

Ngày: 14/11/2026 · Trạng thái: chờ user duyệt

## 1. Mục đích

Đưa màn ERP `report.bonusBusinessEmployee` ("Báo cáo thưởng theo nhân viên", menu Báo cáo thu nhập) sang HRM,
cùng số liệu với ERP trên DB gộp, **cộng thêm hợp đồng mới của HRM (`hrm_contracts`)**, và **sửa 3 lỗi sẵn có ở cả hai bên**
(xem §6). Màn chỉ đọc.

## 2. Mục tiêu / Không làm / Phản mục tiêu

**Mục tiêu**
- Bộ lọc, bảng phòng → NV có dòng Tổng cộng, popup chi tiết theo HĐ, In, Xuất Excel — đủ như ERP.
- Popup chi tiết hiện đúng mã HĐ + khách hàng cho cả HĐ ERP (hãng, dịch vụ) lẫn HĐ mới HRM.
- Phạm vi quyền đúng 4 cấp theo mã RBAC `sale.bao_cao_thuong_theo_nhan_vien.view` (đã có trong catalog `hrm-api/app/Support/Permissions/Catalog/sale.php:840`, scopes 1-4).
- ERP được vá cùng đợt để 2 màn cho cùng số.

**Không làm**
- Không port màn "Báo cáo thưởng theo hợp đồng" (`report.bonus_business_contract`); dòng phòng ở HRM **không có link** (chỉ hiện mã - tên phòng).
- Không đổi công thức 3 cột thưởng; không thêm cột / bộ lọc ngoài ERP.

**Phản mục tiêu (chạy được vẫn là hỏng)**
- Số lệch ERP (sau khi ERP đã vá) ở bất kỳ cột / dòng tổng nào.
- Người không đủ quyền thấy thưởng của người khác — ở bảng, dòng tổng, popup, In, Excel.
- Hai HĐ khác loại trùng id bị cộng chung một dòng trong popup.

## 3. Nguồn ERP cần bám

Repo `ERP/TanPhatDev` (Laravel 6):
- Routes `routes/web.php:3233` (`report.getDetailByEmployee` — popup), `:3238-3241` (index, searchData, print, export).
- Controller `app/Http/Controllers/ReportController.php:2113-2160` (index/searchData/print/export), `:4334` (`getDetailByEmployee` + dòng tổng popup).
- Service `app/Services/Reports/BonusBusinessEmployeeReportService.php` — toàn bộ logic: `getCostEmployees`, `getDataDepartment`, `filterDate`, `renderDataBonusBusinessDepartments`, `getDetailByEmployee`, `printListData`.
- View `resources/views/reports/bonus_business_employee.blade.php` (bảng, popup, per_page = 10, bắt buộc Từ/Đến ngày).
- In: `report_templates.id = 309` (`ReportTemplate::BAO_CAO_THUONG_THEO_NHAN_VIEN`), khổ ngang. Excel: `PositionInventoryReportList` với cùng bảng HTML của `printListData`, tên file `bao_cao_thuong_theo_nhan_vien.xlsx`.

## 4. Số liệu (bám ERP)

**Nguồn:** `account_details` với `account_id = 117`, `invoiceable_type` KHÔNG thuộc BillPayment / BillPaymentAuthorization / ClosingEntry,
`contractable_id` và `employee_id` khác NULL. Mỗi cột = Σ bên Có (`type = 2`) − Σ bên Nợ (`type = 1`) của `money_value_exchange`, theo `work_id`:

| Cột | work code |
|---|---|
| Thưởng thực hiện hợp đồng (`diff_employee`) | `TTHHD` |
| Thưởng năng suất tháng (`commission_month`) | `TNST` |
| Thưởng năng suất quý (`commission_quarter`) | `TNSQ` |

Tổng cộng = 3 cột cộng lại. Lấy id work theo code (`works.code`), không hard-code id.

**Lọc ngày:** `invoiceable_date_accounting` trong [Từ ngày 00:00:00, Đến ngày 23:59:59]; cả 2 ô bắt buộc.

**Bảng chính:** gom theo `employee_id`, bỏ NV có cả 3 cột = 0. Xếp NV vào **phòng hiện tại** (thành viên phòng, như ERP `Department::members` → `employee_system`) — user chốt; phòng `status = 1`.
Một NV thuộc nhiều phòng thì hiện ở mỗi phòng như ERP. Dòng phòng = tổng NV trong phòng; dòng Tổng cộng đầu bảng tính trên **toàn bộ** kết quả, không chỉ trang đang xem.
Phân trang theo **phòng**, 10 phòng / trang như ERP. STT phòng `n`, NV `n.m`. Số 0 hiện `-`.

**Bộ lọc:** Công ty / Phòng ban / Bộ phận (bộ lọc chuẩn HRM theo cờ quyền) · Từ ngày · Đến ngày. Nút Lọc, Làm mới, In, Xuất Excel.

**Popup chi tiết (bấm tên NV):** cùng bộ lọc ngày, NV đó; gom theo **(`contractable_type`, `contractable_id`)**. Cột: STT · Hợp đồng · Khách hàng (mã - tên) · 3 cột thưởng · Tổng cộng, có dòng tổng.

## 5. Hợp đồng mới HRM

Popup phải đọc mã HĐ + khách hàng theo đúng loại:

| `contractable_type` | Bảng | Mã HĐ | Khách hàng |
|---|---|---|---|
| `App\Model\Sale\Firm\Contract\FirmContract` | HĐ hãng ERP | `code` | `customer` |
| `App\Model\Customers\WrServiceContract` | HĐ dịch vụ ERP | `code` | `customer` |
| `Modules\Assign\Entities\Contract\Contract` | `hrm_contracts` | `code` | `Contract::customer()` → bảng `customers` qua `hrm_contracts.customer_id` (`code`, `fullname`) |
| loại khác | — | để trống, vẫn hiện số | — |

Ghi nhận khi khảo sát (DB local `erp_hrm_check`, 14/11): bút toán TK117 của 3 work trên hiện chỉ có 2 loại ERP (FirmContract 115.670 dòng, WrServiceContract 12.949 dòng).
Chưa có dòng nào của HĐ HRM — nhánh HĐ HRM cần test bằng dữ liệu dựng tay. Bảng chính không phụ thuộc loại HĐ nên tự nhận HĐ HRM.
Nguồn ghi sau này: các phiếu quyết toán thưởng đã port sang HRM nhận HĐ HRM với đúng chuỗi type này
(`hrm-api/Modules/Finance/Services/BillProductivitySettlementQuarterCalculator.php:37` `TYPE_HRM_CONTRACT`). Không có morph alias.

## 5b. Các quyết định của Claude (user chưa xác nhận — xem khi duyệt)

- **Tổng cộng = tổng các dòng đang có**, giữ đúng như ERP:
  - NV ở nhiều phòng thì cộng nhiều lần.
  - NV có thưởng nhưng không thuộc phòng `status = 1` nào thì không hiện, và không vào tổng.
  - Lý do: ưu tiên khớp số ERP.
- **Cấp Công ty:**
  - Phạm vi là "công ty đang chọn" (`current_company_role`), như `SalesIncomeScope`.
  - Ô lọc Công ty để trống thì vẫn chỉ trong công ty đó.
- **Cấp Phòng ban / Bộ phận** mà người xem không quản lý phòng nào / không có bộ phận: chỉ thấy chính mình.
- **Popup ERP dùng chung với màn "Thưởng theo hợp đồng":**
  - Khi vá quyền ở ERP, popup cho xem NV nếu NV nằm trong phạm vi của **một trong hai** mã: `sale.bao_cao_thuong_theo_nhan_vien.view` hoặc `accounting.bao_cao_thuong_theo_hop_dong.view`.
  - Như vậy không làm hỏng màn kia.
- **In / Excel ERP** gọi lại đúng `bonusBusinessEmployeeSearchData`, nên vá một chỗ là cả 2 theo.
- **Mẫu in 309:** dùng nguyên, không sửa, vì sửa sẽ đổi luôn bản in ERP.

## 6. Ba lỗi ERP — sửa ở cả HRM và ERP (`develop_02`)

1. **Popup gom HĐ chỉ theo `contractable_id`** (`getDetailByEmployee`: `groupBy('contractable_id')`) → HĐ hãng và HĐ dịch vụ trùng id bị cộng chung, mã/khách hàng lấy ngẫu nhiên một bên.
   Sửa: gom theo `contractable_type, contractable_id`. ⚠️ Hàm này dùng chung với popup màn "Báo cáo thưởng theo hợp đồng" (`bonus_contract_report.blade.php:390`), nên sửa xong màn đó cũng đúng theo.
2. **Ô tổng "Thưởng NS quý" trong popup** kiểm tra nhầm `total_.commission_month` (view `:195`) → quý có số nhưng tháng = 0 thì hiện `-`. Sửa: kiểm tra `commission_quarter`.
   (Dòng tổng BE `ReportController:4334` đã cộng đủ 3 cột — chỉ sai ở view.)
3. **Quyền lấy số lệch quyền mở màn:** index dùng mã RBAC, còn searchData xét 4 quyền tên cũ "Xem báo cáo chi phí bán hàng theo nhân viên…". Ở cấp bộ phận, người xem vẫn thấy NV cả phòng (lọc bộ phận đang comment).
   Popup `report.getDetailByEmployee` **không kiểm quyền gì**: gửi `employee_id` bất kỳ là xem được thưởng theo HĐ của người đó.
   Sửa (cả 2 bên): searchData / popup / In / Excel đều dùng `permissionScope('sale.bao_cao_thuong_theo_nhan_vien.view')`, áp như §7.

## 7. Quyền (HRM, và ERP sau vá)

Màn **không gate**: ai cũng vào được; không có quyền thì chỉ thấy số của **chính mình** (NV hưởng = `account_details.employee_id`).

| Cấp | Thấy |
|---|---|
| Tổng công ty (4) | tất cả |
| Công ty (3) | NV thuộc phòng của công ty đang chọn, HOẶC chính mình |
| Phòng ban (2) | NV thuộc phòng mình quản lý (`employee_manage_departments`), HOẶC chính mình |
| Bộ phận (1) | NV thuộc bộ phận của mình, HOẶC chính mình |

Phạm vi áp theo **phòng / bộ phận hiện tại của NV** (đi cùng cách xếp phòng ở §4), không theo cột tổ chức trên bút toán.
Popup kiểm lại: NV được xem phải nằm trong phạm vi, ngoài phạm vi thì trả rỗng (không tin `employee_id` client gửi).
FE nhận cờ `is_all_company / is_company / is_department / is_part` từ API meta để hiện bộ lọc, như màn Tổng hợp thu nhập BH.

## 8. HRM — vị trí và khuôn

- Đường dẫn FE: `/sale/bonus-business-employee`. Menu: gắn link vào placeholder "Thưởng theo nhân viên" ở `hrm-client/components/subsystem-menu/sale-hub.js:266`.
- Khuôn: bám màn đã port **Bảng tổng hợp thu nhập từ bán hàng** (`/sale/sales-income-summary`):
  - BE: controller + service ở `Modules/Finance` (`SalesIncomeSummaryController`, `Services/SalesIncome/*`), gồm meta (cờ quyền), index, detail, export (cây đầy đủ không phân trang), print theo `report_templates`.
  - FE: `V2BaseSmartFilterPanel`, popup `V2BaseModal`, Excel FE (`export-excel.js`).
- In: dùng lại `report_templates.id = 309` (DB chung), khổ ngang, các biến `CHI_TIET`, `NGAY/THANG/NAM`, `TU_NGAY/DEN_NGAY`, `HEADER` như ERP.
- Excel: tiêu đề "Báo cáo thưởng theo nhân viên", khoảng ngày, cột như bảng, dòng phòng in đậm, dòng NV thường; tên file `bao_cao_thuong_theo_nhan_vien.xlsx`.
- Skill áp dụng: `erp-to-hrm-screen`, `report-styles`, `export-excel`, `print-page`, `modal-popup`.
- Deploy: chạy `catalog-sync` nếu cần cho mã quyền.

## 9. Để lại cho người làm

- Cách viết truy vấn (một câu SQL có subquery hay Eloquent như ERP). Điều kiện bắt buộc: số khớp ERP sau vá, và không N+1 khi popup có nhiều HĐ.
- Đặt tên class / route API theo quy ước module Finance.
- Kiểm chứng: so số HRM với ERP đã vá trên cùng DB (ít nhất 1 khoảng ngày có cả HĐ hãng và HĐ DV, và 1 NV có HĐ trùng id khác loại nếu tìm được).
  Test quyền 4 cấp + không quyền; Playwright cho màn HRM và màn ERP đã vá.
