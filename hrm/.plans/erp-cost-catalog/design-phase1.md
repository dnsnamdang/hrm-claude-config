# ERP Cost Catalog — Spec Backend (Phase 1)

> Mọi đường dẫn tương đối với `hrm-api/`.

## 1. Model ERP (mysql2) — copy pattern `Modules/Human/Entities/TpProduct.php`

### `Modules/Human/Entities/TpCost.php`
- `$connection = 'mysql2'`, `$table = 'costs'` (constructor prefix `env('DB_DATABASE_SECOND').'.'` như TpProduct).
- Hằng:
  ```php
  const KIND_CHI_PHI = 1;   // Chi phí phải trả / khác
  const KIND_DICH_VU = 2;   // Dịch vụ
  // type (chỉ khi kind_of=1)
  const TYPE_QUOC_TE=1, TYPE_NOI_DIA=2, TYPE_NCC_QT=3, TYPE_BAO_GIA_DV=4,
        TYPE_LAP_DAT=5, TYPE_DU_AN=6, TYPE_BAN_HANG=7, TYPE_GIA_HH=8;
  ```
- `getKindList()` → [1=>'Chi phí khác', 2=>'Dịch vụ'].
- `getTypeList()` → [1=>'Quốc tế',2=>'Nội địa',3=>'NCC quốc tế',4=>'Báo giá dịch vụ',5=>'Lắp đặt',6=>'Dự án',7=>'Bán hàng',8=>'Giá hàng hoá'].
- `scopeActive($q)` → `where('status',1)`.

### `Modules/Human/Entities/TpCompanyCost.php`
- `$connection='mysql2'`, `$table='company_costs'`. Cột: `id, company_id, cost_id, discount, timestamps`.

## 2. Endpoint dùng chung — `Modules/Assign/Http/Controllers/Api/V1/ErpCostController.php`

### `index(Request)` — `GET /assign/erp-costs`
- Query param: `keyword` (tìm theo `name` LIKE), `kind_of` (lọc 1/2; rỗng = cả hai).
- Base: `TpCost::active()->whereIn('kind_of',[1,2])`.
- `limit(50)`, `orderBy('name')`.
- Trả mỗi item:
  ```php
  ['id','name','kind_of','kind_name','type','type_name','vat_percent','rate_value_capital']
  ```

### `store(ErpCostStoreRequest)` — `POST /assign/erp-costs`
- `DB::connection('mysql2')->transaction(function(){ ... })`:
  - insert `costs`: `name, en_name, kind_of`, `type = kind_of==1 ? type : null`,
    `rate_value_capital = kind_of==2 ? rate_value_capital : null`,
    `revenue_calculation = kind_of==2 ? (revenue_calculation?1:0) : null`,
    `vat_percent`, `status=1`, `created_by = <ERP employee id>` (resolve qua `TpEmployee::where('employee_info_id', auth()->user()->employee_info_id)->first()->id`, fallback `auth()->id()`).
- **KHÔNG ghi `company_costs`** — bỏ chiết khấu (HRM không dùng; không có mapping company HRM→ERP). `TpCompanyCost` model giữ lại nhưng chưa dùng.
- Trả về cost mới chuẩn hoá như `index`.
- Controller: `catch (ValidationException $e) { throw $e; } catch (Exception $e){ Log::error($e); responseUnprocessableEntity }`.

### `ErpCostStoreRequest` — `Modules/Assign/Http/Requests/Quotation/ErpCostStoreRequest.php`
Mirror rule ERP (`CostsController@store`):
```php
$kindOf = (int) $this->kind_of;
return [
  'name' => ['required','max:255',
      Rule::unique('costs')->where(fn($q)=>$q->where('type', $this->type))   // connection mysql2
  ],
  'kind_of' => 'required|in:1,2',
  'type' => $kindOf===1 ? 'required|in:1,2,3,4,5,6,7,8' : 'nullable',
  'rate_value_capital' => $kindOf===2 ? 'required|numeric|min:0' : 'nullable',
  'vat_percent' => 'required|numeric|max:100',
  'en_name' => 'nullable|string|max:255',
  'revenue_calculation' => 'nullable|boolean',
];
```
- Message tiếng Việt: `name.unique` = "Đã tồn tại trên hệ thống", v.v.
- **Lưu ý:** `Rule::unique('costs')` phải trỏ connection `mysql2` → dùng `Rule::unique('mysql2.<db>.costs',...)` hoặc set connection trong rule. Xác minh khi code (xem mục 5 — `unique` cross-connection).

### Routes — `Modules/Assign/Routes/api.php` (group prefix `assign`)
```php
Route::get('/erp-costs', [ErpCostController::class, 'index']);
Route::post('/erp-costs', [ErpCostController::class, 'store']);
```
KHÔNG gắn middleware permission (mọi user sửa được báo giá/BOM dùng được).

## 3. Migration — `database/migrations/2026_06_02_xxxxxx_add_cost_id_to_service_lines.php`
- `quotation_service_items`:
  - `cost_id` unsignedBigInteger nullable, after `code`.
  - `unit_id` → `nullable()->change()`.
- `bom_list_products`:
  - `cost_id` unsignedBigInteger nullable, after `product_type`.
- `down()`: dropColumn `cost_id` cả 2 bảng (không revert nullable unit_id để an toàn).

## 4. Quotation — nhận & lưu `cost_id`
- `Http/Requests/Quotation/QuotationStoreRequest.php` + `QuotationUpdateRequest.php`:
  - thêm `service_items.*.cost_id => 'nullable|integer'`.
  - đổi `service_items.*.unit_id` → `'nullable|integer'`.
- `Services/QuotationService.php`:
  - block tạo service_items (trong `create()` ~dòng 157, `update()` ~dòng 539): thêm `'cost_id' => $si['cost_id'] ?? null`.
  - **`qty` luôn = 1** cho dòng dịch vụ/chi phí (BE ép `'qty' => 1` khi có `cost_id`, không tin giá trị FE gửi).
  - Nếu có `cost_id` và `vat_percent` rỗng → fallback lấy `TpCost::find(cost_id)->vat_percent`.
- `Http/Controllers/Api/V1/QuotationController.php` (`storeServiceItem` ~1172, `updateServiceItem`): rule `cost_id` nullable, `unit_id` nullable; lưu `cost_id`.
- `Transformers/DetailQuotationResource.php::resolveServiceItems()`: thêm `cost_id`, `kind_of` (badge).

## 4b. BOM — nhận & lưu `cost_id` (dòng service, product_type=2)
- `Http/Requests/BomList/BomListStoreRequest.php`: thêm `groups.*.parent.cost_id` + `groups.*.children.*.cost_id` => `nullable|integer`.
- `Services/BomListService.php` (`mapProductPayload`/`syncProducts`): khi `product_type=2` → map `cost_id` + **ép `qty_needed = 1`**; giữ rule strip model/brand/origin + no children.
- Resource BOM products: thêm `cost_id`.

## 5. Rủi ro / cần xác minh khi code
- **`created_by` khi insert `costs`**: ERP dùng `Auth::user()->info` (employee). HRM auth → cần map sang `employee_id` ERP. Xác minh field nào ERP `costs.created_by` tham chiếu (bigint unsigned). Dùng `auth()->user()->employee_id` (đã dùng ở QuotationController store).
- **`company_id`**: lấy từ `current_company`/employee của user HRM.
- **`Rule::unique` cross-connection (mysql2)**: Laravel `Rule::unique('costs')` mặc định connection chính. Phải ép connection ERP. Phương án: validate thủ công bằng `TpCost::where('name',...)->where('type',...)->exists()` trong Request `withValidator` để chắc chắn đúng connection.
- **`vat_percent` NOT NULL default 0** ở `costs` — luôn set giá trị.
