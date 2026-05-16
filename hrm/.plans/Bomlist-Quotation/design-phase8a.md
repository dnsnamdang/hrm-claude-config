# Design: BOM List — Phase 8a: Status workflow + Currency + Columns + Service

## Ngày: 2026-04-10
## Người phụ trách: @dnsnamdang

---

## 1. Mục đích

Cập nhật BOM List để hỗ trợ:
- Workflow trạng thái rõ ràng theo loại BOM (Thành phần / Tổng hợp), tự động đồng bộ với hồ sơ trình duyệt
- Loại tiền tệ cho mỗi BOM (lấy từ ERP)
- Bổ sung dữ liệu tính toán: giá bán, thành tiền nhập/bán, tỷ suất lợi nhuận
- Bổ sung loại dữ liệu **Dịch vụ** (không có model/brand/origin)

## 2. Scope

### Làm:
- Thêm 2 status mới: 5 (Đã được tổng hợp), 6 (Không duyệt)
- Thêm cột `currency_id` vào `bom_lists`
- Thêm cột `product_type` vào `bom_list_products` (1=Hàng hoá, 2=Dịch vụ)
- Reuse `estimated_price` (giá nhập) + `quoted_price` (giá bán) đã có
- Accessor tính: `import_total`, `sale_total`, `profit_margin`
- Logic sync status BOM từ submission service (gọi thủ công)
- UI: Card BOM hiển thị select Currency, bảng product có icon phân biệt Hàng/Dịch vụ
- Modal "Thêm hàng hoá" — Tab "Tạo mới" thêm toggle Hàng/Dịch vụ
- Update Excel template: thêm cột Giá bán, Loại
- Migration backfill data cũ

### Không làm:
- Approval workflow theo cấp + thresholds → **Phase 8b**
- Quy đổi tỷ giá tự động khi đổi currency
- Lấy dịch vụ từ ERP

---

## 3. Status Workflow

### 3.1 Bảng status đầy đủ

| Code | Tên | Áp dụng | Trigger |
|---|---|---|---|
| 1 | Đang tạo | Cả 2 | User click "Lưu nháp" |
| 2 | Hoàn thành | Cả 2 | User click "Lưu" |
| 3 | Chờ duyệt | Tổng hợp | Submission → Chờ duyệt |
| 4 | Đã duyệt | Tổng hợp | Submission → Đã duyệt |
| 5 | Đã được tổng hợp | Thành phần | Bị BOM Tổng hợp chọn |
| 6 | Không duyệt | Tổng hợp | Submission → Không duyệt |

### 3.2 Workflow BOM Thành phần (type=1)

```
[Tạo mới]
    ↓ Lưu nháp
  Status 1 (Đang tạo)
    ↓ Lưu
  Status 2 (Hoàn thành)
    ↓ Bị BOM Tổng hợp chọn
  Status 5 (Đã được tổng hợp) ← LOCKED, không cho sửa/xoá
    ↓ BOM Tổng hợp bỏ chọn / xoá
  Status 2 (Hoàn thành)
```

**Quy tắc:**
- Status 1, 2: cho sửa bình thường (giống logic hiện tại)
- Status 5: KHÔNG cho sửa, KHÔNG cho xoá
- Phase 7.6 đã có validate unique aggregate → 1 BOM Thành phần chỉ thuộc 1 BOM Tổng hợp

### 3.3 Workflow BOM Tổng hợp (type=2)

```
[Tạo mới]
    ↓ Lưu nháp
  Status 1 (Đang tạo)
    ↓ Lưu
  Status 2 (Hoàn thành)
    ↓ Submission → Chờ duyệt
  Status 3 (Chờ duyệt) ← LOCKED
    ↓ Submission → Đã duyệt        ↓ Submission → Không duyệt
  Status 4 (Đã duyệt) ← LOCKED   Status 6 (Không duyệt)
                                     ↓ User sửa
                                   Status 2 (Hoàn thành) — sẵn sàng trình lại
```

**Quy tắc:**
- Status 1, 2, 6: cho sửa
- Status 3, 4: KHÔNG cho sửa
- Khi user sửa BOM ở status 6 → tự động chuyển về 2

