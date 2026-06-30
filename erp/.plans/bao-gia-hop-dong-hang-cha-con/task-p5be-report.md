# Phase 5 BE — Báo cáo thực thi

## STATUS: DONE — php -l sạch cả 3 file

---

## Task 5.1 — calcChildAwareRemaining + tích hợp vào service

**File:** `app/Services/Sale/Firm/Contract/FirmContractProductExportService.php`

### Method mới

```php
public function calcChildAwareRemaining($products)
```

- Đặt TRƯỚC `getDataProductExportAccounting` (khoảng dòng 397 sau khi thêm)
- Visibility: **public** (để Task 5.2 ở controller tái dùng không cần instantiate riêng)
- Legacy-safe: dòng không có con (`children->isEmpty()`) → `quantity - exported_qty` như cũ
- Công thức cha: `Q - a - max_i(delivered_i / r_i)`, con: `(Q * r_i) - delivered_i - r_i * a`; cả hai `max(0, ...)`

### Tích hợp trong `formatWarehouseExportData` (nhánh non-combo)

Vị trí: trước `$tabs = $tabs->toArray()` (sau khi `$tab_products` đã được build).

Thêm đoạn:
```php
$allContractProducts = FirmContractTabProduct::query()
    ->where('firm_contract_id', $contract->id)
    ->whereIn('parent_id', $tab_ids)
    ->get(['id', 'child_parent_id', 'child_ratio', 'quantity', 'exported_qty']);
$childAwareRemaining = $this->calcChildAwareRemaining($allContractProducts);
```

Thay tính `qty` từ:
```php
$product['quantity'] - $product['exported_qty'] - ($targetData['join_exporting_qty'] ?? 0)
```
thành:
```php
$baseRemaining = $childAwareRemaining[$product['id']] ?? max(0, $product['quantity'] - $product['exported_qty']);
max(0, $baseRemaining - $joinExportingQty)
```

Đồng thời thêm 2 field trả FE: `child_parent_id`, `child_ratio` (để FE biết cấu trúc cha-con).

**Nhánh combo (type=1):** KHÔNG thay đổi — combo dùng `FirmContractComboGroupOptionProduct`, không có quan hệ cha-con.

---

## Task 5.2 — Validate quỹ khi store yêu cầu xuất

**File:** `app/Http/Controllers/Warehouse/ProductExportRequestsController.php`

**Vị trí:** Chèn vào sau block `XUAT_BAN_HD_HANG || XUAT_BD_SC` (dòng ~613), trước `XUAT_DIEU_CHUYEN_KHO_CHI_NHANH` check, trước `DB::beginTransaction()`.

**Logic:**
1. Chỉ chạy khi `$request->type == XUAT_BAN_HD_HANG && $request->firm_contract_id` có giá trị
2. Load `FirmContractTabProduct` cho contract + tab_ids trong request
3. Gọi `calcChildAwareRemaining` (instantiate `FirmContractProductExportService`)
4. Gom `qty` yêu cầu theo `firm_contract_tab_product_id`
5. Với mỗi dòng: nếu qty > remaining → `throw ValidationException::withMessages(['tabs' => [...]])`

**Concern:** FE có thể không gửi `firm_contract_tab_product_id` trong `tabs.*.products.*` — hiện tại code bỏ qua (skip) những dòng thiếu field này và KHÔNG vỡ luồng. Cần kiểm tra FE gửi đủ `firm_contract_tab_product_id` để validate hoạt động đầy đủ.

**Note về ValidationException:** Throw ở ngoài `DB::beginTransaction()` nên tự nhiên propagate qua Laravel exception handler (trả 422 JSON). Không bị catch bởi `catch (Exception $e)` trong DB transaction block.

---

## Task 5.4 — Chặn giảm SL cha dưới mức đã xuất quy đổi

**File:** `app/Http/Controllers/Sale/Firm/FirmContractController.php`

**Vị trí:** Chèn vào trước `DB::beginTransaction()` trong method `update()` (dòng ~447 gốc).

**Logic:**
1. Load tất cả `FirmContractTabProduct` hiện tại (trước khi xóa-tái tạo) với `exported_qty`, `child_parent_id`, `child_ratio`
2. Build map `firm_quotation_tab_product_id → new quantity` từ `FirmQuotationTabProduct` (quotation product thực sự, không phải request)
3. Với mỗi dòng cha có con:
   - `Q_min = a + max_i(delivered_i / r_i)`
   - Nếu `Q_new < Q_min` → throw ValidationException
4. Check thêm từng con: `(Q_new * r_i) >= delivered_i + r_i * a`

**Note:** ValidationException throw trước `DB::beginTransaction()` → không bị `catch (Exception $e)` trong try block phía dưới.

---

## php -l

```
No syntax errors detected in app/Services/Sale/Firm/Contract/FirmContractProductExportService.php
No syntax errors detected in app/Http/Controllers/Warehouse/ProductExportRequestsController.php
No syntax errors detected in app/Http/Controllers/Sale/Firm/FirmContractController.php
```

---

## File list (đường dẫn tuyệt đối từ TanPhatDev/)

1. `app/Services/Sale/Firm/Contract/FirmContractProductExportService.php` — thêm `calcChildAwareRemaining()` + tích hợp vào `formatWarehouseExportData`
2. `app/Http/Controllers/Warehouse/ProductExportRequestsController.php` — thêm validate quỹ trước `DB::beginTransaction()`
3. `app/Http/Controllers/Sale/Firm/FirmContractController.php` — thêm validate giảm SL cha trước `DB::beginTransaction()`

---

## Concerns

1. **FE gửi `firm_contract_tab_product_id` không?** Hiện tại trong `tabs.*.products`, FE có thể không gửi `firm_contract_tab_product_id` (chỉ có trong response `getDataForWarehouseExport` sau Phase 5.1). Nếu FE chưa được cập nhật để gửi lại field này khi submit, validate Task 5.2 sẽ bỏ qua tất cả dòng → không có bảo vệ. Cần confirm FE phase 5 FE có gửi `firm_contract_tab_product_id` vào payload store.

2. **Nhánh combo:** Không bị ảnh hưởng — calcChildAwareRemaining chỉ được gọi trong nhánh non-combo (`type != 1`).

3. **`tab_ids` trong `formatWarehouseExportData`:** Khi `tab_ids` rỗng, `whereIn('parent_id', [])` trả collection rỗng → `calcChildAwareRemaining([])` trả `[]` → fallback về legacy. An toàn.
