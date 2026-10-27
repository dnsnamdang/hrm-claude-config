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

---

## Phase 6 — HTHT (Hỗ trợ hạch toán) — sát ERP
Spec: `docs/superpowers/specs/2026-08-13-hop-dong-htht-design.md`. Nghiên cứu ERP: 5 báo cáo agent (bóc tách giá / bút toán / approve / cấu hình % / bảng con).

**Chốt brainstorm 2026-08-13:** (B đầy đủ nhưng) chỉ ghi 4 bảng `firm_support_accounting*`, KHÔNG account_details · tái dùng bảng+cấu hình ERP polymorphic · có màn HTHT preview/duyệt · Duyệt=Có hiệu lực (1 bước) · field thiếu → A1 (thêm cột + snapshot lúc tạo HĐ từ product master).

### Phase A — Phòng thực hiện ✅ (xong session 2026-08-13)
- [x] Models `ImplementDepartment`/`ImplementEmployee` (bảng ERP polymorphic).
- [x] `syncImplements` (create+update), `DetailContractResource.resolveImplements`, Request rules.
- [x] FE `ContractImplementSection` (box chính+hỗ trợ ngang, lọc NV theo phòng, tự thêm người lập 100%), màn tạo/sửa/chi tiết.
- [x] Validate 100%/phòng chỉ khi gửi duyệt (Lưu nháp không chặn) — BE `assertImplementsComplete` + FE `validateForm(isSubmit)`.
- [x] Gộp Duyệt = Có hiệu lực (bỏ `activate`/"Xác nhận hiệu lực", quyền 1142).

### Phase B — Bóc tách giá (support_accounting cha) [ ]
- [x] Migration: thêm `sale_max_percent`/`standard_price`/`net_price`/`cost_price` vào `hrm_contract_product_prices` (migrated local).
- [x] Snapshot lúc tạo HĐ: `snapshotProductMasterPrice` tra `product_prices` (erp_product_id + price_type, dòng launch_date mới nhất ≤ nay, status=1) → điền 4 cột. OPEN-ITEM #3 CHỐT: query thẳng DB (dòng trùng = lịch sử giá).
- [x] Bóc tách 4 nhóm gộp trong `getAccountingInfo` (không tách accessor riêng — tính trực tiếp từ dòng hàng, mirror recomputeTotals).
- [x] Models HTHT: `SupportAccounting(+Department/DepartmentDetail/Employee)` trỏ bảng ERP (php -l sạch).
- [x] Service `ContractSupportAccountingService::getAccountingInfo` (bóc tách 4 nhóm, COMPUTED) — verify HĐ 13 đúng VAT/tổng.
- [x] API `GET /assign/contracts/{id}/support-accounting` (preview).
- [ ] FE cột I read-only (bóc tách giá).

### Phase C — Phân bổ phòng/NV theo quy chế [ ]
- [x] `getDepartmentImplement`: implement_* + company_rule_commissions (chia % địa bàn) + regulations match. Gắn vào `getAccountingInfo` (nested).
- [x] `calculate` + `saveDepartment` + `saveDepartmentDetail` — verify HĐ 13 ghi đúng 4 bảng. Migration fix unique composite (gop_db collision).
- [x] `commission_sale` nhánh mới nhất (#4).
- [ ] FE cột III phân bổ phòng/NV.

### Phase D — Màn HTHT + luồng duyệt [ ]
- [x] Màn HTHT `support-accounting.vue`: bóc tách giá + input (nguồn vốn/TNDN/dự phòng/thưởng HĐ/market cost/8 dòng chi phí thực hiện) + phân bổ phòng (quy chế % 4 vai trò + NV).
- [x] `ContractController@approve` nhận payload HTHT → `calculate(true)` + Có hiệu lực.
- [x] Nút chi tiết HĐ "Duyệt" → điều hướng màn HTHT; nút "Hỗ trợ hạch toán" xem sau duyệt; Không duyệt (reject). [Chuyển duyệt/notify: để sau]
- [x] Preview khi chưa chờ duyệt: ẩn action (isPreview).

### Phase E — Verify [ ]
- [ ] E2E + đối chiếu số HTHT với 1 HĐ ERP thật cùng data.

### Open-items cần chốt trước/khi code (xem mục 9 spec)
#1 service item có định mức/giá vốn? · #2 serviceItems→repair_service vs other_cost · #3 nguồn standard/cost trong master · #4 bỏ nhánh commission_sale lịch sử · #5 market_costs nhập tay=0 · #6 cột ma (service_pack/adjust_price/vat_extra) để null.

### Checkpoint — 2026-08-13 (Phase 6 HTHT — BRAINSTORM + SPEC xong, chưa code)
Vừa hoàn thành: nghiên cứu sâu HTHT ERP (5 agent) + chốt 4 quyết định lớn (chỉ 4 bảng không account_details / tái dùng bảng ERP / màn preview-duyệt / A1 snapshot field thiếu) + viết spec đầy đủ `docs/superpowers/specs/2026-08-13-hop-dong-htht-design.md`.
Đang làm dở: (không) — chờ user review spec + chốt 6 open-items.
Bước tiếp theo: user review spec → chốt open-items #1-#4 → bắt đầu Phase B (migration + snapshot + accessor + getAccountingInfo).
Blocked:

### Checkpoint — 2026-08-13 (Phase 6B — nền tảng: migration + models + snapshot)
Vừa hoàn thành: migration 4 cột snapshot (migrated) · 4 model HTHT trỏ bảng ERP · helper `snapshotProductMasterPrice` wire vào `createFromQuotation`. OPEN-ITEM #3 CHỐT = query thẳng `product_prices` (dòng trùng là lịch sử giá → chọn launch_date mới nhất ≤ nay, status=1); sale_max_percent độc lập unit.
Đang làm dở: (không) — nền Phase B xong.
Bước tiếp theo: accessor `Contract` (total_*/discount_rate_*/net_price_*/cost_price) + `ContractSupportAccountingService::getAccountingInfo` (bóc tách 4 nhóm) + API preview `GET /support-accounting` + FE cột I read-only.
Blocked:

### Checkpoint — 2026-08-13 (Phase 6B backend xong — bóc tách giá + API)
Vừa hoàn thành: `ContractSupportAccountingService::getAccountingInfo` (bóc tách 4 nhóm, port ERP phần AUTO) + API `GET /support-accounting` (preview) + commit `299c31d53`. Verify HĐ 13: price_total 1.260.000, VAT 100.800, after_vat 1.360.800 (discount_rate/cost=0 vì HĐ cũ chưa có snapshot).
Đang làm dở: (không) — backend Phase B xong.
Bước tiếp theo: FE cột I (hiển thị bóc tách giá read-only) HOẶC sang Phase C (phân bổ phòng theo regulations + CompanyRuleCommission). Gợi ý: làm Phase C (lõi tính tiền hoa hồng) trước, FE gộp ở Phase D.
Blocked:

### Checkpoint — 2026-08-13 (Phase 6C backend xong — phân bổ phòng/NV/quy chế)
Vừa hoàn thành: port trọn `ContractSupportAccountingService` (getAccountingInfo nested + getDepartmentImplement + getRegulations/getMatchRegulation + getBaseCommissionSale + calculate + saveDepartment + saveDepartmentDetail) ghi 4 bảng firm_support_accounting*. Migration `2026_08_13_000002` đổi unique firm_support_accounting → composite (contractable_id, contractable_type) fix collision ERP↔HRM. Commit `d6d5bea45`. Verify HĐ 13: 2 phòng (50/50) + 4 detail (type1/3) + 2 NV, quy chế khớp reg 133/1. commission_sale=0 do HĐ 13 chưa có standard_price snapshot (HĐ mới sẽ có).
Đang làm dở: (không) — backend Phase B+C xong.
Bước tiếp theo: Phase D — màn HTHT FE (cột I/II/III + input) + tích hợp luồng duyệt (approve nhận payload HTHT → calculate + Có hiệu lực; nút Duyệt điều hướng màn HTHT; Chuyển duyệt/Không duyệt). Trước đó nên tạo 1 HĐ mới (có snapshot) để verify commission_sale ra số.
Blocked:

### Checkpoint — 2026-08-13 (Phase 6D xong — màn HTHT + luồng duyệt)
Vừa hoàn thành: BE approve nhận payload HTHT → calculate(true) + Có hiệu lực (commit df727cde2); FE màn `support-accounting.vue` (bóc tách giá + input + phân bổ phòng, preview/duyệt) + nút chi tiết HĐ điều hướng (commit efcf7de37). Nuxt auto-route /assign/contracts/:id/support-accounting.
Đang làm dở: (không) — Phase B/C/D code xong.
Bước tiếp theo (Phase E + user): (1) user `yarn dev` mở màn HTHT xem giao diện + luồng Duyệt; (2) tạo 1 HĐ MỚI (có snapshot standard_price) để verify commission_sale ra số ≠ 0; (3) đối chiếu vài số với HĐ ERP thật. Các mục để sau: Chuyển duyệt (BGD), notify, FE cho phép sửa % phòng (v1 đang dùng % quy chế mặc định), KQKD dự kiến tính live.
Blocked:

### Phase 6E — Sửa logic HTHT theo spec Excel (1.HTHT 20-1-2025) + JS ERP [ ]
Nghiên cứu file Excel spec + JS `FirmSupportAccounting.blade.php`. Phát hiện: `market_costs` (biến ERP) = **"Thưởng NVKD"** (label) = HRM `sales_bonus` (xác nhận qua `payment-info.blade.php` bind Thưởng NVKD → form.market_costs).
- [x] Snapshot standard_price = min(sau giảm, net) × G × H + fallback cost_price.
- [x] total_market_costs = sales_bonus (mục 12 = Thưởng NVKD, xác nhận biến market_costs = label Thưởng NVKD).
- [x] 14.1 auto-tính có trần; discount_tndn mặc định config; exec += employee_commission (reorder).
- [x] FE: mục 12 = sales_bonus (đã có); thêm 4.1 Thưởng năng suất; không có ô market chết.
- [x] Verify HĐ 15 (từ BG77): DS tiêu chuẩn 52.516.352, gross 30.96tr, eff 94.03% — khớp công thức.

### Checkpoint — 2026-08-14 (Phase 6E — sửa logic HTHT theo spec Excel, verify khớp)
Vừa hoàn thành: đối chiếu file Excel spec (1.HTHT 20-1-2025) 3 tab + JS FirmSupportAccounting → phát hiện & sửa: (1) market_costs = Thưởng NVKD (sales_bonus); (2) standard_price mục 18 = min(sau giảm,net)×G×H; (3) 14.1 auto-tính có trần; (4) discount_tndn mặc định config; (5) exec += employee_commission. Commit a3c1812ea (BE) + 65a55e982 (FE). Verify HĐ 15 từ BG-2026-00077 khớp công thức (DS tiêu chuẩn 52.516.352, gross 30.96tr, eff 94.03%). Tạo data test: BG-2026-00077 (created_by=13), HĐ 15.
Đang làm dở: (không).
Bước tiếp theo (user): yarn dev mở màn HTHT HĐ 15 xem số 3 cột khớp. Còn lại: verify đối chiếu 1 HĐ ERP thật; 2 hệ số G/H cần cấu hình đúng company_price_types/company_product_types theo từng công ty.
Blocked:

### Phase 7 — Vòng đời HĐ (từ spec LOGIC HỢP ĐỒNG) [ ]
Chốt: làm Mục 3 (hiệu lực & thời hạn thực hiện) trước; Mục 4 (duyệt đa cấp) bỏ qua (chưa có config tổng công ty); Mục 7 (cảnh báo) chưa làm.

#### 7.3 — Điều kiện hiệu lực + Thời hạn thực hiện HĐ [x] (2026-08-14)
- [x] Migration hrm_contracts: effective_condition (1 ký/2 đặt cọc/3 bảo lãnh), guarantee_approved_date, execution_deadline_days, execution_deadline_base (1 hiệu lực/2 mặt bằng/3 childpart/4 chốt TK), execution_base_date, execution_end_date.
- [x] Logic tính effective_date theo điều kiện: 1=sign_date, 2=ngày đặt cọc lần đầu (min account_details phiếu thu/báo có/điều chỉnh của HĐ), 3=guarantee_approved_date.
- [x] execution_end_date = base_date (hiệu lực nếu base=1, else execution_base_date) + days. Accessor can_export (chưa hiệu lực HOẶC chưa có thời hạn → false).
- [x] Request rules + Resource trả field. FE form tạo/sửa + chi tiết: select điều kiện + thời hạn + auto hiển thị ngày hiệu lực.

#### 8 — Gỡ gate quyền "Lập hợp đồng" cho khớp ERP [x] (2026-09-17)
Bối cảnh: user phát hiện `/assign/contracts` không có nút "Tạo hợp đồng" do gate quyền. Điều tra ERP
(agent) xác nhận **ERP KHÔNG yêu cầu quyền để lập HĐ hãng** (chỉ gate ở khâu DUYỆT). User chốt hướng
**A — khớp ERP hoàn toàn**: gỡ hết gate quyền `Lập hợp đồng` ở đường TẠO (giữ nguyên gate Sửa/Xóa/Duyệt).
- [x] FE nút "Tạo hợp đồng" màn danh sách: bỏ `v-if="hasAPermission('Lập hợp đồng')"` (`pages/assign/contracts/index.vue:60`).
- [x] FE nút "Lập hợp đồng" màn báo giá: bỏ `hasAPermission('Lập hợp đồng')` trong computed `canCreateContract`, giữ điều kiện nghiệp vụ (status=7 trúng thầu + chưa có HĐ + chỉ người lập) (`pages/assign/quotations/_id/index.vue:1064`).
- [x] BE route store: gỡ `->middleware('checkPermission:Lập hợp đồng')` (`Modules/Assign/Routes/api.php:758`).
- [x] BE controller store: gỡ block `isCurrentEmployeeHasPermission('Lập hợp đồng')` (defense-in-depth), giữ check "chỉ người lập báo giá" (`Api/V1/ContractController.php:319`).
- [x] Rà quét sạch: FE grep `hasAPermission('Lập hợp đồng')` rỗng; BE không còn enforce. Quyền id 1137 để nguyên trong seeder (định nghĩa nhưng không enforce — giống ERP giữ id 40 "Thêm hợp đồng"). Luồng "Lập hợp đồng DỊCH VỤ" (CustomerCare) là quyền/nghiệp vụ khác — KHÔNG đụng.
- [ ] Verify: đăng nhập tài khoản KHÔNG có quyền 1137 → nút "Tạo hợp đồng" hiện; tạo & lưu HĐ không bị 403.

### Checkpoint — 2026-09-17 (Phase 8 — gỡ gate quyền lập HĐ khớp ERP)
Vừa hoàn thành: gỡ 4 gate quyền `Lập hợp đồng` ở đường TẠO (2 FE nút + BE route middleware + BE controller check), giữ nguyên gate Sửa/Xóa/Duyệt và các điều kiện nghiệp vụ (trúng thầu, chỉ người lập). `php -l` sạch controller + route. Nhánh: `gop_db` (cả hrm-api & hrm-client).
Đang làm dở: (không).
Bước tiếp theo (user): bấm thật màn `/assign/contracts` — nút "Tạo hợp đồng" phải hiện, lập & lưu HĐ không 403.
Blocked: (không)

#### 9 — Bỏ bắt buộc "Ngày ký" ở form Tạo/Sửa HĐ [x] (2026-10-14)
Bối cảnh: user báo "Ngày ký hiển thị theo dữ liệu khi Xác nhận KH đã ký >> Form Tạo không thể bắt buộc nhập trường này". Ngày ký chỉ được điền khi xác nhận KH đã ký (chưa có luồng này ở HRM) → form Tạo/Sửa KHÔNG được bắt buộc.
- [x] FE `pages/assign/contracts/_id/edit.vue`: gỡ dấu `*` nhãn "Ngày ký" (dòng ~49), bỏ wrapper `field-error` + `V2BaseError` cho ô này, giữ nguyên `V2BaseDatePicker` để vẫn nhập tay được.
- [x] FE `validateForm()`: gỡ dòng `if (!this.form.sign_date) errs.sign_date = 'Vui lòng nhập ngày ký'` (~dòng 1111).
- [x] BE `ContractStoreRequest`: `sign_date` `required|date` → `nullable|date`, gỡ message `sign_date.required`.
- [x] BE `ContractUpdateRequest`: `sign_date` `required|date` → `nullable|date`, gỡ message `sign_date.required`.
- [x] An toàn null: `ContractService::recomputeEffectiveDates()` đã xử lý `sign_date` null (effective_date = null khi điều kiện = Kể từ ngày ký) — không vỡ.
- [x] Verify Playwright `/assign/contracts/create?quotation_id=74`: nhãn "Ngày ký" không còn `*`; bấm "Trình duyệt" khi ô trống → KHÔNG hiện lỗi "Vui lòng nhập ngày ký". `php -l` sạch 2 FormRequest.

#### 10 — Tài khoản ngân hàng Bên A: dropdown chọn như FirmContract ERP [x] (2026-10-14)
Bối cảnh: user (chuyển lời chị) — "Tài khoản ngân hàng Bên A hiện PM tự hiển thị, không biết lấy cái nào". Ảnh chú thích đỏ: "phải để CHỌN tài khoản như logic cũ, KHÔNG hiển thị mặc định". User chốt: logic cũ = **HĐ hãng FirmContract bên ERP**. Điều tra: ERP Bên A = **dropdown chọn `company_account_id`** (nguồn `company_accounts` lọc theo `company_id`, KHÔNG auto-chọn mặc định), lưu snapshot 4 cột text từ account được chọn (`FirmContractService.php:458-462`). Cả ERP lẫn HRM **đều không có** khái niệm "tài khoản theo quy chế của phòng" → bỏ ý "default theo phòng". Hiện HRM auto-điền tài khoản `orderBy('id')->first()` (`ContractController::quotationPrefill`).
Chốt với user: (1) dropdown chọn, KHÔNG mặc định; (2) **chuẩn ERP** — thêm cột FK `company_account_id` + snapshot.
- [x] BE Migration `hrm_contracts`: thêm `company_account_id` unsignedBigInteger nullable (guard hasColumn).
- [x] BE `Contract` model: thêm relation `company_account()` belongsTo CompanyAccount.
- [x] BE `ContractStoreRequest`/`ContractUpdateRequest`: thêm `company_account_id => required|exists:company_accounts,id`; `company_account_number` → nullable (suy từ account); đổi message required sang company_account_id.
- [x] BE `ContractService` store+update: set `company_account_id` + snapshot 4 cột (account_number/name/bank_name/bank_branch) từ `CompanyAccount::find($company_account_id)` (giống FirmContract ERP), chống lệch FE.
- [x] BE `ContractController::quotationPrefill`: BỎ prefill 4 cột company_account_* (không auto-chọn tài khoản nữa); giữ company info + Bên B.
- [x] BE endpoint mới `GET /assign/contracts/company-accounts`: trả danh sách company_accounts status=1 theo company người lập (+ include id đang chọn khi sửa), kèm currency để dựng nhãn.
- [x] FE `edit.vue`: thay 4 ô text Bên A bằng 1 `V2BaseSelect` "Tài khoản ngân hàng *" (`form.company_account_id`), nhãn option giống ERP `<số TK> - <loại tiền> tại <ngân hàng> chi nhánh <chi nhánh> - <tên TK>`; onChange đổ snapshot 4 cột; fetch options ở mounted (cả tạo & sửa); edit set company_account_id từ detail; validateForm bắt buộc company_account_id thay company_account_number.
- [x] BE `DetailContractResource`: trả `company_account_id`.
- [x] Verify Playwright: dropdown hiện danh sách tài khoản, không chọn sẵn; chọn → lưu OK; sửa → reselect đúng tài khoản đã lưu.

## Phase 11 — Bổ sung 6 trường FirmContract còn thiếu trên màn HĐ (mục 1, 2a/b/c, 5, 6) [ ]

> Spec: `.plans/hop-dong/design-phase11-firm-fields.md`. Nhánh `gop_db` (hrm-api + hrm-client).
> Để lại mục 3 (giao hàng + tiến độ TT #11252) và mục 4 (điều kiện thời gian thực hiện).
> **Ràng buộc chung** (áp mọi task): ERP = Laravel 6 nhưng HRM = Laravel 8/PHP7.4 — KHÔNG `?->`.
> DB gộp `erp_hrm_check`: KHÔNG FK cứng, bảng trùng ưu tiên bản ERP. Màn edit.vue là **màn CŨ**:
> bám pattern `touched`/`formError`/`validateForm()`/`.fld-grid`/`.c-section`, dropdown dùng
> `V2BaseSelect` (như Bên A). Số quốc tế. Đỏ chỉ cho lỗi validate. KHÔNG tự sửa giá trị user nhập.
> Cột mới vào `hrm_contracts`: `customer_type`, `customer_deputy_id`, `customer_account_id`,
> `need_install` (tái dùng `representative_role` cho chức vụ đại diện — KHÔNG thêm `deputy_role`).

### Review Focus (kiểm riêng — spec ngụ ý nhưng dễ vỡ)
- [ ] Khách **tổ chức không có bản ghi `customer_deputies`** → dropdown rỗng → validate "required" chặn đúng khi chính thức (Task 11.6 + 11.9).
- [x] **HĐ cũ chưa có `customer_type` snapshot** (2 dòng test) → Resource suy live → FE vẫn rẽ nhánh đúng (Task 11.7 + 11.8).
- [x] **Đổi ẩn/hiện ô định danh theo loại khách** → lỗi cũ không bám ô đang ẩn; tổ chức không gửi/không validate `customer_id_card_number` (Task 11.9 + 11.12).
- [x] Khách chỉ **1 tài khoản NH** → dropdown tự chọn; khách **0 tài khoản** → `customer_account_id` nullable, không chặn (Task 11.10).
- [x] `need_install` **null ở HĐ cũ** → khi Sửa bắt buộc chọn trước khi lưu chính thức (Task 11.11 + 11.12).

### Task 11.1 — Migration thêm 4 cột `hrm_contracts` [x]
**File:** Create `hrm-api/Modules/Assign/Database/Migrations/2026_10_14_000002_add_firm_fields_to_hrm_contracts_table.php`
- [x] Viết migration: guard `Schema::hasColumn` từng cột; thêm `customer_type` unsignedTinyInteger nullable, `customer_deputy_id` unsignedBigInteger nullable, `customer_account_id` unsignedBigInteger nullable, `need_install` unsignedTinyInteger nullable. PHPDoc trên `up()`/`down()`. `down()` drop 4 cột (guard hasColumn).
- [x] Chạy: `cd hrm-api && php artisan migrate` — kiểm `.env` DB trỏ `erp_hrm_check` trước khi chạy.
- [x] Verify: `SHOW COLUMNS FROM hrm_contracts LIKE 'customer_type'` (và 3 cột còn lại) có kết quả.

### Task 11.2 — Model `Contract` + xác định nguồn deputy/bank [x]
**File:** Modify `hrm-api/Modules/Assign/Entities/Contract/Contract.php`
- [x] Grep tìm model sẵn có: `grep -rln "customer_deputies\|customer_has_bank_accounts" hrm-api/app hrm-api/Modules` → xác định class `CustomerDeputy` / `CustomerHasBankAccount` (ERP có `CustomerHasBankAccount::getCustomerAccounts()`). Nếu có model → thêm 2 belongsTo `customerDeputy('customer_deputy_id')`, `customerAccount('customer_account_id')` (khuôn `company_account()` Phase 10). Nếu không có model phù hợp → bỏ qua relation, Service dùng `DB::table('customer_deputies')` / `DB::table('customer_has_bank_accounts')`.
- [x] `php -l Contract.php` sạch.

### Task 11.3 — 2 endpoint danh sách deputy + bank account [x]
**File:** Modify `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ContractController.php` (khuôn `companyAccounts()`) + `hrm-api/Modules/Assign/Routes/api.php`
- [x] Method `customerDeputies(Request $r)`: validate `customer_id`; trả `DB::table('customer_deputies')->where('customer_id',$id)->orderBy('name')->get(['id','name','role'])`.
- [x] Method `customerBankAccounts(Request $r)`: trả `customer_has_bank_accounts` theo `customer_id` → `['id','account_number','account_name','bank_name','bank_branch']`.
- [x] Route `GET assign/contracts/customer-deputies` + `GET assign/contracts/customer-bank-accounts` cạnh `company-accounts` (chỉ đọc, không middleware quyền).
- [x] Verify: `php artisan route:list | grep customer-deputies` thấy route; gọi thử tinker/curl 1 customer_id ra mảng.

### Task 11.4 — `ContractService::store()` snapshot mới [x]
**File:** Modify `hrm-api/Modules/Assign/Services/ContractService.php` (mảng snapshot khách ~103-118 + trường riêng HĐ ~142-153)
- [x] Sau snapshot từ `$quotation`: thêm `customer_type` = `Customer::find($quotation->customer_id)` → `$cus ? $cus->customer_type : null` (biến tạm, không `?->`); `customer_email` best-effort (`$cus->email` ?: contact đầu tiên).
- [x] `customer_deputy_id` = `$data['customer_deputy_id'] ?? null`; nếu có → `$dep = DB::table('customer_deputies')->find(...)`, ghi đè `representative_name`=`$dep->name`, `representative_role`=`$dep->role`. Không có → giữ `representative_name/role` từ `$data`.
- [x] TK bên B: `$cusAcc = DB::table('customer_has_bank_accounts')->find($data['customer_account_id'] ?? 0)`; set `customer_account_id` + snapshot `customer_bank_account_number`=`$cusAcc->account_number`, `customer_bank_name`=`$cusAcc->bank_name`, `customer_bank_branch`=`$cusAcc->bank_branch` (fallback `$data` nếu rỗng — khuôn Bên A).
- [x] `need_install` = `$data['need_install'] ?? null`.
- [x] Định danh: nếu tổ chức (`customer_type`>1) → `customer_id_card_number/date/place` = null (MST đã ở `customer_tax_code`); cá nhân → giữ từ `$data`.
- [x] `php -l` sạch.

### Task 11.5 — `ContractService::update()` áp cùng logic [x]
**File:** Modify `ContractService.php` (~334-362)
- [x] Lặp lại set `customer_deputy_id`+representative snapshot, `customer_account_id`+bank snapshot, `need_install`, định danh theo type (dùng helper riêng nếu trùng nhiều với store để DRY).
- [x] Guard HĐ cũ: nếu `$contract->customer_type` null → set lại từ `customers` theo `$contract->customer_id`.
- [x] `php -l` sạch.

### Task 11.6 — Validation 2 FormRequest (required có điều kiện) [x]
**File:** Modify `hrm-api/Modules/Assign/Http/Requests/Contract/ContractStoreRequest.php` + `ContractUpdateRequest.php`
- [x] Tính `$isOrg` (tra `customers.customer_type` theo customer_id của báo giá/HĐ) + `$official` (theo status). `customer_deputy_id`: required khi `$isOrg && $official`, nullable khác; `exists:customer_deputies,id` khi có. `customer_account_id`: nullable + `exists:customer_has_bank_accounts,id` khi có. `need_install`: `required|in:0,1` khi `$official`, nullable khi nháp. `customer_id_card_number`: required khi `!$isOrg && $official`, nullable khác.
- [x] KHÔNG khai `messages()` cho rule phổ biến (lang file đã có). Rethrow `ValidationException`.
- [x] Verify BE trực tiếp: POST payload tổ chức thiếu `customer_deputy_id` (status chính thức) → 422 `customer_deputy_id`; payload cá nhân thiếu CCCD → 422; payload thiếu `need_install` → 422. `php -l` sạch 2 file.

### Task 11.7 — `DetailContractResource` trả field mới [x]
**File:** Modify `hrm-api/Modules/Assign/Transformers/DetailContractResource.php`
- [x] Trả thêm: `customer_type` (snapshot ?: suy live từ quan hệ customer), `customer_deputy_id`, `need_install`, `price_type_name` (từ `price_types` theo `price_type_id`), `customer_email`, `customer_contact_name`, `customer_contact_phone`, `customer_address`, `customer_tax_code`.
- [x] Verify: mở detail 1 HĐ qua API thấy đủ field, `customer_type` ≠ null kể cả HĐ cũ.

### Task 11.8 — FE: Bảng giá read-only + khai `data()` [x]
**File:** Modify `hrm-client/pages/assign/contracts/_id/edit.vue`
- [x] `data().form` thêm: `customer_type`, `customer_deputy_id`, `customer_account_id`, `need_install`, `price_type_name`, `customer_contact_name`, `customer_contact_phone`, `customer_email`, `customer_tax_code`, `customer_address`. Thêm state `customerDeputyOptions:[]`, `customerBankOptions:[]`.
- [x] Computed `isOrganization()` = `Number(this.form.customer_type || this.contract.customer_type) > 1`.
- [x] Khối "Thông tin chung": thêm 1 `.fld` read-only "Bảng giá" hiển thị `form.price_type_name` (kiểu `.ro-value` như ô Tên khách hàng dòng 106). Không vào payload.

### Task 11.9 — FE: Bên B rẽ nhánh cá nhân/tổ chức [x]
**File:** Modify `edit.vue` (template Bên B 102-121)
- [x] Người đại diện: `v-if="isOrganization"` → `V2BaseSelect` "Người đại diện *" (`form.customer_deputy_id`, `:options="customerDeputyOptions"`) + `@change` đổ `representative_name`=dep.name, `representative_role`=dep.role; ô Chức vụ disabled. `v-else` → giữ 2 ô free-text `representative_name`/`representative_role`.
- [x] Ô định danh: `v-if="!isOrganization"` → "CCCD/CMND *" (`customer_id_card_number` required) + Ngày/Nơi cấp (giữ 110-115). `v-else` → "Mã số thuế" read-only từ `customer_tax_code`, ẩn ngày/nơi cấp, không `req`.
- [x] Khối Liên hệ `v-if="isOrganization"`: 3 ô read-only `customer_contact_name`, `customer_contact_phone`, `customer_email` (`.ro-value`/`disabled`, chữ xám).

### Task 11.10 — FE: TK ngân hàng Bên B thành dropdown [x]
**File:** Modify `edit.vue` (116-118)
- [x] Thay 3 ô text → 1 `V2BaseSelect` "Số tài khoản" (`form.customer_account_id`, `:options="customerBankOptions"`); nhãn option `<account_number> - <bank_name> chi nhánh <bank_branch> - <account_name>`; `@change` đổ `customer_bank_account_number/name/branch`; 3 ô tên TK/NH/chi nhánh hiển thị disabled (tự fill). 1 TK → tự chọn.

### Task 11.11 — FE: Địa chỉ giao hàng + Lắp đặt [x]
**File:** Modify `edit.vue`
- [x] "Địa chỉ giao hàng": `.fld` read-only từ `form.customer_address` (`.ro-value`/disabled).
- [x] "Lắp đặt": 2 radio Có(1)/Không(0) `form.need_install` bắt buộc; bọc `field-error` + `V2BaseError` khi `touched && formError.need_install`. Dùng `V2BaseRadio` nếu màn có sẵn, else radio theo pattern local.

### Task 11.12 — FE: validate + buildPayload + edit-set + fetch options [x]
**File:** Modify `edit.vue` (`validateForm` 1140, `buildPayload` 1199, edit-set 1086-1094, mounted)
- [x] `validateForm()`: tổ chức → bắt buộc `customer_deputy_id`, bỏ bắt buộc `customer_id_card_number`; cá nhân → giữ `customer_id_card_number` (1149). Luôn bắt buộc `need_install` (phải 0/1). Giữ `company_account_id`.
- [x] Đổi `isOrganization` → xoá lỗi field ẩn (`delete this.formError.customer_id_card_number` / `customer_deputy_id`).
- [x] `buildPayload()` thêm `customer_deputy_id`, `customer_account_id`, `need_install`; cá nhân gửi `customer_id_card_*`, tổ chức không gửi. Không gửi `price_type_id`.
- [x] Edit-set (1086-1094): set `customer_type`, `customer_deputy_id`, `customer_account_id`, `need_install`, các field hiển thị MST/liên hệ/địa chỉ/price_type_name.
- [x] `mounted`/sau khi có `customer_id`: fetch customer-deputies + customer-bank-accounts (chỉ khi có customer_id); reselect đúng khi Sửa.
- [x] Sau lưu: `markFormSaved()` + `$router.push('/assign/contracts')`.

### Task 11.13 — Verify Playwright 2 loại khách + php -l [x]
- [x] Mở `http://127.0.0.1:3000` (KHÔNG localhost). HĐ **cá nhân**: ô "CCCD/CMND *" required + ngày/nơi cấp; không có dropdown Người đại diện, không có khối Liên hệ.
- [x] HĐ **tổ chức**: ô "Mã số thuế" read-only KHÔNG báo đỏ khi trống; dropdown Người đại diện bắt buộc + chức vụ tự fill; khối Liên hệ read-only.
- [x] Bảng giá read-only đúng tên; TK bên B dropdown nạp + chọn tự fill + lưu OK + Sửa reselect; Địa chỉ giao hàng read-only đúng; Lắp đặt radio bắt buộc (bấm Trình duyệt khi trống → đỏ).
- [x] Lưu 2 loại khách không mất dữ liệu; mở lại Sửa đúng giá trị. `php -l` sạch toàn bộ file BE. `rm -rf /Users/nguyentrancu/DEV/code/ERP-HRM/.playwright-mcp`.

### Checkpoint — 2026-10-14 (Phase 11 — PLAN xong, chưa code)
Vừa hoàn thành: brainstorming (duyệt design) + spec `design-phase11-firm-fields.md` + plan 13 task.
Đang làm dở: (không).
Bước tiếp theo: user chọn execution method → bắt đầu Task 11.1 (migration).
Blocked: (không).

### Checkpoint — 2026-10-15 (Phase 11 — CODE XONG, review + fix xong, CHƯA commit)
Vừa hoàn thành: toàn bộ 13 task Phase 11 (Native execution). BE: migration 4 cột + Contract entity 2 belongsTo + 2 endpoint deputy/bank + ContractService resolveCustomerFirmFields (store/update) + 2 FormRequest required-có-điều-kiện + DetailContractResource. FE: edit.vue rẽ nhánh cá nhân/tổ chức, Bảng giá read-only, TK Bên B dropdown, địa chỉ giao hàng read-only, need_install radio, validate/buildPayload/fetch options. Verify Playwright 2 loại khách PASS. Final review: 2 opus reviewer (api+client) → fix 3 Important (api#1 IDOR scope exists theo customer_id; api#2 deputy null cho cá nhân; api#3+client#1 snapshot-first customer_type), verify curl PASS; 3 minor deferred.
Đang làm dở: (không).
Bước tiếp theo: CHỜ user yêu cầu commit/push (CLAUDE.md: không tự commit). Chưa commit cả 2 repo.
Blocked: (không).

## Phase 12 — Fix hiển thị cha-con bảng dòng hàng màn Chi tiết HĐ (@dangquang)

**Bug (screenshot user):** màn `/assign/contracts/{id}` bảng "Thiết bị chính" hiển thị dòng con
(`parent_id` ≠ null) **trông ngang cấp** với dòng cha. Điều tra: DB remote `hrm_erp_test` HĐ id=1
dòng 4,5 ĐÃ có `parent_id=3` (data ĐÚNG, không phải bug tạo-từ-báo-giá). Nguyên nhân thật =
**render FE**: `buildLineRows` đánh STT **tuần tự** cho cả con (…3,4,5) + tên con chỉ thụt **16px**
→ con trông như mục top-level. Màn **báo giá** (`pages/assign/quotations/_id/index.vue`) đã có
pattern cha-con chuẩn: STT con = `{cha}.{con}` ("3.1","3.2"), tên con thụt `pl-4`=24px, dòng con
`.child-row td { color:#555; font-weight:300 }`. CLAUDE.md bắt buộc copy pattern có sẵn → đồng bộ
màn Chi tiết HĐ theo báo giá. Fix này đúng cho cả 2 khả năng (deploy remote cũ / indent 16px mờ).

### Task 12.1 — FE: STT phân cấp + indent + style dòng con [x]
**File:** Modify `pages/assign/contracts/_id/index.vue`
- [x] `buildLineRows` (`pushProductRows`): thêm tham số `parentStt`. Top-level giữ đếm global `stt` (1,2,3…); con → `_stt = parentStt + '.' + childSeq` (3.1, 3.2; đệ quy → 3.1.1). Gắn cờ `_isChild`.
- [x] Template dòng product: STT con thêm class xám `.line-child-stt` (`#6b7280`, KHÔNG dùng `.text-muted` vì trong hrm-client là ĐỎ); tên thụt `row._level * 24` (thay 16, cả dòng group); `<tr>` con gắn `.line-child-row`.
- [x] CSS: `.line-table .line-child-row td { color:#555; font-weight:300 }` + `.line-table .line-child-stt { color:#6b7280 }` (copy từ báo giá nhưng STT xám thay vì đỏ).

### Task 12.2 — Verify Playwright HĐ có dòng con + dọn screenshot [x]
- [x] Mở `http://127.0.0.1:3000/assign/contracts/15` (HĐ 15 có dòng con "Linh kiện con test" parent_id). DOM + ảnh xác nhận: STT con = "1.1" (cờ `line-child-stt`), tên thụt 24px, dòng con chữ #555; dòng cha "1","2","3" pad 0px đen. Phân cấp rõ ràng.
- [x] Dọn screenshot MÌNH tạo (`local-contract15-lines.png` + thư mục `.playwright-mcp/` root), 4 png tracked trong `hrm-client/.playwright-mcp/` giữ nguyên.

### Checkpoint — 2026-10-15 (Phase 12 — CODE + VERIFY XONG, CHƯA commit)
Vừa hoàn thành: fix hiển thị cha-con bảng dòng hàng màn Chi tiết HĐ (`contracts/_id/index.vue`). STT con phân cấp "{cha}.{con}", indent 24px (cả group), dòng con chữ #555 + STT xám #6b7280 — đồng bộ pattern màn Báo giá. Verify Playwright HĐ 15 PASS (DOM + ảnh). Chẩn đoán: data DB remote ĐÚNG (parent_id set đủ), bug thuần ở render FE (STT tuần tự + indent 16px mờ).
Đang làm dở: (không).
Bước tiếp theo: CHỜ user yêu cầu commit/push. 1 file FE chưa commit (`contracts/_id/index.vue`) + 2 file task Khách hàng Phase cũ vẫn chưa commit.
Blocked: (không).

## Phase 13 — Fix DSTC (Doanh số tiêu chuẩn) = 0 ở màn HTHT HĐ (@dangquang)

**Bug (screenshot user):** màn Hỗ trợ hạch toán `HĐ_TPE_HN_KD1_26_0001_HD853` mục 18 "Doanh số
tiêu chuẩn" = 0 (kéo theo mục 19 = 0), trong khi mục 17 "Tổng HĐ thu về" = 140,197,000 đúng.

**Chẩn đoán (đã xác minh DB remote `hrm_erp_test`):**
- DSTC = Σ `standard_price × qty` (dòng SP cha, `getBaseCommissionSale` dòng 342-352). `standard_price`
  được freeze lúc tạo HĐ bởi `ContractService::snapshotProductMasterPrice()` (dòng 704-746).
- ERP (`FirmContractService.php:702-757`) tính `standard_price` = `min(giá sau giảm, net) × G × H`,
  `net = quoted − quoted×sale_max/100`; **`sale_max_percent` lấy từ `product_unit_prices`** (qua
  `Product::getPriceByUnitAndType` → `product_units` theo product_id+unit_id, rồi `product_unit_prices`
  theo product_unit_id+price_type_id). Khi KHÔNG có dòng giá → `firstOrFail` ném → catch → `sale_max=0`
  nhưng **vẫn tính** standard_price.
- HRM **port đúng công thức** nhưng đọc `sale_max_percent` từ bảng **legacy `product_prices`** (khóa
  `product_id`). Bảng này gộp DB chỉ còn SP cũ (product_id 3895–8527); 8 dòng SP của HĐ đều >31000 →
  không có dòng → HRM `return` SỚM → `standard_price` NULL cả 8 dòng → DSTC=0. **Đây là lỗi port
  (sai nguồn đọc + return sớm).**
- `snapshotProductMasterPrice` chỉ gọi lúc store (dòng 286), KHÔNG gọi lúc update → sửa HĐ không re-freeze.

**Quyết định chốt với user (2026-10-15):**
1. **cost_price "khớp ERP":** ERP `firm_contract_tab_products` KHÔNG có cột cost; ERP đọc giá vốn ở
   cấp HĐ (`$contract->cost_price`, từ recipe) không ở dòng. **Ruling:** vẫn freeze `cost_price` theo
   dòng nhưng đổi nguồn sang `product_units.cost_price` (hậu duệ gop_db của `product_prices.recipe_price`
   đã rỗng, nằm sẵn trong join) để lãi gộp HTHT (ContractSupportAccountingService:54,105,435) có giá
   vốn THẬT — khớp màn HTHT ERP hiển thị giá vốn thật, thay vì để 0 (lãi gộp bị thổi phồng). DSTC
   KHÔNG phụ thuộc cost_price. Nếu user muốn để NULL thuần → chỉ gỡ 1 dòng gán cost_price.
2. **Không backfill** HĐ cũ (user chốt).
3. **Gọi re-freeze cả khi update** (user chốt) → HĐ "Chờ duyệt" chỉ cần Không duyệt → Sửa → Lưu là
   tự tính lại DSTC đúng, không cần script.

### Task 13.1 — BE: `snapshotProductMasterPrice()` đọc `product_unit_prices` (khớp ERP) [x]
**File:** Modify `hrm-api/Modules/Assign/Services/ContractService.php:704-760`
- [x] Thay query `product_prices` (by product_id) bằng: `product_units` (where product_id + unit_id,
      fallback `is_base=1` khi unit_id rỗng) → `product_unit_prices` (where product_unit_id +
      price_type_id). Lấy `sale_max_percent` từ dòng giá, `cost_price` từ `product_units.cost_price`.
- [x] **BỎ `return` sớm**: không có product_unit/dòng giá → `sale_max=0`, cost=null, VẪN tính
      `net_price`/`standard_price` (khớp try/catch ERP). Giữ nguyên công thức G/H.
- [x] Cập nhật PHPDoc nguồn từ `product_prices` → `product_unit_prices`/`product_units` + ghi rõ lý do bỏ return sớm.

### Task 13.2 — BE: re-freeze `standard_price` khi update HĐ [x]
**File:** Modify `hrm-api/Modules/Assign/Services/ContractService.php` (update() + method mới ~748)
- [x] Thêm `refreezeProductMasterPrices(Contract $contract)`: lấy `price_type` từ `$contract->quotation`,
      G từ `company_price_types`; loop mọi `ContractProductPrice` của HĐ, dựng `$attrs` từ cột dòng
      (erp_product_id, unit_id, quoted_price, unit_price_after_discount), gọi `snapshotProductMasterPrice`,
      ghi lại `sale_max_percent/net_price/cost_price/standard_price` + `updated_by`.
- [x] Gọi trong `update()` — khối 2e sau `recomputeEffectiveDates`, trước History.

### Task 13.3 — Verify [x]
- [x] Dry-run (Reflection, KHÔNG ghi DB) gọi `snapshotProductMasterPrice` cho từng dòng HĐ 1 trên
      DB remote `hrm_erp_test` → **DSTC = 129,476,020.00** (khớp tính tay). 8 dòng đều có
      `standard_price` khác NULL; `cost_price` lấy giá vốn thật (49009=3,769,529…); dòng con id4/id5
      = 0 và không tính vào DSTC. Code path PHP chạy sạch (dry-run HĐ 15 local cũng không lỗi).
- [x] `php -l` ContractService.php: No syntax errors.

### Task 13.4 — BE: vế `min()` cộng `extra_price` + đối xứng store/update (khớp ERP có vượt trội) [x]
**File:** Modify `hrm-api/Modules/Assign/Services/ContractService.php`
- Explore xác nhận công thức ERP khớp, cảnh báo 1 điểm tinh tế: ERP `FirmContractService:700`
  `price_after_discount = round(price + price_extra − price_discount)` **CÓ cộng `price_extra`**, còn
  HRM `QuotationService::recomputeUnitPriceAfterDiscount()` tính `unit_price_after_discount = quoted − discount`
  **KHÔNG cộng extra** (extra là cột RIÊNG `hrm_contract_product_prices.extra_price`, gán qua
  `setLineAdjustment` cấp HĐ; `quotation_product_prices` không có cột này).
- **Ruling (khớp ERP):** vế đầu `min()` của `standard_price` phải là `round(unit_price_after_discount + extra_price)`
  (hiện chỉ `unit_price_after_discount`). Lệch chỉ lộ khi dòng CÓ vượt trội **và** giảm giá vượt
  ngưỡng sale_max (min rơi vào vế giá-sau-giảm thay vì net); khi đó HRM cũ thiếu `+ extra × G × H`
  mỗi đơn vị. HĐ 1 extra=discount=0 nên không đổi (DSTC vẫn 129,476,020). Cost nếu sai: lệch DSTC ở
  HĐ có vượt trội + chiết khấu sâu.
- [x] `snapshotProductMasterPrice()`: `$priceAfterDiscount = round((unit_price_after_discount ?? quoted) + extra_price)`.
- [x] `refreezeProductMasterPrices()`: thêm `extra_price => $line->extra_price` vào `$attrs`.
- [x] **store() đối xứng update():** store snapshot (286) chạy TRƯỚC khi áp `line_adjustments` (344-352)
      nên extra chưa vào standard_price; thêm `refreezeProductMasterPrices($contract)` ngay sau khối
      adjustments (355) để store cũng freeze đúng khi tạo HĐ có vượt trội. (update() đã đúng: refreeze
      ở 501 sau adjustments 488.)
- [x] Verify lại dry-run HĐ 1 (extra=0) → DSTC vẫn **129,476,020.00**; case tổng hợp có extra khớp ERP.

### Checkpoint — 2026-10-15 (Phase 13 — CODE + VERIFY XONG, CHƯA commit)
Vừa hoàn thành: fix DSTC=0 màn HTHT HĐ. `snapshotProductMasterPrice()` nay đọc `product_units` +
`product_unit_prices` (thay `product_prices` legacy rỗng), bỏ `return` sớm nên hàng hoá không có
dòng giá vẫn tính `standard_price` (khớp try/catch ERP). Thêm `refreezeProductMasterPrices()` gọi
trong `update()` → HĐ Chờ duyệt chỉ cần Không duyệt → Sửa → Lưu là tự tính lại đúng, không backfill.
Verify dry-run trên DB remote: DSTC HĐ 1 = 129,476,020.00 (đúng kỳ vọng).
Task 13.4 (Explore xác nhận công thức ERP): vế `min()` cộng `extra_price` + `round()` khớp ERP
`round(price+extra−discount)`; store() thêm refreeze sau adjustments (đối xứng update). Dry-run lại:
CASE A (HĐ 1, extra=0) DSTC vẫn 129,476,020.00; CASE B (min rơi vào vế giá-sau-giảm) extra 0→595k,
extra 1tr→1,595k (chênh đúng extra×G×H). `php -l` sạch.
Đang làm dở: (không).
Bước tiếp theo: CHỜ user yêu cầu commit/push. 1 file BE chưa commit (`ContractService.php`) + các file
Phase 11/12 chưa commit (ContractResource.php, contracts/index.vue, contracts/_id/index.vue).
Blocked: (không).

---

## Phase 14 — Lịch sử HĐ (màn chi tiết): Hành động tiếng Việt + mặc định thu gọn

**Bối cảnh (user, kèm screenshot):** Khối "Lịch sử" ở màn Chi tiết HĐ hiển thị cột **Hành động** ra
mã thô tiếng Anh (`submit`, `create`). Yêu cầu: (1) Hành động hiển thị **tiếng Việt**; (2) khối Lịch
sử **mặc định ẩn (thu gọn)**, có nút tùy chỉnh **Xem / Thu gọn**.

**Hiện trạng:** Màn chi tiết dùng khối Lịch sử TỰ CHẾ (bảng đơn giản Thời gian/Hành động/Người thực
hiện/Ghi chú), KHÔNG dùng `SystemInfoSection`. BE `DetailContractResource::resolveHistories()` trả
`action` thô; FE `pages/assign/contracts/_id/index.vue:343` render thẳng `h.action`.
Actions có thể có: create / update / submit / approve / reject / liquidate (ContractService).
→ Phạm vi: chỉ 2 chỉnh sửa nhỏ trên khối hiện có, KHÔNG rebuild sang SystemInfoSection (user không yêu cầu).

### Task 14.1 — BE: trả `action_label` tiếng Việt [x]
**File:** Modify `hrm-api/Modules/Assign/Transformers/DetailContractResource.php` (`resolveHistories()` ~318)
- [x] Thêm helper map action → nhãn VN: create=Tạo mới, update=Chỉnh sửa, submit=Gửi duyệt,
      approve=Duyệt, reject=Từ chối, liquidate=Thanh lý; fallback = action thô.
      → `historyActionLabel(?string $action): ?string` (dòng 345), null/rỗng→null.
- [x] Thêm key `action_label` vào DTO mỗi dòng history (giữ nguyên `action` cho tương thích). (dòng 329)

### Task 14.2 — FE: hiển thị nhãn VN + khối mặc định thu gọn, toggle Xem/Thu gọn [x]
**File:** Modify `hrm-client/pages/assign/contracts/_id/index.vue`
- [x] Cột Hành động render `h.action_label || h.action || '—'`. (dòng 349)
- [x] Thêm data `showHistory: false`; header khối Lịch sử click toggle (`.section-header--toggle`,
      cursor pointer) + nút `V2BaseButton light` bên phải (slot #prefix chevron ri-arrow-up/down-s-line,
      chữ "Thu gọn"/"Xem lịch sử"). Thân `.section-body` bọc `v-show="showHistory"` (dựng sẵn, chỉ ẩn).
- [x] Sửa màu `.text-muted` (ĐỎ) trong khối → xám `#6b7280` (count + dòng rỗng) theo CLAUDE.md.

### Task 14.3 — Verify Playwright [x]
- [x] Mở màn chi tiết HĐ 13 (có 5 history) trên local: khối Lịch sử thu gọn mặc định (nút "Xem lịch sử"
      + chevron xuống); bấm "Xem lịch sử" → bảng hiện, cột Hành động ra tiếng Việt (Chỉnh sửa/Duyệt/
      Gửi duyệt/Chỉnh sửa/Tạo mới); nút đổi "Thu gọn" + chevron lên; bấm "Thu gọn" → ẩn lại. OK.

### Checkpoint — 2026-10-15 (Phase 14 — CODE + VERIFY XONG, CHƯA commit)
Vừa hoàn thành: BE `action_label` VN (DetailContractResource.php: resolveHistories + historyActionLabel,
`php -l` sạch) + FE toggle khối Lịch sử (index.vue: data showHistory, header toggle + nút V2BaseButton,
v-show body, đổi text-muted→xám). Verify Playwright HĐ 13: thu gọn mặc định, nhãn VN đúng, toggle 2 chiều OK.
Files CHƯA commit: `DetailContractResource.php`, `pages/assign/contracts/_id/index.vue`.
Lưu ý: `ProductExportRequestForm.vue` có sửa đổi KHÔNG thuộc việc này — vẫn để nguyên unstaged cho user.
Bước tiếp theo: chờ user yêu cầu commit/push (Phase 11/12/13/14 cùng feature hop-dong).
Blocked: không

---

## Phase 15 — Màn Duyệt HTHT: nút "Không duyệt" bắt buộc nhập lý do từ chối

**Bối cảnh (user, nguyên văn):** "Không duyệt nhưng chưa bắt buộc nhập lý do từ chối (Phần này em xử
lý như ở ERP cũ) màn Duyệt HTHT" → Màn Duyệt Hỗ trợ hạch toán (HTHT), nút **Không duyệt** (reject)
hiện CHƯA bắt buộc nhập lý do. Làm giống ERP cũ: **bắt buộc nhập lý do từ chối**.

**Xác minh ERP cũ:** `ContractsController::validApproveReject()` (dòng 1678-1679) có rule
`'valid_comment' => 'required'` — ERP luôn bắt buộc nhập lý do khi không duyệt. → đúng yêu cầu.

**Hiện trạng HRM (THIẾU validate):** `support-accounting.vue::doReject()` (dòng 322-340) dùng
`$bvModal.msgBoxConfirm` rồi POST `/reject` với `payload: { rejected_reason: '' }` (RỖNG). BE
`ContractController::reject()` (dòng 600) → `ContractService::reject()` chỉ set giá trị truyền vào,
KHÔNG validate required. Màn chi tiết HĐ `index.vue` ĐÃ có reject modal bắt buộc lý do (mẫu để bám).
Endpoint `/reject` DÙNG CHUNG cho cả index.vue (đã gửi lý do) và support-accounting.vue → thêm
validate BE không phá index.vue.

### Task 15.1 — BE: validate `rejected_reason` required ở endpoint reject [x]
**File:** Modify `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ContractController.php` (`reject()` ~600)
- [x] Trước khi gọi `$service->reject(...)`, validate `rejected_reason` = `required|string|max:255`
      (dùng `$request->validate()`, câu lỗi chuẩn lang file "Bắt buộc phải nhập"). Rethrow `ValidationException`.

### Task 15.2 — FE: thay msgBoxConfirm bằng reject modal bắt buộc lý do [x]
**File:** Modify `hrm-client/pages/assign/contracts/_id/support-accounting.vue`
- [x] Import `V2BaseLabel`, `V2BaseTextarea`; thêm data `rejectModalShow/rejectReason/rejectError`.
- [x] Nút "Không duyệt" mở modal (`openReject` → `rejectModalShow = true`, dọn `rejectReason/rejectError`)
      thay vì gọi doReject trực tiếp. Modal bám pattern index.vue: b-modal + V2BaseLabel required +
      V2BaseTextarea + text-danger + 2 nút Huỷ/Xác nhận từ chối.
- [x] `handleReject()`: trống → `rejectError='Vui lòng nhập lý do từ chối'` return (không gọi API);
      có lý do → POST `/reject` payload `{ rejected_reason }`, thành công push về chi tiết HĐ
      (`/assign/contracts/${contractId}`) — CÙNG đích với `doApprove` sẵn có, đối xứng approve/reject.

### Task 15.3 — Verify Playwright [x]
- [x] BE 422: POST `/api/v1/assign/contracts/13/reject` với `{rejected_reason:''}` → **422**
      `{"errors":{"rejected_reason":["Bắt buộc phải nhập"]}}`.
- [x] FE màn support-accounting (HĐ 13 set tạm status=2): bấm "Không duyệt" → modal "Từ chối hợp đồng"
      hiện; bấm "Xác nhận từ chối" khi để trống → lỗi đỏ "Vui lòng nhập lý do từ chối" dưới ô, KHÔNG có
      request `/reject` (đã soi network).
- [x] Happy-path: nhập lý do → reject OK, status 2→3 (DANG_TAO, đúng nghiệp vụ), ghi 1 dòng
      ContractHistory (action=reject, note=lý do), navigate về chi tiết HĐ.
- [x] Dọn DB về gốc: xoá history test (id 26), `UPDATE hrm_contracts SET status=1, rejected_reason=NULL,
      updated_by=13 WHERE id=13` — đã xác nhận HĐ 13 về đúng gốc.

### Checkpoint — 2026-10-15 (Phase 15 — CODE + VERIFY XONG, CHƯA commit)
Vừa hoàn thành: nút "Không duyệt" màn Duyệt HTHT nay bắt buộc nhập lý do từ chối (như ERP cũ), chặn
ở CẢ FE (modal + lỗi inline, không gọi API khi trống) lẫn BE (422 required). Verify Playwright đủ 3 ca.
Files CHƯA commit: `ContractController.php` (BE), `support-accounting.vue` (FE).
Bước tiếp theo: chờ user xác nhận trước khi commit/push.
Blocked:

---

## Phase 16 — HĐ bị từ chối về "Đang tạo" nhưng danh sách/chi tiết không có nút Sửa/Xóa

**Yêu cầu user:** "khi không duyệt Hợp đồng ở trạng thái Đang tạo nhưng không có nút sửa, màn danh sách".

**Chốt với user (free-text "1 A, 2 có, 3 như erp"):** đồng bộ ERP `app/Contract.php:2699-2707`
(`canEdit`/`canDelete` = `status==3 (Đang tạo) && created_by==Auth::id()`, KHÔNG gate quyền):
1. (A) `is_can_edit` = người lập + status Đang tạo(3) — BỎ gate quyền "Sửa hợp đồng", bỏ Chờ duyệt(2).
2. Nút Xóa đồng bộ: `is_can_delete` = người lập + Đang tạo(3) — BỎ gate quyền "Xóa hợp đồng".
3. Phạm vi trạng thái = chỉ Đang tạo(3).

Giữ gate Duyệt/Thanh lý nguyên trạng (không đụng). Chốt chặn thật ở BE (middleware route), FE chỉ ẩn nút.
Màn chi tiết phải KHỚP màn danh sách (CLAUDE.md).

### Task 16.1 — BE Entity: isEditableStatus() chỉ Đang tạo + accessor is_can_edit/is_can_delete theo người lập [x]
**File:** `hrm-api/Modules/Assign/Entities/Contract/Contract.php`
- [x] `isEditableStatus()` (215-218) → chỉ `status === STATUS_DANG_TAO`.
- [x] `getIsCanDeleteAttribute()` (153-156) → `isEditableStatus() && (int)created_by === (int)auth()->id()`.
- [x] Thêm `getIsCanEditAttribute()` cùng công thức (edit=delete y hệt ERP).

### Task 16.2 — BE Resource: bỏ gate quyền ở is_can_edit/is_can_delete [x]
**File:** `hrm-api/Modules/Assign/Transformers/ContractResource.php`
- [x] `is_can_edit` = `(bool) $this->resource->is_can_edit` (bỏ `self::perm('edit')`).
- [x] `is_can_delete` = `(bool) $this->resource->is_can_delete` (bỏ `self::perm('delete')`).
- [x] Gỡ 'edit'/'delete' khỏi mảng `perm()` (không còn dùng); giữ approve/liquidate.

### Task 16.3 — BE DetailResource: thêm is_can_edit [x]
**File:** `hrm-api/Modules/Assign/Transformers/DetailContractResource.php`
- [x] Thêm `'is_can_edit' => (bool) $this->is_can_edit` cạnh `is_can_delete` (dòng 140).

### Task 16.4 — BE Service: guard update() chỉ Đang tạo [x]
**File:** `hrm-api/Modules/Assign/Services/ContractService.php`
- [x] `update()` (388-391): đổi guard sang `!$contract->isEditableStatus()`, message "Chỉ sửa được hợp đồng đang tạo".
- [x] `destroy()` (104-107): message rõ "Chỉ người lập mới xóa được hợp đồng đang tạo" (accessor tự đúng).

### Task 16.5 — BE Middleware CheckContractEditable + route [x]
**File:** `hrm-api/app/Http/Middleware/CheckContractEditable.php` (mới) + `app/Http/Kernel.php` + `Modules/Assign/Routes/api.php`
- [x] Middleware kiểm `is_can_edit` (người lập + Đang tạo) → 403 nếu không. Khuôn CheckCustomerNotLocked.
- [x] Kernel đăng ký alias `contractEditable`.
- [x] Route PUT /{id}, DELETE /{id}, attachments POST+DELETE: thay `checkPermission:Sửa/Xóa hợp đồng` → `contractEditable`.

### Task 16.6 — BE Controller: gỡ check quyền trong update()/destroy() [x]
**File:** `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ContractController.php`
- [x] `update()` (~498): gỡ `if (!isCurrentEmployeeHasPermission('Sửa hợp đồng')) abort(403)`.
- [x] `destroy()` (~526): gỡ `if (!isCurrentEmployeeHasPermission('Xóa hợp đồng')) abort(403)`.

### Task 16.7 — FE chi tiết: canEdit/canDelete đọc cờ BE, khớp danh sách [x]
**File:** `hrm-client/pages/assign/contracts/_id/index.vue`
- [x] `canEdit()` (604-610) → dùng `item.is_can_edit` từ BE (bỏ hasAPermission + bỏ CHO_DUYET).
- [x] `canDelete()` (611-618) → dùng `item.is_can_delete` (bỏ hasAPermission).
- [x] `canManageAttachments()` (637-639) vẫn = canEdit.

### Task 16.8 — Verify Playwright + khôi phục DB [x]
- [x] Người lập + HĐ Đang tạo(3) → thấy Sửa/Xóa ở CẢ danh sách và chi tiết dù không có quyền "Sửa/Xóa HĐ".
- [x] HĐ Chờ duyệt(2)/Đã duyệt(1) → KHÔNG thấy Sửa/Xóa.
- [x] API PUT /{id} của người lập (HĐ Đang tạo) không 403; PUT khi Đã duyệt → chặn.
- [x] Khôi phục DB: `UPDATE hrm_contracts SET status=1, rejected_reason=NULL, updated_by=13 WHERE id=13` + xoá history test.

### Checkpoint — 2026-10-15 (Phase 16)
Đồng bộ ERP: Sửa/Xóa HĐ nay mở cho người lập khi HĐ Đang tạo, KHÔNG cần quyền "Sửa/Xóa hợp đồng".
Chốt chặn BE = middleware contractEditable; FE ẩn nút khi !is_can_edit/!is_can_delete; chi tiết khớp danh sách.

**VERIFY XONG (2026-10-15):**
- HTTP end-to-end bằng JWT mint cho `App\Models\TpEmployee::find(25)` (user KHÔNG có quyền "Sửa/Xóa hợp đồng"):
  - creator=25 + status Đang tạo(3) → PUT = **422** (KHÔNG 403) ⇒ ungate OK, người lập không quyền vẫn sửa được.
  - creator=25 + status Đã duyệt(1) → PUT = **403** (middleware chặn sai trạng thái).
  - creator=13 + status Đang tạo(3), token emp25 → PUT = **403** (không phải người lập).
  - DELETE creator≠self → **403** (middleware DELETE chạy; không xoá thật). Route PUT/DELETE/attachments đều gắn `contractEditable` (Routes/api.php:834-842).
- UI Playwright HĐ 13: Đang tạo(3) → danh sách hiện ri-edit-line + ri-delete-bin-line, chi tiết footer có Sửa+Xoá (+Trình duyệt); Đã duyệt(1) → danh sách KHÔNG nút, chi tiết chỉ còn Quay lại. Chi tiết khớp danh sách.
- DB khôi phục gốc: HĐ 13 status=1, created_by=13, updated_by=13, rejected_reason=NULL; history giữ nguyên 5 dòng (không phát sinh dòng test — curl bị chặn 422/403 trước khi ghi).

**CHƯA commit/push — chờ user xác nhận.**
