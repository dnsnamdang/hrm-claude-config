# Ghi note cho học viên bên ngoài theo từng buổi — @namdangit

## Mục tiêu
Ở tab "Điểm danh học viên" (màn chi tiết khoá học), phần "2. Học viên bên ngoài": cho phép người quản lý ghi note cho từng học viên ở từng buổi điểm danh (không bắt buộc).

## Scope
- Note gắn theo **từng bản ghi điểm danh** (học viên × buổi). Chỉ ghi được cho ô đã có bản ghi (status ≠ 0). Ô `-` (chưa điểm danh) không hiện icon note.
- UI: icon 📝 trong mỗi ô buổi; click mở modal textarea; ô có note → icon nổi bật.

## Thay đổi chính
- DB: thêm cột `note` (text nullable) vào `course_student_attendances`.
- Model: thêm `note` vào `$fillable`.
- BE đọc: `getClientAttandance` select thêm `note`; `CourseClientAttendanceTransformer` expose `note`.
- BE ghi: route mới `POST training/courses/student-attendance/{id}/note` (auth:api, không checkPermission — mirror route approve) → service update note.
- FE `CourseFormShow.vue`: computed `clientAttendanceGroupBy` mang thêm `note` vào từng ô; thêm icon + modal + handler lưu → reload list.

## Spec chi tiết
`docs/superpowers/specs/2026-07-09-course-attendance-note-design.md`
