# Fix — Phiếu đăng ký làm thêm lưu sai phòng ban (lệch công ty)

## Bối cảnh
- Màn `/timesheet/overtime-assignment/approve`: phiếu 4412 (Đặng Khắc Quang, NV cty4 phòng Logistic SG-92) lại hiện phòng "Nhân sự hành chính" (dept 43, thuộc cty1) → tưởng phiếu công ty khác.
- Gốc rễ 2 khiếm khuyết:
  1. FE `components/modals/AddDepartment.vue` gọi `department/` (DepartmentService::index) KHÔNG lọc company_id → liệt kê phòng mọi công ty → chọn nhầm phòng cty khác.
  2. BE `OvertimeAssignmentService::save()` ép `company_id = current_company_role` nhưng KHÔNG ép `department_id` → lưu lệch.
- Quy mô: 267 phiếu lệch (265 sửa được bằng phòng thật của NV, 2 phiếu NV không có phòng).
- Quy tắc đúng đã verify: `department_id` = `employee_infos.department_id` của nhân viên trên phiếu → 265/267 về đúng company_id.

## Phase 1 — BE
- [x] `DepartmentService::index()`: thêm filter `company_id` (chỉ khi request truyền) — không đổi hành vi mặc định.
- [x] `OvertimeAssignmentService::save()`: guard — nếu `department_id` rỗng hoặc thuộc công ty khác `current_company_role` thì đặt lại = phòng thật của `employee_id`. Không đụng khi update trạng thái (không có employee_id trong payload).

## Phase 2 — FE
- [x] `components/modals/AddDepartment.vue`: thêm prop `companyId` (opt-in); nếu có thì nối `&company_id=` vào API. Mặc định giữ nguyên (11 màn dùng chung).
- [x] `overtime-assignment/add.vue` (+ `_id/index.vue`, `_id/approve.vue`): truyền `:company-id` = công ty người tạo vào `<AddDepartment>`.

## Phase 3 — Dữ liệu cũ
- [x] Seeder `FixOvertimeAssignmentDepartmentSeeder` (1 UPDATE JOIN) đặt lại `department_id` = phòng thật NV cho các phiếu lệch (dept.company_id != oa.company_id) và NV có phòng. Bỏ qua 2 phiếu NV null phòng. (Đã chạy: 265 phiếu; seeder idempotent chạy lại = 0.)

## Verify
- [x] Tạo phiếu đăng ký làm thêm mới (guard BE test: FE gửi dept 43 → lưu 92): modal chỉ hiện phòng công ty hiện tại; phiếu lưu department_id đúng công ty.
- [x] Chạy command: 265 phiếu về đúng phòng; phiếu 4412 → dept 92 (Logistic SG).
- [x] Màn approve không còn phiếu hiện phòng công ty khác.
