# Quy tắc xây dựng permission cho các màn danh sách tổng hợp
- Áp dụng cho các bảng có các field: company_id, department_id, part_id (field này có thể có hoặc không) =>> Nếu có thì quyền sẽ theo bộ quyền như sau Xem [Tên màn danh sách] theo công ty, Xem [Tên màn danh sách] theo phòng ban, Xem [Tên màn danh sách] theo bộ phận, Xem tất cả [Tên màn danh sách]
- Quyền xem tất cả =>> Lấy tất cả bản ghi trừ trạng thái Đang tạo / Nháp
- Các quyền còn lại query theo các field tương ứng
- Bộ lọc luôn bắt đầu bằng: Lọc theo công ty >> Lọc theo phòng ban >> lọc theo bộ phận ==>> Dùng `<b-button v-b-toggle>` + `<b-collapse>` cho filter panel