# Plan — Loại meeting "Họp tìm hiểu & Giới thiệu sản phẩm" + Khảo sát nhu cầu đầu tư

> **Cho agent thực thi:** dùng `superpowers:subagent-driven-development` (khuyến nghị) hoặc `superpowers:executing-plans` để làm từng task. Các bước dùng checkbox `- [ ]` để theo dõi.

**Goal:** Thêm loại meeting hệ thống "Họp tìm hiểu & Giới thiệu sản phẩm" (không cho Sửa/Xoá/Khoá) và khối "Khảo sát nhu cầu khách hàng" 3 câu hỏi bắt buộc trong tab Biên bản, hiện cả ở bản In và file Excel.

**Architecture:** Đánh dấu bản ghi danh mục hệ thống bằng cột `meeting_types.code` + whitelist `SYSTEM_CODES`, chặn 423 ở BE. Đáp án lưu ở 2 cột trên `meetings` (câu 1 & 3) + bảng mới `meeting_investment_demands` (câu 2). Danh sách lĩnh vực đọc **động** từ bảng `scopes` bên ERP qua connection `mysql2`, snapshot tên lúc lưu.

**Tech Stack:** PHP 7.4 · Laravel 8 · MySQL · Nuxt 2.14 (Vue 2, chạy bằng **Node 12** + heap 8192) · Bootstrap-Vue · Vuex 3 · ExcelJS (client) · Playwright (E2E)

**Spec:** `docs/superpowers/specs/2026-08-21-meeting-tim-hieu-gioi-thieu-sp-design.md` — đọc kèm plan này.

**Người phụ trách:** @dnsnamdang

---

## Global Constraints

Áp cho **mọi** task, không nhắc lại ở từng task:

- **Nhánh**: `meeting-by-market` ở **cả 2 repo** (`hrm-api`, `hrm-client`). Kiểm tra bằng `git branch --show-current` trước khi sửa code — sai nhánh thì dừng lại, không tự checkout.
- **Commit**: user ĐÃ cho phép commit **local** (mỗi task 1 commit). **TUYỆT ĐỐI KHÔNG `git push`.**
- **PHP**: dùng đường dẫn tuyệt đối `/opt/homebrew/opt/php@7.4/bin/php` — `php` KHÔNG có trên PATH.
- **Line ending**: nhiều file `hrm-client` (và một số file `hrm-api`) đang là **CRLF**. Kiểm tra `file <path>` trước khi sửa; file CRLF thì dòng thêm mới cũng phải `\r\n`. Sau khi sửa bằng script luôn chạy `git diff --stat` — số dòng đổi lớn bất thường = đã phá line ending, trả lại ngay.
- **Model mới BẮT BUỘC `extends BaseModel`** (`use App\Models\BaseModel;`), `created_by`/`updated_by` phải có trong `$fillable`. Ngoại lệ duy nhất: model đọc bảng ERP (`Tp*`, connection `mysql2`) — dùng `Model` thuần và ghi rõ lý do trên class.
- **Cờ quyền FE fail-closed**: không gán literal `true` cho bất kỳ cờ quyền nào.
- **Nút không dùng được thì ẨN HẲN** (`v-if`), không `:disabled` xám — áp cho phần MỚI của feature này. Không sửa đại trà 6 bản ghi loại meeting cũ.
- **Chữ đỏ chỉ dùng cho lỗi validate**. Nhãn/mô tả dùng xám `#6b7280` (nhãn) / `#374151` (giá trị).
- **Popup xác nhận** dùng `await this.$confirm({...})` (component chung `components/modal/base-confirm-modal.vue`). Không `$bvModal.msgBoxConfirm()`, không tự dựng confirm riêng.
- **Không N+1**: eager load quan hệ dùng trong Resource; không query trong vòng lặp.
- **Không thêm quyền mới** cho feature này.
- **Hằng mã loại meeting** (dùng thống nhất BE + FE): `HOP_TIM_HIEU_GIOI_THIEU_SP`
- **Rà project trước khi dựng UI mới**: grep pattern sẵn có rồi copy, ghi rõ trong task "copy pattern từ `<file:dòng>`".

### Vì sao plan này KHÔNG dùng TDD kiểu PHPUnit

`hrm-api/Modules/Assign/Tests/{Feature,Unit}` **rỗng hoàn toàn** (0 file test), và `phpunit.xml` đang **comment** 2 dòng `DB_CONNECTION=sqlite` / `DB_DATABASE=:memory:` → chạy PHPUnit sẽ đập thẳng vào DB dev thật. Dựng hạ tầng test BE là một dự án riêng, không nhét vào feature này (`CLAUDE.md`: không tự phát minh pattern mới).

Thay vào đó mỗi task có **bước verify cụ thể, chạy được, có kết quả kỳ vọng rõ ràng** (truy vấn MySQL / `artisan tinker` / `curl`), và Phase 5 bổ sung **E2E Playwright thật** theo đúng khuôn `e2e/tests/assign/` đã có.

---

## File Structure

### `hrm-api` (BE)

| File | Trách nhiệm |
|------|-------------|
| `Modules/Assign/Database/Migrations/2026_08_21_000001_add_code_to_meeting_types_table.php` | **Mới** — cột `meeting_types.code` |
| `Modules/Assign/Database/Migrations/2026_08_21_000002_add_investment_survey_columns_to_meetings_table.php` | **Mới** — 2 cột câu 1 & 3 trên `meetings` |
| `Modules/Assign/Database/Migrations/2026_08_21_000003_create_meeting_investment_demands_table.php` | **Mới** — bảng chi tiết câu 2 |
| `Modules/Assign/Database/Seeders/SystemMeetingTypesSeeder.php` | **Mới** — tạo bản ghi loại meeting hệ thống, idempotent |
| `Modules/Assign/Entities/MeetingType.php` | Sửa — `code` vào `$fillable`, `isSystem()`, 3 hàm `isCan*` |
| `Modules/Assign/Entities/TpScope.php` | **Mới** — đọc `scopes` bên ERP qua `mysql2`, chỉ đọc |
| `Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php` | **Mới** — 1 dòng lĩnh vực đầu tư của 1 meeting |
| `Modules/Assign/Entities/Meeting/Meeting.php` | Sửa — `$fillable`, relation `investment_demands()`, `requiresInvestmentSurvey()` |
| `Modules/Assign/Services/MeetingTypeService.php` | Sửa — `updateOrCreate` không nhận `code` |
| `Modules/Assign/Http/Controllers/Api/V1/MeetingTypeController.php` | Sửa — 5 guard 423 |
| `Modules/Assign/Transformers/MeetingType/MeetingTypeResource.php` | Sửa — `code`, `is_system` |
| `Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` | Sửa — `investmentScopes()`; `$request->only()` + gọi sync + eager load |
| `Modules/Assign/Services/MeetingService.php` | Sửa — `syncInvestmentDemands()` |
| `Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php` | Sửa — rules + `withValidator` + messages |
| `Modules/Assign/Transformers/MeetingResource/MeetingTransformer.php` | Sửa — 4 field mới |
| `Modules/Assign/Routes/Meeting/api.php` | Sửa — route `investment-scopes` đặt **trước** `{id}` |
| `resources/views/exports/meeting_record.blade.php` | Sửa — section khảo sát trước "Kết luận cuộc họp" |

### `hrm-client` (FE)

| File | Trách nhiệm |
|------|-------------|
| `utils/meetingTypeCodes.js` | **Mới** — hằng `MEETING_TYPE_PRODUCT_INTRO`, dùng chung mọi màn |
| `store/optionsSelect.js` | Sửa — state/mutation/action/getter `investmentScopes` (cache) |
| `pages/assign/meeting/components/MeetingInvestmentSurvey.vue` | **Mới** — toàn bộ khối 3 câu hỏi |
| `pages/assign/meeting/components/MeetingReport.vue` | Sửa — nhúng component + khối Excel |
| `pages/assign/meeting/components/MeetingForm.vue` | Sửa — build payload khảo sát |
| `pages/assign/meeting_type/index.vue` | Sửa — ẩn Sửa/Xoá/Khoá cho bản ghi hệ thống |

### `e2e` (test)

| File | Trách nhiệm |
|------|-------------|
| `e2e/tests/assign/meeting-investment-survey.spec.ts` | **Mới** — E2E luồng khảo sát + ca fail-closed guard 423 |

---

# PHASE 1 — DB & danh mục loại meeting hệ thống

### Task 1.1: 3 migration + chạy migrate

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_08_21_000001_add_code_to_meeting_types_table.php`
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_08_21_000002_add_investment_survey_columns_to_meetings_table.php`
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_08_21_000003_create_meeting_investment_demands_table.php`

**Interfaces:**
- Produces: cột `meeting_types.code`; cột `meetings.has_investment_demand`, `meetings.has_maintenance_demand`; bảng `meeting_investment_demands` với các cột `id, meeting_id, scope_id, scope_name, expected_amount, expected_start_date, position, created_by, updated_by, created_at, updated_at`.

- [ ] **Bước 1: Tạo migration cột `code`**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddCodeToMeetingTypesTable extends Migration
{
    public function up()
    {
        Schema::table('meeting_types', function (Blueprint $table) {
            $table->string('code', 50)->nullable()->unique()->after('id')
                ->comment('Ma dinh danh ben vung; ma nam trong SYSTEM_CODES = ban ghi he thong, khong cho sua/xoa/khoa');
        });
    }

    public function down()
    {
        Schema::table('meeting_types', function (Blueprint $table) {
            $table->dropUnique('meeting_types_code_unique');
            $table->dropColumn('code');
        });
    }
}
```

- [ ] **Bước 2: Tạo migration 2 cột trên `meetings`**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddInvestmentSurveyColumnsToMeetingsTable extends Migration
{
    public function up()
    {
        Schema::table('meetings', function (Blueprint $table) {
            $table->tinyInteger('has_investment_demand')->nullable()->after('conclusion')
                ->comment('Cau 1 khao sat: KH co nhu cau dau tu khong (1=Co, 0=Khong, NULL=chua tra loi)');
            $table->tinyInteger('has_maintenance_demand')->nullable()->after('has_investment_demand')
                ->comment('Cau 3 khao sat: KH co nhu cau dich vu sua chua/bao duong/bao tri khong');
        });
    }

    public function down()
    {
        Schema::table('meetings', function (Blueprint $table) {
            $table->dropColumn(['has_investment_demand', 'has_maintenance_demand']);
        });
    }
}
```

- [ ] **Bước 3: Tạo migration bảng `meeting_investment_demands`**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateMeetingInvestmentDemandsTable extends Migration
{
    public function up()
    {
        Schema::create('meeting_investment_demands', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('meeting_id')->comment('FK meetings.id');
            $table->unsignedBigInteger('scope_id')->comment('id bang scopes ben ERP (mysql2) - KHONG dat FK vi khac database');
            $table->string('scope_name', 255)->comment('Snapshot ten linh vuc tai thoi diem chon');
            $table->decimal('expected_amount', 20, 2)->nullable()->comment('Muc dau tu du kien (VND)');
            $table->date('expected_start_date')->nullable()->comment('Thoi gian du kien bat dau');
            $table->integer('position')->default(0)->comment('Thu tu hien thi');
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();

            $table->unique(['meeting_id', 'scope_id']);
            $table->index('scope_id');
            $table->foreign('meeting_id')->references('id')->on('meetings')->onDelete('cascade');
        });
    }

    public function down()
    {
        Schema::dropIfExists('meeting_investment_demands');
    }
}
```

- [ ] **Bước 4: Chạy migrate**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan migrate
```

Kỳ vọng: 3 dòng `Migrated:` cho đúng 3 file trên, không lỗi.

- [ ] **Bước 5: Verify schema thật trong DB**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" "$DB_DATABASE" -e "
  SHOW COLUMNS FROM meeting_types LIKE 'code';
  SHOW COLUMNS FROM meetings LIKE 'has_%_demand';
  SHOW CREATE TABLE meeting_investment_demands\G"
```

(`$DB_DATABASE` / `$DB_PASSWORD` lấy từ `hrm-api/.env`.)

Kỳ vọng:
- `meeting_types.code` = `varchar(50)`, `Null = YES`, `Key = UNI`
- `meetings` có đúng 2 dòng `has_investment_demand` và `has_maintenance_demand`, cùng `tinyint`, `Null = YES`
- `meeting_investment_demands` có `UNIQUE KEY ... (meeting_id, scope_id)`, `KEY ... (scope_id)`, và `CONSTRAINT ... FOREIGN KEY (meeting_id) REFERENCES meetings (id) ON DELETE CASCADE`

- [ ] **Bước 6: Verify rollback sạch rồi migrate lại**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan migrate:rollback --step=3 && /opt/homebrew/opt/php@7.4/bin/php artisan migrate
```

Kỳ vọng: rollback không lỗi (đặc biệt `dropUnique` trước `dropColumn`), migrate lại thành công. Đây là bước bắt lỗi `down()` viết sai — rất hay gặp với cột có unique index.

---

### Task 1.2: `MeetingType::isSystem()` + chặn Sửa/Xoá/Khoá ở Entity

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/MeetingType.php`

**Interfaces:**
- Consumes: cột `meeting_types.code` (Task 1.1)
- Produces: `MeetingType::CODE_PRODUCT_INTRO` (string `'HOP_TIM_HIEU_GIOI_THIEU_SP'`), `MeetingType::SYSTEM_CODES` (array), `MeetingType::isSystem(): bool`. Ba hàm `isCanEdit()`, `isCanDelete()`, `isCanLockUpdate()` giữ nguyên chữ ký `(): bool`.

- [ ] **Bước 1: Thêm hằng + `code` vào `$fillable`**

Trong `class MeetingType`, ngay dưới 2 hằng `STATUS_*` sẵn có:

```php
    /** Ma loai meeting he thong "Hop tim hieu & Gioi thieu san pham" */
    const CODE_PRODUCT_INTRO = 'HOP_TIM_HIEU_GIOI_THIEU_SP';

    /**
     * Ban ghi he thong: khong cho Sua / Xoa / Khoa.
     * Dinh nghia bang WHITELIST (khong phai "code != null") de sau nay
     * con gan code cho ban ghi thuong ma khong vo tinh khoa no.
     */
    const SYSTEM_CODES = [self::CODE_PRODUCT_INTRO];
```

Và thêm `'code',` vào đầu mảng `$fillable`.

- [ ] **Bước 2: Thêm `isSystem()` và sửa 3 hàm `isCan*`**

Thay 3 hàm hiện có bằng:

```php
    public function isSystem()
    {
        return $this->code !== null && in_array($this->code, self::SYSTEM_CODES, true);
    }

    public function isCanEdit()
    {
        return !$this->isSystem()
            && $this->status == self::STATUS_ACTIVE
            && !$this->meetings()->exists();
    }

    public function isCanDelete()
    {
        return !$this->isSystem() && !$this->meetings()->exists();
    }

    public function isCanLockUpdate()
    {
        // Cho phep khoa/mo khoa ke ca khi loai meeting da duoc su dung.
        // Rieng ban ghi he thong thi khong bao gio cho khoa.
        return !$this->isSystem() && $this->status == self::STATUS_ACTIVE;
    }
```

- [ ] **Bước 3: Lint**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Entities/MeetingType.php
```

Kỳ vọng: `No syntax errors detected`

- [ ] **Bước 4: Verify bằng tinker (chưa có bản ghi hệ thống nên phải ra `false` hết)**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute="
\$t = Modules\Assign\Entities\MeetingType::find(1);
echo 'isSystem=' . var_export(\$t->isSystem(), true) . PHP_EOL;
\$t->code = 'HOP_TIM_HIEU_GIOI_THIEU_SP';
echo 'isSystem(sau khi gan code)=' . var_export(\$t->isSystem(), true) . PHP_EOL;
echo 'isCanEdit=' . var_export(\$t->isCanEdit(), true) . PHP_EOL;
echo 'isCanDelete=' . var_export(\$t->isCanDelete(), true) . PHP_EOL;
echo 'isCanLockUpdate=' . var_export(\$t->isCanLockUpdate(), true) . PHP_EOL;
"
```

Kỳ vọng:
```
isSystem=false
isSystem(sau khi gan code)=true
isCanEdit=false
isCanDelete=false
isCanLockUpdate=false
```

(Gán trên object trong bộ nhớ, **không** `save()` → DB không đổi.)

---

### Task 1.3: Seeder tạo bản ghi loại meeting hệ thống

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Seeders/SystemMeetingTypesSeeder.php`

**Interfaces:**
- Consumes: `MeetingType::CODE_PRODUCT_INTRO` (Task 1.2)
- Produces: 1 bản ghi `meeting_types` với `code = 'HOP_TIM_HIEU_GIOI_THIEU_SP'`, `name = 'Họp tìm hiểu & Giới thiệu sản phẩm'`, `has_customer = 1`, `status = 1`.

- [ ] **Bước 1: Viết seeder**

```php
<?php

namespace Modules\Assign\Database\Seeders;

use Illuminate\Database\Seeder;
use Modules\Assign\Entities\MeetingType;

/**
 * Tao cac loai meeting HE THONG - ban ghi khong cho Sua / Xoa / Khoa.
 *
 * Khoa theo cot `code` nen chay lai nhieu lan khong nhan ban du lieu.
 * KHONG dung toi 6 ban ghi loai meeting cu.
 *
 * Chay: php artisan db:seed --class="Modules\\Assign\\Database\\Seeders\\SystemMeetingTypesSeeder"
 */
class SystemMeetingTypesSeeder extends Seeder
{
    public function run()
    {
        MeetingType::updateOrCreate(
            ['code' => MeetingType::CODE_PRODUCT_INTRO],
            [
                'name'         => 'Họp tìm hiểu & Giới thiệu sản phẩm',
                'description'  => 'Cuộc họp tìm hiểu nhu cầu và giới thiệu sản phẩm/giải pháp tới khách hàng.',
                'has_customer' => 1,
                'status'       => MeetingType::STATUS_ACTIVE,
            ]
        );

        $this->command->info('Da tao/cap nhat loai meeting he thong: ' . MeetingType::CODE_PRODUCT_INTRO);
    }
}
```

- [ ] **Bước 2: Chạy seeder**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan db:seed --class="Modules\\Assign\\Database\\Seeders\\SystemMeetingTypesSeeder"
```

- [ ] **Bước 3: Verify data + cột audit**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" "$DB_DATABASE" -e "
  SELECT id, code, name, has_customer, status, created_by, updated_by FROM meeting_types ORDER BY id;"
```

Kỳ vọng: có bản ghi thứ 7, `code = HOP_TIM_HIEU_GIOI_THIEU_SP`, `name = Họp tìm hiểu & Giới thiệu sản phẩm`, `has_customer = 1`, `status = 1`. Sáu bản ghi cũ **không đổi**, `code` của chúng = `NULL`.

- [ ] **Bước 4: Verify idempotent — chạy seeder lần 2**

Chạy lại đúng lệnh Bước 2, rồi:

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" "$DB_DATABASE" -e "
  SELECT COUNT(*) AS n FROM meeting_types WHERE code = 'HOP_TIM_HIEU_GIOI_THIEU_SP';"
```

Kỳ vọng: `n = 1` (không nhân bản).

---

### Task 1.4: Guard 423 ở `MeetingTypeController` + chặn ghi `code` ở Service

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingTypeController.php`
- Modify: `hrm-api/Modules/Assign/Services/MeetingTypeService.php`

**Interfaces:**
- Consumes: `MeetingType::isSystem()` (Task 1.2), bản ghi hệ thống (Task 1.3)
- Produces: 5 endpoint trả HTTP 423 khi đụng bản ghi hệ thống.

- [ ] **Bước 1: Guard trong `updateOrCreate()`**

Trong `MeetingTypeController::updateOrCreate()`, đặt **ngay đầu hàm**, TRƯỚC `try`:

```php
        if ($request->filled('id')) {
            $existing = MeetingType::find($request->input('id'));
            if ($existing && $existing->isSystem()) {
                return $this->responseJson(
                    'Loại meeting hệ thống, không được phép sửa.',
                    Response::HTTP_LOCKED
                );
            }
        }
```

- [ ] **Bước 2: Guard trong `destroy()`**

Đặt ngay đầu hàm, TRƯỚC `try`:

```php
        if ($meetingType->isSystem()) {
            return $this->responseJson(
                'Loại meeting hệ thống, không được phép xoá.',
                Response::HTTP_LOCKED
            );
        }
```

- [ ] **Bước 3: Guard trong `deleteByIds()`**

Đặt ngay sau `$request->validate([...])`, TRƯỚC `try`. All-or-nothing: có 1 id hệ thống là chặn cả lượt, không xoá nửa vời im lặng:

```php
        $systemIds = MeetingType::whereIn('id', $request->ids)
            ->whereIn('code', MeetingType::SYSTEM_CODES)
            ->pluck('id')
            ->toArray();

        if (!empty($systemIds)) {
            return $this->responseJson(
                'Danh sách chứa loại meeting hệ thống, không được phép xoá.',
                Response::HTTP_LOCKED
            );
        }
```

- [ ] **Bước 4: Guard trong `lock()` và `unlock()`**

`lock()` — đặt TRƯỚC dòng `if (!$meetingType->isCanLockUpdate())` sẵn có, để message nói đúng lý do thay vì "Dữ liệu đã thay đổi":

```php
        if ($meetingType->isSystem()) {
            return $this->responseJson(
                'Loại meeting hệ thống, không được phép khoá.',
                Response::HTTP_LOCKED
            );
        }
```

`unlock()` — hàm này hiện **không có guard nào**; đặt ngay đầu hàm:

```php
        if ($meetingType->isSystem()) {
            return $this->responseJson(
                'Loại meeting hệ thống, không được phép mở khoá.',
                Response::HTTP_LOCKED
            );
        }
```

- [ ] **Bước 5: Chặn đường ghi `code` ở Service**

Mở `MeetingTypeService::updateOrCreate()`. Xác nhận **cả 2 nhánh** (`$meetingType->update([...])` và `MeetingType::create([...])`) chỉ liệt kê `name`, `has_customer`, `status`, `description` — **không** có `code`. Nếu có thì bỏ đi. Thêm comment trên hàm:

```php
    /**
     * LUU Y: cot `code` KHONG duoc phep set tu API/import.
     * Chi seeder (SystemMeetingTypesSeeder) moi duoc ghi vao `code`.
     */
```

- [ ] **Bước 6: Lint**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Http/Controllers/Api/V1/MeetingTypeController.php \
  && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Services/MeetingTypeService.php
```

Kỳ vọng: `No syntax errors detected` cho cả 2 file.

- [ ] **Bước 7: Verify 5 guard bằng curl**

Khởi động API và lấy token. Dùng user E2E `e2e_assign@test.local / Password@123` (do `e2e_provision.php` tạo, role Super admin) hoặc user thật có quyền "Quản lý danh mục loại meeting":

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan serve --port=8000 &
sleep 3

# Nạp biến DB từ .env
export $(grep -E '^DB_(DATABASE|PASSWORD)=' .env | tail -2 | xargs)

SYS_ID=$(mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" "$DB_DATABASE" -Nse \
  "SELECT id FROM meeting_types WHERE code='HOP_TIM_HIEU_GIOI_THIEU_SP'")
echo "SYS_ID=$SYS_ID"

TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"e2e_assign@test.local","password":"Password@123"}' \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("data",{}).get("token") or d.get("token",""))')
echo "TOKEN len=${#TOKEN}"

