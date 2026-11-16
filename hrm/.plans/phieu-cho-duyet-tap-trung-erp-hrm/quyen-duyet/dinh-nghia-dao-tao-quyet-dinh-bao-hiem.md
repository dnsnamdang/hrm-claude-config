# Định nghĩa loại phiếu — nhóm Đào tạo / Quyết định / Bảo hiểm (@cuong61n)

Ngày 16/11/2026. Làm theo `BRIEF-dinh-nghia-loai-phieu.md`. Đã đọc lại code gốc (không chỉ tin `04-dao-tao-quyet-dinh.md`); số dòng trong báo cáo cũ có thể lệch, bảng dưới ghi theo code đã đối chiếu.

## 1. 10 loại đã đăng ký

| doc_type | Màn gốc (menu) / handler_path | Cấp (status → chữ) | Gate | Hạn |
|---|---|---|---|---|
| `training_request` Đề xuất đào tạo | `/training/training_requests/{id}/approve` | 2 Chờ trưởng phòng duyệt · 3 Chờ quản lý đào tạo duyệt | Cấp 1: mã `training.de_xuat_dao_tao_truong_phong.approve` **AND** phòng phiếu ∈ `manageDepartmentIdsOf(người duyệt, công ty đang làm)` (gồm cờ quản lý tất cả phòng ban). Cấp 2: chỉ mã `…quan_ly_dao_tao.approve`. Không so công ty phiếu | Không (validate `from_time` của `update()` đã bị comment) |
| `course_request` Đề xuất mở khoá học | `/training/course_requests/{id}/approve` | 2 Chờ trưởng phòng duyệt · 4 Chờ BGĐ duyệt | Cấp 1: mã TP **AND** quản lý phòng. Cấp 2: mã BGĐ **AND** công ty đang làm == `company_id` phiếu | `from_time` (so ở độ chính xác phút) → `approvable_until` |
| `course` Khoá học | `/training/courses/{id}/approve` | như trên | như trên (mã `training.khoa_hoc_*`) | như trên |
| `course_register` Đăng ký khoá học | `/training/course-registers/{id}/approve` | 5 Chưa duyệt | chỉ mã `training.dang_ky_khoa_hoc.approve` (BE không kiểm gì, FE kiểm mã + status 5) | Không |
| `training_planning` Kế hoạch đào tạo | `/training/training-survey-planning/{id}/approve` | 2 Chờ duyệt | chỉ mã `training.ke_hoach_dao_tao.approve` | Không |
| `capacity_evaluate_planning` Kế hoạch đánh giá năng lực | `/training/capacity-evaluate-planning/{id}/approve` | 2 Chờ QLĐT duyệt · 3 Chờ BGĐ duyệt | 2: `training.ke_hoach_danh_gia_quan_ly_dao_tao.approve`; 3: `…ke_hoach_danh_gia_ban_giam_doc.approve` (chỉ mã) | Không |
| `capacity_evaluate` Kỳ thi đánh giá năng lực | `/training/capacity-evaluate/{id}/approve` | như trên | `training.ky_thi_danh_gia_nang_luc_*` (chỉ mã) | Không |
| `decision` Quyết định (19 loại) | `/decision/<url loại>/{id CHI TIẾT}/approve` | 2 Chờ xem xét · 3 Chờ duyệt | 2: `decision.quyet_dinh.confirm`; 3: `decision.quyet_dinh.approve`. Không quản lý, không so công ty | 4 loại thiếu mẫu in PLHĐ: cấp 3 `approvable=false` |
| `trouble_shooting_report` Biên bản xử lý sự cố | `/decision/category/trouble-shooting-reports/{id}/approve` | 2 Chờ duyệt | chỉ mã `decision.bien_ban_xu_ly_su_co.approve` | Không |
| `insurance_register` Phiếu đăng ký bảo hiểm | `/decision/insurance/{id}/approve` | 2 Chờ duyệt | chỉ mã `decision.phieu_dang_ky_bao_hiem.approve` | Không |

Tất cả: màu trạng thái `#D97706` (chờ duyệt); chữ lấy đúng chữ FE (BE các phiếu này không có accessor `status_text`). `excludeOwn() = false` (code gốc không chặn tự duyệt, kể cả người lập tự duyệt phiếu của mình). Phiếu chỉ ở 1 cấp tại 1 thời điểm nên người kiêm 2 cấp bấm lần lượt như màn gốc.

### Không đăng ký
- **Yêu cầu điểm danh học viên** (`course_student_attendances`): không có người duyệt xác định (không mã, không người phụ trách/giảng viên ở BE hay FE) → không biểu diễn được. Cần nghiệp vụ chốt.
- Hợp đồng đào tạo (route chết, controller không có method), HĐLĐ / Phụ lục HĐLĐ (không có luồng duyệt, FE gọi route không tồn tại), Duyệt câu hỏi / Kết quả thi (route `deny` chết), thông báo nội bộ (trạng thái chờ duyệt đã comment), `manpower_plannings_changes` (có hằng, không route/bảng).

## 2. Quyết định hợp lý: 1 doc_type `decision` cho 19 loại
- Mọi loại dùng chung bảng `decisions`, chung trạng thái, **chung 2 mã** — không có quyền theo loại ⇒ người duyệt giống hệt nhau; tách 19 doc_type chỉ thêm 19 lần quét/nạp ở `ensureBootstrapped` mỗi lần mở màn mà không khác logic.
- Tên loại ("Quyết định bổ nhiệm nhân sự · <đối tượng>") nằm đầu `title`; `handler_path` trỏ đúng màn từng loại và dùng **id bản ghi chi tiết** (bảng theo loại, khoá `decision_id`), vì màn duyệt và route `toggle-approve` dùng id đó, không phải `decisions.id` (đã kiểm: mọi loại có `pages/decision/<url>/_id/approve.vue`, test kiểm file tồn tại).
- Đánh đổi: ô lọc "Loại phiếu" chỉ có 1 mục "Quyết định"; muốn lọc theo loại thì gõ tên loại vào ô tìm kiếm. Nếu orchestrator muốn tách: bọc `DecisionDefinition` bằng 19 lớp con (đã có `levels/row`), mỗi lớp chỉ khai `docType/label` + lọc `type`; không phải viết lại logic.
- 19 loại: DB local có dòng chi tiết cho 14 loại; 5 loại `renew_labor_contracts`, `retirements`, `suspend_labor_contracts`, `increase_seniorities`, `decision_salary_bonuses` có 0 dòng — logic các loại này chỉ dựa code (cùng khuôn), chưa thử với dữ liệu thật (đặc biệt `increase_seniorities` thuộc 4 loại cần mẫu in PLHĐ).

## 3. Điểm kỹ thuật cần biết
- Người duyệt tính theo **từng công ty** (cặp nhân viên × công ty giữ mã) vì code gốc kiểm mã ở công ty đang làm và không lọc phiếu theo công ty. ~55 cặp/phiếu Quyết định ở DB local; Đăng ký khoá học 68 cặp × 48 phiếu.
- Cấp TP đào tạo dịch ngược đúng `manageDepartmentIdsOf` (cờ tất cả phòng ban chỉ trả phòng có `departments.company_id` = công ty; dòng lệch công ty trong `employee_manage_departments` vẫn tính — DB local có 9 dòng như vậy, đã có ca test). Khai là mã **AND** phòng, không có nhánh quản lý độc lập (test "người quản lý phòng không giữ mã → không thấy").
- Hạn duyệt phiếu khoá học: validate `from_time after_or_equal <phút hiện tại>` ở `update()` + ô from_time bị `disabled` trên màn duyệt ⇒ quá phút của from_time là 422 ở cả TP lẫn BGĐ. `approvable_until = endOfMinute(from_time)`. Phiếu Khoá học treo từ 2025 ở DB local chính là ca này (0 người duyệt). Các ràng buộc 422 khác theo dữ liệu (vd `subject_approve_name`, chi phí duyệt) **chưa mô hình hoá**.
- Thiếu mẫu in PLHĐ: `AppendixLaborContract::isMissingDecisionPrintTemplate` (cùng hàm 4 controller gọi) ⇒ cấp Duyệt (status 3 → 5) trả 422; cấp Xem xét không bị chặn. Phiếu đó **ẩn khỏi "Chờ tôi duyệt"** theo brief — lưu ý người duyệt vẫn có thể muốn "Từ chối" để trả lại (BE message gợi ý đúng việc đó); cân nhắc hiện phiếu `approvable=false` ở tab riêng nếu cần.
- Không sao chép lỗi của màn gốc: danh sách chờ lọc phòng quản lý áp cả cho người kiêm cấp 2; màn chung ẩn QĐ bổ nhiệm/điều chuyển khi HĐLĐ kèm hết hạn.

## 4. Chỗ ghi bằng query builder đã xử lý
Chỉ **1 chỗ**: `Modules/Training/Http/Controllers/V1/CourseController.php` hàm `defer()` — `CourseRegister::query()->where(...)->update(['status' => 20, ...])` (hoãn đăng ký, mass update không bắn sự kiện). Đã thêm `ApprovalInboxService::scheduleSync('course_register', $id)` cho các id vừa đổi. Đã rà `app` + `Modules/{Training,Decision}`: mọi nơi còn lại ghi status của 10 model này đều qua Eloquent (`->update()` trên instance / `save()`), kể cả `DecisionResetStatusService`, `DecisionLaborContractService`. `WorkingPositionController` mass-update `decisions` chỉ chạm QĐ định biên đang `status = 5` nên không ảnh hưởng hàng đợi.

