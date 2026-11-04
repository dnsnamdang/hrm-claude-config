# Port màn **Phiếu hạch toán dịch vụ — HĐBH** (ERP → HRM)

> Phiếu "#2" của luồng hạch toán dịch vụ phía **BÁN theo Hợp đồng bán hàng / HĐ hãng**.
> Là **đích** của luồng **Yêu cầu hạch toán dịch vụ HĐBH** (`ServiceAccountingRequest`) đã port trước.
> Màn này **sinh bút toán** (ghi `account_details`), lật YC sang `Đã hạch toán`, đóng luồng.

- **Ngày tạo tài liệu:** 2026-11-03
- **Nhánh:** ERP `gop_db` (chỉ đọc) · hrm-api + hrm-client = **nhánh feature riêng tách từ `develop`** (user chốt 03/11), merge về develop sau khi xong · DB gộp `erp_hrm_check` (**KHÔNG migration** — bảng ERP có sẵn)
- **Nguồn ERP:**
  - Route: `admin/sale/service-accounting?type=all` · name `serviceAccounting.*`
  - Controller `App\Http\Controllers\Sale\ServiceAccountingController` (377 dòng)
  - Model `App\Model\Sale\ServiceAccounting` · con `ServiceAccountingItem` / `ServiceAccountingCost`
  - Excel `App\ExcelExports\ServiceAccountingExportExcel`
- **Màn anh em đã port (khuôn FE/BE):**
  - `phieu-hach-toan-dich-vu-hddv` (phiếu HDDV — gần nhất về bố cục) → `pages/finance/wr-accounting-services/`
  - YC HĐBH (`ServiceAccountingRequest`) → `Modules/Finance/.../ServiceAccountingRequest*`, `pages/finance/service-accounting-requests/` — **cung cấp nguồn tạo phiếu này**

---

## 1. Ý đồ & phạm vi

### Phiếu này LÀ gì
Nhận **một nguồn** = 1 **YC hạch toán DV** (`service_accounting_request_id`, bắt buộc). Copy
`contractable_id/type` + items + costs từ YC. Khi `status = Đã duyệt` thì **tính bút toán** theo
hợp đồng, **ghi `account_details`**, lật YC → `Đã hạch toán (5)` và lật `ServiceExportRequest` (nếu có)
→ `Đã hạch toán`, cập nhật ngày bàn giao HĐ. Trạng thái phiếu **2 mức**: `Đang tạo = 1` (primary),
`Đã duyệt = 2` (success). `type` phiếu: `Dịch vụ(1) · Chi phí(2) · Vận chuyển(3)`.

`contractable` là **morphTo**. ERP về lý thuyết cho `Contract` / `ServiceContract` / `FirmContract`,
nhưng **DB gộp thực tế**: truy vấn `service_accounting` → **1275/1275 dòng đều `FirmContract`**
(`App\Model\Sale\Firm\Contract\FirmContract`), **0 dòng** ServiceContract/Contract. ⇒ **Khóa scope
= FirmContract-only** (quyết định Claude, có dữ kiện DB): query thêm `where contractable_type =
FirmContract::class`, null-guard khi contractable rỗng, **bỏ hẳn nhánh else** (`getDataCreateDept` —
xem §3). Nếu sau này phát sinh loại HĐ khác thì mở rộng sau.

> **Dữ kiện DB gộp (03/11, đã kiểm):** 1275 phiếu — **tất cả** `FirmContract`, **tất cả** `status=2`
> (Đã duyệt), **0 dòng** `Đang tạo`. `service_accounting_items` = **0 dòng**; `service_accounting_costs`
> = **1378 dòng**; `account_details` invoiceable `...\ServiceAccounting` = **7257 dòng**. ⇒ (a) scope
> FirmContract chắc chắn; (b) thực tế dữ liệu nằm ở **bảng costs** — bảng Dịch vụ (items) sẽ **rỗng**
> với data hiện có, vẫn render bình thường; (c) checkpoint Phase 1 **khả thi** (có 1275 phiếu + 7257
> bút toán để đối chiếu).

### Hai pha (user chốt 03/11: "Phase 1 đọc trước")

