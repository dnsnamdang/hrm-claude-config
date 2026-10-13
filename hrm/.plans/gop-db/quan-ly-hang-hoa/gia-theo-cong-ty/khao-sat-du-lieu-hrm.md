# Giá theo công ty (Hướng B) — Khảo sát dữ liệu + HRM (09/10/2026)

> Khảo sát CHỈ ĐỌC: không sửa source, DB chỉ SELECT (mysql CLI, `hrm_erp` — bản chụp ERP mới nhất 15/09/2026), không artisan,
> không checkout/stash/commit.
> **HRM:** worktree `wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}`, nhánh `feat/chuyen-doi-hang-hoa`, HEAD api `a862fbeef`.
> **ERP:** worktree `wt-erp-2d1` (nhánh `feat/2d1-erp-khong-loi`, HEAD `b2f1761789`) — chỉ grep/đếm, số dòng ERP chi tiết xem
> `../2d-erp-khong-loi/khao-sat-c-gia.md` §2.2.
> **"6 tháng"** = 15/03 → 15/09/2026 (theo mốc bản chụp).
> **Bối cảnh:** user 09/10 đảo QC-2 (`../2d-erp-khong-loi/d2-ton.md`): bảng giá RIÊNG theo công ty làm TRƯỚC; Cập nhật giá + Duyệt giá
> dựng trên mô hình mới. Đã chốt 30/09: A4 Hướng B (`product_unit_prices.company_id` NOT NULL, dữ liệu cũ gán công ty tạo) + A5
> (`product_company_units`). Tiền đề #8: bỏ hệ số giá `product_company_coefficients.coefficient`.

---

## 0. Tóm tắt — phát hiện chính

1. 🔴 **Gán "dữ liệu cũ = công ty tạo" (A4 nguyên văn) làm 4 công ty mất giá ngay ngày bật.** Trong 6 tháng, các công ty bán
   rất nhiều hàng do công ty KHÁC tạo (đo hợp nhất HĐ bán + phiếu xuất + báo giá ERP + báo giá HRM, mục 2.2):
   **Cty 4 SG 4.979 mã · Cty 3 Vinh 1.884 · Cty 8 ETEK 566 · Cty 2 HP 414 · Cty 1 TPE 174** (hàng chủ Cty 4).
   Cty 2 và Cty 8 **100%** hàng bán là hàng của công ty khác. Con số "7/8 công ty không có dòng giá" ở §25e đúng nhưng chưa nói
   hết: 4 trong 7 công ty đó đang bán hàng hằng ngày.
2. 🔴 **Hôm nay giá "chung" thực chất đã do nhiều công ty cùng ghi.** Phiếu tính giá ERP của **Cty 4 đã định giá 984 mã chủ Cty 1**
   (6 tháng), Cty 3: 118 mã, Cty 8: 9, Cty 2: 2 — ghi thẳng vào bảng chung (PTG không có cổng "chủ hàng"). Gán dòng giá cũ cho
   công ty tạo nghĩa là giá Cty 4 vừa tính trở thành giá của Cty 1. ⇒ câu **G3**.
3. 🔴 **Thêm `company_id` vào `product_unit_prices` mà quên lọc ở 1 chỗ đọc = nhân dòng im lặng.** Gần như mọi chỗ đọc (ERP lẫn
   HRM) nối `product_units → product_unit_prices` chỉ kẹp `price_type_id` (vd `BorrowExportRequestService.php:370-376`,
   `WrQuotationService.php:94-100`, popup ERP `SearchController`). Khi có 2+ công ty cùng 1 ĐVT, các truy vấn này trả N dòng/ĐVT,
   hoặc `first()`/`firstOrFail()` lấy bừa giá của công ty nào đó. Không lỗi, không cảnh báo. Đây là rủi ro lớn nhất của Hướng B.
4. **`product_units` tách đúng 13 cột "giá" + 6 cột cấu trúc** (đo mục 1.2). Ngoài 3 cột §25c đã nêu, còn `according_base_price`
   (cờ "Tính theo giá niêm yết", 141 ĐVT) và **8 cột chờ duyệt/ghi chú duyệt** — đều phải theo công ty.
5. **HRM có 3 cách hiểu "công ty để tính giá"** cùng lúc: công ty ghi trên chứng từ (Assign — `CompanyHelper::pricingCompanyId`),
   công ty hồ sơ người dùng `auth()->user()->info->company_id` (Finance, CustomerCare, và ERP `getData`), công ty đang làm việc
   `current_company_role` (MasterData). Với hệ số thì lệch chỉ ra chênh 2–5%; với giá riêng thì lệch là ra **giá của công ty khác
   hoặc không có giá**. ⇒ câu **G8**.
6. **HRM: 20 file / 37 điểm đọc–ghi** (mục 3). 4 helper `TpProductUnitPrice` gánh phần lớn Assign; Finance/CustomerCare nối bảng thô
   từng chỗ (11 điểm). FE (`hrm-client`) **không tự tính giá** — chỉ hiển thị số BE trả (grep công thức `/1000)*1000` + tên bảng: 0).
7. **Lấy hàng về (2-C2) hiện KHÔNG sinh giá** (`ProductWriteService::take` `:155-195` chỉ ghi `product_company_coefficients`).
   Tạo ĐVT mới (`writeUnits` `:322-339`) sinh 6 dòng giá 0 **không có công ty**. Gỡ hàng (`ProductLifecycleService::release`
   `:178-190`) không đụng giá. Cả 3 phải đổi (mục 4).
8. **Không cần backfill trạng thái trước nữa:** lý do 2-A không backfill dòng trạng thái (K1: "có dòng `pcc` = ERP nhân hệ số") hết
   hiệu lực khi bỏ hệ số ⇒ đợt giá là lúc gỡ được luật suy ra `@TODO-BACKFILL` (`Product.php:360-417`).

---

## 1. Mô hình dữ liệu đề xuất (Hướng B)

### 1.1 Hiện trạng (đo `SHOW CREATE TABLE`, 09/10)

```
products (45.890; company_id = công ty TẠO)
 └─< product_units 46.560          — KHÔNG company_id
      └─< product_unit_prices 264.646   — KHÔNG company_id; chỉ INDEX (product_unit_id, price_type_id), không UNIQUE (trùng: 0)
           └─< product_expected_prices 95.266 (unit_price_id)
 └─< product_company_coefficients 1.105 — UNIQUE(product_id, company_id), coefficient decimal(10,4) NOT NULL, status + 4 ô quản trị (2-A)
product_approves (company_id có sẵn) ─< product_approve_prices (product_unit_price_id, product_expected_price_id) — 0 dòng
```

Không bảng nào trong chuỗi giá có `company_id`; chưa có `product_company_units` (`SHOW TABLES LIKE 'product_company%'` = 1 bảng).

### 1.2 `product_units` — cột nào chung, cột nào theo công ty (đo 46.560 ĐVT)

| Cột | Đo | Bản chất | Đề xuất |
|---|---:|---|---|
| `id`, `product_id`, `unit_id`, `is_base`, `unit_coefficient`, timestamps | — | cấu trúc ĐVT | **CHUNG** (giữ) |
| `cost_price` (giá vốn, NOT NULL không default) | ≠0: **24.877** | giá | **theo công ty** |
| `buy_price` (giá mua ngoài) | not null 1.101 · ≠0 **1.091** | giá | theo công ty |
| `sale_max_percent_coefficient` ("Hệ số tính định mức hàng thúc đẩy bán", default 1) | ≠1: **23.503** | giá | theo công ty |
| `liquidation_sale_max_percent` ("ĐM đàm phán giá hàng thúc đẩy bán %") | ≠0: **5.678** | giá | theo công ty (F8: HRM không hiện; ERP L1 vẫn ghi — HĐ5) |
| `according_base_price` (cờ "Tính theo giá niêm yết", `products/form.blade.php:1058-1060`) | ≠0: **141** | cách tính giá | theo công ty |
| `price_wait_approve`, `coefficient_wait_approve`, `sale_max_percent_wait_approve`, `flag_price_wait_approve` | not null 12.168 · cờ>0 **24** | duyệt giá vốn | theo công ty |
| `approve_comment`, `approve_time`, `reason_edit_price`, `note_edit_price` | 31 · 47 · 324 · 0 | vết duyệt | theo công ty |

⇒ **6 cột chung, 13 cột sang `product_company_units`.** Theo chủ hàng: Cty 1 giữ 23.814 giá vốn ≠0, Cty 4 1.043, Cty 3 16, Cty 2 3.

### 1.3 Đề xuất — phương án B1 (khớp A4/A5)

**Bảng MỚI `product_company_units`** (lớp "giá theo công ty" của 1 ĐVT):

| Cột | Ghi chú |
|---|---|
| `id`, `product_unit_id` FK `product_units`, `company_id` FK `companies` | **UNIQUE(product_unit_id, company_id)** |
| `product_id` | dư thừa có chủ đích (lọc theo hàng × công ty không phải nối qua `product_units`); INDEX(company_id, product_id) |
| 13 cột ở mục 1.2 (cùng kiểu dữ liệu) | `cost_price` NOT NULL DEFAULT 0 (khác bảng cũ: có default) |
| `created_by`, `updated_by`, timestamps | `company_id` gán TAY (bài học 2-C2: không qua hook BaseModel) |

**`product_unit_prices` + `company_id`** (bigint unsigned, FK `companies`, INDEX):
- Bước 1: thêm NULLABLE → backfill → bước 2 `NOT NULL` + **UNIQUE(product_unit_id, company_id, price_type_id)** (thay INDEX
  `product_unit_prices_unit_price_type_index`). UNIQUE vừa chặn đua ghi vừa là chốt cho HĐ1 "1 dòng / loại giá" — nay theo công ty.

**`product_expected_prices`:** KHÔNG thêm cột (§25a — thừa hưởng qua `unit_price_id`). Cron 01:00 áp theo `unit_price_id` ⇒ tự đúng
công ty. Cờ `*_wait_approve`/`flag` ở đây và ở `product_unit_prices` tự thành "theo công ty" vì dòng đã thuộc công ty.

**Duyệt giá:** `product_approves.company_id` có sẵn (ERP ghi = công ty của chủ hàng `PriceCalculate.php:384`, phải đổi thành công ty
của bộ giá). `product_approve_prices.product_unit_price_id` trỏ dòng giá ⇒ theo công ty. Cờ duyệt cấp ĐVT (giá vốn) sang
`product_company_units`. `companies.is_company_price/brand_ids` đã là theo công ty ⇒ không đổi.

**`product_company_coefficients.coefficient`:** ngừng ĐỌC ngay khi bật giá theo công ty; **giữ cột** (NOT NULL, ERP cũ còn ghi ở
đường chưa chặn) — gỡ ở bước dọn cuối. Từ đây dòng `pcc` chỉ còn nghĩa "trạng thái + quản trị" ⇒ backfill được dòng trạng thái (mục 4.4).

**`product_units` 13 cột cũ:** ngừng đọc/ghi giá, **XOÁ ở bước cuối** sau khi rà xong ERP (như A4 "ép NOT NULL/xoá để cuối"). Trong lúc
chưa xoá, HRM vẫn phải ghi `cost_price = 0` khi INSERT ĐVT (NOT NULL không default, MySQL strict).

**Bất biến mới (thay HĐ1/HĐ2/G2):** *Mọi cặp (hàng × công ty) có trạng thái ≠ NULL đều có ĐỦ bộ giá: 1 dòng `product_company_units`
+ 6 dòng `product_unit_prices` cho MỖI ĐVT.* Sinh ở: tạo hàng (công ty tạo), lấy về (công ty lấy), thêm ĐVT (mọi công ty đang có
trạng thái), backfill. Xoá ở: xoá cứng hàng, gỡ hàng (công ty gỡ). Lý do: ERP `firstOrFail` ở `getPriceByUnitAndType`/`base_price`
(`app/Product.php:1431-1452`) và popup INNER lọc `price_type_id` — giữ được kiểu đọc "có dòng chắc chắn" thì sửa ERP chỉ là thêm 1
điều kiện `company_id`, không phải viết lại nhánh "không có giá". Lưu ý dữ liệu cũ không đủ 6 dòng (loại 5 thiếu ~14.349 ĐVT, loại 6
thiếu 365) — backfill bù luôn.

### 1.4 So sánh phương án thay thế

| | **B1 ⭐ thêm `company_id` vào bảng cũ + `product_company_units`** | B2 Bảng giá MỚI song song (`product_company_unit_prices`, `..._expected_prices`, `product_company_units`), bảng cũ đóng băng | B3 Lai: chủ dùng bảng cũ, công ty khác dùng bảng mới | B1' như B1 nhưng `product_unit_prices.company_unit_id → product_company_units.id` thay `company_id` |
|---|---|---|---|---|
| Khớp chốt A4/A5 | ✅ | lệch (A4 ghi `product_unit_prices.company_id`) | lệch | gần (ý giống, khoá khác) |
| Đọc ERP/HRM phải sửa | mọi chỗ đọc (34 file ERP + 20 file HRM) | mọi chỗ đọc (như B1) + cron 01:00 + PTG + duyệt | chỉ chỗ đọc cho công ty KHÁC chủ — nhưng chỗ nào cũng phải rẽ 2 nhánh | như B1 |
| Chỗ sót thì sao | 🔴 nhân dòng / giá bừa công ty, im lặng | 🟡 đọc ra **giá cũ đóng băng** — sai nhưng ổn định, dễ đối soát | 🔴 công ty khác đọc ra giá chủ | 🔴 như B1 |
| Rollback | khó (đã ép NOT NULL + đổi UNIQUE) | dễ: đọc lại bảng cũ | trung bình | khó |
| Nguồn sự thật | 1 | **2** trong thời gian chuyển (ai sửa bảng cũ là lệch) | 2 vĩnh viễn, bất đối xứng; N2 (màn Hãng SX ghi đè `products.company_id`) làm giá "lạc chủ" | 1 |
| Khoá `product_approve_prices`, `product_expected_prices` | giữ nguyên | phải trỏ bảng mới ⇒ đổi cả cron + PTG ERP | 2 kiểu | giữ nguyên |
| Dữ liệu | 264.646 dòng + phần chép (mục 2) | chép toàn bộ sang bảng mới | ít nhất | như B1 |

⇒ **Giữ B1** (đúng chốt, 1 nguồn sự thật). Bù rủi ro "sót chỗ đọc" bằng: (a) danh sách đọc đầy đủ + mốc grep (`@TODO-GIACTY`) cho
từng chỗ; (b) **chặn bằng UNIQUE + kiểm số dòng**: test PHPUnit sinh 2 công ty cùng giá khác nhau cho 1 ĐVT rồi gọi từng helper đọc,
khẳng định đúng giá + đúng số dòng; (c) bật theo trình tự cột NULLABLE → code đọc có lọc → backfill công ty thứ 2 → NOT NULL.
B1' gọn hơn về mô hình (giá không thể "lạc" khỏi lớp công ty) nhưng mọi truy vấn phải nối thêm 1 bảng — không đáng.

---

## 2. Backfill

### 2.1 Phân bố theo công ty tạo (`products.company_id`)

| Chủ | Mã | ĐVT | Dòng giá | Giá ≠ 0 | Giá hiệu lực (st 1 / st 2 / st 2 tương lai) |
|---|---:|---:|---:|---:|---|
| 1 TPE | 44.815 | 45.477 | **258.270** | 111.903 | 78.176 / 15.684 / 2.022 |
| 4 SG | 1.056 | 1.056 | 6.215 | 5.132 | 1.121 / 285 / 32 |
| 3 Vinh | 14 | 23 | 138 | 92 | — |
| 2 HP | 3 | 3 | 18 | 11 | — |
| *(NULL)* | 1 (`SG-PSS180103`, id 9964, `status = 0`, 2020) | 1 | 5 | 4 | — |
| 5, 6, 7, 8 | 0 | 0 | 0 | — | — |

