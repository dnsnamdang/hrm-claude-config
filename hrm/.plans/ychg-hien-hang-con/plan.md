# Plan — YCHG: hiện hàng con của hàng cha (ERP chỉ-đọc + hàng tạm sửa được)

## Bối cảnh / yêu cầu user
Trên màn lập **Yêu cầu hỏi giá (YCHG)** `sale/price-asking-requests/add`:
1. **Hàng chọn từ ERP**: sau khi chọn, hiện hết hàng con theo **công thức ghép bộ** (`recipe_products`) — **chỉ nhìn, không sửa**.
2. **Hàng tạm chọn từ nguồn kho hàng tạm (Tái sử dụng)**: nếu hàng tạm đó **có con** thì hiện hết con ra, mỗi con có **nút Sửa** cho phép nhập đủ thông tin cho hàng tạm con.

## Phát hiện mô hình dữ liệu (đã kiểm DB `erp_hrm_check`)
- Con ERP (ghép bộ): `recipe_products(base_product_id, product_id, unit_id, qty, is_main)` — 6.213 dòng; `Product::recipeProducts() = hasMany(RecipeProduct,'base_product_id')`. Data test: `BETA-78CT-EMFORD` (id 26274, 78 con).
- Con hàng tạm: cây `bom_list_products.parent_id` (+ `show_children`, `erp_product_id`); lấy qua endpoint SẴN CÓ `GET assign/product-projects/reuse-children?source_type=bom|quotation&source_id=`. Luồng quote/BOM đã có `_reuseChildren` (`QuotationProductSearchModal.addSelectedReuse` + `fetchReuseChildren`).
- YCHG lưu **phẳng** `product_ids` (không có cột cha-con). Dòng YCHG gom theo Thương hiệu×Hãng (`PriceAskingRequestWriter::rebuildLines`).
- `ProductCompany` table thật = `product_company_coefficients` (status TEMP 6/7/8).

## Quyết định đã chốt (tự quyết — user bảo "làm đi")
- **QĐ1**: Con ERP là **hiển thị suy ra tại chỗ** từ `recipe_products`, KHÔNG thành dòng YCHG, KHÔNG ảnh hưởng payload lưu. Hiện ở cả màn Thêm lẫn Chi tiết/Sửa.
- **QĐ2**: Chia 2 phase. Phase 1 (con ERP chỉ-đọc) KHÔNG đụng `QuotationProductSearchModal.vue` (component dùng chung) — chỉ sửa BE reader + form YCHG. Phase 2 (con hàng tạm) có đụng modal dùng chung → bám pattern `_reuseChildren` sẵn có.
- **QĐ3**: Con ERP chỉ gắn cho dòng **không phải hàng tạm** (`!is_temp`). Query gộp 1 lần theo toàn bộ ids (không N+1).

---

## Phase 1 — Con ERP chỉ-đọc (công thức ghép bộ)

### Tasks
- [x] Task 1 — BE: `PriceAskingProductReader::enrich()` gắn `recipe_children` cho dòng ERP (`!is_temp`) có `recipe_products`. Thêm method private `recipeChildren(array $ids)`: 1 query gộp `recipe_products` JOIN `products` (code,name) + `units` (ĐVT), group theo `base_product_id`, sắp `is_main DESC, id`. Mỗi con: `{id, code, name, qty, unit, is_main}`. ✅ verify tinker: id 26274 → 78 con đúng shape.
- [x] Task 2 — FE: `PriceAskingRequestForm.vue` lưới — dưới mỗi dòng SP có `recipe_children`, render dòng con **chỉ đọc**, thụt lề, màu xám `#6b7280`, nhãn "Công thức ghép bộ: N hàng con (chỉ xem)". Không nút sửa/xoá. Không in đậm, không tô đỏ. ✅
- [x] Task 3 — Kiểm Playwright: mở `127.0.0.1:3000/sale/price-asking-requests/add?product_ids=26297` (26274 bị chặn ở cty 1), xác nhận dòng cha `BETA-TP-EM-FORD` có note "Công thức ghép bộ: 76 hàng con (chỉ xem)" + 76 dòng con chỉ-đọc hiện dưới (mã/tên/ĐVT, con đầu có tag "Chính"), ô Hành động dòng con rỗng. ✅ PASS, 0 console error liên quan.

### Checkpoint Phase 1 — 2026-10-30
Hoàn thành + verify Playwright. BE `PriceAskingProductReader.php` (recipe_children), FE `PriceAskingRequestForm.vue` (recipe-note + dòng con chỉ-đọc + CSS). CHƯA commit.

---

## Phase 2 — Con hàng tạm sửa được (CHỜ sau Phase 1)

### Quy tắc nghiệp vụ đã CHỐT (user 2026-10-30)
- **CHỈ hỏi giá cấp CHA.** Mọi hàng con — ERP lẫn hàng tạm — **KHÔNG** là dòng hỏi giá, **KHÔNG** vào `product_ids` payload.
- **Con hàng ERP**: chỉ show (Phase 1, xong).
- **Con hàng tạm**: show dưới cha + nút **Sửa** mở modal nhập đủ thông tin cho hàng tạm con; con vẫn **không** được hỏi giá.
- **Chặn gửi duyệt**: còn hàng tạm con **chưa đủ thông tin** → phiếu **không gửi được**, hiện thông báo rõ con nào/thiếu gì.

