# Employee QTC Logic Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thiện logic nhân viên QTC: sync ngược về PCT cũ cùng hợp đồng, auto-fill từ contract ERP khi tạo PCT mới.

**Architecture:** Sửa 2 file BE trong hrm-api: (1) `AssignRequest::syncWrAssignTask()` thêm logic sync QTC qua các PCT cùng `contractable_id`+`contractable_type`, (2) `WrAssignTaskListResource::toArray()` lấy QTC từ contract ERP thay vì wr_assign_task. FE giữ nguyên.

**Tech Stack:** Laravel 8, PHP, MySQL (cross-database query via `mysql2` connection)

---

### Task 1: Sync QTC ngược lại PCT cũ cùng hợp đồng

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/AssignRequest.php:292-328`

- [ ] **Step 1: Thêm logic sync sau vòng lặp lưu assign_business_tasks**

Mở file `hrm-api/Modules/Assign/Entities/AssignRequest.php`. Tìm method `syncWrAssignTask()`, tìm đoạn đóng vòng lặp `foreach` ở dòng ~328 (dòng `}`). Thêm code **ngay sau** dòng `}` đóng foreach và **trước** dòng `}` đóng method:

```php
        // Sync employee_info_qtc_ids cho các PCT cũ cùng hợp đồng
        foreach ($data as $item) {
            $employeeInfoQtcIds = json_encode($item['employee_info_qtc_ids'] ?? []);
            $contractableId = @$item['contractable_id'];
            $contractableType = @$item['contractable_type'];

            if (!$contractableId || !$contractableType) continue;

            AssignBusinessTask::where('contractable_id', $contractableId)
                ->where('contractable_type', $contractableType)
                ->where('assign_request_id', '!=', $this->id)
                ->update(['employee_info_qtc_ids' => $employeeInfoQtcIds]);
        }
```

- [ ] **Step 2: Verify import AssignBusinessTask đã có**

Chạy:
```bash
grep -n "use.*AssignBusinessTask" hrm-api/Modules/Assign/Entities/AssignRequest.php
```

Nếu chưa có, thêm ở đầu file:
```php
use Modules\Assign\Entities\AssignBusinessTask;
```

Nhưng code hiện tại đã dùng `AssignBusinessTask` (dòng 295-301), nên import chắc chắn đã có hoặc dùng inline. Kiểm tra:
```bash
grep -n "AssignBusinessTask" hrm-api/Modules/Assign/Entities/AssignRequest.php | head -5
```

Nếu dùng inline `new AssignBusinessTask()` mà không có import, thì cần thêm. Nếu đã có import hoặc dùng full namespace → không cần thêm.

- [ ] **Step 3: Verify thủ công**

Test flow:
1. Tạo PCT A với phiếu giao việc thuộc hợp đồng X, chọn nhân viên QTC = Nguyễn Văn A
2. Tạo PCT B với phiếu giao việc cũng thuộc hợp đồng X, chọn nhân viên QTC = Nguyễn Văn B
3. Kiểm tra DB: `assign_business_tasks` của PCT A phải có `employee_info_qtc_ids` = Nguyễn Văn B (đã được sync)

---

### Task 2: Lấy QTC từ contract ERP thay vì wr_assign_task

**Files:**
- Modify: `hrm-api/Modules/Assign/Transformers/WrAssignTaskResource/WrAssignTaskListResource.php:65-70`

- [ ] **Step 1: Sửa logic lấy employee_qtc_id**

Mở file `hrm-api/Modules/Assign/Transformers/WrAssignTaskResource/WrAssignTaskListResource.php`. Tìm block dòng 65-70:

```php
            if ($assign_request->employee_qtc_id) {
                $tpEmployee = TpEmployee::query()->find($assign_request->employee_qtc_id);
                $tpEmployeeInfo = TpEmployeeInfo::query()->find($tpEmployee->employee_info_id);
                $item['employee_info_qtc_id'] = $tpEmployee->employee_info_id;
                $item['employee_info_qtc_name'] = $tpEmployeeInfo->fullname;
            }
```

Thay bằng:

```php
            $contract = null;
            if ($assign_request->contractable_type == 'firm') {
                $contract = \App\Models\TpContract::query()->find($assign_request->contractable_id);
            } elseif ($assign_request->contractable_type == 'wr') {
                $contract = \App\Models\TpWrContract::query()->find($assign_request->contractable_id);
            }
            if ($contract && $contract->employee_qtc_id) {
                $tpEmployee = TpEmployee::query()->find($contract->employee_qtc_id);
                if ($tpEmployee) {
                    $tpEmployeeInfo = TpEmployeeInfo::query()->find($tpEmployee->employee_info_id);
                    if ($tpEmployeeInfo) {
                        $item['employee_info_qtc_id'] = $tpEmployee->employee_info_id;
                        $item['employee_info_qtc_name'] = $tpEmployeeInfo->fullname;
                    }
                }
            }
```

- [ ] **Step 2: Verify thủ công**

Test flow:
1. Tạo quyết toán công cho 1 hợp đồng → ERP contract được cập nhật `employee_qtc_id`
2. Tạo PCT mới, chọn phiếu giao việc thuộc hợp đồng đó
3. Kiểm tra: nhân viên QTC tự động fill vào và không cho sửa (disabled)
4. Tạo PCT với phiếu giao việc thuộc hợp đồng chưa có QTC → cho chọn tự do
