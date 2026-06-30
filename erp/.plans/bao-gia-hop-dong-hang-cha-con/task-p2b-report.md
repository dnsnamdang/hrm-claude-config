# Task P2b Report — carry firm_contract_tab_product_id xuống phiếu xuất kho

## Mục tiêu
Carry `firm_contract_tab_product_id` xuyên xuống bảng phiếu xuất kho để attribution `exported_qty` chính xác tuyệt đối cho cha-con.

---

## TASK A — Migration thêm cột

**File tạo mới:**
`database/migrations/2026_06_20_100004_add_fctp_id_to_export_tab_products.php`

- Class: `AddFctpIdToExportTabProducts`
- up(): thêm `firm_contract_tab_product_id` (unsignedBigInteger, nullable) vào cả 2 bảng:
  - `product_export_tab_products` (after `firm_contract_tab_id`)
  - `warehouse_export_tab_products` (after `firm_contract_tab_id`)
- down(): dropColumn trên cả 2 bảng

php -l: **No syntax errors detected**

---

## TASK B — Lưu cột khi build phiếu xuất

**File sửa: `app/Model/Warehouse/ProductExportTab.php`**
- Dòng 26 (sau `$p->firm_contract_tab_id`): thêm `$p->firm_contract_tab_product_id = $pro['firm_contract_tab_product_id'] ?? null;`

**File sửa: `app/Model/Warehouse/WarehouseExportTab.php`**
- Dòng 27 (sau `$p->firm_contract_tab_id`): thêm `$p->firm_contract_tab_product_id = $pro['firm_contract_tab_product_id'] ?? null;`

php -l cả 2 file: **No syntax errors detected**

---

## TASK C — Ưu tiên $p->firm_contract_tab_product_id trong syncFirmContractTabProducts

**File sửa: `app/Model/Warehouse/ProductExport.php`**
- Vị trí: method `syncFirmContractTabProducts`, block xử lý XUAT_HANG_HD (~dòng 1689-1705)
- Thay thế logic cũ (Phase 2: chỉ dùng bridge `ProductExportRequestTabProduct`) bằng logic ưu tiên 3 cấp:

```php
$fctpId = !empty($p->firm_contract_tab_product_id)
    ? $p->firm_contract_tab_product_id                                // Priority 1: trực tiếp từ $p (Phase 2b)
    : ($productExportRequestTabProduct->firm_contract_tab_product_id ?? null); // Priority 2: qua bridge (Phase 2)

$contract_product = null;
if (!empty($fctpId)) {
    $contract_product = FirmContractTabProduct::query()->where('id', $fctpId)->first();
}
if (!$contract_product) { // Priority 3: legacy fallback (firm_contract_id + parent_id + product_id + unit_id)
    $contract_product = FirmContractTabProduct::query()->where([...])->first();
}
```

Đoạn cộng `exported_qty`/`warehouse_exported_qty`/`need_repair`/save và cập nhật `ProductExportRequestTabProduct` giữ nguyên.

php -l: **No syntax errors detected**

---

## Kết quả php -l

| File | Kết quả |
|------|---------|
| `database/migrations/2026_06_20_100004_add_fctp_id_to_export_tab_products.php` | No syntax errors detected |
| `app/Model/Warehouse/ProductExportTab.php` | No syntax errors detected |
| `app/Model/Warehouse/WarehouseExportTab.php` | No syntax errors detected |
| `app/Model/Warehouse/ProductExport.php` | No syntax errors detected |

---

## Concern

- Cột `firm_contract_tab_product_id` trên `product_export_tab_products` / `warehouse_export_tab_products` phụ thuộc FE truyền đúng giá trị này trong payload khi tạo phiếu xuất. Nếu FE chưa truyền → fallback về bridge Phase 2 → fallback legacy, hoạt động bình thường.
- `after('firm_contract_tab_id')` chỉ có tác dụng trên MySQL (column ordering); logic không phụ thuộc vị trí cột.
