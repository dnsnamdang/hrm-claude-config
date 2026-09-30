# Import / Export cho các màn Danh mục ERP → HRM — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm Import file Excel cho 13 màn Danh mục và Xuất Excel cho 9 màn Danh mục đã chuyển từ ERP sang HRM.

**Architecture:** Không dựng framework mới. Import đi qua `V2BaseImportModal` (luồng 4 bước có sẵn) + một mixin FE dùng chung được đổi tên từ `FinanceImportMixin` thành `CatalogImportMixin`; file mẫu sinh ngay tại FE từ chính `importColumns` của màn. Export đi qua `ExportColumnRegistry` + `DynamicExport` ở BE, riêng màn Phường/xã dựng file ở FE bằng ExcelJS theo lô vì bảng có 13.465 dòng.

**Tech Stack:** Laravel 8 + nwidart/laravel-modules + maatwebsite/excel (BE) · Nuxt 2 / Vue 2 + BootstrapVue + SheetJS `XLSX` 0.20.3 (global qua CDN) + ExcelJS 4.4 (FE) · PHPUnit 9.5 (chạy theo đường dẫn file)

**Spec:** [docs/superpowers/specs/gop-db/2026-09-10-catalog-import-export-design.md](../../../docs/superpowers/specs/gop-db/2026-09-10-catalog-import-export-design.md)

---

## Global Constraints

Mọi task đều phải tuân theo, không nhắc lại ở từng task:

- **Nhánh:** `feat/catalog-import-export`, tách từ `gop_db`. Tạo ở **cả hai** repo `hrm-api` và `hrm-client`.
- **KHÔNG commit, KHÔNG push.** Rule dự án: AI không xử lý git commit. Làm xong mỗi task thì báo user, user tự commit.
- **Ngôn ngữ:** mọi thông báo, nhãn, comment code viết bằng tiếng Việt.
- **Import chỉ THÊM MỚI.** Dòng trùng → `isValid = false`, lý do "… đã tồn tại trong hệ thống"; dòng hợp lệ vẫn được tạo. Không upsert, không all-or-nothing.
- **Server validate lại toàn bộ** trong `import()` trước khi ghi, không tin kết quả validate từ FE.
- **Mỗi dòng bọc try/catch riêng** trong `import()`; cả lượt nằm trong `DB::transaction` ở controller.
- **Không tự tạo bản ghi cha.** Tra cứu theo mã không thấy → báo lỗi dòng đó.
- **Nút Import gate quyền giống hệt nút "Tạo mới" của chính màn đó.** Màn nào nút Tạo mới có `v-if="canManage"` thì nút Import cũng vậy; màn nào không gate (5 màn Nhân sự) thì Import cũng không gate — **CẤM hard-code cờ quyền giả**.
- **Chữ trên nút / màu / icon** theo skill `button-convention`: nút Import dùng `secondary status="warning"` + icon `ri-upload-line` + chữ "Import Excel", đặt ngay sau nút "Xuất Excel" trong `<template #actions-bottom>`.
- **Cột Trạng thái trong file Excel** nhận `Hoạt động` / `Khóa`, chuẩn hoá không phân biệt hoa thường và dấu.
- **Route tĩnh đặt TRƯỚC route wildcard** `/{id}` trong file routes, nếu không sẽ bị nuốt.
- **MySQL local đang tắt lúc viết plan.** Trước khi làm Phase 2, bật MySQL và chạy lại lệnh đối chiếu ràng buộc `unique` ở Task 3.

---

## ĐÍNH CHÍNH khoá chống trùng — đối chiếu DB + FormRequest thật, 11/09/2026

> Chạy ở Task 3 Step 7. **Bảng này THẮNG mọi khối `«rules»` viết trong các task bên dưới.**
> Chỗ nào task ghi khác thì sửa theo bảng này.

**Phát hiện nền tảng:** trong 13 bảng, **chỉ `source_capitals.name` có UNIQUE index thật ở DB**.
12 bảng còn lại không có unique nào ngoài khoá chính → quy tắc chống trùng nằm hoàn toàn ở tầng
ứng dụng (FormRequest). Vì vậy `validateRows()` phải bám **đúng rule của FormRequest màn đó**, không
suy từ DB, và cũng không được kỳ vọng DB chặn giúp.

| Màn | Khoá chống trùng THỰC TẾ | Nguồn |
| --- | --- | --- |
| Tiền tệ | **`code` VÀ `name`** — cả hai đều unique | `Finance/Http/Requests/Currency/CurrencyRequest.php:57,62` |
| Tài khoản ngân hàng | `account_number` | `CompanyAccountRequest.php:24` |
| Vụ việc | `code` | `WorkRequest.php:19` |
| Mã phí | `code` | `CostDebtRequest.php:19` |
| Nguồn vốn | `name` (unique thật ở DB) | `SourceCapitalRequest.php:18` |
| Quốc gia | **`name` VÀ mã** — mã lưu ở cột **`country_code`**, bảng KHÔNG có cột `code` | `CreateNationRequest.php:21,27` |
| Khu vực | **`name` unique TOÀN CỤC**, không phải theo quốc gia | `CreateAreasRequest.php:21` |
| Tỉnh/TP | **`name` unique theo cặp (`nation_id` + `area_id`)** | `CreateProvinceRequest.php:21-26` |
| Phường/xã | **`name` unique theo `province_id`**; `code` bắt buộc nhưng **KHÔNG unique** | `CreateWardRequest.php:21-25` |
| Ngân hàng | **`code` VÀ `name`** | `CreateBankRequest.php:18-19` |
| Cấp dịch vụ bảo dưỡng | `name` | `Level/LevelRequest.php:27` |
| Ghi chú kiểm tra bảo dưỡng | **`name` (Hạng mục) VÀ `key_name` (Ký hiệu)** | `NoteMaintenance/NoteMaintenanceRequest.php:42,47` |
| Dịch vụ sửa chữa & chi phí khác | `name`, **giới hạn trong nhóm `whereNull('type')`** | `Cost/CostRequest.php:43-45` |

### Việc phải sửa ở từng task

| Task | Sửa gì |
| --- | --- |
| 4 — Tiền tệ | Thêm nhánh bắt trùng **`name`** (cả trong file lẫn trong hệ thống), `«snapshot»` thêm khoá `names`. Bổ sung test `test_ten_da_ton_tai_trong_he_thong`. |
| 13 — Quốc gia | `«snapshot»` phải `pluck('id', 'country_code')` — `pluck('id','code')` sẽ **lỗi cột không tồn tại**. Thêm bắt trùng `name`. Payload tạo vẫn dùng key `code` được vì `Nation` có alias `code` ↔ `country_code` (`Nation.php:54-64`). |
| 14 — Khu vực | Bỏ ghép `nation_id` vào khoá: `«snapshot»['names']` chỉ theo **tên viết thường**, thông báo đổi thành "Tên khu vực đã tồn tại trong hệ thống". Vẫn giữ tra cứu `nation_code` để lấy `nation_id`/`nation_name`. |
| 15 — Tỉnh/TP | Khoá trùng là **`nation_id . '|' . area_id . '|' . tên thường`** (không phải nation + tên). Thêm rule `code`: cho phép rỗng, có thì phải là **số, tối đa 10 chữ số**; `license_plate`: bắt buộc, **chỉ chữ số, 1-50 ký tự**. Sửa cả unit test cho khớp. |
| 16 — Phường/xã | **Đổi khoá chống trùng**: theo **`province_id` + tên thường**, KHÔNG theo `code`. `code` vẫn bắt buộc nhưng chỉ validate **là số, tối đa 10 chữ số** — bỏ mọi thông báo "Mã số phường/xã đã tồn tại". `«snapshot»` đổi `codes` → `names` khoá `province_id|tên thường`. |
| 17 — Ngân hàng | Thêm nhánh bắt trùng **`name`**, `«snapshot»` thêm khoá `names`. |
| 19 — Ghi chú kiểm tra bảo dưỡng | Thêm nhánh bắt trùng **`name` (Hạng mục)**, `«snapshot»` thêm khoá `names`. |
| 20 — Dịch vụ / chi phí | Truy vấn trùng phải thêm `->whereNull('type')` thay cho `->where('kind_of', Cost::KIND_OF_SERVICE)` — FormRequest scope theo `type`, không theo `kind_of`. Áp cho cả `«snapshot»` lẫn kiểm tra lại trong `«create»`. |

**Khuôn bắt trùng cho màn có HAI khoá** (áp cho Tiền tệ, Quốc gia, Ngân hàng, Ghi chú bảo dưỡng) —
mỗi khoá một `$seenInFile` riêng, đừng dùng chung một mảng:

```php
            // Khai NGOÀI vòng lặp, cạnh $seenInFile:
            // $seenNamesInFile = [];

            if ($name !== '') {
                $nameKey = mb_strtolower($name);
                if (isset($seenNamesInFile[$nameKey])) {
                    $errors[] = "Tên bị trùng với dòng {$seenNamesInFile[$nameKey]} trong file";
                } else {
                    $seenNamesInFile[$nameKey] = $index + 2;
                }
                if (isset($existingNames[$nameKey])) {
                    $errors[] = 'Tên đã tồn tại trong hệ thống';
                }
            }
```

Thay chữ "Tên" bằng nhãn đúng của màn ("Tên tiền tệ", "Tên quốc gia", "Tên ngân hàng", "Hạng mục").

---

## ĐÍNH CHÍNH Khuôn A — không phải controller nào cũng có `responseBadRequest()`

> Phát hiện khi làm Task 5 (11/09/2026). **Kiểm điều này TRƯỚC khi dán Khuôn A vào bất kỳ controller nào.**

Dự án có **3 lớp `ApiController` khác nhau**; chỉ bản ở `app/` có `responseBadRequest()`:

| Lớp cha | Có gì | Controller dùng |
| --- | --- | --- |
| `App\Http\Controllers\ApiController` | `responseJson()` **+ `responseBadRequest()`** | CurrencyController, AccountController, LevelController, NoteMaintenanceController, CostController |
| `Modules\Finance\Http\Controllers\V1\ApiController` | **chỉ** `responseJson($message, $code, $data)` | WorkController, CostDebtController, SourceCapitalController, CompanyAccountController |
| `Modules\Human\Http\Controllers\Api\V1\ApiController` | `responseJson()`, `responseErrorJson()`, `apiGetList()` — **không có** `responseBadRequest()` | NationController, AreaController, ProvinceController, WardController, BankController |

⇒ **9/13 controller** trong phạm vi feature KHÔNG có `responseBadRequest()`. Dán Khuôn A nguyên văn
vào các controller đó sẽ fatal `Call to undefined method`.

**Cách kiểm nhanh trước khi dán:**

```bash
grep -q "use App.Http.Controllers.ApiController" <duong-dan-controller> && echo "DUNG KHUON A GOC" || echo "DUNG KHUON A THICH UNG"
```

**Khuôn A thích ứng** — thay mọi lời gọi `responseBadRequest($msg)` bằng:

```php
            return $this->responseJson($msg, Response::HTTP_BAD_REQUEST);
```

Phần còn lại của Khuôn A giữ nguyên. Vẫn cần `use Illuminate\Http\Response;` (đa số đã có) và bổ
sung `use Exception;`, `use Illuminate\Support\Facades\DB;`, `use Illuminate\Support\Facades\Log;`
nếu đầu file chưa khai.

**KHÔNG** đổi lớp cha của controller sang `App\Http\Controllers\ApiController` để "cho tiện" — làm
thế là đổi hành vi của mọi method sẵn có trong controller đó, nằm ngoài phạm vi feature này.

---

## File Structure

**Tạo mới:**

| File | Trách nhiệm |
| --- | --- |
| `hrm-client/utils/mixins/CatalogImportMixin.js` | Luồng validate/import dùng chung cho mọi màn danh mục (đổi tên từ `FinanceImportMixin.js`) |
| `hrm-api/Modules/Finance/Tests/Unit/CurrencyImportValidationTest.php` | Unit test cho hàm thuần `CurrencyService::validateRows()` |
| `hrm-api/Modules/Human/Tests/Unit/ProvinceImportValidationTest.php` | Unit test cho `ProvinceService::validateRows()` — màn có tra cứu 2 cấp cha |

**Sửa:**

| File | Thay đổi |
| --- | --- |
| `hrm-client/utils/import-helper.js` | Thêm `buildImportTemplate()` + 2 helper nội bộ |
| `hrm-client/pages/finance/{accounts,type-accounts}/index.vue` | Trỏ import mixin sang tên mới |
| 13 file `hrm-client/pages/**/index.vue` | Thêm nút + modal + `importColumns` + `mapImportRow` |
| 13 file `Modules/*/Services/*Service.php` | Thêm `validateImportData()` + `validateRows()` + `import()` |
| 13 file `Modules/*/Http/Controllers/**/*Controller.php` | Thêm `validateImport()` + `import()` |
| 3 file `Modules/{Finance,Human,CustomerCare}/Routes/api.php` | Thêm 2 route/màn |
| `hrm-api/app/ExcelExport/ExportColumnRegistry.php` | Thêm 8 bộ cột xuất file |

**Xoá:** `hrm-client/utils/mixins/FinanceImportMixin.js` (sau khi đổi tên)

---

## Khuôn chuẩn (Appendix) — dùng lại ở mọi task Phase 2-4

Bốn khuôn dưới đây là **code thật**, chỉ thay các token `«...»`. Mỗi task Phase 2-4 cho sẵn bảng giá trị đầy đủ của mọi token, không có chỗ nào phải tự nghĩ.

### Khuôn A — 2 method của Controller

Dán vào cuối class controller, trước dấu `}` cuối cùng.

```php
    /**
     * Bước validate của luồng import Excel (V2BaseImportModal).
     */
    public function validateImport(Request $request)
    {
        $items = $request->input('«payloadKey»');

        if (!is_array($items) || empty($items)) {
            return $this->responseBadRequest('Dữ liệu validate rỗng');
        }

        try {
            $result = $this->«serviceProp»->validateImportData($items);

            $message = ($result['invalidCount'] ?? 0) > 0
                ? "Validate xong: {$result['validCount']} hợp lệ, {$result['invalidCount']} không hợp lệ"
                : 'Validate thành công';

            return $this->responseJson($message, Response::HTTP_OK, $result);
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseBadRequest($e->getMessage());
        }
    }

    /**
     * Ghi dữ liệu import (chỉ nhận dòng hợp lệ, vẫn validate lại phía server).
     */
    public function import(Request $request)
    {
        $items = $request->input('«payloadKey»');

        if (!is_array($items) || empty($items)) {
            return $this->responseBadRequest('Dữ liệu import rỗng');
        }

        try {
            $validation = $this->«serviceProp»->validateImportData($items);
            $validItems = [];
            foreach ($validation['rows'] as $row) {
                if ($row['isValid']) {
                    $validItems[] = $items[$row['index']];
                }
            }

            if (empty($validItems)) {
                return $this->responseBadRequest('Không có dòng nào hợp lệ để import');
            }

            $result = DB::transaction(function () use ($validItems) {
                return $this->«serviceProp»->import($validItems);
            });

            $code = $result['failed'] > 0 ? Response::HTTP_MULTI_STATUS : Response::HTTP_OK;

            return $this->responseJson(
                "Import xong: {$result['success']} thành công, {$result['failed']} thất bại",
                $code,
                $result
            );
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseBadRequest($e->getMessage());
        }
    }
```

Kiểm `use` đầu file, thiếu thì thêm: `Illuminate\Http\Request`, `Illuminate\Http\Response`, `Illuminate\Support\Facades\DB`, `Illuminate\Support\Facades\Log`, `Exception`.

### Khuôn B — 3 method của Service

`validateImportData()` nạp dữ liệu đối chiếu từ DB rồi gọi `validateRows()` **thuần** (không DB, không auth, không `now()`) — đây là hàm được unit test.

```php
    /**
     * Bước validate: nạp dữ liệu đối chiếu từ DB rồi giao cho hàm thuần `validateRows()`.
     *
     * @param  array $items
     * @return array{rows: array, total: int, validCount: int, invalidCount: int}
     */
    public function validateImportData(array $items): array
    {
        return $this->validateRows($items, $this->importSnapshot());
    }

    /**
     * Ảnh chụp dữ liệu đang có trong DB, dùng để bắt trùng và tra cứu cha.
     *
     * @return array
     */
    private function importSnapshot(): array
    {
        return «snapshot»;
    }

    /**
     * HÀM THUẦN — không đụng DB, không auth, không now(). Đây là hàm được unit test.
     *
     * @param  array $items    mảng dòng đã map sang key BE
     * @param  array $snapshot kết quả `importSnapshot()`
     * @return array{rows: array, total: int, validCount: int, invalidCount: int}
     */
    public function validateRows(array $items, array $snapshot): array
    {
        $seenInFile = [];
        $rows = [];
        $validCount = 0;
        $invalidCount = 0;

        foreach ($items as $index => $item) {
            $errors = [];

            «rules»

            $isValid = count($errors) === 0;
            $isValid ? $validCount++ : $invalidCount++;

            $rows[] = [
                'index' => $index,
                'row' => $index + 2,
                'isValid' => $isValid,
                'errors' => $errors,
            ];
        }

        return [
            'rows' => $rows,
            'total' => count($items),
            'validCount' => $validCount,
            'invalidCount' => $invalidCount,
        ];
    }

    /**
     * Ghi dữ liệu import. Mỗi dòng bọc try/catch riêng để 1 dòng lỗi không chặn các dòng còn lại.
     *
     * @param  array $items
     * @return array{total: int, success: int, failed: int, errors: array}
     */
    public function import(array $items): array
    {
        $employeeId = $this->currentEmployeeId();
        $snapshot = $this->importSnapshot();

        $total = count($items);
        $success = 0;
        $failed = 0;
        $errors = [];

        foreach ($items as $index => $item) {
            try {
                «create»

                $success++;
            } catch (\Exception $e) {
                $failed++;
                $errors[] = [
                    'index' => $index,
                    'name' => $item['name'] ?? 'N/A',
                    'error' => $e->getMessage(),
                ];
            }
        }

        return compact('total', 'success', 'failed', 'errors');
    }
```

Service nào chưa có `currentEmployeeId()` thì copy nguyên văn từ `Modules/Finance/Services/TypeAccountService.php`.

### Khuôn C — parseStatus (chỉ dán vào service của màn CÓ cột Trạng thái)

```php
    /**
     * Đổi nhãn trạng thái trong file Excel sang mã. Trả null nếu không nhận diện được.
     */
    private function parseStatus(string $text): ?int
    {
        $normalized = mb_strtolower(trim($text));

        if ($normalized === '' || in_array($normalized, ['hoạt động', 'hoat dong', 'active', '1'], true)) {
            return «STATUS_ACTIVE»;
        }

        if (in_array($normalized, ['khóa', 'khoa', 'inactive', 'lock', '2', '0'], true)) {
            return «STATUS_INACTIVE»;
        }

        return null;
    }
```

### Khuôn D — đấu nối FE trong `pages/«màn»/index.vue`

**D1 — nút**, đặt ngay sau nút "Xuất Excel" trong `<template #actions-bottom>`:

```vue
                    <!-- Import ghi dữ liệu vào hệ thống -> tách tông CAM (button-convention 2b) -->
                    <V2BaseButton
                        «gate»
                        secondary
                        status="warning"
                        size="sm"
                        class="btn-compact"
                        @click="openImportModal('«modalId»')"
                    >
                        <template #prefix>
                            <i class="ri-upload-line" style="font-size: 13px"></i>
                        </template>
                        Import Excel
                    </V2BaseButton>
```

**D2 — modal**, đặt cạnh các modal khác cuối `<template>`:

```vue
        <!-- Import Excel -->
        <V2BaseImportModal
            ref="importModal"
            modal-id="«modalId»"
            title="Import «nhãn»"
            subtitle="Import từ Excel • Validate xong dòng hợp lệ sẽ bị khoá"
            :columns="importColumns"
            :required-fields="importRequiredFields"
            :existing-data="[]"
            :skip-rows="1"
            @validate-data="handleValidateImportData"
            @import-data="handleImportData"
            @download-template="handleDownloadImportTemplate"
        />
```

`:skip-rows="1"` vì file mẫu có dòng gợi ý ở dòng 2. `:existing-data="[]"` — việc bắt trùng do BE lo, không dùng bộ bắt trùng client-side của modal.

**D3 — script:**

```js
import V2BaseImportModal from '@/components/V2BaseImportModal.vue'
import CatalogImportMixin from '@/utils/mixins/CatalogImportMixin.js'
import { buildImportTemplate } from '@/utils/import-helper'
```

Thêm `CatalogImportMixin` vào mảng `mixins`, thêm `V2BaseImportModal` vào `components`.

**D4 — data:**

```js
            // Cấu hình cho CatalogImportMixin
            importApiPrefix: '«apiPrefix»',
            importPayloadKey: '«payloadKey»',
            importItemLabel: '«nhãn»',
```

**D5 — computed:**

```js
        importColumns() {
            return «columns»
        },
        importRequiredFields() {
            return «required»
        },
```

**D6 — methods:**

```js
        /** Đổi 1 dòng Excel sang payload BE — CatalogImportMixin gọi hàm này. */
        mapImportRow(row) {
            return «mapRow»
        },
        /** File mẫu sinh từ chính `importColumns` nên header không bao giờ lệch với trình đọc. */
        handleDownloadImportTemplate() {
            try {
                buildImportTemplate(this.importColumns, {
                    requiredFields: this.importRequiredFields,
                    fileName: '«fileName»',
                    sheetName: '«sheetName»',
                })
            } catch (error) {
                console.error('Error building import template:', error)
                this.$toasted?.global?.error?.({ message: 'Lỗi khi tạo file mẫu' })
            }
        },
```

Màn nào chưa có `loadData()` (mixin gọi sau khi import xong) thì dùng đúng tên hàm nạp danh sách của màn đó bằng cách khai thêm `loadData() { return this.«tênHàmThật»() }`.

---

## Phase 1 — Khung dùng chung

### Task 1: Tạo nhánh làm việc

**Files:** không sửa file nào

- [x] **Step 1: Tạo nhánh ở cả hai repo**

```bash
cd D:/CompanyProject/hrm/hrm-api && git checkout gop_db && git checkout -b feat/catalog-import-export
cd D:/CompanyProject/hrm/hrm-client && git checkout gop_db && git checkout -b feat/catalog-import-export
```

- [x] **Step 2: Xác nhận đang đứng đúng nhánh**

```bash
cd D:/CompanyProject/hrm && for d in hrm-api hrm-client; do echo -n "$d: "; git -C $d branch --show-current; done
```

Expected: cả hai in `feat/catalog-import-export`.

---

### Task 2: `buildImportTemplate()` trong `import-helper.js`

**Files:**
- Modify: `hrm-client/utils/import-helper.js` (thêm vào cuối file)

**Interfaces:**
- Consumes: global `XLSX` (SheetJS 0.20.3, nạp qua CDN ở `nuxt.config.js:96`)
- Produces: `buildImportTemplate(columns, options)` — `columns` là mảng `importColumns` của màn; `options = { requiredFields: string[], fileName: string, sheetName?: string, includeHintRow?: boolean }`; không trả giá trị, gọi xong trình duyệt tải file về.

- [x] **Step 1: Viết hàm**

Thêm vào cuối `hrm-client/utils/import-helper.js`:

```javascript
/**
 * Dựng file .xlsx mẫu TỪ CHÍNH `importColumns` mà màn đang dùng để đọc file import.
 *
 * Vì sao sinh động thay vì đặt file tĩnh trong `static/`: header của file mẫu và bộ nhận diện
 * header của `parseExcelFile()` khi đó là MỘT nguồn duy nhất — thêm/bớt cột là file mẫu tự đúng,
 * không bao giờ lệch âm thầm như 17 file `Mau_import_*.xlsx` đang có.
 *
 * File sinh ra gồm 2 dòng:
 *   · dòng 1 — header, cột bắt buộc gắn hậu tố " *"
 *   · dòng 2 — gợi ý giá trị (`placeholder`, hoặc danh sách lựa chọn nếu `type: 'select'`)
 * Màn dùng file mẫu này phải khai `:skip-rows="1"` để trình đọc bỏ qua dòng gợi ý.
 *
 * @param {Array}  columns  mảng `importColumns` của màn
 * @param {Object} options  { requiredFields, fileName, sheetName, includeHintRow }
 */
export function buildImportTemplate(columns, options = {}) {
    if (typeof XLSX === 'undefined') {
        throw new Error('Thiếu thư viện XLSX. (XLSX is not defined)')
    }

    const cols = Array.isArray(columns) ? columns : []
    if (!cols.length) {
        throw new Error('Không có cột nào để dựng file mẫu.')
    }

    const required = new Set(options.requiredFields || [])

    const header = cols.map((col) => {
        const label = stripHtmlTag(col.label || col.key || '')
        return required.has(col.key) && !label.endsWith('*') ? `${label} *` : label
    })

    const hint = cols.map((col) => {
        if (col.type === 'select' && Array.isArray(col.options)) {
            return col.options.map((opt) => opt.name ?? opt.id ?? '').join(' / ')
        }

        return col.placeholder || ''
    })

    const aoa = options.includeHintRow === false ? [header] : [header, hint]
    const sheet = XLSX.utils.aoa_to_sheet(aoa)
    sheet['!cols'] = cols.map((col) => ({ wch: pixelToChar(col.width) }))

    const book = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(book, sheet, options.sheetName || 'Mau import')
    XLSX.writeFile(book, options.fileName || 'Mau_import.xlsx')
}

/** Nhãn cột có thể chứa thẻ HTML (dấu * đỏ) — file Excel chỉ nhận chữ thuần. */
function stripHtmlTag(value) {
    return String(value)
        .replace(/<[^>]*>/g, '')
        .replace(/\s+/g, ' ')
        .trim()
}

/** `width` của cột preview là chuỗi px ('180px'); Excel đo theo số ký tự. */
function pixelToChar(width) {
    const px = parseInt(String(width || ''), 10)
    if (!px || Number.isNaN(px)) return 20

    return Math.min(60, Math.max(10, Math.round(px / 7)))
}
```

- [x] **Step 2: Kiểm cú pháp**

```bash
cd D:/CompanyProject/hrm/hrm-client && npx eslint utils/import-helper.js
```

Expected: không có lỗi. Nếu dự án chưa cấu hình eslint thì bỏ qua bước này và chuyển sang Step 3.

- [x] **Step 3: Xác nhận hàm export ra đúng tên**

```bash
cd D:/CompanyProject/hrm/hrm-client && grep -n "^export function" utils/import-helper.js
```

Expected: có dòng `export function buildImportTemplate(columns, options = {}) {`.

---

### Task 3: Đổi `FinanceImportMixin` thành `CatalogImportMixin` + hồi quy 2 màn Tài chính

**Files:**
- Create: `hrm-client/utils/mixins/CatalogImportMixin.js` (nội dung y hệt file cũ, chỉ sửa docblock)
- Delete: `hrm-client/utils/mixins/FinanceImportMixin.js`
- Modify: `hrm-client/pages/finance/accounts/index.vue`, `hrm-client/pages/finance/type-accounts/index.vue`

**Interfaces:**
- Produces: mixin mặc định export object có `openImportModal(modalId)`, `handleValidateImportData(dataRows)`, `handleImportData(dataRows)`. Màn dùng phải khai `importApiPrefix`, `importPayloadKey`, `importItemLabel`, method `mapImportRow(row)`, có `$refs.importModal` và `loadData()`.

- [x] **Step 1: Đổi tên file, giữ nguyên từng dòng logic**

```bash
cd D:/CompanyProject/hrm/hrm-client && git mv utils/mixins/FinanceImportMixin.js utils/mixins/CatalogImportMixin.js
```

- [x] **Step 2: Sửa docblock đầu file cho đúng phạm vi mới**

Thay 2 dòng đầu docblock trong `utils/mixins/CatalogImportMixin.js`:

```javascript
/**
 * Luồng import Excel dùng chung cho MỌI màn danh mục (Tài chính, Nhân sự, CSKH, Giao việc).
 *
```

(dòng cũ là `Luồng import Excel dùng chung cho phân hệ Tài chính (danh mục tài khoản + loại tài khoản).`)

Phần `Màn dùng mixin phải khai:` bên dưới giữ nguyên không đổi.

- [x] **Step 3: Trỏ 2 màn Tài chính sang tên mới**

Trong cả `pages/finance/accounts/index.vue` và `pages/finance/type-accounts/index.vue`:

- dòng `import FinanceImportMixin from '@/utils/mixins/FinanceImportMixin.js'` → `import CatalogImportMixin from '@/utils/mixins/CatalogImportMixin.js'`
- trong mảng `mixins: [...]`, `FinanceImportMixin` → `CatalogImportMixin`
- comment `// Cấu hình cho FinanceImportMixin` → `// Cấu hình cho CatalogImportMixin`
- comment `/** Đổi 1 dòng Excel sang payload BE — FinanceImportMixin gọi hàm này. */` → `… — CatalogImportMixin gọi hàm này. */`

- [x] **Step 4: Xác nhận không còn tham chiếu tên cũ**

```bash
cd D:/CompanyProject/hrm/hrm-client && grep -rn "FinanceImportMixin" pages/ utils/ components/
```

Expected: không in ra gì.

- [x] **Step 5: Chạy dev server**

```bash
cd D:/CompanyProject/hrm/hrm-client && npm run dev
```

Expected: build xong không lỗi. Để chạy nền, sang bước sau.

- [x] **Step 6: Hồi quy Import ở 2 màn Tài chính bằng Playwright**

Với **từng** màn `/finance/type-accounts` và `/finance/accounts`:

1. Mở màn, bấm **Import Excel** → modal mở đúng
2. Bấm **(File mẫu)** → tải được file `Mau_import_loai_tai_khoan.xlsx` / `Mau_import_tai_khoan.xlsx` (2 màn này **vẫn dùng file tĩnh**, không đổi sang `buildImportTemplate`)
3. Nạp file mẫu đã điền 1 dòng mới → xem trước đúng cột → Validate → hiện "hợp lệ" → Import → danh sách có bản ghi mới
4. Chụp ảnh màn hình bước 3 và bước kết quả

**Bắt buộc đóng browser** (`browser_close`) sau khi xong.

- [x] **Step 7: Đối chiếu ràng buộc `unique` thật của 13 bảng**

Bật MySQL local rồi chạy:

```bash
cd D:/CompanyProject/hrm/hrm-api && php artisan tinker --execute="
foreach (['currencies','company_accounts','works','cost_debts','source_capitals','nations','areas','provinces','wards','banks','levels','note_maintenances','costs'] as \$t) {
    echo '### '.\$t.PHP_EOL;
    foreach (DB::select('SHOW INDEX FROM '.\$t.' WHERE Non_unique = 0') as \$i) {
        echo '   '.\$i->Key_name.' -> '.\$i->Column_name.PHP_EOL;
    }
    echo '   cols: '.implode(', ', Schema::getColumnListing(\$t)).PHP_EOL;
}"
```

Ghi kết quả vào mục "Quyết định đã chốt" của `design.md`. Bảng nào có `unique` khác với khoá chống trùng ghi trong spec §6 thì **theo DB**, và sửa lại spec §6 cho khớp.

---

### Checkpoint Phase 1 — ✅ XONG 11/09/2026

Đã chạy và nghiệm thu:

- Nhánh `feat/catalog-import-export` ở cả 2 repo, `HEAD == gop_db`, cây sạch.
  ⚠️ **Bẫy đã gặp:** `gop_db` đang bị worktree `.worktrees/gop-db` giữ nên `git checkout gop_db`
  THẤT BẠI, và lệnh `git checkout -b` kế tiếp tách nhầm từ nhánh đang đứng. Lần sau dùng thẳng
  `git checkout -b <tên-mới> gop_db` (một lệnh), hoặc kiểm `git rev-parse HEAD` vs `gop_db` sau khi tạo.
- `buildImportTemplate()` — kiểm bằng XLSX giả lập: header ra đúng (cột bắt buộc có hậu tố ` *`,
  thẻ HTML bị gỡ), dòng gợi ý lấy `placeholder` và liệt kê lựa chọn cho cột `select`,
  `!cols` quy đổi px → số ký tự đúng, mảng rỗng ném lỗi.
- `CatalogImportMixin.js` — đổi tên xong, 0 tham chiếu tên cũ, 2 file `.vue` parse sạch
  (`vue-template-compiler` + `@babel/core`).
- **Hồi quy thật trên máy local** (MySQL Laragon + `php artisan serve :8000` + `npm run dev :3000`):
  - `/finance/type-accounts`: mở modal → nạp file 3 dòng → Validate ra **1 hợp lệ / 2 lỗi** đúng lý do
    ("đã tồn tại trong hệ thống", "không được để trống") → Bỏ dòng lỗi → Import → DB có bản ghi
    `ZZTEST01` đủ `code/name/note/status/created_by`. Đã xoá bản ghi thử sau khi kiểm.
  - `/finance/accounts`: danh sách 316 dòng nạp bình thường, modal Import mở đúng.
  - 0 lỗi console ở cả hai màn.
- Đối chiếu ràng buộc `unique` 13 bảng — kết quả đã ghi thành mục
  "ĐÍNH CHÍNH khoá chống trùng" ở đầu file này.

**Ghi chú kỹ thuật phát hiện lúc hồi quy:** `type_accounts` / `accounts` **chỉ ghi version khi SỬA**;
`store()` không ghi version tạo → bản ghi import có 0 version là bình thường ở 2 màn này.
Đừng lấy 2 màn đó làm chuẩn cho hành vi Lịch sử thay đổi — 13 màn đích đều có
`logCatalogCreate()` trong hàm tạo nên quyết định Q10 (gọi lại method tạo sẵn có) giữ nguyên.

---

## Phase 2 — Tài chính

Phase 2 gồm 5 task Import (Task 4-8) và 4 task Export (Task 9-12). Mỗi task làm trọn một màn: BE + FE + nghiệm thu.

### Bảng tra cứu chung Phase 2-4 — method TẠO sẵn có của từng service

Hàm `import()` **phải gọi lại method tạo sẵn có** của service, KHÔNG `Model::create()` thẳng — vì
method đó đang gọi `logCatalogCreate()`, bỏ qua là Lịch sử thay đổi của bản ghi import bị thủng.

| Service | Method tạo | Nhận vào |
| --- | --- | --- |
| `Modules\Finance\Services\CurrencyService` | `store(Request $request): Currency` | `Request` |
| `Modules\Finance\Services\CompanyAccountService` | `createOrUpdate(array $attrs, ?CompanyAccount $obj = null): CompanyAccount` | `array` |
| `Modules\Finance\Services\WorkService` | `createWork(array $attrs): Work` | `array` |
| `Modules\Finance\Services\CostDebtService` | `createCostDebt(array $attrs): CostDebt` | `array` |
| `Modules\Finance\Services\SourceCapitalService` | `createSourceCapital(array $attrs): SourceCapital` | `array` |
| `Modules\Human\Services\NationService` | `createNation(array $attributes)` | `array` |
| `Modules\Human\Services\AreaService` | `createArea(array $attributes)` | `array` |
| `Modules\Human\Services\ProvinceService` | `createProvince(array $attributes)` | `array` |
| `Modules\Human\Services\WardService` | `createWards(array $attributes)` | `array` |
| `Modules\Human\Services\BankService` | `createBank(array $attributes)` | `array` |
| `Modules\CustomerCare\Services\LevelService` | `store(Request $request): Level` | `Request` |
| `Modules\CustomerCare\Services\NoteMaintenanceService` | `store(Request $request): NoteMaintenance` | `Request` |
| `Modules\CustomerCare\Services\CostService` | `store(Request $request, int $kindOf = Cost::KIND_OF_SERVICE): Cost` | `Request` |

Service nhận `Request` thì trong `import()` dựng `new Request($payload)` rồi truyền vào — đừng
truyền `stdClass` hay mảng trần, service gọi `$request->get()` sẽ fatal.

`$employeeId` lấy theo đúng cách service đó đang dùng ở method tạo: `$this->currentEmployeeId()`
với service extends `FinanceService` (Currency), `auth()->id()` với các service còn lại. Method tạo
đã tự set `created_by` nên hàm `import()` **không cần truyền** trường này.

---

### Task 4: Import — Danh mục tiền tệ `/finance/currencies`

**Files:**
- Create: `hrm-api/Modules/Finance/Tests/Unit/CurrencyImportValidationTest.php`
- Modify: `hrm-api/Modules/Finance/Services/CurrencyService.php` (thêm 4 method vào cuối class)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/CurrencyController.php` (Khuôn A)
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (nhóm `/currencies`, dòng ~112)
- Modify: `hrm-client/pages/finance/currencies/index.vue` (Khuôn D)

**Interfaces:**
- Consumes: `buildImportTemplate()` (Task 2), `CatalogImportMixin` (Task 3)
- Produces: `CurrencyService::validateRows(array $items, array $snapshot): array` — hàm thuần, `$snapshot = ['codes' => array<string mã viết HOA, int id>]`; trả `['rows' => [...], 'total' => int, 'validCount' => int, 'invalidCount' => int]`, mỗi phần tử `rows` có `index`, `row`, `isValid`, `errors`.

- [x] **Step 1: Viết test thất bại**

Tạo `hrm-api/Modules/Finance/Tests/Unit/CurrencyImportValidationTest.php`:

```php
<?php

namespace Modules\Finance\Tests\Unit;

use Modules\Finance\Services\CurrencyService;
use PHPUnit\Framework\TestCase;

/**
 * Unit test cho `CurrencyService::validateRows()` — hàm THUẦN (không DB, không auth) nên chạy
 * bằng `PHPUnit\Framework\TestCase`, KHÔNG cần boot Laravel.
 */
class CurrencyImportValidationTest extends TestCase
{
    private function service(): CurrencyService
    {
        return new CurrencyService();
    }

    /** Ảnh chụp DB giả lập: hệ thống đã có sẵn mã USD. */
    private function snapshot(): array
    {
        return ['codes' => ['USD' => 7]];
    }

    public function test_dong_hop_le_thi_khong_co_loi()
    {
        $result = $this->service()->validateRows([
            ['code' => 'EUR', 'name' => 'Euro', 'other_name' => '', 'exchange_rate' => '27000', 'status' => 'Hoạt động'],
        ], $this->snapshot());

        $this->assertSame(1, $result['validCount']);
        $this->assertSame(0, $result['invalidCount']);
        $this->assertTrue($result['rows'][0]['isValid']);
        $this->assertSame(2, $result['rows'][0]['row']);
    }

    public function test_thieu_ma_va_ten_thi_bao_khong_duoc_de_trong()
    {
        $result = $this->service()->validateRows([
            ['code' => '', 'name' => '', 'exchange_rate' => '1'],
        ], $this->snapshot());

        $this->assertFalse($result['rows'][0]['isValid']);
        $this->assertContains('Mã tiền tệ không được để trống', $result['rows'][0]['errors']);
        $this->assertContains('Tên tiền tệ không được để trống', $result['rows'][0]['errors']);
    }

    public function test_ma_da_ton_tai_trong_he_thong()
    {
        $result = $this->service()->validateRows([
            ['code' => 'usd', 'name' => 'Đô la Mỹ', 'exchange_rate' => '25000'],
        ], $this->snapshot());

        $this->assertFalse($result['rows'][0]['isValid']);
        $this->assertContains('Mã tiền tệ đã tồn tại trong hệ thống', $result['rows'][0]['errors']);
    }

    public function test_ma_trung_nhau_trong_cung_file()
    {
        $result = $this->service()->validateRows([
            ['code' => 'GBP', 'name' => 'Bảng Anh', 'exchange_rate' => '32000'],
            ['code' => 'GBP', 'name' => 'Bảng Anh 2', 'exchange_rate' => '32000'],
        ], $this->snapshot());

        $this->assertTrue($result['rows'][0]['isValid']);
        $this->assertFalse($result['rows'][1]['isValid']);
        $this->assertContains('Mã tiền tệ bị trùng với dòng 2 trong file', $result['rows'][1]['errors']);
    }

    public function test_ty_gia_sai_kieu_so()
    {
        $result = $this->service()->validateRows([
            ['code' => 'JPY', 'name' => 'Yên Nhật', 'exchange_rate' => 'abc'],
            ['code' => 'KRW', 'name' => 'Won', 'exchange_rate' => '-5'],
            ['code' => 'THB', 'name' => 'Baht', 'exchange_rate' => ''],
        ], $this->snapshot());

        $this->assertContains('Tỷ giá không hợp lệ', $result['rows'][0]['errors']);
        $this->assertContains('Tỷ giá không hợp lệ', $result['rows'][1]['errors']);
        $this->assertContains('Tỷ giá không được để trống', $result['rows'][2]['errors']);
    }

    public function test_trang_thai_khong_nhan_dien_duoc()
    {
        $result = $this->service()->validateRows([
            ['code' => 'AUD', 'name' => 'Đô la Úc', 'exchange_rate' => '17000', 'status' => 'Tạm dừng'],
        ], $this->snapshot());

        $this->assertContains('Trạng thái chỉ nhận "Hoạt động" hoặc "Khóa"', $result['rows'][0]['errors']);
    }
}
```

- [x] **Step 2: Chạy test để chắc chắn nó FAIL**

```bash
cd D:/CompanyProject/hrm/hrm-api && php vendor/bin/phpunit Modules/Finance/Tests/Unit/CurrencyImportValidationTest.php
```

Expected: FAIL — `Call to undefined method Modules\Finance\Services\CurrencyService::validateRows()`.

- [x] **Step 3: Viết 4 method trong `CurrencyService`**

Dán vào cuối class `Modules/Finance/Services/CurrencyService.php`:

```php
    /**
     * Bước validate: nạp dữ liệu đối chiếu từ DB rồi giao cho hàm thuần `validateRows()`.
     */
    public function validateImportData(array $items): array
    {
        return $this->validateRows($items, $this->importSnapshot());
    }

    /** Ảnh chụp mã tiền tệ đang có, dùng để bắt trùng. */
    private function importSnapshot(): array
    {
        return [
            'codes' => Currency::query()
                ->pluck('id', 'code')
                ->mapWithKeys(function ($id, $code) {
                    return [mb_strtoupper(trim((string) $code)) => $id];
                })
                ->toArray(),
        ];
    }

    /**
     * HÀM THUẦN — không đụng DB, không auth, không now(). Đây là hàm được unit test.
     */
    public function validateRows(array $items, array $snapshot): array
    {
        $existingCodes = $snapshot['codes'] ?? [];
        $seenInFile = [];
        $rows = [];
        $validCount = 0;
        $invalidCount = 0;

        foreach ($items as $index => $item) {
            $errors = [];

            $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));
            $name = trim((string) ($item['name'] ?? ''));
            $otherName = trim((string) ($item['other_name'] ?? ''));
            $rate = trim((string) ($item['exchange_rate'] ?? ''));
            $statusText = trim((string) ($item['status'] ?? ''));

            if ($code === '') {
                $errors[] = 'Mã tiền tệ không được để trống';
            } elseif (mb_strlen($code) > 255) {
                $errors[] = 'Mã tiền tệ tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$code])) {
                    $errors[] = "Mã tiền tệ bị trùng với dòng {$seenInFile[$code]} trong file";
                } else {
                    $seenInFile[$code] = $index + 2;
                }
                if (isset($existingCodes[$code])) {
                    $errors[] = 'Mã tiền tệ đã tồn tại trong hệ thống';
                }
            }

            if ($name === '') {
                $errors[] = 'Tên tiền tệ không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên tiền tệ tối đa 255 ký tự';
            }

            if ($otherName !== '' && mb_strlen($otherName) > 255) {
                $errors[] = 'Tên gọi khác tối đa 255 ký tự';
            }

            if ($rate === '') {
                $errors[] = 'Tỷ giá không được để trống';
            } elseif (!is_numeric(str_replace(',', '', $rate)) || (float) str_replace(',', '', $rate) <= 0) {
                $errors[] = 'Tỷ giá không hợp lệ';
            }

            if ($statusText !== '' && $this->parseStatus($statusText) === null) {
                $errors[] = 'Trạng thái chỉ nhận "Hoạt động" hoặc "Khóa"';
            }

            $isValid = count($errors) === 0;
            $isValid ? $validCount++ : $invalidCount++;

            $rows[] = [
                'index' => $index,
                'row' => $index + 2,
                'isValid' => $isValid,
                'errors' => $errors,
            ];
        }

        return [
            'rows' => $rows,
            'total' => count($items),
            'validCount' => $validCount,
            'invalidCount' => $invalidCount,
        ];
    }

    /**
     * Ghi dữ liệu import. Mỗi dòng bọc try/catch riêng để 1 dòng lỗi không chặn các dòng còn lại.
     * Gọi lại `store()` sẵn có để `logCatalogCreate()` vẫn chạy (Lịch sử thay đổi).
     */
    public function import(array $items): array
    {
        $total = count($items);
        $success = 0;
        $failed = 0;
        $errors = [];

        foreach ($items as $index => $item) {
            try {
                $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));

                if (Currency::query()->where('code', $code)->exists()) {
                    throw new \Exception('Mã tiền tệ đã tồn tại trong hệ thống');
                }

                $this->store(new Request([
                    'code' => $code,
                    'name' => trim((string) ($item['name'] ?? '')),
                    'other_name' => trim((string) ($item['other_name'] ?? '')) ?: null,
                    'exchange_rate' => (float) str_replace(',', '', (string) ($item['exchange_rate'] ?? '0')),
                    'status' => $this->parseStatus((string) ($item['status'] ?? '')) ?? Currency::STATUS_ACTIVE,
                ]));

                $success++;
            } catch (\Exception $e) {
                $failed++;
                $errors[] = [
                    'index' => $index,
                    'name' => $item['name'] ?? 'N/A',
                    'error' => $e->getMessage(),
                ];
            }
        }

        return compact('total', 'success', 'failed', 'errors');
    }
```

Thêm Khuôn C (`parseStatus`) vào cùng class với `«STATUS_ACTIVE» = Currency::STATUS_ACTIVE` và
`«STATUS_INACTIVE» = Currency::STATUS_BLOCK`. Kiểm `use Illuminate\Http\Request;` đã có ở đầu file.

⚠️ Mở `CurrencyService::store()` đọc trước khi viết `import()`: nếu `store()` đọc thêm trường nào
ngoài 5 trường trên (ví dụ `company_id`) thì bổ sung vào mảng truyền cho `new Request([...])`.

- [x] **Step 4: Chạy test để chắc chắn nó PASS**

```bash
cd D:/CompanyProject/hrm/hrm-api && php vendor/bin/phpunit Modules/Finance/Tests/Unit/CurrencyImportValidationTest.php
```

Expected: `OK (6 tests, ...)`.

- [x] **Step 5: Thêm 2 method vào Controller**

Dán Khuôn A vào `Modules/Finance/Http/Controllers/V1/CurrencyController.php` với
`«payloadKey» = currencies`, `«serviceProp» = currencyService` (kiểm lại tên property thật ở
constructor của controller, lệch thì dùng tên thật).

- [x] **Step 6: Thêm 2 route**

Trong `Modules/Finance/Routes/api.php`, nhóm `['prefix' => '/currencies']`, đặt **ngay sau** dòng
`Route::get('/export', ...)` (tức vẫn nằm TRƯỚC mọi route `/{currency}`):

```php
        Route::post('/import/validate', [CurrencyController::class, 'validateImport'])
            ->middleware('checkPermission:Quản lý danh mục tiền tệ');
        Route::post('/import', [CurrencyController::class, 'import'])
            ->middleware('checkPermission:Quản lý danh mục tiền tệ');
```

- [x] **Step 7: Xác nhận route đã đăng ký**

```bash
cd D:/CompanyProject/hrm/hrm-api && php artisan route:list --path=finance/currencies | grep import
```

Expected: 2 dòng `POST api/v1/finance/currencies/import` và `.../import/validate`.

- [x] **Step 8: Đấu nối FE**

Áp Khuôn D vào `hrm-client/pages/finance/currencies/index.vue` với bảng giá trị:

| Token | Giá trị |
| --- | --- |
| `«gate»` | `v-if="canManage"` — mở màn kiểm lại nút "Tạo mới" đang gate bằng gì thì dùng đúng cái đó |
| `«modalId»` | `import-currency-modal` |
| `«nhãn»` | `tiền tệ` |
| `«apiPrefix»` | `finance/currencies` |
| `«payloadKey»` | `currencies` |
| `«fileName»` | `Mau_import_tien_te.xlsx` |
| `«sheetName»` | `Tien te` |
| `«required»` | `['Code', 'Name', 'ExchangeRate']` |

`«columns»`:

```javascript
            return [
                {
                    key: 'Code',
                    label: 'Mã tiền tệ <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã tiền tệ', 'Ma tien te', 'Mã', 'Ma'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: USD',
                    width: '160px',
                },
                {
                    key: 'Name',
                    label: 'Tên tiền tệ <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên tiền tệ', 'Ten tien te', 'Tên', 'Ten'],
                    type: 'text',
                    placeholder: 'VD: Đô la Mỹ',
                    width: '280px',
                },
                {
                    key: 'OtherName',
                    label: 'Tên gọi khác',
                    aliases: ['Tên gọi khác', 'Ten goi khac'],
                    type: 'text',
                    placeholder: 'VD: Dollar',
                    width: '240px',
                },
                {
                    key: 'ExchangeRate',
                    label: 'Tỷ giá (VNĐ) <span style="color: #dc2626;">*</span>',
                    aliases: ['Tỷ giá (VNĐ)', 'Ty gia (VND)', 'Tỷ giá', 'Ty gia'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 25000',
                    width: '160px',
                },
                {
                    key: 'Status',
                    label: 'Trạng thái',
                    aliases: ['Trạng thái', 'Trang thai'],
                    type: 'select',
                    options: [
                        { id: 'active', name: 'Hoạt động' },
                        { id: 'inactive', name: 'Khóa' },
                    ],
                    width: '140px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                code: String(row.Code || '').trim().toUpperCase(),
                name: String(row.Name || '').trim(),
                other_name: String(row.OtherName || '').trim(),
                exchange_rate: String(row.ExchangeRate || '').trim(),
                status: String(row.Status || '').trim(),
            }
```

- [x] **Step 9: Nghiệm thu bằng Playwright, có ảnh**

Chạy đủ 6 mục nghiệm thu ở spec §10 trên màn `/finance/currencies`. Chụp ảnh ít nhất: bảng xem
trước, kết quả validate có dòng lỗi, danh sách sau khi import. **Đóng browser** khi xong.

- [x] **Step 10: Báo user để commit**

Liệt kê file đã đổi, kèm ảnh nghiệm thu. Không tự commit.

---

**✅ XONG 11/09/2026.** Unit test `CurrencyImportValidationTest` — **10 test / 25 assertion, PASS**.

Nghiệm thu thật trên local (file 6 dòng dữ liệu → **1 hợp lệ / 5 lỗi**, đúng từng dòng):

| Dòng | Dữ liệu | Kết quả |
| --- | --- | --- |
| 1 | `ZZT1` · tỷ giá `27,500` | hợp lệ — dấu phân cách nghìn được bóc đúng, DB lưu `27500` |
| 2 | `USD` | "Mã tiền tệ đã tồn tại trong hệ thống" |
| 3 | `ZZT2` / tên `EURO` | "Tên tiền tệ đã tồn tại trong hệ thống" |
| 4 | thiếu mã | "Mã tiền tệ không được để trống" |
| 5 | tỷ giá `abc` | "Tỷ giá không hợp lệ" |
| 6 | tên `tiền tệ kiểm thử 1` | "Tên tiền tệ bị trùng với dòng 2 trong file" (không phân biệt hoa/thường) |

Import dòng hợp lệ → DB có `code/name/other_name/exchange_rate/status/created_by` đúng, và
`catalog_histories` có 1 dòng `action=create` → xác nhận **quyết định Q10 (gọi lại `store()` thay vì
`Currency::create()`) là cần thiết**, nếu gọi thẳng model thì Lịch sử thay đổi sẽ trống.

Import lại đúng file đó: `ZZT1` vẫn chỉ 1 bản ghi, tổng bảng không tăng. Đã xoá dữ liệu thử.

⚠️ **2 điều ghi lại cho các task sau:**

1. `php artisan route:list` **đang chết** vì lỗi có sẵn ở `app/Helper/PermissionHelper.php:23`
   (`RequestUpdateTimeSheetController` gọi helper quyền lúc nạp route, không có user đăng nhập).
   Không liên quan feature này. **Cách xác minh route thay thế:** gọi HTTP thẳng —
   route tồn tại trả **401**, sai đường dẫn trả **404/405**:
   `curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8000/api/v1/<duong-dan>`
2. Đừng đoán dữ liệu có sẵn khi dựng file thử. Lần đầu tôi lấy tên "Đô la Mỹ" để test trùng tên
   nhưng DB không có tên đó (tên thật là `USD`, `EURO`, `VietNamDong`...) → dòng đó hợp lệ và trông
   như bug. **Luôn `SELECT` danh sách thật trước khi dựng file thử.**

### Task 5: Import — Danh mục vụ việc `/finance/works`

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/WorkService.php`, `hrm-api/Modules/Finance/Http/Controllers/V1/WorkController.php`, `hrm-api/Modules/Finance/Routes/api.php` (nhóm `works`, dòng ~140)
- Modify: `hrm-client/pages/finance/works/index.vue`

**Interfaces:**
- Produces: `WorkService::validateRows(array $items, array $snapshot): array` — `$snapshot = ['codes' => array<string mã HOA, int id>]`, trả cùng khuôn Task 4.

- [x] **Step 1: Thêm 3 method vào `WorkService`**

Dán Khuôn B với bảng giá trị:

| Token | Giá trị |
| --- | --- |
| `«snapshot»` | `['codes' => Work::query()->pluck('id', 'code')->mapWithKeys(function ($id, $code) { return [mb_strtoupper(trim((string) $code)) => $id]; })->toArray()]` |

`«rules»` — dán nguyên khối này vào thân vòng lặp của `validateRows()`:

```php
            $existingCodes = $snapshot['codes'] ?? [];

            $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));
            $name = trim((string) ($item['name'] ?? ''));
            $note = trim((string) ($item['note'] ?? ''));
            $statusText = trim((string) ($item['status'] ?? ''));

            if ($code === '') {
                $errors[] = 'Mã vụ việc không được để trống';
            } elseif (mb_strlen($code) > 255) {
                $errors[] = 'Mã vụ việc tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$code])) {
                    $errors[] = "Mã vụ việc bị trùng với dòng {$seenInFile[$code]} trong file";
                } else {
                    $seenInFile[$code] = $index + 2;
                }
                if (isset($existingCodes[$code])) {
                    $errors[] = 'Mã vụ việc đã tồn tại trong hệ thống';
                }
            }

            if ($name === '') {
                $errors[] = 'Tên vụ việc không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên vụ việc tối đa 255 ký tự';
            }

            if ($note !== '' && mb_strlen($note) > 255) {
                $errors[] = 'Ghi chú tối đa 255 ký tự';
            }

            if ($statusText !== '' && $this->parseStatus($statusText) === null) {
                $errors[] = 'Trạng thái chỉ nhận "Hoạt động" hoặc "Khóa"';
            }
```

`«create»` — thân try của `import()`:

```php
                $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));

                if (Work::query()->where('code', $code)->exists()) {
                    throw new \Exception('Mã vụ việc đã tồn tại trong hệ thống');
                }

                $this->createWork([
                    'code' => $code,
                    'name' => trim((string) ($item['name'] ?? '')),
                    'note' => trim((string) ($item['note'] ?? '')) ?: null,
                    'status' => $this->parseStatus((string) ($item['status'] ?? '')) ?? 1,
                ]);
```

Bỏ dòng `$employeeId = $this->currentEmployeeId();` trong Khuôn B — `createWork()` đã tự set
`created_by` bằng `auth()->id()`, và `WorkService` KHÔNG extends `FinanceService` nên không có
method đó, để lại là fatal.

Thêm Khuôn C với `«STATUS_ACTIVE» = 1`, `«STATUS_INACTIVE» = 2` (bảng `works` không khai hằng
trạng thái; modal đang dùng chuỗi `'1'` / `'2'`).

- [x] **Step 2: Chạy nhanh kiểm cú pháp PHP**

```bash
cd D:/CompanyProject/hrm/hrm-api && php -l Modules/Finance/Services/WorkService.php
```

Expected: `No syntax errors detected`.

- [x] **Step 3: Thêm 2 method vào Controller**

Khuôn A với `«payloadKey» = works`, `«serviceProp» = workService`.

- [x] **Step 4: Thêm 2 route**

Trong nhóm `['prefix' => 'works']`, đặt **ngay sau** `Route::post('/', ...)` và **trước**
`Route::put('/{id}', ...)`:

```php
        Route::post('/import/validate', [WorkController::class, 'validateImport'])
            ->middleware('checkPermission:Quản lý danh mục vụ việc');
        Route::post('/import', [WorkController::class, 'import'])
            ->middleware('checkPermission:Quản lý danh mục vụ việc');
```

- [x] **Step 5: Xác nhận route**

```bash
cd D:/CompanyProject/hrm/hrm-api && php artisan route:list --path=finance/works | grep import
```

Expected: 2 dòng POST.

- [x] **Step 6: Đấu nối FE**

Khuôn D vào `hrm-client/pages/finance/works/index.vue`:

| Token | Giá trị |
| --- | --- |
| `«gate»` | `v-if="canManage"` (màn này đã có `canManage`, xem `index.vue:164`) |
| `«modalId»` | `import-work-modal` |
| `«nhãn»` | `vụ việc` |
| `«apiPrefix»` | `finance/works` |
| `«payloadKey»` | `works` |
| `«fileName»` | `Mau_import_vu_viec.xlsx` |
| `«sheetName»` | `Vu viec` |
| `«required»` | `['Code', 'Name']` |

`«columns»`:

```javascript
            return [
                {
                    key: 'Code',
                    label: 'Mã vụ việc <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã vụ việc', 'Ma vu viec', 'Mã', 'Ma'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: VV001',
                    width: '180px',
                },
                {
                    key: 'Name',
                    label: 'Tên vụ việc <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên vụ việc', 'Ten vu viec', 'Tên', 'Ten'],
                    type: 'text',
                    placeholder: 'VD: Dự án nhà máy A',
                    width: '320px',
                },
                {
                    key: 'Note',
                    label: 'Ghi chú',
                    aliases: ['Ghi chú', 'Ghi chu'],
                    type: 'text',
                    width: '280px',
                },
                {
                    key: 'Status',
                    label: 'Trạng thái',
                    aliases: ['Trạng thái', 'Trang thai'],
                    type: 'select',
                    options: [
                        { id: 'active', name: 'Hoạt động' },
                        { id: 'inactive', name: 'Khóa' },
                    ],
                    width: '140px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                code: String(row.Code || '').trim().toUpperCase(),
                name: String(row.Name || '').trim(),
                note: String(row.Note || '').trim(),
                status: String(row.Status || '').trim(),
            }
```

Màn này nạp danh sách bằng hàm riêng — kiểm tên hàm thật (`index.vue:264` đang gọi
`finance/works`) rồi khai thêm `loadData() { return this.«tênHàmThật»() }` nếu chưa có
method tên `loadData`.

- [x] **Step 7: Nghiệm thu Playwright + ảnh, đóng browser**

Đủ 6 mục spec §10 trên `/finance/works`.

- [x] **Step 8: Báo user để commit**

---

**✅ XONG 11/09/2026.** Nghiệm thu thật (file 5 dòng → **1 hợp lệ / 4 lỗi**, đúng từng dòng):

| Dòng | Dữ liệu | Kết quả |
| --- | --- | --- |
| 1 | `ZZVV1` | hợp lệ |
| 2 | `TVC` (mã có thật) | "Mã vụ việc đã tồn tại trong hệ thống" |
| 3 | thiếu mã | "Mã vụ việc không được để trống" |
| 4 | trạng thái `Tạm dừng` | "Trạng thái chỉ nhận \"Hoạt động\" hoặc \"Khóa\"" |
| 5 | `zzvv1` | "Mã vụ việc bị trùng với dòng 2 trong file" (viết thường vẫn bắt được) |

Import dòng hợp lệ → DB đúng `code/name/note/status/created_by`, `catalog_histories` có
1 dòng `action=create`. Đã xoá dữ liệu thử.

⚠️ **Lệch khuôn đã gặp và đã xử lý:** `WorkController` kế thừa `Modules\Finance\...\V1\ApiController`
(bản rút gọn) nên **không có `responseBadRequest()`** — đã dùng Khuôn A thích ứng
(`responseJson($msg, Response::HTTP_BAD_REQUEST)`). Xem mục "ĐÍNH CHÍNH Khuôn A" đầu file:
cùng tình trạng này còn **CostDebt, SourceCapital, CompanyAccount và cả 5 controller Nhân sự**.

Ghi chú: trang này thụt lề **2 space** (khác màn Tiền tệ 4 space) và **chưa có Export** — nút
"Xuất Excel" sẽ được thêm ở Task 9.

### Task 6: Import — Danh mục mã phí `/finance/cost-debts`

Giống hệt Task 5 về cấu trúc, chỉ đổi tên. **Files:** `CostDebtService.php`, `CostDebtController.php`,
`Modules/Finance/Routes/api.php` (nhóm `cost-debts`, dòng ~149), `hrm-client/pages/finance/cost-debts/index.vue`.

**Interfaces:** Produces `CostDebtService::validateRows(array $items, array $snapshot): array`, `$snapshot = ['codes' => ...]`.

- [x] **Step 1: Thêm 3 method vào `CostDebtService`**

Dán Khuôn B. `«snapshot»`:

```php
        return [
            'codes' => CostDebt::query()
                ->pluck('id', 'code')
                ->mapWithKeys(function ($id, $code) {
                    return [mb_strtoupper(trim((string) $code)) => $id];
                })
                ->toArray(),
        ];
```

`«rules»` — copy nguyên khối `«rules»` của Task 5, thay mọi chữ **"Mã vụ việc"** → **"Mã phí"** và
**"Tên vụ việc"** → **"Tên mã phí"**.

`«create»`:

```php
                $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));

                if (CostDebt::query()->where('code', $code)->exists()) {
                    throw new \Exception('Mã phí đã tồn tại trong hệ thống');
                }

                $this->createCostDebt([
                    'code' => $code,
                    'name' => trim((string) ($item['name'] ?? '')),
                    'note' => trim((string) ($item['note'] ?? '')) ?: null,
                    'status' => $this->parseStatus((string) ($item['status'] ?? '')) ?? 1,
                ]);
```

Bỏ dòng `$employeeId = ...` như Task 5. Thêm Khuôn C với `1` / `2`.

- [x] **Step 2: `php -l Modules/Finance/Services/CostDebtService.php`**

- [x] **Step 3: Khuôn A vào Controller** — `«payloadKey» = cost_debts`, `«serviceProp» = costDebtService`

- [x] **Step 4: Thêm 2 route** trong nhóm `['prefix' => 'cost-debts']`, sau `Route::post('/', ...)`, trước `Route::put('/{id}', ...)`:

```php
        Route::post('/import/validate', [CostDebtController::class, 'validateImport'])
            ->middleware('checkPermission:Quản lý danh mục mã phí');
        Route::post('/import', [CostDebtController::class, 'import'])
            ->middleware('checkPermission:Quản lý danh mục mã phí');
```

- [x] **Step 5: `php artisan route:list --path=finance/cost-debts | grep import`**

- [x] **Step 6: Khuôn D vào `hrm-client/pages/finance/cost-debts/index.vue`**

| Token | Giá trị |
| --- | --- |
| `«gate»` | `v-if="canManage"` |
| `«modalId»` | `import-cost-debt-modal` |
| `«nhãn»` | `mã phí` |
| `«apiPrefix»` | `finance/cost-debts` |
| `«payloadKey»` | `cost_debts` |
| `«fileName»` | `Mau_import_ma_phi.xlsx` |
| `«sheetName»` | `Ma phi` |
| `«required»` | `['Code', 'Name']` |

`«columns»` — copy nguyên khối `«columns»` Task 5, đổi: nhãn `Mã vụ việc` → `Mã phí`, aliases
`['Mã phí', 'Ma phi', 'Mã', 'Ma']`, placeholder `VD: MP001`; nhãn `Tên vụ việc` → `Tên mã phí`,
aliases `['Tên mã phí', 'Ten ma phi', 'Tên', 'Ten']`, placeholder `VD: Chi phí vận chuyển`.

`«mapRow»` — y hệt Task 5.

- [x] **Step 7: Nghiệm thu Playwright + ảnh, đóng browser**

- [x] **Step 8: Báo user để commit**

---

**✅ XONG 11/09/2026.** Nghiệm thu thật: file 3 dòng → **1 hợp lệ / 2 lỗi** ("Mã phí đã tồn tại trong hệ thống" cho mã `HHKDTM` có thật, "Tên mã phí không được để trống"). Import dòng hợp lệ → DB đúng `code/name/note/status/created_by/updated_by` (service này gán luôn `updated_by` lúc tạo), `catalog_histories` có `action=create`. Đã xoá dữ liệu thử.

Dùng Khuôn A **thích ứng** (`CostDebtController` không có `responseBadRequest`).

### Task 7: Import — Danh mục nguồn vốn `/finance/source-capitals`

Màn đơn giản nhất: file mẫu chỉ 1 cột, chống trùng theo **tên** (bảng không có cột `code`).

**Files:** `SourceCapitalService.php`, `SourceCapitalController.php`, `Modules/Finance/Routes/api.php`
(nhóm `source-capitals`, dòng ~158), `hrm-client/pages/finance/source-capitals/index.vue`.

**Interfaces:** Produces `SourceCapitalService::validateRows(array $items, array $snapshot): array`, `$snapshot = ['names' => array<string tên viết thường, int id>]`.

- [x] **Step 1: Thêm 3 method vào `SourceCapitalService`**

Khuôn B. `«snapshot»`:

```php
        return [
            'names' => SourceCapital::query()
                ->pluck('id', 'name')
                ->mapWithKeys(function ($id, $name) {
                    return [mb_strtolower(trim((string) $name)) => $id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $existingNames = $snapshot['names'] ?? [];

            $name = trim((string) ($item['name'] ?? ''));
            $key = mb_strtolower($name);

            if ($name === '') {
                $errors[] = 'Tên nguồn vốn không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên nguồn vốn tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$key])) {
                    $errors[] = "Tên nguồn vốn bị trùng với dòng {$seenInFile[$key]} trong file";
                } else {
                    $seenInFile[$key] = $index + 2;
                }
                if (isset($existingNames[$key])) {
                    $errors[] = 'Tên nguồn vốn đã tồn tại trong hệ thống';
                }
            }
```

`«create»`:

```php
                $name = trim((string) ($item['name'] ?? ''));

                $trung = SourceCapital::query()
                    ->whereRaw('LOWER(TRIM(name)) = ?', [mb_strtolower($name)])
                    ->exists();
                if ($trung) {
                    throw new \Exception('Tên nguồn vốn đã tồn tại trong hệ thống');
                }

                $this->createSourceCapital(['name' => $name]);
```

Bỏ dòng `$employeeId = ...`. **Không** thêm Khuôn C — file mẫu màn này không có cột Trạng thái
(`createSourceCapital()` luôn đặt `SourceCapital::STATUS_ACTIVE`).

- [x] **Step 2: `php -l Modules/Finance/Services/SourceCapitalService.php`**

- [x] **Step 3: Khuôn A vào Controller** — `«payloadKey» = source_capitals`, `«serviceProp» = sourceCapitalService`

- [x] **Step 4: Thêm 2 route** trong nhóm `['prefix' => 'source-capitals']`, sau `Route::post('/', ...)`, trước `Route::put('/{id}', ...)`:

```php
        Route::post('/import/validate', [SourceCapitalController::class, 'validateImport'])
            ->middleware('checkPermission:Quản lý danh mục nguồn vốn');
        Route::post('/import', [SourceCapitalController::class, 'import'])
            ->middleware('checkPermission:Quản lý danh mục nguồn vốn');
```

- [x] **Step 5: `php artisan route:list --path=finance/source-capitals | grep import`**

- [x] **Step 6: Khuôn D vào `hrm-client/pages/finance/source-capitals/index.vue`**

| Token | Giá trị |
| --- | --- |
| `«gate»` | `v-if="canManage"` |
| `«modalId»` | `import-source-capital-modal` |
| `«nhãn»` | `nguồn vốn` |
| `«apiPrefix»` | `finance/source-capitals` |
| `«payloadKey»` | `source_capitals` |
| `«fileName»` | `Mau_import_nguon_von.xlsx` |
| `«sheetName»` | `Nguon von` |
| `«required»` | `['Name']` |

`«columns»`:

```javascript
            return [
                {
                    key: 'Name',
                    label: 'Tên nguồn vốn <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên nguồn vốn', 'Ten nguon von', 'Tên', 'Ten'],
                    type: 'text',
                    placeholder: 'VD: Vốn vay ngân hàng',
                    width: '360px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                name: String(row.Name || '').trim(),
            }
```

- [x] **Step 7: Nghiệm thu Playwright + ảnh, đóng browser**

- [x] **Step 8: Báo user để commit**

---

**✅ XONG 11/09/2026.** Nghiệm thu thật: 3 dòng → **1 hợp lệ / 2 lỗi**
("Tên nguồn vốn đã tồn tại trong hệ thống" cho tên `Test vốn` có thật; "Tên nguồn vốn bị trùng với
dòng 2 trong file" — không phân biệt hoa/thường). Import → DB đúng `name/status/created_by`,
`catalog_histories` có `action=create`. Đã xoá dữ liệu thử.

⚠️ **Lỗi đã gặp và đã sửa — nhớ khi làm 9 màn còn lại:** lần chạy đầu Validate trả **HTTP 500**,
log Laravel ghi `Class 'Modules\Finance\Http\Controllers\V1\Response' not found`. Nguyên nhân:
`SourceCapitalController` **không sẵn có `use Illuminate\Http\Response;`**, mà script chèn `use` tự
động của tôi lại neo vào chính dòng đó nên cả chuỗi `Response`/`DB`/`Log` không được thêm.

**Việc bắt buộc sau khi dán Khuôn A vào mỗi controller** — kiểm bằng chuỗi cố định, đừng dùng regex
có dấu `\` (dễ sai escape trong shell và cho kết quả "thiếu" giả):

```bash
for u in 'use Illuminate\Http\Request;' 'use Illuminate\Http\Response;' \
         'use Illuminate\Support\Facades\DB;' 'use Illuminate\Support\Facades\Log;' 'use Exception;'; do
    grep -qF "$u" <duong-dan-controller> || echo "THIEU: $u"
done
```

`php -l` **KHÔNG bắt được lỗi này** (class thiếu chỉ nổ lúc chạy) — phải gọi thật endpoint hoặc đọc
`storage/logs/laravel.log` sau lần validate đầu tiên.

Ghi chú: màn này chỉ có 1 cột nên dòng để trống bị `parseExcelFile()` loại ngay từ bước đọc
(dòng trống hoàn toàn) — vì vậy "Tên nguồn vốn không được để trống" không có cơ hội xuất hiện.

### Task 8: Import — Danh mục tài khoản ngân hàng `/finance/account-banks`

Màn phức tạp nhất Phase 2: **3 tra cứu cha theo mã** (ngân hàng, chi nhánh, tiền tệ).

**Files:** `CompanyAccountService.php`, `CompanyAccountController.php`, `Modules/Finance/Routes/api.php`
(nhóm `/account-banks`, dòng ~168), `hrm-client/pages/finance/account-banks/index.vue`.

**Interfaces:** Produces `CompanyAccountService::validateRows(array $items, array $snapshot): array` với
`$snapshot = ['accountNumbers' => array<string, int>, 'banks' => array<string mã HOA, int id>, 'branches' => array<string "bankId|tên thường", int id>, 'currencies' => array<string mã HOA, int id>]`.

- [x] **Step 1: Đọc `CompanyAccountService::createOrUpdate()` trước khi viết**

```bash
cd D:/CompanyProject/hrm/hrm-api && sed -n '155,215p' Modules/Finance/Services/CompanyAccountService.php
```

Ghi lại **chính xác** danh sách key mà nó đọc từ `$attrs` — `import()` phải truyền đủ đúng từng ấy key
(ít nhất `bank_id`, `bank_branch_id`, `bank_name`, `bank_branch`, `account_name`, `account_number`,
`currency_id`, `status`, và `company_id` nếu có).

- [x] **Step 2: Thêm 3 method vào `CompanyAccountService`**

Khuôn B. `«snapshot»`:

```php
        return [
            'accountNumbers' => CompanyAccount::query()
                ->pluck('id', 'account_number')
                ->mapWithKeys(function ($id, $number) {
                    return [trim((string) $number) => $id];
                })
                ->toArray(),
            'banks' => \Modules\Human\Entities\Bank::query()
                ->get(['id', 'code', 'name'])
                ->mapWithKeys(function ($bank) {
                    return [mb_strtoupper(trim((string) $bank->code)) => ['id' => $bank->id, 'name' => $bank->name]];
                })
                ->toArray(),
            'branches' => \DB::table('bank_branches')
                ->get(['id', 'bank_id', 'name'])
                ->mapWithKeys(function ($row) {
                    return [$row->bank_id . '|' . mb_strtolower(trim((string) $row->name)) => $row->id];
                })
                ->toArray(),
            'currencies' => \Modules\Finance\Entities\Currency\Currency::query()
                ->pluck('id', 'code')
                ->mapWithKeys(function ($id, $code) {
                    return [mb_strtoupper(trim((string) $code)) => $id];
                })
                ->toArray(),
        ];
```

⚠️ Trước khi viết, xác nhận tên bảng chi nhánh và cột của nó:

```bash
cd D:/CompanyProject/hrm/hrm-api && php artisan tinker --execute="echo implode(', ', Schema::getColumnListing('bank_branches'));"
```

Lệch tên bảng/cột thì sửa theo kết quả thật.

`«rules»`:

```php
            $existingNumbers = $snapshot['accountNumbers'] ?? [];
            $banks = $snapshot['banks'] ?? [];
            $branches = $snapshot['branches'] ?? [];
            $currencies = $snapshot['currencies'] ?? [];

            $number = trim((string) ($item['account_number'] ?? ''));
            $accountName = trim((string) ($item['account_name'] ?? ''));
            $bankCode = mb_strtoupper(trim((string) ($item['bank_code'] ?? '')));
            $branchName = trim((string) ($item['bank_branch'] ?? ''));
            $currencyCode = mb_strtoupper(trim((string) ($item['currency_code'] ?? '')));
            $statusText = trim((string) ($item['status'] ?? ''));

            if ($number === '') {
                $errors[] = 'Số tài khoản không được để trống';
            } elseif (mb_strlen($number) > 255) {
                $errors[] = 'Số tài khoản tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$number])) {
                    $errors[] = "Số tài khoản bị trùng với dòng {$seenInFile[$number]} trong file";
                } else {
                    $seenInFile[$number] = $index + 2;
                }
                if (isset($existingNumbers[$number])) {
                    $errors[] = 'Số tài khoản đã tồn tại trong hệ thống';
                }
            }

            if ($accountName === '') {
                $errors[] = 'Chủ tài khoản không được để trống';
            }

            $bankId = null;
            if ($bankCode === '') {
                $errors[] = 'Mã ngân hàng không được để trống';
            } elseif (!isset($banks[$bankCode])) {
                $errors[] = "Không tìm thấy ngân hàng: {$bankCode}";
            } else {
                $bankId = $banks[$bankCode]['id'];
            }

            if ($branchName === '') {
                $errors[] = 'Chi nhánh không được để trống';
            } elseif ($bankId !== null && !isset($branches[$bankId . '|' . mb_strtolower($branchName)])) {
                $errors[] = "Không tìm thấy chi nhánh \"{$branchName}\" thuộc ngân hàng {$bankCode}";
            }

            if ($currencyCode === '') {
                $errors[] = 'Mã tiền tệ không được để trống';
            } elseif (!isset($currencies[$currencyCode])) {
                $errors[] = "Không tìm thấy tiền tệ: {$currencyCode}";
            }

            if ($statusText !== '' && $this->parseStatus($statusText) === null) {
                $errors[] = 'Trạng thái chỉ nhận "Hoạt động" hoặc "Khóa"';
            }
```

`«create»`:

```php
                $number = trim((string) ($item['account_number'] ?? ''));
                $bankCode = mb_strtoupper(trim((string) ($item['bank_code'] ?? '')));
                $branchName = trim((string) ($item['bank_branch'] ?? ''));
                $currencyCode = mb_strtoupper(trim((string) ($item['currency_code'] ?? '')));

                if (CompanyAccount::query()->where('account_number', $number)->exists()) {
                    throw new \Exception('Số tài khoản đã tồn tại trong hệ thống');
                }

                $bank = $snapshot['banks'][$bankCode] ?? null;
                if (!$bank) {
                    throw new \Exception("Không tìm thấy ngân hàng: {$bankCode}");
                }

                $branchId = $snapshot['branches'][$bank['id'] . '|' . mb_strtolower($branchName)] ?? null;
                if (!$branchId) {
                    throw new \Exception("Không tìm thấy chi nhánh \"{$branchName}\" thuộc ngân hàng {$bankCode}");
                }

                $currencyId = $snapshot['currencies'][$currencyCode] ?? null;
                if (!$currencyId) {
                    throw new \Exception("Không tìm thấy tiền tệ: {$currencyCode}");
                }

                $this->createOrUpdate([
                    'account_number' => $number,
                    'account_name' => trim((string) ($item['account_name'] ?? '')),
                    'bank_id' => $bank['id'],
                    'bank_name' => $bank['name'],
                    'bank_branch_id' => $branchId,
                    'bank_branch' => $branchName,
                    'currency_id' => $currencyId,
                    'status' => $this->parseStatus((string) ($item['status'] ?? '')) ?? CompanyAccount::STATUS_ACTIVE,
                ]);
```

Giữ dòng `$snapshot = $this->importSnapshot();` ở đầu `import()` (Khuôn B đã có). Bỏ dòng
`$employeeId = ...`. Thêm Khuôn C với `«STATUS_ACTIVE» = CompanyAccount::STATUS_ACTIVE`,
`«STATUS_INACTIVE» = CompanyAccount::STATUS_LOCKED`.

- [x] **Step 3: `php -l Modules/Finance/Services/CompanyAccountService.php`**

- [x] **Step 4: Khuôn A vào Controller** — `«payloadKey» = account_banks`, `«serviceProp» = companyAccountService`

- [x] **Step 5: Thêm 2 route** trong nhóm `['prefix' => '/account-banks']`, đặt **ngay sau** `Route::get('/options', ...)` (vẫn trước mọi route `/{id}`):

```php
        Route::post('/import/validate', [CompanyAccountController::class, 'validateImport'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
        Route::post('/import', [CompanyAccountController::class, 'import'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
```

- [x] **Step 6: `php artisan route:list --path=finance/account-banks | grep import`**

- [x] **Step 7: Khuôn D vào `hrm-client/pages/finance/account-banks/index.vue`**

| Token | Giá trị |
| --- | --- |
| `«gate»` | `v-if="canManage"` |
| `«modalId»` | `import-account-bank-modal` |
| `«nhãn»` | `tài khoản ngân hàng` |
| `«apiPrefix»` | `finance/account-banks` |
| `«payloadKey»` | `account_banks` |
| `«fileName»` | `Mau_import_tai_khoan_ngan_hang.xlsx` |
| `«sheetName»` | `TK ngan hang` |
| `«required»` | `['AccountNumber', 'AccountName', 'BankCode', 'BankBranch', 'CurrencyCode']` |

`«columns»`:

```javascript
            return [
                {
                    key: 'AccountNumber',
                    label: 'Số tài khoản <span style="color: #dc2626;">*</span>',
                    aliases: ['Số tài khoản', 'So tai khoan', 'STK'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 0123456789',
                    width: '200px',
                },
                {
                    key: 'AccountName',
                    label: 'Chủ tài khoản <span style="color: #dc2626;">*</span>',
                    aliases: ['Chủ tài khoản', 'Chu tai khoan'],
                    type: 'text',
                    placeholder: 'VD: CÔNG TY TNHH ABC',
                    width: '280px',
                },
                {
                    key: 'BankCode',
                    label: 'Mã ngân hàng <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã ngân hàng', 'Ma ngan hang'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: VCB',
                    width: '160px',
                },
                {
                    key: 'BankBranch',
                    label: 'Chi nhánh <span style="color: #dc2626;">*</span>',
                    aliases: ['Chi nhánh', 'Chi nhanh'],
                    type: 'text',
                    placeholder: 'VD: Chi nhánh Hà Nội',
                    width: '240px',
                },
                {
                    key: 'CurrencyCode',
                    label: 'Mã tiền tệ <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã tiền tệ', 'Ma tien te'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: VND',
                    width: '140px',
                },
                {
                    key: 'Status',
                    label: 'Trạng thái',
                    aliases: ['Trạng thái', 'Trang thai'],
                    type: 'select',
                    options: [
                        { id: 'active', name: 'Hoạt động' },
                        { id: 'inactive', name: 'Khóa' },
                    ],
                    width: '140px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                account_number: String(row.AccountNumber || '').trim(),
                account_name: String(row.AccountName || '').trim(),
                bank_code: String(row.BankCode || '').trim().toUpperCase(),
                bank_branch: String(row.BankBranch || '').trim(),
                currency_code: String(row.CurrencyCode || '').trim().toUpperCase(),
                status: String(row.Status || '').trim(),
            }
```

- [x] **Step 8: Nghiệm thu Playwright + ảnh, đóng browser**

Ngoài 6 mục spec §10, phải test thêm: file có dòng ghi **mã ngân hàng không tồn tại** và dòng ghi
**chi nhánh không thuộc ngân hàng đó** → cả hai dòng phải báo lỗi rõ tên, và **không** có bản ghi
ngân hàng/chi nhánh nào được tạo thêm.

- [x] **Step 9: Báo user để commit**

---

**✅ BE XONG — FE CHƯA NGHIỆM THU BẰNG MẮT (11/09/2026).**

Nghiệm thu **ở tầng API** (gọi thẳng endpoint bằng token thật, vì Playwright MCP của phiên bị kẹt —
xem cuối mục). Kết quả `POST /api/v1/finance/account-banks/import/validate` với 5 dòng:

| Dòng | Tình huống | Kết quả |
| --- | --- | --- |
| 2 | `ZZTK000001` · VIETCOMBANK · Hoàn Kiếm · VNĐ | **hợp lệ** |
| 3 | STK `2591100125008` đã có | "Số tài khoản đã tồn tại trong hệ thống" |
| 4 | mã NH `ZZZBANK` | "Không tìm thấy ngân hàng: ZZZBANK" |
| 5 | chi nhánh `Long Biên` + NH `VIETCOMBANK` | "Không tìm thấy chi nhánh \"Long Biên\" thuộc ngân hàng VIETCOMBANK" |
| 6 | tiền tệ `ZZZ` | "Không tìm thấy tiền tệ: ZZZ" |

Dòng 5 là ca đáng giá nhất: `Long Biên` **CÓ tồn tại** trong `bank_branches` nhưng thuộc ngân hàng
**MB** — khoá ghép `bankId|tên chi nhánh` chặn đúng.

`POST .../import` → "Import xong: 1 thành công, 0 thất bại". Đối chiếu DB:

- `banks` 25 → **25**, `bank_branches` 132 → **132**, `currencies` 19 → **19** → **không tự tạo bản
  ghi cha nào** (đúng quyết định Q7).
- `company_accounts` 46 → 47; bản ghi có đủ `bank_id/bank_name`, `bank_branch_id/bank_branch`,
  `currency_id`, `company_id`, `created_by`; `catalog_histories` có `action=create`.
- Đã xoá dữ liệu thử, số về lại 46.

**Đơn giản hơn plan:** `createOrUpdate()` tự suy `bank_name` / `bank_branch` (từ id) và
`company_id` (từ `currentCompanyId()`), nên `import()` chỉ cần truyền **6 khoá**:
`account_number`, `account_name`, `bank_id`, `bank_branch_id`, `currency_id`, `status`.
Bảng chi nhánh là `bank_branches(id, bank_id, name, province_id)` — đúng như plan dự đoán.

✅ **Đã nghiệm thu trực quan (bổ sung cùng ngày, qua `playwright-b`):** mở `/finance/account-banks`,
nút Import Excel hiện đúng chỗ; nạp file → Validate ra **1 hợp lệ / 4 lỗi** với đúng 4 thông báo
trên; Bỏ dòng lỗi → Import → DB có bản ghi đủ `bank_name` / `bank_branch` / `currency_id`, và
`banks` / `bank_branches` / `currencies` vẫn 25/132/19. Đã xoá dữ liệu thử. 0 lỗi console.

⚠️ **Bẫy hạ tầng gặp ở task này:** `playwright-a` kẹt trạng thái, báo
`Browser is already in use for .../profile-a` kể cả sau khi đã tắt ĐÚNG PID mọi tiến trình Chrome
của profile đó và xoá `lockfile`; `browser_close` cũng trả cùng lỗi.

**Cách chữa nhanh — chuyển sang `playwright-b`** (profile riêng `C:/Users/Legion/.pw-mcp/profile-b`,
thư mục file `C:/Users/Legion/.pw-mcp/out-b`). Kiểm nó đang rảnh trước khi dùng, để không giẫm
phiên khác:

```powershell
Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
    Where-Object { $_.CommandLine -like '*profile-b*' }
```

Nhớ **copy file .xlsx thử sang `out-b`** — mỗi server chỉ cho đọc thư mục gốc của chính nó
(`browser_file_upload` báo "outside allowed roots" nếu lấy từ `out-a`).

### Checkpoint Phase 2 (phần Import)

Báo user: 5 màn Tài chính đã có Import, kèm ảnh nghiệm thu từng màn. Chờ duyệt rồi sang Task 9-12.

---

## Phase 2 (tiếp) — Export cho 4 màn Tài chính

### Khuôn E — thêm Export ở BE

**E1 — bộ cột** trong `hrm-api/app/ExcelExport/ExportColumnRegistry.php`, thêm vào mục `// ---- Finance ----`:

```php
        '«registryKey»' => «cols»,
```

**E2 — method `export()`** ở cuối class controller:

```php
    /**
     * Xuất Excel theo đúng bộ lọc đang áp dụng trên màn danh sách.
     */
    public function export(Request $request)
    {
        try {
            $collection = $this->«serviceProp»->«indexMethod»($request)->get();
            $data = «Resource»::collection($collection)->resolve();

            // Cột xuất theo lựa chọn ở popup "Chọn trường xuất file" (list-page mục 14b)
            return Excel::download(
                (new DynamicExport())
                    ->forData($data)
                    ->withColumns(ExportColumnRegistry::resolve('«registryKey»', $request))
                    ->withTitle('«tiêu đề»'),
                '«fileName»'
            );
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseBadRequest($e->getMessage());
        }
    }
```

Thêm `use` nếu thiếu: `App\ExcelExport\DynamicExport`, `App\ExcelExport\ExportColumnRegistry`,
`Maatwebsite\Excel\Facades\Excel`.

⚠️ `«indexMethod»` phải là hàm **trả query/paginator theo đúng bộ lọc** mà `index()` của controller
đang dùng. Mở `index()` đọc trước; nếu nó trả `->paginate()` thì tách hoặc gọi lại đúng hàm build
query, đừng để export ra khác danh sách.

**E3 — route** đặt TRƯỚC mọi route `/{id}`:

```php
        Route::get('/export', [«Controller»::class, 'export'])
            ->middleware('«permission»');
```

### Khuôn F — thêm Export ở FE

**F1 — import + mixin:**

```js
import ExportFieldsModal from '@/components/modal/export-fields-modal.vue'
import exportFieldsMixin from '@/utils/mixins/exportFieldsMixin.js'
import { downloadExcel } from '@/utils/download-excel'
import { buildQueryString } from '@/utils/url-action'
```

Thêm `exportFieldsMixin` vào `mixins`, `ExportFieldsModal` vào `components`.

**F2 — nút**, đặt ngay sau nút "Tạo mới":

```vue
                    <!-- Nhóm Xuất file -> XANH LÁ (button-convention 2b) -->
                    <V2BaseButton secondary status="success" size="sm" class="btn-compact" @click="openExportModal('excel')">
                        <template #prefix>
                            <i class="ri-file-excel-2-line" style="font-size: 13px"></i>
                        </template>
                        Xuất Excel
                    </V2BaseButton>
```

**F3 — popup**, đặt cạnh các modal khác:

```vue
        <!-- Chọn trường xuất file — bắt buộc ở mọi màn có nút Xuất (list-page 14b) -->
        <ExportFieldsModal
            :modal-id="exportFieldsModalId"
            :columns="exportFields"
            :default-selected="visibleExportFields"
            :exporting="exporting"
            @export="handleExportFields"
        />
```

**F4 — data:** `exportFieldsModalId: '«modalId»',`

**F5 — computed `exportFields()`:** `id` PHẢI khớp key khai ở `ExportColumnRegistry`, lệch là cột ra rỗng.

**F6 — method `runExport()`:**

```js
        async runExport(type, fields = null) {
            try {
                // `fields` = cột user tick ở popup, theo ĐÚNG thứ tự -> cũng là thứ tự cột file
                const fieldParam = Array.isArray(fields) && fields.length ? { fields: fields.join(',') } : {}
                this.$nuxt.$loading.start()
                // Xuất theo đúng bộ lọc đang áp dụng nhưng lấy TẤT CẢ dòng, không theo trang.
                await downloadExcel(
                    this.$axios,
                    `«apiPrefix»/export${buildQueryString({
                        ...this.buildParams({ page: 1, per_page: 10000 }),
                        ...fieldParam,
                    })}`,
                    '«fileName»'
                )
                this.$toasted?.global?.success?.({ message: 'Xuất Excel thành công' })
            } catch (error) {
                console.error('Error exporting:', error)
                if (error?.response?.status !== 403) {
                    this.$toasted?.global?.error?.({ message: 'Lỗi khi xuất Excel' })
                }
            } finally {
                this.$nuxt.$loading.finish()
            }
        },
```

Màn nào không có method `buildParams()` thì dùng đúng hàm dựng tham số lọc mà `loadData()` của màn
đó đang dùng — mở `loadData()` đọc trước, và **kiểm bằng mắt** rằng tham số gửi đi khi xuất trùng
khớp với tham số gửi đi khi nạp danh sách.

---

### Task 9: Export — Danh mục vụ việc `/finance/works`

**Files:**
- Modify: `hrm-api/app/ExcelExport/ExportColumnRegistry.php`, `Modules/Finance/Http/Controllers/V1/WorkController.php`, `Modules/Finance/Routes/api.php`
- Modify: `hrm-client/pages/finance/works/index.vue`

**Interfaces:**
- Consumes: `ExportColumnRegistry::resolve('works', $request)`
- Produces: endpoint `GET api/v1/finance/works/export`

- [x] **Step 1: Xác nhận Resource trả đúng key**

```bash
cd D:/CompanyProject/hrm/hrm-api && grep -rn "class WorkResource" -A 30 Modules/Finance/Transformers/ | head -35
```

Bộ key phải có đủ: `code`, `name`, `note`, `status_text`, `created_by_name`, `created_at`,
`updated_by_name`, `updated_at`. Thiếu key nào thì **bổ sung vào Resource** rồi mới khai ở registry —
key không khớp là cột ra rỗng.

- [x] **Step 2: Khai bộ cột** (Khuôn E1), `«registryKey» = works`:

```php
        'works' => [
            'code' => 'Mã vụ việc',
            'name' => 'Tên vụ việc',
            'note' => 'Ghi chú',
            'status_text' => 'Trạng thái',
            'created_by_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updated_by_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [x] **Step 3: Thêm `export()` vào Controller** (Khuôn E2)

| Token | Giá trị |
| --- | --- |
| `«serviceProp»` | `workService` |
| `«indexMethod»` | đọc `WorkController::index()` rồi dùng đúng hàm build query của nó |
| `«Resource»` | `WorkResource` (dùng đúng class `index()` đang dùng) |
| `«registryKey»` | `works` |
| `«tiêu đề»` | `Danh mục vụ việc` |
| `«fileName»` | `danh_muc_vu_viec.xlsx` |

- [x] **Step 4: Thêm route** (Khuôn E3) trong nhóm `['prefix' => 'works']`, TRƯỚC `Route::put('/{id}', ...)`:

```php
        Route::get('/export', [WorkController::class, 'export'])
            ->middleware('checkPermission:Quản lý danh mục vụ việc');
```

- [x] **Step 5: Xác nhận route**

```bash
cd D:/CompanyProject/hrm/hrm-api && php artisan route:list --path=finance/works | grep export
```

- [x] **Step 6: Đấu nối FE** (Khuôn F) vào `hrm-client/pages/finance/works/index.vue`

| Token | Giá trị |
| --- | --- |
| `«modalId»` | `works-export-fields-modal` |
| `«apiPrefix»` | `finance/works` |
| `«fileName»` | `danh_muc_vu_viec.xlsx` |

`exportFields()`:

```javascript
            return [
                { id: 'code', name: 'Mã vụ việc' },
                { id: 'name', name: 'Tên vụ việc' },
                { id: 'note', name: 'Ghi chú' },
                { id: 'status_text', name: 'Trạng thái' },
                { id: 'created_by_name', name: 'Người tạo' },
                { id: 'created_at', name: 'Ngày tạo' },
                { id: 'updated_by_name', name: 'Người cập nhật' },
                { id: 'updated_at', name: 'Ngày cập nhật' },
            ]
```

- [x] **Step 7: Nghiệm thu**

Đặt bộ lọc bất kỳ trên màn → Xuất Excel → mở file kiểm: số dòng khớp bộ lọc, đúng các cột đã tick,
đúng thứ tự tick, không ô nào bị Excel cảnh báo định dạng. Chụp ảnh. **Đóng browser.**

- [x] **Step 8: Báo user để commit**

---

**✅ XONG 11/09/2026.** Nghiệm thu:

- Gọi thẳng `GET /api/v1/finance/works/export`: không token → **401**; có token → **200**, file 81 KB.
- **Bộ lọc được tôn trọng**: không lọc → 24 dòng dữ liệu (= `COUNT(*)` bảng `works`);
  `keyword=ph` → 5 dòng (= số bản ghi khớp trong DB).
- **Tham số `fields=` có tác dụng**: truyền 5 key thì file ra đúng 5 cột đó.
- Qua UI: popup "Chọn trường xuất file" mở đúng, tick sẵn 8/8; bấm Xuất file → tải
  `danh_muc_vu_viec.xlsx`, header `STT · Mã vụ việc · Tên vụ việc · Ghi chú · Ngày tạo · Trạng thái ·
  Người tạo · Người cập nhật · Ngày cập nhật` — **đúng thứ tự tick trong popup**; 24 dòng dữ liệu;
  ô rỗng để TRỐNG (không in dấu `-`). 0 lỗi console.

⚠️ **Lỗi đã bắt được khi xem bằng mắt — kiểm mục này ở MỌI task Export còn lại:** lần chạy đầu popup
chỉ tick sẵn **7/8 trường, thiếu "Trạng thái"**. Nguyên nhân: cột trạng thái trên bảng đặt key
`workStatus`, trong khi key xuất file là `status_text`; `exportFieldsMixin` chỉ tự suy được khi key
bảng trùng key xuất hoặc chỉ lệch hậu tố `_text`. **Fix:** khai trong `data()`

```js
exportFieldKeyMap: { workStatus: 'status_text' },
```

→ sau đó tick sẵn đủ 8/8. Trước khi coi một task Export là xong, luôn mở popup và **đọc dòng
"Đang chọn n/m trường"**; `n < m` là dấu hiệu có cột bị rớt.

Ghi chú khác: `DynamicExport` tự chèn khối chân ký ("Ngày ..., tháng ..., năm ..." + "Người lập") ở
cuối file — khi đếm số dòng dữ liệu để đối chiếu thì phải bỏ khối này ra, nếu không sẽ lệch 1 dòng.

### Task 10: Export — Danh mục mã phí `/finance/cost-debts`

Cùng khuôn Task 9.

- [x] **Step 1: Xác nhận Resource trả đủ key** `code`, `name`, `note`, `status_text`, `created_by_name`, `created_at`, `updated_by_name`, `updated_at`

- [x] **Step 2: Khai bộ cột**, `«registryKey» = cost_debts`:

```php
        'cost_debts' => [
            'code' => 'Mã phí',
            'name' => 'Tên mã phí',
            'note' => 'Ghi chú',
            'status_text' => 'Trạng thái',
            'created_by_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updated_by_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [x] **Step 3: `export()` vào `CostDebtController`** — `«serviceProp» = costDebtService`, `«tiêu đề» = Danh mục mã phí`, `«fileName» = danh_muc_ma_phi.xlsx`

- [x] **Step 4: Route** trong nhóm `['prefix' => 'cost-debts']`, trước `Route::put('/{id}', ...)`:

```php
        Route::get('/export', [CostDebtController::class, 'export'])
            ->middleware('checkPermission:Quản lý danh mục mã phí');
```

- [x] **Step 5: `php artisan route:list --path=finance/cost-debts | grep export`**

- [x] **Step 6: Khuôn F** vào `pages/finance/cost-debts/index.vue` — `«modalId» = cost-debts-export-fields-modal`, `«apiPrefix» = finance/cost-debts`, `«fileName» = danh_muc_ma_phi.xlsx`. `exportFields()` copy Task 9, đổi nhãn `Mã vụ việc` → `Mã phí`, `Tên vụ việc` → `Tên mã phí`.

- [x] **Step 7: Nghiệm thu + ảnh, đóng browser**

- [x] **Step 8: Báo user để commit**

---

### Task 11: Export — Danh mục nguồn vốn `/finance/source-capitals`

Bảng này **không có** cột Ghi chú / Mã / Người cập nhật trên màn.

- [x] **Step 1: Xác nhận Resource trả đủ key** `name`, `status_text`, `created_by_name`, `created_at`

- [x] **Step 2: Khai bộ cột**, `«registryKey» = source_capitals`:

```php
        'source_capitals' => [
            'name' => 'Tên nguồn vốn',
            'status_text' => 'Trạng thái',
            'created_by_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
        ],
```

- [x] **Step 3: `export()` vào `SourceCapitalController`** — `«serviceProp» = sourceCapitalService`, `«tiêu đề» = Danh mục nguồn vốn`, `«fileName» = danh_muc_nguon_von.xlsx`

- [x] **Step 4: Route** trong nhóm `['prefix' => 'source-capitals']`, trước `Route::put('/{id}', ...)`:

```php
        Route::get('/export', [SourceCapitalController::class, 'export'])
            ->middleware('checkPermission:Quản lý danh mục nguồn vốn');
```

- [x] **Step 5: `php artisan route:list --path=finance/source-capitals | grep export`**

- [x] **Step 6: Khuôn F** vào `pages/finance/source-capitals/index.vue` — `«modalId» = source-capitals-export-fields-modal`, `«apiPrefix» = finance/source-capitals`, `«fileName» = danh_muc_nguon_von.xlsx`

```javascript
            return [
                { id: 'name', name: 'Tên nguồn vốn' },
                { id: 'status_text', name: 'Trạng thái' },
                { id: 'created_by_name', name: 'Người tạo' },
                { id: 'created_at', name: 'Ngày tạo' },
            ]
```

- [x] **Step 7: Nghiệm thu + ảnh, đóng browser**

- [x] **Step 8: Báo user để commit**

---

### Task 12: Export — Danh mục tài khoản ngân hàng `/finance/account-banks`

- [x] **Step 1: Xác nhận Resource trả đủ key** `account_number`, `account_name`, `bank_name`, `bank_branch`, `currency_text`, `status_text`, `created_by_name`, `created_at`, `updated_by_name`, `updated_at`

- [x] **Step 2: Khai bộ cột**, `«registryKey» = company_accounts`:

```php
        'company_accounts' => [
            'account_number' => 'Số tài khoản',
            'account_name' => 'Chủ tài khoản',
            'bank_name' => 'Ngân hàng',
            'bank_branch' => 'Chi nhánh',
            'currency_text' => 'Loại tiền tệ',
            'status_text' => 'Trạng thái',
            'created_by_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updated_by_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [x] **Step 3: `export()` vào `CompanyAccountController`** — `«serviceProp» = companyAccountService`, `«tiêu đề» = Danh mục tài khoản ngân hàng`, `«fileName» = danh_muc_tai_khoan_ngan_hang.xlsx`

- [x] **Step 4: Route** trong nhóm `['prefix' => '/account-banks']`, ngay sau `Route::get('/options', ...)`:

```php
        Route::get('/export', [CompanyAccountController::class, 'export'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
```

- [x] **Step 5: `php artisan route:list --path=finance/account-banks | grep export`**

- [x] **Step 6: Khuôn F** vào `pages/finance/account-banks/index.vue` — `«modalId» = account-banks-export-fields-modal`, `«apiPrefix» = finance/account-banks`, `«fileName» = danh_muc_tai_khoan_ngan_hang.xlsx`

```javascript
            return [
                { id: 'account_number', name: 'Số tài khoản' },
                { id: 'account_name', name: 'Chủ tài khoản' },
                { id: 'bank_name', name: 'Ngân hàng' },
                { id: 'bank_branch', name: 'Chi nhánh' },
                { id: 'currency_text', name: 'Loại tiền tệ' },
                { id: 'status_text', name: 'Trạng thái' },
                { id: 'created_by_name', name: 'Người tạo' },
                { id: 'created_at', name: 'Ngày tạo' },
                { id: 'updated_by_name', name: 'Người cập nhật' },
                { id: 'updated_at', name: 'Ngày cập nhật' },
            ]
```

⚠️ Bảng trên màn để cột `status` (vẽ badge) còn file xuất cần chữ nên khai `status_text` — đây đúng
là trường hợp `exportFieldsMixin` tự thử hậu tố `_text`, không cần `exportFieldKeyMap`.

- [x] **Step 7: Nghiệm thu + ảnh, đóng browser**

- [x] **Step 8: Báo user để commit**

---

**✅ XONG 11/09/2026** (làm gộp 3 màn cùng lượt vì chung khuôn).

| Màn | Số dòng file | Đối chiếu `total` của màn danh sách |
| --- | --- | --- |
| Mã phí | 22 | 22 ✓ |
| Nguồn vốn | 6 | 6 ✓ |
| Tài khoản ngân hàng | 26 | 26 ✓ |

File tải qua UI có header khớp **đúng các cột đã tick và đúng thứ tự tick**. 0 lỗi console.

⚠️ **Số dòng file KHÁC `COUNT(*)` của bảng — và đó là ĐÚNG:** `source_capitals` có 9 bản ghi trong
DB nhưng màn chỉ hiện 6 (ẩn bản ghi đã khoá mềm); `company_accounts` có 46 nhưng màn chỉ hiện 26
(lọc theo công ty đang đăng nhập). Export dùng lại đúng hàm mà `index()` dùng nên khớp **màn**,
không khớp **bảng**. Khi nghiệm thu, đối chiếu với `total` trả về từ endpoint danh sách:

```bash
curl -s "http://127.0.0.1:8000/api/v1/finance/<man>?page=1&per_page=10" -H "Authorization: Bearer $TOKEN"
```

⚠️ **Lại gặp bẫy `exportFieldKeyMap`** (giống Task 9): cột trạng thái trên bảng đặt key
`costDebtStatus` / `accountBankStatus`, không phải `status` → phải khai ánh xạ tay ở `data()`,
nếu không popup rớt mất cột Trạng thái. Màn Nguồn vốn không có cột trạng thái nên không cần.

📌 **Lệch so với spec §6 — đã quyết và ghi lại:** spec ghi bộ cột xuất của **Nguồn vốn** gồm
`status_text`, nhưng `SourceCapitalListResource` không trả trường đó **và bảng trên màn cũng không
có cột Trạng thái**. Đã **bỏ `status_text`** khỏi bộ cột thay vì thêm một trường màn không hiển thị
— giữ đúng nguyên tắc "file xuất khớp thứ người dùng đang nhìn". Bộ cột cuối: Tên nguồn vốn ·
Người tạo · Ngày tạo.

### Checkpoint Phase 2

Báo user: 5 màn Tài chính có Import, 4 màn có thêm Export. Kèm ảnh từng màn. Chờ duyệt rồi sang Phase 3.

---

## Phase 3 — Địa lý + Ngân hàng (5 màn, mỗi màn cả Import lẫn Export)

**Khác Phase 2 ở 3 điểm, nhớ kỹ:**

1. **Không màn nào gate quyền.** Route BE không gắn `checkPermission`, nút "Tạo mới" không có
   `v-if` — nút Import và nút Xuất Excel cũng **không gate**. `«gate»` để **trống**. Cấm tạo cờ
   `canManage = true` giả.
2. **Controller trả `XxxListResource` bọc paginator**, không phải `Resource::collection()` như
   Finance. Hàm `export()` phải dựng `$data` bằng chính resource đó:
   `$data = (new NationListResource($paginator))->toArray($request);` — đọc file resource trước
   để biết nó trả mảng phẳng hay còn bọc thêm tầng.
3. **Resource hiện trả `status` dạng SỐ.** File xuất cần chữ → thêm khoá `status_text` vào resource
   (`$data->status == 1 ? 'Hoạt động' : 'Khóa'`, dùng đúng hằng `STATUS_ACTIVE` / `STATUS_INACTIVE`
   của entity) rồi mới khai ở `ExportColumnRegistry`.

Bộ cột xuất file khai trong `ExportColumnRegistry.php` dưới một mục mới `// ---- Human ----`.

---

### Task 13: Quốc gia `/human/nations` — Import + Export

**Files:** `Modules/Human/Services/NationService.php`, `Modules/Human/Http/Controllers/Api/V1/NationController.php`,
`Modules/Human/Transformers/NationResource/NationListResource.php`, `Modules/Human/Routes/api.php` (nhóm `/human/nations`, dòng ~396),
`hrm-api/app/ExcelExport/ExportColumnRegistry.php`, `hrm-client/pages/human/nations/index.vue`

**Interfaces:** Produces `NationService::validateRows(array $items, array $snapshot): array`, `$snapshot = ['codes' => array<string mã HOA, int id>]`

- [x] **Step 1: Thêm 3 method vào `NationService`** (Khuôn B)

`«snapshot»`:

```php
        return [
            'codes' => Nation::query()
                ->pluck('id', 'code')
                ->mapWithKeys(function ($id, $code) {
                    return [mb_strtoupper(trim((string) $code)) => $id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $existingCodes = $snapshot['codes'] ?? [];

            $name = trim((string) ($item['name'] ?? ''));
            $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));
            $postalCode = trim((string) ($item['postal_code'] ?? ''));

            if ($name === '') {
                $errors[] = 'Tên quốc gia không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên quốc gia tối đa 255 ký tự';
            }

            if ($code === '') {
                $errors[] = 'Mã quốc gia không được để trống';
            } elseif (mb_strlen($code) > 255) {
                $errors[] = 'Mã quốc gia tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$code])) {
                    $errors[] = "Mã quốc gia bị trùng với dòng {$seenInFile[$code]} trong file";
                } else {
                    $seenInFile[$code] = $index + 2;
                }
                if (isset($existingCodes[$code])) {
                    $errors[] = 'Mã quốc gia đã tồn tại trong hệ thống';
                }
            }

            if ($postalCode !== '' && mb_strlen($postalCode) > 255) {
                $errors[] = 'Mã bưu chính tối đa 255 ký tự';
            }
```

`«create»`:

```php
                $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));

                if (Nation::query()->where('code', $code)->exists()) {
                    throw new \Exception('Mã quốc gia đã tồn tại trong hệ thống');
                }

                $this->createNation([
                    'name' => trim((string) ($item['name'] ?? '')),
                    'code' => $code,
                    'postal_code' => trim((string) ($item['postal_code'] ?? '')) ?: null,
                    'status' => Nation::STATUS_ACTIVE,
                ]);
```

Bỏ dòng `$employeeId = ...`. **Không** thêm Khuôn C (file mẫu màn này không có cột Trạng thái).

⚠️ Mở `NationService::createNation()` đọc trước: nếu nó đọc thêm key nào (vd `created_by`) thì bổ
sung đúng key đó vào mảng truyền vào.

- [x] **Step 2: `php -l Modules/Human/Services/NationService.php`**

- [x] **Step 3: Khuôn A vào `NationController`** — `«payloadKey» = nations`, `«serviceProp» = nationService`

- [x] **Step 4: Thêm `status_text` vào `NationListResource::toArray()`**

Trong khối `$nationData[] = [...]`, thêm ngay sau `'status' => $data->status,`:

```php
                'status_text' => (int) $data->status === Nation::STATUS_ACTIVE ? 'Hoạt động' : 'Khóa',
```

Thêm `use Modules\Human\Entities\Nation;` ở đầu file nếu chưa có.

- [x] **Step 5: Thêm `export()` vào `NationController`** (Khuôn E2, biến thể Human)

```php
    /**
     * Xuất Excel theo đúng bộ lọc đang áp dụng trên màn danh sách.
     */
    public function export(Request $request)
    {
        try {
            $nations = $this->nationService->getNations($request);
            $data = (new NationListResource($nations))->toArray($request);

            return Excel::download(
                (new DynamicExport())
                    ->forData($data)
                    ->withColumns(ExportColumnRegistry::resolve('nations', $request))
                    ->withTitle('Danh mục quốc gia'),
                'danh_muc_quoc_gia.xlsx'
            );
        } catch (Exception $e) {
            Log::error($e);

            return $this->responseBadRequest($e->getMessage());
        }
    }
```

⚠️ Kiểm bằng `dd($data)` một lần: `toArray()` phải trả **mảng phẳng các dòng**. Nếu nó bọc thêm
tầng (vd `['data' => [...]]`) thì lấy đúng nhánh chứa danh sách.

- [x] **Step 6: Khai bộ cột** trong `ExportColumnRegistry.php`, mục mới `// ---- Human ----`:

```php
        'nations' => [
            'name' => 'Tên quốc gia',
            'code' => 'Mã quốc gia',
            'postal_code' => 'Mã bưu chính',
            'status_text' => 'Trạng thái',
            'created_by_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updated_by_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [x] **Step 7: Thêm 3 route** trong nhóm `['prefix' => '/human/nations']`, TRƯỚC `Route::get('/{id}', ...)`:

```php
        Route::get('/export', [NationController::class, 'export']);
        Route::post('/import/validate', [NationController::class, 'validateImport']);
        Route::post('/import', [NationController::class, 'import']);
```

- [x] **Step 8: Xác nhận route**

```bash
cd D:/CompanyProject/hrm/hrm-api && php artisan route:list --path=human/nations
```

Expected: có `GET .../export`, `POST .../import`, `POST .../import/validate`.

- [x] **Step 9: Đấu nối FE** — Khuôn D (Import) + Khuôn F (Export) vào `hrm-client/pages/human/nations/index.vue`

| Token | Giá trị |
| --- | --- |
| `«gate»` | **để trống** (màn không gate quyền — xem ghi chú đầu Phase 3) |
| `«modalId»` (import) | `import-nation-modal` |
| `«modalId»` (export) | `nations-export-fields-modal` |
| `«nhãn»` | `quốc gia` |
| `«apiPrefix»` | `human/nations` |
| `«payloadKey»` | `nations` |
| `«fileName»` (mẫu) | `Mau_import_quoc_gia.xlsx` |
| `«fileName»` (xuất) | `danh_muc_quoc_gia.xlsx` |
| `«sheetName»` | `Quoc gia` |
| `«required»` | `['Name', 'Code']` |

`«columns»`:

```javascript
            return [
                {
                    key: 'Name',
                    label: 'Tên quốc gia <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên quốc gia', 'Ten quoc gia', 'Tên', 'Ten'],
                    type: 'text',
                    placeholder: 'VD: Việt Nam',
                    width: '280px',
                },
                {
                    key: 'Code',
                    label: 'Mã quốc gia <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã quốc gia', 'Ma quoc gia', 'Mã', 'Ma'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: VN',
                    width: '160px',
                },
                {
                    key: 'PostalCode',
                    label: 'Mã bưu chính',
                    aliases: ['Mã bưu chính', 'Ma buu chinh'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 100000',
                    width: '160px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                name: String(row.Name || '').trim(),
                code: String(row.Code || '').trim().toUpperCase(),
                postal_code: String(row.PostalCode || '').trim(),
            }
```

`exportFields()`:

```javascript
            return [
                { id: 'name', name: 'Tên quốc gia' },
                { id: 'code', name: 'Mã quốc gia' },
                { id: 'postal_code', name: 'Mã bưu chính' },
                { id: 'status_text', name: 'Trạng thái' },
                { id: 'created_by_name', name: 'Người tạo' },
                { id: 'created_at', name: 'Ngày tạo' },
                { id: 'updated_by_name', name: 'Người cập nhật' },
                { id: 'updated_at', name: 'Ngày cập nhật' },
            ]
```

Màn này dùng `apiGet` (không phải `apiGetMethod`) — mixin import gọi `apiPostMethod`, vẫn chạy
được vì đó là action root dùng chung. Kiểm tên hàm nạp danh sách, chưa có `loadData` thì khai thêm.

- [x] **Step 10: Nghiệm thu Playwright + ảnh, đóng browser** — đủ 6 mục spec §10; riêng mục 6 (ẩn nút theo quyền) **bỏ qua** vì màn không gate quyền, ghi rõ lý do khi báo cáo

- [x] **Step 11: Báo user để commit**

---

**✅ XONG 11/09/2026.** Import + Export màn Quốc gia, nghiệm thu qua UI (`playwright-b`) và API.

- Validate: dòng trùng tên `Việt Nam` → "Tên quốc gia đã tồn tại trong hệ thống"; trùng mã `gggg` →
  "Mã quốc gia đã tồn tại trong hệ thống"; thiếu cả hai → 2 lỗi; trùng tên trong file → bắt đúng.
- Import qua UI → DB có `country_code=ZZUI1`, `postal_code`, `status=1`, `created_by`, lịch sử `create`.
- Export: file 38 dòng khớp danh sách, header đúng cột đã tick, `Trạng thái` ra chữ. 0 lỗi console.
- Hai nút **không gate quyền**, đúng hiện trạng nút "Tạo mới" của màn.

⚠️ **BA điểm riêng của nhóm Nhân sự — áp cho Task 14-17:**

1. **`getNations()` phân trang bằng `limit`, KHÔNG phải `per_page`.** Gửi `per_page` thì file chỉ
   ra 10 dòng. Kiểm hàm lấy danh sách của từng màn trước khi viết `runExport`.
2. **Bảng `nations` không có cột `code`** — mã ở cột **`country_code`**, entity chỉ khai accessor/
   mutator bắc cầu. `pluck('id', 'code')` sẽ lỗi "column not found"; phải đọc thẳng `country_code`.
   Ngược lại, payload truyền vào `createNation()` vẫn dùng key `code` được (nhờ mutator).
3. **Cột trạng thái trên bảng đặt key `nationStatus`** → phải khai
   `exportFieldKeyMap: { nationStatus: 'status_text' }`, nếu không popup rớt cột Trạng thái.
   (Cùng bẫy với `workStatus` / `costDebtStatus` / `accountBankStatus`.)

🐞 **LỖI CÓ SẴN phát hiện được, NẰM NGOÀI phạm vi feature — chưa sửa, đã báo user:**
`NationService::getNations()` khai whitelist sort `'code' => 'nations.code'` nhưng cột thật là
`country_code` → **bấm sắp xếp theo cột "Mã quốc gia" trên màn danh sách trả HTTP 500**
(`Unknown column 'nations.code' in 'order clause'`). Đã tái hiện bằng
`GET /api/v1/human/nations?sort_by=code` → 500 (trong khi `sort_by=name` → 200).
Sửa chỉ cần đổi 1 dòng thành `'code' => 'nations.country_code'`, nhưng đó là hành vi màn danh sách
nên chờ user quyết.

Ghi chú hạ tầng: nút "Xuất file" trong popup thỉnh thoảng làm Playwright báo
`Cannot read properties of undefined (reading 'url')` và tab nhảy về `about:blank` — file KHÔNG
tải về. Không phải lỗi sản phẩm (server không ghi lỗi nào); bấm lại là được.

### Task 14: Khu vực `/human/areas` — Import + Export

Khác Task 13: có **1 tra cứu cha theo mã quốc gia**, chống trùng theo **tên + quốc gia** (bảng không có `code`).

- [x] **Step 1: Thêm 3 method vào `AreaService`** (Khuôn B)

`«snapshot»`:

```php
        return [
            'nations' => Nation::query()
                ->get(['id', 'code', 'name'])
                ->mapWithKeys(function ($nation) {
                    return [mb_strtoupper(trim((string) $nation->code)) => ['id' => $nation->id, 'name' => $nation->name]];
                })
                ->toArray(),
            'names' => Area::query()
                ->get(['id', 'name', 'nation_id'])
                ->mapWithKeys(function ($area) {
                    return [$area->nation_id . '|' . mb_strtolower(trim((string) $area->name)) => $area->id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $nations = $snapshot['nations'] ?? [];
            $existingNames = $snapshot['names'] ?? [];

            $name = trim((string) ($item['name'] ?? ''));
            $nationCode = mb_strtoupper(trim((string) ($item['nation_code'] ?? '')));

            if ($name === '') {
                $errors[] = 'Tên khu vực không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên khu vực tối đa 255 ký tự';
            }

            $nationId = null;
            if ($nationCode === '') {
                $errors[] = 'Mã quốc gia không được để trống';
            } elseif (!isset($nations[$nationCode])) {
                $errors[] = "Không tìm thấy quốc gia: {$nationCode}";
            } else {
                $nationId = $nations[$nationCode]['id'];
            }

            if ($name !== '' && $nationId !== null) {
                $key = $nationId . '|' . mb_strtolower($name);
                if (isset($seenInFile[$key])) {
                    $errors[] = "Khu vực bị trùng với dòng {$seenInFile[$key]} trong file";
                } else {
                    $seenInFile[$key] = $index + 2;
                }
                if (isset($existingNames[$key])) {
                    $errors[] = 'Khu vực này đã tồn tại trong quốc gia đã chọn';
                }
            }
```

`«create»`:

```php
                $name = trim((string) ($item['name'] ?? ''));
                $nationCode = mb_strtoupper(trim((string) ($item['nation_code'] ?? '')));

                $nation = $snapshot['nations'][$nationCode] ?? null;
                if (!$nation) {
                    throw new \Exception("Không tìm thấy quốc gia: {$nationCode}");
                }

                $trung = Area::query()
                    ->where('nation_id', $nation['id'])
                    ->whereRaw('LOWER(TRIM(name)) = ?', [mb_strtolower($name)])
                    ->exists();
                if ($trung) {
                    throw new \Exception('Khu vực này đã tồn tại trong quốc gia đã chọn');
                }

                $this->createArea([
                    'name' => $name,
                    'nation_id' => $nation['id'],
                    'nation_name' => $nation['name'],
                    'status' => Area::STATUS_ACTIVE,
                ]);
```

Giữ dòng `$snapshot = $this->importSnapshot();` đầu `import()`. Bỏ `$employeeId = ...`.

- [x] **Step 2: `php -l Modules/Human/Services/AreaService.php`**
- [x] **Step 3: Khuôn A vào `AreaController`** — `«payloadKey» = areas`, `«serviceProp» = areaService`
- [x] **Step 4: Thêm `status_text` vào `AreaListResource`** (như Task 13 Step 4, dùng `Area::STATUS_ACTIVE`)
- [x] **Step 5: `export()` vào `AreaController`** — `getAreas($request)` (kiểm tên hàm thật trong `AreaController::index()`), resource `AreaListResource`, registry key `areas`, tiêu đề `Danh mục khu vực`, file `danh_muc_khu_vuc.xlsx`
- [x] **Step 6: Bộ cột registry:**

```php
        'areas' => [
            'name' => 'Tên khu vực',
            'nation_name' => 'Quốc gia',
            'status_text' => 'Trạng thái',
            'created_by_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updated_by_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

Kiểm `AreaListResource` có trả `nation_name` không; không có thì bổ sung.

- [x] **Step 7: 3 route** trong nhóm `['prefix' => '/human/areas']`, trước `Route::get('/{id}', ...)` — y khuôn Task 13 Step 7, đổi `NationController` → `AreaController`
- [x] **Step 8: `php artisan route:list --path=human/areas`**
- [x] **Step 9: FE** `hrm-client/pages/human/areas/index.vue`

| Token | Giá trị |
| --- | --- |
| `«gate»` | để trống |
| `«modalId»` (import / export) | `import-area-modal` / `areas-export-fields-modal` |
| `«nhãn»` | `khu vực` |
| `«apiPrefix»` | `human/areas` |
| `«payloadKey»` | `areas` |
| `«fileName»` (mẫu / xuất) | `Mau_import_khu_vuc.xlsx` / `danh_muc_khu_vuc.xlsx` |
| `«sheetName»` | `Khu vuc` |
| `«required»` | `['Name', 'NationCode']` |

```javascript
            return [
                {
                    key: 'Name',
                    label: 'Tên khu vực <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên khu vực', 'Ten khu vuc', 'Tên', 'Ten'],
                    type: 'text',
                    placeholder: 'VD: Miền Bắc',
                    width: '280px',
                },
                {
                    key: 'NationCode',
                    label: 'Mã quốc gia <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã quốc gia', 'Ma quoc gia', 'Quốc gia', 'Quoc gia'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: VN',
                    width: '160px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                name: String(row.Name || '').trim(),
                nation_code: String(row.NationCode || '').trim().toUpperCase(),
            }
```

`exportFields()`: `name` / `nation_name` / `status_text` / `created_by_name` / `created_at` / `updated_by_name` / `updated_at` với nhãn như bộ cột registry ở Step 6.

- [x] **Step 10: Nghiệm thu + ảnh, đóng browser.** Bắt buộc test thêm dòng ghi **mã quốc gia không tồn tại** → báo lỗi, **không** tự tạo quốc gia mới
- [x] **Step 11: Báo user để commit**

---

**✅ XONG 11/09/2026.** Import + Export màn Khu vực.

Validate (5 dòng → **1 hợp lệ / 4 lỗi**): trùng tên `Tây Bắc Bộ` → "Tên khu vực đã tồn tại trong hệ
thống"; mã quốc gia `ZZZ` → "Không tìm thấy quốc gia: ZZZ"; thiếu cả hai → 2 lỗi; trùng tên trong
file (khác hoa/thường) → bắt đúng.

Import → `areas` 22 → 23, bản ghi có `nation_id=7`, `nation_name=Korea` (service tự suy từ id),
`status=1`, lịch sử `create`. **`nations` giữ nguyên 36** → không tự tạo quốc gia mới (đúng Q7).
Export: 23 dòng, header `Tên khu vực · Quốc gia · Trạng thái · Người tạo · Ngày tạo · Người cập
nhật · Ngày cập nhật`. UI có đủ 3 nút, popup tick sẵn có "Trạng thái". Đã xoá dữ liệu thử.

📌 Chống trùng tên **TOÀN CỤC**, không theo quốc gia — đúng đính chính (`CreateAreasRequest.php:21`
dùng `Rule::unique('areas','name')` không kèm `where`). `createArea()` tự set `nation_name` nên
`import()` chỉ cần truyền `nation_id`.

### Task 15: Tỉnh/TP `/human/provinces` — Import + Export

Màn có **2 tra cứu cha** (quốc gia theo mã, khu vực theo tên trong quốc gia đó) → task này có unit test.

**Files:** thêm `hrm-api/Modules/Human/Tests/Unit/ProvinceImportValidationTest.php`

**Interfaces:** Produces `ProvinceService::validateRows(array $items, array $snapshot): array` với
`$snapshot = ['nations' => array<string mã HOA, array{id,name}>, 'areas' => array<string "nationId|tên thường", int id>, 'names' => array<string "nationId|tên thường", int id>]`

- [x] **Step 1: Viết test thất bại**

Tạo `hrm-api/Modules/Human/Tests/Unit/ProvinceImportValidationTest.php`:

```php
<?php

namespace Modules\Human\Tests\Unit;

use Modules\Human\Services\ProvinceService;
use PHPUnit\Framework\TestCase;

/**
 * Unit test cho `ProvinceService::validateRows()` — hàm THUẦN. Trọng tâm: tra cứu 2 cấp cha
 * (quốc gia theo mã, khu vực theo tên TRONG quốc gia đó) và quy tắc KHÔNG tự tạo bản ghi cha.
 */
class ProvinceImportValidationTest extends TestCase
{
    private function snapshot(): array
    {
        return [
            'nations' => ['VN' => ['id' => 1, 'name' => 'Việt Nam']],
            'areas' => ['1|miền bắc' => 10],
            'names' => ['1|hà nội' => 100],
        ];
    }

    private function row(array $override = []): array
    {
        return array_merge([
            'name' => 'Hải Phòng',
            'code' => '31',
            'license_plate' => '15',
            'nation_code' => 'VN',
            'area_name' => 'Miền Bắc',
        ], $override);
    }

    public function test_dong_hop_le()
    {
        $result = (new ProvinceService())->validateRows([$this->row()], $this->snapshot());

        $this->assertSame(1, $result['validCount']);
        $this->assertTrue($result['rows'][0]['isValid']);
    }

    public function test_khong_tim_thay_quoc_gia()
    {
        $result = (new ProvinceService())->validateRows([
            $this->row(['nation_code' => 'XX']),
        ], $this->snapshot());

        $this->assertFalse($result['rows'][0]['isValid']);
        $this->assertContains('Không tìm thấy quốc gia: XX', $result['rows'][0]['errors']);
    }

    public function test_khu_vuc_khong_thuoc_quoc_gia_da_chon()
    {
        $result = (new ProvinceService())->validateRows([
            $this->row(['area_name' => 'Miền Nam']),
        ], $this->snapshot());

        $this->assertFalse($result['rows'][0]['isValid']);
        $this->assertContains('Không tìm thấy khu vực "Miền Nam" thuộc quốc gia VN', $result['rows'][0]['errors']);
    }

    public function test_tinh_da_ton_tai_trong_he_thong()
    {
        $result = (new ProvinceService())->validateRows([
            $this->row(['name' => 'Hà Nội']),
        ], $this->snapshot());

        $this->assertFalse($result['rows'][0]['isValid']);
        $this->assertContains('Tỉnh/TP này đã tồn tại trong quốc gia đã chọn', $result['rows'][0]['errors']);
    }

    public function test_thieu_truong_bat_buoc()
    {
        $result = (new ProvinceService())->validateRows([
            $this->row(['name' => '', 'license_plate' => '']),
        ], $this->snapshot());

        $this->assertContains('Tên tỉnh/TP không được để trống', $result['rows'][0]['errors']);
        $this->assertContains('Biển số xe không được để trống', $result['rows'][0]['errors']);
    }

    public function test_trung_nhau_trong_cung_file()
    {
        $result = (new ProvinceService())->validateRows([
            $this->row(['name' => 'Đà Nẵng']),
            $this->row(['name' => 'đà nẵng']),
        ], $this->snapshot());

        $this->assertTrue($result['rows'][0]['isValid']);
        $this->assertFalse($result['rows'][1]['isValid']);
        $this->assertContains('Tỉnh/TP bị trùng với dòng 2 trong file', $result['rows'][1]['errors']);
    }
}
```

- [x] **Step 2: Chạy test, xác nhận FAIL**

```bash
cd D:/CompanyProject/hrm/hrm-api && php vendor/bin/phpunit Modules/Human/Tests/Unit/ProvinceImportValidationTest.php
```

Expected: FAIL — `Call to undefined method ...::validateRows()`.

- [x] **Step 3: Thêm 3 method vào `ProvinceService`** (Khuôn B)

`«snapshot»`:

```php
        return [
            'nations' => Nation::query()
                ->get(['id', 'code', 'name'])
                ->mapWithKeys(function ($nation) {
                    return [mb_strtoupper(trim((string) $nation->code)) => ['id' => $nation->id, 'name' => $nation->name]];
                })
                ->toArray(),
            'areas' => Area::query()
                ->get(['id', 'name', 'nation_id'])
                ->mapWithKeys(function ($area) {
                    return [$area->nation_id . '|' . mb_strtolower(trim((string) $area->name)) => $area->id];
                })
                ->toArray(),
            'names' => Province::query()
                ->get(['id', 'name', 'nation_id'])
                ->mapWithKeys(function ($province) {
                    return [$province->nation_id . '|' . mb_strtolower(trim((string) $province->name)) => $province->id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $nations = $snapshot['nations'] ?? [];
            $areas = $snapshot['areas'] ?? [];
            $existingNames = $snapshot['names'] ?? [];

            $name = trim((string) ($item['name'] ?? ''));
            $code = trim((string) ($item['code'] ?? ''));
            $licensePlate = trim((string) ($item['license_plate'] ?? ''));
            $nationCode = mb_strtoupper(trim((string) ($item['nation_code'] ?? '')));
            $areaName = trim((string) ($item['area_name'] ?? ''));

            if ($name === '') {
                $errors[] = 'Tên tỉnh/TP không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên tỉnh/TP tối đa 255 ký tự';
            }

            if ($licensePlate === '') {
                $errors[] = 'Biển số xe không được để trống';
            } elseif (mb_strlen($licensePlate) > 255) {
                $errors[] = 'Biển số xe tối đa 255 ký tự';
            }

            $nationId = null;
            if ($nationCode === '') {
                $errors[] = 'Mã quốc gia không được để trống';
            } elseif (!isset($nations[$nationCode])) {
                $errors[] = "Không tìm thấy quốc gia: {$nationCode}";
            } else {
                $nationId = $nations[$nationCode]['id'];
            }

            if ($areaName === '') {
                $errors[] = 'Tên khu vực không được để trống';
            } elseif ($nationId !== null && !isset($areas[$nationId . '|' . mb_strtolower($areaName)])) {
                $errors[] = "Không tìm thấy khu vực \"{$areaName}\" thuộc quốc gia {$nationCode}";
            }

            if ($name !== '' && $nationId !== null) {
                $key = $nationId . '|' . mb_strtolower($name);
                if (isset($seenInFile[$key])) {
                    $errors[] = "Tỉnh/TP bị trùng với dòng {$seenInFile[$key]} trong file";
                } else {
                    $seenInFile[$key] = $index + 2;
                }
                if (isset($existingNames[$key])) {
                    $errors[] = 'Tỉnh/TP này đã tồn tại trong quốc gia đã chọn';
                }
            }

            if ($code !== '' && mb_strlen($code) > 255) {
                $errors[] = 'Mã số tỉnh tối đa 255 ký tự';
            }
```

`«create»`:

```php
                $name = trim((string) ($item['name'] ?? ''));
                $nationCode = mb_strtoupper(trim((string) ($item['nation_code'] ?? '')));
                $areaName = trim((string) ($item['area_name'] ?? ''));

                $nation = $snapshot['nations'][$nationCode] ?? null;
                if (!$nation) {
                    throw new \Exception("Không tìm thấy quốc gia: {$nationCode}");
                }

                $areaId = $snapshot['areas'][$nation['id'] . '|' . mb_strtolower($areaName)] ?? null;
                if (!$areaId) {
                    throw new \Exception("Không tìm thấy khu vực \"{$areaName}\" thuộc quốc gia {$nationCode}");
                }

                $trung = Province::query()
                    ->where('nation_id', $nation['id'])
                    ->whereRaw('LOWER(TRIM(name)) = ?', [mb_strtolower($name)])
                    ->exists();
                if ($trung) {
                    throw new \Exception('Tỉnh/TP này đã tồn tại trong quốc gia đã chọn');
                }

                $this->createProvince([
                    'name' => $name,
                    'code' => trim((string) ($item['code'] ?? '')) ?: null,
                    'license_plate' => trim((string) ($item['license_plate'] ?? '')),
                    'nation_id' => $nation['id'],
                    'area_id' => $areaId,
                    'status' => Province::STATUS_ACTIVE,
                ]);
```

Giữ `$snapshot = $this->importSnapshot();`. Bỏ `$employeeId = ...`.

- [x] **Step 4: Chạy test, xác nhận PASS**

```bash
cd D:/CompanyProject/hrm/hrm-api && php vendor/bin/phpunit Modules/Human/Tests/Unit/ProvinceImportValidationTest.php
```

Expected: `OK (6 tests, ...)`.

- [x] **Step 5: Khuôn A vào `ProvinceController`** — `«payloadKey» = provinces`, `«serviceProp» = provinceService`
- [x] **Step 6: `status_text` vào `ProvinceListResource`**; kiểm resource có trả `nation_name` / `area_name` không, thiếu thì bổ sung
- [x] **Step 7: `export()` vào `ProvinceController`** — registry key `provinces`, tiêu đề `Danh mục tỉnh/thành phố`, file `danh_muc_tinh_thanh_pho.xlsx`
- [x] **Step 8: Bộ cột registry:**

```php
        'provinces' => [
            'name' => 'Tên tỉnh/TP',
            'code' => 'Mã số tỉnh',
            'license_plate' => 'Biển số xe',
            'nation_name' => 'Quốc gia',
            'area_name' => 'Khu vực',
            'status_text' => 'Trạng thái',
            'created_by_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updated_by_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [x] **Step 9: 3 route** trong nhóm `['prefix' => '/human/provinces']`, trước `Route::get('/{id}', ...)`
- [x] **Step 10: `php artisan route:list --path=human/provinces`**
- [x] **Step 11: FE** `hrm-client/pages/human/provinces/index.vue`

| Token | Giá trị |
| --- | --- |
| `«gate»` | để trống |
| `«modalId»` (import / export) | `import-province-modal` / `provinces-export-fields-modal` |
| `«nhãn»` | `tỉnh/TP` |
| `«apiPrefix»` | `human/provinces` |
| `«payloadKey»` | `provinces` |
| `«fileName»` (mẫu / xuất) | `Mau_import_tinh_thanh_pho.xlsx` / `danh_muc_tinh_thanh_pho.xlsx` |
| `«sheetName»` | `Tinh TP` |
| `«required»` | `['Name', 'LicensePlate', 'NationCode', 'AreaName']` |

```javascript
            return [
                {
                    key: 'Name',
                    label: 'Tên tỉnh/TP <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên tỉnh/TP', 'Ten tinh/TP', 'Tên tỉnh', 'Ten tinh'],
                    type: 'text',
                    placeholder: 'VD: Hải Phòng',
                    width: '240px',
                },
                {
                    key: 'Code',
                    label: 'Mã số tỉnh',
                    aliases: ['Mã số tỉnh', 'Ma so tinh', 'Mã số', 'Ma so'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 31',
                    width: '140px',
                },
                {
                    key: 'LicensePlate',
                    label: 'Biển số xe <span style="color: #dc2626;">*</span>',
                    aliases: ['Biển số xe', 'Bien so xe'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 15',
                    width: '140px',
                },
                {
                    key: 'NationCode',
                    label: 'Mã quốc gia <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã quốc gia', 'Ma quoc gia', 'Quốc gia', 'Quoc gia'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: VN',
                    width: '160px',
                },
                {
                    key: 'AreaName',
                    label: 'Tên khu vực <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên khu vực', 'Ten khu vuc', 'Khu vực', 'Khu vuc'],
                    type: 'text',
                    placeholder: 'VD: Miền Bắc',
                    width: '200px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                name: String(row.Name || '').trim(),
                code: String(row.Code || '').trim(),
                license_plate: String(row.LicensePlate || '').trim(),
                nation_code: String(row.NationCode || '').trim().toUpperCase(),
                area_name: String(row.AreaName || '').trim(),
            }
```

`exportFields()`: đúng 10 key của bộ cột registry ở Step 8, nhãn y hệt.

- [x] **Step 12: Nghiệm thu + ảnh, đóng browser.** Test thêm: dòng có khu vực **thuộc quốc gia khác** → phải báo lỗi
- [x] **Step 13: Báo user để commit**

---

**✅ XONG 11/09/2026.** Unit test `ProvinceImportValidationTest` — **9 test / 20 assertion, PASS**.

Validate qua API (5 dòng → **1 hợp lệ / 4 lỗi**):

| Dòng | Tình huống | Kết quả |
| --- | --- | --- |
| 2 | SG + khu vực `Peninsula` (đúng cặp) | hợp lệ |
| 3 | mã quốc gia `XX` | "Không tìm thấy quốc gia: XX" |
| 4 | khu vực `Riyadh` + quốc gia `SG` | "Không tìm thấy khu vực \"Riyadh\" thuộc quốc gia SG" |
| 5 | thiếu tên, `code=abc`, `license_plate=14A` | 3 lỗi: tên trống · "Mã số tỉnh phải là số" · "Biển số xe chỉ gồm chữ số" |
| 6 | trùng tên dòng 2 (khác hoa/thường) | "Tỉnh/TP bị trùng với dòng 2 trong file" |

Dòng 4 là ca đáng giá: `Riyadh` CÓ tồn tại nhưng thuộc quốc gia khác — khoá ghép
`nationId|tên khu vực` chặn đúng.

Import → `provinces` 45 → 46, bản ghi đủ `code/license_plate/nation_id/area_id/status/created_by`,
lịch sử `create`; **`nations` (36) và `areas` (22) giữ nguyên** → không đẻ danh mục cha.
Export: 46 dòng, 10 cột. UI đủ 3 nút, popup có "Trạng thái". Đã xoá dữ liệu thử.

📌 **Khoá chống trùng là (quốc gia + khu vực + tên)**, không phải (quốc gia + tên) như spec ghi ban
đầu — `CreateProvinceRequest.php:21-26` dùng `Rule::unique('provinces')->where(area_id, nation_id)`.
Có test riêng (`test_cung_ten_khac_khu_vuc_thi_hop_le`) khoá hành vi này.

📌 `createProvince()` **không tự gán `created_by`/`updated_by`** → `import()` set tay, nếu không cột
"Người tạo" trên danh sách và trong file xuất sẽ rỗng. (Dữ liệu cũ đang có 34/45 bản ghi `created_by`
NULL đúng vì lý do này.)

### Task 16: Phường/xã `/human/wards` — Import + **Export dựng ở FE**

⚠️ Bảng `wards` có **13.465 dòng** → Export màn này **KHÔNG** đi đường `DynamicExport` ở BE.
Không khai bộ cột trong `ExportColumnRegistry`, không thêm route `/export`.

- [x] **Step 1: Thêm 3 method vào `WardService`** (Khuôn B)

`«snapshot»`:

```php
        return [
            'provinces' => Province::query()
                ->get(['id', 'code', 'name'])
                ->mapWithKeys(function ($province) {
                    return [trim((string) $province->code) => ['id' => $province->id, 'name' => $province->name]];
                })
                ->toArray(),
            'codes' => Ward::query()
                ->pluck('id', 'code')
                ->mapWithKeys(function ($id, $code) {
                    return [trim((string) $code) => $id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $provinces = $snapshot['provinces'] ?? [];
            $existingCodes = $snapshot['codes'] ?? [];

            $name = trim((string) ($item['name'] ?? ''));
            $code = trim((string) ($item['code'] ?? ''));
            $provinceCode = trim((string) ($item['province_code'] ?? ''));

            if ($name === '') {
                $errors[] = 'Tên phường/xã không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên phường/xã tối đa 255 ký tự';
            }

            if ($code === '') {
                $errors[] = 'Mã số không được để trống';
            } elseif (mb_strlen($code) > 255) {
                $errors[] = 'Mã số tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$code])) {
                    $errors[] = "Mã số bị trùng với dòng {$seenInFile[$code]} trong file";
                } else {
                    $seenInFile[$code] = $index + 2;
                }
                if (isset($existingCodes[$code])) {
                    $errors[] = 'Mã số phường/xã đã tồn tại trong hệ thống';
                }
            }

            if ($provinceCode === '') {
                $errors[] = 'Mã số tỉnh không được để trống';
            } elseif (!isset($provinces[$provinceCode])) {
                $errors[] = "Không tìm thấy tỉnh/TP có mã số: {$provinceCode}";
            }
```

`«create»`:

```php
                $code = trim((string) ($item['code'] ?? ''));
                $provinceCode = trim((string) ($item['province_code'] ?? ''));

                if (Ward::query()->where('code', $code)->exists()) {
                    throw new \Exception('Mã số phường/xã đã tồn tại trong hệ thống');
                }

                $province = $snapshot['provinces'][$provinceCode] ?? null;
                if (!$province) {
                    throw new \Exception("Không tìm thấy tỉnh/TP có mã số: {$provinceCode}");
                }

                $this->createWards([
                    'name' => trim((string) ($item['name'] ?? '')),
                    'code' => $code,
                    'province_id' => $province['id'],
                    'status' => Ward::STATUS_ACTIVE,
                ]);
```

Giữ `$snapshot = $this->importSnapshot();`. Bỏ `$employeeId = ...`.

⚠️ `importSnapshot()` của màn này nạp 13.465 dòng `wards` — chấp nhận được vì chỉ `pluck` 2 cột,
nhưng **không** được `->get()` cả bản ghi.

- [x] **Step 2: `php -l Modules/Human/Services/WardService.php`**
- [x] **Step 3: Khuôn A vào `WardController`** — `«payloadKey» = wards`, `«serviceProp» = wardsService` (chú ý: property tên `wardsService`, có chữ "s")
- [x] **Step 4: 2 route Import** (KHÔNG có `/export`) trong nhóm `['prefix' => '/human/wards']`, trước `Route::get('/{id}', ...)`:

```php
        Route::post('/import/validate', [WardController::class, 'validateImport']);
        Route::post('/import', [WardController::class, 'import']);
```

- [x] **Step 5: `php artisan route:list --path=human/wards | grep import`**
- [x] **Step 6: FE Import** — Khuôn D vào `hrm-client/pages/human/wards/index.vue`

| Token | Giá trị |
| --- | --- |
| `«gate»` | để trống |
| `«modalId»` | `import-ward-modal` |
| `«nhãn»` | `phường/xã` |
| `«apiPrefix»` | `human/wards` |
| `«payloadKey»` | `wards` |
| `«fileName»` | `Mau_import_phuong_xa.xlsx` |
| `«sheetName»` | `Phuong xa` |
| `«required»` | `['Name', 'Code', 'ProvinceCode']` |

```javascript
            return [
                {
                    key: 'Name',
                    label: 'Tên phường/xã <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên phường/xã', 'Ten phuong/xa', 'Tên', 'Ten'],
                    type: 'text',
                    placeholder: 'VD: Phường Cửa Nam',
                    width: '280px',
                },
                {
                    key: 'Code',
                    label: 'Mã số <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã số', 'Ma so', 'Mã', 'Ma'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 00109',
                    width: '160px',
                },
                {
                    key: 'ProvinceCode',
                    label: 'Mã số tỉnh <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã số tỉnh', 'Ma so tinh', 'Tỉnh/TP', 'Tinh/TP'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 01',
                    width: '160px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                name: String(row.Name || '').trim(),
                code: String(row.Code || '').trim(),
                province_code: String(row.ProvinceCode || '').trim(),
            }
```

- [x] **Step 7: FE Export dựng bằng ExcelJS theo lô**

Không dùng Khuôn F. Thêm vào `pages/human/wards/index.vue`:

```javascript
        /**
         * Bảng `wards` có hơn 13.000 dòng — dựng file ở BE sẽ timeout trên server (đã dính ở màn
         * `customer-care/serials`). Nên lấy dữ liệu theo LÔ rồi dựng .xlsx ngay tại trình duyệt.
         */
        async runExport() {
            const ExcelJS = (await import('exceljs')).default
            const { saveAs } = await import('file-saver')

            try {
                this.exporting = true
                this.$nuxt.$loading.start()

                const rows = await this.fetchAllWards()

                const book = new ExcelJS.Workbook()
                const sheet = book.addWorksheet('Phuong xa')
                sheet.columns = [
                    { header: 'STT', key: 'stt', width: 8 },
                    { header: 'Tên phường/xã', key: 'name', width: 36 },
                    { header: 'Mã số', key: 'code', width: 14 },
                    { header: 'Tỉnh/TP', key: 'province_name', width: 28 },
                    { header: 'Trạng thái', key: 'status_text', width: 14 },
                    { header: 'Người tạo', key: 'created_by_name', width: 22 },
                    { header: 'Ngày tạo', key: 'created_at', width: 18 },
                ]
                sheet.getRow(1).font = { bold: true }
                sheet.getRow(1).alignment = { horizontal: 'center', vertical: 'middle', wrapText: true }

                rows.forEach((row, i) => {
                    sheet.addRow({
                        stt: i + 1,
                        name: row.name || '',
                        code: row.code || '',
                        province_name: row.province_name || '',
                        status_text: row.status_text || '',
                        created_by_name: row.created_by_name || '',
                        created_at: row.created_at || '',
                    })
                })

                const buffer = await book.xlsx.writeBuffer()
                // Cột "Mã số" là chuỗi toàn chữ số -> tắt cảnh báo "Number stored as text"
                const cleaned = await ignoreNumberStoredAsText(buffer, new Set([3]), 2, rows.length + 1)
                saveAs(new Blob([cleaned]), 'danh_muc_phuong_xa.xlsx')

                this.$toasted?.global?.success?.({ message: 'Xuất Excel thành công' })
            } catch (error) {
                console.error('Error exporting wards:', error)
                this.$toasted?.global?.error?.({ message: 'Lỗi khi xuất Excel' })
            } finally {
                this.exporting = false
                this.$nuxt.$loading.finish()
            }
        },

        /** Lấy toàn bộ phường/xã theo ĐÚNG bộ lọc đang áp, mỗi lượt 5.000 dòng. */
        async fetchAllWards() {
            const LO = 5000
            let page = 1
            let all = []

            for (;;) {
                const res = await this.$store.dispatch(
                    'apiGet',
                    `human/wards${buildQueryString({ ...this.buildParams({ page, per_page: LO }) })}`
                )
                const batch = res?.data || []
                all = all.concat(batch)

                if (batch.length < LO) break
                page += 1
            }

            return all
        },
```

Thêm import: `import { ignoreNumberStoredAsText } from '@/utils/export/excel-ignored-errors'` và
`import { buildQueryString } from '@/utils/url-action'`.

Nút "Xuất Excel" dùng Khuôn F2 nhưng `@click="runExport()"` gọi thẳng — **không** dùng
`exportFieldsMixin` / popup chọn cột ở màn này (bộ cột cố định, đường xuất khác hẳn). Thêm
`exporting: false` vào `data()`.

⚠️ Kiểm `this.buildParams` và tên action (`apiGet` vs `apiGetMethod`) đúng như `loadData()` của màn
đang dùng; kiểm `res.data` là mảng dòng hay còn bọc thêm tầng.

- [x] **Step 8: Nghiệm thu + ảnh, đóng browser**

Ngoài 5 mục Import, phải đo: bấm Xuất Excel với bộ lọc rỗng → file tải về đủ 13.465 dòng, thời gian
chấp nhận được, mở file không có tam giác xanh ở cột Mã số. Ghi lại thời gian thực tế vào báo cáo.

- [x] **Step 9: Báo user để commit**

---

**✅ XONG 11/09/2026.** Import (BE) + Export dựng ở FE bằng ExcelJS theo lô.

- Validate (5 dòng → **1 hợp lệ / 4 lỗi**): trùng phường trong cùng tỉnh; "Không tìm thấy tỉnh/TP:
  …"; thiếu tên + `code=abc` ("Mã số phải là số"); trùng trong file.
- Import → `wards` 13.465 → 13.466, id cấp thủ công `max+1`, có lịch sử, `provinces` không đổi.
- **Export qua UI: tải về `danh_muc_phuong_xa.xlsx` đủ 13.465 dòng, 0,5 MB**, header
  `STT · Tên phường/xã · Tỉnh/TP · Quốc gia · Trạng thái · Người tạo · Ngày tạo · Người cập nhật ·
  Ngày cập nhật`. Đã xoá dữ liệu thử.

📌 **Tra tỉnh theo TÊN, không theo mã** (khác plan): 11/45 tỉnh trong DB chưa có `code` nên tra theo
mã sẽ không nhập được phường của những tỉnh đó. Đã kiểm tên tỉnh **duy nhất tuyệt đối** (0 trùng)
và đó cũng là thứ người dùng chọn ở màn Tạo mới. Cột "Mã số" của phường vẫn bắt buộc như
`CreateWardRequest` nhưng **KHÔNG unique** (8.940/13.465 bản ghi đang để trống).

📌 File xuất **không có cột "Mã số"**: bảng trên màn không hiển thị cột đó và `WardListResource`
cũng không trả — giữ nguyên tắc "file xuất khớp thứ người dùng đang nhìn".

🐞 **LỖI CÓ SẴN #1 — đã sửa:** màn Phường/xã **chưa bao giờ ghi được Lịch sử thay đổi**
(`catalog_histories` có 0 dòng cho `wards`). Cột `wards.id` KHÔNG có `AUTO_INCREMENT` nhưng model
khai `incrementing = true`, nên sau `create()` Laravel ghi đè id trong bộ nhớ bằng `lastInsertId()`
= **0**; `logCatalogCreate()` gặp `getKey()` = 0 là thoát sớm. Vá phòng thủ trong `createWards()`:
gán lại id vừa cấp khi `getKey()` rỗng. Ảnh hưởng cả đường tạo tay trên UI, không riêng import.

🐞 **LỖI CÓ SẴN #2 — đã sửa (user chọn hướng 2):** `WardListResource` gọi `Ward::canDelete()` cho
TỪNG dòng, mỗi dòng 1 query `employee_infos` → lấy cả bảng để xuất file thành ~13.500 query.
Gom lại **đúng 1 query cho cả trang** trong `WardListResource::wardIdsDangDuocSuDung()`.

| | Trước | Sau |
| --- | --- | --- |
| 1 lô 5.000 dòng | **23,3 s** | **3,0 s** |
| Cả lượt xuất (3 lô) | ~70 s | ~9 s |

Đã đối chiếu 200 phường/xã (gồm 50 phường đang được hồ sơ nhân sự dùng): **0 bản ghi lệch** kết quả
`can_delete` giữa cách cũ và cách mới. `Ward::canDelete()` giữ nguyên cho các nơi gọi khác.

⚠️ Ghi lại để khỏi tranh luận lại: **số dòng KHÔNG phải nguyên nhân chậm**. Truy vấn thuần join cả
13.468 dòng chỉ mất **0,02 s**; toàn bộ thời gian nằm ở N+1 kể trên. Trước khi kết luận "bảng to nên
phải xuất ở FE", hãy đo truy vấn thuần trước.

### Task 17: Ngân hàng `/human/banks` — Import + Export

**KHÔNG import logo** — màn Tạo mới có ô tải ảnh, file Excel không chở được.

- [x] **Step 1: Thêm 3 method vào `BankService`** (Khuôn B)

`«snapshot»`:

```php
        return [
            'codes' => Bank::query()
                ->pluck('id', 'code')
                ->mapWithKeys(function ($id, $code) {
                    return [mb_strtoupper(trim((string) $code)) => $id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $existingCodes = $snapshot['codes'] ?? [];

            $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));
            $name = trim((string) ($item['name'] ?? ''));
            $shortName = trim((string) ($item['short_name'] ?? ''));
            $intlName = trim((string) ($item['international_business_name'] ?? ''));
            $address = trim((string) ($item['business_address'] ?? ''));
            $statusText = trim((string) ($item['status'] ?? ''));

            if ($code === '') {
                $errors[] = 'Mã ngân hàng không được để trống';
            } elseif (mb_strlen($code) > 255) {
                $errors[] = 'Mã ngân hàng tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$code])) {
                    $errors[] = "Mã ngân hàng bị trùng với dòng {$seenInFile[$code]} trong file";
                } else {
                    $seenInFile[$code] = $index + 2;
                }
                if (isset($existingCodes[$code])) {
                    $errors[] = 'Mã ngân hàng đã tồn tại trong hệ thống';
                }
            }

            if ($name === '') {
                $errors[] = 'Tên ngân hàng không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên ngân hàng tối đa 255 ký tự';
            }

            if ($shortName === '') {
                $errors[] = 'Tên viết tắt không được để trống';
            } elseif (mb_strlen($shortName) > 255) {
                $errors[] = 'Tên viết tắt tối đa 255 ký tự';
            }

            if ($intlName !== '' && mb_strlen($intlName) > 255) {
                $errors[] = 'Tên giao dịch quốc tế tối đa 255 ký tự';
            }

            if ($address !== '' && mb_strlen($address) > 500) {
                $errors[] = 'Địa chỉ giao dịch tối đa 500 ký tự';
            }

            if ($statusText !== '' && $this->parseStatus($statusText) === null) {
                $errors[] = 'Trạng thái chỉ nhận "Hoạt động" hoặc "Khóa"';
            }
```

`«create»`:

```php
                $code = mb_strtoupper(trim((string) ($item['code'] ?? '')));

                if (Bank::query()->where('code', $code)->exists()) {
                    throw new \Exception('Mã ngân hàng đã tồn tại trong hệ thống');
                }

                $this->createBank([
                    'code' => $code,
                    'name' => trim((string) ($item['name'] ?? '')),
                    'short_name' => trim((string) ($item['short_name'] ?? '')),
                    'international_business_name' => trim((string) ($item['international_business_name'] ?? '')) ?: null,
                    'business_address' => trim((string) ($item['business_address'] ?? '')) ?: null,
                    'status' => $this->parseStatus((string) ($item['status'] ?? '')) ?? Bank::STATUS_ACTIVE,
                ]);
```

Bỏ `$employeeId = ...`. Thêm Khuôn C với `Bank::STATUS_ACTIVE` / `Bank::STATUS_INACTIVE`.

⚠️ `Bank` có `booted()` đọc `MasterSetting` (`use_crm`) — chạy import một lượt nhỏ trước để chắc
chắn hook đó không chặn tạo bản ghi.

- [x] **Step 2: `php -l Modules/Human/Services/BankService.php`**
- [x] **Step 3: Khuôn A vào `BankController`** — `«payloadKey» = banks`, `«serviceProp» = bankService`
- [x] **Step 4: `status_text` vào `BankListResource`**
- [x] **Step 5: `export()` vào `BankController`** — resource `BankListResource`, registry key `banks`, tiêu đề `Danh mục ngân hàng`, file `danh_muc_ngan_hang.xlsx`
- [x] **Step 6: Bộ cột registry:**

```php
        'banks' => [
            'code' => 'Mã ngân hàng',
            'name' => 'Tên ngân hàng',
            'short_name' => 'Tên viết tắt',
            'international_business_name' => 'Tên giao dịch quốc tế',
            'business_address' => 'Địa chỉ giao dịch',
            'status_text' => 'Trạng thái',
            'created_by_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updated_by_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [x] **Step 7: 3 route** trong nhóm `['prefix' => '/human/banks']`, TRƯỚC `Route::get('/{id}', ...)` **và trước** `Route::get('/bank-branches/{id}', ...)`:

```php
        Route::get('/export', [BankController::class, 'export']);
        Route::post('/import/validate', [BankController::class, 'validateImport']);
        Route::post('/import', [BankController::class, 'import']);
```

- [x] **Step 8: `php artisan route:list --path=human/banks`** — xác nhận 3 route mới không bị route nào nuốt
- [x] **Step 9: FE** `hrm-client/pages/human/banks/index.vue`

| Token | Giá trị |
| --- | --- |
| `«gate»` | để trống |
| `«modalId»` (import / export) | `import-bank-modal` / `banks-export-fields-modal` |
| `«nhãn»` | `ngân hàng` |
| `«apiPrefix»` | `human/banks` |
| `«payloadKey»` | `banks` |
| `«fileName»` (mẫu / xuất) | `Mau_import_ngan_hang.xlsx` / `danh_muc_ngan_hang.xlsx` |
| `«sheetName»` | `Ngan hang` |
| `«required»` | `['Code', 'Name', 'ShortName']` |

```javascript
            return [
                {
                    key: 'Code',
                    label: 'Mã ngân hàng <span style="color: #dc2626;">*</span>',
                    aliases: ['Mã ngân hàng', 'Ma ngan hang', 'Mã', 'Ma'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: VCB',
                    width: '160px',
                },
                {
                    key: 'Name',
                    label: 'Tên ngân hàng <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên ngân hàng', 'Ten ngan hang', 'Tên', 'Ten'],
                    type: 'text',
                    placeholder: 'VD: Ngân hàng TMCP Ngoại thương Việt Nam',
                    width: '340px',
                },
                {
                    key: 'ShortName',
                    label: 'Tên viết tắt <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên viết tắt', 'Ten viet tat'],
                    type: 'text',
                    placeholder: 'VD: Vietcombank',
                    width: '200px',
                },
                {
                    key: 'InternationalName',
                    label: 'Tên giao dịch quốc tế',
                    aliases: ['Tên giao dịch quốc tế', 'Ten giao dich quoc te'],
                    type: 'text',
                    placeholder: 'VD: JOINT STOCK COMMERCIAL BANK FOR FOREIGN TRADE OF VIETNAM',
                    width: '320px',
                },
                {
                    key: 'BusinessAddress',
                    label: 'Địa chỉ giao dịch',
                    aliases: ['Địa chỉ giao dịch', 'Dia chi giao dich'],
                    type: 'textarea',
                    rows: 2,
                    width: '300px',
                },
                {
                    key: 'Status',
                    label: 'Trạng thái',
                    aliases: ['Trạng thái', 'Trang thai'],
                    type: 'select',
                    options: [
                        { id: 'active', name: 'Hoạt động' },
                        { id: 'inactive', name: 'Khóa' },
                    ],
                    width: '140px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                code: String(row.Code || '').trim().toUpperCase(),
                name: String(row.Name || '').trim(),
                short_name: String(row.ShortName || '').trim(),
                international_business_name: String(row.InternationalName || '').trim(),
                business_address: String(row.BusinessAddress || '').trim(),
                status: String(row.Status || '').trim(),
            }
```

`exportFields()`: đúng 10 key của bộ cột registry ở Step 6.

- [x] **Step 10: Nghiệm thu + ảnh, đóng browser.** Kiểm thêm: bản ghi tạo bằng Import hiện đúng trên danh sách dù **không có logo**
- [x] **Step 11: Báo user để commit**

---

**✅ XONG 11/09/2026.** Import + Export màn Ngân hàng.

Validate (5 dòng → **1 hợp lệ / 4 lỗi**): trùng mã `MB`; trùng tên "Ngân hàng Thương mại Cổ phần
Quân đội"; dòng trống báo đủ 4 lỗi (mã, tên, tên viết tắt, trạng thái sai); dòng cuối báo **cả hai**
lỗi trùng mã + trùng tên trong file.

Import → `banks` 25 → 26, bản ghi đủ `code/name/short_name/international_business_name/
business_address/status`, **`logo` = NULL** (đúng thiết kế: file Excel không chở được ảnh), có lịch
sử `create`. Export qua UI: 26 dòng, khớp cột đã tick. Đã xoá dữ liệu thử.

⚠️ **Màn này khác 4 màn địa lý ở 3 điểm, đọc kỹ nếu sau này sửa:**

1. Thụt lề **4 space** (4 màn kia 2 space).
2. Key cột trên bảng dùng **camelCase** (`shortName`, `businessAddress`, `bankStatus`,
   `createdByName`, `updatedByName`…) trong khi key xuất file là snake_case → mixin không tự suy
   được cột nào, phải khai `exportFieldKeyMap` cho **cả 8 cột**, không chỉ mỗi cột trạng thái.
3. Tham số sắp xếp là **`sortBy` / `sortDesc`** (camelCase), không phải `sort_by` / `sort_desc`;
   phân trang vẫn là `limit`.

📌 Cột "Người cập nhật" trong bộ xuất dùng key **`updated_by`** (không phải `updated_by_name`) vì đó
đúng là thứ `BankListResource` trả ra — 4 màn địa lý thì ngược lại.

### Checkpoint Phase 3

Báo user: 5 màn Nhân sự đã có Import; 4 màn có Export qua BE, màn Phường/xã có Export dựng ở FE
kèm số liệu thời gian thực tế. Chờ duyệt rồi sang Phase 4.

---

## Phase 4 — CSKH (3 màn, chỉ thêm Import)

Ba màn này **đã có Export sẵn**, không đụng vào phần xuất file. Service của cả ba nhận `Request`
ở method tạo → `import()` phải dựng `new Request([...])`.

---

### Task 18: Import — Cấp dịch vụ bảo dưỡng `/customer-care/levels`

Bảng `levels` chỉ có 1 trường nhập: `name`.

**Files:** `Modules/CustomerCare/Services/LevelService.php`, `Modules/CustomerCare/Http/Controllers/V1/LevelController.php`,
`Modules/CustomerCare/Routes/api.php` (nhóm `/levels`, dòng ~30), `hrm-client/pages/customer-care/levels/index.vue`

**Interfaces:** Produces `LevelService::validateRows(array $items, array $snapshot): array`, `$snapshot = ['names' => array<string tên thường, int id>]`

- [x] **Step 1: Thêm 3 method vào `LevelService`** (Khuôn B)

`«snapshot»`:

```php
        return [
            'names' => Level::query()
                ->pluck('id', 'name')
                ->mapWithKeys(function ($id, $name) {
                    return [mb_strtolower(trim((string) $name)) => $id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $existingNames = $snapshot['names'] ?? [];

            $name = trim((string) ($item['name'] ?? ''));
            $key = mb_strtolower($name);

            if ($name === '') {
                $errors[] = 'Tên cấp không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên cấp tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$key])) {
                    $errors[] = "Tên cấp bị trùng với dòng {$seenInFile[$key]} trong file";
                } else {
                    $seenInFile[$key] = $index + 2;
                }
                if (isset($existingNames[$key])) {
                    $errors[] = 'Tên cấp đã tồn tại trong hệ thống';
                }
            }
```

`«create»`:

```php
                $name = trim((string) ($item['name'] ?? ''));

                $trung = Level::query()
                    ->whereRaw('LOWER(TRIM(name)) = ?', [mb_strtolower($name)])
                    ->exists();
                if ($trung) {
                    throw new \Exception('Tên cấp đã tồn tại trong hệ thống');
                }

                $this->store(new Request(['name' => $name]));
```

Bỏ `$employeeId = ...`. Không thêm Khuôn C. Kiểm `use Illuminate\Http\Request;` ở đầu file.

- [x] **Step 2: `php -l Modules/CustomerCare/Services/LevelService.php`**

- [x] **Step 3: Khuôn A vào `LevelController`** — `«payloadKey» = levels`, `«serviceProp» = levelService`

- [x] **Step 4: 2 route** trong nhóm `['prefix' => '/levels']`, ngay sau `Route::get('/export', ...)`:

```php
        Route::post('/import/validate', [LevelController::class, 'validateImport'])
            ->middleware('checkPermission:Quản lý cấp dịch vụ bảo dưỡng');
        Route::post('/import', [LevelController::class, 'import'])
            ->middleware('checkPermission:Quản lý cấp dịch vụ bảo dưỡng');
```

- [x] **Step 5: `php artisan route:list --path=customer-care/levels | grep import`**

- [x] **Step 6: Khuôn D vào `hrm-client/pages/customer-care/levels/index.vue`**

| Token | Giá trị |
| --- | --- |
| `«gate»` | `v-if="canManage"` (màn đã có `canManage`, xem `index.vue:229`) |
| `«modalId»` | `import-level-modal` |
| `«nhãn»` | `cấp dịch vụ bảo dưỡng` |
| `«apiPrefix»` | `customer-care/levels` |
| `«payloadKey»` | `levels` |
| `«fileName»` | `Mau_import_cap_dich_vu_bao_duong.xlsx` |
| `«sheetName»` | `Cap dich vu` |
| `«required»` | `['Name']` |

```javascript
            return [
                {
                    key: 'Name',
                    label: 'Tên cấp <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên cấp', 'Ten cap', 'Tên', 'Ten'],
                    type: 'text',
                    placeholder: 'VD: Cấp 1',
                    width: '360px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                name: String(row.Name || '').trim(),
            }
```

- [x] **Step 7: Nghiệm thu Playwright + ảnh, đóng browser**
- [x] **Step 8: Báo user để commit**

---

**✅ XONG 11/09/2026.** Validate 4 dòng → **1 hợp lệ / 3 lỗi** ("Tên cấp đã tồn tại trong hệ thống"
cho `Cấp 1 (6T)`; "không được để trống"; trùng trong file). Import → `levels` 29 → 30, có
`created_by`, lịch sử `create`. UI đủ 3 nút (Tạo mới · Xuất Excel · Import Excel). Đã xoá dữ liệu thử.

### Task 19: Import — Ghi chú kiểm tra bảo dưỡng `/customer-care/note-maintenances`

3 trường: Hạng mục (`name`), Ký hiệu (`key_name`), Mô tả (`description`). Chống trùng theo **Ký hiệu**.

- [x] **Step 1: Thêm 3 method vào `NoteMaintenanceService`** (Khuôn B)

`«snapshot»`:

```php
        return [
            'keyNames' => NoteMaintenance::query()
                ->pluck('id', 'key_name')
                ->mapWithKeys(function ($id, $keyName) {
                    return [mb_strtoupper(trim((string) $keyName)) => $id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $existingKeys = $snapshot['keyNames'] ?? [];

            $name = trim((string) ($item['name'] ?? ''));
            $keyName = mb_strtoupper(trim((string) ($item['key_name'] ?? '')));
            $description = trim((string) ($item['description'] ?? ''));

            if ($name === '') {
                $errors[] = 'Hạng mục không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Hạng mục tối đa 255 ký tự';
            }

            if ($keyName === '') {
                $errors[] = 'Ký hiệu không được để trống';
            } elseif (mb_strlen($keyName) > 255) {
                $errors[] = 'Ký hiệu tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$keyName])) {
                    $errors[] = "Ký hiệu bị trùng với dòng {$seenInFile[$keyName]} trong file";
                } else {
                    $seenInFile[$keyName] = $index + 2;
                }
                if (isset($existingKeys[$keyName])) {
                    $errors[] = 'Ký hiệu đã tồn tại trong hệ thống';
                }
            }

            if ($description !== '' && mb_strlen($description) > 500) {
                $errors[] = 'Mô tả tối đa 500 ký tự';
            }
```

`«create»`:

```php
                $keyName = mb_strtoupper(trim((string) ($item['key_name'] ?? '')));

                if (NoteMaintenance::query()->where('key_name', $keyName)->exists()) {
                    throw new \Exception('Ký hiệu đã tồn tại trong hệ thống');
                }

                $this->store(new Request([
                    'name' => trim((string) ($item['name'] ?? '')),
                    'key_name' => $keyName,
                    'description' => trim((string) ($item['description'] ?? '')) ?: null,
                ]));
```

Bỏ `$employeeId = ...`. Không thêm Khuôn C.

- [x] **Step 2: `php -l Modules/CustomerCare/Services/NoteMaintenanceService.php`**
- [x] **Step 3: Khuôn A vào `NoteMaintenanceController`** — `«payloadKey» = note_maintenances`, `«serviceProp» = noteMaintenanceService`
- [x] **Step 4: 2 route** trong nhóm `['prefix' => '/note-maintenances']`, ngay sau `Route::get('/export', ...)`:

```php
        Route::post('/import/validate', [NoteMaintenanceController::class, 'validateImport'])
            ->middleware('checkPermission:Quản lý ghi chú kiểm tra bảo dưỡng');
        Route::post('/import', [NoteMaintenanceController::class, 'import'])
            ->middleware('checkPermission:Quản lý ghi chú kiểm tra bảo dưỡng');
```

- [x] **Step 5: `php artisan route:list --path=customer-care/note-maintenances | grep import`**
- [x] **Step 6: Khuôn D vào `hrm-client/pages/customer-care/note-maintenances/index.vue`**

| Token | Giá trị |
| --- | --- |
| `«gate»` | `v-if="canManage"` |
| `«modalId»` | `import-note-maintenance-modal` |
| `«nhãn»` | `ghi chú kiểm tra bảo dưỡng` |
| `«apiPrefix»` | `customer-care/note-maintenances` |
| `«payloadKey»` | `note_maintenances` |
| `«fileName»` | `Mau_import_ghi_chu_kiem_tra_bao_duong.xlsx` |
| `«sheetName»` | `Ghi chu bao duong` |
| `«required»` | `['Name', 'KeyName']` |

```javascript
            return [
                {
                    key: 'Name',
                    label: 'Hạng mục <span style="color: #dc2626;">*</span>',
                    aliases: ['Hạng mục', 'Hang muc'],
                    type: 'text',
                    placeholder: 'VD: Kiểm tra dầu máy',
                    width: '300px',
                },
                {
                    key: 'KeyName',
                    label: 'Ký hiệu <span style="color: #dc2626;">*</span>',
                    aliases: ['Ký hiệu', 'Ky hieu'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: KTDM',
                    width: '160px',
                },
                {
                    key: 'Description',
                    label: 'Mô tả',
                    aliases: ['Mô tả', 'Mo ta'],
                    type: 'textarea',
                    rows: 2,
                    width: '320px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                name: String(row.Name || '').trim(),
                key_name: String(row.KeyName || '').trim().toUpperCase(),
                description: String(row.Description || '').trim(),
            }
```

- [x] **Step 7: Nghiệm thu + ảnh, đóng browser**
- [x] **Step 8: Báo user để commit**

---

**✅ XONG 11/09/2026.** Validate 5 dòng → **1 hợp lệ / 4 lỗi**, hai khoá chống trùng chạy độc lập:
trùng **Hạng mục**; trùng **Ký hiệu**; dòng trống báo cả hai lỗi "không được để trống"; dòng cuối
báo **đồng thời** "Hạng mục bị trùng với dòng 2 trong file" + "Ký hiệu bị trùng với dòng 2 trong file".

⚠️ **Không chạy được qua HTTP bằng tài khoản test** — trả 403 vì tài khoản chỉ có quyền
*Xem ghi chú kiểm tra bảo dưỡng*, không có *Quản lý…*. Đã chứng minh đây KHÔNG phải lỗi code:
route `POST /customer-care/note-maintenances` (store **có sẵn**, cùng quyền) cũng trả 403, trong khi
`index` và `export` (cho phép quyền *Xem*) trả 200. Nên đã kiểm logic bằng cách gọi thẳng
`NoteMaintenanceService::validateImportData()` — kết quả đúng như bảng trên.

✅ **Tiện thể nghiệm thu luôn mục #6 của spec §10** ("không đủ quyền thì ẨN nút"): mở màn này bằng
tài khoản chỉ có quyền Xem → trên thanh hành động **chỉ còn "Xuất Excel"**, cả "Tạo mới" lẫn
"Import Excel" đều bị ẩn. Đúng quyết định Q6.

### Task 20: Import — Dịch vụ sửa chữa và chi phí khác `/customer-care/costs`

Màn này có 2 điểm riêng, đọc kỹ trước khi code:

1. `CostService::store()` nhận tham số thứ hai `$kindOf`, mặc định `Cost::KIND_OF_SERVICE` — đúng
   giá trị `CostController::store()` đang dùng (`$this->costService->store($request)`), nên
   `import()` gọi `store(new Request([...]))` là khớp, **không** truyền `$kindOf` khác.
2. Cột **ĐM giảm giá (%)** KHÔNG nằm trong bảng `costs`. `store()` đọc key `discount` rồi
   `saveDiscount()` ghi sang bảng `company_costs` theo **công ty đang đăng nhập**. Giữ nguyên
   cách đó — chỉ cần truyền key `discount` vào `new Request([...])`.

- [x] **Step 1: Đọc lại 3 hàm liên quan trước khi viết**

```bash
cd D:/CompanyProject/hrm/hrm-api && sed -n '192,210p;307,341p;342,355p' Modules/CustomerCare/Services/CostService.php
```

Ghi lại đúng danh sách key mà `payload()` và `saveDiscount()` đọc từ `$request`:
`name`, `type`, `rate_value_capital`, `revenue_calculation`, `vat_percent`, `discount`.

- [x] **Step 2: Thêm 3 method vào `CostService`** (Khuôn B)

`«snapshot»`:

```php
        return [
            'names' => Cost::query()
                ->where('kind_of', Cost::KIND_OF_SERVICE)
                ->pluck('id', 'name')
                ->mapWithKeys(function ($id, $name) {
                    return [mb_strtolower(trim((string) $name)) => $id];
                })
                ->toArray(),
        ];
```

`«rules»`:

```php
            $existingNames = $snapshot['names'] ?? [];

            $name = trim((string) ($item['name'] ?? ''));
            $key = mb_strtolower($name);
            $rateCapital = trim((string) ($item['rate_value_capital'] ?? ''));
            $vat = trim((string) ($item['vat_percent'] ?? ''));
            $discount = trim((string) ($item['discount'] ?? ''));

            if ($name === '') {
                $errors[] = 'Tên dịch vụ / chi phí không được để trống';
            } elseif (mb_strlen($name) > 255) {
                $errors[] = 'Tên dịch vụ / chi phí tối đa 255 ký tự';
            } else {
                if (isset($seenInFile[$key])) {
                    $errors[] = "Tên dịch vụ / chi phí bị trùng với dòng {$seenInFile[$key]} trong file";
                } else {
                    $seenInFile[$key] = $index + 2;
                }
                if (isset($existingNames[$key])) {
                    $errors[] = 'Tên dịch vụ / chi phí đã tồn tại trong hệ thống';
                }
            }

            // 3 cột phần trăm: dấu phẩy là dấu THẬP PHÂN, không phải phân cách nghìn
            // (xem docblock `CostService::toNumber()`).
            foreach ([
                ['% Tính giá vốn', $rateCapital, true],
                ['% VAT', $vat, true],
                ['ĐM giảm giá (%)', $discount, false],
            ] as [$nhan, $giaTri, $batBuoc]) {
                if ($giaTri === '') {
                    if ($batBuoc) {
                        $errors[] = "{$nhan} không được để trống";
                    }
                    continue;
                }

                $so = str_replace(',', '.', $giaTri);
                if (!is_numeric($so)) {
                    $errors[] = "{$nhan} không hợp lệ";
                } elseif ((float) $so < 0 || (float) $so > 100) {
                    $errors[] = "{$nhan} phải nằm trong khoảng 0 - 100";
                }
            }
```

`«create»`:

```php
                $name = trim((string) ($item['name'] ?? ''));

                $trung = Cost::query()
                    ->where('kind_of', Cost::KIND_OF_SERVICE)
                    ->whereRaw('LOWER(TRIM(name)) = ?', [mb_strtolower($name)])
                    ->exists();
                if ($trung) {
                    throw new \Exception('Tên dịch vụ / chi phí đã tồn tại trong hệ thống');
                }

                $this->store(new Request([
                    'name' => $name,
                    'rate_value_capital' => trim((string) ($item['rate_value_capital'] ?? '')),
                    'vat_percent' => trim((string) ($item['vat_percent'] ?? '')),
                    'revenue_calculation' => (int) ($item['revenue_calculation'] ?? 0),
                    'discount' => trim((string) ($item['discount'] ?? '')) ?: null,
                ]));
```

Bỏ `$employeeId = ...`. Không thêm Khuôn C — `store()` luôn đặt `Cost::STATUS_ACTIVE`, nên file
mẫu **không có cột Trạng thái**.

- [x] **Step 3: `php -l Modules/CustomerCare/Services/CostService.php`**
- [x] **Step 4: Khuôn A vào `CostController`** — `«payloadKey» = costs`, `«serviceProp» = costService`
- [x] **Step 5: 2 route** trong nhóm `['prefix' => '/costs']`, ngay sau `Route::get('/export', ...)`:

```php
        Route::post('/import/validate', [CostController::class, 'validateImport'])
            ->middleware('checkPermission:Quản lý dịch vụ sửa chữa và chi phí khác');
        Route::post('/import', [CostController::class, 'import'])
            ->middleware('checkPermission:Quản lý dịch vụ sửa chữa và chi phí khác');
```

- [x] **Step 6: `php artisan route:list --path=customer-care/costs | grep import`**
- [x] **Step 7: Khuôn D vào `hrm-client/pages/customer-care/costs/index.vue`**

| Token | Giá trị |
| --- | --- |
| `«gate»` | `v-if="canManage"` |
| `«modalId»` | `import-cost-modal` |
| `«nhãn»` | `dịch vụ sửa chữa và chi phí khác` |
| `«apiPrefix»` | `customer-care/costs` |
| `«payloadKey»` | `costs` |
| `«fileName»` | `Mau_import_dich_vu_sua_chua.xlsx` |
| `«sheetName»` | `Dich vu chi phi` |
| `«required»` | `['Name', 'RateValueCapital', 'VatPercent']` |

```javascript
            return [
                {
                    key: 'Name',
                    label: 'Tên dịch vụ / chi phí <span style="color: #dc2626;">*</span>',
                    aliases: ['Tên dịch vụ / chi phí', 'Ten dich vu / chi phi', 'Tên dịch vụ', 'Ten dich vu'],
                    type: 'text',
                    placeholder: 'VD: Thay dầu máy',
                    width: '320px',
                },
                {
                    key: 'RateValueCapital',
                    label: '% Tính giá vốn <span style="color: #dc2626;">*</span>',
                    aliases: ['% Tính giá vốn', '% Tinh gia von', 'Tính giá vốn', 'Tinh gia von'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 70 (0 - 100)',
                    width: '180px',
                },
                {
                    key: 'VatPercent',
                    label: '% VAT <span style="color: #dc2626;">*</span>',
                    aliases: ['% VAT', 'VAT (%)', 'VAT'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 10 (0 - 100)',
                    width: '140px',
                },
                {
                    key: 'Discount',
                    label: 'ĐM giảm giá (%)',
                    aliases: ['ĐM giảm giá (%)', 'DM giam gia (%)', 'Định mức giảm giá', 'Dinh muc giam gia'],
                    type: 'text',
                    mono: true,
                    placeholder: 'VD: 5 (0 - 100)',
                    width: '180px',
                },
                {
                    key: 'RevenueCalculation',
                    label: 'Có tính doanh thu',
                    aliases: ['Có tính doanh thu', 'Co tinh doanh thu'],
                    type: 'select',
                    options: [
                        { id: '1', name: 'Có' },
                        { id: '0', name: 'Không' },
                    ],
                    width: '180px',
                },
            ]
```

`«mapRow»`:

```javascript
            return {
                name: String(row.Name || '').trim(),
                rate_value_capital: String(row.RateValueCapital || '').trim(),
                vat_percent: String(row.VatPercent || '').trim(),
                discount: String(row.Discount || '').trim(),
                // "Có" / "1" -> 1, còn lại -> 0
                revenue_calculation: ['có', 'co', '1', 'true'].includes(
                    String(row.RevenueCalculation || '').trim().toLowerCase()
                )
                    ? 1
                    : 0,
            }
```

- [x] **Step 8: Nghiệm thu + ảnh, đóng browser**

Ngoài 6 mục spec §10, kiểm thêm: dòng có **ĐM giảm giá** → sau import mở popup Sửa thấy đúng giá
trị giảm giá (tức `company_costs` đã được ghi), và dòng ghi `12,5` ở cột % ra **12,5** chứ không
phải 125.

- [x] **Step 9: Báo user để commit**

---

**✅ XONG 11/09/2026.** Validate 3 dòng → **1 hợp lệ / 2 lỗi** ("Tên dịch vụ / chi phí đã tồn tại
trong hệ thống"; "% Tính giá vốn không hợp lệ" + "% VAT phải nằm trong khoảng 0 - 100"). Dòng ghi
`12,5` ở cột phần trăm được hiểu đúng là **12,5** (không phải 125).

Import qua UI → `costs` +1 với `kind_of=2` (KIND_OF_SERVICE), `type=NULL`, `rate=65`, `vat=8`,
`revenue_calculation=1`, lịch sử `create`. **`company_costs` có 1 dòng `discount=3`** → xác nhận
ĐM giảm giá được `saveDiscount()` ghi sang bảng riêng đúng như màn Tạo mới. Đã xoá dữ liệu thử
(gồm cả dòng `company_costs`).

📌 Phạm vi chống trùng là nhóm **`type IS NULL`** (không phải `kind_of`) — đúng đính chính, bám
`Cost/CostRequest.php:43-45`.

### Checkpoint Phase 4 — kết thúc

Báo user: đủ 13 màn có Import, 9 màn có thêm Export. Cập nhật `.plans/gop-db/STATUS.md`: cắt entry
khỏi mục "Đang làm", chèn lên đầu mục "Hoàn thành".

---

## Phase 5 — Sửa lỗi phản hồi task Redmine #11160 (21/09/2026)

Nguồn: http://quanly.dnsmedia.vn/issues/11160 — ghi chú #4…#12 của QA.

### FE — khung dùng chung
- [x] `utils/import-helper.js` — `parseExcelFile` chỉ bỏ dòng 2 khi ĐÚNG là dòng gợi ý (`isHintRow`),
      hết lỗi nuốt dòng dữ liệu đầu tiên ở mọi màn để `skip-rows=1` (#7, #8, #12)
- [x] `utils/import-helper.js` — `buildHintRow()` tách riêng làm nguồn chung cho file mẫu + trình đọc
- [x] `utils/import-helper.js` — `buildImportTemplate()` chuyển sang **ExcelJS**, cột `type: 'select'`
      có **ô chọn giá trị thật** (data validation kiểu list, danh sách dài đẩy sang sheet ẩn `DanhMuc`)
- [x] 19 màn gọi `buildImportTemplate` đổi sang `await` (hàm nay bất đồng bộ)
- [x] `CatalogImportMixin` — import xong gọi `onMutated()` nếu màn có, để xoá cache dropdown địa danh

### FE/BE — sửa 5 màn đã có
- [x] Quốc gia: mã bưu chính chỉ nhận chữ số, tối đa 50 (`NationService` validate + import) (#4)
- [x] Khu vực: cột "Mã quốc gia" → **"Tên quốc gia"** dạng ô chọn; BE tra theo tên, vẫn đọc được
      file cũ ghi mã (#6)
- [x] Tỉnh/TP: như trên + cột "Tên khu vực" thành ô chọn (#5)
- [x] Phường/xã: cột Tỉnh/TP thành ô chọn
- [x] Ngân hàng: cột Trạng thái tự có ô chọn Hoạt động/Khóa nhờ khung mới (#12)

### BE+FE — 2 màn địa lý còn thiếu (#9)
- [x] Quận/Huyện: `DistrictService` thêm `exportRows/validateRows/import`, controller + 3 route,
      `ExportColumnRegistry['districts']`, FE thêm nút Xuất/Import + modal
- [x] Đường/Phố: `HamletService` tương tự (phường/xã tra theo cặp Tỉnh/TP + Phường/xã),
      `ExportColumnRegistry['hamlets']`, FE thêm nút Xuất/Import + modal

### Gọn giao diện popup import
- [x] `components/V2BaseImportToolbar.vue` — ẩn HẲN cả nhóm "Hiển thị" (nhãn + nút "Chỉ dòng lỗi"
      + chip "Dòng hợp lệ đang bị khoá") cho popup đỡ tốn diện tích. **Comment lại, KHÔNG xoá** —
      markup nhóm nằm trong 1 khối comment, CSS `.lock-pill` comment riêng ở khối style; bật lại
      thì bỏ comment ở 2 chỗ. Sự kiện `toggle-errors` / state `onlyErrors` bên `V2BaseImportModal`
      giữ nguyên nên không phải sửa gì thêm

- [x] Thu khoảng cách trong popup import (đo bằng Playwright, trước → sau):
      dải thông báo cách khối trên **24px → 12px**, cao **44px → 32px** (thêm `.import-inline-alert`
      padding `7px 12px` thay padding mặc định `.75rem 1.25rem` của Bootstrap) ·
      bảng preview `mt-3 → mt-2` (24px → 12px) · dòng thống kê trong toolbar `mt-2 → mt-1`
      (12px → 6px). Thân popup gọn bớt ~36px.

### Đồng bộ STYLE file mẫu import (21/09/2026)
Chuẩn lấy theo màn **Nhóm ngành** (`static/Mau_import_NhomNganh.xlsx`, dev-hrm/assign/industry-groups):
cột A = STT · hàng 1 header nền `#B8CCE4` đậm 12pt căn giữa wrap · hàng 2 dòng mô tả yêu cầu nhập
(cao 46,5) · hàng 3+ dòng ví dụ · toàn bộ ô viền mảnh.
- [x] `buildImportTemplate` (ExcelJS) dựng đúng khuôn trên -> **mọi màn dùng `V2BaseImportModal`
      đồng bộ theo, không phải sửa từng màn**
- [x] `buildHintRow()` sinh câu mô tả tự động: `(Bắt buộc, không được trùng)` · `Bắt buộc (chọn 01
      trong Hoạt động/ Khóa)` · `Text`; màn muốn câu riêng thì khai `col.hint`
- [x] Dòng ví dụ suy từ `col.sample` (mảng = nhiều dòng), không có thì lấy `placeholder` / option
      đầu; màn chưa khai `sample` chỉ sinh **1 dòng** (2 dòng suy tự động sẽ trùng mã nhau)
- [x] `isHintRow()` nhận dạng dòng mô tả theo ĐẶC TRƯNG (ngoặc đơn / "Bắt buộc" / "chọn 01 trong" /
      "Text" / "VD:") thay vì so khớp nguyên văn -> file mẫu cũ lẫn mới đều bỏ đúng 1 dòng
- [x] Màn **Phường/xã** khai `hint` + `sample` cụ thể làm mẫu đối chiếu cho user
- [x] Soi lại file chuẩn bằng openpyxl rồi khớp ĐÚNG từng thuộc tính (vòng sửa 2):
      font **Calibri 12** · hàng tiêu đề cao **15,5** (trước để 30 nên nhìn to hơn) và KHÔNG wrap,
      bù lại nới độ rộng cột theo độ dài tiêu đề · hàng mô tả **IN NGHIÊNG**, cao 46,5, wrap, căn
      giữa · viền **đen `FF000000`** (trước dùng xám xanh) · kẻ sẵn khung trống **tới hàng 17** ·
      tên sheet kiểu **`DM_phuongxa`** (bỏ dấu, bỏ khoảng trắng, tiền tố `DM_`)
- [x] Vòng sửa 3 — căn lề + độ rộng:
      · ⚠️ ExcelJS chỉ hiểu `vertical: 'middle'`, ghi `'center'` là thuộc tính **rơi mất im lặng**
        -> file ra không căn giữa theo chiều dọc như file chuẩn. Đã đổi.
      · độ rộng cột bám dải chuẩn **20 - 34 ký tự** (trước để theo `width` px nên ra 40/24/37 —
        thừa một khoảng trắng bên phải), lấy `max(độ dài tiêu đề, độ dài dòng ví dụ)` rồi kẹp lại.
      · chiều cao hàng mô tả **tính theo số dòng chữ thực tế** thay vì cứng 46,5.
      · cột STT ở hàng mô tả bỏ `wrapText` cho khớp file chuẩn.

📌 Giống hệt màn Nhóm ngành: **dòng ví dụ nằm trong vùng dữ liệu**, người dùng phải xoá trước khi
nhập thật (tải mẫu lên nguyên trạng thì 2 dòng ví dụ được đọc thành dữ liệu).

### Đồng bộ XUẤT Excel màn Phường/xã (22/09/2026)
Màn này trước đây bấm Xuất là tải thẳng file cột cứng do trang tự dựng bằng ExcelJS — không có
popup chọn trường, không letterhead, không tiêu đề báo cáo, không khối ký tên.
- [x] BE: `ExportColumnRegistry['wards']` + `WardService::exportRows()` + `WardController::exportRows()`
      + route `GET human/wards/export-rows` (khuôn 14c, trần `limit` 5.000)
- [x] FE: thêm `exportFieldsMixin` + `ExportFieldsModal`, `runExport(type, fields)` gọi
      `exportListFile()`; gỡ `fetchAllWards()` + đoạn dựng file tự chế
- [x] Đồng bộ `utils/export/listExportFile.js` theo bản BE `DynamicExport`: tiêu đề **25pt**
      (trước 14), hàng tiêu đề cột **bỏ nền xám**, **cột STT căn giữa**, thêm **khối ký tên** cuối
      file → ảnh hưởng cả 9 màn đang dùng helper, nay giống hệt ~20 màn dùng DynamicExport
- [x] Đo thật: 13.465 dòng, tải theo lô 2.000 + dựng file ở trình duyệt ~15s, có dòng tiến độ

### Kiểm thử trên trình duyệt (Playwright MCP, 21/09/2026 — stack gop_db: client :3002, API :8003)
- [x] Khu vực · file 3 dòng KHÔNG có dòng gợi ý → bảng xem trước ra **đủ 3 dòng** (trước đây nuốt
      dòng 1), validate 3/3 hợp lệ, import xong cả 3 nằm trong danh sách
- [x] Khu vực · file CÓ dòng gợi ý + 2 dòng thật → ra đúng **2 dòng** (bỏ đúng dòng gợi ý)
- [x] Quốc gia · mã bưu chính `ABC-123` → báo "Mã bưu chính chỉ được nhập chữ số"; `100000` hợp lệ
- [x] Quận/Huyện · Xuất Excel ra 738 dòng đúng cột; import 2 dòng → 1 hợp lệ, 1 báo
      "Không tìm thấy tỉnh/TP: Tỉnh Không Có Thật"; import xong có Người tạo / Ngày tạo
- [x] File mẫu Khu vực / Tỉnh-TP / Đường-Phố / Ngân hàng đều mở được bằng openpyxl và có **ô chọn
      giá trị thật**; danh sách dài (45 tỉnh) nằm ở sheet ẩn `DanhMuc`
- [x] Đã xoá sạch dữ liệu thử (3 khu vực, 1 quận/huyện + lịch sử tương ứng)

**2 lỗi phát hiện nhờ lượt test này, đã sửa:**
1. `errorStyle: 'error'` sai chuẩn OOXML (chỉ nhận `stop`/`warning`/`information`) → file mẫu bị
   openpyxl từ chối, Excel đòi "repair". Đổi thành `'stop'`.
2. Gán data validation từng ô làm ExcelJS sinh 2 vùng CHỒNG NHAU (`F3:F502` + `F10:F502`) → chuyển
   sang `sheet.dataValidations.add(range, …)`, còn đúng 1 vùng.

### Kiểm thử
- [x] `Modules/Human/Tests/Unit/CatalogImportFixesTest.php` — 5 test: mã bưu chính chỉ chữ số ·
      khu vực/tỉnh tra quốc gia theo tên (và vẫn đọc file cũ ghi mã) · quận huyện · đường phố
- [x] `ProvinceImportValidationTest` cũ vẫn xanh (9/9) — đường tra theo MÃ không vỡ

### ⏸ HOÃN — 2 màn CSKH có bảng con (#11)
**Chốt với user 21/09/2026: để sau, lần này chỉ xử lý danh mục PHẲNG.**
- [ ] Gói bảo dưỡng (`customer-care/services`) — vướng: bắt buộc file PDF đính kèm (Excel không
      chở được) + bảng hạng mục bảo dưỡng theo cấp dịch vụ
- [ ] Công việc, lỗi thiết bị (`customer-care/device-errors`) — vướng: bắt buộc danh sách hàng hoá,
      hàng thay thế, bảng dịch vụ sửa chữa kèm giá vốn/giá dịch vụ

Làm 2 màn này cần: trình đọc Excel nhiều sheet + `V2BaseImportModal` nhận sheet con (đã dựng thử
rồi gỡ bỏ trong session 21/09 để giữ diff sạch).

---

## Self-review của plan (đã chạy khi viết)

| Mục kiểm | Kết quả |
| --- | --- |
| Spec §3.1 — 13 màn Import | Task 4-8 (5 Tài chính), 13-17 (5 Nhân sự), 18-20 (3 CSKH) = 13 ✓ |
| Spec §3.2 — 9 màn Export | Task 9-12 (4 Tài chính), 13-15 + 17 qua BE, 16 qua FE = 9 ✓ |
| Spec §5.2 `CatalogImportMixin` | Task 3 ✓ |
| Spec §5.3 `buildImportTemplate` | Task 2 ✓ |
| Spec §6 bộ cột 13 màn | Có đủ `«columns»` cụ thể ở từng task ✓ |
| Spec §7 bảng xử lý lỗi | Thể hiện trong `«rules»` từng task + Khuôn A (207 / 400) ✓ |
| Spec §8 vị trí + gate nút | Global Constraints + `«gate»` từng task ✓ |
| Spec §10 nghiệm thu | Step áp chót của mọi task ✓ |
| Chữ ký hàm nhất quán | `validateImportData(array): array`, `validateRows(array, array): array`, `import(array): array`, `importSnapshot(): array` — dùng đúng một bộ tên ở cả 13 task ✓ |
| Khoá `$snapshot` | Mỗi task khai rõ trong mục **Interfaces**; task nào dùng `$snapshot` trong `import()` đều giữ dòng `$snapshot = $this->importSnapshot();` ✓ |
| Không placeholder | Mọi token `«...»` đều có bảng giá trị đầy đủ trong chính task đó ✓ |

**Điểm còn phải xác minh lúc thi công** (đã cài thành step, không phải chỗ bỏ lửng):

- Ràng buộc `unique` thật của 13 bảng — Task 3 Step 7 (MySQL local đang tắt lúc viết plan).
- Key mà mỗi `Resource` trả ra so với bộ cột khai ở `ExportColumnRegistry` — step đầu của mọi task Export.
- Danh sách key mà các method tạo sẵn có đọc từ `$attrs` / `$request` — step đầu của Task 8, 13, 20.
- Tên bảng/cột chi nhánh ngân hàng (`bank_branches`) — Task 8 Step 2.
