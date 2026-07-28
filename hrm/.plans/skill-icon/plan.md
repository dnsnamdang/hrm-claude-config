# Plan — Skill Icon

**Owner:** @junfoke
**Spec:** [docs/superpowers/specs/2026-07-27-skill-icon-design.md](../../docs/superpowers/specs/2026-07-27-skill-icon-design.md)

## Task 1 — DB + BE — ✅ DONE
- [x] Migration `2026_07_27_100000_add_icon_to_skills_table.php` (icon VARCHAR(50) nullable) — CHƯA chạy
- [x] Skill entity `$fillable` += 'icon'
- [x] SkillController: KHÔNG cần sửa (store dùng $request->all() + create/update, icon tự lưu qua fillable)
- [x] PublicBrowseController::filterOptions select skills thêm 'icon'
- [x] php -l sạch

## Task 2 — hrm-client — ✅ DONE
- [x] constants/skillIcons.js (SKILL_ICONS 20 icon + DEFAULT_SKILL_ICON='ri-lightbulb-line')
- [x] add_skill_modal.vue: icon-picker (swatch + panel lưới + hint + bỏ chọn) bind data.icon, reset icon:null, accent màu #1abc9c
- [x] skills/index.vue: CỘT "Icon" riêng (mirror màn loại đào tạo) — thêm column 'icon' sau STT + slot #cell-icon (chip icon-chip) + import DEFAULT_SKILL_ICON

## Task 3 — elearning — ✅ DONE
- [x] AppHeader dropdown "Học theo kỹ năng": icon dùng `item.icon || 'ri-lightbulb-line'`
- [ ] Verify browser (user)

## Task 4 — Thẻ loại đào tạo/kỹ năng trên card dùng icon riêng (đồng bộ với dropdown) — ✅ DONE
- [x] BE subjects() + learningPaths(): eager load trainingType thêm 'icon'; skillMap lấy id,name,icon (get→keyBy) + setRelation kèm icon
- [x] SubjectBrowseResource + LearningPathBrowseResource: thêm 'training_type_icon' + 'skill_icon'
- [x] LearnCard + PathCard: thẻ dùng `item.training_type_icon || 'ri-price-tag-3-line'` và `item.skill_icon || 'ri-brain-line'`
- [x] php -l sạch
- [ ] Verify browser (user)
> Mở rộng phạm vi so với quyết định ban đầu (chỉ dropdown) theo yêu cầu user: card cũng dùng icon riêng cho khỏi lệch.

## Task 5 — Màn Học theo danh mục: thêm thẻ kỹ năng trên card — ✅ DONE
- [x] sectionBaseQueries (dùng cho contents/homeSection): eager load thêm 'skill:id,name,icon' + trainingType 'icon' → item contents có skill_name/skill_icon
- [x] CategoryContentsView LearnCard: `:show-skill="true"` (chỉ thẻ kỹ năng, không hiện thẻ loại đào tạo vì thường đã lọc theo danh mục)
- [x] php -l sạch
- [ ] Verify browser (user)

## Task 6 — Fix icon màn danh sách hiện sai (luôn bóng đèn) — ✅ DONE
- [x] Bug: `SkillListResource` (resource whitelist field) thiếu `icon` → FE nhận undefined → rơi về DEFAULT_SKILL_ICON. Modal Sửa đúng vì show() dùng CompanyDetailResource trả full record.
- [x] Fix: thêm `'icon' => $obj->icon` vào SkillListResource

### Checkpoint — 2026-07-28
Vừa hoàn thành: Fix bug icon danh sách kỹ năng (Task 6) — bổ sung `icon` vào SkillListResource.
Bước tiếp: user verify màn Quản lý kỹ năng hiện đúng icon từng kỹ năng.
Blocked:

### Checkpoint — 2026-07-27
Vừa hoàn thành: CODE DONE 3/3 task. BE php -l sạch. Migration CHƯA chạy.
Bước tiếp: user chạy migration `php artisan migrate` → gán icon cho vài kỹ năng ở màn Quản lý kỹ năng → verify dropdown "Học theo kỹ năng" elearning hiện icon riêng.
Blocked:
