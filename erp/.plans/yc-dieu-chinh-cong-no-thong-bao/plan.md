# YC điều chỉnh công nợ: báo người tạo khi kế toán duyệt / từ chối — plan

Báo 27/11/2026 (dev-erp): kế toán duyệt / không duyệt phiếu yêu cầu điều chỉnh công nợ → người tạo không nhận thông báo.

## Nguyên nhân (đọc code develop_02)
- Không duyệt: `BillAdjustDeptRequestController::changeStatus()` (status 6) chỉ lưu status + `note_reject`, không gửi thông báo.
- Duyệt: KT "Tạo phiếu kế toán" (YC → 3) rồi duyệt PKT → `BillAdjustDept::processApproved()` → `updateStatus()` đặt YC = 4
  "Đã duyệt phiếu kế toán", cũng không gửi. (Cùng hàm đã báo người tạo cho YC hạch toán bổ sung — bám pattern đó.)
- Chỉ có thông báo chiều gửi duyệt (store/update → quyền `finance.ke_toan_thanh_toan.manage`).

## Tasks
- [x] `changeStatus()`: status = 6 → `NotificationHelper::sendNotify(created_by, link show, "<KT> đã từ chối phiếu yêu cầu điều chỉnh công nợ: <b>mã</b>. Lý do: …")`
- [x] `BillAdjustDept::processApproved()`: có `bill_adjust_dept_request_id` → báo người tạo YC "<KT> đã duyệt phiếu yêu cầu điều chỉnh công nợ: <b>mã</b>"
- [ ] Kiểm màn thật (dev-erp)
- [x] Commit/push develop_02 `0e53c874ea` + gop_db `9fd91fa914` (27/11/2026)

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Thông báo khi `changeStatus` status 6 + `processApproved` ✓push develop_02 `0e53c874ea` + gop_db `9fd91fa914`.
Đang làm dở: Kiểm màn thật (dev-erp).
Bước tiếp theo: Chờ user trả lời: có thông báo cả khi tạo chứng từ hạch toán và khi hủy không.
Blocked: Chờ trả lời user
