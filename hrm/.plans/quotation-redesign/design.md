# Thiết kế lại module Báo giá (Quotation) — Tóm tắt

## Mục tiêu

Biến báo giá thành **đối tượng độc lập**, hỗ trợ cả tự xây dựng sản phẩm lẫn kế thừa từ BOM, 1 flow tạo duy nhất, DB sạch cho thống kê.

## Scope

- Thêm luồng tạo báo giá trực tiếp (không qua YCXD giá)
- Hệ thống tự quyết type theo BOM dự án: có BOM → kế thừa, không BOM → tự nhập
- Giữ nguyên luồng YCBG hiện tại, refactor nội bộ service
- Tách `QuotationForm.vue` từ `edit.vue` (2600+ dòng) → component chung cho create + edit
- DB migration backward-compatible (thêm cột, chuyển nullable)

## Quyết định lớn

| Hạng mục | Quyết định |
|---|---|
| Phân loại | `type=1` (từ BOM), `type=2` (tự nhập) + `pricing_request_id` nullable |
| Chọn dự án | Chọn trước → hệ thống tự quyết type |
| Nhiều BOM | Cho Sale chọn từ dropdown |
| Trạng thái | Giữ nguyên 6 trạng thái |
| Quyền tạo | Chỉ Sale phụ trách dự án |
| Tiền tệ | Mặc định VNĐ |
| Kiến trúc BE | Refactor `create()` chung, `createFromPricingRequest()` delegate |
| Kiến trúc FE | Tách `QuotationForm.vue`, thêm `create.vue` wrapper |

## Spec chi tiết

→ Xem `docs/superpowers/specs/2026-05-27-quotation-redesign-design.md`

## Liên quan

- Branch: `tpe-develop-assign`
- Feature gốc: `project-implementation-types` Phase C
- Người phụ trách: @dnsnamdang
