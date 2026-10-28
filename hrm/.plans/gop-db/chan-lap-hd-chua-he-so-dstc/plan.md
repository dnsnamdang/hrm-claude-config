# Chặn lập HĐ khi hàng hoá chưa đủ điều kiện tính DSTC — Implementation Plan

> **For agentic workers:** triển khai từng task theo thứ tự. Steps dùng checkbox (`- [x]`).

**Goal:** Chặn lập HĐ (mới + phụ lục) trên ERP và HRM khi có dòng hàng hoá chưa gắn tính chất, tính chất chưa khai hệ số DSTC, hoặc hệ số = 0; HĐ dịch vụ: dòng "Dịch vụ" (nature 0) phải > 0.

**Architecture:** BE-only. ERP: guard tầng controller TRƯỚC `DB::beginTransaction()` theo idiom `[bool,message]→responseErrors` (vì catch controller nuốt message exception). HRM: guard đầu `createFromQuotation` ném `ValidationException::withMessages` (422). Helper thêm method `validateProducts/validateService` phân biệt 3 reason (`no_nature`/`no_config`/`zero_coef`), KHÔNG đổi method tính hệ số cũ.

**Tech Stack:** ERP Laravel 6.20.44/PHP7.4; HRM API Laravel 8/PHP7.4. DB chung `company_product_natures` + cây `product_natures`.

**Spec:** `.plans/gop-db/chan-lap-hd-chua-he-so-dstc/design.md` (tiền đề: `docs/superpowers/specs/gop-db/2026-10-19-he-so-dstc-theo-tinh-chat-nature-design.md`)

## Global Constraints

- Nhánh: cả 2 repo ở worktree `feat/chan-lap-hd-chua-he-so-dstc` (off `origin/gop_db`). KHÔNG commit/push khi chưa có yêu cầu.
- ERP = Laravel 6 — KHÔNG facade Http, KHÔNG cú pháp L7+/PHP8 (no arrow-fn trong code mới nếu lệch style file; file helper hiện đã dùng closure).
- KHÔNG đổi hành vi `ProductNatureDstcCoefficient::forProduct/forService/forNature` (đang dùng ở điểm tính giá).
- `cachedMap()`/query phải phân biệt "không có dòng" vs "coef 0" bằng `array_key_exists`, KHÔNG truthiness.
- Message nghiệp vụ riêng (không nằm trong bộ validation chung) → viết tiếng Việt theo design §Message.
- Company_id: ERP `auth()->user()->info->company_id`; HRM `optional(optional(auth()->user())->info)->company_id`.
- Số en-US khi format (không áp dụng ở đây, không in số).

## Review Focus

- Hàng tạm HRM `erp_product_id` NULL → phải ra `no_nature` (không bỏ qua).
- Hệ số đúng 0 → `zero_coef` (không nhầm thành OK).
- Tính chất bị xoá khỏi danh mục sau khi khai → leo cây vẫn ra `product_nature_id` (FK không xoá), nhưng company có dòng → vẫn validate theo dòng đó; nếu nature_id trỏ nature đã xoá thì vẫn chặn đúng theo config.
- Bỏ sót 1 controller trong họ HĐ (principle order, service annex) = lọt lưới.
- Trait dùng chung cho cả `FirmContractService` (standalone) và `ZTFirmContractService` (standalone) — 2 lớp không cùng cha.

## File Structure

**ERP (`.worktrees/erp-dstc`):**
- Modify: `app/Support/ProductNatureDstcCoefficient.php` — thêm `validateProducts`, `validateService`, private `cachedMap`; refactor `forNature` dùng `cachedMap` (byte-equivalent).
- Create: `app/Services/Sale/Firm/Contract/Concerns/ValidatesProductNatureDstc.php` — trait: `validateProductNatureDstc(Request): array` (goods) + `validateServiceNatureDstc(?int): array`.
- Modify: `app/Services/Sale/Firm/Contract/FirmContractService.php` — `use ValidatesProductNatureDstc;`.
- Modify: `app/Services/Sale/Firm/Contract/ZTFirmContractService.php` — `use ValidatesProductNatureDstc;`.
- Modify controllers (chèn guard trước `DB::beginTransaction()`), danh sách ở Task 4-6.

**HRM (`.worktrees/hrm-api-dstc`):**
- Modify: `Modules/MasterData/Support/ProductNatureDstcCoefficient.php` — thêm `validateProducts`, `validateService`.
- Modify: `Modules/Assign/Services/ContractService.php::createFromQuotation` — guard goods.
- Modify: `Modules/CustomerCare/Services/WrServiceContractService.php::createFromQuotation` — guard service.

