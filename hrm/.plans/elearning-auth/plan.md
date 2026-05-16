# Elearning Auth — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Xây dựng hệ thống authentication cho elearning hỗ trợ 2 loại user (Employee HRM + Learner bên ngoài) với 1 form login chung, đăng ký + xác thực email cho Learner.

**Architecture:** Laravel multi-guard JWT — guard `elearning` mới cho Learner, guard `api` hiện tại cho Employee. Bảng `elearning_users` riêng biệt, middleware `ElearningAuthenticate` decode JWT claim `user_type` để load đúng model. Frontend Vue 3 + Pinia auth store + axios interceptor + router guard.

**Tech Stack:** Laravel 8, JWT (tymon/jwt-auth), nwidart/laravel-modules, Vue 3, Vite 5, Pinia 3, Vue Router 4, Tailwind CSS 3.4, axios

**Spec:** `docs/superpowers/specs/2026-05-12-elearning-auth-design.md`

---

## File Structure

### Backend — `hrm-api/`

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `Modules/Elearning/module.json` | Module registration |
| Create | `Modules/Elearning/Providers/ElearningServiceProvider.php` | Boot module, load migrations/views |
| Create | `Modules/Elearning/Providers/RouteServiceProvider.php` | Register API routes |
| Create | `Modules/Elearning/Routes/api.php` | Auth route definitions |
| Create | `Modules/Elearning/Database/Migrations/2026_05_12_000001_create_elearning_users_table.php` | Bảng elearning_users |
| Create | `Modules/Elearning/Database/Migrations/2026_05_12_000002_create_elearning_verifications_table.php` | Bảng elearning_verifications |
| Create | `Modules/Elearning/Entities/ElearningUser.php` | Model Learner (JWTSubject) |
| Create | `Modules/Elearning/Entities/ElearningVerification.php` | Model verification tokens |
| Create | `Modules/Elearning/Http/Requests/ElearningRegisterRequest.php` | Validate đăng ký |
| Create | `Modules/Elearning/Http/Requests/ElearningLoginRequest.php` | Validate đăng nhập |
| Create | `Modules/Elearning/Http/Requests/ElearningResetPasswordRequest.php` | Validate reset password |
| Create | `Modules/Elearning/Http/Middleware/ElearningAuthenticate.php` | Multi-guard JWT middleware |
| Create | `Modules/Elearning/Services/ElearningAuthService.php` | Business logic auth |
| Create | `Modules/Elearning/Http/Controllers/Api/V1/ElearningAuthController.php` | 10 auth endpoints |
| Create | `Modules/Elearning/Mail/ElearningVerifyEmail.php` | Mailable verify email |
| Create | `Modules/Elearning/Mail/ElearningResetPassword.php` | Mailable reset password |
| Create | `Modules/Elearning/Resources/views/emails/verify.blade.php` | Template email verify |
| Create | `Modules/Elearning/Resources/views/emails/reset-password.blade.php` | Template email reset |
| Modify | `config/auth.php` | Thêm guard + provider `elearning` |
| Modify | `modules_statuses.json` | Đăng ký module Elearning |

### Frontend — `elearning/`

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `src/utils/api.js` | Axios instance + interceptors |
| Create | `src/stores/auth.js` | Pinia auth store |
| Create | `src/views/auth/LoginView.vue` | Trang đăng nhập |
| Create | `src/views/auth/RegisterView.vue` | Trang đăng ký |
| Create | `src/views/auth/VerifyEmailView.vue` | Trang xác thực email |
| Create | `src/views/auth/ForgotPasswordView.vue` | Trang quên mật khẩu |
| Create | `src/views/auth/ResetPasswordView.vue` | Trang đặt lại mật khẩu |
| Create | `src/layouts/AuthLayout.vue` | Layout cho trang auth (không header/footer) |
| Modify | `src/router/index.js` | Thêm routes + beforeEach guard |
| Modify | `src/components/layout/AppHeader.vue` | User info / login button |
| Modify | `package.json` | Thêm dependency axios |

---

## Phase 1 — Backend: Module Scaffold + Database

### Task 1: Scaffold module Elearning

**Files:**
- Create: `Modules/Elearning/module.json`
- Create: `Modules/Elearning/Providers/ElearningServiceProvider.php`
- Create: `Modules/Elearning/Providers/RouteServiceProvider.php`
- Create: `Modules/Elearning/Routes/api.php`
- Modify: `modules_statuses.json`

- [x] **Step 1: Tạo module.json**

```json
// Modules/Elearning/module.json
{
    "name": "Elearning",
    "alias": "elearning",
    "description": "Module Elearning - Học trực tuyến",
    "keywords": [],
    "priority": 0,
    "providers": [
        "Modules\\Elearning\\Providers\\ElearningServiceProvider"
    ],
    "aliases": {},
    "files": [],
    "requires": []
}
```

- [x] **Step 2: Tạo ElearningServiceProvider.php**

```php
<?php
// Modules/Elearning/Providers/ElearningServiceProvider.php

namespace Modules\Elearning\Providers;

use Illuminate\Support\ServiceProvider;

class ElearningServiceProvider extends ServiceProvider
{
    protected $moduleName = 'Elearning';
    protected $moduleNameLower = 'elearning';

    public function boot()
    {
        $this->registerViews();
        $this->loadMigrationsFrom(module_path($this->moduleName, 'Database/Migrations'));
    }

    public function register()
    {
        $this->app->register(RouteServiceProvider::class);
    }

    public function registerViews()
    {
        $sourcePath = module_path($this->moduleName, 'Resources/views');
        $this->loadViewsFrom([$sourcePath], $this->moduleNameLower);
    }

    public function provides()
    {
        return [];
    }
}
```

- [x] **Step 3: Tạo RouteServiceProvider.php**

```php
<?php
// Modules/Elearning/Providers/RouteServiceProvider.php

namespace Modules\Elearning\Providers;

use Illuminate\Support\Facades\Route;
use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;

class RouteServiceProvider extends ServiceProvider
{
    protected $moduleNamespace = 'Modules\Elearning\Http\Controllers';

    public function boot()
    {
        parent::boot();
    }

    public function map()
    {
        $this->mapApiRoutes();
    }

    protected function mapApiRoutes()
    {
        Route::prefix('api')
            ->middleware('api')
            ->namespace($this->moduleNamespace)
            ->group(module_path('Elearning', '/Routes/api.php'));
    }
}
```

- [x] **Step 4: Tạo Routes/api.php (placeholder)**

```php
<?php
// Modules/Elearning/Routes/api.php

use Illuminate\Support\Facades\Route;

Route::prefix('v1/elearning')->group(function () {
    // Auth routes sẽ thêm ở Task 8
});
```

- [x] **Step 5: Tạo các thư mục cần thiết**

```bash
cd /Users/manhcuong/Desktop/dns/HRM/hrm-api
mkdir -p Modules/Elearning/Database/Migrations
mkdir -p Modules/Elearning/Database/Seeders
mkdir -p Modules/Elearning/Entities
mkdir -p Modules/Elearning/Http/Controllers/Api/V1
mkdir -p Modules/Elearning/Http/Middleware
mkdir -p Modules/Elearning/Http/Requests
mkdir -p Modules/Elearning/Services
mkdir -p Modules/Elearning/Mail
mkdir -p Modules/Elearning/Transformers
mkdir -p Modules/Elearning/Resources/views/emails
```

- [x] **Step 6: Đăng ký module trong modules_statuses.json**

Thêm `"Elearning": true` vào file `modules_statuses.json`.

- [x] **Step 7: Verify module load**

```bash
cd /Users/manhcuong/Desktop/dns/HRM/hrm-api
php artisan module:list
```

Expected: Elearning xuất hiện trong danh sách modules, status Enabled.

---

### Task 2: Migration — elearning_users + elearning_verifications

**Files:**
- Create: `Modules/Elearning/Database/Migrations/2026_05_12_000001_create_elearning_users_table.php`
- Create: `Modules/Elearning/Database/Migrations/2026_05_12_000002_create_elearning_verifications_table.php`

- [x] **Step 1: Tạo migration elearning_users**

```php
<?php
// Modules/Elearning/Database/Migrations/2026_05_12_000001_create_elearning_users_table.php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateElearningUsersTable extends Migration
{
    public function up()
    {
        Schema::create('elearning_users', function (Blueprint $table) {
            $table->id();
            $table->string('fullname')->comment('Họ tên');
            $table->string('email')->unique()->comment('Email đăng nhập');
            $table->string('password')->comment('Bcrypt hash');
            $table->string('phone', 20)->nullable()->comment('Số điện thoại');
            $table->string('organization')->nullable()->comment('Đơn vị/công ty');
            $table->string('avatar', 500)->nullable()->comment('URL ảnh đại diện');
            $table->timestamp('email_verified_at')->nullable()->comment('Thời điểm xác thực email, NULL = chưa verify');
            $table->tinyInteger('status')->default(1)->comment('1=active, 0=disabled');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('elearning_users');
    }
}
```

- [x] **Step 2: Tạo migration elearning_verifications**

```php
<?php
// Modules/Elearning/Database/Migrations/2026_05_12_000002_create_elearning_verifications_table.php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateElearningVerificationsTable extends Migration
{
    public function up()
    {
        Schema::create('elearning_verifications', function (Blueprint $table) {
            $table->id();
            $table->string('email')->comment('Email');
            $table->string('token')->comment('SHA-256 hash của token gốc');
            $table->string('type', 20)->default('verify')->comment('verify | reset_password');
            $table->timestamp('expired_at')->comment('Thời điểm hết hạn');
            $table->timestamp('created_at')->nullable();

            $table->index('email');
            $table->index('token');
        });
    }

    public function down()
    {
        Schema::dropIfExists('elearning_verifications');
    }
}
```

- [x] **Step 3: Chạy migration**

```bash
cd /Users/manhcuong/Desktop/dns/HRM/hrm-api
php artisan migrate
```

Expected: 2 bảng `elearning_users` và `elearning_verifications` được tạo.

- [x] **Step 4: Verify bảng đã tạo**

```bash
php artisan tinker --execute="echo Schema::hasTable('elearning_users') ? 'OK' : 'FAIL';"
php artisan tinker --execute="echo Schema::hasTable('elearning_verifications') ? 'OK' : 'FAIL';"
```

---

### Task 3: Models — ElearningUser + ElearningVerification

**Files:**
- Create: `Modules/Elearning/Entities/ElearningUser.php`
- Create: `Modules/Elearning/Entities/ElearningVerification.php`

- [x] **Step 1: Tạo ElearningUser model**

```php
<?php
// Modules/Elearning/Entities/ElearningUser.php

namespace Modules\Elearning\Entities;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Tymon\JWTAuth\Contracts\JWTSubject;

class ElearningUser extends Authenticatable implements JWTSubject
{
    protected $table = 'elearning_users';

    protected $guarded = [];

    protected $hidden = ['password'];

    protected $casts = [
        'email_verified_at' => 'datetime',
    ];

    const STATUS_ACTIVE = 1;
    const STATUS_DISABLED = 0;

    const STATUSES = [
        ['id' => self::STATUS_ACTIVE, 'name' => 'Hoạt động', 'color' => '#28a745'],
        ['id' => self::STATUS_DISABLED, 'name' => 'Vô hiệu', 'color' => '#dc3545'],
    ];

    public function getJWTIdentifier()
    {
        return $this->getKey();
    }

    public function getJWTCustomClaims()
    {
        return [
            'email' => $this->email,
            'user_type' => 'learner',
        ];
    }

    public function isVerified()
    {
        return $this->email_verified_at !== null;
    }

    public function isActive()
    {
        return $this->status === self::STATUS_ACTIVE;
    }
}
```

- [x] **Step 2: Tạo ElearningVerification model**

```php
<?php
// Modules/Elearning/Entities/ElearningVerification.php

namespace Modules\Elearning\Entities;

use Illuminate\Database\Eloquent\Model;

class ElearningVerification extends Model
{
    protected $table = 'elearning_verifications';

    protected $guarded = [];

    public $timestamps = false;

    protected $dates = ['expired_at', 'created_at'];

    const TYPE_VERIFY = 'verify';
    const TYPE_RESET_PASSWORD = 'reset_password';

    const VERIFY_EXPIRE_HOURS = 24;
    const RESET_PASSWORD_EXPIRE_HOURS = 1;

    public function isExpired()
    {
        return now()->greaterThan($this->expired_at);
    }
}
```

---

### Task 4: Auth Guard Configuration

**Files:**
- Modify: `config/auth.php`

- [x] **Step 1: Thêm guard và provider `elearning` vào config/auth.php**

Thêm vào mảng `guards` (sau `'api'`):

```php
'elearning' => [
    'driver' => 'jwt',
    'provider' => 'elearning_users',
    'hash' => false,
],
```

Thêm vào mảng `providers` (sau `'users'`):

```php
'elearning_users' => [
    'driver' => 'eloquent',
    'model' => Modules\Elearning\Entities\ElearningUser::class,
],
```

- [x] **Step 2: Verify guard hoạt động**

```bash
php artisan tinker --execute="echo config('auth.guards.elearning.driver');"
```

Expected: `jwt`

---

## Phase 2 — Backend: Auth Logic

### Task 5: Form Requests

**Files:**
- Create: `Modules/Elearning/Http/Requests/ElearningLoginRequest.php`
- Create: `Modules/Elearning/Http/Requests/ElearningRegisterRequest.php`
- Create: `Modules/Elearning/Http/Requests/ElearningResetPasswordRequest.php`

- [x] **Step 1: Tạo ElearningLoginRequest**

```php
<?php
// Modules/Elearning/Http/Requests/ElearningLoginRequest.php

namespace Modules\Elearning\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Contracts\Validation\Validator;
use Illuminate\Http\Exceptions\HttpResponseException;

class ElearningLoginRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'email' => 'required|email',
            'password' => 'required|string',
        ];
    }

    public function messages()
    {
        return [
            'email.required' => 'Vui lòng nhập email',
            'email.email' => 'Email không đúng định dạng',
            'password.required' => 'Vui lòng nhập mật khẩu',
        ];
    }

    protected function failedValidation(Validator $validator)
    {
        throw new HttpResponseException(response()->json([
            'code' => 422,
            'message' => 'Dữ liệu không hợp lệ',
            'errors' => $validator->errors(),
        ], 422));
    }
}
```

- [x] **Step 2: Tạo ElearningRegisterRequest**

```php
<?php
// Modules/Elearning/Http/Requests/ElearningRegisterRequest.php

namespace Modules\Elearning\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Contracts\Validation\Validator;
use Illuminate\Http\Exceptions\HttpResponseException;

class ElearningRegisterRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'fullname' => 'required|string|max:255',
            'email' => 'required|email|max:255|unique:elearning_users,email|unique:employees,email',
            'password' => 'required|string|min:8|confirmed',
            'phone' => ['nullable', 'string', 'regex:/^0[0-9]{9}$/'],
            'organization' => 'nullable|string|max:255',
        ];
    }

    public function messages()
    {
        return [
            'fullname.required' => 'Vui lòng nhập họ tên',
            'email.required' => 'Vui lòng nhập email',
            'email.email' => 'Email không đúng định dạng',
            'email.unique' => 'Email đã được sử dụng',
            'password.required' => 'Vui lòng nhập mật khẩu',
            'password.min' => 'Mật khẩu tối thiểu 8 ký tự',
            'password.confirmed' => 'Xác nhận mật khẩu không khớp',
            'phone.regex' => 'Số điện thoại không đúng định dạng (10 số, bắt đầu bằng 0)',
        ];
    }

    protected function failedValidation(Validator $validator)
    {
        throw new HttpResponseException(response()->json([
            'code' => 422,
            'message' => 'Dữ liệu không hợp lệ',
            'errors' => $validator->errors(),
        ], 422));
    }
}
```

- [x] **Step 3: Tạo ElearningResetPasswordRequest**

```php
<?php
// Modules/Elearning/Http/Requests/ElearningResetPasswordRequest.php

namespace Modules\Elearning\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Contracts\Validation\Validator;
use Illuminate\Http\Exceptions\HttpResponseException;

class ElearningResetPasswordRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'token' => 'required|string',
            'email' => 'required|email',
            'password' => 'required|string|min:8|confirmed',
        ];
    }

    public function messages()
    {
        return [
            'token.required' => 'Token không hợp lệ',
            'email.required' => 'Vui lòng nhập email',
            'password.required' => 'Vui lòng nhập mật khẩu mới',
            'password.min' => 'Mật khẩu tối thiểu 8 ký tự',
            'password.confirmed' => 'Xác nhận mật khẩu không khớp',
        ];
    }

    protected function failedValidation(Validator $validator)
    {
        throw new HttpResponseException(response()->json([
            'code' => 422,
            'message' => 'Dữ liệu không hợp lệ',
            'errors' => $validator->errors(),
        ], 422));
    }
}
```

---

### Task 6: Middleware — ElearningAuthenticate

**Files:**
- Create: `Modules/Elearning/Http/Middleware/ElearningAuthenticate.php`

- [x] **Step 1: Tạo middleware**

```php
<?php
// Modules/Elearning/Http/Middleware/ElearningAuthenticate.php

namespace Modules\Elearning\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Tymon\JWTAuth\Facades\JWTAuth;
use Tymon\JWTAuth\Exceptions\JWTException;
use Modules\Elearning\Entities\ElearningUser;

class ElearningAuthenticate
{
    public function handle(Request $request, Closure $next)
    {
        try {
            $token = JWTAuth::parseToken();
            $payload = $token->getPayload();
            $userType = $payload->get('user_type');
        } catch (JWTException $e) {
            return response()->json([
                'code' => 401,
                'message' => 'Token không hợp lệ hoặc đã hết hạn',
            ], 401);
        }

        try {
            if ($userType === 'learner') {
                $user = auth()->guard('elearning')->userOrFail();

                if (!$user->isActive()) {
                    return response()->json([
                        'code' => 401,
                        'message' => 'Tài khoản đã bị vô hiệu hóa',
                    ], 401);
                }
            } else {
                $user = auth()->guard('api')->userOrFail();

                $info = $user->info;
                if ($info && $info->status == 0) {
                    return response()->json([
                        'code' => 401,
                        'message' => 'Tài khoản đã bị vô hiệu hóa',
                    ], 401);
                }
            }
        } catch (\Exception $e) {
            return response()->json([
                'code' => 401,
                'message' => 'Không thể xác thực người dùng',
            ], 401);
        }

        $request->merge(['user_type' => $userType]);

        return $next($request);
    }
}
```

- [x] **Step 2: Đăng ký middleware trong ElearningServiceProvider**

Thêm vào method `boot()` của `ElearningServiceProvider.php`:

```php
public function boot()
{
    $this->registerViews();
    $this->loadMigrationsFrom(module_path($this->moduleName, 'Database/Migrations'));

    $router = $this->app['router'];
    $router->aliasMiddleware('elearning.auth', \Modules\Elearning\Http\Middleware\ElearningAuthenticate::class);
}
```

---

### Task 7: Service — ElearningAuthService

**Files:**
- Create: `Modules/Elearning/Services/ElearningAuthService.php`

- [x] **Step 1: Tạo service**

```php
<?php
// Modules/Elearning/Services/ElearningAuthService.php

namespace Modules\Elearning\Services;

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Modules\Elearning\Entities\ElearningUser;
use Modules\Elearning\Entities\ElearningVerification;
use Modules\Elearning\Mail\ElearningVerifyEmail;
use Modules\Elearning\Mail\ElearningResetPassword;
use App\Models\TpEmployee;

class ElearningAuthService
{
    public function attemptLogin($email, $password)
    {
        $employee = TpEmployee::where('email', $email)->first();
        if ($employee) {
            $token = auth()->guard('api')->attempt([
                'email' => $email,
                'password' => $password,
            ]);

            if ($token) {
                $info = $employee->info;
                if ($info && $info->status == 0) {
                    return ['error' => 'Tài khoản đã bị vô hiệu hóa', 'code' => 401];
                }

                return [
                    'token' => $token,
                    'user_type' => 'employee',
                    'user' => [
                        'id' => $employee->id,
                        'email' => $employee->email,
                        'fullname' => $info ? $info->fullname : $employee->email,
                        'avatar' => $info ? $info->image : null,
                        'company' => $info && $info->company ? $info->company->name : null,
                        'department' => $info && $info->department ? $info->department->name : null,
                    ],
                ];
            }
        }

        $elearningUser = ElearningUser::where('email', $email)->first();
        if (!$elearningUser) {
            return ['error' => 'Email hoặc mật khẩu không đúng', 'code' => 401];
        }

        if (!$elearningUser->isVerified()) {
            return ['error' => 'Vui lòng xác thực email trước khi đăng nhập', 'code' => 422];
        }

        if (!$elearningUser->isActive()) {
            return ['error' => 'Tài khoản đã bị vô hiệu hóa', 'code' => 401];
        }

        $token = auth()->guard('elearning')->attempt([
            'email' => $email,
            'password' => $password,
        ]);

        if (!$token) {
            return ['error' => 'Email hoặc mật khẩu không đúng', 'code' => 401];
        }

        return [
            'token' => $token,
            'user_type' => 'learner',
            'user' => [
                'id' => $elearningUser->id,
                'email' => $elearningUser->email,
                'fullname' => $elearningUser->fullname,
                'avatar' => $elearningUser->avatar,
                'phone' => $elearningUser->phone,
                'organization' => $elearningUser->organization,
            ],
        ];
    }

    public function registerUser($data)
    {
        return DB::transaction(function () use ($data) {
            $user = ElearningUser::create([
                'fullname' => $data['fullname'],
                'email' => $data['email'],
                'password' => Hash::make($data['password']),
                'phone' => $data['phone'] ?? null,
                'organization' => $data['organization'] ?? null,
            ]);

            $this->sendVerificationEmail($user);

            return $user;
        });
    }

    public function sendVerificationEmail(ElearningUser $user)
    {
        ElearningVerification::where('email', $user->email)
            ->where('type', ElearningVerification::TYPE_VERIFY)
            ->delete();

        $plainToken = Str::random(64);

        ElearningVerification::create([
            'email' => $user->email,
            'token' => hash('sha256', $plainToken),
            'type' => ElearningVerification::TYPE_VERIFY,
            'expired_at' => now()->addHours(ElearningVerification::VERIFY_EXPIRE_HOURS),
            'created_at' => now(),
        ]);

        $verifyUrl = config('app.elearning_client_url', env('ELEARNING_CLIENT_URL', 'http://localhost:3000'))
            . '/verify-email?token=' . $plainToken;

        Mail::to($user->email)->send(new ElearningVerifyEmail([
            'fullname' => $user->fullname,
            'verify_url' => $verifyUrl,
            'expire_hours' => ElearningVerification::VERIFY_EXPIRE_HOURS,
        ]));
    }

    public function verifyEmail($plainToken)
    {
        $hashedToken = hash('sha256', $plainToken);

        $verification = ElearningVerification::where('token', $hashedToken)
            ->where('type', ElearningVerification::TYPE_VERIFY)
            ->first();

        if (!$verification) {
            return ['error' => 'Token không hợp lệ hoặc đã hết hạn', 'code' => 422];
        }

        if ($verification->isExpired()) {
            $verification->delete();
            return ['error' => 'Token đã hết hạn, vui lòng gửi lại email xác thực', 'code' => 422];
        }

        $user = ElearningUser::where('email', $verification->email)->first();
        if (!$user) {
            return ['error' => 'Không tìm thấy tài khoản', 'code' => 404];
        }

        $user->update(['email_verified_at' => now()]);
        $verification->delete();

        return ['success' => true];
    }

    public function canResendVerification($email)
    {
        $lastSent = ElearningVerification::where('email', $email)
            ->where('type', ElearningVerification::TYPE_VERIFY)
            ->orderBy('created_at', 'desc')
            ->first();

        if ($lastSent && $lastSent->created_at && now()->diffInSeconds($lastSent->created_at) < 60) {
            return false;
        }

        return true;
    }

    public function sendPasswordResetEmail($email)
    {
        $employee = TpEmployee::where('email', $email)->first();
        if ($employee) {
            return ['error' => 'Tài khoản nhân viên vui lòng liên hệ quản trị viên HRM để đặt lại mật khẩu', 'code' => 422];
        }

        $user = ElearningUser::where('email', $email)->first();
        if (!$user) {
            return ['success' => true];
        }

        ElearningVerification::where('email', $email)
            ->where('type', ElearningVerification::TYPE_RESET_PASSWORD)
            ->delete();

        $plainToken = Str::random(64);

        ElearningVerification::create([
            'email' => $email,
            'token' => hash('sha256', $plainToken),
            'type' => ElearningVerification::TYPE_RESET_PASSWORD,
            'expired_at' => now()->addHours(ElearningVerification::RESET_PASSWORD_EXPIRE_HOURS),
            'created_at' => now(),
        ]);

        $resetUrl = config('app.elearning_client_url', env('ELEARNING_CLIENT_URL', 'http://localhost:3000'))
            . '/reset-password?token=' . $plainToken . '&email=' . urlencode($email);

        Mail::to($email)->send(new ElearningResetPassword([
            'fullname' => $user->fullname,
            'reset_url' => $resetUrl,
            'expire_hours' => ElearningVerification::RESET_PASSWORD_EXPIRE_HOURS,
        ]));

        return ['success' => true];
    }

    public function resetPassword($plainToken, $email, $newPassword)
    {
        $hashedToken = hash('sha256', $plainToken);

        $verification = ElearningVerification::where('token', $hashedToken)
            ->where('email', $email)
            ->where('type', ElearningVerification::TYPE_RESET_PASSWORD)
            ->first();

        if (!$verification) {
            return ['error' => 'Token không hợp lệ hoặc đã hết hạn', 'code' => 422];
        }

        if ($verification->isExpired()) {
            $verification->delete();
            return ['error' => 'Token đã hết hạn, vui lòng gửi lại yêu cầu đặt lại mật khẩu', 'code' => 422];
        }

        $user = ElearningUser::where('email', $email)->first();
        if (!$user) {
            return ['error' => 'Không tìm thấy tài khoản', 'code' => 404];
        }

        $user->update(['password' => Hash::make($newPassword)]);
        $verification->delete();

        return ['success' => true];
    }

    public function getProfile($userType)
    {
        if ($userType === 'employee') {
            $user = auth()->guard('api')->user();
            $info = $user->info;

            return [
                'user_type' => 'employee',
                'id' => $user->id,
                'email' => $user->email,
                'fullname' => $info ? $info->fullname : $user->email,
                'avatar' => $info ? $info->image : null,
                'phone' => $info ? $info->telephone : null,
                'company' => $info && $info->company ? $info->company->name : null,
                'department' => $info && $info->department ? $info->department->name : null,
                'can_edit_profile' => false,
            ];
        }

        $user = auth()->guard('elearning')->user();

        return [
            'user_type' => 'learner',
            'id' => $user->id,
            'email' => $user->email,
            'fullname' => $user->fullname,
            'avatar' => $user->avatar,
            'phone' => $user->phone,
            'organization' => $user->organization,
            'can_edit_profile' => true,
        ];
    }

    public function updateProfile($data)
    {
        $user = auth()->guard('elearning')->user();

        $user->update([
            'fullname' => $data['fullname'] ?? $user->fullname,
            'phone' => $data['phone'] ?? $user->phone,
            'organization' => $data['organization'] ?? $user->organization,
        ]);

        return $user->fresh();
    }
}
```

---

### Task 8: Mail — Email Templates

**Files:**
- Create: `Modules/Elearning/Mail/ElearningVerifyEmail.php`
- Create: `Modules/Elearning/Mail/ElearningResetPassword.php`
- Create: `Modules/Elearning/Resources/views/emails/verify.blade.php`
- Create: `Modules/Elearning/Resources/views/emails/reset-password.blade.php`

- [x] **Step 1: Tạo ElearningVerifyEmail Mailable**

```php
<?php
// Modules/Elearning/Mail/ElearningVerifyEmail.php

namespace Modules\Elearning\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

class ElearningVerifyEmail extends Mailable
{
    use Queueable, SerializesModels;

    private $data;

    public function __construct($data)
    {
        $this->data = $data;
    }

    public function build()
    {
        return $this->from(config('mail.from.address'), config('mail.from.name'))
            ->subject('Xác thực email - TPE Elearning')
            ->view('elearning::emails.verify')
            ->with($this->data);
    }
}
```

- [x] **Step 2: Tạo ElearningResetPassword Mailable**

```php
<?php
// Modules/Elearning/Mail/ElearningResetPassword.php

namespace Modules\Elearning\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

class ElearningResetPassword extends Mailable
{
    use Queueable, SerializesModels;

    private $data;

    public function __construct($data)
    {
        $this->data = $data;
    }

    public function build()
    {
        return $this->from(config('mail.from.address'), config('mail.from.name'))
            ->subject('Đặt lại mật khẩu - TPE Elearning')
            ->view('elearning::emails.reset-password')
            ->with($this->data);
    }
}
```

- [x] **Step 3: Tạo template verify email**

```blade
{{-- Modules/Elearning/Resources/views/emails/verify.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #034EA0; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; }
        .btn { display: inline-block; background: #034EA0; color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }
        .footer { text-align: center; padding: 15px; color: #6b7280; font-size: 13px; }
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0">TPE Elearning</h2>
    </div>
    <div class="content">
        <p>Xin chào <strong>{{ $fullname }}</strong>,</p>
        <p>Cảm ơn bạn đã đăng ký tài khoản TPE Elearning. Vui lòng nhấn nút bên dưới để xác thực email của bạn:</p>
        <p style="text-align: center;">
            <a href="{{ $verify_url }}" class="btn">Xác thực email</a>
        </p>
        <p>Link này sẽ hết hạn sau <strong>{{ $expire_hours }} giờ</strong>.</p>
        <p>Nếu bạn không đăng ký tài khoản này, vui lòng bỏ qua email này.</p>
    </div>
    <div class="footer">
        <p>&copy; {{ date('Y') }} TPE Elearning. All rights reserved.</p>
    </div>
</body>
</html>
```

- [x] **Step 4: Tạo template reset password email**

```blade
{{-- Modules/Elearning/Resources/views/emails/reset-password.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #034EA0; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #f9fafb; padding: 30px; border: 1px solid #e5e7eb; }
        .btn { display: inline-block; background: #034EA0; color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }
        .footer { text-align: center; padding: 15px; color: #6b7280; font-size: 13px; }
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0">TPE Elearning</h2>
    </div>
    <div class="content">
        <p>Xin chào <strong>{{ $fullname }}</strong>,</p>
        <p>Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản của bạn. Nhấn nút bên dưới để tiếp tục:</p>
        <p style="text-align: center;">
            <a href="{{ $reset_url }}" class="btn">Đặt lại mật khẩu</a>
        </p>
        <p>Link này sẽ hết hạn sau <strong>{{ $expire_hours }} giờ</strong>.</p>
        <p>Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.</p>
    </div>
    <div class="footer">
        <p>&copy; {{ date('Y') }} TPE Elearning. All rights reserved.</p>
    </div>
</body>
</html>
```

---

### Task 9: Controller — ElearningAuthController

**Files:**
- Create: `Modules/Elearning/Http/Controllers/Api/V1/ElearningAuthController.php`

- [x] **Step 1: Tạo controller**

```php
<?php
// Modules/Elearning/Http/Controllers/Api/V1/ElearningAuthController.php

namespace Modules\Elearning\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Modules\Elearning\Http\Requests\ElearningLoginRequest;
use Modules\Elearning\Http\Requests\ElearningRegisterRequest;
use Modules\Elearning\Http\Requests\ElearningResetPasswordRequest;
use Modules\Elearning\Services\ElearningAuthService;
use Modules\Elearning\Entities\ElearningUser;

class ElearningAuthController extends ApiController
{
    protected $authService;

    public function __construct(ElearningAuthService $authService)
    {
        $this->authService = $authService;
    }

    public function login(ElearningLoginRequest $request)
    {
        try {
            $result = $this->authService->attemptLogin(
                $request->email,
                $request->password
            );

            if (isset($result['error'])) {
                return $this->responseJson($result['error'], $result['code']);
            }

            return $this->responseSuccess('Đăng nhập thành công', [
                'access_token' => $result['token'],
                'token_type' => 'bearer',
                'user_type' => $result['user_type'],
                'user' => $result['user'],
            ]);
        } catch (\Exception $e) {
            Log::error('Elearning login error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }

    public function register(ElearningRegisterRequest $request)
    {
        try {
            $this->authService->registerUser($request->validated());

            return $this->responseCreated('Đăng ký thành công, vui lòng kiểm tra email để xác thực tài khoản');
        } catch (\Exception $e) {
            Log::error('Elearning register error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }

    public function verifyEmail(Request $request)
    {
        try {
            $request->validate(['token' => 'required|string']);

            $result = $this->authService->verifyEmail($request->token);

            if (isset($result['error'])) {
                return $this->responseJson($result['error'], $result['code']);
            }

            return $this->responseSuccess('Xác thực email thành công, bạn có thể đăng nhập ngay bây giờ');
        } catch (\Exception $e) {
            Log::error('Elearning verify email error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }

    public function resendVerification(Request $request)
    {
        try {
            $request->validate(['email' => 'required|email']);

            $user = ElearningUser::where('email', $request->email)->first();
            if (!$user) {
                return $this->responseSuccess('Nếu email tồn tại, bạn sẽ nhận được email xác thực');
            }

            if ($user->isVerified()) {
                return $this->responseUnprocessableEntity('Email đã được xác thực');
            }

            if (!$this->authService->canResendVerification($request->email)) {
                return $this->responseUnprocessableEntity('Vui lòng chờ 60 giây trước khi gửi lại');
            }

            $this->authService->sendVerificationEmail($user);

            return $this->responseSuccess('Đã gửi lại email xác thực');
        } catch (\Exception $e) {
            Log::error('Elearning resend verification error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }

    public function forgotPassword(Request $request)
    {
        try {
            $request->validate(['email' => 'required|email']);

            $result = $this->authService->sendPasswordResetEmail($request->email);

            if (isset($result['error'])) {
                return $this->responseJson($result['error'], $result['code']);
            }

            return $this->responseSuccess('Nếu email tồn tại, bạn sẽ nhận được hướng dẫn đặt lại mật khẩu');
        } catch (\Exception $e) {
            Log::error('Elearning forgot password error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }

    public function resetPassword(ElearningResetPasswordRequest $request)
    {
        try {
            $result = $this->authService->resetPassword(
                $request->token,
                $request->email,
                $request->password
            );

            if (isset($result['error'])) {
                return $this->responseJson($result['error'], $result['code']);
            }

            return $this->responseSuccess('Đặt lại mật khẩu thành công');
        } catch (\Exception $e) {
            Log::error('Elearning reset password error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }

    public function logout()
    {
        try {
            $userType = request()->get('user_type');
            $guard = $userType === 'learner' ? 'elearning' : 'api';
            auth()->guard($guard)->logout();

            return $this->responseSuccess('Đăng xuất thành công');
        } catch (\Exception $e) {
            Log::error('Elearning logout error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }

    public function refresh()
    {
        try {
            $userType = request()->get('user_type');
            $guard = $userType === 'learner' ? 'elearning' : 'api';
            $token = auth()->guard($guard)->refresh();

            return $this->responseSuccess('Token đã được làm mới', [
                'access_token' => $token,
                'token_type' => 'bearer',
            ]);
        } catch (\Exception $e) {
            Log::error('Elearning refresh error: ' . $e->getMessage());
            return $this->responseUnauthorized('Không thể làm mới token');
        }
    }

    public function profile()
    {
        try {
            $userType = request()->get('user_type');
            $profile = $this->authService->getProfile($userType);

            return $this->responseSuccess('Thành công', $profile);
        } catch (\Exception $e) {
            Log::error('Elearning profile error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }

    public function updateProfile(Request $request)
    {
        try {
            $userType = $request->get('user_type');

            if ($userType !== 'learner') {
                return $this->responseForbidden('Nhân viên không thể cập nhật profile từ Elearning');
            }

            $request->validate([
                'fullname' => 'sometimes|required|string|max:255',
                'phone' => ['nullable', 'string', 'regex:/^0[0-9]{9}$/'],
                'organization' => 'nullable|string|max:255',
            ]);

            $user = $this->authService->updateProfile($request->only(['fullname', 'phone', 'organization']));

            return $this->responseUpdated('Cập nhật thành công', [
                'id' => $user->id,
                'email' => $user->email,
                'fullname' => $user->fullname,
                'phone' => $user->phone,
                'organization' => $user->organization,
                'avatar' => $user->avatar,
            ]);
        } catch (\Exception $e) {
            Log::error('Elearning update profile error: ' . $e->getMessage());
            return $this->responseInternalServerError();
        }
    }
}
```

