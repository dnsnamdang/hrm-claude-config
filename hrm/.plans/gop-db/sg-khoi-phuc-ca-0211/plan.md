# Khôi phục ca ngày 02/11/2026 bị mất của công ty Sài Gòn (company_id=4) (chưa có số Redmine) — @cuong61n

## Bối cảnh
Anh Nguyễn Huy Hoàng (22611020, id 1585) có đơn nghỉ #14525 duyệt từ 30/10 nhưng công 02/11 vẫn "KLD". Nguyên nhân: 02/11 09:52 (lịch sử 948–950, changed_by 670) gỡ ca 90 NV rồi gán lại nhầm năm 2027 nên 02/11/2026 mất ca; 03/11 13:44 (960/961) sửa sai nhưng gán lại từ 03/11. Không có ca thì đơn nghỉ không được tính vào công.

## Task
- [x] 04/11/2026 — Tra nguyên nhân qua `shift_assignment_history` + `attendances` (prod, chỉ đọc).
- [x] 04/11/2026 — Thêm lại ca 02/11 cho 86 NV thiếu (ca 21 / shift_detail 1, lấy từ lịch sử 948), transaction, bỏ qua người đã có ca.
- [x] 04/11/2026 — Chạy `create:many_timesheet_detail_by_employee` + `calc:employee_timesheet` 02/11 cho 90 NV trên prod (/var/www/tpe/hrm-api). Kết quả: 75 NV có dòng công (63 đủ công, 1 phép — gồm anh Hoàng 1,00 công/1,0 phép, 9 KLD, còn lại 0 công khác); 15 NV status=0 (đã nghỉ việc) không sinh công.

## Lưu ý
- 15 NV đã nghỉ việc nằm trong danh sách 948 nên cũng được thêm lại dòng ca 02/11 (giống trạng thái trước khi gỡ); không có bảng công. Nếu muốn dọn thì xoá riêng.
- Ghi trực tiếp DB nên màn Lịch sử phân ca không có dòng cho lần này.
- Đề nghị bên SG chú ý chọn đúng năm khi gán ca (tài khoản 670).
