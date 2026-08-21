# Đồng bộ loại đào tạo — Tóm tắt

**Owner:** @junfoke · **Ngày:** 2026-07-28 · **Module:** Training

## Mục tiêu
Khóa học chỉ chứa **bài học cùng loại đào tạo**; Lộ trình chỉ chứa **khóa học cùng loại đào tạo**. Hiện tại 2 picker không ràng buộc → dữ liệu lẫn loại.

## Quyết định (đã chốt)
1. Popup chọn **ẩn hẳn** item khác loại + chốt chặn BE khi lưu.
2. Chưa chọn loại → **chặn mở popup** (toast nhắc chọn loại trước).
3. Đổi loại sau khi đã thêm → **cảnh báo + chặn lưu** tới khi gỡ (không tự xóa).
4. Dữ liệu cũ lẫn loại (mở sửa) → **cảnh báo + chặn lưu** tới khi gỡ.

## Phạm vi (7 file, không migration)
- **FE Khóa học:** `subjects/tabs/TabInfo.vue` (filter popup + guard + mismatch UI), `SubjectBuilderForm.vue` (chặn validate/saveDraft).
- **FE Lộ trình:** `learning-path/TabInfo.vue` (filter popup + guard + mismatch UI), `LearningPathForm.vue` (chặn validate).
- **BE:** `SubjectDetailResource.php` (+`training_type_id` trong lesson), `SubjectBuilderRequest.php` + `LearningPathRequest.php` (after() chặn mismatch).

Tận dụng pattern sẵn có: broken/locked lesson (khóa học) và violatingPublicSubjects (lộ trình).

## Spec chi tiết
`docs/superpowers/specs/2026-07-28-dong-bo-loai-dao-tao-design.md`
