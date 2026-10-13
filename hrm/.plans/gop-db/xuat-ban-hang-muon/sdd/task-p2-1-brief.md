# Task P2-1: 6 Entity BorrowSell* — Brief (requirements, dùng verbatim)

Đây là requirements của bạn. Đọc file này trước, dùng đúng các giá trị verbatim.

## Bối cảnh
Feature "xuất bán hàng mượn" Phase 2 (nhánh `gop_db`, DB gộp `erp_hrm_check`). Đây là task ĐẦU tiên: tạo 6 Eloquent entity map 6 bảng `borrow_sell*` ĐÃ TỒN TẠI trong DB (KHÔNG viết migration). Repo: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api`.

## Ràng buộc toàn cục (bắt buộc)
- Nhánh `gop_db`: KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2`/`env('DB_DATABASE_SECOND')`. Bảng trùng tên ưu tiên bản ERP.
- KHÔNG commit khi chưa được yêu cầu — NHƯNG task này KẾT THÚC bằng 1 commit (đúng quy trình SDD, xem Step 6). Chỉ commit trong phạm vi file của task.
- KHÔNG đọc `vendor/`, `node_modules/`.
- Làm việc tiếng Việt.

## Files
- Create: `Modules/Finance/Entities/BorrowSell/BorrowSell.php` + `BorrowSellProduct.php` + `BorrowSellProductDetail.php` + `BorrowSellTab.php` + `BorrowSellTabProduct.php` + `BorrowSellTabProductDetail.php`
- Test: `Modules/Finance/Tests/Unit/BorrowSellEntityTest.php`

## Mẫu bám theo (ĐỌC trước khi viết)
`Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php` (Phase 1) — copy pattern: const, `$guarded=[]`, relations, `generateCode()`, `canView()` (dùng helper quyền HRM `isCurrentEmployeeHasPermission`). Xem cả các entity con `BorrowSellRequestProduct.php`, `BorrowSellRequestTab.php`... cùng thư mục.

## Nguồn ERP để đối chiếu logic (chỉ đọc)
`/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/TanPhatDev/app/Model/Warehouse/BorrowSell.php` — đặc biệt `generateCode` (`"PXBHM-".generateCode(5,id)`) và `canView` (`can("Kế toán kho") && status!=3 || created_by==auth`).

## Interfaces phải PRODUCE (task sau phụ thuộc — đúng tên/chữ ký)
- `BorrowSell` const: `PREFIX='PXBHM'`, `STATUS_DEFAULT=1`, `PERMISSION_KE_TOAN_KHO='Kế toán kho'`, `CONTRACT_FIRM='App\Model\Sale\Firm\Contract\FirmContract'`, `CONTRACT_WR_SERVICE='App\Model\Customers\WrServiceContract'`.
- `BorrowSell::generateCode(): string` → chuỗi bắt đầu `'PXBHM-'` (pad theo pattern Phase 1).
- `BorrowSell::canView(): bool` → `isCurrentEmployeeHasPermission('Kế toán kho') && status != 3 || created_by == <auth id>` (bám cách Phase 1 `BorrowSellRequest::canView` lấy auth id).
- Relations:
  - `BorrowSell::products()` hasMany `BorrowSellProduct`
  - `BorrowSell::tabs()` hasMany `BorrowSellTab`
  - `BorrowSell::borrowSellRequest()` belongsTo `Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest` (FK verify ở Step 1)
  - `BorrowSellProduct::details()` hasMany `BorrowSellProductDetail`
  - `BorrowSellTab::products()` hasMany `BorrowSellTabProduct`
  - `BorrowSellTabProduct::details()` hasMany `BorrowSellTabProductDetail`

## Các bước (TDD)
### Step 1 — Verify tên bảng + cột (BẮT BUỘC trước khi code)
```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
mysql -h127.0.0.1 -uroot erp_hrm_check -N -e "SHOW TABLES LIKE 'borrow_sell%';"
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM borrow_sells;"
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM borrow_sell_products;"
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM borrow_sell_product_details;"
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM borrow_sell_tabs;"
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM borrow_sell_tab_products;"
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM borrow_sell_tab_product_details;"
```
Ghi lại tên bảng thật + FK (`borrow_sell_id`, `borrow_sell_request_id`, `borrow_sell_product_id`, `borrow_sell_tab_id`, `borrow_sell_tab_product_id`). Nếu HRM đã đổi tên `hrm_borrow_sell*` → khai `protected $table` tường minh (verify bản nào tồn tại; ưu tiên bản ERP nếu cả hai có).

### Step 2 — Viết test (fail trước)
```php
// Modules/Finance/Tests/Unit/BorrowSellEntityTest.php
namespace Modules\Finance\Tests\Unit;

use Tests\TestCase;
use Modules\Finance\Entities\BorrowSell\BorrowSell;
use Modules\Finance\Entities\BorrowSell\BorrowSellProduct;

class BorrowSellEntityTest extends TestCase
{
    public function test_generate_code_has_pxbhm_prefix()
    {
        $this->assertStringStartsWith('PXBHM-', BorrowSell::generateCode());
    }

    public function test_products_relation_defined()
    {
        $this->assertInstanceOf(
            \Illuminate\Database\Eloquent\Relations\HasMany::class,
            (new BorrowSell())->products()
        );
        $this->assertInstanceOf(
            \Illuminate\Database\Eloquent\Relations\HasMany::class,
            (new BorrowSellProduct())->details()
        );
    }
}
```

### Step 3 — Chạy test, kỳ vọng FAIL
`php artisan test --filter=BorrowSellEntityTest` → FAIL (class not found).

### Step 4 — Viết 6 entity
Namespace `Modules\Finance\Entities\BorrowSell;`, extend `Illuminate\Database\Eloquent\Model`, `$guarded=[]`, khai `$table` nếu khác mặc định. `BorrowSell` thêm const + `generateCode()` + `canView()` + relations như Interfaces.

### Step 5 — Chạy test, kỳ vọng PASS
`php artisan test --filter=BorrowSellEntityTest` → PASS.

### Step 6 — Commit (chỉ file của task)
```bash
git add Modules/Finance/Entities/BorrowSell Modules/Finance/Tests/Unit/BorrowSellEntityTest.php
git commit -m "feat(finance): thêm 6 entity BorrowSell (Phase 2 phiếu xuất bán hàng mượn)"
```

## Báo cáo
Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-1-report.md` (tên bảng/cột thật đã verify, quyết định `$table`, kết quả test, commit hash). Trả về CHAT chỉ: status (DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT), commit hash, 1 dòng tóm tắt test, và concern nếu có.

## KHÔNG được làm
- KHÔNG tự dispatch subagent khác (kể cả reviewer).
- KHÔNG viết migration.
- KHÔNG đụng file ngoài phạm vi task.
- KHÔNG dùng mysql2/DB_CONNECTION_SECOND.