**PHASE 1 — CHỈ ĐỌC (làm trước):**
1. **Danh sách** (`index`, `type=all`): xem + Xuất Excel. Phân quyền 3 cấp.
2. **Chi tiết** (`show`): Thông tin chung + 3 bảng con (Dịch vụ / Chi phí khác / Vận chuyển) + bảng
   **bút toán** (nhóm) + Lịch sử. Footer chỉ **Quay lại** (ERP không có In).
3. Quyền xem (api-guard) + menu.
4. **Checkpoint số liệu**: đối chiếu tổng thanh toán / bút toán hiển thị khớp ERP **trước khi** mở Phase 2.

**PHASE 2 — GHI (làm sau, chờ chốt số liệu):**
5. **Tạo từ YC** (`create` + `store`): mở từ nút ở màn YC HĐBH (đường `service_accounting_request_id`).
6. **Duyệt = hạch toán**: `store`/`update` với `status=Đã duyệt` → ghi `account_details` + lật YC/PXK.
7. **Sửa / Xóa**: **theo ERP** — chỉ khi `status = Đang tạo` **và** là người lập (xem §6).

### Ngoài scope / link trống
- Màn HĐ hãng (`FirmContract`) ở HRM: "Số hợp đồng" hiển thị `contractable->link`. Nếu màn đích chưa
  có route tương ứng ở HRM → để **chữ, không link** (giống cách YCHTDV xử lý).
- Không port `exportList` server-side của ERP → dùng khuôn **export-rows** HRM (`listExportFile.js`).

---

## 2. Dữ liệu (bảng ERP sẵn trên DB gộp — KHÔNG migration)

| Bảng | Vai trò | Ghi chú cột |
|---|---|---|
| `service_accounting` | phiếu | fillable: `service_accounting_request_id, contractable_id, contractable_type, status, note, type, payed_cost`; `approver_id`, `approved_at`, `created_by` (BaseModel ERP) |
| `service_accounting_items` | con **DỊCH VỤ** | service_id, service_name, service_code, service_level_id/name, qty, price, cost_price, value_discount, sale_max_percent, coefficient_cost_price |
| `service_accounting_costs` | con **CHI PHÍ / VẬN CHUYỂN** | cost_id, name, price, value_discount, value_extra, total_price, sale_max_percent, coefficient_cost_price (name = "Chi phí vận chuyển" ⇒ nhánh vận chuyển) |
| `account_details` + `account_detail_refs` | SỔ bút toán | ghi qua `AccountDetail::saveAccountDetail` (đã có ở HRM) |
| `service_accounting_requests*` | YC nguồn | entity HRM đã port: `ServiceAccountingRequest` + `...Cost` (+ items) |
| `firm_contract_costs` | bộ chi phí HĐ hãng | YC Phase 2 đã port write-back (`exported`) qua `syncCosts`/`rollbackAccounting` |

> **⚠️ Hình dạng bảng (đã kiểm 03/11) — quyết định khuôn BE:** `service_accounting` **KHÔNG có** cột
> `company_id` / `department_id` / `part_id` / `customer_id` / `customer_name`. Cột thật: `id, code,
> type, service_accounting_request_id, contractable_id, contractable_type, status, note, comment,
> approver_id, approved_at, created_by, updated_by, payed_cost, timestamps`. ⇒ Phiếu **cùng hình dạng
> với YC sibling** (`service_accounting_requests`), **KHÁC** phiếu HDDV (`wr_accounting_services` có
> cột org/customer trực tiếp). **Hệ quả khuôn port:**
> - **Scope + canView + searchByFilter** lấy khuôn **YC sibling** (`ServiceAccountingRequest`): org suy
>   từ `employee_create.info`, customer/VAT suy từ `contractable`=FirmContract (`whereHasMorph`), KHÔNG
>   lọc cột company_id trực tiếp. (Lọc "công ty/phòng ban" ở UI → ánh xạ qua employee_create.info.)
> - **Bút toán (accounting) + render + export + shell chi tiết read-only** lấy khuôn **phiếu HDDV**
>   (`WrAccountingService`): quan hệ `accounting()` hasMany + `journalRows()` cột phẳng + `JournalTable.vue`
>   + `DynamicExport` + shell `Form + SystemInfoSection + V2Footer`.
> - **Phân quyền:** giữ **3 cấp** theo ERP/§3 (tổng cty/cty/phòng ban) — bỏ cấp "bộ phận/part" mà YC có.

