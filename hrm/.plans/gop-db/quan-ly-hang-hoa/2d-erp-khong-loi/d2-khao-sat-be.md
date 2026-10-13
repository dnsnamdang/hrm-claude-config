# Đợt 2-D2 — Khảo sát BE: Cập nhật giá hàng hoá + Duyệt giá (09/10/2026)

> Khảo sát CHỈ ĐỌC: không sửa source, không ghi DB (chỉ SELECT), không artisan, không checkout/stash/commit.
> **ERP:** worktree `wt-erp-2d1` (nhánh `feat/2d1-erp-khong-loi` = gop_db + 2-D1, HEAD `b2f1761789`). Số dòng dưới đây theo worktree này
> (khớp gop_db ở các file giá, vì 2-D1 không sửa `ProductsController` vùng giá / `ProductApprovesController`).
> **HRM:** worktree `wt-chuyen-doi-hang-hoa/hrm-api` (nhánh `feat/chuyen-doi-hang-hoa`, HEAD `a862fbeef`).
> **DB:** `hrm_erp` local, SELECT ngày 09/10/2026.
> **Đọc trước:** `khao-sat-c-gia.md` (§1 L1/L5, §2.5 HĐ1–HĐ10, §4.2), `ton.md` mục C, `d1-plan.md`, `../2c-ghi/chot.md`.
> Ký hiệu: `PC` = `app/Http/Controllers/ProductsController.php` (ERP) · `PAC` = `app/Http/Controllers/ProductApprovesController.php` (ERP)
> · `web` = `routes/web.php` (ERP) · `MD` = `Modules/MasterData` (HRM).

---

## 0. Tóm tắt — phát hiện quan trọng

1. 🔴 **Duyệt giá ĐÃ TỪNG CHẠY thật** (khảo sát C ghi "0 lần dùng" là chưa đủ): `product_units.approve_time` có 47 dòng từ
   **04/07/2025 → 26/01/2026** (Cty 1: 28 duyệt + 17 không duyệt; Cty 4: 1 + 1). Cờ "Không duyệt" (= 2) còn trên **18 ĐVT, 92 dòng giá,
   17 giá hiệu lực**; **7 mã** đang `products.status` = 5 (Không duyệt) / 2 (Chờ duyệt). Bảng `product_approves` rỗng vì ERP **xoá cứng**
   bản ghi khi duyệt/không duyệt (`PAC:248,266,321,330,383,394,484,498`) — ERP **không lưu lịch sử duyệt**.
2. 🔴 **Duyệt/Không duyệt ghi đè `products.status`**: duyệt ⇒ `status = 1` (`PAC:258-260`, `:437-439`), không duyệt ⇒ `status = 5`
   (`PAC:298-300`, `:388-389`). Với luật suy trạng thái của HRM (`Product::companyStatusSql` `MD/Entities/Product/Product.php:383-391`:
   chỉ `products.status = 1` mới ra *Đang kinh doanh*) thì port 1–1 sẽ làm hàng **biến mất khỏi các màn hàng hoá công ty HRM** sau khi
   bị "Không duyệt" giá. ⇒ câu **F1**.
3. 🔴 **Màn Quy định HRM ghi sai danh mục cho cờ duyệt giá**: ô "Hàng cập nhật giá – Hãng cần duyệt" (`brand_ids`) và "Hàng mới – Hãng cần
   duyệt" (`new_brand_ids`) lấy option từ bảng **`brands` (Thương hiệu)** (`MD/Support/RegulationTabRegistry.php:388-399` → `MD/Services/RegulationConfigService.php:551-555`),
   trong khi ERP hiểu đó là **id Hãng SX** (option `Manufacture::getForSelect()` `resources/views/common/companies/regulation.blade.php:704`; so với
   `$product->manufacture_id` ở `PC:2656-2658`, `app/Model/Order/PriceCalculate.php:392-395`, `app/Product.php:7119-7121`). Bật duyệt giá
   theo hãng từ màn HRM ⇒ áp sai hàng, im lặng. ⇒ câu **F9**.
4. ⚠️ **Cty 8 (ETEK) đang bật `is_new_company = 1, is_new_brand = 1`** (duyệt giá HÀNG MỚI, mọi hãng). Đường dùng cờ này là
   `Product::createRecord` (`app/Product.php:7111-7130`, `:7285-7346`) — gọi từ **duyệt hàng tạm ERP (giữ tới Phase 6)**. Hàng mới của Cty 8
   từ hàng tạm sẽ vào `status = 2` + sinh `product_approves` ⇒ màn Duyệt giá HRM **phải** đọc được bản ghi này. Hiện Cty 8 có 0 hàng.
5. **Ba nguồn sinh bản ghi chờ duyệt, cùng một định dạng** (ghép theo `product_id + product_unit_id + unit_id`, giá hiện tại
   `product_expected_price_id` NULL, giá hiệu lực có id): `PC@updatePrice` (`:2912-3127`, sẽ chuyển HRM) · `PriceCalculate::updatePriceWithApproval`
   (`app/Model/Order/PriceCalculate.php:376-760`, **ở ERP tới Phase 7**) · `Product::createRecord` (hàng mới, **ERP tới Phase 6**). Phiếu tính giá
   còn **chặn duyệt phiếu** nếu mã đang có bản ghi chờ (`PriceCalculate.php:332-361`, lọc `whereNull('approved_id')`). ⇒ HRM màn Duyệt **tương
   thích được** nếu giữ đúng định dạng + **xoá bản ghi sau khi xử lý như ERP** (mục B6).
6. **Không cần migration**: lịch sử giá ghi được vào bảng dùng chung **`catalog_histories`** (`table_name`, `table_id`, `old_value`/`new_value`
   JSON — `app/Services/CatalogHistoryService.php:749-845`); bảng duyệt dùng nguyên `product_approves`/`product_approve_prices`; quyền thêm bằng
   seeder. ⚠️ Nhưng endpoint đọc chung `catalog-histories/{table}/{id}` **không gate quyền** (`routes/api.php:37-48`) ⇒ log có **giá vốn**
   phải đi endpoint riêng có gate (tiền đề #5).
7. **Id quyền HRM**: `origin/develop` đã dùng **1679–1698** ⇒ khảo sát C ghi "1679+ trống" là **sai**. Trống thật: **1657–1659, 1662–1669, 1699+**
   (1654 giữ cho *Xuất excel*, 1656 giữ cho *Chính sách giá nội bộ*). Seeder nhánh feature không có id trùng (`uniq -d` rỗng).
8. Lỗi ERP cần biết khi port (không vá ở ERP — ghi N54+): lọc *Tồn kho* trên màn giá là ô chết (`PC:2499-2501` comment); `approvesSubmit` ghi
   cột `price` bằng giá **đề nghị** chứ không phải giá **người duyệt sửa** (`PAC:473` khác `:237`); duyệt đơn lẻ không kiểm công ty
   (`PAC:200-202` comment) và cả 4 route duyệt không gate quyền (N29); cron 01:00 xoá cờ chờ duyệt của giá hiện tại khi áp giá hiệu lực
   (`app/Console/Commands/UpdateProductPrice.php` — đoạn `flag_*_wait_approve = 0`) ⇒ bản ghi duyệt mồ côi; `manualUpdatePrices` **không lọc
   `flag`** (`PC:2243`) ⇒ áp được cả giá hiệu lực đang chờ duyệt (giá 0) — xem F5.

---

## A. Cập nhật giá nhanh (L1) — ERP chi tiết

### A1. Màn + danh sách (`PC@editPrices :2296-2305`, `PC@getProductsAndPrices :2313-2547`, view `resources/views/products/editPrices.blade.php`)

**Route:** `web:586` GET `products/editPrices` (`checkPermission:Cập nhật nhanh giá hàng hóa`) · `web:595` GET `getProductsAndPrices` (**không gate
route**, gate trong code) · `web:596` POST `{id}/updatePrice` (gate quyền).

**Query (`:2321-2405`):**
- `products p` **INNER JOIN `product_models pm`** (`:2322`; đo: 0 hàng thiếu model, HRM bắt buộc `model_id` `MD/Http/Requests/Product/ProductRequest.php:53`).
- Cột: `p.id, name, model_id, code, product_cate, manufacture_id, status, norm, note, product_type, pm.name model_name` (`:2323`).
- Eager `units` (`:2325-2383`) — LEFT JOIN `units`, sắp `is_base DESC, unit_coefficient ASC`; cột `id, unit_id, product_id, is_base,
  COALESCE(coefficient_wait_approve, unit_coefficient) AS unit_coefficient` (đo: 2.048 ĐVT có `coefficient_wait_approve` nhưng **0 dòng lệch**),
  `units.name, flag_price_wait_approve, note_edit_price, reason_edit_price, approve_comment`; **chỉ khi có quyền** `Cập nhật nhanh giá hàng hóa`
  mới thêm `cost_price` (= `price_wait_approve` nếu cờ ≠ 0/NULL) và `liquidation_sale_max_percent` (`:2329-2333`).
  - `prices` (`:2339-2368`): `id, price_type_id, product_unit_id`, 3 cờ chờ duyệt, 3 cờ sửa tay TMĐT, và **giá/hệ số/ĐMGG = bản CHỜ DUYỆT nếu
    cờ ≠ 0/NULL** (CASE), kèm `price_old/coefficient_old/sale_max_percent_old` = giá đang chạy.
  - `expected_prices` (`:2370-2378`): `effect_date > hôm nay`, `COALESCE(*_wait_approve, *)`, `flag`.
- Eager `manufacture(id,name)`, `model(id,name)`, `recipe_products.product(id,code,name,barcode_id).order_code`, `recipe_products.unit` (`:2384-2404`).
- **Lọc** (`:2407-2497`): `name`/`code`/`model` LIKE; `status=1` ⇒ có cờ = 1 (Chờ duyệt) ở ĐVT/giá/giá hiệu lực tương lai; `status=2` ⇒ có cờ = 2
  (Không duyệt); `manufacture_id` (hãng **phải thuộc công ty người dùng**, khác ⇒ `success=false` "Hãng sản xuất này không thuộc quyền quản lý
  của bạn!" `:2476-2485`); `product_cate` LIKE; `product_type`; `brand_id`. `check_in_stock` **comment** (`:2499-2501`) ⇒ ô lọc Tồn kho trên UI
  (`editPrices.blade.php:115-123`) không có tác dụng.
- `type=updating` (màn *Hàng sắp điều chỉnh tăng giá*, L3, `resources/views/products/price_updating.blade.php:149-155`) ⇒ chỉ hàng có giá hiệu lực
  tương lai, **không kiểm quyền**; ngược lại không có quyền ⇒ `data=[]` "Không có quyền!" (`:2503-2516`).
- Sắp xếp `order[name]` (cột tự do từ request — injection-ish) mặc định `p.name DESC` (`:2518-2524`); **`p.status IN (1,2,5)`** + `paginate(per_page=20)`
  (`:2526`); hậu xử lý `appendManualOnlineFlagsToResponse` (`PC:3268-3323`) nạp lại 3 cờ sửa tay.
- ⚠️ Danh sách **không lọc theo công ty**: mọi công ty thấy toàn bộ 28.378 mã (đo), chỉ lúc Lưu mới chặn (A3). Số mã sửa được theo luật ERP:
  **Cty 1 = 27.029 · Cty 4 = 966 · Cty 3 = 14 · Cty 2 = 1 · Cty 5/6/7/8 = 0** (mục E).

**Tồn kho** — không nằm trong query; FE gọi thêm `POST warehouse_infos/stockOfProducts` (`web:37`) với `get_all=1` (`editPrices.blade.php:516-531`,
`:569-590`) ⇒ `ProductStockService::getStockQty` (`app/Services/Product/ProductStockService.php:13-97`) ⇒ `Product::getAccountingStockDetail`
(`app/Product.php:2391-2430`): với `get_all` = **`SUM(accounting_stocks.qty) WHERE stock_id IS NOT NULL`** của mã, **mọi kho mọi công ty**,
JOIN `product_units` theo ĐVT đang chọn; FE chia `in_warehouse / unit_coefficient` (`editPrices.blade.php:577-581`). Đổi ĐVT ⇒ gọi lại cho 1 mã.

**Cột hiển thị** (`editPrices.blade.php:187-223`, `:233-372`): Tên (+ ô "Lý do sửa giá" = `reason_edit_price`, link công thức lắp ráp, "Ghi chú không
duyệt" = `approve_comment`) · ĐVT (chọn) · Mã (+ ô sửa **ghi chú hàng hoá `products.note`**) · Model · Hãng SX · Loại HH (`product_cate`) · Tính chất
(`product_type`) · Tồn kho · Giá vốn (badge Chờ duyệt/Không duyệt) · 7 cột giá: Loại · Giá hiện tại · Hệ số · Giá công thức · Giá mới · ĐMGG ·
Ngày hiệu lực · Lưu. **Không có cột `norm` và ĐMGG thanh lý** — cả hai chỉ gửi lại nguyên giá trị cũ (`partials/classes/sale/ProductWithPrice.blade.php:65-77`).

**Hành vi FE ảnh hưởng dữ liệu (để port FE đúng):**
- Sửa **giá/hệ số/ĐMGG bán lẻ (loại 1) ⇒ chép sang loại 2–5** (`partials/classes/sale/ProductPrice.blade.php:179-181`, `:203`, `:225` →
  `ProductUnit.blade.php` `updatePrices` ~`:110-145`); TMĐT (6) = bán lẻ × `configs.coefficient_ecommerce_price` (= 1,3 cả 8 công ty) trừ khi tick "Chỉnh sửa".
- Đổi hệ số ⇒ giá = `round(hệ số × giá vốn / 100) × 100` (`ProductPrice.blade.php:202`); "Giá công thức" = giá vốn × hệ số, TMĐT làm tròn nghìn (`:239-247`).
- Giá hiệu lực: chỉ thêm được khi chưa có và loại ≠ 6 (`editPrices.blade.php:291`); loại 6 khoá, lấy theo bán lẻ cùng thứ tự.

### A2. Validate (`PC:2551-2620`) — trả `success=false, errors, message "Cập nhật thất bại!"` (HTTP 200)

| Trường | Luật | Câu ERP |
|---|---|---|
| `cost_price` | required · numeric · 0 ≤ x ≤ 999.999.999.999 | Bắt buộc phải nhập / Không hợp lệ / Không được vượt quá 12 chữ số |
| `norm` | nullable · numeric · 0 ≤ x < 1000 | Không hợp lệ |
| `liquidation_sale_max_percent` | nullable · numeric · 0 ≤ x < 1000 | (mặc định) |
| `unit_id` | required · exists:units | Bắt buộc phải chọn |
| `prices` | required · array · min 1 | Bắt buộc phải nhập / Không hợp lệ |
| `prices.*.price_type_id` | required · exists:price_types | |
| `prices.*.coefficient` | required · numeric · 0 ≤ x ≤ 100 · not_in:100 | …/ Không được vượt quá 2 chữ số trước dấu phẩy |
| `prices.*.price` | required · numeric · 0 ≤ x ≤ 999.999.999.999 | |
| `prices.*.sale_max_percent` | nullable · numeric · 0–100 | (khoá message viết sai `prices.*sale_max_percent` `:2593-2595` ⇒ không áp) |
| `prices.*.is_manual_*_online` (3) | nullable · in:true,false,1,0 | |
| `prices.*.expected_prices` | nullable · array · **min 1 max 1** | |
| `…expected_prices.*.price` | required · numeric · 0 – 999.999.999.999 | |
| `…expected_prices.*.coefficient` | required · numeric · 0–**99** (lệch giá hiện tại: < 100) | |
| `…expected_prices.*.sale_max_percent` | nullable · numeric · 0–100 | |
| `…expected_prices.*.effect_date` | required · date · **after:today** | Phải chọn ngày tương lai |

Không validate: `note`, `note_edit_price`, `reason_edit_price`, số dòng `prices` (không bắt đủ 6), trùng `price_type_id`.
Lưu ý cột DB: `product_unit_prices.coefficient` / `product_expected_prices.coefficient` = `decimal(5,2)`, `sale_max_percent decimal(5,2)`,
`price decimal(16,2)`, `product_units.cost_price decimal(16,2)` ⇒ max 12 chữ số vừa.

### A3. Cổng sửa (sau validate)
1. `Product::findOrFail($id)` (`:2622`).
2. Có `manufacture_id` ⇒ `manufactures.company_id` phải = công ty người dùng, khác ⇒ "Hãng sản xuất này không thuộc quyền quản lý của bạn!" (`:2624-2631`).
3. `Product::canEdit()` = `products.company_id` NULL **hoặc** = công ty người dùng (`app/Product.php:6958-6960`), khác ⇒ "Không có quyền sửa hàng này!" (`:2664-2668`).
4. **Không** kiểm `products.status`, không kiểm trạng thái theo công ty, không khoá dòng.
- Cờ duyệt: `company_id = products.company_id ?? công ty người dùng`; `companies.is_company_price` + (`is_all_brand` hoặc `manufacture_id ∈ brand_ids`)
  ⇒ `$is_approve` (`:2648-2663`). (Đoạn đọc `configs.is_company_price` ở `:2318-2320` và `:2634-2647` là code chết.)

### A4. Ghi (trong 1 transaction `:2669-3135`) — pseudo-code port 1–1

```
version = ProductVersion::create(...)                       # ERP — HRM BỎ (QC-9), ghi catalog_histories thay
unit = product_units WHERE product_id AND unit_id = req.unit_id  firstOrFail     # :2701-2703
ecomCoef = configs.coefficient_ecommerce_price; retail = req.prices[type=1]      # :2689-2699
FOR p IN req.prices:                                                              # :2704-2869
   manual* = toBoolean(p.is_manual_*)                                             # PC:3325-3341
   IF p.type == 6 AND retail:                                                     # HĐ4 :2710-2720
       IF !manualPrice: p.price = round(retail.price × ecomCoef)
       IF !manualCoef : p.coefficient = retail.coefficient × ecomCoef
       IF !manualSale : p.sale_max_percent = 0
   price = product_unit_prices WHERE type AND product_unit_id=unit.id  first  ELSE new   # HĐ1 :2722-2727
   price.is_manual_* = (type==6 ? manual* : 0)
   IF !is_approve:                                                                # HĐ3 :2731-2741
       price.{price,coefficient,sale_max_percent ?? 0} = p.*
       price.{price,coefficient,sale_max_percent}_wait_approve = 0 ; 3 flag_* = 0 ; save
   ELSE:                                                                          # nhánh duyệt :2742-2786
       flag_x = (p.x != price.x) ? 1 : 0     (x = price, coefficient, sale_max_percent)
       price.x_wait_approve = p.x ; price.flag_x_wait_approve = flag_x ; save   # giá đang chạy GIỮ NGUYÊN
       IF có x đổi: approve_prices[] = {pup_id, type, old=price.x, new=x_wait, company_id, by}
       ELSE       : approve_price_deletes[] = {...}
   IF p.expected_prices có:                                                       # HĐ6 :2788-2856
       DELETE product_expected_prices WHERE unit_price_id=price.id AND id NOT IN gửi lên AND effect_date > today
       DELETE product_approve_prices  WHERE pup_id=price.id AND pep_id NOT IN gửi lên AND (pep_id NOT NULL OR pep_id != 0)
       FOR e (index i): IF type==6 AND retail.expected[i]: e.price=round(retail_e.price×ecomCoef); e.coef=retail_e.coef×ecomCoef; IF !manualSale: e.sale=0
            ep = find(e.id) ?? new ; ep.unit_price_id, effect_date, status = 2
            IF !is_approve: ep.{price,coefficient,sale ?? 0} = e.* ; save
            ELSE: ep.*_wait_approve = e.* ; save ; IF khác ep.*: ep.flag = 1 ; approve_expected_prices[] += {pup_id, pep_id, …, effect_date}
   ELSE:
       DELETE expected tương lai của price ; DELETE approve_prices có pep_id của price          # :2857-2868
# giá vốn — HĐ5 :2870-2892
IF is_approve AND req.cost_price != unit.cost_price:
     unit.price_wait_approve = req.cost_price ; flag_price_wait_approve = 1 ; cost_flag = true   # cost_price GIỮ NGUYÊN
ELSE unit.cost_price = req.cost_price ; flag_price_wait_approve = 0 ; price_wait_approve = 0
unit.liquidation_sale_max_percent = req.liquidation_sale_max_percent ; unit.note_edit_price ; unit.reason_edit_price ; save
product.norm = req.norm ; product.note = req.note ; save                         # :2900-2904 — HRM BỎ (QC-8)
# bản ghi duyệt — chỉ khi is_approve (:2912-3127)
IF approve_prices OR approve_expected_prices:
     pa = product_approves WHERE product_id, product_unit_id, unit_id  first
     IF pa: cập nhật cost_price/note/reason/company_id ; xoá approve_prices có pep_id ; upsert approve_prices theo pup_id
     ELSE: tạo pa (snapshot code/name/model/brand/manufacture tên, product_type, product_cate, unit_name, cost_price=req,
           unit_coefficient=unit.unit_coefficient, company_id, note_edit_price, reason_edit_price) + approve_prices
     insert approve_prices cho từng giá hiệu lực
     NOTIFY mọi NV có quyền "Duyệt giá hàng hoá" của company_id (Employee::withPermissionRole) — "Bạn có yêu cầu duyệt giá hàng hoá từ <tên>",
            link route('products.approvePrices')                                  # :3029-3033
ELIF is_approve: chỉ đổi giá vốn ⇒ cập nhật pa nếu có, tạo pa (không dòng giá) nếu cost_flag   # :3034-3083
IF is_approve AND approve_price_deletes: xoá approve_prices tương ứng (pep_id NULL/0), xoá pa nếu hết dòng       # :3085-3113
IF is_approve: pa không còn dòng giá và không đổi giá vốn ⇒ xoá pa                                                # :3115-3127
TRẢ data_with_prices (Product.php:1618-1680) + message "Sản phẩm đã được cập nhật giá mới" / "Yêu cầu duyệt giá hàng hoá đã được gữi!"
```

- HĐ áp dụng: **HĐ1** (sinh dòng thiếu: đo loại 5 chỉ 32.211/46.560 ĐVT, loại 6 46.195), **HĐ2** (không đụng `unit_id/is_base/unit_coefficient`),
  **HĐ3** (nhánh không duyệt), **HĐ4** (TMĐT), **HĐ5**, **HĐ6** (≤ 1 giá tương lai — đo: 0 giá đang có > 1 dòng tương lai; 2.054 dòng tương lai
  status 2), **HĐ7**, **HĐ8** (1 transaction / ĐVT). **HĐ9 ĐỔI**: vì port Duyệt giá, HRM **sẽ ghi** `product_approves*` đúng định dạng ERP
  (không còn "để trống"). **HĐ10 bỏ** (không ghi `product_versions`).
- ⚠️ ERP không gán `created_by` cho `product_expected_prices` mà dựa `BaseModel` (ERP) tự gán; cột **NOT NULL + FK `employees`** (đo
  `information_schema`) và cron 01:00 dùng `$p->created_by` cho `product_versions` ⇒ HRM phải gán tường minh `created_by/updated_by`.
- ⚠️ Giá hiệu lực MỚI ở nhánh duyệt chỉ set `*_wait_approve` ⇒ `price`/`coefficient` (NOT NULL không default) nhận **0** nhờ `strict=false`
  (ERP `config/database.php:59`; HRM `config/database.php:61` cũng `false`) ⇒ HRM gán `price=0, coefficient=0` tường minh.

---

## B. Duyệt giá (L5)

### B1. Schema (`SHOW CREATE TABLE`, `hrm_erp`)

`product_approves` (AUTO_INCREMENT 8, **0 dòng**): `id` · `product_id` · `product_unit_id` · `product_code` · `product_name` · `model_id` ·
`model_name` · `brand_id` · `brand_name` · `manufacture_id` · `manufacture_name` · `product_type` · `product_cate` · `approved_id` ·
`unit_id` · `unit_name` · `approved_time` · `cost_price decimal(18,2)` · `unit_coefficient decimal(10,2)` · `created_by` · `updated_by` ·
`status tinyint` · `company_id` · `department_id` · `part_id` · `comment text` · `created_at` · `updated_at` · `reason_edit_price text` ·
`note_edit_price text`. Không FK, không index ngoài PK.
- `approved_id`, `approved_time`, `status`, `comment` **không đường nào ghi** (grep ERP); `approved_id` chỉ được ĐỌC ở `PriceCalculate.php:349`.
- `department_id`/`part_id` gán trong hook `created` của model (`app/ProductApprove.php:13-21`, theo người tạo).

`product_approve_prices` (AUTO_INCREMENT 8, **0 dòng**): `id` · `product_approve_id` · `product_unit_price_id` · `product_expected_price_id`
(NULL/0 = giá hiện tại) · `price_type_id` · `price_type` (không ai ghi) · `price_old` · `price decimal(15,2)` · `coefficient_old` · `coefficient
decimal(10,2)` · `sale_max_percent_old` · `sale_max_percent decimal(8,2)` · `effect_date` · `created_by` · `updated_by` · timestamps.

Cờ trên bảng giá: `product_units.{price_wait_approve, coefficient_wait_approve, sale_max_percent_wait_approve, flag_price_wait_approve,
approve_comment, approve_time, reason_edit_price, note_edit_price}` · `product_unit_prices.{price,coefficient,sale_max_percent}_wait_approve`
+ 3 `flag_*` · `product_expected_prices.{*_wait_approve, flag}`. Quy ước cờ: **NULL/0 = bình thường · 1 = Chờ duyệt · 2 = Không duyệt**.

### B2. Ai sinh bản ghi chờ duyệt

| Nguồn | File:dòng | Điều kiện | Ghi gì | Sau 2-D2 |
|---|---|---|---|---|
| Cập nhật giá nhanh | `PC:2742-2786, 2827-2856, 2870-2883, 2912-3127` | `companies.is_company_price` + hãng | A4 | **chuyển HRM** |
| Phiếu tính giá (Lưu & duyệt) | `PriceCalculate.php:332-374` (chặn nếu mã đang chờ) → `updatePriceWithApproval :376-760` (thông báo `:713-715`) | như trên | như A4 + `products.note` (`:364-369`) | **ERP tới Phase 7** |
| Form sửa hàng ERP | `PC@update` (~`:1960-1980`, thông báo `:1976`) | như trên | | đã chặn 2-D1 |
| Hàng mới (duyệt hàng tạm) | `Product::createRecord` `app/Product.php:7111-7130` (`status = 2`), `:7285-7346` | `companies.is_new_company` + `is_new_brand`/`new_brand_ids` | `products.status = 2`, giá vào `*_wait_approve` + `product_approves` | **ERP tới Phase 6** — ⚠️ Cty 8 đang bật |
| Cập nhật giá theo hãng | `app/Jobs/ManufactureExpectPriceMailJob.php:~120-139` | | | đã khoá 2-D1 (N36) |

### B3. Màn danh sách (`PAC@index :132-135`, `@searchData :137-186`, view `resources/views/products_approve/list.blade.php`)
- Lọc cứng `pa.company_id = công ty người dùng` (`:150`); lọc `product_id`, `product_model` LIKE, `product_code` LIKE, `product_name` LIKE,
  `manufacture_id`, `product_cate` (`whereJsonContains`), `update_employee_id` (= `updated_by`), `product_type`; sắp `updated_at DESC`; phân trang.
- Eager `prices`, `product`, `employee_update.info`, `department`; LEFT JOIN `products` lấy `product_type/product_cate` hiện tại.
- Cột (`list.blade.php:164-262`): STT · ô tick (chọn để duyệt hàng loạt) · Tên (+ Lý do sửa giá) · ĐVT · Model · Mã (link xem + nút **Duyệt** /
  **Không duyệt** + Ghi chú hàng hoá `products.note`) · Loại HH · Tính chất · Ghi chú (`note_edit_price`) · **Giá vốn** (đề nghị) · mỗi dòng giá:
  Loại · Giá cũ · **Hệ số (sửa được)** · **Giá mới (sửa được)** + chênh lệch · ĐMGG cũ · **ĐMGG mới (sửa được)** · Ngày hiệu lực/"Đang áp dụng" ·
  Người cập nhật (mã phòng – tên) · Thời gian. Không duyệt ⇒ hộp nhập "Ghi chú" (`approve_comment`) (`:433-470`, `:513-550`).
- Route list `web:587` gate `Duyệt giá hàng hoá`; `searchData :588` **không gate**.

### B4. Ghi khi xử lý

| Thao tác | Route | Ghi |
|---|---|---|
| **Duyệt 1 mã** `approveSubmit` | `web:589` (không gate, **không kiểm công ty** `PAC:200-202`) | `PAC:188-274`: version; với mỗi `approve_price`: giá hiệu lực ⇒ `effect_date` < mai thì dời **= mai**, `price/coef/sale` = **giá người duyệt gửi** (cả `*_wait_approve`), `flag=0`; giá hiện tại ⇒ `price/coef/sale` = gửi lên, `*_wait_approve` = gửi lên, 3 cờ = 0; xoá dòng approve_price. ĐVT: `cost_price = pa.cost_price`, **`unit_coefficient = pa.unit_coefficient`** (snapshot!), `approve_comment=''`, cờ = 0. **`products.status = 1`**. History `units`. **Xoá `pa`**. Không thông báo. |
| **Duyệt hàng loạt** `approvesSubmit` | `web:591` (không gate; lọc `company_id`) | `PAC:414-507`: như trên với các `pa` tick, nhưng **giá hiện tại `price = $price->price` (giá ĐỀ NGHỊ), còn `*_wait_approve` = giá người duyệt gửi** (`:473-476`) ⇒ lệch với duyệt đơn. `products.status = 1` (`:437-439`). |
| **Không duyệt 1 mã** `notApproveSubmit` | `web:590` | `PAC:352-412`: giá hiệu lực `flag = 2`; giá hiện tại cờ 1 ⇒ 2 (0 giữ 0); xoá dòng approve_price; ĐVT cờ 1 ⇒ 2, `approve_comment`, `approve_time = now`; **`products.status = 5`**; xoá `pa`; thông báo người đề nghị (`pa.updated_by`): "Không duyệt yêu cầu duyệt giá của mã hàng <mã> từ <tên>", link `editPrices?status=2` (`:396-406`). |
| **Không duyệt hàng loạt** `notApprovesSubmit` | `web:592` | `PAC:276-350`: như trên cho từng `pa` tick (lọc công ty), 1 `approve_comment` chung. |
| Xuất Excel | `web:593` (không gate) | `PAC:514-561` → `app/ExcelExports/ProductApproveExport.php` (33 dòng) + view `products_approve/exports/export`, cùng bộ lọc, có `HEADER` công ty. |

- Giá trị "Giá chờ duyệt" **không** áp lên giá đang chạy cho tới khi duyệt ⇒ trong lúc chờ, ERP + HRM đọc giá vẫn ra giá cũ (popup/`getData`
  đọc cột `price`) — đúng ý nghĩa duyệt.
- Không duyệt **giữ nguyên** `*_wait_approve` (giá bị từ chối vẫn nằm đó) — màn giá hiện lại giá bị từ chối kèm badge đỏ cho tới lần lưu sau.
- Màn tổng hợp "chờ duyệt" ERP (`HomeController@approveList`, `web:73`, `app/Http/Controllers/HomeController.php:587-600`): đếm `product_approves`
  theo công ty + đếm hàng "Không duyệt giá bán" ⇒ link `approvePrices` và `editPrices?status=2`.

### B5. Cờ `is_company_price` đặt ở đâu
- ERP: màn *Quy chế công ty* `resources/views/common/companies/regulation.blade.php:478-553` (card "BGĐ duyệt giá" + "Tất cả các hãng" + "Hãng cần duyệt";
  card Hàng mới tương tự) → `CompaniesController@postRegulations` (`app/Http/Controllers/Common/CompaniesController.php:436-449`, `web:490`).
- **HRM đã có** ô tương đương ở màn *Quy định* tab **Hàng hoá** (`MD/Support/RegulationTabRegistry.php:384-400`, store `company`), có test
  `MD/Tests/Feature/RegulationHanghoaTest.php`. ⚠️ Lỗi option Thương hiệu ≠ Hãng SX — §0 mục 3, câu F9.
- Đo: `is_company_price = 0` cả 8 công ty; `is_all_brand` 0/NULL; `brand_ids` NULL; **Cty 8 `is_new_company = 1, is_new_brand = 1`**.

### B6. Tương thích với Phiếu tính giá ERP (giữ tới Phase 7) + hàng tạm (Phase 6)
- Định dạng bản ghi PTG sinh = định dạng `updatePrice` (`PriceCalculate.php:574-720` y `PC:2912-3033`, chỉ khác `note_edit_price/reason_edit_price`
  để trống) ⇒ **màn Duyệt HRM đọc được nguyên** nếu đọc theo `product_approves.company_id` + `prices`.
- ERP dựa vào việc **bản ghi bị XOÁ sau khi xử lý**: `PriceCalculate::approve` chặn phiếu nếu còn `pa` (`approved_id IS NULL`); `PC@updatePrice`/PTG tìm
  `pa` theo (product, unit) **không lọc** `approved_id`; `HomeController:591` đếm mọi `pa`. ⇒ HRM **phải xoá `pa` + `pap`** sau khi duyệt/không duyệt
  (như ERP), không được "đánh dấu đã duyệt" bằng `approved_id` — nếu không PTG sẽ cập nhật vào bản đã duyệt và dashboard ERP đếm sai. Vết duyệt
  lưu sang `catalog_histories` (mục C3).
- Thông báo do PTG/hàng tạm sinh vẫn bắn từ ERP cho NV có quyền ERP `Duyệt giá hàng hoá` (guard `web`, 12 role), link `route('products.approvePrices')`
  (`PriceCalculate.php:713-715`, `app/Product.php:7341-7345`) ⇒ sau khi chặn route này bằng middleware 2-D1, người bấm sẽ ra trang "đã chuyển sang
  HRM" + link ⇒ cần thêm đích HRM vào `ProductMovedToHrm::TARGETS` (`app/Http/Middleware/ProductMovedToHrm.php:28-36`).
- Duyệt hàng MỚI (`products.status = 2`) qua màn HRM: approve ⇒ `status = 1` là đúng nghĩa ERP (hàng được phép bán). Xem F1.
- Cron 01:00 (`UpdateProductPrice.php`, đoạn lấy `flag != 1 OR NULL` + `status = 2`) **bỏ qua** giá hiệu lực đang chờ duyệt ✅, nhưng khi áp giá hiệu lực
  khác nó **đặt 3 cờ chờ duyệt của giá hiện tại về 0** ⇒ dòng `pap` (giá hiện tại) mồ côi, sau đó nếu duyệt thì ghi đè giá mà cron vừa áp. HRM
  nên so `price_old` với giá đang chạy lúc duyệt và cảnh báo (tự quyết K9).

### B7. 6 ĐVT cờ chờ duyệt mồ côi (đo lại)
- `product_units.flag_price_wait_approve = 1`: **6 ĐVT** — 5 mã TATE-* (Cty 1, 13/08/2025, `products.status = 1`) + `BETA-007200036` (Cty 1,
  01/03/2026 14:31 = giờ cron N5, `products.status = 0`). `product_unit_prices` cờ 1-1-1: 5 dòng (đều của BETA-007200036, loại 1–5).
  `product_expected_prices.flag = 1`: 6 dòng, `effect_date` 30/06/2025 → 31/12/2025 (đã qua, `status = 2` ⇒ cron **mãi bỏ qua**).
- Không có `pa` nào ⇒ màn Duyệt HRM không hiện; màn giá sẽ hiện badge "Chờ duyệt" mãi tới khi lưu lại (nhánh không duyệt xoá cờ — đúng ERP).
- Cờ 2 (Không duyệt): 18 ĐVT · 92 dòng giá · 17 giá hiệu lực — hiển thị badge đỏ + `approve_comment` (31 ĐVT có ghi chú) như ERP.

---

## C. HRM hiện có — dùng lại được

| Cần | Có sẵn | Ghi chú |
|---|---|---|
| Công ty đang làm | `ProductService::currentCompanyId()` = `auth()->user()->current_company_role` (`MD/Services/Product/ProductService.php:55-59`; `app/Models/TpEmployee.php:105`) | dùng y |
| Trạng thái theo công ty | `Product::scopeWithCompanyStatus` / `companyStatusSql($companyId)` (`MD/Entities/Product/Product.php:368-391`), `ownerStatusSql` (`:400-417`); hằng `ProductCompany::STATUS_ENTERING_INFO=1 … STOPPED=4`, `isLocked()` (`MD/Entities/Product/ProductCompany.php:23-60`) | QC-5: chặn khi `companyStatusSql(cty) = 1`. Vì cổng sửa bắt `products.company_id = cty` nên trạng thái của cty = trạng thái chủ |
| Cổng chủ + khoá | `ProductWriteService::assertOwner()` (`MD/Services/Product/ProductWriteService.php:103-117`) | ⚠️ **không dùng nguyên**: nó chặn `products.status ≠ 1` (ERP màn giá nhận 1/2/5) và không xét hãng SX. Viết cổng riêng theo A3 + QC-5 + F3 |
| Kiểm quyền | `app/CommonServices/PermissionService.php:20` `isCurrentEmployeeHasPermission` (chỉ đọc qua role — memory) + middleware `checkPermission:` ở `MD/Routes/api.php:253-297` | |
| Model bảng giá | `MD/Entities/Product/ProductUnit.php` (fillable đủ cột chờ duyệt, quan hệ `prices`), `ProductUnitPrice.php` (fillable chỉ 5 cột, **thiếu** cờ chờ duyệt + 3 cờ TMĐT, không quan hệ `expected_prices`) · Human `Modules/Human/Entities/TpProductUnitPrice.php` (`getRetailPrices` nhân hệ số), `TpProductUnit`, `TpProductCompanyCoefficient` | **chưa có** model `ProductExpectedPrice`, `ProductApprove`, `ProductApprovePrice` ở HRM (chỉ query thô ở `Modules/Assign/Services/QuotationService.php`, xoá thô ở `ProductLifecycleService.php:162-166`) |
| Tồn kho | `Modules/Finance/Services/AccountingStockService.php:59` `detail()` (port `getAccountingStockDetail`, từng mã) | Màn giá cần 1 query gộp cho cả trang: `SELECT product_id, SUM(qty) FROM accounting_stocks WHERE stock_id IS NOT NULL AND product_id IN (…) GROUP BY product_id` (index `product_id` có sẵn; 23.411 dòng / 14.469 mã) |
| Lịch sử | `app/Services/CatalogHistoryService.php` — `log()` `:749`, `logUpdate()` `:785`, `logStatus()` `:830`, `getLogs()` `:847`, `getFilterOptions()` `:987` (người thực hiện qua `app/Services/HistoryPerformerOptions.php`); bảng `catalog_histories (table_name, table_id, action, old_value, new_value, note, changed_by, changed_at)` index `(table_name, table_id, changed_at)` | Ghi `table_name='product_prices'`, `table_id = products.id`, khoá dạng bảng theo ĐVT × loại giá (skill entity-history §3). ⚠️ route đọc chung không gate — làm endpoint riêng gate quyền (giá vốn) |
| Thông báo | `Modules/Timesheet/Services/EmployeeInfoService.php:466` `sendNotification`, `:519` `sendToAllNotification` (skill notification-convention: `[PREFIX] Nhóm: Tên. Ghi chú`) | ERP ghi cùng bảng `notifications` qua adapter (`app/Model/Common/Notification.php`) |
| Quy định công ty | `RegulationTabRegistry.php:384-400` + màn `hrm-client/components/regulation-config/RegulationConfigScreen.vue` | đọc cờ `is_company_price/is_all_brand/brand_ids` từ `companies` |
| Seeder quyền | `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1572-1584` (1652, 1653, 1655, 1670–1675) | id trống mục 0.7 |

---

## D. ERP sau khi HRM chạy — chặn / ẩn / giữ

### D1. Route (`routes/web.php`, nhóm `products` `:563-635`) — gắn `productMovedToHrm:<đích>` TRƯỚC `checkPermission`

| Dòng | Route | Xử lý | Đích HRM (thêm vào `TARGETS`) |
|---|---|---|---|
| 586 | GET `editPrices` `products.editPrices` | **MW** | `price-edit` ⇒ màn Cập nhật giá HRM |
| 596 | POST `{id}/updatePrice` `products.updatePrice` | **MW** (403 JSON) | — |
| 587 | GET `approvePrices` `products.approvePrices` | **MW** | `price-approve` ⇒ màn Duyệt giá HRM (cũng là đích của thông báo PTG/hàng tạm) |
| 588 | GET `approvePricesSearchData` | **MW** (chỉ màn duyệt ERP gọi; đọc nhưng lộ giá vốn không gate) | — |
| 589–592 | POST `approveSubmit` / `notApproveSubmit` / `approvesSubmit` / `notApprovesSubmit` | **MW** (đồng thời đóng N29) | — |
| 593 | GET `approveExportExcel` | **MW** nếu HRM port xuất Excel (G) | `price-approve` |
| 609 | GET `manualUpdatePrices` | theo **F5** | — |
| **GIỮ** | `:595` `getProductsAndPrices` (màn L3 `price_updating.blade.php:149` gọi, `type=updating`, không ghi; nút lưu ở view này không được gắn — `$scope.updatePrice` không có `ng-click`) · `:594` `priceUpdating` · `:608` `expectedPrices` · `:626` `exportExcelNorm` · `price_logs` `:4349-4352` (gop_db) · `price_*` PTG · `tmp_products/*` · `:46` `getPriceOfProducts` · `getData*` | TRẮNG | |

### D2. Menu / nút / chỗ trỏ
- `resources/views/layouts/topmenubar.blade.php:932` "Cập nhật giá nhanh" ⇒ đổi link sang HRM (dựng URL sẵn, không `@json`).
- `topmenubar.blade.php:2224-2226` "Danh sách hàng hóa chờ duyệt giá bán" ⇒ link HRM (giữ `@if can`).
- `resources/views/products/list.blade.php:39` nút "Cập nhật giá" ⇒ link HRM hoặc bỏ (màn HH ERP đã bỏ menu ở 2-D1).
- `resources/views/products/expectedPrices.blade.php:20` nút "cập nhật thủ công" ⇒ ẩn nếu F5 = chặn.
- `app/Http/Controllers/HomeController.php:587-600` (dashboard chờ duyệt) 2 link ⇒ trỏ HRM (số đếm giữ nguyên).
- `app/Observers/ProductWriteAuditObserver.php:24-29` bỏ `products.updatePrice`, 4 `products.*Submit` (và `product.manualUpdatePrices` nếu F5 = chặn) khỏi
  `WHITELIST_ROUTES` để mọi lần ghi giá thủ công sót lại đều vào log.
- Không sửa `ProductInfoController@editPrices`/`Product2Controller@editPrices`/`ProductTemplatesController@editPrices` (không có route).

### D3. Đường ghi giá CÒN LẠI ở ERP sau 2-D2 (phải ghi rõ trong plan)
Phiếu tính giá (+ nhánh duyệt, + `products.note`) — Phase 7 · Duyệt hàng tạm `Product::createRecord` (+ duyệt hàng mới theo `is_new_company`) —
Phase 6 · Cron 01:00 `product:update_price` · Cron 14:30 N5 · `manualUpdatePrices` (nếu F5 = giữ) · màn Quy chế công ty ERP vẫn ghi cờ duyệt.

---

## E. Số đo DB (`hrm_erp`, 09/10/2026)

| Đo | Kết quả |
|---|---|
| `product_approves` / `product_approve_prices` | 0 / 0 dòng (AUTO_INCREMENT 8 / 8 — có lượt ghi rồi xoá, vd PHPUnit `ProductLifecycleApiTest.php:281-282`) |
| Lịch sử duyệt thật (`product_units.approve_time`) | 47 ĐVT, 04/07/2025 → 26/01/2026: Cty 1 duyệt 28 / không duyệt 17; Cty 4: 1 / 1 |
| Cờ chờ duyệt (=1) | ĐVT 6 · dòng giá 5 · giá hiệu lực 6 (mồ côi, B7) |
| Cờ không duyệt (=2) | ĐVT 18 · dòng giá 92 · giá hiệu lực 17 · `approve_comment` khác rỗng 31 ĐVT |
| `products.status` | 0: 17.512 · 1: 28.371 · 2: 1 (`MNSG-GPO12CE`, Cty 1) · 5: 6 (Cty 1: 5, Cty 4: 1) |
| Danh sách màn giá (`status IN (1,2,5)` JOIN model) | 28.378 mã |
| Sửa được theo luật ERP (hãng SX + chủ = cty) | Cty 1: **27.029** · Cty 4: 966 · Cty 3: 14 · Cty 2: 1 · Cty 5/6/7/8: 0 (hãng SX: Cty 1 1.065, Cty 2 3, Cty 4 2, Cty 3 1) |
| `products.company_id` NULL / `manufacture_id` NULL | 0 / 0 (nhánh `canEdit` "NULL ⇒ ai cũng sửa" không có ca thật) |
| "Đang nhập thông tin" (`pcc.status = 1`) | **0** (1.105 dòng `pcc` đều `status` NULL — dữ liệu test 2-C đã dọn) |
| `companies` cờ duyệt | `is_company_price = 0` ×8 · Cty 8 `is_new_company = 1, is_new_brand = 1` |
| Dòng giá theo loại | 1–4: 46.560 · 5: 32.211 · 6: 46.195 (ĐVT: 46.560); trùng (ĐVT, loại): 0 |
| TMĐT sửa tay | giá 112 · hệ số 0 · ĐMGG 2 |
| `liquidation_sale_max_percent ≠ 0` / `norm ≠ 0` | 5.678 ĐVT / 23.319 mã |
| Hàng nhiều ĐVT | 589 mã (tối đa 4 ĐVT) |
| Giá hiệu lực tương lai (status 2) | 2.054 dòng |
| `accounting_stocks` | 23.411 dòng · 14.469 mã · 6.076 dòng `stock_id` NULL (bị loại) |
| Quyền ERP | `Cập nhật nhanh giá hàng hóa` 100063 (18 role) · `Duyệt giá hàng hoá` 100983 (12 role) · `Quản lý giá` 100127 (23 role) |
| Quyền HRM trống | 1657–1659, 1662–1669, 1699+ (develop dùng 1679–1698; gop_db dùng 1676–1678; feature dùng 1652/1653/1655/1670–1675) |

---

## F. Tồn nghiệp vụ cần hỏi (chỉ điều CHƯA chốt ở `ton.md` mục C) — hỏi lần lượt

| # | Câu | ⭐ Đề xuất | Hệ quả từng đáp án |
|---|---|---|---|
| **F1** | Duyệt / Không duyệt giá ở ERP **ghi đè `products.status`** (duyệt ⇒ 1, không duyệt ⇒ 5). HRM port có làm y vậy không? | ⭐ **Chỉ đổi khi hàng đang `status = 2` (hàng MỚI chờ duyệt từ ERP hàng tạm)**: duyệt 2 ⇒ 1, không duyệt 2 ⇒ 5; hàng đang 1 thì **giữ nguyên** | ⭐: hàng đang bán bị từ chối GIÁ vẫn bán/hiện bình thường ở HRM + ERP (chỉ giá đề nghị bị bỏ); luồng duyệt hàng mới của ERP vẫn đúng nghĩa. **Y ERP**: hàng đang bán bị từ chối giá ⇒ `status = 5` ⇒ biến mất khỏi màn công ty HRM (company_status NULL), không lấy về được (L3), popup ERP vẫn thấy (lọc `≠ 0`); duyệt có thể "hồi sinh" hàng `status = 0`. **Không đụng status**: hàng mới Cty 8 kẹt ở `status = 2` mãi |
| **F2** | Màn Cập nhật giá HRM **hiện hàng nào**? ERP hiện cả 28.378 mã cho mọi công ty, chỉ chặn lúc Lưu (Cty 2 sửa được 1 mã) | ⭐ **Mặc định chỉ hàng mình sửa được** (hãng SX + chủ = công ty), có ô lọc bỏ để xem toàn bộ (chỉ đọc, dòng không sửa được khoá ô + ghi lý do) | ⭐: đúng người đúng việc, vẫn xem được giá (tiền đề #5). **Y ERP**: CN thấy 28k mã, bấm lưu mới báo lỗi. **Chỉ hàng sửa được, không cho xem hết**: Cty 5–8 vào màn trống |
| **F3** | Hàng công ty đang **Ngừng kinh doanh (4)** có cho sửa giá? (ERP không có khái niệm này) | ⭐ **Chặn 423** như form (G9a/V1) | Chặn: muốn chỉnh giá phải mở khoá trước. Cho: giá vẫn chỉnh được khi đang khoá |
| **F4** | Ô lọc **Tồn kho (Còn/Hết)** của ERP là ô chết (BE comment). HRM? | ⭐ **Làm thật**, cùng định nghĩa cột Tồn kho (tổng tồn kế toán mọi kho, `stock_id` NOT NULL) | Làm: thêm 1 `EXISTS`/`NOT EXISTS`. Y ERP (bỏ ô): mất lọc. Giữ ô chết: lừa người dùng |
| **F5** | **`manualUpdatePrices`** (nút "cập nhật thủ công" ở *Trạng thái cập nhật giá*, GET có ghi — N30): chặn hay giữ? | ⭐ **Chặn** + ẩn nút | Chặn: chỉ còn cron 01:00 áp giá hiệu lực; cron lỗi thì phải chạy tay `artisan` (có `date` tham số). Giữ: nút **không lọc `flag`** (`PC:2243`) ⇒ có thể áp giá hiệu lực đang chờ duyệt (giá 0) vào giá thật |
| **F6** | Người duyệt **sửa hệ số/giá/ĐMGG** trước khi duyệt (ERP cho; nhưng duyệt hàng loạt ERP lại ghi `price` = giá đề nghị, lệch duyệt đơn). HRM? | ⭐ Cho sửa; **cả duyệt đơn và hàng loạt đều áp giá người duyệt nhập**; giá vốn **không** sửa (ERP lấy `pa.cost_price`) | ⭐: nhất quán. Y ERP: duyệt hàng loạt áp giá đề nghị nhưng lưu giá sửa vào cột chờ — sai im lặng. Không cho sửa: người duyệt phải từ chối rồi chờ lập lại |
| **F7** | **Thông báo** Duyệt giá trên HRM: prefix + ai nhận | ⭐ Prefix **`[GIA]`**. Gửi đề nghị ⇒ NV có quyền HRM *Duyệt giá* của `pa.company_id`: `[GIA] Chờ duyệt: <mã> – <tên>. Người đề nghị: <tên>`. Không duyệt ⇒ người đề nghị (`pa.updated_by`): `[GIA] Từ chối: <mã>. Lý do: <ghi chú>`. **Thêm** báo *Đã duyệt* cho người đề nghị (ERP không có) | ERP chỉ báo 2 chiều (gửi, từ chối). Thêm *Đã duyệt*: người đề nghị biết giá đã chạy. Bản ghi do PTG/hàng tạm (ERP) sinh vẫn chỉ báo cho quyền ERP — người duyệt HRM không nhận thông báo cho các bản đó (cần gán thêm quyền ERP hoặc chấp nhận) |
| **F8** | Bản ghi chờ duyệt do **PTG/hàng tạm ERP** sinh: thông báo ERP gửi cho NV có quyền ERP `Duyệt giá hàng hoá` (guard `web`), không phải quyền HRM. Có cần HRM tự bắn thêm? | ⭐ **Không** ở 2-D2 (PTG/hàng tạm chuyển ở Phase 6/7); chỉ đổi đích link thông báo ERP sang màn HRM (D1) + ghi việc ngoài luồng | Không: người duyệt cần có cả 2 quyền (ERP để nhận chuông, HRM để duyệt). Có: thêm hook ERP hoặc job HRM quét `product_approves` mới — vượt phạm vi |
| **F9** | Màn **Quy định HRM** tab Hàng hoá: ô "Hãng cần duyệt" (`brand_ids`, `new_brand_ids`) lấy danh sách **Thương hiệu** nhưng ERP hiểu là **Hãng SX** ⇒ sửa trong 2-D2 hay ghi N? | ⭐ **Sửa trong 2-D2** (đổi option sang `manufactures`, nhãn "Hãng sản xuất cần duyệt") — vì cờ này là công tắc của Duyệt giá đang port | Sửa: 1 dòng registry + test; dữ liệu hiện NULL nên không phải chuyển đổi. Ghi N (tiền đề #9): ai bật duyệt theo hãng từ HRM trước khi sửa sẽ áp sai hàng, im lặng |
| **F10** | Lịch sử giá: chỉ ghi **từ lúc HRM chạy**, hay đọc kèm lịch sử ĐVT/giá cũ của ERP (`product_histories.column_name = 'units'`, JSON cả bộ ĐVT) | ⭐ **Chỉ từ lúc HRM chạy**; popup ghi 1 dòng "Lịch sử trước <ngày> xem ở ERP" (route `productHistory` `web:574` còn) | ⭐: gọn, không phải giải mã JSON cũ. Đọc ERP: thêm bộ chuyển đổi JSON cũ, dính N26 (59.710 dòng mồ côi) |

**Thứ tự hỏi:** F1 → F9 → F2 → F3 → F6 → F7 → F8 → F5 → F4 → F10.

### Điểm kỹ thuật tự quyết (không hỏi)
- **K1** Quyền HRM (guard `api`, nhóm "Hàng hoá", type 9): **1657 "Cập nhật giá bán hàng hoá"** (vào màn + lưu + xem giá vốn trên màn + xem lịch
  sử giá) · **1658 "Duyệt giá bán hàng hoá"** (màn duyệt + 4 thao tác + xuất Excel). Tên tránh trùng với quyền ERP guard `web` (`Cập nhật nhanh giá
  hàng hóa`, `Duyệt giá hàng hoá`). Kiểm `uniq -d` + DB `permissions` ngay trước khi seed; seed chỉ 2 dòng (KHÔNG chạy cả seeder — memory).
- **K2** Cổng lưu giá: quyền 1657 → `products.status ∈ {1,2,5}` → hãng SX thuộc công ty (`manufactures.company_id`) → chủ hàng = công ty (giữ nhánh
  `company_id` NULL như ERP) → QC-5 `companyStatusSql(cty) ≠ 1` (423 "Hàng hoá đang nhập thông tin, chưa được nhập giá") → F3. 403/422 HTTP chuẩn
  HRM thay cho `success=false` HTTP 200 của ERP; validate báo đồng thời mọi ô (memory), giữ câu chữ ERP.
- **K3** BE **tự tính** TMĐT (HĐ4) cho cả giá hiện tại và giá hiệu lực khi cờ sửa tay tắt (không tin FE); `coefficient_ecommerce_price` đọc `configs`.
- **K4** Không ghi `products.norm`/`products.note` (QC-8) — chỉ trả ra để hiện; **không hiện, không ghi** `liquidation_sale_max_percent` (ERP không có cột,
  chỉ gửi lại giá trị cũ, 0 bị biến thành NULL); không ghi `unit_coefficient` khi duyệt (HĐ2 — ERP chép snapshot `pa.unit_coefficient`).
- **K5** Ghi `product_expected_prices.created_by/updated_by` = người thao tác; giá hiệu lực mới ở nhánh duyệt gán `price = 0, coefficient = 0` tường minh.
- **K6** Mỗi lượt lưu = 1 ĐVT trong 1 transaction, `lockForUpdate` dòng `product_units` (N27 tránh 2 người lưu chồng).
- **K7** Sinh bản ghi chờ duyệt đúng định dạng ERP (B1, B6), `company_id = products.company_id ?? cty`, `department_id/part_id` theo người tạo; sau
  duyệt/không duyệt **xoá `pa` + `pap`** như ERP; vết ghi vào lịch sử.
- **K8** Lịch sử: `catalog_histories` với `table_name = 'product_prices'`, `table_id = products.id`; action `update` (lưu giá), `submitted` (gửi duyệt),
  `approved`, `rejected` (+ `note` = ghi chú không duyệt); khoá dạng bảng `ĐVT × loại giá` (giá, hệ số, ĐMGG, giá hiệu lực + ngày), giá vốn theo ĐVT.
  Endpoint đọc riêng `GET master-data/product-prices/{product}/histories` gate 1657 **hoặc** 1658 (không mở qua `catalog-histories/{table}` chung —
  không thêm `product_prices` vào whitelist `CatalogHistoryService::TABLES` để route chung không lộ giá vốn).
- **K9** Lúc duyệt: nếu giá đang chạy ≠ `price_old` (cron/PTG đã đổi) ⇒ vẫn cho duyệt nhưng trả cảnh báo kèm số; cờ của giá hiện tại đã bị cron xoá ⇒
  vẫn áp theo bản duyệt (y ERP).
- **K10** Duyệt đơn lẻ kiểm `pa.company_id = cty` (ERP comment mất); bản ghi không còn ⇒ 404 "Yêu cầu duyệt đã được xử lý".
- **K11** Danh sách giá: sắp xếp chỉ nhận whitelist cột (`code`, `model_name`, `name`) — ERP nhận chuỗi tự do (`PC:2518-2521`). Lọc theo cây phân loại
  mới thay `product_cate`/`product_type` cũ (khảo sát C §4.2). Lọc "Trạng thái giá": Chờ duyệt (1) / Không duyệt (2) y ERP.
- **K12** Tồn kho trả kèm list (1 query gộp/trang, chia `unit_coefficient` ĐVT đang chọn ở FE như ERP); endpoint tồn 1 mã khi đổi ĐVT.
- **K13** ERP: thêm đích `price-edit`, `price-approve` vào `ProductMovedToHrm::TARGETS`; route chặn theo D1; menu/link theo D2. Việc ngoài luồng mới
  ghi `chot.md` N54+: lọc tồn kho chết, duyệt hàng loạt lệch giá, `manualUpdatePrices` bỏ qua cờ, cron xoá cờ chờ duyệt giá hiện tại, regulation
  option sai (nếu F9 = ghi N), `getProductsAndPrices` sắp xếp cột tự do.

---

## G. Ước lượng thay đổi

### G1. HRM `hrm-api` (nhánh con từ `feat/chuyen-doi-hang-hoa`)

| File | Mới/Sửa | Ghi chú |
|---|---|---|
| `MD/Entities/Product/ProductExpectedPrice.php` | mới | bảng `product_expected_prices`, `extends Model` |
| `MD/Entities/Product/ProductApprove.php`, `ProductApprovePrice.php` | mới | 2 bảng duyệt, quan hệ `prices` |
| `MD/Entities/Product/ProductUnitPrice.php` | sửa | fillable thêm 9 cột (3 sửa tay + 3 chờ duyệt + 3 cờ), quan hệ `expected_prices` |
| `MD/Services/ProductPrice/ProductPriceListService.php` | mới (~250) | query A1 + tồn kho + `can_edit` theo K2 |
| `MD/Services/ProductPrice/ProductPriceWriteService.php` | mới (~400) | A4 + K2–K8 |
| `MD/Services/ProductPrice/ProductPriceApprovalService.php` | mới (~350) | B3/B4 + K7, K9, K10, F1, F6 |
| `MD/Services/ProductPrice/ProductPriceHistoryService.php` | mới (~150) | snapshot/diff + đọc (dùng `CatalogHistoryService::log*`/`getLogs` hoặc tách hàm) |
| `MD/Services/ProductPrice/ProductPriceNotifier.php` | mới (~60) | F7 |
| `MD/Http/Controllers/V1/Product/ProductPriceController.php` | mới | `index`, `options`, `stock`, `update`, `histories` |
| `MD/Http/Controllers/V1/Product/ProductPriceApprovalController.php` | mới | `index`, `approve`, `reject`, `bulkApprove`, `bulkReject`, `export` |
| `MD/Http/Requests/ProductPrice/UpdateProductPriceRequest.php`, `ApprovePriceRequest.php`, `RejectPriceRequest.php` | mới | A2 |
| `MD/Transformers/ProductPrice/*Resource.php` | mới ×2 | ẩn `cost_price` khi thiếu quyền |
| `MD/Exports/ProductApproveExport.php` + blade | mới | skill export-excel (nếu giữ xuất Excel) |
| `MD/Routes/api.php` | sửa | ~12 route, route tĩnh trước `/{product}` |
| `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | sửa | +2 dòng 1657, 1658 |
| `MD/Support/RegulationTabRegistry.php` (+ `RegulationConfigService.php:551`) | sửa | chỉ nếu F9 = sửa |
| `MD/Tests/Feature/ProductPriceListTest.php`, `ProductPriceUpdateTest.php`, `ProductPriceApprovalTest.php` | mới | G3 |

≈ **20 file mới + 4–5 file sửa**, ~1.800–2.200 dòng BE (chưa kể test).

**Migration: KHÔNG CẦN** (bảng giá, bảng duyệt, `catalog_histories` đều có sẵn; quyền thêm bằng seeder). Không có thay đổi schema ⇒ không có ngoại lệ
tiền đề #1. (Nếu user muốn bảng lịch sử riêng `product_price_histories`-kiểu-HRM thay vì `catalog_histories` thì mới phát sinh 1 migration — NGOẠI LỆ, hỏi riêng;
lưu ý tên `product_price_histories` đã bị ERP chiếm, 0 dòng, FK sang `product_prices`/`product_versions`.)

### G2. ERP (`wt-erp-2d1` hoặc nhánh mới) — ~6 file
`routes/web.php` (7–9 dòng D1) · `app/Http/Middleware/ProductMovedToHrm.php` (+2 đích) · `resources/views/layouts/topmenubar.blade.php` (2 link) ·
`resources/views/products/list.blade.php:39` · `resources/views/products/expectedPrices.blade.php:20` (F5) · `app/Http/Controllers/HomeController.php:587-600` ·
`app/Observers/ProductWriteAuditObserver.php:24-29` · test ERP route/middleware (khuôn 2-D1).

### G3. PHPUnit ca chính (~40)
**Danh sách (8):** không quyền 1657 ⇒ 403 · trả `cost_price` chỉ khi có quyền · lọc mặc định chỉ hàng sửa được (F2) · bỏ lọc ⇒ thấy hàng công ty khác với
`can_edit=false` · lọc Chờ duyệt / Không duyệt · lọc tồn kho (F4) · tồn = SUM bỏ `stock_id` NULL · hàng thiếu dòng loại 5 vẫn trả đủ 6 dòng (ảo).
**Lưu giá (18):** không quyền ⇒ 403 · hãng SX công ty khác ⇒ 403 · chủ công ty khác ⇒ 403 · hàng "Đang nhập thông tin" ⇒ 423 (QC-5) · hàng Ngừng KD
⇒ 423 (F3) · `status = 0` ⇒ 403 · validate đồng thời (giá âm, hệ số 100, ngày hiệu lực hôm nay, 2 giá hiệu lực) · nhánh không duyệt ghi 6 giá + 3 cờ về 0
(HĐ3) · ĐVT thiếu loại 5 ⇒ sinh dòng (HĐ1) · TMĐT tự tính khi cờ tắt, giữ khi bật (HĐ4) · giá hiệu lực: tạo/sửa/xoá dòng tương lai không gửi, không đụng
status 1 (HĐ6) · giá vốn + lý do sửa giá ghi ĐVT, không đụng `buy_price/sale_max_percent_coefficient/unit_coefficient/liquidation` (HĐ5, K4) · không ghi
`norm/note` (QC-8) · không đụng `product_company_coefficients` (HĐ7) · lỗi giữa chừng rollback cả ĐVT (HĐ8) · ghi `catalog_histories` đúng diff, không đổi
⇒ không ghi · không ghi `product_versions/product_histories` · `created_by` giá hiệu lực.
**Nhánh duyệt (6):** `is_company_price=1` + hãng trong `brand_ids` ⇒ giá đang chạy giữ nguyên, ghi `*_wait_approve` + cờ 1 + `pa/pap` định dạng ERP +
thông báo người duyệt · hãng ngoài danh sách ⇒ ghi thẳng · `is_all_brand` · chỉ đổi giá vốn ⇒ `pa` không dòng giá · sửa lại về giá cũ ⇒ xoá `pap`/`pa` ·
lưu lần 2 cập nhật `pa` cũ (không tạo trùng).
**Duyệt (8):** không quyền 1658 ⇒ 403 · `pa` công ty khác ⇒ 403/404 · duyệt đơn áp giá người duyệt sửa + dời ngày hiệu lực quá khứ = mai + xoá `pa/pap` +
`status` theo F1 · duyệt hàng loạt cùng kết quả (F6) · không duyệt: cờ 1⇒2, `approve_comment`, `approve_time`, status theo F1, thông báo người đề nghị ·
đọc được `pa` do PTG sinh (`note_edit_price` NULL, không `reason`) · cảnh báo giá đã đổi (K9) · sau duyệt `PriceCalculate::approve` không còn bị chặn
(không còn `pa`).

E2E/Playwright thuộc phần khảo sát FE (không thuộc file này).
