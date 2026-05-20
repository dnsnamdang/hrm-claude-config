# Thêm cột "KH sử dụng cuối cùng" — Báo cáo chi tiết báo giá

> Spec chi tiết: `docs/superpowers/specs/2026-05-19-detail-report-customer-last-used-design.md`

## Mục tiêu
Thêm cột `customer_last_used_name` vào màn plan/detail-report, hiển thị trên web + export Excel.

## Scope
- Dùng field có sẵn trong bảng `quotations` — không cần migration
- Vị trí: sau cột "Địa chỉ"
- Tổng cột: 26 → 27

## Quyết định
- Dùng `customer_last_used_name` trực tiếp, không join sang bảng customers
- Không thêm filter mới cho cột này
