# Task 8 — Report: Controller + 3 Resource + Routes (BorrowSellRequest)

## Files created/modified

1. **Modified** `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php`
   — thêm 4 public method (`findOrFail`, `findForShow`, `histories`, `searchContracts`), đặt giữa
   nhóm "deny/managerApprove/switchBoardOfManager/boardOfManagerApprove" và nhóm "Helpers" (private).
   Verbatim theo brief, không sửa method cũ.
2. **Created** `Modules/Finance/Http/Controllers/V1/BorrowSellRequestController.php` — verbatim brief.
3. **Created** `Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestListResource.php` — verbatim brief.
4. **Created** `Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestDetailResource.php` — verbatim brief.
5. **Created** `Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestPrintResource.php` — verbatim brief.
6. **Modified** `Modules/Finance/Routes/api.php`:
   - Thêm `use Modules\Finance\Http\Controllers\V1\BorrowSellRequestController;` (giữa `BillPaymentRequestController` và `CompanyAccountController`, gần nhóm `Bill*` — file không strict alphabetical toàn bộ nhưng khu vực này theo A→C).
   - Đã đọc 20 dòng đầu + nhiều group mẫu trước khi sửa: file dùng style `[Controller::class, 'method']` (KHÔNG string-action) → giữ nguyên style brief.
   - File có 1 outer group `Route::group(['prefix' => '/v1/finance', 'middleware' => 'auth:api'], function () {...})` bọc TOÀN BỘ các nhóm con (vd `/product-imports`, `/prepick-stocks`...). Route brief chỉ cho code `prefix => /borrow-sell-requests` KHÔNG có outer group — đã **nest đúng vào outer group hiện có** (prefix cha thật là `/v1/finance`, không phải `/api/finance` như brief đoán mơ hồ — verify bằng `route:list` output dưới, path đầy đủ là `api/v1/finance/borrow-sell-requests`). Đặt group mới NGAY TRƯỚC dấu đóng `});` cuối file (sau nhóm `/prepick-stocks`).
   - Thứ tự route giữ đúng: các route tĩnh (`/`, `/contracts`, `/contracts/{id}/borrow-sell-data`, `/{id}/deny`, `/{id}/manager-approve`, `/{id}/switch-board-of-manager`, `/{id}/board-of-manager-approve`, `/{id}/histories`, `/{id}/print-data`) đặt TRƯỚC `GET /{id}` (show) cuối cùng.

## Điểm lệch brief + cách resolve

- **Route file cần nest vào outer group `/v1/finance` (auth:api)** — brief chỉ đưa code group `/borrow-sell-requests` không kèm outer group, dễ hiểu nhầm là group độc lập ở root. Đã đọc file thật, xác nhận toàn bộ route Finance nằm trong 1 outer group duy nhất → đặt group mới bên trong outer group đó (giống mọi group khác trong file), KHÔNG tạo outer group riêng.
- **`use` cho `BorrowSellRequestController`** không có vị trí "chuẩn" duy nhất trong file (thứ tự use không strict alphabetical toàn cục, có nhiều đoạn xen kẽ không theo abc, vd `AdditionAccountingRequestController` nằm sau `ProductTransferRequestController`). Đã chọn chèn theo nhóm gần đúng vị trí abc cục bộ (giữa Bill* và Company*) — không ảnh hưởng chức năng, chỉ là style.
- Không phát hiện cột thiếu hay sai lệch nào khác so với brief — mọi cột/relation/const dùng đúng như FACT đã trace.

## Verify

### 1. `php -l` (6 file)

```
== Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php ==
No syntax errors detected
== Modules/Finance/Http/Controllers/V1/BorrowSellRequestController.php ==
No syntax errors detected
== Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestListResource.php ==
No syntax errors detected
== Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestDetailResource.php ==
No syntax errors detected
== Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestPrintResource.php ==
No syntax errors detected
== Modules/Finance/Routes/api.php ==
No syntax errors detected
```

### 2. `composer dump-autoload -o`

```
Generated optimized autoload files containing 12327 classes
```
(thành công, không lỗi)

### 3. Tinker — class_exists / method_exists

```
Controller: bool(true)
List: bool(true)
Detail: bool(true)
Print: bool(true)
searchContracts: bool(true)
findOrFail: bool(true)
findForShow: bool(true)
histories: bool(true)
```

### 4. `php artisan route:list --path=borrow-sell-requests`

