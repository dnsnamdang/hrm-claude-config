# Lập hợp đồng ERP từ báo giá HRM (bỏ qua firm-quotation)

- **Ngày**: 2026-06-15
- **Loại**: Cross-system HRM (Module Assign) → ERP (TanPhatDev). Feature lớn, 3 phase.
- **Cặp tài liệu**: HRM ở `HRM/.plans/hrm-quotation-to-erp-contract/`.

## 1. Mục tiêu

Cho phép **lập hợp đồng bán (firm_contract) bên ERP trực tiếp từ báo giá module Assign bên HRM** — KHÔNG đồng bộ báo giá thành `firm_quotation` ERP nữa. Chỉ áp dụng báo giá HRM:
- Đã **trúng thầu** (`quotations.status = 7`),
- Đã **đồng bộ hết hàng tạm** sang ERP (`tmp_sync_status = 'synced'` — mọi dòng `quotation_product_prices` có `erp_product_id`),
- **Tiền tệ = VND** (ngoại tệ xử lý sau, ngoài phạm vi).

## 2. Quyết định đã chốt (brainstorming)

| # | Quyết định |
|---|---|
| 1 | KHÔNG tạo `firm_quotation` ERP. Lập HĐ thẳng từ báo giá HRM. |
| 2 | **1 cơ chế, 2 cửa vào**: dùng form "Lập hợp đồng" sẵn có của ERP; báo giá HRM chỉ **prefill** KH + sản phẩm + tiền; NV ERP nhập nốt các trường chỉ-ERP (người ký, chức danh, TK công ty, template, kiểu in, lịch thanh toán, cài đặt/xuất hóa đơn) rồi lưu như luồng thường. |
| 3 | Cửa vào 1: popup "chọn báo giá" trong màn tạo HĐ ERP thêm nguồn **"Báo giá HRM"**. Cửa vào 2: nút bên HRM deep-link sang URL màn tạo HĐ ERP, preselect báo giá. |
| 4 | **(CẬP NHẬT 2026-06-15) ERP lấy dữ liệu báo giá HRM qua API HTTP** (không đọc DB trực tiếp nữa). ERP `HrmApiService` gọi 3 endpoint HRM: `GET /api/v1/assign/quotations/erp-contract/eligible`, `GET .../{id}`, `POST .../{id}/mark`. **Tạm KHÔNG xác thực** (ERP↔HRM chưa có cơ chế auth — bổ sung sau). Ghi ngược cũng qua API (`/mark`). Config ERP: `services.hrm.base_url` (env `HRM_API_BASE_URL`). |
| 5 | Khớp khách hàng: resolve `customers.id` ERP theo `customer_code` → fallback `customer_tax_code` (KHÔNG dùng `customer_id` vì là snapshot). |
| 6 | Sản phẩm: `quotation_product_prices.erp_product_id` chính là `product_id` thật ERP → đẩy vào **1 tab mặc định** của HĐ. |
| 7 | Schema: thêm `firm_contracts.hrm_quotation_id` (nullable), `firm_quotation_id` → nullable. |
| 8 | **Chống lập trùng**: lập HĐ xong ghi ngược về HRM (cột `quotations.erp_firm_contract_id`); báo giá đã có HĐ bị **ẩn** khỏi popup ERP + **ẩn** nút bên HRM. |
| 9 | Làm **cả 3 phase** trong feature này. |

## 3. Hiện trạng đã khảo sát

### HRM (nguồn)
- `Modules/Assign/Entities/Quotation.php`, bảng `quotations`: `STATUS_TRUNG_THAU = 7`; cột `customer_code`, `customer_tax_code`, `customer_name`, `currency_id`, `total_after_vat`, `tmp_sync_status` ('synced' khi hết hàng tạm), `erp_firm_quotation_id`.
- Dòng SP: `quotation_product_prices` — `erp_product_id` (≠null = hàng thật ERP), `code`, `name`, `quoted_price`, `vat_percent`, SL.
- "Đã đồng bộ hết hàng tạm" = `tmp_sync_status='synced'` (hoặc mọi dòng có `erp_product_id`).
- Tiền: `quotations.currency_id` → join bảng HRM `currencies` lọc code = 'VND'.