- Mồ côi: `product_units`/`product_unit_prices`/`product_expected_prices` mồ côi **0/0/0**; hàng không công ty **1** (đã xoá ERP —
  gán Cty 4 theo tiền tố `SG-`, hoặc chỉ cần đặt NOT NULL sau khi gán; không ảnh hưởng nghiệp vụ); hàng không ĐVT **1** (`TPE-BNKN1`,
  status 0).
- ⚠️ 13.662 dòng giá hiệu lực `status = 2` nhưng `effect_date` đã qua (cron bỏ qua vì `flag`/lỗi cũ) — chép thì chép nguyên, không xử lý
  trong đợt này.

### 2.2 Công ty khác ĐANG dùng hàng của chủ khác (đo 6 tháng)

Nguồn "đang bán": hợp nhất `firm_contracts`×`firm_contract_tab_products` (HĐ bán) · `product_exports`×`product_export_details`
(phiếu xuất) · `firm_quotations`×`firm_quotation_tab_products` (báo giá ERP) · `quotations`×`quotation_product_prices.erp_product_id`
(báo giá HRM), theo `company_id` chứng từ, `created_at ≥ 15/03/2026`. Cộng thêm cặp có dòng `pcc` (hệ số) ở công ty khác chủ.

| Công ty | Mã đã bán (mọi chủ) | Trong đó của công ty khác | …còn `products.status = 1` | có dòng `pcc` | `pcc` ≠ 1 |
|---|---:|---:|---:|---:|---:|
| 1 TPE | 10.184 | **174** (chủ Cty 4) | 174 | 0 | 0 |
| 2 HP | 414 | **414** | 413 | 126 | 67 |
| 3 Vinh | 1.897 | **1.884** | 1.865 | 117 | 76 |
| 4 SG | 5.499 | **4.979** | 4.902 | 13 | 8 |
| 8 ETEK | 566 | **566** | 562 | 0 | 0 |
| 5, 6, 7 | 0 | 0 | — | — | — |

Theo từng nguồn (mã của công ty khác): HĐ — Cty 2 198, Cty 3 999, Cty 4 1.546, Cty 8 165, Cty 1 32 · Phiếu xuất — 181 / 665 / 1.827 / 174 / 24 ·
Báo giá ERP — 401 / 1.827 / 4.418 / 561 / 154.

**Tập "cần giá ngày bật" = đã bán 6 tháng ∪ có dòng `pcc`, trừ công ty chủ:**

| Công ty | Cặp hàng×công ty | …status 1 | ĐVT | Dòng giá cần chép | Giá ≠ 0 | Giá HL tương lai | ĐVT có giá vốn ≠0 | Giá đổi nếu nhân hệ số | Giá lẻ nghìn (không `pcc`) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 174 | 174 | 183 | 1.093 | 982 | 11 | 177 | 0 | 250 |
| 2 | 826 | 685 | 1.027 | 5.964 | 4.049 | 36 | 827 | 1.954 | 351 |
| 3 | 2.283 | 2.130 | 2.564 | 15.127 | 11.278 | 213 | 2.297 | 1.914 | 1.823 |
| 4 | 5.012 | 4.912 | 5.154 | 30.323 | 23.513 | 908 | 4.612 | 124 | 3.547 |
| 8 | 566 | 562 | 680 | 4.069 | 3.097 | 45 | 672 | 0 | 942 |
| **Tổng** | **8.861** | 8.463 | 9.608 | **56.576** | 42.919 | 1.213 | 8.585 | 3.992 | 6.913 |

Tổng 5.908 mã khác nhau. Có tồn kho (bất kỳ kho): Cty 1 91 · Cty 2 544 · Cty 3 1.750 · Cty 4 3.582 · Cty 8 541 mã.

### 2.3 Phương án sinh giá ban đầu cho công ty không phải chủ

| Phương án | Dòng thêm | Ngày bật | Hệ quả |
|---|---:|---|---|
| **P1 ⭐ Chép "đúng con số ERP đang hiện" cho tập 2.2** — có `pcc` ⇒ `ROUND(giá × hệ số / 1000) × 1000` (giá + giá hiệu lực tương lai); không `pcc` ⇒ chép nguyên; giá vốn/giá mua ngoài/13 cột chép nguyên của chủ | ~56.576 giá + 9.608 `pcu` + ~1.213 giá HL | người bán **không thấy gì đổi** | đóng băng luôn chênh 2–5% của HP/Vinh vào bộ giá riêng; giá vốn công ty khác = giá vốn chủ (sai bản chất nhưng y hôm nay); hàng bán lẻ tẻ trước 15/03 không có giá ⇒ phải nhập/lấy về lại |
| P2 Chép nguyên (bỏ hệ số) cho tập 2.2 | như P1 | **3.992 dòng giá của HP/Vinh/SG giảm** về giá TPE | đơn giản, nhưng đổi giá thật của chi nhánh ngày bật |
| P3 Chép cho **mọi hàng × 8 công ty** | ~1,85 triệu dòng giá (264.646 × 7) + ~326k `pcu` | không ai mất giá | bảng ×8; "giá" của công ty chưa từng bán hàng đó là giá giả — trái §26 (công ty lấy về **tự tính giá**) và vô nghĩa với trạng thái theo công ty |
| P4 Để trống (A4 nguyên văn) | 0 | **8.861 cặp mất giá**: Cty 4 5.012 · Vinh 2.283 · HP 826 · ETEK 566 · TPE 174 | phải nhập ~42.919 giá ≠ 0 trước ngày bật, không thì chứng từ của 5 công ty dừng |

Kèm theo P1/P2: sinh **dòng trạng thái `pcc` status 3 (Đang kinh doanh)** cho các cặp được chép (đang bán thật ⇒ đúng trạng thái), giữ
dòng `pcc` cũ (UPDATE `status`, không đụng `coefficient`) — xem mục 4.4.

---

## 3. HRM đọc/ghi giá — danh sách đầy đủ

Ký hiệu công ty: **CT** = công ty ghi trên chứng từ · **HS** = `auth()->user()->info->company_id` (hồ sơ NV) · **LV** =
`current_company_role` (công ty đang làm việc) · **—** = không theo công ty (đọc thẳng giá chung). Mức sửa: **S** nhỏ (thêm 1
điều kiện) · **M** vừa (đổi tham số/chữ ký) · **L** viết lại.

### 3.1 Helper dùng chung (`Modules/Human/Entities`)

| # | File:dòng | Đọc | Công ty hiện tại | Mức |
|---|---|---|---|---|
| H1 | `TpProductUnitPrice.php:29-60` `getRetailPrices` (mysql2) | giá loại X ĐVT cơ bản × hệ số | CT (tham số `$companyId`, NULL ⇒ giá gốc) | **M**: lọc `pup.company_id`, bỏ hệ số; NULL ⇒ phải có công ty (không còn "giá gốc") |
| H2 | `:69-91` `getCostPrices` | `pu.cost_price` ĐVT cơ bản | — | **M**: thêm `$companyId`, đọc `product_company_units` |
| H3 | `:100-122` `getBaseUnitIds` | `pu.unit_id` | — | không đổi |
| H4 | `:129-174` `getUnitOptions` | mọi ĐVT + giá loại X + `pu.cost_price` | CT (tham số, có thể NULL) | **M**: LEFT JOIN `pup` + `pcu` kẹp công ty |
| H5 | `:181-218` `getUnitPrice` | giá vốn + giá loại X theo ĐVT | **— (và KHÔNG nhân hệ số — lệch với H1/H4 ngay hôm nay)** | **M**: thêm `$companyId` |
| H6 | `TpProductCompanyCoefficient.php:39-79` | `pcc.coefficient`, công thức làm tròn | CT | **gỡ** (tiền đề #8) |

### 3.2 Assign (báo giá, BOM)

| # | File:dòng | Gọi | Công ty | Mức |
|---|---|---|---|---|
| A1 | `Http/Controllers/Api/V1/BomListController.php:405-410`, `:486-490`, `:563-567` | H1 (CT) + H2 (—) | CT = `CompanyHelper::pricingCompanyId` (`app/Helpers/CompanyHelper.php:52-59`: chứng từ, fallback HS) | S (truyền công ty vào H2) |
| A2 | `QuotationController.php:978-981` | H4 | CT | S |
| A3 | `Services/QuotationService.php:961`, `:1241`, `:1690`, `:2297`, `:2930`, `:3431` | H4 | CT (`$quotation->company_id`) | S |
| A4 | `QuotationService.php:2763` | H5 | **—** | S (truyền CT) |
| A5 | `QuotationService.php:2850-2851` | H2 (—) + H1 (CT) | lệch nhau | S |
| A6 | `QuotationService.php:5194-5202` `calculateValidityDate` + `:5210-5235` `getErpPriceChangeDates` (route `Routes/api.php:607`) | `product_expected_prices` tương lai | **—** (lấy ngày gần nhất của MỌI công ty) | S: kẹp `pup.company_id` = CT |
| A7 | `QuotationImportService.php:951` | H4 | CT | S |
| A8 | `BomListService.php:2528`, `Transformers/BomListResource/DetailBomListResource.php:38` | H4 không công ty — chỉ dùng ĐVT | — | không đổi (nhưng sau đổi H4 nhân dòng nếu không kẹp ⇒ phải đảm bảo H4 luôn kẹp) |
| A9 | `ErpProductSearchService.php:43` → ERP `Api/HrmProductSearchController.php:86` → `SearchController::searchProductStockBuyerApi` | giá do ERP tính (popup + hệ số) | CT gửi `company_id` | phía **ERP** (popup); HRM `:96` H2 S |

### 3.3 Finance (kho, chuyển hàng, mượn)

| # | File:dòng | Đọc | Công ty | Mức |
|---|---|---|---|---|
| F1 | `Services/ProductImportRequestService.php:1447-1470` `productUnits` (route ×2: nhập hàng + giữ hàng `ProductPrepickRequestController.php:178-180`) | 6 giá mọi ĐVT × hệ số | **HS** | S |
| F2 | `ProductTransferRequestService.php:522-540` (lúc lưu) | giá loại 1 thô | **—** (docblock `:481-488`: cố ý không hệ số) | S + câu G8 |
| F3 | `ProductTransferRequestService.php:984-1000` `productUnits` | 6 giá × hệ số | HS (`currentCompanyId :1141-1146`) | S |
| F4 | `BorrowSellRequest/BorrowSellRequestService.php:446-470` (so giá HĐ khi xuất) + `:485-505` `priceByUnitAndType` | giá loại HĐ × hệ số | HS (hệ số) / — (giá) | S — ⚠️ đổi nguồn giá là đổi kết quả "Sản phẩm có sự thay đổi về giá. Không thể xuất!" |
| F5 | `BorrowExportRequestService.php:370-376` `unitsOfProducts`, `:606-612` | giá loại 1 thô | — | S |
| F6 | `PrepickApprovalRouteService.php:233-241` `basePrice` (ngưỡng duyệt giữ hàng) | giá lẻ ĐVT cơ bản | — | S |

### 3.4 CustomerCare

| # | File:dòng | Đọc | Công ty | Mức |
|---|---|---|---|---|
| C1 | `Services/ServiceService.php:1044-1060` (chọn vật tư cho dịch vụ) | giá lẻ + `sale_max_percent` + `pcc` | HS | S |
| C2 | `WrServiceQuotationService.php:597-605`, `:862-866` | giá loại 1 thô | — | S |
| C3 | `WrQuotationService.php:94-100` | giá loại 1 thô | — | S |

### 3.5 MasterData (luồng hàng hoá — GHI)

| # | File:dòng | Việc | Mức |
|---|---|---|---|
| M1 | `Services/Product/ProductWriteService.php:322-339` `writeUnits` | INSERT ĐVT `cost_price/buy_price = 0` + 6 dòng giá 0, **không công ty** | **M**: sinh bộ giá (6 dòng + 1 `pcu`) cho MỖI công ty đang có trạng thái của hàng |
| M2 | `ProductWriteService.php:155-195` `take` (lấy về) | chỉ `pcc` | **M**: sinh bộ giá công ty lấy về (mục 4.2) |
| M3 | `ProductWriteService.php:556-568` sửa tab Quản trị (sinh dòng `pcc` coef 1) | dòng trạng thái | S: bỏ ràng buộc "dòng = hệ số" khỏi chú thích/luật D1 |
| M4 | `ProductLifecycleService.php:124-131` xoá cứng | xoá giá dự kiến → giá → ĐVT (mọi công ty) | không đổi + thêm xoá `product_company_units` |
| M5 | `ProductLifecycleService.php:178-190` `release` (gỡ) | không đụng giá | **M**: xoá bộ giá + `pcu` của công ty gỡ (kèm giá hiệu lực, `product_approves` của công ty đó) |
| M6 | `ProductLifecycleService.php:162-166` | xoá `product_approves` | không đổi |
| M7 | `Entities/Product/Product.php:360-417` `companyStatusSql`/`ownerStatusSql` (`@TODO-BACKFILL`) | suy trạng thái | gỡ nhánh CASE sau khi backfill trạng thái (mục 4.4) |
| M8 | `Entities/Product/ProductUnit.php:24-35` fillable 13 cột giá · `ProductUnitPrice.php:22` fillable thiếu `company_id` · `ProductCompany.php:43,77` `NEUTRAL_COEFFICIENT` | model | S |
| M9 | `Services/Product/ProductService.php:169`, `Transformers/Product/AdminData.php:46` | đọc `pcc` (trạng thái/quản trị, không hệ số) | không đổi |
| M10 | `database/e2e_provision.php`, seeder `BackfillQuotationProductUnitIdSeeder` | dữ liệu test | S |

### 3.6 FE `hrm-client`

Không tính giá: không có công thức hệ số/làm tròn nghìn, không đọc bảng giá. `pages/assign/quotations/_id/edit.vue` + 16 file khác chỉ hiển
thị `retail_price`/`cost_price` BE trả. `components/product/detail/ProductTabAdmin.vue:47-52` hiện `tech_coefficient` (không phải hệ số giá).
⇒ FE chỉ đổi khi làm màn giá mới (2-D2).

**Tổng:** 20 file HRM / 37 điểm (6 helper, 15 Assign, 9 Finance, 4 CustomerCare, 10 MasterData — trùng lặp đã gộp). Không điểm nào
cần L; rủi ro nằm ở việc **sót**, không ở độ khó.

### 3.7 ERP (đối chiếu, chi tiết ở khảo sát C §2.2)

`product_unit_prices`/`ProductUnitPrice` **44 file**, `product_expected_prices` **25**, hệ số **21** (grep `app` + `resources/views` của
`wt-erp-2d1`; §25b đếm 34 sau khi loại `product_templates`/`product_infos`). Điểm nóng: `Product::getDataAttribute` `app/Product.php:1242-1260`
(hệ số theo **HS**), `getUnitsInfoAttribute :1404-1419` (quan hệ `prices` không kẹp công ty), `getBasePriceAttribute :1431-1439` +
`getPriceByUnitAndType :1441-1452` (`firstOrFail`), popup `SearchController` (CASE hệ số). **Đường ghi ERP còn sống phải biết công ty:**
Phiếu tính giá `PriceCalculate::updatePriceWithApproval` (Phase 7), duyệt hàng tạm `Product::createRecord` (Phase 6), cron 01:00 (tự đúng
qua `unit_price_id`), cron 14:30 N5 (đưa giá về 0 theo tồn — phải theo công ty), `manualUpdatePrices`.

---

## 4. Tương tác với luồng đã làm

### 4.1 Trạng thái theo công ty

- Màn giá (D2 đã chốt): chỉ hàng **Đang kinh doanh (3) ở công ty user** ⇒ với bộ giá riêng, "sửa được" = có trạng thái 3 tại công ty mình;
  **luật QC-4 (hãng SX + chủ = công ty đang làm) hết lý do tồn tại** — nó sinh ra để chặn công ty khác sửa giá chung. ⇒ câu G4.
- QC-5 (không nhập giá hàng *Đang nhập thông tin*) và D3 (khoá *Chờ tính giá*/*Ngừng KD*) giữ nguyên, áp theo trạng thái công ty mình.
- Duyệt giá (D1): Duyệt/Không duyệt đổi `products.status` (2→1/5) — `products.status` là của CHỦ, giá là của công ty ⇒ công ty B bị Không
  duyệt giá thì không được đổi `products.status` của hàng chủ A. Cần soát lại D1 theo mô hình mới (đề xuất: chỉ đổi khi công ty duyệt = chủ).

### 4.2 Lấy hàng về (2-C2)

Hôm nay `take` không sinh giá ⇒ công ty B dùng giá chung (× hệ số nếu có). Hướng B: **sinh bộ giá RỖNG (6 dòng giá 0/ĐVT + `pcu` giá vốn 0)
cho công ty lấy về ngay lúc lấy** (bất biến 1.3). Không chép giá chủ (§26: công ty lấy về tự tính giá; §28: chính sách nội bộ chỉ là số
gợi ý, không ghi bảng giá). N53 đã ẩn hàng status 1/2 khỏi popup ERP ở công ty người dùng ⇒ giá 0 không lọt ra chứng từ. Mã đã có bộ giá
từ backfill (P1) thì không sinh lại (`insertOrIgnore` + UNIQUE).

### 4.3 G2 — 6 dòng giá 0/ĐVT

Đổi thành: mỗi ĐVT mới ⇒ cho MỖI công ty có dòng `pcc.status IS NOT NULL` của hàng (gồm chủ): 6 dòng `product_unit_prices` (giá 0, kèm
`company_id`) + 1 dòng `product_company_units` (giá vốn 0). `product_units.cost_price/buy_price = 0` vẫn ghi tới khi xoá cột. Vì C7 (ĐVT
đã lưu khoá), không có ca sửa/xoá ĐVT.

### 4.4 Backfill trạng thái + quy trình §26

- Khi bỏ hệ số, sinh dòng `pcc` không còn đổi giá ERP ⇒ **backfill luôn dòng trạng thái** (A3: hàng `products.status = 1` ⇒ dòng chủ
  status 3; P1 thêm dòng status 3 cho 8.861 cặp công ty khác) và gỡ nhánh suy ra `@TODO-BACKFILL` (M7). Dòng `pcc` cũ (1.105, `status`
  NULL, `created_by` NULL) chỉ UPDATE `status`, không xoá (V5/L1 còn dựa vào `created_by IS NULL`).
- §26: Công ty lấy về → *Đang nhập thông tin* → Chờ tính giá → (Phase 7) tính giá **vào bộ giá của chính công ty đó** → Đang kinh doanh.
  Trước Phase 7 (H1''), cặp mới lấy về có giá 0 và kẹt ở 1 — đúng như QC-5 đã chấp nhận.
- Chính sách giá nội bộ (§28) đọc giá vốn/6 giá **của công ty bán** = bộ giá của chủ hàng ⇒ cần `pcu`/`pup` kẹp công ty bán — khớp B1.

---

## 5. Câu hỏi nghiệp vụ (hỏi LẦN LƯỢT, theo thứ tự)

| # | Câu | ⭐ Đề xuất | Hệ quả từng đáp án |
|---|---|---|---|
| **G1** | Ngày bật, công ty KHÁC chủ đang bán hàng (8.861 cặp, mục 2.2) lấy giá ở đâu? | ⭐ **P1**: chép đúng con số ERP đang hiện (× hệ số làm tròn nghìn nếu có dòng hệ số, nguyên giá nếu không) cho tập "đã bán 6 tháng ∪ có dòng hệ số" | P1: ngày bật không ai thấy đổi; ~56,6k dòng giá. P2 chép nguyên: 3.992 giá của HP/Vinh/SG giảm về giá TPE. P3 nhân bản 8 công ty: ~1,85 triệu dòng, giá giả cho công ty chưa từng bán, trái §26. P4 để trống: 5 công ty (SG 5.012 · Vinh 2.283 · HP 826 · ETEK 566 · TPE 174 cặp) dừng chứng từ tới khi nhập ~42,9k giá |
| **G2** | Mốc "đang bán" để chép (nếu G1 = P1/P2)? | ⭐ **6 tháng** (15/03–15/09) + mọi cặp có dòng hệ số | 12 tháng: thêm cặp, ít ca "hàng lâu lâu mới bán bị mất giá". Chỉ hệ số: Cty 4/8 gần như không có gì (13/0 cặp) |
| **G3** | Dòng giá cũ (bảng chung) gán cho ai, biết PTG của Cty 4 đã định giá 984 mã chủ Cty 1 trong 6 tháng? | ⭐ **gán công ty tạo** (A4) — Cty 4 vẫn có bản sao qua G1 | Gán chủ: TPE nhận cả giá do SG tính cho hàng TPE; SG giữ bản sao y hệt. Gán theo "người định giá gần nhất": phải dò lịch sử PTG từng mã, mỗi mã một chủ khác nhau, không có ích hơn khi đã có bản sao |
| **G4** | Ai sửa được giá mã nào khi giá đã riêng? (thay QC-4) | ⭐ **Công ty nào sửa bộ giá của công ty đó** cho mọi hàng *Đang kinh doanh* tại công ty mình; bỏ điều kiện hãng SX + chủ | Theo ⭐: SG/Vinh/HP tự quản giá hàng TPE mình bán (đúng ý §26). Giữ QC-4: chi nhánh không sửa được giá của chính mình (chỉ TPE có hãng) — vô nghĩa với giá riêng |
| **G5** | Giá vốn/giá mua ngoài của công ty không phải chủ (chép ở G1, và công ty lấy về mới) | ⭐ Backfill **chép giá vốn chủ**; lấy về mới ⇒ **0, tự nhập** (lúc tính giá, tham khảo §28) | Chép: báo giá/BOM của SG… giữ lãi gộp như hôm nay (đang đọc giá vốn TPE). Để 0: lãi gộp trên báo giá công ty khác thành 100% tới khi nhập. Tính theo §28 (giá vốn chủ × (1+%)): chưa có bảng §28 nên chưa làm được |
| **G6** | Khi nào ngừng nhân hệ số giá? | ⭐ **Cùng lúc bật giá theo công ty** (hệ số đã đóng băng từ 2-D1, N35) | Cùng lúc: một lần đổi, P1 giữ được số. Giữ thêm một thời gian: phải đọc 2 nguồn (giá riêng × hệ số?) — dễ nhân đôi chênh |
| **G7** | Phiếu tính giá ERP (giữ tới Phase 7) và duyệt hàng tạm ERP (Phase 6) ghi giá vào bộ của công ty nào? | ⭐ PTG ghi vào **công ty lập phiếu** (`price_calculates.company_id`); hàng tạm ghi vào **công ty của hàng tạm** (+ sinh bộ giá cho công ty đó) | Theo ⭐: SG tính giá hàng TPE ⇒ chỉ đổi giá SG (đúng giá riêng). Ghi vào chủ: giữ hành vi cũ "SG sửa giá TPE" — trái giá riêng. Chặn PTG ERP tới Phase 7: 4.008 lần ghi/6 tháng dừng |
| **G8** | Giá trên chứng từ lấy theo công ty nào? | ⭐ **Công ty ghi trên chứng từ** (đã là quy ước Assign `pricingCompanyId`); Finance/CustomerCare + ERP `getData` đổi từ "công ty hồ sơ NV" sang công ty chứng từ | Theo ⭐: NV kiêm nhiệm lập chứng từ cho SG thấy giá SG. Giữ công ty hồ sơ: NV TPE lập phiếu cho SG ra giá TPE (hôm nay chỉ lệch 2–5% qua hệ số; với giá riêng lệch tuỳ ý hoặc không có giá) |
| **G9** | Duyệt giá (D1 đã chốt): Duyệt/Không duyệt có đổi `products.status` khi công ty duyệt KHÔNG phải chủ? | ⭐ **Chỉ công ty chủ** mới đổi `products.status` (2→1/5); công ty khác chỉ đổi cờ trên bộ giá của mình | Theo ⭐: SG không duyệt giá thì hàng TPE không biến mất ở TPE. Đổi cho mọi công ty: một chi nhánh từ chối giá làm hàng ngừng ở cả 8 công ty |
| **G10** | Cron 14:30 đưa giá về 0 khi hết tồn (N5, đang để sau) | ⭐ vẫn để sau, nhưng ghi rõ: khi làm thì **theo tồn + bộ giá của từng công ty** | Để nguyên ERP: cron reset giá theo `products.company_id` ⇒ chỉ đụng bộ giá chủ (sau khi sửa kẹp công ty) hoặc mọi công ty (nếu không kẹp) — phải chọn trước ngày bật |

## 6. Điểm kỹ thuật tự quyết (không hỏi)

1. Phương án B1 (mục 1.3); không B2/B3/B1'.
2. 13 cột `product_units` sang `product_company_units` (mục 1.2); xoá cột cũ ở bước cuối; tới lúc đó HRM vẫn ghi `cost_price = 0` khi tạo ĐVT.
3. UNIQUE(product_unit_id, company_id, price_type_id) + UNIQUE(product_unit_id, company_id); migration 2 bước (NULLABLE → backfill → NOT NULL).
4. `product_expected_prices` không thêm cột; `product_approves.company_id` = công ty của bộ giá.
5. Bất biến "có trạng thái ⇒ đủ bộ giá"; lấy về sinh bộ giá rỗng; gỡ hàng xoá bộ giá công ty gỡ; thêm ĐVT sinh cho mọi công ty có trạng thái.
6. Backfill bù luôn dòng loại 5/6 còn thiếu (~14.349 / 365 ĐVT) cho mọi công ty được backfill; hàng NULL công ty (id 9964, đã xoá) gán Cty 4.
7. Backfill trạng thái `pcc` cùng đợt; gỡ `@TODO-BACKFILL`; dòng `pcc` cũ chỉ UPDATE `status`.
8. Helper đọc HRM bắt buộc tham số công ty (không còn "NULL = giá gốc"); gom chỗ nối bảng thô ở Finance/CustomerCare về 1 service giá dùng chung
   (đã có ghi chú `ProductPrepickRequestController.php:174` đề xuất `ProductUnitPriceService`).
9. Mốc grep `@TODO-GIACTY` ở mọi điểm mục 3 + PHPUnit "2 công ty khác giá cùng ĐVT" cho từng helper (đo đúng giá + đúng số dòng).
10. Backfill chạy bằng lệnh artisan riêng, idempotent (`insertOrIgnore` theo UNIQUE), có `--dry-run` in số dòng theo công ty để so với bảng 2.2.
