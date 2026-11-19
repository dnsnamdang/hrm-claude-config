# Plan — Báo giá vận chuyển (BGVC)

Màn ERP: `admin/delivery_quotations` — Báo giá vận chuyển (DeliveryQuotation).

## Tasks

- [x] Task 1 — Rà soát màn BGVC từ code (Controller / Model / form.blade): fields, validation store/update, status, phân quyền (canEdit/canDelete/canSummaryCost), luồng nghiệp vụ, xuất Excel, bảng giá hiệu lực.
- [x] Task 2 — Viết testcase Excel `testcase.xlsx` theo skill `testcase-documenter` (15 cột, block mô tả 9 mục, TEST SUMMARY COUNTIF, section TC-ROLE + La Mã).
- [x] Task 3 — Fix bug 500 màn danh sách `delivery_cost_summaries` (Tổng hợp giá đề xuất): DataTable crash "Trying to get property 'id' of non-object". Nguyên nhân: closure `editColumn('base_quotation')` truy cập `$object->base_quotation->id` khi quan hệ null (BGVC gốc bị xóa / `delivery_quotation_id` mồ côi) → cả bảng fail, `data=[]` dù `recordsTotal=53`. Fix: null-check `base_quotation` + gia cố `employee_create` trong `DeliveryCostSummaryController@searchData`.

## Checkpoint — 2026-10-30
Vừa hoàn thành: sinh `testcase.xlsx` — 60 TC (6 TC-ROLE + 54 La Mã) / 9 section, P0 = 50%.
Đang làm dở: (không)
Bước tiếp theo: bàn giao QA; recalc COUNTIF sẽ tự chạy khi mở bằng Excel (máy local không có LibreOffice nên chưa recalc offline).
Blocked: (không)

## Ghi chú nguồn (reverse-engineer)
- Controller: `app/Http/Controllers/Common/DeliveryQuotationController.php`
- Model: `app/Model/Common/DeliveryQuotation.php` (+ Vehicle/Payload/Road, PriceListValidDelivery)
- Form: `resources/views/common/delivery_quotations/form.blade.php`
- Route: `routes/web.php` prefix `delivery_quotations`, middleware `checkPermission:Quản lý chi phí vận chuyển`
- Bẫy chính: `note` bắt buộc ở `update()` nhưng KHÔNG bắt buộc ở `store()`.