### 3.4 Sync status từ submission

**Cơ chế:** Gọi thủ công qua method service.

```php
// BomListService.php
public function syncStatusFromSubmission($submissionType, $referenceId, $submissionStatus)
{
    // $submissionType: 'solution' | 'solution_module'
    // $referenceId: solution_id hoặc solution_module_id
    // $submissionStatus: status code của submission
    
    $statusMap = [
        SubmissionStatus::CHO_DUYET => BomList::STATUS_CHO_DUYET,    // 3
        SubmissionStatus::DA_DUYET => BomList::STATUS_DA_DUYET,      // 4
        SubmissionStatus::KHONG_DUYET => BomList::STATUS_KHONG_DUYET, // 6
    ];
    
    $newStatus = $statusMap[$submissionStatus] ?? null;
    if (!$newStatus) return;
    
    // Tìm BOM Tổng hợp gắn với hồ sơ này
    $query = BomList::where('bom_list_type', BomList::TYPE_AGGREGATE);
    if ($submissionType === 'solution_module') {
        $query->where('solution_module_id', $referenceId);
    } else {
        $query->where('solution_id', $referenceId)->whereNull('solution_module_id');
    }
    $query->update(['status' => $newStatus]);
}
```

**Điểm gọi:** SubmissionService khi đổi status hồ sơ → gọi `BomListService::syncStatusFromSubmission()`. Cần xác định cụ thể trong plan-phase8a (đọc code SubmissionService).

### 3.5 Sync status BOM Thành phần

Khi save BOM Tổng hợp (lưu nháp hoặc lưu), service sẽ:
1. Lấy danh sách BOM con `bom_list_relations`
2. Set status BOM con = 5 (Đã được tổng hợp)

Khi xoá BOM Tổng hợp / bỏ chọn BOM con:
1. Set status BOM con quay về 2 (Hoàn thành)

```php
// BomListService.php
protected function syncChildStatus(BomList $aggregate, array $newChildIds, array $oldChildIds)
{
    $added = array_diff($newChildIds, $oldChildIds);
    $removed = array_diff($oldChildIds, $newChildIds);
    
    if ($added) {
        BomList::whereIn('id', $added)->update(['status' => BomList::STATUS_DA_DUOC_TONG_HOP]);
    }
    if ($removed) {
        BomList::whereIn('id', $removed)->update(['status' => BomList::STATUS_HOAN_THANH]);
    }
}
```

### 3.6 SubBomModal — filter

Popup chọn BOM con (`BomBuilderSubBomModal.vue`):
- Filter `status = 2` (chỉ Hoàn thành) — không hiện status 5 (đã thuộc BOM khác)
- Đã có sẵn từ Phase 7.3, chỉ cần đảm bảo filter chính xác

---

## 4. Currency

### 4.1 Cấu trúc DB

**Migration:** Thêm cột vào `bom_lists`
```sql
ALTER TABLE bom_lists 
    ADD COLUMN currency_id BIGINT UNSIGNED NULL AFTER customer_id 
    COMMENT 'FK currencies (ERP DB)';
```

**Backfill:** Set `currency_id` = ID của VND trong `currencies` table (ERP DB) cho tất cả BOM cũ.

### 4.2 Model mới

`Modules/Human/Entities/TpCurrency.php` (mysql2 connection — giống `TpProduct`)
```php
class TpCurrency extends Model
{
    protected $connection = 'mysql2';
    protected $table = 'currencies';
    public $timestamps = false;
}
```

### 4.3 API endpoint

```
GET /assign/bom-lists/currencies → trả về danh sách currencies từ ERP
```

Response:
```json
[
    { "id": 1, "code": "VND", "name": "Việt Nam Đồng", "symbol": "₫" },
    { "id": 2, "code": "USD", "name": "US Dollar", "symbol": "$" }
]
```

### 4.4 UI

**`BomBuilderInfoCard.vue`:**
- Thêm field "Loại tiền tệ" (V2BaseSelect)
- Default: VND
- Khi user đổi currency:
  - Nếu BOM đã có sản phẩm → hiện confirm modal: "Đổi loại tiền tệ sẽ giữ nguyên số tiền hiện tại, chỉ thay đổi đơn vị hiển thị. Bạn cần kiểm tra lại giá. Tiếp tục?"
  - Confirm OK → set currency mới
  - Cancel → revert về currency cũ

### 4.5 Hiển thị

- Card BOM: hiển thị tên + symbol currency (vd: "Việt Nam Đồng (₫)")
- Bảng product: format giá theo symbol currency của BOM
- Excel export: header thêm dòng "Loại tiền tệ: VND"

---

## 5. Cột giá + Accessor

### 5.1 Mapping

| Cột yêu cầu | Cột DB | Loại |
|---|---|---|
| Giá nhập | `bom_list_products.estimated_price` (đã có) | Lưu DB |
| Giá bán | `bom_list_products.quoted_price` (đã có) | Lưu DB |
| Thành tiền nhập | Accessor `import_total` | Tính lúc đọc |
| Thành tiền bán | Accessor `sale_total` | Tính lúc đọc |
| Tỷ suất lợi nhuận | Accessor `profit_margin` | Tính lúc đọc |

### 5.2 Accessor

```php
// BomListProduct.php
public function getImportTotalAttribute()
{
    return ($this->estimated_price ?? 0) * ($this->qty_needed ?? 0);
}

public function getSaleTotalAttribute()
{
    return ($this->quoted_price ?? 0) * ($this->qty_needed ?? 0);
}

public function getProfitMarginAttribute()
{
    if (!$this->estimated_price || $this->estimated_price == 0) return null;
    return round((($this->quoted_price - $this->estimated_price) / $this->estimated_price) * 100, 2);
}

protected $appends = ['import_total', 'sale_total', 'profit_margin'];
```

### 5.3 UI bảng product

Thêm cột vào `BomBuilderTableCard.vue`:
- **Giá nhập** (đã có)
- **Thành tiền nhập** (mới) — tính từ accessor
- **Giá bán** (đã có)
- **Thành tiền bán** (mới) — tính từ accessor
- **Tỷ suất lợi nhuận** (mới) — tính từ accessor, format `xx.xx%`, màu đỏ nếu < 10%, vàng 10-20%, xanh > 20% (chỉ hiển thị màu, không có logic cảnh báo — Phase 8b)

### 5.4 Validate

- Giá bán có thể lớn hơn, bằng, hoặc nhỏ hơn giá nhập
- Nếu giá nhập = 0 → tỷ suất hiển thị "—"
- Số âm: không cho phép

---

## 6. Loại dữ liệu Dịch vụ

### 6.1 Cấu trúc DB

**Migration:** Thêm cột vào `bom_list_products`
```sql
ALTER TABLE bom_list_products 
    ADD COLUMN product_type TINYINT NOT NULL DEFAULT 1 AFTER bom_list_id 
    COMMENT '1=Hàng hoá, 2=Dịch vụ';
```

**Backfill:** Set `product_type = 1` cho tất cả record cũ.

### 6.2 Constant

```php
// BomListProduct.php
const PRODUCT_TYPE_GOODS = 1;
const PRODUCT_TYPE_SERVICE = 2;
```

### 6.3 Quy tắc

- **Hàng hoá (1):** Có model_id, brand_id, origin_id (có thể null tuỳ trường hợp), có cha/con
- **Dịch vụ (2):**
  - Có: name, unit_id, estimated_price, quoted_price, qty_needed, product_attributes
  - Không có: model_id, brand_id, origin_id, erp_product_id (luôn null)
  - **Chỉ làm hàng cha**, không có hàng con
  - Không lấy từ ERP

### 6.4 UI — Modal "Thêm hàng hoá"

`BomBuilderAddProductModal.vue`:

**Tab 1 (Tìm có sẵn):** Giữ nguyên — chỉ search hàng hoá ERP/BOM. Không có dịch vụ.

**Tab 2 (Tạo mới):** Thêm radio toggle ở đầu form
```
○ Hàng hoá   ● Dịch vụ
```

