# Plan — Báo cáo tồn theo kho

> Phụ trách: @khoipv · nhánh `develop` (con của `gop_db`, cả hrm-api + hrm-client)
> Port ERP `warehouseReport.stockWareshouseProduct` (Kho › Báo cáo kho › "Báo cáo tồn theo kho") → HRM `/warehouse/stock-warehouse-product`.
> Khuôn: màn anh em "Báo cáo tồn kho tổng hợp theo mặt hàng" (`/warehouse/stock-general-product`) — khác ở: nhóm cột "Chi tiết" theo KHO
> (không theo công ty thuê), thêm ô lọc Model (LIKE) + cột Hãng sản xuất.

## Phase 1 — Port màn

### BE
- [x] Khảo sát ERP: route / controller / `Product::stockWareshouseProductSearchData` / blade / JS class `WarehouseReportProduct` / Excel `StockWareshouseProductExcel`
- [x] `WarehouseStockReportService::aggregateByWarehouse()` (hàm MỚI, không sửa hàm cũ) — cộng `stock_logs` chia cột theo kho
- [x] `StockWarehouseProductReportService` (options / context / report)
- [x] `StockWarehouseProductPrintService` + `StockWarehouseProductExport` + 2 blade (export + print)
- [x] Controller + route `/v1/finance/stock-warehouse-product` (`/`, `/options`, `/print-list-data`, `/export`)
- [x] Đối chiếu số với hàm ERP gốc trên cùng DB `gop_db` — 6 ca (cty 1 cả 7 kho hôm nay 6.256 hàng · LN 31/03 · LN thương hiệu · 7 kho lọc Model · LN 1 công ty thuê · LN lọc Hợp đồng): tập hàng + SL tồn + SL từng kho + Hãng SX khớp 100%;
      thứ tự chỉ lệch giữa các hàng MySQL coi là TRÙNG tên (collation bỏ dấu: "ác quy" = "ắc quy") — ERP chỉ `ORDER BY name`, HRM thêm `id`
- [x] Smoke HTTP kernel: options / index (trang 2, lọc Model) / 422 thiếu ngày+kho / In 2 kiểu + chọn cột (logo, khối ký) / Excel 2 kiểu (đọc lại xlsx: tiêu đề, Kho, 2 tầng, logo) / 403 tài khoản không quyền (emp 24, 4 endpoint)
      Đo: màn 1,7s (6.256 hàng × 7 kho); Excel Đầy đủ toàn bộ 6.256 hàng ~70s (ERP gửi mail khi ≥ 500 — HRM tải thẳng như màn Tổng hợp); In > 2.000 dòng báo vượt trần

### FE
- [x] `pages/warehouse/stock-warehouse-product/index.vue` + `components/StockWarehouseSummary.vue`, `StockWarehouseTable.vue`
- [x] Menu Kho › Báo cáo kho: gắn link mục "Báo cáo tồn theo kho"
- [x] Parse template/script + grep tự kiểm skill erp-to-hrm-screen
- [x] Playwright MCP 24/10 (user yêu cầu, tài khoản DNS Admin, local 3000/8000): vào màn tự chọn công ty + 7 kho + 5 công ty thuê, tổng hợp 6.256 / 7 / 4 kho có tồn;
      bảng 2 tầng 7 kho, dòng 1 khớp API · lọc Model Enter 25 hàng · trang 2 STT 21–25 · bỏ tick Xem toàn bộ kho → xoá kho, Tìm kiếm báo đỏ
      "Vui lòng chọn kho" không gọi API · tick lại đủ kho + công ty thuê · đổi ĐVT Túi (x20) 1.290 → 64,5, bản in theo ĐVT đã chọn (`units`) · In xem trước
      (letterhead, khối ký) · Xuất Excel Đầy đủ tải file (logo, 2 tầng, `#,##0`) · Xóa lọc về 6.256 · mỗi thao tác đúng 1 request · console 0 lỗi
      Ghi nhận nhỏ: Model toàn chữ số (vd "44700") Excel đọc thành SỐ (maatwebsite FromView) — như màn Tổng hợp / ERP

### Fix #11870 — Bộ lọc (tester 26/10/2026)
- [x] 1. Bật/tắt "Xem toàn bộ kho" lag: 5 ô danh mục dựng mảng option mới mỗi lần bộ lọc đổi -> select2 khởi tạo lại cả 5 ô;
      chuyển sang computed `catalogOptions` (giữ tham chiếu)
- [x] 2 + 5. Danh sách xổ hẹp hơn ô + chip lệch nhãn: sửa component DÙNG CHUNG `V2BaseFloatingField` (user đồng ý 27/10) — select2
      trong vỏ `tags` tràn hết khung (lề âm = `--ff-pad-x`), đệm trái chip = `--ff-pad-x`, mũi tên / nút × giữ chỗ cũ
- [x] User 27/10 (ảnh): danh sách xổ đè viền dưới, góc bo + cạnh dọc của ô thò vào danh sách -> select2 tràn tới MÉP NGOÀI
      viền (đệm + 1px) cả 2 bên + đáy (-4px, bù đệm dưới 4px của khung chọn), bỏ bo 2 góc dưới khi đang xổ (`:has`)
- [x] 3. Ô Kho: danh sách xổ "mã - tên", chip chỉ mã (slot `#field-warehouse_ids` + `templateSelection`)
- [x] 4. Model / Hợp đồng: bỏ icon (i), hướng dẫn thành placeholder hiện khi bấm vào ô (`placeholder` + `noHint`)
- [x] 6. Xóa lọc: xoá trắng Công ty + Kho (user chốt 27/10, khác ERP `clear()`), bảng trống chờ chọn lại

### Fix #11871 — Popup In báo cáo (tester 26/10/2026)
- [x] Sửa component DÙNG CHUNG `V2BaseReportPrintModal` (user chốt 27/10: áp mọi popup In): bỏ dòng "Bản in A4 ngang…" (+ prop `note`,
      bỏ luôn `note` ở `self-inventory-report`); chú thích "Cột STT luôn được in…" thành icon (i) + `b-popover info-popover` cạnh "Chọn cột in"

### Checkpoint — 24/10/2026
Vừa hoàn thành: Phase 1 BE + FE (khuôn màn Tổng hợp theo mặt hàng); thêm hàm MỚI `aggregateByWarehouse()` vào service dùng chung (không sửa hàm cũ); đối chiếu ERP 6/6 ca khớp
Đang làm dở: —
Bước tiếp theo: user mở `/warehouse/stock-warehouse-product` kiểm giao diện; cân nhắc Excel toàn bộ (~70s) có cần chạy nền / gửi mail như ERP không
Blocked:

ĐÃ PUSH 24/10/2026 lên `develop`: api `f637713a6` (merge `11e921aeb`), client `612fede85` (merge `d12262082`).

## Fix — Redmine #12173 (16/11/2026) @khoipv

User chốt: (1) cây Hàng hóa ▸ Kho; (5) Excel chọn cột cho các báo cáo Kho (khuôn `ExportModeModal pick-columns` của #12172).

- [x] (1) Bảng: bỏ nhóm cột "Chi tiết" mỗi kho 1 cột → dòng con mỗi kho có tồn dưới từng mặt hàng; ô chọn cấp "Đến hàng hóa / Đến kho" (In/Excel giữ dạng cột như ERP)
- [x] (2) BE `item-list` + FE số khối tổng hợp bấm được → popup chi tiết (mặt hàng / kho / mặt hàng của 1 kho)
- [x] (3) Thu nhỏ cột ĐVT, SL tồn
- [x] (4) Đo + giảm thời gian Xuất Excel (8 kho, ~6.159 mặt hàng ~1 phút)
- [x] (5) Excel chọn cột: Tồn theo kho + Thẻ kho + Tồn kho chi tiết / tổng hợp theo mặt hàng + Tổng hợp xuất nhập tồn (BE `/export` nhận `cols`)
- [x] Kiểm: php -l + smoke HTTP kernel; compile template + babel
- [ ] Mở trình duyệt kiểm thật (user tự test)

Kết quả (16/11/2026, local, công ty TPE 7 kho / 6.256 mặt hàng):
- Excel chậm do HTML reader của PhpSpreadsheet áp style inline TỪNG Ô: 1.000 dòng 26,6s có style vs 2,4s không style. Bỏ style ô thân
  bảng bản Excel, kẻ viền + căn STT theo VÙNG ở `StockWarehouseProductExport::styleTableBody()` → dựng file 129s → 18,8s (HTTP cả truy vấn
  27,5s); Ngắn gọn 6,6s. File vẫn ô số `#,##0`, viền mảnh, STT căn giữa. 5 màn kho khác chưa áp tối ưu này (chưa đo).
- `item-list`: products 6.256 = ô; warehouses 7 = 7; in-stock 4 = 4; từng kho CSKH 417 / KTCN 5 / LN 4.815 / PTT 1.301 = ô; metric lạ 422.
  Không quyền tổng công ty mà gửi `d_warehouse_id` / `d_in_stock` → 403 (chưa thử bằng tài khoản thật).
- Excel `cols`: Tồn chi tiết / Tồn tổng hợp / Tổng hợp XNT qua HTTP ra đúng cột chọn, không gửi = đủ cột; Thẻ kho thử qua service (tài khoản
  thử thiếu quyền Thẻ kho → 403 HTTP).

### Checkpoint — 16/11/2026
Vừa hoàn thành: #12173 đủ 5 mục — bảng cây Hàng hóa ▸ Kho + ô chọn cấp; popup bấm số (`item-list`); ĐVT 100 / SL tồn 90; Excel 129s → 19s;
Excel chọn cột ở 5 màn kho (+ Tồn theo vị trí đã có từ #12172)
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm `/warehouse/stock-warehouse-product` + popup Xuất Excel của Thẻ kho / Tồn chi tiết / Tồn tổng hợp / Tổng hợp XNT
Blocked:

## Phản hồi #12173 (QA 21/11/2026) — popup chi tiết thiếu nút In / Xuất Excel @khoipv

- [x] Kiểm 23/11: đã làm chung trong #12172 (api `5eb3802a5`, client `3b7c4c370`, đã lên `origin/develop` sáng 23/11) — popup drill
      `StockWarehouseDrillModal` có đủ 3 nút In danh sách · Xuất Excel danh sách · Đóng; BE `item-list/print-list-data` + `item-list/export`
      (trait `ServesDrillListPrint`). Không sửa code thêm.
- [x] Smoke HTTP kernel (Super admin, kho KTCN, đến ngày 23/11): `item-list` 200 / 5 dòng; `print-list-data` cols=name,code,qty + q="vít"
      + sort qty desc → 3 dòng, đúng thứ tự cột + thứ tự SL giảm dần; `item-list/export` 200 xlsx
- [ ] User mở trình duyệt kiểm lại popup trên dev sau khi deploy, rồi trả lời QA trên Redmine

### Checkpoint — 23/11/2026
Vừa hoàn thành: xác nhận phản hồi #12173 đã được xử lý trong commit #12172 sáng 23/11, smoke test BE đạt
Đang làm dở: —
Bước tiếp theo: deploy dev → QA test lại popup chi tiết Báo cáo tồn theo kho
Blocked:
