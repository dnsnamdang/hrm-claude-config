# Task P2-7 Report — BorrowSellService::store() (orchestrator tạo phiếu xuất bán hàng mượn)

## Status: DONE

## File tạo
- `Modules/Finance/Services/BorrowSell/BorrowSellService.php` — orchestrator `store()` + private
  `updateWarehouse()`, `returningQty()`, `computeHeaderSums()`.
- `Modules/Finance/Tests/Feature/BorrowSellStoreTest.php` — 3 test, đều XANH THẬT (không skip).

## Kết quả test
```
php vendor/bin/phpunit --filter=BorrowSellStoreTest Modules/Finance/Tests/Feature/BorrowSellStoreTest.php
OK (3 tests, 13 assertions)
```
- `test_compute_header_sums_firm_includes_price_and_wr_service_zeroes_price` — khoá Ruling T7-1
  (Firm cộng price vào amount_after_extra; WrService price=0). Pure function, không cần DB.
- `test_compute_header_sums_accumulates_multiple_rows` — nhiều dòng SP cộng dồn đúng.
- `test_returning_qty_excludes_parent_request` — khoá Ruling T7-5, DỰNG FIXTURE THẬT trên
  `product_export_requests`/`borrow_sell_requests`/`borrow_sell_request_products`/
  `borrow_sell_request_product_details` (đã verify các bảng này KHÔNG có FOREIGN KEY constraint
  thật, chỉ có index đặt tên `*_foreign`, nên insert orphan row an toàn trong
  `DatabaseTransactions`). Assert: loại trừ parent → 2 (chỉ còn phiếu khác); không loại trừ → 7
  (cộng cả 2 phiếu).

Regression check các test liên quan sẵn có vẫn xanh:
```
php vendor/bin/phpunit --filter="BorrowSellPostingFirmTest|BorrowSellPostingWrServiceTest|BorrowSellDeliveryTripAccountingTest|BorrowSellEntityTest|BorrowSellRequestCalculatorTest" Modules/Finance/Tests
OK (9 tests, 40 assertions)
```

## Tóm tắt implementation (theo 7 rulings)
- **T7-1**: `computeHeaderSums(array $rows): array` — private pure function, nhận mảng dòng SP
  server build (`is_firm, price, extra_price, allocated_price, vat_percent, qty`), trả 6 field
  header sums. `store()` tích luỹ `$rowsForSums[]` trong lúc loop products (dùng giá đã copy vào
  `BorrowSellProduct`, KHÔNG đọc từ `$request`), gọi `computeHeaderSums()` sau loop, set vào
  `$object` rồi save 1 lần trước `updateWarehouse()`.
- **T7-2**: `$object->code = 'TMP-'.uniqid()` → `save()` (lấy id thật) → `code =
  BorrowSell::PREFIX.'-'.str_pad((string)$object->id,5,'0',STR_PAD_LEFT)` → `save()` lần 2.
  KHÔNG dùng `BorrowSell::generateCode()` static (dùng `max('id')+1` trước insert → race).
- **T7-3**: `updateWarehouse()` dùng `DB::table(...)->increment(...)` cho `borrow_returned_qty`,
  `returned_by_sell` (trên `product_export_request_details`) và `exported_qty` (trên
  `firm_contract_tab_products`/`wr_service_contract_items`, chọn bảng theo
  `BorrowSellProduct::objectable_type`). `approved_qty` (gán, không cộng dồn) dùng
  Eloquent `->save()` bình thường.
- **T7-4**: toàn bộ `store()` bọc trong 1 `DB::transaction(closure)`. Sau `updateWarehouse()`,
  gọi `postDeliveryTripAccounting($object)` RỒI `postAccounting($object)` (resolve qua
  `app(BorrowSellPostingService::class)`), check tuple `[ok, err]`, `throw new \RuntimeException`
  nếu `ok=false` để rollback transaction ngoài (2 service posting tự mở transaction/savepoint
  riêng bên trong, không sửa gì trong đó).
- **T7-5**: `returningQty(int $exportRequestId, int $productId, int $excludeParentRequestId): float`
  — copy nguyên body Phase 1 `BorrowSellRequestService::returningQty()`, thêm
  `->where('bsr.id', '!=', $excludeParentRequestId)` vào nhánh `$sell` (subquery lọc
  `bsr.status = 2`). 2 nhánh `$import`/`$other` giữ nguyên.
- **T7-6**: Service chỉ port nhánh `HANG_THUONG`. `store()` chặn sớm (throw
  `ValidationException`) nếu `$parent->type !== BorrowSellRequest::HANG_THUONG` — KHÔNG có bất kỳ
  code nào xử lý `tabs`/`syncTabs`/`contract_promotion_id` (branch KM của ERP bị bỏ hoàn toàn,
  đúng ruling).
- **T7-7**: Không có bất kỳ điều kiện nào tham chiếu cột `need_check_exported` — cả check tồn
  trong quota hợp đồng (ERP dòng 258-264, gated bởi cột này) lẫn gate trong `updateWarehouse`
  (ERP dòng 412: `need_check_exported || (Firm && !count(tabs)) || WrService`) đều bị BỎ (luôn
  chạy nhánh cộng `exported_qty`, không check quota hợp đồng — vì Ruling T7-6 đã loại tabs nên
  điều kiện ERP thu về `true` trong mọi trường hợp Service này xử lý).

## Luồng store() (đối chiếu brief)
1. `BorrowSellRequest::findOrFail($request->borrow_sell_request_id)`.
2. Validate NGOÀI transaction: `!$parent->canApprove()` → `ValidationException`. Thêm guard
   `$parent->type !== HANG_THUONG` → `ValidationException` (assumption, xem mục Concerns).
3. `DB::transaction(closure)`:
   a. Tạo `$object` (copy header từ `$parent`: `contractable_id/type`, `type`, `status=1` CỨNG,
      `firm_contract_tab_id`, `borrow_sell_request_id`, `created_by=auth()->id()`, `note`,
      `vat_percent` từ request, `bear_the_shipping` từ request) → save → generateCode (T7-2) → save.
   b. Loop `$request->products` → tra `BorrowSellRequestProduct` cha theo
      `objectable_id`/`objectable_type` → tạo `BorrowSellProduct` copy snapshot toàn bộ field giá
      từ dòng cha (KHÔNG từ payload) → loop `product['details']` → tra
      `BorrowSellRequestProductDetail` cha theo `product_export_request_detail_id` → load
      `ProductExportRequestDetail` thật → tính `returningQty()` (loại trừ parent) →
      `BorrowSellRequestCalculator::availableSellQty/isQtyExceeded` → throw nếu vượt → tạo
      `BorrowSellProductDetail` → cộng dồn `qty` + `total_export_price` (weighted theo
      `unit_coefficient`) → set `$p->qty`/`$p->export_price` (bình quân gia quyền) → ghi ngược
      `export_price` xuống `$requestProduct` (như ERP) → tích luỹ `$rowsForSums[]`.
   c. `!$hasChange` → throw.
   d. `computeHeaderSums()` → set 6 field header → save (T7-1).
   e. `updateWarehouse($object)` (T7-3, T7-6, T7-7).
   f. `postDeliveryTripAccounting` rồi `postAccounting`, check `[ok,err]` throw nếu lỗi (T7-4).
   g. Approve parent: `status=DA_DUYET`, `approver_id=auth()->id()`, `approved_time=now()`, save.
   h. `return $object`.

## Concerns / giả định (t7-investigation.md thiếu chi tiết hoặc brief không nói rõ)

1. **Guard "chỉ HANG_THUONG"**: brief không yêu cầu tường minh throw nếu `$parent->type !=
   HANG_THUONG`, chỉ nói "T7-6: HANG_THUONG only — bỏ tabs". Vì toàn bộ code Service không xử lý
   nhánh KM (`tabs`, `contract_promotion_id` lookup) nên nếu gọi `store()` với phiếu YC loại
   `HANG_KM`, code sẽ silent-fail sai cách (tra `BorrowSellRequestProduct` theo
   `objectable_id/objectable_type` có thể vẫn ra kết quả nhưng `contract_promotion_id` snapshot sẽ
   sai ngữ nghĩa). Tôi thêm 1 guard tường minh throw `ValidationException` ngay đầu `store()` để
   fail-closed thay vì chạy sai logic — CẦN CONFIRM với người sở hữu design nếu route/FE có thể
   gửi phiếu HANG_KM vào endpoint này (nếu có, Phase sau phải bổ sung nhánh KM riêng).

2. **KHÔNG gọi `$contract->updateHandoverDate()`** (ERP bước 11, `store()` dòng 316). Brief liệt
   kê luồng store() từng bước (mục "Luồng store()") KHÔNG có bước này — chỉ có a→i kết thúc ở
   approve parent. Tôi theo đúng brief (không thêm hành vi ngoài spec). Nếu cần, đây là 1 dòng bổ
   sung dễ thêm sau (cần entity Contract implement `updateHandoverDate()` — chưa kiểm tra HRM có
   port hàm này chưa).

3. **KHÔNG update nested `objectable` của `wr_service_contract_items`** (ERP dòng 416-421:
   `WrServiceContract` còn có 1 cấp `objectable` lồng bên trong `contract_item->objectable` cũng
   cộng `exported_qty`). t7-investigation.md mục 2 có nhắc tới nhưng brief (mục "updateWarehouse()
   — port ERP") chỉ liệt kê map 2 bảng phẳng (`firm_contract_tab_products` /
   `wr_service_contract_items`), không nhắc nested objectable. `wr_service_contract_items` có cột
   `objectable_id`/`objectable_type` (morphTo generic, ERP trỏ tới nhiều loại bảng khác nhau tuỳ
   `type`) — việc port đúng đòi hỏi điều tra thêm ngoài scope brief này. Bỏ qua theo đúng phạm vi
   brief, ghi rõ ở đây để task sau (nếu WrService cần double-increment) biết chỗ thiếu.

4. **`ProductExportRequest::DA_TRA` không có const trong entity HRM** (`Modules/Finance/Entities/
   ProductImportRequest/ProductExportRequest.php` chỉ có `DA_MUON=2`, thiếu `DA_TRA`). Đã verify
   giá trị ERP thật (`app/Model/Warehouse/ProductExportRequest.php:56 const DA_TRA = 3`) và dữ
   liệu thật trên DB gộp (`SELECT DISTINCT borrow_status FROM product_export_requests WHERE
   type=3` → có giá trị 1/2/3). Khai lại `const PER_DA_TRA = 3` cục bộ trong
   `BorrowSellService` (KHÔNG sửa entity `ProductExportRequest` — theo constraint "không tự sửa
   hàm/entity dùng chung khi chưa xác nhận").

5. **`bear_the_shipping`/`vat_percent` lấy từ `$request`** (không tính lại) — theo đúng ERP gốc
   (t7-investigation.md mục 9: ERP tin thẳng field này từ FE, không validate). Không nằm trong
   phạm vi T7-1 (chỉ 6 field `sum_amount_*`/`vat_cost_allocated` phải tính lại).

6. **Payload `products[].objectable_id/objectable_type` + `details[].product_export_request_detail_id`
   + `details[].qty`** — dùng đúng shape brief khuyến nghị dựa theo ERP (t7-investigation.md mục
   9, kết luận payload). Chưa có `StoreBorrowSellRequest` FormRequest thật (task Controller/Task 8
   sẽ tạo) nên chưa validate rule ở tầng HTTP — `store()` tự `firstOrFail()`/kiểm tra dữ liệu
   thiếu bằng exception Laravel chuẩn (`ModelNotFoundException` nếu thiếu `details` key hoặc dữ
   liệu sai — CHƯA bọc thành `ValidationException` cho các case "thiếu key trong payload", chỉ có
   "tồn không đủ" và "không có thay đổi" là `ValidationException` tường minh theo đúng brief).

## Không đụng
- `Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php` — chỉ gọi qua `app(...)`,
  không sửa file.
- Không có migration mới, không sửa entity nào khác ngoài 2 file tạo mới.
