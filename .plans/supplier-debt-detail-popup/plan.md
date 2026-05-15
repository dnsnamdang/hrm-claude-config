# Plan: Popup chi tiết phát sinh — Công nợ NCC

## Trạng thái
- Bắt đầu: 2026-05-05
- Người phụ trách: @nguyentrancu97
- Code DONE: 2026-05-05

### Checkpoint — 2026-05-05
Vừa hoàn thành: 5/5 task — popup chi tiết phát sinh 5 cột trên 2 màn công nợ NCC
Bước tiếp theo: user test trên cả 2 màn (NCC trong nước + nước ngoài)

## Phase 1: BE — Mở rộng API endpoint

- [x] Task 1: Kiểm tra `AccountDetail::getInvoiceableSupplierDetail($request)` — ĐÃ support 5 type sẵn (total_payable, adjust_debt, total_returned, total_paid, adjust_has). Không cần sửa BE.

## Phase 2: FE — Domestic (supplier-debt-details)

- [x] Task 2: Refactor JS — xoá `showGetPaidDetail` + `billPaidDetailModal`, đổi thành `showInvoiceableDetail(row, type)` với BaseSearchModal tạo mới mỗi lần (title động theo type)
- [x] Task 3: Thêm `ng-click` cho 5 cột: total_payable, adjust_debt, total_returned, total_paid, adjust_has

## Phase 3: FE — Foreign (supplier-debt-nation-details)

- [x] Task 4: Refactor JS — fix endpoint (đổi từ `getInvoiceableDetail` sang `getInvoiceableSupplierDetail`), dùng pattern type động giống domestic
- [x] Task 5: Thêm `ng-click` cho 5 cột ở cả dòng cha (supplier) và dòng con (contract)
