> ## ⚠️ NƠI LÀM VIỆC — WORKTREE (chốt 17/09/2026, user yêu cầu)
>
> Nhánh `gop_db` đang được một phiên làm việc khác dùng → mọi thay đổi code của plan này làm trong
> **worktree riêng**, nhánh `feat/quan-ly-phong-hop`:
>
> | Thứ | Đường dẫn |
> |---|---|
> | Repo BE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api` |
> | Repo FE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-client` |
> | Bộ e2e | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e` (DÙNG CHUNG, không có worktree) |
> | Tài liệu (plan, ledger) | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-phong-hop/` |
>
> - API của worktree chạy ở **`http://127.0.0.1:8001`**, Nuxt của worktree ở **`http://127.0.0.1:3001`**.
>   Cổng 8000/3000 là server của phiên khác — **KHÔNG đụng, KHÔNG tắt, KHÔNG `pkill`**.
> - Chạy e2e phải truyền cả 2 biến: `BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001`.
> - Phiên đăng nhập của Playwright gắn theo ORIGIN. `.auth/user.json` chỉ dùng được cho `:3000` → đã tạo sẵn
>   **`.auth/user-wt.json`** (admin) và **`.auth/user-nocost-wt.json`** (tài khoản thiếu quyền) với origin
>   đổi sang `:3001`. Spec UI phải khai `test.use({ storageState: '.auth/user-wt.json' })`, KHÔNG dùng
>   `user.json` (dùng nhầm là bị đẩy về `/login`, rất dễ tưởng lỗi đăng nhập).
> - TUYỆT ĐỐI KHÔNG `git commit` / `push` / `stash` / `checkout` file.
> - Worktree KHÔNG có `.plans`, `.claude`, `docs`, `CLAUDE.md` (là symlink ngoài repo) — tài liệu ghi về
>   đường dẫn tài liệu ở bảng trên.
> - Đường dẫn trong phần dưới ghi `hrm-api/...` hay `hrm-client/...` thì hiểu là **thư mục tương ứng trong
>   worktree**, không phải checkout gốc.

## Task 2: Migration 6 bảng + 2 alter

**Files:**
- Create: `hrm-api/Modules/Meeting/Database/Migrations/2026_09_17_000001_create_meeting_room_amenities_table.php`
- Create: `…000002_create_meeting_rooms_table.php`
- Create: `…000003_create_meeting_room_room_amenity_table.php`
- Create: `…000004_create_meeting_room_bookings_table.php`
- Create: `…000005_create_meeting_room_booking_participants_table.php`
- Create: `…000006_create_meeting_room_booking_recurrences_table.php`
- Create: `…000007_add_meeting_room_id_to_meetings_table.php`
- Create: `…000008_add_meeting_room_config_to_general_regulations_table.php`

**Interfaces:**
- Produces: 6 bảng mới, cột `meetings.meeting_room_id`, 5 cột cấu hình trong `general_regulations`

> Tạo **cả 6 bảng ngay phase 1** (kể cả bảng booking chưa dùng tới) vì `MeetingRoom::isCanDelete()`
> ở Task 4 phải truy vấn `meeting_room_bookings`.

- [ ] **Bước 1: Viết migration bảng tiện nghi**

```php
Schema::create('meeting_room_amenities', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->string('code', 50)->unique();
    $table->string('name', 255);
    $table->string('icon', 100)->nullable();
    $table->integer('sort_order')->default(0);
    $table->tinyInteger('status')->default(1)->comment('1 Hoạt động, 2 Khóa');
    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->timestamps();
});
```

- [ ] **Bước 2: Viết migration bảng phòng họp**

```php
Schema::create('meeting_rooms', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->string('code', 50);
    $table->string('name', 255);
    $table->unsignedBigInteger('company_id');
    $table->unsignedBigInteger('department_id')->nullable();
    $table->unsignedBigInteger('part_id')->nullable();
    $table->tinyInteger('allow_cross_company')->default(0);
    $table->string('location', 255)->nullable();
    $table->integer('capacity')->nullable();
    $table->unsignedBigInteger('manager_employee_id')->nullable();
    $table->tinyInteger('require_approval')->default(0);
    $table->time('open_time')->nullable();
    $table->time('close_time')->nullable();
    $table->integer('checkin_grace_minutes')->nullable();
    $table->char('checkin_qr_token', 36)->nullable()->unique();
    $table->text('description')->nullable();
    $table->tinyInteger('status')->default(1)->comment('1 Hoạt động, 2 Khóa');
    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->timestamps();

    $table->unique(['company_id', 'code']);
    $table->index(['company_id', 'status']);
});
```

- [ ] **Bước 3: Viết migration pivot**

```php
Schema::create('meeting_room_room_amenity', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->unsignedBigInteger('meeting_room_id');
    $table->unsignedBigInteger('meeting_room_amenity_id');
    $table->integer('quantity')->default(1);
    $table->string('note', 255)->nullable();
    $table->unique(['meeting_room_id', 'meeting_room_amenity_id'], 'mr_amenity_unique');
});
```

- [ ] **Bước 4: Viết migration bảng phiếu đặt phòng**

Đủ cột theo spec mục 4.4 (`code`, `meeting_room_id`, `title`, `content`, `start_at`, `end_at`,
`status`, `booked_by_employee_id`, `host_employee_id`, `attendee_count`, `company_id`,
`department_id`, `meeting_id` unique nullable, `source`, `approved_by`, `approved_at`,
`reject_reason`, `is_auto_rejected`, `cancelled_by`, `cancelled_at`, `cancel_reason`,
`checkin_at`, `checkout_at`, `auto_released_at`, `checkout_reminded_at`, `recurrence_id`,
`created_by`, `updated_by`, `timestamps`) kèm index:

```php
$table->index(['meeting_room_id', 'start_at', 'end_at'], 'mrb_room_time_index');
$table->index('status');
$table->index('booked_by_employee_id');
$table->unique('meeting_id');
$table->index('recurrence_id');
```

- [ ] **Bước 5: Viết 2 migration còn lại + 2 alter**

```php
// participants
Schema::create('meeting_room_booking_participants', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->unsignedBigInteger('meeting_room_booking_id');
    $table->unsignedBigInteger('employee_id');
    $table->timestamps();
    $table->unique(['meeting_room_booking_id', 'employee_id'], 'mrbp_unique');
});

// meetings
Schema::table('meetings', function (Blueprint $table) {
    $table->unsignedBigInteger('meeting_room_id')->nullable()->after('location');
});

// general_regulations
Schema::table('general_regulations', function (Blueprint $table) {
    $table->time('meeting_room_open_time')->nullable()->default('07:00:00');
    $table->time('meeting_room_close_time')->nullable()->default('20:00:00');
    $table->integer('meeting_room_checkin_grace_minutes')->nullable()->default(15);
    $table->integer('meeting_room_checkout_reminder_minutes')->nullable()->default(10);
    $table->integer('meeting_room_max_advance_days')->nullable()->default(90);
});
```

Bảng `meeting_room_booking_recurrences` theo spec mục 4.6.

- [ ] **Bước 6: Chạy migration**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan config:clear
/opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=Modules/Meeting/Database/Migrations
```
Kỳ vọng: 8 migration chạy OK, không lỗi.

- [ ] **Bước 7: Kiểm bảng có thật + đúng index**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" hrm_erp -e "SHOW CREATE TABLE meeting_room_bookings\G" | grep -i "KEY"
```
Kỳ vọng: thấy `mrb_room_time_index (meeting_room_id, start_at, end_at)` và unique `meeting_id`.

- [ ] **Bước 8: Kiểm rollback không hỏng**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan migrate:rollback --path=Modules/Meeting/Database/Migrations --step=8
/opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=Modules/Meeting/Database/Migrations
```
Kỳ vọng: rollback sạch rồi migrate lại được (mọi `down()` phải `dropColumn`/`dropIfExists` đúng).

---
