# Task P2-4 — Report: BorrowSellPostingService nhánh FirmContract

## Bước điều tra 1 — resolveContract nạp HĐ ra sao

**Kết luận: `borrow_sells.contractable_id` trỏ THẲNG `firm_contracts.id` (ERP HĐ hãng thật), KHÔNG PHẢI `hrm_contracts.id`.**

Verify bằng SQL thật trên `erp_hrm_check`:
```sql
SELECT id, contractable_id, contractable_type, borrow_sell_request_id, status FROM borrow_sells ORDER BY id DESC LIMIT 10;
-- => contractable_id ví dụ 24889, 24890, 24884... contractable_type='App\Model\Sale\Firm\Contract\FirmContract'
SELECT id, code FROM firm_contracts WHERE id=24889;  -- => tồn tại, khớp
SELECT id, code FROM hrm_contracts WHERE id=24889;   -- => KHÔNG tồn tại
SELECT count(*), max(id) FROM hrm_contracts;         -- => chỉ 2 dòng, max id=15
SELECT max(id) FROM firm_contracts;                  -- => 24935
```
`hrm_contracts` (bảng của `Modules\Assign\Entities\Contract\Contract`) là HĐ "Giao việc" theo báo giá — miền dữ liệu hoàn toàn khác HĐ hãng ERP, chỉ có 2 dòng test. Vậy `Contract::find($bs->contractable_id)` (như brief gợi ý nếu id trỏ thẳng) là SAI — sẽ luôn trả null cho dữ liệu Firm thật.

**Nhưng** 6 method cụm của `SupportAccountingTrait` type-hint cứng `Contract $contract` (namespace `Modules\Assign\Entities\Contract\Contract`), không nhận `FirmContract`. Sau khi kiểm tra kỹ, tìm được lời giải KHÔNG PHẢI đoán mà dựa trên cấu trúc DB đã verify:

1. Entity `Modules\Finance\Entities\Contract\FirmContract` (đã có sẵn, chỉ đọc, `$table='firm_contracts'`) map đúng bảng `firm_contracts`.
2. `firm_contracts` có ĐỦ và ĐÚNG TÊN các cột mà trait cần: `customer_id`, `created_by`, `code`, `company_id`, `department_id`, `part_id` — trùng tên với các cột tương ứng trên `hrm_contracts`/`Contract` entity.
3. Bảng HTHT `firm_support_accounting` (đằng sau `Contract::support_accounting()` morphOne) là bảng **polymorphic dùng chung** — verify:
   ```sql
   SELECT contractable_type, count(*) FROM firm_support_accounting GROUP BY contractable_type;
   -- App\Model\Sale\Firm\Contract\FirmContract  21403
   -- Modules\Assign\Entities\Contract\Contract  2
   ```
   => `firm_support_accounting` đã được ERP + HRM dùng chung sẵn, khớp đúng `BorrowSell::CONTRACT_FIRM` const.
4. `getDataBorrowSellAccounting`/`saveAccountDetail` phía ERP (`BorrowSellsController@update`, dòng ~283-309) xác nhận: khi `contractable_type===FirmContract::class`, `contractable_id`/`contractable_type` dùng để ghi sổ chính là `$object->contractable_id`/`$object->contractable_type` (id HĐ hãng thật) — KHÔNG qua biến đổi nào khác. Củng cố việc dùng `$bs->contractable_id`/`$bs->contractable_type` trực tiếp cho meta ghi sổ (không dùng id của shim, shim không có id thật).

=> **Giải pháp `resolveContract`**: nạp `FirmContract::find($bs->contractable_id)`, dựng SHIM `new Contract($firm->getAttributes())` (KHÔNG lưu DB — chỉ dùng trong bộ nhớ để thoả type-hint trait), rồi `setRelation('support_accounting', SupportAccounting::where('contractable_id', $firm->id)->where('contractable_type', BorrowSell::CONTRACT_FIRM)->first())` để gắn đúng HTHT của chính HĐ hãng đó (không phải HTHT rỗng do querying theo `Contract::class`).

Đây KHÔNG phải là đoán dữ liệu — mọi cột dùng để dựng shim đều lấy trực tiếp từ `firm_contracts` (bảng thật, đã verify tồn tại + đúng tên cột), và quan hệ HTHT lấy đúng theo khoá polymorphic đã verify tồn tại sẵn cho cả 2 loại contractable. Đây là điểm lệch khỏi khung quyết định nhị phân của brief ("nếu contractable_id trỏ thẳng contracts.id → Contract::find; nếu không rõ → NEEDS_CONTEXT") — thực tế contractable_id trỏ thẳng **firm_contracts.id chứ không phải contracts.id (hrm_contracts)**, và giải pháp shim vẫn khả thi & không suy đoán số liệu. Báo `DONE_WITH_CONCERNS` để chủ động flag điểm này cho reviewer, thay vì tự ý coi là NEEDS_CONTEXT khi đã có lời giải kỹ thuật rõ ràng và verify được.

## Bước điều tra 2 — công thức giá vốn

ERP `FirmContractBorrowSellService::costAccounting` (dòng 198-210):
```php
$total = $product->export_price * $product->qty;   // KHÔNG nhân unit_coefficient
AccountDetail::createDataSaveDept($accounts, 157, $total, AccountDetail::TYPE_HAS, [632], [...]);
```
ERP KHÔNG nhân `unit_coefficient`. Tuy nhiên brief mục "Bút toán nhánh Firm" (dòng 63-68) yêu cầu tường minh:
```
$cost = Σ qty × unit_coefficient × export_price
```
— đúng công thức mẫu HRM `ProductExportPostingService::costAccounting` (xuất hàng thường, cũng nhân `unit_coefficient`) do `borrow_sell_products` (bảng HRM, Task 1) có cột `unit_coefficient` riêng để chuẩn hoá đơn vị bán ≠ đơn vị cơ sở (khác cấu trúc dữ liệu ERP gốc cho HĐ hãng). Đã theo đúng chỉ định của brief (Σ qty×unit_coefficient×export_price), KHÔNG theo công thức thô ERP — chọn theo hướng dẫn tường minh trong brief (ưu tiên hơn phần "port ERP" tổng quát), vì brief đã lường trước sai khác này và ra quyết định sẵn ở mục Bút toán nhánh Firm.

Đã ghi chú rõ trong code (docblock `costAccounting`).

## Shape `getDataAccounting`

`public function getDataAccounting(BorrowSell $bs): array` → `[bool $ok, array $accounts, string $message]`, KHÔNG ghi DB — khớp shape `getDataProductExportAccounting`.
- Nhánh `contractable_type === BorrowSell::CONTRACT_FIRM` → gọi `resolveContract` + `firmBranch`.
- Nhánh khác (WrService) → `[false, [], 'Nhánh WrService chưa hỗ trợ (Task 5)']` (đúng yêu cầu brief, KHÔNG tự làm).
- Lỗi cấu hình (thiếu HTHT / thiếu trưởng phòng...) từ `firmBranch` được ném `\RuntimeException` (vì interface bắt buộc `firmBranch(): void`, không có tham số lỗi) và `getDataAccounting` bắt lại chuyển thành `[false, [], $msg]`.

`public function postAccounting(BorrowSell $bs): array` → `[bool $ok, string $message]`; gọi `getDataAccounting`, nếu ok và `$accounts` không rỗng thì `resolveContract` lại 1 lần nữa (chỉ để lấy `company_id/department_id/part_id/customer_id/created_by/code` của HĐ hãng cho `$meta`, vì bảng `borrow_sells` KHÔNG có các cột tổ chức này — verify `SHOW COLUMNS borrow_sells`), rồi `AccountDetail::saveAccountDetail(...)` trong `DB::transaction`. `meta.contractable_id/contractable_type` lấy THẲNG từ `$bs->contractable_id/contractable_type` (không phải id của shim — shim không có id thật), đúng cách ERP ghi (`BorrowSellsController@update` dòng ~309).

## Cách dựng fixture test

Chọn HĐ Firm THẬT: `firm_contracts.id=9` (mã `HĐ_TPV_MT_KD_25_0002_01`), có:
- `firm_support_accounting.id=62` (`contractable_id=9`, `contractable_type=FirmContract`), `before_vat_total=11.566.668`, `before_vat_product` cùng giá trị, `before_vat_delivery_cost=0`, `before_vat_repair_service=0`.
- `firm_support_accounting_departments.id=76`: `department_id=77` (Kinh doanh CN Vinh, `company_id=3`, `department_lead_id=1056`), `is_main=1`, `objectable_type=Department`, `objectable_id=77`.
- `firm_support_accounting_employees.id=78`: 1 NV (employee_id=417, `part_id=NULL` → bỏ qua nhánh trưởng bộ phận, không lỗi).
- `firm_contracts.id=9`: `customer_id=19074`, `created_by=417`, `company_id=3`, `department_id=77`.

Test (`BorrowSellPostingFirmTest::test_firm_branch_credits_157_for_cost`) build `BorrowSell`/`BorrowSellProduct` HOÀN TOÀN in-memory (`new BorrowSell([...])`, `setRelation('products', collect([...]))`) — KHÔNG lưu DB (dùng `DatabaseTransactions` sẵn có nhưng thực tế không insert gì vì `getDataAccounting` chỉ đọc). Trước khi build, kiểm tra `firm_contracts`/`firm_support_accounting` (id=9/62) còn tồn tại trong DB test → nếu không, `markTestSkipped`.

## Kết quả test

```
php vendor/bin/phpunit --filter=BorrowSellPostingFirmTest Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php
```
→ `OK (1 test, 5 assertions)`

Giá trị thực tế (chạy qua tinker với data fixture giống test, 1 SP: price=1.000.000, qty=10, export_price=900.000, unit_coefficient=1, vat=10%, `sum_amount_after_extra`=11.000.000, `sum_amount_after_extra_vat`=1.100.000):
- **157 (Có) = 632 (Nợ) = 9.000.000** (giá vốn: 900.000 × 10 × 1)
- Cụm 1 (Doanh thu): Nợ 1311=12.100.000 / Có 5111=11.000.000 + Có 33311=1.100.000
- Cụm 2 (Giảm trừ): Nợ 5213=10.000.000 + Nợ 33311=1.000.000 / Có 1311=11.000.000 (do `allocated_price=rebate_price=0` → `discount_price = price+extra_price = 1.000.000`)
- Cụm 4/5 (Thưởng HĐ + TNCN): 0 (vì `bonus_contract_before_vat=0`, `tndn_vat=0` ở HĐ fixture)
- Cụm 6+7 (Hoa hồng tháng/quý), cụm 8 (Quỹ rủi ro): tổng ~40.000 (theo tỷ lệ `%` phân bổ theo HTHT dept 77)
- **Tổng Nợ = Tổng Có = 32.140.000** (cân)

## Files thay đổi
- `Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php` (mới)
- `Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php` (mới)

## Commit
`fe9c48f25` — "feat(finance): BorrowSellPostingService nhánh FirmContract (giá vốn TK157 + doanh thu + cụm hỗ trợ)" (2 files changed, 326 insertions(+))
