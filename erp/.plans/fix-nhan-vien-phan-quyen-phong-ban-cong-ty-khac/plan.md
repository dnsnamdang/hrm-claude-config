# Sửa nhân viên: phân quyền công ty hiện phòng ban của công ty khác

Không Redmine (prod `admin/employees/1239/edit`) · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 30/10/2026 (@junfoke)
- [x] 30/10/2026 — Xử lý: khối phân quyền công ty EG hiện phòng của công ty khác — ô "Quản lý các phòng" (và "Quản lý các bộ phận") lấy phòng của mọi công ty. Lọc theo công ty của khối ở `common/employees/edit.blade.php` + `create.blade.php`; giá trị đã chọn từ trước thuộc công ty khác vẫn hiện để lưu không mất dữ liệu; không sửa hàm lấy phòng ban dùng chung. Kiểm local NV 146 (5 công ty): khối SG còn 18/64 phòng; thêm công ty mới đổi danh sách đúng. Commit `0ea3732ec1` — đã lên gop_db + develop_02.
