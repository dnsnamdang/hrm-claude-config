# Tạo tài khoản Dns Tester trên cổng hrm.eteksofts.com — @khoipv

Yêu cầu (18/11/2026): tạo nhân viên **Dns Tester**, email đăng nhập `dnstester@gmail.com`, mật khẩu ban đầu do user chốt;
các thông tin khác sao chép từ nhân viên **Nguyễn Đăng Nam**; cấp quyền giống hệt tài khoản Nguyễn Đăng Nam.
Không sửa code — thao tác dữ liệu trên cổng qua giao diện/API bằng tài khoản namdangit@gmail.com.

## Tasks
- [x] Xác nhận cổng là production + chốt mật khẩu ban đầu với user
- [x] Đăng nhập cổng (tài khoản namdangit sai mật khẩu trên production → dùng tài khoản quang.khoi.589 của user),
      đọc hồ sơ + vai trò/quyền của Nguyễn Đăng Nam. Có 2 tài khoản trùng tên → user chốt nguồn là **DNS NamDang (employee id 13, namdangit@gmail.com)**,
      không phải "Nguyễn Đăng Nam" id 1117 (namnd.ldhn@tanphat.com, không có vai trò)
- [x] Tạo nhân viên Dns Tester qua `POST human/employee-infos` (sao chép hồ sơ id 6, đổi tên + email; mã NV + mã chấm cơm để hệ thống tự sinh vì phải duy nhất)
      → employee id **1441**, hồ sơ id 1876, mã NV/mã chấm cơm 11911298, Phòng Cộng tác viên_NV; `PUT admin/accounts/1441` chép điểm nhận cơm + hạn mức công nợ
- [x] Gán vai trò giống id 13 qua `PUT admin/employee-roles/1441`: TPE (Giám đốc, Kinh doanh Tự xử lý DATKT, Super Admin, Super admin (DNS DÙNG),
      Thử nghiệm AI + GROUP CHAT, toàn bộ phòng ban) + thêm công ty TPV/TPSG (Super Admin) + EG (không vai trò).
      Để gán ở TPV/TPSG phải tạm đổi công ty đang làm việc của tài khoản user rồi đã trả về như cũ (company_role = null)
- [x] Kiểm tra: đăng nhập `dnstester@gmail.com` / `2026Dns@1` OK; vai trò từng công ty khớp id 13, tổng quyền hiệu lực 943 = 943

### Checkpoint — 18/11/2026
Vừa hoàn thành: tạo tài khoản Dns Tester (id 1441) trên hrm.eteksofts.com, quyền giống DNS NamDang (id 13)
Đang làm dở: —
Bước tiếp theo: user đăng nhập thử trên trình duyệt
Blocked:
