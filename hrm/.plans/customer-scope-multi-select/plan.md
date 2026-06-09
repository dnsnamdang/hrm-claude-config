# Plan — customer-scope-multi-select

> Thực thi theo subagent-driven. Spec: `docs/superpowers/specs/2026-06-25-customer-scope-multi-select-design.md`
> Phụ trách: @manhcuong. Thứ tự: ERP (nguồn) → HRM (sync/FE). Verify browser cuối mỗi phase. KHÔNG đụng permission/git.

**Ràng buộc chung:** Pivot `customer_activity_types`(customer_id, customer_scope_group_id) + `customer_business_fields`(customer_id, customer_scope_id), unique cặp, id catalog HRM không FK cứng. Bỏ HẲN cột đơn `customers.customer_scope_group_id`/`customer_scope_id` sau backfill. Resource emit primary computed (phần tử đầu) + mảng `*_ids[]`. Catalog Loại hình↔Lĩnh vực N-N qua `customer_scope_group_members` — KHÔNG đổi schema catalog. Cột `customer_scope_*` trên prospective_projects/solutions/applications/meetings là field riêng — KHÔNG drop. Validate rethrow `ValidationException`; FE lỗi inline is-invalid/invalid-feedback + touched. Nhãn: "Loại hình hoạt động khách hàng" (tooltip "Là tập hợp cùng loại hình hoạt động sản xuất kinh doanh tương đồng về mặt công nghệ.") + "Lĩnh vực kinh doanh khách hàng" (tooltip "Khách hàng sản xuất kinh doanh sản phẩm dịch vụ cụ thể.").

---

## Phase 1 — ERP DB (TanPhatDev, mysql2)

- [x] BE: Migration tạo `customer_activity_types` + `customer_business_fields` (ERP DB), unique cặp customer_id+catalog_id, có timestamps — 2026_06_25_000001/000002
- [x] BE: Migration backfill pivot từ 2 cột đơn hiện có trên `customers` (mỗi giá trị ≠ null → 1 dòng), idempotent — 2026_06_25_000003
- [ ] BE: Migration (chạy sau, file riêng) DROP cột `customer_scope_group_id` + `customer_scope_id` trên `customers` — LÀM SAU khi backfill verify (Phase cuối)
- [ ] Verify (USER, chờ import DB ERP xong): chạy migrate, đối soát số dòng pivot == số KH có scope cũ

## Phase 2 — ERP BE (TanPhatDev)

- [x] BE: `Model/Sale/Customer.php` activityTypeIds/businessFieldIds + accessor primary (getPrimaryScopeGroupIdAttribute/getPrimaryScopeIdAttribute) + syncActivityTypes/syncBusinessFields
- [x] BE: `Model/Sale/Customer.php@searchByFilter` lọc theo pivot (subquery whereIn customers.id), bỏ filter cột đơn
- [x] BE: `CustomersController@store/update` validate `customer_scope_group_ids`/`customer_scope_ids` (required|array|min:1 + closure exists + thuộc ≥1 loại hình), message VN
- [x] BE: `CustomersController@store/update` lưu pivot qua sync trong transaction, KHÔNG set cột đơn
- [x] BE: `CustomersController` create/edit/show truyền scopeTree + ids đã chọn; response searchCustomer bổ sung ids + primary
- [x] BE: `Services/Hrm/CustomerScopeReader.php@scopeTree()` trả cây 2 cấp {id,name,scopes:[{id,name}]}
- [ ] Verify (USER): tạo/sửa KH chọn nhiều loại hình + nhiều lĩnh vực → pivot ghi đúng, validate chặn lĩnh vực không thuộc loại hình

## Phase 3 — ERP FE (blade + AngularJS)

- [x] FE: `customerForm.blade.php` đổi nhãn 2 trường + icon (i) tooltip (data-toggle=tooltip)
- [x] FE: trường Loại hình (A) → `<select multiple class=select2-dynamic>` ng-model mảng `customer_scope_group_ids` + ng-change onAChange
- [x] FE: trường Lĩnh vực (B) → ban đầu TreeView, SAU ĐỔI về multi-select (user chốt 2026-06-25, xem Phase 6); partial scopeTreeView.blade.php đã XÓA
- [x] FE: `customerScopeJs.blade.php` — scopeOptions() (B multi-select lọc theo A) + lọc chéo 2 chiều + auto-clear (onAChange dọn B; onBChange tự bỏ A theo); đã bỏ hàm tree
- [x] FE: `create.blade.php`/`edit.blade.php` init mảng/preload ids; `classes/sale/Customer.blade.php` submit `*_ids[]`
- [x] FE: `sale/customers/index.blade.php` đổi nhãn filter (giữ key, BE đọc pivot)
- [x] FE: `searchCustomer.blade.php` + 2 JS đọc primary/ids thay cột đơn
- [x] FE: `customermanager/show_.blade.php` A multiple + B tree, gọi activityTypeIds/businessFieldIds trong blade (CustomerManagerController không truyền compact → workaround, có thể cải thiện sau)
- [ ] Verify browser (USER, khi DB ERP sẵn sàng): create+edit chọn nhiều giá trị, lọc chéo+auto-clear, tree, list filter, searchCustomer. ⚠️ Kiểm KỸ: A select2-dynamic multiple có bind ng-model mảng + bắn ng-change không (nếu lỗi → đổi sang pattern class `select2` như vehicle_manufacts)

## Phase 4 — HRM DB (hrm-api)

- [x] BE: Migration tạo `customer_activity_types` + `customer_business_fields` (HRM, Modules/Human) — 2026_06_25_000001/000002
- [x] BE: Migration backfill pivot từ cột đơn HRM — 2026_06_25_000003
- [x] BE: Migration DROP cột đơn (file riêng 2026_06_25_000009, "CHẠY CUỐI CÙNG")
- [ ] Verify (USER): migrate, đối soát số dòng pivot, cột đơn đã mất

## Phase 5 — HRM BE (hrm-api)

- [x] BE: `Modules/Human/Entities/Customer.php` belongsToMany activityTypes/businessFields + activityTypeIds/businessFieldIds + accessor primary; bỏ scopeGroup()/scope() + 2 fillable
- [x] BE: `Modules/Assign/Http/Requests/Customer/{Save,Update}CustomerRequest.php` rule array + * + closure thuộc-loại-hình qua customer_scope_group_members, min:1, message VN
- [x] BE: Human requests GIỮ NGUYÊN (validate scalar theo catalog, không đụng cột customers) — module Human xử lý tối thiểu (user chốt)
- [x] BE: `Modules/Assign/Services/CustomerService.php` writeErpPivots (mysql2, trong transaction), filter list subquery pivot ERP, bỏ set/đọc cột đơn; scopeByCode() → primary+mảng
- [x] BE: `Modules/Timesheet/Services/CustomerService.php` syncSimpleData + sync_data() copy pivot ERP→HRM (map id theo code)
- [x] BE: `Transformers/CustomerResource/CustomerDetailResource.php` emit `*_ids[]` + primary (arrays[0]) + name null (FE resolve)
- [x] BE: `Human/Services/CustomerService.php` create/update/show/sync_data → pivot/primary (sync scalar→1 dòng); AUDIT toàn hrm-api: chỉ Human CustomerService đụng cột customers, downstream dùng cột RIÊNG entity (an toàn drop)
- [ ] Verify (USER): tạo/sửa KH qua HRM → ghi ERP + sync HRM đủ pivot; filter list OR; auto-fill TKT/meeting nhận primary

## Phase 6 — HRM FE (hrm-client)

- [x] FE: `CustomerForm.vue` field → mảng `customer_scope_group_ids`/`customer_scope_ids`, init từ pivot khi edit (fallback scalar)
- [x] FE: trường Loại hình (A) → V2BaseSelect multiple + nhãn mới + icon (i) tooltip (v-b-tooltip)
- [x] FE: trường Lĩnh vực (B) → V2BaseSelect MULTIPLE (KHÔNG tree — user chốt 2026-06-25) + nhãn mới + tooltip
- [x] FE: computed filteredScopes/filteredScopeGroups + watcher auto-clear (A→dọn B; B→tự bỏ A theo) có cờ guard _syncingScope chống loop; buildPayload gửi mảng
- [x] FE: validate inline ≥1 mỗi trường (scopeTouched + scopeGroupError/scopeError + is-invalid/invalid-feedback)
- [x] FE: `pages/assign/customers/index.vue` đổi nhãn cột/filter (giữ key, BE chấp nhận)
- [x] FE: `CustomerInfoSection.vue` (TKT) đổi nhãn; auto-fill đọc primary qua scope-by-code (không vỡ, hiện scope chính)
- [x] FE (ERP): đổi B tree→multi-select + sửa luôn modal searchCustomer ERP; xóa scopeTreeView.blade.php
- [ ] Verify browser (USER): /assign/customers add+edit+view+manager + Thêm nhanh KH TKT + ERP — nhãn+tooltip, multiselect, lọc chéo+auto-clear, lưu+load lại đúng. ⚠️ Kiểm is-invalid viền select2 (đã bù text đỏ)

## Phase 7 — Verify end-to-end

- [ ] Verify: tạo KH ở HRM → kiểm DB ERP + HRM khớp pivot; sửa ở ERP → sync về HRM; xóa giá trị → pivot cập nhật; downstream TKT/meeting/search không vỡ

---

### Iteration 6e — Fix ERP infinite digest (panel bung sẵn + click-out không đóng) — 2026-06-25
ROOT CAUSE (chẩn đoán qua Playwright pageerror): AngularJS `$rootScope:infdig` (10 digest iterations). `selectedBusinessFieldPairs()` → `getPairs()` → `normPairs()` tạo OBJECT MỚI mỗi lần gọi; ngRepeat chip B dùng $watchCollection so element theo tham chiếu → object mới mỗi digest = "luôn đổi" → digest vô hạn → ABORT → ng-show không kịp gán .ng-hide (panel display:block bung sẵn) + ng-click/backdrop không chạy (digest hỏng). Fix: selectedBusinessFieldPairs() trả THẲNG $scope.customer.customer_business_fields (ref ổn định; chuẩn hoá đã làm 1 lần ở loadCustomerScopes). selectedGroupIds trả số (primitive) nên không lỗi; filter trả cùng ref nên ổn. node --check OK. VERIFIED Playwright (ERP edit 43243): PAGEERRORS=[] (hết infdig), panelA/B display:none + hasNgHide:true (ẩn mặc định, chỉ hiện chip), scopeTreeOpen=false → cả 2 triệu chứng (panel bung sẵn + click-out không đóng) ĐÃ HẾT.

### Iteration 6d — ERP backdrop click-outside + chip/UI giống HRM — 2026-06-25
(1) Click-outside: bỏ handler $(document) (không đáng tin do multi-include), thay BACKDROP `.scope-dd-backdrop` (position:fixed z1050 trong suốt, ng-if khi mở, ng-click closeScopeTree/closeScopeGroupTree — Angular thuần). Panel z1051 trên backdrop. (2) Chip/dropdown ERP port style HRM `.csp-*` → `.escp-*` (prefix riêng, không đụng Bootstrap global): chip bo góc nền nhạt #eff6ff viền #bfdbfe, B chip "Loại hình(nhạt) : Lĩnh vực(đậm)" ellipsis, × hover đỏ; panel shadow + toolbar/search sticky + row hover; header nhóm đậm + con thụt lề. Thêm helper scopeLeafName (tên lĩnh vực thuần, tránh split chuỗi). node --check OK, div cân bằng, không @word lạc. ERP-only, user verify browser.

### Iteration 6c — Fix ERP click-outside không đóng dropdown — 2026-06-25
Nguyên nhân: customerScopeJs @include NHIỀU LẦN/trang (form + modal searchCustomer + customermanager), handler dùng `$(document).off('click.scopeTree').on()` chung → chỉ 1 handler sống sót bind vào $scope instance cuối (modal) → dropdown ở form không đóng khi click ngoài. Fix: namespace riêng theo $scope.$id + gỡ khi $destroy → mỗi instance 1 handler. node --check OK. (ERP-only, user tự test.) HOTFIX: comment chứa "@include" làm Blade parse lỗi "unexpected ','" → đổi thành "include" (bỏ @). Đã quét sạch @word lạc trong customerScopeJs/scopeFieldA/scopeFieldB.

### Iteration 6b — Lọc A→B chỉ theo loại hình CHỦ ĐỘNG chọn — 2026-06-25
Bug: A rỗng, tick 1 lĩnh vực → tự thêm loại hình cha vào A → lọc A→B kích hoạt → B bị lock chỉ còn loại hình đó. Fix: thêm state explicitGroupIds (loại hình user tick TRỰC TIẾP ở field A); lọc A→B dùng explicitGroupIds (không dùng customer_scope_group_ids). Loại hình tự thêm do tick lĩnh vực KHÔNG lọc B. dropGroupFromAIfNoPair/removePair/toggleGroup giữ loại hình explicit dù hết cặp. HRM (CustomerForm.vue) + ERP (customerScopeJs) đều sửa. Verify Playwright HRM: A rỗng → B hiện TẤT CẢ loại hình+lĩnh vực, chọn thoải mái. → DONE.

### Iteration 6 — CẶP (loại hình–lĩnh vực) + UI chip đẹp — 2026-06-25 (user chốt)
Bug: 1 lĩnh vực thuộc 2 loại hình → tick 1 chỗ sáng cả 2. User chốt: lưu THEO CẶP. Thêm cột customer_scope_group_id vào pivot customer_business_fields (ERP+HRM), unique(customer_id, customer_scope_id, customer_scope_group_id). B = mảng cặp {customer_scope_group_id, customer_scope_id}. A (customer_activity_types) = loại hình (giữ). Contract: payload save `customer_scope_group_ids`(A) + `customer_business_fields`(B pairs); resource trả `customer_scope_group_ids` + `customer_business_fields`(pairs) + `customer_scope_ids`(distinct, primary) + primary single. Validate mỗi pair: scope thuộc group (customer_scope_group_members). Hành vi: tick lĩnh vực dưới X→pair(X,Y)+X vào A; bỏ→nếu X hết lĩnh vực thì X rời A; bỏ X ở A→cascade bỏ pairs dưới X. UI: ERP chip overflow fix (wrap+max-height scroll); HRM rebuild component đẹp (<style scoped> .csp-*, dropdown nổi+toolbar+search+nhóm thụt lề+chip ellipsis — CSS cũ .scope-multi-* trong <style scss> global nên render vỡ). Lọc A→B: chọn loại hình ở A → B chỉ hiện lĩnh vực thuộc loại hình đó (HRM groupedScopeOptions + ERP filteredScopeGroupsForTree). → DONE. Migration cặp: ERP 2026_06_26_000001/2/3 + HRM Modules/Human 2026_06_26_000001/2/3 (thêm cột customer_scope_group_id + backfill + unique mới) — CHỜ USER chạy. VERIFY Playwright HRM (namdangit) PASS: A chips gọn không tràn, B dropdown đẹp lọc đúng theo A. ERP user xác nhận đẹp (chỉ còn user test cặp + tràn sau fix).

### Iteration 5 — chip + grouped-checkbox dropdown (tham khảo smart_application_form_3.html) — 2026-06-25
CẢ A và B dùng component chip+dropdown-checkbox (bỏ select2/V2BaseSelect cũ). A "Loại hình" = dropdown checkbox PHẲNG + chips tên loại hình. B "Lĩnh vực" = dropdown checkbox THEO NHÓM (header=loại hình có checkbox chọn-cả-nhóm, con=lĩnh vực) + chips "Loại hình : Lĩnh vực" + toolbar chọn/xóa tất cả + search. Header cha tick khi ≥1 con chọn (khác reference: reference tick khi đủ nhóm). Tick con→cha tick + loại hình vào A. Cross-sync A↔B giữ nguyên. Áp ERP (AngularJS, bỏ select2 cả A+B) + HRM (Vue). → DONE: HRM CustomerForm.vue (chip+dropdown A phẳng + B theo nhóm, header isParentChecked=≥1 con, compile+babel OK, v-click-outside); ERP partial mới scopeFieldA/scopeFieldB.blade.php include ở customerForm/searchCustomer/customermanager (errKey), customerScopeJs helper, header ng-checked=isGroupChecked(≥1 con), bỏ select2 cả 2 field, node --check OK. Chip B = "Loại hình : Lĩnh vực". Chờ user test browser.

### Đổi B sang TreeView dropdown — 2026-06-25 (iteration 4, user chốt)
Giữ 2 field. A "Loại hình" = multi-select riêng (tự điền theo cha tick). B "Lĩnh vực kinh doanh" = dropdown BẤM-MỚI-MỞ dạng tree (cha=loại hình, con=lĩnh vực, cha collapsible). Tick con → thêm vào B + cha tự tick (auto-fill A qua onBChange). Tick cha = chọn/bỏ tất cả con. Cha checked khi ≥1 con được chọn. Áp ERP (AngularJS dropdown panel) + HRM (Vue dropdown + v-click-outside). Logic cross-sync A↔B giữ nguyên. → DONE: HRM CustomerForm.vue (toggleLeaf tạo mảng mới→watcher fill A; scopesOfGroup/isParentChecked/toggleParent; v-click-outside); ERP customerScopeJs (tree state + toggleLeaf gọi onBChange + click handler namespaced) + customerForm/searchCustomer/customermanager (B markup tree, bỏ select2 B, submit qua model). Compile/node --check sạch. Chờ user test browser.

### Fix ERP select2 A bị mất — 2026-06-25
User báo: ERP chọn A rồi chọn 2 B tương ứng → A mất. Root-cause: onBChange destroy+reinit select2 A (options tĩnh) → reinit bắn 'change' transient → Angular ghi rỗng customer_scope_group_ids. Fix: thêm helper applyScopeSelect2Value (.val().trigger('change.select2'), Angular không nghe); onBChange KHÔNG reinit A, chỉ apply value; onAChange reinit B + apply lại value B; loadCustomerScopes apply value sau load (edit). Chờ user test browser. (Còn note: id A/B dùng chung form+modal — chỉ an toàn khi không render đồng thời 2 form; vấn đề có sẵn từ trước.)

### Fix mapping 2 chiều — 2026-06-25
User báo: chọn Lĩnh vực (B) trước phải tự fill Loại hình (A) cha tương ứng. ĐÃ sửa onBChange (HRM CustomerForm.vue watcher + ERP customerScopeJs): A = loại hình cha của lĩnh vực đang chọn (giữ thứ tự A cũ + auto-ADD cha mới + vẫn tự bỏ khi lĩnh vực con cuối bị bỏ). 1 lĩnh vực thuộc nhiều loại hình → fill tất cả cha. Guard chống loop giữ nguyên. Cập nhật spec mục 6.

### Checkpoint — 2026-06-25
Vừa hoàn thành: CODE DONE toàn bộ Phase 1-6 (subagent-driven, review từng phase + final whole-branch review PASS không Critical). ERP (TanPhatDev) + HRM (hrm-api + hrm-client) đều xong. UI multi-select cả 2 trường (bỏ tree theo user). Cột đơn chưa drop (migration 000009 chờ chạy cuối).
Đang làm dở: —
Bước tiếp theo (USER):
  1. Quyết định I-1 (màn Human single-select có thể ghi đè data multi của Assign — xem mục dưới).
  2. Chạy migration ERP (TanPhatDev: 000001/000002 tạo pivot + 000003 backfill) — KHÔNG chạy drop vội.
  3. Chạy migration HRM (hrm-api Modules/Human: 000001/000002 + 000003 backfill).
  4. Verify browser: /assign/customers (add/edit/view/manager) + Thêm nhanh KH TKT + ERP /admin/customers — nhãn+tooltip, multi-select, lọc chéo+auto-clear, lưu+load. ⚠️ Kiểm select2 multiple bind + viền is-invalid.
  5. Chạy full re-sync customer (M-3) để pivot HRM khớp ERP master, ĐỐI SOÁT, rồi mới chạy migration DROP cột (ERP 2026_06_25 drop + HRM 000009).
Blocked: chờ user quyết I-1 + verify (cần browser + chạy migration).
Final review minors: M-1 (đã fix), M-4 (đã fix), M-3 (ops: re-sync trước drop). I-1 (Important, chờ user).
