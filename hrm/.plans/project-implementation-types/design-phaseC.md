# Phase C — Báo giá trực tiếp (không GP, không BOM)

## Mục tiêu

Dự án Type 1 (Tự triển khai) bỏ hẳn bước tạo Giải pháp + BOM. KD tạo báo giá trực tiếp từ tab "Báo giá" trên Dự án TKT, với form gộp: vừa quản lý sản phẩm (thêm/xóa/nhóm/parent-child) vừa nhập giá — 1 bước duy nhất.

## Phạm vi

- Chỉ áp dụng dự án `implementation_type = 1` (SELF)
- Báo giá cũ (đã có `bom_list_id`) vẫn hoạt động bình thường
- Báo giá mới Type 1 đi luồng không BOM

## Quyết định thiết kế

| # | Quyết định | Lý do |
|---|-----------|-------|
| 1 | `bom_list_id` nullable trên `quotations` | Báo giá mới Type 1 không có BOM |
| 2 | Mở rộng `quotation_product_prices` thay vì tạo bảng riêng | Nhanh implement, product data luôn ở 1 chỗ |
| 3 | Tạo bảng `quotation_groups` | Groups cho báo giá không BOM |
| 4 | Form gộp 1 bước (sản phẩm + giá) | KD thao tác nhanh, không cần qua BOM |
| 5 | Ẩn tab GP + BOM cho Type 1 | Luồng mới thay thế hoàn toàn luồng cũ |
| 6 | Backward compatible | Báo giá cũ có `bom_list_id` vẫn hoạt động |

---

## DB Changes

### 1. Alter `quotations` — `bom_list_id` nullable

```sql
ALTER TABLE quotations MODIFY bom_list_id BIGINT UNSIGNED NULL;
```

Khi tạo báo giá trực tiếp (Type 1): `bom_list_id = NULL`, `solution_id = NULL`, `solution_version_id = NULL`, `solution_module_id = NULL`, `solution_module_version_id = NULL`.

### 2. Alter `quotation_product_prices` — thêm product fields + `bom_list_product_id` nullable

```sql
ALTER TABLE quotation_product_prices 
  MODIFY bom_list_product_id BIGINT UNSIGNED NULL;

ALTER TABLE quotation_product_prices
  ADD COLUMN quotation_group_id INT UNSIGNED NULL AFTER bom_list_product_id,
  ADD COLUMN parent_id BIGINT UNSIGNED NULL AFTER quotation_group_id,
  ADD COLUMN product_type TINYINT NOT NULL DEFAULT 1 AFTER parent_id COMMENT '1=Hàng hoá, 2=Dịch vụ',
  ADD COLUMN erp_product_id BIGINT UNSIGNED NULL AFTER product_type,
  ADD COLUMN code VARCHAR(255) NULL AFTER erp_product_id,
  ADD COLUMN name VARCHAR(255) NULL AFTER code,
  ADD COLUMN model_id BIGINT UNSIGNED NULL AFTER name,
  ADD COLUMN brand_id BIGINT UNSIGNED NULL AFTER model_id,
  ADD COLUMN origin_id BIGINT UNSIGNED NULL AFTER brand_id,
  ADD COLUMN unit_id BIGINT UNSIGNED NULL AFTER origin_id,
  ADD COLUMN qty_needed DOUBLE DEFAULT 0 AFTER unit_id,
  ADD COLUMN product_attributes TEXT NULL AFTER qty_needed,
  ADD COLUMN sort_order INT DEFAULT 0 AFTER product_attributes;
```

**Logic xác định nguồn product data:**
- Nếu `bom_list_product_id IS NOT NULL` → lấy từ relation `bomListProduct` (báo giá từ BOM, luồng cũ)
- Nếu `bom_list_product_id IS NULL` → lấy trực tiếp từ các field mới trên `quotation_product_prices` (báo giá trực tiếp)

**Unique constraint:** Cần drop unique cũ `uq_quotation_product` (vì `bom_list_product_id` nullable). Thay bằng index thường:
```sql
ALTER TABLE quotation_product_prices DROP INDEX uq_quotation_product;
ALTER TABLE quotation_product_prices ADD INDEX idx_quotation_bom_product (quotation_id, bom_list_product_id);
```

### 3. Tạo bảng `quotation_groups`

```sql
CREATE TABLE quotation_groups (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  quotation_id BIGINT UNSIGNED NOT NULL,
  name VARCHAR(255) NOT NULL,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL,
  INDEX idx_quotation_groups_quotation (quotation_id)
);
```

---

## BE Changes

### 1. QuotationService — method `createDirect(ProspectiveProject $project): Quotation`

Tạo báo giá trống (không có BOM, không có products):

```
- Validate: project.implementation_type === 1
- Validate: project.status >= STATUS nào đó (cần xác nhận)
- Quotation::create({
    pricing_request_id: null,
    bom_list_id: null,
    project_id: project.id,
    solution_id: null, solution_version_id: null, ...
    customer snapshot từ project,
    status: DANG_TAO,
    code: getNextCode(),
  })
- Log history ACTION_CREATE
- Return quotation
```

### 2. QuotationService — sửa `upsertPrices()` 

Hiện tại `upsertPrices` phụ thuộc `$quotation->bomList->products()` để validate. Cần xử lý 2 case:

**Case 1 — Báo giá có BOM** (luồng cũ): Giữ nguyên logic hiện tại, products chỉ update giá, không thêm/xóa.

**Case 2 — Báo giá không BOM**: 
- FE gửi full danh sách products (bao gồm: name, code, qty, unit_id, erp_product_id, parent_id, quotation_group_id, product_type, estimated_price, quoted_price, vat_percent, discount fields)
- BE xóa products cũ + insert lại (replace-all strategy, giống BOM import)
- Hoặc: sync incremental (updateOrCreate bằng price_id nếu có, create nếu mới, delete nếu không gửi lên)

**Recommend:** Sync incremental — FE gửi `price_id` cho row đã tồn tại, `null` cho row mới. BE:
1. Collect tất cả `price_id` FE gửi lên
2. Delete records có `quotation_id` match nhưng `id` không nằm trong list
3. UpdateOrCreate từng row

### 3. QuotationService — sửa `recomputeTotals()`

Hiện tại dựa vào `bomList->products` để tính. Cần xử lý case không BOM:
- Nếu `bom_list_id IS NOT NULL` → logic cũ
- Nếu `bom_list_id IS NULL` → đọc trực tiếp từ `quotation_product_prices` (dùng các field mới: qty_needed, parent_id...)

### 4. Route + Controller

```php
// Route mới
Route::post('/create-direct', [QuotationController::class, 'createDirect']);

// Controller
public function createDirect(Request $request)
{
    $projectId = $request->input('project_id');
    $project = ProspectiveProject::findOrFail($projectId);
    $quotation = $this->quotationService->createDirect($project);
    return $this->responseJson(new DetailQuotationResource($quotation));
}
```

### 5. DetailQuotationResource — xử lý 2 nguồn data

Hiện tại load products qua `QuotationProductPrice → bomListProduct`. Cần:
- Nếu `bom_list_id` có → logic cũ (load qua bomListProduct)
- Nếu `bom_list_id` null → đọc trực tiếp từ `quotation_product_prices` fields mới
  - `model_name`, `brand_name`, `origin_name`, `unit_name` → resolve từ TpModel/TpBrand/TpOrigin/TpUnit qua `model_id`/`brand_id`/`origin_id`/`unit_id`
- Groups: nếu có BOM → load từ `bom_list_groups`, không BOM → load từ `quotation_groups`

### 6. Export Excel — xử lý báo giá không BOM

`QuotationController::exportExcel()` hiện tại load `$quotation->bomList->products`. Cần fallback:
- Nếu `bom_list_id` null → build "virtual bom" từ `quotation_product_prices` (map các field mới thành object giống BomListProduct để blade template render)

---

## FE Changes

### 1. Ẩn tab GP + BOM trên Dự án TKT Type 1

**File:** `pages/assign/prospective-projects/_id/manager.vue`

Trong computed `tabs()`:
- Ẩn tab `solution-info` khi `implementation_type === 1`
- Ẩn tab liên quan BOM (nếu có)
- Các tab phụ thuộc `solutionData.id` (tasks, issues, files, review-profiles): ẩn khi Type 1

### 2. Tab "Báo giá" — thêm nút "Tạo báo giá"

**File:** `ProspectiveProjectQuotationsTab.vue`

- Nhận thêm prop `implementationType`
- Khi `implementationType === 1`: hiện nút "Tạo báo giá" 
- Click → gọi API `POST /quotations/create-direct` → redirect tới `/assign/quotations/{id}/edit`

### 3. Form edit báo giá — chế độ "Quản lý sản phẩm"

**File:** `pages/assign/quotations/_id/edit.vue`

Khi `item.bom_list_id === null` (báo giá trực tiếp):
- Hiện UI quản lý sản phẩm (thêm/xóa/sắp xếp):
  - Nút "Thêm nhóm" → tạo quotation_group
  - Nút "Thêm hàng hoá" trong mỗi nhóm → mở modal search ERP + thêm hàng tự tạo
  - Nút xóa từng sản phẩm
  - Parent-child: thêm hàng con cho hàng cha
- Các field giá (estimated_price, quoted_price, VAT, discount) vẫn inline editable như hiện tại
- Khi save: gửi full products array (bao gồm product info + pricing info)

Khi `item.bom_list_id !== null` (báo giá từ BOM):
- Giữ nguyên logic hiện tại (chỉ sửa giá, không thêm/xóa sản phẩm)

### 4. Trang tạo mới báo giá (optional)

Có thể tạo trang `pages/assign/quotations/create.vue` riêng, hoặc dùng chung trang edit (tạo trống rồi redirect edit). **Recommend dùng chung trang edit** — API `createDirect` tạo record trống → redirect `/quotations/{id}/edit`.

---

## Luồng hoàn chỉnh

```
Dự án TKT (Type 1)
  └─ Tab "Báo giá"
       └─ Nút "Tạo báo giá"
            └─ API createDirect → tạo quotation trống
            └─ Redirect → /quotations/{id}/edit
                 └─ Form gộp:
                      ├─ Quản lý nhóm (quotation_groups)
                      ├─ Thêm sản phẩm (ERP + tự tạo, parent-child)
                      ├─ Nhập giá (estimated_price, quoted_price)
                      ├─ VAT, chiết khấu
                      └─ Lưu → sync products + groups
```

---

## Edge Cases

1. **Báo giá trực tiếp xóa** → cascade delete `quotation_product_prices` + `quotation_groups`
2. **Copy/duplicate báo giá** → copy cả product fields + groups (không phụ thuộc BOM)
3. **Export Excel báo giá không BOM** → dùng product data từ `quotation_product_prices` trực tiếp
4. **In báo giá** → tương tự export, đọc từ `quotation_product_prices`
5. **Gửi duyệt** → logic duyệt không thay đổi (dựa trên quotation, không phụ thuộc BOM)
6. **Dự án Type 1 đã có Solution + BOM + Báo giá cũ** → vẫn hoạt động, báo giá cũ có `bom_list_id` đi luồng cũ

---

## Không thay đổi

- Luồng duyệt báo giá (TP → BGĐ)
- Service items (dịch vụ bổ sung) — đã có bảng riêng `quotation_service_items`
- Chiết khấu tổng (`quotation_discounts`)
- Permission "Xem giá vốn hàng hoá" — áp dụng y hệt
- Lock giá bán ERP — áp dụng y hệt
