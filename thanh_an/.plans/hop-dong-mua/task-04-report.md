# Task 4 — Report: Transformers Hợp đồng mua

**STATUS:** DONE

## File đã tạo

1. `hrm-thanhan-api/Modules/Supply/Transformers/PurchaseContract/PurchaseContractResource.php` (list)
2. `hrm-thanhan-api/Modules/Supply/Transformers/PurchaseContract/DetailPurchaseContractResource.php` (detail)

Namespace: `Modules\Supply\Transformers\PurchaseContract`, cả 2 extends `Modules\Human\Transformers\ApiResource`.

## Kết quả `php -l`

```
No syntax errors detected in .../PurchaseContract/PurchaseContractResource.php
-----
No syntax errors detected in .../PurchaseContract/DetailPurchaseContractResource.php
```

## Điểm đã làm đúng theo brief

- Map trạng thái/loại **thủ công** (không dùng `statusDisplay()` — entity không có method này):
  - `$status = collect(PurchaseContract::STATUSES)->firstWhere('id', $this->status);`
  - `status_color = $status['text_type'] ?? ''` (lấy từ key `text_type`, KHÔNG phải `color`).
- `is_can_edit / is_can_delete / is_can_approve`: dùng thẳng accessor entity, không tự tính lại điều kiện.
- Ngày (`created_at, sign_time, end_time, approved_at, sent_at`) qua `Helper::formatDate(...)`.
- `created_by_name = $this->employee_create_name`.
- `so_dong = $this->products_count ?? $this->products()->count()`.
- Detail trả đủ 3 mảng con `products / payment_terms / progress` với đúng tên cột đã kiểm chứng từ migration; `purposes` trả nguyên (đã cast array trong entity), `enabled` cast `(bool)`.
- Toàn bộ tên cột đã đối chiếu trực tiếp với 4 migration `2026_07_20_000001..000004`.

## Concern

Không có. Các trường hợp mảng con null được bảo vệ bằng `optional(...)->map(...) ?? []`.
