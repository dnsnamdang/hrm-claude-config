# Plan — Ghi note học viên ngoài theo buổi

## Phase 1: Note per buổi cho học viên ngoài

### BE
- [x] Migration thêm cột `note` (text nullable) vào `course_student_attendances` (không transaction) — đã chạy
- [x] Model `CourseStudentAttendance`: thêm `note` vào `$fillable`
- [x] `CourseService::getClientAttandance`: select thêm `note`
- [x] `CourseClientAttendanceTransformer`: expose `note`
- [x] Route `POST training/courses/student-attendance/{id}/note` (group /courses, auth:api)
- [x] `CourseController::studentAttendanceNote($request,$id)` + `CourseService::studentAttendanceNote($note,$id)`

### FE (`CourseFormShow.vue`)
- [x] Computed `clientAttendanceGroupBy`: gán `note` vào từng ô attendance từ bản ghi thật
- [x] Bảng học viên ngoài: thêm icon 📝 trong mỗi ô có `attendance.id`; đổi màu nếu có note
- [x] Modal note: textarea, prefill note cũ, hiện tên HV
- [x] Handler lưu: POST endpoint mới → reload `getListStudentAttandance` + toast

### Kiểm thử (đã verify qua Playwright)
- [x] Ô đã điểm danh có icon; ô `-` không có
- [x] Ghi note → lưu (DB), reload icon đổi xanh (text-primary), mở lại prefill đúng note
- [x] Dọn dữ liệu test (reset note về null)

### Checkpoint — 2026-07-09
Vừa hoàn thành: Ghi note học viên ngoài theo từng buổi (BE migration+model+service+transformer+route+controller, FE icon+modal+handler), verify end-to-end.
Bước tiếp theo: (không) — feature hoàn tất, chờ user review.
Blocked:
