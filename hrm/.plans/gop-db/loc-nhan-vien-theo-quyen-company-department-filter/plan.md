# Bộ lọc Công ty/Phòng ban/Nhân viên: ô Nhân viên lọc theo quyền xem của màn

Không Redmine (user báo: quyền xem theo công ty EG mà ô Nhân viên hiện cả HN) · @junfoke · hrm-client nhánh `gop_db`

## Ngày 05/11/2026 (@junfoke)
- [x] 05/11/2026 — Xử lý lỗi hiển thị component dùng chung `CompanyDepartmentFilter.vue` (Đề nghị tra soát công, Đơn xin nghỉ…): Phòng ban / Bộ phận đã lọc theo quyền nhưng ô **Nhân viên** lấy từ `human/employee/getEmployeesForFilter` trả mọi công ty, FE chỉ lọc khi đã chọn công ty/phòng/bộ phận. Dữ liệu danh sách không bị lộ.
- [x] 05/11/2026 — Sửa: ô Nhân viên lọc theo quyền xem của màn, cùng quy tắc API danh sách — Tổng công ty: tất cả; Công ty: NV công ty được quyền; Phòng ban: NV thuộc phòng **hoặc** bộ phận mình quản lý; Bộ phận: NV bộ phận mình quản lý. Test local (Trịnh Thị Trang, EG, quyền tra soát công – công ty): ô Nhân viên còn 23 người (trước ~1.100), gõ "Văn Quang" chỉ ra Phạm Văn Quang (EG). Commit `50ea799f7` (đã lên origin gop_db + develop).
- [ ] Chưa thử màn Đơn xin nghỉ, tài khoản quyền phòng ban/bộ phận, và trên hrm.eteksofts.com.