### ERP (đích)
- Hợp đồng: `app/Model/Sale/Firm/Contract/FirmContract.php`, bảng `firm_contracts`. Cột liên kết hiện tại `firm_quotation_id`. Status: `DANG_TAO=1`, `CHO_DUYET=2`, ...
- Tạo HĐ: `FirmContractController::store()` + `FirmContractService` (`saveFirmContractData`) — hiện **bắt buộc** `firm_quotation_id`, gọi `quotation->canCreateContract()`, copy tabs/cost từ `firm_quotation`, cuối cùng set `firm_quotation.status = DA_LAP_HD`.
- Validation: `FirmContractStoreRequest` bắt buộc `firm_quotation_id`, `tabs.*.firm_quotation_tab_id`, `signer_id`, `signer_role_id`, `company_account_id`, `template`, `contract_type_print`, `need_install`, `has_invoice`, `customer_id`, `code_input`, `identity_card_number`.
- Chi tiết SP HĐ: `firm_contract_tab_products` (`product_id` = Product thật). Báo giá ERP: `firm_quotation_tab_products` (`product_id`/`tmp_product_id`).
- API tích hợp HRM↔ERP: prefix `v1/admin/`, middleware `check.api.key` (header `x-api-key`). ERP đã có controller `CRM/Sale/FirmQuotationController` + `FirmContractController` cho API.
- Connection `hrm` đọc thẳng DB HRM (`config/database.php`).

## 4. Thiết kế 3 phase

### Phase 1 — ERP Backend
1. **`app/Services/Hrm/HrmQuotationReader.php`** (mới, theo pattern `CustomerScopeReader`): 
   - `searchEligible($filters)`: query connection `hrm` `quotations` join `currencies` — lọc `status=7`, `tmp_sync_status='synced'`, `currencies.code='VND'`, **chưa có** `erp_firm_contract_id`. Trả list: id, code, customer_name, customer_code, total_after_vat, ngày.
   - `getForContract($hrmQuotationId)`: trả KH (code/tax_code → resolve `customers.id` ERP) + danh sách SP (`erp_product_id` → product_id, name, code, quantity, price, vat_percent). Validate mọi dòng có `erp_product_id` (nếu thiếu → lỗi).
2. **Migration `firm_contracts`**: thêm `hrm_quotation_id unsignedBigInteger nullable`; đổi `firm_quotation_id` → nullable.
3. **Migration/HRM**: thêm `quotations.erp_firm_contract_id unsignedBigInteger nullable` (qua connection `hrm` — tạo migration ở HRM repo, xem cặp HRM).
4. **Nới `FirmContractStoreRequest`**: khi có `hrm_quotation_id` → `firm_quotation_id` & `tabs.*.firm_quotation_tab_id` không bắt buộc; thêm validate `hrm_quotation_id`. Các trường chỉ-ERP vẫn bắt buộc.
5. **Nới `FirmContractService::saveFirmContractData()`**: nhánh nguồn HRM:
   - Bỏ `canCreateContract()` của firm_quotation; thay bằng kiểm tra báo giá HRM hợp lệ (status/tmp/VND/chưa có HĐ) qua `HrmQuotationReader`.
   - Tạo **1 tab mặc định** chứa SP từ báo giá HRM (product_id = erp_product_id) thay vì copy từ `firm_quotation_tab`.
   - KHÔNG set `firm_quotation.status`. Lưu `firm_contracts.hrm_quotation_id`.
   - Sau commit: **ghi ngược** `quotations.erp_firm_contract_id = <contract id>` qua connection `hrm`.
6. **Endpoint FE** (web, dùng trong màn tạo HĐ): 
   - `GET firm-contracts/hrm-quotations/searchData` → list báo giá HRM đủ điều kiện (DataTable).
   - `GET firm-contracts/hrm-quotations/{id}/getDataForContract` → prefill KH + SP.

> **Cần khảo sát khi lập plan**: cấu trúc payload `tabs/groups/revenue_costs/costs/contract_process_payments/...` mà `store()` yêu cầu — xác định field nào bắt buộc cho nguồn HRM, field nào để trống/NV ERP nhập; cách `saveFirmContractData` build tab/product để chèn nhánh HRM tối thiểu xâm lấn.

### Phase 2 — ERP Frontend (màn tạo hợp đồng)
- Popup "chọn báo giá": thêm tab/nguồn **"Báo giá HRM"** — DataTable từ `hrm-quotations/searchData`. Chọn 1 dòng → gọi `getDataForContract` → prefill: khách hàng (đã resolve `customer_id`), bảng sản phẩm (1 tab, product thật + SL/giá/VAT). NV ERP nhập nốt người ký/template/lịch TT... rồi lưu.
- Đọc `?hrm_quotation_id=` trên URL → tự mở popup/preselect báo giá HRM đó (phục vụ deep-link).
- Gửi `hrm_quotation_id` trong payload khi lưu HĐ.

### Phase 3 — HRM Frontend
- Trên màn báo giá Assign (tab Báo giá của dự án / `ProspectiveProjectQuotationsTab.vue`): với báo giá `status=7` + `tmp_sync_status='synced'` + VND + **chưa có** `erp_firm_contract_id` → hiện nút **"Lập hợp đồng ERP"**.
- Nút mở tab mới URL ERP: `{ERP_BASE}/admin/sale/firm-contracts/create?hrm_quotation_id={id}` (base ERP từ config HRM).
- Báo giá đã có `erp_firm_contract_id` → ẩn nút (đã lập HĐ).

## 5. Luồng tổng quát

```
[HRM] Báo giá trúng thầu (7) + tmp_sync_status=synced + VND + chưa có HĐ
   ├─(cửa A) NV ERP mở màn tạo HĐ → popup chọn báo giá → tab "Báo giá HRM" → chọn
   └─(cửa B) NV HRM bấm "Lập hợp đồng ERP" → deep-link sang màn tạo HĐ ERP (preselect)
        → ERP prefill KH + sản phẩm (product thật) vào 1 tab
        → NV ERP nhập người ký/template/lịch TT... → Lưu
        → ERP tạo firm_contract (hrm_quotation_id set, firm_quotation_id null)
        → ghi ngược HRM quotations.erp_firm_contract_id
        → báo giá ẩn khỏi popup ERP + ẩn nút HRM (chống trùng)
```

## 6. Edge case / rủi ro

- Không resolve được KH ERP (code & tax_code đều không khớp) → báo lỗi rõ, chặn lập HĐ.
- Báo giá còn dòng `erp_product_id` null (chưa sync hết) → không đủ điều kiện, không xuất hiện.
- Báo giá đã có `erp_firm_contract_id` → loại khỏi danh sách + ẩn nút.
- Báo giá ngoại tệ → loại (ngoài phạm vi).
- HĐ ERP lập lỗi giữa chừng → rollback, KHÔNG ghi ngược HRM.
- Ghi ngược HRM lỗi sau khi HĐ đã commit → cần log + cơ chế bù (xác định khi lập plan; tối thiểu log để xử lý tay).

## 7. Phạm vi

- ✅ ERP BE (service đọc HRM, migration, nới store/request, 2 endpoint), ERP FE (popup + prefill + deep-link), HRM (migration `erp_firm_contract_id`, nút FE).
- ❌ KHÔNG bật lại firm-quotation sync. KHÔNG xử lý báo giá ngoại tệ. KHÔNG tự hoàn thiện các trường chỉ-ERP (NV ERP nhập).

## 8. Test (tổng quát)

1. Báo giá HRM đủ điều kiện (7 + synced + VND) hiện trong popup "Báo giá HRM" của màn tạo HĐ ERP.
2. Chọn → prefill đúng KH (resolve theo code/tax_code) + đủ sản phẩm (product thật).
3. NV ERP nhập nốt → lưu → HĐ tạo thành công, `hrm_quotation_id` set, `firm_quotation_id` null.
4. Ghi ngược HRM: `quotations.erp_firm_contract_id` được set.
5. Báo giá đã lập HĐ → biến mất khỏi popup + nút HRM ẩn.
6. Deep-link từ HRM (`?hrm_quotation_id=`) → màn tạo HĐ ERP tự preselect đúng báo giá.
7. Báo giá thiếu điều kiện (chưa synced / ngoại tệ / không resolve được KH) → không lập được, báo lỗi/loại khỏi danh sách.
