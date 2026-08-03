# Task 2 — ProductRequest + ProductResource + ProductForm (min_stock)

**Trạng thái:** DONE

## Bối cảnh
Task 1 đã thêm cột `products.min_stock DECIMAL(18,2) NULL` + fillable trên `Product` entity. Task 2 đưa `min_stock` vào validate (BE), resource trả về (BE), và form hàng hoá (FE).

## File đã sửa

### 1. `nhatlinh-api/Modules/Category/Http/Requests/ProductRequest.php`
- Thêm rule trong `rules()`:
  ```php
  'min_stock' => 'nullable|numeric|min:0',
  ```
- Thêm message lỗi trong `messages()` (đồng bộ style các field số khác như `vat`):
  ```php
  'min_stock.numeric' => 'Mức tồn tối thiểu phải là số',
  'min_stock.min' => 'Mức tồn tối thiểu không được nhỏ hơn 0',
  ```

### 2. `nhatlinh-api/Modules/Category/Transformers/ProductResource/ProductResource.php`
- Thêm `'min_stock' => $this->min_stock,` cạnh `'vat' => $this->vat,` trong `toArray()`. Đây là resource dùng cho list (`GET category/products`).

### 3. `nhatlinh-api/Modules/Category/Transformers/ProductResource/DetailProductResource.php`
- File này tồn tại (đúng như plan lường trước) và là resource dùng cho `GET category/products/{id}` — nguồn dữ liệu `loadData()` của `ProductForm.vue` khi sửa/xem chi tiết.
- Thêm `'min_stock' => $this->min_stock,` cạnh `'vat' => $this->vat,` trong `toArray()`. Bắt buộc phải sửa file này để form sửa nạp được giá trị (nếu chỉ sửa `ProductResource.php` thì form edit sẽ không có `min_stock` vì nó gọi API detail, không phải list).

### 4. `nhatlinh-client/pages/category/products/components/ProductForm.vue`
- **Input mới:** thêm 1 `form-row` ngay dưới header "Đơn vị tính & Bảng giá" (trước bảng ĐVT), dùng `V2BaseInput` (đúng style các input số khác trong file như `vat`, `conversion_rate`):
  ```html
  <div class="form-row">
      <div class="col-md-3 mb-2">
          <V2BaseLabel>Mức tồn tối thiểu</V2BaseLabel>
          <V2BaseInput
              v-model="form.min_stock"
              type="number"
              placeholder="Để trống = không cảnh báo"
              size="sm"
              :disabled="isView"
              min="0"
          />
          <small class="text-muted">Theo ĐVT cơ bản, để trống = không cảnh báo tồn thấp</small>
          <div v-if="formError['min_stock']" class="text-small-error mt-1">
              <i class="ri-error-warning-line mr-1"></i>{{ formError['min_stock'] }}
          </div>
      </div>
  </div>
  ```
  Đặt gần khu vực ĐVT/số lượng theo yêu cầu, có ghi chú nhỏ, hỗ trợ hiện lỗi inline `formError['min_stock']` (đồng bộ pattern lỗi inline các field khác trong file — không cần thêm `touched` riêng vì form này validate qua response 422 chung, giống cách `formError['code']`, `formError['vat']` đang làm).
- **`data().form`:** thêm `min_stock: null` (khởi tạo mặc định, để trống = không cảnh báo).
- **`resetForm()`:** thêm `min_stock: null` vào object reset (đồng bộ với `data()` để tránh lệch state sau khi tạo mới liên tiếp).
- **`loadData()`:** thêm nạp giá trị khi sửa/xem:
  ```js
  min_stock: data.min_stock !== null && data.min_stock !== undefined ? data.min_stock : null,
  ```
- **`submitForm()` — payload:** thêm vào payload gửi đi:
  ```js
  min_stock: this.form.min_stock !== null && this.form.min_stock !== '' ? this.form.min_stock : null,
  ```
  (Empty string → null vì `V2BaseInput` không dùng `.number` modifier, input rỗng trả về `''`, giống cách các field số khác trong file — không phá vỡ convention hiện có.)

## Verify

### BE — `php -l`
```
$ cd nhatlinh-api && php -l Modules/Category/Http/Requests/ProductRequest.php \
    && php -l Modules/Category/Transformers/ProductResource/ProductResource.php \
    && php -l Modules/Category/Transformers/ProductResource/DetailProductResource.php

No syntax errors detected in Modules/Category/Http/Requests/ProductRequest.php
No syntax errors detected in Modules/Category/Transformers/ProductResource/ProductResource.php
No syntax errors detected in Modules/Category/Transformers/ProductResource/DetailProductResource.php
```
(Có warning `imagick.so` không load được — chỉ do PHP CLI local thiếu extension, không liên quan code, không ảnh hưởng kết quả `php -l`.)

### FE — đọc lại (không build)
- Xác nhận `form.min_stock` xuất hiện đúng 3 chỗ: khởi tạo (`data()`), nạp lại (`loadData()`), reset (`resetForm()`), và trong payload submit (`submitForm()`).
- Binding dùng `V2BaseInput` (component chuẩn của form, không dùng `b-form-input` để giữ đồng bộ style).
- Input đặt trong tab "Thông tin chung", ngay dưới heading "Đơn vị tính & Bảng giá" — gần khu vực số lượng/ĐVT theo yêu cầu.
- Không cần verify build vì Node cũ không build được (theo Global Constraints) — user cần tự mở trình duyệt test luồng thêm/sửa hàng hoá.

## Concerns
- Không sửa `ProductRequest.php` message riêng là bắt buộc theo plan (plan chỉ yêu cầu rule), nhưng đã thêm thêm messages để đồng bộ pattern lỗi tiếng Việt sẵn có trong file — không phải yêu cầu bắt buộc, có thể bỏ nếu không cần.
- Chưa test thực tế trên trình duyệt (submit/nạp lại) vì không có access UI — cần user tự verify theo Step 5 của Task 2 trong plan: thêm/sửa 1 hàng, nhập Mức tồn tối thiểu, lưu, mở lại kiểm tra giá trị giữ đúng.
- Không đụng tới `pages/category/products/index.vue` (danh sách) — task 2 không yêu cầu hiển thị `min_stock` ở màn danh sách, chỉ ở form.

---

## Fix C1 + T4b (final review)

**Trạng thái:** DONE

### FIX 1 (CRITICAL) — `min_stock` không được lưu xuống DB

**File:** `nhatlinh-api/Modules/Category/Services/ProductService.php`

Nguyên nhân: `updateOrCreate()` (dòng 122-138 cũ) và `update()` (dòng 166-189 cũ) build mảng `$productData` thủ công, quên field `min_stock` dù cột DB + validate + resource đã có từ Task 2. Hệ quả: `min_stock` luôn NULL trong DB → `WhDashboardService::lowStock()` (`whereNotNull('min_stock')`) luôn trả rỗng.

Đã thêm vào CẢ HAI mảng (dòng 136 và 188, đặt cạnh `supplier_id`):
```php
'min_stock' => $request->min_stock !== '' ? $request->min_stock : null,
```
Theo đúng style property-access `$request->field` mà file đang dùng cho các field khác (không dùng `->input()`). Empty string từ FE (input rỗng) → `null`; giá trị hợp lệ (kể cả `0`) được giữ nguyên (không dùng `?:` vì `0` là falsy, tránh mất giá trị 0).

### FIX 2 (Minor) — đồng bộ Carbon string-unit trong `movementByTime()`

**File:** `nhatlinh-api/Modules/Warehouse/Services/WhDashboardService.php`

Vòng lặp sinh label mốc (dòng ~68-78 cũ) dùng `->sub($config['unit'], $i)` dạng string-unit, không nhất quán với `windowStart()` (đã dùng `subWeeks/subMonths/subQuarters/subYears`). Đã đổi thành `switch ($granularity)` gọi đúng method cụ thể (`subWeeks($i)` / `subQuarters($i)` / `subYears($i)` / `subMonths($i)` mặc định), giữ nguyên số mốc, thứ tự cũ→mới và định dạng label — không đổi output.

### Verify

**1. `php -l`:**
```
No syntax errors detected in Modules/Category/Services/ProductService.php
No syntax errors detected in Modules/Warehouse/Services/WhDashboardService.php
```
(chỉ có warning `imagick.so` không load — môi trường local, không liên quan code sửa)

**2. Tinker — FIX 1 (min_stock lưu được qua update array giống ProductService):**
```php
$p = Product::first();
$p->update(['min_stock' => 15]);
$reload = Product::find($p->id);
// min_stock_after_save='15.00'
$p->update(['min_stock' => $orig]); // khôi phục dữ liệu gốc
// min_stock_restored=NULL
```
Kết quả: `product_id=1`, `min_stock_after_save='15.00'` (không NULL) → cột lưu đúng khi có `min_stock` trong mảng update. Đã đọc lại code, xác nhận cả 2 mảng `$productData` trong `ProductService.php` (dòng 136 và 188) nay có key `'min_stock'`. Dữ liệu test đã được khôi phục về giá trị gốc (NULL), không làm bẩn DB.

**3. Tinker — FIX 2 (4 granularity vẫn đúng số mốc/label):**
```
week: count=12 labels=2026-W16,...,2026-W27
month: count=12 labels=2025-08,...,2026-07
quarter: count=8 labels=2024-Q4,...,2026-Q3
year: count=5 labels=2022,2023,2024,2025,2026
```
Đúng số mốc kỳ vọng (12/12/8/5), thứ tự cũ→mới, định dạng label không đổi (`YYYY-WWW`, `YYYY-MM`, `YYYY-QN`, `YYYY`).

### Concerns
- Không có concern mới. `min_stock` giờ dùng property-access `$request->min_stock` (thay vì `input()`) để đồng bộ 100% với style hiện có của file — hành vi tương đương (`Illuminate\Http\Request::__get` proxy sang `input()`).
- Key `'unit'` trong mảng `$config` của `movementByTime()` (vd `'unit' => 'week'`) nay không còn được dùng ở vòng lặp label (đã thay bằng switch theo `$granularity`) nhưng vẫn giữ nguyên trong khai báo `$config` để tối thiểu hoá diff — không gây lỗi, chỉ là field dư không dùng.
