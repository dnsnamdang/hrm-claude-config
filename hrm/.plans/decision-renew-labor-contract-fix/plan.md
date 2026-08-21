# Plan — Fix QĐ ký hợp đồng lao động (renew-labor-contract), tab Thông tin tiếp nhận

Phụ trách: @namdangit — Redmine #10815 (phản hồi test)
Branch: `tpe-develop-assign` (cả hrm-api + hrm-client)

## Bug ghi nhận
1. "Người quản lý trực tiếp" chỉ liệt kê NV trong phòng ban của người được ký HĐLĐ → phải giống QĐ tiếp nhận nhân sự (không giới hạn phòng ban).
2. "Số HĐLĐ gần nhất" hiển thị sai — đang lấy HĐ đầu tiên được lập. Đúng: có HĐ đang hiệu lực thì lấy HĐ đó, không có thì lấy HĐ đã hết hiệu lực có ngày hết hạn gần nhất.

## Phase 1 — Fix

### FE (`pages/decision/renew-labor-contract/components/FormComponent.vue`)
- [x] `getEmployeeInfo`: bỏ tham số `department_id`, đổi sang `except_employee_info_id` (dùng `buildQuery`) — đồng bộ QĐ tiếp nhận nhân sự
- [x] `setEmployeeInfo`: gọi `getEmployeeInfo(employeeInfo.id)` thay vì truyền `renew_department_id`; thêm guard `!employeeInfo` tránh crash khi không tìm thấy NV

### BE
- [x] `DecisionLaborContract::pickLatestFromCollection()` (mới): chọn HĐ đang hiệu lực (đã duyệt + start_date ≤ hôm nay + end_date ≥ hôm nay/NULL, ưu tiên start_date mới nhất); không có thì lấy HĐ hết hạn có end_date gần nhất. Đọc status bằng `getRawOriginal` vì accessor đổi 2 → 3/4 theo ngày
- [x] `Transformers/RenewLaborContract/EmployeeInfoResource`: thay `sortByDesc('updated_at')->first()` bằng helper trên (áp dụng cho `decision_labor_contract_code/id` + `enter_date_to`)
- [ ] Test lại trên UI (chờ user xác nhận có cần verify không)

## Phase 2 — Bắt buộc nhập "Đến ngày" theo cấu hình loại HĐLĐ

Cấu hình: danh mục `/human/labor-contract` → modal loại HĐ → checkbox `Bắt buộc nhập "Đến ngày" ở quá trình công tác`
(cột `labor_contracts.is_required_to_date`, trước đây chỉ dùng ở quá trình công tác trong hồ sơ NV).

### BE
- [x] `AcceptPersonnelService::getLaborContracts`: select thêm `is_required_to_date` (endpoint dùng chung cho cả 3 màn)
- [x] `AcceptPersonnelRequest`: `enter_date_to` required khi `LaborContract::isRequiredToDate(labor_contract_id)`
- [x] `RenewLaborContractRequest`: `renew_date_to` required theo cùng điều kiện
- [ ] QĐ HĐLĐ (`DecisionLaborContractController::store/update`) dùng `Request` thuần, chưa có FormRequest → chưa validate BE (FE-only)

### FE
- [x] QĐ ký HĐLĐ: `renew-labor-contract/components/FormDecisionComponent.vue` sync cờ `is_required_to_date` vào formSubmit (watch `labor_contract_id` + sau khi load options + khi chọn); `FormComponent.vue` computed `isRequiredToDate` → "Thời gian gia hạn đến" required + dấu `<Required />`
- [x] QĐ tiếp nhận nhân sự: cùng cơ chế → "Thời gian tiếp nhận đến" required **theo cờ** (trước đây required cứng)
- [x] QĐ HĐLĐ: `labor-contract/components/FormDecisionComponent.vue` computed `isRequiredToDate` (tự tra trong laborContractOptions) → "Thời gian hợp đồng đến" required
- [x] QĐ HĐLĐ: áp dụng cả khi Loại HĐ được fill từ "Số quyết định tiếp nhận/ký HĐLĐ" (`decision_relation_id`) — bỏ điều kiện loại trừ ban đầu

### Checkpoint — 2026-08-10
Vừa hoàn thành: fix 2 bug FE + BE nêu trên.
Đang làm dở: chưa test UI.
Bước tiếp theo: user build FE + test màn /decision/renew-labor-contract/add.
Blocked:
