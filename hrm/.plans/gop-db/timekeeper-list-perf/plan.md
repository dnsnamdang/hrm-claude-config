# Màn Dữ liệu chấm công (/timesheet/timekeeping/timekeeper) load chậm — @manhcuong

Nguyên nhân: mở màn không lọc ngày → API `GET timekeeper/` quét cả bảng `timesheets` (~821k dòng), join `employee_infos.ssn` (varchar, lệch kiểu với bigint) không dùng được index → count 6,6s + lấy trang 5,6s.

## Phase 1 — Sửa
- [x] DB prod: sao lưu 309.819 dòng `timesheets` trước 2025 (`~/backups/hrm/` + `hrm-prod:/home/erp_tpe/timesheets_before_2025_20261014.sql.gz`) rồi xoá theo lô 10k (14/10/2026)
- [x] BE `TimekeeperService::index`: không gửi khoảng ngày → mặc định 1 tháng gần nhất
- [x] FE `timekeeper/index.vue`: mặc định lọc "Từ" = đầu tháng khi ô ngày trống
- [x] Deploy prod (gop_db) 14/10/2026 — api 9cbe6d56b, client 381850e13
- [x] Fix lần 2 (14/10/2026): huỷ 7 câu count treo trên DB (~26 phút, client đã 504/499); join `titles` lồng trong join `employee_infos` làm MySQL bỏ hash join → đổi sang join phẳng (lọc 1 tháng 60s → 2,5s). Deploy api 8c924c4be
