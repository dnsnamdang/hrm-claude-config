# presale — so mốc trước / sau (Task 8.8)

- Đầu vào: `presale-routes.json` (38 route hrm-api × 6 tài khoản = 228 ô). ERP: 0 hit presale ⇒ không chụp ERP.
- Trước: `presale-truoc.json` (chụp 13:25 28/10), chụp lần 2 cùng code gốc ⇒ **0 ô lệch** (mốc ổn định).
- Sau: `presale-sau.json` (chụp 13:47, code đã đổi) ⇒ `ScopeSnapshot diff`: **224 ô khớp, 4 ô lệch**.

## 4 ô lệch — do THỜI GIAN, không do quyền

| ô | trước | sau |
|---|---|---|
| bc.meeting-by-employees.filter × pv4 (13) | 1912 | 1911 |
| bc.meeting-by-employees.filter × pv4_thieu (145) | 1912 | 1911 |
| bc.meeting-by-employees.filter × pv2 (148) | 1779 | 1778 |
| bc.meeting-by-employees.filter × pv1 (110) | 1779 | 1778 |

- Cả 4 ô chỉ lệch đúng 1 phần tử ở danh sách `data.customers` (các danh sách khác trong ô — công ty / phòng / NV / loại / dự án — bằng nhau).
- Nguyên nhân: `MeetingByEmployeesReportService::applyMeetingFilters` lọc theo `now()` (#11145: meeting đã qua giờ chỉ lấy Hoàn thành/Hủy,
  chưa tới giờ lấy Chốt lịch). Meeting 2270 (KH 25925 "ANH THANH", status 2 = Chốt lịch, start 2026-10-28 13:30) là meeting DUY NHẤT của KH
  25925 trong kỳ: lúc chụp trước (13:25) còn ở tương lai ⇒ có KH, lúc chụp sau (13:47) đã qua giờ ⇒ bị loại.
- Tài khoản 13 có phạm vi 4 ⇒ nhánh `return` (không lọc) ở cả code cũ lẫn mới — lệch xuất hiện cả ở 13 chứng tỏ không do đổi quyền.
  1190 (C9) và 207 không thấy meeting đó ⇒ không lệch.
- Không ô U8 (rehearsal không có ai có mã Xem presale mà không phạm vi).
