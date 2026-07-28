# Elearning — Học theo danh mục (trộn Lộ trình + Khóa học)

**Owner:** @junfoke — **Ngày tạo:** 2026-07-27
**Spec chi tiết:** [docs/superpowers/specs/2026-07-27-elearning-category-contents-design.md](../../docs/superpowers/specs/2026-07-27-elearning-category-contents-design.md)

## Mục tiêu
Click 1 danh mục (loại đào tạo) ở trang chủ elearning → 1 màn hiển thị **cả lộ trình học lẫn khóa học** thuộc danh mục đó, gộp chung 1 grid, phân biệt bằng badge, có bộ lọc loại đào tạo / tên / trạng thái. Hiện tại chỉ ra khóa học.

## Các quyết định lớn
- **Data:** Hướng A — thêm endpoint BE gộp `GET /public/contents` (trộn path+course, phân trang/sort/filter server-side). Cần branch `tpe-develop-elearning`.
- **Route:** tạo view/route mới `learning-contents` (`/learning/contents`); giữ nguyên `learning-by-category`.
- **"Xem tất cả":** trỏ sang màn trộn mới, không kèm `training_type_id`.
- **UI:** dùng lại layout list-page + `LearnCard` (badge sẵn có). Filter: loại đào tạo (pre-select) + trạng thái + keyword.

## Phạm vi
- BE: 1 endpoint gộp (tái dùng logic subjects + learning-paths).
- FE: 1 view mới `CategoryContentsView.vue` + 1 route + sửa 2 điểm điều hướng ở HomeView.
- Không sửa `LearnCard`, `useListPage`, `learning-by-category`.
