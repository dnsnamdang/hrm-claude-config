# Thiết kế — Port "Báo cáo doanh số theo nhân viên kinh doanh" ERP → HRM

> Trạng thái: **ĐÃ DUYỆT 23/11/2026** — code xong 2 pha, ĐÃ push develop (chưa gop_db). Người làm: @nguyentrancu97. Plan: `plan.md`.
> Nguồn ERP là chuẩn số liệu. HRM là chuẩn giao diện (bám skill `erp-to-hrm-screen`).

## 1. Ý định & bối cảnh (why)

Port báo cáo **"Báo cáo doanh số theo nhân viên kinh doanh"** từ ERP sang HRM, kèm một số nâng cấp theo
yêu cầu nghiệp vụ. Báo cáo cho lãnh đạo/kế toán xem doanh số theo từng nhân viên kinh doanh, bung theo
cây **Phòng ban ▸ Nhân viên ▸ Hợp đồng**, với 4 cột tiền. Đây là màn mới hoàn toàn ở HRM (grep xác nhận
HRM chưa có màn/endpoint riêng).

## 2. Mục tiêu / Không mục tiêu / Chống mục tiêu

**Mục tiêu**
- Port đúng 4 cột tiền của ERP, **số khớp ERP** ở chỉ tiêu 1.
- Nâng cấp theo yêu cầu: cột "Doanh số xuất hàng" cộng thêm phần phối hợp tạm tính; chú thích tiêu đề;
  sort cột tiền; ô lọc "Phối hợp bán hàng"; form cấp xem NV ▸ HĐ (form mới anh Nam); 2 chỉ tiêu xem.
- Giao diện bám khuôn màn HRM **BC thưởng theo quý** (`bonus-quarter-report`).

**Không mục tiêu**
- Không sửa báo cáo ERP gốc (ERP vẫn chạy song song).
- Không port các màn phối hợp / hỗ trợ hạch toán (đã có dữ liệu sẵn ở bảng `*_support_accounting_*`).

**Chống mục tiêu (fail dù chạy được)**
- Số liệu chỉ tiêu 1 **lệch ERP** → coi như hỏng.
- Hardcode id tài khoản của ERP vào HRM (sai đa công ty) — xem Ràng buộc §4.
- Lộ dữ liệu chéo công ty do bỏ phân cấp quyền xem.

## 3. Nguồn ERP (đã đọc tới gốc — file:dòng)

