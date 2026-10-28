# meeting — đường đọc chụp mốc (Task 8.3, 28/10/2026)

Chỉ hrm-api (scan: ERP 0 hit). Máy đọc: `meeting-routes.json`. 13 route × 5 tài khoản = 65 ô.

| app | method | url | mã | chuỗi phạm vi? | cột lọc |
|---|---|---|---|---|---|
| api | GET | assign/meeting | meeting.danh_sach_meeting.view | có (MeetingCriteria) | 4 không lọc / 3 company_id / 2 department_id∪part_id∪created_by / 1 part_id∪created_by / không created_by; ngoài cùng ∪ created_by ∪ host ∪ company_members |
| api | GET | assign/meeting/{id} (10 id mẫu) | meeting.danh_sach_meeting.view | có (Meeting::canViewByMeetingRules) | 4 true / 3 company_id / 2 department_id∈quản lý ∪ part_id / 1 part_id |
| api | GET | meeting/room-bookings | meeting.phieu_dat_phong_hop.view (≥4) | có/không | ≥4 không lọc; không: booked_by ∪ participants ∪ quản lý phòng; cờ duyệt từng dòng (approve) |
| api | GET | meeting/room-bookings/{id} (7 id) | meeting.phieu_dat_phong_hop.view | có/không | canView |
| api | GET | assign/meeting_types | danh_muc_loai_meeting.manage\|view | middleware | — |
| api | GET | assign/meeting_cancel_reasons | danh_muc_ly_do_huy_cuoc_hop.manage\|view | middleware | — |
| api | GET | meeting/rooms, rooms/form-options, rooms/643, room-amenities, room-purposes, room-services, settings/room-hours | meeting.phong_hop.manage | middleware (+ checkin_qr_token ở show) | — |

## Tài khoản (rehearsal, công ty 1)
| key | NV | danh_sach_meeting.view | khác |
|---|---|---|---|
| pv4 | 13 namdangit | 4 | đủ 8 mã meeting.* (phieu_dat_phong_hop.view 4) |
| pv3 | 145 nguyetdtm.nshn | 3 | + danh_muc_loai_meeting.manage/view |
| pv2 | 148 hieudd.da | 2 | quản lý phòng 55 |
| pv1 | 110 honglv.pt | 1 | + danh_muc_loai_meeting.view; quản lý phòng 47, bộ phận 26 |
| khong_ma | 207 hantt.kthn | — | không mã meeting.* |

Ca thiếu: "có mã không phạm vi" (không có người thật — kiểm bằng PHPUnit); khác công ty (không đổi công ty trên DB — PHPUnit).
Không chụp: export/import/lock/ghi (route ghi chỉ đổi chuỗi tên → mã, không phạm vi).
