# Plan — Độ khó khóa học (Course Level)

- **Người phụ trách:** @junfoke
- **Plan chi tiết:** [docs/superpowers/plans/2026-06-09-course-level.md](../../docs/superpowers/plans/2026-06-09-course-level.md)
- **Spec:** [docs/superpowers/specs/2026-06-09-course-level-design.md](../../docs/superpowers/specs/2026-06-09-course-level-design.md)

## Tiến độ (tổng quát)

### BE (hrm-api)
- [x] Task 1 — Migration cột `level` + hằng `Subject::LEVELS` + accessor `level_name`
- [x] Task 2 — Validate `SubjectBuilderRequest` (required khi publish) + lưu ở `SubjectService`
- [x] Task 3 — `SubjectDetailResource` + `SubjectBrowseResource` trả `level`/`level_name`
- [x] Task 4 — `PublicBrowseController`: `filterOptions` trả `levels` + filter `level`

### FE admin (hrm-client)
- [x] Task 5 — `TabInfo.vue` dropdown Độ khó (bắt buộc) + `SubjectBuilderForm` default/payload/validate

### FE elearning (Vue 3)
- [x] Task 6 — `filterOptions` store + sidebar filter (category/skill) + `LearnCard` + `subjectDetail` map level thật. Bonus: `DetailHero.vue` đã có `v-if="entity.level"` nên null tự ẩn.
  - UX chốt (2026-06-09): độ khó hiển thị ở **hàng metadata dưới card** (`Trung cấp • 80 phút • 4.4`) thay vì badge banner — gọn, nhất quán demo, ẩn khi null.

### Verify
- [ ] Task 7 — Checklist browser thủ công (sau khi user chạy migrate)

### Checkpoint — 2026-06-09
Vừa hoàn thành: Toàn bộ code BE + FE admin + FE elearning (Task 1-6) qua subagent-driven, đã review từng nhóm.
Đang làm dở: Không.
Bước tiếp theo: User chạy `php artisan migrate` (hrm-api) → verify browser theo checklist Task 7.
Blocked: Build/eslint không chạy được tại máy do Node 14 (Vite 5/eslint cần Node ≥18) — verify cú pháp đã làm thủ công, build thật chạy trong Docker.

> Lưu ý: KHÔNG tự chạy `php artisan migrate` — báo user chạy.
