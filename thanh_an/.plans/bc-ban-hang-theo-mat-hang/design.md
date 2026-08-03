# Báo cáo bán hàng theo mặt hàng — Design (tóm tắt)

> @khoipv · Tạo 2026-07-02 · Trạng thái: **Chờ user review spec**

## Mục tiêu
Báo cáo bán hàng dạng **cây 3 cấp** gom **theo mặt hàng**
(Hàng hoá › Khách hàng › Luồng bán hàng), 4 giai đoạn Báo giá → Thầu → Hợp đồng → Thực xuất bán.
Theo mẫu `bc_banhang_theo_mathang.html`, UI đồng bộ `sale/report-project-contract`.

Menu (đã có): `/contract/reports/sale-product` → trang mới `pages/contract/reports/sale-product/index.vue`.

## Quyết định lớn
- **A1**: Giữ đủ 4 giai đoạn; cột **Thực xuất bán để trống** (=0/`–`), chờ dữ liệu sau.
- **A2**: Chỉ **1 quyền** `Xem báo cáo bán hàng theo mặt hàng` (không tách 3 cấp).
- **A2b (giả định)**: Không lọc dữ liệu theo cấp — ai có quyền xem toàn bộ (chờ xác nhận).
- **A3**: Có xuất Excel (ExcelJS).

## Kỹ thuật chốt
- Luồng "hd" neo theo từng Hợp đồng; chuỗi lấy qua FK `contract.quotation_id / bid_package_id / project_id`.
- Luồng "pipeline" cho mặt hàng đã báo giá nhưng KH chưa ký HĐ.
- Show-once BG/Thầu khi nhiều HĐ dùng chung.
- BE: 1 method `saleProductReport` + 1 route + 1 permission (seeder). Không migration.
- FE: cây flatten + collapse, drill-down tái dùng endpoint có sẵn.

## Link
- Spec chi tiết: `docs/superpowers/specs/2026-07-02-bc-ban-hang-theo-mat-hang-design.md`