**Controller** `app/Http/Controllers/ReportController.php`:
- `bySalesStaff()` :6311 (render), `bySalesStaffSearchData()` :6323 (bảng chính, cache 10'),
  `bySalesStaffSearch()` :6487 (modal drill, phân nhánh `type` 1–4), print :6384, export :6428,
  printDetail :6535, exportDetail :6597. Route `routes/web.php:3462-3468`.
- Quyền: `sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view` (scope 4 cấp).

**Service** `app/Services/Reports/BySalesStaffService.php` (2418 dòng):
- `getData()` :33 (view phòng ban) / `getDataEmployee()` :105 (view cá nhân).
- `getFirstContractIds()` :122 — tập HĐ: bút toán **đầu tiên** của HĐ (TK 131, `AccountDetail::getAccountChild(131)` :129) rơi trong kỳ (`havingRaw('MIN(invoiceable_date_accounting) >= ...')` :139).
- 4 chỉ tiêu cột: `getContractData()` :1554, `getActualRevenue()` :1626, `getSupportAccounting()` :1770,
  `getSettlementContract()` :1854 (+ biến thể `...Department()` / `...Employee()`).

**4 cột tiền** (blade `resources/views/reports/by_sales_staff.blade.php:95-108`):
1. **Tổng giá trị HĐ trước thuế** = `total_product_before_vat` ← `firm.total_before_vat` (getContractData).
2. **Doanh số xuất hàng** = `total_actual_revenue` ← công thức 511/5213 (getActualRevenue).
3. **DSTC HĐ có hiệu lực** = `commission_sale` ← `SUM(fe.commission_sale)` (getSupportAccounting).
4. **DSTC HĐ quyết toán** = `settlement_commission_sale` ← `sce.commission_sale`, `sc.status=5`, `fscd.type=2`.

**Công thức cột 2 (getActualRevenue :1640-1653):**
```sql
SUM(CASE WHEN ac.type = 2 THEN money_value_exchange ELSE 0 END)   -- PS Có
- SUM(CASE WHEN ac.type = 1 THEN money_value_exchange ELSE 0 END) -- PS Nợ
FROM account_details ac JOIN firm ON firm.id = ac.contractable_id
WHERE ac.contractable_type IN (FirmContract, WrServiceContract)   -- bản WR :1718
  AND ac.employee_id = <nhân viên>
  AND ( ac.account_id IN (181..187)  -- 511 + các con 5111..5118
     OR ac.account_id IN (192) )     -- 5213 "Giảm giá hàng bán"
```
- `ac.type`: **2 = Có, 1 = Nợ**.
- Mapping id↔số hiệu TK ở `database/seeds/SyncAccount.php:200-212`: `181=511 … 187=5118`, `192=5213`.
  **Chỉ gồm 511(+con) và 5213** — KHÔNG lấy 521 cha, 5211 (chiết khấu), 5212 (hàng bán trả lại).
  (User đã xác nhận giữ đúng tập này.)
- Loại trừ phiếu kết chuyển: ERP báo cáo này loại **ngầm** qua INNER JOIN vào HĐ (bút toán kết chuyển
  không gắn contractable nên rớt). Port HRM vẫn join HĐ nên loại ngầm tương tự; **không** cần
  `whereNotIn ClosingEntry` trừ khi QA phát hiện lệch.

**Phối hợp / hỗ trợ hạch toán** (getSupportAccounting :1788-1802):
`firm_support_accounting` → `firm_support_accounting_departments` (fd) → `firm_support_accounting_employees` (fe).
Bản WR: `wr_support_accounting_*`. Cột ở `fe`: `employee_id`, `commission_sale_percent`
(% doanh số được ghi nhận), `commission_sale` (số tiền chia). Cột 3 của báo cáo = `SUM(fe.commission_sale)`
group `firm.id + fe.employee_id`.

**Phân cấp quyền** (ReportController :6313-6319, áp trong filter :1183-1213):
`is_all_company` (không giới hạn) / `is_company` (công ty + bản thân) / `is_department`
(`whereIn employee_department_id, $departmentManagement` + bản thân) / `is_part`/mặc định
(`employee_id = auth id`). Không cấp nào → `getDataEmployee()` cá nhân.

**Bảng giá**: ERP **chưa dùng** trong báo cáo (biến `$price_types` nạp nhưng không truyền ra view). Chỉ tiêu 2
là phần mới hoàn toàn.

## 4. Ràng buộc

- **Id tài khoản phải giải theo SỐ HIỆU, không hardcode.** DB HRM là `erp_hrm_check` (gop_db), mỗi công ty
  có bộ `accounts` riêng → id của 511/5213 **khác nhau giữa các công ty**. Dùng `AccountDetail::getAccountChild()`
  (hoặc tra `accounts` theo code 511*, 5213) để lấy đúng tập id theo công ty, giống cách ERP tự dùng cho TK 131
  ở `getFirstContractIds`. Hardcode `[181..187,192]` = sai đa công ty.
- `firm_contracts.price_type` và `service_contracts.price_type` là **integer cấp hợp đồng** (1 HĐ = 1 loại giá),
  trỏ danh mục `price_types` (có cột `order`). **Phải verify 2 bảng này + `price_types` tồn tại trong DB HRM**
  trước khi làm chỉ tiêu 2.
- Phân trang theo pattern **#12205**: cắt trang theo DÒNG GỐC (HĐ × NV) **trước**, gộp cây **sau**;
  `summary`/`total` tính trên TOÀN BỘ rows. Giữ nguyên hành vi (1 phòng có thể nằm 2 trang, STT theo trang).
- Quyền dùng Catalog (`hrm-api/app/Support/Permissions/Catalog/`): tìm mã có sẵn cho báo cáo này; chưa có thì
  tạo `sale.bao_cao_doanh_so_theo_nhan_vien_kinh_doanh.view` (có `scopes` 4 cấp), thêm `hrm` vào `platforms`,
  chạy `permission:catalog-sync`. KHÔNG seeder, KHÔNG tự gán vai trò.
- Nhãn, định dạng số (`,` nghìn `.` thập phân), màu nút/trạng thái, bộ thông báo: theo skill `erp-to-hrm-screen`
  + `list-page` + SRS.
- KHÔNG commit/push/gop_db khi chưa có lệnh user.

## 5. Cách làm đã chốt (A1 + B2)

### 5.1 Cấu trúc 2 chỉ tiêu (A1 — một màn, "Chỉ tiêu" là dropdown trong bộ lọc)
Một trang + một service dùng chung, param `criterion` (1 = Tổng doanh số, 2 = Chi tiết theo bảng giá):
- **Chỉ tiêu 1**: cây **Phòng ▸ NV ▸ HĐ** (3 tầng).
- **Chỉ tiêu 2**: chèn thêm tầng Loại giá → **Phòng ▸ NV ▸ Loại giá ▸ HĐ** (4 tầng). Khóa gom ở `service.tree()`
  thêm 1 cấp lấy theo `firm.price_type`; mỗi dòng Loại giá = tổng các HĐ của NV thuộc loại giá đó.
- 4 cột tiền **y hệt** ở cả hai chỉ tiêu; chỉ khác độ sâu cây. Ô "Cấp xem" ở chỉ tiêu 2 có thêm mục
  "Đến loại giá".

### 5.2 Trình tự (B2 — chỉ tiêu 1 trước, đối chiếu ERP, rồi mới chỉ tiêu 2)
- **Pha 1**: màn + service chỉ tiêu 1 đầy đủ (4 cột, phối hợp tạm tính cột 2, sort, lọc "Phối hợp bán hàng",
  chú thích tiêu đề, cấp xem NV▸HĐ, in/Excel/tùy chỉnh cột, phân trang #12205, phân cấp quyền). **Đối chiếu số
  khớp ERP** trên DB thật (nhiều NV, nhiều công ty) → chốt.
- **Pha 2**: thêm tầng Loại giá cho chỉ tiêu 2 (dropdown Chỉ tiêu + 1 cấp cây + mục "Đến loại giá").

### 5.3 Form xem — khuôn `bonus-quarter-report`
- Component cây `BySalesStaffTable.vue` song sinh `BonusQuarterTable.vue`: ô `V2BaseSelect size=xs` "Cấp xem"
  trong tiêu đề cột tổ chức; `level` **chỉ là cách xem phía client (bung sẵn tới cấp nào), KHÔNG gửi API** —
  BE luôn trả nguyên cây. Options chỉ tiêu 1: {Chỉ phòng ban, Đến nhân viên, Đến hợp đồng}; chỉ tiêu 2 thêm
  {Đến loại giá} xen giữa NV và HĐ.
- `index.vue`: `V2BaseSmartFilterPanel floating` + `V2BaseCompanyDepartmentFilter` (slot tổ chức) + header
  actions (Cấu hình cột / In / Xuất Excel). Mixin: `PageTitleMixin`, `CheckPermission`, `filterStateMixin`,
  `columnCustomizationMixin`. `columnScreenKey` mới duy nhất, vd `sale_by_sales_staff_report`.

### 5.4 Nâng cấp nghiệp vụ

**(a) Cột "Doanh số xuất hàng" cộng phối hợp tạm tính — CHỐT PA (cộng dồn).**
> ⚠️ ERP **không có** blend này; đây là chỉ tiêu MỚI. Sau blend, **cột 2 KHÔNG còn khớp tổng ERP** (cố ý).
> Chỉ cột 1/3/4 + **phần base cột 2** (trước blend) đối chiếu khớp ERP. Test: base cột 2 == ERP, rồi cộng
> blend như số hạng tách riêng.

Với `R(C)` = doanh số 511/5213 của **cả HĐ** C; `%e` = `commission_sale_percent` NV e ở bảng hỗ trợ hạch toán:
```
Cột2(e) = [doanh số trực tiếp: Σ account_details nơi ac.employee_id = e, TK 511(+con)+5213]
        + [phối hợp: Σ các HĐ phối hợp C mà e là NV tham gia của  R(C) × %e ]
```
- **Cộng dồn**: NV chính giữ đủ phần trực tiếp; NV tham gia được cộng thêm phần ước tính. Tổng cột 2 có thể
  **vượt** tổng doanh số thực (một HĐ tính cho cả chủ HĐ lẫn người phối hợp) — đúng nghĩa "tạm tính".
- `R(C)` lấy của **cả HĐ** (tổng mọi employee_id trên bút toán của C), KHÔNG khử trùng với phần trực tiếp.
- Gồm **cả** `firm_support_accounting_employees` (firm) lẫn `wr_support_accounting_employees` (HĐ dịch vụ WR).
- HĐ phối hợp C **không bắt buộc** nằm trong tập `getFirstContractIds` của kỳ: phần phối hợp cộng cho mọi HĐ
  e tham gia có `R(C)` phát sinh trong kỳ (lọc TK 511/5213 theo kỳ, không lọc theo bút toán 131 đầu kỳ).
- Dòng HĐ trong cây hiển thị cột 2 = **tổng** (trực tiếp + phối hợp của NV đó trên HĐ đó); cộng dồn lên NV, Phòng.

**(b) Chú thích tiêu đề**: thêm icon info/tooltip (skill `info-icon-tooltip`) cạnh tiêu đề cột "Doanh số
xuất hàng": *"Doanh số xuất hàng = PS Có 511 − PS Nợ 511 + PS Có 521 − PS Nợ 521 (Đã bao gồm nhập trả lại)"*.
(Giữ nguyên câu chữ user yêu cầu dù code chỉ gộp 5213.)

**(c) Sort cột tiền tăng/giảm** — pattern `bonus-contract-report`: FE `th.th-sort` + state `sort{column,order}`
gửi `sort_column`/`sort_order`; BE hằng `SORTABLE` (whitelist 4 cột tiền) + `sort()` validate + orderBy, phụ ổn
định theo `contractable_id`.

**(d) Lọc "Phối hợp bán hàng"** — field select nhị phân trong popup (khuôn `sales-income-summary.has_invoice`):
`{ key:'coordinated', label:'Phối hợp bán hàng', type:'select', placeholder:'Tất cả',
options:[{id:'1',name:'Có phối hợp'},{id:'0',name:'Không'}] }`. Khi `='1'` → chỉ hiện HĐ có bản ghi
`*_support_accounting_*`. Default rỗng = tất cả.

## 6. Khuôn HRM bám theo (file:dòng)
- Cây NV▸HĐ + ô Cấp xem: `pages/sale/bonus-quarter-report/components/BonusQuarterTable.vue:33,247,260-264`;
  service `Modules/Finance/Services/BonusQuarter/BonusQuarterReportService.php:50-68,85,125-163`.
- Sort cột tiền: `pages/sale/bonus-contract-report/index.vue:90-96,297,436-439`;
  `Modules/Finance/Services/BonusContractReport/BonusContractReportService.php:41,52-61,139`.
- Lọc nhị phân: `pages/sale/sales-income-summary/index.vue:300-307`.
- Chỉ tiêu dropdown: `pages/sale/compare-contract-by-time-report/index.vue:283` (field select `target`).

## 7. Để lại cho người làm (builder)
- Tên route/slug HRM (`/sale/by-sales-staff-report` hoặc theo sheet quy hoạch phân hệ) + vị trí menu
  (sheet quy hoạch trước, menu ERP tham chiếu; khai `sale-hub.js` + các file menu liên quan).
- Danh sách cột xuất Excel + template in (map `ReportTemplate::BAO_CAO_DOANH_SO_THEO_NHAN_VIEN_KINH_DOANH`).
- 4 modal drill-down (type 1–4) — port sau hoặc cùng pha 1 tùy khối lượng; nêu rõ trong plan.
- Xác định mã quyền Catalog cụ thể.

## 8. Quyết định đã CHỐT với user (23/11/2026)

- **Công thức cột Doanh số xuất hàng = PA (cộng dồn)** — chi tiết §5.4a.
- **Tỷ lệ** = `commission_sale_percent` cấp nhân viên (`*_support_accounting_employees`).
- **Gồm cả HĐ dịch vụ (WR)** ở phần phối hợp (base cột 2 vốn đã tính FirmContract + WrServiceContract).
- **NV thuộc nhánh phòng của chính NV** (hồ sơ nhân sự), không theo phòng hỗ trợ trên bảng hạch toán.
- **Phân trang #12205**: dòng gốc = HỢP của (HĐ×NV trực tiếp) ∪ (HĐ×NV chỉ phối hợp); NV chỉ phối hợp vẫn
  có dòng HĐ đó.
- **Quyền own-scope**: NV thấy dòng của chính mình (kể cả nhờ phối hợp); báo cáo theo từng NV nên không lộ
  số NV khác.
- **Lọc "Phối hợp bán hàng"=Có**: hiện HĐ có ≥1 bản ghi `*_support_accounting_employees` (firm + WR);
  `summary`/`total` tính lại trên tập đã lọc.
- **Chỉ tiêu 2, HĐ thiếu `price_type`**: gom nhóm **"Chưa xác định"** (KHÔNG loại — để tổng chỉ tiêu 2 =
  chỉ tiêu 1); thứ tự dòng Loại giá theo `price_types.order`.

## 9. Phương án đã cân nhắc & loại
- **A2 (tách 2 route theo `mode`)**: loại — user mô tả một báo cáo đổi chỉ tiêu, tách đôi thừa menu + nhân đôi code.
- **B1 (làm trọn một lượt)**: loại — chỉ tiêu 2 không có ERP soi số; dồn rủi ro số liệu. B2 làm chắc phần có
  "đáp án" (chỉ tiêu 1 khớp ERP) trước.