**Message builder dùng chung (mỗi repo 1 chỗ):** gom trong trait (ERP) / 1 private method của service (HRM) để tránh lặp câu chữ. Dòng mã-tên lấy từ `products` (`code`,`name`) — ERP batch 1 query; HRM từ `quotation->productPrices` (có `code`,`name`,`erp_product_id`).

---

### Task 1 — ERP helper: thêm validate methods, giữ forNature byte-equivalent

**Files:** Modify `app/Support/ProductNatureDstcCoefficient.php`

- [x] **Step 1:** Rút phần nạp map trong `forNature` ra private `cachedMap(int $companyId): array` (giữ nguyên query `pluck('coefficient','product_nature_id')->map(float)->toArray()` + cache `$maps`). `forNature` gọi `cachedMap` rồi `array_key_exists($natureId,$map) ? (float)$map[$natureId] : 1.0` — kết quả không đổi.
- [x] **Step 2:** Thêm private `natureByProducts(array $ids): array` (batch leo cây `whereIn('p.id',$ids)->pluck('fg.product_nature_id','p.id')`) để tra nature theo lô.
- [x] **Step 3:** Thêm `validateProducts(?int $companyId, array $erpProductIds): array` — với mỗi id duy nhất: id rỗng → `no_nature`; leo cây không ra nature → `no_nature`; `cachedMap` không có key nature → `no_config`; coef `<= 0` → `zero_coef`; else bỏ qua. Trả `[erp_product_id => reason]` cho các id lỗi. `$companyId===null` → coi mọi id có nature-hoặc-không: không có company thì không tra được config ⇒ trả rỗng (không chặn khi thiếu company — company luôn có ở luồng thật; an toàn fail-open ở tầng helper, guard tầng service vẫn có company).
- [x] **Step 4:** Thêm `validateService(?int $companyId): ?string` — `cachedMap` không có key `0` → `no_config`; coef `<=0` → `zero_coef`; else `null`.
- [x] **Step 5 (test):** Viết `test_erp_dstc_validate.php` chạy qua tinker (bọc `DB::beginTransaction()/rollBack()`): seed 1 company + 4 products (đã khai>0, chưa phân loại, ra nature chưa khai, khai coef 0) → assert `validateProducts` trả đúng 3 reason; `validateService` 2 ca. (ERP không có PHPUnit tiện cho DB chung → tinker script trong scratchpad.)
- [x] **Step 6:** Chạy script, xác nhận PASS.

### Task 2 — ERP trait guard (goods + service) + message builder

**Files:** Create `app/Services/Sale/Firm/Contract/Concerns/ValidatesProductNatureDstc.php`

**Interfaces — Produces:**
- `validateProductNatureDstc(\Illuminate\Http\Request $request): array` → `[bool $isInvalid, ?string $message]`.
- `validateServiceNatureDstc(?int $companyId): array` → `[bool, ?string]`.

- [x] **Step 1:** Trait trong namespace `App\Services\Sale\Firm\Contract\Concerns`. `validateProductNatureDstc`:
  - gom `$productIds` từ `$request->tabs[*]['products'][*]['product_id']` + `$request->groups[*]['products'][*]['product_id']` (y hệt `validateDifferencePrice`; null-guard như bản gốc).
  - rỗng → `[false,null]`.
  - `$companyId = optional(optional(auth()->user())->info)->company_id;`
  - `$bad = ProductNatureDstcCoefficient::validateProducts($companyId,$productIds);` rỗng → `[false,null]`.
  - nạp `code,name,` + (tên nature nếu reason `no_config`) cho các id lỗi bằng 1 query `products` leo cây; dựng message theo design §Message; trả `[true,$message]`.
- [x] **Step 2:** `validateServiceNatureDstc(?int $companyId)`: `$r = ProductNatureDstcCoefficient::validateService($companyId);` null → `[false,null]`; else message dịch vụ theo reason → `[true,$msg]`.
- [x] **Step 3:** `FirmContractService` + `ZTFirmContractService` thêm `use ...\Concerns\ValidatesProductNatureDstc;` trong thân class (import use statement đầu file).
- [x] **Step 4 (test):** tinker: dựng `Request` giả có `tabs`/`groups` với 1 product lỗi → `app(FirmContractService::class)->validateProductNatureDstc($req)` trả `[true, msg chứa mã]`; product OK → `[false,null]`.
- [x] **Step 5:** Chạy, PASS.

### Task 3 — ERP wiring: firm contracts (10 site validateDifferencePrice)

**Files (Modify):** chèn ngay SAU block `validateDifferencePrice` hiện có (cùng pattern, trước transaction):
- `app/Http/Controllers/Sale/Firm/FirmContractController.php` (store ~148, update ~370)
- `app/Http/Controllers/Sale/Firm/PrincipleContractController.php` (~78)
- `app/Http/Controllers/Sale/Firm/ZTFirmContractAdditionAnnexesController.php` (~104)  ← phụ lục bổ sung
- `app/Http/Controllers/Sale/Firm/ZtecFirmContractController.php` (~127, ~313)
- `app/Http/Controllers/Sale/Firm/FirmContractAdditionAnnexesController.php` (~108)  ← phụ lục bổ sung
- `app/Http/Controllers/Sale/Firm/ZtPrincipleContractController.php` (~95, biến `$ZTFirmContractService`)
- `app/Http/Controllers/CRM/Sale/FirmContractController.php` (~96, ~219)

- [x] **Step 1:** Đọc mỗi file quanh dòng đã nêu, xác nhận biến service + vị trí trước `DB::beginTransaction()`.
- [x] **Step 2:** Chèn:
  ```php
  list($isInvalidDstc, $messageDstc) = $firmContractService->validateProductNatureDstc($request);
  if ($isInvalidDstc) return $this->responseErrors($messageDstc);
  ```
  (đổi tên biến service cho khớp từng controller; ZtPrincipleContract dùng `$ZTFirmContractService`).
- [x] **Step 3 (verify):** `grep -n validateProductNatureDstc` các file → đủ 10 chèn; đọc lại 2 file đại diện xác nhận nằm trước transaction.

### Task 4 — ERP wiring: principle orders + Ztec manufacture/design (store/update)

**Files:** đọc rồi chèn guard (service là `PrincipleOrderService`/`ZTPrincipleOrderService`, đều kế thừa `FirmContractService` → có method):
- `app/Http/Controllers/Sale/Firm/PrincipleOrderController.php`
- `app/Http/Controllers/Sale/Firm/ZtecPrincipleOrderController.php`
- `app/Http/Controllers/Sale/Firm/ZtecManufactureRequirementController.php`
- `app/Http/Controllers/Sale/Firm/ZtecDesignRequirementController.php`

- [x] **Step 1:** Mỗi controller: tìm action `store`/`update`, xác nhận request có `tabs`/`groups` (nếu shape khác → điều chỉnh traversal trong trait bằng cách thêm nhánh đọc, HOẶC bỏ guard nếu action không dựng dòng hàng có giá — ghi chú lý do).
- [x] **Step 2:** Chèn guard trước `DB::beginTransaction()` như Task 3 pattern.
- [x] **Step 3 (verify):** grep đủ; đọc 1 file xác nhận.

### Task 5 — ERP wiring: phụ lục thường (regular annex)

**Files:**
- `app/Http/Controllers/Sale/Firm/FirmContractAnnexesController.php`
- `app/Http/Controllers/Sale/Firm/ZtecFirmContractAnnexesController.php`

Ghi chú: `FirmContractAnnexService` KHÔNG tính lại DSTC → guard ở đây chủ yếu để honor HƯỚNG 2; nếu request annex không có `tabs`/`groups` product thì guard trả `[false,null]` (vô hại). 
- [x] **Step 1:** Đọc action store/update của 2 controller. Nếu có service `FirmContractService` sẵn (DI) thì gọi `validateProductNatureDstc`; nếu không có và request không mang dòng hàng giá → **bỏ qua** và ghi 1 dòng trong plan "annex thường không mang dòng DSTC, không guard".
- [x] **Step 2:** Chèn guard nếu áp dụng.
- [x] **Step 3:** Ghi kết luận (guard hay bỏ qua + lý do).

### Task 6 — ERP wiring: HĐ dịch vụ (WrServiceContract)

**Files:**
- `app/Http/Controllers/Customercare/WarrantyRepairContractsController.php` (store ~227, update ~440)
- `app/Http/Controllers/Customercare/WarrantyRepairContractAnnexController.php`
- `app/Http/Controllers/Customercare/WarrantyRepairContractAdditionAnnexController.php`
- (Service point: `app/Model/Customers/WrServiceContract.php` tiêu thụ DSTC product+service.)

