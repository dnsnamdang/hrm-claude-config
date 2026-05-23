# Mẫu in riêng cho hợp đồng lao động — Tóm tắt

> Người thực hiện: @khoipv · 2026-05-22

## Mục tiêu

Mỗi hợp đồng lao động lưu bản mẫu in riêng thay vì dùng chung FK tới `print_templates`. Sửa mẫu gốc không ảnh hưởng hợp đồng cũ.

## Scope

- Thêm cột `print_template` (longText) vào `employment_contracts`
- Migration backfill data cũ từ `print_templates` table
- FE: layout 2 tab (Thông tin HĐ + Mẫu in với CKEditor + bảng biến)
- BE: logic in ưu tiên bản riêng, fallback về `print_template_id`

## Quyết định lớn

- Clone pattern từ `contract/contract` (3 field: type_id, template_id, template content)
- Migrate tự động cho data cũ — snapshot nội dung tại thời điểm chạy migration
- CKEditor cho phép chỉnh sửa (không phải snapshot read-only)

## Spec chi tiết

→ `docs/superpowers/specs/2026-05-22-employment-contract-print-template-design.md`
