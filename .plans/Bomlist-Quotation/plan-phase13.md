# Plan Phase 13 — Email khách hàng trên Dự án TKT + Báo giá

> **Spec:** [design-phase13-customer-email.md](./design-phase13-customer-email.md)
> **Ngày bắt đầu:** 2026-04-20
> **Người phụ trách:** @dnsnamdang
> **Branch:** `tpe-develop-assign` (cả API + Client)

**Goal:** Bổ sung trường `customer_email` (required + validate format) vào Dự án TKT, snapshot sang Báo giá. Pattern nhất quán với Batch 10 (MST + Người liên hệ + SĐT liên hệ).

**Architecture:** Tận dụng cột `prospective_projects.customer_email` đã có sẵn. Chỉ cần thêm 1 migration cho `quotations.customer_email` + update service snapshot + thêm UI input Project + UI display Quotation.

**Tech stack:** Laravel 8 + MySQL (API), Nuxt 2 + Vue 2 + Bootstrap-Vue (Client).

---

## Trạng thái tổng

- Brainstorm: Done (2026-04-20)
- Design: Done (`design-phase13-customer-email.md`)
- Plan: Done
- Tiến độ: 14/16 tasks (code DONE — còn Task 15-16 manual test)

---

## Quy tắc thực thi

1. Không commit/push — user tự quản lý git.
2. Hoàn thành 1 task → đánh `[x]` ngay, không batch cuối session.
3. Sau mỗi nhóm (13.X) → smoke test thủ công qua Postman/UI.
4. FE tuân thủ V2Base components (xem `docs/shared.md`).
5. Follow đúng convention pattern Batch 10 (Task 54-57 plan-phase12).

---

## 13.1 — BE Quotation: Migration + Service + Transformer (5 tasks)

**Folder:** `hrm-api/database/migrations/`, `hrm-api/Modules/Assign/Services/`, `hrm-api/Modules/Assign/Transformers/`

- [x] **Task 1:** Migration `2026_04_20_100001_add_customer_email_to_quotations.php`

  File: `hrm-api/database/migrations/2026_04_20_100001_add_customer_email_to_quotations.php`
  ```php
  <?php
  use Illuminate\Database\Migrations\Migration;
  use Illuminate\Database\Schema\Blueprint;
  use Illuminate\Support\Facades\Schema;

  class AddCustomerEmailToQuotations extends Migration {
      public function up() {
          Schema::table('quotations', function (Blueprint $t) {
              $t->string('customer_email')->nullable()->after('customer_address')
                ->comment('Email khách hàng (snapshot từ prospective_projects tại thời điểm tạo)');
          });
      }
      public function down() {
          Schema::table('quotations', function (Blueprint $t) {
              $t->dropColumn('customer_email');
          });
      }
  }
  ```

- [x] **Task 2:** Chạy migration + verify

  ```bash
  cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-api && php artisan migrate
  ```
  Expected: "Migrated: 2026_04_20_100001_add_customer_email_to_quotations".
  Verify: `DESCRIBE quotations` có cột `customer_email VARCHAR(255) NULL` ngay sau `customer_address`.

  Entity `Quotation` dùng `$guarded = []` (mass assignment cho tất cả field) → **KHÔNG cần sửa entity**.

- [x] **Task 3:** Service `QuotationService::createFromRequest` — thêm dòng snapshot

  File: `hrm-api/Modules/Assign/Services/QuotationService.php`

  Tìm block có `'customer_address' => $project->customer_address ?? null,` (khoảng dòng 64). Thêm dòng ngay sau:
  ```php
  'customer_tax_code' => $project->customer_tax_code ?? null,
  'customer_address' => $project->customer_address ?? null,
  'customer_email' => $project->customer_email ?? null,    // NEW Phase 13
  'customer_contact_name' => $project->customer_contact_name ?? null,
  'customer_contact_phone' => $project->customer_contact_phone ?? null,
  ```

