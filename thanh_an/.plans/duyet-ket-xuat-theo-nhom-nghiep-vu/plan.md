# Plan — Duyệt HĐ kết xuất cung ứng theo nhóm nghiệp vụ

> @khoipv — Bắt đầu 26/10/2026

## Yêu cầu
Quyền "Duyệt hợp đồng kết xuất cung ứng" (id 525) đang duyệt **toàn hệ thống** (chỉ xét quyền).
Đổi sang xét **nhóm nghiệp vụ giống quyền "Duyệt hợp đồng"** (`Contract::canApprove()`):
có quyền **VÀ** (người lập HĐ thuộc nhóm mình quản lý `listManageEmployeeIdsByGroup()` **HOẶC** HĐ do chính mình lập).

## Phase 1 — BE
- [x] `Contract::canApproveRenderSupply()` — thêm điều kiện nhóm như `canApprove()` (từ chối dùng chung hàm → tự áp dụng; guard server `approveRenderSupply/rejectRenderSupply` gọi accessor nên chặn luôn API)
- [x] `ContractService::notifyRenderSupplyApprovers()` — chỉ báo quản lý nhóm của người gửi có quyền 525 (`listEmployeeInfoHasPermission(..., auth employee_info_id)`, giống `sendNotification()` lúc gửi duyệt HĐ)
- [x] `php -l` sạch + script kiểm tra (chỉ gán status trong bộ nhớ, không ghi DB): DB local chỉ có NV 13 giữ quyền 525 (quản lý nhóm 4, 18, 21) → 60 HĐ gần nhất: 20 HĐ do NV 13 lập duyệt được, 40 HĐ người khác lập (ngoài nhóm) bị chặn (trước đây duyệt được cả 60), 0 ca lệch so với luật. Chưa có dữ liệu ca "quản lý nhóm duyệt HĐ của thành viên" → user test trên dev.

### Checkpoint — 26/10/2026
Vừa hoàn thành: sửa BE accessor + thông báo, verify bằng script
Đang làm dở:
Bước tiếp theo: user test trên dev (quản lý nhóm có quyền 525 duyệt HĐ của thành viên; người có quyền ngoài nhóm không thấy nút duyệt)
Blocked:

## Phase 2 — FE
- [x] Không cần sửa: `approve-render-supply.vue` + `render.vue` đọc cờ `can_approve_render_supply` từ API
