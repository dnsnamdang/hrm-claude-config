# Plan — Bỏ bắt buộc Ngày sinh & SĐT cho giảng viên thuê ngoài (Redmine #11409)

Owner: @junfoke — Bug Redmine http://quanly.dnsmedia.vn/issues/11409

## Phase 1 — Bỏ required cho type = 2 (Giảng viên thuê ngoài)

### BE (hrm-api)
- [x] `TeacherController::store` — `employee.birthday` → `required_if:type,1|nullable|date`
- [x] `TeacherController::store` — `employee.telephone` → `required_if:type,1` + `nullable`, closure check trùng thoát sớm khi rỗng
- [x] `TeacherController::update` — sửa tương tự 2 trường trên
- [x] Đổi key message `.required` → `.required_if` cho birthday/telephone (cả store & update)
- [x] Gán dữ liệu dùng `?? null` cho `birthday` / `telephone` (store & update)
- [x] Migration `2026_09_10_000000_update_teachers_table_v3.php` — `teachers.birthday`, `teachers.telephone` nullable
- [x] `TeacherResource` — không `Carbon::parse(null)` (trước đây ra ngày hôm nay), trả `null`
- [x] `resources/views/exports/teacher_report.blade.php` — cột Ngày sinh để trống khi null
- [ ] Chạy `php artisan migrate` (chờ user duyệt — không tự chạy)

### FE (hrm-client)
- [x] `pages/training/teachers/components/TeacherForm.vue` — `<Required v-if="form.type == 1" />` cho Ngày sinh và Số điện thoại (theo đúng pattern sẵn có của Số CCCD / Email / Trình độ)

### Checkpoint — 2026-09-10
Vừa hoàn thành: toàn bộ code BE + FE của #11409.
Đang làm dở: không.
Bước tiếp theo: chạy migration trên DB dev rồi test tạo giảng viên thuê ngoài bỏ trống Ngày sinh + SĐT.
Blocked: migration chưa chạy (theo quy tắc không tự đụng DB).
