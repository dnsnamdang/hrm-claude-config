# elearning-exam-mode — Plan

> Owner: @junfoke · Tạo: 2026-06-15

## Phase 0 — Chốt quyết định kiến trúc ✅ (2026-06-15)

- [x] P0.1 Deep-link HRM: `/training/courses/{courseId}/exam_kits/{examId}/todo` (ExamToDoForm).
- [x] P0.2 Mối nối: `courses.subject_id` + `ExamTestResult.course_id` (type_do='subject'); exam_id cùng `exam_kits`.
- [x] P0.3 Chốt: thêm cột điểm thi vào `subject_enrollments` + hàm set done khi đạt (trong scope).
- [x] P0.4 Chốt: exam-mode **chỉ employee** (learner không thi).
- [x] P0.5 Viết spec chi tiết `docs/superpowers/specs/2026-06-15-elearning-exam-mode-design.md` (2026-06-15).

## Phase 1 — Chặn auto-complete sai (BE elearning) ✅ (2026-06-15)

- [x] P1.1 Sửa `LearningSessionService::recalculateCourseProgress()`: thêm `$isExamMode`, khóa
      exam-mode KHÔNG tự set `done` theo % bài (vẫn cập nhật progress + chuyển ENROLLED→LEARNING). php -l PASS.
- [x] P1.2 Completion mode giữ nguyên (isExamMode=false → hành vi cũ); lộ trình chỉ sync khi
      becameDone nên exam-mode sẽ sync ở Phase 4 (sau khi đạt thi). Không phá vỡ luồng cũ.

## Phase 2 — Endpoint trạng thái thi cho elearning (BE, chỉ employee)

> Kiến trúc CHỐT: Hướng A cải tiến = engine thi nhận biết subject, tách khỏi course.
> RÀNG BUỘC: ADDITIVE — giữ nguyên luồng thi course cũ. Xem spec mục 4 + memory feedback-training-exam-backward-compat.

## Phase 2 — Engine thi subject-aware (BE Training, ADDITIVE) ✅ (2026-06-15)

- [x] P2.1 Migration: `exam_test_results.subject_id` (nullable, root migrations) +
      `subject_enrollments.exam_score`(decimal)/`exam_result`(tinyint) (module migration). KHÔNG tự chạy.
- [x] P2.2 `ExamKitController::getForSubjectTodo` + `ExamKitService::getDataForSubjectToDo`
      (time_limit từ subject_exams) + route `GET training/subjects/{subjectId}/exams/{id}/getForTodo`.
- [x] P2.3 `ExamResultController::store` thêm nhánh `type_do='elearning_subject'`; `ExamResultService::store`
      ghi subject_id, KHÔNG set course_register, set `percent_achieved` cho luồng subject. Giữ nhánh cũ.
- [x] P2.4 `ExamKitService::canReplyDoExamSubject` đếm theo subject_id + `subjects.exam_attempt_limit`.
      php -l toàn bộ PASS.

## Phase 3 — BE: chấm điểm → set hoàn thành khóa ✅ (2026-06-15)

- [x] P3.1+P3.2 `LearningSessionService::syncSubjectExamCompletion($employeeId,$subjectId)`: tính điểm
      cuối theo `exam_score_rule` (highest/last/average) trên `percent_achieved`; ngưỡng từ
      `subject_exams.pass_score_percent` của đề được chọn; đạt → set `SubjectEnrollment`
      (exam_score/exam_result/done/completed_at) + `syncLearningPathCompletion`; còn result=2 → đánh dấu chờ.
      Hook: cuối `ExamResultService::store` (nhánh elearning_subject) + cuối `updateResultEssayQuestion`
      (khi `subject_id`, set thêm percent_achieved sau chấm). Gọi qua app() (Training→Elearning). php -l PASS.
      Giả định: rule 'average' lấy ngưỡng theo đề lượt cuối.

## Phase 4 — Endpoint trạng thái thi cho elearning (BE, chỉ employee) ✅ (2026-06-15)

- [x] P4.1 `SubjectDetailController::examStatus($slug)` + route `GET subjects/{slug}/exam-status`
      (group elearning.auth). Trả applicable/participation_required/required_percent/current_percent/
      eligible/attempts_used/attempt_limit/last_result/exam_link/exam_result/enrollment_status.
      Non-employee hoặc không phải exam-mode → applicable=false.
