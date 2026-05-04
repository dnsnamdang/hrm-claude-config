# Thêm cột Mô tả vào các màn danh sách module Giao việc

## Mục tiêu
Bổ sung cột "Mô tả" (`description`) vào bảng danh sách của 7 màn trong module Giao việc, giúp người dùng xem nhanh mô tả mà không cần mở modal chi tiết.

## Scope
- 7 màn danh sách FE (chỉ thêm cột hiển thị, không sửa BE/API)
- Vị trí cột: trước cột "Cập nhật"
- Hiển thị: `item.description || '—'`
- Style: `text-wrap`, width 250–300px

## Các màn áp dụng
1. `pages/assign/industry-groups/index.vue` — Nhóm ngành
2. `pages/assign/customer-scopes/index.vue` — Lĩnh vực khách hàng
3. `pages/assign/solution-groups/index.vue` — Nhóm giải pháp
4. `pages/assign/application/index.vue` — Ứng dụng
5. `pages/assign/project_items/index.vue` — Hạng mục dự án
6. `pages/assign/project_role/index.vue` — Vai trò dự án
7. `pages/assign/meeting_type/index.vue` — Loại meeting

## Spec chi tiết
Không cần spec riêng — thay đổi thuần UI, không ảnh hưởng logic/API.
