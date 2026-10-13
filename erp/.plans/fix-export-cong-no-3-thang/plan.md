# Bỏ giới hạn 3 tháng export báo cáo công nợ KH — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Export báo cáo chi tiết công nợ KH (`customer-debt-details`) theo đúng khoảng thời gian search, không còn giới hạn 3 tháng; đồng thời bỏ nguyên nhân timeout (đưa query nặng vào job async).

**Architecture:** (1) Chuyển `getReportSummary` + `getDeptBegin` từ controller vào `CustomerDebtDetailsMailJob::handle()` → export chạy hoàn toàn async (giống report by-employee). (2) Bỏ guard JS 3 tháng ở blade.

**Tech Stack:** PHP 7.4 / Laravel 6, queue async (prod có worker), Blade + jQuery.

## Global Constraints

- KHÔNG commit/push khi user chưa yêu cầu.
- KHÔNG đọc/sửa `vendor/`, `node_modules/`.
- Branch: `master` (user chốt).
- KHÔNG sửa hàm dùng chung `AccountDetail::getReportSummary`/`getDeptBegin` — chỉ dời chỗ gọi + dựng `Request` trong job.
- Prod queue async (worker) — đã xác nhận; đây là điều kiện để hết timeout.
- 2 báo cáo kia (`compare-customer-debts`, `customer-debt-detail-by-employee`) KHÔNG đổi.

---

## File Structure
- **Modify** `app/Http/Controllers/Sale/SaleReportsController.php::exportCustomerDebtDetails` (~247-260) — chỉ dispatch request.
- **Modify** `app/Jobs/CustomerDebtDetailsMailJob.php` — constructor `($user,$type,$data_request)` + handle tự tính summary/dept_begin.
- **Modify** `resources/views/sale/sale_reports/customer-debt-details.blade.php` (309-321) — bỏ guard 3 tháng.

---

### Task 1: BE — đưa 2 query nặng vào job (async), controller chỉ dispatch

**Files:**
- Modify: `app/Http/Controllers/Sale/SaleReportsController.php` (~247-260)
- Modify: `app/Jobs/CustomerDebtDetailsMailJob.php` (constructor 40-47, handle 54-58, props 32-33)

**Interfaces:**
- `CustomerDebtDetailsMailJob::__construct($user, $type, $data_request)` (bỏ 2 tham số `$summary`, `$dept_begin`).
- `AccountDetail::getReportSummary($request)` + `getDeptBegin($request, 21)` — dùng `$request->startDate` (cần object) → job dựng `new \Illuminate\Http\Request($this->request)`.
- `getReportData($this->request)` giữ nguyên (dùng array access).

- [x] **Step 1: Controller chỉ dispatch request**

Thay `exportCustomerDebtDetails` (dòng 247-260):

```php
    public function exportCustomerDebtDetails(Request $request)
    {
        $type = $request->type ?: 'debt_detail';

        $user = auth()->user();
        $summary = AccountDetail::getReportSummary($request);
        $dept_begin = AccountDetail::getDeptBegin($request, 21);
        CustomerDebtDetailsMailJob::dispatch($user, $type, $summary->toArray(), $dept_begin, $request->all());
        $message = array(
            "message" => "Báo cáo chi tiết công nợ khách hàng sẽ gửi về mail của bạn trong ít phút!",
            "alert-type" => "success"
        );
        return redirect()->back()->with($message);
    }
```

bằng:

```php
    public function exportCustomerDebtDetails(Request $request)
    {
        $type = $request->type ?: 'debt_detail';

        $user = auth()->user();
        // Đẩy toàn bộ query nặng (summary + dept_begin) vào job async để tránh timeout web request.
        CustomerDebtDetailsMailJob::dispatch($user, $type, $request->all());
        $message = array(
            "message" => "Báo cáo chi tiết công nợ khách hàng sẽ gửi về mail của bạn trong ít phút!",
            "alert-type" => "success"
        );
        return redirect()->back()->with($message);
    }
```

- [x] **Step 2: Job — đổi constructor (bỏ summary/dept_begin)**

Trong `app/Jobs/CustomerDebtDetailsMailJob.php`, thay constructor (dòng 40-47):

```php
    public function __construct($user, $type, $summary, $dept_begin, $data_request)
    {
        $this->user = $user;
        $this->type = $type;
        $this->request = $data_request;
        $this->summary = $summary;
        $this->dept_begin = $dept_begin;
    }
```

bằng:

```php
    public function __construct($user, $type, $data_request)
    {
        $this->user = $user;
        $this->type = $type;
        $this->request = $data_request;
    }
```

- [x] **Step 3: Job — handle tự tính summary/dept_begin**

Thay đầu `handle()` (dòng 54-58):

```php
    public function handle()
    {
        $data = $this->getReportData($this->request);
        $data['summary'] = $this->summary;
        $data['dept_begin'] = $this->dept_begin;
```

bằng:

```php
    public function handle()
    {
        $request = new \Illuminate\Http\Request($this->request);
        $summary = AccountDetail::getReportSummary($request);
        $dept_begin = AccountDetail::getDeptBegin($request, 21);

        $data = $this->getReportData($this->request);
        $data['summary'] = $summary->toArray();
        $data['dept_begin'] = $dept_begin;
```

- [x] **Step 4: Job — xóa 2 property không còn dùng**

Xóa 2 dòng khai báo property (dòng 32-33):

```php
    protected $summary;
    protected $dept_begin;
```

(giữ lại `protected $user; $type; $request;`)

- [x] **Step 5: Lint** (php -l sạch)

Run: `php -l app/Http/Controllers/Sale/SaleReportsController.php && php -l app/Jobs/CustomerDebtDetailsMailJob.php`
Expected: `No syntax errors detected` cả 2.

- [ ] **Step 6: Commit** (chỉ khi user yêu cầu)

```bash
git add app/Http/Controllers/Sale/SaleReportsController.php app/Jobs/CustomerDebtDetailsMailJob.php
git commit -m "perf(report): đưa query summary/dept_begin của export công nợ KH vào job async"
```

---

### Task 2: FE — bỏ guard 3 tháng trên nút export

**Files:**
- Modify: `resources/views/sale/sale_reports/customer-debt-details.blade.php` (309-321)

- [x] **Step 1: Bỏ guard**

Thay handler `.export-button` (dòng 309-321):

```js
            $(document).on('click', '.export-button', function(event) {
                event.preventDefault();
                const startDate = new Date($scope.form.startDate);
                const endDate = new Date($scope.form.endDate);
                const threeMonthsLater = new Date(startDate);
                threeMonthsLater.setMonth(threeMonthsLater.getMonth() + 3);

                if (endDate < threeMonthsLater) {
                    window.open($(this).data('href') + "?" + $.param($scope.form) + '&per_page=9999999999', "_blank");
                } else {
                    toastr.warning('Khoảng thời gian không được quá 3 tháng');
                }
            })
```

bằng:

```js
            $(document).on('click', '.export-button', function(event) {
                event.preventDefault();
                window.open($(this).data('href') + "?" + $.param($scope.form) + '&per_page=9999999999', "_blank");
            })
```

- [ ] **Step 2: Kiểm thử thủ công (dev)**

Trên dev (queue chạy async): mở báo cáo `customer-debt-details`, chọn range > 3 tháng → bấm Export → KHÔNG còn toast "không được quá 3 tháng"; nhận thông báo "sẽ gửi về mail"; mail nhận được file đúng range. Kiểm web request trả nhanh (không treo do query nặng).

- [ ] **Step 3: Commit** (chỉ khi user yêu cầu)

```bash
git add resources/views/sale/sale_reports/customer-debt-details.blade.php
git commit -m "fix(report): bỏ giới hạn 3 tháng khi export chi tiết công nợ KH"
```

---

## Follow-up fix (regression sau khi dời query vào job)

### Checkpoint — 2026-07-01
Lỗi phát sinh khi test: `Call to a member function can() on null` (AccountDetail:1498) — `getReportSummary` dùng `auth()->user()->can()` mà **queue worker không có auth**. Do dời hàm từ controller (có auth) vào job.
Fix: thêm `auth()->setUser($this->user);` ở đầu `CustomerDebtDetailsMailJob::handle()` (trước getReportSummary/getDeptBegin). Không sửa hàm dùng chung.
Verify: php -l sạch; tinker prod setUser(Employee 13) → getReportSummary chạy OK không throw.

- [x] BE follow-up: `auth()->setUser($this->user)` trong job (fix can() on null)

## Self-Review

1. **Spec coverage:**
   - Bỏ nguyên nhân timeout (query nặng vào job async) → Task 1. ✅
   - Bỏ giới hạn 3 tháng FE → Task 2. ✅
   - Không sửa getReportSummary/getDeptBegin → job dựng Request gọi, không đổi hàm. ✅
   - 2 báo cáo kia không đổi → không có task. ✅
2. **Placeholder scan:** không TBD/TODO; mọi step có code + lệnh + expected. ✅
3. **Type consistency:** constructor mới `($user,$type,$data_request)` khớp lời gọi ở controller (Task 1 Step 1). `$summary->toArray()` khớp việc handle dùng array `$data['summary']`. ✅

### Checkpoint — 2026-07-01 (regression #2)
Lỗi tiếp: `Call to a member function parameters() on null` — getDeptBegin dùng array-access $request['x'] → Request::offsetExists cần route()->parameters(); worker không có route.
Fix: gắn $request->setRouteResolver (Route GET / bind) cho request dựng trong job.
Verify: prod reproduce getReportSummary + getDeptBegin đều OK; php -l sạch.
Tổng 2 regression đã fix (đều do dời query vào job): (1) setUser cho can(); (2) route resolver cho offsetExists.
