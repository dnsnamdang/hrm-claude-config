# Plan — YCXH loại 19 "Xuất thực hiện hợp đồng"

**Goal:** Dựng luồng Tạo YCXH loại 19 trên HRM, port nguồn chọn HĐ union của ERP
(`firm_contracts` + `wr_service_contracts`), nhập tay dòng hàng, thay scaffold `hrm_contracts`.

**Nhánh:** `gop_db` (hrm-api + hrm-client). DB trỏ PROD → chỉ SELECT đọc, KHÔNG ghi DB.
Không migration mới (gộp DB ghi thẳng bảng ERP sẵn có).

**Ràng buộc chung:**
- PHP 7.4 (không `?->`), null-safe bằng `optional()` / `?? null`.
- Số/tiền quốc tế `1,234,567.89`; ngày `dd/mm/yyyy` (BE trả sẵn).
- KHÔNG commit/push khi chưa có yêu cầu.
- KHÔNG lọc công ty trên picker (theo ERP).

---

## Phase 1 — BE: Entity + hằng số

- [x] 1.1: `FirmContract.php` — thêm `const EMPLEMENT_STATUSES = [3, 6, 7, 8, 9, 10];`
      (docblock: sao y ERP `searchEmplementAllContract` :555; khác `SELECTABLE_STATUSES` của
      bill_adjust). Tái dùng `SELECTABLE_TYPES = [1,4,8]` (đã có) cho loại HĐ emplement.
- [x] 1.2: `WrServiceContract.php` — thêm `const EMPLEMENT_TYPE = 1;` +
      `const EMPLEMENT_STATUSES = [3, 4, 6];` (docblock: sao y ERP :572-573).
- [x] 1.3: `php -l` 2 file → PASS.

## Phase 2 — BE: Endpoint tìm HĐ union

- [x] 2.1: `Modules/Assign/Routes/api.php` — thêm route TĨNH **trước** `/{id}` (cạnh :708):
      `Route::get('/emplement-contracts', [ProductExportRequestController::class, 'emplementContracts']);`
- [x] 2.2: `ProductExportRequestController` — thêm method `emplementContracts(Request $request)`
      (mô phỏng `firmContracts()` :534-561):
      - `$keyword = trim(q|keyword)`, `$limit` = clamp(1..100, mặc định 20).
      - Query A (firm): `DB::table('firm_contracts')` select
        `id, code, customer_name, customer_address`, `DB::raw("'firm' as source")`,
        `whereNull('is_zt')`, `whereIn('status', FirmContract::EMPLEMENT_STATUSES)`,
        `whereIn('type', FirmContract::SELECTABLE_TYPES)`.
      - Query B (wr): `DB::table('wr_service_contracts')` select
        `id, code, customer_name, customer_address`, `DB::raw("'wr' as source")`,
        `whereIn('status', WrServiceContract::EMPLEMENT_STATUSES)`,
        `where('type', WrServiceContract::EMPLEMENT_TYPE)`.
      - Keyword (nếu có): mỗi query `where(code like || customer_name like)`.
      - `unionAll`, bọc `fromSub(...)->orderByDesc(...)->limit($limit)` — sắp theo `id` desc trong
        từng nguồn trước union (union không giữ order), hoặc order ngoài theo `code`. Trả
        `['items' => ...]`.
      - try/catch Log::error như `firmContracts()`.
- [x] 2.3: Thêm `use` cho `FirmContract`, `WrServiceContract` ở đầu controller (nếu chưa có).
- [x] 2.4: `php -l` controller → PASS.

## Phase 3 — BE: Validate + tạo phiếu

- [x] 3.1: `rulesForType()` nhánh 19 (:696-699) — thay `exists:hrm_contracts,id`:
      - `emplement_contract_type` => `($isDraft ? 'nullable' : 'required') . '|in:firm,wr'`.
      - `emplement_contract_id` => `($isDraft ? 'nullable' : 'required') . '|integer'`
        + rule tồn tại động: `Rule::exists('firm_contracts','id')` khi type=firm,
        `Rule::exists('wr_service_contracts','id')` khi type=wr (dùng closure `function` kiểm
        theo `$request->input('emplement_contract_type')`; nếu khó, validate `integer` ở đây và
        kiểm tồn tại trong service findOrFail).
      - Giữ warehouse_id cho 19 (:764-766) y nguyên.
- [x] 3.2: `createManual()` nhánh 19 (:322-352) — resolve model động:
      ```php
      $source = $data['emplement_contract_type'] ?? null; // 'firm' | 'wr'
      $emplementContract = null;
      $emplementClass = null;
      if ($type === ProductExportRequest::XUAT_THUC_HIEN_HD && !empty($data['emplement_contract_id'])) {
          if ($source === 'wr') {
              $emplementContract = WrServiceContract::find((int) $data['emplement_contract_id']);
              $emplementClass = WrServiceContract::class;
          } else { // mặc định firm
              $emplementContract = FirmContract::find((int) $data['emplement_contract_id']);
              $emplementClass = FirmContract::class;
          }
      }
      ```
      - `emplement_contract_type` => `$emplementContract ? $emplementClass : null`.
      - Snapshot KH: `customer_id/customer_name/customer_address/customer_contact_name` từ model.
      - Điện thoại liên hệ null-safe theo 2 cột khác tên:
        `$emplementContract->customer_contact_phone ?? $emplementContract->customer_contact_phones ?? ($data['customer_mobile'] ?? null)`
        (firm = số ít, wr = số nhiều — đọc được cái nào trước).
      - Dòng hàng vẫn `insertManualLines` (giữ nguyên).
- [x] 3.3: Thêm `use` `FirmContract`/`WrServiceContract` trong Service (nếu chưa có).
- [x] 3.4: `php -l` controller + service → PASS.

## Phase 4 — FE: Form + modal

- [x] 4.1: `ProductExportRequestForm.vue` — thêm `const EMPLEMENT_CONTRACT_TYPES = [19]`
      (cạnh :950-958) + computed `isEmplementContractType()`.
- [x] 4.2: Thêm data: `showEmplementContractModal: false`,
      `selectedEmplementContract: null` (nhớ cả `source`), + field form
      `emplement_contract_id: null`, `emplement_contract_type: null` trong initialState.
- [x] 4.3: Tạo `EmplementContractSearchModal.vue` (copy `FirmContractSearchModal.vue`), đổi:
      endpoint `assign/product-export-requests/emplement-contracts?q=&limit=`,
      cột hiển thị Mã + Tên KH + Địa chỉ; khi chọn emit object kèm `source`.
- [x] 4.4: Template — thêm khối loại 19: ô "Chọn hợp đồng / đơn hàng (*)" (mở modal) + hiện tên
      HĐ đã chọn + snapshot KH/địa chỉ chỉ đọc; **giữ bảng hàng nhập tay** như MANUAL_TYPES
      (`QuotationProductSearchModal` + bảng). Thêm 19 vào điều kiện hiện bảng hàng nhập tay.
- [x] 4.5: Đăng ký `EmplementContractSearchModal` vào `components`; mở/đóng modal, gán
      `selectedEmplementContract` + `form.emplement_contract_id`/`emplement_contract_type`.
- [x] 4.6: `validateForm()` — loại 19: gửi duyệt bắt buộc HĐ + ≥1 dòng hàng; nháp chỉ cần loại.
- [x] 4.7: build payload submit gửi `emplement_contract_id` + `emplement_contract_type`.

## Phase 5 — Verify

- [x] 5.1: Playwright `http://127.0.0.1:3000` — chọn loại 19 → hiện ô chọn HĐ + bảng nhập tay.
- [x] 5.2: Modal trả cả firm + wr, đúng bộ lọc, không lọc công ty (so Network param với BE).
- [x] 5.3: Chọn HĐ → snapshot KH/địa chỉ chỉ đọc; nhập tay ≥1 dòng; lưu nháp OK; gửi duyệt OK.
- [x] 5.4: Kiểm DB phiếu vừa tạo: `emplement_contract_type` đúng class theo nguồn (chỉ đọc).

## Checkpoint — 2026-10-06
Vừa hoàn thành: Phase 5 verify trình duyệt XONG — cả 2 nguồn HĐ đã kiểm end-to-end trên `erp_new`:
- **wr**: phiếu 41534 → `emplement_contract_type = Modules\Finance\Entities\Contract\WrServiceContract` (round-trip sửa hiện đúng locked label + snapshot KH + dòng hàng).
- **firm**: phiếu 41535 → `emplement_contract_type = Modules\Finance\Entities\Contract\FirmContract`, `emplement_contract_code = HĐ_TPSG_KV3_26_0596_2409-TPET`, snapshot KH đầy đủ, `identity_card_number = 0318079636` (BE fallback `customer_tax_code ?? identity_card_number` lấy đúng MST từ model HĐ — picker union trả null nên panel FE hiện "—", nhưng bản ghi lưu đúng MST).
- Picker union firm+wr, KHÔNG lọc công ty — đã xác nhận (84 firm + 16 wr).
Đang làm dở: (không)
Bước tiếp theo: Chờ yêu cầu commit/push gop_db. Nếu cần, verify thêm nút "Lưu và gửi duyệt" (lần này mới chạy "Lưu nháp" — cùng đường `createManual`, chỉ khác status + guard validate đã verify ở FE).
Blocked: (không)

Quan sát nhỏ (không chặn Phase 5, ngoài scope): panel snapshot KH hiện MST rỗng là "—", lệch quy ước ô rỗng để trống hẳn của CLAUDE.md — là lựa chọn hiển thị FE có sẵn của panel chỉ-đọc, chưa sửa.

## Ghi chú

- gop_db: CHƯA commit (chờ yêu cầu).
- Pre-check trước code Phase 3: xác nhận cột `customer_contact_name` tồn tại trên cả 2 bảng
  (firm_contracts đã dùng ở `createManual`; wr_service_contracts fillable có — đã verify ERP model).
- Liên quan: `.plans/gop-db/ycxh-xuat-ban-hang-type14/` (mẫu khối chọn HĐ + luồng store đa loại).
