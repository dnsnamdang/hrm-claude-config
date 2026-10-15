# Task 6 — BorrowSellRequestService (store + duyệt + notify + searchByFilter) — Report

## 1. File tạo/sửa

- **Create:** `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php`
- **Modify:** `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php` — thêm `public static function searchByFilter($request)` + `public static function meta(): array` (chèn trước block "2 helper cho loại phiếu nhập 9").
- **Modify:** `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestSourceService.php` — đổi visibility `private function firmExportingQty(...)` → `public function firmExportingQty(...)` và `private function firmBorrowingQty(...)` → `public function firmBorrowingQty(...)`. **KHÔNG đổi logic**, chỉ thêm docblock giải thích lý do (Task 6 cần gọi để guard quỹ HĐ ở `store()`). Đây là thay đổi DUY NHẤT trên file Task 5, đúng RULING #8 brief.

## 2. Lựa chọn visibility SourceService

Chọn phương án DRY (đổi `private` → `public`) thay vì viết lại `firmInflightQty()` riêng trong Service, để tránh trùng logic + tránh lệch khi Task 5 sau này sửa. Lý do đã ghi trong docblock 2 method.

## 3. Cột hợp đồng đã dùng — PHÁT HIỆN QUAN TRỌNG khác brief

Brief giả định cột `support_accounting_id` tồn tại (hoặc biến thể tên) trực tiếp trên `firm_contracts`/`wr_service_contracts`. Đã chạy `Schema::getColumnListing()` cho cả 2 bảng — **KHÔNG có cột nào dạng `support_accounting*`**. Đọc lại ERP gốc (`app/Http/Controllers/Warehouse/BorrowSellRequestsController.php:255` + `FirmContract::support_accounting()` / `WrServiceContract::support_accounting()`) thì đây là **relation `morphOne`**, không phải cột:

- `FirmContract::support_accounting()` → `morphOne(FirmSupportAccounting::class, 'contractable')`
- `WrServiceContract::support_accounting()` → `morphOne(WrSupportAccounting::class, 'contractable')`

Verify bảng thật trong DB gộp (`information_schema.tables`): `firm_support_accounting` và `wr_support_accounting` (số ít, KHÔNG có "s" cuối — khác convention Eloquent mặc định vì model không khai `$table` nhưng đã kiểm tra dữ liệu thật). Cột `contractable_id` + `contractable_type`. Đã verify dữ liệu thật:
```
firm_support_accounting.contractable_type distinct: 'App\Model\Sale\Firm\Contract\FirmContract', 'Modules\Assign\Entities\Contract\Contract'
wr_support_accounting.contractable_type distinct: 'App\Model\Customers\WrServiceContract'
```
Khớp CHÍNH XÁC với `BorrowSellRequest::CONTRACT_FIRM` / `CONTRACT_WR_SERVICE`. → `loadContract()` trong Service tính `has_support_accounting` bằng `exists()`-query trên 2 bảng này thay vì đọc cột, port ĐÚNG ý nghĩa ERP (không phải khung no-op). Đây KHÔNG phải "cần chốt" — đã tự giải quyết được bằng cách đọc source ERP thật (repo `ERP/TanPhatDev` có sẵn cạnh HRM, đọc read-only).

Cột khác đã dùng của `firm_contracts`: `id, customer_id, customer_type, customer_name, customer_address, customer_mobile, customer_contact_name, customer_contact_phone, contact_address, type, price_type` — tất cả tồn tại đúng tên.

Cột khác đã dùng của `wr_service_contracts`: `id, customer_id, customer_type, customer_name, customer_address, customer_mobile, customer_contact_name` — tồn tại. **`customer_contact_phone` và `contact_address` KHÔNG tồn tại trên `wr_service_contracts`** trong DB gộp (chỉ có `customer_contact_phones` dạng khác + `receiver_address`/`delivery_place` không tương đương 1-1) → set `null` cho 2 trường snapshot này khi tạo phiếu WrService (ghi "cần chốt": nếu UI cần đúng số điện thoại/địa chỉ liên hệ của HĐ dịch vụ, cần xác nhận field nguồn chính xác — hiện để trống, không chặn nghiệp vụ).

## 4. `need_check_exported` — GAP dữ liệu merged DB

