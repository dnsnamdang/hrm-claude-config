# Fix xem chi tiết Đề nghị nhập kho / xuất kho báo "không có quyền" dù thấy trong danh sách — @junfoke

Repo `TanPhatDev`, nhánh `gop_db`. Báo lỗi: chị Hải Yến (EG) có đủ quyền xem nhưng bấm vào phiếu ĐN nhập kho bị chặn.

## Nguyên nhân
Danh sách lọc theo 4 quyền phạm vi (tổng công ty / công ty / phòng ban / bộ phận) + thủ kho + người tạo, còn `canView()` của màn chi
tiết chỉ cho thủ kho của kho đó hoặc người lập.

## Ngày 02/11/2026 (@junfoke)
- [x] 02/11/2026 — `WarehouseImportRequest::canView()` viết lại khớp điều kiện danh sách (người lập; phiếu đang tạo chỉ người lập; thủ kho; tổng công ty; công ty; phòng ban/bộ phận mình hoặc mình quản lý). Kiểm local: quyền công ty/tổng công ty 0/30 → 30/30, không mở rộng ngoài danh sách.
- [x] 02/11/2026 — Theo user chỉ sửa thêm đúng màn Đề nghị xuất kho (không lan ~30 model máy quét nghi ngờ): `WarehouseExportRequest::canView()` giữ 4 điều kiện cũ + thêm nhánh tổng công ty / công ty / phòng ban. Chỉ `php -l` (phép kiểm dữ liệu chạy quá lâu, đã dừng).
- [x] 02/11/2026 — Commit `07cc5e2d66` "fix xem chi tiết" (gop_db, đã lên origin).
