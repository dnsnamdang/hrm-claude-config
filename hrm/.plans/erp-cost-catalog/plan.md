# ERP Cost Catalog — Implementation Plan

**Goal:** Dòng dịch vụ/chi phí trong BOM & Quotation chọn từ danh mục `costs` ERP + tạo nhanh ghi thẳng vào danh mục ERP.

**Spec:** `design.md` (tóm tắt) · `design-phase1.md` (BE) · `design-phase2.md` (FE)
**Branch:** `tpe-develop-assign` · **Người phụ trách:** @dnsnamdang

---

## Phase B — Backend (hrm-api)

### B1. Model ERP (mysql2)
- [x] Tạo `Modules/Human/Entities/TpCost.php` (table `costs`, hằng kind_of/type, getKindList/getTypeList, scopeActive) — verified tinker OK
- [x] Tạo `Modules/Human/Entities/TpCompanyCost.php` (table `company_costs`) — verified

### B2. Endpoint dùng chung
- [x] Tạo `ErpCostStoreRequest` (mirror rule ERP; unique tên theo type check thủ công trên mysql2 qua `withValidator`)
- [x] Tạo `ErpCostController` — `index()` search + `store()` ghi mysql2 vào `costs` (BỎ company_costs/chiết khấu); `created_by` resolve qua `TpEmployee`
- [x] Thêm 2 route `GET/POST /assign/erp-costs` (không middleware permission)
- [x] Verify index qua tinker (classes resolve + trả đúng data). Store chưa test thật để tránh tạo rác `costs` ERP → để E2E.

### B3. Migration
- [x] Tạo migration thêm `cost_id` vào `quotation_service_items` và `bom_list_products` (unit_id đã nullable sẵn)
- [x] Chạy `php artisan migrate` + verify `Schema::hasColumn` = OK cả 2 bảng

### B4. Quotation nhận cost_id
- [x] `QuotationStoreRequest` + `QuotationUpdateRequest`: thêm `service_items.*.cost_id`, unit_id+qty nullable
- [x] `QuotationService` create/update: map `cost_id`, **ép `qty=1` khi có cost_id**, helper `resolveServiceVat` fallback vat từ `TpCost`
- [x] `QuotationController` storeServiceItem/updateServiceItem: rule cost_id + unit_id nullable + ép qty=1
- [x] `DetailQuotationResource::resolveServiceItems`: thêm `cost_id`

### B5. BOM nhận cost_id (dòng service)
- [x] `BomListStoreRequest`: thêm `parent.cost_id` + `children.*.cost_id`
- [x] `BomListService::mapProductPayload`: map `cost_id` + **ép `qty_needed=1`** khi product_type=2
- [x] `DetailBomListResource`: thêm `cost_id`

---

## Phase F — Frontend (hrm-client)

### F1. Component dùng chung (đọc skill modal-popup + button-convention trước)
- [x] Tạo `pages/assign/components/cost/CostPickerModal.vue` (search + filter loại + badge + nút Tạo nhanh)
- [x] Tạo `pages/assign/components/cost/CostQuickCreateModal.vue` (mirror ERP, field động theo kind_of, validate inline)

### F2. Quotation
- [x] `quotations/_id/edit.vue`: modal "Thêm dịch vụ" → chọn từ danh mục (CostPickerModal), tự điền name+vat+cost_id, **SL=1 khóa**
- [x] Payload service_items (bulk + endpoint): thêm cost_id, qty=1; `serviceItemErrors` bỏ qty/unit_id, yêu cầu cost_id
- [x] Bảng dịch vụ: bỏ sửa tên inline + khóa SL hiển thị (ĐVT cột chung để trống cho dòng DV)

### F3. BOM
- [x] `BomBuilderAddProductModal.vue` nhánh isService → chọn từ danh mục (CostPickerModal, name+cost_id), **SL=1 khóa**, bỏ ĐVT; goods giữ nguyên
- [x] `BomBuilderEditor.vue`: carry `costId` qua row (`handleAddProductApply` + `mapProductToRow`) + `mapGroupRowForSave` gửi `cost_id` + ép `qty_needed=1` cho service
- [ ] ⚠ Cần verify: `openEditRow`/editForm (sửa dòng inline) chưa giữ `costId` — kiểm tra khi test, bổ sung nếu mất link

---

## Phase F4 — Hợp nhất popup Thêm hàng hoá / dịch vụ (BOM + Quotation)

**Mục tiêu:** Gộp về 1 popup BOM với 2 tab; bỏ popup lồng + radio Dịch vụ trong tab Tạo mới. Tách panel danh mục dùng chung cho cả BOM + Quotation.

**Cấu trúc popup hợp nhất (title: "Thêm hàng hoá / dịch vụ"):**
- **Tab "Hàng hoá"**: danh sách hàng ERP (search + multi-select, như Tab 1 cũ) + nút **"Thêm hàng tạm"** → mở popup `BomProductCreateModal` (form hàng hoá thủ công, BỎ radio dịch vụ).
- **Tab "Dịch vụ & Chi phí"**: nhúng `CostCatalogPanel` (danh sách costs ERP + search + lọc loại + nút **"Thêm mới"** = tạo nhanh). Chọn 1 mục → emit apply (product_type=2, cost_id, SL=1).

### Tasks
- [x] **F4.1** Tách `pages/assign/components/cost/CostCatalogPanel.vue` (inline) — search + list + nút "Thêm mới" (mở `CostQuickCreateModal`); emit `select(cost)`
- [x] **F4.2** Rút gọn `CostPickerModal.vue` → modal mỏng bọc `CostCatalogPanel` (Quotation giữ nguyên hành vi)
- [x] **F4.3** (gộp vào F4.4) Form tạo hàng hoá thủ công → overlay "Thêm hàng tạm" trong `BomBuilderAddProductModal` (không tách file riêng để giảm rủi ro)
- [x] **F4.4** Tái cấu trúc `BomBuilderAddProductModal.vue`:
  - Tab "Hàng hoá": ERP list + nút "Thêm hàng tạm" → overlay form hàng hoá thủ công (createProduct đóng overlay, giữ modal)
  - Tab "Dịch vụ & Chi phí": nhúng `CostCatalogPanel`, chọn mục → `onServiceSelected` build item (product_type=2, cost_id, qty=1) → emit apply + toast
  - Bỏ tab "Tạo mới" + radio + `CostPickerModal` lồng; footer tab Dịch vụ chỉ còn "Đóng". Tag cân bằng OK.
