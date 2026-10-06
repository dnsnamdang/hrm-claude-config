# Sửa ERP để không lỗi khi hàng hoá thiếu 3 cột cũ (21/09/2026)

> **User chốt 21/09/2026:**
> - *"Khi update quản lý hàng hoá HRM tôi sẽ **chặn toàn bộ route tạo/sửa hàng hoá ERP**."*
> - *"Chỉ cần tập trung vào việc **update Model + Controller phía ERP sao cho các chức năng có sửa
>   hàng hoá không bị lỗi**."*
> - *"Các trường mã chỉ quan tâm `code`; `code_2025`, `code_2020` là tôi backup để mapping khi đổi
>   cách sinh mã ⇒ không cần quan tâm."*

---

## 0. Việc gì KHÔNG còn phải lo

| Việc từng nêu | Vì sao hết lo |
|---|---|
| **BB-7** — rule `required` của `product_type`/`group_id` chặn sửa ở ERP | Route tạo/sửa bên ERP **bị chặn**, không ai đi qua validate đó nữa |
| Đồng bộ rule validate ERP ↔ HRM (`name` unique bộ 3, `avatar` required, `not_in:0`…) | Chỉ còn HRM validate. HRM tự chọn rule của mình |
| `code_2025` · `code_2020` (~36.000 dòng mỗi cột) | User xác nhận là **cột backup để mapping**, không phải trường nghiệp vụ |
| Va chạm mã giữa 2 app | ERP hết tạo hàng hoá ⇒ không còn 2 tiến trình cùng sinh mã |

⇒ **Chỉ còn đúng một loại việc: làm ERP ĐỌC được hàng hoá thiếu 3 cột cũ mà không nổ.**

---

## 1. 🔴 Vấn đề trung tâm: `->group->…` không chỗ nào null-safe

`products.group_id` sẽ **trống** với hàng hoá tạo từ HRM. ERP truy cập quan hệ `group` bằng
`->group->cột` ở **hơn 100 chỗ** và **KHÔNG một chỗ nào** dùng `optional()` hay `?->`.

PHP 7.4: `null->name` ⇒ **`Trying to get property of non-object`** — nổ ra màn hình, không phải
hiển thị trống.

### 1.1 Các file làm việc trên bảng `products` — PHẢI sửa

| File | Số chỗ | Còn sống sau khi chặn route? | Mức |
|---|---|---|---|
| **`Http/Controllers/Common/SearchController.php`** | **11** | 🟢 **CÓ — popup chọn hàng của 338 màn** | 🔴 |
| `Http/Controllers/Sale/DeviceErrorController.php` | 8 | 🟢 có — lỗi thiết bị / bảo hành | 🔴 |
| `Product.php` | 7 | 🟢 có — model dùng chung | 🔴 |
| `Http/Controllers/Sale/TmpProductsController.php` | 3 | 🟢 có — hàng tạm (tới hết Phase 6) | 🔴 |
| `Model/Sale/LiquidationQuotation.php` | 2 | 🟢 có — báo giá thanh lý | 🟡 |
| `Model/Sale/CostFixingQuotation.php` | 2 | 🟢 có — báo giá chốt giá | 🟡 |
| `Jobs/ProductSettingMailJob.php` | 1 | 🟢 có — **job nền gửi mail** | 🟡 |
| `Http/Controllers/Sale/MyTmpProductsController.php` | 1 | 🟢 có | 🟡 |
| `Console/Commands/ExportLargeProductList.php` | 1 | 🟢 có — **lệnh theo lịch** | 🟡 |
| `BaseProduct.php` | 1 | 🟢 có — `must_serial` | 🟡 |
| `Model/Product/JobCluster.php` | 2 | ⚫ cây cũ (Phase 5 bỏ) | ⚪ |
| `Http/Controllers/ProductsController.php` | 14 | ⚠️ route **bị chặn**, nhưng xem §1.3 | 🟡 |
| ~~`Http/Controllers/Product2Controller.php`~~ | ~~12~~ | ⚫ **BỎ QUA** — user chốt 21/09: chức năng liên quan chưa dùng tới (xem §1.4) | ⚪ |

**Tổng phải sửa ngay: ~37 chỗ** trên 10 file còn sống (chưa tính 2 controller bị chặn).

### 1.2 Vì sao `SearchController` là nặng nhất

```php
->addColumn('group_id',   fn($product) => $product->group->name)          // :787
->addColumn('vat_percent', fn($product) => $product->vat_percent
                                 ? floatval($product->vat_percent)
                                 : floatval($product->group->vat_percent)) // :807
```

Đây là callback của **DataTables, chạy cho TỪNG DÒNG kết quả**. Chỉ cần **một** hàng hoá thiếu nhóm
lọt vào trang kết quả là **cả popup nổ** — với mọi người dùng, ở cả 338 màn.

Nặng hơn hẳn `BB-6` đã nêu trước đó (ở đó tôi mới nói hàng hoá *"biến mất"*; thực tế còn **crash**).

📌 Có **một** chỗ ERP đã kiểm null — `SearchController:813` viết `$product->group ? … : …`. Chứng tỏ
lỗi này từng xảy ra và được vá lẻ một chỗ, không rà hết.

### 1.3 `ProductsController` bị chặn route vẫn nên rà

14 chỗ. Route **tạo/sửa** bị chặn, nhưng trong đó còn các hàm **chỉ đọc** mà màn khác gọi —
`searchData`, `getData`, `getDataForPriceAsking`, `getDataForInventory`, `barcode`… Cần rà xem hàm
nào còn được gọi từ ngoài; hàm đó vẫn phải null-safe.

### 1.4 ⚫ `Product2Controller` — BỎ QUA ở giai đoạn này (user chốt 21/09/2026)

*"Chưa cần quan tâm đến controller này, vì các chức năng liên quan chưa dùng tới."*

Ghi lại để sau này khỏi khảo sát lại:

- **Là 2 màn** trong nhóm menu **"Đồng bộ hàng hoá"**, cùng controller, phân biệt bằng query:
  `product2.index?type=creating` = *Danh sách hàng hoá đang tạo* · `?type=approver` = *Danh sách chờ
  nhập giá*.
- Quy mô: **2.433 dòng** · 8 view + **3 tab** (*Thông tin hàng hóa* · *Thông tin mua hàng* ·
  *Giá theo đơn vị*) · 12 route, có **3 hàm cập nhật** `update`/`update2`/`update3`.
- **Có ghi thật vào `products`**: `Product::createRecord()` :506 · `ProductVersion::create()` :1152 ·
  `AttributeProduct::create()` :1183.
- Trên DB local: `product_infos` **0 dòng**, `pi_groups` **0 dòng**, `sync_*` **không có bảng**,
  hàng hoá `group_id`/`model_id` NULL = **0/0** ⇒ khớp với "chưa dùng tới".

🟢 **Một thứ NÊN dùng lại từ nó** — `searchData` đã null-safe sẵn đúng bài toán Phase 2 tạo ra:

```php
->editColumn('group_id', fn($p) => $p->group_id ? $p->group->name : 'Chưa xác định')
->editColumn('model',    fn($p) => $p->model_id ? $p->model->name : 'Chưa xác định')
```

⇒ Khi sửa `SearchController` và các chỗ khác, dùng đúng khuôn `'Chưa xác định'` này cho nhất quán
với ERP, thay vì để trống.

---

## 2. Cách sửa

### 2.1 Null-safe ở nơi đọc

PHP 7.4 (không có `?->`), dùng `optional()` của Laravel:

```php
// TRƯỚC
$product->group->name
floatval($product->group->vat_percent)
$this->group->rate_liquidation

// SAU
optional($product->group)->name
floatval(optional($product->group)->vat_percent ?? 0)
optional($this->group)->rate_liquidation ?? 0
```

⚠️ Với cột **số** phải kèm giá trị mặc định (`?? 0`), nếu không `floatval(null)` = 0 thì may, nhưng
phép chia `… / $rate` sẽ ra lỗi chia cho 0 ở chỗ khác.

### 2.2 Hoặc: accessor gom về một chỗ trong `Product.php`

Thay vì vá ~37 chỗ rời, thêm accessor và đổi nơi gọi sang dùng nó:

```php
// app/Product.php
public function getGroupNameAttribute()      { return optional($this->group)->name ?? ''; }
public function getGroupVatPercentAttribute(){ return optional($this->group)->vat_percent ?? 0; }
public function getRateLiquidationValueAttribute()
{
    return $this->rate_liquidation !== null
        ? $this->rate_liquidation
        : (optional($this->group)->rate_liquidation ?? 0);
}
```

**Đổi lại:** vẫn phải sửa ~37 nơi gọi. Lợi ở chỗ sau này gỡ hẳn `group` thì chỉ sửa trong accessor.
⇒ **Đề xuất dùng cách này cho `Product.php` + các model**, còn controller thì `optional()` tại chỗ.

### 2.3 Thêm vào `Product.php`

| Việc | Chi tiết |
|---|---|
| `$fillable` | thêm `product_type_id`, `product_characteristic_id` — ERP còn tạo hàng hoá qua đường **hàng tạm** tới hết Phase 6; thiếu fillable thì `create()` **bỏ qua im lặng** |
| Quan hệ đọc cây mới | `product_type_ref()` · `product_characteristic()` |
| ⚠️ Đặt tên | **KHÔNG** đặt quan hệ tên `product_type()` — trùng cột chuỗi cũ đang dùng ở 77 chỗ, `$product->product_type` sẽ đổi nghĩa |

---

## 3. Còn 2 cột kia thì sao

| Cột | Rủi ro | Xử lý |
|---|---|---|
| `product_type` | **chuỗi**, không phải quan hệ ⇒ **không crash**. Nhưng `where('product_type','!=','service_product')` ở `SearchController` (4 hàm) làm hàng hoá **biến mất** (`NULL <> 'x'` → NULL → loại dòng) | Bỏ điều kiện đó (BB-6) |
| `product_cate` | chuỗi JSON, mọi chỗ lọc đều bọc `if (!empty($request->…))` ⇒ **không crash, không biến mất** | Không phải làm gì |

---

## 4. Thứ tự làm

1. **Trước khi bật màn HRM:**
   - `SearchController`: 11 chỗ `optional()` + bỏ 4 điều kiện `!= 'service_product'`
   - `Product.php`: 3 accessor + `$fillable` + 2 quan hệ
   - `BaseProduct.php`, `DeviceErrorController`, `TmpProductsController`, 2 model báo giá,
     `ProductSettingMailJob`, `MyTmpProductsController`, `ExportLargeProductList` — `optional()`
2. **Chặn route tạo/sửa hàng hoá ERP** (user làm)
3. **Rà `ProductsController`**: hàm chỉ-đọc nào còn được gọi từ ngoài thì cũng null-safe
   (⚫ `Product2Controller` bỏ qua — §1.4)

⚠️ **Khi chặn route, lưu ý 2 điểm:**
- Product2 **dùng chung quyền** `Thêm hàng hóa` / `Sửa hàng hóa` / `Xem hàng hóa` / `Xóa hàng hóa`
  ⇒ chặn bằng cách **bỏ quyền** sẽ chặn nhầm nó. Phải chặn **theo route** (`products/*`).
- 🐞 Tên route **`productDelete` bị khai TRÙNG 2 lần**: `routes/web.php:580` (ProductsController) và
  **:674** (Product2Controller). Laravel lấy bản khai **sau** ⇒ `route('productDelete')` hiện sinh ra
  URL **`/product2/{id}/delete`**, dù được gọi từ màn hàng hoá chính (`ProductsController:335,488`,
  `products/show.blade.php:33`). Chặn route mà không biết chuyện này sẽ chặn nhầm chỗ.
4. Cây cũ `JobCluster` — để Phase 5

---

## 5. Cách kiểm

Tạo **một** hàng hoá có `group_id = NULL` và `product_type = NULL` trên DB thử, rồi:

| # | Kiểm | Đạt khi |
|---|---|---|
| 1 | Mở **popup chọn hàng hoá** ở một màn bất kỳ, tìm đúng hàng hoá đó | popup **không nổ**, tìm thấy, cột Nhóm hiển thị trống |
| 2 | Mở popup ở màn có lọc giá (`price_type`) | không nổ ở nhánh `rate_liquidation` |
| 3 | Màn **Lỗi thiết bị** chọn hàng hoá đó | không nổ |
| 4 | Lập **báo giá thanh lý** với hàng hoá đó | không nổ, `rate_liquidation` về 0 |
| 5 | Chạy `ExportLargeProductList` | file xuất ra, cột Nhóm trống |
| 6 | Chạy job `ProductSettingMailJob` | không nổ |
| 7 | Duyệt **hàng tạm** tạo hàng hoá mới | vẫn tạo được |
| 8 | `grep -rn '\->group->' app | grep -v optional` trên các file ở §1.1 | **rỗng** |
