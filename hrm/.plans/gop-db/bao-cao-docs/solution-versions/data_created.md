# Dữ liệu tạo thêm (DB local_hrm_erp của gop_db-api) — 02/10/2026

Tạo bằng SQL (`seed.sql` cùng thư mục), id đặt cứng dải 951+ để không đụng dữ liệu các phiên khác.
Dùng CHUNG cho 2 báo cáo: `solution-versions` và `task-manager-by-employees`.

| Bảng | id | Nội dung |
|---|---|---|
| solutions | 951 | HN_DA.UD.0137.2026.DA013_GP951 – Giải pháp trang bị xưởng thực hành ô tô – Trường ĐH Quy Nhơn (dự án 130, Phòng Dự án, PM/người tạo NV 835 Vũ Quang Minh, trạng thái 7) |
| solutions | 952 | HN_DA.UD.0129.2026.DA016_GP952 – Giải pháp mô hình dạy học nghề Điện tử công nghiệp (dự án 133, Phòng KTCN, PM/người tạo NV 987 Hà Mạnh Cường, trạng thái 9) |
| solution_versions | 951, 952, 953 | GP951 V1 (14–25/09, Đã duyệt GP, duyệt 26/09) · GP951 V2 (01–20/10, Đang triển khai) · GP952 V1 (01–15/10, Chờ duyệt GP) |
| solution_modules | 951, 952, 953 | 2 hạng mục của GP951 (leader 835, 1142) + 1 hạng mục GP952 (leader 987) |
| solution_version_members | 951–958 | PM / Leader hạng mục / Thành viên của 3 version |
| tasks | 951–962 | 12 nhiệm vụ (mã TPE.TASK.NB.26.0951 → 0962): 3 nhiệm vụ tháng 9 (V1), 7 nhiệm vụ tháng 10 (V2, có 1 quá hạn 957 và 1 đến hạn hôm nay 958), 2 nhiệm vụ GP952 |
| task_result_progress_logs | 951–967 | Giờ thực tế báo cáo tiến độ của các nhiệm vụ trên |

Không sửa/xoá bản ghi có sẵn. Gỡ dữ liệu: xoá theo các id trên ở 6 bảng.