H=(-H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json')
C='-s -o /dev/null -w %{http_code}\n'

echo -n 'updateOrCreate  : '; curl $C -X POST   "${H[@]}" http://127.0.0.1:8000/api/v1/assign/meeting_types            -d "{\"id\":$SYS_ID,\"name\":\"X\",\"status\":1,\"has_customer\":1}"
echo -n 'destroy         : '; curl $C -X DELETE "${H[@]}" "http://127.0.0.1:8000/api/v1/assign/meeting_types/$SYS_ID"
echo -n 'lock            : '; curl $C            "${H[@]}" "http://127.0.0.1:8000/api/v1/assign/meeting_types/$SYS_ID/lock"
echo -n 'unlock          : '; curl $C            "${H[@]}" "http://127.0.0.1:8000/api/v1/assign/meeting_types/$SYS_ID/unlock"
echo -n 'delete_by_ids   : '; curl $C -X POST   "${H[@]}" http://127.0.0.1:8000/api/v1/assign/meeting_types/delete_by_ids -d "{\"ids\":[$SYS_ID]}"
```

Kỳ vọng: **cả 5 dòng đều in `423`**.

Ra `401` = token sai (kiểm lại đường dẫn field token trong response login). Ra `403` = user thiếu quyền "Quản lý danh mục loại meeting" — cấp quyền rồi chạy lại, **không** được bỏ qua bước này.

- [ ] **Bước 8: Verify không chặn nhầm bản ghi thường (regression)**

```bash
# Khoá rồi mở khoá lại bản ghi id=3 (loại meeting thường)
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/v1/assign/meeting_types/3/lock
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/v1/assign/meeting_types/3/unlock
```

Kỳ vọng: `200` rồi `200`. Sau đó kiểm `SELECT status FROM meeting_types WHERE id=3` = `1` (đã trả về nguyên trạng).

- [ ] **Bước 9: Verify cột audit không bị hỏng khi thêm `code`**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" "$DB_DATABASE" -Nse \
  "SELECT id, updated_by, updated_at FROM meeting_types WHERE id=3"
```

Kỳ vọng: `updated_by` **không NULL** (đã ghi nhân viên vừa khoá/mở khoá). Đây là cách duy nhất phát hiện audit hỏng — không có exception, không có log.

---

### Task 1.5: `MeetingTypeResource` trả `code` + `is_system`

**Files:**
- Modify: `hrm-api/Modules/Assign/Transformers/MeetingType/MeetingTypeResource.php`

**Interfaces:**
- Consumes: `MeetingType::isSystem()` (Task 1.2)
- Produces: response của `GET /assign/meeting_types` và `GET /assign/meeting_types/getAll` có thêm `code: string|null` và `is_system: bool`.

- [ ] **Bước 1: Thêm 2 field**

Trong `toArray()`, ngay sau `'id' => $this->id,`:

```php
        'code' => $this->code,
        'is_system' => $this->isSystem(),
```

- [ ] **Bước 2: Lint**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Transformers/MeetingType/MeetingTypeResource.php
```

- [ ] **Bước 3: Verify qua API**

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/v1/assign/meeting_types/getAll | python3 -m json.tool | head -40
```

Kỳ vọng: bản ghi hệ thống có `"code": "HOP_TIM_HIEU_GIOI_THIEU_SP"`, `"is_system": true`, `"is_can_edit": false`, `"is_can_delete": false`; 6 bản ghi cũ có `"code": null`, `"is_system": false`.

---

### Task 1.6: FE ẩn nút Sửa / Xoá / Khoá cho bản ghi hệ thống

**Files:**
- Modify: `hrm-client/pages/assign/meeting_type/index.vue`

**Interfaces:**
- Consumes: field `is_system` từ `MeetingTypeResource` (Task 1.5)

- [ ] **Bước 1: Kiểm line ending trước khi sửa**

```bash
cd HRM/hrm-client && file pages/assign/meeting_type/index.vue
```

Nếu báo `with CRLF line terminators` → mọi dòng thêm mới phải kết thúc `\r\n`.

- [ ] **Bước 2: Ẩn nút Khoá/Mở khoá**

Nút Khoá nằm ở `pages/assign/meeting_type/index.vue:188-205` (`<button ... @click="confirmToggleLock(item)">`). Thêm `v-if` vào thẻ `<button>`:

```html
                            v-if="!item.is_system"
```

- [ ] **Bước 3: Ẩn nút Sửa**

Nút Sửa ở `:237` (`:disabled="!item.is_can_edit || item.status === 2"`). Thêm vào thẻ `<button>` đó:

```html
                            v-if="!item.is_system"
```

**Giữ nguyên** `:disabled` và `:title` sẵn có cho các bản ghi thường — `CLAUDE.md` cấm sửa đại trà màn cũ.

- [ ] **Bước 4: Ẩn nút Xoá**

Nút Xoá ở `:260` (`:disabled="!item.is_can_delete"`). Thêm vào thẻ `<button>` đó:

```html
                            v-if="!item.is_system"
```

- [ ] **Bước 5: Ẩn checkbox chọn dòng**

Trong `<template #cell-checkbox="{ item }">` (`:148-155`), bọc `V2BaseCheckbox` bằng:

```html
                    <V2BaseCheckbox
                        v-if="!item.is_system"
                        ...giữ nguyên các prop cũ...
                    />
```

- [ ] **Bước 6: Build FE và verify bằng mắt**

```bash
cd HRM/hrm-client && nvm use 12 && NODE_OPTIONS=--max-old-space-size=8192 npm run dev
```

Mở `http://127.0.0.1:3000/assign/meeting_type`.

Kỳ vọng:
- Dòng "Họp tìm hiểu & Giới thiệu sản phẩm": cột Hành động **chỉ còn nút Xem** (con mắt); **không** có Sửa, Xoá, Khoá; **không** có checkbox đầu dòng.
- 6 dòng cũ: giữ nguyên đủ nút như trước (Xem, Khoá, Sửa, Xoá) và checkbox.
- Tích chọn tất cả (checkbox header) → dòng hệ thống không bị chọn.

- [ ] **Bước 7: Kiểm line ending không bị phá**

```bash
cd HRM/hrm-client && git diff --stat pages/assign/meeting_type/index.vue
```

Kỳ vọng: chỉ vài dòng thay đổi (khoảng 4-5 dòng thêm). Nếu thấy cả file bị đánh dấu đổi → đã phá line ending, `git checkout` file rồi sửa lại bằng tay.

---

# PHASE 2 — Đọc danh sách lĩnh vực từ ERP

### Task 2.1: Entity `TpScope` + endpoint `investment-scopes`

**Files:**
- Create: `hrm-api/Modules/Assign/Entities/TpScope.php`
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php`
- Modify: `hrm-api/Modules/Assign/Routes/Meeting/api.php`

**Interfaces:**
- Produces:
  - `Modules\Assign\Entities\TpScope` — connection `mysql2`, table `scopes`, hằng `TpScope::STATUS_ACTIVE = 1`
  - `MeetingController::investmentScopes(Request $request)` — trả `{"data": [{"id": int, "name": string, "is_locked": bool}]}`
  - Route `GET /api/v1/assign/meeting/investment-scopes`

- [ ] **Bước 1: Tạo entity `TpScope`**

```php
<?php

namespace Modules\Assign\Entities;

use Illuminate\Database\Eloquent\Model;

/**
 * Bang `scopes` cua ERP (connection mysql2) - danh muc "Linh vuc" TPE cung cap.
 *
 * KHONG extends BaseModel: day la bang cua ERP, HRM chi DOC.
 * Hook created_by/updated_by cua BaseModel dung auth()->id() cua HRM,
 * ghi sang ERP se tro sai nhan vien.
 *
 * CANH BAO: dung nham voi Modules\Assign\Entities\Scope\Scope - do la bang
 * `scopes` cua HRM tren connection MAC DINH (danh muc "Nhom nganh"), khac han.
 */
class TpScope extends Model
{
    protected $connection = 'mysql2';
    protected $table = 'scopes';
    public $timestamps = false;

    const STATUS_ACTIVE = 1;
}
```

- [ ] **Bước 2: Thêm method `investmentScopes()` vào `MeetingController`**

Thêm `use Modules\Assign\Entities\TpScope;` vào phần `use` đầu file, rồi thêm method (đặt cạnh các method danh mục sẵn có như `getListCustomer`):

```php
    /**
     * Danh muc "Linh vuc dau tu" cho khoi Khao sat nhu cau khach hang (tab Bien ban).
     * Nguon: bang `scopes` ben ERP qua connection mysql2.
     *
     * include_ids: id linh vuc dang duoc meeting su dung (ke ca da bi khoa ben ERP)
     * -> van phai tra ve, neu khong man Sua se mat gia tri da chon.
     */
    public function investmentScopes(Request $request)
    {
        try {
            $includeIds = $request->input('include_ids', []);
            if (!is_array($includeIds)) {
                $includeIds = explode(',', (string) $includeIds);
            }
            $includeIds = array_values(array_filter(array_map('intval', $includeIds)));

            $scopes = TpScope::where(function ($q) use ($includeIds) {
                    $q->where('status', TpScope::STATUS_ACTIVE);
                    if (!empty($includeIds)) {
                        $q->orWhereIn('id', $includeIds);
                    }
                })
                ->orderBy('id')
                ->get(['id', 'name', 'status']);

            $data = $scopes->map(function ($s) {
                return [
                    'id' => (int) $s->id,
                    'name' => $s->name,
                    'is_locked' => (int) $s->status !== TpScope::STATUS_ACTIVE,
                ];
            })->values();

            return $this->responseJson('success', Response::HTTP_OK, $data);
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseJson(
                'Không kết nối được danh mục lĩnh vực bên ERP. Vui lòng thử lại.',
                Response::HTTP_SERVICE_UNAVAILABLE
            );
        }
    }
```

- [ ] **Bước 3: Thêm route — ĐẶT TRƯỚC mọi route `{id}`**

Trong `Modules/Assign/Routes/Meeting/api.php`, thêm ngay sau dòng `Route::get('/calendar', ...)`:

```php
        // Danh muc linh vuc dau tu (bang scopes ben ERP) cho khoi Khao sat tab Bien ban.
        // Dat TRUOC moi route wildcard {id} de khong bi nuot.
        Route::get('/investment-scopes', [MeetingController::class, 'investmentScopes']);
```

- [ ] **Bước 4: Lint + kiểm route đã đăng ký**

```bash
cd HRM/hrm-api \
  && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Entities/TpScope.php \
  && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Http/Controllers/Api/V1/MeetingController.php \
  && /opt/homebrew/opt/php@7.4/bin/php artisan route:list --path=assign/meeting | grep investment-scopes
```

Kỳ vọng: 2 dòng `No syntax errors detected` + 1 dòng route `GET|HEAD  api/v1/assign/meeting/investment-scopes`.

- [ ] **Bước 5: Verify endpoint trả đủ 13 lĩnh vực**

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/v1/assign/meeting/investment-scopes | python3 -m json.tool
```

Kỳ vọng: mảng **13 phần tử** (khớp `SELECT COUNT(*) FROM erp2326.scopes WHERE status=1`), phần tử đầu `{"id": 1, "name": "Ô TÔ - Máy móc, Thiết bị , vật tư phụ tùng sửa chữa bảo dưỡng", "is_locked": false}`.

- [ ] **Bước 6: Verify `include_ids` giữ lĩnh vực đã khoá**

```bash
# Khoá tạm lĩnh vực id=2 bên ERP
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" erp2326 -e "UPDATE scopes SET status=2 WHERE id=2;"

# Không include_ids -> KHÔNG có id=2
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://127.0.0.1:8000/api/v1/assign/meeting/investment-scopes" | grep -c '"id": 2,'

# Có include_ids -> CÓ id=2 và is_locked=true
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://127.0.0.1:8000/api/v1/assign/meeting/investment-scopes?include_ids[]=2" | python3 -m json.tool | grep -A 2 '"id": 2,'

# Trả lại nguyên trạng
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" erp2326 -e "UPDATE scopes SET status=1 WHERE id=2;"
```

Kỳ vọng: lần 1 đếm ra `0`; lần 2 thấy `"id": 2` kèm `"is_locked": true`.

- [ ] **Bước 7: Verify route không bị `{id}` nuốt**

```bash
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/v1/assign/meeting/investment-scopes
```

Kỳ vọng: `200`, **không** phải 404/500 của `show('investment-scopes')`.

---

### Task 2.2: Vuex cache `investmentScopes`

**Files:**
- Modify: `hrm-client/store/optionsSelect.js`
- Create: `hrm-client/utils/meetingTypeCodes.js`

**Interfaces:**
- Consumes: `GET assign/meeting/investment-scopes` (Task 2.1)
- Produces:
  - `utils/meetingTypeCodes.js` export `MEETING_TYPE_PRODUCT_INTRO = 'HOP_TIM_HIEU_GIOI_THIEU_SP'`
  - Vuex `optionsSelect`: state `investmentScopes`, mutation `SET_INVESTMENT_SCOPES`, action `fetchInvestmentScopes({ includeIds = [] })`, getter `getInvestmentScopes`
  - ⚠️ **Cache CHỈ chứa mục active** (lọc `is_locked` trước khi commit, theo đúng pattern `fetchProjectPhases` cùng file — action đó từng dính bug "khoá A rồi đổi sang bản ghi B, A vẫn còn trong dropdown mọi màn cho tới khi F5"). Danh sách đầy đủ (active + mục khoá được `include_ids` kéo về) trả qua **giá trị return** của action. Nơi tiêu thụ phải dùng giá trị return, KHÔNG đọc getter.
  - Lỗi API → trả `state.investmentScopes` (cache cũ), KHÔNG trả `[]` (để select không bị trống).
  - Mỗi phần tử: `{ id: number, name: string, is_locked: boolean }`

- [ ] **Bước 1: Tạo file hằng**

`hrm-client/utils/meetingTypeCodes.js`:

```js
/**
 * Mã loại meeting hệ thống — phải khớp tuyệt đối với
 * Modules\Assign\Entities\MeetingType::CODE_PRODUCT_INTRO bên hrm-api.
 */
export const MEETING_TYPE_PRODUCT_INTRO = 'HOP_TIM_HIEU_GIOI_THIEU_SP'
```

- [ ] **Bước 2: Thêm state — CHÚ Ý tên khoá**

⚠️ `store/optionsSelect.js` **đã có** state `scopes` (dùng cho danh mục "Nhóm ngành" của HRM, gọi `assign/scopes/getAll`). **KHÔNG** dùng lại khoá đó. Thêm khoá mới vào cuối object `state()`:

```js
    investmentScopes: [],
```

- [ ] **Bước 3: Thêm mutation**

Thêm vào object `mutations`:

```js
    SET_INVESTMENT_SCOPES(state, investmentScopes) {
        state.investmentScopes = investmentScopes
    },
```

- [ ] **Bước 4: Thêm action (có cache)**

Thêm vào object `actions`:

```js
    /**
     * Danh mục "Lĩnh vực đầu tư" (bảng scopes bên ERP) cho khối Khảo sát tab Biên bản.
     * Cache lại vì danh mục ít đổi; truyền includeIds để lĩnh vực đã chọn nay bị khoá vẫn hiện.
     */
    async fetchInvestmentScopes({ commit, dispatch, state }, { includeIds = [] } = {}) {
        // Đã có cache và không cần bổ sung id nào ngoài cache -> khỏi gọi lại
        const cachedIds = state.investmentScopes.map((s) => s.id)
        const missing = includeIds.filter((id) => !cachedIds.includes(Number(id)))
        if (state.investmentScopes.length > 0 && missing.length === 0) {
            return state.investmentScopes
        }

        try {
            const query = includeIds.map((id) => `include_ids[]=${encodeURIComponent(id)}`).join('&')
            const url = query
                ? `assign/meeting/investment-scopes?${query}`
                : 'assign/meeting/investment-scopes'
            const { data } = await dispatch('apiGetMethod', url, { root: true })
            const scopes = (data || []).map((s) => ({
                id: Number(s.id),
                name: s.name,
                is_locked: !!s.is_locked,
            }))
            commit('SET_INVESTMENT_SCOPES', scopes)
            return scopes
        } catch (error) {
            console.error('Error fetching investment scopes:', error)
            return []
        }
    },
```

- [ ] **Bước 5: Thêm getter**

Thêm vào object `getters`:

```js
    getInvestmentScopes: (state) => state.investmentScopes,
```

- [ ] **Bước 6: Verify bằng Vue devtools / console**

Build FE, mở bất kỳ màn nào, chạy trong console trình duyệt:

```js
await $nuxt.$store.dispatch('optionsSelect/fetchInvestmentScopes', {})
$nuxt.$store.getters['optionsSelect/getInvestmentScopes'].length
```

Kỳ vọng: `13`.

Gọi lần 2 và xem tab Network: **không** phát sinh request mới (đã cache).

- [ ] **Bước 7: Verify không đụng state `scopes` cũ**

```js
$nuxt.$store.state.optionsSelect.scopes.length
```

Kỳ vọng: `0` (chưa ai gọi `fetchScopes`) — chứng tỏ 2 danh mục tách bạch, không ghi đè nhau.

---

# PHASE 3 — Nhập & lưu đáp án

### Task 3.1: Entity + relation + `syncInvestmentDemands()`

**Files:**
- Create: `hrm-api/Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php`
- Modify: `hrm-api/Modules/Assign/Entities/Meeting/Meeting.php`
- Modify: `hrm-api/Modules/Assign/Services/MeetingService.php`

**Interfaces:**
- Consumes: bảng `meeting_investment_demands` (Task 1.1), `TpScope` (Task 2.1), `MeetingType::CODE_PRODUCT_INTRO` (Task 1.2)
- Produces:
  - `MeetingInvestmentDemand` với `$fillable = ['meeting_id','scope_id','scope_name','expected_amount','expected_start_date','position','created_by','updated_by']`, cast `expected_start_date` → `date`
  - `Meeting::investment_demands(): HasMany` (đã `orderBy('position')`)
  - `Meeting::requiresInvestmentSurvey(): bool`
  - `MeetingService::syncInvestmentDemands($demands, $entity): void`

- [ ] **Bước 1: Tạo `MeetingInvestmentDemand`**

```php
<?php

namespace Modules\Assign\Entities\Meeting;

use App\Models\BaseModel;

/**
 * 1 dong "Linh vuc dau tu" cua khoi Khao sat nhu cau khach hang (tab Bien ban).
 *
 * scope_id tro toi bang `scopes` ben ERP (connection mysql2) nen KHONG co FK.
 * scope_name la SNAPSHOT ten linh vuc luc luu -> ERP doi ten/xoa khong lam sai bien ban cu.
 */
class MeetingInvestmentDemand extends BaseModel
{
    protected $table = 'meeting_investment_demands';

    protected $fillable = [
        'meeting_id',
        'scope_id',
        'scope_name',
        'expected_amount',
        'expected_start_date',
        'position',
        'created_by',
        'updated_by',
    ];

    protected $casts = [
        'expected_start_date' => 'date',
    ];

    public function meeting()
    {
        return $this->belongsTo(Meeting::class, 'meeting_id');
    }
}
```

- [ ] **Bước 2: Sửa `Meeting` entity**

Thêm `use Modules\Assign\Entities\Meeting\MeetingInvestmentDemand;` (cùng namespace nên không bắt buộc, nhưng thêm cho rõ khi đọc).

Thêm vào `$fillable`, ngay sau `'conclusion',`:

```php
        // Khao sat nhu cau khach hang (loai meeting Hop tim hieu & Gioi thieu san pham)
        'has_investment_demand',
        'has_maintenance_demand',
```

Thêm 2 method:

```php
    /** Cac linh vuc dau tu KH quan tam - cau 2 khoi Khao sat */
    public function investment_demands()
    {
        return $this->hasMany(MeetingInvestmentDemand::class, 'meeting_id', 'id')
            ->orderBy('position');
    }

    /** Meeting nay co phai loai can khoi Khao sat nhu cau dau tu khong */
    public function requiresInvestmentSurvey()
    {
        return $this->meeting_type
            && $this->meeting_type->code === MeetingType::CODE_PRODUCT_INTRO;
    }
```

- [ ] **Bước 3: Thêm `syncInvestmentDemands()` vào `MeetingService`**

Thêm `use Modules\Assign\Entities\TpScope;` vào phần `use`, rồi thêm method ngay sau `syncReports()`:

```php
    /**
     * Luu cac dong "Linh vuc dau tu" cua khoi Khao sat (tab Bien ban).
     * Bam khuon syncReports(): xoa het roi ghi lai.
     *
     * LUU Y: doc $entity->has_investment_demand SAU khi repository->update() da chay,
     * nen 2 cot has_*_demand PHAI nam trong $request->only() o MeetingController::update().
     */
    public function syncInvestmentDemands($demands, $entity)
    {
        // Cau 1 = Khong / chua tra loi -> xoa sach chi tiet, khong de rac
        if ((int) $entity->has_investment_demand !== 1) {
            $entity->investment_demands()->delete();
            return;
        }

        if (!is_array($demands)) {
            return; // FE khong gui field -> giu nguyen du lieu cu
        }

        $entity->investment_demands()->delete();

        // Snapshot ten linh vuc: nap 1 lan cho ca mang, KHONG query trong vong lap
        $scopeIds = array_values(array_filter(array_column($demands, 'scope_id')));
        $scopeById = empty($scopeIds)
            ? collect()
            : TpScope::whereIn('id', $scopeIds)->pluck('name', 'id');

        foreach (array_values($demands) as $i => $item) {
            $scopeId = (int) ($item['scope_id'] ?? 0);
            if (!$scopeId) {
                continue;
            }

            $entity->investment_demands()->create([
                'scope_id' => $scopeId,
                // uu tien ten ERP hien tai; ERP xoa mat thi lay ten FE gui len
                'scope_name' => $scopeById[$scopeId] ?? ($item['scope_name'] ?? ''),
                'expected_amount' => $item['expected_amount'] ?? null,
                'expected_start_date' => $item['expected_start_date'] ?? null,
                'position' => $i,
            ]);
        }
    }
```

- [ ] **Bước 4: Lint**

```bash
cd HRM/hrm-api \
  && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php \
  && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Entities/Meeting/Meeting.php \
  && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Services/MeetingService.php
```

Kỳ vọng: 3 dòng `No syntax errors detected`.

- [ ] **Bước 5: Verify sync bằng tinker (ghi → đọc → xoá)**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute="
\$m = Modules\Assign\Entities\Meeting\Meeting::orderBy('id','desc')->first();
\$svc = app(Modules\Assign\Services\MeetingService::class);

// 1) Cau 1 = Co -> ghi 2 dong
\$m->has_investment_demand = 1; \$m->save();
\$svc->syncInvestmentDemands([
  ['scope_id'=>1,'expected_amount'=>1500000000,'expected_start_date'=>'2027-03-15'],
  ['scope_id'=>5,'expected_amount'=>200000000,'expected_start_date'=>'2027-06-01'],
], \$m);
echo 'sau khi ghi: ' . \$m->investment_demands()->count() . PHP_EOL;
echo 'snapshot ten: ' . \$m->investment_demands()->first()->scope_name . PHP_EOL;
echo 'created_by: ' . var_export(\$m->investment_demands()->first()->created_by, true) . PHP_EOL;

// 2) Cau 1 = Khong -> phai xoa sach
\$m->has_investment_demand = 0; \$m->save();
\$svc->syncInvestmentDemands([], \$m);
echo 'sau khi doi sang Khong: ' . \$m->investment_demands()->count() . PHP_EOL;

// Tra lai nguyen trang
\$m->has_investment_demand = null; \$m->save();
"
```

Kỳ vọng:
```
sau khi ghi: 2
snapshot ten: Ô TÔ - Máy móc, Thiết bị , vật tư phụ tùng sửa chữa bảo dưỡng
created_by: <id nhân viên, KHÔNG phải NULL>
sau khi doi sang Khong: 0
```

`created_by` ra `NULL` = quên `extends BaseModel` hoặc quên `created_by` trong `$fillable` — quay lại Bước 1.

*(Chạy trong tinker CLI không có `auth()` nên `created_by` có thể NULL; nếu vậy, verify lại ở Task 3.3 Bước 6 qua API thật — đó mới là đường ghi thực tế.)*

---

### Task 3.2: Validate ở `MeetingUpdateApiRequest`

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php`

**Interfaces:**
- Consumes: `MeetingType::CODE_PRODUCT_INTRO` (Task 1.2)
- Produces: 400 với các key `has_investment_demand`, `has_maintenance_demand`, `investment_demands`, `investment_demands.{i}.expected_amount`, `investment_demands.{i}.expected_start_date`

- [ ] **Bước 1: Thêm rule vào `rules()`**

Trong `rules()` đã có sẵn khối tính `$hasCustomer` từ `$meetingTypeId`. Thêm **ngay sau khối đó** (dùng lại biến `$meetingType` đã có):

```php
        // Khao sat nhu cau khach hang - chi ap cho loai meeting he thong
        $needSurvey = $meetingType && $meetingType->code === \Modules\Assign\Entities\MeetingType::CODE_PRODUCT_INTRO;

        if ($needSurvey) {
            $rules['has_investment_demand']  = 'nullable|boolean|required_if:status,3';
            $rules['has_maintenance_demand'] = 'nullable|boolean|required_if:status,3';

            $rules['investment_demands']                       = 'nullable|array';
            $rules['investment_demands.*.scope_id']            = 'required|integer|min:1';
            $rules['investment_demands.*.expected_amount']     = 'nullable|numeric|min:0|max:999999999999999999';
            $rules['investment_demands.*.expected_start_date'] = 'nullable|date|after_or_equal:today';
        }
```

⚠️ Biến `$meetingType` hiện đang được gán **bên trong** `if ($meetingTypeId)`. Nâng khai báo lên trước để dùng được ở đây:

```php
        $meetingTypeId = $this->input('meeting_type_id');
        $meetingType = $meetingTypeId ? \Modules\Assign\Entities\MeetingType::find($meetingTypeId) : null;
        $hasCustomer = $meetingType ? (bool) $meetingType->has_customer : true;
```

(thay cho khối `$hasCustomer = true; if ($meetingTypeId) { ... }` hiện tại — giữ nguyên hành vi mặc định `true` khi không tìm thấy loại.)

- [ ] **Bước 2: Thêm ràng buộc liên trường vào `withValidator()`**

Trong `withValidator($validator)` đã có sẵn 1 `$validator->after(...)`. **Thêm một `after()` thứ hai** (không sửa cái cũ):

```php
        $validator->after(function ($v) {
            $meetingTypeId = $this->input('meeting_type_id');
            $meetingType = $meetingTypeId ? \Modules\Assign\Entities\MeetingType::find($meetingTypeId) : null;
            $needSurvey = $meetingType
                && $meetingType->code === \Modules\Assign\Entities\MeetingType::CODE_PRODUCT_INTRO;

            // Chi chan khi bam Hoan thanh
            if (!$needSurvey || (int) $this->input('status') !== \Modules\Assign\Entities\Meeting\Meeting::HOAN_THANH) {
                return;
            }

            // Tra loi "Khong" -> khong doi gi them
            if ((int) $this->input('has_investment_demand') !== 1) {
                return;
            }

            $demands = $this->input('investment_demands', []);
            if (empty($demands)) {
                $v->errors()->add('investment_demands', 'Vui lòng chọn ít nhất một lĩnh vực đầu tư.');
                return;
            }

            foreach ($demands as $i => $d) {
                $amount = $d['expected_amount'] ?? null;
                if ($amount === null || $amount === '') {
                    $v->errors()->add("investment_demands.$i.expected_amount", 'Vui lòng nhập mức đầu tư dự kiến.');
                }
                if (empty($d['expected_start_date'])) {
                    $v->errors()->add("investment_demands.$i.expected_start_date", 'Vui lòng chọn thời gian dự kiến bắt đầu.');
                }
            }
        });
```

- [ ] **Bước 3: Thêm messages**

Vào mảng `return [...]` của `messages()`:

```php
            'has_investment_demand.required_if' => 'Vui lòng trả lời câu hỏi về nhu cầu đầu tư của khách hàng.',
            'has_maintenance_demand.required_if' => 'Vui lòng trả lời câu hỏi về nhu cầu dịch vụ sửa chữa, bảo dưỡng/bảo trì.',
            'investment_demands.*.expected_start_date.after_or_equal' => 'Phải lớn hơn hoặc bằng ngày hiện tại.',
```

- [ ] **Bước 4: Lint**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php
```

- [ ] **Bước 5: Verify — hoãn sang Task 3.3**

Rule chỉ chạy được khi có meeting thuộc loại hệ thống + đường ghi hoàn chỉnh. Verify 400 nằm ở Task 3.3 Bước 7. Task này dừng ở lint + đọc lại code.

---

### Task 3.3: Nối vào `MeetingController::update()` + Transformer + eager load

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php`
- Modify: `hrm-api/Modules/Assign/Transformers/MeetingResource/MeetingTransformer.php`

**Interfaces:**
- Consumes: `MeetingService::syncInvestmentDemands()` (Task 3.1), rule (Task 3.2)
- Produces: response detail meeting có thêm `has_investment_demand`, `has_maintenance_demand`, `investment_demands[]`, `meeting_type_code`

- [ ] **Bước 1: ⚠️ Thêm 2 cột vào `$request->only()` — BƯỚC DỄ SÓT NHẤT**

Trong `MeetingController::update()`, mảng `$request->only([...])` (bắt đầu ~dòng 343) là **danh sách cột liệt kê tay**. Thêm ngay sau `'conclusion',`:

```php
            'has_investment_demand',
            'has_maintenance_demand',
```

Quên bước này thì 2 câu trả lời **im lặng không được ghi** (không exception, không log), và `syncInvestmentDemands()` đọc giá trị cũ → **xoá nhầm** các dòng lĩnh vực vừa nhập. Thêm vào `$fillable` của `Meeting` là **chưa đủ**.

- [ ] **Bước 2: Gọi sync trong transaction**

Trong `update()`, ngay sau dòng `$this->service->syncReports($request->reports, $entity);`:

```php
            $this->service->syncInvestmentDemands($request->investment_demands, $entity);
```

- [ ] **Bước 3: Eager load ở `show()` và `print()`**

Thêm `'investment_demands',` vào mảng `load([...])` của `print()` (hiện có `company_members`, `customer_members`, `reports`, `attachments`, `projects`, `meeting_type`). Làm tương tự cho `show()` và mọi chỗ khác trả detail meeting.

- [ ] **Bước 4: Thêm 4 field vào `MeetingTransformer`**

Ngay sau `'conclusion' => $meeting->conclusion,`:

```php
            'has_investment_demand' => $meeting->has_investment_demand,
            'has_maintenance_demand' => $meeting->has_maintenance_demand,
            'investment_demands' => $meeting->investment_demands,
            'meeting_type_code' => $meeting->meeting_type ? $meeting->meeting_type->code : null,
```

- [ ] **Bước 5: Lint**

```bash
cd HRM/hrm-api \
  && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Http/Controllers/Api/V1/MeetingController.php \
  && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Transformers/MeetingResource/MeetingTransformer.php
```

- [ ] **Bước 6: Verify đường ghi thật — bắt đúng lỗi Bước 1**

Tạo 1 meeting thuộc loại hệ thống qua UI (hoặc tinker), rồi `POST` cập nhật qua API với payload khảo sát:

```bash
MEETING_ID=<id meeting loại hệ thống>

curl -s -X POST "http://127.0.0.1:8000/api/v1/assign/meeting/$MEETING_ID" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{
    "name":"Test khao sat","meeting_type_id":<SYS_ID>,"status":2,
    "start_date":"2027-01-10 09:00:00","end_date":"2027-01-10 11:00:00",
    "mode_id":1,"location":"HN","company_members":[{"name":"NV A"}],
    "has_investment_demand":1,"has_maintenance_demand":0,
    "investment_demands":[{"scope_id":1,"expected_amount":1500000000,"expected_start_date":"2027-03-15"}]
  }' | python3 -m json.tool | head -30

mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" "$DB_DATABASE" -e "
  SELECT has_investment_demand, has_maintenance_demand FROM meetings WHERE id=$MEETING_ID;
  SELECT scope_id, scope_name, expected_amount, expected_start_date, position, created_by
    FROM meeting_investment_demands WHERE meeting_id=$MEETING_ID;"
```

Kỳ vọng:
- `meetings.has_investment_demand = 1`, `has_maintenance_demand = 0`
- `meeting_investment_demands` có **1 dòng**: `scope_id = 1`, `scope_name` là tên đầy đủ từ ERP, `expected_amount = 1500000000.00`, `expected_start_date = 2027-03-15`, `position = 0`, **`created_by` không NULL**

Nếu `has_investment_demand` vẫn NULL và bảng chi tiết rỗng → Bước 1 chưa làm.

- [ ] **Bước 7: Dựng hàm gọi dùng chung cho 6 ca verify tiếp theo**

```bash
# Dán vào shell 1 lần, dùng cho Bước 8-12
post_meeting () {   # $1 = status, $2 = phần JSON khảo sát
  curl -s -X POST "http://127.0.0.1:8000/api/v1/assign/meeting/$MEETING_ID" \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
    -w '\nHTTP %{http_code}\n' \
    -d "{
      \"name\":\"Test khao sat\",
      \"meeting_type_id\":$SYS_ID,
      \"status\":$1,
      \"start_date\":\"2027-01-10 09:00:00\",
      \"end_date\":\"2027-01-10 11:00:00\",
      \"mode_id\":1,
      \"location\":\"HN\",
      \"company_members\":[{\"name\":\"NV A\",\"attendance_status\":1}],
      $2
    }"
}
```

⚠️ `attendance_status` bắt buộc có giá trị 1/2/3 khi `status = 3` — guard điểm danh sẵn có ở `MeetingController::update()` chạy **trước**, thiếu nó sẽ ra 400 "Vui lòng hoàn thành điểm danh…" chứ không phải 400 khảo sát.

- [ ] **Bước 8: Verify 400 khi Hoàn thành thiếu đáp án câu 1 & 3**

```bash
post_meeting 3 '"has_investment_demand":null,"has_maintenance_demand":null,"investment_demands":[]'
```

Kỳ vọng: HTTP **400**; body có key `has_investment_demand` = "Vui lòng trả lời câu hỏi về nhu cầu đầu tư của khách hàng." **và** `has_maintenance_demand` = "Vui lòng trả lời câu hỏi về nhu cầu dịch vụ sửa chữa, bảo dưỡng/bảo trì."

- [ ] **Bước 9: Verify 400 khi Có nhưng không chọn lĩnh vực nào**

```bash
post_meeting 3 '"has_investment_demand":1,"has_maintenance_demand":0,"investment_demands":[]'
```

Kỳ vọng: HTTP **400**, key `investment_demands` = "Vui lòng chọn ít nhất một lĩnh vực đầu tư."

- [ ] **Bước 10: Verify 400 khi tích lĩnh vực nhưng bỏ trống tiền/ngày**

```bash
post_meeting 3 '"has_investment_demand":1,"has_maintenance_demand":0,"investment_demands":[{"scope_id":1}]'
```

Kỳ vọng: HTTP **400**, có **cả 2** key `investment_demands.0.expected_amount` = "Vui lòng nhập mức đầu tư dự kiến." và `investment_demands.0.expected_start_date` = "Vui lòng chọn thời gian dự kiến bắt đầu."

- [ ] **Bước 11: Verify ngày quá khứ bị chặn ở BE**

```bash
post_meeting 3 '"has_investment_demand":1,"has_maintenance_demand":0,"investment_demands":[{"scope_id":1,"expected_amount":1000,"expected_start_date":"2020-01-01"}]'
```

Kỳ vọng: HTTP **400**, key `investment_demands.0.expected_start_date` = "Phải lớn hơn hoặc bằng ngày hiện tại."

- [ ] **Bước 12: Verify Lưu (chưa Hoàn thành) KHÔNG bị chặn — regression**

```bash
post_meeting 2 '"has_investment_demand":null,"has_maintenance_demand":null,"investment_demands":[]'
```

Kỳ vọng: HTTP **200**. Bắt buộc chỉ áp khi `status = 3` — ra 400 ở đây là rule đặt sai chỗ.

- [ ] **Bước 13: Verify loại meeting khác không bị đòi khảo sát — regression**

```bash
# meeting_type_id = 2 (Meeting nội bộ, has_customer = 0)
curl -s -X POST "http://127.0.0.1:8000/api/v1/assign/meeting/$MEETING_ID" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -w '\nHTTP %{http_code}\n' \
  -d "{\"name\":\"Test noi bo\",\"meeting_type_id\":2,\"status\":3,
       \"start_date\":\"2027-01-10 09:00:00\",\"end_date\":\"2027-01-10 11:00:00\",
       \"mode_id\":1,\"location\":\"HN\",
       \"company_members\":[{\"name\":\"NV A\",\"attendance_status\":1}],
       \"conclusion\":\"Ket luan test\"}"
```

Kỳ vọng: HTTP **200**, không có key lỗi nào bắt đầu bằng `has_investment` / `has_maintenance` / `investment_demands`.

- [ ] **Bước 14: Verify cascade xoá**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" "$DB_DATABASE" -e "
  DELETE FROM meetings WHERE id=<id meeting test dùng 1 lần>;
  SELECT COUNT(*) AS con_lai FROM meeting_investment_demands WHERE meeting_id=<id đó>;"
```

Kỳ vọng: `con_lai = 0`.

---

### Task 3.4: Component FE `MeetingInvestmentSurvey.vue`

**Files:**
- Create: `hrm-client/pages/assign/meeting/components/MeetingInvestmentSurvey.vue`

**Interfaces:**
- Consumes: `optionsSelect/fetchInvestmentScopes` (Task 2.2) — **dùng GIÁ TRỊ RETURN, KHÔNG đọc getter `getInvestmentScopes`**: getter chỉ chứa mục active (cache dùng chung), lĩnh vực đã khoá mà bản ghi này đang dùng chỉ có trong giá trị return. `MEETING_TYPE_PRODUCT_INTRO` (Task 2.2), field `investment_demands` từ API (Task 3.3)
- Produces:
  - Props: `form` (Object, required), `isShow` (Boolean, default false), `formError` (Object, default `() => ({})`)
  - Method public `buildPayload()` → `{ has_investment_demand: 0|1|null, has_maintenance_demand: 0|1|null, investment_demands: Array<{scope_id, scope_name, expected_amount, expected_start_date}> }`
  - Method public `loadScopes()` → `Promise<void>` (gọi khi mở tab Biên bản)

- [ ] **Bước 1: Rà pattern sẵn có trước khi code**

```bash
cd HRM/hrm-client
grep -rn "V2BaseRadio\|b-form-radio" pages/assign components | head -10
grep -rn "formatCurrency\|formatNumber\|thousand" utils/*.js | head -10
grep -rn "disabled-date" pages/assign/meeting/components/MeetingReport.vue
```

Ghi lại vào comment đầu component: "copy pattern radio từ `<file:dòng>`, format số từ `<file:dòng>`, disabled-date từ `MeetingReport.vue:141`". Nếu **không** tìm thấy helper format số dùng chung → tạo `utils/formatMoney.js` và ghi chú để lần sau không lệch.

- [ ] **Bước 2: Viết template**

Các thuộc tính `data-testid` bên dưới là **bắt buộc** — E2E ở Task 5.1 bám vào chúng. Không đổi tên, không bỏ đi.

```html
<template>
    <div data-testid="investment-survey">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <div class="sec-title">
                <i class="ri-search-eye-line text-brand mr-1"></i>Khảo sát nhu cầu khách hàng
            </div>
        </div>

        <!-- Câu 1 -->
        <div class="mb-3">
            <div class="mb-2">
                1. Anh/Chị có nhu cầu đầu tư trong thời gian tới? <Required />
            </div>
            <div class="d-flex align-items-center" style="gap: 24px">
                <b-form-radio v-model="answer1" :value="1" :disabled="isShow" data-testid="q1-yes" @change="onChangeAnswer1(1)">Có</b-form-radio>
                <b-form-radio v-model="answer1" :value="0" :disabled="isShow" data-testid="q1-no" @change="onChangeAnswer1(0)">Không</b-form-radio>
            </div>
            <V2BaseError
                v-if="formError['has_investment_demand']"
                :message="formError['has_investment_demand'][0]"
            />
        </div>

        <!-- Câu 2 — chỉ hiện khi câu 1 = Có -->
        <div v-if="answer1 === 1" class="mb-3">
            <div class="mb-2">
                2. Anh/Chị đầu tư vào lĩnh vực nào TPE cung cấp? <Required />
                <span style="color: #6b7280">(chọn nhiều)</span>
            </div>

            <div v-if="loadingScopes" class="py-2" style="color: #6b7280">Đang tải danh mục lĩnh vực...</div>
            <div v-else-if="scopeLoadFailed" class="py-2 text-danger">
                Không tải được danh mục lĩnh vực. Vui lòng thử lại.
                <a href="javascript:void(0)" @click="loadScopes">Tải lại</a>
            </div>

            <template v-else>
                <div class="row header-row px-1">
                    <div class="col-1">Chọn</div>
                    <div class="col-5">Lĩnh vực</div>
                    <div class="col-3">Mức đầu tư dự kiến (VNĐ)</div>
                    <div class="col-3">Thời gian dự kiến bắt đầu</div>
                </div>

                <div
                    v-for="(row, i) in rows"
                    :key="'sc-' + row.scope_id"
                    class="row g-2 align-items-center mb-2"
                    data-testid="scope-row"
                    :data-scope-id="row.scope_id"
                >
                    <div class="col-1 text-center">
                        <V2BaseCheckbox
                            :modelValue="row.checked"
                            :disabled="isShow || (row.missing && !row.checked)"
                            data-testid="scope-check"
                            @change="onToggleRow(i, $event)"
                        />
                    </div>
                    <div class="col-5">
                        <span style="color: #374151">{{ row.scope_name }}</span>
                    </div>
                    <div class="col-3">
                        <V2BaseInput
                            v-model="row.amount_text"
                            :disabled="isShow || !row.checked"
                            placeholder="Nhập mức đầu tư dự kiến"
                            data-testid="scope-amount"
                            @input="onAmountInput(i, $event)"
                        />
                        <V2BaseError
                            v-if="errorFor(i, 'expected_amount')"
                            :message="errorFor(i, 'expected_amount')"
                        />
                    </div>
                    <div class="col-3" data-testid="scope-date">
                        <V2BaseDatePicker
                            v-model="row.expected_start_date"
                            type="date"
                            value-type="YYYY-MM-DD"
                            format="DD/MM/YYYY"
                            size="sm"
                            :disabled="isShow || !row.checked"
                            :disabled-date="(date) => date < new Date(new Date().setHours(0, 0, 0, 0))"
                        />
                        <V2BaseError
                            v-if="errorFor(i, 'expected_start_date')"
                            :message="errorFor(i, 'expected_start_date')"
                        />
                    </div>
                </div>

                <V2BaseError v-if="formError['investment_demands']" :message="formError['investment_demands'][0]" />
            </template>
        </div>

        <!-- Câu 3 -->
        <div>
            <div class="mb-2">
                3. Anh/Chị có nhu cầu về dịch vụ sửa chữa bảo dưỡng/bảo trì máy móc thiết bị? <Required />
            </div>
            <div class="d-flex align-items-center" style="gap: 24px">
                <b-form-radio v-model="answer3" :value="1" :disabled="isShow" data-testid="q3-yes">Có</b-form-radio>
                <b-form-radio v-model="answer3" :value="0" :disabled="isShow" data-testid="q3-no">Không</b-form-radio>
            </div>
            <V2BaseError
                v-if="formError['has_maintenance_demand']"
                :message="formError['has_maintenance_demand'][0]"
            />
        </div>
    </div>
</template>
```

- [ ] **Bước 3: Viết script**

```html
<script>
export default {
    name: 'MeetingInvestmentSurvey',
    props: {
        form: { type: Object, required: true },
        isShow: { type: Boolean, default: false },
        formError: { type: Object, default: () => ({}) },
    },
    data() {
        return {
            answer1: null,
            answer3: null,
            rows: [],
            // Danh mục lĩnh vực dùng để dựng bảng — LẤY TỪ GIÁ TRỊ RETURN của action,
            // KHÔNG đọc getter: getter chỉ chứa mục active (cache dùng chung toàn app),
            // còn lĩnh vực đã khoá mà bản ghi này đang dùng chỉ có trong giá trị return.
            scopeOptions: [],
            loadingScopes: false,
            scopeLoadFailed: false,
        }
    },
    computed: {
        /** Gom state khảo sát để watcher ghi ngược vào `form` (xem watch.surveyState) */
        surveyState() {
            return {
                a1: this.answer1,
                a3: this.answer3,
                rows: this.rows.map((r) => ({
                    id: r.scope_id,
                    c: r.checked,
                    a: r.amount_text,
                    d: r.expected_start_date,
                })),
            }
        },
    },
    watch: {
        'form.id': {
            immediate: true,
            handler() {
                this.hydrateFromForm()
            },
        },
        /**
         * Ghi ngược đáp án vào `form` mỗi khi user đổi.
         *
         * BẮT BUỘC: `unsavedChangesMixin` ở MeetingForm theo dõi object `form`.
         * Đáp án khảo sát nằm trong data riêng của component -> không ghi ngược thì
         * user sửa khảo sát rồi thoát màn sẽ KHÔNG được cảnh báo mất dữ liệu.
         *
         * An toàn, không lặp vô hạn: hydrateFromForm() chỉ chạy theo `form.id`,
         * không watch `form.investment_demands`.
         */
        surveyState: {
            deep: true,
            handler() {
                const payload = this.buildPayload()
                this.$set(this.form, 'has_investment_demand', payload.has_investment_demand)
                this.$set(this.form, 'has_maintenance_demand', payload.has_maintenance_demand)
                this.$set(this.form, 'investment_demands', payload.investment_demands)
            },
        },
    },
    methods: {
        /** Nạp danh mục lĩnh vực (lazy) — MeetingReport gọi khi mở tab Biên bản */
        async loadScopes() {
            if (this.loadingScopes) return
            this.loadingScopes = true
            this.scopeLoadFailed = false
            try {
                const includeIds = (this.form.investment_demands || []).map((d) => Number(d.scope_id))
                // Dùng GIÁ TRỊ RETURN, không đọc getter — xem comment ở data.scopeOptions
                const scopes = await this.$store.dispatch('optionsSelect/fetchInvestmentScopes', { includeIds })
                this.scopeOptions = scopes || []
                this.scopeLoadFailed = this.scopeOptions.length === 0
                this.buildRows()
            } finally {
                this.loadingScopes = false
            }
        },

        /** Đọc đáp án đã lưu từ form (mở màn Sửa/Chi tiết) */
        hydrateFromForm() {
            const a1 = this.form.has_investment_demand
            const a3 = this.form.has_maintenance_demand
            this.answer1 = a1 === null || a1 === undefined ? null : Number(a1)
            this.answer3 = a3 === null || a3 === undefined ? null : Number(a3)
            this.buildRows()
        },

        /**
         * Ghép danh mục lĩnh vực với đáp án đã lưu.
         * Lĩnh vực đã chọn mà ERP đã xoá hẳn -> push dòng ảo từ snapshot (missing = true),
         * hiển thị đúng tên gốc, cho bỏ tích nhưng không cho tích lại.
         */
        buildRows() {
            const saved = this.form.investment_demands || []
            const savedById = {}
            saved.forEach((d) => {
                savedById[Number(d.scope_id)] = d
            })

            const rows = (this.scopeOptions || []).map((s) => {
                const d = savedById[s.id]
                return {
                    scope_id: s.id,
                    scope_name: s.name,
                    missing: false,
                    checked: !!d,
                    amount_text: d && d.expected_amount != null ? this.formatMoney(d.expected_amount) : '',
                    expected_start_date: d ? d.expected_start_date || null : null,
                }
            })

            const knownIds = rows.map((r) => r.scope_id)
            saved.forEach((d) => {
                const id = Number(d.scope_id)
                if (knownIds.includes(id)) return
                rows.push({
                    scope_id: id,
                    scope_name: d.scope_name || '(Lĩnh vực đã bị xoá bên ERP)',
                    missing: true,
                    checked: true,
                    amount_text: d.expected_amount != null ? this.formatMoney(d.expected_amount) : '',
                    expected_start_date: d.expected_start_date || null,
                })
            })

            this.rows = rows
        },

        onToggleRow(i, checked) {
            const row = this.rows[i]
            row.checked = !!checked
            if (!row.checked) {
                // Bỏ tích -> xoá luôn giá trị, không giữ ngầm rồi lưu nhầm
                row.amount_text = ''
                row.expected_start_date = null
            }
            this.$set(this.rows, i, row)
        },

        async onChangeAnswer1(value) {
            if (value === 0 && this.rows.some((r) => r.checked)) {
                const ok = await this.$confirm({
                    title: 'Xoá dữ liệu lĩnh vực đầu tư?',
                    message:
                        'Chuyển sang "Không" sẽ xoá toàn bộ lĩnh vực đã chọn cùng mức đầu tư và thời gian đã nhập. Bạn có chắc chắn?',
                    textAccept: 'Xoá',
                })
                if (!ok) {
                    this.$nextTick(() => {
                        this.answer1 = 1
                    })
                    return
                }
            }
            if (value === 0) {
                this.rows.forEach((r, i) => this.onToggleRow(i, false))
            }
        },

        onAmountInput(i, value) {
            const digits = String(value || '').replace(/\D/g, '')
            this.rows[i].amount_text = digits ? this.formatMoney(digits) : ''
            this.$set(this.rows, i, this.rows[i])
        },

        formatMoney(value) {
            const n = String(value).replace(/\D/g, '')
            return n.replace(/\B(?=(\d{3})+(?!\d))/g, '.')
        },

        toNumber(text) {
            const digits = String(text || '').replace(/\D/g, '')
            return digits === '' ? null : Number(digits)
        },

        /** Map index trong payload -> key lỗi BE trả về */
        errorFor(rowIndex, field) {
            const payloadIndex = this.payloadIndexOf(rowIndex)
            if (payloadIndex < 0) return null
            const key = `investment_demands.${payloadIndex}.${field}`
            return this.formError[key] ? this.formError[key][0] : null
        },

        payloadIndexOf(rowIndex) {
            let idx = -1
            for (let i = 0; i <= rowIndex; i += 1) {
                if (this.rows[i] && this.rows[i].checked) idx += 1
            }
            return this.rows[rowIndex] && this.rows[rowIndex].checked ? idx : -1
        },

        /** MeetingForm gọi khi build payload lưu meeting */
        buildPayload() {
            return {
                has_investment_demand: this.answer1,
                has_maintenance_demand: this.answer3,
                investment_demands: this.rows
                    .filter((r) => r.checked)
                    .map((r) => ({
                        scope_id: r.scope_id,
                        scope_name: r.scope_name,
                        expected_amount: this.toNumber(r.amount_text),
                        expected_start_date: r.expected_start_date || null,
                    })),
            }
        },
    },
}
</script>
```

- [ ] **Bước 4: Verify component compile được**

```bash
cd HRM/hrm-client && nvm use 12 && NODE_OPTIONS=--max-old-space-size=8192 npm run dev
```

Kỳ vọng: build xong không lỗi. (Component chưa được nhúng nên chưa thấy trên UI — nhúng ở Task 3.5.)

---

### Task 3.5: Nhúng vào `MeetingReport.vue` + build payload ở `MeetingForm.vue`

**Files:**
- Modify: `hrm-client/pages/assign/meeting/components/MeetingReport.vue`
- Modify: `hrm-client/pages/assign/meeting/components/MeetingForm.vue`

**Interfaces:**
- Consumes: `MeetingInvestmentSurvey.buildPayload()` và `.loadScopes()` (Task 3.4)

- [ ] **Bước 1: Nhúng component vào `MeetingReport.vue`**

Ngay **sau** khối 1 "Biên bản cuộc họp" (sau `</div>` đóng khối, trước `<hr class="mt-4 mb-4" />` dẫn vào khối "Import tài liệu"), chèn:

```html
        <hr v-if="needInvestmentSurvey" class="mt-4 mb-4" />

        <MeetingInvestmentSurvey
            v-if="needInvestmentSurvey"
            ref="investmentSurvey"
            :form="form"
            :isShow="isShow"
            :formError="formError"
        />
```

Trong `<script>` của `MeetingReport.vue`:

```js
import MeetingInvestmentSurvey from './MeetingInvestmentSurvey.vue'
```

Thêm vào `components: { ... }`: `MeetingInvestmentSurvey,`

Khai prop mới + computed:

```js
    props: {
        // ...các prop cũ...
        isProductIntroType: { type: Boolean, default: false },
    },
    computed: {
        needInvestmentSurvey() {
            return this.isProductIntroType
        },
    },
```

⚠️ **TUYỆT ĐỐI KHÔNG đọc `form.meeting_type_code` cho điều kiện này.** Field đó chỉ có trong response API detail → màn **Tạo mới không bao giờ có nó** (khối khảo sát sẽ không bao giờ hiện), và màn Sửa thì **stale** khi user đổi dropdown loại meeting.

Nguồn đúng là dropdown. Trong `MeetingForm.vue`, thêm computed ngay cạnh `hasCustomer` (`MeetingForm.vue:357-362`) và bám đúng khuôn đó:

```js
import { MEETING_TYPE_PRODUCT_INTRO } from '@/utils/meetingTypeCodes'
// ...
        /** Loại meeting hệ thống "Họp tìm hiểu & Giới thiệu sản phẩm" -> hiện khối Khảo sát */
        isProductIntroType() {
            return this.selectedMeetingType
                ? this.selectedMeetingType.code === MEETING_TYPE_PRODUCT_INTRO
                : false
        },
```

rồi truyền xuống đúng như `hasCustomer` đang được truyền:

```html
        <MeetingReport ... :isProductIntroType="isProductIntroType" />
```

`selectedMeetingType` khớp theo `form.meeting_type_id` nên bám thẳng dropdown, phản ứng tức thì ở cả tạo mới lẫn sửa. `MeetingTypeResource` đã trả `code` cho mỗi loại meeting (Task 1.5).

- [ ] **Bước 2: Lazy-load danh mục khi tab Biên bản mở**

Trong `MeetingReport.vue`, thêm watcher (tab dùng `v-show` nên component luôn mounted — phải bắt lúc tab thực sự hiện):

```js
    watch: {
        needInvestmentSurvey: {
            immediate: true,
            handler(val) {
                if (!val) return
                this.$nextTick(() => {
                    if (this.$refs.investmentSurvey) this.$refs.investmentSurvey.loadScopes()
                })
            },
        },
    },
```

- [ ] **Bước 3: Đưa payload khảo sát vào request lưu meeting**

Trong `MeetingForm.vue`, tìm chỗ dựng payload trước khi gọi `apiPostMethod` (`~dòng 776` và `~934`). Thêm ngay trước khi gửi:

```js
            const surveyRef = this.$refs.meetingReport && this.$refs.meetingReport.$refs.investmentSurvey
            if (surveyRef) {
                Object.assign(payload, surveyRef.buildPayload())
            }
```

(Đặt tên biến payload theo đúng biến đang có trong hàm đó.)

- [ ] **Bước 4: Build + verify UI**

```bash
cd HRM/hrm-client && nvm use 12 && NODE_OPTIONS=--max-old-space-size=8192 npm run dev
```

Tạo meeting loại "Họp tìm hiểu & Giới thiệu sản phẩm" → mở tab Biên bản.

Kỳ vọng:
- Khối "🔍 Khảo sát nhu cầu khách hàng" nằm **giữa** bảng "Biên bản cuộc họp" và "Import tài liệu kèm biên bản"
- Câu 2 **ẩn** khi chưa chọn hoặc chọn "Không"; chọn "Có" → hiện bảng **13 dòng** lĩnh vực
- Chưa tích dòng nào → 2 ô Mức đầu tư và Thời gian đều xám (disabled)
- Tích 1 dòng → 2 ô mở; gõ `1500000000` → hiển thị `1,500,000,000` (dấu phẩy — do `V2BaseCurrencyInput` dùng chung)
- Mở datepicker → ngày trước hôm nay bị mờ
- Bỏ tích → 2 ô xoá trắng và xám lại
- Đổi câu 1 sang "Không" khi đang có dòng đã tích → hiện popup xác nhận

- [ ] **Bước 5: Verify khối KHÔNG hiện với loại meeting khác**

Mở 1 meeting loại "Meeting nội bộ" → tab Biên bản.

Kỳ vọng: **không** thấy khối Khảo sát; Network **không** có request `investment-scopes`.

- [ ] **Bước 6: Verify lưu và mở lại**

Điền đủ câu 1 = Có + 2 lĩnh vực + câu 3, bấm Lưu, F5 mở lại tab Biên bản.

Kỳ vọng: đúng 2 dòng vẫn được tích, số tiền và ngày đúng như đã nhập, đúng thứ tự.

- [ ] **Bước 7: Verify lỗi validate hiện đúng ô**

Xoá trống Mức đầu tư của dòng thứ 2, bấm **Hoàn thành**.

Kỳ vọng: dòng thứ 2 viền đỏ + text "Vui lòng nhập mức đầu tư dự kiến." — **đúng dòng thứ 2**, không phải dòng khác (đây là bài kiểm tra `payloadIndexOf`).

- [ ] **Bước 8: Verify chế độ chỉ đọc**

Mở meeting đã Hoàn thành.

Kỳ vọng: radio và checkbox không bấm được, ô nhập không sửa được.

- [ ] **Bước 9: Verify cảnh báo thoát khi chưa lưu**

Mở tab Biên bản của meeting loại hệ thống, chỉ đổi **duy nhất** câu 1 sang "Có" (không đụng gì khác), rồi bấm "Quay lại".

Kỳ vọng: hiện popup cảnh báo mất dữ liệu chưa lưu.

Không hiện popup = watcher `surveyState` chưa ghi ngược vào `form` (Task 3.4) — `unsavedChangesMixin` chỉ theo dõi object `form`, không thấy `data` riêng của component.

- [ ] **Bước 10: Kiểm line ending**

```bash
cd HRM/hrm-client && git diff --stat pages/assign/meeting/components/
```

Kỳ vọng: chỉ vài chục dòng đổi trên 2 file đã sửa, `MeetingInvestmentSurvey.vue` là file mới.

---

# PHASE 4 — In & Excel

### Task 4.1: Section khảo sát trong bản In biên bản

**Files:**
- Modify: `hrm-api/resources/views/exports/meeting_record.blade.php`

**Interfaces:**
- Consumes: `$meeting->investment_demands` (Task 3.1), eager load ở `print()` (Task 3.3)

- [ ] **Bước 1: Chèn section trước "Kết luận cuộc họp"**

Mở file, tìm comment `<!-- Section {{$sectionNumber}}: Kết luận cuộc họp -->` (~dòng 259). Chèn **ngay trước** nó:

```blade
<!-- Section {{$sectionNumber}}: Khảo sát nhu cầu khách hàng (chỉ loại Họp tìm hiểu & Giới thiệu sản phẩm) -->
@if($meeting->requiresInvestmentSurvey())
    <div style="margin-bottom: 20px;">
        <div style="font-weight: bold; margin-bottom: 10px; font-family: 'Times New Roman', serif; font-size: 13px;">{{$sectionNumber}}. Khảo sát nhu cầu khách hàng (Customer needs survey):</div>

        <div style="margin-bottom: 8px; font-family: 'Times New Roman', serif; font-size: 13px;">
            {{$sectionNumber}}.1 Nhu cầu đầu tư trong thời gian tới:
            <strong>{{ $meeting->has_investment_demand === null ? 'Chưa trả lời' : ($meeting->has_investment_demand ? 'Có' : 'Không') }}</strong>
        </div>

        @if($meeting->has_investment_demand && $meeting->investment_demands->count())
            <div style="margin-bottom: 8px; font-family: 'Times New Roman', serif; font-size: 13px;">{{$sectionNumber}}.2 Lĩnh vực đầu tư:</div>
            <table style="width: 100%; border-collapse: collapse; font-family: 'Times New Roman', serif; font-size: 13px; margin-bottom: 8px;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #000; padding: 5px; width: 8%;">STT</th>
                        <th style="border: 1px solid #000; padding: 5px;">Lĩnh vực</th>
                        <th style="border: 1px solid #000; padding: 5px; width: 25%;">Mức đầu tư dự kiến (VNĐ)</th>
                        <th style="border: 1px solid #000; padding: 5px; width: 22%;">Thời gian dự kiến bắt đầu</th>
                    </tr>
                </thead>
                <tbody>
                @foreach($meeting->investment_demands as $idx => $d)
                    <tr>
                        <td style="border: 1px solid #000; padding: 5px; text-align: center;">{{ $idx + 1 }}</td>
                        <td style="border: 1px solid #000; padding: 5px;">{{ $d->scope_name }}</td>
                        <td style="border: 1px solid #000; padding: 5px; text-align: right;">{{ $d->expected_amount ? number_format($d->expected_amount, 0, ',', ',') : '' }}</td>
                        <td style="border: 1px solid #000; padding: 5px; text-align: center;">{{ $d->expected_start_date ? $d->expected_start_date->format('d/m/Y') : '' }}</td>
                    </tr>
                @endforeach
                </tbody>
            </table>
        @endif

        <div style="font-family: 'Times New Roman', serif; font-size: 13px;">
            {{$sectionNumber}}.3 Nhu cầu dịch vụ sửa chữa, bảo dưỡng/bảo trì máy móc thiết bị:
            <strong>{{ $meeting->has_maintenance_demand === null ? 'Chưa trả lời' : ($meeting->has_maintenance_demand ? 'Có' : 'Không') }}</strong>
        </div>
    </div>
    @php $sectionNumber++; @endphp
@endif
```

- [ ] **Bước 2: Kiểm print template có tồn tại**

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" "$DB_DATABASE" -Nse \
  "SELECT COUNT(*) FROM print_templates WHERE code='BIEN_BAN_CUOC_HOP'"
```

Kỳ vọng: `1`. Ra `0` → `/print` sẽ trả 400 "template of non-object"; seed bản ghi `print_templates` trước khi verify (lỗi hạ tầng local đã biết, không phải lỗi code feature này).

- [ ] **Bước 3: Verify bản in của meeting loại hệ thống**

Mở `http://127.0.0.1:3000/assign/meeting/<MEETING_ID>/print`.

Kỳ vọng:
- Có section "Khảo sát nhu cầu khách hàng (Customer needs survey)"
- Số thứ tự section **liên tục**, và section "Kết luận cuộc họp" ngay sau nó có số lớn hơn đúng 1
- Tiền hiển thị `1,500,000,000` (dấu PHẨY — user chốt 2026-08-21, khớp ô nhập trên màn hình), ngày `15/03/2027`

- [ ] **Bước 4: Verify meeting loại khác không có section này (regression)**

Mở bản in của 1 meeting "Meeting nội bộ".

Kỳ vọng: **không** có section Khảo sát; đánh số các section còn lại **không bị nhảy cóc**.

- [ ] **Bước 5: Verify câu 1 = Không thì không in bảng lĩnh vực**

Đổi meeting sang câu 1 = Không, in lại.

Kỳ vọng: có dòng `.1 ... Không` và `.3 ...`, **không** có mục `.2` và bảng lĩnh vực.

---

### Task 4.2: Khối khảo sát trong file Excel biên bản

**Files:**
- Modify: `hrm-client/pages/assign/meeting/components/MeetingReport.vue`

**Interfaces:**
- Consumes: `needInvestmentSurvey` (Task 3.5), `this.$refs.investmentSurvey.buildPayload()` (Task 3.4)

- [ ] **Bước 1: Chèn khối vào `exportMeetingExcel()`**

Trong `exportMeetingExcel()`, tìm khối "KẾT LUẬN CUỘC HỌP" (`~dòng 647`, bắt đầu bằng `rowCursor += 1; sectionNumber++;`). Chèn **ngay trước** nó:

```js
                // Khối Khảo sát nhu cầu khách hàng — chỉ với loại Họp tìm hiểu & Giới thiệu sản phẩm
                if (this.needInvestmentSurvey) {
                    const survey = this.$refs.investmentSurvey
                        ? this.$refs.investmentSurvey.buildPayload()
                        : { has_investment_demand: null, has_maintenance_demand: null, investment_demands: [] }

                    const yesNo = (v) => (v === null || v === undefined ? 'Chưa trả lời' : v ? 'Có' : 'Không')
                    // Chống formula injection: giá trị bắt đầu bằng = + - @ phải prefix dấu nháy đơn
                    const safeText = (v) => {
                        const s = String(v == null ? '' : v)
                        return /^[=+\-@]/.test(s) ? `'${s}` : s
                    }

                    rowCursor += 1
                    sectionNumber++
                    worksheet.mergeCells(`A${rowCursor}:F${rowCursor}`)
                    worksheet.getCell(`A${rowCursor}`).value = `${sectionNumber}. KHẢO SÁT NHU CẦU KHÁCH HÀNG`
                    worksheet.getCell(`A${rowCursor}`).font = { bold: true, size: 12 }
                    rowCursor += 1

                    worksheet.getCell(`A${rowCursor}`).value = '1. Nhu cầu đầu tư trong thời gian tới:'
                    worksheet.getCell(`B${rowCursor}`).value = yesNo(survey.has_investment_demand)
                    rowCursor += 1

                    if (survey.has_investment_demand === 1 && survey.investment_demands.length) {
                        worksheet.getCell(`A${rowCursor}`).value = '2. Lĩnh vực đầu tư:'
                        rowCursor += 1

                        const surveyCols = ['A', 'B', 'C', 'D']
                        worksheet.getCell(`A${rowCursor}`).value = 'STT'
                        worksheet.getCell(`B${rowCursor}`).value = 'Lĩnh vực'
                        worksheet.getCell(`C${rowCursor}`).value = 'Mức đầu tư dự kiến (VNĐ)'
                        worksheet.getCell(`D${rowCursor}`).value = 'Thời gian dự kiến bắt đầu'
                        surveyCols.forEach((col) => {
                            worksheet.getCell(`${col}${rowCursor}`).font = { bold: true }
                            worksheet.getCell(`${col}${rowCursor}`).border = borderThin
                        })
                        rowCursor += 1

                        survey.investment_demands.forEach((d, idx) => {
                            worksheet.getCell(`A${rowCursor}`).value = idx + 1
                            worksheet.getCell(`A${rowCursor}`).alignment = { horizontal: 'center' }
                            worksheet.getCell(`B${rowCursor}`).value = safeText(d.scope_name)
                            // Ghi SỐ (không phải chuỗi) để Excel SUM được
                            // !== null chứ KHÔNG dùng truthy: mức đầu tư = 0 là giá trị hợp lệ
                            // (rule cho phép min:0) và phải hiện ra "0", không được để trống
                            worksheet.getCell(`C${rowCursor}`).value =
                                d.expected_amount !== null && d.expected_amount !== undefined
                                    ? d.expected_amount
                                    : ''
                            worksheet.getCell(`C${rowCursor}`).numFmt = '#,##0'
                            worksheet.getCell(`D${rowCursor}`).value = d.expected_start_date
                                ? this.$dayjs(d.expected_start_date).format('DD/MM/YYYY')
                                : ''
                            worksheet.getCell(`D${rowCursor}`).alignment = { horizontal: 'center' }
                            surveyCols.forEach((col) => {
                                worksheet.getCell(`${col}${rowCursor}`).border = borderThin
                            })
                            rowCursor += 1
                        })
                    }

                    worksheet.getCell(`A${rowCursor}`).value =
                        '3. Nhu cầu dịch vụ sửa chữa, bảo dưỡng/bảo trì máy móc thiết bị:'
                    worksheet.getCell(`B${rowCursor}`).value = yesNo(survey.has_maintenance_demand)
                    rowCursor += 1
                }
```

⚠️ Kiểm `this.$dayjs` có tồn tại trong màn này không (`grep -n "dayjs" pages/assign/meeting/components/MeetingReport.vue`). Nếu không có thì `import dayjs from 'dayjs'` và dùng `dayjs(...)`.

- [ ] **Bước 2: Build + xuất Excel meeting loại hệ thống**

Mở meeting đã điền khảo sát → tab Biên bản → nút **Excel**.

Kỳ vọng: file `Bien_ban_cuoc_hop_<mã>.xlsx` tải về, mở lên có khối "KHẢO SÁT NHU CẦU KHÁCH HÀNG" nằm **trước** khối "KẾT LUẬN CUỘC HỌP", số thứ tự section liên tục.

- [ ] **Bước 3: Verify ô tiền là SỐ, không phải chuỗi**

Trong Excel, click ô Mức đầu tư → gõ `=SUM(C<đầu>:C<cuối>)` ở ô trống.

Kỳ vọng: ra tổng đúng (nếu là chuỗi sẽ ra `0`).

- [ ] **Bước 4: Verify meeting loại khác (regression)**

Xuất Excel 1 meeting "Meeting nội bộ".

Kỳ vọng: **không** có khối Khảo sát, các section khác đánh số liên tục như trước.

- [ ] **Bước 5: Verify chống formula injection**

Tạm đổi tên 1 lĩnh vực bên ERP thành `=1+1`:

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" erp2326 -e "UPDATE scopes SET name='=1+1' WHERE id=3;"
```

Tích lĩnh vực đó, lưu, xuất Excel.

Kỳ vọng: ô hiện chuỗi `=1+1`, **không** tính ra `2`.

```bash
# Trả lại nguyên trạng
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" erp2326 -e "UPDATE scopes SET name='Thiết bị làm sạch' WHERE id=3;"
```

---

# PHASE 5 — E2E & nghiệm thu

### Task 5.1: E2E Playwright

**Files:**
- Create: `HRM/e2e/tests/assign/meeting-investment-survey.spec.ts`

**Interfaces:**
- Consumes: toàn bộ Phase 1-4. Dùng lại `e2e/pages/LoginPage.ts` và cấu trúc của `e2e/tests/assign/quotation-unit-select.spec.ts`.

- [ ] **Bước 1: Đọc file mẫu để bám đúng khuôn**

```bash
cd HRM/e2e && sed -n '1,60p' tests/assign/quotation-unit-select.spec.ts && cat pages/LoginPage.ts
```

Bám đúng cách login, cách chờ, cách đặt `test.describe` của file đó. **Không** tự chế khuôn mới.

- [ ] **Bước 2: Viết spec**

Tạo `tests/assign/meeting-investment-survey.spec.ts`. Selector bám vào `data-testid` đã gắn ở Task 3.4 Bước 2, nên không cần codegen dò DOM.

```ts
import { test, expect, Page } from '@playwright/test'
import { LoginPage } from '../../pages/LoginPage'

// id meeting dựng sẵn cho E2E — điền trước khi chạy (xem Bước 3)
const SYSTEM_MEETING_ID = process.env.E2E_SYSTEM_MEETING_ID as string
const INTERNAL_MEETING_ID = process.env.E2E_INTERNAL_MEETING_ID as string
const SYSTEM_TYPE_NAME = 'Họp tìm hiểu & Giới thiệu sản phẩm'

async function openReportTab(page: Page, meetingId: string) {
    await page.goto(`/assign/meeting/${meetingId}/edit`)
    await page.getByRole('tab', { name: /Biên bản/i }).click()
}

test.beforeEach(async ({ page }) => {
    await new LoginPage(page).login()
})

test('1. Loại meeting hệ thống bị khoá Sửa/Xoá/Khoá ở màn danh mục', async ({ page }) => {
    await page.goto('/assign/meeting_type')

    const sysRow = page.locator('tr', { hasText: SYSTEM_TYPE_NAME }).first()
    await expect(sysRow).toBeVisible()
    await expect(sysRow.locator('.ri-edit-line')).toHaveCount(0)
    await expect(sysRow.locator('.ri-delete-bin-6-line')).toHaveCount(0)
    await expect(sysRow.locator('.ri-lock-line, .ri-lock-unlock-line')).toHaveCount(0)
    await expect(sysRow.locator('input[type="checkbox"]')).toHaveCount(0)
    await expect(sysRow.locator('.ri-eye-line')).toHaveCount(1)

    // Regression: loại meeting thường vẫn đủ nút
    const normalRow = page.locator('tr', { hasText: 'Meeting nội bộ' }).first()
    await expect(normalRow.locator('.ri-edit-line')).toHaveCount(1)
    await expect(normalRow.locator('.ri-delete-bin-6-line')).toHaveCount(1)
})

test('2. Khối khảo sát chỉ hiện với đúng loại meeting', async ({ page }) => {
    await openReportTab(page, SYSTEM_MEETING_ID)
    await expect(page.getByTestId('investment-survey')).toBeVisible()

    await openReportTab(page, INTERNAL_MEETING_ID)
    await expect(page.getByTestId('investment-survey')).toHaveCount(0)
})

test('3. Câu 2 hiện/ẩn theo câu 1, đủ 13 lĩnh vực', async ({ page }) => {
    await openReportTab(page, SYSTEM_MEETING_ID)

    await page.getByTestId('q1-no').check()
    await expect(page.getByTestId('scope-row')).toHaveCount(0)

    await page.getByTestId('q1-yes').check()
    await expect(page.getByTestId('scope-row')).toHaveCount(13)
})

test('4. Ô con khoá theo checkbox và format phân cách nghìn', async ({ page }) => {
    await openReportTab(page, SYSTEM_MEETING_ID)
    await page.getByTestId('q1-yes').check()

    const row = page.getByTestId('scope-row').first()
    const amount = row.getByTestId('scope-amount')
    const check = row.getByTestId('scope-check')

    await expect(amount).toBeDisabled()

    await check.check()
    await expect(amount).toBeEnabled()
    await amount.fill('1500000000')
    await expect(amount).toHaveValue('1,500,000,000')

    await check.uncheck()
    await expect(amount).toBeDisabled()
    await expect(amount).toHaveValue('')
})

test('5. Chặn Hoàn thành khi thiếu đáp án bắt buộc', async ({ page }) => {
    await openReportTab(page, SYSTEM_MEETING_ID)

    // Để trống cả 3 câu -> đòi câu 1 và câu 3
    await page.getByRole('button', { name: /Hoàn thành/i }).click()
    await expect(
        page.getByText('Vui lòng trả lời câu hỏi về nhu cầu đầu tư của khách hàng.')
    ).toBeVisible()
    await expect(
        page.getByText('Vui lòng trả lời câu hỏi về nhu cầu dịch vụ sửa chữa, bảo dưỡng/bảo trì.')
    ).toBeVisible()

    // Tích lĩnh vực dòng 2 nhưng bỏ trống tiền -> lỗi phải nằm ĐÚNG dòng 2
    await page.getByTestId('q1-yes').check()
    await page.getByTestId('q3-no').check()
    const row2 = page.getByTestId('scope-row').nth(1)
    await row2.getByTestId('scope-check').check()
    await page.getByRole('button', { name: /Hoàn thành/i }).click()

    await expect(row2.getByText('Vui lòng nhập mức đầu tư dự kiến.')).toBeVisible()
    const row1 = page.getByTestId('scope-row').nth(0)
    await expect(row1.getByText('Vui lòng nhập mức đầu tư dự kiến.')).toHaveCount(0)
})

test('6. Lưu rồi mở lại giữ đúng đáp án', async ({ page }) => {
    await openReportTab(page, SYSTEM_MEETING_ID)

    await page.getByTestId('q1-yes').check()
    await page.getByTestId('q3-yes').check()

    const row = page.getByTestId('scope-row').first()
    const scopeId = await row.getAttribute('data-scope-id')
    await row.getByTestId('scope-check').check()
    await row.getByTestId('scope-amount').fill('1500000000')
    await row.getByTestId('scope-date').locator('input').fill('15/03/2027')
    await page.keyboard.press('Escape')

    await page.getByRole('button', { name: /^Lưu/i }).first().click()
    await expect(page.getByText(/thành công/i)).toBeVisible()

    await openReportTab(page, SYSTEM_MEETING_ID)
    const savedRow = page.locator(`[data-testid="scope-row"][data-scope-id="${scopeId}"]`)
    await expect(savedRow.getByTestId('scope-check')).toBeChecked()
    await expect(savedRow.getByTestId('scope-amount')).toHaveValue('1,500,000,000')
})
```

⚠️ Tên nút footer (`Hoàn thành`, `Lưu`) và selector tab lấy từ `V2Footer` / `V2BaseTabNavigation` — nếu regex không khớp, mở `pages/assign/meeting/components/MeetingForm.vue` xem nhãn thật rồi sửa **regex trong test**, KHÔNG sửa nhãn ở app.

- [ ] **Bước 2b: Dựng 2 meeting cho E2E**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute="
\$sys = Modules\Assign\Entities\MeetingType::where('code','HOP_TIM_HIEU_GIOI_THIEU_SP')->first();
echo 'E2E_SYSTEM_MEETING_ID=' . Modules\Assign\Entities\Meeting\Meeting::where('meeting_type_id',\$sys->id)->whereIn('status',[0,1,2])->value('id') . PHP_EOL;
echo 'E2E_INTERNAL_MEETING_ID=' . Modules\Assign\Entities\Meeting\Meeting::where('meeting_type_id',2)->whereIn('status',[0,1,2])->value('id') . PHP_EOL;
"
```

Ra rỗng thì tạo tay 2 meeting qua UI (1 loại hệ thống, 1 "Meeting nội bộ", trạng thái Chốt lịch) rồi ghi 2 biến vào `HRM/e2e/.env`.

- [ ] **Bước 3: Chạy E2E**

```bash
# terminal A
cd HRM/hrm-client && nvm use 12 && NODE_OPTIONS=--max-old-space-size=8192 npm run dev
# terminal B
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan serve
# terminal C
cd HRM/e2e && nvm use && npx playwright test tests/assign/meeting-investment-survey.spec.ts
```

Kỳ vọng: **6/6 PASS**.

Lưu ý về ca phân quyền: feature này **không thêm quyền mới**, nên phần "fail-closed" ở đây là **5 guard 423** của danh mục loại meeting — được phủ bằng curl ở Task 1.4 Bước 7 và chạy lại ở Task 5.2 (T-3), không đưa vào E2E vì Playwright không gọi thẳng API danh mục.

- [ ] **Bước 4: Xem report khi có ca fail**

```bash
cd HRM/e2e && npm run report
```

---

### Task 5.2: Chạy toàn bộ bộ nghiệm thu của spec

**Files:** không sửa file nào — chỉ verify.

- [ ] **Bước 1: Chạy 20 test case mục 13 của spec**

Mở `docs/superpowers/specs/2026-08-21-meeting-tim-hieu-gioi-thieu-sp-design.md` mục 13, chạy tay từng ca T-1 → T-20 trên data thật, tick từng dòng.

Các ca **chưa** được E2E phủ, bắt buộc làm tay:
- **T-3**: 5 endpoint danh mục trả 423 (curl — đã làm ở Task 1.4 Bước 7, chạy lại xác nhận)
- **T-12, T-13**: In biên bản + Excel (Task 4.1/4.2 — chạy lại xác nhận)
- **T-14**: khoá lĩnh vực bên ERP rồi mở lại meeting đã chọn nó → vẫn hiện đúng tên
- **T-15**: xoá meeting → dòng chi tiết bị xoá theo
- **T-17**: vào 2 meeting liên tiếp → `investment-scopes` chỉ gọi 1 lần
- **T-18**: bắt lỗi quên `$request->only()`
- **T-19**: sửa 1 loại meeting thường → cột Người cập nhật ra tên
- **T-20**: chỉ đổi câu 1 rồi Quay lại → có cảnh báo mất dữ liệu chưa lưu

- [ ] **Bước 2: Rà lại toàn bộ diff**

```bash
cd HRM/hrm-api && git status --short && git diff --stat
cd HRM/hrm-client && git status --short && git diff --stat
```

Kỳ vọng:
- `hrm-api`: 3 migration + 1 seeder + 2 entity mới; 8 file sửa
- `hrm-client`: 2 file mới (`utils/meetingTypeCodes.js`, `MeetingInvestmentSurvey.vue`); 4 file sửa
- **Không** file nào bị đánh dấu đổi toàn bộ (dấu hiệu phá line ending)

- [ ] **Bước 3: Rà `git diff` tìm cờ quyền hard-code**

```bash
cd HRM/hrm-client && git diff | grep -nE "can[A-Za-z]*\s*=\s*true"
```

Kỳ vọng: **không có kết quả**.

- [ ] **Bước 4: Dọn dữ liệu test**

Xoá các meeting test đã tạo; trả `erp2326.scopes` về nguyên trạng (`status = 1` hết, tên lĩnh vực id=3 đúng gốc).

```bash
mysql -h127.0.0.1 -uroot -p"$DB_PASSWORD" erp2326 -e "SELECT id, name, status FROM scopes ORDER BY id;"
```

Kỳ vọng: 13 dòng, `status = 1` tất cả, tên đúng như mục 3.6 của spec.

- [ ] **Bước 5: Cập nhật `plan.md` + `STATUS.md`**

Tick `[x]` mọi task đã xong, ghi checkpoint theo format bắt buộc của `CLAUDE.md`, cập nhật `.plans/STATUS.md`.

---

## Checkpoint

### Checkpoint — 2026-08-22 (wrap up)
Vừa hoàn thành: **13/13 task code + final review đóng vòng** + **3 đợt tinh chỉnh UI theo yêu cầu user** (bố cục I–V cho cả bản in lẫn màn hình, bảng có border, căn nhãn, cỡ chữ tiêu đề bản in, gộp ghi chú vào tiêu đề, giảm khoảng cách).
Đang làm dở: không có việc code nào đang dở.
Bước tiếp theo (đều cần USER làm vì liên quan môi trường/mắt người):
  1. Chạy seeder trên `hrm_tpe` — DB mới có 6 loại meeting, **thiếu bản ghi hệ thống** nên chưa chọn được loại "Họp tìm hiểu & Giới thiệu sản phẩm" để thử
  2. Build FE xem bằng mắt tab Biên bản ở CẢ 2 loại meeting (có / không có khảo sát)
  3. Chạy lại E2E trên DB đúng — **ưu tiên ca "đủ 13 lĩnh vực"** (13 = đọc đúng `erp2326`, 22 = đọc nhầm connection mặc định)
  4. Chạy 19 test case nghiệm thu (T-20 đã chuyển ngoài scope)
  5. Dọn fixture rác: meeting 43/44/46/47 ở `hrm_erp`; `employees.employee_work_position_id` của id 1170 đã bị đổi thành 17
Blocked: không có blocker kỹ thuật; chỉ chờ user chạy seeder + nhìn giao diện.

---

## Commit của feature (local, CHƯA push)

**hrm-api** (`134cdf6`..`fa723d0`):
| commit | nội dung |
|---|---|
| `fcccceb` | 3 migration |
| `91bdd89` | loại meeting hệ thống + 5 guard 423 |
| `ba480fd` | endpoint danh mục lĩnh vực từ ERP |
| `e34067d` | lưu + validate đáp án khảo sát |
| `16d2907` | fix `exists` + `distinct` cho `scope_id` |
| `0307b86` | section khảo sát trong bản In |
| `dc56043` | in mức đầu tư = 0 thay vì để trống |
| `fa723d0` | vá finding review cuối phía BE |

**hrm-client** (`b2e9c1c`..`38f7e60`):
| commit | nội dung |
|---|---|
| `e51d159` | ẩn nút Sửa/Xoá/Khoá cho loại meeting hệ thống |
| `2592830` | store cache danh mục lĩnh vực |
| `f975e7d` | fix cache chỉ giữ mục active |
| `82c1bc7` | component khối khảo sát |
| `08cf2dfb` | nhúng khối vào tab Biên bản |
| `eab3431` | fix điều kiện hiện khối (theo dropdown, không theo field stale) |
| `9e16d63` | khối khảo sát trong file Excel |
| `38f7e60` | hiện lỗi lĩnh vực + chặn tích lại lĩnh vực đã khoá |

**e2e**: `tests/assign/meeting-investment-survey.spec.ts` (6 ca)

---

# PHASE 6 — Đổi nguồn khảo sát sang Lĩnh vực kinh doanh nội bộ + nhập theo Nhóm ngành

> **Cho agent thực thi:** dùng `superpowers:subagent-driven-development` (khuyến nghị) hoặc `superpowers:executing-plans`, làm từng task một. Các bước dùng checkbox `- [ ]`.

**Goal:** Khối "Khảo sát nhu cầu khách hàng" đọc danh mục **Lĩnh vực kinh doanh nội bộ** (`internal_business_scopes`, DB HRM) thay cho `scopes` bên ERP, và Mức đầu tư / Thời gian dự kiến nhập ở **cấp Nhóm ngành** (`scopes` HRM) thay vì cấp Lĩnh vực.

**Architecture:** 1 bảng phẳng — mỗi dòng `meeting_investment_demands` = 1 nhóm ngành được chọn, mang thêm id + snapshot tên của lĩnh vực cha. Endpoint danh mục trả **cây 2 tầng** trong 1 lần gọi. Khối khảo sát **bỏ hoàn toàn** phụ thuộc connection `mysql2`.

**Spec:** `.plans/meeting-tim-hieu-gioi-thieu-sp/design-phase2.md` — đọc kèm plan này.

**Nhánh:** `tpe` ở **cả 2 repo** (đã chứa sẵn cả feature khảo sát lẫn 2 danh mục mới). Kiểm bằng `git branch --show-current` trước khi sửa; sai nhánh thì dừng, không tự checkout.

## Global Constraints — Phase 6

Ngoài toàn bộ Global Constraints ở đầu file (vẫn áp), thêm:

- **Không tạo bảng mới, không tạo endpoint mới, không thêm quyền mới.** Chỉ đổi ruột những gì đã có.
- **`renameColumn` phải chạy ở `Schema::table()` RIÊNG**, không gộp chung block với `dropIndex` / `addColumn` — doctrine/dbal đọc schema tại thời điểm dựng block, gộp chung sẽ đọc nhầm trạng thái.
- **Không bọc `addColumn` / `renameColumn` trong `DB::transaction`** — MySQL implicit-commit → lỗi "no active transaction" (đã vấp ở migration `2026_08_22_000002`).
- **Không đặt FK cứng** cho `scope_id` / `internal_business_scope_id` — giữ kiểu snapshot, xoá danh mục không được làm hỏng biên bản cũ.
- **BE không tin payload FE** cho `internal_business_scope_id`: luôn tra lại từ `scopes.internal_business_scope_id` và ghi đè.
- **Giữ nguyên câu chữ 3 câu hỏi và cách đánh số 1–2–3** ở cả màn hình, bản in và Excel.
- `.tbl-bordered` / `.sec-title` / `.header-row` đang **chép** giữa `MeetingInvestmentSurvey.vue` và `MeetingReport.vue` — sửa bên nào phải soát bên kia.
- **Commit**: giữ nguyên quy ước Phase 1 — commit **local** mỗi task, **TUYỆT ĐỐI KHÔNG `git push`**.
- DB local: `hrm_tpe` (`hrm-api/.env`). Lệnh PHP dùng `/opt/homebrew/opt/php@7.4/bin/php`.

## File Structure — Phase 6

### `hrm-api`

| File | Trách nhiệm |
|------|-------------|
| `Modules/Assign/Database/Migrations/2026_08_23_000001_switch_meeting_investment_demands_to_internal_scopes.php` | **Mới** — xoá data cũ, đổi tên 2 cột, thêm 2 cột nhóm ngành, dựng lại index |
| `Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php` | Sửa — `$fillable` + docblock |
| `Modules/Assign/Entities/TpScope.php` | **XOÁ** — không còn chỗ dùng |
| `Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` | Sửa — `investmentScopes()` trả cây 2 tầng + helper `normalizeIdList()` |
| `Modules/Assign/Services/MeetingService.php` | Sửa — `syncInvestmentDemands()` tra tên từ 2 bảng HRM |
| `Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php` | Sửa — rule `exists` bỏ tiền tố `mysql2.` |
| `Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php` | Sửa — rule + closure `after()` bắt buộc nhóm ngành |
| `resources/views/exports/meeting_record.blade.php` | Sửa — bảng bản in 5 cột, `rowspan` cột Lĩnh vực |

### `hrm-client`

| File | Trách nhiệm |
|------|-------------|
| `store/optionsSelect.js` | Sửa — `fetchInvestmentScopes` nhận `includeGroupIds`, giữ `industry_groups` |
| `pages/assign/meeting/components/MeetingInvestmentSurvey.vue` | Sửa — bảng 5 cột phẳng, tích ở cấp nhóm ngành |
| `pages/assign/meeting/components/MeetingReport.vue` | Sửa — bảng trong file Excel biên bản 5 cột |

### `e2e`

| File | Trách nhiệm |
|------|-------------|
| `tests/assign/meeting-investment-survey.spec.ts` | Sửa — thay ca "đủ 13 lĩnh vực", thêm ca nhóm ngành |

---

### Task 6.1: Migration đổi schema + Entity

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_08_23_000001_switch_meeting_investment_demands_to_internal_scopes.php`
- Modify: `hrm-api/Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php`

**Interfaces:**
- Produces: bảng `meeting_investment_demands` với các cột `id, meeting_id, internal_business_scope_id, internal_business_scope_name, scope_id, scope_name, expected_amount, expected_start_date, position, created_by, updated_by, created_at, updated_at`; `unique(meeting_id, scope_id)`; index trên cả 2 cột id.
- Produces: `MeetingInvestmentDemand::$fillable` chứa `internal_business_scope_id`, `internal_business_scope_name`.

- [ ] **Bước 1: Viết migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

/**
 * Khao sat nhu cau KH doi nguon danh muc:
 * - Linh vuc: bang `scopes` ben ERP (mysql2)  ->  `internal_business_scopes` (HRM)
 * - Chi tiet muc dau tu / thoi gian: tu cap Linh vuc  ->  cap Nhom nganh (`scopes` HRM)
 *
 * Du lieu cu bi XOA SACH: `scope_id` cu tro bang cua ERP, khong map sang danh muc noi bo duoc.
 * Feature chua len production nen chap nhan mat du lieu thu nghiem.
 */
class SwitchMeetingInvestmentDemandsToInternalScopes extends Migration
{
    public function up()
    {
        DB::table('meeting_investment_demands')->delete();

        // Phai go index truoc khi doi ten cot (index dang tro vao `scope_id` cu)
        Schema::table('meeting_investment_demands', function (Blueprint $table) {
            $table->dropUnique('meeting_investment_demands_meeting_id_scope_id_unique');
            $table->dropIndex('meeting_investment_demands_scope_id_index');
        });

        // renameColumn PHAI dung o block rieng: doctrine/dbal doc schema luc dung block,
        // gop chung voi dropIndex/addColumn se doc nham trang thai bang
        Schema::table('meeting_investment_demands', function (Blueprint $table) {
            $table->renameColumn('scope_id', 'internal_business_scope_id');
            $table->renameColumn('scope_name', 'internal_business_scope_name');
        });

        Schema::table('meeting_investment_demands', function (Blueprint $table) {
            $table->unsignedBigInteger('scope_id')->after('internal_business_scope_name')
                ->comment('Nhom nganh - bang scopes HRM. KHONG dat FK: xoa danh muc khong duoc lam hong bien ban cu');
            $table->string('scope_name', 255)->after('scope_id')
                ->comment('Snapshot ten nhom nganh tai thoi diem luu');
        });

        Schema::table('meeting_investment_demands', function (Blueprint $table) {
            $table->unique(['meeting_id', 'scope_id']);
            $table->index('internal_business_scope_id');
            $table->index('scope_id');
        });
    }

    public function down()
    {
        DB::table('meeting_investment_demands')->delete();

        Schema::table('meeting_investment_demands', function (Blueprint $table) {
            $table->dropUnique('meeting_investment_demands_meeting_id_scope_id_unique');
            $table->dropIndex('meeting_investment_demands_internal_business_scope_id_index');
            $table->dropIndex('meeting_investment_demands_scope_id_index');
            $table->dropColumn(['scope_id', 'scope_name']);
        });

        Schema::table('meeting_investment_demands', function (Blueprint $table) {
            $table->renameColumn('internal_business_scope_id', 'scope_id');
            $table->renameColumn('internal_business_scope_name', 'scope_name');
        });

        Schema::table('meeting_investment_demands', function (Blueprint $table) {
            $table->unique(['meeting_id', 'scope_id']);
            $table->index('scope_id');
        });
    }
}
```

- [ ] **Bước 2: Lint file PHP**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Database/Migrations/2026_08_23_000001_switch_meeting_investment_demands_to_internal_scopes.php
```

Kỳ vọng: `No syntax errors detected`.

- [ ] **Bước 3: Chạy migrate**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan migrate
```

Kỳ vọng: 1 dòng `Migrated: ...SwitchMeetingInvestmentDemandsToInternalScopes`, không lỗi.

- [ ] **Bước 4: Verify schema thật**

```bash
mysql -h127.0.0.1 -uroot -p'Dnsmedia@2025!' hrm_tpe -e "SHOW CREATE TABLE meeting_investment_demands\G"
```

Kỳ vọng:
- Có đủ 4 cột `internal_business_scope_id` (bigint unsigned), `internal_business_scope_name` (varchar 255), `scope_id` (bigint unsigned), `scope_name` (varchar 255)
- `UNIQUE KEY meeting_investment_demands_meeting_id_scope_id_unique (meeting_id, scope_id)`
- 2 index thường trên `internal_business_scope_id` và `scope_id`
- FK `meeting_id` → `meetings(id)` `ON DELETE CASCADE` vẫn còn
- **Không** còn cột tên `scope_id` mang nghĩa cũ (kiểm bằng comment cột: `Nhom nganh - bang scopes HRM`)

- [ ] **Bước 5: Verify rollback sạch rồi migrate lại**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan migrate:rollback --step=1 && /opt/homebrew/opt/php@7.4/bin/php artisan migrate
```

Kỳ vọng: rollback không lỗi (đây là bước bắt lỗi thứ tự `dropUnique` / `dropIndex` / `renameColumn`), migrate lại thành công. Nếu rollback báo `Unknown key`, tên index đang khác mặc định — đọc lại `SHOW CREATE TABLE` lấy tên thật rồi sửa migration.

- [ ] **Bước 6: Sửa Entity**

`hrm-api/Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php` — đổi docblock và `$fillable`:

```php
/**
 * 1 dong "Nhom nganh quan tam" cua khoi Khao sat nhu cau khach hang (tab Bien ban).
 *
 * 1 dong = 1 NHOM NGANH (bang `scopes` HRM) + snapshot linh vuc cha
 * (`internal_business_scopes`). Muc dau tu du kien va thoi gian du kien bat dau
 * nhap o CAP NHOM NGANH.
 *
 * Ca 2 cot id deu KHONG co FK: ten duoc snapshot lai nen xoa danh muc khong
 * lam sai bien ban cu.
 */
class MeetingInvestmentDemand extends BaseModel
{
    protected $table = 'meeting_investment_demands';

    protected $fillable = [
        'meeting_id',
        'internal_business_scope_id',
        'internal_business_scope_name',
        'scope_id',
        'scope_name',
        'expected_amount',
        'expected_start_date',
        'position',
        'created_by',
        'updated_by',
    ];
```

Giữ nguyên `$casts` và quan hệ `meeting()`.

- [ ] **Bước 7: Lint + verify Entity khớp schema**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php
/opt/homebrew/opt/php@7.4/bin/php artisan tinker <<'PHP'
$m = new Modules\Assign\Entities\Meeting\MeetingInvestmentDemand();
$cols = Schema::getColumnListing('meeting_investment_demands');
$missing = array_diff($m->getFillable(), $cols);
echo empty($missing) ? "OK: fillable khop schema\n" : "SAI: thieu cot ".implode(',', $missing)."\n";
PHP
```

Kỳ vọng: `No syntax errors detected` và `OK: fillable khop schema`.

- [ ] **Bước 8: Commit**

```bash
cd HRM/hrm-api && git add Modules/Assign/Database/Migrations/2026_08_23_000001_switch_meeting_investment_demands_to_internal_scopes.php Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php && git commit -m "feat(meeting): khao sat nhu cau luu theo nhom nganh + linh vuc noi bo"
```

---

### Task 6.2: Endpoint danh mục trả cây 2 tầng + xoá `TpScope`

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php:528-563`
- Delete: `hrm-api/Modules/Assign/Entities/TpScope.php`

**Interfaces:**
- Consumes: Entity `Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope` (hằng `STATUS_ACTIVE`, quan hệ `scopes()`), `Modules\Assign\Entities\Scope\Scope` (hằng `STATUS_ACTIVE`, cột `internal_business_scope_id`) — **đã có sẵn trên nhánh**, không phải tạo.
- Produces: `GET assign/meeting/investment-scopes?include_ids[]=&include_group_ids[]=` trả mảng `{ id:int, name:string, is_locked:bool, industry_groups: [{ id:int, name:string, is_locked:bool }] }`.

- [ ] **Bước 1: Đổi import ở đầu `MeetingController.php`**

Bỏ dòng:

```php
use Modules\Assign\Entities\TpScope;
```

Thêm:

```php
use Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope;
use Modules\Assign\Entities\Scope\Scope;
```

- [ ] **Bước 2: Thay toàn bộ method `investmentScopes()`**

```php
    /**
     * Danh muc cho khoi Khao sat nhu cau khach hang (tab Bien ban) — cay 2 tang:
     * Linh vuc kinh doanh noi bo (`internal_business_scopes`) -> Nhom nganh (`scopes`).
     * Ca 2 bang deu o DB HRM (connection mac dinh) — khong con doc ERP qua mysql2.
     *
     * include_ids       : id LINH VUC meeting dang dung (ke ca da khoa)
     * include_group_ids : id NHOM NGANH meeting dang dung (ke ca da khoa)
     * -> khong tra ve thi man Sua se mat gia tri da chon.
     */
    public function investmentScopes(Request $request)
    {
        try {
            $includeIds = $this->normalizeIdList($request->input('include_ids', []));
            $includeGroupIds = $this->normalizeIdList($request->input('include_group_ids', []));

            $scopes = InternalBusinessScope::query()
                ->where(function ($q) use ($includeIds) {
                    $q->where('status', InternalBusinessScope::STATUS_ACTIVE);
                    if (!empty($includeIds)) {
                        $q->orWhereIn('id', $includeIds);
                    }
                })
                ->with(['scopes' => function ($q) use ($includeGroupIds) {
                    $q->where(function ($sub) use ($includeGroupIds) {
                        $sub->where('scopes.status', Scope::STATUS_ACTIVE);
                        if (!empty($includeGroupIds)) {
                            $sub->orWhereIn('scopes.id', $includeGroupIds);
                        }
                    })->orderBy('scopes.id');
                }])
                ->orderBy('id')
                ->get(['id', 'name', 'status']);

            $data = $scopes->map(function ($s) {
                return [
                    'id' => (int) $s->id,
                    'name' => $s->name,
                    'is_locked' => (int) $s->status !== InternalBusinessScope::STATUS_ACTIVE,
                    'industry_groups' => $s->scopes->map(function ($g) {
                        return [
                            'id' => (int) $g->id,
                            'name' => $g->name,
                            'is_locked' => (int) $g->status !== Scope::STATUS_ACTIVE,
                        ];
                    })->values(),
                ];
            })
            // Linh vuc chua co nhom nganh con nao -> bo han khoi ket qua:
            // muc dau tu / thoi gian nhap o cap nhom nganh nen dong khong co con la dong chet
            ->filter(function ($item) {
                return $item['industry_groups']->isNotEmpty();
            })
            ->values();

            return $this->responseJson('success', Response::HTTP_OK, $data);
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseJson(
                'Không tải được danh mục lĩnh vực. Vui lòng thử lại.',
                Response::HTTP_BAD_REQUEST
            );
        }
    }

    /** Chuan hoa tham so id: nhan mang hoac chuoi "1,2,3" -> mang int duong */
    private function normalizeIdList($value)
    {
        if (!is_array($value)) {
            $value = explode(',', (string) $value);
        }

        return array_values(array_filter(array_map('intval', $value)));
    }
```

Lưu ý: bỏ hẳn câu lỗi `503 "Không kết nối được danh mục lĩnh vực bên ERP"` — không còn gọi ERP.

- [ ] **Bước 3: Kiểm chỗ nào còn dùng `TpScope`**

```bash
cd HRM/hrm-api && grep -rn "TpScope" --exclude-dir=vendor --exclude-dir=node_modules .
```

Kỳ vọng: chỉ còn **2 dòng** ở `Modules/Assign/Services/MeetingService.php` (import + `TpScope::whereIn`) và file Entity chính nó.
**CHƯA xoá file `TpScope.php` ở task này** — `MeetingService` vẫn gọi tới, xoá bây giờ sẽ fatal ngay khi lưu meeting. Task 6.3 sửa service xong mới xoá.

- [ ] **Bước 4: Lint**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Http/Controllers/Api/V1/MeetingController.php
```

Kỳ vọng: `No syntax errors detected`.

- [ ] **Bước 5: Verify truy vấn trả đúng cây (không cần HTTP)**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan tinker <<'PHP'
use Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope;
use Modules\Assign\Entities\Scope\Scope;

$tree = InternalBusinessScope::where('status', InternalBusinessScope::STATUS_ACTIVE)
    ->with(['scopes' => function ($q) { $q->where('scopes.status', Scope::STATUS_ACTIVE); }])
    ->orderBy('id')->get(['id','name','status']);

foreach ($tree as $s) {
    echo $s->id . ' - ' . $s->name . ' -> ' . $s->scopes->count() . " nhom nganh\n";
}
echo "Tong linh vuc co con: " . $tree->filter(function($s){ return $s->scopes->isNotEmpty(); })->count() . "\n";
echo "Tong nhom nganh active: " . Scope::where('status', Scope::STATUS_ACTIVE)->count() . "\n";
PHP
```

Kỳ vọng: in ra danh sách lĩnh vực kèm số nhóm ngành con; tổng nhóm ngành active > 0 (migration `2026_08_22_000002` đã backfill 22 bản ghi cũ về `LVKDNB.KHAC`). **Ghi lại 2 con số này** — Task 6.8 dùng làm kỳ vọng cho E2E.

- [ ] **Bước 6: Verify endpoint qua HTTP**

```bash
cd HRM/hrm-api
# Sinh JWT cho tai khoan dev (repo dung tymon/jwt-auth)
TOKEN=$(/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute="
\$u = Modules\\Human\\Entities\\Employee::whereHas('info', function (\$q) { \$q->where('email', 'namdangit@gmail.com'); })->first();
echo JWTAuth::fromUser(\$u);
" | tail -1)
/opt/homebrew/opt/php@7.4/bin/php artisan serve --port=8000 &
sleep 3
curl -s "http://127.0.0.1:8000/api/v1/assign/meeting/investment-scopes" -H "Authorization: Bearer $TOKEN" | head -c 600
```

Nếu `artisan tinker --execute` không chạy trên bản Laravel này, lấy token bằng cách đăng nhập FE rồi copy từ DevTools → Network → header `Authorization`.

Kỳ vọng: JSON có `industry_groups` lồng bên trong mỗi phần tử, không phần tử nào có `industry_groups: []`.

- [ ] **Bước 7: Commit**

```bash
cd HRM/hrm-api && git add -A Modules/Assign && git commit -m "feat(meeting): endpoint danh muc khao sat tra cay linh vuc noi bo -> nhom nganh"
```

---

### Task 6.3: Lưu dữ liệu + validate

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/MeetingService.php:118-163`
- Modify: `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php:73-78, 205-212`
- Modify: `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php:148-156, 240-265, 340-345`

**Interfaces:**
- Consumes: Entity + schema từ Task 6.1; `Scope` / `InternalBusinessScope` từ Task 6.2.
- Produces: payload `investment_demands[]` nhận các key `scope_id`, `scope_name`, `internal_business_scope_id`, `internal_business_scope_name`, `expected_amount`, `expected_start_date`. **BE ghi đè `internal_business_scope_id` bằng giá trị tra từ `scopes`.**

- [ ] **Bước 1: Đổi import ở `MeetingService.php`**

Bỏ `use Modules\Assign\Entities\TpScope;`, thêm:

```php
use Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope;
use Modules\Assign\Entities\Scope\Scope;
```

- [ ] **Bước 2: Thay phần tra tên + vòng lặp trong `syncInvestmentDemands()`**

Giữ nguyên 2 khối đầu (`has_investment_demand !== 1` → xoá sạch; `!is_array($demands)` → mảng rỗng; `$entity->investment_demands()->delete()`). Thay từ dòng `// Snapshot ten linh vuc...` trở xuống:

```php
        // Snapshot ten: nap 1 lan cho ca mang, KHONG query trong vong lap
        $scopeIds = array_values(array_filter(array_column($demands, 'scope_id')));
        $scopeById = empty($scopeIds)
            ? collect()
            : Scope::whereIn('id', $scopeIds)->get(['id', 'name', 'internal_business_scope_id'])->keyBy('id');

        $internalIds = $scopeById->pluck('internal_business_scope_id')->filter()->unique()->values()->all();
        $internalNameById = empty($internalIds)
            ? collect()
            : InternalBusinessScope::whereIn('id', $internalIds)->pluck('name', 'id');

        foreach (array_values($demands) as $i => $item) {
            $scopeId = (int) ($item['scope_id'] ?? 0);
            if (!$scopeId) {
                continue;
            }

            $scope = $scopeById->get($scopeId);

            // KHONG tin payload FE: linh vuc cha luon tra lai tu DB.
            // Nhom nganh mo coi (internal_business_scope_id NULL) -> ghi NULL, khong chet.
            $internalId = $scope ? $scope->internal_business_scope_id : null;
            $internalName = $internalId && isset($internalNameById[$internalId])
                ? $internalNameById[$internalId]
                : ($item['internal_business_scope_name'] ?? '');

            $entity->investment_demands()->create([
                'internal_business_scope_id' => $internalId,
                'internal_business_scope_name' => $internalName,
                'scope_id' => $scopeId,
                // uu tien ten hien tai trong DB; danh muc bi xoa thi lay ten FE gui len
                'scope_name' => $scope ? $scope->name : ($item['scope_name'] ?? ''),
                'expected_amount' => $item['expected_amount'] ?? null,
                'expected_start_date' => $item['expected_start_date'] ?? null,
                'position' => $i,
            ]);
        }
```

- [ ] **Bước 3: Sửa rule ở `MeetingCreateApiRequest.php`**

Trong khối `if ($needSurvey) { ... }` (dòng ~73):

```php
            $rules['investment_demands']                              = 'nullable|array';
            $rules['investment_demands.*.scope_id']                   = 'required|integer|min:1|distinct|exists:scopes,id';
            $rules['investment_demands.*.internal_business_scope_id'] = 'nullable|integer';
            $rules['investment_demands.*.expected_amount']            = 'nullable|numeric|min:0|max:999999999999999999';
            $rules['investment_demands.*.expected_start_date']        = 'nullable|date|after_or_equal:today';
```

Trong `messages()` đổi 2 dòng:

```php
            'investment_demands.*.scope_id.exists' => 'Nhóm ngành không tồn tại hoặc đã bị xoá.',
            'investment_demands.*.scope_id.distinct' => 'Mỗi nhóm ngành chỉ được chọn một lần.',
```

- [ ] **Bước 4: Sửa rule + messages ở `MeetingUpdateApiRequest.php`**

Áp **y hệt** 5 dòng rule và 2 dòng message của Bước 3 (2 file đang lặp rule, giữ nguyên cách lặp đó — không gom lại thành trait ở task này).

- [ ] **Bước 5: Sửa closure `after()` ở `MeetingUpdateApiRequest.php`**

Thay khối kiểm `empty($demands)`:

```php
            $demands = $this->input('investment_demands', []);
            if (empty($demands)) {
                // Ngoai le: ca danh muc chua co nhom nganh nao Hoat dong -> bang rong,
                // bat buoc se lam ket man Hoan thanh. Bo qua rang buoc trong truong hop nay.
                $hasAnyScope = \Modules\Assign\Entities\Scope\Scope::where('status', \Modules\Assign\Entities\Scope\Scope::STATUS_ACTIVE)->exists();
                if ($hasAnyScope) {
                    $v->errors()->add('investment_demands', 'Vui lòng chọn ít nhất một nhóm ngành.');
                }
                return;
            }
```

Giữ nguyên vòng lặp kiểm `expected_amount` / `expected_start_date` bên dưới (câu chữ lỗi không đổi).

- [ ] **Bước 6: Xoá `TpScope` (giờ mới an toàn) + lint**

```bash
cd HRM/hrm-api && git rm Modules/Assign/Entities/TpScope.php
for f in Modules/Assign/Services/MeetingService.php Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php; do /opt/homebrew/opt/php@7.4/bin/php -l "$f"; done
grep -rn "mysql2.scopes\|TpScope" --exclude-dir=vendor --exclude-dir=node_modules .
```

Kỳ vọng: 3 dòng `No syntax errors detected`, và `grep` **không in ra dòng nào** (nếu còn = đã sót chỗ dùng, sửa nốt rồi chạy lại).

- [ ] **Bước 7: Verify lưu thật bằng tinker**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan tinker <<'PHP'
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\Scope\Scope;
use Modules\Assign\Services\MeetingService;

$meeting = Meeting::whereHas('meeting_type', function ($q) { $q->where('code', 'HOP_TIM_HIEU_GIOI_THIEU_SP'); })->first();
if (!$meeting) { echo "BO QUA: chua co meeting loai he thong, chay SystemMeetingTypesSeeder truoc\n"; return; }

$scope = Scope::where('status', Scope::STATUS_ACTIVE)->first();
$meeting->has_investment_demand = 1;
$meeting->save();

app(MeetingService::class)->syncInvestmentDemands([
    ['scope_id' => $scope->id, 'scope_name' => 'TEN SAI FE GUI', 'internal_business_scope_id' => 999999, 'expected_amount' => 1000, 'expected_start_date' => '2026-12-01'],
], $meeting);

$row = $meeting->investment_demands()->first();
echo "scope_name = {$row->scope_name} (ky vong: {$scope->name})\n";
echo "internal_business_scope_id = {$row->internal_business_scope_id} (ky vong: {$scope->internal_business_scope_id}, KHONG phai 999999)\n";
echo "internal_business_scope_name = {$row->internal_business_scope_name}\n";
PHP
```

Kỳ vọng: `scope_name` là tên thật trong DB (không phải "TEN SAI FE GUI"), `internal_business_scope_id` là id thật của lĩnh vực cha (**không** phải 999999) → chứng minh BE ghi đè payload.

- [ ] **Bước 8: Dọn dữ liệu thử**

```bash
mysql -h127.0.0.1 -uroot -p'Dnsmedia@2025!' hrm_tpe -e "DELETE FROM meeting_investment_demands;"
```

- [ ] **Bước 9: Commit**

```bash
cd HRM/hrm-api && git add -A Modules/Assign/Services/MeetingService.php Modules/Assign/Http/Requests/Meeting Modules/Assign/Entities/TpScope.php && git commit -m "feat(meeting): luu + validate khao sat theo nhom nganh, BE tu tra linh vuc cha"
```

---

### Task 6.4: Vuex `fetchInvestmentScopes` giữ cây 2 tầng

**Files:**
- Modify: `hrm-client/store/optionsSelect.js:445-478`

**Interfaces:**
- Consumes: endpoint từ Task 6.2.
- Produces: `dispatch('optionsSelect/fetchInvestmentScopes', { includeIds, includeGroupIds })` → trả mảng `{ id, name, is_locked, industry_groups: [{ id, name, is_locked }] }` (**giá trị return**, không phải getter).

- [ ] **Bước 1: Kiểm line ending trước khi sửa**

```bash
cd HRM/hrm-client && file store/optionsSelect.js
```

Nếu in `CRLF` thì dòng thêm mới phải dùng `\r\n`.

- [ ] **Bước 2: Thay thân action**

```js
    async fetchInvestmentScopes({ commit, dispatch, state }, { includeIds = [], includeGroupIds = [] } = {}) {
        const sanitize = (list) =>
            (list || []).filter((id) => id !== null && id !== undefined && id !== '').map((id) => Number(id))

        const sanitizedIds = sanitize(includeIds)
        const sanitizedGroupIds = sanitize(includeGroupIds)

        // Cache chi dung duoc khi CA HAI cap deu da co trong cache — thieu 1 nhom nganh
        // da khoa la tai dung lai loi "muc da khoa bien mat khoi dropdown cho toi khi F5"
        const cachedIds = state.investmentScopes.map((s) => s.id)
        const cachedGroupIds = state.investmentScopes.reduce(
            (acc, s) => acc.concat((s.industry_groups || []).map((g) => g.id)),
            [],
        )
        const missing = sanitizedIds.filter((id) => !cachedIds.includes(id))
        const missingGroups = sanitizedGroupIds.filter((id) => !cachedGroupIds.includes(id))
        if (state.investmentScopes.length > 0 && missing.length === 0 && missingGroups.length === 0) {
            return state.investmentScopes
        }

        try {
            const query = [
                ...sanitizedIds.map((id) => `include_ids[]=${encodeURIComponent(id)}`),
                ...sanitizedGroupIds.map((id) => `include_group_ids[]=${encodeURIComponent(id)}`),
            ].join('&')
            const url = query
                ? `assign/meeting/investment-scopes?${query}`
                : 'assign/meeting/investment-scopes'
            const { data } = await dispatch('apiGetMethod', url, { root: true })
            const fetched = (data || []).map((s) => ({
                id: Number(s.id),
                name: s.name,
                is_locked: !!s.is_locked,
                industry_groups: (s.industry_groups || []).map((g) => ({
                    id: Number(g.id),
                    name: g.name,
                    is_locked: !!g.is_locked,
                })),
            }))

            // Cache dung chung toan app chi giu muc con hoat dong — CA HAI cap
            commit(
                'SET_INVESTMENT_SCOPES',
                fetched
                    .filter((scope) => !scope.is_locked)
                    .map((scope) => ({
                        ...scope,
                        industry_groups: scope.industry_groups.filter((g) => !g.is_locked),
                    })),
            )

            return fetched
        } catch (error) {
            console.error('Error fetching investment scopes:', error)
            return state.investmentScopes
        }
    },
```

Giữ nguyên khối comment cảnh báo "dùng giá trị return, đừng đọc getter" ở ngay trên action.

- [ ] **Bước 3: Verify không phá line ending**

```bash
cd HRM/hrm-client && git diff --stat store/optionsSelect.js
```

Kỳ vọng: chỉ vài chục dòng thay đổi. Nếu báo cả file đổi → đã phá line ending, `git checkout -- store/optionsSelect.js` rồi sửa lại bằng tay.

- [ ] **Bước 4: Commit**

```bash
cd HRM/hrm-client && git add store/optionsSelect.js && git commit -m "feat(meeting): store danh muc khao sat giu cay linh vuc -> nhom nganh"
```

---

### Task 6.5: Bảng khảo sát 5 cột ở `MeetingInvestmentSurvey.vue`

**Files:**
- Modify: `hrm-client/pages/assign/meeting/components/MeetingInvestmentSurvey.vue`

**Interfaces:**
- Consumes: action từ Task 6.4.
- Produces: `this.$refs.investmentSurvey.buildPayload()` → `{ has_investment_demand, has_maintenance_demand, investment_demands: [{ scope_id, scope_name, internal_business_scope_id, internal_business_scope_name, expected_amount, expected_start_date }] }`; `loadScopes()` giữ nguyên tên (MeetingReport đang gọi).

- [ ] **Bước 1: Thay khối bảng của câu 2 trong `<template>`**

Thay từ `<div class="tbl-bordered">` tới thẻ đóng tương ứng:

```html
                <div class="tbl-bordered">
                    <div class="row header-row px-1" style="color: #6b7280">
                        <div class="col-3">Lĩnh vực</div>
                        <div class="col-1">Chọn</div>
                        <div class="col-3">Nhóm ngành</div>
                        <div class="col-3">Mức đầu tư dự kiến (VNĐ)</div>
                        <div class="col-2">Thời gian dự kiến bắt đầu</div>
                    </div>

                    <div
                        v-for="(row, i) in rows"
                        :key="'sc-' + row.scope_id"
                        class="row g-2 align-items-center mb-2"
                        :class="{ 'group-break': row.is_group_break }"
                        data-testid="scope-row"
                        :data-scope-id="row.scope_id"
                        :data-internal-scope-id="row.internal_business_scope_id"
                    >
                        <div class="col-3">
                            <span v-if="row.is_group_start" style="color: #374151" data-testid="scope-parent">{{
                                row.internal_business_scope_name
                            }}</span>
                        </div>
                        <div class="col-1 text-center">
                            <V2BaseCheckbox
                                :modelValue="row.checked"
                                :disabled="isShow || ((row.missing || row.is_locked) && !row.checked)"
                                data-testid="scope-check"
                                @change="onToggleRow(i, $event)"
                            />
                        </div>
                        <div class="col-3">
                            <span style="color: #374151">{{ row.scope_name }}</span>
                            <V2BaseError v-if="errorFor(i, 'scope_id')" :message="errorFor(i, 'scope_id')" />
                        </div>
                        <div class="col-3">
                            <V2BaseCurrencyInput
                                v-model="row.expected_amount"
                                :precision="0"
                                :disabled="isShow || !row.checked"
                                placeholder="Nhập mức đầu tư dự kiến"
                                data-testid="scope-amount"
                            />
                            <V2BaseError v-if="errorFor(i, 'expected_amount')" :message="errorFor(i, 'expected_amount')" />
                        </div>
                        <div class="col-2" data-testid="scope-date">
                            <V2BaseDatePicker
                                v-model="row.expected_start_date"
                                type="date"
                                value-type="YYYY-MM-DD"
                                format="DD/MM/YYYY"
                                size="sm"
                                :disabled="isShow || !row.checked"
                                :disabled-date="disablePastDates"
                            />
                            <V2BaseError v-if="errorFor(i, 'expected_start_date')" :message="errorFor(i, 'expected_start_date')" />
                        </div>
                    </div>
                </div>
```

**Không đổi** câu chữ tiêu đề câu 2, không đổi 2 khối "Đang tải…" / "Không tải được…".

- [ ] **Bước 2: Thay `loadScopes()`**

```js
        /** Nap danh muc (lazy) — MeetingReport goi khi mo tab Bien ban */
        async loadScopes() {
            if (this.loadingScopes) return
            this.loadingScopes = true
            this.scopeLoadFailed = false
            try {
                const saved = this.form.investment_demands || []
                const includeIds = saved
                    .map((d) => Number(d.internal_business_scope_id))
                    .filter((id) => !!id)
                const includeGroupIds = saved.map((d) => Number(d.scope_id)).filter((id) => !!id)
                // Dung GIA TRI RETURN, khong doc getter — xem comment o data.scopeOptions
                const scopes = await this.$store.dispatch('optionsSelect/fetchInvestmentScopes', {
                    includeIds,
                    includeGroupIds,
                })
                this.scopeOptions = scopes || []
                this.scopeLoadFailed = this.scopeOptions.length === 0
                this.buildRows()
            } finally {
                this.loadingScopes = false
            }
        },
```

- [ ] **Bước 3: Thay `buildRows()`**

```js
        /**
         * Phang hoa cay linh vuc -> nhom nganh thanh danh sach dong, moi dong = 1 nhom nganh.
         * Nhom nganh da chon ma danh muc xoa mat -> push dong ao tu snapshot (missing = true),
         * hien dung ten goc, cho bo tich nhung khong cho tich lai.
         */
        buildRows() {
            const saved = this.form.investment_demands || []
            const savedByScopeId = {}
            saved.forEach((d) => {
                savedByScopeId[Number(d.scope_id)] = d
            })

            const rows = []
            ;(this.scopeOptions || []).forEach((s) => {
                ;(s.industry_groups || []).forEach((g, gi) => {
                    const d = savedByScopeId[Number(g.id)]
                    rows.push({
                        internal_business_scope_id: s.id,
                        internal_business_scope_name: s.name,
                        scope_id: g.id,
                        scope_name: g.name,
                        missing: false,
                        is_locked: !!g.is_locked,
                        is_group_start: gi === 0,
                        checked: !!d,
                        expected_amount: d && d.expected_amount != null ? Number(d.expected_amount) : null,
                        expected_start_date: d ? d.expected_start_date || null : null,
                    })
                })
            })

            const knownIds = rows.map((r) => r.scope_id)
            saved.forEach((d) => {
                const id = Number(d.scope_id)
                if (knownIds.includes(id)) return
                rows.push({
                    internal_business_scope_id: d.internal_business_scope_id
                        ? Number(d.internal_business_scope_id)
                        : null,
                    internal_business_scope_name: d.internal_business_scope_name || '(Lĩnh vực đã bị xoá)',
                    scope_id: id,
                    scope_name: d.scope_name || '(Nhóm ngành đã bị xoá)',
                    missing: true,
                    is_locked: false,
                    is_group_start: true,
                    checked: true,
                    expected_amount: d.expected_amount != null ? Number(d.expected_amount) : null,
                    expected_start_date: d.expected_start_date || null,
                })
            })

            // Dong dau bang khong can duong ke ngan nhom
            rows.forEach((r, i) => {
                r.is_group_break = r.is_group_start && i > 0
            })

            this.rows = rows
        },
```

- [ ] **Bước 4: Thay `buildPayload()`**

```js
        /** MeetingForm / MeetingReport goi khi build payload luu meeting */
        buildPayload() {
            return {
                has_investment_demand: this.answer1,
                has_maintenance_demand: this.answer3,
                investment_demands: this.rows
                    .filter((r) => r.checked)
                    .map((r) => ({
                        scope_id: r.scope_id,
                        scope_name: r.scope_name,
                        // BE se ghi de internal_business_scope_id bang gia tri tra tu DB;
                        // van gui len de bang hien thi lai dung ngay khi chua reload
                        internal_business_scope_id: r.internal_business_scope_id,
                        internal_business_scope_name: r.internal_business_scope_name,
                        expected_amount: r.expected_amount != null ? Number(r.expected_amount) : null,
                        expected_start_date: r.expected_start_date || null,
                    })),
            }
        },
```

- [ ] **Bước 5: Đổi câu chữ hộp thoại xác nhận ở `onChangeAnswer1()`**

```js
                const ok = await this.$confirm({
                    title: 'Xoá dữ liệu nhóm ngành đã chọn?',
                    message:
                        'Chuyển sang "Không" sẽ xoá toàn bộ nhóm ngành đã chọn cùng mức đầu tư và thời gian đã nhập. Bạn có chắc chắn?',
                    textAccept: 'Xoá',
                    danger: true,
                })
```

Giữ nguyên phần còn lại của method (`$nextTick` trả về 1, vòng `onToggleRow(i, false)`).

- [ ] **Bước 6: Thêm style đường ngăn nhóm**

Thêm vào cuối `<style scoped>`:

```css
/* Thay cho rowspan: bang dung div.row/col nen khong gop o duoc.
   Dong dau cua moi linh vuc duoc ke dam hon de nhin ra ranh gioi nhom. */
.tbl-bordered .row.group-break {
    border-top: 2px solid #d1d5db;
}
```

- [ ] **Bước 7: Không đổi các phần còn lại**

`surveyState`, watcher `form.id`, watcher `surveyState`, `hydrateFromForm`, `onToggleRow`, `disablePastDates`, `errorFor`, `payloadIndexOf` **giữ nguyên** — chúng đã đúng với cấu trúc `rows` mới.

- [ ] **Bước 8: Verify line ending + build FE**

```bash
cd HRM/hrm-client && git diff --stat pages/assign/meeting/components/MeetingInvestmentSurvey.vue
NODE_OPTIONS=--max-old-space-size=8192 npm run dev
```

(Node 12 — xem `.plans/STATUS.md` mục "Chạy môi trường dev HRM".)

Kỳ vọng: `git diff --stat` chỉ vài chục dòng; dev server build không lỗi.

- [ ] **Bước 9: Verify bằng mắt**

Mở meeting loại "Họp tìm hiểu & Giới thiệu sản phẩm" → tab Biên bản → câu 1 chọn "Có".

Kỳ vọng:
- Bảng 5 cột đúng thứ tự Lĩnh vực · Chọn · Nhóm ngành · Mức đầu tư · Thời gian, **không cột nào lẻ hàng**
- Tên lĩnh vực chỉ hiện ở dòng đầu mỗi nhóm, có đường kẻ đậm ngăn giữa 2 lĩnh vực
- Tích 1 dòng → 2 ô bên phải bật lên; bỏ tích → 2 ô trắng lại và bị khoá

- [ ] **Bước 10: Commit**

```bash
cd HRM/hrm-client && git add pages/assign/meeting/components/MeetingInvestmentSurvey.vue && git commit -m "feat(meeting): bang khao sat nhap theo nhom nganh, gom dong theo linh vuc"
```

---

### Task 6.6: Bản in biên bản 5 cột với `rowspan`

**Files:**
- Modify: `hrm-api/resources/views/exports/meeting_record.blade.php:199-221`

**Interfaces:**
- Consumes: `$meeting->investment_demands` (đã có `internal_business_scope_name`, `scope_name` từ Task 6.1 + 6.3).

- [ ] **Bước 1: Thay khối bảng "Lĩnh vực đầu tư"**

```blade
            @if($meeting->has_investment_demand && $meeting->investment_demands->count())
                <div style="margin-bottom: 8px; font-family: 'Times New Roman', serif; font-size: 13px;">{{$ivIndex}}.2 Lĩnh vực đầu tư:</div>
                <table style="width: 100%; border-collapse: collapse; font-family: 'Times New Roman', serif; font-size: 13px; margin-bottom: 8px;">
                    <thead>
                        <tr>
                            <th style="border: 1px solid #000; padding: 5px; width: 6%;">STT</th>
                            <th style="border: 1px solid #000; padding: 5px; width: 27%;">Lĩnh vực</th>
                            <th style="border: 1px solid #000; padding: 5px; width: 27%;">Nhóm ngành</th>
                            <th style="border: 1px solid #000; padding: 5px; width: 22%;">Mức đầu tư dự kiến (VNĐ)</th>
                            <th style="border: 1px solid #000; padding: 5px; width: 18%;">Thời gian dự kiến bắt đầu</th>
                        </tr>
                    </thead>
                    <tbody>
                    @php $stt = 0; @endphp
                    @foreach($meeting->investment_demands->groupBy('internal_business_scope_id') as $groupRows)
                        @foreach($groupRows as $d)
                            <tr>
                                <td style="border: 1px solid #000; padding: 5px; text-align: center;">{{ ++$stt }}</td>
                                @if($loop->first)
                                    <td style="border: 1px solid #000; padding: 5px; vertical-align: middle;" rowspan="{{ $loop->count }}">{{ $d->internal_business_scope_name }}</td>
                                @endif
                                <td style="border: 1px solid #000; padding: 5px;">{{ $d->scope_name }}</td>
                                <td style="border: 1px solid #000; padding: 5px; text-align: right;">{{ $d->expected_amount !== null ? number_format($d->expected_amount, 0, ',', ',') : '' }}</td>
                                <td style="border: 1px solid #000; padding: 5px; text-align: center;">{{ $d->expected_start_date ? $d->expected_start_date->format('d/m/Y') : '' }}</td>
                            </tr>
                        @endforeach
                    @endforeach
                    </tbody>
                </table>
            @endif
```

Lưu ý: `$loop` trong `@foreach` lồng trỏ vào vòng **trong** — đúng cái ta cần (`$loop->count` = số nhóm ngành của lĩnh vực đó). Giữ nguyên `number_format(..., ',', ',')` (dấu **phẩy** phân cách nghìn — quyết định #5 spec gốc) và `format('d/m/Y')`.

- [ ] **Bước 2: Dựng dữ liệu thử 2 lĩnh vực × nhiều nhóm ngành**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan tinker <<'PHP'
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\Scope\Scope;
use Modules\Assign\Services\MeetingService;

$meeting = Meeting::whereHas('meeting_type', function ($q) { $q->where('code', 'HOP_TIM_HIEU_GIOI_THIEU_SP'); })->first();
$meeting->has_investment_demand = 1; $meeting->has_maintenance_demand = 0; $meeting->save();

// Lay 3 nhom nganh nam o >= 2 linh vuc khac nhau de kiem rowspan
$scopes = Scope::where('status', Scope::STATUS_ACTIVE)
    ->whereNotNull('internal_business_scope_id')
    ->orderBy('internal_business_scope_id')->take(4)->get();

app(MeetingService::class)->syncInvestmentDemands(
    $scopes->map(function ($s, $i) {
        return ['scope_id' => $s->id, 'expected_amount' => 1000000 * ($i + 1), 'expected_start_date' => '2026-12-0'.($i+1)];
    })->all(),
    $meeting
);
echo "meeting id = {$meeting->id}, so dong = " . $meeting->investment_demands()->count() . "\n";
echo "so linh vuc khac nhau = " . $meeting->investment_demands()->distinct('internal_business_scope_id')->count('internal_business_scope_id') . "\n";
PHP
```

Kỳ vọng: in ra `so dong = 4` và `so linh vuc khac nhau >= 1`. Ghi lại `meeting id`.

- [ ] **Bước 3: Verify bản in**

Mở `/assign/meeting/<meeting id>` → nút In biên bản (hoặc gọi `GET api/v1/assign/meeting/<id>/print`).

Kỳ vọng:
- Bảng mục `1.2 Lĩnh vực đầu tư` có **5 cột**
- Ô Lĩnh vực gộp dọc đúng số dòng của nhóm (rowspan), không lệch cột, không dòng trống thừa
- STT chạy liên tục 1,2,3,4 theo dòng nhóm ngành
- Mức đầu tư phân cách bằng dấu **phẩy**

- [ ] **Bước 4: Dọn dữ liệu thử**

```bash
mysql -h127.0.0.1 -uroot -p'Dnsmedia@2025!' hrm_tpe -e "DELETE FROM meeting_investment_demands;"
```

- [ ] **Bước 5: Commit**

```bash
cd HRM/hrm-api && git add resources/views/exports/meeting_record.blade.php && git commit -m "feat(meeting): ban in bien ban them cot Nhom nganh, gop o Linh vuc"
```

---

### Task 6.7: File Excel biên bản 5 cột

**Files:**
- Modify: `hrm-client/pages/assign/meeting/components/MeetingReport.vue:768-805`

**Interfaces:**
- Consumes: `buildPayload()` từ Task 6.5 (đã có 2 field mới).

- [ ] **Bước 1: Thay khối bảng trong `if (survey.has_investment_demand === 1 && survey.investment_demands.length)`**

```js
                    if (survey.has_investment_demand === 1 && survey.investment_demands.length) {
                        worksheet.getCell(`A${rowCursor}`).value = '2. Lĩnh vực đầu tư:'
                        rowCursor += 1

                        const surveyCols = ['A', 'B', 'C', 'D', 'E']
                        worksheet.getCell(`A${rowCursor}`).value = 'STT'
                        worksheet.getCell(`B${rowCursor}`).value = 'Lĩnh vực'
                        worksheet.getCell(`C${rowCursor}`).value = 'Nhóm ngành'
                        worksheet.getCell(`D${rowCursor}`).value = 'Mức đầu tư dự kiến (VNĐ)'
                        worksheet.getCell(`E${rowCursor}`).value = 'Thời gian dự kiến bắt đầu'
                        surveyCols.forEach((col) => {
                            worksheet.getCell(`${col}${rowCursor}`).font = { bold: true }
                            worksheet.getCell(`${col}${rowCursor}`).border = borderThin
                        })
                        rowCursor += 1

                        survey.investment_demands.forEach((d, idx) => {
                            worksheet.getCell(`A${rowCursor}`).value = idx + 1
                            worksheet.getCell(`A${rowCursor}`).alignment = { horizontal: 'center' }
                            // Ghi ten linh vuc o MOI dong (khong bo trong nhu tren man hinh):
                            // file Excel de loc/pivot, o trong lam hong thao tac loc
                            worksheet.getCell(`B${rowCursor}`).value = safeText(d.internal_business_scope_name)
                            worksheet.getCell(`C${rowCursor}`).value = safeText(d.scope_name)
                            // Ghi SO (khong phai chuoi) de Excel SUM duoc
                            // !== null chu KHONG dung truthy: muc dau tu = 0 la gia tri hop le
                            worksheet.getCell(`D${rowCursor}`).value =
                                d.expected_amount !== null && d.expected_amount !== undefined
                                    ? d.expected_amount
                                    : ''
                            worksheet.getCell(`D${rowCursor}`).numFmt = '#,##0'
                            worksheet.getCell(`E${rowCursor}`).value = d.expected_start_date
                                ? dayjs(d.expected_start_date).format('DD/MM/YYYY')
                                : ''
                            worksheet.getCell(`E${rowCursor}`).alignment = { horizontal: 'center' }
                            surveyCols.forEach((col) => {
                                worksheet.getCell(`${col}${rowCursor}`).border = borderThin
                            })
                            rowCursor += 1
                        })
                    }
```

Giữ nguyên `safeText()`, `yesNo()`, phần tiêu đề `KHẢO SÁT NHU CẦU KHÁCH HÀNG` và 2 câu 1/3 bên ngoài khối này.

- [ ] **Bước 2: Verify**

Dựng lại dữ liệu thử như Task 6.6 Bước 2, mở tab Biên bản → nút Xuất Excel.

Kỳ vọng:
- Bảng "2. Lĩnh vực đầu tư" có **5 cột**, cột B lặp tên lĩnh vực ở mọi dòng
- Cột D là **số** (bấm vào ô thấy giá trị số, `SUM` chạy được), định dạng `#,##0`
- Mức đầu tư = 0 vẫn hiện `0`, không để trống

- [ ] **Bước 3: Verify line ending + commit**

```bash
cd HRM/hrm-client && git diff --stat pages/assign/meeting/components/MeetingReport.vue && git add pages/assign/meeting/components/MeetingReport.vue && git commit -m "feat(meeting): file Excel bien ban them cot Nhom nganh"
```

---

### Task 6.8: Cập nhật E2E

**Files:**
- Modify: `HRM/e2e/tests/assign/meeting-investment-survey.spec.ts`

**Interfaces:**
- Consumes: `data-testid` đã có (`investment-survey`, `scope-row`, `scope-check`, `scope-amount`, `scope-date`, `q1-yes`, `q1-no`, `q3-yes`, `q3-no`) + `scope-parent` mới thêm ở Task 6.5.

- [ ] **Bước 1: Đọc lại spec hiện tại để biết ca nào phải thay**

```bash
cd HRM/e2e && grep -n "test(" tests/assign/meeting-investment-survey.spec.ts
```

Ca `'3. Câu 2 hiện/ẩn theo câu 1, đủ 13 lĩnh vực'` **phải thay** — 13 là số bản ghi ERP, không còn đúng.

- [ ] **Bước 2: Thay ca 3 bằng ca đếm động theo DB**

Số dòng kỳ vọng **không viết cứng** — truyền qua env, lấy từ 2 con số đã ghi lại ở Task 6.2 Bước 5
(`E2E_SCOPE_ROW_COUNT` = tổng nhóm ngành active có lĩnh vực cha active; `E2E_SCOPE_PARENT_COUNT` = số lĩnh vực có con).
Cách này bám đúng khuôn env sẵn có của file (`E2E_SYSTEM_MEETING_ID`), tránh dùng `request` fixture vì
`baseURL` của Playwright trỏ FE chứ không trỏ API.

```ts
const SCOPE_ROW_COUNT = Number(process.env.E2E_SCOPE_ROW_COUNT)
const SCOPE_PARENT_COUNT = Number(process.env.E2E_SCOPE_PARENT_COUNT)

test('3. Câu 2 hiện/ẩn theo câu 1, số dòng = số nhóm ngành đang hoạt động', async ({ page }) => {
    expect(SCOPE_ROW_COUNT).toBeGreaterThan(0)

    await openReportTab(page, SYSTEM_MEETING_ID)

    // Chưa trả lời câu 1 -> chưa có bảng
    await expect(page.getByTestId('scope-row')).toHaveCount(0)

    await page.getByTestId('q1-yes').click()
    await expect(page.getByTestId('scope-row')).toHaveCount(SCOPE_ROW_COUNT)

    // Lĩnh vực chỉ hiện tên ở dòng đầu mỗi nhóm -> số nhãn = số lĩnh vực
    await expect(page.getByTestId('scope-parent')).toHaveCount(SCOPE_PARENT_COUNT)

    await page.getByTestId('q1-no').click()
    await expect(page.getByTestId('scope-row')).toHaveCount(0)
})
```

- [ ] **Bước 3: Thêm ca lưu + mở lại đúng nhóm ngành**

```ts
test('7. Lưu nhóm ngành rồi mở lại giữ đúng lĩnh vực cha, số tiền, ngày', async ({ page }) => {
    await openReportTab(page, SYSTEM_MEETING_ID)
    await page.getByTestId('q1-yes').click()

    const firstRow = page.getByTestId('scope-row').first()
    const scopeId = await firstRow.getAttribute('data-scope-id')
    const parentId = await firstRow.getAttribute('data-internal-scope-id')
    expect(parentId).not.toBeNull()

    await firstRow.getByTestId('scope-check').click()
    await firstRow.getByTestId('scope-amount').locator('input').fill('1500000000')
    await firstRow.getByTestId('scope-date').locator('input').fill('01/12/2026')
    await page.getByTestId('q3-no').click()
    await page.getByRole('button', { name: /Lưu/i }).click()
    await expect(page.getByText(/thành công/i)).toBeVisible()

    await page.reload()
    await page.getByRole('tab', { name: /Biên bản/i }).click()

    const savedRow = page.locator(`[data-testid="scope-row"][data-scope-id="${scopeId}"]`)
    await expect(savedRow).toHaveAttribute('data-internal-scope-id', parentId as string)
    await expect(savedRow.getByTestId('scope-amount').locator('input')).toHaveValue(/1,500,000,000|1500000000/)
    await expect(savedRow.getByTestId('scope-date').locator('input')).toHaveValue('01/12/2026')
})
```

- [ ] **Bước 4: Thêm ca bắt buộc khi Hoàn thành**

```ts
test('8. Hoàn thành mà không tích nhóm ngành nào -> báo lỗi', async ({ page }) => {
    await openReportTab(page, SYSTEM_MEETING_ID)
    await page.getByTestId('q1-yes').click()

    // Bỏ tích hết
    const checks = page.getByTestId('scope-check')
    const n = await checks.count()
    for (let i = 0; i < n; i += 1) {
        const cb = checks.nth(i).locator('input')
        if (await cb.isChecked()) await cb.uncheck()
    }

    await page.getByTestId('q3-no').click()
    await page.getByRole('button', { name: /Hoàn thành/i }).click()
    await expect(page.getByText('Vui lòng chọn ít nhất một nhóm ngành.')).toBeVisible()
})
```

- [ ] **Bước 5: Thêm ca phân quyền (bắt buộc — fail-closed)**

Quy tắc dự án: E2E của màn có phân quyền phải cover **cả có quyền lẫn không quyền**.

```ts
test('9. Người không có quyền meeting không vào được màn; người có quyền meeting nhưng không có quyền danh mục nhóm ngành vẫn dựng được bảng', async ({ browser }) => {
    // 9a. Không có quyền meeting -> không vào được màn Sửa meeting
    const ctxNoPerm = await browser.newContext()
    const pageNoPerm = await ctxNoPerm.newPage()
    await new LoginPage(pageNoPerm).login(
        process.env.E2E_NO_PERM_EMAIL as string,
        process.env.E2E_NO_PERM_PASSWORD as string,
    )
    await pageNoPerm.goto(`/assign/meeting/${SYSTEM_MEETING_ID}/edit`)
    await expect(pageNoPerm.getByTestId('investment-survey')).toHaveCount(0)
    await ctxNoPerm.close()

    // 9b. Có quyền meeting, KHÔNG có quyền danh mục nhóm ngành -> bảng vẫn dựng đủ dòng
    // (2 endpoint getAll và endpoint investment-scopes đều không gắn checkPermission)
    const ctxMeetingOnly = await browser.newContext()
    const pageMeetingOnly = await ctxMeetingOnly.newPage()
    await new LoginPage(pageMeetingOnly).login(
        process.env.E2E_MEETING_ONLY_EMAIL as string,
        process.env.E2E_MEETING_ONLY_PASSWORD as string,
    )
    await openReportTab(pageMeetingOnly, SYSTEM_MEETING_ID)
    await pageMeetingOnly.getByTestId('q1-yes').click()
    await expect(pageMeetingOnly.getByTestId('scope-row')).toHaveCount(SCOPE_ROW_COUNT)
    await ctxMeetingOnly.close()
})
```

2 tài khoản trên lấy từ fixture đã dùng ở Phase 5; nếu chưa có thì dựng bằng cách gán/thu hồi role như
`hrm-api/database/e2e_internal_scope_fixture.php` (feature `linh-vuc-kinh-doanh-noi-bo`) đã làm, và **ghi
lại vào plan** id tài khoản đã tạo để dọn sau.

- [ ] **Bước 6: Đổi mọi câu chữ "lĩnh vực" thành "nhóm ngành" ở các ca còn lại**

Rà cả file: ca kiểm lỗi bỏ trống mức đầu tư / thời gian, ca nhóm ngành đã khoá không cho tích lại. Câu lỗi BE nay là **"Nhóm ngành không tồn tại hoặc đã bị xoá."** và **"Mỗi nhóm ngành chỉ được chọn một lần."**

- [ ] **Bước 7: Chạy E2E**

```bash
cd HRM/e2e && E2E_SCOPE_ROW_COUNT=<so ghi lai o Task 6.2 Buoc 5> E2E_SCOPE_PARENT_COUNT=<so ghi lai o Task 6.2 Buoc 5> \
  npx playwright test tests/assign/meeting-investment-survey.spec.ts --reporter=list
```

Kỳ vọng: **tất cả ca PASS**. Ca nào fail vì chưa có meeting loại hệ thống trên `hrm_tpe` → chạy `php artisan db:seed --class=Modules\\Assign\\Database\\Seeders\\SystemMeetingTypesSeeder` trước (việc còn treo từ Phase 1-5).

- [ ] **Bước 8: Commit**

```bash
cd HRM/e2e && git add tests/assign/meeting-investment-survey.spec.ts && git commit -m "test(meeting): E2E khao sat theo nhom nganh"
```

---

### Checkpoint — Phase 6

Sau Task 6.8:

1. `grep -rn "TpScope\|mysql2.scopes" HRM/hrm-api --exclude-dir=vendor` → **không dòng nào**.
2. Mở meeting loại hệ thống, tab Biên bản: bảng 5 cột, gom nhóm đúng.
3. Bản in: `rowspan` đúng. File Excel: 5 cột, cột D là số.
4. E2E toàn bộ PASS.
5. Cập nhật `.plans/STATUS.md` mục `meeting-tim-hieu-gioi-thieu-sp`: ghi Phase 6 đã xong, ghi rõ **dữ liệu khảo sát cũ đã bị migration xoá**, và nhắc môi trường khác phải chạy `php artisan migrate`.

### Checkpoint — Phase 6 (2026-08-23, wrap up)

**Đã xong:** 8/8 task, mỗi task 1 reviewer riêng; 2 task phải fix 1 vòng (6.1 nullability, 6.8 thiếu ca test); review toàn nhánh bằng opus → 1 Important + 6 Minor → 1 đợt fix → re-review **8/8 ADDRESSED, 0 hỏng mới**.

**Commit (local, CHƯA push):**

| repo | dải commit | số commit |
|---|---|---|
| `hrm-api` | `abdd60a`..`2b18830` | 7 |
| `hrm-client` | `edae337`..`64c9e9e` | 4 |
| `e2e` | — | không commit được (không phải git repo) |

**Bug tự bắt & sửa trong lúc làm:**
1. `renameColumn` không đổi nullability → `internal_business_scope_id` còn `NOT NULL`, sẽ chết lỗi 1048 khi ghi NULL cho nhóm ngành mồ côi.
2. Drop unique cũ trực tiếp ăn lỗi MySQL 1553 (FK `meeting_id` cần index hỗ trợ) → phải thêm index tạm rồi gỡ.
3. Code mẫu E2E trong plan tìm `<input>` lồng trong `<input>` — `V2BaseCurrencyInput`/`V2BaseCheckbox` dùng `inheritAttrs:false` + `v-bind="$attrs"` nên `data-testid` nằm thẳng trên `<input>`.
4. Ca E2E phân quyền dùng chung meeting cũ sẽ bị `canManage()` đá sang `/show` (khoá hết input) → fixture phải tạo meeting riêng do chính tài khoản đó tạo.
5. Danh mục rỗng hợp lệ bị báo **đỏ** "Không tải được danh mục" — sai bản chất, vi phạm quy tắc chữ đỏ.
6. Cửa thoát chống kẹt màn Hoàn thành dùng luật lỏng hơn luật dựng bảng (thiếu điều kiện lĩnh vực cha Hoạt động).
7. CSS đường ngăn nhóm ra viền đôi 3px hai tông (border-bottom 1px + border-top 2px cộng dồn).

**CÒN LẠI — đều cần môi trường hoặc mắt người:**
1. `.plans/meeting-tim-hieu-gioi-thieu-sp/phase6-kiem-thu-cong.md` — 11 mục kiểm bằng mắt (UI, bản in, Excel, E2E chạy thật).
2. Chạy `hrm-api/database/e2e_meeting_survey_fixture.php` (idempotent, chỉ tạo tài khoản E2E riêng, không đụng user/role sẵn có) rồi đặt env → mở khoá 2 ca E2E phân quyền + ca nhóm ngành khoá.
3. Môi trường khác: `php artisan migrate` — migration `2026_08_23_000001` **xoá sạch** `meeting_investment_demands`.

**Minor đã hoãn có chủ đích (không chặn merge):** `groupBy` gom mọi dòng mồ côi vào chung 1 khối rowspan nhãn rỗng · `(int)($item['scope_id'] ?? 0)` nuốt im lặng giá trị không phải số · nhánh `catch` của store trả cache thiếu mục khoá (kế thừa code cũ) · `knownIds` tính 1 lần nên `:key` trùng nếu BE trả 2 bản ghi mồ côi trùng `scope_id` (lỗ hổng có sẵn trước Phase 6).

---

# PHASE 7 — Chọn cặp Lĩnh vực » Nhóm ngành (thay bảng phẳng của Phase 6)

> **Cho agent thực thi:** dùng `superpowers:subagent-driven-development`. Các bước dùng checkbox `- [ ]`.

**Goal:** Thay cách chọn ở khối Khảo sát: từ bảng liệt kê toàn bộ nhóm ngành → **2 ô select cặp cha-con có tìm kiếm** (`CascadePairSelect`), bảng chỉ chứa dòng đã chọn, có dòng Tổng + dòng lĩnh vực số La Mã.

**Spec:** `.plans/meeting-tim-hieu-gioi-thieu-sp/design-phase2.md` — **mục 10–18** (phần "ĐỢT CẬP NHẬT 2026-08-23"). Mục 4.6/4.7/4.8 của spec đã bị thay thế, đừng làm theo.

**Nguồn chân lý về hành vi + giao diện:** `.plans/meeting-tim-hieu-gioi-thieu-sp/demo/khao-sat-nhom-nganh.html` — mockup user đã duyệt. Mở đọc trước khi code FE. Chi tiết tương tác nào spec không nói thì lấy theo mockup.

**Nhánh:** `tpe` ở cả 2 repo. BASE: `hrm-api 2b18830c3` · `hrm-client 64c9e9e21`.

## Global Constraints — Phase 7

Ngoài Global Constraints đầu file (vẫn áp) và của Phase 6 (vẫn áp), thêm:

- **Tái dùng `components/assign-components/CascadePairSelect.vue`**, KHÔNG viết component chọn cặp mới. Nếu thiếu tính năng (đóng/mở nhóm, badge đếm) thì **thêm prop tuỳ chọn có default giữ nguyên hành vi cũ** — tuyệt đối không đổi hành vi của 2 màn đang dùng nó (`pages/assign/customers`, `pages/assign/prospective-projects`).
- Mockup dùng `window.confirm()` chỉ để demo. Bản thật **bắt buộc** dùng `await this.$confirm({...})`.
- Bảng dùng style tiêu đề của `components/V2BaseDataTable.vue` (nền `#f8fafc`, viền `1px solid #e5e7eb`, 12px, padding `6px 8px`, không in hoa), **không** áp zebra `nth-child(even)`.
- Giữ nguyên: endpoint `investment-scopes`, schema `meeting_investment_demands`, `MeetingService::syncInvestmentDemands()` (chỉ bổ sung, không viết lại), store `optionsSelect.js`.
- Bấm Lưu/Hoàn thành 1 lần phải hiện **hết** lỗi mọi ô, không bắt sửa từng ô.

## File Structure — Phase 7

### `hrm-api`
| File | Trách nhiệm |
|------|-------------|
| `Modules/Assign/Database/Migrations/2026_08_24_000001_create_meeting_investment_scopes_table.php` | **Mới** |
| `Modules/Assign/Entities/Meeting/MeetingInvestmentScope.php` | **Mới** |
| `Modules/Assign/Entities/Meeting/Meeting.php` | Sửa — relation `investment_scopes()` |
| `Modules/Assign/Services/MeetingService.php` | Sửa — `syncInvestmentScopes()` |
| `Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` | Sửa — `$request->only()` + gọi sync + eager load |
| `Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php` · `MeetingUpdateApiRequest.php` | Sửa — rule + message lĩnh vực |
| `Modules/Assign/Transformers/MeetingResource/MeetingTransformer.php` | Sửa — trả `investment_scopes` |
| `resources/views/exports/meeting_record.blade.php` | Sửa — bảng bố cục mới |

### `hrm-client`
| File | Trách nhiệm |
|------|-------------|
| `pages/assign/meeting/components/MeetingInvestmentSurvey.vue` | **Viết lại** phần câu 2 + 3 |
| `pages/assign/meeting/components/MeetingReport.vue` | Sửa — Excel bố cục mới |
| `pages/assign/meeting/components/MeetingForm.vue` | Sửa — vá null-guard `work_position` |
| `components/assign-components/CascadePairSelect.vue` | Sửa — thêm prop tuỳ chọn: đóng/mở nhóm + badge đếm |

---

### Task 7.1: Bảng `meeting_investment_scopes` + Entity + relation

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_08_24_000001_create_meeting_investment_scopes_table.php`
- Create: `hrm-api/Modules/Assign/Entities/Meeting/MeetingInvestmentScope.php`
- Modify: `hrm-api/Modules/Assign/Entities/Meeting/Meeting.php`

**Interfaces:**
- Produces: bảng `meeting_investment_scopes(id, meeting_id, internal_business_scope_id, internal_business_scope_name, position, created_by, updated_by, timestamps)`, `unique(meeting_id, internal_business_scope_id)`, `index(internal_business_scope_id)`, FK `meeting_id` cascade.
- Produces: `Meeting::investment_scopes()` hasMany order theo `position`.

- [ ] **Bước 1: Viết migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Linh vuc kinh doanh noi bo user CHON o khoi Khao sat (cau 2).
 * Luu rieng vi user co the chon 1 linh vuc ma CHUA tich nhom nganh nao —
 * truong hop do khong suy nguoc ra tu bang meeting_investment_demands duoc.
 */
class CreateMeetingInvestmentScopesTable extends Migration
{
    public function up()
    {
        Schema::create('meeting_investment_scopes', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('meeting_id')->comment('FK meetings.id');
            $table->unsignedBigInteger('internal_business_scope_id')
                ->comment('id bang internal_business_scopes HRM. KHONG dat FK: xoa danh muc khong duoc lam hong bien ban cu');
            $table->string('internal_business_scope_name', 255)->comment('Snapshot ten linh vuc tai thoi diem luu');
            $table->integer('position')->default(0);
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();

            $table->unique(['meeting_id', 'internal_business_scope_id'], 'mis_meeting_scope_unique');
            $table->index('internal_business_scope_id', 'mis_scope_id_index');
            $table->foreign('meeting_id')->references('id')->on('meetings')->onDelete('cascade');
        });
    }

    public function down()
    {
        Schema::dropIfExists('meeting_investment_scopes');
    }
}
```

Tên index đặt ngắn (`mis_*`) vì tên mặc định của Laravel sẽ vượt giới hạn 64 ký tự của MySQL.

- [ ] **Bước 2: Entity**

`MeetingInvestmentScope.php` — `extends BaseModel` (bắt buộc theo Global Constraints), `$table = 'meeting_investment_scopes'`, `$fillable` gồm `meeting_id, internal_business_scope_id, internal_business_scope_name, position, created_by, updated_by`, quan hệ `meeting()` belongsTo. Docblock nêu rõ vì sao lưu riêng (xem comment migration).

- [ ] **Bước 3: Relation trên `Meeting`**

Thêm cạnh `investment_demands()`:

```php
    /** Linh vuc user chon o cau 2 (ke ca linh vuc chua tich nhom nganh nao) */
    public function investment_scopes()
    {
        return $this->hasMany(MeetingInvestmentScope::class, 'meeting_id', 'id')
            ->orderBy('position');
    }
```

- [ ] **Bước 4: Lint + migrate + verify schema**

```bash
cd HRM/hrm-api
/opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Database/Migrations/2026_08_24_000001_create_meeting_investment_scopes_table.php
/opt/homebrew/opt/php@7.4/bin/php -l Modules/Assign/Entities/Meeting/MeetingInvestmentScope.php
/opt/homebrew/opt/php@7.4/bin/php artisan migrate
/opt/homebrew/opt/mysql@8.0/bin/mysql -h127.0.0.1 -uroot -p'Dnsmedia@2025!' hrm_tpe -e "SHOW CREATE TABLE meeting_investment_scopes\G"
```

Kỳ vọng: đủ cột, `UNIQUE KEY mis_meeting_scope_unique (meeting_id, internal_business_scope_id)`, FK cascade tới `meetings`.

- [ ] **Bước 5: Verify rollback sạch rồi migrate lại**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan migrate:rollback --step=1 && /opt/homebrew/opt/php@7.4/bin/php artisan migrate
```

- [ ] **Bước 6: Commit** (local, KHÔNG push)

---

### Task 7.2: Lưu + validate lĩnh vực đã chọn

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/MeetingService.php`
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php`
- Modify: `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php`, `MeetingUpdateApiRequest.php`
- Modify: `hrm-api/Modules/Assign/Transformers/MeetingResource/MeetingTransformer.php`

**Interfaces:**
- Consumes: Task 7.1.
- Produces: payload nhận thêm `investment_scopes: [{ internal_business_scope_id, internal_business_scope_name }]`; API trả về `investment_scopes` trong `MeetingTransformer`.

- [ ] **Bước 1: `MeetingService::syncInvestmentScopes($scopes, $entity)`**

Bám **đúng khuôn** `syncInvestmentDemands()` ngay phía trên nó: câu 1 ≠ Có → `$entity->investment_scopes()->delete()` rồi return; `!is_array($scopes)` → mảng rỗng; xoá hết rồi ghi lại; snapshot tên **tra 1 lần cho cả mảng** bằng `InternalBusinessScope::whereIn(...)->pluck('name','id')` (KHÔNG query trong vòng lặp); tên ưu tiên giá trị DB, thiếu thì lấy từ payload; `position` = chỉ số dòng; bỏ qua phần tử thiếu id.

- [ ] **Bước 2: Nối vào controller**

Trong `MeetingController::store()` và `update()`: thêm `'investment_scopes'` vào `$request->only([...])` **nếu** danh sách đó có liệt kê field khảo sát, và gọi `$this->service->syncInvestmentScopes($request->investment_scopes, $entity);` **ngay cạnh** lời gọi `syncInvestmentDemands(...)` đã có (2 chỗ: dòng ~242 và ~437). Thêm `'investment_scopes'` vào mảng eager load của `show()` và `print()`.

- [ ] **Bước 3: Transformer**

Thêm `'investment_scopes' => $meeting->investment_scopes,` ngay cạnh `'investment_demands'`.

- [ ] **Bước 4: Validate**

Ở **cả 2** FormRequest, trong khối `if ($needSurvey)`:

```php
$rules['investment_scopes']                                  = 'nullable|array';
$rules['investment_scopes.*.internal_business_scope_id']     = 'required|integer|min:1|distinct|exists:internal_business_scopes,id';
$rules['investment_scopes.*.internal_business_scope_name']   = 'nullable|string|max:255';
```

`messages()` thêm:

```php
'investment_scopes.*.internal_business_scope_id.exists'   => 'Lĩnh vực kinh doanh nội bộ không tồn tại hoặc đã bị xoá.',
'investment_scopes.*.internal_business_scope_id.distinct' => 'Mỗi lĩnh vực chỉ được chọn một lần.',
```

Trong closure `after()` của `MeetingUpdateApiRequest` (chỉ chạy khi `status = 3`), **trước** phần kiểm nhóm ngành: nếu `investment_scopes` rỗng → `$v->errors()->add('investment_scopes', 'Vui lòng chọn ít nhất một lĩnh vực.');` rồi `return`. Giữ nguyên ngoại lệ "cả danh mục không còn nhóm ngành Hoạt động" đã có.

- [ ] **Bước 5: Lint 5 file + verify bằng tinker**

Dựng 1 meeting loại `HOP_TIM_HIEU_GIOI_THIEU_SP`, gọi `syncInvestmentScopes` với 1 lĩnh vực **không** kèm nhóm ngành nào, đọc lại `investment_scopes()` → phải còn đúng 1 dòng, tên lấy từ DB (không phải tên sai FE gửi). Dọn dữ liệu thử sau khi xong. In output thật.

- [ ] **Bước 6: Commit**

---

### Task 7.3: `CascadePairSelect` — thêm đóng/mở nhóm + badge đếm

**Files:**
- Modify: `hrm-client/components/assign-components/CascadePairSelect.vue`

**Interfaces:**
- Produces: 2 prop tuỳ chọn `collapsibleChildGroups` (Boolean, default `false`) và `showChildGroupCount` (Boolean, default `false`).

- [ ] **Bước 1: Đọc kỹ component + 2 nơi đang dùng**

```bash
cd HRM/hrm-client && grep -rn "CascadePairSelect" pages components | grep -v "CascadePairSelect.vue"
```

Ghi lại 2 màn đang dùng. **Mọi thay đổi phải giữ nguyên hành vi khi 2 prop mới = false.**

- [ ] **Bước 2: Thêm đóng/mở nhóm trong panel CON**

Chỉ áp cho panel con, KHÔNG đụng panel cha. Dòng tiêu đề nhóm: icon **SVG chevron inline** xoay theo trạng thái (thu gọn = `rotate(-90deg)`, bung = `rotate(0)`), có transition. Bấm icon hoặc tên → đóng/mở; bấm checkbox → chỉ tick cả nhóm (tách sự kiện, kiểm `closest()` trước). Mặc định bung. Đang gõ tìm kiếm thì nhóm có kết quả khớp **tự bung**, không ghi đè state đóng/mở user đã đặt.

- [ ] **Bước 3: Badge đếm**

Cuối dòng tiêu đề nhóm: `N/M` = số con **đang chọn** / **tổng số con của nhóm đó** (tính trên toàn bộ, không phụ thuộc search hay trạng thái thu gọn). Ẩn khi `N = 0`. Style: 11px, nền `#f1f5f9`, chữ `#6b7280`, bo tròn.

- [ ] **Bước 4: Verify không phá 2 màn cũ**

```bash
cd HRM/hrm-client && file components/assign-components/CascadePairSelect.vue && git diff --stat components/assign-components/CascadePairSelect.vue
```

Đọc lại diff: xác nhận mọi nhánh mới đều nằm sau `v-if="collapsibleChildGroups"` / `v-if="showChildGroupCount"`, và 2 màn cũ không truyền prop nên đi đúng nhánh cũ. Ghi rõ kết luận này vào báo cáo.

- [ ] **Bước 5: Commit**

---

### Task 7.4: Viết lại `MeetingInvestmentSurvey.vue`

**Files:**
- Modify: `hrm-client/pages/assign/meeting/components/MeetingInvestmentSurvey.vue`

**Interfaces:**
- Consumes: Task 7.3; endpoint cây 2 tầng (Phase 6) qua `optionsSelect/fetchInvestmentScopes`.
- Produces: `buildPayload()` trả `{ has_investment_demand, has_maintenance_demand, investment_scopes: [{internal_business_scope_id, internal_business_scope_name}], investment_demands: [{scope_id, scope_name, internal_business_scope_id, internal_business_scope_name, expected_amount, expected_start_date}] }`. Giữ nguyên tên `loadScopes()` (MeetingReport đang gọi).

- [ ] **Bước 1: Đọc mockup trước khi viết**

```bash
sed -n '1,80p' HRM/.plans/meeting-tim-hieu-gioi-thieu-sp/demo/khao-sat-nhom-nganh.html
```

Đọc hết phần `<script>` của mockup để nắm state + các hàm render. **Không chép nguyên JS thuần sang Vue** — chuyển sang state/computed/method của Vue 2, nhưng giữ đúng hành vi.

- [ ] **Bước 2: Câu 2 — cặp select**

Dùng `CascadePairSelect` với `collapsibleChildGroups` + `showChildGroupCount`, xếp **dọc**. `parentOptions` = mảng lĩnh vực từ `scopeOptions`; `childOptions` = phẳng hoá `industry_groups` thành `{ id, name, parent_ids: [linhVucId] }`. `v-model` = mảng cặp `{parent_id, child_id}`; `:parents` + `@parents-change` để giữ lĩnh vực chọn mà chưa có nhóm ngành.

- [ ] **Bước 3: Câu 3 + bảng**

Theo mục 14 của spec và mockup: dòng tóm tắt `Đang chọn: N lĩnh vực · M nhóm ngành`; bảng có dòng `Tổng:`, dòng lĩnh vực La Mã (tiền tự cộng, chỉ đọc), nhóm ngành đếm lại từ 1 và thụt lề; **không** có nút `×`; tiền dùng `V2BaseCurrencyInput`, ngày dùng `V2BaseDatePicker` + `disablePastDates` (giữ nguyên 2 component cũ).

- [ ] **Bước 4: Giữ nguyên các phần không đổi**

Câu 1 và câu 4 (radio + `V2BaseError`), watcher `form.id`, watcher `surveyState` ghi ngược vào `form`, `hydrateFromForm`, `errorFor`/`payloadIndexOf`, 2 khối "Đang tải…" / "Không tải được…". Đổi số hiển thị câu bảo trì 3 → 4. Hộp xác nhận dùng `await this.$confirm({...})`.

- [ ] **Bước 5: Verify tĩnh**

`file` + `git diff --stat` (kiểm line ending), đọc lại toàn file đối chiếu mockup, đếm cột grid = 12 ở cả header lẫn dòng dữ liệu.

- [ ] **Bước 6: Commit**

---

### Task 7.5: Bản in + Excel theo bố cục mới

**Files:**
- Modify: `hrm-api/resources/views/exports/meeting_record.blade.php`
- Modify: `hrm-client/pages/assign/meeting/components/MeetingReport.vue`

- [ ] **Bước 1: Bản in**

Thay bảng `rowspan` của Phase 6 bằng bố cục mục 14: dòng `Tổng:`, dòng lĩnh vực La Mã (tiền = tổng con), nhóm ngành đếm lại từ 1. Gom nhóm bằng `$meeting->investment_demands->groupBy('internal_business_scope_id')`. Giữ `number_format($d->expected_amount, 0, ',', ',')` và `format('d/m/Y')`. Giữ đánh số `IV/` + các mục con.

- [ ] **Bước 2: Excel**

Cùng bố cục. Giữ nguyên: ghi **số** + `numFmt '#,##0'`, điều kiện `!== null && !== undefined` để 0 vẫn hiện, `safeText()` cho mọi cột tên.

- [ ] **Bước 3: Verify**

Dựng dữ liệu thử 2 lĩnh vực × nhiều nhóm ngành bằng tinker, render blade lấy **HTML thật** ghi ra file tạm, trích đoạn bảng vào báo cáo, tự kiểm số dòng/số cột/STT/tổng tiền. Dọn dữ liệu thử.

- [ ] **Bước 4: Commit** (mỗi repo 1 commit)

---

### Task 7.6: Vá bug `work_position` + E2E

**Files:**
- Modify: `hrm-client/pages/assign/meeting/components/MeetingForm.vue`
- Modify: `HRM/e2e/tests/assign/meeting-investment-survey.spec.ts`

- [ ] **Bước 1: Vá null-guard**

`MeetingForm.vue:997` và `:1018`: `currentEmployee.info.work_position.name` → kiểm null, fallback `''`. Không đụng gì khác trong `initializeCompanyMembers()`.

- [ ] **Bước 2: Viết lại E2E theo UI mới**

Giữ nguyên khuôn file hiện tại (`LoginPage`, `test.describe`, đọc env). Phủ đủ: chọn lĩnh vực → ô nhóm ngành lọc đúng · tick con tự thêm cha · đóng/mở nhóm · badge `N/M` · bảng dựng đúng Tổng/La Mã/đếm lại · tổng tiền tự cộng · validate báo hết lỗi cùng lúc · **ca phân quyền fail-closed** (bắt buộc) · nhóm ngành đã khoá không cho tích lại.

Selector bám `data-testid`; số lượng đọc từ env, không viết cứng.

- [ ] **Bước 3: Chạy thật**

Bật API (`artisan serve :8000`) + FE (`npm run dev`, Node 12 + heap 8192), chạy Playwright bằng **Node 20**:

```bash
cd HRM/e2e && npx playwright test tests/assign/meeting-investment-survey.spec.ts --reporter=list
```

Fixture đã dựng sẵn trên `hrm_tpe` (meeting 44/45/46, tài khoản `e2e_*@test.local`) — xem `e2e/.env`. Dán output thật vào báo cáo.

- [ ] **Bước 4: Commit** (`e2e/` không phải git repo → chỉ commit `hrm-client`)

---

### Checkpoint — Phase 7

1. Mở màn Sửa meeting loại hệ thống → tab Biên bản: 4 câu, cặp select hoạt động, bảng đúng bố cục.
2. Bản in + Excel đúng bố cục mới.
3. E2E chạy thật PASS.
4. `pages/assign/customers` và `pages/assign/prospective-projects` không đổi hành vi (regression `CascadePairSelect`).
5. Cập nhật `.plans/STATUS.md`.

### Checkpoint — Phase 7 (2026-08-24, wrap up)

**Đã xong:** 6/6 task, mỗi task 1 reviewer riêng; 3 task phải fix 1 vòng (7.2, 7.4, 7.6); review toàn nhánh bằng opus → 3 Important + 5 Minor → 1 đợt fix 9 việc → re-review **9/9 ADDRESSED, 0 hỏng mới**.

**E2E chạy THẬT: 20/20 xanh, 0 skip** (khác Phase 6 chỉ compile-check).

**Commit (local, CHƯA push):**

| repo | dải commit | số commit |
|---|---|---|
| `hrm-api` | `60af8ca`..`43245bd` | 6 |
| `hrm-client` | `11f8f97`..`8816d49` | 7 |
| `e2e` | — | không commit được (không phải git repo) |

**Bug tự bắt & sửa (ngoài phần thiết kế):**
1. **Regression do chính Phase 7**: chuyển sang `CascadePairSelect` làm **mất** enforcement khoá nhóm ngành mà Phase 6 đã cài → nhóm ngành đã khoá tích lại được. Reviewer tự đào từ `git log`, không ai báo.
2. **Ngày lưu lệch 1 ngày** khi mở lại (cast `date` + timezone +7 → serialize UTC). Mới do Phase 7.
3. **Lỗi validate bị giấu**: `tabForErrorKey()` không nhận key khảo sát → nhảy nhầm tab, user không thấy lỗi.
4. **Lỗi BE `scope_id` không có chỗ hiển thị** → nhóm ngành bị admin xoá làm user kẹt không biết bỏ tích dòng nào.
5. **Panel con lọc sai** khi mở lại meeting có lĩnh vực chưa chọn nhóm ngành — đúng ca mà Phase 7 sinh ra để hỗ trợ.
6. **Huỷ hộp xác nhận làm checkbox lệch state** — cách vá đầu (`$forceUpdate()`) KHÔNG đủ, ca E2E mới bắt được, phải đổi sang ép tạo lại DOM.
7. **1 ca E2E là test giả**: DB chỉ có 1 lĩnh vực có nhóm ngành con nên ca "lọc theo lĩnh vực" pass kể cả khi xoá hẳn cơ chế lọc → seed thêm lĩnh vực E2E riêng.
8. Bug có sẵn: `MeetingForm.vue` crash màn Sửa với user thiếu chức danh (đã vá null-guard).

**2 lỗi soạn spec của chính tôi, đã đính chính (không sửa code):**
- Mục 14 ghi phân cách nghìn dấu **chấm** → thực tế là dấu **phẩy** (quyết định #5 gốc + `V2BaseCurrencyInput` + `number_format` bản in).
- Mục 13 ghi câu 4 hiện khi "câu 1 = Có" → sai, câu 4 **độc lập**; ẩn nó sẽ làm user kẹt vì BE vẫn bắt buộc trả lời.

**CÒN LẠI:**
1. Nghiệm thu bằng mắt: bảng câu 3, panel đóng/mở + badge, bản in nhiều lĩnh vực, file Excel thật.
2. Parked: 1 comment lạc hậu ở `e2e/.../meeting-investment-survey.spec.ts:553` còn nhắc `serializeDate()`.
3. Môi trường khác: chạy `php artisan migrate` (bảng `meeting_investment_scopes`).
4. `hrm-api/database/e2e_meeting_survey_seed.php` tạo bản ghi danh mục tiền tố `E2E` — chỉ chạy trên môi trường test.

---

## PHASE 8 — Tinh chỉnh UI theo phản hồi user (2026-08-24)

Không phải phase code mới — gom các yêu cầu chỉnh giao diện user nêu sau khi nghiệm thu Phase 7. Mỗi việc đều đã kiểm bằng trình duyệt thật trên `hrm_tpe`, và chạy lại bộ E2E sau mỗi đợt.

### Đợt 1 — 3 việc
- [x] Icon mục "Khảo sát nhu cầu khách hàng" dùng đúng màu brand như các mục cùng cấp
- [x] 4 câu hỏi thụt lề so với tiêu đề mục cha
- [x] 2 ô chọn Lĩnh vực / Nhóm ngành xếp cùng hàng, chia đôi

### Đợt 2 — 3 việc
- [x] Cột STT ở bảng "Nội dung khác" và "Tài liệu đính kèm" đổi từ ô nhập sang text
- [x] Radio Có/Không nằm cùng hàng với câu hỏi
- [x] Dời nút In / Excel lên đầu tab Biên bản; nút In mở popup xem trước

### Đợt 3 — 6 việc
- [x] Radio Có/Không căn giữa theo chiều dọc với câu hỏi
- [x] Header MỌI bảng trong form meeting (tất cả các tab): chữ thường + `font-weight: bold`
- [x] Giá trị cột STT căn giữa
- [x] Panel Nhóm ngành: cấp con thụt lề so với cấp cha
- [x] Màn TẠO meeting ẩn nút In / Xuất Excel
- [x] Popup xuất Excel theo mẫu popup in Báo giá (chọn phần → tải thẳng file)

### Đợt 4 — làm lại luồng In cho đúng chuẩn Báo giá
- [x] Khảo sát lại chuẩn: `QuotationPrintConfigModal` → `QuotationPrintPreview`
- [x] Gộp popup cấu hình dùng chung cho cả In và Excel (`MeetingPartsConfigModal.vue`)
- [x] `MeetingPrintPreview.vue` mới: xl + scrollable + hide-footer + `print-preview-modal`, nút In cạnh tiêu đề, nội dung render bằng Vue
- [x] Gỡ sạch iframe + nhánh `?embed=1` ở trang in
- [x] Ghi chú chéo `meeting_record.blade.php` ↔ `MeetingPrintPreview.vue`

**Commit (local, CHƯA push):** `hrm-client` `2a0afdb`..`9839d6d` (5) · `hrm-api` `9078a6a` (1)

**Lỗi tự bắt được khi kiểm bằng mắt — đọc code đều lọt:**
1. Icon bị đen vì `.text-brand` khai trong `<style scoped>` của `MeetingReport.vue` nên không áp xuống component con.
2. Đặt cứng `flex: 0 0 50%` cho 2 ô select làm ô thứ hai **tràn 13px** khỏi khung (do `gap: 12px`) → đổi sang `flex: 1 1 0`.
3. Popup xem trước bản đầu nhúng iframe kéo theo **cả sidebar ứng dụng** vào khung xem trước.
4. Agent kết luận "nhóm ngành con đã thụt lề sẵn" dựa trên CSS (`padding-left` 32px vs 12px) — **đo thật thì chữ hai cấp rơi đúng cùng mốc 955px** vì dòng cha có chevron bù trừ.
5. Bỏ tích 1 phần khi in → mục biến mất nhưng **số La Mã không lùi**, in ra `I, II, IV`.

**NỢ KỸ THUẬT MỚI (user đã chấp nhận khi chọn phương án):** bản in có **HAI nguồn** — blade server `meeting_record.blade.php` (mở tab in thật, in từ màn danh sách) và Vue `MeetingPrintPreview.vue` (xem trước). Đã ghi chú chéo ở cả 2 file. Ngoài ra header "Số biên bản / Ngày lập" của bản in server đọc từ `print_templates` trong DB (admin cấu hình được), còn bản Vue dựng tĩnh tương đương → đổi print template thì bản xem trước không đổi theo.

### Đợt 5 — icon xoá từng dòng bảng "Mức đầu tư / Thời gian" (2026-08-24)
- [x] Mỗi dòng nhóm ngành có icon thùng rác cuối dòng; bấm là **bỏ chọn luôn nhóm ngành tương ứng ở ô select**
- [x] Chỉ hỏi xác nhận khi dòng đó **đã nhập** mức đầu tư/thời gian (user chốt); dòng trống xoá thẳng
- [x] Xoá nhóm ngành cuối của một lĩnh vực **KHÔNG** bỏ chọn lĩnh vực đó (user chốt)
- [x] E2E ca 18 (3 nhánh a/b/c) — bộ meeting **21/21 xanh**

**Cách làm**: chỉ bỏ đúng 1 cặp khỏi `pairs` trong `MeetingInvestmentSurvey.vue#onRemoveRow()`. `pairs` là
v-model của `CascadePairSelect` nên checkbox tự nhả và watcher `pairs` sẵn có tự dọn tiền/ngày —
**KHÔNG đụng** `CascadePairSelect.vue` (5 màn khác đang dùng) và không đụng BE / bản in / Excel.
Nút xoá đặt TRONG ô cột cuối cạnh datepicker theo đúng pattern bảng "Các nội dung khác"
(`MeetingReport.vue:226`), không thêm cột thứ 5.

**2 việc phát sinh, đã xử lý:**
1. `V2BaseButton` **không có prop `danger`** (chỉ `status="danger"`) → 2 nút xoá sẵn có ở tab Biên bản
   (bảng Các nội dung khác + Tài liệu đính kèm) lâu nay ra **màu xám** chứ không đỏ. Đã đổi cả 3 nút
   sang `status="danger"` cho đồng bộ.
2. Thêm nút vào cột `col-2` làm **datepicker bị bóp, cắt cụt** (`20/12/202`, `Chọn ngà`) — chỉ thấy khi
   chụp màn hình, đọc code không lộ. Cân lại bề ngang: Lĩnh vực/Nhóm ngành `col-5`→`col-4`,
   Thời gian `col-2`→`col-3` (vẫn 4 cột, header không đổi).

**Bẫy đã dính rồi trả lại**: sửa `MeetingReport.vue` bằng script python mặc định → **phá CRLF toàn file**
(`git diff --stat` báo 2904 dòng). Đúng mục 379 CLAUDE.md. Đã `git checkout` và làm lại bằng
`io.open(..., newline='')` → còn đúng 4 dòng.

### Đợt 6 — 5 tinh chỉnh UI theo phản hồi user (2026-08-24)
- [x] Tiêu đề cột STT căn giữa ở MỌI bảng trong meeting (3 bảng còn thiếu: Khảo sát, Các nội dung khác, Tài liệu đính kèm — 2 bảng Thành phần đã căn sẵn)
- [x] Cột "Mức đầu tư dự kiến" căn phải ĐỒNG NHẤT cả cột
- [x] Radio Có/Không căn đúng dòng câu hỏi (lệch 9.6px → **0px**, đo thật)
- [x] Đánh số câu hỏi "1." → **"Câu 1."** cho khỏi lẫn với đầu mục La Mã
- [x] Nút thêm "Thành phần — Phía Công ty" đổi về đúng kiểu nút "Phía Khách hàng" (vuông nhỏ `tertiary` + `ri-add-line`)

**Việc 3 — thủ phạm KHÔNG nằm trong meeting.** `assets/scss/custom-theme.scss` (khối "Custom input
Material") có rule **thiếu tiền tố `.mate-field`**:
```css
input:not(:placeholder-shown) + label { top: 0; transform: translateY(-50%) scale(1); }
```
Radio/checkbox không có placeholder nên `:not(:placeholder-shown)` LUÔN đúng → **mọi**
`.custom-control-label` của bootstrap-vue trong TOÀN APP bị kéo lên nửa dòng. 3 rule ngay trên nó
đều có `.mate-field`, riêng dòng này sót. Đợt 3 trước đây chỉ căn được chấm tròn BÊN TRONG label nên
nhìn vẫn lệch. Lần này hoá giải trong phạm vi `.q-item` (`transform: none`) — **chưa sửa rule gốc**
vì blast radius toàn app, để user quyết.

**Việc 2 — căn phải "đồng nhất" cần thêm 12px.** Chỉ `text-right` thì chữ ô chỉ-đọc dừng ở 1007.5px
còn số trong `V2BaseCurrencyInput` dừng ở 995.5px (input có viền 1px + padding-right 10px riêng).
Thêm class `.amount-cell { padding-right: 20px }` cho 3 ô chỉ-đọc → 4 dòng thẳng một mốc.

**Hệ quả lên E2E (đáng nhớ):** căn radio đúng làm chấm tròn `::after` nằm CHỒNG lên ô
`input.custom-control-input` ẩn (`opacity:0; z-index:-1`) — đúng bố cục bootstrap gốc. Playwright
lập tức báo `<label>Có</label> intercepts pointer events` ở **mọi** `getByTestId('qN-yes').check()`.
Người dùng thật bấm chữ "Có" vẫn bình thường; chỉ script click thẳng vào input ẩn là hỏng. Đã thêm
helper `chooseRadio(page, testId)` bấm NHÃN (đúng thao tác thật) và thay 10 lời gọi `.check()`.

**Kiểm chứng**: bộ meeting **21/21 xanh**. Toàn suite 41 passed / 1 flaky / 2 failed — cả 2 lỗi
(`quotation-unit-select`, `internal-business-scope` ca "Xoá bản ghi vừa tạo") đã **stash code ra chạy
lại vẫn đỏ y hệt** → lỗi có sẵn, không do đợt này.

### Checkpoint — 2026-08-24 (wrap up, sau Đợt 4)
Vừa hoàn thành: 4 đợt tinh chỉnh UI (13 việc) sau nghiệm thu Phase 7; đợt cuối làm lại toàn bộ luồng In theo chuẩn Báo giá. E2E chạy lại sau mỗi đợt, lượt cuối **20/20 xanh**.
Đang làm dở: không có việc code nào đang dở.
Bước tiếp theo: user nghiệm thu bằng mắt phần chưa ai nhìn — file Excel thật mở bằng Excel, bản in thật khi bấm In trong modal xem trước (mở cửa sổ mới + hộp thoại in của trình duyệt), và bản in từ màn danh sách meeting (đường blade server).
Blocked: không có.

### Checkpoint — 2026-08-24 (wrap up, sau Đợt 5-6)
Vừa hoàn thành: Đợt 5 (icon xoá từng dòng bảng Mức đầu tư/Thời gian — xoá là bỏ chọn luôn nhóm ngành ở select; chỉ hỏi xác nhận khi dòng đã nhập tiền/ngày; xoá nhóm ngành cuối KHÔNG bỏ chọn lĩnh vực) + Đợt 6 (5 tinh chỉnh UI: STT căn giữa, cột tiền căn phải đồng nhất, radio căn đúng dòng câu hỏi, đánh số "Câu N.", nút thêm Phía Công ty đồng bộ Phía Khách hàng). Thêm E2E ca 18; bộ meeting **21/21 xanh**. Đã kiểm bằng mắt trên `hrm_tpe` thật (ảnh trong scratchpad phiên).
Đang làm dở: không có việc code nào đang dở.
Bước tiếp theo: (1) user quyết có sửa tận gốc rule CSS toàn cục `input:not(:placeholder-shown) + label` ở `assets/scss/custom-theme.scss` (thiếu tiền tố `.mate-field`, đang kéo mọi radio/checkbox toàn app lên nửa dòng) hay giữ cách hoá giải cục bộ trong `.q-item`; (2) phần chưa ai nhìn từ Đợt 4 vẫn còn nguyên — file Excel thật mở bằng Excel, bản in thật từ modal xem trước, bản in từ màn danh sách (đường blade server); (3) commit khi user yêu cầu (CLAUDE.md mục 384 — hiện toàn bộ Đợt 5-6 chưa commit).
Blocked: không có.

### Checkpoint — 2026-08-24 (đã push + nghiệm thu bằng mắt xong)
Vừa hoàn thành: user đã **push code lên `origin/tpe`** (cả `hrm-api` lẫn `hrm-client`, working tree sạch, đã xác minh `9078a6a4` và `9839d6d2` đều là ancestor của `origin/tpe`) và **nghiệm thu bằng mắt xong** phần còn treo — file Excel thật, bản in từ modal xem trước, bản in từ màn danh sách (đường blade server). Client commit gộp: `f81cbbfc9 meeting khao sat nhu cầu KH` → merge `58f8cf6d2`.
Đang làm dở: không có.
Bước tiếp theo: **feature coi như đóng**. Việc duy nhất còn nợ đã được user chốt HOÃN: sửa tận gốc rule CSS toàn cục `input:not(:placeholder-shown) + label` ở `assets/scss/custom-theme.scss` (thiếu tiền tố `.mate-field`) — hiện đang hoá giải cục bộ trong `.q-item`, chạy đúng, để dành làm sau vì blast radius toàn app.
Blocked: không có.
