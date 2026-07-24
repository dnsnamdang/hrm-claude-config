# Plan: Trường "Bảng giá" (ERP price list) cho Báo giá

> Design tóm tắt: `.plans/baogia-bang-gia/design.md`
> Spec đầy đủ: `docs/superpowers/specs/2026-07-17-baogia-bang-gia-design.md`

## Trạng thái
- Bắt đầu: 2026-07-17
- Phụ trách: @manhcuong
- Tiến độ: 13/13 task ✅ (code + verify; chờ review tổng)
- Code pushed: ❌

## Ràng buộc chung (mọi task)
- BE **PHP 7.4** — lint `/opt/homebrew/opt/php@7.4/bin/php -l` (KHÔNG `php -l`, máy mặc định 8.1). Không cú pháp PHP 8.
- FE **Vue 2 / Node 14.21.3** — gọi đúng binary (node mặc định máy là 12.x). Không cú pháp Vue 3.
- KHÔNG commit git. KHÔNG viết file test (dự án không PHPUnit). Verify: `php -l` + tinker DB thật (bọc `DB::beginTransaction`/`rollBack` khi ghi; ERP mysql2 CHỈ đọc, không ghi) + Playwright UI.
- Migration: không FK, không transaction. Cột `price_type_id` nullable; đọc `null → 1` (Bán lẻ).
- **Bảng giá = `price_type_id`**; danh mục ERP `price_types` (mysql2): 1 Bán lẻ, 2 Đại lý cấp 1, 3 Đại lý cấp 2, 4 Đại lý cấp 3, 5 Giá bán theo lô, 6 Giá bán TMĐT.
- **Chỉ đổi giá BÁN** (`quoted_price`) hàng ERP theo price_type; **giá vốn (`estimated_price`) giữ nguyên** (`cost_price` không theo bảng giá). KHÔNG đụng logic GG/VAT/tổng.
- Backward-compat: `TpProductUnitPrice` thêm param `priceTypeId` **default 1** — caller cũ không đổi hành vi.
- Giá không có ở bảng giá đã chọn → `quoted_price = 0` (không fallback). Chỉ đổi được khi **Đang tạo**.

---

## Phase 1: DB + Danh mục + Model

### BE
- [x] Task 1: Migration `2026_07_19_100000_add_price_type_id_to_quotations_table.php` — cột `price_type_id` unsignedBigInteger nullable, sau `currency_id`, không FK/transaction. Migrate + verify cột nullable, báo giá cũ đều NULL.
- [x] Task 2: `TpProductUnitPrice` tham số hoá `priceTypeId` (default 1): `getUnitOptions(array $erpIds, int $priceTypeId = 1)` (~:141), `getUnitPrice($erpId, $unitId, int $priceTypeId = 1)` (~:180/196), `getRetailPrices` (~:46) — thay `where('pup.price_type_id', 1)` → `$priceTypeId`. `cost_price` KHÔNG đụng. Verify: tinker gọi với priceTypeId=2 trả giá Đại lý cấp 1 khác giá =1.
- [x] Task 3: Endpoint `GET /assign/quotations/price-types` → `DB::connection('mysql2')->table('price_types')->orderBy('order')->get(['id','name'])`, cache 10' (copy pattern `BomListController::getCurrencies` + `erpProductCatalogs`). Route + controller method.

## Phase 2: BE — áp giá theo price_type

- [x] Task 4: `QuotationService` store/update lưu `price_type_id` (từ request, mặc định 1); truyền price_type của báo giá vào `getUnitOptions`/`pickUnitPrices` (~:2489) ở mọi nơi lấy giá hàng ERP (materialize BOM ~:116, direct). `QuotationImportService::erpPrices` (~:2010) dùng price_type báo giá. Giá 0 → `quoted_price = 0`. Giá vốn giữ.
- [x] Task 5: `ErpProductSearchService::search()` (~:80) + controller `erpProductSearch` (~:611) nhận `price_type` từ FE (mặc định `RETAIL_PRICE_TYPE_ID`). FE truyền price_type_id báo giá khi search hàng.
- [x] Task 6: Endpoint re-price `POST /assign/quotations/erp-reprice` — nhận `{price_type_id, currency_id, items:[{erp_product_id, unit_id}]}` → `getUnitOptions(erpIds, price_type_id)` + `pickUnitPrices` + chia tỷ giá → trả `[{erp_product_id, unit_id, quoted_price}]`. Không ghi DB. Route + controller + service method.
- [x] Task 7: `QuotationErpSyncService` (~:244) — `'price_type' => $quotation->price_type_id ?: 1` thay số 1 cứng.
- [x] Task 8: `DetailQuotationResource` trả `price_type_id` + `price_type_name` (map 6 loại hoặc join ERP). `QuotationStoreRequest`/`UpdateRequest` thêm rule `price_type_id` `required|integer|in:1,2,3,4,5,6`; update báo giá đã gửi duyệt bỏ qua thay đổi (khoá).

## Phase 3: FE — dropdown + áp giá + hiển thị

- [x] Task 9: `edit.vue` — thay placeholder read-only "Bảng giá áp dụng: Bán lẻ" (~:186-188) bằng **dropdown Bảng giá** (V2BaseSelect, `v-model="form.price_type_id"`, `:options="priceTypeOptions"`, bắt buộc, `:disabled="!isCreateMode"`); `loadPriceTypes()` (copy `loadCurrencies`); mặc định `price_type_id=1` khi tạo; buildSavePayload gửi `price_type_id`.
- [x] Task 10: `edit.vue` `handleChangePriceType()` (copy pattern `handleChangeCurrency` ~:181): gọi `/erp-reprice` với dòng hàng ERP hiện có (`erp_product_id != null`) → cập nhật `quoted_price` từng dòng + `refreshParentRollups()` + tính lại tổng; **GIỮ** GG + hàng tạm. Truyền `price_type_id` vào `QuotationProductSearchModal` (search đúng giá).
- [x] Task 11: `edit.vue` `loadDetail` map `price_type_id`→`form`; khi mở Sửa (Đang tạo) tự gọi `/erp-reprice` lấy giá ERP mới nhất theo price_type đang lưu → cập nhật + tính lại (AC4). Màn Xem `_id/index.vue` hiển thị trường **Bảng giá** (`price_type_name` cạnh Loại tiền tệ).

## Phase 4: Verify E2E

- [x] Task 12: Migration production-safe + tinker: `getUnitOptions/getUnitPrice` với priceTypeId 1 vs 2 trả giá khác nhau đúng; `/erp-reprice` trả quoted_price đúng theo price_type + tỷ giá; sync ERP payload gửi đúng price_type; báo giá cũ (null) đọc như Bán lẻ; giá vốn không đổi.
- [x] Task 13: E2E Playwright 5 AC trên báo giá test riêng: AC1 dropdown 6 loại mặc định Bán lẻ · AC2 thêm hàng lấy giá Bán lẻ · AC3 đổi Đại lý cấp 1 giá đổi + tổng tính lại + GG giữ · AC4 sửa ERP → mở Sửa giá cập nhật · AC5 Xem hiển thị bảng giá.

---

## Verify (sau khi code)
- [x] Lint BE 7.4 sạch + compile FE Node 14.21.3 sạch
- [x] AC1 — form Tạo có Bảng giá đủ 6 loại, mặc định Bán lẻ
- [x] AC2 — thêm hàng → đơn giá theo Bán lẻ
- [x] AC3 — đổi Đại lý cấp 1 → đơn giá đổi + tổng tính lại; GG/hàng tạm giữ
- [x] AC4 — ERP đổi giá → mở Sửa → đơn giá cập nhật
- [x] AC5 — Xem chi tiết hiển thị đúng bảng giá
- [x] Regression: báo giá cũ null → Bán lẻ; giá vốn không đổi; GG/VAT/tổng không vỡ; sync ERP gửi đúng price_type; caller cũ TpProductUnitPrice (default 1) không đổi hành vi

---

## Checkpoint

### Checkpoint — 2026-07-17
Vừa hoàn thành: Brainstorming (9 quyết định) + khảo sát ERP (price_types 6 loại) + spec + design + plan 13 task/4 phase.
Đang làm dở: Chưa code.
Bước tiếp theo: chọn cách thực thi → Task 1 migration.
Blocked: (không có)

### Checkpoint — 2026-07-17 (CODE DONE + REVIEW TỔNG READY)
Vừa hoàn thành: TẤT CẢ 13 task (subagent-driven; phần lớn inline vì mechanical/small, Task 4 giao subagent). Review tổng whole-branch = **READY, 0 finding chặn merge**.
Verify: Task2 param price_type (PT1 retail=1/PT2=23.9M, cost giữ, no-param=1); Task4 store PT2 quoted=23.9M/cost giữ; Task6 /erp-reprice PT1=1/PT2=23.9M; Task8 resource null→Bán lẻ. E2E browser: AC1 dropdown 6 loại mặc định Bán lẻ PASS; AC2/AC3 đổi bảng giá→2 reprice qua endpoint thật, ERP quoted 1→23.9M, hàng tạm+GG giữ PASS; AC4 mechanism repriceErpRows trên loadDetail khi Sửa+canEdit; AC5 resource+view.
FINDING (không chặn, giống pattern currency user đã chọn): 🟡 thiếu guard server-side khoá đổi price_type sau gửi duyệt (currency_id cũng vậy — pattern sẵn); 🔵 dropdown desync khi huỷ confirm; 🔵 khoá ở !isCreateMode (khoá sớm như currency).
Bước tiếp theo: user nghiệm thu browser (tạo báo giá direct → chọn/đổi bảng giá + thêm hàng ERP + mở Sửa) → commit + chạy migration production.
Blocked: (không có)
