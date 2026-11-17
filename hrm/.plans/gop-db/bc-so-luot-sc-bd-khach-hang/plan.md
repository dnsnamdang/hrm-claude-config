# Plan — Báo cáo số lượt SC - BD cho 1 khách hàng

## Phase 1 — BE (hrm-api, Modules/Sale)
- [x] Service `WarrantyRepairByCustomerReportService` (quyền/phạm vi, lượt SC + BD, gom thiết bị, summary, item-list)
- [x] Print service + blade in + Excel export + blade Excel
- [x] Controller + route `v1/sale/reports/warranty-repair-by-customer` + `checkPermission` 2 mã
- [x] Catalog `sale.php`: thêm `hrm` vào `platforms` 2 mã
- [x] Kiểm số liệu bằng SQL độc lập (khách nhiều lượt), phạm vi 4 mức, 403 khi không quyền

## Phase 2 — FE (hrm-client)
- [x] `pages/sale/warranty-repair-by-customer-report/index.vue` + Summary + Table + VisitModal
- [x] Menu `sale-hub.js` → link + quyền
- [x] Verify trình duyệt 1366px: chưa chọn khách, chọn khách, đổi kỳ, popup, In, Excel

## Phase 3 — Bàn giao
- [x] Commit nhánh feat, cập nhật STATUS + memory

### Checkpoint — 2026-11-16 (xong, chưa push)
Vừa hoàn thành: BE + FE + verify trình duyệt 1366px (chưa chọn khách, chọn khách, popup lượt, In popup, In chính bỏ cột, Excel,
403 khi không quyền, 4 mức phạm vi, đối chiếu SQL độc lập khách 29TPHXDO-60: 37 lượt SC / 33 lượt BD / 59 thiết bị).
Commit `feat/bc-so-luot-sc-bd-khach-hang`: api `90c284aac`, client `58343d85d`.
Bước tiếp theo: user check → push + merge `develop`. Deploy `permission:catalog-sync`.

### Checkpoint — 2026-11-16 (merge develop)
Vừa hoàn thành: push `feat/bc-so-luot-sc-bd-khach-hang` + merge vào `develop` (api `d51632a4c`, client `f9b8ced17`). Merge kéo theo 8 commit đã có trên gop_db mà develop chưa có (7 commit trợ lý agent của dnsnamdang, 1 commit "Giao cho tôi" của Manh Cuong).
Bước tiếp theo: QA trên dev (HRM `/sale/warranty-repair-by-customer-report`, ERP `/admin/report/warranty_repair_service_by_customer`); dev chạy `permission:catalog-sync`; lên gop_db khi user bảo.
Blocked:

## Ngày 17/11/2026 (@junfoke)
- [x] 17/11/2026 — Hỗ trợ check route ERP `warranty_repair_service_by_customer` + quyền: URL đúng là `/admin/reports/...` (gõ `report` sẽ 404); route và menu ERP không chặn quyền, ai đăng nhập cũng mở được — quyền chỉ quyết phạm vi dữ liệu: `sale.bao_cao_so_luot_sua_chua_bao_duong_cho_1_khach_hang.view` (≥ GROUP tất cả công ty / ≥ COMPANY công ty mình), `..._theo_nhan_vien.view` (≥ DEPARTMENT phòng / ≥ PART bộ phận).
