# Quyền duyệt nhóm ĐÀO TẠO và QUYẾT ĐỊNH / VĂN BẢN (HRM) — @cuong61n

Ngày 16/11/2026. Chỉ đọc code (nhánh `gop_db-main` của `hrm-api`), không chạy lệnh ghi, không truy vấn DB. Đường dẫn tính từ `hrm-api/` (BE) và `hrm-client/` (FE). "Chưa xác minh" = chỉ suy từ code, chưa đối chiếu dữ liệu thật. Hạ tầng quyền chung (mã quyền, vai trò theo công ty, `manager_departments`, 3 biến thể "phòng tôi quản lý") đã có ở `00-ha-tang-quyen.md`, file này không nhắc lại.

---

## 0. Kết luận nhanh (đọc trước)

1. **"Quyền + là quản lý" chỉ đúng cho 3 loại phiếu ĐÀO TẠO ở cấp "Trưởng phòng"**: Đề xuất đào tạo (cấp 1), Đề xuất mở khoá học (cấp 1), Khoá học (cấp 1). Cả 3 = mã quyền Trưởng phòng AND `department_id` của phiếu ∈ `manager_departments` (phòng mình được phân công quản lý, gồm cờ "quản lý tất cả phòng ban"). Không dùng `department_lead_id`. Các cấp còn lại (QLĐT, BGĐ) và **toàn bộ nhóm Quyết định / sự cố / bảo hiểm** chỉ có MÃ QUYỀN, KHÔNG có điều kiện quản lý nào.
2. **Quyết định (19 loại có luồng, 2 cấp Xem xét → Duyệt)**: mọi loại dùng CHUNG 2 mã `decision.quyet_dinh.confirm` (Xem xét) và `decision.quyet_dinh.approve` (Duyệt) — không loại nào có quyền riêng (`Services/Decision/DecisionService.php:327-335`). Không có điều kiện quản lý, không có phạm vi công ty/phòng ban ở bước duyệt và ở các màn "chờ duyệt".
3. **Một người giữ nhiều cấp: KHÔNG bị chặn ở BE, FE bắt bấm lần lượt.** Quyết định: cùng người có `confirm` + `approve` thì bấm "Chuyển ban giám đốc duyệt" (status 2→3), màn tự quay lại danh sách (`go(-1)`), mở lại phiếu bấm "BGĐ duyệt" (3→5). BE không so `reviewed_by` với `approved_by`, không chặn người tạo tự duyệt. Có thể nhảy thẳng 2→5 bằng gọi API (không kiểm status hiện tại).
4. **Lỗi đã biết, đã xác minh lại**: `toggleApprove` Quyết định không kiểm status hiện tại (nhảy cấp); `status_request` của Đề xuất mở khoá học / Khoá học nhận giá trị 4 mà không kiểm gì (nhảy thẳng sang "Chờ BGĐ"); từ chối (4/6) không cần quyền ở 4 loại QĐ không có middleware; biên bản sự cố, kế hoạch đào tạo, kế hoạch/kỳ thi đánh giá năng lực, đăng ký khoá học, điểm danh: **BE không kiểm quyền duyệt**; bảo hiểm chỉ kiểm khi TỪ CHỐI.
5. **Phát hiện MỚI so với tài liệu nền** (xem mục 13): (a) middleware `checkPermission` giờ đi cùng cổng `CurrentPermission::has` với service, ý "2 bộ kiểm quyền lệch nhau" của `inventory-hrm.md` đã lỗi thời; (b) người có CẢ quyền Trưởng phòng LẪN quyền QLĐT/BGĐ bị lọc nhầm ở màn `type=waiting` (bộ lọc phòng quản lý áp luôn cho cấp 2); (c) khi duyệt Đề xuất mở khoá học / Khoá học thì `department_id` + `company_id` của phiếu bị ghi đè bằng của NGƯỜI DUYỆT; (d) Đề xuất mở khoá học / Khoá học phải còn `from_time >= hiện tại` mới duyệt được (422); (e) `deny` của Đề xuất mở khoá học không kiểm gì kể cả status; (f) màn chung `/decision/waiting-approve` KHÔNG lọc công ty đang làm.
6. **Đánh giá cho bảng gom**: biểu diễn được bằng cột gate đơn giản cho gần hết (xem mục 12). Ba chỗ cần lưu ý: cấp Trưởng phòng đào tạo = `permission` AND `department` (phải đọc "khớp gate_scope" là AND, không phải OR như `database.md` mục 5 có thể gây hiểu nhầm); Quyết định cần `approvable` cho phiếu thiếu mẫu in PLHĐ; **Yêu cầu điểm danh** không có người duyệt xác định, không biểu diễn được cho tới khi nghiệp vụ chốt.

---

## 1. Quyết định (bảng `decisions`) — 19 loại có luồng

### 1.1 Các cấp (mã status → chữ)

Hằng số `Modules/Decision/Entities/Decision.php:24-34`; điều kiện chuyển cấp: `DecisionService::toggleApprove` (`Services/Decision/DecisionService.php:327-351`).

| status | Hằng | Chữ nghiệp vụ | Chuyển tới | Ai bấm (theo FE) |
|---|---|---|---|---|
| 1 | `STATUS_CREATING` | Đang tạo (nháp) | gửi → 2 | người tạo (`decision.quyet_dinh.manage`, `isChangeData` `pages/decision/mixins/common-rules.js:19-27`) |
| 2 | `STATUS_CREATED` | Chờ xem xét (cấp 1) | Xem xét → 3; từ chối → 4 | người có `decision.quyet_dinh.confirm` |
| 3 | `STATUS_REVIEWED` | Đã xem xét / chờ duyệt (cấp 2) | Duyệt → 5; từ chối → 6 | người có `decision.quyet_dinh.approve` |
| 4 | `REJECTED_REVIEW` | Không xem xét | người tạo sửa lại, gửi lại → 2 | — |
| 5 | `STATUS_APPROVED` | Đã duyệt | (7 hiệu lực / 8 hết hiệu lực do job; 20 = đã sinh HĐLĐ với QĐ tiếp nhận) | — |
| 6 | `REJECTED_APPROVE` | Không duyệt | người tạo sửa lại | — |

Chữ cấp màn danh sách do FE/BE trả theo status; nút trên màn duyệt: `V2Footer.vue:51-64` ("Chuyển ban giám đốc duyệt" = cấp Xem xét, "BGĐ duyệt" = cấp Duyệt). Gửi lại sau khi bị từ chối: `updateOrCreateSimple` đặt `reviewed_by/approved_by = null` (`DecisionService.php:76-84`).

### 1.2 Ai được duyệt từng cấp

| Cấp | Mã quyền | Điều kiện quản lý | Phạm vi công ty/phòng | Bằng chứng BE | Bằng chứng FE |
|---|---|---|---|---|---|
| Xem xét (2→3) | `decision.quyet_dinh.confirm` (tên cũ `Xem xét quyết định`, Catalog `app/Support/Permissions/Catalog/decision.php:58`) | **Không** | **Không** (quyền kiểm theo công ty đang làm nhưng phiếu không bị lọc theo công ty) | `DecisionService.php:329-331` | `common-rules.js:45`, `:30-36` |
| Duyệt (3→5) | `decision.quyet_dinh.approve` (`Duyệt quyết định`, Catalog `decision.php:73`) | **Không** | **Không** | `DecisionService.php:333-335` | `common-rules.js:46` |
| Từ chối (4 hoặc 6) | không cần mã nào ở BE (xem 1.4) | Không | Không | `DecisionService.php:327-335` chỉ kiểm status 3 và 5 | `transfer-personnel/_id/approve.vue:121-126` chọn 4 hay 6 theo status hiện tại |

Quyền cấp "duyệt" trong Catalog khai `'scopes' => []` (không phạm vi) — `decision.php:58-86`. Không tồn tại quyền riêng theo loại QĐ.

### 1.3 Bảng loại × quyền × kiểm ở đâu

Cột "Middleware" = route `toggle-approve` có `->middleware('checkPermission:decision.quyet_dinh.approve|decision.quyet_dinh.confirm')` (có 1 mã là qua; cổng `CurrentPermission::has` — `app/Http/Middleware/CheckPermission.php:17-41`). "BE (service)" = `DecisionService::toggleApprove`. Tất cả: quyền Xem xét = `confirm`, quyền Duyệt = `approve`, không quản lý, không công ty.

| # | Loại (`decisions.type`) | Route (dòng `Routes/api.php`) | Controller::toggleApprove | Middleware | Việc phụ khi Duyệt (5) / điều kiện chặn |
|---|---|---|---|---|---|
| 1 | `department_establishments` (thành lập phòng) | 98 | `DepartmentEstablishmentController.php:92` | Có | ngày hiệu lực ≤ hôm nay → tạo phòng ban ngay |
| 2 | `department_changes` (sửa đổi phòng ban) | 109 | `DepartmentChangeController.php:76` | Có | hiệu lực ≤ hôm nay → cập nhật phòng |
| 3 | `department_dissolutions` (giải thể phòng ban) | 123 | `DepartmentDissolutionController.php:133` | Có | hiệu lực ≤ hôm nay → khoá phòng |
| 4 | `manpower_plannings` (ban hành định biên) | 239 | `ManpowerPlanningController.php:79` | Có | hiệu lực ≤ hôm nay → đồng bộ định biên |
| 5 | `decision_regulation_salary_alls` (quy chế lương) | 250 | `DecisionRegulationSalaryController.php:93` | Có | hiệu lực ≤ hôm nay → cập nhật quy chế đang dùng |
| 6 | `regulation_general_alls` (quy chế chung) | 533 | `Regulations/RegulationGeneralController.php:78` | Có | hiệu lực ≤ hôm nay → cập nhật quy chế đang dùng |
| 7 | `accept_personnels` (tiếp nhận nhân sự) | 278 | `AcceptPersonnelController.php:168` | Có | không (khối đồng bộ đã comment) |
| 8 | `decision_rewards` (khen thưởng) | **138** | `DecisionRewardController.php:105` | **KHÔNG** | ghi `updateReviewedValue`/`updateApprovedValue` TRƯỚC khi kiểm quyền (nằm trong transaction, quyền sai thì throw → rollback) |
| 9 | `decision_salary_bonuses` (thưởng lương tháng 13) | **152** | `DecisionSalaryBonusController.php:105` | **KHÔNG** | không |
| 10 | `employee_disciplines` (kỷ luật) | **316** | `EmployeeDisciplineController.php:59` | **KHÔNG** | cập nhật `meeting_participants.state_of_discipline` (3→4, từ chối→5); hiệu lực ≤ hôm nay → khoá nhân viên |
| 11 | `decision_appoint_personnels` (bổ nhiệm) | 332 | `AppointPersonnelController.php:108` | Có | **422 nếu thiếu mẫu in PLHĐ** (`AppendixLaborContract::isMissingDecisionPrintTemplate`, `Entities/AppendixLaborContract/AppendixLaborContract.php:42-45`); tự sinh phụ lục HĐLĐ |
| 12 | `decision_transfer_personnels` (điều chuyển) | 345 | `TransferPersonnelController.php:93` | Có | như 11; cập nhật `employee_department_dissolutions.state_of_decision` nếu có `department_dissolution_id` |
| 13 | `renew_labor_contracts` (ký HĐLĐ) | 359 | `RenewLaborContractController.php:118` | Có | không |
| 14 | `salary_changes` (điều chỉnh lương) | 371 | `SalaryChangeController.php:88` | Có | như 11 (422 thiếu mẫu in), sinh phụ lục |
| 15 | `assign_trainings` (cử đi đào tạo) | **379** | `AssignTrainingController.php:67` | **KHÔNG** | không (đoạn sinh HĐ đào tạo đã comment) |
| 16 | `termination_labor_contracts` (chấm dứt HĐLĐ) | 396 | `TerminationLaborContractController.php:119` | Có | hiệu lực ≤ hôm nay → đồng bộ nghỉ việc; cập nhật `employee_department_dissolutions` |
| 17 | `retirements` (nghỉ hưu) | 407 | `RetirementController.php:96` | Có | không (khối đồng bộ đã comment) |
| 18 | `suspend_labor_contracts` (tạm hoãn HĐLĐ) | 419 | `SuspendLaborContractController.php:82` | Có | gán số thoả thuận; hiệu lực ≤ hôm nay → đồng bộ nhân viên |
| 19 | `increase_seniorities` (tăng lương thâm niên) | 445 | `IncreaseSeniorityController.php:101` | Có | như 11 (422 thiếu mẫu in), sinh phụ lục |

Loại KHÔNG có luồng: `manpower_plannings_changes` — có hằng (`Decision.php:114`, có trong `Decision::TYPE`) nhưng không có route; xem `inventory-hrm.md` QĐ4. **Hợp đồng đào tạo** (`training_contracts`): route `toggle-approve` ở `Routes/api.php:427` nhưng `TrainingContractController` không có method → 500 (route chết, theo `inventory-hrm.md` QĐ22; mình chưa mở lại file controller). **HĐLĐ và Phụ lục HĐLĐ**: KHÔNG có `toggle-approve` trong `Routes/api.php:295-309, 451-461`, chỉ có `store/update/destroy` gắn `checkPermission:decision.hop_dong_lao_dong.create` / `decision.phu_luc_hop_dong_lao_dong.create`; FE `pages/decision/appendix-labor-contract/_id/approve.vue:119,152` gọi route `.../toggle-approve` không tồn tại (màn chết).

### 1.4 Kiểm ở đâu — BE hay chỉ FE (fail-open)?

- **BE kiểm 2 chỗ** (cùng cổng quyền theo công ty đang làm):
  1. Middleware (15/19 loại): có `confirm` HOẶC `approve` là qua — không xét status hiện tại, không xét loại hành động. Người chỉ có `confirm` vẫn qua cổng khi gửi `status=6` (từ chối duyệt) hay `status=2/7/…`.
  2. Service `toggleApprove` (cả 19 loại): chỉ 2 điều kiện: `status == 3` cần `confirm`; `status == 5` cần `approve` (`DecisionService.php:329-335`). **Mọi giá trị status khác (1, 2, 4, 6, 7, 8…) không kiểm quyền ở service** — với 4 loại không middleware (khen thưởng, thưởng T13, kỷ luật, cử đi đào tạo) nghĩa là **bất kỳ tài khoản đăng nhập nào** từ chối / đặt lại trạng thái được. Kiểm tra `status` hợp lệ: không có (`Request` thường, không FormRequest).
- **Không kiểm status hiện tại** ⇒ nhảy cấp: người có `approve` gọi `status=5` ngay cả khi phiếu đang 2 hoặc 1 (nháp); gọi lại `status=5` trên phiếu đã 5 chạy lại hiệu ứng phụ (sinh phụ lục, đồng bộ…); người có `confirm` gọi `status=3` trên phiếu đã 5 kéo lùi. Lỗi đã biết, xác minh lại đúng.
- **FE chỉ là lớp mặt**: `isShowApprove` (`common-rules.js:30-36`) = (`confirm` và status 2) hoặc (`approve` và status 3); mọi `approve.vue` gọi nó ở `mounted` rồi chuyển 404 (`transfer-personnel/_id/approve.vue:180`). Ngoại lệ: `regulations/salary/_id/approve.vue` không có redirect `isShowApprove` (chỉ footer lọc theo status/quyền, `mounted` ở `:64-68`); `appendix-labor-contract` màn chết (1.3).
- **Phạm vi công ty**: không có ở cả toggle (route-model-binding theo id bảng chi tiết, không so `company_id`) lẫn danh sách chờ. Chỉ có ở THÔNG BÁO: `EmployeeInfoService::listEmployeeInfoByPermission` lọc `employee_infos.company_id = công ty đang làm của người thao tác` (`Modules/Timesheet/Services/EmployeeInfoService.php:561-571`; gọi ở `DecisionService.php:394,406`). Người duyệt công ty khác không nhận thông báo nhưng vẫn gọi API duyệt được và vẫn THẤY phiếu trên màn chờ duyệt (1.5).

### 1.5 Màn chờ duyệt: ai THẤY, có khớp ai DUYỆT được không?

Có **2 loại màn**, cùng một logic lọc:

| Màn | API | Tiêu chí thấy | Nguồn |
|---|---|---|---|
| Chung `/decision/waiting-approve` | `GET decision/waiting-approve` | `status ∈ {2 nếu có confirm; 3 nếu có approve}`; **không lọc công ty đang làm, không lọc phòng, không lọc theo người tạo**; lọc tuỳ chọn `company_id` do người dùng chọn. Không có cả 2 quyền → `whereIn([])` ⇒ rỗng | `Services/Decision/WaitingApproveService.php:187-195` (không có `where company_id` mặc định) |
| Riêng từng loại (`*/waiting-approve.vue`, ngoài menu) | `GET decision/<loại>?type=waiting-approve` | giống trên, thêm: không có cả 2 quyền → `whereNull(id)`. **Bỏ qua** `DecisionViewScope` (nhánh scope nằm trong `else`) | `DecisionService.php:177-192` |

Hệ quả:
- **Thấy ⊇ Duyệt được**: ai có `confirm`/`approve` thấy đúng các phiếu cấp tương ứng của **mọi công ty**, trong khi quyền được kiểm theo công ty đang làm. Với nhân sự thuộc nhiều công ty, danh sách chứa cả phiếu công ty khác (có thể duyệt được nếu có quyền tại công ty đang làm, vì BE không so công ty phiếu). **Câu hỏi mở của `inventory-hrm.md` #578 "danh sách chờ có lọc công ty không" → KHÔNG.**
- **QĐ bổ nhiệm + điều chuyển bị ẩn khi HĐLĐ gắn kèm không còn hạn**: `WaitingApproveService.php:236-241` — `type ∉ {appoint, transfer}` HOẶC `whereDate(decision_labor_contracts.end_date, '>=', hôm nay)`; `end_date` NULL (HĐ không thời hạn) hoặc không có HĐLĐ gắn ⇒ false ⇒ phiếu **biến mất khỏi màn chung** (xác nhận lại `inventory-hrm.md` bất thường 1, phiếu 747). Màn riêng theo loại (`type=waiting-approve` ở `DecisionService.php`) KHÔNG có điều kiện này; màn riêng bổ nhiệm/điều chuyển không tồn tại (`inventory-hrm.md`), nên 2 loại này chỉ còn thấy qua màn danh sách thường/thông báo.
- **3 màn riêng hỏng**: `decision-reward/waiting-approve.vue` và `decision-salary-bonus/waiting-approve.vue` gọi `decision/department-dissolution` (chép nhầm từ giải thể phòng) — xác minh `pages/decision/decision-reward/waiting-approve.vue:303-306`, `pages/decision/decision-salary-bonus/waiting-approve.vue:303-306`; `manpower-planning/waiting-approve.vue` trỏ link nhầm (theo inventory, chưa mở lại).
- **Số đếm dashboard Quyết định**: coi `decision.quyet_dinh.manage` như đủ quyền xem xét lẫn duyệt (`Services/Dashboard/DashboardService.php:460-466`) — lệch với màn chờ và với `toggleApprove` (không nhận `manage`).
- **Danh sách thường**: người tạo chỉ thấy nháp (status 1) của mình, còn lại theo `decision.quyet_dinh.view` (scope) — `DecisionService.php:193-197` — không liên quan quyền duyệt.

### 1.6 Người tạo / người xem xét có tự duyệt được không?

**Có, không chặn ở đâu.** Tìm `reviewed_by`/`created_by` trong `Modules/Decision/{Http,Rules,Entities,Services}`: không có so sánh người thao tác với `created_by` hay `reviewed_by`; chỉ ghi nhận `reviewed_by`/`approved_by = auth()->id()` (`DecisionService.php:342-345`). FE cũng không ẩn nút khi `item.created_by == tôi`.

### 1.7 Một người giữ cả 2 cấp (Xem xét rồi Duyệt)

| Tình huống | Hành vi |
|---|---|
| Người A có `confirm` + `approve`, phiếu status 2 | FE hiện nút "Chuyển ban giám đốc duyệt" (status 2) — `isReviewed && status == 2` (`transfer-personnel/_id/approve.vue:8`). Bấm → gửi `status=3`. Xong `$router.go(-1)` (`:163`) về trang trước. |
| A mở lại phiếu (nay status 3) | FE hiện "BGĐ duyệt" (`isApprove && status == 3`, `:11`). Bấm → `status=5`. |
| Số lần bấm | **2 lần, tách thao tác, không tự nhảy cấp ở FE**. `reviewed_by = approved_by = A` (BE không phản đối). |
| Gọi thẳng API | `status=5` khi phiếu còn 2 **chạy được** (service không đọc status hiện tại) — bỏ qua bước Xem xét, `reviewed_by` để trống (hoặc giữ giá trị cũ). |

Với màn chung/riêng "chờ duyệt": người A có cả 2 quyền thấy phiếu status 2 VÀ 3 (`WaitingApproveService.php:187-195`) — vậy phiếu nào cũng hiện, không cần lọc thêm.

### 1.8 Điều kiện đặc thù / "không duyệt được nữa"

| Điều kiện | Áp cho | Bằng chứng | Hệ quả |
|---|---|---|---|
| Thiếu mẫu in PLHĐ (`appendix_print_template_id` trống hoặc mẫu rỗng) | bổ nhiệm, điều chuyển, điều chỉnh lương, tăng thâm niên — **chỉ khi `status == 5`** | `AppointPersonnelController.php:111-114`, `TransferPersonnelController.php:96-99`, `SalaryChangeController.php:91-94`, `IncreaseSeniorityController.php:104-107` | trả 422, phiếu kẹt ở "Chờ duyệt" tới khi người tạo chọn mẫu in (cấp Xem xét không bị chặn) |
| HĐLĐ gắn kèm `end_date` NULL / hết hạn | bổ nhiệm, điều chuyển | `WaitingApproveService.php:236-241` | **phiếu vẫn duyệt được qua URL/thông báo nhưng KHÔNG hiện** ở màn chung |
| Ngày hiệu lực ≤ hôm nay | QĐ cơ cấu, kỷ luật, chấm dứt, tạm hoãn, quy chế | các controller ở 1.3 | quyết định việc đồng bộ ngay hay chờ job (không chặn duyệt) |
| Nhập "giá trị đã xem xét/đã duyệt" | khen thưởng | `DecisionRewardController.php:108-112` + `DecisionRewardService.php:345` (`DecisionReward::find($request->id)`: `$request->id` lấy từ body; chưa xác minh FE có gửi `id`) | chưa xác minh |
| Hạn mức chi phí / cam kết | không thấy ở nhóm Quyết định | — | không áp |

Màn ẩn không gắn quyền, đưa QĐ/HĐLĐ về "Đang tạo": `Routes/api.php:78-81` (`decision/reset-status`, chỉ vào bằng URL) — mở lối "làm lại luồng" cho bất kỳ tài khoản nào biết URL. Chưa xác minh `DecisionResetStatusController` có kiểm quyền bên trong (grep "Permission" trong service/controller không thấy).

---

## 2. Biên bản xử lý sự cố (`trouble_shooting_reports`)

| Mục | Nội dung | Bằng chứng |
|---|---|---|
| Cấp | **1 cấp**: 1 đang tạo · **2 chờ duyệt** · 3 đã duyệt · 4 không duyệt | `Entities/TroubleShootingReport.php:15-18` |
| Ai duyệt | mã `decision.bien_ban_xu_ly_su_co.approve` (Catalog `Catalog/decision.php:258`; tên cũ `Duyệt biên bản xử lý sự cố`). Không quản lý, không phạm vi, không công ty | FE `category/trouble-shooting-reports/_id/approve.vue:131` |
| BE kiểm? | **KHÔNG**. Route không middleware (`Routes/api.php:291`); `TroubleShootingReportService::toggleApprove` (`Services/TroubleShootingReport/TroubleShootingReportService.php:302-318`) không gọi hàm quyền nào, không đọc status hiện tại. Bất kỳ tài khoản đăng nhập nào duyệt/từ chối được (kể cả phiếu đã duyệt, ghi lại `approved_by`, đổi `code`). Mọi lần gọi đều đặt lại `meeting_participants.state_of_discipline = 1` của người vi phạm (`:303-308`) | — |
| Ai THẤY (màn chờ) | `type=waiting-approve`: có `approve` → `status = 2`, không có → rỗng (`Services/TroubleShootingReport/TroubleShootingReportService.php:111-122`). Không lọc công ty/phòng | — |
| Khớp thấy/duyệt? | Thấy = có `approve`; duyệt = bất kỳ ai ở BE ⇒ BE rộng hơn FE | — |
| Người tạo tự duyệt | Không chặn (FE `approve.vue:131` chỉ kiểm quyền, không kiểm `created_by`; BE không kiểm) | — |
| Một người nhiều cấp | Chỉ 1 cấp nên không áp dụng | — |
| Thông báo | khi chuyển 2: gửi tất cả người có `approve` trong công ty (`TroubleShootingReportService.php:344-374`, nhánh `STATUS_CREATED` từ `:360`) | — |
| Điều kiện đặc thù | Không SoftDeletes; mỗi lần toggle ghi lại `code` (≠3 ⇒ null) — `TroubleShootingReportService.php:314` | — |

---

## 3. Phiếu đăng ký bảo hiểm (`insurance_registers`)

| Mục | Nội dung | Bằng chứng |
|---|---|---|
| Cấp | **1 cấp**: 1 đang tạo · **2 chờ duyệt** · 3 đã duyệt · 4 không duyệt · 5 hiệu lực · 6 hết hạn · 7 huỷ | `Entities/InsuranceRegister/InsuranceRegister.php:11-17` |
| Ai duyệt | `decision.phieu_dang_ky_bao_hiem.approve` (Catalog `Catalog/decision.php:493`; tên cũ `Duyệt phiếu đăng ký bảo hiểm`). Không quản lý, không phạm vi | FE `insurance/_id/approve.vue:131-136`: chặn nếu `status != 2` hoặc thiếu quyền |
| BE kiểm? | **Chỉ khi TỪ CHỐI (status 4)**: `InsuranceService.php:726-729`. **Duyệt (3) không kiểm quyền**; route không middleware (`Routes/api.php:477`). Không đọc status hiện tại. Huỷ: `cancel` không kiểm quyền (`InsuranceController.php:187-200`; route `Routes/api.php:482`), FE ẩn nếu thiếu `approve` (`insurance/index.vue:263`) | — |
| Ai THẤY | Màn `insurance/waiting-approve.vue` gọi `decision/insurance?status=2`: **không lọc theo quyền duyệt**, chỉ lọc theo **phạm vi của mã Xem** `decision.phieu_dang_ky_bao_hiem.view` qua `DecisionViewScope` (`InsuranceService.php:411-415,500-509`). Người tạo luôn thấy phiếu của mình. Mục "Duyệt" trong dropdown ở màn chờ CHỈ kiểm `status == 2`, không kiểm quyền (`insurance/waiting-approve.vue:209-214`) — bấm vào bị `approve.vue` chặn 404. Không có trong màn chung | — |
| Khớp thấy/duyệt | Không khớp: người có `.view` mà không có `.approve` thấy nút "Duyệt" ở màn chờ nhưng bị 404 | — |
| Người tạo tự duyệt | Không chặn. | — |
| Điều kiện đặc thù | Duyệt phải gửi `form_submit.insurance_type_id[]` với số tiền duyệt từng loại + từng nhân viên; tổng NV trả + công ty trả duyệt **không vượt** `total_fee` của loại (`InsuranceService.php:739-748`, so sánh ở `:745`), nếu vi phạm throw → transaction rollback. Mã phiếu `PDKBH_xxxxx` sinh lúc chuyển 2 (`:538-541`) | — |
| Thông báo | khi chuyển 2: người có `approve` trong công ty (`:542-550`) | — |

---

## 4. Đề xuất đào tạo (`training_requests`) — 2 cấp

Hằng `Entities/TrainingRequest.php:10-14`: 1 đang tạo · **2 chờ TP duyệt** · **3 chờ QLĐT duyệt** · 4 đã duyệt · 5 không duyệt. Cơ chế: `POST training/training_requests/{id}` với `status_request` (`Routes/api.php:152-163`).

| Cấp | `status_request` gửi lên | Điều kiện BE (`TrainingRequestController::update`, `:171-190`) | Quyền | Quản lý? | Công ty? |
|---|---|---|---|---|---|
| Gửi duyệt (1/2→) | 1, 2 | `canEdit()` (`Entities/TrainingRequest.php:48-51`): status ∈ {1,5} AND `department_id` ∈ `manager_departments` AND `created_by == tôi` | — | **Có**: người tạo phải là quản lý phòng của phiếu | không |
| **Cấp 1 — Trưởng phòng** (2→3) | 3 | `canDepartmentHeadApprove()` (`:58-69`): status == 2 AND mã `training.de_xuat_dao_tao_truong_phong.approve` AND `department_id` ∈ `manager_departments` | `training.de_xuat_dao_tao_truong_phong.approve` (Catalog `Catalog/training.php:333`) | **Có** (V1: `manageDepartmentIdsOf`, gồm cờ quản lý tất cả phòng) | **Không** (chỉ gián tiếp: `manager_departments` tính theo công ty đang làm) |
| **Cấp 2 — QLĐT** (3→4) | 4 | `canManagerTrainingApprove()` (`:76-87`): status == 3 AND mã `training.de_xuat_dao_tao_quan_ly_dao_tao.approve` | `Catalog/training.php:349` | **Không** | **Không** (không so `company_id`) |
| Từ chối | gọi `POST …/{id}/deny` (`:464-474`) | `canDeny()` (`:89-100`): status ∈ {2,3} AND (có 1 trong 2 mã) AND `current_company_role == company_id` | 1 trong 2 mã | **Không** (người có mã TP của phòng khác vẫn từ chối được) | Có |
| Lỗ hổng | `status_request` khác 1-4 | **Không kiểm gì**: gửi 5 ⇒ `$obj->status = 5` (Không duyệt) (`:258`) | — | — | — |

Validate FE/BE: khi 3 phải nhập `person_cost_*_department_head_approve` + `subject_approve_name`; khi 4 nhập `*_training_manager_approve` (`:204-213`) — **nhưng khối `validator->fails()` đã bị comment (`:227-229`)** nên các ràng buộc chỉ có trên FE. Rule `from_time >= hiện tại` cũng không còn hiệu lực ở update.

- **Ai THẤY (màn chờ `?type=waiting`, `:336-352`)**: giữ lại **sau** `TrainingViewScope::apply(... 'training.de_xuat_dao_tao.view' ...)` (`:333`, nhánh không `getForCourse`), rồi: không có cả 2 mã → `created_by = -1`; có mã TP → `status ∈ {2}` VÀ `department_id ∈ manager_departments`; có mã QLĐT → thêm `status 3`. **Lỗi thấy**: dòng `whereIn('department_id', manager_departments)` (`:344`) áp cho cả khi người đó còn là QLĐT ⇒ QLĐT kiêm TP chỉ thấy phiếu cấp 2 ở phòng mình quản lý. Số đếm dashboard cùng lỗi (`Modules/Training/Services/Dashboard/JobWaitingApproveService.php:39-60`, dòng `:50`). Cũng phải có quyền Xem `training.de_xuat_dao_tao.view` (scope), nếu không chỉ thấy phiếu mình tạo (`TrainingViewScope.php`, nhánh cuối `created_by`).
- **Người nhận thông báo ≠ người duyệt được**: `listEmployeeInfoByPermission($mã, $employeeInfoId)` nhận tham số thứ 2 nhưng bỏ qua (`Timesheet/Services/EmployeeInfoService.php:561`) ⇒ **mọi người có mã Trưởng phòng trong công ty** nhận thông báo (`TrainingRequestController.php:142,268`), kể cả không quản lý phòng của phiếu.
- **Tự duyệt**: Có thể. Người tạo bắt buộc là quản lý phòng (canEdit); nếu cũng có mã TP thì tự duyệt cấp 1 của chính phiếu mình — không có điều kiện `created_by != tôi`.
- **Một người nhiều cấp (TP + QLĐT)**: FE nút theo status (`TrainingRequestApproveForm.vue:665-669, 686-692`): 2 → "Trưởng phòng duyệt" (`submitSave(3)`), 3 → "QLĐT duyệt" (`submitSave(4)`). Xong chuyển về danh sách (`:1403`). Phải bấm lần lượt, mỗi lần BE kiểm lại status — **không thể nhảy 2→4** (4 yêu cầu status == 3). Đây là loại duy nhất trong nhóm có chống nhảy cấp đúng.
- **Điều kiện đặc thù**: QLĐT có quyền chọn môn + chi phí duyệt (FE). Cam kết (`month_committed`) lưu ở phiếu. Hạn mức chi phí: không thấy ràng buộc BE. FE list: nút Duyệt hiện đúng theo cờ BE `canDepartmentHeadApprove || canManagerTrainingApprove` (`training_requests/index.vue:229`; cờ trả ở `Transformers/TrainingRequestResource/TrainingRequestListResource.php:64-66`).

---

## 5. Đề xuất mở khoá học (`course_requests`) — 2 cấp

Hằng `Entities/CourseRequest.php:12-16`: 1 · **2 chờ TP duyệt** · **4 chờ BGĐ duyệt** · 5 đã duyệt · 6 không duyệt (3 là giá trị `status_request`, không phải status).

| Cấp | `status_request` | Điều kiện BE (`CourseRequestController::update:171-190`) | Quyền | Quản lý? | Công ty? |
|---|---|---|---|---|---|
| Gửi duyệt | 1, 2 | `canEdit()` (`Entities/CourseRequest.php:168-173`): status ∈ {1,6} AND mã `training.de_xuat_mo_khoa_hoc.create` AND `info.department_id == department_id` (**phòng của chính người tạo**, không phải "quản lý") AND `created_by == tôi` | `…de_xuat_mo_khoa_hoc.create` | Không (cùng phòng) | không |
| **TP duyệt** (2→4) | 3 | `canDepartmentHeadApprove` (`:179-192`): status == 2 AND mã `…de_xuat_mo_khoa_hoc_truong_phong.approve` AND `department_id ∈ manager_departments` | Catalog `training.php:397` | **Có** | không |
| **BGĐ duyệt** (4→5) | 5 | `canDirectorApprove` (`:197-210`): status == 4 AND mã `…de_xuat_mo_khoa_hoc_ban_giam_doc.approve` AND `current_company_role == company_id` | Catalog `training.php:413` | Không | **Có** |
| Từ chối | `POST …/{id}/deny` | **KHÔNG kiểm gì** (`CourseRequestController.php:305-336`): không quyền, không status, không công ty. Bất kỳ tài khoản đăng nhập nào, kể cả với phiếu đã duyệt | — | — | — |
| Lỗ hổng nhảy cấp | `status_request = 4` (hoặc 6/…) | **Không kiểm** (`update` chỉ kiểm 1,2,3,5); `Service::update` ghi `status = status_request` (`CourseRequestService.php:311`) ⇒ người bất kỳ đẩy phiếu từ 2 sang "Chờ BGĐ" mà bỏ qua TP | — | — | — |

- **Tác dụng phụ chưa có ở tài liệu nền**: mọi lần `update` (kể cả khi TP/BGĐ duyệt) ghi đè `company_id = công ty đang làm` và `department_id = phòng của NGƯỜI THAO TÁC` (`CourseRequestService.php:310-311`). BGĐ duyệt xong, phòng của phiếu thành phòng của BGĐ.
- **Điều kiện đặc thù / "không duyệt được nữa"**: validate chạy THẬT ở update (`CourseRequestController.php:269-275`): `from_time` và `to_time` phải `>= thời điểm hiện tại`, bắt buộc `subject_approve_name` ở 3 và 5 ⇒ **phiếu có `from_time` đã qua thì cả TP lẫn BGĐ đều nhận 422** ("Phải lớn hơn hoặc bằng thời gian hiện tại"). FE có cho sửa lại `from_time` lúc duyệt hay không: chưa xác minh.
- **Ai THẤY (`CourseRequestService.php:75-94`)**: sau `TrainingViewScope` `training.de_xuat_mo_khoa_hoc.view`; TP: `status 2 AND department ∈ manager_departments`; BGĐ: `status 4` (không lọc công ty; BE duyệt bắt buộc công ty khớp) — BGĐ có quyền Xem phạm vi tổng công ty thấy cả phiếu công ty khác nhưng không duyệt được. Cùng lỗi kiêm nhiệm TP + BGĐ như mục 4 (`:86`).
- **Thông báo**: dùng `listEmployeeInfoHasPermission($mã, $employeeInfoId)` (`CourseRequestService.php:327,341`) — đúng "quản lý phòng của người gửi ∩ có mã" (`Timesheet/Services/EmployeeInfoService.php:544-558`) ⇒ **khớp** người duyệt cấp TP (khác Đề xuất đào tạo). Cấp BGĐ: cũng dùng hàm này nên chỉ gửi cho người VỪA quản lý phòng của người gửi VỪA có mã BGĐ (hẹp hơn so với BE chấp nhận mọi người có mã BGĐ cùng công ty).
- **Tự duyệt / nhiều cấp**: như mục 4 — không chặn tự duyệt; người kiêm TP + BGĐ bấm lần lượt (FE `CourseRequestApproveFormShow.vue:757-758`: cần `form.isTruongPhong` / `form.isBangiamdoc` từ BE `CourseRequestService.php:227-228`). FE chỉ kiểm MÃ, không kiểm quản lý phòng — nút TP có thể hiện mà BE từ chối 403. List: cờ BE đủ điều kiện (`CourseRequestListResource.php:68-71`, `course_requests/index.vue:233`).

---

## 6. Khoá học (`courses`) — 2 cấp

Hằng `Entities/Course.php:14-18` (giống đề xuất mở khoá học: 2 chờ TP · 4 chờ BGĐ · 5 đã duyệt · 6 không duyệt).

| Cấp | `status_request` | Điều kiện BE (`CourseController::update:285-302`) | Quyền | Quản lý? | Công ty? |
|---|---|---|---|---|---|
| Gửi duyệt | 1, 2 | `canEdit` (`Entities/Course.php:331-342`): status ∈ {1,6} AND mã `training.khoa_hoc.create` AND `created_by == tôi` | `khoa_hoc.create` | Không | không |
| TP duyệt (2→4) | 3 | `canDepartmentHeadApprove` (`:349-362`): status == 2 AND `training.khoa_hoc_truong_phong.approve` AND `department_id ∈ manager_departments` | Catalog `training.php:477` | **Có** | không |
| BGĐ duyệt (4→5) | 5 | `canDirectorApprove` (`:367-380`): status == 4 AND `training.khoa_hoc_ban_giam_doc.approve` AND công ty khớp | Catalog `training.php:493` | Không | **Có** |
| Từ chối | `POST …/{id}/deny` | `canDeny` (`:385-397`): status ∈ {2,4} AND (1 trong 2 mã) AND `current_company_role == company_id`, **không kiểm phòng quản lý** (`CourseController.php:557-568`) | 1 trong 2 | Không | Có |
| Lỗ hổng | `status_request = 4` | Không kiểm (xem mục 5) | — | — | — |

