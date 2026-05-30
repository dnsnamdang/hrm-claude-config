# Skill: Elearning Auth & SSO

Quy tắc auth, SSO với hrm-client, profile và avatar cho project Elearning.

> Đọc skill `elearning-base` + `elearning-validate` trước khi áp dụng skill này.

---

## 1. Mô hình user

Elearning có **2 loại user** dùng chung BE `hrm-api` nhưng tách bảng + tách guard:

| User type | Bảng DB | Guard JWT | Claim `user_type` trong JWT |
|---|---|---|---|
| **Employee** (nhân viên HRM) | `employees` (đã có sẵn) | `api` | (không có claim) |
| **Learner** (người ngoài) | `elearning_learners` | `elearning` | `'learner'` |

**1 JWT_SECRET chung** cho cả 2 — chung `tymon/jwt-auth`. Phân biệt qua claim `user_type` trong payload.

## 2. Multi-guard middleware `elearning.auth`

File: `Modules/Elearning/Http/Middleware/ElearningAuth.php`. Đã đăng ký alias trong `app/Http/Kernel.php`.

Logic:
1. Parse JWT từ Bearer header
2. Đọc claim `user_type`:
   - `'learner'` → `auth('elearning')->setToken()->authenticate()`
   - Khác/không có → `auth('api')->setToken()->authenticate()`
3. Set `$request->attributes->set('user_type', 'learner'|'employee')` để controller đọc

Áp dụng route:
```php
Route::middleware('elearning.auth')->group(function () {
    Route::get('auth/profile', [AuthController::class, 'profile']);
    // ...
});
```

Trong controller:
```php
$userType = $request->attributes->get('user_type');
if ($userType !== 'learner') {
    return response()->json(['code' => 423, 'message' => '...'], 423);
}
$learner = auth('elearning')->user(); // hoặc auth('api')->user() cho employee
```

## 3. Flow SSO với hrm-client

Pattern dựa trên SSO của HRM-CRM (xem `sso.csv`): JWT bay qua URL, không có ticket trung gian.

### 3.1. Employee đã login HRM → vào elearning

```
[1] User mở elearning URL bất kỳ (vd: /).
[2] router.beforeEach thấy chưa auth + route bảo vệ:
    → window.location = `${HRM_CLIENT_URL}/sso/elearning?target=${origin}`
[3] hrm-client `pages/sso/elearning.vue`:
    - middleware: [] (bypass middleware authenticated)
    - Đọc store.state.current_employee + localStorage.access_token
    - Có login → window.location = `${target}/sso?token=${jwt}`
    - Chưa login → window.location = `${target}/login?sso=failed`
[4] elearning /sso (SsoView):
    → POST /elearning/auth/sso-exchange { token }
    → BE verify JWT bằng auth('api')->setToken->authenticate()
    → Trả về { access_token: <same token>, user_type: 'employee', user: {...} }
[5] FE lưu token, redirect '/'.
```

**Lưu ý quan trọng:**
- Query param dùng `target` (KHÔNG dùng `redirect_page` — vì `nuxtClientInit` của hrm-client tự "cướp" redirect khi thấy `redirect_page`, sẽ phá flow)
- hrm-client `middleware/authenticated.js` đã có bypass `if (route.path.startsWith('/sso/'))`
- Cross-origin: localStorage không share giữa `localhost` và `127.0.0.1`. Elearning phải redirect tới ĐÚNG host user đã login hrm-client (cấu hình `VITE_HRM_CLIENT_URL`)

### 3.2. User chưa login → vào elearning

Flow trên dẫn tới `/login?sso=failed`. Login page có 3 lựa chọn:
- Form login learner (email + password)
- Link "Đăng ký" (cho user ngoài)
- Nút **"Đăng nhập bằng HRM"** → redirect `${HRM_CLIENT_URL}/login?redirect_page=${origin}/sso` → user login HRM → tự bay về `/sso?token=...`

### 3.3. Throttle chống loop

Trong `router.beforeEach`, lưu `sessionStorage.sso_last_attempt` timestamp.
Nếu vào URL có `?sso=failed` mà lastAttempt < 3s → render login (chống loop SSO failed → SSO failed).
Nếu > 3s → vẫn thử SSO lại (case user mới login HRM tab khác).

```js
const SSO_THROTTLE_MS = 3000
// ssoSkipRoutes: register, forgot-password, reset-password, verify-email → render trực tiếp, không SSO
```

## 4. Single Sign-Out (HRM logout → elearning logout)

Cross-origin, browser không tự thông báo. Cách giải quyết:

### 4.1. BE — invalidate JWT khi HRM logout

JWT_TTL = null trong .env, blacklist library của `tymon/jwt-auth` không hoạt động. **Solution kép:**

1. Trong `AuthNewController::logout`: tự parse token + `invalidate(true)` + lưu Redis key `revoked_jwt:<jti>` forever (vì middleware `auth:api` đã except 'logout' nên `auth()->user()` = null trong method này)
2. `checkLogin` + middleware `ElearningAuth` đều check `Cache::has('revoked_jwt:'.$jti)` → 401 nếu có

### 4.2. FE — polling check session

