---
name: import-excel
description: Xây dựng chức năng import Excel (V2BaseImportModal) + KHUÔN CHUẨN của file Excel mẫu dùng chung toàn hệ thống
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

            // --- 3 key dưới đây chỉ dùng cho FILE MẪU (xem mục "File Excel mẫu") ---
            hint: '(Bắt buộc, không được trùng)',   // Dòng mô tả (hàng 2). Không khai -> tự suy
            sample: ['Giá trị 1', 'Giá trị 2'],     // Dòng ví dụ (hàng 3, 4). Mảng = nhiều dòng
            unique: true,                           // Chỉ ảnh hưởng câu mô tả tự suy
        },
        {
            key: 'Status',
            label: 'Trạng thái',
            type: 'select',           // -> file mẫu có Ô CHỌN GIÁ TRỊ thật (data validation)
            options: [{ id: 'active', name: 'Hoạt động' }, { id: 'inactive', name: 'Khóa' }],
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

## File Excel mẫu — KHUÔN CHUẨN TOÀN HỆ THỐNG (chốt 21/09/2026)

> **Bản gốc của khuôn: `hrm-client/static/Mau_import_NhomNganh.xlsx`** (màn Nhóm ngành —
> `/assign/industry-groups`). Mọi file mẫu import phải ra ĐÚNG hình thức này, không mỗi màn một kiểu.

**KHÔNG tự dựng file mẫu, KHÔNG đặt file tĩnh mới trong `static/`.** Gọi hàm dùng chung:

```javascript
import { buildImportTemplate } from '@/utils/import-helper'

// ⚠️ HÀM BẤT ĐỒNG BỘ (nạp ExcelJS theo chunk) — thiếu `await` là không bắt được lỗi
async handleDownloadImportTemplate() {
    try {
        await buildImportTemplate(this.importColumns, {
            requiredFields: this.importRequiredFields,
            fileName: 'Mau_import_phuong_xa.xlsx',
            sheetName: 'Phuong xa',   // helper tự chuẩn hoá thành `DM_phuongxa`
        })
    } catch (error) {
        console.error('Error building import template:', error)
        this.$toasted?.global?.error?.({ message: 'Lỗi khi tạo file mẫu' })
    }
}
```

### Hình thức file sinh ra (đã đối chiếu từng ô với bản gốc)

| Thành phần | Quy cách |
| --- | --- |
| Tên sheet | `DM_<tên bỏ dấu, bỏ khoảng trắng>` — vd `DM_phuongxa` |
| Font toàn file | **Calibri 12** |
| Cột A | **STT**, rộng 8.4; dòng ví dụ đánh số 1, 2 |
| Hàng 1 — tiêu đề | in đậm, nền **`#B8CCE4`**, căn giữa cả 2 chiều, **KHÔNG wrap**, cao **15.5**; cột bắt buộc có hậu tố ` *` |
| Hàng 2 — mô tả | **IN NGHIÊNG**, căn giữa cả 2 chiều, **wrap**, cao = số dòng chữ thực tế × 15.5 |
| Hàng 3+ — ví dụ | chữ thường, không căn, cao 15.5 |
| Viền | `thin` màu **đen `FF000000`**, kẻ sẵn khung trống **tới hàng 17** |
| Độ rộng cột dữ liệu | `max(độ dài tiêu đề, độ dài dòng ví dụ)` kẹp trong **20 – 34** ký tự |
| Cột `type: 'select'` | có **ô chọn giá trị thật**; danh sách > 255 ký tự hoặc có dấu phẩy thì đẩy sang sheet ẩn `DanhMuc` rồi tham chiếu |

### Câu mô tả ở hàng 2
Không khai gì thì helper tự suy: `(Bắt buộc, không được trùng)` · `Bắt buộc (chọn 01 trong Hoạt
động/ Khóa)` · `Text`. Danh mục dài (> 6 lựa chọn) ghi `chọn 01 trong danh sách sổ xuống của ô`.
**Nên khai `hint` sát nghiệp vụ** cho màn quan trọng — xem `pages/human/wards/index.vue` làm mẫu.

### 5 cái bẫy đã trả giá — đừng dẫm lại

1. **`errorStyle` của data validation phải là `'stop'`.** Chuẩn OOXML chỉ nhận `stop | warning |
   information`; ExcelJS ghi thẳng giá trị vào XML nên để `'error'` là file sai chuẩn — openpyxl
   không mở được, Excel đòi "repair".
2. **Căn giữa dọc phải là `vertical: 'middle'`.** ExcelJS KHÔNG hiểu `'center'`, thuộc tính rơi mất
   im lặng, file ra nhìn lệch hẳn file chuẩn mà không báo lỗi gì.
3. **Gán data validation theo VÙNG** (`sheet.dataValidations.add(range, …)`). Gán từng ô thì
   ExcelJS gom thành nhiều vùng chồng nhau (`F3:F502` + `F10:F502`) → Excel coi là file cần sửa.
4. **Độ rộng cột KHÔNG lấy từ `width` px của bảng preview** (280px → 40 ký tự, thừa một mảng trắng).
   Tính theo nội dung rồi kẹp 20 – 34.
5. **Chiều cao hàng tiêu đề là 15.5, không phải 30.** Để cao hơn là nhìn "to" hơn file chuẩn ngay.

### Dòng mô tả và trình đọc
`parseExcelFile()` tự nhận ra hàng 2 là dòng mô tả và bỏ qua — nhận dạng theo ĐẶC TRƯNG (bọc ngoặc
đơn / chứa "Bắt buộc" / "chọn 01 trong" / "Text" / "VD:"), KHÔNG so khớp nguyên văn. Vì vậy:
- `:skip-rows="1"` nghĩa là **"được phép bỏ tối đa 1 dòng"**, chỉ bỏ khi đúng là dòng mô tả.
- File người dùng tự gõ (không có dòng mô tả) **không bị nuốt mất dòng đầu tiên** — lỗi Redmine
  #11160 mục 7, 8, 12 chính là chỗ này.

### Dòng ví dụ
Nằm TRONG vùng dữ liệu, giống hệt file mẫu gốc → người dùng phải xoá trước khi nhập thật. Màn nào
không khai `sample` thì helper chỉ sinh **1 dòng** (nhiều dòng suy tự động sẽ trùng mã nhau).

### Tự kiểm trước khi bàn giao
```bash
# Trong hrm-client: KHÔNG được còn màn nào tự dựng file mẫu bằng SheetJS hay tự tạo file tĩnh mới
grep -rn "XLSX.writeFile\|aoa_to_sheet" pages/ | grep -i "mau\|template"   # phải RỖNG
```
Mở file tải về bằng Excel thật: không có cảnh báo "repair", hàng 2 in nghiêng, cột `select` bấm ra
danh sách chọn.

## Checklist khi tạo import mới
1. [ ] Tạo import columns config (key, label, aliases, type, width)
2. [ ] Xác định required fields
3. [ ] Viết FE validation rules (client-side)
4. [ ] Tạo BE validate endpoint + service method
5. [ ] Tạo BE import endpoint + service method
6. [ ] File mẫu: gọi `buildImportTemplate()` (KHÔNG tự dựng, KHÔNG thêm file tĩnh) — xem mục
       "File Excel mẫu — KHUÔN CHUẨN TOÀN HỆ THỐNG"; khai `hint` / `sample` cho cột nghiệp vụ
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
- BOM import: `hrm-client/pages/assign/bom-list/components/BomImportModal.vue`
