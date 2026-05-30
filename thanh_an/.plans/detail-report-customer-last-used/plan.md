# Plan: Thêm cột "KH sử dụng cuối cùng" — Báo cáo chi tiết báo giá

> Người phụ trách: @khoipv | Ngày: 2026-05-19

## Phase 1 — BE: Thêm field vào API response

- [x] `detailReport()`: thêm select + mapping cho `customer_last_used_name`
- [x] `exportDetailReport()`: thêm select + mapping cho `customer_last_used_name`

## Phase 2 — FE: Hiển thị cột mới

- [x] Thêm `<b-th>` header "KH sử dụng cuối cùng" sau cột "Địa chỉ"
- [x] Thêm `<b-td>` body hiển thị `row.customer_last_used_name`
- [x] Cập nhật colspan empty state: 26 → 27

## Phase 3 — FE: Export Excel

- [x] Thêm column definition vào mảng `columns`
- [x] Thêm field vào `addRow`
- [x] Cập nhật `numCols` index (shift +1)
