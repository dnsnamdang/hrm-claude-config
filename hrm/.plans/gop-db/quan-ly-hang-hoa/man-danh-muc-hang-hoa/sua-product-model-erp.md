# Việc phải sửa `Product.php` + `ProductsController` bên ERP (21/09/2026)

> User: *"Khi đưa quản lý hàng hoá sang HRM, bổ sung một số danh mục, bỏ bớt một số như đã phân
> tích ⇒ model `Product.php` bên ERP cũng cần phải cập nhật."*
>
> **Đúng — và có một chỗ là CHẶN CỨNG**, không sửa thì hàng hoá do HRM tạo **không sửa được ở ERP**.

---

## 1. 🔴 BB-7 — Rule `required` chặn cứng hàng hoá do HRM tạo

`ProductsController@update` (dòng 1117) khai bộ rule **inline** (không dùng `getRules()`), trong đó:

```php
'product_type'            => 'required',
'group_id'                => 'required|exists:groups,id',
'vat_percent_tax_rate_id' => 'required',
'avatar'                  => 'required',
'company_id'              => 'required|exists:companies,id',
```

**Cơ chế hỏng:** HRM tạo hàng hoá theo quyết định 3 + 6 + 8 ⇒ `product_type` trống, `product_cate`
trống, `group_id` trống. Người dùng mở hàng hoá đó **ở ERP** rồi bấm Lưu ⇒ **422, không lưu được**.

Thêm 2 rule nữa dễ vấp:
- `avatar => required` — hàng hoá **bắt buộc có ảnh** ở ERP. Đo đúng: `products.avatar` có
  **45.448 / 45.890** dòng (97 %) ⇒ rule chạy bình thường, **HRM phải áp cùng**: form bắt buộc ảnh
  đại diện, nếu không hàng hoá tạo từ HRM sẽ không sửa được ở ERP.
- `name` unique theo **bộ 3** `(model_id, brand_id, origin_id)`:
  ```php
  Rule::unique('products')->where(fn($q) => $q->where('model_id', …)->where('brand_id', …)->where('origin_id', …))->ignore($id)
  ```
  HRM **phải áp cùng rule**, nếu không sẽ tạo được bản trùng mà ERP không sửa nổi.

**Hai cách xử lý — phải chọn trước khi bật màn HRM:**

| Cách | Việc | Đổi lại |
|---|---|---|
| (a) **Nới rule bên ERP** | bỏ `required` của `product_type` + `group_id` trong `ProductsController@update` (và `getRules()` nếu cần) | Đúng hướng "3 cột cũ sẽ bỏ". Nhưng đụng vào validate của màn đang chạy |
| (b) **HRM vẫn điền 3 cột cũ** | trái quyết định 3 + 6 (đã loại phương án ánh xạ) | không nên |

⇒ Đề xuất **(a)**, gộp cùng lần sửa `SearchController` (BB-6).

---

## 2. Quy mô phải rà trong `Product.php`

`app/Product.php` — **8.122 dòng**. Số chỗ đụng các cột sắp bỏ:

| Cột / thành phần | Số chỗ trong `Product.php` |
|---|---|
| `group_id` | **94** |
| `product_type` | **77** |
| `product_cate` | **75** |
| `group_ids_use` (Nhóm máy/Máy) | 6 |
| `productsUse()` | 5 |
| `groupsUse()` | 3 |
| `getCanRetailAttribute()` | 1 |

`$fillable` hiện có 27 cột, **chưa có** `product_type_id` / `product_characteristic_id`.

---

## 3. Danh sách việc — chia theo thời điểm

### 3.1 Làm NGAY trong Phase 2 (bắt buộc, nếu không ERP vỡ)

| # | Việc | Nơi | Vì sao |
|---|---|---|---|
| 1 | **Bỏ `required` của `product_type` + `group_id`** | `ProductsController@update:1127,1133` | BB-7 — không sửa thì hàng hoá HRM tạo không lưu được ở ERP |
| 2 | Thêm `product_type_id`, `product_characteristic_id` vào **`$fillable`** | `Product.php:244` | ERP còn ghi qua đường hàng tạm tới hết Phase 6; thiếu fillable thì `create()` **bỏ qua im lặng** |
| 3 | Thêm 2 quan hệ đọc cây phân loại mới | `Product.php` | ERP cần hiển thị Loại sản phẩm ở màn xem/danh sách |
| 4 | Bỏ 2 điều kiện lọc enum cũ | `SearchController` (4 hàm) | BB-6 — hàng hoá mới vô hình với 338 màn |

**Quan hệ cần thêm** (`Product.php`):

```php
public function product_type_ref()      // tránh trùng tên với cột chuỗi `product_type`
{
    return $this->belongsTo('App\Model\MasterData\ProductType', 'product_type_id', 'id');
}

public function product_characteristic()
{
    return $this->belongsTo('App\Model\MasterData\ProductCharacteristic', 'product_characteristic_id', 'id');
}
```

⚠️ **Bẫy đặt tên:** cột chuỗi cũ tên `product_type`. Khai quan hệ cùng tên `product_type()` sẽ
**đụng nhau** — `$product->product_type` đang trả chuỗi enum ở 77 chỗ. Phải đặt tên khác
(`product_type_ref` / `productTypeRef`). Đây đúng là cái bẫy đã gặp ở Phase 1 khi đặt tên Entity
`ProductAttribute` để tránh clash với `$model->attributes` của Eloquent.

### 3.2 Làm DẦN (khi gỡ 3 cột cũ — đã note ở §9 spec)

| # | Việc | Số chỗ |
|---|---|---|
| 5 | Thay 94 chỗ `group_id` bằng cây mới | `Product.php` 94 · toàn ERP 422 file |
| 6 | Thay 77 chỗ `product_type` | `Product.php` 77 · toàn ERP 281 file |
| 7 | Thay 75 chỗ `product_cate` | `Product.php` 75 · toàn ERP 159 file |
| 8 | Gỡ `getCanRetailAttribute()` + chuỗi `QuotationProduct → Quotation → canCreateSaleOrder` | 1 + 4 |
| 9 | Gỡ `groupsUse()` / `productsUse()` / `group_ids_use` (Nhóm máy – Máy) | 14 |
| 10 | Gỡ 2 mảng nhãn cứng `$product_cates` (11 giá trị) + nhãn `product_type` (16 giá trị) | `Product.php:250` |

### 3.3 KHÔNG đụng

`ProductTemplate.php` · `ProductInfo.php` — hàng hoá gốc và hàng hoá có sẵn giữ nguyên ERP, có
`product_type` / `product_cate` / `group_id` **của riêng chúng**.

---

## 4. Ràng buộc HRM phải sao chép y hệt

Bộ rule của `ProductsController@update` là **hợp đồng dữ liệu** mà mọi bảng vệ tinh phải thoả. HRM
không áp đúng thì tạo ra bản ghi ERP không sửa nổi.

| Nhóm | Rule |
|---|---|
| Tên | unique theo **bộ 3** `(model_id, brand_id, origin_id)` · `max:180` |
| Đơn vị tính | `units` ≥ 1 · `unit_id` **distinct** · `cost_price` required · `sale_max_percent_coefficient` required **`not_in:0`** |
| Giá | mỗi ĐVT `prices` ≥ 1 · `price_type_id` exists · `price` required · `coefficient` required `max:99` |
| Giá hiệu lực | `expected_prices` **`max:1`** — tối đa 1 dòng **MỖI LẦN GỬI** · `effect_date` **`after:today`** |
| Thuộc tính | `value` `required_if` thuộc tính đó `require = true` |
| Hàng hoá kèm | `qty` `min:1` · `unit_id` required (trừ *vật tư sửa chữa*) |
| Hệ số theo công ty | `company_id` **distinct** · `coefficient` **`not_in:0`** |
| Khác | `barcode` `max:15` · `hs_code` regex `^\d{3,12}$` · `norm` `max:1000` **`not_in:1000`** · `tech_coefficient` `min:1` |

⚠️ Ba rule dễ bỏ sót vì "lạ": **`not_in:0`** ở 2 chỗ và **`not_in:1000`** ở `norm` — đều là "khác 0
/ khác trần", không phải `min`/`max` thường.

📌 **`expected_prices => max:1` không có nghĩa mỗi loại giá chỉ được 1 dòng giá hiệu lực.** Đo thật:
**22.343** `unit_price` đang có **nhiều hơn 1** dòng trong `product_expected_prices`. Rule chỉ giới
hạn **mỗi lần LƯU gửi lên tối đa 1 dòng mới**; lịch sử thì tích luỹ. Mockup vẽ nhiều dòng là **đúng**.

---

## 5. Câu cần chốt

1. Nới rule `required` (`product_type`, `group_id`) bên ERP theo cách (a) — xác nhận để gộp cùng
   lần sửa `SearchController`.
2. **Ảnh đại diện bắt buộc** (`avatar => required`, 97 % hàng hoá đang có) — form HRM áp cùng chứ?
   Mockup hiện chưa đánh dấu bắt buộc.

---

## 6. 🐞 Đính chính số đo của chính tôi (21/09/2026)

Ở vòng rà soát trường (design.md mục B) tôi báo **`avatar`, `short_description`, `special_feature`,
`comment`, `comment_temp` đều "0 dòng"** và lấy đó làm căn cứ loại chúng khỏi mockup.

**Sai ở 2 cột.** Nguyên nhân: câu đo dùng `where($cot, '<>', 0)` cho **cột chuỗi** — MySQL ép kiểu
số nên `'abc' = 0` là TRUE, loại sạch mọi giá trị chữ.

| Cột | Tôi báo | Thật |
|---|---|---|
| `avatar` | 0 | **45.448 / 45.890** |
| `comment` | 0 | **2.267** |
| `model_old` | 770 | **3.706** |
| `old_barcode` | 100 | **133** |
| `code_2025` | 42 | **36.195** |
| `code_2020` | 44 | **36.001** |
| `serial_number` · `short_description` · `special_feature` · `comment_temp` | 0 | **0 — đúng** |

⇒ Kết luận **"bỏ ô Serial number"** vẫn đúng (0 dòng thật). Nhưng **`avatar` phải là trường bắt
buộc** trên form HRM, và `code_2025`/`code_2020` (**~36.000 dòng mỗi cột**) không phải "dữ liệu di
sản < 2%" như tôi viết — cần hỏi lại nghiệp vụ 2 cột mã này dùng làm gì.

**Cách đo đúng cho cột chuỗi:** `whereNotNull($c)->where($c, '<>', '')` — **không** so với `0`.
