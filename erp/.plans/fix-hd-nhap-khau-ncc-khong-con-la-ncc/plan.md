# HĐ nhập khẩu: danh sách lỗi "No query results for model Supplier"

Không Redmine (user gửi ảnh lỗi cổng dev) · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 04/11/2026 (@junfoke)
- [x] 04/11/2026 — Xử lý lỗi màn Danh sách hợp đồng nhập khẩu báo "No query results for model Supplier 232905": cột Nhà cung cấp tìm bằng `Supplier::findOrFail` (chỉ khách có `is_supplier = 1`), có HĐ trỏ vào khách không còn là NCC ⇒ cả bảng không tải. Đổi sang `find`: có NCC thì hiện "mã - tên", không có thì hiện `supplier_name` lưu trên HĐ (giống `BuyServiceContractController`). File `BuyContract2Controller.php`. Commit `18b2b30792`, đã lên `origin/gop_db`. Local không có bản ghi gây lỗi nên chưa thấy chạy thật.
