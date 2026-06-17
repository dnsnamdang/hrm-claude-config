# Design Phase 31 — Logic hàng hoá cha-con (BOM + Báo giá)

> Spec chi tiết. Tóm tắt ở `design.md`. Phạm vi: cả BOM và Báo giá tự lập.
> Ngày: 2026-06-08 — @dnsnamdang — branch `tpe-develop-assign`.

## 1. Mục tiêu

Chuẩn hoá lại logic tạo và tính giá hàng hoá cha-con, phân biệt rõ 2 nguồn cha:

1. **Cha là hàng ERP**: con tự động lấy theo công thức ghép bộ có sẵn trong ERP (`recipe_products`), khoá hoàn toàn — không cho thêm/bớt/sửa.
2. **Cha là hàng tạm (tự tạo)**: được tự chọn con (ERP hoặc tự tạo), nhập giá tay, có validate cha ≥ Σ con.

## 2. Nhận diện "bộ ghép" trong ERP

- ERP DB = connection `mysql2`, DB `env('DB_DATABASE_SECOND')`.
- Bảng `recipe_products`:

  | Cột | Ý nghĩa |
  |---|---|
  | `base_product_id` | ID hàng CHA (bộ ghép) |
  | `product_id` | ID hàng CON (thành phần) |
  | `qty` decimal(12,2) | SL con / 1 bộ cha |
  | `unit_id` | Đơn vị con |
  | `is_main` | Cờ thành phần chính (chỉ tham khảo, không dùng cho logic) |

- Một hàng ERP **là bộ ghép** ⇔ tồn tại ≥1 dòng `recipe_products` với `base_product_id = <id hàng đó>`. **Không** phụ thuộc `products.product_type`.
- Toàn DB hiện có 864 base products.

## 3. Logic tạo hàng cha-con

| Loại cha | Nguồn con | Thêm/bớt/sửa con thủ công |
|---|---|---|
| Hàng ERP **có** recipe | Auto snapshot từ `recipe_products` lúc chọn cha | ❌ Khoá hoàn toàn |
| Hàng ERP **không** recipe | Không có con (hàng lẻ) | ❌ Không cho thêm con |
| Hàng tạm (tự tạo) | Chọn tay | ✅ Con = ERP hoặc tự tạo |

**Quy tắc:**
- Chỉ **hàng tạm** mới hiện nút "thêm hàng con". Hàng ERP không hiện nút thêm con.
- Con của cha tạm là **hàng ERP** → chỉ user có quyền **"Xem giá vốn hàng hoá"** mới được chọn (FE ẩn lựa chọn ERP, BE chặn nếu thiếu quyền).
- **Bỏ** quy tắc cũ "cha tự tạo không được thêm con ERP" (Phase erp-cost-catalog P17). Nay cho phép, gắn theo quyền.
- **Giữ** quy tắc: cha là dịch vụ (`product_type=2`) → không có con (tự strip).
- **Giữ** quy tắc: con không trùng `erp_product_id` với chính cha trực tiếp của nó.
- Cha-con tối đa **1 cấp** (con không có con) — giữ nguyên hiện trạng.
- Áp dụng cho **cả BOM và Báo giá tự lập**.

## 4. Snapshot recipe (cha ERP)

Khi user chọn cha là hàng ERP:
- BE check `recipe_products` theo `base_product_id`.
- Có recipe → trả danh sách con kèm: `erp_product_id` (=product_id), `code`, `name`, `model/brand/origin/unit`, `product_attributes`, `qty` (= recipe.qty × SL cha), `cost_price`, `list_price` (lấy từ `TpProductUnitPrice::getCostPrices/getRetailPrices`).
- FE lưu thành các dòng con `parent_id` trỏ về cha, khoá toàn bộ ô nhập.
- Không recipe → cha là hàng lẻ, không tạo con.
- **Snapshot 1 lần** (info sản phẩm + giá): ERP đổi recipe sau khi đã lưu → KHÔNG cập nhật phiếu cũ.
- **SL con KHOÁ** (không sửa tay) = `recipe_qty × SL cha`. **Đổi SL cha → SL con tự nhân lại** theo `recipe_qty` (SL gốc/1 bộ). (Cập nhật 2026-06-09 — đổi quyết định cũ "không re-scale".)
  - Endpoint trả thêm `recipe_qty` (SL gốc/1 bộ). FE lưu `_recipeUnitQty`; khi load lại phục hồi = `qty_con / SL_cha`. Đổi SL cha → `qty_con = _recipeUnitQty × SL_cha`.

## 5. Logic giá

### 5.1 Hàng ERP (cha hoặc con)
- Giá nhập (`estimated_price` / `cost_price`) + giá bán (`quoted_price` / `list_price`): **luôn khoá**, lấy từ ERP, không cho sửa.

