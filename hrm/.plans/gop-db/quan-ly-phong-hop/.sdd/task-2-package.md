# Review package — Task 2 (migration, worktree phong-hop-api)

## git status
 M modules_statuses.json
?? Modules/Meeting/

## Nội dung 8 migration

### Modules/Meeting/Database/Migrations/2026_09_17_000001_create_meeting_room_amenities_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMeetingRoomAmenitiesTable extends Migration
{
    public function up()
    {
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
    }

    public function down()
    {
        Schema::dropIfExists('meeting_room_amenities');
    }
}
```

### Modules/Meeting/Database/Migrations/2026_09_17_000002_create_meeting_rooms_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMeetingRoomsTable extends Migration
{
    public function up()
    {
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
    }

    public function down()
    {
        Schema::dropIfExists('meeting_rooms');
    }
}
```

### Modules/Meeting/Database/Migrations/2026_09_17_000003_create_meeting_room_room_amenity_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMeetingRoomRoomAmenityTable extends Migration
{
    public function up()
    {
        Schema::create('meeting_room_room_amenity', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('meeting_room_id');
            $table->unsignedBigInteger('meeting_room_amenity_id');
            $table->integer('quantity')->default(1);
            $table->string('note', 255)->nullable();
            $table->unique(['meeting_room_id', 'meeting_room_amenity_id'], 'mr_amenity_unique');
        });
    }

    public function down()
    {
        Schema::dropIfExists('meeting_room_room_amenity');
    }
}
```

### Modules/Meeting/Database/Migrations/2026_09_17_000004_create_meeting_room_bookings_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMeetingRoomBookingsTable extends Migration
{
    public function up()
    {
        Schema::create('meeting_room_bookings', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('code', 50);
            $table->unsignedBigInteger('meeting_room_id');
            $table->string('title', 255);
            $table->text('content')->nullable();
            $table->dateTime('start_at');
            $table->dateTime('end_at');
            $table->tinyInteger('status')->comment('1 Chờ duyệt, 2 Đã duyệt, 3 Từ chối, 4 Đã hủy, 5 Hoàn thành');
            $table->unsignedBigInteger('booked_by_employee_id');
            $table->unsignedBigInteger('host_employee_id')->nullable();
            $table->integer('attendee_count')->nullable();
            $table->unsignedBigInteger('company_id')->nullable();
            $table->unsignedBigInteger('department_id')->nullable();
            $table->unsignedBigInteger('meeting_id')->nullable();
            $table->tinyInteger('source')->default(1)->comment('1 Tự đặt, 2 Sinh từ Meeting');
            $table->unsignedBigInteger('approved_by')->nullable();
            $table->dateTime('approved_at')->nullable();
            $table->string('reject_reason', 500)->nullable();
            $table->tinyInteger('is_auto_rejected')->default(0);
            $table->unsignedBigInteger('cancelled_by')->nullable();
            $table->dateTime('cancelled_at')->nullable();
            $table->string('cancel_reason', 500)->nullable();
            $table->dateTime('checkin_at')->nullable();
            $table->dateTime('checkout_at')->nullable();
            $table->dateTime('auto_released_at')->nullable();
            $table->dateTime('checkout_reminded_at')->nullable();
            $table->unsignedBigInteger('recurrence_id')->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();

            $table->index(['meeting_room_id', 'start_at', 'end_at'], 'mrb_room_time_index');
            $table->index('status');
            $table->index('booked_by_employee_id');
            $table->unique('meeting_id');
            $table->index('recurrence_id');
        });
    }

    public function down()
    {
        Schema::dropIfExists('meeting_room_bookings');
    }
}
```

### Modules/Meeting/Database/Migrations/2026_09_17_000005_create_meeting_room_booking_participants_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMeetingRoomBookingParticipantsTable extends Migration
{
    public function up()
    {
        Schema::create('meeting_room_booking_participants', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('meeting_room_booking_id');
            $table->unsignedBigInteger('employee_id');
            $table->timestamps();
            $table->unique(['meeting_room_booking_id', 'employee_id'], 'mrbp_unique');
        });
    }

    public function down()
    {
        Schema::dropIfExists('meeting_room_booking_participants');
    }
}
```

### Modules/Meeting/Database/Migrations/2026_09_17_000006_create_meeting_room_booking_recurrences_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMeetingRoomBookingRecurrencesTable extends Migration
{
    public function up()
    {
        Schema::create('meeting_room_booking_recurrences', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('meeting_room_id');
            $table->string('title', 255);
            $table->text('content')->nullable();
            $table->string('weekdays', 20)->comment('vd 1,3,5 - 1 la Thu 2');
            $table->date('start_date');
            $table->date('end_date');
            $table->time('start_time');
            $table->time('end_time');
            $table->unsignedBigInteger('host_employee_id')->nullable();
            $table->integer('attendee_count')->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('meeting_room_booking_recurrences');
    }
}
```

### Modules/Meeting/Database/Migrations/2026_09_17_000007_add_meeting_room_id_to_meetings_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddMeetingRoomIdToMeetingsTable extends Migration
{
    public function up()
    {
        Schema::table('meetings', function (Blueprint $table) {
            $table->unsignedBigInteger('meeting_room_id')->nullable()->after('location');
        });
    }

    public function down()
    {
        Schema::table('meetings', function (Blueprint $table) {
            $table->dropColumn('meeting_room_id');
        });
    }
}
```

### Modules/Meeting/Database/Migrations/2026_09_17_000008_add_meeting_room_config_to_general_regulations_table.php
```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddMeetingRoomConfigToGeneralRegulationsTable extends Migration
{
    public function up()
    {
        Schema::table('general_regulations', function (Blueprint $table) {
            $table->time('meeting_room_open_time')->nullable()->default('07:00:00');
            $table->time('meeting_room_close_time')->nullable()->default('20:00:00');
            $table->integer('meeting_room_checkin_grace_minutes')->nullable()->default(15);
            $table->integer('meeting_room_checkout_reminder_minutes')->nullable()->default(10);
            $table->integer('meeting_room_max_advance_days')->nullable()->default(90);
        });
    }

    public function down()
    {
        Schema::table('general_regulations', function (Blueprint $table) {
            $table->dropColumn([
                'meeting_room_open_time',
                'meeting_room_close_time',
                'meeting_room_checkin_grace_minutes',
                'meeting_room_checkout_reminder_minutes',
                'meeting_room_max_advance_days',
            ]);
        });
    }
}
```

## Schema THỰC TẾ trong DB (sau rollback + migrate lại, do người điều phối chạy)
```sql
*************************** 1. row ***************************
       Table: meeting_rooms
Create Table: CREATE TABLE `meeting_rooms` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_id` bigint unsigned NOT NULL,
  `department_id` bigint unsigned DEFAULT NULL,
  `part_id` bigint unsigned DEFAULT NULL,
  `allow_cross_company` tinyint NOT NULL DEFAULT '0',
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `capacity` int DEFAULT NULL,
  `manager_employee_id` bigint unsigned DEFAULT NULL,
  `require_approval` tinyint NOT NULL DEFAULT '0',
  `open_time` time DEFAULT NULL,
  `close_time` time DEFAULT NULL,
  `checkin_grace_minutes` int DEFAULT NULL,
  `checkin_qr_token` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '1 Hoạt động, 2 Khóa',
  `created_by` bigint unsigned DEFAULT NULL,
  `updated_by` bigint unsigned DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `meeting_rooms_company_id_code_unique` (`company_id`,`code`),
  UNIQUE KEY `meeting_rooms_checkin_qr_token_unique` (`checkin_qr_token`),
  KEY `meeting_rooms_company_id_status_index` (`company_id`,`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
*************************** 1. row ***************************
       Table: meeting_room_bookings
Create Table: CREATE TABLE `meeting_room_bookings` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `meeting_room_id` bigint unsigned NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text COLLATE utf8mb4_unicode_ci,
  `start_at` datetime NOT NULL,
  `end_at` datetime NOT NULL,
  `status` tinyint NOT NULL COMMENT '1 Chờ duyệt, 2 Đã duyệt, 3 Từ chối, 4 Đã hủy, 5 Hoàn thành',
  `booked_by_employee_id` bigint unsigned NOT NULL,
  `host_employee_id` bigint unsigned DEFAULT NULL,
  `attendee_count` int DEFAULT NULL,
  `company_id` bigint unsigned DEFAULT NULL,
  `department_id` bigint unsigned DEFAULT NULL,
  `meeting_id` bigint unsigned DEFAULT NULL,
  `source` tinyint NOT NULL DEFAULT '1' COMMENT '1 Tự đặt, 2 Sinh từ Meeting',
  `approved_by` bigint unsigned DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `reject_reason` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_auto_rejected` tinyint NOT NULL DEFAULT '0',
  `cancelled_by` bigint unsigned DEFAULT NULL,
  `cancelled_at` datetime DEFAULT NULL,
  `cancel_reason` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `checkin_at` datetime DEFAULT NULL,
  `checkout_at` datetime DEFAULT NULL,
  `auto_released_at` datetime DEFAULT NULL,
  `checkout_reminded_at` datetime DEFAULT NULL,
  `recurrence_id` bigint unsigned DEFAULT NULL,
  `created_by` bigint unsigned DEFAULT NULL,
  `updated_by` bigint unsigned DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `meeting_room_bookings_meeting_id_unique` (`meeting_id`),
  KEY `mrb_room_time_index` (`meeting_room_id`,`start_at`,`end_at`),
  KEY `meeting_room_bookings_status_index` (`status`),
  KEY `meeting_room_bookings_booked_by_employee_id_index` (`booked_by_employee_id`),
  KEY `meeting_room_bookings_recurrence_id_index` (`recurrence_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
*************************** 1. row ***************************
       Table: meeting_room_room_amenity
Create Table: CREATE TABLE `meeting_room_room_amenity` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `meeting_room_id` bigint unsigned NOT NULL,
  `meeting_room_amenity_id` bigint unsigned NOT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mr_amenity_unique` (`meeting_room_id`,`meeting_room_amenity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
Field	Type	Null	Key	Default	Extra
meeting_room_open_time	time	YES		07:00:00	
meeting_room_close_time	time	YES		20:00:00	
meeting_room_checkin_grace_minutes	int	YES		15	
meeting_room_checkout_reminder_minutes	int	YES		10	
meeting_room_max_advance_days	int	YES		90	
Field	Type	Null	Key	Default	Extra
meeting_room_id	bigint unsigned	YES		NULL	
```
