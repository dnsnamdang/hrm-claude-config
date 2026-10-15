# Tự sinh PLHĐ theo mẫu in chọn trong QĐ (#10894) — Tóm tắt

**Người phụ trách:** @junfoke — 2026-10-09 · Nhánh `gop_db`
Spec đầy đủ: [docs/superpowers/specs/gop-db/2026-10-09-decision-appendix-print-template-design.md](../../../docs/superpowers/specs/gop-db/2026-10-09-decision-appendix-print-template-design.md)

## Mục tiêu
Bật lại tự sinh Phụ lục HĐLĐ khi duyệt QĐ bổ nhiệm / điều chuyển / điều chỉnh lương / tăng lương thâm niên
(tắt từ 13/07/2026, commit `aac01d75c`), nhưng sinh theo **mẫu in PLHĐ chọn ngay trong QĐ** đúng Redmine #10894.

## Scope
- DB: `hrm_print_templates.appendix_decision_type`; `decisions.appendix_print_template_id` + `appendix_print_template`.
- Danh mục mẫu in: trường + bộ lọc "PLHĐ của quyết định".
- 4 màn QĐ: tab "Mẫu in PLHĐ" (component riêng `FormAppendixPrintTemplateComponent`).
- Duyệt QĐ: gọi lại tự sinh, dùng mẫu của QĐ; thiếu mẫu → chặn duyệt (422).
- Sửa PLHĐ trùng khi duyệt lại QĐ tăng lương thâm niên.

## Quyết định chính (user chốt 09/10/2026)
- QĐ cũ chưa có mẫu PLHĐ → **chặn duyệt**, người duyệt Từ chối để người tạo bổ sung.
- **Không sinh bù** PLHĐ cho QĐ đã duyệt 13/07 → nay.
- **Không sửa** `FormPrintTemplateComponent` dùng chung (~30 màn).
