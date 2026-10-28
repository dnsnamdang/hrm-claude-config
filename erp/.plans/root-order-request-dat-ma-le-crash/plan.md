# Fix: màn root_order_request/show crash khi chọn "Đặt theo mã lẻ"

## Bối cảnh / Triệu chứng
- URL: `/admin/orders/root_order_request/{id}/show` (vd 8689).
- Khi bấm **"Đặt theo mã lẻ"** (combo có `has_recipe`) → `addByRecipe` tách combo thành các dòng linh kiện lấy từ `getRecipe`.
- Lỗi JS: `TypeError: Cannot read properties of undefined (reading 'brand_id')`
  tại `$scope.notificationForegins (show:5169)`.

## Nguyên nhân gốc (ĐÃ XÁC ĐỊNH)
File: `resources/views/orders/root_order_requests/show.blade.php`
- 3 hàm filter thông báo đọc `product.product.brand_id`:
  - `inlandNotificationFrees` (dòng 885-887)
  - `inlandNotificationFirms` (dòng 889-891)
  - `notificationForegins` (dòng 893-895) — hàm trong stack trace (dùng khi `type_order_request == 2`)
- Dòng DB-load có relation lồng `product` → `product.product.brand_id` OK.
- Dòng tách từ recipe (`addByRecipe` → `form.addProduct(r)` với `r` là data phẳng từ
  `ProductsController@getRecipe` = `Product::find(...)->publicDataFor(...)`) KHÔNG có key `product` lồng,
  mà có `brand_id` ở cấp cao nhất → `product.product` undefined → đọc `.brand_id` crash.
  (`RootOrderRequestProduct` constructor chỉ copy key từ input; không có `product` thì `this.product` undefined.)

## Hướng sửa (đã áp dụng)
Phát hiện khi verify: dòng recipe KHÔNG có `brand_id` phẳng — brand nằm ở OBJECT `brand` (`product.brand.id`);
còn `manufacture_id` thì cả dòng DB lẫn recipe đều có phẳng (giữ nguyên). Nên fix bằng 1 helper chung
`$scope.productBrandId(product)`:
```
if (product.product) return product.product.brand_id; // dòng DB-load (relation lồng)
if (product.brand)   return product.brand.id;         // dòng recipe (getRecipe trả object brand)
return product.brand_id;                               // phòng hờ
```
Cả 3 hàm `inlandNotificationFrees` / `inlandNotificationFirms` / `notificationForegins` dùng helper này thay cho `product.product.brand_id`.

## Verify (Playwright, local 6477, 2026-10-27)
- Dòng DB-load: `product.product.brand_id`=277 (có nested `product`); dòng recipe: `product.brand.id`=333, KHÔNG có nested `product`.
- Biểu thức CŨ `splitRow.product.brand_id` → ném đúng lỗi "Cannot read properties of undefined (reading 'brand_id')" (khớp stack trace prod show:5169).
- Sau fix: `productBrandId(splitRow)`=333; gọi cả 3 hàm trên dòng recipe-split (set type=2) → NO crash.

## Tasks
- [x] Trace + xác định nguyên nhân gốc (recipe-split row không có nested `product`; brand ở object `brand`)
- [x] Fix 3 hàm bằng helper `productBrandId` trong show.blade.php
- [x] Verify bằng Playwright trên local: dòng recipe-split không còn crash, resolve đúng brand.id
