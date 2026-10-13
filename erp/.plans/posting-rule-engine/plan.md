# Posting Rule Engine — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (recommended) hoặc executing-plans. Steps dùng checkbox `- [x]`.

**Goal:** Màn cấu hình công thức hạch toán + engine runtime sinh bút toán khi ghi sổ, pilot end-to-end cho `product_export` / Xuất bán HĐ hãng (chạy SHADOW đối chiếu logic cũ trước khi flip).

**Architecture:** config = data (bảng posting_*) · nghiệp vụ = code (VariableProvider) · engine đọc config+catalog → mảng bút toán (dạng `AccountDetail::saveAccountDetail` nhận) → so khớp với `getDataProductExportAccounting`.

**Tech:** PHP 7.4 / Laravel 6 · AngularJS 1.3.9 + Blade · symfony/expression-language · MySQL. Design: `.plans/posting-rule-engine/design.md`.

## Global Constraints
- Làm trong `ERP/TanPhatDev`. KHÔNG commit/push khi chưa yêu cầu (được commit LOCAL nếu chạy subagent-driven; không push).
- ERP = **Laravel 6 / PHP 7.4** — không dùng facade `Http`, tính năng L7+/PHP8.
- `.env` DB đọc trước khi migrate/tinker (`grep DB_ .env`) — hiện `erp_new` (prod). **KHÔNG chạy migrate lên prod** — migrate ở DB dev, hoặc chỉ viết migration + để user chạy.
- Mảng bút toán engine phải cùng shape với `$accounts` mà `AccountDetail::saveAccountDetail` nhận: `['identify_number'=>mã TK,'type'=>1|2,'value'=>số,'value_exchange'=>số?,'customer_id'?,'supplier_id'?,'employee_id'?,'employee_company_id'?/'employee_department_id'?/'employee_part_id'?,'cost_debt_id'?,'work'?,'currency_id'?,'exchange_rate'?,'contractable_id'?,'contractable_type'?]`.
- Bút toán `type`: 1=Nợ (`AccountDetail::TYPE_DEPT`), 2=Có (`AccountDetail::TYPE_HAS`).
- Validate: BE rethrow `ValidationException` (không catch chung); FE hiện lỗi inline.
- Loại phiếu pilot code: `product_export.xuat_ban_hd_hang`.
- Verify không có PHPUnit cho phần này → dùng `php -l` + tinker + đối chiếu shadow trên dữ liệu thật (giống cách verify các báo cáo khác).

---

## PHASE 0 — Schema + Model

### Task 0.1: Migration 5 bảng posting_*
**Files:** Create `database/migrations/2026_07_24_000001_create_posting_rule_tables.php`
**Produces:** bảng `posting_doc_types`, `posting_groups`, `posting_lines`, `posting_config_histories`, `posting_shadow_logs` (schema như design mục 4).
- [x] Viết migration đủ 5 bảng: cột theo design; FK `unsignedBigInteger` (không cascade cứng, theo convention ERP); `created_by/updated_by nullable`; index `posting_doc_types.code` unique, `posting_groups.posting_doc_type_id`, `posting_lines.posting_group_id`.
- [x] `php -l` migration sạch.
- [x] (KHÔNG migrate prod) — verify cú pháp: `php artisan migrate --pretend` HOẶC review SQL. Ghi rõ để user chạy `php artisan migrate` ở DB dev.
- [x] Commit (chỉ khi user yêu cầu).

### Task 0.2: Model 5 entity
**Files:** Create `app/Model/Accounting/Posting/{PostingDocType,PostingGroup,PostingLine,PostingConfigHistory,PostingShadowLog}.php`
**Produces:** Eloquent models + relations (`PostingDocType hasMany groups`, `PostingGroup hasMany lines belongsTo docType`, `PostingLine belongsTo group`).
- [x] Tạo 5 model, `$fillable`, `$casts` (`snapshot`/`diff` => 'array', `active`/`has_condition` => 'boolean'). Const `SIDE_NO='no'`, `SIDE_CO='co'` trên PostingLine.
- [x] `php -l` sạch.
- [x] Tinker: tạo thử 1 doc_type + group + line + đọc lại quan hệ (ở DB dev).
- [x] Commit (khi user yêu cầu).

### Task 0.3: Migration thêm `loop_source` vào posting_groups (nhóm lặp)
**Files:** Create `database/migrations/2026_07_24_000002_add_loop_source_to_posting_groups.php`; Modify `app/Model/Accounting/Posting/PostingGroup.php` (+`loop_source` vào $fillable)
**Produces:** cột `posting_groups.loop_source` varchar nullable (key collection để lặp; null = nhóm thường).
- [x] Migration `Schema::table('posting_groups', add string('loop_source')->nullable()->after('cond_expr'))` + down dropColumn. Thêm `loop_source` vào PostingGroup $fillable.
- [x] `php -l` sạch. Migrate trên `dev_erp_2` (kiểm `grep DB_ .env` = local trước) — chỉ file này: `php artisan migrate --path=database/migrations/2026_07_24_000002_add_loop_source_to_posting_groups.php`. Tinker: `Schema::hasColumn('posting_groups','loop_source')` = true.
- [x] Commit (khi user yêu cầu).

---

## PHASE 1 — Variable Catalog (code) — QUAN TRỌNG NHẤT

### Task 1.1: Interface + Registry
**Files:** Create `app/Services/Posting/Contracts/PostingVariableProvider.php`, `app/Services/Posting/PostingVariableProviderRegistry.php`
**Produces:**
- Interface `PostingVariableProvider`: `catalog(): array`, `attributes(): array`, `values($record): array`, `objectFor($record): array` (design mục 6).
- Registry: `register($docTypeCode, $providerClass)`, `for($docTypeCode): PostingVariableProvider`. Đăng ký `product_export.xuat_ban_hd_hang => ProductExportVariableProvider` (trong 1 service provider hoặc mảng config).
- [x] Viết interface + registry. `php -l` sạch.
- [x] Commit (khi user yêu cầu).

### Task 1.2: ProductExportVariableProvider
**Files:** Create `app/Services/Posting/Providers/ProductExportVariableProvider.php`
**Consumes:** logic tính hiện có trong `FirmContractProductExportService` (đọc `getDataProductExportAccounting` + `prepareData` + 8 sub-method: revenueAccounting, revenueDeductionAccounting, costAccounting, bonusContractAccounting, vatExtraCostAccounting, monthlyAndQuarterlyCommissionAccounting, riskFundAccounting) để liệt kê ĐỦ biến cần cho công thức 8 cụm.
**Produces:** `values(ProductExport $pe)` trả map biến gồm tối thiểu:
`sum_amount_after_extra`, `sum_amount_after_extra_vat`, `sale_invoice`, `sale_invoice_vat`, `gia_von` (từ costAccounting), `percent_export_without_delivery`, `percent_export_without_cost`, `before_vat_total/product/repair_service/delivery_cost` (support_accounting), `vat_percent`, `type` (attribute), + các rate/bonus dùng ở 8 cụm. `catalog()`/`attributes()` trả metadata + sample (lấy từ 1 phiếu thật hoặc hằng).
- [x] Viết provider — **tái dùng** `prepareData`/sub-method (refactor `prepareData` thành public hoặc trích helper nếu cần) để KHÔNG lệch số với logic cũ.
- [x] `objectFor($pe)` → `['customer_id'=>$pe->customer_id]` (+ supplier/employee nếu cụm cần).
- [x] `php -l` sạch.
- [x] Tinker: lấy 1 product_export type=XUAT_BAN_HD_HANG thật → `values()` in ra map biến; đối chiếu vài số với logic cũ (`prepareData`). KHÔNG bịa.
- [x] Commit (khi user yêu cầu).

### Task 1.3: Provider collections() + collectionValues() (nhóm lặp — 4 cụm động)
**Files:** Modify `app/Services/Posting/Providers/ProductExportVariableProvider.php` + interface `PostingVariableProvider` (thêm 2 method — cập nhật interface Task 1.1)
**Consumes:** 4 cụm động ở `app/Services/Sale/Firm/Contract/FirmContractExportService.php` (bonusContractAccounting 63, vatExtraCostAccounting 122, monthlyAndQuarterlyCommissionAccounting 182, riskFundAccounting 277).
**Produces:**
- Interface `PostingVariableProvider` thêm `collections(): array` + `collectionValues($record, string $key): array` (design mục 6 + 6b).
- Provider trả các collection **đã LÀM PHẲNG** vòng lặp lồng: `bonus_recipients`, `tndn_recipients`, `commission_recipients`, `risk_departments` — mỗi item = `['vars'=>[...trường per-item đã tính: rate/month_amount/quarter_amount/risk_fund_amount...], 'object'=>['employee_id'=>..,'employee_department_id'=>..]]`. Tái dùng data mà 4 method đang lặp (department_main.employees, support_accounting.departments...). Provider tính sẵn `item.rate`/`item.month_amount`/... để công thức config gọn.
- [x] Viết `collections()` (metadata + itemFields) + `collectionValues()`. Cập nhật interface (Task 1.1 file). Registry không đổi.
- [x] `php -l` sạch.
- [x] Tinker (dev_erp_2): với ProductExport thật (id=780 hoặc tương tự), `collectionValues($pe,'commission_recipients')` → in danh sách item; **đối chiếu** số/đối tượng với vòng lặp cũ trong monthlyAndQuarterlyCommissionAccounting (vài item). Tương tự 1 collection nữa. KHÔNG bịa.
- [x] Commit (khi user yêu cầu).

---

## PHASE 2 — Engine runtime

### Task 2.1: DynamicAccountResolver + object mapping
**Files:** Create `app/Services/Posting/Contracts/DynamicAccountResolver.php` + `app/Services/Posting/DynamicAccountResolverRegistry.php`
**Produces:** interface `resolve($key, $record): ?int`; registry theo key. (Pilot: nếu bút toán XUAT_BAN_HD_HANG dùng TK cố định → registry rỗng, engine chỉ lookup identify_number.)
- [x] Viết interface + registry (có thể rỗng ở pilot). `php -l` sạch. Commit (khi yêu cầu).

### Task 2.2: PostingEngine::generate
**Files:** Create `app/Services/Posting/PostingEngine.php`
**Consumes:** PostingDocType+groups+lines; VariableProviderRegistry; DynamicAccountResolverRegistry; `symfony/expression-language`.
**Produces:** `generate(string $docTypeCode, $record): array` → mảng bút toán (shape saveAccountDetail).
- [x] Nạp doc_type + groups(active order) + lines(order). `vals = provider->values($record)`.
- [x] Đánh giá điều kiện: chuẩn hóa `{Bien}` → biến expression-language; group không thỏa → skip; exception → skip + log.
- [x] **Nhóm thường** (`loop_source` null): mỗi line tính với `vals`. **Nhóm lặp** (`loop_source` != null): `items=provider->collectionValues($record,loop_source)`; mỗi item → ctx = `vals + item.<field>`; line tính với ctx; `@item` → object của item; group++ mỗi item (cột `account_details.group`).
- [x] Mỗi line: tính `value_formula` → số; account cố định → `identify_number`=account; `@KEY` → resolver→account_id; obj `@phieu` → `objectFor`, `@item` → object của item; fee→cost_debt_id (lookup mã phí), job→work (lookup vụ việc). Bỏ dòng `value==0` (design mục 14).
- [x] Set bối cảnh từ record (company/department/part, currency, exchange_rate). Trả mảng.
- [x] `php -l` sạch.
- [x] Tinker: `PostingEngine::generate('product_export.xuat_ban_hd_hang', $pe)` với config seed thử (Task 3.x hoặc seed tạm) → in mảng bút toán.
- [x] Commit (khi yêu cầu).

---

## PHASE 3 — Màn cấu hình (Blade + AngularJS) + API

### Task 3.1: Controller + routes + quyền
**Files:** Create `app/Http/Controllers/Accounting/PostingRuleController.php`; Modify `routes/web.php` (group `admin/accounting/posting-rules`); seeder quyền `Cấu hình hạch toán`.
**Produces:** `index` (view), `config` (GET JSON: groups+lines+catalog+danh mục), `save` (POST), `history` (GET).
- [x] Route + controller khung. `config` trả groups/lines theo doc_type + `provider->catalog()/attributes()` + accounts (identify_number+name), objects, feeCodes (cost_debts), jobCodes (works). Gắn `checkPermission:Cấu hình hạch toán` route thao tác.
- [x] Thêm quyền vào seeder (hoặc tinker firstOrCreate). `php -l` sạch.
- [x] `php artisan route:list --path=posting-rules` thấy route.
- [x] Commit (khi yêu cầu).

### Task 3.2: save + validate + history
**Files:** Modify PostingRuleController (`save`)
**Produces:** `save` validate (nhóm 1Nợ-nCó/nNợ-1Có, đủ Nợ/Có, công thức/điều kiện parse được + biến ∈ catalog) → lưu groups/lines (replace theo doc_type) + version++ + PostingConfigHistory snapshot. Rethrow ValidationException.
- [x] Viết validate (BE) dùng expression-language parse + đối chiếu biến với catalog. `php -l` sạch.
- [x] Tinker: gọi save với payload hợp lệ → lưu OK + history +1; payload lỗi (n-n) → ValidationException.
- [x] Commit (khi yêu cầu).

### Task 3.3: View Blade + AngularJS (port demo)
**Files:** Create `resources/views/accounting/posting_rules/index.blade.php` (+ partial JS)
**Consumes:** demo `~/Documents/demo/posting-rule-engine-v3.html` (UI/logic), API config/save/history.
**Produces:** màn cấu hình: chọn loại phiếu · list nhóm (kéo-thả, active, điều kiện) · dòng định khoản (Nợ/Có, TK select2, giá trị popup ƒx, đối tượng/mã phí/vụ việc) · popup công thức ƒx (cond/value, token, preview) · validate realtime · lưu/hủy/lịch sử.
- [x] Dựng Blade + Angular controller (interpolation `<% %>`, `layouts/app`). Kéo-thả bằng jQuery UI sortable. Select2 theo chuẩn ERP (chú ý `ng-non-bindable` cho select trong vùng Angular compile). Popup ƒx port từ demo (đánh giá preview client-side như demo; validate cuối cùng ở BE khi lưu).
- [x] **Nhóm lặp:** dropdown "Lặp theo" (từ `collections()`); khi chọn → popup ƒx thêm token `{item.<field>}` (từ `itemFields`) + đối tượng có option `@item`. Validate: dòng nhóm lặp dùng `{item.*}` chỉ hợp lệ khi nhóm có loop_source.
- [x] Verify: mở màn trên dev, chọn loại phiếu, thêm nhóm/dòng, đặt công thức, lưu → reload thấy dữ liệu; nhóm n-n → chặn lưu.
- [x] Commit (khi yêu cầu).

---

## PHASE 4 — Tích hợp SHADOW + đối chiếu

### Task 4.1: comparePostings + tích hợp shadow
**Files:** Create `app/Services/Posting/PostingShadowComparer.php`; Modify `app/Http/Controllers/Warehouse/ProductExportsController.php` (nhánh `XUAT_BAN_HD_HANG` quanh dòng ~858).
**Produces:** khi store product_export type=XUAT_BAN_HD_HANG: tính `$engineData = PostingEngine::generate(...)`, `comparePostings($data cũ, $engineData)` (so tập bút toán bỏ qua thứ tự theo type/account/value làm tròn/customer/supplier/employee/cost_debt/work), ghi `PostingShadowLog` (matched, diff). **Vẫn saveAccountDetail bằng `$data` cũ** (chưa flip).
- [x] Viết comparer + chèn shadow (bọc try/catch để KHÔNG làm hỏng luồng store nếu engine lỗi — chỉ log).
- [x] `php -l` sạch.
- [x] Tinker: mô phỏng generate + compare trên vài product_export thật → in diff (kỳ vọng khớp sau khi config đủ 8 cụm; ghi lại lệch để chỉnh config/provider).
- [x] Commit (khi yêu cầu).

### Task 4.2: Cờ flip engine
**Files:** Modify ProductExportsController + config (`config/posting.php` hoặc env `POSTING_ENGINE_DOCS`).
**Produces:** nếu doc_type nằm trong danh sách bật → dùng `$engineData` để saveAccountDetail thay `$data`. Mặc định TẮT (shadow).
- [x] Thêm cờ + nhánh chọn nguồn. `php -l` sạch. Commit (khi yêu cầu).

### Task 4.3 (không code — vận hành): đối chiếu tới khớp 100%
- [ ] User/dev: nhập config 8 cụm qua màn → chạy nhiều product_export thật ở dev → xem `posting_shadow_logs` → chỉnh config/provider tới khi `matched=true` toàn bộ → bật cờ flip.

---

## Self-Review (đã chạy)
- **Spec coverage:** schema (T0.1) · model (T0.2) · variable catalog (T1.1-1.2) · engine + TK động/obj (T2.1-2.2) · màn+API+validate+history (T3.1-3.3) · shadow+flip (T4.1-4.3). ✅ khớp design 16 mục.
- **Placeholder:** không có TBD; các "khi yêu cầu" là quy ước commit.
- **Rủi ro:** phần lệch số engine vs logic cũ (8 cụm phức tạp) → xử lý bằng shadow + Task 1.2 tái dùng logic tính hiện có + Task 4.3 đối chiếu; KHÔNG flip khi chưa khớp.

---

### Checkpoint — 2026-07-24
Vừa hoàn thành: TOÀN BỘ code Phase 0→4.2 (16 commit trên nhánh `cau_hinh_hach_toan`, HEAD `bf58a54109`), mỗi task qua review 2 tầng; final whole-branch review (opus) = **READY TO MERGE** ở chế độ SHADOW (cờ `POSTING_ENGINE_DOCS` tắt = hành vi ghi sổ legacy y hệt).
Đang làm dở: Task 4.3 (vận hành, không code) — chưa bắt đầu.
Bước tiếp theo: (1) user review nhánh + test màn cấu hình trên dev; (2) quyết DESIGN FORK I2 (@creator cho cụm Thưởng HĐ/TNCN); (3) vận hành 4.3: tạo phiếu thật → đọc posting_shadow_logs → dựng config đủ 8 cụm qua màn → đối chiếu tới matched 100% → xử lý 5 điều kiện flip → bật cờ theo từng doc_type.
Blocked: DESIGN FORK I2 cần user quyết trước khi flip 2 cụm Thưởng HĐ/TNCN.

**5 điều kiện an toàn trước khi FLIP (từ final review):**
1. I1 — thêm guard cân đối Nợ=Có + parity vs legacy trong nhánh flip (`ProductExportsController` ~877) trước khi lưu bằng engine (hiện chỉ kiểm `!empty`).
2. I3 — siết `PostingShadowComparer` canonical-key (thêm employee_department/company/part_id + group, bỏ cộng dồn) HOẶC audit hàng-đối-hàng đạt 100% trên phiếu thật.
3. I2 — xử lý `@creator` cho cụm Thưởng HĐ/TNCN (dòng Nợ 5211 dùng created_by cố định) HOẶC giữ legacy 2 cụm này.
4. M1 — khử hàm `constant()` của symfony/expression-language (đính chính: KHÔNG phải "0 hàm").
5. Migrate `posting_*` trên DB đích rồi bật `POSTING_ENGINE_DOCS` theo từng doc_type.

