# Design Phase 30: Báo giá tự xây dựng (Standalone Quotation)

## Mục tiêu

Cho phép tạo báo giá trực tiếp không qua YCBG/BOM. User tự xây dựng danh sách hàng hoá và dịch vụ trên form báo giá, theo pattern giống tạo BOM (chọn từ ERP + thêm nhanh, cha-con, nhóm hàng).

## Scope

### Làm:
- Thêm loại báo giá `type=2` (standalone) bên cạnh `type=1` (BOM-based)
- Tạo báo giá standalone trực tiếp từ trang danh sách (không cần YCBG)
- CRUD hàng hoá trực tiếp trên form báo giá (thêm/sửa/xoá, cha-con, nhóm hàng)
- Bắt buộc gắn Dự án TKT, Giải pháp tuỳ chọn
- Export/Import Excel gồm cả thông tin SP + giá

### Không làm:
- Không tạo bảng mới — mở rộng `quotation_product_prices`
- Không tạo permission riêng
- Không thay đổi flow BOM-based hiện tại

## Phương án đã chọn

**Phương án A: Mở rộng `quotation_product_prices`** — thêm cột metadata trực tiếp. Khi standalone thì `bom_list_product_id = null`, product info lưu trên chính bảng này. Khi BOM-based thì các cột metadata giữ null (lấy từ BOM như cũ).

---

## 1. Database

### 1.1 Migration: Alter `quotations`

```sql
ALTER TABLE quotations
  ADD COLUMN type TINYINT NOT NULL DEFAULT 1 COMMENT '1=BOM-based, 2=Standalone';

-- Nullable hoá các FK không cần cho standalone
ALTER TABLE quotations MODIFY bom_list_id BIGINT UNSIGNED NULL;
ALTER TABLE quotations MODIFY pricing_request_id BIGINT UNSIGNED NULL;
ALTER TABLE quotations MODIFY solution_id BIGINT UNSIGNED NULL;
ALTER TABLE quotations MODIFY solution_version_id BIGINT UNSIGNED NULL;

-- Drop unique constraint pricing_request_id (standalone không có)
ALTER TABLE quotations DROP INDEX quotations_pricing_request_id_unique;
ALTER TABLE quotations ADD INDEX quotations_pricing_request_id_index (pricing_request_id);

-- Backfill
UPDATE quotations SET type = 1 WHERE type IS NULL;
```

Giữ bắt buộc: `project_id`, `customer_id`, `currency_id`, `code`.

### 1.2 Migration: Alter `quotation_product_prices`

```sql
-- Nullable hoá BOM FK
ALTER TABLE quotation_product_prices MODIFY bom_list_product_id BIGINT UNSIGNED NULL;

-- Drop unique constraint, thay bằng index thường
ALTER TABLE quotation_product_prices
  DROP INDEX quotation_product_prices_quotation_id_bom_list_product_id_unique;
ALTER TABLE quotation_product_prices
  ADD INDEX qpp_quotation_bom_product_idx (quotation_id, bom_list_product_id);

-- Product metadata (chỉ dùng khi standalone)
ALTER TABLE quotation_product_prices
  ADD COLUMN erp_product_id BIGINT UNSIGNED NULL AFTER bom_list_product_id,
  ADD COLUMN code VARCHAR(100) NULL AFTER erp_product_id,
  ADD COLUMN name VARCHAR(500) NULL AFTER code,
  ADD COLUMN product_attributes TEXT NULL AFTER name,
  ADD COLUMN model_id BIGINT UNSIGNED NULL AFTER product_attributes,
  ADD COLUMN brand_id BIGINT UNSIGNED NULL AFTER model_id,
  ADD COLUMN origin_id BIGINT UNSIGNED NULL AFTER brand_id,
  ADD COLUMN unit_id BIGINT UNSIGNED NULL AFTER origin_id,
  ADD COLUMN qty DECIMAL(16,2) NOT NULL DEFAULT 1 AFTER unit_id,
  ADD COLUMN parent_id BIGINT UNSIGNED NULL AFTER qty,
  ADD COLUMN group_name VARCHAR(255) NULL AFTER parent_id,
  ADD COLUMN group_sort_order INT NOT NULL DEFAULT 0 AFTER group_name,
  ADD COLUMN product_type TINYINT NOT NULL DEFAULT 1 COMMENT '1=Hàng hoá, 2=Dịch vụ' AFTER group_sort_order,
  ADD COLUMN sort_order INT NOT NULL DEFAULT 0 AFTER product_type;

-- Index
ALTER TABLE quotation_product_prices ADD INDEX qpp_parent_id_idx (parent_id);
```

### 1.3 Không tạo bảng mới

Reuse toàn bộ: `quotation_service_items`, `quotation_discounts`, `quotation_histories`.

---

## 2. Backend

### 2.1 Model `Quotation`

```php
const TYPE_BOM_BASED = 1;
const TYPE_STANDALONE = 2;

// Relationship bomList() giữ nguyên — nullable cho standalone
// Thêm scope
public function scopeStandalone($query) {
    return $query->where('type', self::TYPE_STANDALONE);
}

public function scopeBomBased($query) {
    return $query->where('type', self::TYPE_BOM_BASED);
}
```

### 2.2 Model `QuotationProductPrice`

Thêm relationships:
```php
public function tpModel()    { return $this->belongsTo(TpModel::class, 'model_id'); }
public function tpBrand()    { return $this->belongsTo(TpBrand::class, 'brand_id'); }
public function tpOrigin()   { return $this->belongsTo(TpOrigin::class, 'origin_id'); }
public function tpUnit()     { return $this->belongsTo(TpUnit::class, 'unit_id'); }
public function erpProduct() { return $this->belongsTo(TpProduct::class, 'erp_product_id'); }
public function parent()     { return $this->belongsTo(self::class, 'parent_id'); }
public function children()   { return $this->hasMany(self::class, 'parent_id'); }
```

Thêm casts + accessors tương tự `BomListProduct` (import_total, sale_total).

### 2.3 Endpoint tạo báo giá standalone

```
POST /api/v1/assign/quotations/standalone
```

Request body:
```json
{
  "project_id": 123,
  "solution_id": null,
  "solution_version_id": null,
  "solution_module_id": null,
  "solution_module_version_id": null,
  "currency_id": 1,
  "description": "Mô tả"
}
```

Logic:
1. Validate `project_id` tồn tại
2. Lấy customer info từ dự án TKT (snapshot: customer_id, customer_code, customer_name, customer_tax_code, customer_address, customer_contact_name, customer_contact_phone, customer_email)
3. Auto-gen code `BG-YYYY-NNNNN` (giống BOM-based)
4. Tạo quotation: `type=2`, `bom_list_id=null`, `pricing_request_id=null`, `status=DANG_TAO`
5. Return `{ id, code }` → FE redirect

### 2.4 CRUD sản phẩm trên quotation standalone

Chỉ hoạt động khi `quotation.type = TYPE_STANDALONE` và `status = STATUS_DANG_TAO`.

#### POST `/quotations/{id}/products` — Thêm sản phẩm

2 mode:

**Mode 1 — Chọn từ ERP** (`erp_product_id` có giá trị):
```json
{
  "erp_product_id": 456,
  "qty": 10,
  "parent_id": null,
  "group_name": "Thiết bị mạng",
  "product_type": 1
}
```
BE tự copy: code, name, model_id, brand_id, origin_id, unit_id, product_attributes từ ERP record.

**Mode 2 — Thêm nhanh** (`erp_product_id = null`):
```json
{
  "code": "SP-001",
  "name": "Switch Cisco 24 port",
  "model_id": 1,
  "brand_id": 2,
  "origin_id": 3,
  "unit_id": 4,
  "qty": 5,
  "product_attributes": "<p>Layer 3</p>",
  "parent_id": null,
  "group_name": "Thiết bị mạng",
  "product_type": 1,
  "estimated_price": 5000000
}
```
Auto-create model/brand/origin/unit trên ERP DB nếu chưa có (giống BOM import).

**Batch mode**: Cho phép gửi array `products[]` để thêm nhiều SP cùng lúc.

#### PUT `/quotations/{id}/products/{productId}` — Sửa

Sửa thông tin SP + giá. Chỉ sửa được SP thuộc quotation này.

#### DELETE `/quotations/{id}/products/{productId}` — Xoá

Cascade xoá tất cả children. Recompute totals sau khi xoá.

### 2.5 Service: Cập nhật logic tính toán

6 method cần thêm nhánh standalone:

#### `computeTotals(Quotation $quotation)`
```php
if ($quotation->type === Quotation::TYPE_STANDALONE) {
    $products = $quotation->productPrices()->get();
    // Build parent-child map từ quotation_product_prices.parent_id
    $childrenMap = $products->whereNotNull('parent_id')->groupBy('parent_id');
    $parents = $products->whereNull('parent_id');
    // qty lấy từ quotation_product_prices.qty (thay vì bom_list_products.qty_needed)
} else {
    // Giữ nguyên logic hiện tại — đọc từ bom_list_products
}
// Phần tính tổng (sale, vat, discount) — dùng chung
```

#### `upsertPrices(Quotation $quotation, array $products)`
- Standalone: update trực tiếp `quotation_product_prices` (không cần map `bom_list_product_id`)
- Key match bằng `id` thay vì `bom_list_product_id`

#### `applyBulkVat(Quotation $quotation, ...)`
- Standalone: lấy danh sách cha/orphan từ `quotation_product_prices.parent_id` thay vì `bom_list_products`

#### `calculateTotals(Quotation $quotation)`
- Standalone: skip logic đọc `bomList->products`, dùng `productPrices` trực tiếp

#### `recomputeUnitPriceAfterDiscount(Quotation $quotation)`
- Standalone: parent check từ self-ref `parent_id`

#### `allocateDiscount(Quotation $quotation)`
- Không thay đổi lớn — đã dùng `productPrices` + `serviceItems` trực tiếp

### 2.6 Resource (API response)

`DetailQuotationResource` cập nhật:
- Standalone: mỗi product trả kèm metadata (code, name, model, brand, origin, unit, qty, parent_id, group_name, product_type, sort_order)
- BOM-based: giữ nguyên (metadata lấy từ BOM relationship)

### 2.7 Export / Import Excel

**Export**:
- Standalone: lấy product info từ `quotation_product_prices` trực tiếp
- Template output giống nhau (cùng format cột)

**Import**:
- Standalone: import cả thông tin SP + giá (parse STT cha-con, nhóm hàng, tạo `quotation_product_prices` rows)
- BOM-based: giữ nguyên (chỉ import giá)

### 2.8 Validation

- Submit: ≥1 sản phẩm cha/orphan phải có `quoted_price > 0` và `qty > 0`
- CRUD product: chỉ khi `type=2` + `status=1`
- Type không cho thay đổi sau khi tạo

### 2.9 Lịch sử

Thêm 3 action mới trong `quotation_histories`:
- `add_product` — kèm metadata SP vừa thêm
- `remove_product` — kèm metadata SP vừa xoá
- `update_product` — kèm diff thay đổi

### 2.10 Giữ nguyên (không thay đổi)

- Workflow duyệt (submit → TP → BGĐ)
- Chiết khấu (cả 2 method: per-item + tổng)
- Dịch vụ bổ sung (CRUD giữ nguyên)
- In báo giá (đã dùng data từ quotation)
- Cấu hình duyệt giá

---

## 3. Frontend

### 3.1 Trang danh sách `/assign/quotations/index.vue`

- Thêm button **"Tạo báo giá"** (icon `ri-add-line`) trên toolbar
- Click → mở modal tạo (không trang riêng):
  - Dự án TKT (bắt buộc, cascading từ Công ty)
  - Giải pháp (tuỳ chọn, filter theo dự án)
  - Loại tiền tệ (bắt buộc, default VND)
  - Mô tả (tuỳ chọn)
- Submit → `POST /quotations/standalone` → redirect `/quotations/{id}/edit`
- Thêm cột **"Loại BG"** (Kế thừa BOM / Tự xây dựng)
- Thêm filter **Loại BG** (select 2 option)
- BOM-based: cột BOM hiện tên + link. Standalone: hiện "—"

### 3.2 Trang edit `/assign/quotations/_id/edit.vue`

#### Điều kiện: `quotation.type === 2`

**Header info**:
- Ẩn: trường BOM, YCBG
- Giữ: Mã BG, Dự án, Giải pháp (nếu có), Khách hàng (snapshot), Loại tiền tệ, Hiệu lực, Giao hàng, Bảo hành

**Bảng sản phẩm — editable mode**:

| Tính năng | BOM-based (giữ nguyên) | Standalone |
|-----------|----------------------|------------|
| Toolbar | Chỉ VAT + CK + Làm tròn | + "Chọn hàng hoá" + "Thêm nhanh" + "Thêm nhóm" |
| Thêm SP | Không | Chọn ERP / Thêm nhanh (reuse BOM pattern) |
| Xoá SP | Không | Nút xoá per row (cascade con) |
| Sửa thông tin | Không | Inline: tên, mã, SL, ĐVT, TSKT |
| Sửa giá | Giá nhập + Giá bán | Giá nhập + Giá bán (giống) |
| Nhóm hàng | Readonly | Thêm/xoá/đổi tên nhóm |
| Cha-con | Readonly | "Thêm con" per row |
| Import | Chỉ giá | SP + giá |
| Kéo thả | Không | Đổi thứ tự (reuse BOM) |

**Reuse components từ BOM**:
- Modal thêm nhanh SP (adapt API endpoint)
- Modal chọn từ ERP (adapt API endpoint)
- Logic nhóm hàng (group row rendering)
- Logic cha-con (expand/collapse, thêm con)

**Dịch vụ bổ sung, CK, footer tổng, toolbar giá**: giữ nguyên cho cả 2 type.

### 3.3 Trang view `/assign/quotations/_id/index.vue`

- Ẩn BOM/YCBG khi standalone
- Hiển thị sản phẩm readonly (giống hiện tại)
- Không thay đổi lớn

### 3.4 In báo giá

- Không thay đổi — đã dùng data từ quotation
- Standalone: ẩn mục BOM trên bản in

---

## 4. Ràng buộc & Edge cases

1. **Type lock**: Không cho chuyển type sau khi tạo
2. **CRUD SP lock**: Chỉ khi `status = DANG_TAO` (1) + `type = STANDALONE` (2)
3. **Xoá cha cascade con**: Confirm modal trước khi xoá
4. **Dữ liệu cũ**: Backfill `type=1`, không ảnh hưởng flow cũ
5. **Permission**: Không cần permission riêng cho standalone
6. **Validate submit**: ≥1 SP cha/orphan có `quoted_price > 0`
7. **Xoá quotation standalone**: Cho phép khi `status = DANG_TAO` (giống BOM-based)