- [x] **Task 4:** Transformer `DetailQuotationResource` — expose `customer_email`

  File: `hrm-api/Modules/Assign/Transformers/DetailQuotationResource.php`

  Tìm block (khoảng dòng 117):
  ```php
  'customer_name' => $this->customer_name,
  'customer_tax_code' => $this->customer_tax_code,
  'customer_address' => $this->customer_address,
  'customer_contact_name' => $this->customer_contact_name,
  ```

  Thêm dòng ngay sau `customer_address`:
  ```php
  'customer_name' => $this->customer_name,
  'customer_tax_code' => $this->customer_tax_code,
  'customer_address' => $this->customer_address,
  'customer_email' => $this->customer_email,                 // NEW Phase 13
  'customer_contact_name' => $this->customer_contact_name,
  ```

- [x] **Task 5:** Smoke test BE nhóm 13.1 qua tinker

  ```bash
  cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-api && php artisan tinker
  ```
  Chạy:
  ```php
  // Lấy project có customer_email
  $p = \Modules\Assign\Entities\ProspectiveProject::whereNotNull('customer_email')->first();
  echo $p ? $p->customer_email : 'no project has email';

  // Tạo quotation test qua API endpoint hoặc gọi trực tiếp service
  // → Sau đó query Quotation::latest()->first()->customer_email để verify snapshot
  ```
  Expected: Quotation mới tạo có `customer_email` trùng với project.

**Smoke test nhóm 13.1 pass → chuyển sang 13.2.**

---

## 13.2 — BE Project: FormRequest validation (1 task)

**Folder:** `hrm-api/Modules/Assign/Http/Requests/ProspectiveProject/`

- [x] **Task 6:** Thêm rule `customer_email` vào `ProspectiveProjectRequest`

  File: `hrm-api/Modules/Assign/Http/Requests/ProspectiveProject/ProspectiveProjectRequest.php`

  Trong method `rules()`, trong `$baseRules` (khoảng dòng 38-52), thêm dòng sau `'customer_id' => 'required|integer'`:
  ```php
  $baseRules = [
      'name' => 'required|max:255|unique:prospective_projects,name,' . $this->id,
      'project_scale_id' => 'required|integer',
      'investment_type_id' => 'required|integer',
      'project_address' => 'required|max:255',
      'customer_id' => 'required|integer',
      'customer_email' => 'required|email|max:255',           // NEW Phase 13
      'main_sale_employee_id' => 'required|integer',
      // ... rest unchanged
  ];
  ```

  Trong `messages()`, thêm vào return array:
  ```php
  'customer_email.required' => 'Email khách hàng là bắt buộc.',
  'customer_email.email' => 'Email khách hàng không đúng định dạng.',
  'customer_email.max' => 'Email khách hàng không quá 255 ký tự.',
  ```

**Smoke test nhóm 13.2:** Gọi POST `/api/v1/assign/prospective-projects` không có `customer_email` → 422 với message tiếng Việt. Nhập `abc@` → 422. Nhập valid email → 200.

---

## 13.3 — FE Project: Input Email trong CustomerInfoSection (2 tasks)

**Folder:** `hrm-client/pages/assign/prospective-projects/components/`

- [x] **Task 7:** Thêm input Email vào `CustomerInfoSection.vue`

  File: `hrm-client/pages/assign/prospective-projects/components/CustomerInfoSection.vue`

  Tìm block readonly (dòng 32-43) và block "Người liên hệ" (dòng 45-56). Chèn row input Email **giữa** 2 block này (ngay trước `<div class="row">` của "Người liên hệ"):

  ```html
  <div v-if="formSubmit.customer_id" class="readonly-box readonly-customer-info mb-3">
      <!-- ... existing display ... -->
  </div>

  <!-- NEW Phase 13: input Email khách hàng -->
  <div class="row">
      <div class="col-md-12 mb-2">
          <V2BaseLabel required>Email khách hàng</V2BaseLabel>
          <V2BaseInput
              v-model="formSubmit.customer_email"
              type="email"
              placeholder="Nhập email khách hàng"
              :disabled="isShow"
          />
          <V2BaseError v-if="formError.customer_email" :message="formError.customer_email" />
      </div>
  </div>

  <div class="row">
      <div class="col-md-12 mb-2">
          <V2BaseLabel required>Người liên hệ</V2BaseLabel>
          <!-- ... existing ... -->
      </div>
  </div>
  ```

  Logic auto-fill `updated.customer_email = customerDetail.email || customer.email || ''` đã có sẵn ở dòng 179 và 205 — **KHÔNG sửa**.