- [x] **F4.5a** BOM `BomBuilderTableCard`: "Chọn hàng hoá"/"Thêm hàng hoá" → **"Thêm mới"** (giữ "Thêm con")
- [x] **F4.5b** Quotation (`edit.vue`): "Thêm sản phẩm"+"Thêm dịch vụ" → 1 nút **"Thêm mới"** (hiện khi canEdit cả 2 mode). Truyền `:serviceOnly="!isDirectQuotation"` (direct→2 tab; từ BOM→chỉ tab Dịch vụ). `onAddProductApply` route product_type=2/cost_id → `serviceItems` (giá inline, vat prefill từ cost). Bỏ modal `showAddServiceModal` + `CostPickerModal` (gỡ import/registration). Thêm prop `serviceOnly` vào BomBuilderAddProductModal (ẩn tab Hàng hoá + footer).
- [ ] **F4.6** Verify E2E (BOM + Quotation) — cần dev server

---

## Phase F5 — Bugfix sau test popup hợp nhất

- [x] **F5.1** Quotation: gen mã hàng hoá tự nhập khi để trống (`nextGoodsCode()` pattern HHxxxxxx, dùng trong `onAddProductApply`; ERP giữ rỗng). BOM đã gen sẵn qua `getNextGoodsCode`.
- [x] **F5.2** Quotation bảng chi tiết: khóa sửa inline **mã/tên/ĐVT** (cha + con) → chỉ còn editable SL + đơn giá nhập + đơn giá bán (theo logic cũ, đồng bộ BOM table). Tên/ĐVT nhập qua popup "Thêm mới".
- [x] **F5.3** Popup tạo nhanh dịch vụ bị ẩn dưới popup cha → (v1) z-index b-modal chưa ăn ở Quotation → (v2) **đổi `CostQuickCreateModal` sang overlay custom** (`.cost-qc-backdrop` position fixed z-index 5300, native `<select>` cho loại chi phí) → chắc chắn nổi trên mọi popup cha.

## Phase F6 — Đồng nhất build hàng hoá/dịch vụ BOM ↔ Báo giá tạo độc lập (CHỜ CHỐT HƯỚNG)

Approach B (chốt qua brainstorming): popup sửa riêng cho Quotation, không đụng BOM.

- [x] **F6.1** Tạo `QuotationProductEditModal.vue` (sửa hàng tạm: tên/mã/ĐVT/model/hãng/xuất xứ/spec; V2BaseSelectRemote tự fetch + initialOption; validate inline name+ĐVT)
- [x] **F6.2** Tái dùng `CostPickerModal` cho sửa dịch vụ (re-import vào edit.vue)
- [x] **F6.3** edit.vue: nút "Sửa" dòng hàng tạm (non-ERP, cạnh "Thêm con") → `openProductEdit`→`onProductEditSave` merge; nút "Sửa" dòng dịch vụ → `openServiceReselect`→CostPickerModal→`onServiceReselect` (đổi cost_id/name/vat). Compile OK.
- [ ] **F6.4** Verify dev server: sửa hàng tạm + sửa dịch vụ → lưu/reload đúng

## Phase F7 — Bugfix (sau test F6)

- [x] **F7.1** Lưu báo giá có dịch vụ → 500 `Column not found: 'specification'` (bảng `quotation_service_items` không có cột này nhưng `QuotationService::create()` hardcode insert). Đây là nguyên nhân thực của "popup tạo nhanh không phản hồi" (cost ĐÃ tạo OK, fail ở bước lưu). → Bỏ `'specification'` khỏi insert create() (FE không gửi; update() cũng không). Không cần migration.
- [x] **F7.2** Lệch cột dòng dịch vụ: nút sửa/xoá nằm ô "TT sau VAT" còn cột thao tác cuối trống → ở direct mode chuyển nút sang cột thao tác cuối (đồng nhất dòng sản phẩm); non-direct giữ trong ô cuối.
- [x] **F11** (a) Bug: sửa input VAT (type=number) trong popup tạo nhanh → arrow Up/Down bị `b-tabs` cha bắt → đổi tab → ẩn overlay (tưởng đóng). Fix: thêm `no-key-nav` cho b-tabs `BomBuilderAddProductModal` + `@keydown.stop` trên `.cost-qc-card`. (b) Đổi nền phần "Dịch vụ bổ sung" sang xanh nhẹ (header `#e2f5ee`, row `.service-item-row` `#eef9f4`).
- [x] **F10** Đồng nhất logic nhóm Báo giá theo BOM:
  - **Invariant "đã dùng nhóm → tất cả trong nhóm"**: tạo nhóm auto-gán hàng lẻ vào nhóm mới (giống BOM `saveGroupModal`); add modal bắt chọn nhóm khi đã có nhóm (sẵn từ BomBuilderAddProductModal); save safety-net `assignOrphanProductsToFirstGroup`; xoá nhóm → chuyển hàng sang nhóm còn lại (giữ invariant, không tạo orphan).
  - **Sửa nhóm đồng nhất**: bỏ sửa inline ở Báo giá → dùng **modal Thêm/Sửa nhóm** (showGroupModal + groupModalMode add/edit) giống BOM. Pencil → modal edit; "Thêm nhóm" → modal add. Button theo V2BaseButton (Lưu/Thêm primary trước, Huỷ tertiary cuối).
