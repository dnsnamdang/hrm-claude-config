# Plan Phase 11 — Tách BOM và Báo giá

> **Spec:** [design-phase11.md](./design-phase11.md)
> **Ngày bắt đầu:** 2026-04-15
> **Người phụ trách:** @dnsnamdang
> **Branch:** cần tạo mới từ `update-claude-config-7-4-25` (sau khi Phase 10 merge) — **HỎI USER trước khi tạo**

---

## Trạng thái tổng
- Brainstorm: Done
- Design: Done (`design-phase11.md`)
- Plan: Done
- Tiến độ: ~85/89 tasks (~96%) — Toàn bộ code Phase 11 done. Chỉ còn 9 nhóm test thủ công (Task 80-89) do user thực hiện.
- Adjust: Task 8 (xoá BomPricing*) dời sau khi strip service/controller references. Task 32-33 ưu tiên trước nhóm 11.3-11.4 để tránh fatal error từ code gọi table đã drop.
- Note: Field NV KD của project là `main_sale_employee_id` (không phải `sale_id` như spec gốc). Cũng có `main_sale_department_id`, `main_sale_part_id`. Dùng `Employee` entity (không phải User). Check permission qua `auth()->user()->employee_info_id`.
- Note: `BaseModel` auto-set `created_by, updated_by, company_id, department_id, part_id` khi create/save — không cần set thủ công trong Service.

---

## Quy tắc thực thi
1. Clear data BOM local trước khi bắt đầu (destructive migration).
2. Không commit/push — user tự quản lý git.
3. Hoàn thành 1 task → đánh `[x]` ngay, không batch cuối session.
4. Sau mỗi nhóm (11.X) → test quick smoke bằng API/UI.
5. FE → tuân thủ style V2Base components (`docs/shared.md`).

---

## 11.1 — BE: Migrations (7 tasks) ✓

**Folder thực tế:** `hrm-api/database/migrations/` (pricing tables đã tạo ở đây ở Phase 9/10, không phải module Assign)

- [x] **Task 1:** Migration `2026_04_14_100001_drop_pricing_snapshots_and_histories_tables.php`
  ```php
  public function up() {
      Schema::dropIfExists('bom_pricing_snapshots');
      Schema::dropIfExists('bom_pricing_histories');
  }
  public function down() { /* no-op, không rollback được data */ }
  ```

- [x] **Task 2:** Migration `2026_04_14_100002_drop_pricing_columns_from_bom_lists.php`
  ```php
  public function up() {
      Schema::table('bom_lists', function (Blueprint $t) {
          $t->dropColumn([
              'price_approved_by','price_approved_at','price_rejected_reason',
              'price_approval_level','price_requested_by','price_requested_at',
              'pricing_version','tp_approved_by','tp_approved_at'
          ]);
      });
  }
  ```

- [x] **Task 3:** Migration `2026_04_14_100003_reset_bom_status_to_max_6.php`
  ```php
  public function up() {
      DB::table('bom_lists')->whereIn('status', [7,8,9,10,11])->update(['status' => 4]);
  }
  ```

- [x] **Task 4:** Migration `2026_04_14_100004_create_pricing_requests_table.php` — schema đầy đủ theo design 2.2 (bao gồm index `bom_list_id+status` và `project_id+created_by`).

- [x] **Task 5:** Migration `2026_04_14_100005_create_quotations_table.php` — schema đầy đủ theo design 2.3 (snapshot khách hàng + 4 field thương mại + validity_days + workflow status) + thêm index `project_id+status`.

- [x] **Task 6:** Migration `2026_04_14_100006_create_quotation_product_prices_table.php` — schema 2.4 (unique quotation_id + bom_list_product_id).

- [x] **Task 7:** Migration `2026_04_14_100007_create_quotation_histories_table.php` — schema 2.5 (action, from_status, to_status, meta json, actor_id).

**Smoke test result:** `php artisan migrate` chạy OK 7 migrations, không có lỗi schema.

**Smoke test:**
```bash
cd hrm-api && php artisan migrate
# Verify: SHOW TABLES LIKE 'quotation%'; DESCRIBE bom_lists (không còn cột pricing).
```

---

## 11.2 — BE: Entities (5 tasks) — 4/5 done

**Folder:** `hrm-api/Modules/Assign/Entities/`

- [x] **Task 8:** Xoá 2 file: `BomPricingHistory.php`, `BomPricingSnapshot.php`. (Thực hiện sau Task 32+33 để không break references.)

- [x] **Task 9:** Sửa `BomList.php` — xoá 5 STATUS constants 7-11, xoá relationships `pricingSnapshots()`, `pricingHistories()`, xoá các accessor/scope liên quan pricing. Giữ nguyên các relationship khác (products, groups, currency, subBoms...).

- [x] **Task 10:** Tạo `PricingRequest.php`
  ```php
  class PricingRequest extends Model {
      protected $table = 'pricing_requests';
      protected $fillable = [/* all fields từ design 2.2 */];

      const STATUS_DANG_TAO = 1;
      const STATUS_CHO_XD_GIA = 2;
      const STATUS_DANG_XD_GIA = 3;
      const STATUS_DA_CO_BAO_GIA = 4;

      public static $statusLabels = [
          1 => 'Đang tạo', 2 => 'Chờ xây dựng giá',
          3 => 'Đang xây dựng giá', 4 => 'Đã có báo giá'
      ];

      public function bomList() { return $this->belongsTo(BomList::class); }
      public function project() { return $this->belongsTo(ProspectiveProject::class, 'project_id'); }
      public function solution() { return $this->belongsTo(Solution::class); }
      public function solutionVersion() { return $this->belongsTo(SolutionVersion::class); }
      public function quotation() { return $this->hasOne(Quotation::class); }
      public function creator() { return $this->belongsTo(User::class, 'created_by'); }
      public function files() {
          return $this->hasMany(File::class, 'table_id', 'id')
              ->where('table', 'pricing_requests');
      }

      public function getNextCode() {
          $maxId = static::max('id') ?? 0;
          return 'YCBG-' . date('Y') . '-' . str_pad($maxId + 1, 5, '0', STR_PAD_LEFT);
      }
  }
  ```

- [x] **Task 11:** Tạo `Quotation.php`
  ```php
  class Quotation extends Model {
      protected $table = 'quotations';
      protected $fillable = [/* all fields từ design 2.3 */];

      const STATUS_DANG_TAO = 1;
      const STATUS_CHO_TP_DUYET = 2;
      const STATUS_CHO_BGD_DUYET = 3;
      const STATUS_DA_DUYET = 4;

      const LEVEL_1 = 1; const LEVEL_2 = 2; const LEVEL_3 = 3;

      public function pricingRequest() { return $this->belongsTo(PricingRequest::class); }
      public function bomList() { return $this->belongsTo(BomList::class); }
      public function project() { return $this->belongsTo(ProspectiveProject::class, 'project_id'); }
      public function currency() { return $this->belongsTo(TpCurrency::class, 'currency_id'); }
      public function productPrices() { return $this->hasMany(QuotationProductPrice::class); }
      public function histories() { return $this->hasMany(QuotationHistory::class)->orderByDesc('created_at'); }
      public function creator() { return $this->belongsTo(User::class, 'created_by'); }
      public function tpApprover() { return $this->belongsTo(User::class, 'tp_approved_by'); }
      public function approver() { return $this->belongsTo(User::class, 'approved_by'); }

      public function getNextCode() {
          $maxId = static::max('id') ?? 0;
          return 'BG-' . date('Y') . '-' . str_pad($maxId + 1, 5, '0', STR_PAD_LEFT);
      }
  }
  ```

- [x] **Task 12:** Tạo `QuotationProductPrice.php` + `QuotationHistory.php` (QuotationHistory dùng `Model` thuần, `$timestamps=false`, cast meta→array + 9 ACTION_* constants).

**Smoke test result:** 3 entities load + BomList refactored không lỗi (count OK, BomList count=22).

---

## 11.3 — BE: Services — PricingRequest (5 tasks) ✓

**File:** `hrm-api/Modules/Assign/Services/PricingRequestService.php` (đã tạo, 5 methods + 2 helpers)

- [x] **Task 13:** Tạo `PricingRequestService` với method `getFormInfo($projectId, $solutionVersionId, $solutionModuleVersionId = null)`:
  - Validate user có `sale_id === $project->sale_id` (throw 403 nếu không)
  - Resolve `bom_list_id`: `BomList::where('solution_version_id', $svId)->where('solution_module_version_id', $smvId)->where('bom_list_type', BomList::TYPE_AGGREGATE)->where('status', BomList::STATUS_HOAN_THANH)->first()` (throw 422 "Chưa có BOM tổng hợp Hoàn thành cho version này" nếu null).
  - Return: `{bom_list, project, solution, solution_version, solution_module, solution_module_version}` + customer info từ project.

- [x] **Task 14:** Method `storeDraft(array $data)`:
  - Auto code, set `status=1`, `created_by=auth()->id()`, snapshot company/department/part từ user.
  - Create record + upload files (nếu có) qua bảng `files` (reference service upload của `solution_review_profiles`).
  - Return record eager load files.

- [x] **Task 15:** Method `updateDraft(PricingRequest $req, array $data)`:
  - Validate status=1 (throw 422 nếu ≥ 2 — "Đã gửi không thể sửa").
  - Update fields, re-sync files (delete file cũ bị bỏ + upload file mới).

- [x] **Task 16:** Method `send(PricingRequest $req)`:
  - Validate status=1 + validate `created_by=auth()->id()`.
  - Update `status=2, sent_at=now()`.
  - Dispatch notification "pricing_request_sent" đến tất cả user có permission `assign.bom-list.build-price`.

- [x] **Task 17:** Method `destroy(PricingRequest $req)`:
  - Validate status=1 + `created_by=auth()->id()`.
  - Delete files + delete record.

---

## 11.4 — BE: Services — Quotation (10 tasks)

**File:** `hrm-api/Modules/Assign/Services/QuotationService.php`

- [ ] **Task 18:** Method `createFromRequest(PricingRequest $req)` — **DB transaction** để tránh race:
  - Lock `SELECT ... FOR UPDATE` trên pricing_request → validate status=2 (throw 409 nếu ≠ 2 = đã có user khác tạo).
  - Load BOM + customer info từ project.
  - Insert quotation: copy snapshot (description, deadline, delivery/warranty/payment_terms từ request) + snapshot khách hàng (id, code, name, tax_code, address, contact_name, contact_phone từ project/customer) + currency_id từ BOM + mã auto `BG-YYYY-NNNNN` + `created_by=auth()->id()` + `status=1`.
  - Update request `status=3`.
  - Log history action=`create`.
  - Return quotation eager load products.

- [ ] **Task 19:** Method `update(Quotation $q, array $data)`:
  - Validate status=1.
  - Update các field cho phép sửa: `description`, `deadline`, `delivery_time`, `warranty_time`, `payment_terms`, `validity_days`, `note`.
  - Upsert `quotation_product_prices` (mỗi bom_list_product_id 1 dòng: estimated_price, quoted_price).
  - Log history action=`save_draft`.

- [ ] **Task 20:** Method `calculateLevel(Quotation $q)`:
  - Load products + prices, tính `totalImport = Σ(estimated_price × qty)`, `totalSale = Σ(quoted_price × qty)`, `V = totalSale` (quy đổi về VND theo exchange_rate currency), `M = (totalSale - totalImport) / totalSale × 100`.
  - Lookup `bom_price_approval_configs`: `levelV` từ order_value, `levelM` từ profit_margin (logic Phase 9 giữ nguyên).
  - Return `['level' => MAX(levelV, levelM), 'total_import' => ..., 'total_sale' => ..., 'margin' => ...]`.

- [ ] **Task 21:** Method `submit(Quotation $q)`:
  - Validate status=1, `created_by=auth()->id()`, tất cả price > 0.
  - Gọi `calculateLevel` → lưu `price_approval_level`.
  - Nếu level=1: return `['level'=>1, 'can_self_approve'=>true]` — không đổi status, NLG xác nhận bước sau.
  - Nếu level=2: status→2 (Chờ TP), `submitted_at=now()`, notify users quyền TP. Log action=`submit`.
  - Nếu level=3: status→2, `submitted_at=now()`, notify users quyền TP (TP duyệt trước rồi chuyển BGĐ). Log action=`submit`.

- [ ] **Task 22:** Method `selfApprove(Quotation $q)`:
  - Validate level=1, status=1, `created_by=auth()->id()`.
  - Status→4, `approved_by=auth()->id()`, `approved_at=now()`.
  - Update `pricing_request.status=4`.
  - Notify: creator + NV KD + users quyền TP. Log action=`self_approve`.

- [ ] **Task 23:** Method `tpApprove(Quotation $q)`:
  - Validate status=2, user có quyền `approve-price-tp`.
  - Nếu level=2: status→4, `approved_by=auth()->id()`, `approved_at=now()`. Request→4. Notify. Log action=`tp_approve`.
  - Nếu level=3: status→3, `tp_approved_by=auth()->id()`, `tp_approved_at=now()`. Notify users quyền BGĐ. Log action=`tp_approve_forward`.

- [ ] **Task 24:** Method `bgdApprove(Quotation $q)`:
  - Validate status=3, user có quyền `approve-price-bgd`.
  - Status→4, `approved_by=auth()->id()`, `approved_at=now()`. Request→4. Notify. Log action=`bgd_approve`.

- [ ] **Task 25:** Method `reject(Quotation $q, string $reason)`:
  - Validate status IN (2,3), user có quyền TP (status=2) hoặc BGĐ (status=3), reason required.
  - Status→1, `rejected_reason=$reason`, clear `submitted_at, tp_approved_by/at, approved_by/at, price_approval_level`.
  - Notify creator + TP (nếu BGĐ reject). Log action=`reject`.

- [ ] **Task 26:** Method `updateSalesNote(Quotation $q, string $note)`:
  - Validate status=4, `project.sale_id === auth()->id()`.
  - Update `sales_note`. Log action=`update_sales_note` + old/new vào meta.

- [ ] **Task 27:** Method `getListForUser($userId, array $filters)`:
  - Base query + eager load (project, solution, currency, creator, productPrices).
  - Filter: user chỉ thấy `created_by=$userId` (NLG).
  - Apply filters: project_id, solution_id, solution_version_id, customer_id, status, price_approval_level, created_from/to.
  - Trả paginated result.

  Method `getPendingApproval($userId, array $filters)`:
  - Load permissions user.
  - Nếu có quyền TP → status IN (2); có quyền BGĐ → status IN (3); có cả 2 → status IN (2,3).
  - Return paginated.

---

## 11.5 — BE: Controllers + Requests + Routes (8 tasks)

**Folder:** `hrm-api/Modules/Assign/Http/Controllers/`, `Http/Requests/`

- [ ] **Task 28:** Tạo `PricingRequestController` với 7 actions (formInfo, index, show, store, update, send, destroy). Mỗi action delegate service, return transformer.

- [ ] **Task 29:** Tạo Form Requests: `PricingRequestStoreRequest`, `PricingRequestUpdateRequest` (rules: description required string, deadline nullable date, delivery_time required string max 255, warranty_time required string max 255, payment_terms required string, files array).

- [ ] **Task 30:** Tạo `QuotationController` với 14 actions (index, show, store, update, calculateLevel, submit, selfApprove, tpApprove, bgdApprove, reject, updateSalesNote, pendingApproval, exportExcel, histories).

- [ ] **Task 31:** Tạo Form Requests: `QuotationStoreRequest` (pricing_request_id required exists), `QuotationUpdateRequest`, `QuotationRejectRequest` (reason required), `QuotationSalesNoteRequest`.

- [x] **Task 32:** Sửa `BomListController.php` — xoá toàn bộ block pricing (398-586), 11 actions.

- [x] **Task 33 (partial):** Sửa `BomListService.php`:
  - [x] Xoá 2 imports BomPricingHistory + BomPricingSnapshot.
  - [x] Xoá 2 eager load `priceRequestedBy.info, priceApprovedBy.info` trong `index`.
  - [x] Xoá toàn bộ block pricing (924-1473): 11 methods + 4 helpers (notifyPricing, notifyPricingToUser, getCurrentEmployeeName, logPricingHistory, snapshotPricing, applyCommonFilters).
  - [ ] **Còn lại:** Update `syncStatusFromSubmission` để notify 4 đối tượng khi duyệt. (Sẽ làm ở Task 41-43 kèm notification refactor.)
  - [ ] **Còn lại:** Thêm validate `BomListService::update`: status≥4 throw 422. (Task 79.)

- [x] **Task 34 (partial):** Cập nhật `Routes/api.php`:
  - [x] Xoá 11 route BOM pricing + 2 list pending-*.
  - [ ] **Còn lại:** Thêm route group `/pricing-requests` + `/quotations` (sau khi có controller).

- [ ] **Task 35:** Smoke test Postman: `GET /api/v1/assign/pricing-requests` trả [], `GET /api/v1/assign/quotations` trả [], 9 route cũ trả 404.

---

## 11.6 — BE: Transformers + Excel Export (4 tasks)

**Folder:** `hrm-api/Modules/Assign/Transformers/`

- [ ] **Task 36:** Tạo `PricingRequestResource`:
  - Basic fields + status_label + eager load: bom_list (code/name/id), project (id/name/customer), solution (id/name), solution_version (number), quotation (id/code/status) — null nếu chưa có.
  - Resource cho list: bỏ files, bỏ quotation detail.
  - `DetailPricingRequestResource`: thêm `files` (array), thêm full quotation.

- [ ] **Task 37:** Tạo `QuotationResource` + `DetailQuotationResource`:
  - Basic list: code, pricing_request_code, bom_name, project, solution, version, customer_name, totals (computed), margin, level, status, created_at, creator.
  - Detail: full snapshot + products (JOIN bom_list_products + quotation_product_prices), groups (từ bom_list_groups), histories, currency object.

- [ ] **Task 38:** Tạo `Modules/Assign/Exports/QuotationExport.php`:
  - Reuse `BomListExport` pattern + template blade.
  - Template blade `resources/views/exports/quotation.blade.php`: header có mã BG, tên BOM, khách hàng snapshot (tên, MST, địa chỉ, liên hệ), điều kiện giao hàng/bảo hành/thanh toán, hiệu lực báo giá.
  - Table: giống BOM đầy đủ giá (structure từ BOM + giá từ quotation_product_prices).

- [ ] **Task 39:** QuotationController::exportExcel → return Excel download.

---

## 11.7 — BE: Notifications + Hồ sơ trình duyệt (5 tasks)

- [ ] **Task 40:** Cập nhật `SolutionReviewProfileService.php` + `SolutionModuleReviewProfileService.php` (nếu tách):
  - Bỏ xử lý input `bom_list_ids[]`.
  - Trong `store/update`: sau khi validate profile, resolve BOM auto (như PricingRequestService::getFormInfo task 13).
  - Nếu không tìm thấy BOM tổng hợp Hoàn thành theo version → throw 422.
  - Gắn BOM qua pivot `bom_list_review_profile` hoặc field cũ (tùy schema hiện tại — **đọc code trước khi sửa**).

- [ ] **Task 41:** Cập nhật hook `reviewSolutionProfileDecision` + `reviewModuleProfileDecision` (đã có trong Phase 8a Task 9-10): khi profile duyệt → `BomListService::syncStatusFromSubmission` với 4 notify targets mới.

- [ ] **Task 42:** Tạo helper/method `NotificationService` (hoặc dùng `EmployeeInfoService::sendToAllNotification` sẵn có):
  - Type `pricing_request_sent`: message "Có yêu cầu XD giá mới từ [kinh doanh] cho dự án [X]", link `/assign/pricing-requests/:id`.
  - Type `quotation_submitted_tp`: "Báo giá [BG-code] đang chờ TP duyệt", link `/assign/quotations/:id`.
  - Type `quotation_submitted_bgd`: "Báo giá [BG-code] đang chờ BGĐ duyệt".
  - Type `quotation_approved`: "Báo giá [BG-code] đã được duyệt".
  - Type `quotation_rejected`: "Báo giá [BG-code] bị từ chối. Lý do: [X]".
  - Type `bom_approved` (update text): "BOM [code] đã được duyệt" + link BOM detail.

- [ ] **Task 43:** Wire notification vào 6 điểm trong service (PricingRequestService::send, QuotationService::submit/selfApprove/tpApprove/bgdApprove/reject, BomListService::syncStatusFromSubmission).

- [ ] **Task 44:** Smoke test: tạo pricing_request → send → check `notifications` table có record cho users có quyền build-price.

---

## 11.8 — FE: Stores + Routing (3 tasks)

**Folder:** `hrm-client/store/`, `pages/assign/`

- [ ] **Task 45:** Tạo `store/pricing-request.js`:
  - Actions: `fetchList, fetchDetail, fetchFormInfo, createDraft, updateDraft, send, remove`.
  - Dùng `this.$store.dispatch('apiGetMethod'/'apiPostMethod'/'apiPutMethod'/'apiDeleteMethod')` theo convention Phase 9/10.

- [ ] **Task 46:** Tạo `store/quotation.js`:
  - Actions: `fetchList, fetchDetail, fetchPendingApproval, create, update, calculateLevel, submit, selfApprove, tpApprove, bgdApprove, reject, updateSalesNote, exportExcel, fetchHistories`.

- [ ] **Task 47:** Sửa `store/bom-list.js` — xoá 11 pricing actions (request/saveDraft/submit/selfApprove/tpApprove/approve/reject/adjust/calculateLevel/fetchPendingPricing/fetchPendingApproval).

---

## 11.9 — FE: Xoá màn cũ + refactor BomBuilderEditor (5 tasks)

- [ ] **Task 48:** Xoá 3 folder/file:
  - `pages/assign/bom-list/pending-pricing/` (folder)
  - `pages/assign/bom-list/pending-price-approval/` (folder)
  - `pages/assign/bom-list/_id/pricing.vue`

- [ ] **Task 49:** Sửa `pages/assign/bom-list/index.vue`:
  - Xoá 5 status 7-11 trong filter options.
  - Xoá cột "Cấp duyệt" nếu có.

- [ ] **Task 50:** Sửa `pages/assign/bom-list/_id/index.vue`:
  - Xoá button "Yêu cầu XD giá", "Duyệt giá", "Từ chối giá", "Điều chỉnh giá".
  - Xoá hiển thị cột giá (estimated_price, quoted_price, margin) trong detail view.
  - Xoá button xem `BomPricingHistoryModal` (đổi sang timeline của quotation).

- [ ] **Task 51:** Sửa `pages/assign/bom-list/_id/edit.vue`:
  - Xoá prop `pricingMode` trong BomBuilderEditor call.

- [ ] **Task 52:** Sửa `components/assign/bom-builder/BomBuilderEditor.vue`:
  - Giữ `pricingMode` prop (vẫn dùng cho quotation edit).
  - Đổi logic load data trong `pricingMode`: thay vì fetch BOM + pricing fields, nhận **quotation data qua prop** (quotationData: `{ info, products_with_prices, groups }`).
  - Move footer "Cấp duyệt dự kiến" logic sang parent page (vì data giờ của quotation).
  - Giữ logic edit 2 cột giá (estimated_price, quoted_price).

---

## 11.10 — FE: Popup "Yêu cầu XD giá" (4 tasks)

**Folder:** `hrm-client/components/assign/pricing-request/`

- [ ] **Task 53:** Tạo `PricingRequestModal.vue`:
  - Props: `show, projectId, solutionVersionId, solutionModuleVersionId`.
  - `mounted` khi show=true → call `fetchFormInfo` → hiện thông tin BOM auto-pick (readonly).
  - Form: mã (readonly "Tự sinh sau khi lưu"), BOM (readonly), deadline (V2BaseDatePicker), delivery_time (V2BaseInput required), warranty_time (V2BaseInput required), payment_terms (V2BaseTextarea required), description (CompactReviewEditor / CKEditor 5), upload files (reference component file của solution-review-profiles).
  - Buttons: "Lưu nháp" → `createDraft` (status=1). "Lưu và gửi" → `createDraft` + `send`. "Huỷ".
  - Toast + emit `saved` sau khi OK.

- [ ] **Task 54:** Tạo component `PricingRequestFileUpload.vue` (hoặc reuse): multiple files, drag-drop, progress, delete trước khi save.

- [ ] **Task 55:** Validate FE:
  - delivery_time/warranty_time/payment_terms required → show error per field.
  - File size max 20MB/file, total 100MB.

- [ ] **Task 56:** Test popup: mở popup → auto-pick BOM, submit draft → verify DB, submit send → verify status=2.

---

## 11.11 — FE: Màn `/assign/pricing-requests/*` (5 tasks)

**Folder:** `hrm-client/pages/assign/pricing-requests/`

- [ ] **Task 57:** Tạo `index.vue`:
  - Reuse pattern V2BaseDataTable + V2BaseFilterPanel (Phase 9 bom-list/pending-pricing cũ).
  - 2 góc nhìn (không tách tab, filter tự động):
    - NV KD (qua check `current_user.id in project.sale_ids` hoặc field `sale_id`): thấy record của mình (mọi status).
    - User có permission `Xây dựng giá Bom giải pháp`: thấy status IN (2,3).
    - BE xử lý logic phân quyền, FE chỉ gọi API.
  - Cột: STT, Mã YCBG, BOM (code+name), Dự án, Giải pháp, Version, Khách hàng, Deadline, Người YC, Ngày gửi, Trạng thái (badge color).
  - Filter cascading: Dự án → Giải pháp → Version, Khách hàng, Trạng thái (1-4), Ngày gửi.
  - Row action: Xem, "Tạo báo giá" (enable khi status=2 + `current_user` có quyền build-price + chưa có quotation).

- [ ] **Task 58:** Tạo `_id/index.vue` (chi tiết readonly):
  - Header: mã, trạng thái, ngày gửi, người yêu cầu.
  - Section info: BOM (link), Dự án, GP, Version, Khách hàng, Deadline, 3 field thương mại, description (HTML render).
  - Section file đính kèm: list + download link.
  - Section "Báo giá đã tạo": nếu có quotation → hiển thị card (mã, status, link), nếu chưa → show "Chưa có báo giá".
  - Button "Tạo báo giá" (nếu quyền + chưa có quotation + status=2): call `quotation/create` với `pricing_request_id` → redirect `/assign/quotations/:id/edit`.
  - Button "Sửa" (status=1, người tạo) → redirect edit. Button "Huỷ nháp" (status=1, người tạo).

- [ ] **Task 59:** Tạo `_id/edit.vue` (sửa nháp status=1):
  - Form giống popup modal (task 53) nhưng full page.
  - Chỉ enable khi status=1 + `created_by===me`.
  - Buttons: "Lưu nháp" (cập nhật), "Lưu và gửi" (cập nhật + send), "Huỷ".

- [ ] **Task 60:** Button "Tạo báo giá" call API:
  - Show confirm: "Bạn sẽ trở thành người làm giá cho yêu cầu này. Xác nhận?"
  - Call `POST /quotations` với `{pricing_request_id}`.
  - Nếu 409 (user khác vừa tạo): toast "Yêu cầu này đã được [user X] tiếp nhận" + refresh page.
  - Nếu OK: redirect `/assign/quotations/:id/edit`.

- [ ] **Task 61:** Thêm menu sidebar + navigation guards (required permission hoặc sale_id check).

---

## 11.12 — FE: Màn `/assign/quotations/*` (7 tasks)

**Folder:** `hrm-client/pages/assign/quotations/`

- [ ] **Task 62:** Tạo `index.vue` (danh sách báo giá):
  - Permission guard: require `Xây dựng giá Bom giải pháp`.
  - Filter API: NLG thấy `created_by=me`.
  - Cột: STT, Mã BG, Mã YCBG, BOM, Dự án, GP, Version, Khách hàng, Tổng bán, Tỷ suất LN (% + color), Cấp duyệt, Trạng thái, Ngày tạo, Người tạo.
  - Filter: Dự án cascading, Khách hàng, Trạng thái (1-4), Cấp duyệt, Ngày tạo from/to.
  - Row action: Xem, Sửa (status=1 + me), Xuất Excel, Xem lịch sử (modal timeline).

- [ ] **Task 63:** Tạo `_id/edit.vue` (màn làm giá):
  - Header: mã BG, mã YCBG, BOM link, khách hàng snapshot (readonly card).
  - Info card (editable khi status=1 + me): description (CKEditor), deadline, delivery/warranty/payment, validity_days, note (CKEditor).
  - Table: mount BomBuilderEditor `pricingMode=true` với prop `quotationData` (load qua API `/quotations/:id` include products + group + prices).
  - Hai cột editable: Giá nhập, Giá bán (reuse logic Phase 9).
  - Footer bar (sticky bottom): Tổng nhập | Tổng bán | Tỷ suất LN (color) | **Cấp duyệt dự kiến** (computed real-time qua `calculateLevel` debounce 500ms).
  - Buttons: "Lưu nháp" (PUT), "Gửi duyệt" (popup).
  - Read-only nếu status ≠ 1 (không phải editor mode).

- [ ] **Task 64:** Tạo `components/assign/quotation/QuotationSubmitModal.vue`:
  - Load `calculateLevel` khi mở → hiện level.
  - Cấp 1: message "Theo quy chế, bạn có thể tự duyệt báo giá này" + buttons "Xác nhận duyệt" (call selfApprove) / "Huỷ".
  - Cấp 2: "Báo giá cần gửi tới Trưởng phòng duyệt" + button "Xác nhận gửi" (call submit).
  - Cấp 3: "Báo giá cần gửi tới Trưởng phòng (bước 1) và Ban giám đốc (bước 2) duyệt" + button "Xác nhận gửi".
  - Toast success + redirect về list.

- [ ] **Task 65:** Tạo `_id/index.vue` (chi tiết readonly):
  - Full readonly view (info + table + footer tổng).
  - Section "Ghi chú kinh doanh" (sales_note):
    - Hiển thị khi status=4.
    - Enable edit (inline textarea + button Lưu) khi `project.sale_id===me`.
    - Button Lưu call `PUT /quotations/:id/sales-note`.
  - Section "Lịch sử phê duyệt": button mở `QuotationHistoryModal`.
  - Footer bar:
    - Button "Quay lại" (luôn có).
    - Button "Xuất Excel" (luôn có).
    - Button "In" (**disabled** + tooltip "Sẽ triển khai ở phase sau").
    - Button "Sửa" (status=1 + me) → redirect edit.
    - Button "Duyệt" (status=2 + quyền TP, hoặc status=3 + quyền BGĐ) → modal confirm → tpApprove/bgdApprove.
    - Button "Từ chối" (status IN (2,3) + quyền tương ứng) → modal nhập lý do → reject.

- [ ] **Task 66:** Tạo `components/assign/quotation/QuotationRejectModal.vue`:
  - Textarea reason (required, max 500).
  - Buttons: "Xác nhận từ chối" (call reject) / "Huỷ".

- [ ] **Task 67:** Tạo `components/assign/quotation/QuotationHistoryModal.vue`:
  - Reuse pattern Phase 9 `BomPricingHistoryModal`.
  - Timeline actions + actor + timestamp + note.

- [ ] **Task 68:** `pending-approval/index.vue`:
  - Permission guard: require `Trưởng phòng duyệt giá` OR `Ban giám đốc duyệt giá`.
  - BE auto filter theo quyền.
  - Cột giống `quotations/index.vue` + cột "Người gửi" + "Ngày gửi".
  - Click row → `/assign/quotations/:id` (không phải edit).

---

## 11.13 — FE: Tab Hồ sơ + Tab Báo giá trong dự án tiền khả thi (4 tasks)

**File:** `hrm-client/pages/assign/prospective-projects/_id/manager.vue`

- [ ] **Task 69:** Sửa tab "Hồ sơ":
  - Filter API mặc định chỉ status = Đã duyệt.
  - Thêm cột "BOM list": render `bom.code . bom.name` + link `/assign/bom-list/:id`.
  - Thêm cột Actions: button "Yêu cầu XD giá" (chỉ show khi `project.sale_id===me` + profile status=Đã duyệt).
  - Button click → mở `PricingRequestModal` với `projectId, solutionVersionId, solutionModuleVersionId` từ profile.

- [ ] **Task 70:** Thêm tab "Báo giá" (mới):
  - List quotation status=4 của project.
  - Gọi API `GET /prospective-projects/:id/quotations`.
  - Cột: STT, Mã BG, Mã YCBG, BOM, Version, Tổng bán, Tỷ suất LN, Ngày duyệt, Người duyệt, Actions.
  - Actions: Xem (→ `/assign/quotations/:id`), Sửa sales_note (inline hoặc popup), In (disabled), Xuất Excel.

- [ ] **Task 71:** Component inline `QuotationSalesNoteInline.vue`: textarea + button Lưu + Huỷ inline trong row.

- [ ] **Task 72:** Test 2 tabs end-to-end: mở dự án → thấy tab Hồ sơ có button yêu cầu → tạo request → mở tab Báo giá thấy quotation sau khi duyệt.

---

## 11.14 — FE: Hồ sơ trình duyệt + Menu Sidebar (4 tasks)

- [ ] **Task 73:** Sửa `pages/assign/solution-review-profiles/create.vue` + `_id/edit.vue`:
  - Bỏ field "Chọn BOM list" hoàn toàn (remove input UI + remove từ payload).
  - Thêm hint text ở đầu form: "BOM list sẽ tự động lấy theo version giải pháp của hồ sơ".

- [ ] **Task 74:** Cập nhật `layouts/default.vue` (hoặc file menu sidebar — tìm qua grep nếu không có):
  - Xoá item "BOM chờ XD giá" (`/assign/bom-list/pending-pricing`).
  - Xoá item "BOM chờ duyệt giá" (`/assign/bom-list/pending-price-approval`).
  - Thêm "Yêu cầu xây dựng giá" (`/assign/pricing-requests`) — isShow: user có sale_id hoặc quyền build-price.
  - Thêm "Danh sách báo giá" (`/assign/quotations`) — isShow: quyền `Xây dựng giá Bom giải pháp`.
  - Thêm "Báo giá chờ duyệt" (`/assign/quotations/pending-approval`) — isShow: quyền TP hoặc BGĐ.
  - Giữ "Cấu hình duyệt giá" (`/assign/settings/price-approval`) như cũ.

- [ ] **Task 75:** Cập nhật route guards (middleware `auth.js` hoặc per-page) — đảm bảo permission check đúng.

- [ ] **Task 76:** Cleanup: grep toàn bộ FE codebase tìm reference "pricingMode", "bom_pricing", "pricing_version" còn sót lại → xoá/sửa.

---

## 11.15 — Fix notifications text + BOM detail (3 tasks)

- [ ] **Task 77:** Grep text notification trong BE có chứa "BOM" trong context duyệt giá → đổi thành "Báo giá" theo spec user.

- [ ] **Task 78:** Fix text label trong FE (filter dropdown, status badge) — toàn bộ references "BOM chờ duyệt giá/XD giá" → thay đổi sang "Báo giá chờ duyệt"/"Yêu cầu XD giá".

- [ ] **Task 79:** Bổ sung validate BE trong `BomListService::update`: status≥4 throw 422 "BOM đã duyệt không thể sửa. Nếu cần thay đổi, liên hệ NV KD tạo yêu cầu XD giá mới".

---

## 11.16 — Test thủ công end-to-end (10 tasks)

- [ ] **Task 80:** **Module 1 — BOM strip pricing:**
  - [ ] Mở bom-list/index.vue → filter không còn status 7-11
  - [ ] Mở BOM status=4 → không có button pricing
  - [ ] Thử gọi 9 API cũ (`/bom-lists/:id/request-pricing`, v.v.) → 404
  - [ ] Sửa BOM status=4 qua API → 422 "không thể sửa"
  - [ ] Duyệt hồ sơ trình duyệt → BOM 2→4, 4 notification gửi (check bảng notifications)

- [ ] **Task 81:** **Module 2 — Auto-pick BOM:**
  - [ ] Tạo hồ sơ trình duyệt không có BOM Hoàn thành cho version → submit → 422 rõ message
  - [ ] Tạo BOM tổng hợp Hoàn thành cho version → submit → OK, BOM gắn đúng

- [ ] **Task 82:** **Module 3 — PricingRequest CRUD:**
  - [ ] NV KD của project mở tab Hồ sơ → thấy button "Yêu cầu XD giá"
  - [ ] Mở popup → auto-pick BOM đúng
  - [ ] Lưu nháp → status=1
  - [ ] Mở sửa → fields load đúng
  - [ ] Upload 2 file → lưu thành công
  - [ ] Lưu và gửi → status=2 + notification gửi đến users quyền build-price
  - [ ] Thử sửa khi status=2 → block 422
  - [ ] NV KD khác mở list → không thấy request của mình

- [ ] **Task 83:** **Module 4 — Tạo báo giá:**
  - [ ] User quyền build-price mở list pricing-requests status=2 → thấy button "Tạo báo giá"
  - [ ] Click → confirm → redirect edit quotation
  - [ ] Snapshot đầy đủ: customer_name, tax_code, address, contact, 4 field thương mại, description
  - [ ] Request → status=3
  - [ ] User khác cùng click "Tạo báo giá" → toast 409 "đã được X tiếp nhận"

- [ ] **Task 84:** **Module 5 — Quotation pricing + workflow:**
  - [ ] Mở edit quotation → fill giá → cấp duyệt dự kiến update realtime
  - [ ] Lưu nháp → reload thấy giá đã lưu
  - [ ] Gửi duyệt cấp 1 (quote nhỏ) → popup tự duyệt → xác nhận → status=4
  - [ ] Tạo quotation mới → gửi duyệt cấp 2 → status=2
  - [ ] User quyền TP mở pending-approval → thấy, duyệt → status=4
  - [ ] Tạo quotation cấp 3 → submit → status=2
  - [ ] TP "Duyệt & chuyển BGĐ" → status=3
  - [ ] BGĐ duyệt → status=4
  - [ ] Reject ở bất kỳ bước → quay về status=1, lưu reason

- [ ] **Task 85:** **Module 6 — Sales note:**
  - [ ] NV KD mở tab Báo giá → edit sales_note → lưu OK
  - [ ] User khác (không phải sale_id) → không thấy button edit
  - [ ] Quotation status ≠ 4 → field ẩn

- [ ] **Task 86:** **Module 7 — Tab Hồ sơ/Báo giá:**
  - [ ] Tab Hồ sơ filter status=Đã duyệt, cột BOM có link
  - [ ] Tab Báo giá hiển thị quotation Đã duyệt
  - [ ] Action In disabled + tooltip
  - [ ] Action Xuất Excel download OK

- [ ] **Task 87:** **Module 8 — Export Excel:**
  - [ ] Xuất Excel báo giá → có snapshot khách hàng
  - [ ] Có 4 field thương mại
  - [ ] Structure BOM giữ nguyên + giá từ quotation_product_prices

- [ ] **Task 88:** **Module 9 — Navigate màn cũ:**
  - [ ] Gõ URL `/assign/bom-list/pending-pricing` → 404
  - [ ] `/assign/bom-list/:id/pricing` → 404
  - [ ] Menu sidebar không còn item cũ

- [ ] **Task 89:** **Module 10 — Phân quyền:**
  - [ ] NV KD không có quyền build-price → không thấy menu "Danh sách báo giá"
  - [ ] User không có quyền TP/BGĐ → không thấy menu "Báo giá chờ duyệt"
  - [ ] TP có cả quyền BGĐ → thấy status IN (2,3) trong pending-approval
  - [ ] NV KD chỉ thấy pricing_requests của mình
  - [ ] NLG chỉ thấy quotations của mình

---

## Checkpoints

### Checkpoint — 2026-04-15
Vừa hoàn thành (session 1):
- **Nhóm 11.1 (Migrations):** 7 migrations — drop `bom_pricing_snapshots` + `bom_pricing_histories`, drop 9 cột pricing trên `bom_lists`, reset status 7-11→4, create 4 bảng mới. `php artisan migrate` OK.
- **Nhóm 11.2 (Entities):** xoá 5 status 7-11 + 4 relationship pricing trong `BomList.php`; tạo 4 entity mới; xoá 2 file `BomPricingHistory.php` + `BomPricingSnapshot.php`.
- **Strip pricing cũ:** xoá block 550 dòng trong `BomListService`, 11 actions trong `BomListController`, 13 routes.
- **Nhóm 11.3 (PricingRequestService):** 5 method + 2 helper.

### Checkpoint — 2026-04-15 (session 2)
Vừa hoàn thành:
- **Nhóm 11.4 (QuotationService):** 10 method — createFromRequest (race-safe với lockForUpdate), update, upsertPrices, calculateLevel, calculateTotals, submit (cấp 1/2/3), selfApprove, tpApprove (cấp 2→4 / cấp 3→3), bgdApprove, reject (với reason, clear fields), updateSalesNote, getListForUser, getPendingApproval (union TP+BGĐ); 3 notify methods (notifyByPermission, notifyApproved, notifyRejected).
- **Nhóm 11.5 (Controllers + Requests + Routes):**
  - Form Requests: 5 file (PricingRequestStore/Update, QuotationStore/Update/Reject).
  - Controllers: `PricingRequestController` (7 actions), `QuotationController` (14 actions).
  - Routes: thêm 20 route mới (`/pricing-requests`, `/quotations`, form-info, quotations-by-project). Tất cả resolve OK qua DI.
- **Nhóm 11.6 (Transformers):** 4 resource mới (`PricingRequestResource`, `DetailPricingRequestResource`, `QuotationResource`, `DetailQuotationResource`). Tạm hoãn Task 38-39 (Excel export) — cần template blade riêng.
- **Nhóm 11.7:**
  - Update `BomListService::syncStatusFromSubmission`: khi approved → notify 4 đối tượng (người gửi hồ sơ, PM GP, người lập BOM, NV KD dự án) qua `notifyBomApproved`.
  - Update `SolutionService::storeSolutionReviewProfile` + `SolutionModuleService::storeReviewProfile`: bỏ input `bom_list_ids`, auto-pick BOM tổng hợp Hoàn thành theo version khi submit, throw 422 nếu không có match.
- **Task 79:** BomListService::update đã có validate status ≤ 2 từ trước — không cần sửa.

Đang làm dở: Không.

Bước tiếp theo:
1. **Test BE end-to-end qua Postman** — verify flow Phase 11 hoạt động (tạo pricing_request, tạo quotation, workflow duyệt, notifications).
2. **Task 38-39 (Excel export báo giá)** — làm khi có thời gian, cần template blade riêng với section khách hàng + 4 field thương mại.
3. **Nhóm 11.8+ (FE):** 40+ tasks — stores, màn pricing-requests, màn quotations, popup yêu cầu XD giá, tab Hồ sơ/Báo giá trong dự án tiền khả thi, menu sidebar, cleanup BOM FE cũ, test.

Blocked: Không.

### Checkpoint — 2026-04-15 (session 3)
Vừa hoàn thành:
- **Nhóm 11.9 (Xoá FE cũ + cleanup):**
  - Xoá folder `bom-list/pending-pricing/`, `bom-list/pending-price-approval/`, file `bom-list/_id/pricing.vue`, component `BomPricingHistoryModal.vue`.
  - Cleanup `bom-list/index.vue`: xoá 5 status 7-11 trong filter, xoá button "Yêu cầu XD giá" + "Lịch sử phê duyệt giá" + handler, xoá import BomPricingHistoryModal.
  - Rewrite `bom-list/_id/index.vue`: xoá toàn bộ buttons pricing (Yêu cầu XD giá, Duyệt giá, Từ chối, Điều chỉnh, Lịch sử) + 2 modal + logic liên quan. Giữ readonly view + button Quay lại + Xuất Excel.
- **Nhóm 11.10 (Popup):** Tạo `PricingRequestFormModal.vue` — popup tạo YCBG với form đầy đủ (deadline, delivery_time, warranty_time, payment_terms, description, file upload) + 2 mode (Lưu nháp / Lưu và gửi).
- **Nhóm 11.11 (pricing-requests pages):** Tạo 3 page:
  - `/assign/pricing-requests/index.vue` — list với filter + actions (Xem, Sửa, Tạo báo giá)
  - `/assign/pricing-requests/_id/index.vue` — chi tiết readonly + file attachments + link quotation
  - `/assign/pricing-requests/_id/edit.vue` — sửa nháp (form full page)