**invoiceable_type của phiếu** = chuỗi ERP `App\Model\Sale\ServiceAccounting` (quan hệ `accounting`
morphMany `invoiceable`). ⇒ **Phase 2** thêm hằng `INVOICEABLE_SERVICE_ACCOUNTING = 'App\\Model\\Sale\\ServiceAccounting'`
vào HRM `AccountDetail` để báo cáo công nợ (nếu đã port) nhận ra.
**contractable_type** HĐBH = `App\Model\Sale\Firm\Contract\FirmContract`.

---

## 3. Kiến trúc port — tận dụng hạ tầng SẴN CÓ

### Entity (`Modules/Finance/Entities/ServiceAccounting/`)
- `ServiceAccounting extends Model` (bảng ERP + boot hook công ty/phòng → **không** BaseModel; service
  tự gán `created_by`/`updated_by` ở mọi đường ghi). Hằng `DANG_TAO=1`, `DA_DUYET=2`; `DICH_VU/CHI_PHI/VAN_CHUYEN`.
  `STATUSES` trả chữ+màu (BE quyết: Đang tạo `#64748B` nháp · Đã duyệt `#16A34A`).
  Quan hệ: `service_accounting_request()`, `contractable()` morphTo, `approver()`, `items()`, `costs()`,
  `accounting()` morphMany AccountDetail orderBy(group,id).
  `searchByFilter` 3 cấp (mirror ERP) · `canView` mirror · `generateCode('HTDV')` (prefix `<cty>.HTDV.`).
  **Phase 2:** `canEdit`/`canDelete` = `created_by == auth()->id() && status == DANG_TAO`; `getDataForEdit`.
- `ServiceAccountingItem`, `ServiceAccountingCost` (bảng ERP, không BaseModel).

### Service (`Modules/Finance/Services/`)
- `ServiceAccountingService` — Phase 1: `list()` (searchByFilter + Resource), `getDataForShow()`
  (mirror ERP eager-load + đánh số nhóm bút toán + tính `vat_percent` theo `type` cho FirmContract),
  `exportRows()`. **Phase 2:** `store()`/`update()` (syncItems/syncCosts + nhánh duyệt), posting.
- **Phase 2 posting** — `store` khi `status=DA_DUYET` (scope FirmContract-only):
  - `contractable_type === FirmContract` → `FirmContractCostService::getDataCostAccounting($phieu)`.
    PLBS/HDDA_PLBS → lưu hạch toán về **HĐ gốc** (`parent_contract_id`).
  - **BỎ nhánh else** (`getDataCreateDept`): DB không có dòng ServiceContract/Contract ⇒ không port.
  - `AccountDetail::saveAccountDetail($data, $phieu->id, ServiceAccounting::class, $contractable_id, $contractable_type)`.
  - Lật `service_accounting_request.status = DA_HACH_TOAN(5)` + `approver/approved_at`; lật
    `service_export_request.status = DA_HACH_TOAN` (nếu có); `contractable->updateHandoverDate()`.
  - **SỬA bug ERP:** nếu `saveAccountDetail`/`getData...` trả false thì **rollback** (ERP `store`
    có nhánh `return responseErrors($message)` SAU khi đã làm việc khác mà **không** `DB::rollBack()` —
    port phải rollback). Không port `Log::error` lộ trace ra response.
  - **⚠️ Dependency Phase 2 (builder-check, đã kiểm HRM):** các mảnh sau **CHƯA có** ở HRM, phải port/
    xác minh khi mở Phase 2 — (1) `FirmContractCostService::getDataCostAccounting` (YC Phase 2 mới port
    write-back `syncCosts`/`rollbackAccounting`, **chưa có** hàm sinh bút toán này); (2) `FirmContract::
    updateHandoverDate()` (grep HRM: `updateHandoverDate` chỉ có ở `ProductExport(Request)Service`,
    `WrAccountingServiceService` — **không** trên entity FirmContract); (3) entity `ServiceExportRequest`
    (grep HRM: **không tìm thấy class** — bước lật PXK `Đã hạch toán` là optional/skip nếu HĐBH không
    gắn PXK); (4) cờ `accounted` trên item/cost nguồn (YC) để `syncItems/syncCosts` chặn copy khi đã
    hạch toán. **Phase 1 không đụng mục nào.**
- `ServiceAccountingNotifyService` — Phase 2, thông báo theo `NotificationMeta::build` (khi duyệt báo
  người lập YC — mirror ERP `NotificationHelper::sendNotify`).

### Resource
- `ServiceAccountingListResource` (list) · `ServiceAccountingShowResource` (chi tiết, gồm items/costs/
  accounting đã nhóm + contractable.link + customer).

### FE (`pages/finance/service-accounting/`)
- `index.vue` — list xem + export; 4 mixin chuẩn. **Cột:** STT · Mã phiếu (link) · Số hợp đồng ·
  Khách hàng · Tổng thanh toán · Người lập · Ngày duyệt · Trạng thái. **Phase 1: không cột Hành động**
  (Sửa/Xóa thuộc Phase 2).
- `_id/index.vue` — chi tiết: `V2BaseFormCard` Thông tin chung + khối Hạch toán (bảng bút toán) +
  3 bảng Dịch vụ/Chi phí khác/Vận chuyển; `SystemInfoSection` lịch sử; footer chỉ Quay lại.
- **Phase 2:** `create.vue` + `components/ServiceAccountingForm.vue` (dùng chung show/create readonly);
  nối nút tạo từ màn YC HĐBH; cột Hành động Sửa/Xóa (ẩn-hẳn khi không đủ điều kiện, theo quy ước HRM).
- Menu: nhóm "Dịch vụ" trong `subsystem-menu/finance.js` + `sale-hub.js`, ngay sau YC HĐBH.

