# Phase 2 Report — Refactor attribution `exported_qty` sang `firm_contract_tab_product_id`

**Ngày:** 2026-06-20  
**STATUS: DONE_WITH_CONCERNS**

---

## 1. Kết quả truy vết `$p` (carry path)

### ProductExport.php — syncFirmContractTabProducts (type XUAT_BAN_HD_HANG)

| Trường hợp | `$tabs` từ | `$p` là model | Có `firm_contract_tab_product_id`? |
|---|---|---|---|
| `is_export_direct = true` | `$this->tabs` (ProductExportTab) | `ProductExportTabProduct` | **KHÔNG** |
| `is_export_direct = false` | `$this->warehouse_export->tabs` (WarehouseExportTab) | `WarehouseExportTabProduct` | **KHÔNG** |

**Kết luận:** `$p` trong `syncFirmContractTabProducts` KHÔNG bao giờ có `firm_contract_tab_product_id` trực tiếp. Cột này chỉ tồn tại trên `product_export_request_tab_products` (migration `2026_06_20_100003`).

### WarehouseExportRequest.php — block XUAT_BAN_HD_HANG (~dòng 940)

- `$this->tabs` → `WarehouseExportRequestTab` → `$p` là `WarehouseExportRequestTabProduct`  
- `WarehouseExportRequestTabProduct` **KHÔNG có** `firm_contract_tab_product_id`

---

## 2. Giải pháp thực tế (thay vì spec gốc)

Do `$p` không mang `firm_contract_tab_product_id`, cách carry là:  
1. Tìm `ProductExportRequestTabProduct` bằng khóa cũ `(product_export_request_id, firm_contract_id, firm_contract_tab_id, product_id, unit_id)`  
2. Nếu bản ghi tìm được có `firm_contract_tab_product_id` → dùng để lookup `FirmContractTabProduct` bằng `id`  
3. Nếu không → fallback lookup `FirmContractTabProduct` bằng khóa cũ `(firm_contract_id, parent_id, product_id, unit_id)`  
4. Bọc toàn bộ `save()` trong `if ($contract_product)` và `if ($productExportRequestTabProduct)` để không crash khi null

---

## 3. Chi tiết từng file đã sửa

### TASK 2.1 — `ProductExportRequestTab.php`

**File:** `app/Model/Warehouse/ProductExportRequestTab.php`  
**Dòng sửa:** ~23 (sau `firm_contract_tab_combo_product_id`)  
**Thay đổi:** Thêm 1 dòng:
```php
$p->firm_contract_tab_product_id = $pro['firm_contract_tab_product_id'] ?? null;
```

### TASK 2.2 + 2.3 — `ProductExport.php`

**File:** `app/Model/Warehouse/ProductExport.php`  
**Dòng sửa:** ~1675–1703 (block XUAT_BAN_HD_HANG trong `syncFirmContractTabProducts`)  

**Logic cũ (bị xóa):**
- Lookup `FirmContractTabProduct` bằng khóa cũ, gọi `save()` trực tiếp (không null-check → crash nếu không tìm được)
- Lookup `ProductExportRequestTabProduct` bằng khóa cũ, gọi `save()` trực tiếp (không null-check)

**Logic mới:**
1. Tìm `ProductExportRequestTabProduct` bằng khóa cũ (vì `$p` không có `firm_contract_tab_product_id`)
2. Nếu tìm được và có `firm_contract_tab_product_id` → lookup `FirmContractTabProduct` by `id`
3. Fallback: lookup `FirmContractTabProduct` by `(firm_contract_id, parent_id, product_id, unit_id)`
4. Bọc tất cả `save()` trong `if ($contract_product)` / `if ($productExportRequestTabProduct)`

### TASK 2.4 — `WarehouseExportRequest.php`

**File:** `app/Model/Warehouse/WarehouseExportRequest.php`  
**Dòng sửa (use statement):** ~8 (thêm `use App\Model\Warehouse\ProductExportRequestTabProduct;`)  
**Dòng sửa (logic):** ~940–958 (block XUAT_BAN_HD_HANG trong method `prepareExport` hoặc tương tự)  

**Logic mới:** Áp dụng đúng pattern như TASK 2.2 — lookup `ProductExportRequestTabProduct` by old key, dùng `firm_contract_tab_product_id` từ đó để tìm `FirmContractTabProduct` by id, fallback khóa cũ, bọc `if ($contract_product)`.

---

## 4. Kết quả `php -l`

```
No syntax errors detected in ProductExportRequestTab.php
No syntax errors detected in ProductExport.php
No syntax errors detected in WarehouseExportRequest.php
```

---

## 5. CONCERNS

### CONCERN 1 (QUAN TRỌNG): Carry path cho ProductExportTabProduct và WarehouseExportTabProduct chưa hoàn chỉnh

- `product_export_tab_products` và `warehouse_export_tab_products` KHÔNG có cột `firm_contract_tab_product_id` trong bất kỳ migration nào
- `ProductExportTab::syncTabProducts` và `WarehouseExportTab::syncTabProducts` KHÔNG carry `firm_contract_tab_product_id` khi tạo records
- **Hệ quả:** Phase 2 dùng cách "bridge lookup" (tìm ProductExportRequestTabProduct bằng khóa cũ, rồi dùng `firm_contract_tab_product_id` của nó để tìm FirmContractTabProduct)
- **Rủi ro:** Nếu HĐ cha-con có 2 dòng trùng `(product_id, unit_id)` trong cùng 1 tab, khóa cũ sẽ match sai bản ghi → cộng `exported_qty` vào sai dòng con

**Phương án khuyến nghị:** Phase 3 nên thêm `firm_contract_tab_product_id` vào `product_export_tab_products` và `warehouse_export_tab_products`, carry từ `ProductExportRequestTabProduct` khi tạo phiếu xuất, để có thể dùng id trực tiếp mà không cần bridge.

### CONCERN 2: Lookup `ProductExportRequestTabProduct` bằng khóa cũ vẫn là điểm yếu

Nếu 1 yêu cầu xuất có 2 dòng trùng `(firm_contract_id, firm_contract_tab_id, product_id, unit_id)` (trường hợp cha-con cùng sản phẩm, cùng đơn vị), `.first()` sẽ lấy bản ghi đầu tiên, dẫn đến cộng `exported_qty` không đúng dòng.

### CONCERN 3: `WarehouseExportRequest` thêm `use` cho lớp cùng namespace

`ProductExportRequestTabProduct` cùng namespace `App\Model\Warehouse` với `WarehouseExportRequest` — trong PHP không bắt buộc `use` cho cùng namespace, nhưng khai báo `use` tường minh là an toàn và rõ ràng hơn (không gây lỗi).
