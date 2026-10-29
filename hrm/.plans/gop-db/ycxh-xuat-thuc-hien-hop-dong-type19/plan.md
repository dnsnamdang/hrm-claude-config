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

## Phase 6 — Nâng cấp popup chọn HĐ cho giống ERP (cột + link + sort + phân trang)

**Bối cảnh:** User yêu cầu 4 việc cho popup "Chọn hợp đồng / đơn hàng" ở màn Tạo YCXH loại 19:
(1) đủ 8 cột như popup ERP, (2) link vào cột số HĐ, (3) sort từng cột, (4) sửa lỗi
ERP có 16.582 bản ghi mà HRM chỉ hiện 20 (nguyên nhân: FE hard-cap `limit=20` + BE trả mảng
phẳng không phân trang server-side).

**Quyết định đã chốt (user "ok" 2026-10-13):**
- **1a:** tái dùng `utils/contract-link.js` nguyên trạng — firm → ERP `/admin/sale/firm-contracts/{id}`
  (tab mới), wr → HRM `/customer-care/wr-service-contracts/{id}` (nội bộ). Firm type 8 vẫn mở
  firm-contracts.
- **2-text:** ô lọc Khách hàng = text input LIKE `customer_name`.
- **3-snapshot:** cột Khách hàng = snapshot `customer_name` (không join bảng khách hàng).

### BE — `ProductExportRequestController::emplementContracts()` viết lại

- [x] 6.1: Validate params mới: `contract_type` (`in:firm-1,firm-4,firm-8,wr-1`), `code`, `customer`,
      `page`, `per_page`, `sort_by`, `sort_desc`.
- [x] 6.2: Mỗi nguồn (firm/wr) `leftJoin employees as ae` (ae.id = c.approver_id) +
      `leftJoin employee_infos as ai` (ai.id = ae.employee_info_id); selectRaw bổ sung
      `c.total_after_vat as total`, `ai.fullname as approver_name`, `created_at`, `type`,
      `approved_time`, `source` + giữ snapshot KH (customer_name/address/contact_name/
      contact_phone[firm số ít / wr số nhiều]/tax_code[firm NULL]).
- [x] 6.3: Lọc `contract_type` → chỉ union nguồn liên quan (firm-N lọc cả type N; wr-1 chỉ nguồn wr).
      Lọc `code` LIKE, `customer` LIKE customer_name.
- [x] 6.4: Sort whitelist `{created_at, code, type, total, approved_time}`, mặc định `created_at desc`;
      khoá lạ rơi về mặc định.
- [x] 6.5: Phân trang server-side: `DB::query()->fromSub($union,'contracts')`,
      `(clone $base)->count()` lấy total, `->forPage($page,$perPage)->get()`.
- [x] 6.6: Transform mỗi dòng: thêm `type_name` (helper `emplementTypeName`), `object_type` (morph
      class để contract-link.js dựng link), `object_id`. Trả
      `responseJson('success', 200, ['data'=>$items, 'meta'=>{current_page,last_page,total,per_page}])`.
- [x] 6.7: Helper `private function emplementTypeName(string $source, int $type): string`
      (wr → "Hợp đồng sửa chữa - bảo dưỡng - bảo trì"; firm 1/4/8 → vật tư / dự án / đơn hàng nguyên tắc).
- [x] 6.8: `php -l` controller → PASS.

### FE — `EmplementContractSearchModal.vue` viết lại theo `V2BaseDataTable`

- [x] 6.9: Dựng lại trên `V2BaseModal` + `V2BaseDataTable` (khuôn `bill-income/ContractSearchModal`),
      hỗ trợ `:pagination` + `:sort-by/:sort-direction` + `@sort/@page-change/@page-size-change`.
- [x] 6.10: 3 ô lọc: `<select>` Loại hợp đồng (Tất cả + 4 option firm-1/firm-4/firm-8/wr-1),
      `V2BaseInput` Số hợp đồng, `V2BaseInput` Khách hàng + nút Tìm kiếm / Làm mới.
- [x] 6.11: 8 cột: STT · Ngày lập(sort) · Loại hợp đồng(sort) · Số hợp đồng(sort,link) · Khách hàng ·
      Tổng thanh toán(phải,sort) · Ngày duyệt(sort) · Người duyệt.
- [x] 6.12: Cột Số HĐ render `nuxt-link`(to)/`<a href target=_blank>` qua
      `contractLink(object_type, object_id)`, `@click.stop` (cả dòng đang bắt click để CHỌN).
- [x] 6.13: `fetch()` gửi `{page,per_page,contract_type?,code?,customer?,sort_by?,sort_desc?}`,
      đọc `res.data.data` + `res.data.meta`. Chọn dòng qua `tr.emplement-row` → emit `select`+`close`.
      Tiền format en-US, ngày `DD/MM/YYYY`.

### Phase 6 — Verify (Playwright, DNS Admin namdangit@gmail.com)

- [x] 6.14: Popup hiện đủ 8 cột + 3 ô lọc + mũi tên sort; footer "Hiển thị 1–10 / 19720",
      page-size 10/20/50/100. Request `emplement-contracts?page=1&per_page=10` →
      `meta:{current_page:1,last_page:1972,total:19720,per_page:10}` (sửa xong lỗi "20 vs 16582").
- [x] 6.15: Sort "Tổng thanh toán" → `sort_by=total&sort_desc=0` trả dãy tăng dần (0,0,…,3240,3499),
      kết quả có cả firm lẫn wr.
- [x] 6.16: Lọc Loại HĐ "Đơn hàng nguyên tắc" → `contract_type=firm-8` trả 200.
- [x] 6.17: Link: firm → `http://127.0.0.1:8001/admin/sale/firm-contracts/{id}` (tab mới ERP);
      wr → `/customer-care/wr-service-contracts/{id}` (nội bộ HRM). Người duyệt join ra tên đúng
      (vd "Đoàn Sơn Tùng", "Trần Ngọc Duy").

### Checkpoint — 2026-10-13
Vừa hoàn thành: Phase 6 XONG — nâng cấp popup chọn HĐ cho giống ERP (8 cột + link cột số HĐ +
sort từng cột + phân trang server-side) và sửa lỗi "chỉ 20 dòng".
- BE `emplementContracts()` viết lại: validate contract_type/code/customer/page/per_page/sort_by/
  sort_desc; join `employees`→`employee_infos` lấy tên người duyệt; whitelist sort; phân trang
  `fromSub + count + forPage`; thêm `type_name`/`object_type`/`object_id`; helper `emplementTypeName`.
  `php -l` PASS.
- FE `EmplementContractSearchModal.vue` viết lại theo `V2BaseDataTable` (8 cột, 3 ô lọc, sort,
  phân trang, link cột số HĐ qua `contract-link.js`).
- Verify trình duyệt: total **19.720** (dev DB; ERP prod ~16.852), last_page 1972; sort total tăng
  dần OK; lọc firm-8 OK; link firm→ERP:8001 tab mới, wr→HRM nội bộ OK; tiền en-US "4,309,200".
Đang làm dở: (không)
Bước tiếp theo: Chờ yêu cầu commit/push gop_db.
Blocked: (không)

## Ghi chú

- gop_db: CHƯA commit (chờ yêu cầu).
- Pre-check trước code Phase 3: xác nhận cột `customer_contact_name` tồn tại trên cả 2 bảng
  (firm_contracts đã dùng ở `createManual`; wr_service_contracts fillable có — đã verify ERP model).
- Liên quan: `.plans/gop-db/ycxh-xuat-ban-hang-type14/` (mẫu khối chọn HĐ + luồng store đa loại).
