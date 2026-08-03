# Báo cáo tổng hợp nhu cầu mua hàng — Design (tóm tắt)

- **Phân hệ:** Cung ứng — màn thứ 3 (`pages/supply/reports/purchase-demand`)
- **Nguồn demo:** `hrm-thanhan-client/bao_cao_nhu_cau_mua.html`
- **Spec chi tiết:** `docs/superpowers/specs/2026-07-13-bao-cao-nhu-cau-mua-design.md`

## Mục tiêu
Tổng hợp **nhu cầu mua hàng** theo từng mã hàng, gom từ các dòng "Mua hàng" (`alloc_mua`) trong **Phiếu xử lý cung ứng** đã duyệt → hỗ trợ quyết định mua.

## Quyết định lớn (đã chốt)
1. **Phạm vi:** build đủ khung như demo; chỉ cột "SL đề xuất mua" có dữ liệu thật. Cột tồn kho / tồn thầu / HĐ mua NCC **giữ cột, hiển thị `—`** (chờ module). 2 nút hành động + lọc NCC/HĐ mua **ẩn**.
2. Chỉ tính phiếu xử lý **status = 5** (Đã duyệt/Đã xử lý).
3. "Người đề xuất" = người lập **Đề xuất cung ứng** gốc (`supply_proposals.created_by`).
4. Thêm **1 quyền mới** "Xem báo cáo tổng hợp nhu cầu mua hàng". **Không** phân quyền cấp.
5. **Xuất Excel:** FE (ExcelJS).
6. **Không migration mới** — tổng hợp từ bảng sẵn có.

## Kiến trúc
- **BE:** `SupplyReportController` + `SupplyReportService` (mới), route `GET supply/reports/purchase-demand`. Gom `supply_handling_products.alloc_mua>0` ⋈ `supply_handlings (status=5)` ⋈ `supply_proposals` ⋈ `users`, group theo `product_id`.
- **FE:** `pages/supply/reports/purchase-demand/index.vue` + menu. KPI + filter + bảng khối/mã hàng (rowspan) + popup chi tiết + tooltip + xuất Excel.

## Ngoài phạm vi
Module tồn kho, tồn thầu chuẩn, HĐ mua NCC, 2 nút hành động, phân quyền cấp, Excel BE.
