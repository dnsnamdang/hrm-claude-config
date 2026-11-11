# Prod: khoá học KH-00283 thấy trên app nhưng không đăng ký được — @cuong61n

> Hỗ trợ người dùng trên PROD (hrm.eteksofts.com, nhánh gop_db), không có số Redmine. Người phụ trách: @cuong61n.

## Phase 1 — Điều tra (11/11/2026)

- [x] 11/11/2026 · Tra logic đăng ký: KHÔNG bắt buộc có trong "Danh sách học viên" mới đăng ký được. App chỉ hiện nút "Đăng ký khóa học" khi khoá có **Thông báo khóa học** còn hạn đăng ký (`course_notifications.registration_deadline > hôm nay`) — `CourseListResource` trả `can_register`/`register_link` theo thông báo. Màn "Danh sách khóa học" của app (`getForMyCourse`, status=5) hiện MỌI khoá đã duyệt cho mọi người, nên thấy khoá mà không có nút.
- [x] 11/11/2026 · Kiểm dữ liệu prod (chỉ đọc): KH-00283 tạo 15:26 duyệt 15:32 ngày 11/11, học 12/11 09:00–10:00, `close_register=0`, có `course_register_configs` (id 999), có 3 học viên `course_students` (NV 126, 237, 346), **0 bản ghi `course_notifications`**, 0 đăng ký `course_registers` → nguyên nhân: chưa phát Thông báo khóa học nên app không có nút đăng ký.
- [x] 11/11/2026 · Log prod 15:26:40 có lỗi phụ `getLastNotification`: `Attempt to read property "registration_deadline" on null` (CourseController:946) — mở phần thông báo của khoá chưa có thông báo nào thì 500. Chưa sửa.
- [ ] Hướng xử lý (chờ user chốt): (a) người phụ trách khoá tạo Thông báo khóa học cho KH-00283, hạn đăng ký trước giờ học; hoặc (b) thêm thẳng NV vào tab Danh sách học viên. Tuỳ chọn sửa lỗi null ở `getLastNotification`.
