# Đợt 2-C4 — Vòng đời (Xoá + Khoá/Mở khoá theo công ty): khảo sát BE (08/10/2026)

> CHỈ ĐỌC: không sửa source, không ghi DB. Code HRM = worktree `websites/wt-chuyen-doi-hang-hoa/hrm-api`
> nhánh `feat/chuyen-doi-hang-hoa` (HEAD `d3c6496a1` — đã có 2-C1, 2-C2, 2-C3); đường dẫn dưới đây tính từ
> `hrm-api/Modules/MasterData/` trừ khi ghi khác. ERP = `ERP/TanPhatDev` (nhánh `develop_01`).
> Số đo: DB local `hrm_erp` (chỉ SELECT), 08/10/2026.
> Luật ưu tiên: `chot.md` (G6, G7, G9a, B2/B3, L1–L7, N8) > `man-danh-muc-hang-hoa/design.md` §35b-4 > `yeu-cau-ghi.md` §1.4/§1.9 > mockup.

---

## 0. Tóm tắt

| # | Kết luận |
|---|---|
| 1 | ERP `canDelete()` (`app/Product.php:7215-7255`) = 1 điều kiện công ty + 4 điều kiện dữ liệu (tồn, mượn chưa trả, là phụ kiện, là thành phần công thức). ERP **không** xoá cứng (`status = 0`). 4 điều kiện dữ liệu đều là **tập con** của "có dòng ở bảng FK trỏ vào `products`" — đo: mọi hàng không vướng FK đều qua 4 điều kiện ERP |
| 2 | **172 FK / 165 bảng** trỏ `products`, **100 % `NO ACTION`/`RESTRICT`** (0 CASCADE, 0 SET NULL) ⇒ xoá cứng phải xoá bảng con theo đúng thứ tự, và FK là chốt chặn cuối thật. NHƯNG còn **183 cột `product_id`/`base_product_id` KHÔNG có FK** (139 cột sau khi loại bảng template/info/tmp/bak) — ~50 bảng trong đó HRM có code ghi (serials, prepick_details, wr_*, product_import_direct_details…) ⇒ FK **không đủ** làm định nghĩa "chưa phát sinh chứng từ" |
| 3 | Hàng **xoá được theo §35b-4 hiện = 0**: `product_company_coefficients` 1.105 dòng, **100 % `status` NULL** (dữ liệu thử 2-C1/2-C2 đã dọn). Chỉ hàng HRM tạo (dòng chủ `status = 1`) mới thoả *Đang nhập thông tin*; 28.371 hàng ERP cũ đều suy ra 3 ⇒ không xoá được. (Tham khảo: 18.345/28.371 hàng hoạt động qua `canDelete` ERP, nhưng 9.043 trong đó bị FK chặn xoá cứng; chỉ 9.302 sạch FK) |
| 4 | "Công ty tạo xoá" vs "công ty lấy về gỡ" phân biệt được bằng `products.company_id = current_company_role`. Dòng ERP (hệ số cũ) vs dòng HRM sinh phân biệt được bằng **`created_by IS NULL`** (ERP model `ProductCompanyCoefficient extends Model` không gán `created_by` — 1.105/1.105 dòng hiện có NULL; HRM luôn gán) — `coefficient = 1` KHÔNG dùng được (258 dòng ERP có hệ số 1.0000) |
| 5 | Khoá G6: nền đọc đã xét status 4 đúng ở **9/10 chỗ** (màn Đang KD, đếm chưa xếp catalog, Nhập thông tin, Kho, can_edit, can_take_back, L3 owner_not_trading, popup catalog B3 cả list lẫn sync). Lệch: (a) 2-C1/2-C2 trả **403** cho hàng Ngừng KD, CLAUDE.md HRM + G6 đòi **423**; (b) lỗi có sẵn ở `tradingCompanyNames()` — 4 hàng của Cty 4 có dòng chủ hệ số cũ bị thiếu công ty tạo ở cột *Công ty đang kinh doanh* (N18) |
| 6 | Quyền: dùng **1652** cho cả Xoá (§35b-4 đã chốt) và Khoá/Mở khoá (G6 mặc định) ⇒ **không seeder**. Seeder nhánh: 0 id trùng (bỏ dòng comment); 1652/1653/1655 có trong DB; id trống gần nhất nếu cần quyền mới: 1657–1659, 1662–1669, 1679+ (1654/1656 đã giữ) |
| 7 | Ảnh/tệp S3: **147** URL ảnh mô tả và **5.556** giá trị `avatar` đang dùng chung giữa nhiều hàng; `TableFileHelper::deleteByIds` HRM và ERP đều không xoá S3 ⇒ đề xuất KHÔNG xoá S3 |
| 8 | 7 câu hỏi nghiệp vụ (mục 9) — chủ yếu xác nhận "mặc định đề xuất" của G6 và điều kiện gỡ của công ty lấy về |

---

## 1. ERP: xoá / khoá hàng hoá

### 1.1 `canDelete()` — `ERP/TanPhatDev/app/Product.php:7215-7255`

| # | Điều kiện (chặn khi…) | Dòng | Thông báo ERP |
|---|---|---|---|
| 1 | `Auth::user()->info->company_id != products.company_id` | :7218 | "Hàng không thuộc công ty" |
| 2 | `stocks.accounting_qty > 0` | :7224 | "Hàng có tồn kho!" |
| 3 | `product_export_request_details` ⨝ `product_export_requests.type = 3`, `base_exported_qty > borrow_returned_qty` | :7230-7235 | "Hàng đang mượn chưa trả hết!" |
| 4 | `product_has_accessories.product_id = id` (hàng là phụ kiện của hàng khác) | :7241 | "Hàng nằm trong danh sách phụ kiện!" |
| 5 | `recipe_products.product_id = id` (hàng là thành phần công thức ghép bộ) | :7247 | "Hàng nằm trong công thức ghép bộ!" |

Không kiểm: phụ kiện lắp đặt / sửa chữa (`product_has_install_accessories`, `product_has_repair_accessories` cột `product_id`), "máy dùng cho" (`productables` loại `App\Product` trỏ ngược), chứng từ bán/mua/kho khác.

### 1.2 Đường gọi

| Route `routes/web.php` | Controller `app/Http/Controllers/ProductsController.php` | Ghi |
|---|---|---|
| `GET products/{id}/delete` :580 (quyền ERP *Xóa hàng hóa*) | `delete` :1999 | `canDelete` → `status = 0`, `deleted_at = now()` |
| `POST products/bulkDelete` :581 | `bulkDelete` :4588 | `canDelete` từng hàng, 1 hàng hỏng ⇒ cả lô không xoá; `status = 0`, **không** gán `deleted_at` |
| `GET products/{id}/restore` :606 | `restore` :2020 | `status = 1`, để nguyên `deleted_at` |
| Khoá | — | **không có**; `STATUSES` đặt `KHOA = 0` trùng "đã xoá" (`erp-ghi-hang-hoa.md` §4) |

⇒ ERP: xoá = khoá = `status 0` toàn cục, không đụng bảng con. HRM 2-C4 khác hẳn: xoá **cứng** (G7) và khoá **theo công ty** (G6).

### 1.3 §35b-4 (`man-danh-muc-hang-hoa/design.md:3199`)

> Có xoá, chỉ hàng chưa dùng, theo quyền **Xây dựng thông tin hàng hoá** (không thêm quyền): xoá được khi hàng ở *Đang nhập thông tin*, **do công ty mình tạo**, **chưa công ty nào lấy về**, **chưa phát sinh chứng từ**. Hàng công ty khác đã lấy về thì *xoá* = gỡ dòng của công ty mình ở `product_company_coefficients`, không đụng `products`.

---

## 2. Đề xuất hàm kiểm "xoá được" ở HRM

### 2.1 Điều kiện (thứ tự xét — 403/423 TRƯỚC 422 như R6 của 2-C1)

| # | Điều kiện | Mã | Nguồn |
|---|---|---|---|
| a | Quyền 1652 tại công ty đang làm việc (`assertCanWrite`, R22) | 403 | §35b-4 |
| b | Hàng tồn tại | 404 | |
| c | `products.status = 1` | 403 | D2 |
| d | Công ty mình có dùng: là chủ (`products.company_id = current_company_role`) HOẶC có dòng `status NOT NULL` | 403 | |
| e | Trạng thái tại công ty mình ≠ 4 | **423** | CLAUDE.md HRM :59-60 (bản ghi khoá không xoá) |
| f | Trạng thái tại công ty mình = 1 *Đang nhập thông tin* (chủ: dòng thật, KHÔNG suy ra — hàng ERP cũ suy ra 3 ⇒ chặn) | 422 | §35b-4 |
| — | **Nhánh CHỦ** (xoá cứng) | | |
| g | Không công ty nào khác có dòng `status NOT NULL` | 422 | §35b-4 "chưa công ty nào lấy về" |
| h | 4 điều kiện dữ liệu ERP (tồn kế toán > 0, mượn chưa trả, là phụ kiện, là thành phần công thức) — giữ đúng câu báo ERP | 422 | G7 |
| i | Mở rộng: là phụ kiện lắp đặt / sửa chữa của hàng khác; là "Máy dùng cho" của hàng khác (`productables` `productable_type = 'App\Product' AND productable_id = id` — không FK) | 422 | đề xuất, Q6 |
| j | Chưa phát sinh chứng từ: không có dòng ở **153 cột FK ngoài** (172 trừ 19 cột là bảng con của chính hàng — mục 3) **và** ở danh sách cột `product_id` không FK (mục 3.3) | 422 | §35b-4 |
| k | FK 1451 khi DELETE `products` (lọt lưới j) ⇒ rollback + 422 "Hàng hoá đã phát sinh chứng từ" | 422 | G7 "FK là chốt chặn cuối" |
| — | **Nhánh CÔNG TY LẤY VỀ** (gỡ) | | |
| l | Chỉ xét trạng thái của mình (Q4); KHÔNG kiểm chứng từ (gỡ không xoá `products`, chứng từ vẫn trỏ được) | | G7 |

Ghi chú điều kiện g: với luật hiện tại **không thể xảy ra** (L3: chỉ lấy về được khi công ty tạo = 3; chủ không lùi 3 → 1 — C2) — vẫn kiểm để phòng (vd phase Tính giá mở lại lấy về hàng đang nhập — N17).

### 2.2 Chi phí đo (1 mã)

| Cách kiểm | Thời gian |
|---|---|
| UNION ALL 153 cột FK ngoài (`LIMIT 1` mỗi bảng, có index FK) | 0,32–0,74 s |
| UNION ALL 139 cột không FK (169/183 cột **không index** `product_id`, ~2,59 triệu dòng phải quét) | 2,8 s (ấm) – 9,4 s (lạnh) |
| Quét toàn bảng `products` theo 153 FK (28k hàng) | 7,5 s |

⇒ Xoá từng mã chấp nhận được (người dùng bấm 1 lần, có spinner). Nếu làm hàng loạt: 1 câu UNION dùng `product_id IN (…)` cho cả lô (chi phí gần như không đổi theo số mã). Đề xuất: dựng **1 lớp `ProductUsageGuard`** chứa 2 danh sách cột (FK đọc từ `information_schema` lúc chạy hay hằng số? ⇒ đề xuất **hằng số trong code** + test so khớp với `information_schema` để phát hiện bảng FK mới).

### 2.3 Đề xuất hàm (tên tạm)

- `Product::deletableAt(int $companyId, ?int $companyStatus, Collection $companies): bool` — điều kiện rẻ c–g (dùng cho cờ `can_delete` ở list/chi tiết, KHÔNG gồm h–j vì tốn query).
- `ProductUsageGuard::reasons(array $ids): array` — h–j, trả lý do theo từng mã (câu báo ERP cho h).
- `ProductLifecycleService::destroy(Product)` — chia 2 nhánh `hardDelete` (chủ) / `release` (công ty lấy về).

⚠️ Theo CLAUDE.md "nút không dùng được thì ẩn hẳn": cờ `can_delete` chỉ tính được c–g; h–j (tồn kho, chứng từ) chỉ biết khi bấm ⇒ BE trả 422 kèm lý do. Với hàng HRM mới (status 1, giá 0) khả năng vướng h–j rất thấp — chấp nhận.

---

## 3. Bảng con phải xoá khi xoá cứng (nhánh chủ)

### 3.1 Đối chiếu với 2-C1 (`Services/Product/ProductWriteService.php`)

| Thứ tự xoá | Bảng | Khoá | 2-C1 ghi? | FK → products | Số dòng toàn bảng |
|---|---|---|---|---|---|
| 1 | `product_expected_prices` | `unit_price_id ∈` giá của ĐVT hàng | không (ERP ghi) | gián tiếp (FK → `product_unit_prices`) | 95.266 |
| 2 | `product_unit_prices` | `product_unit_id ∈` ĐVT hàng | ✅ 6 dòng/ĐVT (:333-338) | gián tiếp (FK → `product_units`) | 264.646 |
| 3 | `product_units` | `product_id` | ✅ (:328-332) | ✅ | 46.560 |
| 4 | `attribute_products` | `product_id` | ✅ (:343-354) | ✅ | 51.128 |
| 5 | `recipe_products` | `base_product_id` | ✅ (:362) | ✅ | 6.438 |
| 6 | `product_has_accessories` | `base_product_id` | ✅ | ✅ | 989 |
| 7 | `product_has_install_accessories` | `base_product_id` | ✅ | ✅ | 28 |
| 8 | `product_has_repair_accessories` | `base_product_id` | ✅ | ✅ | 5 |
| 9 | `files` | `table = 'product_tech_attachments' AND table_id ∈` | ✅ (:387-431) | không | 10 |
| 10 | `product_tech_attachments` | `product_id` | ✅ | ✅ | 35 |
| 11 | `product_galleries` | `product_id` | ✅ (:438-459) | ✅ | 1.548 |
| 12 | `product_videos` | `product_id` | ✅ (:461-471) | ✅ | 2 |
| 13 | `productables` (**5 loại, mọi `productable_type`**) | `product_id` | ✅ (:513-522) | **không** | 45.549 |
| 14 | `product_vehicle_model_has_life` | `product_id` | ✅ (:498-509) | **không** | 48.736 |
| 15 | `product_company_coefficients` (**mọi công ty**) | `product_id` | ✅ (:556-570) | ✅ | 1.105 |
| 16 | `product_suppliers` (**mọi công ty**) | `product_id` | ✅ (:572-578) | ✅ | 1.741 |
| 17 | `product_business_catalogs` (**mọi công ty**) | `product_id` | ✅ (:580-586) | ✅ | 0 |
| 18 | `product_barcodes`, `product_categories`, `product_prices`, `product_documents`, `product_features`, `product_histories`, `product_versions` | `product_id` | không (ERP ghi khi sửa ở ERP) | ✅ | 107 · 3.685 · 20.127 · 0 · 0 · 319.303 · 113.768 |
| 19 | `product_approves` (+ `product_approve_prices` theo cha) | `product_id` | không | **không** | 0 |
| 20 | `products` | `id` | ✅ | — | 45.890 |

Ghi chú:
- Bước 18–19: HRM không ghi nhưng hàng HRM tạo vẫn có thể bị **ERP sửa** (2-D chưa chặn route — N4) ⇒ sinh `product_histories`/`product_versions`/`product_barcodes`. Đề xuất xoá cùng (là dữ liệu CỦA hàng, không phải chứng từ); không xoá thì FK 1451 chặn ⇒ hàng không bao giờ xoá được.
- `productables` hướng ngược (`productable_type = 'App\Product' AND productable_id = id`) **không** thuộc hàng đang xoá — là dữ liệu của hàng khác: chặn (2.1-i) hoặc gỡ (Q6). Đo: 2.535 hàng đang là "Máy dùng cho" của hàng khác. Item-search 2-C1 (`Services/Product/ProductOptionService.php:134`) chỉ lọc `p.status = 1` ⇒ hàng HRM mới tạo chọn được làm máy/phụ kiện/công thức ngay.
- `product_templates`: hàng HRM tạo không có `product_template_id` (N6) ⇒ không đụng.
- Mọi lệnh xoá dùng `DB::table` kẹp khoá đúng (bẫy `productables` kẹp type: ở đây xoá **mọi** type của `product_id` là đúng vì xoá cả hàng — ghi chú rõ trong code để reviewer không "sửa").
- `Product` không dùng `SoftDeletes`, `BaseModel` không có hook `deleting` ⇒ `DB::table('products')->where('id')->delete()` hay `$product->delete()` đều là xoá cứng.

### 3.2 FK trỏ vào `products`

`information_schema.REFERENTIAL_CONSTRAINTS`: **172 FK / 165 bảng, DELETE_RULE: 172 NO ACTION/RESTRICT, 0 CASCADE, 0 SET NULL.** 19 cột thuộc bảng con của chính hàng (mục 3.1), **153 cột ngoài** = chứng từ/kho (stocks, accounting_stocks, contract_products, quotation_products, product_export_request_details, warehouse_*_lots…). FK con của bảng con: chỉ `product_unit_prices.product_unit_id → product_units`, `product_expected_prices.unit_price_id → product_unit_prices` (không chứng từ nào FK vào `product_units`).

Đo trên hàng hoạt động (`products.status = 1`, 28.371):

| Đo | Số |
|---|---:|
| Vướng ERP đk 2 (tồn > 0) | 8.031 |
| Vướng ERP đk 3 (mượn chưa trả) | 151 |
| Vướng ERP đk 4 (là phụ kiện) | 191 |
| Vướng ERP đk 5 (là thành phần công thức) | 2.503 |
| Qua 4 đk dữ liệu ERP | 18.345 |
| …và sạch 153 FK ngoài (xoá cứng được về mặt FK) | **9.302** |
| …nhưng FK chặn | 9.043 |
| Hàng `status = 0` sạch FK ngoài | 15.174 / 17.512 |

⇒ Không có hàng nào xoá được theo §35b-4 lúc này (0 dòng trạng thái); bảng trên chỉ để thấy FK chặn mạnh hơn ERP.

### 3.3 Cột `product_id` KHÔNG có FK (bẫy)

183 cột (`product_id`/`base_product_id`) không FK; loại bảng `product_template*`, `product_info*`, `recipe_product_(infos|templates)`, `tmp_product_*`, `*bak*`, `productables`, `product_vehicle_model_has_life`, `product_classifies`, `product_approves` còn **139 cột**; **169/183 không có index**. HRM có code đọc/ghi ~50 bảng trong số đó, vd: `serials` (10 file), `prepick_details` (11), `account_details` (25), `wr_service_contract_*`, `wr_service_quotation_*`, `product_import_direct_details`, `device_error_products`, `firm_contract_tab_products`, `product_export_request_tab_products`… ⇒ chỉ dựa FK sẽ để lại **dòng mồ côi im lặng** (vd phiếu bảo hành trỏ hàng đã xoá ⇒ màn đó văng "property of non-object"). Danh sách đầy đủ: chạy lại câu SQL ở phụ lục A.

---

## 4. "Công ty tạo xoá" vs "Công ty lấy về gỡ"

| | Công ty TẠO (`products.company_id = current_company_role`) | Công ty LẤY VỀ (không phải chủ, dòng mình `status NOT NULL`) |
|---|---|---|
| Điều kiện | 2.1 a–k | 2.1 a–e + trạng thái của mình (Q4) |
| Ghi | xoá cứng 20 bước mục 3.1 trong **1 transaction**, `lockForUpdate` dòng `products` + mọi dòng `product_company_coefficients` của hàng | **dòng ERP** (`created_by IS NULL` — hệ số cũ, L1): `UPDATE status = NULL` (+ 4 ô quản trị về NULL — Q5), **giữ `coefficient`**; **dòng HRM sinh** (`created_by NOT NULL`, lấy về chèn mới): `DELETE`. Kèm xoá `product_business_catalogs` + `product_suppliers` `where company_id = mình` (Q5). Không đụng `products` |
| Sau | hàng biến mất mọi màn; mã `code` được giải phóng (UNIQUE) — **mã có thể sinh lại cho hàng khác** (ERP không bao giờ giải phóng mã vì xoá mềm) | về "Chưa sử dụng" ở Kho, lấy về lại được (L1: dòng ERP ⇒ UPDATE lại status 1; dòng đã xoá ⇒ INSERT coef 1) |
| Ảnh hưởng giá ERP (K2) | không còn hàng | dòng HRM xoá ⇒ popup ERP của công ty đó **thôi làm tròn nghìn**; dòng ERP giữ ⇒ giá không đổi |

Công ty tạo xoá khi công ty khác đã lấy về ⇒ **chặn** (§35b-4, đk g) — không xoá dây chuyền dòng của công ty khác.

Phân biệt dòng ERP / dòng HRM:
- ERP ghi dòng qua `ProductCompanyCoefficient extends Model` (`app/Model/Product/ProductCompanyCoefficient.php:7`) ở `syncCompanyCoefficients` (`app/Product.php:6290-6300`) — **không gán `created_by`**. Đo: 1.105/1.105 dòng `created_by NULL` (2021-09-13 → 2026-08-26), 258 dòng hệ số 1.0000.
- HRM: `take()` INSERT có `created_by` (`ProductWriteService.php:181-185`), `writeAdmin` INSERT có `created_by` (:565-569); UPDATE dòng ERP (:178-179, :559-560) **không** gán `created_by` ⇒ dòng ERP giữ NULL ⇒ luật `created_by IS NULL` đứng vững.
- ⚠️ Lỗ hổng: màn Hãng SX ERP (N2) xoá-chèn lại mọi dòng của hàng thuộc hãng ⇒ dòng HRM thành dòng ERP (`created_by NULL`, `status NULL`) — đã mất trạng thái từ trước, không phát sinh lỗi mới.

S3 / tệp đính kèm:
- `product_galleries.url`, `products.avatar`, `product_videos.url` là URL; `files.file_path` cho tài liệu kỹ thuật.
- Đo dùng chung: **147** URL ảnh mô tả thuộc ≥ 2 hàng; **5.556** giá trị `avatar` lặp ở ≥ 2 hàng (ERP Sao chép giữ URL); `files` tài liệu kỹ thuật: 0 trùng.
- `App\Helper\TableFileHelper::deleteByIds` (`app/Helper/TableFileHelper.php:48-62`) chỉ xoá dòng `files`, không xoá S3; ERP không bao giờ xoá S3 (xoá mềm).
- ⇒ ⭐ chỉ xoá dòng DB, **không xoá đối tượng S3** (Q7). Hàng HRM chỉ có tệp tải lên riêng, nhưng Sao chép (G8, làm sau) sẽ dùng chung URL như ERP ⇒ xoá S3 bây giờ là cài bẫy cho G8.

---

## 5. Khoá / Mở khoá (G6)

### 5.1 Chuyển trạng thái đề xuất (G6 mặc định — Q1)

| Từ \ Thao tác | Khoá | Mở khoá |
|---|---|---|
| 1 Đang nhập thông tin | ✗ 422 (dùng Xoá) | — |
| 2 Chờ tính giá | ✗ 422 (chưa có hàng nào — H1') | — |
| 3 Đang kinh doanh (dòng thật) | `UPDATE status = 4` | — |
| 3 suy ra (chủ, chưa có dòng — 28.371 hàng cũ) | `INSERT coefficient = 1, status = 4, created_by` (G6 như G4) | — |
| 3 suy ra (chủ, có dòng ERP `status NULL` — 4 hàng Cty 4) | `UPDATE status = 4`, giữ `coefficient` | — |
| 4 Ngừng kinh doanh | ✗ 422 (đã khoá) | `UPDATE status = 3` |
| NULL (công ty chưa dùng) | ✗ 403 | ✗ 403 |
| `products.status ≠ 1` | ✗ 403 (D2) | ✗ 403 |

- Công ty lấy về: dòng luôn = 1 tới phase Tính giá (H1') ⇒ **chưa khoá được gì**; luật trên tự đúng khi phase Tính giá đưa lên 3.
- Mở khoá KHÔNG xoá dòng HRM vừa sinh lúc khoá ⇒ hàng cũ khoá-mở 1 lần là để lại dòng `coefficient 1` ⇒ popup ERP của công ty tạo làm tròn nghìn (K2). Đo quy mô nếu khoá hàng cũ chưa có dòng: Cty 1 **8.229**/27.370 · Cty 4 604/980 · Cty 3 13/14 · Cty 2 2/3 mã có giá ĐVT cơ bản lẻ nghìn.
- Ghi `updated_by`, `updated_at` (CLAUDE.md HRM :174 — khoá/mở khoá cũng là cập nhật). Lịch sử: CLAUDE.md :66 đòi ghi lịch sử khoá/mở khoá, nhưng §14b đã **hoãn lịch sử hàng hoá** ⇒ không ghi, ghi chú lệch trong plan.
- ERP không biết status 4 (N8): popup 338 màn ERP **và cả các popup HRM** đọc `product_company_coefficients` (`Modules/Finance/Services/ProductImportRequestService.php:1448`, `ProductTransferRequestService.php:984`, `BorrowSellRequest/BorrowSellRequestService.php:457`, `Modules/CustomerCare/Services/ServiceService.php:990`) đều chỉ đọc `coefficient`, không xét `status` ⇒ N8 mở rộng sang popup HRM (Phase 4).

### 5.2 Rà các chỗ 2-B / 2-C1 / 2-C2 / 2-C3 đã xét status 4

| # | Chỗ | File:dòng | Xét 4 | Kết luận |
|---|---|---|---|---|
| 1 | Màn *Hàng đang kinh doanh* | `Services/Product/ProductService.php:202` (`company_status = 3`) | 4 ≠ 3 ⇒ loại | ✅ |
| 2 | Đếm "chưa xếp catalog" (dòng nhắc cam) | `ProductService.php:111` (`= 3`) | loại | ✅ |
| 3 | Màn *Hàng hoá nhập thông tin* | `ProductService.php:198` (`= 1`) | loại | ✅ |
| 4 | Màn *Dữ liệu hàng hoá công ty* | `ProductService.php:191-194` (`IS NOT NULL`, lọc `company_status` tự do) | hiện, badge `#DC2626` | ✅ — đây là chỗ đặt **Mở khoá** |
| 5 | *Kho dữ liệu* `usage=unused` | `ProductService.php:180-187` (`IS NULL`) | 4 = đang dùng | ✅ |
| 6 | Cột *Công ty đang kinh doanh* | `Entities/Product/Product.php:456-470` (`where status = 3` + chủ chưa có dòng) | chủ khoá ⇒ có dòng 4 ⇒ không thêm chủ | ✅ cho 4 · ❌ **lỗi có sẵn**: chủ có dòng ERP `status NULL` (suy ra 3) cũng bị bỏ — 4 hàng: 38930, 39426, 39432, 39802 (Cty 4) ⇒ N18 |
| 7 | `can_edit` | `Product.php:423-428` + `ProductListResource.php:61`, `ProductDetailResource.php:43-44` | `!== STOPPED` | ✅ (G9a ẩn Sửa) |
| 8 | `can_take_back` | `Product.php:434-440` (`companyStatus === null`) | 4 ≠ null ⇒ không lấy lại | ✅ |
| 9 | L3 `owner_not_trading` (công ty tạo Ngừng KD ⇒ công ty khác không lấy về) | `ProductWriteService.php:219-221`, `Product.php:400-416` (`ownerStatusSql` COALESCE dòng chủ) | chủ = 4 ⇒ bỏ qua | ✅ (Q-A5 2-C2) |
| 10 | Popup catalog B3 | `Services/Product/ProductCatalogService.php:143-144` (tab Thêm `<> 4`), `:169` (sync thêm ⇒ 422 "ngừng kinh doanh"); gỡ không xét | đúng B3 | ✅ |
| 11 | Sửa đầy đủ / tab Quản trị / mở form | `ProductWriteService.php:113-115` (`assertOwner`), `:133-135` (`assertCanEditAdmin`) ← `Http/Requests/Product/ProductRequest.php:24-29`, `ProductAdminDataRequest.php:22-26`, `ProductWriteController.php:38-40` | `abort(403, …)` | ❌ **phải 423** (G6 + CLAUDE.md HRM :59-61). Đổi được ngay trong `authorize()` vì Laravel 8 chạy `passesAuthorization()` TRƯỚC validator ⇒ 423 vẫn đứng trước 422, không cần middleware. Test phải sửa: `Tests/Feature/ProductWriteApiTest.php:398-411`, các ca 403-status-4 ở `ProductTakeApiTest.php` (~:452-455, :479-482) |
| 12 | FE nhận 423 | `hrm-client/utils/helpers.js:258, 272` | đã có câu mặc định | ✅ |

### 5.3 Mã lỗi 423 vs 403

- **423** khi trạng thái tại công ty mình = 4 ở mọi thao tác GHI (sửa đầy đủ, tab Quản trị, mở form sửa, Xoá/Gỡ, Khoá lại) — thông báo "Hàng hoá đang ngừng kinh doanh, vui lòng mở khoá trước khi cập nhật." Đặt điều kiện trong 1 hàm entity (vd `ProductCompany::isLocked()` / `Product::lockedAt($companyId)`), không rải `if`.
- **403** giữ cho: không quyền 1652 · không phải chủ khi sửa lớp chung · `products.status ≠ 1` (D2) · công ty chưa dùng.
- Mở khoá là ngoại lệ duy nhất được gọi khi đang khoá.
- Thứ tự trong `assertOwner`: công ty (403) → D2 (403) → khoá (423) — giữ nguyên, chỉ đổi mã nhánh cuối.

---

## 6. Quyền

| Thao tác | Quyền | Căn cứ |
|---|---|---|
| Xoá / Gỡ | **1652** *Xây dựng thông tin hàng hoá* | §35b-4 "không thêm quyền" — đã chốt |
| Khoá / Mở khoá | **1652** (G6 mặc định, Q2) | G6 |

Kiểm seeder (`Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, memory *id-quyen-trung-khi-merge-nhanh-dai*):
- Nhánh: `grep -E '^\s*Permission::create' | uniq -d` ⇒ **0 id trùng** (các id 7, 8, 16… trùng chỉ nằm ở dòng comment). 1652/1653/1655 ở :1582-1584; 1670–1675 :1574-1579.
- `origin/gop_db` (c448133eb, 08/10 20:06): 0 trùng; đang dùng 1640–1651, 1660, 1661, **1676–1678** (CSKH tiềm năng — nhánh feature chưa có, merge sẽ không đụng id hàng hoá).
- DB local: 1652/1653/1655 có; 1652 gán role 18 *Super admin* + 100125 *E2E No Cost* (`company_id = 1`). Còn 4 quyền cũ 1616–1619 (nhánh `feat/p1` — §35b-5 đã bỏ, việc dọn để khi merge).
- Nếu Q2 chọn quyền mới: id trống 1657–1659 (1654, 1656 đã giữ cho Excel / Chính sách giá); phải INSERT riêng 1 dòng + `role_has_permissions.company_id = 1` + `cache:clear` (không chạy cả seeder — truncate).

---

## 7. Đề xuất endpoint, file, PHPUnit

### 7.1 Endpoint (khối `Routes/api.php:253-289`, đặt TRƯỚC `GET /{product}`)

| Method · URL | Gate | Hành vi | Trả |
|---|---|---|---|
| `DELETE master-data/products/{product}` | `checkPermission:Xây dựng thông tin hàng hoá` + `assertCanWrite` (R22) | chủ ⇒ xoá cứng; công ty lấy về ⇒ gỡ | 200 `{mode: 'deleted'|'released', code}` · 403/404/423/422 như 2.1 |
| `PUT master-data/products/{product}/lock` | như trên | 3 → 4 (5.1) | 200 `{company_status: 4, status_text, status_color}` · 403 · 422 (không ở 3) |
| `PUT master-data/products/{product}/unlock` | như trên | 4 → 3 | 200 · 403 · 422 (không ở 4) |

- Không dùng `GET …/lock` như danh mục cũ (đổi dữ liệu bằng GET); route **unlock KHÔNG gắn** guard 423.
- Hàng loạt: **không làm** ở 2-C4 (mockup chỉ có mục ⋮ từng dòng: *Xoá* ở màn Nhập thông tin — `mockup-luong-xay-dung-hang-hoa.html` `menuHtml` kiểu `nhap`; *Khóa* ở các màn khác — kiểu `kd`; không có *Mở khoá*). Nếu Q3 = có: `POST /bulk-delete` ≤ 100 mã, ngữ nghĩa "bỏ qua từng mã + lý do" như `take`, guard chứng từ chạy 1 câu `IN (…)`.
- Cờ mới ở `ProductListResource` + `ProductDetailResource`: `can_delete` (c–g, nhánh chủ cần mọi dòng công ty — list đã nạp `companies` mọi công ty ở `ProductService.php:278-281`; chi tiết `show()` chỉ nạp dòng công ty mình `:140-142` ⇒ thêm 1 query đếm), `can_lock` (= 3 ∧ 1652 ∧ status 1), `can_unlock` (= 4 ∧ 1652).

### 7.2 File sẽ đụng (hrm-api) — không migration, không seeder

| Loại | File |
|---|---|
| Create | `Services/Product/ProductLifecycleService.php` (destroy/hardDelete/release/lock/unlock) · `Services/Product/ProductUsageGuard.php` (ERP 4 đk + mở rộng + 153 FK + danh sách không FK) · `Http/Controllers/V1/Product/ProductLifecycleController.php` (hoặc thêm vào `ProductWriteController`) · `Tests/Feature/ProductLifecycleApiTest.php` |
| Modify | `Routes/api.php` (3 route) · `Entities/Product/Product.php` (`deletableAt`, `lockableAt`, `unlockableAt`; + sửa `tradingCompanyNames` nếu N18 làm trong đợt) · `Entities/Product/ProductCompany.php` (`isLocked`/hằng thông báo) · `Services/Product/ProductWriteService.php` (403 → 423 ở :113-115, :133-135) · `Transformers/Product/ProductListResource.php` + `ProductDetailResource.php` (3 cờ) · `Tests/Feature/ProductWriteApiTest.php` + `ProductTakeApiTest.php` (403 → 423) |
| FE (khảo sát riêng) | `components/product/ProductListPage.vue` (mục ⋮ Xoá / Khóa / Mở khoá theo cờ, `$confirm`), `pages/master-data/products/_id/index.vue` (footer), xử lý 423 ở form sửa |

### 7.3 PHPUnit tối thiểu (`DatabaseTransactions` + `ActsAsProductUser`; có quyền + không quyền + công ty khác — memory *always-test-permission-cases*)

**Xoá — công ty tạo**
1. Cty A (1652) tạo hàng (2-C1 `POST /`) rồi `DELETE` ⇒ 200 `deleted`; **0 dòng** còn lại ở cả 20 bảng mục 3.1 cho `product_id` đó (đếm từng bảng, kể cả `product_unit_prices` 6×ĐVT, `files`, 5 loại `productables`, đời xe); bảng khác không đổi số dòng (snapshot đếm `productables` loại không liên quan).
2. Hàng còn trạng thái 1 nhưng có tồn (`stocks.accounting_qty > 0`) / mượn chưa trả / là phụ kiện / là thành phần công thức ⇒ 422 đúng câu ERP, không xoá gì.
3. Hàng là phụ kiện lắp đặt / là "Máy dùng cho" hàng khác ⇒ 422 (theo Q6).
4. Có dòng ở 1 bảng chứng từ FK (vd `quotation_products`) ⇒ 422; có dòng ở 1 bảng KHÔNG FK (vd `serials`) ⇒ 422 (bắt được trước FK).
5. Hàng cũ ERP (suy ra 3, không dòng) ⇒ 422 "chỉ xoá hàng Đang nhập thông tin"; dòng chủ = 4 ⇒ **423**; `products.status = 0` ⇒ 403.
6. Công ty khác (B) đã có dòng `status 1` trên hàng của A ⇒ A xoá 422 "đã có công ty lấy về".
7. Không 1652 ⇒ 403; 1652 chỉ ở công ty khác công ty đang làm việc ⇒ 403 (R22); 0 dòng bị xoá.
8. Test so khớp danh sách 153 FK hằng số với `information_schema` (phát hiện FK mới).

**Gỡ — công ty lấy về**
9. B lấy về hàng chưa có dòng (INSERT coef 1, `created_by` B) + xếp catalog + NCC ⇒ `DELETE` ⇒ 200 `released`; dòng B **bị xoá**, catalog/NCC của B xoá; `products` + dòng/catalog/NCC của A không đổi (snapshot).
10. B lấy về mã có dòng ERP hệ số 1.03 (`created_by NULL`) ⇒ gỡ ⇒ dòng còn, `status NULL`, **`coefficient` vẫn 1.03**, 4 ô NULL; `/warehouse?usage=unused` của B có lại mã; lấy về lại được (L1).
11. B gỡ khi dòng = 4 ⇒ 423; B chưa lấy về ⇒ 403; B không 1652 ⇒ 403.

**Khoá / Mở khoá**
12. Chủ khoá hàng có dòng 3 ⇒ 4; mở khoá ⇒ 3; `coefficient` không đổi; `updated_by` = người bấm.
13. Chủ khoá hàng cũ chưa có dòng ⇒ INSERT coef 1, status 4, `company_id = current_company_role` (khác `info->company_id`); hàng có dòng ERP `status NULL` ⇒ UPDATE 4, giữ hệ số.
14. Khoá hàng 1 / 4 ⇒ 422; mở khoá hàng 3 ⇒ 422; công ty chưa dùng ⇒ 403; không 1652 ⇒ 403.
15. Sau khoá: `/trading` không có, `/company` có badge "Ngừng kinh doanh" `#DC2626`, `/entering` không có; `can_edit = false`, `can_unlock = true`; `PUT /{id}`, `PUT /{id}/admin-data`, `GET /{id}/edit` ⇒ **423**; Cty khác `take` ⇒ skipped `owner_not_trading`; `catalogs/sync` thêm ⇒ 422, gỡ ⇒ 200.
16. Cột *Công ty đang kinh doanh* của hàng chủ khoá không có tên chủ; (nếu N18 sửa) hàng chủ có dòng ERP `status NULL` có tên chủ.

---

## 8. Rủi ro + việc ngoài luồng mới

| # | Rủi ro | Cách né |
|---|---|---|
| R1 | FK chỉ phủ 172 cột; 139 cột `product_id` không FK (HRM dùng ~50 bảng) ⇒ xoá cứng để lại dòng mồ côi im lặng | guard quét danh sách không FK trước khi xoá (2–9 s/lượt) + test ca `serials` |
| R2 | Xoá cứng **giải phóng `code`** (UNIQUE) ⇒ `ProductCodeGenerator` có thể cấp lại đúng mã đó cho hàng khác; chứng từ ERP/HRM chép `code` dạng chuỗi (không FK) trỏ nhầm | chỉ xoá được hàng chưa phát sinh chứng từ (đk j) ⇒ không có chứng từ nào giữ mã đó; chấp nhận, ghi chú |
| R3 | Xoá `productables` phải xoá **mọi type** của `product_id` (khác bẫy chung "luôn kẹp type") — reviewer dễ "sửa" lại | comment + test đếm 5 loại về 0 |
| R4 | Gỡ dòng HRM sinh làm đổi giá popup ERP (bỏ làm tròn nghìn) | đúng mong muốn (trả nguyên trạng); dòng ERP giữ `coefficient` |
| R5 | Khoá hàng cũ chưa có dòng ⇒ sinh dòng coef 1 ⇒ popup ERP làm tròn nghìn kể cả sau khi mở khoá (8.229 mã Cty 1 có giá lẻ nghìn) | G6 đã chấp nhận như G4; xác nhận ở Q1 |
| R6 | ERP chưa biết status 4 (N8) + màn Hãng SX ERP xoá-chèn dòng (N2) ⇒ hàng đang khoá có thể tự "mở khoá" (mất dòng) khi ai đó lưu Hãng SX ở ERP | đã ghi N2/N8; 2-D chặn |
| R7 | Đua: 2 người cùng xoá / xoá + khoá cùng lúc | `lockForUpdate` dòng `products` + dòng công ty trong transaction; xoá lần 2 ⇒ 404 |
| R8 | Đổi 403 → 423 làm đỏ ca test cũ + FE nào đang bắt 403 riêng cho Ngừng KD | sửa 2 file test; FE đã có nhánh 423 ở `helpers.js:272` |
| R9 | Lịch sử khoá/mở khoá (CLAUDE.md :66) vs §14b hoãn lịch sử | theo §14b — ghi chú lệch trong plan |

Việc ngoài luồng mới (nối tiếp N17 ở `c2-plan.md:391`):

| # | Việc | Nguồn |
|---|---|---|
| N18 | `Product::tradingCompanyNames()` (`Entities/Product/Product.php:456-470`) bỏ sót công ty tạo khi dòng chủ là dòng ERP `status NULL` (luật suy ra coi là 3) ⇒ cột *Công ty đang kinh doanh* thiếu chủ ở 4 hàng Cty 4 (38930, 39426, 39432, 39802). Lỗi 2-B, thuộc luồng hàng hoá — có thể sửa trong 2-C4 nếu user cho | đọc code + đo 08/10 |
| N19 | Popup HRM (Finance: Yêu cầu nhập hàng, Yêu cầu chuyển kho, Mượn bán; CustomerCare: Dịch vụ) đọc `product_company_coefficients` chỉ lấy hệ số, không xét `status` ⇒ hàng Ngừng KD (4) vẫn chọn được ở HRM (mở rộng N8 sang HRM, Phase 4 popup dùng chung) | 5.1 |
| N20 | 139 cột `product_id` không FK, 169/183 không index ⇒ mọi kiểm "đã dùng chưa" sau này (Phase 4/5) đều chậm + dễ sót; cân nhắc index/FK khi dọn DB | 3.3 |
| N21 | DB local còn 4 quyền cũ 1616–1619 (nhánh `feat/p1`) — dọn khi merge | 6 |

---

## 9. Câu hỏi cho user (hỏi lần lượt — chỉ điểm chưa có chốt)

### Q1. Xác nhận "mặc định đề xuất" của G6 về **chuyển trạng thái khoá**

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **Chỉ khoá được từ 3 *Đang kinh doanh* → 4; mở khoá về 3. Hàng cũ chưa có dòng ⇒ sinh dòng `coefficient 1`, status 4** (đúng G6) | luật gọn, khớp mockup (*Khóa* chỉ ở các màn ngoài *Nhập thông tin*); hàng đang nhập dùng Xoá thay vì Khoá; mở khoá không xoá dòng ⇒ popup ERP của công ty tạo làm tròn nghìn vĩnh viễn với mã từng khoá (Cty 1: tối đa 8.229 mã giá lẻ nghìn) |
| (b) Khoá được từ 1/2/3; mở khoá trả về trạng thái trước khi khoá | phải nhớ trạng thái cũ ⇒ **thêm cột** (vd `status_before_lock`) = migration bảng ERP; hàng đang nhập có 2 lối (Xoá / Khoá) |
| (c) Như (a) nhưng mở khoá hàng cũ ⇒ XOÁ dòng HRM đã sinh lúc khoá (nếu 4 ô quản trị trống) | trả giá ERP về nguyên trạng; thêm 1 nhánh code + phân biệt dòng bằng `created_by`; mất dữ liệu quản trị nếu người dùng đã khai giữa chừng (điều kiện "4 ô trống" né được) |

### Q2. Quyền Khoá / Mở khoá

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **1652 *Xây dựng thông tin hàng hoá*** của chính công ty (G6) | không seeder, không đụng DB; ai sửa được hàng thì khoá được |
| (b) Quyền mới (vd 1657 *Khoá / mở khoá hàng hoá*) | tách vai (vd chỉ trưởng phòng ngừng KD); thêm seeder + INSERT DB local + gán role; memory id trùng phải kiểm lại khi merge |

### Q3. Có làm **hàng loạt** (Xoá / Khoá nhiều mã một lượt) ở 2-C4 không?

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **Không** — chỉ từng dòng (menu ⋮ + footer chi tiết), đúng mockup chốt | ít việc; guard chứng từ 2–9 s/lượt chấp nhận được cho 1 mã |
| (b) Có, ≤ 100 mã/lượt, bỏ qua từng mã + lý do như *Lấy về* | thêm thanh chọn dòng ở 2–3 màn + endpoint `bulk-*`; guard chạy 1 câu `IN (…)` |

### Q4. Công ty LẤY VỀ được "Xoá" (gỡ) ở trạng thái nào của mình?

G7 chỉ nói gỡ = trả dòng; `yeu-cau-ghi.md:93` ghi *đề xuất* chưa chốt.

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **Chỉ khi trạng thái của mình = 1 *Đang nhập thông tin*** (nút Xoá chỉ có ở màn này — mockup) | đối xứng với công ty tạo (§35b-4); hiện mọi hàng lấy về đều = 1 (H1') nên không hạn chế gì thêm; sau phase Tính giá hàng đã kinh doanh muốn bỏ thì dùng Khoá |
| (b) Ở mọi trạng thái trừ 4 (1/2/3) | công ty lấy về bỏ được cả hàng đang kinh doanh — mất dữ liệu quản trị + catalog đã khai, popup ERP đổi giá ngay |

### Q5. Gỡ (công ty lấy về) dọn những gì ngoài dòng công ty + catalog?

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **Dọn sạch phần của công ty mình**: catalog + **NCC** (`product_suppliers` theo `company_id`) + dòng công ty (dòng ERP ⇒ `status NULL` + **4 ô quản trị về NULL**, giữ `coefficient`; dòng HRM ⇒ xoá) | đúng nguyên trạng trước khi lấy về; lấy về lại thì 4 ô trống như L2 |
| (b) Chỉ đúng chữ G7: dòng công ty + catalog, NCC và 4 ô giữ | lấy về lại thấy NCC/bảo hành cũ — trái L2 (lấy về để trống); NCC của công ty còn trỏ hàng công ty không dùng |

### Q6. Hàng do công ty tạo muốn xoá đang được **hàng khác** tham chiếu ở tab *Nhóm máy* (là "Máy dùng cho") hoặc là phụ kiện **lắp đặt / sửa chữa**

ERP chỉ chặn phụ kiện đi kèm + công thức. Phụ kiện lắp đặt/sửa chữa có FK (DB tự chặn); "Máy dùng cho" (`productables` loại `App\Product`) **không có FK** — 2.535 hàng đang là máy của hàng khác.

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **Chặn**, báo rõ "Hàng đang được khai là Máy dùng cho / phụ kiện lắp đặt / phụ kiện sửa chữa của hàng khác" | không âm thầm sửa dữ liệu hàng của người khác; người dùng gỡ ở hàng kia trước |
| (b) Tự gỡ liên kết ở hàng kia rồi xoá | xoá trơn tru, nhưng hàng khác (có thể của công ty khác — `productables` là lớp chung) bị đổi mà chủ của nó không biết |

### Q7. Xoá cứng có xoá **tệp trên S3** (ảnh, video, tài liệu kỹ thuật) không?

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **Không** — chỉ xoá dòng DB | an toàn: 147 URL ảnh + 5.556 avatar đang dùng chung giữa nhiều hàng (Sao chép kiểu ERP), HRM/ERP chưa từng xoá S3; tốn dung lượng tệp mồ côi (hàng mới tạo thường ≤ 10 ảnh) |
| (b) Xoá đối tượng S3 nếu không còn dòng nào khác trỏ cùng URL (`product_galleries`, `products.avatar`, `files`, `product_templates`…) | dọn dung lượng; phải quét nhiều bảng + xoá S3 SAU commit (rollback không lấy lại được tệp); bẫy khi làm Sao chép (G8) |

---

## Phụ lục A — câu SQL đã chạy (SELECT)

```sql
-- FK trỏ products
SELECT COUNT(*), SUM(DELETE_RULE='CASCADE'), SUM(DELETE_RULE IN ('RESTRICT','NO ACTION'))
FROM information_schema.REFERENTIAL_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA='hrm_erp' AND REFERENCED_TABLE_NAME='products';          -- 172 · 0 · 172
-- Cột product_id/base_product_id không FK
SELECT c.TABLE_NAME, c.COLUMN_NAME FROM information_schema.COLUMNS c
JOIN information_schema.TABLES t ON t.TABLE_SCHEMA=c.TABLE_SCHEMA AND t.TABLE_NAME=c.TABLE_NAME AND t.TABLE_TYPE='BASE TABLE'
WHERE c.TABLE_SCHEMA='hrm_erp' AND c.COLUMN_NAME IN ('product_id','base_product_id')
  AND NOT EXISTS (SELECT 1 FROM information_schema.KEY_COLUMN_USAGE k WHERE k.TABLE_SCHEMA=c.TABLE_SCHEMA
     AND k.TABLE_NAME=c.TABLE_NAME AND k.COLUMN_NAME=c.COLUMN_NAME AND k.REFERENCED_TABLE_NAME='products'); -- 183
-- Nguồn gốc dòng công ty
SELECT created_by IS NULL, COUNT(*), SUM(coefficient=1) FROM product_company_coefficients GROUP BY 1; -- 1 · 1105 · 258
-- Dòng chủ là dòng ERP status NULL trên hàng hoạt động (N18)
SELECT pcc.product_id FROM product_company_coefficients pcc JOIN products p ON p.id=pcc.product_id
WHERE pcc.company_id=p.company_id AND p.status=1;                                   -- 38930, 39426, 39432, 39802
```
