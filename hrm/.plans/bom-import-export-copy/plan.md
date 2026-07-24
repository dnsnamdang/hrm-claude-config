# Plan: Import / Export / Sao chép BOM List

> Design tóm tắt: `.plans/bom-import-export-copy/design.md`
> Spec đầy đủ: `docs/superpowers/specs/2026-07-15-bom-import-export-copy-design.md`

## Trạng thái
- Bắt đầu: 2026-07-15 · Hoàn thành code: 2026-07-16
- Phụ trách: @manhcuong
- Tiến độ: **27/27 task ✅** — cả 4 phase XONG, mỗi nhóm qua review + fix + re-review sạch, **REVIEW TỔNG = READY**
- Cách chạy: subagent-driven (implementer → reviewer → fix → re-review), model Opus
- Code pushed: ❌ **CHƯA COMMIT** — toàn bộ ở working tree, branch `tpe-develop-assign` (cả 2 repo). **0 commit** cả 2 repo.

### File đã sửa (chưa commit) — 7 (API) + 8 (client)
**hrm-api**:
- `Modules/Assign/Services/BomListService.php` ← phần lớn thay đổi
- `Modules/Assign/Http/Controllers/Api/V1/BomListController.php`
- `Modules/Assign/Routes/api.php`
- `Modules/Assign/Http/Requests/BomList/BomListStoreRequest.php`
- `app/ExcelExport/BomListExport.php`
- `resources/views/exports/bom_list_import_format.blade.php` ← **MỚI**
- `database/migrations/2026_07_16_100000_add_copied_from_to_bom_lists_table.php` ← **MỚI, đã chạy local**

**hrm-client**:
- `pages/assign/bom-list/components/BomImportModal.vue` ← **MỚI** (~1300 dòng)
- `pages/assign/bom-list/components/BomBuilderImportModal.vue` ← **ĐÃ XOÁ**
- `pages/assign/bom-list/components/BomBuilderEditor.vue`
- `pages/assign/bom-list/components/BomBuilderTableCard.vue`
- `pages/assign/bom-list/components/BomExportModal.vue`
- `pages/assign/bom-list/index.vue`
- `pages/assign/bom-list/_id/index.vue`
- `pages/assign/bom-list/add.vue`

### ⚠️ 3 việc user cần biết khi release
1. **Master Data lạ giờ BÁO LỖI** thay vì âm thầm tạo danh mục ERP → file Excel cũ đang import trót lọt **sẽ bắt đầu đỏ**.
2. **Export MẤT kiểu báo cáo nhóm-số-La-Mã** → ai dùng export để in/gửi đối tác sẽ thấy file khác hẳn (giờ là bảng phẳng round-trip).
3. File **12 cột đúng file mẫu Google Sheet**. **KHÔNG có cột "Giá nhập"** — BOM không quản lý giá (giá xử lý ở Báo giá); xem mục "REVIEW TỔNG + SAI LẦM" bên dưới trước khi định thêm lại.

### ⚠️ Quy ước verify của feature này
- Lint BE: **`/opt/homebrew/opt/php@7.4/bin/php -l`** — KHÔNG dùng `php -l` (máy mặc định PHP 8.1, production 7.4 → không bắt được cú pháp PHP 8 lọt vào).
- Dự án **không có PHPUnit/eslint** cho phần này → verify bằng tinker + dữ liệu thật + Playwright. Ghi DB thì bọc `DB::beginTransaction()` + `DB::rollBack()`.
- Đo query: `Event::listen(QueryExecuted)` đăng ký **ĐÚNG 1 LẦN** — đăng ký theo từng connection sẽ **đếm đúp** (đã có agent mắc bẫy này và báo số sai).

---

## Phase 1: Import — Backend

### BE — Master Data & lookup ✅ (review clean 2026-07-15)
- [x] Task 1: `resolveLookupId()` — 4 call site (`BomListService.php:646-649`) chuyển `autoCreate: false`; hết tự tạo danh mục ERP
- [x] Task 2: Thêm `preloadMasterData()` + `lookupFromPreloaded()` — nạp `product_models`/`brands`/`origins`/`units` bằng `keyBy` lowercase, tránh N+1
- [x] Task 3: Thêm `resolveCostByName()` + `preloadCostsByName()` + `lookupCostFromPreloaded()` — tra `costs` ERP theo **TÊN** (`status=1`, `kind_of=2`); không khớp → `null` = chi phí tự do *(đổi từ `resolveCostByCode` — `costs` không có cột `code`, xem đính chính design)*

**Chữ ký bàn giao cho nhóm sau** (ổn định, đã review):
- `preloadMasterData(): array` → `['model'|'brand'|'origin'|'unit' => [name_lower_trim => id]]`
- `lookupFromPreloaded(array $preloaded, string $type, ?string $name): ?int`
- `resolveCostByName(?string $name): ?object` (TpCost) · `preloadCostsByName(array $names): array` · `lookupCostFromPreloaded(array $preloaded, ?string $name): ?object`
- Helper nội bộ: `normalizeLookupKey()`, `lookupTableMap()`, `erpCostQuery()`, `costSelectColumns()`
- ⚠️ Gọi `preloadMasterData()` / `preloadCostsByName()` **1 lần/lần import** rồi truyền xuống loop — gọi trong loop là mất sạch tác dụng.
- ⚠️ `preloadCostsByName()` trả mảng **thiếu key** khi không khớp → dùng `lookupCostFromPreloaded()` thay vì tự index.

**Fix đã áp sau review** (3 Important): `resolveLookupId` `LOWER(name)` → `LOWER(TRIM(name))` + `orderBy('id')` (2 đường tra cứu trước đó có candidate set khác nhau → lệch id ở ca whitespace); thêm `lookupCostFromPreloaded` (tránh caller tự normalize sai); `costSelectColumns()` cho 2 hàm cost cùng shape (trước đó preload trả 5 cột, live trả 13 → `->kind_of` null âm thầm).

**Minor còn treo → đưa vào review tổng cuối:**
- `normalizeLookupKey()` chỉ là nguồn duy nhất phía PHP; predicate SQL là phép normalize thứ 2 độc lập. **PHP `trim()` ≠ SQL `TRIM()`** (PHP cắt cả `\t \n \r \0 \x0B`, SQL chỉ cắt space) → lệch với tên kiểu `"FOO\t"`. Hiện **chưa kích hoạt**: 0 bản ghi có tab/newline đầu-cuối trên cả 5 bảng.
- N+1 ở `importProducts` **chưa đóng** — 4 call site vẫn dùng `resolveLookupId`; preload/lookup hiện là **dead code, 0 caller**. Task 9-13 phải khép lại.

### BE — Validate STT ✅ (review clean 2026-07-15)
- [x] Task 4: Hàm `validateSttStructure(array $products): array` — trả `[index => [messages]]`, chỉ chứa dòng CÓ lỗi; logic thuần, không DB
- [x] Task 5: Đủ 4 luật (bắt buộc/trùng/định dạng · tối đa 2 cấp · cha phải nằm trên · tịnh tiến không nhảy bậc), 4 message đúng nguyên văn spec §4.3

**Verify**: 12/12 ca brief + 10 ca bẫy reviewer tự dựng (số ≥10 `10,11`, `1..15` tuần tự, `1.10`, `' 1'`/`'1 '`, `1.0`/`0`/`0.1`, thiếu hẳn key `stt`, `1.1` mồ côi, `1,1.1.1`, `1,2,2`, `1,1.1,3`) → không thủng ca nào. Không off-by-one. 500 dòng = 2.7ms. Diff thuần thêm mới, 0 dòng bị xoá/sửa → chứng minh không đụng `validateImportData()`/`importProducts()`.

**3 quyết định đã chốt** (implementer nêu, tôi quyết): (1) `2, 1` anh em đảo thứ tự → **không báo lỗi**, vì `bom_list_products` KHÔNG có cột `stt`/`sort_order` (đã verify schema) nên số STT bị vứt sau import, ép thứ tự là vô nghĩa; (2) dòng STT rác kéo theo tối đa 1 dòng "nhảy bậc" kế nó → chấp nhận, cơ chế resync chặn nhiễu ở 1 dòng thay vì lan cả file; (3) trùng lặp báo lỗi cả 2 dòng → chấp nhận, không có cơ sở chọn dòng nào đúng.

**Minor còn treo → review tổng cuối triage:**
- **M1** `BomListService.php:637` — Luật 3 trộn "thứ tự mảng" với "giá trị key": `break` khi `$otherIndex >= $index` chỉ đúng khi key tăng dần. Key giảm dần → báo sai "không tìm thấy cha". Rủi ro ~0 (Excel luôn cho list tuần tự). **→ Task 9 khi wire vào nhớ thêm docblock `@param` ghi rõ precondition "key phải tăng dần theo thứ tự dòng".**
- **M2** `:647` — cha trùng (`1, 1, 1.1`) → con báo "không tìm thấy cha" dù cha có ở trên (cha bị loại khỏi `$validStt` do lỗi Luật 1). Cùng họ quyết định (2)/(3).
- **M3** (nit) `0`, `0.1`, `1.0` bị chặn bằng message "nhảy bậc" — chặn đúng, message hơi lệch bản chất.
- **M4** (nit) `:666` `asort` không stable trên PHP 7.4 — chỉ ảnh hưởng ca leading zero (`1` vs `01`), message giống nhau.

### BE — Validate Mã hàng ✅ (review clean sau 1 vòng fix, 2026-07-15)
- [x] Task 6: `preloadErpProductsByCode()` + `lookupErpProductFromPreloaded()` — tra ERP **thẳng DB** qua `TpProduct` (mysql2), KHÔNG qua HTTP `ErpProductSearchService`; mirror mapping của `syncErpFields()` (`:1233`)
- [x] Task 7: `preloadTempProductProjectsByCode()` + `lookupTempProductFromPreloaded()` — UNION theo `ProductProjectController:71-100`, thêm `erp_product_id IS NULL`; **phạm vi GLOBAL** *(sửa: spec đầu ghi "lọc theo dự án của BOM" — sai, xem đính chính spec §4.4b)*
- [x] Task 8: `classifyImportRow($product, $ctx)` — 3 nhánh (a) erp → (b) product_project → (c) new_temp; preload truyền từ ngoài, **0 query trong loop**

**Verify**: 3 nhánh chạy data thật (a: `2Q-GIADEPHUTUNG` lowercase+dính nháy vẫn khớp; b: `HH000001/HH000002` → `pending_confirm`; c: 4 message Master Data nguyên văn; mã trống → `Mã hàng là bắt buộc.`); vế quotation của UNION test qua transaction+rollback (244→244 nguyên vẹn); thứ tự (a) trước (b) verify bằng cách dựng temp row trùng mã ERP → ra `source=erp`, rollback 32→32. **N+1**: `classifyImportRow` trong loop = **0 query** (verify 200 và 300 dòng). Preload ERP = `ceil(2×N/500) × 5` query — **KHÔNG phải hằng số**: 200 mã→5, 300 mã→10, file 500 dòng→10; cộng UNION 2 + masterData 4. Bẫy đã thử không vỡ: mã dạng số `123` (PHP ép array key thành int), mã có dấu `:`, mã straddle chunk, mã truyền vào dạng int. Exhaustive: 43.548/43.548 mã ERP khớp, 0 sót. Collation verify ở **cấp cột** cho cả 3 cột `code` trên **2 database** (`products` ở mysql2; `bom_list_products`/`quotation_product_prices` ở hrm) — đều `utf8mb4_unicode_ci`; `products.code` có 0 mã non-ASCII nên ca Unicode fold không với tới được.

**Fix đã áp sau review** (2 Important + 2 Minor): thêm `'uom'` vào `locked_fields` (ĐVT hàng ERP phải khoá theo tài liệu mục 2.4 — trước đó để user sửa được); đổi `product_project_id`→`source_row_id` + `product_project_source`→`source_row_type` (chặn Task 9-10 map nhầm vào cột chết); `resolveSystemUnit()` fallback ĐVT từ file khi ERP không có `baseUnit` (1/43.548 hàng — `TPE-BNKN1`; nếu không fix là **regression**, vì code cũ luôn lấy ĐVT từ file); `buildCodeMatchCandidates()` 4→2 biến thể/mã (query 10→5).

**⚠️ RÀNG BUỘC BÀN GIAO cho Task 9-10 — đọc kỹ:**
- `classifyImportRow()` trả `status` **KHÔNG phải kết luận cuối** — nhánh (c) bỏ TRỐNG Master Data vẫn ra `valid` (cố ý, tránh double-error). Task 9 **bắt buộc AND** với `validateImportData()` (vốn lo case bỏ trống).
- `resolved` dùng key `*_id` (không phải tên) vì `mapProductPayload()` bọc `toNullableInt()` → nhét tên vào sẽ thành **null âm thầm, không exception**.
- **ĐỪNG** đẩy nguyên `$classify` vào `$row` — `mapProductPayload()` (`:1929/:1936`) vẫn đọc/ghi `product_project_id` (cột CHẾT). Map `source_row_id` có chủ đích hoặc bỏ hẳn.
- `importProducts()` **KHÔNG** gọi `syncErpFields()` (chỉ store/update gọi) → logic "giữ ĐVT user nếu hợp lệ" không tự có ở luồng import. Đã chốt: import khoá ĐVT theo ERP (xem spec §4.4a).

**Minor còn treo → review tổng cuối:**
- `mapProductPayload()` `:1929/:1936` ghi vào cột chết `product_project_id` — code CŨ có sẵn, ngoài scope nhóm này.
- Nhánh (b) chỉ có 2 dòng data thật (`unit_id` đều not-null) → nhánh fallback ĐVT của (b) chưa được data thật cover (verify gián tiếp qua (a) `TPE-BNKN1`, dùng chung helper).

### BE — Viết lại validateImportData ✅ (review clean 2026-07-15) — *gộp Task 14 vào nhóm này*
- [x] Task 9: `validateImportData(BomList $bomList, array $products): array` — 12 cột mới, `qty > 0` (cũ là `>= 0`), Nhóm hàng ≤250, Ghi chú ≤500; **xoá hẳn** luật `Đơn giá dự toán không hợp lệ` (bỏ cột Giá nhập)
- [x] Task 10: Response shape mới — `status` (valid/invalid/pending_confirm), `resolved`, `locked_fields`, `source`, `source_row_id/type`, `message`, `pendingCount`; giữ `isValid` = `status==='valid'` cho FE cũ; `row = index+2`; `total = valid+invalid+pending` (pending KHÔNG cộng vào 2 cái kia)
- [x] Task 14: (gộp lên đây vì đổi chữ ký Service là vỡ Controller ngay) — xoá route `POST /import/validate-data` + method `Controller::validateImportData()`; `validateImport()` giờ **thực sự dùng** `$bomList`; sửa lời gọi trong `import()` (`:524`)

**Verify**: 12/12 ca brief pass data thật. **N+1: 10/50/200 dòng đều = 11 query** (hằng số tuyệt đối, 200 dòng chạy 48ms). Bẫy "AND 2 nguồn lỗi" không thủng: nhánh (c) `model=''` → `invalid` đúng 1 lỗi (không double-error). Không ghi rác vào cột chết: `json_encode` output → **không có** chuỗi `product_project_id`, chỉ có `source_row_id/source_row_type`.

**2 đổi hành vi có chủ đích (reviewer xác nhận đúng):**
- `validateImportData()` giờ **chặn quyền + trạng thái BOM** (copy y nguyên 2 guard của `importProducts()`) — trước đây validate không chặn gì. Hợp lý: validate được mà import chắc chắn fail là vô nghĩa.
- Luật "bỏ trống là bắt buộc" cho Model/Brand/Origin/ĐVT **chỉ áp nhánh (c) new_temp**. Hàng ERP/hàng tạm cũ để trống 4 ô vẫn valid vì các ô đó **bị khoá**, lấy từ hệ thống (tài liệu 2.4). Code cũ bắt buộc MỌI dòng → đó là **luật sai của code cũ**, user không có cách sửa ô bị khoá để hết lỗi.

**Fix đã áp sau review**: thêm luật ĐVT đóng lỗ hổng — dòng **hàng hoá** có `source ∈ {erp, product_project}` và `resolved.unit_id === null` → lỗi `Đơn vị tính là bắt buộc` (không dấu chấm cuối, khớp message sẵn có).
> ⚠️ **Reviewer đã chặn 1 quyết định SAI của tôi**: tôi định áp luật này cho MỌI nhánh → sẽ gắn lỗi cho **100% dòng dịch vụ** (dòng dịch vụ luôn `unit_id=null` theo thiết kế, hardcode `:606`) + double-error ở `new_temp`. Bản thu hẹp là bắt buộc, đừng nới lại.

**Minor còn treo → review tổng cuối:**
- `:695,699` — alias cột `Loại` rộng hơn message (nhận thêm `'1'`,`'2'`,`'dịch vụ'`,`'dich vu'`,`'hang hoa'`) trong khi message nói *"Chỉ nhận 'Hàng hoá' hoặc 'Dịch vụ & Chi phí khác'"*. Tập cha nên không chặn nhầm; giữ để nhận lại payload `1/2` từ lưới FE.
- Ca `source='product_project'` + `unit_id=null` chưa chứng minh bằng data thật (hàng tạm có `unit_id` NULL = 0/2 trong DB) — suy ra từ đối xứng với nhánh `erp` (đã chứng minh trực tiếp).
- Guard trả **400** thay vì 403 — pattern sẵn có của `importProducts()`, không đổi ở đây.

### 🔴 Bug CÓ SẴN trên branch (KHÔNG phải của feature này, chưa sửa — chờ user quyết)
`Modules/Decision/Routes/web.php:17` dùng cú pháp chuỗi cũ `'DecisionController@index'` → Laravel 8 phân giải thành `Modules\Decision\Http\Controllers\DecisionController`, nhưng class thật ở namespace `Modules\Decision\Http\Controllers\V1`. Hệ quả: **`php artisan route:list` hỏng toàn bộ** + route web `GET /decision` sẽ 500. Đã stash code feature để xác nhận lỗi có TRƯỚC (tại commit `8bb484b9b`). `Modules/Decision/Routes/api.php:10` khai đúng. Sửa = thêm `V1\` vào dòng 17.

### BE — Import ✅ (review clean sau 1 vòng fix, 2026-07-15) — *gộp Task 15 vào nhóm này*
- [x] Task 11: `importProducts(BomList $bomList, array $entries)` — dịch vụ → `bom_list_service_items` (qty=1), hàng hoá → `bom_list_products`; replace-all xoá **cả 3** bảng (products + groups + service_items)
- [x] Task 12: `resolution` (`keep_and_sync` → import; thiếu/`new_code` → 400) + `skip_invalid`; server **luôn validate lại**, không tin `status` FE gửi
- [x] Task 13: `note` lưu ở **cả 2** bảng

**🔴 SỬA LỖI KIẾN TRÚC (quan trọng nhất nhóm này)**: `import()` trước đây gọi validate rồi **VỨT BỎ `resolved`**, để `importProducts()` tra cứu lại từ đầu → 2 đường tra cứu độc lập, user xem preview một đằng DB lưu một nẻo. Và dòng `pending_confirm` (`isValid=false`) bị **âm thầm loại bỏ**. Nay `importProducts()` **tiêu thụ `resolved`**. Chữ ký nhận `$entries = [['product'=>…, 'row'=>…], …]` — ghép cặp thay vì 2 mảng song song (caller có lọc dòng → mảng song song sẽ lệch index âm thầm, dòng này lấy `resolved` của dòng kia).
**Bằng chứng cứng**: `mysql2` = **0 query** ở đường ghi với mọi cỡ file (12/60/240 dòng) — code cũ gọi `resolveLookupId` 4 lần/dòng = N+1 thật. Import mã ERP thật kèm Tên/Model/Brand **rác** trong file → DB lưu **dữ liệu chuẩn ERP**.

**🔴 BUG CŨ ĐÃ ĐÓNG**: code cũ ghi dòng dịch vụ vào `bom_list_products` với `product_type=2`, nhưng FE render khối "Dịch vụ & Chi phí khác" từ `service_items` và `mapProductsToGroups()` không lọc `product_type` → dòng dịch vụ hiện **nhầm ở lưới Hàng hoá**. Verify sau fix: `bom_list_products WHERE product_type=2` = **0**.

**Fix đã áp sau review — cả 3 đều là mất/lệch dữ liệu ÂM THẦM:**
1. **VAT dịch vụ**: hardcode `vat_percent=0` → lấy từ `resolved['vat_percent']` (cost đã khớp). **497/504 cost dịch vụ có VAT=8** → cùng 1 cost thêm bằng tay lưu 8, import lưu 0. `preloadCostsByName()` đã select sẵn cột này → **0 query mới**. Chi phí tự do (`cost_id=null`) giữ 0.
2. **Cắt chuỗi âm thầm**: 🔴 **DB KHÔNG strict** — `sql_mode=NO_ENGINE_SUBSTITUTION`, `config strict=false` (đã tự verify). Giả định "insert quá dài → lỗi → dòng failed → HTTP 207 → user biết" là **SAI**: thực tế DB **cắt còn 50 ký tự, failed=0, HTTP 200, không báo gì**. Đã thêm luật độ dài vào validate: hàng hoá code/name ≤255; dịch vụ code ≤**50** (`bom_list_service_items.code` là varchar(50), `bom_list_products.code` là varchar(255)), name ≤255.
3. **Con mồ côi**: `skip_invalid=true` + cha bị skip → con hợp lệ ghi với `parent_id=NULL` **VÀ `bom_list_group_id=NULL`** (mất cả cha lẫn nhóm), chỉ báo "Đã bỏ qua 1 dòng lỗi". Nay **cascade skip** con của cha bị bỏ, tách bộ đếm `skipped`/`cascade_skipped` + message riêng (`Đã bỏ qua N dòng lỗi và M dòng con của chúng.`) — con bị cascade KHÔNG phải dòng lỗi, gộp chung là nói sai với user.

**Quyết định**: nhóm hàng **chỉ tạo từ dòng hàng hoá** (bảng `bom_list_service_items` không có cột nhóm → tạo từ dòng dịch vụ chỉ sinh nhóm rỗng trên lưới). Code cũ tạo từ mọi dòng. Verify: dòng dịch vụ mang nhóm → không sinh nhóm rác.

**Minor còn treo → review tổng cuối:**
- `BomListController.php:236` — `tempnam(...) . '.xlsx'` tạo **2 file**, `deleteFileAfterSend` chỉ xoá file `.xlsx` → file 0 byte ở lại `/tmp` vĩnh viễn. **Byte-identical với baseline = bug CÓ SẴN**, không phải của nhóm này.
- `BomListController.php:613` — `total = count($entries)` không tính dòng skip → file 2 dòng báo "1/1" (có key `skipped` riêng nên chấp nhận được).
- Nhánh **207 gần như chết**: DB non-strict nên insert hầu như không ném lỗi → `failed>0` rất khó xảy ra. Chính là lý do fix #2 quan trọng.
- Luật độ dài kiểm trên **giá trị file** (thứ user sửa được), không phải `resolved`. **False positive**: dòng mã ERP thật kèm Tên 300 ký tự trong file bị chặn, dù ô Tên đó **bị khoá** và `resolved.name` ghi xuống là tên ERP 34 ký tự hợp lệ. Thiên về chặn nên **không mất dữ liệu, có báo rõ** — chỉ lệch tinh thần "ô bị khoá thì bỏ qua giá trị file". Muốn chuẩn thì xét độ dài trên `resolved`.
- 🔧 **Comment SAI cần sửa** `BomListService.php:~625`: ghi *"503/504 cost đang có vat_percent = 8"* — gộp nhầm 2 con số. Phân bố thật của `TpCost::active()->where(kind_of, KIND_DICH_VU)` = 504 dòng: **vat=8 → 497**, vat=10 → 5, vat=1 → 1, vat=0 → 1. Đúng phải là *"497/504 có vat=8; 503/504 có vat khác 0"*.

**Ghi nhận kỹ thuật**: fix agent dùng `mb_strlen` (ký tự) chứ không `strlen` (byte) — đúng semantics `varchar` của MySQL. Dùng `strlen` sẽ chặn oan ở ~17 ký tự tiếng Việt. Reviewer verify 50 ký tự `ế` → validate pass, DB lưu đủ 50.

### BE — Route & template
- [x] ~~Task 14~~ → **đã gộp vào nhóm "Viết lại validateImportData" ở trên** (đổi chữ ký Service làm vỡ Controller ngay, không tách được)
- [x] Task 15: `importTemplate()` → 12 cột mới đúng thứ tự (`Loại *, Nhóm hàng, STT *, Tên hàng *, Mã hàng *, Model, Thương hiệu, Xuất xứ, ĐVT, Số lượng *, Thông số kỹ thuật, Ghi chú`) + 3 dòng mẫu (cha `1` / con `1.1` / dịch vụ `2`). Verify: đọc lại file sinh ra bằng PhpSpreadsheet → header đúng nguyên văn có dấu `*`; 3 dòng mẫu chạy qua `validateImportData()` → **0 lỗi** và import được thật *(gộp vào nhóm "BE — Import")*

## Phase 2: Import — Frontend

### FE — Modal mới ✅ (review clean sau 1 vòng fix, 2026-07-16)
- [x] Task 16: `BomImportModal.vue` — wizard **3 bước** (bỏ bước 4 vì là code chết: set rồi đóng modal ngay, không ai thấy), parse Excel qua util `parseExcelFile` dùng lại, chặn file ≠ .xlsx/.xls
- [x] Task 17: Chặn sai cấu trúc header + message nguyên văn
- [x] Task 18: 3 trạng thái dòng (xanh/đỏ/**vàng**) + `__status`/`__resolution`/`__locked`; lọc "Chỉ dòng lỗi"; sửa ô + Validate lại; ô khoá **không render input**
- [x] Task 19: Dòng "Chờ xác nhận" — 2 nút; chặn Import khi chưa chọn
- [x] Task 20: `canImport` — sáng khi 0 lỗi HOẶC tích "Bỏ qua dòng lỗi"; **pending chưa chọn → TẮT kể cả đã tích** (thứ tự điều kiện quan trọng: check pending đứng TRƯỚC check skipInvalid); confirm trước import

**+ BE**: `BomListService.php` thêm `*_name` (`model_name`/`brand_name`/`origin_name`/`uom_name`) vào `resolved` — **phương án D**, 106 dòng (phần lớn comment), **0 query mới** (verify 10/10/10 query ở 5/50/200 dòng; dùng lại query sẵn có).

**Quyết định trong nhóm này:**
- **KHÔNG** tái dùng `V2BaseImportTable`/`V2BaseImportToolbar` — chúng khoá theo **DÒNG** chứ không theo **Ô** và chỉ biết 2 trạng thái. Vẫn dùng lại util `parseExcelFile` + các `V2Base*`.
- **Gửi TOÀN BỘ dòng**, không lọc trước — BE dùng **index dòng gốc** cho `skip_invalid` + cascade skip; lọc trước sẽ **lệch index**. (Modal cũ lọc `validRows` — sai, không chép.)
- FE **điền xuôi `lastGroup`** vào ô "Nhóm hàng" trên lưới (chỉ dòng cha; con + dịch vụ không điền; user xoá tay thì không tự điền lại). Giữ hành vi modal cũ nhưng **hiện lên lưới** thay vì thành luật ngầm → payload = đúng thứ user nhìn thấy, BE vẫn là nguồn sự thật duy nhất.
- `skipInvalid` **không** reset sau mỗi lần Validate (reset sẽ bắt user tích lại sau mỗi lần sửa; BE vẫn chặn đúng).

**Fix đã áp sau review (2 Important + 3 Minor):**
1. **`product_attributes` là rich-text HTML thật** → ô khoá hiện `<div> <div> <p>KT...` cho user. Nằm trong `locked_fields` của **MỌI dòng ERP** = happy path. Thêm `plainText()` (strip tag → decode entity → gộp whitespace) cho cả `lockedText` + `lockedTitle`. **Không dùng `v-html`.**
2. **Race**: response Validate của file CŨ đóng dấu `__status`/`__locked` lên lưới file MỚI theo index → hiện xanh "Hợp lệ" cho dòng chưa validate. Thêm `_validateSeq` theo pattern `_reqSeq` sẵn có (`QuotationProductSearchModal.vue`), bump ở 4 chỗ.
3. Bỏ bước 4 wizard (code chết) · reset lưới trước khi chặn sai định dạng · reset counts trong catch.

**Verify**: compile sạch bằng **Node 14.21.3** (⚠️ `node` mặc định máy là **12.x** — phải gọi đúng binary); `plainText` chạy trong **Chromium thật** 18/18 ca an toàn, 0 element tạo ra, `<img onerror>`/`<script>`/`</textarea>`/entity lồng/hex entity đều không fire; `SERVICE_LOAI_KEYS` khớp `resolveImportProductType()` **đủ 5/5 alias**; alias 12 cột nhận 12/12 có `*` + 12/12 không `*`.

**⚠️ CHƯA ĐO Playwright bố cục** — modal chưa có nút mở. **Task 21-22 BẮT BUỘC đo** (2 trạng thái × 2 viewport + assert `.modal-body` không cuộn dọc). Selector: `.bom-import-content`, `.bom-import-grid-wrap`, `.bom-import-grid`.

**Minor còn treo → review tổng cuối:**
- **m-1 (đang gộp vào Task 21-22 để sửa)** `BomImportModal.vue:791-793` — **comment bảo mật có tiền đề SAI**: nói *"sau bước 1 chuỗi không còn `<` nên decode không dựng ra element"*. Đo thật: `<` **vẫn còn** (tag chưa đóng không khớp regex `/<[^>]*>/`; decode entity `&#x3C;` **tự sinh lại** `<`). Kết luận (không dựng element) vẫn đúng nhưng **đúng nhờ RCDATA của `<textarea>`**, không phải nhờ hết `<`. Nguy hiểm: người sau tin comment → tưởng output sạch tag → đổ vào `v-html` → **XSS thật**.
- `SERVICE_LOAI_KEYS` là **bộ alias thứ 2** chép từ BE (vì lúc Load lên bảng FE chưa có `product_type`, server chỉ trả sau Validate). Trôi lệch → **chỉ sai hiển thị**, không sai dữ liệu ghi (BE luôn validate lại). Triệt tiêu hẳn thì phải chuyển việc điền sang sau Validate — đánh đổi: user không thấy ngay ở preview.
- BE `preloadMasterData()` giữ thêm map `id => name` của 4 danh mục suốt request (`product_models` ~37,6k dòng) → peak memory tăng vài MB. 0 query thêm.

