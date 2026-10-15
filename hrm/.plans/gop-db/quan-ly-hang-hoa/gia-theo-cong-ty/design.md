# Giá theo công ty + màn Cập nhật giá bán / Duyệt giá bán (HRM) — DESIGN (09/10/2026)

> **Chỉ là tài liệu.** Chưa sửa source, chưa chạy migration/seeder. DB chỉ SELECT (`hrm_erp` local, bản chụp ERP 15/09/2026, đo lại 09/10).
> Muốn code đợt con nào thì phải hỏi riêng và nhận câu "làm" rõ ràng, kèm phạm vi (CLAUDE.md gốc, tiền đề #6).
>
> **Luật cao nhất (theo thứ tự):** `ton.md` (P1–P14 + ghi chú cuối 09/10) → `../2d-erp-khong-loi/d2-ton.md` (D1–D12, đảo QC-2) →
> `../2d-erp-khong-loi/ton.md` mục C (QC-*; QC-2 và QC-4 đã bị đảo) → `../2c-ghi/chot.md` → `../SO-CHOT-VA-TON.md` §1 →
> `../man-danh-muc-hang-hoa/design.md` §19 §24 §25 §26 + `ton-chot-truoc-code.md` A4/A5.
> Chỗ nào nguồn chốt mâu thuẫn hoặc còn thiếu: **không tự quyết nghiệp vụ**, ghi ở §9 *Tồn còn lại*.
>
> **Mã tham chiếu:**
> - ERP: worktree `websites/wt-erp-2d1`, nhánh `feat/2d1-erp-khong-loi`, HEAD `b2f1761789`.
> - HRM: `websites/wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}`, nhánh `feat/chuyen-doi-hang-hoa`, api `a862fbeef`, client `9b05f7b42`.
>
> **Ký hiệu:** `P` = ERP `app/Product.php` · `PC` = ERP `app/Http/Controllers/ProductsController.php` · `PAC` = ERP
> `app/Http/Controllers/ProductApprovesController.php` · `SC` = ERP `app/Http/Controllers/Common/SearchController.php` · `web` =
> ERP `routes/web.php` · `MD` = HRM `hrm-api/Modules/MasterData` · `upp` = `product_unit_prices` · `pep` = `product_expected_prices`
> · `pcu` = `product_company_units` (bảng mới) · `pcc` = `product_company_coefficients` · `pa`/`pap` = `product_approves`/`product_approve_prices`.
> Nguồn khảo sát: `KE` = `khao-sat-erp.md` · `KH` = `khao-sat-du-lieu-hrm.md` · `KB` = `../2d-erp-khong-loi/d2-khao-sat-be.md` ·
> `KF` = `../2d-erp-khong-loi/d2-khao-sat-fe.md` · `KC` = `../2d-erp-khong-loi/khao-sat-c-gia.md`.

---

## 1. Tóm tắt quyết định

### 1.1 Tiền đề và nền

| Mã | Nội dung | Nguồn |
|---|---|---|
| TĐ#1 | Chuyển nền code, không đổi CSDL. Mọi thay đổi schema là **NGOẠI LỆ** (§2.4 liệt kê từng migration) | `SO-CHOT-VA-TON.md` §1 #1 |
| TĐ#5 | Không bảo mật thông tin hàng hoá và giá bán. Quyền chỉ kiểm soát **thao tác** và **xem giá vốn** | §1 #5 |
| TĐ#7 | Không merge vào `gop_db` | §1 #7, memory |
| TĐ#8 | Bỏ hệ số giá `pcc.coefficient`, mỗi công ty tự xây giá riêng | §1 #8 |
| TĐ#9 | Việc ngoài luồng thì ghi lại (N*), không vá trong đợt | §1 #9 |
| A4 | Hướng B: `upp.company_id` NOT NULL, dữ liệu cũ gán cho công ty tạo. Ép NOT NULL / xoá cột chung để cuối | `ton-chot-truoc-code.md:26` |
| A5 | Tách giá vốn/giá mua ngoài khỏi `product_units` ⇒ bảng `pcu` | `ton-chot-truoc-code.md:27` |
| §25a | `pep` **không** thêm `company_id` (thừa hưởng qua `unit_price_id`) | `design.md` §25a |
| H1'/H1'' | Hàng HRM tạo/lấy về nằm ở *Đang nhập thông tin* cho tới luồng Tính giá (Phase 7), không có nút chuyển tạm | `2c-ghi/chot.md:8-9` |
| 🔴 Ghi chú 09/10 | **Lên production MỘT LẦN** khi xong hết các phase ⇒ không thiết kế giai đoạn tạm giữa các phase | `ton.md:41-42` |

### 1.2 Giá theo công ty (P1–P14)

| Mã | Chốt | Nguồn |
|---|---|---|
| P1 | Công ty khác chủ: chép **đúng con số ERP đang hiện** (giá chủ × hệ số, làm tròn như `getData`) | `ton.md:23` |
| P2/P2b | **Đổi 15/10:** **nhóm chia sẻ 1 Tân Phát · 3 Vinh · 4 SG** chép giá **lẫn nhau** mọi hàng đang bán: hàng của công ty nào trong nhóm cũng chép cho 2 công ty còn lại, áp hệ số của **công ty NHẬN** (không có ⇒ 1, giá bằng). Không theo mốc chứng từ. ~~Cụm cũ 1·2·3·4~~ (HP ra khỏi nhóm) | `ton.md:24`, `cum-gia-1510-brief.md` |
| P2c | **Đổi 15/10:** **2 HP · 7 ETEK Green tự quản** — chỉ dùng hàng mình LÀM CHỦ (`products.company_id`): vẫn qua B1–B4, KHÔNG nhận hàng chép, KHÔNG cho hàng của mình sang nhóm (3 mã HP ở lại HP). **Cty 5, 6, 8 không dùng phần mềm**: không chép, không xử lý giá riêng (như cũ) | `ton.md:24, 43-44`, `cum-gia-1510-brief.md` |
| P2d | Chép giá thì **sinh kèm dòng trạng thái "Đang kinh doanh"** ở công ty nhận. Bất biến 2 chiều trạng thái ⇔ bộ giá | `ton.md:24` |
| P3 | Dòng giá cũ gán cho `products.company_id` (Cty1 258.270 · Cty4 6.215 · Cty3 138 · Cty2 18 · NULL 5) | `ton.md:25` |
| P4 | Chưa có giá = chưa tới "Đang kinh doanh" ⇒ không vào popup. Popup chỉ lấy hàng Đang kinh doanh | `ton.md:26` |
| P5 | Mỗi công ty sửa bộ giá của mình. **Bỏ QC-4** (luật hãng SX + chủ) | `ton.md:27` |
| P6 | Chứng từ đọc giá của **công ty ghi trên chứng từ** (sửa/duyệt chứng từ cũ cũng vậy) | `ton.md:28` |
| P7 | 13 cột theo công ty. Backfill chép giá vốn của chủ. Hàng lấy về mới ⇒ 0 | `ton.md:29` |
| P8 | Hạch toán hỗ trợ / hiệu quả HĐ: lấy giá vốn công ty chứng từ, thiếu thì chặn duyệt | `ton.md:30` |
| P9/P9b | PTG + hàng tạm ERP: **chốt ở Phase 7/6**, không có giai đoạn tạm | `ton.md:31` |
| P10 | Bỏ hệ số cùng lúc bật giá theo công ty. Chấp nhận 26 chỗ `getPriceByUnitAndType` đổi sang giá có hệ số | `ton.md:32` |
| P11 | Cron 14:30 chỉ reset dòng giá của chính công ty có cấu hình | `ton.md:33` |
| P12 | Bật **một lần cả cụm 1-2-3-4**, có lệnh so khớp trước khi bật, có cờ để lui. *(Đổi 10/10 bỏ cờ; đổi 15/10: nhóm chia sẻ 1·3·4 + tự quản 2·7 — xem P2c)* | `ton.md:34` |
| P13 | Duyệt/Không duyệt: chỉ duyệt của **công ty chủ** mới đổi `products.status`. Công ty khác chỉ đổi trạng thái theo công ty mình | `ton.md:35` |
| P14 | Giá theo công ty lên cùng lúc với 2 màn giá HRM (thực tế cả feature lên một lần) | `ton.md:36` |

### 1.3 Màn giá (D1–D12) và QC còn hiệu lực

| Mã | Chốt | Nguồn |
|---|---|---|
| D1 | Duyệt/Không duyệt chỉ đổi `products.status` khi đang `= 2` (2→1 / 2→5). Kết hợp P13: chỉ công ty chủ | `d2-ton.md:30` |
| D2 | Màn Cập nhật giá chỉ hiện hàng **ĐANG KINH DOANH ở công ty của user** (gồm hàng lấy về). Không có chế độ xem toàn bộ. D2b tự hết nhờ P5 | `d2-ton.md:31, 44` |
| D3 | Khoá **Ngừng kinh doanh (4)** và **Chờ tính giá (2)**: BE chặn 423 | `d2-ton.md:32` |
| D4 | Sửa ô "Hãng cần duyệt" ở `/sale/regulation-config`: option `brands` → `manufactures` cho `brand_ids` + `new_brand_ids` | `d2-ton.md:33` |
| D5 | Duyệt theo logic ERP (`PAC:188-274`): người duyệt sửa được hệ số/giá/ĐMGG + giá hiệu lực (ngày < mai thì dời = mai), áp giá người duyệt gửi. Giá vốn lấy `pa.cost_price`. Duyệt hàng loạt port theo nghĩa duyệt đơn | `d2-ton.md:34` |
| D6 | Lọc Còn/Hết tồn **làm thật, theo tồn công ty mình** | `d2-ton.md:35` |
| D7 | Chặn + ẩn nút `manualUpdatePrices` (cron 01:00 vẫn chạy) | `d2-ton.md:36` |
| D8 | Thông báo 2 chiều, prefix `[GIA]`: gửi đề nghị ⇒ người có quyền 1658; kết quả Đã duyệt/Không duyệt ⇒ người đề nghị. Bản ghi do PTG/hàng tạm ERP sinh: HRM không bắn thêm, chỉ đổi link ERP sang HRM | `d2-ton.md:37` |
| D9 | Menu ở **phân hệ Tài chính**. Vị trí nhóm cụ thể chốt ở mockup | `d2-ton.md:38` |
| D10 | Lịch sử giá theo **hàng hoá × công ty**, popup ở 2 màn, chỉ có từ lúc HRM chạy, chưa thêm khối vào chi tiết hàng hoá | `d2-ton.md:39` |
| D11 | Xuất Excel ở màn Duyệt giá. Màn Cập nhật giá không có | `d2-ton.md:40` |
| D12 | Làm mockup HTML trước (2 màn + 3 popup, JS tính thật, style V2 đo từ app) | `d2-ton.md:41` |
| QC-1 | Phiếu tính giá ở ERP tới Phase 7 | `ton.md:47` |
| QC-5 | Hàng "Đang nhập thông tin" **không** cho nhập giá | `ton.md:51` |
| QC-6 | Port Duyệt giá sang HRM | `ton.md:54` |
| QC-7 | Cập nhật giá theo hãng: khoá ERP (đã làm ở 2-D1), port sau (N36) | `ton.md:55` |
| QC-8 | Công khoán + ghi chú hàng hoá: màn giá chỉ hiển thị | `ton.md:52` |
| QC-9 | Lịch sử theo khuôn entity-history HRM, ngừng ghi `product_versions` | `ton.md:53` |
| QC-10 | 2 cron + 3 màn chỉ xem giữ ERP, chuyển sau (N34) | `ton.md:56` |
| ~~QC-0~~ | "2-D2 không chặn go-live" **hết hiệu lực** do ghi chú "lên production một lần" | `ton.md:46` ↔ `ton.md:41` |
| ~~QC-2, QC-3, QC-4~~ | Đảo bởi d2-ton đầu file, P10 và P5 | `d2-ton.md:3-9` |

---

## 2. Mô hình dữ liệu cuối

### 2.1 Sơ đồ

```
products (company_id = công ty QUẢN LÝ/tạo; status ERP 0/1/2/5)
 ├─< product_company_coefficients  (product_id, company_id) UNIQUE  — "dòng hàng × công ty": status 1..4 + 4 ô quản trị
 │                                   coefficient: NGỪNG ĐỌC, giữ cột (NOT NULL) tới bước dọn cuối; dòng mới ghi 1
 └─< product_units                  (product_id, unit_id, is_base, unit_coefficient, timestamps) — CHUNG
      │   13 cột giá cũ: ngừng đọc/ghi (chỉ INSERT 0 vì NOT NULL), xoá ở bước dọn cuối (§2.4 M-cuối)
      ├─< product_company_units  MỚI (product_unit_id, company_id) UNIQUE — 13 cột giá theo công ty
      └─< product_unit_prices    + company_id (product_unit_id, company_id, price_type_id) UNIQUE
           └─< product_expected_prices (unit_price_id)        — thừa hưởng công ty từ cha (§25a)
           └─< product_approve_prices.product_unit_price_id  — thừa hưởng
product_approves.company_id = công ty của BỘ GIÁ (công ty sửa giá), không còn là công ty chủ
```

### 2.2 Bảng mới `product_company_units`

| Cột | Kiểu (giữ đúng kiểu ở `product_units`, đo `information_schema` 09/10) | Ghi chú |
|---|---|---|
| `id` | bigint unsigned PK | |
| `product_unit_id` | bigint unsigned NOT NULL, FK `product_units.id` | |
| `company_id` | bigint unsigned NOT NULL, FK `companies.id` | gán tay, không qua hook BaseModel (bài học 2-C2) |
| `product_id` | bigint unsigned NOT NULL, FK `products.id` | dư thừa có chủ đích (lọc hàng × công ty không phải nối qua `product_units`) |
| `cost_price` | decimal(16,2) NOT NULL **DEFAULT 0** | bảng cũ NOT NULL không default |
| `buy_price` | decimal(16,2) NULL | |
| `sale_max_percent_coefficient` | double(12,2) NULL DEFAULT 1.00 | |
| `liquidation_sale_max_percent` | double NULL DEFAULT 0 | |
| `according_base_price` | tinyint(1) NULL DEFAULT 0 | |
| `price_wait_approve` | decimal(18,2) NULL | |
| `coefficient_wait_approve` | decimal(10,2) NULL | |
| `sale_max_percent_wait_approve` | decimal(10,2) NULL | |
| `flag_price_wait_approve` | tinyint NULL | 0/NULL bình thường · 1 chờ duyệt · 2 không duyệt |
| `approve_comment` | text NULL | |
| `approve_time` | datetime NULL | |
| `reason_edit_price` | text NULL | |
| `note_edit_price` | text NULL | |
| `created_by`, `updated_by`, `created_at`, `updated_at` | | |

Khoá/index: **UNIQUE(`product_unit_id`, `company_id`)** · INDEX(`company_id`, `product_id`).
13 cột theo công ty = đúng danh sách `KH:60-73` (6 cột chung: `id, product_id, unit_id, is_base, unit_coefficient, timestamps`).

### 2.3 `product_unit_prices.company_id`

- Bước 1: `company_id` bigint unsigned **NULL**, FK `companies.id`, INDEX(`product_unit_id`, `company_id`, `price_type_id`).
- Bước 2 (sau backfill, §3): `NOT NULL` + **UNIQUE(`product_unit_id`, `company_id`, `price_type_id`)**, bỏ INDEX thường
  `product_unit_prices_unit_price_type_index` (bị UNIQUE bao). Đo 09/10: 0 cặp trùng (ĐVT × loại), nên tạo UNIQUE không vướng.
- Giá hiệu lực `pep`: không thêm cột. Cron 01:00 áp theo `unit_price_id` ⇒ tự đúng công ty (`KE:215`).
- Cờ chờ duyệt trên `upp`/`pep` tự thành "theo công ty", vì dòng đã thuộc một công ty.

### 2.4 Migration — NGOẠI LỆ schema (TĐ#1), đặt ở `hrm-api/Modules/MasterData/Database/Migrations` (cùng chỗ 2-A)

| # | File (đề xuất) | Việc | Lùi |
|---|---|---|---|
| M1 | `2026_10_xx_000001_create_product_company_units_table.php` | tạo bảng §2.2 | drop bảng |
| M2 | `…000002_add_company_id_to_product_unit_prices_table.php` | §2.3 bước 1 (NULL + FK + index) | drop cột |
| M3 | `…000003_enforce_company_id_on_product_unit_prices_table.php` | §2.3 bước 2. **Tự kiểm**: còn dòng `company_id IS NULL`, hoặc còn cặp trùng (ĐVT, công ty, loại) ⇒ `throw` kèm số dòng, không đổi gì | về NULL + index thường |
| M-cuối | (**không thuộc đợt này**) drop 13 cột giá ở `product_units` + `pcc.coefficient` | chỉ chạy khi PTG (Phase 7) và hàng tạm (Phase 6) không còn ghi cột cũ và test danh sách trắng ở 2 repo = 0 | — |

- Không migration cho `pcc`: dòng trạng thái ghi bằng lệnh backfill (§3), cột `status` đã có từ 2-A.
- Không migration cho lịch sử, duyệt, quyền: `catalog_histories`, `pa`/`pap` có sẵn. Quyền thêm bằng seeder, chỉ 2 dòng (§6.2).
- **Trình tự khi triển khai** (một lần, G2b 10/10 — không cờ): `migrate` tới M2 (M1–M2) → lệnh backfill (§3) → lệnh so khớp
  = 0 lệch → `migrate` (M3). KHÔNG còn lệnh `complete-sets`, KHÔNG còn bước bật cờ (code mới luôn đọc/ghi theo công ty).
  M3 tự chặn nếu ai chạy `migrate` một lèo mà quên backfill.

### 2.5 Bất biến (thay HĐ1/HĐ2/G2 của bảng chung — `KC:151-164`, `2c-ghi/chot.md:26`)

| # | Bất biến | Ai giữ |
|---|---|---|
| BB1 | **Trạng thái ⇔ bộ giá:** cặp (hàng × công ty) có `pcc.status IS NOT NULL` ⇔ có **đủ bộ giá**: với **mỗi** ĐVT của hàng có 1 dòng `pcu` + 6 dòng `upp` (loại 1–6) của công ty đó | tạo hàng, lấy về, thêm ĐVT, gỡ, xoá cứng, backfill |
| BB2 | **Đang kinh doanh ⇒ có giá:** `pcc.status = 3` ⇒ BB1 (các giá có thể = 0 do cron 14:30. "Có giá" nghĩa là có đủ dòng) | như trên + đường chuyển trạng thái (Phase 7) |
| BB3 | 1 dòng / (ĐVT × công ty × loại giá); sửa tại chỗ, không xoá dòng khi sửa giá. Thiếu thì sinh (HĐ1 theo công ty) | UNIQUE M3 + service ghi |
| BB4 | ≤ 1 giá hiệu lực tương lai / dòng `upp`, `status = 2`, `effect_date > hôm nay` (HĐ6 giữ nguyên) | service ghi giá |
| BB5 | Màn giá không đổi `unit_id`/`is_base`/`unit_coefficient` (HĐ2, C7) | service ghi giá + duyệt (không chép `pa.unit_coefficient` như ERP `PAC:254,490`) |
| BB6 | `pa.company_id` = công ty của bộ giá. Mỗi (hàng × ĐVT × công ty) có ≤ 1 `pa` đang mở. Xử lý xong thì **xoá cứng `pa` + `pap`** như ERP, vì PTG/dashboard ERP dựa vào việc này (`KB:254-260`) | service ghi + duyệt |
| BB7 | Mọi đường đọc giá đều mang `company_id` tường minh. Không global scope (`KE:272`) | lớp truy cập §4 + test danh sách trắng |
| BB8 | Ngày bật, mọi đường đọc trả **đúng số ERP đang hiện** cho cụm 1-2-3-4 (P1, P12), trừ các lệch đã liệt kê ở §3.6. *Đổi 15/10: chỉ cho cặp cần có giá (chủ + nhận trong nhóm 1·3·4); HP/ETEK Green chỉ còn hàng mình làm chủ — N128* | lệnh so khớp + snapshot §3.7 |

---

## 3. Backfill

### 3.1 Lệnh

- HRM `php artisan product-price:backfill-company {--dry-run} {--company=*} {--chunk=500}` (đặt ở `MD/Console`). Chạy theo lô, mỗi lô
  một transaction. **Idempotent**: `insertOrIgnore` theo UNIQUE. UPDATE chỉ đụng dòng còn `company_id IS NULL`, hoặc `pcc.status IS NULL`.
- `--dry-run` in số dòng sẽ ghi theo bảng × công ty, để so với bảng ước tính §3.4. Không chạy trong migration.
- **Đổi 15/10:** 2 danh sách ở 1 chỗ (config `price.php`): `shared_price_company_ids = [1, 3, 4]` (nhóm chia sẻ, B5) và
  `self_managed_company_ids = [2, 7]` (tự quản: chỉ B1–B4 cho hàng mình làm chủ; dùng cho so khớp + cột bảng in). Cty 5/6/8 không
  thuộc danh sách nào (P2c). ~~`CLUSTER = [1, 2, 3, 4]` (`price.cluster_company_ids`)~~ đã bỏ.

### 3.2 Thuật toán (đúng thứ tự)

```
B0  Kiểm trước: upp mồ côi = 0, pcu đã có = 0 (hoặc chỉ có dòng do chính lệnh tạo), trùng (ĐVT, loại) = 0. Lệch ⇒ dừng.
B1  GÁN CHỦ (P3): UPDATE upp SET company_id = products.company_id (qua product_units), mọi trạng thái hàng.
      Hàng products.company_id NULL (id 9964 `SG-PSS180103`, status 0, 1 ĐVT / 5 dòng): gán Cty 4 theo tiền tố SG- (KH:143),
      chỉ gán ở dòng giá/pcu, không sửa `products`.
B2  PCU CHỦ: với MỌI ĐVT (46.560), INSERT pcu(company = chủ) chép nguyên 13 cột từ product_units (P7).
B3  BÙ LOẠI GIÁ CHO CHỦ: với hàng products.status = 1 (xem T1), ĐVT thiếu loại 5/6 ⇒ INSERT upp (company = chủ, price 0,
      coefficient 0, sale_max_percent NULL, cờ 0) — y hành vi ERP `PC:2724-2727` tự sinh khi lưu.
B4  TRẠNG THÁI CHỦ (A3, gỡ @TODO-BACKFILL): hàng products.status = 1 ⇒ pcc(chủ) status 3. Có dòng (status NULL) ⇒ UPDATE status,
      giữ coefficient. Chưa có ⇒ INSERT coefficient 1, status 3, created_by NULL.
B5  CHÉP NHÓM (P1, P2b — đổi 15/10): với mỗi hàng H: products.status = 1 (T1), chủ C ∈ SHARED = {1,3,4}; với mỗi công ty
    nhận R ∈ SHARED \ {C}. Chủ ∈ tự quản {2,7} hoặc 5/6/8 ⇒ dừng ở B4 (không chép ra, không nhận vào):
      k = pcc(H, R).coefficient nếu có dòng, ngược lại 1                     # hệ số của công ty NHẬN
      với mỗi ĐVT U của H:
        pcu(U, R)  = chép 5 cột giá trị của pcu(U, C): cost_price, buy_price, sale_max_percent_coefficient,
                     liquidation_sale_max_percent, according_base_price. 8 cột duyệt/vết = NULL (P7, T7)
        với mỗi loại t = 1..6:
          src = upp(U, C, t)   (đã đủ 6 sau B3)
          price' = (k ≠ 1) ? round(src.price × k / 1000) × 1000 : src.price     # đúng P:1249-1257 (getData), làm tròn
                                                                               # half-away-from-zero, tính trên DECIMAL/PHP
          INSERT upp(U, R, t): price', coefficient = src.coefficient, sale_max_percent = src.sale_max_percent,
                               3 cờ is_manual_* = src, *_wait_approve = NULL, flag_* = 0
          với mỗi pep của src có status = 2 AND effect_date > hôm nay (đúng những gì getData trả):
               INSERT pep(unit_price_id = dòng mới): price = (k ≠ 1) ? round(ep.price × k / 1000) × 1000 : ep.price,
                    coefficient, sale_max_percent, effect_date, status 2, flag 0, *_wait_approve NULL,
                    created_by/updated_by = created_by của ep gốc (cột NOT NULL + FK employees — KB:184-185)
      TRẠNG THÁI NHẬN (P2d): pcc(H, R) status 3. Có dòng ⇒ UPDATE status (giữ coefficient). Chưa có ⇒ INSERT coefficient 1, status 3.
B6  Kiểm sau: BB1 cho mọi cặp có status, số dòng khớp dry-run, upp.company_id NULL = 0.
```

- **Không chép:** dòng `pep` đã áp (status 1) — đó là lịch sử. Không chép `pep` status 2 đã quá ngày (13.662 dòng, cron bỏ qua mãi,
  `KH:145`; ghi N65). Không chép cờ/giá chờ duyệt, vì yêu cầu duyệt thuộc công ty đã gửi.
- **Không đụng** `pcc.coefficient` (HĐ7). Dòng `pcc` cũ chỉ UPDATE `status` (V5/L1 dựa vào `created_by IS NULL`, `KH:304-305`).
- Không có cặp nào đang ở trạng thái 1/2/4: production chưa có hàng HRM, local `pcc.status` NULL cả 1.105 dòng (đo 09/10). Lệnh vẫn
  bỏ qua cặp đã có `status`, để chạy lại được.

### 3.3 ĐVT thiếu dòng loại 5/6

Đo 09/10, hàng `status = 1` thuộc cụm: Cty 1 thiếu loại 5 ở 5.407 ĐVT, loại 6 ở 358 · Cty 4 thiếu loại 5 ở 102, loại 6 ở 6 · Cty 2/3 đủ.
B3 bù cho chủ, nên B5 chép ra đủ 6 dòng. Hệ quả: với các ĐVT này, chứng từ hỏi loại 5/6 sẽ nhận **giá 0** thay cho lỗi 404/500 do
`firstOrFail` (`P:1441-1452`). Đây là lệch có chủ đích, nằm trong §3.6.

### 3.4 Số dòng ước tính (đo `hrm_erp` 09/10, phương án ⭐ T1 = chỉ hàng `products.status = 1`)

> **Đổi 15/10:** bảng dưới là **luật cũ 1-2-3-4**. Số luật mới (nhóm chia sẻ 1·3·4, tự quản 2·7) đo bằng dry-run 15/10: chép
> `upp` 346.128 · `pcu` 57.688 · `pep` 4.014 · `pcc` nhận 56.736, TỔNG GHI 810.016 (Cty 2 chỉ 24 dòng chủ) — bảng đầy đủ ở
> `runbook-trien-khai.md` mục 3a.

| Đối tượng | Chủ (giữ/gán) | Bù chủ | Chép cho 3 công ty nhận | Tổng sau backfill |
|---|---:|---:|---:|---:|
| Hàng thuộc cụm, `status = 1` | Cty1 27.370 · Cty4 984 · Cty3 14 · Cty2 3 = **28.371** mã / **28.847** ĐVT | — | — | — |
| `upp` | 264.646 gán `company_id` (167.209 của hàng status 1) | **5.873** | 3 × 28.847 × 6 = **519.246** | **≈ 789.765** |
| `pep` tương lai (status 2, > 09/10) | 2.008 (Cty1 1.976 · Cty4 32) | — | **6.024** | +6.024 |
| `pcu` | **46.560** (mọi ĐVT, gồm hàng status 0) | — | 3 × 28.847 = **86.541** | **133.101** |
| `pcc` status 3 | ~28.371 dòng chủ (đa số INSERT) | — | 3 × 28.371 = **85.113** (≈1.100 UPDATE, còn lại INSERT) | ≈ 113.484 dòng có status |
| Giá đổi số vì hệ số ≠ 1 (đo trên dòng chép) | — | — | Cty2 1.338 · Cty3 1.332 · Cty4 90 dòng | |

Nếu T1 = chép **mọi** hàng, kể cả 17.512 hàng ERP đã xoá (`status = 0`): bù chủ 5.873 + 8.840 = ~14,7k, chép 3 × 46.559 ĐVT × 6 ≈ **838k**
dòng (`ton.md:24` ghi "~775k" là tính theo dòng giá Cty 1 × 3, chưa bù loại 5/6). Số này chốt lại bằng `--dry-run` sau khi trả lời T1.

### 3.5 Lệnh so khớp (chỉ đọc) — bắt buộc = 0 lệch trước khi bật

`php artisan product-price:compare {--company=1,3,4} {--csv=path}`, đặt ở HRM, đọc thẳng DB. **Đổi 15/10:** cặp cần so = (hàng × chủ)
cho chủ ∈ nhóm chia sẻ ∪ tự quản + (hàng × R) khi chủ và R cùng ∈ nhóm chia sẻ; HP/ETEK Green thiếu hàng chép không phải lệch. Với mỗi cặp:
1. Đủ bộ: 6 dòng `upp` + 1 `pcu` / ĐVT (BB1), `pcc.status = 3`.
2. **Giá hiệu dụng cũ** (= số ERP hiện cho người dùng công ty R hôm nay: dòng chủ × `pcc(H,R)` theo luật `getData`, gồm cả `pep`
   tương lai) **=** dòng mới của R, cho 6 loại × mọi ĐVT + giá hiệu lực. Nếu so ra lệch thì in CSV: mã, ĐVT, loại, công ty, cũ, mới.
3. `pcu(U,R)` 5 cột giá trị = `product_units` 5 cột của ĐVT đó (giá vốn chép nguyên, P7).
4. Đếm các nhóm lệch đã chấp nhận ở §3.6, in riêng. Không tính vào "0 lệch".

### 3.6 Lệch đã biết giữa các đường đọc ERP (không thể cùng giữ, vì ERP đang làm tròn 3 kiểu)

| Đường | Luật làm tròn hôm nay | Sau khi giá đã nướng hệ số | Số dòng lệch (đo 09/10, hàng status 1 cụm) |
|---|---|---|---|
| `getData` R1 (`P:1249-1257`) — số lên chứng từ | chỉ khi `k ≠ 1` | **= backfill** (gốc P1) | 0 |
| Popup `SC:461,984,1427,1815` | khi **có dòng** `pcc` (kể cả `k = 1`) | đọc nguyên ⇒ dòng `pcc` k = 1 có giá lẻ nghìn: popup đổi từ số tròn sang số lẻ (= số `getData`) | Cty2 220 · Cty3 214 · Cty4 15 ⇒ **T4** |
| `getPriceOfProducts` R4 (`PC:3569-3597`) | giá × k, rồi tròn nghìn nếu ≥ 1.000 (cả khi k = 1) | **giữ luật "≥ 1.000 thì tròn nghìn"**, chỉ bỏ nhân k ⇒ ra đúng số cũ | 0 (nếu bỏ luật này thì ~10.5k dòng/công ty đổi số) |
| `getPriceByUnitAndType` R2 (`P:1441-1452`) | **không** nhân k | đọc giá đã nướng ⇒ 26 chỗ lấy `.price` đổi số ở mã k ≠ 1 | đã chấp nhận ở **P10** |
| ĐVT thiếu loại 5/6 | `firstOrFail` lỗi | giá 0 | 5.873 dòng bù (§3.3) |
| `base_price` R3 (`P:1431`, kể cả `base_price` trong JSON getData) | **không** nhân k | đọc giá đã nướng ⇒ đổi số ở mã k ≠ 1 (cùng bản chất P10) | snapshot G3: 140 lượt / 451 mã × 4 Cty — ✅ user chấp nhận 10/10 |
| R4 khi giá < 1.000 có k ≠ 1 | giá × k, KHÔNG tròn (< 1.000) | = số getData (backfill đã tròn nghìn, vd 1 × 1.02 ⇒ 0) | snapshot G3: 242 lượt — ✅ user chấp nhận 10/10 |

### 3.7 Snapshot theo route (bằng chứng "mọi đường đọc ra đúng số")

ERP command `price:snapshot {--out=} {--sample=500}`: lấy mẫu cố định gồm mã có `pcc` k ≠ 1, mã k = 1, mã nhiều ĐVT, mã thiếu loại 5,
mã có giá hiệu lực. Với 4 công ty, gọi **chính hàm ERP**: `getData($cid)`, `getPriceByUnitAndType`, R4, 4 khối popup, `base_price`,
ghi ra JSON. Quy trình trên **bản sao DB**: (1) code cũ chụp *before* → (2) migrate M1–M2 + backfill + code mới + cờ bật chụp *after*
→ (3) diff chỉ được chứa các nhóm ở §3.6.

---

## 4. Lớp truy cập giá tập trung

### 4.1 Xác định công ty (P6)

**Thứ tự: tham số tường minh > công ty chứng từ > công ty người dùng.** Cron/queue luôn truyền tay. Không dùng global scope.

| Ngữ cảnh | Công ty |
|---|---|
| Lập chứng từ mới | `company_id` đang chọn trên form (= công ty người dùng khi form không cho chọn) |
| Mở lại / sửa / duyệt / hạch toán chứng từ | `company_id` của chứng từ (vd Ban điều hành Cty 1 duyệt HĐ SG ⇒ giá SG) |
| 5 bảng **không có `company_id`**: `contracts` (1 dòng), `project_quotations` (5), `order_requests` (0), `combo_campaigns` (5.030), `tmp_products` (1.957) — đo 09/10 | `created_by` → `employees.employee_info_id` → `employee_infos.company_id` (`app/Employee.php:85-88`), qua 1 helper chung `DocumentCompany::of($doc)` |
| HRM | chuẩn hoá về `CompanyHelper::pricingCompanyId($doc)` (`hrm-api/app/Helpers/CompanyHelper.php:52-59`). Bỏ "công ty hồ sơ NV" ở Finance/CustomerCare và `current_company_role` ở luồng đọc giá (`KH:31-34`) |
| Màn giá HRM (ghi) | `ProductService::currentCompanyId()` = `current_company_role` (`MD/Services/Product/ProductService.php:55-59`): công ty đang làm việc, cùng chuẩn với các màn hàng hoá 2-B/2-C |

### 4.2 API ERP — `App\Services\Product\ProductPriceService` (PHP 7.4 / Laravel 6)

| Hàm | Thay cho | Ghi chú |
|---|---|---|
| `unitsInfoFor(int $productId, int $companyId): Collection` | `P::getUnitsInfoAttribute :1404-1420` | ĐVT chung + phủ 13 cột từ `pcu` của công ty **trùng tên khoá cũ** + `prices` lọc `company_id` + `expected_prices` > hôm nay. Giữ hình dạng JSON ⇒ 0 view FE phải sửa (`KE:94-96`) |
| `dataFor(Product $p, int $companyId): array` | `getDataAttribute :1242`, `getData($cid) :1312` | bỏ nhân `pcc` khi cờ bật. Accessor cũ gọi `dataFor($p, công ty ND)` |
| `priceOf(int $pid, ?int $unitId, int $type, int $companyId): ProductUnitPrice` | `getPriceByUnitAndType :1441` | chữ ký cũ thêm tham số cuối `?int $companyId = null` (null = ND) ⇒ 69 chỗ gọi vẫn chạy. Thiếu dòng ⇒ `PriceNotFoundForCompany` (mã/công ty/loại) thay 404 câm |
| `basePriceOf(int $pid, int $companyId)` | `getBasePriceAttribute :1431` | |
| `costOf(int $pid, ?int $unitId, int $companyId): ?ProductCompanyUnit` | đọc `product_units.cost_price/buy_price` (R8) | P8: `null` = **thiếu** (xem T8) |
| Scope `ProductUnitPrice::scopeForCompany($q, int $cid)` + helper `PriceSql::joinPrices($query, 'pp', $cid)` | mọi `leftJoin('product_unit_prices as pp')` (R5, R7) | ép điều kiện `pp.company_id = ?` trong mệnh đề ON |
| Model mới `App\Model\Product\ProductCompanyUnit` | | |
| `PriceFlag::perCompany(): bool` (env `PRICE_PER_COMPANY`, config `price.php`) | | **Cờ lui (P12).** Tắt ⇒ chạy luật cũ: đọc dòng của **công ty chủ** (`company_id = products.company_id`) × `pcc` như hôm nay. Bật ⇒ đọc dòng công ty, không nhân |

### 4.3 API HRM — `MD/Services/ProductPrice/ProductPriceReader` (+ gom các join thô)

Bỏ "NULL = giá gốc": mọi hàm **bắt buộc** `int $companyId`. Thay ruột 4 helper `Modules/Human/Entities/TpProductUnitPrice.php`:
`getRetailPrices :29-60`, `getCostPrices :69-91`, `getUnitOptions :129-174`, `getUnitPrice :181-218`. **Gỡ** `TpProductCompanyCoefficient.php:39-79`
(hệ số). Thêm `ProductPriceSql::joinPrices($q, $alias, $companyId)` dùng chung cho Finance/CustomerCare (gợi ý sẵn ở
`ProductPrepickRequestController.php:174`). Cờ lui dùng cùng env `PRICE_PER_COMPANY` (ERP và HRM phải cùng giá trị, lệnh so khớp in ra cả hai).

### 4.4 Đường đọc phải chuyển

**ERP (≈ 55–65 file sửa + ~6 file mới, `KE` §1, §6.2):**

| Nhóm | Phạm vi | Cách sửa |
|---|---|---|
| R1 `getData`/`units_info` | lõi `P` (3 hàm) phủ 93 lời gọi AJAX / 71 view. **~37 file** gọi `->data` lúc nạp lại chứng từ (`KE:90`) | đổi thành `->getData($ct)` (công ty chứng từ) |
| R1.7 `units_info` trực tiếp | 31 chỗ / 20 file | tách `unitsOnly()` cho chỗ chỉ cần ĐVT. `WrServiceQuotation` dùng giá ⇒ truyền CT |
| R2 `getPriceByUnitAndType` | 69 chỗ / 42 file | thêm tham số. ~25 chỗ R2b/R2c/R2d (+ R2a ở luồng duyệt) phải truyền CT (`KE:104-111`) |
| R3 `base_price` | 13 chỗ / 9 file | 5–6 chỗ truyền CT |
| R4 `getPriceOfProducts` | `PC:3569-3597`, 13 view | bỏ nhân `pcc`, **giữ** luật ≥ 1.000 làm tròn (§3.6) |
| R5 popup | `SC` 7 khối (`:444-478, 967-1001, 1335-1444, 1798-1816`) + API HRM `searchProductStockBuyerApi` | join `pp.company_id = ?`, bỏ `CASE pcc`. **Lọc trạng thái đổi từ loại trừ sang chỉ nhận** (P4): `excludeCompanyUnavailableProducts :109-129` ⇒ `EXISTS pcc.status = 3 tại công ty`. Hàng không có dòng trạng thái thì không còn lọt vào popup |
| R6 hệ số | 17 chỗ (gồm 6 chỗ "kiểm lệch giá" R2d) | bỏ nhân khi cờ bật |
| R7 SQL lẻ | 15 file (`KE:150-168`) + màn còn mở `PC@getProductsAndPrices :2313` (màn L3), `@expectedPrices :2234` | thêm điều kiện công ty |
| R8 giá vốn | 10 file sống (`KE:173-187`): BG dự án / phân tích dự án / BG đại lý / HĐ đại lý / báo cáo lợi nhuận / lắp đặt / CRM | đọc `pcu` của CT. Giá vốn đọc sống ở hạch toán hỗ trợ ⇒ P8 |
| Đường ghi | cron 14:30 (§5.6), observer log thêm `company_id` (`KE:223`) | |
| Ngoài phạm vi | PTG `PriceCalculate::updatePriceWithApproval` (W1), duyệt hàng tạm `P::createRecord` (W2) | **chốt ở Phase 7/6** (P9) |

**HRM (20 file / 37 điểm, `KH` §3):**

| Nhóm | Điểm | Cách sửa |
|---|---|---|
| Human helper | H1–H6 `TpProductUnitPrice.php`, `TpProductCompanyCoefficient.php` | §4.3 |
| Assign | A1 `BomListController.php:405-410, 486-490, 563-567` · A2 `QuotationController.php:978-981` · A3 `QuotationService.php:961,1241,1690,2297,2930,3431` · A4 `:2763` · A5 `:2850-2851` · A6 `:5194-5235` (ngày đổi giá ERP — kẹp công ty) · A7 `QuotationImportService.php:951` · A8 `BomListService.php:2528`, `DetailBomListResource.php:38` · A9 `ErpProductSearchService.php:43,96` | truyền `pricingCompanyId($quotation)` |
| Finance | F1 `ProductImportRequestService.php:1447-1470` · F2 `ProductTransferRequestService.php:522-540` · F3 `:984-1000` · F4 `BorrowSellRequestService.php:446-505` · F5 `BorrowExportRequestService.php:370-376, 606-612` · F6 `PrepickApprovalRouteService.php:233-241` | `joinPrices(.., CT)`. ⚠️ F4 đổi nguồn giá ⇒ đổi kết quả câu "Sản phẩm có sự thay đổi về giá" |
| CustomerCare | C1 `ServiceService.php:1044-1060` · C2 `WrServiceQuotationService.php:597-605, 862-866` · C3 `WrQuotationService.php:94-100` | như trên |
| MasterData (ghi) | M1–M10 | §5.3 |

### 4.5 Test danh sách trắng (cả 2 repo) — chốt chặn rủi ro số 1 ("quên lọc công ty ⇒ nhân dòng im lặng", `KH:25-28`)

- PHPUnit `PriceReaderWhitelistTest`: quét `app/` (ERP) và `app/` + `Modules/` (HRM) theo regex
  `product_unit_prices|ProductUnitPrice|product_company_units|ProductCompanyUnit|product_expected_prices|ProductExpectedPrice|pu\.cost_price|->cost_price|product_company_coefficients.*coefficient`,
  so với tệp `tests/fixtures/price-readers.txt` (file + lý do, đã duyệt). File mới chưa duyệt ⇒ đỏ. File trong danh sách mà không
  còn khớp ⇒ đỏ (danh sách không phình).
- Mốc `@TODO-GIACTY` ở từng điểm §4.4 trong lúc làm. Xong thì `git grep @TODO-GIACTY` phải = 0.
- PHPUnit "2 công ty, cùng ĐVT, khác giá": với mỗi hàm §4.2/§4.3 và mỗi điểm nhóm Finance/CustomerCare, kiểm đúng giá **và đúng số dòng**
  (không nhân dòng). ERP chạy trên DB MySQL local (sqlite không đủ cho SQL MySQL, `KE:339`).

---

## 5. Đường ghi

### 5.1 Màn HRM "Cập nhật giá bán" — port L1 theo công ty

Nguồn hành vi: ERP `PC@updatePrice :2550-3135`, pseudo-code ở `KB:130-178`, phép tính FE T1–T11 ở `KF:125-137`.

**Cổng (BE, theo thứ tự, báo HTTP chuẩn HRM thay `success=false` HTTP 200 của ERP):**
1. Quyền **1657** ⇒ 403.
2. `products.status ∉ {0}` và hàng tồn tại. ⇒ 404/403.
3. Trạng thái công ty mình (`companyStatusSql(cty)` sau khi gỡ CASE, tức `pcc.status`):
   `1` Đang nhập thông tin ⇒ **423** "Hàng hoá đang nhập thông tin, chưa được nhập giá" (QC-5) ·
   `2` Chờ tính giá / `4` Ngừng kinh doanh ⇒ **423** (D3) · NULL ⇒ 403 "Hàng chưa dùng ở công ty" · `3` ⇒ qua.
4. **Không** kiểm hãng SX thuộc công ty, **không** kiểm `canEdit()` chủ (P5 bỏ QC-4).
5. Cờ gửi duyệt `is_approve`: đọc quy định của **công ty bộ giá** (công ty đang làm): `companies.is_company_price = 1` và
   (`is_all_brand = 1` hoặc `manufacture_id ∈ brand_ids`). ERP đọc công ty chủ (`PC:2648-2663`). Đổi vì P5: giá của Cty 2 phải đi
   người duyệt Cty 2 (tự chốt, hệ quả trực tiếp của P5/P13).

**Validate** = y ERP `PC:2551-2620` (`KB:96-118`), báo đồng thời mọi ô (memory), giữ câu chữ ERP. ĐMGG ngoài 0–100 thì báo đỏ, không
kẹp như ERP (T10). Không validate/không ghi `norm`, `note` (QC-8), `liquidation_sale_max_percent` (`KB:376`).

**Ghi** (1 ĐVT / 1 transaction, `lockForUpdate` dòng `pcu`, HĐ8 + K6):
- `upp` tìm theo (ĐVT, **công ty**, loại), thiếu thì sinh (BB3). Nhánh không duyệt: ghi giá/hệ số/ĐMGG, `*_wait_approve = 0`, 3 cờ = 0 (HĐ3).
  Loại 6 TMĐT BE tự tính khi cờ sửa tay tắt (HĐ4, `configs.coefficient_ecommerce_price`).
- `pep` theo HĐ6 (≤ 1 dòng tương lai, xoá dòng tương lai không gửi lên, không đụng status 1). Gán `created_by/updated_by` tường minh.
  Giá hiệu lực mới ở nhánh duyệt thì gán `price = 0, coefficient = 0` tường minh (`KB:184-187`).
- Giá vốn + lý do sửa giá ghi **`pcu` của công ty** (HĐ5 theo công ty). Không ghi 13 cột ở `product_units`.
- Nhánh duyệt: ghi `*_wait_approve` + cờ 1 cho trường thực sự đổi. Upsert `pa` theo (hàng, ĐVT, **công ty**) đúng định dạng ERP (`KB:166-176`),
  `pa.company_id` = công ty bộ giá, `department_id/part_id` theo người tạo. Gửi lại khi đang chờ ⇒ ghi đè đề xuất cũ (không tạo `pa` trùng).
- Lịch sử `catalog_histories` (D10, §6.4). Không ghi `product_versions/product_histories` (QC-9, HĐ10 bỏ).
- Thông báo D8 (§6.5).

### 5.2 Màn HRM "Duyệt giá bán" — port theo logic ERP (D5)

| Thao tác | Hành vi (nguồn ERP) | Khác ERP |
|---|---|---|
| Danh sách | `pa.company_id = công ty đang làm`, sắp `updated_at DESC` (`PAC:137-186`) | gate 1658 cả route đọc |
| Duyệt 1 / hàng loạt | áp **giá người duyệt gửi** cho giá hiện tại và giá hiệu lực. `effect_date < mai` ⇒ dời = mai. Cờ về 0. Giá vốn `pcu(công ty pa).cost_price = pa.cost_price`, `approve_comment = ''`. Xoá `pa` + `pap` (`PAC:188-274`) | hàng loạt = duyệt đơn lặp lại (sửa lỗi `PAC:448,473` — N56). **Không** chép `pa.unit_coefficient` (BB5). Kiểm `pa.company_id = cty` ở cả duyệt đơn (`PAC:200-202` bị comment). Giá đang chạy ≠ `price_old` (cron/PTG vừa đổi) ⇒ vẫn duyệt, trả cảnh báo kèm số (K9) |
| Không duyệt 1 / hàng loạt | cờ 1 ⇒ 2 ở giá/ĐVT/giá hiệu lực, `approve_comment` + `approve_time` vào `pcu`, xoá `pa`+`pap` (`PAC:276-412`). Lý do **bắt buộc** | |
| `products.status` | chỉ khi `pa.company_id = products.company_id` (P13) **và** `products.status = 2` (D1): Duyệt ⇒ 1, Không duyệt ⇒ 5. Hàng đang 1 giữ nguyên | công ty khác: xem **T3** |
| Bản ghi do PTG / hàng tạm ERP sinh | đọc được nguyên (cùng định dạng, `note/reason` NULL — `KB:254-256`) | ERP đang ghi `pa.company_id` = chủ. Phải đổi ở Phase 7/6 (P9) |
| Đã xử lý / không còn | 404 "Yêu cầu duyệt đã được xử lý" (K10) | |

### 5.3 `ProductWriteService` / lấy về / gỡ / xoá (đợt 2-C, HRM) — giữ BB1

| Điểm | Hiện tại | Sau |
|---|---|---|
| Tạo hàng — `writeUnits` `MD/Services/Product/ProductWriteService.php:322-339` | INSERT ĐVT `cost_price/buy_price = 0` + 6 dòng `upp` giá 0 **không công ty** | INSERT ĐVT (13 cột cũ = 0/NULL vì NOT NULL) + với **mỗi công ty đang có `pcc.status`** của hàng (lúc tạo: công ty tạo, status 1): 6 `upp` (giá 0, `company_id`) + 1 `pcu` (giá vốn 0) |
| Thêm ĐVT khi sửa (C7) | 6 dòng giá 0 | như trên, cho mọi công ty có trạng thái |
| Lấy về — `take` `:154-195` | chỉ ghi `pcc` | + sinh **bộ giá rỗng** của công ty lấy về (6 `upp` giá 0 / ĐVT + `pcu` giá vốn 0 — P7 "hàng lấy về mới ⇒ 0"). Đã có (từ backfill) thì `insertOrIgnore` bỏ qua |
| Gỡ — `release` `ProductLifecycleService.php:178-190` | không đụng giá | xoá `pep` → `pap`/`pa` → `upp` → `pcu` **của công ty gỡ** (V4: chỉ khi trạng thái = 1) |
| Xoá cứng `:108-131`, `:162-166` | xoá `pep`/`upp`/ĐVT mọi công ty, xoá `pa` | + xoá `pcu` |
| Luật suy trạng thái `MD/Entities/Product/Product.php:358-417` | `@TODO-BACKFILL` CASE `products.status = 1` | **gỡ CASE** ở `scopeWithCompanyStatus`, `companyStatusSql`, `ownerStatusSql` cùng lúc với backfill (B4). Phải gỡ cùng đợt với B4 |
| Model | `ProductUnit.php:24-35` fillable 13 cột · `ProductUnitPrice.php:22` thiếu `company_id` + 9 cột cờ | thêm `ProductCompanyUnit`, `ProductExpectedPrice`, `ProductApprove`, `ProductApprovePrice` (`KB:404-406`) |
| Seed e2e | `database/e2e_provision.php`, `BackfillQuotationProductUnitIdSeeder` | thêm `company_id` + `pcu` |

### 5.4 ERP: đường ghi còn lại

| Đường | Xử lý đợt này |
|---|---|
| PTG `PriceCalculate.php:332-760` (W1) | **Chốt ở Phase 7** (P9). Đợt này không sửa. ⚠️ Trên DB dev, sau M3 (NOT NULL) PTG ERP sinh dòng `upp` mới sẽ lỗi vì thiếu `company_id`. Chấp nhận, vì không lên production trước Phase 7 |
| Duyệt hàng tạm `P::createRecord :6929+` (W2) | **Chốt ở Phase 6**. Cảnh báo như trên |
| Cập nhật giá nhanh `PC@updatePrice` (W5) | chặn route (§5.7). Không sửa tạm (G8 cũ) |
| `manualUpdatePrices` (W6) | chặn + ẩn nút (D7) |
| Duyệt giá ERP (W7) | chặn route (§5.7) |
| Cập nhật giá theo hãng (W8) | đã khoá 2-D1 |
| Nhập kho cập nhật giá vốn (W9) | đang tắt (`ProductImport.php:1189`). Ghi chú: nếu ai bật lại thì phải ghi `pcu` |

### 5.5 Cron 01:00 `product:update_price`

Không đổi về công ty (`UpdateProductPrice.php:54-80` áp theo `unit_price_id` ⇒ đúng dòng của công ty). Thêm `company_id` vào nhật ký
(`:85`). Lỗi cũ "xoá cờ chờ duyệt của giá hiện tại khi áp giá hiệu lực" ⇒ N58, K9 xử lý phía duyệt.

### 5.6 Cron 14:30 `ResetProductPriceWhenZeroInventoryCommand` (P11)

- Hiện tại: chọn hàng `Product::where('company_id', $company->id)` + `product_cate` (`:82-91`), reset **mọi** dòng `upp` của mã (`:112-121`) và
  `product_units.cost_price/sale_max_percent_coefficient` (`:124-132`).
- Sau: chọn hàng **công ty có bộ giá** (`EXISTS pcu WHERE company_id = $company->id`), giữ lọc `product_cate` (N5 để sau, Q13). Tồn tính
  trên kho kế toán của công ty (giữ `:69-72`). Reset **chỉ** `upp.company_id = $company->id` và `pcu` của công ty đó.
- `Jobs/ResetProductPriceWhenZeroInventory.php` không được dispatch (code chết) ⇒ N63, không sửa.

### 5.7 ERP: route + lối vào phải chặn / đổi (D7 + 2 màn giá ERP)

| `web` | Route | Xử lý |
|---|---|---|
| :586 | GET `editPrices` | middleware `productMovedToHrm:price-edit` |
| :596 | POST `{id}/updatePrice` | middleware (403 JSON) |
| :587 | GET `approvePrices` | `productMovedToHrm:price-approve` (cũng là đích thông báo PTG/hàng tạm: `PriceCalculate.php:713-715`, `P:7341-7345`) |
| :588 | GET `approvePricesSearchData` | middleware |
| :589–592 | POST `approveSubmit`, `notApproveSubmit`, `approvesSubmit`, `notApprovesSubmit` | middleware (đóng luôn N29) |
| :593 | GET `approveExportExcel` | `price-approve` |
| :609 | GET `manualUpdatePrices` | middleware (D7) |
| giữ | `:594` `priceUpdating`, `:595` `getProductsAndPrices` (màn L3, chỉ đọc — thêm lọc công ty R7), `:608` `expectedPrices`, `price_logs`, PTG, `tmp_products/*`, `:46` `getPriceOfProducts`, `getData*` | danh sách trắng |

Kèm: `app/Http/Middleware/ProductMovedToHrm.php:28-36` thêm `'price-edit' => '/finance/product-prices'`, `'price-approve' => '/finance/product-price-approvals'` ·
`resources/views/layouts/topmenubar.blade.php:932` (Cập nhật giá nhanh) và `:2225` (DS chờ duyệt giá bán) đổi link sang HRM ·
`products/list.blade.php:39` nút "Cập nhật giá" ⇒ link HRM · `products/expectedPrices.blade.php:20` ẩn nút cập nhật thủ công ·
`HomeController.php:591, 598` 2 link dashboard ⇒ HRM (số đếm giữ, nhưng phải đếm theo `pa.company_id` = ND, R7) ·
`Observers/ProductWriteAuditObserver.php:24-29` bỏ `products.updatePrice`, 4 `*Submit`, `product.manualUpdatePrices` khỏi danh sách trắng.

### 5.8 PTG / hàng tạm

**Chốt ở Phase 7 (PTG) / Phase 6 (hàng tạm).** Đợt này chỉ (1) đảm bảo màn Duyệt HRM đọc được `pa` do 2 nguồn này sinh, (2) đổi đích
link thông báo ERP sang màn HRM. Không thiết kế ERP ghi giá theo công ty nào trong lúc chờ (P9b, ghi chú "lên production một lần").

---

## 6. Màn HRM

### 6.1 Bố cục (mockup chốt trước theo D12: `gia-theo-cong-ty/mockup-gia.html`)

Khung chung: page `layout: 'default-sidebar'` (finance là hub, `components/subsystem-menu/hub.js:35`), mixin `PageTitleMixin`,
`filterStateMixin`, `CheckPermission`. Style V2 phải **đo `getComputedStyle` từ app đang chạy**, không chép CSS mockup khác (memory).

**Màn 1 — Cập nhật giá bán** `/finance/product-prices` (gate 1657):
- Bộ lọc `V2BaseSmartFilterPanel`: ô tìm mã/tên/model · cây phân loại 4 cấp (`ProductListPage.vue:20-33`) · Hãng SX (mọi hãng, P5) ·
  Thương hiệu · Trạng thái duyệt (Tất cả / Chờ duyệt / Không duyệt) · Tồn kho (Tất cả / Còn / Hết — D6).
- Phạm vi: chỉ hàng `pcc.status = 3` ở công ty đang làm (D2), sắp xếp theo whitelist cột (K11), 20 dòng / trang.
- Bảng nhập tại chỗ, mỗi hàng là 1 khối rowspan. Bố cục theo `KF:233-263`: tiêu đề 1 tầng, nowrap. Cột Tên/ĐVT dính trái. Bảng có
  vùng cuộn riêng (`.content-page overflow:hidden` giết sticky). Cột: Tên (✎ Lý do sửa giá, 📐 công thức lắp ráp, "Ghi chú không duyệt")
  · ĐVT (chọn) · Mã (+ công khoán, ghi chú HH: chỉ đọc) · Model · Hãng · Tồn kho (công ty mình — xem **T6**) · Giá vốn (badge) · Loại giá ·
  Giá hiện tại · Hệ số · Giá công thức · Giá mới · ĐMGG · Hiệu lực · 💾 Lưu / 🕘 Lịch sử. Đủ 6 loại giá, thiếu thì FE hiện dòng rỗng.
- Lưu từng khối (hàng × ĐVT đang chọn). Đổi ĐVT / trang / bộ lọc khi khối đang bẩn ⇒ `$confirm` "Thông tin chưa lưu". Rời route ⇒ `unsavedChangesMixin`.
- Phép tính T1–T11 (`KF:125-137`) đặt ở `utils/productPriceModel.js` (hàm thuần, dùng chung 2 màn).

**Màn 2 — Duyệt giá bán** `/finance/product-price-approvals` (gate 1658):
- Bộ lọc: tìm mã/tên/model · cây phân loại · Hãng SX · Người cập nhật. Nút **Xuất Excel** trên header bộ lọc (D11).
- Khối rowspan = 1 + số dòng giá đổi: ☐ · # · Tên (+ lý do) · ĐVT · Mã · Giá vốn đề xuất · Loại · Giá cũ · **Hệ số / Giá mới / ĐMGG mới**
  (sửa được, có chênh lệch ±) · Hiệu lực · Người cập nhật · Thời gian · ✓ Duyệt / ✕ Không duyệt / 🕘.
- Tick ≥ 1 ⇒ thanh hàng loạt "Đã chọn N yêu cầu [Duyệt] [Không duyệt] [Bỏ chọn]".

**3 popup:**
1. **Lịch sử giá** (D10): vỏ `V2BaseModal` + `SystemInfoSection` (`components/modal/SettingHistoryModal.vue`), endpoint riêng.
2. **Lý do không duyệt**: `$confirm({ danger, showInput, inputLabel: 'Lý do không duyệt' })` bắt buộc nhập (button-convention 6c).
3. **Xác nhận Duyệt** (đơn / hàng loạt): `$confirm` gọi tên mã + hệ quả ("Giá mới áp dụng ngay; giá hiệu lực đã qua ngày dời về ngày mai").
   Phụ (chỉ đọc, 1–1 ERP): popup công thức lắp ráp.

Đo DOM bắt buộc khi kiểm (`KF:325-336`): `thead tr` = 1 · rowSpan ô Tên = số `tr` khối · sticky trái/trên không đè · đúng 1 vùng cuộn dọc ·
ô khoá nền `rgb(241,245,249)` · định dạng số · 1 request / lần Lưu · footer phân trang không đè bảng · console sạch ở cả ca có quyền và không quyền.

### 6.2 Quyền (đề xuất id — kiểm 09/10)

| id | name (guard `api`, `group` 'Hàng hoá', `type` 9) | Gate |
|---|---|---|
| **1657** | `Cập nhật giá bán hàng hoá` | menu + page + `GET list/stock/options` + `PUT` lưu + xem giá vốn trên màn + xem lịch sử |
| **1658** | `Duyệt giá bán hàng hoá` | menu + page + list + 4 thao tác + xuất Excel + xem lịch sử |

Kiểm trùng 09/10:
- Seeder nhánh chung (HEAD): 1650, 1651, 1652, 1653, 1655, 1660, 1661, 1670–1675.
- `origin/develop`: 1676–1698.
- `origin/gop_db`: 1676–1678.
- Quét **mọi nhánh remote** của `hrm-api`: không nhánh nào dùng 1656–1669 hay 1699–1719.
- DB `hrm_erp`: 1652, 1653, 1655, 1660, 1661, 1670–1678, không có 1657/1658.
- Trùng tên: không. ERP guard `web` có `Cập nhật nhanh giá hàng hóa` (100063), `Duyệt giá hàng hoá` (100983), tên khác nên không đụng.
- 1654 (Xuất excel DS hàng hoá) và 1656 (Chính sách giá nội bộ) đang giữ chỗ.

Seed: chỉ thêm 2 dòng. **Không chạy cả `PermissionsTableSeeder`** (truncate cả bảng — memory). `role_has_permissions` cần `company_id`.
Kiểm `uniq -d` + DB ngay trước khi seed (memory "trùng id khi merge nhánh dài"). Super admin không bypass. Menu `isShow` theo tên quyền.
Endpoint BE không quyền ⇒ 403. Nhớ toast 403 của interceptor (memory) ⇒ page gate trước khi gọi API.

### 6.3 Menu Finance (D9 — đề xuất, chốt cuối ở mockup)

Hiện `components/subsystem-menu/finance.js` không có nhóm giá. Header `:24` ghi *"ERP có nhóm 'Quản lý giá - CTKM' nhưng sheet gộp xếp các màn
đó sang phân hệ khác -> không kéo về"*. Chốt D9 đè lên ghi chú này, nên phải sửa comment cùng lúc.

```js
// hubGroup MỚI bám đúng tên nhóm ERP (topmenubar.blade.php:932-937), đặt sau 'Kế toán công nợ', trước 'Danh mục'
{ label: 'Giá bán', hubGroup: 'Quản lý giá - CTKM', hubIcon: 'ri-price-tag-3-line', isMenuCollapsed: false, subItems: [
    { label: 'Phiếu tính giá' },                                   // xám — Phase 7
    { label: 'Cập nhật giá bán', link: '/finance/product-prices', isShow: ['Cập nhật giá bán hàng hoá'] },
    { label: 'Duyệt giá bán', link: '/finance/product-price-approvals', isShow: ['Duyệt giá bán hàng hoá'] },
    { label: 'Cập nhật giá theo hãng' },                           // xám — N36
    { label: 'Trạng thái cập nhật giá', erpPath: '/admin/products/expectedPrices' },     // N34
    { label: 'Hàng sắp điều chỉnh tăng giá', erpPath: '/admin/products/priceUpdating' }, // N34
] },
// lối phụ ở nhóm 'Chờ duyệt' (cuối file, :526+), như ERP đặt "DS hàng hoá chờ duyệt giá bán" ở top menu Chờ duyệt
{ label: 'Giá bán chờ duyệt', hubGroup: 'Chờ duyệt', icon: 'ri-price-tag-3-line', isMenuCollapsed: false, subItems: [
    { label: 'Hàng hoá chờ duyệt giá bán', link: '/finance/product-price-approvals', isShow: ['Duyệt giá bán hàng hoá'] },
] },
```

Nhóm có 6 mục, đạt `NAV_MIN = 5` (`components/sale/SaleMenuHub.vue:111`), nên không phải hạ ngưỡng. Khai `subItems`, không `children`.
Không đổi nhãn mục cũ. "Nhật ký cập nhật giá" (ERP đọc file log trên máy chủ ERP) để ngoài, vì không có đường `erpPath` ổn định. Đường ERP
`erpPath` kiểm lại lúc làm mockup.

### 6.4 Lịch sử giá (D10, QC-9) — không migration

`catalog_histories` không có cột công ty. Chốt kỹ thuật: `table_name = 'product_prices'`, **`table_id = product_company_coefficients.id`**
(dòng hàng × công ty, duy nhất theo cặp, luôn có khi có trạng thái — BB1). Action `update` · `submitted` · `approved` · `rejected` (`note` =
lý do). Dữ liệu dạng bảng ĐVT × loại giá (giá, hệ số, ĐMGG, giá hiệu lực + ngày), giá vốn theo ĐVT (skill entity-history §3). Endpoint
riêng `GET master-data/product-prices/{product}/histories` gate 1657 **hoặc** 1658. **Không** thêm `product_prices` vào whitelist route
chung `catalog-histories/{table}/{id}`, vì route đó không gate mà log lại có giá vốn (`KB:39-40`, N64).

### 6.5 Thông báo 2 chiều (D8, skill notification-convention)

| Sự kiện | Người nhận | Nội dung (≤ 120 ký tự, tên in đậm `<b>`) | Deep-link |
|---|---|---|---|
| Gửi đề nghị (nhánh duyệt) | NV có quyền 1658 **của `pa.company_id`** (`sendToAllNotification`) | `[GIA] Chờ duyệt: <b>{mã} – {tên ≤50}</b>. Người đề nghị: {tên}` | `/finance/product-price-approvals?approve_id={pa.id}` |
| Đã duyệt | người đề nghị (`pa.updated_by`) | `[GIA] Đã duyệt: <b>{mã} – {tên}</b>. Giá mới áp dụng từ {ngày}` | `/finance/product-prices?product_id={id}` |
| Không duyệt | người đề nghị | `[GIA] Từ chối: <b>{mã} – {tên}</b>. Lý do: {ghi chú}` | `/finance/product-prices?product_id={id}&status=2` |
| `pa` do PTG / hàng tạm ERP sinh | — | HRM **không** bắn thêm. ERP vẫn báo cho quyền ERP, link đổi sang HRM qua middleware đích `price-approve` | |

Ghép chuỗi qua 1 helper (cắt 50/120). Deep-link mất `pa` (đã xoá sau khi xử lý) ⇒ page mở ra không thấy thì toast "Yêu cầu đã được xử lý".

### 6.6 Excel màn Duyệt (D11)

`MD/Exports/ProductApproveExport.php` + blade, theo skill export-excel: letterhead công ty, số là số thật, có ngăn nghìn, cột đủ rộng.
Cột như ERP `PAC:514-561` (bỏ Loại HH/Tính chất cũ, thêm cây phân loại mới). Cùng bộ lọc màn. Gate 1658 (1654 chưa tồn tại trong DB). Tải
trực tiếp từ server `?token=` + `Content-Disposition` (memory: Safari không nhận blob).

### 6.7 Lọc tồn thật theo công ty (D6)

Tồn = `SUM(accounting_stocks.qty) WHERE stock_id IS NOT NULL AND accounting_warehouse_id IN (kho kế toán của công ty đang làm) AND product_id IN (trang)`.
Định nghĩa kho theo công ty y cron 14:30 (`AccountingWarehouse::where('company_id')`). Lọc "Còn/Hết" = `EXISTS`/`NOT EXISTS` cùng điều kiện, có
index `product_id` sẵn. Cột hiện chia `unit_coefficient` của ĐVT đang chọn ở FE như ERP. Endpoint tồn 1 mã khi đổi ĐVT (K12). ERP gốc: tổng
mọi công ty (`P:2391-2430`) ⇒ **T6**.

---

## 7. Chia đợt con

Nhánh HRM: mỗi đợt mở nhánh con **từ `feat/chuyen-doi-hang-hoa`**, xong merge về nhánh chung. Đợt sau checkout từ nhánh chung (memory).
Không merge `gop_db`. Làm trong worktree `wt-chuyen-doi-hang-hoa` (api 8031 / Nuxt 3031).

Nhánh ERP: **đề xuất nhánh con `feat/gia-cty-erp` từ `feat/2d1-erp-khong-loi`**, không từ `gop_db`. Lý do: cần middleware
`ProductMovedToHrm` + popup N53 của 2-D1, và `feat/2d1-erp-khong-loi` đang đóng vai nhánh chung ERP của feature. Merge về
`feat/2d1-erp-khong-loi`, worktree `wt-erp-2d1`.

DB: **xem T5**. Backfill sinh dòng giá thứ 2 cho mỗi ĐVT, nên mọi code cũ (nhánh khác, session khác) đọc `hrm_erp` chung sẽ nhân dòng ngay.

| Đợt | Nội dung | Repo / nhánh | Phụ thuộc | Nghiệm thu |
|---|---|---|---|---|
| **G0** Mockup | `mockup-gia.html` 2 màn + 3 popup, JS T1–T11, menu Finance (D9, D12) | tài liệu | — | user chốt bố cục + vị trí menu. Đo style từ app |
| **G1** Nền CSDL + backfill | M1, M2, M3 · model `ProductCompanyUnit` · lệnh `backfill-company` + `compare` · gỡ `@TODO-BACKFILL` (B4) | hrm-api `feat/gia-cty-g1-nen` | G0 không chặn | `--dry-run` khớp §3.4 (sau khi trả lời T1) · `compare` = 0 lệch ngoài §3.6 · M3 tự chặn khi chưa backfill · PHPUnit idempotent (chạy 2 lần, số dòng không đổi) |
| **G2** Đọc + ghi HRM | `ProductPriceReader` + 20 file §4.4 HRM · `ProductWriteService`/take/release/hardDelete §5.3 · test danh sách trắng HRM · cờ `PRICE_PER_COMPANY` | hrm-api `feat/gia-cty-g2-doc-hrm` | G1 | test 2 công ty khác giá cho mọi điểm · whitelist xanh · e2e hàng hoá 2-C cũ (lifecycle/take/form/read) xanh lại. BB1 sau tạo/lấy về/gỡ/xoá |
| **G3** Đọc + ghi ERP | `ProductPriceService` + R1–R8 (≈55–65 file) · popup chỉ nhận status 3 · cron 14:30 · `price:snapshot` · whitelist ERP | ERP `feat/gia-cty-erp` | G1 (song song G2 được) | snapshot before/after trên bản sao DB: diff chỉ gồm §3.6 · PHPUnit resolver công ty (5 bảng không `company_id`) · Playwright ERP: popup × 4 công ty, giá dòng chứng từ sau khi chọn hàng, hạch toán hỗ trợ 1 HĐ dự án + 1 HĐ đại lý |
| **G4** Màn Cập nhật giá bán | BE list/stock/update/histories + FE màn 1 + popup lịch sử + quyền 1657 + menu | hrm-api + hrm-client `feat/gia-cty-g4-cap-nhat` | G2, G0 | PHPUnit ~30 ca (`KB:433-441` sửa theo công ty) · Playwright đo DOM §6.1 · sửa/thêm e2e `product-prices*.spec.ts` (ca có quyền + không quyền + công ty khác + Đang nhập thông tin 423) |
| **G5** Duyệt giá bán | nhánh gửi duyệt của G4 + màn 2 + 2 popup + Excel + thông báo + quyền 1658 + D4 (Quy định `RegulationTabRegistry.php:384-400` option `manufactures`) | như G4 `feat/gia-cty-g5-duyet` | G4 | PHPUnit nhánh duyệt + duyệt (`KB:442-448`) · e2e A1–A5 (`KF:319-323`) · thông báo đúng người/đúng link · đọc được `pa` định dạng PTG |
| **G6** ERP chặn + nghiệm thu tổng | route §5.7 + middleware đích + link menu/dashboard + observer · chạy lại toàn bộ `compare` + `snapshot` + bộ e2e liên quan | ERP `feat/gia-cty-erp` + cả 2 | G3, G5 | route chặn trả trang "đã chuyển" + link đúng · runbook triển khai 1 lần (§2.4) chạy thử trọn trên bản sao DB |

Thứ tự đề xuất: G0 ∥ G1 → G2 ∥ G3 → G4 → G5 → G6. Mỗi đợt hỏi "làm" riêng, nêu repo · nhánh · file/bảng · có chạy migration/seeder vào DB nào.

**Rủi ro:**

| # | Rủi ro | Giảm |
|---|---|---|
| R-a | Sót 1 đường đọc ⇒ nhân dòng / `first()` lấy giá công ty bất kỳ, im lặng | whitelist 2 repo + test 2 công ty + snapshot route |
| R-b | ~525k dòng mới, query nóng (`getData` 93 lời gọi, popup 338 màn) chậm | UNIQUE (ĐVT, công ty, loại) làm index phủ. Đo `EXPLAIN` popup trước/sau ở G3 |
| R-c | DB dev dùng chung bị backfill làm hỏng nhánh khác | T5 |
| R-d | Cờ lui: sau khi bật, giá do công ty nhận sửa sẽ vô hình khi tắt cờ (cờ tắt đọc dòng chủ) | ghi rõ ở runbook. Lui chỉ dùng trong ngày bật |
| R-e | PTG/hàng tạm ERP gãy trên DB dev sau M3 | chấp nhận (P9). Phase 7/6 làm lại |
| R-f | Giá vốn đọc sống ở hạch toán hỗ trợ (`KE:236-245`) đổi nguồn ⇒ HĐ đang chờ duyệt đổi số | backfill chép nguyên giá vốn chủ ⇒ cụm không đổi. P8 + T8 |
| R-g | Hệ số đọc ở 2 nơi (ERP + HRM) bỏ không đồng thời | cùng env cờ. `compare` in giá trị cờ của cả 2 |

---

## 8. Việc ngoài luồng phát hiện (đánh số tiếp theo `2c-ghi/chot.md`, chỉ liệt kê, không vá)

| # | Việc | Nguồn |
|---|---|---|
| N54 | ERP làm tròn giá × hệ số theo 3 luật khác nhau: `getData` chỉ khi k ≠ 1 (`P:1249`), popup khi có dòng `pcc` (`SC:461`), R4 khi ≥ 1.000 kể cả k = 1 (`PC:3569-3597`) ⇒ cùng 1 mã, 3 màn ra 3 số | đo 09/10 |
| N55 | Ô lọc Tồn kho màn giá ERP là ô chết (`PC:2499-2501` comment) | `KB:43` |
| N56 | Duyệt hàng loạt ERP: FE gửi `price`, BE đọc `prices` (`PAC:448`); giá hiện tại ghi giá đề nghị (`PAC:473`); `dd($e)` trong catch (`PAC:270, 503`) | `KB:236`, `KF:36-39` |
| N57 | `manualUpdatePrices` không lọc `flag` (`PC:2243`) ⇒ áp được giá hiệu lực đang chờ duyệt (giá 0) | `KB:46` (chặn ở D7) |
| N58 | Cron 01:00 đặt 3 cờ chờ duyệt của giá hiện tại về 0 khi áp giá hiệu lực ⇒ `pap` mồ côi, duyệt sau ghi đè giá cron vừa áp | `KB:265-267` |
| N59 | `getProductsAndPrices` nhận cột sắp xếp tự do từ request (`PC:2518-2521`). Route còn giữ cho màn L3 | `KB:75` |
| N60 | `ProductExportsController.php:766` truyền `unit_coefficient` vào chỗ `unit_id` của `getPriceByUnitAndType` | `KE:344` |
| N61 | `getData`/`units_info` trả `cost_price`/`buy_price` cho mọi màn chứng từ, kể cả người không có quyền xem giá vốn (R1.1). Sau đợt này giá trị là của `pcu` công ty, nhưng vẫn lộ | `KE:345` |
| N62 | `WrServiceQuotation` lấy `units[0]->prices[0]` theo **thứ tự**, không theo `price_type_id` | `KE:346` |
| N63 | `Jobs/SyncProductUnitPricesToCrm.php`, `Jobs/ResetProductPriceWhenZeroInventory.php` không được dispatch (code chết) | `KE:347` |
| N64 | HRM route chung `catalog-histories/{table}/{id}` không gate quyền (`hrm-api/routes/api.php:37-48`) | `KB:39-40` |
| N65 | 13.662 dòng giá hiệu lực `status = 2` đã quá ngày (cron bỏ qua mãi) + 6 ĐVT / 5 dòng giá / 6 giá hiệu lực mang cờ chờ duyệt mồ côi | `KH:145`, `KB:269-273` |
| N66 | 3 bảng chứng từ không `company_id` gần như rỗng: `contracts` 1 dòng, `project_quotations` 5, `order_requests` 0. Code đọc giá trên chúng nên rà xem còn sống không, trước khi đầu tư helper công ty | đo 09/10 |
| N67 | 2 nơi ghi cờ duyệt giá `companies.is_company_price/brand_ids`: màn Quy chế công ty ERP (`CompaniesController.php:436-449`) và màn Quy định HRM | `KB:247-252` |
| N68 | `getPriceByUnitAndType`/`base_price` dùng `firstOrFail` ⇒ lỗi 404/500 câm khi thiếu dòng (đợt này thay bằng exception có tên, nhưng chỗ gọi chưa bắt) | `KE:21`, `P:1431-1452` |
| N69 | Cty 8 đang bật `is_new_company = 1, is_new_brand = 1` (duyệt hàng mới) trong khi Cty 8 sẽ bị loại bỏ (P2c) ⇒ tắt cờ khi loại công ty | `KB:29-31`, đo 09/10 |
| N70 | Cty 5/6/8 "sẽ loại bỏ": sau khi popup chỉ nhận hàng Đang kinh doanh, người dùng 3 công ty này không chọn được hàng nào. Cty 8 hôm nay đang bán 566 mã (đã chấp nhận ở P2c) ⇒ cần mốc tổ chức tắt tài khoản / chứng từ dở dang | `ton.md:24` |

---

## 9. Tồn còn lại (hỏi LẦN LƯỢT, mỗi câu ⭐ + hệ quả)

| # | Câu | ⭐ Đề xuất | Hệ quả từng đáp án |
|---|---|---|---|
| **T1** | Cụm 1-2-3-4 chép giá + sinh "Đang kinh doanh" cho **hàng nào**? `ton.md` ghi "~775k dòng" (= mọi dòng Cty 1 × 3), tức tính cả **17.512 hàng ERP đã xoá** (`products.status = 0`) | ⭐ **chỉ hàng `products.status = 1`** (28.371 mã / 28.847 ĐVT ⇒ ~525k dòng giá mới) | ⭐: không tạo trạng thái "Đang kinh doanh" cho hàng đã xoá. Khớp L3 (chỉ lấy về hàng status 1) và popup (lọc `status != 0`). Chép mọi hàng: ~838k dòng. Hàng đã xoá thành "Đang kinh doanh" ở 3 công ty nhận nhưng không ở công ty chủ (vì chủ suy theo status 1), nên trạng thái lệch giữa các công ty |
| **T2** | "Hàng Cty 1 quản lý thì **LUÔN** sao chép giá cho 2/3/4": chỉ là **backfill một lần** ngày bật, hay **luật thường trực** (hàng mới / giá mới của 1 công ty trong cụm tự lan sang 3 công ty còn lại)? | ⭐ **một lần** (backfill). Sau đó mỗi công ty tự quản giá (P5). Hàng mới đi đường lấy về (2-C2) + Tính giá (Phase 7) | ⭐: đúng P5/§26 "công ty lấy về tự tính giá". Thường trực: phải thêm hook ở tạo hàng HRM, PTG, duyệt, cron 01:00 để lan giá × hệ số. Hệ số lại sống tiếp, trái P10/TĐ#8. Sửa giá ở Cty 2 rồi bị Cty 1 đè |
| **T3** | Trạng thái theo công ty khi duyệt (P13 "công ty khác chỉ đổi trạng thái theo công ty mình") + 7 hàng `products.status` 2/5 hiện có | ⭐ (a) Backfill **không** sinh dòng trạng thái cho hàng status 2/5 (giữ luật suy hôm nay). (b) Công ty chủ duyệt 2→1 thì **ghi luôn `pcc` chủ = 3** (không thì hàng duyệt xong vẫn vô hình sau khi gỡ CASE suy ra). (c) Công ty khác: Duyệt khi trạng thái công ty mình = 2 (Chờ tính giá) ⇒ 3. Không duyệt ⇒ giữ 2. Chi tiết chốt ở Phase 7 | (a) 7 mã (1 chờ duyệt `MNSG-GPO12CE` + 6 không duyệt) biến khỏi popup ERP ở mọi công ty khi popup chuyển sang "chỉ Đang KD". Hôm nay popup còn hiện chúng (lọc `status != 0`). Sinh status 3 cho chúng: hàng bị Không duyệt lại bán được. (b) Không ghi: luồng duyệt hàng mới Phase 6 ra hàng "không trạng thái". (c) Hiện chưa có nguồn nào sinh `pa` cho cặp đang ở trạng thái 2, nên chỉ áp từ Phase 7 |
| **T4** | Popup ERP hiện **tròn nghìn** cả khi hệ số = 1 (có dòng `pcc`), còn `getData` (số lên chứng từ) giữ số lẻ. P1 chốt "làm tròn như getData" | ⭐ chấp nhận: popup hiện đúng số `getData` (Cty2 220 · Cty3 214 · Cty4 15 dòng đổi hiển thị) | ⭐: popup = chứng từ, hết lệch N54 ở popup. Giữ số popup cũ: phải lưu thêm luật làm tròn riêng cho popup, mà dòng `pcc` sau backfill đã mất nghĩa "có hệ số" |
| **T5** | DB chạy migration + backfill trong lúc dev | ⭐ **bản sao riêng** (vd `hrm_erp_giacty`), worktree G1–G6 trỏ vào đó. `hrm_erp` chung chỉ nhận khi cả feature xong | ⭐: không làm hỏng nhánh/session khác (code cũ không lọc công ty sẽ nhân dòng ngay khi có dòng thứ 2). Chạy thẳng `hrm_erp`: mọi session ERP/HRM khác (gop_db, develop) thấy popup nhân dòng, giá bừa |
| **T6** | Cột "Tồn kho" ở màn Cập nhật giá: tồn **công ty mình** (khớp ô lọc D6) hay **tổng mọi công ty** (như ERP `P:2391-2430`)? | ⭐ công ty mình | ⭐: cột và ô lọc cùng một định nghĩa. Mọi công ty: y ERP, nhưng lọc "Hết tồn" có thể hiện hàng mà cột vẫn > 0 |
| **T7** | Backfill chép 13 cột `pcu` cho công ty nhận: chỉ 5 cột giá trị (giá vốn, giá mua ngoài, hệ số định mức, ĐMGG thanh lý, cờ theo giá niêm yết), **không** chép 8 cột duyệt/vết | ⭐ như vậy | ⭐: yêu cầu duyệt/ghi chú không duyệt thuộc công ty đã gửi, không nhân sang 3 công ty. Chép cả 13: 3 công ty nhận hiện badge "Không duyệt" của Cty 1 |
| **T8** | P8 "thiếu giá vốn thì chặn duyệt hạch toán": "thiếu" là **không có dòng `pcu`**, hay **giá vốn = 0**? Hôm nay ~21,7k/46,6k ĐVT có giá vốn 0 | ⭐ thiếu = **không có dòng `pcu`** của công ty chứng từ. 0 vẫn là giá trị hợp lệ như hôm nay | ⭐: HĐ đang chạy với giá vốn 0 không bị chặn đột ngột. Nhưng với BB1 hầu như không có ca "không có dòng", nên chặn gần như không bao giờ xảy ra. Thiếu = 0: chặn ngay hàng nghìn HĐ có mã giá vốn 0, và mọi hàng lấy về mới (P7 = 0) cho tới khi nhập giá vốn |

---

*Kèm mức độ tin cậy:* `file:dòng` ERP/HRM lấy theo HEAD ghi ở đầu file. Số liệu §3.3–§3.6, §6.2 và N66/N69 đo lại 09/10 trên `hrm_erp`
(chỉ SELECT). Số còn lại trích từ khảo sát nguồn (ghi mã nguồn ở từng dòng).

### Trả lời §9 (09/10/2026)

- **T1** ✅ chỉ hàng `products.status = 1` (28.371 mã / ~525k dòng giá).
- **T2** ✅ chép MỘT LẦN ngày bật; sau đó mỗi công ty tự quản giá, hệ số bỏ hẳn.
- **T4** ✅ chấp nhận 449 dòng popup đổi hiển thị (popup = số getData).
- **T5** 🔄 user chọn **chạy thẳng `hrm_erp` chung** (không bản sao). ⚠️ Hệ quả đã nêu: session/nhánh khác chưa lọc công ty sẽ thấy nhân dòng
  giá ngay khi có dòng công ty thứ 2 ⇒ khi tới G1 phải: sao lưu `hrm_erp` trước, báo user thời điểm chạy backfill, cân nhắc chỉ chạy backfill
  khi G2/G3 (lọc công ty) đã sẵn; vẫn xin phép riêng trước khi chạy migration/backfill.

- **T3** ✅ 7 mã status 2/5 không sinh trạng thái (biến khỏi popup); công ty quản lý duyệt 2→1 ghi luôn trạng thái Đang kinh doanh của công ty đó; duyệt ở công ty khác chốt ở Phase 7.
- **T6** ✅ cột Tồn = tồn công ty mình.
- **T7** ✅ chỉ chép 5 cột giá trị, không chép 8 cột duyệt/vết.
- **T8** ✅ "thiếu giá vốn" = không có dòng `product_company_units` của công ty chứng từ; giá vốn 0 vẫn hợp lệ.

**09/10/2026: §9 chốt đủ T1–T8 ⇒ design KHÔNG còn tồn. Bước kế: G0 mockup (tài liệu, không cần xin phép code); G1+ phải hỏi "làm" riêng kèm phạm vi.**

### Chốt từ mockup G0 (09/10/2026)

- **Q1** ✅ màn Duyệt giá: không có quyền 1092 ⇒ ẩn CẢ Giá vốn LẪN Hệ số (giá = hệ số × giá vốn suy ngược được); BE không trả 2 trường.
- **Q2** ✅ công ty tắt duyệt giá khi còn yêu cầu chờ ⇒ Lưu áp giá mới + xoá yêu cầu chờ cũ (cờ chờ duyệt về 0).
- Thứ tự cột (U1–U18 trong `mockup-gia.html`): **user đang xem, góp ý sau**.
- ✅ **09/10 user "đồng ý, chốt mockup"** — giữ thứ tự cột U1–U18 như mockup; màn Cập nhật giá bán: quyền 1657 gồm xem + nhập giá vốn công ty mình (không áp luật ẩn theo 1092). Mockup `mockup-gia.html` là bản chốt.

### Đổi 10/10/2026 — BỎ CỜ, đổi DB dev

- 🔴 User bác cờ `PRICE_PER_COMPANY` (G2): feature làm ở local, chỉ lên production khi xong hết phase ⇒ **không cờ, không đường lui**; giá LUÔN
  đọc theo công ty ở cả HRM và ERP. Bỏ R-d, R-g, lệnh `complete-sets`; §4.3 "cờ lui" hết hiệu lực. Đợt **G2b** gỡ cờ.
- **T5 đổi:** chép giá thật + compare + M3 chạy trên **bản sao riêng `hrm_erp_giacty`**, ngay sau G2b; worktree HRM (`wt-chuyen-doi-hang-hoa/hrm-api`)
  + worktree ERP (`wt-erp-2d1`) trỏ sang bản sao. `hrm_erp` chung giữ nguyên (đã có M1/M2 — vô hại).
- **N71** (compare loại cặp HRM sinh ra) làm trong G2b. **N72** ✅ backfill chép 4 ô quản trị từ `products` vào dòng `pcc` chủ + công ty nhận.
- Nhánh chung hrm-api chưa push (user 10/10).

### Đổi 15/10/2026 — luật chép giá: nhóm chia sẻ 1·3·4, tự quản 2·7

- Chốt user 15/10 (`cum-gia-1510-brief.md`): P2/P2b/P2c, §3.1, §3.2 B5, §3.5 sửa theo. B1–B4 không đổi (mọi công ty chủ). Vẫn backfill
  MỘT lần ngày chuyển đổi (T2 không đổi).
- Code: hrm-api nhánh `feat/cdhh-cum-gia` (merge local vào `feat/chuyen-doi-hang-hoa`). Số dry-run luật mới: `runbook-trien-khai.md` 3a.
- Việc treo: `hrm_erp_giacty` đã backfill bằng luật cũ ⇒ HP đang giữ hàng chép của 1/3/4 (+ 1/3/4 giữ 3 mã HP). Lệnh mới không tự
  dọn (chạy lại = 0 dòng; so khớp bỏ qua cặp ngoài luật ⇒ 0 lệch). User "dọn sau". ERP `PriceSnapshotCommand` (snapshot §3.7) còn
  gõ cứng `[1, 2, 3, 4]` — ngoài phạm vi đợt này.
