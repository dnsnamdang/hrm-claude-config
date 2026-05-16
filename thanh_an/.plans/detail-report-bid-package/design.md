# Báo cáo chi tiết thầu — Design Summary

## Mục tiêu
Tạo màn báo cáo chi tiết gói thầu, tương tự báo cáo chi tiết báo giá nhưng source từ `bid_packages` + `bid_package_products`.

## Scope
- BE: API endpoint `GET category/bid_packages/detail-report` (paginated) + phân quyền 3 cấp + 9 filters
- FE: Page `pages/bid_package/detail-report/index.vue` với bảng 27 cột + export Excel client-side

## Khác biệt so với báo cáo báo giá
- Source: `bid_packages` thay vì `quotations`
- Thêm 2 cột: "Số hợp đồng bán", "Tên hợp đồng" (join `contracts`)
- Thêm 2 filter: "Số hợp đồng bán", "Trạng thái gói thầu"
- Status map khác (gói thầu có flow riêng)

## Quyết định
- Export Excel bằng ExcelJS phía client (giống báo giá)
- Permission naming: "Xem báo cáo chi tiết thầu theo [cấp]"
- Join contracts: `LEFT JOIN contracts ON contracts.bid_package_id = bid_packages.id`

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-06-detail-report-bid-package-design.md`

## Phụ trách
@khoipv
