---
name: list-page
description: Quy tắc xây dựng màn danh sách với permission theo cấp
---

# Quy tắc xây dựng permission cho các màn danh sách tổng hợp
- Áp dụng cho các bảng có các field: company_id, department_id, part_id (field này có thể có hoặc không) =>> Nếu có thì quyền sẽ theo bộ quyền như sau Xem [Tên màn danh sách] theo công ty, Xem [Tên màn danh sách] theo phòng ban, Xem [Tên màn danh sách] theo bộ phận, Xem tất cả [Tên màn danh sách]
- Quyền xem tất cả =>> Lấy tất cả bản ghi trừ trạng thái Đang tạo / Nháp
- Các quyền còn lại query theo các field tương ứng
- Bộ lọc luông bắt đầu bằng: Lọc theo công ty >> Lọc theo phòng ban >> lọc theo bộ phận ==>> Tuân thủ theo V2BaseFilterPanel.vue
- Style bắt buộc: luôn import `@import '@/assets/scss/v2-styles.scss';` trong thẻ `<style lang="scss">` của trang danh sách
- Các khối bộ lọc theo logic Cascading filter: Công ty =>> Phòng ban =>> Bộ phận; Dự án TKT =>> Giải pháp =>> Hạng mục