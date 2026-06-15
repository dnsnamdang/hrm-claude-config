# Đồng bộ Phòng ban/Chức vụ kiêm nhiệm — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans để triển khai từng task. Steps dùng checkbox (`- [ ]`).
> **Lưu ý project:** KHÔNG commit/push git (theo CLAUDE.md). Verify bằng `php -l` + `php artisan migrate` + kịch bản thủ công. Module chưa có hạ tầng PHPUnit → dùng verify thủ công thay cho TDD tự động.

**Goal:** Khi duyệt quyết định bổ nhiệm có tick Kiêm nhiệm, thêm 1 dòng vào "Phòng ban/Chức vụ kiêm nhiệm" của hồ sơ nhân sự thay vì ghi đè vị trí chính.

**Architecture:** Thêm cột `is_concurrently` vào phụ lục hợp đồng (`appendix_labor_contracts`), copy cờ từ `DecisionAppointPersonnel` khi sinh phụ lục. Hàm sync `updateEmployeeInfo()` đọc cờ này: nếu kiêm nhiệm → `firstOrCreate` dòng kiêm nhiệm (chống trùng) + ghi history; nếu không → giữ nguyên ghi đè cũ.

**Tech Stack:** PHP 7.4, Laravel 8, nwidart/laravel-modules, MySQL.

**Spec:** `.plans/appoint-concurrent-sync-employee/design.md`

---

## File Structure

- **Create:** `hrm-api/database/migrations/2026_06_11_000001_add_is_concurrently_to_appendix_labor_contracts_table.php` — thêm cột cờ kiêm nhiệm.
- **Modify:** `hrm-api/Modules/Decision/Services/AppendixLaborContract/AppendixLaborContractService.php`
  - `autogenousAppendixLaborContract()` (~dòng 766-880): copy `is_concurrently` vào `updateOrCreate`.
  - `updateEmployeeInfo()` (dòng 567-613): rẽ nhánh kiêm nhiệm + thêm private method `addConcurrentlyDepartmentPosition()`.
  - Thêm 2 `use`: `EmployeeConcurrentlyDepartmentPosition`, `Title`.

> Entity `AppendixLaborContract` dùng `$guarded = []` → KHÔNG cần sửa fillable.

---

## Task 1: Migration thêm cột `is_concurrently` — ✅ DONE (2026-06-11)

**Files:**
- Create: `hrm-api/database/migrations/2026_06_11_000001_add_is_concurrently_to_appendix_labor_contracts_table.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddIsConcurrentlyToAppendixLaborContractsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('appendix_labor_contracts', function (Blueprint $table) {
            $table->boolean('is_concurrently')->default(false)->after('decision_type')->comment('Phụ lục sinh từ bổ nhiệm kiêm nhiệm hay không');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('appendix_labor_contracts', function (Blueprint $table) {
            $table->dropColumn('is_concurrently');
        });
    }
}
```

- [ ] **Step 2: Lint cú pháp**

Run: `php -l hrm-api/database/migrations/2026_06_11_000001_add_is_concurrently_to_appendix_labor_contracts_table.php`
Expected: `No syntax errors detected`

- [ ] **Step 3: Chạy migration**

Run (trong thư mục `hrm-api`): `php artisan migrate`
Expected: `Migrating: 2026_06_11_000001_add_is_concurrently_to_appendix_labor_contracts_table` → `Migrated`

- [ ] **Step 4: Verify cột tồn tại**

Run (trong `hrm-api`): `php artisan tinker --execute="echo Schema::hasColumn('appendix_labor_contracts','is_concurrently') ? 'OK' : 'MISSING';"`
Expected: `OK`

---

## Task 2: Copy cờ `is_concurrently` khi sinh phụ lục — ✅ DONE (2026-06-11)

**Files:**
- Modify: `hrm-api/Modules/Decision/Services/AppendixLaborContract/AppendixLaborContractService.php` (trong `autogenousAppendixLaborContract()`, mảng dữ liệu `updateOrCreate`)

- [ ] **Step 1: Thêm dòng copy cờ vào mảng updateOrCreate**

Tìm dòng `'decision_type' => $decision->type,` (trong khối thứ 2 của `updateOrCreate`, ~dòng 772) và thêm ngay **sau** nó:

```php
                'decision_type' => $decision->type,
                'is_concurrently' => $relationDecision->is_concurrently ?? 0,
```

> Với quyết định điều chuyển / điều chỉnh lương / tăng thâm niên, `$relationDecision` không có thuộc tính này → `?? 0`.

- [ ] **Step 2: Lint cú pháp**

Run: `php -l hrm-api/Modules/Decision/Services/AppendixLaborContract/AppendixLaborContractService.php`
Expected: `No syntax errors detected`

---

## Task 3: Rẽ nhánh `updateEmployeeInfo()` cho kiêm nhiệm — ✅ DONE (2026-06-11)

**Files:**
- Modify: `hrm-api/Modules/Decision/Services/AppendixLaborContract/AppendixLaborContractService.php`

- [ ] **Step 1: Thêm 2 import**

Sau dòng `use Modules\Human\Entities\EmployeeInfoLog;` (dòng 21) thêm:

```php
use Modules\Human\Entities\EmployeeConcurrentlyDepartmentPosition;
use Modules\Human\Entities\Title;
```

- [ ] **Step 2: Thêm rẽ nhánh đầu hàm `updateEmployeeInfo()`**

Mở đầu thân hàm `updateEmployeeInfo(AppendixLaborContract $appendixLaborContract, $employeeInfo)` (ngay sau dấu `{` ở dòng 568), chèn:

```php
        // Bổ nhiệm kiêm nhiệm: KHÔNG đổi vị trí chính, chỉ thêm 1 dòng Phòng ban/Chức vụ kiêm nhiệm
        if ($appendixLaborContract->is_concurrently) {
            $this->addConcurrentlyDepartmentPosition($appendixLaborContract, $employeeInfo);

            return;
        }

```

> Phần còn lại của `updateEmployeeInfo()` (ghi đè vị trí chính + history "Thông tin cơ bản") **giữ nguyên** — chỉ chạy khi không kiêm nhiệm.

- [ ] **Step 3: Thêm private method `addConcurrentlyDepartmentPosition()`**

Thêm method mới ngay **sau** hàm `updateEmployeeInfo()` (sau dấu `}` đóng hàm, trước hàm `storeEmployeeSalaryHistory()`):

```php
    private function addConcurrentlyDepartmentPosition(AppendixLaborContract $appendixLaborContract, $employeeInfo)
    {
        $keys = [
            'employee_info_id' => $employeeInfo->id,
            'department_id' => $appendixLaborContract->new_department_id,
            'working_position_id' => $appendixLaborContract->new_working_position_id,
        ];

        // Chống trùng: đã có dòng cùng nhân viên + phòng ban + chức vụ thì bỏ qua (không ghi history lặp)
        if (EmployeeConcurrentlyDepartmentPosition::where($keys)->exists()) {
            return;
        }

        $title = Title::find($appendixLaborContract->new_title_id);

        $concurrently = EmployeeConcurrentlyDepartmentPosition::create($keys + [
            'title_id' => $appendixLaborContract->new_title_id,
            'title' => $title->name ?? null,
        ]);

        $employeeInfo->saveEmployeeChangeHistory(
            [],
            $concurrently->toArray(),
            $employeeInfo->id,
            'Thông tin nhân sự',
            'Phòng ban/ Chức vụ kiêm nhiệm',
            true,
            ['title_id', 'position_order_index']
        );
    }
```

- [ ] **Step 4: Lint cú pháp**

Run: `php -l hrm-api/Modules/Decision/Services/AppendixLaborContract/AppendixLaborContractService.php`
Expected: `No syntax errors detected`

---

## Task 4: Verify thủ công end-to-end — ⏳ CHỜ USER (browser)

- [ ] **Step 1: Kịch bản kiêm nhiệm (chính)**

1. Tạo quyết định bổ nhiệm cho 1 nhân viên, **tick "Kiêm nhiệm"**, chọn Phòng ban/Chức vụ/Chức danh mới, `effective_date` = hôm nay hoặc trước đó.
2. Duyệt quyết định (chuyển trạng thái Đã duyệt).
3. Mở màn Hồ sơ nhân sự của nhân viên đó → tab "Phòng ban/ Chức vụ kiêm nhiệm".

Expected:
- Có **1 dòng mới** đúng Phòng ban + Chức vụ + Chức danh của quyết định.
- Phòng ban/bộ phận **chính** của nhân viên **KHÔNG đổi**.
- Lịch sử thay đổi có entry section "Phòng ban/ Chức vụ kiêm nhiệm".

- [ ] **Step 2: Kịch bản chống trùng**

Duyệt lại (hoặc trigger sync lần 2) cùng quyết định kiêm nhiệm đó.
Expected: **Không** phát sinh dòng kiêm nhiệm thứ 2 trùng; không có history lặp.

- [ ] **Step 3: Kịch bản bổ nhiệm thường (regression)**

Tạo + duyệt 1 quyết định bổ nhiệm **KHÔNG** tick kiêm nhiệm, `effective_date` ≤ hôm nay.
Expected: Phòng ban/bộ phận **chính** của nhân viên đổi sang phòng ban quyết định **như cũ** (không phát sinh dòng kiêm nhiệm).

- [ ] **Step 4: Kiểm tra log lỗi nếu có sự cố**

Nếu có lỗi khi duyệt → đọc `hrm-api/storage/logs/laravel-2026-06-11.log`.

---

## Checkpoint — 2026-06-11
Vừa hoàn thành: Task 1-3 (code) — migration `is_concurrently` đã migrate, copy cờ trong `autogenousAppendixLaborContract`, rẽ nhánh `updateEmployeeInfo` + method `addConcurrentlyDepartmentPosition` (chống trùng + null-guard). Qua spec review ✅ + code quality review ✅ (đã vá: null-guard new_department_id/new_working_position_id, đổi `?? 0` → `?? false`). `php -l` sạch.
Đang làm dở: không có.
Bước tiếp theo: User verify trên browser theo Task 4 (kiêm nhiệm thêm dòng + giữ vị trí chính / chống trùng / regression bổ nhiệm thường).
Blocked: (không)

## Self-Review (đã rà)

- **Spec coverage:** QĐ#1 (giữ vị trí chính) → Task 3 Step 2 (return sớm). QĐ#2 (Phương án A) → Task 1 + Task 2. QĐ#3 (bỏ part) → mapping Task 3 không có part_id. QĐ#4 (chống trùng) → Task 3 Step 3 `exists()` guard. Mapping mục 5 spec → Task 3 Step 3. Ngoài scope (lương/hủy duyệt) → không tạo task. ✓
- **Placeholder scan:** Không có TBD/TODO; mọi step có code/command cụ thể. ✓
- **Type consistency:** `is_concurrently` dùng nhất quán; `EmployeeConcurrentlyDepartmentPosition` / `Title` import đúng namespace; `saveEmployeeChangeHistory` đúng 7 tham số. `$guarded=[]` nên `create()`/`updateOrCreate()` nhận mass-assign. ✓
