# Plan — Popup chọn hàng hoá theo công ty (Redmine #11286)

**Mục tiêu:** Popup "Chọn hàng hoá" ở 3 nơi (Báo giá HRM, Bomlist HRM, Báo giá ERP) có thêm cột
Nguồn hàng / Lĩnh vực / Chương, bộ lọc theo Công ty, và giá bán luôn là giá của công ty ghi trên chứng từ.

**Spec đầy đủ:** `docs/superpowers/specs/2026-09-11-popup-hang-hoa-theo-cong-ty-design.md`
**Phụ trách:** @khoipv · **Nhánh:** `fix-bug-11092026` (hrm-api, hrm-client, erp)

## Ràng buộc chung (áp cho mọi task)

- Công thức giá duy nhất: `giá gốc theo price_type × hệ số công ty`, làm tròn
  `ROUND(price * coefficient / 1000) * 1000`. Thiếu hệ số → giữ nguyên giá gốc, KHÔNG ghi 0.
- Hệ số lấy theo `quotations.company_id` / `bom_lists.company_id` (công ty trên chứng từ),
  KHÔNG theo người đăng nhập. Popup lúc tạo mới dùng công ty người đăng nhập.
- Bộ lọc công ty dùng tham số **`source_company_id`**, tuyệt đối không tái dùng `company_id`
  (`company_id` bên ERP đang mang nghĩa "công ty tính giá").
- `getUnitOptions()` / `getRetailPrices()` thêm tham số cuối `$companyId = null`; không truyền thì
  hành vi y như cũ.
- Không migration, không cột mới. 3 thông tin mới chỉ hiển thị trong popup.
- Select trong modal dùng `V2BaseSelectInModal` (theo `.claude/skills/modal-popup/SKILL.md`).
- Không commit khi user chưa yêu cầu.

---

## Phase 1 — ERP (`D:\laragon\www\erp`)

### Task 1 — API search trả thêm Nguồn hàng / Lĩnh vực / Chương + filter công ty

**File:** `app/Http/Controllers/Common/SearchController.php` — hàm `searchProductStockBuyerApi()` (~dòng 1263)

- [x] ~~Thêm `'products.company_id'` vào `$select`~~ — KHÔNG cần: `$select` đã có `products.*`
      nên `company_id` và `group_id` sẵn có trong kết quả
- [x] Thêm filter ngay cạnh khối filter `brand_id`:
  ```php
  if (!empty($request->source_company_id)) {
      $products = $products->where('products.company_id', $request->source_company_id);
  }
  ```
- [x] KHÔNG đụng nhánh `if (!empty($request->price_type ?? ''))` — đó là chỗ join
      `product_company_coefficients` theo `company_id`, giá phải giữ nguyên
- [x] KHÔNG join `product_group_classifies` vào query chính (nhóm có nhiều dòng phân loại sẽ nhân bản
      dòng hàng hoá, làm sai `recordsFiltered`)
- [x] Kiểm chứng: `php artisan tinker` gọi trực tiếp hàm, xác nhận `recordsFiltered` không đổi khi
      chưa truyền `source_company_id`, và giảm đúng khi truyền `source_company_id=4`

### Task 2 — Map field mới + danh sách công ty cho dropdown

**File:** `app/Http/Controllers/Api/HrmProductSearchController.php`

- [x] Trong `search()`, sau khi có `$rows`: gom `group_id` của trang kết quả, chạy **một** query
      `product_group_classifies` join `scopes` + `chapters`, gộp theo `group_id` thành
      `['scope_names' => [...], 'chapter_names' => [...]]`, loại trùng
- [x] `mapProduct()` trả thêm: `company_id`, `company_code`, `company_name`, `scope_names`, `chapter_names`
      (mảng rỗng khi nhóm chưa phân loại — 496 hàng hoá thuộc diện này)
- [x] `catalogs()` thêm khoá `companies`: các công ty có ít nhất một hàng hoá
      → **đã đổi**: trả TOÀN BỘ công ty (xem mục Bổ sung bên dưới), `{id, code, name}`, giữ cache 10'
- [x] Kiểm chứng:
      `curl "http://erp.test:8080/api/v1/hrm/products/search?company_id=1&employee_id=39&price_type=1&start=0&length=3"`
      → mỗi phần tử có đủ 5 khoá mới; `.../catalogs` có khoá `companies`

### Task 3 — Popup chọn hàng hoá bên ERP

**File:**
- `resources/views/partials/modals/searchProductQuotation.blade.php` — khối filter
- `resources/views/partials/modals/js/searchProductQuotationJs.blade.php` — mảng `columns` (~dòng 138) và hàm `data:`

- [x] Thêm ô select "Công ty" vào khối filter của popup, nguồn từ danh sách công ty có hàng hoá
- [x] Đẩy giá trị ô đó vào `data:` của DataTables dưới tên `source_company_id`
- [x] Thêm 3 cột vào mảng `columns`: `company_code` (Nguồn hàng), `scope_names` (Lĩnh vực),
      `chapter_names` (Chương) — hai cột sau render mỗi giá trị một dòng
- [x] Cập nhật `searchProductStockBuyer()` (bản không-Api, dùng cho popup ERP) y hệt Task 1
- [x] Kiểm chứng: user mở popup Báo giá trên ERP, xác nhận 3 cột và ô lọc hoạt động

---

## Phase 2 — hrm-api

### Task 4 — Hai hàm giá dùng chung nhận thêm `$companyId`

**File:**
- Tạo: `Modules/Human/Entities/TpProductCompanyCoefficient.php`
- Sửa: `Modules/Human/Entities/TpProductUnitPrice.php`

- [x] Entity mới `TpProductCompanyCoefficient`: connection `mysql2`, bảng `product_company_coefficients`,
      hàm tĩnh `getCoefficients(array $productIds, int $companyId): array` trả `[product_id => coefficient]`.
      Đây là **nơi duy nhất** đọc bảng hệ số; hai hàm dưới và Task 7 đều dùng lại nó.
- [x] `getUnitOptions(array $erpProductIds, int $priceTypeId = 1, ?int $companyId = null): array`
      — khi có `$companyId`, join `product_company_coefficients` theo `(product_id, company_id)` và
      nhân vào `retail_price` theo công thức ở Ràng buộc chung. `cost_price` **giữ nguyên**
      (hệ số chỉ áp cho giá bán).
- [x] `getRetailPrices(array $erpProductIds, int $priceTypeId = 1, ?int $companyId = null): array` — tương tự
- [x] Kiểm chứng bằng tinker trên mã `ENEO.700-V5029`:
      `getUnitOptions([id], 1)` giữ nguyên 1.265.000; `getUnitOptions([id], 1, 2)` ra 1.316.000

### Task 5 — Truyền `$companyId` vào các chỗ gọi (12/14; 2 chỗ xác minh là không cần)

Bảng dưới là quyết định cho **toàn bộ** chỗ gọi hiện có. Chỗ nào ghi "giữ nguyên" thì không sửa.

| # | Vị trí | Hàm | Nguồn `companyId` |
|---|---|---|---|
| 1 | `QuotationService::enforceErpProductPrice()` (~3382) | getUnitOptions | `$quotation->company_id` |
| 2 | `QuotationService` ~959 (copy sang báo giá mới) | getUnitOptions | `$new->company_id` |
| 3 | `QuotationService` ~1239 | getUnitOptions | `$quotation->company_id` |
| 4 | `QuotationService::createFromBom()` (~1688) | getUnitOptions | `$quotation->company_id` |
| 5 | `QuotationService::copyBomIntoQuotation()` (~2290) | getUnitOptions | `$quotation->company_id` |
| 6 | `QuotationService::repriceErpItems()` (~2881) | getUnitOptions | thêm tham số `?int $companyId` vào chữ ký hàm, controller truyền `company_id` của báo giá đang mở |
| 7 | `QuotationService` ~2806 (combo ERP) | getRetailPrices | `$quotation->company_id` |
| 8 | `QuotationImportService` ~951 | getUnitOptions | `$quotation->company_id` |
| 9 | ~~`BomListService::syncErpFields()` (~2486)~~ | getUnitOptions | **KHÔNG sửa** — chỉ dùng `unit_id` để lọc ĐVT hợp lệ, không đọc giá |
| 10 | ~~`DetailBomListResource` ~38~~ | getUnitOptions | **KHÔNG sửa** — chỉ lấy `unit_id`/`unit_name`/`is_base`, không kèm giá |
| 11 | `QuotationController::erpProductUnits()` (~892) | getUnitOptions | FE gửi thêm `quotation_id`; lấy `company_id` của báo giá đó, chưa có thì dùng công ty người đăng nhập |
| 12 | `BomListController::searchErpProducts()` (~391) | getRetailPrices | công ty người đăng nhập (popup lúc tạo/sửa BOM) |
| 13 | `BomListController::getErpRecipeChildren()` (~456) | getRetailPrices | công ty người đăng nhập |
| 14 | `BomListController::getErpProductPrices()` (~530) | getRetailPrices | FE gửi `bom_list_id` nếu có, không thì công ty người đăng nhập |

- [x] Sửa 12 chỗ theo bảng (chỗ 9 và 10 xác minh là không đọc giá nên giữ nguyên)
- [x] `getCostPrices()` **giữ nguyên** ở mọi chỗ — giá vốn không nhân hệ số
- [x] Kiểm chứng (tinker, mã `ENEO.640-S4136`, hệ số công ty 2 = 1.1, giá gốc 404.000):
      popup Báo giá = **444.000**, BE chốt khi lưu = **444.000**, popup BOM = **444.000** → cả ba khớp.
      Còn lại user kiểm trên trình duyệt (TC05)

### Task 6 — Helper công ty + service search báo giá

**File:**
- Tạo: `app/Helpers/CompanyHelper.php` (hoặc thêm vào file helper sẵn có của dự án)
- Sửa: `Modules/Assign/Services/ErpProductSearchService.php`

- [x] Helper MỚI `currentEmployeeCompanyId($employee = null): ?int` — bê nguyên logic
      `ErpProductSearchService::resolveCompanyId()` (ưu tiên `company_id` → `current_company_role`
      → `employee_info.company_id`). Không sửa hàm dùng chung nào khác.
- [x] `ErpProductSearchService::resolveCompanyId()` gọi lại helper này
- [x] `ALLOWED_FILTERS` thêm `'source_company_id'`
- [x] `mapProduct()` map thêm `company_id`, `company_code`, `company_name`, `scope_names`, `chapter_names`
- [x] `search()` nhận thêm tham số công ty tính giá: khi sửa báo giá đã có thì truyền
      `quotations.company_id`, tạo mới thì công ty người đăng nhập
- [x] Kiểm chứng: gọi `/assign/quotations/erp-product-search?start=0&length=5` qua tinker,
      xác nhận 5 khoá mới có mặt

### Task 7 — Popup Bomlist (query thẳng DB)

**File:** `Modules/Assign/Http/Controllers/Api/V1/BomListController.php` — `searchErpProducts()`
(dùng lại `TpProductCompanyCoefficient` đã tạo ở Task 4, không tạo thêm entity)

- [x] `searchErpProducts()`: eager thêm quan hệ nhóm hàng; trả thêm `company_id`, `company_code`,
      `scope_names`, `chapter_names` (lấy qua `product_group_classifies` theo `group_id`, gộp nhiều giá trị)
- [x] Nhận filter `source_company_id`
- [x] `list_price` đi qua `getRetailPrices($ids, 1, $companyId)` của Task 4
- [x] Kiểm chứng: gọi `/assign/bom-lists/erp-products?length=5` qua tinker, so `list_price` của một mã
      có hệ số với số popup báo giá trả về — phải trùng

---

## Phase 3 — hrm-client

### Task 8 — Popup chọn hàng hoá của Báo giá

**File:** `pages/assign/quotations/components/QuotationProductSearchModal.vue`

- [x] Thêm ô lọc "Công ty" bằng `V2BaseSelectInModal`, nguồn từ `companies` của API catalogs,
      gửi lên `source_company_id`, đặt cạnh các ô lọc sẵn có
- [x] Thêm cột **Nguồn hàng** (sau cột "Mã hàng"): hiện `company_code`, `title` là `company_name`
- [x] Thêm cột **Lĩnh vực** và **Chương** cạnh cột "Loại hàng hóa": render mỗi giá trị một `<div>`,
      rỗng thì để trống (không hiện nhãn)
- [x] Reset ô lọc công ty khi bấm "Xoá lọc" cùng các ô khác
- [x] Kiểm chứng: `npx vue-template-compiler` / build FE không lỗi; user mở popup xác nhận mắt thường

### Task 9 — Popup chọn hàng hoá của Bomlist

**File:** `pages/assign/bom-list/components/BomBuilderAddProductModal.vue`

- [x] Làm y hệt Task 8 nhưng theo style list của module BOM (đọc lại file để bám đúng khuôn hiện có)
- [x] Kiểm chứng: build FE không lỗi; user mở popup xác nhận

---

## Phase 4 — Kiểm thử (user chạy trên trình duyệt)

- [ ] TC01 — Popup báo giá: đủ 3 cột mới, hàng không phân loại thì Lĩnh vực/Chương trống
- [ ] TC02 — Lọc Công ty ở popup báo giá: danh sách thu hẹp đúng, **giá không đổi**
- [ ] TC03 — Popup Bomlist: 3 cột + lọc công ty hoạt động như popup báo giá
- [ ] TC04 — Giá khớp nhau: cùng một mã hàng, popup báo giá và popup BOM ra cùng số
- [ ] TC05 — Lưu báo giá: đơn giá sau khi lưu **bằng đúng** số hiển thị lúc chọn (mã có hệ số ≠ 1)
- [ ] TC06 — Đổi ĐVT trong màn sửa: giá vẫn theo hệ số công ty của báo giá
- [ ] TC07 — Người công ty khác mở báo giá cũ, sửa rồi lưu → đơn giá **không** đổi (theo Q6)
- [ ] TC08 — Báo giá lập từ BOM: giá chuyển sang đúng hệ số
- [ ] TC09 — Import báo giá từ Excel: giá theo hệ số công ty của báo giá
- [ ] TC10 — Giá vốn không bị nhân hệ số; tài khoản không có quyền "Xem giá vốn hàng hoá" vẫn không thấy
- [ ] TC11 — Popup ERP: 3 cột + lọc công ty
- [ ] TC12 — Regression: bản in và file Excel báo giá/BOM không xuất hiện 3 thông tin mới

---

## Ghi chú môi trường

ERP và HRM phải cùng trỏ một DB ERP (hiện cùng `erp_new_11032026`). Dữ liệu báo giá cũ trong
`hrm_production_18072026` nhập từ thời `gop_db`: 867/1.074 dòng trỏ sang mặt hàng khác, 207 dòng mất id.
**Khi kiểm thử phải tạo báo giá mới**, không mở-rồi-lưu báo giá cũ trên DB này.

---

### Bổ sung sau rà soát lại task (2026-09-11)

- [x] Popup ERP: hai cột Lĩnh vực/Chương bị bóp quá hẹp. Nguyên nhân: dùng class `th-wrap` bê từ
      hrm-client sang nhưng **bên ERP không có class đó** (`th-wrap` chỉ được định nghĩa trong
      `<style scoped>` của QuotationProductSearchModal.vue). Đã đổi sang class `col-classify` và
      định nghĩa thật trong `<style>` của `searchProductQuotation.blade.php`:
      `min-width: 200px`, cho xuống dòng, `vertical-align: top`.
      Bài học: copy markup giữa 2 project phải kiểm class có tồn tại ở đích không.

- [x] Thứ tự cột: **Lĩnh vực + Chương đứng ngay trước cột Model** ở cả 3 popup (yêu cầu user).
      Popup Bomlist vốn đã đúng; popup Báo giá HRM và popup ERP chuyển 2 cột từ trước "Tên hàng hoá"
      xuống sau nó. Đổi luôn khắc phục một rủi ro: trước đó 2 cột mới chen giữa `sticky-col-c`
      (Loại hàng hoá) và `sticky-col-d` (Tên hàng hoá) — hai cột dính trái phải liền nhau.
- [x] Sửa `colspan` của dòng "không có dữ liệu" cho khớp số cột thật: popup Báo giá 20, Bomlist 14.
      Lưu ý: bản gốc vốn đã lệch sẵn (17 cột nhưng `colspan="16"`), không phải do thay đổi này.

- [x] Dropdown lọc Công ty: đổi từ "chỉ công ty có hàng hoá" sang **hiển thị TOÀN BỘ công ty**
      (yêu cầu trực tiếp của user). `ProductSourceInfoService::sourceCompanies()` bỏ lọc theo
      `products.company_id` và bỏ luôn lọc `companies.status`. Kết quả: 7 công ty
      (TPE, TPHP, TPV, TPSG, TPA, UPS, ETEK GREEN) thay vì 2. Áp dụng chung cho cả 3 popup.

- [x] Popup **Bomlist** thiếu cột **"Loại hàng hóa"** — task ghi rõ "Các cột Loại hàng hóa, Lĩnh vực,
      Chương", popup Báo giá có sẵn cột này nhưng popup BOM thì không. Đã bổ sung:
      `BomListController::searchErpProducts()` trả thêm `product_cate` (mảng mã, decode từ JSON),
      FE đổi mã sang tên qua danh mục `product_cates` của ERP (không khai lại hằng số ở HRM),
      colspan 12 → 13. Kiểm chứng: API trả `["hang_ban_not_ton_kho"]`, template + script parse OK.

## Checkpoint — 2026-09-11

Vừa hoàn thành: Phase 1 (ERP) + Phase 2 (hrm-api) + Phase 3 (hrm-client) — toàn bộ 9 task code.
Đang làm dở: (không)
Bước tiếp theo: user chạy 12 test case Phase 4 trên trình duyệt (ERP + HRM). Chưa commit ở cả 3 repo.
Blocked: (không)

### Kiểm chứng đã chạy được trong phiên

| Phép thử | Kết quả |
|---|---|
| ERP search, lọc `source_company_id` | không lọc 23.913 / cty 4 → 495 / cty 1 → 23.418 (tổng khớp) |
| ERP search trả 5 khoá mới | `company_id/company_code/company_name/scope_names/chapter_names` có đủ |
| ERP `catalogs` | thêm khoá `companies` (TPE, TPSG) |
| Blade popup ERP | cả 2 file compile OK |
| `getUnitOptions` không truyền companyId | 1.265.000 — y như trước khi sửa |
| `getUnitOptions` có companyId | 1.316.000 — đúng hệ số 1.04; giá vốn giữ nguyên 951.456 |
| **Ba đường giá khớp nhau** (`ENEO.640-S4136`, hệ số cty 2 = 1.1, gốc 404.000) | popup Báo giá **444.000** = BE chốt lúc lưu **444.000** = popup BOM **444.000** |
| API popup BOM | 3 cột mới có dữ liệu; lọc cty 4 chỉ còn hàng TPSG |
| API popup Báo giá qua HRM | lọc công ty đúng, nguồn hàng đúng |
| 2 file `.vue` | template + script parse OK |
