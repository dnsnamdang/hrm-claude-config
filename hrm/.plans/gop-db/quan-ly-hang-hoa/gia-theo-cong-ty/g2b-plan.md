# G2b — Bỏ cờ PRICE_PER_COMPANY (checkpoint 10/10/2026)

> Phạm vi user cho phép: hrm-api worktree `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/gia-cty-g2b-bo-co` (từ
> `feat/chuyen-doi-hang-hoa` @ `1409a38e7`), merge `--no-ff` LOCAL. KHÔNG push, KHÔNG gop_db, KHÔNG ERP/hrm-client,
> KHÔNG migration/seeder/backfill thật/ghi DB ngoài transaction test, KHÔNG đổi `.env`.
> Nguồn: `design.md` mục "Đổi 10/10/2026 — BỎ CỜ", `g2-plan.md` (N71–N75).

## Trạng thái

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Xoá `PriceFlag`, `price.per_company`, mọi nhánh cờ tắt; đọc giá luôn theo công ty chứng từ, thiếu công ty ⇒ lỗi | ✅ |
| 2 | 4 helper `TpProductUnitPrice` + A6 luôn đọc DB gộp (bỏ `mysql2`/`erp2326` cho giá — đóng N74) | ✅ |
| 3 | Đường ghi luôn đủ bộ (6 upp + pcu); bỏ lệnh `product-price:complete-sets` + test | ✅ |
| 4 | Gỡ hẳn luật suy trạng thái `@TODO-BACKFILL`; AdminData xử lý theo N72 (giữ đường lùi — xem dưới) | ✅ |
| 5 | N72 backfill chép ô quản trị từ `products` vào pcc (INSERT chép, UPDATE chỉ điền ô NULL) + test | ✅ |
| 6 | N71 compare bỏ cặp HRM sinh, chỉ kiểm BB1 + test | ✅ |
| 7 | Cập nhật test + chạy toàn bộ 4 module, đối chứng `1409a38e7` | ✅ |
| 8 | Commit + merge local; runbook `design.md` §2.4 | ✅ |

## Commit

`feat/gia-cty-g2b-bo-co`: `c24ad62db` bỏ cờ · `620094f5f` N71 + N72. Merge `--no-ff` vào `feat/chuyen-doi-hang-hoa` = **`61d1b215d`** (chưa push).

## Thay đổi chính

- **Xoá**: `MD/Services/ProductPrice/PriceFlag.php`, `MD/Console/CompleteCompanyPriceSetsCommand.php` (+ đăng ký ở provider),
  `Human/Entities/TpProductCompanyCoefficient.php` (H6 — không còn ai gọi), khoá `per_company` ở `config/price.php`.
- `ProductPriceSql::requireCompany()` thay `PriceFlag::requireCompany()`; `forCompany()` luôn `alias.company_id = ?`.
- `ProductPriceReader::costByUnit` chỉ đọc `product_company_units` (bỏ lùi `product_units.cost_price`).
- `TpProductUnitPrice` 4 helper = 1 dòng gọi reader. `QuotationService::priceCompanyOf` = `CompanyHelper::pricingCompanyId`;
  `calculateValidityDate` / `getErpPriceChangeDates` (A6) qua `nearestExpectedDates`.
- Finance F1/F3 (`productUnits`), F4 (`assertDiffPrice`), CustomerCare C1 (`searchProducts`): bỏ hệ số pcc.
- `ProductPriceSetWriter`: `companiesWithStatus` chỉ dòng `status` NOT NULL; `ensureUnitSet/ensureProductSet` luôn sinh 6 upp + pcu;
  bỏ `writesPrices`, `completeSets`.
- `Product`: `companyStatusSql` = `pcs.status`, `ownerStatusSql` = `pco.status`, `tradingCompanyNames` chỉ dòng thật.
  `ProductLifecycleService`: bỏ `statusAt`; khoá luôn UPDATE dòng có sẵn (bỏ nhánh sinh dòng coef 1 cho hàng cũ chưa có dòng).
- `database/e2e_provision.php`: snapshot giá luôn qua reader (DB gộp), không `mysql2` (file chỉ sửa, không chạy).

## Quyết định AdminData (N72)

**Giữ đường lùi cột chung** (gỡ nhãn `@TODO-BACKFILL`, ghi lý do trong docblock). Sau N72, cặp có dòng (chủ + công ty nhận
của hàng status 1 cụm) đọc dòng với cùng số như cột chung. Vẫn còn ca KHÔNG có dòng cần lùi tới khi xoá cột chung (§24c-1 bước 5):
1. Màn Kho dữ liệu + chi tiết (mở cho mọi người) xem bằng công ty CHƯA dùng hàng.
2. Hàng ERP status 2/5 (backfill T1/T3 không sinh dòng).
3. Công ty ngoài cụm (Cty 7…) chưa lấy về.

`products` KHÔNG có cột chính sách kinh doanh (đo `information_schema` 10/10: chỉ `guarantee int NULL`, `guarantee_type varchar NULL`,
`min_stock_qty decimal(12,2) NOT NULL DEFAULT 0`) ⇒ N72 chép 3 ô, `business_policy_id` không đụng.

## N71 — tiêu chí "cặp HRM sinh" sau backfill

B4/B5 bỏ qua cặp đã có `status` trước khi chạy. Sau backfill mọi cặp đều có status ⇒ nhận lại bằng dấu vết: cặp có dòng `pcu`
`created_by` NOT NULL (`ProductPriceSetWriter` luôn ghi người thao tác; backfill luôn NULL) HOẶC `pcc.status` ≠ 3 (backfill chỉ đặt 3).
Cặp này chỉ kiểm BB1 (status NOT NULL + pcu + 6 upp / ĐVT). Công ty nhận chưa có status mà chủ đang ở trạng thái ≠ 3 ⇒ bỏ qua
(`chu_chua_kinh_doanh`, = B5 `owner_not_ready`). Chủ CHƯA có status (chưa backfill) thì không bỏ qua — vẫn báo thiếu bộ.
⚠️ Tiêu chí chỉ đúng NGAY SAU backfill: ĐVT thêm ở HRM sau đó mang `created_by` ⇒ cặp bị coi là HRM (đúng ý: compare hết ý nghĩa sau
khi bắt đầu sửa giá). Lệnh in thêm 2 dòng "Không so giá — …".

## PHPUnit (DB `hrm_erp`, DatabaseTransactions)

| Bộ | Trước (`1409a38e7`) | Sau (`61d1b215d`) |
|---|---|---|
| `Modules/MasterData/Tests` | 280 ca, 2016 assertion — OK (đo ở G2) | **280 ca, 1975 assertion — OK** |
| `Modules/Assign/Tests` | 1 skipped | 1 skipped (y hệt) |
| `Modules/Finance/Tests` | 121 — 1 error `BorrowSellStoreTest::test_returning_qty_excludes_parent_request`, 1 failure `PrepickTrackingApiTest::test_export_tree_indent_and_bold_per_level` (chạy lại 10/10) | y hệt |
| `Modules/Human/Tests` | 14 — 2 failure `CatalogImportFixesTest`, `ProvinceImportValidationTest` (chạy lại 10/10) | y hệt |
| CustomerCare | không có test | — |

Ca đổi/mới: `ProductPriceReaderTest` 7→5 (bỏ cờ tắt + mẫu `mysql2`; thêm ca 7 điểm ném lỗi thiếu công ty) · `PriceReadPointsTest` 8
(bỏ nhánh cờ tắt, thêm ca công ty thứ 2 / chủ chưa backfill ra 0) · `ProductPriceSetWriteTest` 7 (bỏ `complete-sets`, đủ bộ cho công ty
khác khi thêm ĐVT, trạng thái không suy ra) · `CompanyPriceBackfillTest` 10→12 (+N71, +N72) · `ProductTakeApiTest`,
`ProductLifecycleApiTest`, `ProductReadApiTest`: fixture hàng ERP cũ = dòng trạng thái thật (như sau B4); ca "suy ra" đổi thành
"không suy ra" (403 chưa dùng / `owner_not_trading`). Kiểm test bắt lỗi: tắt N71 ⇒ ca N71 đỏ; bỏ chép ô quản trị ⇒ ca N72 đỏ.

**Ca phụ thuộc dữ liệu thật** (chạy lại trên bản sao `hrm_erp_giacty` sau backfill):
- `CompanyPriceBackfillTest::mau_du_lieu_that_backfill_xong_so_khop_0_lech` — đòi hàng CHƯA backfill (assert số ghi > 0); trên bản sao
  đã backfill sẽ đỏ vì không còn gì để ghi ⇒ cần đổi thành "compare = 0 lệch trên mẫu" khi chạy sau backfill.
- `ProductReadApiTest::kho_du_lieu_loc_tinh_trang_su_dung_va_hien_cong_ty_dang_kinh_doanh` dùng hàng thật Cty 1 — đã viết chạy được cả
  trước/sau backfill.
- `PriceReadPointsTest::f2_*` dùng 1 phiếu chuyển hàng thật (không phụ thuộc giá).

## Chạy trên DB đích hrm_erp_giacty (10/10)

Nhánh `fix/gia-cty-test-sau-backfill` (`627f16f3a`) → merge `--no-ff` LOCAL vào `feat/chuyen-doi-hang-hoa` = `98a59deff` (chưa push).
Chỉ sửa test (8 file `Modules/MasterData/Tests`), không đụng code, không migration/seeder, không ghi DB ngoài transaction test.

**Nguyên nhân từng nhóm (trước: 280 ca — 29 error + 2 failure):**
- 16 lỗi 1048 (`PriceReadPointsTest` 8, `ProductPriceReaderTest` 5, `ProductPriceSetWriteTest` 3): fixture `BuildsCompanyPrices`
  chèn dòng giá `company_id` NULL ("chưa backfill — không được đọc"); `legacyTradingProduct` giá NULL. ⇒ bỏ dòng NULL (chủ A
  không bộ giá); hàng ERP cũ = bộ giá + pcu của chủ A như sau backfill; ca lấy về/gỡ kiểm bộ chủ A giữ đủ thay vì "dòng NULL".
- 13 lỗi 1452 (`CompanyPriceBackfillTest` 12 + `ProductLifecycleApiTest::chu_xoa_cung_sach_20_bang`): INSERT không có cột
  `company_id` ⇒ connection không strict lấy mặc định ngầm 0 ⇒ vướng FK `companies` (không phải 1048). Đều là fixture test.
- `ProductCompanyFoundationTest::test_dong_he_so_cu_khong_bi_dong_vao` (113484 ≠ 0): K1 "0 dòng pcc có status" chỉ đúng
  trước backfill ⇒ đổi thành status chỉ NULL hoặc 1–4 + coefficient NOT NULL.
- `ProductWriteApiTest::sua_hang_cu_chi_bo_sung_loai_va_catalog_thi_luu_duoc` (404): ca chọn "hàng ERP cũ chưa có dòng công ty" —
  sau backfill 0 hàng thoả (8.631 hàng ứng viên đều có dòng chủ status 3) ⇒ id 0 ⇒ 404. Hành vi đúng của mô hình mới ⇒ ca
  chọn hàng có dòng chủ status 3: D1 dòng chủ giữ nguyên (so 7 cột), G4 đổi ô quản trị ⇒ upsert đúng dòng, giữ status + hệ số.

**Bộ backfill** (`CompanyPriceBackfillTest`, 12 ca, không `@group`/skip nào): hàng giả dựng ở dạng duy nhất còn tồn tại được sau M3 —
dòng giá mang công ty CHỦ (B1 xong, `upp.assign` luôn 0), chưa pcu / bù loại / trạng thái / bộ nhận ⇒ B2–B6, dry-run = chạy
thật, chạy 2 lần, `--company`, so khớp, N71, N72, B0, SG- vẫn kiểm đủ (số kỳ vọng khác cũ chỉ ở `upp.assign`).
`m3_tu_chan…`: DB đích guard toàn bảng 0/0 + CSDL tự chặn NULL (1048) / trùng (1062); nhánh chặn của guard kiểm trên bảng
`TEMPORARY product_unit_prices` cùng tên (che bảng thật trong phiên, không commit ngầm, DROP trong `finally`).
`mau_du_lieu_that…`: ~250 hàng thật ⇒ compare 0 lệch (có nhóm `bu_loai_gia_0`), dry-run 0 dòng, B0 sạch, chạy thật 0 dòng + B6 đạt
(bỏ hàng giả setUp khỏi mẫu — H4 status 2 từng lọt vào nhóm status 2/5).
⚠️ Bộ test MasterData nay nhắm DB ĐÍCH: trên `hrm_erp` gốc (chưa backfill) các ca guard/mẫu thật/`sua_hang_cu…` sẽ đỏ — đúng ý.

**Rà đường ghi `product_unit_prices` trong hrm-api (app/, Modules/, database/, seeder, command):** chỉ 2 chỗ —
`ProductPriceSetWriter::ensureUnitSet` (có `company_id`, chỉ chèn loại còn thiếu ⇒ không vướng UNIQUE) và `CompanyPriceBackfill::apply`
(có `company_id`). Không model `ProductUnitPrice`/`TpProductUnitPrice` nào create/save; seeder chỉ đọc. ⇒ **không có lỗi code**.
Ngoài phạm vi hrm-api: ERP (`TanPhatDev`: `app/Product.php`, `ExcelImports/*`, seeds) còn ghi bảng này không `company_id` — trên DB gộp
sau M3 sẽ lỗi 1452; cần chốt khi đưa M3 lên DB dùng chung.

| Bộ (DB `hrm_erp_giacty`) | Trước | Sau (`98a59deff`) |
|---|---|---|
| `Modules/MasterData/Tests` | 280 — 29 error, 2 failure | **280 ca, 2000 assertion — OK** |
| `Modules/Assign/Tests` | — | 1 skipped (y hệt hrm_erp) |
| `Modules/Finance/Tests` | — | 121 — 1 error `BorrowSellStoreTest` (FK `created_by` employees), 1 failure `PrepickTrackingApiTest` — y hệt đỏ sẵn |
| `Modules/Human/Tests` | — | 14 — 2 failure `CatalogImportFixesTest`, `ProvinceImportValidationTest` — y hệt đỏ sẵn |

## Còn đọc `mysql2` gần phạm vi giá (liệt kê, KHÔNG sửa — ngoài giá)

- `TpProductUnitPrice::getBaseUnitIds` — ĐVT gốc (`product_units.unit_id`) cho `ErpProductSearchService` + `BackfillQuotationProductUnitIdSeeder`.
- `QuotationController::priceTypes` — danh mục `price_types`.
- `QuotationService::calculateValidityDate` — `configs.quotation_valid_days`.
- `BomListController` / `QuotationService` — `recipe_products`, `currencies`; `DetailQuotationResource` / `QuotationController` — ảnh + bảo hành `products`.
- `database/e2e_provision.php` — `products` (tên/mã), `currencies`.

## Ghi chú

- Đường ghi tab Quản trị `ProductWriteService::writeAdmin` nhánh G4/D1 (chủ chưa có dòng) giờ chỉ còn chạy cho hàng chưa backfill —
  không gỡ (ngoài danh sách việc), chỉ sửa chú thích.
- `vendor/composer` classmap của worktree vẫn liệt kê 3 lớp đã xoá (không ai gọi ⇒ vô hại); `composer dump-autoload` khi tiện.
- N73 (`BorrowExportRequestTestDataSeeder`), N75 (`e2e_provision` mã hàng 3920 = id `erp2326`) còn mở.

## Cần user quyết

- **Q-G2b-1** `mau_du_lieu_that_…` sau khi backfill bản sao: đổi thành ca chỉ so khớp (không đòi số ghi > 0) hay giữ làm ca "trước backfill"?
- **Q-G2b-2** Trỏ worktree sang `hrm_erp_giacty` + chạy backfill/compare/M3 — đợt riêng, cần "làm" riêng (đổi `.env`, ghi DB).
- **Q-G2b-3** Push `feat/chuyen-doi-hang-hoa` (G1 + fixture + G2 + G2b chưa push).
