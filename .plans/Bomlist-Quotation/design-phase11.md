# Design Phase 11 — Tách BOM và Báo giá (Update logic 14/04/2026)

**Ngày brainstorm:** 2026-04-15
**Người phụ trách:** @dnsnamdang

---

## 1. Scope & Nguyên tắc

### 1.1 Mục tiêu
Tách `bom_lists` và `quotations` thành 2 entity độc lập, đưa vai trò Kinh doanh (Sales) vào workflow xây dựng giá, tinh giản workflow BOM.

### 1.2 Breaking change (local dev, cho phép clear data)
- BOM không còn quản lý giá. Status BOM chỉ còn 1..6 (Đang tạo → Hoàn thành → Chờ duyệt → Đã duyệt / Đã được tổng hợp / Không duyệt).
- Xoá toàn bộ cơ chế version báo giá + snapshot + "Điều chỉnh giá" (Phase 10).
- Tách thành 2 entity mới: `pricing_requests` (kinh doanh) + `quotations` (người làm giá). 1 BOM → N báo giá (độc lập).
- Sửa báo giá Đã duyệt = không làm. Muốn thay đổi → tạo yêu cầu XD giá mới → sinh báo giá mới.
- Không thêm permission mới. Kinh doanh xác định bằng `prospective_projects.sale_id = current_user.id`.
- BOM lock (read-only) từ status=Đã duyệt. Quotation chỉ override `estimated_price` + `quoted_price` qua bảng riêng; qty/spec/structure giữ y BOM.
- Config duyệt giá (`bom_price_approval_configs` + logs) giữ nguyên — dùng chung cho quotation.

### 1.3 Quyết định quan trọng (đã chốt brainstorming)
| # | Điểm | Quyết định |
|---|---|---|
| 1 | Migration strategy | A — local dev, drop & reset (đã clear được data cũ) |
| 2 | Quan hệ BOM ↔ Quotation | C — BOM lock sau Đã duyệt, quotation link động qua `bom_id` + bảng `quotation_product_prices` riêng |
| 3 | Pricing Request vs Quotation | B — 2 entity tách riêng (KPI khác, user khác) |
| 4 | Quotation có sửa structure products? | a — chỉ sửa giá. Qty/spec/structure giữ y BOM |
| 5 | Workflow duyệt | Giữ nguyên Phase 10 — cấp 1 tự duyệt, cấp 2 TP duyệt, cấp 3 TP→BGĐ 2 bước |
| 6 | "Điều chỉnh giá" | Xoá hoàn toàn — thay bằng "tạo yêu cầu mới" |
| 7 | Auto-pick BOM trong hồ sơ | A — match theo `solution_version_id`, không có → 422 |
| 8 | Permission mới cho kinh doanh | Không thêm, check `project.sale_id` |
| 8c | Race tạo báo giá | Y — ai tạo trước thành NLG, DB transaction chặn |
| 9 | Sales note | Field riêng `sales_note`, hiện khi quotation Đã duyệt, chỉ NV KD nhập |
| 10 | Fields phiếu YCBG | Mã auto, ghi chú text, file đính kèm, deadline, delivery_time*, warranty_time*, payment_terms* |
| 11 | Kiểu dữ liệu 3 field | Text tự do cả 3. Copy snapshot sang quotation. Sau gửi lock |
| 12 | Màn cũ Phase 9/10 | Xoá/đổi tên theo mapping section 4 |
| 13 | In báo giá PDF | Để phase sau, tạm button disabled |
| 13b | Phân quyền theo cấp | NV KD thấy của mình, NLG thấy của mình, TP/BGĐ theo quyền |

---

## 2. Data model

### 2.1 Sửa `bom_lists`
- **DROP columns:** `price_approved_by`, `price_approved_at`, `price_rejected_reason`, `price_approval_level`, `price_requested_by`, `price_requested_at`, `pricing_version`, `tp_approved_by`, `tp_approved_at`.
- **DROP tables:** `bom_pricing_snapshots`, `bom_pricing_histories`.
- **Reset data:** `UPDATE bom_lists SET status = 4 WHERE status IN (7,8,9,10,11)`.
- Xoá 5 status constant STATUS_CHO_XAY_DUNG_GIA ... STATUS_DA_DUYET_GIA khỏi Entity.

### 2.2 Table mới `pricing_requests`
```php
Schema::create('pricing_requests', function (Blueprint $table) {
    $table->id();
    $table->string('code', 30)->unique();                // YCBG-YYYY-NNNNN
    $table->unsignedBigInteger('bom_list_id');
    $table->unsignedBigInteger('project_id');
    $table->unsignedBigInteger('solution_id');
    $table->unsignedBigInteger('solution_version_id');   // NOT NULL
    $table->unsignedBigInteger('solution_module_id')->nullable();
    $table->unsignedBigInteger('solution_module_version_id')->nullable();

    $table->text('description');
    $table->date('deadline')->nullable();
    $table->string('delivery_time');                     // Required
    $table->string('warranty_time');                     // Required
    $table->text('payment_terms');                       // Required

    $table->tinyInteger('status')->default(1);           // 1=Đang tạo, 2=Chờ XD, 3=Đang XD, 4=Đã có BG
    $table->timestamp('sent_at')->nullable();

    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->unsignedBigInteger('company_id')->nullable();
    $table->unsignedBigInteger('department_id')->nullable();
    $table->unsignedBigInteger('part_id')->nullable();
    $table->timestamps();

    $table->index(['bom_list_id', 'status']);
    $table->index(['project_id', 'created_by']);
});
```

**File đính kèm**: dùng bảng `files` chung (polymorphic qua `table='pricing_requests' + table_id=id`). Không tạo bảng riêng.

### 2.3 Table mới `quotations`
```php
Schema::create('quotations', function (Blueprint $table) {
    $table->id();
    $table->string('code', 30)->unique();                        // BG-YYYY-NNNNN
    $table->unsignedBigInteger('pricing_request_id')->unique();  // 1-1
    $table->unsignedBigInteger('bom_list_id');
    $table->unsignedBigInteger('project_id');
    $table->unsignedBigInteger('solution_id');
    $table->unsignedBigInteger('solution_version_id');           // NOT NULL
    $table->unsignedBigInteger('solution_module_id')->nullable();
    $table->unsignedBigInteger('solution_module_version_id')->nullable();
    $table->unsignedBigInteger('currency_id');

    // Snapshot từ request
    $table->text('description');
    $table->date('deadline')->nullable();
    $table->string('delivery_time');
    $table->string('warranty_time');
    $table->text('payment_terms');
    $table->integer('validity_days')->nullable();                // Thời gian hiệu lực báo giá (số ngày)

    // Snapshot khách hàng (lock tại thời điểm tạo BG)
    $table->unsignedBigInteger('customer_id');
    $table->string('customer_code', 30)->nullable();
    $table->string('customer_name');
    $table->string('customer_tax_code', 30)->nullable();
    $table->string('customer_address')->nullable();
    $table->string('customer_contact_name')->nullable();
    $table->string('customer_contact_phone', 30)->nullable();

    $table->text('note')->nullable();         // Ghi chú nội bộ NLG
    $table->text('sales_note')->nullable();   // Ghi chú kinh doanh (sau Đã duyệt)

    $table->tinyInteger('status')->default(1); // 1=Đang tạo, 2=Chờ TP, 3=Chờ BGĐ, 4=Đã duyệt (reject → quay về 1)
    $table->tinyInteger('price_approval_level')->nullable();
    $table->unsignedBigInteger('tp_approved_by')->nullable();
    $table->timestamp('tp_approved_at')->nullable();
    $table->unsignedBigInteger('approved_by')->nullable();
    $table->timestamp('approved_at')->nullable();
    $table->text('rejected_reason')->nullable();
    $table->timestamp('submitted_at')->nullable();

    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->unsignedBigInteger('company_id')->nullable();
    $table->unsignedBigInteger('department_id')->nullable();
    $table->unsignedBigInteger('part_id')->nullable();
    $table->timestamps();

    $table->index(['bom_list_id', 'status']);
    $table->index(['created_by', 'status']);
});
```

### 2.4 Table mới `quotation_product_prices`
```php
Schema::create('quotation_product_prices', function (Blueprint $table) {
    $table->id();
    $table->unsignedBigInteger('quotation_id');
    $table->unsignedBigInteger('bom_list_product_id');
    $table->decimal('estimated_price', 15, 2)->default(0);
    $table->decimal('quoted_price', 15, 2)->default(0);
    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->timestamps();

    $table->unique(['quotation_id', 'bom_list_product_id']);
});
```

### 2.5 Table mới `quotation_histories`
```php
Schema::create('quotation_histories', function (Blueprint $table) {
    $table->id();
    $table->unsignedBigInteger('quotation_id');
    $table->string('action', 50); // create/save_draft/submit/self_approve/tp_approve_forward/tp_approve/bgd_approve/reject/update_sales_note
    $table->tinyInteger('from_status')->nullable();
    $table->tinyInteger('to_status')->nullable();
    $table->text('note')->nullable();
    $table->json('meta')->nullable();
    $table->unsignedBigInteger('actor_id');
    $table->timestamp('created_at')->useCurrent();
});
```

### 2.6 ERD tóm tắt
```
prospective_projects (sale_id, pm_id)
    └── solutions ─ solution_versions
          └── solution_review_profiles (auto pick bom_list_id)
          └── bom_lists (AGGREGATE, Hoàn thành → Đã duyệt)
                └── bom_list_products + bom_list_groups
pricing_requests (1) ─── (1) quotations
    └── files (polymorphic)
quotations
    └── quotation_product_prices ─→ bom_list_products
    └── quotation_histories
```

---

## 3. Workflow

### 3.1 BOM rút gọn
```
1 Đang tạo → 2 Hoàn thành → 3 Chờ duyệt → 4 Đã duyệt
                     ↓                          ↓
                 5 Tổng hợp              6 Không duyệt
```
- Status=4 lock read-only.
- Khi hồ sơ trình duyệt duyệt → hook `syncStatusFromSubmission` đẩy BOM 2→4, notify 4 đối tượng: người gửi hồ sơ, PM, người lập BOM, NV KD dự án.

### 3.2 PricingRequest
```
1 Đang tạo
   ↓ "Lưu và gửi"
2 Chờ XD giá  ── notify users có quyền "Xây dựng giá Bom giải pháp"
   ↓ NLG bấm "Tạo báo giá" → sinh Quotation (status=1)
3 Đang XD giá
   ↓ Quotation → 4 (Đã duyệt)
4 Đã có báo giá ── notify NV KD
```
- Status ≥ 2: lock hoàn toàn (không sửa/huỷ). Muốn đổi → tạo request mới.
- Quotation reject → quay về 1, request vẫn giữ status=3.

### 3.3 Quotation
```
1 Đang tạo
   ↓ "Gửi duyệt" → calculateLevel(V, M)
   ├─ Cấp 1 → popup tự duyệt → 4 Đã duyệt
   ├─ Cấp 2 → 2 Chờ TP → TP duyệt → 4
   └─ Cấp 3 → 2 Chờ TP → TP "Duyệt & chuyển BGĐ" → 3 Chờ BGĐ → BGĐ duyệt → 4
2/3 Chờ duyệt → Từ chối + reason → 1 Đang tạo
```
- Duyệt xong: notify người lập BG, NV KD, users quyền TP.
- TP reject cấp 2: notify NLG. BGĐ reject cấp 3: notify NLG + TP.

### 3.4 API endpoints

**PricingRequest:**
```
POST   /api/v1/assign/prospective-projects/{id}/pricing-requests/form-info
GET    /api/v1/assign/pricing-requests
GET    /api/v1/assign/pricing-requests/{id}
POST   /api/v1/assign/pricing-requests                  # tạo nháp
PUT    /api/v1/assign/pricing-requests/{id}              # sửa nháp
POST   /api/v1/assign/pricing-requests/{id}/send         # status 1→2
DELETE /api/v1/assign/pricing-requests/{id}              # chỉ nháp
```

**Quotation:**
```
POST   /api/v1/assign/quotations                         # tạo từ request
GET    /api/v1/assign/quotations
GET    /api/v1/assign/quotations/{id}
PUT    /api/v1/assign/quotations/{id}                    # lưu giá+note
POST   /api/v1/assign/quotations/{id}/calculate-level    # tính realtime
POST   /api/v1/assign/quotations/{id}/submit
POST   /api/v1/assign/quotations/{id}/self-approve
POST   /api/v1/assign/quotations/{id}/tp-approve         # cấp 2→4, cấp 3→3
POST   /api/v1/assign/quotations/{id}/bgd-approve
POST   /api/v1/assign/quotations/{id}/reject             # reason required
PUT    /api/v1/assign/quotations/{id}/sales-note         # status=4 only
GET    /api/v1/assign/quotations/pending-approval
GET    /api/v1/assign/quotations/{id}/export-excel
GET    /api/v1/assign/quotations/{id}/histories
GET    /api/v1/assign/prospective-projects/{id}/quotations  # tab Báo giá
```

**Hồ sơ trình duyệt (sửa):** bỏ field `bom_list_ids[]`. BE tự resolve `BomList::where('solution_version_id', $profile->solution_version_id)->where('bom_list_type', AGGREGATE)->where('status', HOAN_THANH)->firstOrFail()`. Không match → 422.

---

## 4. Frontend

### 4.1 Màn mới
1. **Popup "Yêu cầu XD giá"** — tab Hồ sơ trong `/assign/prospective-projects/:id/manager`. Show nếu `project.sale_id===me` + hồ sơ status=Đã duyệt. Fields: mã (readonly), BOM (readonly), deadline, delivery/warranty/payment*, description (CKEditor), files. Buttons: Lưu nháp | Lưu và gửi | Huỷ.
2. **`/assign/pricing-requests`** — danh sách. NV KD thấy của mình (mọi status); NLG thấy status IN (2,3). Cột: Mã YCBG, BOM, Dự án, GP, Version, KH, Deadline, Người YC, Ngày gửi, Trạng thái. Actions: Xem, Tạo báo giá (status=2 + chưa có quotation).
3. **`/assign/pricing-requests/:id`** — chi tiết readonly + file + link quotation (nếu có) + timeline.
4. **`/assign/quotations`** — danh sách. NLG thấy của mình. Cột: Mã BG, Mã YCBG, BOM, Dự án, GP, Version, KH, Tổng bán, Tỷ suất LN, Cấp duyệt, Trạng thái, Ngày tạo.
5. **`/assign/quotations/:id/edit`** — màn làm giá. Reuse `BomBuilderEditor` ở `pricingMode`, rewire sang quotation API. Info card readonly. Table 2 cột editable (giá nhập, giá bán). Footer realtime. Buttons: Lưu nháp | Gửi duyệt. Popup gửi duyệt theo cấp.
6. **`/assign/quotations/:id`** — chi tiết readonly. Section `sales_note` enable khi status=4 + `sale_id===me`. Button Xuất Excel | Lịch sử | Duyệt/Từ chối (TP/BGĐ). Button "In" disabled + tooltip.
7. **`/assign/quotations/pending-approval`** — TP thấy status=2, BGĐ thấy (2,3), cả 2 union. Click → detail + Duyệt/Từ chối.

### 4.2 Màn update
- **`/assign/prospective-projects/:id/manager`**:
  - Tab Hồ sơ: filter status=Đã duyệt, thêm cột BOM (link), cột action có button "Yêu cầu XD giá".
  - Thêm tab Báo giá: list quotation Đã duyệt, cột Mã BG, BOM, Version, Tổng bán, Ngày duyệt, Actions (Xem/Sửa sales_note/In[disabled]/Xuất Excel).
- **`/assign/solution-review-profiles/*`** (create + edit): bỏ field chọn BOM, BE tự resolve.

### 4.3 Xoá
| File/route | Lý do |
|---|---|
| `/assign/bom-list/pending-pricing` (folder) | Thay bởi `/assign/pricing-requests` |
| `/assign/bom-list/pending-price-approval` (folder) | Thay bởi `/assign/quotations/pending-approval` |
| `/assign/bom-list/_id/pricing.vue` | Thay bởi `/assign/quotations/:id/edit` |
| Button "Yêu cầu XD giá" trên chi tiết BOM | Chuyển sang tab Hồ sơ |
| Button "Điều chỉnh giá" trên BOM | Thay bằng tạo request mới |
| 5 status 7-11 trong filter `bom-list/index.vue` | BOM không còn |
| 2 menu sidebar "BOM chờ XD giá" + "BOM chờ duyệt giá" | Đổi tên |

### 4.4 Menu sidebar
- "Yêu cầu xây dựng giá" (thay "BOM chờ XD giá")
- "Báo giá chờ duyệt" (thay "BOM chờ duyệt giá", isShow TP/BGĐ)
- "Danh sách báo giá" (mới, isShow NLG)
- "Cấu hình duyệt giá" (giữ)

---

## 5. Migration + Refactor + Test

### 5.1 Thứ tự migration (prefix `2026_04_14_*`)
```
1. drop_pricing_snapshots_and_histories_tables
2. drop_pricing_columns_from_bom_lists
3. reset_bom_status_to_max_6
4. create_pricing_requests_table
5. create_quotations_table
6. create_quotation_product_prices_table
7. create_quotation_histories_table
```
Không tạo bảng attachment riêng. Không seeder mới.

### 5.2 BE refactor
**Sửa:**
- `BomList.php`: xoá 5 STATUS constants 7-11, xoá relationship snapshots/histories/pricing.
- `BomListService.php`: xoá 9 method pricing (request/saveDraft/submit/selfApprove/tpApproveForward/approve/reject/adjustPricing/calculateLevel). Giữ `syncStatusFromSubmission` (4 notify targets). Xoá logic `pricing_version`.
- `BomListController.php`: xoá 9 endpoint pricing + 2 list pending-*.
- `SolutionReviewProfileService.php`: auto-resolve bom_list_id, bỏ input param.
- Route `Modules/Assign/Routes/api.php`: xoá route cũ, thêm 18 route mới.

**Xoá file:** `BomPricingHistory.php`, `BomPricingSnapshot.php`.

**Tạo mới:**
- Entities: `PricingRequest`, `Quotation`, `QuotationProductPrice`, `QuotationHistory`.
- Services: `PricingRequestService`, `QuotationService`.
- Controllers: `PricingRequestController`, `QuotationController`.
- Requests: store/update/send/approve/reject/submit/update-sales-note.
- Transformers: `PricingRequestResource`, `QuotationResource`, `DetailQuotationResource`.
- Excel Export: `QuotationExport` (reuse pattern `BomListExport` + thêm section thông tin thương mại + snapshot khách hàng).
- Notifications (7 types): `pricing_request_sent`, `quotation_ready_to_build`, `quotation_submitted_tp`, `quotation_submitted_bgd`, `quotation_approved`, `quotation_rejected`, `bom_approved` (giữ nhưng 4 targets).

