# Course Rebuild Subject — Design (tóm tắt)

**Ngày:** 2026-04-22 · **Owner:** @manhcuong · **Spec đầy đủ:** [docs/superpowers/specs/2026-04-22-course-rebuild-subject-design.md](../../docs/superpowers/specs/2026-04-22-course-rebuild-subject-design.md)

## Mục tiêu
Rebuild FE màn tạo/sửa `subjects` (module Training) theo prototype `hrm-client/pages/training/subjects/Course_create.html` — 4 tab đầy đủ. Đổi label "Môn học" → "Khoá học" **chỉ trên các màn trực tiếp** của subjects + sidebar. Downstream (training_programs, courses, training_plans, reports) giữ nguyên label + logic cũ. BE thêm cột/bảng mới hỗ trợ tính năng còn thiếu, migrate data cũ.

## Scope
- **FE:** rebuild `SubjectBuilderForm.vue` thành shell + 4 sub-tab (TabInfo, TabEvaluation, TabLearners, TabCertificate). Rename label trên toàn bộ file trong `pages/training/subjects/`. Xoá `SubjectForm.vue` (deprecated).
- **BE:** thêm 12 cột vào `subjects` + 4 bảng mới (`subject_exams`, `subject_exam_graders`, `subject_assignees` polymorphic, `subject_certificate_fields`). Refactor `SubjectService` + `SubjectBuilderRequest`. Upload ảnh cert template dùng endpoint chung `POST /files/upload` (giống `FileAttachmentTable.vue`), không thêm route mới.
- **Migration:** 7 file — schema + backfill (`evaluation_config` JSON → `subject_exams`; `working_position_subjects.is_encouraged` + `capability_subjects` → `subject_assignees`) + rename permission `Quản lý môn học` → `Quản lý khoá học`.

## Quyết định chính
- **Approach 1 (normalize):** tách bảng mới thay JSON `evaluation_config`. Giữ `evaluation_config` cho backward-compat, không xoá.
- **Polymorphic `subject_assignees`:** 1 bảng cho 3 loại (department/position/capability) với `is_mandatory` flag.
- **Status:** thêm giá trị `3=DRAFT`. Lưu tạm = status=3, skip hầu hết validation.
- **Certificate template URL:** cột string trên `subjects` (không dùng bảng `files`).
- **Upload ảnh cert:** endpoint riêng (upload trước → URL → submit sau).
- **Downstream không đổi:** Export Excel, auto-assign onboarding job, render PDF cert thực — tất cả out-of-scope.
- **Permission:** rename string (không đổi ID), seeder cập nhật đồng bộ.

## Phase tổng quát
P1 Schema · P2 Entity/Resource · P3 Service · P4 Controller/Route · P5 Permission rename · P6 FE shell + rename label · P7 Tab 1 · P8 Tab 2 · P9 Tab 3 · P10 Tab 4 · P11 Sidebar + index · (P12 Testcase UI tạm skip)

## Downstream impact
Không có. Các pivot cũ giữ nguyên, subjects id/code/name không đổi.
