# G2 — HRM đọc/ghi giá theo công ty (checkpoint 10/10/2026)

> Phạm vi user cho phép: hrm-api worktree `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/gia-cty-g2-doc-hrm` (từ
> `feat/chuyen-doi-hang-hoa` @ `98afafb05`), merge `--no-ff` LOCAL. KHÔNG push, KHÔNG gop_db, KHÔNG ERP/hrm-client,
> KHÔNG migration/seeder/backfill/ghi DB ngoài transaction test. Nguồn: `design.md` §2.5, §4.1, §4.3, §4.4 (HRM), §4.5, §5.3.

## Trạng thái

| # | Task | Trạng thái |
|---|---|---|
| 1 | Baseline PHPUnit 4 module trên `98afafb05` | ✅ |
| 2 | Cờ `PRICE_PER_COMPANY` + `ProductPriceSql` + `ProductPriceReader` (+ test) | ✅ |
| 3 | H1–H6 helper Human + A1–A9 Assign | ✅ |
| 4 | F1–F6 Finance + C1–C3 CustomerCare | ✅ |
| 5 | Đường ghi BB1 (tạo / thêm ĐVT / lấy về / gỡ / xoá cứng) + gỡ CASE theo cờ + lệnh `complete-sets` | ✅ |
| 6 | Test danh sách trắng + chốt lời gọi helper | ✅ |
| 7 | Chạy lại toàn bộ test + commit + merge local | ✅ |

## Commit

Nhánh `feat/gia-cty-g2-doc-hrm`: `347501f32` lớp đọc + cờ · `fa9e461dc` Human + Assign · `9968b19d9` Finance + CustomerCare ·
`4612e6d5f` đường ghi BB1 · `890dc9da6` whitelist. Merge `--no-ff` vào `feat/chuyen-doi-hang-hoa` = **`1409a38e7`** (chưa push).

## File

- Mới: `Modules/MasterData/Services/ProductPrice/{PriceFlag,ProductPriceSql,ProductPriceReader,ProductPriceSetWriter}.php` ·
  `Modules/MasterData/Console/CompleteCompanyPriceSetsCommand.php` · `Entities/Product/{ProductExpectedPrice,ProductApprove,ProductApprovePrice}.php` ·
  `tests/fixtures/price-readers.txt` · test `ProductPriceReaderTest`, `PriceReadPointsTest`, `ProductPriceSetWriteTest`,
  `PriceReaderWhitelistTest`, `Concerns/BuildsCompanyPrices`.
- Sửa: `config/price.php` · `app/Helpers/CompanyHelper.php` · Human `TpProductUnitPrice`, `TpProductCompanyCoefficient` ·
  Assign `BomListController`, `QuotationController`, `QuotationService`, `QuotationImportService`, `BomListService`,
  `DetailBomListResource`, `ErpProductSearchService` · Finance `ProductImportRequestService`, `ProductTransferRequestService`,
  `BorrowSellRequestService`, `BorrowExportRequestService`, `PrepickApprovalRouteService` · CustomerCare `ServiceService`,
  `WrServiceQuotationService`, `WrQuotationService` · MasterData `ProductWriteService`, `ProductLifecycleService`,
  `ProductUsageGuard`, `Product`, `ProductUnit`, `ProductUnitPrice`, `CompanyPriceBackfill` (B0), `MasterDataServiceProvider`,
  test `ProductLifecycleApiTest` (19→20) · `database/e2e_provision.php` (chỉ sửa file, không chạy).
- Toàn bộ file LF; `git diff --ignore-cr-at-eol` = `git diff` (328+/146−, không nhiễu EOL). `@TODO-GIACTY` = 0.

## Quyết định cờ `PRICE_PER_COMPANY` (mặc định TẮT)

**Đọc**
- Cờ BẬT: mọi đường đọc mang `company_id` = công ty chứng từ (`CompanyHelper::pricingCompanyId($doc, $explicit)` — tường minh >
  chứng từ > người dùng); thiếu công ty ⇒ `InvalidArgumentException` (fail-closed). Không nhân hệ số. Giá vốn từ
  `product_company_units`. 4 helper Human đọc DB mặc định (DB gộp), không qua `mysql2`.
- Cờ TẮT: 4 helper Human + A6 giữ NGUYÊN đường cũ `mysql2` (từng dòng). Finance/CustomerCare (vốn đọc DB gộp) đi qua
  `ProductPriceSql::forCompany` với luật "giá chủ hàng": `company_id IS NULL OR = products.company_id` + hệ số cũ y như trước.
  Trên `hrm_erp` hiện tại (mọi dòng NULL) kết quả y hệt; sau khi có dòng công ty khác (lấy về, backfill chép cụm) đọc HRM không nhân dòng.
- Gỡ CASE suy trạng thái (`companyStatusSql`, `scopeWithCompanyStatus`, `ownerStatusSql`, `statusAt`, `tradingCompanyNames`)
  CHỈ khi cờ bật; cờ tắt giữ luật `@TODO-BACKFILL`.

**Ghi (BB1)** — chạy cả 2 trạng thái, khác 1 điểm:
- Cờ BẬT: đủ bộ (6 `upp` + 1 `pcu`) cho mọi công ty có `pcc.status`.
- Cờ TẮT: `upp` CHỈ sinh cho công ty CHỦ hàng (+ chủ suy ra theo luật cũ); công ty khác (lấy về, thêm ĐVT khi đã có công ty lấy về)
  chỉ sinh `pcu`. Lý do: DB gộp dùng chung với ERP local — ERP cũ (popup `SearchController`, `units_info`) nối `upp` không kẹp
  công ty, 1 dòng giá công ty thứ 2 là nhân dòng ngay ở ERP. Tạo hàng mới bằng code G2 chỉ có dòng của chủ ⇒ đọc cũ (HRM + ERP) không đổi.
- Bù BB1 lúc bật cờ: lệnh mới `product-price:complete-sets {--dry-run} {--product=*}` — sinh phần thiếu cho mọi cặp có trạng thái;
  **dừng nếu còn `upp.company_id` NULL** (phải sau backfill). Runbook §2.4 thành: migrate M1–M2 → backfill → **complete-sets** → compare → M3 → bật cờ.
- Gỡ: xoá `pep` → `pap`/`pa` → `upp` → `pcu` của công ty gỡ. Xoá cứng: + xoá `pcu`. `CHILD_FK_COLUMNS` + `product_company_units`.
- Backfill B0 `pcu_foreign`: bỏ qua pcu của cặp đã có `status` (do G2 sinh) — không thì backfill dừng.

## PHPUnit (DB `hrm_erp`, DatabaseTransactions)

| Bộ | Trước (`98afafb05`) | Sau (`1409a38e7`) |
|---|---|---|
| `Modules/MasterData/Tests` | 256 ca — 1 failure (`danh_sach_fk_khop_information_schema`, đỏ có chủ đích từ G1) | **280 ca, 2016 assertion — OK** |
| `Modules/Assign/Tests` | 1 ca skipped | 1 ca skipped (y hệt) |
| `Modules/Finance/Tests` | 121 ca — 1 error `BorrowSellStoreTest::test_returning_qty_excludes_parent_request`, 1 failure `PrepickTrackingApiTest::test_export_tree_indent_and_bold_per_level` | y hệt (đỏ sẵn, không liên quan giá) |
| `Modules/Human/Tests` | 14 ca — 2 failure (`CatalogImportFixesTest`, `ProvinceImportValidationTest` — validate import) | y hệt |
| CustomerCare | không có test | — |

24 ca mới: `ProductPriceReaderTest` 7 · `PriceReadPointsTest` 8 · `ProductPriceSetWriteTest` 7 · `PriceReaderWhitelistTest` 2.
Kiểm test bắt lỗi (đặt lại code cũ tạm thời rồi hoàn nguyên): Finance/CC cũ ⇒ 7/8 ca đỏ; MasterData ghi cũ ⇒ 5/7 ca đỏ;
B0 cũ ⇒ ca B0 đỏ; bỏ tham số công ty 1 lời gọi Assign ⇒ ca chốt lời gọi đỏ.

## Lệch design / ghi chú

1. **Cờ tắt ghi chỉ `upp` của chủ** (design §5.3 ghi đủ bộ cho mọi công ty) + lệnh `complete-sets` mới — xem quyết định cờ.
2. Cờ tắt Finance/CC đọc "giá chủ hàng" (NULL hoặc = chủ) thay vì "không lọc như cũ" — y hệt trên DB chưa backfill, chống nhân dòng sau đó.
3. Test "mọi điểm đọc": F1–F6, C1 (popup), C2 (`productLineInfo`), C3, A3 (`repriceErpItems`), A6, H1–H6 có ca 2 công ty end-to-end.
   A1/A2/A4/A5/A7/A8/A9 + C2 `deviceErrorDetailsByIds` KHÔNG có ca end-to-end riêng: các điểm này chỉ gọi helper H1–H5 (đã test 2 công ty)
   — chốt bằng test quét `moi_loi_goi_helper_gia_human_deu_truyen_cong_ty` (mọi lời gọi truyền đủ tham số công ty) + helper ném lỗi khi thiếu.
   Cờ tắt của nhóm Assign = đường `mysql2` cũ không đổi (test với mẫu thật bên `erp2326`).
4. `ProductUnit::prices()` (không dùng ở đâu) đổi thành `pricesOfCompany($companyId)`.
5. Quét danh sách trắng bỏ chú thích PHP (tránh khớp nhầm docblock) và bắt thêm đọc hệ số `pcc` nhiều dòng.
6. `productUnits()` Finance nhận tham số `?int $companyId` tường minh nhưng controller chưa truyền (FE chưa gửi) ⇒ dùng công ty người dùng.
7. `BackfillQuotationProductUnitIdSeeder`: chỉ đọc ĐVT gốc, không đổi (chỉ ở danh sách trắng).
8. e2e Playwright hàng hoá 2-C (design G2 nghiệm thu) **chưa chạy** — không đụng FE, chờ user yêu cầu.

## Việc ngoài luồng (ghi lại, không vá)

- **N71** `CompanyPriceComparator` so mọi cặp hàng status 1 × cụm ⇒ cặp do HRM tạo/lấy về (trạng thái 1) sẽ ra lệch "thiếu trạng thái"
  / giá 0. Cần loại cặp đã có trạng thái trước backfill (như B4/B5) trước khi dùng `compare = 0` làm cổng bật cờ.
- **N72** Backfill B4 chèn `pcc` chủ với 4 ô quản trị NULL ⇒ `AdminData::source()` lấy dòng ⇒ bảo hành / tồn tối thiểu của hàng cũ
  hiện trống thay vì cột chung `products` (`AdminData` `@TODO-BACKFILL`, chưa gỡ vì cột chung chưa xoá).
- **N73** `BorrowExportRequestTestDataSeeder` nối thẳng `product_unit_prices` không kẹp công ty (seeder test).
- **N74** 4 helper Human cờ tắt đọc `mysql2` = DB ERP CŨ `erp2326` (nợ gộp DB) ⇒ hàng tạo ở HRM không có giá ở báo giá/BOM khi cờ tắt.
  Cờ bật thì đã đọc DB gộp.
- **N75** `e2e_provision.php` mã hàng 3920 là id `erp2326`; cờ bật đọc DB gộp theo id đó.

## Cần user quyết

- **Q-G2-1** Chấp nhận quyết định cờ tắt (chỉ chủ có dòng giá, bù bằng `complete-sets` trước khi bật cờ) + bổ sung bước vào runbook §2.4?
- **Q-G2-2** N71 (compare loại cặp HRM) làm ở đợt nào — trước khi chạy backfill thật?
- **Q-G2-3** N72 AdminData sau backfill B4 — sửa ở G1 backfill (chép 4 ô từ `products`) hay ở `AdminData` (lùi theo từng ô)?
- **Q-G2-4** Push `feat/chuyen-doi-hang-hoa` (đang có G1 + fix fixture + G2 chưa push)?
