# Định nghĩa loại phiếu — Công việc, phần C (công tác) — @cuong61n

Ngày 16/11/2026. Definition: `hrm-api/Modules/ApprovalCenter/Definitions/Assign/`; test: `hrm-api/tests/Feature/ApprovalCenter/Assign/`.

| doc_type | Màn gốc | Cấp | Gate | Pending local | Verify | Đột biến | Trạng thái |
|---|---|---|---|---|---|---|---|
| `assign_business` | `/assign/assign_business?type=waiting` → `/{id}/approve` | 1 (status 2, type 2) | `assign.phieu_giao_cong_tac.approve` + department_id ∈ manageDepartmentIdsOf (chặt) = `canApproveAssignBusiness()` | 71 | 39.963 cặp, 0 chênh | 6/6 (+ trait 2/2) | xong |
| `assign_business_result` | `/assign/assign_business/{id}/approve_result` | 1 (status 5) | `assign.ket_qua_cong_tac.approve` + quản lý phòng chặt = `canApproveResultAssignBusiness()` | 0 | 3.114 cặp (6 phiếu seed), 0 chênh | 4/4 (+ trait) | xong |
| `extend_end_soon_request` | `/assign/extend-end-soon-request/{id}/show` | 1 (status 2) | chỉ mã `assign.phieu_giao_cong_tac.approve` (BE không kiểm phòng/công ty) = `canApprove()` | 94 | 51.900 cặp, 0 chênh | 4/4 | xong |
| Đề xuất công tác (type=1) | `/assign/assign_requests/{id}` | — | — | 29 | — | — | BỎ |

Đề xuất công tác bị bỏ: FE (`AssignRequestForm.vue:983-995`) chỉ có "Không duyệt" và "Lập phiếu công tác" (đi sang tạo chứng từ kế tiếp); không có thao tác "Duyệt" độc lập.

Ghi chú: status 1 "Đang tạo" của phiếu công tác không phải chờ duyệt (người lập tự "Lưu và duyệt"). Duyệt kết quả chỉ có "Duyệt", không có "Không duyệt" ⇒ rời hàng chờ duy nhất khi duyệt. Trùng lịch (424) và ERP dueConfig chỉ ghi ở gate_blocker (phụ thuộc phiếu khác, không tính được độc lập). Chữ/màu trạng thái do FE map (BE không có accessor) ⇒ Definition tự đặt "Chờ duyệt"/"Chờ duyệt kết quả" #D97706.

Đồng bộ: AssignRequest gắn trait (`assign_business`) + hook `saved/deleted` thêm cho `assign_business_result` (trong `boot()`); ExtendEndSoonRequest gắn trait. Không có chỗ nào ghi `status` bằng query builder; chỉ `AssignBusinessService.php:469` `$assignRequest->parent()->update(['status'=>4])` (relation update, không phát event) nhưng chỉ chạm phiếu đề xuất type=1 (đã bỏ) nên không cần sync.

Lỗi code gốc: `AssignBusinessController::deny` gọi `canApproveAssignBusiness()` trước khi kiểm `null` (500 khi id sai); extend-end-soon approve/reject không kiểm phòng/công ty; `approver_id` của extend_end_soon không được ghi; URL thông báo extend dùng `/extend_end_soon_request/` (sai so với route FE `/extend-end-soon-request/`).