- [x] **F9** Đồng nhất thêm hàng vào Group ở Báo giá theo BOM: mỗi group header có nút **"Thêm mới"** (`openAddNewForGroup` → set `addProductTargetGroupId` = group.id/temp_id → modal pre-target nhóm → hàng hoá vào đúng nhóm). Wiring directGroupsForModal/bomGroupOptions/targetGroupId đã sẵn. CHỐT: **dịch vụ giữ section riêng** (không vào nhóm) — khác BOM nhưng theo quotation-redesign.
- [x] **F8** Chuẩn hoá button popup "Thêm mới" (`BomBuilderAddProductModal`) theo V2BaseButton (giữ backdrop custom — chọn "chỉ sửa button"): footer tab Hàng hoá đổi thứ tự primary "Thêm N" trước → tertiary "Đóng" cuối (+icon fas fa-arrow-left); footer tab Dịch vụ "Đóng" +icon; quick-add overlay đổi Lưu(primary) trước → Huỷ cuối; header "Đóng" +icon. Manual overlay footer + toolbar đã chuẩn sẵn.
- [x] **F7.5** ⭐ ROOT CAUSE "Lưu không phản hồi": dự án dùng **vee-validate v2** → inject `this.errors` (ErrorBag) vào MỌI component, che computed `errors` của tôi → `isValid` luôn false (ErrorBag có keys) → Lưu luôn bị chặn ngầm; toast `Object.values(this.errors)` ra rác ("225"). Fix: đổi computed `errors`→`formErrors` trong `CostQuickCreateModal` + `QuotationProductEditModal`.
- [x] **F7.4** Thêm Giá vốn / Giá bán (hiện đơn vị tiền tệ qua prop `currencyCode` drill edit.vue→BomBuilderAddProductModal→CostCatalogPanel→CostQuickCreateModal + CostPickerModal). Khi lưu: `rate_value_capital = round(giá vốn/giá bán×100, 2)`. Giá nhập/bán đính kèm cost → dòng dịch vụ tự điền (tránh nhập lại). Fix "Lưu không phản hồi": **toast khi validate fail** (không im lặng) + `console.error` trong catch.
- [x] **F7.3** SỬA LOGIC DỊCH VỤ (note lại từ user): catalog chỉ `status=1 && kind_of=2`. Phân 2 loại bằng `revenue_calculation` (1=Dịch vụ có tính DT, 0=Chi phí khác), `type=null`. Quick-create: "Loại"=selectbox mặc định chưa chọn (2 lựa chọn), bỏ checkbox/tỷ lệ giá vốn/tên TA/loại chi phí, giữ Tên+VAT. → `ErpCostStoreRequest` (kind_of in:2, revenue_calculation required in:0,1, rate_value_capital nullable), `ErpCostController::index` (where kind_of=2 + filter revenue_calculation + badge theo rev), `CostQuickCreateModal` (selectbox), `CostCatalogPanel` (filter revenue_calculation). Việc bỏ rate_value_capital bắt buộc cũng fix "Lưu không phản hồi".

---

## Phase V — Verify E2E (xem design.md / plan đã duyệt)
- [ ] Migration OK
- [ ] Search erp-costs theo kind_of
- [ ] Tạo nhanh Dịch vụ (kind_of=2) → row costs + company_costs
- [ ] Tạo nhanh Chi phí (kind_of=1, type) + check trùng tên
- [ ] Quotation: thêm DV từ danh mục → lưu/reload đúng, sửa VAT được, không ĐVT
- [ ] BOM: thêm DV từ danh mục → lưu/reload đúng
- [ ] Backward-compat: dòng cũ cost_id=null vẫn chạy

---

## Phase P3 — Tách Dịch vụ & Chi phí khác thành bảng riêng trên BOM (đồng nhất Báo giá)

Spec: `design-phase3.md`. Chốt: bảng mới cost-only, KHÔNG migrate data cũ.

### Backend
- [x] **P3.B1** Migration tạo `bom_list_service_items` (bom_list_id, cost_id, name, code, qty, estimated_price, vat_percent, note, sort_order, audit)
- [x] **P3.B2** Entity `BomListServiceItem` + `BomList::serviceItems()` hasMany
- [x] **P3.B3** `BomListStoreRequest`: thêm mảng `service_items.*`
- [x] **P3.B4** `BomListService` store/update: sync serviceItems vào bảng mới (không tạo product_type=2)
- [x] **P3.B5** `DetailBomListResource`: trả `service_items`
- [x] **P3.B6** `QuotationService::createFromBom`: copy BOM serviceItems → quotation service_items (cost_id, giá vốn, vat)

### Frontend
- [x] **P3.F1** `BomBuilderEditor`: data `serviceItems`, load từ resource, apply service vào serviceItems, buildSavePayload thêm service_items, orphan-net không đụng service
- [x] **P3.F2** `BomBuilderTableCard`: section "Dịch vụ & Chi phí khác" riêng (nền xanh nhẹ) + nút Thêm mới + sửa/xoá; bỏ render product_type=2 mới trong nhóm
- [x] **P3.F3** `BomBuilderAddProductModal` `onServiceSelected`: emit service (cost_id, giá vốn, vat) không cần nhóm hàng
- [ ] **P3.V** Verify dev server: thêm DV BOM → bảng mới; hàng hoá theo nhóm; BOM→báo giá DV chảy sang; BOM cũ OK
- [x] **P3.B6b** Đã tra luồng: `create()` (POST /assign/quotations — dùng cho cả tạo báo giá lẫn YCXD giá từ pricing-requests) ĐÃ copy; `createFromBom()` (POST create-from-bom — tab Hồ sơ trình duyệt) NAY đã copy dịch vụ. `createFromRequest()` = **dead code** (không caller) → bỏ qua.

---

## Phase P4 — Nhúng section dịch vụ vào trong bảng Chi tiết BOM (đồng nhất Quotation)

Sai logic: section "Dịch vụ & Chi phí khác" trên BOM đang là 1 card độc lập tách rời bảng. Quotation render dịch vụ NGAY TRONG bảng chi tiết (cùng `<table>`, sau hàng hoá, có hàng phân cách). → BOM phải giống vậy.

- [x] **P4.1** `BomBuilderTableCard.vue`: thêm prop `serviceItems`; render `<tbody class="bom-service-tbody">` cuối bảng (hàng phân cách "Dịch vụ & Chi phí khác" nền xanh + nút Thêm mới + các dòng DV khớp cột động `visibleColumns`, VAT inline trong ô Tên, giá vốn = cột Giá nhập) + emit `open-service-add` / `remove-service`. Không mang class `group-tbody` → không bị sortable kéo
- [x] **P4.2** `BomBuilderEditor.vue`: bỏ block section độc lập; truyền `:service-items` + `@open-service-add`/`@remove-service`; container-fluid đóng lại ngay sau card
- [x] **P4.3** Đổi nhãn "Dịch vụ bổ sung" → "Dịch vụ & Chi phí khác" trên Quotation (`edit.vue:436`, `index.vue:262`, `QuotationPrintPreview.vue:93`); BOM đã đúng tên
- [x] **P4.V** Compile-check 5 SFC = TPL OK. (User hard-refresh xác nhận sau)

## Phase P5 — Đồng nhất thao tác Dịch vụ/Chi phí + kéo thả BOM ↔ Quotation

Mục tiêu: thao tác giống nhau giữa BOM và Quotation; khác biệt duy nhất là BOM không có Giá bán + VAT.

- [x] **P5.1** BOM service row: bỏ input VAT inline ở cột Tên hàng (BomBuilderTableCard)
- [x] **P5.2** BOM service row: drag handle `.drag-service` ở cột Thao tác + sortable (initSortables thêm sortable cho `tbody.bom-service-tbody`, key theo `_uid`); Editor gắn `_uid` (load + apply) + `reorderServices` + watch serviceItems re-init
- [x] **P5.3** Quick-create BOM ẩn Giá bán + VAT: prop `hideSaleVat` drill `BomBuilderAddProductModal`(`quickHideSaleVat`)→`CostCatalogPanel`→`CostQuickCreateModal`; BOM gửi vat=0, rate=0 (BE `vat_percent` required|numeric|min:0 chấp nhận 0). Quotation default false (giữ nguyên)
- [x] **P5.4** Quotation service rows: tách `tbody.q-service-tbody` + grip `.q-drag-service` ở cột STT + `reorderQuotationServices` (`_uid` cho service, load + apply); giữ Giá bán + VAT. BE đã `sort_order=$i` + relationship `orderBy('sort_order')` → persist
- [x] **P5.5** Quotation hàng hoá kéo thả như BOM: tách render thành `<tbody class="q-parent-tbody">` per-parent + `<tbody>` group head; grip `.q-drag-parent`/`.q-drag-child` ở cột STT; `initQuotationSortables` (Sortable cho parent + child + service) + `reorderQuotationParents`/`reorderQuotationChildren`; signature `rowStructureSignature` re-init; **BE: thêm `orderBy('sort_order')` cho `$prices` nhánh direct trong DetailQuotationResource** (đọc đúng thứ tự sau reload)
- [x] **P5.V** Compile-check 6 SFC = TPL OK + JS OK. (User hard-refresh xác nhận)
- [x] **P5.6** Báo giá tự xây dựng (direct): thêm cột "Thao tác" ĐẦU TIÊN như BOM (thead + group-head + parent + child + service + tfoot colspan). Drag handle + Xoá (parent/child), drag + Chọn lại + Xoá (service) dồn vào cột thao tác; bỏ cột thao tác cuối; bỏ grip ở cột STT (parent/child); non-direct giữ grip STT cho service. Sửa/Thêm con (parent) vẫn dưới tên
- [x] **P5.7** Header nhóm "Dịch vụ & Chi phí khác" trên Quotation: style giống BOM (nền `#e2f5ee`, title `#0f8a63` + icon, `.q-service-sep-row`) + nút **"Thêm mới"** (`openServiceAdd` mở popup tab Dịch vụ qua `addModalInitialTab=1` + prop `:initial-tab`)
- [x] **P5.8** Form thêm mới (BOM + Quotation) luôn hiển thị 2 phần có header cùng style xanh: **A — Hàng hoá** + **B — Dịch vụ & Chi phí khác**.
  - BOM `BomBuilderTableCard`: thêm `<tbody>` header "A — Hàng hoá" (class chung `.bom-section-row`/`.bom-section-title`) ngay sau thead + nút Thêm mới (dời từ toolbar); đổi B header "B — Dịch vụ & Chi phí khác"; bỏ nút "Thêm mới" primary trùng ở toolbar
  - Quotation `edit.vue`: thêm `<tbody>` header "A — Hàng hoá" (class chung `.q-section-row`/`.q-section-title`) sau thead + nút Thêm nhóm/Thêm mới (dời từ toolbar trên); đổi B header; bỏ "Thêm nhóm"+"Thêm mới" trùng ở toolbar trên
- [x] **P5.9** Màn SHOW (xem) thể hiện 2 phần A/B như tạo/sửa:
  - BOM view (`bom-list/_id/index.vue` dùng BomBuilderEditor view-only → BomBuilderTableCard): A header sẵn always; đổi B `v-if` bỏ gate viewOnly (`!pricingMode`) → B luôn hiện cả ở view (read-only, có hint "Chưa có")
  - Quotation view (`quotations/_id/index.vue` — component riêng): thêm header A "A — Hàng hoá" + đổi B "B — Dịch vụ & Chi phí khác" (style xanh `.q-section-row`/`.q-section-title`), B luôn hiện + hàng "Chưa có dịch vụ"
- [x] **P5.10** Tách "Thêm mới" thành 2 popup riêng (Hàng hoá / Dịch vụ) — CHỐT cách "ẩn tab": prop `goodsOnly` cho `BomBuilderAddProductModal` (ẩn tab Dịch vụ, title "Thêm hàng hoá"); BOM + Quotation bind `:goods-only`/`:service-only` theo `addModalInitialTab`. Quotation non-direct: chỉ popup Dịch vụ. Fix `openAddChildProduct` set tab=0
- [x] **P5.11** Bỏ select "Nhóm hàng" trong tab Dịch vụ của popup (dịch vụ là nhóm riêng, không cần chọn nhóm hàng hoá)
- [x] **P5.12** Hiện tổng cộng trên dòng header A/B (BOM + Quotation tạo/sửa + xem) — v1: text dồn phải
- [x] **P5.13** ĐỔI: tổng **căn theo từng cột** (mirror dòng TỔNG cuối bảng), không dồn phải:
  - BOM `BomBuilderTableCard`: header A/B dựng nhiều `<td>` khớp `visibleColumns` — label colspan `viewOnly?3:4`, đổ tổng vào cột importAmount/amount/profitMargin (A: totalImport/totalAmount/totalProfitMargin; B: serviceImportTotal ở cột Giá nhập, còn lại trống)
  - Quotation `edit.vue`: header A/B mirror tfoot (label colspan `7:6`), đổ vào TT nhập/TT bán/Tiền VAT/TT sau VAT — computeds thêm `productSaleAfterDiscountTotal`/`productVatTotal`/`serviceSaleAfterDiscountTotal`/`serviceVatTotal`
  - Quotation `index.vue` (xem): mirror tfoot view (thứ tự cột khác: TT bán ngay sau Giá bán) — đổ TT nhập/TT bán/Tiền VAT/TT sau VAT theo cột

- [x] **P5.14** BOM bỏ TOÀN BỘ logic nhập giá nhập (hàng hoá + dịch vụ + chi phí). CHỐT (qua hỏi): BOM hiện đã ẩn giá bán từ Phase 11 → bỏ giá nhập = BOM **không còn cột giá nào** (chỉ cấu trúc). Mọi giá nhập ở Báo giá.
  - `BomBuilderEditor`: `visibleColumns.estimatedPrice/importAmount = false`; bỏ 2 key khỏi `columnOptions` (toggle không còn)
  - Popup tạo nhanh: đổi prop `hideSaleVat`→`hidePricing` (ẩn cả Giá vốn + Giá bán + VAT, chỉ còn Loại + Tên) — drill `BomBuilderEditor`(`quick-hide-pricing`)→`BomBuilderAddProductModal`(`quickHidePricing`)→`CostCatalogPanel`(`hidePricing`)→`CostQuickCreateModal`; gửi cost/sale/vat/rate=0
  - Bỏ ô "Giá nhập" form "Thêm hàng tạm" (`BomBuilderAddProductModal`) + form sửa dòng (`BomBuilderEditModal`)
  - Dịch vụ BOM: ô giá vốn inline nằm trong cột estimatedPrice → tự ẩn; header B không còn tổng giá
  - Quotation giữ nguyên (hidePricing mặc định false → vẫn nhập đủ giá vốn/giá bán/VAT)
  - Lưu ý: `estimated_price` vẫn còn trong DB/payload (=0), Báo giá nhập giá thật. Import Excel chưa đụng (cột giá nếu có vẫn map ngầm, không hiển thị)

- [x] **P5.17** (a) Bỏ nền các row item (hàng hoá/dịch vụ/chi phí) trên BOM + Báo giá (edit + view) — chỉ giữ nền dòng group + header A/B. Xoá bg `.bom-parent-row`/`.bom-service-item-row` (BOM), `.parent-row`/`.service-item-row` (báo giá edit), `.parent-row` (view). (b) Icon phân biệt Dịch vụ (`ri-service-line` xanh) vs Chi phí khác (`ri-money-dollar-circle-line` cam) theo `revenue_calculation`: BE 2 resource trả `revenue_calculation` (tra `TpCost` theo cost_id, batch); FE thêm field khi add (onServiceSelected) + load; icon ở BOM row + Báo giá edit row + view (badge DV/CP)
- [x] **P5.16** Đổi loại BOM chưa clear Dịch vụ & Chi phí khác → bổ sung `serviceItems` vào check `hasData` + clear `this.serviceItems = []` ở cả nhánh clear trực tiếp lẫn nhánh sau xác nhận (`handlebom_list_typeChange` + `handleConfirmDeleteAction`)
- [x] **P5.15** Fix popup tự đóng khi focus/click vào input number (spinner) — cả popup "Thêm hàng tạm" + "Tạo nhanh Dịch vụ/Chi phí". Nguyên nhân: click/mousedown bên trong nổi (bubble) lên backdrop/b-tabs (`@keydown.stop` cũ không trị vì là sự kiện click chứ không phải arrow). Fix: thêm `@keydown.stop @click.stop @mousedown.stop` trên card của 3 overlay (`cost-qc-card`, `bom-quick-add-card` ×2). Click backdrop ngoài vẫn đóng bình thường.

- [x] **P5.21** Tài liệu: `changes-summary.pdf` (tổng hợp thay đổi luồng BOM→Báo giá) + `testcase.xlsx` (40 test case BOM→Báo giá, 10 nhóm). Script sinh: `_gen_docs.py`
- [x] **P5.20** Check + fix lỗi gộp BOM với logic mới: `applySubBomSelection()` chỉ gộp products+groups, BỎ QUA `service_items` của BOM con → mất dịch vụ khi gộp + khi lưu `syncServiceItems` xoá sạch. Fix: gộp `detail.service_items` từng BOM con vào `allServiceItems` (id=null, _uid mới, giữ cost_id/revenue_calculation/name/estimated_price/vat) → `this.serviceItems = allServiceItems`. (product_type=2 cũ vẫn hỗ trợ song song — không lỗi; estimated_price=0 đúng vì BOM không nhập giá)
- [x] **P5.19** BOM cột Số lượng căn giữa đồng nhất hàng hoá + dịch vụ (tạo/sửa/xem): `.table-input` thêm `text-align:center`, td qty + th "Số lượng" thêm `text-center`
- [x] **P5.18** Quotation thêm 4 cột Model/Thương hiệu/Xuất xứ/TSKT sau cột Tên hàng + nút "Ẩn/Hiện cột chi tiết" (mặc định hiện) — áp dụng tạo/sửa (`edit.vue`) + xem (`index.vue`). Flag `showQuotationExtraCols`; thêm th + td (parent/child/service) gated cùng flag; spec render v-html `.q-spec-preview`; colspan động: `tableColspan`/`totalColspan` +4, leading colspan header A/B + tfoot TỔNG +4. BE đã trả sẵn model_name/brand_name/origin_name/specification; bổ sung map `specification` ở edit fetchData.

## Phase P6 — Bugfix hàng tạm Báo giá tự xây dựng

- [x] P6.1 — Hàng tạm cấp con: bổ sung button "Sửa" (mở `QuotationProductEditModal`) — chỉ hiện với hàng tạm (`!isErpProduct`) không phải dịch vụ
- [x] P6.2 — `QuotationProductEditModal`: thay `<textarea>` Thông số kỹ thuật bằng rich editor `CompactReviewEditor` (đồng nhất form Thêm hàng tạm)

## Phase P7 — Tách 2 cột chiết khấu phân bổ (CK tổng)

- [x] P7.1 — Thêm cột read-only "CK phân bổ tự động": FE tính live theo tỷ lệ giá trị (largest remainder, khớp BE `allocateDiscount`)
- [x] P7.2 — Đổi tên cột "CK phân bổ" → "Phân bổ CK" (input, lưu DB), chỉ ghi đè bằng giá trị auto khi bấm "Phân bổ tự động"
- [x] P7.3 — Nút "Phân bổ tự động"/"Phân bổ lại": confirm cảnh báo ghi đè (`$bvModal.msgBoxConfirm`) → fill FE từ cột tự động (`applyAutoAllocation`), bỏ round-trip backend
- [x] P7.4 — Cập nhật colspan (edit `tableColspan` 14→15, view `discountExtraCols` 1→2) + header A/B + tfoot + child rows cho 2 cột
- [x] P7.5 — View (index.vue): hiển thị 2 cột read-only đồng nhất (auto tính lại từ giá đã lưu + Phân bổ CK đã lưu)

## Phase P8 — Bugfix lưu hàng tạm cha-con (báo giá tự xây dựng)

- [x] P8.1 — FE: payload products gửi `temp_id` (=_tempId) + tách `parent_id` (chỉ integer khi cha đã lưu) / `parent_temp_id` (temp string `p_*` khi cha mới)
- [x] P8.2 — BE request: thêm rule `products.*.temp_id` + `products.*.parent_temp_id` = nullable|string (Store + Update)
- [x] P8.3 — BE `upsertDirectProducts`: tách `saveDirectProduct()` + 2-pass — tạo cha trước (map tempId→id), pass 2 resolve `parent_id` cho con của cha tạm

## Phase P9 — Tinh chỉnh UI cột CK phân bổ + VAT + Tỷ suất LN

- [x] P9.1 — Header "CK phân bổ tự động": bỏ text phụ → icon info `ri-information-line` + tooltip hover (edit + view)
- [x] P9.2 — Input "Phân bổ CK" disabled khi `totalQuotationDiscount <= 0` (chưa có CK tổng) — cha + dịch vụ
- [x] P9.3 — Căn giữa VAT row hàng hoá: scoped CSS `.vat-cell` dùng `::v-deep` (xuyên V2BaseInput) — đồng nhất dịch vụ
- [x] P9.4 — Tỷ suất LN dịch vụ: thêm `svcMarginPercent()` → null khi chưa nhập giá nhập → hiển thị "—" như hàng hoá
- [x] P9.5 — Hiển thị tỷ giá áp dụng (`1 <currency> = <rate> VND`) căn phải (`ml-auto`) trên toolbar VAT/làm tròn/CK, chỉ khi currency ≠ VND

## Phase P10 — Đồng nhất button "Thêm nhóm" BOM theo Quotation

- [x] P10.1 — Đổi tên "Tạo nhóm" → "Thêm nhóm" và chuyển từ toolbar card vào header section A (trước "Thêm mới"), style `tertiary size=xs` + icon `ri-folder-add-line` giống Quotation

## Phase P11 — Dịch vụ/Chi phí ERP: giá vốn tính ngược từ giá bán theo tỷ lệ

- [x] P11.1 — Carry `rate_value_capital` qua luồng chọn ERP (CostPicker → AddProductModal `onServiceSelected` → edit `onAddProductApply` + `onServiceReselect`)
- [x] P11.2 — BE `DetailQuotationResource::resolveServiceItems`: trả thêm `rate_value_capital` (lookup TpCost theo cost_id)
- [x] P11.3 — edit.vue: giá vốn (estimated_price) input disabled khi `svcHasRate`; giá bán `@input` → `recalcSvcCost` (giá vốn = giá bán × rate%/100)
- [x] P11.4 — Hiển thị badge "Tỷ lệ giá vốn: X%" ở cột tên dịch vụ (edit + view)

## Phase P12 — Bugfix: tạo báo giá từ BOM (PricingRequest) không kế thừa Dịch vụ & Chi phí

- [x] P12.1 — `QuotationService::createFromRequest`: bổ sung copy `bomList->serviceItems()` → `quotation_service_items` (mirror `createFromBom`). (`create()` + `createFromBom()` đã có sẵn — chỉ path PricingRequest thiếu)

## Phase P13 — Khoá giá vốn cho mọi dịch vụ ERP (không chỉ khi có rate)

- [x] P13.1 — `svcFromErp(svc)=!!cost_id` → khoá ô giá vốn cho mọi dịch vụ/chi phí từ ERP (P11 cũ chỉ khoá khi rate!=null → cost ERP không có tỷ lệ vẫn editable). recalc giữ nguyên (chỉ tính khi có rate); tooltip phân biệt có/không tỷ lệ.

## Phase P14 — Tỷ lệ giá vốn: tách logic Báo giá tự lập vs từ BOM (chốt lại)

