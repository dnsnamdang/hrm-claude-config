# Plan: Bomlist - Quotation

## Trạng thái
- Bắt đầu: 2026-03-28
- Tiến độ: Phase 1-6 done

## Danh sách task

### Phase 1: Màn danh sách BOM List + Status + Delete
[x] Task 1-10: Hoàn thành

### Phase 1.5: Bổ sung trường mới + Permission + Filter
[x] Task 11-20: Hoàn thành

### Phase 2: Refactor logic lưu sản phẩm BOM
[x] Hoàn thành

### Phase 3: Xuất Excel
[x] Hoàn thành

### Phase 4: Import Excel
[x] Hoàn thành

### Phase 5: Trang chi tiết (view-only)
[x] Trang detail _id/index.vue — reuse BomBuilderEditor viewOnly
[x] Ẩn tất cả buttons thêm/sửa/xoá/kéo thả
[x] Editable fields → text thuần
[x] Fix sticky columns khi ẩn cột Thao tác
[x] Header card: người tạo + thời gian
[x] Footer bar fixed: button Sửa + Xuất Excel
[x] STT cấp con: lùi đầu dòng, font-weight normal
[x] Button Import chỉ hiện loại BOM Thành phần

### Phase 6: Test toàn bộ BOM List ✓

#### 6.1 Màn danh sách
[x] Truy cập /assign/bom-list — hiện danh sách đúng
[x] Quick search theo Mã BOM, Tên BOM
[x] Filter cascading: chọn Dự án → tự select Giải pháp → enable Hạng mục
[x] Filter: Công ty, Phòng ban, Bộ phận, Người tạo, Trạng thái, Loại BOM, Ngày tạo
[x] Phân quyền: user chỉ thấy BOM theo quyền (tất cả / công ty / phòng ban / bộ phận)
[x] BOM Đang tạo chỉ hiện cho người tạo
[x] Column customization: tuỳ chỉnh cột hiển thị
[x] Pagination + sorting (ngày tạo, ngày cập nhật)

#### 6.2 Tạo BOM List
[x] Tạo BOM loại Thành phần — Lưu nháp (status=1)
[x] Tạo BOM loại Thành phần — Lưu (status=2)
[x] Tạo BOM loại Tổng hợp — chọn BL con
[x] Chọn Dự án → tự fill Giải pháp + Khách hàng
[x] Thêm nhanh hàng hoá cha → thêm lần 2 không trùng code
[x] Thêm nhanh hàng hoá con cho cha vừa tạo local
[x] Chọn hàng hoá từ danh mục (PickModal) → copy data sang bom_list_products
[x] Sửa hàng hoá trong BOM → KHÔNG thay đổi product_projects
[x] Xoá hàng hoá cha/con
[x] Kéo thả đổi thứ tự cha/con

#### 6.3 Sửa BOM List
[x] Mở edit BOM Đang tạo — hiện cả Lưu nháp + Lưu
[x] Mở edit BOM Hoàn thành — chỉ hiện Lưu (ẩn Lưu nháp)
[x] BOM Chờ duyệt/Đã duyệt — form disabled, không sửa được
[x] Sửa thông tin header (tên, ghi chú, loại BOM)
[x] Sửa sản phẩm → save → reload đúng data

#### 6.4 Xoá BOM List
[x] Xoá BOM Đang tạo (status=1) + created_by = user → thành công
[x] Xoá BOM Hoàn thành (status=2) → không cho xoá
[x] Xoá BOM của người khác → không cho xoá
[x] Confirm modal hiện đúng thông tin

#### 6.5 Xuất Excel
[x] Click icon xuất Excel trên row → hiện popup chọn cột
[x] Chọn/bỏ chọn cột → Select all/deselect all
[x] Checkbox xuất cấp con: bật → có hàng con, tắt → chỉ hàng cha
[x] File Excel: header thông tin BOM đúng (tên, dự án, giải pháp, hạng mục, KH)
[x] File Excel: font Times New Roman, auto-fit, số tiền format #,##0
[x] File Excel: hàng cha bold background xanh, hàng con indent
[x] Xuất từ trang chi tiết (footer bar) → hoạt động đúng

#### 6.6 Import Excel
[x] Download template mẫu → file mở được, có header + dòng mẫu cha/con
[x] Import file mẫu → preview đúng 2 dòng (cha + con)
[x] Validate: thiếu tên → lỗi, thiếu model/brand/origin/uom/qty → lỗi
[x] Validate: hàng cha thành tiền ≠ tổng con → cảnh báo
[x] Import thành công → sản phẩm thêm vào BOM, reload đúng
[x] Model/Brand/Origin/Unit chưa có trong DB → tự tạo mới
[x] Mã hàng hoá không nhập → tự sinh
[x] Phân biệt cha/con qua STT (1=cha, 1.1=con) → parent_id đúng
[x] Button Import chỉ hiện ở loại BOM Thành phần

#### 6.7 Trang chi tiết (view-only)
[x] Truy cập /assign/bom-list/{id} → hiện readonly
[x] Không có buttons: Chọn hàng hoá, Import, Thêm nhanh, Sửa, Xoá, kéo thả
[x] Không có cột Thao tác, không lệch layout
[x] Editable fields hiện text thuần (qty, price, specification)
[x] STT cấp con lùi đầu dòng, font-weight normal
[x] Header card: hiện người tạo + thời gian
[x] Footer bar fixed: button Sửa → navigate edit, button Xuất Excel → show modal
[x] Bộ lọc header disable toàn bộ input/select

### Phase 7: Cập nhật theo yêu cầu khách hàng

#### 7.1 Popup "Thêm hàng hoá" gộp (thay PickModal + QuickCreateModal)
[x] Tạo BomBuilderAddProductModal.vue — 2 tab (Tìm có sẵn + Tạo mới)
[x] Tab 1: Search hàng ERP (erp2326.products) + hàng BOM hiện tại
[x] Tab 1: Filter theo Model, Thương hiệu, Xuất xứ
[x] Tab 1: Multi-select checkbox + nhập số lượng + badge nguồn (ERP/BOM)
[x] Tab 2: Form tạo mới dùng V2Base components (giữ style cũ)
[x] Tab 2: Validate từng field (Tên, Model, ĐVT, Thương hiệu, Xuất xứ) — hiện lỗi tại element
[x] Tab 2: Chọn nhóm hàng khi có groups
[x] API endpoint GET /erp-products — search products từ ERP
[x] API endpoint GET /{bomList}/bom-products — search products trong BOM
[x] Model TpProduct + TpProductUnit (mysql2 connection)
[x] Xoá BomBuilderPickModal.vue + BomBuilderQuickCreateModal.vue
[x] Load model options từ API (get-model)

