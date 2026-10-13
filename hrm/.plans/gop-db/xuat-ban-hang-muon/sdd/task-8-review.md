# Task 8 Review — Controller + 3 Resource + 4 Service method + Routes

## SPEC COMPLIANCE: ✅
## QUALITY: APPROVED

Đã đọc brief, report, review package, và verify trực tiếp file thật (`Modules/Finance/Routes/api.php` dòng 42, 744-760) để xác nhận nesting route đúng như report claim (package chỉ có grep rời rạc không đủ context).

## Kiểm tra theo checklist

- **PHP 7.4, không constructor property promotion:** `BorrowSellRequestController::__construct` khai `private $service; private $source;` tường minh, gán trong body. Đúng.
- **Cờ quyền fail-closed:** mọi `is_can_*` (List + Detail Resource) gọi thẳng `canX()` trên entity item — không có `= true` hard-code nào. `meta()` gọi qua `BorrowSellRequest::meta()` (static entity, fail-closed theo T6). Đúng.
- **Gate quyền ở controller:** show/printData check `canView()`; deny check `canDeny()`; managerApprove/switchBoardOfManager check `canManagerApprove()` (switchBoardOfManager dùng cùng gate với managerApprove — đúng NHƯ BRIEF quy định verbatim, không phải lỗi implementer); boardOfManagerApprove check `canBoardOfManagerApprove()`; histories check `canView()`. Không sót action nào trong danh sách global constraint yêu cầu. `contracts`/`contractBorrowSellData`/`store` không gate thêm ở controller — đúng R2/R4 (store gate qua FormRequest T7, ngoài phạm vi T8).
- **searchByFilter/meta qua ENTITY static, không qua `$this->service`:** `index()` gọi `BorrowSellRequest::searchByFilter($request)->paginate((int) $request->get('per_page', 20))` — đúng, có paginate vì searchByFilter trả builder.
- **Không dùng mysql2/DB_CONNECTION_SECOND:** `DB::table('firm_contracts')`/`DB::table('wr_service_contracts')` dùng connection mặc định (không `::connection('mysql2')`). Đúng, khớp ruling.
- **Route order + nesting:** verify trực tiếp file thật — group `/borrow-sell-requests` nằm TRONG outer group `Route::group(['prefix' => '/v1/finance', 'middleware' => 'auth:api'], ...)` (dòng 42), đặt ngay trước `});` đóng outer group cuối file (dòng 744-760). 11 route, `GET /{id}` (show) là route cuối cùng, sau mọi route tĩnh (`/contracts`, `/contracts/{id}/borrow-sell-data`, `/{id}/deny`, `/{id}/manager-approve`, `/{id}/switch-board-of-manager`, `/{id}/board-of-manager-approve`, `/{id}/histories`, `/{id}/print-data`). Không có route trùng/nuốt nhau. Đúng.

## Đặc biệt soi

- **N+1 / null-safety `contractable_type`:** List Resource batch-query `firm_contracts`/`wr_service_contracts` theo `contractable_id` unique, tránh N+1; nếu `contractable_type` không khớp CONTRACT_FIRM/CONTRACT_WR_SERVICE (lý thuyết không xảy ra vì cột NOT set khác) thì rơi vào nhánh `else` tra `wrCodes` — không throw, chỉ trả `null` nếu id không có trong map (`?? null`). An toàn.
- **`optional(optional($item->employee_create)->info)->fullname`:** an toàn khi `employee_create` null (double `optional()` chain) — không throw.
- **Resource `->map()->values()` trên relation:** show/printData đều gọi `service->findForShow()` → `with(['products.details', 'tabs'])->findOrFail()` — eager loaded, không N+1. deny/managerApprove/switchBoardOfManager/boardOfManagerApprove/histories dùng `findOrFail()` (không eager) nhưng KHÔNG trả Resource nào dùng `products`/`tabs` — an toàn, khớp brief.
- **Fail-open dữ liệu nhạy cảm:** xác nhận cả 3 Resource (List/Detail/Print) KHÔNG có trường giá vốn/lương/rebate_price/allocated_price/net_price/export_price — chỉ field hiển thị cơ bản. Đúng Phase 1 scope.
- **Route trùng/nuốt:** không có, đã verify ở trên bằng cả report (Route::getRoutes() workaround do route:list bị crash bởi bug pre-existing module Timesheet — không liên quan T8) và đọc file thật.

## Finding

Không có finding BLOCKING. Không có finding NON-BLOCKING đáng kể — code khớp brief verbatim (đã diff trực tiếp package vs brief, giống hệt).

## Bất đồng ruling

Không có.

## Ghi chú phụ

- Report có nêu 1 vấn đề môi trường ngoài phạm vi T8 (`php artisan route:list` crash toàn cục do `RequestUpdateTimeSheetController::__construct()` module Timesheet gọi `isCurrentEmployeeHasPermission()` trong constructor, vỡ khi CLI không có auth user) — đã tự verify không liên quan thay đổi T8 (route pre-existing `product-imports` cũng crash giống hệt), dùng `Route::getRoutes()` làm workaround hợp lý. Không cần xử lý trong T8, nên báo cho dev khác biết nếu cần fix riêng module Timesheet.
