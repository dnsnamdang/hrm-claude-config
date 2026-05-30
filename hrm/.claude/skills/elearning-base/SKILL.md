# Skill: Elearning Base Convention

Quy tắc nền tảng khi làm việc với project Elearning (Vue 3 + Vite). Đọc skill này TRƯỚC khi viết code mới cho elearning.

> Đây là project học trực tuyến CỦA RIÊNG, **KHÔNG** dùng chung pattern V2Base/Bootstrap 4 với hrm-client (Nuxt 2). Code rất khác với phần còn lại của hệ thống HRM.

---

## 1. Tech stack

| | |
|---|---|
| Framework | **Vue 3.5 + Vite 5** (Composition API `<script setup>`) |
| Router | Vue Router 4 |
| State | Pinia 3 |
| Styling | **Tailwind CSS 3.4** — KHÔNG Bootstrap, KHÔNG SCSS module |
| Icons | **Remix Icon** (`ri-*`) là chính |
| HTTP | axios (instance `api` + `hrmApi` ở `src/utils/api.js`) |
| BE | Laravel 8 — module `Modules/Elearning` trong `hrm-api` |

---

## 2. Cấu trúc thư mục `elearning/src/`

```
src/
├── components/
│   ├── base/          # Tái sử dụng nhiều nơi (LearnCard, CategoryCard...)
│   ├── layout/        # AppHeader, AppFooter, AppToast
│   └── [page-name]/   # Component riêng từng page
├── composables/       # Shared logic: useToast, useFormError, useCompanyLogo...
├── constants/         # Enum, status, mockData
├── layouts/           # DefaultLayout (có header), AuthLayout (page auth)
├── router/            # 1 file index.js
├── stores/            # Pinia: auth.js, elearning.js, ...
├── utils/             # api.js, common helpers
└── views/             # Page-level component
```

---

## 3. Convention component Vue

- Dùng `<script setup>` Composition API
- Props khai báo qua `defineProps()` có type + default
- Emits qua `defineEmits()`
- File PascalCase: `LearnCard.vue`, `HeroBanner.vue`
- Component dùng > 1 nơi → `components/base/`
- Component riêng 1 page → `components/[page-name]/`

## 4. Convention store Pinia

- Mỗi domain 1 store: `useAuthStore`, `useCourseStore`...
- File: `src/stores/<domain>.js`
- Action **không validate** — submit thẳng lên BE, trả về object có shape:
  ```js
  { success: true, message?, data? }
  // hoặc
  { success: false, message?, errors? /* {field: msg} */, errorCode? /* tùy lỗi */ }
  ```
- Action gọi API qua `api` instance (`@/utils/api`); gọi sang HRM legacy → `hrmApi`

## 5. Tailwind class patterns hay dùng

```
Card:        "border border-line rounded-[14px] bg-white hover:border-brand/25 transition"
Button primary: "h-10 rounded-[10px] bg-brand text-sm font-black text-white hover:bg-brand-2 disabled:opacity-50"
Button outline: "h-10 rounded-[10px] border border-line bg-white text-[13px] font-black text-[#0b2f67] hover:bg-brand/5"
Pill/Badge:  "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1.5 text-xs font-black"
Input:       "h-10 w-full rounded-[10px] border px-3 text-sm font-extrabold focus:outline-none border-line focus:border-brand/45"
Input error: "border-red-400 focus:border-red-400"
```

Token màu: `brand`, `brand-2`, `ink`, `muted`, `line` (xem `tailwind.config.js`).

## 6. Convention router

- Thêm route ở `src/router/index.js`, lazy-load `() => import('@/views/...')`
- `meta.guest: true` cho trang public; `meta.layout: 'auth'` để dùng AuthLayout
- Route bảo vệ → KHÔNG khai báo gì, mặc định sẽ qua SSO check (xem skill `elearning-auth`)

## 7. Convention API

- Base URL: `${VITE_API_URL}/v1/elearning` cho API elearning
- Base URL phụ: `${VITE_HRM_API_URL}/v1` cho API HRM legacy (login, logout HRM, master-settings)
- Bearer token tự inject qua axios interceptor (đọc `localStorage.elearning_token`)
- 401 → axios interceptor tự refresh, fail thì clear + redirect `/login`
- Format response BE chuẩn:
  ```json
  // Success
  { "code": 200, "message": "...", "data": {...} }
  // Lỗi field validation
  { "code": 422, "errors": { "email": "Email đã tồn tại" } }
  // Lỗi tổng quan
  { "code": 423, "message": "..." }
  ```

## 8. Backend (`Modules/Elearning`)

- Path: `hrm-api/Modules/Elearning/`
- Cấu trúc chuẩn Laravel module: `Entities/`, `Http/Controllers/Api/V1/`, `Http/Requests/`, `Http/Middleware/`, `Services/`, `Transformers/`, `Routes/api.php`, `Database/Migrations/`, `Mail/`, `Resources/views/`
- Route prefix: `v1/elearning`
- Controller extends `App\Http\Controllers\Controller`, **KHÔNG** extends ApiController của HRM (vì response format hơi khác — không cần `responseJson` helper)
- Form Request kế thừa `Modules\Elearning\Http\Requests\BaseRequest` (đã sẵn pattern 422)
- Service tách logic, transaction wrap đầy đủ
- Middleware auth route: `'elearning.auth'` (multi-guard, xem skill `elearning-auth`)

## 9. KHÔNG làm

- Không dùng Bootstrap/SCSS module trong elearning
- Không dùng V2Base components (đó là của hrm-client)
- Không tự validate ở FE — submit thẳng, BE handle (xem skill `elearning-validate`)
- Không hardcode chuỗi tiếng Việt vào logic — tách constants nếu là enum/status
- Không tạo ApiController custom — dùng `Controller` cơ bản

## 10. Skill liên quan

| Khi làm gì | Đọc skill |
|---|---|
| Validate form, error handling, toast | `elearning-validate` |
| Auth, SSO, profile, avatar | `elearning-auth` |
