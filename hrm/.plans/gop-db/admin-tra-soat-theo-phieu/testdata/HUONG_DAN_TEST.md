# Hướng dẫn test #11523 — Đề nghị tra soát admin theo phiếu

- Tạo dữ liệu: `python3 seed_testdata.py` (chạy lại được, tự dọn bộ cũ) · Dọn: `python3 cleanup_testdata.py`
- Màn test: `http://127.0.0.1:3011` → menu Quản lý đơn → Tra soát công admin → Thêm mới
- Mọi phiếu nằm ở **Ngày làm việc = 29/09/2026**. 3 NV ở trang 1 popup chọn nhân viên:
  **A** Vũ Thị Phương Linh (12611039) · **B** Phạm Trung Đức (12611038) · **C** Đào Quốc Trung (12611037)

| Loại tra soát | Phiếu | A | B | C |
|---|---|---|---|---|
| Phiếu giao việc | TEST11523 Gặp KH chung A-B (08:00~17:00) | ✔ | ✔ | |
| Phiếu giao việc | TEST11523 Gặp KH riêng A (13:00~17:00) | ✔ | | |
| Phiếu công tác | TEST11523 Công tác chung A-B | ✔ | ✔ | |
| Phiếu làm thêm | TEST11523 Làm thêm chung A-B (18:00~21:00) | ✔ | ✔ | |
| Phiếu công tác kỹ thuật | PCT-TEST-KT — 2 công việc (HÀ VIỆT Ô TÔ, A THANH) | ✔ | ✔ | |
| Phiếu công tác khác | PCT-TEST-KC | ✔ | ✔ | ✔ |

## Kịch bản

| # | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở màn Thêm | Loại tra soát mặc định "Tra soát ca làm việc", KHÔNG có ô Ca/phiếu |
| 2 | Chọn loại "Phiếu giao việc", chưa chọn ngày | Ô Ca/phiếu hiện, dòng xám "Chọn ngày làm việc trước" |
| 3 | Chọn ngày 29/09/2026, chưa có NV | Dòng xám "Chọn nhân viên trước" |
| 4 | Thêm NV **A** | Ca/phiếu có **2** phiếu giao việc (chung + riêng A) |
| 5 | Thêm tiếp NV **B** | Còn **1** phiếu: "Gặp KH chung A-B" (phiếu riêng A biến mất) |
| 6 | Chọn phiếu chung, thêm NV **C** | Phiếu đã chọn bị xoá khỏi ô, ô khoá, dòng "Các nhân viên đã chọn không có ca/phiếu chung…" |
| 7 | Đổi loại sang "Phiếu công tác khác" (vẫn A+B+C) | Có PCT-TEST-KC → chọn, điền giờ 08:00–17:00 + lý do → DUYỆT → về danh sách |
| 8 | Xoá C (dấu −), loại "Phiếu công tác kỹ thuật" | Có PCT-TEST-KT; chọn → hiện ô "Phiếu công việc được giao" với 2 công việc, KHÔNG tự điền |
| 9 | Bấm DUYỆT khi chưa chọn công việc | "Bắt buộc nhập" dưới ô Phiếu công việc được giao |
| 10 | Chọn công việc, điền giờ + lý do → DUYỆT | Lưu thành công, về danh sách |
| 11 | Loại "Phiếu làm thêm" / "Phiếu công tác" với A+B | Mỗi loại có đúng 1 phiếu TEST11523 → lưu được |
| 12 | Đổi ngày sang 28/09/2026 khi đang chọn phiếu | Phiếu bị xoá, dòng "không có ca/phiếu chung" |
| 13 | Loại "Tra soát ca làm việc" với A+B+C | Không có ô Ca/phiếu, lưu như trước đây |
| 14 | Mở chi tiết các bản ghi vừa lưu | Hiện Loại tra soát + Ca/phiếu (phiếu kỹ thuật có kèm công việc sau dấu "/"); bản ghi cũ hiện "Tra soát ca làm việc" |

## Kiểm dữ liệu sau khi lưu

```sql
SELECT w.id, w.timesheet_type, w.timesheet_type_id, w.job_assign_id, w.timesheet_type_name,
       t.employee_info_id AS ssn, t.verify_date, t.type, t.job_type, t.job_id, t.job_assign_id
FROM admin_request_update_workings w
JOIN admin_request_update_working_employees e ON e.admin_request_update_working_id = w.id
JOIN admin_request_update_working_employee_timesheets x ON x.admin_request_update_working_employee_id = e.id
JOIN timesheets t ON t.id = x.timesheet_id
WHERE DATE(w.from_date) = '2026-09-29' ORDER BY w.id DESC;
```

- Loại phiếu: mỗi NV 2 lượt chấm công (giờ từ / giờ đến), `type = 1`, `job_type` = loại (công tác kỹ thuật/khác đều ghi `new_business_trip`), `job_id` = id phiếu, `job_assign_id` chỉ có ở phiếu kỹ thuật
- Loại ca làm việc: `type = 0`, `job_type/job_id` NULL — như cũ
