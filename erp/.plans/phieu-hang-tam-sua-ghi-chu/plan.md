# Phiếu yêu cầu duyệt hàng tạm — cho sửa GHI CHÚ khi Đang tạo

## Yêu cầu
Cho sửa **phiếu yêu cầu duyệt hàng tạm** (`TmpProductRequest`) khi phiếu ở trạng thái **Đang tạo** (`DANG_TAO=4`), và **chỉ sửa được ghi chú** (`note`). Sửa inline ngay trên trang Show. Không thêm permission riêng.

## Hiện trạng
- `status` là accessor suy diễn (`getStatusAttribute`): DANG_TAO khi toàn bộ sản phẩm con còn nháp.
- `note` là cột thật trên `tmp_product_requests`.
- Controller chưa có edit/update (chỉ index/show/store/searchData/print).
- Show page (`show.blade.php:26`): ô ghi chú `<input ng-model="form.note" disabled>` (Angular controller 'Sale').
- Response helper: `successResponse($msg,$data)` / `errorResponse($msg,$errors)` → `{success, message, ...}`.

## Thiết kế
- **BE guard cứng**: `updateNote` chặn nếu `status != DANG_TAO`; chỉ update `note`.
- **FE**: khi `$object->is_can_edit` (status==DANG_TAO) → bật ô ghi chú + nút "Lưu ghi chú" (AJAX). Ngược lại giữ `disabled`.

## Tasks
- [x] BE1: Model `TmpProductRequest` — thêm accessor `getIsCanEditAttribute()` = `status == DANG_TAO`
- [x] BE2: Route `POST tmp_product_requests/{id}/update-note` → `updateNote`
- [x] BE3: Controller `updateNote()` — guard canView + status==DANG_TAO, validate note, update note, `php -l` sạch
- [x] FE1: `show.blade.php` — ô ghi chú editable + nút "Lưu ghi chú" khi `is_can_edit`; thêm `$scope.saveNote()`
- [ ] User test trên dev: phiếu Đang tạo sửa được note; phiếu đã gửi/đang xử lý KHÔNG sửa được (nút ẩn + BE chặn)
- [x] FIX kèm: cột Trạng thái ở màn Show thiếu case "Đang tạo" (status=3) → thêm `<span ng-if="product.status == 3">Đang tạo</span>` (show.blade dòng ~72)

### Checkpoint — 2026-07-01
Vừa hoàn thành: BE (accessor is_can_edit + route + updateNote guard status==DANG_TAO, chỉ update note) + FE (show.blade bật ô ghi chú + nút Lưu ghi chú + saveNote AJAX). php -l sạch, route đăng ký OK.
Đang làm dở: không.
Bước tiếp theo: user test dev → commit.
Blocked:

## Nhánh
`sync_quotation`
