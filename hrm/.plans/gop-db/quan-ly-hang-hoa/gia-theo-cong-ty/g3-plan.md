# G3 — ERP đọc/ghi giá theo công ty (checkpoint 10/10/2026)

> Phạm vi user cho phép: ERP worktree `wt-erp-2d1`, nhánh **`feat/gia-cty-erp`** (từ `feat/2d1-erp-khong-loi` @ `b2f1761789`).
> Commit LOCAL, KHÔNG merge / push / gop_db. DB `.env` worktree = `hrm_erp_giacty` (bản sao đã backfill + M3). Không migration /
> seeder / đổi `.env`. Không cờ, không đường lui (design "Đổi 10/10/2026 — BỎ CỜ").

## Trạng thái

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Lõi: `ProductPriceService`, `DocumentCompany`, `PriceSql`, `PriceNotFoundForCompany`, model `ProductCompanyUnit` | ✅ |
| 2 | R1/R2/R3/R7 lõi `app/Product.php` (dataFor/getData/unitsInfoFor/basePriceFor/getPriceByUnitAndType, màn hàng hoá ERP, Excel, báo cáo thanh lý) | ✅ |
| 3 | R4 `getPriceOfProducts` (bỏ k, giữ ≥1.000 tròn nghìn) · R5 popup 4 hàm + API HRM (join theo công ty, chỉ nhận `pcc.status = 3`) · R1.4 getData | ✅ |
| 4 | R1.5/R1.7/R2a–e/R3/R6/R7 caller bán hàng (33 file) + mua/kho/CSKH/báo cáo (57 file) | ✅ |
| 5 | R8 giá vốn `product_company_units` của công ty chứng từ + P8 chặn duyệt (6 luồng duyệt) | ✅ |
| 6 | Đường ghi: PTG (@TODO-PHASE7), duyệt hàng tạm (@TODO-PHASE6), cron 14:30 (P11), cron 01:00 + observer `company_id` | ✅ |
| 7 | PHPUnit sqlite (22 ca mới) + whitelist + sửa 2 test 2-D1 | ✅ |
| 8 | `price:snapshot` before/after | ✅ chỉ nhóm lệch đã biết + 2 nhóm cần xác nhận |
| 9 | Playwright | ✅ một phần (xem mục Playwright) |

## Commit (`feat/gia-cty-erp`, chưa push)

| Commit | Nhóm | File |
|---|---|---|
| `fe334ef9f4` | R0 lõi + R1/R2/R3/R7 lõi | 6 (5 mới + `Product.php`) |
| `8c87d2a4b8` | R4, R5, R1.4, R7 màn hàng hoá | 3 (`SearchController`, `ProductsController`, blade Excel) |
| `71d0aa02f7` | R1.5, R2a–d, R3, R6, R7 bán hàng | 33 |
| `855da22055` | R1.5, R1.7, R2d/e, R3, R7 mua hàng / kho / CSKH / báo cáo | 57 |
| `82476a88fd` | R8 + P8 | 18 |
| `3d07fadece` | Đường ghi (PTG, hàng tạm, cron 14:30, cron 01:00, observer, job clone) | 7 |
| `1d033d38f9` | Đường ghi: nhánh chờ duyệt hàng tạm gán price/coefficient = 0 tường minh | 1 |
| `30540fe9d7` | Test + whitelist + `price:snapshot` | 9 |

Tổng `b2f1761789..HEAD`: 132 file, +9.696 / −685 (gồm `tests/fixtures/g3-schema.json` ~64 KB).

## Quyết định kỹ thuật (tự chốt trong phạm vi design)

- `->data` load lại chứng từ ⇒ **`dataFor($cid)`** (hàm mới, CÙNG hình dạng JSON accessor `->data`). Design ghi "đổi thành `->getData($ct)`" nhưng
  `getData($cid)` trả bộ khoá khác (thiếu `manufacture_id`, `product_cate`, `product`…) ⇒ đổi sang getData sẽ vỡ view.
- `DocumentCompany::ofOrUser($doc)`: chứng từ chưa lưu ⇒ công ty người dùng; đã lưu ⇒ `company_id`, bảng không có cột ⇒ `created_by → employee_infos.company_id`;
  không xác định được ⇒ ném lỗi (không đoán). "Công ty người dùng" = `Auth::user()->info->company_id` (đã tôn trọng `session('current_company')` khi NV nhiều công ty).
