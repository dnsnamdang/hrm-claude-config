# Fix đăng xuất cổng etek báo "Lỗi máy chủ" — @cuong61n

## Task
- [x] (13/11/2026) Điều tra: chị Huyền báo bấm Đăng xuất ở hrm.etek.com.vn hiện 2 toast "Lỗi máy chủ". Log etek 17:12–17:14: `explode(): Argument #2 must be of type string, array given` tại `AuthNewController.php:265` — `.env` etek không có `LOGOUT_URLS` nên config = `[]`, PHP 8.1 ném TypeError, `catch (\Exception)` không bắt được → 500.
- [x] (13/11/2026) Sửa: bản fix đã có ở gop_db (commit a8e903877: ép `(array)`, try/catch riêng từng URL SSO). Cherry-pick sang nhánh `tpe` (không conflict), `php -l` sạch, push `tpe` → a8150bf53.
- [x] (13/11/2026) Deploy etek: `git pull origin tpe` ở /var/www/etek/hrm-api (kéo cả vài commit tpe khác chưa có), lên a8150bf53. Config không bị cache nên không cần recache.
- [ ] Chờ chị Huyền bấm Đăng xuất lại để xác nhận (chưa tự test được vì cần token đăng nhập etek).

Trạng thái: đã push `tpe` + đã deploy etek 13/11/2026; chờ xác nhận.