**Lệch quy trình verify:** `php artisan route:list` (mọi path, kể cả path pre-existing `product-imports` không đụng tới trong task này) CRASH trong môi trường này với lỗi:
```
ErrorException: Trying to get property 'employee_info_id' of non-object
at app/Helper/PermissionHelper.php:23
called from Modules/Timesheet/Http/Controllers/Api/V1/RequestUpdateTimeSheetController.php:51
```
Đây là bug PRE-EXISTING không liên quan Task 8 — `RequestUpdateTimeSheetController::__construct()` (module Timesheet, không đụng trong task này) gọi `isCurrentEmployeeHasPermission()` NGAY TRONG constructor, hàm này truy cập `auth()->user()->employee_info_id` — vỡ khi chạy CLI không có user đăng nhập. Đã verify KHÔNG PHẢI do thay đổi của task này bằng cách chạy `route:list --path=product-imports` (route đã tồn tại từ trước, không đụng) → CRASH giống hệt. Đã thử `route:clear` + `config:clear` → không khắc phục được (lỗi runtime, không phải cache).

**Workaround verify tương đương** — dump route qua `Route::getRoutes()` (không trigger controller resolve):
```
GET|HEAD api/v1/finance/borrow-sell-requests -> ...Controller@index
GET|HEAD api/v1/finance/borrow-sell-requests/contracts -> ...Controller@contracts
GET|HEAD api/v1/finance/borrow-sell-requests/contracts/{id}/borrow-sell-data -> ...Controller@contractBorrowSellData
POST api/v1/finance/borrow-sell-requests -> ...Controller@store
POST api/v1/finance/borrow-sell-requests/{id}/deny -> ...Controller@deny
POST api/v1/finance/borrow-sell-requests/{id}/manager-approve -> ...Controller@managerApprove
POST api/v1/finance/borrow-sell-requests/{id}/switch-board-of-manager -> ...Controller@switchBoardOfManager
POST api/v1/finance/borrow-sell-requests/{id}/board-of-manager-approve -> ...Controller@boardOfManagerApprove
GET|HEAD api/v1/finance/borrow-sell-requests/{id}/histories -> ...Controller@histories
GET|HEAD api/v1/finance/borrow-sell-requests/{id}/print-data -> ...Controller@printData
GET|HEAD api/v1/finance/borrow-sell-requests/{id} -> ...Controller@show
```
Đủ 11 route, `GET /{id}` (show) nằm DƯỚI mọi route tĩnh. Full path xác nhận outer prefix thật là `api/v1/finance` (khớp middleware `auth:api`).

### 5. Smoke test THẬT (chỉ đọc)

```
searchContracts type=array count=40
```
(company_id null trong context CLI không đăng nhập → không lọc theo company, trả cả 2 loại HĐ, không lỗi)

```
detail OK keys=id,code,type,type_name,status
print OK
```
(có phiếu sẵn trong DB — `with(['products.details','tabs'])->first()` → cả 2 Resource `toArray()` chạy KHÔNG throw)

```
paginate OK total=0
list toArray OK count=0
meta={"canViewAllCompany":false,"canViewCompany":false,"canViewDepartment":false,"isKeToanKho":false,"isTP":false,"isBGD":false}
```
`total=0` là ĐÚNG hành vi fail-closed (R5): không có `auth()->id()` trong context CLI → nhánh else của `searchByFilter` (`where('created_by', auth()->id())`) không match gì → 0 kết quả, KHÔNG lỗi. `meta()` trả toàn `false` (fail-closed) đúng như thiết kế khi không có user.

## STATUS

DONE

## Verify tổng (1 dòng)

php -l 6 file OK, dump-autoload OK, class/method_exists OK (8/8 true), 11/11 route đúng thứ tự (verify qua Route::getRoutes() do route:list bị crash bởi bug pre-existing ở module Timesheet không liên quan), smoke test đọc (searchContracts/Detail/Print/searchByFilter+paginate/meta) chạy không lỗi.

## Concerns

- `php artisan route:list` bị crash TOÀN CỤC (không riêng route mới) do bug pre-existing ở `RequestUpdateTimeSheetController::__construct()` (module Timesheet) gọi permission-check ngay trong constructor, vỡ khi CLI không có auth user. KHÔNG liên quan Task 8, không sửa trong phạm vi task này (ngoài scope, đụng module khác) — nên báo để controller/dev khác biết nếu cần fix riêng.
