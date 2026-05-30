# Phase 29: Chiết khấu báo giá

> **Feature:** Bomlist-Quotation
> **Branch:** tpe-develop-assign
> **Ngày:** 2026-05-22

---

## 1. Tổng quan

Thêm chức năng chiết khấu (CK) trên báo giá với 2 phương thức:

| # | Phương thức | Mô tả |
|---|------------|-------|
| 1 | CK theo mặt hàng | Nhập CK trên từng dòng sản phẩm cha + dịch vụ bổ sung |
| 2 | CK theo tổng đơn hàng | Tạo các khoản CK từ danh mục → phân bổ về từng line |

- 1 báo giá chỉ áp dụng **1 trong 2** phương thức (hoặc không CK)
- Mỗi dòng có thể nhập **% hoặc giá trị**, hệ thống tính cái còn lại
- CK áp dụng **trước thuế** (VAT tính trên giá sau CK)
- Báo giá cũ mặc định = Không CK (không cần migration data)
- Chỉ sửa CK khi status=1 (Đang tạo)

Kèm theo: CRUD **Danh mục loại chiết khấu** (dùng chung, không phân quyền cấp)

---

## 2. Database

### 2.1 Bảng mới: `discount_types`

```php
Schema::create('discount_types', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->string('code', 30)->unique();
    $table->string('name');
    $table->tinyInteger('status')->default(1); // 1=Hoạt động, 2=Khoá, 3=Chờ duyệt
    $table->unsignedBigInteger('quotation_id')->nullable(); // Báo giá tạo nhanh (khi status=3)
    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->timestamps();
});
```

**Phân quyền:**
- Permission: `Quản lý danh mục loại chiết khấu` → toàn quyền CRUD + khoá/mở + duyệt
- User KHÔNG có quyền → chỉ thêm nhanh trên báo giá → status=3 (Chờ duyệt), gắn `quotation_id`
- Khi duyệt: status 3→1, `quotation_id` → null (áp dụng toàn hệ thống)
- API `getAll?quotation_id=X`: trả về status=1 + (status=3 AND quotation_id=X)

### 2.2 Bảng mới: `quotation_discounts`

Lưu các khoản CK khi báo giá chọn phương thức CK theo tổng.

```php
Schema::create('quotation_discounts', function (Blueprint $table) {
    $table->bigIncrements('id');
    $table->unsignedBigInteger('quotation_id');
    $table->unsignedBigInteger('discount_type_id');
    $table->enum('input_mode', ['percent', 'amount']);
    $table->decimal('percent_value', 10, 4)->nullable();
    $table->decimal('amount_value', 18, 2)->default(0);
    $table->integer('sort_order')->default(0);
    $table->unsignedBigInteger('created_by')->nullable();
    $table->unsignedBigInteger('updated_by')->nullable();
    $table->timestamps();

    $table->foreign('quotation_id')->references('id')->on('quotations')->onDelete('cascade');
    $table->foreign('discount_type_id')->references('id')->on('discount_types');
});
```

### 2.3 Alter: `quotations`

```php
$table->tinyInteger('discount_method')->nullable(); // null=Không CK, 1=Theo mặt hàng, 2=Theo tổng
$table->decimal('total_discount_amount', 18, 2)->default(0);
```

### 2.4 Alter: `quotation_product_prices`

```php
$table->string('discount_input_mode', 10)->nullable(); // 'percent' | 'amount'
$table->decimal('discount_percent', 10, 4)->default(0);
$table->decimal('discount_amount', 15, 2)->default(0);        // CK₫ trên 1 đơn vị (method=1)
$table->decimal('allocated_discount_amount', 18, 2)->default(0); // CK phân bổ (method=2)
```

### 2.5 Alter: `quotation_service_items`

Thêm cùng 4 cột tương tự `quotation_product_prices`:

```php
$table->string('discount_input_mode', 10)->nullable();
$table->decimal('discount_percent', 10, 4)->default(0);
$table->decimal('discount_amount', 15, 2)->default(0);
$table->decimal('allocated_discount_amount', 18, 2)->default(0);
```

---

## 3. Công thức tính

### 3.1 CK theo mặt hàng (discount_method = 1)

Áp dụng trên **dòng cha** (parent product) + **dịch vụ bổ sung**. Dòng con không có CK.

```
Nếu nhập %:
  CK(₫) = Giá bán × CK(%) / 100

Nếu nhập ₫:
  CK(%) = CK(₫) / Giá bán × 100

Đơn giá sau CK = Giá bán − CK(₫)
TT bán         = Đơn giá sau CK × SL
Tiền VAT       = TT bán × VAT%
TT sau VAT     = TT bán + Tiền VAT
```

**Khi user sửa giá bán:** hệ thống dựa vào `discount_input_mode` để tính lại:
- mode=percent → giữ %, tính lại ₫
- mode=amount → giữ ₫, tính lại %

### 3.2 CK theo tổng (discount_method = 2)

**Tính tổng CK:**

```
Mỗi khoản CK:
  Nếu mode=percent → amount_value = Tổng bán × percent_value / 100
  Nếu mode=amount  → amount_value = giá trị nhập

Tổng CK = Σ(quotation_discounts.amount_value)
```

**Phân bổ tự động (Largest Remainder Method):**

```
grand_sale = Σ(line_sale_total)  // tổng TT bán tất cả line

Bước 1: Mỗi line → raw = Tổng CK × (line_sale / grand_sale)
Bước 2: Mỗi line → allocated = floor(raw)
Bước 3: remainder = Tổng CK − Σ(allocated)
Bước 4: Sắp các line theo phần thập phân giảm dần
         → chia thêm 1₫ cho top N line (N = remainder)
```

**Phân bổ thủ công:**
- User sửa trực tiếp cột "CK phân bổ" trên từng line
- Thanh trạng thái: `Đã phân bổ: X / Y — Còn lại: Z`
- Xanh khi X = Y, đỏ khi X ≠ Y
- **Không cho submit** khi Σ(phân bổ) ≠ Tổng CK

**Khi user sửa giá bán sau khi đã phân bổ:**
- Tổng bán thay đổi → khoản CK tính theo % cũng thay đổi → Tổng CK thay đổi
- Cảnh báo: "Giá bán đã thay đổi, vui lòng phân bổ lại chiết khấu"
- Bắt buộc phân bổ lại trước khi submit
- Flag `needs_reallocation` (FE-only, không lưu DB)

**Công thức per-line (sau phân bổ):**

```
TT bán sau CK (line) = TT bán − allocated_discount_amount
Tiền VAT             = TT bán sau CK × VAT%
TT sau VAT           = TT bán sau CK + Tiền VAT
```

### 3.3 Tổng footer

```
Tổng nhập      = Σ(estimated_price × qty) — tất cả line + DV
Tổng bán       = Σ(TT bán trước CK)
Tổng CK        = Σ(CK) — tùy method
Tổng bán sau CK = Tổng bán − Tổng CK
Tỷ suất LN     = (Tổng bán sau CK − Tổng nhập) / Tổng nhập × 100
Tổng VAT       = Σ(Tiền VAT) — tính trên giá sau CK
Tổng sau VAT   = Tổng bán sau CK + Tổng VAT
```

- `total_after_vat` lưu DB = Tổng sau VAT (sau CK)
- Cấp duyệt (`price_approval_level`) tính trên Tổng sau VAT (sau CK)

---

## 4. API

### 4.1 Danh mục loại CK

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/assign/discount-types` | Danh sách (phân trang, search, filter status) |
| POST | `/assign/discount-types` | Tạo mới |
| PUT | `/assign/discount-types/{id}` | Cập nhật |
| DELETE | `/assign/discount-types/{id}` | Xóa (nếu chưa dùng) |
| POST | `/assign/discount-types/{id}/lock` | Khoá |
| POST | `/assign/discount-types/{id}/unlock` | Mở khoá |
| GET | `/assign/discount-types/active` | Lấy danh sách status=1 (cho select) |

### 4.2 Quotation — endpoint có sẵn mở rộng

| Endpoint | Thay đổi |
|----------|---------|
| `PUT /assign/quotations/{id}` | Nhận thêm `discount_method`, `line_discounts[]`, `quotation_discounts[]`, `line_allocations[]` |
| `GET /assign/quotations/{id}` | Trả thêm discount fields trên products, services, quotation_discounts |
| Export Excel | Thêm cột CK tương ứng method |
| Import Excel | Hỗ trợ cột CK% + CK₫ (method=1) |

### 4.3 Quotation — endpoint mới

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/assign/quotations/{id}/allocate-discount` | Phân bổ tự động CK tổng (BE tính Largest Remainder, trả về allocated per line) |

---

## 5. UI — Màn sửa Báo giá

### 5.1 Toolbar — Radio chọn phương thức CK

Đặt cùng toolbar với "Áp dụng VAT đồng loạt":

```
[Áp dụng VAT đồng loạt ▾]   ○ Không CK  ○ CK theo mặt hàng  ○ CK theo tổng
```

- Khi chuyển method mà đã có dữ liệu CK → confirm: "Thay đổi phương thức sẽ xóa dữ liệu chiết khấu hiện tại. Tiếp tục?"

### 5.2 Bảng sản phẩm — CK theo mặt hàng (method=1)

Thêm 3 cột sau "Giá bán":

| ... | Giá bán | **CK(%)** | **CK(₫)** | **Đơn giá sau CK** | TT bán | Tỷ suất LN | VAT% | ...
|-----|---------|-----------|-----------|---------------------|--------|-------------|------|

- Dòng CHA: cả 3 cột hiển thị, CK% + CK₫ editable (nhập 1 → tính cái kia)
- Dòng CON: 3 cột hiển thị "—"
- Dịch vụ bổ sung: tương tự dòng cha

### 5.3 Bảng sản phẩm — CK theo tổng (method=2)

Thêm 1 cột readonly sau "Giá bán":

| ... | Giá bán | **CK phân bổ** | TT bán | ...
|-----|---------|----------------|--------|

- Hiển thị `allocated_discount_amount` (editable khi phân bổ thủ công)
- Dòng con: "—"

### 5.4 Section CK tổng (method=2, dưới bảng sản phẩm)

```
┌─────────────────────────────────────────────────────────────────┐
│  CHIẾT KHẤU TỔNG ĐƠN HÀNG                                     │
│                                                                 │
│  | # | Loại CK (select)    | % / ₫ (toggle) | Giá trị | Thành tiền CK | ✕ │
│  | 1 | CK khách thân thiết | %               | 10      | 5,000,000     |   │
│  | 2 | CK đơn hàng lớn     | ₫               |         | 10,000,000    |   │
│  |   |                     |                 | TỔNG CK | 15,000,000    |   │
│                                                                 │
│  [+ Thêm khoản CK]  [+ Thêm nhanh loại CK]                    │
│                                                                 │
│  [Phân bổ tự động]  [Phân bổ lại]                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                  │
│  Đã phân bổ: 15,000,000 / 15,000,000 ✓                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                  │
└─────────────────────────────────────────────────────────────────┘
```

- "Thêm nhanh loại CK": inline form nhập mã + tên → tạo vào `discount_types` luôn
- Select loại CK: chỉ hiện status=1 (Mở)

### 5.5 Footer tổng

```
Tổng nhập | Tổng bán | Tổng CK | Tổng bán sau CK | Tỷ suất LN | Tổng VAT | Tổng sau VAT
```

- Tổng CK + Tổng bán sau CK: chỉ hiện khi method ≠ null
- Khi không CK: ẩn 2 cột này, giữ layout như hiện tại

---

## 6. Danh mục loại CK — CRUD

### 6.1 Menu

Danh mục → Danh mục loại chiết khấu (`/assign/discount-types`)

### 6.2 Danh sách

- V2Base list page chuẩn
- Cột: STT | Mã | Tên | Trạng thái | Thao tác
- Filter: search (mã + tên), trạng thái
- Thao tác: Sửa, Khoá/Mở, Xóa (nếu chưa dùng trong báo giá nào)

### 6.3 Form tạo/sửa

- Modal hoặc inline (theo convention V2Base)
- Fields: Mã (required, unique), Tên (required)
- Trạng thái: mặc định Mở khi tạo

---

## 7. Export / Import Excel

### 7.1 Export

- Method=1: thêm 3 cột CK(%), CK(₫), Đơn giá sau CK vào sau Giá bán
- Method=2: thêm 1 cột CK phân bổ + section tóm tắt khoản CK tổng ở cuối
- Method=null: giữ nguyên format hiện tại

### 7.2 Import (method=1)

- Template thêm 2 cột: CK(%), CK(₫) — user nhập 1 trong 2
- Validate: CK ≥ 0, CK(₫) ≤ Giá bán
- Nếu nhập cả 2: ưu tiên CK(₫), tính lại %

---

## 8. Lịch sử báo giá

Ghi chi tiết vào `quotation_histories` với action + meta:

| Action | Meta |
|--------|------|
| `update_discount_method` | `{ from: null, to: 1 }` |
| `update_line_discounts` | `{ changes: [{ product_id, old_percent, new_percent, old_amount, new_amount }] }` |
| `update_total_discounts` | `{ added: [...], removed: [...], changed: [...] }` |
| `allocate_discount` | `{ mode: 'auto'|'manual', allocations: [{ line_id, amount }] }` |

---

## 9. Edge cases

1. **Giá bán = 0**: CK(%) không thể tính → chỉ cho nhập CK(₫) = 0
2. **CK(₫) > Giá bán**: Validate không cho nhập (CK tối đa = Giá bán, đơn giá sau CK ≥ 0)
3. **Tất cả line TT bán = 0**: Phân bổ CK tổng không thể chia theo tỷ trọng → cảnh báo yêu cầu nhập giá bán trước
4. **Xóa sản phẩm/dịch vụ khi đã phân bổ CK tổng**: Invalidate phân bổ → yêu cầu phân bổ lại
5. **Thêm khoản CK tổng khi đã phân bổ**: Invalidate → yêu cầu phân bổ lại
6. **Báo giá cũ (trước migration)**: `discount_method = null`, tất cả CK fields = 0 → hoạt động bình thường