| Field | Hàng hoá | Dịch vụ |
|---|---|---|
| Tên | ✅ | ✅ |
| Mã | ✅ | ✅ |
| Model | ✅ | ❌ Ẩn |
| Thương hiệu | ✅ | ❌ Ẩn |
| Xuất xứ | ✅ | ❌ Ẩn |
| ĐVT | ✅ | ✅ |
| Đặc điểm | ✅ | ✅ |
| Giá nhập | ✅ | ✅ |
| Giá bán | ✅ | ✅ |
| Số lượng | ✅ | ✅ |

### 6.5 UI — Bảng product

- Icon trước tên: 📦 (hàng hoá) / 🛠 (dịch vụ) — dùng remixicon `ri-box-3-line` / `ri-tools-line`
- Dịch vụ nằm chung group với hàng hoá (không tách riêng)
- Cột Model/Thương hiệu/Xuất xứ: nếu là dịch vụ → hiển thị "—"
- Không cho phép drop hàng con vào dịch vụ (drag-drop validation)

### 6.6 Validate FE

```js
// BomBuilderAddProductModal.vue — submitCreate()
if (form.product_type === 2) {
    // Dịch vụ
    required: ['name', 'unit_id', 'estimated_price', 'quoted_price', 'qty_needed']
    // Bỏ qua: model_id, brand_id, origin_id
} else {
    // Hàng hoá — như cũ
    required: ['name', 'unit_id', 'model_id', 'brand_id', 'origin_id']
}
```

### 6.7 Validate BE

`BomListService::syncProducts()`:
- Nếu `product_type = 2` → bỏ qua validate model/brand/origin
- Nếu `product_type = 2` và có `parent_id != null` → reject (dịch vụ không được làm con)
- Nếu `product_type = 2` và là cha có con → reject (dịch vụ không có con)

---

## 7. Excel Import / Export

### 7.1 Export — thêm cột

Hiện tại Excel export có các cột: STT, Mã, Tên, Model, Thương hiệu, Xuất xứ, ĐVT, Đặc điểm, Số lượng, Đơn giá, Thành tiền

**Thêm:**
- Cột "Loại" (Hàng hoá / Dịch vụ)
- Cột "Giá bán" 
- Cột "Thành tiền bán"
- Cột "Tỷ suất lợi nhuận"
- Header info: "Loại tiền tệ: [name] ([symbol])"

### 7.2 Import — update template

Template cũ thêm 4 cột Loại, Giá bán, Thành tiền bán, Tỷ suất.

**Validate import:**
- Nếu cột "Loại" = "Dịch vụ" → bỏ qua validate Model/Thương hiệu/Xuất xứ
- Nếu Loại = Dịch vụ + có hàng con (STT 1.1, 1.2) → cảnh báo "Dịch vụ không có hàng con"
- Nếu cột "Loại" trống → mặc định = Hàng hoá

### 7.3 Backfill cho file cũ

User có thể vẫn dùng file Excel format cũ (không có cột Loại + Giá bán):
- Mặc định Loại = Hàng hoá
- Giá bán = 0 (user nhập sau trong app)

---

## 8. Migration

### 8.1 Migration 1 — Thêm currency_id

```php
// 2026_04_10_100000_add_currency_id_to_bom_lists.php
public function up()
{
    Schema::table('bom_lists', function (Blueprint $table) {
        $table->unsignedBigInteger('currency_id')->nullable()->after('customer_id')
            ->comment('FK currencies (ERP DB)');
    });
    
    // Backfill VND
    $vndId = DB::connection('mysql2')->table('currencies')->where('code', 'VND')->value('id');
    if ($vndId) {
        DB::table('bom_lists')->whereNull('currency_id')->update(['currency_id' => $vndId]);
    }
}
```

### 8.2 Migration 2 — Thêm product_type

```php
// 2026_04_10_100001_add_product_type_to_bom_list_products.php
public function up()
{
    Schema::table('bom_list_products', function (Blueprint $table) {
        $table->tinyInteger('product_type')->default(1)->after('bom_list_id')
            ->comment('1=Hàng hoá, 2=Dịch vụ');
    });
}
```

### 8.3 Migration 3 — Cập nhật status comment

```php
// 2026_04_10_100002_update_bom_lists_status_comment.php
public function up()
{
    DB::statement("ALTER TABLE bom_lists MODIFY COLUMN status TINYINT NOT NULL DEFAULT 1 
        COMMENT '1=Đang tạo, 2=Hoàn thành, 3=Chờ duyệt, 4=Đã duyệt, 5=Đã được tổng hợp, 6=Không duyệt'");
}
```

---

## 9. Permission

Không thêm permission mới ở Phase 8a. Permission xét duyệt giá → Phase 8b.

---

## 10. File structure

### Backend — Tạo mới
- `database/migrations/2026_04_10_100000_add_currency_id_to_bom_lists.php`
- `database/migrations/2026_04_10_100001_add_product_type_to_bom_list_products.php`
- `database/migrations/2026_04_10_100002_update_bom_lists_status_comment.php`
- `Modules/Human/Entities/TpCurrency.php`

### Backend — Sửa
- `Modules/Assign/Entities/BomList.php` — thêm const STATUS_DA_DUOC_TONG_HOP=5, STATUS_KHONG_DUYET=6, update getStatusList(), thêm $fillable currency_id, relationship currency()
- `Modules/Assign/Entities/BomListProduct.php` — thêm const PRODUCT_TYPE_*, $fillable product_type, accessors import_total/sale_total/profit_margin
- `Modules/Assign/Services/BomListService.php` — thêm syncStatusFromSubmission(), syncChildStatus(), update syncProducts() validate dịch vụ, update store/update để handle currency_id
- `Modules/Assign/Http/Controllers/Api/V1/BomListController.php` — thêm getCurrencies()
- `Modules/Assign/Http/Requests/BomList/BomListStoreRequest.php` — thêm rule currency_id, conditional rule cho product_type
- `Modules/Assign/Routes/api.php` — thêm route currencies
- `Modules/Assign/Exports/BomListExport.php` — thêm cột Loại, Giá bán, Thành tiền bán, Tỷ suất
- `Modules/Assign/Imports/BomListImport.php` — parse cột Loại, conditional validate
- `Modules/Assign/Transformers/BomListResource/BomListShowResource.php` — append currency, accessor mới

### Frontend — Sửa
- `pages/assign/bom-list/components/BomBuilderInfoCard.vue` — thêm select Currency
- `pages/assign/bom-list/components/BomBuilderTableCard.vue` — thêm cột Giá bán, Thành tiền nhập/bán, Tỷ suất, icon hàng/dịch vụ
- `pages/assign/bom-list/components/BomBuilderAddProductModal.vue` — Tab 2 thêm radio Hàng/Dịch vụ, conditional fields
- `pages/assign/bom-list/components/BomBuilderEditor.vue` — handle currency change, sync productType khi save
- `pages/assign/bom-list/components/BomBuilderImportModal.vue` — preview cột Loại
- `pages/assign/bom-list/index.vue` — hiển thị icon dịch vụ trong list nếu cần
- `pages/assign/bom-list/_id/index.vue` — hiển thị currency + cột mới ở view chi tiết

---

## 11. Quyết định thiết kế

1. **Status code thống nhất 1-6** (không tách enum theo type) — đơn giản query, FE map label theo type khi hiển thị
2. **Sync status thủ công** (option C trong brainstorm) — không dùng observer, dễ debug, dễ test
3. **Reuse cột giá có sẵn** — không thêm cột giá mới, tránh migration phức tạp
4. **Dịch vụ flag bằng cột product_type** — không tách bảng, đơn giản query
5. **Currency 1-1 với BOM** — không hỗ trợ đa tiền tệ trong cùng BOM, không quy đổi tự động
6. **Accessor cho thành tiền/tỷ suất** — không lưu DB, tránh data lệch

---

## 12. Câu hỏi mở (Phase 8b sẽ giải quyết)

- Cấu hình ngưỡng phê duyệt (1 tỷ, 20 tỷ, 10%, 20%) — hardcode hay configurable?
- 2 permission mới: gán theo phòng ban hay theo user trực tiếp?
- Cấp phê duyệt link với hồ sơ trình duyệt giải pháp/hạng mục thế nào?
- Workflow notify khi cần duyệt?
- Logic màu cảnh báo trên cột tỷ suất (đã setup UI ở Phase 8a, logic ở Phase 8b)
