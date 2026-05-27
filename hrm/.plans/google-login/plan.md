# Google Login cho Elearning — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm chức năng đăng nhập bằng tài khoản Google vào màn login/register elearning, sử dụng Google Identity Services (GIS).

**Architecture:** FE load Google GIS SDK → popup chọn tài khoản → nhận id_token → gửi lên BE → BE verify token với Google tokeninfo API → tìm/tạo learner → trả JWT. Tách composable `useGoogleAuth` cho FE, thêm method `loginWithGoogle` vào AuthService BE.

**Tech Stack:** Laravel 8 (PHP 7.4), Vue 3 + Vite, Google Identity Services JS SDK, Google tokeninfo API

---

## File Structure

### Backend (hrm-api)
| Action | File | Responsibility |
|--------|------|---------------|
| Create | `Modules/Elearning/Database/Migrations/2026_05_26_100000_add_google_fields_to_elearning_learners_table.php` | Thêm `google_id`, `avatar_url` vào bảng `elearning_learners` |
| Create | `Modules/Elearning/Http/Requests/GoogleLoginRequest.php` | Validate request `credential` |
| Modify | `Modules/Elearning/Services/AuthService.php` | Thêm method `loginWithGoogle()` |
| Modify | `Modules/Elearning/Http/Controllers/Api/V1/AuthController.php` | Thêm method `loginWithGoogle()` |
| Modify | `Modules/Elearning/Transformers/LearnerResource.php` | Thêm `avatar_url` |
| Modify | `Modules/Elearning/Routes/api.php` | Thêm route `POST auth/google` |

### Frontend (elearning)
| Action | File | Responsibility |
|--------|------|---------------|
| Create | `src/composables/useGoogleAuth.js` | Load GIS SDK, init, prompt Google login |
| Modify | `src/stores/auth.js` | Thêm action `loginWithGoogle()` |
| Modify | `src/views/auth/LoginView.vue` | Thêm nút + divider Google login |
| Modify | `src/views/auth/RegisterView.vue` | Thêm nút Google login |

---

## Phase 1: Backend

### Task 1: Migration — thêm cột google_id, avatar_url

**Files:**
- Create: `hrm-api/Modules/Elearning/Database/Migrations/2026_05_26_100000_add_google_fields_to_elearning_learners_table.php`

- [ ] **Step 1: Tạo migration file**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddGoogleFieldsToElearningLearnersTable extends Migration
{
    public function up()
    {
        Schema::table('elearning_learners', function (Blueprint $table) {
            $table->string('google_id', 255)->nullable()->unique()->after('avatar')->comment('Google sub ID');
            $table->string('avatar_url', 500)->nullable()->after('google_id')->comment('Avatar URL từ Google');
        });
    }

    public function down()
    {
        Schema::table('elearning_learners', function (Blueprint $table) {
            $table->dropColumn(['google_id', 'avatar_url']);
        });
    }
}
```

- [ ] **Step 2: Cập nhật Learner model — cho phép password nullable**

File: `hrm-api/Modules/Elearning/Entities/Learner.php`

Sửa `setPasswordAttribute` để xử lý `password = null` (learner tạo từ Google không có password):

```php
public function setPasswordAttribute($value)
{
    if (is_null($value)) {
        $this->attributes['password'] = null;
        return;
    }
    if (!empty($value)) {
        $this->attributes['password'] = Hash::needsRehash($value) ? Hash::make($value) : $value;
    }
}
```

---

### Task 2: GoogleLoginRequest

**Files:**
- Create: `hrm-api/Modules/Elearning/Http/Requests/GoogleLoginRequest.php`

- [ ] **Step 1: Tạo request class**

```php
<?php

namespace Modules\Elearning\Http\Requests;

class GoogleLoginRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'credential' => 'required|string',
        ];
    }

    public function messages()
    {
        return [
            'credential.required' => 'Thiếu thông tin xác thực từ Google',
        ];
    }
}
```

---

### Task 3: AuthService — thêm loginWithGoogle()

**Files:**
- Modify: `hrm-api/Modules/Elearning/Services/AuthService.php`

- [ ] **Step 1: Thêm import Illuminate\Support\Facades\Http**

Thêm vào đầu file, sau dòng `use Illuminate\Support\Str;`:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
```

- [ ] **Step 2: Thêm method loginWithGoogle vào cuối class (trước closing bracket)**

```php
/**
 * Đăng nhập/đăng ký bằng Google id_token.
 * Trả về [token, null] nếu OK, [null, errorMessage] nếu fail.
 */
public function loginWithGoogle(string $credential): array
{
    $payload = $this->verifyGoogleToken($credential);
    if (!$payload) {
        return [null, 'Xác thực Google thất bại'];
    }

    $sub = $payload['sub'];
    $email = $payload['email'];
    $name = $payload['name'] ?? $email;
    $picture = $payload['picture'] ?? null;

    $learner = DB::transaction(function () use ($sub, $email, $name, $picture) {
        $learner = Learner::where('google_id', $sub)->first();
        if ($learner) {
            return $learner;
        }

        $learner = Learner::where('email', $email)->first();
        if ($learner) {
            $learner->google_id = $sub;
            if (!$learner->avatar_url) {
                $learner->avatar_url = $picture;
            }
            $learner->save();
            return $learner;
        }

        return Learner::create([
            'email' => $email,
            'fullname' => $name,
            'google_id' => $sub,
            'avatar_url' => $picture,
            'password' => null,
            'email_verified_at' => now(),
            'status' => 1,
        ]);
    });

    if ((int) $learner->status !== 1) {
        return [null, 'Tài khoản đã bị khóa'];
    }

    $token = auth('elearning')->login($learner);
    return [$token, null];
}

private function verifyGoogleToken(string $credential): ?array
{
    try {
        $response = Http::get('https://oauth2.googleapis.com/tokeninfo', [
            'id_token' => $credential,
        ]);

        if (!$response->successful()) {
            return null;
        }

        $payload = $response->json();

        if (($payload['aud'] ?? '') !== config('services.google.client_id')) {
            Log::warning('Google login: aud mismatch', ['aud' => $payload['aud'] ?? null]);
            return null;
        }

        if (($payload['email_verified'] ?? '') !== 'true') {
            return null;
        }

        return $payload;
    } catch (\Exception $e) {
        Log::error('Google token verification failed', ['error' => $e->getMessage()]);
        return null;
    }
}
```

---

### Task 4: AuthController — thêm loginWithGoogle()

**Files:**
- Modify: `hrm-api/Modules/Elearning/Http/Controllers/Api/V1/AuthController.php`

- [ ] **Step 1: Thêm import GoogleLoginRequest**

Thêm vào đầu file cùng các import Request khác:

```php
use Modules\Elearning\Http\Requests\GoogleLoginRequest;
```

- [ ] **Step 2: Thêm method loginWithGoogle vào controller (sau method login)**

```php
public function loginWithGoogle(GoogleLoginRequest $request)
{
    [$token, $error] = $this->auth->loginWithGoogle($request->credential);

    if (!$token) {
        return response()->json([
            'code' => 423,
            'message' => $error,
        ], 423);
    }

    $learner = auth('elearning')->user();
    return $this->loginResponse($token, 'learner', new LearnerResource($learner));
}
```

---

### Task 5: LearnerResource — thêm avatar_url

**Files:**
- Modify: `hrm-api/Modules/Elearning/Transformers/LearnerResource.php`

- [ ] **Step 1: Thêm avatar_url vào toArray**

Trong method `toArray()`, thêm sau dòng `'avatar'`:

```php
'avatar_url' => $this->avatar_url,
```

---

### Task 6: Route + Config

**Files:**
- Modify: `hrm-api/Modules/Elearning/Routes/api.php`
- Modify: `hrm-api/config/services.php`

- [ ] **Step 1: Thêm route POST auth/google**

Trong file `api.php`, thêm sau dòng `Route::post('auth/resend-verify-email', ...)`:

```php
Route::post('auth/google', [AuthController::class, 'loginWithGoogle']);
```

- [ ] **Step 2: Thêm config Google client_id**

Trong `hrm-api/config/services.php`, thêm vào mảng return:

```php
'google' => [
    'client_id' => env('GOOGLE_CLIENT_ID'),
],
```

- [ ] **Step 3: Thêm env variable vào .env.example**

```
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

---

## Phase 2: Frontend

### Task 7: Composable useGoogleAuth

**Files:**
- Create: `elearning/src/composables/useGoogleAuth.js`

- [ ] **Step 1: Tạo composable**

```js
import { ref } from 'vue'

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID
const SCRIPT_SRC = 'https://accounts.google.com/gsi/client'

const scriptLoaded = ref(false)
const scriptLoading = ref(false)

function loadScript() {
  if (scriptLoaded.value) return Promise.resolve()
  if (scriptLoading.value) {
    return new Promise((resolve) => {
      const check = setInterval(() => {
        if (scriptLoaded.value) {
          clearInterval(check)
          resolve()
        }
      }, 50)
    })
  }

  scriptLoading.value = true
  return new Promise((resolve, reject) => {
    const el = document.createElement('script')
    el.src = SCRIPT_SRC
    el.async = true
    el.defer = true
    el.onload = () => {
      scriptLoaded.value = true
      scriptLoading.value = false
      resolve()
    }
    el.onerror = () => {
      scriptLoading.value = false
      reject(new Error('Không thể tải Google SDK'))
    }
    document.head.appendChild(el)
  })
}

export function useGoogleAuth() {
  const googleLoading = ref(false)

  async function loginWithGoogle(onCredential) {
    googleLoading.value = true
    try {
      await loadScript()

      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: (response) => {
          onCredential(response.credential)
        },
        auto_select: false,
        cancel_on_tap_outside: true,
      })

      window.google.accounts.id.prompt((notification) => {
        if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
          googleLoading.value = false
        }
      })
    } catch {
      googleLoading.value = false
    }
  }

  return { googleLoading, loginWithGoogle }
}
```

---

### Task 8: Auth store — thêm action loginWithGoogle

**Files:**
- Modify: `elearning/src/stores/auth.js`

- [ ] **Step 1: Thêm action loginWithGoogle**

Trong block `actions`, thêm sau method `login()`:

```js
async loginWithGoogle(credential) {
  this.loading = true
  try {
    const { data } = await api.post('/auth/google', { credential })
    this.setSession(data.data.access_token, data.data.user_type, data.data.user)
    return { success: true }
  } catch (error) {
    const res = error.response?.data
    return {
      success: false,
      message: res?.message,
      errors: res?.errors,
    }
  } finally {
    this.loading = false
  }
},
```

---

### Task 9: LoginView — thêm nút Google

**Files:**
- Modify: `elearning/src/views/auth/LoginView.vue`

- [ ] **Step 1: Thêm import useGoogleAuth**

Trong `<script setup>`, thêm sau dòng `import { useToast }`:

```js
import { useGoogleAuth } from '@/composables/useGoogleAuth'
```

- [ ] **Step 2: Khởi tạo composable**

Thêm sau dòng `const toast = useToast()`:

```js
const { googleLoading, loginWithGoogle } = useGoogleAuth()
```

- [ ] **Step 3: Thêm handler handleGoogleLogin**

Thêm sau function `handleResendVerify`:

```js
function handleGoogleLogin() {
  loginWithGoogle(async (credential) => {
    const result = await auth.loginWithGoogle(credential)
    googleLoading.value = false
    if (result.success) {
      toast.success('Đăng nhập thành công')
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    } else {
      applyError(result)
    }
  })
}
```

- [ ] **Step 4: Thêm UI nút Google vào template**

Thêm vào template, **sau thẻ đóng `</form>`**, **trước block `<p class="mt-5 text-center...">`**:

```html
<div class="relative my-5">
  <div class="absolute inset-0 flex items-center">
    <div class="w-full border-t border-line"></div>
  </div>
  <div class="relative flex justify-center text-xs">
    <span class="bg-white px-2 text-muted">hoặc</span>
  </div>
</div>

<button
  type="button"
  :disabled="googleLoading || auth.loading"
  class="flex h-10 w-full items-center justify-center gap-2 rounded-[10px] border border-line bg-white text-sm font-bold text-ink hover:bg-gray-50 disabled:opacity-50"
  @click="handleGoogleLogin"
>
  <svg width="18" height="18" viewBox="0 0 48 48">
    <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
    <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
    <path fill="#FBBC05" d="M10.53 28.59a14.5 14.5 0 0 1 0-9.18l-7.98-6.19a24.1 24.1 0 0 0 0 21.56l7.98-6.19z"/>
    <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
  </svg>
  <span>{{ googleLoading ? 'Đang xử lý...' : 'Đăng nhập bằng Google' }}</span>
</button>
```

---

### Task 10: RegisterView — thêm nút Google

**Files:**
- Modify: `elearning/src/views/auth/RegisterView.vue`

- [ ] **Step 1: Thêm imports**

Trong `<script setup>`, thêm:

```js
import { useGoogleAuth } from '@/composables/useGoogleAuth'
import { useRouter } from 'vue-router'
```

- [ ] **Step 2: Khởi tạo composable + router**

Thêm sau dòng `const toast = useToast()`:

```js
const router = useRouter()
const { googleLoading, loginWithGoogle } = useGoogleAuth()
```

- [ ] **Step 3: Thêm handler**

Thêm sau function `handleResend`:

```js
function handleGoogleRegister() {
  loginWithGoogle(async (credential) => {
    const result = await auth.loginWithGoogle(credential)
    googleLoading.value = false
    if (result.success) {
      toast.success('Đăng nhập thành công')
      router.push('/')
    } else {
      toast.error(result.message || 'Đăng nhập Google thất bại')
    }
  })
}
```

- [ ] **Step 4: Thêm UI nút Google vào template**

Thêm vào template, **sau thẻ đóng `</form>`**, **trước block `<p class="mt-5 text-center...">`** (và cũng hiện khi `!registered`):

```html
<template v-if="!registered">
  <div class="relative my-5">
    <div class="absolute inset-0 flex items-center">
      <div class="w-full border-t border-line"></div>
    </div>
    <div class="relative flex justify-center text-xs">
      <span class="bg-white px-2 text-muted">hoặc</span>
    </div>
  </div>

  <button
    type="button"
    :disabled="googleLoading || auth.loading"
    class="flex h-10 w-full items-center justify-center gap-2 rounded-[10px] border border-line bg-white text-sm font-bold text-ink hover:bg-gray-50 disabled:opacity-50"
    @click="handleGoogleRegister"
  >
    <svg width="18" height="18" viewBox="0 0 48 48">
      <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
      <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
      <path fill="#FBBC05" d="M10.53 28.59a14.5 14.5 0 0 1 0-9.18l-7.98-6.19a24.1 24.1 0 0 0 0 21.56l7.98-6.19z"/>
      <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
    </svg>
    <span>{{ googleLoading ? 'Đang xử lý...' : 'Đăng ký bằng Google' }}</span>
  </button>
</template>
```

---

## Phase 3: Env + Hướng dẫn setup

### Task 11: Env variables

- [ ] **Step 1: Thêm env vào elearning/.env.example (hoặc .env)**

```
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

- [ ] **Step 2: Thêm env vào hrm-api/.env.example (hoặc .env)**

```
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

**Lưu ý:** Cả BE và FE dùng cùng 1 Google Client ID. Cần tạo OAuth 2.0 credentials trong Google Cloud Console:
1. Vào https://console.cloud.google.com → APIs & Services → Credentials
2. Create OAuth 2.0 Client ID → Web application
3. Authorized JavaScript origins: thêm `http://localhost:5173` (dev) + domain production
4. Copy Client ID → set vào cả 2 file env

---

### Checkpoint — Khi hoàn tất

Kiểm tra:
- [ ] Mở màn login → thấy nút "Đăng nhập bằng Google" dưới form
- [ ] Click nút → popup Google hiện ra
- [ ] Chọn tài khoản → tự login, redirect về trang chủ
- [ ] Learner mới được tạo trong DB với google_id, avatar_url, email_verified_at = now()
- [ ] Learner cũ (email trùng) được link google_id, login bình thường
- [ ] Mở màn register → thấy nút "Đăng ký bằng Google"
- [ ] Click → tạo learner + login luôn
