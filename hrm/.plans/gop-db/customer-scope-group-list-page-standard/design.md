# Chuẩn hoá màn Loại hình hoạt động khách hàng theo skill `list-page`

- **Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · **Ngày:** 2026-09-05
- **Màn:** `/assign/customer-scope-groups` — `hrm-client/pages/assign/customer-scope-groups/index.vue`
- Màn thứ 10 của đợt

## Phạm vi

FE đầy đủ theo `list-page` + `button-convention` + mục 15b, BE tối thiểu (whitelist sort, tên người
tạo, ô tìm nhanh, chữ trạng thái, cờ xóa, popup chọn trường xuất Excel).
**KHÔNG làm lịch sử thay đổi.**

## Hiện trạng lệch chuẩn (đã sửa)

| Điểm | Trước | Sau |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + 7 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Cột định danh | 1 cột gộp `Mã - Tên`, chứa luôn 3 nút thao tác | Tách `Mã` (button `.v2-cell-link` mở modal Xem) / `Tên` |
| Hành động | 3 nút trong cột gộp, disable + tooltip | Cột "Hành động" cuối, `V2BaseRowActions`, bỏ "Xem", ẩn thay vì disable |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Cột Hành động; lý do bị chặn đưa vào `title` badge |
| Trạng thái | `v-html` + `status-pill` tự dựng | `V2BaseBadge` |
| Người tạo / Ngày tạo | Là dòng phụ trong cột gộp | Cột riêng, BE trả `d/m/Y H:i` |
| Điều kiện Xóa | FE tự suy từ `customer_scopes_count > 0` | Cờ BE `is_can_delete` — **entity CHƯA có `isCanDelete()`**, đã bổ sung |
| Cấu hình cột / giữ bộ lọc | không có | `columnCustomizationMixin` + `filterStateMixin` |
| Xuất Excel | tải thẳng, `.xls` | Popup chọn trường + `$safeLoading` + `.xlsx` |
| Sort | BE whitelist chỉ có `updated_at` | Mã / Tên / Ngày tạo / Ngày cập nhật |
| Ô tìm nhanh | chỉ mã + tên | thêm người tạo (`EXISTS`) |
| Bề rộng cột | không khai gì | `fixed-layout` + `width`/`minWidth` đủ 11 cột (1838px) |
| Ô rỗng | in `—` | Để trống |

## Ghi chú

Entity `CustomerScopeGroup` trước đây chỉ có `isCanEdit()` + `isCanLockUpdate()`; luật "chỉ xoá khi
chưa có lĩnh vực kinh doanh trực thuộc" **chỉ tồn tại ở FE** (tự suy từ `customer_scopes_count`).
Đã đưa luật về entity (`isCanDelete()`) và trả qua Resource để BE là nguồn duy nhất.
