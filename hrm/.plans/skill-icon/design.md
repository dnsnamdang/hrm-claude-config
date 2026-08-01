# Skill Icon — Icon riêng cho từng kỹ năng

**Owner:** @junfoke — **Ngày:** 2026-07-27
**Spec:** [docs/superpowers/specs/2026-07-27-skill-icon-design.md](../../docs/superpowers/specs/2026-07-27-skill-icon-design.md)

## Mục tiêu
Mirror cơ chế icon của TrainingType sang Skill: mỗi kỹ năng chọn icon riêng (icon-picker ở màn quản lý), hiển thị ở dropdown "Học theo kỹ năng" trên header elearning.

## Quyết định
- Bộ icon riêng cho kỹ năng (`skillIcons.js`, default `ri-lightbulb-line`).
- Elearning chỉ hiển thị icon ở dropdown "Học theo kỹ năng" (không đụng card/API browse).

## Phạm vi
- DB: migration thêm `skills.icon` (không tự chạy).
- BE Training: Skill fillable + SkillController store/update + filterOptions select icon.
- hrm-client: skillIcons.js + icon-picker trong add_skill_modal.vue + cột Icon ở skills/index.vue.
- elearning: AppHeader dropdown kỹ năng dùng item.icon.
