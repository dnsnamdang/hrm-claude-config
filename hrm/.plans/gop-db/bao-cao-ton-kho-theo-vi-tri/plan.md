# Plan — Báo cáo tồn kho theo vị trí

> Phụ trách: @khoipv · nhánh `develop` (con của `gop_db`, cả hrm-api + hrm-client)

## Phase 1 — Port màn

### BE
- [x] Khảo sát ERP: route / controller / `StockPosition::warehouseReportLocation*` / blade / JS class / Excel / lệnh nền
- [x] Chụp số liệu Thẻ kho (5 ca) + màn Chi tiết (5) + màn Tổng hợp (5) TRƯỚC khi tách hàm
- [x] Tách vào `WarehouseStockReportService` (user chốt 23/10): `applyProductFilters()`, `positionIdsOf()`, `contractsOfImports()`;
      Thẻ kho + màn Chi tiết gọi lại — chụp lại 15/15 ca khớp từng byte
- [x] `StockLocationProductReportService`: options / structure / context / report (cắt trang theo vị trí, cây Vị trí ▸ Hàng ▸ Công ty ▸ Lô)
- [x] `StockLocationProductPrintService` + `StockLocationProductExport` + 2 blade (Đầy đủ / Ngắn gọn, dòng Tổng cộng)
- [x] Controller + route `/v1/finance/stock-location-product` (`/`, `/options`, `/structure`, `/print-list-data`, `/export`)
- [x] Đối chiếu số với hàm ERP gốc (cùng DB `gop_db`), kho LN hôm nay: 764 vị trí, cùng thứ tự, SL tồn / Nhà kho / mặt hàng / lô khớp 100%
      (sau khi sửa ép `(int)` làm mất hàng tồn lẻ 0.3)
- [x] Đối chiếu thêm 7 ca (SG hôm nay, SG lọc Nhà, LN 31/03, LN thương hiệu, LN 1 công ty thuê, LN hợp đồng, PTT): vị trí / thứ tự / SL tồn
      / mặt hàng / lô khớp 100%, trừ đúng các lỗi ERP đã ghi ở spec §6: `GROUP_CONCAT` 1024 ký tự cắt hụt mặt hàng (SG01-N1-KV6 205/299,
      PTT-N1-KV-DA 170/211 — ERP là đoạn đầu của HRM); lô nhiều nhật ký cùng giây (ERP `usort` không ổn định); lọc Hợp đồng: SL nhân đôi
      do JOIN (96 vs 48) + ghi đè chỉ số công ty
- [x] Lọc Hợp đồng: vị trí có lô của hợp đồng thì chỉ giữ công ty có lô (ERP `transformInput($status = true)`)
- [x] Smoke HTTP kernel: options / structure / index (trang 2, lọc Nhà+Dãy) / 422 thiếu kho + kho công ty khác / In 2 kiểu + chọn cột /
      Excel 2 kiểu (đọc lại xlsx: tiêu đề, Kho, 2 tầng, gộp ô, `#,##0`, logo, khối ký) / 403 tài khoản không quyền (mọi endpoint)
- [x] Tối ưu dựng cây (gom cặp theo vị trí 1 lần): 697 vị trí 7s → 1s; In / Excel bỏ trần thời gian như ERP

### FE
- [x] `pages/warehouse/stock-location-product/index.vue` (khuôn màn Chi tiết + ScopePicker của Thẻ kho)
- [x] `components/StockLocationSummary.vue`, `components/StockLocationTable.vue` (cây 4 cấp, ô chọn cấp bung, ĐVT từng hàng)
- [x] Menu Kho › Báo cáo kho có link
- [x] Parse template/script (vue-template-compiler + babel) + grep tự kiểm skill erp-to-hrm-screen
- [ ] Mở trình duyệt kiểm thật (user tự test — chưa chạy Playwright)

### Checkpoint — 23/10/2026
Vừa hoàn thành: Phase 1 BE + FE; tách 3 hàm dùng chung (số 3 màn cũ không đổi); đối chiếu ERP 8 ca khớp (lệch chỉ ở lỗi ERP đã ghi)
Đang làm dở: —
Bước tiếp theo: user mở `/warehouse/stock-location-product` kiểm giao diện; ca quyền "theo công ty" / "theo kho" chờ `permission:sync`
Blocked:

## Fix — Redmine #11861 (26/10/2026)

- [x] Ô lọc Hợp đồng: bỏ icon tooltip, đưa chữ "Gõ mã hợp đồng rồi Enter hoặc bấm Tìm kiếm." thành placeholder (hiện khi bấm vào ô)
- [x] Bảng: bỏ cột Hợp đồng (đưa hợp đồng + khách hàng vào ô Lô như ERP); thêm cột **SL** (SL lô) và **Cộng** (SL công ty) như ERP —
      In/Excel đã đúng sẵn, không đụng
- [x] Parse template/script (vue-template-compiler + babel); đếm ô mỗi dòng cây = 10 = số cột
- [ ] Mở trình duyệt kiểm thật (user tự test)
