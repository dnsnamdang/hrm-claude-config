# Đợt 2-C2 — Lấy về + sửa mức Quản trị — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (hoặc executing-plans). Bước dùng checkbox `- [ ]`.
> 08/10/2026 · @namdangit · CHỈ là tài liệu — chưa đụng source. Code chỉ bắt đầu khi user trả lời **"làm"** cho mục 0 (CLAUDE.md root).

**Goal:** Công ty có quyền 1652 lấy hàng hoá của công ty khác về dùng (1 mã hoặc ≤ 100 mã/lượt) ở màn *Kho dữ liệu hàng hoá*, rồi khai tab *Quản trị hàng hoá* của công ty mình (4 ô quản trị + NCC + catalog) mà không đụng được lớp chung.

**Architecture:** BE thêm 2 endpoint trong `Modules/MasterData` — `POST products/take` (lấy về, bỏ qua từng mã không hợp lệ kèm lý do) và `PUT products/{id}/admin-data` (chỉ nhận khối `admin`, khoá lạ ⇒ 403) — tái dùng `ProductWriteService::writeAdmin()` của 2-C1; nới `GET {id}/edit` + `can_edit` cho công ty lấy về, thêm `edit_scope` + `can_take_back`; luật "trạng thái công ty tạo" (L3) đặt cạnh luật suy ra 2-B trong `Product.php`. FE mở rộng `ProductListPage.vue` (ô tick + thanh chọn + action *Lấy về* ở Kho) và `ProductForm.vue` (chế độ `admin`: tab Thông tin chỉ đọc bằng 5 component chi tiết 2-B).

**Tech Stack:** Laravel 8 + nwidart, PHP 7.4 (`/opt/homebrew/opt/php@7.4/bin/php`), PHPUnit `DatabaseTransactions` trên `hrm_erp` · Nuxt 2 / Vue 2, V2Base* · Playwright (MCP để kiểm + spec viết sẵn).

**Spec / luật (thứ tự ưu tiên):** `chot.md` mục *Chốt riêng đợt 2-C2* **L1–L7** (cao nhất, ĐÈ đề xuất khảo sát) > G1–G11, T6, H1', C1–C12, D1–D4 > `c2-khao-sat-be.md` §2–§6 > `c2-khao-sat-fe.md` §4 (T1–T8) > mockup. Đáp án `c2-ton.md` Q1–Q7.

**Đã kiểm lại file:dòng khảo sát (08/10, worktree HEAD api `35c4aa971` / client `81f38f36d`, cây sạch):** route khối products `Routes/api.php:253-289` (POST `/` :283, `/{product}/edit` :285, PUT :286, show :288) · `ProductWriteService` `assertCanWrite` :76, `assertOwner` :84-97, `sameAsShown` :386, `writeAdmin` :402-444 · `ProductRequest::authorize` :21-31, rule `admin.*` :132-140, `checkClusters` :318-332 · `ProductWriteController::edit` :31-46 · `can_edit` `ProductListResource.php:59-63`, `ProductDetailResource.php:43-47` · `Product::scopeWithCompanyStatus` :366-378, `companyStatusSql` :381-389 · `ProductService::applyScreen` :173-201 (warehouse :178-185) · `withCompanyRelations` :264-280 (nạp MỌI dòng `companies`) · FE `ProductListPage.vue` tick :158-172, thanh `#left-actions` :142-156, `#cell-actions` :279-284, `canBuildCatalog` :645-647, cột `actions` :628-638 · `ProductForm.vue` `parentTab: 'info'` :67, `toPayload` :217, toast :223 · `ProductParentTabs.vue` **194** dòng (khảo sát ghi 181 — không ảnh hưởng) · spec `products-read-ui.spec.ts:19` (bộ cột warehouse), `:30` (`WRITE_BUTTONS` cấm "Lấy về"), `products-form-ui.spec.ts:233-245` (E2). DB local: `product_company_coefficients` 1.105 dòng, **0** dòng `status` NOT NULL; 5 dòng của chính công ty tạo; 1652 chỉ gán role *Super admin* + *E2E No Cost* ở Cty 1.

> ⚠️ Tên đã chốt theo yêu cầu lead: endpoint **`POST products/take`**, cờ **`can_take_back`** (khảo sát FE ghi `take-back`, khảo sát BE ghi `can_take` — bỏ).

---

## 0. Phạm vi xin phép (đưa user duyệt "làm" — mỗi PHA xin riêng)

| | |
|---|---|
| Repo | `hrm-api` + `hrm-client`, worktree `websites/wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}` |
| Nhánh | **`feat/p2c2-lay-ve`** tạo từ `feat/chuyen-doi-hang-hoa` (api `35c4aa971`, client `81f38f36d`) ở cả 2 repo, trong worktree. Xong từng pha: commit trên nhánh con (hỏi trước khi commit); xong cả đợt: merge `--no-ff` về `feat/chuyen-doi-hang-hoa` + push — **hỏi riêng**. ⛔ **KHÔNG merge / cherry-pick sang `gop_db`** (memory: feat Chuyển đổi hàng hoá không vào gop_db) |
| BE — tạo (3) | `Modules/MasterData/Http/Requests/Product/ProductTakeRequest.php` · `Http/Requests/Product/ProductAdminDataRequest.php` · `Tests/Feature/ProductTakeApiTest.php` |
| BE — sửa (9) | `Routes/api.php` (khối :253-289) · `Http/Controllers/V1/Product/ProductWriteController.php` · `Services/Product/ProductWriteService.php` · `Http/Requests/Product/ProductRequest.php` (tách `checkClusters`) · `Entities/Product/Product.php` (luật trạng thái công ty tạo) · `Services/Product/ProductService.php` (Kho lọc status 0 + cột `owner_status`) · `Transformers/Product/ProductListResource.php` · `Transformers/Product/ProductDetailResource.php` · `Transformers/Product/ProductFormResource.php` (+ `Transformers/Product/AdminData.php` nếu giữ tự quyết Q-A3) |
| BE — có thể tạo thêm (1) | `Http/Requests/Product/Concerns/ChecksCatalogClusters.php` (trait chung cho `checkClusters`) |
| FE — sửa (8) | `utils/product-list-screens.js` · `components/product/ProductListPage.vue` · `pages/master-data/products/warehouse.vue` (docblock) · `pages/master-data/products/entering.vue` (docblock nếu cần) · `components/product/form/ProductForm.vue` · `components/product/form/ProductFormAdmin.vue` · `components/product/form/productFormModel.js` · `components/product/detail/ProductParentTabs.vue` |
| e2e (không phải repo git — `wt-chuyen-doi-hang-hoa/e2e`, chép bản cuối về `HRM/e2e`) | tạo `tests/master-data/products-take.api.spec.ts`, `tests/master-data/products-take-ui.spec.ts`; sửa `products-read-ui.spec.ts`; rà `products-form-ui.spec.ts` (E2) |
| Migration / seeder / quyền mới | **KHÔNG** — đã xác nhận: 4 cột quản trị + `status` có sẵn ở `product_company_coefficients`, UNIQUE `(product_id, company_id)` có thật, quyền 1652/1653 có trong DB local. Không chạy `migrate`, không chạy seeder |
| Ghi DB local `hrm_erp` | (1) PHPUnit: chỉ trong `DatabaseTransactions` (rollback). (2) Kiểm Playwright MCP + e2e (khi user cho chạy): **lấy về thật vài mã Cty 4 về Cty 1** ⇒ sinh dòng `product_company_coefficients` (+ `product_suppliers`, `product_business_catalogs` khi Lưu tab Quản trị) — **dọn bằng DELETE đúng id đã ghi nhận trước**; (3) role tạm `E2E C2 tạm - chỉ xem hàng công ty` (chỉ 1653) gán cho tài khoản `e2e_cmd_noperm@test.local` + `cache:clear` (bẫy spatie cache 24h), gỡ ở `afterAll`. **Hỏi riêng trước khi ghi (2)(3)** |
| Không đụng | ERP · popup 2-C3 · 6 component chi tiết chỉ đọc (chỉ TÁI DÙNG, không sửa) · 12 component form 2-C1 (không thêm prop `disabled`) · `PUT /{product}` đầy đủ (giữ chỉ chủ) |

**3 pha, 13 task:**

| Pha | Task | Deliverable kiểm được |
|---|---|---|
| **P1 — BE** | B1–B6 | `ProductTakeApiTest` xanh (đủ ca mục 2.1); hồi quy `ProductWriteApiTest`, `ProductReadApiTest`, `ProductCatalogApiTest`, `ProductCompanyFoundationTest` xanh |
| **P2 — FE** | F1–F5 | Playwright MCP đo DOM từng luồng (mục 3.3) |
| **P3 — e2e + chốt** | E1–E2 | spec mới + sửa viết xong, `--list` OK (chạy khi user yêu cầu, `--workers=1`); review cuối; checkpoint |

---

## Global Constraints

- **L1** lấy về mã đã có dòng hệ số cũ (`status NULL`) ⇒ UPDATE `status = 1`, **giữ `coefficient`**; chưa có dòng ⇒ INSERT `coefficient = 1` (`ProductCompany::NEUTRAL_COEFFICIENT`), `status = 1`.
- **L2** lúc lấy về **KHÔNG ghi 4 ô quản trị** (để nguyên NULL / không chép cột chung). Chấp nhận cột *Bảo hành / Tồn tối thiểu* của công ty lấy về chuyển trống.
- **L3** chỉ lấy về khi `products.status = 1` **và** trạng thái của CÔNG TY TẠO (suy theo 2-B: `COALESCE(dòng chủ.status, CASE WHEN products.status = 1 THEN 3 END)`) **= 3**. Hàng công ty tạo ở 1/2/4 ⇒ bỏ qua + lý do.
- **L4** `GET warehouse` lọc `products.status <> 0` (giữ 7 mã status 2/5 — hiện, nhưng `can_take_back = false`).
- **L5** `PUT admin-data` bắt buộc `admin.job_cluster_ids` ≥ 1 (C1) — nhánh đã lưu bị khoá thì giữ (D3). `take` KHÔNG đòi catalog, KHÔNG ghi NCC/catalog.
- **L6** không làm popup *Xem hàng hoá Công ty khác*; màn Nhập thông tin có nút điều hướng sang Kho dữ liệu (công tắc *Chỉ hàng công ty chưa dùng* bật sẵn).
- **L7** không thông báo khi công ty tạo sửa lớp chung (đọc thẳng `products`).
- **T6** `tech_coefficient` là cột chung — công ty lấy về KHÔNG sửa (FE khoá ô, BE 403 nếu gửi).
- **H1'** Lưu tab Quản trị KHÔNG đổi trạng thái; hàng lấy về treo ở 1 tới phase Tính giá.
- **G9b** trần 100 mã/lượt (FE chặn lúc tick + BE 422).
- `company_id` của dòng mới gán TAY = `auth()->user()->current_company_role` (`DB::table`, không qua hook `BaseModel::creating`).
- Không dùng `DB::upsert()` / `updateOrInsert` (đè `coefficient` + lùi `status` — R2/R3 khảo sát BE). UPDATE luôn kẹp `whereNull('status')`; INSERT dùng `insertOrIgnore` (đua ⇒ 0 dòng ⇒ "đang dùng rồi"). Không cần `lockForUpdate` (tránh gap-lock khi 2 lượt lấy song song).
- Quyền: middleware `checkPermission:Xây dựng thông tin hàng hoá` + `assertCanWrite()` (R22, theo công ty đang làm việc) ở mọi đường ghi; 403 luôn TRƯỚC 422 (R6 — kiểm trong `authorize()`).
- Test quyền luôn 2 phía (có / không 1652; 1652 chỉ ở công ty khác ⇒ 403) — memory *always-test-permission-cases*. Không bypass super admin.
- FE: V2Base*, `$confirm` (không `b-modal`/`msgBoxConfirm`), `V2BaseRowActions` icon, slot `#cell-<key>`, không `trim`, không chờ `networkidle`, e2e `--workers=1`; KHÔNG tự chạy e2e (chỉ `--list`) nhưng BẮT BUỘC kiểm Playwright MCP + đo DOM trước khi báo xong (CLAUDE.md root).

Lệnh test BE: `cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/<File>.php [--filter <ca>]`. KHÔNG `config:cache`.

---

## 1. Hợp đồng API

### 1.1 `POST /api/v1/master-data/products/take` (MỚI)

Route đặt TRƯỚC `/{product}` (cạnh `POST /` :283). Middleware `checkPermission:Xây dựng thông tin hàng hoá`. `ProductTakeRequest::authorize()` gọi `assertCanWrite()`.

Request:
```json
{ "product_ids": [101, 102, 103] }
```
Rule: `product_ids` `required|array|min:1|max:100` · `product_ids.*` `required|integer|distinct`. (Không `exists` — id lạ đưa vào `skipped`.)

Response 200 (kể cả khi không mã nào lấy được):
```json
{ "data": {
    "company_name": "CN Hải Phòng",
    "taken":   [ { "id": 101, "code": "TP-0001" } ],
    "skipped": [ { "id": 102, "code": "TP-0002", "reason": "already_used",       "message": "Công ty đang dùng hàng hoá này rồi" },
                 { "id": 103, "code": "TP-0003", "reason": "owner_not_trading",  "message": "Công ty tạo chưa kinh doanh hàng hoá này" } ] } }
```

Thứ tự xét từng mã (dừng ở lý do đầu tiên khớp):

| # | Điều kiện | Kết quả `reason` · `message` |
|---|---|---|
| 1 | id không tồn tại | `not_found` · "Không tìm thấy hàng hoá" (`code` = null) |
| 2 | `products.status ≠ 1` (0 / 2 / 5) | `erp_inactive` · "Hàng hoá đã xoá hoặc chưa duyệt ở ERP" (G9b) |
| 3 | `products.company_id = công ty mình` | `own_product` · "Hàng hoá do công ty mình tạo" |
| 4 | trạng thái công ty tạo (L3) ≠ 3 | `owner_not_trading` · "Công ty tạo chưa kinh doanh hàng hoá này" |
| 5 | đã có dòng của mình `status` NOT NULL (1/2/3/4) | `already_used` · "Công ty đang dùng hàng hoá này rồi" |
| 6 | có dòng của mình `status NULL` | UPDATE `status = 1, updated_by, updated_at` `WHERE id = ? AND status IS NULL`; 0 dòng ảnh hưởng (đua) ⇒ `already_used`; **không đụng `coefficient` + 4 ô** (L1, L2) ⇒ `taken` |
| 7 | chưa có dòng | `insertOrIgnore` `product_id, company_id = current_company_role, coefficient = 1, status = 1, created_by, updated_by, timestamps` (4 ô NULL — L2); 0 dòng ⇒ `already_used` ⇒ còn lại `taken` |

Mã lỗi:

| Ca | HTTP |
|---|---|
| Không có 1652 (mọi công ty) | **403** (middleware) |
| 1652 chỉ ở công ty khác công ty đang làm việc | **403** (`assertCanWrite`, R22) |
| `product_ids` thiếu / rỗng / > 100 / trùng / không phải số | **422** (`product_ids` / `product_ids.N`) |
| Mọi mã đều bị bỏ qua | **200**, `taken = []` (FE toast cảnh báo) |
| Lỗi DB khác | 500 — cả lô trong 1 transaction, không ghi nửa chừng |

Không ghi: `products` (mọi cột), `product_suppliers`, `product_business_catalogs`, dòng của công ty khác.

### 1.2 `PUT /api/v1/master-data/products/{product}/admin-data` (MỚI)

Route `->where('product','[0-9]+')`, middleware `checkPermission:Xây dựng thông tin hàng hoá`, đặt TRƯỚC `PUT /{product}`. `ProductAdminDataRequest`.

Request (chỉ đúng 1 khoá cấp 1):
```json
{ "admin": { "business_policy_id": 3, "min_stock_qty": 5, "guarantee": 12, "guarantee_type": "thang",
             "supplier_ids": [10, 11], "job_cluster_ids": [55] } }
```
Rule `admin.*` = chép 8 rule `ProductRequest.php:132-140` (dùng chung qua hằng/ham tĩnh, KHÔNG copy tay để khỏi lệch) + `checkClusters` (trait chung — D3/B2).

`authorize()` theo thứ tự (mọi nhánh 403 xảy ra TRƯỚC 422):
1. `assertCanWrite()` ⇒ 403 "Bạn không có quyền xây dựng thông tin hàng hoá ở công ty đang làm việc."
2. `Product::findOrFail` ⇒ **404**.
3. `assertCanEditAdmin($product)` (mới):
   - `products.status ≠ 1` ⇒ 403 "Hàng hoá đã bị xoá ở ERP, không sửa được." (D2)
   - không phải chủ **và** không có dòng của mình `status` NOT NULL ⇒ 403 "Công ty chưa lấy hàng hoá này về, không khai được dữ liệu quản trị."
   - dòng của mình `status = 4` ⇒ 403 "Hàng hoá đang ngừng kinh doanh, mở khoá trước khi sửa." (đồng bộ 2-C1; 423 để 2-C4 chốt)
4. Khoá lạ: `array_diff(array_keys($this->all()), ['admin'])` ≠ ∅ **hoặc** `array_diff(array_keys((array) $this->input('admin')), ADMIN_KEYS)` ≠ ∅ ⇒ **403** "Chỉ công ty tạo hàng hoá mới được sửa thông tin chung." (`ADMIN_KEYS` = 6 khoá trên; chặn cả `tech_coefficient`, `name`, `units`, `admin.coefficient`, `admin.status`, `admin.company_id`…)

Service `updateAdmin($product, $admin)`: `DB::transaction` → `writeAdmin($product, $admin, ProductCompany::STATUS_TRADING)` (nhánh có dòng: UPDATE 4 ô, giữ `coefficient`, KHÔNG đổi status ≠ NULL — H1'). Chủ gọi được (đi nhánh G4/D1 sẵn có) — xem tự quyết Q-A2.

Response 200 `{ id, code }` (giống `PUT /{product}`) · 422 thiếu `admin` / `admin.job_cluster_ids` rỗng (L5) / Tiểu mục mới thuộc nhánh khoá / rule sai kiểu.

### 1.3 `GET /products/{product}/edit` (SỬA)

- Thay `assertOwner()` bằng `assertCanEditAdmin()` (cùng 403 như 1.2 bước 3) — công ty lấy về mở được form; công ty chưa lấy về vẫn 403; không 1652 vẫn 403.
- `ProductFormResource` trả thêm: `edit_scope` = `'full'` (chủ) | `'admin'` (công ty lấy về) · `owner_company_id`. (`owner_company_name` đã có :35.)
- `PUT /{product}` (đầy đủ) GIỮ `assertOwner` ⇒ công ty lấy về gọi vào ⇒ 403 như cũ.

### 1.4 Cờ ở resource (SỬA)

| Cờ | Ở | Luật |
|---|---|---|
| `can_edit` | list + chi tiết | 1652 tại công ty đang làm việc ∧ `products.status = 1` ∧ trạng thái mình ≠ 4 ∧ (**chủ** ∨ **trạng thái mình ∈ {1,2,3} mà không phải chủ**) |
| `can_take_back` | **list** (4 màn, thực tế chỉ Kho dùng) | 1652 ∧ `products.status = 1` ∧ không phải chủ ∧ trạng thái mình NULL ∧ trạng thái công ty tạo (L3) = 3 |
| `edit_scope` | `/edit` | như 1.3 |

`owner_status` lấy từ cột SELECT mới trong `ProductService::index()` (biểu thức ở `Product::ownerStatusSql()`), KHÔNG lazy load. `PermissionService` gọi 1 lần / request (đã cache theo request ở 2-C1 — kiểm lại khi viết).

### 1.5 `GET /products/warehouse` (SỬA — L4)

`applyScreen` nhánh `SCREEN_WAREHOUSE` thêm `$query->where('products.status', '<>', Product::STATUS_DELETED)` cho MỌI `usage`. 3 màn kia không đổi (đã đòi `company_status` NOT NULL). Chi tiết `GET /{id}` hàng status 0 vẫn mở được (§35b-3).

---

## 2. Task BE (PHA 1)

### Task B1: Luật "trạng thái công ty tạo" (L3) — 1 chỗ duy nhất

**Files:** Modify `Entities/Product/Product.php` (cạnh `companyStatusSql` :381-389) · Test `Tests/Feature/ProductTakeApiTest.php` (khung + fixture).

- [x] Viết test trước: fixture `takeFixture()` trong `ProductTakeApiTest` (dùng `ActsAsProductUser::actAs`, `productTypeFixture` không cần) — chèn tay 1 hàng `products` của Cty A (`status 1`, không dòng nào) ⇒ owner 3; 1 hàng A có dòng chủ `status 1` ⇒ owner 1; 1 hàng A có dòng chủ `status NULL` ⇒ owner 3; 1 hàng A có dòng chủ `status 4` ⇒ owner 4; 1 hàng `status 0` ⇒ owner NULL. Ca `owner_status_suy_ra_dung_luat_2b` đọc qua `GET warehouse` (cần B3) — nên viết ca ở B3, B1 chỉ thêm hàm.
- [x] Thêm:
```php
/** Trạng thái của CÔNG TY TẠO (L3, 2-C2) — cùng luật suy ra với companyStatusSql. @TODO-BACKFILL gỡ cùng lúc. Cần leftJoin alias `pco`. */
public static function ownerStatusSql(): string
{
    return sprintf('COALESCE(pco.status, CASE WHEN products.status = %d THEN %d END)', self::STATUS_ACTIVE, ProductCompany::STATUS_TRADING);
}
public function scopeWithOwnerStatus(Builder $query): Builder
{
    return $query->leftJoin('product_company_coefficients as pco', function ($j) {
        $j->on('pco.product_id', '=', 'products.id')->on('pco.company_id', '=', 'products.company_id');
    })->addSelect(DB::raw(self::ownerStatusSql() . ' AS owner_status'));
}
```
- [x] Cập nhật docblock `scopeWithCompanyStatus` ("chỗ DUY NHẤT chứa luật suy ra" ⇒ "2 chỗ cạnh nhau: company + owner").

**Xong khi:** hàm có, `php -l` sạch; dùng được ở B2/B3.

### Task B2: `POST products/take` (L1, L2, L3, G9b)

**Files:** Create `Http/Requests/Product/ProductTakeRequest.php` · Modify `ProductWriteService.php` (thêm `take(array $ids): array`), `ProductWriteController.php` (`take`), `Routes/api.php` · Test `ProductTakeApiTest.php`.

- [x] **Test trước (đỏ)** — `DatabaseTransactions` + `ActsAsProductUser`; công ty A = 1 (chủ), B = 6 (`company_role` 6, `info->company_id` khác — chứng minh gán tay):
  1. `lay_ve_ma_chua_co_dong_tao_dong_coef_1_status_1` — 1 dòng `company_id = 6`, `coefficient 1`, `status 1`, 4 ô NULL (**L2**), `products` không đổi cột nào (so snapshot `(array) DB::table('products')->find($id)`).
  2. `lay_ve_ma_co_dong_he_so_cu_update_giu_coefficient` — dòng B `status NULL, coefficient 1.03, guarantee NULL` ⇒ `status 1`, **coefficient vẫn 1.03**, số dòng không tăng (**L1**).
  3. `lay_ve_khong_chep_cot_chung_vao_4_o` — hàng có `products.guarantee = 24, min_stock_qty = 3` ⇒ dòng mới 4 ô NULL; list `/company` của B trả `guarantee_text = null` (**L2** đã chấp nhận).
  4. `lo_hon_hop_chi_lay_ma_hop_le_va_bao_ly_do` — 1 lô: id lạ · `status 0` · `status 5` · hàng của B · hàng A mà dòng chủ `status 1` (**công ty tạo chưa kinh doanh — L3**) · hàng A dòng chủ `status 4` · hàng A mà B đã có dòng `status 3` · 1 mã hợp lệ ⇒ `taken` đúng 1, `skipped` đúng 7 mã với `reason` lần lượt `not_found, erp_inactive, erp_inactive, own_product, owner_not_trading, owner_not_trading, already_used`; dòng `status 3` của B không bị lùi.
  5. `dong_chu_status_null_tinh_la_dang_kinh_doanh` — hàng A có dòng chủ `status NULL` (hệ số cũ chủ) ⇒ lấy được (L3 suy ra 3).
  6. `qua_100_ma_hoac_rong_bi_422` — 101 id ⇒ 422 `product_ids`; `[]` ⇒ 422; `[1,1]` ⇒ 422 (distinct); 0 dòng ghi.
  7. `khong_quyen_1652_bi_403` — `actAs(6, ['Xem dữ liệu hàng hoá công ty'])` ⇒ 403, 0 dòng ghi.
  8. `quyen_1652_chi_o_cong_ty_khac_bi_403` — role 1652 gắn `company_id = 1`, user làm việc ở 6 ⇒ 403 (R22).
  9. `lay_ve_2_lan_lan_sau_bao_dang_dung` — lần 2 `skipped already_used`, không 500, vẫn 1 dòng.
  10. `sau_lay_ve_hien_o_entering_company_khong_o_unused_trading` — `/entering`, `/company` của B có mã; `/warehouse?usage=unused` không; `/trading` không; catalog popup `catalogs/products?tab=add` (1655) có.
  11. `tat_ca_bi_bo_qua_van_200_taken_rong`.
- [x] Chạy ⇒ đỏ đúng lý do (route 404).
- [x] Viết `ProductTakeRequest` (authorize = `assertCanWrite`; rules mục 1.1; messages tiếng Việt "Mỗi lượt chỉ lấy về tối đa 100 mã hàng").
- [x] `ProductWriteService::take()` — 1 transaction: 1 query `products` (id, code, status, company_id) `whereIn` + `withOwnerStatus()`; 1 query dòng của mình `whereIn product_id, company_id = mình`; vòng lặp xét theo bảng 1.1; UPDATE kẹp `whereNull('status')`, INSERT `insertOrIgnore`; trả `['company_name' => …, 'taken' => […], 'skipped' => […]]` giữ thứ tự id gửi lên.
- [x] Controller `take(ProductTakeRequest $r)` → `responseJson('success', 200, …)`. Route `Route::post('/take', $write . '@take')->middleware('checkPermission:' . $build);` đặt trước `POST /`.
- [x] Chạy ⇒ 11/11 xanh.

**Xong khi:** 11 ca xanh; `grep -n "upsert\|updateOrInsert" ProductWriteService.php` = 0.

### Task B3: Kho dữ liệu lọc status 0 (L4) + `can_take_back` + `owner_status`

**Files:** Modify `Services/Product/ProductService.php` (`index()` :61-97 thêm `->withOwnerStatus()`; `applyScreen` warehouse :178-185) · `Transformers/Product/ProductListResource.php` · Test `ProductTakeApiTest.php`.

- [x] Test trước:
  12. `kho_khong_tra_hang_status_0_van_tra_status_2_5` — hàng `status 0` không có trong `/warehouse` (cả `usage` trống/`unused`/`used`); hàng `status 5` có, `can_take_back = false`.
  13. `can_take_back_dung_4_phia` — B có 1652: hàng A owner 3 ⇒ true; hàng A owner 1 ⇒ false; hàng B tự tạo ⇒ false; hàng B đã lấy về ⇒ false. B **không** 1652 (chỉ 1653) ⇒ false ở mọi dòng.
  14. `owner_status_suy_ra_dung_luat_2b` — 5 hàng fixture B1 ra đúng `owner_status` 3/1/3/4/NULL (đọc qua cột `owner_status` không lộ ra response — assert gián tiếp qua `can_take_back` hoặc thêm khoá tạm trong test bằng query trực tiếp `Product::withOwnerStatus()`).
- [x] Sửa code; cột `owner_status` chỉ dùng nội bộ (không trả ra JSON).
- [x] Hồi quy `ProductReadApiTest` (đặc biệt `kho_du_lieu_loc_tinh_trang_su_dung…` :108) + `ProductCatalogApiTest`.

**Xong khi:** 14/14 + hồi quy Read xanh; đếm query `/warehouse?per_page=100` không tăng so với trước (đo `DB::enableQueryLog` trong 1 ca hoặc tay — leftJoin, không N+1).

### Task B4: Nới `GET edit` + `edit_scope` + `can_edit` cho công ty lấy về

**Files:** Modify `ProductWriteService.php` (thêm `assertCanEditAdmin(Product): void`, `editScope(Product): string`) · `ProductWriteController::edit` :31-46 · `Transformers/Product/ProductFormResource.php` · `ProductListResource.php` :59-63 · `ProductDetailResource.php` :43-47 · (`AdminData.php` nếu giữ Q-A3) · Test `ProductTakeApiTest.php`.

- [x] Test trước:
  15. `cong_ty_lay_ve_mo_form_edit_scope_admin` — B lấy về ⇒ `GET /{id}/edit` 200, `edit_scope = admin`, `owner_company_id = 1`, `admin` 4 ô **NULL** (không lùi cột chung — Q-A3).
  16. `chu_mo_form_edit_scope_full` — chủ ⇒ `full`.
  17. `chua_lay_ve_hoac_khong_quyen_mo_form_403` — B chưa lấy về ⇒ 403; B lấy về nhưng không 1652 ⇒ 403; B lấy về, dòng B `status 4` ⇒ 403; `products.status 0` ⇒ 403.
  18. `can_edit_mo_cho_cong_ty_lay_ve` — list `/entering` + chi tiết của B: `can_edit = true`; B không 1652 ⇒ false; công ty C chưa dùng ⇒ false; dòng B `status 4` ⇒ false.
  19. `cong_ty_lay_ve_put_day_du_van_403` — B `PUT /{id}` nguyên form ⇒ 403 (giữ `assertOwner`).
- [x] Sửa code. Hồi quy `ProductWriteApiTest` — đặc biệt `cong_ty_khac_sua_bi_403_ca_edit_lan_put` (:264, công ty khác CHƯA lấy về ⇒ vẫn 403) và `can_edit_theo_quyen_va_cong_ty_tao` (:490).

**Xong khi:** 19/19 + `ProductWriteApiTest` toàn bộ xanh.

### Task B5: `PUT products/{id}/admin-data` (L5, T6)

**Files:** Create `ProductAdminDataRequest.php` (+ trait `Concerns/ChecksCatalogClusters.php`) · Modify `ProductRequest.php` (dùng trait + hằng rule admin dùng chung), `ProductWriteService.php` (`updateAdmin`), `ProductWriteController.php` (`updateAdmin`), `Routes/api.php` · Test `ProductTakeApiTest.php`.

- [x] Test trước:
  20. `cong_ty_lay_ve_luu_tab_quan_tri_dung_cong_ty` — B ghi 4 ô + 2 NCC + 1 Tiểu mục ⇒ dòng B có 4 ô; `product_suppliers`/`product_business_catalogs` của B đúng; của A **không đổi** (snapshot); `coefficient` + `status` B không đổi (vẫn 1 — H1').
  21. `dong_he_so_cu_lay_ve_roi_luu_van_giu_coefficient` — B có dòng `1.03` ⇒ lấy về ⇒ Lưu ⇒ `coefficient` 1.03.
  22. `gui_field_lop_chung_bi_403_khong_ghi_gi` — `name` · `units` · `tech_coefficient` · `admin.coefficient` · `admin.status` (mỗi khoá 1 lượt) ⇒ 403, `products` + dòng B + NCC + catalog không đổi.
  23. `thieu_catalog_bi_422` — `admin.job_cluster_ids = []` ⇒ 422 `admin.job_cluster_ids` (**L5**); thiếu hẳn `admin` ⇒ 422.
  24. `tieu_muc_nhanh_khoa_them_moi_422_da_luu_thi_giu` (D3/B2 — chép khuôn ca tương ứng ở `ProductWriteApiTest`).
  25. `chua_lay_ve_hoac_khong_quyen_admin_data_403` — chưa lấy về · không 1652 · 1652 ở công ty khác · status 4 · `products.status 0` ⇒ 403; id lạ ⇒ 404; **403 trước 422** (payload sai + chưa lấy về ⇒ 403).
  26. `chu_goi_admin_data_di_nhanh_g4` — chủ hàng cũ chưa có dòng, đổi 1 ô ⇒ sinh dòng `coef 1, status 3` (giữ nguyên hành vi 2-C1).
- [x] Sửa code; rule admin lấy từ 1 nguồn (vd `ProductRequest::adminRules(): array` static) — `ProductRequest::rules()` gọi lại hàm này.
- [x] Route `Route::put('/{product}/admin-data', $write . '@updateAdmin')->where('product','[0-9]+')->middleware(...)` trước `PUT /{product}`.

**Xong khi:** 26/26 xanh; `ProductWriteApiTest` vẫn xanh (rule admin không lệch).

### Task B6: Hồi quy + review BE

- [x] Chạy `ProductTakeApiTest`, `ProductWriteApiTest`, `ProductReadApiTest`, `ProductCatalogApiTest`, `ProductCompanyFoundationTest`, `ProductFormOptionsTest` — ghi số ca vào Checkpoint.
- [x] `route:list --path=master-data/products` (không `route:cache`): `take` + `admin-data` đứng trước `/{product}`.
- [x] Tự review: không `fill($request->all())`; không ghi `products`; `company_id` gán tay; 403 trước 422.
- [x] Hỏi user commit PHA 1.

---

## 3. Task FE (PHA 2)

### 3.1 Tự chốt UI (từ `c2-khao-sat-fe.md` §4, đã chỉnh theo L1–L7)

| # | Tự chốt |
|---|---|
| T1 | Lấy về 1 dòng: cột *Hành động* ở Kho (chỉ thêm khi có 1652), `V2BaseRowActions` action `{ key: 'take_back', title: 'Lấy về', icon: 'ri-download-2-line', visible: !!item.can_take_back }`; mã hàng vẫn là link chi tiết, không nút *Xem* |
| T2 | Ô tick chỉ ở dòng `can_take_back`; tick đầu bảng chỉ tick các dòng đó của trang; giữ tick qua trang (`listSelected`); trần **100** — vượt thì toast cảnh báo `Mỗi lượt chỉ lấy về tối đa 100 mã hàng — hãy lấy lượt này rồi chọn tiếp`, ô vừa bấm trả về chưa tick (khuôn `TICK_CAP` + `tickRev` của `ProductCatalogBuilderModal.vue`) |
| T3 | `$confirm` cho cả 1 dòng và hàng loạt, trước lớp tải: tiêu đề *Xác nhận lấy về*; 1 dòng `Lấy hàng hoá <mã> về <công ty đang làm việc>? Hàng sẽ ở trạng thái Đang nhập thông tin.`; hàng loạt `Lấy <N> hàng hoá đã chọn về <công ty>? …`; `textAccept: 'Lấy về'`, không `danger` |
| T4 | Thanh `#left-actions` ở Kho: `Đã chọn N hàng hoá` · **Lấy về công ty** (primary, `btn-compact`, `ri-download-2-line`) · **Bỏ chọn** (tertiary). Xong: toast success `Đã lấy <mã> về <công ty> — trạng thái Đang nhập thông tin` / `Đã lấy <n> hàng hoá về <công ty> — trạng thái Đang nhập thông tin`; có `skipped` ⇒ thêm toast cảnh báo `Bỏ qua <k> mã: <mã> (lý do)…` (≤ 5 mã, còn lại "và x mã khác"); `taken = 0` ⇒ chỉ toast cảnh báo. Xoá tick, `loadData()`, ở lại màn |
| T5 | Form `edit_scope = admin`: mở thẳng tab *Quản trị*; tab cha *Thông tin hàng hoá* mờ (prop `lockedKeys`, `opacity .4`) nhưng bấm được, hiện **chỉ đọc** bằng `ProductTabGeneral/Specs/Purchase/Vehicles/Machines` (gọi thêm `GET products/{id}`), đi được 5 step; 12 component form 2-C1 KHÔNG render (`v-if`) ⇒ không validate ẩn |
| T6 | Dải báo trên thẻ tab: `ri-information-line` + `Hàng hoá do <b>{owner_company_name}</b> tạo — chỉ khai được tab <b>Quản trị hàng hoá</b>.`; nền `#f5f8fc`, viền `#e3ebf5`, bo 6px, đệm 8px 12px, chữ 12px `#374151` (xám, không đỏ) |
| T7 | (popup lối b) — **KHÔNG làm** (L6) |
| T8 | Lưu ở mức `admin`: `PUT products/{id}/admin-data` body `toAdminPayload(form)` = `{ admin: {...} }` (không `tech_coefficient`); ô Hệ số công nghệ `disabled` + hint giữ nguyên; toast `Đã lưu hàng hoá <mã>`, sang chi tiết như 2-C1 |
| T9 (mới, L6) | Màn *Hàng hoá nhập thông tin*: nút secondary **Kho dữ liệu** (icon `ri-database-2-line`, tooltip `Lấy hàng hoá của công ty khác về — mở Kho dữ liệu, chỉ hàng công ty chưa dùng`), đứng trước *Tạo mới*, chỉ hiện khi có 1652; bấm ⇒ `router.push('/master-data/products/warehouse?usage=unused')`; Kho đọc `?usage=unused` lúc khởi tạo để bật sẵn công tắc |

### Task F1: Kho dữ liệu — ô tick, thanh chọn, action *Lấy về* (T1–T4)

**Files:** `utils/product-list-screens.js` (warehouse: `rowActions: true`, cờ `takeBack: true`) · `components/product/ProductListPage.vue` · `pages/master-data/products/warehouse.vue` (docblock bỏ "CHỈ ĐỌC").

- [ ] **Tái hiện trước (Playwright MCP):** Kho dữ liệu hiện 0 ô tick, 0 cột Hành động, tổng có cả hàng status 0 (đo `meta.total` trước/sau B3).
- [ ] `canTakeBack = screen.takeBack && hasAPermission('Xây dựng thông tin hàng hoá')`; `canSelectRows = canBuildCatalog || canTakeBack`; tách cột `checkbox`, `#header-checkbox`, `#cell-checkbox` khỏi `canBuildCatalog` (ô tick dòng thêm điều kiện `item.can_take_back` khi ở Kho); thanh `#left-actions` 2 nhánh (Xếp catalog / Lấy về công ty).
- [ ] Cột `actions` ở Kho chỉ push khi `canTakeBack` (giữ ca E2 không quyền: 0 cột Hành động); `#cell-actions` truyền action theo màn (`edit` ở company/entering, `take_back` ở warehouse).
- [ ] Trần 100; `$confirm`; `apiPostMethod({ url: 'master-data/products/take', payload: { product_ids } })`; lớp tải; toast; reset tick; `loadData()`.
- [ ] Khởi tạo `filters.usage` từ `$route.query.usage === 'unused'` — kiểm bẫy *nuốt lần lọc đầu* (memory `hrm-list-page-2-loi-bo-loc-am-tham`): đếm request list khi mở `?usage=unused` phải đúng **1** và có `usage=unused`.

**Xong khi:** đo MCP mục 3.3 dòng K1–K6 đạt.

### Task F2: Nút **Kho dữ liệu** ở màn Nhập thông tin (T9 / L6)

**Files:** `ProductListPage.vue` (slot `#actions`, `screen.slug === 'entering'`), `utils/product-list-screens.js` nếu cần cờ.

- [ ] Nút chỉ khi 1652; bấm ⇒ sang Kho, công tắc bật, lưới chỉ hàng chưa dùng.

**Xong khi:** MCP: nút có 1 cái (có quyền) / 0 (không quyền); sau bấm URL `…/warehouse?usage=unused`, công tắc `checked`, request list có `usage=unused`.

### Task F3: Form chế độ `admin` (T5, T6, T8)

**Files:** `components/product/form/ProductForm.vue` · `ProductFormAdmin.vue` (prop `adminOnly` ⇒ Hệ số công nghệ `disabled`) · `productFormModel.js` (`toAdminPayload`) · `components/product/detail/ProductParentTabs.vue` (prop `lockedKeys`, chỉ CSS mờ).

- [ ] Đọc `edit_scope` từ `/edit`; `admin` ⇒ `parentTab = 'admin'`, dải báo, tab Thông tin = 5 `ProductTab*` chỉ đọc + `ProductStepTabs` đi được 5 step; `save()` rẽ `admin-data`.
- [ ] `openFirstErrorTab`: ở `admin` luôn ở tab Quản trị (lỗi 422 chỉ có `admin.*`).
- [ ] Không đổi gì luồng `full` (hồi quy 2-C1).

**Xong khi:** MCP F-mục 3.3 dòng U1–U6 đạt.

### Task F4: Lối vào Sửa cho công ty lấy về

**Files:** không sửa nếu B4 đúng (menu dòng `entering`/`company` + footer chi tiết đều theo `can_edit`).

- [ ] MCP: B (Cty 1 lấy về hàng Cty 4) thấy Sửa ở menu dòng 2 màn + footer chi tiết; bấm ⇒ form `admin`.

### Task F5: Kiểm tổng bằng Playwright MCP (bắt buộc trước khi báo xong)

### 3.3 Bảng đo DOM (Playwright MCP — số lấy từ DOM / request, không nhìn ảnh)

Chuẩn bị: api 8031 + Nuxt 3031 của worktree (memory: node 12 heap 8192, kill theo PID cổng). Tài khoản admin e2e (Cty 1, có 1652). Chọn mã fixture: `SELECT p.id FROM products p WHERE p.status=1 AND p.company_id=4 AND NOT EXISTS (SELECT 1 FROM product_company_coefficients c WHERE c.product_id=p.id AND c.company_id IN (1,4)) LIMIT 3` — ghi id trước, dọn bằng `DELETE FROM product_company_coefficients WHERE product_id IN (…) AND company_id = 1` (+ `product_suppliers`/`product_business_catalogs` cùng điều kiện) sau khi đo. **Hỏi riêng trước khi ghi.**

| # | Đo | Kỳ vọng |
|---|---|---|
| K1 | Kho: số `tbody input[type=checkbox]` vs số dòng API `can_take_back = true` của trang | bằng nhau; dòng còn lại 0 ô tick |
| K2 | `meta.total` Kho trước/sau B3 | giảm đúng số hàng status 0 (≈ 17.512 trên DB local); `SELECT COUNT(*)` đối chiếu |
| K3 | Bấm action *Lấy về* 1 dòng → popup confirm: tiêu đề + câu có mã + tên công ty; Huỷ ⇒ 0 POST `take` | đếm request |
| K4 | Đồng ý ⇒ đúng 1 POST, body `product_ids` 1 phần tử; toast đúng chữ; badge dòng → *Đang nhập thông tin* (đo `textContent` + `getComputedStyle(color)` = màu `#64748B`); dòng mất ô tick + action | |
| K5 | Tick 3 ⇒ thanh `Đã chọn 3 hàng hoá`; *Lấy về công ty* ⇒ 1 POST 3 phần tử; thanh ẩn (0 phần tử `.product-bulk-bar`) | |
| K6 | Trần: dựng 100 tick (per_page 100) rồi tick thêm ở trang 2 ⇒ toast cảnh báo, đếm vẫn 100, ô vừa bấm `checked = false` | |
| K7 | Bố cục: thanh chọn không đè hàng tiêu đề / bảng (toạ độ `getBoundingClientRect`), cột Hành động 90px, `th` 1 dòng (`white-space: nowrap`) | |
| U1 | Form B: tab cha active = *Quản trị*; dải báo có `owner_company_name` đúng; `getComputedStyle` nền `rgb(245, 248, 252)` | |
| U2 | Tab *Thông tin* `opacity` = `0.4`; bấm vào ⇒ số `input:not([disabled]), select:not([disabled]), textarea:not([disabled])` trong vùng Thông tin = **0**; đi được 5 step | |
| U3 | Ô Hệ số công nghệ `disabled = true` | |
| U4 | Lưu ⇒ đúng 1 PUT `…/admin-data`, body `Object.keys` = `['admin']`, không `tech_coefficient`; toast `Đã lưu hàng hoá <mã>`; chi tiết: trạng thái vẫn *Đang nhập thông tin* | |
| U5 | Lưu thiếu catalog ⇒ chấm đỏ tab Quản trị, `.v2-error` ở ô catalog, không PUT thứ 2 | |
| U6 | Hồi quy chủ: form hàng Cty 1 mở tab *Thông tin*, 0 dải báo, Hệ số công nghệ sửa được, PUT `/{id}` | |
| N1 | Không quyền (tài khoản `e2e_cmd_noperm` + role tạm 1653): Kho 0 ô tick, 0 cột Hành động, 0 chữ *Lấy về*; Nhập thông tin 404 như cũ; console không lỗi | |

---

## 4. e2e (PHA 3)

### Task E1: Sửa spec hiện có

- [ ] `products-read-ui.spec.ts`:
  - `:19` bộ cột `warehouse` thêm `'Hành động'` cuối (tài khoản admin có 1652); tiêu đề cột tick rỗng chữ đã bị `filter(Boolean)` lọc.
  - `:30` giữ `WRITE_BUTTONS`; `:73` `allowed` thêm nhánh `screen === 'warehouse' ? /Lấy về công ty|Lấy về/g` và `entering` thêm `Kho dữ liệu` (không khớp `WRITE_BUTTONS` sẵn — chỉ ghi chú). Sửa comment dòng 71-72 nêu lối ghi 2-C2.
- [ ] `products-form-ui.spec.ts` E2 (`:233-245`): giữ — tài khoản role rỗng không 1652 ⇒ vẫn 0 cột Hành động. Chỉ sửa câu mô tả nếu cần.

### Task E2: Spec mới (viết sẵn, `--list` OK, chạy khi user yêu cầu, `--project=chromium --no-deps --workers=1`)

`tests/master-data/products-take.api.spec.ts` (serial, `beforeAll` chọn mã fixture bằng `runMysql`, `afterAll` DELETE dòng đã ghi + `flushApiPermissionCache()`):

| # | Ca |
|---|---|
| A1 | admin (Cty 1) `POST take` 1 mã Cty 4 chưa dùng ⇒ 200 `taken` 1; DB: dòng Cty 1 `status 1`, `coefficient 1`, 4 ô NULL |
| A2 | dòng hệ số cũ: chèn tạm dòng Cty 1 `status NULL, coefficient 1.03` cho mã thứ 2 ⇒ take ⇒ `coefficient` 1.03, số dòng không tăng |
| A3 | lô hỗn hợp: mã status 0 · mã Cty 1 tự tạo · mã vừa lấy (A1) · mã Cty 4 có dòng chủ `status 1` chèn tạm (L3) ⇒ đúng `reason` từng mã |
| A4 | 101 id ⇒ 422; `[]` ⇒ 422 |
| A5 | **không quyền**: `e2e_cmd_noperm` + role tạm **chỉ 1653** (`E2E C2 tạm - chỉ xem hàng công ty`) + `cache:clear` ⇒ `GET company` 200 (chứng minh có quyền xem) nhưng `POST take` 403, `GET /{id}/edit` 403, `PUT admin-data` 403; DB không đổi |
| A6 | `PUT admin-data` kèm `name` / `tech_coefficient` ⇒ 403, `products` không đổi (so `runMysql` trước/sau); body chuẩn ⇒ 200, dòng Cty 1 đúng 4 ô, `status` vẫn 1 |
| A7 | `GET warehouse?keyword=<mã status 0>` ⇒ 0 dòng |

`tests/master-data/products-take-ui.spec.ts` (serial): ca **K1, K3–K6, U1–U5, N1** ở bảng 3.3 (+ K7 bố cục: đo toạ độ thanh chọn vs bảng; memory *e2e-ui-phai-kiem-khuon-giao-dien*). Ô tick: bấm toạ độ input (label 0×0 — memory *e2e-viewport-1280*); nút V2BaseButton chọn theo locator `hasText` chuẩn hoá khoảng trắng; chờ `waitForResponse` của `take`/`admin-data`, KHÔNG `networkidle`.

- [ ] `npx playwright test products-take --list` (Node 20) OK; chép 3 file về `HRM/e2e/tests/master-data/`.
- [ ] ⚠️ Khi chạy: bộ `serial` — đọc dòng tổng kết, "did not run" ≠ passed (CLAUDE.md root).

---

## 5. Rủi ro + việc ngoài luồng

### 5.1 Rủi ro đợt này

| # | Rủi ro | Né / test |
|---|---|---|
| R1 | `upsert`/`updateOrInsert` đè `coefficient` dòng hệ số cũ ⇒ **đổi giá ERP im lặng** | cấm; ca 2, 21, A2 |
| R2 | UPDATE dòng `status` NOT NULL ⇒ lùi trạng thái | `whereNull('status')`; ca 4 |
| R3 | Hook `BaseModel::creating` gán `info->company_id` | `DB::table` + gán tay; ca 1 dùng user `company_role ≠ info->company_id` |
| R4 | `admin-data` lọc bớt field thay vì 403 ⇒ thủng khi thêm field | whitelist + 403; ca 22 |
| R5 | `AdminData::formValues` lùi `guarantee`/`guarantee_type` về cột chung khi dòng có NULL ⇒ form công ty lấy về hiện bảo hành của cột chung trong khi list hiện trống, Lưu là ghi luôn giá trị đó (trái L2) | Q-A3: công ty lấy về đọc dòng NGHIÊM (không lùi); ca 15 |
| R6 | Luật suy ra trạng thái nằm 2 chỗ (company + owner) ⇒ backfill gỡ 1 chỗ quên chỗ kia | đặt cạnh nhau trong `Product.php`, cùng `@TODO-BACKFILL` |
| R7 | Kho đọc `?usage=unused` lúc mở dễ dính lỗi nuốt lần lọc đầu / bắn 2 request | đếm request ở F1 |
| R8 | Tab Thông tin chỉ đọc gọi thêm `GET /{id}` ⇒ 2 request lúc mở form `admin` | chấp nhận (chỉ ở `admin`); đo thời gian mở form < 2s dev |
| R9 | Thêm cột Hành động ở Kho làm vỡ ca `products-read-ui` (bộ cột) | E1 sửa cùng lúc; chạy lại TOÀN BỘ spec màn khi user cho chạy |
| R10 | Dữ liệu thật bị lấy về khi kiểm MCP/e2e quên dọn ⇒ hàng Cty 4 hiện ở màn Nhập thông tin Cty 1 | ghi id trước, DELETE theo id; checkpoint ghi "đã dọn: 0 dòng còn" |
| R11 | `products.status = 2/5` vẫn hiện ở Kho nhưng không lấy được | `can_take_back = false`; 7 mã — chấp nhận (L4 chỉ lọc 0) |

### 5.2 Việc ngoài luồng mới (thêm vào `chot.md` khi user duyệt)

| # | Việc | Nguồn |
|---|---|---|
| N15 | 3 nhân viên `company_role ≠ info->company_id`: HRM ghi dòng hàng × công ty theo `company_role`, popup ERP (`SearchController.php:403`) đọc hệ số theo `info->company_id` ⇒ hàng lấy về của họ lệch giá/hệ số giữa 2 bên | khảo sát BE §2.4 |
| N16 | `AdminData::formValues` (2-C1) lùi từng ô bảo hành về cột chung khi dòng có NULL ⇒ form công ty TẠO hiện bảo hành khác với list/chi tiết (đọc dòng); 2-C2 chỉ sửa nhánh công ty lấy về (Q-A3), nhánh chủ để nguyên | đọc code 08/10 |
| N17 | Hàng HRM mới tạo (dòng chủ `status 1`) **không lấy về được** tới phase Tính giá (L3 + H1') — phase Tính giá phải mở lại luồng lấy về cho hàng này; e2e/tester cần biết | L3 × H1' |

(N1–N14 không đổi; N2/N4 — ERP form hàng hoá + Hãng SX xoá sạch `product_company_coefficients` — nay ảnh hưởng thêm dòng "đã lấy về" của công ty khác, nhắc lại khi plan 2-D.)

---

## 6. Điểm tự quyết chưa có chốt (đưa user xem khi duyệt plan — đều đổi được không tốn)

| # | Tự quyết | Lý do |
|---|---|---|
| Q-A1 | `take` mọi mã bị bỏ qua vẫn **200** `taken = []` (không 422); id lạ vào `skipped not_found` (không 422 cả lô) | ngữ nghĩa "bỏ qua từng mã" của L3/khảo sát; FE 1 nhánh xử lý |
| Q-A2 | `admin-data` cho cả **chủ** gọi (đi nhánh G4/D1), FE chỉ dùng cho công ty lấy về | 1 luật `assertCanEditAdmin`; không thêm 403 vô nghĩa |
| Q-A3 | Form công ty lấy về đọc 4 ô **nghiêm từ dòng** (không lùi cột chung như `formValues` của chủ) | giữ đúng L2 "để trống"; không lén ghi cột chung sang dòng khi Lưu |
| Q-A4 | Khoá lạ trong `admin.*` (vd `admin.coefficient`, `admin.status`) cũng **403** như khoá cấp 1 | chặn ghi hệ số/trạng thái qua cửa sau |
| Q-A5 | Dòng chủ `status 4` (Ngừng KD) ⇒ `owner_not_trading` (không lấy về được) | L3 "= 3" đọc nguyên văn; G6 khoá theo công ty nhưng L3 mới hơn |
| Q-A6 | `can_take_back` chỉ ở resource **danh sách**; chi tiết không có nút Lấy về | mockup chỉ có lối Kho; L6 hoãn popup |
| Q-A7 | Nhãn nút L6 **"Kho dữ liệu"** (điều hướng, không phải nút ghi) | ≤ 3 chữ theo skill button-convention; tránh khớp `WRITE_BUTTONS` |
| Q-A8 | Hàng `products.status 2/5` vẫn ở Kho (chỉ lọc 0 theo L4) | L4 nguyên văn "status = 0" |

---

## 7. Checkpoint

<!-- Điền khi làm: ngày · vừa xong · đang dở · bước tiếp · blocked. Ghi số ca PHPUnit/e2e (đọc dòng tổng kết), id dữ liệu đã ghi + đã dọn. -->

**08/10/2026 — PHA 1 (BE) XONG** · worktree `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/p2c2-lay-ve`, commit **`2739d0379`** (chưa push, chưa merge).

- B1–B6 xong. `ProductTakeApiTest` **26/26** (252 assertions) — đỏ trước đúng lý do (route 404 / thiếu scope) rồi xanh.
- Hồi quy xanh như trước: `ProductWriteApiTest` 34 · `ProductReadApiTest` 8 · `ProductCatalogApiTest` 6 · `ProductCompanyFoundationTest` 5 · `ProductFormOptionsTest` 4 · `BusinessCatalogTreeTest` 12 · `ProductClassificationCatalogTest` 11 · `ProductCodeGeneratorTest` 9 · `ProductImageUploadTest` 4 · `ProductNatureAutoPartsTest` 2 · `ProductCatalogBaseTest` 6 ⇒ **101/101**. Tổng **127/127**.
- Thứ tự route (đọc `app('router')->getRoutes()` — `route:list` nổ vì controller khác ngoài luồng): `POST /take` và `PUT /{product}/admin-data` đứng trước `PUT/GET /{product}`.
- `/warehouse?per_page=100`: 10 query cố định (leftJoin `pco`, không N+1); `meta.total` = 28.378 = `COUNT(*) WHERE status <> 0`.
- DB `hrm_erp` sạch sau test: `product_company_coefficients` 1.105 dòng, 0 dòng `status` NOT NULL; `business_policies` 0; không còn hàng fixture.
- Lệch nhỏ so với plan (không đổi hợp đồng): (1) whitelist `admin.*` không chép tay hằng `ADMIN_KEYS` mà suy từ `ProductRequest::adminRules()` (`ProductAdminDataRequest::adminKeys()`); (2) cờ `can_edit`/`can_take_back` gom vào `Product::editableAt()` / `takeableAt()` dùng chung list + chi tiết; (3) Q-A3 làm trong `AdminData::formValues` (nhánh không phải công ty tạo có dòng ⇒ đọc nghiêm), nhánh chủ giữ nguyên (N16).
- ⚠️ Cho PHA 2 (FE): `GET /edit` trả `admin.catalogs` (hiển thị) — `toAdminPayload` KHÔNG được gửi khoá này (khoá lạ ⇒ 403). Body chỉ 6 khoá: `business_policy_id, min_stock_qty, guarantee, guarantee_type, supplier_ids, job_cluster_ids`.
- Bước tiếp: PHA 2 (FE F1–F5) — chờ user cho phép riêng.

**08/10/2026 — F5 kiểm Playwright MCP trên app thật** · api 8031 (hrm-api `2739d0379`) + Nuxt 3031 (hrm-client `3a9eae100`), viewport 1280×800, tài khoản `e2e_assign` (Cty 1, Super admin có 1652). Không chạy test runner. **Không phát hiện lỗi code ⇒ không commit.**

| # | Số đo từ DOM / request | Kết quả |
|---|---|---|
| K0 | Nhập thông tin: nút "Kho dữ liệu" đứng trước "Tạo mới"; bấm ⇒ URL `/warehouse?usage=unused`, **1** request list (`…&usage=unused`), công tắc "Chỉ hàng công ty chưa dùng" `checked = true`. Mở thẳng URL `?usage=unused`: cũng 1 request | ĐẠT |
| K1 | `?usage=unused`: 20 dòng, 20 `can_take_back` ⇒ 20 ô tick + 20 nút "Lấy về", tập id trùng khớp. Không lọc: 20 dòng, 2 `can_take_back` ⇒ 2 ô tick + 2 nút, id khớp; 1 ô tick đầu bảng; cột "Hành động" có | ĐẠT |
| K2 | `meta.total` Kho = 28.378 = `COUNT(*) WHERE status <> 0` (17.512 mã status 0 bị lọc) | ĐẠT |
| K3 | Popup "Xác nhận lấy về": "Lấy hàng hoá SG-VT-NM0102 về CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT? Hàng sẽ ở trạng thái Đang nhập thông tin.", nút [Lấy về, Hủy]; Hủy ⇒ 0 modal, **0 POST** | ĐẠT |
| K4 | Đồng ý ⇒ 1 POST body `{product_ids:[50061]}` 200; toast "Đã lấy SG-VT-NM0102 về CÔNG TY CỔ PHẦN… — trạng thái Đang nhập thông tin"; badge "Đang nhập thông tin" color `rgb(100, 116, 139)` nền `rgba(100,116,139,.1)`; dòng còn 0 ô tick, 0 nút | ĐẠT |
| K5 | Tick 3 ⇒ thanh "Đã chọn 3 hàng hoá · Lấy về công ty · Bỏ chọn"; popup "Lấy 3 hàng hoá đã chọn về …"; **1 POST** body 3 mã `[49985,49999,50060]` (bắt ở `page.route`; để giữ trần 3 mã ghi thật, body gửi đi được thay bằng `[50060,49999,50061]`) ⇒ taken 2 + skipped `already_used` ⇒ 2 toast: "Đã lấy 2 hàng hoá về …" + "Bỏ qua 1 mã: SG-VT-NM0102 (Công ty đang dùng hàng hoá này rồi)"; sau đó 0 `.product-bulk-bar`, 0 ô đang tick | ĐẠT |
| K6 | per_page 100, tick đầu bảng ⇒ "Đã chọn 100"; trang 2 bấm 1 ô ⇒ toast "Mỗi lượt chỉ lấy về tối đa 100 mã hàng — hãy lấy lượt này rồi chọn tiếp", ô `checked=false`, vẫn 100; tick đầu bảng trang 2 ⇒ 0 ô tick thêm, vẫn 100; Bỏ chọn ⇒ thanh biến mất; 0 POST | ĐẠT |
| K7 | Thanh chọn top 247 / bottom 289 < thead top 306 (không đè); th "Hành động" 90px; 16/16 th `white-space: nowrap`, mọi th cao 34px | ĐẠT |
| L2 | Dòng sinh ra (id 4388/4389/4390): `coefficient 1.0000`, `status 1`, `business_policy_id/min_stock_qty/guarantee/guarantee_type` NULL cả 3; `/edit` trả `admin` 4 ô null, `supplier_ids []`, `job_cluster_ids []` | ĐẠT |
| L3 | `POST take` (API, 0 dòng ghi): `own_product` · `erp_inactive` (status 0 và status 2/5) · `not_found` (code null) · `already_used`, đúng câu tiếng Việt; 101 id ⇒ 422. UI taken = 0 (body thay bằng 6 mã bỏ qua) ⇒ CHỈ 1 toast cảnh báo `warning-toast` "Bỏ qua 6 mã: … (5 mã kèm lý do) và 1 mã khác". `owner_not_trading` không có ca thật trên DB local (0 dòng status NOT NULL) — PHPUnit đã phủ | ĐẠT |
| F4 | `/entering` Cty 1: 3 mã lấy về `can_edit true`, menu dòng có "Sửa" (`ri-edit-line`); chi tiết 50061: `can_edit true`, footer [Sửa, Quay lại], meta "Đang nhập thông tin" | ĐẠT |
| U1 | `/50061/edit` 200 `edit_scope admin`, `owner_company_id 4`; `GET /50061` 200 song song; tab active "Quản trị hàng hoá"; 1 `.product-scope-notice` "Hàng hoá do CÔNG TY TNHH THIẾT BỊ TÂN PHÁT SÀI GÒN tạo — chỉ khai được tab Quản trị hàng hoá."; nền `rgb(245, 248, 252)`, viền `rgb(227, 235, 245)`, bo 6px, đệm `8px 12px`, chữ `rgb(55, 65, 81)` 12px | ĐẠT |
| U2 | Tab Thông tin `opacity 0.4`; bấm vào ⇒ 4 step (hàng không có tab xe — `show_vehicle_tab` false), mỗi step: 1 `.product-form__readonly` có nội dung, **0** ô nhập hiện + bật ngoài khối admin; 0 `input[data-path="nature"]` | ĐẠT |
| U3 | Ô Hệ số công nghệ `disabled = true` (giá trị 1) | ĐẠT |
| U5 | Lưu thiếu catalog ⇒ 1 PUT `…/50061/admin-data` 422 `admin.job_cluster_ids` "Phải xếp hàng hoá vào ít nhất 1 Tiểu mục catalog kinh doanh."; 1 chấm `.ptabs__err` ở tab Quản trị (0 ở tab Thông tin), ở lại tab Quản trị, 1 dòng lỗi dưới ô catalog, toast "Vui lòng kiểm tra lại dữ liệu nhập". Lưu khi đang đứng ở tab Thông tin ⇒ 422 ⇒ tự về tab Quản trị | ĐẠT |
| U4 | Body PUT: `Object.keys = ['admin']`, `admin` đúng 6 khoá (`business_policy_id, min_stock_qty, guarantee, guarantee_type, supplier_ids, job_cluster_ids`), không `tech_coefficient`/`catalogs`; 1 PUT/lượt Lưu | **ĐẠT MỘT PHẦN** — lượt Lưu thành công (200, toast, sang chi tiết) **KHÔNG đo được**: DB local không có Tiểu mục nào chọn được (2 `job_clusters` thuộc chương `internal_business_scope_id NULL`; thử chèn id 1 vào body ⇒ 422 "Tiểu mục không tồn tại: #1", 0 dòng ghi). Tạo catalog tạm nằm ngoài phạm vi được cho phép ⇒ bỏ, chờ lead/user. Spec `products-take-ui` U4 tự tạo catalog `E2EC1S` nên chạy được khi user cho chạy |
| U6 | Hàng Cty 1 (50066) `/edit` `edit_scope full`: tab active "Thông tin hàng hoá", 0 dải báo, opacity 1, 0 vùng chỉ đọc, 13 ô nhập bật; Hệ số công nghệ `disabled = false`; console chỉ lỗi 404 ảnh đại diện có sẵn (xem ghi chú) | ĐẠT (không bấm Lưu — không ghi) |
| N1 | Role tạm id 103208 "E2E C2 tạm - chỉ xem hàng công ty" (chỉ 1653, `company_id 1`) gán `e2e_cmd_noperm` (employee 1184) + `cache:clear`. API: `company` 200, `warehouse` 200 (20 dòng, 0 `can_take_back`), `entering` 403, `/50061/edit` 403, `POST take` **403**, `PUT admin-data` 403. UI: lưới công ty 20 dòng; Kho 20 dòng, **0** ô tick thân + 0 đầu bảng, 0 th "Hành động", 0 chữ "Lấy về", 0 `span[title="Lấy về"]`; Nhập thông tin ⇒ trang 404 "Không tìm thấy hoặc không được cấp quyền", 0 nút "Kho dữ liệu"; console chỉ 2 lỗi tải tài nguyên 404, không lỗi JS | ĐẠT |

**Dọn dữ liệu (đã chứng minh bằng SELECT):**
- Trước khi ghi: 6 mã ứng viên (50061, 50060, 49999, 49985, 49984, 49983 — Cty 4, status 1) có **0** dòng ở `product_company_coefficients` / `product_suppliers` / `product_business_catalogs`; tổng bảng 1.105 (0 dòng status NOT NULL) / 1.741 / 0; chụp nguyên dòng `products` của 6 mã ra file.
- Ghi thật: đúng 3 mã (50061 qua K4; 50060, 49999 qua K5) ⇒ 3 dòng `product_company_coefficients` id 4388/4389/4390. Lưu tab Quản trị: 2 lượt đều 422 ⇒ 0 dòng NCC/catalog/4 ô.
- Sau khi đo: `DELETE … WHERE id IN (4388,4389,4390) AND company_id = 1` ⇒ ROW_COUNT 3. Kiểm lại: `product_company_coefficients` 1.105 (0 status NOT NULL), `product_suppliers` 1.741, `product_business_catalogs` 0; 0 dòng của 6 mã ở cả 3 bảng; `products` 6 dòng `diff` từng cột trước/sau = giống hệt. (AUTO_INCREMENT các bảng đã nhích — không ảnh hưởng.)
- Role tạm: xoá `employee_has_roles` + `role_has_permissions` + `roles` id 103208 ⇒ SELECT còn 0; e2e_cmd_noperm còn đúng role cũ 100126; `cache:clear`; gọi lại `GET company` bằng token đó ⇒ 403 (quyền đã mất thật).
- Server: kill đúng PID theo cổng (php artisan 19289 + php -S 19480, nuxt 19298) ⇒ 8031/3031 không còn LISTEN.

**Ghi chú (không phải lỗi 2-C2, chưa sửa):**
- Spec `products-take-ui` K4 mở `warehouse?keyword=<mã>` nhưng màn KHÔNG đọc `keyword` từ URL (request thật không có `keyword`) — ca chỉ xanh vì mã vừa lấy tình cờ nằm trang 1. Nên đổi sang gõ ô tìm kiếm khi user cho chạy e2e.
- Console mọi màn có 1 lỗi 404 `…/master-data/products/e2e.png` (ảnh đại diện tài khoản e2e đường dẫn tương đối) — có sẵn, ngoài luồng.
- `min_stock_qty`/`guarantee` gửi dạng chuỗi ("5", "12") — BE nhận numeric, không lỗi.
- Thời gian mở form `admin` (dev, nạp lại toàn trang): `/edit` 0,9s, `GET /{id}` 1,3s song song; form sẵn sàng ~7s — form chủ cũng ~10s ⇒ chậm do bundle dev, không riêng nhánh admin (R8).
- Còn lại: U4 lượt Lưu 200 cần 1 Tiểu mục hợp lệ (tạo catalog tạm hoặc chạy spec) — **xin phép riêng**.

**08/10/2026 — e2e 2-C2 (user cho chạy 3 spec + ghi/dọn DB `hrm_erp`)** · api 8031 (hrm-api `2739d0379`) + Nuxt 3031 (hrm-client `3a9eae100`), bản sao `wt-chuyen-doi-hang-hoa/e2e`, Node 20, `--no-deps --workers=1 --retries=0`, truyền `API_BASE=…8031 BASE_URL=…3031 API_REPO=<worktree>/hrm-api` (thiếu `API_REPO` thì `runMysql`/`cache:clear` đi vào checkout chính).

| Spec | Kết quả cuối (dòng tổng kết) |
|---|---|
| `products-take.api` (`--project=api`) | **7 passed**, 0 failed / skipped / did-not-run — xanh ngay lượt 1 |
| `products-take-ui` (`--project=chromium`) | **10 passed**, 0 failed / skipped / did-not-run (lượt 5) |
| `products-read-ui` (`--project=chromium`) | **8 passed**, 0 failed / skipped / did-not-run |

**Không lỗi app ⇒ không commit.** 4 lỗi đều ở SPEC `products-take-ui` (đã sửa, chép về `HRM/e2e`):
1. K4 (theo ghi chú F5): bỏ `?keyword=` trên URL; mở Kho rồi gõ mã vào ô tìm kiếm thật (`placeholder="Tìm theo mã, tên hàng hoá, model, barcode"`) + Enter ⇒ chờ đúng request có `keyword=<mã>`, assert API trả id đích, dòng đích có link `/products/<id>?` chữ = mã và còn nút "Lấy về" trước khi bấm.
2. K1 đỏ `Unexpected token '<'`: regex `LIST` khớp cả TÀI LIỆU HTML của `page.goto('/master-data/products/warehouse?…')` (cùng đường với API) ⇒ đổi `LIST`/`TAKE`/`entering`/`company` sang `/api/v1/master-data/…`. (K0 xanh trước đó chỉ vì đi bằng bấm nút, không tải lại trang.)
3. U1–U3: step đang mở của `ProductStepTabs` là class `on` + `aria-selected="true"`, không phải `active` ⇒ assert `aria-selected`.
4. N1: `.container-fluid` khớp 3 phần tử (strict) ⇒ đo `.v2-styles > .container-fluid`; console có 2 lỗi "Failed to load resource 404" (ảnh đại diện e2e — ngoài luồng đã ghi) ⇒ cho qua lỗi tải tài nguyên 404 nhưng bắt mọi response API 404/5xx; thêm assert trang Nhập thông tin hiện "Không tìm thấy hoặc không được cấp quyền".
- U4 làm chặt (Lưu tab Quản trị THÀNH CÔNG của công ty lấy về): nhập "Số lượng tồn kho tối thiểu" 7 + chọn catalog E2EC1S ⇒ PUT `…/admin-data` **200**, đúng 1 PUT, `Object.keys(body) = ['admin']`, `admin` đúng 6 khoá, toast "Đã lưu hàng hoá <mã>", sang chi tiết "Đang nhập thông tin"; DB: dòng Cty 1 `status|coefficient|min_stock_qty` = `1|<giữ nguyên>|7.00`, `product_business_catalogs` đúng 1 dòng `company_id 1` × Tiểu mục E2EC1S, dòng hệ số công ty khác và dòng `products` giống hệt trước khi Lưu.

**Đối chứng ca không quyền (cài lỗi tạm trong spec, đã bỏ — `grep` 0 dấu vết):**
- A5 (api): role tạm thêm 1652 ⇒ ĐỎ `POST take` "Expected 403, Received 200".
- N1 (UI): role tạm thêm 1652 ⇒ ĐỎ ở `can_take_back` API; tắt thêm assert API ⇒ vẫn ĐỎ ở UI "ô tick thân bảng Expected 0, Received 20". Sau khi bỏ lỗi: cả 2 xanh trong lượt chạy đủ bộ.

**DB sạch (SELECT sau cùng):** `product_company_coefficients` **1.105** (0 `status` NOT NULL) · `product_suppliers` **1.741** · `product_business_catalogs` **0** · role `E2E%tạm%` 0 · rác `E2EC1S` (catalog 3 cấp + cây phân loại + hàng) 0 · `e2e_cmd_noperm` còn đúng role 100126. afterAll của 2 spec đã dọn đủ kể cả lượt đỏ giữa chừng — không cần sửa afterAll. (7 dòng `role_has_permissions` mồ côi của `role_id 9` có từ trước, không phải của e2e.)
- Server: kill đúng PID theo cổng (artisan 23089 + php -S 23110, nuxt 23101) ⇒ 8031/3031 không còn LISTEN. Git 2 repo worktree sạch.
- Spec đã chép về `HRM/e2e/tests/master-data/`: `products-take.api.spec.ts`, `products-take-ui.spec.ts` (mới), `products-read-ui.spec.ts` (bản E1). `utils/` 2 bên giống nhau.
- Bước tiếp: chờ lead/user (review cuối, merge `feat/p2c2-lay-ve` → `feat/chuyen-doi-hang-hoa`; ⛔ không gop_db).
