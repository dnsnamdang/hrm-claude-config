# Plan — Phiếu chi tiền (ERP → HRM)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng `superpowers:subagent-driven-development` (khuyến nghị) hoặc `superpowers:executing-plans` để thực thi từng task. Step dùng checkbox (`- [ ]`) để theo dõi.

- Người phụ trách: @khoipv
- Nhánh: `gop_db` (cả 2 repo — **KHÔNG tạo branch riêng**)
- Spec: `docs/superpowers/specs/gop-db/2026-08-19-finance-bill-payment-design.md` (ĐÃ DUYỆT 2026-08-19)
- Design tóm tắt: `.plans/gop-db/finance-bill-payment/design.md`

**Goal:** Port màn ERP "Phiếu chi tiền" (`admin/income-expenditure/bill_payments`, bảng `bill_payments`) sang HRM tại `Modules/Finance` + `pages/finance/bill-payments` — đủ 5 loại chi, 1 màn danh sách duy nhất, tạo/sửa/xóa nháp, gửi duyệt, duyệt **kèm ghi bút toán sổ cái**, hủy, in 2 liên, xuất Excel.

**Architecture:** BE bám nguyên bộ `BillIncome*` trong `Modules/Finance` (Entity + Service + FormRequest + Resource + Controller V1), quyền kiểm bằng trait `ChecksEmployeePermission` chứ không dùng middleware. Nghiệp vụ chia **2 nhánh**: nhánh A (loại 1/2/6/12, lập từ Đề nghị thanh toán, duyệt 1 cấp) và nhánh B (loại 4 Chi thu nhập nhân viên, lập trực tiếp, duyệt 2 cấp). Mỗi nhánh có **1 service ghi sổ cái riêng**, cả hai tách hàm **thuần** `buildEntries()` trả mảng dòng đã đủ cột — unit test được không cần DB, đây là cơ chế kiểm chứng chính. FE bám khuôn `pages/finance/bill-incomes/`.

**Tech Stack:** PHP 7.4 / Laravel 8 / MySQL (DB gộp `gop_db`, connection mặc định) · PHPUnit 9.5 · Nuxt 2 / Vue 2 / Bootstrap-Vue.

---

## Global Constraints

Mọi task đều phải tuân thủ, không nhắc lại trong từng task:

- Nhánh git phải là `gop_db` ở **CẢ** `hrm-api` và `hrm-client` — kiểm `git branch --show-current` trước khi sửa file; sai nhánh thì **DỪNG**, báo user.
- **KHÔNG git commit / push** — user tự commit. Plan này cố ý **không có step commit**; thay bằng step verify.
- **KHÔNG tạo nhánh mới.**
- KHÔNG đổi schema 3 bảng `bill_payments` / `bill_payment_details` / `bill_payment_detail_product_export_requests`, **KHÔNG migration**.
- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND`. Model `TpXxx` **được dùng** nếu chạy trên connection mặc định — cụ thể `App\Models\TpCustomer` (bảng `customers`) là luồng khách hàng duy nhất; **đừng** thay bằng `Modules\Timesheet\Entities\Customer` (id lệch).
- KHÔNG nới `$guarded` của `Modules/Finance/Entities/Accounting/AccountDetail.php` (entity **CHỈ ĐỌC**, `BillPaymentDebtService` phụ thuộc) — ghi sổ cái qua `AccountDetailEntry` đã có.
- KHÔNG sửa `registerMorphMap()` ngoài việc **THÊM 5 cặp** ở Task 2. Không đụng 11 cặp đã có.
- KHÔNG gắn middleware `checkPermission` cho route nào của màn này — gate trong Controller/Entity (spec §7.2).
- `ValidationException` **KHÔNG** được catch — để bay lên cho FE nhận 422 chuẩn Laravel.
- KHÔNG chạy `PermissionsTableSeeder` trên DB local (`run()` truncate bảng, và seeder đang có sẵn lỗi trùng id 1117/1118).
- Cờ quyền FE **fail-closed**: khởi tạo `false`, cấm gán literal `true`. Pattern bị chặn khi review: `can[A-Za-z]*\s*=\s*true`.
- **KHÔNG tự test bằng Playwright** — verify bằng `php -l` + phpunit + tinker (BE) và `vue-template-compiler` + `@babel/parser` (FE); user tự mở trình duyệt. Báo rõ phần chưa kiểm chứng.
- **Dữ liệu nghiệp vụ đã lưu: KHÔNG sửa.** Mọi bản ghi test tạo ra phải xóa sạch. Baseline đếm thật 2026-08-19: `bill_payments` **1.302** · `bill_payment_details` **3.307** · `bill_payment_detail_product_export_requests` **0**.
- Mọi text hiển thị tiếng Việt. Toast dùng đúng câu ERP ghi trong spec §12.
- Migration PHP (nếu có) phải có PHPDoc trên `up()`/`down()` — nhưng feature này **không có migration**.
- ⚠️ **Tên quan hệ trộn 2 kiểu — bẫy đã dính 1 lần, đọc kỹ:**
  - Entity **MỚI** của feature này (`BillPayment`, `BillPaymentDetail`) dùng **camelCase**: `details`, `billPaymentRequest`, `employeeCreate`, `approvedBy`, `accountingApprovedBy`, `accountHas`, `paymentDepartment`, `customer`, `supplier`, `employee`, `contractable`, `productExportRequests`.
  - Entity **CŨ** `BillPaymentRequest` (feature trước, **KHÔNG được sửa**) dùng **snake_case**: `details`, `currency`, `employee_create`, `employee_update`, `approved_by`.
  → Eager load xuyên 2 entity phải viết `billPaymentRequest.employee_create.info`, **KHÔNG** phải `billPaymentRequest.employeeCreate.info`. Sai tên là Eloquent ném `Call to undefined relationship` lúc chạy, `php -l` không bắt được.
- FE trước khi code phải đọc: `.claude/skills/erp-to-hrm-screen/SKILL.md`, `list-page`, `button-convention`, `modal-popup`, `form-validate`, `unsaved-changes`, `select-and-input-state`, `print-page`, `notification-convention`. Icon phải đối chiếu font local: `grep "^\.ri-xxx:before" hrm-client/assets/scss/custom/plugins/icons/_remixicon.scss`.

---

## Bảng tra id dùng trong mọi step verify

Nhiều step verify cần id nhân viên / phiếu cụ thể. **Chạy khối lệnh này MỘT LẦN ở đầu, ghi kết quả ra giấy**, rồi thay vào chỗ `<...>` của các task. Đừng đoán id.

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "
-- <id kế toán thanh toán>
SELECT e.id, ei.fullname, 'Kế toán thanh toán' quyen FROM employees e
  JOIN employee_infos ei ON ei.id = e.employee_info_id
  JOIN employee_has_roles ehr ON ehr.employee_id = e.id
  JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
  JOIN permissions p ON p.id = rhp.permission_id
 WHERE p.name = 'Kế toán thanh toán' LIMIT 3;
-- <id thủ quỹ>
SELECT e.id, ei.fullname, 'Thủ quỹ duyệt phiếu chi' quyen FROM employees e
  JOIN employee_infos ei ON ei.id = e.employee_info_id
  JOIN employee_has_roles ehr ON ehr.employee_id = e.id
  JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
  JOIN permissions p ON p.id = rhp.permission_id
 WHERE p.name = 'Thủ quỹ duyệt phiếu chi' LIMIT 3;
-- <id kế toán trưởng>
SELECT e.id, ei.fullname, 'Kế toán trưởng duyệt phiếu chi' quyen FROM employees e
  JOIN employee_infos ei ON ei.id = e.employee_info_id
  JOIN employee_has_roles ehr ON ehr.employee_id = e.id
  JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
  JOIN permissions p ON p.id = rhp.permission_id
 WHERE p.name = 'Kế toán trưởng duyệt phiếu chi' LIMIT 3;
-- <id nhân viên có quyền tổng cty> / <chỉ có quyền công ty> / <không quyền>
SELECT e.id, MAX(p.name = 'Xem tất cả phiếu chi của tổng công ty') tong_cty,
       MAX(p.name = 'Xem tất cả phiếu chi của công ty') cong_ty
  FROM employees e
  LEFT JOIN employee_has_roles ehr ON ehr.employee_id = e.id
  LEFT JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
  LEFT JOIN permissions p ON p.id = rhp.permission_id
 GROUP BY e.id HAVING tong_cty = 1 OR cong_ty = 1 LIMIT 5;
-- <id phòng ban có phiếu loại 4>
SELECT payment_department_id, COUNT(*) n FROM bill_payments
 WHERE type = 4 AND payment_department_id IS NOT NULL GROUP BY payment_department_id ORDER BY n DESC LIMIT 3;
-- <id phiếu status 1 / 2 / loại 4 status 5>
SELECT id, code, type, status FROM bill_payments WHERE status IN (1,2) OR (type = 4 AND status = 5);
"
```

⚠️ **Trạng thái 5 hiện có 0 dòng** và `status = 1` chỉ có **1 dòng** — các step cần phiếu ở 2 trạng thái đó phải **tự tạo phiếu test trong transaction rồi rollback**, không mượn dữ liệu thật.

⚠️ **Auth guard cache theo tiến trình**: mỗi danh tính chạy **1 lệnh tinker riêng**. Gộp nhiều `loginUsingId()` trong 1 process thì lần 2 trở đi vẫn dùng danh tính đầu — đừng kết luận nhầm là fail-open.

---

# Phase 1 — Nền tảng Backend: xem được danh sách + chi tiết

## Task 1: Entity `BillPayment` + 2 entity chi tiết

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/BillPayment/BillPayment.php`
- Create: `hrm-api/Modules/Finance/Entities/BillPayment/BillPaymentDetail.php`
- Create: `hrm-api/Modules/Finance/Entities/BillPayment/BillPaymentDetailProductExportRequest.php`

**Interfaces:**
- Consumes: `Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest` (đã có) · `Modules\Finance\Entities\Concerns\ChecksEmployeePermission` (đã có) · `Modules\Finance\Entities\Account\Account` · `Modules\Human\Entities\Employee`.
- Produces: class `Modules\Finance\Entities\BillPayment\BillPayment` — 5 hằng `STATUS_*`, hằng `STATUSES`, 4 hằng `PERMISSION_*`, hằng `TYPE_PAYMENT_EMPLOYEE = 4`; quan hệ `details()`, `billPaymentRequest()`, `employeeCreate()`, `approvedBy()`, `accountingApprovedBy()`, `accountHas()`, `paymentDepartment()`; static `generateCode(): string`. Task 2-23 dùng class này.

**Khuôn để copy:** `hrm-api/Modules/Finance/Entities/BillIncome/BillIncome.php` — copy nguyên cấu trúc docblock, `boot()`, `$fillable`, hằng số; đổi tên bảng/cột.

- [x] **Step 1: Kiểm tra branch cả 2 repo**

```bash
git -C D:/laragon/www/hrm/hrm-api branch --show-current
git -C D:/laragon/www/hrm/hrm-client branch --show-current
```
Kỳ vọng: cả 2 in `gop_db`. Khác → **DỪNG**, báo user.

- [x] **Step 2: Đếm baseline dữ liệu**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT (SELECT COUNT(*) FROM bill_payments) bp, (SELECT COUNT(*) FROM bill_payment_details) bpd, (SELECT COUNT(*) FROM account_details) ad, (SELECT COUNT(*) FROM account_detail_refs) adr;"
```
Kỳ vọng: `bp = 1302`, `bpd = 3307`. Lệch → dừng, báo user (có người ghi song song).

- [x] **Step 3: Viết `BillPayment.php`**

Yêu cầu bắt buộc trong file:

```php
class BillPayment extends Model
{
    use ChecksEmployeePermission;

    protected $table = 'bill_payments';

    const STATUS_CREATING = 1;                    // Đang tạo
    const STATUS_AWAITING_APPROVE = 2;            // Chờ chi tiền (chờ Thủ quỹ)
    const STATUS_APPROVED = 3;                    // Đã duyệt
    const STATUS_CANCEL = 4;                      // Hủy
    const STATUS_AWAITING_ACCOUNTING_APPROVE = 5; // Chờ KT trưởng duyệt (CHỈ nhánh B)

    /** Bộ màu đổi so với ERP (ERP để danger cho cả 1/2/4/5) — spec §5.2. */
    public const STATUSES = [
        ['id' => self::STATUS_CREATING, 'name' => 'Đang tạo', 'type' => 'secondary'],
        ['id' => self::STATUS_AWAITING_APPROVE, 'name' => 'Chờ chi tiền', 'type' => 'warning'],
        ['id' => self::STATUS_APPROVED, 'name' => 'Đã duyệt', 'type' => 'success'],
        ['id' => self::STATUS_CANCEL, 'name' => 'Hủy', 'type' => 'danger'],
        ['id' => self::STATUS_AWAITING_ACCOUNTING_APPROVE, 'name' => 'Chờ KT trưởng duyệt', 'type' => 'warning'],
    ];

    /** Loại chi lập trực tiếp, KHÔNG qua Đề nghị thanh toán (nhánh B). */
    const TYPE_PAYMENT_EMPLOYEE = 4;

    /** Loại chi lập từ Đề nghị thanh toán (nhánh A). */
    const TYPES_FROM_REQUEST = [1, 2, 6, 12];

    /** Tên giữ NGUYÊN VĂN ERP. Bản HRM guard `api` id 1503-1506 khai ở Task 2. */
    const PERMISSION_TREASURER = 'Thủ quỹ duyệt phiếu chi';
    const PERMISSION_CHIEF_ACCOUNTANT = 'Kế toán trưởng duyệt phiếu chi';
    const PERMISSION_VIEW_ALL_COMPANY = 'Xem tất cả phiếu chi của tổng công ty';
    const PERMISSION_VIEW_COMPANY = 'Xem tất cả phiếu chi của công ty';

    /** Quyền tạo/sửa/xóa — dùng LẠI quyền đã có (id 1152), không khai mới. */
    const PERMISSION_ACCOUNTANT = 'Kế toán thanh toán';
}
```

`$fillable` liệt kê đủ 24 cột của bảng (spec §4): `code`, `bill_payment_request_id`, `receiver`, `account_has`, `date_accounting`, `status`, `created_by`, `updated_by`, `company_id`, `department_id`, `part_id`, `approved_id`, `sum_payment_money_request_exchange`, `sum_payment_money_approve_exchange`, `type`, `type_payment`, `type_money_id`, `exchange_rate`, `reason`, `payment_department_id`, `accounting_approved_id`.

`boot()` copy nguyên pattern của `BillIncome::boot()` (`BillIncome.php:79-99`):

```php
protected static function boot()
{
    parent::boot();

    // 3 cột đơn vị tổ chức gán ở `creating` — KHÔNG bắt chước ERP gán ở `created` rồi save()
    // lần 2 (2 câu ghi, để lại bản ghi nửa vời nếu lần 2 lỗi). Gán ĐÈ vô điều kiện, KHÔNG dùng
    // `??`: 3 cột nằm trong $fillable, client gửi `0`/`""` thì `??` giữ nguyên và bản ghi lọt
    // khỏi mọi nhánh lọc theo cấp.
    static::creating(function (self $model) {
        $info = optional(auth()->user())->info;
        $model->company_id = optional($info)->company_id;
        $model->department_id = optional($info)->department_id;
        $model->part_id = optional($info)->part_id;
        $model->created_by = $model->created_by ?: auth()->id();
    });

    static::saving(function (self $model) {
        $model->updated_by = auth()->id() ?? $model->updated_by;
    });
}
```

**KHÔNG** khai accessor `getDateAccountingAttribute()` trả `d/m/Y` như ERP — giữ `Y-m-d`, format ở Resource (lý do: cột này ghi thẳng vào sổ cái).

`generateCode()` — bọc transaction + `lockForUpdate()`, copy pattern `BillIncomeRequest::generateCode()`:

```php
/**
 * Mã phiếu `<mã công ty>.PC<mm><yy>.<5 số>` — ví dụ `TP.PC0825.00001`.
 * ERP dùng autoGenerateCode() KHÔNG khoá; 2 cổng cùng sinh mã dễ trùng nên HRM khoá dòng.
 */
public static function generateCode(): string
{
    $companyCode = optional(optional(auth()->user())->info)->company->code ?? '';
    $prefix = $companyCode . '.PC' . now()->format('my') . '.';

    $max = (int) static::query()
        ->where('code', 'like', $prefix . '%')
        ->lockForUpdate()
        ->selectRaw('MAX(CAST(SUBSTRING(code, ?) AS UNSIGNED)) as max_num', [mb_strlen($prefix) + 1])
        ->value('max_num');

    for ($i = 1; $i <= 5; $i++) {
        $code = $prefix . str_pad($max + $i, 5, '0', STR_PAD_LEFT);
        if (!static::query()->where('code', $code)->exists()) {
            return $code;
        }
    }

    return $prefix . str_pad($max + 6, 5, '0', STR_PAD_LEFT);
}
```

⚠️ Bám **đúng bản production** `BillIncomeRequest::generateCode()` (:392-411). KHÔNG dùng `orderByDesc('code')` rồi `substr` — `code` là chuỗi nên `'...00009' > '...00010'`, sinh mã trùng ngay khi vượt 9 phiếu/tháng.

- [x] **Step 4: Viết `BillPaymentDetail.php`**

`$table = 'bill_payment_details'`. `$fillable` liệt kê **đúng** các cột có thật trong bảng (spec §4).

⚠️ **KHÔNG** khai 4 cột `payment_market_cost`, `payment_extra`, `cost_debt_id`, `type_payment_employee` — **không tồn tại trong DB**, ERP truyền vào nhưng bị `$fillable` lọc âm thầm.
⚠️ **KHÔNG** port `saveCommissionEmployee()` và 4 quan hệ `diff_employees()` / `commission_months()` / `commission_quarters()` / `commission_bonus_quarters()` — code chết, `where('type_payment_employee', N)` trên cột không tồn tại, gọi vào là nổ SQL.

Quan hệ cần có: `billPayment()`, `customer()` (→ `App\Models\TpCustomer`), `supplier()`, `employee()`, `contractable()` (`morphTo`), `account()` (→ `Account`, khoá `account_dept`), `productExportRequests()`.

- [x] **Step 5: Viết `BillPaymentDetailProductExportRequest.php`**

`$table = 'bill_payment_detail_product_export_requests'`, `$fillable = ['bill_payment_detail_id', 'product_export_request_id', 'allocated_value', 'allocated_value_exchange']`. Docblock ghi rõ: **0 dòng dữ liệu thật, port theo yêu cầu 1:1, không test chạy thật được**.

- [x] **Step 6: Verify — lint + đọc dữ liệu thật qua entity**

