# Plan: Cấu hình chặn luồng quá hạn — Tab 2 chặn TP + Lịch sử chỉnh sửa

## Trạng thái
- Bắt đầu: 2026-04-20
- Phase 1-3: đã hoàn thành
- Phase 4 (popup + Excel): code DONE — @nguyentrancu97

## Phase 1-3: Đã hoàn thành ✅

## Phase 4: Popup thông báo + Xuất Excel

### BE — ERP (TanPhatDev)
- [x] Task 1: Service `DueConfigBlockService::getOverdueEmployees($userId)` — trả danh sách NV quá hạn
- [x] Task 2: API endpoint `GET /api/v1/due-configs/overdue-employees` (JSON + Excel)
- [x] Task 3: Excel export class `OverdueEmployeesExcel`

### BE — HRM (hrm-api)
- [x] Task 4: Proxy endpoint `GET /api/v1/due-configs/overdue-employees` gọi ERP API

### FE — ERP (TanPhatDev)
- [x] Task 5: Partial view modal `common/due_configs/overdue-modal.blade.php`
- [x] Task 6: Include modal vào layout + JS xử lý bắt response → mở modal + xuất Excel
- [x] Task 6b: Fix — dùng `ajaxComplete` thay vì `ajaxPrefilter` để original success callback vẫn chạy (reset loading state)
- [x] Task 6c: Fix — xử lý flash message (non-AJAX redirect) trong layout nhận diện "quá hạn" → mở popup

### FE — HRM (hrm-client)
- [x] Task 7: Sửa `plugins/axios.js` — nhận diện 403 quá hạn → trigger modal thay vì toast
- [x] Task 8: Component `OverdueEmployeesModal.vue` — modal global + gọi API + xuất Excel (blob download)
- [x] Task 9: Mount modal vào `layouts/default.vue`

### Checkpoint — 2026-05-05
Vừa hoàn thành: Phase 4 — popup danh sách NV quá hạn + xuất Excel
Key fix: responseErrors() trả HTTP 200 (không phải 400) → dùng ajaxComplete intercept success response thay vì ajaxError
Bước tiếp theo: user test toàn bộ trên ERP + HRM