#### 7.2 Cấp nhóm hàng (Grouping)
[x] Tạo bảng bom_list_groups (migration)
[x] Thêm bom_list_group_id vào bom_list_products (migration)
[x] Entity BomListGroup + relationships
[x] Button "Tạo nhóm" ở header → mở b-modal (không dùng prompt trình duyệt)
[x] Sửa nhóm → b-modal centered
[x] Xoá nhóm → BaseConfirmModal xác nhận
[x] Row nhóm hiển thị STT La Mã (I, II, III)
[x] STT hàng cha reset mỗi nhóm
[x] Button "Thêm hàng hoá" nằm trực tiếp trên row nhóm
[x] Mỗi nhóm expand/collapse (mũi tên + v-show)
[x] Hiển thị số lượng hàng mỗi nhóm
[x] Service syncGroups() + loadDetail() eager load groups
[x] Save payload: bom_groups[] + group_id per product

#### 7.3 Validate BOM tổng hợp
[x] Unique: 1 solution + module chỉ 1 BOM tổng hợp
[x] validateUniqueAggregate() trong BomListService
[x] Controller trả lỗi 422 nếu trùng
[x] SubBomModal: filter theo solution/module, exclude status nháp

#### 7.4 Đồng bộ hàng ERP
[x] Thêm erp_product_id vào bom_list_products (migration)
[x] syncErpFields() — re-fetch ERP data khi lưu BOM
[x] Mapping: name, code, model_id, brand_id, origin_id, product_attributes, unit_id

#### 7.5 Sửa lỗi / cải thiện
[x] Fix cột column_customizations thiếu bom_lists (migration)
[x] Fix API route 404 — đổi $axios sang $store.dispatch('apiGetMethod')
[x] Fix checkbox chọn hàng không reactive (bỏ computed copy, dùng mảng gốc)
[x] Đổi tên cột "Đặc điểm" → "Thông số kỹ thuật"
[x] Fix group modal lệch layout → dùng b-modal centered

#### 7.6 Test
[ ] Test tạo BOM với groups + hàng ERP + hàng tạo mới
[ ] Test edit BOM — groups + products load đúng
[ ] Test validate BOM tổng hợp unique
[ ] Test SubBom modal filter
[ ] Test expand/collapse nhóm
[ ] Test trang chi tiết view-only

### Phase 8a: Status workflow + Currency + Columns + Service (2026-04-10)

#### 8a.1 Migrations + Entities
[x] Task 1: Migration currency_id vào bom_lists (có backfill VND)
[x] Task 2: Migration product_type vào bom_list_products
[x] Task 3: Migration update status comment bom_lists
[x] Task 4: Model TpCurrency (mysql2 connection)
[x] Task 5: BomList constants STATUS_DA_DUOC_TONG_HOP=5, STATUS_KHONG_DUYET=6 + relationship currency()
[x] Task 6: BomListProduct constants PRODUCT_TYPE_* + accessors import_total/sale_total/profit_margin

#### 8a.2 Services
[x] Task 7: BomListService::syncChildStatus() + integrate vào store/update/destroy
[x] Task 8: BomListService::syncStatusFromSubmission() (nhận profile, dùng bomLists() many-to-many)
[x] Task 9: Hook SolutionService::storeSolutionReviewProfile + reviewSolutionProfileDecision
[x] Task 10: Hook SolutionModuleService::storeReviewProfile + reviewModuleProfileDecision
[x] Task 11: BomListService handle currency_id + validate dịch vụ (không có con) + mapProductPayload thêm product_type
[x] Task 11b (phát sinh): Fix edit BOM ở status KHONG_DUYET → auto reset về HOAN_THANH

#### 8a.3 Controller / Request / Transformer
[x] Task 12: Controller getCurrencies() endpoint + route /currencies
[x] Task 13: BomListStoreRequest thêm rules currency_id + product_type conditional
[x] Task 14: DetailBomListResource append currency object + import_total/sale_total/profit_margin
[x] Task 14b: BomListService::loadDetail eager load currency

#### 8a.4 Excel
[x] Task 15: BomListExport blade thêm row "Loại tiền tệ" + 3 cột mới (Loại, Thành tiền nhập, Tỷ suất LN) + ẩn Model/Brand/Origin khi dịch vụ
[x] Task 15b: moneyFields thêm import_amount, dataStartRow 9→10
[x] Task 16: BomListController::importTemplate thêm cột "Loại" + dòng mẫu dịch vụ
[x] Task 16b: BomListService::validateImportData parse product_type từ text/int + bỏ validate model/brand/origin khi dịch vụ

#### 8a.5 Frontend — Core
[x] Task 17: BomBuilderEditor load currencies + currency_id trong bomForm + save payload + mapProductToRow/mapGroupRowForSave thêm productType/product_type + computed currentCurrencySymbol + visibleColumns/columnOptions thêm importAmount + profitMargin
[x] Task 18: BomBuilderInfoCard prop currencyOptions + select Currency + emit change-currency + handler onChangeCurrency ở Editor (có confirm modal)
[x] Task 19: BomBuilderTableCard prop currencySymbol + 4 cột mới + icon hàng/dịch vụ trong parent row + format tỷ suất có màu (đỏ<10%, vàng 10-20%, xanh>20%)

#### 8a.6 Frontend — Modals
[x] Task 20: BomBuilderAddProductModal Tab 2 radio Hàng/Dịch vụ + conditional Model/Brand/Origin + createProduct() validate có điều kiện + onProductTypeChange clear fields + Tab 1 hardcode product_type=1
[x] Task 21: BomBuilderEditor handleAddProductApply forward productType (Task drag cross-parent SKIP — reorderChildren chỉ trong cùng parent)
[x] Task 22: BomBuilderImportModal cột ProductType + đổi label "Giá nhập/Giá bán" + importRequiredFields giảm + importValidationRules conditional + handleValidateData/handleImportData map `loai`

#### 8a.7 Frontend — Detail + wrap-up
[x] Task 23a: BomExportModal update availableColumns thêm product_type, import_amount, profit_margin + đổi label
[x] Task 23b: Trang chi tiết _id/index.vue tự inherit từ BomBuilderEditor viewOnly (không cần sửa)
[x] Task 24: Update plan.md + STATUS.md
[ ] Task 25: Test thủ công Phase 8a (chờ user)

#### Gap / Follow-up (cần xử lý khi test hoặc phase sau)
[ ] VND backfill: 0/6 rows ở local vì ERP DB local chưa có bảng currencies — verify trên staging/prod

### Phase 8b: Fix gap/follow-up từ Phase 8a (2026-04-11)

[x] Task 26: FE — Ẩn nút "Chọn con" và "Thêm nhanh con" trên parent row khi productType === 2 (Dịch vụ)
  - File: BomBuilderTableCard.vue
  - Chỗ cần sửa: 2 block render (có groups + không groups) ở dòng ~169 và ~312
  - Logic: `<template v-if="(group.parent.productType || 1) !== 2">` bọc 2 button
[x] Task 27: FE — Rebalance layout BomBuilderInfoCard để row sub-bom full width
  - File: BomBuilderInfoCard.vue
  - Hiện tại: Khách hàng(4) + Ghi chú(4) + Loại BOM(4) | Currency(4) + SubBom(8)
  - Mới: Khách hàng(3) + Ghi chú(3) + Loại BOM(3) + Currency(3) | SubBom(12)

#### Test round 1 — Bug từ user (2026-04-11)
[x] Task 28: Fix edit Dịch vụ bị validate như Hàng hoá → không lưu được
  - File: BomBuilderEditor.vue (openEditRow, saveEditRow)
  - openEditRow: thêm `product_type: Number(row.productType) || 1` vào editForm
  - saveEditRow: `isService` check, skip model validation, force null modelId/brandId/originId + clear text fields khi service
  - updatedRow: set `productType` explicitly để tránh mất qua spread
[x] Task 29: EditModal template — layout theo loại
  - Thêm computed `isService`
  - Service: ẩn row Model/Brand/Origin, merge UOM lên row Name/Code: Name(4)+Code(4)+UOM(4)
  - Hàng hoá: giữ layout cũ
  - Title: icon + "Sửa nhanh dịch vụ" vs "Sửa nhanh hàng hoá"
[x] Task 30: AddProductModal Tab 2 — radio → toggle button
  - `b-form-radio-group buttons button-variant="outline-primary" size="sm"`
[x] Task 31: AddProductModal Tab 2 — layout gọn khi service
  - Thêm computed `isService`
  - Service: Name(4)+Code(4)+UOM(4), ẩn row UOM/Model/Brand/Origin
  - Hàng hoá: giữ layout cũ
  - Label động: "Tên dịch vụ" / "Tên hàng hoá"

#### Test round 3 — Bug batch 2 (2026-04-11)
[x] Task 33: Style "Số lượng cần dùng" — thay `<input class="v2-plain-input">` bằng `<V2BaseInput type="number" v-model.number>` trong EditModal + AddProductModal
[x] Task 34: Rich text HTML cho Đặc điểm/Thông số kỹ thuật
  - Modal EditModal + AddProductModal: thay `V2BaseTextarea` bằng `CompactReviewEditor` (CKEditor 5 wrapper), bind qua `:value` + `@input`, `:visible` để mount/unmount theo modal show
  - Table: bỏ inline textarea, hiện `v-html` preview với class `.spec-preview` (click "Sửa" để edit qua modal rich)
[x] Task 35: Strip dấu `'` đầu tên ERP products — BE `searchErpProducts` dùng closure `$stripLeadingQuote` áp cho code, name, model_name, brand_name, origin_name, unit_name
[x] Task 36: Thu nhỏ sticky columns trong BomBuilderTableCard
  - `sticky-col-a` (Thao tác): 110px → 90px, left: 0
  - `sticky-col-b` (STT): 100px → 50px, left: 110→90
  - `sticky-col-c` (Tên hàng): min-width 420px → 260px, left: 210→140
  - View-only: sticky-col-c--vo left: 100→50
  - Giảm các min-width cột khác (Model 150→130, Brand 140→120, UOM 120→100, qty 140→110...)
[x] Task 37: Thêm đơn vị tiền tệ vào header cột giá/thành tiền
  - "Giá nhập ({{ currencySymbol }})", "Thành tiền nhập ({{ currencySymbol }})"
  - "Giá bán ({{ currencySymbol }})", "Thành tiền bán ({{ currencySymbol }})"

#### Test round 4 — Bug batch 3 (2026-04-11)
[x] Task 38: Cột "Thao tác" thu nhỏ nữa — 90px → 70px, cập nhật sticky-col-b left 90→70
[x] Task 39: Cột STT text thuần — bỏ border/background `.order-box`, giữ font-weight, giảm width 50→42px
[x] Task 40: Cột Tên hàng fix width cố định + cho wrap
  - `width: 260px; min-width: 260px; max-width: 260px`
  - `white-space: normal; word-wrap: break-word; overflow-wrap: break-word`
  - Áp cho cả sticky-col-c và sticky-col-c--vo
[x] Task 41: Bỏ button "Thêm nhanh hàng hoá" ở header cột Tên hàng (gộp vào Task 40 khi simplify th)
[x] Task 42: Đổi "Số lượng cần dùng" → "Số lượng", min-width 110→80, update columnOptions label
[x] Task 43: Default currency VNĐ khi tạo BOM mới — match cả 'VND' lẫn 'VNĐ'
  - FE Editor.loadCurrencies: find code/name in ['VND','VNĐ']
  - BE BomListService.getDefaultCurrencyId: whereIn + orderByRaw FIELD
  - BE migration 2026_04_10_100000: whereIn + orderByRaw FIELD
  - Root cause: DB của anh có `code='VNĐ'` với diacritic
[x] Task 44: Bỏ box-shadow ở sticky-col-c

#### Test round 5 — Bug batch 4 (2026-04-11)
[x] Task 45: Expand button `+/-` chỉ hiện khi có cấp con
  - `v-if="group.children && group.children.length"` trên button (cả 2 chỗ render)
[x] Task 46: Gộp "Chọn con" + "Thêm nhanh con" → 1 button "Thêm con"
  - Cả 2 button trước đều trigger mở `BomBuilderAddProductModal` (Phase 7 đã unify modal)
  - Xoá button "Chọn con", rename "Thêm nhanh con" → "Thêm con", giữ event `open-pick`
  - Xoá handler `openAddProductModalAsChild` + listener `@open-quick-child` ở Editor.vue
  - CSS `.inline-actions-under`: `flex-wrap: wrap` → `flex-wrap: nowrap` + `white-space: nowrap`
[x] Task 47: Fix tên hàng tràn cột + widen cột

#### Test round 6 — Bug batch 5 (2026-04-11)
[x] Task 48: Tên hàng font-weight 700 → 300 (`.bom-name` + `.child-name`)
[x] Task 49: Ẩn action buttons mặc định, chỉ hiện khi hover row
  - `.inline-actions-under` `opacity: 0; visibility: hidden` default
  - `.bom-parent-row:hover .inline-actions-under, .bom-child-row:hover .inline-actions-under` opacity: 1
  - `transition: opacity 0.15s` mượt
[x] Task 50: Reorder columns — "Số lượng" sang phải "Thông số kỹ thuật"
  - Header th order: UOM → Thông số → Số lượng → Giá nhập → ...
  - 4 block td (parent grouped/ungrouped, child grouped/ungrouped)
  - columnOptions array trong Editor.vue: swap qty ↔ specification
[x] Task 51: Row TỔNG TIỀN lên đầu + sticky + tổng thêm import
  - Xoá `<tfoot>` cũ
  - Thêm row 2 trong `<thead>` v-if visible amount||importAmount
  - Render th theo từng visibleColumn, fill total vào cột importAmount + amount
  - CSS `.bom-table thead tr:first-child th { top: 0 }` cho row header
  - CSS `.bom-table thead tr.bom-total-row th { top: 34px; background: #fff7ed }` cho row total
  - CSS cho sticky col trong total row: top 34 + left X kép
  - Thêm computed `totalImport` (sum estimatedPrice * qty cho mọi row)
[x] Task 52: Bỏ icon hàng hoá, chỉ giữ icon dịch vụ
  - `v-if="(productType || 1) === 2"` — chỉ render khi service
  - 2 chỗ render (grouped + ungrouped)

#### Test round 7 — Fix save BOM (2026-04-11)
[x] Task 53: Bug groups không lưu — mismatch key giữa bomGroups.id vs products.group_id
  - Root cause: FE format group_id = `'g_<id>'` nhưng dùng `.id || .client_id` nhiều chỗ → mixed format ('g_5' vs 5)
  - BE `syncGroups` map cả 3 key: client_id, id integer, 'g_<id>' — tolerate mọi format từ FE
  - FE fix 3 chỗ dùng `.id || .client_id`:
    - `recalculateDisplayNumbers`: `g.client_id || ('g_' + g.id)`
    - `confirmRemoveGroup`: same
    - `openAddProductModalAsParent`: same
[x] Task 54: Bug apostrophe khi lưu — syncErpFields ghi đè raw ERP name
  - Fix: closure `$stripQuote = ltrim($v, "'")` áp cho name + code trong syncErpFields
[x] Task 55: Bug service đã xoá vẫn lưu — không reproduce được qua code review
  - Đoán nguyên nhân: khi convert hàng hoá → dịch vụ nhưng còn children cũ, BE throw → transaction rollback → data cũ (kể cả service) vẫn còn
  - Fix safety: BE `syncProducts` tự động strip children khi parent là service (thay vì throw) — forgiving behavior

#### Test round 8 — Vẫn không lưu được nhóm + bỏ icon (2026-04-11)
[x] Task 56: Fix các chỗ còn dùng `.id || .client_id` (6 chỗ còn sót)
  - BomBuilderTableCard.vue: button "Thêm hàng hoá" group row (line 128), getGroupProducts filter (line 569), getGroupKey helper (extract từ isGroupExpanded + toggleGroupExpand)
  - BomBuilderAddProductModal.vue: `bomGroupOptions.id` mapping, `watch.show` selectedGroupId default
[x] Task 57: openAddProductModal default target group
  - Khi bấm "Chọn hàng hoá" trên toolbar (không truyền groupId) + đã có groups → auto-assign về group cuối cùng
  - Tránh products orphan không gán vào group nào
[x] Task 58: Thêm group selector vào Tab 1 "Tìm hàng có sẵn"
  - Trước: Tab 1 không có selector → user không biết hàng được thêm vào group nào
  - Sau: hiện dropdown "Nhóm hàng" như Tab 2, rõ ràng UX
[x] Task 59: Bỏ thẻ `<i>` dịch vụ ở đầu tên hàng
  - `.bom-name` chỉ còn `{{ group.parent.name }}` thuần text
[x] Task 60: Thêm Log::debug ở BE syncGroups + syncProducts
  - Trace actual group_id values + groupMap content để debug nếu bug còn
  - Log path: `hrm-api/storage/logs/laravel-<ngày>.log`

#### Test round 11 — UX polish + ERP readonly (2026-04-11)
[x] Task 63: AddProductModal Tab 1 — click row (mã / tên) để toggle checkbox
  - `<td class="clickable-cell" @click="item.selected = !item.selected">` cho 2 cột mã + tên
  - CSS `.clickable-cell` cursor pointer + hover bg
[x] Task 64: AddProductModal Tab 2 — bỏ label "Loại sản phẩm", giảm padding top
  - Bỏ `<V2BaseLabel>Loại sản phẩm</V2BaseLabel>`
  - Thêm class `mt-n2` để đẩy toggle button lên sát top
[x] Task 65: AddProductModal — fixed footer buttons
  - Move buttons ra khỏi `<b-tab>` content → `<div class="modal-footer-fixed">` ngoài
  - Conditional render theo `activeTab` (0 = Tìm sẵn, 1 = Tạo mới)
  - CSS: padding 12/20 + border-top + bg trắng + flex-shrink 0 → sticky bottom
[x] Task 66: Toast message theo loại
  - `BomBuilderEditor.saveEditRow`: `isService ? 'Đã cập nhật dịch vụ.' : 'Đã cập nhật hàng hoá.'`
[x] Task 67: ERP products chỉ cho sửa 3 field: Số lượng, Giá nhập, Giá bán
  - `BomBuilderEditor.openEditRow`: thêm `erpProductId: this.toNullableId(row.erpProductId)` vào editForm
  - `BomBuilderEditModal`: computed `isFromErp = !!editForm.erpProductId`
  - Disabled: Tên, UOM, Model, Brand, Origin, Ghi chú, Đặc điểm (`:disabled="disabled || isFromErp"`)
  - Enabled: Số lượng, Đơn giá dự toán, Đơn giá báo giá
  - Banner `.alert alert-info` ở top khi isFromErp giải thích constraint

#### Test round 10 — Resource không expose groups (2026-04-11)
[x] Task 62: **ROOT CAUSE THẬT** — DetailBomListResource thiếu field `groups` + `bom_list_group_id`
  - Log round 9 confirm: BE save đúng (`groupMap={g_1:10,g_2:11}`, 6 rows với groupIds khớp)
  - Nhưng sau reload, FE vẫn không thấy groups — vì `DetailBomListResource::toArray()` KHÔNG expose:
    - Field `groups` (list bom_list_groups) → `detail.groups = undefined` → FE không load bomGroups
    - Field `products[].bom_list_group_id` → rows có `group_id = null` → không match bomGroup nào
  - Fix: thêm 2 field vào resource
    - `'groups' => $this->groups->map({id, name, sort_order})`
    - Products thêm `bom_list_group_id` + `erp_product_id` (cũng thiếu)
  - Tất cả fix trước (Task 53-61) là cần thiết nhưng không đủ — bug chính là ở resource layer

#### Test round 9 — Orphan rows hidden (2026-04-11)
[x] Task 61: Fix orphan rows bị ẩn khi có groups
  - Root cause thật từ log: user thêm 2 product trước khi tạo nhóm → rows có group_id=null → template filter by group_id → bị ẩn hoàn toàn khi bomGroups > 0
  - User tưởng "nhóm không lưu" nhưng thật ra groups đã lưu + 3/5 rows hiển thị; 2 rows orphan ẩn mất
  - Fix 3 lớp:
    - `saveGroupModal`: khi tạo nhóm, auto-assign orphan rows (group_id null hoặc không match known) về nhóm mới
    - `buildSavePayload`: safety cleanup — mọi orphan row được assign về first group trước khi gửi BE
    - `getGroupProducts(0)`: gộp orphan rows vào group đầu tiên khi render → user luôn thấy mọi row
  - Root cause: `.bom-table td { white-space: nowrap }` có specificity cao hơn `.sticky-col-c`
  - Fix: selector `.bom-table td.sticky-col-c` + `!important` + `word-break: break-word`
  - Width: 260px → 320px
  - Áp rules tương tự cho `.sticky-col-c--vo`
  - Bỏ inline style width trên `<th>` (để CSS class kiểm soát)

#### Test round 2 — Field name bảng currencies (2026-04-11)
[x] Task 32: Fix field `symbol` không tồn tại — thay bằng `code`
  - Cột thực tế: id, code, name, other_name, status, exchange_rate (KHÔNG có symbol)
  - BE: TpCurrency.php fillable (thay symbol → other_name, status, exchange_rate)
  - BE: BomListController::getCurrencies() select (thay symbol → exchange_rate, thêm where status=1)
  - BE: DetailBomListResource currency object (thay symbol → exchange_rate)
  - BE: exports/bom_list.blade.php row "Loại tiền tệ" (symbol → code, default "VNĐ (VND)")
  - FE: BomBuilderInfoCard currencySelectOptions label (c.symbol → c.code, format "CODE - Name")
  - FE: BomBuilderEditor currentCurrencySymbol (c.symbol → c.code, default "VND")
  - FE: BomBuilderTableCard prop currencySymbol default ('₫' → 'VND')

### Phase 9: Làm giá + Phê duyệt giá BOM (2026-04-12)

**Scope:** Chỉ áp dụng cho BOM tổng hợp cấp giải pháp. Flow: Đã duyệt → Yêu cầu XD giá → Làm giá → Tính cấp duyệt → Duyệt/Từ chối.

#### 9.1 Backend — Status + Entity + Migration ✓
[x] Task 1: Thêm 5 status mới vào BomList entity
  - STATUS_CHO_XAY_DUNG_GIA = 7 (Chờ xây dựng giá, #FF9800)
  - STATUS_DANG_XAY_DUNG_GIA = 8 (Đang xây dựng giá, #03A9F4)
  - STATUS_CHO_TP_DUYET_GIA = 9 (Chờ TP duyệt giá, #673AB7)
  - STATUS_CHO_BGD_DUYET_GIA = 10 (Chờ BGĐ duyệt giá, #E91E63)
  - STATUS_DA_DUYET_GIA = 11 (Đã duyệt giá, #009688)
[x] Task 2: Migration tạo table `bom_price_approval_configs`
  - id, type (enum: order_value/profit_margin), level (1/2/3)
  - min_value (decimal 15,2 nullable), max_value (decimal 15,2 nullable)
  - description, updated_by, timestamps
[x] Task 3: Migration tạo table `bom_price_approval_config_logs` (audit)
  - id, config_id (FK), old_value (json), new_value (json), changed_by, created_at
[x] Task 4: Migration thêm cột vào bom_lists
  - price_approved_by (bigint nullable) — người duyệt giá
  - price_approved_at (timestamp nullable) — thời gian duyệt
  - price_rejected_reason (text nullable) — lý do từ chối
  - price_approval_level (tinyint nullable) — cấp duyệt (1/2/3)
  - price_requested_by (bigint nullable) — PM yêu cầu XD giá
  - price_requested_at (timestamp nullable) — thời gian yêu cầu
[x] Task 5: Tạo Entity BomPriceApprovalConfig + BomPriceApprovalConfigLog
[x] Task 6: Seeder dữ liệu mặc định cho bom_price_approval_configs (6 rows)
  - order_value: level 1 (0 → 1B), level 2 (1B → 20B), level 3 (20B → null)
  - profit_margin: level 1 (20 → null), level 2 (10 → 20), level 3 (0 → 10)

#### 9.2 Backend — Permissions ✓
[x] Task 7: Seeder thêm 3 permissions mới (migration 2026_04_12_200003)
  - `Xây dựng giá Bom giải pháp` (assign.bom-list.build-price)
  - `Trưởng phòng duyệt giá Bom giải pháp` (assign.bom-list.approve-price-tp)
  - `Ban giám đốc duyệt giá Bom giải pháp` (assign.bom-list.approve-price-bgd)

#### 9.3 Backend — Config CRUD API ✓
[x] Task 8: BomPriceApprovalConfigController — index, update
  - GET /api/v1/assign/bom-price-approval-configs → danh sách config (6 rows)
  - PUT /api/v1/assign/bom-price-approval-configs/{id} → cập nhật ngưỡng
  - Mỗi lần update → ghi audit log (old vs new)
[x] Task 9: BomPriceApprovalConfigController — logs
  - GET /api/v1/assign/bom-price-approval-configs/logs → timeline audit

#### 9.4 Backend — Pricing workflow API ✓
[x] Task 10: API yêu cầu xây dựng giá
  - POST /api/v1/assign/bom-lists/{id}/request-pricing
  - Validate: BOM tổng hợp cấp GP, status = 4 (Đã duyệt)
  - Update: status → 7, price_requested_by, price_requested_at
  - Gửi notification (database channel) cho users có quyền `build-price`
[x] Task 11: API lưu nháp giá
  - PUT /api/v1/assign/bom-lists/{id}/save-pricing-draft
  - Validate: status IN (7, 8), user có quyền `build-price`
  - Update products: estimated_price, quoted_price
  - Update BOM: status → 8
[x] Task 12: API gửi duyệt giá
  - POST /api/v1/assign/bom-lists/{id}/submit-pricing
  - Validate: status IN (7, 8), user có quyền `build-price`
  - Tính V (tổng thành tiền bán), M (tỷ suất LN tổng)
  - Lookup config → Level_V, Level_M → Final = MAX(Level_V, Level_M)
  - Nếu cấp 1 → return response {level: 1, can_self_approve: true}
  - Nếu cấp 2 → status → 9, notify users quyền TP, return {level: 2}
  - Nếu cấp 3 → status → 10, notify users quyền BGĐ, return {level: 3}
[x] Task 13: API tự duyệt giá (cấp 1)
  - POST /api/v1/assign/bom-lists/{id}/self-approve-pricing
  - Validate: vừa submit-pricing trả về level 1
  - Update: status → 11, price_approved_by, price_approved_at, price_approval_level = 1
[x] Task 14: API duyệt giá (TP/BGĐ)
  - POST /api/v1/assign/bom-lists/{id}/approve-pricing
  - Validate: status IN (9, 10), user có quyền tương ứng
  - Update: status → 11, price_approved_by, price_approved_at, price_approval_level
  - Notify người làm giá (price_requested_by hoặc người submit)
[x] Task 15: API từ chối giá
  - POST /api/v1/assign/bom-lists/{id}/reject-pricing
  - Validate: status IN (9, 10), user có quyền tương ứng, reason required
  - Update: status → 8, price_rejected_reason
  - Notify người làm giá

#### 9.5 Backend — Notification ✓
[x] Task 16: Notification tích hợp trong BomListService (dùng EmployeeInfoService::sendToAllNotification)
  - Type: request_pricing / submit_pricing / approve_pricing / reject_pricing
  - Data: bom_id, bom_code, bom_name, message, link
  - Gửi cho đúng users theo permission

#### 9.6 Frontend — Cấu hình duyệt giá ✓
[x] Task 17: Tạo page `/assign/settings/price-approval`
  - 2 section: "Theo giá trị đơn hàng" + "Theo tỷ suất lợi nhuận"
  - Mỗi section: bảng 3 row (cấp 1/2/3), cột: Cấp | Từ | Đến | Người duyệt
  - Input editable cho Từ/Đến, button "Lưu cấu hình"
  - Section audit log timeline bên dưới
[x] Task 18: Thêm menu item trong Cấu hình chung + Phê duyệt sidebar
  - "Cấu hình duyệt giá" dưới nhóm Cấu hình

#### 9.7 Frontend — Màn làm giá (pricing screen) ✓
[x] Task 19: Tạo page `/assign/bom-list/:id/pricing`
  - Reuse BomBuilderEditor ở mode mới: `pricingMode`
  - Tất cả cột readonly NGOẠI TRỪ: Giá nhập (estimated_price), Giá bán (quoted_price)
  - Footer hiển thị: Tổng giá nhập | Tổng giá bán | Tỷ suất LN tổng (%) | Cấp duyệt dự kiến (realtime)
[x] Task 20: BomBuilderEditor — thêm prop `pricingMode`
  - Khi pricingMode=true: disable drag, disable add/delete row, disable edit tất cả trừ giá
  - Chỉ cho edit estimated_price + quoted_price
  - Tính realtime: import_total, sale_total, profit_margin per row
[x] Task 21: Footer bar pricing + computed pricingTotalImport/Sale/Margin
  - Buttons: "Lưu nháp" | "Gửi duyệt"
  - Hiển thị tổng + cấp duyệt dự kiến (call API tính level mà không submit)

#### 9.8 Frontend — Popup flows ✓
[x] Task 22: Popup "Gửi duyệt" — cấp 1 (tự duyệt)
  - Message: "Theo quy chế, bạn có thể tự duyệt báo giá này"
  - Buttons: "Xác nhận duyệt" | "Huỷ"
  - Xác nhận → call self-approve API → toast success
[x] Task 23: Popup "Gửi duyệt" — cấp 2/3
  - Message: "Theo quy chế, báo giá này cần gửi tới [Trưởng phòng/Ban giám đốc] duyệt"
  - Buttons: "Xác nhận gửi" | "Huỷ"
  - Xác nhận → submit-pricing đã chuyển status → toast + redirect
[x] Task 24: Popup "Từ chối" — sẽ nằm ở màn pending-price-approval
  - Textarea bắt buộc: "Lý do từ chối"
  - Buttons: "Xác nhận từ chối" | "Huỷ"

#### 9.9 Frontend — Màn danh sách BOM chờ XD giá ✓
[x] Task 25: Tạo page `/assign/bom-list/pending-pricing`
  - Filter: status = 7 (Chờ xây dựng giá)
  - Permission: `Xây dựng giá Bom giải pháp`
  - Reuse pattern V2BaseDataTable
  - Cột: STT | Mã BOM | Tên BOM | Dự án | Giải pháp | Khách hàng | Người yêu cầu | Ngày yêu cầu | Trạng thái
  - Click row → redirect `/assign/bom-list/:id/pricing`
[x] Task 26: Thêm menu "BOM chờ xây dựng giá" vào group Phê duyệt (menu-sidebar.js)
  - isShow: ['Xây dựng giá Bom giải pháp']

#### 9.10 Frontend — Màn danh sách BOM chờ duyệt giá ✓
[x] Task 27: Tạo page `/assign/bom-list/pending-price-approval`
  - Quyền TP → thấy status = 9
  - Quyền BGĐ → thấy status = 9 + 10
  - Cột: STT | Mã BOM | Tên BOM | Dự án | Giải pháp | Khách hàng | Tổng giá bán | Tỷ suất LN | Cấp duyệt | Người gửi | Ngày gửi | Trạng thái
  - Click row → màn review giá (readonly BomBuilderEditor) + buttons Duyệt / Từ chối
[x] Task 28: Thêm menu "BOM chờ duyệt giá" vào group Phê duyệt (menu-sidebar.js)
  - isShow: ['Trưởng phòng duyệt giá Bom giải pháp', 'Ban giám đốc duyệt giá Bom giải pháp']

#### 9.11 Frontend — Button + Status updates trang hiện tại ✓
[x] Task 29: Trang danh sách BOM (index.vue) — thêm 11 status vào filter options
[x] Task 30: Trang chi tiết BOM (_id/index.vue) — button "Yêu cầu xây dựng giá"
  - Chỉ hiện khi: BOM tổng hợp cấp GP + status = 4 + user là PM
  - Click → call request-pricing API → toast + redirect
[x] Task 31: BomBuilderEditor — emit bom-loaded event cho parent page

#### 9.12 Frontend — Notification bell ✓
[x] Task 32: Notification tích hợp sẵn qua EmployeeInfoService (Redis publish + database channel)
  - Hiển thị notification trong bell icon (đã có sẵn)
  - Click notification → redirect tới màn pricing hoặc review tương ứng

#### 9.13 Bugfix + Polish từ test (2026-04-12 ~ 2026-04-13)
[x] Task 33: Fix Vue 2 optional chaining (?.) trong templates
[x] Task 34: Fix buildQueryString import path (@/utils/helpers → @/utils/url-action)
[x] Task 35: Fix apiPostMethod/apiPutMethod payload key (data → payload)
[x] Task 36: Fix fetchData response format ({data, meta} destructure)
[x] Task 37: Fix pagination keys (page/perPage → current_page/per_page)
[x] Task 38: Fix sort handler params ({key} → {field})
[x] Task 39: Fix Employee relationship (employee_info → info)
[x] Task 40: Fix route ordering (/logs trước /{id})
[x] Task 41: Fix pricingMode — ẩn FooterBar save + disable InfoCard + isReadonly
[x] Task 42: Fix V2BaseDataTable column header (label → title)
[x] Task 43: Fix mapProductToRow thiếu dbId → getPricingProducts trả rỗng
[x] Task 44: Fix redirect sau lưu nháp → pending-pricing
[x] Task 45: Fix cấp duyệt dự kiến realtime (load configs + computed)
[x] Task 46: Fix gửi duyệt — tách calculate trước, confirm sau, submit cuối
[x] Task 47: Thêm 4 cột mới (Phòng GP, PM, Phòng KD, NV KD) + eager load relationships
[x] Task 48: Rewrite 2 list pages theo đúng pattern BOM index (V2BaseTitleSubInfo, V2BaseCodeTitle, row-actions hover)
[x] Task 49: Thêm filters cascading (Dự án→GP, Khách hàng) cho 2 list pages
[x] Task 50: Cấu hình duyệt giá — V2BaseCurrencyInput cho số tiền + validate nối tiếp
[x] Task 51: Cấu hình tỷ suất LN — logic ngược (cao→tự duyệt), "Từ" cấp N editable → "Đến" cấp N+1 auto, cấp 3 min=null (bao gồm âm)
[x] Task 52: Cấu hình — mô tả auto generate từ số liệu Từ/Đến
[x] Task 53: Quy đổi VNĐ khi tính cấp duyệt (exchange_rate từ currency BOM)
[x] Task 54: Validate giá nhập/bán > 0 khi gửi duyệt (FE + BE)
[x] Task 55: Row TỔNG TIỀN hiển thị tỷ suất LN tổng (%) + color coding
[x] Task 56: Thu nhỏ cột Model/Thương hiệu/Xuất xứ/ĐVT
[x] Task 57: Chặn sửa BOM khi status != 1,2 (FE redirect + BE throw)
[x] Task 58: Màn show — button Sửa chỉ hiện khi canEditBom + button Quay lại luôn hiện
[x] Task 59: Màn show — button Duyệt giá/Từ chối theo status + permission TP/BGĐ
[x] Task 60: Lịch sử phê duyệt — migration bom_pricing_histories + Entity + API + log tự động 6 methods
[x] Task 61: BomPricingHistoryModal — modal timeline + button ở 3 list pages + trang show
[x] Task 62: Thêm cột Version GP vào 2 màn danh sách chờ duyệt
[x] Task 63: Update validateUniqueAggregate — unique trên cùng version (không phải toàn giải pháp)
[x] Task 64: Xuất Excel cho 2 màn danh sách chờ duyệt (reuse export-list API)
[x] Task 65: Màn BOM chờ XD giá lấy thêm status "Đang xây dựng giá" (8)
[x] Task 66: Button thu gọn card thông tin trên màn làm giá

**Tổng: 66 tasks (32 plan + 34 bugfix/polish)**

## Checkpoint
- 2026-03-28: Phase 1 done
- 2026-03-29: Phase 1.5 + 2 done
- 2026-03-29: Phase 3 + 4 done
- 2026-03-30: Phase 5 done
- 2026-04-08: Phase 6 done — test passed

### Checkpoint — 2026-04-09
Vừa hoàn thành: Phase 7.1–7.5 code done, đã fix 5 vòng bug từ test user
Đang làm dở: Phase 7.6 — test thủ công (chưa hoàn thành, user wrap up)
Bước tiếp theo: Tiếp tục test Phase 7.6 → fix bug nếu có → đánh [x] test cases
Blocked:

### Checkpoint — 2026-04-10
Vừa hoàn thành: Phase 8a code done 24/25 task. Workflow status (5,6), Currency cấp BOM, cột giá (accessors), loại Dịch vụ, Excel import/export đã update. Sync status từ submission qua hook manual trong SolutionService + SolutionModuleService. Fix edit KHONG_DUYET quay về HOAN_THANH.
Đang làm dở: Task 25 test thủ công (chờ user test)
Bước tiếp theo: Test thủ công các scenario (status workflow, currency, dịch vụ, excel), fix bug nếu có
Concerns cần test:
  - Backfill VND 0/6 rows (ERP DB local chưa có currencies) — staging/prod cần verify
  - Drag-drop cross-parent không có, nên chưa có validate "Dịch vụ không có con" khi thêm con qua nút — cần check nút "Thêm nhanh con" và "Chọn con" khi parent là dịch vụ
  - Layout InfoCard row "Chọn BL con" chỉ dùng 8/12 col sau khi thêm currency select
Blocked:

### Checkpoint — 2026-04-11
Vừa hoàn thành: Phase 8b Task 26+27 — fix 2/3 gap/follow-up Phase 8a.
  - Task 26: BomBuilderTableCard ẩn nút "Chọn con"/"Thêm nhanh con" khi parent productType=2 (cả grouped + ungrouped rendering)
  - Task 27: BomBuilderInfoCard rebalance — 4 field (Khách hàng/Ghi chú/Loại BOM/Currency) xuống col-md-3, sub-bom row về col-md-12 full width
Đang làm dở: Không
Bước tiếp theo: Test thủ công Phase 8a + 8b scenario (status workflow, currency, dịch vụ hidden buttons, layout InfoCard)
Blocked: Backfill VND — chờ verify trên staging/prod

### Checkpoint — 2026-04-11 (session test fix bugs)
Vừa hoàn thành: 11 round fix bug batch từ user test (Task 28-67). Các nhóm fix:
  - Round 1 (28-31): Fix edit dịch vụ validate sai + UX thêm sản phẩm (radio→toggle, layout)
  - Round 2 (32): Fix field `symbol` không tồn tại → dùng `code`, fix default VND match cả 'VNĐ'
  - Round 3 (33-37): Style Số lượng, rich text HTML đặc điểm, strip apostrophe ERP, thu nhỏ sticky columns, currency vào header
  - Round 4 (38-44): Thu nhỏ Thao tác/STT/Tên, bỏ button header, fix layout text tràn, bỏ box-shadow
  - Round 5 (45-47): Expand button có con mới hiện, gộp "Chọn con"+"Thêm nhanh con" → "Thêm con", fix wrap tên
  - Round 6 (48-52): Font 300, hover-show buttons, reorder cols (Số lượng sau Thông số), row TỔNG TIỀN sticky, bỏ icon hàng hoá
  - Round 7 (53-55): Fix save BOM — groups key mismatch, apostrophe trong syncErpFields, strip children service
  - Round 8 (56-60): 6 chỗ còn dùng `.id || .client_id`, default target group, Tab 1 group selector
  - Round 9 (61): Orphan rows hidden — auto-assign khi tạo group + safety cleanup + display orphan dưới group đầu
  - Round 10 (62): ROOT CAUSE THẬT — DetailBomListResource thiếu field `groups` + `bom_list_group_id`. User log confirm BE save đúng nhưng resource không expose → FE không thấy. Fix bằng thêm 2 field vào resource
  - Round 11 (63-67): UX polish — click row để check, bỏ label loại sp, fixed footer, toast theo loại, ERP readonly 3 field
  - Cleanup: Xoá 2 Log::debug sau khi user confirm groups đã lưu thành công
  - Round 12 (Excel): fix thiếu tổng tiền nhập + strip_tags thông số kỹ thuật
  - Round 13 (Table): fix z-index header sticky bị non-sticky cells đè + merge STT nhóm + tên nhóm cùng 1 cell
  - Round 14: Button "Xoá trắng BOM" → "Quay lại" navigate về danh sách
  - Round 15: Fix SubBom modal — getAll API thiếu 5 field (bom_list_type, status, project_id, solution_id, module_id) + limit(10) cứng
  - Round 16: Fix gộp BOM mất nhóm — cloneSubBomGroup thiếu group_id + validate currency BOM con cùng BOM tổng hợp
  - Round 17: Import Excel — template thêm cột Nhóm hàng, BE importProducts tạo groups, fix 404 validate/import khi bomId null
  - Round 18: Bỏ validate thành tiền cha≠con, đổi tên cột template (Giá nhập/Giá bán), row con clear nhóm
  - Round 19: Fix import 404, lưu nháp bỏ required groups, validate groups nullable cả status=2
  - Round 20: Fix columnFields crash (Array.isArray check), button Quay lại thay Xoá trắng BOM
  - Round 21: Excel export — rewrite blade hỗ trợ group rows, bỏ nền parent row, width cố định tất cả cột, specification giữ HTML format
Đang làm dở: Không
Bước tiếp theo: Test BOM tổng hợp (gộp nhóm + currency validate) + tiếp tục test Phase 8a+8b
Blocked: Backfill VND trên staging/prod

### Checkpoint — 2026-04-12
Vừa hoàn thành: Round 12-16 fix từ test (Task 68+). Tổng 16 round fix bugs trong 2 ngày test.
  - Excel: tổng tiền nhập + strip HTML tags thông số kỹ thuật
  - Table: z-index specificity fix (0,2,3 vs 0,2,1), merge STT+tên nhóm cùng cell
  - UX: "Xoá trắng BOM" → "Quay lại", click row toggle check, fixed footer, ERP readonly 3 field
  - SubBom: getAll API thiếu 5 field + limit cứng 10 → fix expose fields + dynamic limit
  - Gộp BOM: cloneSubBomGroup thiếu group_id → mất nhóm, thêm validate currency match
Đang làm dở: Không
Bước tiếp theo: Test Excel export + các scenario Phase 8a+8b còn lại
Blocked: Backfill VND trên staging/prod

### Checkpoint — 2026-04-12 (session 2)
Vừa hoàn thành: Round 17-21 fix bugs. Tổng 21 round trong 3 session test.
  - Import: template cột Nhóm hàng, BE tạo groups, fix 404 bomId null, bỏ validate thành tiền, đổi tên cột
  - Save: bỏ required groups cả draft + save, fix columnFields crash trang danh sách
  - UX: button Quay lại thay Xoá trắng BOM
  - Excel export: rewrite blade hỗ trợ group rows (La Mã + nền xanh), bỏ nền parent, width cố định 15 cột, specification giữ HTML format
Đang làm dở: Không
Bước tiếp theo: Test Excel export format + scenario Phase 8a+8b còn lại
Blocked: Backfill VND trên staging/prod

### Checkpoint — 2026-04-12 (session 3)
Vừa hoàn thành: Phase 9 code done — 32/32 tasks. Làm giá + Phê duyệt giá BOM.
  - BE: 5 status mới (7-11), 4 migrations (configs + audit logs + bom_lists columns + permissions)
  - BE: 2 Entity mới (BomPriceApprovalConfig + Log), seeder 6 rows mặc định
  - BE: 3 permissions mới (group='BOM List', type=4)
  - BE: Config CRUD API (index + update + logs)
  - BE: 7 pricing workflow endpoints (request/draft/submit/self-approve/approve/reject/calculate-level)
  - BE: 2 list endpoints (pending-pricing + pending-price-approval)
  - BE: Notification tích hợp qua EmployeeInfoService
  - FE: Màn cấu hình duyệt giá (/assign/settings/price-approval)
  - FE: Màn làm giá (/assign/bom-list/:id/pricing) — pricingMode + popup flows
  - FE: Màn BOM chờ XD giá (/assign/bom-list/pending-pricing)
  - FE: Màn BOM chờ duyệt giá (/assign/bom-list/pending-price-approval) + Duyệt/Từ chối
  - FE: 11 status trong filter, button "Yêu cầu XD giá" trên trang chi tiết
  - Menu sidebar: 3 items mới (Cấu hình duyệt giá + 2 danh sách phê duyệt)
Đang làm dở: Không
Bước tiếp theo: Test toàn bộ flow Phase 9 trên dev
Blocked: Cần gán permissions cho user test

### Checkpoint — 2026-04-13
Vừa hoàn thành: Phase 9 bugfix + polish — 34 tasks bổ sung (Task 33-66). Tổng 66 tasks.
  - Fix hàng loạt bugs FE: Vue 2 template, import paths, store dispatch, response format, column headers
  - Fix BE: Employee relationship, route ordering, config orderBy, getCurrentEmployeeName
  - Cấu hình duyệt giá: V2BaseCurrencyInput format, tỷ suất LN logic ngược, auto-sync boundaries, mô tả auto-generate
  - Màn làm giá: fix lưu giá (dbId thiếu), redirect, cấp duyệt realtime (load configs), gửi duyệt tách calculate→confirm→submit
  - Quy đổi VNĐ khi tính cấp duyệt (exchange_rate), validate giá > 0
  - 2 list pages: rewrite theo pattern BOM index, thêm 4 cột mới + Version GP, cascading filter, xuất Excel
  - Lịch sử phê duyệt: migration + entity + API + log 6 methods + modal timeline + button 3 pages + trang show
  - Màn show BOM: button Duyệt/Từ chối theo status+permission, button Quay lại luôn hiện
  - Chặn sửa BOM status != 1,2 (FE+BE), unique aggregate per version
  - Row TỔNG TIỀN hiển thị tỷ suất LN, thu nhỏ cột Model/Brand/Origin/ĐVT
Đang làm dở: Không
Bước tiếp theo: Test toàn bộ flow Phase 9 end-to-end
Blocked: Không

### Checkpoint — 2026-04-13 (session 2)
Vừa hoàn thành: Tài liệu + Skills migration
  - SRS: docs/srs/bom-list.md — 13 sections, 20 business rules, 28+ API endpoints
  - SRS HTML: docs/srs/bom-list.html — Mermaid diagrams (Use Case, Swimlane, ER, State Machine, Flowchart)
  - Test Cases Excel: docs/srs/BOM_List_TestCases.xlsx — 70 TCs, 9 nhóm, format Step/Thao tác/KQ mong đợi/KQ thực tế/Pass-Fail/Ghi chú
  - Skills migration: .skills/ → .claude/skills/ + thêm YAML frontmatter cho 7 skills + cập nhật CLAUDE.md
Đang làm dở: Không
Bước tiếp theo: Test Phase 9 theo file test cases
Blocked: Không

### Checkpoint — 2026-04-13 (session 3)
Vừa hoàn thành: Phase 10 code done — Duyệt giá 2 bước + Version báo giá + Rà soát logic BOM
  - Duyệt cấp 3 (2 bước): submitPricing cấp 3 → status=9 (TP trước). TP "Duyệt & Chuyển BGĐ" → status=10. BGĐ duyệt → 11 notify NLG+TP. BGĐ từ chối → 8 notify NLG+TP
  - Migration: tp_approved_by/at + pricing_version trên bom_lists, table bom_pricing_snapshots
  - Version báo giá: snapshot giá khi duyệt xong, adjustPricing (11→8 version++), API pricing-versions + pricing-snapshot/{v}
  - FE: popup cấp 3 "2 bước duyệt", button "Duyệt & Chuyển BGĐ" (TP), button "Điều chỉnh giá" (NLG status=11)
  - History: 2 actions mới tp_approve_forward + adjust_pricing
  - Rà soát logic chọn BOM con: filter theo solution_version_id / solution_module_version_id. 3 trường hợp đúng logic
  - BE getAll: thêm filter solution_id/module_id/version_id
  - BomListTable.vue rewrite: popup dạng bảng, checkbox, filter context (solution/module/version)
  - ModuleApprovalModal + SolutionApprovalModal: truyền context version vào BomListTable
Đang làm dở: Không
Bước tiếp theo: Test Phase 10 end-to-end
Blocked: Không
