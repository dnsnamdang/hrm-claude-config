# Task 4 — Transformers cho Hợp đồng mua

Bạn là implementer. Viết 2 Resource transformer cho tính năng "Hợp đồng mua" trong module Supply (Laravel 8, PHP 7.4). KHÔNG git commit. KHÔNG đọc vendor/. Trả lời tiếng Việt.

## Vị trí file (theo convention Supply — Transformers có subfolder theo entity)

- Tạo: `hrm-thanhan-api/Modules/Supply/Transformers/PurchaseContract/PurchaseContractResource.php`
- Tạo: `hrm-thanhan-api/Modules/Supply/Transformers/PurchaseContract/DetailPurchaseContractResource.php`

Namespace tương ứng: `Modules\Supply\Transformers\PurchaseContract`.

## Bắt buộc đọc trước khi code (đây là nguồn chân lý)

1. Mẫu list resource: `Modules/Supply/Transformers/SupplyHandling/SupplyHandlingResource.php`
2. Mẫu detail resource: `Modules/Supply/Transformers/SupplyHandling/DetailSupplyHandlingResource.php`
3. Entity: `Modules/Supply/Entities/PurchaseContract.php` (chú ý `const STATUSES` dùng key `text_type`, KHÔNG có `color`; có `TYPES`; accessor `is_can_edit/is_can_delete/is_can_approve`)
4. Entity con: `PurchaseContractProduct.php`, `PurchaseContractPaymentTerm.php`, `PurchaseContractProgress.php`
5. Migration cột thật: `Database/Migrations/2026_07_20_000001_create_purchase_contracts_table.php` (header + snapshot Bên A `main_company_*` + Bên B `supplier_*`), `..._000002_...products...`, `..._000003_...payment_terms...`, `..._000004_...progress...`

## Yêu cầu chung (khác với mẫu SupplyHandling)

- Cả 2 Resource extends `Modules\Human\Transformers\ApiResource` (giống mẫu).
- Dùng `Modules\Human\Helper\Helper::formatDate(...)` cho các cột ngày (created_at, sign_time, end_time, approved_at, sent_at).
- **QUAN TRỌNG — map trạng thái/loại thủ công** vì `PurchaseContract` KHÔNG có method `statusDisplay()`:
  ```php
  $status = collect(PurchaseContract::STATUSES)->firstWhere('id', $this->status);
  $type   = collect(PurchaseContract::TYPES)->firstWhere('id', $this->type);
  ```
  - `status_name` = `$status['name'] ?? ''`
  - `status_color` = `$status['text_type'] ?? ''`  ← lấy từ key `text_type`
  - `type_name` = `$type['name'] ?? ''`
- `is_can_edit / is_can_delete / is_can_approve`: dùng thẳng accessor entity (`$this->is_can_edit`, ...). KHÔNG tự tính lại điều kiện trong resource.
- `created_by_name` = `$this->employee_create_name` (accessor BaseModel dùng ở mẫu).

## PurchaseContractResource (list) — trả các field:

id, code, number, name, type, type_name, main_company_id, main_company_name, supplier_id, supplier_name, sign_time (formatDate), end_time (formatDate), total_amount, status, status_name, status_color, so_dong (= `$this->products_count ?? $this->products()->count()`), created_by_name, created_at (formatDate), is_can_edit, is_can_delete, is_can_approve.

## DetailPurchaseContractResource (detail) — trả đủ để dựng lại form:

- Toàn bộ field header: id, code, number, name, type, type_name.
- Snapshot Bên A (Bên Mua): main_company_id + main_company_name, main_company_address, main_company_tax, main_company_phone, main_company_bank_no, main_company_bank_name, main_company_bank_branch, main_company_representative, main_company_title.
- Snapshot Bên B (NCC): supplier_id + supplier_code, supplier_name, supplier_address, supplier_tax, supplier_phone, supplier_bank_no, supplier_bank_name, supplier_bank_branch, supplier_representative, supplier_title, supplier_auth_doc.
- Thời gian: sign_time, end_time (formatDate).
- Giao nhận: delivery_method, delivery_address, delivery_cost_payer, delivery_note.
- Điều khoản: condition (longText, trả nguyên).
- Thanh toán: payment_mode, payment_note, pay_days, pay_max_debt, pay_nt_text.
- Tổng/trạng thái: total_amount, status, status_name, status_color, reason_deny, sent_at (formatDate), approved_by, approved_at (formatDate).
- created_by_name, created_at (formatDate).
- `is_can_edit`, `is_can_delete`, `is_can_approve`.
- Mảng con:
  - `products` = `$this->products->map(...)` trả: id, product_id, product_code, product_hh_code, product_name, product_trade_name, unit_id, unit_name, specification, producer_country, proposed_qty, order_qty, price, vat_percent, amount, purposes (đã cast array trong entity — trả nguyên), note, sort_order.
  - `payment_terms` = `$this->paymentTerms->map(...)` trả: id, term_code, enabled (bool cast), max_days, max_value, max_orders.
  - `progress` = `$this->progress->map(...)` trả: id, label, pct, time, sort_order.
  - Với mọi mảng con: nếu quan hệ chưa load thì `$this->whenLoaded(...)` hoặc kiểm `relationLoaded`; nhưng đơn giản nhất là cứ `$this->products` (controller sẽ eager load). Dùng `optional()`/`?? []` để an toàn khi null.

## Verify (bắt buộc)

- Chạy `php -l` cho CẢ 2 file, dán output vào report.
- KHÔNG chạy migrate/test khác.

## Report

Ghi báo cáo đầy đủ vào file: `.plans/hop-dong-mua/task-04-report.md` (đường dẫn tuyệt đối: `D:\laragon\www\dns\.plans\hop-dong-mua\task-04-report.md`).
Trả về cho tôi: STATUS (DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT), danh sách file tạo, kết quả `php -l` từng file, và concern nếu có.
