# Phase 1 — Schema & Model: Báo cáo thực thi

**Ngày:** 2026-06-20  
**Status:** DONE

---

## Danh sách file đã tạo / sửa

### File MỚI (migration)

1. `ERP/TanPhatDev/database/migrations/2026_06_20_100001_add_child_columns_to_firm_quotation_tab_products.php`
   - Class: `AddChildColumnsToFirmQuotationTabProducts`
   - up(): thêm `child_parent_id` (unsignedBigInteger nullable) và `child_ratio` (integer nullable) vào bảng `firm_quotation_tab_products`
   - down(): dropColumn cả 2

2. `ERP/TanPhatDev/database/migrations/2026_06_20_100002_add_child_columns_to_firm_contract_tab_products.php`
   - Class: `AddChildColumnsToFirmContractTabProducts`
   - up(): thêm `child_parent_id` + `child_ratio` vào bảng `firm_contract_tab_products`
   - down(): dropColumn cả 2

3. `ERP/TanPhatDev/database/migrations/2026_06_20_100003_add_firm_contract_tab_product_id_to_export_request.php`
   - Class: `AddFirmContractTabProductIdToExportRequest`
   - up(): thêm `firm_contract_tab_product_id` (unsignedBigInteger nullable) vào bảng `product_export_request_tab_products`, đặt after `firm_contract_tab_id`
   - down(): dropColumn

### File ĐÃ SỬA (model)

4. `ERP/TanPhatDev/app/Model/Sale/Firm/Quotation/FirmQuotationTabProduct.php`
   - **$fillable**: thêm `'child_parent_id'`, `'child_ratio'` sau `'vat_percent'` (dòng 45–46)
   - **Relation children()**: `hasMany(self::class, 'child_parent_id', 'id')` — đặt trước `getProductAttribute()` (khoảng dòng 67)
   - **Relation childParent()**: `belongsTo(self::class, 'child_parent_id', 'id')` — đặt ngay sau `children()`

5. `ERP/TanPhatDev/app/Model/Sale/Firm/Contract/FirmContractTabProduct.php`
   - **$fillable**: thêm `'child_parent_id'`, `'child_ratio'` sau `'warehouse_exported_qty'` (dòng 66–67)
   - **Relation children()**: `hasMany(self::class, 'child_parent_id', 'id')` — đặt ngay sau `real_product()` relation (khoảng dòng 80)
   - **Relation childParent()**: `belongsTo(self::class, 'child_parent_id', 'id')` — đặt ngay sau `children()`

---

## Kết quả php -l

| File | Kết quả |
|------|---------|
| migration 100001 (firm_quotation_tab_products) | No syntax errors detected |
| migration 100002 (firm_contract_tab_products) | No syntax errors detected |
| migration 100003 (product_export_request_tab_products) | No syntax errors detected |
| FirmQuotationTabProduct.php | No syntax errors detected |
| FirmContractTabProduct.php | No syntax errors detected |

**Tất cả 5 file: PASS**

---

## Concerns / Ghi chú

- Tất cả cột mới đều `nullable()` — legacy-safe, không ảnh hưởng row hiện có.
- `child_parent_id` là self-reference FK trong cùng bảng — chưa tạo foreign key constraint (intentional: tránh issue khi migrate với data cũ, có thể thêm riêng sau nếu cần).
- Migration chưa được chạy (theo ràng buộc env local → DB production, cần deploy hoặc chạy trên server staging).