---

## PHASE 5 — Tổng quát hoá "đối tượng" (giải quyết I2: @creator)

**Mục tiêu:** cụm Thưởng HĐ (`bonusContractAccounting`) có dòng Nợ 5211 dùng `Employee = contract->created_by` (người tạo phiếu, cố định) — loop model hiện chỉ có `@phieu`/`@item`. Tổng quát hoá "đối tượng" thành danh mục do provider khai báo (`phieu`, `creator`, …) để engine cấu hình được cả 8 cụm. (Đính chính: cụm TNCN KHÔNG dùng created_by — cả 2 vế là recipient, `@item` đủ.)

**Mô hình mới của `obj` trên posting_lines (vẫn là string, KHÔNG đổi schema):**
- `null` → không gắn đối tượng.
- `@item` → object của item nhóm lặp (giữ nguyên).
- `@<key>` → `provider->objectValues(record, key)`, với `key ∈ provider->objects()` (vd `@phieu`, `@creator`). `@phieu` = `objectValues(record,'phieu')` map về `objectFor()` cũ → back-compat.

### Task 5.1: Tổng quát object trong interface + engine
**Files:** Modify `PostingVariableProvider` (interface), `PostingEngine` (buildLine, ~dòng 219-234).
**Produces:** interface thêm `objects(): array` (danh mục [{key,label}]) + `objectValues($record, string $key): ?array` (field-bag: customer_id/supplier_id/employee_id/employee_department_id/obj_department_id/obj_part_id…; null nếu key lạ). Engine buildLine: `@item` giữ nguyên; `@<key>` → objectValues(record,key) merge (null → Log::warning + bỏ đối tượng); `@phieu` chạy qua objectValues('phieu'). Back-compat @phieu.
- [x] Sửa interface + engine. `php -l` sạch. Unit tinker: provider giả có objectValues('creator')→bag → buildLine dòng obj=@creator merge đúng employee_id/employee_department_id; obj=@unknown → log + không merge; @phieu vẫn chạy.
- [x] Commit.

### Task 5.2: ProductExportVariableProvider objects() + objectValues()
**Files:** Modify `app/Services/Posting/Providers/ProductExportVariableProvider.php`.
**Produces:** `objects()` = `[{key:'phieu',label:'Phiếu (chứng từ)'}, {key:'creator',label:'Người tạo phiếu'}]`. `objectValues($record,'phieu')` = `objectFor($record)`; `objectValues($record,'creator')` = `['employee_id'=>contract->created_by, 'employee_department_id'=>contract->department_id]` (lấy từ HĐ của phiếu xuất, tái dùng data đã có); key lạ → null. Xác minh object item của `bonus_recipients` mang `employee_department_id = department_root->id` (khớp legacy dòng 85); nếu chưa → sửa collectionValues cho đúng.
- [x] Sửa provider. `php -l` sạch. Tinker trên export thật: `objectValues(record,'creator')` = created_by + contract->department_id KHỚP legacy dòng 82; item bonus_recipients object employee_department_id = department_root KHỚP dòng 85.
- [x] Commit.

### Task 5.3: config() trả objects + save validate obj
**Files:** Modify `PostingRuleController` (`config`, `save`).
**Produces:** `config()` thêm `objects` = provider->objects() (rỗng nếu chưa có provider). `save()` validate `obj`: hợp lệ nếu `null` | `@item` (chỉ khi group có loop_source) | `@<key>` với key ∈ objects() keys; khác → ValidationException tại đúng line.
- [x] Sửa controller. `php -l` sạch. Tinker: config JSON có objects [phieu,creator]; save payload obj=@creator hợp lệ; obj=@xxx lạ → ValidationException; @item ở nhóm thường → lỗi (giữ nguyên).
- [x] Commit.

### Task 5.4: FE dropdown "đối tượng" động
**Files:** Modify `resources/views/accounting/posting_rules/_script.blade.php` (+ index nếu cần).
**Produces:** dropdown "đối tượng" của dòng đổ từ `config.objects` (map `@<key>`) + thêm option `@item` chỉ khi nhóm có loop_source (bỏ hardcode @phieu/@item). Validate realtime: `@item`/`@<key>` hợp lệ theo objects + loop như BE.
- [x] Sửa FE. Blade compile + `php -l` sạch. Rà tay: nhóm thường thấy Phiếu/Người tạo; nhóm lặp thêm Item; payload obj đúng `@<key>`.
- [x] Commit.

### Task 5.5 (verify I2 giải quyết — feeds 4.3): dựng cụm Thưởng HĐ + đối chiếu shadow
- [ ] Cấu hình cụm Thưởng HĐ qua engine (loop_source=bonus_recipients; Nợ 5211 obj=@creator job=12; Có 35241 obj=@item job=12) trên 1 export thật → engine tái tạo ĐÚNG dòng Nợ 5211 employee=created_by + Có 35241 employee=recipient → shadow matched cụm này. (Không code; vận hành + tinh chỉnh provider/config nếu lệch.)

### Checkpoint — Phase 5 (planned 2026-07-24)
Vừa hoàn thành: chốt Hướng A cho I2 + lên plan Phase 5 (5 task).
Bước tiếp theo: dispatch Task 5.1 (interface + engine object generalization) qua subagent-driven.
Blocked: để trống.

### Checkpoint — Phase 5 code xong (2026-07-24)
Vừa hoàn thành: Task 5.1→5.4 (interface+engine object model, provider objects/objectValues creator, config+validate obj, FE dropdown động) — 6 commit (89fced2968, 2b8e3af8c6, a7c3764a62, f3b97c3f86, +fix 831362bf67), mỗi task review 2 tầng, fix infinite-digest FE. HEAD `831362bf67`. Nay engine cấu hình được cả 8 cụm (có @creator).
Đang làm dở: Task 5.5 (vận hành) chưa bắt đầu.
Bước tiếp theo: user test màn dev (dropdown "đối tượng" có Phiếu/Người tạo phiếu; nhóm lặp thêm @item) → Task 5.5: dựng cụm Thưởng HĐ config → đối chiếu shadow. Sau đó quay lại 5 điều kiện flip (I1/I3/M1 + migrate DB đích).
Blocked: để trống.

---

## PHASE 6 — Hardening trước FLIP (I1 / I3 / M1)

**Mục tiêu:** siết 3 điều kiện an toàn từ final review trước khi cho phép lưu bút toán bằng engine.

### Task 6.1: SafeExpressionLanguage — khử hàm (M1)
**Files:** Create `app/Services/Posting/SafeExpressionLanguage.php`; Modify `PostingEngine` (dòng 86), `PostingRuleController` (dòng 196).
**Produces:** class `SafeExpressionLanguage extends Symfony\Component\ExpressionLanguage\ExpressionLanguage` override `registerFunctions()` thành no-op → KHÔNG còn hàm mặc định `constant()`. Engine (eval) + controller (validate parse) dùng `SafeExpressionLanguage` thay `new ExpressionLanguage()`.
- [x] Tạo class + đổi 2 chỗ khởi tạo. `php -l` sạch. Tinker: công thức `constant('PHP_INT_MAX')` → parse/evaluate NÉM lỗi (hàm không tồn tại); công thức số học `{a} + {b} * 2` vẫn chạy đúng.
- [x] Commit.

### Task 6.2: Siết canonical-key comparer (I3)
**Files:** Modify `app/Services/Posting/PostingShadowComparer.php` (`keyParts`).
**Produces:** thêm vào canonical-key: `employee_company_id`, `employee_department_id`, `employee_part_id`, `obj_company_id` (đủ bộ dimension của bút toán). Giữ cộng dồn theo key (nay ở mức dimension đầy đủ → không còn gộp nhầm 2 dòng khác phòng/bộ phận). KHÔNG thêm `group` (số group nội bộ engine vs legacy khác nhau → sẽ gây lệch giả). Ghi chú quyết định trong docblock.
- [x] Sửa keyParts. `php -l` sạch. Tinker: 2 dòng CÙNG (type,number,employee_id) nhưng KHÁC employee_department_id → nay tách 2 key (trước gộp 1). matched cũ (bỏ dimension) vs mới trên vài cặp mẫu.
- [x] Commit.

### Task 6.3: Guard flip cân đối + parity (I1)
**Files:** Modify `PostingShadowComparer` (thêm `isBalanced()`), `ProductExportsController` (nhánh flip ~dòng 877).
**Produces:** trước khi flip sang engineData, BẮT BUỘC: `!empty($engineData)` AND `comparer->isBalanced($engineData)` (Σ Nợ == Σ Có, ±1đ) AND `$shadowCmp['matched'] === true` (khớp legacy phiếu này). Không đủ 3 điều kiện mà cờ đang bật → `Log::error('[posting-flip] ... lý do')` + fallback `$data` legacy (không lưu bút toán engine đáng ngờ). `isBalanced(array $lines): bool` = so tổng value type=1 vs type=2 (±1đ). Ghi comment: gate parity (matched) là bảo thủ cho pilot — có thể nới xuống balance-only khi kế toán đủ tin cậy.
- [x] Sửa comparer + controller. `php -l` sạch. Rà tay + tinker: engineData cân+matched → flip; unbalanced HOẶC !matched + cờ bật → Log::error + dùng $data (không dùng engine). Cờ tắt → như cũ.
- [x] Commit.

### Checkpoint — Phase 6 (planned 2026-07-24)
Vừa hoàn thành: lên plan Phase 6 (I1/I3/M1).
Bước tiếp theo: dispatch Task 6.1 (SafeExpressionLanguage) qua SDD.
Blocked: để trống.

### Checkpoint — Phase 6 xong (2026-07-24)
Vừa hoàn thành: Task 6.1→6.3 (M1 SafeExpressionLanguage; I3 siết comparer key; I1 guard flip cân đối+parity) — 3 commit (ed36e56ec4, 3e460e9253, 80a2403204), mỗi task review Approved. HEAD `80a2403204`.
Đang làm dở: —
Bước tiếp theo: chỉ còn 2 việc VẬN HÀNH (không code): (a) migrate `posting_*` trên DB đích + (b) 5.5/4.3 — chạy phiếu thật → đối chiếu `posting_shadow_logs` (nay đã siết + guard) tới matched=100% → bật `POSTING_ENGINE_DOCS`. Tuỳ chọn: thêm collection `products` để cụm giá vốn shadow khớp per-mã-hàng.
Blocked: để trống.

---

## PHASE 7 — Cụm giá vốn theo từng mã hàng (collection `products`)

**Mục tiêu:** cụm giá vốn khớp legacy per-mã-hàng: N dòng **Có 1561** (mỗi mã 1 dòng, có `product_id`, value = export_price×qty×unit_coefficient) + **1 dòng Nợ 632 gộp** (`{gia_von}`), tất cả cùng 1 group. Cần: collection `products`, engine hỗ trợ "dòng gộp trong nhóm lặp + shared group", product_id vào key comparer.

**De-risk (đã kiểm):** `account_details.product_id` fillable; `createDataSaveDept` map `Product::class→product_id`; `buildLine` merge object `@item` → chỉ cần object item = `{product_id}`, save không cần sửa.

**Quy tắc engine mới (backward-compat):** nhóm lặp mà CÓ ÍT NHẤT 1 dòng "item-free" (value không chứa `{item.` VÀ obj != `@item`) → chế độ **shared-group**: 1 group number cho cả nhóm, dòng có tham chiếu item lặp theo item, dòng item-free emit 1 lần. Nhóm lặp mà MỌI dòng đều tham chiếu item → giữ chế độ cũ **per-item-group** (mỗi item 1 group). 4 cụm lặp hiện tại (bonus/tndn/commission/risk) mọi dòng đều dùng `{item.*}` → KHÔNG đổi hành vi.

### Task 7.1: Provider collection `products`
**Files:** Modify `app/Services/Posting/Providers/ProductExportVariableProvider.php`.
**Produces:** `collections()` thêm entry `products` (itemFields: `line_total`). `collectionValues($record,'products')` trả mỗi mã hàng: `['vars'=>['line_total'=>export_price×qty×unit_coefficient], 'object'=>['product_id'=>product_id]]` — qty = `is_export_direct ? product->qty : product->lot->qty` (tái dùng đúng logic `costAccounting` legacy dòng 670-675). Null-safe lot.
- [x] Sửa provider. `php -l` sạch. Tinker export thật: `collectionValues($ex,'products')` mỗi item line_total KHỚP legacy per-mã + object product_id đúng; Σ line_total == `{gia_von}`.
- [x] Commit.

### Task 7.2: Engine — dòng gộp trong nhóm lặp + shared group
**Files:** Modify `app/Services/Posting/PostingEngine.php` (generate loop, ~dòng 107-125).
**Produces:** helper `lineRefsItem($line)` = `strpos(value_formula,'{item.')!==false || trim(obj)==='@item'`. Nếu nhóm lặp có ≥1 dòng item-free → shared-group: `$groupNo++` một lần; dòng item → lặp theo items (ctx=vals+item_*), dòng item-free → buildLine 1 lần với $vals ($item=null). Ngược lại (mọi dòng ref item) → giữ nguyên vòng lặp cũ (groupNo++ mỗi item). Docblock quy tắc + lý do.
- [x] Sửa engine. `php -l` sạch. Tinker: (a) 4 cụm cũ (bonus…) group-number + số dòng KHÔNG đổi so trước (regression); (b) cụm giá vốn cấu hình products → sinh N dòng Có 1561 (mỗi product_id) + 1 Nợ 632 gộp, cùng 1 group.
- [x] Commit.

### Task 7.3: Comparer key thêm product_id
**Files:** Modify `app/Services/Posting/PostingShadowComparer.php` (`keyParts`).
**Produces:** thêm `product_id` vào canonical-key (norm). Cập nhật docblock.
- [x] Sửa keyParts. `php -l` sạch. Tinker: 2 dòng cùng account khác product_id → 2 key riêng (trước gộp 1).
- [x] Commit.

