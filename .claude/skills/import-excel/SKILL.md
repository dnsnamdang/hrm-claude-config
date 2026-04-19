---
name: import-excel
description: Xây dựng chức năng import Excel trong module Giao việc
---

# Skill: Import Excel trong module Giao việc

## Tổng quan
Import Excel sử dụng quy trình 4 bước qua component `V2BaseImportModal`:
1. Chọn file (.xlsx, .xls)
2. Preview dữ liệu (bảng)
3. Validate (gọi API BE)
4. Import (gọi API BE, chỉ dòng hợp lệ)

## Component chính

### FE: V2BaseImportModal
- Path: `hrm-client/components/V2BaseImportModal.vue`
- Dùng lại cho mọi chức năng import — không code lại UI

### Props cần truyền
```vue
<V2BaseImportModal
    ref="importModal"
    modal-id="import-[feature]-modal"
    title="Import [tên]"
    subtitle="Import từ Excel • Validate xong dòng hợp lệ sẽ bị khoá"
    :columns="importColumns"
    :required-fields="importRequiredFields"
    :validation-rules="importValidationRules"
    template-file-name="Mau_import_xxx.xlsx"
    :existing-data="[]"
    existing-data-key="code"
    :skip-rows="0"
    @validate-data="handleValidateData"
    @import-data="handleImportData"
    @download-template="handleDownloadTemplate"
/>
```

### Cấu hình columns
```javascript
importColumns() {
    return [
        {
            key: 'Name',              // Key dùng trong code
            label: 'Tên hàng hoá',    // Hiện trên bảng preview (hỗ trợ HTML: <span style="color: #dc2626;">*</span>)
            aliases: ['Tên hàng hoá', 'Ten hang hoa'],  // Các biến thể header Excel
            type: 'text',             // 'text' | 'textarea'
            width: '280px',           // Độ rộng cột preview
            mono: false,              // Font monospace
            rows: 2,                  // Chỉ dùng cho type: 'textarea'
        },
    ]
}
```

### skipRows
- `skipRows=0`: Data bắt đầu ngay sau header row (row 2 trở đi)
- `skipRows=1`: Skip 1 dòng sau header (dùng khi có dòng mô tả)
- **Lưu ý**: Parser luôn lấy row đầu tiên làm header. `skipRows` là số dòng skip **sau header**

### Import helper
- Path: `hrm-client/utils/import-helper.js`
- Function: `parseExcelFile(file, columns, skipRows)`
- Parse bằng thư viện XLSX
- Map columns qua: label → key → aliases (case-insensitive, bỏ dấu, bỏ khoảng trắng)
- Mỗi row có metadata: `__row`, `__validated`, `__isValid`, `__errors`, `__dirty`

## Events flow

### 1. validate-data
- V2BaseImportModal emit `validate-data` với array rows (raw data, key = column.key)
- Parent component:
  1. Map data sang format BE (snake_case)
  2. POST tới API validate
  3. Nhận response có `rows[].isValid`, `rows[].errors`
  4. Update modal state trực tiếp qua `$refs.importModal`:
```javascript
const modal = this.$refs.importModal
modal.importRows = validatedRows       // Gắn __validated, __isValid, __errors
modal.importValidatedRows = validatedRows
modal.importValidCount = data.validCount
modal.importInvalidCount = data.invalidCount
modal.currentStep = 3                  // Chuyển sang step 3
```

### 2. import-data
- V2BaseImportModal **đã filter chỉ valid rows** trước khi emit
- Data emit ra **KHÔNG có** `__isValid` — không filter lại trong handler
- Parent component:
  1. Map data sang format BE
  2. POST tới API import
  3. Xử lý response (success/partial/error)
  4. Hide modal + emit event reload data

### 3. download-template
- Parent component xử lý download (static file hoặc API)

## BE Pattern

### Controller structure
```php
// Validate endpoint
public function validateImport(Request $request, Model $model)
{
    $products = $request->input('products');
    if (!is_array($products) || empty($products)) {
        return $this->responseJson('Dữ liệu validate rỗng', Response::HTTP_BAD_REQUEST);
    }
    $result = $this->service->validateImportData($products);
    return $this->responseJson("Validate xong: ...", Response::HTTP_OK, $result);
}

// Import endpoint
public function import(Request $request, Model $model)
{
    $products = $request->input('products');
    if (!is_array($products) || empty($products)) {
        return $this->responseJson('Dữ liệu import rỗng', Response::HTTP_BAD_REQUEST);
    }
    // Validate lại server-side
    $validation = $this->service->validateImportData($products);
    $validProducts = array_filter(...);
    // Import trong transaction
    $result = DB::transaction(fn() => $this->service->importProducts($model, $validProducts));
    // Response: 200 = all success, 207 = partial
}
```

