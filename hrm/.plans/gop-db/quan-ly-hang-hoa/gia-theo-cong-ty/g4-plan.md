# G4 — Màn "Cập nhật giá bán" HRM (checkpoint 10/10/2026)

> Phạm vi user cho phép: hrm-api + hrm-client worktree `wt-chuyen-doi-hang-hoa`, nhánh `feat/gia-cty-g4-cap-nhat` (từ
> `feat/chuyen-doi-hang-hoa`: api `98a59deff`, client `9b05f7b42`), merge `--no-ff` LOCAL. KHÔNG push, KHÔNG gop_db, KHÔNG ERP.
> DB `hrm_erp_giacty` — KHÔNG migration; quyền 1657 chèn bằng lệnh riêng (không chạy cả seeder).

## Trạng thái — ✅ xong cả 8 task

| # | Task | |
|---|---|---|
| 1 | Đọc nguồn + skill + khảo sát code | ✅ |
| 2 | BE list/stock/update/histories + quyền 1657 (seeder) + lịch sử bảng gated | ✅ |
| 3 | PHPUnit 30 ca + toàn bộ MasterData trên giacty | ✅ 310/310 |
| 4 | DB giacty: quyền 1657 + role e2e | ✅ |
| 5 | FE page + bảng + model T1–T11 + popup lịch sử/công thức + menu Finance | ✅ |
| 6 | Playwright MCP 1440 + 1280, SQL trước/sau, trả giá cũ | ✅ |
| 7 | Spec e2e `wt-chuyen-doi-hang-hoa/e2e/tests/master-data/product-prices-ui.spec.ts` (6 ca, `--list` OK, CHƯA chạy) | ✅ |
| 8 | Commit + merge local | ✅ |

## Commit

| Repo | Nhánh G4 | Merge `--no-ff` vào `feat/chuyen-doi-hang-hoa` |
|---|---|---|
| hrm-api | `218f80436` API + quyền + test · `494837d87` perf lọc duyệt | **`8b2c96aea`** |
| hrm-client | `dcccb38a7` màn + menu | **`2454cd867`** |

## File

- API mới: `Modules/MasterData/Services/ProductPrice/{ProductPriceListService,ProductPriceUpdateService,ProductPriceHistoryService}.php`,
  `Http/Controllers/V1/Product/ProductPriceController.php`, `Tests/Feature/ProductPriceScreenApiTest.php`.
- API sửa: `Routes/api.php` (nhóm `product-prices` gate 1657), `app/Services/CatalogHistoryService.php` (`GATED_TABLES` + `action_labels`
  — route chung `catalog-histories` vẫn chỉ nhận `TABLES` ⇒ `product_prices` 400), `PermissionsTableSeeder.php` (+1657),
  `tests/fixtures/price-readers.txt` (+3 file), `Tests/Feature/Concerns/ActsAsProductUser.php` (map 1657).
- Client mới: `pages/finance/product-prices/index.vue`, `components/product/price/{ProductPriceTable,ProductPriceHistoryModal,ProductRecipeModal}.vue`,
  `utils/productPriceModel.js`. Sửa: `components/subsystem-menu/finance.js`.

Endpoint: `GET master-data/product-prices` · `GET …/stock?product_ids=` · `PUT …/{product}` · `GET …/histories/{product}` (+`/filter-options`).

## DB `hrm_erp_giacty` — dòng đã chèn (không đụng `hrm_erp`)

- `permissions` id **1657** `Cập nhật giá bán hàng hoá` (api, group Hàng hoá, type 9).
- `roles` id **105473** `E2E Giá bán G4`; `role_has_permissions` (1657, 105473, company 1) + (1657, 105473, company 2);
  `employee_has_roles` (105473, e2e_assign 1180, company 1) + (…, company 2). Role 18 Super admin KHÔNG được gán.
- Tạm trong lúc kiểm (đã trả): `employee_infos.company_role` của 1614 = 2 → NULL; `pcc` 12499 status 4 → 3;
  giá TEWI-AQUA (product_unit 3, Cty 1) sửa → REPLACE nguyên dòng từ dump (md5 Cty1 `8d4b0e14…` = trước); xoá 2 giá hiệu lực
  108049/108050 + log `catalog_histories` 3783. Cty 2/3/4 md5 không đổi suốt quá trình.

## PHPUnit (giacty)

`ProductPriceScreenApiTest` 30 ca / 212 assertion (quyền 403 đọc-ghi-lịch sử · bỏ qua company_id request · chỉ Đang KD tại
công ty · bộ giá + pcu đúng công ty · công ty chưa dùng không thấy/403 · giá chờ duyệt hiện ở ô, `*_old` = giá chạy · lọc duyệt
chỉ cờ công ty mình · tồn/lọc Còn-Hết kho công ty, loại stock_id NULL · chỉ giá hiệu lực tương lai · 423 ×3 trạng thái · 404 ·
công ty bật duyệt ⇒ 423 · validate đồng thời câu ERP · đủ 6 loại + ĐVT thuộc hàng · ghi đúng công ty, B không đổi · TMĐT ×1,3/ĐMGG 0 ·
sửa tay giữ · xoá cờ chờ duyệt · BB3 sinh dòng · giá vốn vào pcu, product_units/pcc/norm/note không đổi · giá hiệu lực tạo + TMĐT suy
+ created_by · sửa tại chỗ/xoá dòng không gửi/giữ status 1 (BB4) · bỏ hiệu lực bán lẻ ⇒ xoá TMĐT · ĐVT phụ · Q2 xoá pa/pap
công ty mình, giữ của B · lịch sử 1 dòng, lưu lại không log rác, nhãn "Cập nhật giá" · route chung 400, công ty khác không thấy).
Đột biến kiểm test bắt lỗi (bỏ kẹp công ty ở pcu/tồn/trạng thái) ⇒ 4 ca đỏ. Toàn bộ MasterData **310 ca OK** (trước 280).

## Playwright MCP (Nuxt 3031 + API 8031, đo DOM)

| Đo | 1440 | 1280 |
|---|---|---|
| thead tr / chiều cao th / th cắt chữ / số cột / ⓘ | 1 / 34 / 0 / 14 / 5 | 1 / 34 / 0 / 14 / 5 |
| đáy tiêu đề = đỉnh dòng 1 | 299 = 299 | 299 = 299 |
| vùng cuộn dọc / trang cao | 1 / 900 = 900 | 1 / 900 = 900 |
| footer dưới đáy vùng cuộn | 828 ≥ 822 | 828 ≥ 822 |
| cuộn dọc 700: th dính đỉnh vùng cuộn | 265 = 265 | 265 = 265 |
| cuộn ngang 500: ô Tên dịch | 0px | 0px |
| thanh cuộn trên = scrollWidth bảng | 1812 = 1812 | 1812 = 1812 |
| rowSpan ô Tên = số tr khối | 6 = 6 | |

- Phép tính (TEWI-AQUA giá vốn 195,989,760): hệ số Bán lẻ 1.5 ⇒ 293,984,600 (loại 2–5 cùng), TMĐT 382,179,980 / 1.95, giá công thức
  TMĐT 382,180,000; giá 120,000,000 ⇒ TMĐT 156,000,000; ĐMGG 8 lan 2–5, TMĐT 0; hiệu lực hệ số 1.4 ⇒ 274,385,664 (không tròn) — khớp mockup
  (node chạy model với số mockup ABAC: 129,750,000 / 168,675,000 / 156,000,000 / 135,000,000 / 126,000,000 / 163,800,000).
- Validate: 3 lỗi đồng thời (giá vốn trống, hệ số 100, ngày hiệu lực trống), toast "Có 3 ô chưa hợp lệ…", 0 PUT, focus ô giá vốn.
- Lưu: bấm 2 lần ⇒ 1 PUT 200, toast, SQL Cty 1 đổi đúng (loại 2 = 320,000,000 theo giá vốn mới), Cty 2/3/4 md5 không đổi, 2 giá hiệu lực
  (bán lẻ + TMĐT 356,701,363), created_by 1180. Popup lịch sử 800px, nhãn "Cập nhật giá", thêm mới/sửa thông tin đúng.
- Khoá: đặt Ngừng KD sau khi tải ⇒ PUT 423, 25/25 ô disabled nền rgb(241,245,249) chữ rgb(71,85,105), không nút Lưu, ghi chú khoá.
- Chưa lưu: đổi bộ lọc / đổi ĐVT / rời route đều hỏi; "Ở lại" giữ giá trị, "Bỏ thay đổi" bỏ nháp.
- Công ty 2 (company_role tạm): giá Cty 2 (341,000,000 / giá vốn 195,989,760), 0 lịch sử của Cty 1.
- Không quyền (e2e_cmd_noperm): URL ⇒ /pages/extras/404, 0 bảng, 0 request product-prices; dashboard "Quản lý giá - CTKM 4 chức năng"
  (có quyền: 5 mục, panel 2 cột x 466/878).
- Console: chỉ 404 `e2e.png` (ảnh đại diện user, có sẵn) + 423 cố ý; cảnh báo HMR. Ảnh: `ERP-HRM/.playwright-mcp/g4/*.png`.

## Lệch design / mockup (tự chốt, cần user nhìn)

1. Đường lịch sử `master-data/product-prices/histories/{product}` (design ghi `…/{product}/histories`) — để dùng nguyên `SystemInfoSection`.
2. Công ty bật duyệt giá ⇒ BE 423 "chức năng gửi duyệt giá chưa mở" (nhánh gửi duyệt = G5); FE đổi nhãn nút "Gửi duyệt" theo cờ. Hiện cả 8 công ty `is_company_price = 0`.
3. BE bắt đủ 6 loại giá (`prices` size 6) — ERP chỉ `min:1`; FE luôn gửi 6.
4. Lưu thường xoá "Lý do không duyệt" (`approve_comment`) — theo mockup; ERP giữ.
5. Quyền 1657 `type 9` group "Hàng hoá" theo design §6.2 — skill erp-to-hrm-screen bảo `type` = phân hệ chính (Tài chính = 8).
6. Cột Hiệu lực 156px (mockup 140) vì V2BaseDatePicker có icon lịch; th cao 34 (app 33); badge cờ dùng V2BaseBadge thu nhỏ (U6).
7. Không dùng `filterStateMixin` (màn không có trang con cùng tab; tránh 2 `beforeRouteLeave`). Popup công thức lắp ráp không có cột
   "Code đặt hàng" (chi tiết hàng hoá không trả).
8. Lọc "Trạng thái duyệt" ~2,5s (quét cờ ~200k dòng giá, không index — không migration ở G4).

## Ngoài luồng (không vá)

- **N85** Rule toàn cục `translateY(-8px)` trên `.custom-control-label` (V2BaseCheckbox) — màn này ghim lại cục bộ.
- **N86** `V2BasePagination` ở 1280 cho "Số dòng/trang:" xuống 2 dòng (màn này ép nowrap cục bộ).
- **N87** Seeder quyền có sẵn ~17 id lặp (`uniq -d`: 7, 8, 16–21, 91, 94, 95, 102…) ở cả HEAD và `origin/develop` — không do G4.
- **N88** `ProductDetailResource` không trả "Code đặt hàng" của thành phần công thức lắp ráp.

## Cần user quyết

- Q-G4-1 Quyền 1657 để `type 9` (Hàng hoá) hay `type 8` (Tài chính)?
- Q-G4-2 Chấp nhận các lệch 1–4 ở trên? (đặc biệt 2: chặn 423 tới G5)
- Q-G4-3 Chạy spec e2e `product-prices-ui` (ghi DB giacty, tự trả giá) khi nào?
- Q-G4-4 Role tạm 105473 giữ cho G5 hay gỡ?
