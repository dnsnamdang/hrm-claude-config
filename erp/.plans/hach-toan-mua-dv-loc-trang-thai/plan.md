# Hạch toán mua dịch vụ: kế toán lưu nháp nhưng không thấy phiếu + ô lọc Trạng thái sai

Không Redmine · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 03/11/2026 (@junfoke)
- [x] 03/11/2026 — Hỗ trợ: "kế toán lưu phiếu hạch toán nhưng sang DS Hạch toán mua DV không thấy để sửa". Dữ liệu prod phiếu 67 (EG.HTMDV.2026000067) đúng: Đang tạo, người lập Phạm Quế Nương; người tìm là Nguyễn Hải Yến → đúng thiết kế, phiếu nháp chỉ người lập thấy/sửa. Gửi user mô tả logic hiện tại (nháp / đã duyệt theo quyền tổng công ty-công ty / nút Sửa-Xóa) để hỏi lại nghiệp vụ.
- [x] 03/11/2026 — Lỗi tìm ra khi kiểm: ô lọc Trạng thái DS Hạch toán mua DV lấy nhầm trạng thái của phiếu YC (5 trạng thái) → đổi sang `BuyServiceAccounting::STATUSES` (Đang tạo / Đã duyệt). Commit `2397f6bddd`.
- [ ] Chờ user chốt có cho người khác xem/sửa phiếu nháp không.

## Ngày 04/11/2026 (@junfoke)
- [x] 04/11/2026 — Hỗ trợ check tiếp phiếu YC EG.YCHTMDV.2026000070 (người lập YC Nguyễn Thị Cẩm Ly): dữ liệu prod cho thấy 11:11 ngày 04/11 chị Phạm Quế Nương đã tự sửa phiếu nháp HT EG.HTMDV.2026000067 và hạch toán → YC 70 "Đã hạch toán", HT 67 "Đã duyệt". Không lỗi hệ thống; chị Nguyễn Hải Yến (1189) không thấy phiếu nháp là đúng thiết kế, nay đã duyệt thì thấy được nếu có quyền xem theo công ty/tổng công ty.