- Cùng ghi đè `company_id`/`department_id` bằng của người thao tác khi duyệt (`Services/Course/CourseService.php:483-484`; lúc store `:420-421`).
- Cùng validate `from_time >= hiện tại` + phải nhập `cost_department_head_approve` (3) / `cost_director_approve` (5) cho từng khoản (`CourseController.php:320-336`, bắt lỗi `:414`) ⇒ khoá học đã quá ngày bắt đầu không duyệt được nữa; chỉ phiếu chờ duy nhất 2025-05-26 trong `inventory-hrm.md` đang treo gần 17 tháng rất có thể do đây — **chưa xác minh** (không xem dữ liệu).
- **Ai THẤY (`CourseService.php:110-196`)**: scope mã Xem `training.khoa_hoc.view` (`:116-171`: toàn bộ ẩn nháp của người khác; scope 0 = chỉ khoá mình tạo / phụ trách / giảng viên) rồi `type=waiting` (`:180-196`) giống mục 5 (cùng lỗi kiêm TP+BGĐ ở `:188`).
- Thông báo: `listEmployeeInfoHasPermission` (`CourseService.php:506,525`).
- Tự duyệt / nhiều cấp: như mục 5. FE cờ list `canDepartmentHeadApprove || canDirectorApprove` (`courses/index.vue:271`; `CourseListResource.php:85` còn có `canDeny`).

---

## 7. Đăng ký khoá học của học viên (`course_registers`, status 5 = chờ duyệt)

| Mục | Nội dung | Bằng chứng |
|---|---|---|
| Cấp | **1 cấp**: 5 `PENDING` chờ duyệt → 10 duyệt / 15 từ chối (6 huỷ, 20 hoãn) | `Entities/CourseRegister.php:13-14`; `Services/CourseRegister/CourseRegisterService.php:88-111` |
| Ai duyệt | mã `training.dang_ky_khoa_hoc.approve` (Catalog `Catalog/training.php:526`). Không quản lý, không phạm vi, **không gắn với người phụ trách/giảng viên khoá** | FE `course-registers/_id/approve.vue:214` (cũng chặn `status != 5`); list `course-registers/index.vue:156,404` |
| BE kiểm? | **KHÔNG**. Route không middleware (`Routes/api.php:282`); `toggleApprove` (`CourseRegisterService.php:88-111`) không kiểm quyền, không kiểm status, không kiểm công ty; chỉ xử lý `status == 10` và `== 15`, giá trị khác → bỏ qua | — |
| Ai THẤY | `getList` (`:20-72`): **ai có `…approve` thấy MỌI đăng ký, không áp phạm vi Xem** (`:66-79` — chỉ người KHÔNG có `approve` mới qua `TrainingViewScope` `training.dang_ky_khoa_hoc.view`); lọc `company_id` chỉ khi người dùng chọn. Dashboard đếm `status = 5` mọi công ty (`JobWaitingApproveService.php:110-115`) và chỉ hiện thẻ khi có `…approve` (`DashboardService.php:117-124`) | — |
| Người tạo tự duyệt | Học viên tự đăng ký; nếu nhân viên đó có `…approve` thì tự duyệt được (không so `created_by`) | — |
| Một người nhiều cấp | 1 cấp, không áp dụng | — |
| Điều kiện đặc thù | Không | — |

---

## 8. Yêu cầu điểm danh học viên (`course_student_attendances`, status 1 = chờ duyệt)

| Mục | Nội dung | Bằng chứng |
|---|---|---|
| Cấp | `Entities/CourseStudentAttendance.php:12-16`: 0 chưa điểm danh · **1 chờ duyệt** · 2 duyệt · 3 không duyệt. Học viên tự điểm danh (status 0 → 1) `AttendanceController::studentAttendance` (`Http/Controllers/V1/AttendanceController.php:55-77`) | — |
| Ai duyệt | **Không xác định.** Không có mã quyền, không có điều kiện "người phụ trách / giảng viên" ở BE hay FE. Nút "Lưu" ở tab học viên (`CourseFormShow.vue:2089-2094`) và ô "Click để duyệt" (`CourseForm.vue:2132-2137`) hiện cho bất kỳ người nào mở được màn khoá học | — |
| BE kiểm? | **KHÔNG**: `studentAttendanceApprove` / `approve-multiple` (`Routes/api.php:234-235`; `CourseController.php:902-914, 929-941`; `CourseService.php:808-828`) chỉ `update status`, không quyền/không status/không công ty/không "đúng khoá"; `status` mặc định 1 nếu không gửi | — |
| Ai THẤY | Không có màn chờ duyệt (inventory: `/training/attendance/request-list` là của chính học viên) | `inventory-hrm.md` H22 |
| Tự duyệt | Học viên có quyền mở màn khoá có thể tự duyệt điểm danh của mình (chưa xác minh FE ai mở được tab học viên) | — |

---

## 9. Kế hoạch đào tạo (`training_plannings`, status 2 = chờ duyệt)

| Mục | Nội dung | Bằng chứng |
|---|---|---|
| Cấp | **1 cấp**: 2 chờ duyệt → 3 duyệt / 4 không duyệt | `Services/TrainingSurveyPlanning/TrainingSurveyPlanningService.php:350-362` |
| Ai duyệt | `training.ke_hoach_dao_tao.approve` (Catalog `Catalog/training.php:299`). Không quản lý, không phạm vi | FE `training-survey-planning/_id/approve.vue:126`; menu `components/menu-sidebar.js:630` |
| BE kiểm? | **KHÔNG** (không quyền, không status, không công ty): route `Routes/api.php:397` không middleware, `toggleApprove` chỉ gọi `update` theo `status` 3 hoặc 4; giá trị khác trả `null` thành công. Người tạo/ai cũng duyệt được kể cả phiếu nháp | — |
| Ai THẤY | `training-survey-planning/need-approve` gọi `training/training-planning?status=2`, lọc theo **phạm vi mã Xem** `training.ke_hoach_dao_tao.view` (`TrainingSurveyPlanningService.php:239`), không lọc theo quyền duyệt. Dashboard đếm `status=2` MỌI công ty (`JobWaitingApproveService.php:31-36`) | — |
| Tự duyệt / nhiều cấp | Không chặn tự duyệt (không so `created_by`). 1 cấp | — |
| Thông báo | không thấy gửi thông báo cho người duyệt khi gửi duyệt (grep không ra) — chưa xác minh hoàn toàn | — |

---

## 10. Kế hoạch đánh giá năng lực và Kỳ thi đánh giá năng lực — 2 cấp (QLĐT → BGĐ)

Cả hai cùng khuôn: status **2 chờ QLĐT** → (QLĐT duyệt) **3 chờ BGĐ** → (BGĐ duyệt) **5 đã duyệt**; **4 từ chối**; không hằng số (suy từ FE).

| Loại | Mã QLĐT | Mã BGĐ | BE | FE |
|---|---|---|---|---|
| Kế hoạch đánh giá (`evaluation_planning_capacities`) | `training.ke_hoach_danh_gia_quan_ly_dao_tao.approve` (`Catalog/training.php:575`) | `training.ke_hoach_danh_gia_ban_giam_doc.approve` (`:591`) | `CapacityEvaluatePlanningService::toggleApprove` (`:1456-1485`): `update status = request->status`; nếu status 3 thì gửi thông báo cho người có mã BGĐ | list: `capacity-evaluate-planning/index.vue:168,174` (status 2 & mã QLĐT / status 3 & mã BGĐ); `_id/approve.vue:232-248` |
| Kỳ thi (`evaluation_capacities`) | `training.ky_thi_danh_gia_nang_luc_quan_ly_dao_tao.approve` (`:639`) | `training.ky_thi_danh_gia_nang_luc_ban_giam_doc.approve` (`:655`) | `CapacityEvaluateService::toggleApprove` (`:270-296`): như trên | `capacity-evaluate/index.vue:182,188`; `_id/approve.vue:231-251` |

- **BE kiểm?** KHÔNG quyền, KHÔNG status hiện tại, KHÔNG công ty, KHÔNG quản lý (routes `Routes/api.php:453`, `:472` không middleware; service nhận bất kỳ `status`). Nhảy cấp tự do (gửi 5 ngay từ 2; gửi 3 hay 5 từ bất kỳ).
- **Quản lý?** Không. **Phạm vi?** Không.
- **Ai THẤY / màn chờ**: không có màn "chờ duyệt" riêng (`inventory-hrm.md` H24-H25); dòng duyệt nằm trong danh sách chung của màn.
- **Một người nhiều cấp (QLĐT + BGĐ)**: FE **có xử lý riêng**: nếu CÓ CẢ HAI mã thì không chặn theo status ở `created()` (`capacity-evaluate-planning/_id/approve.vue:232-248`; ngược lại chỉ 1 mã thì phải status khớp, không thì 404). Footer hiện nút theo status (`boardDirectorApprove: status == 3`, `trainingManagementApprove: status == 2`, `capacity-evaluate/_id/approve.vue:90-91`) ⇒ bấm lần lượt (2→3 rồi 3→5, `approve()` lấy `status = formData.status == 3 ? 5 : 3`, `:189`). BE không chặn.
- **Tự duyệt**: không chặn. **Điều kiện đặc thù**: không thấy.

---

## 11. Các mục khác trong nhóm (đã rà)

| Mục | Kết quả | Bằng chứng |
|---|---|---|
| Duyệt câu hỏi | **Route chết**: `POST training/questions/{id}/deny` (`Routes/api.php:176`) nhưng `QuestionController` không có method `deny` (grep `function deny` chỉ có ở Capability/Course/CourseRequest/TrainingRequest controller). Câu hỏi chỉ có khoá/mở khoá (`:174-175`) | `Http/Controllers/V1/` |
| Kết quả thi | **Route chết**: `POST exam-results/{id}/deny` (`Routes/api.php:321`) không có method trong `ExamResultController`. `ExaminerController::approveExamResultOffline` (`:863-882`, route `Routes/api.php:89`) thực chất là CHỐT điểm đạt/không đạt (`result = 1 or 3`) theo điểm đạt, không phải phiếu duyệt, không kiểm quyền | — |
| `CapabilityController::deny` | không có route; mã sao chép của đề xuất đào tạo, đã lạc loài (`CapabilityController.php:245`) | — |
| Thông báo nội bộ (`self_notifications`, module Human) | có `toggle-approve` (`Routes/api.php:359`, `SelfNotificationsController.php:113-134`) nhận `status` bất kỳ, không kiểm quyền/status; trạng thái "Gửi duyệt" đã bị comment (`Entities/SelfNotifications.php:33-37`), `canApprove` dùng tên cũ `Duyệt thông báo nội bộ` không có trong Catalog. **Không có cấp "chờ duyệt" thật → loại khỏi bảng gom** (chưa xác minh FE còn gửi `status`) | — |
| Hợp đồng đào tạo | không có luồng duyệt (xem 1.3) | — |

---

## 12. Đánh giá cho BẢNG GOM (`approval_inbox_items`): Definition phải khai gì

Ký hiệu theo `database.md` mục 2/5: `gate_type` ∈ {`permission`, `approver`, `dept_manager`, `assignee_list`}, `gate_scope`, `required_permission`.

| Loại | Cấp hiện tại ← cột | gate (1) mã quyền (2) quản lý phòng (3) đích danh (4) kết hợp | Biểu diễn được bằng cột gate đơn giản? | Ghi chú |
|---|---|---|---|---|
| Quyết định (19 loại) | status 2 → `required_permission = decision.quyet_dinh.confirm`; status 3 → `decision.quyet_dinh.approve` | (1) | **Có** (`permission`, `gate_scope=none`) | 2 cấp cùng 1 phiếu, cấp đổi theo status; registry chỉ tính cấp hiện tại ⇒ "một người nhiều cấp" không phát sinh dòng thừa (người đó thấy phiếu ở cấp nào thì dòng ấy). Công ty: BE không lọc; bảng gom lọc `company_id = công ty đang làm` (database.md §5) = **thu hẹp hành vi** so với màn chung hiện tại (đang thấy mọi công ty) — cần chốt. `approvable`: bổ nhiệm/điều chuyển/lương/thâm niên thiếu mẫu in PLHĐ ⇒ cấp Duyệt không duyệt được (422), nên tính `approvable = 0` cho status 3 của 4 loại này. **Đừng copy** lỗi `end_date` của `WaitingApproveService:236-241` |
| Biên bản sự cố | status 2 → `decision.bien_ban_xu_ly_su_co.approve` | (1) | Có | BE hiện không kiểm; gate bảng gom chặt hơn BE — chấp nhận được (chỉ người có mã thấy) |
| Phiếu đăng ký bảo hiểm | status 2 → `decision.phieu_dang_ky_bao_hiem.approve` | (1) | Có | Màn hiện lọc theo phạm vi mã **Xem**, không theo mã duyệt; bảng gom lọc theo mã duyệt ⇒ người có `.view` không có `.approve` hết thấy phiếu (đúng nghiệp vụ) |
| Đề xuất đào tạo — cấp TP (2) | `training.de_xuat_dao_tao_truong_phong.approve` | **(4) = (1) AND (2)** | **Có nếu** hiểu `gate_type=permission` + `gate_scope=department` nghĩa là "có mã AND `department_id ∈ manageDepartmentIdsOf(tôi, công ty)`" (đúng V1 `PermissionHelper.php:98-113`, gồm cờ quản lý tất cả phòng). **KHÔNG được** đọc nó là OR giữa 2 gate (`database.md` §5 viết `gate_type='dept_manager'` là nhánh độc lập: nếu dùng nhánh đó cho cấp TP, mọi quản lý phòng — dù không có mã Trưởng phòng — sẽ thấy phiếu = lộ) | Cần ghi rõ trong Definition: AND |
| Đề xuất đào tạo — cấp QLĐT (3) | `training.de_xuat_dao_tao_quan_ly_dao_tao.approve` | (1) | Có | BE không so công ty ở cấp này; bảng gom lọc công ty đang làm = thu hẹp, cần chốt |
| Đề xuất mở khoá học — TP (2) | `…de_xuat_mo_khoa_hoc_truong_phong.approve` | (4) permission AND department | Có (như trên) | |
| Đề xuất mở khoá học — BGĐ (4) | `…de_xuat_mo_khoa_hoc_ban_giam_doc.approve` + công ty | (1) + `company_id` | Có | BE đòi `company_id == công ty đang làm` — đúng điều kiện chung của bảng gom |
| Khoá học — TP (2) / BGĐ (4) | `training.khoa_hoc_truong_phong.approve` / `training.khoa_hoc_ban_giam_doc.approve` | giống 2 dòng trên | Có | |
| `approvable` cho Đề xuất mở khoá học và Khoá học | — | — | **Cần cột `approvable`** | `from_time` đã qua ⇒ cả TP lẫn BGĐ nhận 422 (mục 5, 6); Definition: `approvable = (from_time >= now)`. Đề xuất đào tạo KHÔNG có ràng buộc này (validate bị comment) |
| Đăng ký khoá học (5) | `training.dang_ky_khoa_hoc.approve` | (1) | Có | Không có khái niệm quản lý / người phụ trách khoá. Hiện ai có mã thấy mọi công ty ⇒ bảng gom lọc công ty = thu hẹp |
| Kế hoạch đào tạo (2) | `training.ke_hoach_dao_tao.approve` | (1) | Có | |
| Kế hoạch đánh giá, Kỳ thi ĐGNL | status 2 → mã `…quan_ly_dao_tao.approve`; status 3 → mã `…ban_giam_doc.approve` | (1) | Có | Trạng thái không có hằng số BE: Definition phải tự ghi 2/3/4/5 |
| **Yêu cầu điểm danh học viên** | status 1 | **không có** | **KHÔNG biểu diễn được** | Không có người duyệt xác định. Gợi ý (cần user chốt, không phải hành vi hiện tại): người phụ trách (`course_person_charges`) + giảng viên (`course_teachers`) của khoá ⇒ (3) `assignee_list` đích danh |

**Các điểm bảng gom KHÔNG được sao chép từ hành vi hiện tại**: (i) bộ lọc phòng quản lý áp cho cả cấp 2 khi người dùng kiêm 2 cấp (lỗi mục 4/5/6); (ii) thông báo gửi cho "mọi người có mã" khác với "người duyệt được" (Đề xuất đào tạo); (iii) BE nhiều chỗ không kiểm — bảng gom sẽ là cửa chặt hơn, nên khi gọi duyệt từ màn gom phải đi qua đúng hàm duyệt lẻ và **bổ sung kiểm quyền/status ở hàm lẻ** (thuộc việc "Điều kiện bảo mật trước khi làm duyệt nhanh/hàng loạt" `danh-gia-tung-phieu.md` §7.6); (iv) người tạo tự duyệt được ở mọi loại — nếu muốn ẩn phiếu của chính người xem khỏi hàng đợi thì đó là thay đổi nghiệp vụ, cần user chốt (cấp Trưởng phòng đào tạo thì người tạo mặc định cũng là quản lý phòng, nên phiếu của mình LUÔN nằm trong hàng đợi nếu giữ nguyên).

**Trường hợp "một người nhiều cấp" cho registry**: vì mỗi phiếu chỉ ở 1 cấp tại một thời điểm (status đơn), người kiêm 2 cấp chỉ thấy phiếu ở cấp hiện tại, bấm xong phiếu sang cấp kế rồi vẫn hiện trong hàng đợi của chính họ (2 lần xuất hiện liên tiếp). `approval_inbox_logs` nên ghi 2 dòng (2 cấp) cùng `actor_id`. Nếu muốn "bấm 1 lần duyệt cả 2 cấp" thì phải bổ sung nghiệp vụ mới (hiện không có ở BE lẫn FE).

---

## 13. Mâu thuẫn / bổ sung so với tài liệu nền (`inventory-hrm.md`, `danh-gia-tung-phieu.md`)

| # | Tài liệu nền nói | Code đang chạy | Bằng chứng |
|---|---|---|---|
| 1 | Middleware `checkPermission` dùng spatie `getAllPermissions()` trên `Modules\Timesheet\Entities\Employee`, lệch với service (`inventory-hrm.md:187`) | **Lỗi thời.** Middleware gọi `CurrentPermission::has` (cùng cổng với `isCurrentEmployeeHasPermission`); tên quyền đã đổi sang MÃ `decision.quyet_dinh.approve|confirm` | `app/Http/Middleware/CheckPermission.php:17-41`; `app/Helper/PermissionHelper.php:20-26` |
| 2 | Quyền tên tiếng Việt ("Xem xét quyết định", "Trưởng phòng duyệt đề xuất đào tạo"…) | Đã chuyển sang mã `phan_he.doi_tuong.hanh_dong`; tên cũ chỉ còn là bí danh | Catalog `decision.php:58,73,258,493`; `training.php:299,333,349,397,413,477,493,526,575,591,639,655` |
| 3 | Số dòng (`:58/:76/:89`, `api.php:91`…) | Đã trôi; nay `TrainingRequest.php:58,76,89`, `Routes/api.php:98…` (bảng 1.3) | — |
| 4 | "Danh sách chờ có lọc theo công ty đang làm không?" (câu hỏi mở) | **Không lọc** (cả màn chung lẫn riêng từng loại) | `WaitingApproveService.php:187-195`, `DecisionService.php:177-192` |
| 5 | H18 `canDeny` không kiểm phòng quản lý; gửi `status_request` khác 1-4 bỏ qua kiểm tra | **Đúng**; riêng `canDeny` có kiểm công ty | `TrainingRequest.php:89-100`, `TrainingRequestController.php:175-190` |
| 6 | H19: `deny` không kiểm quyền; gửi `status_request` = 4 nhảy sang BGĐ | **Đúng**, và `deny` còn không kiểm cả status | `CourseRequestController.php:305-336`, `:175-186`, `CourseRequestService.php:311` |
| 7 | H20 chỉ nêu kẽ hở `status_request` | Đúng; thêm: `Course::deny` CÓ kiểm (`canDeny`: quyền + status + công ty, không kiểm phòng) | `CourseController.php:557-568`, `Course.php:385-397` |
| 8 | H21, H23, H24, H25, QĐ20 "BE không chốt"; QĐ21 chỉ kiểm khi từ chối | **Đúng hết** (mục 2, 3, 7, 9, 10) | — |
| 9 | (không nêu) | **Mới**: người có cả mã TP lẫn mã QLĐT/BGĐ bị lọc phòng sai ở màn chờ + dashboard của 3 loại đào tạo | `TrainingRequestController.php:336-352`, `CourseRequestService.php:78-94`, `CourseService.php:180-196`, `JobWaitingApproveService.php:50,74,98` |
| 10 | (không nêu) | **Mới**: duyệt Đề xuất mở khoá học / Khoá học ghi đè `department_id`, `company_id` của phiếu bằng của người duyệt | `CourseRequestService.php:310-311`, `CourseService.php:483-484` |
| 11 | (không nêu) | **Mới**: Đề xuất mở khoá học / Khoá học 422 khi `from_time` đã qua lúc duyệt (có thể giải thích phiếu Khoá học treo 17 tháng) | `CourseRequestController.php:269-275`, `CourseController.php:320-321, 414` |
| 12 | (không nêu) | **Mới**: danh sách Đăng ký khoá học — ai có `…approve` bỏ qua phạm vi Xem, thấy mọi công ty | `CourseRegisterService.php:66-79` |
| 13 | (không nêu) | **Mới**: thông báo cấp TP của Đề xuất đào tạo gửi mọi người có mã (không giới hạn quản lý phòng) vì tham số bị bỏ qua | `EmployeeInfoService.php:561`, `TrainingRequestController.php:142,268` |
| 14 | (không nêu) | **Mới**: validate của `TrainingRequestController::update` bị comment, nên ràng buộc ngày/chi phí khi duyệt chỉ ở FE | `TrainingRequestController.php:227-229` |
| 15 | (không nêu) | **Mới**: HĐLĐ / Phụ lục HĐLĐ không có luồng duyệt (FE phụ lục gọi route không tồn tại); route `reset-status` không gắn quyền | `Routes/api.php:295-309, 451-461, 77-81` |
| 16 | `danh-gia-tung-phieu.md` §3 gọi Quyết định là "17 loại" | Code có **19 loại có luồng** (+1 hằng không route, + HĐ đào tạo route chết) | `Decision.php:79-108`, bảng 1.3 |
| 17 | `danh-gia-tung-phieu.md` §3: phiếu bảo hiểm "Đã tạo" | status 2 = Chờ duyệt (`STATUS_CREATED`), không trùng chữ "Đã tạo" của nháp | `InsuranceRegister.php:11-17` |
| 18 | "Super admin (role 18) vượt quyền" | Lỗi thời (xem `00-ha-tang-quyen.md` §0.3) — không thấy bypass trong các luồng nhóm này | — |

### Chưa xác minh
- Dữ liệu thật (có người nào đang giữ đồng thời `confirm` + `approve`, có phiếu đào tạo nào bị kẹt 422 do `from_time` đã qua).
- FE có cho sửa `from_time` lúc TP/BGĐ duyệt Đề xuất mở khoá học / Khoá học hay không.
- `DecisionResetStatusController` / `TrainingContractController` kiểm quyền bên trong (chỉ rà qua route + grep).
- `DecisionRewardController::toggleApprove` có nhận `request->id` không (service gọi `DecisionReward::find($request->id)`).
- Màn riêng `manpower-planning/waiting-approve.vue` (link nhầm, lấy theo inventory).
- Quyền "xem" số tiền ở đề xuất đào tạo / phiếu bảo hiểm (`danh-gia-tung-phieu.md` §8, ngoài phạm vi file này).