- [x] **Step 1:** Đọc `WarrantyRepairContractsController@store/@update` quanh `DB::beginTransaction()` (~294). Xác định company_id + dòng sản phẩm (`product_repairs`/`syncProduct`) và dòng dịch vụ.
- [x] **Step 2:** Thêm guard trước transaction: (a) service nature 0: `list($bad,$msg)=app(FirmContractService::class)->validateServiceNatureDstc($companyId); if($bad) return $this->responseErrors($msg);` (b) nếu HĐ dịch vụ có gắn product thật thì validate các `product_id` đó qua `ProductNatureDstcCoefficient::validateProducts` (dựng message qua helper/trait). Chọn đúng nguồn product_id sau khi đọc request shape.
- [x] **Step 3:** 2 controller annex dịch vụ: đọc, chèn guard tương ứng (addition annex có tính lại giá → validate; annex thường nếu không → bỏ qua, ghi lý do).
- [x] **Step 4 (verify):** grep đủ; smoke qua tinker nếu khả thi.

### Task 7 — HRM helper: thêm validate methods

**Files:** Modify `Modules/MasterData/Support/ProductNatureDstcCoefficient.php`

- [x] **Step 1:** Thêm `validateProducts(?int $companyId, array $erpProductIds): array` → `[erp_product_id => reason]`. Dùng lại query batch `natureByProduct` (đã có trong `forProducts`); id rỗng/null → `no_nature`; nature null → `no_nature`; `company_product_natures` không có nature (phân biệt bằng `->pluck` rồi kiểm `contains key` — load `pluck('coefficient','product_nature_id')` và dùng `->has()`) → `no_config`; coef `<=0` → `zero_coef`.
- [x] **Step 2:** Thêm `validateService(?int $companyId): ?string` — tra `company_product_natures(company,0)`: không có dòng → `no_config`; coef `<=0` → `zero_coef`; else null. (Khác `forNature`: `forNature` trả 1.0 khi null; ở đây phải phân biệt null-row vs value → query `->first(['coefficient'])` rồi kiểm `=== null`.)
- [x] **Step 3 (test):** `Modules/MasterData/Tests/.../ProductNatureDstcValidateTest.php` (hoặc Feature test có sẵn trong module): 4 ca goods + 2 ca service. Dùng DB thật/transaction.
- [x] **Step 4:** Chạy `php artisan test --filter ProductNatureDstcValidate` → PASS.

### Task 8 — HRM guard: ContractService::createFromQuotation (goods)

**Files:** Modify `Modules/Assign/Services/ContractService.php`

- [x] **Step 1:** Đọc `createFromQuotation` (~410) + cách lấy product source (`quotation->productPrices`, context ~829). Xác định `erp_product_id` từng dòng (hàng tạm NULL).
- [x] **Step 2:** Ngay đầu hàm (trước `DB::transaction`): `$companyId = optional(optional(auth()->user())->info)->company_id;` lấy mảng `erp_product_id` từ `$quotation->productPrices`; `$bad = ProductNatureDstcCoefficient::validateProducts($companyId,$ids);` nếu không rỗng → dựng message (private `buildDstcMessage($quotation,$bad)` đọc `code/name` từ productPrices) → `throw ValidationException::withMessages(['products'=>[$message]]);`.
- [x] **Step 3 (test):** Feature test: quotation có 1 dòng chưa phân loại → `createFromQuotation` ném 422; quotation đủ điều kiện → tạo OK.
- [x] **Step 4:** Chạy test → PASS.

### Task 9 — HRM guard: WrServiceContractService::createFromQuotation (service)

**Files:** Modify `Modules/CustomerCare/Services/WrServiceContractService.php`

- [x] **Step 1:** Đọc `createFromQuotation` (~410) + `forService`/companyId (~1183-1191).
- [x] **Step 2:** Đầu hàm (trước transaction): `$r = ProductNatureDstcCoefficient::validateService($companyId);` nếu `!== null` → `throw ValidationException::withMessages(['service'=>[<message dịch vụ theo reason>]]);`. ~~Nếu HĐ dịch vụ có product thật → cũng `validateProducts` cho các dòng đó.~~ **SUPERSEDED (user chốt 2026-10-21):** T9 lúc đầu CHỈ validate nature 0 vì HRM `priceCoefficients()` định giá mọi dòng bằng `forService`. **ĐẢO LẠI bởi Task 11 (user chốt 2026-10-21 "sửa cho giống erp"):** pricing HRM đã căn về ERP (dòng hàng thật dùng `forProduct`), nên guard GIỜ validate CẢ nature 0 LẪN từng product thật như ERP `validateServiceContractDstc`. Guard ở CẢ `createFromQuotation` lẫn `update`. Private helper `assertServiceDstcConfigured(array $data)`.
- [x] **Step 3 (test):** Feature test: company chưa khai dòng Dịch vụ / coef 0 → 422; khai >0 → OK.
- [x] **Step 4:** Chạy test → PASS.

### Task 10 — Đối chiếu & tổng kết

- [x] **Step 1:** ERP: `grep -rn validateProductNatureDstc\|validateServiceNatureDstc app/Http/Controllers` → so với danh sách Task 3-6, không sót.
- [x] **Step 2:** Xác nhận `forNature/forProduct/forService` (2 repo) không đổi hành vi (diff chỉ refactor nội bộ).
- [x] **Step 3:** Cập nhật STATUS.md (mục feature) + memory topic `he-so-dstc-chuyen-enum-sang-product-nature.md` (ghi HƯỚNG 2 + kiến trúc guard).
- [x] **Step 4:** Báo cáo user: điểm đã guard, điểm bỏ qua (annex thường không DSTC) + lý do; chờ lệnh commit.

### Task 11 — Căn pricing HĐ dịch vụ HRM cho GIỐNG ERP + mở rộng guard (user chốt 2026-10-21 "sửa cho giống erp")

**Bối cảnh:** Port Phase-1 (commit 49318b57b) gộp hệ số về 1 cặp `priceCoefficients()` = `forService(nature 0)` + `price_type 99`, áp cho MỌI dòng. ERP thì tách theo loại dòng: dòng dịch vụ/công dùng `forService`+pt99, còn **vật tư/hàng hoá thật dùng `forProduct(product_id)`+pt1**. User yêu cầu HRM giống ERP.

**Files:** Modify `Modules/CustomerCare/Services/WrServiceContractService.php`

**Mapping (đã đối chiếu ERP `WrServiceContract.php`):**
- GIỮ `forService`+pt99: dòng sửa chữa chính (`syncProducts` main, 1222-1227), dịch vụ kèm (`choose_services`, ERP 1340-1345), gói bảo dưỡng (`extend.services`, ERP 1433-1438).
- ĐỔI sang `forProduct(product_id)`+pt1: vật tư sửa chữa (`choose_product_items`, ERP 1270-1277), vật tư gói (`extend.services.products`, ERP 1459-1465), hàng bán kèm (`merchandises`, ERP 1522-1530).

- [x] **Step 1:** Thay `priceCoefficients()` bằng `serviceCoefficients()` (forService+pt99) + `productCoefficients($erpProductId)` (forProduct+pt1) + helper `priceTypeCoefficient($companyId,$priceTypeId)` + `currentCompanyId()`.
- [x] **Step 2:** `syncProducts`: main line + `choose_services` dùng `$serviceCoef`; mỗi `choose_product_items` dùng `productCoefficients($item['product_id'])`.
- [x] **Step 3:** `syncExtendProducts`: `services` dùng `$serviceCoef`; mỗi `services.products` dùng `productCoefficients($item['product_id'])`.
- [x] **Step 4:** `syncMerchandises`: mỗi dòng dùng `productCoefficients($row['product_id'])`.
- [x] **Step 5:** Mở rộng guard `assertServiceDstcConfigured(array $data)`: gom product_id thật từ `product_repairs[*].choose_product_items[*]`, `merchandises[*]`, `extend_products[*].services[*].products[*]` → `validateProducts` + `validateService(nature 0)`; dựng message như ERP `validateServiceContractDstc` (header + bullet "Dòng Dịch vụ" + bullet từng hàng). Truyền `$data` ở 2 chỗ gọi.
- [x] **Step 6:** Cập nhật docblock (bỏ "forService cho tất cả"), STATUS.md, memory (ERP↔HRM ĐÃ căn, không còn "lệch cố ý").
- [x] **Step 7 (test):** Tinker (require worktree file trước): pricing per-line (service line = forService, product line = forProduct) + guard (nature 0 + product thật) → PASS.

## Self-Review

- Spec coverage: goods (T2-T5,T8) + service (T6,T9) + helper 3-reason (T1,T7) + HƯỚNG-2 annex (T3 addition, T5/T6 regular) ✔.
- Placeholder: controller lists có đường dẫn thật + dòng; traversal có nhánh "đọc xác nhận shape" cho principle/service (shape chưa chắc) ✔.
- Type consistency: `validateProducts` trả `[id=>reason]` (cả 2 repo); trait trả `[bool,?string]`; guard controller `[bool,message]` ✔.
- Review Focus: hàng tạm NULL (T7-S1,T8), coef 0 (T1-S3,T7-S1), sót controller (T10-S1) ✔.
