# Task 1 brief

## Task 1: Migration `regulation_scheduled_versions`

**Files:**
- Create: `Modules/MasterData/Database/Migrations/2026_09_12_000001_create_regulation_scheduled_versions_table.php`

**Interfaces:**
- Produces: bảng `regulation_scheduled_versions` với cột: `id, scope_type, scope_id, tab_key, effective_date, status, payload(json), diff_snapshot(json null), note, created_by, updated_by, created_at, updated_at, applied_at`. Index `(scope_type, scope_id, tab_key, status, effective_date)`.

- [ ] **Step 1: Viết migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateRegulationScheduledVersionsTable extends Migration
{
    public function up()
    {
        if (Schema::hasTable('regulation_scheduled_versions')) {
            return;
        }
        Schema::create('regulation_scheduled_versions', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('scope_type', 20);            // company | department | part
            $table->unsignedBigInteger('scope_id');
            $table->string('tab_key', 50);               // congno, baogia, ...
            $table->date('effective_date');
            $table->string('status', 20)->default('pending'); // pending | applied | canceled
            $table->json('payload');                     // toàn bộ giá trị mới của tab (nguồn chân lý)
            $table->json('diff_snapshot')->nullable();   // [{key,label,old,new,unit}] chỉ để hiển thị
            $table->string('note', 500)->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();
            $table->timestamp('applied_at')->nullable();
            $table->index(
                ['scope_type', 'scope_id', 'tab_key', 'status', 'effective_date'],
                'rsv_scope_tab_status_date_idx'
            );
        });
    }

    public function down()
    {
        Schema::dropIfExists('regulation_scheduled_versions');
    }
}
```

- [ ] **Step 2: Chạy migration**

Run: `cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api && php artisan migrate --path=Modules/MasterData/Database/Migrations/2026_09_12_000001_create_regulation_scheduled_versions_table.php`
Expected: "Migrated" không lỗi. (Trước khi chạy: `grep DB_ .env` xác nhận trỏ DB gộp local, không phải prod.)

- [ ] **Step 3: Verify bảng tồn tại**

Run: `php artisan tinker --execute="echo \Schema::hasTable('regulation_scheduled_versions') ? 'OK' : 'MISSING';"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add Modules/MasterData/Database/Migrations/2026_09_12_000001_create_regulation_scheduled_versions_table.php
git commit -m "feat(masterdata): create regulation_scheduled_versions table"
```
(Chỉ commit khi người dùng đã cho phép — nếu chưa, bỏ qua step commit ở mọi task.)

---

