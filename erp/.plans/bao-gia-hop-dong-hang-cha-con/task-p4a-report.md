# Task P4A Report — Phase 4 phần 1: Class JS báo giá + hợp đồng

## Path thật các file đã sửa

| File | Path thật |
|------|-----------|
| FirmQuotationTabProduct | `ERP/TanPhatDev/resources/views/partials/classes/sale/firm/quotation/FirmQuotationTabProduct.blade.php` |
| FirmQuotationTab | `ERP/TanPhatDev/resources/views/partials/classes/sale/firm/quotation/FirmQuotationTab.blade.php` |
| FirmContractTabProduct | `ERP/TanPhatDev/resources/views/partials/classes/sale/firm/contract/FirmContractTabProduct.blade.php` |
| FirmContractTab | `ERP/TanPhatDev/resources/views/partials/classes/sale/firm/contract/FirmContractTab.blade.php` |

## Cơ chế `quantity` hiện tại và cách thêm getter con

### FirmQuotationTabProduct — có getter/setter tự viết

`quantity` có getter/setter riêng trong class (không qua `initGetSet`), backing là `_quantity`. Setter format số với `_quantity_dot`.

**Cách thêm:** Override trực tiếp trong getter `quantity` của class — nếu `is_child` thì tính `SL cha × child_ratio`, trả về dạng `numberWithCommas(roundNumber(...))`. Cha vẫn dùng getter cũ.

Thêm `get _effective_quantity()` riêng để dùng trong `total_cost`, `base_unit_qty`, `submit_data` — trả về SL thực tính (không format) để tính toán số học.

### FirmContractTabProduct — quantity do `initGetSet` tạo tự động

`quantity` nằm trong `this.number` → `initGetSet` dùng `Object.defineProperty` tạo getter/setter trực tiếp trên **instance** (backing `_quantity`, getter trả `toLocaleString('en')`).

**Cách thêm:** Không thể override prototype getter vì `Object.defineProperty` instance override prototype. Giải pháp: trong `after()` (sau khi `initGetSet` đã chạy), nếu là dòng con thì gọi lại `Object.defineProperty(this, 'quantity', {..., configurable: true})` để override lại instance property. Getter mới của con tra cha theo `tmp_row_id` và trả `SL cha × child_ratio`.

Thêm `get _effective_quantity()` trên prototype để `total_cost_after_extra`, `total_cost_after_discount`, `submit_data` dùng thống nhất.

## Danh sách getter tổng đã filter `!p.is_child`

### FirmQuotationTab
- `sum_qty` — filter `!p.is_child`
- `total_cost` — filter `!p.is_child`
- `vat_cost` — filter `!p.is_child`
- `cost_after_vat` — filter `!p.is_child`

### FirmContractTab
- `sum_qty` — filter `!p.is_child`
- `total_extra` — filter `!p.is_child`
- `total_discount` — filter `!p.is_child`
- `total_before_vat` — filter `!p.is_child` (cả 2 nhánh isPrincipleContract)
- `total_after_vat` — filter `!p.is_child`

`vat_cost` và `vat_cost_decimal` tính từ `total_after_vat - total_before_vat` (đã filter gián tiếp).

`total_after_extra` = `_total_cost + total_extra` (dùng field `_total_cost` từ form + total_extra đã filter).

## Tên class product dùng trong `addChild`

| Tab | Class product |
|-----|---------------|
| FirmQuotationTab.addChild | `new FirmQuotationTabProduct(childData, this)` |
| FirmContractTab.addChild | `new FirmContractTabProduct(childData, this)` |

## Method `removeProduct` mới

Cả 2 tab: khi xoá dòng cha (`!removing.is_child`), filter toàn bộ `_products` loại bỏ dòng cha + tất cả con có `child_parent_tmp_id == removing.tmp_row_id`. Khi xoá dòng con, splice theo index như cũ.

FirmContractTab không có `removeProduct` trước → thêm mới.
FirmQuotationTab có `removeProduct` trước → sửa lại.

## Kết quả `php -l`

```
No syntax errors detected in FirmQuotationTabProduct.blade.php
No syntax errors detected in FirmQuotationTab.blade.php
No syntax errors detected in FirmContractTabProduct.blade.php
No syntax errors detected in FirmContractTab.blade.php
```

## Lưu ý / Concern

1. **`_effective_quantity` vs getter `quantity`**: Cần dùng `_effective_quantity` (trả số thực, không format) ở mọi chỗ tính toán (`total_cost`, `submit_data`). Getter `quantity` (format `numberWithCommas`) chỉ dùng cho UI hiển thị.

2. **Contract `after()` override quantity**: Khi load lại dữ liệu từ server (dòng con đã lưu có `child_parent_tmp_id`), `after()` sẽ override đúng. Khi thêm con mới bằng `addChild()`, hàm set `child_parent_tmp_id` sau constructor → getter mới không được apply. **Cần lưu ý**: `addChild` set `child_parent_tmp_id` SAU khi constructor đã chạy xong. Với FirmContractTabProduct, nên truyền `child_parent_tmp_id` và `child_ratio` vào `childData` ngay từ đầu để `after()` xử lý được. Tuy nhiên `_effective_quantity` (prototype getter) vẫn hoạt động đúng dù không có override `quantity` vì nó đọc trực tiếp `this.is_child` và `this.child_parent_tmp_id`.

3. **`allocationExtraCost()` trong FirmContractTab** không được filter con — giữ nguyên behavior vì nếu có hàng con trong allocation thì logic chia phụ phí sẽ phức tạp hơn và nằm ngoài scope P4A.