- [x] **Task 8:** Smoke test compile `CustomerInfoSection.vue`

  ```bash
  cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-client && node -e "\
  const c=require('vue-template-compiler'),fs=require('fs');\
  const f='pages/assign/prospective-projects/components/CustomerInfoSection.vue';\
  const s=fs.readFileSync(f,'utf8'); const p=c.parseComponent(s);\
  const r=p.template?c.compile(p.template.content):null;\
  console.log(f,'tpl:',p.template?'OK':'-','script:',p.script?'OK':'-','errs:',r?r.errors.length:'-');"
  ```
  Expected: `tpl: OK script: OK errs: 0`.

---

## 13.4 — FE Project: Validation trong add.vue + edit.vue (2 tasks)

**Folder:** `hrm-client/pages/assign/prospective-projects/`

- [x] **Task 9:** Thêm validate `customer_email` vào `add.vue`

  File: `hrm-client/pages/assign/prospective-projects/add.vue`

  Trong `submitForm()` (áp cả "Lưu nháp" + "Gửi duyệt"), tìm block validate `customer_contact_id` (đã có từ Batch 10). Thêm block validate email **ngay sau** block contact:

  ```js
  // Validate customer_contact_id (đã có từ Batch 10 — giữ nguyên)
  if (!this.formSubmit.customer_contact_id) {
      this.formError.customer_contact_id = 'Người liên hệ là bắt buộc'
      this.$toast.error('Vui lòng chọn người liên hệ của khách hàng')
      return
  }

  // NEW Phase 13: validate customer_email
  if (!this.formSubmit.customer_email || !this.formSubmit.customer_email.trim()) {
      this.formError.customer_email = 'Email khách hàng là bắt buộc'
      this.$toast.error('Vui lòng nhập email khách hàng')
      return
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(this.formSubmit.customer_email.trim())) {
      this.formError.customer_email = 'Email khách hàng không đúng định dạng'
      this.$toast.error('Email khách hàng không đúng định dạng')
      return
  }
  ```

  Note: đặt block email sau contact để thứ tự toast error match thứ tự UI field.

- [x] **Task 10:** Thêm validate `customer_email` vào `_id/edit.vue`

  File: `hrm-client/pages/assign/prospective-projects/_id/edit.vue`

  Copy block validate email y hệt Task 9 vào `submitForm()` của edit.vue, đặt ngay sau block validate `customer_contact_id`.

**Smoke test nhóm 13.3 + 13.4:**
```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-client && node -e "\
const c=require('vue-template-compiler'),fs=require('fs');\
for (const f of [\
  'pages/assign/prospective-projects/components/CustomerInfoSection.vue',\
  'pages/assign/prospective-projects/add.vue',\
  'pages/assign/prospective-projects/_id/edit.vue']) {\
  const s=fs.readFileSync(f,'utf8'); const p=c.parseComponent(s);\
  const r=p.template?c.compile(p.template.content):null;\
  console.log(f,'tpl:',p.template?'OK':'-','script:',p.script?'OK':'-','errs:',r?r.errors.length:'-');\
}"
```
Expected: 3 dòng đều `tpl: OK script: OK errs: 0`.

---

## 13.5 — FE Project: Display Email trong manager.vue + _id/index.vue (2 tasks)

**Folder:** `hrm-client/pages/assign/prospective-projects/_id/`

- [x] **Task 11:** Thêm row display "Email khách hàng" vào `manager.vue`

  **Note:** `manager.vue` render Customer Info qua tab `TktTab → CustomerInfoSection :isShow="true"`. Input Email ở Task 7 tự động hiển thị disabled khi show. Thêm dòng "Email" vào `readonly-box` của CustomerInfoSection sau "Địa chỉ" để UX nhất quán (MST/SĐT/Địa chỉ/**Email**/Liên hệ). Không sửa manager.vue trực tiếp.

  File: `hrm-client/pages/assign/prospective-projects/_id/manager.vue`

  Tìm row hiển thị "Địa chỉ" (grep `customer_address` trong template). Thêm row mới **ngay sau**:

  ```html
  <!-- Row Địa chỉ hiện có — giữ nguyên -->
  <tr>
      <th>Địa chỉ</th>
      <td colspan="...">{{ form.customer_address || '—' }}</td>
  </tr>
  <!-- NEW Phase 13 -->
  <tr>
      <th>Email khách hàng</th>
      <td colspan="...">{{ form.customer_email || '—' }}</td>
  </tr>
  ```

  Colspan / tên variable (`form` vs `formSubmit` vs `project` ...) tuân theo pattern row "Địa chỉ" cùng file. Đọc trước khi sửa để match đúng.

