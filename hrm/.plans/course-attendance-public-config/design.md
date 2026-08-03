# Cấu hình màn điểm danh học viên bên ngoài (public) — @namdangit

## Mục tiêu
Tinh chỉnh màn điểm danh công khai qua QR (`/client/course-attendance`) dành cho học viên bên ngoài:
1. **Logo động**: thay logo hardcode `logo-etek.jpg` bằng logo cấu hình ở `/timesheet/setting/setting-master`.
2. **Bỏ bắt buộc email**: trường email không còn required (cả FE và BE), nhưng vẫn kiểm định dạng nếu có nhập.

## Scope
- FE: `hrm-client/pages/client/course-attendance/index.vue`
- BE: `hrm-api/Modules/Training/Http/Requests/Client/CourseAttendance/StoreStudentAttendanceRequest.php`
- KHÔNG cần migration (cột `email` đã `nullable`).

## Quyết định chính
- Logo lấy qua API public `GET /v1/master-settings` (không cần auth) → phần tử `category == 'logo'` → field `content`.
- Fallback logo: **để trống** (không hiển thị logo nếu setting chưa cấu hình) — theo yêu cầu user.
- Email rỗng: FE gửi lên, BE `prepareForValidation` convert `''` → `null` để không vướng rule `email` format và không vi phạm `unique` (MySQL cho phép nhiều NULL).
- Các trường name / phone / company giữ nguyên bắt buộc.

## Link spec chi tiết
`docs/superpowers/specs/2026-07-09-course-attendance-public-config-design.md`
