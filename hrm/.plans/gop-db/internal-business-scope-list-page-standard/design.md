# Chuẩn hoá màn Lĩnh vực Công ty kinh doanh theo skill `list-page`

- **Người phụ trách:** @khoipv · **Nhánh:** `gop_db` · **Ngày:** 2026-09-05
- **Màn:** `/assign/internal-business-scopes` — `hrm-client/pages/assign/internal-business-scopes/index.vue`
- Màn thứ 8 của đợt

## Điểm khác các màn trước: BE đã chuẩn sẵn

`InternalBusinessScopeService` từ đợt trước đã có `SORTABLE_COLUMNS`, tìm theo người tạo bằng
`EXISTS`, **xếp theo độ khớp** (skill mục 3b), `status_text`, ngày `d/m/Y H:i`, đủ cờ `is_can_*`.
Nên BE lần này chỉ còn phần **xuất file theo cột user chọn**.

## Bug có thật phát hiện khi soát (không phải do lần sửa này)

`InternalBusinessScope::isCanLockUpdate()` viết cứng tiền tố bảng cũ:

```php
return $this->scopes()->where('scopes.status', Scope::STATUS_ACTIVE)->doesntExist();
```

Bảng nhóm ngành của HRM đã đổi tên thành **`hrm_scopes`** khi gộp DB (`scopes` là bảng của ERP)
→ mọi lần đọc bản ghi nổ **500 `Unknown column 'scopes.status'`**, và vì `Resource` gọi hàm này nên
**cả màn danh sách chết** với người có quyền xem. (Tài khoản test không có quyền nên trả 403 trước,
che mất lỗi.) Đây là cùng họ lỗi với `ScopeService` đã sửa ở màn Nhóm ngành.
→ Sửa: lấy tên bảng từ chính model (`$this->scopes()->getModel()->getTable()`), không viết cứng.

## Hiện trạng lệch chuẩn (đã sửa)

| Điểm | Trước | Sau |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + 7 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields` |
| Ô lọc gõ tay (Mã / Tên) | Gõ 1 ký tự = 1 request | `textFilterKeys()` — chờ Enter / nút Tìm kiếm |
| Cột Hành động | Dùng renderer `type: 'actions'` dựng sẵn trong `V2BaseDataTable` | `V2BaseRowActions` (component dùng chung, có menu `⋮` khi > 3 nút) |
| Cấu hình cột / giữ bộ lọc | không có | `columnCustomizationMixin` + `filterStateMixin` |
| Xuất Excel | tải thẳng cả bảng | Popup chọn trường (giữ cách tải TRỰC TIẾP vì blob hỏng trên Safari/webview) |
| Bề rộng cột | cột Tên thiếu `width` | `fixed-layout` + `width`/`minWidth` đủ 10 cột (1578px) |
| Cột "Số nhóm ngành" | BE trả `scopes_count` nhưng bảng KHÔNG hiện | Thêm cột (căn phải) |
| Ô rỗng | in `—` (5 chỗ) | Để trống |
| Chữ | `Khoá` / `Xoá` | `Khóa` / `Xóa` (bảng text chuẩn), gồm cả `status_text` ở BE |
| Nút | Import trắng, Xuất trắng | Import cam + `ri-upload-line`, Xuất xanh lá, `:interactable` |
