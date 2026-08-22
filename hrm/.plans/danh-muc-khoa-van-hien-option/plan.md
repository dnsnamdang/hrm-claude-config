# Plan — Danh mục bị khoá vẫn hiện ở bản ghi đang dùng

## Phase 1 — Giai đoạn dự án (màn dự án tiềm năng)
### BE
- [x] `ProjectPhaseService::getAll` nhận `include_ids` → `where(status=ACTIVE) orWhereIn('id', $includeIds)`

### FE
- [x] `store/optionsSelect.js`: `fetchProjectPhases({ includeIds })` — refetch khi id đang dùng thiếu trong cache, merge options, giữ nguyên tên gốc + cờ `is_locked` (không thêm hậu tố)
- [x] `ProgressFinanceSection.vue`: truyền `includeIds` khi load; watcher `project_phase_id` nạp lại nếu id không có trong options

### Khác
- [x] Thêm quy tắc chung vào `CLAUDE.md` (mục Nguyên tắc chung)

## Phase 2 — 🔒 ở ô đã chọn + chỉ hiện danh mục khoá khi đang dùng (2026-08-20)
### FE
- [x] `utils/select2LockedOption.js`: gắn 🔒 cả `templateSelection` (ô/chip giá trị đã chọn); thêm `filterUnusedLockedOptions` (ẩn option khoá không được dùng) + `mergeLockedOptions`
- [x] `V2BaseSelect` / `V2BaseSelectInModal`: lọc options qua `filterUnusedLockedOptions` trước khi render
- [x] `DescriptionInfoSelect.vue`: tự gắn 🔒 ở `templateSelection` (wrapper có `templateResult` riêng)
- [x] `store/optionsSelect.js`: `fetchProjectPhases` chỉ cache giai đoạn CÒN HOẠT ĐỘNG (bỏ merge), trả về danh sách đầy đủ cho màn dùng
- [x] Thêm `utils/mixins/projectPhaseOptionsMixin.js` (`projectPhaseOptions` + `loadProjectPhaseOptions`)
- [x] Áp mixin: prospective-projects (add/edit qua `ProgressFinanceSection`, index), solutions/index, quotations (index + _id/edit), request-solution (index, pending, RequestTab), my-job/SolutionUpcomingModal
- [x] Dùng giá trị trả về của action: report/meeting-by-projects, report/prospective-projects
- [x] `meeting/index.vue`: bộ lọc Loại meeting gửi `include_ids` theo giá trị đang lọc

### Khác
- [x] Cập nhật `.claude/skills/select-and-input-state/SKILL.md` mục 1 + `CLAUDE.md` (quy tắc 🔒 và cấm cache danh mục khoá vào store)
