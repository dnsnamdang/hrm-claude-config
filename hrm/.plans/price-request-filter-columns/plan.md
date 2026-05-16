# Plan: Thêm filter + cột thương hiệu, hãng sản xuất vào danh sách YCHG / YCTG / Phiếu tính giá

## Trạng thái
- Bắt đầu: 2026-04-13
- Tiến độ: 11/12 task ✅ (uncommitted), chờ manual test

## Phase 1: Model — thêm relationship + filter

### PriceAskingRequest.php
- [x] Task 1: Thêm `brand()` belongsTo Brand, `manufacture()` belongsTo Manufacture + eager load trong searchByFilter
- [x] Task 2: Thêm filter `manufacture_id` trong `searchByFilter()`

### PriceCalculateRequest.php
- [x] Task 3: Thêm `brand()` belongsTo Brand, `manufacture()` belongsTo Manufacture + eager load
- [x] Task 4: Thêm filter `brand_id`, `manufacture_id`, `asking_department_id`, `asking_created_by` trong `searchByFilter()`

### PriceCalculate.php
- [x] Task 5: Thêm filter `brand_id`, `manufacture_id`, `calculate_department_id`, `price_asking_request`, `asking_department_id` trong `searchByFilter()`. Eager load brand/manufacture qua price_calculate_request

## Phase 2: Controller — thêm addColumn

- [x] Task 6: `PriceAskingRequestController::searchData()` — addColumn `brand_name`, `manufacture_name`
- [x] Task 7: `PriceCalculateRequestController::searchData()` — addColumn `brand_name`, `manufacture_name`
- [x] Task 8: `PriceCalculateController::searchData()` — addColumn `brand_name`, `manufacture_name` (qua price_calculate_request)

## Phase 3: View — thêm search_columns + columns

- [x] Task 9: `price_asking_requests/index.blade.php` — thêm search_column `manufacture_id` + 2 columns brand_name, manufacture_name
- [x] Task 10: `price_calculate_requests/index.blade.php` — thêm search_columns brand_id, manufacture_id, asking_department_id, asking_created_by + 2 columns
- [x] Task 11: `price_calculates/index.blade.php` — thêm search_columns brand_id, manufacture_id, calculate_department_id, price_asking_request, asking_department_id + 2 columns

## Phase 4: Manual test

- [ ] Task 12: Test cả 3 screens: filter hoạt động, cột hiển đúng tên, không lỗi JS

## Checkpoint

### Checkpoint — 2026-04-13
Vừa hoàn thành: 11/12 task code — 9 files, 142 insertions
- 3 models: relationships brand/manufacture, eager load, filters (manufacture, brand, department, employee qua YCHG/YCTG chain)
- 3 controllers: addColumn brand_name, manufacture_name
- 3 views: search_columns + datatable columns
Đang làm dở: Chờ user manual test + tự commit
Bước tiếp theo: User test → commit → báo lại
Blocked: không
