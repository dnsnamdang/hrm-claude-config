---
name: playwright-setup
description: Chuẩn team để Claude Code tự setup Playwright E2E cho 1 project. Dùng khi user yêu cầu "cài/thêm Playwright", "viết test e2e", "setup test tự động", hoặc khi cần kiểm thử luồng FE. Mặc định stack Nuxt 2 + Vue 2 + Select2 + JWT; xem mục cuối nếu project dùng AngularJS/Blade (ERP).
---

# Playwright E2E — Chuẩn setup của team

> Đây là chuẩn dùng chung. Khi user yêu cầu cài Playwright / thêm test e2e cho project này, **làm theo skill này**, không tự nghĩ kiểu khác. Đã áp dụng thực tế: `nhatlinh/e2e/`, `HRM/e2e/`.

## Nguyên tắc bất biến (KHÔNG được vi phạm)

1. **Test ở thư mục riêng `e2e/`** ngang hàng client/api — KHÔNG cài vào `node_modules` của app.
2. **Node 20** cho test (`.nvmrc`), cài `@playwright/test` **local**. App Nuxt vẫn Node 14, không đụng.
   - Lý do: Playwright cần Node ≥18; app cũ chạy Node 12/14. Cài chung hoặc dùng Playwright **global** = nguồn gốc lỗi "phải cài lại Playwright" → tuyệt đối tránh.
3. **Auth qua `storageState`**: login UI 1 lần (`auth/login.setup.ts`) → lưu token → mọi test tái dùng.
4. **Page Object Model**: mỗi trang 1 class trong `pages/`, selector + thao tác gom 1 nơi.
5. **KHÔNG `webServer` auto** (app Node 14, test Node 20 — xung đột). User tự chạy `npm run dev`.
6. **KHÔNG sửa file `.vue`** để thêm `data-testid` mà chưa hỏi user.
7. **KHÔNG commit** `.env`, `.auth/`, `playwright-report/`, `trace.zip`, `screenshots/`.

## Quy trình setup (làm theo thứ tự)

1. Tạo `e2e/` cạnh app: `mkdir -p <project>/e2e`.
2. Tạo các file template ở mục **Templates** bên dưới.
3. Cài: `cd e2e && nvm use && npm install && npx playwright install chromium`.
4. `cp .env.sample .env` → điền `TEST_EMAIL`/`TEST_PASSWORD` (tài khoản test trên DB local).
5. Sửa `pages/LoginPage.ts` cho khớp trang login thật (placeholder, text nút).
6. Verify không cần app: `npx playwright test --list` (phải liệt kê test, không lỗi config/TS).
7. Báo user bật FE + API rồi mới chạy `npm test` (xem mục Chạy).

## Templates

### `.nvmrc`
```
20
```

### `package.json`
```json
{
  "name": "<project>-e2e",
  "private": true,
  "version": "1.0.0",
  "scripts": {
    "test": "playwright test",
    "test:ui": "playwright test --ui",
    "test:headed": "playwright test --headed",
    "test:debug": "playwright test --debug",
    "report": "playwright show-report",
    "codegen": "playwright codegen http://127.0.0.1:3000"
  },
  "devDependencies": {
    "@playwright/test": "^1.50.0",
    "@types/node": "^20.11.0",
    "dotenv": "^16.4.0"
  }
}
```

### `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2021", "module": "commonjs", "moduleResolution": "node",
    "esModuleInterop": true, "strict": true, "skipLibCheck": true,
    "resolveJsonModule": true, "types": ["node"]
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "legacy"]
}
```

### `.gitignore`
```
node_modules/
.auth/
playwright-report/
test-results/
.env
trace.zip
screenshots/
```

### `.env.sample`
```
BASE_URL=http://127.0.0.1:3000
TEST_EMAIL=<tài_khoản_test>
TEST_PASSWORD=<mật_khẩu>
```

### `playwright.config.ts`
```ts
import { defineConfig, devices } from '@playwright/test';
import 'dotenv/config';

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:3000';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: BASE_URL,
    viewport: { width: 1440, height: 900 },
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 15000,
  },
  projects: [
    // login.setup.ts nằm trong ./auth → phải override testDir, nếu không project setup không thấy file
    { name: 'setup', testDir: './auth', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
  ],
  // KHÔNG webServer auto: app Nuxt Node 14, e2e Node 20.
});
```

### `auth/login.setup.ts`
```ts
import { test as setup } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

const authFile = '.auth/user.json';

setup('authenticate', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login(process.env.TEST_EMAIL!, process.env.TEST_PASSWORD!);
  await page.context().storageState({ path: authFile }); // lưu cookie + localStorage (JWT)
});
```

### `pages/LoginPage.ts` (sửa placeholder/text nút cho khớp project)
```ts
import { Page, expect } from '@playwright/test';

export class LoginPage {
  constructor(private readonly page: Page) {}

  async goto() {
    await this.page.goto('/login', { waitUntil: 'domcontentloaded' });
    await expect(this.page.getByPlaceholder('Địa chỉ email')).toBeVisible({ timeout: 15000 });
  }

  async login(email: string, password: string) {
    await this.page.getByPlaceholder('Địa chỉ email').fill(email);
    await this.page.getByPlaceholder('Mật khẩu').first().fill(password);
    await this.page.getByRole('button', { name: 'Đăng nhập' }).click();
    await this.page.waitForURL((url) => !url.pathname.includes('/login'), { timeout: 20000 });
  }
}
```

> **Lưu ý ô mật khẩu show/hide:** nhiều trang login có nút ẩn/hiện mật khẩu, tạo **2 input cùng `placeholder="Mật khẩu"`** (1 `type=password` + 1 `type=text`, hoặc 1 bản bị comment trong DOM). `.first()` có thể trỏ ô đang ẩn → mật khẩu không vào ô thật → BE trả 422. Kiểm chắc ăn: sau `fill`, assert `(await field.inputValue()).length > 0`; nếu sai, target ô hiển thị (`locator('input[type="password"]:visible')`).

## Helper cho stack team — `utils/select2.ts`

Stack team dùng **Select2 (`v-select2-component`)** + **vue2-datepicker** (khó tự động hoá). Copy nguyên file này vào mọi project Nuxt:

```ts
import { Page } from '@playwright/test';

/** Chọn option trong Select2. currentText = text ô đang hiển thị; optionText = option cần chọn (bỏ trống → option đầu). Options nạp async → retry 4 lần. */
export async function pickSelect2(page: Page, currentText: string, optionText?: string): Promise<string | null> {
  const rendered = page.locator('.select2-selection__rendered', { hasText: currentText }).first();
  await rendered.waitFor({ state: 'visible', timeout: 8000 });
  const realOption = () =>
    optionText
      ? page.locator('li.select2-results__option', { hasText: optionText }).first()
      : page.locator('li.select2-results__option:not(.select2-results__message)').first();

  let chosen: string | null = null;
  for (let attempt = 1; attempt <= 4; attempt++) {
    await rendered.click();
    await page.locator('.select2-results').first().waitFor({ state: 'visible', timeout: 8000 });
    const search = page.locator('.select2-search__field');
    if (optionText && (await search.count()) && (await search.first().isVisible())) {
      await search.first().fill(optionText);
      await page.waitForTimeout(400);
    }
    try {
      await realOption().waitFor({ state: 'visible', timeout: 4000 });
      chosen = (await realOption().textContent())?.trim() ?? null;
      await realOption().click();
      break;
    } catch (e) {
      await page.keyboard.press('Escape').catch(() => {});
      await page.waitForTimeout(1500);
      if (attempt === 4) throw new Error(`Select2 "${currentText}" không có option sau 4 lần thử`);
    }
  }
  await page.locator('.select2-results').first().waitFor({ state: 'hidden', timeout: 5000 }).catch(() => {});
  return chosen;
}

/** Điền vue2-datepicker (.mx-input) theo thứ tự (idx 0 = ô đầu). */
export async function fillDate(page: Page, idx: number, ddmmyyyy: string): Promise<void> {
  const input = page.locator('.mx-input').nth(idx);
  await input.click();
  await input.fill(ddmmyyyy);
  await page.keyboard.press('Enter');
  await page.keyboard.press('Escape').catch(() => {});
}

export function todayDDMMYYYY(): string {
  const d = new Date();
  const p = (n: number) => String(n).padStart(2, '0');
  return `${p(d.getDate())}/${p(d.getMonth() + 1)}/${d.getFullYear()}`;
}
```

**Selector hay dùng (Bootstrap-Vue + V2Base):** currency `.v2-currency-input` · footer nút Lưu `.V2Footer button` · modal `.modal`/`.modal-card`/`.modal-footer` · icon `.ri-...`.

## Viết test (Page Object Model)

`pages/<Entity>Page.ts` gom selector + thao tác; `tests/<module>/<flow>.spec.ts` chỉ gọi method.

```ts
// pages/SomePage.ts
import { Page, expect } from '@playwright/test';
import { pickSelect2 } from '../utils/select2';

export class SomePage {
  constructor(private readonly page: Page) {}
  async gotoList() {
    await this.page.goto('/<route>', { waitUntil: 'domcontentloaded' });
    await this.page.getByRole('button', { name: 'Tạo mới' }).waitFor({ timeout: 15000 });
  }
  async selectFirstCustomer() { return pickSelect2(this.page, 'Chọn khách hàng'); }
}
```
```ts
// tests/<module>/<flow>.spec.ts
import { test, expect } from '@playwright/test';
import { SomePage } from '../../pages/SomePage';

test.describe('<Module> — <nghiệp vụ>', () => {
  test('<mô tả test tiếng Việt>', async ({ page }) => {
    const p = new SomePage(page);
    await p.gotoList();
    // ... thao tác + expect ...
  });
});
```

**Thứ tự ưu tiên selector:** `getByRole` → `getByLabel`/`getByPlaceholder` → `getByText` → `data-testid` (chỉ khi bí, hỏi trước) → CSS/XPath (tránh). Bí → gợi ý user chạy `npm run codegen`.

## Chạy test

Cần FE + API đang chạy (test không tự dựng app):
```bash
# terminal A: cd <client> && nvm use 14 && npm run dev   # 127.0.0.1:3000
# terminal B: cd <api> && php artisan serve              # 127.0.0.1:8000
cd e2e && nvm use
npm test            # headless
npm run test:ui     # debug trực quan (khuyến nghị khi viết test)
npm run report      # xem HTML report (trace + screenshot khi fail)
npm run codegen     # tự sinh selector
```

## Tài khoản test — mô hình auth & cách tạo (nếu chưa có)

Bước 4 (điền `.env`) chỉ chạy nếu **có tài khoản hợp lệ trên DB local**. Nếu login fail, hiểu mô hình auth thật trước khi loay hoay:

**Mô hình auth (Nuxt + JWT tymon + spatie tùy biến):**
- Login: `POST /api/v1/users/auth/login` body `{email,password}` → `auth()->attempt(['email','password','status'=>1])`. Account **phải `status=1`**. Response `{ meta:{code,message}, data:{ access_token,... } }` — token key = **`access_token`**; sai creds → **422** `"Tên đăng nhập hoặc mật khẩu không đúng"` (KHÔNG phải 401).
- **Xác thực bằng bảng `employees`** (KHÔNG phải `users`). User và Employee là **cùng 1 bản ghi** (`auth()->user()->id == Employee::find(id)->id`).
- Quyền qua bảng tùy biến **`employee_has_roles`** (cột `role_id, model_type, employee_id, company_id`; morph key = `employee_id`, model_type = `Modules\Timesheet\Entities\Employee`) — KHÔNG phải `model_has_roles` mặc định. `role_has_permissions` có thêm cột `company_id`.

**Tạo user E2E chuyên dụng** (idempotent — đặt script ở `<api>/database/e2e_provision.php`, chạy `php artisan tinker --execute="require base_path('database/e2e_provision.php');"`):
```php
$infoId = DB::table('employee_infos')->insertGetId([
    'code'=>'E2E','fullname'=>'E2E User','image'=>'e2e.png','telephone'=>'0900000000',
    'company_id'=>1,'department_id'=>1,'status'=>1,'created_at'=>now(),'updated_at'=>now(),
]);
$empId = DB::table('employees')->insertGetId([
    'email'=>'e2e@test.local','password'=>Hash::make('Password@123'),'status'=>1,
    'employee_info_id'=>$infoId,'created_at'=>now(),'updated_at'=>now(),
]);
DB::table('company_employees')->insert(['employee_id'=>$empId,'company_id'=>1]); // BẮT BUỘC: thiếu → login crash null
DB::table('employee_has_roles')->insert([
    'role_id'=>1,'model_type'=>'Modules\\Timesheet\\Entities\\Employee','employee_id'=>$empId,'company_id'=>1,
]); // role 1 = Admin (đủ quyền). Đổi role_id nếu cần quyền hẹp hơn để test 403.
app(\Spatie\Permission\PermissionRegistrar::class)->forgetCachedPermissions(); // cache spatie 24h
```
Gotcha: `employee_infos.image` NOT NULL (+CHECK) → giá trị **khác rỗng** (vd `'e2e.png'`). `company_employees` bắt buộc. Sau insert **phải reset cache spatie**. Rồi `.env`: `TEST_EMAIL=e2e@test.local` / `TEST_PASSWORD=Password@123`. **KHÔNG đoán mật khẩu tài khoản thật** — tạo user E2E.

## Tùy chọn: E2E API-level (khi FE chưa dựng được)

Khi FE không chạy được (Node cũ, build lỗi node-sass/openssl) nhưng cần kiểm luồng nghiệp vụ ngay, dùng Playwright `request` gọi thẳng API (vẫn trong `e2e/`, Node 20):
- `globalSetup`: provision user+fixtures (shell `php artisan tinker`) → login lấy `access_token` → ghi `.auth/state.json` (token + id fixtures).
- Test đọc token → header `Authorization: Bearer <token>`, gọi endpoint thật, assert `status()` + JSON. Fixtures tạo mới mỗi lần → đọc id từ `state.json`, KHÔNG hardcode.
- Lỗi nghiệp vụ (validate, vượt tồn, vượt hạn mức HĐ) BE trả **422** (Controller rethrow `ValidationException` trước `catch Exception`) — assert **422**, không phải 400. Không token → **401**.
- Ưu: không cần FE/Select2/datepicker, chạy nhanh, ổn định. Nhược: không kiểm Vue render. Có thể chạy song song với UI test trong cùng `e2e/` (project Playwright riêng).
- Lưu ý DB dev có thể thiếu bảng phụ (vd `customer_categories` chưa migrate → `GET /sale/contracts/{id}` 500 do eager-load): né bằng cách assert qua endpoint khác (vd `issued`/`remaining`) thay vì gọi đúng endpoint lỗi.

## Nếu project dùng AngularJS/Blade (ERP — KHÁC stack)

Nguyên tắc 1–7 vẫn giữ nguyên (e2e riêng, Node 20, local, storageState, POM). Chỉ khác **selector**:
- Login: dò bằng `npm run codegen` (không chắc placeholder "Địa chỉ email").
- Select2 là **jQuery select2** (không phải `v-select2-component`) — class `.select2-results__option` thường vẫn dùng được, nhưng kiểm tra lại.
- KHÔNG có `vue2-datepicker` (`.mx-input`) / `.v2-currency-input` / `.V2Footer` — bỏ helper tương ứng, dò selector thật.
- DataTable server-side (Yajra) → chờ `networkidle` sau search.
→ Vẫn theo skill này về cấu trúc; chỉ thay phần selector bằng codegen trên app thật.

## Troubleshooting nhanh

| Triệu chứng | Xử lý |
| --- | --- |
| `SyntaxError`/lệnh không chạy | Sai Node → `nvm use` (Node 20). Không chạy Node 12/14. |
| `ERR_CONNECTION_REFUSED` | Chưa bật `npm run dev` (FE). |
| Bị đẩy về `/login` | Token hết hạn → xóa `.auth/user.json`, chạy lại. |
| "phải cài lại Playwright" tái diễn | Đang dùng bản global → cài **local** trong `e2e/package.json`. |
| Select2 không có option | Tăng `waitForTimeout` ở bước mở form, hoặc truyền `optionText` để search. |
| Click bị overlay/toast che | `.click({ force: true })` fallback. |
| Mọi test fail `ENOENT '.auth/user.json'` | Project `setup` không chạy: file `login.setup.ts` nằm trong `./auth` (ngoài `testDir: './tests'`). Đảm bảo project `setup` có **`testDir: './auth'`** (đã có trong template). Verify: `npx playwright test --list` phải thấy `[setup]`. |
| Login API trả **422** "...mật khẩu không đúng" | Sai creds, account không `status=1`, hoặc account không có trong bảng `employees` (auth KHÔNG dùng bảng `users`). Xem mục "Tài khoản test" → tạo user E2E chuyên dụng, KHÔNG đoán mật khẩu. |
| Ô mật khẩu trống dù đã `fill` | Nút show/hide tạo 2 input trùng `placeholder="Mật khẩu"` → `.first()` trỏ ô ẩn. Target `input[type="password"]:visible`; assert `inputValue().length>0` sau fill. |
| `getAllPermissions()`/quyền không có dù đã gán role | Reset cache spatie: `php artisan permission:cache-reset` (hoặc `forgetCachedPermissions()`); roles gắn qua `employee_has_roles` (không phải `model_has_roles`). |
