# G5 — Duyệt giá bán HRM (checkpoint 10/10/2026)

> Phạm vi user cho phép: hrm-api + hrm-client worktree `wt-chuyen-doi-hang-hoa`, nhánh `feat/gia-cty-g5-duyet` (từ
> `feat/chuyen-doi-hang-hoa`: api `8b2c96aea`, client `2454cd867`), merge `--no-ff` LOCAL. KHÔNG push, KHÔNG gop_db, KHÔNG ERP.
> DB `hrm_erp_giacty` — KHÔNG migration; quyền 1657 (type 9→8) + 1658 chèn bằng lệnh riêng (không chạy cả seeder).

## Trạng thái

| # | Task | |
|---|---|---|
| 1 | Đọc nguồn + skill + khảo sát code | ✅ |
| 2 | BE: nhánh gửi duyệt (thay 423) + màn Duyệt (list/duyệt/không duyệt/hàng loạt) + Q1 + Excel + thông báo + D4 + quyền | ✅ |
| 3 | PHPUnit 22 ca mới + toàn bộ MasterData trên giacty | ✅ 332/332 |
| 4 | DB giacty: quyền 1657 type 8 / 1658 + role tạm 105473 | ✅ |
| 5 | FE: màn Duyệt + bảng + popup + menu + nhánh Gửi duyệt ở màn Cập nhật + D4 nhãn | ✅ |
| 6 | Playwright MCP 1440 + 1280 | ✅ |
| 7 | e2e G4 + spec duyệt mới (chạy) | ✅ 6/6 + 8/8 |
| 8 | Commit + merge local | ✅ |

## Commit

| Repo | Nhánh G5 | Merge `--no-ff` vào `feat/chuyen-doi-hang-hoa` |
|---|---|---|
| hrm-api | `a4ce81740` API + quyền + test · `c4c81ae44` Excel 0 ≠ ô trống | **`1952c2ee0`** |
| hrm-client | `b90c80b5c` màn Duyệt + Gửi duyệt + menu + D4 | **`1bef3ce9d`** |

## File

- API mới: `Modules/MasterData/Services/ProductPrice/{ProductPriceApprovalSubmitter,ProductPriceApprovalService,ProductPriceNotifier}.php`,
  `Http/Controllers/V1/Product/ProductPriceApprovalController.php`, `Exports/ProductPriceApprovalExport.php`,
  `Tests/Feature/ProductPriceApprovalApiTest.php`, `Tests/Feature/Concerns/FakesPriceNotifier.php`.
- API sửa: `ProductPriceUpdateService` (423 ⇒ nhánh gửi duyệt, tách `resolvePrices`), `ProductPriceListService` (brand_ids CSV,
  lọc `product_id`, `applyClassification` dùng chung), `ProductPriceHistoryService` (snapshot đề nghị, `logAction`, Q1 che giá vốn/hệ
  số), `app/Services/CatalogHistoryService.php` (`logUpdate(..., $action)`, `getLogs(..., $transform)` — tương thích ngược),
  `ProductPriceController@update` (message theo nhánh), `Routes/api.php` (nhóm `product-price-approvals` gate 1658),
  `RegulationTabRegistry` + `RegulationConfigService` (D4 option `manufactures`), seeder quyền, `price-readers.txt` (+2 file),
  test G4 (ca 423 ⇒ ca gửi duyệt), `RegulationHanghoaTest` (D4), `ActsAsProductUser` (map 1658).
- Client mới: `pages/finance/product-price-approvals/index.vue`, `components/product/price/ProductPriceApprovalTable.vue`.
  Sửa: `pages/finance/product-prices/index.vue` (popup Gửi duyệt, deep-link), `ProductPriceHistoryModal.vue` (prop `endpointBase`),
  `utils/productPriceModel.js` (helper duyệt), `components/subsystem-menu/finance.js`, `components/regulation-config/data.js` (D4 nhãn).
- e2e (ngoài git): mới `e2e/tests/master-data/product-price-approvals-ui.spec.ts`; sửa `product-prices-ui.spec.ts` (hằng `URL` che
  `new URL()` ⇒ đổi tên `PAGE_URL` — lỗi có sẵn của G4, spec G4 chưa từng chạy).

Endpoint: `GET master-data/product-price-approvals` (+`/filter-options`, `/export`, `/histories/{product}[/filter-options]`) ·
`POST …/{pa}/approve` · `POST …/{pa}/reject` · `POST …/approve` (items) · `POST …/reject` (ids).

## DB `hrm_erp_giacty`

- Giữ (dữ liệu đích): `permissions` 1657 type 9→8; INSERT 1658 `Duyệt giá bán hàng hoá` (api, Hàng hoá, type 8);
  `role_has_permissions` (1658, 105473, 1) + (1658, 105473, 2). Kiểm trùng: seeder HEAD/origin/develop/origin/gop_db + mọi nhánh remote
  + DB không có 1658 / tên trùng. Super admin không gán.
- Tạm trong lúc kiểm (ĐÃ TRẢ): `companies` id 1 `is_company_price` 0→1→0, `is_all_brand` 0→1→0 (brand_ids NULL giữ);
  yêu cầu pa 239/240/241 + pap (xoá), giá/cờ/pcu/giá hiệu lực của ĐVT 3/5/6 (hàng 3897/3899/3900) trả theo snapshot
  `scratchpad/snap-before.tsv` (md5 `99c4c5b9…`; sau trả: mọi cột giá trị trùng, chỉ `updated_at` đổi do UPDATE của spec e2e — đã đặt lại
  bằng script trả), `catalog_histories` id > 3920 bảng product_prices (xoá), `notifications` loại product_price_approve (xoá, còn 681 dòng
  như trước), `employee_infos.company_role` 1614 (spec N2 đặt 2 ⇒ trả NULL).

## PHPUnit (giacty)

`ProductPriceApprovalApiTest` 22 ca / 291 assertion: gửi duyệt giữ giá chạy + cờ đúng ô đổi + pa định dạng ERP (công ty bộ giá, status 1)
+ B không đổi + lịch sử submitted + thông báo đúng người/link · 1658 công ty khác không nhận · brand_ids CSV · gửi lại ghi đè / gửi đúng giá
chạy đóng yêu cầu · giá hiệu lực mới giá thật 0 cờ 1 · 403 mọi route không 1658 · Q1 ẩn giá vốn + hệ số (BE không trả) · công ty khác không
thấy · lọc người cập nhật / approve_id · đọc + duyệt pa định dạng PTG (không chép unit_coefficient — BB5) · duyệt đơn áp giá sửa + ngày qua ⇒
mai + xoá cứng + thông báo · Q1 duyệt giữ hệ số đề nghị · hàng loạt áp giá sửa từng yêu cầu (N56) · K9 cảnh báo · validate đồng thời 4 ô ·
không duyệt bắt buộc lý do, cờ 1→2 + thông báo `&status=2` · hàng loạt 1 lý do · P13/T3 công ty quản lý 2→1 + pcc 3 + đủ bộ giá / 2→5 ·
công ty khác không đổi status · công ty khác 404 · đã xử lý 404 · lịch sử Q1 · Excel số thật + cột theo Q1 · nội dung ≤ 50/120.
Đột biến (bỏ kẹp công ty / bỏ giá sửa / bỏ điều kiện công ty quản lý) ⇒ ca đỏ. Toàn bộ MasterData **332 OK** (trước 310).

## Playwright MCP (Nuxt 3031 + API 8031, e2e_assign — có 1657+1658, KHÔNG 1092)

| Đo màn Duyệt | 1440 | 1280 |
|---|---|---|
| thead tr / th cao / th cắt chữ / số cột (Q1) | 1 / 33 / 0 / 13 | 1 / 33 / 0 / 13 |
| có 1092 (giả lập chặn API thêm 2 trường) | 15 cột, th 34 (ⓘ), bảng 1744 | 15 / 34 / 1744 |
| đáy tiêu đề = đỉnh dòng 1 | 298 = 298 | 298 = 298 |
| vùng cuộn dọc / trang cao | 1 / 900 = 900 | 1 / 900 = 900 |
| footer dưới vùng cuộn | 828 ≥ 822 | 828 ≥ 822 |
| rowSpan ô Tên = số tr khối · cuộn ngang 400 ô Tên dịch | 2 = 2 · 0px | 2 = 2 · 0px |
| th 12px/700 rgb(10,124,136), đáy 2px rgb(32,217,234); z th 5 > td dính 2 | ✓ | ✓ |
| nút Duyệt rgb(26,188,156) / Không duyệt rgb(220,38,38), cao 32; chênh lệch tăng rgb(22,163,74) | ✓ | ✓ |

- Gửi duyệt (màn Cập nhật, TEWI-AQUA): nút "Gửi duyệt", popup liệt kê giá đổi, 0 PUT trước khi đồng ý, 1 PUT 200, toast
  "Đã gửi yêu cầu duyệt giá bán…", 6 badge Chờ duyệt; SQL Cty 1 giá chạy 341,000,000 giữ, wait 342,000,000 cờ 1; Cty 2/3/4 không cờ;
  pa 239 company 1 status 1; thông báo `[GIA] Chờ duyệt: <b>TEWI-AQUA – …(cắt 50)</b>. Người đề nghị: E2E Assign` link `?approve_id=239`.
- Hệ số 1.35 × giá vốn 1,000,000 ⇒ 1,350,000 (round trăm). Tick 2 → lọc mã còn 1 ⇒ "Đã chọn 2 yêu cầu (1 đang ẩn do bộ lọc)", ô tất cả
  checked; bỏ lọc ⇒ 2 vẫn tick, ô tất cả indeterminate.
- Không duyệt: lý do trống ⇒ "Vui lòng nhập lý do không duyệt", 0 POST, nút đồng ý đỏ; có lý do ⇒ 1 POST 200, SQL 6 cờ = 2, pcu
  approve_comment + approve_time; deep-link `/finance/product-prices?product_id=3897&status=2` ⇒ 6 badge Không duyệt + lý do.
- Duyệt (sửa giá 123,456,000): popup gọi tên mã, 1 POST gửi `rows` đã sửa ⇒ SQL Cty 1 = 123,456,000 cờ 0; md5 dòng giá Cty 2/3/4 không
  đổi; thông báo `[GIA] Đã duyệt … Giá mới áp dụng từ 10/10/2026` link `?product_id=3899`.
- Validate duyệt: giá trống + ĐMGG 150 ⇒ 2 lỗi đồng thời, toast "1 yêu cầu có ô chưa hợp lệ…", 0 POST, không mở popup.
- Deep-link `?approve_id=239` đã xử lý ⇒ toast "Yêu cầu đã được xử lý", bảng trống. Lịch sử ở màn duyệt: popup 800px, "Gửi duyệt giá".
- Menu: nhóm Quản lý giá - CTKM › Giá bán 6 mục (có Duyệt giá bán), Chờ duyệt có nhóm "Giá bán chờ duyệt" → "Hàng hoá chờ duyệt giá
  bán" mở đúng màn.
- Excel: 200, `Content-Disposition: …danh_sach_hang_cho_duyet_gia_ban.xlsx`; Q1 không cột Giá vốn/Hệ số; ô tiền kiểu n `#,##0`; letterhead
  local cần `ERP_URL` (companies.header tương đối — memory) ⇒ kiểm với ERP_URL: drawings=1, dữ liệu tụt 1 dòng đúng.
- Console: chỉ 404 `e2e.png` (có sẵn) + cảnh báo router/HMR. Đã sửa trong lúc kiểm: `errors` trùng computed toàn cục (vee-validate) ⇒ đổi
  `fieldErrors`; Excel ô 0 bị bỏ trống ⇒ `WithStrictNullComparison`.

## e2e

Node 20, `--project=chromium --no-deps --workers=1 --retries=0`, API_BASE 8031 / BASE_URL 3031 / API_REPO worktree, `.auth/user.json`
làm mới bằng `auth/login.setup.ts`. Lượt cuối (16:26–16:29): **`product-price-approvals-ui` 8 passed** (A1–A6, N1, N2) ·
**`product-prices-ui` (G4) 6 passed**. Các lượt trước đỏ vì lỗi SPEC (đã sửa, không phải lỗi app): hằng `URL` che `new URL()` (cả spec G4);
`browser.newContext` thừa hưởng storageState của project ⇒ ca "không quyền" vẫn đăng nhập E2E Assign (thêm `storageState` rỗng);
sau đăng nhập app quay `/login` 1 nhịp (chờ trang chọn phân hệ); chờ `keyword` rỗng; focus ô lỗi + nền ô khoá có độ trễ (expect.poll);
nút trong popup có glyph icon (bấm `.modal-footer button`). Một lượt chạy 36 phút do popup `beforeunload` treo trang.
Sau cùng: snapshot giá/pcu/giá hiệu lực/pa/pap/companies của 4 hàng thử **trùng byte** với trước (md5 `99c4c5b9…`), notifications 681,
catalog_histories không còn dòng > 3920 của product_prices, company_role NULL. Server 8031/3031 đã tắt đúng PID (80685+81006, 81069+con).

## Lệch design / mockup (tự chốt, cần user nhìn)

1. Đánh dấu nguồn yêu cầu bằng `product_approves.status = 1` (bản HRM sinh) — cột ERP không đường nào ghi/đọc; bản PTG/hàng tạm (status
   NULL) hiện badge "Từ phiếu tính giá ERP". Nếu PTG cập nhật lại 1 pa do HRM sinh thì vẫn mang nhãn HRM.
2. Duyệt/Không duyệt bản do PTG/hàng tạm ERP sinh: HRM VẪN báo người đề nghị (pa.updated_by) — D8 "không bắn thêm" hiểu cho chiều GỬI.
3. Thông báo "Chờ duyệt" gửi cả chính người gửi nếu người đó có 1658 (y ERP).
4. Giá hiệu lực ở nhánh duyệt: đổi NGÀY cũng tính là đổi (cờ 1 + dòng duyệt — như mockup); ngày ghi thẳng như ERP. Cờ không đổi ⇒ 0 (ERP giữ cờ cũ).
5. Gửi duyệt xoá "Lý do không duyệt" cũ (mockup); `pa.updated_by` = người gửi lần cuối (ERP chỉ đổi khi giá vốn đổi).
6. Duyệt/không duyệt KHÔNG tự sinh `pcu`/bộ giá cho công ty chưa có trạng thái (BB1); chỉ ca T3 công ty quản lý 2→1 mới sinh đủ bộ.
7. Nhãn nút "Không duyệt" theo mockup/ERP (skill button-convention khuyên "Từ chối").
8. Hàng loạt: yêu cầu đã bị người khác xử lý thì bỏ qua (trả `skipped`), không chặn cả lô.
9. Thanh hàng loạt: nút Bỏ chọn dùng tertiary. Màn Duyệt có cảnh báo "chưa lưu" khi rời màn còn ô đã sửa (unsaved-changes skill).

## Ngoài luồng (không vá)

- **N89** G4 `approvalRule` giải mã `brand_ids` bằng JSON trong khi ERP + màn Quy định lưu CSV ⇒ đã sửa trong G5 (đúng phạm vi vì là
  công tắc nhánh gửi duyệt) — ghi lại để biết G4 từng sai.
- **N90** Spec e2e G4 `product-prices-ui.spec.ts` có hằng `URL` che `new URL()` ⇒ mọi ca gọi `openAndSearch` lỗi ReferenceError (spec G4
  chưa từng chạy). Đã đổi tên `PAGE_URL` (e2e ngoài git).
- **N91** API `php artisan serve` đơn luồng + DB giacty: mỗi request 1–3s ⇒ bộ e2e duyệt ~30 phút; nên chạy e2e trên php-fpm/valet.
- **N92** `companies.header` Cty 1 trên giacty là đường dẫn tương đối, `.env` worktree không có `ERP_URL` ⇒ Excel/bản in local không logo.
- **N93** `scrollToFirstError` không focus ô `V2BaseCurrencyInput` lỗi (focus giữ ở ô vừa gõ) — gặp ở màn Duyệt khi ô Giá mới trống.