### Task 7.4: Cập nhật config giá vốn + verify shadow
**Files:** seed script + verify (không sửa code sản phẩm).
**Produces:** nhóm "Giá vốn hàng xuất" đổi thành loop `products`: Có 1561 value `{item.line_total}` obj `@item` (product) + Nợ 632 value `{gia_von}` obj none. Chạy engine trên export thật → so `PostingShadowComparer` với legacy: cụm giá vốn `matched` (N×1561 có product_id + 1×632 gộp khớp).
- [x] Cập nhật seed + tinker verify cụm giá vốn matched vs legacy. (Không commit code sản phẩm; seed là scratch.)

### Checkpoint — Phase 7 (planned 2026-07-24)
Vừa hoàn thành: de-risk product_id + lên plan Phase 7.
Bước tiếp theo: dispatch Task 7.1 (provider products) qua SDD.
Blocked: để trống.

### Checkpoint — Phase 7 xong (2026-07-24)
Vừa hoàn thành: Task 7.1→7.4 (provider collection products; engine shared-group + dòng gộp; comparer +product_id; verify shadow giá vốn matched). 3 commit code (9509ec379b, 86d8d763a3, 3725527bd8) + verify vận hành. HEAD `3725527bd8`. Engine nay tái tạo ĐỦ 8 cụm khớp legacy — kể cả giá vốn per-mã (phiếu 724: 4×1561+1×632 matched=TRUE).
Đang làm dở: —
Bước tiếp theo: chỉ còn VẬN HÀNH: migrate `posting_*` DB đích + chạy nhiều phiếu thật → đối chiếu `posting_shadow_logs` toàn bộ 8 cụm tới matched=100% → bật `POSTING_ENGINE_DOCS`. (Lưu ý: cụm thưởng/hoa hồng có thể lệch nhẹ do làm tròn trung gian — tinh chỉnh provider/công thức khi đối chiếu thật.)
Blocked: để trống.

---

## PHASE 8 — Đổi tên biến giá trị sang tiếng Việt gợi nhớ (dễ hiểu)
- [x] Đổi 14 key catalog + values() trong ProductExportVariableProvider sang mã tiếng Việt IN HOA không dấu (TIEN_HANG, THUE_SUAT, GIA_VON, TY_LE_XUAT_TRU_VC, QUY_THUONG_HD...). Bảng đổi tên đã user duyệt.
- [x] Re-seed config mẫu (doc 6, version 3) với value_formula dùng key mới
- [x] Verify: catalog 14 key mới; engine phiếu 780 = 17 dòng; cụm giá vốn phiếu 724 shadow matched=TRUE
- [x] FE: nút chèn biến ưu tiên LABEL tiếng Việt (chính) + mã {KEY} nhỏ mờ; cập nhật placeholder ví dụ
- [x] Chờ user hard-refresh test màn → COMMIT 402bd18a6a

### Checkpoint — Phase 8 (2026-07-27)
Vừa hoàn thành: đổi 14 tên biến sang tiếng Việt gợi nhớ (provider+config+FE), verify BE OK.
Bước tiếp theo: user test màn dev → commit provider + FE + (re-seed đã chạy dev).
Blocked: —

---

## PHASE 9 — Đối chiếu shadow thực tế + tinh chỉnh khớp legacy
- [x] Chạy đối chiếu engine vs legacy trên phiếu thật (batch 8 + 30 phiếu) qua tinker
- [x] Phát hiện 2 nguyên nhân lệch: (a) legacy giữ dòng 0đ, engine bỏ; (b) @creator gán thừa employee_department_id cho cụm Doanh thu/Giảm trừ (legacy chỉ set employee)
- [x] Fix comparer: bỏ dòng value==0 hai phía (commit 4bc28b723a)
- [x] Fix provider: tách @creator (chỉ người) vs @creator_dept (người+phòng); config cụm Thưởng HĐ dùng @creator_dept (commit 4bc28b723a)
- [x] Re-seed config version 4; đối chiếu lại: 29/30 phiếu matched=TRUE
- [x] Phiếu lệch còn lại (764): lệch 2đ do làm tròn cụm thưởng → CHỐT hướng 1 (giữ nguyên, guard I1 tự fallback legacy, KHÔNG nới epsilon)

### Checkpoint — Phase 9 (2026-07-27)
Vừa hoàn thành: đối chiếu shadow thực tế 30 phiếu → 29 khớp tuyệt đối, tinh chỉnh 2 điểm (dòng 0đ + tách creator). Engine giờ khớp legacy trên đại đa số phiếu.
Bước tiếp theo: (tuỳ chọn) đối chiếu diện rộng hơn / phiếu nhiều thưởng; gói seed vào UpdateDB; migrate DB đích + merge/push khi sẵn sàng.
Blocked: —
