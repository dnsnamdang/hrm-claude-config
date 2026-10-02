# Meeting — Quản lý người tham gia & Điểm danh (Redmine #10534)

## Mục tiêu
Tài liệu test case cho phần bổ sung ở màn Quản lý Meeting: quản lý danh sách người tham gia
(Thành phần Công ty / Khách hàng) và điểm danh thành viên. Không đụng code — chỉ sinh testcase.

## Scope
- Khối "Thành phần — Phía Công ty" (chọn nhân viên qua popup) + "Thành phần — Phía Khách hàng"
  (nhập tay) ở tab Thông tin — màn Tạo / Sửa / Xem chi tiết meeting.
- Tab "Điểm danh" — điểm danh từng thành viên, điều kiện hoàn thành cuộc họp.

## Quyết định
- Tách 2 file testcase (mỗi màn/chức năng một file theo skill testcase-documenter):
  - `testcase - Quản lý danh sách người tham gia.xlsx` (mới) — 38 TC.
  - `testcase - Điểm danh thành viên meeting.xlsx` (làm lại bản cũ theo chuẩn 17 cột) — 35 TC.
- Dùng engine chung `.claude/skills/testcase-documenter/assets/tc_engine.py`; generator lưu cùng folder.
- Viết bằng ngôn ngữ nghiệp vụ (không thuật ngữ code) — bộ kiểm tra thuật ngữ báo "OK - sach".

## Sự thật nghiệp vụ chốt (từ code + màn thật)
- Bắt buộc ≥1 thành viên công ty mới lưu được cuộc họp; họ tên khách mời bắt buộc; SĐT (nếu nhập)
  phải bắt đầu bằng 0 và gồm 10–12 chữ số.
- Khối Khách hàng chỉ hiện với loại họp có khách hàng ("Họp đối tác"); đổi sang loại nội bộ thì
  xoá khách mời (trừ khi kế thừa từ dự án).
- Chống trùng nhân sự công ty; chọn tất cả theo bộ lọc trên mọi trang; kéo-thả đổi thứ tự trong
  từng bảng, không kéo chéo.
- Điểm danh chỉ mở khi đang Sửa + cuộc họp "Đã chốt lịch"; hoàn thành cuộc họp cần đủ biên bản +
  điểm danh đầy đủ. Thông báo: "Vui lòng thêm biên bản cuộc họp trước khi hoàn thành!" /
  "Vui lòng hoàn thành điểm danh cho tất cả thành viên trước khi chốt biên bản và hoàn thành cuộc họp."
- Nhóm quyền "Quản lý meeting" chỉ có 4 quyền xem theo cấp (tổng công ty/công ty/phòng ban/bộ phận);
  thao tác người tham gia/điểm danh không có quyền riêng, đi kèm quyền mở màn Sửa meeting.

## Nguồn code
- FE: `pages/assign/meeting/components/GeneralInfo.vue`, `PopupStaff.vue`, `MeetingAttendance.vue`,
  `MeetingForm.vue`.
- BE: `Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php`, `MeetingUpdateApiRequest.php`;
  route `Modules/Assign/Routes/Meeting/api.php`; `PermissionsTableSeeder` (nhóm "Quản lý meeting").
