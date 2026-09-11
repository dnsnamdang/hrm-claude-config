# Chuẩn hoá màn Danh mục loại tài liệu theo skill `list-page`

- **Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · **Ngày:** 2026-09-05
- **Màn:** `/assign/attachment-type` — `hrm-client/pages/assign/attachment-type/index.vue`
- Màn thứ 7 của đợt (solutions · industry-groups · application · customer-scopes · meeting_type · questions)

## Phạm vi

FE đầy đủ theo `list-page` + `button-convention` + mục 15b, BE tối thiểu (whitelist sort, tên người
tạo, ô tìm nhanh, chữ trạng thái, popup chọn trường xuất Excel). **KHÔNG làm lịch sử thay đổi.**

## Hiện trạng lệch chuẩn (đã sửa)

| Điểm | Trước | Sau |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + `title`/`subtitle` riêng, 6 ô hard-code | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Cột định danh | 1 cột gộp `Mã - Tên`, chứa luôn 3 nút thao tác | Tách `Mã` (button `.v2-cell-link` mở modal Xem) / `Tên` |
| Hành động | **Nút thao tác bị nhân đôi**: vừa nằm trong cột gộp `typeInfo`, vừa có cột `actions` riêng với 3 nút inline-style | 1 cột "Hành động" duy nhất dùng `V2BaseRowActions` |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Cột Hành động |
| Trạng thái | `v-html` + `status-pill` tự dựng | `V2BaseBadge` |
| Người tạo / Ngày tạo | Có cột nhưng chữ **in đậm** + icon rỗng `<i class="mr-1 text-muted">` | Cột chữ thường chuẩn (`.text-muted` là màu ĐỎ trong hệ thống này) |
| Cấu hình cột / giữ bộ lọc | không có | `columnCustomizationMixin` + `filterStateMixin` |
| Xuất Excel | tải thẳng, `$nuxt.$loading`, file `.xls` | Popup chọn trường + `$safeLoading` + `.xlsx` |
| Sort | whitelist chỉ nhận tên cột thô (`updated_at`/`created_at`/`id`) | Mã / Tên / Ngày tạo / Ngày cập nhật theo key cột FE |
| Bề rộng cột | không khai gì | `fixed-layout` + `width`/`minWidth` đủ 10 cột (1668px) |
| `metaSummary` | computed dựng 3 chỉ số nhưng **không nơi nào dùng** | Bỏ |

## Ghi chú riêng

- Thêm cờ **`is_can_edit`** ở Resource (`status === STATUS_ACTIVE`) để FE gate nút Sửa bằng cờ BE
  thay vì tự so `item.status === 2` ở 2 chỗ khác nhau như bản cũ.
- Giữ nguyên bước **hỏi lại máy chủ trước khi mở form Sửa** (bản ghi có thể vừa bị người khác khóa).
