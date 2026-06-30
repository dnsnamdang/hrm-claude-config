# Task P4b — Báo giá: UI bảng cha-con + edit-load

## Nơi nạp data edit

**File:** `app/Services/Sale/Firm/Quotation/FirmQuotationService.php`
**Method:** `getDataForEdit($id)` (dòng ~417)

Mỗi product gọi `$product->getDataForQuotationEdit()` — đây là method trên `BaseQuotationProduct` trả về `$product->data` merged với `$this->toArray()`. `toArray()` đã có `child_parent_id` và `child_ratio` nhờ `$fillable`, nhưng **không có** `tmp_row_id` và `child_parent_tmp_id` mà FE cần.

**Fix:** Override `getDataForQuotationEdit()` trên `FirmQuotationTabProduct` để append thêm:
- `tmp_row_id` = `(string) $this->id`
- `child_parent_tmp_id` = `$this->child_parent_id ? (string) $this->child_parent_id : null`
- `child_ratio` = `$this->child_ratio`

Dùng DB id làm stable key → `tmp_row_id` dòng cha và `child_parent_tmp_id` dòng con khớp nhau, class JS dựng đúng cụm.

## Cách tái dùng modal chọn sản phẩm

Modal dùng: `#searchProduct` (Datatable `#search-product-table`), callback qua `$scope.addProduct`.

Kỹ thuật: lưu context `tab` + `parentProduct` vào `$scope._childPickerTab/_childPickerParent`, set flag `$scope._addProductMode = 'child'`, rồi mở modal bình thường (`$scope.searchProduct(tab)`). Wrap `$scope.addProduct` bằng closure mới — khi mode là `'child'`, route request sang `tab.addChild(parentProduct, childData, 1)` thay vì `tab.addProduct`; sau đó reset flag và gọi `_addProductOriginal` cho flow thông thường.

## Files đã sửa

| File | Thay đổi |
|------|----------|
| `resources/views/sale/firm/quotations/form.blade.php` | CSS `.child-row`; `ng-class` thêm `child-row`; `ng-style` thụt lề ô tên + icon `└`; SL conditional read-only cho con; input tỉ lệ trong cell SL cho con; nút `+ con` trong cột Thành tiền |
| `resources/views/sale/firm/quotations/formJs.blade.php` | Thêm `openChildPicker`, wrap `$scope.addProduct` để route sang `addChild` khi mode child |
| `app/Model/Sale/Firm/Quotation/FirmQuotationTabProduct.php` | Override `getDataForQuotationEdit()` để trả `tmp_row_id`, `child_parent_tmp_id`, `child_ratio` |

## php -l

```
No syntax errors detected in form.blade.php
No syntax errors detected in formJs.blade.php
No syntax errors detected in FirmQuotationTabProduct.php
```

## STATUS

DONE. Không có concern tắc nghẽn.

**Lưu ý nhỏ:** `$scope._addProductOriginal` được gán ngay sau khi `$scope.addProduct` được định nghĩa lần đầu trong `formJs.blade.php`. Thứ tự này quan trọng — nếu ai đó định nghĩa lại `$scope.addProduct` sau đó thì phải cập nhật lại. Trong codebase hiện tại không có trường hợp đó nên an toàn.

**Edit-load concern:** Khi load lại báo giá đã lưu, `getDataForEdit` trả về products đã có `tmp_row_id = DB id`. Class JS dùng `form.tmp_row_id || randomString()` — vì `tmp_row_id` đã có sẵn từ BE, class sẽ dùng đúng giá trị DB id → `child_parent_tmp_id` khớp → cụm cha-con hiển thị đúng.
