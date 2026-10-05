# Bổ sung 05/10/2026 — cột Loại thành số + popup theo loại; NV tham gia thành số + popup NV

User yêu cầu 05/10, chốt 3 câu + nói "làm" (phạm vi gọn: 2 popup mới KHÔNG có In/Excel — user xác nhận "click nhầm phương án"
In/Excel). Nhánh `gop_db-mbe-loc-trang-thai` ở cả 2 repo (worktree `websites/wt-update-style-mbe`; client đã có commit e7e7e5fb0 ô
lọc Trạng thái; api tách từ origin/gop_db 9696baa26). Không migration/seeder.

## Quyết định đã chốt

| # | Chốt |
|---|---|
| B1 | Cột **Loại meeting** ở dòng Công ty / Phòng / NV / TỔNG: chỉ hiện **số loại** ("n loại", DrillNum bấm được). Dòng meeting giữ tên loại. |
| B2 | Bấm → popup **"Meeting theo loại"**: cột Loại · Hoàn thành · Đã hủy · Tổng, dòng TỔNG cuối; mỗi số bấm được → popup danh sách meeting đúng `meeting_type_id` (+ `status`). Nhóm chưa có loại = "Chưa phân loại" gửi `meeting_type_id=0`. Dữ liệu có Chốt lịch (lịch tương lai) thì thêm cột Chốt lịch, không có thì ẩn. |
| B3 | Popup danh sách meeting: cột **Nhân viên tham gia** chỉ hiện **số người**, bấm → popup **"Nhân viên tham gia"**: STT · Nhân viên (mã phụ) · Phòng ban · Chức vụ (hồ sơ) · Vai trò trong meeting. NV thuộc phạm vi đang xem in đậm (#14). |
| B4 | Hai popup mới chỉ có nút **Đóng** (không In/Excel). |
| B5 | File In/Excel của bảng cây và danh sách meeting GIỮ ĐẦY ĐỦ như cũ (tên NV tham gia; "n Loại · n Loại"). Chỉ màn hình đổi. |

## Phạm vi kỹ thuật

**hrm-api** — chỉ `Modules/Assign/Services/Report/MeetingByEmployeesReportService::companyMembers()`: mỗi NV trả thêm
`department_name`, `position` (working_positions qua `i.employee_work_position_id`, như `leaves()`), `role` (`me.role`). Thêm assert vào
`tests/Feature/MeetingByEmployees/DrillApiTest.php`. Export / blade KHÔNG đổi (B5).

**hrm-client** (`pages/assign/report/meeting-by-employees/`), không gọi endpoint mới:
- `components/MeetingTree.vue`: ô Loại dòng cha = DrillNum "n loại" (số mục trong `totals.by_type`, kể cả Chưa phân loại), emit
  `drill-types({ scope_*, title })`.
- `components/TypeBreakdownModal.vue` (V2BaseReportModal, khuôn `EmployeeListModal`): lấy dòng từ `item-list` của scope đó (vòng lặp 500/trang
  như các popup khác), gom theo `type_id` × `status` (đếm meeting không trùng); số = DrillNum → mở popup meeting với `meeting_type_id`
  (0 = chưa phân loại) + `status`. Tổng theo loại phải khớp ô "n Loại" của cây/khối tổng hợp.
- `components/MeetingListModal.vue`: cột NV tham gia = DrillNum số người (`row.employees.length`), emit `open-employees(row)`; Excel/In
  của popup giữ nguyên.
- `components/MeetingEmployeesModal.vue` (V2BaseReportModal): hiển thị `row.employees` (không gọi API); in đậm `in_scope`; chỉ nút Đóng.
- `index.vue`: wiring + z-order popup chồng popup đúng (khuôn panel `above-modal`).
- e2e (ngoài git): thêm ca vào `e2e/tests/assign/meeting-by-employees.spec.ts`, chỉ viết.

## Kết quả (05/10/2026)

Code xong: api `2197200a7` · client `bd96d6756` (cùng `e7e7e5fb0` ô lọc Trạng thái) trên nhánh `gop_db-mbe-loc-trang-thai` — ĐÃ MERGE + PUSH gop_db 05/10 (api 60aa9bfa0 · client 81b715269).
PHPUnit `tests/Feature/MeetingByEmployees` 41/41. Playwright đo khớp (popup loại = cây ở 5 dòng; NV tham gia 21 = 21 dòng; z-index chồng đúng).
Review: Approved. Minor để sau: TỔNG popup loại tải cả item-list (nên thêm by_type×by_status vào totals khi dữ liệu lớn); ẩn STT dòng TỔNG bằng
CSS `:has()`; cột Chốt lịch chưa thấy trên dữ liệu thật (chưa có lịch tương lai). e2e ca 13–14 đã viết, chưa chạy.
