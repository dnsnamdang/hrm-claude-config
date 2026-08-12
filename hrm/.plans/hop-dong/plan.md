# Hợp đồng HRM (tạo từ Báo giá) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans để chạy plan theo từng task. Đánh `[x]` khi xong.

**Goal:** Dựng feature "Hợp đồng" ở HRM (module Assign), tạo 1-1 từ báo giá trúng thầu, snapshot dòng hàng (đóng băng) + các khối trường riêng của hợp đồng.

**Architecture:** Clone bộ bảng/model/service/controller/FE của Báo giá (`Modules/Assign` + `pages/assign/quotations`) sang Hợp đồng (prefix `hrm_`), thêm bảng điều khoản thanh toán + đính kèm, luồng tạo copy snapshot từ báo giá, trạng thái + phê duyệt theo ERP, phân quyền 4 cấp.

**Tech Stack:** PHP 7.4 / Laravel 8 (`nwidart/laravel-modules`, `spatie/laravel-permission`, `maatwebsite/excel`), Nuxt 2 / Vue 2 (V2Base components), MySQL DB gộp `erp_hrm_check`.

## Global Constraints (copy verbatim từ spec)
- **DB gộp `erp_hrm_check`** → MỌI bảng mới prefix **`hrm_`** (ERP cũ vẫn còn `contracts`/`contract_products`/`contract_costs`/`contract_process_payments`). KHÔNG đụng bảng ERP cũ.
- **1 báo giá → 1 hợp đồng**: `hrm_contracts.quotation_id` UNIQUE.
- **Snapshot + đóng băng dòng hàng**: copy dòng hàng từ báo giá; dòng hàng read-only; FE KHÔNG gửi dòng hàng lên khi tạo/sửa.
- **Copy Y NGUYÊN** số giá/chiết khấu/VAT từ báo giá (không tính lại).
- **Trạng thái theo ERP** (enum `App\Contract`): DANG_TAO=3, CHO_DUYET=2, DA_DUYET=1, CO_HIEU_LUC=6, CHO_HIEU_LUC=7, DANG_XUAT_HANG=8, DA_XUAT_HANG=9, DA_THANH_LY=10, DA_QUYET_TOAN=11, DANG_QUYET_TOAN=12. v1 kích hoạt 6 trạng thái đầu (DANG_TAO/CHO_DUYET/DA_DUYET/CHO_HIEU_LUC/CO_HIEU_LUC/DA_THANH_LY).
- **Có bước phê duyệt** hợp đồng (CHO_DUYET → DA_DUYET).
- **Phân quyền 4 cấp** giống báo giá (tổng cty/công ty/phòng ban/bộ phận). Permission id mới từ **1137**, `type=4`, `group='Hợp đồng'`. Sửa trực tiếp `PermissionsTableSeeder.php`, KHÔNG migration permission.
- **Xóa** chỉ khi `status=DANG_TAO`.
- **Bắt buộc nhập**: Ngày ký (`sign_date`) + Ngày hiệu lực (`effective_date`). Điều khoản thanh toán lệch tổng → chỉ cảnh báo, không chặn.
- BE rethrow `ValidationException`; FE validate inline `touched`+`is-invalid`+`invalid-feedback`. Route thao tác dữ liệu gắn `checkPermission`.
- Verify bằng **runtime + tinker** (dự án không dùng unit test PHP): `php artisan route:list`, tinker, `yarn dev`.
- Đính kèm dùng bảng `files` chung (`table='hrm_contracts'`).
- **KHÔNG commit/push git khi chưa có yêu cầu user.**

---

## PHASE 1 — Database (migrations + entities)

### Task 1.1: Migration bảng cha `hrm_contracts`
**Files:**
- Create: `hrm-api/database/migrations/2026_08_10_100001_create_hrm_contracts_table.php`
- Tham chiếu khuôn: `database/migrations/2026_04_14_100005_create_quotations_table.php` (+ các add-column migration của quotations để gộp cột vào 1 migration mới)

**Deliverable:** Bảng `hrm_contracts` với 3 nhóm cột (spec §3.1):
- ① Snapshot: `quotation_id` (unsignedBigInteger, UNIQUE, FK→quotations), `customer_id`, `customer_code`, `customer_name`, `customer_tax_code`, `customer_address`, `customer_contact_name`, `customer_contact_phone`, `customer_email`, `project_id`, `solution_id`, `solution_version_id`, `solution_module_id` (nullable), `solution_module_version_id` (nullable), `currency_id`, `exchange_rate` decimal(15,4), `price_type_id`, `discount_method` tinyint, `rounding_mode`, `shipping_cost`, `shipping_vat_percent`, `shipping_discount`, `total_vat_amount`, `total_after_vat`, `total_discount_amount`, `description`, `payment_terms`, `validity_date`.
- ② Trường riêng: `code_input` nullable, `sign_date` date, `effective_date` date, `expiry_date` date nullable, `valid_approver_id` nullable; `representative_name`, `representative_role`, `customer_id_card_number`, `customer_id_card_date` date nullable, `customer_id_card_place`, `company_signer_id` nullable, `company_signer_role`; `customer_bank_account_number`, `customer_bank_name`, `customer_bank_branch`, `company_account_number`, `company_account_name`, `company_bank_name`, `company_bank_branch`, `company_name`, `company_phone`, `company_address`, `company_tax_code`.
- ③ `code` (unique), `status` tinyint default 3 (DANG_TAO), `approver_id` nullable, `approved_at` nullable, `submitted_at` nullable, `rejected_reason` nullable, `company_id`/`department_id`/`part_id` unsignedBigInteger nullable, `created_by`/`updated_by` nullable, `timestamps()`.

**Verify:**
- [x] Chạy `php artisan migrate` trên DB local (kiểm `grep DB_ .env` trước), `SHOW COLUMNS FROM hrm_contracts` đủ cột. ✅ 65 cột, migrate OK.
- [x] `SELECT COUNT(*) FROM information_schema.tables WHERE table_name='hrm_contracts'` = 1. ✅ + quotation_id UNIQUE+FK, code unique.
- [ ] Commit khi user yêu cầu.
- **[✔ REVIEW PASSED 2026-08-10]** file `2026_08_10_100001_create_hrm_contracts_table.php`.

### Task 1.2: Migrations 6 bảng con
**Files:** Create trong `hrm-api/database/migrations/` (mốc `2026_08_10_1000xx`):
- `..02_create_hrm_contract_groups_table.php` — clone `quotation_groups`: `contract_id`, `name`, `sort_order`, `parent_id` nullable.
- `..03_create_hrm_contract_product_prices_table.php` — clone `quotation_product_prices`: `contract_id`, `contract_group_id` nullable, `parent_id` nullable, `product_type`, `sort_order`, snapshot SP (`erp_product_id`, `code`, `name`, `model_id`, `brand_id`, `origin_id`, `unit_id`, `qty_needed`, `product_attributes`, `show_children`), `estimated_price`, `quoted_price`, `vat_percent`, `discount_input_mode`, `discount_percent`, `discount_amount`, `allocated_discount_amount`, `unit_price_after_discount`.
- `..04_create_hrm_contract_service_items_table.php` — clone `quotation_service_items`.
- `..05_create_hrm_contract_discounts_table.php` — clone `quotation_discounts`.
- `..06_create_hrm_contract_process_payments_table.php` — MỚI: `contract_id`, `sort_order`, `milestone`, `deadline` date nullable, `amount` decimal nullable, `amount_percent` decimal nullable, `note`.
- `..07_create_hrm_contract_histories_table.php` — clone `quotation_histories`.

**Verify:**
- [ ] `php artisan migrate`; `SHOW COLUMNS` từng bảng khớp khuôn.
- [ ] Commit khi user yêu cầu.

### Task 1.3: Entities + relations
**Files:** Create trong `hrm-api/Modules/Assign/Entities/Contract/`:
- `Contract.php` (khuôn `Entities/Quotation.php`) — `$table='hrm_contracts'`; hằng số trạng thái (Global Constraints); relations: `quotation()` belongsTo Quotation; `groups()`/`products()`/`serviceItems()`/`discounts()`/`processPayments()`/`histories()` hasMany; `files()` = `hasMany(File::class,'table_id','id')->where('table','hrm_contracts')`; `getNextCode()` (copy `Quotation::getNextCode()`, prefix chốt ở Task 2.2); accessor `is_can_delete` = `status == DANG_TAO`.
- `ContractGroup.php`, `ContractProductPrice.php` (self-ref `parent()`/`children()`), `ContractServiceItem.php`, `ContractDiscount.php`, `ContractProcessPayment.php`, `ContractHistory.php`.
- Modify: `Modules/Assign/Entities/Quotation.php` — thêm relation `contract()` hasOne(Contract) + accessor `has_contract` = `$this->contract()->exists()`.

