# Chuẩn hoá màn Ngân hàng câu hỏi khảo sát theo skill `list-page`

- **Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · **Ngày:** 2026-09-05
- **Màn:** `/assign/questions` — `hrm-client/pages/assign/questions/index.vue`
- Màn thứ 6 của đợt (sau solutions · industry-groups · application · customer-scopes · meeting_type)

## Điểm khác hẳn 5 màn trước: đây là màn CŨ HOÀN TOÀN

5 màn trước đã ở nền V2 (V2BaseFilterPanel + V2BaseDataTable), chỉ cần chuyển chuẩn. Màn này còn
nguyên **bootstrap-vue đời đầu**: `b-table` + `b-dropdown` + `b-collapse` + `Select2` +
`b-pagination` tự ghép, không dùng một component V2Base nào → phải **viết lại toàn bộ** (549 dòng
cũ → ~830 dòng mới).

## Phạm vi

FE đầy đủ theo `list-page` + `button-convention` + mục 15b, BE tối thiểu (whitelist sort, tên người
tạo, ô tìm nhanh, chữ hiển thị, popup chọn trường xuất Excel). **KHÔNG làm lịch sử thay đổi.**

## Quyết định riêng của màn

- **KHÔNG có cột Mã.** Bảng `survey_questions` không có cột mã; khoá `code` trong Resource là khoá
  **ảo** (`'cau_hoi_' . $id`) dựng riêng cho form-template. Theo skill mục 3a → cột định danh là
  **Tiêu đề câu hỏi**, và vì màn CÓ route chi tiết (`/assign/questions/{id}`) nên dùng `nuxt-link`
  (mục 3), không phải `button` như màn danh mục dùng modal.
- **Chữ của 3 trường phân loại chuyển về BE**: `data_type_text`, `application_scope_text`,
  `status_text`. Trước đây FE tự map bằng `getDataTypeLabel()` / `getApplicationScopeLabel()` /
  `getStatusText()` — thêm loại dữ liệu mới là phải sửa cả 2 nơi. Nguồn duy nhất giờ là hằng
  `SurveyQuestion::DATA_TYPE_NAMES`; FE chỉ còn giữ danh sách cho Ô LỌC.
- **Giữ 3 popup xác nhận riêng** (`confirm-question-delete/lock/unlock`) vì chúng có sẵn phần cảnh
  báo khi bản ghi đang được form khảo sát dùng — không thay bằng `BaseConfirmModal` chung.
- Sort: trước đây `index()` luôn `orderByDesc('id')`, bảng **không có cột nào sort được**; nay
  whitelist Tiêu đề / Ngày tạo / Ngày cập nhật.