- [x] P4.2 eligible theo participation rule (=1 cần current≥required; =0 true); attempts_used đếm
      ExamTestResult theo (employee_id+subject_id); exam_link chọn ngẫu nhiên 1 đề trong subject_exams
      → /training/subjects/{id}/exams/{examId}/todo. php -l PASS.

## Phase 5 — FE: màn làm bài subject (hrm-client) + elearning ✅ (2026-06-15)

- [x] P5.1 hrm-client: page `pages/training/subjects/_id/exams/_idExam/todo.vue` tái dùng `ExamToDoForm`;
      thêm prop `idSubject` + nhánh load `training/subjects/{id}/exams/{id}/getForTodo` + submit
      `type_do='elearning_subject'` (set form.subject_id). Giữ nguyên nhánh course/capacity.
- [x] P5.2 elearning [DetailEnrollCard]: khối exam-mode (banner + nút "Làm đề thi" gate theo eligible +
      hết lượt → disable + hint %) + [ContentDetailView] truyền exam-status + handleTakeExam mở
      `${VITE_HRM_CLIENT_URL}${exam_link}`.
- [~] P5.3 [SubjectLearnView] CTA "Làm đề thi" — DEFER (màn học dùng learningSession store, cần fetch
      exam-status riêng; màn chi tiết đã là entry chính theo yêu cầu). Làm sau nếu cần.
- [x] P5.4 Hiện kết quả gần nhất (pass/fail/grading + điểm) + lượt thi; hết lượt → khóa nút.
- [x] P5.5 store `subjectDetail` + state `examStatus` + action `fetchExamStatus`; gọi khi đã đăng nhập;
      BE trả applicable=false cho learner/non-exam → tự ẩn.

## Phase 7 — Chấm tự luận cho bài thi subject (BE Training, ADDITIVE) ✅ (2026-06-15)

- [x] P7.1 `ExaminerService::getListOfExams`: thêm nhánh subject (UNION) — JOIN subject_exams +
      subject_exam_graders (grader = employee hiện tại), gộp với nhánh course. Bộ lọc chung qua closure.
      Bỏ qua nhánh subject khi lọc course_id. Người chấm subject không cần là `examiner`. Trả collection.
- [x] P7.2 Thêm relation `ExamTestResult::subject()`.
- [x] P7.3 Siết quyền `updateResultEssayQuestion`: bài subject_id → kiểm tra người chấm thuộc
      subject_exam_graders của đề. php -l PASS.
- [~] P7.4 Widget dashboard chờ chấm (ExamWaitingGradingService) + thông báo người chấm — DEFER
      (course cũng chưa có thông báo). Làm sau nếu cần.

> Hoàn thành sau chấm đã có sẵn: hook cuối updateResultEssayQuestion (Phase 3) → syncSubjectExamCompletion.

## Phase 8 — Thông báo về elearning khi chấm xong bài thi subject (2026-06-16)

- [x] P8.1 BE `ExamResultService::updateResultEssayQuestion`: sau khi chấm xong (result 1/3, hết chờ chấm)
      bài subject → gửi DB notification (type `ExamGraded`, url `/khoa-hoc/{slug}`) tới EmployeeInfo người
      thi + Redis publish `user_notification_{employee_id}` (mirror OnboardingAutoEnroll). Helper
      `notifySubjectExamGraded()`. php -l PASS.
- [x] P8.2 BE `NotificationController::ELEARNING_TYPES` thêm `'ExamGraded'` (whitelist hiển thị).
- [x] P8.3 FE `stores/notification.js` `ELEARNING_NOTI_TYPES` thêm `'ExamGraded'` (lọc realtime + toast).
      Click chuông → markRead + router.push(url) → màn chi tiết khóa học xem điểm (đã có sẵn).

## Phase 9 — Chặn học viên ngoài với khóa exam-mode (2026-06-16)

Quyết định: khóa exam-mode hoàn thành phải ĐẠT bài thi (chỉ employee thi được) → học viên ngoài/khách
học 100% sẽ kẹt không hoàn thành. Hướng: CHẶN TỪ GỐC.

- [x] P9.1 BE `SubjectDetailController::enroll`: subject exam-mode + user_type≠employee → trả 403
      "Khoá học này yêu cầu thi trên hệ thống nội bộ, chỉ dành cho nhân viên." php -l PASS.
- [x] P9.2 FE store `subjectDetail`: map `entity.isExamMode = data.evaluation_mode === 'exam'`.
- [x] P9.3 FE `DetailEnrollCard`: computed `examLockedForExternal = isExamMode && !auth.isEmployee` →
      ẩn toàn bộ nút hành động, hiện khối amber "Không áp dụng cho học viên ngoài" (cả người lỡ vào).
- [ ] P9.4 (DEFER tùy chọn) ẩn khóa exam-mode khỏi listing public cho non-employee — chưa làm, card đã
      hiện "không áp dụng" là đủ theo quyết định.

## Phase 10 — Quy tắc lấy điểm TRUNG BÌNH + ngưỡng đạt cấp khóa (2026-06-16)

Quyết định: (1) average chỉ CHỐT khi hết lượt (trước đó hiện "TB tạm tính, còn k lượt"); (2) ngưỡng đạt
dùng 1 ngưỡng CHUNG cấp khóa (vì trộn điểm nhiều đề). attempt_limit đã required min:1 sẵn → lượt luôn hữu hạn.

- [x] P10.1 Migration `subjects.exam_pass_percent` (unsignedTinyInteger nullable) — CHƯA chạy.
- [x] P10.2 BE validate `SubjectBuilderRequest`: rule=average → exam_pass_percent required 1-100 (khác:
      nullable) + message. SubjectService save + SubjectDetailResource expose.
- [x] P10.3 BE `syncSubjectExamCompletion`: tách nhánh average — TB % tất cả lượt; nếu attempts_used <
      attempt_limit → lưu exam_score tạm tính, exam_result=null, KHÔNG done; hết lượt → so ngưỡng cấp khóa
      (exam_pass_percent) → chốt 1/3 + done. highest/last giữ nguyên (ngưỡng per-đề lượt được chọn). php -l PASS.
- [x] P10.4 BE examStatus trả `pass_percent` (ngưỡng cấp khóa).
- [x] P10.5 FE builder TabEvaluation: ô "Ngưỡng đạt khóa (%)" hiện khi rule=average + reset khi đổi mode;
      SubjectBuilderForm default/load/TAB_EVAL_KEYS thêm exam_pass_percent.
- [x] P10.6 FE elearning DetailEnrollCard: computed averagePending/remainingAttempts → hiện "Điểm TB tạm
      tính: X% • Còn k lượt (cần ≥ pass_percent%) — phải thi đủ N lượt mới chốt" khi average chưa chốt.

## Phase 6 — Verify

- [ ] P6.1 **Regression luồng course CŨ**: thi course cũ (getForTodo/ExamResultService nhánh cũ/
      canReplyDoExam) vẫn chạy nguyên — KHÔNG vỡ. + queue chấm course (getListOfExams nhánh course) vẫn đúng.
- [ ] P6.2 participation=1: chưa đủ % (khóa) / đủ % (thi được). participation=0: thi ngay.
- [ ] P6.3 Đạt → done + chứng chỉ; không đạt còn lượt → thi lại; hết lượt → khóa; chờ chấm tự luận → trung gian.
- [ ] P6.4 exam-mode KHÔNG tự done khi học hết bài (Phase 1). Lộ trình đồng bộ khi khóa đạt.

---

### Checkpoint — 2026-06-15 (4)
Vừa hoàn thành: Phase 5 (FE). hrm-client: page todo.vue subject + ExamToDoForm prop idSubject/nhánh
elearning_subject. elearning: DetailEnrollCard khối exam (banner+nút Làm đề thi+gate+kết quả) +
ContentDetailView (exam-status + handleTakeExam deep-link HRM) + store fetchExamStatus.
P5.3 (CTA màn học) DEFER. CODE TOÀN BỘ feature DONE.
Đang làm dở: —
Bước tiếp theo: Phase 6 — VERIFY. (1) user `php artisan migrate` 2 migration. (2) Verify browser:
regression luồng course cũ + thi subject (participation 0/1, đạt→done+chứng chỉ, hết lượt, chờ chấm).
  LƯU Ý: chưa chạy migration; FE elearning cần build trong Docker (Node≥18); chưa verify browser.
Blocked:

### Checkpoint — 2026-06-15 (5) — Fix khi verify Phase 6
Đang verify, đã sửa 4 bug:
1. Trang kết quả 404 sau khi thi subject: getForCompleteResultView gọi canReplyDoExam(null course_id) → crash.
   Sửa additive: subject_id → canReplyDoExamSubject; course giữ nguyên. (ExamResultService.php:167)
2. Breadcrumb "Kết quả thi" trỏ về màn quản lý admin: check_complete_test bỏ link khi form.subject_id.
3. Chưa tham gia mà nút "Làm đề thi" sáng (participation=0): examStatus eligible giờ yêu cầu đã enroll
   + thêm cờ `enrolled`; DetailEnrollCard thêm thông báo "Cần tham gia khóa học trước khi thi".
4. Back về elearning: handleTakeExam kèm ?return=<url elearning> → ExamToDoForm.submitSave forward query
   → check_complete_test nút "Về khóa học" (window.location về elearning). Course flow không ảnh hưởng.
Bước tiếp theo: user tiếp tục verify (migrate + browser). Blocked:

### Checkpoint — 2026-06-15 (6) — Phase 7: chấm tự luận cho subject
Phát hiện luồng chấm tự luận chưa nhận bài subject (queue getListOfExams chỉ JOIN course_exams →
bài subject course_id=null không hiện). Đã sửa ADDITIVE:
- ExaminerService::getListOfExams thêm nhánh subject (UNION qua subject_exams + subject_exam_graders,
  grader=employee hiện tại), giữ nguyên nhánh course; bộ lọc chung qua closure.
- ExamTestResult::subject() relation.
- updateResultEssayQuestion: kiểm tra grader thuộc subject_exam_graders cho bài subject.
- php -l 3 file PASS. Hoàn thành-sau-chấm đã wire ở Phase 3.
DEFER: widget dashboard chờ chấm + notification người chấm.
Bước tiếp theo: user verify end-to-end gồm luồng tự luận (grader thấy bài subject → chấm → khóa done).
Blocked:

### Checkpoint — 2026-06-16 (1) — Polish UI khi verify (FE-only, additive)
Sửa 3 chỗ hiển thị trong lúc verify, không đụng logic BE:
1. Cột "Mã" đề thi ở TabEvaluation (SubjectBuilderForm, exam-mode) luôn ra "—" vì exam_kits KHÔNG có
   cột `code`. Thêm helper `examCode(row)` → `EXAM_<id pad 4 số>` (vd EXAM_0080), ưu tiên meta.code nếu
   sau này có. Đổi header cột "Mã"→"ID"; dùng cho cả chip đã chọn.
   File: hrm-client/pages/training/subjects/components/tabs/TabEvaluation.vue.
2. Dropdown "Chọn người chấm" (TabEvaluation) bị lặp tiêu đề với nút → đổi header "Danh sách người chấm"
   (song song "Danh sách đề thi") + hiện số đã chọn.
3. elearning màn chi tiết môn — dòng "Điều kiện đạt của khoá học" trước đây chỉ lấy pass_score_percent
   của ĐỀ ĐẦU TIÊN. Vì hệ thống chọn ngẫu nhiên 1 đề, ngưỡng đạt phụ thuộc đề được giao. Sửa thích nghi:
   gộp min–max ngưỡng tất cả đề → cùng % giữ "≥ 60%", khác % hiện khoảng "(50%–70%, tuỳ đề)". Áp cho cả
   badge label + dòng diễn giải + dòng theo chương.
   File: elearning stores/subjectDetail.js (subjectExamPassScoreRange thay subjectExamPassScore),
   constants/subjectDetail.js (getPassRuleLabel/getPassRuleDesc), components/subject-detail/SubjectRequirements.vue.
Bước tiếp theo: user verify trên browser (cần môn có nhiều đề khác ngưỡng để thấy dạng khoảng).
Blocked:

### Checkpoint — 2026-06-16 (2) — Người chấm subject lấy từ danh mục "Người chấm thi"
Phát hiện: dropdown "chọn người chấm" ở TabEvaluation đang lấy TẤT CẢ nhân viên (training/employees/all),
KHÔNG đồng bộ với danh mục Examiners mà luồng course cũ dùng (course_exam_examiners.examiner_id).
User chọn: lọc chỉ người trong danh mục. Vì subject_exam_graders lưu employee_id nên chỉ examiner
NỘI BỘ (type=1, có employee_id) mới gán được (examiner thuê ngoài type=2 không có employee_id → loại).
Đã làm (additive, không migration):
- BE: ExaminerController::getAllForGrader (type=1 + status=1 + whereNotNull employee_id + scope
  current_company, unique theo employee_id) → trả {id: employee_id, name: fullname}. Route GET
  training/examiners/getAllForGrader (đặt trước /{id}). php -l PASS.
- FE: TabEvaluation.fetchEmployees đổi sang gọi training/examiners/getAllForGrader; text rỗng dropdown
  đổi thành "Chưa có người chấm trong danh mục Người chấm thi".
LƯU Ý: grader_ids cũ (employee_id không còn trong danh mục) vẫn lưu nhưng không hiện tên (graderName→#id).
Bước tiếp theo: user verify — thêm examiner nội bộ vào danh mục → mở cấu hình thi môn → dropdown chỉ hiện
người trong danh mục; chọn → lưu → người đó vào queue chấm (getListOfExams nhánh subject).
Blocked:

### Checkpoint — 2026-06-16 (2) — Chặn thi khi chờ chấm + Lịch sử thi
1. Chờ chấm tự luận → chặn thi lượt mới (tránh phí lượt):
   - BE examStatus: thêm `pending_grading` (có result=2) → eligible=false khi pending.
   - BE canReplyDoExamSubject: chặn (return false) nếu còn result=2 — defense ở submit/load.
   - FE DetailEnrollCard: nút disable + thông báo "Đang chờ chấm — chờ kết quả mới thi tiếp" (ưu tiên trên các hint khác).
2. Lịch sử thi ở elearning:
   - BE examStatus: thêm mảng `history` (id/date/exam_name/score/status mỗi lần thi).
   - FE DetailEnrollCard: nút toggle "Lịch sử thi (N)" → list từng lần (số thứ tự, ngày, điểm, kết quả màu).
   php -l 2 file BE PASS.
Bước tiếp theo: user verify (migrate + browser): chờ chấm chặn thi; lịch sử hiện đủ các lần.
Blocked:

### Checkpoint — 2026-06-16 (3) — Fix queue chấm không thấy bài subject
User báo màn /training/examiners/list-of-exams không hiện bài thi subject. Debug qua tinker (employee 13
vừa thi vừa là grader): query nhánh subject TRẢ ĐÚNG bài 964, service trả 11 bài gồm 964 — nhưng concat
course rồi subject làm 964 (id cao nhất) bị đẩy cuối → phân trang đẩy sang trang 2. Sửa: ExaminerService
::getListOfExams sort GỘP toàn cục theo sortBy/sortDesc sau merge, trước phân trang. Verify tinker:
IDS [964,942,...] đúng id desc. php -l PASS.
Bước tiếp theo: user reload màn chấm (đúng tài khoản grader) → thấy bài chờ chấm đầu danh sách → chấm.
Blocked:

### Checkpoint — 2026-06-16 (4) — Hiển thị kết quả theo quy tắc lấy điểm
"Kết quả gần nhất" chỉ chuẩn cho rule 'last'. Sửa hiển thị theo exam_score_rule:
- BE examStatus trả thêm `score_rule` + `exam_score` (điểm chính thức theo rule, từ enrollment).
- FE DetailEnrollCard: nhãn động — highest→"Điểm cao nhất", last→"Điểm lần cuối", average→"Điểm trung
  bình"; chờ chấm→"Kết quả: Chờ chấm". Điểm hiển thị = exam_score (chính thức) thay vì last_result.
  Ưu tiên: pending > exam_result(enrollment) > last_result(fallback). php -l BE PASS.
Bước tiếp theo: user verify hiển thị đúng theo từng rule (đổi Quy tắc lấy điểm ở builder).
Blocked:

### Checkpoint — 2026-06-16 (5) — Fix tiến độ >100% + popup nhắc thi ở màn học
1. BUG tiến độ 150%: enrollment có dòng enrollment_lesson_progress RÁC (subject_lesson_id của bài đã bị
   xóa khi rebuild subject) → đếm 3 done / 2 total. Sửa recalculateCourseProgress: chỉ đếm done trong
   subject_lessons thuộc subject hiện tại (whereIn lessonIds) + cap 100%. php -l PASS. (Giá trị cũ 150 tự
   sửa khi có sự kiện học kế tiếp; chưa tự sửa DB theo nguyên tắc.)
2. P5.3 (trước DEFER) — popup nhắc làm bài thi ở MÀN HỌC: tạo ExamPromptModal; SubjectLearnView fetch
   exam-status (onMount + sau completionSignal) → khi eligible & chưa đạt & không chờ chấm → popup
   "Sẵn sàng làm bài thi" (1 lần/phiên) → nút "Làm đề thi" deep-link HRM kèm ?return.
Bước tiếp theo: user verify (mở lại bài để recompute tiến độ về 100%; học đủ % → popup nhắc thi hiện).
Blocked:

### Checkpoint — 2026-06-16 (6) — Fix popup nhắc thi không hiện khi đã học xong + cap progress
1. Tiến độ 150% vẫn hiện sau reload: thêm 2 lớp — FE getter courseProgress cap min(100); BE getSessionData
   gọi recalculateCourseProgress khi tải màn học → chữa luôn giá trị lưu (verify enroll 16 → 100%). php -l PASS.
2. Popup nhắc thi không hiện khi nhân viên đã học xong TỪ TRƯỚC: trước chỉ trigger trên completionSignal
   (bài vừa xong) → vào lại không có signal. Sửa: initCourse await fetchExamStatus + maybeShowExamPrompt
   khi vào màn học. Verify subject 52: participation=1, required=80, progress=100, pending=0 → eligible → popup.
Bước tiếp theo: user verify popup hiện khi vào học khóa đã đủ %; bấm Làm đề thi → HRM.
Blocked:

### Checkpoint — 2026-06-16 (7) — Fix popup nhắc thi gọi sai baseURL (404)
Popup vẫn không hiện dù đủ điều kiện: fetchExamStatus ở SubjectLearnView import @/services/api (baseURL
= VITE_API_URL, KHÔNG có /api/v1/elearning) nhưng gọi '/subjects/.../exam-status' → 404 → catch nuốt →
examStatus=null. Sửa: dùng full path '/api/v1/elearning/subjects/{slug}/exam-status' + parse res.data||res
(đúng như subjectDetail store). Lưu ý 2 api module: @/services/api (no prefix, dùng full path) vs
@/utils/api (có prefix). Giờ examStatus nạp đúng → popup hiện.
Bước tiếp theo: user verify popup hiện thật.
Blocked:

### Checkpoint — 2026-06-16 (8) — Thông báo về elearning khi chấm xong bài thi subject
Yêu cầu: bài chờ chấm → chấm xong gửi thông báo về elearning, nhấn trỏ về màn khóa học xem điểm.
- BE `ExamResultService::updateResultEssayQuestion`: sau syncSubjectExamCompletion, khi result chốt
  (1=đạt/3=không đạt) → helper `notifySubjectExamGraded()` ghi DB notification (BaseNotification, type
  `ExamGraded`, url `/khoa-hoc/{slug}`, title kèm Đạt/Không đạt) cho EmployeeInfo người thi + Redis
  publish `user_notification_{employee_id}` (mirror OnboardingAutoEnroll). Gửi tới NGƯỜI THI
  (examResult->employee_id) chứ không phải grader. php -l PASS.
- BE NotificationController whitelist + FE notification store whitelist thêm `ExamGraded`. Click chuông
  dùng sẵn onClickNoti → markRead + router.push('/khoa-hoc/{slug}') → màn chi tiết khóa học (xem điểm
  ở khối exam-mode DetailEnrollCard). Socket chỉ connect cho employee → đúng đối tượng; offline thì
  chuông vẫn hiện ở lần fetch sau.
Bước tiếp theo: user verify — chấm xong 1 bài tự luận subject → tk người thi thấy chuông/toast → bấm
về màn khóa học thấy điểm cập nhật.
Blocked:
