# Meeting — Quản lý danh sách người tham gia & Điểm danh (Redmine #10534) — @junfoke

> Tài liệu test case cho phần bổ sung ở màn Quản lý Meeting: quản lý danh sách người tham gia
> (Thành phần Công ty / Khách hàng) và điểm danh thành viên. Yêu cầu Redmine #10534 (TPE Lệ:
> "Nhờ DND update testcase").

## Phạm vi
- **File 1** `testcase - Quản lý danh sách người tham gia.xlsx` — MỚI.
- **File 2** `testcase - Điểm danh thành viên meeting.xlsx` — làm lại từ `meeting-diem-danh/testcase-diem-danh.xlsx`
  (format cũ 15 cột + đầy thuật ngữ code) sang chuẩn team hiện tại (17 cột, 2 khối summary DNS/TP,
  ngôn ngữ nghiệp vụ, dùng `tc_engine`).

## Nguồn đối chiếu
- Code FE: `pages/assign/meeting/components/GeneralInfo.vue` (khối Thành phần), `PopupStaff.vue`
  (popup chọn nhân viên), `MeetingAttendance.vue` (điểm danh), `MeetingForm.vue` (guard Hoàn thành).
- Validate BE: `Modules/Assign/Http/Requests/Meeting/MeetingCreate/UpdateApiRequest.php`
  (company_members required, tên bắt buộc, SĐT định dạng 0 + 9–11 số).
- Quyền: `PermissionsTableSeeder` nhóm "Quản lý meeting" (4 quyền xem theo cấp tổ chức); route CRUD
  meeting chỉ chặn đăng nhập, không có quyền riêng cho thao tác người tham gia.
- Nhãn thật đã xác nhận trên cổng dev bằng Playwright (popup, nút, tab, thông báo).

## Tasks
- [x] Đọc issue #10534 + tài liệu, khảo sát code người tham gia + điểm danh
- [x] Xác nhận nhãn thật trên màn create meeting + popup (Playwright)
- [x] Viết generator + sinh `testcase - Quản lý danh sách người tham gia.xlsx`
- [x] Viết generator + sinh lại `testcase - Điểm danh thành viên meeting.xlsx` theo chuẩn mới
- [x] Chạy bộ kiểm tra thuật ngữ ("OK - sach") + kiểm P0 ≥ 40%

### Checkpoint — 2026-09-04
Vừa hoàn thành: Sinh 2 file testcase (người tham gia + điểm danh) theo `tc_engine`, ngôn ngữ nghiệp vụ.
Đang làm dở: —
Bước tiếp theo: Gửi QA / gắn vào Redmine #10534.
Blocked:
