# assign — so sánh mốc trước/sau (Task 8.12)

- Mốc trước: `assign-truoc.json` (48 route × 8 tài khoản = 384 ô), chụp 2 lần trên code gốc (hrm-api 120303c13) ⇒ khác 0 ô.
- Mốc sau: `assign-sau.json` chụp sau khi đổi code (cùng tài khoản, cùng token, cùng tham số).
- `snap.py diff assign-truoc.json assign-sau.json` ⇒ **Tổng ô: 384 · Khác: 0** (status, so_dong, ids_hash, co_hash — co_hash gồm mọi cờ bool kể cả cờ từng dòng canEdit/canApprove…).
- Không ô U8 (rehearsal không có người giữ mã có phạm vi ở scope NULL).
- Bỏ khỏi mốc: `assign/my-job/assign-business-list` (55–59 s/ô) — xem assign-routes.md.
