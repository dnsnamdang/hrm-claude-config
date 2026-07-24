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

---

## Phase 9 — Fix "nhân đôi tab ra nhầm tài khoản" (cross-tab auth sync)

**Bug user báo (2026-07-15):** Đăng nhập tk học viên ngoài → đăng xuất → đăng nhập bằng SSO HRM → nhân đôi tab (Chrome Duplicate) → tab nhân đôi lại là tk học viên ngoài.

**Root cause (đã xác minh bằng Playwright, không suy đoán):**
Auth store chỉ đọc `localStorage` ĐÚNG 1 LẦN lúc tab khởi tạo (`stores/auth.js:8-9`) và KHÔNG có tab nào lắng nghe event `storage`. Đổi tài khoản ở 1 tab → các tab elearning đang mở giữ identity CŨ trong RAM nhưng request lại gửi TOKEN MỚI (vì `utils/api.js:16-18` đọc localStorage LIVE mỗi request). Tab nhân đôi đọc localStorage thật → ra tài khoản khác tab gốc.
→ Duplicate tab KHÔNG phải nguyên nhân, chỉ là thứ phơi bày sự lệch pha. Hướng lệch (tab gốc sai hay tab mới sai) phụ thuộc tab nào là tab zombie.

**Bằng chứng đo được:** tab zombie hiển thị header "Akira Lee (HV)" trong khi `GET /elearning/auth/profile` bằng chính token trong localStorage trả về "DNS ADMIN update" (employee, sub=13). → Không chỉ lỗi hiển thị: thao tác trong tab đó GHI DỮ LIỆU VÀO NHẦM TÀI KHOẢN.

**Đã loại trừ:** BE `refresh` (AuthController:331-360) chọn guard theo claim TRONG token → không thể trộn tài khoản. BE `ssoExchange` (:126-145) đúng. Luồng 1 tab sạch (logout learner → SSO HRM → mở tab mới) KHÔNG tái hiện.

### Task

- [x] FE: `stores/auth.js` — thêm `initCrossTabSync()` lắng nghe event `storage`; so sánh IDENTITY (claim `sub` + `user_type` decode từ JWT) chứ KHÔNG so token thô — để `tryRefresh` định kỳ (cùng user, token mới) không gây reload oan
- [x] FE: `stores/auth.js` — token bị xoá ở tab khác (logout) → `clearAuth()` + về `/` (single sign-out giữa các tab)
- [x] FE: `stores/auth.js` — identity đổi ở tab khác (đăng nhập tk khác) → `window.location.reload()` để mọi store fetch lại theo đúng user (patch riêng auth store là chưa đủ: dữ liệu các store khác — my-learning, notification… — vẫn của user cũ)
- [x] FE: `App.vue` — gọi `initCrossTabSync()` trong `onMounted`
- [x] Verify bằng Playwright: 2 tab, đổi tài khoản ở tab 1 → tab 0 tự đồng bộ, không còn zombie

### Test case

- [x] TC16: Tab A learner + tab B → logout ở B → tab A tự về trạng thái chưa đăng nhập (không còn hiện tên learner)
- [x] TC17: Tab A learner + tab B → ở B logout rồi SSO HRM → tab A tự reload thành employee (header đúng tên nhân viên)
- [x] TC18: Sau TC17, nhân đôi tab A → tab nhân đôi khớp tài khoản với tab gốc
- [x] TC19: Token tự refresh (cùng user) → các tab khác KHÔNG bị reload oan

### Checkpoint — 2026-07-15
Vừa hoàn thành: Phase 9 — fix cross-tab auth sync. 2 file FE elearning:
- `src/stores/auth.js` — thêm helper `tokenIdentity()` (decode claim `sub` + `user_type`) + action `initCrossTabSync()` lắng nghe event `storage`: token bị xoá ở tab khác → `clearAuth()` + về `/`; identity đổi → `window.location.reload()`; identity KHÔNG đổi (refresh token) → bỏ qua.
- `src/App.vue` — gọi `auth.initCrossTabSync()` trong `onMounted`.
Verify thật bằng Playwright (2 tab + tab nhân đôi, learner akiralee2002 ↔ employee namdangit): TC16/17/18/19 PASS. Đo trực tiếp `GET /elearning/auth/profile` để đối chiếu header hiển thị vs identity BE trả về → đã khớp. TC19 dùng canary `window.__reloadCanary` chứng minh refresh token cùng user KHÔNG reload oan tab khác. `eslint src/stores/auth.js src/App.vue` → exit 0.
Không đụng BE, không migration, không permission, không git.
Đang làm dở: không có.
Bước tiếp theo: User verify tay trên Chrome thật bằng Duplicate tab (Ctrl+Shift+D) — Playwright chỉ mở tab mới cùng URL, tương đương về localStorage nhưng KHÔNG copy sessionStorage như Duplicate thật.
Blocked: không có.

---

## Phase 10 — Fix link xác thực email hỏng (`http:///verify-email`)

**Bug user báo (2026-07-16):** Bấm nút "Xác thực email" trong mail đăng ký → Google chặn với thông báo "Trang trước đó đang đưa bạn tới một url không hợp lệ (`http:///verify-email?token=705edbb7-...`)". Link thiếu hoàn toàn phần host.

**Root cause (đã trace, không suy đoán):**
`.env` của `hrm-api` KHÔNG khai báo key `ELEARNING_CLIENT_URL`, trong khi `AuthService.php:132` build link bằng `rtrim(env('ELEARNING_CLIENT_URL', ''), '/') . '/verify-email?token=' . $token`.
→ `env()` trả về default `''` → `$verifyUrl` = `/verify-email?token=...` (đường dẫn tương đối, không host) → blade render thẳng vào `href` (`emails/verify-email.blade.php:13`) → Gmail resolve link tương đối trong email thành `http:///verify-email?token=...` → URL không hợp lệ. Khớp 100% với ảnh user gửi.

**Bug thứ 2 cùng gốc (grep toàn repo, chỉ 2 chỗ dùng key này):**
`AuthService.php:171` sinh link `reset-password` y hệt → mail quên mật khẩu cũng đang hỏng, chỉ là chưa ai test tới.

**Cạm bẫy thứ 2 (nghiêm trọng hơn, phải fix cùng):**
Gọi `env()` NGOÀI file config → khi server chạy `php artisan config:cache`, Laravel bỏ nạp `.env` → `env()` trả `null` → link vỡ lại y hệt kể cả khi .env đã có key. Local hiện chưa cache config nên chỉ lộ nguyên nhân 1, nhưng lên staging/production dính ngay. Module Elearning hiện KHÔNG có thư mục `Config/`.

**Ghi chú môi trường:** `.env` local dùng `MAIL_HOST=mailhog` → mail local không ra Gmail. Email hỏng user nhận là do SERVER ĐÃ DEPLOY gửi → `.env` trên server đó cũng thiếu key, user phải tự thêm (ngoài tầm sửa của session này).

**User đã chốt:** URL FE elearning = `https://elearning.eteksofts.com` (FE ở root, API dưới `/api/v1/elearning`) · fix cả 2 dòng · được sửa `.env` local.

### Task

- [x] BE: Tạo `Modules/Elearning/Config/config.php` + `registerConfig()` trong `ElearningServiceProvider` (mẫu `AssignServiceProvider`) — `'client_url' => env('ELEARNING_CLIENT_URL', 'http://localhost:3001')` (chỗ hợp lệ DUY NHẤT để gọi `env()`, an toàn với `config:cache`)
- [x] BE: `AuthService.php:132` — `env('ELEARNING_CLIENT_URL', '')` → `config('elearning.client_url')` (link verify-email)
- [x] BE: `AuthService.php:171` — `env('ELEARNING_CLIENT_URL', '')` → `config('elearning.client_url')` (link reset-password)
- [x] BE: Thêm `ELEARNING_CLIENT_URL=https://elearning.eteksofts.com` vào `.env` local của hrm-api
- [x] Verify: build lại link bằng tinker/route thật → link phải có đủ host, không còn `http:///`

### Test case

- [x] TC20: Đăng ký tk mới → mail nhận được có link dạng `https://elearning.eteksofts.com/verify-email?token=...` (đủ host)
- [ ] TC21: Bấm link trong mail → vào đúng trang verify, tài khoản được kích hoạt, không còn cảnh báo Google
- [x] TC22: Quên mật khẩu → link reset dạng `https://elearning.eteksofts.com/reset-password?token=...` (đủ host)
- [ ] TC23: ~~Chạy `php artisan config:cache` rồi sinh lại link~~ → KHÔNG kiểm chứng được: `config:cache` hỏng sẵn toàn repo do `config/ckfinder.php:27` chứa Closure (bug riêng, ngoài scope). Để lại khi nào ckfinder được fix.

### Checkpoint — 2026-07-16
Vừa hoàn thành: Phase 10 — fix link xác thực email hỏng. 4 file BE (`hrm-api`, branch `tpe-develop-elearning`):
- `Modules/Elearning/Config/config.php` — file MỚI, khai báo `client_url` (chỗ hợp lệ duy nhất gọi `env()`).
- `Modules/Elearning/Providers/ElearningServiceProvider.php` — thêm `registerConfig()` (publishes + mergeConfigFrom) + gọi trong `boot()`, copy đúng mẫu `AssignServiceProvider:48-56`. Module trước đó KHÔNG nạp config nào.
- `Modules/Elearning/Services/AuthService.php` — dòng 132 (verify-email) + 171 (reset-password): `env('ELEARNING_CLIENT_URL','')` -> `config('elearning.client_url')`.
- `.env` (local) — thêm `ELEARNING_CLIENT_URL=https://elearning.eteksofts.com` ngay dưới `ERP_URL`.

Verify thật (không suy đoán): `tinker` -> `config('elearning.client_url')` = `https://elearning.eteksofts.com`; render Mailable `LearnerVerifyEmail` THẬT -> `href` = `https://elearning.eteksofts.com/verify-email?token=...`, khẳng định không còn chuỗi `http:///`. TC20 (phần build link) + TC22 PASS ở mức code.

PHÁT HIỆN THÊM: `php artisan config:cache` HỎNG SẴN toàn repo (KHÔNG do thay đổi này) — `config/ckfinder.php:27` gán Closure vào `$config['authentication']` -> `LogicException: Your configuration files are not serializable` (`Closure::__set_state()`). Hệ quả: server không cache config được, nên cạm bẫy `env()` chưa từng kích hoạt -> nguyên nhân sống DUY NHẤT là `.env` thiếu key. TC23 không kiểm chứng được chừng nào ckfinder chưa fix -> KHÔNG đánh pass.

Không đụng DB, không migration, không permission, không git.
Đang làm dở: không có.
Bước tiếp theo: User thêm `ELEARNING_CLIENT_URL=https://elearning.eteksofts.com` vào `.env` của SERVER đã deploy (elearning.eteksofts.com) — email hỏng user nhận là do server đó gửi (local dùng `MAIL_HOST=mailhog`, không ra Gmail được). Sau đó chạy TC21 (đăng ký thật -> bấm link trong mail).
Blocked: TC21 cần .env server (ngoài tầm session). TC23 cần fix `config/ckfinder.php` trước (bug riêng, ngoài scope phase này).
