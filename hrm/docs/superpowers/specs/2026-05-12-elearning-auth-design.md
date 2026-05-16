# Spec: Elearning Auth — Hệ thống xác thực cho Elearning

**Ngày tạo:** 2026-05-12
**Feature:** elearning-auth
**Người phụ trách:** @manhcuong

---

## 1. Mục tiêu

Xây dựng hệ thống authentication cho ứng dụng Elearning (Vue 3 + Vite), hỗ trợ 2 loại người dùng:

1. **Nhân viên HRM (Employee)** — đã có tài khoản trong bảng `employees`, đăng nhập bằng email/password HRM
2. **Học viên bên ngoài (Learner)** — không có tài khoản HRM, cần đăng ký mới

Hai ứng dụng (hrm-client và elearning) chạy trên **domain khác nhau hoàn toàn**, không thể share cookie.

---

## 2. Yêu cầu nghiệp vụ

### 2.1. Đăng nhập

- **1 form login chung** cho cả Employee và Learner
- Hệ thống tự nhận biết loại user dựa trên email:
  1. Kiểm tra email trong bảng `employees` trước → nếu match + password đúng → login thành công, `user_type = employee`
  2. Nếu không có trong `employees` → kiểm tra bảng `elearning_users` → nếu match + password đúng + đã verify email → login thành công, `user_type = learner`
  3. Nếu tìm thấy trong `elearning_users` nhưng chưa verify email → trả lỗi "Vui lòng xác thực email trước khi đăng nhập"
  4. Không tìm thấy ở cả 2 bảng → trả lỗi "Email hoặc mật khẩu không đúng"
- JWT token trả về chứa custom claim `user_type` (`employee` | `learner`)

### 2.2. Đăng ký (chỉ Learner)

- Các field bắt buộc: `fullname`, `email`, `password`, `password_confirmation`
- Các field tùy chọn: `phone`, `organization` (tên đơn vị/công ty)
- Validate:
  - `email`: unique trong cả 2 bảng `employees` VÀ `elearning_users`
  - `password`: tối thiểu 8 ký tự
  - `fullname`: bắt buộc, tối đa 255 ký tự
  - `phone`: format số điện thoại VN (10 số, bắt đầu 0)
- Sau đăng ký: gửi email xác thực, chưa verify thì không đăng nhập được
- FE hiện thông báo "Đăng ký thành công, vui lòng kiểm tra email để xác thực tài khoản"

### 2.3. Xác thực email

- Gửi email chứa link: `{ELEARNING_CLIENT_URL}/verify-email?token={token}`
- Token random 64 ký tự, hash SHA-256 trước khi lưu DB
- Token hết hạn sau **24 giờ**
- Cho phép gửi lại email xác thực (rate limit: 1 lần / 60 giây)
- Sau verify thành công: set `email_verified_at`, redirect sang trang login với message thành công

### 2.4. Quên mật khẩu (chỉ Learner)

- Nhập email → kiểm tra trong `elearning_users` → gửi email reset link
- Link: `{ELEARNING_CLIENT_URL}/reset-password?token={token}&email={email}`
- Token hết hạn sau **1 giờ**
- Form reset: nhập password mới + xác nhận
- Sau reset: redirect sang login với message thành công
- Employee quên password → thông báo "Vui lòng liên hệ quản trị viên HRM" (không hỗ trợ reset từ elearning)

### 2.5. Profile

- Xem thông tin cá nhân
- Learner: sửa được `fullname`, `phone`, `organization`, `avatar`
- Employee: chỉ xem (thông tin đồng bộ từ HRM, không cho sửa từ elearning)

### 2.6. Quyền hạn Learner

- Xem & tham gia khóa học công khai
- Bình luận, đánh giá khóa học
- Hỏi đáp với giảng viên
- Xem chứng chỉ
- KHÔNG có quyền quản trị (tạo khóa, quản lý user, xem báo cáo...)

---

## 3. Database Schema

### 3.1. Bảng `elearning_users`

```sql
CREATE TABLE elearning_users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL COMMENT 'Họ tên',
    email VARCHAR(255) NOT NULL COMMENT 'Email đăng nhập',
    password VARCHAR(255) NOT NULL COMMENT 'Bcrypt hash',
    phone VARCHAR(20) NULL COMMENT 'Số điện thoại',
    organization VARCHAR(255) NULL COMMENT 'Đơn vị/công ty',
    avatar VARCHAR(500) NULL COMMENT 'URL ảnh đại diện',
    email_verified_at TIMESTAMP NULL COMMENT 'Thời điểm xác thực email, NULL = chưa verify',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '1=active, 0=disabled',
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    UNIQUE INDEX elearning_users_email_unique (email)
) COMMENT 'Học viên bên ngoài đăng ký elearning';
```

### 3.2. Bảng `elearning_verifications`

Dùng chung cho xác thực email VÀ reset password.

```sql
CREATE TABLE elearning_verifications (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL COMMENT 'Email',
    token VARCHAR(255) NOT NULL COMMENT 'SHA-256 hash của token gốc',
    type VARCHAR(20) NOT NULL DEFAULT 'verify' COMMENT 'verify | reset_password',
    expired_at TIMESTAMP NOT NULL COMMENT 'Thời điểm hết hạn',
    created_at TIMESTAMP NULL,
    INDEX elearning_verifications_email_index (email),
    INDEX elearning_verifications_token_index (token)
) COMMENT 'Token xác thực email và reset password cho elearning_users';
```

**Lưu ý:** Không khai báo foreign key constraint (theo convention project).

---

## 4. Backend Architecture

### 4.1. Laravel Auth Guard

Thêm vào `config/auth.php`:

```php
'guards' => [
    // ... existing guards ...
    'elearning' => [
        'driver' => 'jwt',
        'provider' => 'elearning_users',
    ],
],

'providers' => [
    // ... existing providers ...
    'elearning_users' => [
        'driver' => 'eloquent',
        'model' => Modules\Elearning\Entities\ElearningUser::class,
    ],
],
```

### 4.2. Model: `ElearningUser`

**File:** `Modules/Elearning/Entities/ElearningUser.php`

- Extends `Illuminate\Foundation\Auth\User as Authenticatable`
- Implements `Tymon\JWTAuth\Contracts\JWTSubject`
- Table: `elearning_users`
- `$guarded = []`
- `$hidden = ['password']`
- `$casts = ['email_verified_at' => 'datetime']`
- Custom JWT claim: `getJWTCustomClaims()` trả về `['user_type' => 'learner']`

Constants trạng thái:
```php
const STATUS_ACTIVE = 1;
const STATUS_DISABLED = 0;
const STATUSES = [
    ['id' => self::STATUS_ACTIVE, 'name' => 'Hoạt động', 'color' => '#28a745'],
    ['id' => self::STATUS_DISABLED, 'name' => 'Vô hiệu', 'color' => '#dc3545'],
];
```

### 4.3. Model: `ElearningVerification`

**File:** `Modules/Elearning/Entities/ElearningVerification.php`

- Extends `Illuminate\Database\Eloquent\Model`
- Table: `elearning_verifications`
- `$guarded = []`

Constants:
```php
const TYPE_VERIFY = 'verify';
const TYPE_RESET_PASSWORD = 'reset_password';
const VERIFY_EXPIRE_HOURS = 24;
const RESET_PASSWORD_EXPIRE_HOURS = 1;
```

### 4.4. Controller: `ElearningAuthController`

**File:** `Modules/Elearning/Http/Controllers/Api/V1/ElearningAuthController.php`

Extends `ApiController`. Các method:

| Method | Chức năng |
|--------|-----------|
| `login(Request)` | Kiểm tra `employees` (guard `api`) → fallback `elearning_users` (guard `elearning`) |
| `register(ElearningRegisterRequest)` | Tạo ElearningUser + token verify + gửi mail |
| `verifyEmail(Request)` | Nhận token, set `email_verified_at` |
| `resendVerification(Request)` | Rate limit 60s, gửi lại mail verify |
| `forgotPassword(Request)` | Tạo token reset + gửi mail |
| `resetPassword(Request)` | Validate token + update password |
| `logout()` | Invalidate JWT token |
| `refresh()` | Trả token mới |
| `profile()` | Lấy profile dựa trên `user_type` claim |
| `updateProfile(Request)` | Chỉ cho phép Learner cập nhật |

### 4.5. Service: `ElearningAuthService`

**File:** `Modules/Elearning/Services/ElearningAuthService.php`

Chứa business logic:
- `attemptLogin($email, $password)` — logic phân biệt employee vs learner
- `registerUser($data)` — tạo user + verification token
- `sendVerificationEmail($user)` — gửi mail verify
- `verifyEmail($token)` — xác thực email
- `sendPasswordResetEmail($email)` — gửi mail reset
- `resetPassword($token, $email, $password)` — đặt lại mật khẩu
- `getProfile($user, $userType)` — lấy profile theo loại

### 4.6. Middleware: `ElearningAuthenticate`

**File:** `Modules/Elearning/Http/Middleware/ElearningAuthenticate.php`

Logic:
1. Lấy JWT token từ header `Authorization: Bearer {token}`
2. Decode token, đọc claim `user_type`
3. Nếu `user_type = employee` → set guard `api`, load TpEmployee
4. Nếu `user_type = learner` → set guard `elearning`, load ElearningUser
5. Kiểm tra status (active/disabled)
6. Set `auth()->user()` + inject `user_type` vào request

### 4.7. Form Requests

| Class | Validate |
|-------|----------|
| `ElearningRegisterRequest` | fullname: required, max:255; email: required, email, unique employees + elearning_users; password: required, min:8, confirmed; phone: nullable, regex VN; organization: nullable, max:255 |
| `ElearningLoginRequest` | email: required, email; password: required |
| `ElearningResetPasswordRequest` | token: required; email: required, email; password: required, min:8, confirmed |

### 4.8. Mail

| Mailable | Nội dung |
|----------|----------|
| `ElearningVerifyEmail` | Subject: "Xác thực email Elearning", body: link verify, hết hạn 24h |
| `ElearningResetPassword` | Subject: "Đặt lại mật khẩu Elearning", body: link reset, hết hạn 1h |

### 4.9. Routes

**File:** `Modules/Elearning/Routes/api.php`

```
Route::prefix('v1/elearning/auth')->group(function () {
    // Public
    Route::post('login', [ElearningAuthController::class, 'login']);
    Route::post('register', [ElearningAuthController::class, 'register']);
    Route::post('verify-email', [ElearningAuthController::class, 'verifyEmail']);
    Route::post('resend-verification', [ElearningAuthController::class, 'resendVerification']);
    Route::post('forgot-password', [ElearningAuthController::class, 'forgotPassword']);
    Route::post('reset-password', [ElearningAuthController::class, 'resetPassword']);

    // Authenticated
    Route::middleware('elearning.auth')->group(function () {
        Route::post('logout', [ElearningAuthController::class, 'logout']);
        Route::post('refresh', [ElearningAuthController::class, 'refresh']);
        Route::get('profile', [ElearningAuthController::class, 'profile']);
        Route::put('profile', [ElearningAuthController::class, 'updateProfile']);
    });
});
```

---

## 5. Frontend Architecture (Vue 3 + Vite + Pinia)

### 5.1. API Utility

**File:** `src/utils/api.js`

- Tạo axios instance với `baseURL` từ `import.meta.env.VITE_API_URL`
- Request interceptor: gắn `Authorization: Bearer {token}` từ localStorage
- Response interceptor: 401 → xóa token, redirect `/login`

### 5.2. Auth Store (Pinia)

**File:** `src/stores/auth.js`

```
State:
  - token: string | null
  - user: object | null
  - userType: 'employee' | 'learner' | null

Getters:
  - isAuthenticated: boolean
  - isEmployee: boolean
  - isLearner: boolean
  - userName: string

Actions:
  - login(email, password) → call API, lưu token vào localStorage, fetch profile
  - register(data) → call API register
  - logout() → call API, xóa token + state
  - refreshToken() → call API refresh, update token
  - fetchProfile() → call API profile, set user + userType
  - updateProfile(data) → call API update
  - initAuth() → đọc token từ localStorage, nếu có thì fetch profile (dùng khi app mount)
```

### 5.3. Router Guard

**File:** `src/router/index.js`

```
beforeEach:
  - Route có meta.requiresAuth + chưa login → redirect /login?redirect={to.fullPath}
  - Route /login, /register + đã login → redirect /
```

### 5.4. Các trang mới

| Route | File | Mô tả |
|-------|------|-------|
| `/login` | `src/views/auth/LoginView.vue` | Form email + password. Link "Đăng ký" + "Quên mật khẩu" |
| `/register` | `src/views/auth/RegisterView.vue` | Form đăng ký: fullname, email, password, confirm, phone, organization |
| `/verify-email` | `src/views/auth/VerifyEmailView.vue` | Nhận `?token=` từ URL, gọi API verify, hiển thị kết quả |
| `/forgot-password` | `src/views/auth/ForgotPasswordView.vue` | Nhập email, gửi request reset |
| `/reset-password` | `src/views/auth/ResetPasswordView.vue` | Nhận `?token=&email=`, form đặt password mới |

### 5.5. UI Updates