### Hướng đã CHỐT (user 2026-10-30) — xem design-phase2.md
- **A = BE tự tạo con.** FE chỉ gửi `source {type,id}` (đã có sẵn trong `buildTempPayload`). BE khi tạo hàng tạm cha từ YCHG tự đọc con của source → tạo hàng tạm con (status 6) + link `recipe_products(base=cha, product=con, is_main=0)`. Con đã có `erp_product_id` → link thẳng, KHÔNG tạo trùng. → **KHÔNG sửa `QuotationProductSearchModal.vue` dùng chung.**
- **B = chỉ 1 cấp con trực tiếp.**

### Tasks Phase 2
- [x] Task 4 — BE tạo con: `TempProductService::create($data, $source)` — khi payload YCHG có `source {type,id}` và nguồn có con trực tiếp: `buildTempChildren()` đọc `bom_list_products`/`quotation_product_prices` theo `parent_id`; con có `erp_product_id` → link id đó, con thô → `createTempChild()` tạo hàng tạm (status 6) kế thừa model/brand/origin + manufacture placeholder của cha, units từ `unit_id`. Trả `recipes[]` → `ProductWriteService::writeKits` ghi `recipe_products(base=cha, product=con, is_main=0)`. Chạy trong transaction cùng cha; backfill `erp_product_id` cho dòng nguồn. ✅ verify tinker (parent line 338 → 4 con 48xxx, pcc_status=6, recipe_products=4). Khai thêm `product_type_id/vat_percent_tax_rate_id = null` trong childData để shared writer không chạm index thiếu (dọn PHP Notice line 546).
- [x] Task 5 — BE reader: `PriceAskingProductReader::recipeChildren()` trả con cho CẢ cha ERP lẫn cha tạm; mỗi con kèm `product_id, is_temp, is_complete, editable`. `markEditable()`: `editable = parentIsTemp && child.is_temp`. `is_complete` = `product_type_id!==null && model_id!==null && vat_percent_tax_rate_id!==null && có ≥1 product_units`. ✅ verify tinker: con tạm → is_temp=true, is_complete=false, editable=true.
- [x] Task 6 — BE chặn gửi: `PriceAskingRequestWriter::validateInput()` khi `send=true` gọi `incompleteTempChildren()` (join `recipe_products`→`products`→`pcc` TEMP_STATUSES per-company) → gom con tạm chưa đủ thông tin theo cha, đẩy vào `$errors['temp_children']` → `ValidationException` (422). Defense-in-depth. ✅ verify tinker: 4 con thiếu → báo đúng; sau khi bổ sung product_type/model/vat → hết chặn.
- [x] Task 7 — FE form: `PriceAskingRequestForm.vue` — dòng con `editable` thêm nút **Sửa** (`openTempEdit(child.product_id)`); con thiếu → chip hổ phách "Thiếu thông tin" (KHÔNG đỏ, theo rule đỏ-chỉ-validate); recipe-note động (bổ sung / chỉ xem) + `.recipe-missing-note`; `save(send)` chặn client-side qua `incompleteTempChildrenList` + toast; `onTempUpdated` refetch dòng cha để cập nhật `is_complete` sau khi sửa con. CHƯA kiểm Playwright.
- [x] Task 8 — Kiểm Playwright (fixture persist parent product_id 48532 lập từ bom line 338): ✅
  - Dòng cha hiện "Lập từ HH-00002 · BOM BOM-2026-00016" + note động "Công thức ghép bộ: 4 hàng con (bổ sung đủ thông tin trước khi gửi)" + note hổ phách "Còn 4 hàng con tạm chưa đủ thông tin — chưa gửi được".
  - 4 dòng con tạm: mỗi dòng chip "Thiếu thông tin" (đo computed color `rgb(180,83,9)`=#b45309 trên nền `rgb(254,243,199)`=#fef3c7 — KHÔNG đỏ, hợp rule) + 1 nút Sửa (tổng 5 icon sửa = 4 con + 1 cha).
  - Nút Sửa con → mở panel "Sửa hàng tạm · AOKA-21202" điền sẵn Tên "Mỏ lết 8 inch", ĐVT "Bộ" (khoá), Model/Thương hiệu/Xuất xứ/Hãng SX kế thừa cha; đúng 2 ô còn trống = % VAT + Loại sản phẩm (2 trường khiến is_complete=false).
  - "Lưu và gửi duyệt" khi con chưa đủ → KHÔNG POST tới price-asking-requests, ở lại /add (chặn client-side). BE send-block đã verify ở Task 6 (hoàn tất con → hết chặn).
  - **Không regress Phase 1**: product_ids=26297 (BETA-TP-EM-FORD) vẫn note "76 hàng con (chỉ xem)", 76 dòng con read-only (0 nút sửa, 0 chip), con đầu tag "Chính".
  - Dọn fixture sau test: products=0 recipe=0 units=0 pcc=0, bom lines 339-342 `erp_product_id` về NULL.

## Checkpoint Phase 2 — 2026-10-30 (DONE, verified Playwright)
Task 4/5/6 verify tinker PASS. Task 7 FE + Task 8 Playwright PASS (fixture đã dọn sạch). Toàn bộ Phase 1 + Phase 2 hoàn tất.

## Commit + push — 2026-10-31
Chỉ stage đúng 4 file feature (loại các thay đổi WrAccountingService/finance không liên quan còn trong working tree), rebase lên origin/develop rồi push:
- hrm-api `develop` **3e46dd0db** — 3 file BE (PriceAskingProductReader, PriceAskingRequestWriter, TempProductService).
- hrm-client `develop` **6ebff1775** — 1 file FE (PriceAskingRequestForm.vue).
Các thay đổi không liên quan (Finance/WrAccountingService, docs/superpowers…) vẫn để nguyên trong working tree, CHƯA commit.
