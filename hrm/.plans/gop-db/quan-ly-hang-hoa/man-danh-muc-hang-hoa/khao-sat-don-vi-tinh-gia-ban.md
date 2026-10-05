# Khảo sát: Đơn vị tính ↔ Giá bán (21/09/2026)

> Đo thật trên DB gộp `hrm_erp` + mã nguồn `ERP/TanPhatDev`. Phục vụ thiết kế lại tab 1 (Đơn vị
> tính) và tab 6 (Giá bán) của màn hàng hoá.

## 0. Kết luận một câu

ERP **đã có** quản lý giá bán theo đơn vị tính **và theo thời gian** — nhưng cấu trúc nằm ở **3
tầng bảng**, có **luồng duyệt giá** riêng, và **2 bảng/1 cột trong tài liệu đã chết**. Việc thiết
kế lại chủ yếu là **gỡ phần chết + dựng lại giao diện**, không phải làm mới cơ chế.

## 1. Cấu trúc thật — 3 tầng

```
products
 └─ product_units                 46.560 dòng   ← hàng hoá × ĐƠN VỊ TÍNH
     │   is_base · unit_coefficient · cost_price (giá vốn) · buy_price (giá mua ngoài)
     │   according_base_price · liquidation_sale_max_percent · sale_max_percent_coefficient
     │   + 4 cột chờ duyệt
     └─ product_unit_prices      264.646 dòng   ← × 6 LOẠI GIÁ  (46.560 × 6)
         │   price · coefficient · sale_max_percent
         │   is_manual_price_online · is_manual_coefficient_online · is_manual_sale_max_percent_online
         │   + 6 cột chờ duyệt
         └─ product_expected_prices  95.266 dòng ← GIÁ THEO THỜI GIAN
                 price · coefficient · sale_max_percent · effect_date · status · flag
```

## 2. 6 loại giá (`price_types`)

| # | Tên | Số dòng giá |
|---|---|---|
| 1 | Bán lẻ | 46.560 |
| 2 | Đại lý cấp 1 | 46.560 |
| 3 | Đại lý cấp 2 | 46.560 |
| 4 | Đại lý cấp 3 | 46.560 |
| 5 | Giá bán theo lô | 32.211 |
| 6 | Giá bán thương mại điện tử (online) | 46.195 |

## 3. 🔴 Phần ĐÃ CHẾT — đừng bê sang

| Thứ | Bằng chứng |
|---|---|
| **Bảng `product_prices`** (20.127 dòng) | `launch_date` chỉ từ **25/05/2020 → 05/02/2021**, phủ 4.475/45.890 hàng hoá, chỉ 4 loại giá cũ. Bảng sống là `product_unit_prices` (264.646 dòng, phủ 100%). ⚠️ Bảng này **không có `unit_id`** — đây là thế hệ trước khi giá tách theo ĐVT. |
| **Cột "Giá công thức"** (`recipe_price`) | Có ô trên màn *Cập nhật nhanh giá* (`editPrices.blade.php:220,310,345`) nhưng **BE không trả trường này** — `ProductsController` và `Product.php` không hề nhắc `recipe_price`. Cột **luôn rỗng**. Dữ liệu cũ 3.828/20.127 dòng nằm ở bảng chết. `recipe_price` chỉ còn sống ở **hàng tạm** và **hàng hoá gốc**. |
| **`according_base_price`** (suy giá theo ĐVT cơ bản × hệ số) | chỉ bật **141 / 46.560** (0,3%). |

## 4. Luồng DUYỆT GIÁ — cơ chế "cột song song", không phải bảng riêng

Sửa giá **không ghi đè** giá đang chạy. Giá mới ghi vào cột `*_wait_approve` và bật cờ
`flag_*_wait_approve`; màn Sửa/Xem thì hiển thị **giá chờ duyệt** thay cho giá thật:

```sql
CASE WHEN flag_price_wait_approve IS NULL THEN price
     WHEN flag_price_wait_approve = 0    THEN price
     ELSE price_wait_approve END AS price          -- Product.php:999-1002, 1135-1138
COALESCE(product_units.coefficient_wait_approve, product_units.unit_coefficient)
```

Cờ có **3 trạng thái**: `NULL`/`0` = không có gì chờ · `1` = đang chờ duyệt · `2` = đã từ chối
(`ProductApprovesController:316` — `flag == 1 ? 2 : 0`).

Duyệt xong thì đẩy `*_wait_approve` sang cột chính, hạ cờ về 0, xoá `approve_comment`
(`ProductApprovesController:240-256`).

**Đang treo tại thời điểm đo:** `product_units` 6 · `product_unit_prices` 5 mỗi cờ ·
`product_expected_prices` 6. Ít — nhưng luồng có thật và đang chạy.

Quyền liên quan: `Quản lý giá` · `Cập nhật nhanh giá hàng hóa` · **`Duyệt giá hàng hoá`** ·
`Lập yêu cầu tính giá`.

## 5. Giá theo thời gian (`product_expected_prices`) — đang chạy thật

- 95.266 dòng, bản ghi mới nhất **14/09/2026**.
- `status = 1`: 79.297 dòng (effect_date 21/12/2020 → 03/09/2026) · `status = 2`: 15.969 dòng
  (19/09/2020 → **31/08/2027**).
- **2.495 dòng giá còn ở tương lai** (`effect_date > hôm nay`).

→ Yêu cầu "quản lý giá **theo thời gian**" trong tài liệu **đã có sẵn cơ chế**, không phải làm mới.

## 6. Dữ liệu đơn vị tính — gần như đơn trị

| Số ĐVT / hàng hoá | Số hàng hoá |
|---|---|
| 1 | **45.300** (98,7%) |
| 2 | 508 |
| 3 | 80 |
| 4 | 1 |

→ Giao diện nên **tối ưu cho trường hợp 1 ĐVT**, nhiều ĐVT là ngoại lệ (589 hàng hoá).

## 7. ⚠️ Đồng bộ CRM ngoài

`ProductUnitPrice::save()` (dòng 110-172) — khi `config('services.mate.use_crm')` bật **và** hàng
hoá có `product_template_id` thì **tạo bản ghi giá bên CRM** (`product.pricelist.item`) và ghi
`module_mappings`. Trường đẩy đi: `fixed_price = price / unit_coefficient`, `total_package_price`,
`packaging_id`.

- **29.813 / 45.890** hàng hoá có `product_template_id` → thuộc diện đồng bộ.
- Trên DB local: `MATE_API_USE_CRM` mặc định `false`, `module_mappings` cho `product.pricelist.item`
  = **0 dòng** → chưa chạy ở đây. **Phải hỏi lại: production có bật không.**
- Nếu bật mà HRM ghi giá không qua đường này ⇒ **giá bên CRM đứng yên**, lệch âm thầm.

## 8. Đối chiếu tài liệu tab 6 ↔ chỗ lưu thật

| Trường trong tài liệu | Lưu ở đâu | Ghi chú |
|---|---|---|
| Đơn vị tính | `product_units.unit_id` | 🟢 |
| Giá vốn | `product_units.cost_price` | 🟢 dữ liệu nhạy cảm — gate quyền `Quản lý giá` |
| Giá mua ngoài | `product_units.buy_price` | 🟢 |
| Loại giá | `product_unit_prices.price_type_id` | 🟢 6 loại |
| Hệ số | `product_unit_prices.coefficient` | 🟢 |
| Giá bán | `product_unit_prices.price` | 🟢 |
| Định mức đàm phán giá | `product_unit_prices.sale_max_percent` | 🟢 |
| Ngày hiệu lực | `product_expected_prices.effect_date` | 🟢 nhưng là **bảng tầng 3**, không cùng dòng với giá hiện hành |
| **Giá công thức** | ❌ **không có nguồn** | cột trên màn hiện luôn rỗng; dữ liệu cũ ở bảng chết |
| **Hệ số giá theo công ty** | `product_company_coefficients` (1.105 dòng) | 🟡 bảng riêng, không thuộc 3 tầng trên |

## 9. Các màn đang có

| Màn | Route | Quy mô |
|---|---|---|
| Khối "Giá theo đơn vị" trong form hàng hoá | `productCreate` / `productEdit` | nằm trong `form.blade.php` 95KB |
| **Cập nhật nhanh giá hàng hoá** | `products.editPrices` | view **678 dòng**; cột: Giá vốn · Giá · Loại · Giá hiện tại · Hệ số · ~~Giá công thức~~ · Giá mới · ĐMGG · Ngày hiệu lực |
| **Duyệt giá hàng hoá** | `products.approvePrices` | view **727 dòng** |
| Giá dự kiến | `product.expectedPrices` | view 85 dòng |
| Cập nhật giá thủ công | `product.manualUpdatePrices` | — |
| Cập nhật giá (job) | `product.priceUpdating` | — |

**41 file** đọc `product_unit_prices` / `ProductUnitPrice`.

## 10. QUYẾT ĐỊNH (user chốt 21/09/2026)

> **"Chỉ bỏ đồng bộ CRM ⇒ luồng này không dùng nữa. Còn lại không thay đổi logic quản lý."**

| Hạng mục | Chốt |
|---|---|
| Cấu trúc 3 tầng (`product_units` → `product_unit_prices` → `product_expected_prices`) | **GIỮ NGUYÊN** |
| Luồng duyệt giá bằng cột `*_wait_approve` + cờ 3 trạng thái | **GIỮ NGUYÊN** |
| 6 loại giá | **GIỮ NGUYÊN** |
| Giá theo thời gian (`effect_date`) | **GIỮ NGUYÊN** |
| Giá vốn / giá mua ngoài ở `product_units` | **GIỮ NGUYÊN** |
| **Đồng bộ CRM** | ⚫ **BỎ** |

📌 Suy ra cho giao diện mới (không phải đổi logic, chỉ là không port phần chết):
`product_prices` là bảng chết → không đọc. Cột **"Giá công thức"** không có nguồn dữ liệu ở
đường hàng hoá → **không dựng lại ô này** trên màn mới; nếu sau này cần thì phải làm nguồn trước.

## 11. Bỏ đồng bộ CRM — phạm vi đo được

### 11.1 Luồng hàng hoá ĐÃ NGỪNG gần 1 năm

`MATE_API_USE_CRM` **không khai trong `.env`** của ERP → mặc định `false`.

| Nhánh (`erp_model`) | Số mapping | Bản ghi mới nhất |
|---|---|---|
| `ProductUnitPrice` (`crm_model = product.price.list`) | **113.044** | **08/10/2025** |
| `ProductModel` | 32.842 | 08/10/2025 |
| `ProductUnit` | 24.246 | 08/10/2025 |
| `ProductTemplate` / `Product` | 23.813 / 23.811 | 08/10/2025 |
| `Customer` · `ProductSupplier` · `Brand` | 3.708 · 1.071 · 981 | 09–10/2025 |

⚠️ Sửa lại số đã nêu trước đó: lần đầu tôi tra `crm_model = 'product.pricelist.item'` (tên dùng
trong `ProductUnitPrice::save()`) ra **0 dòng** và kết luận nhầm là chưa từng chạy. Tên thật trong
`module_mappings` là **`product.price.list`** — có 113.044 dòng. Kết luận "đã ngừng" vẫn đúng,
nhưng vì mốc thời gian chứ không phải vì thiếu dữ liệu.

### 11.2 ⚠️ Nhánh CÒN SỐNG — KHÔNG được gỡ nhầm

| `erp_model` | Số mapping | Mới nhất |
|---|---|---|
| **Employee** | 1.147 | **14/09/2026** |
| **EmployeeInfo** | 1.109 | **14/09/2026** |
| Department | 177 | 18/07/2026 |
| Part | 44 | 17/07/2026 |
| Company | 8 | 22/01/2026 |

Đồng bộ **nhân sự / cơ cấu tổ chức** vẫn đang chạy ⇒ "bỏ đồng bộ CRM" = **bỏ nhánh hàng hoá & giá**,
giữ nguyên nhánh nhân sự.

### 11.3 Khối lượng

`use_crm` xuất hiện ở **40 file / 76 chỗ**; **38 model** gọi đồng bộ trong `save()`; 31 service
`app/Services/CRM/`; `ModuleMapping` ở **101 file / 399 chỗ**; `getCompareId` 29 file / 114 chỗ.

**13+ model thuộc nhánh hàng hoá:** `Product` · `ProductTemplate` · `ProductUnit` ·
**`ProductUnitPrice`** · `ProductModel` · `Brand` · `Manufacture` · `Origin` · `Unit` · `TaxRate` ·
`Attribute` · `AttributeProduct` · `AttachmentType` · `Group` · `ProductGroupClassify` ·
`Scope`/`Chapter`/`JobGroup`/`JobCluster`.

### 11.4 🔑 Liên quan ngược tới Phase 1

8 model trong danh sách trên — `Brand`, `Manufacture`, `Origin`, `Unit`, `TaxRate`, `Attribute`,
`ProductModel`, `AttachmentType` — **chính là các danh mục đã port sang HRM ở Phase 1**. HRM dùng
model Eloquent riêng nên **không chạy `save()` của ERP**, tức đồng bộ CRM đã bị bỏ qua từ Phase 1
mà không ai phát hiện. Quyết định bỏ luồng này **khép luôn lỗ hổng đó** — không còn nợ kỹ thuật
treo lại từ Phase 1.

## 12. Câu còn lại cần chốt

**Giá theo công ty** (đã chốt tách Phase 3) sẽ nhân lên với 6 loại giá × ĐVT × thời gian:
8 công ty × 6 loại giá × 46.560 ĐVT ≈ **2,2 triệu tổ hợp giá**. Cần xác nhận khối lượng này đúng ý
trước khi thiết kế Phase 3.