**Lưu ý quan trọng**: KHÔNG dùng `$request->validate()` vì nó throw `ValidationException` với message generic "The given data was invalid." — dùng check thủ công `if (!is_array(...))` thay thế.

### Service validate pattern
```php
public function validateImportData(array $products)
{
    $rows = [];
    foreach ($products as $index => $product) {
        $errors = [];
        // Validate từng field...
        $rows[] = [
            'index' => $index,
            'row' => $index + 2,
            'isValid' => count($errors) === 0,
            'errors' => $errors,
        ];
    }
    return ['rows' => $rows, 'total' => ..., 'validCount' => ..., 'invalidCount' => ...];
}
```

### Service import pattern
- Mỗi row wrap trong try-catch riêng → tiếp tục xử lý nếu 1 row lỗi
- Return: `{ total, success, failed, errors[] }`

### Lookup fields (model, brand, origin, unit...)
- Pattern: tìm theo tên (case-insensitive) → nếu chưa có → tạo mới
```php
private function resolveOrCreateLookup($type, $name)
{
    if (empty($name)) return null;
    $record = $modelClass::whereRaw('LOWER(name) = ?', [mb_strtolower($name)])->first();
    if ($record) return $record->id;
    $record = $modelClass::create(['name' => $name, 'status' => 1]);
    return $record->id;
}
```

### Phân biệt cha/con
- Qua cột STT: số nguyên = cha (`1`, `2`, `3`), có dấu chấm = con (`1.1`, `1.2`)
- Import theo thứ tự: cha trước → lưu ID → con tìm cha qua `parentMap[stt]`

## Routes
```php
Route::get('/import-template', [Controller::class, 'importTemplate']);  // ĐẶT TRƯỚC /{id}
Route::post('/{model}/import/validate', [Controller::class, 'validateImport']);
Route::post('/{model}/import', [Controller::class, 'import']);
```
**Lưu ý**: Route static (`/import-template`) phải đặt TRƯỚC route wildcard (`/{model}`) để tránh bị match sai.

## Template Excel mẫu
- Tạo qua API endpoint (PhpSpreadsheet Writer → response()->download()) thay vì static file
- Lý do: file static từ tinker/artisan có thể bị lỗi format
- Font: Times New Roman, có header style, có dòng mẫu cha + con

## Checklist khi tạo import mới
1. [ ] Tạo import columns config (key, label, aliases, type, width)
2. [ ] Xác định required fields
3. [ ] Viết FE validation rules (client-side)
4. [ ] Tạo BE validate endpoint + service method
5. [ ] Tạo BE import endpoint + service method
6. [ ] Tạo template download endpoint
7. [ ] Thêm routes (static trước wildcard)
8. [ ] Tích hợp V2BaseImportModal vào page/component
9. [ ] Test: upload → preview → validate → import → verify DB

## Phần khác nhau giữa các module

Khi implement import cho module mới, cần xác định:

| Thông tin | Ví dụ |
|---|---|
| Tên module | BomList, Payroll, Timesheet |
| Columns config | key, label, aliases, type, width |
| Required fields | ['Name', 'Code', ...] |
| skipRows | 0 hoặc 1 |
| Validation đặc thù BE | trùng mã, tồn tại FK, range số |
| Lookup fields cần resolve | model, brand, unit... |
| Có cấu trúc cha/con không | nếu có → dùng pattern STT |
| Template Excel | có dòng mẫu cha/con hay flat |

---

## Cách gọi skill này

Khi bắt đầu implement import cho module mới:
```
@.skills/import-excel/SKILL.md

Implement import excel cho module [TÊN MODULE].

Columns:
- [key]: [label] | aliases: [...] | required: true/false

Validation đặc thù:
- [ví dụ: mã không được trùng trong cùng BOM]

Có cấu trúc cha/con: có / không
Lookup fields: [danh sách nếu có]
File tham chiếu thêm: [nếu có module tương tự]
```

## File tham chiếu
- FE tham chiếu: `hrm-client/pages/assign/project_phase/index.vue` (import giai đoạn dự án)
- BE tham chiếu: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProjectPhaseController.php`
- BE service: `hrm-api/Modules/Assign/Services/ProjectPhaseService.php`
- Import helper: `hrm-client/utils/import-helper.js`
- Import error helper: `hrm-client/utils/import-error-helper.js`
- BOM import: `hrm-client/pages/assign/bom-list/components/BomBuilderImportModal.vue`
