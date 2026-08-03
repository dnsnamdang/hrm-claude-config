# Phân quyền màn danh sách Issue — Design (tóm tắt)

**Màn:** `/assign/issues` — `Modules/Assign` (BE) + `pages/assign/issues` (FE)
**Người phụ trách:** @manhcuong

## Mục tiêu
Áp dụng phân quyền xem danh sách Issue theo skill `list-page` (org-based, 4 cấp) đồng thời giữ
quyền xem tự động theo vai trò cá nhân và theo Dự án/Giải pháp. Nguồn yêu cầu: `phan_quyen_issue.xlsx` (sheet "Issue").

## Mô hình 3 tầng (theo Excel)
- **Tầng 1 — vai trò cá nhân (tự động, không cần tick):** người xem luôn thấy issue mà mình là 1 trong 6 vai trò:
  Người tạo (`creator_id`), Người phát hiện (`detected_by`), Người phụ trách (`assignee_id`),
  Người phối hợp (`supporters` n-n), Người duyệt đóng (`approver_id`), Người theo dõi (`watchers` n-n).
- **Tầng 2 — thành viên Dự án/Giải pháp (tự động):** thấy issue thuộc `solution_id` mình là thành viên
  (`solution_members` / `solution_module_members`) hoặc `project_id` mình là thành viên
  (`prospective_project_support_department_employees` + dự án của các solution mình tham gia).
- **Tầng 3 — quản lý tổ chức (tick quyền):** 4 quyền cấp dần Tổng công ty → Công ty → Phòng ban → Bộ phận,
  query theo `company_id/department_id/part_id` của issue (snapshot org người tạo).

## Quyết định chốt (theo trả lời user)
- **Tầng 3 xét org của TẤT CẢ người giữ vai trò** (không chỉ người tạo) — đúng nguyên văn Excel
  "bất kỳ ai trong các vai trò thuộc cấp mình quản lý". Vì watchers/supporters là n-n (số lượng động) nên
  KHÔNG lưu cột org trên `issues` mà dùng **bảng phụ `issue_org_units`** (issue_id, employee_id, company/department/part)
  snapshot org của 6 vai trò mỗi issue, đồng bộ khi store/update.
- Phạm vi quản lý của người xem lấy theo org bản thân + đơn vị được phân công quản lý
  (`current_company_role`, `listManageDepartmentIds()`, `listManagePartIds()`) — tái dùng helper `isCurrentEmployeeHasPermission`.
- "Tổng công ty" = xem tất cả (không giới hạn). FE bổ sung bộ lọc cascading Công ty → Phòng ban → Bộ phận
  (dùng `V2BaseCompanyDepartmentFilter`), khớp nếu bất kỳ vai trò nào thuộc đơn vị lọc.

## Cách triển khai (tham chiếu pattern `MeetingCriteria`)
1. **DB:** migration tạo bảng `issue_org_units` + backfill org từ 6 vai trò (UNION creator/assignee/approver/detected + issue_watchers + issue_supporters → join employees/employee_infos).
2. **BE store/update:** `syncIssueOrgUnits()` xoá + chèn lại org của 6 vai trò sau khi sync watchers/supporters.
3. **BE index:** OR Tầng 1 (6 vai trò) + Tầng 2 (solution/project membership) + Tầng 3 (subquery `issue_org_units` theo quyền cấp); "tổng cty" → bỏ qua scope (xem tất cả).
4. **Seeder:** thêm 4 quyền group "Quản lý issue" (ids 1099–1102).
5. **FE:** `V2BaseCompanyDepartmentFilter` (ẩn nhân viên) + auto-search deep watcher + filterStateMixin (`assign_issues`) + v2-styles (đã có).

## Tên 4 quyền (group "Quản lý issue", type 4)
- Xem danh sách issue theo tổng công ty (id 1099)
- Xem danh sách issue theo công ty (id 1100)
- Xem danh sách issue theo phòng ban (id 1101)
- Xem danh sách issue theo bộ phận (id 1102)

## Phase 2 — Task (`/assign/tasks`)
Cùng kiến trúc Issue, khác biệt:
- **5 vai trò** (Tầng 1): `created_by` (tạo), `assignee_id` (xử lý), `approver_id` (phê duyệt kết quả),
  **người duyệt triển khai** (ĐỘNG: có quyền `Duyệt task` + quản lý phòng của người xử lý — không snapshot),
  `watchers` (theo dõi).
- **Kế thừa Cha↔Con**: vai trò ở task cha → thấy mọi task con (`tasks.parent_id IN myDirectTaskIds`);
  vai trò ở task con → thấy task cha (`tasks.id IN parent_ids(myDirectTaskIds)`).
- Bảng phụ `task_org_units` (snapshot org của tạo/xử lý/phê duyệt/theo dõi). Quyền 1103–1106 group "Quản lý task".
- FE: `tasks/index.vue` đã import sẵn `V2BaseCompanyDepartmentFilter` + deep watcher; bổ sung set `permissions`, org fields, filterStateMixin (`assign_tasks`).

## Test
`hrm-api/scope_permission_test.php` — chạy trong DB transaction rồi rollback (không đụng data thật).
17 case PASS: Tầng 1/2/3 cả Issue+Task, kế thừa Cha↔Con, deployment approver, lọc org, loại trừ khác công ty, sync org_units.

## Lưu ý / điểm cần xác nhận khi verify
- Tầng 2 "thành viên dự án" suy ra từ `solution_members`/`solution_module_members` (→ project của solution) +
  `prospective_project_support_department_employees`. Nếu nghiệp vụ có nguồn thành viên dự án khác → bổ sung.
- Route `index` KHÔNG gắn middleware `checkPermission` (user chỉ có Tầng 1/2 vẫn xem được danh sách của mình).
