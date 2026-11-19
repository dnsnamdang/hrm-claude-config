# Check: NV Ngô Thị Hoàng Yến (NV.00031) còn 0.5 phép nhưng làm đơn nghỉ 0.5 ngày bị báo "Ngày nghỉ không được lớn hơn số ngày nghỉ còn lại" — @khoipv

Màn: `https://demothanhan.dnsmedia.vn/timesheet/report/attendance_report` — NV.00031 (employee_info_id 31, Phòng Kế hoạch HN, company_id 4)
Ảnh: app mobile, đơn 19/11/2026 13:30–17:30 (0.5 ngày)
Bắt đầu: 18/11/2026 · Liên quan: `.plans/check-phep-con-lai-tran-van-chot`

## Task
- [x] Lấy báo cáo phép trên demo: được dùng 6, đã nghỉ 5.5 (T2 0.5, T4 **0.5**, T5 1, T6 0.5, T7 0.5, T9 0.5, T10 2.0) → còn 0.5
- [x] Lấy đơn Nghỉ phép đã duyệt 2026: tổng `total_days` = **6.0** → validate (`LeaveDayNPRule`) còn 0 → chặn đơn 0.5
- [x] Đối chiếu từng đơn với bảng công → lệch duy nhất đơn **1340**
- [x] Kiểm 10/10 (T7 chẵn, vụ Trần Văn Chót): đã tính lại 17/11 → `work_day_phep` 0.5, khớp đơn 1712 → KHÔNG còn lệch
- [x] Soát các đơn phép đã duyệt 2026 tạo trước 28/08 (ngày thứ thường) xem còn đơn nào lưu sai số ngày
- [ ] Chờ user chốt hướng xử lý

## Số liệu
| Đơn | Ngày nghỉ | `total_days` đơn | Bảng công `work_day_phep` |
|---|---|---|---|
| 1204 | 06/02 13:30–17:35 | 0.5 | |
| **1340** | **21/04 08:00–12:00 (sáng)** | **1** | **0.5** (summary 62419) |
| 1409 | 27/05 cả ngày | 1 | |
| 1460 | 17/06 sáng | 0.5 | |
| 1521 | 15/07 sáng | 0.5 | |
| 1646 | 12/09 (T7) sáng | 0.5 | 0.5 |
| 1712 | 10/10 (T7) chiều | 0.5 | 0.5 (tính lại 17/11) |
| 1732 | 14/10 chiều | 0.5 | |
| 1750 | 21/10 cả ngày | 1 | |
| | **Tổng** | **6.0** | **5.5** |

## Nguyên nhân
- Đơn 1340 nghỉ **buổi sáng** 21/04 (ca 56 Hành chính Đội Cấn, nghỉ trưa 12:00–13:30) nhưng lưu `total_days = 1`.
- Gọi lại `calculate-intend-day` trên demo cùng khoảng giờ → **0.5** ⇒ đúng phải là 0.5.
- Đơn tạo 21/04/2026, **trước** bản sửa `50671041` (28/08/2026) — lúc đó BE tin số ngày FE/app gửi lên; FE gọi API tính ngày theo từng thao tác chọn giờ, response về chậm ghi đè → lưu nhầm 1 (lỗi đã sửa ở `fix-so-ngay-nghi-du-kien-0`, nay BE tự tính lại trong `AttendanceRequest::recalculateTotalDays()`).
- Bảng công tính lại theo giờ thực tế → 0.5 ⇒ báo cáo còn 0.5; validate cộng `total_days` các đơn đã duyệt → 6 − 6 = 0 ⇒ chặn.
- ⇒ App chặn là do **dữ liệu đơn cũ sai**, không phải lỗi code hiện tại. Báo cáo "còn 0.5" là đúng.

## Hướng xử lý (chờ user)
1. Sửa dữ liệu: `UPDATE attendances SET total_days = 0.5 WHERE id = 1340;` → validate còn 0.5, NV làm được đơn. (Không cần tính lại công — bảng công đã đúng 0.5.)
2. Sửa thêm các đơn cũ lưu sai (danh sách soát bên dưới) bằng cùng cách.

## Kết quả soát các đơn cũ
Soát 218 đơn phép đã duyệt 2026, tạo trước 28/08, bắt đầu ngày T2–T6 (gọi lại `calculate-intend-day` trên demo, so với `total_days` đã lưu).

**Cùng lỗi (nghỉ nửa ngày nhưng lưu 1 ngày, bảng công 0.5):**
| Đơn | NV | Ngày | Lưu | Đúng | Ảnh hưởng hiện tại |
|---|---|---|---|---|---|
| 1340 | 31 Ngô Thị Hoàng Yến | 21/04 sáng | 1 | 0.5 | báo cáo còn 0.5, validate còn 0 → chặn |
| 1560 | 7 Nguyễn Thị Thu Hòa | 03/08 sáng | 1 | 0.5 | báo cáo còn 1, validate còn 0.5 → sẽ chặn đơn 1 ngày |
| 1200 | 41 Mai Tuấn Anh | 02/02 chiều | 1 | 0.5 | đã dùng quá phép (7.5/7), không đổi kết quả chặn |

**Không phải lỗi** (1527, 1520, 1512, 1444, 1214): đơn nhiều ngày qua thứ 7/CN — lệch do quy định cuối tuần đã đổi + lúc soát truyền `is_calc_holiday=1`, không cùng nguyên nhân.

SQL đề xuất (chờ user xác nhận):
```sql
UPDATE attendances SET total_days = 0.5 WHERE id IN (1340, 1560, 1200);
```

### Checkpoint — 18/11/2026
Vừa hoàn thành: ra nguyên nhân (đơn 1340 lưu 1 ngày thay vì 0.5) + soát xong, thêm 2 đơn cùng lỗi (1560, 1200)
Đang làm dở: —
Bước tiếp theo: user chốt chạy UPDATE total_days = 0.5 cho 1340 / 1560 / 1200 trên demo
Blocked:
