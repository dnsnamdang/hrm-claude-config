# Skill: Elearning Validate / Error / Toast

Quy tắc xử lý validate, error response và thông báo (toast) cho project Elearning.
Áp dụng cho mọi form/API call trong `elearning/src/`.

> **Nguyên tắc cốt lõi:** FE KHÔNG validate trùng với BE. Submit thẳng, BE trả lỗi, FE render. Lỗi gắn field hiện inline; lỗi tổng quan + mọi thông báo thành công hiện toast.

---

## 1. Convention response BE

| HTTP status | Khi dùng | Body |
|---|---|---|
| **200** | Thành công có message | `{ code: 200, message: 'Đăng ký thành công', data: {...} }` |
| **422** | Lỗi validate field | `{ code: 422, errors: { email: 'Email đã tồn tại', password: '...' } }` |
| **423** | Lỗi nghiệp vụ tổng quan (KHÔNG gắn field cụ thể) | `{ code: 423, message: 'Sai mật khẩu', error_code?: 'email_not_verified' }` |
| **401** | Token invalid → axios interceptor tự xử lý | `{ code: 401, message: 'Unauthorized' }` |

**Quy tắc chọn 422 vs 423:**
- Lỗi sinh ra do giá trị 1 field cụ thể (định dạng, trùng, độ dài, mismatch) → **422 errors**
- Lỗi nghiệp vụ không gắn 1 field (sai credentials, account inactive, rate limit, không có quyền, token reset hết hạn, upload fail...) → **423 message**

## 2. Form Request BE

- Kế thừa `Modules\Elearning\Http\Requests\BaseRequest` (đã sẵn pattern trả 422)
- Khai báo `rules()` + `messages()` với message TIẾNG VIỆT đầy đủ cho từng rule
- Validate `password_confirmation` dùng rule `same:password` ở chính field `password_confirmation` (KHÔNG dùng `password.confirmed` vì lỗi sẽ gắn vào field `password`)

```php
public function rules() {
    return [
        'email' => 'required|email|max:255|unique:elearning_learners,email',
        'password' => 'required|string|min:8',
        'password_confirmation' => 'required|string|same:password',
    ];
}
public function messages() {
    return [
        'email.required' => 'Vui lòng nhập email',
        'email.email' => 'Email không đúng định dạng',
        'email.unique' => 'Email đã được sử dụng',
        'password.required' => 'Vui lòng nhập mật khẩu',
        'password.min' => 'Mật khẩu tối thiểu 8 ký tự',
        'password_confirmation.required' => 'Vui lòng xác nhận mật khẩu',
        'password_confirmation.same' => 'Mật khẩu xác nhận không khớp',
    ];
}
```

## 3. Controller trả lỗi tổng quan (423)

```php
return response()->json([
    'code' => 423,
    'message' => 'Email hoặc mật khẩu không đúng',
], 423);

// Nếu cần FE biết loại lỗi cụ thể (vd hiện CTA khác) — thêm error_code:
return response()->json([
    'code' => 423,
    'error_code' => 'email_not_verified',
    'message' => 'Email chưa được xác thực...',
    'email' => $email, // optional data kèm
], 423);
```

## 4. Action store Pinia — KHÔNG validate, return shape chuẩn

```js
async login(email, password) {
  try {
    const { data } = await api.post('/auth/login', { email, password })
    // ... set session
    return { success: true, message: data.message }
  } catch (error) {
    const res = error.response?.data
    return {
      success: false,
      message: res?.message,        // 423: message tổng
      errors: res?.errors,           // 422: { field: msg }
      errorCode: res?.error_code,    // (optional) phân biệt loại 423
      // ...field khác BE trả kèm nếu cần (vd email cho case email_not_verified)
    }
  }
}
```

## 5. View — dùng composable `useFormError` + `useToast`

```vue
<script setup>
import { reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useFormError } from '@/composables/useFormError'
import { useToast } from '@/composables/useToast'

const auth = useAuthStore()
const toast = useToast()
const form = reactive({ email: '', password: '' })

// Truyền danh sách field cần track inline error
const { fieldErrors, applyError, clearErrors } = useFormError(['email', 'password'])

async function handleSubmit() {
  clearErrors()
  const result = await auth.login(form.email, form.password)
  if (result.success) {
    toast.success('Đăng nhập thành công')
    // ... navigate
  } else {
    applyError(result)
    // → 422 errors: tự gắn vào fieldErrors.email, fieldErrors.password
    // → 423/network: tự push toast.error(message)
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" novalidate>
    <input
      v-model="form.email"
      :class="fieldErrors.email ? 'border-red-400' : 'border-line'"
    />
    <p v-if="fieldErrors.email" class="mt-1 text-xs text-red-500">{{ fieldErrors.email }}</p>

    <input
      v-model="form.password"
      :class="fieldErrors.password ? 'border-red-400' : 'border-line'"
    />
    <p v-if="fieldErrors.password" class="mt-1 text-xs text-red-500">{{ fieldErrors.password }}</p>

    <button type="submit" :disabled="auth.loading">Đăng nhập</button>
  </form>
</template>
```

**KHÔNG viết** các pattern này ở FE:
- Hàm `validate()` check email format / required / min length
- Cờ `touched`
- Banner `<div v-if="errorMessage">...</div>` cho lỗi tổng — phải dùng toast
- Banner `<div v-if="successMessage">...</div>` cho success — phải dùng toast

## 6. Toast usage

Composable `useToast` ở `src/composables/useToast.js`. 4 type:

```js
const toast = useToast()
toast.success('Đã lưu thành công')   // xanh, 3s
toast.error('Email đã tồn tại')       // đỏ, 4s
toast.warning('Cảnh báo')             // vàng, 3.5s
toast.info('Thông tin')               // trắng, 3s

// Custom duration
toast.success('Đã gửi mail xác thực', 5000)

// Custom (low-level)
toast.show('text', 'success', 3000)
toast.hide()
```

Toast component `AppToast.vue` đã render trong `DefaultLayout` + `AuthLayout` — không cần mount thêm. Vị trí: góc TRÊN-PHẢI màn hình.

## 7. Khi nào DÙNG TOAST vs KHI NÀO GIỮ BANNER

**Toast** (mặc định):
- Mọi thông báo thành công (đăng nhập, lưu, cập nhật, đổi mật khẩu, upload, đăng ký...)
- Mọi lỗi tổng quan (423, 401, 5xx, network error)
- Validation message ngoài danh sách field tracked

**Banner trong form** (chỉ giữ khi có 1 trong các yếu tố):
- Có **CTA button** đi kèm thông báo (vd: "Email chưa verify" + nút "Gửi lại mail")
- Là **page-level confirmation** không có form (vd: VerifyEmailView, SsoView khi load)
- Là **instruction kéo dài** sau action không nên biến mất (vd: sau register hiện "Vào hộp thư X để bấm liên kết")

Khi giữ banner, dùng style chuẩn:
```html
<!-- Banner cảnh báo (amber) -->
<div class="mb-4 rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-700">...</div>
<!-- Banner thông tin/instruction (emerald) -->
<div class="mb-4 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">...</div>
<!-- Banner lỗi (đỏ) — chỉ dùng cho page-level error -->
<div class="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">...</div>
```

## 8. Pitfall — Vue boolean attribute `disabled`

`:disabled="loading || successMessage"` — khi `loading=false` và `successMessage=''`, expression = `''` (empty string). Vue **KHÔNG** remove attribute với value rỗng → button bị disabled.

**Fix:** ép boolean rõ ràng:
```vue
:disabled="loading || !!successMessage"
:disabled="!!loading || done"
```

## 9. Checklist trước khi commit form mới

- [ ] BE Form Request có rules + messages tiếng Việt đầy đủ
- [ ] Controller: lỗi nghiệp vụ trả 423, lỗi field trả 422 (tự động qua BaseRequest)
- [ ] Store action không validate, return `{success, message?, errors?, errorCode?}`
- [ ] View dùng `useFormError(['field1', 'field2', ...])` + `useToast()`
- [ ] KHÔNG còn hàm `validate()`, cờ `touched`, banner success/error tổng
- [ ] Field error hiện inline; success/general error hiện toast
- [ ] `:disabled` đã ép boolean nếu có chuỗi rỗng
