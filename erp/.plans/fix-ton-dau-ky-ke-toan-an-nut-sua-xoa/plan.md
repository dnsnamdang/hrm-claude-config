# Tồn đầu kỳ kế toán: danh sách hiện Sửa/Xóa ở dòng đã khoá (chị Hải Yến báo "không có quyền")

Không Redmine · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 03/11/2026 (@junfoke)
- [x] 03/11/2026 — Hỗ trợ phân quyền màn Khai báo tồn hàng đầu kỳ kế toán (`warehouse/beginning_accounting_stocks`): vào màn + thêm/sửa/xoá/nhập-xuất Excel dùng chung 1 quyền "Kế toán kho" (nhóm "Kế toán" — khác quyền cùng tên của HRM); phạm vi do 2 quyền "Xem khai báo tồn kho kế toán theo tổng công ty / theo công ty". Phát hiện lỗ hổng: không có quyền phạm vi nào thì thấy tất cả công ty, màn sửa không kiểm công ty — chưa sửa, chờ user đồng ý.
- [x] 03/11/2026 — Xử lý: chị Hải Yến bấm Sửa dòng ETGN-EG-EQ4101-26 (kho EG_LN04) báo "không có quyền" dù thấy nút. Nguyên nhân: dòng bị khoá vì thủ kho đã khai tồn đầu (id 10687, 13/10/2026), nhưng danh sách không lấy kho thực tế + công ty của kho kế toán nên luôn hiện nút Sửa/Xóa. Sửa `BeginningAccountingStock` (danh sách lấy đủ cột). Gửi SQL user chạy prod xác nhận. Commit `d04f9e14f8`.
- [ ] Đổi câu "không có quyền" thành lý do khoá rõ ràng; bịt lỗ hổng phạm vi công ty — chờ user.
