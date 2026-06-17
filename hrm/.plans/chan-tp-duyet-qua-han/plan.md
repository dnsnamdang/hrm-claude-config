# Plan — Testcase: Chặn TP duyệt khi NV có hàng quá hạn (HRM)

## Phạm vi
Chỉ viết testcase cho luồng **chặn trưởng phòng duyệt** trên HRM. HRM dùng middleware `checkDueConfigsManager` GỌI API sang ERP (`/api/v1/due-configs/check-manager-block`) để quyết định chặn — không tự tính quá hạn.

## Nguồn tham chiếu (code)
- Middleware HRM: `hrm-api/app/Http/Middleware/CheckDueConfigsManager.php` (use_erp, map TpEmployee, ErpApiService, 403, fail-open)
- API proxy: `hrm-api/app/Http/Controllers/Api/V1/DueConfigController.php` (overdueEmployees)
- Routes gắn middleware: `hrm-api/Modules/Timesheet/Routes/api.php` (8+) + `hrm-api/Modules/Assign/Routes/...` (7) — tổng ~20 route
- FE modal: `hrm-client/components/modal/OverdueEmployeesModal.vue`, trigger ở `hrm-client/plugins/axios.js` (403 + message 'quá hạn')
- ERP service đích: `DueConfigBlockService::isManagerBlocked` (xem testcase ERP)

## Tasks
- [x] Điều tra luồng tích hợp HRM→ERP (use_erp, mapping NV, fail-open, modal)
- [x] Liệt kê 20 route Timesheet + Assign gắn middleware
- [x] Viết generator `generate-testcase.py` theo skill testcase-documenter
- [x] Sinh `testcase.xlsx` — 29 TC, P0 41%
- [ ] User review nội dung testcase

## Cấu trúc testcase (6 section)
- I. Điều kiện gọi check (use_erp / auth) — 3 TC
- II. Mapping NV & gọi API ERP (blocked/allow/fail-open) — 6 TC
- III. Phạm vi phiếu — Timesheet — 6 TC
- IV. Phạm vi phiếu — Assign — 6 TC
- V. FE — modal NV quá hạn — 4 TC
- VI. Edge cases & tích hợp — 4 TC

### Checkpoint — 2026-06-11
Vừa hoàn thành: testcase.xlsx (29 TC) + generator cho luồng chặn TP duyệt (HRM)
Bước tiếp theo: user review; phần ERP nằm ở `ERP/.plans/chan-tp-duyet-qua-han/`
Blocked:
