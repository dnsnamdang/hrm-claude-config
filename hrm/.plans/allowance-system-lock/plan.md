# Plan — Khóa sửa/xóa phụ cấp hệ thống (allowance)

Phụ trách: @khoipv

## Bối cảnh
Màn `human/allowance` có cờ `is_not_change` để khóa phụ cấp do hệ thống tự sinh (hiện tại: "Phụ cấp kiêm nhiệm" `PC_KN`). Tuy nhiên:
- DB thực tế `PC_KN` đang `is_not_change = 0` → chưa bị khóa (migration `add_pckn` set giá trị nhưng `is_not_change`/`status` không nằm trong `$fillable` nên bị mass-assignment bỏ qua).
- FE đang **ẩn** nút thay vì disable.
- BE không chặn update/delete theo cờ.

## Yêu cầu
- FE: **disable** nút Sửa/Xóa khi `is_not_change = 1` (thay vì ẩn).
- BE: chặn update (store có id) và delete khi `is_not_change = 1`.
- Giữ `is_not_change` NGOÀI `$fillable` để người dùng không tự gửi cờ khóa.
- Fix dữ liệu `PC_KN` về `is_not_change = 1` bằng migration (query builder).

## Tasks

### BE
- [x] Migration data-fix: set `is_not_change = 1` cho `PC_KN` qua query builder
- [x] `AllowanceController::store` — chặn update khi entity `is_not_change = 1` (trả HTTP 403)
- [x] `AllowanceController::delete` — chặn xóa khi entity `is_not_change = 1` (trả HTTP 403)

### FE
- [x] `human/allowance/index.vue` — đổi nút Sửa/Xóa từ `v-if` ẩn sang `:disabled` + tooltip giải thích

### Verify
- [x] Chạy migration, query lại DB xác nhận `PC_KN` = 1
- [x] Lint PHP controller + migration: no syntax errors
- [ ] Test FE thực tế: nút Sửa/Xóa của PC_KN bị disable (cần user kiểm tra trên trình duyệt)
