# Elearning Auth — Implementation Plan (v2 — 2026-05-20)

**Goal:** Xây auth elearning theo spec v2: Employee auto-SSO qua hrm-client, Learner đăng ký/đăng nhập tại elearning, không verify email.

**Spec:** `docs/superpowers/specs/2026-05-20-elearning-auth-design.md`

**Người phụ trách:** @manhcuong

---

## Phase 0 — Cleanup spec cũ

> Khi check thực tế (2026-05-20): BE `Modules/Elearning` rỗng hoàn toàn (chỉ 2 folder `Database/Seeders`, `Transformers`). `config/auth.php` chưa có guard elearning. `modules_statuses.json` chưa có Elearning. → Không có gì để cleanup ở BE.

### Cleanup BE

- [x] Skip — folder Modules/Elearning trống hoàn toàn, không có file cần xóa.

### Cleanup FE elearning

- [x] Xóa `src/views/auth/VerifyEmailView.vue`
- Giữ lại các view khác — sẽ ghi đè ở Phase 5/6

---

## Phase 1 — Backend: Database

### Migration

- [x] Tạo `2026_05_20_000001_create_elearning_learners_table.php` — fields: id, email (unique), password, fullname, phone (nullable), avatar (nullable), status (tinyInt default 1), timestamps, created_by/updated_by (nullable). Mỗi cột có `comment()`.
- [x] Tạo `2026_05_20_000002_create_elearning_password_resets_table.php` — fields: id, email, token (string 64, index), expires_at (timestamp), timestamps. Mỗi cột có `comment()`.

---

## Phase 2 — Backend: Module core

### Module scaffold

- [x] Tạo `Modules/Elearning/module.json`
- [x] Tạo `Providers/ElearningServiceProvider.php` + `Providers/RouteServiceProvider.php`
- [x] Cập nhật `modules_statuses.json` — `Elearning: true`

### Entity

- [x] Tạo `Entities/Learner.php` — extends Authenticatable (tránh BaseModel auto-fill company_id), implements JWTSubject, mutator setPasswordAttribute hash bcrypt, claim `user_type=learner`.
- [x] Tạo `Entities/ElearningPasswordReset.php` — extends Model, có method `isExpired()`.

### Config & Middleware

- [x] Sửa `config/auth.php` — thêm guard `elearning` + provider `learners`.
- [x] Sửa `app/Http/Kernel.php` — đăng ký alias `'elearning.auth'`.
- [x] Tạo `Http/Middleware/ElearningAuth.php` — đọc Bearer token, phân nhánh guard theo claim `user_type`.

### Routes

- [x] Viết `Routes/api.php` — prefix `v1/elearning`, group public + group middleware `elearning.auth`.

---

## Phase 3 — Backend: Auth endpoints

### Form Request

- [x] Tạo `Http/Requests/LoginRequest.php` — email required|email, password required|string.
- [x] Tạo `Http/Requests/RegisterRequest.php` — email required|email|unique:elearning_learners, password required|min:8|confirmed, fullname required|max:100, phone nullable|regex VN.
- [x] Tạo `Http/Requests/SsoExchangeRequest.php` — token required|string.
- [x] Tạo `Http/Requests/ForgotPasswordRequest.php` — email required|email.
- [x] Tạo `Http/Requests/ResetPasswordRequest.php` — token required|string, password required|min:8|confirmed.
- [x] Tạo `Http/Requests/UpdateProfileRequest.php` — fullname required, phone nullable|regex, avatar nullable|string.

### Service

- [x] Tạo `Services/AuthService.php` — method: `attemptLearnerLogin`, `registerLearner` (transaction, hash password, issue token, trả token+user), `verifySsoToken` (auth('api')->setToken->authenticate, throw nếu fail), `issueResetToken` (transaction, UUID, lưu DB TTL 1h, dispatch Mail, rate-limit 3/h/email), `applyPasswordReset` (transaction, check token còn hạn, update password Learner, xóa record reset).

### Resource

