# Sửa logic nhân viên QTC

## Mục tiêu

Hoàn thiện 3 luồng logic nhân viên QTC trong phiếu công tác (PCT) và quyết toán công.

## Scope

- BE: `hrm-api` — AssignRequest entity, WrAssignTaskListResource
- FE: `hrm-client` — giữ nguyên (logic auto-fill + disable đã có)
- Không sửa ERP

## Luồng 1: Sync QTC ngược lại PCT cũ cùng hợp đồng

**Trigger**: Khi tạo/sửa phiếu công tác, lưu `employee_info_qtc_ids` cho `assign_business_tasks`.

**Logic cần thêm** (trong `AssignRequest::syncWrAssignTask()` sau khi lưu xong):
1. Với mỗi `assign_business_task` vừa lưu, lấy `contractable_id` + `contractable_type`
2. Tìm tất cả `assign_business_tasks` khác có cùng `contractable_id` + `contractable_type` (khác `assign_request_id` hiện tại)
3. Cập nhật `employee_info_qtc_ids` của chúng giống giá trị vừa lưu

**Bảng**: `assign_business_tasks`
- `assign_request_id` — FK tới phiếu công tác
- `jobinvoiceable_id` — FK tới wr_assign_task
- `jobinvoiceable_type` — loại (TpWrAssignTask)
- `employee_info_qtc_ids` — JSON array `[{id, text}]`

**Lưu ý**: Cần lấy `contractable_id`, `contractable_type` từ bản ghi `TpWrAssignTask` bên ERP (qua `jobinvoiceable_id`).

## Luồng 2: Auto-fill QTC từ hợp đồng ERP khi tạo PCT mới

**Trigger**: Khi FE gọi API lấy danh sách phiếu giao việc (WrAssignTask) để chọn.

**Sửa `WrAssignTaskListResource::toArray()`** (dòng 65-70):
- Thay vì check `$assign_request->employee_qtc_id` (trên wr_assign_task)
- Lấy contract từ `contractable_id` + `contractable_type`:
  - Nếu `contractable_type` chứa `FirmContract` → query `TpContract::find(contractable_id)`
  - Nếu `contractable_type` chứa `WrServiceContract` → query `TpWrContract::find(contractable_id)`
- Nếu contract có `employee_qtc_id` → trả `employee_info_qtc_id` + `employee_info_qtc_name`
- FE auto-fill và disable — logic đã có sẵn trong HandleMixin (dòng 453-458, 728)

## Luồng 3: Cập nhật QTC về ERP khi quyết toán công

**Giữ nguyên** `SettlementContractService::syncEmployeeQtcContractErp()` — logic đã đúng:
- Lấy user đang tạo phiếu quyết toán
- Map sang `tp_employees.id`
- Cập nhật `employee_qtc_id` + `department_qtc_id` về contract ERP (hỗ trợ cả `wr` và `firm`)

## Files ảnh hưởng

| File | Thay đổi |
|------|----------|
| `hrm-api/Modules/Assign/Entities/AssignRequest.php` | Thêm logic sync QTC ngược trong `syncWrAssignTask()` |
| `hrm-api/Modules/Assign/Transformers/WrAssignTaskResource/WrAssignTaskListResource.php` | Sửa lấy QTC từ contract thay vì wr_assign_task |
| `hrm-api/Modules/Assign/Services/SettlementContractService.php` | Giữ nguyên |
| FE (HandleMixin.js, AssignBusinessForm.vue) | Giữ nguyên |
