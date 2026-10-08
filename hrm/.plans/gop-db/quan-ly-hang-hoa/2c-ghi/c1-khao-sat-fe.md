# Đợt 2-C1 — Khảo sát FE: Tạo + sửa hàng hoá do công ty tạo

> 07/10/2026 · khảo sát CHỈ ĐỌC (không sửa source, không ghi DB). Đọc DB `hrm_erp` bằng `SHOW COLUMNS`/`SELECT COUNT` để đối chiếu.
> Code: worktree `websites/wt-chuyen-doi-hang-hoa/{hrm-client,hrm-api}` nhánh `feat/chuyen-doi-hang-hoa` (client `e046aff2c`).
> Luật ưu tiên: `chot.md` (G1–G11, T6, H1') > ERP đang chạy > mockup `man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html`.
> Đường dẫn FE dưới đây tương đối từ `hrm-client/`, BE từ `hrm-api/`.

---

## 0. Kết luận nhanh

| # | Câu | Kết luận |
|---|---|---|
| 1 | Màn chi tiết 2-B tái dùng làm form sửa? | **Tái dùng KHUNG** (`ProductParentTabs`, `ProductStepTabs`, khung page), **KHÔNG tái dùng 6 component tab** — chúng nhận `product` (dữ liệu hiển thị: tên, chuỗi gộp), dựng toàn ô `disabled`, bảng `ProductReadonlyTable`. Form sửa cần `v-model` theo id, ô chọn có nguồn option, bảng dòng nhập tại chỗ ⇒ **tách bộ tab form riêng** `components/product/form/*`; chi tiết giữ nguyên |
| 2 | Nhánh cũ có FE form dùng lại? | **Không**. Nhánh cũ chỉ có `pages/master-data/mockup-hang-hoa/form.vue` (889 dòng, tĩnh, 1 tầng tab, đã xếp **BỎ** ở `2b-doc/tai-su-dung-nhanh-cu.md:74,228`). Chỉ còn tham khảo được: CKEditor cho ô rich text (`form.vue:315–321, 672–716`) |
| 3 | Bảng trường | mục 3 — 5 tab con + tab cha Quản trị, ~40 trường + 9 bảng dòng |
| 4 | Component dùng chung | mục 4 — có sẵn đủ: `V2BaseAttachmentSection`/`V2BaseFile`, CKEditor, `V2BaseSelectRemote`, `V2BaseSelect` multiple, `V2BaseRadio`, `V2BaseCheckbox`, `V2BaseCurrencyInput`, `scrollToFirstError`, `formValidateMixin`, `rowFieldErrors`, `unsavedChangesMixin`. **Không có** component tab 2 tầng chung — dùng 2 component riêng của 2-B |
| 5 | Màn Tính chất hàng hoá | FE `pages/master-data/product-natures/{index,AddProductNatureModal}.vue`; BE nền `BaseCatalog*` (Entity/Request/Resource/Service `ProductNature*`). Bảng `product_natures` CHƯA có cột cờ |
| 6 | Bản đồ file + ca e2e | mục 6, 7 |
| ⚠️ | Thiếu BE cho form | form-options thiếu: thuộc tính theo Loại SP, cờ phụ tùng ô tô trên `product_types`, nhóm máy, tìm hàng hoá (4 bảng con + máy), loại tài liệu kỹ thuật, đời xe; resource chi tiết thiếu `order_code_id`, `guarantee`/`guarantee_type` tách, đời xe theo model (mục 5) |

---

## 1. Màn chi tiết chỉ đọc 2-B

### 1.1 File + cấu trúc

| File | Dòng | Vai trò |
|---|---|---|
| `pages/master-data/products/_id/index.vue` | 198 | page chi tiết; `layout: 'default-sidebar'` (`:65`); gọi `GET master-data/products/{id}` (`:145`); 403/404 → `/pages/extras/404` (`:152`) |
| `components/product/detail/ProductParentTabs.vue` | 181 | **tab cha** segmented iOS, props `tabs [{key,label,svg,tip}]` + `value`, emit `change`; thumb trượt đo bằng `$nextTick + rAF` + `ResizeObserver` (`:51–78`) — **dùng lại được nguyên cho form** |
| `components/product/detail/ProductStepTabs.vue` | 127 | **tab con** dạng step, props `tabs [{key,label}]` + `value`; step trước tab đang mở hiện ✓ (`:10,19`) — **dùng lại được**, cần thêm: (a) ẩn tab xe theo G11 (truyền mảng tabs đã lọc là đủ), (b) chấm đỏ step có lỗi (CHƯA có — thêm prop `errorKeys`) |
| `components/product/detail/ProductTabGeneral.vue` | 287 | tab con 1 — ô `V2BaseInput :value=text(...) disabled` |
| `…/ProductTabSpecs.vue` | 139 | tab con 2 — rich text `v-html` trong `.v2-linked-field` (`:40,46`) |
| `…/ProductTabPurchase.vue` | 80 | tab con 3 — VAT/thuế hiện **chuỗi %** (`pct(product.vat_percent)`), không phải id thuế suất |
| `…/ProductTabVehicles.vue` | 102 | tab con 4 — 3 select multiple disabled, gọi `vehicle-options` LAZY khi mở tab (`:85–98`, page `visited.vehicles` `index.vue:23,139`). **Không có bảng Đời xe** |
| `…/ProductTabMachines.vue` | 58 | tab con 5 — Nhóm máy + bảng Máy (`v-if groupOptions.length`) |
| `…/ProductTabAdmin.vue` | 146 | tab cha Quản trị — 3+… ô + bảng nhánh catalog (STT La Mã `:73–87`); Bảo hành hiện chuỗi gộp `guarantee_text` |
| `…/ProductReadonlyTable.vue` | 84 | bảng chỉ đọc, slot `#cell-<key>` |
| `…/ProductInfoTip.vue` · `productDetailFormat.js` | 51 · 27 | icon ⓘ; `num/pct/text/selectedOptions` (số `en-US`) |

Đo Playwright MCP (07/10, hàng 3905, `e2e_assign`): tiêu đề `Chi tiết hàng hoá: TEWI-821060`; 2 tab cha; 5 step (Thông tin chung · Thông số kỹ thuật · Mua hàng · Phân loại xe · Nhóm máy); 5 khối tab 1; footer chỉ **Quay lại**; 0 ô nhập bật (trừ 1 ô topbar); badge *Đang kinh doanh* ở góc phải thẻ tab. ⇒ **Tab Phân loại xe hiện cho MỌI hàng** (chưa có cờ G11).

### 1.2 Đi vào / quay lại / footer

- Vào: 4 màn danh sách bấm Mã → `detailLink(item)` = `/master-data/products/{id}?from=<path màn>` (`components/product/ProductListPage.vue:682`).
- Quay lại: `backUrl` đọc `?from=` (chỉ nhận chuỗi bắt đầu `/master-data/products/`), mặc định `/master-data/products/warehouse` (`_id/index.vue:58–59,122–125`).
- Footer: `<V2Footer :menu="{}" :url-back="backUrl" />` (`:41`). `V2Footer` đã có sẵn nút **Sửa** qua `menu.edit` → emit `edit` (`components/V2Footer.vue:93–96`) và **Lưu** qua `menu.submit_form` → emit `submitForm` (`:14–17, 303–305`); Lưu nháp là `menu.submit_and_draft` (G3: không bật).
- Danh sách hiện **không có cột Hành động** (2-B tự chốt bỏ — `2b-doc/plan.md` "Lệch mockup"). G9a cần thêm cột `actions` + `V2BaseRowActions` (ví dụ `pages/customer-care/note-maintenances/index.vue:121–126`).

### 1.3 Quyết định tái dùng (đề xuất)

| Phần | Tái dùng? | Lý do |
|---|---|---|
| `ProductParentTabs`, `ProductStepTabs`, `ProductInfoTip`, `productDetailFormat.js` | ✅ nguyên trạng (+ prop chấm đỏ) | thuần trình bày |
| 6 component tab chi tiết | ❌ tách form riêng | bind giá trị hiển thị (`brand_name`, `guarantee_text`, `pct(vat_percent)`), không có id/option; bật edit trong cùng component là `v-if` khắp nơi, rủi ro làm hỏng màn chi tiết đã xanh e2e 6/6 |
| Page chi tiết | giữ chỉ đọc, thêm nút **Sửa** footer (`menu.edit`, theo quyền 1652 + điều kiện G9a) | G9a |
| CSS `.product-tabs-card*` (`_id/index.vue:163–198`) | chép sang page form hoặc rút thành component khung `ProductFormShell` | chưa kiểm có muốn rút chung không — đề xuất rút để chi tiết và form không lệch khuôn |

---

## 2. Nhánh cũ `feat/p1-danh-muc-hang-hoa` (hrm-client)

| File | Kết luận |
|---|---|
| `pages/master-data/mockup-hang-hoa/form.vue` (889) | BỎ — tĩnh, 1 tầng tab `b-tabs`, còn dấu tab Giá, không có tab Quản trị 4 cột. Tham khảo: dùng `V2BaseSelect` 24 chỗ, `V2BaseIconButton` cho nút +, **CKEditor 5** (`@ckeditor/ckeditor5-build-classic` + `ckeditor5-vue`) cho *Đặc điểm* — ghi chú ERP dùng `ck-editor` (`form.blade.php:880`) |
| `pages/master-data/mockup-hang-hoa/index.vue` | BỎ (2-B đã thay) |
| Các màn danh mục (product-models, order-codes, tax-rates, units, product-types…) | đã có trên nhánh chung (`pages/master-data/*/Add*Modal.vue`) ⇒ nút **+** thêm nhanh có thể mở các modal này |
| Store/update service, form request | FE không có; BE `ProductRequest` lấy khung, sửa nhiều (`yeu-cau-ghi.md` §3) |

---

## 3. Bảng trường của form (mockup §5 × chốt)

Ký hiệu cột **BB** (bắt buộc khi Lưu — G3 bỏ Lưu nháp): ✅ = bắt buộc · — = không · ❓ = chưa chốt. Theo skill `form-validate` FE chỉ `required` ô Tên; mọi bắt buộc khác BE trả 422 **một lượt đủ mọi ô** ⇒ thoả G3 "báo đồng thời".

### 3.0 Khung

| Phần | Mockup | Chốt / thực tế |
|---|---|---|
| Dải `#bao-muon` "Hàng hoá do X tạo — chỉ khai tab Quản trị" | có | **2-C2** (công ty lấy về). 2-C1 không hiện |
| Ô Mã / Trạng thái | không hiện trong form | giữ; tiêu đề `Thêm mới hàng hoá` / `Sửa hàng hoá: <mã>`; badge trạng thái góc thẻ tab như chi tiết (đề xuất) |
| Footer | Lưu nháp · Lưu · Quay lại | **Lưu · Quay lại** (G3). Lưu không đổi trạng thái (H1') |
| Toast Lưu | "…chuyển sang Chờ tính giá…" | đổi câu (G9b-4, H1'): đề xuất *"Đã lưu hàng hoá <mã>"* |

### 3.1 Tab con 1 — Thông tin chung

| Khối | Trường | Loại ô | BB | Nguồn option / cột | Hành vi |
|---|---|---|---|---|---|
| Thông tin hàng hoá | Tên hàng hoá | input | ✅ (FE + BE) | `products.name` | rule trùng tên × model × thương hiệu × hãng SX (ERP store) |
| | Model | select tìm server + nút **+** | ✅ | `option-search?type=product_models` (39.796 dòng, `ProductOptionService.php:59,98`); form-options chỉ trả bản ghi đang chọn qua `include_ids` | + mở `pages/master-data/product-models/AddProductModelModal.vue` (chưa kiểm modal chạy được trong form khác) |
| | Công ty quản lý | input disabled | — | tạo mới: công ty hiện tại; sửa: `owner_company_name` | |
| | Tên thường gọi · Tên tiếng Anh · Barcode | input | — | `common_name`, `english_name`, `barcode` | không dùng prop `trim` |
| | Ghi chú | textarea col-12 | — | `note` | |
| Phân loại | Tính chất · Nhóm chức năng · Nhóm sản phẩm | input disabled col-4×3 | — | `form-options.product_types[].path` (`ProductOptionService.php:134–168`) | **tự điền khi chọn Loại SP**, bỏ chọn ⇒ xoá trắng (mockup `plChonLoai` L6713) |
| | Loại sản phẩm | select + nút **+** col-6 | ✅ | `form-options.product_types` | đổi Loại SP ⇒ (a) điền 3 cấp cha, (b) nạp bảng thuộc tính theo loại (tab 2), (c) **G11** ẩn/hiện tab Phân loại xe theo cờ của Tính chất. ❓ có tự điền % VAT từ `product_types.vat_percent_tax_rate_id` không (bảng có cột này — `ProductType.php:27`) |
| | Đặc tính sản phẩm | select col-6 | — | `form-options.product_characteristics` (danh mục thật, không phải 4 giá trị cứng của mockup — inventory §7-15) | mockup mặc định "Hàng nhập khẩu" ⇒ đề xuất KHÔNG mặc định |
| Nguồn gốc | Thương hiệu · Xuất xứ · Hãng SX | select col-3×3 | ✅ ✅ ✅ (DB NOT NULL — `yeu-cau-ghi.md` T1; cần cho sinh mã) | `brands`, `origins`, `manufacturers` | mockup không có `*` ⇒ G3 "đủ trường bắt buộc của form" phải gồm 3 ô này (đề xuất, xem câu hỏi Q2) |
| | Code đặt hàng | select tìm server + **+** col-3 | — | `option-search?type=order_codes` | resource chi tiết **không trả `order_code_id`** (chỉ `order_code_name`, `ProductDetailResource.php:65`) |
| Đơn vị tính (bảng dòng) | Đơn vị | select trong ô | ✅ | `form-options.units` (kèm `can_be_base`) | nút header **Thêm đơn vị tính** |
| | Đơn vị cơ bản | radio 1 dòng | ✅ đúng 1 | `product_units.is_base` | G2: đúng 1 dòng hệ số 1; dòng cơ bản: hệ số = 1 disabled, không nút xoá. ❓ chỉ đơn vị `can_be_base=1` mới được tick cơ bản? |
| | Hệ số quy đổi | input số | ✅ | `unit_coefficient` | |
| | Quy đổi | chữ tự sinh | — | — | "Đơn vị cơ bản" / "1 Bộ = 2 Cái" (đã có ở `ProductTabGeneral.vue:226–231`) |
| | (xoá) | icon | | | sửa hàng cũ: xoá ĐVT đã có giá? ❓ (G2 chỉ nói bù 6 dòng giá cho đơn vị mới) |
| Tài liệu · Ảnh · Video | Tài liệu kỹ thuật | mockup: upload "Chọn tệp PDF/Word" | — | **DB thật: `product_tech_attachments(product_id, attachment_type_id)` — KHÔNG có cột file** (đo `SHOW COLUMNS`); chi tiết 2-B hiện select multiple loại tài liệu (`ProductTabGeneral.vue:128–133`); 35 dòng | ⚠️ lệch mockup ↔ ERP ⇒ câu hỏi Q4 |
| | Hình ảnh (≤10) | upload ảnh nhiều | ❓ (ERP `avatar` bắt buộc, mockup không `*`) | `product_galleries` (1.548 dòng, url **tương đối** `/uploads/products/...`) + `products.avatar` (S3 tuyệt đối) | ảnh nào là avatar? HRM tải lên S3 ⇒ url tuyệt đối trong `product_galleries` — ERP hiển thị được không: **chưa kiểm** |
| | Video | input "Dán đường dẫn video" | — | `product_videos` (2 dòng, `url` NOT NULL, `position` NOT NULL) | 1 hay nhiều link? ❓ |

### 3.2 Tab con 2 — Thông số kỹ thuật

| Khối | Trường | Loại ô | BB | Nguồn | Hành vi |
|---|---|---|---|---|---|
| Thông số cơ bản | Trọng lượng (kg) · Kích thước (D×R×C) · Định mức công lắp đặt | input số / text / số col-4×3 | — | `weight`, `size`, `norm` | |
| | Bảng thuộc tính: Thuộc tính (chữ) · Giá trị (input) · Đơn vị thuộc tính (select) · Bắt buộc (checkbox) · In tem (checkbox) · xoá | bảng dòng | ❓ giá trị bắt buộc khi cột "Bắt buộc" tick? | danh sách thuộc tính theo Loại SP: `product_type_attributes` (`ProductType.php:60–68`); đơn vị: `form-options.attribute_units` | đổi Loại SP ⇒ nạp lại dòng (giữ giá trị đã nhập của thuộc tính trùng?). Nút header **Thêm thông số** thêm thuộc tính ngoài loại? ❓. **Endpoint thiếu**: `product-types/{id}` bị gate quyền "Xem danh mục loại sản phẩm" (`Routes/api.php:73–86`) ⇒ cần `GET products/attributes-by-type` |
| Phụ kiện tiêu chuẩn · Đặc điểm | 2 ô rich text col-6 | CKEditor | — | `standard_accessories`, `product_attributes` | chi tiết đang render `v-html` |
| Công thức lắp ráp | Mã · Tên · ĐVT · Số lượng · Thành phần chính (checkbox) · xoá + nút **Chọn hàng hoá** | bảng dòng + popup chọn hàng | — | `recipe_products` | **cần popup tìm hàng hoá** (chưa có endpoint) |
| Phụ kiện mua thêm · Vật tư lắp đặt | Mã · Tên · ĐVT · SL · xoá | như trên | — | `product_has_accessories`, `product_has_install_accessories` | |
| Vật tư sửa chữa – bảo dưỡng | Mã · Tên · xoá | như trên | — | `product_has_repair_accessories` | |

### 3.3 Tab con 3 — Mua hàng

| Trường | Loại ô | BB | Nguồn | Ghi chú |
|---|---|---|---|---|
| Tên khai báo hải quan · HS Code | input | — | `customs_name`, `hs_code` | |
| SL tối thiểu nhập mua | input số | — | `min_buy_qty` | |
| % VAT | select + **+** | ✅ | `form-options.tax_rates` (`name` = "8%", `ProductOptionService.php:171–185`) | gửi `vat_percent_tax_rate_id`, BE suy `vat_percent` |
| Thuế NK không CO · có CO · chống bán phá giá | select + **+** | — | `tax_rates` | `*_tax_rate_id` |
| Hệ số tính thuế BVMT | input số | — | `environment_tax_coefficient` (NOT NULL DEFAULT 1.00) | F7: BE tự suy cờ; cờ 0 ⇒ FE hiện TRỐNG |

### 3.4 Tab con 4 — Phân loại xe (G11)

| Trường | Loại ô | BB | Nguồn | Hành vi |
|---|---|---|---|---|
| Hãng xe | select multiple + "Chọn tất cả" | **— (G11)** (mockup còn `*`) | `vehicle-options.vehicle_manufacts` (LAZY khi mở tab) | |
| Loại xe | multiple lọc theo Hãng | — | `vehicle_brands` (có `vehicle_manufact_id`) | đổi Hãng ⇒ bỏ giá trị cấp dưới không hợp lệ (mockup `dongBoXe` L3150) |
| Model xe | multiple lọc theo Hãng + Loại | — | `vehicle_models` | |
| Áp dụng tất cả đời xe cho model | checkbox col-12 | — | | |
| Bảng Hãng (rowspan) · Loại · Model · Đời xe (multiple riêng từng model + Chọn tất cả) | bảng | — | **thiếu nguồn đời xe** trong `vehicleOptions()` (`ProductOptionService.php:242–249`) và thiếu dữ liệu đời xe trong resource chi tiết | ⚠️ bẫy `th rowspan` + sticky (SO-CHOT §6) |
| **Ẩn/hiện tab** | — | — | cờ `is_auto_parts` (đề xuất) ở `product_natures`, cần đưa vào `form-options.product_types[].path` (vd `path.nature_is_auto_parts`) | hiện khi Tính chất của Loại SP đang chọn có tick. ❓ Loại SP đổi sang tính chất không tick khi tab đã có dữ liệu xe: xoá dữ liệu xe khi Lưu hay giữ (câu hỏi Q5) |

### 3.5 Tab con 5 — Nhóm máy (luôn hiện — G11)

| Trường | Loại ô | BB | Nguồn | Hành vi |
|---|---|---|---|---|
| Nhóm máy | select multiple col-12 | — | bảng `groups` — **chưa có trong form-options** | |
| Bảng Máy: STT · Mã máy · Tên máy · xoá + nút **Chọn máy** | bảng + popup | ✅ khi đã chọn ≥1 nhóm (khối chỉ hiện khi có nhóm) | máy = `products` thuộc nhóm (`productables` loại `App\Product`) — **chưa có endpoint** | bỏ nhóm ⇒ bỏ máy không còn thuộc nhóm (mockup `veKhoiMay` L3201) |

### 3.6 Tab cha — Quản trị hàng hoá

| Trường | Loại ô | BB | Nguồn | Ghi chú |
|---|---|---|---|---|
| Nhà cung cấp | multiple tìm server (chip) col-6 | — | `option-search?type=suppliers` | ghi `product_suppliers` kèm `company_id` công ty hiện tại |
| Chính sách kinh doanh | select col-6 | — | `form-options.business_policies` | |
| SL tồn kho tối thiểu · Bảo hành · Đơn vị bảo hành · Hệ số công nghệ | số · số · select Ngày/Tháng/Năm · số | — | dòng công ty (3 ô đầu); `products.tech_coefficient` (T6 chung) | mockup 6 ô ⇒ bố cục 6+6 / 3+3+3+3 (đủ 12 cột mỗi hàng). Chi tiết hiện Bảo hành gộp — resource cần trả `guarantee` + `guarantee_type` tách. 11.156 hàng `tech_coefficient = 0` vs rule `min:1` (`yeu-cau-ghi.md` §3) |
| Catalog 4 cột checkbox (Lĩnh vực · Chương · Mục · Tiểu mục) + bảng nhánh (STT La Mã · 4 cấp · nút Gỡ) | 4 cột tick có ô tìm + bảng | ❓ (C5-a "≥1 nhánh khi Lưu" vs G3 "đủ trường bắt buộc của form" — chưa nói rõ còn hiệu lực) | `catalog-options` (`ProductOptionService.php:283–316`, có `parent_id`, `is_locked`); chỉ lưu Tiểu mục | khoá ở bất kỳ cấp ⇒ không xếp thêm (B2, áp tương tự popup 2-C3); bỏ tick cấp trên ⇒ gỡ nhánh con + toast "Đã gỡ N nhánh…". Có thể tái dùng `components/product/catalog/ProductCatalogTree.vue` (431 dòng) — **chưa kiểm** hợp khuôn 4 cột không |

### 3.7 Mockup báo lỗi

- Chỉ có 1 ca: thiếu catalog (`catThieu`/`catBaoLoi`, L6629–6640): chuyển tab cha *Quản trị*, thêm class `.o-loi` lên nhãn tab cha ⇒ **chấm đỏ 7px góc phải** (CSS L373), viền đỏ cột Tiểu mục, chữ đỏ dưới khối, toast. Thiếu Tên: chỉ toast (L3349). Mockup **không** có báo lỗi cho các ô khác.
- Bản thật (G3 + skill `form-validate`): BE 422 trả mọi lỗi → map `formErrors` (key `units.0.unit_id`…) → chấm đỏ trên **cả tab cha lẫn step con** có lỗi → mở tab chứa lỗi ĐẦU TIÊN theo thứ tự tab → `scrollToFirstError(this.$el)` (`utils/scrollToFirstError.js:33`). ⚠️ Pane ẩn bằng `v-show` thì `firstVisible` bỏ qua ⇒ phải đổi tab TRƯỚC rồi `$nextTick` mới cuộn.
- Khuôn có sẵn: `V2BaseTabNavigation` có `hasError` (icon cảnh báo, `components/V2BaseTabNavigation.vue:47,52`), ví dụ `pages/assign/meeting/components/MeetingForm.vue:473` (`tabErrorFlags`). Tab hàng hoá dùng segmented/step riêng ⇒ chép ý tưởng, thêm chấm đỏ theo CSS mockup.

---

## 4. Component dùng chung có sẵn

| Nhu cầu | Component | Ví dụ đang dùng | Ghi chú |
|---|---|---|---|
| Khối tệp nhiều dòng (upload, xem trước, xoá, chặn đuôi/dung lượng) | `components/V2BaseAttachmentSection.vue` (v-model = mảng đường dẫn, `upload-url`, `error-message`) | `pages/finance/buy-service-requests/components/BuyServiceRequestForm.vue`, `customer-care/wr-quotations/components/WrQuotationForm.vue` | skill form-validate §1d. Cần endpoint upload của màn |
| Ô chọn tệp lẻ | `components/V2BaseFile.vue` (`autoUpload` → `uploadFilesToS3`, `multiple`, `accept`) | (0 thẻ `<V2BaseFile ` trong pages — chưa thấy màn dùng; skill dẫn meeting tab Biên bản) | bẫy `position:absolute` của input file |
| Ảnh đơn (logo) | `components/V2BaseImageField.vue` | `components/human-components/company/CompanyForm.vue` | 1 ảnh, không hợp ≤10 ảnh. **Không có** component lưới nhiều ảnh ⇒ ghép `V2BaseFile multiple accept=image/*` + lưới thumbnail (như `ProductTabGeneral.vue:140–151`) |
| Rich text | CKEditor 5 `<ckeditor :editor="ClassicEditor">` (`package.json:13–14`); có cả `vue-quill-editor` | 13 file nhóm `pages/training/*` (vd `courses/components/CourseForm.vue`) | **không có wrapper V2Base** ⇒ dùng trực tiếp như nhánh cũ |
| Select tìm server (đơn) | `components/V2BaseSelectRemote.vue` (`fetchFn`, `initialOption`, `minimumInputLength`) | 55 file (vd `pages/lookup/stock-companies/index.vue`) | chỉ **đơn** (`value` String/Number) ⇒ Nhà cung cấp (nhiều) phải dùng cách khác — **chưa kiểm** `V2BaseSelect` có chế độ ajax multiple |
| Select thường / nhiều | `V2BaseSelect` (`extra-settings {multiple:true}`, `keep-locked-options`, 🔒 qua `utils/select2LockedOption.js`) | chi tiết 2-B | |
| Radio | `V2BaseRadio` — option `{value,label}` (memory) | `pages/meeting/bookings/components/BookingFormModal.vue` | radio ĐVT cơ bản trong bảng |
| Checkbox | `V2BaseCheckbox` | popup 2-C3 | bẫy: bắn lại `change` khi đổi prop từ code (2-C3 đã gặp) |
| Số | `V2BaseCurrencyInput`, `V2BaseInput` | `pages/customer-care/wr-information-requests/components/WrCostTable.vue` | |
| Bảng dòng nhập tại chỗ | **không có component chung** — khuôn: `V2BaseTableScroll` + `<table class="v2-table v2-form-table">` + V2Base* trong `td` | `WrCostTable.vue` (236), `WrDeviceLinesTable.vue` (716) | lỗi theo dòng: `utils/rowFieldErrors.js`; `validateAll(null,{vmId:null})` (form-validate §3c) |
| Tab 2 tầng | không có chung; dùng `ProductParentTabs` + `ProductStepTabs` (2-B) | màn chi tiết hàng hoá | `V2BaseTabNavigation` là thanh tab thường 1 tầng |
| Validate | `utils/mixins/formValidateMixin.js` (`fieldError/hasFieldError`, gộp lỗi FE + 422), `V2BaseError` (`.v2-error`), `utils/scrollToFirstError.js` | nhóm Giữ hàng | |
| Rời trang chưa lưu | `utils/mixins/unsavedChangesMixin.js` (skill `unsaved-changes`) | `pages/customer-care/warranty-repair-handle-requests/create.vue` | |
| Menu dòng | `V2BaseRowActions` | `pages/customer-care/note-maintenances/index.vue:122` | |
| Footer | `V2Footer` (`menu.submit_form`, `menu.edit`) | chi tiết 2-B | |
| Thêm nhanh danh mục (+) | modal sẵn: `pages/master-data/{product-models,order-codes,tax-rates,product-types,units}/Add*Modal.vue` | các màn danh mục | **chưa kiểm** modal có nhúng được (props, quyền "Quản lý danh mục …" — nút + phải ẩn khi thiếu quyền) |
| Popup chọn hàng hoá | không có popup chung cho hàng hoá HRM; gần nhất `pages/assign/quotations/components/QuotationProductSearchModal.vue` (đọc ERP, kèm giá) | | không tái dùng được (giá + API ERP) ⇒ viết popup mới trên endpoint tìm hàng hoá mới |

---

## 5. Tính chất hàng hoá (G11) + khoảng trống BE

### 5.1 Màn danh mục Tính chất hàng hoá

| Lớp | File | Ghi chú |
|---|---|---|
| FE list | `pages/master-data/product-natures/index.vue` (862) | cột `code · name · barcodeTemplate · description · …` (`:341–433`); ô lọc `:313–327` |
| FE modal | `pages/master-data/product-natures/AddProductNatureModal.vue` (323) | hàng 1: Mã col-3 · Tên col-6 · Trạng thái col-3; hàng 2: **Mẫu in barcode col-6 đứng lẻ** (`:52`), Diễn giải col-12 ⇒ ô tick "Phụ tùng ô tô" đặt col-6 cạnh Mẫu in barcode là đủ 12 cột |
| BE route | `Modules/MasterData/Routes/api.php:63` (vòng `$productCatalogs`, quyền "Quản lý/Xem danh mục tính chất hàng hóa") | |
| BE Entity | `Modules/MasterData/Entities/ProductClassification/ProductNature.php` (`$fillable` `:26–36`) | thêm cột vào fillable |
| BE Request/Resource/Service | `Http/Requests/ProductClassification/ProductNatureRequest.php` (`ownRules`), `Transformers/ProductClassification/ProductNatureResource.php` (`ownFields`), `Services/ProductClassification/ProductNatureService.php` (`fillableFrom`, `catalogColumns` lịch sử, `importExtraColumns`) | hook nền `BaseCatalog*` — import/export Excel có cần cột mới không: ❓ |
| DB `product_natures` | cột hiện có: id, code, name, description, barcode_template_type, status, created_by/updated_by, timestamps | **chưa có cờ** ⇒ migration thêm `is_auto_parts tinyint default 0` |
| Nguồn form | `ProductOptionService::productTypes()` join `product_natures as n` (`:136–146`) | thêm `n.is_auto_parts` vào select + `path` |

### 5.2 Khoảng trống BE phục vụ form (để plan BE)

| Thiếu | Dùng cho |
|---|---|
| `POST master-data/products` + `PUT master-data/products/{id}` + quyền 1652 | Lưu |
| `GET products/attributes-by-type?product_type_id=` (không gate quyền danh mục) | bảng thuộc tính tab 2 |
| `GET products/item-search` (mã/tên, phân trang, loại trừ chính nó) | 4 bảng hàng con + Chọn máy |
| Nhóm máy (`groups`) trong form-options hoặc endpoint riêng | tab 5 |
| Loại tài liệu (`attachment_types`, 8 dòng) trong form-options | Tài liệu kỹ thuật (nếu giữ khuôn ERP) |
| Đời xe (`vehicle_life` + bảng nối `product_vehicle_model_has_life`) trong `vehicle-options` + resource | bảng đời xe |
| Upload ảnh/video (thư mục, S3 hay `/uploads` ERP) | tab 1 |
| Resource chi tiết bổ sung: `order_code_id`, `guarantee`, `guarantee_type`, `avatar`/gallery id, `vehicle_lives`, `can_edit` | nạp form sửa + ẩn/hiện nút Sửa (FE không biết chắc công ty hiện tại = `company_role` ⇒ để BE trả `can_edit`) |
| `can_edit` trong `ProductListResource` | Sửa ở menu dòng (G9a) |

---

## 6. Đề xuất bản đồ file FE 2-C1

| File | Mới/Sửa | Nội dung |
|---|---|---|
| `pages/master-data/products/create.vue` | mới | `layout: 'default-sidebar'`; tiêu đề `Thêm mới hàng hoá`; bọc `ProductForm mode="create"`; Quay lại `?from=` (mặc định `/master-data/products/entering`). ⚠️ route tĩnh `create` phải không bị `_id` nuốt — Nuxt ưu tiên tĩnh, kiểm `route.name` |
| `pages/master-data/products/_id/edit.vue` | mới | tiêu đề `Sửa hàng hoá: <mã>` (chỉ ghép khi đã có mã); 403/404 → trang 404; `ProductForm mode="edit"` |
| `pages/master-data/products/_id/index.vue` | sửa | footer `:menu="{ edit: canEdit }"` + `@edit` → `/_id/edit?from=…` (G9a; `can_edit` từ BE; ẩn khi trạng thái 4) |
| `components/product/form/ProductForm.vue` | mới | giữ `form` + `formErrors` (`formValidateMixin`) + `unsavedChangesMixin`; tải `form-options` (+ `include_ids` khi sửa) 1 lần; `ProductParentTabs` + `ProductStepTabs` (lọc tab xe theo G11); lưu → `validateAll(null,{vmId:null})` → POST/PUT → 422: chấm đỏ tab, mở tab lỗi đầu, `scrollToFirstError`; `V2Footer menu.submit_form` |
| `components/product/form/ProductFormGeneral.vue` | mới | tab 1 (3 card + bảng ĐVT + tài liệu/ảnh/video) |
| `components/product/form/ProductFormUnitsTable.vue` | mới | bảng ĐVT (radio cơ bản, hệ số, quy đổi, xoá) |
| `components/product/form/ProductFormSpecs.vue` | mới | tab 2 (thông số, bảng thuộc tính, 2 CKEditor, 4 bảng hàng con) |
| `components/product/form/ProductFormItemsTable.vue` | mới | 1 component cho 4 bảng hàng con (prop cột: có SL / thành phần chính) |
| `components/product/form/ProductItemPickerModal.vue` | mới | popup chọn hàng hoá (dùng chung 4 bảng + Chọn máy), khuôn `modal-popup` |
| `components/product/form/ProductFormPurchase.vue` | mới | tab 3 |
| `components/product/form/ProductFormVehicles.vue` | mới | tab 4, LAZY `vehicle-options`, lọc dây chuyền, bảng đời xe |
| `components/product/form/ProductFormMachines.vue` | mới | tab 5 |
| `components/product/form/ProductFormAdmin.vue` | mới | tab cha Quản trị (6 ô + catalog 4 cột + bảng nhánh); prop `adminOnly` sẵn cho 2-C2 |
| `components/product/detail/ProductStepTabs.vue`, `ProductParentTabs.vue` | sửa nhỏ | prop đánh dấu lỗi (chấm đỏ 7px như mockup L373) |
| `components/product/ProductListPage.vue` + `utils/product-list-screens.js` | sửa | nút **Tạo mới** (primary, `#actions`) chỉ ở màn `entering` + quyền `Xây dựng thông tin hàng hoá`; cột `actions` + `V2BaseRowActions` (Sửa khi `item.can_edit`) ở các màn có hàng của công ty (`entering`, `company`; ❓ `trading`/`warehouse`) |
| `pages/master-data/product-natures/AddProductNatureModal.vue` + `index.vue` | sửa | ô tick "Phụ tùng ô tô" col-6 + cột/lọc ❓ |
| e2e `HRM/e2e/tests/master-data/products-write.api.spec.ts` + `products-form-ui.spec.ts` | mới | ca mục 7; sửa `products-read-ui.spec.ts` (nút Sửa footer, tab xe giờ ẩn/hiện) |

## 7. Ca e2e cần có

| # | Ca | Kiểm (đo DOM/HTTP) |
|---|---|---|
| E1 | Có 1652: màn *Hàng hoá nhập thông tin* có nút **Tạo mới** → mở `/products/create`, footer đúng **Lưu · Quay lại** (không Lưu nháp) | số nút footer = 2 |
| E2 | Không 1652 (role tạm chỉ 1653 + `cache:clear`): không nút Tạo mới, không nút Sửa (menu dòng + footer chi tiết); vào thẳng `/create` → 404/403; `POST`/`PUT` → 403 | bắt route được gọi |
| E3 | Bấm Lưu form trống → mọi ô bắt buộc báo **cùng lúc** (đếm `.v2-error` có chữ ≥ số ô BB ở mọi tab), chấm đỏ ở tab cha + step có lỗi, tự mở tab lỗi đầu, không gọi lần POST thứ 2 | đếm marker theo tab |
| E4 | Tạo thành công đủ trường → toast, sang chi tiết/danh sách; hàng nằm ở *Hàng hoá nhập thông tin*, badge *Đang nhập thông tin* (H1' không đổi) | API list |
| E5 | Sửa hàng do công ty tạo → Lưu → trạng thái giữ nguyên (thử cả hàng trạng thái 1 và 3) | |
| E6 | Chọn Loại SP → 3 ô cha tự điền đúng, bỏ chọn → trống | giá trị 3 input |
| E7 | G11: Loại SP thuộc Tính chất có tick → step *Phân loại xe* hiện; đổi sang tính chất không tick → step biến mất; tab *Nhóm máy* luôn hiện; Hãng xe trống vẫn lưu được | số step 4/5 |
| E8 | ĐVT: 0 hoặc 2 dòng cơ bản → lỗi; dòng cơ bản hệ số = 1 disabled; không có nút xoá ở dòng cơ bản | |
| E9 | Nhóm máy có chọn mà bảng Máy trống → lỗi ở tab 5 | |
| E10 | Catalog (nếu C5-a còn): thiếu nhánh → mở tab Quản trị, chấm đỏ, chữ đỏ dưới khối | |
| E11 | Màn Tính chất hàng hoá: tick "Phụ tùng ô tô" lưu được, mở lại còn tick; không quyền Quản lý danh mục → ô disabled | |
| E12 | Sửa từ menu dòng và từ footer chi tiết mở cùng `/_id/edit`, Quay lại về đúng `?from` | URL |
| E13 | Rời form khi có thay đổi → popup chưa lưu | |
| E14 (API) | 2 token 2 công ty: công ty B `PUT` hàng của A (chưa lấy về) → 403; body có `code`/giá → bị bỏ qua/422 | |

---

## 8. Câu hỏi còn mở (UI + nghiệp vụ)

| # | Câu | Phương án đề xuất |
|---|---|---|
| Q1 | C5-a "Lưu phải ≥1 nhánh catalog" còn hiệu lực sau G3? (hàng cũ 3 nhưng chưa xếp catalog bấm Lưu sẽ bị chặn) | giữ (form có khối catalog `*`) |
| Q2 | Bộ bắt buộc khi Lưu: mockup `*` = Tên, Model, Loại SP, ĐVT, % VAT, Máy(khi có nhóm), catalog; DB buộc thêm Thương hiệu, Hãng SX, Xuất xứ (sinh mã cần Hãng SX). Gắn `*` cho 3 ô Nguồn gốc? | có |
| Q3 | Ảnh: `products.avatar` (ERP bắt buộc) vs *Hình ảnh ≤10* (`product_galleries`) — ảnh đầu = avatar? bắt buộc? HRM upload S3 url tuyệt đối — ERP có hiện được gallery url tuyệt đối không (chưa kiểm) | ảnh đầu tiên = avatar, không bắt buộc |
| Q4 | *Tài liệu kỹ thuật*: mockup là upload file, DB/ERP là danh sách **loại tài liệu** (`attachment_type_id`, không có file) | theo ERP: select nhiều loại tài liệu |
| Q5 | Đổi Loại SP sang Tính chất không tick "Phụ tùng ô tô" khi đã khai xe: Lưu xoá liên kết xe (`productables` 3 loại xe + đời xe) hay giữ ẩn? | xoá khi Lưu, cảnh báo trước |
| Q6 | Thuộc tính: nút *Thêm thông số* thêm thuộc tính ngoài Loại SP? "Bắt buộc" tick ⇒ Giá trị bắt buộc khi Lưu? Đổi Loại SP giữ giá trị thuộc tính trùng? | chỉ thuộc tính theo loại; giữ giá trị trùng id |
| Q7 | Chọn Loại SP có tự điền % VAT từ `product_types.vat_percent_tax_rate_id` không | điền khi ô VAT đang trống |
| Q8 | Video: 1 link hay nhiều | nhiều dòng |
| Q9 | Nút **+** thêm nhanh (Model, Loại SP, Code đặt hàng, Thuế suất) làm ở 2-C1 hay hoãn? hiện theo quyền "Quản lý danh mục …" | hoãn, chỉ làm Model (bắt buộc + 39.796 dòng) |
| Q10 | Nút Sửa ở menu dòng của màn nào: *Nhập thông tin* + *Dữ liệu hàng hoá công ty*; có ở *Kho dữ liệu* / *Đang kinh doanh* không | 2 màn công ty; chi tiết mở từ mọi màn có footer Sửa |
| Q11 | Sửa hàng CŨ của công ty có ĐVT đã có giá: cho xoá ĐVT không | không cho xoá ĐVT đã có dòng giá |
| Q12 | Cột mới Tính chất: tên cột (`is_auto_parts`), có thêm cột/lọc ở danh sách + import/export Excel không | có cột + lọc, import/export thêm cột |
| Q13 | Sau Lưu tạo mới đi đâu: chi tiết hàng vừa tạo hay về *Hàng hoá nhập thông tin* | về chi tiết (thấy mã vừa sinh) |
