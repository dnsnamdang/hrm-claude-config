# Task 5a Report — BE Tạo/Lưu phiếu YCCGKH

**Status:** DONE

**Commit hash (short):** `74d2cc05e8` (worktree branch `worktree-agent-af266e5279e77b640`, sẽ merge vào `task_10696`)

---

## Verify php -l

```
No syntax errors detected in app/Services/Sale/CustomerHandoverService.php
No syntax errors detected in app/Http/Requests/CustomerHandoverStoreRequest.php
No syntax errors detected in app/Http/Controllers/Sale/CustomerHandoverRequestController.php
```

---

## Files đã tạo/sửa

| File | Thao tác |
|---|---|
| `app/Services/Sale/CustomerHandoverService.php` | Tạo mới |
| `app/Http/Requests/CustomerHandoverStoreRequest.php` | Tạo mới |
| `app/Http/Controllers/Sale/CustomerHandoverRequestController.php` | Sửa — thêm 5 methods: `create`, `store`, `searchContract`, `searchCustomer`, `searchContact`; thêm `resolveContractable` helper; cập nhật imports |
| `resources/views/sale/customer_handover_requests/create.blade.php` | Tạo mới (placeholder, comment `{{-- 5b --}}`) |

---

## CustomerHandoverService

### `snapshotContractCustomer($contractable): array`

Phân biệt `FirmContract` vs `WrServiceContract`:

**FirmContract:**
- `customer_tax_code` → `null` (FirmContract không có cột tax_code trực tiếp)
- `customer_identity` → `identity_card_number`
- `grant_date/grant_location` → `identity_card_date` / `identity_card_place`
- `deputy_name/role` → `deputy_name` / `deputy_role`
- `account.id` → `customer_account_id`
- `account.number/name/bank_name/bank_branch/bank_province_id` → trực tiếp
- `contact` → `customer_contact_id`, `customer_contact_name`, `contact_address`, `customer_contact_phone`
- `delivery_place` → accessor (từ firm_quotation/parent_contract)
- `receiver_address` → `null`

**WrServiceContract:**
- `customer_tax_code` → `customer_tax_code`
- `customer_identity` → `customer_identity_card_number`
- `grant_date/grant_location` → `customer_grant_date` / `customer_grant_location`
- `deputy_name/role` → `customer_deputy_name` / `customer_deputy_role`
- `account.id` → `null` (không có customer_account_id)
- `account.bank_province_id` → `customer_bank_province` (tên cột khác so với FirmContract!)
- `contact.address` → `null` (không có)
- `contact.phone` → `customer_contact_phones` (plural)

### `logHistory($handover, $action, $note, $status): void`

Tạo `CustomerHandoverRequestHistory` với `created_by = auth()->id()`.

---

## store() — logic chính

1. Resolve contractable (FirmContract hoặc WrServiceContract) từ `contractable_type` + `contractable_id`
2. Snapshot `old_customer_data` từ HĐ
3. `is_send=1` → status `CHO_DUYET` + sinh `code`; `is_send=0` → status `DANG_TAO` + code null
4. Lưu `CustomerHandoverRequest`
5. Upload files lên S3 (`customer_handover_requests/`) → tạo `File` records với `fileable_id`/`fileable_type`
6. Nếu `is_send=1`: ghi lịch sử "gửi duyệt"
7. Rethrow `ValidationException`, catch `Exception` → rollback + log

---

## Concerns

### Lưu file — mirror được không?

**Có.** Pattern `fileable_id`/`fileable_type` mirror đúng `morphMany(File::class, 'fileable')` đã khai báo trong model `CustomerHandoverRequest`. Cách lưu (CmcS3Helper::putFile → File::create) nhất quán với `DeliveryCostSummaryController`.

### searchCustomer — mirror được logic báo giá không?

**Có một phần.** Method `searchCustomer` mirror `SearchController::searchCustomer` với đầy đủ các filter (customer_type, keyword, code, fullname, province_id, tax_code, phone cho cá nhân). Trả DataTables server-side — FE Task 5b cần dùng đúng các params này.

### searchContact — đơn giản hơn CustomersController?

`CustomersController::searchContact` search theo regex SĐT + cần `customer_id`. Method mới trong Task 5a search theo `customer_id` + `keyword` (tên/SĐT), trả JSON đơn giản (không DataTables) với `customer_contact_accounts`. Phù hợp hơn cho popup fill thông tin TK ngân hàng.

### Edge cases cần chú ý (Task 5b+)

1. `FirmContract.delivery_place` là accessor (không phải cột), luôn trả string — Task 5b FE cần display-only, không có ID.
2. `WrServiceContract.customer_bank_province` là tên cột (không phải `bank_province_id`) — khi áp dụng lên HĐ (Task 7) cần map đúng.
3. `FirmContract.identity_card_place` kiểu có thể là province_id (FK) — cần xác nhận khi Task 7 implement `applyToContract`.
4. Tiền điều kiện tạo phiếu (đã có YCCGKH, đã có đề nghị xuất HĐ, chỉ người tạo HĐ) chưa kiểm tra trong `store()` — cần thêm ở Task 5b sau khi FE có UI xác nhận.