```bash
php -l Modules/Finance/Entities/BillPayment/BillPayment.php
php -l Modules/Finance/Entities/BillPayment/BillPaymentDetail.php
php -l Modules/Finance/Entities/BillPayment/BillPaymentDetailProductExportRequest.php
```
Kỳ vọng: `No syntax errors detected` cả 3.

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
\$b = BillPayment::with('details')->find(1);
echo BillPayment::count(), ' | ', \$b->code, ' | details=', \$b->details->count(), PHP_EOL;
"
```
Kỳ vọng: in `1302 | <mã phiếu> | details=<số>`. Nổ `Call to undefined relationship` → sai tên quan hệ, xem Global Constraints.

---

## Task 2: Quyền + morphMap

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm sau dòng khai id 1502)
- Modify: `hrm-api/Modules/Finance/Providers/FinanceServiceProvider.php:54-68` (thêm 5 cặp vào `Relation::morphMap`)
- Create: `hrm-api/Modules/Finance/Entities/Contract/ProductExport.php`
- Create: `hrm-api/Modules/Finance/Entities/Contract/DeliveryTripAccounting.php`
- Create: `hrm-api/Modules/Finance/Entities/Contract/OtherDeliveryTripAccounting.php`
- Create: `hrm-api/Modules/Finance/Entities/Contract/DeclareDebtBeginning.php`

**Interfaces:**
- Produces: 4 entity morph target + 5 khoá morphMap mới. Task 9 và 14 ghi các `*_type` này vào sổ cái.

- [x] **Step 1: Thêm 4 quyền vào seeder**

Chèn ngay **sau** dòng khai id 1502 (`Thủ quỹ duyệt phiếu thu`):

```php
        // Màn Phiếu chi tiền — 4 quyền ERP ĐÃ CÓ ở guard `web` (id 100207 / 100319 / 100220 /
        // 100221) nhưng app chạy guard `api` nên phải khai bản `api` riêng. Giữ NGUYÊN VĂN tên
        // của ERP để 2 cổng đối chiếu quyền không lệch và để trait ChecksEmployeePermission
        // (so theo `name`, không lọc guard) bắt được cả 13 role đang gán bản `web`.
        // Quyền TẠO/SỬA/XÓA dùng LẠI 'Kế toán thanh toán' (id 1152), KHÔNG khai mới.
        Permission::create(['id' => 1503, 'guard_name' => 'api', 'name' => 'Thủ quỹ duyệt phiếu chi', 'display_name' => 'Thủ quỹ duyệt phiếu chi', 'group' => 'Phiếu chi tiền', 'type' => 8, 'sort_order' => 1]);
        Permission::create(['id' => 1504, 'guard_name' => 'api', 'name' => 'Kế toán trưởng duyệt phiếu chi', 'display_name' => 'Kế toán trưởng duyệt phiếu chi', 'group' => 'Phiếu chi tiền', 'type' => 8, 'sort_order' => 2]);
        Permission::create(['id' => 1505, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu chi của tổng công ty', 'display_name' => 'Xem tất cả phiếu chi của tổng công ty', 'group' => 'Phiếu chi tiền', 'type' => 8, 'sort_order' => 3]);
        Permission::create(['id' => 1506, 'guard_name' => 'api', 'name' => 'Xem tất cả phiếu chi của công ty', 'display_name' => 'Xem tất cả phiếu chi của công ty', 'group' => 'Phiếu chi tiền', 'type' => 8, 'sort_order' => 4]);
```

- [x] **Step 2: Kiểm id 1503-1506 chưa bị dùng**

```bash
grep -n "'id' => 150[3-6]" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```
Kỳ vọng: đúng **4** dòng (4 dòng vừa thêm). Nhiều hơn → trùng id, đổi dải và báo user.

- [x] **Step 3: Chèn 4 quyền vào DB local bằng tay (KHÔNG chạy seeder)**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "
INSERT INTO permissions (id, name, display_name, guard_name, \`group\`, type, sort_order, created_at, updated_at) VALUES
 (1503,'Thủ quỹ duyệt phiếu chi','Thủ quỹ duyệt phiếu chi','api','Phiếu chi tiền',8,1,NOW(),NOW()),
 (1504,'Kế toán trưởng duyệt phiếu chi','Kế toán trưởng duyệt phiếu chi','api','Phiếu chi tiền',8,2,NOW(),NOW()),
 (1505,'Xem tất cả phiếu chi của tổng công ty','Xem tất cả phiếu chi của tổng công ty','api','Phiếu chi tiền',8,3,NOW(),NOW()),
 (1506,'Xem tất cả phiếu chi của công ty','Xem tất cả phiếu chi của công ty','api','Phiếu chi tiền',8,4,NOW(),NOW());"
```
Kỳ vọng: chạy xong không lỗi. Lỗi trùng khoá → id đã tồn tại, dừng và báo user.

- [x] **Step 4: Viết 4 entity morph target**

Mỗi file là entity mỏng, chỉ khai `$table` và `$fillable` rỗng (chỉ đọc), kèm docblock nói rõ nó là bảng của ERP. Ví dụ `ProductExport.php`:

```php
<?php

namespace Modules\Finance\Entities\Contract;

use Illuminate\Database\Eloquent\Model;

/**
 * Phiếu xuất hàng của ERP — chỉ dùng làm đích morph cho `account_details.billable_type`
 * ở nhánh phân bổ phiếu xuất hàng của phiếu chi (0 dòng dữ liệu thật).
 * CHỈ ĐỌC: không ghi qua entity này.
 */
class ProductExport extends Model
{
    protected $table = 'product_exports';
    protected $guarded = ['*'];
}
```

Tên bảng 3 entity còn lại — **SỐ ÍT**, đã verify trên DB thật: `delivery_trip_accounting` · `other_delivery_trip_accounting` · `declare_debt_beginning`. (Chỉ `product_exports` là số nhiều.)

- [x] **Step 5: Xác nhận 4 bảng tồn tại trước khi khai entity**

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SHOW TABLES LIKE 'product_exports'; SHOW TABLES LIKE 'delivery_trip_accounting'; SHOW TABLES LIKE 'other_delivery_trip_accounting'; SHOW TABLES LIKE 'declare_debt_beginning';"
```
Kỳ vọng: in đủ 4 tên bảng. Thiếu bảng nào → **DỪNG**, báo user (không tự tạo bảng).

- [x] **Step 6: Thêm 5 cặp vào morphMap**

Trong `FinanceServiceProvider::registerMorphMap()`, thêm vào **cuối** mảng (giữ nguyên 11 cặp đã có):

```php
            // Chứng từ phiếu chi — để `account_details.invoiceable_type` ghi đúng chuỗi class ERP,
            // nếu không cổng ERP đọc sổ cái sẽ không resolve được chứng từ (spec §6).
            'App\Model\IncomeExpenditure\BillPayment'      => BillPayment\BillPayment::class,
            // 4 đích `billable_type` của phiếu chi (spec §6.1).
            'App\Model\Warehouse\ProductExport'            => FinanceContract\ProductExport::class,
            'App\Model\Warehouse\DeliveryTripAccounting'  => FinanceContract\DeliveryTripAccounting::class,
            'App\Model\Warehouse\OtherDeliveryTripAccounting' => FinanceContract\OtherDeliveryTripAccounting::class,
            'App\Model\Accounting\DeclareDebtBeginning'    => FinanceContract\DeclareDebtBeginning::class,
```

⚠️ Đầu file provider phải có `use` cho namespace mới, cạnh alias `FinanceContract` đã có:

```php
use Modules\Finance\Entities\BillPayment;
```
(alias `FinanceContract` cho `Modules\Finance\Entities\Contract` đã tồn tại sẵn — 4 entity mới nằm cùng namespace đó nên không cần thêm.)

⚠️ 4 chuỗi namespace ERP bên trái phải **khớp chính xác** tên class thật của ERP. Xác minh bằng:

```bash
grep -rn "^namespace" /d/laragon/www/erp/app/Model/Warehouse/ProductExport.php /d/laragon/www/erp/app/Model/Accounting/DeclareDebtBeginning.php
grep -rn "class DeliveryTripAccounting\b\|class OtherDeliveryTripAccounting\b" /d/laragon/www/erp/app/ --include=*.php
```
Lệch → sửa lại chuỗi theo kết quả grep, **không** đoán.

- [x] **Step 7: Verify**

```bash
php -l Modules/Finance/Providers/FinanceServiceProvider.php
php -l Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
php artisan tinker --execute="
echo count(Illuminate\Database\Eloquent\Relations\Relation::morphMap()), PHP_EOL;
echo DB::table('permissions')->whereIn('id',[1503,1504,1505,1506])->count(), PHP_EOL;
"
```
Kỳ vọng: số cặp morphMap **tăng đúng 5** so với trước (đếm trước khi sửa để so), và in `4`.

---

## Task 3: `BillPaymentService` (lọc + phạm vi quyền) + `BillPaymentListResource` + `index`

**Files:**
- Modify: `hrm-api/Modules/Finance/Entities/BillPayment/BillPayment.php` (thêm `applyScope()` + `existsForRequest()`)
- Create: `hrm-api/Modules/Finance/Services/BillPaymentService.php`
- Create: `hrm-api/Modules/Finance/Transformers/BillPaymentResource/BillPaymentListResource.php`
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm group `/bill-payments` sau group `/bill-incomes`, khoảng dòng 258)

**Interfaces:**
- Consumes: `BillPayment` (Task 1).
- Produces: `BillPaymentService::searchByFilter(Request $request)` trả **paginator** (bám khuôn `BillIncomeService`, KHÔNG trả Builder) · `BillPayment::applyScope(Builder $q): Builder` · `BillPayment::existsForRequest(int $requestId, ?int $exceptBillId = null): bool` · endpoint `GET /api/v1/finance/bill-payments`. Task sau cần Builder thô thì gọi thẳng `BillPayment::applyScope()`.

**Khuôn để copy:** `Services/BillIncomeService.php` (213 dòng) và `Transformers/BillIncomeResource/BillIncomeListResource.php` (81 dòng).

- [x] **Step 1: Viết `applyScope()` trong entity `BillPayment`**

```php
/**
 * Phạm vi dữ liệu màn danh sách — port ERP `searchByFilter()` nhánh `_type = all`
 * (`BillPayment.php:216-227`), là nhánh rộng nhất trong 4 chế độ cũ. 3 chế độ còn lại của ERP
 * nay là bộ lọc trên màn (user chốt gộp 1 màn, spec §2 quyết định #2).
 *
 * Phiếu NHÁP (status 1) của người khác LUÔN bị ẩn ở mọi cấp quyền.
 * Người dùng luôn thấy phiếu mình đã duyệt (approved_id / accounting_approved_id).
 */
public static function applyScope(Builder $query): Builder
{
    $employeeId = auth()->id();

    if (!static::currentEmployeeIsSuperAdmin()
        && !static::currentEmployeeHasPermission(self::PERMISSION_VIEW_ALL_COMPANY)) {
        if (static::currentEmployeeHasPermission(self::PERMISSION_VIEW_COMPANY)) {
            $companyId = static::currentCompanyId();
            $query->where(function (Builder $q) use ($companyId, $employeeId) {
                $companyId === null ? $q->whereNull('company_id') : $q->where('company_id', $companyId);
                $q->orWhere('created_by', $employeeId)
                  ->orWhere('approved_id', $employeeId)
                  ->orWhere('accounting_approved_id', $employeeId);
            });
        } else {
            $query->where(function (Builder $q) use ($employeeId) {
                $q->where('created_by', $employeeId)
                  ->orWhere('approved_id', $employeeId)
                  ->orWhere('accounting_approved_id', $employeeId);
            });
        }
    }

    // Nháp của người khác luôn ẩn — đúng ERP :222-226.
    return $query->where(function (Builder $q) use ($employeeId) {
        $q->where('status', '!=', self::STATUS_CREATING)
          ->orWhere(function (Builder $q1) use ($employeeId) {
              $q1->where('status', self::STATUS_CREATING)->where('created_by', $employeeId);
          });
    });
}
```

- [x] **Step 2: Viết `BillPaymentService::searchByFilter()`**

Nhận đủ 12 khoá lọc, port từ ERP `searchByFilter()` :253-320:

`code` (like) · `code_bill_payment_request` (whereHas) · `type` · `created_by` · `created_by_request` (whereHas) · `status` · `department` · `object_id` (whereHas details: `customer_id` HOẶC `supplier_id`) · `money_from` / `money_to` (trên `sum_payment_money_approve_exchange`, bỏ dấu `,`) · `start_date` / `end_date` (trên `created_at`).

⚠️ ERP viết `->where('customer_id', ...)->whereOr('supplier_id', ...)` — `whereOr` **không phải** method của Laravel query builder, đây là **lỗi ERP**. HRM viết đúng:

```php
$query->whereHas('details', function (Builder $q) use ($objectId) {
    $q->where('customer_id', $objectId)->orWhere('supplier_id', $objectId);
});
```

Eager load: `['billPaymentRequest.employee_create.info', 'details', 'employeeCreate.info', 'paymentDepartment']`.

⚠️ **KHÔNG** eager load `billPaymentRequest.department` — entity `BillPaymentRequest` của feature trước **không khai quan hệ `department()`** (đã verify: chỉ có `details`, `currency`, `employee_create`, `employee_update`, 4 quan hệ approver) và **bị cấm sửa**. Dùng sẽ nổ `Call to undefined relationship` lúc chạy. Tra tên phòng ban theo lô bằng 1 query `DB::table('departments')`.

⚠️ **Ô lọc "Phòng ban" lệch ERP CÓ CHỦ Ý.** ERP lọc `bill_payments.department_id` (`searchByFilter()` :266-268) — đó là phòng ban của **kế toán lập phiếu** — trong khi cột hiển thị lại lấy phòng ban của **phiếu đề nghị** (nhánh A) hoặc `payment_department` (loại 4). Tức bộ lọc ERP không khớp chính cột nó đứng cạnh. HRM lọc theo **đúng cột đang hiện** (`payment_department_id` OR `billPaymentRequest.department_id`).

Sắp xếp mặc định `created_at DESC`. Cho phép sort: `code` · `sum_payment_money_approve_exchange` · `created_at` · `updated_at` · `status`.

- [x] **Step 3: Viết `BillPaymentListResource`**

Trả 14 field khớp cột màn danh sách (spec §11.1): `id` · `code` · `bill_payment_request_id` · `bill_payment_request_code` · `type` · `type_text` · `object_name` · `sum_payment_money_approve_exchange` · `created_by_request_name` · `department_name` · `created_at` (`d/m/Y H:i`) · `created_by_name` · `updated_at` (`d/m/Y H:i`) · `updated_by_name` · `status` · `status_text` · `status_type` + 7 cờ `is_can_*` (Task 4 điền, tạm trả `false` hết ở task này).

`object_name` port từ ERP `searchData()` :70-81, **mở rộng cho loại 12 và 4**:

```php
/**
 * Cột "Khách hàng / Nhà cung cấp" — nội dung đổi theo loại chi.
 * Tiêu đề cột đổi so với ERP ("Khách hàng") vì bảng `customers` chứa CẢ KH lẫn NCC
 * (`is_customer` / `is_supplier`) — spec §11.1.
 */
private function objectName(): ?string
{
    $detail = $this->details->first();
    if (!$detail) {
        return null;
    }

    $type = $this->billPaymentRequest->type ?? $this->type;

    if (in_array($type, [2, 6], true)) {
        return trim($detail->customer_code . '-' . $detail->customer_name, '-') ?: null;
    }
    if (in_array($type, [1, 12], true)) {
        return trim($detail->supplier_code . '-' . $detail->supplier_name, '-') ?: null;
    }

    return null; // loại 4 để trống (đối tượng là nhiều nhân viên)
}
```

- [x] **Step 4: Viết `BillPaymentController::index()` + route**

Controller kế thừa `ApiController` như `BillIncomeController`. Docblock đầu class phải ghi rõ **vì sao không dùng middleware `checkPermission`** (spec §7.2).

Route thêm vào `Routes/api.php`, ngay sau group `/bill-incomes`:

```php
    // Phiếu chi tiền (bảng ERP `bill_payments` trên DB gộp).
    // KHÔNG gắn middleware quyền — xem docblock BillPaymentController.
    Route::group(['prefix' => '/bill-payments'], function () {
        Route::get('/', [BillPaymentController::class, 'index']);
        // Route TĨNH phải khai TRƯỚC /{id} để không bị route động nuốt.
        Route::get('/accounts', [BillPaymentController::class, 'accounts']);
        Route::get('/search-payment-requests', [BillPaymentController::class, 'searchPaymentRequests']);
        Route::get('/payment-employees', [BillPaymentController::class, 'paymentEmployees']);
        Route::get('/{id}', [BillPaymentController::class, 'show']);
        Route::get('/{id}/print-data', [BillPaymentController::class, 'printData']);
        Route::get('/{id}/export', [BillPaymentController::class, 'export']);
        Route::post('/', [BillPaymentController::class, 'store']);
        Route::put('/{id}', [BillPaymentController::class, 'update']);
        Route::delete('/{id}', [BillPaymentController::class, 'destroy']);
        Route::post('/{id}/submit', [BillPaymentController::class, 'submit']);
        Route::post('/{id}/approve', [BillPaymentController::class, 'approve']);
        Route::post('/{id}/cancel', [BillPaymentController::class, 'cancel']);
    });
```

Ở task này chỉ implement `index()`; các action còn lại khai method rỗng ném `abort(501)` để route đăng ký được, Task sau điền dần.

- [x] **Step 5: Verify — lint + gọi thật**

```bash
php -l Modules/Finance/Services/BillPaymentService.php
php -l Modules/Finance/Transformers/BillPaymentResource/BillPaymentListResource.php
php -l Modules/Finance/Http/Controllers/V1/BillPaymentController.php
php artisan route:list --path=bill-payments
```
Kỳ vọng: 13 route hiện ra, `php -l` sạch.

- [x] **Step 6: Verify phạm vi quyền bằng dữ liệu thật**

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
use Modules\Human\Entities\Employee;
foreach ([<id nhân viên có quyền tổng cty>, <id chỉ có quyền công ty>, <id không quyền>] as \$id) {
    auth()->loginUsingId(\$id);
    echo \$id, ' => ', BillPayment::applyScope(BillPayment::query())->count(), PHP_EOL;
}
"
```

⚠️ **Bẫy đã dính**: auth guard cache theo tiến trình — chạy nhiều danh tính trong **1** process thì lần 2 trở đi vẫn dùng danh tính đầu. Phải chạy **mỗi id 1 lệnh tinker riêng**, đừng gộp vòng lặp rồi kết luận là fail-open.

Kỳ vọng: người có quyền tổng công ty ≥ người chỉ có quyền công ty ≥ người không quyền; không ai thấy phiếu nháp của người khác.

---

## Task 4: Gate quyền (`BillPaymentAccess`) + `BillPaymentDetailResource` + `show`

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/BillPayment/BillPaymentAccess.php` (trait)
- Modify: `hrm-api/Modules/Finance/Entities/BillPayment/BillPayment.php` (dùng trait)
- Create: `hrm-api/Modules/Finance/Transformers/BillPaymentResource/BillPaymentDetailResource.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`show()`)
- Modify: `hrm-api/Modules/Finance/Transformers/BillPaymentResource/BillPaymentListResource.php` (nối 7 cờ thật)

**Interfaces:**
- Produces: 7 method `canView()` · `canEdit()` · `canDelete()` · `canSubmit()` · `canApprove()` · `canCancel()` · `canExport()` trên `BillPayment`. **Màn danh sách và màn chi tiết đọc CÙNG bộ cờ này** — bẫy đã dính ở feature trước (2 màn lệch số nút).

- [x] **Step 1: Viết trait `BillPaymentAccess`**

```php
/** Người lập phiếu, đang ở trạng thái nháp, và có quyền kế toán thanh toán. */
public function canEdit(): bool
{
    return $this->status === self::STATUS_CREATING
        && $this->created_by === auth()->id()
        && static::currentEmployeeHasPermission(self::PERMISSION_ACCOUNTANT);
}

public function canDelete(): bool
{
    return $this->canEdit();
}

public function canSubmit(): bool
{
    return $this->canEdit();
}

/**
 * Duyệt — tự nhận biết cấp theo trạng thái hiện tại.
 * status 5 (chỉ nhánh B) → Kế toán trưởng · status 2 → Thủ quỹ.
 */
public function canApprove(): bool
{
    if (!$this->isSameCompanyAsCurrentEmployee()) {
        return false;
    }
    if ($this->status === self::STATUS_AWAITING_ACCOUNTING_APPROVE) {
        return static::currentEmployeeHasPermission(self::PERMISSION_CHIEF_ACCOUNTANT);
    }
    if ($this->status === self::STATUS_AWAITING_APPROVE) {
        return static::currentEmployeeHasPermission(self::PERMISSION_TREASURER);
    }

    return false;
}

public function canCancel(): bool
{
    return $this->canApprove();
}
```

`canView()` port ERP `canView()` :760-796 (đã có docblock sẵn bên ERP, logic khớp `applyScope`).

`isSameCompanyAsCurrentEmployee()` — dùng `static::currentCompanyId()` của trait; **hai vế cùng `null` KHÔNG coi là cùng công ty** (trait đã ghi rõ lý do).

- [x] **Step 2: Viết `BillPaymentDetailResource`**

Ngoài field đầu phiếu, trả `details` (mảng dòng chi tiết đủ cột theo nhánh), `bill_payment_request` (tóm tắt phiếu đề nghị nguồn), và 7 cờ `is_can_*` lấy thẳng từ 7 method Task này. Ngày trả sẵn `d/m/Y` / `d/m/Y H:i`, tiền trả số thô (FE format).

- [x] **Step 3: Nối 7 cờ thật vào `BillPaymentListResource`**

Thay 7 giá trị `false` tạm ở Task 3 bằng `$this->canEdit()`, … — **đúng cùng 7 method**, không viết lại điều kiện.

- [x] **Step 4: Viết `show()`**

```php
public function show($id)
{
    $bill = BillPayment::with([...])->findOrFail($id);
    if (!$bill->canView()) {
        abort(403, 'Bạn không có quyền xem phiếu chi này.');
    }

    return $this->responseSuccess(new BillPaymentDetailResource($bill));
}
```

- [x] **Step 5: Verify — 7 cờ khớp giữa 2 màn**

```bash
php -l Modules/Finance/Entities/BillPayment/BillPaymentAccess.php
php -l Modules/Finance/Transformers/BillPaymentResource/BillPaymentDetailResource.php
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
auth()->loginUsingId(<id nhân viên có quyền Thủ quỹ>);
\$b = BillPayment::where('status', 2)->first();
echo json_encode(['edit'=>\$b->canEdit(),'delete'=>\$b->canDelete(),'submit'=>\$b->canSubmit(),'approve'=>\$b->canApprove(),'cancel'=>\$b->canCancel()]), PHP_EOL;
"
```
Kỳ vọng: `approve` và `cancel` = true, `edit`/`delete`/`submit` = false (phiếu đã gửi duyệt).

- [x] **Step 6: Verify không có cờ nào hard-code true**

```bash
grep -rnE "is_can_[a-z_]*'\s*=>\s*true" Modules/Finance/Transformers/BillPaymentResource/
```
Kỳ vọng: **0 kết quả**.

---

# Phase 2 — Tạo / sửa / xóa nháp + gửi duyệt (nhánh A)

## Task 5: Popup chọn Phiếu đề nghị chi + endpoint `accounts`

**Files:**
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`searchPaymentRequests()`, `accounts()`)
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentService.php` (thêm `searchAvailableRequests()`)

**Interfaces:**
- Consumes: `BillPaymentRequest` (entity feature trước, **KHÔNG sửa**) — quan hệ snake_case.
- Produces: `GET /v1/finance/bill-payments/search-payment-requests` và `/accounts`. Task 19 (FE) dùng.

- [x] **Step 1: Viết `searchAvailableRequests()`**

Lọc **cứng** `status = BillPaymentRequest::STATUS_AWAITING_CREATE_BILL_PAYMENT` (= 6) — đúng ERP (`formJs.blade.php`: `d.status = 6`).

Loại bỏ phiếu **đã có phiếu chi** trỏ tới:

```php
$query->whereNotExists(function ($q) {
    $q->selectRaw('1')
      ->from('bill_payments')
      ->whereColumn('bill_payments.bill_payment_request_id', 'bill_payment_requests.id');
});
```
(bản SQL của cùng luật `existsForRequest()` — dùng ở tầng danh sách nên phải là subquery, không gọi được helper PHP theo từng dòng.)

⚠️ **KHÔNG lọc trạng thái phiếu chi** — đúng ERP: hủy phiếu chi là **ngõ cụt**, không lập lại được (spec §5.5 điểm hở #2, user chốt giữ nguyên).

⚠️ Luật "1 đề nghị chỉ 1 phiếu chi" xuất hiện ở **3 nơi** (task này · Task 6 `guardOneBillPerRequest()` · Task 23 cờ `is_can_create_bill_payment`). Viết lại 3 lần là chắc chắn lệch nhau. Khai **1 helper duy nhất** trên entity ở Task 3 và dùng chung cả 3 chỗ:

```php
/** Đề nghị $requestId đã có phiếu chi chưa. KHÔNG lọc trạng thái — xem spec §5.5 điểm hở #2. */
public static function existsForRequest(int $requestId, ?int $exceptBillId = null): bool
{
    return static::query()
        ->where('bill_payment_request_id', $requestId)
        ->when($exceptBillId, function ($q) use ($exceptBillId) { return $q->where('id', '!=', $exceptBillId); })
        ->exists();
}
```

Cho lọc theo `code`, `type`, khoảng ngày; phân trang 10.

- [x] **Step 2: Viết `accounts()`**

Trả danh sách tài khoản cho 2 ô `Tài khoản có` / `Tài khoản nợ`. Copy nguyên `BillIncomeController::accounts()`.

- [x] **Step 3: Verify**

```bash
php artisan tinker --execute="
use Modules\Finance\Services\BillPaymentService;
auth()->loginUsingId(<id kế toán thanh toán>);
echo app(BillPaymentService::class)->searchAvailableRequests([])->count(), PHP_EOL;
"
mysql -h127.0.0.1 -uroot gop_db -e "
SELECT COUNT(*) ky_vong FROM bill_payment_requests r
WHERE r.status = 6 AND NOT EXISTS (SELECT 1 FROM bill_payments b WHERE b.bill_payment_request_id = r.id);"
```
Kỳ vọng: 2 số **bằng nhau**.

---

## Task 6: `BillPaymentWriteService` — tạo / sửa nháp (nhánh A)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentWriteService.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/BillPayment/BillPaymentStoreRequest.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/BillPayment/BillPaymentUpdateRequest.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`store()`, `update()`)

**Interfaces:**
- Produces: `BillPaymentWriteService::store(array $data): BillPayment` · `update(BillPayment $bill, array $data): BillPayment` · **`public function syncDetails(BillPayment $bill, array $details): void`**.
  ⚠️ `syncDetails()` bắt buộc **public** — Task 10 gọi nó từ `BillPaymentApprovalFlowService` (service khác).
  `guardOneBillPerRequest()` là **private**, KHÔNG phải interface công khai.

**Khuôn để copy:** `Services/BillIncomeWriteService.php` (239 dòng).

- [x] **Step 1: Viết `BillPaymentStoreRequest`**

Luật theo spec §9.1 / §9.2, **rẽ nhánh theo `type`**:

```php
public function rules(): array
{
    $rules = [
        'type'        => 'required|integer',
        'account_has' => 'required|exists:accounts,id',
        'receiver'    => 'required|string|max:255',
        'details'     => 'required|array|min:1',
        'details.*.account_dept' => 'required|exists:accounts,id',
    ];

    if (in_array((int) $this->input('type'), BillPayment::TYPES_FROM_REQUEST, true)) {
        $rules['bill_payment_request_id'] = 'required|exists:bill_payment_requests,id';
        $rules['details.*.payment_money_approve'] = 'nullable|numeric|min:0';
        $rules['details.*.product_export_requests.*.allocated_value'] = 'required|numeric|min:0';
    }

    if ((int) $this->input('type') === BillPayment::TYPE_PAYMENT_EMPLOYEE) {
        $rules['payment_department_id'] = 'required|exists:departments,id';
        $rules['type_payment']  = 'required';
        $rules['type_money_id'] = 'required';
        $rules['exchange_rate'] = 'required|numeric';
        $rules['reason']        = 'required|string';
        foreach (['payment_diff_employee', 'payment_commission_month', 'payment_commission_quarter',
                  'payment_commission_bonus_quarter', 'payment_delivery_money', 'payment_other_cost'] as $col) {
            $rules['details.*.' . $col] = 'required|numeric';
        }
    }

    return $rules;
}
```

`messages()` tiếng Việt cho từng khoá.

⚠️ **KHÔNG** khai luật `note` — bảng không có cột `note`, lý do hủy xử lý riêng ở Task 11.

- [x] **Step 2: Viết `BillPaymentUpdateRequest`**

Kế thừa luật của Store. ⚠️ **Đây là chỗ sửa lỗi ERP #2**: ERP khai `BillPaymentUpdateRequest` nhưng `update()` lại nhận `BillPaymentStoreRequest` nên luật update **chưa bao giờ chạy**. Controller HRM phải type-hint **đúng** `BillPaymentUpdateRequest`.

- [x] **Step 3: Viết `guardOneBillPerRequest()`**

```php
/**
 * 1 Đề nghị thanh toán chỉ được có 1 Phiếu chi. KHÔNG lọc theo trạng thái phiếu chi — đúng
 * ERP: hủy phiếu chi là ngõ cụt, đề nghị không lập lại phiếu khác được (spec §5.5 điểm hở #2,
 * user chốt GIỮ NGUYÊN, không phải bug cần sửa).
 */
private function guardOneBillPerRequest(int $requestId, ?int $exceptBillId = null): void
{
    if (BillPayment::existsForRequest($requestId, $exceptBillId)) {
        abort(422, 'Đề nghị thanh toán đã lập phiếu chi tiền.');
    }
}
```

- [x] **Step 4: Viết `syncDetails()`**

Port ERP `syncDetails()` :373-446 — xóa hết dòng cũ (kèm bảng phân bổ) rồi tạo lại, cộng dồn 2 cột tổng vào phiếu.

⚠️ **KHÔNG** truyền 4 cột `payment_market_cost`, `payment_extra`, `cost_debt_id`, `type_payment_employee` — không tồn tại trong DB (spec §4).

- [x] **Step 5: Viết `store()` + `update()`**

`store()`: bọc `DB::transaction`, sinh mã bằng `BillPayment::generateCode()`, `guardOneBillPerRequest()` (chỉ nhánh A), tạo phiếu ở `STATUS_CREATING`, `syncDetails()`.

⚠️ **Khác ERP có chủ ý**: ERP `store()` còn nhận `status` trong payload để vừa tạo vừa gửi duyệt. HRM **luôn tạo ở trạng thái nháp**; gửi duyệt là endpoint riêng (Task 8). FE bấm "Lưu và gửi duyệt" thì gọi 2 API tuần tự.

`update()`: gate `canEdit()`, trả **423** nếu không:

```php
if (!$bill->canEdit()) {
    abort(423, 'Phiếu chi đã bị khóa, không sửa được.');
}
```

- [x] **Step 6: Verify — tạo thật rồi xóa sạch**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id kế toán thanh toán>);
\$svc = app(Modules\Finance\Services\BillPaymentWriteService::class);
\$bill = \$svc->store([...payload nhánh A tối thiểu...]);
echo \$bill->code, ' | details=', \$bill->details()->count(), ' | status=', \$bill->status, PHP_EOL;
DB::rollBack();
echo 'rolled back', PHP_EOL;
"
```
Kỳ vọng: in mã đúng dạng `<cty>.PC<mmyy>.00001`, `status=1`, rồi rollback.

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT COUNT(*) FROM bill_payments;"
```
Kỳ vọng: **1302** — đúng baseline, không sót bản ghi test.

---

## Task 7: Xóa nháp (`destroy`)

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentWriteService.php` (`destroy()`)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`destroy()`)

**Interfaces:**
- Produces: `BillPaymentWriteService::destroy(BillPayment $bill): void` · `DELETE /v1/finance/bill-payments/{id}`.

- [x] **Step 1: Viết `destroy()`**

```php
/**
 * Sửa LỖI ERP #1: `BillPaymentController::delete()` không kiểm quyền lẫn trạng thái —
 * gọi thẳng URL là xóa được phiếu đã duyệt của người khác.
 */
public function destroy(BillPayment $bill): void
{
    if (!$bill->canDelete()) {
        abort(423, 'Phiếu chi đã bị khóa, không xóa được.');
    }

    DB::transaction(function () use ($bill) {
        $detailIds = $bill->details()->pluck('id');
        BillPaymentDetailProductExportRequest::whereIn('bill_payment_detail_id', $detailIds)->delete();
        $bill->details()->delete();
        $bill->delete();
    });
}
```

⚠️ **KHÔNG** trả trạng thái phiếu đề nghị về — đúng ERP, an toàn vì nháp chưa hề đụng phiếu đề nghị (spec §5.5 điểm hở #1).

- [x] **Step 2: Verify — thử xóa phiếu đã duyệt phải bị chặn**

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
auth()->loginUsingId(<id kế toán thanh toán>);
\$b = BillPayment::where('status', 3)->first();
try { app(Modules\Finance\Services\BillPaymentWriteService::class)->destroy(\$b); echo 'FAIL - xóa được!', PHP_EOL; }
catch (\Throwable \$e) { echo 'OK ', \$e->getStatusCode(), PHP_EOL; }
"
```
Kỳ vọng: in `OK 423`. In `FAIL` → gate hỏng, dừng lại sửa.

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT COUNT(*) FROM bill_payments;"
```
Kỳ vọng: **1302**.

---

## Task 8: Gửi duyệt (`submit`) + đồng bộ ngược + chuông

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentNotifyService.php`
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentWriteService.php` (`submit()`)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`submit()`)

**Interfaces:**
- Consumes: `ChecksEmployeePermission::employeeInfoIdsHavingPermission(string, ?int): int[]` (đã có trong trait).
- Produces: `BillPaymentWriteService::submit(BillPayment $bill): BillPayment` · `BillPaymentNotifyService::notifySubmitted(BillPayment $bill): void`.

**Khuôn để copy:** `Services/BillPaymentRequestNotifyService.php` (feature trước, cùng phân hệ).

- [x] **Step 1: Viết `submit()` — rẽ 2 nhánh**

```php
/**
 * Gửi duyệt. Nhánh A (loại 1/2/6/12) -> Chờ chi tiền (2), báo Thủ quỹ.
 * Nhánh B (loại 4)                   -> Chờ KT trưởng duyệt (5), báo Kế toán trưởng.
 *
 * ⚠️ KHÔNG gán `accounting_approved_id` ở đây. ERP gán = người ĐANG ĐĂNG NHẬP lúc gửi duyệt,
 * tức người LẬP phiếu chứ không phải người duyệt (`BillPaymentController::store()` :175-180 và
 * `update()` :233-236) — lỗi ERP #8, HRM ghi ở đúng bước KT trưởng bấm duyệt (Task 15).
 */
public function submit(BillPayment $bill): BillPayment
{
    if (!$bill->canSubmit()) {
        abort(423, 'Phiếu chi đã bị khóa, không gửi duyệt được.');
    }

    return DB::transaction(function () use ($bill) {
        $isPaymentEmployee = (int) $bill->type === BillPayment::TYPE_PAYMENT_EMPLOYEE;

        $bill->status = $isPaymentEmployee
            ? BillPayment::STATUS_AWAITING_ACCOUNTING_APPROVE
            : BillPayment::STATUS_AWAITING_APPROVE;
        $bill->save();

        if (!$isPaymentEmployee) {
            // Đồng bộ ngược: đề nghị -> 7 "Chờ duyệt phiếu chi" (spec §5.5).
            BillPaymentRequest::query()
                ->where('id', $bill->bill_payment_request_id)
                ->update(['status' => BillPaymentRequest::STATUS_AWAITING_APPROVE_BILL_PAYMENT]);
        }

        $this->notifyService->notifySubmitted($bill);

        return $bill;
    });
}
```

- [x] **Step 2: Viết `BillPaymentNotifyService::notifySubmitted()`**

Người nhận = `BillPayment::employeeInfoIdsHavingPermission($permission, $bill->company_id)`.

⚠️ Chọn `$permission` theo **TRẠNG THÁI HIỆN TẠI của phiếu**, không theo `type` — vì Task 15 gọi lại
chính hàm này ở bước 2 nhánh B (lúc đó `type` vẫn là 4 nhưng người cần báo đã là **Thủ quỹ**):

```php
$permission = $bill->status === BillPayment::STATUS_AWAITING_ACCOUNTING_APPROVE
    ? BillPayment::PERMISSION_CHIEF_ACCOUNTANT   // status 5 -> KT trưởng
    : BillPayment::PERMISSION_TREASURER;         // status 2 -> Thủ quỹ (cả nhánh A lẫn bước 2 nhánh B)
```

Chọn theo `type` là bug: phiếu loại 4 sau khi KT trưởng duyệt sẽ báo nhầm lại cho chính KT trưởng, Thủ quỹ không bao giờ nhận được thông báo.

Nội dung theo `notification-convention`: `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`, tên phiếu ≤ 50 ký tự và **in đậm**, tổng ≤ 120 ký tự, deep-link `/finance/bill-payments/<id>`.

- [x] **Step 3: Verify — luồng gửi duyệt, rollback sau khi kiểm**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id kế toán thanh toán>);
use Modules\Finance\Entities\BillPayment\BillPayment;
use Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest;
\$bill = BillPayment::where('status', 1)->first();
\$reqId = \$bill->bill_payment_request_id;
app(Modules\Finance\Services\BillPaymentWriteService::class)->submit(\$bill);
echo 'bill=', \$bill->fresh()->status, ' request=', BillPaymentRequest::find(\$reqId)->status, PHP_EOL;
DB::rollBack();
"
```
Kỳ vọng: in `bill=2 request=7`.

- [x] **Step 4: Verify `accounting_approved_id` KHÔNG bị gán khi gửi duyệt**

Trong cùng lệnh trên, in thêm `\$bill->fresh()->accounting_approved_id`. Kỳ vọng: `null`.

---

# Phase 3 — Duyệt + ghi sổ cái (nhánh A)

## Task 9: `BillPaymentAccountingService::buildEntries()` + unit test

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentAccountingService.php`
- Create: `hrm-api/Modules/Finance/Tests/Unit/BillPaymentAccountingServiceTest.php`

**Interfaces:**
- Consumes: `AccountDetailEntry` · `AccountDetailRef` (đã có).
- Produces: `BillPaymentAccountingService::buildEntries(array $input): array{entries: array, refs: array}` (**hàm thuần**, không DB không auth) · **`public function persist(array $built): void`** — chỉ insert, mọi dữ liệu cần thiết đã nằm trong `$built`. Task 10 gọi.

**Khuôn để copy:** `Services/BillIncomeAccountingService.php` (253 dòng) — copy nguyên cấu trúc `buildEntries()` / `creditEntry()` / `debitEntry()` / `persist()`, đảo chiều Nợ ↔ Có và đổi 4 nhánh theo loại chi.

- [x] **Step 1: Viết test TRƯỚC — nhánh loại 1 (chi trả NCC)**

```php
public function test_loai_1_ghi_1_dong_no_va_1_dong_co()
{
    $built = (new BillPaymentAccountingService())->buildEntries([
        'bill' => ['id' => 999, 'account_has' => 2, 'code' => 'TP.PC0825.00001', 'date_accounting' => '2026-08-19', 'company_id' => 1, 'department_id' => 2, 'part_id' => 3],
        'request' => ['type' => 1, 'type_money_id' => 1, 'exchange_rate' => 1, 'created_by' => 10],
        'creator' => ['id' => 10, 'company_id' => 1, 'department_id' => 2, 'part_id' => 3],
        'details' => [[
            'account_dept' => 31, 'supplier_id' => 7, 'payment_money_approve' => 1000000,
            'payment_money_approve_exchange' => 1000000, 'contractable_id' => null, 'contractable_type' => null,
        ]],
        'account_identify_numbers' => [2 => '1111', 31 => '3311'],
    ]);

    $this->assertCount(2, $built['entries']);
    $this->assertSame(AccountDetailEntry::TYPE_DEBT, $built['entries'][0]['type']);
    $this->assertSame(31, $built['entries'][0]['account_id']);
    $this->assertSame(AccountDetailEntry::TYPE_HAS, $built['entries'][1]['type']);
    $this->assertSame(2, $built['entries'][1]['account_id']);
    $this->assertSame(1000000.0, $built['entries'][1]['money_value']);
    $this->assertSame('App\Model\IncomeExpenditure\BillPayment', $built['entries'][0]['invoiceable_type']);
}
```

Viết thêm 3 test: **loại 6** (`employee_id` = người lập đề nghị, `work_id` = `TTHHD`, `group_id` = 1) · **loại 12** (`billable_type` = `DeliveryTripAccounting`, `supplier_id` lấy từ chuyến xe) · **dòng 0 đồng bị bỏ qua** (`payment_money_approve <= 0 && payment_money_approve_exchange <= 0` → `continue`).

- [x] **Step 2: Chạy test để chắc chắn nó FAIL**

```bash
cd D:/laragon/www/hrm/hrm-api && php artisan test Modules/Finance/Tests/Unit/BillPaymentAccountingServiceTest.php
```
Kỳ vọng: FAIL — `Class "BillPaymentAccountingService" not found`.

- [x] **Step 3: Viết `buildEntries()`**

Hằng số đầu class:

```php
const INVOICEABLE_TYPE   = 'App\Model\IncomeExpenditure\BillPayment';
const PRODUCT_EXPORT_TYPE = 'App\Model\Warehouse\ProductExport';
const DELIVERY_TRIP_TYPE  = 'App\Model\Delivery\DeliveryTripAccounting';
const OTHER_DELIVERY_TRIP_TYPE = 'App\Model\Delivery\OtherDeliveryTripAccounting';
const DECLARE_DEBT_TYPE   = 'App\Model\Accounting\DeclareDebtBeginning';
```
(4 chuỗi cuối phải khớp kết quả grep ở Task 2 Step 6.)

Cấu trúc port ERP `saveAccountsDetail()` :538-690, **4 nhánh** đúng thứ tự `if` của ERP: có phân bổ phiếu xuất hàng → loại 6 → loại 12 → còn lại. Mỗi dòng **Nợ** kèm 1 ref trỏ `account_has`. Sau vòng lặp, nếu tổng > 0 thì thêm **1 dòng Có** trên `account_has` kèm ref trỏ **từng `account_dept` khác nhau** (lọc trùng).

⚠️ Chiều Nợ/Có **ngược với phiếu thu**: phiếu chi ghi Nợ trên `account_dept` của từng dòng và Có trên `account_has` của phiếu.

15 cột denormalize (`identify_number`, `invoiceable_code`, `invoiceable_date_accounting`, `contractable_code`, …) điền **tường minh trong `buildEntries()`**, không dựa vào hook — giống `BillIncomeAccountingService`.

- [x] **Step 4: Chạy test để chắc chắn PASS**

```bash
php artisan test Modules/Finance/Tests/Unit/BillPaymentAccountingServiceTest.php
```
Kỳ vọng: 4 test PASS.

- [x] **Step 5: Viết `persist()`**

Chỉ insert, không tính toán: `AccountDetailEntry::create()` từng dòng, lấy id thật rồi `AccountDetailRef::create()` theo `entry_index`. Copy nguyên `BillIncomeAccountingService::persist()`.

- [x] **Step 6: Verify đối chiếu ngược với dữ liệu ERP đã ghi**

Với **5 phiếu đã duyệt của mỗi loại chi 1 / 2 / 6 / 12**: dựng lại bút toán bằng `buildEntries()` rồi diff từng trường với `account_details` + `account_detail_refs` mà cổng ERP đã ghi.

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
foreach ([1,2,6,12] as \$type) {
  \$bills = BillPayment::where('type', \$type)->where('status', 3)->limit(5)->get();
  foreach (\$bills as \$b) {
    \$erp = DB::table('account_details')
      ->where('invoiceable_type', 'App\\\\Model\\\\IncomeExpenditure\\\\BillPayment')
      ->where('invoiceable_id', \$b->id)->orderBy('id')->get();
    // dựng lại bằng buildEntries() và so từng cột: account_id, type, money_value,
    // money_value_exchange, customer_id, supplier_id, employee_id, contractable_*, billable_*, work_id
    echo \$b->code, ' erp_rows=', \$erp->count(), PHP_EOL;
  }
}
"
```
Kỳ vọng: **số dòng và từng trường khớp 100%**. Lệch dù 1 phiếu → **DỪNG**, báo user, không đi tiếp Task 10.

⚠️ Chỉ **ĐỌC**, tuyệt đối không ghi gì vào `account_details` ở step này.

---

## Task 10: Duyệt nhánh A (`approve`) — khóa dòng, ghi sổ, đồng bộ ngược

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentApprovalFlowService.php`
- Create: `hrm-api/Modules/Finance/Http/Requests/BillPayment/BillPaymentApproveRequest.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`approve()`)

**Interfaces:**
- Consumes: `BillPaymentAccountingService::buildEntries()` + `persist()` (Task 9).
- Produces: `BillPaymentApprovalFlowService::approve(int $id, array $details): BillPayment` · `syncPaymentMoneyApprove(BillPayment $bill, array $details): void`.

**Khuôn để copy:** `Services/BillIncomeApprovalService.php` (411 dòng).

- [x] **Step 1: Viết `approve()` — khóa dòng + chặn duyệt lại**

```php
/**
 * ⚠️ Ghi vào sổ cái DÙNG CHUNG với cổng ERP — duyệt 2 lần là nhân đôi bút toán, không hoàn
 * tác được. ERP không chặn (`BillPaymentController::update()` :255-275 chỉ đổi status).
 * HRM khóa dòng + kiểm lại trạng thái trong transaction, trả 409.
 */
public function approve(int $id, array $details): BillPayment
{
    return DB::transaction(function () use ($id, $details) {
        $bill = BillPayment::query()->lockForUpdate()->findOrFail($id);

        if (!$bill->canApprove()) {
            abort(403, 'Bạn không có quyền duyệt phiếu chi này.');
        }
        if ($bill->status === BillPayment::STATUS_APPROVED) {
            abort(409, 'Phiếu chi đã được duyệt trước đó.');
        }

        // Kiểm trần số tiền — sửa LỖI ERP #3: ERP chỉ chạy validatePaymentMoney() khi
        // `status != 4`, mà 4 là *Hủy* còn duyệt là 3, nên ERP KHÔNG hề kiểm lúc duyệt.
        $this->guardPaymentMoneyCeiling($bill, $details);

        $this->writeService->syncDetails($bill, $details);
        ...
    });
}
```

Nhánh A sau khi đổi trạng thái:
1. `status = STATUS_APPROVED`, `date_accounting = now()->format('Y-m-d')`, `approved_id = auth()->id()`.
2. Đề nghị → `STATUS_APPROVED_BILL_PAYMENT` (8).
3. `syncPaymentMoneyApprove()` — đồng bộ `payment_money_approve(_exchange)` xuống `bill_payment_request_details`, khớp **8 khóa** (spec §5.5), chỉ ghép khóa nào có mặt trong payload.
4. Ghi sổ: `$this->accountingService->persist($this->accountingService->buildEntries($input), ...)`.
5. Log riêng: mã phiếu · số dòng sổ cái · tổng tiền.
6. Chuông báo người lập.

- [x] **Step 2: Viết `guardPaymentMoneyCeiling()`**

Nhánh A: từng dòng `payment_money_approve ≤ payment_money_request`. Vượt → `abort(422, 'Số tiền chi không được vượt quá số dư!')` (nguyên văn ERP).

- [x] **Step 3: Verify — duyệt thật trong transaction rồi rollback**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id thủ quỹ>);
\$before = DB::table('account_details')->count();
\$bill = app(Modules\Finance\Services\BillPaymentApprovalFlowService::class)->approve(<id phiếu status 2>, [...]);
\$after = DB::table('account_details')->count();
echo 'status=', \$bill->status, ' rows_added=', \$after - \$before, PHP_EOL;
DB::rollBack();
echo 'final=', DB::table('account_details')->count(), PHP_EOL;
"
```
Kỳ vọng: `status=3`, `rows_added` > 0, và `final` **bằng đúng** con số baseline trước khi chạy.

- [x] **Step 4: Verify chặn duyệt lại trả 409**

Gọi `approve()` lần 2 trên phiếu vừa duyệt (trong cùng transaction). Kỳ vọng: ném lỗi **409**, `account_details` không tăng thêm dòng nào.

- [x] **Step 5: Verify baseline sổ cái nguyên vẹn**

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT (SELECT COUNT(*) FROM account_details) ad, (SELECT COUNT(*) FROM account_detail_refs) adr, (SELECT COUNT(*) FROM bill_payments) bp;"
```
Kỳ vọng: khớp đúng baseline Task 1 Step 2.

---

## Task 11: Hủy phiếu (`cancel`)

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Requests/BillPayment/BillPaymentCancelRequest.php`
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentApprovalFlowService.php` (`cancel()`)
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentNotifyService.php` (**thêm `notifyCancelled()`**)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`cancel()`)

**Interfaces:**
- Produces: `BillPaymentApprovalFlowService::cancel(int $id, string $reason): BillPayment` · `BillPaymentNotifyService::notifyCancelled(BillPayment $bill, string $reason): void` (người nhận = **người lập phiếu**, lý do hủy nằm trong nội dung thông báo — đây là nơi DUY NHẤT lý do hủy tồn tại).

- [x] **Step 1: Viết `BillPaymentCancelRequest`**

```php
public function rules(): array
{
    return ['reason' => 'required|string|max:500'];
}

public function messages(): array
{
    return [
        'reason.required' => 'Vui lòng nhập lý do hủy phiếu chi.',
        'reason.max'      => 'Lý do hủy không được quá 500 ký tự.',
    ];
}
```

- [x] **Step 2: Viết `cancel()`**

```php
/**
 * Hủy phiếu chi.
 *
 * ⚠️ Lý do hủy KHÔNG được lưu xuống DB: bảng `bill_payments` không có cột `note`, còn cột
 * `reason` đang giữ *Lý do chi* — ghi đè là mất dữ liệu gốc. ERP cũng bắt nhập rồi bỏ đi
 * (`BillPaymentStoreRequest`: `'note' => Rule::requiredIf($this->status == 4)`).
 * User chốt 2026-08-19: giữ hành vi ERP, đưa lý do vào NỘI DUNG THÔNG BÁO CHUÔNG gửi người
 * lập, không thêm cột (feature này không migration). Spec §9.1.
 */
public function cancel(int $id, string $reason): BillPayment
{
    return DB::transaction(function () use ($id, $reason) {
        $bill = BillPayment::query()->lockForUpdate()->findOrFail($id);

        if (!$bill->canCancel()) {
            abort(403, 'Bạn không có quyền hủy phiếu chi này.');
        }

        $bill->status = BillPayment::STATUS_CANCEL;
        $bill->save();

        // Nhánh B không có phiếu đề nghị -> không đồng bộ ngược.
        if ($bill->bill_payment_request_id) {
            BillPaymentRequest::query()
                ->where('id', $bill->bill_payment_request_id)
                ->update(['status' => BillPaymentRequest::STATUS_CANCEL]);
        }

        $this->notifyService->notifyCancelled($bill, $reason);

        return $bill;
    });
}
```

- [x] **Step 3: Verify**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id thủ quỹ>);
use Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest;
\$bill = app(Modules\Finance\Services\BillPaymentApprovalFlowService::class)->cancel(<id phiếu status 2>, 'Test hủy');
echo 'bill=', \$bill->status, ' request=', BillPaymentRequest::find(\$bill->bill_payment_request_id)->status, PHP_EOL;
DB::rollBack();
"
```
Kỳ vọng: in `bill=4 request=9`.

---

# Phase 4 — Nhánh B: loại 4 "Chi thu nhập cho nhân viên"

## Task 12: `PaymentEmployeeLookupService` — hút số liệu nhân viên theo phòng ban

**Files:**
- Create: `hrm-api/Modules/Finance/Services/PaymentEmployeeLookupService.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`paymentEmployees()`)

**Interfaces:**
- Produces: `PaymentEmployeeLookupService::forDepartment(int $departmentId, ?int $accountId): array` · `GET /v1/finance/bill-payments/payment-employees?department_id=&account_id=`. Task 20 (FE) dùng.

**Nguồn ERP:** `AccountDetail::getDataAdPaymentEmployee()` :3933 (đọc), `BillPaymentController::getDataPaymentEmployee()` :320-390 (biến đổi).

- [x] **Step 1: Lấy bảng mã công việc**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT id, code, name FROM works WHERE code IN ('TTHHD','TNST','TNSQ','TT','TVC','CPK');"
```
Ghi lại 6 id thật. Thiếu mã nào → **DỪNG**, báo user (không tự chế mã).

- [x] **Step 2: Viết truy vấn `forDepartment()`**

`GROUP BY employee_id` trên `account_details`, mỗi khoản:

```sql
SUM(CASE WHEN work_id = :work AND type = 2 THEN money_value_exchange ELSE 0 END)
- SUM(CASE WHEN work_id = :work AND type = 1 THEN money_value_exchange ELSE 0 END)
```

6 khoản ↔ 6 mã công việc: `diff_employee`←`TTHHD` · `commission_month`←`TNST` · `commission_quarter`←`TNSQ` · `commission_bonus_quarter`←`TT` · `delivery_money`←`TVC` · `other_cost`←`CPK`.

Lọc theo phòng ban qua `employee_department_id`. **Bỏ** nhân viên có cả 6 khoản = 0 (đúng ERP :360-368).

- [x] **Step 3: Viết phần biến đổi output**

Mỗi nhân viên trả: `employee_id` · `employee_code` · `employee_name` · `account_number` · `bank_name` · `bank_branch` · 6 khoản đề nghị · 6 khoản `payment_*`. Quy tắc mặc định của ERP :341-355 — nếu **tổng 6 khoản > 0** thì `payment_*` = khoản tương ứng, ngược lại = 0.

- [x] **Step 4: Verify trên dữ liệu thật**

```bash
php artisan tinker --execute="
\$rows = app(Modules\Finance\Services\PaymentEmployeeLookupService::class)->forDepartment(<id phòng ban có phiếu loại 4>, null);
echo count(\$rows), PHP_EOL;
echo json_encode(\$rows[0] ?? null, JSON_UNESCAPED_UNICODE), PHP_EOL;
"
```
Kỳ vọng: ra danh sách nhân viên, không nhân viên nào có cả 6 khoản = 0.

- [x] **Step 5: Verify đối chiếu với 1 phiếu loại 4 đã duyệt**

Lấy 1 phiếu `type = 4, status = 3`, đọc `payment_department_id`, gọi `forDepartment()` với phòng ban đó và so **danh sách nhân viên** với `bill_payment_details` của phiếu. Lệch nhiều → xem lại cách lọc phòng ban (ERP lọc qua `employee_department_id` trên sổ cái, không phải qua bảng nhân sự).

---

## Task 13: Tạo / sửa / gửi duyệt nhánh B

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentWriteService.php` (nhánh loại 4 trong `store()` / `update()` / `syncDetails()`)
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentApprovalFlowService.php` (mở rộng `guardPaymentMoneyCeiling()` cho 6 khoản nhánh B)
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentNotifyService.php` (người nhận là KT trưởng)

