# Chuẩn hoá màn Lĩnh vực kinh doanh khách hàng theo skill `list-page`

- **Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · **Ngày:** 2026-09-05
- **Màn:** `/assign/customer-scopes` — `hrm-client/pages/assign/customer-scopes/index.vue`
- Màn thứ 4 sau [solutions](../solution-list-page-standard/design.md),
  [industry-groups](../industry-group-list-page-standard/design.md),
  [application](../application-list-page-standard/design.md)

## Phạm vi (giữ đúng như 3 màn trước)

FE đầy đủ theo `list-page` + `button-convention` + mục 15b (bề rộng cột), BE tối thiểu
(whitelist sort, tên người tạo, popup chọn trường xuất Excel). **KHÔNG làm lịch sử thay đổi.**

## Hiện trạng lệch chuẩn

| Điểm | Hiện tại | Chuẩn |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + `title` ghi trùng tên bảng bên dưới, 7 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Ô lọc gõ tay | Gõ 1 ký tự = 1 request | `textFilterKeys()` — chờ Enter / nút Tìm kiếm |
| Cột định danh | 1 cột gộp `Mã - Tên`, chứa luôn 3 nút thao tác | Tách `Mã` (button `.v2-cell-link` mở modal Xem) / `Tên` |
| Hành động | Xem / Sửa / Xóa nhét dưới tên, disable + tooltip | Cột "Hành động" cuối, `V2BaseRowActions`, bỏ "Xem", ẩn thay vì disable |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Chuyển sang cột Hành động |
| Trạng thái | `v-html` + `status-pill` tự dựng | `V2BaseBadge` `variant` brand/required |
| Người tạo / Ngày tạo | Là dòng phụ trong cột gộp | Cột riêng, bắt buộc |
| Cấu hình cột / giữ bộ lọc | không có | `columnCustomizationMixin` + `filterStateMixin` |
| Xuất Excel | tải thẳng cả bảng, `$nuxt.$loading` | Popup chọn trường + `$safeLoading` |
| Sort | BE whitelist chỉ có `updated_at` | Mã / Tên / Ngày tạo / Ngày cập nhật |
| Bề rộng cột | không khai gì | `fixed-layout` + `width`/`minWidth` đủ mọi cột theo 4 bậc (mục 15b) |
| Ô rỗng | in `—` | Để trống |

## Ghi chú riêng của màn

- **Nút Xóa không có cờ BE**: entity `CustomerScope` chỉ có `isCanEdit()` và `isCanLockUpdate()`
  (hàm sau luôn trả `true` — ứng dụng không còn liên kết lĩnh vực KH nữa). Bản cũ lấy nhầm
  `is_can_lock_update` làm điều kiện disable nút Xóa. Bản mới gate Xóa bằng đúng quyền `canManage`,
  còn ràng buộc nghiệp vụ để BE quyết khi gọi API.
- Cột "Loại hình hoạt động khách hàng" là chuỗi gộp nhiều nhóm (`groups.name` nối bằng dấu phẩy)
  → bậc L (260px) + `clamp-2` + `:title`.
