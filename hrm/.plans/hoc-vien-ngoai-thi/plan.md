# Plan — Học viên ngoài thi khóa exam-mode

> Plan chi tiết (code đầy đủ): `docs/superpowers/plans/2026-07-23-hoc-vien-ngoai-thi.md`
> Spec: `docs/superpowers/specs/2026-07-23-hoc-vien-ngoai-thi-design.md`

## Trạng thái
Plan DONE (2026-07-23). Chờ user chọn cách thực thi (subagent-driven / inline) + cho phép migrate.

## Tasks (tổng quát theo Phase)

### Phase 1 — BE Elearning (gating + endpoint)
- [x] Task 1 — Migration `learner_id` cho `exam_test_results` (file tạo xong, CHƯA migrate — chờ user OK)
- [x] Task 2 — `ExamTestResult::learner()` relation
- [x] Task 3 — Helper `ExamTakerResolver::fromRequest()`
- [ ] Task 4 — Nới chặn ghi danh (`enroll:261`) cho learner khi public
- [ ] Task 5 — `examStatus` learner-aware
- [ ] Task 6 — `SubjectExamController` (todo + submit) + 2 route

### Phase 2 — BE Training (learner-aware)
- [ ] Task 7 — `ExamResultService::store` gán `learner_id` + guard `$employee`
- [ ] Task 8 — `syncSubjectExamCompletion($ownerId,$subjectId,$ownerCol)` + 2 caller

### Phase 3 — FE elearning (màn thi native)
- [x] Task 9 — Route `/khoa-hoc/:slug/thi` + phân nhánh `handleTakeExam` (dùng `@/services/api`, getter `isLearner`)
- [x] Task 10 — Store `subjectExam` + `SubjectExamView.vue` (render type 1/2/3/5/6/7 + đồng hồ + cảnh báo rời trang)
- [x] Task 11 — `SubjectExamResultView.vue` (đạt/trượt/chờ chấm/đang tính TB) + sửa text `ExamPromptModal` theo isLearner

### Phase 4 — HRM examiner chấm bài learner
- [x] Task 12 — BE: `ExamResultListResource` + `getEssayQuestionAnswer` hiện tên learner + cờ `is_external` (null-safe employee)
- [x] Task 13 — FE hrm-client: badge "Học viên ngoài" ở list `exam_results/index` + modal `grading-essay-question-modal`

### Fix sau final review (2026-07-23)
- [x] Render câu type 5 (điền từ) trong SubjectExamView (review phát hiện thiếu)
- [x] Màn kết quả: trạng thái trung tính "Đã nộp/đang tính TB" khi exam_result=null (rule average còn lượt)
- [x] Cảnh báo rời trang khi đang làm bài

## CODE DONE — chờ user
- ⚠️ CHƯA chạy migration `2026_07_23_100000_add_learner_id_to_exam_test_results` → luồng learner sẽ 500 cho tới khi migrate.
- Final review: 0 Critical, regression nhân viên PASS. Minor chấp nhận: created_by=0 cho learner (guard api null; strict=false nên điền 0), completion_time âm khi time_limit=0 (pattern có sẵn của luồng nhân viên).

## Verify (manual)
V1 ghi danh · V2 eligible · V3 trắc nghiệm · V4 tự luận + examiner · V5 hết lượt/chờ chấm · V6 regression nhân viên.
