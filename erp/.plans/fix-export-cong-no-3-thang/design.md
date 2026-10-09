# Design — Bỏ giới hạn 3 tháng khi export báo cáo công nợ khách hàng

## Vấn đề (user báo)
Xuất Excel 3 báo cáo công nợ KH bị giới hạn 3 tháng, không xuất được đúng khoảng thời gian search.

## Điều tra (kết quả)
Giới hạn 3 tháng là **guard JavaScript trên nút Export** (không phải BE), và **CHỈ tồn tại ở 1/3 báo cáo**:

| Báo cáo | Blade | Guard 3 tháng? |
|---|---|---|
| `customer-debt-details` | `sale/sale_reports/customer-debt-details.blade.php:309-321` | **CÓ** — chặn nếu `endDate >= startDate + 3 tháng` |
| `customer-debt-detail-by-employee` | `...customer-debt-detail-by-employee.blade.php:362-370` | KHÔNG (export thẳng theo range search) |
| `compare-customer-debts` | `...compare-customer-debts.blade.php:359-366` | KHÔNG (chỉ check đủ điều kiện bắt buộc) |

→ Chỉ `customer-debt-details` bị chặn. 2 báo cáo kia vốn đã export đúng range search.

## An toàn khi bỏ
Export `customer-debt-details` chạy **async qua Mail Job** (`SaleReportsController::exportCustomerDebtDetails` → `CustomerDebtDetailsMailJob`, đã `ini_set memory 1024M` + `set_time_limit 3600`) → range dài xử lý nền, không treo trình duyệt. Bỏ guard an toàn.

## Nguyên nhân timeout (điều tra sâu — vì sao mới chặn 3 tháng)
`SaleReportsController::exportCustomerDebtDetails` chạy **2 query nặng ĐỒNG BỘ trong web request** trước khi dispatch job (dòng 252-253):
```php
$summary = AccountDetail::getReportSummary($request);    // nặng, SYNC
$dept_begin = AccountDetail::getDeptBegin($request, 21);  // nặng, SYNC
CustomerDebtDetailsMailJob::dispatch($user, $type, $summary, $dept_begin, $request->all());
```
→ Range dài → 2 query timeout ngay trong request. (Báo cáo by-employee không bị vì job tự query hết → async.)
`getReportSummary($request)` dùng `$request->startDate` (object). Job có `$timeout=60000`. **Prod chạy queue async (worker) — user xác nhận.**

## Giải pháp (đã chốt: phương án a — 2 phần)
**Phần 1 (BE — bỏ nguyên nhân timeout):** Chuyển `getReportSummary` + `getDeptBegin` từ controller vào `CustomerDebtDetailsMailJob::handle()` (job làm hết, async giống by-employee). Controller chỉ `dispatch($user, $type, $request->all())`. Đổi constructor job `($user, $type, $data_request)`. Trong handle dựng `new Request($this->request)` để gọi getReportSummary/getDeptBegin (không sửa hàm dùng chung).

**Phần 2 (FE — bỏ giới hạn):** Bỏ hẳn guard 3 tháng ở `customer-debt-details.blade.php` — nút export mở thẳng URL export theo range search (giống 2 báo cáo kia).

**Trước (dòng 309-321):**
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
**Sau:**
```js
$(document).on('click', '.export-button', function(event) {
    event.preventDefault();
    window.open($(this).data('href') + "?" + $.param($scope.form) + '&per_page=9999999999', "_blank");
})
```

## Phạm vi
- `resources/views/sale/sale_reports/customer-debt-details.blade.php` (bỏ guard 3 tháng).
- `app/Http/Controllers/Sale/SaleReportsController.php::exportCustomerDebtDetails` (chỉ dispatch request).
- `app/Jobs/CustomerDebtDetailsMailJob.php` (constructor + handle tự tính summary/dept_begin).
- 2 báo cáo kia (`compare-customer-debts`, `customer-debt-detail-by-employee`): KHÔNG đổi (đã đúng, đã async / không giới hạn).

## Không làm
- Không sửa hàm dùng chung `getReportSummary`/`getDeptBegin` (chỉ dời chỗ gọi + dựng Request trong job).
- Không đổi logic tính toán/kết quả báo cáo.

## Điều kiện
- Prod chạy queue async (worker) — đã xác nhận. Nếu 1 ngày chuyển sang sync thì cần tối ưu query thêm.

## Branch
Xác nhận với user (hiện đang ở `master`).