- **AppHeader.vue**: kiểm tra `isAuthenticated` → hiển thị tên user + avatar + dropdown (Profile, Đăng xuất). Nếu chưa login → nút "Đăng nhập"
- **Employee badge**: hiển thị tag "Nhân viên" + tên công ty
- **Learner badge**: hiển thị tag "Học viên"

### 5.6. Form Validation (FE)

- Dùng flag `touched` — chỉ hiện lỗi sau lần submit đầu
- Viền đỏ `border-red-500` cho field lỗi
- Text lỗi `text-red-500 text-sm` bên dưới field
- Validate realtime (email format, password length, confirm match) + server-side errors

---

## 6. Luồng xử lý chi tiết

### 6.1. Login Flow

```
User nhập email + password → POST /api/v1/elearning/auth/login
  → BE: auth()->guard('api')->attempt({email, password})
    → Thành công → trả JWT + user_type: 'employee'
    → Thất bại → tìm trong elearning_users
      → Tìm thấy + chưa verify → 422: "Vui lòng xác thực email"
      → Tìm thấy + đã verify → auth()->guard('elearning')->attempt()
        → Thành công → trả JWT + user_type: 'learner'
        → Thất bại → 401: "Email hoặc mật khẩu không đúng"
      → Không tìm thấy → 401: "Email hoặc mật khẩu không đúng"
```

### 6.2. Register Flow

```
User điền form → POST /api/v1/elearning/auth/register
  → Validate (email unique cả 2 bảng, password rules...)
  → DB::transaction:
    1. Tạo ElearningUser (email_verified_at = null)
    2. Tạo ElearningVerification (type=verify, expired_at = now+24h)
    3. Gửi email verify
  → Response 201: "Đăng ký thành công, vui lòng kiểm tra email"
```

### 6.3. Email Verification Flow

```
User click link trong email → GET /verify-email?token=abc123
  → FE: mount → POST /api/v1/elearning/auth/verify-email {token: 'abc123'}
  → BE: hash token → tìm trong elearning_verifications (type=verify, not expired)
    → Tìm thấy → set email_verified_at → xóa record verification → 200: OK
    → Không tìm thấy / hết hạn → 422: "Token không hợp lệ hoặc đã hết hạn"
  → FE: hiển thị kết quả + link sang login
```

### 6.4. Reset Password Flow

```
User nhập email → POST /forgot-password
  → Kiểm tra email trong elearning_users
    → Có → tạo token + gửi mail → 200: "Vui lòng kiểm tra email"
    → Không có → 200: "Nếu email tồn tại, bạn sẽ nhận được email" (không leak email exist)
    → Email thuộc employees → 422: "Tài khoản nhân viên vui lòng liên hệ quản trị viên HRM"

User click link → GET /reset-password?token=abc&email=user@mail.com
  → FE: hiện form password mới
  → POST /reset-password {token, email, password, password_confirmation}
  → BE: validate token + update password → 200: OK
```

---

## 7. Bảo mật

- **Password**: hash bcrypt (Laravel default)
- **Verification token**: random 64 bytes → SHA-256 hash trước khi lưu DB (chỉ lưu hash, không lưu plain text)
- **Rate limit**: resend verification 1 lần/60s, forgot password 1 lần/60s (dùng Laravel throttle middleware)
- **JWT**: dùng cùng secret key với HRM (`JWT_SECRET` trong .env)
- **CORS**: cấu hình cho phép origin elearning domain
- **Email enumeration**: endpoint forgot-password luôn trả 200 (trừ trường hợp employee → thông báo rõ)
- **Disabled account**: middleware kiểm tra `status = 1` mỗi request

---

## 8. Edge Cases

1. **Email trùng**: Người ngoài đăng ký email đã có trong `employees` → từ chối, thông báo "Email đã được sử dụng"
2. **Employee bị disable**: Login elearning cũng bị chặn (kiểm tra `employee_info.status`)
3. **Learner bị disable**: Admin HRM có thể disable từ backend → middleware chặn
4. **Token hết hạn**: Tự động cleanup bằng artisan command scheduled (tùy chọn, không bắt buộc phase đầu)
5. **Concurrent register**: Unique constraint trên email đảm bảo không duplicate
6. **Employee đổi email trên HRM**: Không ảnh hưởng elearning (login bằng email mới)

---

## 9. Ngoài scope (phase này)

- OAuth2 / Social login (Google, Facebook)
- 2FA (Two-factor authentication)
- Admin management UI cho elearning_users trong hrm-client
- Session management (xem devices đang login)
- Đồng bộ profile Employee → Elearning (avatar, thông tin)
- API rate limiting toàn diện
