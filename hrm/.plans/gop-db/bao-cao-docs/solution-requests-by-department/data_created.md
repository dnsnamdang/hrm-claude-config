# Dữ liệu tạo thêm cho SRS "Báo cáo Theo dõi YCLGP theo phòng KD" (DB local_hrm_erp, nhánh gop_db)

Tạo bằng SQL ngày 02/10/2026. Không sửa/xoá dữ liệu có sẵn.

## request_solutions (10 dòng) — id 21–30
- Mã `TPE.YCP.TC.26.0901` … `TPE.YCP.TC.26.0910`
- `created_by = 13` (DNS Admin, phòng CTV_NV id 111), `company_id = 1`, `department_id = 111`
- Gắn dự án TKT có sẵn: 5, 20, 31, 7, 135, 140, 41, 143, 13, 37
- Phòng tiếp nhận: 51 / 5 / 55 / 44; người tiếp nhận + PM là nhân viên có sẵn (35, 59, 148, 589, 341, 149, 65, 48, 50)
- Trạng thái: 2 Chờ tiếp nhận · 3 Đã tiếp nhận · 6 Đang thực hiện (×3) · 11 Đã chốt GP · 9 YC bổ sung · 8 Đã hoàn thành · 4 Từ chối · 10 Đóng
- Ngày gửi: 8 dòng 01–02/10/2026 (id 21–28), 2 dòng tháng 9/2026 (id 29, 30)

Lý do tạo theo người đăng nhập: service lọc phạm vi bằng tên quyền KHÔNG khớp seeder nên admin
chỉ thấy yêu cầu do chính mình tạo (xem mục "Điểm đáng ngờ" trong báo cáo).

## solutions (2 dòng) — id 31, 32
- `HN_DA.UD.0137.2026.DA001_GP901` — request_solution_id 24, department 55
- `HN_KD3.UD.0100.2026.DA008_GP902` — request_solution_id 26, department 44

Gỡ: `DELETE FROM solutions WHERE id IN (31,32); DELETE FROM request_solutions WHERE id BETWEEN 21 AND 30;`