## 5. File đã tạo / sửa
- Definition: `Modules/ApprovalCenter/Definitions/Training/{TrainingRequest,CourseRequest,Course,CourseRegister,TrainingPlanning,CapacityEvaluatePlanning,CapacityEvaluate}Definition.php`, `Definitions/Decision/{Decision,TroubleShootingReport}Definition.php`, `Definitions/Insurance/InsuranceRegisterDefinition.php`.
- Khung dùng chung của nhóm (Registry không quét `Support/`): `Definitions/Training/Support/{PermissionApprovers,PermissionLevelsDefinition,TwoLevelCourseDefinition,SeedSupport}.php`.
- Model gắn trait `SyncsApprovalInbox` + `approvalInboxDocType()`: `Training/Entities/{TrainingRequest,CourseRequest,Course,CourseRegister,TrainingPlanning,EvaluationPlanningCapacity,EvaluationCapacity}.php`, `Decision/Entities/{Decision,TroubleShootingReport}.php`, `Decision/Entities/InsuranceRegister/InsuranceRegister.php`.
- Sửa code nghiệp vụ: `CourseController::defer()` (xem mục 4).
- Test: `tests/Feature/ApprovalCenter/{Training,Decision,Insurance}/*DefinitionTest.php` + `Training/Concerns/{ManagerGatedTests,TwoLevelCourseTests,PermissionLevelsTests}.php`. 75 test (Training 50, Decision 19, Insurance 6), tất cả xanh.

## 6. Kết quả kiểm
- `approval-inbox:verify` (seed phiếu thử + dữ liệu thật): 0 chênh lệch ở cả 10 loại; số cặp so / cặp được duyệt thật (có phiếu thử): training_request 7.308/531, course_request 4.168/43, course 4.212/33, course_register 26.208/3.808, training_planning 3.888/688, capacity_evaluate_planning 3.936/632, capacity_evaluate 3.592/392, decision 5.016/565, trouble_shooting_report 4.530/530, insurance_register 4.390/390.
- Kiểm thử đột biến: xem báo cáo cuối — tất cả đột biến cuối cùng đều bị bắt (3 đột biến ban đầu sống sót đã bổ sung ca test: mã hai cấp trùng tập người ở DB local → dựng chênh lệch vai trò trong giao dịch; `pendingQuery` chưa được kiểm; danh sách 4 loại PLHĐ test đang đọc lại hằng của Definition).
- API thật `:8000`: `/approval-center/inbox/counts` và `/inbox?doc_type=<từng loại>` trả đúng với JWT của 1 người (user 1177, công ty 9) kèm `handler_path` đúng. Không mở trình duyệt (theo brief). Chưa viết spec e2e.
- Dữ liệu thử đã dọn bằng `approval-center:clean-test`; **lệnh này chỉ xoá phiếu nguồn, các dòng `approval_inbox_items` đã đóng của phiếu thử vẫn còn** — đã xoá tay (items/logs/assignees mồ côi của 10 loại) trong DB local.

## 7. Lỗi / lỗ hổng của code gốc (chỉ ghi lại)
1. `DecisionService::toggleApprove` không kiểm status hiện tại (nhảy 2→5, duyệt lại phiếu đã duyệt chạy lại hiệu ứng phụ); 4 loại (khen thưởng, thưởng lương T13, kỷ luật, cử đi đào tạo) không có middleware ⇒ từ chối (status 4/6) không cần quyền.
2. `CourseRequestController::deny` không kiểm quyền / status / công ty; `status_request = 4` ở Đề xuất mở khoá học / Khoá học nhảy thẳng sang "Chờ BGĐ"; `status_request` ngoài 1–4 ở Đề xuất đào tạo không kiểm.
3. BE không kiểm quyền duyệt: Biên bản sự cố, Kế hoạch đào tạo, Kế hoạch/Kỳ thi ĐGNL, Đăng ký khoá học, Điểm danh; Phiếu bảo hiểm chỉ kiểm khi từ chối.
4. Duyệt Đề xuất mở khoá học / Khoá học ghi đè `department_id` + `company_id` của phiếu bằng của người duyệt.
5. Thông báo cấp TP của Đề xuất đào tạo gửi cho mọi người có mã (tham số thứ 2 bị bỏ qua) — khác người duyệt thật.
6. `TrainingRequestController::update`: khối `validator->fails()` bị comment nên mọi ràng buộc chỉ có ở FE.

## 8. Cần người điều phối quyết định / sửa file dùng chung
- Không cần sửa file dùng chung nào. Đề xuất (không bắt buộc): `ApprovalCenterCleanTestCommand` nên xoá luôn dòng bảng gom của phiếu thử đã xoá.
- Ghi vào `plan.md` công việc này (không tự sửa để tránh va chạm với các agent khác).
- `ensureBootstrapped` chạy `needsBootstrap` cho TỪNG Definition mỗi lần mở màn: nhóm này thêm 10 Definition ⇒ cần theo dõi tổng chi phí khi cả 6 nhóm đăng ký (chọn 1 doc_type cho 19 loại Quyết định cũng nhằm giảm số này).
