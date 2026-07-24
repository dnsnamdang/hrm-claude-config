# Task 1 — Migrations 4 bảng · Báo cáo

**Người phụ trách:** @khoipv
**Ngày:** 2026-07-20
**Trạng thái:** DONE

## File đã tạo (4)

Đường dẫn: `D:\laragon\www\dns\hrm-thanhan-api\Modules\Supply\Database\Migrations\`

1. `2026_07_20_000001_create_purchase_contracts_table.php` — bảng cha (spec §2.1)
2. `2026_07_20_000002_create_purchase_contract_products_table.php` — dòng hàng (spec §2.2)
3. `2026_07_20_000003_create_purchase_contract_payment_terms_table.php` — điều khoản TT theo đơn (spec §2.3)
4. `2026_07_20_000004_create_purchase_contract_progress_table.php` — điều khoản TT theo đợt (spec §2.4)

## Xác nhận đủ cột theo spec

### 2.1 `purchase_contracts`
- Header: `id`, `code` (index), `number`, `name`, `type`
- Snapshot Bên A (Bên Mua): `main_company_id` (index) + `main_company_name/address/tax/phone/bank_no/bank_name/bank_branch/representative/title` (10 cột)
- Snapshot Bên B (NCC): `supplier_id` (index) + `supplier_code/name/address/tax/phone/bank_no/bank_name/bank_branch/representative/title/auth_doc` (12 cột)
- Thời gian: `sign_time`, `end_time`
- Giao nhận: `delivery_method`, `delivery_address`, `delivery_cost_payer`, `delivery_note`
- Điều khoản HĐ: `condition` (longText)
- Thanh toán: `payment_mode`, `payment_note`, `pay_days`, `pay_max_debt` (bigInteger), `pay_nt_text`
- Tổng & trạng thái: `total_amount` (bigInteger default 0), `status` (default 1), `reason_deny`, `sent_at`, `approved_by`, `approved_at`
- Audit: `created_by`, `updated_by`, `company_id`, `department_id`
- `timestamps()` + `softDeletes()`

### 2.2 `purchase_contract_products`
- `id`, `purchase_contract_id` (index), `product_id` (nullable, index)
- Snapshot hàng: `product_code`, `product_hh_code`, `product_name`, `product_trade_name`, `unit_id`, `unit_name`, `specification`, `producer_country`
- Số lượng/giá: `proposed_qty` decimal(15,3) nullable, `order_qty` decimal(15,3) default 0, `price` bigInteger default 0, `vat_percent` decimal(5,2), `amount` bigInteger default 0
- `purposes` json nullable, `note`, `sort_order`
- `timestamps()` (không softDeletes — đúng yêu cầu)

### 2.3 `purchase_contract_payment_terms`
- `id`, `purchase_contract_id` (index), `term_code` (string), `enabled` (bool default false), `max_days` (nullable), `max_value` (bigInteger nullable), `max_orders` (nullable)
- `timestamps()`

### 2.4 `purchase_contract_progress`
- `id`, `purchase_contract_id` (index), `label`, `pct` decimal(5,2), `time` date, `sort_order` default 0
- `timestamps()`

## Tuân thủ Global Constraints
- KHÔNG foreign key — chỉ `->index()` cho `code`, `main_company_id`, `supplier_id`, `purchase_contract_id`, `product_id`.
- Mọi cột có `->comment()` tiếng Việt.
- Bảng cha có `softDeletes()`; 3 bảng con chỉ `timestamps()`.
- Audit cols đủ 4 cột, nullable, có comment (theo khuôn `supply_handlings`).
- Kiểu cột đúng spec: qty = decimal(15,3), tiền = bigInteger, pct/vat = decimal(5,2), purposes = json.

## Kết quả `php -l`
Tất cả 4 file: **No syntax errors detected.**

## Concerns
- Audit cols và các cột id (`main_company_id`, `supplier_id`, `purchase_contract_id`, `product_id`) dùng `unsignedBigInteger` để đồng bộ với khuôn `supply_handlings` hiện có (spec ghi "integer" nhưng convention module dùng unsignedBigInteger — chọn theo convention module). Không ảnh hưởng logic vì BaseModel chỉ set giá trị int.
- Chưa chạy `php artisan migrate` (theo yêu cầu, để controller/DB dev quyết định sau).
