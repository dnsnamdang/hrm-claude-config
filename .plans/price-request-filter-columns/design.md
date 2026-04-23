# Design: Thêm filter + cột thương hiệu, hãng sản xuất vào danh sách YCHG / YCTG / Phiếu tính giá

## Bối cảnh

3 danh sách trong module Order (TanPhatDev) cần bổ sung filter và cột hiển thị thương hiệu (brand), hãng sản xuất (manufacture). Ngoài ra screen 2 + 3 cần thêm các filter liên quan phiếu YCHG/YCTG/phòng/người tạo.

## Thay đổi

### Screen 1 — Yêu cầu hỏi giá (`price_asking_requests`)

- `PriceAskingRequest.php`: thêm relationship `brand()` belongsTo Brand, `manufacture()` belongsTo Manufacture. Thêm filter `manufacture_id` trong `searchByFilter()`
- `PriceAskingRequestController.php`: thêm `editColumn` cho `brand_name`, `manufacture_name` trong `searchData()`
- `price_asking_requests/index.blade.php`: thêm search_column `manufacture_id` (select, `Manufacture::getForSelect()`). Thêm 2 column `brand_name`, `manufacture_name`. Filter `brand_id` đã có → giữ nguyên

### Screen 2 — Yêu cầu tính giá (`price_calculate_requests`)

- `PriceCalculateRequest.php`: thêm relationship `brand()`, `manufacture()`. Thêm filters trong `searchByFilter()`: `brand_id`, `manufacture_id`, `price_asking_request` (code YCHG), `asking_department_id` (phòng YCHG, join qua price_asking_request), `asking_created_by` (người tạo YCHG, join qua price_asking_request)
- `PriceCalculateRequestController.php`: thêm `editColumn` cho `brand_name`, `manufacture_name`
- `price_calculate_requests/index.blade.php`: thêm 5 search_columns (brand_id select, manufacture_id select, price_asking_request text đã có → giữ nguyên, asking_department_id select `Department::getForSelectAll()`, asking_created_by select-ajax) + 2 columns

### Screen 3 — Phiếu tính giá (`price_calculates`)

- `PriceCalculate::searchByFilter()`: thêm filters `brand_id`, `manufacture_id` (join qua `price_calculate_request`), `calculate_department_id` (phòng YCTG), `price_asking_request` (code YCHG, join qua chain), `asking_department_id` (phòng YCHG, join qua chain)
- `PriceCalculateController.php`: thêm `editColumn` cho `brand_name`, `manufacture_name` (lấy qua `price_calculate_request.brand_id` / `manufacture_id`)
- `price_calculates/index.blade.php`: thêm search_columns + 2 columns. Filter `price_calculate_request` text đã có → giữ nguyên

## Không thay đổi

- Migration / DB — fields `brand_id`, `manufacture_id` đã có trên `price_asking_requests` + `price_calculate_requests`
- Model `Brand`, `Manufacture` — đã có `getForSelect()`, dùng luôn
- Logic create/edit/show/form — không đụng
- Filter brand hiện có trên screen 1 (qua Product) — giữ nguyên
