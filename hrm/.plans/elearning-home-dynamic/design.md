# elearning-home-dynamic — Tóm tắt design

- **Người phụ trách**: @junfoke
- **Ngày**: 2026-07-15
- **Spec chi tiết**: `docs/superpowers/specs/2026-07-15-elearning-home-dynamic-design.md`

## Mục tiêu

Thay 2 khối còn hardcode ở homepage elearning (`elearning/src/views/home/HomeView.vue`) bằng data thật:
1. **Hoạt động gần đây** (trong `HeroBanner`) — đang lấy `RECENT_ACTIVITIES` mock.
2. **Danh mục nội dung** — đang lấy `CATEGORIES` mock + đếm trên mock.

## Scope

**Trong scope**: 2 API elearning mới + 2 migration additive + ô chọn icon ở màn Loại đào tạo (hrm-client) + sửa store/HeroBanner/HomeView.

**Ngoài scope**: khối Vinh danh (vẫn mock), 4 section giữa (đã là data thật qua `public/home-content`), 2 nút demo "Bạn cần học"/"Khuyến nghị" trong banner.

## Các quyết định lớn

| # | Quyết định |
|---|---|
| 1 | Feed là **toàn hệ thống** (hoạt động của mọi người), gồm cả nhân viên HRM lẫn học viên ngoài |
| 2 | Chỉ **3 loại**: bắt đầu học / hoàn thành / đạt chứng nhận (bỏ "cập nhật tiến độ" như event riêng — spam feed, xem #8) |
| 3 | **Đọc thẳng bảng enrollment**, KHÔNG tạo bảng activity log, KHÔNG chạm luồng học đang chạy |
| 4 | **Bỏ nút "Xem →"** — không làm màn list hoạt động riêng |
| 5 | **15 dòng / 30 ngày / mỗi người tối đa 2 dòng** (chống một người chiếm feed) |
| 6 | **Danh mục = `training_types`** — không tạo bảng mới, không tạo màn quản lý mới. Chỉ thêm cột `icon` + `sort_order`, admin chọn ở màn Loại đào tạo có sẵn |
| 7 | Guest/học viên ngoài **chỉ thấy hoạt động + count của nội dung `is_public = 1`** (tránh lộ khóa nội bộ ra internet) |
| 8 | **Phụ đề tiến độ lộ trình** (chốt 2026-07-15): dòng `complete`/`certificate` của khoá thuộc **đúng 1** lộ trình đã ghi danh → hiện thêm *"2/5 trong lộ trình X"*. **Không** tạo event "cập nhật tiến độ" riêng |

## Điểm cần nhớ

- Data thật nằm ở `Modules/Training` (`subject_enrollments`, `learning_path_enrollments`), không phải `Modules/Elearning`.
- **Cả 2 bảng enrollment đều có `employee_id` + `learner_id` (nullable)** — migration `Modules/Elearning/.../2026_05_27_100000_add_learner_id_to_enrollment_tables.php`. Học viên ngoài học lộ trình + nhận chứng chỉ lộ trình bình thường (`LearningSessionService::syncLearningPathCompletion()` ưu tiên `learner_id`). → Cả 4 query feed đều tra tên theo 2 nguồn, không có ngoại lệ.
  ⚠️ Bài học: migration của bảng `Modules/Training` **có thể nằm trong `Modules/Elearning/Database/Migrations`** — luôn grep toàn repo, đừng chỉ đọc migration tạo bảng.
- **Phụ đề tiến độ phải tính theo mốc quá khứ**, không phải trạng thái hiện tại: `done` = số khoá DONE có `completed_at <= occurred_at` của chính dòng đó. Thiếu mệnh đề này → dòng feed cũ hiện tiến độ cao hơn dòng mới, sai sự thật và người dùng nhìn ra ngay.
- `learning_path_subjects` (entity `LearningPathSubject`) — **1 khoá thuộc được nhiều lộ trình**. Đây là lý do phải bỏ phụ đề khi khoá thuộc ≥2 lộ trình đang học, và cũng là lý do không tách event "cập nhật tiến độ" (1 hành động → N dòng).
- elearning **không có dayjs** → tự viết `src/utils/timeAgo.js`, không thêm dependency.
- hrm-client **đã nạp Remix Icon CDN** (`nuxt.config.js:56`) → icon picker preview được icon thật.
- 2 migration additive — **user tự chạy**, không tự động migrate.
- Bỏ getter `categoryCount` sẽ kéo theo `mixAll` / `pickThumb` / state `courses`,`subjects` / import `THUMBS`,`COURSES`,`SUBJECTS` trong `stores/elearning.js` thành code chết → xoá luôn. (`store.courses`/`store.subjects` ở các file khác là của store `learningPathDetail`/`learningSession`, không liên quan.)
