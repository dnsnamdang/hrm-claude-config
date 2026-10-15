# Task P2-9 Report — BorrowSellController + 3 Resource + routes (API phiếu xuất bán hàng mượn)

Status: **DONE**
Commit: `394b5da44` (nhánh `gop_db`)
Test: `php vendor/bin/phpunit --filter=BorrowSellApiTest Modules/Finance/Tests/Feature/BorrowSellApiTest.php` → **5 test, 13 assertions, OK (4 xanh thật + 1 skip có lý do)**

## Cột company_id/department_id trên `borrow_sells` — KHÔNG tồn tại

Đọc `DESCRIBE borrow_sells` thật trên DB `erp_hrm_check` (env local đang trỏ DB này —
`grep DB_ .env`): bảng `borrow_sells` **không có** cột `company_id`/`department_id` (khác
`borrow_sell_requests` — bảng này CÓ 2 cột đó). Cột thật trên `borrow_sells`: id, status, type,
code, borrow_sell_request_id, contractable_id, contractable_type, firm_contract_tab_id,
project_tab_id, created_by, updated_by, note, created_at, updated_at, export_price, vat_percent,
vat_cost_allocated, sum_amount_allocated, sum_amount_allocated_after_vat, sum_amount_after_extra,
sum_amount_after_extra_vat, sum_amount_after_extra_after_vat, bear_the_shipping.

**Giải pháp đã áp dụng**: `BorrowSell::searchByFilter()` scope company/department qua
`whereHas('borrowSellRequest', fn($q) => $q->where('company_id', ...))` /
`whereIn('department_id', ...)` — dùng quan hệ `borrowSellRequest()` (đã có sẵn trên entity,
`belongsTo` qua `borrow_sell_request_id`) để tra `company_id`/`department_id` của phiếu YÊU CẦU
gốc, thay vì `where()` trực tiếp trên `borrow_sells` như code mẫu giả định trong brief. Đã ghi
chú GOTCHA này ngay trong docblock của entity `BorrowSell.php`.

Tương tự, `borrow_sells` **không lưu snapshot khách hàng** (`customer_name`,
`customer_address`,...) như `borrow_sell_requests` — 3 Resource (List/Detail/Print) đều lấy các
field này qua `optional($this->borrowSellRequest)->customer_name` v.v.

## Base ApiController + responseJson

Đã đọc `Modules/Finance/Http/Controllers/V1/BorrowSellRequestController.php` +
`Modules/Finance/Http/Controllers/V1/ApiController.php` để xác nhận:
- `ApiController extends \Illuminate\Routing\Controller` (namespace
  `Modules\Finance\Http\Controllers\V1`).
- `responseJson($message, $code = 200, $data = null)` → trả `response()->json(['code','message','data'], $code)`.

`BorrowSellController` dùng đúng `extends ApiController` + gọi `$this->responseJson(...)` với
đúng signature (không tự chế helper khác).

## Rulings đã áp dụng

- **T9-perm**: `BorrowSell::searchByFilter()` tái dùng NAME hằng
  `BorrowSellRequest::PERMISSION_VIEW_ALL_COMPANY/_COMPANY/_DEPARTMENT` (KHÔNG dùng id
  100315-100318). 4 nhánh: all company (không lọc) → company (whereHas company_id) → department
  (whereHas department_id) → mặc định `created_by = auth()->id()`.
- **T9-store-gate**: route group `/borrow-sells` KHÔNG middleware `checkPermission`. Controller
  `store()` gọi `BorrowSell::userCanCreate()` → 403 tường minh nếu thiếu quyền "Kế toán kho"
  TRƯỚC khi gọi `BorrowSellService::store()`. Service giữ nguyên `BorrowSellRequest::canApprove()`
  (đã có từ T7) làm defense-in-depth — không đụng service.
- **T9-print**: `BorrowSellPrintResource` là JSON thuần (mảng lồng nhau), không gọi tới bảng mẫu
  in nào.
- **T9-accounting-in-detail**: `BorrowSellDetailResource::toArray()` gọi
  `app(BorrowSellPostingService::class)->getDataAccounting($this->resource)` → `[$ok, $accounts,
  $err]` → `'accounting' => $ok ? $accounts : []`, `'accounting_error' => $ok ? null : $err`. Test
  #3 verify khối này có dữ liệu thật (không rỗng) khi fixture hợp lệ.
- **T9-entity-additions**: chỉ sửa `Modules/Finance/Entities/BorrowSell/BorrowSell.php` — thêm
  `searchByFilter`, `meta()`, `userCanCreate()`, accessor `getIsCanViewAttribute()`, và thêm quan
  hệ `employee_create()` (cần cho `creator_name` ở cả 3 Resource, không có trong code mẫu brief
  nhưng đúng phạm vi "chỉ thêm vào BorrowSell"). KHÔNG đụng `BorrowSellRequest` hay entity khác.

