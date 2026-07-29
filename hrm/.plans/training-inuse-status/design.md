# Đồng bộ trạng thái + chặn xóa theo "đang dùng" (Bài học / Khóa học / Lộ trình)

> Owner: @junfoke — Bắt đầu 2026-07-20
> Spec chi tiết: `docs/superpowers/specs/2026-07-20-training-inuse-status-design.md`

## Mục tiêu

Thống nhất khái niệm trạng thái và ràng buộc thao tác cho 3 entity đào tạo (Bài học → Khóa học → Lộ trình), mô hình theo pattern tham chiếu của module Assign (Ngành → Ứng dụng → Dự án). Xuất phát từ việc phát hiện 3 entity đang **bất nhất** cả về nhãn status lẫn cách xác định "đang dùng".

## Hiện trạng (vấn đề)

| Entity | Bộ status | Xác định "đang dùng" |
|---|---|---|
| Bài học (Lesson) | 1=Hoạt động, 2=Khóa | ❌ `canDelete()` đang STUB (`$isUsedInCourse = false; // TODO`) |
| Khóa học (Subject) | 1=Hoạt động, 2=Khóa, 3=Nháp | ✅ check 5 bảng downstream — nhưng **thiếu** `learning_path_subjects` + enrollment |
| Lộ trình (LearningPath) | 1=Nháp, 2=**Đang dùng**, 3=Khóa | ⚠️ thủ công; `is_can_delete` = chỉ khi Nháp |

→ Lệch mã status (Nháp=1 ở LP nhưng =3 ở Subject) từng gây bug ở tính năng chống trùng tên trước đó.

## Quyết định đã chốt

1. **Đồng bộ nhãn status lộ trình:** đổi `2 = "Đang dùng"` → `"Hoạt động"`. **Chỉ đổi nhãn hiển thị, GIỮ nguyên mã số** (1=Nháp, 2=Hoạt động, 3=Khóa). Không migrate DB.
2. **Định nghĩa "đang dùng"** (chặn Xóa khi thỏa 1 trong 2):
   - **Bị cấp trên ĐÃ XUẤT BẢN tham chiếu** (Nháp KHÔNG tính):
     - Bài học ∈ `subject_lessons` của khóa học status ∈ {Hoạt động, Khóa}
     - Khóa học ∈ `learning_path_subjects` của lộ trình status ∈ {Hoạt động, Khóa} **+ giữ 5 check downstream hiện có**
   - **Có học viên ghi danh:** `enrollment_lesson_progress` (bài học) / `subject_enrollments` (khóa) / `learning_path_enrollments` (lộ trình)
3. **Chỉ chặn XÓA.** Khóa + Sửa luôn cho phép.
4. **Nới điều kiện xóa lộ trình:** từ "chỉ xóa khi Nháp" → "xóa được trừ khi có học viên ghi danh" (lộ trình Hoạt động chưa ai học vẫn xóa được) — đồng bộ 3 entity.
5. **Gỡ ràng buộc khóa lộ trình:** bỏ chặn "Lộ trình đang dùng, không thể khóa" → khóa được cả bản Hoạt động (để bảo trì).
6. **Badge "Bị khóa" phía learner (elearning):** khi khóa học/lộ trình đang học bị Khóa → hiện badge "Bị khóa" ở màn "Khóa học của tôi". (Khóa học đã có sẵn cờ `locked`; lộ trình còn thiếu; FE chưa render badge.)

## Phạm vi

- **Phase 1 — BE Training** (`Modules/Training`): nhãn status LP; chuẩn hóa `is_can_delete`/`is_can_lock` 3 entity; chặn xóa; nới xóa LP; gỡ chặn khóa LP; expose transformer.
- **Phase 2 — FE hrm-client** (`pages/training`): nhãn status LP; ẩn/disable nút Xóa theo `is_can_delete` + tooltip; toast 400 khi cố xóa.
- **Phase 3 — elearning** (`Modules/Elearning` + `elearning/src`): thêm cờ `locked` cho lộ trình trong MyLearningService; render badge "Bị khóa" trên thẻ My Learning (khóa + lộ trình).

## Ngoài phạm vi

- Không migrate/đổi mã số status (chỉ đổi nhãn).
- Không chặn Sửa/Khóa theo "đang dùng".
- Không đụng luồng validate trùng tên (đã xong ở tính năng trước).