- [x] P14.1 — Chốt: tự lập = chỉ nhập giá bán + giá vốn tính từ tỷ lệ ERP (P11). Từ BOM = nhập CẢ giá vốn + giá bán, PM tự tính tỷ lệ
- [x] P14.2 — FE edit.vue: `svcCostLocked = isDirectQuotation && cost_id` (chỉ khoá giá vốn ở tự lập); `svcRatePercent` (tự lập=rate ERP, BOM=giá vốn/giá bán live); badge cột Tên hàng + tooltip phân biệt; `onSvcSalePriceChange`
- [x] P14.3 — BE `syncServiceCostRatesToErp`: báo giá từ BOM (non-direct) khi lưu → ghi `rate = giá vốn/giá bán×100` về `costs.rate_value_capital` (ERP mysql2) cho item có cost_id, quoted_price>0. Gọi ở cả create + update

## Phase P15 — Hiển thị tỷ giá kèm ngày ghi nhận + ở màn xem

- [x] P15.1 — edit.vue: tỷ giá toolbar thêm ngày ghi nhận = ngày tạo báo giá (`item.created_at`, formatDateVN)
- [x] P15.2 — index.vue (xem): hiển thị tỷ giá ở cell "Loại tiền tệ" (computed `exchangeRate` + ngày tạo), chỉ khi currency ≠ VND

## Phase P16 — Bugfix validate giá dòng dịch vụ (false positive)

- [x] P16.1 — `validatePrices()`: bỏ check `!s.unit_id` (dịch vụ ERP không có ĐVT → luôn false positive) + bỏ bắt buộc `estimated_price>0` (giá vốn có thể 0 / bị khoá theo tỷ lệ). Giữ bắt buộc tên + SL>0 + giá bán>0

## Phase P17 — Validate hàng con không trùng mã CHA trực tiếp (BOM + Báo giá)

- [x] P17.1 — Chốt scope: con ≠ mã CHA trực tiếp (không cho thêm chính cha làm con)
- [x] P17.2 — Quotation `onAddProductApply`: bỏ qua + toast dòng con trùng mã cha; helper `sameProductCode` (erp_product_id ưu tiên, fallback code)
- [x] P17.3 — BOM `handleAddProductApply`: tương tự; helper `sameProductCode` xử lý cả camelCase/snake

## Phase P18 — Fix hàng tạm trùng mã (gộp BOM) gây lỗi validate

- [x] P18.1 — `sameProductCode` (BOM + Báo giá): chỉ coi CÙNG sản phẩm khi cùng `erp_product_id`; bỏ fallback so code → hàng tạm khác tên trùng mã auto KHÔNG còn bị chặn sai khi thêm con
- [x] P18.2 — Gốc: `applySubBomSelection` gộp BOM giữ nguyên mã con → trùng. Thêm `dedupeTempGoodsCodes()` đánh lại mã HH duy nhất cho hàng tạm trùng (giữ lần đầu)

## Phase P19 — Khoá sửa mã hàng tạm ở màn edit (chống nhập trùng mã)

- [x] P19.1 — `QuotationProductEditModal`: input Mã → `:disabled="true"` (chỉ hiển thị). BOM `BomBuilderEditModal` đã khoá sẵn

## Checkpoint

### Checkpoint — 2026-06-05 (Phase P12→P19 — bugfix luồng BOM↔Báo giá)
Vừa hoàn thành:
- P12: `createFromRequest` copy service items BOM→báo giá (path PricingRequest thiếu).
- P13→P14: chốt logic tỷ lệ giá vốn — tự lập khoá giá vốn (tính từ rate ERP); từ BOM nhập cả giá vốn+giá bán, PM tính tỷ lệ + ghi `rate_value_capital` về ERP khi lưu (`syncServiceCostRatesToErp`).
- P15: hiển thị tỷ giá + ngày tạo báo giá (edit toolbar + view cell Loại tiền tệ).
- P16: fix validate giá dịch vụ false-positive (bỏ check `unit_id` + bỏ bắt buộc giá vốn>0; giữ giá bán>0).
- P17→P18: validate con không trùng mã CHA trực tiếp (so theo `erp_product_id`, KHÔNG chặn hàng tạm theo code); dedupe mã hàng tạm khi gộp BOM (`dedupeTempGoodsCodes`).
- P19: khoá sửa mã hàng tạm ở màn edit báo giá (BOM đã khoá sẵn).
Đang làm dở: (không)
Bước tiếp theo: user hard-refresh E2E test toàn bộ P12→P19 (đặc biệt: tạo báo giá từ BOM kế thừa dịch vụ + tính/ghi rate về ERP, gộp BOM trùng mã, thêm con trùng mã).
Blocked:

### Checkpoint — 2026-06-04 (Phase P6→P11 — bugfix + tinh chỉnh Báo giá)
Vừa hoàn thành:
- P6: hàng tạm cấp con thêm nút Sửa; `QuotationProductEditModal` TSKT dùng `CompactReviewEditor`.
- P7: tách 2 cột CK — "CK phân bổ tự động" (read-only, FE largest-remainder) + "Phân bổ CK" (input lưu DB); nút Phân bổ tự động confirm ghi đè (`applyAutoAllocation`, bỏ round-trip BE); áp dụng edit + view.
- P8: fix lưu hàng tạm cha-con (FE gửi `temp_id`/`parent_temp_id`; BE 2-pass `saveDirectProduct` resolve parent_id; rule request).
- P9: header icon info tooltip; input Phân bổ CK disabled khi chưa có CK tổng; VAT hàng hoá căn giữa (`::v-deep`); Tỷ suất LN dịch vụ "—" khi chưa có giá (`svcMarginPercent`).
- P10: button "Tạo nhóm"→"Thêm nhóm" chuyển vào header section A của BOM (đồng nhất Quotation).
- P11: dịch vụ ERP giá vốn tính ngược từ giá bán theo `rate_value_capital`; khoá ô giá vốn; badge "Tỷ lệ giá vốn: X%" ở tên (edit + view); BE resource trả thêm rate.
Đang làm dở: (không)
Bước tiếp theo: user hard-refresh E2E test toàn bộ P6→P11.
Blocked:

### Checkpoint — 2026-06-04 (Phase P6 — bugfix hàng tạm Báo giá tự xây dựng)
Vừa hoàn thành: P6.1 thêm button "Sửa" cho hàng tạm cấp con (edit.vue, cell tên hàng con); P6.2 thay textarea Thông số kỹ thuật trong `QuotationProductEditModal.vue` bằng `CompactReviewEditor` (đồng nhất form Thêm hàng tạm).
Đang làm dở: (không)
Bước tiếp theo: User hard-refresh test sửa hàng tạm cha (editor TSKT hiển thị nội dung cũ) + sửa hàng tạm con.
Blocked:

### Checkpoint — 2026-06-04 (Phase P5 — đồng nhất UX BOM↔Báo giá + bỏ giá BOM + fix gộp BOM)
Vừa hoàn thành P5.1 → P5.20:
- Đồng nhất Dịch vụ/Chi phí: drag-thả reorder (BOM + Báo giá hàng hoá/dịch vụ), quick-create tách popup (ẩn tab), bỏ select nhóm ở tab dịch vụ.
- 2 phần A — Hàng hoá / B — Dịch vụ & Chi phí khác (header xanh, tổng theo cột) ở cả tạo/sửa/xem (BOM + Báo giá).
- BOM bỏ TOÀN BỘ cột giá (giá nhập ở Báo giá); popup tạo nhanh BOM chỉ Loại + Tên.
- Báo giá: cột Thao tác đầu (direct), thêm 4 cột Model/Thương hiệu/Xuất xứ/TSKT + nút Ẩn/Hiện (mặc định hiện).
- Icon phân biệt Dịch vụ (xanh) / Chi phí khác (cam) theo revenue_calculation (BE 2 resource trả thêm field).
- Bỏ nền row item (chỉ giữ group + header A/B); BOM cột SL căn giữa đồng nhất.
- Fix: đổi loại BOM clear serviceItems; popup không tự đóng khi focus input number (@keydown/@click/@mousedown.stop); **gộp BOM nay gộp cả service_items của BOM con (trước bị mất)**.
Đang làm dở: Không.
Bước tiếp: User hard-refresh test toàn bộ E2E (đặc biệt gộp BOM có dịch vụ, reorder, ẩn/hiện cột). Chờ user chốt: BOM aggregate có cho thêm dịch vụ thủ công (nút B) không.
Blocked: Không.

### Checkpoint — 2026-06-03 (Phase P3 — fix section dịch vụ BOM vô hình)
Vừa hoàn thành: Fix bug "Form tạo/sửa BOM không hiện nhóm Dịch vụ & Chi phí khác + chọn dịch vụ báo thành công nhưng không hiển thị".
- **Root cause**: section "Dịch vụ & Chi phí khác" trong `BomBuilderEditor.vue` bị đặt NGOÀI `.container-fluid` (cha là `.v2-styles ... d-flex justify-content-center`) → render nhưng thành flex-item bị ép sát cạnh container → vô hình. Đúng triệu chứng: cảnh báo `bsvc-5` (DOM đã render) nhưng mắt không thấy; console sạch (không lỗi JS).
- **Fix**: di chuyển thẻ `</div>` đóng `.container-fluid` xuống sau section (gỡ `</div>` ngay sau `<BomBuilderTableCard />`, thêm `</div>` trước `<BomBuilderFooterBar>`). Section giờ nằm trong luồng container → hiển thị dưới bảng hàng hoá. Compile-check: TPL OK.
- Logic thêm dịch vụ vào `serviceItems` đã đúng từ trước (chỉ bị layout che).
Đang làm dở: Không.
Bước tiếp: User hard-refresh xác nhận section hiển thị + chọn dịch vụ hiện trong section (P3.V); chạy nốt verify E2E Phase V & F4.6 & F6.4.

### Checkpoint — 2026-06-02 (Phase F4 — hợp nhất popup done)
Vừa hoàn thành: F4.1–F4.5 (BOM + Quotation).
- Tách `CostCatalogPanel.vue` (panel inline); `CostPickerModal` rút gọn bọc panel.
- `BomBuilderAddProductModal`: 2 tab (Hàng hoá: ERP list + "Thêm hàng tạm" overlay / Dịch vụ & Chi phí: CostCatalogPanel). Prop `serviceOnly` ẩn tab Hàng hoá. Bỏ radio + popup lồng.
- BOM `BomBuilderTableCard`: nút → "Thêm mới".
- Quotation `edit.vue`: 1 nút "Thêm mới" (serviceOnly khi từ BOM); `onAddProductApply` route dịch vụ → serviceItems (giá inline); bỏ modal nhập giá DV.
Đang làm dở: Chưa build/E2E.
Bước tiếp: dev server test toàn bộ (F4.6 + Phase V). Verify openEditRow giữ costId. Test store() ghi costs ERP.

### Checkpoint — 2026-06-02 (code BE+FE done)
Vừa hoàn thành: Toàn bộ Phase B (BE) + Phase F (FE).
- BE: TpCost/TpCompanyCost, ErpCostController (index+store) + ErpCostStoreRequest + routes, migration cost_id (đã chạy), Quotation (request+service+controller+resource) nhận cost_id + ép qty=1 + vat fallback, BOM (request+service+resource) nhận cost_id + ép qty_needed=1. Lint sạch.
- FE: CostPickerModal + CostQuickCreateModal (mới), tích hợp Quotation edit.vue (modal "Thêm dịch vụ" → chọn danh mục, bỏ ĐVT, SL=1) + BOM BomBuilderAddProductModal/Editor (nhánh service chọn danh mục, cost_id qua payload, SL=1).
Đang làm dở: Chưa chạy build/E2E.
Bước tiếp theo: Chạy dev server test E2E (search, tạo nhanh DV/chi phí, thêm DV vào báo giá + BOM, backward-compat). Verify `openEditRow` giữ costId. Test `store()` ghi `costs` ERP thật.
Blocked: Không.
Lưu ý: `bỏ chiết khấu` khỏi tạo nhanh (không có mapping company HRM→ERP); `route:list` lỗi toàn cục do module Decision (pre-existing).