---

### Task 10: Routes — Đăng ký endpoints

**Files:**
- Modify: `Modules/Elearning/Routes/api.php`

- [x] **Step 1: Cập nhật routes**

```php
<?php
// Modules/Elearning/Routes/api.php

use Illuminate\Support\Facades\Route;
use Modules\Elearning\Http\Controllers\Api\V1\ElearningAuthController;

Route::prefix('v1/elearning')->group(function () {

    // Auth — Public
    Route::prefix('auth')->group(function () {
        Route::post('login', [ElearningAuthController::class, 'login']);
        Route::post('register', [ElearningAuthController::class, 'register']);
        Route::post('verify-email', [ElearningAuthController::class, 'verifyEmail']);
        Route::post('resend-verification', [ElearningAuthController::class, 'resendVerification']);
        Route::post('forgot-password', [ElearningAuthController::class, 'forgotPassword']);
        Route::post('reset-password', [ElearningAuthController::class, 'resetPassword']);
    });

    // Auth — Authenticated
    Route::prefix('auth')->middleware('elearning.auth')->group(function () {
        Route::post('logout', [ElearningAuthController::class, 'logout']);
        Route::post('refresh', [ElearningAuthController::class, 'refresh']);
        Route::get('profile', [ElearningAuthController::class, 'profile']);
        Route::put('profile', [ElearningAuthController::class, 'updateProfile']);
    });
});
```

- [x] **Step 2: Verify routes đăng ký thành công**

```bash
cd /Users/manhcuong/Desktop/dns/HRM/hrm-api
php artisan route:list --path=elearning
```

Expected: 10 routes elearning/auth/* hiển thị.

---

## Phase 3 — Frontend: Core Auth

### Task 11: Install axios + Tạo API utility

**Files:**
- Modify: `elearning/package.json` (thêm axios)
- Create: `elearning/src/utils/api.js`

- [x] **Step 1: Install axios**

```bash
cd /Users/manhcuong/Desktop/dns/HRM/elearning
npm install axios
```

- [x] **Step 2: Tạo .env**

```
# elearning/.env
VITE_API_URL=http://localhost:8000/api/v1/elearning
```

- [x] **Step 3: Tạo src/utils/api.js**

```js
// src/utils/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/elearning',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('elearning_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('elearning_token')
      const currentPath = window.location.pathname
      if (currentPath !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export default api
```

---

### Task 12: Auth Store (Pinia)

**Files:**
- Create: `elearning/src/stores/auth.js`

- [x] **Step 1: Tạo auth store**

```js
// src/stores/auth.js
import { defineStore } from 'pinia'
import api from '@/utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('elearning_token') || null,
    user: null,
    userType: null,
    loading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isEmployee: (state) => state.userType === 'employee',
    isLearner: (state) => state.userType === 'learner',
    userName: (state) => (state.user ? state.user.fullname : ''),
  },

  actions: {
    async login(email, password) {
      this.loading = true
      try {
        const { data } = await api.post('/auth/login', { email, password })
        this.token = data.data.access_token
        this.userType = data.data.user_type
        this.user = data.data.user
        localStorage.setItem('elearning_token', this.token)
        return { success: true }
      } catch (error) {
        const res = error.response?.data
        return { success: false, message: res?.message, errors: res?.errors }
      } finally {
        this.loading = false
      }
    },

    async register(formData) {
      this.loading = true
      try {
        const { data } = await api.post('/auth/register', formData)
        return { success: true, message: data.message }
      } catch (error) {
        const res = error.response?.data
        return { success: false, message: res?.message, errors: res?.errors }
      } finally {
        this.loading = false
      }
    },

    async fetchProfile() {
      if (!this.token) return
      try {
        const { data } = await api.get('/auth/profile')
        this.user = data.data
        this.userType = data.data.user_type
      } catch {
        this.clearAuth()
      }
    },

    async updateProfile(formData) {
      try {
        const { data } = await api.put('/auth/profile', formData)
        this.user = { ...this.user, ...data.data }
        return { success: true }
      } catch (error) {
        const res = error.response?.data
        return { success: false, message: res?.message, errors: res?.errors }
      }
    },

    async logout() {
      try {
        await api.post('/auth/logout')
      } catch {
        // ignore
      } finally {
        this.clearAuth()
      }
    },

    async refreshToken() {
      try {
        const { data } = await api.post('/auth/refresh')
        this.token = data.data.access_token
        localStorage.setItem('elearning_token', this.token)
      } catch {
        this.clearAuth()
      }
    },

    async initAuth() {
      if (this.token && !this.user) {
        await this.fetchProfile()
      }
    },

    clearAuth() {
      this.token = null
      this.user = null
      this.userType = null
      localStorage.removeItem('elearning_token')
    },
  },
})
```

---

### Task 13: Router — Auth routes + Navigation guard

**Files:**
- Modify: `elearning/src/router/index.js`

- [x] **Step 1: Cập nhật router**

```js
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { layout: 'auth', guest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
      meta: { layout: 'auth', guest: true },
    },
    {
      path: '/verify-email',
      name: 'verify-email',
      component: () => import('@/views/auth/VerifyEmailView.vue'),
      meta: { layout: 'auth' },
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/views/auth/ForgotPasswordView.vue'),
      meta: { layout: 'auth', guest: true },
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('@/views/auth/ResetPasswordView.vue'),
      meta: { layout: 'auth', guest: true },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const { useAuthStore } = await import('@/stores/auth')
  const auth = useAuthStore()

  await auth.initAuth()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  if (to.meta.guest && auth.isAuthenticated) {
    return next({ name: 'home' })
  }

  next()
})

export default router
```

---

### Task 14: Auth Layout

**Files:**
- Create: `elearning/src/layouts/AuthLayout.vue`
- Modify: `elearning/src/App.vue`

- [x] **Step 1: Tạo AuthLayout.vue**

```vue
<!-- src/layouts/AuthLayout.vue -->
<template>
  <div class="flex min-h-screen items-center justify-center bg-gradient-to-br from-brand/5 via-white to-brand-2/5">
    <div class="w-full max-w-[440px] px-4 py-8">
      <div class="mb-6 text-center">
        <router-link to="/">
          <img src="/TPE_LOGO.svg" alt="Logo" class="mx-auto h-[48px]" />
        </router-link>
      </div>
      <slot />
    </div>
    <AppToast />
  </div>
</template>

<script setup>
import AppToast from '@/components/layout/AppToast.vue'
</script>
```

- [x] **Step 2: Cập nhật App.vue để hỗ trợ multi-layout**

Đọc file `src/App.vue` hiện tại rồi cập nhật:

```vue
<!-- src/App.vue -->
<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

const route = useRoute()

const layouts = {
  default: DefaultLayout,
  auth: AuthLayout,
}

const layout = computed(() => layouts[route.meta.layout] || DefaultLayout)
</script>
```

---

## Phase 4 — Frontend: Auth Pages

### Task 15: LoginView

**Files:**
- Create: `elearning/src/views/auth/LoginView.vue`

- [x] **Step 1: Tạo LoginView.vue**

```vue
<!-- src/views/auth/LoginView.vue -->
<template>
  <div class="rounded-[14px] border border-line bg-white p-6 shadow-sm">
    <h1 class="mb-1 text-xl font-black text-ink">Đăng nhập</h1>
    <p class="mb-6 text-sm text-muted">Đăng nhập vào hệ thống Elearning</p>

    <div v-if="errorMessage" class="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <form @submit.prevent="handleLogin" novalidate>
      <div class="mb-4">
        <label class="mb-1.5 block text-sm font-bold text-ink">Email <span class="text-red-500">*</span></label>
        <input
          v-model="form.email"
          type="email"
          class="h-10 w-full rounded-[10px] border px-3 text-sm font-extrabold focus:outline-none"
          :class="touched && errors.email ? 'border-red-400 focus:border-red-400' : 'border-line focus:border-brand/45'"
          placeholder="Nhập email"
        />
        <p v-if="touched && errors.email" class="mt-1 text-xs text-red-500">{{ errors.email }}</p>
      </div>

      <div class="mb-4">
        <label class="mb-1.5 block text-sm font-bold text-ink">Mật khẩu <span class="text-red-500">*</span></label>
        <div class="relative">
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            class="h-10 w-full rounded-[10px] border px-3 pr-10 text-sm font-extrabold focus:outline-none"
            :class="touched && errors.password ? 'border-red-400 focus:border-red-400' : 'border-line focus:border-brand/45'"
            placeholder="Nhập mật khẩu"
          />
          <button
            type="button"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-ink"
            @click="showPassword = !showPassword"
          >
            <i :class="showPassword ? 'ri-eye-off-line' : 'ri-eye-line'"></i>
          </button>
        </div>
        <p v-if="touched && errors.password" class="mt-1 text-xs text-red-500">{{ errors.password }}</p>
      </div>

      <div class="mb-5 text-right">
        <router-link to="/forgot-password" class="text-sm font-bold text-brand hover:underline">Quên mật khẩu?</router-link>
      </div>

      <button
        type="submit"
        :disabled="auth.loading"
        class="flex h-10 w-full items-center justify-center rounded-[10px] bg-brand text-sm font-black text-white hover:bg-brand-2 disabled:opacity-50"
      >
        <i v-if="auth.loading" class="ri-loader-4-line animate-spin mr-2"></i>
        Đăng nhập
      </button>
    </form>

    <p class="mt-5 text-center text-sm text-muted">
      Chưa có tài khoản?
      <router-link to="/register" class="font-bold text-brand hover:underline">Đăng ký</router-link>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })
const errorMessage = ref('')
const touched = ref(false)
const showPassword = ref(false)

function validate() {
  errors.email = ''
  errors.password = ''
  if (!form.email) errors.email = 'Vui lòng nhập email'
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errors.email = 'Email không đúng định dạng'
  if (!form.password) errors.password = 'Vui lòng nhập mật khẩu'
  return !errors.email && !errors.password
}

async function handleLogin() {
  touched.value = true
  errorMessage.value = ''
  if (!validate()) return

  const result = await auth.login(form.email, form.password)
  if (result.success) {
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } else {
    errorMessage.value = result.message || 'Đăng nhập thất bại'
    if (result.errors) {
      Object.keys(result.errors).forEach((key) => {
        if (errors[key] !== undefined) {
          errors[key] = Array.isArray(result.errors[key]) ? result.errors[key][0] : result.errors[key]
        }
      })
    }
  }
}
</script>
```

---

### Task 16: RegisterView

**Files:**
- Create: `elearning/src/views/auth/RegisterView.vue`

- [x] **Step 1: Tạo RegisterView.vue**

```vue
<!-- src/views/auth/RegisterView.vue -->
<template>
  <div class="rounded-[14px] border border-line bg-white p-6 shadow-sm">
    <h1 class="mb-1 text-xl font-black text-ink">Đăng ký</h1>
    <p class="mb-6 text-sm text-muted">Tạo tài khoản Elearning mới</p>

    <div v-if="successMessage" class="mb-4 rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">
      {{ successMessage }}
      <router-link to="/login" class="font-bold underline">Đăng nhập</router-link>
    </div>

    <div v-if="errorMessage" class="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <form v-if="!successMessage" @submit.prevent="handleRegister" novalidate>
      <div class="mb-4">
        <label class="mb-1.5 block text-sm font-bold text-ink">Họ tên <span class="text-red-500">*</span></label>
        <input
          v-model="form.fullname"
          type="text"
          class="h-10 w-full rounded-[10px] border px-3 text-sm font-extrabold focus:outline-none"
          :class="touched && errors.fullname ? 'border-red-400' : 'border-line focus:border-brand/45'"
          placeholder="Nhập họ tên"
        />
        <p v-if="touched && errors.fullname" class="mt-1 text-xs text-red-500">{{ errors.fullname }}</p>
      </div>

      <div class="mb-4">
        <label class="mb-1.5 block text-sm font-bold text-ink">Email <span class="text-red-500">*</span></label>
        <input
          v-model="form.email"
          type="email"
          class="h-10 w-full rounded-[10px] border px-3 text-sm font-extrabold focus:outline-none"
          :class="touched && errors.email ? 'border-red-400' : 'border-line focus:border-brand/45'"
          placeholder="Nhập email"
        />
        <p v-if="touched && errors.email" class="mt-1 text-xs text-red-500">{{ errors.email }}</p>
      </div>

      <div class="mb-4">
        <label class="mb-1.5 block text-sm font-bold text-ink">Mật khẩu <span class="text-red-500">*</span></label>
        <div class="relative">
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            class="h-10 w-full rounded-[10px] border px-3 pr-10 text-sm font-extrabold focus:outline-none"
            :class="touched && errors.password ? 'border-red-400' : 'border-line focus:border-brand/45'"
            placeholder="Tối thiểu 8 ký tự"
          />
          <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-ink" @click="showPassword = !showPassword">
            <i :class="showPassword ? 'ri-eye-off-line' : 'ri-eye-line'"></i>
          </button>
        </div>
        <p v-if="touched && errors.password" class="mt-1 text-xs text-red-500">{{ errors.password }}</p>
      </div>

      <div class="mb-4">
        <label class="mb-1.5 block text-sm font-bold text-ink">Xác nhận mật khẩu <span class="text-red-500">*</span></label>
        <input
          v-model="form.password_confirmation"
          type="password"
          class="h-10 w-full rounded-[10px] border px-3 text-sm font-extrabold focus:outline-none"
          :class="touched && errors.password_confirmation ? 'border-red-400' : 'border-line focus:border-brand/45'"
          placeholder="Nhập lại mật khẩu"
        />
        <p v-if="touched && errors.password_confirmation" class="mt-1 text-xs text-red-500">{{ errors.password_confirmation }}</p>
      </div>

      <div class="mb-4">
        <label class="mb-1.5 block text-sm font-bold text-ink">Số điện thoại</label>
        <input
          v-model="form.phone"
          type="text"
          class="h-10 w-full rounded-[10px] border border-line px-3 text-sm font-extrabold focus:border-brand/45 focus:outline-none"
          placeholder="Nhập số điện thoại"
        />
        <p v-if="touched && errors.phone" class="mt-1 text-xs text-red-500">{{ errors.phone }}</p>
      </div>

      <div class="mb-5">
        <label class="mb-1.5 block text-sm font-bold text-ink">Đơn vị / Công ty</label>
        <input
          v-model="form.organization"
          type="text"
          class="h-10 w-full rounded-[10px] border border-line px-3 text-sm font-extrabold focus:border-brand/45 focus:outline-none"
          placeholder="Nhập tên đơn vị / công ty"
        />
      </div>

      <button
        type="submit"
        :disabled="auth.loading"
        class="flex h-10 w-full items-center justify-center rounded-[10px] bg-brand text-sm font-black text-white hover:bg-brand-2 disabled:opacity-50"
      >
        <i v-if="auth.loading" class="ri-loader-4-line animate-spin mr-2"></i>
        Đăng ký
      </button>
    </form>

    <p class="mt-5 text-center text-sm text-muted">
      Đã có tài khoản?
      <router-link to="/login" class="font-bold text-brand hover:underline">Đăng nhập</router-link>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const form = reactive({
  fullname: '',
  email: '',
  password: '',
  password_confirmation: '',
  phone: '',
  organization: '',
})
const errors = reactive({
  fullname: '',
  email: '',
  password: '',
  password_confirmation: '',
  phone: '',
})
const errorMessage = ref('')
const successMessage = ref('')
const touched = ref(false)
const showPassword = ref(false)

function validate() {
  Object.keys(errors).forEach((k) => (errors[k] = ''))
  if (!form.fullname) errors.fullname = 'Vui lòng nhập họ tên'
  if (!form.email) errors.email = 'Vui lòng nhập email'
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errors.email = 'Email không đúng định dạng'
  if (!form.password) errors.password = 'Vui lòng nhập mật khẩu'
  else if (form.password.length < 8) errors.password = 'Mật khẩu tối thiểu 8 ký tự'
  if (!form.password_confirmation) errors.password_confirmation = 'Vui lòng xác nhận mật khẩu'
  else if (form.password !== form.password_confirmation) errors.password_confirmation = 'Xác nhận mật khẩu không khớp'
  return Object.values(errors).every((e) => !e)
}

async function handleRegister() {
  touched.value = true
  errorMessage.value = ''
  if (!validate()) return

  const result = await auth.register(form)
  if (result.success) {
    successMessage.value = result.message || 'Đăng ký thành công! Vui lòng kiểm tra email để xác thực tài khoản.'
  } else {
    errorMessage.value = result.message || 'Đăng ký thất bại'
    if (result.errors) {
      Object.keys(result.errors).forEach((key) => {
        if (errors[key] !== undefined) {
          errors[key] = Array.isArray(result.errors[key]) ? result.errors[key][0] : result.errors[key]
        }
      })
    }
  }
}
</script>
```

---

### Task 17: VerifyEmailView

**Files:**
- Create: `elearning/src/views/auth/VerifyEmailView.vue`

- [x] **Step 1: Tạo VerifyEmailView.vue**

```vue
<!-- src/views/auth/VerifyEmailView.vue -->
<template>
  <div class="rounded-[14px] border border-line bg-white p-6 shadow-sm text-center">
    <div v-if="loading" class="py-8">
      <i class="ri-loader-4-line animate-spin text-3xl text-brand"></i>
      <p class="mt-3 text-sm text-muted">Đang xác thực email...</p>
    </div>

    <div v-else-if="success" class="py-4">
      <i class="ri-checkbox-circle-line text-5xl text-green-500"></i>
      <h2 class="mt-3 text-lg font-black text-ink">Xác thực thành công!</h2>
      <p class="mt-2 text-sm text-muted">Email của bạn đã được xác thực. Bạn có thể đăng nhập ngay bây giờ.</p>
      <router-link to="/login" class="mt-5 inline-flex h-10 items-center rounded-[10px] bg-brand px-5 text-sm font-black text-white hover:bg-brand-2">
        Đăng nhập
      </router-link>
    </div>

    <div v-else class="py-4">
      <i class="ri-close-circle-line text-5xl text-red-500"></i>
      <h2 class="mt-3 text-lg font-black text-ink">Xác thực thất bại</h2>
      <p class="mt-2 text-sm text-muted">{{ errorMessage }}</p>
      <div class="mt-5 flex items-center justify-center gap-3">
        <button
          v-if="showResend"
          :disabled="resending"
          class="inline-flex h-10 items-center rounded-[10px] border border-brand/25 bg-brand/[0.08] px-4 text-sm font-black text-brand hover:bg-brand/[0.12] disabled:opacity-50"
          @click="resendVerification"
        >
          <i v-if="resending" class="ri-loader-4-line animate-spin mr-2"></i>
          Gửi lại email xác thực
        </button>
        <router-link to="/login" class="inline-flex h-10 items-center rounded-[10px] border border-line bg-white px-4 text-sm font-black text-ink hover:bg-brand/5">
          Về trang đăng nhập
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from '@/composables/useToast'
import api from '@/utils/api'

const route = useRoute()
const toast = useToast()

const loading = ref(true)
const success = ref(false)
const errorMessage = ref('')
const showResend = ref(false)
const resending = ref(false)
const email = ref('')

onMounted(async () => {
  const token = route.query.token
  if (!token) {
    loading.value = false
    errorMessage.value = 'Token không hợp lệ'
    return
  }

  try {
    await api.post('/auth/verify-email', { token })
    success.value = true
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Xác thực thất bại'
    showResend.value = true
  } finally {
    loading.value = false
  }
})

async function resendVerification() {
  const inputEmail = prompt('Nhập email của bạn để gửi lại xác thực:')
  if (!inputEmail) return

  resending.value = true
  try {
    await api.post('/auth/resend-verification', { email: inputEmail })
    toast.show('Đã gửi lại email xác thực')
  } catch (error) {
    toast.show(error.response?.data?.message || 'Không thể gửi lại email')
  } finally {
    resending.value = false
  }
}
</script>
```

---

### Task 18: ForgotPasswordView

**Files:**
- Create: `elearning/src/views/auth/ForgotPasswordView.vue`

- [x] **Step 1: Tạo ForgotPasswordView.vue**

```vue
<!-- src/views/auth/ForgotPasswordView.vue -->
<template>
  <div class="rounded-[14px] border border-line bg-white p-6 shadow-sm">
    <h1 class="mb-1 text-xl font-black text-ink">Quên mật khẩu</h1>
    <p class="mb-6 text-sm text-muted">Nhập email để nhận hướng dẫn đặt lại mật khẩu</p>

    <div v-if="successMessage" class="mb-4 rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">
      {{ successMessage }}
    </div>

    <div v-if="errorMessage" class="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <form @submit.prevent="handleSubmit" novalidate>
      <div class="mb-5">
        <label class="mb-1.5 block text-sm font-bold text-ink">Email <span class="text-red-500">*</span></label>
        <input
          v-model="email"
          type="email"
          class="h-10 w-full rounded-[10px] border px-3 text-sm font-extrabold focus:outline-none"
          :class="touched && emailError ? 'border-red-400' : 'border-line focus:border-brand/45'"
          placeholder="Nhập email đã đăng ký"
        />
        <p v-if="touched && emailError" class="mt-1 text-xs text-red-500">{{ emailError }}</p>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="flex h-10 w-full items-center justify-center rounded-[10px] bg-brand text-sm font-black text-white hover:bg-brand-2 disabled:opacity-50"
      >
        <i v-if="loading" class="ri-loader-4-line animate-spin mr-2"></i>
        Gửi yêu cầu
      </button>
    </form>

    <p class="mt-5 text-center text-sm text-muted">
      <router-link to="/login" class="font-bold text-brand hover:underline">Quay lại đăng nhập</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/utils/api'

const email = ref('')
const emailError = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const loading = ref(false)
const touched = ref(false)

async function handleSubmit() {
  touched.value = true
  emailError.value = ''
  errorMessage.value = ''
  successMessage.value = ''

  if (!email.value) {
    emailError.value = 'Vui lòng nhập email'
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    emailError.value = 'Email không đúng định dạng'
    return
  }

  loading.value = true
  try {
    const { data } = await api.post('/auth/forgot-password', { email: email.value })
    successMessage.value = data.message || 'Vui lòng kiểm tra email để đặt lại mật khẩu'
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Có lỗi xảy ra'
  } finally {
    loading.value = false
  }
}
</script>
```

---

### Task 19: ResetPasswordView

**Files:**
- Create: `elearning/src/views/auth/ResetPasswordView.vue`

- [x] **Step 1: Tạo ResetPasswordView.vue**

```vue
<!-- src/views/auth/ResetPasswordView.vue -->
<template>
  <div class="rounded-[14px] border border-line bg-white p-6 shadow-sm">
    <h1 class="mb-1 text-xl font-black text-ink">Đặt lại mật khẩu</h1>
    <p class="mb-6 text-sm text-muted">Nhập mật khẩu mới cho tài khoản của bạn</p>

    <div v-if="successMessage" class="mb-4 rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">
      {{ successMessage }}
      <router-link to="/login" class="font-bold underline">Đăng nhập</router-link>
    </div>

    <div v-if="errorMessage" class="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
      {{ errorMessage }}
    </div>

    <form v-if="!successMessage" @submit.prevent="handleReset" novalidate>
      <div class="mb-4">
        <label class="mb-1.5 block text-sm font-bold text-ink">Mật khẩu mới <span class="text-red-500">*</span></label>
        <div class="relative">
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            class="h-10 w-full rounded-[10px] border px-3 pr-10 text-sm font-extrabold focus:outline-none"
            :class="touched && errors.password ? 'border-red-400' : 'border-line focus:border-brand/45'"
            placeholder="Tối thiểu 8 ký tự"
          />
          <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-ink" @click="showPassword = !showPassword">
            <i :class="showPassword ? 'ri-eye-off-line' : 'ri-eye-line'"></i>
          </button>
        </div>
        <p v-if="touched && errors.password" class="mt-1 text-xs text-red-500">{{ errors.password }}</p>
      </div>

      <div class="mb-5">
        <label class="mb-1.5 block text-sm font-bold text-ink">Xác nhận mật khẩu <span class="text-red-500">*</span></label>
        <input
          v-model="form.password_confirmation"
          type="password"
          class="h-10 w-full rounded-[10px] border border-line px-3 text-sm font-extrabold focus:border-brand/45 focus:outline-none"
          :class="touched && errors.password_confirmation ? 'border-red-400' : 'border-line'"
          placeholder="Nhập lại mật khẩu mới"
        />
        <p v-if="touched && errors.password_confirmation" class="mt-1 text-xs text-red-500">{{ errors.password_confirmation }}</p>
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="flex h-10 w-full items-center justify-center rounded-[10px] bg-brand text-sm font-black text-white hover:bg-brand-2 disabled:opacity-50"
      >
        <i v-if="loading" class="ri-loader-4-line animate-spin mr-2"></i>
        Đặt lại mật khẩu
      </button>
    </form>

    <p class="mt-5 text-center text-sm text-muted">
      <router-link to="/login" class="font-bold text-brand hover:underline">Quay lại đăng nhập</router-link>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/utils/api'

const route = useRoute()

const form = reactive({ password: '', password_confirmation: '' })
const errors = reactive({ password: '', password_confirmation: '' })
const errorMessage = ref('')
const successMessage = ref('')
const loading = ref(false)
const touched = ref(false)
const showPassword = ref(false)

function validate() {
  errors.password = ''
  errors.password_confirmation = ''
  if (!form.password) errors.password = 'Vui lòng nhập mật khẩu mới'
  else if (form.password.length < 8) errors.password = 'Mật khẩu tối thiểu 8 ký tự'
  if (!form.password_confirmation) errors.password_confirmation = 'Vui lòng xác nhận mật khẩu'
  else if (form.password !== form.password_confirmation) errors.password_confirmation = 'Xác nhận mật khẩu không khớp'
  return !errors.password && !errors.password_confirmation
}

async function handleReset() {
  touched.value = true
  errorMessage.value = ''
  if (!validate()) return

  loading.value = true
  try {
    const { data } = await api.post('/auth/reset-password', {
      token: route.query.token,
      email: route.query.email,
      password: form.password,
      password_confirmation: form.password_confirmation,
    })
    successMessage.value = data.message || 'Đặt lại mật khẩu thành công!'
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Có lỗi xảy ra'
  } finally {
    loading.value = false
  }
}
</script>
```

---

## Phase 5 — Frontend: Header Integration

### Task 20: Cập nhật AppHeader — User info + Login/Logout

**Files:**
- Modify: `elearning/src/components/layout/AppHeader.vue`

- [x] **Step 1: Cập nhật AppHeader.vue**

Thay thế nút User placeholder và thêm auth logic. Cần sửa phần `<script setup>` và phần nút User trong template.

**Thay thế nút User trong template** (dòng 23-24 hiện tại):

Thay:
```html
<button class="h-10 rounded-[10px] border border-line bg-white px-3 text-[13px] font-black text-[#0b2f67] inline-flex items-center gap-2 hover:bg-brand/5 hover:border-brand/20" @click="toast.show('Demo: Tài khoản')">
  <i class="ri-user-3-line"></i> User
</button>
```

Bằng:
```html
<!-- User đã đăng nhập -->
<div v-if="auth.isAuthenticated" class="relative group inline-flex">
  <button class="h-10 rounded-[10px] border border-line bg-white px-3 text-[13px] font-black text-[#0b2f67] inline-flex items-center gap-2 hover:bg-brand/5 hover:border-brand/20">
    <i class="ri-user-3-line"></i>
    <span class="hidden sm:inline max-w-[120px] truncate">{{ auth.userName }}</span>
    <span v-if="auth.isEmployee" class="hidden md:inline rounded-full bg-brand/10 px-2 py-0.5 text-[10px] font-black text-brand">NV</span>
    <span v-else class="hidden md:inline rounded-full bg-green-100 px-2 py-0.5 text-[10px] font-black text-green-700">HV</span>
    <i class="ri-arrow-down-s-line text-xs transition-transform group-hover:rotate-180"></i>
  </button>
  <div class="hidden group-hover:block absolute top-full right-0 min-w-[200px] bg-white rounded-xl shadow-lg py-2 z-[1000] border border-gray-200">
    <div class="px-4 py-2 border-b border-line">
      <p class="text-sm font-bold text-ink truncate">{{ auth.user?.fullname }}</p>
      <p class="text-xs text-muted truncate">{{ auth.user?.email }}</p>
    </div>
    <a href="#" class="flex items-center gap-2.5 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-[#f0f7ff] hover:text-brand" @click.prevent="toast.show('Demo: Profile')">
      <i class="ri-user-settings-line text-base text-muted"></i> Tài khoản
    </a>
    <a href="#" class="flex items-center gap-2.5 px-4 py-2 text-sm font-semibold text-red-600 hover:bg-red-50" @click.prevent="handleLogout">
      <i class="ri-logout-box-r-line text-base"></i> Đăng xuất
    </a>
  </div>
</div>
<!-- Chưa đăng nhập -->
<router-link
  v-else
  to="/login"
  class="h-10 rounded-[10px] border border-line bg-white px-3 text-[13px] font-black text-[#0b2f67] inline-flex items-center gap-2 hover:bg-brand/5 hover:border-brand/20"
>
  <i class="ri-user-3-line"></i> <span class="hidden sm:inline">Đăng nhập</span>
</router-link>
```

**Cập nhật `<script setup>`:**

Thay toàn bộ `<script setup>` bằng:

```html
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'
import { useAuthStore } from '@/stores/auth'

const toast = useToast()
const router = useRouter()
const auth = useAuthStore()
const searchQuery = ref('')

const trainingTypes = [
  { id: 'internal', name: 'Đào tạo nội bộ', icon: 'ri-building-2-line' },
  { id: 'onboarding', name: 'Đào tạo hội nhập', icon: 'ri-team-line' },
  { id: 'professional', name: 'Đào tạo chuyên môn', icon: 'ri-briefcase-line' },
  { id: 'softskill', name: 'Đào tạo kỹ năng mềm', icon: 'ri-chat-smile-2-line' },
  { id: 'safety', name: 'Đào tạo an toàn lao động', icon: 'ri-shield-check-line' },
]

const skillTypes = [
  { id: 'leadership', name: 'Kỹ năng lãnh đạo', icon: 'ri-user-star-line' },
  { id: 'communication', name: 'Kỹ năng giao tiếp', icon: 'ri-chat-3-line' },
  { id: 'teamwork', name: 'Kỹ năng làm việc nhóm', icon: 'ri-group-line' },
  { id: 'time-mgmt', name: 'Kỹ năng quản lý thời gian', icon: 'ri-time-line' },
  { id: 'problem-solving', name: 'Kỹ năng giải quyết vấn đề', icon: 'ri-focus-3-line' },
  { id: 'office-it', name: 'Kỹ năng tin học văn phòng', icon: 'ri-computer-line' },
]

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>
```

---

## Checkpoint cuối

- [x] **Verify BE**: `php artisan route:list --path=elearning` — 10 routes
- [x] **Verify FE**: `cd elearning && npm run dev` — app chạy, truy cập `/login`, `/register`
- [x] **Test login flow**: đăng nhập bằng email employee → nhận token + user_type=employee
- [x] **Test register flow**: đăng ký email mới → nhận email verify → click verify → login
- [x] **Test header**: sau login hiển thị tên + badge, logout hoạt động

### Checkpoint — 2026-05-12
Vừa hoàn thành: Tất cả 20 tasks (5 phases). Spec compliance review 30/30 ✅
Đang làm dở: không
Bước tiếp theo: User chạy migration + cấu hình ELEARNING_CLIENT_URL trong .env + test thủ công
Blocked: không
