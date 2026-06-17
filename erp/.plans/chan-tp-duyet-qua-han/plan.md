# Plan — Testcase: Chặn TP duyệt khi NV có hàng quá hạn (ERP)

## Phạm vi
Chỉ viết testcase cho luồng **chặn trưởng phòng duyệt** (middleware `checkDueConfigsManager` + `DueConfigBlockService::isManagerBlocked`). KHÔNG bao gồm widget cảnh báo dashboard hay CRUD cấu hình due_configs.

## Nguồn tham chiếu (code)
- Middleware: `app/Http/Middleware/CheckDueConfigsManager.php`
- Service: `app/Services/DueConfig/DueConfigBlockService.php` (isManagerBlocked, getOverdueEmployees)
- API: `app/Http/Controllers/Api/DueConfigController.php` (checkManagerBlock, overdueEmployees)
- Routes gắn middleware: `routes/web.php` (~30 route: xuất hàng/giữ/mượn/nhập, đặt hàng, HĐ mua-bán, quyết toán, thanh toán, giao việc...)
- Modal: `resources/views/layouts/app.blade.php:205` (`show_overdue_modal`)

## Tasks
- [x] Điều tra luồng + 3 loại quá hạn (giữ/mượn/nhập thẳng) + điều kiện config (tab=2 + company_due_configs)
- [x] Viết generator `generate-testcase.py` theo skill testcase-documenter (9 mục mô tả + summary + 6 section)
- [x] Sinh `testcase.xlsx` — 36 TC, P0 44%
- [ ] User review nội dung testcase, chỉnh số liệu mẫu nếu cần

## Cấu trúc testcase (6 section)
- I. Điều kiện kích hoạt chặn (config) — 5 TC
- II. 3 loại quá hạn — 10 TC
- III. Phạm vi phiếu áp dụng — 7 TC
- IV. Trường hợp không chặn — 5 TC
- V. Thông báo & modal NV quá hạn — 5 TC
- VI. Edge cases & bảo mật — 4 TC

### Checkpoint — 2026-06-11
Vừa hoàn thành: testcase.xlsx (36 TC) + generator cho luồng chặn TP duyệt (ERP)
Bước tiếp theo: user review; phần HRM nằm ở `HRM/.plans/chan-tp-duyet-qua-han/`
Blocked:
