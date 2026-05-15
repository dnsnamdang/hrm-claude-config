# Popup chi tiết phát sinh — Công nợ NCC

## Mục tiêu
Click vào số liệu 5 cột (Hàng hoá/DV, ĐCCN tăng, Xuất trả lại, Đã thanh toán, ĐCCN giảm) trên 2 màn báo cáo công nợ NCC → popup hiển thị danh sách phiếu chi tiết.

## Scope
- 2 view: `supplier-debt-details` (trong nước) + `supplier-debt-nation-details` (nước ngoài)
- 1 API endpoint mở rộng: `get-invoiceable-supplier-detail` + param `type`
- Pattern: `BaseSearchModal` (giống customer-debt-details)

## Quyết định
- Dùng chung 1 endpoint cho cả 5 type (param `type` phân biệt)
- Popup hiển thị giống nhau cho mọi type: STT, Số phiếu, Số tiền, Ngày hạch toán, Người lập
- Refactor domestic (đã có 2 cột) + thêm mới foreign (chưa có gì)

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-05-supplier-debt-detail-popup-design.md`
