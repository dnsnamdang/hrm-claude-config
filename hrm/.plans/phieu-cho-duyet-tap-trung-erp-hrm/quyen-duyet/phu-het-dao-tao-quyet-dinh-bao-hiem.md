# Phủ hết màn duyệt — nhóm Đào tạo / Quyết định / Bảo hiểm (đợt 2) — @cuong61n

Ngày 17/11/2026. Làm theo `BRIEF-dinh-nghia-loai-phieu.md` + `BRIEF-bo-sung-phu-het-man-duyet.md`. Đã đọc lại code gốc (nhánh `gop_db-main`); số dòng ghi theo code đã đối chiếu. Manifest dọn dữ liệu thử: `wave2-training.json`.

## 1. Kết quả đợt này

| Việc | Kết quả |
|---|---|
| Yêu cầu điểm danh học viên | **Đăng ký mới** `course_student_attendance` (nhãn "Điểm danh học viên") — BE không chốt quyền, người duyệt lấy theo điều kiện giao diện (mục 3) |
| Quyết định | **Tách 1 doc_type gộp → 19 doc_type** `decision_<loại>` (mỗi loại 1 lớp con của `Support/BaseDecisionDefinition`), nhãn = tên màn trên menu, người duyệt lọc "Loại phiếu" đúng từng loại |
| Duyệt câu hỏi / kết quả thi / hợp đồng đào tạo / phụ lục HĐLĐ | **Bỏ — có bằng chứng route chết / không có trạng thái chờ** (mục 5) |
| 10 loại đợt 1 | Đối chiếu lại gate với entity (`canDepartmentHeadApprove`, `canDirectorApprove`, `canManagerTrainingApprove`, FE index/approve): **không thấy sai / thiếu cấp** nên không tăng version (riêng Quyết định `version()` = 2 vì đổi doc_type) |

## 2. Bảng kiểm kê toàn module

| Luồng | Màn FE | doc_type | Ghi chú / bằng chứng bỏ |
|---|---|---|---|
| Đề xuất đào tạo (TP → QLĐT) | `/training/training_requests/{id}/approve` | `training_request` | đợt 1 |
| Đề xuất mở khoá học (TP → BGĐ) | `/training/course_requests/{id}/approve` | `course_request` | đợt 1 |
| Khoá học (TP → BGĐ) | `/training/courses/{id}/approve` | `course` | đợt 1 |
| Đăng ký khoá học | `/training/course-registers/{id}/approve` | `course_register` | đợt 1 |
| Kế hoạch đào tạo | `/training/training-survey-planning/{id}/approve` | `training_planning` | đợt 1 |
| Kế hoạch đánh giá năng lực (QLĐT → BGĐ) | `/training/capacity-evaluate-planning/{id}/approve` | `capacity_evaluate_planning` | đợt 1 |
| Kỳ thi đánh giá năng lực (QLĐT → BGĐ) | `/training/capacity-evaluate/{id}/approve` | `capacity_evaluate` | đợt 1 |
| **Điểm danh học viên chờ duyệt** | `/training/courses/{id}/show` → tab "Điểm danh học viên" | `course_student_attendance` | **MỚI đợt 2** |
| Quyết định × 19 loại (Xem xét → Duyệt) | `/decision/<url loại>/{id chi tiết}/approve` | `decision_department_establishment`, `_department_change`, `_department_dissolution`, `_manpower_planning`, `_regulation_general`, `_regulation_salary`, `_accept_personnel`, `_reward`, `_employee_discipline`, `_appoint_personnel`, `_transfer_personnel`, `_renew_labor_contract`, `_salary_change`, `_salary_bonus`, `_assign_training`, `_termination_labor_contract`, `_retirement`, `_suspend_labor_contract`, `_increase_seniority` | **TÁCH đợt 2** (trước: `decision`) |
| Biên bản xử lý sự cố | `/decision/category/trouble-shooting-reports/{id}/approve` | `trouble_shooting_report` | đợt 1 |
| Phiếu đăng ký bảo hiểm | `/decision/insurance/{id}/approve` | `insurance_register` | đợt 1 |
| Duyệt câu hỏi (`questions/{id}/deny`) | không có màn duyệt | — | Route `Training/Routes/api.php:176` trỏ `QuestionController::deny` **không tồn tại** (0 hàm `deny`); câu hỏi chỉ có trạng thái Hoạt động/Khoá (`pages/training/questions/index.vue:537-546`) |
| Kết quả thi (`exam_test_results/{id}/deny`) | không có | — | Route `api.php:321` trỏ `ExamResultController::deny` **không tồn tại** |
| "Chốt điểm" kết quả thi offline (`examiners/approveExamResultOffline`) | popup `components/modals/ExamOfflineResult.vue:33` | — | Người nhập điểm tự bấm "Chốt điểm" (tính đạt/không đạt, `ExaminerController.php:863`); không có trạng thái chờ người khác duyệt |
| Hợp đồng đào tạo (`decision/training-contract/{id}/toggle-approve`) | không có màn duyệt | — | `Decision/Routes/api.php:427` trỏ `TrainingContractController::toggleApprove` **không tồn tại** |
| Phụ lục hợp đồng lao động | `pages/decision/appendix-labor-contract/_id/approve.vue` | — | FE gọi `decision/appendix-labor-contract/{id}/toggle-approve` (`approve.vue:118,152`) nhưng **route không có** (`api.php:451-461`), controller không có `toggleApprove`; phụ lục không có trạng thái riêng (suy từ quyết định gốc) |
| HĐLĐ (`labor-contract`) | — | — | không có màn / route duyệt |
| Quyết định sửa đổi định biên (`manpower_plannings_changes`) | — | — | có hằng nhưng không route / bảng |
| Widget `JobWaitingApproveService` + `DashboardService::waitingApprove` | dashboard Đào tạo / Quyết định | — | chỉ đếm lại đúng các loại đã đăng ký (kế hoạch, đề xuất, khoá, đăng ký khoá; Quyết định) — không phải luồng duyệt mới. Lưu ý dashboard Quyết định tính `quyet_dinh.manage` vào người duyệt (khác nút duyệt thật) |
| Danh sách yêu cầu điểm danh (`/training/attendance/request-list`) | màn của HỌC VIÊN | — | học viên tự điểm danh (status 0→1), không có nút duyệt |
| Bảo hiểm `insurance-out-company`, `reset-status`, `reward-condition` | — | — | không có luồng chờ duyệt (`toggle-status` danh mục) |
| Module `Insurance` (`Modules/Insurance`) | — | — | không có route duyệt / Entity |

## 3. Điểm danh học viên (`course_student_attendance`) — **BE KHÔNG CHỐT QUYỀN**

- Phiếu = 1 dòng `course_student_attendances` status 1 (CHO_DUYET) của khoá ĐÃ DUYỆT (status 5) — mỗi học viên × mỗi lần điểm danh (`course_attendances`). Học viên bấm "Điểm danh" (`AttendanceController::studentAttendance`, status 0→1); người duyệt mở `/training/courses/{id}/show` › tab "Điểm danh học viên", đánh dấu ô "X (Chờ duyệt)" → Lưu → modal Duyệt / Không duyệt → `POST training/courses/student-attendance/approve-multiple` (status 2 / 3, kèm `reason_deny`).
- BE: route không middleware (`Routes/api.php:234-236`); `CourseService::studentAttendanceApprove(Multiple)` chỉ `update()` theo id, không kiểm người, status hiện tại hay khoá. `/show` không phải mục menu (middleware FE `checkPermission` không chặn) và `CourseController::show` không kiểm quyền / phạm vi.
- **Điều kiện giao diện (cổng thật duy nhất)**: tab `v-if="form.canViewAllInfo && form.status == 5"` (`CourseFormShow.vue:1966`); `canViewAllInfo` do `CourseService.php:393` = (người phụ trách khoá ∪ người tạo khoá) HOẶC giữ mã `training.thong_tin_tat_ca_khoa_hoc.view` ở công ty đang làm.
- Người duyệt = (người phụ trách + người tạo khoá) × mọi công ty + người giữ mã theo từng công ty. `truth()` gọi đúng `CourseController::show` đọc `canViewAllInfo` (đệm theo người × công ty × khoá); nếu `show()` tự lỗi thì quay về đúng biểu thức của `getDataForShow`.
- Hook đồng bộ: model `CourseStudentAttendance` tự có `booted()` (không dùng trait vì mỗi "gửi yêu cầu điểm danh" tạo hàng trăm dòng status 0); `CourseService::studentAttendanceApprove` / `studentAttendanceApproveMultiple` (query `update()`) gọi `scheduleSync` tường minh; `Course::booted()` đồng bộ lại dòng chờ khi khoá đổi status / bị xoá; `Course::syncPersonsCharge()` đồng bộ lại khi đổi người phụ trách.
- Không mở sẵn tab: FE không có tham số chọn tab ⇒ `handler_path` = `/training/courses/{id}/show` (mở tab đầu, người duyệt chuyển sang tab "Điểm danh học viên").

## 4. Quyết định — tách theo loại

- 1 lớp trừu tượng `Definitions/Decision/Support/BaseDecisionDefinition` (logic chung; Registry không quét `Support/`) + 19 lớp `*DecisionDefinition` chỉ khai `decisionType()`. `Decision::approvalInboxDocType()` trả doc_type theo `type` của bản ghi (`BaseDecisionDefinition::DOC_TYPES`); loại chưa hỗ trợ trả khoá không có Definition nên sync bỏ qua.
- Logic giữ nguyên: Xem xét `decision.quyet_dinh.confirm` (status 2) → Duyệt `decision.quyet_dinh.approve` (status 3); không quản lý phòng, không so công ty; 4 loại tự sinh phụ lục HĐLĐ (bổ nhiệm, điều chuyển, điều chỉnh lương, tăng lương thâm niên) thiếu mẫu in thì cấp Duyệt `approvable = false`. `title` nay chỉ còn đối tượng áp dụng (nhãn loại đã ở cột "Loại phiếu").
- **QĐ bị ẩn do HĐLĐ không thời hạn**: màn chờ duyệt chung `/decision/waiting-approve` (`WaitingApproveService.php:236-241`) ẩn QĐ bổ nhiệm / điều chuyển khi `decision_labor_contracts.end_date` null hoặc đã qua. Bảng gom **không sao chép** — phiếu vẫn vào hàng đợi và duyệt được ở màn từng loại (route `toggle-approve` và màn approve không kiểm hạn hợp đồng). Cần người phụ trách module Quyết định xác nhận có muốn giữ hành vi ẩn đó không.
- Dữ liệu cũ: các dòng `approval_inbox_*` mang doc_type `decision` (cũ) đã xoá khỏi DB local; **nếu một môi trường nào đã có dòng `decision` cũ thì phải xoá trước khi bật bản này** (Registry không còn doc_type đó nên không ai đóng chúng).

## 5. Kết quả kiểm

Số liệu = `approval-inbox:verify` trên phiếu thử + dữ liệu thật; "cặp được duyệt thật" lấy từ test hồi quy (`assertDefinitionMatchesTruth`).

| doc_type | Gate tóm tắt | Pending thật ở DB local | verify (cặp so / chênh lệch) | Đột biến (bị bắt / thử) |
|---|---|---|---|---|
| `course_student_attendance` | người phụ trách ∪ người tạo khoá × mọi công ty + giữ mã `training.thong_tin_tat_ca_khoa_hoc.view` | 3.338 | 60.000 / 0 (300 phiếu đầu; test: 2.760 cặp, 464 được duyệt) | 5/5 |
| `decision_*` (19) | confirm → approve (chỉ mã) | 1 (`decision_termination_labor_contract`) | 1.536–2.560 mỗi loại / 0 | 9/9 (Base) |
| `training_request`, `course_request`, `course`, `course_register`, `training_planning`, `capacity_evaluate_planning`, `capacity_evaluate`, `trouble_shooting_report`, `insurance_register` | như đợt 1 | 12 / 4 / 5 / 52 / 4 / 4 / 4 / 4 / 4 | 2.490–15.544 / 0 | (đợt 1) |

Đột biến Điểm danh: bỏ người tạo khoá · bỏ người giữ mã · người phụ trách chỉ 1 công ty · bỏ điều kiện khoá đã duyệt · đổi mã quyền ⇒ cả 5 làm test đỏ. Đột biến Quyết định: cấp Duyệt dùng mã Xem xét · cấp Xem xét dùng mã Duyệt · bỏ chặn thiếu mẫu in PLHĐ · pendingQuery không lọc loại · describe không kiểm loại · 2 loại trùng doc_type · thiếu 1 loại trong 4 loại PLHĐ · trạng thái hiệu lực không tính đã duyệt ⇒ cả 9 (kể cả pendingQuery) bị bắt.
Test: `tests/Feature/ApprovalCenter/Training` 58 (Điểm danh 8), `Decision` 24, `Insurance` 6 — xanh. `ApprovalChangeWatcherTest` (chung) xanh nhưng chạy ~2'50" vì mỗi lần quét đầy đủ phải sync cả 3.338 dòng điểm danh.
API thật `:8000` (JWT nhân viên 13 · công ty 1): `/inbox/counts` tách đủ 19 nhãn Quyết định + "Điểm danh học viên"; `/inbox?doc_type=decision_appoint_personnel` và `course_student_attendance` trả `handler_path` đúng. Không mở trình duyệt.

## 6. Việc cần người điều phối / người phụ trách module

1. **3.338 dòng điểm danh chờ duyệt thật từ 2024** (92 khoá, mỗi dòng ~70 người duyệt ⇒ ~233.000 dòng `approval_inbox_assignees`) sẽ ngập "Chờ tôi duyệt" của người phụ trách khoá. Code gốc không có hạn duyệt. Cần user quyết: giữ nguyên, hay thêm hạn (vd khoá đã kết thúc quá N ngày thì ẩn) — chỉ làm được trong Definition (`approvable_until`) sau khi có con số.
2. `course_student_attendances` không có index `status` / `course_id` (toàn bảng 42.000 dòng; `pendingQuery`, `Course::scheduleAttendanceInboxSync` quét tuần tự) — đề xuất thêm index `(status, course_id)` (không tự migrate).
3. `ApprovalCenterCleanTestCommand` vẫn không xoá dòng `approval_inbox_*` đã đóng của phiếu thử (đã dọn tay ở DB local).
4. `ensureBootstrapped` chạy `needsBootstrap` cho TỪNG Definition mỗi lần mở màn: Quyết định tách 19 loại ⇒ +18 truy vấn `exists()` (đều có index `status`/`type`), cần theo dõi khi tổng loại > 100.

## 7. Lỗi / lỗ hổng của code gốc (chỉ ghi lại, không sửa)

Mới đợt này:
- Điểm danh: route duyệt (`approve`, `approve-multiple`) **không kiểm quyền / người / status / khoá** — ai đăng nhập cũng gọi được, duyệt lại dòng đã duyệt, đổi dòng của khoá khác.
- `CourseController::show` không kiểm quyền / phạm vi; trả `canViewAllInfo` chỉ để FE ẩn tab.
- `CourseService::getDataForShow` ném `ErrorException` ("Attempt to read property title on null", `CourseService.php:375-377`) khi khoá còn dòng đề thi đã bị xoá ⇒ `show()` nuốt lỗi, trả null ⇒ **trang chi tiết khoá trắng** (DB local: khoá 4 và nhiều khoá khác) — người duyệt không mở được tab điểm danh.
- Route chết: `questions/{id}/deny`, `exam_test_results/{id}/deny`, `training-contract/{id}/toggle-approve`, `appendix-labor-contract/{id}/toggle-approve` (FE vẫn gọi ⇒ 404).
- `WaitingApproveService` ẩn QĐ bổ nhiệm / điều chuyển có HĐLĐ không thời hạn.
Đợt trước (còn nguyên): xem `dinh-nghia-dao-tao-quyet-dinh-bao-hiem.md` mục 7.

## 8. File đã tạo / sửa

- Definition: `Modules/ApprovalCenter/Definitions/Training/CourseStudentAttendanceDefinition.php`; `Definitions/Decision/Support/BaseDecisionDefinition.php` + 19 `Definitions/Decision/*DecisionDefinition.php` (xoá `Decision/DecisionDefinition.php`).
- Model / service nguồn: `Modules/Decision/Entities/Decision.php` (`approvalInboxDocType()` theo `type`); `Modules/Training/Entities/CourseStudentAttendance.php` (hook `booted()`); `Modules/Training/Entities/Course.php` (`booted()`, `scheduleAttendanceInboxSync()`, gọi trong `syncPersonsCharge()`); `Modules/Training/Services/Course/CourseService.php` (2 chỗ `->update()` điểm danh gọi `scheduleSync`).
- Test: `tests/Feature/ApprovalCenter/Training/CourseStudentAttendanceDefinitionTest.php` (mới), `tests/Feature/ApprovalCenter/Decision/DecisionDefinitionTest.php` (viết lại cho 19 doc_type, thêm 5 ca).
- Không chạy migration nào. Dữ liệu thử đã dọn (`approval-center:clean-test --manifest=wave2-training.json` + dòng `approval_inbox_*` mồ côi + 4 quyết định thử `TEST-APPROVAL-CENTER` còn sót từ đợt 1).
