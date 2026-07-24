# Task 1 Report — Helper format ngày (_CHU/_SO)

## STATUS: DONE

## File đã sửa
- `hrm-api/Modules/Human/Helper/Helper.php` — thêm 3 hàm static ngay sau `formatDateVILong` (trước `array_find_el`):
  - `formatDateVICapital($date)` — "Ngày 13 tháng 07 năm 2026" (HOA "Ngày", zero-pad d/m)
  - `formatDateVICapitalInline($date)` — "ngày 13 tháng 07 năm 2026" (thường)
  - `fillDateVariants(array &$result, string $baseName, $date, string $legacyFormat = 'so')` — gán gốc + `_CHU` + `_SO`

Không sửa file khác, không đổi hàm sẵn có, không commit/push.

## Verify

### 1. php -l
```
No syntax errors detected in Modules/Human/Helper/Helper.php
```

### 2. tinker
```
Ngày 13 tháng 07 năm 2026
13/07/2026
Array
(
    [NGAY_KY] => ngày 13 tháng 7 năm 2026
    [NGAY_KY_CHU] => Ngày 13 tháng 07 năm 2026
    [NGAY_KY_SO] => 13/07/2026
)
|
```

Đúng kỳ vọng: định dạng chữ HOA + zero-pad, số `13/07/2026`, mảng đủ 3 khóa (NGAY_KY dùng formatDateVILong khi legacyFormat='chu'), null → chuỗi rỗng (dòng cuối chỉ có `|`).
