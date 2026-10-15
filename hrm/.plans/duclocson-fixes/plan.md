# Sửa lỗi riêng bản Đức Lộc Sơn (nhánh `duclocson`)

## Báo cáo tổng hợp đi giao việc/công tác — hiện tổng số nhưng bảng trống (12/10/2026)
- [x] FE: `getData()` đọc thừa `.data` (`response.data.data.data`) → bảng trống khi mở màn / nhấn Enter ô tìm kiếm
- [x] FE: nhân viên không có phòng ban làm vỡ bảng → method `departmentName()`
- [x] BE: lọc nhân viên đã xoá hồ sơ (employeeInfo null) trước khi đọc `->ssn` (JobAssignmentNote + BusinessTripAssign)
- [x] Deploy 12/10/2026 (api b52db4c6, client e627cdf1) bằng ~/build_tpe.sh mới tạo trên server
- [ ] User test lại trên hrm.duclocson.vn
