# Task 5 — DashboardRequest + DashboardController + Route

## File tạo/sửa

- **Tạo** `nhatlinh-api/Modules/Warehouse/Http/Requests/DashboardRequest.php`
- **Tạo** `nhatlinh-api/Modules/Warehouse/Http/Controllers/Api/V1/DashboardController.php`
- **Sửa** `nhatlinh-api/Modules/Warehouse/Routes/api.php` (thêm import `DashboardController` + route `GET /dashboard` đặt trên cùng group, trước `/receipts`)

## Kiểu response đã chọn + lý do khớp WhReportController

Đọc `WhReportController` (dùng cho mọi endpoint đọc kho khác) thấy pattern chuẩn của module:
- Controller **extends `App\Http\Controllers\ApiController`** (không phải `Illuminate\Routing\Controller` trần), dùng `try/catch (\Exception $e)` bọc quanh gọi service, `Log::error($e)` khi lỗi.
- Response thành công dùng `$this->responseJson('success', Response::HTTP_OK, $data)` (xem method `stockCard()` — case tương tự dashboard: 1 object tổng hợp, không phân trang).
- Response lỗi dùng `$this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST)`.

→ `DashboardController` viết theo đúng pattern này thay vì `response()->json(['data'=>...])` như snippet gợi ý trong plan, để đồng nhất format `{code, message, data}` toàn bộ API kho (`ApiController::responseJson`).

Với `DashboardRequest`: các Request khác trong `Modules/Warehouse/Http/Requests` (`WhIssueRequest`, `WhReceiptRequest`, `WhTransferRequest`) đều **extends `Modules\Training\Http\Requests\BaseRequest`** (đã có sẵn `authorize() => true` + `failedValidation()` rethrow `ValidationException` với payload `{code, errors}` chuẩn 422 — đúng convention CLAUDE.md). Dùng lại `BaseRequest` thay vì `Illuminate\Foundation\Http\FormRequest` trần (snippet plan) để đồng nhất với các Request khác cùng module và tự động có xử lý lỗi validate đúng chuẩn.

## Output verify

- `php -l` cho cả 3 file: **No syntax errors detected** (bỏ qua warning `imagick.so` — lỗi môi trường có sẵn, không liên quan).
- `php artisan route:list --path=warehouse/dashboard` **KHÔNG chạy được** — toàn bộ lệnh `route:list` crash với `BindingResolutionException: Target class [Modules\Decision\Http\Controllers\DecisionController] does not exist` (lỗi pre-existing ở route Decision module, namespace đúng phải là `...Http\Controllers\V1\DecisionController`; không liên quan Task 5, xác nhận qua `find` thấy file thật nằm ở `V1/DecisionController.php`).
- Verify thay thế qua tinker (duyệt `Route::getRoutes()` lọc uri chứa `warehouse/dashboard`):
  ```
  GET|HEAD api/v1/warehouse/dashboard middleware=api,auth:api,checkPermission:Xem dashboard kho
  ```
  → Route đăng ký đúng, đủ middleware `auth:api` + `checkPermission:Xem dashboard kho`.
- Tinker smoke test `WhDashboardService::getData(['granularity'=>'month'])` → trả đủ 6 khoá: `kpis, movement_by_time, top_export, top_import, low_stock, stock_by_warehouse`.
- **HTTP E2E: bỏ qua** — không có server dev đang chạy (thử `localhost`, `127.0.0.1`, cổng 8000, cổng 80 đều 404) và không có token dev sẵn có trong phạm vi task.

## Concerns

- `php artisan route:list` (không path filter) hiện đang **crash toàn cục** do bug pre-existing ở `Modules/Decision/Routes` (namespace controller sai). Không phải do Task 5 gây ra (đã verify route Warehouse dashboard đăng ký đúng qua cách khác), nhưng nên báo để đội Decision fix riêng — hiện `artisan route:list` không dùng được cho toàn bộ dự án cho tới khi fix.
- Không verify được HTTP 200/401/403 thực tế do thiếu server + token dev trong môi trường này.
