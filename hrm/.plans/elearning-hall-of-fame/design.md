# elearning-hall-of-fame — Tóm tắt design

- **Người phụ trách**: @junfoke
- **Ngày**: 2026-07-16
- **Spec chi tiết**: `docs/superpowers/specs/2026-07-16-elearning-hall-of-fame-design.md`
- **Liên quan**: `.plans/elearning-home-dynamic/` (feed + danh mục — khối Vinh danh khi đó cố ý để ngoài scope)

## Mục tiêu

Thay khối "Vinh danh học viên" ở trang chủ elearning (`HALL_OF_FAME` — 5 thẻ cứng) bằng bảng vàng **tự tính theo cấu hình**. Đây là khối mock cuối cùng của trang chủ.

Yêu cầu gốc từ sếp: *"cho họ cấu hình cách lấy dữ liệu ra rồi PM tự xử lý, không cần mỗi tháng họ vào chọn lại"*.

## Các quyết định lớn

| # | Quyết định |
|---|---|
| 1 | **Hệ thống tự tính theo cấu hình** — bác bỏ hướng "admin chốt tay từng tháng" (nợ vận hành) |
| 2 | **6 tiêu chí** + 1 tổng hợp. Bỏ "streak" (tốn query, khái niệm mới) và "tốc độ hoàn thành" (méo — khoá ngắn luôn thắng) |
| 3 | **Top N cấu hình riêng từng danh hiệu** |
| 4 | **"Gương mặt tiêu biểu" = tiêu chí tổng hợp tự tính**: lọt top của ≥ `min_criteria` bảng khác. Biến danh hiệu chủ quan duy nhất thành tính được |
| 5 | "Đạt tiêu chí" = **lọt top** của tiêu chí đó (tương đối), không phải vượt ngưỡng tuyệt đối |
| 6 | **Mỗi người đúng 1 thẻ** — khử trùng theo `sort_order`, bảng dưới nhường suất cho người kế tiếp |
| 7 | **Một kỳ chung** cho cả khối, mặc định **30 ngày gần nhất** (tránh trang chủ hụt một mảng mỗi đầu tháng) |
| 8 | **Học viên ngoài có lên bảng vàng**, dòng phòng ban ghi "Học viên ngoài" |
| 9 | **Quyền mới** `Quản lý vinh danh học viên` (ID 1082) trong `PermissionsTableSeeder` |
| 10 | **Dùng chung 1 icon** huy chương vàng như mock — không cho chọn icon từng danh hiệu |

## Điểm cần nhớ

- **Điểm thi lấy từ `subject_enrollments.exam_score`**, KHÔNG phải `exam_test_results`. `LearningSessionService::syncSubjectExamCompletion()` (dòng 497, 541) đã chốt điểm theo `exam_score_rule` của khoá (highest/last/average) rồi ghi vào cột này — đọc từ đây vừa gọn vừa đúng nghiệp vụ.
- ⚠️ **Học viên ngoài KHÔNG bao giờ có `exam_score`**: `syncSubjectExamCompletion($employeeId, ...)` chỉ nhận employeeId, docblock ghi rõ *"Chỉ áp dụng employee"*; `exam_test_results` cũng chỉ có `employee_id`. → Tiêu chí điểm thi loại họ **do bản chất dữ liệu**, không phải do thiết kế. User đã biết và chấp nhận.
- ⚠️ **`enrollment_lesson_progress.STATUS_DONE = 2`**, khác `SubjectEnrollment::STATUS_DONE = 3`. Dùng nhầm hằng là ra số sai mà không báo lỗi.
- **`on_time_rate` phải có ngưỡng tối thiểu 3 nội dung có hạn** (hằng trong code, KHÔNG đưa ra cấu hình): không có thì người 1/1 = 100% luôn thắng người 19/20 = 95% → bảng vàng vinh danh người học ít nhất.
- **Chỉ cho tối đa 1 badge `composite`** — 2 cái sẽ đếm lẫn nhau, vô nghĩa.
- Seed `min_criteria = 2` (không phải 3): seed chỉ có 3 badge thường, ngưỡng 3 đòi lọt top cả 3 bảng → gần như không ai đạt, bảng vàng mặc định không bao giờ có Gương mặt tiêu biểu.
- `owner_key` dùng chung quy ước với `HomeActivityService`: `e:{employee_id}` / `l:{learner_id}`.
- Thẻ vinh danh **không hiện tên khoá học** → khác feed hoạt động, **không cần lọc `is_public`**.
- `dept` lấy qua `EmployeeInfo::department()`/`part()` (`Modules/Human/Entities/EmployeeInfo.php:696-704`) — đã verify.
- `PermissionsTableSeeder` khai ID tường minh, max hiện tại = 1081 → dùng 1082.
- Sau feature này `HALL_OF_FAME` hết người import → xoá; kiểm tra `mockData.js` còn export nào sống không, không còn thì xoá cả file.
- 2 migration + 1 seeder — **user tự chạy**, không tự động migrate/seed.
