# Dữ liệu mẫu đã tạo (DB local_hrm_erp của gop_db-api) — 02/10/2026

Dùng CHUNG cho 2 SRS: performance-by-employee + performance-by-solutions. Tạo bằng SQL: `performance-by-employee/seed.sql` (chỉ INSERT;
dòng copy cấu trúc từ bản ghi có sẵn: dự án 113, yêu cầu làm GP 15, giải pháp 24, hạng mục 3, nhiệm vụ 10).
Mục đích: kỳ mặc định của 2 báo cáo là THÁNG HIỆN TẠI (10/2026) mà DB chưa có dự án nào bắt đầu trong tháng 10.

| Bảng | id | Nội dung |
|---|---|---|
| prospective_projects | 148 | HN_DA.UD.0137.2026.DA020 — Cung cấp thiết bị thực hành điện – điện tử cho Trường CĐ Kỹ thuật Công nghiệp Bắc Giang (bắt đầu 01/10/2026, status 4) |
| prospective_projects | 149 | HN_DA.UD.0137.2026.DA021 — Trang bị xưởng thực hành ô tô – Trường CĐ nghề Việt Xô số 1 (bắt đầu 02/10/2026, status 9 → "Đã chốt" HĐ) |
| request_solutions | 31, 32 | TPE.YCP.TC.26.0091 / 0092 — phòng nhận 55 (PHÒNG DỰ ÁN) |
| solutions | 33, 34 | HN_DA.UD.0137.2026.DA020_GP01 (status 7, PM 781) / DA021_GP01 (status 17, PM 149) |
| solution_modules | 6, 7, 8, 9 | 2 hạng mục / giải pháp ("Xây dựng danh mục thiết bị", "Ốp bản vẽ móng máy"), leader 835 / 1142 / 781 / 148 |
| solution_module_members | 1, 2, 3, 4 | 148, 149, 835, 126 kèm vai trò |
| tasks | 15 – 24 | TPE.TASK.NB.26.0901 → 0910, người thực hiện 835, 148, 1142, 149, 781, 126; có giờ ước tính + giờ thực tế (cột actual_hours) |
| task_result_progress_logs | 5 – 14 | 1 dòng / nhiệm vụ 15–24, hours = giờ thực tế |

Sau khi chạy seed, đã chỉnh hạn (due_date) của chính các nhiệm vụ 15, 20, 21, 23 sang 02–03/10 để có số "Hoàn thành đúng hạn"
(seed.sql đã cập nhật theo giá trị cuối).

Gỡ dữ liệu (nếu cần):
DELETE FROM task_result_progress_logs WHERE task_id BETWEEN 15 AND 24;
DELETE FROM tasks WHERE id BETWEEN 15 AND 24 AND code LIKE 'TPE.TASK.NB.26.09%';
DELETE FROM solution_module_members WHERE id BETWEEN 1 AND 4;
DELETE FROM solution_modules WHERE id BETWEEN 6 AND 9;
DELETE FROM solutions WHERE id IN (33, 34);
DELETE FROM request_solutions WHERE id IN (31, 32);
DELETE FROM prospective_projects WHERE id IN (148, 149);
