# Fix: tab Chờ duyệt phiếu giao công tác lộ phiếu chi nhánh khác — @cuong61n

- [x] 27/10/2026 BE `AssignBusinessService` (searchByFilter + export, nhánh `type=waiting`): người có quyền "Trưởng phòng duyệt phiếu giao công tác" chỉ thấy phiếu chờ duyệt thuộc `manager_departments` + phiếu mình tạo/tham gia (trước đó thấy toàn hệ thống — case chị Bùi Thị Thịnh CN Vinh thấy phiếu Hà Nội)
- [x] 27/10/2026 BE Cấu hình phân hệ: `syncPlaceOrigins` cập nhật theo id (trước xoá hết tạo lại → phiếu CT mất "Địa điểm xuất phát", vd PCT-11263); `AssignConfigStoreRequest` chặn gỡ địa điểm đang có phiếu dùng (422 `places_origin`)
- [x] 27/10/2026 Dữ liệu prod: gán lại place_origin_id 19→28 (2156), 20→29 (591), 22→27 (1) theo binlog; nhóm cũ 1,2,9,12,13,14,17,18 (3.793 phiếu) để trống theo chốt của user
