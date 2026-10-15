# Fix: "Người nhận đơn hàng" trống ở màn Tạo yêu cầu đặt hàng

Nhánh: `gop_db` (ERP TanPhatDev)

## Bối cảnh / Root cause
- Màn `admin/orders/root_order_request/create`: ô "Người nhận đơn hàng" trống dù brand/hãng đã phân người phụ trách.
- `getDeputy()` đọc `assign_histories` bản ghi ĐANG MỞ (`employee_date_to IS NULL`) rồi lấy `buy_employee_id`. Bản đang mở (id 2305, Ruijun 1033 / JINAN 1048 / cty 1) có `buy_employee_id = NULL`.
- Nguyên nhân gốc: `AssignDepartmentBrandController::submitApprove()` (dòng 441-475) khi duyệt phiếu phân công PHÒNG BAN tạo bản ghi lịch sử mới với employee NULL (nhánh `department_type=3` null cả 2) và đóng bản ghi cũ (`employee_date_to=now()`), KHÔNG khôi phục người phụ trách từ phân công NHÂN VIÊN đang hiệu lực. Đổi phòng 95→46 (16/07) rồi 46→95 (25/09) làm NV 575 (Phạm Thị Diệu Linh) mất khỏi lịch sử đang mở, dù `assign_employee_manufactures` (id 2252) vẫn ghi NV 575 cho phòng 95.
- Phạm vi (read-only): 503 history đang mở thiếu NV, chỉ **1** bản khôi phục được (đúng phòng có phân công NV) = history 2305. Các bản còn lại là phân công phòng chờ phân NV (đúng thiết kế cảnh báo ở dòng 486-519).

## Task
- [x] T1 — Đọc & xác định root cause (read-only DB server, code review + Explore agent)
- [x] T2 — (B) Sửa `AssignDepartmentBrandController::submitApprove()`: thêm helper `resolveAssignedEmployeeForDepartment()` và khôi phục `brand_employee_id`/`buy_employee_id` cho bản ghi lịch sử mới khi phòng phụ trách mới vẫn có phân công NHÂN VIÊN đã duyệt hiệu lực. Không có thì để trống + giữ nguyên cảnh báo cũ. `php -l` OK.
- [x] T3a — (A) Thêm method `\UpdateDB::fixAssignHistoryMissingEmployee_20260925($dryRun=true)`. Dry-run trên server: quét 503 bản, khôi phục **1 bản** (hist 2305: brand/buy emp null→575), đã rollback.
- [x] T3b — Chạy ghi thật `(false)`: khôi phục hist 2305 (brand/buy emp → 575). Verify `getDeputy` trả "Phạm Thị Diệu Linh".
- [x] T4 — Commit B lên `gop_db` (`020e8ec30a` → rebase → push `cf0ff7826c`). UpdateDB.php (A) commit `f3ed52e6c8` push OK.

### Checkpoint — 2026-09-25
Vừa hoàn thành: A ghi thật (1 bản, verify OK), B commit+push gop_db (`cf0ff7826c`).
Đang làm dở: —
Bước tiếp theo: (tuỳ chọn) commit UpdateDB.php để lưu vết method fix; deploy B để ăn cho các phiếu về sau.
Blocked: —

## Ràng buộc
- Chỉ ĐỌC DB server `hrm_erp_gop`; A ghi thật chỉ khi user xác nhận.
- `submitApprove` là logic dùng chung → đã xin ý kiến, user chốt hướng B+A (khuyến nghị).
