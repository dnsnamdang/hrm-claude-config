# YCHG — Popup "Chọn hàng hoá" + tab "Chọn từ kho hàng tạm" — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans để triển khai từng task. Các bước dùng checkbox (`- [ ]`) để theo dõi.

**Goal:** Bổ sung thông tin giá (gate quyền giá vốn), ảnh, trạng thái và bộ lọc nâng cao cho 2 popup chọn hàng của màn YCHG `/sale/price-asking-requests/add`.

**Architecture:** Phase A độc lập trên popup "Chọn hàng hoá" (thêm cột Giá nhập gate quyền). Phase B/C trên tab "Chọn từ kho hàng tạm" của `QuotationProductSearchModal` (mode ychg): chuyển data sang endpoint `assign/product-projects?scope=ychg` phân trang server-side, thêm cột Ảnh/Trạng thái/Thông tin giá, rồi bộ lọc nâng cao. Mọi field nhạy cảm (giá vốn/estimated_price) gate bằng `isCurrentEmployeeHasPermission` ở BE, trả `null` khi không quyền; FE cờ fail-closed.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api, nwidart modules); Nuxt 2 / Vue 2 / Bootstrap-Vue (hrm-client); V2Base* components.

**Spec:** `HRM/.plans/ychg-chon-hang-kho-tam/design.md`

## Global Constraints

- Cờ quyền FE fail-closed: khởi tạo `false`, chỉ set từ field BE; TUYỆT ĐỐI không hard-code `= true` (`grep -nE 'can[A-Za-z]*\s*=\s*true'` phải rỗng trên file sửa).
- BE gate dữ liệu nhạy cảm (giá vốn) bằng `isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá')`, trả `null` nếu không quyền — defense-in-depth, không dựa FE ẩn.
- Element form màn mới = `V2Base*`; select trong popup = `V2BaseSelectInModal`. KHÔNG HTML thô.
- Số định dạng quốc tế: FE `Number(x).toLocaleString('en-US')`, null → "—". KHÔNG `vi-VN` cho số.
- Icon Info = `ri-information-line` + `b-popover custom-class="info-popover"`.
- Badge trạng thái = `V2BaseBadge :color="…_color"`, chữ+màu do BE trả. KHÔNG map số→chữ ở FE.
- Nút chỉ-icon trong toolbar (Cấu hình cột) thêm `btn-compact`; cụm nút `mr-2 mb-2`, nút cuối `mb-2`.
- Hiệu năng: KHÔNG `per_page` khổng lồ / lọc client cho danh sách lớn; search server-side có `page`/`per_page`; ô tìm debounce ≥300ms + cancel request cũ.
- Tài liệu/thao tác chỉ trong `HRM/`. KHÔNG commit/đẩy git (trừ khi user yêu cầu).
- BẮT BUỘC grep pattern trong project trước khi dựng UI mới; nút cấu hình cột, thumbnail ảnh, badge đều phải copy pattern sẵn có (ghi `copy từ <file:dòng>` trong task).

## Review Focus

- **Không có quyền "Xem giá vốn" (CHỈ Phase A)**: cột Giá nhập PHẢI ẩn và `cost_price` = `null` từ BE ở endpoint `product-options` (không rò qua network tab). Test gate 1 endpoint này. (Rủi ro lộ giá vốn — cao nhất.) Lưu ý Phase B KHÔNG gate (estimated_price không phải giá vốn).
- **Hàng tạm nguồn BOM hoặc Báo giá chưa trúng thầu / không do user tạo Báo giá**: cụm "Thông tin giá" PHẢI hiện "—". Test điều kiện `is_won && quotation_created_by===me && sourceType==='quotation'`.
- **Keyword rỗng + danh sách kho hàng tạm lớn**: phân trang server-side trả đúng trang, không rơi về `per_page=1000`/lọc client. Test `scope=ychg` phân trang.
- **Hàng tạm trong phiên nháp (`sessionTempGoods`) chưa lưu DB**: vẫn phải xuất hiện (ghim nhóm riêng) khi endpoint server không trả chúng. Test gộp 2 nguồn.
- **Chọn dòng cha có con ghép bộ**: chọn cha vẫn copy đủ con sau khi đổi sang `scope=ychg`. Test picker chỉ lấy cha + copy con.

---

## PHASE A — Popup "Chọn hàng hoá": cột Giá nhập gate quyền

### Task A1: BE — PriceAskingAccess thêm `hasCost()`

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceAskingAccess.php`
- Reference pattern: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceCalculateRequestAccess.php:23,54`

**Interfaces:**
- Produces: `PriceAskingAccess::hasCost(): bool` — `isCurrentEmployeeHasPermission(self::PERMISSION_COST)`, hằng `PERMISSION_COST = 'Xem giá vốn hàng hoá'`.

- [ ] **Step 1:** Thêm hằng `PERMISSION_COST = 'Xem giá vốn hàng hoá'` và method `hasCost(): bool { return isCurrentEmployeeHasPermission(self::PERMISSION_COST); }` vào `PriceAskingAccess`, copy đúng mẫu `PriceCalculateRequestAccess`.
- [ ] **Step 2:** Verify bằng tinker/route tạm: user có quyền → `true`, không quyền → `false`.

### Task A2: BE — Reader trả `cost_price` gate quyền + controller trả `can_view_cost_price`

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceAskingProductReader.php` (quanh dòng 206 nơi set `retail_price`; constructor đã có `ProductPriceReader $prices`)
- Modify: `hrm-api/Modules/MasterData/Http/Controllers/V1/PriceCalculation/PriceAskingRequestController.php:68` (`productOptions`)

**Interfaces:**
- Consumes: `ProductPriceReader::costPrices(array $productIds, int $companyId): array` (ProductPriceReader.php:96); `PriceAskingAccess::hasCost()` (Task A1).
- Produces: mỗi dòng option thêm `cost_price` (số|null); meta response thêm `can_view_cost_price` (bool).

- [ ] **Step 1 (test):** Viết test/kịch bản API: gọi `product-options` với user CÓ quyền → mỗi item có `cost_price` numeric, meta `can_view_cost_price=true`; user KHÔNG quyền → `cost_price=null`, meta `false`.
- [ ] **Step 2:** Chạy, xác nhận FAIL (chưa có field).
- [ ] **Step 3:** Reader: nhận cờ `canCost` (truyền từ controller) → nếu `canCost` gọi `costPrices(ids, companyId)` gắn `cost_price` mỗi dòng, ngược lại `cost_price=null` và KHÔNG query giá vốn. Áp cho CẢ nhánh `ids` lẫn nhánh `search`.
- [ ] **Step 4:** Controller `productOptions`: `$canCost = $access->hasCost();` truyền vào reader; thêm `can_view_cost_price => $canCost` vào meta cả 2 nhánh.
- [ ] **Step 5:** Chạy lại 2 kịch bản → PASS. Tự kiểm: user không quyền, dump query log không có truy vấn bảng giá vốn.

### Task A3: FE — PriceAskingProductPickerModal thêm cột Giá nhập + toggle phiên

**Files:**
- Modify: `hrm-client/components/sale/price-asking/PriceAskingProductPickerModal.vue`
- Grep trước: pattern nút "Cấu hình cột hiển thị" (`btn-compact`) + cơ chế ẩn/hiện cột đã có trong project (danh sách V2BaseDataTable). Ghi `copy từ <file:dòng>`.

**Interfaces:**
- Consumes: field `cost_price` + meta `can_view_cost_price` (Task A2).

- [ ] **Step 1:** Cờ `canViewCostPrice: false` (data, fail-closed); set từ `meta.can_view_cost_price` sau mỗi lần load options.
- [ ] **Step 2:** State `showCostColumn: true` (phiên, không persist). Computed `columns` chỉ chèn cột `cost_price` ("Giá nhập") khi `canViewCostPrice === true && showCostColumn`. Format `Number(v).toLocaleString('en-US')`, null → "—".
- [ ] **Step 3:** Nút icon "Cấu hình cột hiển thị" (`btn-compact`) ở thanh trên bảng, chỉ render khi `canViewCostPrice`; bấm toggle `showCostColumn`. Bám pattern đã grep (dropdown checkbox cột nếu project đã có; nếu chỉ 1 cột toggle thì nút toggle đơn giản theo đúng pattern gần nhất).
- [ ] **Step 4 (Playwright):** Mở `http://127.0.0.1:3000/sale/price-asking-requests/add`, bấm "Chọn hàng hoá": user có quyền thấy cột Giá nhập + nút cấu hình, toggle ẩn/hiện chạy, số đúng format; (nếu dựng được user không quyền) cột ẩn, network `product-options` trả `cost_price:null`. Mở lại popup → về mặc định hiện.
- [ ] **Step 5:** Tự kiểm grep `can[A-Za-z]*\s*=\s*true` trên file → rỗng.

---

## PHASE B — Tab "Chọn từ kho hàng tạm": data server-side + 3 cột mới + Model search

### Task B1: BE — ProductProjectController: keyword gồm model + trả đủ field

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php` (`applyKeyFilters` ~260; `transformItem` ~634; `transformQuotationItem` ~698)

**Interfaces:**
- Produces: mỗi dòng (scope=ychg) có: `galleries`, `estimated_price` (số — KHÔNG gate), `quoted_price`, `erp_sync_status_name`/`_color`, `model_name`, `brand_name`, `source_type`, `is_won` (bool, suy từ quotation status 7), `quotation_created_by` (id người tạo Báo giá nguồn).

> **Quyết định (builder-check 2026-11-03):** `estimated_price` KHÔNG phải giá vốn → KHÔNG gate quyền, KHÔNG null field, giữ nguyên endpoint cho màn danh sách dự án / export / picker BOM-Báo giá cũ (không regress).

- [ ] **Step 1 (test):** Kịch bản API `GET assign/product-projects?scope=ychg&keyword=<model>&page=1&per_page=20`: trả đúng dòng khớp model; mỗi dòng có đủ field trên (bao gồm `is_won`, `quotation_created_by`); phân trang hoạt động.
- [ ] **Step 2:** Chạy → FAIL (model-in-keyword chưa có / field `is_won`/`quotation_created_by` thiếu).
- [ ] **Step 3:** `applyKeyFilters`: mệnh đề keyword thêm `orWhere` theo model (`pm.name`/alias model đã join trong buildQuery) cạnh code+name hiện có.
- [ ] **Step 4:** `transformQuotationItem`/`transformItem`: bổ sung `is_won` (quotation status 7) + `quotation_created_by` (người tạo Báo giá nguồn). KHÔNG đổi field cũ, KHÔNG gate `estimated_price`.
- [ ] **Step 5:** Chạy lại → PASS. Xác nhận màn danh sách dự án + export + picker BOM/Báo giá cũ không đổi hành vi.

### Task B2: FE — loadReuseRows dùng scope=ychg phân trang + quick search model + ghim session

**Files:**
- Modify: `hrm-client/pages/assign/quotations/components/QuotationProductSearchModal.vue` (`loadReuseRows` ~1177; `filteredReuseRows` ~808; `reuseSearch`; placeholder ô tìm)

**Interfaces:**
- Consumes: endpoint `assign/product-projects?scope=ychg&page=&per_page=&keyword=` (Task B1).

- [ ] **Step 1:** `loadReuseRows` (nhánh ychg): gọi `scope=ychg` + `page`/`per_page` + `keyword`; BỎ `only_temp=1&per_page=1000` và BỎ lọc client theo code/name. Debounce `reuseSearch` ≥300ms + cancel request cũ (dùng pattern cancel đã có trong project — grep).
- [ ] **Step 2:** `sessionTempGoods` (hàng tạm trong phiên nháp) tách thành nhóm ghim đầu bảng (client), nhãn "Trong phiếu"; không bị endpoint server ghi đè.
- [ ] **Step 3:** Placeholder ô tìm nhanh: "Tìm theo mã / tên / model hàng tạm". (Phase B không cần cờ quyền giá vốn.)
- [ ] **Step 4 (Playwright):** Mở popup "Thêm hàng tạm" → tab "Chọn từ kho hàng tạm": gõ model thấy lọc đúng (server), phân trang hoạt động, hàng tạm trong phiếu hiện ở nhóm ghim. Chọn 1 dòng cha có con ghép bộ → thêm vào phiếu copy đủ con (không regress).

### Task B3: FE — 3 cột Ảnh / Trạng thái / Thông tin giá

**Files:**
- Modify: `hrm-client/pages/assign/quotations/components/QuotationProductSearchModal.vue` (bảng reuse ~315-396)
- Reuse: `hrm-client/components/product/TempGalleryThumb.vue` (ảnh zoom); `V2BaseBadge` (trạng thái)

**Interfaces:**
- Consumes: `row.galleries`, `row.erp_sync_status_name/_color`, `row.estimated_price`, `row.quoted_price`, `row.is_won`, `row.quotation_created_by`, `row.sourceType` (Task B1).

- [ ] **Step 1:** Cột **Hình ảnh**: `<TempGalleryThumb :galleries="row.galleries" />`.
- [ ] **Step 2:** Cột **Trạng thái**: `<V2BaseBadge :color="row.erp_sync_status_color">{{ row.erp_sync_status_name }}</V2BaseBadge>`.
- [ ] **Step 3:** Cột **Thông tin giá**: computed per-row hiện `giá nhập – giá bán` CHỈ khi `row.sourceType==='quotation' && row.is_won && row.quotation_created_by===currentEmployeeId`; còn lại "—". Format `toLocaleString('en-US')`. KHÔNG gate quyền giá vốn (estimated_price không phải giá vốn). (Lấy `currentEmployeeId` từ store theo pattern có sẵn — grep.)
- [ ] **Step 4 (Playwright):** Dòng Báo giá trúng thầu do chính user tạo Báo giá → hiện cụm giá; dòng BOM / báo giá người khác tạo / chưa trúng thầu → "—". Ảnh click phóng to. Badge trạng thái đúng màu BE.

---

## PHASE C — Bộ lọc nâng cao tab kho hàng tạm

### Task C1: BE — thêm filter source_type / quotation_id / bom_list_id / structure

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php` (`applyKeyFilters` + union buildQuery)

**Interfaces:**
- Produces: endpoint nhận thêm `source_type` (all|bom|quotation), `quotation_id`, `bom_list_id`, `structure` (all|standalone|parent|recipe).

- [ ] **Step 1 (test):** Kịch bản API cho từng filter: `source_type=quotation` chỉ trả dòng báo giá; `quotation_id=X`/`bom_list_id=Y` lọc đúng nguồn; `structure=recipe` chỉ trả cha có `recipe_products.base_product_id=p.id`, `standalone` không con/không recipe.
- [ ] **Step 2:** Chạy → FAIL.
- [ ] **Step 3:** Thêm các mệnh đề filter vào `applyKeyFilters`/union. `structure`: `recipe` = tồn tại `recipe_products.base_product_id`; `parent` vs `recipe` phân biệt theo quyết định ở Step 0 (xác nhận định nghĩa "Hàng Cha" vs "ghép bộ" với user nếu dữ liệu không tách bạch — xem design §9); `standalone` = không con + không recipe. Lưu ý picker reuse đang `whereNull parent_id` → nới cho filter `parent` nếu cần.
- [ ] **Step 4:** Chạy lại → PASS.

### Task C2: BE — endpoint options cho dropdown nguồn (nếu chưa có)

**Files:**
- Modify/Create: endpoint autocomplete Dự án / Báo giá nguồn / Bomlist nguồn / Thương hiệu (grep xem đã có `search?limit=` dùng lại được chưa — ưu tiên tái dùng, KHÔNG tạo mới nếu đã có).

**Interfaces:**
- Produces: option list server-side có `limit`, trả `{id, text}` cho từng dropdown.

- [ ] **Step 1:** Grep endpoint options sẵn có (project list đã có cho nhân viên/hàng hoá). Nếu đủ → ghi lại, bỏ task. Nếu thiếu dropdown nào → bổ sung endpoint search `limit` cho đúng dropdown đó.
- [ ] **Step 2:** Verify từng endpoint trả đúng, có phân trang/limit.

### Task C3: FE — khối bộ lọc nâng cao trên bảng kho hàng tạm

**Files:**
- Modify: `hrm-client/pages/assign/quotations/components/QuotationProductSearchModal.vue` (thêm khối filter phía trên bảng reuse)
- Dùng: `V2BaseSelectInModal` cho mọi select trong popup.

**Interfaces:**
- Consumes: filter params của Task C1; options của Task C2.

- [ ] **Step 1:** Thêm khối filter: Dự án (autocomplete), Báo giá nguồn, Bomlist nguồn, Thương hiệu, Nguồn (Tất cả/Từ BOM Giải pháp/Từ Báo giá), Trạng thái cấu trúc (Tất cả/Độc lập/Cha/Ghép bộ), Model — tất cả `V2BaseSelectInModal`/`V2BaseInput`. Placeholder theo quy ước list-page.
- [ ] **Step 2:** Gửi tham số xuống `loadReuseRows` (giữ phân trang server-side, debounce). Đổi filter → reset về trang 1.
- [ ] **Step 3 (Playwright):** Mỗi filter lọc đúng, kết hợp nhiều filter + quick search cùng lúc; đổi filter reset trang; không regress chọn dòng.
- [ ] **Step 4:** Tự kiểm grep HTML thô (`<select `/`<input ` không V2Base) trên khối mới → rỗng; cờ quyền `= true` → rỗng.

---

## Self-review notes

- Spec coverage: Phase A = popup "Chọn hàng hoá" + Giá nhập gate + toggle phiên (✓). Phase B = quick search model + 3 cột (✓) + chuyển data server-side (quyết định §3.4). Phase C = toàn bộ bộ lọc nâng cao (✓).
- Điểm cần user xác nhận trước khi code Phase C: định nghĩa "Hàng Cha" vs "Hàng công thức lắp ghép bộ" (design §9) — Task C1 Step 3 chặn ở đây.
- Đã chốt qua builder-check (2026-11-03): `estimated_price` KHÔNG phải giá vốn → Phase B không gate; chủ sở hữu cụm giá = `quotations.created_by` (người tạo Báo giá nguồn).
