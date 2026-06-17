# Redesign màn `training/skills` theo V2Base — Tóm tắt

**Người phụ trách:** @khoipv
**Spec chi tiết:** `docs/superpowers/specs/2026-06-03-skills-v2-redesign-design.md`

## Mục tiêu
Đổi giao diện màn `pages/training/skills/index.vue` cho giống `pages/training/learning-path/index.vue`, dùng bộ component V2Base. **Chỉ FE**, không đổi BE/DB/API/permission.

## Scope
- `index.vue`: `PageHeader + b-table + b-collapse` → `V2BaseFilterPanel` + `V2BaseDataTable` + `V2BaseButton` + `BaseConfirmModal`, layout `v2-styles`.
- Cột gộp kiểu learning-path: STT • Kỹ năng (V2BaseTitleSubInfo + icon hành động inline) • Trạng thái (pill + toggle khóa inline) • Cập nhật (ngày + người).
- Modal Thêm/Sửa: **giữ modal** `add_skill_modal.vue` (chỉ dùng riêng màn này), restyle V2 + validation inline (`is-invalid`/`invalid-feedback`/`touched`).
- Giữ tính năng: Xuất Excel, In, Lịch sử thay đổi, Khóa/Mở khóa.

## Quyết định đã chốt
1. Form thêm/sửa: giữ modal, restyle V2Base.
2. Tính năng phụ: giữ tất cả (Excel, In, Lịch sử, Khóa/Mở khóa).
3. Cột: gộp kiểu learning-path.

## Không đổi
`print.vue`, BE, DB, permission, endpoint & tham số API (FE map filter mới về tham số cũ).
