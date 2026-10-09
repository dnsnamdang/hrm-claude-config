# task_10533 — Chỉnh UI Cấu hình hệ thống (theo 4 ảnh)

Nhánh: task_10533. View: resources/views/common/configs/

## Trạng thái hiện tại
- Căn phải label form (text căn phải): ĐÃ CÓ `text-md-right` trên mọi tab (commit trước). Screenshot từ bản dev cũ.

## Tasks
- [x] Đổi tên tab "Danh mục" → "Hàng hóa" (edit.blade.php ~L17)
- [x] CSKH — bảng "Bảng tính công khoán": thêm cột STT + header in hoa (cskh.blade.php)
- [x] Test render (blade compile) + báo user về phần alignment đã có sẵn

### Checkpoint — 2026-07-14
Vừa hoàn thành: Đổi tab "Danh mục"→"Hàng hóa" (edit.blade L17); bảng công khoán CSKH thêm cột STT (<% $index+1 %>) + header in hoa/căn giữa (thead text-center text-uppercase). Blade compile OK.
Phát hiện: alignment "text căn phải" ĐÃ có sẵn `text-md-right` trên mọi tab (commit trước) → screenshot từ bản dev cũ chưa deploy.
Đang làm dở: (không). Chưa commit — chờ user.

### Checkpoint — 2026-07-14 (sửa lại theo phản hồi user)
User đính chính: label cần căn TRÁI (không phải phải — annotation ảnh ghi nhầm).
- [x] Bỏ `text-md-right` khỏi 22 label config (tabs/*.blade.php) → căn trái. Giữ 14 input `form-control text-right` (số/ngày căn phải).
Blade compile OK toàn bộ tab.
