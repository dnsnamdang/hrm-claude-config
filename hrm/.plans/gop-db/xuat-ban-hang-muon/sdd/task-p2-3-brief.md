# Task P2-3: Tách `SupportAccountingTrait` từ `ProductExportPostingService` — Brief (verbatim)

Đây là requirements của bạn. Đọc file này trước, dùng đúng giá trị verbatim.

## Bối cảnh
Feature "xuất bán hàng mượn" Phase 2 (HRM, Laravel 8/PHP 7.4, nhánh `gop_db`, DB gộp `erp_hrm_check`). Repo: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api`.
Đây là task **RỦI RO NHẤT**: refactor **service dùng chung** `ProductExportPostingService` (hạch toán XUẤT HÀNG thường) — tách 13 method hạch toán cụm + 2 property cache thành `SupportAccountingTrait` để Task 4-5 (`BorrowSellPostingService`) tái dùng. **User đã duyệt** việc sửa service dùng chung này (Hướng A).

**MỤC TIÊU SỐNG CÒN:** hành vi hạch toán xuất hàng thường KHÔNG được đổi 1 ly. Đây là **di chuyển NGUYÊN VĂN** (cut-paste), KHÔNG sửa logic, KHÔNG "tiện tay" cải tiến. Bút toán sinh ra trước/sau refactor phải y hệt.

## Ràng buộc toàn cục (bắt buộc)
- Nhánh `gop_db`: KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2`. KHÔNG migration.
- KHÔNG đọc `vendor/`, `node_modules/`. Làm việc tiếng Việt.
- Task kết thúc bằng đúng 1 commit trong phạm vi 3 file (Step 6).
- **CẤM TUYỆT ĐỐI git network/rewrite:** KHÔNG pull/push/fetch/rebase/reset --hard/merge. CHỈ `git add <path>` + `git commit`. Gặp xung đột/cần sync → DỪNG, báo NEEDS_CONTEXT.
- KHÔNG tự dispatch subagent (kể cả reviewer).
- **Chạy test bằng `php vendor/bin/phpunit --filter=<Name>`** — KHÔNG dùng `php artisan test` (lỗi TTY trong env này).

## Files
- Create: `Modules/Assign/Services/Accounting/SupportAccountingTrait.php`
- Modify: `Modules/Assign/Services/ProductExportPostingService.php`
- Test: `Modules/Assign/Tests/Feature/ProductExportPostingRegressionTest.php`

## Sự thật đã VERIFY (dùng làm chuẩn — đừng verify lại tốn công, chỉ đọc để nắm)
File `Modules/Assign/Services/ProductExportPostingService.php` (660 dòng, namespace `Modules\Assign\Services`) hiện có:
- **13 method cần DI CHUYỂN NGUYÊN VĂN vào trait** (đúng signature verbatim, đều `private`):
  - dòng 354 `revenueAccounting($total_price, $vat_cost, Contract $contract, array &$accounts, int &$group): void`
  - dòng 366 `revenueDeductionAccounting($sale_invoice, $sale_invoice_vat, Contract $contract, array &$accounts, int &$group): void`
  - dòng 414 `bonusContractAccounting($percent, $sa, Contract $contract, array &$accounts, int &$group): ?string`
  - dòng 461 `vatExtraCostAccounting($percent, $sa, Contract $contract, array &$accounts, int &$group): ?string` **(cụm TNCN — KHÔNG đổi tên)**
  - dòng 508 `monthlyAndQuarterlyCommissionAccounting($percent, $sa, $contractCompanyId, array &$accounts, int &$group): ?string`
  - dòng 570 `riskFundAccounting($percent, $sa, $contractCompanyId, array &$accounts, int &$group): void`
  - dòng 589 `dept(int $id)`
  - dòng 600 `deptLeadId(int $id): ?int`
  - dòng 606 `deptCompany(int $id): ?int`
  - dòng 612 `deptName(int $id): string`
  - dòng 618 `partLeadId($partId): ?int`
  - dòng 632 `objectableDeptId($department): ?int`
  - dòng 649 `objColumnFor($type): string`
- **2 property cache PHẢI DI CHUYỂN KÈM vào trait** (dòng 49-50): `private $deptCache = [];` và `private $partCache = [];`. Đã verify: 2 cache này CHỈ được 3 helper `dept()`/`partLeadId()`/`objectableDeptId()` (nằm trong 13 method di chuyển) tham chiếu — KHÔNG method nào còn lại trong class dùng → chuyển theo là sạch, không để lại property mồ côi.
- **Method Ở LẠI class** (KHÔNG đụng): `postAccounting`, `postParentImportAccounting`, `postArrangeDeliveryAccounting`, `getDataProductExportAccounting`, `prepareData`, `costAccounting`, `costAccountingProduction`.
- Import ở đầu file gồm: `use Modules\Assign\Entities\Warehouse\ProductExport;` (dòng 7), `use Modules\Assign\Entities\Contract\Contract;` (dòng 12), `use Modules\Finance\Entities\Account\AccountDetail;` (dòng 13), `use Illuminate\Support\Facades\DB;` (dòng 6), `use Carbon\Carbon;` (dòng 5).

### CHÚ Ý import cho trait
Trait dùng `Contract`, `DB`, có thể `Carbon`, `AccountDetail`... tuỳ thân method. Sau khi cắt method sang trait, **thêm đủ `use` (import) các class mà thân method trait tham chiếu** vào đầu file trait (namespace `Modules\Assign\Services\Accounting`). Đừng để trait thiếu import → fatal. Cách chắc: đọc thân 13 method, liệt kê class/facade chúng gọi, import đúng bấy nhiêu.

## Interfaces phải PRODUCE
- `trait SupportAccountingTrait` (namespace `Modules\Assign\Services\Accounting`) chứa: 2 property `$deptCache`/`$partCache` + 13 method trên, **giữ nguyên visibility `private`, nguyên tham chiếu `&$accounts`/`&$group`, thân hàm không đổi 1 ký tự.**
- `ProductExportPostingService` `use Modules\Assign\Services\Accounting\SupportAccountingTrait;` + `use SupportAccountingTrait;` trong thân class; đã xoá 13 method + 2 property đã chuyển; hành vi không đổi.
- (Task 4-5 sẽ `use SupportAccountingTrait` trong `BorrowSellPostingService`.)

## Các bước (TDD — regression chốt trước/sau)
### Step 1 — Viết regression test chốt hành vi HIỆN TẠI
```php
// Modules/Assign/Tests/Feature/ProductExportPostingRegressionTest.php
namespace Modules\Assign\Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Modules\Assign\Services\ProductExportPostingService;
use Modules\Assign\Entities\Warehouse\ProductExport; // ĐÚNG namespace (Warehouse, KHÔNG phải ProductExport\)

class ProductExportPostingRegressionTest extends TestCase
{
    use DatabaseTransactions;

    public function test_post_accounting_snapshot_stable()
    {
        $pxh = ProductExport::whereNotNull('id')->orderByDesc('id')->first();
        if (!$pxh) {
            $this->markTestSkipped('Không có ProductExport trong DB để snapshot.');
        }
        $svc = app(ProductExportPostingService::class);
        $data = $svc->getDataProductExportAccounting($pxh); // trả mảng $accounts, KHÔNG ghi DB
        $sumDept = collect($data)->where('type', 1)->sum('value');
        $sumHas  = collect($data)->where('type', 2)->sum('value');
        $this->assertEqualsWithDelta($sumDept, $sumHas, 1.0, 'Nợ phải cân Có');
        $this->assertNotEmpty($data);
    }
}
```
> Nếu `getDataProductExportAccounting($pxh)` ném lỗi vì PXH mới nhất không gắn HĐ hợp lệ: đổi sang chọn PXH gắn HĐ hợp lệ (ví dụ lọc theo cột contract_id/liên kết HĐ mà bạn thấy trong entity ProductExport), hoặc nếu vẫn không có dữ liệu phù hợp → gọi trực tiếp 1 method cụm (vd `bonusContractAccounting`) qua reflection với `$accounts`/`$group` tham chiếu và assert cấu trúc dòng. Mục tiêu là **so khớp trước/sau refactor**, không phải giá trị tuyệt đối. GHI baseline (số dòng + tổng Nợ/Có) vào report.

### Step 2 — Chạy trên code CŨ, kỳ vọng PASS
`php vendor/bin/phpunit --filter=ProductExportPostingRegressionTest`
Ghi output (số dòng data, tổng Nợ, tổng Có) làm **baseline** vào report.

### Step 3 — Tạo trait, di chuyển NGUYÊN VĂN
Tạo `Modules/Assign/Services/Accounting/SupportAccountingTrait.php`:
```php
<?php
namespace Modules\Assign\Services\Accounting;

use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Contract\Contract;
use Modules\Finance\Entities\Account\AccountDetail;
// + thêm import khác nếu thân method cần (Carbon, ...)

trait SupportAccountingTrait
{
    private $deptCache = [];
    private $partCache = [];

    // <13 method cắt nguyên văn từ ProductExportPostingService, giữ private + &$accounts/&$group + thân không đổi>
}
```
CẮT (không copy-để-lại) 2 property + 13 method khỏi service.

### Step 4 — `use` trait trong service
Trong `ProductExportPostingService.php`: thêm import `use Modules\Assign\Services\Accounting\SupportAccountingTrait;`, và `use SupportAccountingTrait;` ngay sau `class ProductExportPostingService {`. Xác nhận: không còn định nghĩa trùng 13 method, không còn khai 2 property đã chuyển, không còn import thừa (nếu service không còn dùng class nào sau khi cắt thì cứ để import — KHÔNG bắt buộc dọn, tránh rủi ro).

### Step 5 — Chạy lại regression, kỳ vọng PASS + KHỚP baseline
`php vendor/bin/phpunit --filter=ProductExportPostingRegressionTest`
Expected: PASS, tổng Nợ/Có + số dòng == baseline Step 2. Nếu LỆCH → refactor sai (bạn đã đổi hành vi), soi lại phần cắt/dán. Ghi kết quả so khớp vào report.

### Step 6 — Commit (chỉ 3 file)
```bash
git add Modules/Assign/Services/Accounting/SupportAccountingTrait.php Modules/Assign/Services/ProductExportPostingService.php Modules/Assign/Tests/Feature/ProductExportPostingRegressionTest.php
git commit -m "refactor(assign): tách SupportAccountingTrait dùng chung cho hạch toán xuất hàng + bán hàng mượn"
```

## Báo cáo
Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-3-report.md`: baseline Step 2 (số dòng + tổng Nợ/Có), kết quả Step 5 (khớp/lệch), danh sách import đã thêm vào trait, xác nhận 2 property đã chuyển, commit hash. Trả về CHAT chỉ: status, commit hash, 1 dòng tóm tắt (baseline khớp?), concern nếu có.

## KHÔNG được làm
- KHÔNG sửa logic/thân method (chỉ di chuyển). KHÔNG đổi tên method (nhất là `vatExtraCostAccounting`).
- KHÔNG đụng 7 method ở lại (postAccounting/prepareData/costAccounting...).
- KHÔNG dispatch subagent, KHÔNG migration, KHÔNG mysql2, KHÔNG git network op.
- KHÔNG "tiện tay" refactor gì khác trong service.
