# Điều tra: đơn kết thúc nghỉ sớm của Nguyễn Thị Lý không hiện ở "Duyệt dự kiến kết thúc nghỉ phép" — @cuong61n

Nguồn: tin nhắn hỗ trợ 10/11/2026 (chị Huyền HCNS báo không thấy đơn), PROD hrm.eteksofts.com, nhánh gop_db.

## Tasks
- [x] 10/11/2026 — Tra PROD (`hrm_erp_gop`): đơn KTNS id 70 đã lưu đúng (đơn nghỉ 12000, dự kiến kết thúc 11/11/2026 17:30, trạng thái Chờ duyệt, tạo 10/11/2026 09:09). Không mất dữ liệu.
- [x] 10/11/2026 — Nguyên nhân: chị Lý thuộc công ty ETEK (company 8, P. Kinh doanh id 120); người xem (Nguyễn Thị Thu Huyền, id 867) đang ở công ty Tân Phát (company 1) và không quản lý phòng nào của ETEK. Màn danh sách (`AttendancesExtendRequestService::index`) lọc `company_id = công ty hiện tại` + phòng ban mình quản lý trong công ty đó → đơn ETEK không hiện. Nhánh quyền `don_xin_nghi_nshc.approve` trong hàm này đang để trống (code cũ), nên quyền duyệt NSHC không mở rộng phạm vi.
- [x] 10/11/2026 — Người thấy được đơn: Trịnh Thị Trang (id 1060, ETEK, quản lý P.KD 120, có quyền duyệt đơn nghỉ công ty 8 — cũng là người đã duyệt đơn nghỉ 12000). Nguyễn Thị Duyên / Nguyễn Trung Phong có quản lý P.KD 120 nhưng công ty hiện tại là Tân Phát nên cũng không thấy.
- [ ] Chờ user chốt: hướng dẫn chị Trang duyệt (đúng luồng hiện tại) hay sửa code cho HCNS (quyền NSHC) xem/duyệt đơn KTNS liên công ty.

Trạng thái: đã điều tra xong, chưa sửa code.
