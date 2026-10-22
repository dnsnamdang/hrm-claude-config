# Plan — Thẻ kho

> Phụ trách: @khoipv · nhánh `develop` (cả hrm-api + hrm-client)

## Phase 1 — Port màn

### BE
- [x] Quyền "Thủ kho" + "Xem báo cáo tồn kho theo tổng công ty" (type 21) trong `PermissionsTableSeeder` — dry-run OK
- [x] `StockCardReportService`: options / structure / context (phạm vi công ty, kho, công ty thuê, vị trí) / report
- [x] `StockCardPrintService`: bảng 2 tầng, 2 kiểu Đầy đủ / Rút gọn, chọn cột, mẫu 251 hoặc blade dự phòng
- [x] `StockCardExport` + blade `exports/stock_card`
- [x] `StockCardController` + route `/v1/finance/stock-card`
- [x] Ô tìm nhanh `keyword` (lọc sau khi cộng dồn SL tồn)
- [x] Smoke test HTTP kernel: options / index / print / export / structure, 403 không quyền, 422 thiếu hàng

### FE
- [x] `ScopePicker.vue` thêm prop `optional` (user đồng ý)
- [x] `pages/warehouse/stock-card/index.vue` (khuôn `pages/lookup/stock-companies`)
- [x] `ExportModeModal.vue`, `voucher-link.js`
- [x] Menu Kho › Báo cáo kho › Thẻ kho có link
- [x] Parse template/script (vue-template-compiler + babel)
- [x] Test Playwright (22/10, local, tài khoản DNS Admin): chọn hàng, đổi ĐVT, phân trang, chọn kho → công ty thuê + cây vị trí,
      tick Nhà/Vị trí, tìm nhanh, đổi công ty, Loại báo cáo, In (Đầy đủ/Rút gọn), Xuất Excel, Cấu hình cột, F5 khôi phục, Làm mới,
      báo đỏ bắt buộc, link chứng từ — đạt
- [x] Fix sau test: bản in cột Ngày / Số chứng từ không xuống dòng

### Checkpoint — 22/10/2026
Vừa hoàn thành: port BE + FE màn Thẻ kho, smoke test BE qua HTTP kernel
Đang làm dở: —
Bước tiếp theo: chạy `php artisan permission:sync` (hoặc seeder) để tạo 2 quyền; user mở `/warehouse/stock-card` kiểm trên trình duyệt
Blocked:
