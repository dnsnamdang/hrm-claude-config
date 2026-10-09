# Task P2-4: BorrowSellPostingService — nhánh FirmContract (giá vốn TK 157) — Brief (verbatim)

Đây là requirements của bạn. Đọc file này trước, dùng đúng giá trị verbatim.

## Bối cảnh
Feature "xuất bán hàng mượn" Phase 2 (HRM, Laravel 8/PHP 7.4, nhánh `gop_db`, DB gộp `erp_hrm_check`). Repo: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api`.
Task này tạo `BorrowSellPostingService` với NHÁNH FirmContract: sinh bút toán cho phiếu xuất bán hàng mượn `BorrowSell` khi hợp đồng là HĐ hãng (FirmContract). Task 5 (sau) thêm nhánh WrService. Task 3 (đã xong, commit 2d4bbfe) đã tạo `SupportAccountingTrait` — bạn `use` lại.

## Ràng buộc toàn cục (bắt buộc)
- Nhánh `gop_db`: KHÔNG `DB_CONNECTION_SECOND`/`mysql2`. KHÔNG migration.
- KHÔNG đọc `vendor/`, `node_modules/`. Làm việc tiếng Việt.
- Kết thúc bằng đúng 1 commit trong phạm vi 2 file (Step 5).
- **CẤM git network/rewrite:** KHÔNG pull/push/fetch/rebase/reset --hard/merge. CHỈ `git add <path>` + `git commit`. Gặp xung đột → DỪNG, báo NEEDS_CONTEXT.
- KHÔNG tự dispatch subagent. **Chạy test bằng `php vendor/bin/phpunit --filter=<Name>`** (KHÔNG `php artisan test` — TTY fail).
- Work id (Global Constraints, bảng `works` cột `code`): DTHH=15 (doanh thu), GGHH=16 (giảm giá), TTHHD=12 (thưởng HĐ + TNCN), TNST=13 (HH tháng), TNSQ=14 (HH quý), RRP=6 (quỹ rủi ro). HRM KHÔNG có `getByCode()` → query `Work::where('code', ...)`.

## Files
- Create: `Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php`
- Test: `Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php`

## Nguồn ERP để port (chỉ đọc)
- `/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/TanPhatDev/app/Services/Sale/Firm/Contract/FirmContractBorrowSellService.php` — logic hạch toán bán hàng mượn nhánh HĐ hãng.
- (Task 5 sẽ dùng `app/Model/Warehouse/BorrowSell.php::getDataCreateDept()` cho nhánh WrService — task này CHƯA đụng.)

## Mẫu HRM để bám (chỉ đọc — QUAN TRỌNG)
`Modules/Assign/Services/ProductExportPostingService.php` — đặc biệt `getDataProductExportAccounting()` (dòng ~269-309): cách gọi trait `revenueAccounting`/`revenueDeductionAccounting`/`bonusContractAccounting`/`vatExtraCostAccounting`/`monthlyAndQuarterlyCommissionAccounting`/`riskFundAccounting` theo đúng thứ tự 8 cụm, cách trả `[bool, array, string]`, cách `costAccounting($pxh, $accounts, $group, $creditAcc)` ghi giá vốn. Service của bạn NHÁI cấu trúc này nhưng cho `BorrowSell` và credit **157**.

## Sự thật đã VERIFY (dùng làm chuẩn)
- Entity `BorrowSell` (Task 1): const `CONTRACT_FIRM='App\Model\Sale\Firm\Contract\FirmContract'`, `CONTRACT_WR_SERVICE='App\Model\Customers\WrServiceContract'`. Cột phân loại HĐ = `contractable_type` (+ `contractable_id`). Relation `products()` hasMany `BorrowSellProduct`.
- Cột `borrow_sell_products`: `product_id, product_name, unit_id, price, extra_price, contract_qty, qty, unit_coefficient, export_price, allocated_price, rebate_price, vat_percent`. **KHÔNG có cột `borrow_sell_qty`** — số lượng bán thực dùng cột **`qty`**.
- Trait `SupportAccountingTrait` (namespace `Modules\Assign\Services\Accounting`) cung cấp 6 method cụm + helper dept. Các method cụm nhận `Contract $contract` (kiểu `Modules\Assign\Entities\Contract\Contract`) và tự đọc `support_accounting` của HĐ.
- Contract entity HRM cho hạch toán = `Modules\Assign\Entities\Contract\Contract` (đã import sẵn trong ProductExportPostingService).

## BƯỚC ĐIỀU TRA BẮT BUỘC trước khi code (ghi kết quả vào report)
1. **resolveContract:** đọc entity `Modules/Finance/Entities/BorrowSell/BorrowSell.php` + cách ERP `FirmContractBorrowSellService` lấy HĐ. Xác định: từ `BorrowSell` (có `contractable_id`/`contractable_type`) nạp về `Modules\Assign\Entities\Contract\Contract` như thế nào (contractable_id có trỏ thẳng contracts.id không? hay qua borrow_sell_request?). Verify bằng 1 query mysql nếu cần:
   ```bash
   mysql -h127.0.0.1 -uroot erp_hrm_check -e "SELECT id, contractable_id, contractable_type, borrow_sell_request_id FROM borrow_sells ORDER BY id DESC LIMIT 5;"
   ```
   Nếu `contractable_id` trỏ thẳng `contracts.id` → `Contract::find($bs->contractable_id)`. Nếu KHÔNG rõ → báo NEEDS_CONTEXT, đừng đoán.
2. **Giá vốn:** xác nhận công thức `$cost = Σ (qty × unit_coefficient × export_price)` khớp ERP (đọc `FirmContractBorrowSellService`). Nếu ERP nhân cột khác (contract_qty?) → theo ERP, ghi rõ trong report.

## ⚠️ GOTCHA BẮT BUỘC — const WORK_* (nếu thiếu sẽ fatal)
Trait `SupportAccountingTrait` gọi 6 hằng số qua `self::WORK_*` NHƯNG các const này KHÔNG nằm trong trait — chúng ở `ProductExportPostingService`. Khi `BorrowSellPostingService` `use` trait, `self::WORK_*` phân giải theo class `BorrowSellPostingService` → **class của bạn PHẢI tự khai đủ 6 const này** (copy y hệt), nếu không PHP fatal "undefined constant":
```php
const WORK_DOANH_THU   = 15; // DTHH
const WORK_GIAM_TRU_DT = 16; // GGHH
const WORK_THUONG_HH   = 12; // TTHHD (thưởng HĐ + TNCN)
const WORK_HH_THANG    = 13; // TNST
const WORK_HH_QUY      = 14; // TNSQ
const WORK_QUY_RUI_RO  = 6;  // RRP
```

## Interfaces phải PRODUCE (Task 5-7 phụ thuộc — đúng tên/chữ ký)
- `class BorrowSellPostingService { use \Modules\Assign\Services\Accounting\SupportAccountingTrait; }` — **kèm 6 const WORK_* ở trên** (xem GOTCHA).
- `public function getDataAccounting(BorrowSell $bs): array` → trả `[bool $ok, array $accounts, string $message]` (KHÔNG ghi DB). **Trả cùng shape với `getDataProductExportAccounting`** để nhất quán. (Nếu bạn thấy hợp lý hơn khi trả thẳng mảng `$accounts`, PHẢI thống nhất: chọn `[bool,array,string]` cho khớp mẫu HRM — Task 5/7 sẽ dựa vào shape này.)
- `public function postAccounting(BorrowSell $bs): array` → `[bool $ok, string $message]`; nếu ok, ghi `account_details` qua `AccountDetail::saveAccountDetail($accounts, $bs->id, get_class($bs), $bs->code, [...])`.
- `private function resolveContract(BorrowSell $bs): ?Contract`
- `private function firmBranch(BorrowSell $bs, Contract $contract, array &$accounts, int &$group): void`

## Bút toán nhánh Firm (thứ tự 8 cụm như mẫu HRM)
1. Doanh thu: `revenueAccounting($gross, $gross_vat, $contract, $accounts, $group)` — Nợ 1311 / Có 511 (DTHH=15) + Có 33311.
2. Giảm trừ (nếu có): `revenueDeductionAccounting($sale_invoice, $sale_invoice_vat, $contract, $accounts, $group)` (GGHH=16).
3. **Giá vốn: Nợ 632 / Có 157** (KHÁC xuất thường dùng 155/156/1561). `$cost = Σ qty×unit_coefficient×export_price`. Ghi trực tiếp:
   ```php
   AccountDetail::createDataSaveDept($accounts, '632', $cost, AccountDetail::TYPE_DEPT, $ref, $objects, $note);
   AccountDetail::createDataSaveDept($accounts, '157', $cost, AccountDetail::TYPE_HAS, $ref, $objects, $note);
   ```
   (Xem cách `costAccounting` trong ProductExportPostingService dựng `$ref`/`$objects`/`$note` để làm tương tự cho BorrowSell.)
4-8. Cụm hỗ trợ (gọi trait, đọc `support_accounting` của `$contract`, dùng `%` xuất tương ứng): `bonusContractAccounting` (TTHHD=12), `vatExtraCostAccounting` (TNCN, TTHHD=12), `monthlyAndQuarterlyCommissionAccounting($pct, $sa, $contract->company_id, ...)` (TNST=13/TNSQ=14), `riskFundAccounting($pct, $sa, $contract->company_id, ...)` (RRP=6). Tính `$gross/$gross_vat/$sale_invoice/$sa/%` bám cách `prepareData` của ProductExportPostingService (đọc giá bán = price+extra_price, qty, vat_percent, giảm giá...). Nếu công thức % ERP bán-mượn khác → theo ERP `FirmContractBorrowSellService`, ghi rõ report.

## Các bước (TDD)
### Step 1 — Viết test nhánh Firm (fail trước)
```php
// Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php
namespace Modules\Finance\Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Modules\Finance\Services\BorrowSell\BorrowSellPostingService;
use Modules\Finance\Entities\BorrowSell\BorrowSell;

class BorrowSellPostingFirmTest extends TestCase
{
    use DatabaseTransactions;

    public function test_firm_branch_credits_157_for_cost()
    {
        $bs = $this->makeFirmBorrowSellFixture(); // xem ghi chú dưới
        [$ok, $accounts, $msg] = app(BorrowSellPostingService::class)->getDataAccounting($bs);
        $this->assertTrue($ok, $msg);

        $cost157 = collect($accounts)->first(fn($a) => $a['number'] == '157' && $a['type'] == 2);
        $cost632 = collect($accounts)->first(fn($a) => $a['number'] == '632' && $a['type'] == 1);
        $this->assertNotNull($cost157, 'Phải có Có 157 (giá vốn hàng gửi bán)');
        $this->assertNotNull($cost632, 'Phải có Nợ 632');
        $this->assertEqualsWithDelta($cost157['value'], $cost632['value'], 0.01);

        $this->assertEqualsWithDelta(
            collect($accounts)->where('type',1)->sum('value'),
            collect($accounts)->where('type',2)->sum('value'),
            1.0, 'Nợ phải cân Có'
        );
    }
}
```
> **`makeFirmBorrowSellFixture()`** — ưu tiên cách ÍT tốn công & ổn định: chọn 1 HĐ Firm THẬT trong DB gộp có `support_accounting`, dựng 1 `BorrowSell` in-memory (`new BorrowSell([...])`, set `contractable_type=BorrowSell::CONTRACT_FIRM`, `contractable_id=<id HĐ Firm thật>`) + gán quan hệ `products` bằng collection 1 `BorrowSellProduct` in-memory (`qty`, `unit_coefficient`, `export_price`, `price`, `extra_price`, `vat_percent`) — KHÔNG cần lưu DB nếu `getDataAccounting` chỉ đọc. Nếu `getDataAccounting`/trait BẮT BUỘC bản ghi thật (vd query lại từ DB) → tạo bản ghi tối thiểu trong `DatabaseTransactions` rồi rollback. Nếu không tìm được HĐ Firm phù hợp → `markTestSkipped` kèm lý do (đừng để test đỏ vì thiếu data).

### Step 2 — Chạy, kỳ vọng FAIL (class not found)
`php vendor/bin/phpunit --filter=BorrowSellPostingFirmTest`

### Step 3 — Viết `BorrowSellPostingService` + `firmBranch` + `resolveContract`
Port từ ERP `FirmContractBorrowSellService`, nhái cấu trúc `getDataProductExportAccounting`. `postAccounting` gọi `getDataAccounting` rồi `saveAccountDetail` trong `DB::transaction` (xem cách ProductExportPostingService::postAccounting). `getDataAccounting` rẽ nhánh: `contractable_type == CONTRACT_FIRM` → `firmBranch`; type khác (WrService) → tạm trả `[false, [], 'Nhánh WrService chưa hỗ trợ (Task 5)']` (Task 5 sẽ bổ sung — KHÔNG tự làm WrService ở task này).

### Step 4 — Chạy, kỳ vọng PASS
`php vendor/bin/phpunit --filter=BorrowSellPostingFirmTest`

### Step 5 — Commit (2 file)
```bash
git add Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php
git commit -m "feat(finance): BorrowSellPostingService nhánh FirmContract (giá vốn TK157 + doanh thu + cụm hỗ trợ)"
```

## Báo cáo
Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-4-report.md`: kết quả 2 bước điều tra (resolveContract nạp HĐ ra sao, công thức giá vốn), shape `getDataAccounting`, cách dựng fixture, kết quả test (giá trị 157/632, tổng Nợ/Có), commit hash. Trả về CHAT chỉ: status, commit hash, 1 dòng tóm tắt, concern.

## KHÔNG được làm
- KHÔNG làm nhánh WrService (để Task 5). KHÔNG sửa trait/ProductExportPostingService.
- KHÔNG đổi tên method trait. KHÔNG dùng cột `borrow_sell_qty` (dùng `qty`).
- KHÔNG dispatch subagent, migration, mysql2, git network op.