### Quyền (type = Bán hàng, guard `api`, khai `PermissionsTableSeeder` — KHÔNG dùng lại quyền ERP web)
- `Xem phiếu hạch toán dịch vụ HĐBH - theo tổng công ty | công ty | phòng ban`
- **Phase 2:** `Hạch toán dịch vụ HĐBH` (tạo phiếu + ghi sổ). *(ERP gate `canView` theo quyền "Xem
  hạch toán dịch vụ theo …"; HRM tách tên riêng cho phiếu, không trùng tên quyền YC.)*

---

## 4. Danh sách & Lọc (mirror ERP `searchByFilter`)

- **Phạm vi:** `type=all` → 3 cấp (tổng cty / công ty = `Company::getMembers` / phòng ban =
  `Department::getMembers` / else chính mình); thêm điều kiện: thấy phiếu `status != Đang tạo`
  **hoặc** phiếu `Đang tạo` do chính mình lập. `type != all` → chỉ phiếu của mình.
- **Bộ lọc:** `startDate`/`endDate` (created_at), `code` (like), `status`, `company`, `department`,
  `contract_code` (whereHasMorph code), `customer` (whereHasMorph customer_id), `cost` (whereHas costs.cost_id),
  `money_from`/`money_to` (payed_cost). Mặc định `orderBy created_at DESC`.
- **Export** (`getDataForExport`, 9 cột): STT · Ngày lập · Mã · Số hợp đồng · Khách hàng ·
  Tổng thanh toán · Người lập · Ngày duyệt · Trạng thái. HRM dùng khuôn export-rows + số **chuẩn quốc tế**.

## 5. Chi tiết

- **Eager-load (bám khuôn phiếu HDDV, KHÔNG bê nguyên eager-load ERP):** `contractable.customer.
  deputies`, `items`, `costs.cost`, `service_accounting_request`, `employee_create.info`, và
  `accounting.account`. ⚠️ ERP eager-load sâu `accounting.(refs|customer|employee.info|product|
  obj_department|obj_part|work|service_accounting_item|service_accounting_cost)` — các quan hệ này
  **chưa chắc có trên `AccountDetail` của HRM**; phiếu HDDV anh em render bút toán từ **cột phẳng**
  trên `account_details` (chỉ cần `accounting.account` cho tên TK). ⇒ **Theo khuôn HDDV**: render
  bảng bút toán từ cột phẳng, eager-load tối thiểu `accounting.account`; quan hệ nào thực sự cần sẽ
  xác minh **lúc build** theo cột có thật, không giả định.
- Đánh `group_number` tăng dần theo `group` (mirror ERP).
- **`vat_percent` (FirmContract, theo `type`):** Dịch vụ→`revenue_costs[0].vat_percent` · Chi phí→
  `costs[0].vat_percent` · Vận chuyển→`delivery_vat_percent` (`revenue_costs = costs`). ⚠️ **fallback 0**
  khi mảng rỗng / cột vắng; **xác minh tên cột VAT trên `firm_contracts` / `firm_contract_costs` lúc
  build** (đã thấy có nhóm `total_*_vat`, `delivery_before_vat` — chưa chốt chính xác `delivery_vat_percent`).
- **Lịch sử (`SystemInfoSection`):** theo **khuôn phiếu HDDV** (created/updated/approved). Không phát minh format mới.

---

## 6. Quyết định đã chốt

1. **Phân kỳ:** Phase 1 **chỉ-đọc** trước (list + chi tiết + export + lịch sử), có **checkpoint số
   liệu** trước khi làm Phase 2 ghi sổ. *(user chốt 03/11)*
2. **Đường tạo (Phase 2):** **y hệt ERP** — phiếu sinh **từ YC hạch toán DV** (`service_accounting_request_id`
   bắt buộc), copy contractable + items + costs từ YC. Không tạo tay từ HĐ. *(user chốt 03/11)*
3. **Sửa/Xóa (Phase 2):** **theo ERP** — `canEdit`/`canDelete` = người lập **và** `status = Đang tạo`.
   Đã duyệt (đã hạch toán) → khóa cứng, chặn ở BE (423/404 như ERP trả `not_found`). *(user chốt 03/11)*
   - **Lệch chủ ý với phiếu HDDV** (immutable) — **user ĐÃ xác nhận chấp nhận** (03/11): giữ Sửa/Xóa
     cho phiếu HĐBH đúng ERP, dù phiếu HDDV immutable. (Thực tế DB hiện 0 phiếu "Đang tạo" ⇒ nút gần
     như không bật với data thật, nhưng vẫn làm đúng ERP.)
4. **Trạng thái:** 2 mức (Đang tạo / Đã duyệt), giữ nháp — khác phiếu HDDV (1 mức).
5. **Vị trí tài liệu:** top-level `.plans/phieu-hach-toan-dich-vu-hdbh/` (song song phiếu HDDV) — *quyết định của Claude*.
6. **Export/In:** có Export (khuôn export-rows), **không có In** (ERP không có print cho màn này).
7. **Scope `contractable` = FirmContract-only** *(quyết định Claude, dữ kiện DB 1275/1275)* — query
   lọc `contractable_type`, null-guard, bỏ nhánh else `getDataCreateDept`. Bảng Dịch vụ (items) rỗng
   với data hiện có (items=0 dòng) nhưng vẫn render; dữ liệu thực ở bảng costs.
8. **Bút toán render + eager-load** theo **khuôn phiếu HDDV** (cột phẳng, `accounting.account`), không
   bê eager-load sâu của ERP *(quyết định Claude — builder-check)*. VAT fallback 0, xác minh cột lúc build.

## 7. User đã chốt (sau builder-check, 03/11)

1. **Sửa/Xóa lệch phiếu HDDV** → **CHẤP NHẬN** — phiếu HĐBH **có** Sửa/Xóa (Đang tạo + người lập)
   đúng ERP, dù phiếu HDDV immutable.
2. **Nhánh** → **nhánh feature riêng** tách từ `develop` cho cả hrm-api + hrm-client (merge về develop
   sau), ERP chỉ đọc DB gộp, không migration.

→ Không còn câu hỏi mở. Doc sẵn sàng để duyệt.

## 8. Non-goals / Anti-goals
- **Non-goal:** port `exportList` server-side ERP; màn HĐ hãng đích (nếu chưa có ở HRM).
- **Anti-goal:** đổi công thức bút toán khác ERP mà không chốt số liệu (giữ trung thành, bug ERP giữ
  nguyên trừ chỗ rollback đã nêu §3); dùng lại quyền ERP guard web; tạo migration mới.
