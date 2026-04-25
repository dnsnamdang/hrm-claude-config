# Design: Làm lại giao diện danh sách khoá học

**Spec chi tiết:** [docs/superpowers/specs/2026-04-25-subjects-list-ui-design.md](../../docs/superpowers/specs/2026-04-25-subjects-list-ui-design.md)

## Mục tiêu

Fix 3 bug logic + 1 bug CSS + thêm nút lock/unlock trạng thái trong bảng danh sách khoá học (`subjects/index.vue`). Dựa theo prototype `Course_list.html`.

## Scope

Chỉ sửa `hrm-client/pages/training/subjects/index.vue`.

## Quyết định chính

- Giữ hover row actions (không thêm cột Hành động riêng)
- Giữ Bootstrap badge (không đổi sang pill màu theo prototype)
- Giữ text thuần cho Loại đào tạo / Hình thức đánh giá
- Không thêm page header (pageTitle qua V2BaseDataTable là đủ)
- Thêm nút lock toggle (Bootstrap style) vào cột Trạng thái
