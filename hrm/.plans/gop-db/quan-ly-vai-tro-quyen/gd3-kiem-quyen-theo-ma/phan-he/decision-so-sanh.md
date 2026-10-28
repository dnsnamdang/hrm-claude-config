# decision — so mốc trước / sau (Task 8.7)

- Trước: `decision-truoc.json` (chụp 2 lần trên code gốc, `diff` = 0 ô ⇒ mốc ổn định).
- Sau: `decision-sau.json` (code đã đổi sang mã; hrm-api 8011 + ERP 8012 bản mới).
- `php tests/Support/ScopeSnapshot.php diff --before=decision-truoc.json --after=decision-sau.json` ⇒ **Khác nhau: 0 ô / 408**.
- Ô U8: không có (rehearsal không ai có mã decision.* Xem mà không phạm vi; không ai mức 1).
- Ghi chú tín hiệu: `dash.all-decisions-by-time` trả 400 (thiếu tham số) cho 3 tài khoản có quyền dashboard, 200/0 cho 3 tài khoản còn lại — trước = sau; nhiều route dashboard / danh sách ra 0 dòng ở pv3_b/pv2/khong_ma (dữ liệu C9 ít) — vẫn so được status + băm.
