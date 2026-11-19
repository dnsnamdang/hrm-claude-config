# Danh mục chi phí — Kiểu "Chi phí phải trả" bắt nhập VAT mà không có ô (ERP) — @junfoke

Màn `admin/accounting/costs?kind_of=1` (chi phí luồng mua).

## Ngày 06/11/2026 (@junfoke)
- [x] 06/11/2026 — Xử lý lỗi: Kiểu "Chi phí phải trả" lưu bị bắt nhập VAT nhưng ô **% VAT** bị ẩn (ô VAT thêm từ 23/07/2025 commit "sua vat" chỉ cho hiện với "Chi phí kinh doanh", phần lưu thì bắt cả 2 kiểu; các chi phí phải trả cũ đều VAT = 8). Cho ô % VAT hiện ở cả 2 kiểu, vẫn bắt buộc. `resources/views/accounting/costs/index.blade.php`, commit `f10f16c882` (gop_db, đã push). Đã mở form trên ERP local, chưa bấm Lưu thử.