- [x] **Task 12:** Thêm row display "Email khách hàng" vào `_id/index.vue`

  **Note:** `_id/index.vue` dùng `<CustomerInfoSection :isShow="true">` (dòng 9-15). Input Email (Task 7) + readonly-box Email (Task 11) trong CustomerInfoSection đã tự động hiển thị. Không cần sửa `_id/index.vue` trực tiếp.

  File: `hrm-client/pages/assign/prospective-projects/_id/index.vue`

  Tìm row hiển thị "Địa chỉ" (grep `customer_address` trong template). Thêm row mới ngay sau y hệt Task 11:

  ```html
  <tr>
      <th>Địa chỉ</th>
      <td colspan="...">{{ form.customer_address || '—' }}</td>
  </tr>
  <!-- NEW Phase 13 -->
  <tr>
      <th>Email khách hàng</th>
      <td colspan="...">{{ form.customer_email || '—' }}</td>
  </tr>
  ```

  Nếu `_id/index.vue` không có row "Địa chỉ" ở template (chỉ có trong data state) → thêm row Email vào vị trí hợp lý (khớp layout thông tin KH của file).

**Smoke test nhóm 13.5:**
```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-client && node -e "\
const c=require('vue-template-compiler'),fs=require('fs');\
for (const f of [\
  'pages/assign/prospective-projects/_id/manager.vue',\
  'pages/assign/prospective-projects/_id/index.vue']) {\
  const s=fs.readFileSync(f,'utf8'); const p=c.parseComponent(s);\
  const r=p.template?c.compile(p.template.content):null;\
  console.log(f,'tpl:',p.template?'OK':'-','script:',p.script?'OK':'-','errs:',r?r.errors.length:'-');\
}"
```
Expected: 2 dòng đều `tpl: OK script: OK errs: 0`.

---

## 13.6 — FE Báo giá: Display Email trong edit + show (2 tasks)

**Folder:** `hrm-client/pages/assign/quotations/_id/`

- [x] **Task 13:** Thêm row "Email khách hàng" vào `quotations/_id/edit.vue`

  File: `hrm-client/pages/assign/quotations/_id/edit.vue`

  Info table đã có (sau Batch 10) 2 row: (MST + Địa chỉ) và (Người liên hệ + SĐT liên hệ). Chèn row Email **giữa** 2 row này:

  ```html
  <tr>
      <th>MST</th>
      <td>{{ item.customer_tax_code || '—' }}</td>
      <th>Địa chỉ</th>
      <td>{{ item.customer_address || '—' }}</td>
  </tr>
  <!-- NEW Phase 13 -->
  <tr>
      <th>Email khách hàng</th>
      <td colspan="3">{{ item.customer_email || '—' }}</td>
  </tr>
  <tr>
      <th>Người liên hệ</th>
      <td>{{ item.customer_contact_name || '—' }}</td>
      <th>SĐT liên hệ</th>
      <td>{{ item.customer_contact_phone || '—' }}</td>
  </tr>
  ```

  Tên variable (`item` vs `quotation` vs `form`) tuân theo pattern row MST hiện có trong file.

- [x] **Task 14:** Thêm row "Email khách hàng" vào `quotations/_id/index.vue` (show báo giá)

  File: `hrm-client/pages/assign/quotations/_id/index.vue`

  Tìm info table có row "Địa chỉ" hoặc "MST". Thêm row Email y hệt Task 13 (vị trí giữa MST/Địa chỉ và Người liên hệ/SĐT liên hệ).

**Smoke test nhóm 13.6:**
```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm/hrm-client && node -e "\
const c=require('vue-template-compiler'),fs=require('fs');\
for (const f of [\
  'pages/assign/quotations/_id/edit.vue',\
  'pages/assign/quotations/_id/index.vue']) {\
  const s=fs.readFileSync(f,'utf8'); const p=c.parseComponent(s);\
  const r=p.template?c.compile(p.template.content):null;\
  console.log(f,'tpl:',p.template?'OK':'-','script:',p.script?'OK':'-','errs:',r?r.errors.length:'-');\
}"
```
Expected: 2 dòng đều `tpl: OK script: OK errs: 0`.

---

## 13.7 — Manual test end-to-end (2 tasks)

- [ ] **Task 15:** Manual test Project TKT

  - [ ] Tạo Project mới, chọn KH có email → input Email auto-fill đúng → Lưu nháp OK.
  - [ ] Tạo Project mới, chọn KH chưa có email → input rỗng → Lưu nháp → toast "Email khách hàng là bắt buộc".
  - [ ] Tạo Project mới, nhập `abc@` → Lưu nháp → toast "không đúng định dạng".
  - [ ] Tạo Project mới, nhập `test@company.com` → Gửi duyệt OK. Verify DB `prospective_projects.customer_email`.
  - [ ] Edit Project cũ chưa có email (nếu có) → input rỗng → submit bị block đến khi nhập.
  - [ ] Edit Project: sửa email → save → reload thấy email mới.
  - [ ] Mở màn show (`_id/manager.vue` + `_id/index.vue`) → thấy row "Email khách hàng" đúng giá trị, không có input.

- [ ] **Task 16:** Manual test Báo giá

  - [ ] Tạo YCBG từ Project có email → tạo Quotation → mở edit → thấy row "Email khách hàng" snapshot đúng.
  - [ ] Verify DB `quotations.customer_email` match `prospective_projects.customer_email` tại thời điểm tạo.
  - [ ] Show báo giá cũ (trước migration, `customer_email = NULL`) → row hiển thị "—".
  - [ ] Edit báo giá: row Email là readonly display, không có input sửa.
  - [ ] Đổi email trên Project → Quotation cũ giữ nguyên email cũ (immutability). Tạo Quotation mới → lấy email mới.

**Tất cả pass → Phase 13 Done. Wrap up + cập nhật STATUS.**

---

## Checkpoints

### Checkpoint — 2026-04-20
Vừa hoàn thành: Design + Plan Phase 13 (design-phase13-customer-email.md + plan-phase13.md). Branch `tpe-develop-assign`.
Đang làm dở: Không.
Bước tiếp theo: Bắt đầu Task 1 (migration quotations.customer_email) khi user xác nhận.
Blocked: Không.

### Checkpoint — 2026-04-20 (Phase 13 code DONE 14/16)
Vừa hoàn thành:
- **13.1 BE Quotation (Task 1-5):** Migration `2026_04_20_100001_add_customer_email_to_quotations` chạy OK (column `VARCHAR(255) NULL` sau `customer_address`). `QuotationService::createFromRequest` snapshot `customer_email` từ project (dòng 65). `DetailQuotationResource` expose `customer_email` (dòng 118). Entity `$guarded=[]` không cần sửa. Smoke test tinker pass.
- **13.2 BE Project (Task 6):** `ProspectiveProjectRequest` thêm rule `'customer_email' => 'required|email|max:255'` + 3 messages tiếng Việt.
- **13.3 FE CustomerInfoSection (Task 7-8):** Thêm `<V2BaseInput>` Email required sau readonly-box, trước select "Người liên hệ". Thêm dòng Email vào readonly-box giữa Địa chỉ và Liên hệ. Compile OK.
- **13.4 FE validation (Task 9-10):** `add.vue` + `_id/edit.vue` — block validate email required + regex format sau block contact validation, dùng pattern `this.$toasted?.global?.error` (không phải `$toast.error`) để nhất quán với Batch 10.
- **13.5 FE Project show (Task 11-12):** `manager.vue` render qua `TktTab → CustomerInfoSection :isShow=true` → đã inherit input disabled + readonly-box Email. `_id/index.vue` cũng reuse CustomerInfoSection :isShow=true → inherit. **Không sửa 2 file này trực tiếp.**
- **13.6 FE Báo giá (Task 13-14):** `quotations/_id/edit.vue` thêm row "Email khách hàng" colspan=3 giữa row MST/Địa chỉ và row Người liên hệ/SĐT. `quotations/_id/index.vue` thêm row sau Địa chỉ (trước Hiệu lực báo giá).
- Compile all 8 FE files: 0 errors.

Đang làm dở: Không.

Bước tiếp theo:
1. User test manual end-to-end (Task 15-16):
   - Task 15: Project TKT (tạo mới có/không email, edit project cũ, show manager+index hiển thị)
   - Task 16: Báo giá (tạo YCBG → snapshot email, show edit/index display, không sửa được email)
2. Nếu bug → dispatch fix.
3. Nếu OK → wrap up + move Phase 13 về "Hoàn thành" trong STATUS.md.

Blocked: Không.

### Checkpoint — 2026-04-20 (Wrap up session — UI fix + SRS + testcases)
Vừa hoàn thành:
- **UI fix (theo yêu cầu user):** Gộp Email cùng row Địa chỉ ở cả 2 màn Báo giá:
  - `quotations/_id/edit.vue`: MST chuyển sang row riêng colspan=3; Địa chỉ + Email cùng row 4 cột.
  - `quotations/_id/index.vue` (show): row Địa chỉ đổi từ colspan=3 → cặp Địa chỉ + Email. Xoá row Email riêng.
  - Compile OK 0 errors. Design-phase13 section 5.1 + 5.2 đã update phản ánh layout mới.
- **SRS end-to-end:** Tạo `docs/srs/bomlist-to-quotation-srs.html` (57KB) + `.pdf` (749KB). Bao gồm: sơ đồ Use Case SVG (5 actor × 12 UC), sơ đồ Swimlane SVG (5 lane × 12 bước × 3 decision + nhánh reject đỏ), luồng E2E BOM List → YCBG → Báo giá → Duyệt, 12 Business Rules, Data Model, 20 API endpoints, 11 UI screens.
- **UI Test cases E2E:** Tạo `docs/srs/bomlist-to-quotation-testcases.xlsx` (36KB, 140 cases / 12 sheets): Cover + BOM List (20) + PricingRequest (10) + Quotation Create (8) + Quotation Edit (21) + Submit & Approve (19) + Display (8) + Customer Info (16) + Margin Threshold (10) + Export & History (8) + Permission (8) + Edge Cases (12). Màu Priority/Type. Status column để QA fill.

Đang làm dở: Không.

Bước tiếp theo:
1. User chạy manual test theo checklist trong `testcases.xlsx` (filter Priority=High trước).
2. Nếu pass end-to-end → move Phase 13 về "Hoàn thành" trong STATUS.md.
3. Nếu bug → dispatch fix theo ID test case.

Blocked: Không.

---

### Checkpoint — 2026-04-23 (Bug fix BOM thêm hàng con)

Bug user báo (4 lỗi khi tạo/sửa hàng con trong Tạo BOM):

- [x] **Bug 1** — Tab "Tạo mới" hàng con: Model / Xuất xứ / Thương hiệu / Giá nhập không hiển thị ra bảng chi tiết BOM sau khi lưu.
  - Root cause 1: `BomBuilderEditor.vue` `handleAddProductApply()` hardcode `estimatedPrice: 0` bỏ qua `item.estimated_price`.
  - Root cause 2: `BomBuilderAddProductModal.vue` `findOpt` dùng strict `===` so sánh id → fail khi type khác nhau (number vs string) → model_name/brand_name/origin_name bị rỗng.
  - Fix: dùng `Number(item.estimated_price) || 0`; `findOpt` dùng `String(o.id) === String(id)`; thêm fallback `resolveOptionTextById(quickCreateModelOptions/...)` trong `handleAddProductApply` và `openEditRow`.
- [x] **Bug 2** — Sửa hàng con: Select Model chỉ hiển thị "Model #1"; label "Đơn giá dự toán".
  - Root cause: Khi Bug 1 chưa fix, `row.model` rỗng → `editForm.model_id = ''` → watch fallback `Model #${id}`.
  - Fix: `openEditRow` fallback resolve từ `quickCreateModelOptions` theo `modelId` (+ tương tự brand/origin/unit). Label đổi từ "Đơn giá dự toán" → "Giá nhập" ở `BomBuilderEditModal.vue` dòng 110.
