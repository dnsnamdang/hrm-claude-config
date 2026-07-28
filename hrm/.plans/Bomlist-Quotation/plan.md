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

### Phase 29: Chiết khấu báo giá

> Spec chi tiết: `design-phase29-discount.md`

#### 29.1 — Danh mục loại chiết khấu (CRUD)

- [x] Task 1: Migration `create_discount_types_table`
- [x] Task 2: Model `DiscountType` + Resource (DiscountTypeResource + DetailDiscountTypeResource)
- [x] Task 3: Controller CRUD + lock/unlock + routes (8 endpoints)
- [x] Task 4: FormRequest validation (code unique, name required)
- [x] Task 5: FE — Trang danh sách V2Base `/assign/discount-types`
- [x] Task 6: FE — Modal tạo/sửa loại CK
- [x] Task 7: FE — Thêm menu "Danh mục loại chiết khấu" (sidebar assign)
- [x] Task 7b: Fix — Thêm bộ lọc (người tạo, ngày tạo từ/đến) + Mã tự sinh tăng dần (CK-YYYY-NNNNN)

#### 29.2 — Database + Model cho CK báo giá

- [x] Task 8: Migration `create_quotation_discounts_table`
- [x] Task 9: Migration alter `quotations` (discount_method, total_discount_amount)
- [x] Task 10: Migration alter `quotation_product_prices` (4 cột CK)
- [x] Task 11: Migration alter `quotation_service_items` (4 cột CK)
- [x] Task 12: Model `QuotationDiscount` + relationships
- [x] Task 13: Update Model `Quotation` (relationship quotationDiscounts, constant DISCOUNT_METHOD_*)
- [x] Task 14: Update Model `QuotationProductPrice` (casts, accessors CK)
- [x] Task 15: Update Model `QuotationServiceItem` (casts, accessors CK)

#### 29.3 — BE: Logic tính toán + API

- [x] Task 16: Update `computeTotals()` — tính toán có CK (cả 2 method)
- [x] Task 17: Update `calculateTotals()` — trả thêm total_discount, total_sale_after_discount
- [x] Task 18: Update `upsertPrices()` — lưu discount fields per line
- [x] Task 19: Thêm method `syncQuotationDiscounts()` — CRUD khoản CK tổng
- [x] Task 20: Thêm method `allocateDiscount()` — Largest Remainder phân bổ tự động
- [x] Task 21: Thêm endpoint `POST /quotations/{id}/allocate-discount`
- [x] Task 22: Update `show()` — eager load quotationDiscounts, discount fields
- [x] Task 23: Update `update()` — nhận + xử lý discount data
- [x] Task 24: Update Resource — trả discount fields

#### 29.4 — FE: CK theo mặt hàng (method=1)

- [x] Task 25: Toolbar — radio chọn phương thức CK (cùng hàng VAT đồng loạt)
- [x] Task 26: Confirm khi chuyển method đã có dữ liệu CK
- [x] Task 27: Thêm 3 cột bảng: CK(%), CK(₫), Đơn giá sau CK (ẩn/hiện theo method)
- [x] Task 28: Logic nhập CK%↔CK₫ (nhập 1 tính cái kia, dựa trên input_mode)
- [x] Task 29: Cập nhật computed: lineSaleTotal, lineVatAmount, lineAfterVat (tính trên giá sau CK)
- [x] Task 30: Dịch vụ bổ sung — thêm CK tương tự sản phẩm cha
- [x] Task 31: Validate: CK ≥ 0, CK₫ ≤ Giá bán, Đơn giá sau CK ≥ 0

#### 29.5 — FE: CK theo tổng (method=2)

- [x] Task 32: Section CK tổng dưới bảng sản phẩm (bảng khoản CK + CRUD)
- [x] Task 33: Select loại CK từ danh mục (chỉ status=1) + "Thêm nhanh loại CK"
- [x] Task 34: Toggle % / ₫ cho mỗi khoản CK + tính thành tiền
- [x] Task 35: Thêm 1 cột "CK phân bổ" trên bảng sản phẩm (readonly/editable)
- [x] Task 36: Nút "Phân bổ tự động" — gọi API allocate-discount
- [x] Task 37: Nút "Phân bổ lại" — reset + gọi lại API
- [x] Task 38: Cho phép sửa tay cột "CK phân bổ" + thanh trạng thái realtime
- [x] Task 39: Validate trước submit: Σ(phân bổ) = Tổng CK
- [x] Task 40: Cảnh báo khi sửa giá bán mà đã phân bổ → bắt buộc phân bổ lại

#### 29.6 — Footer tổng + Cấp duyệt

- [x] Task 41: Cập nhật footer: Tổng CK + Tổng bán sau CK (ẩn khi không CK)
- [x] Task 42: Cập nhật Tỷ suất LN tính trên giá sau CK
- [x] Task 43: Cập nhật clientLevelPreview tính trên tổng sau CK
- [x] Task 44: Cập nhật popup gửi duyệt — hiển thị tổng sau CK

#### 29.7 — Export / Import

- [x] Task 45: Export Excel — thêm cột CK theo method (3 cột method=1, 1 cột method=2)
- [x] Task 46: Export Excel — section tóm tắt khoản CK tổng (method=2)
- [x] Task 47: Import Excel — template thêm CK%, CK₫
- [x] Task 48: Import Excel — validate + parse CK (method=1)

#### 29.8 — Lịch sử + Xem báo giá

- [x] Task 49: Ghi log chi tiết khi thay đổi CK (quotation_histories)
- [x] Task 50: Màn xem báo giá (index.vue) — hiển thị CK readonly theo method
- [x] Task 51: Lịch sử báo giá — render action CK (labels, detail per-line)

#### 29.9 — Test thủ công

- [ ] Task 52: Test CRUD danh mục loại CK
- [ ] Task 53: Test CK theo mặt hàng — nhập %, nhập ₫, sửa giá bán
- [ ] Task 54: Test CK theo tổng — tạo khoản CK, phân bổ tự động, sửa tay
- [ ] Task 55: Test chuyển method CK — confirm xóa dữ liệu cũ
- [ ] Task 56: Test footer tổng + cấp duyệt sau CK
- [ ] Task 57: Test export/import với CK
- [ ] Task 58: Test lịch sử ghi log CK
- [ ] Task 59: Test báo giá cũ (không CK) vẫn hoạt động bình thường

#### 29.10 — Bảng tổng hợp giá trị + Validate phân bổ + Fix bugs + In báo giá (2026-05-23)

- [x] Task 60: Bảng tổng hợp giá trị 8 dòng trên form edit (Tổng giá nhập → TSLN sau CK)
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - 8 rows: Tổng giá nhập, Tổng DT trước CK, Tổng CK, Tổng DT sau CK, Tổng VAT, Tổng TT sau VAT, TSLN trước CK, TSLN sau CK
  - Label CK thay đổi theo discountMethod (1: "theo mặt hàng", 2: "theo tổng")
  - TSLN chỉ hiện khi canViewImportPrice
- [x] Task 61: Layout CK tổng + Bảng tổng hợp trên 1 row (50/50)
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - Flex row d-flex, mỗi section flex: 0 0 50%
  - Bỏ max-width + margin-left auto khỏi .summary-table
- [x] Task 62: Validate bắt buộc phân bổ hết trước khi lưu (CK tổng)
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - save() kiểm tra allocationMatch khi discountMethod=2 + totalQuotationDiscount>0
  - Thêm option skipAllocationCheck để handleAllocateDiscount + openImportModal bypass