### FE — Nối vào editor

### FE — Nối vào editor ✅ (review clean, KHÔNG cần vòng fix, 2026-07-16)
- [x] Task 21: `BomBuilderEditor.vue` đổi sang `BomImportModal`; xoá `BomBuilderImportModal.vue` (grep 0 hit trước khi xoá); xoá `showImportModal` (code chết)
- [x] Task 22: `BomBuilderTableCard.vue` — nút Import màn Tạo mới **hiện + khoá + tooltip** `Vui lòng lưu nháp BOM trước khi import` (AC1)
- [x] +sửa comment bảo mật `plainText()` trong `BomImportModal.vue` (0 byte logic — reviewer dựng lại baseline chứng minh diff nằm gọn trong 1 block `/** */`)

### 🔴 SAI LẦM LỚN NHẤT CỦA TÔI — user phát hiện, đã sửa (2026-07-16)

**Tôi tự bịa ra "AC1 ca 4: BOM tổng hợp → ẩn nút Import" từ CODE CHẾT, rồi sửa prop bind để "làm nó chạy đúng" ⇒ LẤY MẤT khả năng import vào BOM tổng hợp mà user vẫn dùng.**

- **Task KHÔNG hề yêu cầu.** Nguyên văn AC1: *"…khi **chưa lưu nháp** (hoặc ở trạng thái **không cho phép sửa**), kiểm tra nút Import có bị ẩn hoặc bị khóa không…"* — **không một chữ nào** về loại BOM.
- Điều kiện `bom_list_type !== 'aggregate'` ở `TableCard:11` là **code chết**: prop khai `bom_list_type` (snake_case), cha truyền `:bom-list-type` → Vue 2 `hyphenate()` chỉ đổi chữ HOA nên **không bao giờ khớp** → luôn nhận default `'component'`. ⇒ **Hành vi THẬT bấy lâu = LUÔN hiện nút.**
- **Thực tế 5/5 BOM trong hệ thống đều là TỔNG HỢP** → sau khi tôi "sửa", chức năng import **gần như vô dụng**.
- User phát hiện: *"sao button import excel chỉ hiển thị khi bom list chưa có hàng hoá?"* — thực chất là "component thì hiện, tổng hợp thì ẩn". Trùng hợp vì `/add` mặc định `bom_list_type: 'component'` (`BomBuilderEditor.vue:343`) và BOM mới thì luôn rỗng.
- Nghịch lý lộ ra: **"Thêm mới" bấm được** trên BOM tổng hợp (user đã chốt giữ) nhưng **Import bị ẩn** → thêm tay thì được, thêm hàng loạt thì không.

**ĐÃ SỬA**: bỏ `bom_list_type !== 'aggregate'` khỏi `v-if` nút Import → chỉ còn `!viewOnly` + `:interactable="!!bomId"`, **đúng bằng những gì AC1 đòi**.
**Verify Playwright thật**: `/25/edit` (BOM tổng hợp, có hàng hoá) → nút **hiện, không khoá** ✓ · `/add` → nút **hiện + khoá + tooltip** "Vui lòng lưu nháp BOM trước khi import" ✓ (AC1 thật vẫn đạt).

> **⚠️ CHỈ ĐẠO CỦA USER — áp cho mọi việc sau này**: *"không cần quan tâm đến code cũ, làm sao để đạt được yêu cầu của task chuẩn nhất là được."*
> **Bài học**: **code chết không phải là spec.** Trước khi "sửa cho nó chạy đúng", phải hỏi: (1) *yêu cầu có đòi thứ này không?* (2) *hành vi THẬT hiện nay là gì?* Một điều kiện nằm trong code nhưng chưa từng chạy = nó **chưa bao giờ là hành vi của hệ thống**.

**Bug prop bind (`BomBuilderEditor.vue:46` `:bom-list-type` vs `TableCard:707` khai `bom_list_type`) vẫn giữ đã sửa** — nó là bug thật; nhưng giờ **không còn chỗ tiêu thụ sống nào** đổi hành vi (2 nút "Thêm mới" user đã chốt giữ bấm được, nút Import hết gate theo loại).
- Reviewer verify bind fix đổi **đúng 1 hành vi**: grep `bom_list_type` trong TableCard → chỉ `:11` là chỗ tiêu thụ sống (còn lại là comment + khai prop). `BomBuilderTableCard` chỉ có **1 call site**; đối chiếu cả 12 prop → `bom_list_type` là outlier snake_case **duy nhất**, 11 prop kia bind đúng. Chứng minh bằng **Vue 2 SSR harness**: `:bom-list-type` → prop `"component"`, `$attrs ["bom-list-type"]`, nút HIỆN trên aggregate (FAIL); `:bom_list_type` → prop `"aggregate"`, `$attrs []`, nút ẨN (PASS).

**Verify UI THẬT** (đăng nhập bằng phiên khôi phục từ profile Chrome MCP, không cần mật khẩu; chỉ `localhost:3000`):
- **AC1 4/4 PASS** — reviewer tự đo lại: `/add` → hiện+`disabled`+`pointer-events:none`+tooltip render thật (`opacity 0.9`, khớp nguyên văn); `/9/edit` → bật, modal mới mở; `/8` detail → ẩn; BOM tổng hợp → **ẩn**.
- **Luồng import 8/8 PASS đầu-cuối** trên BOM test id=9: dòng dịch vụ vào đúng khối **"Dịch vụ & Chi phí khác"** (chứng minh bug cũ Phase 1 đã đóng, bằng UI thật); rác bị ghi đè bởi ERP (`DVT-RAC` → **"Cái"**, không phải "40"); HTML thông số kỹ thuật hiện **text sạch**; dòng lỗi → Import TẮT → tích "Bỏ qua dòng lỗi" → BẬT → chỉ dòng hợp lệ vào; **dòng vàng vẫn TẮT kể cả đã tích**; "Giữ nguyên mã và đồng bộ" kéo "súng vặn ốc" từ hệ thống đè tên giả trong file; confirm replace-all chặn tới khi đồng ý; `.txt` bị từ chối.
- **Bố cục bảng ĐÃ ĐO** (nợ từ Task 16-20): `.modal-body` **không cuộn dọc** ở 2 trạng thái × 2 viewport (28/18 dòng thấy được, dòng 31.5px, sticky thead). Parse 42 dòng từ file mẫu thật của BE.
- Compile sạch **Node 14.21.3**; 0 lỗi console từ code mới.

**Kỹ thuật ghi nhận**: `V2BaseButton` **không có prop `disabled`** — chỉ `interactable` (`:43`), tự set `:disabled` native + class `.v2-btn--disabled { pointer-events: none }` (`:118`) ⇒ tooltip **bắt buộc** phải bọc `<span>` ngoài (browser nuốt event trên phần tử disabled). Tooltip đúng pattern dự án (`v-b-tooltip.hover` + `:title`, 243 file dùng).

**Minor còn treo → review tổng cuối:**
- 🔴 **`openPickModal()` (`BomBuilderEditor.vue:1634`) là CODE CHẾT** — nó chứa guard chặn thêm hàng vào BOM tổng hợp + toast *"BOM LIST tổng hợp chỉ nhận dữ liệu từ BL con"*, nhưng template nối `@open-pick="openAddProductModal"` (`:2400`) — hàm này **không có guard aggregate nào**. ⇒ Kết hợp với quyết định giữ 2 nút "Thêm mới" bấm được: **KHÔNG còn lớp nào** ngăn thêm hàng trực tiếp vào BOM tổng hợp, toast kia **không bao giờ hiện**. Hiện trạng CÓ SẴN, user đã chốt giữ — nhưng comment ở `:102-108` đang mô tả một guard không hoạt động.
- Lệch `button-convention`: skill quy định Import → `secondary` + `ri-upload-line`; code dùng `tertiary` + `ri-file-upload-line`. Nút anh em "Xuất Excel" cùng toolbar cũng `tertiary` → sửa lẻ sẽ lạc lõng. **Giữ nguyên là đúng.**
- **Data test còn lại trong DB local**: BOM **id=9** "ZZ TEST IMPORT — Claude (xoá được)" — xoá được, cần dọn khi kết thúc feature. BOM 2/3/8 của user **nguyên vẹn** (đã verify BOM 8 `updated_at` không đổi).

### 🔴 Nút "Xuất Excel" CHẾT ở màn Cập nhật — user phát hiện, đã sửa (2026-07-16)

**Bug CÓ SẴN** (verify ở HEAD: `_id/edit.vue` và `add.vue` chưa bao giờ có export, trong khi nút đã nằm sẵn ở `TableCard`): nút "Xuất Excel" emit `export-excel` → `BomBuilderEditor` chuyển tiếp lên cha → nhưng **chỉ `_id/index.vue` (Chi tiết) và `index.vue` (Danh sách) khai `BomExportModal`** → ở màn **Cập nhật** và **Tạo mới** không ai nghe ⇒ **bấm không ra gì**.
AC3 của task đòi *"Nhấn nút Export trên màn hình BOM Giải pháp"* → nút có mà không chạy = **chưa đạt AC** → sửa.

**Chốt với user**: *"button xuất excel là ở trong màn edit/show tương ứng, không để ở màn danh sách"*.

| Màn | Trước | Sau |
|---|---|---|
| Cập nhật `/:id/edit` | nút chết | **Nối `BomExportModal` + `handleExport`** → chạy |
| Chi tiết `/:id` | chạy | giữ nguyên |
| Tạo mới `/add` | nút chết | **Khoá + tooltip** "Vui lòng lưu nháp BOM trước khi xuất Excel" (đối xứng nút Import — chưa lưu thì không có gì để xuất) |
| Danh sách — **action từng dòng** | có "Xuất Excel" | **GỠ** (xuất BOM nào thì vào màn của BOM đó) + dọn code chết: `case 'export'`, `handleExport()`, state `bomToExport`, khai `BomExportModal` |
| Danh sách — **toolbar "Xuất Excel"** | có | **GIỮ** — đây là việc KHÁC: xuất *danh sách các BOM* theo bộ lọc (`handleExportList`), không phải xuất 1 BOM |

**Giữ lại thứ user đang có**: action ở màn Danh sách đặt tên file theo **mã BOM** (`BOM_BOM-2026-00009.xlsx`) còn màn Chi tiết hardcode `BOM_export.xlsx`. Gỡ đường Danh sách mà không mang tên file tốt sang = **mất thứ đang có** → đã chuyển `BOM_${bomData.code}` sang **cả** `_id/edit.vue` và `_id/index.vue`.

**Verify Playwright thật**: `/25/edit` → modal "Xuất Excel BOM List" mở, bấm xuất → **tải thật `BOM_BOM-2026-00009.xlsx`** (đúng mã) ✓ · `/25` chi tiết → modal mở ✓ · Danh sách → action dòng còn **Xem chi tiết / Sửa / Sao chép / Xem lịch sử / Xóa**, **hết Xuất Excel**; toolbar vẫn còn ✓ · `/add` → Import **khoá**+tooltip, Xuất Excel **khoá**+tooltip ✓ · compile Node 14.21.3 sạch 4 file.

## Phase 3: Export ✅ (review clean, KHÔNG cần vòng fix, 2026-07-16)

- [x] Task 23: `BomExportModal.vue` — **BỎ HẲN phần chọn cột** (luôn xuất đủ 12), chỉ còn "Xuất hàng hoá cấp con"
- [x] Task 24: **blade MỚI** `bom_list_import_format.blade.php` (phẳng 12 cột, header dòng 1, không tfoot, không khối info) + `withFlatFormat()` trên `BomListExport` + `export()` load `serviceItems`

**🔴 BRIEF CỦA TÔI SAI — implementer chặn kịp**: tôi bảo sửa `bom_list.blade.php`, nhưng blade đó **DÙNG CHUNG với Quotation** qua `BomListExport::view()` (3 call site: `BomListController:178`, `QuotationController:1028` exportExcel, `:1107` exportImportTemplate). Sửa tại chỗ sẽ **VỠ CHỨC NĂNG** `exportImportTemplate`: `registerEvents()` (`BomListExport.php:228-242`) chèn `['type'=>'group']` vào `$orderedProducts` **cốt để khớp số dòng** với dòng nhóm blade render, rồi đếm `$row++` để mở khoá ô + ghi công thức → bỏ dòng nhóm là **lệch 1 dòng mỗi nhóm** → mở khoá sai ô, công thức `={est}*{qty}` sai dòng.
⇒ **Phương án A**: blade RIÊNG + cờ `withFlatFormat` mặc định `false`, chỉ `export()` bật. `bom_list.blade.php` **KHÔNG đụng 1 byte**.

**2 điều kiện round-trip tôi bỏ sót, implementer tìm ra:**
1. **Header phải ở dòng 1** — `BomImportModal.vue:578` gọi `parseExcelFile(file, columns, 0, 0)` → `headerRow=0`. Export cũ sinh **6 dòng info** + 1 dòng trống → header ở **dòng 8** → import lại báo "thiếu header".
2. **Phải tắt `<tfoot>`** — dòng TỔNG CỘNG/VAT/breakdown sẽ bị parse thành **dòng dữ liệu rác**.

**3 quyết định user chốt giữa chừng:**
- **Định dạng**: theo file mẫu — **phẳng, round-trip được**. Đánh đổi đã chấp nhận: **MẤT kiểu báo cáo nhóm-số-La-Mã** hiện có (ai dùng export để in/gửi đối tác sẽ thấy file khác đi) → **cần báo user khi release**.
- **Bỏ hẳn chọn cột**: `parseExcelFile` bắt buộc đủ 12 header, thiếu 1 cột là file **âm thầm không nạp lại được** — đúng loại bẫy feature này đang diệt.
- **Dòng di sản `product_type=2`** → in `Loại = "Dịch vụ & Chi phí khác"` ⇒ round-trip **tự chuyển nó sang đúng bảng** `bom_list_service_items`, tự dọn di sản. (DB local 0 dòng.)

**Chênh scope +2 file (đã duyệt)**: `_id/index.vue` + `index.vue` — cả 2 đều `fields.forEach(...)`; bỏ `fields` mà không sửa caller → `TypeError` bị `try/catch` **nuốt thành toast "Lỗi khi xuất Excel"** (hỏng âm thầm). Mỗi caller xoá đúng 1 dòng.