Cột `need_check_exported` **không tồn tại ở bất kỳ bảng nào** trong `erp_hrm_check` (đã `grep information_schema.columns` toàn DB, 0 kết quả). ERP đọc `$contract->need_check_exported` trên `WrServiceContract` (HĐ hãng Firm luôn `true`, không có cờ này). Vì cột không tồn tại nên KHÔNG thể select nó trong query builder (sẽ lỗi SQL). Xử lý: `loadContract()` trả `need_check_exported = null` cho nhánh WrService, và `syncProducts()` coalesce `$contract->need_check_exported ?? true` → **luôn `true`** trong thực tế hiện tại. Đây là hành vi AN TOÀN HƠN ERP gốc (luôn enforce check quỹ SL hợp đồng, không bao giờ bỏ qua ngầm) chứ không phải bypass — nhưng có nghĩa Phase 1 KHÔNG thể tái tạo trường hợp ERP cho phép bỏ qua check với 1 số HĐ dịch vụ đặc biệt. **Cần chốt**: nếu nghiệp vụ thực sự cần cờ này linh hoạt theo từng HĐ dịch vụ, phải bổ sung cột `need_check_exported` vào `wr_service_contracts` trong 1 migration riêng (ngoài scope Task 6).

## 5. assertDiffPrice() — port ĐẦY ĐỦ (không dùng khung no-op)

Đọc ERP `app/Product.php:1407 getPriceByUnitAndType()`:
```
ProductUnit::where('product_id',...)->where('unit_id',...)  // hoặc where('is_base', true) nếu không có unit_id
  → firstOrFail()
ProductUnitPrice::where('product_unit_id', $unit->id)->where('price_type_id', $type ?: 1)->firstOrFail()
```
Verify bảng `product_units` (đã dùng ở Task 5) + `product_unit_prices` (cột: `id, price_type_id, product_unit_id, price, ...`) tồn tại đủ trong DB gộp. Port thành `priceByUnitAndType()` private, khác ERP 1 điểm có chủ đích: ERP dùng `firstOrFail()` (ném 404/500 nếu thiếu dữ liệu catalog); Service HRM trả `null` và **bỏ qua so sánh SP đó** (không chặn) nếu thiếu product_unit/giá — vì đây chỉ là mốc so sánh, thiếu dữ liệu tham chiếu không nên làm sập luồng tạo phiếu. Toàn bộ phần còn lại (hệ số công ty `product_company_coefficients`, làm tròn `round($price*$coef/1000)*1000`, so sánh `floatValue()`, gom `change_price` list, throw `ValidationException` kèm key `change_price`) port khớp 1-1 với ERP `checkDiffPrice()` (controller dòng 641-711). Dùng thẳng helper global `floatValue()` có sẵn trong HRM (`app/Helper/FormatHelper.php:1039`), không cần viết lại.

## 6. searchByFilter() — filter đã bỏ/đổi

- Bỏ eager-load `contractable`/`customer` (entity Task 3 chưa khai morph relation `contractable`; dữ liệu khách hàng đã snapshot sẵn trên `borrow_sell_requests` nên không thiếu thông tin hiển thị list).
- `customer` filter: đổi từ `whereHasMorph` sang lọc thẳng cột snapshot `customer_id` trên chính bảng (nhanh hơn, cùng kết quả).
- `contract_code` filter: port bằng subquery `firm_contracts`/`wr_service_contracts` theo `contractable_type` tương ứng (thay `whereHasMorph`).
- Bỏ nhánh `type == 'create_adjust'` (ERP lọc `status in [1,12,13]` — Phase 1 HRM chưa dùng các status 1/12/13 cho luồng này, entity Task 3 chỉ có DA_DUYET=1/CHO_KE_TOAN_KHO=2/DANG_TAO=3/KHONG_DUYET=4/CHO_TP_DUYET=10/CHO_BGD_DUYET=11 — không rõ ý nghĩa 12/13 trong scope HRM, để ngoài scope, ghi cần chốt nếu FE cần tab này).
- Bỏ nhánh `type == 'return'` (ERP dùng cho màn chọn phiếu để trả hàng — đã có sẵn `searchForPicker()` riêng trong entity từ trước cho đúng mục đích này, `searchByFilter()` không cần cover lại).
- Còn lại (type=all/accounting/waiting_approve, các filter phụ contract_id/contract_type/created_by/export_type/approver/code/status/startDate/endDate/company/department/productName/productCode, order mặc định, guard cuối `created_by=self OR status!=3`) port 1-1.

## 7. Notification — chuẩn hoá theo skill `notification-convention`

Brief đề xuất nhóm hành động "Gửi duyệt"/"Chờ TP duyệt"/"Chờ BGD duyệt" — KHÔNG nằm trong 14 nhóm hành động chuẩn của skill. Đã đổi thống nhất về **"Chờ duyệt"** (nhóm chuẩn) cho mọi thông báo chuyển tiếp người duyệt kế tiếp (tạo mới → KT kho, TP duyệt → KT kho, TP chuyển BGD, BGD duyệt → KT kho), giữ nguyên "Từ chối" cho `deny()`. Đã bọc `<b>...</b>` quanh mã phiếu (tên đối tượng) theo mục 4 skill. Prefix giữ `[XBHM]` (chưa có prefix chuẩn khác cho module này, theo plan gốc).

