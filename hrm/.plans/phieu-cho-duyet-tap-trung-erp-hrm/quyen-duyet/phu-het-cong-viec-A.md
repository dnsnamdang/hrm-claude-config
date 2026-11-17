# Phủ hết màn duyệt — Công việc, fork A (Đề xuất công tác, Duyệt triển khai task, Duyệt kết quả task) — @cuong61n

17/11/2026. Definition: `hrm-api/Modules/ApprovalCenter/Definitions/Assign/{AssignRequest,TaskStartApproval,TaskResultApproval}Definition.php` (+ trait phụ `TaskApprovalSupport.php`).
Test: `hrm-api/tests/Feature/ApprovalCenter/Assign/{AssignRequest,TaskStartApproval,TaskResultApproval}DefinitionTest.php`.

| doc_type | Màn gốc (FE) | Cấp | Gate | Pending local thật | Verify | Đột biến | Trạng thái |
|---|---|---|---|---|---|---|---|
| `assign_request` | `/assign/assign_requests/{id}` (list `?type=waiting`) | 1: status 2 (type=1) "Chờ duyệt" | **BE không chốt quyền — theo điều kiện giao diện**: mã `assign.phieu_de_xuat_di_cong_tac.manage` (công ty đang làm) ∧ phiếu nằm trong danh sách chờ theo phạm vi mã Xem `assign.danh_sach_phieu_de_xuat_di_cong_tac.view` (1 bộ phận / 2 phòng QL ∪ bộ phận ∪ mình lập ∪ có tên / 3 công ty / 4 tất cả). truth() gọi `AssignRequestService::searchByFilter(type=waiting)` | 29 | 15.312 cặp (verify CLI), test 9.512 + 2.800 + … cặp, 0 chênh | 7/7 (+1 đột biến tương đương) | xong |
| `task_start_approval` | `/assign/tasks?open_task={id}` | 1: status 2 "Chờ phê duyệt triển khai" | `assign.trien_khai_task.approve` ∧ phòng người làm ∈ QL ∪ phòng mình (= `Task::canStartApprove`) ∧ `TaskAccess::assertWritable` (nhóm đóng ⇒ approvable=false) | 1 | 3.276 cặp, 0 chênh | 5/5 | xong |
| `task_result_approval` | `/assign/tasks?open_task={id}` | 1: status 6 "Hoàn thành - Chờ duyệt" | người duyệt đích danh `tasks.approver_id` (mọi công ty) ∧ assertWritable; không có approver_id ⇒ approvable=false | 4 | 4.000 cặp, 0 chênh | 4/4 | xong |

## Quyết định / điểm cần chú ý
- **Đề xuất công tác**: "Duyệt" = Lập phiếu công tác (status 2→4 do `AssignBusinessService` ghi `parent()->update()`), "Không duyệt" = `deny` (BE kiểm `assign.phieu_giao_cong_tac.approve` + quản lý phòng — KHÁC mã hiện nút). Theo phụ lục lấy điều kiện giao diện (người thấy nút Duyệt ở danh sách). Chuyển người phụ trách vá BE: `AssignRequestController::update/store` không kiểm quyền (ai cũng gọi được status_request 3/6).
- Task không có cột công ty / phòng ⇒ dòng gom lấy công ty / phòng / bộ phận của NGƯỜI LÀM. Người xin: duyệt triển khai = `created_by`, duyệt kết quả = `assignee_id`.
- Code gốc không chặn người làm = người duyệt kết quả (`excludeOwn()` false), người giao tự duyệt triển khai.
- `TaskAccess::assertWritable` luôn qua với người duyệt (họ nằm trong tầng 1 của `applyPermissionScope`) nên chỉ còn chốt "nhóm đóng"; phần này kiểm được vì đã chạy migration.

## Chỗ ghi bằng query builder đã xử lý (thêm `scheduleSync`)
- `Modules/Assign/Services/AssignBusinessService.php` (~469): `$assignRequest->parent()->update(['status' => DA_LAP_PHIEU_CONG_TAC])` ⇒ `scheduleSync('assign_request', parent_id)`.
- `Modules/Assign/Services/Workspace/WorkspaceTaskCanceller.php` (~68): huỷ hàng loạt việc khi đóng nhóm ⇒ `scheduleSync` cho việc đang ở status 2 / 6.
- Model: `AssignRequest::boot()` thêm hook `assign_request`; `Task::booted()` hook có điều kiện cho `task_start_approval` + `task_result_approval` (KHÔNG dùng trait vì Task lưu rất dày; chỉ sync khi đang / vừa rời status 2 / 6 — kiểm bằng `wasChanged('status')`).

## Migration đã chạy
`php artisan migrate --path=Modules/Assign/Database/Migrations/2026_11_14_000001_add_workspace_to_tasks.php --force` (thêm `tasks.workspace_id`, `source_message_id`) để kiểm nhánh nhóm đóng; các test "nhóm đã đóng" trước đây `skipped` nay chạy xanh.

## Lỗi code gốc phát hiện (chỉ ghi lại)
- Phiếu đề xuất công tác: update/store không kiểm quyền; nút "Không duyệt" ở màn chi tiết hiện cho mọi người mở được (`isApprove` hard-code `pages/assign/assign_requests/_id/index.vue:6`) nhưng BE `deny` đòi mã `phieu_giao_cong_tac.approve` + quản lý phòng; `deny` kiểm quyền trước khi kiểm null (500 khi sai id).
- Tab "Phiếu đề xuất công tác cần duyệt": người có `.manage` thấy MỌI phiếu trong phạm vi xem, không lọc theo phòng quản lý.

## Việc cho điều phối
- Dữ liệu thử đã dọn bằng `approval-center:clean-test --manifest=wave2-assign-A.json`.
- `approval-inbox:verify` chạy chậm khi nhiều fork cùng chạy trên DB (timeout 120s cho task_start_approval lúc cao điểm).
