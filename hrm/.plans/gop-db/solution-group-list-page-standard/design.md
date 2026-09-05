# Chuẩn hoá màn Nhóm giải pháp theo skill `list-page`

- **Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · **Ngày:** 2026-09-05
- **Màn:** `/assign/solution-groups` (bảng `industries`) — `hrm-client/pages/assign/solution-groups/index.vue`
- Màn thứ 9 của đợt

## Phạm vi

FE đầy đủ theo `list-page` + `button-convention` + mục 15b, BE tối thiểu (whitelist sort, tên người
tạo, ô tìm nhanh, chữ trạng thái, cờ xóa, popup chọn trường xuất Excel).
**KHÔNG làm lịch sử thay đổi.**

## Hiện trạng lệch chuẩn (đã sửa)

| Điểm | Trước | Sau |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + 6 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Cột định danh | 1 cột gộp `Mã - Tên`, chứa luôn 3 nút thao tác | Tách `Mã` (button `.v2-cell-link` mở modal Xem) / `Tên` |
| Hành động | 3 nút trong cột gộp, disable + tooltip | Cột "Hành động" cuối, `V2BaseRowActions`, bỏ "Xem", ẩn thay vì disable |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Cột Hành động; lý do bị chặn đưa vào `title` badge |
| Trạng thái | `v-html` + `status-pill` tự dựng | `V2BaseBadge` |
| Người tạo / Ngày tạo | Là dòng phụ trong cột gộp, ngày format ở FE | Cột riêng, BE trả `d/m/Y H:i` |
| Điều kiện Xóa | FE tự suy từ `applications_count > 0` | Cờ BE `is_can_delete` (`isCanDelete()` đã có sẵn nhưng Resource KHÔNG trả) |
| Cấu hình cột / giữ bộ lọc | không có | `columnCustomizationMixin` + `filterStateMixin` |
| Xuất Excel | tải thẳng, `.xls` | Popup chọn trường + `$safeLoading` + `.xlsx` |
| Sort | BE whitelist chỉ có `updated_at` | Mã / Tên / Ngày tạo / Ngày cập nhật |
| Ô tìm nhanh | chỉ mã + tên | thêm người tạo (`EXISTS`) |
| Bề rộng cột | không khai gì | `fixed-layout` + `width`/`minWidth` đủ 12 cột (2018px) |
| Link "Số ứng dụng" | `<a href target="_blank">` | `nuxt-link` + `.v2-cell-link` |
| Ô rỗng | in `—` | Để trống |