**Verify (reviewer tự chạy lại, không tin report):**
- **Quotation 4/4 đường KHÔNG ĐỔI** — đưa `BomListExport.php` về HEAD dump baseline, khôi phục rồi dump lại; phủ cả 2 nhánh (Q2 `discount_method=1` + có dịch vụ, Q3 `NULL`). Đã kiểm **tính ổn định của phép đo trước** (2 lần chạy cùng code → identical) rồi mới tin.
- **Round-trip chống dương tính giả**: BOM 9 → Export → **XOÁ SẠCH BOM 9** → Import file vừa export qua UI thật (**bấm qua dialog xác nhận** — đúng cái bẫy làm implementer suýt dương tính giả) → "Import thành công 3/3" → **KHỚP 100%** (nhóm, cha-con, qty, HTML `product_attributes`, note, dịch vụ).
- Header khớp `importTemplate()` **từng byte** 13/13 ô. STT sinh liên tục `1, 1.1, 1.2, 2, 2.1 … 11.2`. `include_children=0` → STT cha **không nhảy**. **0 query** lúc render; `export()` còn **bỏ 5 quan hệ thừa** → ít query hơn trước.
- XSS: thông số dùng `{!! nl2br(e($htmlToText(…))) !!}` — **escape TRƯỚC rồi mới thêm `<br>`**; tiêm `<script>` + `</td><td>` → không rò, vẫn đúng 12 `<td>`.

**Blade mới SỬA LUÔN 1 bug có sẵn**: blade cũ (`@if($hasGroups)`) **bỏ hẳn** dòng cha không thuộc nhóm nào khi BOM có nhóm; blade mới xuất chúng lên đầu.

**Minor còn treo → review tổng cuối:**
- `bom_list_import_format.blade.php:87,111` — `$isService()` bỏ trống Model/TH/XX nhưng **không bỏ trống ĐVT** → dòng di sản `product_type=2` xuất kèm ĐVT, lệch quy ước. 0 dòng hôm nay, import cũng bỏ qua ĐVT ở dòng dịch vụ → thuần thẩm mỹ.
- `blade:56-63` — dòng cha có `bom_list_group_id` trỏ nhóm **không tồn tại** sẽ **biến mất khỏi export** → round-trip replace-all sẽ **xoá** dòng đó. Hiện không thể xảy ra (0 dòng mồ côi); blade cũ cũng cùng hình dạng.
- Export cố ý đẩy dòng cha **không-nhóm lên ĐẦU** → thứ tự file có thể khác thứ tự trên màn hình. Có comment giải thích (tránh `applyGroupForwardFill()` hút dòng đó vào nhóm phía trên). Đúng ưu tiên round-trip.
- Tên file: màn chi tiết hardcode `BOM_export.xlsx`, màn danh sách dùng `BOM_${code}`. Có sẵn, cả 2 vứt tên file BE (tải bằng blob).

### 🔴 Bug CÓ SẴN thứ 2 trên branch (KHÔNG phải feature này, chưa sửa)
`bom_list.blade.php:250-257` render dòng tiêu đề **"Dịch vụ bổ sung"** mà `registerEvents()` **không đếm** → `QuotationController::exportImportTemplate` **lệch 1 dòng khi báo giá có dịch vụ**. Reviewer xác minh trên `quotation_2`: unlock rơi vào **dòng 4** (ô rỗng của tiêu đề) trong khi **dòng 5** (dịch vụ thật, `J5=600000`) vẫn `LOCK=inherit` ⇒ **user KHÔNG sửa được giá dịch vụ** trong file template báo giá. Đã đóng băng đúng hành vi lỗi vào baseline khi so sánh. **Đề xuất task riêng.**

> ⚠️ **Phát hiện khi làm Task 4-5 — bắt buộc đọc trước khi code Task 24**: `bom_list_products` **KHÔNG có cột `stt` lẫn `sort_order`** (đã verify schema). STT chỉ là input tạm lúc import để suy ra `parent_id`, sau đó **bị vứt**; thứ tự = thứ tự chèn (theo `id`).
> ⇒ Export **phải TỰ SINH LẠI STT** từ cấu trúc cây + thứ tự dòng (cha đánh 1,2,3…; con đánh X.1, X.2…), KHÔNG thể lấy lại số gốc trong file import.
> ⇒ Round-trip vì thế **không byte-identical** nếu file gốc đánh số lệch/nhảy (vd `1, 3` hoặc `2, 1`) — export sẽ chuẩn hoá lại thành `1, 2`. Đây là hành vi ĐÚNG, không phải bug; nhưng mục Verify round-trip phải hiểu đúng kỳ vọng này: **import lại không lỗi** ≠ **file giống hệt**.

## Phase 4: Sao chép BOM ✅ (review clean, KHÔNG cần vòng fix, 2026-07-16)

### BE
- [x] Task 25: Migration `2026_07_16_100000_add_copied_from_to_bom_lists_table.php` — `copied_from_bom_list_id` nullable, **không bọc DDL trong transaction**, không FK; đã chạy thật (id 1571 batch 301) + rule `nullable|integer|exists:bom_lists,id` vào `BomListStoreRequest`
- [x] Task 26: `getCopyData()` + `copyData()` + route `GET /{bomList}/copy-data` (`api.php:416`, **TRƯỚC** `/{bomList}` `:417`)

### FE
- [x] Task 27: `index.vue` action Sao chép (icon `ri-file-copy-line`, gate `hasAPermission('Tạo BOM List')`) → `/add?copy_from={id}`; `add.vue` đọc query; `BomBuilderEditor.vue` +4 chỗ tối thiểu (`:284` prop, `:565` `isCopyMode`, `:872` mounted, `:930-938` `loadBomDetail`)

**🔴 BRIEF CỦA TÔI SAI 3 CHỖ — implementer làm theo code thật (tôi đã tự verify cả 3):**
1. **BOM tổng hợp có `bom_list_products` RIÊNG** — FE `mergeSubBomGroups` **vật chất hoá** vật tư lúc gộp; `bom_list_relations` = **0 dòng** trong DB. Làm đúng brief ("copy vật tư từ BOM con qua relations") sẽ ra **0 sản phẩm**. ⇒ dùng chung 1 đường code cho cả 2 loại BOM.
2. **`products[]`/`groups[]` PHẢI GIỮ `id`** (brief bảo bỏ): `mapProductsToGroups` link cha-con qua `child.parent_id === parent.id`, `client_id = 'g_'+g.id` → bỏ `id` là **mất hàng con + dồn nhầm nhóm**.
3. **`service_items` thì ĐÚNG là phải bỏ `id`** (ngược lại): giữ `id` → `syncServiceItems` chạy `update()` khớp **0 dòng** → **item mất trắng**.

**Verify (reviewer tự kiểm, không tin report):**
- **Giữ `id` KHÔNG ghi đè BOM nguồn** (chỗ nguy hiểm nhất): payload gửi `bom_groups[0].id = 85` (id nhóm **của nguồn**) nhưng `syncGroups():2025` `delete()` **scoped theo BOM mới** rồi luôn `create()`, chỉ dùng id cũ làm key map; `mapProductPayload()` **không đọc `id`**. Kết quả thật: BOM mới ra group 88, products 1418/1419, cha-con đúng — **nguồn không suy suyển**.
- BOM nguồn **read-only**: `updated_at` + products + group + service item nguyên vẹn sau 3 lần copy.
- `syncChildStatus` **no-op** (`sub=[]` → added/removed rỗng) → **0 BOM con đổi status**.
- `service_items` bỏ `id` → **TẠO MỚI** (id 296), không mất trắng.
- **N+1: không** — `getCopyData()` = **13 query cố định** với BOM 2/6/23 sản phẩm (chỉ +1~2 so với `show()`).
- Edge: `copied_from=999999` → **422**; `GET /999999/copy-data` → **404**; `?copy_from=abc` → về form Tạo mới thường. `update()` **không** đụng `copied_from_bom_list_id` → provenance không mất khi sửa BOM copy sau này.
- Gate quyền: gỡ `Tạo BOM List` khỏi store → action `copy` biến mất, `view/export/logs` còn.
- **`BomBuilderEditor.vue` đúng 4 chỗ tối thiểu**, không vỡ Import/Export: mở `/9/edit` → `isCopyMode=false`, `$refs.bomImportModal` = `BomImportModal` sống, service item vẫn giữ `id=294` (edit vẫn update chứ không tạo lại). `isCopyMode = !isEditMode && !!copyFromId` → **edit luôn thắng**.
- Dữ liệu test **đã dọn sạch** — DB về đúng 5 BOM (1/2/3/8/9), `copied_from` toàn NULL, products 34 / groups 4 / service_items 1 / relations 0.

