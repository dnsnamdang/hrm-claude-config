# Độ khó khóa học (Course Level) — Tóm tắt

- **Người phụ trách:** @junfoke
- **Spec chi tiết:** [docs/superpowers/specs/2026-06-09-course-level-design.md](../../docs/superpowers/specs/2026-06-09-course-level-design.md)

## Mục tiêu
Thêm trường "Độ khó" cho khóa học (`Subject`), biến từ mock/hardcode trong elearning
thành dữ liệu thật: admin chọn khi tạo/sửa → lưu DB → hiển thị + lọc ở trang duyệt elearning.

## Quyết định lớn
- 3 mức cố định: `1=Cơ bản`, `2=Trung cấp`, `3=Nâng cao` (enum trong code).
- Cột DB `level` **nullable**; bắt buộc **ở form**. Khóa cũ `null` → "Chưa phân loại".
- Hiển thị: form admin, bộ lọc + card + chi tiết trang duyệt elearning.
- **Scope:** chỉ Khóa học (Subject). Lộ trình (LearningPath) ngoài scope.

## Các tầng thay đổi
- **DB:** migration thêm cột `level` + hằng `Subject::LEVELS`.
- **BE (hrm-api):** validate store/update; `SubjectDetailResource` + `SubjectBrowseResource`
  thêm `level`/`level_name`; `PublicBrowseController` thêm `levels` vào filterOptions + filter `level`.
- **FE admin (hrm-client):** `TabInfo.vue` dropdown bắt buộc; `SubjectBuilderForm.vue` payload.
- **FE elearning:** `filterOptions.js` nạp `levels`; sidebar filter "Độ khó"; card badge; `subjectDetail.js` dùng level thật.