- **Nhóm 11.12 (quotations pages + modals):** Tạo 5 file:
  - `/assign/quotations/index.vue` — list báo giá (NLG xem của mình)
  - `/assign/quotations/_id/index.vue` — chi tiết với actions TP/BGĐ duyệt + từ chối + sales note edit (NV KD only) + table readonly
  - `/assign/quotations/_id/edit.vue` — làm giá (edit 2 cột giá + info card + footer realtime tổng + cấp duyệt dự kiến)
  - `/assign/quotations/pending-approval/index.vue` — list chờ duyệt (TP/BGĐ)
  - `QuotationRejectModal.vue` + `QuotationSubmitModal.vue` (cấp 1 tự duyệt, cấp 2/3 gửi)
- **Nhóm 11.13 (Tab Hồ sơ update):**
  - `ProspectiveProjectReviewProfilesTab.vue`: thêm cột "BOM list" (link), thêm button "Yêu cầu XD giá" (chỉ NV KD + hồ sơ Đã duyệt), integrate `PricingRequestFormModal`.
  - `manager.vue`: truyền prop `main-sale-employee-id` xuống tab.
  - BE `ProspectiveProjectService::getReviewProfiles` thêm field `bom_list` (first) vào response.
- **Nhóm 11.14 (Menu sidebar):** Xoá "BOM chờ XD giá", "BOM chờ duyệt giá". Thêm "Yêu cầu XD giá", "Danh sách báo giá", "Báo giá chờ duyệt".

Đang làm dở: Không.

Bước tiếp theo: Đã hoàn thành ở session 4.

Blocked: Không.

### Checkpoint — 2026-04-17 (session 8-12) — Test UI + Fix bugs + UX polish + Phân quyền

Vừa hoàn thành — **~30 fix/enhancement từ test thủ công**:

**Form YCBG:**
- Fix upload file (S3 trả string URL, không phải object) + BE prepareForValidation filter file rỗng
- Rewrite popup theo pattern chuẩn (header icon + V2BaseButton footer + file chip inline)
- Popup xem chi tiết YCBG (table key-value compact, reuse ở tab Hồ sơ + list)

**Màn show báo giá:**
- Info table key-value, topbar title+status (v-html global style), page-content bg trắng
- Collapsible "Thông tin chung", sticky header + footer products table
- Tỷ suất LN từng dòng + tổng, font-weight 300 cho table body
- V2BaseButton chuẩn (light/secondary/primary/success/danger), popup YCBG + lịch sử
- Button "Quay lại" → $router.go(-1)
- Phân quyền can_view_import_price: KD không xem giá nhập/tỷ suất chi tiết, xem tỷ suất tổng

**Màn edit báo giá:**
- Layout giống show (info table + collapsible + sticky)
- Bỏ deadline, thêm Giải pháp+Hạng mục cùng row Dự án
- Required 4 field (hiệu lực/giao hàng/bảo hành/tiền tệ) + validate giá >0 khi submit + cell-invalid highlight
- Đổi currency → cảnh báo confirm + reactive currencyCode/exchangeRate toàn form
- Cấp duyệt client-side realtime (load configs, không cần call API) + quy đổi VND
- Điều khoản thanh toán + ghi chú nội bộ: CKEditor rich text, section cuối báo giá
- Footer pricing compact (font 11-11.5px, label rút gọn, responsive @media ≤1366px)
- Lưu nháp skip validate + redirect danh sách, gửi duyệt strict + redirect danh sách
- Cấp 3 rõ 2 bước: "C3 — TP & BGĐ" + popup submit flow visual (2 step pill)

**Danh sách báo giá:**
- 12 cột (tiền tệ, tổng giá trị, người tạo, ngày tạo, cấp duyệt label, người duyệt, ngày duyệt)
- Column customization (ColumnCustomizationModal + API quotations)
- Bộ filter đầy đủ: V2BaseCompanyDepartmentFilter → Dự án → GP → Version (cascading) → Khách hàng → Trạng thái → Cấp duyệt → Người duyệt → Ngày tạo
- Button lịch sử (QuotationHistoryModal rewrite theo BOM cũ — icon circle + màu theo action)

**Phân quyền:**
- Migration 7 permissions group "Báo giá" (4 cấp xem + XD giá + TP + BGĐ), bỏ "Tạo Báo giá"
- Chuyển 3 permission pricing từ group "BOM List" → "Báo giá"
- BE checkPermissionListWithColumn cho danh sách báo giá
- DetailQuotationResource.can_view_import_price (người tạo/duyệt/quản lý xem đầy đủ, KD chỉ xem giá bán + tỷ suất tổng)

**Global:**
- Notification mobile: APP_NAME_MOBILE, strip_tags HTML body
- Layout: padding 15→5px (custom-assign.scss), pt-2→pt-1 (7 pages)
- PageTitleMixin cho 15 trang Assign thiếu + 2 trang pricing-requests
- BomBuilderEditor: bỏ PageHeader cũ, bỏ select tiền tệ, bỏ currencySymbol header cột
- V2BaseDataTable: slot row-expand cho sub-table inline
- SidebarMenu: v-html pageTitle + global CSS cho status/level inline

Đang làm dở: Không.
Bước tiếp: User test end-to-end flow hoàn chỉnh.
Blocked: Không.

---

### Checkpoint — 2026-04-16 (session 7) — Redesign Tab Hồ sơ + Expand YCBG

Vừa hoàn thành:

1. **Migration cột `approved_at`** cho `solution_review_profiles` + `solution_module_review_profiles` (`2026_04_16_100001`) — kèm backfill `updated_at` cho profile đã approved.
2. **BE services**: `reviewSolutionProfileDecision` + `reviewModuleProfileDecision` set `approved_at = now()` khi `action=approve`.
3. **Entity casts**: 2 model review profile thêm `'approved_at' => 'datetime'`.
4. **`ProspectiveProjectService::getReviewProfiles`** rewrite filter + output:
   - Chỉ hiện profile `status=approved` (tab Hồ sơ)
   - Bỏ filter: status, sent_date_from/to, review_deadline_from/to
   - Thêm filter: approved_date_from/to (theo `approved_at`)
   - Default sort: `approved_at DESC`
   - Batch load `pricing_requests` với eager `quotation` + `creator.info` theo `bom_list_id`
   - Output thêm: `approved_at` (formatted), `approved_at_raw`, `pricing_requests[]`, `pricing_requests_count`
5. **V2BaseDataTable**: thêm slot `row-expand` để consumer render sub-table inline dưới row chính (truyền `item`, `index`, `colspan`).
6. **`ProspectiveProjectReviewProfilesTab.vue`** rewrite toàn bộ:
   - Filter chỉ 3 field: Version GP, Ngày duyệt từ/đến
   - Cột mới: `expand` (button toggle với count badge) | STT | Mã hồ sơ | Version GP | BOM list | Ngày duyệt | Thao tác
   - Button action icon-only: "Xem" (ri-eye-line), "Yêu cầu XD giá" (ri-price-tag-3-line text-primary) với tooltip
   - Expanded sub-table inline: STT, Mã YCBG (link), Người gửi, Ngày gửi, Deadline, Trạng thái (badge), Báo giá (link nếu có), Ngày duyệt báo giá, Action
   - Load version options từ endpoint `solutions/{id}/versions`
   - CSS polish: expand arrow rotate, count badge, sub-table style

Đang làm dở: Không.

Bước tiếp theo: User test UI mới.

Blocked: Không.

---

### Checkpoint — 2026-04-15 (session 6) — Bug fixes từ test UI

Vừa hoàn thành — **xử lý 9 bug + 1 cleanup từ test thủ công của user**:

1. **Bug: Form BOM list vẫn hiển thị cột "Giá bán", "Thành tiền bán", "Tỷ suất LN"**
   - `BomBuilderEditor`: tắt `visibleColumns.salePrice/amount/profitMargin = false` + xoá khỏi `columnOptions`

2. **Bug: Popup thêm nhanh / sửa nhanh / import / export hàng hoá vẫn có "Giá bán"**
   - `BomBuilderAddProductModal`: xoá input "Giá bán", nới col Ghi chú
   - `BomBuilderEditModal`: xoá input "Đơn giá báo giá" + cập nhật banner ERP
   - `BomExportModal`: xoá 3 option (sale_price/amount/profit_margin)
   - `BomBuilderImportModal`: xoá cột SalePrice + validation
   - `BomListController::importTemplate`: xoá cột "Đơn giá bán" trong template Excel

3. **Cleanup triệt để "giá bán" khỏi BOM (theo phản biện của user về việc spec đã ghi rõ mà vẫn sót)**
   - Migration `2026_04_14_100008_drop_quoted_price_from_bom_list_products`
   - `BomListProduct`: xoá `getSaleTotalAttribute` + `getProfitMarginAttribute`
   - `BomListService`: xoá `quoted_price` trong validateImportData + buildProductPayload + mapProductPayload
   - `DetailBomListResource`: xoá 3 field quoted_price/sale_total/profit_margin
   - `BomBuilderEditor.buildSavePayload` + `buildPayloadFromRow`: xoá emit `quoted_price`
   - `QuotationController::exportExcel`: tính lại profit_margin tại chỗ (vì accessor đã bỏ)

4. **Bug: BOM thành phần status="Hoàn thành" không hiển thị khi tạo BOM tổng hợp cấp hạng mục**
   - `BomBuilderEditor.filteredSubBoms`: thay strict equal version bằng `looseVersionMatch` — BOM con/parent không có version → cho qua (tương thích data cũ)

5. **Bug: Lưu nháp BOM không nhập tên → lỗi SQL hiển thị toast**
   - `BomListStoreRequest`: `name` luôn `required` (cả khi nháp), match cột DB NOT NULL
   - FE: `<V2BaseError :message="formError.name" />` đã có sẵn → tự render error

6. **Bug: Tab Hồ sơ trình duyệt vẫn hiện text generic "BOM tự động lấy" cả khi đang duyệt**
   - `ModuleApprovalModal` + `SolutionApprovalModal`: thêm `previewBom` data + `loadPreviewBom()` method
   - Hiện 3 trạng thái UI: loading spinner / alert xanh có link mã+tên BOM (mở tab mới) / alert đỏ "Chưa có BOM"
   - Profile đã có `bom_quotes` → dùng cái đầu; chưa có → query `bom-lists/getAll` filter version
   - BE `BomListController::getAll`: thêm filter `bom_list_type`, `status`, `only_aggregate_solution_level`

7. **Debug: Notify "gửi cả app" khi duyệt hồ sơ module**
   - `BomListService::notifyBomApproved`: thêm `Log::info` ghi rõ recipients + sources mapping → user cung cấp log để trace

8. **Bug: Tab Hồ sơ không thấy button "Yêu cầu XD giá"**
   - `manager.vue`: thay `projectData` (không tồn tại) → `tktForm.main_sale_employee_id` (cả 2 chỗ tab Hồ sơ + tab Báo giá)
   - `ProspectiveProjectReviewProfilesTab` + `ProspectiveProjectQuotationsTab` + `quotations/_id/index.vue`: thay `$store.state.auth?.user?.employee_id` → `$store.state.current_employee?.id` (theo mixin `CheckPermission`)

9. **Bug: "Chưa có BOM tổng hợp Hoàn thành" hiển thị nhầm khi yêu cầu XD giá**
   - `PricingRequestService::getFormInfo`: đổi filter `STATUS_HOAN_THANH` (2) → `STATUS_DA_DUYET` (4) — yêu cầu XD giá chỉ khi BOM đã được duyệt qua hồ sơ
   - Loose version match (giống fix #4) — BOM cũ không có version vẫn match được
   - Thêm log Warning với criteria + candidates khi không tìm thấy BOM
   - Đổi message lỗi rõ ràng hơn

Đang làm dở: Không.

Bước tiếp theo:
- User test tiếp các flow còn lại (tạo PricingRequest end-to-end, làm giá, duyệt cấp 1/2/3, sales note)
- Em chờ feedback bug tiếp theo

Blocked: Không.

---

### Checkpoint — 2026-04-15 (session 5) — Polish + enhancements
Vừa hoàn thành:
- **Render groups + parent-child** trong cả edit + detail quotation pages — render theo nhóm La Mã (I, II, III), hàng cha đậm, hàng con indent + text-muted, badge "DV" cho dịch vụ, row TỔNG với nền cam.
- **Fix computed total**: loại bỏ parent-có-children khỏi tổng (tránh trùng với children).
- **Fix file upload FE**: chuyển từ `$axios.post('/api/v1/files/upload', ...)` sang `$store.dispatch('uploadImage', formData)` với key `attachments[]` (match backend endpoint).
- **Cleanup BE transformers**: xoá 10 pricing fields cũ khỏi `BomListListResource` + `DetailBomListResource` (reference đến fields đã drop + relationships đã xoá khỏi BomList entity).
- **Quotation History Modal**: tạo `QuotationHistoryModal.vue` + button "Lịch sử" trong detail page (timeline đầy đủ 9 actions với color dot + actor + meta.reason/level/note).
- **Fix buildFileUrl** trong pricing-request detail — dùng file_path trực tiếp (đã là S3 URL đầy đủ).

### Checkpoint — 2026-04-15 (session 4)
Vừa hoàn thành — **Phase 11 code COMPLETE (85/89 tasks, 96%)**:
- **Task 70-72 (Tab Báo giá):** Tạo `ProspectiveProjectQuotationsTab.vue` — list quotation Đã duyệt của project với cột Mã BG/BOM/Version/Khách hàng/Ngày duyệt + actions Xem, Sửa sales_note (NV KD only, modal inline), In (disabled), Xuất Excel. Wire vào `manager.vue`: import component, thêm tab `'quotations'`, show panel, truyền props project-id + main-sale-employee-id.
- **Task 73 (Bỏ chọn BOM FE):** Sửa `SolutionApprovalModal.vue` + `ModuleApprovalModal.vue` — thay `BomListTable` picker bằng alert info "BOM tổng hợp sẽ tự động được lấy theo version khi gửi hồ sơ". Xoá payload `bom_list_ids` khỏi 2 form (BE đã auto-pick rồi).
- **Task 38-39 (Excel export):** Implement `QuotationController::exportExcel` — load quotation + override giá từ `quotation_product_prices` vào BOM products → reuse `BomListExport` class với template `exports.bom_list` hiện có. Thêm route `GET /api/v1/assign/quotations/{id}/export-excel`.

Đang làm dở: Không.

Bước tiếp theo: **User test thủ công end-to-end** theo 10 module Task 80-89:
1. BOM strip pricing (status 1-6, lock ≥4, notify 4 targets khi duyệt)
2. Hồ sơ trình duyệt auto-pick BOM
3. PricingRequest CRUD + send + upload file
4. Tạo báo giá race-safe từ request
5. Quotation workflow cấp 1/2/3 + reject → về 1
6. Sales note NV KD only
7. Tab Hồ sơ + tab Báo giá trong dự án tiền khả thi
8. Export Excel quotation
9. Navigate màn cũ → 404
10. Phân quyền menu + list theo role

Blocked: Không.

---

## Checkpoint template (tham khảo)

```markdown
### Checkpoint — YYYY-MM-DD
Vừa hoàn thành: [task X]
Đang làm dở: [file + line + dừng đâu]
Bước tiếp theo: [hành động cụ thể]
Blocked: [để trống nếu không có]
```
