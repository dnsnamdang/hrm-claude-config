# YCHG — Nâng cấp popup "Chọn hàng hoá" + tab "Chọn từ kho hàng tạm"

> Màn áp dụng: `/sale/price-asking-requests/add` (và `/edit`) — luồng Yêu cầu hỏi giá (YCHG).
> Breadcrumb: Bán hàng › Yêu cầu › Hàng hóa › YC hỏi giá › Thêm hàng tạm › Chọn từ kho hàng tạm.

## 1. Mục đích & bối cảnh

Khi lập YCHG, người dùng thêm hàng vào phiếu qua 2 lối:
- **"Chọn hàng hoá"** → popup `PriceAskingProductPickerModal` (hàng ERP đang nhập/đang kinh doanh của công ty).
- **"Thêm hàng tạm"** → overlay `QuotationProductSearchModal` (mode `ychg`) gồm 2 tab: **Thêm mới** và **Chọn từ kho hàng tạm (Tái sử dụng)**.

Yêu cầu nâng cấp: bổ sung thông tin giá (gate quyền giá vốn), ảnh, trạng thái, và bộ lọc để chọn hàng nhanh/đúng hơn — đặc biệt ở tab kho hàng tạm hiện chỉ có ô tìm nhanh theo mã/tên.

## 2. Hiện trạng (đã rà code)

### 2.1 Popup "Chọn hàng hoá"
- FE: `hrm-client/components/sale/price-asking/PriceAskingProductPickerModal.vue` — modal `V2BaseModal` + `V2BaseDataTable`, cột: check / Mã / Tên / Model / Thương hiệu—Hãng / Trạng thái. Tick giữ qua trang, phân trang server.
- BE: `GET master-data/price-asking-requests/product-options` → `PriceAskingRequestController@productOptions` → `PriceAskingProductReader::search()`.
  - Keyword **đã** search `p.code`, `p.name`, `pm.name` (model) — mục "quick search theo Model" ĐÃ ĐẠT.
  - Reader trả `retail_price` (giá bán lẻ) nhưng **CHƯA trả giá vốn/giá nhập**.
  - Reader đã inject `ProductPriceReader $prices`; reader này có sẵn `costPrices(array $ids, int $companyId)`.
  - Quyền giá vốn: `'Xem giá vốn hàng hoá'` (đã tồn tại, nhóm "Báo giá", type 4). Mẫu gate: `PriceCalculateRequestAccess::hasCost()` = `isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá')`.

### 2.2 Tab "Chọn từ kho hàng tạm (Tái sử dụng)"
- FE: `hrm-client/pages/assign/quotations/components/QuotationProductSearchModal.vue`, method `loadReuseRows()`.
  - Hiện gọi `GET assign/product-projects?only_temp=1&prospective_project_id={projectId}&per_page=1000` (**chỉ dự án gắn trên phiếu**) + gộp hàng tạm trong phiên nháp (`sessionTempGoods`).
  - Lọc **client-side** chỉ theo mã/tên (`filteredReuseRows`). Bảng cột: Mã / Tên / Model / Thương hiệu / Xuất xứ / ĐVT / Nguồn (badge BOM|Báo giá) / Dự án. YCHG chọn 1 dòng (radio).
  - Data mỗi dòng **đã có** `galleries`, `estimated_price`, `quoted_price`, `model_name`, `brand_name`, `source_type` nhưng chưa render Ảnh/Trạng thái/Giá.
- BE: `Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php`.
  - **Đã có sẵn** `scope=ychg` = hàng tạm MỌI dự án user được xem (`ProspectiveProject::visibleIdsQuery()`), KHÔNG cần `prospective_project_id`.
  - `applyKeyFilters()` đã hỗ trợ server-side: `keyword` (code+name), `model_id`, `brand_id`, `origin_id`, `unit_id`, `prospective_project_id`, `solution_id`, `created_by`, `erp_sync_status`. Có phân trang.
  - Picker reuse chỉ lấy **hàng tạm cha** (`whereNull erp_product_id` + `whereNull parent_id`); chọn cha tự copy con.
  - `transformItem/transformQuotationItem` trả: `galleries`, `estimated_price`, `quoted_price`, `erp_sync_status_name`/`_color`, `model_name`, `brand_name`, `source_type`.
  - **Chưa có** filter: Nguồn (`source_type`), Báo giá nguồn (`quotation_id`), Bomlist nguồn (`bom_list_id`), Trạng thái cấu trúc (độc lập/cha/ghép bộ); keyword chưa gồm model.

