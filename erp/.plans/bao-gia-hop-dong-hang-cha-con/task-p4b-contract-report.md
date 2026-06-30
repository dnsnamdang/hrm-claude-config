# Task P4b Contract — Báo cáo thực hiện

## 1. Nơi nạp data edit HĐ

- **File**: `app/Services/Sale/Firm/Contract/FirmContractService.php`
- **Method**: `getDataForEdit($id)` (dòng ~1082)
- **Flow**: Controller `FirmContractController::edit()` (dòng 315) gọi `$firmContractService->getDataForEdit($firm_contract->id)`, truyền kết quả vào view `contracts.edit` dưới key `$data`.
- Products được load qua Eloquent `with(['tabs.products' => fn($q) => $q->select(['*', 'product_attributes as attribute_products'])])` — tất cả cột DB được include qua `*`, kể cả `child_parent_id` và `child_ratio`.

## 2. Kết quả verify selectQuotation flow

**Đã verify, không cần sửa formJs.blade.php.**

Lý do:
- `formJs.blade.php` gọi `$scope.form.selectQuotation(quotation)` sau khi nhận response từ `getDataForContract`.
- `selectQuotation` trong class `FirmContract` (FirmContract.blade.php dòng 459) thực hiện `this.tabs = quotation.tabs`.
- `FirmContractTab.set tabs()` gọi `new FirmContractTabProduct(val, this)` cho mỗi product.
- `FirmContractTabProduct.after()` đọc `form.tmp_row_id`, `form.child_parent_tmp_id`, `form.child_ratio` — các field này đã được Phase 4a đảm bảo trả về từ `getDataForContract` (trên báo giá).
- Không có transform/filter field nào trong formJs gây mất `tmp_row_id`/`child_parent_tmp_id`.

## 3. Danh sách file đã sửa

### A. `resources/views/sale/firm/contracts/form.blade.php`

**Thêm CSS `.child-row`** (đầu `<style>`):
```css
.child-row {
    background: #f7fbff;
}
.child-row td:first-child {
    padding-left: 8px;
}
```

**Cập nhật `<tr ng-repeat>`** — thêm `'child-row': product.is_child` vào ng-class:
```html
<tr ng-repeat="product in tab.products" ng-class="{'odd-row': $index % 2 == 0, 'invalid': !form.checkValidTabProduct(product), 'child-row': product.is_child}">
```

**Cột tên hàng** — thêm indent + icon `└`:
```html
<td style="width: 350px" ng-style="product.is_child ? {'padding-left': '30px'} : {}">
    <span ng-if="product.is_child">&lfloor; </span><% product.product_name %>
</td>
```

**Cột SL** — thêm nhãn tỉ lệ read-only:
```html
<td class="text-center">
    <% product.quantity %>
    <small ng-if="product.is_child" class="text-muted d-block">(tỉ lệ <% product.child_ratio %>)</small>
</td>
```

Không thêm nút xoá riêng — nút xoá chưa có trong form HĐ này (read-only table). Nếu sau này có thêm nút xoá thì phải thêm `ng-if="!product.is_child"`.

### B. `app/Services/Sale/Firm/Contract/FirmContractService.php`

**Thêm vào cuối `getDataForEdit()`**, trước `return $result`:
```php
// Thiết lập tmp_row_id / child_parent_tmp_id cho từng dòng sản phẩm
// để FE FirmContractTabProduct có thể khôi phục quan hệ cha-con khi edit
foreach ($result['tabs'] as &$tab) {
    foreach ($tab['products'] as &$product) {
        $product['tmp_row_id']        = (string) $product['id'];
        $product['child_parent_tmp_id'] = $product['child_parent_id']
            ? (string) $product['child_parent_id']
            : null;
    }
    unset($product);
}
unset($tab);
```

**Lý do**: `FirmContractTabProduct.after()` (JS class) đọc `form.tmp_row_id || randomString()` — nếu không có `tmp_row_id` từ server, mỗi lần load trang sẽ sinh ID ngẫu nhiên, và `child_parent_tmp_id` sẽ là null nên dòng con không nhận ra cha của mình, mất hoàn toàn quan hệ cha-con khi edit.

## 4. Kết quả php -l

```
No syntax errors detected in app/Services/Sale/Firm/Contract/FirmContractService.php
No syntax errors detected in resources/views/sale/firm/contracts/form.blade.php
```

## 5. Concern / Risk

1. **show.blade.php không được sửa**: `getDataForShow` cũng load products nhưng có thêm filter `->where('root_quantity', '>', 0)`. Nếu trang show cũng cần hiển thị cha-con, cần thêm mapping tương tự trong `getDataForShow`. Hiện tại Phase 4b chỉ yêu cầu form edit.

2. **Khoá chặt dòng con**: FE class `FirmContractTabProduct` đã khoá write vào `quantity` cho dòng con (set() bỏ qua). Tuy nhiên input `total_extra_cost` và `discount` (doanh số vượt trội, giảm giá) vẫn có thể nhập trên dòng con vì form.blade.php chưa thêm `ng-disabled="product.is_child"` cho 2 input đó. Có thể là intentional (cho phép nhập giảm giá riêng cho dòng con) — cần xác nhận với PM nếu cần khoá thêm.

3. **`child_ratio` từ DB là null**: Nếu HĐ cũ lưu trước khi có cột `child_ratio`, giá trị sẽ null → dòng con vẫn nhận biết qua `child_parent_id != null` nhưng tỉ lệ hiển thị sẽ rỗng. Không ảnh hưởng tính năng mới, chỉ UI.
