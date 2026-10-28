# So sánh mốc trước / sau — phân hệ human (Task 8.6, 28/10/2026)

## hrm-api (ScopeSnapshot)
- 27 route × 5 tài khoản = **135 ô** (`human-truoc.json` / `human-sau.json`).
- Mốc trước chụp 2 lần, `diff` ⇒ 0 ô khác (mốc ổn định).
- Sau khi đổi code: `diff --before=human-truoc.json --after=human-sau.json` ⇒ **Khác nhau: 0 ô**. Không có ô U8 (rehearsal không có người "có mã không phạm vi").

## Cờ ngoài snapshot (script scratch human-flags.py — gọi API, đọc khoá bool cấp đỉnh)
| tài khoản | hasPermissionEmployeeAccount | permissionResigned | hasPermissionRelationship (tên unknown) |
|---|---|---|---|
| 13 | true → true | true → true | false → false |
| 145 | false → false | true → true | false → false |
| 148 | false → false | false → false | false → false |
| 110 | false → false | false → false | false → false |
| 207 | false → false | false → false | false → false |
Trước = sau (diff file JSON rỗng).

## ERP (server tạm :8012, DB rehearsal) — mục menu "Quản lý tài khoản" trỏ HRM /admin/accounts
Đếm `admin/accounts` trong HTML trang `/` (topmenubar) theo phiên từng tài khoản:
| tài khoản | trước | sau |
|---|---|---|
| 13 | 1 | 1 |
| 145 | 1 | 1 |
| 148 | 1 | 1 |
| 110 | 1 | 1 |
| 207 | 0 | 0 |

## Kết luận
Mọi ô khớp; không ô lệch, không ô U8.
