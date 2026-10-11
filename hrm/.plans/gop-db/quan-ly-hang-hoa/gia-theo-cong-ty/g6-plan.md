# G6 — ERP chặn màn giá + nghiệm thu tổng (checkpoint 10/10/2026)

> Phạm vi user cho phép (10/10): (1) ERP worktree `wt-erp-2d1`, nhánh `feat/gia-cty-g6-chan` từ `feat/2d1-erp-khong-loi` @ `5b3cdd032c`,
> merge `--no-ff` LOCAL; (2) hrm-api/hrm-client worktree `wt-chuyen-doi-hang-hoa`, nhánh `feat/gia-cty-g6` (gỡ lệch 1–2 G5), merge LOCAL về
> `feat/chuyen-doi-hang-hoa`; (3) nghiệm thu tổng trên `hrm_erp_giacty`; (4) chạy thử runbook trên bản sao tạm `hrm_erp_runbook` (dump từ
> `hrm_erp` chỉ đọc) rồi DROP. KHÔNG push, không gop_db, không seeder, không đổi `.env`.
> Bối cảnh 10/10: cả feature lên production 1 lần; PTG (Phase 7) + hàng tạm (Phase 6) cũng chuyển HRM ⇒ không thiết kế giai đoạn tạm.

## Trạng thái

| # | Việc | |
|---|---|---|
| 1 | ERP: middleware 10 route giá (W5/W6/W7) + đích `price-edit`/`price-approve` | ✅ |
| 2 | ERP: menu, nút products/list, expectedPrices, dashboard, link thông báo PTG/hàng tạm → HRM | ✅ (observer giữ nguyên theo lệnh giao) |
| 3 | ERP: PHPUnit + lint blade | ✅ 62 ca, 1 đỏ sẵn ExampleTest |
| 4 | HRM: gỡ lệch 1–2 G5 + test/spec | ✅ |
| 5 | Nghiệm thu: compare · snapshot · PHPUnit · e2e · Playwright ERP | ✅ (ca đỏ phân loại bên dưới) |
| 6 | Runbook thử + `runbook-trien-khai.md` + DROP | ✅ |

## Commit

| Repo | Nhánh G6 | Merge `--no-ff` LOCAL |
|---|---|---|
| ERP | `02568c4fc8` | `027fb570a2` → `feat/2d1-erp-khong-loi` |
| hrm-api | `a26d16602` | `0feda6059` → `feat/chuyen-doi-hang-hoa` |
| hrm-client | `790f1fa7b` | `06ec3a1e1` → `feat/chuyen-doi-hang-hoa` |

e2e (ngoài git): `product-price-approvals-ui.spec.ts` (+ assert pa.status NULL, API không `source`, 0 nhãn ERP) ·
`utils/productFixture.ts` (dọn `pap/pa/pep/pcu` trước `product_units` — FK bảng mới làm dọn rác hỏng) · `products-read.api.spec.ts`
(token nocost lấy theo cổng BASE_URL, trước ghim 3000).

## ERP (§5.7)

- `ProductMovedToHrm`: `price-edit` ⇒ `/finance/product-prices`, `price-approve` ⇒ `/finance/product-price-approvals`; trang báo câu riêng luồng giá.
- Chặn: `editPrices`, `updatePrice`, `manualUpdatePrices` (price-edit) · `approvePrices`, `approvePricesSearchData`, 4 `approve*Submit`,
  `approveExportExcel` (price-approve). Giữ: `getProductsAndPrices`, `priceUpdating`, `expectedPrices`, `price_logs`, `getPriceOfProducts`, `getData*`, PTG, hàng tạm.
- Menu "Cập nhật giá nhanh" ⇒ "Cập nhật giá bán (HRM)", "DS hàng hoá chờ duyệt giá bán" ⇒ "Duyệt giá bán (HRM)" (target _blank); nút
  products/list ⇒ HRM; bỏ nút Cập nhật (expectedPrices, D7); dashboard 2 thẻ ⇒ HRM (`?status=2`); link thông báo `route('products.approvePrices')`
  (hàng tạm `Product.php`, PTG, `ProductsController` ×2, `ManufactureExpectPriceMailJob`) ⇒ HRM. Observer: không đổi (lệnh giao "giữ nguyên").
- PHPUnit `G6PriceRoutesMovedToHrmTest` 6 ca + `ProductMovedToHrmRoutesTest` 56 ⇒ 66. Đột biến bỏ chặn `updatePrice` ⇒ 1 + 2 ca đỏ.
- Playwright (8090, `e2e_assign`): 5 GET ⇒ 403, đúng 1 link HRM đúng đích, `_blank`; AJAX searchData + 5 POST (có CSRF + X-Request-ID) ⇒ 403 JSON
  `redirect_url` đúng; `getProductsAndPrices`/`priceUpdating`/`expectedPrices` 200; menu "Cập nhật giá bán (HRM)" href 3031, 0 link cũ.
  **Chưa đo**: menu "Duyệt giá bán (HRM)" + 2 thẻ dashboard (gate quyền ERP `Duyệt giá hàng hoá` — e2e_assign không có; cấp role tạm bị bộ phân loại chặn).

## Nghiệm thu (hrm_erp_giacty)

- `compare`: 113.484 cặp, **0 lệch** (T4 449, §3.3 23.492), 13,6 s.
- `price:snapshot` after (code G6) = G3 after (khác duy nhất khoá `at`); diff vs before = đúng các nhóm chấp nhận (§3.6 + R3 140 + R4 242).
- PHPUnit hrm-api: MasterData **332 OK** · Assign 1 skipped · Finance 121 (1 lỗi `BorrowSellStoreTest` FK created_by=1, 1 đỏ
  `PrepickTrackingApiTest` thụt lề Excel) · Human 14 (2 đỏ validate import) — 4 ca ngoài luồng giá, module không đổi trong feature ⇒ đỏ sẵn.
  ERP sqlite 62 (1 đỏ sẵn ExampleTest).
- e2e (`--workers=1 --no-deps`, 8031/3031): xem bảng ca đỏ ở báo cáo. Dữ liệu: CHECKSUM 42 bảng trước/sau — trả `pcu` 10712/10717/10721
  (updated_by/at), xoá 31 dòng `catalog_histories` rác (30 e2e + 1 PHPUnit id 4156); còn khác `employees.login_count` (đăng nhập e2e).

## Ca đỏ e2e

| Spec | Kết quả | Phân loại |
|---|---|---|
| product-prices-ui | 6/6 | — |
| product-price-approvals-ui | 8/8 | — |
| products-read-ui 8/8 · products-form-ui 17 + 1 skip | xanh | — |
| products-catalog-popup-ui 6 + 1 đỏ · products-lifecycle-ui 8 + 1 đỏ + 1 skip | ca "KHÔNG quyền" INSERT `roles.company_id` không tồn tại | đỏ sẵn (schema gộp DB) |
| products-read.api | 1 đỏ: nocost được xem `/company` (200) | đỏ sẵn (quyền tài khoản nocost trên DB) |
| products-write.api E14 | GET edit hàng công ty khác 200 | đỏ sẵn (luật 2-C2: công ty tạo còn dòng pcc ⇒ coi là "đã lấy về") |
| **products-lifecycle.api A1, products-take.api A1, products-take-ui K3–K6** | không còn "mã ERP cũ chưa có dòng hệ số" / "mã sạch để lấy về" | **do giá theo công ty** (backfill đặt trạng thái 3 cho mọi hàng status 1 × 4 công ty cụm; không còn hàng ngoài cụm) — cần viết lại tiền điều kiện (Q-G6-1) |

## Trả lời user (10/10/2026) + làm tiếp

- **Q-G6-4 Observer**: ✅ GIỮ NGUYÊN `ProductWriteAuditObserver` (không gỡ 6 tên route giá khỏi danh sách trắng dù design §5.7 ghi bỏ — route đã chặn
  ở middleware nên danh sách trắng ghi của chúng vô hại).
- **Q-G6-3 Quyền 1657/1658**: seeder riêng `Modules/MasterData/Database/Seeders/ProductPricePermissionSeeder.php` (hrm-api nhánh
  `feat/gia-cty-g6-quyen` `5b327e085`, merge LOCAL `b282d0829`). Idempotent (đã có đúng tên ⇒ bỏ qua), type 8, nhóm Hàng hoá, KHÔNG gán role
  (khuôn `*PermissionSeeder` Finance gán Super admin 18 — cố ý không theo, vì super admin không có quyền mặc định); id/tên bị chiếm ⇒ ném lỗi,
  không ghi. PHPUnit `ProductPricePermissionSeederTest` 4 ca (transaction): DB thiếu ⇒ chèn đúng 2, chạy lại 0, thiếu 1 ⇒ chèn 1, chiếm id/tên ⇒ dừng.
  Chạy thật trên `hrm_erp_giacty`: "chèn 0 dòng", CHECKSUM `permissions`/`role_has_permissions`/`employee_has_permissions` không đổi. Runbook bước 6 đã cập nhật.
- **Q-G6-2 Đo ERP có quyền**: cấp tạm role 105600 `G6_E2E_TMP` (web; 100983 Duyệt giá hàng hoá + 100033 + 100127 @ Cty 1, gán e2e_assign `App\Employee`).
  DOM: menu "Duyệt giá bán (HRM)" href `http://127.0.0.1:3031/finance/product-price-approvals` `_blank`; "Cập nhật giá bán (HRM)" đúng; 0 link cũ.
  `/admin/approveList`: "Danh sách chờ duyệt giá hàng hoá" link `…/finance/product-price-approvals` (count 0 ⇒ view `ng-if count > 0` ẩn) ·
  "Hàng không được duyệt giá bán" link `…/finance/product-prices?status=2` count 20, có trong DOM. Gỡ role (3 bảng), CHECKSUM `roles`/
  `role_has_permissions`/`employee_has_roles`/`employee_has_permissions` khớp trước. `permission:cache-reset` ERP báo "Unable to flush cache" (redis — như 2-D1).
  Server 8090 tắt đúng PID.
- **Q-G6-1 Viết lại tiền điều kiện "lấy về"** (e2e ngoài git): helper `createProductOfCompany()` ở `utils/productFixture.ts` — tạo hàng thử E2EC1S
  bằng Cty 1 rồi chuyển hết dòng (products.company_id, pcc→status chủ, upp, pcu, NCC, catalog) sang Cty 4; tự kiểm Cty 1 còn 0 dòng + đủ bộ BB1
  của chủ. `products-take.api`: 3 hàng tự dựng ([2] chủ status 1 cho owner_not_trading), A6 kiểm dòng chủ vẫn 3. `products-lifecycle.api`:
  A2 hàng tự dựng; A3 mã ERP cũ = dòng backfill 3 (chỉ đọc, so trước/sau); A4 khoá hàng thử đặt 3 (cùng dòng → 4 → 3, không sinh dòng);
  thêm `product_company_units` vào kiểm bảng con khi xoá cứng. `products-take-ui`: beforeAll dựng 105 hàng Cty 4 (K3–K5 + K6 > 100).
  Chạy lại (`--workers=1 --no-deps`, 8031/3031): **take.api 6/6** (bỏ ca A5 "KHÔNG quyền" — đỏ sẵn `roles.company_id`; chạy đủ: A1–A4 xanh, A5 đỏ sẵn,
  A6–A7 "did not run") · **lifecycle.api 5 passed + A6 đỏ sẵn** (`roles.company_id`) · **take-ui 9 passed + N1 đỏ sẵn** (`roles.company_id`) ·
  lifecycle-ui 8 passed + N1 đỏ sẵn + 1 skip · write.api 5 passed + E14 đỏ sẵn (2-C2). Sửa thêm trong lúc chạy (lỗi spec, không phải code):
  sinh mã ≤ 99 mã/khuôn ⇒ rải 105 hàng qua 3 model; U4 lọc catalog theo Cty 1 + kiểm catalog công ty tạo không đổi. Không thấy lỗi code.
  Dữ liệu: CHECKSUM 42 bảng trước/sau khớp, trừ `employees` (login_count do đăng nhập e2e); 0 hàng E2EC1S, 0 role tạm còn lại. Server tắt đúng PID.
- Đỏ sẵn còn lại cần 1 đợt riêng: spec chèn `roles.company_id` (cột không có trên DB gộp) ở 5 ca "KHÔNG quyền" (take.api A5, lifecycle.api A6,
  take-ui N1, lifecycle-ui N1, catalog-popup-ui).