**Interfaces:**
- Consumes: `PaymentEmployeeLookupService` (Task 12).
- Produces: nhánh loại 4 của `store()` / `update()` / `submit()` — không tham số mới.

- [x] **Step 1: Nhánh loại 4 trong `store()`**

Bỏ qua `guardOneBillPerRequest()` (không có phiếu đề nghị). Khoá cứng theo ERP `changeType()` (`formJs.blade.php:44-50`):

```php
if ((int) $data['type'] === BillPayment::TYPE_PAYMENT_EMPLOYEE) {
    $data['bill_payment_request_id'] = null;
    $data['account_has']  = 2;   // tài khoản tiền mặt 1111 — ERP khoá cứng ở FE, HRM khoá ở BE
    $data['type_money_id'] = 1;  // VND
}
```

⚠️ **Khoá ở BE, không chỉ ở FE** — ERP chỉ khoá ở FE nên gọi thẳng API là lách được.

- [x] **Step 2: `syncDetails()` cho nhánh B**

Ghi 12 cột thu nhập (6 đề nghị + 6 `payment_*`) + `employee_id/code/name` + `account_dept`. **Không** ghi `customer_id`/`supplier_id`/`contractable_*`.

- [x] **Step 3: Trần số tiền nhánh B trong `guardPaymentMoneyCeiling()`**

Port `validatePaymentMoney()` của ERP :448-467 — với mỗi trong 6 khoản:

```php
if (abs($detail[$requestCol]) < abs($detail[$paymentCol]) && (float) $detail[$paymentCol] != 0.0) {
    abort(422, 'Số tiền chi không được vượt quá số dư!');
}
```

- [x] **Step 4: Verify — tạo + gửi duyệt phiếu loại 4, rollback**

```bash
php artisan tinker --execute="
DB::beginTransaction();
auth()->loginUsingId(<id kế toán thanh toán>);
\$svc = app(Modules\Finance\Services\BillPaymentWriteService::class);
\$bill = \$svc->store([...payload loại 4, lấy details từ PaymentEmployeeLookupService...]);
echo 'account_has=', \$bill->account_has, ' money=', \$bill->type_money_id, ' req=', var_export(\$bill->bill_payment_request_id, true), PHP_EOL;
\$svc->submit(\$bill);
echo 'status=', \$bill->fresh()->status, ' acc_approved=', var_export(\$bill->fresh()->accounting_approved_id, true), PHP_EOL;
DB::rollBack();
"
```
Kỳ vọng: `account_has=2 money=1 req=NULL`, rồi `status=5 acc_approved=NULL`.

- [x] **Step 5: Verify BE khoá cứng, không tin FE**

Gọi `store()` với `type = 4` nhưng payload cố tình gửi `account_has = 99`, `type_money_id = 7`. Kỳ vọng: bản ghi vẫn ra `account_has = 2`, `type_money_id = 1`.

---

## Task 14: `PaymentEmployeeAccountingService::buildEntries()` + unit test

**Files:**
- Create: `hrm-api/Modules/Finance/Services/PaymentEmployeeAccountingService.php`
- Create: `hrm-api/Modules/Finance/Tests/Unit/PaymentEmployeeAccountingServiceTest.php`

**Interfaces:**
- Produces: `PaymentEmployeeAccountingService::buildEntries(array $input): array{entries: array, refs: array}` (**hàm thuần**) · `persist(array $built): void`. Task 15 gọi.

**Nguồn ERP:** `BillPayment::saveAccountsDetailEmployee()` :691-732 + 2 helper `AccountDetail::createDataSaveDept()` :897 và `saveAccountDetail()` :989 — **cả 2 helper phải port**, đặt private trong service này, không nhét vào entity chỉ-đọc.

- [x] **Step 1: Đọc kỹ 2 helper ERP trước khi viết**

```bash
sed -n '897,1060p' /d/laragon/www/erp/app/Model/Accounting/AccountDetail.php
```
Ghi ra giấy: `createDataSaveDept()` gom theo khoá nào, `saveAccountDetail()` ghi ra bao nhiêu dòng.

- [x] **Step 2: Viết test TRƯỚC — 1 nhân viên, 2 khoản dương**

```php
public function test_mot_nhan_vien_hai_khoan_duong()
{
    $built = (new PaymentEmployeeAccountingService())->buildEntries([
        'bill' => ['id' => 999, 'account_has' => 2, 'payment_department_id' => 5, 'code' => 'TP.PC0825.00002', 'date_accounting' => '2026-08-19'],
        'payment_department' => ['id' => 5, 'company_id' => 1],
        'account_has_identify_number' => '1111',
        'works' => ['TTHHD' => 11, 'TNST' => 12, 'TNSQ' => 13, 'TT' => 14, 'TVC' => 15, 'CPK' => 16],
        'details' => [[
            'employee_id' => 77, 'payment_money_approve' => 3000000,
            'account_identify_number' => '3341',
            'payment_diff_employee' => 2000000, 'payment_commission_month' => 1000000,
            'payment_commission_quarter' => 0, 'payment_commission_bonus_quarter' => 0,
            'payment_delivery_money' => 0, 'payment_other_cost' => 0,
        ]],
    ]);

    // 2 dòng Nợ theo 2 khoản dương + 1 dòng Có tổng 3.000.000 trên account_has
    $debits = array_values(array_filter($built['entries'], fn ($e) => $e['type'] === AccountDetailEntry::TYPE_DEBT));
    $credits = array_values(array_filter($built['entries'], fn ($e) => $e['type'] === AccountDetailEntry::TYPE_HAS));
    $this->assertCount(2, $debits);
    $this->assertCount(1, $credits);
    $this->assertSame(3000000.0, $credits[0]['money_value']);
    $this->assertSame(11, $debits[0]['work_id']);
    $this->assertSame(5, $debits[0]['employee_department_id']);
    $this->assertSame(1, $debits[0]['employee_company_id']);
}
```

Viết thêm 2 test: **khoản âm đảo chiều** (`payment_other_cost = -500000` → dòng ghi `TYPE_HAS`, `money_value = 500000`, và tổng âm ra **1 dòng Nợ** trên `account_has`) · **dòng `payment_money_approve` rỗng bị bỏ qua**.

- [x] **Step 3: Chạy test để chắc chắn FAIL**

```bash
php artisan test Modules/Finance/Tests/Unit/PaymentEmployeeAccountingServiceTest.php
```
Kỳ vọng: FAIL — class chưa tồn tại.

- [x] **Step 4: Viết `buildEntries()`**

Với mỗi dòng chi tiết có `payment_money_approve`, sinh 6 bút toán theo bảng spec §6.2. Quy tắc dấu:

```php
// ERP: createDataSaveDept(..., abs($value), $value > 0 ? TYPE_DEBT : TYPE_HAS, [1111], [...])
$type = $value > 0 ? AccountDetailEntry::TYPE_DEBT : AccountDetailEntry::TYPE_HAS;
$money = abs($value);
```

⚠️ ERP có **lỗi thiếu `> 0`** ở khoản thưởng quý: `$detail->payment_commission_bonus_quarter ? TYPE_DEBT : TYPE_HAS` (dùng truthy thay vì so sánh) — nghĩa là giá trị **âm** cũng ra `TYPE_DEBT`. Port **đúng theo 5 khoản còn lại** (`> 0`), và ghi chú lệch này trong docblock để người review biết đây là chủ ý.

Cuối cùng 2 dòng tổng trên `account_has`: 1 dòng **Có** = tổng các khoản dương, 1 dòng **Nợ** = tổng trị tuyệt đối các khoản âm; `refs` = danh sách `identify_number` đã dùng.

- [x] **Step 5: Chạy test để chắc chắn PASS**

```bash
php artisan test Modules/Finance/Tests/Unit/PaymentEmployeeAccountingServiceTest.php
```
Kỳ vọng: 3 test PASS.

- [x] **Step 6: Verify đối chiếu ngược 5 phiếu loại 4 đã duyệt**

Giống Task 9 Step 6 nhưng cho `type = 4`: dựng lại bằng `buildEntries()`, diff từng trường với `account_details` mà ERP đã ghi (`invoiceable_id` = id phiếu).

Kỳ vọng: khớp 100%. Lệch → **DỪNG**, báo user. Đây là nhánh nguy hiểm nhất của feature (cơ chế gộp theo `identify_number`).

---

## Task 15: Duyệt 2 cấp nhánh B

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/BillPaymentApprovalFlowService.php` (rẽ nhánh trong `approve()`)

**Interfaces:**
- Consumes: `PaymentEmployeeAccountingService` (Task 14).
- Produces: `approve()` xử lý được cả 2 cấp của nhánh B — không đổi chữ ký.

- [x] **Step 1: Rẽ nhánh theo trạng thái trong `approve()`**

```php
// Nhánh B bước 1 — Kế toán trưởng duyệt: chỉ chuyển sang Chờ chi tiền, CHƯA ghi sổ cái.
if ($bill->status === BillPayment::STATUS_AWAITING_ACCOUNTING_APPROVE) {
    $bill->status = BillPayment::STATUS_AWAITING_APPROVE;
    // Sửa LỖI ERP #8: ERP gán `accounting_approved_id` = người LẬP lúc gửi duyệt.
    $bill->accounting_approved_id = auth()->id();
    $bill->save();

    $this->notifyService->notifySubmitted($bill); // -> Thủ quỹ
    return $bill;
}
```

Bước 2 (Thủ quỹ, `status = 2`) dùng chung code với nhánh A, chỉ khác **service ghi sổ**:

```php
$accountingService = (int) $bill->type === BillPayment::TYPE_PAYMENT_EMPLOYEE
    ? $this->paymentEmployeeAccountingService
    : $this->accountingService;
```

Và **bỏ qua** 2 việc chỉ có ở nhánh A: cập nhật trạng thái đề nghị (8) và `syncPaymentMoneyApprove()` — nhánh B không có phiếu đề nghị.

- [x] **Step 2: Đảm bảo ghi sổ nằm TRONG transaction**

```php
/**
 * ⚠️ Khác ERP CÓ CHỦ Ý: ERP đẩy phần ghi sổ nhánh B vào job HandleAccountingPaymentEmployee
 * (ShouldQueue). HRM chạy QUEUE_CONNECTION=sync nên job vẫn chạy ngay, NHƯNG nằm ngoài
 * transaction của controller -> ghi sổ hỏng thì phiếu vẫn "Đã duyệt" mà sổ cái trống.
 * HRM gọi thẳng service trong CÙNG transaction, hỏng thì rollback cả hai. Spec §6.4.
 */
```

**KHÔNG** tạo Job, **KHÔNG** `dispatch()`.

- [x] **Step 3: Verify luồng 2 cấp**

```bash
php artisan tinker --execute="
DB::beginTransaction();
\$svc = app(Modules\Finance\Services\BillPaymentApprovalFlowService::class);
\$before = DB::table('account_details')->count();
auth()->loginUsingId(<id kế toán trưởng>);
\$b = \$svc->approve(<id phiếu loại 4 status 5>, [...]);
echo 'sau KT truong: status=', \$b->status, ' acc=', \$b->accounting_approved_id, ' rows=', DB::table('account_details')->count() - \$before, PHP_EOL;
DB::rollBack();
"
```
Kỳ vọng: `status=2`, `acc=<id kế toán trưởng>`, `rows=0` — **bước 1 chưa ghi sổ cái**.

- [x] **Step 4: Verify bước 2 mới ghi sổ**

Chạy tiếp `approve()` với danh tính **thủ quỹ** (lệnh tinker **riêng** — auth guard cache theo tiến trình). Kỳ vọng: `status=3` và `account_details` tăng đúng số dòng `buildEntries()` trả về. Rollback sau khi kiểm.

- [x] **Step 5: Verify baseline sổ cái**

```bash
mysql -h127.0.0.1 -uroot gop_db -e "SELECT (SELECT COUNT(*) FROM account_details) ad, (SELECT COUNT(*) FROM account_detail_refs) adr;"
```
Kỳ vọng: khớp đúng baseline Task 1 Step 2.

---

# Phase 5 — In & Xuất Excel

## Task 16: `BillPaymentPrintService` — 3 mẫu, 2 liên

**Files:**
- Create: `hrm-api/Modules/Finance/Services/BillPaymentPrintService.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`printData()`)

**Interfaces:**
- Produces: `BillPaymentPrintService::render(BillPayment $bill): array{html: string, template_id: int}` · `GET /v1/finance/bill-payments/{id}/print-data`. Task 22 (FE) dùng.

**Khuôn để copy:** `Services/BillIncomePrintService.php` (686 dòng) — đã có sẵn cơ chế đọc `report_templates`, `fillReport()`, `clearNull()`.

- [x] **Step 1: Xác nhận 3 mẫu còn trong DB**

```bash
mysql -h127.0.0.1 -uroot --default-character-set=utf8mb4 gop_db -e "SELECT id, name, CHAR_LENGTH(template) len FROM report_templates WHERE id IN (211,217,236);"
```
Kỳ vọng: 3 dòng — `211` (~3.079) · `217` (~2.091) · `236` (~3.887). Thiếu mẫu nào → **DỪNG**, báo user.

- [x] **Step 2: Viết `render()` — chọn mẫu theo loại chi**

```php
/** Port ERP `BillPaymentController::print()` :392-432. */
private function pickTemplateId(BillPayment $bill): int
{
    if ((int) $bill->type === BillPayment::TYPE_PAYMENT_EMPLOYEE) {
        return self::TEMPLATE_PAYMENT_EMPLOYEE; // 236, in 1 liên
    }
    if ((int) $bill->type === 12) {
        return self::TEMPLATE_SINGLE; // 211
    }

    return $bill->details()->count() === 1 ? self::TEMPLATE_SINGLE : self::TEMPLATE_MULTI; // 211 / 217
}
```

Ghép 2 liên: mẫu **211** → nối `<br>` × 9 giữa 2 liên (cùng 1 trang A4); mẫu **217** → chèn `<div class="page-break active"></div>`; mẫu **236** → **1 liên**, không ghép.

Liên 1 gọi `getPrintData($bill, 1)`, liên 2 gọi `getPrintData($bill, 2)` — tham số `numberDebit` của ERP quyết định nhãn liên.

- [x] **Step 3: Verify — dựng bản in cho 1 phiếu mỗi loại**

```bash
php artisan tinker --execute="
use Modules\Finance\Entities\BillPayment\BillPayment;
\$svc = app(Modules\Finance\Services\BillPaymentPrintService::class);
foreach ([1,2,6,12,4] as \$t) {
  \$b = BillPayment::where('type', \$t)->where('status', 3)->first();
  if (!\$b) { echo \$t, ' - khong co phieu', PHP_EOL; continue; }
  \$r = \$svc->render(\$b);
  echo \$t, ' template=', \$r['template_id'], ' len=', strlen(\$r['html']), PHP_EOL;
}
"
```
Kỳ vọng: loại 4 → `236`; loại 12 → `211`; loại 1/2/6 → `211` hoặc `217` tùy số dòng chi tiết; `len` > 0 và **không còn chuỗi `{{`** nào chưa thay.

- [x] **Step 4: Verify không sót placeholder**

```bash
php artisan tinker --execute="
\$r = app(Modules\Finance\Services\BillPaymentPrintService::class)->render(Modules\Finance\Entities\BillPayment\BillPayment::where('status',3)->first());
preg_match_all('/\{\{[^}]+\}\}/', \$r['html'], \$m);
echo count(\$m[0]), ' placeholder con lai', PHP_EOL;
"
```
Kỳ vọng: `0 placeholder con lai`.

---

## Task 17: Xuất Excel 1 phiếu

**Files:**
- Create: `hrm-api/Modules/Finance/Exports/BillPaymentExport.php`
- Create: `hrm-api/Modules/Finance/Resources/views/exports/bill-payment.blade.php`
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/BillPaymentController.php` (`export()`)

**Interfaces:**
- Produces: `GET /v1/finance/bill-payments/{id}/export` → tải `phieu_chi_tien_<mã>.xlsx`.

**Nguồn ERP:** `app/ExcelExports/BillPaymentExcel.php` + `BillPayment::excelBillPaymentTable()` :1236 và `excelBillPaymentWithExchangeTable()` :1124.

- [x] **Step 1: Viết blade export**

2 biến thể theo ERP: có tỷ giá (`excelBillPaymentWithExchangeTable`) và không (`excelBillPaymentTable`). Chọn theo `type_money_id != 1`.

- [x] **Step 2: Viết `export()` trong controller**

Gate bằng `canView()` (giống In). Trả `Excel::download()`.

- [x] **Step 3: Verify**

```bash
php artisan tinker --execute="
auth()->loginUsingId(<id có quyền xem>);
\$b = Modules\Finance\Entities\BillPayment\BillPayment::where('status',3)->first();
\$file = (new Modules\Finance\Exports\BillPaymentExport(\$b))->raw(Maatwebsite\Excel\Excel::XLSX);
echo strlen(\$file), ' bytes', PHP_EOL;
"
```
Kỳ vọng: > 0 bytes, không exception.

---

# Phase 6 — Frontend

## Task 18: Màn danh sách `index.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/index.vue`

**Interfaces:**
- Consumes: `GET /v1/finance/bill-payments`, `GET /v1/finance/bill-payments/accounts`.
- Produces: route `/finance/bill-payments`.

**Khuôn để copy:** `hrm-client/pages/finance/bill-incomes/index.vue` (827 dòng) — copy pattern rồi đổi cột/bộ lọc.

- [x] **Step 1: Kiểm khoá cấu hình cột không trùng màn khác**

```bash
cd D:/laragon/www/hrm/hrm-client && grep -rn "finance_bill_payments" pages/ components/
```
Kỳ vọng: **0 kết quả** trước khi viết. Có kết quả → đổi khoá, báo user.

- [x] **Step 2: Dựng khung màn**

4 mixin bắt buộc: `PageTitleMixin` · `CheckPermission` · `filterStateMixin` · `columnCustomizationMixin`. `localStorageKey` = `columnScreenKey` = `'finance_bill_payments'`.

14 cột theo spec §11.1. Cột **Mã phiếu** là `<nuxt-link>` thật (chuột phải mở tab mới được), đặt `locked: true` cùng STT và Hành động. Sắp xếp mặc định `created_at DESC`.

Bảng trống hiện dòng **"Không có dữ liệu phù hợp"**. Phân trang mặc định 10, chọn 5/10/20/50/100, đổi số dòng nhảy về trang 1. STT dùng `getNumericalOrder(currentPage, pageSize, index)` — **không** `index + 1`.

- [x] **Step 3: Dựng bộ lọc**

10 trường (spec §11.1) → **có** popup "Cài đặt bộ lọc", **bỏ** khối nâng cao. Ô chọn tự tìm ngay khi chọn; ô gõ tay chờ Enter/nút Tìm kiếm. Placeholder `Chọn <X>` / `Nhập <X>` — **không** `Tất cả`, **không** `Chọn...`. Nút **Làm mới** xóa hết điều kiện **và** tải lại danh sách. Panel lọc **bỏ prop `title`**, dùng mặc định "Bộ lọc danh sách".

- [x] **Step 4: Cột hành động + toolbar**

Toolbar: **Thêm mới → Cấu hình cột** (màn này không có Import / Xuất danh sách).

Cột hành động: **Sửa → Xóa → menu "…"** (In · Xuất Excel · Duyệt · Hủy). Nút không dùng được thì **ẩn hẳn** (`visible` / `v-if`), **không** `disabled` (`V2BaseButton` không có prop đó). Không có nút "Xem chi tiết".

⚠️ `V2BaseRowActions` emit **chuỗi key**, so `action === 'edit'` chứ không phải `action.key`.

Mọi cờ quyền khởi tạo `false`, chỉ gán từ `is_can_*` của BE.

- [x] **Step 5: Verify — parse + kiểm cờ quyền**

```bash
cd D:/laragon/www/hrm/hrm-client
node -e "
const c=require('vue-template-compiler'),fs=require('fs');
const s=fs.readFileSync('pages/finance/bill-payments/index.vue','utf8');
const t=s.match(/<template>([\s\S]*)<\/template>/)[1];
const r=c.compile(t);
console.log(r.errors.length? r.errors : 'template OK');
"
grep -nE "can[A-Za-z]*\s*=\s*true" pages/finance/bill-payments/index.vue
```
Kỳ vọng: `template OK` và grep **0 kết quả**.

⚠️ **Không** dùng `npx eslint` làm cổng verify — hrm-client không có ESLint config và fail trên Node 14.

- [x] **Step 6: Verify icon có thật trong font local**

```bash
grep "^\.ri-" assets/scss/custom/plugins/icons/_remixicon.scss | grep -E "<tên icon đã dùng>"
```
Kỳ vọng: mỗi icon dùng trong màn đều có 1 dòng. Thiếu → đổi icon khác, không để icon trống.

---

## Task 19: Form nhánh A + `create.vue` / `_id/edit.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/create.vue`
- Create: `hrm-client/pages/finance/bill-payments/_id/edit.vue`
- Create: `hrm-client/pages/finance/bill-payments/components/BillPaymentForm.vue`
- Create: `hrm-client/pages/finance/bill-payments/components/PaymentRequestSearchModal.vue`

**Interfaces:**
- Consumes: `GET /search-payment-requests`, `GET /accounts`, `POST /`, `PUT /{id}`, `POST /{id}/submit`.
- Produces: component `BillPaymentForm` với prop `value` (object phiếu) và `mode` (`'create' | 'edit'`).

**Khuôn để copy:** `pages/finance/bill-incomes/components/BillIncomeForm.vue` (1.018 dòng) và `IncomeRequestSearchModal.vue` (274 dòng). Khuôn form chuẩn là `CustomerForm.vue` — ⚠️ **không** chép khuôn từ `ProductTransferRequestForm.vue` (class `form-card` / `form-header` nằm trong `<style>` riêng của màn đó, không có ở v2-styles).

- [x] **Step 1: Viết `PaymentRequestSearchModal.vue`**

Popup chọn phiếu đề nghị. Mọi select trong popup dùng **`V2BaseSelectInModal`**, không `V2BaseSelect`.

⚠️ `V2BaseSelect` là select2 — **không có** prop `reduce` / `label`.
⚠️ **Không** đặt prop tên `errors` hoặc `fields` — vee-validate chiếm 2 tên đó, prop bị che, chỉ lộ khi mở trình duyệt.

- [x] **Step 2: Viết `BillPaymentForm.vue` — khối đầu phiếu nhánh A**

Chọn phiếu đề nghị → tự đổ và **khoá chỉ đọc**: Loại chi · Hình thức TT · Loại tiền · Tỷ giá · Lý do chi · Người đề nghị · Phòng ban. Tự nhập: Tài khoản có · Người nhận.

Ô chọn trong bảng dùng `V2BaseInput` readonly + popup, **không** tự chế nút.

- [x] **Step 3: Bảng chi tiết nhánh A**

Cột: Tài khoản nợ · Đối tượng (KH/NCC/NV) · Hợp đồng · Số tiền đề nghị chi · **Số tiền chi** · Ghi chú. Tiền căn phải, định dạng `.` ngăn nghìn `,` ngăn thập phân.

- [x] **Step 4: Validate + unsaved-changes**

Chỉ trường **Tên/bắt buộc tối thiểu** gắn `required` ở FE; required còn lại do BE trả 422. Lỗi hiện **inline ngay dưới ô** (`is-invalid` + `invalid-feedback`), dùng cờ `touched` để chỉ hiện sau lần submit đầu. Còn lỗi → **không gọi API**, con trỏ nhảy về ô lỗi đầu tiên.

Dùng `unsavedChangesMixin` (page) + gọi `markFormSaved()` sau khi lưu thành công. Chưa đổi gì mà bấm Hủy → **không** hiện popup confirm.

⚠️ Chọn đúng mixin theo kiểu màn — sai mixin thì popup **không bao giờ** hiện (xem mục 2b của `unsaved-changes/SKILL.md`).

- [x] **Step 5: 2 nút lưu**

Nút trong `V2Footer`, **không** tự dựng khối nút. "Lưu nháp" → `POST /` hoặc `PUT /{id}`. "Lưu và gửi duyệt" → lưu xong gọi tiếp `POST /{id}/submit`.

⚠️ Lưu dữ liệu dùng `apiPostMethod` với khoá `payload`, **không** phải `apiPost`.

- [x] **Step 6: Verify parse cả 4 file**

```bash
cd D:/laragon/www/hrm/hrm-client
for f in pages/finance/bill-payments/create.vue pages/finance/bill-payments/_id/edit.vue pages/finance/bill-payments/components/BillPaymentForm.vue pages/finance/bill-payments/components/PaymentRequestSearchModal.vue; do
  node -e "
  const c=require('vue-template-compiler'),fs=require('fs');
  const s=fs.readFileSync('$f','utf8');
  const t=(s.match(/<template>([\s\S]*)<\/template>/)||[])[1];
  const r=c.compile(t||'');
  console.log('$f', r.errors.length? r.errors : 'OK');
  "
done
grep -rnE "can[A-Za-z]*\s*=\s*true" pages/finance/bill-payments/
grep -rn "V2BaseSelect\b" pages/finance/bill-payments/components/PaymentRequestSearchModal.vue
```
Kỳ vọng: 4 dòng `OK`; 2 grep cuối **0 kết quả** (trong modal phải là `V2BaseSelectInModal`).

---

## Task 20: Bảng nhánh B `PaymentEmployeeTable.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/components/PaymentEmployeeTable.vue`
- Modify: `hrm-client/pages/finance/bill-payments/components/BillPaymentForm.vue` (rẽ nhánh theo Loại chi)

**Interfaces:**
- Consumes: `GET /v1/finance/bill-payments/payment-employees?department_id=`.
- Produces: component nhận `department_id`, emit `input` là mảng `details` nhánh B.

- [x] **Step 1: Rẽ nhánh trong `BillPaymentForm.vue`**

Loại chi = 4 → ẩn khối chọn phiếu đề nghị, hiện ô **Phòng ban chi**; Tài khoản có và Loại tiền hiện **chỉ đọc** (BE khoá cứng ở Task 13, FE chỉ hiển thị cho khớp).

- [x] **Step 2: Viết `PaymentEmployeeTable.vue`**

Đổi phòng ban → gọi API hút số liệu → đổ bảng. Cột: STT · Số tài khoản nợ · Tên tài khoản · Nhân viên · 6 khoản (đề nghị / thực chi) · Số TK ngân hàng · Tên ngân hàng · Chi nhánh · Tổng cộng. Dòng **Tổng cộng** cuối bảng.

Ô "thực chi" cho sửa, chặn vượt khoản đề nghị ngay tại FE (BE vẫn kiểm lại — Task 13 Step 3).

- [x] **Step 3: Nút lưu nhánh B**

"Lưu và gửi KT trưởng duyệt" thay cho "Lưu và gửi duyệt" — cùng gọi `POST /{id}/submit`, BE tự rẽ sang trạng thái 5.

- [x] **Step 4: Verify**

```bash
cd D:/laragon/www/hrm/hrm-client
node -e "
const c=require('vue-template-compiler'),fs=require('fs');
const s=fs.readFileSync('pages/finance/bill-payments/components/PaymentEmployeeTable.vue','utf8');
const r=c.compile(s.match(/<template>([\s\S]*)<\/template>/)[1]);
console.log(r.errors.length? r.errors : 'OK');
"
```
Kỳ vọng: `OK`.

---

## Task 21: Màn chi tiết + popup duyệt

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/_id/index.vue`
- Create: `hrm-client/pages/finance/bill-payments/components/ApproveBillPaymentModal.vue`

**Interfaces:**
- Consumes: `GET /{id}`, `POST /{id}/approve`, `POST /{id}/cancel`.

**Khuôn để copy:** `pages/finance/bill-incomes/_id/index.vue` (352 dòng) và `ApproveBillIncomeModal.vue` (326 dòng).

- [x] **Step 1: Dựng màn chi tiết**

Tiêu đề `Chi tiết phiếu chi: <mã>`, số phiếu hiện ngay dưới tiêu đề. Trạng thái dùng `V2BaseBadge`, text từ `status_text` của BE — **không** map số → chữ ở FE. Ô rỗng in `—`.

⚠️ Hành động ở màn chi tiết phải **khớp hệt** màn danh sách — cả danh sách nút lẫn điều kiện ẩn/hiện, đọc từ **cùng bộ cờ `is_can_*`**. Đây là bẫy đã dính (2 màn lệch số nút).

- [x] **Step 2: Viết `ApproveBillPaymentModal.vue`**

Nhập số tiền thực chi từng dòng rồi gửi `POST /{id}/approve`. Nhánh B hiện 6 khoản thay vì 1 ô số tiền.

Popup xác nhận dùng `base-confirm-modal` / `$confirm()`, **không** tự khai `b-modal`.

- [x] **Step 3: Nút Hủy phiếu**

Bắt buộc nhập lý do hủy (BE trả 422 nếu thiếu). Hiện rõ cho user biết lý do này **đi vào thông báo** gửi người lập.

- [x] **Step 4: Verify**

```bash
cd D:/laragon/www/hrm/hrm-client
for f in pages/finance/bill-payments/_id/index.vue pages/finance/bill-payments/components/ApproveBillPaymentModal.vue; do
  node -e "
  const c=require('vue-template-compiler'),fs=require('fs');
  const s=fs.readFileSync('$f','utf8');
  const r=c.compile(s.match(/<template>([\s\S]*)<\/template>/)[1]);
  console.log('$f', r.errors.length? r.errors : 'OK');
  "
done
grep -rn "b-modal" pages/finance/bill-payments/components/ApproveBillPaymentModal.vue
```
Kỳ vọng: 2 dòng `OK`; grep `b-modal` **0 kết quả**.

---

## Task 22: Trang in `_id/print.vue`

**Files:**
- Create: `hrm-client/pages/finance/bill-payments/_id/print.vue`

**Interfaces:**
- Consumes: `GET /{id}/print-data`.

**Khuôn để copy:** `pages/finance/bill-incomes/_id/print.vue` (359 dòng).

- [x] **Step 1: Dựng trang in**

Nhận HTML đã đổ mẫu từ BE, render vào khung giấy A4.

⚠️ `hrm-client/static/css/pdf.css` **không tồn tại** mà plugin in lại khai nạp → phải **tự bù rule** vào `options.styles`. **KHÔNG** thêm file vào `static/` (thư mục dùng chung toàn hệ thống). Bài học từ `finance-bill-adjust-dept-request`.

- [x] **Step 2: Kiểm các lỗi in hay gặp**

Đọc `.claude/skills/print-page/SKILL.md` và kiểm: viền phải/dưới khi sang trang · nội dung cột bị cắt · logo/letterhead · tự bật hộp thoại in (không bắt user Ctrl+P) · ô gộp `rowspan` khi in nhiều trang.

- [x] **Step 3: Verify**

```bash
cd D:/laragon/www/hrm/hrm-client
node -e "
const c=require('vue-template-compiler'),fs=require('fs');
const s=fs.readFileSync('pages/finance/bill-payments/_id/print.vue','utf8');
const r=c.compile(s.match(/<template>([\s\S]*)<\/template>/)[1]);
console.log(r.errors.length? r.errors : 'OK');
"
grep -rn "pdf.css" pages/finance/bill-payments/_id/print.vue
```
Kỳ vọng: `OK`; grep `pdf.css` **0 kết quả** (rule phải nằm inline trong `options.styles`).

---

## Task 23: Menu + nút "Tạo phiếu chi" ở màn Đề nghị thanh toán

**Files:**
- Modify: `hrm-client/components/subsystem-menu/finance.js:83`
- Modify: `hrm-client/pages/finance/bill-payment-requests/_id/index.vue` (thêm nút)
- Modify: `hrm-api/Modules/Finance/Transformers/BillPaymentRequestResource/*` (thêm cờ `is_can_create_bill_payment`)

**Interfaces:**
- Produces: cờ BE `is_can_create_bill_payment` trên resource chi tiết Đề nghị thanh toán.

⚠️ **Đây là màn ĐÃ NGHIỆM THU** — phải test lại luồng cũ của nó sau khi sửa.

- [x] **Step 1: Gắn link menu**

Đổi `{ label: 'Phiếu chi' }` (dòng 83) thành:

```js
            { label: 'Phiếu chi', link: '/finance/bill-payments' },
```

Giữ nguyên 3 mục còn lại của nhóm. Đúng **1 lối vào**, không thêm mục `?mode=`.

- [x] **Step 2: Thêm cờ BE**

```php
/**
 * Đề nghị thanh toán đã đủ điều kiện lập Phiếu chi chưa (spec §11.7).
 * 3 điều kiện: đang ở trạng thái 6 · chưa có phiếu chi nào trỏ tới · có quyền Kế toán thanh toán.
 */
'is_can_create_bill_payment' => $this->status === self::STATUS_AWAITING_CREATE_BILL_PAYMENT
    && !BillPayment::existsForRequest($this->id)
    && BillPayment::currentEmployeeHasPermissionPublic(BillPayment::PERMISSION_ACCOUNTANT),
```

⚠️ `currentEmployeeHasPermission()` trong trait là `protected` — thêm 1 wrapper `public static` trên `BillPayment` thay vì đổi tầm nhìn của trait dùng chung.

- [x] **Step 3: Thêm nút ở màn chi tiết đề nghị**

Nút "Tạo phiếu chi" trong `V2Footer`, `v-if="detail.is_can_create_bill_payment"` (cờ khởi tạo `false`), điều hướng `/finance/bill-payments/create?bill_payment_request_id=<id>`.

- [x] **Step 4: Nhận query param ở `create.vue`**

`create.vue` đọc `$route.query.bill_payment_request_id` → nếu có thì tự nạp phiếu đề nghị vào form, bỏ qua bước mở popup.

- [x] **Step 5: Verify**

```bash
cd D:/laragon/www/hrm/hrm-client
node -e "require('@babel/parser').parse(require('fs').readFileSync('components/subsystem-menu/finance.js','utf8'),{sourceType:'module'});console.log('menu OK')"
node -e "
const c=require('vue-template-compiler'),fs=require('fs');
const s=fs.readFileSync('pages/finance/bill-payment-requests/_id/index.vue','utf8');
const r=c.compile(s.match(/<template>([\s\S]*)<\/template>/)[1]);
console.log(r.errors.length? r.errors : 'detail OK');
"
grep -n "Phiếu chi" components/subsystem-menu/finance.js
```
Kỳ vọng: `menu OK` · `detail OK` · dòng menu có `link: '/finance/bill-payments'`.

- [x] **Step 6: Verify cờ BE trên dữ liệu thật**

```bash
cd D:/laragon/www/hrm/hrm-api && php artisan tinker --execute="
auth()->loginUsingId(<id kế toán thanh toán>);
use Modules\Finance\Entities\BillPaymentRequest\BillPaymentRequest;
\$co = BillPaymentRequest::where('status',6)->whereNotExists(function(\$q){\$q->selectRaw('1')->from('bill_payments')->whereColumn('bill_payments.bill_payment_request_id','bill_payment_requests.id');})->count();
\$da = BillPaymentRequest::where('status',6)->whereExists(function(\$q){\$q->selectRaw('1')->from('bill_payments')->whereColumn('bill_payments.bill_payment_request_id','bill_payment_requests.id');})->count();
echo 'duoc tao=', \$co, ' da co phieu=', \$da, PHP_EOL;
"
```
Kỳ vọng: 2 con số hợp lý; phiếu đã có phiếu chi thì cờ phải `false`.

---

## Checkpoint cuối — trước khi báo xong

- [x] Chạy lại toàn bộ unit test: `php artisan test Modules/Finance/Tests/Unit/`
- [x] Đếm lại baseline: `bill_payments` = **1302** · `bill_payment_details` = **3307** · `account_details` / `account_detail_refs` khớp số ghi ở Task 1 Step 2
- [x] `grep -rnE "can[A-Za-z]*\s*=\s*true" hrm-client/pages/finance/bill-payments/` → **0 kết quả**
- [x] `php -l` sạch trên toàn bộ file BE mới
- [x] Chạy checklist tự kiểm mục A–H của `.claude/skills/erp-to-hrm-screen/SKILL.md`
- [x] Báo user **rõ phần chưa kiểm chứng**: nhánh phân bổ phiếu xuất hàng (0 dòng dữ liệu) chỉ verify bằng đọc code; toàn bộ FE chưa mở trình duyệt
- [x] Cập nhật `plan.md` (đánh `[x]`) + `.plans/gop-db/STATUS.md`


---

### Checkpoint — 2026-08-19

Vua hoan thanh: TOAN BO 23/23 task (6 phase). BE 26 file, FE 9 file. 18/18 unit test PASS.
Dang lam do: khong con task nao trong plan.
Buoc tiep theo: user tu mo trinh duyet nghiem thu; quyet 5 diem con treo (xem design.md muc "Diem con treo").
Blocked: khong co.

**Luu y khi doc lai plan nay**: mot so step verify trong plan mo ta lenh khong chay duoc tren may nay
(`php artisan route:list`, `php artisan tinker <file>`) — da thay bang cach khac, ghi trong ledger.
Mot so step co ket qua LECH voi mo ta ban dau cua plan (namespace morph, ten bang, mau badge, cot
Khach hang/NCC, chu ky service, ten class ApprovalFlow) — plan va spec DA duoc sua theo du lieu that;
ly do tung thay doi ghi trong ledger `<scratchpad>/sdd/finance-bill-payment/progress.md`.

### Sửa lỗi file Excel xuất phiếu chi — 2026-08-20 (user yêu cầu, cùng bộ lỗi của Phiếu thu)

Cùng 3 triệu chứng đã sửa ở `.plans/gop-db/finance-bill-income/plan.md` mục F1-F5: thiếu logo
letterhead, cột quá hẹp, cột số tiền bị Excel cảnh báo "The number in this cell is formatted as
text". Phiếu chi nặng hơn Phiếu thu vì có **3 bố cục** (default / delivery / employee).

- [x] G1. `BillPaymentPrintService`: các hàm dựng bảng bản EXCEL + ô số tiền xuất SỐ THÔ.
      KHÔNG đụng bản IN.
- [x] G2. `BillPaymentExport` implement `WithColumnWidths` — bề rộng riêng cho từng bố cục.
- [x] G3. `BillPaymentExport` implement `WithDrawings` — nhúng letterhead vào A1 (bỏ quyết định cũ
      "không nhúng ảnh": lý do cũ là `safeImage()` của ERP luôn trả ảnh trong suốt, HRM nay tải
      thẳng URL nên ra ảnh thật).
- [x] G4. `registerEvents()`: tính lại vùng ô tiền theo bố cục (vùng cứng của ERP đang trỏ trượt —
      trước đây vô hại vì ô là chuỗi, nay ô là SỐ nên trỏ trượt = mất dấu phân cách).
- [x] G5. Kiểm chứng: dựng file cho mỗi bố cục, đọc lại xác nhận kiểu ô + bề rộng + drawing.
- [x] G6. Viết `.claude/skills/export-excel/SKILL.md` gói 3 quy tắc này (skill là tài sản chung →
      tạo file, KHÔNG commit, để user đưa qua PR).

**Cách làm chốt lại (khác đề xuất ban đầu ở G4):** không tính lại vùng ô nữa mà bỏ hẳn cơ chế vùng ô.
HTML reader của PhpSpreadsheet đọc thuộc tính `data-format` trên từng thẻ `<td>`
(`Reader/Html.php::processDomElementDataFormat()`), nên mỗi ô tiền tự khai `data-format="#,##0"`
ngay chỗ dựng HTML → không còn phụ thuộc số dòng. Đã áp cùng cách cho Phiếu thu (sửa lại F4).

Phần nhúng letterhead tách thành trait dùng chung
`Modules/Finance/Exports/Concerns/EmbedsCompanyLetterhead.php` (Phiếu thu + Phiếu chi cùng dùng).

**Kết quả kiểm chứng (dựng file thật cho cả 3 bố cục, đọc lại bằng PhpSpreadsheet):**

| Bố cục | Phiếu | Trước | Sau |
| --- | --- | --- | --- |
| default (loại 1) | 918, 25 dòng | cột F dòng 12-36 `General` → `1000000` | F+G `#,##0` từ dòng đầu tới dòng Tổng cộng |
| employee (loại 4) | 290, 20 dòng | ô "Số tiền thực chi" là CHUỖI `"120,058,380"`; bảng kê 2 mất định dạng từ dòng 46; cột Tổng cộng không bao giờ có | tất cả `[n]` + `#,##0`, hết bảng |
| delivery (loại 12) | 1316, 60 dòng | 2 ô tiền khối Liên/Nợ/Có là CHUỖI | `[n]` + `#,##0` |
| Bề rộng cột | cả 3 | A=7.14 · B=14.28 (đổi từ px) | đặt theo bố cục: vd default A=8 · C=30 · D/E=26 |
| Logo | cả 3 | không có | drawing A1, dòng 1 cao 58pt |

Bản IN của cả 3 loại chạy lại vẫn ra số có dấu phân cách như cũ (`render()` không đổi).

**Chưa kiểm chứng:** ảnh letterhead thật (local không với tới `erp.test:8080/uploads/...`) — test
bằng PNG tạm qua `file://`. Phiếu ngoại tệ: DB gộp 0 phiếu, chỉ đối chiếu code.

### Checkpoint — 2026-08-20 (G1-G6)
Vừa hoàn thành: sửa 3 lỗi file Excel phiếu chi + viết skill `.claude/skills/export-excel/SKILL.md`.
Đang làm dở: không có.
Bước tiếp theo: user tải lại Excel phiếu chi (thử cả loại 1, loại 4, loại 12) trên môi trường dev.
Blocked: không.

⚠️ `.claude/skills/export-excel/SKILL.md` và dòng mới trong bảng skill của `CLAUDE.md` là **tài sản
chung** → theo quy tắc team phải đưa qua PR, chưa commit.


---

## Phase I - Logo (letterhead) dung chung cach cua man Bao gia (2026-08-21)

Lam theo yeu cau user ngay sau khi xong ben Phieu thu (xem
`.plans/gop-db/finance-bill-income/plan.md` Phase G + H cho ly do day du).

- [x] I1 - `BillPaymentPrintService::headerUrl()`: lay cong ty theo `bill_payments.company_id`
      truoc, fallback cong ty nguoi tao (ERP lay theo nguoi tao)
- [x] I2 - Thieu `ERP_URL` -> tra nguyen path tuong doi thay vi `''` (dung nhanh
      `return company.header_url || h` cua bao gia)
- [x] I3 - Cap nhat docblock muc 5 cua class + docblock `headerUrl()`
- [x] I4 - Verify ban IN (ca 5 loai phieu / 2 mau 211 + 236) va ban EXCEL

**Chi sua 1 file**: `Modules/Finance/Services/BillPaymentPrintService.php` - 2 dong lenh, con lai
la comment. `BillPaymentExport` da dung san trait `EmbedsCompanyLetterhead` nen khong phai sua.

### Checkpoint - 2026-08-21 (I1-I4)
Vua hoan thanh: logo ban in + Excel phieu chi.

Do tren du lieu that (1.305 phieu chi): **0 phieu mat logo** truoc va sau (nguoi tao deu co
`company_id`), nhung **162 phieu** truoc day in ra logo KHAC cong ty ghi tren phieu -> nay dung.

Verify that:

| | Ket qua |
| --- | --- |
| `TPHP.PC0726.00001` (phieu cty 2, nguoi tao cty 1) | ban in mau 211 -> `.../cn-hp.png` (truoc la `ts-hn.png`) |
| `TPSG.PC0726.00011` (phieu cty 4, nguoi tao cty 5) | `.../tpsg.png` |
| Ca 5 loai phieu (type 1/2/4/6/12, mau 211 + 236) | deu co `<img src="https://erp.eteksofts.com/uploads/...">` |
| File Excel `BillPaymentExport::drawings()` | 1 drawing `letterhead 650x72 @A1` |

**Chua kiem chung:** anh hien that tren trinh duyet - can user mo lai ban in tren dev.
Blocked: khong.
