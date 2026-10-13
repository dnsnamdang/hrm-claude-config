# Task P2-1: 6 Entity BorrowSell* — Report

## Status: DONE

Commit: `c562527e0f348a38d8c24bb0033e82b40ea5c9f1`
Branch: `gop_db` (repo `hrm-api`)

## Step 1 — Verify tên bảng + cột (DB `erp_hrm_check`)

`SHOW TABLES LIKE 'borrow_sell%';` xác nhận cả 13 bảng `borrow_sell*` đều dùng tên GỐC (không có bản `hrm_borrow_sell*`), tức không có xung đột tên cần khai `$table` khác mặc định Laravel — nhưng vẫn khai `$table` tường minh trên mọi entity (giống pattern Phase 1) để tránh phụ thuộc convention đặt tên.

6 bảng của task này + cột đã verify:

- `borrow_sells`: id, status, type, code(UNI), **borrow_sell_request_id**, contractable_id, contractable_type, firm_contract_tab_id, project_tab_id, created_by, updated_by, note, timestamps, export_price, vat_percent, vat_cost_allocated, sum_amount_allocated(_after_vat), sum_amount_after_extra(_vat/_after_vat), bear_the_shipping. Không có cột `company_id`/`department_id` (khác `borrow_sell_requests` Phase 1).
- `borrow_sell_products`: id, **parent_id** (→ borrow_sells.id), objectable_id/type, product_id, product_name, unit_id, unit_name, brand_id, brand_name, model_id, model_name, code, price, extra_price, contract_qty, qty, contract_promotion_id, unit_coefficient, export_price, allocated_price, rebate_price, vat_percent, timestamps.
- `borrow_sell_product_details`: id, **parent_id** (→ borrow_sell_products.id), product_export_request_id, product_export_request_detail_id, product_id, unit_id, qty, timestamps.
- `borrow_sell_tabs`: id, **parent_id** (→ borrow_sells.id), firm_contract_id, firm_contract_tab_id, name, timestamps.
- `borrow_sell_tab_products`: id, **parent_id** (→ borrow_sell_tabs.id), borrow_sell_id, firm_contract_id, firm_contract_tab_id, product_id, unit_id, contract_qty, qty, exported_qty, timestamps.
- `borrow_sell_tab_product_details`: id, **parent_id** (→ borrow_sell_tab_products.id), borrow_sell_id, firm_contract_tab_id, product_export_request_id, product_export_request_detail_id, product_id, unit_id, qty, timestamps.

FK pattern giống hệt nhóm Phase 1 `BorrowSellRequest*`: quan hệ cha-con dùng cột `parent_id` (không dùng tên FK tường minh kiểu `borrow_sell_id`) ở TẤT CẢ 5 quan hệ hasMany trong scope task này. Cột `borrow_sell_id` có tồn tại trên `borrow_sell_tab_products`/`borrow_sell_tab_product_details` nhưng là cột snapshot phụ (giống `borrow_sell_request_id` snapshot trên `borrow_sell_request_tab_product*` bản Phase 1) — KHÔNG dùng làm FK cho relation `hasMany` (đã bám đúng interface brief yêu cầu: `products()`/`tabs()`/`details()` dùng `parent_id`).

## Quyết định `$table`

Không có bảng nào bị đổi tên `hrm_*` (chỉ ERP), nên `$table` khai đúng tên gốc:
`borrow_sells`, `borrow_sell_products`, `borrow_sell_product_details`, `borrow_sell_tabs`, `borrow_sell_tab_products`, `borrow_sell_tab_product_details`.

## Step 4 — 6 entity đã tạo

`Modules/Finance/Entities/BorrowSell/`:
- `BorrowSell.php` — namespace `Modules\Finance\Entities\BorrowSell`, `use ChecksEmployeePermission`, `$guarded=[]`.
  - const: `PREFIX='PXBHM'`, `STATUS_DEFAULT=1`, `PERMISSION_KE_TOAN_KHO='Kế toán kho'`, `CONTRACT_FIRM`, `CONTRACT_WR_SERVICE` (verbatim theo interface brief).
  - `generateCode(): string` — **static thuần** (không dùng `$this`), khác cách Phase 1 `BorrowSellRequest::generateCode()` (instance method, set `$this->code` rồi `save()`). Lý do: interface brief chỉ định chữ ký `BorrowSell::generateCode(): string` và test gọi `BorrowSell::generateCode()` KHÔNG qua instance (`new BorrowSell()`) — nếu viết instance method dùng `$this->id` thì gọi static sẽ Fatal Error "Using $this when not in object context". Implementation: `self::PREFIX . '-' . str_pad((string)(self::max('id') ?? 0) + 1, 5, '0', STR_PAD_LEFT)`. Giữ đúng prefix `PXBHM-` + pad 5 số như ERP (`generateCode(5,id)`), chỉ khác cơ chế lấy số (max(id)+1 thay vì `$this->id` sau khi đã insert) vì method không còn ràng buộc vào 1 record cụ thể. **Ghi chú cho task sau**: nếu cần code gắn với ĐÚNG id bản ghi vừa tạo (tránh race condition giữa lúc tính code và lúc insert), cân nhắc bổ sung 1 method khác (vd `assignCode()` instance) thay vì đổi chữ ký `generateCode()` này (interface đã "chốt" cho task khác dùng).
  - `canView(): bool` — instance method, port ERP `canView()`: `(currentEmployeeHasPermission('Kế toán kho') && status != 3) || created_by == auth()->id()`. Dùng trait `ChecksEmployeePermission::currentEmployeeHasPermission()` (protected static) — bám đúng cách Phase 1 `BorrowSellRequest::canView()` xử lý quyền/auth id, KHÔNG dùng `Auth::user()->can()` (ERP, guard `web`) vì lý do đã ghi trong docblock trait (guard mismatch + model_type mismatch, xem `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php`).
  - Relations: `products()` hasMany `BorrowSellProduct` (`parent_id`), `tabs()` hasMany `BorrowSellTab` (`parent_id`), `borrowSellRequest()` belongsTo `Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest` (`borrow_sell_request_id`).
- `BorrowSellProduct.php` — `details()` hasMany `BorrowSellProductDetail` (`parent_id`).
- `BorrowSellProductDetail.php` — không quan hệ.
- `BorrowSellTab.php` — `products()` hasMany `BorrowSellTabProduct` (`parent_id`).
- `BorrowSellTabProduct.php` — `details()` hasMany `BorrowSellTabProductDetail` (`parent_id`).
- `BorrowSellTabProductDetail.php` — không quan hệ.

Tất cả extend `Illuminate\Database\Eloquent\Model`, `public $timestamps = true`, `protected $guarded = []` (đúng yêu cầu brief; Phase 1 dùng `guarded=['id']`, brief task này chỉ định rõ `$guarded=[]` nên dùng đúng verbatim).

## Step 3 & 5 — Kết quả test

Chạy bằng `php artisan test Modules/Finance/Tests/Unit/BorrowSellEntityTest.php` (KHÔNG dùng `--filter=` vì `phpunit.xml` chỉ scan `./tests/Unit` + `./tests/Feature`, không scan `Modules/*/Tests` — filter theo class name không match được suite nào nên "No tests executed"; chạy trực tiếp theo path thì PHPUnit/Artisan vẫn nạp và chạy đúng file).

- Step 3 (trước khi viết entity): **FAIL** — `Class 'Modules\Finance\Entities\BorrowSell\BorrowSell' not found` (2 test lỗi, đúng kỳ vọng TDD).
- Step 5 (sau khi viết entity): **PASS** — 2/2 test pass (`generate code has pxbhm prefix`, `products relation defined`), 0.90s–1.17s.

Không gặp lỗi DB test/bootstrap (Step verify + test đều chạy được trên DB thật `erp_hrm_check` qua `.env` hiện tại, không dùng `mysql2`).

## Commit

Chỉ 7 file trong phạm vi task được add + commit:
```
Modules/Finance/Entities/BorrowSell/BorrowSell.php
Modules/Finance/Entities/BorrowSell/BorrowSellProduct.php
Modules/Finance/Entities/BorrowSell/BorrowSellProductDetail.php
Modules/Finance/Entities/BorrowSell/BorrowSellTab.php
Modules/Finance/Entities/BorrowSell/BorrowSellTabProduct.php
Modules/Finance/Entities/BorrowSell/BorrowSellTabProductDetail.php
Modules/Finance/Tests/Unit/BorrowSellEntityTest.php
```
Commit hash: `c562527e0f348a38d8c24bb0033e82b40ea5c9f1`.

**Lưu ý xử lý sự cố nhỏ khi commit**: `git status` trước khi bắt đầu đã có sẵn nhiều file Phase 1 đang pending (staged + unstaged, kể cả 1 file `D` — xoá `Modules/Finance/Entities/ProductImportRequest/BorrowSellRequest.php`, không liên quan task này). Lần `git add` đầu chỉ add đúng 7 file của task nhưng `git commit` (không path) đã gộp CẢ file `D` kia đang có sẵn trong index từ trước → phát hiện qua `git show --stat HEAD` thấy 8 file thay vì 7. Đã sửa bằng `git reset --soft HEAD~1` (không đụng working tree) rồi `git restore --staged` riêng file `D` đó, commit lại — kết quả cuối chỉ đúng 7 file, working tree các file Phase 1 khác được khôi phục nguyên trạng pending như trước khi bắt đầu task (đã verify lại `git status --short` + chạy lại test PASS).

## Concern

- `generateCode()` đổi từ instance-mutating (Phase 1 style) sang static-pure theo đúng interface brief chỉ định — task sau (tạo phiếu `BorrowSell` thật) cần biết: gọi `BorrowSell::generateCode()` TRƯỚC khi insert (không dựa vào `$this->id` của bản ghi vừa tạo), và có race condition nhẹ giữa 2 request đồng thời (dùng `max(id)+1` thay vì id thật) — cần cân nhắc unique constraint `code` (đã có `UNI` trên `borrow_sells.code`) để catch trùng, hoặc lock khi cần độ chính xác cao hơn.
- `borrow_sells` không có `company_id`/`department_id` như `borrow_sell_requests` — nếu task sau cần lọc theo công ty/phòng ban phải lấy qua `borrowSellRequest()` hoặc `contractable`.
