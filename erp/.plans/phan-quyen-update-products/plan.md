# Fix — Phân quyền màn admin/products/update-products

## Yêu cầu
Màn `admin/products/update-products` đang không có phân quyền → phải yêu cầu quyền **"Sửa hàng hóa"**.

## Hiện trạng (routes/web.php)
- Dòng 618 GET `/update-products` → chỉ có `checkDueConfigs`, thiếu checkPermission.
- Dòng 620 POST `/start-update-products` (action chạy cập nhật) → không có middleware nào.

## Fix
- [x] GET `/update-products`: thêm `checkPermission:Sửa hàng hóa` (giữ `checkDueConfigs`).
- [x] POST `/start-update-products`: thêm `checkPermission:Sửa hàng hóa` (action ghi dữ liệu, gate luôn cho an toàn).
- [ ] User test: tài khoản KHÔNG có quyền "Sửa hàng hóa" → không vào được màn / không chạy được cập nhật.

### Checkpoint — 2026-06-11
Vừa hoàn thành: gắn checkPermission:Sửa hàng hóa cho 2 route update-products
Bước tiếp theo: user test phân quyền
Blocked:
