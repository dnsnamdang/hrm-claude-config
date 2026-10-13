# Plan đợt C-a — Bảo mật + giá ERP (việc ngoài luồng) — 13/10/2026

> Nguồn: `soat-bang-c.md` (soát + 16 câu user chốt 13/10). Mục: **N61 🔴 · N59 · N62 · N68 · N60 · N63 · N67 · N54 · N58**.
> ✅ **User cho "LÀM" 13/10/2026** — đúng phạm vi mục 5.
> Môi trường: ERP worktree `websites/wt-erp-2d1`, nhánh chung ERP `feat/2d1-erp-khong-loi` @`f941467a49` (sạch; `origin/gop_db` đi trước **1** commit),
> `.env` trỏ `hrm_erp_giacty`. HRM: không sửa source ở đợt này.

## 0. Hiện trạng đo 13/10 (đọc code)

| Mục | Điểm sửa | Đo được |
|---|---|---|
| N61 | `ProductsController@getData` (`:3172-3180`), `getDataForJoin` (`:3426`→`Product::getDataForJoin` `Product.php:1378`), `getRecipe` (`:3441`, dùng `->data`), `ProductInfoController@getData` (`:1652`, route `product-infos/{id}/getData` `web.php:644`) | `dataFor()` (`Product.php:1268-1322`) + `getData()` (`:1325-1377`) trả `units` = `ProductPriceService::unitsInfoFor` (13 cột `ProductCompanyUnit::PRICE_COLUMNS`) + `lastest_export_price` + `'product' => $this`. `getDataForJoin` dùng `units_info` (cùng 13 cột). Server KHÔNG đọc các khoá này từ JSON (đọc accessor model `->lastest_export_price`); không model nào `$appends`. ~60 màn gọi, 0 màn JS dùng 13 cột / `lastest_export_price` (`soat-bang-c.md` §4). `company_id` request: chỉ Tồn đầu kỳ (kho) gửi (`beginning_stocks/create.blade.php:197`, select `Company::getForSelect()` = MỌI công ty đang hoạt động) |
| N59 | `ProductsController@getProductsAndPrices` `:2545-2548` | `orderBy($request->order['name'], $request->order['value'])` tự do; route `:595` không middleware (giá vốn trong đó đã gate quyền "Cập nhật nhanh giá hàng hóa" `:2337`) |
| N62 | `WrServiceQuotation.php:1018,1081,1097,1224,1325,1351` | `units[0]->prices[0]->price` — `units[0]` = ĐVT cơ bản, công ty người dùng; công ty chưa có giá ⇒ null ⇒ 500 |
| N68 | `app/Exceptions/Handler.php::render` | không xử lý `PriceNotFoundForCompany` (kế thừa `ModelNotFoundException`) ⇒ 404 trắng |
| N60 | `ProductExportsController.php:767` | `getPriceByUnitAndType($pid, $product->unit_coefficient /* null */, 1, …)` ⇒ giá ĐVT cơ bản |
| N63 | `app/Jobs/ResetProductPriceWhenZeroInventory.php`, `app/Jobs/SyncProductUnitPricesToCrm.php` | Job Reset: 0 nơi gọi (Command 14:30 thay). Job CRM: gọi ở `database/seeds/SyncDataToCrmSeeder.php:147`, `UpdateMissingDataToCRM.php:136` |
| N67 | `CompaniesController@postRegulations` `:436-442` + view `common/companies/regulation.blade.php:478-553` | ghi 6 cột `is_company_price, is_all_brand, brand_ids, is_new_company, is_new_brand, new_brand_ids` (+ xử lý `brand_ids`/`new_brand_ids` `:446-451`); route `web.php:490` không quyền |
| N54 | `ProductsController@getPriceOfProducts` `:3609-3617` | `>= 1000 ⇒ round(/1000)*1000` |
| N58 | `app/Console/Commands/UpdateProductPrice.php:74-82` | áp giá xong ghi `*_wait_approve` = giá mới + 3 cờ = 0 bất kể có yêu cầu chờ duyệt. Yêu cầu chờ duyệt (G5 HRM) = dòng `product_approves` + `product_approve_prices.product_unit_price_id` (duyệt/từ chối xong thì xoá dòng `pa` — đo 13/10 `pa` = 0) |

## 1. Thiết kế từng mục (tự chốt — ghi để duyệt)

**N61** — lọc ở TẦNG ENDPOINT, không sửa `dataFor()` / accessor `->data` (server-side chứng từ vẫn dùng):
- Thêm `Product::publicDataFor(int $companyId)` = `dataFor()` bỏ `lastest_export_price`, bỏ `product`, và mỗi phần tử `units` bỏ 13 cột `ProductCompanyUnit::PRICE_COLUMNS` (giữ `prices`, `base_price`, ĐVT). Helper tĩnh `ProductPriceService::stripSensitive($units)` dùng chung.
- `getData` ⇒ `publicDataFor(...)`; `getDataForJoin` ⇒ `units` = `unitsOnly` (màn ghép/tách chỉ cần ĐVT); `getRecipe` ⇒ `publicDataFor` từng NVL.
- `product-infos/{id}/getData` ⇒ gắn `productMovedToHrm:product-list` (màn duy nhất dùng — `product2.create` — đã chặn).
- `company_id` từ request: `DocumentCompany::resolveRequested($id)` — chỉ nhận nếu ∈ {công ty người dùng} ∪ `Employee::companies` (`company_employees`); ngoài ⇒ 403 "Không có quyền xem giá của công ty này". ⚠️ xem tồn C-a-1.
- Ngoài phạm vi (ghi lại): `getDataForInventory` / `getDataForAccountingInventory` / `getDataForPriceAsking` (đã chặn T7) — kiểm khi code, nếu trả 13 cột thì báo trước khi sửa.

**N59** — danh sách trắng cột sort: `p.name, p.code, pm.name, p.product_type, p.status` (đối chiếu cột FE `products/price_updating.blade.php` + `editPrices` lúc code); hướng chỉ `asc|desc`; ngoài danh sách ⇒ mặc định `p.name DESC`.

**N62** — 6 chỗ ⇒ `ProductPriceService::priceOrNull($pid, $unit_id của dòng, 1, DocumentCompany::ofOrUser($this))` (công ty phiếu), null ⇒ 0.

**N68** — `Handler::render`: `PriceNotFoundForCompany` ⇒ ajax/JSON trả **422** `{success:false, message}`; web ⇒ `back()->withErrors(message)`. Câu: giữ message sẵn có của exception (nêu mã / công ty / loại giá) + đuôi "— cập nhật giá ở HRM". Rà `catch (\Exception)` ở luồng tạo **báo giá, HĐ, YC xuất hàng** (3 luồng chính) để không nuốt message — chỉ sửa chỗ nuốt, không đổi cấu trúc.

**N60** — `:767` truyền `$l['unit_id']`; bỏ comment "N60 giữ nguyên". **Chỉ phiếu mới.** Đếm (SELECT) số dòng phiếu ghép/tách cũ có `unit_id` ≠ ĐVT cơ bản để báo user — không sửa dữ liệu.

**N63** — xoá 2 file Job + bỏ đoạn gọi Job CRM trong 2 seeder chạy tay (seeder giữ phần khác).

**N67** — bỏ 6 khoá khỏi `$input` + bỏ khối `:446-451`; view: ẩn thẻ cấu hình duyệt giá (`:478-553`), thay 1 dòng link "Cấu hình duyệt giá công ty đã chuyển sang HRM" → màn Quy định HRM (lấy URL đúng tab lúc code, dùng `HRM_URL_FE`). Phần khác của Quy chế giữ nguyên.

**N54** — trả `$price->price` nguyên số; sửa comment G3.

**N58** — trong vòng lặp cron: nếu `exists product_approve_prices pap join product_approves pa where pap.product_unit_price_id = $price->id` ⇒ chỉ ghi `price/coefficient/sale_max_percent`, KHÔNG đụng `*_wait_approve` + 3 cờ, log thêm "giữ yêu cầu chờ duyệt". Còn lại như cũ.

## 2. Kiểm

| # | Kiểm | Cách |
|---|---|---|
| K1 | PHPUnit ERP — test mới `tests/Feature/OutOfScopeCaTest.php` (hoặc tách theo mục): N61 (JSON getData/getDataForJoin/getRecipe KHÔNG có 13 cột / `lastest_export_price` / `product`; vẫn có `prices`, `base_price`; `company_id` ngoài danh sách ⇒ 403, trong danh sách ⇒ 200; `product-infos/{id}/getData` ⇒ trang moved) · N59 (cột lạ ⇒ không 500, sort mặc định) · N68 (ajax ⇒ 422 + message) · N54 (giá lẻ giữ nguyên) · N58 (dòng có pa giữ cờ; dòng không pa reset như cũ) · N60 (ĐVT không cơ bản lấy đúng giá) · N62 (thiếu giá ⇒ 0, không 500) | cả bộ ERP chạy lại; mốc đỏ sẵn = 1 (`ExampleTest`, N45 đợt C-c) |
| K2 | Playwright trên ERP thật (serve tạm cổng 8090 như G6, tắt đúng PID): (a) thêm hàng ở **Báo giá**, **YC xuất hàng**, **Tồn đầu kỳ kho** (chọn công ty khác), **YC xuất ghép**, popup **Công thức** YC đặt hàng — dòng hiện đủ ĐVT/giá, console sạch, đo response không có trường nhạy cảm; (b) **Quy chế công ty**: thẻ duyệt giá ẩn, có link HRM, lưu Quy chế không đổi 6 cột (so DB trước/sau); (c) **Báo giá DV BH-SC** thêm vật tư ĐVT không cơ bản — giá đúng; (d) **YC đặt hàng** lấy giá lẻ không làm tròn | đo bằng DOM + response mạng, không chỉ ảnh |
| K3 | Dữ liệu dev `hrm_erp_giacty` không đổi ngoài dữ liệu thử (CHECKSUM bảng giá trước/sau); dữ liệu thử dọn hết | như G6 |

## 3. Thứ tự

0. `git fetch` + merge một chiều `origin/gop_db` ⇒ `feat/2d1-erp-khong-loi` (quy trình memory: php -l file trùng + route:list + PHPUnit ERP), push nhánh chung — **đề xuất đầu đợt, cần user cho cùng lần "làm"**.
1. Nhánh con `feat/ca-bao-mat-gia-erp` từ `feat/2d1-erp-khong-loi`.
2. Commit theo mục: N61 → N59 → N54 → N62 → N60 → N68 → N58 → N63 → N67.
3. K1 ⇒ K2 ⇒ K3 ⇒ merge LOCAL vào `feat/2d1-erp-khong-loi`, **không push** tới khi user báo.

## 4. Tồn — hỏi lần lượt

| # | Câu | Đề xuất |
|---|---|---|
| C-a-1 | `company_id` "chỉ công ty user được thao tác" vs màn Tồn đầu kỳ cho chọn mọi công ty | ✅ 13/10 user: **CHẶT** — chỉ công ty chính + `company_employees`, áp mọi người. Tự chốt kèm: select Công ty ở 2 màn Tồn đầu kỳ (kho + kế toán) chỉ liệt kê công ty trong danh sách đó (không hiện lựa chọn bấm vào là 403) — thêm 2 view `beginning_stocks/create`, `beginning_accounting_stocks/create` vào phạm vi |
| C-a-2 | Có merge `origin/gop_db` vào nhánh chung ERP đầu đợt (1 commit mới) không | ✅ 13/10 user: **có**, merge một chiều đầu đợt; migration mới từ gop_db không tự chạy |

## 5. Phạm vi sẽ xin "làm"

| | |
|---|---|
| Repo / nhánh | **ERP** `wt-erp-2d1`: (0) merge `origin/gop_db` ⇒ `feat/2d1-erp-khong-loi` + push nhánh chung; (1) nhánh con `feat/ca-bao-mat-gia-erp`; merge LOCAL, không push |
| File ERP | `app/Product.php` · `app/Services/Product/ProductPriceService.php` · `app/Services/Product/DocumentCompany.php` · `app/Http/Controllers/ProductsController.php` · `app/Http/Controllers/Warehouse/ProductExportsController.php` (đường dẫn xác nhận lúc code) · `app/Model/Customers/WrServiceQuotation.php` · `app/Exceptions/Handler.php` (+ chỗ `catch` nuốt message ở 3 luồng) · `app/Console/Commands/UpdateProductPrice.php` · `app/Http/Controllers/Common/CompaniesController.php` · `resources/views/common/companies/regulation.blade.php` · `routes/web.php` (1 route `product-infos/{id}/getData`) · `resources/views/warehouse/beginning_stocks/create.blade.php` + `beginning_accounting_stocks/create.blade.php` (select công ty) · xoá `app/Jobs/ResetProductPriceWhenZeroInventory.php`, `app/Jobs/SyncProductUnitPricesToCrm.php` · `database/seeds/SyncDataToCrmSeeder.php`, `UpdateMissingDataToCRM.php` · test mới `tests/Feature/*` |
| HRM | Không sửa source. Chỉ `.plans/` |
| DB | `hrm_erp_giacty`: chỉ đọc + dữ liệu thử (tạo/dọn trong test, Playwright). Không migration, không seeder, không quyền mới. Không đụng `hrm_erp` |
| Không đụng | `gop_db`; HRM; cron khác; chứng từ cũ (N60 chỉ đếm) |

## 6. Kết quả code (13/10 — user "làm")

ERP `wt-erp-2d1`: (0) merge `origin/gop_db` ⇒ `feat/2d1-erp-khong-loi` `43c8a09fbf` (**đã push**, kéo 1 commit 32e217df48, lint sạch, route 115, PHPUnit 75/1 đỏ sẵn).
Nhánh con `feat/ca-bao-mat-gia-erp` 10 commit ⇒ merge `3432ca97ac` vào nhánh chung — **ĐÃ PUSH 13/10**; nhánh con đã xoá local. 28 file, +414/−470.

| Mục | Commit | Ghi chú |
|---|---|---|
| N61 | `3fcbf36a5c` + `7f3dd3e961` | `Product::publicDataFor()` + `ProductPriceService::stripSensitive()`; `getDataForJoin` giữ giá bán, bỏ cột pcu (thay vì `unitsOnly` của plan — an toàn hơn cho màn ghép/tách); `DocumentCompany::requested()/allowedForUser()`; route `product-infos/{id}/getData` ⇒ `productMovedToHrm:product-list` (116 route); `Company::getForSelectOfCurrentUser()` cho ô Công ty màn Tồn đầu kỳ kho (màn kế toán không có ô công ty, không gửi `company_id`) |
| N59 | `b373f1f1cc` | danh sách trắng `code→p.code, model_name→pm.name, name→p.name` (FE editPrices chỉ gửi code/model_name) |
| N54 | `e7e2ea24c5` | test R4 đổi kỳ vọng 2450. Bản sao làm tròn ở `Product2Controller`/`ProductTemplatesController::getPriceOfProducts` không có route; `ProductInfo`/`ProductTemplate::getDataAttribute` là bảng khác ⇒ không đụng |
| N62 | `e42f297894` | 14 dòng (6 giá + 8 định mức) dùng `priceOrNull` đúng ĐVT dòng; công ty giữ như G3 (sao chép = người dùng, sửa = công ty phiếu) |
| N60 | `0fd8894a5d` | đo: 3.085 dòng ghép/tách cũ **đều ĐVT cơ bản** ⇒ 0 phiếu cũ lệch |
| N68 | `27204dab75` | `userMessage()` (mã hàng, tên công ty, tên loại giá, hướng xử lý); Handler ajax 422 / web back + toastr; 6 khối `catch` (Báo giá, HĐ, YC xuất hàng × store/update) không bọc lại lỗi thiếu giá |
| N58 | `5408c052aa` | `UpdateProductPrice::hasPendingApproval()` (pap → pa; HRM xoá pa khi duyệt/từ chối — đã đối chiếu `ProductPriceApprovalService:471,601`) |
| N63 | `164fb432ff` | xoá 2 Job; bỏ khối đẩy giá ở 2 seeder CRM; `price-readers.txt` −2 |
| N67 | `51918163e3` | controller + `CompanyRegulationRequest` bỏ 6 cờ; view thay 2 thẻ bằng thẻ "Duyệt giá hàng hóa" link `HRM_URL_FE/sale/regulation-config` (màn HRM chưa hỗ trợ link thẳng tab — ghi chữ "tab Hàng hóa") |

**K1 PHPUnit ERP**: 86 ca (thêm `CaPublicProductDataTest` 5, `CaPriceNotFoundMessageTest` 4, `CaCronPendingApprovalTest` 2; sửa R4 + route 116) — chỉ đỏ sẵn `ExampleTest` (N45 đợt C-c). Chạy lại sau merge nhánh chung: như trên.

**K2 Playwright MCP** (ERP serve 8090 trên `hrm_erp_giacty`, `e2e_assign`, role tạm `CA_UAT_TMP` 117396 = Thêm báo giá · Xem công ty · Thủ kho — đã gỡ):
- 4 API từ phiên thật: `getData` 0 cột pcu / 0 `lastest_export_price` / 0 `product`, 6 loại giá bán; `?company_id=1` 200, `=2` **403**; `getDataForJoin` 0 cột pcu, 6 giá; `getRecipe` 5 NVL 0 rò; `product-infos/1/getData` 403 moved.
- Tồn đầu kỳ kho: ô Công ty **1** lựa chọn (trước 8); thêm hàng qua `addProduct` ⇒ `getData?company_id=1` 200, dòng TEWI-AQUA ĐVT "Bộ".
- YC xuất hàng, YC xuất ghép, Báo giá DV bảo dưỡng-sửa chữa, Báo giá hãng (VT-HH-TB): thêm hàng 0→1, ĐVT + 6 giá, 0 trường nhạy cảm, 0 pageerror. (Báo giá thường `quotations/create` đã tắt sẵn ở ERP — "Chức năng không còn được sử dụng".)
- N54: `getPriceOfProducts` hàng 4015 ĐVT 41 ⇒ **5.658.800** (trước làm tròn 5.659.000).
- N67: màn Quy chế công ty 1 — 0 ô cũ, thẻ link `_blank` đúng URL; lưu Quy chế (dữ liệu form thật + `is_company_price=1, is_all_brand=1, brand_ids=[1,2]`) gọi controller trong transaction ⇒ success, 6 cột vẫn 0/null; rollback.
- N58: `product:update_price 2099-01-01` thật trên giacty trong transaction rollback: dòng có yêu cầu giữ 777.777 + cờ 1, dòng không có reset; log có dòng "giữ yêu cầu chờ duyệt".
- N62: `getForEdit` + `getForCopy` 30 phiếu BH-SC thật không lỗi (màn sửa chỉ mở cho người lập — không vào được bằng e2e).
- Console: chỉ 404 ảnh logo/avatar local (có sẵn).

**K3 dữ liệu**: CRC32 từng dòng 8 bảng (pup, pcu, pep, pa, companies, company_employees, product_versions, product_histories) trước = sau; roles 129 · rhp 18.418 · ehr 1.720 về mốc; server 8090 tắt đúng PID 27385/27400; không log lỗi Laravel ERP hôm nay.

**Phát hiện thêm (note — chưa xử lý, ghi `viec-con-lai.md`)**:
- N77 (nghi, cần soát): trang SỬA/SAO CHÉP chứng từ nhúng `units` đầy đủ (vd `WrServiceQuotation::getForEdit` gán `unitsInfoFor()` có 13 cột pcu) vào JSON trang ⇒ giá vốn có thể lộ qua view-source — cùng loại N61 nhưng ở đường render trang, ngoài 4 API.
- N78: thẻ "Hàng reset giá" (`reset_price_when_zero_inventory_product_types`) vẫn ghi ở CẢ ERP Quy chế lẫn HRM tab Hàng hóa — cùng loại N67.
- N79: `WrServiceQuotation.php:1072,1308` biến `$service` chưa khai báo (cảnh báo "Creating default object") — lỗi cũ.

### Checkpoint — 2026-10-13 (C-a)
Vừa hoàn thành: đợt C-a 9 mục (code + PHPUnit + Playwright + checksum), merge LOCAL nhánh chung ERP `3432ca97ac`.
Đang làm dở: không. Role tạm đã gỡ, server 8090 đã tắt.
Bước tiếp theo: user soát · push nhánh chung ERP khi user báo · chọn đợt kế (C-b chặn ghi danh mục ERP / C-c lỗi cũ / C-d HRM / C-e N1 / C-f dữ liệu) + quyết N77–N79.
Blocked: —
