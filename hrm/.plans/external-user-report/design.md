# Báo cáo học tập — Học viên ngoài công ty — Design (tóm tắt)

**Owner:** @junfoke
**Ngày:** 2026-06-06

---

## Mục tiêu

Màn báo cáo học tập cho học viên ngoài công ty (đăng ký qua form / Google Auth, học khoá & lộ trình public). Hiển thị tạm thời ở menu **Đào tạo → Danh mục**.

## Scope

- **FE hrm-client**: 1 trang mới `pages/training/external-user-report/index.vue`
- **BE hrm-api**: 2 endpoint mới trong `ExternalUserController` (tái dùng entity sẵn có)
- Thêm 1 mục menu vào `training-sidebar.vue`
- Sửa nhẹ component dùng chung `V2BaseDataTable` (thêm `rowClickable` opt-in)

## Quyết định chính

1. **Phân vai component**: màn danh sách ngoài dùng `V2BaseDataTable` (đồng bộ style module); **popup chi tiết dùng table custom** (không bắt buộc V2Base — theo yêu cầu user).
2. **Row-click**: thêm prop opt-in `rowClickable` vào `V2BaseDataTable` (mặc định `false` → không ảnh hưởng màn khác), emit `row-click`, tự bỏ qua khi click nút/link trong dòng.
3. **Dữ liệu thật**: gộp enrollment từ `subject_enrollments` (khoá) + `learning_path_enrollments` (lộ trình) qua `learner_id` (= `elearning_learners.id` = `ExternalUser`).
4. **Tiến độ & trạng thái lộ trình**: theo logic chuẩn learner portal (`MyLearningService`):
   - Tiến độ lộ trình = **trung bình `progress` các khoá** trong lộ trình (KHÔNG phải done/tổng).
   - Hoàn thành khi `status == DONE` **hoặc** `progress >= 100` (cột `status` của LP không cập nhật đáng tin → suy từ progress).
5. **"Đạt"**: DB chưa có cột `is_passed` → quy ước "Đạt" = hoàn thành (done). Cần làm chuẩn theo kết quả thi/chứng chỉ thì mở rộng sau.

## API

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `training/external-users/report` | Danh sách học viên + thống kê (enrolled/learning/completed/passed/completionRate) + KPI summary. Filter: keyword, auth_source, has_enrollment, from_date, to_date. Sort: name/enrolled/completionRate/registeredAt. Không phân trang (trả toàn bộ đã lọc). |
| GET | `training/external-users/{id}/enrollments` | Drill-down chi tiết khoá + lộ trình của 1 học viên. |

## Tồn đọng / Defer

- Cột "Đạt" đang = hoàn thành (chưa có dữ liệu pass/fail thật).
- Nút "Xuất Excel" trong báo cáo còn demo (toast) — chưa có endpoint `report/export`.
- Báo cáo lấy toàn bộ học viên đã lọc, chưa phân trang.
- Mục menu để tạm ở "Danh mục", chưa gắn permission riêng.