### 5.2 Cha tự tạo
- **Giá nhập** (`estimated_price`): **GIỮ auto roll-up** = `Σ(giá nhập con × SL con) / SL cha`, input khoá (như Phase 14A hiện tại).
- **Giá bán** (`quoted_price`, chỉ có ở Báo giá): **nhập tay**.
- Con của cha tự tạo: nếu là ERP → giá khoá; nếu tự tạo → nhập tay.

### 5.3 Hiển thị giá bán hàng con
- Con của **cha tự tạo**: hiện **giá bán đầy đủ** trên báo giá (hiện tại đang ẩn → sửa).
- Con của **cha ERP**: giữ nguyên như hiện tại (không hiện giá bán con).

### 5.4 Validate cha ≥ Σ con (chỉ cha tự tạo, chỉ Báo giá)
- Điều kiện: **thành tiền giá bán cha ≥ Σ thành tiền giá bán con**, tức:
  `quoted_price_cha × qty_cha ≥ Σ(quoted_price_con × qty_con)`.
- Mức so sánh = **thành tiền (tổng)** (đơn giá ↔ thành tiền tương đương về toán học vì SL con tỷ lệ SL cha; chọn thành tiền để khớp cột hiển thị, tránh sai số làm tròn).
- Vi phạm → **chặn lưu**, BE rethrow `ValidationException` (không catch chung), FE hiện lỗi inline tại ô giá bán cha (`is-invalid` + `invalid-feedback`), dùng flag `touched`.
- Validate giá nhập cha ≥ Σ giá nhập con **tự thoả mãn** do giá nhập cha auto = Σ con → không cần chặn riêng (có thể thêm guard `>=` phòng thủ, không bắt buộc).
- Cha ERP: **không** validate (giá cố định từ ERP).

## 6. Toggle hiển thị hàng con (cha ERP)

- Mỗi dòng cha ERP có cờ riêng `show_children` (mặc định = 1, hiện).
- Bật/tắt → ẩn/hiện các dòng con của riêng cha đó trên **màn xem + in + export báo giá** (và màn BOM tương ứng).
- Lưu cột mới `show_children` trên `bom_list_products` + `quotation_product_prices`.
  - **Báo giá type=1 (từ BOM):** lưu trên overlay `quotation_product_prices` của dòng cha (per-phiếu) — toggle KHÔNG ghi đè BOM gốc.
  - **Báo giá type=2 (tự lập):** lưu trên `quotation_product_prices` của dòng cha.
  - **Màn BOM:** lưu trên `bom_list_products`.
- Cha tự tạo: con luôn hiện (không có toggle) — toggle chỉ cho cha ERP.

## 7. Thay đổi Database

Migration mới (theo convention, KHÔNG SoftDeletes, KHÔNG branch_id):

```php
// 2026_06_08_000001_add_show_children_to_bom_and_quotation_products.php
Schema::table('bom_list_products', function (Blueprint $t) {
    $t->tinyInteger('show_children')->default(1)->after('parent_id');
});
Schema::table('quotation_product_prices', function (Blueprint $t) {
    $t->tinyInteger('show_children')->default(1)->after('parent_id');
});
```

- Con vẫn dùng cột `parent_id` sẵn có (cả 2 bảng đã có).
- Không cần bảng mới, không cần đụng `recipe_products` (chỉ đọc).

## 8. API / Backend

### 8.1 Endpoint lấy con recipe (mới)
- `GET /assign/bom-lists/erp-recipe-children?erp_product_id=&qty=` (hoặc POST nhiều id).
- Controller: `BomListController` (cạnh `searchErpProducts` / `getErpProductPrices`).
- Logic:
  1. Query `recipe_products` (mysql2) theo `base_product_id`.
  2. Lấy info `TpProduct` + giá `TpProductUnitPrice::getCostPrices/getRetailPrices` cho danh sách `product_id`.
  3. Map kèm `qty = recipe.qty × qtyCha`, `source='ERP'`, `is_recipe_child=true`.
  4. Rỗng → trả `[]` (cha là hàng lẻ).
- Gắn quyền xem: trả `cost_price` chỉ khi `isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá')` (đồng nhất `DetailQuotationResource`).

### 8.2 BomListService (store/update) — CÁCH A (chốt 2026-06-08)
> Recipe bên ERP là read-only (không sửa được) → BE **tin payload FE** (FE đã đổ con từ endpoint `erp-recipe-children` và khoá). Không re-derive ở BE.
- `processGroups()` / `mapProductPayload()`:
  - Lưu `show_children` cho dòng cha.
  - Cha ERP có recipe: lưu con FE gửi (đã là snapshot recipe, khoá) — BE không re-query.
  - Cha tạm: giữ con FE gửi; nếu con là ERP mà user **không** có quyền "Xem giá vốn hàng hoá" → throw `ValidationException`.
  - Bỏ rule chặn con ERP dưới cha tạm (dòng ~891-892 hiện tại).

### 8.3 QuotationService (save/update + create)
- **Hai luồng dữ liệu (đã verify):**
  - **Type=1 (từ BOM):** `quotation_product_prices` chỉ là overlay giá (key `bom_list_product_id`). Cấu trúc cha-con + `erp_product_id` thừa hưởng từ `bom_list_products` qua join lúc đọc → các hàm `create()/createFromRequest()/createFromBom()` **KHÔNG cần copy `parent_id`**. Vòng copy overlay đã iterate toàn bộ bomProducts (gồm con).
  - **Type=2 (tự lập):** mọi field trên `quotation_product_prices` (có `parent_id`). `saveProductsFromFE` resolve `parent_id` con cha tạm qua pass2 (temp_id → id thật).
- `saveProductsFromFE`: áp recipe snapshot + rule ERP-parent (giống BomListService) khi type=2 pick ERP combo; chặn con thủ công dưới cha ERP; con ERP dưới cha tạm cần quyền. Lưu `show_children`.
- Validate cha tự tạo (cả type=1 + type=2 trong save path): `quoted_price_cha × qty ≥ Σ(quoted_price_con × qty_con)` → rethrow `ValidationException`. Cha ERP không validate.

### 8.4 DetailQuotationResource
- Trả `show_children` cho mỗi dòng cha ở **CẢ 2 nhánh**: type=2 (if, dòng 36-66) lấy `$qpp->show_children`; type=1 (else, dòng 91-116) lấy `$qpp->show_children` từ overlay.
- `quoted_price` (giá bán) hiện **đã luôn trả** cho mọi dòng (chỉ `estimated_price` bị gate quyền) → việc ẩn giá bán con là **FE template**, không sửa ở resource. FE quyết hiển thị con theo `erp_product_id` của cha.

## 9. Frontend (2 EDITOR TÁCH BIỆT)

> BOM dùng `BomBuilderEditor.vue` (+ `BomBuilderTableCard`, `BomBuilderAddProductModal`).
> Báo giá dùng `pages/assign/quotations/_id/edit.vue` (~3800 dòng) + `_id/index.vue` (view) + `QuotationPrintPreview.vue` (in).
> Mọi thay đổi UI cha-con/giá/toggle phải làm ở **CẢ 2 nơi**.

- **Pick cha**:
  - Chọn ERP → gọi endpoint recipe-children → nếu có con: đổ con khoá, ẩn nút thêm con; nếu không có con: hàng lẻ, ẩn nút thêm con.
  - Chọn/để hàng tạm: hiện nút thêm con.
- **Thêm con (cha tạm)**: modal chọn nguồn ERP/tự tạo; tab ERP chỉ hiện khi có quyền "Xem giá vốn hàng hoá" (FE check qua flag `can_view_cost_price` BE trả về).
- **Giá**:
  - Bỏ disable-by-children cho ô giá nhập? KHÔNG — giữ auto roll-up giá nhập cha tạm (input disabled, tính từ con).
  - Ô giá nhập/bán hàng ERP: `disabled`.
  - Ô giá bán cha tạm: cho nhập; validate inline ≥ Σ giá bán con (touched).
  - Con cha tạm: render cột giá bán (bỏ ẩn).
  - Con cha ERP: giữ ẩn giá bán.
- **Toggle con (cha ERP)**: icon/checkbox trên dòng cha ERP, bind `show_children`; ẩn/hiện dòng con tương ứng ở màn xem + in + export.
- **Validate submit**: chặn lưu nếu có cha tạm vi phạm; cuộn tới dòng lỗi.

## 10. Edge cases

1. Cha ERP có recipe nhưng 1 `product_id` con đã ngừng bán (`status≠1`) → vẫn snapshot (snapshot là ảnh chụp); cảnh báo nhẹ nếu cần (tuỳ chọn, không bắt buộc).
2. Đổi SL cha ERP sau snapshot → con giữ SL snapshot (không auto scale). Muốn cập nhật → chọn lại cha.
3. Cha tạm có con ERP, user mất quyền giá vốn khi mở lại phiếu cũ → giá vốn con ẩn theo quyền, nhưng dòng con vẫn giữ; không cho thêm con ERP mới.
4. Validate giá bán: cha tạm chưa nhập giá bán (=0) mà Σ con > 0 → vi phạm → chặn.
5. Con tự tạo dưới cha tạm: giá nhập/bán nhập tay; vẫn tính vào roll-up giá nhập cha + Σ validate giá bán.
6. Import Excel báo giá: giữ validate cha ≥ Σ con cho cha tạm (đồng bộ logic 2-pass hiện có ở Phase 19).

## 11. Downstream impact

- Export Excel BOM/Báo giá: tôn trọng `show_children` (ẩn dòng con khi tắt) — sửa `BomListExport`.
- In báo giá: tôn trọng `show_children`.
- Lịch sử BOM (`BomListLog`): log thêm trường `show_children` nếu cần (tuỳ chọn).
- Product-project (read-only từ `bom_list_products`): không ảnh hưởng (chỉ thêm cột).

## 12. Permission

- Dùng quyền sẵn có **"Xem giá vốn hàng hoá"** — KHÔNG tạo quyền mới.
- Không thêm phân quyền theo cấp.
