# task-assignee-all-company — Mở "Người thực hiện" cho toàn công ty

**Người phụ trách:** @manhcuong
**Ngày tạo:** 2026-07-03

## Mục tiêu

Popup tạo/sửa task (CreateTaskModal — dùng chung cho /assign/tasks, my-job, solutions manager, solution-modules, my-todo, handover) cho phép chọn "Người thực hiện" (cả task cha lẫn task con) là **bất kỳ nhân viên đang hoạt động (status=1) trong công ty hiện tại**, thay vì chỉ PM/staff của giải pháp hoặc leader/staff của hạng mục.

## Hiện trạng & Quyết định

- Ràng buộc cũ chỉ nằm ở FE (computed `assigneeOptionsForModule` lọc theo solution/module staff). BE chỉ validate `exists:employees,id` — không cần sửa validate BE.
- Nguồn danh sách mới: endpoint có sẵn `GET assign/tasks/employees` (`TaskController::getEmployeesByCompany` — lọc `company_id = current_company_role` + `status = 1`). KHÔNG dùng `$store.state.employees` vì list đó chứa nhân viên mọi công ty.
- Người phê duyệt (`approverOptionsForSolution`) GIỮ NGUYÊN ràng buộc theo giải pháp (user chỉ yêu cầu mở Người thực hiện). Sửa lại check reset approver khi đổi solution/module cho đúng list approver (trước đây check nhầm theo list assignee).
- Bỏ reset assignee khi đổi solution/hạng mục + bỏ disable picker khi chưa chọn hạng mục (không còn phụ thuộc).
- Task đang sửa có assignee ngoài danh sách công ty (khác công ty/đã nghỉ) → append từ `peopleOptions` để picker vẫn hiển thị tên.

## Downstream phải sửa cho đúng (BE báo cáo)

Báo cáo **Giải pháp theo version** (/assign/report/solution-versions) lấy nhân sự từ snapshot `solution_version_members` → assignee ngoài snapshot bị bỏ sót:

1. `SolutionVersionsReportService::getVersionMembers()` — bổ sung assignee của task thuộc version nhưng không có trong snapshot (role "Thành viên", module = GROUP_CONCAT tên hạng mục từ task, giờ từ `task_result_progress_logs`).
2. `buildQuery()` cột `member_count` — cộng thêm `COUNT(DISTINCT assignee)` ngoài snapshot per version.

Các luồng khác đã đúng sẵn, không sửa: notification (gửi thẳng assignee), my-job/my-todo (lọc theo assignee), phân quyền xem task (tầng 1 luôn gồm assignee), báo cáo hiệu suất theo NV (đi từ tasks JOIN assignee, người ngoài staff hiện role mặc định "Thành viên").

Spec chi tiết: docs/superpowers/specs/2026-07-03-task-assignee-all-company-design.md
