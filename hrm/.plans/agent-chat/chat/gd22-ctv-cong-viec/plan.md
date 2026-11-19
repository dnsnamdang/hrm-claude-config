# GĐ22 — Phân hệ Công việc chọn được nhân sự phòng cộng tác viên

User báo 16/11/2026 (prod): thêm thành viên nhóm chat tìm "Nguyễn Trần Đức Cư" (CTV.06, PHÒNG CỘNG TÁC VIÊN_NV, công ty 1,
đang làm, có tài khoản emp 1354) không ra; chọn qua phòng ban thì ra. User: "cần cả ở giao nhiệm vụ, meeting, vấn đề cũng chọn được"
⇒ chọn cách 1 (bỏ lọc ở store cho assign) + cách 1 cho API (tham số kem_ctv).
Nhánh `gop_db-ctv-cong-viec` (hrm-api từ 76dbd1641, hrm-client từ 8032569dc).

Gốc:
- `hrm-client/store/actions.js:81` (commit a752f8f3e "ctv" 29/04/2025): trang đầu thuộc training / assign / rice ⇒ lọc
  `cooperation_type = 2` khỏi `employees`, `list_employee_infos`, `departments` ⇒ ô chọn người nhóm chat (workspaceOptions),
  meeting (`state.employees`) không có CTV; kết quả còn tuỳ trang mở đầu tiên (/human thì có).
- `TaskController::getEmployeesByCompany` (GET assign/tasks/employees — TaskPanel + 4 màn kho) lọc CTV ở BE.
- Vấn đề (`allEmployeesOptions`) vốn lấy danh sách CHƯA lọc ⇒ đã chọn được CTV.

- [x] Tái hiện Playwright NV 24: /assign/my-todo 649 NV không có CTV; /human/banks 650 có.
- [x] client `store/actions.js`: bỏ `assign` khỏi danh sách lọc (Đào tạo, Cơm giữ).
- [x] api `getEmployeesByCompany(Request)`: `kem_ctv=1` ⇒ gồm CTV; mặc định giữ lọc (màn kho không đổi). PHPUnit `Task/TaskEmployeesCtvTest`.
- [x] client `TaskPanel.vue` gọi `assign/tasks/employees?kem_ctv=1`.
- [x] Đo lại: /assign có CTV (list, employees, issues); /training vẫn ẩn. API: 407 ⇒ 408 với kem_ctv.
- [x] e2e mới `tests/assign/ctv-cong-viec.spec.ts` 4/4 (TaskPanel Người thực hiện, meeting Người chủ trì, tạo nhóm chat Thành viên, Đào tạo vẫn ẩn).
- [x] e2e màn liên quan: chat-drawer 10/10 · chat-core 8/8 · task-panel-v2 6 pass, ca 7 FAIL (403 hiện 2 toast "Bạn không có quyền…"
      + "Không tải được chi tiết nhiệm vụ") — KHÔNG do đợt này (stub chỉ /tasks/999992, diff TaskPanel chỉ đổi URL nhân viên) ⇒ ngoài luồng;
      meeting-host 4 fail do môi trường (spec dùng .auth/user.json của origin :3000, chạy :3080 ⇒ không đăng nhập) — ô chủ trì đã phủ
      bởi ca 2 spec mới.
- [x] 16/11 commit api 879511857 · client 509532964, gop_db fast-forward, push 2 nhánh. ĐÃ DEPLOY TPE (EXIT 0, Nothing to migrate, bundle có kem_ctv=1, site 200; prod công ty 1: 409 NV đang làm, 7 ở phòng CTV).

Đi kèm (đã nêu user): phòng / nhân sự CTV hiện trong bộ lọc Phòng ban / Nhân viên ở các màn danh sách, báo cáo phân hệ Công việc.

## Ngoài luồng (ghi lại, chưa sửa)
- TaskPanel: mở nhiệm vụ trả 403 ⇒ 2 thông báo (bộ chặn chung + "Không tải được chi tiết nhiệm vụ"); e2e task-panel-v2 ca 7 đỏ trên gop_db 8032569dc.
- e2e meeting-host phụ thuộc .auth/user.json (:3000) — không chạy được trên worktree :3080.
