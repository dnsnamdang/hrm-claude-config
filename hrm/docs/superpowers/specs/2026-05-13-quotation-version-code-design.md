# Thêm solution_version_code & module_version_code vào bảng quotations

**Ngày:** 2026-05-13
**Module:** Assign (Giao việc)
**Người thực hiện:** @manhcuong

## Mục tiêu

Denormalize mã code phiên bản giải pháp (`solution_version_code`) và mã code phiên bản hạng mục (`module_version_code`) vào bảng `quotations` để hiển thị nhanh trên danh sách báo giá mà không cần join bảng `solution_versions` / `solution_module_versions`.

Pattern này đã được áp dụng cho bảng `tasks` (migration `2026_03_23_155715` và `2026_03_24_090200`).

## Hiện trạng

Bảng `quotations` đã có:
- `solution_version_id` (unsignedBigInteger) → FK tới `solution_versions`
- `solution_module_version_id` (unsignedBigInteger, nullable) → FK tới `solution_module_versions`

`DetailQuotationResource` đang join relationship để lấy code:
```php
'solution_version_code' => $this->solutionVersion
    ? Solution::formatVersionCode($this->solutionVersion->code) : null,
'solution_module_version_code' => $this->solutionModuleVersion
    ? Solution::formatVersionCode($this->solutionModuleVersion->code) : null,
```

`QuotationResource` (list) chưa trả version code → phải join nếu muốn hiển thị.

## Thay đổi

### 1. Migration

Thêm 2 cột vào bảng `quotations`:

| Cột | Kiểu | Nullable | Comment |
|-----|------|----------|---------|
| `solution_version_code` | string | yes | Mã phiên bản giải pháp |
| `module_version_code` | string | yes | Mã phiên bản hạng mục |

Đặt sau cột `solution_version_id` và `solution_module_version_id` tương ứng.

### 2. Seeder cập nhật data cũ

Logic:
- Join `quotations` với `solution_versions` theo `solution_version_id` → lấy `solution_versions.code` → format qua `Solution::formatVersionCode()` → update vào `quotations.solution_version_code`
- Join `quotations` với `solution_module_versions` theo `solution_module_version_id` → lấy `solution_module_versions.code` → format qua `Solution::formatVersionCode()` → update vào `quotations.module_version_code`
- Chạy chunk để tránh memory issue với data lớn

### 3. Model — `Quotation.php`

Thêm `solution_version_code`, `module_version_code` vào `$fillable`.

### 4. Service — `QuotationService.php`

**Trong `createFromRequest()`:** Khi tạo quotation từ PricingRequest, lấy code từ bảng version:
```php
// Lấy solution_version_code
$solutionVersionCode = null;
if ($locked->solution_version_id) {
    $sv = SolutionVersion::find($locked->solution_version_id);
    $solutionVersionCode = $sv ? Solution::formatVersionCode($sv->code) : null;
}

// Lấy module_version_code
$moduleVersionCode = null;
if ($locked->solution_module_version_id) {
    $smv = SolutionModuleVersion::find($locked->solution_module_version_id);
    $moduleVersionCode = $smv ? Solution::formatVersionCode($smv->code) : null;
}
```

Set vào quotation khi fill.

### 5. Transformer

**`QuotationResource.php` (list):** Thêm:
```php
'solution_version_code' => $this->solution_version_code,
'module_version_code' => $this->module_version_code,
```

**`DetailQuotationResource.php` (detail):** Đổi từ join relationship sang đọc trực tiếp từ cột:
```php
'solution_version_code' => $this->solution_version_code,
'solution_module_version_code' => $this->module_version_code,
```

## Không thay đổi

- Bảng con `quotation_product_prices`, `quotation_service_items` — không cần version code
- Logic update quotation — không cho phép đổi solution/version sau khi tạo
- Các bảng khác ngoài `quotations`

## Edge cases

- Quotation có `solution_version_id` nhưng bản ghi `solution_versions` đã bị xóa → seeder set `null`
- Quotation có `solution_module_version_id = null` → `module_version_code` = `null`
