# Plan — Danh mục bị khoá vẫn hiện ở bản ghi đang dùng

## Phase 1 — Giai đoạn dự án (màn dự án tiềm năng)
### BE
- [x] `ProjectPhaseService::getAll` nhận `include_ids` → `where(status=ACTIVE) orWhereIn('id', $includeIds)`

### FE
- [x] `store/optionsSelect.js`: `fetchProjectPhases({ includeIds })` — refetch khi id đang dùng thiếu trong cache, merge options, giữ nguyên tên gốc + cờ `is_locked` (không thêm hậu tố)
- [x] `ProgressFinanceSection.vue`: truyền `includeIds` khi load; watcher `project_phase_id` nạp lại nếu id không có trong options

### Khác
- [x] Thêm quy tắc chung vào `CLAUDE.md` (mục Nguyên tắc chung)
