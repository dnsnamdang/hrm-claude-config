# Sửa dữ liệu prod theo yêu cầu (không có số Redmine) — @cuong61n

## Phiếu giao việc PGV-32497 — sửa giờ kết thúc (10/11/2026)
- [x] 10/11/2026 — Chấm công báo: chị Thúy lập phiếu giao việc đi ăn (id 32497) nhưng điền nhầm giờ kết thúc 20:00 → hệ thống tính về sớm cho cả 8 nhân sự trong phiếu. Đã sửa trên PROD (hrm_erp_gop):
  - `job_assignment_note_details.id=32621`: `intend_end_at` 2026-11-09 20:00:00 → **17:15:00** (giờ bắt đầu giữ 17:00).
  - `job_assignment_notes.id=32497`: `total_minutes` 3.0 → 0.25 (cột chỉ lưu 1 số thập phân nên hiện 0.3).
  - Đã kiểm: đọc lại 2 bản ghi đúng giá trị mới. UPDATE có WHERE theo id + giá trị cũ.
  - Chờ: người báo xác nhận hết tính về sớm trên bảng công.

## Xoá 2 phiếu xin nghỉ phép ETEKPOWER của Nguyễn Hoàng Dũng (17/11/2026)
- [x] 17/11/2026 — Chị Thu Huyền báo: anh Dũng (102211230, ETEKPOWER) chọn nhầm loại nghỉ ở 2 phiếu nghỉ phép tháng 11 (4 ngày phép) → xoá 2 phiếu, phía TPE xử lý. Đã xoá trên PROD (hrm_erp_gop):
  - `attendances.id=14959` (09–11/11, 3 ngày) và `id=14965` (16/11, 1 ngày): cùng `employee_id=1799`, `leave_type_id=67` Nghỉ phép, `attendance_status=2` đã duyệt.
  - Phiếu đã duyệt nên API xoá (chỉ xoá được status 0) từ chối → xoá cứng bằng SQL, `WHERE id IN (...) AND employee_id=1799 AND leave_type_id=67 AND attendance_status=2`, bảng không có deleted_at. Không có dòng `attendances_extend_requests` bám theo.
  - Đã kiểm: row_count = 2, đọc lại còn 0 dòng. Backup 2 dòng: `hrm-prod:~/backup_xoa_phieu/attendances_14959_14965_20261117.sql`.
  - Chờ: người báo kiểm lại bảng công / số phép của anh Dũng; để anh Dũng lập lại phiếu đúng loại nghỉ.
  - [x] 17/11/2026 15:37 — Chị Thu Huyền báo tiếp: Báo cáo phép của anh Dũng vẫn ghi nghỉ 4 phép, còn 2 phép. Nguyên nhân: báo cáo đọc `timesheet_summaries.work_day_phep` (đã lưu sẵn), xoá phiếu không tự tính lại → còn dư phép 09, 10, 11, 16/11. Đã chạy `php artisan calc:employee_timesheet 1799 2026-11-09 2026-11-17` trên PROD: 10, 11, 16/11 về 0.
  - Kiểm lại bằng tài khoản cuong61n trên màn Báo cáo phép: Tháng 11 = 1.0, Tổng phép đã dùng 13 → **10**, Tổng phép còn lại 2 → **5**.
  - Còn 1 ngày phép 09/11 là do bản ghi cập nhật công thủ công `admin_request_update_working_employees` id 5247 (tạo 17/11 08:40, không phải từ 2 phiếu đã xoá) → giữ nguyên, chờ chị Thu Huyền xác nhận có đúng không.

## Chặn tạo phiếu tra soát công admin "Nghỉ phép quên làm phiếu" khi đã có đơn xin nghỉ trùng ngày (17/11/2026)
- [x] 17/11/2026 — Từ ca anh Dũng: phiếu tra soát 2192 (trừ 1 ngày phép 09/11) vẫn tạo được dù đơn nghỉ 14959 (09–11/11, đã duyệt) còn đó → khi đơn bị xoá, phiếu tra soát còn sót, báo cáo phép lệch 1 ngày. Code cũ chỉ kiểm số phép còn lại, không kiểm đơn xin nghỉ trùng ngày.
  - Nghiệp vụ: phiếu có trừ ngày phép (`number_day_leave > 0`) bị chặn 422 nếu nhân viên đã có đơn xin nghỉ **chờ TP duyệt / chờ NSHC duyệt / đã duyệt** phủ ngày cần tra soát; thông báo nêu tên NV + mã đơn + khoảng ngày. Đơn nháp/từ chối không chặn. Phiếu không trừ phép (number_day_leave = 0) không bị ảnh hưởng.
  - Kỹ thuật: `Modules/Timesheet/Http/Requests/CreateUpdateAdminTimeSheetRequest.php` thêm `validateNoLeaveRequestOverlap()` gọi trong `withValidator`; message nghiệp vụ riêng gắn vào `number_day_leave`.
  - Đã kiểm (local, gọi FormRequest thật): ngày trùng đơn 13547 → 422 đúng thông báo; ngày không trùng → qua; number_day_leave=0 → qua. `php -l` sạch.
  - Trạng thái: **đã deploy PROD 17/11/2026** — commit `07953fb30` đẩy `origin/gop_db` (worktree tạm từ origin/gop_db, chỉ 1 file), chạy `~/build_tpe.sh` (BE pull + route:cache + restart worker, FE không đổi nên bỏ qua build). Prod đã có hàm `validateNoLeaveRequestOverlap`. Chưa test UI màn tạo phiếu trên prod. Còn chờ: quyết định xử lý phiếu 2192.