**Verify:**
- [ ] tinker: `App\...\Contract::getModel()->getTable()` = `hrm_contracts`; tạo thử 1 record + quan hệ con load được.
- [ ] Commit khi user yêu cầu.

---

## PHASE 2 — Backend

### Task 2.1: `ContractService::createFromQuotation`
**Files:** Create `hrm-api/Modules/Assign/Services/ContractService.php` (khuôn `QuotationService::create`).
**Deliverable:** `createFromQuotation(Quotation $quotation, array $data): Contract` trong `DB::transaction`:
- Guard: `$quotation->status == Quotation::DA_DUYET` else `throw ValidationException` (422); `!$quotation->has_contract` else 422 "Báo giá đã lập hợp đồng".
- Tạo header: copy cột snapshot §3.1① từ quotation; set trường riêng từ `$data`; `code = $contract->getNextCode()`; `status = DANG_TAO`; `company_id/department_id/part_id/created_by` từ auth.
- Copy con giữ quan hệ: map `quotation_groups→hrm_contract_groups` (mảng old_id→new_id, giữ parent_id 2 cấp); `quotation_product_prices→hrm_contract_product_prices` (map contract_group_id + parent_id combo); `quotation_service_items→hrm_contract_service_items`; `quotation_discounts→hrm_contract_discounts`. Copy nguyên số tiền.
- Lưu `process_payments[]` từ `$data`.
- `recomputeTotals()` (copy `QuotationService::recomputeTotals`, chỉ kiểm khớp) → ghi `total_*`.
- `logHistory(ACTION_CREATE)`.

**Verify:**
- [ ] tinker: lấy 1 quotation DA_DUYET → `createFromQuotation` → kiểm `hrm_contracts` + con copy đủ, parent_id combo/nhóm đúng, tổng khớp báo giá.
- [ ] Commit khi user yêu cầu.

### Task 2.2: Controller store + Request + Resource + getNextCode prefix
**Files:**
- Create `Modules/Assign/Http/Controllers/Api/V1/ContractController.php` (khuôn `QuotationController`).
- Create `Modules/Assign/Http/Requests/Contract/ContractStoreRequest.php`, `ContractUpdateRequest.php` — rule: `quotation_id` required|exists; `sign_date` required|date; `effective_date` required|date; các trường riêng nullable; `process_payments` array nullable.
- Create `Modules/Assign/Transformers/DetailContractResource.php`, `ContractResource.php` (khuôn Detail/QuotationResource).
- Chốt prefix mã trong `Contract::getNextCode()` — mặc định `HĐ-YYYY-NNNNN` (xác nhận với user nếu cần HD/CT).
**Deliverable:** `store()` gọi `service->createFromQuotation`, gate quyền "Lập hợp đồng" theo scope (copy pattern gate của QuotationController), rethrow ValidationException, 403 khi sai quyền.
**Verify:**
- [ ] `php artisan route:list | grep assign/contracts`; gọi thử API tạo (Postman/tinker) → 200 + resource đúng; tạo lại từ cùng báo giá → 422.
- [ ] Commit khi user yêu cầu.

### Task 2.3: Routes `/assign/contracts` + guard/scope
**Files:** Modify `Modules/Assign/Routes/api.php` — thêm nhóm prefix `/assign/contracts`: `GET /` (index, scope 4 cấp), `GET /{id}` (show), `POST /` (store), `PUT /{id}` (update), `DELETE /{id}` (destroy), `POST /{id}/submit`, `POST /{id}/approve`, `POST /{id}/reject`, `POST /{id}/activate` (CHO_HIEU_LUC→CO_HIEU_LUC), `POST /{id}/liquidate` (thanh lý), `POST /{id}/attachments`, `DELETE /{id}/attachments/{fileId}`. Gắn `auth:api` + `checkPermission:<quyền>` (Task 2.7).
**Deliverable:** `index()` scope theo 4 quyền xem (copy `scopedQuotationQuery`), server-side filter công ty/phòng/bộ phận.
**Verify:**
- [ ] `route:list` đủ route + middleware; test index trả đúng scope với 2 user khác cấp.
- [ ] Commit khi user yêu cầu.

### Task 2.4: Update (đóng băng dòng hàng)
**Files:** Modify `ContractController` + `ContractService::update`.
**Deliverable:** `update()` chỉ cho khi `status ∈ {DANG_TAO, CHO_DUYET}`; chỉ nhận trường riêng + `process_payments[]` + attachments; **bỏ qua mọi dữ liệu dòng hàng gửi lên** (đóng băng). Rethrow ValidationException.
**Verify:**
- [ ] tinker/API: sửa trường riêng OK; sửa khi CO_HIEU_LUC → 422; dòng hàng không đổi.
- [ ] Commit khi user yêu cầu.

### Task 2.5: Chuyển trạng thái + phê duyệt + history
**Files:** `ContractService` methods: `submit`, `approve`, `reject($reason)`, `activate`, `liquidate`; ghi `hrm_contract_histories` mỗi bước.
**Deliverable:** transitions đúng luồng v1 (Global Constraints); guard trạng thái nguồn hợp lệ; set `approver_id/approved_at/submitted_at/rejected_reason`.
**Verify:**
- [ ] tinker: chạy full vòng DANG_TAO→CHO_DUYET→DA_DUYET→CHO_HIEU_LUC→CO_HIEU_LUC→DA_THANH_LY; reject về DANG_TAO; sai nguồn → 422; history ghi đủ.
- [ ] Commit khi user yêu cầu.

### Task 2.6: Đính kèm (files)
**Files:** `ContractController::uploadAttachments`/`deleteAttachment` (khuôn cơ chế upload S3 + bảng `files` của HRM), `Contract::files()`.
**Deliverable:** upload nhiều file → `files(table='hrm_contracts', table_id)`; xóa file; show trả kèm files.
**Verify:**
- [ ] API upload 2 file → `files` có 2 record đúng table; xóa 1 → còn 1.
- [ ] Commit khi user yêu cầu.

### Task 2.7: Permissions seeder + gắn middleware
**Files:** Modify `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — thêm nhóm `group='Hợp đồng'`, `type=4`, id 1137+:
- 1137 Lập hợp đồng theo công ty · 1138 Lập hợp đồng theo phòng · 1139 Sửa hợp đồng · 1140 Xóa hợp đồng · 1141 Duyệt hợp đồng · 1142 Xác nhận hiệu lực hợp đồng · 1143 Thanh lý hợp đồng · 1144 Xem danh sách Hợp đồng theo tổng công ty · 1145 …theo công ty · 1146 …theo phòng ban · 1147 …theo bộ phận.
Gắn `checkPermission:<quyền>` lên route store/update/destroy/approve/activate/liquidate (Task 2.3).
**Verify:**
- [ ] tinker `firstOrCreate` áp 11 quyền lên DB gộp + gán role test; gọi route thiếu quyền → 403.
- [ ] Commit khi user yêu cầu.

---

## PHASE 3 — Frontend (hrm-client)

### Task 3.1: Danh sách `pages/assign/contracts/index.vue`
**Files:** Create (khuôn `pages/assign/quotations/index.vue`).
**Deliverable:** FilterPanel (keyword/khách hàng/trạng thái/ngày) + DataTable (mã HĐ, mã BG, khách hàng, ngày ký, hiệu lực, giá trị, trạng thái, thao tác). Ẩn/hiện theo 4 quyền xem.
**Verify:**
- [ ] `yarn dev` → trang list load, filter + phân trang chạy; scope theo quyền.
- [ ] Commit khi user yêu cầu.

### Task 3.2: Form tạo/sửa `_id/edit.vue` + `create.vue`
**Files:** Create `pages/assign/contracts/_id/edit.vue` (khuôn quotations edit.vue, rút gọn), `create.vue` (wrapper nhận `?quotation_id=X`).
**Deliverable:** Bố cục spec §5: (1) thông tin từ báo giá + bảng dòng hàng **read-only** (reuse view dòng hàng của quotations, disable edit); (2) khối A; (3) B; (4) C (auto-fill pháp nhân/TK công ty theo công ty nếu có danh mục, cho sửa đè); (5) E `ContractPaymentTermsTable`; (6) H upload. Payload chỉ `quotation_id`+trường riêng+`process_payments[]`+attachments. Validate: bắt buộc `sign_date`+`effective_date`; payment lệch tổng → cảnh báo. Nút Lưu nháp / Trình duyệt.
**Verify:**
- [ ] `yarn dev`: từ báo giá trúng thầu tạo HĐ → dòng hàng hiển thị read-only, lưu nháp OK, thiếu ngày ký/hiệu lực → viền đỏ; payment lệch → cảnh báo không chặn.
- [ ] Commit khi user yêu cầu.

### Task 3.3: Component `ContractPaymentTermsTable.vue`
**Files:** Create `hrm-client/components/...` (theo modal-popup/button-convention nếu áp dụng).
**Deliverable:** bảng thêm/xóa đợt: mô tả, mốc/deadline, số tiền HOẶC %, ghi chú; tính tổng % + tổng tiền, cảnh báo khi ≠ 100% / ≠ giá trị HĐ.
**Verify:**
- [ ] Thêm/xóa đợt, tổng cập nhật, cảnh báo hiện đúng.
- [ ] Commit khi user yêu cầu.

### Task 3.4: Chi tiết `_id/index.vue` + actions trạng thái
**Files:** Create `pages/assign/contracts/_id/index.vue`.
**Deliverable:** hiển thị đầy đủ HĐ + dòng hàng + điều khoản thanh toán + đính kèm + lịch sử; nút theo trạng thái/quyền: Trình duyệt / Duyệt / Từ chối / Xác nhận hiệu lực / Thanh lý.
**Verify:**
- [ ] `yarn dev`: chạy full vòng trạng thái trên UI với quyền tương ứng.
- [ ] Commit khi user yêu cầu.

### Task 3.5: Nút "Lập hợp đồng" trên báo giá + `has_contract`
**Files:** Modify `pages/assign/quotations/_id/index.vue` (+ resource báo giá trả `has_contract`, `contract_id`).
**Deliverable:** báo giá `TRÚNG THẦU` & chưa có HĐ → nút "Lập hợp đồng" (điều hướng `contracts/create?quotation_id=X`, gate quyền Lập); đã có HĐ → nút "Xem hợp đồng".
**Verify:**
- [ ] `yarn dev`: nút hiện đúng theo trạng thái báo giá + quyền.
- [ ] Commit khi user yêu cầu.

### Task 3.6: Menu + tab phân quyền
**Files:** Modify menu (khuôn menu báo giá trong `pages/assign` / file cấu hình menu) + đảm bảo nhóm "Hợp đồng" (type 4) hiện ở màn Phân quyền.
**Verify:**
- [ ] Menu "Hợp đồng" hiện; màn Phân quyền có nhóm Hợp đồng gán được.
- [ ] Commit khi user yêu cầu.

---

## PHASE 4 — Verify tổng thể (E2E)
- [ ] E2E: báo giá DA_DUYET → Lập HĐ → snapshot dòng hàng đóng băng đúng → điền khối A/B/C/E/H → lưu nháp → trình duyệt → duyệt → xác nhận hiệu lực → thanh lý; sửa báo giá gốc không ảnh hưởng HĐ.
- [ ] Phân quyền 4 cấp: 4 user khác cấp thấy đúng phạm vi; thiếu quyền thao tác → 403.
- [ ] Xóa: chỉ nháp xóa được; DA_DUYET trở đi không xóa.
- [ ] Đính kèm upload/xóa OK; điều khoản thanh toán cảnh báo lệch tổng nhưng vẫn lưu.

---

## Câu hỏi mở (chốt khi code, không chặn plan)
- Danh mục cấu hình TK ngân hàng công ty (auto-fill khối C) — có sẵn chưa? Chưa → v1 nhập tay.
- "Xác nhận hiệu lực" (1142) tách hay gộp vào "Duyệt" (1141).
- Prefix mã tự sinh: `HĐ`/`HD`/`CT`.

## Checkpoint — 2026-08-10
Vừa hoàn thành: **Phase 1 (Database) — 3/3 task, subagent-driven + review PASSED**, nhánh `hop-dong` (hrm-api + hrm-client tạo từ gop_db).
- Task 1.1 ✅ migration `hrm_contracts` (65 cột, quotation_id UNIQUE+FK, code unique).
- Task 1.2 ✅ 6 bảng con (`hrm_contract_groups/product_prices/service_items/discounts/process_payments/histories`), FK contract_id/contract_group_id/parent_id đúng.
- Task 1.3 ✅ 7 entity `Modules/Assign/Entities/Contract/` + Quotation.contract()/has_contract; mã `HĐ-YYYY-NNNNN`; File=`App\Models\File`.
- Migrate đã chạy trên DB local `erp_hrm_check` (127.0.0.1). **CHƯA commit git** (chờ user).
**Phase 2 (Backend) — 7/7 task, subagent-driven + review PASSED:**
- 2.1 ✅ `ContractService::createFromQuotation` (guard DA_DUYET+unique, snapshot copy header + con remap parent_id combo/nhóm, process_payments, history) — verified báo giá id=61 (183 SP/6 nhóm/16 combo).
- 2.2 ✅ ContractController(store/show)+ContractStore/UpdateRequest+Detail/ContractResource; gate `isCurrentEmployeeHasPermission`.
- 2.3 ✅ routes index/show/store/destroy + index scope 4 cấp (`scopedContractQuery`+`checkPermissionListWithColumn`) + destroy guard is_can_delete.
- 2.4 ✅ update (đóng băng dòng hàng, chỉ trường riêng + thay process_payments).
- 2.5 ✅ submit/approve/reject/activate/liquidate (guard trạng thái + history) — verified full vòng 3→2→1→6→10.
- 2.6 ✅ đính kèm: `TableFileHelper`+`CmcS3Helper` bảng `files`(table='hrm_contracts') — S3 thật cần test multipart.
- 2.7 ✅ 11 quyền 1137-1147 nhóm 'Hợp đồng' type 4 + middleware checkPermission.
CHƯA commit git (chờ user). **CHƯA áp permission qua tinker trên DB gộp** (user làm khi deploy).

Đang làm dở: (không) — Phase 2 xong.

**Phase 3 (Frontend, hrm-client) — 6/6 task xong (code-complete, CHƯA verify runtime):**
- 3.1 ✅ `pages/assign/contracts/index.vue` (list: filter keyword/status/ngày ký + DataTable + badge trạng thái). API params khớp controller. Field `quotation_code` flat.
- 3.2+3.3 ✅ `pages/assign/contracts/create.vue` (wrapper ?quotation_id) + `_id/edit.vue` (form 6 khối: dòng hàng READ-ONLY qua `buildLineRows()`, khối A/B/C/E/H, validate inline sign_date+effective_date, payload KHÔNG gửi dòng hàng, nút Lưu nháp/Trình duyệt) + `components/ContractPaymentTermsTable.vue` (thêm/xóa đợt, cảnh báo lệch tổng không chặn). Khối C nhập tay (codebase KHÔNG có danh mục TK/pháp nhân công ty — đã confirm). Đính kèm hand-rolled FormData `files[]`.
- 3.4 ✅ `_id/index.vue` chi tiết + thanh nút actions (map trạng thái + ẩn theo quyền `hasAPermission`, popup từ chối gửi `rejected_reason`).
- 3.5 ✅ nút "Lập hợp đồng"/"Xem hợp đồng" trên chi tiết báo giá + `DetailQuotationResource` trả `has_contract`/`contract_id`.
- 3.6 ✅ menu "Hợp đồng" → `/assign/contracts` (`components/subsystem-menu/sale-hub.js`); tab phân quyền render động (nhóm 'Hợp đồng' type 4 tự hiện, không sửa code).

**⚠ CHƯA verify runtime FE** (lint offline — chỉ review cú pháp). Cần user `yarn dev` kiểm: V2Base v-model 2 kiểu binding, `this.$store.state.employees` (3.2 thêm fallback `allEmployeesData` cần confirm), format ngày payload BE, upload/xóa file UX, CSS viền đỏ `::v-deep` trong V2Base, route conflict create.vue↔_id/edit.vue.

### Checkpoint — 2026-08-11 (CODE COMPLETE 19/19)
Vừa hoàn thành: **TOÀN BỘ 3 Phase (DB 3 + BE 7 + FE 6)** qua subagent-driven + review từng task. Nhánh `hop-dong` (hrm-api + hrm-client). **CHƯA commit git.**
Đang làm dở: (không) — code xong hết.
Bước tiếp theo (user):
1. `yarn dev` verify runtime toàn bộ FE (list/tạo/sửa/chi tiết/nút báo giá/menu/phân quyền) — FE mới review cú pháp offline, CHƯA chạy trình duyệt.
2. Áp 11 permission 1137-1147 qua tinker `firstOrCreate` + gán role test.
3. Test E2E full vòng: báo giá duyệt → Lập HĐ → snapshot đóng băng → điền A/B/C/E/H → trình duyệt → duyệt → hiệu lực → thanh lý; xóa chỉ nháp; đính kèm S3 multipart thật.
4. Commit + PR khi duyệt.
Blocked: (không).
3 câu hỏi mở chốt khi test: prefix mã (`HĐ`), auto-fill TK công ty (nhập tay - chưa có danh mục), tách/gộp quyền hiệu lực.

---

## Phase 4 — Doanh số vượt trội + Giảm giá (điều chỉnh thương mại trên hợp đồng)

> Spec: `docs/superpowers/specs/2026-08-11-hop-dong-doanh-so-vuot-troi-design.md`.
> Cho phép nhập **Doanh số vượt trội** (/đơn vị) + chỉnh **Giảm giá** trên **dòng hàng CHA** (ở cả màn Tạo lẫn Sửa), tính lại tổng, và chặn duyệt khi vượt hạn mức (chuyển BGD = role "Giám đốc"). Mirror logic hợp đồng ERP.

### Global Constraints — Phase 4 (copy verbatim từ spec)
- **Chỉ dòng hàng CHA** (`parent_id = null`, hàng hoá) nhận `extra_price` + chỉnh giảm giá. Dòng con/nhóm: bỏ qua.
- **Cách A**: chỉ lưu 2 cột mới `extra_price` (bảng chi tiết) + `total_extra_amount` (bảng HĐ). Số dẫn xuất (after_extra, before_vat, vat, after_vat) **tính runtime**, KHÔNG lưu.
- **Công thức dòng**: `line_after_extra = (quoted_price + extra_price) × qty`; `line_discount` theo `discount_method` (2 = `allocated_discount_amount`; khác = `discount_amount × qty`); `line_before_vat = line_after_extra − line_discount`; `line_vat = line_before_vat × vat_percent/100`; `line_after_vat = line_before_vat + line_vat`.
- **Hạn mức**: `base = Σ line_before_vat`; `percent = base>0 ? total_extra_amount/base×100 : 0`; ngưỡng = `departments.max_extra_price_percent` theo `hrm_contracts.department_id`. `null`/`0` → không giới hạn.
- **BGD = role "Giám đốc"** — check qua `\Modules\Timesheet\Entities\Employee` (model có `HasRoles`, KHÔNG phải `Modules\Human\Entities\Employee`).
- **Kiểm hạn mức đặt ở `approve()`**; ném `ValidationException` (rethrow, KHÔNG catch chung `Exception`).
- **Không thêm quyền mới, không migration permission.** Không thêm trạng thái mới.
- **Không commit git khi chưa có yêu cầu** — kết thúc mỗi task chỉ đánh `[x]`; gộp commit khi user yêu cầu.
- Verify theo convention repo: **tinker + artisan migrate** (BE) và **yarn dev** (FE) — repo không có phpunit test cho Contract.

---

### Task 4.1 — DB: 2 cột mới (`extra_price`, `total_extra_amount`)

**Files:**
- Create: `hrm-api/database/migrations/2026_08_11_100001_add_extra_price_to_hrm_contract_product_prices_table.php`
- Create: `hrm-api/database/migrations/2026_08_11_100002_add_total_extra_amount_to_hrm_contracts_table.php`

**Interfaces — Produces:** cột `hrm_contract_product_prices.extra_price` (decimal 15,2, default 0), `hrm_contracts.total_extra_amount` (decimal 18,2, default 0).

- [ ] **Step 1: Viết migration `extra_price`**
```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddExtraPriceToHrmContractProductPricesTable extends Migration
{
    public function up()
    {
        Schema::table('hrm_contract_product_prices', function (Blueprint $table) {
            $table->decimal('extra_price', 15, 2)->default(0)
                ->comment('Doanh số vượt trội / đơn vị (chỉ dòng hàng cha)')
                ->after('quoted_price');
        });
    }
    public function down()
    {
        Schema::table('hrm_contract_product_prices', function (Blueprint $table) {
            $table->dropColumn('extra_price');
        });
    }
}
```

- [ ] **Step 2: Viết migration `total_extra_amount`**
```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddTotalExtraAmountToHrmContractsTable extends Migration
{
    public function up()
    {
        Schema::table('hrm_contracts', function (Blueprint $table) {
            $table->decimal('total_extra_amount', 18, 2)->default(0)
                ->comment('Tổng doanh số vượt trội = Σ(extra_price × SL) dòng cha')
                ->after('total_after_vat');
        });
    }
    public function down()
    {
        Schema::table('hrm_contracts', function (Blueprint $table) {
            $table->dropColumn('total_extra_amount');
        });
    }
}
```

- [ ] **Step 3: Chạy migrate**
Run: `cd hrm-api && php artisan migrate`
Expected: 2 migration `Migrated` không lỗi.

- [ ] **Step 4: Verify cột tồn tại**
Run: `php artisan tinker --execute="echo Schema::hasColumn('hrm_contract_product_prices','extra_price')?'OK1 ':'FAIL1 '; echo Schema::hasColumn('hrm_contracts','total_extra_amount')?'OK2':'FAIL2';"`
Expected: `OK1 OK2`

- [ ] **Step 5: Checkpoint** (đánh `[x]`, KHÔNG commit — chờ user)

---

### Task 4.2 — BE: recompute tổng + áp `line_adjustments` (store & update)

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/ContractService.php`

**Interfaces — Produces:**
- `private setLineAdjustment(ContractProductPrice $line, array $adj, int $userId, ?int $discountMethod): void`
- `public recomputeTotals(Contract $contract): void`
- `createFromQuotation()` nhận `$data['line_adjustments']` (key `source_price_id` = báo giá qpp id)
- `update()` nhận `$data['line_adjustments']` (key `price_id` = hrm_contract_product_prices id)

**Consumes:** `ContractProductPrice` (`$guarded=[]`), `Contract`, cột `extra_price`/`total_extra_amount` (Task 4.1).

- [ ] **Step 1: Thêm helper `setLineAdjustment` + `recomputeTotals`** vào `ContractService`
```php
/** Áp điều chỉnh (vượt trội + giảm giá) cho 1 dòng hàng CHA. Dùng chung store & update. */
private function setLineAdjustment(ContractProductPrice $line, array $adj, int $userId, ?int $discountMethod): void
{
    $line->extra_price = max(0, (float)($adj['extra_price'] ?? 0));
    if ((int)$discountMethod === 2) {
        $line->allocated_discount_amount = max(0, (float)($adj['allocated_discount_amount'] ?? 0));
    } else {
        $line->discount_percent = max(0, (float)($adj['discount_percent'] ?? 0));
        $line->discount_amount  = max(0, (float)($adj['discount_amount'] ?? 0));
    }
    $line->updated_by = $userId;
    $line->save();
}

/** Tính lại tổng HĐ từ các dòng hàng CHA (parent_id=null). Ghi total_* vào hrm_contracts. */
public function recomputeTotals(Contract $contract): void
{
    $method = (int) $contract->discount_method;
    $parents = ContractProductPrice::where('contract_id', $contract->id)
        ->whereNull('parent_id')->get();

    $totalExtra = 0.0; $totalDiscount = 0.0; $totalVat = 0.0; $totalAfterVat = 0.0;
    foreach ($parents as $p) {
        $qty        = (float) $p->qty_needed;
        $sale       = (float) $p->quoted_price * $qty;
        $extra      = (float) $p->extra_price * $qty;
        $afterExtra = $sale + $extra;
        $discount   = $method === 2
            ? (float) $p->allocated_discount_amount
            : (float) $p->discount_amount * $qty;
        $beforeVat  = $afterExtra - $discount;
        $vat        = $beforeVat * (float) $p->vat_percent / 100;

        $totalExtra    += $extra;
        $totalDiscount += $discount;
        $totalVat      += $vat;
        $totalAfterVat += $beforeVat + $vat;
    }

    $contract->total_extra_amount    = round($totalExtra, 2);
    $contract->total_discount_amount = round($totalDiscount, 2);
    $contract->total_vat_amount      = round($totalVat, 2);
    $contract->total_after_vat       = round($totalAfterVat, 2);
    $contract->save();
}
```

- [ ] **Step 2: Áp `line_adjustments` trong `createFromQuotation()`** — SAU vòng remap `parent_id` của products (sau dòng cập nhật `productIdMap`, ~dòng 193), THAY cho comment `// ---- 5. Totals: đã đóng băng ...`:
```php
// ---- 4b. Áp điều chỉnh vượt trội/giảm giá (nếu FE gửi) — key theo id dòng BÁO GIÁ nguồn ----
if (!empty($data['line_adjustments']) && is_array($data['line_adjustments'])) {
    $adjBySource = collect($data['line_adjustments'])->keyBy('source_price_id');
    foreach ($products as $p) {                 // $products = báo giá productPrices (đã load ở trên)
        if ($p->parent_id !== null) continue;   // chỉ dòng cha
        $adj = $adjBySource->get($p->id);
        if (!$adj) continue;
        $newId = $productIdMap[(int) $p->id] ?? null;
        $line = $newId ? ContractProductPrice::find($newId) : null;
        if ($line) $this->setLineAdjustment($line, (array) $adj, $userId, $contract->discount_method);
    }
}

// ---- 5. Totals: recompute (gồm điều chỉnh; không có adjustment thì ra đúng tổng báo giá) ----
$this->recomputeTotals($contract);
```

- [ ] **Step 3: Áp `line_adjustments` trong `update()`** — thêm trước bước History (sau khối process_payments), key theo id dòng HỢP ĐỒNG:
```php
// ---- 2b. line_adjustments: chỉnh vượt trội/giảm giá dòng cha ----
if (array_key_exists('line_adjustments', $data) && is_array($data['line_adjustments'])) {
    foreach ($data['line_adjustments'] as $adj) {
        $line = ContractProductPrice::where('contract_id', $contract->id)
            ->where('id', $adj['price_id'] ?? 0)
            ->whereNull('parent_id')
            ->first();
        if (!$line) continue;
        $this->setLineAdjustment($line, (array) $adj, $userId, $contract->discount_method);
    }
    $this->recomputeTotals($contract);
}
```

- [ ] **Step 4: Verify recompute qua tinker** (báo giá 52 = trúng thầu, created_by=13)
Run:
```
cd hrm-api && php artisan tinker --execute="
\$q = \Modules\Assign\Entities\Quotation::find(52);
\$svc = app(\Modules\Assign\Services\ContractService::class);
auth()->loginUsingId(13);
\$firstParent = \$q->productPrices()->whereNull('parent_id')->orderBy('sort_order')->first();
\$c = \$svc->createFromQuotation(\$q->fresh(), ['line_adjustments'=>[['source_price_id'=>\$firstParent->id,'extra_price'=>100000]]]);
echo 'total_extra='.\$c->total_extra_amount.' total_after_vat='.\$c->total_after_vat;
\$svc->destroy(\$c->fresh());
"
```
Expected: `total_extra` = 100000 × SL dòng đó (> 0), `total_after_vat` tăng tương ứng. (Nếu báo giá 52 đã có HĐ → dùng báo giá trúng thầu khác chưa lập HĐ; hoặc xoá HĐ cũ trước.)

- [ ] **Step 5: Checkpoint** (đánh `[x]`, KHÔNG commit)

---

### Task 4.3 — BE: hạn mức + chặn duyệt BGD

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/ContractService.php`

**Interfaces — Produces:**
- `private sumBeforeVat(Contract $contract): float`
- `private currentEmployeeHasRole(string $roleName): bool`
- `private assertExtraWithinLimitOrBgd(Contract $contract): void`
- `approve()` gọi `assertExtraWithinLimitOrBgd()` trước khi chuyển trạng thái.

**Consumes:** `\Modules\Timesheet\Entities\Department` (đọc `max_extra_price_percent`), `\Modules\Timesheet\Entities\Employee` (HasRoles), `ValidationException` (đã `use`).

- [ ] **Step 1: Thêm 3 helper** vào `ContractService`
```php
/** Σ giá trị trước VAT của các dòng cha (mẫu số hạn mức). */
private function sumBeforeVat(Contract $contract): float
{
    $method = (int) $contract->discount_method;
    $sum = 0.0;
    foreach (ContractProductPrice::where('contract_id', $contract->id)->whereNull('parent_id')->get() as $p) {
        $qty        = (float) $p->qty_needed;
        $afterExtra = ((float) $p->quoted_price + (float) $p->extra_price) * $qty;
        $discount   = $method === 2 ? (float) $p->allocated_discount_amount : (float) $p->discount_amount * $qty;
        $sum += ($afterExtra - $discount);
    }
    return $sum;
}

/** Người đang đăng nhập có role $roleName không (dùng model Timesheet\Employee có HasRoles). */
private function currentEmployeeHasRole(string $roleName): bool
{
    $user = auth()->user();
    if (!$user) return false;
    $emp = \Modules\Timesheet\Entities\Employee::where('employee_info_id', $user->employee_info_id)->first();
    return $emp ? $emp->roles->pluck('name')->contains($roleName) : false;
}

/** Chặn duyệt nếu tổng vượt trội vượt hạn mức phòng ban & người duyệt không phải BGD (role "Giám đốc"). */
private function assertExtraWithinLimitOrBgd(Contract $contract): void
{
    $limit = optional(\Modules\Timesheet\Entities\Department::find($contract->department_id))->max_extra_price_percent;
    if (!$limit || (float) $limit <= 0) return;                 // không cấu hình → không giới hạn

    $base = $this->sumBeforeVat($contract);
    $percent = $base > 0 ? ((float) $contract->total_extra_amount / $base * 100) : 0;
    if ($percent <= (float) $limit) return;                     // trong hạn mức

    if ($this->currentEmployeeHasRole('Giám đốc')) return;      // BGD duyệt → cho qua

    throw ValidationException::withMessages([
        'extra' => [sprintf(
            'Hợp đồng vượt hạn mức Doanh số vượt trội (%.2f%% > %.2f%%). Vui lòng chuyển duyệt BGD (Giám đốc).',
            $percent, (float) $limit
        )],
    ]);
}
```

- [ ] **Step 2: Gọi kiểm hạn mức đầu `approve()`** — thêm dòng đầu tiên của method (trước `$this->transition(...)`):
```php
public function approve(Contract $contract): Contract
{
    $this->assertExtraWithinLimitOrBgd($contract);   // chặn nếu vượt hạn mức & không BGD
    $employeeId = $this->currentEmployeeId();
    return $this->transition(
        $contract,
        [Contract::STATUS_CHO_DUYET],
        Contract::STATUS_DA_DUYET,
        ['approver_id' => $employeeId, 'approved_at' => now()],
        'approve'
    );
}
```

- [ ] **Step 3: Verify chặn/cho qua qua tinker** — tạo HĐ vượt trội lớn, set ngưỡng phòng ban nhỏ, duyệt bằng người không "Giám đốc" → phải ném ValidationException; gán role "Giám đốc" → qua.
Run (khung, chỉnh id thực tế):
```
cd hrm-api && php artisan tinker --execute="
auth()->loginUsingId(13);
\$c = \Modules\Assign\Entities\Contract\Contract::where('status',2)->latest('id')->first();
\$dept = \Modules\Timesheet\Entities\Department::find(\$c->department_id);
\$old = \$dept->max_extra_price_percent; \$dept->max_extra_price_percent = 0.01; \$dept->save();
\$svc = app(\Modules\Assign\Services\ContractService::class);
try { \$svc->approve(\$c); echo 'KHONG_CHAN'; } catch (\Illuminate\Validation\ValidationException \$e) { echo 'CHAN_OK: '.implode('',\$e->errors()['extra']??['?']); }
\$dept->max_extra_price_percent = \$old; \$dept->save();
"
```
Expected: `CHAN_OK: Hợp đồng vượt hạn mức Doanh số vượt trội ...` (nếu HĐ có vượt trội > 0.01% base).

- [ ] **Step 4: Checkpoint** (đánh `[x]`, KHÔNG commit)

---

### Task 4.4 — BE: Request validation + Resource fields

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Requests/ContractStoreRequest.php`
- Modify: `hrm-api/Modules/Assign/Http/Requests/ContractUpdateRequest.php`
- Modify: `hrm-api/Modules/Assign/Transformers/DetailContractResource.php`
- Modify: `hrm-api/Modules/Assign/Transformers/ContractResource.php`

**Interfaces — Produces:** payload chấp nhận `line_adjustments[]`; JSON hợp đồng trả `extra_price` (mỗi dòng) + `total_extra_amount` (cấp HĐ).

- [ ] **Step 1: `ContractStoreRequest::rules()` — thêm** (key `source_price_id`):
```php
'line_adjustments'                              => 'sometimes|array',
'line_adjustments.*.source_price_id'            => 'required|integer',
'line_adjustments.*.extra_price'                => 'nullable|numeric|min:0',
'line_adjustments.*.discount_percent'           => 'nullable|numeric|min:0',
'line_adjustments.*.discount_amount'            => 'nullable|numeric|min:0',
'line_adjustments.*.allocated_discount_amount'  => 'nullable|numeric|min:0',
```

- [ ] **Step 2: `ContractUpdateRequest::rules()` — thêm** (key `price_id`):
```php
'line_adjustments'                              => 'sometimes|array',
'line_adjustments.*.price_id'                   => 'required|integer',
'line_adjustments.*.extra_price'                => 'nullable|numeric|min:0',
'line_adjustments.*.discount_percent'           => 'nullable|numeric|min:0',
'line_adjustments.*.discount_amount'            => 'nullable|numeric|min:0',
'line_adjustments.*.allocated_discount_amount'  => 'nullable|numeric|min:0',
```

- [ ] **Step 3: `DetailContractResource` — thêm `extra_price` mỗi dòng product** (chỗ map product, cạnh `quoted_price`):
```php
'extra_price' => (float) ($p->extra_price ?? 0),
```
và **thêm `total_extra_amount` cấp HĐ** (cạnh `total_after_vat`, ~dòng 83):
```php
'total_extra_amount' => (float) ($this->total_extra_amount ?? 0),
```

- [ ] **Step 4: `ContractResource` (list) — thêm** cạnh `total_after_vat`:
```php
'total_extra_amount' => (float) ($this->total_extra_amount ?? 0),
```

- [ ] **Step 5: Verify JSON** — GET 1 hợp đồng, kiểm field.
Run:
```
cd hrm-api && php artisan tinker --execute="
\$c = \Modules\Assign\Entities\Contract\Contract::latest('id')->first();
\$r = (new \Modules\Assign\Transformers\DetailContractResource(\$c->load('products')))->toArray(request());
echo 'has_total_extra='.array_key_exists('total_extra_amount', \$r)?'1':'0';
"
```
Expected: in ra `has_total_extra=1`.

- [ ] **Step 6: Checkpoint** (đánh `[x]`, KHÔNG commit)

---

### Task 4.5 — FE: cột nhập vượt trội/giảm giá trên dòng cha (bảng nhiều cấp)

**Files:**
- Modify: `hrm-client/pages/assign/contracts/_id/edit.vue`

**Interfaces — Produces (methods/computed dùng ở Task 4.6):**
- computed `canEditLines`
- helper `lineExtra(row)`, `lineAfterExtra(row)` (bổ sung; đã có `lineSaleTotal/lineDiscountTotal/lineSaleAfterDiscount/lineVatAmount/lineAfterVat` từ bản trước — `lineSaleAfterDiscount` nay = after_extra − discount).

**Consumes:** `contract.status`, `hasAPermission`, `item.quotation_id`, `discountMethod`, `V2BaseCurrencyInput`.

- [ ] **Step 1: Thêm computed `canEditLines`** (trong `computed`):
```js
canEditLines() {
    if (this.isCreateMode) return !!(this.item && this.item.quotation_id) // Tạo: đã chọn báo giá
    return [2, 3].includes(Number(this.contract && this.contract.status)) && this.hasAPermission('Sửa hợp đồng')
},
```

- [ ] **Step 2: Cập nhật helper tính dòng** — thêm extra vào công thức (sửa `lineSaleAfterDiscount` để trừ sau khi cộng extra):
```js
lineExtra(p) { return (Number(p.extra_price) || 0) * (Number(p.qty_needed) || 0) },
lineAfterExtra(p) { return this.lineSaleTotal(p) + this.lineExtra(p) },
// GG total giữ nguyên (lineDiscountTotal). Sau GG = sau điều chỉnh − giảm giá:
lineSaleAfterDiscount(p) { return this.lineAfterExtra(p) - this.lineDiscountTotal(p) },
// lineVatAmount(p) & lineAfterVat(p): giữ nguyên (đã dựa trên lineSaleAfterDiscount)
```

- [ ] **Step 3: Thêm cột "Vượt trội/đv" + "TT sau điều chỉnh"** vào thead bảng hàng hoá (sau cột "Thành tiền", trước "GG (%)"), và ô nhập ở tbody dòng cha:
```html
<!-- thead: chèn 2 th -->
<th class="text-right" style="min-width: 120px">Vượt trội/đv</th>
<th class="text-right" style="min-width: 130px">TT sau điều chỉnh</th>
```
```html
<!-- tbody dòng cha (v-else, product): chèn 2 td sau cột Thành tiền -->
<td class="text-right">
    <V2BaseCurrencyInput
        v-if="canEditLines && !row.parent_id"
        v-model="row.extra_price" :precision="0" @input="onLineChange" />
    <span v-else>{{ formatMoney(row.extra_price) }}</span>
</td>
<td class="text-right">{{ formatMoney(lineAfterExtra(row)) }}</td>
```
> Ghi chú: **dòng cha** = `row._type==='product' && !row.parent_id` (hàng top-level, không phải hàng con thành phần). Dùng thống nhất điều kiện `!row.parent_id` ở mọi cột nhập + `buildLineAdjustments`. Cập nhật `colspan` dòng nhóm + dòng rỗng (đang 14 → 16).

- [ ] **Step 4: Cho sửa cột Giảm giá trên dòng cha** — cột GG hiện đang read-only; bọc input theo `discountMethod` khi `canEditLines`:
```html
<!-- method 1: GG(%) + GG(₫) -->
<td class="text-right">
    <V2BaseCurrencyInput v-if="canEditLines && !row.parent_id && discountMethod!==2"
        v-model="row.discount_amount" :precision="0" @input="onLineChange" />
    <span v-else>{{ formatMoney(lineDiscountTotal(row)) }}</span>
</td>
```
(method 2: ô `row.allocated_discount_amount`.)

- [ ] **Step 5: `onLineChange()`** — trigger reactivity/tính lại tổng runtime (box tổng ở Task 4.6):
```js
onLineChange() { this.$forceUpdate() },
```

- [ ] **Step 6: Verify runtime** — `cd hrm-client && yarn dev`, mở màn Tạo (chọn báo giá) và màn Sửa: ô nhập hiện trên dòng cha, gõ vượt trội → "TT sau điều chỉnh"/"Thành tiền sau VAT" dòng đổi theo. Dòng con/nhóm không có ô.

- [ ] **Step 7: Checkpoint** (đánh `[x]`, KHÔNG commit)

---

### Task 4.6 — FE: box tổng + gửi `line_adjustments` + xử lý 422

**Files:**
- Modify: `hrm-client/pages/assign/contracts/_id/edit.vue`

**Interfaces — Consumes:** `canEditLines`, `lineExtra`, `lineAfterExtra` (Task 4.5); `moneySummary` (đã có).

- [ ] **Step 1: `moneySummary` — thêm `extra` + `afterExtra`** (ưu tiên cộng từ dòng khi có `lineRows`):
```js
moneySummary() {
    const extra = (this.lineRows || []).filter(r => r._type === 'product' && !r.parent_id)
        .reduce((s, r) => s + this.lineExtra(r), 0)
    const afterVat = Number(this.contract && this.contract.total_after_vat) || 0
    const vat = Number(this.contract && this.contract.total_vat_amount) || 0
    const discount = Number(this.contract && this.contract.total_discount_amount) || 0
    const afterDiscount = afterVat - vat
    const beforeDiscount = afterDiscount + discount - extra   // thành tiền bán gốc (chưa cộng vượt trội)
    return { beforeDiscount, extra, afterExtra: beforeDiscount + extra, discount, afterDiscount, vat, afterVat }
}
```
> Lưu ý: khi đang chỉnh chưa lưu, tổng chuẩn nhất là tính runtime từ dòng — nếu cần realtime tuyệt đối, cộng `lineAfterVat` từ dòng cha thay cho `contract.total_*`. Chọn 1 cách nhất quán khi implement.

- [ ] **Step 2: Box tổng — chèn 2 dòng** (dưới "Thành tiền", trong `.value-summary__body`):
```html
<div class="vs-row" v-if="moneySummary.extra">
    <span class="vs-label">Doanh số vượt trội</span>
    <span class="vs-val" style="color:#0284c7">+ {{ formatMoney(moneySummary.extra) }}</span>
</div>
<div class="vs-row" v-if="moneySummary.extra">
    <span class="vs-label">Thành tiền sau điều chỉnh</span>
    <span class="vs-val">{{ formatMoney(moneySummary.afterExtra) }}</span>
</div>
```

- [ ] **Step 3: Build `line_adjustments` khi lưu** — helper gom dòng cha:
```js
buildLineAdjustments(forCreate) {
    return (this.lineRows || [])
        .filter(r => r._type === 'product' && !r.parent_id)
        .filter(r => Number(r.extra_price) || Number(r.discount_amount) || Number(r.allocated_discount_amount) || Number(r.discount_percent))
        .map(r => ({
            [forCreate ? 'source_price_id' : 'price_id']: r.price_id,
            extra_price: Number(r.extra_price) || 0,
            discount_percent: Number(r.discount_percent) || 0,
            discount_amount: Number(r.discount_amount) || 0,
            allocated_discount_amount: Number(r.allocated_discount_amount) || 0,
        }))
},
```
Trong `save()` (hoặc `buildPayload()`): `payload.line_adjustments = this.buildLineAdjustments(this.isCreateMode)`.

- [ ] **Step 4: Xử lý 422 khi Duyệt** — nơi gọi approve, bắt lỗi hạn mức:
```js
} catch (e) {
    const msg = e?.response?.data?.errors?.extra?.[0] || e?.response?.data?.message
    this.$toasted?.global?.error?.({ message: msg || 'Duyệt thất bại' })
}
```

- [ ] **Step 5: Verify E2E runtime** — `yarn dev`:
  1. Tạo HĐ từ báo giá, nhập vượt trội vài dòng → Lưu → reload thấy tổng gồm vượt trội + box hiển thị "Doanh số vượt trội".
  2. Sửa HĐ, đổi vượt trội → Lưu → tổng cập nhật.
  3. Set `departments.max_extra_price_percent` nhỏ, nhập vượt trội lớn, Duyệt bằng user không "Giám đốc" → toast "Vượt hạn mức... chuyển BGD". Gán role "Giám đốc" → duyệt qua.

- [ ] **Step 6: Checkpoint** (đánh `[x]`, KHÔNG commit)

---

### Phase 4 — Ghi chú thực thi
- Thứ tự phụ thuộc: 4.1 → 4.2 → 4.3 → 4.4 → (4.5, 4.6 FE). 4.5 phải trước 4.6 (4.6 dùng `canEditLines`, `lineExtra`, `lineAfterExtra`).
- Downstream cần rà sau khi xong (không thuộc scope code Phase 4): list/báo cáo hợp đồng nếu hiển thị tổng; in HĐ/Excel nếu có cột tiền.
- Prefix mã tự sinh & các câu hỏi mở Phase 1-3 vẫn giữ nguyên, không đụng ở Phase 4.

### Checkpoint — 2026-08-11 (Phase 4 CODE COMPLETE 6/6, subagent-driven + final review READY TO MERGE)
Vừa hoàn thành: **Phase 4 (Doanh số vượt trội + Giảm giá)** — 6 task qua subagent-driven, review từng task + 1 final whole-branch review (opus).
- 4.1 ✅ 2 migration: `hrm_contract_product_prices.extra_price` (15,2) + `hrm_contracts.total_extra_amount` (18,2). Migrate chạy trên `erp_hrm_check`.
- 4.2 ✅ `ContractService`: `setLineAdjustment` + `recomputeTotals`; áp `line_adjustments` ở store (key `source_price_id` qua productIdMap) + update (key `price_id`). **FIX bổ sung**: recompute ban đầu bỏ dịch vụ+shipping → thêm 2 vòng mirror `QuotationService::computeTotals` (verify HĐ từ BG74 ship 2tr diff=0.00).
- 4.3 ✅ hạn mức: `sumBeforeVat` (Σ dòng cha before_vat) / `currentEmployeeHasRole('Giám đốc')` (model Timesheet\Employee) / `assertExtraWithinLimitOrBgd` gọi đầu `approve()`; đọc `departments.max_extra_price_percent`; null/0/base=0 → không chặn; verify CHAN_OK.
- 4.4 ✅ `ContractStoreRequest` (source_price_id) + `ContractUpdateRequest` (price_id) rule; `DetailContractResource` (extra_price/dòng + total_extra_amount/HĐ) + `ContractResource` (total_extra_amount).
- 4.5+4.6 ✅ (gộp, `edit.vue`+`_id/index.vue`): `canEditLines` (Tạo & Sửa), helper `lineExtra`/`lineAfterExtra`, 2 cột "Vượt trội/đv"+"TT sau điều chỉnh" (16 cột), ô nhập dòng cha (extra + giảm giá theo discountMethod), box tổng +2 dòng, `buildLineAdjustments` (diff theo `_orig`), 422 `errors.extra[0]` ở `handleApprove`.
- **Final review (opus)** tìm C1 (canEditLines dùng `this.contract.status`=undefined→`this.item.status`) + I1 (fetchData thiếu total_vat/discount→box sai) + M2 (discount_percent method1 stale) + M3 (thiếu chặn before_vat<0). **Đã fix cả 4** (assertLinesNonNegative + sửa edit.vue) → re-review READY TO MERGE, không regression.

Đang làm dở: (không) — Phase 4 code xong.
Bước tiếp theo (user):
1. `cd hrm-client && yarn dev` verify runtime: màn Tạo/Sửa hiện ô nhập vượt trội/giảm giá trên dòng cha, cột "TT sau điều chỉnh"/"sau VAT" cập nhật realtime, box tổng có dòng "Doanh số vượt trội", Lưu gửi `line_adjustments`, Duyệt vượt hạn mức hiện toast.
2. Tinker/E2E: tạo HĐ nhập vượt trội → Lưu → tổng đúng (gồm dịch vụ/ship); nhập giảm giá > thành tiền → 422 "giá trị trước VAT âm"; set `departments.max_extra_price_percent` nhỏ → Duyệt bằng user thường bị chặn, role "Giám đốc" qua.
3. Commit gộp Phase 4 (2 repo) khi duyệt.
Blocked: (không).

---

## Phase 5 — Redesign màn Tạo/Sửa HĐ: bố cục 1 cột dọc (bỏ 2 cột main/sidebar)

### Yêu cầu (user 2026-08-12)
Màn `assign/contracts/create` (`_id/edit.vue`) đang layout 2 cột (main trái + sidebar phải). Dàn lại **1 cột dọc từ trên xuống** cho ra dáng hợp đồng thật, **giữ khối Chi tiết hàng hoá (đóng băng)**. Được tự ý gom/sắp lại khối. Mockup đã duyệt (scratch `contract-create-single-column.html`).

### Bố cục chốt (1 cột, 7 khối)
1. **Thông tin chung hợp đồng** — gồm **Báo giá nguồn** (trường đầu) + Số HĐ, Ngày ký, Người duyệt hiệu lực, Ngày hiệu lực, Ngày hết hạn. (Gộp báo giá vào đây thay vì khối lẻ 1 trường.)
2. **Bên A — Công ty** (2 card cạnh nhau với Bên B, xuống 1 cột khi hẹp): pháp nhân + TK công ty (company_name/tax_code/phone/address/account_number/account_name/bank_name/bank_branch).
3. **Bên B — Khách hàng**: customer_name (read-only từ báo giá) + đại diện (representative_name/role) + CCCD (customer_id_card_number/date/place) + TK ngân hàng KH (customer_bank_account_number/bank_name/bank_branch). → **Gom đại diện+CCCD từ Khối A cũ + TK NH KH từ sidebar cũ.**
4. **Chi tiết hàng hoá (từ báo giá — đóng băng)** — **BỎ bảng tóm tắt kv** (mã báo giá/mã HĐ/khách hàng/tổng — đã hiện ở khối khác). Giữ nguyên bảng dòng hàng 16 cột + dịch vụ + box tổng giá trị.
5. **Điều khoản thanh toán** — giữ nguyên (ContractPaymentTermsTable).
6. **Ký hợp đồng** — company_signer_id + company_signer_role.
7. **Đính kèm** — giữ nguyên.
- Thanh hành động cố định dưới (Đóng / Lưu nháp / Trình duyệt) giữ nguyên.

### Việc code (`hrm-client/pages/assign/contracts/_id/edit.vue`)
- [x] Template: bỏ `.contract-grid`/`.contract-main`/`.contract-side` → 1 `.page-content` xếp dọc theo thứ tự trên; bỏ inline `style="order:*"`.
- [x] Gộp báo giá nguồn vào khối Thông tin chung; bỏ khối "Báo giá" lẻ.
- [x] Tách Khối A cũ: giữ lại số HĐ/ngày ở "Thông tin chung"; chuyển đại diện KH + CCCD sang "Bên B".
- [x] Dựng 2 card "Bên A" / "Bên B" cạnh nhau (`.parties-row` grid 1fr 1fr, ≤992px → 1fr).
- [x] Bỏ `<table class="kv">` (tóm tắt) trong khối Chi tiết hàng hoá.
- [x] CSS: bỏ/điều chỉnh `.contract-grid/.contract-main/.contract-side/.side-*`; thêm `.parties-row`.
- [x] Giữ NGUYÊN mọi v-model/logic/collapse/Phase 4 (chỉ đổi vị trí DOM + class).
- [ ] User `yarn dev` verify runtime (không build được ở đây).

### Ràng buộc
- KHÔNG đổi binding/computed/method — chỉ reflow DOM + CSS.
- Giữ collapsible cho các khối đang collapse được (info/a/e/h) nếu vẫn hợp lý; các khối mới (Bên A/B/Ký) có thể để tĩnh như sidebar cũ.

