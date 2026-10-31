# Port màn **Phiếu hạch toán dịch vụ — HDDV** (ERP → HRM)

> Phiếu "#2" của luồng hạch toán dịch vụ phía BÁN. Là **đích** của nút "Hạch toán chi phí"
> ở màn Yêu cầu hạch toán dịch vụ HDDV (YCHTDV) đã port trước đó.
> Màn này **sinh bút toán** (ghi `account_details`), đóng luồng YCHTDV / nghiệm thu.

- **Ngày tạo tài liệu:** 2026-10-30
- **Nhánh:** ERP `gop_db` · hrm-api/hrm-client `develop` · DB gộp `erp_hrm_check` (KHÔNG migration — bảng ERP có sẵn)
- **Nguồn ERP:** `admin/customer-care/wr_accounting_services?type=all` · route `WrAccountingService.*`
  · controller `App\Http\Controllers\Customercare\WrAccountingServicesController` (285 dòng)
  · model `App\Model\Customers\WrAccountingService`
- **Màn anh em đã port (khuôn FE/BE):** `wr-accounting-service-requests` (YCHTDV — phiếu #1)

---

## 1. Ý đồ & phạm vi

### Phiếu này LÀ gì
Phiếu hạch toán dịch vụ nhận **một nguồn** (YCHTDV `Chờ duyệt` **hoặc** Kết quả nghiệm thu
`WrAssignTask`), **tính bút toán** theo hợp đồng dịch vụ, **ghi `account_details`**, rồi lật trạng
thái nguồn sang hoàn tất. Trạng thái phiếu **duy nhất**: `Đã hạch toán = 1` (xanh `#16A34A`). Không
nháp, không chờ duyệt.

Hai đường tạo (ERP `create`):
| Tham số vào | `type_accounting` | Nguồn dữ liệu | Có gì |
|---|---|---|---|
| `wr_accounting_service_request_id` | `cost` | `WrAccountingServiceRequest::getForShow` (YCHTDV) | chỉ **chi phí** (total_cost) |
| `wr_approve_result_id` | `service` | `WrAssignTask::getForShow` (nghiệm thu) | chỉ **dịch vụ** (total_service) |

### Màn/chức năng trong scope
1. **Danh sách** (`index`, `type=all`): **chỉ XEM + Xuất Excel**. ERP **cột Hành động đã comment →
   KHÔNG có nút dòng**; toolbar **chỉ Xuất Excel** (không Thêm/Import/In). Phân quyền 3 cấp.
2. **Chi tiết** (`show`): 2 khối — "Thông tin chung" (link HĐ / nghiệm thu, KH/người yêu cầu/phòng
   chỉ-đọc) + "Hạch toán" (bảng bút toán). 3 bảng chi tiết: **Dịch vụ · Chi phí khác · Vận chuyển**.
   Footer chỉ **Quay lại** (ERP không có In). Không nút sửa/xóa.
3. **Tạo + Duyệt** (`create` + `store`): mở từ nút **"Hạch toán chi phí"** của YCHTDV (đường `cost`)
   hoặc từ nghiệm thu (đường `service`). Form hiện HĐ + bảng bút toán tính sẵn; nút **Duyệt** =
   `store` → tạo phiếu + ghi `account_details` + lật nguồn. **Tạo xong KHÔNG sửa/xóa được** (ERP
   không có route update/delete cho phiếu — chỉ có `delete` ẩn; xem §6 Quyết định).

### Ngoài scope / để link trống (màn đích CHƯA port)
- **Màn HĐ dịch vụ** (`WrServiceContract`) — "Số hợp đồng" để chữ, không link (giống YCHTDV).
- **Màn nghiệm thu `WrAssignTask`** — nếu chưa port thì đường tạo `service` **tạm chưa nối** (xem §6).
- Không port `exportList` kiểu ERP server-side → dùng khuôn **export-rows** của HRM.

---

## 2. Dữ liệu (bảng ERP sẵn trên DB gộp — KHÔNG migration)

| Bảng | Vai trò | Ghi chú cột |
|---|---|---|
| `wr_accounting_services` | phiếu | `total_service`, `total_cost` kiểu **text/json**; fillable: code, wr_service_contract_id, wr_approve_result_id, customer_id, customer_name, status, company_id, department_id, created_by, total_service, total_cost, wr_accounting_service_request_id |
| `wr_accounting_service_items` | con **DỊCH VỤ** | service_id, service_name, qty, price, amount, …, amount_cost_price, vat_percent, vat_cost_allocated, allocated_price, amount_allocated, amount_allocated_after_vat |
| `wr_accounting_service_costs` | con **CHI PHÍ/VẬN CHUYỂN** | cost_id, cost_name, price, …, cost_price, vat_percent, vat_cost, price_after_vat (cost_id=5 ⇒ vận chuyển) |
| `account_details` + `account_detail_refs` | SỔ bút toán | ghi qua `AccountDetail::saveAccountDetail` (đã có ở HRM) |
| `wr_support_accounting*` | HTHT HĐ dịch vụ (cụm B5) | entity HRM đã có: `WrSupportAccounting` + `...Department` + `...DepartmentDetail` + `...Employee` |

**invoiceable_type của phiếu** = chuỗi ERP `App\Model\Customers\WrAccountingService` (xác nhận trong
`CustomerDebtAggregator`, `AccountDetail` ERP, báo cáo công nợ). ⇒ **Phase 2 phải thêm hằng**
`INVOICEABLE_WR_ACCOUNTING_SERVICE = 'App\\Model\\Customers\\WrAccountingService'` vào HRM
`Modules/Finance/Entities/Account/AccountDetail.php` để báo cáo công nợ HRM (nếu đã port) nhận ra.
**contractable_type** = `App\Model\Customers\WrServiceContract` (ERP truyền `WrServiceContract::class`).

---

## 3. Kiến trúc port — tận dụng hạ tầng SẴN CÓ

HRM **đã có đủ** hạ tầng hạch toán, nên port = "bê công thức bút toán dịch vụ + gọi helper có sẵn",
KHÔNG dựng mới hạ tầng kế toán:
- `AccountDetail::createDataSaveDept(&$accounts, $number, $value, $type, $ref[], $objects[], $note)` —
  dồn 1 bút toán; **dùng KEY CỘT THÔ** (customer_id, employee_id, work_id, obj_department_id,
  employee_department_id, group, contractable_id/type, service_name…), KHÔNG ::class.
- `AccountDetail::saveAccountDetail($accounts, $invoiceable_id, $invoiceable_type, $invoiceable_code, $meta[])` —
  resolve `Account` theo identify_number, bỏ value≤0, ghi `account_details` + refs. `invoiceable_code`
  NOT NULL trên gộp → **phải truyền code phiếu**.
- **Khuôn posting:** `Modules/Assign/Services/ProductExportPostingService.php` (idempotent theo
  invoiceable, build `$meta`, DB::transaction) + `Accounting/SupportAccountingTrait.php` (8 cụm bán hàng).
  ⚠️ Trait type-hint `Contract $contract` (HĐ hãng) → **không dùng trực tiếp** cho HĐ dịch vụ. Cụm B5
  dịch vụ khác tên trường (contract_performance_bonus_before_vat, personal_income_tax,
  percent_export_not_cost). `WrSupportAccounting` đã khai accessor alias
  `bonus_contract_before_vat`→`contract_performance_bonus_before_vat`, `tndn_vat`→`personal_income_tax`.
  ⇒ **viết service posting RIÊNG** `WrAccountingServicePostingService`, có thể `use` lại các helper tra
  tổ chức của trait nếu tách được, nhưng port công thức B1–B5 theo đúng `getDataCreateDept` ERP.

### Entity (Modules/Finance/Entities/WrAccountingService/)
- `WrAccountingService extends Model` (bảng ERP, có `$casts` json total_service/total_cost; **không
  dùng BaseModel** vì bảng ERP + có boot hook gán company/department — service tự gán `created_by`).
  STATUS `DA_HACH_TOAN=1`; STATUSES xanh. `searchByFilter` 3 cấp; `canView` mirror; `generateCode('HTDV')`.
- `WrAccountingServiceItem` (dịch vụ), `WrAccountingServiceCost` (chi phí/vận chuyển).

### Service
- `WrAccountingServiceService` — list/show/export + `contractData`/`requestData` dựng form tạo +
  `store()` (tạo phiếu + gọi posting + lật nguồn, trong 1 transaction).
- `WrAccountingServicePostingService` — port `getDataCreateDept()`:
  - **Nhánh BAO_HANH (HĐ type 2):** g1 Nợ1311/Có5113+33311, g2 chiết khấu (5213/1311) nếu có rebate.
    ⚠️ **giữ NGUYÊN** bug ghi đè `rebate_price = sum_amount_after_vat` của ERP (port trung thành).
  - **Nhánh else (HOP_DONG…):** B1 doanh thu (1311/5113+33311) · B2 chiết khấu (5211+33311/1311) ·
    B3 giảm trừ (5213+33311/1311) · B4 giá vốn (1541/632 theo từng dịch vụ) · **B5 HTHT** (support
    accounting: percent_export_not_cost, thưởng 5211/35241, TNCN 35241/3335, HH tháng/quý 6411/35241,
    quỹ rủi ro 6411/35241 — fail-closed: thiếu HTHT/trưởng phòng → trả `[false, message]`).
  - **SỬA bug ERP:** nếu `saveAccountDetail` trả status=false thì **rollback** (ERP
    `responseSuccess` mà không rollback → bỏ sót). **KHÔNG port `dd($e)`** trong catch.
- `WrAccountingServiceNotifyService` — thông báo (theo `NotificationMeta::build`).

### FE (pages/finance/wr-accounting-services/)
- `index.vue` (list xem + export; 4 mixin chuẩn; cột: STT, Số phiếu hạch toán, Số hợp đồng, Khách
  hàng, Tổng thanh toán, Người yêu cầu, Người tạo, Ngày tạo, Trạng thái; **không cột Hành động**).
- `_id/index.vue` (chi tiết: khối Thông tin chung `V2BaseFormCard` + khối Hạch toán bảng bút toán +
  3 bảng Dịch vụ/Chi phí khác/Vận chuyển; `SystemInfoSection` lịch sử; footer chỉ Quay lại).
- `create.vue` + `components/WrAccountingServiceForm.vue` (dùng chung show/create readonly).
- Menu: `subsystem-menu/finance.js` + `subsystem-menu/sale-hub.js` nhóm "Dịch vụ", ngay sau YCHTDV.
- **Nối lại** `wr-accounting-service-requests/_id/index.vue` `goToAccounting()`: thay toast placeholder
  bằng `$router.push('/finance/wr-accounting-services/create?wr_accounting_service_request_id=<id>')`.

### Quyền (type 23 — Bán hàng, guard `api`, khai PermissionsTableSeeder)
- `Xem phiếu hạch toán dịch vụ HDDV - theo tổng công ty | công ty | phòng ban`
- `Hạch toán dịch vụ HDDV` (tạo phiếu + ghi sổ — ERP gate bằng `Kế toán kho` + cùng công ty)

---

## 4. Danh sách / lọc / cột (bám ERP nghiệp vụ + UI chuẩn HRM)

**Lọc:** code (text), customer_id (select ajax), wr_service_contract_code (text), requester_id (select),
created_by (select), status (select — chỉ 1 giá trị), khoảng ngày tạo. Ô Công ty chỉ hiện với người
xem mọi công ty (`meta.is_all_company`).

**Scope 3 cấp (`searchByFilter type=all`):** tổng công ty = tất cả · công ty = company_id OR created_by ·
phòng ban = department_id IN quản-lý OR created_by · không quyền = created_by. (type=index: created_by.)

---

## 5. Công thức bút toán (ERP `getDataCreateDept`, port trung thành)

`Work::getByCode()` → DTHH, CKHH, GGHH, TTHHD, TNST, TNSQ, RRP (map `accounting_works.id`, xác minh
Task 0 như ProductExportPostingService đã làm).

- **BAO_HANH:** sum = service.amount_after_extra + cost.other.price_after_extra +
  cost.delivery.price_after_extra; vat = sum×vat%. g1: Nợ1311=sum+vat, Có5113(DTHH, emp=created_by)=sum,
  Có33311=vat. g2 (nếu rebate): rebate=sum_after_vat (⚠️ giữ bug), Nợ5213(emp)=rebate, Có1311=rebate.
- **HOP_DONG (else):** B1 doanh thu / B2 chiết khấu (CKHH) / B3 giảm trừ (GGHH) / B4 giá vốn
  (Có1541 theo dịch vụ → Nợ632 tổng) / B5 HTHT (chi tiết trong code ERP 239–443, port 1-1).

Chi tiết số hiệu TK + ref + đối tượng: xem `design-phase2.md` (viết khi vào Phase 2).

---

## 6. Quyết định đã chốt

1. **Danh sách = chỉ xem + Xuất Excel**, không nút dòng, không nút Thêm — bám ERP (cột action đã comment).
2. **Tạo phiếu KHÔNG kèm sửa/xóa**: ERP chỉ có route `delete` (ẩn, không nút) và không có update thực
   cho phiếu đã hạch toán. HRM **không làm nút Sửa/Xóa** ở màn này (phiếu đã ghi sổ = bất biến). Muốn
   bỏ hạch toán → dùng luồng "Không duyệt" ở YCHTDV (đã có) để kéo YCHTDV về Đang tạo. *(Nếu ERP thực
   tế cho xóa phiếu hạch toán để ghi lại — xác nhận khi vào Phase 2 bằng cách đọc lại blade + test tài
   khoản thường; mặc định KHÔNG port xóa.)*
3. **Sửa 2 bug ERP khi port:** (a) rollback khi `saveAccountDetail` fail; (b) bỏ `dd($e)`.
   **Giữ trung thành** bug ghi đè `rebate_price` nhánh BAO_HANH (thay đổi số kế toán = phải user chốt).
4. **Đường tạo `service` (từ nghiệm thu `WrAssignTask`):** ưu tiên giao **đường `cost` (từ YCHTDV)
   trước** — đó là cái nối lại link trống đã hứa. Đường `service` chỉ nối được khi màn nghiệm thu đã
   port; nếu chưa, để nút ở màn nghiệm thu là link trống (giống quy ước các màn đích chưa port).
   **→ cần user xác nhận** màn nghiệm thu `WrAssignTask` đã/đang port chưa (quyết định đưa đường
   `service` vào Phase mấy).
5. **invoiceable_type/contractable_type** dùng NGUYÊN chuỗi FQN ERP (DB gộp chung bảng account_details
   với ERP — phải khớp để báo cáo công nợ 2 cổng đọc cùng dữ liệu).

### Câu hỏi còn treo cho user (ghi lại, chưa chặn Phase 1 BE list/show)
- Q1: Màn nghiệm thu `WrAssignTask` đã port HRM chưa? (quyết định đường tạo `service`).
- Q2 (carry-over từ phiếu YCHTDV, chưa trả lời): nút "Hạch toán chi phí"/"Số hợp đồng" ở YCHTDV để
  link trống hay `erpUrl()`? → khi port xong phiếu này, "Hạch toán chi phí" nối thẳng vào HRM
  (hết trống); "Số hợp đồng" vẫn trống tới khi port màn HĐ dịch vụ.

### Chốt khi triển khai (2026-10-31, đã commit/push develop)
- Q1 → **đường `service` (WrAssignTask) HOÃN** (HRM chưa có module Giao việc); `store()` chặn sớm bằng
  `RuntimeException`. Chỉ làm đường `cost` (từ YCHTDV).
- Q2 → "Hạch toán chi phí" ở YCHTDV **đã nối thẳng** `create?wr_accounting_service_request_id=<id>`;
  "Số hợp đồng" vẫn để trống tới khi port màn HĐ dịch vụ.
- QĐ #2 (xóa phiếu): giữ mặc định — **KHÔNG port Sửa/Xóa**; phiếu đã ghi sổ bất biến, bỏ hạch toán qua
  "Không duyệt" YCHTDV.
- Lệch UI so với QĐ #1: **GIỮ cột Hành động = chỉ Lịch sử** (skill bắt buộc Lịch sử ở list + chi tiết,
  bám ngang mọi màn anh em) thay vì bỏ hẳn cột action như ERP comment.
- Commit: hrm-api `06b01e074`, hrm-client `51f44677b`.
