# Điều khoản thanh toán trên hợp đồng — Plan

**Người phụ trách:** @khoipv
**Ngày bắt đầu:** 2026-05-18
**Trạng thái:** Đã có spec, chưa code
**Spec:** `docs/superpowers/specs/2026-05-18-contract-payment-terms-design.md`
**Mock:** `hrm-thanhan-client/pages/timesheet/setting/debt-limit/canh-bao-cong-no-v4.html` (section 3)

---

## Phase 1 — BE Database (Task 1)

- [x] **Task 1:** Migration `create_contract_payment_terms_table`
  - File: `hrm-thanhan-api/database/migrations/2026_05_18_120000_create_contract_payment_terms_table.php`
  - Schema: `id`, `contract_id` (FK cascade delete), `term_code` (enum 100PCT/TIME/VALUE/ROLLING), `enabled` (tinyInt default 0), `max_days` (int unsigned nullable), `max_value` (bigInt unsigned nullable), `max_orders` (int unsigned nullable), `timestamps`
  - Index: UNIQUE(`contract_id`, `term_code`)
  - Không seed — HĐ cũ sẽ có 0 row, FE handle bằng default

## Phase 2 — BE Model (Task 2)

- [x] **Task 2:** Model `ContractPaymentTerm` + relation trên Contract
  - File: `hrm-thanhan-api/Modules/Category/Entities/Contract/ContractPaymentTerm.php`
  - Constants: `TERM_100PCT`, `TERM_TIME`, `TERM_VALUE`, `TERM_ROLLING`, `TERMS` (map code → metadata)
  - Method: `getDefaultTerms()` trả 4 item default (enabled=false)
  - Thêm `paymentTerms()` hasMany vào `Contract.php`

## Phase 3 — BE Service + Validation (Task 3-4)

- [x] **Task 3:** Thêm `syncPaymentTerms()` vào `ContractService.php`
  - Gọi trong cả `store()` và `update()` — sau `syncGuarantees`
  - Logic: nếu request có payment_terms → updateOrCreate 4 row; nếu không có → insert 4 row default
  - Validate exclusive: 100PCT bật → các row khác phải tắt

- [x] **Task 4:** Thêm validation rules vào `StoreContractRequest.php`
  - `payment_terms` nullable|array
  - `payment_terms.*.term_code` required|in:100PCT,TIME,VALUE,ROLLING
  - `payment_terms.*.enabled` required|boolean
  - `payment_terms.*.max_days/max_value/max_orders` nullable|integer|min:1

## Phase 4 — BE Response (Task 5)

- [x] **Task 5:** Load paymentTerms khi GET contract
  - Tìm chỗ controller/service trả contract → thêm `->load('paymentTerms')`
  - Verify response có include `payment_terms` array

## Phase 5 — FE Component (Task 6-7)

- [x] **Task 6:** Tạo component `PaymentTermsTab.vue`
  - File: `hrm-thanhan-client/pages/contract/contract/components/PaymentTermsTab.vue`
  - Props: `paymentTerms` (Array), `isShow` (Boolean)
  - Render bảng 4 row giống mock section 3
  - Logic: tick 100PCT → disable 3 row khác + alert; input enable khi row bật; isShow → all disabled
  - Emit `update:payment-terms` khi thay đổi
  - Dùng CurrencyInput cho max_value

- [x] **Task 7:** Tích hợp vào `GeneralComponent.vue`
  - Import + register `PaymentTermsTab`
  - Thay `<div class="row g-2 category-card"></div>` trong tab "Cài đặt công nợ thanh toán" bằng component
  - Init `formSubmit.payment_terms` từ contract data khi edit/show
  - Khi tạo mới: init = [] (FE tự render default)

## Phase 6 — Test (Task 8)

- [ ] **Task 8:** User test end-to-end
  1. Chạy `php artisan migrate` → bảng mới được tạo
  2. Tạo HĐ mới → tab "Cài đặt công nợ thanh toán" hiện bảng 4 row tắt → save → DB có 4 row enabled=0
  3. Edit HĐ → tick "Giới hạn thời gian" + nhập 30 ngày → save → DB row TIME enabled=1, max_days=30
  4. Tick "100% trước giao" → 3 row khác disable + alert hiện → save → DB chỉ 100PCT enabled=1
  5. Bỏ tick 100PCT → 3 row unlock lại
  6. Mở HĐ ở chế độ xem → tất cả disabled
  7. Mở HĐ cũ (chưa có payment terms) → hiện 4 row default tắt → save → tạo 4 row mới

## Files sẽ tạo / sửa

**BE (`hrm-thanhan-api/`):**
- Create `database/migrations/2026_05_18_120000_create_contract_payment_terms_table.php`
- Create `Modules/Category/Entities/Contract/ContractPaymentTerm.php`
- Modify `Modules/Category/Entities/Contract/Contract.php` (thêm relation)
- Modify `Modules/Category/Services/ContractService.php` (thêm syncPaymentTerms)
- Modify `Modules/Category/Http/Requests/StoreContractRequest.php` (thêm rules)
- Modify controller hoặc resource để load paymentTerms

**FE (`hrm-thanhan-client/`):**
- Create `pages/contract/contract/components/PaymentTermsTab.vue`
- Modify `pages/contract/contract/components/GeneralComponent.vue` (import + tích hợp vào tab)
