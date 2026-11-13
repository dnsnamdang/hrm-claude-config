# Plan — Báo cáo bán hàng theo từng mặt hàng

> @khoipv · nhánh `develop` (hrm-api + hrm-client) · spec `docs/superpowers/specs/gop-db/2026-11-13-bao-cao-ban-hang-theo-mat-hang-design.md`

## Phase 1 — Port màn

### BE (hrm-api)
- [x] T1 Catalog quyền: thêm `hrm` vào platforms mã `accounting.bao_cao_ban_hang_theo_mat_hang.view`
- [x] T2 `SaleByProductReportService`: phạm vi 5 mức, union 3 nhánh (+ HĐ HRM), gộp theo hàng, tồn đầu/cuối batch, filter-options, item-list (NVKD + lọc)
- [x] T3 `SaleByProductReportPrintService` + blade in + Excel (bảng chính + popup)
- [x] T4 Controller + route `/v1/finance/sale-by-product-report`
- [x] T5 Smoke test HTTP kernel (tinker) — đối chiếu tổng với ERP query gốc trên cùng kỳ

### FE (hrm-client)
- [x] T6 `pages/sale/sale-by-product-report/index.vue` (bộ lọc floating, kỳ, In/Excel)
- [x] T7 `components/SaleByProductSummary.vue` + `SaleByProductTable.vue`
- [x] T8 `components/SaleByProductDetailModal.vue` (popup: lọc, NVKD, In, Excel)
- [x] T9 Menu `sale-hub.js` → link + codes
- [x] T10 Parse template + babel; báo user phần chưa kiểm trình duyệt

### Kết quả verify (13/11/2026)
- BE: `php -l` sạch; HTTP kernel 7 endpoint 200 (`/`, `filter-options`, `item-list`, `print-list-data`, `item-list/print-list-data`,
  `export`, `item-list/export`), kỳ sai → 422. Ép 5 mức phạm vi + từng bộ lọc (tháng 6/2026): không lỗi SQL; Xuất bán 189.741 +
  KM 4.115 = tổng 193.856 SL thực tế; Excel mở được, `data-format` từng ô.
- FE: parse template + babel 4 file + `sale-hub.js` OK. CHƯA mở trình duyệt (user tự test).
- HĐ HRM: local 0 phiếu xuất kho loại 21 → nhánh HĐ HRM mới kiểm bằng SQL, chưa có số thật.
- Deploy: chạy `php artisan permission:catalog-sync` (bật platform hrm cho mã `accounting.bao_cao_ban_hang_theo_mat_hang.view`).

### Checkpoint — 2026-11-13
Vừa hoàn thành: T1–T10 (BE + FE + menu), code CHƯA commit (hrm-api + hrm-client nhánh develop)
Đang làm dở: —
Bước tiếp theo: user mở `/sale/sale-by-product-report` trên trình duyệt (tài khoản có mã quyền 4 mức) — bấm Mã hàng mở popup, lọc popup, In / Excel 2 nơi
Blocked:

### T11 — Test Playwright trình duyệt thật (13/11/2026, user yêu cầu, chạy --headed) — [x]
- Spec: `e2e/tests/sale/sale-by-product-report.spec.ts` + fixture `e2e/utils/saleByProductFixture.ts` (vai trò quyền tạm + 1 phiếu xuất
  HĐ HRM tạm gắn HĐ #44 + tạm đặt ĐMGG 10% — dọn đúng id / trả NULL ở afterAll, đã kiểm DB sạch).
- Kết quả: **16/16 đạt** (8,3 phút). Phủ: 16 cột (không còn Bảo hành / ĐMGG), số bảng + dòng TỔNG + khối tổng hợp = API, phân trang
  1 request/thao tác, tìm nhanh chờ Enter, nhánh HĐ HRM (giá net theo ĐMGG dòng HĐ, chênh lệch âm đỏ), popup (NVKD, link HĐ HRM →
  /assign/contracts/44, lọc tìm / KH / NVKD, sắp xếp, xoá lọc), In + Excel ở popup và màn chính (mở file kiểm), giữ bộ lọc, Xóa lọc,
  5 mức phạm vi + BE bỏ qua company_id gửi lén.
- **Lỗi thật bắt được + đã sửa:** "In danh sách" trong popup hiện danh sách cột của báo cáo chính → `index.vue` thêm computed
  `printModalColumns` (cột popup khi in từ popup).
- Ghi nhận component chung (không sửa): `V2BasePagination` in tổng số dòng không dấu phân cách ("/ 1832 mặt hàng").

### Checkpoint — 2026-11-13 17:00
Vừa hoàn thành: T1–T11 — port xong BE + FE + menu; test Playwright trình duyệt thật 16/16 đạt; sửa lỗi chọn cột In danh sách của popup (`printModalColumns`)
Đang làm dở: —
Bước tiếp theo: user review + commit 2 repo (hrm-api, hrm-client nhánh develop; e2e spec + fixture nếu muốn giữ); deploy chạy `php artisan permission:catalog-sync`
Blocked:

### Checkpoint — 2026-11-13 (push)
Vừa hoàn thành: commit + rebase lên origin/develop + push — hrm-api `6ce0a92ab`, hrm-client `fb38e3761`; smoke test lại sau rebase đạt
Đang làm dở: —
Bước tiếp theo: deploy chạy `php artisan permission:catalog-sync`; merge develop → gop_db khi team duyệt
Blocked:
