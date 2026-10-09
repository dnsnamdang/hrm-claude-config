# YCXH — Loại "Xuất thực hiện hợp đồng" (type 19)

**Người phụ trách:** @namdangit
**Nhánh:** `gop_db` (cả `hrm-api` và `hrm-client`)
**Ngày:** 2026-10-06
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-10-06-ycxh-xuat-thuc-hien-hop-dong-type19-design.md`

Màn: HRM **Tạo yêu cầu xuất hàng** (`/finance/product-export-requests/create`).
Tiếp nối đợt loại 14 (`ycxh-xuat-ban-hang-type14`) — mục D ghi "Loại 4/16/17/19 còn lại — các đợt sau".

## Bối cảnh / Sự cố

Trên **ERP**, màn Tạo YCXH chọn **Loại = "Xuất thực hiện hợp đồng"** sẽ hiện ô
**"Chọn hợp đồng / đơn hàng (*)"** (modal tìm HĐ bán của khách). Trên **HRM**, loại 19 vẫn hiện
trong dropdown (`DROPDOWN_TYPE_IDS` có 19) nhưng:

- Không rơi vào nhánh FE nào (`CONTRACT_TYPES=[20,21]`, `FIRM_CONTRACT_TYPES=[14]`,
  `MANUAL_TYPES=[3,6,12,18,99]`) → **không có ô chọn hợp đồng, không có bảng hàng**.
- `CREATABLE_TYPE_IDS` **chưa có 19** → bấm lưu bị chặn 422 "Loại yêu cầu không được phép tạo."

→ Loại 19 chưa dựng luồng tạo. Đây là **port tiếp tính năng**, không phải bug ngẫu nhiên.

## Nghiệp vụ loại 19 (chuẩn theo ERP)

Khác hẳn loại 14/20/21 (tự nạp dòng hàng từ hợp đồng):

- Hợp đồng chỉ cung cấp **khách hàng + địa chỉ giao + tham chiếu HĐ** (snapshot).
- **KHÔNG auto-load dòng hàng** — người dùng **nhập tay** bảng hàng (giống loại 3/6/12/18/99).
- Nguồn chọn HĐ là **UNION các hợp đồng bán phía khách hàng** (không phải `hrm_contracts`).

### Nguồn hợp đồng — ERP `SearchContractService::searchEmplementAllContract()` (:547-617)

UNION các query (ERP, đã đọc nguyên văn):

| Nguồn | Bảng | Loại (`type`) | Trạng thái (`status`) | Lọc thêm |
| --- | --- | --- | --- | --- |
| HĐ Vật tư-Hàng hoá-Thiết bị | `firm_contracts` | 1 (`HOP_DONG`) | IN (3,6,7,8,9,10) | `whereNull('is_zt')` |
| HĐ dự án | `firm_contracts` | 4 (`HOP_DONG_DU_AN`) | IN (3,6,7,8,9,10) | `whereNull('is_zt')` |
| Đơn hàng nguyên tắc | `firm_contracts` | 8 (`DON_HANG_NGUYEN_TAC`) | IN (3,6,7,8,9,10) | `whereNull('is_zt')` |
| HĐ Sửa chữa-Bảo dưỡng-Bảo trì | `wr_service_contracts` | 1 (`HOP_DONG`) | IN (3,4,6) | — |

- **KHÔNG lọc công ty** — `elementExtrated()` (:621-640) chỉ lọc `code` / `created_by` / `customer`,
  không có `company_id`. User chốt: **"cứ theo erp trước"** (không thêm bộ lọc công ty).
- ERP có thêm `firm_contract_principle_medical` nhưng query **y hệt** `firm_contract_principle`
  (cùng `DON_HANG_NGUYEN_TAC`/type 8) → trong HRM gộp thành **1 query type 8** để tránh nhân đôi dòng.
- Sắp `created_at` desc.

### Khác biệt với scaffold HRM hiện có (QUYẾT ĐỊNH user chốt)

Scaffold HRM đang đấu loại 19 vào **`hrm_contracts`** (validate `exists:hrm_contracts,id`, service
dùng `Contract::find`, `emplement_contract_type = Contract::class`). **User chốt: thay bằng UNION
ERP** (`firm_contracts` + `wr_service_contracts`) — trích: **"đúng rồi làm theo erp"**.

## Hướng giải quyết

### BE (hrm-api)

1. **Mở `store()` cho loại 19** — thêm `XUAT_THUC_HIEN_HD` (19) vào `CREATABLE_TYPE_IDS`
   (`ProductExportRequest.php:73-83`).
2. **Endpoint tìm HĐ union** — route tĩnh mới (cạnh `/firm-contracts` :708), method mới trong
   `ProductExportRequestController` (mô phỏng `firmContracts()`), build UNION 2 bảng theo bảng trên,
   **không lọc công ty**, trả `items[]` gồm `id, code, customer_name, customer_address` +
   **`source` discriminator** (`firm` | `wr`) để FE/BE biết gắn model nào.
3. **Hằng loại/trạng thái "emplement" cho 2 Entity** (tách khỏi bộ bill_adjust vì status set khác):
   - `FirmContract`: thêm `EMPLEMENT_STATUSES = [3,6,7,8,9,10]`, tái dùng `SELECTABLE_TYPES=[1,4,8]`
     (đã có, trùng đúng nhu cầu) + điều kiện `whereNull('is_zt')`.
   - `WrServiceContract`: thêm `EMPLEMENT_TYPE = 1`, `EMPLEMENT_STATUSES = [3,4,6]`.
4. **Sửa `rulesForType()` nhánh 19 (:696-699)** — bỏ `exists:hrm_contracts,id`. Vì HĐ có thể ở 1
   trong 2 bảng, validate `emplement_contract_id` là `integer` + tồn tại theo `source`:
   nhận thêm `emplement_contract_type` (`firm`|`wr`) và kiểm `exists` đúng bảng tương ứng
   (`required` khi gửi duyệt, `nullable` khi nháp — giữ hành vi hiện tại).
5. **Sửa `createManual()` nhánh 19 (:322-352)** — resolve model động theo `source`:
   - `firm` → `FirmContract::find` → `emplement_contract_type = FirmContract::class`.
   - `wr` → `WrServiceContract::find` → `emplement_contract_type = WrServiceContract::class`.
   - Snapshot KH từ model: `customer_id/customer_name/customer_address/customer_contact_name`.
     ⚠️ Cột điện thoại liên hệ khác tên giữa 2 bảng — `firm_contracts.customer_contact_phone` (số ít)
     vs `wr_service_contracts.customer_contact_phones` (số nhiều) → đọc null-safe theo từng model.
   - Dòng hàng vẫn `insertManualLines` (nhập tay), KHÔNG auto-load.

### FE (hrm-client) — `ProductExportRequestForm.vue`

1. Thêm `EMPLEMENT_CONTRACT_TYPES = [19]` + computed `isEmplementContractType`.
2. Hiện **khối chọn hợp đồng** cho loại 19 (ô "Chọn hợp đồng / đơn hàng (*)" + tên HĐ đã chọn,
   mirror khối loại 14/20/21) nhưng **giữ bảng hàng nhập tay** (`QuotationProductSearchModal` +
   bảng như `MANUAL_TYPES`).
3. Modal tìm HĐ union: **copy `FirmContractSearchModal.vue`** → `EmplementContractSearchModal.vue`,
   đổi endpoint sang route union mới; mỗi item nhớ `source` để submit.
4. Submit gửi `emplement_contract_id` + `emplement_contract_type` (`firm`|`wr`) + bảng hàng nhập tay.
5. Snapshot KH (tên/địa chỉ) hiển thị **chỉ đọc** sau khi chọn HĐ (như ERP).

## Quyết định đã chốt

- Nguồn chọn HĐ = **UNION ERP** `firm_contracts`[type 1,4,8; status 3,6,7,8,9,10; `is_zt` null] +
  `wr_service_contracts`[type 1; status 3,4,6] — **KHÔNG lọc công ty** ("cứ theo erp trước").
- Thay scaffold `hrm_contracts` bằng union ("đúng rồi làm theo erp").
- Loại 19 **nhập tay dòng hàng**, HĐ chỉ cho KH + địa chỉ + tham chiếu (không auto-load).
- Gộp DB — ghi thẳng bảng ERP sẵn có, KHÔNG tạo bảng/migration mới.
- Gộp `firm_contract_principle_medical` vào 1 query type 8 (bỏ dòng nhân đôi của ERP).

## Không làm trong đợt này

- Loại 4/16/17 còn lại của Hướng B (các đợt sau).
- Bộ lọc công ty trên picker (theo ERP: không có).
- Các business-check nâng cao (hạn mức công nợ, lệch giá…) — loại 19 nhập tay nên không áp.

## Verify

- `php -l` sạch các file BE sửa.
- Playwright tại `http://127.0.0.1:3000`:
  1. Chọn loại 19 → hiện ô "Chọn hợp đồng / đơn hàng" + bảng hàng nhập tay.
  2. Modal tìm HĐ trả cả HĐ hãng (firm) lẫn HĐ SC-BD (wr), đúng bộ lọc trạng thái/loại,
     không lọc theo công ty.
  3. Chọn HĐ → snapshot KH + địa chỉ hiển thị chỉ đọc; nhập tay ≥1 dòng hàng.
  4. Lưu nháp: chỉ cần chọn loại. Gửi duyệt: bắt buộc HĐ + ≥1 dòng hàng.
  5. Phiếu tạo xong lưu đúng `emplement_contract_type` = FirmContract/WrServiceContract theo nguồn.
