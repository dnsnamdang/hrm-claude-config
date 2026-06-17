# Plan — Redesign màn training/skills theo V2Base

**Người phụ trách:** @khoipv
**Spec:** `docs/superpowers/specs/2026-06-03-skills-v2-redesign-design.md`
**Plan chi tiết (code đầy đủ):** `docs/superpowers/plans/2026-06-03-skills-v2-redesign.md`

## Phase 1 — FE redesign (chỉ hrm-client)

### Task 1: Rewrite `pages/training/skills/index.vue`
- [x] Thay PageHeader+b-table+b-collapse → V2BaseFilterPanel + V2BaseDataTable + V2BaseButton + BaseConfirmModal (layout v2-styles)
- [x] Cột gộp: STT • Kỹ năng (V2BaseTitleSubInfo + icon Sửa/Lịch sử/Xóa inline) • Trạng thái (pill + toggle khóa inline) • Cập nhật (ngày + người)
- [x] Data flow learning-path (loading/pagination/filters watch deep/loadData) — giữ tham số & shape API cũ
- [x] Giữ exportExcel, In, openLogModal + modal log, toggleLock (lock/unlock), deleteItem
- [x] Review prop/slot/event V2 component — đạt (không lỗi runtime)

### Task 2: Rewrite `components/modal/add_skill_modal.vue`
- [x] Restyle theo skill modal-popup (hide-footer + #modal-header icon tròn + modal-footer V2BaseButton)
- [x] Field tên kỹ năng dùng input + V2BaseLabel + validate inline (is-invalid/invalid-feedback/touched)
- [x] Giữ id="add-skill", props/emits/method submitSave/resetModal
- [x] handleApiError set this.formError — khớp; tích hợp id với index.vue OK

### Task 3: Verify regression (CHỜ USER duyệt browser)
- [ ] Compile (npm run dev) không lỗi
- [ ] Thêm mới / Sửa (validate inline) / Excel / In / Lịch sử / Khóa-Mở khóa / Xóa / Phân quyền / Filter & paging

## Không đổi
print.vue, BE, DB, permission, endpoint API.
