# Plan — 3 báo cáo công nợ khách hàng

> @junfoke · 2026-10-06/07 · nhánh `develop` · Spec: `docs/superpowers/specs/gop-db/2026-10-06-sale-customer-debt-reports-design.md`

## Phase 1 — Hàm chung + Chi tiết công nợ KH (06/10)

- [x] Quyền 1683-1694 (cuối seeder, 4 cấp × 3 màn, type 23) + insert local
- [x] `CustomerDebtAggregator` + `CustomerDebtScope` (dùng chung 3 màn)
- [x] `CustomerDebtDetailReportService` + controller + 4 route `/v1/finance/customer-debt-details`
- [x] FE:
  - `pages/sale/customer-debt-details/`: bảng KH → HĐ, popup chứng từ, Excel chọn trường;
  - `utils/invoiceable-link.js`;
  - menu.
- [x] Đối chiếu ERP: 11 bộ lọc khớp md5 + Tổng cộng + dư đầu kỳ; phạm vi không quyền; popup 9 ca
- [x] Playwright + xem ảnh: bảng, popup, Excel đọc lại
- [x] 07/10: ô = 0 không bấm popup (user chốt giữ chuẩn HRM)

## Phase 2 — Tổng hợp công nợ KH theo nhân viên (07/10)

- [x] Tách lớp cha `AbstractCustomerDebtReportService` (màn Chi tiết chuyển sang, đối chiếu lại vẫn khớp)
- [x] `CustomerDebtScope` thêm `includeOwnUnit` (màn này cộng phòng / bộ phận đang ngồi, y ERP)
- [x] `CustomerDebtByEmployeeReportService` + controller + 3 route `/v1/finance/customer-debt-by-employee`
- [x] Ngày nghiệm thu chỉ tính cho dòng đang hiện (22s → 4,8s)
- [x] FE `pages/sale/customer-debt-by-employee/` + Excel 2 mẫu (chọn trường + mẫu in ERP)
- [x] Đối chiếu ERP 10 bộ lọc khớp; Playwright bảng; Excel đọc lại

## Phase 3 — Bảng đối chiếu công nợ 1 KH (07/10)

- [x] `CustomerDebtCompareReportService` + controller + 5 route `/v1/finance/customer-debt-compare`
- [x] Bỏ HĐ toàn 0 trước rồi mới chia trang (user chốt — ERP trang đầu trống)
- [x] In mẫu 215 (popup xem trước), popup danh sách hàng phiếu xuất / xuất bán mượn, Excel chọn trường
- [x] Đối chiếu ERP 11 trường hợp khớp md5; Playwright bảng / in / popup; Excel đọc lại
- [x] Util chung FE `utils/finance/customerDebtContractLink.js` (3 màn dùng)

## Phase 4 — Verify bằng quyền thật + thao tác thật (07/10)

- [x] User gán quyền tổng công ty (role 18) → Playwright thao tác thật cả 3 màn: gõ ngày, chọn select2 (Số dư cuối kỳ,
      Công ty), tìm KH, Số HĐ + Enter, Ngày nghiệm thu, Làm mới, chuyển trang, popup chứng từ / hàng hóa, In, 4 nút Excel
      (đọc lại file). Số trên màn khớp ERP (20.103 / 2.581 / 281 / 15 / 46 dòng; KH 14951 màn Đối chiếu khớp md5).
- [x] Sửa lỗi: đổi lọc liên tiếp → request cũ về trước tắt "Đang tải" và hiện số kỳ cũ (hoặc về sau đè số mới) ⇒ thêm
      `loadSeq` ở 3 trang, chỉ nhận kết quả lần lọc mới nhất.

## Checkpoint — 2026-10-07

- **Vừa hoàn thành:** cả 3 màn, CHƯA commit (nhánh `develop`).
- **Bước tiếp theo:** chạy SQL quyền 1683-1694 trên server, gán vai trò.
- **Blocked:** không.
