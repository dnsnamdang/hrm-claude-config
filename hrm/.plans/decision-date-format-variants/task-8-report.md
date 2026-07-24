# Task 8 — Report: fillDateVariants cho 2 controller Decision

## Xác nhận key có dấu (dán chính xác từ file)
Key thực tế trong `TrainingContractController.php` là: `NGAY_KY_HDLĐ`
(chỉ ký tự CUỐI là `Đ` có dấu; chuỗi task gốc ghi `NGAY_KY_HĐLĐ` với 2 `Đ` là SAI — đã dùng đúng key gốc trong file: `H-D-L-Đ`).

## 1) TrainingContractController.php
- Mảng: `$result`
- Đã có sẵn `use Modules\Human\Helper\Helper;` (dòng 20) — không cần thêm.

| Biến | Trước | Sau |
|------|-------|-----|
| `NGAY_KY_HDLĐ` (line 96) | `$result['NGAY_KY_HDLĐ'] = $decision ? Carbon::parse($decision->effective_date)->format('d/m/Y') : '';` | `Helper::fillDateVariants($result, 'NGAY_KY_HDLĐ', $decision ? $decision->effective_date : null, 'so');` |
| `NGAY_SINH` (line 105) | `$result['NGAY_SINH'] = Carbon::parse($trainingContract->employee_info->birthday)->format('d/m/Y') ?? '';` | `Helper::fillDateVariants($result, 'NGAY_SINH', $trainingContract->employee_info->birthday, 'so');` |
| `NGAY_HIEU_LUC` (line 114) | `$result['NGAY_HIEU_LUC'] = Carbon::parse($trainingContract->assign_training->decision->effective_date)->format('d/m/Y') ?? '';` | `Helper::fillDateVariants($result, 'NGAY_HIEU_LUC', $trainingContract->assign_training->decision->effective_date, 'so');` |
| `NGAY_CAP_CCCD` (line 125) | `$result['NGAY_CAP_CCCD'] = Helper::formatDate($trainingContract->grant_date);` | `Helper::fillDateVariants($result, 'NGAY_CAP_CCCD', $trainingContract->grant_date, 'so');` |

- Nguồn thô lấy đúng biến trước `->format(...)`. `NGAY_KY_HDLĐ` giữ guard `$decision ? ... : null` để tránh lỗi null-object khi decision không tồn tại.
- KHÔNG đụng `THOI_GIAN_DAO_TAO` (chuỗi giờ from_time - to_time).

## 2) TroubleShootingReportController.php
- Mảng: `$result`
- Đã có sẵn `use Modules\Human\Helper\Helper;` (dòng 28) — không cần thêm.

| Biến | Trước | Sau |
|------|-------|-----|
| `NGAY_HOP` (line 219) | `$result['NGAY_HOP'] = Carbon::parse($troubleShootingReport->meeting_date)->format('d/m/Y');` | `Helper::fillDateVariants($result, 'NGAY_HOP', $troubleShootingReport->meeting_date, 'so');` |
| `NGAY_XAY_RA` (line 225) | `$result['NGAY_XAY_RA'] = Helper::formatDate($troubleShootingReport->incident_date);` | `Helper::fillDateVariants($result, 'NGAY_XAY_RA', $troubleShootingReport->incident_date, 'so');` |

## Verify (php -l)
```
No syntax errors detected in Modules/Decision/Http/Controllers/V1/TrainingContractController.php
No syntax errors detected in Modules/Decision/Http/Controllers/V1/TroubleShootingReportController.php
```

## Concern
- Nhánh `else` (không có laborContract) tại `TrainingContractController` vẫn giữ `$result['NGAY_KY_HDLĐ'] = '';` (không nằm trong 4 dòng task) → nhánh này KHÔNG sinh biến `_CHU`/`_SO`. Nếu template cần variant khi rỗng thì cần xử lý thêm; hiện `formatDate(null)` trả null nên clearNull sẽ dọn placeholder — chấp nhận được.
