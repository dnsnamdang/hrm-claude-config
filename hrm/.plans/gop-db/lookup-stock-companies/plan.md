# Plan — Báo cáo hàng có thể bán theo công ty

> @junfoke · 2026-10-02 · nhánh `develop` · Spec: `docs/superpowers/specs/gop-db/2026-10-02-lookup-stock-companies-design.md`

## Phase 1 — BE

- [x] `SellableStockReportService`: meta (công ty, kho), search (port `stockCompaniesSearchData`), summary + COUNT trong 1 câu SQL, export
- [x] `IncomingStockService` (popup) — port `getStockTranfer` 7 nguồn + chuỗi chứng từ, trả `{type,id,code}`.
      `stockOrderSources()` là nguồn điều kiện DUY NHẤT cho cả cột "Tồn kho" lẫn popup
- [x] `StockCompanyController` + 4 route `/v1/finance/stock-companies` (không gate quyền)
- [x] Đối chiếu số với chính code ERP chạy trên cùng DB

## Phase 2 — FE

- [x] `pages/lookup/stock-companies/index.vue` — SmartFilterPanel (floating), bảng tiêu đề gộp 3 tầng + dòng tổng, ĐVT theo dòng
- [x] Popup `components/IncomingStockModal.vue` + `StockVoucherCell.vue` + `utils/stock-voucher-link.js` (HRM: YC nhập hàng, ĐN nhập kho, Phiếu nhập hàng; còn lại ERP)
- [x] Xuất Excel (ExportFieldsModal + ExcelJS, cột theo kho bung 5 cột/kho)
- [x] Menu `lookup.js` gắn link mục "Hàng có thể bán theo công ty"; mục "Báo cáo Tồn kho có thể bán,..." giữ không link

## Phase 3 — Verify

- [x] Đối chiếu ERP (script chạy `Product::stockCompaniesSearchData` của ERP trỏ `gop_db`):
      5/5 công ty khớp từng dòng (6.193 / 97 / 393 / 3.278 / 141 dòng, 0 lệch);
      4 tổ hợp lọc (kho con, thương hiệu, tính chất) khớp cả 5 cột theo từng kho (md5 trùng)
- [x] Popup: 11 mặt hàng × 7 nguồn trên `erp_dev_24_09` (có sổ tiến độ) — khớp từng dòng (số phiếu, HĐ, SL, ngày, người lập)
- [x] Tốc độ: 1 trang công ty 1 = 0,84s (ERP 1,17s vì tải hết rồi mới phân trang)
- [x] Playwright + xem ảnh: danh sách, dòng tổng, nhóm kho, đổi công ty (ETEK 141 = ERP), chọn kho, popup, đổi ĐVT (450 Cái → 0.09 Thùng x5000), xuất Excel (đọc lại file)
- [x] Checklist grep skill erp-to-hrm-screen: sạch

Lỗi tự bắt khi verify (đã sửa): `pluck(DB::raw)` không lấy được ngày dự kiến; popup thiếu lọc `arriving_qty > 0`
cho 2 nguồn Tổng hợp; dòng tổng gộp đè 3 cột số; "(Phiếu gốc)" bị tô đỏ; ô Hàng hoá khôi phục từ bộ nhớ lọc gây lọc ngầm.

## Checkpoint — 2026-10-02

- **Vừa hoàn thành:** Phase 1-3, code xong + verify, CHƯA commit (nhánh `develop`, cả 2 repo).
- **Đang làm dở:** không.
- **Bước tiếp theo:** user xem màn trên local/dev; đối chiếu popup trên dev (local `gop_db` không có dòng `order_stock_progress`).
- **Blocked:** quyền xuất Excel ERP id 507 không có trên DB gộp — đang để ai cũng xuất được, chờ user chốt nếu cần gate.
