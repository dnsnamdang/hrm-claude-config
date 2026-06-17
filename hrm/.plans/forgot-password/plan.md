# Forgot Password — Plan

Spec: `docs/superpowers/specs/2026-06-01-forgot-password-design.md`
Design tóm tắt: `.plans/forgot-password/design.md`

---

## Tài liệu

### Testcase
- [x] Viết testcase UI người dùng cuối → `.plans/forgot-password/testcase.xlsx` (24 TC: hiển thị, gửi yêu cầu, đặt lại, edge case captcha/token/validate, bảo mật, E2E). Generator: `.plans/forgot-password/generate-testcase.py`

## Phase 0 — Setup

### BE
- [x] `composer require mews/captcha:^3.3` bằng PHP 7.4 → cài `mews/captcha 3.3.3` + `intervention/image 2.7.2` (bản 3.4 kéo intervention/image 4.x cần PHP 8.3 → KHÔNG hợp). Lock đã regenerate dưới PHP 7.4, `composer install` chạy được. **3.3.x: helper `captcha()` không nhận `$api` → controller gọi `app('captcha')->create('default', true)`**

## Phase 1 — Backend

### BE
- [x] Tạo `ForgotPasswordRequest` (email, captcha, captcha_key required)
- [x] Tạo `ResetPasswordRequest` (email, token + password rule 7–20 + 4 yếu tố + not_in 123456@ + confirmed) + messages VN
- [x] `AuthNewController@captcha`: trả `{key, img}` từ `captcha('default', true)` (v3.4 không có `captcha_api()`)
- [x] `AuthNewController@forgotPassword`: verify captcha → TpEmployee email+status=1 → TH2/TH1 (ghi đè password_resets, Hash token, gửi mail đồng bộ)
- [x] `AuthNewController@resetPassword`: verify token (Hash::check + ≤30p) → đổi mật khẩu HumanEmployee + password_changed_at + xóa token; lỗi 422
- [x] `ResetPasswordMail` + blade `resources/views/mails/reset-password.blade.php`
- [x] `routes/api.php`: 3 route public (captcha/forgot-password/reset-password) + thêm 3 method vào `except` của `auth:api` trong constructor

## Phase 2 — Frontend (hrm-client)

### FE
- [x] `store/actions.js`: `getCaptcha`, `forgotPassword`, `resetPassword`
- [x] `pages/login.vue`: link "Quên mật khẩu?" → `/forgot_password`
- [x] `pages/forgot_password/index.vue` (layout auth): email + captcha ảnh + reload + validate inline + message TH1/TH2
- [x] `pages/reset_password/index.vue` (layout auth): token+email query + mật khẩu mới + checklist + map lỗi 422/token
- [x] `middleware/authenticated.js`: whitelist `/forgot_password` + `/reset_password` (trang public)

## Phase 4 — Fix bảo mật: vô hiệu hoá phiên cũ khi reset mật khẩu

### BE
- [x] `AuthNewController@resetPassword`: tăng `token_version` của HumanEmployee (mirror `updatePass`) để mọi phiên ở app/tab/thiết bị khác bị thoát (middleware Authenticate kiểm token_version)
- [x] Sync `token_version` + password sang ERP `HumanTpEmployee` (bọc try/catch, log warning nếu lỗi) — giống `updatePass`
- [x] `php -l` pass, import `HumanTpEmployee` đã có sẵn
- [x] Rà luồng admin reset password nhân viên (`EmployeeService@updateEmployee` dòng 227 + 252-254): ĐÃ có sẵn tăng token_version + sync ERP → KHÔNG cần sửa

## Phase 3 — Test thủ công (chờ user)

### Test
- [ ] `composer install` trên PHP 7.4 thật + GET captcha trả ảnh
- [ ] Email tồn tại+active → nhận mail link, message TH1
- [ ] Email không tồn tại / status=0 → message TH2 "Không tìm thấy tài khoản"
- [ ] Captcha sai → báo lỗi + ảnh captcha refresh
- [ ] Click link mail → màn reset, đặt mật khẩu hợp lệ → về login, đăng nhập được bằng mật khẩu mới
- [ ] Mật khẩu mới yếu / = 123456@ → lỗi inline
- [ ] Dùng lại link cũ (đã reset) → báo không hợp lệ
- [ ] Để link quá 30p → báo hết hạn
- [ ] Sau reset → login không bị bắt đổi mật khẩu (password_changed_at đã set)

---

### Checkpoint — 2026-06-01
Vừa hoàn thành: Toàn bộ code BE (Phase 0-1) + FE (Phase 2). Review nội bộ pass (php -l, trace luồng, middleware public không chặn).
Đang làm dở: (không)
Bước tiếp theo: User chạy `composer install` (PHP 7.4) + cấu hình SMTP thật + test 9 case Phase 3.
Blocked: (không)