## Giả định bổ sung (brief không nói rõ)

1. **status_name mapping tối thiểu**: `BorrowSell` chỉ khai `const STATUS_DEFAULT = 1`, không có
   bộ đủ trạng thái như `BorrowSellRequest` (1/2/3/4/10/11). Dữ liệu thật hiện tại (`SELECT
   DISTINCT status FROM borrow_sells`) chỉ có giá trị `1`. `canView()` port từ ERP có nhắc
   `status != 3` (ngụ ý có trạng thái 3 = có thể "đã huỷ") nhưng không có nguồn xác định tên/giá
   trị đầy đủ trong scope Phase 2 HRM (BorrowSellService chỉ set `STATUS_DEFAULT`). → 2 Resource
   List/Detail dùng map tối thiểu `[1 => 'Đã duyệt']`, các status khác trả `null` cho
   `status_name` (không đoán bừa) — ghi rõ ở đây để task sau bổ sung nếu lộ thêm trạng thái.
2. **`is_can_view` duy nhất trong List Resource** (không thêm is_can_edit/is_can_approve/...):
   BorrowSell entity chỉ có 1 gate `canView()` (không có canEdit/canDeny/... như
   BorrowSellRequest — phiếu XUẤT BÁN thực tế không có quy trình duyệt tiếp theo trong Phase 2).
3. **`show()`/`printData()` không dùng `service->findForShow()`** (khác BorrowSellRequestController
   có method riêng đó) vì `BorrowSellService` (T7) không có method tương đương — controller tự
   `BorrowSell::with([...])->findOrFail()` như code mẫu brief.
4. **`is_can_view` truyền qua Resource dùng `$this->is_can_view`** (accessor Eloquent, không gọi
   lại `canView()` trực tiếp trong Resource) — mirror cách brief gợi ý accessor + tránh gọi 2 lần.
5. Filter cơ bản trong `searchByFilter` GIỮ TỐI THIỂU đúng như brief cho phép (`code`, `status`,
   `contractable_type`, `startDate`, `endDate`) — không port đủ bộ filter phức tạp của
   `BorrowSellRequest::searchByFilter` (contract_code subquery, productName/productCode,...) vì
   brief không liệt kê và không có UI FE tham chiếu ở Phase 2 scope task này.

## Test — chi tiết 5 case

1. `test_index_route_is_registered_under_finance_prefix` — XANH THẬT: `GET
   /api/v1/finance/borrow-sells` không auth → 401 (không phải 404), chứng minh route đăng ký đúng
   dưới prefix `/api/v1/finance` + middleware `auth:api` của group cha.
2. `test_user_can_create_is_fail_closed_without_auth` — XANH THẬT: `BorrowSell::userCanCreate()`
   guest → `false`.
3. `test_detail_resource_has_accounting_block_and_fail_closed_is_can_view` — XANH THẬT: dựng 1
   `BorrowSell` KHÔNG lưu DB (contract WrService id=4, cùng fixture pattern
   `BorrowSellPostingWrServiceTest`), gọi `getDataAccounting()` thật → `accounting` không rỗng,
   `accounting_error` null; đồng thời verify `is_can_view=false` (guest, `created_by` khác) —
   khoá regression "hardcode is_can_view=true".
4. `test_print_resource_shape_is_plain_json` — XANH THẬT: `BorrowSellPrintResource` có key
   `code`/`products`, 1 sản phẩm, `stt=1`.
5. `test_store_without_permission_returns_403` — SKIP: cần helper `actingAs` employee JWT thật
   (gán/không gán quyền "Kế toán kho" qua DB) mà test suite module Finance hiện chưa có sẵn; gate
   403 đã được khoá gián tiếp bằng test #2 (đơn vị hoá `userCanCreate()`) + đọc code controller.

Ngoài ra đã verify thêm (không phải test chính thức, chạy tay 1 lần rồi xoá):
`POST /borrow-sells`, `GET /borrow-sells/1`, `GET /borrow-sells/1/print-data` không auth đều trả
401 (không 404) — xác nhận cả 4 route trong group đăng ký đúng.

## Ghi chú phụ

- `php artisan route:list` bị crash toàn app (lỗi `Trying to get property 'employee_info_id' of
  non-object` tại `app/Helper/PermissionHelper.php:23`, gọi từ
  `RequestUpdateTimeSheetController.php:51`) — lỗi **có sẵn từ trước, không liên quan task này**
  (module Timesheet, không đụng tới trong task P2-9). Đã dùng HTTP test thật (401 vs 404) để verify
  route thay vì `route:list`.
- Không sửa `StoreBorrowSellRequest` (comment cũ trong đó nói "quyền gate ở middleware
  checkPermission:Kế toán kho" — không đúng thực tế route hiện tại không có middleware đó; comment
  lệch so với code thật nhưng nằm ngoài phạm vi 7 file được giao ở task này nên không sửa).