- [x] Task 63: Fix bug 2 lỗi đồng thời khi chuyển CK method 1→2 rồi phân bổ
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - handleAllocateDiscount gọi save(true, {skipAllocationCheck: true}) + check kết quả trước khi tiếp
- [x] Task 64: Hiện số tiền còn lại chưa phân bổ trên header cột CK phân bổ
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - "Còn: xxx" text-success khi match, text-danger khi chưa match
- [x] Task 65: Export Excel — bảng tổng hợp giá trị 8 dòng ở cuối
  - File: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` (tính summaryData)
  - File: `hrm-api/app/ExcelExport/BomListExport.php` (withSummaryData setter)
  - File: `hrm-api/resources/views/exports/bom_list.blade.php` (render 8 rows summary)
  - TSLN xanh/đỏ theo giá trị dương/âm, dòng Tổng TT sau VAT highlight blue
- [x] Task 66: Thêm field unit_price_after_discount vào DB + auto-compute
  - Migration: `2026_05_23_100000_add_unit_price_after_discount_to_quotation_tables.php`
  - File: `hrm-api/Modules/Assign/Entities/QuotationProductPrice.php` (cast)
  - File: `hrm-api/Modules/Assign/Entities/QuotationServiceItem.php` (cast)
  - File: `hrm-api/Modules/Assign/Services/QuotationService.php` (recomputeUnitPriceAfterDiscount)
  - Tự động tính trong recomputeTotals() — method 1: giá bán - CK₫, method 2: (giá×SL - phân bổ)/SL
- [x] Task 67: Cập nhật màn xem báo giá (index.vue) — CK columns + bảng tổng hợp
  - File: `hrm-client/pages/assign/quotations/_id/index.vue`
  - discountMethod dùng Number() conversion
  - "Thành tiền bán" → lineSaleAfterDiscount / svcSaleAfterDiscount
  - Footer TỔNG → totalSaleAfterDiscount
  - Bảng tổng hợp 8 dòng + layout 50/50 với CK tổng section
- [x] Task 68: Cập nhật In báo giá — config modal + preview + list page
  - File: `hrm-client/components/assign/quotation/QuotationPrintConfigModal.vue` (dynamic columns theo discountMethod)
  - File: `hrm-client/components/assign/quotation/QuotationPrintPreview.vue` (CK columns + summary table)
  - File: `hrm-client/pages/assign/quotations/index.vue` (truyền :discountMethod cho config modal)
  - File: `hrm-client/pages/assign/quotations/_id/index.vue` (truyền :discountMethod cho config modal)

### Phase 30: Báo giá tự xây dựng (Standalone Quotation)

> Spec chi tiết: `design-phase30-standalone-quotation.md`

#### 30.1 — Database + Model

- [ ] Task 1: Migration alter `quotations` — thêm `type` (default 1), nullable hoá `bom_list_id`, `pricing_request_id`, `solution_id`, `solution_version_id`. Drop unique constraint `pricing_request_id`. Backfill `type=1`.
- [ ] Task 2: Migration alter `quotation_product_prices` — nullable hoá `bom_list_product_id`, drop unique constraint, thêm 13 cột metadata (erp_product_id, code, name, product_attributes, model_id, brand_id, origin_id, unit_id, qty, parent_id, group_name, group_sort_order, product_type, sort_order)
- [ ] Task 3: Update Model `Quotation` — constants TYPE_BOM_BASED/TYPE_STANDALONE, scopes, nullable bomList relationship
- [ ] Task 4: Update Model `QuotationProductPrice` — relationships (tpModel, tpBrand, tpOrigin, tpUnit, erpProduct, parent, children), casts, accessors

#### 30.2 — BE: API tạo standalone

- [ ] Task 5: FormRequest `StoreStandaloneQuotationRequest` — validate project_id required, solution_id nullable, currency_id required
- [ ] Task 6: QuotationService::createStandalone() — snapshot customer từ dự án TKT, auto-gen code, tạo quotation type=2
- [ ] Task 7: Controller endpoint `POST /quotations/standalone` + route

#### 30.3 — BE: CRUD sản phẩm trên quotation

- [ ] Task 8: Endpoint `POST /quotations/{id}/products` — thêm SP đơn lẻ hoặc batch. Mode 1: chọn ERP (copy metadata). Mode 2: thêm nhanh (nhận trực tiếp). Guard: type=2 + status=1
- [ ] Task 9: Endpoint `PUT /quotations/{id}/products/{productId}` — sửa thông tin + giá SP
- [ ] Task 10: Endpoint `DELETE /quotations/{id}/products/{productId}` — xoá SP, cascade xoá children, recompute totals
- [ ] Task 11: Auto-create model/brand/origin/unit trên ERP DB nếu chưa có (reuse logic BOM import)

#### 30.4 — BE: Cập nhật logic tính toán (6 method)

- [ ] Task 12: `computeTotals()` — nhánh standalone: đọc hierarchy từ `quotation_product_prices.parent_id`, qty từ cùng bảng
- [ ] Task 13: `upsertPrices()` — standalone: match by `id` thay vì `bom_list_product_id`
- [ ] Task 14: `applyBulkVat()` — standalone: lấy cha/orphan từ self-ref `parent_id`
- [ ] Task 15: `calculateTotals()` — standalone: skip BOM dependency
- [ ] Task 16: `recomputeUnitPriceAfterDiscount()` — standalone: parent check từ self-ref
- [ ] Task 17: `allocateDiscount()` — verify hoạt động với standalone (đã dùng productPrices trực tiếp)

#### 30.5 — BE: Resource + Export/Import

- [ ] Task 18: `DetailQuotationResource` — trả metadata khi standalone (code, name, model, brand, origin, unit, qty, parent_id, group_name, product_type, sort_order)
- [ ] Task 19: Export Excel — standalone lấy product info từ `quotation_product_prices` trực tiếp
- [ ] Task 20: Import Excel — standalone import cả SP + giá (parse STT cha-con, nhóm hàng, tạo rows)

#### 30.6 — BE: Lịch sử

- [ ] Task 21: Log 3 action mới trong `quotation_histories`: `add_product`, `remove_product`, `update_product` (kèm metadata SP)

#### 30.7 — FE: Tạo báo giá standalone

- [ ] Task 22: Button "Tạo báo giá" trên toolbar trang danh sách `/assign/quotations/index.vue`
- [ ] Task 23: Modal tạo — 4 field: Dự án TKT (bắt buộc, cascading), Giải pháp (tuỳ chọn), Loại tiền tệ (bắt buộc, default VND), Mô tả
- [ ] Task 24: Submit modal → gọi `POST /quotations/standalone` → redirect `/quotations/{id}/edit`

#### 30.8 — FE: Edit page — mode standalone

- [ ] Task 25: Header info — ẩn trường BOM + YCBG khi `type=2`, giữ các field còn lại
- [ ] Task 26: Toolbar — thêm buttons "Chọn hàng hoá" + "Thêm nhanh" + "Thêm nhóm" (chỉ hiện khi standalone + status=1)
- [ ] Task 27: Bảng SP editable — inline sửa tên, mã, SL, ĐVT, TSKT. Nút xoá per row. Reuse rendering hiện có
- [ ] Task 28: Modal chọn hàng hoá từ ERP — adapt từ BOM pattern, gọi API quotation
- [ ] Task 29: Modal thêm nhanh SP — adapt từ BOM pattern, gọi API quotation
- [ ] Task 30: Logic nhóm hàng — thêm/xoá/đổi tên nhóm, group row rendering
- [ ] Task 31: Logic cha-con — "Thêm con" per row, expand/collapse, cascade xoá
- [ ] Task 32: Import Excel standalone — import cả SP + giá, preview + validate

#### 30.9 — FE: Danh sách + View + Print

- [ ] Task 33: Cột + filter "Loại BG" trên trang danh sách (2 option: Kế thừa BOM / Tự xây dựng)
- [ ] Task 34: Trang view `_id/index.vue` — ẩn BOM/YCBG khi standalone, hiển thị SP metadata
- [ ] Task 35: In báo giá — ẩn mục BOM trên bản in khi standalone

#### 30.10 — Test thủ công

- [ ] Task 36: Test tạo báo giá standalone (modal, redirect, data đúng)
- [ ] Task 37: Test CRUD sản phẩm — thêm nhanh, chọn ERP, sửa, xoá, cha-con, nhóm
- [ ] Task 38: Test tính toán — tổng giá, VAT, CK theo mặt hàng, CK theo tổng, phân bổ
- [ ] Task 39: Test export/import Excel standalone
- [ ] Task 40: Test workflow duyệt (submit → TP → BGĐ) cho standalone
- [ ] Task 41: Test báo giá cũ (BOM-based) vẫn hoạt động bình thường
- [ ] Task 42: Test lịch sử ghi log CRUD product
- [ ] Task 43: Test in báo giá standalone

### Phase 31: Logic hàng hoá cha-con (BOM + Báo giá) (2026-06-08)

> Spec: `design-phase31.md`. Áp dụng cả BOM + Báo giá (type=1 từ BOM + type=2 tự lập). Branch `tpe-develop-assign`.
>
> **Bối cảnh đã verify (KHÔNG được làm sai):**
> - Type=1 (từ BOM): `quotation_product_prices` chỉ là **overlay giá** key theo `bom_list_product_id`. Cấu trúc cha-con + attributes + `erp_product_id` lấy qua **join `bom_list_products`** trong `DetailQuotationResource` (nhánh else, dòng 72-123). KHÔNG copy `parent_id` ở các hàm `create()`.
> - Type=2 (tự lập): mọi field nằm trên `quotation_product_prices` (có `parent_id`, `code`, `name`, `erp_product_id`). Resource nhánh if (dòng 20-67).
> - `quoted_price` (giá bán) ĐÃ luôn trả trong resource (chỉ `estimated_price` bị gate quyền) → ẩn giá bán con hiện tại là do **FE template**.
> - `show_children` per-phiếu → lưu trên `quotation_product_prices` overlay của dòng cha (cả 2 type) + `bom_list_products` cho màn BOM. KHÔNG đụng BOM gốc khi toggle trên báo giá.
> - 2 editor FE TÁCH BIỆT: BOM = `BomBuilderEditor.vue` (+ BomBuilderTableCard/AddProductModal); Báo giá = `pages/assign/quotations/_id/edit.vue` (~3800 dòng) + `_id/index.vue` (view) + `QuotationPrintPreview.vue` (in). Sửa CẢ 2.
> - Recipe snapshot xảy ra khi LƯU (BE): `BomListService` (BOM) + `QuotationService::saveProductsFromFE` (báo giá type=2 pick ERP combo). Type=1 thừa hưởng từ BOM, không re-fetch.
> - Bảng "Tổng hợp giá trị" + footer TSLN chỉ lặp dòng CHA (`parent_id` null) → KHÔNG cộng dồn con. Hiện giá bán con là display-only, KHÔNG được cộng vào tổng.
> - Dịch vụ tách bảng `bom_list_service_items`/`quotation_service_items` KHÔNG có `parent_id` → không đụng cha-con.

#### 31.1 — Backend: DB + Entity

- [x] Task 1: Migration `2026_06_08_000001_add_show_children_to_bom_and_quotation_products` — thêm `show_children` tinyint default 1 vào `bom_list_products` (after `parent_id`) + `quotation_product_prices` (after `parent_id`) ✓
- [x] Task 2: `BomListProduct` + `QuotationProductPrice` (entity ĐÃ tồn tại, có `parent()`/`children()`, `$guarded=[]`) — `show_children` tự fillable (xác nhận cả 2 dùng `$guarded=[]`, không cần sửa) ✓

#### 31.2 — Backend: Endpoint recipe children

- [x] Task 3: `BomListController::getErpRecipeChildren(Request)` — input `erp_product_id` + `qty` (SL cha). Query `recipe_products` (mysql2, `env('DB_DATABASE_SECOND')`) theo `base_product_id`. Rỗng → trả `[]` (hàng lẻ) ✓
- [x] Task 4: Map con (pattern `searchErpProducts`): info + giá + `qty = recipe.qty × qtyCha`, `source='ERP'`, `is_recipe_child=true`. `cost_price=null` nếu thiếu quyền. **KHÔNG lọc status=1** (snapshot giữ con ngừng bán) ✓
- [x] Task 5: Route `GET /assign/bom-lists/erp-recipe-children` (cạnh `erp-products`) ✓

#### 31.3 — Backend: BomListService (tạo/sửa cha-con)

- [x] Task 6: `syncProducts()` (dòng 868-869) — lưu `show_children` cho dòng cha ✓
- [x] Task 7: **Cách A** — recipe ERP read-only, BE tin payload FE cho con cha ERP (không re-derive). Không cần code thêm ✓
- [x] Task 8: Bỏ rule cũ chặn con ERP dưới cha tạm (dòng 891-893). Thay bằng: con ERP dưới cha tạm thiếu quyền `Xem giá vốn hàng hoá` → `\Illuminate\Validation\ValidationException::withMessages`. Áp cả store+update ✓
- [x] Task 9: Giữ nguyên strip con khi cha là dịch vụ (863-866) + auto roll-up giá nhập (FE) ✓

#### 31.4 — Backend: QuotationService + Resource

- [x] Task 10: Lưu `show_children` ở `upsertBomProducts` (dòng 817) + `saveDirectProduct` (dòng 901). Check quyền ERP-child gộp vào `validateParentChildRules` (type=2) ✓
- [x] Task 11: `validateParentChildRules()` gọi đầu `upsertPrices` (dòng 775) — validate `quoted_price_cha × qty ≥ Σ(con)` cho cả type=1 (qty từ bom_list_products) + type=2 (qty từ payload), chỉ cha KHÔNG-ERP, epsilon 0.01, throw `\Illuminate\Validation\ValidationException` ✓
- [x] Task 12: Xác nhận `create()/createFromRequest()/createFromBom()` KHÔNG cần copy `parent_id` (type=1 thừa hưởng từ BOM), `show_children` dùng DB default ✓
- [x] Task 13: `DetailQuotationResource` — thêm `show_children` CẢ 2 nhánh (type=2 dòng 46, type=1 dòng 102, đều từ `$qpp` overlay). `quoted_price` con giữ trả như cũ ✓

#### 31.5 — Frontend BOM (`BomBuilderEditor.vue` + components) + BE flag

- [x] Task 14a: BE — `DetailBomListResource` thêm `can_view_cost_price` ✓
- [x] Task 14b: `BomBuilderEditor.handleAddProductApply` (async, ~2400) — pick cha ERP → gọi `erp-recipe-children` → push con khoá (`lockedPrice`, `isRecipeChild`, qty/giá từ recipe); rỗng=hàng lẻ; for...of await tuần tự; try/catch ✓
- [x] Task 14c: `mapProductToRow` (1030) thêm `showChildren`+`isRecipeChild`; `buildSavePayload` (2117) thêm `show_children` vào parent; `loadBomDetail` (897) set `canViewCostPrice` ✓
- [x] Task 15: `BomBuilderAddProductModal` props `canViewCostPrice`+`isAddingChild`, computed `displayedProducts`/`hideErpForChild` ẩn ERP khi thêm con thiếu quyền + ghi chú; editor truyền prop (`addProductParentRowId`) ✓
- [x] Task 16a: nút "Thêm con" thêm `&& !group.parent.erpProductId` (cả 2 nhánh có/không nhóm) ✓
- [x] Task 16b: nút mắt toggle `group.parent.showChildren` trên dòng cha ERP có con (cả 2 nhánh), độc lập `group.expanded` ✓

#### 31.6 — Frontend Báo giá (`quotations/_id/edit.vue` + `_id/index.vue` + print)

- [x] Task 18: `edit.vue` — hiện giá bán con của cha **tự tạo** (cha ERP giữ `—`) + cột thành tiền con; validate inline `isParentSalePriceInvalid` + flag `priceTouched`, chặn `save(strict)`; tổng/TSLN không đổi (FE-A1 ✓ — chờ test browser)
- [x] Task 17: `edit.vue` — pick cha ERP gọi recipe-children (async, parent_id=`_tempId`→BE resolve) + con khoá; ẩn nút thêm con cha ERP; toggle show_children; truyền props modal; load+save show_children. **+ Fix: guard cha ERP trong `refreshParentRollups` (edit) + `refreshParentTotals` (BOM) — không roll-up đè giá vốn combo ERP** ✓
- [x] Task 19: `index.vue` + `QuotationPrintPreview.vue` — con cha tự tạo hiện giá bán + thành tiền (cha ERP `—`); `visibleChildren()`/điều kiện ẩn con khi cha ERP `show_children=0`; print đổi chữ ký `renderChildCell(...,parent,...)` + điều kiện per-cha kèm `config.includeChildren`. Thêm helper `isErpProduct` ở cả 2 file. (Toggle ở edit.vue đã làm ở Task 17) ✓

#### 31.7 — Frontend: export tôn trọng show_children

- [x] Task 20: `resources/views/exports/bom_list.blade.php` (2 nhánh) + `BomListExport::registerEvents` — ẩn dòng con khi cha ERP `show_children=0` (bổ sung cho `includeChildren` global); row-count blade khớp registerEvents ✓

#### 31.9 — Fix sau verify (2026-06-09)

- [x] Fix quyền chọn con ERP ở chế độ TẠO MỚI: BOM `canViewCostPrice` chỉ set trong `loadBomDetail` (edit) → create=false (chặn nhầm); báo giá item mặc định `can_view_import_price:true` → create=true (quá lỏng). Sửa: lấy quyền strict từ `$store.state.permissions` (name 'Xem giá vốn hàng hoá'). BOM set trong `mounted`; edit.vue thêm computed `canPickErpChild` (riêng, không đụng `canViewCostPrice` hiển thị) + repoint prop modal. Khớp BE gate (strict, không gồm isCreator) ✓
- [x] Fix rule cũ P17 còn sót trong `BomBuilderAddProductModal`: `allProducts` loại bỏ ERP khi `isAddingChildToNonErp` (cha tạm) bất kể quyền → cha tạm KHÔNG chọn được con ERP dù có quyền (báo "chỉ được chọn hàng tự tạo làm hàng con"). Sửa: `allProducts` luôn gồm ERP, để `hideErpForChild` (theo quyền) lo ẩn/hiện; bỏ computed `isAddingChildToNonErp` + cảnh báo cũ ✓
- [x] Fix UX 422 khi lưu báo giá có con ERP dưới cha tạm: validate `validateParentChildRules` (BE dòng 845) chặn vì giá bán cha < Σ giá bán con (con ERP tự điền list_price). Giữ rule. Sửa UX: (1) FE chuyển check cha≥con ra MỌI nút lưu (trước chỉ ở `strict`/gửi duyệt) → `handleSaveDraft` cũng chặn client-side + inline `priceTouched` + toast; (2) BE `QuotationController::update` thêm `catch (ValidationException)` trả message cụ thể thay vì "The given data was invalid." ✓
- [x] Đồng nhất validate dịch vụ giống hàng hoá (chặn khi GỬI DUYỆT, cả FE+BE): nội dung = tên + SL>0 + giá bán>0 + CK≤đơn giá. FE: thêm inline đỏ `cell-invalid` ở ô giá bán DV (giống goods); name/SL/giá bán đã có trong `validatePrices` + CK trong `validateDiscountPerItem` (toast chung). BE `ensureAllPricesPositive`: DV thêm SL>0+tên+CK≤giá, **bỏ** chặn giá vốn DV=0 (over-strict cũ); goods thêm CK≤giá cho đồng bộ; message gộp rõ ràng ✓
- [x] Fix gửi duyệt báo "Chưa nhập đủ giá" cho hàng ERP có giá bán nhưng giá nhập (cost ERP)=0: ô giá nhập ERP khoá, user không sửa được → KHÔNG được bắt buộc. Bỏ chặn giá nhập với hàng ERP ở `validatePrices` (FE) + `ensureAllPricesPositive` (BE). Giá nhập chỉ bắt buộc + báo inline (đã có ở ô) cho hàng TỰ NHẬP ✓
- [x] validate giá cha ≥ Σ con CHỈ khi gửi duyệt (lưu tạm bỏ qua): FE chuyển check vào khối `strict` (chỉ `openSubmit`). BE tách `validateParentChildRules` (upsertPrices, mọi save) chỉ còn **check quyền** con ERP; thêm `assertParentSalePriceFloor` (DB-based, type1+type2) gọi ở `submit()` + `selfApprove()` (chỉ lúc gửi duyệt/tự duyệt) ✓
- [x] Fix nút "Ẩn/Hiện con" (báo giá edit) không có tác dụng: màn edit render con qua `getChildren` không phụ thuộc `show_children`. Thêm method `visibleChildren(parent)` (ẩn con khi cha ERP + show_children=0) cho vòng render con; totals/validate vẫn dùng `getChildren`. Bỏ chặn nuốt lỗi recipe (log + toast) ✓
- [x] SL con recipe KHOÁ + tự nhân theo SL cha (đổi quyết định cũ "không re-scale") — báo giá: BE endpoint trả `recipe_qty`; FE lưu `_recipeUnitQty` (load phục hồi = qty/SL cha), input SL con `:disabled="isRecipeChild"`, `@input` SL cha → `onParentQtyChange` nhân lại con. Bỏ spinner input SL (class `.no-spin` + CSS) ✓
- [x] Đồng nhất BOM: `BomBuilderEditor` lưu `recipeUnitQty` lúc tạo con + derive khi load (`mapProductsToGroups`) + method `onParentQtyChange` (ERP scale con + refresh, tạm chỉ refresh); `BomBuilderTableCard` input SL cha `@input` emit `parent-qty-change` + SL con `:disabled` khi cha ERP + class `.no-spin` (4 input) + CSS. Báo giá đã test PASS ✓
- [x] (REVERTED — user yêu cầu giữ nguyên giá ERP, không tự roll-up) Đã khôi phục guard `if isErpProduct return` trong refreshParentRollups (edit) + refreshParentTotals (BOM); bỏ BE `rollupParentImportCost`. Thay bằng VALIDATE: giá vốn cha < Σ giá vốn con → CHẶN gửi duyệt (không sửa giá). FE `isParentImportInvalid` + check trong save(strict) (gate canViewCostPrice); BE `assertParentImportFloor` gọi ở submit()+selfApprove() (check cả cha ERP). ✓
- [x] Validate bắt buộc "Điều khoản thanh toán" khi gửi duyệt: FE `validateForm` (strip HTML rich editor) + label `required` + lỗi inline; BE `submit()` guard `strip_tags(payment_terms)` rỗng → throw ✓
- [x] Bỏ hiển thị số tiền CK dạng âm (5 chỗ): edit.vue (dòng V + footer pricing), index.vue (dòng V + bảng tổng cũ), QuotationPrintPreview (tổng CK) — bỏ dấu `-`, giữ màu đỏ ✓
- [x] Tổng "Thành tiền nhập" = Σ dòng CHA (Cách A, user duyệt): sửa `totalImport` + `productImportTotal` ở edit.vue + index.vue (bỏ kiểu Σ con cho dòng-có-con → dùng `lineImportTotal(p)`/`lineImport(p)` của cha). Bảng Tổng hợp (summaryBreakdown FE + computeSummaryBreakdown BE) vốn đã Σ dòng cha. Giờ đồng bộ: line-items + Tổng hợp + in đều = Σ dòng cha ✓
- [x] Sync màn xem ↔ tạo/sửa: dòng V "Tổng giá trị" cột CK ở index.vue hiện `-X` đỏ (text-danger) giống edit (trước hiện plain). Đã rà: cấu trúc bảng tổng hợp (I-V, cột), hasCk≡discountMethod, TSLN trước/sau CK, auto-allocation — đều khớp. (Bảng "CK tổng" edit có thêm cột Kiểu/% để nhập — index read-only 2 cột là hợp lý, không đổi) ✓
- [x] Màn xem chi tiết: layout CK tổng + Tổng hợp giá trị đổi từ side-by-side 50/50 sang **full width stacked** (giống edit/create) — `d-flex flex-wrap` + mỗi section `flex:0 0 100%` ✓
- [x] Fixbug CK phân bổ tự động lệch giữa màn tạo (edit.vue) và xem chi tiết (index.vue): index.vue tính `autoAllocationMap` thiếu chi phí vận chuyển trong base + làm tròn nguyên (56) vs edit có VC + cents (54,57). Sửa index.vue khớp edit: thêm dòng SHIP (`item.shipping_cost`) vào base + dùng cents (÷100); `totalAutoAllocatedDiscount` loại SHIP để footer khớp dòng hiển thị. (Giá trị thực `allocated_discount_amount` vốn đã khớp — chỉ cột tham chiếu lệch) ✓
- [x] Nới rộng + `white-space:nowrap` 4 cột header bảng báo giá (Thành tiền nhập 150px, CK phân bổ tự động 170px, Thành tiền bán 150px, Thành tiền sau VAT 170px) để title không xuống 2 dòng ✓
- [x] Thêm confirm khi xoá hàng hoá khỏi báo giá (`removeDirectProduct`): `$bvModal.msgBoxConfirm` (okVariant danger); xoá cha → xoá luôn con kèm theo (cascade, dùng String so khớp parent_id — sửa luôn bug cũ orphan qua Number sai với cha tạm) ✓
- [x] Fixbug: hàng cha ERP (bộ ghép) đang cho XOÁ con → ẩn nút Xoá con: báo giá `edit.vue` nút xoá con `v-if="!isRecipeChild(child)"`; BOM `BomBuilderTableCard` div action con (Sửa+Xoá) thêm `&& !group.parent.erpProductId` (2 nhánh). Thêm con đã ẩn sẵn (cha ERP không có nút "Thêm con"). Con recipe nay khoá hoàn toàn (không thêm/xoá/sửa/đổi SL) ✓
- [x] Thêm text "- Bảng giá bán lẻ" sau tỷ giá ở 3 màn báo giá (edit `Tỷ giá: 1 USD = X VND (ngày) - Bảng giá bán lẻ`, index, print `exchangeRateText`). Chỉ hiện khi currency ≠ VND (đi kèm dòng tỷ giá) ✓
- [x] Thêm validate báo giá: (1) VAT 0–100% + (2) CK% 0–100% → áp CẢ lưu nháp + gửi duyệt (`validateVat` mở rộng + `validateDiscountPercentRange`, gọi đầu `save()`); (3) thành tiền bán mỗi hàng hoá/dịch vụ > 0 → CHỈ gửi duyệt (khối strict, dùng `lineSaleAfterDiscount`/`svcSaleAfterDiscount`), CPVC không validate (giữ Phase 26 cho nháp). BE: VAT/CK range đã enforce sẵn qua `QuotationUpdateRequest` (min:0|max:100 cho products/service/shipping/quotation_discounts) ✓

- [x] Fix rule cũ P17 còn sót chỗ THỨ 2 — `BomBuilderEditor.handleAddProductApply` (dòng 2346-2352): cha tạm + có item ERP → chặn cứng `'Hàng cha là hàng tự tạo — không được thêm hàng ERP làm hàng con.'` bất kể quyền (lần fix trước chỉ gỡ ở AddProductModal `allProducts`). Triệu chứng: có quyền, popup hiện hàng ERP, chọn → vẫn báo lỗi & không thêm được. Sửa: thay chặn cứng bằng guard theo quyền `!this.canViewCostPrice` (đồng nhất message + logic BE `BomListService:892`). Có quyền → cho thêm con ERP dưới cha tạm ✓

- [x] Fix cột "CK phân bổ tự động" màn XEM (index.vue) làm tròn nguyên (55, 23) trong khi màn tạo/sửa (edit.vue) giữ 2 số lẻ (54,57 / 22,74) → lệch hiển thị. Nguyên nhân: `index.formatMoney` dùng `Math.round(n)`, edit `formatMoney` không round. Giá trị `autoAllocationMap` hai bên đã khớp (cents) từ fix trước — chỉ lệch ở format. **Phương án 2 (user chọn):** bỏ `Math.round` ở `formatMoney` chung của index.vue → TOÀN BỘ cột tiền màn xem giữ số lẻ giống edit (đồng nhất hoàn toàn). Print/export là component riêng (`QuotationPrintPreview.vue`), không bị ảnh hưởng ✓

#### 31.8 — Test thủ công

- [ ] Task 21: BOM — cha ERP có recipe → con auto, khoá, toggle ẩn/hiện; cha ERP không recipe → không con/không nút thêm
- [ ] Task 22: BOM — cha tạm + con ERP (có quyền) / chặn khi không quyền; cha tạm + con tự tạo OK
- [ ] Task 23: Báo giá type=1 (từ BOM) — cha-con hiển thị đúng, con cha tạm hiện giá bán, con cha ERP ẩn, toggle hoạt động
- [ ] Task 24: Báo giá type=2 (tự lập) — pick ERP combo → con auto khoá; cha tạm + con; validate cha ≥ Σ con chặn lưu đúng
- [ ] Task 25: Tổng hợp giá trị + TSLN + footer không đổi khi hiện giá bán con (không double-count); báo giá cũ vẫn chạy
- [ ] Task 26: Import Excel báo giá giữ validate cha ≥ Σ con; in + export tôn trọng show_children

### Phase 32: Làm tròn số nhất quán toàn báo giá (2026-06-10)

> Quyết định (user chốt): GIỮ nút "Áp dụng" ghi đè đơn giá như cũ + LƯU `rounding_mode` theo báo giá. TẤT CẢ cột số tiền làm tròn theo mode đã chọn; chưa chọn = mặc định **tối đa 2 số lẻ**. Áp cho cả 3 màn: sửa (`edit.vue`), xem (`index.vue`), in (`QuotationPrintPreview.vue`).
> Giá trị mode: -3 (nghìn), -2 (trăm), -1 (chục), 0 (nguyên), 1 (1 lẻ), 2 (2 lẻ), null = mặc định 2 lẻ.

#### 32.1 — Backend

- [x] B1: Migration `2026_06_10_000001_add_rounding_mode_to_quotations_table` — `tinyInteger('rounding_mode')->nullable()->after('discount_method')` ✓
- [x] B2: Quotation entity — thêm cast `'rounding_mode' => 'integer'` ($guarded=[] sẵn) ✓
- [x] B3: QuotationService — `'rounding_mode' => $data['rounding_mode'] ?? null` ở create standalone (dòng 80) + thêm `'rounding_mode'` vào loop update field (dòng 555). createFromBom để null ✓
- [x] B4: QuotationUpdateRequest (`sometimes|nullable|integer|between:-3,2`) + QuotationStoreRequest (`nullable|integer|between:-3,2`) ✓
- [x] B5: DetailQuotationResource — trả `'rounding_mode'` (int hoặc null) ✓. php -l 6 file sạch

#### 32.2 — Frontend (helper format chung 3 màn)

- [x] F1: `edit.vue` — computed `roundingPrecision` = `roundingMode ?? 2`; formatMoney round value + `maximumFractionDigits: max(0,p)`; thêm `rounding_mode` vào payload save (parseInt) + load từ detail (String). Option đầu select đổi thành "Mặc định (tối đa 2 số lẻ)" (bỏ disabled → quay lại null được). Cập nhật tooltip ✓
- [x] F2: `index.vue` — computed `roundingPrecision` = `item.rounding_mode ?? 2`; formatMoney dùng precision ✓
- [x] F3: `QuotationPrintPreview.vue` — computed `roundingPrecision` = `item.rounding_mode ?? 2`; formatMoney dùng precision ✓
- [ ] F4: Test thủ công: chọn mode (vd Số nguyên) ở edit → save → xem + in đều hiển thị số nguyên; không chọn → cả 3 màn hiển thị tối đa 2 lẻ đồng nhất (⏳ chờ user migrate + E2E)

- [x] Bỏ bắt buộc trường **Model** khi tạo hàng hoá TẠM (`BomBuilderAddProductModal.createProduct` — gỡ check `model_id` bắt buộc + bỏ `required` ở label Model). Modal dùng chung BOM + Báo giá → áp cả 2 màn. Brand/Origin/ĐVT/Tên vẫn bắt buộc
- [x] Fix bug: gộp BOM thành phần (cha tạm + con ERP) vào BOM tổng hợp → con ERP biến thành mã hàng tạm `HH-xxxxx`. Nguyên nhân: `cloneSubBomGroup` map object hàng CON thiếu `erpProductId` (chỉ object cha có) → `dedupeTempGoodsCodes` coi là hàng tạm (đổi mã HH khi trùng) + lưu `erp_product_id=null`. Sửa: thêm `erpProductId/productType/costId/isRecipeChild` cho con + `showChildren` cho cha trong `cloneSubBomGroup`

- [x] Màn DANH SÁCH báo giá (`quotations/index.vue`): cột "Tổng giá trị" (đang lấy `total_sale` = tổng tạm chỉ từ product prices, sai) → đổi label "Tổng giá trị sau VAT" + lấy `total_after_vat` (cột DB, BE `recomputeTotals` = sau CK + VAT). Gỡ cột "Tổng sau VAT" trùng. Fallback `|| total_sale` cho phiếu cũ total_after_vat=0
- [x] Fix bug cache `total_after_vat` SAI (list hiện 1.748 vs chi tiết 3.781.747,99): `QuotationService::update()` gọi `upsertPrices`→`recomputeTotals` ở dòng 601 TRƯỚC khi lưu service items (605+) + CK tổng (644+) → cache theo giá dịch vụ CŨ. Sửa: thêm `recomputeTotals` LẦN CUỐI ở cuối `update()` (sau syncServiceCostRatesToErp) + `$quotation->load('serviceItems')` để đọc giá mới. computeTotals vốn đã cộng dịch vụ đúng. php -l sạch
- [x] Backfill cache total_after_vat cho báo giá CŨ stale (user duyệt): chạy reflection gọi `recomputeTotals` toàn bộ (timestamps off). 22 phiếu xử lý, 3 phiếu sai đã sửa. BG23 = 3.781.747,99 / VAT 280.000 ✓ (local)
- [x] Tạo seeder `RecomputeQuotationTotalsSeeder` (Modules/Assign/Database/Seeders) để chạy backfill trên PRODUCT: reflection gọi `recomputeTotals` toàn bộ, timestamps off. Lệnh: `php artisan db:seed --class="Modules\Assign\Database\Seeders\RecomputeQuotationTotalsSeeder"`. php -l sạch

- [x] Fix bug: lập báo giá từ YCBG (yêu cầu xây dựng giá) báo "Bạn không phải Sale phụ trách dự án này" dù user có quyền xây giá (dự án Liên phòng ban). Nguyên nhân: `QuotationController::store()` gate CỨNG `main_sale_employee_id` cho mọi trường hợp. FE "Tạo báo giá" từ YCBG gọi `POST assign/quotations` với `pricing_request_id` → trúng gate sai. (`createFromRequest` có gate đúng `ensureBuildPricePermission` nhưng là DEAD CODE.) Sửa: khi có `pricing_request_id` → gate theo quyền xây giá theo `implementation_type` (BY_DEPT=2 → "Xây dựng giá bán theo phòng" + cùng phòng; SELF/CROSS_DEPT/null → "Xây dựng giá bán theo công ty"); không có → giữ gate sale phụ trách. php -l sạch
  - Ghi chú (chưa sửa, ngoài phạm vi): path `create()` không đổi status YCBG (→ Đã có báo giá) + không khóa race như `createFromRequest`. Cần xác nhận có cần bổ sung không

- [x] Màn `/assign/product-project`: chỉ lấy hàng hoá TẠM (tự tạo), bỏ hàng từ ERP. Thêm `->whereNull('p.erp_product_id')` vào `ProductProjectController::bomKeyQuery` (bom_list_products) + `quotationKeyQuery` (quotation_product_prices). Key query quyết định tập hàng → buildQuery/buildQuotationQuery (lấy chi tiết theo id đã lọc) không cần sửa. php -l sạch

- [x] Fix bug: dịch vụ ERP (chọn từ danh mục, có `cost_id` + hệ số `rate_value_capital`) trong báo giá TỪ BOM (type=1) đang cho nhập cả giá bán + giá nhập. Đúng: giá nhập = giá bán × hệ số giá vốn, KHOÁ. Nguyên nhân: `svcCostLocked` + `onSvcSalePriceChange` gate `isDirectQuotation` → chỉ type=2 khoá+auto. Sửa (edit.vue): `svcCostLocked = svcHasRate` (khoá cả type=1+2 khi có hệ số); `onSvcSalePriceChange` luôn `recalcSvcCost`; recompute giá nhập khi LOAD (canEdit) để đồng bộ ngay. `rate_value_capital` BE đã trả ở resolveServiceItems cho cả 2 type. estimated_price đã có trong payload save
  - Ghi chú: dịch vụ ERP KHÔNG có hệ số (rate null) → vẫn cho nhập tay (fallback, không khoá). BE chưa enforce (trust FE) — phiếu type=1 cũ giữ giá vốn BOM tới khi mở sửa+lưu lại. Cần BE enforce/backfill không?
- [x] Mô hình giá vốn dịch vụ ERP (user chốt): phân biệt theo **hệ số `rate_value_capital`**:
  - **Hệ số > 0 (đã thiết lập — danh mục có sẵn / thêm nhanh từ báo giá đã set):** giá nhập KHOÁ = giá bán × hệ số. BE ENFORCE (tự tính lại, không tin FE). KHÔNG ghi ngược danh mục.
  - **Hệ số = 0/null (chưa thiết lập — thêm nhanh từ BOM ẩn giá):** giá nhập NHẬP TAY; khi lưu BE tính hệ số = giá vốn/giá bán → GHI NGƯỢC danh mục ERP. Lần sau dịch vụ đó có hệ số → khoá.
  - FE `edit.vue`: `svcCostLocked`/`svcHasRate`/`recalcSvcCost` đổi điều kiện sang `rate > 0`.
  - BE `QuotationService`: thêm `enforceServiceCostsFromRate` (rate>0 → cost=sale×rate); `syncServiceCostRatesToErp` chỉ chạy cho rate=0/null (bỏ guard `isDirectQuotation`, thêm filter rate). Gọi cả ở `create()` + `update()` trước recomputeTotals. php -l sạch.
  - Test: dịch vụ danh mục (rate>0) → giá nhập khoá; dịch vụ thêm nhanh từ BOM (rate=0) → nhập tay, lưu xong danh mục có hệ số, mở lại → khoá

- [x] Nguyên tắc kiến trúc: **BOM KHÔNG quản lý giá** (giá nhập/giá bán/hệ số/tỷ suất) — toàn bộ logic giá ở Báo giá. BOM = cơ cấu hàng hoá (cha-con, SL, model/brand/origin/ĐVT, thông số). Cleanup BE `QuotationService`: gỡ mọi chỗ đọc `estimated_price` từ BOM khi tạo báo giá → init = 0 (hàng tạm + dịch vụ); hàng ERP giữ lấy giá từ danh mục ERP. Sửa: `create()` (127,151), `createFromBom()` (443,470 + gỡ `$bomRate` thừa), `createFromRequest()` (312,333 — dead nhưng đồng nhất). php -l sạch. (Cột giá BOM editor đã ẩn sẵn `visibleColumns=false`)

- [x] VAT hàng hoá ERP: lấy từ bảng `products` ERP (cột `vat_percent`), KHÔNG cho user sửa.
  - BE: `searchErpProducts` + `getErpRecipeChildren` + `getErpProductPrices` trả thêm `vat_percent`. Method mới `QuotationService::enforceErpProductVat` (dùng `resolveProductsAndPrices`, xử lý type=1+type=2) set `quotation_product_prices.vat_percent` = ERP `products.vat_percent` cho hàng có `erp_product_id`; gọi ở `create()`/`update()`/`createFromBom()` trước recomputeTotals. `applyBulkVat` (type=1) skip hàng ERP.
  - FE `edit.vue`: ô VAT hàng cha `:disabled` thêm `|| isErpProduct(parent)` + tooltip; set `vat_percent` từ ERP khi thêm (handleAddProductApply + recipe children + mapProduct nạp BOM); `applyVatToProducts` skip hàng ERP.
  - VAT đồng loạt KHÔNG áp cho Dịch vụ & Chi phí khác (VAT lấy từ danh mục ERP): bỏ block áp service trong `applyVatToProducts`. BE `applyBulkVat` vốn chỉ đụng products, không đụng service.
  - php -l sạch. Lưu ý: phiếu cũ có hàng ERP vat sai sẽ tự đúng khi mở sửa + lưu lại (enforce). Cần backfill không?

- [x] Fix bug: hàng ERP từ BOM bị "đồng bộ hàng tạm sang ERP" (`TmpProductSyncService`) nhầm là hàng tạm. Nguyên nhân: overlay `quotation_product_prices` (type=1) KHÔNG set `erp_product_id` (chỉ overlay giá); `TmpProductSyncService::sendApproval/pullStatus` đọc trực tiếp `whereNull('erp_product_id')` → hàng ERP (overlay erp=null) bị coi là tạm + items map code/name=null. Sửa: đồng bộ định danh (`erp_product_id` + code/name/model/brand/origin/unit/product_attributes) từ bom_list_products sang overlay ở `create()` + `createFromBom()` + `upsertBomProducts()`. upsertBomProducts chỉ set erp_product_id khi BOM là ERP (giữ giá trị overlay cho hàng tạm đã được pullStatus duyệt). Seeder `BackfillQuotationProductErpIdSeeder` (COALESCE, không ghi đè) cho phiếu cũ. php -l sạch. Resource type=1 vẫn dùng join nên hiển thị không đổi

- [x] Fix bug: tạo hồ sơ trình duyệt GIẢI PHÁP tự động lấy BOM loại Thành phần (đáng lẽ chỉ Tổng hợp). Nguyên nhân: `SolutionService::storeSolutionReviewProfile` (~1914) chỉ filter `TYPE_AGGREGATE` khi `!$isSelfImpl` → dự án Tự triển khai (type=1) bỏ filter → pick bất kỳ BOM Hoàn thành mới nhất (gồm Thành phần). User chốt (A): LUÔN chỉ lấy Tổng hợp. Sửa: gỡ điều kiện `if (!$isSelfImpl)`, luôn `where bom_list_type = TYPE_AGGREGATE` + thống nhất message lỗi "Chưa có BOM tổng hợp Hoàn thành". `$isSelfImpl` giữ cho logic status auto-duyệt. Hồ sơ HẠNG MỤC (`SolutionModuleService`) vốn đã filter aggregate không điều kiện → đã đúng. php -l sạch
  - Lưu ý: dự án Tự triển khai giờ BẮT BUỘC có BOM Tổng hợp Hoàn thành mới gửi được hồ sơ (trước cho phép Thành phần)

- [x] Dịch vụ/chi phí từ BOM sang báo giá: ĐÃ chạy đúng (user xác nhận load đủ ở cả flow nút "Lập báo giá" lẫn màn danh sách). Verify: BE createFromBom/create + resource + fetchData copy dịch vụ ĐÚNG (test BOM 41 → 3 dịch vụ). Bổ sung (CHƯA commit, cần deploy): FE `loadBomProducts` copy `bom.service_items` → serviceItems (flow chọn BOM trong dropdown trước giờ chưa copy); BE `DetailBomListResource` thêm `rate_value_capital` vào service_items (khoá giá nhập dịch vụ ERP). php -l sạch

- [x] Fix lỗi làm tròn: giá nhập cha tạm hiện `13.419999999999998` (= 8.95 + 4.47 sai số float). Nguyên nhân: `refreshParentRollups` (edit.vue) + `refreshParentTotals` (BomBuilderEditor) tính `estimated_price = sumChildImport / parentQty` KHÔNG làm tròn → ô input (raw, không qua formatMoney) hiện số float dài. Sửa: làm tròn roll-up — edit.vue theo `roundingPrecision` (kiểu chọn trên toolbar "Làm tròn", chưa chọn = mặc định 2 số lẻ); BomBuilderEditor 2 số lẻ (BOM không có toolbar làm tròn). Gọi `refreshParentRollups` khi load (fetchData + loadBomProducts) để làm sạch float cũ ngay

### Phase 33: Validate báo giá hiển thị inline tại ô (bỏ toast) (2026-06-10)

> Yêu cầu: mọi validate (Giá bán, VAT, chiết khấu, giá nhập, thành tiền, CPVC, CK tổng, field bắt buộc) phải hiện INLINE tại đúng ô (`is-invalid`/`cell-invalid` + `invalid-feedback`, flag touched), KHÔNG hiện trên toast. Chỉ ở màn tạo/sửa `edit.vue` (view/print read-only).

- [x] Thêm flag `rangeTouched` (VAT + CK% range validate mọi lần lưu) + helper `isVatInvalid` / `isShippingVatInvalid` / `isDiscountPercentRangeInvalid`
- [x] Inline VAT 0–100%: ô VAT hàng cha + dịch vụ + chi phí vận chuyển (is-invalid + feedback)
- [x] Inline CK% 0–100% (method 1): ô CK% hàng cha + dịch vụ; CK tổng % đã có sẵn (qdRowErrors)
- [x] Inline giá bán/thành tiền > 0: ô giá bán cha + dịch vụ dùng `lineSaleAfterDiscount/svcSaleAfterDiscount ≤ 0` (gộp giá ≤ 0 + thành tiền ≤ 0) + message
- [x] Inline giá nhập > 0 (tự nhập) + giá vốn cha ≥ Σ con: ô giá nhập hàng cha
- [x] Inline CK theo dòng ≤ đơn giá bán (đã có is-invalid) + thêm message; CPVC giá nhập/giá/CK thêm message
- [x] `save()`: gỡ TẤT CẢ toast validate field; bật touched tương ứng + gọi `scrollToFirstError()` cuộn tới ô lỗi đầu tiên
- [x] Method `scrollToFirstError()` — `$nextTick` querySelector `.is-invalid/.cell-invalid/.text-small-error` → scrollIntoView + focus
- [x] Fix bug: CK tổng %>100 bấm Lưu/Gửi duyệt "không phản hồi" — `validateDiscountPercentRange` short-circuit return TRƯỚC khi `validateQuotationDiscounts` bật `qdTouched` → inline CK tổng không hiện + scroll không thấy gì. Sửa: bật `qdTouched=true` ngay đầu `save()` (cùng `rangeTouched`). Đồng thời `validateVat` chỉ quét hàng CHA (con không có ô VAT) để không chặn ngầm không inline
- [ ] Test thủ công: nhập VAT 150 / CK dòng 120% / CK tổng 120% / bỏ trống giá bán → bấm Lưu/Gửi duyệt → KHÔNG có toast, ô lỗi viền đỏ + text + tự cuộn tới (⏳ chờ user)
- Giữ toast (không phải validate field): nhắc "phân bổ lại CK khi đổi giá" (workflow), "trùng mã hàng con khi thêm" (chưa có ô), lỗi mạng/hệ thống, server 422 fallback

## Checkpoint

### Checkpoint — 2026-06-10 (Phase 31 — fixes test vòng 2)
Vừa hoàn thành: (1) REVERT tự ý roll-up giá vốn cha ERP → giữ nguyên giá ERP (khôi phục guard edit+BOM, bỏ BE rollupParentImportCost). (2) Validate giá vốn cha < Σ con → CHẶN gửi duyệt (FE isParentImportInvalid + BE assertParentImportFloor, không sửa giá). (3) Tổng "Thành tiền nhập" = Σ dòng CHA (Cách A — sửa totalImport+productImportTotal ở edit+index; summaryBreakdown/BE vốn đã đúng). (4) Bỏ hiển thị số tiền CK dạng âm (5 chỗ edit/index/print). (5) Validate bắt buộc "Điều khoản thanh toán" khi gửi duyệt (FE validateForm strip HTML + BE submit guard). (6) Sync auto-allocation + layout full-width + dòng tổng CK giữa edit↔view (vòng trước). Lưu memory: hỏi trước khi đổi logic + hàng ERP giữ nguyên giá.
Đang làm dở: Không
Bước tiếp theo: User chạy `php artisan migrate` + build FE + test theo test-summary-phase31.md. Tồn: "Bảng giá bán lẻ" khi VND; validate VAT/CK range cho màn BOM (nếu cần).
Blocked: Không

### Checkpoint — 2026-06-09 (Phase 31 + fixes sau review)
Vừa hoàn thành: Phase 31 (logic hàng hoá cha-con BOM + Báo giá) CODE DONE toàn bộ (Task 1-20 + 31.9 fixes). BE: migration show_children, endpoint erp-recipe-children (+recipe_qty), BomListService (check quyền con ERP), QuotationService (validateParentChildRules quyền + assertParentSalePriceFloor submit + ensureAllPricesPositive đồng nhất DV), Resource trả show_children + can_view_cost_price. FE BOM + Báo giá: recipe snapshot + con khoá (thêm/xoá/sửa/SL đều khoá) + SL con nhân theo SL cha + toggle show_children + hiện giá bán con cha tạm + validate (VAT/CK range cả nháp+gửi, thành tiền>0/cha≥con/giá nhập tự nhập/dịch vụ chỉ gửi duyệt) + bỏ spinner + confirm xoá + text "Bảng giá bán lẻ" + sync auto-allocation/layout/dòng tổng CK giữa edit↔view.
Đang làm dở: Không
Bước tiếp theo: User chạy `php artisan migrate` (cột show_children) + build FE + test theo `test-summary-phase31.md`. Còn tồn (chờ user xác nhận nếu cần): "Bảng giá bán lẻ" hiển thị khi VND; siết BE chống sửa payload recipe (Cách B); áp validate VAT/CK range cho màn BOM.
Blocked: Không

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

### Phase 18: Cập nhật UI + Fix bugs + Lịch sử BOM (2026-05-07)

#### 18.1 Cập nhật UI danh sách BOM
[x] Task 1: Bỏ font-weight bold 3 cột (Hạng mục, Loại BOM, Người tạo)
[x] Task 2: Loại BOM đổi từ V2BaseBadge sang text thuần

#### 18.2 Xuất Excel bổ sung
[x] Task 3: Button "Xuất Excel" trong footer trang chi tiết BOM
[x] Task 4: Button "Xuất Excel" ở header bảng chi tiết (bên trái "Ẩn/hiện cấp con")

#### 18.3 Popup thêm sản phẩm
[x] Task 5: Button "Lưu và tiếp tục" — không tắt popup, reset form, giữ tab Tạo mới

#### 18.4 Cấu hình duyệt giá
[x] Task 6: Đưa "Tỷ suất lợi nhuận mức sàn" về /assign/settings/price-approval (Section 0)
[x] Task 7: Bỏ title "Cấu hình duyệt giá bán" trùng topbar
[x] Task 8: Fix bug input "Đến" bị ẩn vĩnh viễn khi xoá giá trị (v-if logic)
[x] Task 9: Validate giá trị nối tiếp giữa các cấp (order_value tăng dần, profit_margin giảm dần)
[x] Task 10: Đổi "Lưu" → "Lưu cấu hình" cho đồng bộ

#### 18.5 Fix logic báo giá
[x] Task 11: Fix tổng giá nhập popup gửi duyệt (double-count parent+children) — BE calculateTotals roll-up
[x] Task 12: Fix profit_margin formula — thống nhất (sale-import)/sale ở 5 vị trí (BE controller, FE edit, FE show)
[x] Task 13: Fix áp VAT đồng loạt mất data chưa lưu — chuyển sang FE-only manipulation
[x] Task 14: Fix 404 khi áp VAT (gọi sai method recalcParentFromChildren → refreshParentRollups)
[x] Task 15: Fix input VAT không cập nhật visually — thêm vatBulkKey vào :key của <tr> (Vue 2 reactivity)

#### 18.6 Lịch sử BOM List
[x] Task 16: Migration tạo bảng bom_list_logs
[x] Task 17: Entity BomListLog (8 actions, labels, colors, relations)
[x] Task 18: BomListService — createLog() private method
[x] Task 19: Log tại store(), update(), destroy()
[x] Task 20: Log tại syncStatusFromSubmission() (submitted/approved/rejected)
[x] Task 21: Log tại importProducts()
[x] Task 22: API GET /assign/bom-lists/{id}/logs + controller method + route
[x] Task 23: FE BomListLogModal.vue — timeline popup
[x] Task 24: Button "Xem lịch sử" trên danh sách BOM (row action)
[x] Task 25: Button "Lịch sử" trên trang chi tiết BOM (footer)

#### 18.7 Chi tiết thay đổi trong log
[x] Task 26: buildChanges() resolve tên cho FK (Dự án, Giải pháp, Hạng mục, Khách hàng, Tiền tệ)
[x] Task 27: snapshotProducts() + buildProductChanges() — tracking thêm/xoá/sửa sản phẩm
[x] Task 28: FE hiển thị changes (field cũ→mới) + product diff (added/removed/modified)

### Phase 19: Xuất/Import Excel trên màn sửa Báo giá (2026-05-07)

> **Spec:** docs/superpowers/specs/2026-05-07-quotation-import-export-design.md

#### 19.1 BE — Route + Controller method importPrices

[x] Task 1: Thêm route POST import-prices (validate + import)
  - File: `Modules/Assign/Routes/api.php`
  - Trong group `/assign/quotations`, thêm trước route `/{id}/export-excel`:
    ```php
    Route::post('/{id}/import-prices', [QuotationController::class, 'importPrices']);
    ```

[x] Task 2: Controller importPrices() — parse Excel + match code + update prices
  - File: `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`
  - Thêm use: `use Maatwebsite\Excel\Facades\Excel;`
  - Method `importPrices(Request $request, $id)`:
    ```php
    public function importPrices(Request $request, $id)
    {
        try {
            $request->validate([
                'file' => 'required|file|mimes:xlsx,xls|max:5120',
            ]);

            $quotation = Quotation::with(['bomList.products', 'productPrices'])->findOrFail($id);

            if ((int)$quotation->status !== Quotation::STATUS_DANG_TAO) {
                return $this->responseJson('Chỉ được import khi báo giá ở trạng thái Đang tạo', Response::HTTP_UNPROCESSABLE_ENTITY);
            }

            $rows = Excel::toArray(new \App\Imports\EmptyImport(), $request->file('file'));
            $sheet = $rows[0] ?? [];

            if (empty($sheet)) {
                return $this->responseJson('File Excel rỗng', Response::HTTP_UNPROCESSABLE_ENTITY);
            }

            // Detect header row
            $headerRowIndex = null;
            $columnMap = [];
            $codeAliases = ['mã', 'mã hàng hoá', 'ma hang hoa', 'code'];
            $estAliases = ['giá nhập', 'đơn giá nhập', 'gia nhap', 'estimated price'];
            $quotedAliases = ['giá bán', 'đơn giá bán', 'gia ban', 'quoted price', 'sale price'];
            $vatAliases = ['vat(%)', 'vat', 'thuế vat(%)', 'thuế gtgt(%)'];

            foreach ($sheet as $ri => $row) {
                $mapped = [];
                foreach ($row as $ci => $cell) {
                    $val = mb_strtolower(trim((string)($cell ?? '')));
                    if (in_array($val, $codeAliases)) $mapped['code'] = $ci;
                    if (in_array($val, $estAliases)) $mapped['estimated_price'] = $ci;
                    if (in_array($val, $quotedAliases)) $mapped['quoted_price'] = $ci;
                    if (in_array($val, $vatAliases)) $mapped['vat_percent'] = $ci;
                }
                if (isset($mapped['code'])) {
                    $headerRowIndex = $ri;
                    $columnMap = $mapped;
                    break;
                }
            }

            if ($headerRowIndex === null) {
                return $this->responseJson('Không tìm thấy header hợp lệ (cần cột "Mã" hoặc "Mã hàng hoá")', Response::HTTP_UNPROCESSABLE_ENTITY);
            }

            // Build code→product map from BOM
            $bomProducts = $quotation->bomList->products->keyBy('code');

            // Build code→price map from existing quotation prices
            $existingPrices = $quotation->productPrices->keyBy('bom_list_product_id');

            // Detect parents that have children (để skip import giá cha)
            $parentIds = $quotation->bomList->products
                ->whereNotNull('parent_id')
                ->pluck('parent_id')
                ->unique()
                ->toArray();

            $matched = 0;
            $updated = 0;
            $unmatchedCodes = [];
            $total = 0;

            // Collect last-write-wins per code
            $importData = [];
            for ($ri = $headerRowIndex + 1; $ri < count($sheet); $ri++) {
                $row = $sheet[$ri];
                $code = trim((string)($row[$columnMap['code']] ?? ''));
                if (empty($code)) continue;
                // Skip group rows (Roman numerals: I, II, III, IV, etc.)
                if (preg_match('/^[IVXLCDM]+\.?$/i', $code)) continue;

                $total++;
                $importData[$code] = $row;
            }

            foreach ($importData as $code => $row) {
                $product = $bomProducts->get($code);
                if (!$product) {
                    $unmatchedCodes[] = $code;
                    continue;
                }

                $matched++;

                // Skip parent-with-children (giá roll-up từ con)
                if (in_array((int)$product->id, $parentIds)) continue;

                $updateFields = [];
                if (isset($columnMap['estimated_price'])) {
                    $val = $row[$columnMap['estimated_price']] ?? null;
                    if ($val !== null && $val !== '' && is_numeric($val) && (float)$val >= 0) {
                        $updateFields['estimated_price'] = (float)$val;
                    }
                }
                if (isset($columnMap['quoted_price'])) {
                    $val = $row[$columnMap['quoted_price']] ?? null;
                    if ($val !== null && $val !== '' && is_numeric($val) && (float)$val >= 0) {
                        $updateFields['quoted_price'] = (float)$val;
                    }
                }
                if (isset($columnMap['vat_percent'])) {
                    $val = $row[$columnMap['vat_percent']] ?? null;
                    if ($val !== null && $val !== '' && is_numeric($val) && (float)$val >= 0 && (float)$val <= 100) {
                        $updateFields['vat_percent'] = (float)$val;
                    }
                }

                if (!empty($updateFields)) {
                    \Modules\Assign\Entities\QuotationProductPrice::updateOrCreate(
                        [
                            'quotation_id' => $quotation->id,
                            'bom_list_product_id' => $product->id,
                        ],
                        $updateFields
                    );
                    $updated++;
                }
            }

            if ($matched === 0) {
                return $this->responseJson('Không có mã hàng hoá nào khớp với báo giá', Response::HTTP_UNPROCESSABLE_ENTITY);
            }

            // Recompute totals
            $this->service->publicRecomputeTotals($quotation);

            return response()->json([
                'message' => 'Import thành công',
                'total' => $total,
                'matched' => $matched,
                'updated' => $updated,
                'unmatched' => count($unmatchedCodes),
                'unmatched_codes' => $unmatchedCodes,
            ]);
        } catch (\Illuminate\Validation\ValidationException $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_UNPROCESSABLE_ENTITY);
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
    ```

[x] Task 3: QuotationService — expose recomputeTotals dạng public
  - File: `Modules/Assign/Services/QuotationService.php`
  - Thêm method public wrapper (giữ private `recomputeTotals` nguyên):
    ```php
    public function publicRecomputeTotals(Quotation $quotation): void
    {
        $this->recomputeTotals($quotation);
    }
    ```

[x] Task 4: Tạo EmptyImport class
  - File: `app/Imports/EmptyImport.php`
  - Kiểm tra nếu đã tồn tại (BomList import có thể đã tạo). Nếu chưa:
    ```php
    <?php
    namespace App\Imports;
    use Maatwebsite\Excel\Concerns\WithoutHeadingRow;
    class EmptyImport implements WithoutHeadingRow {}
    ```

#### 19.2 FE — Button Xuất Excel + Import Excel + Modal

[x] Task 5: Thêm 2 button vào header bảng sản phẩm
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - Sửa div.products-title (line ~141) từ:
    ```html
    <div class="products-title">
        <i class="ri-list-check-2 mr-1"></i>Chi tiết sản phẩm — sửa giá
    </div>
    ```
    thành:
    ```html
    <div class="products-title d-flex align-items-center">
        <span><i class="ri-list-check-2 mr-1"></i>Chi tiết sản phẩm — sửa giá</span>
        <span class="ml-auto d-flex" style="gap:6px">
            <V2BaseButton light size="sm" @click="exportExcel">
                <template #prefix><i class="ri-file-excel-2-line mr-1"></i></template>
                Xuất Excel
            </V2BaseButton>
            <V2BaseButton v-if="canEdit" light size="sm" @click="importModalShow = true">
                <template #prefix><i class="ri-upload-2-line mr-1"></i></template>
                Import Excel
            </V2BaseButton>
        </span>
    </div>
    ```

[x] Task 6: Thêm modal import V2BaseImportModal + extra-config (chọn dòng tiêu đề)
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - Thêm sau `</VatFirstEntryPromptModal>` (line ~375):
    ```html
    <!-- Phase 19: Modal import giá từ Excel -->
    <b-modal
        v-model="importModalShow"
        title="Import giá từ Excel"
        centered
        size="lg"
        ok-title="Import"
        cancel-title="Huỷ"
        :ok-disabled="!importFile || importing"
        @ok.prevent="handleImportPrices"
        @hidden="resetImportModal"
    >
        <div class="alert alert-warning py-2 mb-3">
            <i class="ri-error-warning-line mr-1"></i>
            <strong>Lưu ý:</strong> Thao tác này sẽ thay thế toàn bộ giá nhập, giá bán và thuế VAT hiện tại.
            Giá trị rỗng trong file sẽ được bỏ qua (giữ nguyên giá cũ).
        </div>
        <div class="form-group">
            <label class="font-weight-bold">Chọn file Excel (.xlsx, .xls)</label>
            <input
                ref="importFileInput"
                type="file"
                class="form-control-file"
                accept=".xlsx,.xls"
                @change="onImportFileChange"
            />
        </div>
        <div v-if="importResult" class="mt-3">
            <div class="alert py-2" :class="importResult.unmatched > 0 ? 'alert-info' : 'alert-success'">
                <div>Tổng dòng: {{ importResult.total }} | Khớp: {{ importResult.matched }} | Đã cập nhật: {{ importResult.updated }}</div>
                <div v-if="importResult.unmatched > 0" class="mt-1">
                    <strong>Không tìm thấy ({{ importResult.unmatched }}):</strong>
                    {{ importResult.unmatched_codes.join(', ') }}
                </div>
            </div>
        </div>
        <div v-if="importing" class="text-center py-2">
            <b-spinner small class="mr-1"></b-spinner> Đang import...
        </div>
    </b-modal>
    ```

[x] Task 7: Thêm data + methods cho export/import (validate + import API JSON-based)
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - Trong `data()`, thêm:
    ```js
    importModalShow: false,
    importFile: null,
    importing: false,
    importResult: null,
    ```
  - Trong `methods`, thêm:
    ```js
    async exportExcel() {
        try {
            const res = await this.$store.dispatch('apiGetMethod', {
                url: `assign/quotations/${this.quotationId}/export-excel`,
                responseType: 'blob',
            })
            const url = window.URL.createObjectURL(new Blob([res]))
            const a = document.createElement('a')
            a.href = url
            a.download = `BaoGia_${this.item.code || 'export'}.xlsx`
            a.click()
            window.URL.revokeObjectURL(url)
        } catch (e) {
            // Fallback: mở URL trực tiếp (API trả file download)
            const baseUrl = this.$axios?.defaults?.baseURL || ''
            const token = this.$store?.state?.token || ''
            window.open(`${baseUrl}/assign/quotations/${this.quotationId}/export-excel?token=${token}`, '_blank')
        }
    },
    onImportFileChange(e) {
        this.importFile = e.target.files[0] || null
        this.importResult = null
    },
    resetImportModal() {
        this.importFile = null
        this.importResult = null
        this.importing = false
    },
    async handleImportPrices() {
        if (!this.importFile) return
        this.importing = true
        this.importResult = null
        try {
            const formData = new FormData()
            formData.append('file', this.importFile)
            const res = await this.$store.dispatch('apiPostMethod', {
                url: `assign/quotations/${this.quotationId}/import-prices`,
                payload: formData,
            })
            this.importResult = res?.data || res
            this.$toasted?.global?.success?.({
                message: `Import thành công: ${this.importResult.updated || 0} dòng đã cập nhật`,
            })
            // Reload data để FE đồng bộ
            await this.fetchData()
        } catch (e) {
            const msg = e?.response?.data?.message || 'Lỗi import'
            this.$toasted?.global?.error?.({ message: msg })
        } finally {
            this.importing = false
        }
    },
    ```

#### 19.3 Test thủ công

[ ] Task 8: Test xuất Excel
  - Mở /assign/quotations/{id}/edit (status = Đang tạo)
  - Click "Xuất Excel" → file .xlsx download được
  - Mở file → có đủ cột: STT, Mã, Tên hàng, SL, ĐVT, Giá nhập, Thành tiền nhập, Giá bán, Thành tiền bán, Tỷ suất LN, VAT%, Tiền VAT, Thành tiền sau VAT
  - Data khớp với giá trên màn hình

[ ] Task 9: Test import Excel — happy path
  - Xuất Excel → mở file → sửa giá nhập + giá bán + VAT% ở vài dòng → lưu
  - Click "Import Excel" → chọn file vừa sửa → click Import
  - Toast success hiện ra
  - Giá trên màn hình đã cập nhật đúng theo file

[ ] Task 10: Test import — edge cases
  - Import file có mã không tồn tại → hiện unmatched_codes
  - Import file có giá trị rỗng → giữ nguyên giá cũ
  - Import file không có header → hiện lỗi 422
  - Import khi báo giá status != 1 → button Import không hiện (FE) / API trả lỗi 422 (BE)
  - Import file có row cha (có con) → giá cha bị bỏ qua, sau reload FE tự roll-up từ con

### Phase 20: Fix & cải thiện Báo giá — Excel + Hyperlink + Import nhóm (2026-05-09)

#### 20.1 Hyperlink thông tin chung
[x] Task 1: Thêm hyperlink Dự án → /assign/prospective-projects/{id} (target="_blank")
  - File: `_id/edit.vue` + `_id/index.vue` (cả màn sửa + xem)
[x] Task 2: Thêm hyperlink Giải pháp → /assign/solutions/{id} (target="_blank")
  - File: `_id/edit.vue` + `_id/index.vue`

#### 20.2 Fix xuất Excel báo giá (export thường + template)
[x] Task 3: Bổ sung cột Tỷ suất lợi nhuận vào default fields
  - File: `QuotationController::exportExcel` — thêm `profit_margin` vào $fields
[x] Task 4: Đổi thứ tự cột Mã hàng hoá lên trước Tên hàng hoá
  - File: `bom_list.blade.php` — sửa tất cả 6 block (header, grouped parent/child, ungrouped parent/child, footer)
  - File: `QuotationController::exportExcel` — đổi thứ tự $fields
[x] Task 5: Fix data Mã/Tên bị đảo ở block ungrouped
  - Root cause: `replace_all` chỉ match block grouped (indentation khác) → 2 block ungrouped vẫn name trước code
[x] Task 6: Fix thiếu VAT hàng hoá con trong export
  - File: `bom_list.blade.php` — child rows render giá trị `vat_percent` thay vì blank
  - File: `QuotationController::exportExcel` — bỏ force `vat_percent = 0` cho child products

#### 20.3 File mẫu import riêng
[x] Task 7: Tạo endpoint GET /export-import-template riêng cho file mẫu
  - File: `QuotationController::exportImportTemplate` — fields không có profit_margin/vat_amount/after_vat
  - File: `api.php` — thêm route
[x] Task 8: Bỏ dòng tổng cộng trong file mẫu
  - File: `bom_list.blade.php` — bọc `<tfoot>` trong `@if(!($templateMode ?? false))`
[x] Task 9: Khoá cột không cho sửa, trừ Giá nhập / Giá bán / VAT
  - File: `BomListExport.php` — thêm `withTemplateMode()`: sheet protection + unlock 3 cột editable
[x] Task 10: Cột Thành tiền nhập/bán dùng công thức Excel (=Đơn giá × Số lượng)
  - File: `BomListExport.php` — AfterSheet set formula cho cột import_amount + amount, skip dòng nhóm (STT trống)
[x] Task 11: FE gọi endpoint template riêng thay vì reuse exportExcel
  - File: `edit.vue` — `handleDownloadImportTemplate()` gọi `/export-import-template`

#### 20.4 Popup import — cải thiện preview
[x] Task 12: Thêm 2 cột computed: Thành tiền nhập, Thành tiền bán (SL × Giá)
  - File: `V2BaseImportTable.vue` — thêm type `computed` (render text thuần, gọi `col.compute(row)`)
  - File: `edit.vue` — thêm 2 cột computed vào importColumns
  - File: `import-helper.js` — skip cột computed khi check headers, parse data, check blank rows
  - File: `V2BaseImportModal.vue` — skip cột computed khi build dataRows gửi server

#### 20.5 Import xử lý nhóm hàng
[x] Task 13: BE nhận diện row nhóm (STT La Mã) — skip validate Code/giá
  - File: `QuotationController::validateImportPrices` — check `isRomanNumeral`, validate tên nhóm khớp BOM
[x] Task 14: BE importPrices skip row nhóm
  - File: `QuotationController::importPrices` — thêm check La Mã trước khi xử lý
[x] Task 15: Blade render nhóm vào đúng cell (không colspan)
  - File: `bom_list.blade.php` — row nhóm render STT (La Mã) + Name riêng biệt thay vì colspan gộp
[x] Task 16: FE preview — row nhóm bỏ input, background riêng
  - File: `V2BaseImportTable.vue` — thêm props `isGroupRow` + `groupDisplayKeys`, render row nhóm text thuần, background #e8f4fd
  - File: `V2BaseImportModal.vue` — forward 2 props
  - File: `edit.vue` — truyền `isImportGroupRow` (check La Mã) + `groupDisplayKeys: ['STT', 'Name']`

#### 20.6 Test thủ công
[ ] Task 17: Test xuất Excel — cột đúng thứ tự (Mã trước Tên), có VAT con, có Tỷ suất LN
[ ] Task 18: Test file mẫu — bỏ tổng, lock cột, công thức thành tiền, nhóm render đúng cell
[ ] Task 19: Test import từ file mẫu — nhóm validate tên, hàng hoá validate giá, preview đúng
[ ] Task 20: Test hyperlink Dự án + Giải pháp — click mở tab mới

### Phase 21: Dịch vụ bổ sung + Đảo logic cha-con + Làm tròn (2026-05-09)

> **Spec:** docs/superpowers/specs/2026-05-09-quotation-phase21-design.md
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Cho phép thêm dòng dịch vụ bổ sung trên báo giá, đảo logic giá cha-con (giá bán+VAT nhập ở cha), thêm làm tròn đơn giá.

#### 21.1 BE — Migration + Entity dịch vụ bổ sung

- [x] Task 1: Tạo migration bảng `quotation_service_items`
  - File tạo: `hrm-api/database/migrations/2026_05_09_000001_create_quotation_service_items_table.php`
  - Schema theo spec 2.1: id, quotation_id (FK cascade), code(50), name, unit_id, qty, estimated_price, quoted_price, vat_percent, note, sort_order, created_by, updated_by, timestamps
  - Index trên quotation_id

- [x] Task 2: Tạo Entity `QuotationServiceItem`
  - File tạo: `hrm-api/Modules/Assign/Entities/QuotationServiceItem.php`
  - fillable: quotation_id, code, name, unit_id, qty, estimated_price, quoted_price, vat_percent, note, sort_order, created_by, updated_by
  - casts: qty, estimated_price, quoted_price, vat_percent → decimal:2
  - appends: import_total, sale_total, vat_amount, after_vat (accessors tính toán)
  - relations: quotation() → belongsTo Quotation, unit() → belongsTo Unit
  - static `getNextCode($quotationCode)`: tìm max code `DV-{quotationCode}-%` → +1 → format `DV-{code}-{NNN}`

- [x] Task 3: Thêm relation `serviceItems()` vào Quotation entity
  - File sửa: `hrm-api/Modules/Assign/Entities/Quotation.php` (sau line ~108)
  - `return $this->hasMany(QuotationServiceItem::class)->orderBy('sort_order');`

#### 21.2 BE — CRUD API dịch vụ bổ sung

- [x] Task 4: Thêm 3 routes cho service items
  - File sửa: `hrm-api/Modules/Assign/Routes/api.php` (trong group quotations, sau line 384)
  ```php
  Route::post('/{id}/service-items', [QuotationController::class, 'storeServiceItem']);
  Route::put('/{id}/service-items/{itemId}', [QuotationController::class, 'updateServiceItem']);
  Route::delete('/{id}/service-items/{itemId}', [QuotationController::class, 'deleteServiceItem']);
  ```

- [x] Task 5: Controller method `storeServiceItem()`
  - File sửa: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`
  - Validate: quotation status = STATUS_DANG_TAO, name required|max:255, qty numeric|min:0.01, estimated_price numeric|min:0, quoted_price numeric|min:0, vat_percent numeric|min:0|max:100, unit_id nullable|exists:units,id, note nullable
  - Auto-gen code via `QuotationServiceItem::getNextCode($quotation->code)`
  - Create QuotationServiceItem với created_by = auth user
  - Gọi `$this->service->publicRecomputeTotals($quotation)`
  - Return item với unit relation

- [x] Task 6: Controller method `updateServiceItem()`
  - File sửa: `QuotationController.php`
  - Validate tương tự storeServiceItem
  - Validate item thuộc quotation: `$quotation->serviceItems()->findOrFail($itemId)`
  - Update fields, updated_by = auth user
  - Gọi recomputeTotals
  - Return item

- [x] Task 7: Controller method `deleteServiceItem()`
  - File sửa: `QuotationController.php`
  - Validate status = STATUS_DANG_TAO
  - `$quotation->serviceItems()->findOrFail($itemId)->delete()`
  - Gọi recomputeTotals
  - Return success message

#### 21.3 BE — Cập nhật show + update để xử lý service items

- [x] Task 8: Eager load serviceItems trong show()
  - File sửa: `QuotationController.php` line 73
  - Thêm `'serviceItems.unit'` vào mảng with():
  ```php
  $item = Quotation::with([
      'pricingRequest', 'bomList', 'project', 'solution', 'solutionVersion',
      'solutionModule', 'solutionModuleVersion', 'currency', 'creator.info',
      'tpApprover.info', 'approver.info', 'serviceItems.unit',
  ])->findOrFail($id);
  ```

- [x] Task 9: Sửa QuotationService::update() để sync service_items
  - File sửa: `hrm-api/Modules/Assign/Services/QuotationService.php`
  - Trong method update(), sau khi xử lý products, thêm xử lý `$data['service_items']`:
  ```php
  if (isset($data['service_items'])) {
      $existingIds = $quotation->serviceItems()->pluck('id')->toArray();
      $incomingIds = collect($data['service_items'])->pluck('id')->filter()->toArray();
      
      // Delete removed items
      $toDelete = array_diff($existingIds, $incomingIds);
      if (!empty($toDelete)) {
          QuotationServiceItem::whereIn('id', $toDelete)
              ->where('quotation_id', $quotation->id)
              ->delete();
      }
      
      // Upsert
      foreach ($data['service_items'] as $i => $itemData) {
          if (!empty($itemData['id'])) {
              $item = $quotation->serviceItems()->find($itemData['id']);
              if ($item) {
                  $item->update(array_merge($itemData, [
                      'sort_order' => $i,
                      'updated_by' => auth()->id(),
                  ]));
              }
          } else {
              QuotationServiceItem::create(array_merge($itemData, [
                  'quotation_id' => $quotation->id,
                  'code' => QuotationServiceItem::getNextCode($quotation->code),
                  'sort_order' => $i,
                  'created_by' => auth()->id(),
              ]));
          }
      }
  }
  ```

#### 21.4 BE — Đảo logic computeTotals (giá bán cha trực tiếp)

- [x] Task 10: Sửa `computeTotals()` — bỏ roll-up giá bán từ con
  - File sửa: `hrm-api/Modules/Assign/Services/QuotationService.php` lines 233-281
  - Thay đổi: bỏ block `if ($hasChildren)` roll-up lineSale từ con, thay bằng:
  ```php
  // MỚI: luôn dùng trực tiếp quoted_price × qty (giá bán nhập ở cha)
  $pQty = (float) ($p->qty_needed ?? 0);
  $lineSale = ($price ? (float) $price->quoted_price : 0) * $pQty;
  ```
  - Giữ nguyên logic skip children (parent_id check)
  - Giữ nguyên VAT calculation

- [x] Task 11: Thêm service items vào computeTotals()
  - File sửa: `QuotationService.php` — sau vòng foreach products, trước return
  ```php
  // Cộng dịch vụ bổ sung
  foreach ($quotation->serviceItems as $item) {
      $totalSale += (float) $item->quoted_price * (float) $item->qty;
      $totalVat += (float) $item->quoted_price * (float) $item->qty * (float) $item->vat_percent / 100;
  }
  ```

#### 21.5 BE — Export Excel cập nhật

- [x] Task 12: BomListExport — thêm support serviceItems
  - File sửa: `hrm-api/app/ExcelExport/BomListExport.php`
  - Thêm property `protected $serviceItems = [];`
  - Thêm method:
  ```php
  public function withServiceItems($items): self
  {
      $this->serviceItems = $items;
      return $this;
  }
  ```
  - Trong `view()`: truyền thêm `'serviceItems' => $this->serviceItems` vào data array

- [x] Task 13: bom_list.blade.php — thêm section dịch vụ bổ sung + bỏ giá bán/VAT con
  - File sửa: `hrm-api/resources/views/exports/bom_list.blade.php`
  - **Child rows**: set quoted_price, vat_percent, vat_amount, after_vat = '' (để trống)
    - Lines ~134-154 (grouped) và ~200-220 (ungrouped): thay `$child->quoted_price` → `''`, `$child->vat_percent` → `''`
  - **Section dịch vụ bổ sung**: chèn trước `<tfoot>`, sau block grouped/ungrouped:
  ```blade
  @if(count($serviceItems ?? []) > 0)
  <tr>
      <td colspan="{{ count($fieldMap) }}" style="font-weight:bold; background-color:#f0f0f0;">
          Dịch vụ bổ sung
      </td>
  </tr>
  @foreach($serviceItems as $si => $item)
  <tr>
      @foreach($fieldMap as $key => $label)
          @if($key === 'stt')
              <td>{{ $si + 1 }}</td>
          @elseif($key === 'code')
              <td>{{ $item->code }}</td>
          @elseif($key === 'name')
              <td>{{ $item->name }}</td>
          @elseif($key === 'qty')
              <td>{{ $item->qty }}</td>
          @elseif($key === 'unit')
              <td>{{ $item->unit->name ?? '' }}</td>
          @elseif($key === 'estimated_price')
              <td>{{ $item->estimated_price }}</td>
          @elseif($key === 'import_amount')
              <td>{{ $item->import_total }}</td>
          @elseif($key === 'sale_price')
              <td>{{ $item->quoted_price }}</td>
          @elseif($key === 'amount')
              <td>{{ $item->sale_total }}</td>
          @elseif($key === 'profit_margin')
              <td>{{ $item->quoted_price > 0 ? round(($item->quoted_price - $item->estimated_price) / $item->quoted_price * 100, 2) : 0 }}%</td>
          @elseif($key === 'vat_percent')
              <td>{{ $item->vat_percent }}</td>
          @elseif($key === 'vat_amount')
              <td>{{ $item->vat_amount }}</td>
          @elseif($key === 'after_vat')
              <td>{{ $item->after_vat }}</td>
          @else
              <td></td>
          @endif
      @endforeach
  </tr>
  @endforeach
  @endif
  ```

- [ ] Task 14: QuotationController::exportExcel — truyền serviceItems + bỏ roll-up cha
  - File sửa: `QuotationController.php` lines 224-303
  - Bỏ block roll-up quoted_price cha từ con (lines ~263-274)
  - Hàng hoá con: set `quoted_price = null`, `vat_percent = null` trong product object
  - Load serviceItems: `$quotation->load('serviceItems.unit')`
  - Truyền: `->withServiceItems($quotation->serviceItems)`

- [ ] Task 15: QuotationController::exportImportTemplate — cập nhật tương tự
  - File sửa: `QuotationController.php` lines 305-345
  - Tương tự Task 14: bỏ roll-up, con blank giá bán/VAT, truyền serviceItems
  - Template mode: unlock giá bán+VAT cho cha (thay vì con), lock cho con

- [ ] Task 16: BomListExport — đảo lock/unlock cha-con trong templateMode
  - File sửa: `BomListExport.php` registerEvents() lines 163-207
  - Hiện tại: unlock estimated_price, sale_price, vat_percent cho child rows
  - Mới: unlock estimated_price cho child + orphan, unlock sale_price + vat_percent cho parent + orphan
  - Lock sale_price + vat_percent cho child rows

#### 21.6 BE — Import prices cập nhật

- [ ] Task 17: Sửa validateImportPrices — đảo validate cha-con + nhận DV-*
  - File sửa: `QuotationController.php` lines 372-611
  - **Pass 1 thay đổi:**
    - Dòng mã `DV-*`: validate tồn tại trong `$quotation->serviceItems`, validate giá nhập/bán/VAT numeric ≥ 0
    - Hàng hoá cha (có con): validate quoted_price + vat_percent (editable), skip estimated_price
    - Hàng hoá con: validate estimated_price only, skip quoted_price + vat_percent
  - **Pass 2 thay đổi:**
    - Bỏ validate parent sale total = SUM(children sale)
    - Bỏ validate parent VAT = MAX(children VAT)
    - Giữ validate parent import total = SUM(children import) (hoặc bỏ nếu muốn đơn giản)

- [ ] Task 18: Sửa importPrices — đảo import fields + nhận DV-*
  - File sửa: `QuotationController.php` lines 613-698
  - **Cha (có con):** update quoted_price + vat_percent (KHÔNG update estimated_price — roll-up)
  - **Con:** update estimated_price only (KHÔNG update quoted_price, vat_percent)
  - **Orphan:** update cả 3 (giữ nguyên)
  - **Dòng DV-*:** tìm trong serviceItems theo code, update estimated_price + quoted_price + vat_percent
  - Sau import: gọi recomputeTotals (đã có)

#### 21.7 FE — Đảo logic giá cha-con

- [ ] Task 19: Sửa `refreshParentRollups()` — bỏ roll-up giá bán + VAT
  - File sửa: `hrm-client/pages/assign/quotations/_id/edit.vue` lines 690-712
  - Bỏ 2 dòng:
    - `p.quoted_price = parentQty > 0 ? sumQuoted / parentQty : 0` (line ~709)
    - `p.vat_percent = maxVat` (line ~710)
  - Giữ nguyên roll-up estimated_price

- [ ] Task 20: Sửa `lineSaleTotal()` — cha dùng trực tiếp thay vì SUM con
  - File sửa: `edit.vue` lines 658-663
  - Thay đổi:
  ```javascript
  lineSaleTotal(p) {
      // Luôn dùng trực tiếp, kể cả cha có con
      return (Number(p.quoted_price) || 0) * (Number(p.qty_needed) || 0)
  }
  ```

- [ ] Task 21: Template — cha editable giá bán + VAT, con disable
  - File sửa: `edit.vue`
  - **Parent rows (lines ~207-222):**
    - `estimated_price`: giữ disabled (roll-up)
    - `quoted_price`: BỎ disabled → cho nhập tay
    - `vat_percent`: BỎ disabled → cho nhập tay
  - **Child rows (lines ~257-276):**
    - `estimated_price`: giữ editable
    - `quoted_price`: THÊM disabled, hiện "—" hoặc giá trị nhưng không cho sửa
    - `vat_percent`: THÊM disabled, hiện "—"

#### 21.8 FE — VAT đồng loạt bỏ con

- [ ] Task 22: Sửa `applyVatToProducts()` — skip children
  - File sửa: `edit.vue` lines 940-951
  - Thêm check `if (p.parent_id) return` ở đầu forEach:
  ```javascript
  applyVatToProducts(vatPercent, mode) {
      let count = 0
      this.products.forEach(p => {
          if (p.parent_id) return  // skip children
          if (mode === 'zero_only' && Number(p.vat_percent || 0) !== 0) return
          p.vat_percent = vatPercent
          p._lastVatValue = vatPercent
          count++
      })
      // Áp cho dịch vụ bổ sung (thêm sau khi có serviceItems)
      if (this.serviceItems) {
          this.serviceItems.forEach(s => {
              if (mode === 'zero_only' && Number(s.vat_percent || 0) !== 0) return
              s.vat_percent = vatPercent
          })
      }
      this.vatBulkKey++
      return count
  }
  ```

#### 21.9 FE — Dịch vụ bổ sung (section + modal + CRUD)

- [ ] Task 23: Thêm data properties cho service items
  - File sửa: `edit.vue` data()
  - Thêm:
  ```javascript
  serviceItems: [],
  showAddServiceModal: false,
  newServiceItem: {
      name: '', unit_id: null, qty: 1,
      estimated_price: 0, quoted_price: 0,
      vat_percent: 0, note: '',
  },
  savingServiceItem: false,
  ```

- [ ] Task 24: Load serviceItems từ API response
  - File sửa: `edit.vue` — trong fetchData() hoặc method xử lý API response
  - Sau khi load quotation: `this.serviceItems = this.item.service_items || []`

- [ ] Task 25: Template — Section "Dịch vụ bổ sung" cuối bảng
  - File sửa: `edit.vue` — sau tất cả grouped rows, trước footer tổng cộng
  ```html
  <!-- Section dịch vụ bổ sung -->
  <tr class="group-row">
      <td :colspan="totalColumns" class="font-weight-bold" style="background:#f0f0f0;">
          Dịch vụ bổ sung
          <V2BaseButton v-if="canEdit" light size="sm" class="ml-2"
              @click="showAddServiceModal = true">
              <template #prefix><i class="ri-add-line"></i></template>
              Thêm dịch vụ
          </V2BaseButton>
      </td>
  </tr>
  <tr v-for="(svc, si) in serviceItems" :key="'svc-' + svc.id" class="service-item-row">
      <td>{{ si + 1 }}</td>
      <td>{{ svc.code }}</td>
      <td>
          <input v-if="canEdit" v-model="svc.name"
              class="form-control form-control-sm" placeholder="Tên dịch vụ" />
          <span v-else>{{ svc.name }}</span>
      </td>
      <td>
          <input v-if="canEdit" v-model.number="svc.qty" type="number" min="0.01" step="0.01"
              class="form-control form-control-sm text-right" />
          <span v-else>{{ svc.qty }}</span>
      </td>
      <td><!-- ĐVT select --></td>
      <td>
          <input v-if="canEdit" v-model.number="svc.estimated_price" type="number" min="0"
              class="form-control form-control-sm text-right" />
          <span v-else>{{ formatMoney(svc.estimated_price) }}</span>
      </td>
      <td class="text-right">{{ formatMoney(svc.estimated_price * svc.qty) }}</td>
      <td>
          <input v-if="canEdit" v-model.number="svc.quoted_price" type="number" min="0"
              class="form-control form-control-sm text-right" />
          <span v-else>{{ formatMoney(svc.quoted_price) }}</span>
      </td>
      <td class="text-right">{{ formatMoney(svc.quoted_price * svc.qty) }}</td>
      <td class="text-right">
          {{ svc.quoted_price > 0 ? ((svc.quoted_price - svc.estimated_price) / svc.quoted_price * 100).toFixed(2) : 0 }}%
      </td>
      <td>
          <input v-if="canEdit" v-model.number="svc.vat_percent" type="number" min="0" max="100"
              class="form-control form-control-sm text-right" />
          <span v-else>{{ svc.vat_percent }}%</span>
      </td>
      <td class="text-right">{{ formatMoney(svc.quoted_price * svc.qty * svc.vat_percent / 100) }}</td>
      <td class="text-right">{{ formatMoney(svc.quoted_price * svc.qty * (1 + svc.vat_percent / 100)) }}</td>
      <td v-if="canEdit">
          <button class="btn btn-sm btn-outline-danger" @click="removeServiceItem(si)">
              <i class="ri-delete-bin-line"></i>
          </button>
      </td>
  </tr>
  ```

- [ ] Task 26: Modal thêm dịch vụ mới
  - File sửa: `edit.vue` — thêm `<b-modal>` sau các modal hiện tại
  ```html
  <b-modal v-model="showAddServiceModal" title="Thêm dịch vụ bổ sung"
      centered ok-title="Thêm" cancel-title="Huỷ"
      :ok-disabled="!newServiceItem.name || savingServiceItem"
      @ok.prevent="addServiceItem" @hidden="resetNewServiceItem">
      <div class="form-group">
          <label class="font-weight-bold">Tên dịch vụ <span class="text-danger">*</span></label>
          <input v-model="newServiceItem.name" class="form-control" placeholder="Nhập tên dịch vụ" />
      </div>
      <div class="row">
          <div class="col-6 form-group">
              <label>Số lượng</label>
              <input v-model.number="newServiceItem.qty" type="number" min="0.01" class="form-control" />
          </div>
          <div class="col-6 form-group">
              <label>Đơn vị tính</label>
              <!-- Select ĐVT từ master data -->
          </div>
      </div>
      <div class="row">
          <div class="col-6 form-group">
              <label>Đơn giá nhập</label>
              <input v-model.number="newServiceItem.estimated_price" type="number" min="0" class="form-control" />
          </div>
          <div class="col-6 form-group">
              <label>Đơn giá bán</label>
              <input v-model.number="newServiceItem.quoted_price" type="number" min="0" class="form-control" />
          </div>
      </div>
      <div class="row">
          <div class="col-6 form-group">
              <label>VAT (%)</label>
              <input v-model.number="newServiceItem.vat_percent" type="number" min="0" max="100" class="form-control" />
          </div>
      </div>
      <div class="form-group">
          <label>Ghi chú</label>
          <textarea v-model="newServiceItem.note" class="form-control" rows="2"></textarea>
      </div>
  </b-modal>
  ```

- [ ] Task 27: Methods CRUD dịch vụ
  - File sửa: `edit.vue` methods
  ```javascript
  async addServiceItem() {
      this.savingServiceItem = true
      try {
          const res = await this.$store.dispatch('apiPostMethod', {
              url: `assign/quotations/${this.quotationId}/service-items`,
              payload: this.newServiceItem,
          })
          this.serviceItems.push(res.data?.data || res.data)
          this.showAddServiceModal = false
          this.resetNewServiceItem()
          this.$toasted?.global?.success?.({ message: 'Đã thêm dịch vụ' })
      } catch (e) {
          this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi thêm dịch vụ' })
      } finally {
          this.savingServiceItem = false
      }
  },
  removeServiceItem(index) {
      const item = this.serviceItems[index]
      if (item.id) {
          // Confirm xoá
          this.$bvModal.msgBoxConfirm('Bạn có chắc muốn xoá dịch vụ này?', {
              title: 'Xác nhận xoá',
              okTitle: 'Xoá', cancelTitle: 'Huỷ', okVariant: 'danger',
          }).then(async (ok) => {
              if (!ok) return
              try {
                  await this.$store.dispatch('apiDeleteMethod', {
                      url: `assign/quotations/${this.quotationId}/service-items/${item.id}`,
                  })
                  this.serviceItems.splice(index, 1)
                  this.$toasted?.global?.success?.({ message: 'Đã xoá dịch vụ' })
              } catch (e) {
                  this.$toasted?.global?.error?.({ message: 'Lỗi xoá dịch vụ' })
              }
          })
      } else {
          this.serviceItems.splice(index, 1)
      }
  },
  resetNewServiceItem() {
      this.newServiceItem = {
          name: '', unit_id: null, qty: 1,
          estimated_price: 0, quoted_price: 0,
          vat_percent: 0, note: '',
      }
  },
  ```

#### 21.10 FE — Disable thông tin BOM kế thừa

- [ ] Task 28: Disable input tên/mã/SL/ĐVT dòng BOM + ẩn nút xoá
  - File sửa: `edit.vue` template
  - Các input tên, mã, SL, ĐVT của dòng BOM (cả cha/con/orphan): thêm `disabled`
  - Nút xoá row: thêm `v-if="false"` hoặc ẩn cho dòng BOM (phân biệt bằng `bom_list_product_id`)
  - Dòng dịch vụ bổ sung (Task 25): vẫn cho sửa + xoá

#### 21.11 FE — Làm tròn đơn giá

- [ ] Task 29: Thêm data + UI làm tròn
  - File sửa: `edit.vue`
  - Data: `roundingMode: null`
  - Template — thêm vào toolbar (cạnh VAT đồng loạt), chỉ hiện khi canEdit:
  ```html
  <div class="d-flex align-items-center ml-3" v-if="canEdit">
      <b-form-select v-model="roundingMode" size="sm" style="width:200px">
          <option :value="null" disabled>Chọn kiểu làm tròn</option>
          <option value="-1">Làm tròn hàng chục</option>
          <option value="0">Làm tròn số nguyên</option>
          <option value="1">Làm tròn 1 số thập phân</option>
      </b-form-select>
      <V2BaseButton light size="sm" class="ml-1" @click="confirmRounding"
          :disabled="roundingMode === null">
          <template #prefix><i class="ri-calculator-line mr-1"></i></template>
          Làm tròn
      </V2BaseButton>
  </div>
  ```

- [ ] Task 30: Methods confirmRounding + applyRounding
  - File sửa: `edit.vue` methods
  ```javascript
  confirmRounding() {
      const labels = { '-1': 'hàng chục', '0': 'số nguyên', '1': '1 số thập phân' }
      const label = labels[String(this.roundingMode)]
      this.$bvModal.msgBoxConfirm(
          `Bạn có chắc muốn làm tròn đến ${label} cho toàn bộ đơn giá? Thao tác này không thể hoàn tác.`,
          { title: 'Xác nhận làm tròn', okTitle: 'Làm tròn', cancelTitle: 'Huỷ' }
      ).then((ok) => {
          if (ok) this.applyRounding()
      })
  },
  applyRounding() {
      const precision = parseInt(this.roundingMode)
      const roundVal = (val, p) => {
          const factor = Math.pow(10, p)
          return Math.round(val * factor) / factor
      }
      this.products.forEach(p => {
          const isChild = !!p.parent_id
          const hasChildren = this.products.some(
              c => Number(c.parent_id) === Number(p.bom_list_product_id)
          )
          // Giá nhập: round cho con + orphan
          if (!hasChildren) {
              p.estimated_price = roundVal(parseFloat(p.estimated_price) || 0, precision)
          }
          // Giá bán: round cho cha + orphan (con không có giá bán)
          if (!isChild) {
              p.quoted_price = roundVal(parseFloat(p.quoted_price) || 0, precision)
          }
      })
      this.refreshParentRollups()
      // Dịch vụ bổ sung
      this.serviceItems.forEach(s => {
          s.estimated_price = roundVal(parseFloat(s.estimated_price) || 0, precision)
          s.quoted_price = roundVal(parseFloat(s.quoted_price) || 0, precision)
      })
      this.vatBulkKey++
      this.$toasted?.global?.success?.({ message: 'Đã làm tròn đơn giá' })
  },
  ```

#### 21.12 FE — Save gửi service_items + Tổng cộng gộp dịch vụ

- [ ] Task 31: Sửa save() — gửi service_items trong payload
  - File sửa: `edit.vue` lines 844-888
  - Trong payload, thêm:
  ```javascript
  service_items: this.serviceItems.map((s, i) => ({
      id: s.id || null,
      name: s.name,
      unit_id: s.unit_id,
      qty: s.qty,
      estimated_price: s.estimated_price,
      quoted_price: s.quoted_price,
      vat_percent: s.vat_percent,
      note: s.note,
      sort_order: i,
  })),
  ```

- [ ] Task 32: Sửa computed tổng cộng — gộp dịch vụ bổ sung
  - File sửa: `edit.vue`
  - Trong các computed/methods tính tổng (totalSale, totalImport, totalVat, totalAfterVat):
  ```javascript
  // Cộng thêm dịch vụ bổ sung
  this.serviceItems.forEach(s => {
      totalSale += (parseFloat(s.quoted_price) || 0) * (parseFloat(s.qty) || 0)
      totalImport += (parseFloat(s.estimated_price) || 0) * (parseFloat(s.qty) || 0)
      const svcLineSale = (parseFloat(s.quoted_price) || 0) * (parseFloat(s.qty) || 0)
      totalVat += svcLineSale * (parseFloat(s.vat_percent) || 0) / 100
  })
  ```

#### 21.13 FE — Trang xem chi tiết (show) cập nhật

- [ ] Task 33: index.vue — load + hiển thị serviceItems
  - File sửa: `hrm-client/pages/assign/quotations/_id/index.vue`
  - Data: thêm `serviceItems: []`
  - fetchData: `this.serviceItems = this.item.service_items || []`
  - Template: thêm section "Dịch vụ bổ sung" cuối bảng (readonly, tương tự edit nhưng không có input)

- [ ] Task 34: index.vue — đảo logic cha-con giống edit
  - File sửa: `index.vue`
  - Sửa `lineSaleTotal()` lines 589-594: bỏ SUM từ con, dùng trực tiếp `quoted_price × qty`
  - Template: con hiện "—" ở cột giá bán + VAT%
  - Tổng cộng: gộp dịch vụ bổ sung

#### 21.14 Test thủ công

- [ ] Task 35: Test thêm/sửa/xoá dịch vụ bổ sung
  - Mở báo giá status=Đang tạo → bấm "Thêm dịch vụ" → nhập thông tin → lưu
  - Dịch vụ hiện cuối bảng, mã DV-* tự sinh
  - Sửa inline giá → bấm Lưu → reload → giá đúng
  - Xoá dịch vụ → confirm → dịch vụ biến mất

- [ ] Task 36: Test BOM kế thừa không sửa được
  - Dòng BOM: tên/mã/SL/ĐVT disabled, không có nút xoá
  - Chỉ sửa được giá nhập (con/orphan), giá bán (cha/orphan), VAT (cha/orphan)

- [ ] Task 37: Test logic giá cha-con mới
  - Cha có con: giá bán + VAT% editable ở cha, disabled ở con
  - Sửa giá nhập con → giá nhập cha tự roll-up
  - Sửa giá bán cha → thành tiền bán tính đúng (giá bán × SL cha)
  - Orphan: tất cả editable

- [ ] Task 38: Test VAT đồng loạt
  - Áp VAT 10% → cha + orphan + dịch vụ bổ sung có VAT=10%, con không bị ảnh hưởng

- [ ] Task 39: Test làm tròn
  - Chọn "Làm tròn hàng chục" → confirm → đơn giá nhập/bán được round(-1)
  - Chọn "Làm tròn số nguyên" → giá round(0)
  - Chọn "Làm tròn 1 số thập phân" → giá round(1)
  - Giá = 0 không bị lỗi

- [ ] Task 40: Test export Excel
  - Xuất Excel → file có section "Dịch vụ bổ sung" cuối
  - Hàng hoá con: cột giá bán + VAT% trống
  - Tổng cộng gộp cả dịch vụ

- [ ] Task 41: Test import Excel
  - Import file: cha import giá bán + VAT, con import giá nhập, DV-* import đầy đủ
  - Validate đúng logic mới
  - Dòng không khớp → báo unmatched

- [ ] Task 42: Test trang xem chi tiết
  - Dịch vụ bổ sung hiện đúng
  - Con hiện "—" ở giá bán + VAT%
  - Tổng cộng đúng

#### 21.9 Bug fix — Session 2026-05-10

- [x] Task 43: Fix unit_id null sau import dịch vụ (cross-DB TpUnit resolution)
  - BE: `importPrices()` đổi `TpUnit::all()` sang `DB::connection('mysql2')->table()`
  - BE: `DetailQuotationResource` thêm `resolveServiceItems()` manual TpUnit lookup
  - BE: `validateImportPrices()` thêm validate `Đơn vị tính không được để trống` cho DV-*
  - FE: `validatePrices()` thêm check `!s.unit_id`

- [x] Task 44: Fix CKEditor duplicate instances khi toggle section
  - FE: `edit.vue` đổi `v-show="!bottomCollapsed"` → `v-if` cho CompactReviewEditor

- [x] Task 45: Chuẩn hoá format tiền tệ Việt Nam + cho nhập thập phân
  - FE: `V2BaseCurrencyInput.vue` rewrite formatCurrency/parseRawValue/onInput (dấu `.` ngăn cách hàng nghìn, dấu `,` thập phân)
  - FE: `edit.vue` `formatMoney` bỏ `Math.round()` → `Intl.NumberFormat('vi-VN')`

- [x] Task 46: Thêm row tổng cộng + format tiền trên popup import
  - FE: `V2BaseImportTable.vue` thêm `computedSummary` computed + summary row sticky

- [x] Task 47: Overhaul lịch sử báo giá theo pattern BomListLog
  - BE: `QuotationHistory.php` thêm ACTION_LABELS/ACTION_COLORS + accessors
  - BE: `QuotationController::histories()` thêm action_label/action_color/content
  - BE: `QuotationService::update()` rewrite snapshot BEFORE update, per-product price detail, strip HTML rich text
  - BE: `QuotationService::applyBulkVat()` thêm logHistory
  - BE: `QuotationController` thêm `logServiceHistory()` cho store/delete service items
  - FE: `QuotationHistoryModal.vue` rewrite matching BomListLogModal

- [x] Task 48: Fix popup import — row tổng cộng đè dòng đầu + thêm cột sau VAT + button chọn file
  - FE: `V2BaseImportTable.vue` fix sticky `top: 37px` → `40px`
  - FE: `edit.vue` importColumns thêm `_afterVatTotal` computed column
  - FE: `V2BaseImportToolbar.vue` đưa "Chọn file Excel" lên đầu + đổi `primary`

- [x] Task 49: Fix validate message lệch dòng trên popup import
  - BE: `validateImportPrices()` thêm `usort($rows, ...)` theo index trước khi trả response (service rows push pass 1, group+product push pass 2 → thứ tự xáo trộn)
  - FE: `handleValidateImport()` map 1:1 theo index (bỏ logic skip group rows sai)

### Phase 22: In báo giá (2026-05-10)

> **Spec:** .plans/Bomlist-Quotation/design-phase22.md

**Goal:** Button "In" trên trang chi tiết báo giá → chọn cột → preview → in (window.print). Hoàn toàn FE, không cần API mới.

#### 22.1 FE — Modal chọn cột (QuotationPrintConfigModal)

- [x] Task 1: Tạo component `QuotationPrintConfigModal.vue`
  - File tạo: `hrm-client/components/assign/quotation/QuotationPrintConfigModal.vue`
  - Props: `show` (Boolean)
  - Emit: `@preview(config)`, `@close`
  - UI: Danh sách 14 checkbox cột + checkbox "Chọn tất cả" + checkbox "Hiện hàng hoá cấp con"
  - Button "Xem trước" emit config: `{ selectedColumns: [...], includeChildren: Boolean }`

- [x] Task 2: Tích hợp vào trang show
  - File sửa: `hrm-client/pages/assign/quotations/_id/index.vue`
  - Import QuotationPrintConfigModal
  - Enable button "In" (bỏ `:disabled="true"` + tooltip)
  - Click "In" → mở modal config
  - Data: `showPrintConfig: false`, `printConfig: null`

#### 22.2 FE — Modal preview in (QuotationPrintPreview)

- [x] Task 3: Tạo component `QuotationPrintPreview.vue`
  - File tạo: `hrm-client/components/assign/quotation/QuotationPrintPreview.vue`
  - Props: `show`, `config`, `item`, `products`, `groups`, `serviceItems`, `companyHeader`, `salesEmployeeName`
  - Template: layout theo design-phase22.md (banner → header info → bảng → footer)
  - Bảng sản phẩm: render theo `config.selectedColumns`, nhóm La Mã, cha-con (toggle qua `config.includeChildren`)
  - Dịch vụ bổ sung: section cuối bảng
  - Footer: tổng cộng + VAT + sau VAT + điều khoản + ghi chú KD + chữ ký
  - Button: "In" (gọi printContent) + "Đóng"
  - Method `printContent()`: `window.print()` — CSS `@media print` ẩn mọi thứ trừ `.print-content`

- [x] Task 4: CSS print styles
  - File sửa: component QuotationPrintPreview.vue `<style>`
  - `@media print`: ẩn `.no-print`, ẩn modal backdrop/header/footer buttons
  - `@page { size: A4 landscape; margin: 10mm; }`
  - Table: border collapse, font-size 11px, th background #f5f5f5
  - Row nhóm: bold background nhạt
  - Row con: indent tên, text-muted cho cột giá bán/VAT (hiện "—")
  - Row tổng: bold border-top

- [x] Task 5: Tích hợp vào trang show
  - File sửa: `index.vue`
  - Import QuotationPrintPreview
  - Khi QuotationPrintConfigModal emit `@preview(config)` → set `printConfig = config`, mở preview modal
  - Truyền props: item, products, groups, serviceItems
  - `companyHeader`: computed từ `$store.state.employee_company.header` (nếu null → fallback `@/assets/images/info-tpe.jpg`)
  - `salesEmployeeName`: resolve `item.project.main_sale_employee_id` từ `$store.state.employees`

#### 22.3 FE — Logic render bảng

- [x] Task 6: Computed/methods render bảng in
  - File sửa: `QuotationPrintPreview.vue`
  - `filteredColumns`: lọc theo `config.selectedColumns`
  - `groupedData`: transform products → grouped (reuse logic tương tự index.vue)
  - `getChildren(parent)`: trả children nếu `config.includeChildren`, else rỗng
  - `lineSaleTotal(p)`: `quoted_price × qty_needed` (cha dùng trực tiếp)
  - `lineVatAmount(p)`: `lineSaleTotal × vat_percent / 100`
  - `lineAfterVat(p)`: `lineSaleTotal + lineVatAmount`
  - `formatMoney(v)`: `Intl.NumberFormat('vi-VN')`
  - `stripHtml(html)`: remove HTML tags cho cột thông số kỹ thuật
  - `totalSale`, `totalVat`, `totalAfterVat`: computed gộp sản phẩm + dịch vụ

- [x] Task 7: Render header thông tin
  - Banner: `<img :src="companyHeader" />`
  - Bảng 2 cột thông tin (kính gửi, tên đơn vị, địa chỉ... | mã BG, dự án, ngày, ĐDKD...)
  - Dòng intro: "Chúng tôi xin gửi đến quý khách hàng..."

- [x] Task 8: Render footer
  - Điều khoản thanh toán (v-html stripped)
  - Ghi chú kinh doanh (v-html stripped)
  - Block chữ ký: "Ngày {dd} Tháng {mm} Năm {yyyy}" + "ĐẠI DIỆN KINH DOANH" + tên NVKD

#### 22.4 Test thủ công

- [ ] Task 9: Test chọn cột
  - Mở modal → bỏ chọn vài cột → preview → bảng chỉ hiện cột đã chọn
  - "Chọn tất cả" toggle đúng
  - Không chọn cột nào → warning

- [ ] Task 10: Test preview + in
  - Preview hiển thị đúng layout (banner, header, bảng, footer)
  - Bấm "In" → browser print dialog mở
  - Chỉ nội dung báo giá hiện trên bản in (ẩn sidebar, topbar, buttons)

- [ ] Task 11: Test cấp con
  - Bật "Hiện cấp con" → con hiện dưới cha (STT 1.1, 1.2...)
  - Tắt → chỉ hiện cha + orphan

- [ ] Task 12: Test dịch vụ bổ sung + tổng
  - Dịch vụ hiện cuối bảng
  - Tổng cộng + VAT + sau VAT đúng (gộp sản phẩm + DV)

#### 22.5 FE — Tích hợp trang danh sách + Fix bugs

- [x] Task 13: Thêm button In trên trang danh sách báo giá
  - File sửa: `hrm-client/pages/assign/quotations/index.vue`
  - Button ri-printer-line trong row-actions
  - Method `openPrintConfig(item)`: gọi API lấy chi tiết báo giá → mở modal config
  - Import QuotationPrintConfigModal + QuotationPrintPreview

- [x] Task 14: Fix lỗi in từ trang show
  - Fix blank page: chuyển từ `@media print` sang `window.open()` approach (mở cửa sổ mới với HTML+CSS inline)
  - Fix Chrome print dialog không mở: dùng `setTimeout(300)` thay `onload`
  - Fix footer chữ ký lặp mỗi trang: đổi `<tfoot>` sang `<tbody>`
  - Fix nhóm + dịch vụ mất border: xóa `border-left/right: none` trên `.group-row td`
  - Fix header image mất khi in

- [x] Task 15: Fix lỗi 404 trang danh sách
  - Nguyên nhân: `QuotationPrintPreview` render khi `item=null` → crash cả trang
  - Fix: thêm `v-if="item"` trên `<b-modal>`

- [x] Task 16: Fix API call trang danh sách
  - Nguyên nhân: `apiGetMethod` nhận string URL, không nhận object `{ url: ... }`
  - Fix: đổi `dispatch('apiGetMethod', { url: ... })` → `dispatch('apiGetMethod', 'assign/quotations/${item.id}')`

- [x] Task 17: Đưa button In lên header modal preview
  - Chuyển button In từ footer lên `#modal-title` slot
  - Xóa footer buttons (Đóng + In)

#### 22.6 Sửa công thức tỷ suất LN + Cảnh báo DV

- [x] Task 18: Sửa công thức tỷ suất LN toàn bộ codebase (7 chỗ)
  - Công thức chuẩn: (thành_tiền_bán - thành_tiền_nhập) / thành_tiền_nhập × 100 (mẫu số = NHẬP)
  - BE QuotationService.php:462 — /totalSale → /totalImport
  - BE QuotationController.php:257 — /quoted → /est
  - FE edit.vue: marginPercent (line 697) /totalSale → /totalImport
  - FE edit.vue: lineMarginPercent (line 812) /sale → /imp
  - FE edit.vue: service inline margin (line 321) /svc.quoted_price → /svc.estimated_price
  - FE index.vue: marginPercent (line 562) /totalSale → /totalImport
  - FE index.vue: lineMarginPercent (line 672) /sale → /imp
  - FE index.vue: svcMarginPercent (line 678) /sale → /imp

- [x] Task 19: Thêm cảnh báo màu tỷ suất LN cho dịch vụ bổ sung (edit)
  - File sửa: edit.vue line 320
  - Thêm `:class="marginColorClass(...)"` vào td tỷ suất DV
  - Dùng formula: (svc.quoted_price - svc.estimated_price) / svc.estimated_price × 100

- [x] Task 20: Cập nhật SRS báo giá
  - Tạo mới: docs/srs/quotation-srs.html (9 sections, 14 UC, 15 BR, 4 bảng DB, 23 API)
  - Sửa BR-04: công thức roll-up CHA = SUM(con.estimated_price × con.qty) / cha.qty
  - Sửa BR-08: tỷ suất LN mẫu số = totalImport

- [x] Task 21: Tạo test cases Phase 22
  - HTML: docs/srs/quotation-phase22-testcases.html (48 TC, 7 sections)
  - Excel: docs/srs/quotation-phase22-testcases.xlsx (54 TC)
  - Script: docs/srs/quotation-phase22-generate-testcase.py
  - Phạm vi: in BG (config + preview + print + danh sách), tỷ suất LN (7 chỗ), cảnh báo màu DV, tổng nhập/bán, E2E

#### 22.7 Bug fixes + Cải tiến (2026-05-11~12)

- [x] Task 22: Fix V2BaseCurrencyInput parse sai giá từ API
  - Nguyên nhân: formatCurrency nhận string "20000.00" (US format) nhưng parse theo VN (`.` = separator) → "2000000"
  - Fix: formatCurrency luôn dùng Number(value) thay vì replace `.` rồi convert

- [x] Task 23: Fix validate duyệt BG theo logic giá mới
  - BE ensureAllPricesPositive: phân biệt CHA/CON/Orphan, CON skip validate, CHA chỉ validate quoted_price, thêm validate service items
  - FE validatePrices: CHA validate quoted_price > 0 (trước đây skip), CON skip (trước đây validate estimated_price)

- [x] Task 24: Fix popup gửi duyệt thiếu giá nhập DV bổ sung
  - BE calculateTotals: totalImport chỉ loop BOM products → thêm loop serviceItems cộng estimated_price × qty

- [x] Task 25: Import BOM auto-create danh mục mới
  - BE resolveLookupId thêm param autoCreate: tìm trên ERP DB, nếu không có → tạo mới (model/brand/origin/unit)
  - resolveErpEmployeeId: lấy employees.id trên ERP DB thay vì auth()->id() (FK constraint)
  - validateImportData: bỏ lỗi "không tồn tại trong danh mục" (chỉ giữ "là bắt buộc")
  - importProducts: gọi resolveLookupId với autoCreate=true

- [x] Task 26: Bỏ validate giá con khi duyệt BG
  - BE ensureAllPricesPositive: CON → continue (skip hoàn toàn)
  - FE validatePrices: CON → continue

- [x] Task 27: Mẫu in BG — khối tổng căn phải + có viền
  - QuotationPrintPreview: đổi div text thành bảng nhỏ có border, 3 dòng (Tổng trước thuế / Tổng VAT / Thành tiền sau VAT), căn phải (flex-end)
  - Thêm CSS .totals-summary-table cho cả preview + inline print styles

- [x] Task 28: Mở rộng làm tròn từ 3 → 6 options
  - Select: -3 (hàng nghìn), -2 (hàng trăm), -1 (hàng chục), 0 (số nguyên), 1 (1 thập phân), 2 (2 thập phân)
  - Logic roundVal đã hỗ trợ precision âm sẵn (Math.pow(10, p))

### Phase 23: Đổi nguồn dữ liệu Danh sách hàng hoá dự án
> Design: `.plans/Bomlist-Quotation/design-phase23.md`
> Mục tiêu: Chuyển trang `/assign/product-project` từ `product_projects` sang `bom_list_products` (BOM Tổng hợp + Đã duyệt). Bỏ bảng cũ. Thêm trạng thái đồng bộ ERP. Trang read-only.

#### BE — Database + Entity

- [x] Task 1: Migration — thêm cột `erp_sync_status` + drop bảng cũ
  - Tạo file: `hrm-api/Modules/Assign/Database/Migrations/2026_05_12_000001_phase23_product_project_to_bom.php`
  - `up()`:
    1. `Schema::table('bom_list_products', fn => $table->tinyInteger('erp_sync_status')->default(0)->after('sort_order'))`
    2. `Schema::dropIfExists('product_project_attachments')`
    3. `Schema::dropIfExists('product_projects')`
  - `down()`:
    1. Tạo lại `product_projects` + `product_project_attachments` (copy schema từ entity hiện tại)
    2. Bỏ cột `erp_sync_status` khỏi `bom_list_products`

- [x] Task 2: Thêm relationship `bomList()` vào BomListProduct entity
  - File: `hrm-api/Modules/Assign/Entities/BomListProduct.php`
  - Thêm `use Modules\Assign\Entities\BomList;` ở đầu file
  - Thêm method:
    ```php
    public function bomList()
    {
        return $this->belongsTo(BomList::class, 'bom_list_id');
    }
    ```
  - Thêm accessor `getErpSyncStatusNameAttribute()`:
    ```php
    public function getErpSyncStatusNameAttribute()
    {
        return $this->erp_sync_status == 1 ? 'Đã đồng bộ' : 'Chưa đồng bộ';
    }
    ```
  - Thêm `'erp_sync_status_name'` vào `$appends`

- [x] Task 3: Thêm relationship `createdByEmployee()` vào BomListProduct
  - File: `hrm-api/Modules/Assign/Entities/BomListProduct.php`
  - Thêm `use Modules\Human\Entities\Employee;`
  - Thêm method:
    ```php
    public function createdByEmployee()
    {
        return $this->belongsTo(Employee::class, 'created_by');
    }
    ```

#### BE — Controller + Routes

- [x] Task 4: Viết lại method `index()` trong ProductProjectController
  - File: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php`
  - Bỏ dependency injection `ProductProjectService` (constructor)
  - Bỏ import `ProductProjectService`, `ProductProject`, `ProductProjectRequest`, `ProductProjectListResource`, `DetailProductProjectResource`
  - Thêm import: `Modules\Assign\Entities\BomListProduct`, `Modules\Assign\Entities\BomList`
  - Viết lại `index()`:
    ```php
    public function index(Request $request)
    {
        $query = BomListProduct::query()
            ->join('bom_lists', 'bom_list_products.bom_list_id', '=', 'bom_lists.id')
            ->where('bom_lists.bom_list_type', BomList::TYPE_AGGREGATE)
            ->where('bom_lists.status', BomList::STATUS_DA_DUYET)
            ->leftJoin('tp_models', 'bom_list_products.model_id', '=', 'tp_models.id')
            ->leftJoin('tp_brands', 'bom_list_products.brand_id', '=', 'tp_brands.id')
            ->leftJoin('tp_origins', 'bom_list_products.origin_id', '=', 'tp_origins.id')
            ->leftJoin('tp_units', 'bom_list_products.unit_id', '=', 'tp_units.id')
            ->select(
                'bom_list_products.*',
                'bom_lists.code as bom_code',
                'bom_lists.name as bom_name',
                'bom_lists.prospective_project_id',
                'bom_lists.solution_id',
                'tp_models.name as model_name',
                'tp_brands.name as brand_name',
                'tp_origins.name as origin_name',
                'tp_units.name as unit_name'
            )
            ->with(['bomList.prospectiveProject', 'bomList.solution', 'createdByEmployee.info']);

        // Filters
        if ($request->keyword) {
            $kw = escapeLikeKeyword($request->keyword);
            $query->where(function ($q) use ($kw) {
                $q->where('bom_list_products.code', 'like', "%{$kw}%")
                  ->orWhere('bom_list_products.name', 'like', "%{$kw}%");
            });
        }
        if ($request->model_id) $query->where('bom_list_products.model_id', $request->model_id);
        if ($request->brand_id) $query->where('bom_list_products.brand_id', $request->brand_id);
        if ($request->origin_id) $query->where('bom_list_products.origin_id', $request->origin_id);
        if ($request->unit_id) $query->where('bom_list_products.unit_id', $request->unit_id);
        if ($request->prospective_project_id) $query->where('bom_lists.prospective_project_id', $request->prospective_project_id);
        if ($request->solution_id) $query->where('bom_lists.solution_id', $request->solution_id);
        if ($request->created_by) $query->where('bom_list_products.created_by', $request->created_by);
        if (isset($request->erp_sync_status)) $query->where('bom_list_products.erp_sync_status', $request->erp_sync_status);

        $sortField = $request->sort_field ?? 'created_at';
        $sortDir = $request->sort_dir ?? 'desc';
        $query->orderBy("bom_list_products.{$sortField}", $sortDir);

        $perPage = $request->per_page ?? 10;
        $paginated = $query->paginate($perPage);

        // Transform
        $paginated->getCollection()->transform(function ($item) {
            $project = $item->bomList->prospectiveProject ?? null;
            $solution = $item->bomList->solution ?? null;
            $creator = $item->createdByEmployee->info ?? null;

            return [
                'id' => $item->id,
                'code' => $item->code,
                'name' => $item->name,
                'model_name' => $item->model_name,
                'brand_name' => $item->brand_name,
                'origin_name' => $item->origin_name,
                'unit_name' => $item->unit_name,
                'qty_needed' => $item->qty_needed,
                'estimated_price' => $item->estimated_price,
                'quoted_price' => $item->quoted_price,
                'product_attributes' => $item->product_attributes,
                'bom_list_id' => $item->bom_list_id,
                'bom_code' => $item->bom_code,
                'bom_name' => $item->bom_name,
                'prospective_project_id' => $item->prospective_project_id,
                'prospective_project_code' => $project->code ?? null,
                'prospective_project_name' => $project->name ?? null,
                'solution_id' => $item->solution_id,
                'solution_code' => $solution->code ?? null,
                'solution_name' => $solution->name ?? null,
                'erp_sync_status' => $item->erp_sync_status,
                'erp_sync_status_name' => $item->erp_sync_status == 1 ? 'Đã đồng bộ' : 'Chưa đồng bộ',
                'created_by_name' => $creator->fullname ?? null,
                'created_at' => $item->created_at ? $item->created_at->format('d/m/Y H:i') : null,
            ];
        });

        return $this->apiGetList($paginated);
    }
    ```

- [x] Task 5: Viết lại method `export()` trong ProductProjectController
  - File: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php`
  - Dùng cùng query logic như `index()` nhưng `->get()` thay vì `->paginate()`
  - Truyền vào `ProductProjectExport` view
  - Cập nhật `ProductProjectExport` class và blade view (`exports/product_projects.blade.php`) để render dữ liệu mới (thêm cột Mã BOM, Trạng thái ĐB)

- [x] Task 6: Xoá các methods CRUD + import trong ProductProjectController
  - File: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php`
  - Xoá methods: `store()`, `show()`, `update()`, `destroy()`, `getAll()`, `importValidate()`, `importProducts()`, `buildProductProjectImportMaps()`
  - Giữ lại: `index()`, `export()`, `getModel()`, `getGroupProduct()`, `getTaxRates()`, `getBrands()`, `getManufacturers()`, `getOrigins()`, `getUnits()`, `getSuppliers()`, `createModel()`, `createBrand()`, `createOrigin()`, `createUnit()`, `createMasterReference()`

- [x] Task 7: Cập nhật routes — bỏ routes CRUD + import
  - File: `hrm-api/Modules/Assign/Routes/api.php` (dòng 298-321)
  - Bỏ:
    - `Route::post('/', ...)` (store)
    - `Route::get('/getAll', ...)` (getAll)
    - `Route::get('/{productProject}', ...)` (show)
    - `Route::put('/{productProject}', ...)` (update)
    - `Route::delete('/{productProject}', ...)` (destroy)
    - `Route::post('/import/validate', ...)`
    - `Route::post('/import', ...)`
  - Giữ: GET `/`, GET `/export`, GET `/get-*`, POST `/create-*`

- [x] Task 8: Xoá file BE không còn dùng + sửa references trong BomListService + BomListProduct
  - Xoá: `Modules/Assign/Entities/ProductProject.php`
  - Xoá: `Modules/Assign/Entities/ProductProjectAttachment.php`
  - Xoá: `Modules/Assign/Services/ProductProjectService.php`
  - Xoá: `Modules/Assign/Transformers/ProductProjectResource/ProductProjectListResource.php`
  - Xoá: `Modules/Assign/Transformers/ProductProjectResource/DetailProductProjectResource.php`
  - Xoá: `Modules/Assign/Http/Requests/ProductProject/ProductProjectRequest.php`
  - Kiểm tra xem còn file nào import `ProductProject` entity không → nếu có, xoá hoặc sửa reference

#### FE — Sửa trang danh sách

- [x] Task 9: Bỏ CRUD + Import trên `product-project/index.vue`
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - Bỏ components: `CreateProductProjectModal`, `V2BaseImportModal`, `BaseConfirmModal` (confirm delete)
  - Bỏ template sections: button Tạo mới, button Import Excel, confirm delete modal, create modal, import modal
  - Bỏ data: `modalMode`, `selectedProductId`, `itemToDelete`, import-related data
  - Bỏ methods: `openCreateModal()`, `openImportModal()`, `handleDownloadImportTemplate()`, `handleValidateImportData()`, `handleImportProductProjects()`, `handleProductSaved()`, `viewItem()`, `editItem()`, `confirmDelete()`, `handleConfirmDelete()`
  - Bỏ computed: `importColumns`, `importRequiredFields`, `importValidationRules`, `deleteConfirmMessage`
  - Bỏ các select options không còn dùng: `productCateOptions`, `groupOptions`, `supplierOptions`, `manufacturerOptions`, `vatOptions` + PRODUCT_CATE_MAP constant

- [x] Task 10: Đổi row actions → chỉ "Xem BOM"
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - `getRowActions()` chỉ trả 1 action:
    ```javascript
    getRowActions(item) {
        return [{
            key: 'view-bom',
            title: 'Xem BOM',
            icon: 'ri-eye-line',
            class: 'pp-icon-btn',
        }]
    }
    ```
  - `handleRowAction()`: navigate `this.$router.push('/assign/bom-list/' + item.bom_list_id)`

- [x] Task 11: Thêm cột Mã BOM + Trạng thái ĐB vào table
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - Thêm vào `defaultTableColumns` (sau cột `productInfo`):
    ```javascript
    { key: 'bomCode', label: 'Mã BOM', title: 'Mã BOM', width: '140px', minWidth: '140px', align: 'left', isVisible: 'bomCode' },
    ```
  - Thêm vào cuối columns:
    ```javascript
    { key: 'erpSyncStatus', label: 'Trạng thái ĐB', title: 'Trạng thái đồng bộ', width: '140px', minWidth: '140px', align: 'center', isVisible: 'erpSyncStatus' },
    ```
  - Thêm template slots:
    ```html
    <template #cell-bomCode="{ item }">
        <a class="pp-code-badge" style="cursor:pointer" @click="$router.push('/assign/bom-list/' + item.bom_list_id)">
            {{ item.bom_code || '—' }}
        </a>
    </template>
    <template #cell-erpSyncStatus="{ item }">
        <span :class="['pp-chip', item.erp_sync_status === 1 ? 'green' : 'gray']">
            {{ item.erp_sync_status_name }}
        </span>
    </template>
    ```

- [x] Task 12: Thêm filter Trạng thái đồng bộ ERP
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - Thêm `erp_sync_status: undefined` vào `initialFilters`
  - Thêm filter select trong template:
    ```html
    <div class="col-md-3 mb-2">
        <V2BaseLabel text="Trạng thái đồng bộ" />
        <V2BaseSelect
            v-model="filters.erp_sync_status"
            :options="erpSyncOptions"
            size="sm"
            placeholder="Tất cả"
        />
    </div>
    ```
  - Thêm data: `erpSyncOptions: [{ id: 0, name: 'Chưa đồng bộ' }, { id: 1, name: 'Đã đồng bộ' }]`
  - Thêm `erp_sync_status` vào `apiFilters` trong `loadData()`

- [x] Task 13: Cập nhật `loadSelectOptions()` — bỏ API không dùng
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - Bỏ calls: `get-group-product`, `get-manufacturer`, `get-tax-rates`, `get-suppliers`
  - Giữ: `get-model`, `get-brand`, `get-origin`, `get-unit`, prospective-projects, solutions

- [x] Task 14: Bỏ filters cũ không còn dùng
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - Bỏ khỏi `initialFilters`: `product_cate`, `group_id`, `supplier_id`, `manufacture_id`, `vat_percent_tax_rate_id`
  - Bỏ khỏi `apiFilters` trong `loadData()`: tương tự
  - Xoá commented-out filter blocks trong template (Loại hàng hoá, Nhóm hàng hoá, Nhà cung cấp, Hãng sản xuất, Thuế VAT)

- [x] Task 15: Xoá file FE không còn dùng
  - Xoá: `hrm-client/pages/assign/product-project/components/CreateProductProjectModal.vue`

- [x] Task 16: Cập nhật export blade view
  - File: `hrm-api/resources/views/exports/product_projects.blade.php`
  - Thêm cột "Mã BOM" + "Trạng thái ĐB"
  - Cập nhật data binding: dùng trực tiếp `$item->bom_code`, `$item->model_name`, etc. (đã join sẵn)
  - Bỏ PHP logic lấy relation (`$item->prospectiveProject`, `$item->tpModel`) — data đã flatten qua select

#### Test thủ công

- [ ] Task 17: Chạy migration trên local
  - `php artisan migrate` — verify cột `erp_sync_status` được thêm, 2 bảng cũ bị drop

- [ ] Task 18: Test trang danh sách
  - Mở `/assign/product-project` → xác nhận hiển thị dữ liệu từ BOM đã duyệt
  - Không còn button Tạo mới, Import
  - Row action chỉ có "Xem BOM" → navigate đúng
  - Filters hoạt động: keyword, model, brand, origin, unit, dự án, giải pháp, người tạo, trạng thái ĐB
  - Cột Mã BOM hiển thị đúng, click navigate sang BOM
  - Cột Trạng thái ĐB hiển thị pill đúng màu

- [ ] Task 19: Test export Excel
  - Click "Xuất Excel" → download file → verify cột mới (Mã BOM, Trạng thái ĐB)
  - Verify filters áp dụng khi export

- [ ] Task 20: Test edge cases
  - BOM chưa duyệt → hàng hoá KHÔNG hiển thị
  - BOM loại Thành phần → hàng hoá KHÔNG hiển thị
  - BOM Tổng hợp + Đã duyệt → hàng hoá hiển thị
  - Pagination + sorting hoạt động đúng

### Phase 24: Bug fixes + UI improvements (2026-05-12)

[x] Task 1: Thêm cột "Mã hàng" trước "Tên hàng" trong BomBuilderTableCard.vue (header, total, parent, child, group, standalone — 6 vị trí + visibleColumnCount +1)
[x] Task 2: BomBuilderInfoCard.vue — căn đều col-3 cho tất cả trường thông tin chung (Tên BOM col-9→col-3, Dự án/GP/HM col-4→col-3)
[x] Task 3: Sửa điều kiện lấy dự án khi tạo BOM — chuyển từ "nhân sự dự án" sang "nhân sự giải pháp" (PM, solution_members, solution_module_members)
[x] Task 4: Sửa điều kiện hiện nút Sửa BOM — status 1/2/6 + chỉ người tạo. BE thêm check created_by + cho sửa status 6 (Không duyệt)
[x] Task 5: Validate mã hàng hoá bắt buộc khi Lưu nháp / Lưu BOM (FE toast + BE validateProductCodes)
[x] Task 6: Quick create model/brand/origin — check unique (BE trả existed flag + check code brand, FE hiện lỗi inline thay vì tạo trùng)
[x] Task 7: Làm tròn báo giá — đổi label "Làm tròn giá" + icon info tooltip + button "Áp dụng" + disable khi chưa chọn
[ ] Task 8: Test thủ công Phase 24

---

### Phase 25: Bug fixes (2026-05-14)

[x] Task 1: Sửa điều kiện lấy dự án khi tạo BOM — thêm leader hạng mục (solution_modules.leader_id) + chuyển về dùng whereHas('solution') thay whereExists
[x] Task 2: Fix lỗi floating point hiển thị giá nhập — formatMoney dùng Math.round(num*100)/100 + maximumFractionDigits: 2 (BomBuilderTableCard.vue)
[x] Task 3: Thêm STATUS_DUNG (6) vào whereIn phân quyền NLG trên trang danh sách yêu cầu XD giá (PricingRequestController)

---

### Phase 26: Bỏ required giá nhập/bán khi Lưu nháp (2026-05-16)

[x] Task 1: FE — đổi handleSaveDraft() từ strict:true → strict:false
  - File: `hrm-client/pages/assign/quotations/_id/edit.vue`
  - `handleSaveDraft()` gọi `save(false, { strict: false })` thay vì `strict: true`
[x] Task 2: BE — đổi service_items estimated_price + quoted_price từ required → nullable
  - File: `hrm-api/Modules/Assign/Http/Requests/Quotation/QuotationUpdateRequest.php`
  - `service_items.*.estimated_price` → `nullable|numeric|min:0`
  - `service_items.*.quoted_price` → `nullable|numeric|min:0`
[ ] Task 3: Test thủ công — lưu nháp không nhập giá, submit vẫn bắt buộc giá

---

### Phase 27: Fix + bổ sung cột trang Hàng hoá dự án (2026-05-16)

[x] Task 1: Fix text "Không có hàng hoá nào" khi có data — response không có `meta`, FE destructure sai
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - Response format: `{ code, message, data, current_page, total, per_page, from, to, ... }` (flat, không có `meta`)
  - Fix: destructure response đúng format flat thay vì `{ data, meta }`
[x] Task 2: Bỏ class font-weight-bold ở cột Mã hàng
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - Bỏ `font-weight-bold` ở template #cell-code
[x] Task 3: Bổ sung 3 cột mới + BE trả thêm data
  - BE: `ProductProjectController::transformItem()` thêm `product_attributes`, `parent_code`, `parent_name`, `note`
  - BE: `buildQuery()` thêm left join self (parent) để lấy parent code+name
  - FE: thêm 3 cột vào `defaultTableColumns`: Đặc điểm/TSKT, Hàng hoá cha, Ghi chú
  - FE: thêm 3 template slots
[x] Task 4: Bổ sung 3 cột mới vào export Excel
  - File: `hrm-api/resources/views/exports/product_projects.blade.php`
  - Thêm header + body cho: Đặc điểm/TSKT, Hàng hoá cha, Ghi chú
[x] Task 5: Fix tuỳ chọn cột thiếu cột mới — merge cột mới vào saved config
  - File: `hrm-client/pages/assign/product-project/index.vue`
  - `defaultTableColumns`: nếu server config thiếu cột → append cột mới vào cuối
[x] Task 6: Cột Đặc điểm dùng v-html + spec-preview (giống BOM detail) thay vì stripHtml
  - FE: `v-html` + class `spec-preview` (max-height 80px, scroll, format p/ul/ol)
  - CSS: copy `.spec-preview` styles từ BomBuilderTableCard.vue
[x] Task 7: Tăng width cột Hàng hoá cha 200→300px, minWidth 150→250px
[x] Task 8: Fix font chữ cột Đặc điểm trong Excel — thêm html_entity_decode + font-family Times New Roman

---

## Phase 28 — UI cải thiện chi tiết Dự án TKT (2026-05-16)

[x] Task 1: Topbar title hiển thị Mã. Tên dự án + trạng thái dự án (pill inline HTML)
  - File: `hrm-client/pages/assign/prospective-projects/_id/manager.vue`
  - `pageTitle` computed trả HTML: label + `<span>` pill (inline style, border-radius, bg color)
  - `projectStatusInfo` computed map status ID → { name, color } với label rút gọn + màu riêng
[x] Task 2: Tab Yêu cầu — thay "Dự án TKT" bằng trạng thái yêu cầu khi disabled
  - File: `hrm-client/pages/assign/request-solution/components/RequestTab.vue`
  - Khi `disabled=true`: hiện request status pill (outlined style, dot indicator, CSS `color-mix`)
  - CSS: `.request-status-pill` + `.request-status-dot` dùng CSS variable `--pill-color`
[x] Task 3: Tab Yêu cầu — thêm mã yêu cầu trước trạng thái
  - File: `manager.vue` — thêm `code` vào `this.request` object từ API response
  - File: `RequestTab.vue` — hiển thị mã yêu cầu (bold) + trạng thái (pill) cùng dòng
[x] Task 4: Tab Hồ sơ — chuyển button Thao tác vào cột Mã hồ sơ, hover mới hiện
  - File: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectReviewProfilesTab.vue`
  - Xoá cột `actions` khỏi `tableColumns`
  - Merge button (Xem chi tiết + YC XD giá) vào `#cell-profileInfo` cùng dòng mã hồ sơ
  - CSS: `.row-actions` opacity 0 → 1 on `tr:hover`, transition 0.15s
[x] Task 5: Click mã hồ sơ → mở popup xem chi tiết
  - Mã hồ sơ đổi `text-primary`, cursor pointer, underline hover, emit `view-profile`

---

### Checkpoint — 2026-05-23 (Phase 29.10)
Vừa hoàn thành: Phase 29.10 — 9 task (Task 60-68). Bảng tổng hợp giá trị + validate phân bổ + fix bugs + in báo giá
  - Bảng tổng hợp 8 dòng trên form edit + view + export Excel + print preview
  - Layout CK tổng + bảng tổng hợp trên 1 row (50/50)
  - Validate bắt buộc phân bổ hết trước khi lưu (CK tổng) + skipAllocationCheck cho allocate/import
  - Fix bug 2 lỗi đồng thời khi chuyển CK method 1→2 rồi phân bổ
  - Hiện "Còn: xxx" trên header cột CK phân bổ (xanh/đỏ)
  - Export Excel: bảng tổng hợp 8 dòng (TSLN xanh/đỏ, TT sau VAT highlight blue)
  - DB field unit_price_after_discount + auto-compute trong recomputeTotals()
  - In báo giá: config modal dynamic columns theo discountMethod + preview CK columns + summary table
  - Fix discountMethod string→Number() conversion (API trả string)
Đang làm dở: không
Bước tiếp theo: Chạy migration unit_price_after_discount + Test thủ công Phase 29.9 (Task 52-59)
Blocked: không

### Checkpoint — 2026-05-16 (Phase 28)
Vừa hoàn thành: Phase 28 — 5 task UI cải thiện chi tiết Dự án TKT
  - Topbar title: Mã. Tên + status pill inline
  - Tab Yêu cầu: mã YC + trạng thái pill (thay vị trí Dự án TKT khi disabled)
  - Tab Hồ sơ: button gộp vào cột Mã hồ sơ (hover), click mã → popup chi tiết
Đang làm dở: không
Bước tiếp theo: nhận yêu cầu mới
Blocked: không

### Checkpoint — 2026-05-16 (Phase 27)
Vừa hoàn thành: Phase 27 — 8 task fix + bổ sung cột trang Hàng hoá dự án
  - Fix pagination text "Không có hàng hoá nào" (destructure flat response thay vì { data, meta })
  - Bỏ bold cột Mã hàng
  - Thêm 3 cột: Đặc điểm/TSKT (v-html spec-preview), Hàng hoá cha (mã . tên, 300px), Ghi chú
  - BE: left join parent_product, trả thêm product_attributes, parent_code, parent_name, note
  - Export Excel: thêm 3 cột + fix font Đặc điểm (html_entity_decode + Times New Roman)
  - Merge cột mới vào saved column config
Đang làm dở: không
Bước tiếp theo: nhận yêu cầu mới
Blocked: không

### Checkpoint — 2026-05-16 (Phase 26)
Vừa hoàn thành: Phase 26 — bỏ required giá nhập/bán khi Lưu nháp báo giá
  - FE: handleSaveDraft() đổi strict:true → strict:false (edit.vue:1120)
  - BE: service_items estimated_price + quoted_price đổi required → nullable (QuotationUpdateRequest.php)
  - Gửi duyệt vẫn giữ validate giá > 0 (strict:true + ensureAllPricesPositive)
Đang làm dở: không
Bước tiếp theo: Test thủ công Phase 26
Blocked: không

### Checkpoint — 2026-05-14 (Phase 25)
Vừa hoàn thành: 3 bug fixes
  - Filter dự án: thêm leader hạng mục, dùng whereHas gọn hơn
  - Giá nhập: fix floating point 839.100.093,7099999 → 839.100.093,71
  - YCXD giá: NLG thấy được trạng thái Dừng trong danh sách + bộ lọc
Đang làm dở: không
Bước tiếp theo: Test thủ công
Blocked: không

### Checkpoint — 2026-05-12 (Phase 24)
Vừa hoàn thành: 7 task code done — bug fixes + UI improvements
  - Mã hàng: cột mới trong bảng BOM (tạo/sửa/xem chi tiết)
  - Info card: col-3 đều nhau
  - Lấy dự án: filter theo nhân sự giải pháp (PM + members + module members)
  - Nút Sửa: chỉ người tạo, thêm status Không duyệt
  - Validate mã hàng bắt buộc (FE + BE)
  - Check unique tạo nhanh model/brand/origin
  - Làm tròn giá: label + tooltip + button + disable
Đang làm dở: không
Bước tiếp theo: Test thủ công Phase 24
Blocked: không

### Checkpoint — 2026-05-12 (Phase 22 bug fix + improvements)
Vừa hoàn thành: Task 22-28 — 7 bug fixes + improvements
  - Fix V2BaseCurrencyInput parse sai giá API (×100)
  - Fix validate duyệt: phân biệt CHA/CON/Orphan, bỏ validate con, thêm validate DV
  - Fix popup gửi duyệt: totalImport thiếu DV bổ sung
  - Import BOM: auto-create model/brand/origin/unit trên ERP DB
  - Mẫu in: khối tổng căn phải có viền (3 dòng)
  - Làm tròn: 6 options (-3 đến 2)
Đang làm dở: không
Bước tiếp theo: Test thủ công (Task 9-12)
Blocked: không

### Checkpoint — 2026-05-10 (Phase 21 bug fix)
Vừa hoàn thành: 7 bug fix tasks (43-49) cho Phase 21
  - Fix cross-DB TpUnit resolution (import + show)
  - Fix CKEditor duplicate (v-show → v-if)
  - Chuẩn hoá format tiền VN (dấu `.` ngăn cách, dấu `,` thập phân) + cho nhập thập phân
  - Import popup: row tổng cộng sticky + cột sau VAT + button nổi bật + fix validate message lệch dòng
  - Lịch sử báo giá: overhaul theo BomListLog pattern (labels, colors, per-product detail, strip HTML, service CRUD log)
Đang làm dở: Không
Bước tiếp theo: Test thủ công Tasks 35-42 + test lại các bug fix
Blocked: Không

### Checkpoint — 2026-05-09 (Phase 21)
Vừa hoàn thành: Phase 21 — 34/42 tasks code done (còn 8 test thủ công Tasks 35-42)
  - BE: Migration quotation_service_items + Entity + Relation + CRUD API (3 routes) + show eager load + update sync
  - BE: computeTotals đảo logic (giá bán cha trực tiếp, gộp dịch vụ bổ sung)
  - BE: Export Excel (section DV bổ sung, con blank giá bán/VAT, đảo lock template)
  - BE: Import prices (cha import giá bán+VAT, con chỉ giá nhập, DV-* update service items)
  - FE edit.vue: đảo cha-con (cha editable giá bán+VAT, con hiện "—"), VAT skip children, section DV bổ sung + modal + CRUD, disable BOM kế thừa, làm tròn (dropdown 3 mức + confirm), save gửi service_items, tổng gộp DV
  - FE index.vue: hiển thị DV readonly, đảo cha-con, tổng gộp
Đang làm dở: Không
Bước tiếp theo: Chạy migration + test thủ công Tasks 35-42
Blocked: Không

### Checkpoint — 2026-05-28 (Phase 30)
Vừa hoàn thành: Phase 30 — BOM ẩn giá ERP + Báo giá load giá ERP + Hiệu lực báo giá + Tab báo giá dự án
  - BOM: Ẩn giá nhập hàng ERP (cả cha + con) trên FE (hiển thị "—") + BE (force estimated_price=0)
  - Báo giá: Load giá nhập ERP khi chọn BOM → quy đổi tỷ giá. Hàng con ERP load trực tiếp, cha rollup từ con
  - Hiệu lực: Đổi từ số ngày → ngày cụ thể (validity_date). Migration rename cột. Tính realtime trên FE, lưu khi save/approve
  - Icon cảnh báo: Hàng cha ERP sắp đổi giá → warning icon + tooltip ngày thay đổi (cả màn edit + xem)
  - Tab báo giá dự án TKT: Hiển thị tất cả trạng thái (bỏ filter chỉ Đã duyệt), thêm cột Người lập + Trạng thái
  - Button "Tạo báo giá" theo chuẩn V2BaseButton trong slot #actions, bỏ điều kiện implementationType
  - Buttons theo quyền: Sửa/Xoá khi status=1 + là người tạo, Ghi chú KD khi status=4 + là Sale
  - Màn xem: Toolbar hiển thị Chiết khấu, TSLN chỉ hiện 1 dòng khi không CK
Đang làm dở: Không
Bước tiếp theo: Chạy migration validity_date + test thủ công
Blocked: Không

### Checkpoint — 2026-05-09 (Phase 20)
Vừa hoàn thành: Phase 20 — 16 tasks code (Hyperlink + Fix Excel + File mẫu + Import nhóm)
  - Hyperlink: Dự án + Giải pháp trên cả màn sửa + xem báo giá
  - Excel export: fix Mã/Tên đảo (ungrouped blocks), thêm VAT con, thêm cột Tỷ suất LN
  - File mẫu riêng: endpoint /export-import-template, bỏ tfoot, lock cột trừ 3 editable, công thức thành tiền
  - Import nhóm: BE nhận diện La Mã + validate tên nhóm, blade render cell riêng, FE preview row nhóm background xanh nhạt không input
  - Components: V2BaseImportTable hỗ trợ type=computed + isGroupRow
Đang làm dở: Không
Bước tiếp theo: Test thủ công Tasks 17-20
Blocked: Không

### Checkpoint — 2026-05-08
Vừa hoàn thành: Phase 19 — Xuất/Import Excel trên màn sửa Báo giá (Tasks 1-7 code + nhiều vòng fix)
  - BE: 2 route validate + import (JSON-based, không upload file). Controller 2-pass validate: con validate giá/VAT số, cha validate thành tiền = Σ(con × qty) + VAT = max(con). Strip ký tự %/, trong giá/VAT. Skip rows không có STT. Validate qty khớp BOM.
  - BE: BomListExport thêm withSkipHeader() — quotation export bỏ 8 dòng header info, bỏ cột profit_margin.
  - FE: V2BaseImportModal dùng chung, bỏ step pills toàn cục, thêm slot extra-config. Import helper hỗ trợ headerRow param (chọn dòng tiêu đề).
  - FE: edit.vue — 2 button Xuất/Import Excel, modal import với chọn dòng tiêu đề, 7 cột preview (STT, Mã, Tên, SL, Giá nhập, Giá bán, VAT%), filter bỏ row không STT trước validate.
  - FE: V2BaseImportTable — cột "#" (50px) thay "Dòng dữ liệu" (120px).
  - Fix: export 404 (thiếu /api/v1), double modal-body padding, CSS scoped không reach teleported modal, VAT "8.00%" lỗi, row tổng cộng import vào.
Đang làm dở: Không
Bước tiếp theo: Test thủ công export/import trên /assign/quotations/{id}/edit (Tasks 8-10)
Blocked: Không

### Checkpoint — 2026-05-07
Vừa hoàn thành: Phase 18 — 28 tasks (UI fix + logic fix + lịch sử BOM)
  - UI: bỏ bold 3 cột, Loại BOM text thuần, button Xuất Excel 2 chỗ, "Lưu và tiếp tục"
  - Cấu hình: di chuyển tỷ suất LN mức sàn, fix input ẩn, validate nối tiếp
  - Logic: fix double-count tổng nhập, profit margin formula /sale, VAT FE-only, Vue 2 reactivity
  - Lịch sử: migration + entity + 5 chỗ ghi log + API + FE modal + buttons danh sách + chi tiết
  - Chi tiết log: resolve tên FK, tracking thay đổi sản phẩm (thêm/xoá/sửa + children)
Đang làm dở: Không
Bước tiếp theo: Chạy migration bom_list_logs + test lịch sử BOM
Blocked: Không

## Phase 11-fix — FE preview BOM tổng hợp khớp validate BE (Tự triển khai)

- [x] FE: `loadPreviewBom` (SolutionApprovalModal.vue) luôn set `bom_list_type=2` — bỏ điều kiện `if (!isSelfImplementation)` khiến giải pháp Tự triển khai hiển thị nhầm BOM Thành phần
- [x] FE: gộp cảnh báo "chưa có BOM" về 1 message "BOM tổng hợp" (bỏ nhánh self-impl ghi "BOM" gây hiểu nhầm)

### Checkpoint — 2026-07-01
Vừa hoàn thành: Fix lỗi 422 "Chưa có BOM tổng hợp Hoàn thành" khi gửi hồ sơ trình duyệt giải pháp Tự triển khai dù UI hiện có BOM.
  - Nguyên nhân: BE (SolutionService.php:1948) submit LUÔN bắt bom_list_type=TYPE_AGGREGATE(2). FE (SolutionApprovalModal.vue:627 cũ) chỉ lọc type=2 khi KHÔNG tự triển khai → giải pháp Tự triển khai hiện nhầm BOM Thành phần (type=1) lên ô "BOM tổng hợp gắn vào hồ sơ" → submit 422.
  - Dữ liệu thực tế solution 86: current_version_id=103; BOM-2026-00286 type=1 (Thành phần) status=2 version=103 → thoả FE preview lỏng nhưng trượt validate BE.
  - Hướng chốt (user chọn A): sửa FE khớp BE — luôn yêu cầu BOM Tổng hợp.
Đang làm dở: Không
Bước tiếp theo: User verify trên UI — mở modal trình duyệt giải pháp Tự triển khai chưa có BOM Tổng hợp → phải hiện cảnh báo đỏ "Chưa có BOM tổng hợp" thay vì hiện BOM Thành phần.
Blocked: Không

## Phase 32 — Tối ưu UI popup "Thêm hàng hoá" (dồn diện tích cho bảng hàng hoá)

Bối cảnh: popup `QuotationProductSearchModal.vue` (dùng chung `/assign/bom-list/add|edit` + `/assign/quotations/_id/edit`).
Khi mở "Tìm kiếm nâng cao" chỉ còn thấy ~2 dòng hàng hoá — vùng quan trọng nhất lại ít diện tích nhất.

- [x] FE (component chung): `V2BaseFilterPanel.vue` thêm slot `header-actions` (bổ sung, không truyền → render rỗng) để màn cha chèn nút ngang hàng nút toggle "Tìm kiếm nâng cao" — các màn danh sách khác giữ nguyên
- [x] FE: chuyển nút "Thêm hàng tạm" vào slot `header-actions` — bỏ hẳn 1 hàng riêng phía trên bảng
- [x] FE: khối lọc nâng cao từ 4 `filter-row` cứng (5 ô/hàng + 2 ô rỗng độn) → 1 CSS grid `auto-fit minmax(190px,1fr)` — 1920px: 9 ô/hàng còn 2 hàng; 1366px: 6 ô/hàng còn 3 hàng
- [x] FE: hàng "Nhóm hàng" nhãn xếp chồng (~56px) → inline ngang control (32px)
- [x] FE: popup 95vw×95vh → 98vw×98vh, backdrop padding 12→6px, nén padding modal-head/body/footer + tp-card + tab-content
- [x] FE: cột chữ dài (Loại HH / Tên / Ghi chú / Tính chất HH) bọc `.cell-clamp` cắt 2 dòng + `title` tooltip — dòng cao 45-81px → đều 39-40px
- [x] FE: ảnh thumbnail 32→26px (yếu tố quyết định chiều cao dòng)

### Checkpoint — 2026-07-15
Vừa hoàn thành: Phase 32 — tối ưu diện tích bảng trong popup Thêm hàng hoá (2 file FE, không BE/migration/permission).
  - Đo thực tế Playwright @1920x1080 (DNS Admin, /assign/bom-list/add):
    - Nâng cao MỞ + có Nhóm hàng (case user báo): 2 dòng → **15 dòng** đầy đủ; bảng = 61% chiều cao popup (643px)
    - Nâng cao ĐÓNG: 18-19 dòng; khối lọc 236px → 86px (đóng) / 193px (mở)
    - Dòng: 45-81px → 39-40px đều; nút "Thêm hàng tạm" y=63 NGANG HÀNG "Tìm kiếm nâng cao" y=63
  - Regression: `/assign/bom-list` (index) filter panel giữ nguyên — toggle vẫn sát mép phải (gap=0), 1 button, title đúng
  - Select2 lọc vẫn mở đúng, on-screen, search field 186px (không bị co 0) ; @1366x768 grid tự co 6 ô/hàng, không tràn ngang
  - Lưu ý: `pages/assign/bom-list/components/BomBuilderAddProductModal.vue` là CODE CHẾT (BomBuilderEditor đã dùng QuotationProductSearchModal) — chưa xoá
Đang làm dở: Không
Bước tiếp theo: User hard-refresh verify popup ở cả 2 màn (BOM + Báo giá `/assign/quotations/{id}/edit`)
Blocked: Không

## Phase 32b — Fix lỗi UI select2 chọn nhiều + nén khối phân trang

- [x] FE fix: ô search select2 multiple ĐÈ LÊN chip khi đã chọn (lỗi CÓ SẴN TỪ TRƯỚC, không do Phase 32)
  - Nguyên nhân gốc: hack CSS cũ ép `.select2-search--inline { width:100%; float:none }` MỌI LÚC → ô search thành block full-width nằm đè chip đang float. Hack chỉ cần cho trạng thái RỖNG (select2 init lúc panel `v-show=false` → `resizeSearch()` đọc width ul = 0 → field width ~0 → mất placeholder/con nháy).
  - Fix: giới hạn hack bằng `.select2-selection__rendered > .select2-search--inline:only-child` (rỗng thì ô search là con DUY NHẤT; có chip thì ul có thêm `__clear` + `__choice`) → có chip là trả về float mặc định của select2. Bỏ `width:100%!important` + `margin-top` vô điều kiện trên field.
- [x] FE: nén khối phân trang — `.row.paging` bỏ `mt-3` (24px) → 4px, bỏ padding 10px; `.page-total` font 12px; select "Số dòng/trang" 28px; `.page-link` padding gọn
  - (Rule cũ đoán sai selector `.v2-pagination`/`.pagination-wrapper` — KHÔNG tồn tại, đã thay bằng `.row.paging` / `.page-total` thật của V2BasePagination)

### Checkpoint — 2026-07-15
Vừa hoàn thành: Phase 32b — 1 file FE (`QuotationProductSearchModal.vue`, chỉ CSS).
  - Đo Playwright @1920x1080 (click/gõ THẬT, không giả lập):
    - RỖNG: ô search 186px, placeholder "Tất cả" đủ, hộp 32px → fix gốc KHÔNG tái phát
    - CÓ CHIP: overlap `true` → `false`; ô search float left ngay sau chip (x=387), hộp 33px
    - GÕ "Nhập" khi có chip: lọc đúng 3 kết quả (Nhập thường xuyên / theo yêu cầu / mẫu), không đè chip, field nằm trong hộp
    - Chứng minh lỗi CÓ SẴN: ép lại bề rộng cột cũ 350px → vẫn `overlap: true`
  - Phân trang: gap bảng↔paging 24px → 4px; khối 54px → 34px; nâng cao ĐÓNG 20 dòng (trọn trang), MỞ 17 dòng
Đang làm dở: Không
Bước tiếp theo: User hard-refresh verify chọn nhiều + phân trang ở cả 2 màn (BOM + Báo giá)
Blocked: Không
Ghi chú (ngoài scope, KHÔNG sửa): lint cảnh báo `v-else` dòng 257 (`<tr v-for v-else>`) là code CÓ SẴN — không nằm trong diff, bảng vẫn render đúng.

## Phase 32c — Viết skill "popup chứa bảng dữ liệu" + fix Bẫy 1 ở file mẫu

- [x] Skill: `.claude/skills/modal-popup/SKILL.md` thêm **mục 4** "Popup chứa BẢNG dữ liệu — dồn diện tích cho bảng" (8 điểm bắt buộc, dạng hợp đồng/recipe) + checklist riêng cho popup có bảng
- [x] Skill: thêm file tham chiếu `.claude/skills/modal-popup/table-popup-layout.md` — CSS copy-paste đầy đủ, 7 bẫy, ngân sách chiều cao, snippet đo Playwright
- [x] FE fix: `QuotationProductSearchModal.vue` `.modal-body` `overflow-y: auto` → `overflow: hidden` (chính là Bẫy 1 mà skill cảnh báo — file mẫu tự vi phạm)

### Checkpoint — 2026-07-15
Vừa hoàn thành: Phase 32c — viết skill theo TDD (superpowers:writing-skills) + fix file mẫu.
  - RED (baseline, 2 subagent Opus KHÔNG có skill): cả 2 tự tìm ra QuotationProductSearchModal và copy công thức → baseline BỊ NHIỄU (file mẫu đã chứa lời giải). Vẫn thu được:
    - Hội tụ (bằng chứng công thức đúng): chuỗi flex + min-height:0, bỏ max-height cứng, cell-clamp, grid auto-fit, mt-3 của paging
    - Căn nguyên sắc hơn: `.modal-body{overflow-y:auto}` khiến mở filter ĐẨY BẢNG TRÔI khỏi màn (bảng vẫn 400px) — đó mới là lý do "2 dòng"
    - Phân kỳ (chỗ cần siết): tự chế "dense toggle", trần 22vh + overflow trên lưới lọc, nghi vấn `.modal-content`/z-index
  - Kiểm chứng nghi vấn `.modal-content` (đo live, KHÔNG suy đoán): V2BaseSelectInModal chỉ set dropdownParent khi có `.modal-content` → popup overlay không có → append `<body>`. NHƯNG chính component đã set `z-index:9999 !important` (V2BaseSelectInModal.vue:264/296/299) → nổi trên backdrop 5000. Đo: containerZIndex=9999, elementFromPoint giữa dropdown chạm `.select2-results__option`, hitIsInsideDropdown=true → KHÔNG lỗi, không cần vá. Đã ghi thành Bẫy 6.
  - GREEN (1 subagent Opus CÓ skill, bối cảnh khác — Timesheet): đọc đúng SKILL.md mục 4 + table-popup-layout.md, áp đủ 8 điểm, tự dựng harness tĩnh (Bootstrap + CSS thật của V2BaseFilterPanel) và ĐO: 1920 đóng/mở = 19/17 dòng, 1366 = 11/8; bodyMustNotScroll=true cả 4; sweep minmax 190→170px (+1 dòng @1366). PASS.
  - GREEN bắt được lỗi thật: file mẫu vẫn để `.modal-body{overflow-y:auto}` = đúng Bẫy 1 skill cảnh báo → đã fix thành `overflow:hidden`.
  - Verify sau fix (app thật): 1280x720 nâng cao MỞ → 6 dòng, paging KHÔNG bị cắt, footer còn, body không cuộn; 1920x1080 MỞ → 17 dòng, bảng 68%, không thoái lui.
Đang làm dở: Không
Bước tiếp theo: User review skill; theo quy tắc team `.claude/skills/` sửa qua PR (chưa commit/push).
Blocked: Không

### Checkpoint — 2026-07-17 (bugfix)
Vừa hoàn thành: Fix lỗi 500 "Class 'Modules\CRM\Entities\Customer' not found" khi update BomList (BomListService::buildChanges, resolver customer_id). Sai class (CRM không có Customer entity) + sai field (`->name`, cột thực là `fullname`). Đổi sang `\Modules\Human\Entities\Customer` (đúng class BomList::customer() dùng) + `->fullname` (đúng như BomListListResource). Lint PHP OK.
Đang làm dở: Không
Bước tiếp theo: User test update BomList có đổi khách hàng → không còn 500, log thay đổi hiện đúng tên KH
Blocked: Không

### Checkpoint — 2026-07-17 (bugfix - đính chính nguồn KH)
Đính chính Bug class Customer: KH của BomList là customer_id **ERP** (giống nguồn màn /assign/customers → CustomerService đọc trực tiếp ERP qua App\Models\TpCustomer, connection mysql2). Bảng customers HRM chỉ chứa tập KH đã sync → id ERP (43244, 43305, 27127...) phần lớn KHÔNG có → Human\Customer::find trả null. Fix cuối: resolver customer_id dùng `\App\Models\TpCustomer::find($id)->fullname`, bọc try/catch như resolver currency_id. Đã verify 3 id ERP đều resolve được fullname. Lint OK.
Bước tiếp theo: User test update BomList đổi KH → log thay đổi hiện đúng tên KH (kể cả KH chưa sync sang HRM).

### Checkpoint — 2026-07-18 (bugfix - màn edit BOM không hiện khách hàng)
Vừa hoàn thành: Fix ô Khách hàng trống ở màn `/assign/bom-list/{id}/edit`. Root cause: FE `loadBomDetail` gọi vòng 2 `human/customers/{id}` (bảng customers HRM) để lấy tên, nhưng customer_id của BomList là id ERP (TpCustomer/mysql2) → 404 → catch nuốt lỗi → trống. (Tạo mới hiện được vì `handleProjectChange` fill tên từ option dự án.)
Fix tại gốc: (1) BE `DetailBomListResource` trả thêm `customer_name` từ relation ERP `$this->customer->fullname`; (2) `BomListService::loadDetail` eager-load thêm `'customer'`; (3) FE `BomBuilderEditor.loadBomDetail` set thẳng `bomForm.customer_name`/`customer` từ `detail.customer_name`, bỏ call + xóa method chết `loadCustomerInfo`.
Bước tiếp theo: User reload màn edit BOM → ô Khách hàng hiện đúng tên (kể cả KH chưa sync HRM).
Blocked: Không
