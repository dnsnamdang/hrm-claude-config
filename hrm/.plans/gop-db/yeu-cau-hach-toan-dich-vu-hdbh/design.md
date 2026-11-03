# Port màn "Yêu cầu hạch toán dịch vụ — HĐBH" ERP → HRM (CHỈ-ĐỌC Phase 1)

> Nguồn nghiệp vụ: ERP `serviceAccountingRequest` (`App\Model\Sale\ServiceAccountingRequest`,
> controller `app/Http/Controllers/Sale/ServiceAccountingRequestController.php`, view
> `resources/views/sale/service_accounting_requests/`).
> Khuôn UI/kiến trúc HRM: màn song sinh **HDDV** đã port — `wr-accounting-service-requests`
> (entity `Modules/Finance/Entities/WrAccountingServiceRequest`, xem [[hrm-phieu-hach-toan-dich-vu-hddv-port-done]]).

## 1. Ý định & bối cảnh

Màn ERP "Yêu cầu hạch toán làm dịch vụ" (route `serviceAccountingRequest`) là phiếu **YÊU CẦU** kế toán
hạch toán phần **làm dịch vụ** gắn với hợp đồng **BÁN** (HĐBH). Kế toán duyệt rồi lập tiếp phiếu
**Hạch toán dịch vụ** (`serviceAccounting`, màn #2 — ghi sổ). Đây là 1 trong 2 cặp màn hạch toán dịch vụ:

| Cặp | Màn 1 (yêu cầu) | Màn 2 (ghi sổ) | HĐ nguồn |
|---|---|---|---|
| **HDDV** (CSKH, phía chăm sóc) | `wr-accounting-service-requests` ✅ ĐÃ PORT | `wr-accounting-services` ✅ ĐÃ PORT | `WrServiceContract` |
| **HĐBH** (bán hàng) | `serviceAccountingRequest` ⬅ **MÀN NÀY** | `serviceAccounting` ❌ chưa port | `FirmContract` (+3 loại khác) |

## 2. Quyết định scope (call của tôi — user "làm đi", bỏ qua brainstorming)

**Phase 1 = PORT CHỈ-ĐỌC**: entity + danh sách + chi tiết + Xuất Excel. Lý do giống tiền lệ HDDV (hoãn
đường service) và BGHLVC (port chỉ-đọc):

- ERP `contractable` là morphTo 4 loại HĐ (ServiceContract / Contract / FirmContract / ProjectContract),
  nhưng **100% dữ liệu thật (1303 phiếu) nối `FirmContract`**. HRM chỉ có `FirmContract` read-model MỎNG
  (`Modules/Finance/Entities/Contract/FirmContract.php`), **KHÔNG** có bộ nạp chi phí HĐ hãng
  (`getDataForServiceExport`, `FirmContractCost`, quan hệ costs/revenue_costs). → không dựng được
  form TẠO/SỬA (vốn phải nạp chi phí sống từ HĐ).
- Điểm vào tạo phiếu ở ERP là **từ màn HĐ hãng** (prefill `?firm_contract=<id>`) — màn HĐ hãng chưa port.
- Nút "Hạch toán dịch vụ" ở chi tiết dẫn sang **phiếu #2** (`serviceAccounting`) — chưa port.

**HOÃN sang phase sau**: Tạo/Sửa/Xóa, `reject()` (Không duyệt), nút "Hạch toán dịch vụ".
Các phase đó cần port trước bộ chi phí HĐ hãng.

## 3. Phát hiện then chốt — SHOW tự chứa từ snapshot của phiếu

ERP `getDataForShow()` (model :365-424) build **cả `costs` LẪN `revenue_costs` ĐỀU TỪ `$object->costs`** —
tức bảng snapshot `service_accounting_request_costs` của CHÍNH phiếu, KHÔNG phải chi phí sống của HĐ:

```php
$revenue_costs = $object->costs->map(...);   // từ snapshot phiếu
'revenue_costs' => $revenue_costs,
'costs'         => $revenue_costs,            // CÙNG nguồn
```

→ Màn chi tiết HRM đọc thẳng `service_accounting_request_costs`, **không cần** quan hệ chi phí FirmContract.
Chỉ `vat_percent` (ERP lấy từ HĐ, :387-394) là cần HĐ — nhưng **suy được từ chính phiếu**:
`payed_cost = Σ(total_price) × 1.08` nhất quán toàn bộ dữ liệu ⇒ VAT 8%, tính
`vat = payed_cost − Σ(total_price)`, `vat_percent = round(payed_cost/Σtotal_price − 1)×100`.

## 4. Dữ liệu (DB gộp local `erp_hrm_check`, đọc chỉ-đọc)

- `service_accounting_requests` (1303 dòng): id, code(UNI), **type**(1 Dịch vụ / 2 Chi phí khác /
  3 Chi phí vận chuyển), service_export_request_id, **contractable_id**, status, note, comment,
  approver_id, approved_at, created_by, updated_by, created_at, updated_at, **contractable_type**,
  **payed_cost**(16,2). ⚠️ **KHÔNG có** company_id/department_id/part_id/customer_id/customer_name.
  - status: 5=1275, 2=17, 3=7, 1=4. type: 3=975, 1=239, 2=89.
  - contractable_type = **100% `App\Model\Sale\Firm\Contract\FirmContract`** (chuỗi FQN ERP).
    morphMap HRM (`FinanceServiceProvider::registerMorphMap` :63) đã map chuỗi này → HRM FirmContract
    → **morphTo resolve được**.
- `service_accounting_request_costs` (1417 dòng): id, service_accounting_request_id,
  service_export_request_cost_id, contract_costable_id, cost_id, **name, price, value_discount,
  value_extra, total_price**, sale_max_percent, coefficient_cost_price, contract_costable_type
  (=`...\FirmContractCost`, KHÔNG map — không cần resolve). KHÔNG có cột vat.
- `service_accounting_request_items`: **0 dòng** (không dùng — bỏ hẳn, "Gói dịch vụ" luôn trống).
- `firm_contracts`: có code, customer_id, customer_name, customer_type, customer_address,
  customer_mobile, created_by, delivery_vat_percent... (đủ cho hiển thị).
- `employee_infos`: có company_id, department_id, part_id. `customers`: có code, fullname, short_name.

## 5. Nghiệp vụ port từ ERP

### 5.1 Danh sách (controller `searchData` + `searchByFilter`)
Cột (đổi nhãn theo HRM "Người tạo/Ngày tạo"): STT · Ngày tạo · **Mã phiếu**(nuxt-link) ·
Số hợp đồng(mã FirmContract, KHÔNG link — màn HĐ chưa port) · Kinh doanh(người lập HĐ =
FirmContract.created_by→tên NV) · Khách hàng(mã-tên) · Tổng thanh toán(payed_cost) · Người tạo ·
Người duyệt · Ngày duyệt · Trạng thái · Hành động(**chỉ Lịch sử** — Phase 1 không có Sửa/Xóa/Hạch toán).

### 5.2 Phạm vi (type=all) — scope theo INFO NGƯỜI TẠO (bảng thiếu cột org!)
ERP `searchByFilter` :190-212 scope qua `whereHas('employee_create.info', ...)`:
- `Xem ... tổng công ty` / Super Admin → mọi phiếu.
- `Xem ... công ty` → info.company_id == người đăng nhập.company_id.
- `Xem ... phòng ban` → info.department_id (HRM: dùng `manageableDepartmentIds` — rộng hơn, quy ước Tài chính).
- `Xem ... bộ phận` → info.part_id == người đăng nhập.part_id.
- không quyền nào → created_by = mình.
- PLUS: `status != DANG_TAO OR created_by = mình` (phiếu nháp chỉ người tạo thấy).

### 5.3 Bộ lọc (ERP form filter)
keyword(mã/số HĐ/tên KH) · code · contract_code · status · customer · created_by(Người tạo) ·
request_by(Người yêu cầu = người lập HĐ, `whereHasMorph contractable.created_by`) · approver_id(Người duyệt)
· company_id(chỉ big boss) + department_id (org HRM) · start_date/end_date.

### 5.4 Chi tiết (show)
Thông tin chung: Kiểu hạch toán(type) · Số hợp đồng(mã, không link) · Khách hàng(mã/tên/địa chỉ/đt từ
FirmContract) · Ghi chú · Người tạo · Người duyệt · Ngày duyệt · Ghi chú duyệt(comment).
Bảng chi phí (1 tab theo type): cột **Chi phí/Dịch vụ · Giá niêm yết(price) · Doanh số vượt
trội(value_extra) · Giảm giá(value_discount) · Giá trị sau giảm giá(total_price)**. Footer: Tổng
trước thuế(Σtotal_price) · VAT(payed_cost−Σ) · Tổng thanh toán(payed_cost).
Nút: **chỉ Quay lại + Lịch sử** (Không duyệt/Hạch toán HOÃN).

## 6. Quyền (mới, guard `api`, khai `PermissionsTableSeeder` chung)
4 quyền xem (bám ERP 4 cấp) + (HOÃN) quyền Hạch toán:
- `Xem yêu cầu hạch toán dịch vụ HĐBH - theo tổng công ty`
- `Xem yêu cầu hạch toán dịch vụ HĐBH - theo công ty`
- `Xem yêu cầu hạch toán dịch vụ HĐBH - theo phòng ban`
- `Xem yêu cầu hạch toán dịch vụ HĐBH - theo bộ phận`

`type` quyền = `permissionType` phân hệ **Bán hàng** (màn nằm ở Bán hàng như HDDV). Chưa khai quyền
Hạch toán (đi cùng phase ghi).

## 7. Phân hệ & menu
Phân hệ chính **Bán hàng** (ERP đặt ở "Dịch vụ" + "Hàng hoá-Dịch vụ-Vận chuyển → Bán Dịch vụ", link
`?type=all`). Mục menu HRM: thêm vào cây Bán hàng (`sale-hub.js` / subsystem-menu) cạnh HDDV.
Route HRM: `/finance/service-accounting-requests` (module Finance như HDDV).

## 8. Deferred (phase sau)
Tạo/Sửa/Xóa phiếu · reject (Không duyệt) · nút "Hạch toán dịch vụ" → phiếu #2 `serviceAccounting` ·
link màn HĐ hãng. Tất cả phụ thuộc bộ chi phí HĐ hãng (`FirmContractCost` + `getDataForServiceExport`)
chưa port sang HRM.
