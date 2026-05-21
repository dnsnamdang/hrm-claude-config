# Subject Enrollment — Design

## Mục tiêu

Cho phép user enroll (tham gia) khoá học riêng lẻ từ trang chi tiết khoá học trên elearning.
Sau khi enroll, navigate tới trang placeholder (chờ màn học thật).
Khi vào lại trang detail, hiển thị trạng thái "Đã tham gia" + nút "Bắt đầu học".

## Scope

- BE: Tạo bảng `subject_enrollments`, model, service, controller, route
- FE: Sửa store + composable gọi API thật, tạo trang placeholder, cập nhật UI button
- KHÔNG xử lý: learning flow, progress tracking, certificate, enroll từ lộ trình

## Quyết định

1. **Tạo bảng mới** `subject_enrollments` thay vì tái sử dụng `employee_register_courses`
2. **Giữ status enrolled** trong DB cho đến khi user thực sự bắt đầu học bài đầu tiên (chưa implement)
3. **Trang placeholder** chỉ hiện thông báo "Sắp ra mắt", không hiện danh sách bài học
4. Pattern theo `LearningPathEnrollment` để nhất quán

## Spec chi tiết

→ `docs/superpowers/specs/2026-05-21-subject-enrollment-design.md`

## Owner

@junfoke