## 3. Quyết định đã chốt (user + đề xuất)

1. **Phạm vi đợt này**: làm **cả 2 popup** (user chốt).
2. **Nút ẩn/hiện cột**: **chỉ toggle trong phiên**, không lưu per-user (user chốt).
3. **UI**: **theo skill HRM** (SKILL thắng SPEC về hình thức) — giống popup báo giá ERP về ý tưởng, không copy pixel (user chốt).
4. **Nguồn data tab kho hàng tạm** (user giao "tự quyết"): **chuyển sang `scope=ychg` + phân trang + lọc server-side**, bỏ `only_temp=1&per_page=1000` lọc client. Hàng tạm trong phiên nháp ghim nhóm riêng ở đầu bảng (client).
5. **Cột Thông tin giá** (chốt sau builder-check 2026-11-03):
   - **`estimated_price` KHÔNG phải "giá vốn" nhạy cảm** → **KHÔNG gate** theo quyền `Xem giá vốn hàng hoá` ở Phase B. Chỉ dùng làm "giá nhập" của cụm Thông tin giá (giá ước tính từ nguồn báo giá). Endpoint `assign/product-projects` giữ nguyên hành vi cũ cho màn danh sách dự án / export / picker BOM-Báo giá — KHÔNG regress.
   - Việc gate quyền giá vốn **chỉ áp ở Phase A** (`cost_price` thật của popup "Chọn hàng hoá", lấy từ `ProductPriceReader::costPrices`).
   - **Giá nhập** = `estimated_price`; **Giá bán** = `quoted_price`.
   - **Chỉ hiện cụm giá** cho dòng **nguồn Báo giá đã TRÚNG THẦU và do chính user tạo**; "do chính user tạo" = **`quotations.created_by` (người tạo Báo giá nguồn) == `employees.id` người đăng nhập**. Dòng khác (BOM / báo giá người khác / chưa trúng thầu) hiện "—".
6. **Cột Trạng thái** (tab kho hàng tạm): dùng badge `erp_sync_status_name`/`_color` sẵn có (Đã đồng bộ / Chưa đồng bộ).
7. **Cột Hình ảnh**: component `components/product/TempGalleryThumb.vue` (click phóng to qua `openFilePreviewModal`).
8. **Trạng thái cấu trúc (Phase C, user chốt 2026-11-03 "theo đề xuất")**: dropdown chỉ **3 lựa chọn** — `Tất cả` / `Hàng độc lập` (top-level không có dòng con) / `Hàng cha – ghép bộ` (top-level có dòng con qua `parent_id`). **Gộp "Hàng Cha" + "Hàng công thức lắp ghép bộ" làm một** vì điều tra dữ liệu thật: `recipe_products.base_product_id` chỉ trỏ `products.id` (sản phẩm danh mục, 6213/6213 dòng), còn hàng tạm trong picker (`erp_product_id` NULL) có **0** dòng là recipe → option "công thức lắp ghép bộ" theo `recipe_products` sẽ LUÔN rỗng. Tín hiệu cấu trúc duy nhất khả dụng cho hàng tạm là `parent_id`. KHÔNG dùng `recipe_products` cho filter này. (Thay thế điểm "cần xác nhận" ở §9.)

## 4. Phân phase

- **Phase A** — Popup "Chọn hàng hoá": cột **Giá nhập** gate quyền + toggle ẩn/hiện trong phiên. (Nhỏ, độc lập, làm trước.)
- **Phase B** — Tab kho hàng tạm (lõi): chuyển `scope=ychg` + phân trang server-side + quick search thêm Model + 3 cột mới (Ảnh / Trạng thái / Thông tin giá). Hàng tạm trong phiên ghim riêng.
- **Phase C** — Bộ lọc nâng cao đầy đủ: Dự án, Báo giá nguồn, Bomlist nguồn, Thương hiệu, Nguồn (Tất cả/BOM/Báo giá), Trạng thái cấu trúc, Model.

Chi tiết từng phase: `design-phaseA.md`, `design-phaseB.md`, `design-phaseC.md` (viết khi bắt tay phase đó). Dưới đây là spec đủ để lập plan.

---

## 5. Phase A — chi tiết

### BE
- `PriceAskingAccess`: thêm `hasCost(): bool` = `isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá')` (inject `PermissionService`, hoặc tạo `PriceAskingRequestAccess` nhỏ như mẫu `PriceCalculateRequestAccess`). Đặt hằng `PERMISSION_COST = 'Xem giá vốn hàng hoá'`.
- `PriceAskingProductReader`:
  - `search()`/`rows()`/`enrich()` nhận cờ `canCost` (hoặc đọc qua access) → mỗi dòng thêm `cost_price` = `canCost ? costPrices([...])[id] ?? null : null`.
  - Giữ fail-closed: không quyền → field = `null`, KHÔNG query giá vốn.
- `productOptions()`: truyền `canCost` vào reader; thêm `can_view_cost_price` vào meta response (cả nhánh `ids` lẫn nhánh `search`).

### FE — `PriceAskingProductPickerModal.vue`
- Thêm cột `cost_price` ("Giá nhập") vào `columns`, format số chuẩn quốc tế (`toLocaleString('en-US')`), null → "—".
- Cờ `canViewCostPrice: false` (fail-closed), set từ meta `can_view_cost_price` sau `search()`. Cột chỉ thêm vào `columns` khi `canViewCostPrice === true`.
- **Toggle ẩn/hiện trong phiên**: nút icon "Cấu hình cột hiển thị" (btn-compact) ở thanh trên bảng, chỉ hiện khi `canViewCostPrice`. State `showCostColumn` (mặc định true), không lưu — mở lại popup về mặc định. Bám pattern cấu hình cột đã có trong project (grep trước khi tự dựng).
- `addProducts`: không đổi (cột giá chỉ để tham khảo lúc chọn).

## 6. Phase B — chi tiết

### BE — `ProductProjectController`
- Keyword gồm model: trong `applyKeyFilters`, mệnh đề keyword thêm `orWhere pm.name/model` (hoặc join product_models alias có sẵn trong buildQuery). Giữ nguyên code+name.
- `source_type` filter (chuẩn bị cho Phase C nhưng Phase B có thể cần "Nguồn"): lọc union theo bom|quotation. (Có thể để sang Phase C.)
- Đảm bảo `scope=ychg` trả `estimated_price`, `quoted_price`, `galleries`, `erp_sync_status_*`, `source_type`, cờ "đã trúng thầu" (`is_won` suy từ quotation status 7), và **`quotation_created_by`** (= người tạo Báo giá nguồn) để FE so với người đăng nhập quyết hiện cụm giá. Nếu transform chưa trả các field này thì bổ sung (chỉ thêm field, không đổi cũ).
- **KHÔNG gate `estimated_price`** (đã chốt: không phải giá vốn) → giữ nguyên endpoint, không null field, không đụng màn danh sách dự án / export / picker cũ.

### FE — `QuotationProductSearchModal.vue` (mode ychg)
- `loadReuseRows()` (YCHG): đổi sang `GET assign/product-projects?scope=ychg&page=&per_page=` + tham số lọc; **phân trang server-side** (bỏ `per_page=1000`, bỏ filter client theo code/name). Debounce ô tìm ≥300ms + cancel request cũ.
- **Hàng tạm trong phiên nháp** (`sessionTempGoods`): tách thành nhóm ghim ở đầu bảng (client), nhãn "Trong phiếu".
- Ô tìm nhanh placeholder: "Tìm theo mã / tên / model hàng tạm".
- Thêm 3 cột:
  - **Hình ảnh**: `<TempGalleryThumb :galleries="row.galleries" />` (đã có zoom).
  - **Trạng thái**: `<V2BaseBadge :color="row.erp_sync_status_color">{{ row.erp_sync_status_name }}</V2BaseBadge>`.
  - **Thông tin giá**: hiện `giá nhập – giá bán` chỉ khi `row.sourceType==='quotation' && row.is_won && row.quotation_created_by===currentEmployeeId`. Khác → "—". Format số chuẩn quốc tế. **Không gate quyền giá vốn** ở cụm này (estimated_price không phải giá vốn).

