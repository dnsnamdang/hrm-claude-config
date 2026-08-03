# Task 3 — Report

## Mục tiêu
Thay 3 dòng gán biến ngày CHUNG trong `setValuePrintDecision` bằng `Helper::fillDateVariants`.

## File sửa
`hrm-api/Modules/Decision/Services/Decision/DecisionService.php` (dòng 476-478)

## Trước
```php
$result['NGAY_QUYET_DINH'] = Helper::formatDate($decision->effective_date);
$result['NGAY_KY'] = Helper::formatDateVILong($decision->signing_date);
$result['NGAY_HIEU_LUC'] = Helper::formatDateVILong($decision->effective_date);
```

## Sau
```php
Helper::fillDateVariants($result, 'NGAY_QUYET_DINH', $decision->effective_date, 'so');
Helper::fillDateVariants($result, 'NGAY_KY', $decision->signing_date, 'chu');
Helper::fillDateVariants($result, 'NGAY_HIEU_LUC', $decision->effective_date, 'chu');
```

## Ghi chú
- Tên biến nguồn đúng như dự kiến: `$decision->effective_date`, `$decision->signing_date`.
- legacyFormat giữ đúng: NGAY_QUYET_DINH='so', NGAY_KY='chu', NGAY_HIEU_LUC='chu'.
- `use Modules\Human\Helper\Helper;` đã có sẵn tại dòng 17 (không cần thêm).

## Verify
```
$ php -l Modules/Decision/Services/Decision/DecisionService.php
No syntax errors detected in Modules/Decision/Services/Decision/DecisionService.php
```
