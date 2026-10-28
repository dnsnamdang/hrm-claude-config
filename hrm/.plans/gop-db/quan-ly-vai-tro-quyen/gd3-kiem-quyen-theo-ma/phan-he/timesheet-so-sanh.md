# timesheet — so sánh mốc trước / sau (Task 8.5)

Trước: timesheet-truoc.json (chụp 2 lần, diff 0 ô). Sau: timesheet-sau.json (sau khi đổi hrm-api). Công cụ tests/Support/ScopeSnapshot.php diff ⇒ **Khác nhau: 0 ô**.

Tổng: 210 ô (42 route × 5 tài khoản), khớp 210, lệch 0. Không ô U8 (rehearsal không có người "có mã không phạm vi").

| route | pv4 | pv4_khong_duyet | pv2 | pv2_b | khong_ma |
|---|---|---|---|---|---|
| attendance.index | 200/14103 = | 200/14098 = | 200/170 = | 200/556 = | 200/34 = |
| attendance.approve | 200/10 = | 200/48 = | 200/0 = | 200/0 = | 200/34 = |
| attendance.static | 200/46 = | 200/46 = | 200/8 = | 200/8 = | 200/7 = |
| leo.index | 200/196 = | 200/196 = | 200/1 = | 200/1 = | 200/0 = |
| leo.approve | 200/151 = | 200/0 = | 200/0 = | 200/0 = | 200/0 = |
| leo.static | 200/52 = | 200/52 = | 200/14 = | 200/14 = | 200/13 = |
| ota.index1 | 200/547 = | 200/547 = | 200/547 = | 200/547 = | 200/0 = |
| ota.index2 | 200/0 = | 200/0 = | 200/0 = | 200/0 = | 200/0 = |
| ota.static1 | 200/45 = | 200/45 = | 200/7 = | 200/7 = | 200/6 = |
| ota.static2 | 200/45 = | 200/45 = | 200/7 = | 200/7 = | 200/6 = |
| ota.approve | 200/3356 = | 200/7 = | 200/2 = | 200/12 = | 200/2 = |
| otr.index | 200/225 = | 200/225 = | 200/221 = | 200/221 = | 200/0 = |
| otr.approve | 200/219 = | 200/0 = | 200/1 = | 200/0 = | 200/0 = |
| otr.static | 200/5 = | 200/5 = | 200/5 = | 200/5 = | 200/5 = |
| rut.index | 200/24766 = | 200/24765 = | 200/320 = | 200/405 = | 200/12 = |
| rut.approve | 200/24 = | 200/0 = | 200/0 = | 200/0 = | 200/0 = |
| rut.static | 200/49 = | 200/49 = | 200/11 = | 200/11 = | 200/10 = |
| timekeeper.index | 200/6462 = | 200/6462 = | 200/83 = | 200/127 = | 200/18 = |
| timekeeper.flags | 200/1 = | 200/1 = | 200/1 = | 200/1 = | 200/1 = |
| ts_summary.index | 200/89 = | 200/89 = | 200/51 = | 200/58 = | 200/40 = |
| month_summary.show | 200/157 = | 200/157 = | 200/54 = | 200/62 = | 200/44 = |
| timeworking.index | 200/51 = | 200/51 = | 200/0 = | 200/0 = | 200/0 = |
| timeworking.histories | 200/0 = | 200/0 = | 403/-1 = | 403/-1 = | 403/-1 = |
| shift_details.index | 200/15 = | 200/15 = | 200/0 = | 200/0 = | 200/0 = |
| shift_details.general | 200/400 = | 200/400 = | 200/1 = | 200/1 = | 200/1 = |
| sdeds.by_date | 200/144 = | 200/144 = | 200/1 = | 200/1 = | 200/1 = |
| sah.index | 200/619 = | 200/619 = | 403/-1 = | 403/-1 = | 403/-1 = |
| rep.timekeeper | 200/109 = | 200/109 = | 200/14 = | 200/22 = | 200/4 = |
| rep.bta | 200/180 = | 200/180 = | 200/6 = | 200/21 = | 200/0 = |
| rep.bta_job | 200/853 = | 200/853 = | 200/13 = | 200/6 = | 200/1 = |
| rep.bta_business | 200/152 = | 200/152 = | 200/6 = | 200/18 = | 200/0 = |
| rep.bta_jobnote | 200/847 = | 200/847 = | 200/11 = | 200/6 = | 200/1 = |
| rep.bta_all | 200/999 = | 200/999 = | 200/17 = | 200/24 = | 200/1 = |
| rep.overtime | 200/104 = | 200/104 = | 200/3 = | 200/3 = | 200/4 = |
| rep.overtime_detail | 200/100 = | 200/100 = | 200/0 = | 200/0 = | 200/1 = |
| rep.attendance | 200/110 = | 200/110 = | 200/21 = | 200/29 = | 200/11 = |
| aer.index | 200/63 = | 200/0 = | 200/1 = | 200/4 = | 200/0 = |
| leave_type.histories | 200/0 = | 403/-1 = | 403/-1 = | 403/-1 = | 403/-1 = |
| master_settings.histories | 200/84 = | 403/-1 = | 403/-1 = | 403/-1 = | 403/-1 = |
| sh.working_shift_59 | 200/19 = | 200/19 = | 403/-1 = | 403/-1 = | 403/-1 = |
| sh.working_shift_62 | 200/10 = | 200/10 = | 403/-1 = | 403/-1 = | 403/-1 = |
| sh.master_setting | 200/84 = | 403/-1 = | 403/-1 = | 403/-1 = | 403/-1 = |

Ghi chú: ota.index1/index2/approve băm id (dòng có recess_*/approved_at = now() khi cột null ⇒ băm nội dung không ổn định). reports/* (nhóm route không gắn auth:api) vẫn trả theo JWT.
