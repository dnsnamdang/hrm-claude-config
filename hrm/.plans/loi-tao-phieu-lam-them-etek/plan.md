# Lỗi tạo phiếu đăng ký làm thêm cổng ETEK (chưa có số Redmine) — @cuong61n

## Task 1: Điều tra lỗi "Lỗi máy chủ" khi tạo phiếu đăng ký làm thêm trên hrm.etek.com.vn
- Nghiệp vụ: HCNS ETEK báo tạo phiếu đăng ký làm thêm báo "Lỗi máy chủ / Tạo phiếu làm thêm thất bại", NV không có ca và chưa vượt trần giờ tháng.
- Kết quả (đọc log prod, không ghi): `/var/www/etek/hrm-api` (nhánh `tpe`, commit `d8b112be3` "thêm check vượt trần làm thêm", pull lên 06/11/2026 14:04) — `OvertimeAssignmentRequest.php:364` gọi `OvertimeAssignmentService::checkMonthlyOvertimeLimit` nhưng thiếu `use Modules\Timesheet\Services\OvertimeAssignmentService;` → `Class "...Http\Requests\OvertimeAssignmentService" not found` → 500. 96 lượt lỗi từ 07/11 09:15.
- Phạm vi: lỗi nằm trên `origin/tpe` → ảnh hưởng etek + etekpower (etekpower chưa ai tạo nên chưa có log). `gop_db`/`develop` (site tpe) đã có dòng `use` → không lỗi. toyota chưa pull commit này.
- [x] 07/11/2026 Điều tra xong. Hướng sửa: thêm 1 dòng `use` trên nhánh `tpe`, push, pull lại etek + etekpower — chờ user cho phép push/deploy.

## Task 2: Sửa + deploy etek, etekpower
- Nghiệp vụ: tạo phiếu đăng ký/phân công làm thêm ở ETEK, ETEK POWER lưu lại được bình thường, trần giờ tháng vẫn chặn như commit `d8b112be3`.
- Kỹ thuật: thêm `use Modules\Timesheet\Services\OvertimeAssignmentService;` vào `OvertimeAssignmentRequest.php` (rà các file còn lại của commit `d8b112be3` thì đều đủ `use`). `php -l` sạch.
- [x] 07/11/2026 Đã push nhánh `tpe` commit `8ec3006b0`. Deploy prod 16:42 cho etek + etekpower (`git pull --ff-only`, opcache validate_timestamps=On nên không cần reload). Class nạp được trên cả 2 site, không có lỗi mới sau thời điểm deploy. Chưa tự tạo phiếu thật trên prod, chờ HCNS ETEK tạo lại để xác nhận.
