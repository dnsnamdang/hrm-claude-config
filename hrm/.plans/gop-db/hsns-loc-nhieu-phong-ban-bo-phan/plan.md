# Danh sách HSNS: lọc nhiều phòng ban / bộ phận + xuất Excel theo bộ lọc (chưa có số Redmine) — @junfoke

Màn `/human/employee_info`. Làm trên `develop`, mỗi repo 1 commit để cherry-pick sang prod (`gop_db`).

## Ngày 18/11/2026 (@junfoke)
- [x] 18/11/2026 — BE: controller (danh sách + 2 đường xuất Excel) nhận thêm 2 tham số mảng phòng ban / bộ phận; vẫn nhận tham số chọn một cũ nên màn Nhân sự nghỉ việc (dùng chung modal xuất + API) không ảnh hưởng.
- [x] 18/11/2026 — FE: ô Phòng ban, Bộ phận thành droplist chọn nhiều kiểu ô Chức vụ (chip, tìm, checkbox, Xóa tất cả), ngay sau ô Công ty; kế thừa PB theo công ty, BP theo PB đã chọn, đổi công ty / bỏ PB tự bỏ lựa chọn không còn thuộc. Không sửa component lọc dùng chung (~290 màn) — chỉ tắt 2 ô chọn một của nó trên màn HSNS. Modal xuất Excel gửi kèm 2 bộ lọc ở cả 2 đường (có / không cột Ảnh).
- [x] 18/11/2026 — Kiểm local: 2 PB = 33 người (22 + 11), 2 BP = 76 (46 + 30); `export-rows` 2 PB = 33 dòng, không lọc 404 dòng. Bắt + sửa lỗi đổi sang công ty không có bộ phận vẫn giữ bộ phận cũ. Đã xem ảnh giao diện.
- [x] 18/11/2026 — Commit develop api `4321f62c2`, client `65601f328` (đã push).
- [ ] Cherry-pick sang `gop_db` local (api `b2b2b7add`, client `a614c457f`) CHƯA push, chờ user xác nhận. Lưu ý: `origin/gop_db` hiện đã chứa commit gốc (qua merge develop) → kiểm lại trước khi push để khỏi đẩy trùng.
