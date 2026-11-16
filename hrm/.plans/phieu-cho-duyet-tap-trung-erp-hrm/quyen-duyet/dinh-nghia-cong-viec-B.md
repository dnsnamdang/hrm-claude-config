# Định nghĩa loại phiếu — Công việc phần B (Đề xuất CV, Giao việc, Kết quả giao việc, Bàn giao) — @cuong61n

16/11/2026. Definition: `hrm-api/Modules/ApprovalCenter/Definitions/Assign/{JobRequest,AssignJob,AssignJobResult,Handover}Definition.php`. Test: `hrm-api/tests/Feature/ApprovalCenter/Assign/{JobRequest,AssignJob,Handover}DefinitionTest.php` + `Concerns/PhaseBTestHelpers.php`.

| doc_type | Màn gốc | Cấp | Gate | Truth |
|---|---|---|---|---|
| job_request | `/assign/job_requests/{id}/approve` | status 2 Chờ duyệt (pha 3 Chờ giao việc BỎ: giao việc = lập phiếu công tác/giao việc kế tiếp) | `assign.phieu_de_xuat_cong_viec.approve` + `department_request_id` ∈ quản lý chặt | `JobRequest::canApprove()` |
| assign_job | `/assign/assign_jobs/{id}/approve` | status 2 | `assign.phieu_giao_cong_viec.approve` + `department_id` (phòng người lập) ∈ quản lý chặt | status=2 ∧ `AssignJob::canApprove()` |
| assign_job_result | `/assign/assign_jobs/{id}/approve_result` | status 5 (không có Từ chối kết quả trên FE) | `assign.ket_qua_cong_viec.approve` + `department_id` ∈ quản lý chặt | status=5 ∧ `canApproveResult()` |
| handover | `/assign/handover/{id}` | status 2 | `assign.ban_giao_cong_viec.approve` + `department_id` ∈ quản lý ∪ phòng mình | `HandoverService::pending()` chứa phiếu |

## Lỗi / lệch của code gốc (chỉ ghi lại)
- AssignJob: `update` (status_request=3), `approveResult`, `deny` KHÔNG gọi canApprove()/canApproveResult(); `deny` không kiểm status (từ chối được cả phiếu status 5). Nút ở form FE chỉ kiểm mã quyền + status (không phòng); cờ có phòng chỉ nằm ở Resource danh sách (`canApprove`) mà index.vue không dùng. Inbox bám ý đồ Entity.
- Handover: endpoint approve/reject chỉ `checkPermission` + status 2, không kiểm phòng; nút Duyệt ở chi tiết chỉ kiểm mã + status; chỉ màn `/assign/handover/pending` lọc quản lý ∪ own. Inbox bám màn pending.
- JobRequest: `store` với status_request=3 không gọi canApprove (đã có trong báo cáo 02).
- Chữ trạng thái job_requests/assign_jobs do FE map, không có accessor BE → Definition hard-code chữ + `#D97706`.
- Trait chung đã bị đột biến đồng thời bởi nhiều fork: đã thấy `approval-inbox:verify` báo 177 chênh lệch giả do assignees sync lúc trait bị đột biến; `approval-inbox:backfill <doc_type>` rồi verify lại thì 0.

## Ghi `->update()` / query builder
Rà các nguồn ghi vào job_requests / assign_jobs / handovers: toàn Eloquent (`save()`, `$model->update()`, `JobRequest::find()->update()` ở AssignRequest.php:429) → trait tự sync. Không cần `scheduleSync` tường minh. `AssignJob` khai thêm `booted()` để sync loại `assign_job_result` (trait chỉ khai 1 doc_type).