`App.vue` của elearning:
- `visibilitychange` + `focus` event + polling 30s + watch route → gọi `hrmApi.get('/users/auth/check-login')`
- BE trả 401 → axios interceptor clear localStorage + redirect `/login`
- Hoặc trả `{logged_in: false}` → FE chủ động `auth.clearAuth()` + redirect

Chỉ trigger khi user là `employee` (learner không bị ảnh hưởng bởi HRM logout).

## 5. Verify email cho learner

- Register → KHÔNG auto-login. Tạo learner với `email_verified_at=null` + lưu token vào `elearning_email_verifications` (TTL 24h) + gửi mail
- Login chưa verify → 423 với `error_code: 'email_not_verified'` + `email` kèm theo
- View LoginView nhận `errorCode === 'email_not_verified'` → hiện banner CTA "Gửi lại mail xác thực" (KHÔNG dùng toast vì có nút action)
- `POST /auth/verify-email { token }` → set `email_verified_at` + auto-login (trả token)
- `POST /auth/resend-verify-email { email }` → tạo token mới, gửi mail. Rate limit 3 lần/email/giờ → 423

## 6. Forgot/Reset password (chỉ learner)

- `POST /auth/forgot-password { email }` → token UUID, TTL 1h, lưu `elearning_password_resets`, gửi mail. **Luôn trả 200** (bảo mật, không tiết lộ email tồn tại). Rate limit 3/email/giờ → 423.
- `POST /auth/reset-password { token, password, password_confirmation }` → check còn hạn → update password → xóa record.

Token hết hạn / đã dùng → 423 "Liên kết không hợp lệ hoặc đã hết hạn".

## 7. Profile + đổi mật khẩu

Endpoint chung cho cả 2 user type (middleware `elearning.auth`):

| Endpoint | Employee | Learner |
|---|---|---|
| `GET /auth/profile` | Đọc từ `auth('api')->user()` + `load('info')`. Resource `EmployeeBriefResource`. | Resource `LearnerResource` |
| `PUT /auth/profile` | **423** "Vui lòng cập nhật ở HRM" | Cho phép sửa `fullname`, `phone`, `avatar` |
| `POST /auth/change-password` | **423** "Vui lòng đổi ở HRM" | Cho phép đổi (validate `old_password` qua Hash::check) |
| `POST /auth/avatar` (multipart `avatar` file) | **423** | Upload S3 (`CmcS3Helper::putFile`) folder `tanphat_hrm/<env>/elearning_avatars` |

**Avatar mapping cho employee:** trong `EmployeeBriefResource`, lấy từ `info.image` (column tên là `image` trong bảng `employee_infos`, KHÔNG phải `avatar`).

```php
'avatar' => $info->image ?? null,
```

## 8. Logout flow

```js
// stores/auth.js — phân nhánh theo userType
async logout() {
  const wasEmployee = this.isEmployee
  const token = this.token
  try {
    if (wasEmployee) {
      // Gọi BE HRM để blacklist JWT toàn hệ thống
      await hrmApi.post('/users/auth/logout', null, { headers: { Authorization: `Bearer ${token}` } })
    } else {
      await api.post('/auth/logout')
    }
  } catch { /* ignore */ }
  finally {
    this.clearAuth()
    if (wasEmployee) {
      window.location.href = `${HRM_CLIENT_URL}/login` // về HRM login
    } else {
      window.location.href = '/login'
    }
  }
}
```

## 9. Logo công ty (dùng chung HRM)

Composable `useCompanyLogo()` ở `src/composables/useCompanyLogo.js`:
- Fetch 1 lần/session từ `GET ${HRM_API}/v1/master-settings?category=logo`
- Cache `sessionStorage.company_logo`
- Fallback `/TPE_LOGO.svg`

Dùng trong `AppHeader.vue` (cho user đã login) + `AuthLayout.vue` (trang auth).

## 10. Env variables

`elearning/.env`:
```
VITE_API_URL=http://127.0.0.1:8000/api          # base API (sẽ nối /v1/elearning)
VITE_HRM_API_URL=http://127.0.0.1:8000/api      # base API HRM legacy
VITE_HRM_CLIENT_URL=http://127.0.0.1:3000        # hrm-client (DÙNG CÙNG HOST với app user dùng)
```

`hrm-api/.env`:
```
ELEARNING_CLIENT_URL=http://127.0.0.1:5173       # dùng trong Mail (link verify-email, reset-password)
```

## 11. Checklist khi sửa auth flow

- [ ] BE endpoint mới đặt trong `Modules/Elearning/Routes/api.php`
- [ ] Endpoint yêu cầu auth → trong group `Route::middleware('elearning.auth')`
- [ ] Phân biệt employee vs learner qua `$request->attributes->get('user_type')`
- [ ] Lỗi nghiệp vụ không gắn field → 423 (xem skill `elearning-validate`)
- [ ] Resource employee có `load('info')` trước khi serialize
- [ ] Avatar employee map từ `info.image`
- [ ] Action store phân nhánh theo `userType` nếu hành vi khác giữa 2 loại user (vd logout, refresh)
- [ ] Test cả 2 flow: employee SSO + learner local login
