# Hợp đồng tương thích ERP — điều kiện để Phase 2 được coi là XONG

> **Mục tiêu user chốt 21/09/2026:**
> *"Quản lý giá, duyệt giá, tính giá bán sẽ chuyển đổi dần. Chuyển hàng hoá thực hiện trước.
> Mục tiêu quan trọng là phải đảm bảo ERP vẫn chạy ổn định sau khi chuyển hàng hoá sang HRM."*
>
> ⇒ Tiêu chí nghiệm thu Phase 2 **không phải** "màn HRM đẹp và chạy" mà là
> **"ERP không vỡ chỗ nào"**. Tài liệu này là danh sách bất biến + cách kiểm.

---

## 0. Bối cảnh: cái gì ở lại ERP trong Phase 2

| Ở lại ERP (Phase 2 không đụng) | Chuyển sang HRM ngay |
|---|---|
| Quản lý giá · **Duyệt giá** · Tính giá bán | Màn danh sách + tạo/sửa hàng hoá |
| Kho · Mua hàng · Bán hàng · Bảo hành · Kế toán | |
| Hàng hoá gốc · Hàng hoá có sẵn · Đồng bộ hàng hoá | |
| Hàng tạm (Phase 6) | |

⇒ **Form hàng hoá của HRM vẫn phải làm đúng phần GIÁ** — vì tab Giá bán nằm trên form, mà luồng
duyệt giá thì ở lại ERP.

---

## 1. SÁU BẤT BIẾN — hỏng cái nào là ERP vỡ

### BB-1 🔴 Sửa giá phải đi qua LUỒNG DUYỆT, không ghi thẳng

**ERP đang làm gì:** trong `ProductsController@update`, đường ghi giá **trực tiếp đã bị comment tắt**
(dòng 1565–1635). Đường đang chạy tách 2 nhánh theo cờ `$is_approve`:

```php
if ($is_approve) {
    $unit->flag_price_wait_approve   = 1;
    $unit->price_wait_approve        = $u['cost_price'];
    $unit->coefficient_wait_approve  = $u['unit_coefficient'];
    $unit->save();
    $approves[$unit->id] = [ ... ];      // dựng phiếu duyệt giá
} else {
    $unit->cost_price      = $u['cost_price'];
    $unit->unit_coefficient = $u['unit_coefficient'];
    $unit->save();
}
```

**`$is_approve` tính theo cấu hình CÔNG TY** (`ProductsController:1374-1388`):

```
is_approve = companies.is_new_company
             AND ( companies.is_new_brand
                   OR manufacture_id ∈ companies.new_brand_ids )
```

**Đo thực tế:** **1/8 công ty** đang bật (`#8 CÔNG TY CỔ PHẦN ĐẦU TƯ T…`, `is_new_company=true`,
`is_new_brand=true`). `product_approves` hiện **0 dòng** — cơ chế đang bật nhưng chưa phát sinh phiếu.

**Hỏng thì sao:** HRM ghi thẳng `cost_price`/`price` ⇒ **giá đổi mà không ai duyệt**. Đây là lỗ hổng
kiểm soát, không phải lỗi hiển thị. Màn "Duyệt giá hàng hoá" của ERP cũng mất việc.

**Phải làm:** port **nguyên văn** cả điều kiện `$is_approve` lẫn 2 nhánh ghi, kể cả việc dựng bản
ghi `$approves[]`.

### BB-2 🔴 Không có quyền `Quản lý giá` thì KHÔNG đụng gì tới giá

**ERP đang làm gì:** toàn bộ khối xử lý giá nằm trong `if (Auth::user()->can('Quản lý giá'))`
(`ProductsController:1547`). Người không có quyền sửa hàng hoá thì **giá giữ nguyên**.

**Hỏng thì sao:** HRM bỏ điều kiện này ⇒ người không có quyền giá vẫn ghi đè giá khi lưu hàng hoá —
**mất giá âm thầm**, và trái quy tắc fail-closed của CLAUDE.md.

### BB-3 🟡 Mã hàng hoá sinh đúng khuôn + chịu được va chạm

- Port `Product::generateCode()` **nguyên văn**: `MÃ-HÃNG-SX + '-' + (tên barcode | tên model)`,
  cắt 32 ký tự, chống trùng bằng hậu tố `:01`, `:02`.
- **17% mã (7.928/45.890)** đã phải thêm hậu tố ⇒ va chạm là chuyện thường.
- `products.code` có UNIQUE ⇒ bắt `QueryException` 23000 rồi **sinh lại mã và thử lại** (3–5 lần).

**Hỏng thì sao:** mã sai khuôn thì nhìn ra ngay (`TP.0012345` vs `CH-RRI32`); không retry thì người
dùng gặp `Duplicate entry` giữa lúc bấm Lưu.

### BB-4 🟡 Ghi ĐỦ bảng vệ tinh — ERP đọc từ đó

| Bảng | ERP đọc ở đâu |
|---|---|
| `product_units` | **119 file / 453 chỗ** |
| `product_unit_prices` | 41 file |
| `product_expected_prices` | giá theo thời gian, 2.495 dòng còn ở tương lai |
| `attribute_products` | thông số cơ bản, 51.128 dòng |
| `product_suppliers` · `product_company_coefficients` | |
| `product_tech_attachments` · `product_galleries` · `product_videos` | |
| 4 bảng hàng hoá kèm (`recipe_products` 6.438 · `product_has_accessories` 989 · `..._install_` 28 · `..._repair_` 5) | |

**Hỏng thì sao:** thiếu bảng nào thì màn ERP đọc bảng đó hiện trống — im lặng, không lỗi.

### BB-5 🟡 Audit `updated_by` ở MỌI đường ghi

`products.updated_by` có giá trị ở **45.889/45.890** dòng. `Product` của ERP **không**
`extends BaseModel` ⇒ HRM phải **tự gán**: tạo · sửa · **khoá / mở khoá** (chỗ hay quên nhất).
Dùng `auth()->id()` (= `employees.id`), **không** dùng `auth()->user()->info->id`.

### BB-6 🔴 `product_type` không được để trống — hoặc phải sửa `SearchController` TRƯỚC

`SearchController` có dòng lọc **vô điều kiện** ở cả 4 hàm:

```php
$products = $products->where('product_type', '!=', 'service_product');
```

`NULL <> 'x'` trong SQL cho ra **NULL**, mà `WHERE NULL` thì **loại bỏ dòng**.

⇒ Hàng hoá tạo từ HRM có `product_type` trống sẽ **biến mất khỏi popup chọn hàng của 338 màn**.

**Hai cách, phải chọn 1 trước khi bật màn HRM:**
- (a) sửa `SearchController` bỏ 2 điều kiện lọc theo enum cũ *(đã đề xuất, chờ khách xác nhận —
  nới lỏng hành vi: 30 hàng dịch vụ lọt vào popup, báo giá dịch vụ chọn được 45.890 thay vì 12.426)*
- (b) HRM tạm điền `product_type` bằng một giá trị mặc định cho tới khi (a) xong

⚠️ Chưa làm (a) hoặc (b) mà đã cho tạo hàng hoá từ HRM = **hàng hoá mới vô hình với cả hệ thống**.

---

## 2. Điểm cần lưu ý thêm

**Phiếu duyệt giá chụp ảnh 2 cột sắp trống.** `$approves[]` lưu kèm `product_type` và `product_cate`
(`ProductsController:1670-1671`) — hai cột mà HRM sẽ để trống theo quyết định 3 và 6. Phiếu duyệt
giá sinh ra từ HRM sẽ thiếu 2 trường đó. Cần chốt: bỏ khỏi phiếu, hay điền bằng dữ liệu cây mới.

**Không đổi ngữ nghĩa bất kỳ cột nào** ERP đang đọc — `products` có **171 bảng** tham chiếu. Phase 2
chỉ **thêm** cột, không sửa/không đổi ý nghĩa cột cũ.

---

## 3. Kịch bản nghiệm thu — "ERP không vỡ"

Làm trên dữ liệu thật, đo bằng số, **trước khi bật màn HRM cho người dùng**.

### 3.1 Tạo hàng hoá từ HRM rồi kiểm ở ERP

| # | Kiểm | Đạt khi |
|---|---|---|
| 1 | Mở màn danh sách hàng hoá ERP | thấy hàng hoá mới, đúng mã khuôn `XX-YYYY` |
| 2 | Mở **popup tìm hàng hoá** ở một màn bất kỳ trong 338 màn | **tìm thấy** hàng hoá mới (đây là BB-6) |
| 3 | Mở màn Sửa hàng hoá ở ERP | mọi tab hiện đủ dữ liệu HRM đã nhập |
| 4 | Lập báo giá / phiếu xuất kho có hàng hoá mới | chọn được, giá đúng |
| 5 | Cột **Người tạo / Người cập nhật** | ra đúng tên (BB-5) |

### 3.2 Sửa GIÁ từ HRM

| # | Kiểm | Đạt khi |
|---|---|---|
| 6 | Sửa giá hàng hoá thuộc **công ty có `is_new_company = true`** | giá **KHÔNG** đổi ngay; sinh bản ghi chờ duyệt (`flag_price_wait_approve = 1`) |
| 7 | Mở màn **Duyệt giá hàng hoá** của ERP | thấy phiếu vừa tạo |
| 8 | Bấm Duyệt ở ERP | giá mới áp dụng, cờ về 0 |
| 9 | Sửa giá hàng hoá thuộc công ty **không** bật duyệt | giá đổi ngay |
| 10 | Đăng nhập tài khoản **không có quyền `Quản lý giá`**, sửa hàng hoá | giá **giữ nguyên** (BB-2) |

### 3.3 Không hồi quy

| # | Kiểm | Đạt khi |
|---|---|---|
| 11 | Chụp số dòng 12 bảng hàng hoá trước/sau đợt kiểm | chỉ tăng đúng số bản ghi vừa tạo |
| 12 | `SELECT COUNT(*) FROM products WHERE code IS NULL OR code = ''` | **0** |
| 13 | Kiểm mã trùng: `GROUP BY code HAVING COUNT(*) > 1` | **0** |
| 14 | Tạo 2 hàng hoá **cùng lúc** từ HRM và ERP, cùng hãng + model | cả hai lưu được, mã khác nhau (BB-3) |

---

## 4. Thứ tự đề xuất

1. **Trước khi bật màn HRM:** chốt và làm xong BB-6 (sửa `SearchController`).
2. **Phase 2:** màn hàng hoá HRM, port đủ BB-1 → BB-5. Giá vẫn đi qua luồng duyệt của ERP.
3. **Sau Phase 2:** lần lượt chuyển Quản lý giá → Duyệt giá → Tính giá (Phase 7). Mỗi lần chuyển
   xong thì **khoá đường ghi tương ứng bên ERP** (gỡ route / bỏ quyền), không để hai nơi cùng ghi.
4. **Phase 6** (hàng tạm) — sau đó ERP mới thực sự chỉ-đọc.
