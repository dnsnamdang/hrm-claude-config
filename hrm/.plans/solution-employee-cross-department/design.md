# Design — Mở rộng PM/Leader/Member toàn công ty (luồng Giải pháp)

**Spec đầy đủ**: `docs/superpowers/specs/2026-05-20-solution-employee-cross-department-design.md`

## Mục tiêu

Dropdown PM, Leader hạng mục, Member ở 2 luồng "Giải pháp" và "Tiếp nhận yêu cầu làm giải pháp" hiện chỉ hiển thị nhân sự cùng phòng tiếp nhận → mở rộng thành **toàn bộ nhân sự đang làm việc của công ty hiện tại**.

## Quyết định chính

- **Phạm vi**: toàn công ty hiện tại + `status == 1` (đang làm việc)
- **Hiển thị**: giữ `code - fullname` (không thêm tên phòng)
- **Đồng bộ**: áp dụng luôn cho modal "Tiếp nhận yêu cầu giải pháp"
- **Phân quyền BE**: leader/member phòng khác vẫn xem được solution mình tham gia

## Scope thay đổi

**FE — 4 file**:
- `store/actions.js` (thêm `company_id`, `status` vào `employeeOptions`)
- `utils/...` (helper mới `getCompanyActiveEmployeeOptions`)
- `pages/assign/solutions/components/SolutionForm.vue`
- `pages/assign/solutions/components/ModulesTab.vue`
- `components/assign-components/RequestSolutionReceiveModal.vue`

**BE — 1 file**:
- `Modules/Assign/Services/SolutionService.php` (mở rộng `checkPermissionList` cho `index/getList/getDetail` với OR clauses pm/leader/member)

**KHÔNG đụng**: `SolutionRequest` validation, `storeSolution()`, `RequestSolutionService::receive`, notifications, báo cáo.

## Risk chính

- Cần verify `company_id` và `status` có sẵn trên payload `/users/auth/user-profile` (`list_employee_infos`). Nếu thiếu → bổ sung transformer BE.
- Performance của `pluck('id')` khi dataset lớn — fallback subquery nếu cần.

## Liên quan

- `optimize-getall-manager-context` (đã hoàn thành 2026-05-11): cùng pattern mở rộng dropdown sang phòng khác qua truyền id.
