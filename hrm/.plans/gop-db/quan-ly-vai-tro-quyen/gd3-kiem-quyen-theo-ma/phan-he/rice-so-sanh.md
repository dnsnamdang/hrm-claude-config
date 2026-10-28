# rice — so sánh mốc trước / sau (Task 8.4, 28/10/2026)

- Mốc trước `rice-truoc.json`: 50 ô (10 route × 5 tài khoản), chụp lần 2 diff 0 ô (ổn định).
- Mốc sau `rice-sau.json` (sau khi đổi code): `ScopeSnapshot diff` ⇒ **Khác nhau: 0 ô**. Không ô U8.
- Băm nội dung (hash=content) ở danh sách phiếu + mọi báo cáo ⇒ so cả số liệu, không chỉ số dòng.
- Số đáng chú ý: phiếu đăng ký 13/337 = 2381, 311 = 2, 148 = 2, 207 = 0; báo cáo chi tiết 13/337 = 1044, 311 = 13, 148 = 12, 207 = 1
  (không mã ⇒ chỉ dòng của mình — hành vi cũ, giữ); menu-board 200 chỉ 13, 4 người khác 403.
- Ca thiếu trên mốc: phạm vi 3, có mã không phạm vi, khác công ty ⇒ phủ ở `tests/Feature/Rbac/RiceScopeCodesTest.php`.