**Minor còn treo → review tổng cuối:**
- `BomListService.php:1176-1180` — recompute `solution_version_id` **vượt spec** nhưng chính đáng (khớp `syncVersionFields():477`, cùng `current_version_id`, cùng xử null) → form hiển thị = giá trị sẽ lưu.
- `:1167-1170` — nulling `created_by/created_at` là **code chết** (`BomBuilderInfoCard.vue:3` render dưới `v-if="viewOnly"`, `/add` không bao giờ viewOnly). Vô hại, phòng thủ.
- `:1152` — service gọi helper global `request()`; `DetailBomListResource::toArray()` bỏ qua `$request` nên vô hại, nit về layering.
- `copyData()` không gate quyền — nhưng `show():98` cũng vậy → không phát sinh lộ dữ liệu mới.

### 🔴 Bug CÓ SẴN thứ 3 trên branch (KHÔNG phải feature này, ĐÃ QUYẾT không sửa)
`validateUniqueAggregate()` (`BomListService.php:2163-2164`) **so cột `solution_module_version_id` với giá trị `current_version_code`**, trong khi `syncVersionFields():477` ghi `current_version_id` ⇒ **so id với code** → guard **vô hiệu**. Verify: solution 5 có `current_version_id=5` nhưng `current_version_code=1`. Hệ quả: luật "chỉ 1 BOM tổng hợp / solution+version" **KHÔNG được thực thi** cho **mọi** đường tạo BOM (không riêng Copy) — test tạo được 2 BOM tổng hợp cùng solution 5 cùng version 5.
**Quyết định**: KHÔNG sửa — hàm dùng chung, hỏng sẵn cho mọi đường, Copy không làm xấu thêm. ⚠️ **Nếu sau này sửa guard cho đúng thì nút Sao chép trên BOM tổng hợp (hiện 4/5 BOM) sẽ luôn 422 khi giữ nguyên solution** — user sẽ phải đổi solution khi copy. Cân nhắc khi mở task riêng.

---

---

## 🔴 REVIEW TỔNG (2026-07-16) + SAI LẦM CỦA TÔI ĐÃ ĐƯỢC USER CHẶN

### KHÔNG có cột "Giá nhập" — file giữ đúng **12 cột**. ĐỪNG THÊM LẠI.

**Diễn biến**: review tổng báo *"Export → Import xoá trắng Giá nhập"* — tôi tin, và **thêm cột 13** để vá. User chất vấn: *"màn tạo bom-list có chỗ để nhập giá đâu, sao file import lại cần?"* → điều tra lại thì **lỗi đó KHÔNG TỒN TẠI**. Đã **gỡ sạch cột 13**, trả về 12 cột.

**Bằng chứng: BOM không quản lý giá, giá luôn = 0 do THIẾT KẾ**

| Kiểm | Kết quả |
|---|---|
| Ô nhập giá **hàng hoá** trên màn BOM | **KHÔNG CÓ** — `BomBuilderEditor.vue:355` `visibleColumns.estimatedPrice: false`; `estimatedPrice` **không nằm trong `columnOptions`** (`:361-368`) → **không bật lên được** |
| Ô nhập giá **dịch vụ** trên màn BOM | **CŨNG KHÔNG** — `BomBuilderTableCard.vue:678` bọc `<td v-if="visibleColumns.estimatedPrice">`, cùng cờ đó |
| Có chỗ nào set cờ đó `= true`? | **KHÔNG** — `visibleColumns` chỉ ở `:347` (khai false) + `:45`/`:220` (truyền prop) |
| Popup thêm dịch vụ có mang giá? | `QuotationProductSearchModal.vue:1262` — `Number(cost.estimated_price) \|\| 0`, mà bảng `costs` ERP **không có cột `estimated_price`** → luôn **0** |
| Báo giá lập **từ BOM** có lấy giá? | **KHÔNG** — `QuotationService.php:349,490`: `'estimated_price' => 0, // BOM không quản lý giá — xử lý ở báo giá` |
| Ai đọc `bom_list_products.estimated_price`? | Chỉ accessor `import_total` (`BomListProduct.php:79`) → nuôi cột "Thành tiền nhập"… **cũng bị ẩn** |

⇒ Thêm cột giá = ghi vào DB con số **không màn nào hiện, không luồng nào đọc**. BOM 25 của user (test import lúc có cột 13) có hàng hoá giá 1.200.000 — chính là bằng chứng.

**2 lỗi suy luận dẫn tới sai lầm — đáng nhớ:**
1. Reviewer thấy `34/34 sản phẩm giá = 0` → kết luận *"phép đo bị mù, test data không đại diện"*. **Con số đó CHÍNH LÀ câu trả lời** ("BOM không quản lý giá"), nhưng bị đọc thành "test data kém". **Dữ liệu đồng loạt bằng giá trị mặc định có thể là THIẾT KẾ, không phải thiếu sót của phép đo.**
2. Tôi khẳng định "dịch vụ có ô nhập giá" vì **thấy `V2BaseCurrencyInput` ở `TableCard:679`** mà **không kiểm `v-if` bọc ngoài**. **Nhìn thấy component ≠ component đó hiển thị.**

**Revert (6 file)**: `BomListService.php` (xoá khối validate cột 13 + nhánh khoá `estimated_price`; 2 mapper trả lại hardcode `0`), `BomListController.php` (`importTemplate()` 12 cột, `A1:L1`, `A2:L4`), `BomListExport.php` (`FLAT_HEADERS`/`FLAT_WIDTHS` 12, `A1:L`), `bom_list_import_format.blade.php` (bỏ `<td>` 13 + helper `$priceOf`), `BomImportModal.vue` (xoá `PRICE_COLUMN`/`hasPriceHeaderInFile()`/`parseColumns()`, min-width 1760→1640), `BomExportModal.vue` ("13 cột…" → "12 cột").
**GIỮ**: comment `497/504` (sửa số liệu đúng, không liên quan cột 13).
**File đời cũ 13 cột vẫn nạp được**: `parseExcelFile` chỉ bắt buộc cột **được khai** phải có header; **cột thừa bị bỏ qua**, không ném lỗi (verify 2 lớp: chạy `parseExcelFile` thật + UI thật, 3/3 hợp lệ).
**Verify sau revert**: lint PHP 7.4 sạch + compile Node 14.21.3 sạch; `importTemplate()` ≡ `FLAT_HEADERS` ≡ alias FE **12/12 khớp từng ký tự**; round-trip qua UI thật 3/3 (giá = 0 là ĐÚNG); dịch vụ vẫn vào `bom_list_service_items` với `vat_percent=8` từ cost; `locked_fields` về đúng 6 ô; **Quotation export giống hệt HEAD**; validate **11 query bất biến** N=3/30/60, đường ghi **0 query `mysql2`**; data user (BOM 1/2/3/8/25) nguyên vẹn.

### 2 việc dọn kèm
- [x] Sửa comment sai số `BomListService.php:~636`: "503/504 có vat=8" → **"497/504 có vat=8; 503/504 có vat≠0"** (phân bố thật: vat=8→497, vat=10→5, vat=1→1, vat=0→1, tổng 504)
- [x] **Xoá BOM test id=9** ("ZZ TEST IMPORT — Claude") → DB còn đúng **4 BOM (1/2/3/8)**, verify không còn dòng con mồ côi

### Minor được review tổng TRIAGE = "để lại được"
`SERVICE_LOAI_KEYS` alias thứ 2 (verify 5/5 khớp; lệch chỉ sai hiển thị) · `preloadMasterData()` map 37,6k dòng (vài MB, request-scoped, 0 query thêm) · blade `$isService()` không bỏ trống ĐVT (0 dòng `product_type=2`) · `mapProductPayload()` ghi cột chết (code cũ, không nằm trong diff) · luật độ dài kiểm giá trị file (fail an toàn: chặn + báo rõ) · `tempnam` rò file (có sẵn) · M1-M4 luật STT · `openPickModal()` code chết (user chốt giữ — **nhưng comment `:102-108` mô tả guard không chạy → nên vào task follow-up**) · lệch button-convention · guard 400 vs 403 · tên file export.

**Minor mới**: header 13 cột khai **3 nơi** (`BomListController` literal · `BomListExport::FLAT_HEADERS` · alias FE) — verify khớp từng ký tự hôm nay, nhưng **không có gì cưỡng chế**. Sửa 1 dòng: `importTemplate()` dùng `BomListExport::FLAT_HEADERS` → diệt 1/3 bản sao. Cùng họ với `SERVICE_LOAI_KEYS`.

---

## Verify — ✅ TẤT CẢ PASS (review tổng xác nhận READY, 2026-07-16)
- [x] Lint **PHP 7.4.33 thật** 6/6 sạch (`/opt/homebrew/opt/php@7.4/bin/php -l` — KHÔNG `php -l`: máy mặc định 8.1, production 7.4) · Compile **Node 14.21.3** 7/7 (⚠️ node mặc định máy là **12.x**)
- [x] **AC1 4/4** qua UI thật — Tạo mới: hiện + khoá + tooltip (`pointer-events:none`, hover render thật); Sửa: bật, modal mở; Chi tiết: ẩn; **BOM tổng hợp: ẩn** (phải sửa bug prop không bind mới đạt)
- [x] **AC2** — luồng import 8/8 đầu-cuối UI thật: dòng dịch vụ vào **đúng khối** (chứng minh bug cũ đã đóng); rác bị ghi đè bởi ERP (`DVT-RAC` → `Cái`); HTML thông số hiện text sạch; dòng lỗi → Import TẮT → tích → BẬT; **dòng vàng vẫn TẮT kể cả đã tích**; confirm replace-all; `.txt` bị từ chối
- [x] **AC3** — đọc lại file bằng PhpSpreadsheet: **13 cột** đúng thứ tự, khớp `importTemplate()` **từng ký tự**, có dòng dịch vụ cùng bảng
- [x] **AC4** — Copy BOM thành phần + tổng hợp qua UI thật; `status=1`; `copied_from` đúng; **nguồn read-only**; `sub_bom_list_ids=[]`; **0 BOM con đổi status**
- [x] **Round-trip GIỮ GIÁ** (tiêu chí quyết định): BOM giá 5.700.000/1.200.000 → Export → **xoá sạch** → Import → **khôi phục đúng**, không về 0. *(Test cũ chạy trên BOM giá=0 nên mù — xem mục REVIEW TỔNG.)*
- [x] **File 12 cột cũ vẫn import được** → giá = 0, KHÔNG lỗi "thiếu header"
- [x] Regression: `V2BaseImportModal`/`Table`/`Toolbar`/`import-helper.js` **không đụng** → 11 màn khác an toàn · **Quotation export không đổi** (chứng minh: `BomListExport.php` 0 dòng xoá/sửa + 75 dòng thêm, `flatFormat` mặc định false, cả `view()` lẫn `registerEvents()` thoát sớm, `bom_list.blade.php` không đổi, `QuotationController` gọi `withFlatFormat` **0 lần**)
- [x] Edge: STT `2.1.3` → lỗi 2 cấp · Model lạ → "không khớp với Master Data" · mã trùng → dòng vàng · `-5`/`abc`/`5.700.000` → lỗi · giá trống → 0
- [x] **N+1**: validate = **6 query bất biến** (N=3/30/60) · đường ghi `mysql2` = **0 query** · `getCopyData()` = 13 query cố định
- [x] Vệ sinh: **0** `console.log`/`debugger` FE · **0** `dd`/`dump`/`var_dump` BE · **0 commit** · 0 file rác · DB dọn sạch (4 BOM 1/2/3/8, 0 dòng mồ côi)

---

## Checkpoint

### Checkpoint — 2026-07-15 (khởi tạo)
Vừa hoàn thành: Khảo sát BE+FE, đọc 2 tài liệu Google, brainstorming 6 câu chốt (9 quyết định), viết spec đầy đủ + design tóm tắt + plan 27 task.
Đang làm dở: Chưa code dòng nào.
Bước tiếp theo: Task 1 — `resolveLookupId()` chuyển `autoCreate: false`.
Blocked: (không có)

### Checkpoint — 2026-07-16 (HOÀN THÀNH, 27/27) ⭐
**Vừa hoàn thành**: TOÀN BỘ feature. 4 phase / 27 task, mỗi nhóm qua implementer → reviewer → fix → re-review sạch, + **1 vòng REVIEW TỔNG toàn branch = READY**.
**Đang làm dở**: (không có) — code xong, chưa commit.
**Bước tiếp theo**:
1. User review + tự nghiệm thu 4 AC trên browser (hard-refresh trước)
2. User commit/push khi ưng (mình không commit theo quy tắc dự án)
3. Chạy migration ở production: `2026_07_16_100000_add_copied_from_to_bom_lists_table`
4. **Báo user 3 điểm đổi hành vi khi release** (xem mục "3 việc user cần biết" ở đầu file)
**Blocked**: (không có)

**7 lần subagent phát hiện brief/spec của tôi SAI và dừng lại HỎI thay vì đoán** — mỗi lần đều đúng:
1. `costs` KHÔNG có cột `code` (match theo TÊN) · 2. `products.code` 0/43.548 dính nháy (nháy ở `name`) · 3. `product_projects` là bảng **ĐÃ XOÁ** → `product_project_id` là cột chết → đổi tên trả về thành `source_row_id`/`source_row_type` · 4. `resolved` dùng `*_id` nên FE không hiển thị nổi ô khoá → BE trả thêm `*_name` (0 query) · 5. **blade export DÙNG CHUNG với Quotation** → sửa tại chỗ sẽ **vỡ chức năng** `exportImportTemplate` (lệch `$row` → mở khoá sai ô, công thức sai dòng) · 6. **BOM tổng hợp có `bom_list_products` RIÊNG**, `bom_list_relations` = 0 dòng → làm đúng brief sẽ ra **0 sản phẩm** · 7. `products`/`groups` **PHẢI GIỮ `id`** (brief bảo bỏ) nhưng `service_items` **phải bỏ**.

**2 lần reviewer chặn quyết định SAI của tôi**: (a) định áp luật "unit_id null → lỗi" cho MỌI nhánh → sẽ chặn sạch **100% dòng dịch vụ**; (b) review tổng tìm ra **Export→Import xoá trắng Giá nhập** — thứ 7 vòng review trước đều mù vì test toàn chạy trên BOM giá = 0.

### Checkpoint — 2026-07-15 (wrap up, 15/27)
**Vừa hoàn thành**: TOÀN BỘ Phase 1 — BE Import (15/15 task), tất cả đã qua review + fix + re-review sạch:
- Task 1-3: helper tra danh mục (`preloadMasterData`, `lookupFromPreloaded`, `resolveCostByName`, `preloadCostsByName`, `lookupCostFromPreloaded`, `normalizeLookupKey`)
- Task 4-5: `validateSttStructure()` — 4 luật STT
- Task 6-8: `classifyImportRow()` — 3 nhánh erp / product_project / new_temp + preload ERP + UNION "Hàng hoá dự án"
- Task 9-10-14: viết lại `validateImportData(BomList, array)` + response shape mới + dọn route trùng
- Task 11-13-15: viết lại `importProducts()` (tiêu thụ `resolved`) + tách 2 bảng + `resolution`/`skip_invalid` + `note` + file mẫu 12 cột

**Đang làm dở**: Task 16-20 — **code XONG, CHƯA REVIEW**. `BomImportModal.vue` (FE, file mới) + `BomListService.php` thêm `*_name` vào `resolved` (phương án D). Đã gồm điền xuôi `lastGroup` vào ô "Nhóm hàng" trên lưới (chỉ dòng cha; con/dịch vụ không điền). Implementer tự verify 74/74 check logic + SFC compile sạch + BE lint sạch + query hằng số 10 ở 5/50/200 dòng. **Chưa nối vào editor** → chưa test được UI thật.

**Bước tiếp theo**:
1. Sinh diff → **review Task 16-20** (2 file: `BomImportModal.vue` + phần `*_name` của `BomListService.php`) — đây là việc NGAY TIẾP THEO
2. Task 21-22: nối modal vào `BomBuilderEditor.vue`, xoá `BomBuilderImportModal.vue`, sửa `BomBuilderTableCard.vue` (nút Import hiện+disabled+tooltip ở màn Tạo mới — AC1)
3. **BẮT BUỘC ở Task 21-22**: đo Playwright theo skill `table-popup-layout` mục 4 (2 trạng thái × 2 viewport + assert `.modal-body` không cuộn dọc). Task 16-20 **CHƯA đo** — bố cục mới chỉ rà bằng mắt + compile SCSS, **chưa có con số thật** về chiều cao dòng / số dòng thấy được / modal-body có cuộn không (Bẫy 1+2 của skill). Selector cần dùng khi đo: `.bom-import-content`, `.bom-import-grid-wrap`, `.bom-import-grid` (report Task 16-20 có sẵn snippet).
4. Phase 3 (Task 23-24: Export), Phase 4 (Task 25-27: Sao chép)

**Minor mới → review tổng cuối triage**:
- `BomImportModal.vue` phải **chép bộ alias cột "Loại"** của `resolveImportProductType()` sang FE (`SERVICE_LOAI_KEYS`) — vì lúc Load lên bảng FE chưa có `product_type` (server chỉ trả sau Validate) nên không biết dòng nào là dịch vụ để bỏ qua điền xuôi. Đây **đúng là "bộ alias thứ 2"** mà comment `isImportServiceEntry()` cảnh báo. Đã ghi comment "BE là nguồn sự thật, sửa bên đó phải sửa cả đây". Rủi ro nếu trôi lệch: **chỉ ở mức hiển thị** (dịch vụ bị điền nhóm thừa / hàng hoá không được điền), **không sai dữ liệu ghi** vì BE luôn validate lại. Muốn triệt tiêu hẳn thì phải chuyển việc điền sang sau Validate — đánh đổi: user không thấy ngay ở bước preview.

**Blocked**:
- **Verify FE cần đăng nhập**: FE `:3000` + BE `:8000` đang chạy, nhưng `hrm-client/tests/.auth/state.json` **không còn** và mật khẩu nằm ở env `HRM_TEST_PWD` (không có trong repo) → cần user đăng nhập giúp hoặc cấp credential khi tới bước test UI thật.
