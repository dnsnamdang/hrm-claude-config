# Fix: Chức vụ "luôn đủ công HC (PCT kỹ thuật)" chấm 1 lần vẫn đủ công — @manhcuong

Tester chốt (19/10/2026): chức vụ trong danh sách phải có ≥ 2 lượt chấm trong ngày mới gán đủ công của ca; 1 lượt → tính giờ thật. Phát hiện ở PCT-14321, Nguyễn Hoàng Sơn ngày 15/10/2026.

## Phase 1
### BE
- [x] `TimesheetSummaryService` nhánh PCT kỹ thuật: điều kiện đủ công thêm `số lượt chấm (khác giờ) >= 2`
- [x] Sửa giờ âm thành dương: kiểm `checkout < checkin` SAU khi cắt theo khung giờ phiếu (1 lượt 08:01 ra 0,48h → 0)
- [x] Test local (dữ liệu PCT thật, rollback): 7/7 PASS; code cũ FAIL 4 case tương ứng
- [x] Commit + push `gop_db`, deploy prod (2aab77e6c, 19/10/2026) — cron 21:00 tự tính lại từ đầu tháng
