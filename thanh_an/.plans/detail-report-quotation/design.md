# Báo cáo chi tiết báo giá — Tóm t��t

## Mục tiêu
Tạo trang báo cáo tổng hợp sản phẩm từ nhiều báo giá (flatten mỗi dòng = 1 sản phẩm), xem trên web + export Excel theo mẫu sheet 2.

## Scope
- FE: `pages/plan/detail-report/index.vue` — bảng 25 cột + export
- BE: 2 endpoint mới (list paginated + export Excel)
- Bộ lọc triển khai sau

## Quyết định chính
- Mỗi row = 1 product từ quotation_tab_products, join ngược lên quotation
- "Ngày kết chuyển" = ngày kết xuất báo giá (rendered_at)
- "Hàng hóa" = import_type (Nhập khẩu / PPL)
- "Mã/Tên nhân viên" = người tạo báo giá (created_by)
- Export Excel dùng Maatwebsite + Blade view

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-05-detail-report-quotation-design.md`

## Phụ trách
@khoipv
