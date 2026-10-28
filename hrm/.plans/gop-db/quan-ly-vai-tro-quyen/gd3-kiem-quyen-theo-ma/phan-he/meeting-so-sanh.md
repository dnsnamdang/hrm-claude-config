# meeting — so mốc trước/sau (Task 8.3, 28/10/2026)

- `meeting-truoc.json`: 65 ô (13 route × 5 tài khoản). Chụp lần 2 ngay sau (code chưa đổi) + diff ⇒ 0 ô khác (mốc ổn định).
- `meeting-sau.json`: chụp sau khi đổi code (server 8011 php -S nạp code mới). `ScopeSnapshot diff` ⇒ **Khác nhau: 0 ô**.
- Không có ô lệch U8 (không tài khoản nào "có mã không phạm vi").

Số mốc (giống hệt trước/sau): assign/meeting 2274/2232/104/278/0 (pv4/pv3/pv2/pv1/không mã);
assign/meeting/{id} mở được 10/10/8/8/0 trên 10 id mẫu; room-bookings 7/0/0/0/0, chi tiết 7/0/0/0/0;
meeting_types 200 ×4 + 403 (không mã); cancel_reasons, rooms*, amenities, purposes, services, settings: 200 chỉ pv4, còn lại 403.