- [x] Tạo `Transformers/LearnerResource.php` — list các field public của Learner.
- [x] Tạo `Transformers/EmployeeBriefResource.php` — id, fullname, email, avatar, code, current_company.

### Controller

- [x] Tạo `Http/Controllers/Api/V1/AuthController.php` — 10 method theo spec mục 5.6: login (chỉ learner), register (auto-login), ssoExchange (verify JWT, trả lại cùng token + employee info), forgotPassword (luôn 200), resetPassword, profile (phân nhánh user_type), updateProfile (learner OK, employee 403), logout (learner invalidate JWT guard elearning; employee chỉ trả 200), refresh (phân nhánh user_type).

---

## Phase 4 — Backend: Reset password mail

- [x] Tạo `Mail/LearnerResetPassword.php` — Mailable, build subject + view, truyền `$resetUrl = ELEARNING_CLIENT_URL/reset-password?token=...`, TTL 1h.
- [x] Tạo `Resources/views/emails/reset-password.blade.php` — template HTML đơn giản, nút "Đặt lại mật khẩu", note "link có hiệu lực 1 giờ".
- [x] Cập nhật `.env.example` — thêm `ELEARNING_CLIENT_URL=`

---

## Phase 5 — Frontend elearning: core

### utils/store/router

- [x] Ghi đè `src/utils/api.js` — base URL `${VITE_API_URL}/api/v1/elearning`, interceptor Bearer token, 401 → thử refresh (queue request) trước khi clear; expose util `hrmApi` riêng để gọi `${VITE_HRM_API_URL}/v1/users/auth/*`.
- [x] Ghi đè `src/stores/auth.js` — actions: login (learner), register (auto-login sau success), fetchProfile, updateProfile, logout (phân nhánh: employee gọi hrmApi logout + redirect HRM_CLIENT_URL/login; learner gọi elearning logout + router login), refreshToken (phân nhánh tương tự), forgotPassword, resetPassword, ssoExchange.
- [x] Ghi đè `src/router/index.js` — beforeEach: nếu `?sso=failed` → xóa flag sso_attempted + next /login. Nếu chưa auth + chưa attempt → set flag + window.location HRM_CLIENT_URL/sso/elearning?redirect_page=... Nếu attempt rồi → next /login. Bỏ route `/verify-email`.

---

## Phase 6 — Frontend elearning: Views

- [x] Ghi đè `src/views/auth/LoginView.vue` — wire `auth.login`, hiện toast khi query `?sso=failed`, bỏ text "đăng nhập tài khoản công ty".
- [x] Ghi đè `src/views/auth/RegisterView.vue` — wire `auth.register`, success → redirect '/'. Bỏ navigate verify-email.
- [x] Giữ `src/views/auth/SsoView.vue` — review, đảm bảo gọi đúng endpoint `/auth/sso-exchange`.
- [x] Ghi đè `src/views/auth/ForgotPasswordView.vue` — wire `/auth/forgot-password`, hiện success message generic.
- [x] Ghi đè `src/views/auth/ResetPasswordView.vue` — đọc `?token` query, wire `/auth/reset-password`.
- [x] Cập nhật `src/layouts/AuthLayout.vue` (nếu cần) — không có link verify-email.
- [x] Cập nhật `src/components/layout/AppHeader.vue` — nút "Đăng xuất" gọi `auth.logout()` phân nhánh đúng.

---

## Phase 7 — Frontend hrm-client: SSO gate

- [x] Tạo `pages/sso/elearning.vue` — asyncData/middleware: lấy `?redirect_page`. Nếu `store.state.current_employee` → redirect `${redirect_page}/sso?token=<jwt>`. Nếu không → redirect `${redirect_page}/login?sso=failed`. KHÔNG dùng middleware `authenticated` (vì chưa login phải redirect ngược, không phải về login HRM).
- [x] Verify chỗ JWT token lưu ở hrm-client (vuex state? $auth? localStorage?) — đọc `store/index.js`, `plugins/axios.js` để confirm. Sửa logic lấy token trong pages/sso/elearning.vue cho đúng.
- [x] Cập nhật `.env.example` hrm-client (nếu cần) — không bắt buộc, chỉ thêm `ELEARNING_CLIENT_URL` nếu hrm-client có chỗ nào generate link đến elearning.

---

## Phase 8 — Env, CORS, kiểm thử

### Env

- [x] hrm-api `.env`: thêm `ELEARNING_CLIENT_URL=` (dùng trong Mail reset-password).
- [x] elearning `.env`: `VITE_API_URL=`, `VITE_HRM_API_URL=`, `VITE_HRM_CLIENT_URL=`.

### CORS & module

- [x] Sửa `hrm-api/config/cors.php` — thêm origin elearning vào `allowed_origins`.
- [x] Verify `hrm-api/users/auth/logout` đã blacklist JWT thật (test bằng cách logout xong gọi API lại phải 401).

### Test thủ công

- [ ] TC1: User CÓ login HRM mở elearning → auto SSO thành công → vào trang home.
- [ ] TC2: User CHƯA login HRM mở elearning → bị redirect về `/login?sso=failed` → hiện form login learner.
- [ ] TC3: Đăng ký learner mới → tự động login → vào home.
- [ ] TC4: Login learner email/password đúng → vào home.
- [ ] TC5: Login learner sai password → hiện lỗi.
- [ ] TC6: Forgot password → nhận mail → click link → reset thành công → login lại được.
- [ ] TC7: Reset password với token hết hạn / đã dùng → báo lỗi.
- [ ] TC8: Logout learner → clear token → về /login.
- [ ] TC9: Logout employee (đang ở elearning) → JWT HRM bị invalidate → vào lại HRM cũng phải login lại.
- [ ] TC10: Token employee hết hạn khi đang dùng elearning → tự refresh → tiếp tục dùng được.
- [ ] TC11: Mở 2 tab elearning, logout 1 tab → tab kia gặp 401 → redirect login.
- [ ] TC12: Spam forgot password 4 lần/email/giờ → lần 4 bị rate-limit.
- [ ] TC13: Employee bị disable ở HRM → sso-exchange trả lỗi → màn Sso báo lỗi.
- [ ] TC14: Đăng ký với email đã tồn tại → báo 422.
- [ ] TC15: User update profile (learner) → save thành công. Employee update profile → 403.

---

## Checkpoint format

```
### Checkpoint — [timestamp]
Vừa hoàn thành: [task vừa xong]
Đang làm dở: [file + dòng + dừng ở đâu]
Bước tiếp theo: [hành động cụ thể]
Blocked: [để trống nếu không có]
```

---

### Checkpoint — 2026-05-20
Vừa hoàn thành: Phase 0→7 — toàn bộ code BE + FE + env.
Files BE (18): 2 migration, module.json, 2 service provider, 2 entity (Learner, ElearningPasswordReset), 1 middleware (ElearningAuth), 1 BaseRequest + 6 form request, 1 service (AuthService), 1 controller (AuthController), 2 transformer (LearnerResource, EmployeeBriefResource), 1 mail (LearnerResetPassword), 1 blade template, 1 route file. Sửa config/auth.php, app/Http/Kernel.php, modules_statuses.json.
Files FE elearning (8): src/utils/api.js, src/stores/auth.js, src/router/index.js, 5 view (Login, Register, Sso, ForgotPassword, ResetPassword). Xóa VerifyEmailView.vue. Sửa .env.
Files FE hrm-client (1): pages/sso/elearning.vue (ghi đè bản cũ).
Đang làm dở: không có.
Bước tiếp theo: User chạy `cd hrm-api && php artisan migrate` → restart server hrm-api + dev server elearning + nuxt hrm-client → chạy 15 TC ở Phase 8 plan.
Blocked: chưa test thủ công, chưa biết hành vi thực tế của `hrm-api/users/auth/logout` có blacklist JWT thật không (xem TC9).
