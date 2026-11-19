# Sửa lỗi riêng bản Đức Lộc Sơn (nhánh `duclocson`)

## Báo cáo tổng hợp đi giao việc/công tác — hiện tổng số nhưng bảng trống (12/10/2026)
- [x] FE: `getData()` đọc thừa `.data` (`response.data.data.data`) → bảng trống khi mở màn / nhấn Enter ô tìm kiếm
- [x] FE: nhân viên không có phòng ban làm vỡ bảng → method `departmentName()`
- [x] BE: lọc nhân viên đã xoá hồ sơ (employeeInfo null) trước khi đọc `->ssn` (JobAssignmentNote + BusinessTripAssign)
- [x] Deploy 12/10/2026 (api b52db4c6, client e627cdf1) bằng ~/build_tpe.sh mới tạo trên server
- [ ] User test lại trên hrm.duclocson.vn

## App — Lịch sử điểm danh lỗi "Connection closed while receiving data" (21/10/2026)
- [x] BE: `TimekeeperService::employeeIndex` không có mốc ngày thì mặc định từ đầu tháng (của mốc "đến" nếu có) + eager load `conn_info`/`employee_info` — 2,77MB/1,42s → 66KB/0,08s
- [ ] Commit + deploy nhánh `duclocson` (chờ user cho phép)
