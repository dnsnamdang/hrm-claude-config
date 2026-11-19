# Plan — Báo cáo tồn kho tổng hợp theo mặt hàng

> Phụ trách: @khoipv · nhánh `develop` (con của `gop_db`, cả hrm-api + hrm-client)

## Phase 1 — Port màn

### BE
- [x] Chụp số liệu màn Chi tiết TRƯỚC khi tách hàm (3 kho lớn nhất × 2 ngày)
- [x] Tách `WarehouseStockReportService` (dùng chung): 3 quyền + phạm vi kho, danh mục công ty/kho, đọc ngày/mảng, bộ lọc hàng hóa,
      `aggregate()` (cộng `stock_logs` theo công ty thuê, NHIỀU kho), `unitsOf()`
- [x] `StockDetailByProductReportService` gọi lại service chung (giữ nguyên API public) — số trước/sau khớp TỪNG BYTE (6 bộ);
      options / index / print / export / 422 của màn Chi tiết vẫn chạy
- [x] `StockGeneralProductReportService`: options + context (nhiều kho) + report (trang theo mặt hàng, cột theo công ty thuê)
- [x] `StockGeneralProductPrintService` + `StockGeneralProductExport` + 2 blade (Đầy đủ / Ngắn gọn), ĐVT theo lựa chọn từng hàng (`units`)
- [x] Controller + route `/v1/finance/stock-general-product`
- [x] Smoke test: options / index / print (6.256 dòng > trần 2.000 → `truncated`) / export 2 kiểu (đọc lại xlsx: tiêu đề, Kho, 2 tầng
      tiêu đề, số `#,##0`, khối ký), 422 thiếu kho, 403 tài khoản không quyền (cả 3 endpoint)
- [x] Đối chiếu số với hàm ERP gốc `Product::warehouseReportGeneralSearchData` (cùng DB gop_db), công ty 1 / 7 kho: hôm nay (6.256 hàng),
      31/03/2026 (6.230), 2 kho + 1 công ty thuê (415), lọc thương hiệu (573) — khớp 100% SL tồn + từng cột công ty; thứ tự khớp trừ
      2 hàng trùng tên khác hoa/thường (ERP chỉ ORDER BY name)

### FE
- [x] `pages/warehouse/stock-general-product/index.vue` (khuôn màn Chi tiết)
- [x] `components/StockGeneralSummary.vue`, `components/StockGeneralTable.vue` (bảng phẳng, tiêu đề 2 tầng "Chi tiết" theo công ty thuê)
- [x] Menu Kho › Báo cáo kho có link
- [x] Parse template/script (vue-template-compiler + babel) + grep tự kiểm của skill erp-to-hrm-screen
- [x] Test Playwright (23/10, local, DNS Admin — Super admin), 2 lỗi phát hiện + đã sửa:
      · ô "Xem toàn bộ kho" KHÔNG hiện — V2BaseCheckbox có slot mặc định thì chuyển chế độ nhiều ô → nhãn qua prop `label`
      · ô Kho chip "mã - tên" tràn 3 dòng (hàng lọc cao 98px) → nhãn = mã kho như ERP (hàng lọc 55px)
      Đạt: vào màn 2 request (options + báo cáo); bỏ tick → xoá kho, không gọi API; tick lại → đủ 7 kho; bỏ 1 kho bằng x → bỏ tick,
      1 request; đổi công ty → đủ kho + công ty thuê công ty mới; Tìm kiếm khi trống kho → đỏ "Vui lòng chọn kho", không gọi API;
      Xóa lọc → về mặc định; popup chọn hàng → 1 hàng (29,640 khớp DB); đổi ĐVT Hộp x40 → 741 cả SL tồn lẫn cột TPE, không gọi API;
      In Đầy đủ → `units=3923:44`, bản xem trước letterhead + 2 tầng + 741; Xuất Excel UI → file có logo, Hộp (x40) 741 `#,##0`,
      popup tự đóng; F5 giữ hàng đã chọn; x xoá hàng; tiêu đề 2 tầng dính khi cuộn; trang 2 (STT 21–40), 50 dòng/trang → trang 1;
      1366px tiêu đề 1 dòng, trang không cuộn ngang
- [ ] Ca quyền "theo công ty" / "theo kho" (không thấy nhóm Chi tiết): DB local chưa có 3 quyền → cần `php artisan permission:sync`
      (việc treo chung với màn Chi tiết) + gán vai trò cho 1 tài khoản test

### Fix #11874 (tester 26/10/2026)
- [x] 1. ĐVT luôn là ô chọn trên mọi hàng như ERP (kể cả hàng 1 ĐVT — trước hiện chữ trơn) — `StockGeneralTable.vue`
- [x] 2. Ô Hàng hóa trông như chọn nhiều (chip) mà chỉ giữ 1 hàng -> chữ thường + dấu x riêng (khuôn màn Chi tiết #11869)
- [x] 3. Bản in: dòng ngày lệch "Người lập báo cáo" — đã sửa ở layout chung `finance::prints._layout` (#11872), không sửa thêm

### Checkpoint — 23/10/2026
Vừa hoàn thành: Phase 1 BE + FE, số liệu khớp ERP 100%; tách service dùng chung, màn Chi tiết không đổi số; test Playwright đạt
Đang làm dở: —
Bước tiếp theo: chạy `permission:sync` + thử tài khoản quyền "theo công ty" / "theo kho"
Blocked:

## Tài liệu SRS / HDSD / Testcase (07/11/2026) @khoipv

- [x] Đọc brief + skill srs-documenter / hdsd-documenter / testcase-documenter; đọc code FE `pages/warehouse/stock-general-product/**`, BE `StockGeneralProduct*` + `WarehouseStockReportService`; khuôn chép `../bao-cao-ton-kho-chi-tiet-mat-hang/` + `../bao-cao-ton-kho-theo-vi-tri/`
- [x] Chụp ảnh dev-hrm (DNS Admin, `bctkth_shots/_capture/capture.js`, hồ sơ đăng nhập riêng, chặn mọi yêu cầu ghi — lọt 0; màn chỉ có API GET) — công ty CN Hải Phòng, 4 kho CB / HP / KĐN-ALM / NM (96 mặt hàng, cột Chi tiết TPE / TPHP / TPV); 37 icon (`trim_icon --dry` 0/37). Popup Chọn hàng hóa chụp với công ty TPE (CN Hải Phòng dev báo 403 ở `product-picker/tree-counts` + `search`)
- [x] Đối soát số dev (`_capture/doisoat.js`, chỉ GET): ENEO-700-V5231 kho HP / TPHP = 20 = Báo cáo chi tiết theo mặt hàng (20) = Báo cáo theo vị trí (KHOANG1 20) = Thẻ kho 01/01–07/11/2026 (70 + 496 − 546); 31/12/2025 = 70 ở cả 2 báo cáo; 4 kho CN HP = 47 = HP 20 + CB 27. ENEO-640-V5236 kho PTT / TPE = 3,197 = chi tiết = vị trí = Thẻ kho Năm nay (15,141 + 11,404 − 23,348); 31/12/2025 = 15,141 = tồn đầu kỳ. 96/96 dòng: SL tồn = tổng cột công ty — KHỚP
- [x] `gen_srs.py` → `SRS - Báo cáo tồn kho tổng hợp theo mặt hàng.docx` (69 trang, 7 chức năng, selfcheck khớp mẫu; metrics ui=13.0 ev=5.1 evch=1159 intro=2018; Phần 5 bảng 4 cột 16 dòng; Mục lục trang riêng căn giữa)
- [x] `gen_hdsd.py` → `HDSD_Bao cao ton kho tong hop theo mat hang.docx` (11 trang, 6 phần)
- [x] `gen_testcase.py` → `testcase.xlsx` (128 TC, 8 nhóm, P0 41,4%, check_tc `bao_cao` 0 lỗi)
- [x] `gen_checklist.py` → `Đối chiếu checklist.xlsx` (Testcase 103 có TC / 221 N/A; SRS 79 có mục / 84 N/A)
- [x] Ghi nhận nghi lỗi (chưa sửa): popup Chọn hàng hóa lỗi 403 khi Tồn theo công ty ≠ công ty đăng nhập (giống 2 màn anh em); ô Hợp đồng không thoát `%` `_` (gõ "%" ra 3.939 / 6.157 mặt hàng công ty TPE); quyền theo công ty / theo kho không thấy nhóm Chi tiết trên màn nhưng In / Excel Đầy đủ vẫn có (giữ y ERP — ghi rõ trong tài liệu, cần user xác nhận)

### Checkpoint — 07/11/2026
Vừa hoàn thành: bộ SRS + HDSD + Testcase + Đối chiếu checklist màn Báo cáo tồn kho tổng hợp theo mặt hàng
Đang làm dở: —
Bước tiếp theo: user xem tài liệu; quyết định có sửa 3 điểm nghi lỗi không; đẩy Drive khi user yêu cầu
Blocked:
