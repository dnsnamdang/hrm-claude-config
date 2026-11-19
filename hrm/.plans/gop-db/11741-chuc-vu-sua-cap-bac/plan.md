# Plan — #11741 DM chức vụ: cảnh báo khi sửa cấp bậc

## Phase 1 — BE
- [x] Service: hàm tìm ảnh hưởng khi đổi cấp bậc (QĐ định biên hiệu lực / phòng đã định biên / QĐ quy chế lương đang dùng) theo cấu hình
- [x] store(): khi sửa + cấp bậc đổi + có ảnh hưởng + chưa `confirmed` → trả về cờ cần xác nhận + message; `confirmed` → lưu + QĐ định biên chuyển status 8 trong transaction
## Phase 2 — FE
- [x] working-position-modal: nhận phản hồi cần xác nhận → `$confirm` → gửi lại kèm `confirmed`
## Phase 3 — Kiểm thử
- [x] Test 4 tổ hợp cấu hình + Có/Không trên local

### Checkpoint — 2026-10-16
Vừa hoàn thành: BE `WorkingPositionService::getRankChangeImpacts` + `WorkingPositionController::store` (need_confirm / confirmed, hết hiệu lực QĐ định biên trong transaction); FE `working-position-modal.vue` gọi `$confirm`. Đã chạy thử hàm BE trên local (3 nhánh câu cảnh báo ra đúng).
Đang làm dở: không
Bước tiếp theo: test end-to-end trên trình duyệt (bấm Xác nhận / Hủy, QĐ 004/2026/QĐĐB-TPE chuyển Hết hiệu lực)
Blocked:

### Checkpoint — 2026-10-16 (test)
Vừa hoàn thành: test trình duyệt (client :3041 + API :8041 chạy từ worktree) đủ 5 ca: không đổi cấp bậc / dùng QĐ+định biên (Hủy giữ nguyên, Xác nhận → QĐ 004/2026/QĐĐB-TPE "Hết hiệu lực", lọc trạng thái 7/8 đúng, định biên giữ) / dùng QĐ không định biên (chỉ cảnh báo QCL, QĐ không đổi) / không QĐ có định biên (liệt kê phòng) / không cả hai (lưu ngay). Dữ liệu local đã khôi phục nguyên trạng.
Đang làm dở: không
Bước tiếp theo: chờ user quyết lỗi có sẵn "lưu chức vụ không có cấp bậc" (rule list_ranks bị comment) + commit/push
Blocked:
