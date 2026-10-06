# Dữ liệu tạo cho 3 SRS cụm Bàn giao công việc (03/10/2026) — DB local_hrm_erp (gop_db-api :8003)

Dùng chung cho handover / handover-add / handover-receiving.

## tasks (SQL, assignee_id = 13 DNS Admin, solution_id 956 · project_id 151 "Cung cấp và lắp đặt cầu nâng 2 trụ cho xưởng dịch vụ Ô tô Thành An")
id 966–976 — mã TPE.TASK.NB.26.0966 … 0976 (Khảo sát hiện trạng mặt bằng xưởng Thành An, Lập bản vẽ bố trí 2 cầu nâng 2 trụ, …)

## issues (SQL)
id 13 ISS-202610-0101 "Nền xưởng khoang 2 chưa đủ độ dày để đặt cầu nâng" · id 14 ISS-202610-0102 "Khách hàng chưa xác nhận nguồn điện 3 pha cho máy nén khí" (assignee 13, solution 956)

## handovers (API, người lập = 13) + handover_items + handover_logs
| id | mã | trạng thái cuối | công việc → người nhận |
|---|---|---|---|
| 3 | BG.2026.0001 | Đã duyệt | 966→59 (đã nhận), 967→59 (từ chối → giao lại 13), 968→35, issue 13→35 (chờ nhận) |
| 4 | BG.2026.0002 | Hoàn tất | 971, 973 → 59 (tiếp nhận tất cả) |
| 5 | BG.2026.0003 | Nháp | 969→35 |
| 6 | BG.2026.0004 | Từ chối (TP không duyệt) | 970→59 |
| 7 | BG.2026.0005 | Chờ duyệt | 972→35 |
handover_items id 4–12; handover_logs id 7–23.
Hệ quả: tasks 966, 971, 973 assignee → 59; task 967 assignee → 13; tiến độ 966/967/969/971/973 được ghi lại theo phiếu.
Tasks 974–976 + issue 14 để trống cho màn Tạo bàn giao (không lưu phiếu nào thêm).

## Tài khoản người nhận
employees.id 59 Nguyễn Đức Khiển — khiennd.kd3@tanphat.com — đổi mật khẩu local thành `Handover@2026`
(hash cũ lưu ở handover/.old_pw_hash_employee59.txt). Người nhận thứ 2: id 35 Trần Ngọc Duy (không đổi mật khẩu).

## Thông báo phát sinh
Thông báo gửi duyệt / duyệt / từ chối / tiếp nhận / hoàn tất của các phiếu trên (bảng notifications).
