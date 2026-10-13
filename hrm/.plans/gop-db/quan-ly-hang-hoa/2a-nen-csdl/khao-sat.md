# Đợt 2-A — Nền CSDL màn hàng hoá: khảo sát

> 04/10/2026 · @namdangit · đo trên DB local `hrm_erp` (chỉ đọc) + đọc code ERP `TanPhatDev` và hrm-api `gop_db`.
> Phạm vi 2-A (sổ chốt §2c): trạng thái + 4 cột quản trị trên `product_company_coefficients` (A1, §24) ·
> `product_suppliers.company_id` · bảng `product_business_catalogs` (A6) · backfill hàng cũ (A3).
> Chưa đụng source, chưa ghi DB.

## 1. Số đo

| Hạng mục | Số |
|---|---|
| `products` | 45.890 — status 1 (Hoạt động) **28.371** · 0 (Khoá) 17.512 · 5 (Không duyệt) 6 · 2 (Chờ duyệt) 1 · 3/4: 0 |
| Hàng không có `company_id` | **1** (status 0) — "5 hàng mồ côi" của §35a nay chỉ còn 1, và không thuộc diện sinh dòng |
| Hàng status 1 còn `deleted_at` | 175 (bẫy SoftDeletes — ERP vẫn coi là đang hoạt động) |
| `products.company_id` | Cty 1: 44.816 · Cty 4: 1.056 · Cty 3: 14 · Cty 2: 3 |
| `product_company_coefficients` | 1.105 dòng / 589 hàng / 4 công ty; hệ số 1.0000–2.0000; **UNIQUE(product_id, company_id) ĐÃ CÓ SẴN**; `coefficient` decimal(10,4) **NOT NULL** |
| …trong đó dòng của **công ty tạo** | **5** — còn **1.100 dòng là công ty KHÁC** (Cty 2 HP: 538 · Cty 3 Vinh: 516 · Cty 4 SG: 46) |
| `product_suppliers` | 1.741 dòng / 1.740 hàng; 0 dòng mồ côi; chưa có `company_id`; không có unique |
| Dữ liệu 3 cột chung sẽ chuyển | `min_stock_qty` ≠ 0: 754 · `guarantee` có giá trị: 23.869 · `guarantee_type`: 45.429 |
| `product_business_catalogs`, `product_company_units` | chưa tồn tại |
| 4 migration lỡ chạy (batch 410–414) | `add_classification_to_products` · `drop_can_retail_from_product_types` · `add_updated_at_index_to_products` · `add_status_to_vehicle_life` · `add_declare_flags_to_product_types` |

## 2. 🔴 Phát hiện chặn: A1 đặt trạng thái lên bảng mà ERP coi "có dòng = có hệ số giá"

ERP + HRM đọc `product_company_coefficients` ở ~20 chỗ, đều theo nghĩa **"có dòng cho công ty này
⇒ nhân hệ số vào giá bán"**. A3 sinh ~28.371 dòng mới cho công ty tạo. Dòng mới mang `coefficient` gì
cũng hỏng:

| Giá trị `coefficient` của dòng mới | Hậu quả |
|---|---|
| `NULL` (phải nới NOT NULL) | `Product::getDataAttribute` (Product.php:1210), `PrincipleOrderStoreRequest:118`, `ZTPrincipleOrderStoreRequest:69`, `PrincipleOrderService:397`: `$obj ? $obj->coefficient : 1` → null ⇒ `null != 1` ⇒ **giá × null = 0** ở form hàng hoá ERP và đơn hàng nguyên tắc |
| `1` | `SearchController` 7 chỗ (popup hàng hoá 338 màn) + `Product.php:1727` + HRM `ServiceService:1055` dùng `CASE WHEN pcc.coefficient IS NOT NULL THEN ROUND(price × coef / 1000) × 1000` ⇒ **giá bị làm tròn nghìn**. Đo: **33.129 dòng giá / 8.904 hàng** status 1 có giá lẻ nghìn sẽ đổi giá hiển thị trong popup — im lặng |

Thêm nữa, ERP **xoá sạch rồi ghi lại** toàn bộ dòng của hàng hoá mỗi lần lưu (`syncCompanyCoefficients`:
`where('product_id')->delete()`), gọi từ:
- form hàng hoá ERP (ProductsController:1532, Product2Controller:1260, ProductTemplatesController:1474, Product.php:6909) — sẽ chặn ở 2-D;
- 🔴 **màn Hãng sản xuất ERP** (`Sale/ManufacturesController:274`): lưu 1 hãng ⇒ chạy cho **mọi hàng status 1 của hãng**
  ⇒ xoá sạch trạng thái + dữ liệu quản trị của hàng nghìn mã một lượt. Route này KHÔNG nằm trong diện chặn của 2-D.

⇒ Đặt trạng thái/dữ liệu quản trị lên bảng này thì 2-A **không thể đi trước 2-D**, và còn phải sửa
~20 chỗ đọc hệ số (ERP + HRM) để phân biệt "dòng trạng thái" với "dòng hệ số".

### Đề xuất: đảo A1 về phương án bảng riêng `product_companies`

```
product_companies   (bảng chủ hàng × công ty — MỚI)
  id, product_id, company_id   UNIQUE(product_id, company_id), FK products/companies
  status                       Đang nhập thông tin / Chờ tính giá / Đang kinh doanh (hằng HRM)
  business_policy_id · min_stock_qty · guarantee · guarantee_type   (§24, thay cột chung)
  created_by, updated_by, timestamps
product_company_coefficients — GIỮ NGUYÊN, chỉ còn đúng nghĩa hệ số giá
```

| | A1 hiện tại (cột trên `product_company_coefficients`) | Đề xuất (`product_companies`) |
|---|---|---|
| Đổi giá ERP/HRM khi backfill | có (tròn nghìn 8.904 hàng, hoặc giá = 0) | **không** |
| Sửa code đọc hệ số | ~20 chỗ ERP + HRM | 0 |
| ERP lưu hàng / lưu hãng xoá mất trạng thái | có — phải chặn route trước (2-D) + sửa ManufacturesController | **không** |
| Thứ tự 2-A ↔ 2-D | 2-D bắt buộc trước | 2-A đi trước được |
| Giá phải trả | — | 2 bảng cùng khoá (hàng × công ty): form HRM ghi hệ số thì phải đảm bảo đã có dòng `product_companies` (lý do §35a từng loại phương án này) |

## 3. Các câu khác cần chốt (sau câu ở mục 2)

1. **Công ty chi nhánh đang dùng hàng của Cty 1.** 1.100 dòng hệ số cho thấy Cty 2 (HP), 3 (Vinh), 4 (SG)
   đang bán hàng của Cty 1. A3 chỉ sinh trạng thái cho công ty tạo ⇒ khi popup/màn lọc theo trạng thái
   của công ty đăng nhập (A8, Phase 4), **chi nhánh trắng hàng**. Đề xuất: backfill thêm dòng *Đang kinh
   doanh* cho (hàng × công ty) đã có dòng hệ số (1.100 dòng); phần còn lại để Phase 4 quyết cách popup
   lọc. Cần user chốt có mở rộng A3 hay không.
2. **Status 2 (Chờ duyệt, 1 hàng) và 5 (Không duyệt, 6 hàng)**: đề xuất **không sinh dòng** (không phải
   "đang hoạt động" theo A3).
3. **175 hàng status 1 còn `deleted_at`**: đề xuất **vẫn sinh dòng Đang kinh doanh** (bám ERP đang chạy:
   ERP không dùng SoftDeletes, coi là đang bán).
4. `product_suppliers.company_id`: A4 chốt NOT NULL "để cuối". Đề xuất 2-A: thêm cột **nullable** + gán =
   `products.company_id` (1.741/1.741 gán được), ép NOT NULL ở bước cuối cùng với xoá cột chung.
5. **4 cột quản trị**: 2-A chỉ **chép** sang bảng theo công ty, **không xoá** cột trên `products` (bước 5
   §24c-1, sau khi rà 71 file ERP).
6. **A5 `product_company_units` (tách giá vốn)** không có trong danh sách 2-A của §2c — đề xuất để
   Phase 8 (giá), 2-A không làm.
7. **4 migration lỡ chạy** (E1): nhánh mới từ `gop_db` không có các file này nhưng bảng `migrations`
   local có. `can_retail` đã drop trong khi `gop_db` vẫn đọc/ghi. Cần quyết cách xử lý khi mở nhánh 2-A
   (lấy lại migration `add_classification` vào nhánh mới? khôi phục `can_retail` trên DB local?).

## 4. Chốt (04/10/2026)

| # | Chốt |
|---|---|
| K0 | ⛔ Không merge gì vào `gop_db` (nhánh production). Hệ số giá **sẽ bỏ** sau khi xong toàn bộ luồng chuyển đổi |
| K1 | **Giữ A1** (trạng thái + 4 cột quản trị trên `product_company_coefficients`), **hệ số gỡ ở phase sau**. ⇒ 2-A chỉ THÊM CỘT (nullable), **KHÔNG backfill / không sinh dòng mới**; backfill A3 hoãn tới khi phase giá gỡ xong mọi chỗ đọc hệ số. Hệ quả chấp nhận: các màn 2-B/2-C chạy trên dữ liệu rỗng với hàng cũ cho tới lúc đó. Các câu 3.1–3.3 (chi nhánh, status 2/5, `deleted_at`) chuyển sang lúc backfill |
| K2 | Dòng (hàng × công ty) HRM sinh từ 2-C (tạo hàng / lấy hàng về) ghi **`coefficient = 1`**, giữ cột NOT NULL. Hệ quả chấp nhận: popup ERP của công ty lấy về hiện giá làm tròn nghìn. ⚠️ 2-D phải chặn thêm route **lưu Hãng sản xuất ERP** (`Sale/ManufacturesController:274` xoá-ghi lại dòng của mọi hàng status 1 thuộc hãng) |
| K3 | `product_suppliers.company_id`: **toàn bộ dữ liệu cũ gán về Cty 1** (CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT) — user chốt, KHÔNG theo `products.company_id`. Đề xuất kỹ thuật (nêu lúc xin phép code): cột `NOT NULL DEFAULT 1` ⇒ dòng ERP `->suppliers()->sync()` ghi sau này cũng tự về Cty 1, không sinh dòng rỗng, không cần chờ 2-D |
| K4 | Mô hình nhánh: **nhánh chung `feat/chuyen-doi-hang-hoa`** (đã tạo + push 04/10, có P2d). Nhánh 2-A checkout từ nhánh chung, xong merge về nhánh chung |

✅ 4 migration lỡ chạy của nhánh cũ: chỉ có ở DB local ⇒ bỏ qua (user 04/10). Plan: `plan.md`. 2-A không làm A5 (`product_company_units`) và không chép 4 cột quản trị (vì K1 không sinh dòng).
