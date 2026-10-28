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
- [x] User 22/10: ô Hàng hóa mở POPUP chọn hàng (`V2BasePickerField` + `V2ProductPickerModal`) thay ô gõ tìm; tên dài cắt "…" giữ ô 32px — test Playwright đạt
- [x] User 22/10: bỏ icon kính lúp ở ô Hàng hóa (`icon=""`, khuôn ô chọn của Phiếu điều chuyển vị trí)

## Phase 2 — Chuyển sang khuôn báo cáo (skill report-styles, user chốt 22/10/2026)

User chốt: khối tổng hợp 2 khối (Số lượng + Chứng từ, không drill) · bảng cây 2 cấp Chứng từ ▸ Lô/vị trí · ô Kỳ · code luôn không mockup.

### BE
- [x] `context()` nhận `period` (week / month / year mặc định / last_year / custom + from_date/to_date) — khuôn `ServiceDemandReportService::period()`
- [x] `report()` trả `meta` (period_label, from, to, generated_at) + `summary` đếm chứng từ (tổng / nhập / xuất / điều chuyển) + tổng Nhập/Xuất dòng điều chuyển

### FE
- [x] `index.vue`: SmartFilterPanel theo khuôn (Xóa lọc, InfoTip MỤC ĐÍCH BÁO CÁO, In danh sách + Xuất Excel, ô Kỳ, ô ĐVT, ô Số chứng từ/Diễn giải thay ô tìm nhanh), `.pct-body--loading`, Excel tải bằng link `?token=`
- [x] `components/StockCardSummary.vue` (khuôn TrackingSummary, không DrillNum)
- [x] `components/StockCardTable.vue` (khuôn TrackingTable: rsum-tb, dòng TỔNG, caret + ô chọn cấp, V2BaseTableScroll, V2BasePagination theo chứng từ)
- [x] Bỏ bảng tự dựng + Cấu hình cột cũ (khuôn báo cáo không có)
- [x] Test Playwright theo mục 6 skill
- [x] Fix sau test: bảng `min-width` 1500 → 1620px — ở 1366px số lô bị cắt "…" (cột Chứng từ / Lô 280 → 400px)

### Fix sau duyệt (user 22/10/2026)
- [x] Nhập / Xuất trong kỳ ở khối tổng hợp + bản in/Excel CỘNG CẢ điều chuyển vị trí cho khớp số ERP (ERP lỡ cộng vì chuỗi
      `"App\Model\...PositionTransferDetail"` trong SQL bị MySQL nuốt dấu `\` → điều kiện loại không khớp dòng nào). Loại báo cáo
      "Không nhặt điều chuyển" vẫn loại như cũ
- [x] Xuất Excel có loading: tải qua axios blob (bỏ link `?token=`), nút "Đang xuất…" + icon quay + thanh loading Nuxt; popup kiểu
      xuất giữ mở tới khi tải xong, lỗi thì giữ popup
- [x] Ô Nhà / Dãy / Khoang / Vị trí chỉ hiện khi đã chọn Kho (bỏ hết kho -> ẩn, tick đã bị xoá ở watcher)

### Fix #11866 (tester 26/10/2026)
- [x] Ô Đơn vị tính có nút X xoá nhanh; xoá là về ĐVT cơ sở của hàng (không để ô trống)
- [x] User 27/10: BỎ hẳn ô lọc Đơn vị tính (như ERP) — số lượng / In / Excel luôn theo ĐVT cơ sở của hàng (`report.unit_id`)
- [x] ~~Link chứng từ tồn đầu `NHAP_TON_DAU_…`~~ — user bỏ qua 27/10 (ERP không có link, HRM chưa có màn xem tồn đầu)

### Checkpoint — 22/10/2026
Vừa hoàn thành: Phase 2 — chuyển Thẻ kho sang khuôn báo cáo (rsum + bảng cây 2 cấp + ô Kỳ), test Playwright đạt mục 6 skill report-styles
Đang làm dở: —
Bước tiếp theo: chạy `php artisan permission:sync` để tạo 2 quyền; user duyệt giao diện
Blocked:
