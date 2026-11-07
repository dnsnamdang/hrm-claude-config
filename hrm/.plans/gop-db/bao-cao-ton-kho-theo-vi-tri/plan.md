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

## Tài liệu SRS / HDSD / Testcase (07/11/2026) @khoipv

- [x] Đọc brief + skill srs-documenter / hdsd-documenter / testcase-documenter; đọc code FE `pages/warehouse/stock-location-product/**` (+ ScopePicker), BE `StockLocationProduct*` + `WarehouseStockReportService`; khuôn chép `../bao-cao-ton-kho-chi-tiet-mat-hang/`
- [x] Chụp ảnh dev-hrm (DNS Admin, `bctkvt_shots/_capture/capture.js`, hồ sơ đăng nhập riêng, chặn mọi yêu cầu ghi — lọt 0; màn chỉ có API GET) — kho HP - Hải Phòng (8 vị trí, 96 mặt hàng, tổng SL 8,530); ảnh bảng chụp với khối lọc thu gọn; 40 icon (`trim_icon --dry` 0/40). Popup Chọn hàng hóa chụp với công ty TPE (CN Hải Phòng dev báo "Không tải được số lượng")
- [x] Đối soát số dev (`_capture/doisoat.js`, chỉ GET): ENEO-700-V5231 kho HP / TPHP — chỉ ở KHOANG1 = 20 (4 lô 6+2+6+6) = Báo cáo tồn kho chi tiết theo mặt hàng (20) = Thẻ kho 01/01–07/11/2026 (70 + 496 − 546 = 20); ngày 31/12/2025: 70 ở cả 2 báo cáo, lô cắt theo ngày (30+1+3+30+6). 8/8 vị trí: SL vị trí = tổng các dòng hàng hóa — KHỚP
- [x] `gen_srs.py` → `SRS - Báo cáo tồn kho theo vị trí.docx` (75 trang, 7 chức năng, selfcheck khớp mẫu; metrics ui=15.4 ev=5.4 evch=1290 intro=2064; Phần 5 bảng 4 cột 16 dòng; Mục lục trang riêng căn giữa)
- [x] `gen_hdsd.py` → `HDSD_Bao cao ton kho theo vi tri.docx` (11 trang, 6 phần)
- [x] `gen_testcase.py` → `testcase.xlsx` (134 TC, 8 nhóm, P0 41,8%, check_tc `bao_cao` 0 lỗi)
- [x] `gen_checklist.py` → `Đối chiếu checklist.xlsx` (Testcase 103 có TC / 221 N/A; SRS 79 có mục / 84 N/A)
- [x] Ghi nhận nghi lỗi (chưa sửa): ô Lô cắt chữ (nowrap + ẩn tràn) nên mã lô dài che mất "Hợp đồng: <mã>" và liên kết hợp đồng — chỉ còn xem được khi rê chuột; popup Chọn hàng hóa không tải được số lượng khi Tồn theo công ty ≠ công ty đăng nhập (dev, CN Hải Phòng — giống màn Chi tiết); ô Hợp đồng không thoát ký tự `%` `_`

### Checkpoint — 07/11/2026
Vừa hoàn thành: bộ SRS + HDSD + Testcase + Đối chiếu checklist màn Báo cáo tồn kho theo vị trí
Đang làm dở: —
Bước tiếp theo: user xem tài liệu; quyết định có sửa 3 điểm nghi lỗi không; đẩy Drive khi user yêu cầu
Blocked:
