# QTC: bỏ 2 cột công HC ở bảng IV "Quyết toán công khoán theo hợp đồng"

## Yêu cầu
Bảng IV (`EmployeeComponent.vue`) thừa 2 cột → bỏ:
- "Công hành chính được quyết toán" (`work_hr_settlement`)
- "Công HC truy thu/thực lĩnh" (`work_hr_truy_thu`)

## Tasks
- [x] Xoá 2 cột ở 3 chỗ: header, dòng nhân viên, dòng Tổng
- [x] Giữ nguyên computed (work_hr_settlement/work_hr_truy_thu) trong script — chỉ ẩn hiển thị (có thể còn dùng chỗ lưu/tab khác)

## Ghi chú
- FE-only, branch `tpe` (hrm-client). Chưa commit tới khi user duyệt.
