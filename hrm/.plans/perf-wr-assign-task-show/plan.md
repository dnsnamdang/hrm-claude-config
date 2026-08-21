# Plan — Tối ưu tốc độ xem chi tiết phiếu giao công tác (WrAssignTask show)

Bối cảnh: `GET /api/v1/wr-assign-tasks/{id}` bên HRM chỉ proxy sang ERP
`/hrm/wr_assign_tasks/{id}/apiShow`. Toàn bộ thời gian nằm trong
`WrAssignTask::getForDataImportResult()` → `Customer::getListProductOfCustomer()` (ERP).

## Phase 1 — Tối ưu `Customer::getListProductOfCustomer` (ERP, repo TanPhatDev)

- [x] Đo baseline: task 37 (KH 199 hàng hoá) = 10,4s / 263 query / OOM ở memory_limit 128M
- [x] Index hoá `getUnitAndErrors`: bỏ quét tuyến tính collection 31.826 dòng cho từng hàng hoá (−3,5s)
- [x] Gom N+1 serial thành 2 query gộp (nhóm tp/tpc và nhóm ncck) (−2,0s, −197 query)
- [x] Lọc `DeviceErrorProduct` / `DeviceError` theo product_id liên quan thay vì nạp cả bảng (−1,3s, −50MB)
- [x] Đối chiếu output cũ/mới bằng dump JSON — giống hệt từng byte (customer 33601, 43478; task 37, 14580)
- [x] Differential test rộng: 71 khách hàng đa dạng (ncck / tpc / thiết bị cũ / KH rỗng / nhiều serial)
      → byte-identical, kể cả thứ tự phần tử và class của collection
- [x] Differential test tầng `getForDataImportResult`: 45 phiếu (HĐ dịch vụ / lắp đặt / việc khác / phiếu con)
      → byte-identical
- [x] Sửa 2 lỗi do differential test phát hiện:
      (a) `where('cot', null)` trong Laravel dịch thành `IS NULL` (không phải `= NULL`) → bản gộp query
          ban đầu bỏ sót serial ncck có `product_no_sale_name` NULL (17 dòng);
      (b) `device_errors` phải là `Support\Collection` (bản cũ dựng qua `collect()`), không phải Eloquent Collection

## Phase 2 — HRM (repo hrm-api)

- [x] Thêm `connect_timeout` / `timeout` cho Guzzle trong `TpWrAssignTaskService::show()`

## Chờ quyết định

- [ ] Truyền `$product_ids` để chỉ tính hàng hoá có trong phiếu (đổi chữ ký hàm dùng chung, 7 caller)
      — sau Phase 1 chỉ còn lợi ~10%, đang đề nghị bỏ

### Checkpoint — 2026-08-05
Vừa hoàn thành: Phase 1 + Phase 2, đã verify output không đổi.
Kết quả: task 37 10,4s → 0,68s (263 → 66 query); task 14580 2,36s → 0,70s;
peak memory 108MB → 59MB.
Đang làm dở: không.
Bước tiếp theo: chờ user quyết có làm mục Phase 3 (đổi chữ ký) hay không; chưa test trên UI.
Blocked:
