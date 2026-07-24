# Task 5 Report — Thay dòng gán ngày bằng Helper::fillDateVariants

## STATUS: HOÀN THÀNH

Đã thay tất cả dòng gán ngày format INLINE ở 4 controller trong
`Modules/Decision/Http/Controllers/V1/` sang `Helper::fillDateVariants`.
Nguồn truyền vào là NGÀY THÔ (model attribute), không phải chuỗi đã format.

---

## 1) AcceptPersonnelController.php

- Thêm import: `use Modules\Human\Helper\Helper;` (sau `use Modules\Human\Entities\EmployeeInfo;`)

| Biến | Trước | Sau | Nguồn thô |
|------|-------|-----|-----------|
| THOI_GIAN_TIEP_NHAN_TU | `$result['THOI_GIAN_TIEP_NHAN_TU'] = $acceptPersonnel->enter_date ? Carbon::parse(...)->format('d/m/Y') : '';` | `Helper::fillDateVariants($result, 'THOI_GIAN_TIEP_NHAN_TU', $acceptPersonnel->enter_date, 'so');` | `$acceptPersonnel->enter_date` |
| THOI_GIAN_TIEP_NHAN_DEN | inline `->format('d/m/Y')` | `Helper::fillDateVariants($result, 'THOI_GIAN_TIEP_NHAN_DEN', $acceptPersonnel->enter_date_to, 'so');` | `$acceptPersonnel->enter_date_to` |
| NGAY_SINH | `($info && $info->birthday) ? Carbon::parse(...)` | `Helper::fillDateVariants($result, 'NGAY_SINH', $info ? $info->birthday : null, 'so');` | `$info->birthday` (guard null) |
| NGAY_CAP_CMTND | `($info && $info->grant_date) ? Carbon::parse(...)` | `Helper::fillDateVariants($result, 'NGAY_CAP_CMTND', $info ? $info->grant_date : null, 'so');` | `$info->grant_date` (guard null) |

`php -l`: No syntax errors detected

## 2) RenewLaborContractController.php

- Thêm import: `use Modules\Human\Helper\Helper;` (sau `use Modules\Human\Entities\EmployeeInfo;`)

| Biến | Sau | Nguồn thô |
|------|-----|-----------|
| THOI_GIAN_TIEP_NHAN_TU | `Helper::fillDateVariants($result, 'THOI_GIAN_TIEP_NHAN_TU', $renewLaborContract->renew_date_from, 'so');` | `$renewLaborContract->renew_date_from` |
| THOI_GIAN_TIEP_NHAN_DEN | `Helper::fillDateVariants($result, 'THOI_GIAN_TIEP_NHAN_DEN', $renewLaborContract->renew_date_to, 'so');` | `$renewLaborContract->renew_date_to` |
| NGAY_SINH | `Helper::fillDateVariants($result, 'NGAY_SINH', $info ? $info->birthday : null, 'so');` | `$info->birthday` (guard null) |
| NGAY_CAP_CMTND | `Helper::fillDateVariants($result, 'NGAY_CAP_CMTND', $info ? $info->grant_date : null, 'so');` | `$info->grant_date` (guard null) |

`php -l`: No syntax errors detected

## 3) SuspendLaborContractController.php — SỬA CẢ 2 KHỐI

- Thêm import: `use Modules\Human\Helper\Helper;` (sau `use Modules\Human\Entities\EmployeeInfo;`)
- Tên biến model GIỐNG NHAU ở cả 2 khối (`$suspendLaborContract->birthday`, `->suspend_date_start`, `->suspend_date_end`) → dùng replace_all.

**Khối 1 — `print()` (cũ dòng ~127, 130, 131):**
```php
Helper::fillDateVariants($result, 'NGAY_SINH', $suspendLaborContract->birthday, 'so');
Helper::fillDateVariants($result, 'THOI_GIAN_TAM_HOAN_TU', $suspendLaborContract->suspend_date_start, 'so');
Helper::fillDateVariants($result, 'THOI_GIAN_TAM_HOAN_DEN', $suspendLaborContract->suspend_date_end, 'so');
```

**Khối 2 — `printAgreement()` (cũ dòng ~175, 178, 179):**
```php
Helper::fillDateVariants($result, 'NGAY_SINH', $suspendLaborContract->birthday, 'so');
Helper::fillDateVariants($result, 'THOI_GIAN_TAM_HOAN_TU', $suspendLaborContract->suspend_date_start, 'so');
Helper::fillDateVariants($result, 'THOI_GIAN_TAM_HOAN_DEN', $suspendLaborContract->suspend_date_end, 'so');
```

Nguồn thô: `$suspendLaborContract->birthday`, `->suspend_date_start`, `->suspend_date_end`.
Trước: `Carbon::parse(...)->format('d/m/Y') ?? ''` inline ở cả 2 khối.

`php -l`: No syntax errors detected

## 4) TerminationLaborContractController.php

- `use Modules\Human\Helper\Helper;` ĐÃ CÓ SẴN (dòng 22) — không thêm.

| Dòng | Biến | Trước | Sau | legacyFormat |
|------|------|-------|-----|--------------|
| ~174 | THOI_GIAN_BD_CHAM_DUT_HDLD | `Helper::formatDateVILong($terminationLaborContract->termination_date_start)` | `Helper::fillDateVariants($result, 'THOI_GIAN_BD_CHAM_DUT_HDLD', $terminationLaborContract->termination_date_start, 'chu');` | **chu** |
| ~187 | NGAY_SINH | `($info && $info->birthday) ? Carbon::parse(...)->format('d/m/Y') : ''` | `Helper::fillDateVariants($result, 'NGAY_SINH', $info ? $info->birthday : null, 'so');` | **so** |

Xác nhận: dòng 174 = 'chu', dòng 187 = 'so'. Nguồn thô: `$terminationLaborContract->termination_date_start`, `$info->birthday`.

`php -l`: No syntax errors detected

---

## VERIFY (php -l 4 file)
```
No syntax errors detected in Modules/Decision/Http/Controllers/V1/AcceptPersonnelController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/RenewLaborContractController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/SuspendLaborContractController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/TerminationLaborContractController.php
```

## CONCERN
- Với các trường qua `$info` (birthday/grant_date của Accept/Renew/Termination), tôi giữ guard null bằng `$info ? $info->birthday : null` thay vì truyền thẳng `$info->birthday`, để tránh lỗi khi `$info` null (giữ nguyên hành vi guard của code cũ). Giả định `Helper::fillDateVariants` xử lý được null (trả chuỗi rỗng cho các biến variant) như bản Task 1.
- Đã bỏ toàn bộ format inline; `use Carbon\Carbon;` vẫn còn dùng ở các chỗ khác (toggleApprove...) nên không xóa import Carbon.
