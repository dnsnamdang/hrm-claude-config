# Plan — Popup tìm hàng: tách nhãn "Loại hàng hóa" trùng nhau

## Phase 1 — FE modal dùng chung

- [x] Rà nguồn 2 ô lọc, xác nhận lọc 2 cột DB khác nhau (không phải ô thừa)
- [x] Kiểm tra BE đã hỗ trợ `product_types` (mảng) chưa — có sẵn `SearchController.php:573`
- [x] `searchProduct.blade.php`: ô đầu đổi nhãn "Tính chất hàng hóa" + `multiple` + `ng-model="search.product_types"`
- [x] `searchProductJs.blade.php`: khai `product_types: []`, gửi `d.product_types` (2 chỗ), reset (2 hàm)
- [x] Kiểm CRLF nguyên vẹn (`git diff --stat` = 2 file, +9/−3)
- [ ] User test browser: popup chọn hàng KM ở PI — chọn nhiều tính chất, bấm Tìm kiếm / Tất cả
- [ ] Commit sau khi user xác nhận

### Checkpoint — 11/09/2026
Vừa hoàn thành: sửa 2 file FE theo phương án A, diff tối thiểu, CRLF giữ nguyên.
Đang làm dở: không.
Bước tiếp theo: user test trên browser rồi commit.
Blocked: không.
