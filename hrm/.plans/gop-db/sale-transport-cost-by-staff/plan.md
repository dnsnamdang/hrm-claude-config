# Plan — Báo cáo chi phí vận chuyển theo nhân viên kinh doanh

> @junfoke · 2026-10-05 · nhánh `develop` · Spec: `docs/superpowers/specs/gop-db/2026-10-05-sale-transport-cost-by-staff-design.md`

## Phase 1 — BE

- [x] Quyền 1680-1682 (cuối seeder, tên trùng quyền ERP guard web) + insert local
- [x] `Modules/Finance/Services/TransportCostByStaffReportService.php`: 1 tập bút toán gốc (phạm vi + mọi lọc) → 3 cấp, meta, export
- [x] `TransportCostByStaffController` + 3 route `/v1/finance/transport-cost-by-staff` (không gate vào màn)
- [x] Đối chiếu ERP (chạy chính `AccountDetail::transportByStaff*` của ERP trên gop_db, NV 13 quyền tổng công ty)

## Phase 2 — FE

- [x] `pages/sale/transport-cost-by-staff/index.vue` — 8 ô lọc (ngày mặc định đầu tháng → hôm nay), bảng 3 cấp, "Xem chi tiết chuyến xe", Xuất Excel chọn trường
- [x] Menu `sale-hub.js` nhóm Báo cáo › Vận chuyển

## Phase 3 — Verify

- [x] Khớp ERP tuyệt đối (tổng + md5 theo phòng + md5 theo (phòng, NV)): 2 khoảng ngày + 10 bộ lọc (phòng, NV, công ty,
      NV chịu, công ty chịu, YCXH, YCXH + đối tượng, hợp đồng). VD 2025-2026: 1.265.025.853đ / 20 phòng / 109 NV
- [x] Cộng cấp con luôn = cấp cha (cả 3 cấp)
- [x] Phạm vi: NV 13 (tổng công ty) thấy 20 phòng; NV 158 không quyền chỉ thấy cước của mình 18.423.099đ (= ERP lọc NV 158)
- [x] Playwright + xem ảnh: bảng 3 cấp, chi tiết 176 chuyến, link YCXH (HRM) / HĐ hãng (ERP) / phiếu hạch toán (ERP),
      lọc NV chịu 230.046.523đ = ERP, Excel đọc lại đúng 130 chuyến + dòng tổng
- [x] Sửa kèm: chữ "Không có dữ liệu" bị tô đỏ (`.text-muted` trong bảng V2) ở 3 màn báo cáo tự dựng (màn này,
      phân chia thị trường, hàng có thể bán) → màu xám đặt thẳng

## Checkpoint — 2026-10-05

- **Vừa hoàn thành:** Phase 1-3, CHƯA commit (nhánh `develop`).
- **Bước tiếp theo:** chạy SQL quyền 1680-1682 trên server; kế toán xác nhận 215,7 tr cước không mã công việc.
- **Blocked:** không.
