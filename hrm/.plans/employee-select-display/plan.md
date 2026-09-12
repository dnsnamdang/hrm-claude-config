# Plan — Đồng bộ hiển thị option NHÂN VIÊN trong mọi select V2Base

Nhánh: `tpe` (FE `worktrees/tpe-client` :3005 · BE `worktrees/tpe-api` :8005) — @namdangit

Chuẩn chốt 2026-09-11: **`Tên nhân viên - Mã phòng - Mã nhân viên`**
(vd `Nguyễn Thị Cần - HN_KD1 - 11010057`). Thiếu phần nào thì bỏ phần đó.

## BE (hrm-api)
- [x] `Modules/Timesheet/Entities/Employee.php::getAll()` — thêm cột `employee_infos.fullname as fullname` (giữ nguyên `name` ghép sẵn để không vỡ các màn đang hiển thị)
- [x] `AuthNewController::userProfile()` — `list_employee_infos` thêm `departments.code as department_code`

## FE (hrm-client)
- [x] Thêm `utils/employeeOptionText.js` — helper dùng chung (`employeeOptionText`, `employeeFullName`)
- [x] `store/actions.js` — áp helper cho 6 key option: `allEmployeesOptions`, `employeeOptions`, `employeeInfoOptions`, `activeCompanyEmployeeOptions`, `currentEmployeeCompany`, `allEmployeesData`
- [x] `components/V2BaseCompanyDepartmentFilter.vue` + `components/CompanyDepartmentFilterModal.vue` — ô "Nhân viên"
- [x] 21 màn tự dựng option nhân viên từ `state.employees` / `state.list_employee_infos` (assign, timesheet, decision, training report, CompanyForm, StudentModal)

## Vòng 2 — quét nốt các màn lấy nhân viên từ API riêng
- [x] BE `EmployeeInfoController::getEmptyInfos()` + `listForSelect()` — trả thêm `department_code` (subselect, vì nhánh `is_not_cooperation_operation` đã join sẵn `departments`)
- [x] BE `TerminationLaborContractController::employeeOptions()` — thêm `department_code`
- [x] BE `Decision/.../StudentResource` — thêm `department_code`
- [x] BE `CapacityEvaluatePlanningService` (2 query) + `DetailEmployeeByCapacityResource` — thêm `department_code`
- [x] FE: 56 file còn ghép tay (`fullname + '-' + code`, `code + '_' + fullname`, `code + ' - ' + fullname`) → dùng helper

## Đã test (Playwright, 2026-09-11)
- [x] `/assign/meeting` — ô "Nhân viên" và "Người cập nhật gần nhất" ra cùng khuôn; chọn xong ô hiển thị cũng đúng khuôn
- [x] 6 key option trong store đều đúng khuôn
- [x] `/timesheet/attendance`, `/assign/extend-end-soon-request`, `/assign/job_requests`, `/training/courses` — đúng khuôn
- [x] 3 endpoint kiểm trực tiếp (`getEmptyInfos`, `list-for-select`, `employee-options`) đều trả `department_code`
- [x] Case biên của helper: thiếu phòng ban → `Tên - Mã NV`; thiếu mã NV → `Tên - Mã phòng`; rỗng/null → chuỗi rỗng
- [x] Build sạch (không còn lỗi webpack), lỗi console còn lại là cảnh báo Vue có sẵn của từng màn

## Chưa làm
- [ ] Các "picker" bảng chọn nhân viên (SalesTeam/Solution/SupportDepartment/CreateTaskModal…) đã tách sẵn cột Tên / Mã / Phòng → giữ nguyên
- [ ] Cột hiển thị tên nhân viên trong BẢNG và bản in (`employees[].name` vẫn là `"Mã phòng - Tên"`) → chưa đổi, chỉ đổi phần option select

## Vòng 3 — rà triệt để MỌI select nhân viên (không để sót)
- [x] Viết script audit: quét 163 file có `V2BaseSelect*` + 365 file có `Select2` cũ → truy nguồn dựng `text/name/label`
- [x] BE thêm `department_code`: `getEmployeesForFilter`, `agent-employees` (ERP), `ViolatorResource`, `SolutionService` (4 nhánh nhân sự), `SolutionModuleService` (2 nhánh, thêm cả `employee_code`)
- [x] BE thêm helper chung `employeeOptionLabel()` trong `app/Helper/FormatHelper.php` (dùng khi BE tự dựng label)
- [x] BE áp helper: `HandoverService` (3 chỗ, kèm eager load `department` tránh N+1), `BulkPermissionService`
- [x] FE sửa 13 chỗ còn lệch: quotations (Người duyệt), shift-history (2 ô), ProgressTab, CustomerForm + Quotations/ContractsTab, SolutionApprovalModal, ModuleApprovalModal, training-organization-situation, employee-discipline, department-change, bonus-distribution, 5 modal select2 cũ (department/part/group/truncated-leave/add-user-to-conn-info)
- [x] Audit lại: 0 chỗ sai ở Select2 cũ; 4 cảnh báo còn lại ở V2BaseSelect đều là dương tính giả (bảng nhân sự, chi nhánh ngân hàng, danh sách vai trò, nhãn BE đã chuẩn)

## Ghi lại quy ước cho màn mới
- [x] `.claude/skills/select-and-input-state/SKILL.md` mục 2c — viết lại đầy đủ: 3 quy tắc bắt buộc, 4 bẫy đã trả giá, 2 lệnh tự kiểm; thêm 1 dòng vào checklist cuối skill
- [x] `CLAUDE.md` — thêm gạch đầu dòng nguyên tắc (dòng 71)

## Lỗi thật phát hiện khi rà
- Màn Báo giá: ô lọc **Người duyệt** trước đó RỖNG (map `e.fullname || e.label || e.name` trong khi store chỉ có `{id, text}` → `label` rỗng → bị `.filter()` loại sạch). Sau khi sửa: 629 option.

## Chưa làm
- [ ] Các "picker" bảng chọn nhân viên (SearchPicker) đã tách sẵn cột Tên / Mã / Phòng → giữ nguyên
- [ ] Cột tên nhân viên trong BẢNG và bản in (`employees[].name` vẫn `"Mã phòng - Tên"`) — chỉ đổi option select
- [ ] `decision-reward/get-employee-reward` là code chết (hardcode tháng 5/2024, FE đã comment) → không sửa

### Checkpoint — 2026-09-11
Vừa hoàn thành: vòng 3 — rà triệt để mọi select nhân viên + ghi quy ước vào skill/CLAUDE.md
Đang làm dở: không
Bước tiếp theo: user review, quyết có đổi luôn cách hiển thị tên nhân viên trong bảng/bản in không
Blocked:
