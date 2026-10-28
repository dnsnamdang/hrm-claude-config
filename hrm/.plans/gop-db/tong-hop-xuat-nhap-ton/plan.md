# Plan — Tổng hợp xuất nhập tồn

> Phụ trách: @khoipv · nhánh `develop` (con của `gop_db`, cả hrm-api + hrm-client)
> Port ERP `warehouseReport.changeSummaryReport` (Kho › Báo cáo kho › "Tổng hợp xuất nhập tồn") → HRM `/warehouse/change-summary-report`.
> (Màn kế toán `accountingChangeSummaryReport` ở menu Kế toán là màn KHÁC — không thuộc feature này.)
> Khuôn: "Báo cáo tồn theo kho" (`/warehouse/stock-warehouse-product`) + bộ lọc Kỳ / Nhà-Dãy-Khoang-Vị trí nhiều kho của Thẻ kho (`/warehouse/stock-card`).

User chốt 24/10/2026:
- Tách phần gộp cây Nhà/Dãy/Khoang/Vị trí nhiều kho của Thẻ kho ra service chung (Thẻ kho gọi lại, test lại Thẻ kho).
- Lọc vị trí GIỮ Y ERP (kể cả lỗi: tick Nhà/Dãy/Khoang không tick Vị trí = không lọc; có tick Vị trí thì kho không tick bị bỏ).
- Thêm In xem trước (ERP đã comment nút In) như các màn báo cáo kho anh em.

## Phase 1 — Port màn

### BE
- [x] Khảo sát ERP: route / controller / `Product::changeSummaryReportSearchData` / blade / JS `WarehouseReport`, `ProductInStock` / Excel `AccountingChangeSummaryExcel` + `getTableChangeSummary4(Basic)Excel`
- [x] `WarehouseStockReportService`: thêm `structureOf()` (tách từ `StockCardReportService::structure()`) + `period()` (tách từ `StockCardReportService::period()`); Thẻ kho gọi lại
      (Thẻ kho: constructor đổi `PositionInventoryWriteService` → `WarehouseStockReportService`, bỏ `date()` private)
- [x] `ChangeSummaryReportService` (options / structure / context / report) — vị trí theo logic ERP (`positionIds()`), cộng `stock_position_logs`
- [x] `ChangeSummaryReportPrintService` + `ChangeSummaryReportExport` + 2 blade (`exports/change_summary_report`, `prints/change-summary-report`)
- [x] Controller `ChangeSummaryReportController` + route `/v1/finance/change-summary-report` (`/`, `/options`, `/structure`, `/print-list-data`, `/export`)
- [x] Đối chiếu số với hàm ERP gốc `Product::changeSummaryReportSearchData` trên cùng DB `gop_db` — 8 ca (cả 7 kho năm 2026 · Không nhặt điều chuyển ·
      LN 6T/2025 + 2 công ty thuê · tick Vị trí (kho không tick bị bỏ, y lỗi ERP) · chỉ tick Nhà (không thu hẹp, y lỗi ERP) · lá hỗn hợp Dãy/Khoang/Vị trí tự do ·
      thương hiệu + nhóm · 1 ngày): tập hàng + Tồn đầu / Nhập / Xuất khớp 100%; thứ tự chỉ lệch giữa hàng MySQL coi là TRÙNG tên (320 cặp, 0 cặp khác tên)
- [x] Test lại Thẻ kho sau khi tách: structure (3 ca) + period (8 ca) chụp trước/sau giống hệt; 4 endpoint Thẻ kho qua HTTP kernel 200
- [x] Smoke HTTP kernel: options / structure (nhiều kho, tiền tố mã kho; kho lạ → rỗng) / index (trang 2, trang vượt → trang cuối) / 422 (thiếu kho, kỳ ngược,
      thiếu ngày) / In 2 kiểu + chọn cột (bỏ khoá lạ) + vượt trần 2.000 dòng / Excel 2 kiểu (đọc lại xlsx: logo, tiêu đề, Từ–Đến, Kho, cột, `#,##0`, khối ký) /
      403 tài khoản không quyền (emp 24, 13 request). Đo: cả 7 kho 7.776 hàng ~1,7s

### FE
- [x] `pages/warehouse/change-summary-report/index.vue` + `components/ChangeSummarySummary.vue`, `ChangeSummaryTable.vue`
- [x] Menu Kho › Báo cáo kho: gắn link "Tổng hợp xuất nhập tồn"
- [x] Parse template/script (vue-template-compiler + babel) + grep tự kiểm skill erp-to-hrm-screen
- [ ] User mở trình duyệt kiểm (chưa bấm thật — theo quy ước không tự chạy Playwright)

### Fix #11873 (tester 26/10/2026)
- [x] Cột Nhà nhóm theo TỪNG KHO như ERP (tiêu đề mã kho, nhà thụt dưới) thay danh sách phẳng "CSKH | N1 - Nhà 1" — user đồng ý sửa chung
      27/10: BE `WarehouseStockReportService::structureOf()` bỏ tiền tố mã kho trong `code`, gắn `warehouse_id` + `warehouse_code`;
      FE `ScopePicker.vue` (nhiều kho) nhóm Nhà + Vị trí tự do theo kho, tiêu đề nhóm Dãy/Khoang/Vị trí giữ "MÃ KHO | …".
      Áp luôn Thẻ kho; 2 form kiểm kê (1 kho, không có `warehouse_code`) không đổi. Smoke tinker 2 kho OK

### Checkpoint — 24/10/2026
Vừa hoàn thành: Phase 1 BE + FE; tách `structureOf()` + `period()` khỏi Thẻ kho sang `WarehouseStockReportService`; đối chiếu ERP 8/8 ca khớp
Đang làm dở: —
Bước tiếp theo: user bấm thử Thẻ kho chọn 2 kho (LN + KTCN) xem cây vị trí; đã Playwright màn mới (lọc / kỳ / ĐVT / vị trí / In / Excel OK).
Đã push nhánh `develop`: hrm-api `a9c27504c`, hrm-client `9b3a482e6` (24/10/2026)
Blocked:
