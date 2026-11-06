# Kiểm tra NV nghỉ việc không hiện trong bảng lương tháng 10 — PROD TPE — @cuong61n

Phản ánh (06/11/2026, qua chat): "nhân sự này nghỉ việc trong tháng 10, trạng thái đã nghỉ việc → không hiển thị trong bảng lương tháng 10; đúng: bảng lương tháng 10 vẫn phải hiện".

## Tasks

- [x] (06/11/2026) Điều tra trên PROD (hrm.eteksofts.com, DB `hrm_erp_gop`, code nhánh gop_db `681db8655`) — chỉ đọc, không sửa dữ liệu
  - Nghiệp vụ: NV nghỉ trong tháng vẫn được đưa vào bảng lương tháng đó. Logic popup "Thêm nhân sự" (`Modules/Timesheet/Services/EmployeeInfoService.php` ~dòng 118–140) lấy NV `status = đang làm` HOẶC `leave_date > ngày 02 của tháng áp dụng` → NV nghỉ 15/10 vẫn lọt vào bảng lương tháng 10. Màn chi tiết (`SalaryService::getSalaryEmployee`, FE `pages/payroll/salary/_id/index.vue`) không lọc trạng thái.
  - Dữ liệu: bảng "Bảng lương tháng 10/2026" id 747 (TPE, tạo 09:50 06/11, 405 NV). NV nghỉ tháng 10 của TPE: Nguyễn Quốc Trung (12611043, nghỉ 15/10) và Hoàng Thị Hải Yến (12510585, nghỉ 01/11, QĐ chấm dứt HĐ cập nhật 09:26 06/11) → **cả 2 đều ĐANG CÓ trong bảng 747**.
  - Log nginx: sáng 06/11 HR đã tạo/xoá thử các bảng 742, 745, 746 rồi mới tạo 747 → khả năng lúc phản ánh đang xem bảng cũ đã xoá, hoặc bảng tạo trước khi QĐ nghỉ việc được cập nhật.
  - Ghi nhận biên: NV có `leave_date` = 01 hoặc 02 của tháng bị loại khỏi bảng lương tháng đó (vd Nguyễn Việt Hải 82611028 – Cty 8, nghỉ 01/10). Chưa sửa — chờ xác nhận nghiệp vụ.
  - Trạng thái: chờ user xác nhận đúng nhân sự được phản ánh (tên/mã NV) và tài khoản đang xem.
