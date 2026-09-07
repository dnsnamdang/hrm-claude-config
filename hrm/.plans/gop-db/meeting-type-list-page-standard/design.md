# Chuẩn hoá màn Loại meeting theo skill `list-page`

- **Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · **Ngày:** 2026-09-05
- **Màn:** `/assign/meeting_type` — `hrm-client/pages/assign/meeting_type/index.vue`
- Màn thứ 5 của đợt chuẩn hoá (sau solutions · industry-groups · application · customer-scopes)

## Phạm vi

FE đầy đủ theo `list-page` + `button-convention` + mục 15b (bề rộng cột), BE tối thiểu
(whitelist sort, tên người tạo, ô tìm nhanh, popup chọn trường xuất Excel).
**KHÔNG làm lịch sử thay đổi.**

## Quyết định riêng của màn

- **KHÔNG có cột Mã.** Bảng `meeting_types` CÓ cột `code` nhưng **cả 6 bản ghi đều NULL** — cột này
  chỉ dùng đánh dấu bản ghi hệ thống (`MeetingType::SYSTEM_CODES`). Theo skill mục 3a, bảng không có
  mã dùng được thì **cột định danh là TÊN**, và không thêm cột chỉ toàn ô trống.
  → `typeName` là cột định danh: `sticky` + `locked` + là `button.v2-cell-link` mở modal Xem.
- **Bản ghi HỆ THỐNG (`is_system`) không hiện nút thao tác nào** (Sửa / Xóa / Khóa đều `visible: false`)
  thay vì hiện rồi disable — skill mục 7.2. Lý do đặt ở `title` của badge Trạng thái.
- **Giữ chọn nhiều dòng + Xóa hàng loạt** (chức năng thật của màn); ô chọn `sticky` + `locked` cùng
  nhóm với STT / Tên.
- Ô tìm nhanh trước đây bind thẳng vào `filters.name` (BE chỉ lọc `name`). Nay dùng `keyword` riêng
  (BE tìm **tên + người tạo**), còn `name` thành ô lọc nâng cao độc lập.

## Hiện trạng lệch chuẩn (đã sửa)

| Điểm | Trước | Sau |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + 6 ô hard-code | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Cột định danh | Tên + dòng phụ "Người tạo / Ngày tạo" nhồi chung ô | Tên là link mở modal; Người tạo / Ngày tạo tách cột riêng |
| Hành động | 3 nút `<button class="btn btn-light">` tự dựng, inline style 8 dòng/nút | `V2BaseRowActions`, bỏ "Xem" |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Cột Hành động |
| Trạng thái | `v-html` + `status-pill` + `escapeHtml` | `V2BaseBadge` |
| Cấu hình cột / giữ bộ lọc | không có | `columnCustomizationMixin` + `filterStateMixin` |
| Xuất Excel | tải thẳng, `$nuxt.$loading`, file `.xls` | Popup chọn trường + `$safeLoading` + `.xlsx` |
| Sort | BE whitelist chỉ có `updatedAt` | Tên / Ngày tạo / Ngày cập nhật |
| Bề rộng cột | 3 cột có width, còn lại thả nổi | `fixed-layout` + `width`/`minWidth` đủ 10 cột (tổng 1542px) |
| Ô rỗng | in `—` | Để trống |