### Checkpoint — 2026-08-12 (Phase 5: reflow 1 cột + restyle card theo mockup)
Vừa hoàn thành: `_id/edit.vue` — (1) bố cục 1 cột 7 khối theo thứ tự HĐ thật; (2) restyle bám mockup đã duyệt: mỗi khối là **card bo góc riêng** (bg trắng, border, shadow) + **header icon vuông** nền tím nhạt (khối chi tiết icon đỏ "đóng băng"); các trường chuyển sang **lưới label-trên** (`.fld-grid` 2/3 cột, `.fld`, `.span2`); thêm **dải note "đóng băng"** đầu trang; Bên A/Bên B là 2 card cạnh nhau. Giữ nguyên toàn bộ v-model/logic/collapse.
- CSS mới: `.c-section` (card), `.section-header > i:first-child` (ô icon), `.sec-frozen`, `.fld-grid/.fld`, `.note-callout`, `.parties-row/.party-card/.party-badge/.ro-value`. CSS cũ `.page-content/.side-*/.form-info-table` thành dead-code (vô hại, chưa dọn).
- Verify: template compile sạch (vue-template-compiler, 0 lỗi). CHƯA chạy runtime.
Đang làm dở: (không).
Bước tiếp theo (user): `yarn dev` mở `assign/contracts/create` xem có khớp mockup chưa; chốt để commit.

### Checkpoint — 2026-08-12 (Phase 5b: prefill Bên A/Bên B khi chọn báo giá)
Vấn đề user: chọn báo giá xong còn quá nhiều ô trống (ERP cũ prefill gần đủ). Nguyên nhân: FE `loadQuotation` không đổ `form`; BE `createFromQuotation` lấy company/khách từ `$data` FE (rỗng).
Xử lý (user chốt 2 default: TK công ty = status=1 đầu tiên; người đại diện = deputy đầu tiên):
- BE: `ContractController@quotationPrefill($id)` + route `GET /assign/contracts/quotation-prefill/{id}`. Đổ: Bên A ← `companies` (name/tax_code/address/phone) + `company_accounts` (account_number/name/bank_name/bank_branch, status=1 đầu tiên); Bên B ← `customers` (identity_card_number, account_number/bank_name/bank_branch) + `customer_deputies` (name→representative_name, role→representative_role). Dùng `DB::table` (bảng ERP-origin trong DB gộp). php -l sạch.
- FE: `loadQuotation` gọi endpoint prefill → merge vào `this.form` (try/catch không chặn). Template compile OK.
- **Bỏ prefill `company_signer_role`**: `companies.deputy_role` là **id** (vd 43) không phải text → để trống nhập tay. Người ký (NV) + ngày ký/hiệu lực/hết hạn vẫn nhập tay.
- Verify data (quotation 77, KH 3021, cty 1): Bên A ra tên/MST/SĐT + TK MB Long Biên; Bên B ra TK VCB + đại diện "ĐÀO VIỆT HÙNG / Giám Đốc". CCCD KH này rỗng (data), sẽ trống — bình thường.
Bước tiếp (user): `yarn dev` chọn báo giá → kiểm tra các ô Bên A/Bên B tự đầy; chỉnh nếu cần rồi lưu.

### Checkpoint — 2026-08-12 (Phase 5c: Số hợp đồng bắt buộc + mã theo logic ERP)
User chốt phương án 1 (giống hệt ERP). Đã sửa:
- BE `Contract::getNextCode($codeInput)`: sinh mã `HĐ_{companies.code}_{departments.code}_{yy}_{STT 4 số}_{code_input}` (STT chạy theo prefix, escape "_" trong LIKE). Thêm import DB.
- BE `ContractService::createFromQuotation`: truyền `code_input` vào getNextCode. `update`: đổi code_input → thay đuôi "_{code_input}" giữ prefix+STT (fallback getNextCode nếu mã cũ không đúng dạng) — mirror ERP.
- BE `ContractStoreRequest` + `ContractUpdateRequest`: `code_input` từ nullable → **required** + message "Vui lòng nhập số hợp đồng".
- FE `edit.vue`: label "Số hợp đồng" thêm `*` đỏ, placeholder "Nhập số hợp đồng", `validateForm` chặn trống + lỗi inline (field-error + V2BaseError).
- Verify: php -l 4 file sạch; template compile OK; ví dụ mã cty 1 = `HĐ_TPE_HN_KD2_26_0001_123-HĐKT`.
Bước tiếp (user): `yarn dev` tạo HĐ → bỏ trống số HĐ bị chặn; nhập → mã sinh đúng format.

### Checkpoint — 2026-08-12 (Phase 5d: mirror field bắt buộc từ HĐ ERP)
User: các field ERP validate bắt buộc → làm tương tự HĐ HRM. Đối chiếu `FirmContractStoreRequest` (ERP), map các field HRM có:
- Thêm bắt buộc (FE `*` đỏ + validateForm chặn + lỗi inline; BE Store+Update `required` + message):
  - `company_signer_id` (Người ký) ← signer_id
  - `company_signer_role` (Chức vụ người ký) ← signer_role_id
  - `company_account_number` (Số TK công ty, Bên A) ← company_account_id
  - `customer_id_card_number` (CCCD KH, Bên B) ← identity_card_number
  - `process_payments` (Điều khoản TT, ≥1 đợt) ← contract_process_payments (BE `required|array|min:1`)
- Đã có sẵn: `quotation_id`, `code_input`, `sign_date`, `effective_date`.
- BỎ (ERP-only, HRM không có model): type, template, template_print_product, contract_type_print, need_install, has_invoice, status, signer regex CCCD.
- Validate chạy cho CẢ Lưu nháp lẫn Trình duyệt (giống ERP bắt buộc lúc store). php -l 4 file sạch; template compile OK.
Bước tiếp (user): yarn dev — bỏ trống 1 trong các field trên → bị chặn + báo đỏ; điền đủ → lưu OK.

### Checkpoint — 2026-08-12 (Phase 5e: điều khoản thanh toán thêm "Loại thanh toán" cho chọn giống ERP)
User: điều kiện thanh toán cho chọn giống HĐ ERP. ERP có cột select `payment_type` (Tạm ứng/Đặt cọc/Thanh toán).
- DB: migration `2026_08_12_000001_add_payment_type...` thêm cột `payment_type` (string 20, nullable) vào `hrm_contract_process_payments`. Đã migrate local erp_hrm_check. **Cần chạy migrate trên server.**
- BE: ContractService (create+update) lưu `payment_type`; Store+Update Request rule `process_payments.*.payment_type => nullable|in:tam_ung,dat_coc,thanh_toan`; DetailContractResource trả `payment_type`. (entity $guarded=[] nên không sửa fillable.)
- FE: `ContractPaymentTermsTable.vue` thêm cột select "Loại thanh toán" (native select: Tạm ứng/Đặt cọc/Thanh toán, sau STT) + addRow default payment_type=null + fix colspan (empty row 7/8, tfoot 4). `edit.vue` buildPayload gửi payment_type (fetch spread ...pp nên tự map lại).
- Nullable (khớp BE ERP), không bắt buộc chọn. php -l + template compile OK.
Bước tiếp (user): chạy migrate trên server; yarn dev kiểm tra cột chọn loại TT lưu/hiển thị đúng.

### Checkpoint — 2026-08-12 (Phase 5f: báo giá click mở chi tiết + popup tìm kiếm giống ERP)
User: (1) báo giá click mở màn chi tiết; (2) đổi ô chọn báo giá thành popup tìm kiếm giống ERP.
- FE mới `pages/assign/contracts/components/ContractQuotationSearchModal.vue`: b-modal theo skill modal-popup (header icon tròn + X, footer Đóng), ô tìm keyword (debounce 300ms) + bảng báo giá trúng thầu (gọi `assign/contracts/selectable-quotations?keyword=`), click dòng → emit `select`.
- `edit.vue`: thay `V2BaseSelect` bằng **chip báo giá** (`<a target=_blank>` mở `/assign/quotations/{id}`) + nút "Chọn/Đổi báo giá" (chỉ khi tạo & chưa khoá) mở modal. Chip hiện ở cả tạo lẫn sửa (trước chỉ hiện khi tạo). Thêm computed `quotationId`, data `showQuotationModal`, method `onPickQuotation`, CSS `.src-quotation-row` + `a.quotation-tag` hover.
- Template compile OK cả 2 file.
Bước tiếp (user): yarn dev — bấm "Chọn báo giá" → popup tìm/chọn; click chip mã báo giá → mở chi tiết tab mới.
