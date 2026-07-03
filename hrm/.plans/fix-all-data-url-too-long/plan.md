# Fix: `training/employees/all-data` lỗi URL quá dài (ERR_CONNECTION_CLOSED)

**Người phụ trách:** @namdangit

## Bối cảnh
Màn `training/courses/add` → "Chọn tất cả đối tượng": FE nhồi toàn bộ `work_position_ids[]` (hàng trăm id) vào query string của `GET training/employees/all-data` → URL vượt giới hạn → server đóng kết nối (`net::ERR_CONNECTION_CLOSED`).

**Hướng xử lý:** đổi GET → POST, gửi `work_position_ids` qua request body.

## Phase 1 — Đổi GET → POST

### BE
- [x] `Modules/Training/Routes/api.php:357` — đổi `Route::get('/all-data', ...)` → `Route::post(...)` (controller `getAllData` đọc `$request->work_position_ids` qua input bag, chạy được với POST body, không cần sửa thêm)

### FE
- [x] `components/modals/AddEmployeeModal.vue` — `getData()` chuyển từ `apiGetMethod` + `buildQuery` sang `apiPostMethod` với `payload: { work_position_ids }`
- [x] Xóa import `buildQuery` không còn dùng

## Verify
- [ ] Bấm "Chọn tất cả đối tượng" với nhiều chức vụ → modal học viên load dữ liệu, không còn lỗi connection
- [ ] Bấm "+ Thêm học viên" với vài chức vụ → vẫn lọc đúng theo work_position_ids
