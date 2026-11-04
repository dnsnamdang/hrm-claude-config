# YCHG — Tùy chọn duyệt dòng "Duyệt không cần tính giá" (PTKD) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm lựa chọn duyệt dòng thứ 3 "Duyệt không cần tính giá" cho PTKD trên màn chi tiết YCHG (status "Chờ PTKD duyệt"); dòng chọn option-3 bỏ qua YCTG + Phiếu tính giá, tự ghi giá danh mục chuẩn và lên "Đang kinh doanh" ngay khi Duyệt phiếu.

**Architecture:** Thêm một giá trị trạng thái dòng mới `9` (`product_company_coefficients.status`) song song 6/7/8. Một endpoint per-line mới set `9`; toàn bộ phân loại (TH1 giá 0 / TH2 báo giá trúng thầu), ghi giá, promote `9→3` và đóng phiếu dồn vào transaction sẵn có của `PriceAskingRequestWriter::ptkdApprove`. FE thêm 1 nút footer trên trang quyết định từng sản phẩm; badge/nhãn trạng thái `9` do BE trả.

**Tech Stack:** hrm-api Laravel 8 / PHP 7.4 (`Modules/MasterData`); hrm-client Nuxt 2.14 / Vue 2 / Bootstrap-Vue (`components/product/form`, `components/sale/price-asking`). Test: `php artisan test <path>` trên DB `erp_hrm_check`; FE Playwright `http://127.0.0.1:3000`.

**Spec:** `HRM/.plans/ychg-duyet-khong-can-tinh-gia/design.md` (đọc kèm plan này — mọi quyết định nghiệp vụ nằm ở đó).

## Global Constraints

- **Dữ liệu nhạy cảm (giá vốn/giá nhập) gate server-side**, không chỉ ẩn FE. Hành vi GHI giá khi duyệt không cần gate own/quyền-giá-vốn (chỉ gate PTKD); gate M1 chỉ cho XEM giá ở picker.
- **Atomic**: mọi đổi trạng thái/ghi giá của một lần Duyệt phiếu phải nằm trọn trong transaction của `ptkdApprove`. Promote một phần rồi lỗi = cấm.
- **Quyền dùng chung** "PTKD duyệt yêu cầu hỏi giá" + middleware `dueConfig:Duyệt hàng tạm`. KHÔNG thêm quyền, KHÔNG seed.
- **Badge màu + text do BE quyết** (`company_status_text` / `company_status_color`); FE chỉ hiển thị. Số en-US. Dùng đúng 9 mã màu chuẩn HRM.
- **Không đổi luồng** dòng Đồng ý (1/7) và Từ chối (8). Không đụng màn XNK/Kế toán. Không làm radio inline.
- TH1 chỉ hợp lệ khi giá nhập = 0 **VÀ** giá bán = 0 **tường minh** (null/thiếu giá = KHÔNG đủ điều kiện).
- TH2 quy đổi VND bằng tỷ giá **hiện tại** (`QuotationService::resolveCurrentExchangeRate`), KHÔNG dùng `quotations.exchange_rate` đóng băng; đồng giá cả 6 loại giá bán = `quoted_price × rate` (ghi đè auto-compute TMĐT loại 6).

## Review Focus

- **Reader nào đọc `product_company_coefficients.status` mà không biết `9`** (cột "Trạng thái HH công ty quản lý", list sản phẩm, báo cáo, filter, `excludeTempOnly`) → `9` rơi vào nhánh "không xác định" / badge trống. Pinned trong Task 1.
- **Hàng tạm MỚI chưa từng nhập giá (cost null / không có dòng giá) chọn option-3** → phải bị chặn ở Duyệt phiếu (không được coi là TH1 giá 0). Pinned trong Task 2 + Task 4.
- **Báo giá trúng thầu ngoại tệ** → quên × tỷ giá ⇒ ghi giá sai đơn vị. Pinned trong Task 2.
- **Giả định hạ nguồn "status 3 phải kèm một Phiếu tính giá"** (đồng bộ ERP / lập HĐ / join `price_calculate*`) → hàng option-3 lên `3` mà không có Phiếu tính giá có thể vỡ. Pinned trong Task 4 (bước audit hạ nguồn).
- **Bộ Cha–Con lệch luồng** (Cha `9` promote ngay, Con Đồng ý vẫn đi XNK) → định tuyến theo trạng thái từng dòng, không ràng buộc nhau. Pinned trong Task 4.

---

## File Structure

**hrm-api (`Modules/MasterData/`)**
- `Entities/Product/ProductCompany.php` — hằng `9` + maps + membership (Task 1).
- `Services/PriceCalculation/TempNoPriceResolver.php` *(mới)* — phân loại TH1/TH2 + resolve giá (Task 2).
- `Services/PriceCalculation/PriceAskingRequestWriter.php` — `tempApproveNoPrice()` + gate nhận `9` (Task 3); integration trong `ptkdApprove()` (Task 4).
- `Services/PriceCalculation/PriceAskingRequestService.php` — `tempForm` cờ `can_approve_no_price` (Task 3).
- `Http/Controllers/V1/PriceCalculation/PriceAskingRequestController.php` + `Routes/api.php` — route `temp-products/{product}/approve-no-price` (Task 3).
- `Tests/Feature/PriceAskingNoPriceApproveTest.php` *(mới)* — mirror `PriceAskingTempProductTest.php` (Task 2/3/4).

**hrm-client (`components/`)**
- `product/form/ProductForm.vue` — nút footer thứ 3 (Task 5).
- `sale/price-asking/PriceAskingRequestForm.vue` — nhận diện trạng thái `9` Cha + Con (Task 6).

---

## Task 1: Trạng thái dòng `9` + maps + audit reader

**Files:**
- Modify: `Modules/MasterData/Entities/Product/ProductCompany.php:23-33,39-59`
- Test: `Modules/MasterData/Tests/Feature/ProductCompanyFoundationTest.php` (mirror file sẵn có; nếu khác tên thì thêm test vào file đó)

**Interfaces:**
- Produces: hằng `ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE = 9`; `ProductCompany::isTemp(9) === true`; `STATUS_TEXT[9]`, `STATUS_COLOR[9]` tồn tại.

- [ ] **Step 1: Viết test**

```php
public function test_no_price_status_is_temp_and_has_badge(): void
{
    $this->assertSame(9, ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE);
    $this->assertTrue(ProductCompany::isTemp(ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE));
    $this->assertArrayHasKey(9, ProductCompany::STATUS_TEXT);
    $this->assertArrayHasKey(9, ProductCompany::STATUS_COLOR);
    $this->assertNotSame('', trim((string) ProductCompany::STATUS_TEXT[9]));
}
```

- [ ] **Step 2: Chạy test, xác nhận FAIL** (`Undefined constant` / key thiếu).

- [ ] **Step 3: Thêm hằng + maps**
  - `const STATUS_TEMP_APPROVED_NO_PRICE = 9;` (sau dòng 30).
  - Thêm `9` vào `TEMP_STATUSES` (dòng 33) → `[6,7,8,9]`. (Lý do: dòng `9` trước khi Duyệt phiếu vẫn là hàng tạm chưa kinh doanh — phải ẩn khỏi catalog/picker đúng như 6/7/8; `isTemp(9)=true` cho phép mở lại form duyệt và hiện controls hàng tạm. Sau promote → `3` tự hết ẩn.)
  - `STATUS_TEXT[9] = 'Duyệt không cần tính giá'` (chốt chuỗi; FE hiển thị nguyên văn).
  - `STATUS_COLOR[9] = '#7C3AED'` (nhóm "chốt" — cùng nhóm màu `STATUS_TEMP_APPROVED`, thuộc 9 mã chuẩn; KHÔNG chế mã mới).

- [ ] **Step 4: Audit mọi reader của `product_company_coefficients.status`** — bước bắt buộc (Review Focus). Grep `product_company_coefficients` + `company_status` + `STATUS_TEXT` + `STATUS_COLOR` + `TEMP_STATUSES` + `PRICING_FLOW_STATUSES` + `isTemp` + `excludeTempOnly` trong `Modules/`. Với mỗi reader liệt kê ra: xác nhận `9` được map đúng (badge có text/màu) và không rơi vào nhánh "không xác định". Đặc biệt kiểm màn "Trạng thái HH công ty quản lý" (memory `hrm-kho-du-lieu-cot-trang-thai-cong-ty-quan-ly`) + list sản phẩm + filter. Nếu một reader cần loại/giữ `9` riêng (vd filter "Đang kinh doanh" không được lẫn `9`) thì sửa tại reader đó. Nếu `9` đã bị dùng ở đâu khác → đổi sang giá trị trống kế tiếp và cập nhật test. Ghi kết quả audit (danh sách reader đã kiểm) vào report.

- [ ] **Step 5: Chạy test, xác nhận PASS.** `php artisan test Modules/MasterData/Tests/Feature/ProductCompanyFoundationTest.php`

- [ ] **Step 6: Commit** — `feat(ychg): add product status 9 (approved-no-price) + badge maps`

---

## Task 2: `TempNoPriceResolver` — phân loại & resolve giá

**Files:**
- Create: `Modules/MasterData/Services/PriceCalculation/TempNoPriceResolver.php`
- Test: `Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php` (tạo file; mirror scaffolding `PriceAskingTempProductTest.php`: `DatabaseTransactions`, trait `ActsAsProductUser`, fixtures hàng × công ty + `product_company_coefficients`)

**Interfaces:**
- Consumes: `QuotationService::resolveCurrentExchangeRate` (`Modules/Assign/Services/QuotationService.php:1428`) trả `float` tỷ giá hiện tại; `Quotation::STATUS_TRUNG_THAU = 7`.
- Produces:
  ```php
  // null = KHÔNG đủ điều kiện duyệt không cần tính giá
  // ['case' => 'won_bid'|'zero', 'cost' => float, 'sale' => float, 'unit_id' => int]
  public function resolve(int $productId, int $companyId): ?array
  ```
  `cost` = giá nhập (đã quy đổi VND), `sale` = giá bán (đã quy đổi VND), `unit_id` = ĐVT gốc của giá (ĐVT dòng báo giá cho TH2; ĐVT gốc hàng cho TH1).

- [ ] **Step 1: Viết test** (4 ca, mỗi ca 1 phương thức):

```php
// TH2 VND: quotation status=7, estimated_price=100, quoted_price=150, currency VND ⇒ cost=100, sale=150
public function test_resolve_won_bid_vnd(): void { /* assert case=won_bid, cost=100.0, sale=150.0 */ }

// TH2 ngoại tệ: currency rate hiện tại=25000, estimated=2, quoted=3 ⇒ cost=50000, sale=75000
public function test_resolve_won_bid_foreign_currency_multiplies_rate(): void { /* ... */ }

// TH2 nhiều báo giá trúng thầu ⇒ lấy quotations.id lớn nhất
public function test_resolve_won_bid_picks_latest_quotation(): void { /* ... */ }

// TH1: cost_price=0 explicit + retail price row=0 explicit, không có báo giá trúng thầu ⇒ case=zero, cost=0, sale=0
public function test_resolve_zero_when_explicit_zero_prices(): void { /* ... */ }

// Ineligible: cost null / không có dòng giá / không có báo giá trúng thầu ⇒ null
public function test_resolve_null_when_price_missing(): void { /* assertNull */ }

// Ineligible: có báo giá nhưng status != 7 và giá không phải 0 tường minh ⇒ null
public function test_resolve_null_when_no_won_bid_and_nonzero(): void { /* assertNull */ }
```

- [ ] **Step 2: Chạy test, xác nhận FAIL** (class không tồn tại).

- [ ] **Step 3: Implement `resolve()`**
  - **TH2 trước:** query `quotation_product_prices qpp` join `quotations q on q.id = qpp.quotation_id` where `qpp.erp_product_id = $productId` and `q.status = Quotation::STATUS_TRUNG_THAU` and `qpp.estimated_price IS NOT NULL` and `qpp.quoted_price IS NOT NULL`, `order by q.id desc limit 1`. Nếu có: `rate = resolveCurrentExchangeRate($quotation)` (VND/none ⇒ 1.0); `cost = estimated_price * rate`, `sale = quoted_price * rate`, `unit_id` = ĐVT dòng báo giá (cột ĐVT trên `qpp` — builder xác nhận tên cột; fallback ĐVT gốc hàng). `case='won_bid'`.
  - **TH1:** đọc giá hiện tại của hàng tại công ty — pin điểm đọc: `cost_price` của `product_company_units` (ĐVT gốc) **và** giá hiệu lực loại 1 (Bán lẻ) trên `product_unit_prices`. Chỉ hợp lệ khi **cả hai = 0 tường minh** (giá trị `0`, KHÔNG null/thiếu dòng). `case='zero'`, `cost=0, sale=0`, `unit_id` = ĐVT gốc.
  - Ngược lại trả `null`.
  - ⚠️ Builder pin chính xác tên cột ĐVT trên `quotation_product_prices` và điểm đọc giá TH1 (design open items #2); ghi rõ trong report.

- [ ] **Step 4: Chạy test, xác nhận PASS.** `php artisan test Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php`

- [ ] **Step 5: Commit** — `feat(ychg): TempNoPriceResolver classifies TH1/TH2 + VND conversion`

---

## Task 3: Endpoint set trạng thái `9` + gate nhận `9` + cờ FE

**Files:**
- Modify: `Modules/MasterData/Services/PriceCalculation/PriceAskingRequestWriter.php:498-526,528-538` (gate + method mới)
- Modify: `Modules/MasterData/Http/Controllers/V1/PriceCalculation/PriceAskingRequestController.php:156-168`
- Modify: `Modules/MasterData/Routes/api.php:416-423`
- Modify: `Modules/MasterData/Services/PriceCalculation/PriceAskingRequestService.php:553-562` (tempForm meta)
- Test: `PriceAskingNoPriceApproveTest.php` (bổ sung)

**Interfaces:**
- Consumes: `assertTempGate(int $id, int $productId, array $statuses, bool $lock)`, `setTempStatus(...)`, `ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE` (Task 1).
- Produces:
  ```php
  // PriceAskingRequestWriter
  public function tempApproveNoPrice(int $id, int $productId): int   // trả về 9
  ```
  Route: `POST /api/v1/master-data/price-asking-requests/{id}/temp-products/{product}/approve-no-price`.
  `tempForm` meta thêm `can_approve_no_price` (bool, = giá trị `$open` hiện có).

- [ ] **Step 1: Viết test**

```php
// Set 9 qua endpoint
public function test_approve_no_price_sets_status_9(): void {
    // actAs ptkd; POST .../temp-products/{pid}/approve-no-price ⇒ 200, company_status=9; pcc.status=9
}
// Reopen: dòng đang 9 đổi lại sang Đồng ý (7)
public function test_can_reopen_from_9_to_approve(): void {
    // pcc=9 ⇒ POST approve ⇒ 200, status=7
}
// Gate: không phải PTKD ⇒ 403; dòng không thuộc phiếu ⇒ 404; phiếu không ở Chờ PTKD ⇒ 409
public function test_approve_no_price_gate(): void { /* 403/404/409 */ }
// tempForm trả can_approve_no_price=true khi phiếu Chờ PTKD + dòng tạm
public function test_temp_form_exposes_can_approve_no_price(): void { /* ... */ }
```

- [ ] **Step 2: Chạy test, xác nhận FAIL.**

- [ ] **Step 3: Implement**
  - `assertTempGate`: nơi gọi với `ProductCompany::TEMP_STATUSES` nay tự gồm `9` (Task 1) → reopen từ `9` hợp lệ không cần sửa thêm; xác nhận `tempApprove`/`tempReject`/`tempSave` vẫn nhận `9` làm trạng thái hiện tại (đều truyền `TEMP_STATUSES`).
  - `tempApproveNoPrice($id,$productId)`: `DB::transaction` → `[$request] = assertTempGate($id,$productId, ProductCompany::TEMP_STATUSES, true)` → `setTempStatus($request,$productId, ProductCompany::STATUS_TEMP_APPROVED_NO_PRICE, 'approved', 'Duyệt không cần tính giá')` → return `9`. **KHÔNG validate/ghi giá ở đây** (dồn về `ptkdApprove`, design §3.1).
  - Controller `tempApproveNoPrice($id,$product)`: gọi writer, trả `['product_id'=>..., 'company_status'=>9]`, message "Đã ghi nhận duyệt không cần tính giá".
  - Route: thêm trong group `dueConfig:Duyệt hàng tạm` (cạnh `approve`/`reject`): `POST .../temp-products/{product}/approve-no-price`.
  - `tempForm`: thêm `'can_approve_no_price' => $open` vào mảng trả về (dòng ~561).

- [ ] **Step 4: Chạy test, xác nhận PASS.**

- [ ] **Step 5: Commit** — `feat(ychg): per-line approve-no-price endpoint sets status 9 + reopen`

---

## Task 4: Integration trong `ptkdApprove` — validate + ghi giá + promote + đóng phiếu

**Files:**
- Modify: `Modules/MasterData/Services/PriceCalculation/PriceAskingRequestWriter.php:591-665`
- Test: `PriceAskingNoPriceApproveTest.php` (bổ sung — ca end-to-end qua `POST {id}/approve`)

**Interfaces:**
- Consumes: `TempNoPriceResolver::resolve` (Task 2); `ProductPriceWriter::apply(int $productId,int $productUnitId,int $companyId,array $resolved,float $cost,?string $reason,int $by)` + `resolvePrices(array $prices,int $companyId)`; `ProductPriceSetWriter::ensureProductSet(int $productId,int $companyId,int $by)`; `ProductHistoryService::trackStatus`; `moveProducts`, `refreshHead`, `markGroupClosed`, `log` (private, cùng class).
- Produces: `ptkdApprove` xử lý trọn dòng `9` trong transaction; phiếu ra `STATUS_PRICED`(4) hoặc `STATUS_ASKING`(10) tùy còn dòng thường.

- [ ] **Step 1: Viết test** (end-to-end: dựng phiếu Chờ PTKD, set trạng thái dòng qua endpoint, rồi `POST {id}/approve`):

```php
// TH1 promote: dòng giá 0 ⇒ 9 ⇒ Duyệt phiếu ⇒ pcc.status=3, cost_price=0, 6 loại giá bán=0
public function test_ptkd_approve_promotes_th1_zero(): void { /* ... */ }
// TH2 VND promote + ghi giá: cost_price=estimated, retail=quoted, cả 6 loại=quoted (TMĐT KHÔNG ×1.3)
public function test_ptkd_approve_promotes_th2_writes_all_six_prices_flat(): void { /* ... */ }
// TH2 ngoại tệ: giá ghi = ×rate hiện tại
public function test_ptkd_approve_th2_foreign_currency(): void { /* ... */ }
// Chặn: dòng 9 không đủ điều kiện ⇒ 422 'temp_products', message nêu mã hàng
public function test_ptkd_approve_blocks_ineligible_no_price_line(): void { /* assert 422 + code trong message */ }
// Cha–Con lệch: Cha=9 promote→3; Con=Đồng ý(7)→2 vẫn đi XNK
public function test_parent_no_price_child_normal_route_independently(): void { /* ... */ }
// Phiếu toàn option-3 (+ option-2) ⇒ phiếu đóng STATUS_PRICED(4)
public function test_request_all_no_price_closes_priced(): void { /* status=4 */ }
// Phiếu lẫn dòng thường (option-1) ⇒ phiếu STATUS_ASKING(10); dòng 9 vẫn promote ngay
public function test_request_mixed_goes_asking_but_promotes_no_price_now(): void { /* status=10 + dòng 9 =3 */ }
// Atomic: resolver lỗi giữa chừng ⇒ không dòng nào promote (rollback)
public function test_promote_is_atomic_on_failure(): void { /* ... */ }
```

- [ ] **Step 2: Chạy test, xác nhận FAIL.**

- [ ] **Step 3: Implement** — bên trong transaction của `ptkdApprove`, sau khi gom `$statuses` (dòng 609-611), trước phần XNK/moveProducts:
  - Gom tập id dòng (Cha + Con) đang ở `9` từ `$statuses`.
  - **Validate**: với mỗi id `9`, `resolve(id, companyId)`. Dòng trả `null` → gom vào `$invalid` (kèm mã hàng). Nếu `$invalid` → `throw ValidationException::withMessages(['temp_products' => ["<mã1>, <mã2>: chưa đủ điều kiện duyệt không cần tính giá"]])`.
  - **Ghi giá + promote** (mỗi dòng `9` hợp lệ): dựng mảng 6 loại giá bán phẳng = `sale` (ghi đè auto-compute TMĐT loại 6 — xem design open item #3: truyền đủ 6 giá với `is_manual_price_online=true` cho loại 6, hoặc ghi thẳng `writePrices`; builder chốt để "đồng giá" đúng). Áp giá cho ĐVT gốc (`unit_id` từ resolver) qua `ProductPriceWriter::apply(...)`; các ĐVT phụ của hàng dẫn giá theo hệ số đúng cơ chế bộ giá chuẩn (design open item #8 — pin cơ chế `ensureProductSet`/standard set). Sau ghi giá: `trackStatus(companyId,[id], fn() => update pcc 9→3, 'approved', 'Duyệt không cần tính giá — YCHG '.$request->code)` + `ensureProductSet(id, companyId, me)`. Thêm log `price_asking_request_approve_histories` type mới `temp_approve_no_price`.
  - **Phân loại nhóm**: nhóm mà mọi dòng (không tính dòng `8`) đều đã promote (`9→3`) và không còn dòng cần XNK → đưa vào nhánh đóng; chốt trạng thái đóng = `STATUS_PRICED`(4) (đã có giá) và tái dùng `refreshHead` nếu khớp (design open item #4). Nhóm còn dòng thường → vẫn `STATUS_WAITING_XNK` như cũ.
  - `moveProducts(7→2)` giữ nguyên cho dòng Đồng ý; dòng `9` KHÔNG đi qua `moveProducts` (đã promote thẳng 3).
  - **Phiếu**: nếu sau xử lý không còn nhóm `STATUS_WAITING_XNK` nào (mọi dòng `8` hoặc đã `3`) → `refreshHead` đưa phiếu về `4`; nếu còn nhóm thường → giữ `STATUS_ASKING`(10) như hiện tại.

- [ ] **Step 4: Audit hạ nguồn "status 3 phải kèm Phiếu tính giá"** (Review Focus) — grep `price_calculate` join / đồng bộ ERP / lập HĐ xem có coi hàng status `3` bắt buộc kèm một `price_calculate*` không. Nếu có, bổ sung guard hoặc chọn trạng thái kết thúc phù hợp (khoá nghiệp vụ là hàng `3`, không phải sự tồn tại Phiếu tính giá). Ghi kết quả vào report.

- [ ] **Step 5: Chạy test, xác nhận PASS.** `php artisan test Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php`

- [ ] **Step 6: Chạy lại test cũ** `php artisan test Modules/MasterData/Tests/Feature/PriceAskingTempProductTest.php` — xác nhận luồng Đồng ý/Từ chối không vỡ.

- [ ] **Step 7: Commit** — `feat(ychg): ptkdApprove validates+writes price+promotes no-price lines (3), closes request`

---

## Task 5: FE — nút footer "Duyệt không cần tính giá" (ProductForm.vue)

**Files:**
- Modify: `hrm-client/components/product/form/ProductForm.vue:72-105,365-374,427-469`
- Kiểm bằng Playwright (`http://127.0.0.1:3000`)

**Interfaces:**
- Consumes: meta BE `tempMeta.can_approve_no_price` (Task 3); endpoint `POST {ASKING}/{requestId}/temp-products/{productId}/approve-no-price`.

- [ ] **Step 1: Thêm nút** — trong footer `mode === 'temp-approve'`, cạnh "Đồng ý"/"Không duyệt": `V2BaseButton primary size="sm"` chữ **"Duyệt không cần tính giá"**, `v-if="tempMeta.can_approve_no_price && tempStatus !== 9"`, `:interactable="ready && !saving"`. Icon + lề theo button-convention (`mr-2 mb-2`). Có confirm nhẹ như "Đồng ý" (`$confirm`): "Duyệt không cần tính giá cho hàng {code}? Hàng sẽ lên 'Đang kinh doanh' khi duyệt phiếu {ychgCode}, bỏ qua hỏi giá và tính giá." Thêm icon Info tooltip giải thích TH1/TH2 (dùng `ri-information-line` + `b-popover custom-class="info-popover"` như các nút kế bên).

- [ ] **Step 2: Thêm handler** — `tempApproveNoPrice()`: sau confirm, `apiPostMethod(tempUrl('/approve-no-price'))` → thành công `markFormSaved()` + điều hướng về chi tiết phiếu (giống luồng `tempSubmit('approve')`). Map `can_approve_no_price` vào `tempMeta` trong `loadTempForm` (nơi destructure meta, dòng ~371-374).

- [ ] **Step 3: Kiểm Playwright** — mở trang quyết định 1 hàng tạm (status 6), xác nhận 3 nút hiện (Đồng ý / Duyệt không cần tính giá / Không duyệt); bấm nút mới → confirm → quay về phiếu, dòng thành "Sửa" + badge "Duyệt không cần tính giá". Chụp màn hình, xem ảnh.

- [ ] **Step 4: Tự kiểm V2Base** — `grep -rn '<input \|<button \|class="btn ' components/product/form/ProductForm.vue | grep -v V2Base` cho phần thêm mới phải rỗng.

- [ ] **Step 5: Commit** — `feat(ychg): third footer action 'Duyệt không cần tính giá' on temp-approve form`

---

## Task 6: FE — nhận diện trạng thái `9` trên phiếu (Cha + Con)

**Files:**
- Modify: `hrm-client/components/sale/price-asking/PriceAskingRequestForm.vue:254-269,309-325,754-758`
- Kiểm bằng Playwright

**Interfaces:**
- Consumes: `row.company_status === 9`, `row.company_status_text/color` từ BE (Task 1/3).

- [ ] **Step 1: Nhãn nút** — nhánh `v-else` (`Number(row.company_status) !== 6`) đã hiện "Sửa" cho 7/8, nên `9` tự rơi vào "Sửa" — xác nhận không cần đổi logic nút. Badge dòng dùng `company_status_text/color` BE → tự hiển thị "Duyệt không cần tính giá". Làm y hệt cho dòng Con (`child.company_status`).

- [ ] **Step 2: Tooltip** — cập nhật text tooltip nút "Sửa" (dòng ~267, ~323) để câu "Mở lại form để đổi quyết định Đồng ý ↔ Không duyệt" cũng nhắc được lựa chọn thứ 3 (vd "…Đồng ý ↔ Duyệt không cần tính giá ↔ Không duyệt"). Không tô đỏ, chữ xám.

- [ ] **Step 3: `openTempApprove`/readonly guard** — kiểm dòng ~754-758: hàm điều hướng dùng chung, `9` không cần nhánh riêng; xác nhận dòng `9` vẫn mở lại được form (readonly guard chỉ chặn status 8 ở chế độ readonly — xác nhận `9` không bị chặn nhầm).

- [ ] **Step 4: Kiểm Playwright** — phiếu có dòng status `9`: badge đúng chữ/màu; nút "Sửa" mở lại trang quyết định; **nút Duyệt phiếu sáng** khi 100% dòng (Cha + Con) đã rời `6` (gồm dòng `9`). Chụp màn hình, xem ảnh.

- [ ] **Step 5: Commit** — `feat(ychg): recognize status 9 (approved-no-price) on request detail for parent + children`

---

## Checkpoint — hoàn tất

- [ ] Chạy toàn bộ test BE liên quan: `php artisan test Modules/MasterData/Tests/Feature/PriceAskingNoPriceApproveTest.php Modules/MasterData/Tests/Feature/PriceAskingTempProductTest.php Modules/MasterData/Tests/Feature/ProductCompanyFoundationTest.php` — tất cả xanh.
- [ ] Playwright xác nhận luồng đầu-cuối: PTKD chọn option-3 cho Cha + Con → Duyệt phiếu → hàng lên "Đang kinh doanh" với giá đúng (TH1 = 0; TH2 = giá báo giá trúng thầu đã quy đổi VND).
- [ ] Final whole-branch review (model mạnh nhất) tập trung Review Focus: audit reader status `9`, chặn hàng tạm giá-null, ngoại tệ, giả định hạ nguồn Phiếu tính giá, atomic transaction.
