# Fix: Xuất Excel BC tổng hợp đi giao việc/công tác rất chậm

- Người phụ trách: @khoipv
- Bắt đầu: 18/11/2026
- Màn: `/timesheet/report/business_trip_assign_report_` (client `pages/timesheet/report/business_trip_assign_report_.vue`)
- API: `GET timesheet/reports/business_trip_assign_report_` → `BusinessTripAssign::searchByFilter` / `JobAssignmentNote::searchByFilter`

## Nguyên nhân
- FE đã dùng ExcelJS (commit `610f831d`), nhưng gọi API tuần tự từng trang 200 dòng.
- Mỗi lần gọi API, BE:
  1. `$query->get()` lấy TẤT CẢ phiếu khớp bộ lọc (kèm eager load NV + phòng ban) rồi mới cắt trang trong bộ nhớ (`forPage`).
  2. Lấy TOÀN BỘ chấm công của MỌI phiếu công tác/giao việc từ trước tới nay (không lọc theo phiếu/thời gian).
  3. Ghép bằng `Collection::where()` quét toàn bộ tập chấm công cho từng NV → O(NV × số lượt chấm).
- ⇒ Xuất N trang = lặp lại khối nặng N lần.

## Phase 1 — Sửa
### BE
- [x] `BusinessTripAssign::searchByFilter`: phân trang ở DB (`paginate`), chỉ lấy chấm công của các phiếu thuộc trang hiện tại, group theo `job_id`
- [x] `JobAssignmentNote::searchByFilter`: tương tự
- [x] Giữ nguyên format response (`data`, `total`, ... của LengthAwarePaginator) + format `business_timesheet` (`checkin`, `place`)
### FE
- [x] `exportEx`: tăng limit/trang 500, gọi các trang còn lại song song (tối đa 3 request cùng lúc), giữ thứ tự dòng
- [x] Thêm khóa sắp xếp phụ `id desc` để phân trang DB không trùng/sót dòng khi cùng thời gian
### DB
- [x] Migration `Modules/Timesheet/Database/Migrations/2026_11_18_100000_add_job_indexes_for_business_trip_assign_report.php` — index `timesheets(job_type, job_id)`, `job_assignment_note_details(job_assignment_note_id, created_at)`, `job_assignment_employees(job_assignment_note_id)`; đã chạy local
- [x] Kiểm tra cú pháp (php -l) + đo thời gian local

## Kết quả đo local (khoảng 2025-01-01 → 2026-12-31)
| | Cũ (200 dòng/trang) | Mới, chưa index (200) | Mới + index (500) |
|---|---|---|---|
| Phiếu công tác (4353 phiếu) | 16–18s/trang × 22 trang | 0.4–4.7s | ~0.25s/trang × 9 trang |
| Phiếu giao việc (1360 phiếu) | ~4.8s/trang | ~3s | ~0.25s/trang × 3 trang |
Tổng/ số lượt chấm mỗi trang khớp với code cũ.

### Checkpoint — 18/11/2026
Vừa hoàn thành: sửa BE (phân trang DB + chỉ lấy chấm công của trang) + migration index + FE gọi song song 3 request, 500 dòng/trang
Đang làm dở: —
Bước tiếp theo: đã push API `0f4198fa`, client `2370f6d3` (master) — deploy cả 2 + `php artisan migrate`, test tay xuất Excel
Blocked:

