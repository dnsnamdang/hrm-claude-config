# Plan — Đề nghị thanh toán: không hiện tài khoản ngân hàng của khách hàng

**Người phụ trách:** @junfoke — 2026-10-29
Repo: `TanPhatDev`, nhánh `gop_db`

## Ngày 29/10/2026 (@junfoke)

- [x] 29/10/2026 — Loại chi "Chi trả lại khách hàng", hình thức CK: KH có từ 2 tài khoản thì phiếu không hiện tài khoản. Sửa: KH 1 tài khoản tự điền như cũ; từ 2 tài khoản hiện thêm ô "Tài khoản khách hàng" (số TK, chủ TK, ngân hàng), chọn sẵn tài khoản đầu, chọn tài khoản nào điền đúng tài khoản đó.
- [x] 29/10/2026 — Tên ngân hàng / chi nhánh trống ở tài khoản mới: `CustomersController::getDataCustomer` lấy từ danh mục ngân hàng + chi nhánh khi cột chữ trống (giống HRM; KH giờ chỉ quản lý ở HRM).
- [x] 29/10/2026 — Chạy thử trên ERP local (thêm tạm tài khoản thứ 2 cho KH 50TPHPTA-440, xong đã xoá), đã xem ảnh. Commit `65e5f1c7fa`, đã push `gop_db` (4 file).
