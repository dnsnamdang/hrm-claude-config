# Force Change Password — Plan

Spec: `docs/superpowers/specs/2026-06-01-force-change-password-design.md`
Design tóm tắt: `.plans/force-change-password/design.md`

---

## Phase 1 — Database

### BE
- [x] Tạo migration `add_login_count_and_password_changed_at_to_employees_table`: `login_count` (unsignedInteger default 0) + `password_changed_at` (timestamp nullable)
- [x] `up()` backfill `DB::table('employees')->update(['password_changed_at' => now()])` (miễn tài khoản cũ)
- [x] `down()` dropColumn `login_count`, `password_changed_at`
- [x] Thêm cast `password_changed_at => datetime` vào model `TpEmployee`

## Phase 2 — Backend

### BE
- [x] `AuthNewController@login`: `increment('login_count')` + tính `require_change_password = login_count >= 2 && is_null(password_changed_at)`
- [x] `createNewToken()`: thêm `require_change_password` vào payload (mặc định false)
- [x] Tạo middleware `MustChangePassword` (403 + flag, whitelist `users/auth/*` + `master-settings*`)
- [x] Đăng ký middleware vào group `api` trong `Kernel.php`
- [x] Tạo `UpdatePasswordRequest` (rule 7–20 + 4 yếu tố + not_in 123456@ + confirmed + MatchOldPassword) + messages VN
- [x] `AuthNewController@updatePass`: dùng `UpdatePasswordRequest`, set `password_changed_at = now()`

## Phase 3 — Frontend (hrm-client)

### FE
- [x] `pages/login.vue`: nếu `require_change_password` → set flag localStorage + push `/change_password`
- [x] Tạo middleware `force-change-password.js` + đăng ký trong `nuxt.config.js`
- [x] `store/actions.js` `handleError`: 403 `require_change_password` → set flag + push `/change_password`; 401 → xóa flag (chống kẹt vòng lặp)
- [x] `pages/change_password/index.vue`: chế độ `forced` (banner + mô tả điều kiện + nút Đóng=logout)
- [x] `pages/change_password/index.vue`: validate inline (`touched` + `is-invalid` + `invalid-feedback`), rule 7–20 + 4 yếu tố + khác 123456@
- [x] `pages/change_password/index.vue`: map lỗi 422 (`errors.{field}`) về từng input
- [x] `pages/change_password/index.vue`: đổi thành công → clear flag → push `/` + reload
- [x] `pages/change_password/index.vue`: redesign UI — card căn giữa + icon khóa + banner đẹp + checklist điều kiện mật khẩu live (tự xanh khi đạt) + nút V2BaseButton (primary Đổi mật khẩu + tertiary Đóng) theo button-convention

## Phase 4 — Test thủ công (chờ user)

### Test
- [ ] Chạy migration + verify cột + backfill
- [ ] Tài khoản mới: login lần 1 vào được; login lần 2 bị ép sang `/change_password`
- [ ] Nút "Đóng" → logout → login lại vẫn bị ép
- [ ] Đổi mật khẩu sai rule (ngắn/thiếu yếu tố/`123456@`/sai mật khẩu cũ) → lỗi inline đúng
- [ ] Đổi mật khẩu hợp lệ → vào hệ thống, login lần sau không bị ép
- [ ] Tài khoản cũ (backfill) → không bị ép
- [ ] Gọi API khác khi đang bị chặn → 403 → ép về `/change_password`
- [ ] Đổi mật khẩu tự nguyện từ menu → rule mới vẫn áp dụng

---

### Checkpoint — 2026-06-01
Vừa hoàn thành: Toàn bộ code BE (Phase 1-2) + FE (Phase 3). Review nội bộ pass, vá thêm edge case 401 (xóa flag chống kẹt loop).
Đang làm dở: (không)
Bước tiếp theo: User chạy `php artisan migrate` ở hrm-api + test thủ công 8 case Phase 4.
Blocked: (không)
