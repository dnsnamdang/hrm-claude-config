# Dữ liệu tạo cho SRS Quản lý giải pháp (05/10/2026, DB local_hrm_erp)

- prospective_projects id=161 `HN_KD3.UD.0100.2026.DA097` "Cung cấp thiết bị khoang sơn và sấy cho xưởng dịch vụ Kia Hải Phòng" — INSERT SQL nhân bản từ dự án 152 (đổi mã/tên, status=2). Sau khi gửi YCGP dự án tự đồng bộ status=3.
- request_solutions id=35 `TPE.YCP.TC.26.0913` — tạo qua API POST assign/request-solutions (admin id 13, receive_dept 55, status 2), tiếp nhận qua API PUT .../35/receive (receive_id 13, pm_id 970). Sau khi tạo GP → status 6 (Đang thực hiện).
- solutions id=957 `HN_KD3.UD.0100.2026.DA097_GP40` "Giải pháp khoang sơn và sấy xưởng dịch vụ Kia Hải Phòng" — tạo qua GIAO DIỆN (admin, Lưu nháp), status 1 Nháp, PM 970; 1 hạng mục solution_modules id=957 (mã lưu `_HM01` — xem lỗi nghi ngờ), Leader 781, hạn 20/11/2026; version V1 tự sinh.
- Không xóa/sửa dữ liệu có sẵn. Ảnh h_*/s_* dùng lại từ HDSD Giải pháp (dữ liệu GP 955, 956).
