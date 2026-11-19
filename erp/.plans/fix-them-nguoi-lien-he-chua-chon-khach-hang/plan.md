# Fix "Đã có lỗi xảy ra" khi thêm người liên hệ mà chưa chọn khách hàng — @junfoke

Repo `TanPhatDev`, nhánh `gop_db`. Modal người liên hệ dùng chung (giao việc khác, YC lắp đặt, báo giá DV, YC BH sửa chữa).

## Nguyên nhân
Phiếu chưa chọn khách hàng → bấm tìm người liên hệ → Thêm mới → Lưu: request thiếu `customer_id`; validator dùng chung
`uniqueContactPhoneFast` (`AppServiceProvider.php:78`) đọc thẳng `$contact['customer_id']` → Undefined index → 500.

## Ngày 02/11/2026 (@junfoke)
- [x] 02/11/2026 — Xử lý lỗi ERP (ảnh user gửi): BE validator đổi `$contact['customer_id'] ?? null` → trả lỗi validate "Bắt buộc phải nhập" thay vì 500; FE `partials/modals/js/searchContactJs.blade.php` + bản copy `customercare/warranty_requests/searchContactJs.blade.php` chặn mở modal khi chưa có khách, báo "Vui lòng chọn khách hàng trước".
- [x] 02/11/2026 — Test ERP local (Phiếu YC giao việc khác): 4 ca đạt. Commit `91634bbcf9` (gop_db, đã lên origin). Màn YC bảo hành (bản copy) chưa bấm thử.
