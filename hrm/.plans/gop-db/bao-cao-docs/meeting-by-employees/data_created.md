# Dữ liệu đã tạo (DB local `local_hrm_erp` của gop_db-api) — 02/10/2026

Dùng chung cho 2 báo cáo: Meeting theo nhân viên (meeting-by-employees) và Meeting theo dự án (meeting-by-projects).
Tạo bằng SQL: `seed_data.sql` (cùng thư mục). Không sửa/xoá dữ liệu có sẵn.

| Bảng | id | Ghi chú |
|---|---|---|
| meetings | 45–51 | 7 cuộc họp tháng 10/2026, mã TPE.MET.KH.26.0060 → TPE.MET.NB.26.0066 |
| meeting_employees | 24 dòng mới (meeting_id 45–51) | type 1 = phía công ty (NV 24, 44, 62, 66, 67, 68, 75, 76, 83, 139, 212), type 2 = phía khách hàng |
| meeting_reports | 4 dòng mới (meeting_id 45, 45, 46, 47) | biên bản để bấm "Xem" |
| prospective_project_meetings | 6 dòng mới (meeting_id 45,46,47,48,49,51) | gắn dự án TKT 145, 138, 145, 141, 146, 138 |

Chi tiết 7 meeting:
- 45 TPE.MET.KH.26.0060 — 01/10 09:00–11:00, Hoàn thành, Trực tiếp, Meeting với khách hàng, DA 145
- 46 TPE.MET.KH.26.0061 — 01/10 14:00–15:30, Hoàn thành, Online, Meeting với khách hàng, DA 138
- 47 TPE.MET.NB.26.0062 — 02/10 08:30–10:00, Hoàn thành, Trực tiếp, Meeting nội bộ, DA 145
- 48 TPE.MET.KH.26.0063 — 01/10 16:00–17:00, Hủy, Online, Meeting với khách hàng, DA 141
- 49 TPE.MET.KH.26.0064 — 06/10 09:00–11:30, Chốt lịch, Trực tiếp, Meeting với khách hàng, DA 146
- 50 TPE.MET.NB.26.0065 — 08/10 14:00–16:00, Chốt lịch, Trực tiếp, Họp giao ban, không gắn dự án
- 51 TPE.MET.NB.26.0066 — 02/10 07:30–08:30, Hoàn thành, Online, Meeting nội bộ, DA 138

Gỡ dữ liệu (nếu cần):
```sql
DELETE FROM prospective_project_meetings WHERE meeting_id BETWEEN 45 AND 51;
DELETE FROM meeting_reports WHERE meeting_id BETWEEN 45 AND 51;
DELETE FROM meeting_employees WHERE meeting_id BETWEEN 45 AND 51;
DELETE FROM meetings WHERE id BETWEEN 45 AND 51;
```