### 5.3 FE refactor
**Xoá:**
- `pages/assign/bom-list/pending-pricing/` (folder)
- `pages/assign/bom-list/pending-price-approval/` (folder)
- `pages/assign/bom-list/_id/pricing.vue`

**Sửa:**
- `pages/assign/bom-list/index.vue`: xoá 5 status filter.
- `pages/assign/bom-list/_id/index.vue`: xoá 4 button pricing, xoá hiển thị giá.
- `pages/assign/bom-list/_id/edit.vue`: xoá `pricingMode`.
- `components/assign/bom-builder/BomBuilderEditor.vue`: giữ `pricingMode` nhưng rewire nhận quotation data qua prop. Move footer cấp duyệt sang parent.
- `store/bom-list.js`: xoá actions pricing.
- `layouts/default.vue`: update 3 menu items.
- `pages/assign/prospective-projects/_id/manager.vue`: tab Hồ sơ + tab Báo giá mới.
- `pages/assign/solution-review-profiles/_id/edit.vue` + `create.vue`: bỏ chọn BOM.

**Tạo mới:**
- `pages/assign/pricing-requests/{index,_id/index,_id/edit}.vue`
- `pages/assign/quotations/{index,_id/index,_id/edit,create,pending-approval/index}.vue`
- `components/assign/pricing-request/PricingRequestModal.vue`
- `components/assign/quotation/{QuotationInfoCard,QuotationSalesNoteCard,QuotationApproveModal,QuotationRejectModal}.vue`
- `store/pricing-request.js`, `store/quotation.js`

### 5.4 Risks
1. **Auto-pick BOM fail**: throw 422 rõ message, hint UI màn hồ sơ.
2. **BOM lock sau Đã duyệt**: validate `BomListService::update` — status≥4 throw.
3. **Race tạo báo giá**: DB transaction + check `pricing_request.status=2` trước insert; user 2 nhận 409.
4. **Sales_note lỗi quyền**: check `sale_id === auth()->id()` ở middleware.
5. **TP/BGĐ có cả 2 quyền**: list union, button hiển thị theo status row.
6. **Audit cũ**: drop `bom_pricing_histories` mất audit cũ — OK local, production sau này lưu ý.

### 5.5 Test outline (9 module)
1. BOM strip pricing — status 1-6, lock sau 4, notify 4 targets khi submission duyệt.
2. Hồ sơ trình duyệt auto-pick — success/fail theo version.
3. PricingRequest CRUD + send + upload file + phân quyền.
4. Tạo báo giá từ request — race condition, copy snapshot đầy đủ.
5. Quotation pricing + workflow duyệt — cấp 1/2/3, TP→BGĐ, reject → 1, approve → 4.
6. Sales note — NV KD nhập được khi status=4, người khác block.
7. Tab Hồ sơ + tab Báo giá trong dự án tiền khả thi.
8. Export Excel quotation.
9. Navigate màn cũ — redirect/404.

---

## 6. Convention database (bổ sung `CLAUDE.md`)

Thêm vào `CLAUDE.md` mục **"Convention Database"**:

- **Cấp tổ chức**: luôn `company_id, department_id, part_id` — all `unsignedBigInteger nullable`. KHÔNG `branch_id`.
- **Audit**: `$table->timestamps()` + manual `created_by, updated_by` (`unsignedBigInteger nullable`). KHÔNG SoftDeletes cho entity chính.
- **Version solution**: entity gắn với solution phải có `solution_version_id` NOT NULL (+ `solution_module_version_id` nullable nếu áp dụng cả cấp module).
- **File đính kèm**: dùng bảng `files` chung (`table` string + `table_id`). Entity khai báo `hasMany(File::class, 'table_id', 'id')->where('table', '<table_name>')`.
- **Mã code**: pattern `PREFIX-YYYY-NNNNN`, implement `getNextCode()` trên Entity (copy `BomList::getNextCode()`).