- [x] **Bug 3** — Chỉ sau khi "Sửa" + lưu mới hiển thị đúng ra danh sách.
  - Root cause: hệ quả của Bug 1. Tự khỏi khi Bug 1 fix.
- [x] **Bug 4** — Mã hàng hoá auto-gen sai format.
  - Cũ: `HH-0001` (4 chữ số, có gạch nối, max init 1000 → code đầu = `HH-1001`).
  - Mới: `HH000001` (6 chữ số, không gạch, max init 0 → code đầu = `HH000001`).
  - Fix: `getNextGoodsCode()` regex `/HH-?(\d+)/i` (tương thích code cũ), padStart 6, bỏ gạch, max init 0.
  - Fix: `handleAddProductApply` tự gọi `getNextGoodsCode()` khi `item.code` rỗng (trước đây không gọi → mã rỗng được lưu).

File đã sửa:
- `hrm-client/pages/assign/bom-list/components/BomBuilderEditor.vue` (`getNextGoodsCode` + `handleAddProductApply` + `openEditRow`)
- `hrm-client/pages/assign/bom-list/components/BomBuilderEditModal.vue` (label)
- `hrm-client/pages/assign/bom-list/components/BomBuilderAddProductModal.vue` (`findOpt` String compare)

Bước tiếp theo: User test lại flow Tạo BOM → thêm hàng con (cả 2 tab: "Tìm hàng có sẵn" + "Tạo mới") → kiểm tra 4 cột hiển thị + code auto-gen + edit không còn "Model #ID".

Blocked: Không.

- [x] **Bug 5** (2026-04-23) — Xoá hàng con không xoá được (cả "có sẵn" lẫn "tạo mới"). Confirm OK nhưng row vẫn ở lại.
  - Root cause: `handleAddProductApply` push `newRow` vào `children` nhưng **không set `parentRowId`**. Trong `handleConfirmDeleteAction`, `this.groups.find(g => g.parent.rowId === child.parentRowId)` → `undefined` → không filter được → row còn nguyên.
  - Fix: Set `newRow.parentRowId = parentRowId` trước khi push vào children (`BomBuilderEditor.vue` `handleAddProductApply`). Thêm fallback trong `handleConfirmDeleteAction` scan theo `child.rowId` để an toàn cho mọi entry point khác.

- [x] **Bug 6** (2026-04-23) — Parent.qty không click chuột trái được (chuột phải OK).
  - Root cause: SortableJS `filter: 'tr.parent-row'` dùng default `preventOnFilter: true` → block mousedown trên parent row → input qty không focus được.
  - Fix: Thêm `preventOnFilter: false` vào child Sortable init (`BomBuilderTableCard.vue` line 665).

- [x] **Bug 7** (2026-04-23) — Parent disable cả qty và price khi có con; bớt 1 con vẫn disable price.
  - Root cause cũ: `:disabled="group.children && group.children.length > 0"` áp cả qty.
  - Fix: Chỉ disable `estimatedPrice` khi `children.length > 0` ở cả 2 render path (grouped line 210-216 + ungrouped line 379-386). Qty luôn editable.

- [x] **Bug 8** (2026-04-23) — Công thức tỷ suất lợi nhuận sai.
  - Cũ: `(sale - imp) / sale × 100`.
  - Mới (user confirm): `(sale - imp) / imp × 100`.
  - Fix: `quotations/_id/edit.vue` + `quotations/_id/index.vue` → `marginPercent` + `lineMarginPercent`. BOM `BomBuilderTableCard.vue` (`formatProfitMargin` + `totalProfitMargin`) đã dùng đúng công thức mới từ trước — không cần sửa.

---

## Checkpoint template (tham khảo)

```markdown
### Checkpoint — YYYY-MM-DD
Vừa hoàn thành: [task X]
Đang làm dở: [file + line + dừng đâu]
Bước tiếp theo: [hành động cụ thể]
Blocked: [để trống nếu không có]
```
