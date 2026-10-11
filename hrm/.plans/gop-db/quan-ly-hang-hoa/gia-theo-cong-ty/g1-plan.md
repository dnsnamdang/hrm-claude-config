# G1 — Nền CSDL giá theo công ty (checkpoint 09/10/2026)

> Nguồn: `design.md` §2.2–§3.6 + "Trả lời §9" + "Chốt từ mockup". Phạm vi user cho phép: hrm-api worktree
> `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/gia-cty-g1-nen` (từ `feat/chuyen-doi-hang-hoa` @ `a862fbeef`).
> Chỉ chạy M1 + M2 vào `hrm_erp`. **KHÔNG** backfill thật, **KHÔNG** M3, **KHÔNG** seeder, không merge/push. `@TODO-BACKFILL` giữ nguyên (G2).

## Trạng thái

| # | Task | Trạng thái |
|---|---|---|
| 1 | Test trước (TDD) `CompanyPriceBackfillTest` — đỏ đúng lý do (thiếu cột/bảng) | ✅ |
| 2 | M1 `product_company_units`, M2 `upp.company_id` NULL + FK + index, M3 ép NOT NULL + UNIQUE + tự chặn | ✅ code · M1/M2 đã chạy · M3 CHƯA chạy |
| 3 | Model `ProductCompanyUnit`, config `price.cluster_company_ids = [1,2,3,4]` | ✅ |
| 4 | `product-price:backfill-company {--dry-run} {--company=*} {--chunk=500}` (+ `--product=*` nội bộ/test) | ✅ |
| 5 | `product-price:compare {--company=} {--csv=}` (+ `--product=*`) — chỉ đọc | ✅ |
| 6 | Sao lưu → M1, M2 vào `hrm_erp` → dry-run → so §3.4 | ✅ |
| 7 | PHPUnit MasterData toàn bộ + so với commit gốc | ✅ (xem mục Kết quả) |
| 8 | Commit | ✅ `36dd43546` |

## File (commit `36dd43546`, nhánh `feat/gia-cty-g1-nen`)

- `config/price.php` — `cluster_company_ids`
- `Modules/MasterData/Database/Migrations/2026_10_09_000002_create_product_company_units_table.php` (M1)
- `…/2026_10_09_000003_add_company_id_to_product_unit_prices_table.php` (M2)
- `…/2026_10_09_000004_enforce_company_id_on_product_unit_prices_table.php` (M3 — gọi `CompanyPriceGuard::assertReady()` trước mọi DDL)
- `Modules/MasterData/Entities/Product/ProductCompanyUnit.php` (`extends Model`, gán `company_id` tay)
- `Modules/MasterData/Services/ProductPrice/CompanyPriceBackfill.php` (+ `CompanyPriceBackfillReport.php`) — B0–B6
- `Modules/MasterData/Services/ProductPrice/CompanyPriceComparator.php` (+ `CompanyPriceCompareReport.php`) — §3.5
- `Modules/MasterData/Services/ProductPrice/CompanyPriceGuard.php` — tự kiểm M3 (tách ra để test được)
- `Modules/MasterData/Console/BackfillCompanyPricesCommand.php`, `CompareCompanyPricesCommand.php`
- `Modules/MasterData/Providers/MasterDataServiceProvider.php` — đăng ký 2 lệnh (+6 dòng, LF giữ nguyên)
- `Modules/MasterData/Tests/Feature/CompanyPriceBackfillTest.php` — 10 ca

## Cách lệnh backfill chạy

Mỗi lô hàng (`chunkById`): đọc hết dòng liên quan → dựng **kế hoạch trong bộ nhớ** theo đúng thứ tự B1→B5 (bước sau thấy kết quả
"ảo" của bước trước) → dry-run chỉ đếm kế hoạch; chạy thật ghi kế hoạch trong 1 transaction/lô và đối chiếu số dòng thực ghi =
kế hoạch (lệch ⇒ rollback lô, dừng). ⇒ số dry-run = số chạy thật (có test).

- Giá công ty nhận: `scalePrice()` = PHP `round($price * $k / 1000) * 1000` khi `$k != 1` — y hệt `getData` ERP (phép float + `round`
  half-away). Tính trong PHP, không SQL.
- Idempotent không dựa vào UNIQUE upp (chỉ có từ M3): chỉ gán dòng còn NULL, chỉ sinh dòng (ĐVT, công ty, loại) còn thiếu, pcu/pcc
  `insertOrIgnore` theo UNIQUE, cặp đã có `status` thì bỏ qua cả cặp; pep chỉ sinh kèm dòng upp vừa sinh.
- `--company`: chỉ ghi dòng của các công ty này (B1–B4 khi là chủ, B5 khi là công ty nhận). Công ty nhận chỉ được chép khi bộ giá chủ
  đã sẵn sàng (chủ status 3 + đủ 6 loại + pcu chủ) — chưa thì đếm `bỏ qua.owner_not_ready`.
- B0 (dừng, không ghi): `orphan_upp`, `owner_unknown` (products.company_id NULL không khớp tiền tố `SG-`), `duplicates` (ĐVT, công ty —
  NULL tính là chủ, loại), `pcu_foreign` (pcu lệnh này không thể sinh ⇒ có người khác ghi bảng).
- B6 (exit 1 nếu lệch): BB1 cho mọi cặp lệnh vừa đặt status 3, `upp.company_id` NULL = 0 trong phạm vi.

## Lệnh đã chạy vào DB

| Lúc | Lệnh | Kết quả |
|---|---|---|
| 09/10 23:36 | `mysqldump --single-transaction hrm_erp product_unit_prices migrations \| gzip` | `scratchpad/hrm_erp_g1_truoc_M1M2_20261009_233638.sql.gz` (2,0 MB; upp 264.646 dòng, migrations 5.746) |
| 09/10 | `migrate:status` | chỉ 3 migration chờ = M1, M2, M3 |
| 09/10 | `migrate --path=…/2026_10_09_000002_create_product_company_units_table.php --force` | **batch 430** |
| 09/10 | `migrate --path=…/2026_10_09_000003_add_company_id_to_product_unit_prices_table.php --force` | **batch 431** (2,5 s) |
| 09/10 | `product-price:backfill-company --dry-run` | 6,3 s, không ghi (kiểm lại: pcu 0, upp.company_id NOT NULL 0, pcc status 0) |
| 09/10 | `product-price:compare` (chỉ đọc) | 753.991 lệch "thiếu bộ" — đúng vì chưa backfill; lệch giá 0 |

Bản sao lưu: `/private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/a3ffcd9e-43c0-40bd-9175-373312cc3b46/scratchpad/hrm_erp_g1_truoc_M1M2_20261009_233638.sql.gz`
(⚠️ thư mục tạm — chép ra chỗ khác nếu muốn giữ). Lùi M1/M2: `migrate:rollback --path=<file M2>` rồi `<file M1>` (down() có sẵn).

M3 **chưa** chạy ở đâu cả (kể cả `--pretend`): `migrate` một lèo trên `hrm_erp` hôm nay sẽ dừng ở M3 với câu
"còn 264646 dòng company_id NULL, 0 bộ trùng…" (đã kiểm bằng `CompanyPriceGuard::violations()` trong test).

## Dry-run `hrm_erp` (09/10) vs ước tính §3.4

| Bộ đếm | Cty 1 | Cty 2 | Cty 3 | Cty 4 | Tổng | §3.4 |
|---|---:|---:|---:|---:|---:|---|
| upp.assign (B1) | 258.270 | 18 | 138 | 6.220 | 264.646 | 264.646 ✅ (Cty4 6.215 + 5 dòng hàng 9964 NULL) |
| pcu.owner (B2) | 45.477 | 3 | 23 | 1.057 | 46.560 | 46.560 ✅ |
| upp.fill (B3) | 5.765 | 0 | 0 | 108 | 5.873 | 5.873 ✅ (Cty1 5.407+358, Cty4 102+6) |
| pcc.owner (B4) update / insert | 0 / 27.370 | 0 / 3 | 0 / 14 | 4 / 980 | 4 / 28.367 = 28.371 | ~28.371 ✅ |
| pcu.copy (B5) | 1.010 | 28.844 | 28.824 | 27.863 | 86.541 | 86.541 ✅ |
| upp.copy (B5) | 6.060 | 173.064 | 172.944 | 167.178 | 519.246 | 519.246 ✅ ⇒ upp sau = 789.765 ✅ |
| pep.copy (B5) | 32 | 2.008 | 2.008 | 1.976 | 6.024 | 6.024 ✅ |
| pcc.recv (B5) update / insert | 0 / 1.001 | 398 / 27.970 | 382 / 27.975 | 23 / 27.364 | 803 / 84.310 = 85.113 | 85.113 ✅ (§3.4 ghi "≈1.100 UPDATE" — số đó gồm cả dòng pcc của hàng status 0; thực tế hàng status 1 chỉ 803) |
| giá đổi số vì k ≠ 1 (tham khảo) | 0 | 1.338 | 1.332 | 90 | 2.760 | Cty2 1.338 · Cty3 1.332 · Cty4 90 ✅ |

Tổng dòng sẽ ghi: 1.042.374. Hàng duyệt: status 0 = 17.512 · 1 = 28.371 · 2 = 1 · 5 = 6.

Nhóm T4 (§3.6) đo bằng SQL chỉ đọc: Cty2 220 · Cty3 214 · Cty4 15 (= 9 dòng công ty nhận + **6 dòng của chính công ty chủ Cty4** có dòng
pcc k = 1) — khớp §3.6. Lệnh compare đếm T4 cả cặp chủ.

## Kết quả PHPUnit

- `CompanyPriceBackfillTest`: **10/10 xanh, 209 assertion** (~4 s, mọi ghi trong transaction, DB sau test sạch). Ca:
  (1) dry-run không ghi + số = tính tay = chạy thật + bảng in; (2) BB1, giá × 1.05 làm tròn half-away (1039.5→1040, 1291.5→1292),
  k = 1 giữ số lẻ, pep tương lai chép (quá ngày / status 1 không chép, chép created_by/updated_by), pcu chủ 13 cột / nhận 5 cột + 8 NULL,
  pcc cũ giữ hệ số + created_by, pcc mới k 1 created_by NULL, status 0/2 không trạng thái; (3) chạy 2 lần không đổi; (4) `--company`
  [1,2] rồi [3,4]; (5) so khớp 0 lệch + bắt đúng 1 giá sửa tay + CSV + exit 1, và báo thiếu bộ khi chưa backfill; (6) M3 guard (NULL
  thật của DB, NULL bộ giả, trùng); B0 dừng khi không xác định được chủ; hàng NULL `SG-` ⇒ Cty 4 không sửa products;
  **mẫu ~250 hàng THẬT** (k ≠ 1, k = 1 lẻ nghìn, pep tương lai, thiếu loại 5/6, nhiều ĐVT, chủ 2/3/4, status 0/2/5, hàng NULL) ⇒
  B6 đạt, compare 0 lệch, chạy lại 0 dòng.
- Kiểm test bắt lỗi (mutation tay, đã hoàn nguyên): đổi `round`→`floor` ⇒ 2 ca đỏ; bỏ lọc pep status/ngày ⇒ 2 ca đỏ.
- **Toàn bộ `Modules/MasterData/Tests`: 256 ca — 110 error + 6 failure.** Chạy trên commit gốc `a862fbeef` (cùng DB): 246 ca —
  **đúng 116 ca đỏ y hệt** (so danh sách: 0 ca chỉ đỏ ở nhánh mới). Nguyên nhân:
  - 85 ca: fixture `INSERT roles (… company_id …)` — bảng `roles` trên `hrm_erp` không có cột `company_id` (DB gộp, đỏ sẵn).
  - 16 + 8 + 1 ca: FK `employee_infos.department_id`, `companies.updated_by`, `employees.employee_info_id` (fixture lệch DB gộp, đỏ sẵn).
  - 5 failure Regulation (`RegulationTabRegistryTest` ×4, `it_reads_current_congno_values_from_companies`) — đỏ sẵn.
  - ⚠️ **1 ca do G1:** `ProductLifecycleApiTest::danh_sach_fk_khop_information_schema` — FK mới `product_company_units.product_id → products`
    chưa có trong hằng `ProductUsageGuard::CHILD_FK_COLUMNS`. Đỏ ở cả commit gốc vì DB đã có bảng M1. Chưa sửa (ngoài phạm vi) — xem "Cần quyết".
- Hệ quả: 85 ca Product*Test chết ở fixture ⇒ bộ test cũ **không chứng minh được** đường ghi hàng hoá cũ chạy với cột NULL mới. Bù bằng:
  rà tay 17 file HRM đọc `product_unit_prices` — không có `where('company_id')` không tiền tố nào trong câu có join `product_unit_prices`
  (không có lỗi "ambiguous column"); quét heuristic ERP `wt-erp-2d1/app` cũng không thấy. Đường ghi cũ INSERT upp không có `company_id`
  ⇒ NULL (hợp lệ tới M3).

## Lệch so với design / ghi chú

1. **Số migration**: design đề xuất `…000001/2/3`; đã có `2026_10_09_000001` (mẫu tem) ⇒ dùng `2026_10_09_000002/3/4`.
2. **Lệnh đặt ở `MD/Console`** như design, đăng ký qua `MasterDataServiceProvider::register()` (app/Console/Commands không dùng).
3. **Tuỳ chọn nội bộ `--product=*`** ở cả 2 lệnh (phạm vi test, không chạm 264k dòng) — design không có.
4. **pep công ty nhận**: `updated_by` chép `updated_by` của dòng gốc (theo lệnh giao việc); design §3.2 ghi "created_by/updated_by = created_by của ep gốc".
   Dòng gốc có `updated_by` NULL thì dòng mới cũng NULL (cột nullable).
5. **B5 thêm điều kiện "chủ sẵn sàng"** (chủ status 3 sau B4 + đủ 6 loại + có pcu chủ): hàng HRM tạo (chủ status 1 Đang nhập thông tin)
   sẽ không bị chép sang cụm và không thành Đang kinh doanh ở công ty nhận. Production chưa có ca này; local hiện 0 dòng pcc có status.
6. **Cặp đã có `status` bị bỏ qua cả cặp** (không chép giá, không đổi trạng thái), kể cả cặp "lấy về" (2-C2) chưa có bộ giá ⇒ BB1 của các
   cặp đó để G2 xử lý (`take` sinh bộ giá rỗng, §5.3).
7. **compare** so thêm `coefficient`, `sale_max_percent` (cột chép nguyên) ngoài giá. Nhóm chấp nhận nhận diện theo thời điểm: dòng pcc
   "có từ trước" = `created_at` < `created_at` pcu chủ (dòng do backfill sinh cùng lượt); dòng bù loại 5/6 = giá 0 + hệ số 0 + `created_at` ≥
   pcu chủ (ERP vốn có ~30k dòng 0/0 sẵn — không đếm). Sau khi các công ty bắt đầu tự sửa giá, `compare` hết ý nghĩa (so với dòng chủ).
8. B3 bù cho chủ thuộc **mọi** công ty chủ (không chỉ cụm) đúng chữ design; thực tế chủ 5–8 có 0 hàng.
9. M3 dùng `ALTER … MODIFY` thô (không cần doctrine/dbal), đổi thứ tự: thêm UNIQUE rồi mới bỏ 2 index thường. **Chưa chạy thử ở DB nào.**

## Cần user quyết

- **Q-G1-1** `ProductUsageGuard` + xoá cứng: FK `pcu.product_id`/`pcu.product_unit_id` mới làm đỏ `danh_sach_fk_khop_information_schema`, và
  khi đã có dòng pcu thì xoá cứng hàng sẽ vướng FK 1451 (guard trả 422). Đề xuất: thêm `product_company_units` vào `CHILD_FK_COLUMNS`
  (19→20) + xoá pcu ở `ProductLifecycleService` hard delete — đúng §5.3 G2. Làm ngay ở G1 (đụng 2 file ngoài phạm vi) hay để G2?
- **Q-G1-2** Thời điểm chạy backfill thật vào `hrm_erp` (T5: chạy thẳng DB chung) — sau khi G2/G3 lọc công ty sẵn sàng? Trình tự §2.4:
  backfill → compare = 0 → M3.
- **Q-G1-3** Merge `feat/gia-cty-g1-nen` về `feat/chuyen-doi-hang-hoa` (chưa merge, chưa push).

## Sửa fixture DB gộp (10/10)

Nhánh `fix/test-fixture-db-gop` (từ `c87221dc6`) — commit `e39d67520`, merge `--no-ff` LOCAL về `feat/chuyen-doi-hang-hoa` = `98afafb05`.
Chưa push. Chỉ sửa 6 file trong `Modules/MasterData/Tests/`; không đụng code nghiệp vụ / migration / DB (mọi ghi trong DatabaseTransactions).

**Nguyên nhân thật** (đối chiếu `migrations` + log `[fix-fk]` 09/10 12:23 + SHOW CREATE TABLE):
- 85 ca `roles.company_id`: migration HRM `2026_09_25_000002_drop_orphan_org_columns_from_roles_table` (batch 429, chạy vào `hrm_erp`
  09/10) **gỡ có chủ đích** cột này. Không code nghiệp vụ nào đọc `roles.company_id` (grep app/ + Modules/: phạm vi công ty đi qua
  `company_roles`, `employee_has_roles.company_id`, `role_has_permissions.company_id`) ⇒ lỗi chỉ ở fixture `ActsAsProductUser`.
  Lượt xanh 150/150 (2-D1) ngày 09/10 nhiều khả năng chạy trước batch 429 (12:23) — suy luận, chưa đối chiếu giờ.
- 25 ca FK (`employee_infos.department_id`, `companies.updated_by`, `employees.employee_info_id`): 3 FK này **đã trỏ nội bộ `hrm_erp` từ
  trước** (không nằm trong 11 khoá `fix_cross_database_foreign_keys` dựng lại) ⇒ fixture Regulation* luôn sai trên DB gộp (dept 0,
  actor `employees.id = 1` không tồn tại, `employee_info_id = 999999998` ảo) — không do migration 09/10.
- 5 failure + 3 ca 422 lộ ra sau khi gỡ FK: test Regulation **cũ hơn registry** — thay đổi có chủ đích, có commit: `c4dadb993` (26/09, congno
  → MIXED + `debt_calculation_date` bắt buộc store=config), `3277fc5dc` (22/09, 4 field `is_*` baogia → thitruong), `83927ce3c` (22/09,
  +3 field DSTC baogia), 2 field kho congno (17/09).

**Sửa:** `ActsAsProductUser` bỏ `company_id` khỏi INSERT roles (chạy được cả DB có/không cột vì cột cũ nullable; chọn theo schema gộp,
không dùng `Schema::hasColumn` vì cột đã bị gỡ có chủ đích). Regulation{CongnoVersioning,ScalarTabs,Term,History}Test: phòng ban/nhân viên
có thật (`actorId()`), tạo hồ sơ `employee_infos` thật cho ca không quyền; payload API thêm `debt_calculation_date`; kỳ vọng số field
7→10, baogia 14→13, congno không còn trong `scalarCompanyKeys` nhưng có ở cả 2 store, `is_equipment` kiểm ở thitruong. Không bỏ assertion,
không skip.

**PHPUnit `Modules/MasterData/Tests`:** trước 256 ca — 110 error + 6 failure ⇒ sau 256 ca, 1771 assertion — **1 failure**:
`ProductLifecycleApiTest::danh_sach_fk_khop_information_schema` (FK `product_company_units.product_id` chưa có trong
`ProductUsageGuard::CHILD_FK_COLUMNS`) — **đỏ có chủ đích, để G2** (Q-G1-1).

Ngoài luồng (ghi lại, không vá): log 09/10 `[fix-fk]` báo 10 khoá ngoại trên `hrm_erp` local **đã xoá nhưng dựng lại hỏng** (devices,
distribution_rules, salary, salary_employee_data, salary_employees… vì khoá `created_by → hrm_employees` cùng bảng còn chắn) ⇒ DB local
đang thiếu các ràng buộc này.
