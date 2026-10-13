# Task P2-2: Entity ActivityHasDeliveryTrip — Brief (requirements, dùng verbatim)

Đây là requirements của bạn. Đọc file này trước, dùng đúng các giá trị verbatim.

## Bối cảnh
Feature "xuất bán hàng mượn" Phase 2 (nhánh `gop_db`, DB gộp `erp_hrm_check`). Task này tạo 1 Eloquent entity map bảng `activity_has_delivery_trips` ĐÃ TỒN TẠI trong DB (KHÔNG viết migration). Entity này sẽ được task sau (T6 hạch toán chuyến xe giao hàng) dùng để nối `warehouse_export` → chuyến xe (`DeliveryTrip`). Repo: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api`.

## Ràng buộc toàn cục (bắt buộc)
- Nhánh `gop_db`: KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2`/`env('DB_DATABASE_SECOND')`. Bảng trùng tên ưu tiên bản ERP.
- KHÔNG commit khi chưa được yêu cầu — NHƯNG task này KẾT THÚC bằng 1 commit (đúng quy trình SDD, xem Step 6). Chỉ commit trong phạm vi file của task.
- KHÔNG đọc `vendor/`, `node_modules/`.
- Làm việc tiếng Việt.
- **CẤM TUYỆT ĐỐI mọi thao tác git network / rewrite lịch sử:** KHÔNG `git pull`, `git push`, `git fetch`, `git rebase`, `git reset --hard`, `git merge`. CHỈ được `git add <path cụ thể>` + `git commit`. Nếu thấy cần sync/gặp xung đột → DỪNG, báo NEEDS_CONTEXT, KHÔNG tự xử lý.

## Files
- Create: `Modules/Finance/Entities/Delivery/ActivityHasDeliveryTrip.php`
- Test: `Modules/Finance/Tests/Unit/ActivityHasDeliveryTripEntityTest.php`

## Mẫu bám theo (ĐỌC trước khi viết)
- `Modules/Finance/Entities/Delivery/DeliveryTrip.php` (cùng thư mục đích) — copy pattern namespace, khai báo class, quy ước HRM.
- `Modules/Finance/Entities/BorrowSell/BorrowSell.php` (Task 1 vừa xong) — pattern `$guarded=[]`, relation belongsTo.

## Nguồn ERP để đối chiếu logic (chỉ đọc)
`/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/TanPhatDev/app/Model/Warehouse/ActivityHasDeliveryTrip.php`:
```php
class ActivityHasDeliveryTrip extends Model {
    public function trip () {
        return $this->belongsTo('App\Model\Warehouse\DeliveryTrip', 'delivery_trip_id','id');
    }
    // ... còn warehouse_export/warehouse_import/vehicle... — KHÔNG cần port ở task này
}
```
Ở HRM ta CHỈ cần relation `trip()` (T6 dùng). KHÔNG port các relation khác (không cần cho Phase 2).

## Cột thật đã verify (DB gộp `erp_hrm_check`, dùng làm chuẩn)
Bảng `activity_has_delivery_trips` có (trích cột liên quan): `id` (bigint unsigned PK), `warehouse_export_id`, `warehouse_import_id`, `delivery_trip_id` (NOT NULL), `total_cost_transition` (decimal(16,2)), `created_at`, `updated_at`, ... → dùng `$guarded=[]`, KHÔNG cần khai `$fillable`.

## Interfaces phải PRODUCE (task sau T6 phụ thuộc — đúng tên/chữ ký)
- Class `Modules\Finance\Entities\Delivery\ActivityHasDeliveryTrip` extends `Illuminate\Database\Eloquent\Model`.
- `protected $table = 'activity_has_delivery_trips';` (khai tường minh cho chắc, vì đặt trong thư mục `Delivery`).
- `protected $guarded = [];`
- `public function trip()` → `belongsTo(\Modules\Finance\Entities\Delivery\DeliveryTrip::class, 'delivery_trip_id', 'id')`.

## Các bước (TDD)
### Step 1 — Verify tên bảng + entity chưa tồn tại (BẮT BUỘC trước khi code)
```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
mysql -h127.0.0.1 -uroot erp_hrm_check -N -e "SHOW TABLES LIKE '%delivery_trip%';"
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM activity_has_delivery_trips;"
# Xác nhận entity CHƯA có (nếu đã có -> SKIP, báo status DONE với ghi chú "đã tồn tại"):
grep -rn "class ActivityHasDeliveryTrip" Modules/ app/ 2>/dev/null
```
Nếu bảng đã đổi tên hoặc entity đã tồn tại → DỪNG, báo NEEDS_CONTEXT (không tự đoán).

### Step 2 — Viết test (fail trước)
```php
// Modules/Finance/Tests/Unit/ActivityHasDeliveryTripEntityTest.php
namespace Modules\Finance\Tests\Unit;

use Tests\TestCase;
use Modules\Finance\Entities\Delivery\ActivityHasDeliveryTrip;
use Modules\Finance\Entities\Delivery\DeliveryTrip;

class ActivityHasDeliveryTripEntityTest extends TestCase
{
    public function test_table_name_is_activity_has_delivery_trips()
    {
        $this->assertEquals('activity_has_delivery_trips', (new ActivityHasDeliveryTrip())->getTable());
    }

    public function test_trip_relation_points_to_delivery_trip()
    {
        $rel = (new ActivityHasDeliveryTrip())->trip();
        $this->assertInstanceOf(\Illuminate\Database\Eloquent\Relations\BelongsTo::class, $rel);
        $this->assertInstanceOf(DeliveryTrip::class, $rel->getRelated());
        $this->assertEquals('delivery_trip_id', $rel->getForeignKeyName());
    }
}
```

### Step 3 — Chạy test, kỳ vọng FAIL
`php artisan test --filter=ActivityHasDeliveryTripEntityTest` → FAIL (class not found).

### Step 4 — Viết entity
Namespace `Modules\Finance\Entities\Delivery;`, extend `Illuminate\Database\Eloquent\Model`, khai `$table`, `$guarded=[]`, relation `trip()` như Interfaces.

### Step 5 — Chạy test, kỳ vọng PASS
`php artisan test --filter=ActivityHasDeliveryTripEntityTest` → PASS.

### Step 6 — Commit (chỉ file của task)
```bash
git add Modules/Finance/Entities/Delivery/ActivityHasDeliveryTrip.php Modules/Finance/Tests/Unit/ActivityHasDeliveryTripEntityTest.php
git commit -m "feat(finance): thêm entity ActivityHasDeliveryTrip (Phase 2 hạch toán chuyến xe)"
```

## Báo cáo
Ghi report đầy đủ vào `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-2-report.md` (cột thật verify, kết quả test, commit hash). Trả về CHAT chỉ: status (DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT), commit hash, 1 dòng tóm tắt test, concern nếu có.

## KHÔNG được làm
- KHÔNG tự dispatch subagent khác (kể cả reviewer).
- KHÔNG viết migration.
- KHÔNG đụng file ngoài phạm vi task.
- KHÔNG dùng mysql2/DB_CONNECTION_SECOND.
- KHÔNG mọi git network op (xem Ràng buộc toàn cục).
