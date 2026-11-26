# Tra cứu quyền duyệt / hủy duyệt yêu cầu lắp đặt bàn giao (YCLD 893) — @cuong61n

Yêu cầu (chat, 26/11/2026): người dùng hỏi cần quyền gì để Duyệt / Không duyệt phiếu
`erp.eteksofts.com/admin/customer-care/assembly_requests/893/show`. Chỉ điều tra, không sửa code.

## Task

- [x] 26/11/2026 — Lần code ERP (nhánh `gop_db`, đối chiếu prod cùng nội dung):
  - Route `assemblyRequest.approve` / `unApprove` không gắn `checkPermission`; quyền kiểm trong Entity
    `AssemblyRequest::canApprove()` và `canAssignTask()` (`app/Model/Customers/AssemblyRequest.php`).
  - **Duyệt** (`canApprove`): có mã `customer_care.phieu_yeu_cau_lap_dat_ban_giao_truong_phong.approve`
    ("Trưởng phòng duyệt yêu cầu lắp đặt, bàn giao") **và** phiếu ở trạng thái Chờ TP duyệt (6).
    Route approve còn gắn middleware `checkDueConfigsManager:Duyệt yêu cầu lắp đặt bàn giao` (chặn nếu
    phòng do TP quản lý có NV quá hạn).
  - **Không duyệt** (`unApprove`): qua được khi `canApprove()` HOẶC `canAssignTask()`. `canAssignTask`
    = phiếu Chờ giao việc (1) + còn dòng need=1 có SL chưa giao + **phòng ban của người bấm trùng
    phòng tiếp nhận** (`department_reception_id`), không cần mã quyền nào.
  - Nút trên form.blade: khối Duyệt/Không duyệt hiện theo `canApprove()`; khối Chuyển phòng tiếp
    nhận / Không duyệt / Tạo phiếu giao việc hiện theo `canAssignTask()`.
- [x] 26/11/2026 — Đối chiếu prod DB `hrm_erp_gop`: phiếu 893 `TPE.YCLDBG.2026000893`, status = 1
    (Chờ giao việc, tức TP đã duyệt), phòng lập 103 (KD TB&VL công nghiệp), phòng tiếp nhận 51
    (PHÒNG KỸ THUẬT CÔNG NGHỆ), 3 dòng need=1 assign_qty=0, chưa có phiếu giao việc.
    → Nút "Duyệt" không còn áp dụng; "Không duyệt" chỉ hiện với người thuộc phòng 51.
    Mã quyền 100982 đang nằm trong 33 vai trò (TPE_Super Admin, TPE_Trưởng phòng kinh doanh,
    TPE_Tiếp nhận yc SC - Lắp đặt - Duyệt kết quả, …), không cấp trực tiếp cho nhân viên nào.
- [x] 26/11/2026 — Trả lời trong chat. Trạng thái: xong, không có code thay đổi.
- [x] 26/11/2026 — Hỏi tiếp: "Chờ giao việc rồi thì quyền gì để hủy?" → Không cần mã quyền; chỉ
    người thuộc phòng tiếp nhận (phòng 51) bấm "Không duyệt" (status → 4 Từ chối, nhập lý do). Xoá
    chỉ cho người tạo khi phiếu Đang tạo / Từ chối (`canEdit`). Đã trả lời trong chat.
- [x] 26/11/2026 — Hỏi tiếp: "đang là phòng tiếp nhận mà không có nút". Tra prod: tài khoản trong ảnh
    là Nguyễn Phú Cường (id 485, welding@tanphat.com) thuộc phòng 103 (phòng LẬP), không phải phòng
    tiếp nhận 51; Đào Thị Thúy (id 34) thuộc phòng 36. Code so `info->department_id` của người đăng
    nhập với `department_reception_id` của phiếu (EmployeeInfo ERP không ghi đè department_id). Hướng
    xử lý: người phòng 51 bấm Không duyệt hoặc Chuyển phòng tiếp nhận. Đã trả lời trong chat.