- Cron/queue không Auth gọi accessor giá ⇒ `RuntimeException` rõ ràng (cron 01:00 nay truyền công ty dòng giá vào `getDataForVersion`).
- `getPriceByUnitAndType` / `base_price` thiếu dòng ⇒ `PriceNotFoundForCompany` (vẫn là `ModelNotFoundException` ⇒ 404 như `firstOrFail` cũ).
  Trong JSON `getData`/`dataFor`, `base_price` thiếu dòng ⇒ `null` (không làm hỏng cả form).
- Popup: không xác định được công ty ⇒ không hiện hàng nào. API `searchProductStockBuyerApi` lọc trạng thái theo `company_id` tham số (trước theo Auth).
- Danh sách hàng hoá ERP (`searchByFilter`): loại giá 1 đưa vào ON ⇒ hàng chưa có giá ở công ty vẫn hiện (giá trống) thay vì biến mất.
- P8 chặn ở: duyệt HĐ đại lý (Sale/Firm, Ztec, CRM), duyệt HĐ dự án (`ProjectContractsController`), duyệt phân tích giá dự án, duyệt hiệu lực BG dự án.
  Kiểm theo từng (hàng × ĐVT) dòng HĐ; câu báo: "Không thể duyệt: hàng hoá chưa có giá vốn tại công ty <tên> (<mã>…). Vui lòng nhập giá vốn ở màn Cập nhật giá bán (HRM)."
  Accessor giá vốn trả `null` khi thiếu dòng (tổng tính 0 ở màn xem; duyệt bị chặn).
- Cron 14:30 tách `resetCompanyPrices(company, product)` (test được trên sqlite vì `whereJsonContains` không chạy sqlite).

## PHPUnit (sqlite `:memory:`, không chạm DB thật)

`vendor/bin/phpunit` toàn bộ: **56 ca, 1 đỏ sẵn `ExampleTest`** (GET `/` qua `sso.check` ⇒ 302 — y hệt 2-D1, không liên quan).

- `G3CompanyPriceReadTest` 16 ca (106 assertion): mỗi nhóm R1–R8 có ca 2 công ty cùng ĐVT khác giá (Cty 2 có hệ số pcc 1.5 — phải KHÔNG nhân),
  đếm số dòng (không nhân dòng), resolver 5 bảng + thứ tự ưu tiên, cron 14:30, P8 (thiếu dòng chặn / giá vốn 0 hợp lệ).
- `G3CompanyPriceWriteTest` 3 ca (bảng giá giữ NOT NULL như MySQL): duyệt hàng tạm đủ 6 + 1 / ĐVT của công ty hàng tạm + `pcc` 3;
  chờ duyệt ⇒ không sinh 3, `pa.company_id` = công ty hàng tạm; PTG chỉ ghi bộ giá công ty quản lý.
- `G3PriceReaderWhitelistTest` 3 ca: 136 file khớp mẫu đều có lý do trong `tests/fixtures/price-readers.txt`; danh sách không phình; không còn nhân `pcc.coefficient` ngoài vùng chặn 2-D1.
- Đối chứng (sửa tạm rồi trả lại): bỏ lọc công ty ở `unitsInfoFor` ⇒ 2 đỏ · bỏ `pp.company_id` popup ⇒ 1 đỏ · cron bỏ công ty ⇒ 1 đỏ ·
  hàng tạm bỏ `company_id` ⇒ 2 lỗi · hàng tạm bỏ `pcc` 3 ⇒ 1 đỏ · PTG bỏ lọc công ty ⇒ 1 đỏ · thêm file đọc `product_unit_prices` chưa duyệt ⇒ whitelist đỏ.
- Sửa 2 test 2-D1 theo hành vi mới: `ProductPopupCompanyStatusTest` (chỉ nhận status 3) · `ProductBarcodeAndAuditTest` (observer 5 model + `company_id` trong log).
- Lint: `php -l` mọi file sửa; blade sửa biên dịch `Blade::compileString` + `php -l`.

## Snapshot §3.7

Lệnh `price:snapshot --sample=500 --popup-sample=60` (chỉ đọc: transaction `READ ONLY` + rollback).
- **before** = code `b2f1761789` (xuất bằng `git archive` ra scratchpad, KHÔNG thêm worktree), `DB_DATABASE=hrm_erp` qua biến môi trường (không sửa `.env`).
  Đếm 8 bảng (upp/pcu/pcc/products/pep/pu/product_versions/product_histories — số dòng + max cập nhật) trước/sau: **y hệt** ⇒ không ghi gì.
- **after** = code G3 trên `hrm_erp_giacty`, cùng mẫu (`--ids-from=before.json`).
- Mẫu 451 mã (5 nhóm × 100: k ≠ 1, k = 1, nhiều ĐVT, thiếu loại 5, có giá hiệu lực tương lai; trùng nhau gộp), × 4 công ty, đăng nhập NV 1 công ty
  (#24 Cty1, #328 Cty2, #408 Cty3, #222 Cty4). Popup: 60 mã × 4 hàm × loại 1, 3.

| Đường | Khớp | Lệch | Nhóm lệch |
|---|---:|---:|---|
| `->data` units/prices (R1, gồm giá hiệu lực) | 13.904 | 592 | loại 5 thiếu ⇒ nay có dòng giá 0 (§3.3/§3.6) |
| `getData($c)` units/prices | 13.904 | 592 | như trên |
| `base_price` trong JSON | 1.664 | 140 | mã k ≠ 1: cũ không nhân k ⇒ nay = giá đã nướng (**R3, cùng bản chất P10 — §3.6 chưa ghi**) |
| R2 `getPriceByUnitAndType` | 14.443 | 1.265 + 592 | P10 (k ≠ 1) · cũ lỗi 404 thiếu loại 5 ⇒ nay giá 0 |
| R4 `getPriceOfProducts` | 13.662 | 592 + 242 | thiếu loại 5 ⇒ 0 · **242 dòng giá cũ < 1.000 có k ≠ 1** (R4 không tròn khi < 1.000, vd 1 × 1.02 = 1.02) ⇒ nay = số getData (0) — **§3.6 chưa ghi** |
| Popup (4 hàm, R5) | 1.816 | 104 | dòng pcc k = 1 cũ tròn nghìn ⇒ nay số lẻ = getData (T4) |

**Không có lệch nào ngoài các nhóm trên.** 2 nhóm mới (R3 base_price; R4 giá < 1.000) đều là "nay ra đúng số getData", cần user xác nhận (Q-G3-2).
File: scratchpad `snap-before.json` (10 MB), `snap-after.json`, `snapdiff.py`, `snapdiff.txt`.

## Playwright (MCP, ERP worktree `php artisan serve` cổng 8090 trên `hrm_erp_giacty`, đã tắt đúng PID 51023/51033)

Tài khoản `e2e_assign` (Cty 1). Dữ liệu cấu hình tạm (đã xoá, đếm 11 bảng trước/sau KHỚP): role `G3_E2E_TMP` 105204 (3 quyền × 4 công ty),
`company_employees` 1239–1241 (Cty 2/3/4 — để đổi công ty qua `/admin/select-company/{id}`), `employee_manage_departments` 515, 516.

| Ca | Kết quả |
|---|---|
| Popup Báo giá dịch vụ (`sale/service_quotations/create`, `searchProduct` price_type=1) × 4 công ty, mã `ENEO-700-V5031` | Cty1 **1,265,000** · Cty2 **1,290,000** · Cty3 **1,303,000** · Cty4 **1,265,000** — đúng `pp.price` từng công ty, 1 dòng/công ty, ĐMGG 10 |
| Chỉ hàng Đang KD | từ khoá `MNSG-GPO12CE`: chỉ ra `:01` (42462, status 3 cả 4 Cty); **42460** (status 2, không dòng pcc — trước G3 vẫn hiện) bị ẩn ở cả 4 công ty. Danh sách popup không từ khoá: recordsTotal **28.355** |
| Giá dòng chứng từ sau khi chọn hàng | `getData` loại 1 = 1265000/1290000/1303000/1265000, **6 dòng giá** (không nhân dòng); ô giá dòng báo giá hiện đúng số đó ở cả 4 công ty |
| Hạch toán hỗ trợ HĐ đại lý **24527** (Cty 2, xem bằng phiên Cty 1) | "Giá vốn trước thuế" **18,532,580** = Σ giá vốn `product_company_units` Cty 2 × SL (8.028.787×2 + 825.002×3; cả 2 mã không có giá nhập ⇒ đi đường dự phòng pcu) |
| Phân tích giá HĐ dự án **27229** (Cty 1, type 4) | "Giá vốn trước thuế" **540,000** = 180.000 × 3 (pcu Cty 1) |
| P8 chặn duyệt khi thiếu dòng pcu | **KHÔNG kiểm bằng UI**: cần xoá tạm 1 dòng `product_company_units` (rồi trả lại) — bộ phân loại an toàn từ chối sửa dữ liệu nghiệp vụ. Chỉ có PHPUnit (`test_p8_*`, `missingCostError`). Cần user cho phép nếu muốn kiểm UI |

Hạn chế: số giá vốn ở 3 công ty cụm giống nhau (backfill chép nguyên giá vốn chủ) nên màn hạch toán chưa phân biệt được "đọc công ty HĐ" vs "đọc công ty người dùng" bằng số — phân biệt ở PHPUnit (Cty 1 = 700, Cty 2 = 900).

## Lệch / điểm cần biết so với design

1. `->data` ⇒ `dataFor` (không phải `getData`) — xem trên.
2. **R3 `base_price`** (và `data.base_price` trong JSON getData) cũ KHÔNG nhân hệ số (như R2) ⇒ sau khi giá đã nướng hệ số, đổi số ở mã k ≠ 1 — cùng bản chất P10 nhưng §3.6 chỉ ghi R2. (Snapshot đếm riêng nhóm này.)
3. Popup đổi từ "loại trừ" sang "chỉ nhận status 3": hàng ERP status 2/5 (7 mã) và mọi hàng ở Cty 5/6/7/8 không còn trong popup (đã chấp nhận ở T3/N70).
4. W5 `updatePrice` / W6 `manualUpdatePrices` / W7 Duyệt giá ERP **không sửa** (design §5.4: chặn route ở G6). Trong lúc chờ G6 các route này vẫn mở:
   `updatePrice` tìm dòng giá không lọc công ty (`first()`), ghi `product_units` 13 cột cũ ⇒ có thể ghi nhầm công ty trên `hrm_erp_giacty`.
   Đường đọc của màn (`getProductsAndPrices`, `getDataWithPrices`) đã theo công ty người dùng.
5. `units_for_history` (lịch sử ERP cron 01:00 / PTG / W5 / W7) vẫn đọc 13 cột cũ + giá mọi công ty (chỉ để so khác, QC-9 ngừng ghi lịch sử ERP) — N80.
6. Lọc khoá của popup/R4/getData theo công ty người dùng khi lập mới — form nào cho chọn công ty khác người dùng mà không gửi `company_id` thì vẫn lấy công ty người dùng (design: "= công ty người dùng khi form không cho chọn"; không sửa view nào).

## Ngoài luồng (N76+, chỉ ghi, không vá)

- **N76** §4.1 nên liệt kê thêm các bảng chứng từ không có `company_id` mà code đọc giá: `service_contracts`, `project_analysis`, `quotation_templates`
  (ContractAdditionAnnex/RuleContract/RuleContractAnnex dùng chung `contracts`) — `DocumentCompany` đã tự rơi về `created_by`.
- **N77** `ComboCategory.php:89,96` gọi `ComboCampaign::getDataForUse` không truyền công ty (theo người dùng).
- **N78** In mẫu báo giá (`QuotationTemplate`) `prices->filter()->first()->price` vỡ khi công ty người dùng không có dòng giá (vd Cty 7) — hệ quả lọc công ty.
- **N79** `getUnitLiquidation` bản `ProductInfo.php` / `ProductTemplate.php` (vùng chặn 2-D1) vẫn đọc cột cũ.
- **N80** `units_info` ngầm theo người dùng ở `BeginningAccountingStock:40`, `BeginningStock:48`, `HoldDetail:158`, `ProductTransfer:81` (chỉ cần ĐVT, nên đổi `units_only`);
  `units_for_history` đọc cột cũ (mục 5 trên).
- **N81** `WarehouseReportsController:2571` gọi `->price` trên null khi thiếu dòng giá (lỗi cũ, nay dễ gặp hơn); `PrepickTransfer2Controller:471` nhân `$pro['qty']` không tồn tại.
- **N82** Duyệt hàng tạm nhánh chờ duyệt từ trước không gán `price`/`coefficient` (NOT NULL) — MySQL non-strict ngầm ghi 0; đã gán 0 tường minh.
- **N83** Approve HĐ đại lý trả lỗi sớm (`overMaxExtraPricePercent`) mà không `DB::rollBack()` (transaction bỏ dở tới hết request) — lỗi cũ.
- **N84** Seeder ERP (`ProductSaleMaxPercentSeeder`, `ProductUnitSeeder`, `SyncDataToCrmSeeder`, `UpdateMissing*`, `UpdatePackagingIdForPricelist2907`,
  `UpdatePriceZitecProductsSeeder`) là script sửa dữ liệu 1 lần (2020–2025), không nằm trong `DatabaseSeeder` ⇒ không sửa; nếu chạy lại sẽ ghi giá không công ty.
- Import Excel hàng hoá, `product_templates`/product2, `CreateProductService`, `SyncProductInfoService`, `CreateProductUnitsAfterMapping` (bị chặn route 2-D1)
  vẫn ghi `product_unit_prices` không `company_id` ⇒ trên DB sau M3 sẽ lỗi 1048/1452 nếu ai mở lại route.

## Cần user quyết

- **Q-G3-1** Chặn route W5/W6/W7 ngay (kéo phần route của G6 lên) hay để G6? Hiện các route này ghi giá không theo công ty.
- **Q-G3-2** Chấp nhận 2 nhóm lệch snapshot chưa có ở §3.6: R3 `base_price` đổi ở mã k ≠ 1 (140 lượt/451 mã × 4 Cty) và R4 giá < 1.000 có k ≠ 1 (242) — cả hai nay = số getData?
- **Q-G3-3** Kiểm UI P8 (chặn duyệt khi thiếu giá vốn) cần xoá tạm/trả lại 1 dòng `product_company_units` trên `hrm_erp_giacty` — cho phép?
- **Q-G3-4** Merge `feat/gia-cty-erp` về `feat/2d1-erp-khong-loi` (local).

## Trả lời user (10/10/2026)

- **Q-G3-1** ✅ ĐỢI G6 — không chặn W5/W6/W7 trong G3. ⚠️ Trên `hrm_erp_giacty` **không dùng màn Cập nhật giá nhanh ERP**
  (`products/editPrices`, `updatePrice`, `manualUpdatePrices`, Duyệt giá ERP) cho tới G6 — các route này ghi giá không lọc công ty.
- **Q-G3-2** ✅ CHẤP NHẬN 2 nhóm lệch mới: R3 `base_price` mã k ≠ 1 (140 lượt) và R4 giá < 1.000 có k ≠ 1 (242 lượt) — nay = số getData.
  Đã bổ sung bảng §3.6 `design.md`.
- **Q-G3-3** ⏸ Cho phép kiểm P8 UI trên `hrm_erp_giacty`. Đã: kiểm `.env`/`getDatabaseName()` = `hrm_erp_giacty`, sao lưu dòng
  `product_company_units` id 11184 (hàng 3967 `TATE-TMS-1450`, ĐVT 73, Cty 4 — HĐ đại lý chờ duyệt 27684) ra scratchpad
  (`pcu-11184-backup.sql` dạng INSERT `--skip-tz-utc`, `pcu-11184-before.tsv`), tiền kiểm chỉ đọc: `overMaxExtraPricePercent` = false,
  `requiresBgdEscalation` = false ⇒ luồng duyệt sẽ tới chốt P8. **Dừng trước khi xoá**: muốn bấm Duyệt trên UI, e2e_assign phải được cấp
  role tạm (quyền xem HĐ) + làm quản lý phòng 108 (Cty 4) — bộ phân loại an toàn từ chối "Permission Grant". Chưa xoá/sửa dòng nào.
- **Q-G3-4** ⏸ Merge chờ Q-G3-3 theo thứ tự user giao.

### Q-G3-3 + Q-G3-4 hoàn tất (10/10, user cho phép cấp quyền tạm)

- DB = `hrm_erp_giacty`. Cấp tạm role 105205 `G3_E2E_TMP_P8` (quyền 100851, 100864 @ Cty 1) + quản lý phòng 108 (emd 517; 5 dòng quản lý cũ 123/239/254/267/275 không đụng).
- Xoá `product_company_units` 11184 (TATE-TMS-1450, Cty 4) → UI `firm-contracts/27684/support-accounting` bấm **Duyệt**: POST `/27684/approve` HTTP 200
  `success:false`; toast `.toast-warning` (nền rgb(248,148,6), x 1263 y 27, 150×156) "Không thể duyệt: hàng hoá chưa có giá vốn tại công ty CÔNG TY TNHH THIẾT BỊ
  TÂN PHÁT SÀI GÒN (TATE-TMS-1450). Vui lòng nhập giá vốn ở màn Cập nhật giá bán (HRM)." HĐ 27684 giữ status 2, approver NULL, updated_at 2026-09-14 20:31:03.
- Chèn lại 11184 từ backup (`--skip-tz-utc`): `diff` 21 cột trước/sau = giống hệt. Gỡ role 105205 + emd 517. 11 bảng đếm trước/sau khớp.
  `permission:cache-reset` báo "Unable to flush cache" (redis) — như 2-D1. Server tắt đúng PID 59467/59475.
- Merge `--no-ff` LOCAL `feat/gia-cty-erp` → `feat/2d1-erp-khong-loi` = **`5b3cdd032c`** (ahead 9, chưa push).
