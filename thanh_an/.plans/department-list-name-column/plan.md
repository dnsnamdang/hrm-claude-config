# Bỏ mã công ty khỏi cột "Tên phòng ban" — Danh mục phòng ban

**Người phụ trách:** @khoipv
**Ngày:** 18/09/2026

## Mục tiêu
Cột "Tên phòng ban" ở màn Danh mục phòng ban (HCNS) đang hiện `Tên phòng - Mã công ty`.
Yêu cầu: chỉ hiện tên phòng.

## Phạm vi
- Chỉ sửa BE (transformer). FE không đổi vì `index.vue` render thẳng `item.name`.
- Cột "Mã" giữ nguyên `mã phòng - mã công ty` (user chỉ yêu cầu cột tên).
- Xuất Excel đi đường khác (`DepartmentService` select `company_code` riêng) → không ảnh hưởng.

## Task
### Phase 1 — Backend
- [x] Sửa `Modules/Human/Transformers/DepartmentResource/DepartmentListResource.php:29`
      `'name' => $data->name . ' - ' . $data->company->code` → `'name' => $data->name`

### Phase 2 — Kiểm thử
- [ ] Mở màn Danh mục phòng ban: cột Tên phòng ban chỉ hiện tên phòng
- [ ] Cột Mã, bộ lọc, sort theo tên, Xuất Excel không đổi

## Ghi chú
- `DepartmentListResource` (Human) chỉ được dùng ở đúng `DepartmentController@index` → không có downstream khác.
- Bỏ `$data->company->code` cũng tránh lỗi 500 khi phòng ban không gắn công ty.
