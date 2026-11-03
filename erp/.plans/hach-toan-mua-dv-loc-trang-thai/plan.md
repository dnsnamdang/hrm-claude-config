# Hạch toán mua dịch vụ: kế toán lưu nháp nhưng không thấy phiếu + ô lọc Trạng thái sai

Không Redmine · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 03/11/2026 (@junfoke)
- [x] 03/11/2026 — Hỗ trợ: "kế toán lưu phiếu hạch toán nhưng sang DS Hạch toán mua DV không thấy để sửa". Dữ liệu prod phiếu 67 (EG.HTMDV.2026000067) đúng: Đang tạo, người lập Phạm Quế Nương; người tìm là Nguyễn Hải Yến → đúng thiết kế, phiếu nháp chỉ người lập thấy/sửa. Gửi user mô tả logic hiện tại (nháp / đã duyệt theo quyền tổng công ty-công ty / nút Sửa-Xóa) để hỏi lại nghiệp vụ.
- [x] 03/11/2026 — Lỗi tìm ra khi kiểm: ô lọc Trạng thái DS Hạch toán mua DV lấy nhầm trạng thái của phiếu YC (5 trạng thái) → đổi sang `BuyServiceAccounting::STATUSES` (Đang tạo / Đã duyệt). Commit `2397f6bddd`.
- [ ] Chờ user chốt có cho người khác xem/sửa phiếu nháp không.
