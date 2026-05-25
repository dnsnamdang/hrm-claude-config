# Tab "Dữ liệu liên quan" trên Báo giá — Tóm tắt

## Mục tiêu
Thay tab input thủ công bằng tab read-only tự động lấy chứng từ liên quan (Dự toán/Thầu/Hợp đồng) dựa trên `project_id` của báo giá. Giống pattern trên dự toán.

## Scope
- BE: endpoint `GET /v1/category/quotations/{quotation}/related-data`
- FE: component `QuotationRelatedDataComponent.vue` + sửa `GeneralComponent.vue`

## Quyết định lớn
- Tạo endpoint riêng trên QuotationController (không reuse endpoint Project để tránh circular reference)
- Xóa hoàn toàn input thủ công cũ (không cần migration — data cũ inline, không lưu DB riêng)
- Hiện bảng trống khi chưa gắn dự toán

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-25-quotation-related-data-design.md`
