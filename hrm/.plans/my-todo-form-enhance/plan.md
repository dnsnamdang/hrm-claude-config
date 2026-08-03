# Plan — Cải tiến form Nhắc việc cá nhân

**Phụ trách:** @khoipv | **Ngày:** 2026-07-17
**Spec:** `docs/superpowers/specs/2026-07-17-my-todo-form-enhance-design.md`
**Plan chi tiết (step-by-step):** `docs/superpowers/plans/2026-07-17-my-todo-form-enhance.md`
**Tóm tắt:** `.plans/my-todo-form-enhance/design.md`

## Tasks

### Phase 1 — BE
- [x] Task 1: `UpdatePersonalTodoRequest` — `list_id` nullable → required + message (đồng nhất Store) — php -l + tinker `LIST_ID_REQUIRED_OK` — review clean

### Phase 2 — FE
- [x] Task 2: Giờ hạn → `vue2-datepicker type=time format=HH:mm value-type=HH:mm` (TodoFormModal.vue) — parse OK — review clean
- [x] Task 3: Danh sách bắt buộc — label*, placeholder "-- Chọn danh sách --", `listState`, invalid-feedback, chặn `onSave` (TodoFormModal.vue) — parse OK — review clean
- [x] Task 4: Nút "Lưu và tiếp tục" (secondary, chỉ Tạo mới) — `onSave(continueAfter)` + `resetForm()` + `saving` chống double-submit (TodoFormModal.vue) + `onSaveTodo({payload,continueAfter})` + `ref="todoModal"` (index.vue) — parse OK — review clean
- [x] Fix 2 Minor (final review): guard re-entry `onSaveTodo` + refocus Tiêu đề sau `resetForm` — parse OK

### Verify (AC) — chờ user chạy browser
- [x] AC1 (code): sao đỏ Danh sách + giờ 24h — ⏳ verify hiển thị "14:00" trên browser
- [x] AC2: bỏ trống Danh sách → chặn (FE inline + BE required)
- [x] AC3 (code): "Lưu và tiếp tục" → toast + lưu DB + modal mở + reset trống + focus Tiêu đề — ⏳ verify UI
- [x] AC4: "Lưu" → lưu + đóng modal
- [x] AC5: màn Sửa đồng nhất (Update required + giờ 24h)

## Checkpoint
### Checkpoint — 2026-07-17 (2)
Vừa hoàn thành: CODE DONE Task 1-4 + fix 2 Minor (subagent-driven, Opus). Từng task review clean (spec ✅ / quality Approved). Final whole-branch review: READY, không Critical/Important. Verify: php -l + tinker (BE), parse-check vue-template-compiler + @babel/parser (FE) — tất cả pass. KHÔNG commit (theo rule).
Đang làm dở: —
Bước tiếp theo: user bật FE dev server (3000) verify browser AC1 (giờ hiển thị 24h "14:00" theo locale) + AC3 (reset field trống + focus Tiêu đề sau "Lưu và tiếp tục"). Có thể nhờ Claude drive Playwright nếu server chạy.
Blocked:

### Checkpoint — 2026-07-17 (1)
Vừa hoàn thành: Brainstorming + Spec + Plan chi tiết (brainstorming → writing-plans).
Bước tiếp theo: bắt đầu Task 1 (BE UpdatePersonalTodoRequest).
