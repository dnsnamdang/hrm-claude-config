# Chuẩn hoá màn Hạng mục dự án theo skill `list-page`

- **Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · **Ngày:** 2026-09-05
- **Màn:** `/assign/project_items` — `hrm-client/pages/assign/project_items/index.vue`
- Màn thứ 11 của đợt

## Phạm vi

FE đầy đủ theo `list-page` + `button-convention` + mục 15b, BE tối thiểu (whitelist sort, tên người
tạo, ô tìm nhanh, chữ trạng thái, popup chọn trường xuất Excel).
**KHÔNG làm lịch sử thay đổi.**

## Quyết định riêng

- **KHÔNG có cột Mã** — bảng `project_items` không có cột mã → cột định danh là **Tên hạng mục**
  (skill mục 3a), là `button.v2-cell-link` mở modal Xem, `sticky` + `locked`.
- **Giữ chọn nhiều dòng + Xóa hàng loạt** (chức năng thật của màn); ô chọn `sticky` + `locked`
  cùng nhóm với STT / Tên.
- `filters` bỏ 2 khoá `page` / `per_page`: phân trang do `pagination` giữ, để trong `filters` thì
  mỗi lần lật trang lại kích hoạt deep watcher và reset về trang 1.

## Hiện trạng lệch chuẩn (đã sửa)

| Điểm | Trước | Sau |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + 5 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Cột định danh | Tên + dòng phụ "Người tạo / Ngày tạo" nhồi chung ô | Tên là link mở modal; Người tạo / Ngày tạo tách cột riêng |
| Hành động | 3 nút `<button class="btn btn-light">` inline-style 8 dòng/nút | `V2BaseRowActions`, bỏ "Xem" |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Cột Hành động |
| Trạng thái | `v-html` + `status-pill` + `escapeHtml` | `V2BaseBadge` |
| Cấu hình cột / giữ bộ lọc | không có | `columnCustomizationMixin` + `filterStateMixin` |
| Xuất Excel | tải thẳng, `.xls` | Popup chọn trường + `$safeLoading` + `.xlsx` |
| Sort | BE whitelist chỉ có `updatedAt` | Tên / Ngày tạo / Ngày cập nhật |
| Ô tìm nhanh | chỉ tên | thêm người tạo (`EXISTS`) |
| Bề rộng cột | 2 cột có width, còn lại thả nổi | `fixed-layout` + `width`/`minWidth` đủ 10 cột (1542px) |
| Ô rỗng | in `—` | Để trống |