## 7. Phase C — chi tiết

### BE — thêm filter vào `applyKeyFilters`/union
- `source_type` = `all` | `bom` | `quotation` → lọc union (Nguồn).
- `quotation_id` → `q.id` (Báo giá nguồn); `bom_list_id` → `b.id` (Bomlist nguồn).
- **Trạng thái cấu trúc**: `structure` = `standalone` | `parent` | `recipe`:
  - `recipe` = hàng là cha có dòng `recipe_products.base_product_id = p.id` (công thức ghép bộ).
  - `parent` = có con qua `parent_id` nhưng không phải recipe (xác nhận định nghĩa khi làm — hiện picker đã `whereNull parent_id`, cần nới cho filter này).
  - `standalone` = không con, không recipe.
  - ⚠️ Điểm cần làm rõ khi code: phân biệt "Hàng Cha" (parent_id) vs "Hàng công thức lắp ghép bộ" (recipe_products) — xác nhận lại với user nếu dữ liệu không tách bạch.
- Các dropdown nguồn (Dự án, Báo giá, Bomlist, Thương hiệu) cần endpoint options gọn (autocomplete server-side, không load toàn bộ).

### FE — khối bộ lọc nâng cao trên bảng kho hàng tạm
- Dropdown: Dự án (autocomplete tên/mã), Báo giá nguồn, Bomlist nguồn, Thương hiệu, Nguồn (select Tất cả/BOM/Báo giá), Trạng thái cấu trúc (Tất cả/Độc lập/Cha/Ghép bộ), Model.
- Dùng `V2BaseSelectInModal` (select trong modal/popup). Placeholder theo quy ước list-page. Gửi tham số xuống endpoint, phân trang giữ nguyên.

## 8. Non-goals / Anti-goals
- KHÔNG lưu cấu hình cột per-user (chỉ toggle phiên).
- KHÔNG copy pixel layout popup ERP; theo component/skill HRM.
- KHÔNG để lộ giá vốn khi không có quyền (fail-closed cả BE lẫn FE).
- KHÔNG dùng `per_page` khổng lồ / lọc client cho danh sách lớn.
- KHÔNG đụng luồng duyệt PTKD / hiển thị hàng con (đã xong ở feature trước `ychg-hien-hang-con`).

## 9. Rủi ro / điểm cần xác nhận khi code
- Định nghĩa "Hàng Cha" vs "Hàng công thức lắp ghép bộ" ở Trạng thái cấu trúc (Phase C) — **vẫn để xác nhận lúc code Task C1**.
- Khi chuyển `scope=ychg`, kiểm lại hành vi "chọn cha tự copy con" vẫn đúng (picker chỉ lấy cha).

**Đã giải quyết qua builder-check (2026-11-03):**
- ~~estimated_price có phải giá vốn~~ → **KHÔNG**, không gate (quyết định §3.5).
- ~~Chủ sở hữu cụm giá~~ → **người tạo Báo giá nguồn** (`quotations.created_by`) (quyết định §3.5).
- **Nhãn cột "Giá nhập" (quyết định của mình):** Phase A popup "Chọn hàng hoá" dùng "Giá nhập" = `cost_price` (giá vốn thật, gate quyền); Phase B cụm giá dùng "giá nhập" = `estimated_price` (ước tính từ báo giá, không gate). Hai popup khác nhau, ngữ cảnh khác nhau → giữ nhãn "Giá nhập" ở cả hai, không đổi tên. Nếu khi nghiệm thu user thấy khó hiểu thì tách nhãn sau (thay đổi nhỏ, không ảnh hưởng data).
