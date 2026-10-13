# Fix hạch toán báo có trùng (idempotent + atomic) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chặn phát sinh dòng Có thừa khi hạch toán báo có (PBC) — làm `saveAccountsDetail()` idempotent (xóa hạch toán cũ trước khi tạo lại) và bọc job import trong transaction.

**Architecture:** Sửa 2 file. (A) `BillIncomeReport::saveAccountsDetail()` xóa account_details cũ của chính báo có (+ refs) ở đầu method → gọi N lần ra đúng 1 bộ, fix cả đường job (race) lẫn `update()` (cộng dồn). (B) `StoreIncomeReportJob::handle()` bọc `DB::transaction`.

**Tech Stack:** PHP 7.4, Laravel 6, MySQL, queue.

## Global Constraints

- KHÔNG commit/push git khi user chưa yêu cầu (CLAUDE.md). Bước "Commit" chỉ chạy khi user đồng ý.
- KHÔNG đọc/sửa `vendor/`, `node_modules/`.
- ⚠️ `.env` hiện trỏ **PROD erp_new** — TUYỆT ĐỐI không chạy test/tinker GHI dữ liệu. Kiểm thử chỉ trên DEV/local (đổi `.env` trước) hoặc browser dev.
- Chỉ sửa `saveAccountsDetail()` của **BillIncomeReport** — KHÔNG đụng model khác (BillIncome, BillPayment...).
- Branch: `sync_quotation` (xác nhận khi thực thi).
- `account_details` không có FK cứng từ bảng khác ngoài `account_detail_refs` → xóa-tạo-lại an toàn.

---

## File Structure

- **Modify** `app/Model/IncomeExpenditure/BillIncomeReport.php` — thêm khối xóa-cũ ở đầu `saveAccountsDetail()` (sau dòng 352).
- **Modify** `app/Jobs/StoreIncomeReportJob.php` — import `DB` + bọc thân `handle()` trong `DB::transaction`.

---

### Task 1: Idempotent `saveAccountsDetail()` (xóa hạch toán cũ trước khi tạo lại)

**Files:**
- Modify: `app/Model/IncomeExpenditure/BillIncomeReport.php:352`

**Interfaces:**
- `AccountDetail` và `AccountDetailRef` đã được import sẵn trong file (method đang dùng `AccountDetail::create`/`AccountDetailRef::create`).

- [x] **Step 1: Thêm khối xóa-cũ ở đầu method**

Trong `saveAccountsDetail()`, thay đoạn:

```php
        $now = $created_at ?? Carbon::now();

        $details = $this->details;
```

bằng:

```php
        $now = $created_at ?? Carbon::now();

        // Idempotent: xóa hạch toán cũ của CHÍNH báo có này (+ refs) trước khi tạo lại.
        // Tránh trùng/cộng dồn khi saveAccountsDetail bị gọi lại (sửa phiếu, hoặc race ở job import).
        $oldAccountDetailIds = AccountDetail::where('invoiceable_id', $this->id)
            ->where('invoiceable_type', self::class)
            ->pluck('id');
        if ($oldAccountDetailIds->isNotEmpty()) {
            AccountDetailRef::whereIn('account_detail_id', $oldAccountDetailIds)->delete();
            AccountDetail::whereIn('id', $oldAccountDetailIds)->delete();
        }

        $details = $this->details;
```

- [x] **Step 2: Lint**

Run: `php -l app/Model/IncomeExpenditure/BillIncomeReport.php`
Expected: `No syntax errors detected`.

- [x] **Step 3: Review tĩnh — xác nhận `AccountDetail`/`AccountDetailRef` đã import**

Run: `grep -nE "use .*(AccountDetail|AccountDetailRef);" app/Model/IncomeExpenditure/BillIncomeReport.php`
Expected: thấy cả 2 dòng `use`. Nếu thiếu `AccountDetailRef` → thêm `use App\Model\Accounting\AccountDetailRef;` (kiểm chứng namespace bằng `grep -rn "class AccountDetailRef" app/Model`).

- [ ] **Step 4: Commit** (chỉ khi user yêu cầu)

```bash
git add app/Model/IncomeExpenditure/BillIncomeReport.php
git commit -m "fix(bao-co): saveAccountsDetail idempotent - xóa hạch toán cũ trước khi tạo lại"
```

---

### Task 2: Bọc `StoreIncomeReportJob::handle()` trong transaction

**Files:**
- Modify: `app/Jobs/StoreIncomeReportJob.php` (import `DB` + wrap `handle()`)

**Interfaces:**
- Consumes: `BillIncomeReport::saveAccountsDetail()` đã idempotent (Task 1).

- [x] **Step 1: Thêm import DB**

Sau dòng `use Illuminate\Support\Carbon;` (dòng 18), thêm:

```php
use Illuminate\Support\Facades\DB;
```

- [x] **Step 2: Bọc thân `handle()` trong `DB::transaction`**

Đổi:

```php
    public function handle()
    {
        $employee = Employee::query()->with(['info'])->find($this->user_id);
```

thành:

```php
    public function handle()
    {
        DB::transaction(function () {
        $employee = Employee::query()->with(['info'])->find($this->user_id);
```

và thêm `});` đóng closure ngay trước dấu `}` đóng method `handle()` (sau dòng `$bill_income_report->saveAccountsDetail();`). Cụ thể đổi:

```php
            $bill_income_report->saveAccountsDetail();
    }
```

thành:

```php
            $bill_income_report->saveAccountsDetail();
        });
    }
```

- [x] **Step 3: Lint**

Run: `php -l app/Jobs/StoreIncomeReportJob.php`
Expected: `No syntax errors detected`.

- [ ] **Step 4: Commit** (chỉ khi user yêu cầu)

```bash
git add app/Jobs/StoreIncomeReportJob.php
git commit -m "fix(bao-co): bọc StoreIncomeReportJob::handle trong DB transaction"
```

---

### Task 3: Kiểm thử (DEV/local — KHÔNG prod)

**Files:** không sửa code.

- [ ] **Step 1: Đổi `.env` về DB DEV/local** (xác nhận `grep -E "^DB_DATABASE|^DB_HOST" .env` KHÔNG phải prod erp_new) trước khi test ghi dữ liệu.

- [ ] **Step 2: Test đường `update()` (bug cộng dồn)**

Trên dev: tạo 1 báo có (PBC) → ghi nhận số `account_details` (1 Có + 1 Nợ). Mở SỬA phiếu → lưu lại 2–3 lần.
Kỳ vọng: vẫn **đúng 1 Có + 1 Nợ** mỗi lần (trước fix sẽ cộng dồn thành 2,3... Có/Nợ).
Query kiểm: `SELECT type, COUNT(*) FROM account_details WHERE invoiceable_id=<id> AND invoiceable_type LIKE '%BillIncomeReport%' GROUP BY type;`

- [ ] **Step 3: Test đường import**

Trên dev: import Excel báo có (vài dòng) → kiểm mỗi báo có chỉ có 1 Có/detail + 1 Nợ.
Query: `SELECT invoiceable_id, SUM(type=2) n_co, SUM(type=1) n_no FROM account_details WHERE invoiceable_type LIKE '%BillIncomeReport%' GROUP BY invoiceable_id;`

- [ ] **Step 4: Đối chiếu sổ chi tiết tài khoản** — báo có vừa tạo/sửa không còn hiện x2.

---

### Task 4 (OPTIONAL — để pha sau): `StoreIncomeReportJob implements ShouldBeUnique`

Chống worker xử lý job trùng. Chỉ làm nếu sau Task 1–3 vẫn còn nghi double ở đường queue.

- [ ] **Step 1:** `class StoreIncomeReportJob implements ShouldQueue, ShouldBeUnique` + `use Illuminate\Contracts\Queue\ShouldBeUnique;` + định nghĩa `public function uniqueId() { return md5($this->note.'|'.$this->money.'|'.$this->date_accounting.'|'.$this->account_number); }`.
- [ ] **Step 2:** `php -l`. Lưu ý: cần cache driver hỗ trợ lock (redis) — xác nhận hạ tầng trước khi bật.

---

## Self-Review

1. **Spec coverage:**
   - A. Idempotent saveAccountsDetail → Task 1 (xóa cũ + refs trước khi tạo lại). ✅ Fix cả job race lẫn update cộng dồn.
   - B. Atomic job → Task 2 (DB::transaction). ✅
   - C. ShouldBeUnique optional → Task 4 (deferred). ✅
   - 69 bản ghi cũ → ngoài scope (script `fix-data-prod.sql`). ✅ (ghi rõ ở design)
   - Kiểm thử an toàn (không prod) → Task 3 + Global Constraints. ✅
2. **Placeholder scan:** không có TBD/TODO; mọi step code có code cụ thể; lệnh kiểm có expected. ✅
3. **Type consistency:** Task 2 phụ thuộc Task 1 (saveAccountsDetail idempotent) — nhất quán. `AccountDetail`/`AccountDetailRef` xác nhận import ở Task 1 Step 3. ✅
