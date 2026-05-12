# Lộ trình học (Learning Path) — Tóm tắt Design

> Người phụ trách: @khoipv  
> Spec chi tiết: `docs/superpowers/specs/2026-04-29-learning-path-design.md`

## Mục tiêu

Màn Tạo/Sửa/Xem Lộ trình học — gom nhiều khoá học (subjects) thành 1 lộ trình, kết quả dựa trên Đạt/Không đạt của từng khoá.

## Quyết định lớn

- **3 bảng DB:** `learning_paths` + `learning_path_subjects` + `learning_path_assignees`, không FK constraint
- **Mã:** `LP-YYYY-NNNNN`
- **"Danh mục lộ trình"** → thay bằng **Loại đào tạo** (training_types)
- **Khoá học:** lấy từ `subjects/getAll`, bài học read-only từ subjectLessons
- **FE pattern:** Page orchestrate (`add.vue`) + 4 tab component riêng (TabInfo, TabResult, TabLearners, TabCertificate)
- **API:** route model binding `{learningPath}`, 1 request lưu toàn bộ
- **Phân quyền:** permission "Quản lý lộ trình học" + filter company/department/part
- **Chứng chỉ:** canvas preview + jsPDF client-side

## Scope

4 tab đầy đủ, full BE + FE cùng lúc.