## 8. Output verify

### php -l
```
No syntax errors detected in Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php
No syntax errors detected in Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php
No syntax errors detected in Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestSourceService.php
```

### composer dump-autoload -o
```
...
Generated optimized autoload files containing 12321 classes
```

### Tinker khói (class load + method_exists)
```
Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestService
searchByFilter exists: 1
meta exists: 1
store exists: 1
deny exists: 1
managerApprove exists: 1
switchBoardOfManager exists: 1
boardOfManagerApprove exists: 1
getDebtCustomerByEmployee exists: 1
```

### Smoke-test store() — DỰNG ĐƯỢC dữ liệu thật, đã chạy thành công

Dữ liệu dùng (đọc từ DB gộp thật, đã dò để thoả mọi điều kiện: can_borrow_sell, quỹ HĐ, availableSellQty):
- Employee `created_by=590` (auth qua `App\Models\TpEmployee::find(590)` — model provider thật của guard `api`, KHÔNG dùng `Auth::loginUsingId` vì guard JWT không hỗ trợ).
- `firm_contracts.id=5895` (type=7 ≠ DON_HANG_NGUYEN_TAC nên không kích diff-price; `firm_support_accounting` có bản ghi → pass check hỗ trợ hạch toán).
- `product_export_requests.id=12246` (type=3 XUAT_MUON, status=5, borrow_status=2, created_by=590 → `canBorrowSell` pass).
- SP `product_id=36501, unit_id=40` (unit_coefficient=1), detail `base_exported_qty=5, borrow_returned_qty=1`, `returningQty()`=0 (không có import/sell/other in-flight) → available=4, request qty=1 → không exceeded.
- `firm_contract_tab_products.id=67477` (firm_contract_tab_id/parent_id=10530, quantity=1, exported_qty=0) → quỹ HĐ đủ cho qty=1.

Kết quả:
```
OK code=PYCXBHM-04389 status=2 id=4389
products count: 1
details count: 1
pivot count: 1
account_details before/after: 971930/971930   ← KHÔNG đổi (Phase 1 chưa hạch toán) — ĐÚNG
borrow_sell_requests before/after: 4363/4364   ← +1 bản ghi mới
```
`generateCode()` sinh đúng format `PYCXBHM-00004389`? — thực tế in ra `PYCXBHM-04389` (5 chữ số zero-pad của id=4389, đúng `str_pad(...,5,'0',STR_PAD_LEFT)` trong entity Task 3).

Sau đó test tiếp 4 method duyệt/từ chối trên chính bản ghi vừa tạo (ép status thủ công để mô phỏng từng trạng thái nguồn):
```
after managerApprove status=2        (10→2 đúng)
after switchBoardOfManager status=11 (10→11 đúng)
after boardOfManagerApprove status=2 (11→2 đúng)
after deny status=4 comment=Test deny lý do   (→4, comment lưu đúng)
getDebtCustomerByEmployee: 199260000   (chạy không lỗi, trả số dương hợp lý)
searchByFilter count: 35   (nhánh created_by=self vì employee 590 không có quyền view rộng — đúng kỳ vọng)
meta => tất cả false (employee 590 không có quyền nào trong 6 quyền — fail-closed đúng, KHÔNG có cờ nào bị hard-code true)
```

**Đã dọn dữ liệu test** (xoá `borrow_sell_request_product_details`, `borrow_sell_request_products`, `borrow_sell_request_has_export_requests`, `borrow_sell_requests` id=4389) để không để lại rác trên DB dev dùng chung `erp_hrm_check`.

## 9. "Cần chốt" — tổng hợp

1. `wr_service_contracts` thiếu cột `need_check_exported` trong merged DB → hiện luôn coalesce `true` (an toàn hơn, không bypass). Cần chốt có bổ sung migration cột này để khôi phục hành vi linh hoạt theo từng HĐ dịch vụ không.
2. `wr_service_contracts` thiếu `customer_contact_phone`/`contact_address` 1-1 → snapshot 2 trường này trên phiếu WrService hiện để `null`. Cần chốt nguồn dữ liệu đúng nếu UI cần hiển thị.
3. Nhánh `searchByFilter(type=create_adjust)` của ERP (status 1/12/13) chưa port — ngoài scope status hiện có ở entity Task 3. Cần chốt nếu FE Task 8+ cần tab này.

Không có mục nào bị "che check âm thầm" — mọi rẽ nhánh dữ liệu thiếu đều nghiêng về phía AN TOÀN HƠN (luôn check / bỏ qua so sánh khi thiếu mốc tham chiếu, không bao giờ tự động pass một check nghiệp vụ then chốt như over-limit/qty/support-accounting).
