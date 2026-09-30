# Plan: Fix sổ cái "Hàng đang về" lệch với popup Chi tiết

Repo `TanPhatDev` (bản B `hrm-cursor/TanPhatDev`), nhánh `master`. @junfoke
Thiết kế: `design.md` cùng thư mục.

## Phase 0 — Điều tra (XONG)
- [x] Khoanh vùng 2 nguồn số của cột và popup trong `StockTransferReportService`
- [x] Chứng minh bất biến `arriving_qty == SUM(order_stock_progress.qty)` (DB local: 152/153 dòng khớp)
- [x] Tái hiện ca lệch trên DB local (dòng 802, phụ lục KKK-PL.LL id 55 / HĐ gốc 53)
- [x] User chạy SQL prod: xác nhận mã GC-GC-40PRO-A:06 lệch 18 vs 56, 4 dòng sổ cái đều ở bước hợp đồng
- [x] Xác định lỗi 1 (phụ lục lệch id) — `OrderRequest2.php:546-556`
- [x] Xác định lỗi 2 (sai tên trường `buy_contract2_id` trên detail trong nước) — `InlandOrderRequestNew.php:500`
- [x] Đo quy mô prod: 5 dòng nhập khẩu (86→141), 19 dòng trong nước (186→355)

## Phase 1 — Sửa gốc (XONG, user duyệt 10/09)
- [x] Helper `progressRowsOfContractFamily()` — gom bản gốc + phụ lục, trừ lần lượt qua các dòng
- [x] `InlandOrderRequestNew.php:500` — `buy_contract2_id` → `inland_buy_contract_new_id`
- [x] Áp helper cho các điểm phía tồn kho: `OrderRequest2.php:547,567` · `InlandOrderRequestNew.php:500,520`
      · `Invoice2.php:497,519,663,698` · `Invoice2Controller.php:576,598`
      · `InlandBuyContractNewController.php:786,820,1161,1193`
- [x] Không tìm thấy dòng để trừ → `Log::warning` (bỏ pattern bỏ qua im lặng)
- [x] `php -l` sạch, giữ nguyên line ending

## Phase 2 — Hàng rào ở báo cáo (XONG)
- [x] Cột và popup dùng chung một nguồn số để không đá nhau khi sổ cái còn lệch

## Phase 3 — Dọn dữ liệu prod (XONG 10/09, user tự chạy)
- [x] Backup `order_stock_progress_bak_20260910` (52.632 dòng, phải `SET SESSION sql_mode='NO_ENGINE_SUBSTITUTION'`
      + `CREATE TABLE ... LIKE` + `INSERT SELECT` vì có bản ghi `expected_time = '0000-00-00'` làm
      `CREATE TABLE ... AS SELECT` báo lỗi 1292)
- [x] Bảng tạm `osp_fix_20260910` (window function, giữ dòng cập nhật gần nhất) → **26 dòng sổ cái / 24 dòng hàng**
- [x] UPDATE 26 dòng
- [x] Đối chiếu lại: câu (4) ra 0 dòng lệch; `SUM(qty)` của dòng 5798 = 18 = đúng cột
- [ ] User kiểm mã GC-GC-40PRO-A:06 trên báo cáo: cột = popup = 18
- [ ] DROP `osp_fix_20260910` + `order_stock_progress_bak_20260910` sau vài ngày

### Checkpoint — 2026-09-10
Vừa hoàn thành: **Phase 1 + Phase 2 CODE XONG** (6 file, +204/-150, php -l sạch, CRLF nguyên vẹn, CHƯA commit).
- `OrderStockProgress` thêm 3 helper: `contractFamilyIds()` (gốc + phụ lục), `subtractQty()`
  (tra: đúng chứng từ → cùng họ hợp đồng → cùng bước → mọi dòng của dòng hàng, thiếu thì `Log::warning`),
  `addQty()` (tra họ hợp đồng, không có thì tạo mới), `capToQty()` (hàng rào popup).
- Thay **19 điểm trừ** + **6 điểm cộng** (trước đây `if (tìm thấy)` rồi bỏ qua im lặng) ở
  `OrderRequest2`, `InlandOrderRequestNew`, `Invoice2`, `Invoice2Controller`.
- Sửa lỗi sai tên trường `buy_contract2_id` → `inland_buy_contract_new_id` (luồng trong nước).
- `StockTransferReportService`: 4 nhánh popup gọi `capToQty` theo `arriving_qty` của chính dòng hàng.

**Verify trên DB local `erp_dev_30_01_26` (dòng 802, phụ lục KKK-PL.LL id 55 / HĐ gốc 53):**
- `contractFamilyIds(53)` = [54,55,53]; tra từ phụ lục 55 ra cùng họ.
- `subtractQty(HĐ gốc 53, 5)` → trừ đúng dòng nằm ở phụ lục 55 (5→0), tổng sổ cái 10→5 = khớp
  `arriving_qty`; chạy trong transaction rồi rollback, DB không đổi.
- Gọi thẳng `getStockTranfer`: **trước khi sửa popup = 10, sau khi sửa = 5 = đúng cột**; dòng bị bỏ
  là dòng hợp đồng treo, giữ lại phiếu nhập PNH-00211.

Đang làm dở: không.
Bước tiếp theo: user test browser màn báo cáo (mã GC-GC-40PRO-A:06 → cột = popup = 18), rồi
deploy 6 file code + commit. Dữ liệu prod đã dọn xong.
Blocked: không.

### Checkpoint — 2026-09-10 (dọn dữ liệu prod)
Vừa hoàn thành: Phase 3 — user chạy SQL trên prod `erp_new`: backup 52.632 dòng, sửa 26 dòng sổ cái
thuộc 24 dòng hàng, đối chiếu lại 0 dòng lệch, dòng 5798 (mã GC-GC-40PRO-A:06) tổng sổ cái = 18 = cột.
Phần lớn dòng phải cắt nằm ở bước `InlandProductArrivedNew` — khớp với lỗi sai tên trường khiến
luồng trong nước chưa bao giờ trừ sổ cái.
Đang làm dở: không.
Bước tiếp theo: deploy code + user test browser + DROP 2 bảng tạm sau vài ngày.
Blocked: không.
