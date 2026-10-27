# Plan — Báo cáo tồn kho chi tiết theo mặt hàng

> Phụ trách: @khoipv · nhánh `develop` (cả hrm-api + hrm-client)

## Phase 1 — Port màn

### BE
- [x] 2 quyền "Xem báo cáo tồn kho theo công ty" / "… theo kho" (type 21) trong `PermissionsTableSeeder` — dry-run
- [x] `StockDetailByProductReportService`: options (công ty / kho theo 3 cấp quyền / công ty thuê) + report (port `Product::warehouseReportDetailSearchData`)
- [x] `StockDetailByProductPrintService` + `StockDetailByProductExport` + 2 blade (Đầy đủ / Rút gọn)
- [x] Controller + route `/v1/finance/stock-detail-by-product`
- [x] Smoke test HTTP kernel: options / index / print / export (2 kiểu, đọc lại file xlsx), 403 không quyền, 422 thiếu kho
- [x] Tối ưu query nhật ký vị trí (STRAIGHT_JOIN + whereIntegerInRaw): kho LN 34s → 3,2s, kết quả trang 1 giữ nguyên
- [x] Đối chiếu số với hàm ERP gốc (`Product::warehouseReportDetailSearchData`, cùng DB gop_db): kho MT 22/10/2026 (271 hàng) + PTT 31/03/2026 (1.347 hàng) — khớp 100% SL tồn, Cộng từng công ty, SL từng vị trí

### FE
- [x] `pages/warehouse/stock-detail-by-product/index.vue` (khuôn Thẻ kho)
- [x] `components/StockDetailSummary.vue`, `components/StockDetailTable.vue` (cây 4 cấp, ĐVT từng hàng)
- [x] `ExportModeModal` (Thẻ kho) thêm prop `title` (mặc định giữ nguyên)
- [x] Menu Kho › Báo cáo kho có link
- [x] Parse template/script
- [x] Test Playwright (22/10, local, DNS Admin — Super admin): mặc định ngày/công ty, báo đỏ thiếu Kho (cả khi bấm In), chọn kho → tick sẵn
      công ty thuê, 1 request/lần lọc, ô chọn cấp 4 mức + mũi tên, phân trang BE (21–40/1301), chọn hàng qua popup + x xoá chip, đổi ĐVT
      (60,000 Cái → 1,500 Hộp x40 cả dòng con), Hợp đồng chỉ tải khi Enter (lọc HD = 81 hàng không dòng con — khớp ERP), link HĐ mở ERP,
      F5 khôi phục bộ lọc, In (bỏ cột → cols đúng, xem trước đúng), Xuất Excel (tải + đóng popup, nội dung khớp màn), Xóa lọc, đổi công ty
      xoá kho, 1366px tiêu đề 1 dòng / không cuộn trang — đạt
- [x] Fix sau test: bảng `min-width` 1500 → 1240px (cột hẹp lại) — ở 1536px cột Hợp đồng + SL tồn bị đẩy ra ngoài phải cuộn
- [ ] Chạy `php artisan permission:sync` để tạo 2 quyền mới; test tài khoản quyền "theo công ty" / "theo kho"
- [x] 23/10/2026: tách quyền / phạm vi / bộ lọc / `aggregate()` / `unitsOf()` sang `WarehouseStockReportService` (dùng chung với màn
      Báo cáo tồn kho tổng hợp theo mặt hàng — user chốt). Số liệu 3 kho × 2 ngày trước/sau khớp từng byte; options/print/export/422 vẫn chạy

### Checkpoint — 22/10/2026
Vừa hoàn thành: Phase 1 BE + FE, số liệu khớp ERP 100% ở 2 kho
Đang làm dở: —
Bước tiếp theo: user mở `/warehouse/stock-detail-by-product` kiểm giao diện; chạy `php artisan permission:sync`
Blocked:
