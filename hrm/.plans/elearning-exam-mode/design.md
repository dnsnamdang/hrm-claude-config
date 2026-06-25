# elearning-exam-mode — Design (tóm tắt)

> Owner: @junfoke · Tạo: 2026-06-15 · Trạng thái: DESIGN (còn quyết định mở ở Phase 0)

## Mục tiêu

Xử lý khóa học có `evaluation_mode = 'exam'` ("Theo bài thi") ở elearning: học viên vẫn học bài
trong elearning, nhưng việc **làm bài thi đi theo luồng đào tạo cũ (HRM)**; kết quả thi quyết
định hoàn thành khóa + cấp chứng chỉ.

## Quyết định nghiệp vụ đã chốt với user

- Khóa exam-mode **vẫn hiển thị & học được** trong elearning (không ẩn).
- Hành động chính ở màn học/chi tiết: thay "Tiếp tục học" bằng **"Làm đề thi"** → trỏ về HRM.
- `exam_participation_required` là **công tắc gate** cho nút "Làm đề thi":
  - `= 1` (bắt buộc học trước): nút khóa cho tới khi `% bài hoàn thành ≥ exam_min_required_percent`
    (vd 80%); chưa đủ hiện hint điều kiện.
  - `= 0` (không yêu cầu): nút mở **ngay từ đầu**, không cần học trước; bài học là tùy chọn.
- Sau khi thi: **điểm quyết định hoàn thành khóa + chứng chỉ**. elearning KHÔNG tự tính —
  đọc lại `SubjectEnrollment.status` (BE cập nhật từ kết quả thi).

## Hiện trạng BE (kết quả rà soát 2026-06-15)

- Training **đã có** luồng thi cho employee: `POST /api/training/v1/exam_test_results`
  (`ExamResultController@store` → `ExamResultService`); kết quả ở `ExamTestResult`
  (`total_point_exam`, `result` 1=Đạt/2=chờ chấm/3=Không đạt, `percent_achieved`).
  Giới hạn lượt thi: `ExamKitService::canReplyDoExam` (đếm theo `employee_id + exam_id + course_id`).
- `SubjectEnrollment`: status 1/2/3, progress, completed_at, due_date; hỗ trợ `learner_id`.
  **KHÔNG có cột điểm thi.**
- ❌ **Không có** logic tự set enrollment `done` theo kết quả thi (kể cả employee).
- ❌ Elearning **chưa có** route/controller exam cho learner.
- ⚠️ `LearningSessionService::recalculateCourseProgress()` set `done` **thuần theo % bài học**,
  không xét `evaluation_mode` → khóa exam-mode sẽ bị tự báo done sai khi học hết bài.
- Chứng chỉ: cấp on-the-fly khi enrollment `done` + `certificate_enabled` (`CertificateService`).

## Quyết định KIẾN TRÚC (đã chốt 2026-06-15)

1. **Đối tượng thi: CHỈ employee.** External learner không làm bài thi (Training exam dựa
   `employee_id`). Nút "Làm đề thi" chỉ hiện cho user_type=employee; learner không thấy luồng thi.
2. **Cập nhật hoàn thành theo điểm:** khi điểm thi đạt → **gọi hàm cập nhật ngược** set
   `SubjectEnrollment.done` + `completed_at`, và **thêm cột ghi điểm thi** vào `subject_enrollments`
   (vd `exam_score` / `exam_result`). So điểm với `pass_score_percent`, áp `exam_score_rule`
   (highest/last/average) — **cần build service tính điểm theo rule (hiện chưa có).**
3. **Mối nối Subject ↔ luồng thi cũ (đã rõ qua điều tra):**
   - `courses.subject_id` (nullable) — Subject `hasMany` courses. Thi subject → `ExamResultService`
     set `ExamTestResult.course_id = course_id` cho nhánh `type_do='subject'`
     ([ExamResultService.php:287](../../hrm-api/Modules/Training/Services/ExamResult/ExamResultService.php#L287)).
   - `subject_exams.exam_id` và `ExamTestResult.exam_id` cùng trỏ `exam_kits` → truy kết quả theo subject_exams.
   - ⚠️ Cần `course_id` của subject để dựng deep-link → **xác minh exam-mode subject luôn có course
     (courses.subject_id)** và lấy đúng course_id (sub-task Phase 2).
4. **Deep-link làm bài thi (HRM admin, employee):**
   `/training/courses/{courseId}/exam_kits/{examId}/todo` (component `ExamToDoForm`,
   API `training/courses/{courseId}/exams/{examId}/getForTodo`). Cần `course_id` + `exam_id`
   (exam chọn ngẫu nhiên 1 trong `subject_exams` nếu nhiều đề).
5. **Chặn elearning tự complete exam-mode bằng bài học:** sửa `recalculateCourseProgress` để khóa
   exam-mode KHÔNG tự `done` theo % bài (chỉ cập nhật progress để dùng cho gate thi).

## Phạm vi dự kiến (sau khi chốt Phase 0)

- **FE elearning**: nhận diện exam-mode ở màn chi tiết + màn học; nút "Làm đề thi" (gate theo
  participation rule) deep-link HRM; banner giải thích; đọc trạng thái/điểm để hiện hoàn thành.
- **BE elearning**: endpoint trả "trạng thái thi" của khóa cho user (đủ điều kiện thi chưa, số
  lượt còn lại, kết quả gần nhất, deep-link); chặn auto-complete exam-mode theo bài.
- **BE Training**: (nếu trong scope) set enrollment done khi đạt thi.

## Liên quan

- [[course-rebuild-subject]] — nơi định nghĩa cấu hình exam của Subject.
- [[elearning-completion-criteria]] — enforcement tiêu chí hoàn thành (completion mode).
- [[elearning-course-completion]] — luồng chứng chỉ khi enrollment done.
