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

### Fix #11868 (tester 26/10/2026)
- [x] SL tồn sau đổi ĐVT hiện SỐ NGUYÊN như ERP (`roundNumber(qty/hệ số, 2)` rồi `| number:0`) — `StockDetailTable.vue::q()`;
      vd 13 Cái → Thùng x12: 1.08 → 1, 186.5 → 187

### Fix #11869 (tester 26/10/2026)
- [x] Ô Hàng hóa trông như chọn nhiều (chip) mà chỉ giữ 1 hàng → user chốt 27/10 giữ 1 hàng như ERP: ô hiện chữ thường + dấu x
      xoá riêng (`.sd-product-clear`, `@click.stop`), không đổi BE

### Fix #11872 — Bản in (tester 26/10/2026)
- [x] Dòng "Ngày … tháng … năm …" lệch cột "Người lập báo cáo": sửa layout DÙNG CHUNG `finance::prints._layout` (user chốt 27/10: áp
      mọi mẫu in) — dòng ngày nằm trong ô người ký CUỐI, ô khác chừa 1 dòng trống (`visibility: hidden`) cho tên ngang hàng; render
      thử 1 / 2 người ký qua tinker OK

### Checkpoint — 22/10/2026
Vừa hoàn thành: Phase 1 BE + FE, số liệu khớp ERP 100% ở 2 kho
Đang làm dở: —
Bước tiếp theo: user mở `/warehouse/stock-detail-by-product` kiểm giao diện; chạy `php artisan permission:sync`
Blocked:

## Tài liệu SRS / HDSD / Testcase (06/11/2026) @khoipv

- [x] Đọc brief + skill srs-documenter / hdsd-documenter / testcase-documenter; đọc code FE `pages/warehouse/stock-detail-by-product/**`, BE `StockDetailByProduct*` + `WarehouseStockReportService`
- [x] Chụp ảnh dev-hrm (DNS Admin, `bctkct_shots/_capture/capture.js`, hồ sơ đăng nhập riêng, chặn mọi yêu cầu ghi — lọt 0; màn chỉ có API GET) — kho HP - Hải Phòng (96 mặt hàng); 40 icon (`trim_icon --dry` 0/40)
- [x] Đối soát số dev (`_capture/doisoat.js`, chỉ GET): ENEO-700-V5231 kho HP / TPHP — tồn 31/12/2025 = 70; Thẻ kho 01/01–06/11/2026 nhập 496, xuất 546, tồn cuối 20 = SL tồn báo cáo (20) = Báo cáo tồn kho tổng hợp theo mặt hàng (20); tổng 4 lô = 20 — KHỚP
- [x] `gen_srs.py` → `SRS - Báo cáo tồn kho chi tiết theo mặt hàng.docx` (68 trang, 7 chức năng, selfcheck khớp mẫu; metrics ui=14.3 ev=5.3 evch=1186 intro=1913; Phần 5 bảng 4 cột 15 dòng; Mục lục trang riêng căn giữa)
- [x] `gen_hdsd.py` → `HDSD_Bao cao ton kho chi tiet theo mat hang.docx` (12 trang, 6 phần)
- [x] `gen_testcase.py` → `testcase.xlsx` (128 TC, 8 nhóm, P0 41,4%, check_tc `bao_cao` 0 lỗi)
- [x] `gen_checklist.py` → `Đối chiếu checklist.xlsx` (Testcase 103 có TC / 221 N/A; SRS 79 có mục / 84 N/A)
- [x] Ghi nhận nghi lỗi (chưa sửa): popup Chọn hàng hóa báo 403 khi Tồn theo công ty ≠ công ty đăng nhập (dev, CN Hải Phòng); ô Hợp đồng không thoát ký tự `%` `_`; link hợp đồng loại HRM (`to`) bị hiện chữ trơn vì bảng chỉ xử lý `href`; Cài đặt bộ lọc cho ẩn cả 3 ô bắt buộc

### Checkpoint — 06/11/2026
Vừa hoàn thành: bộ SRS + HDSD + Testcase + Đối chiếu checklist màn Báo cáo tồn kho chi tiết theo mặt hàng
Đang làm dở: —
Bước tiếp theo: user xem tài liệu; quyết định có sửa 4 điểm nghi lỗi không; đẩy Drive khi user yêu cầu
Blocked:
