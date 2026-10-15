# Khảo sát đợt C-b — chặn ghi danh mục hàng hoá ở ERP (13/10/2026, chỉ đọc)

> Mục: N76 (8 danh mục Phase 1 + `pi-*`), N32 (Thuế suất: ERP chặn + HRM lan), N33 (ẩn Hàng hoá gốc), N42 (nút ghi `product-infos`), N78 (Hàng reset giá — chờ chốt).
> ERP `wt-erp-2d1` @`3f017e66dd`; HRM worktree `wt-chuyen-doi-hang-hoa` @657fa731f/dc793189e.

## 1. Khuôn đã có (Thương hiệu / Hãng SX, đợt 2-D1)
- Route ghi gắn `->middleware('productMovedToHrm:<đích>')` trước `checkPermission` (web.php:164-174, 231-241); đích ở `ProductMovedToHrm::TARGETS` (:30-53) — **chưa có đích** cho 9 danh mục.
- Menu brands/manufactures VẪN trỏ danh sách ERP chỉ xem (topmenubar:27-28); chỉ "Danh mục hàng hóa (HRM)" là link HRM `_blank` (:19).
- Danh sách: bỏ nút Thêm/Import + cột Hành động. Test `ProductMovedToHrmRoutesTest` (116 route; :329 khẳng định `admin/pi-*` KHÔNG chặn).

## 2. Theo danh mục (ERP) — URL HRM đích
| Danh mục | Route ghi cần chặn (web.php) | Route đọc giữ | pi-* | Menu ERP | HRM |
|---|---|---|---|---|---|
| Model | sale/models store/update/delete/importExcel (4261-4266) | index, searchData, search (dùng nhiều màn lọc) | sale/pi-models (4270-4277) | :21 / pi :48 | `/master-data/product-models` |
| Code đặt hàng | sale/barcodes store/update/delete (4281-4284) | index, searchData | sale/pi-barcodes (4287-4293) | :22 / :49 | `/master-data/order-codes` |
| Đơn vị tính | units create/store/fast/edit/update/delete/importExcel (264-274) + **updateEnglishName** (275) | index, searchData, export | pi-units (279-293) — importExcel GHI LỌT bảng `units` chính | :23 / :50 | `/master-data/units` |
| Thuộc tính | attributes create/store/edit/update/delete/importExcel (298-308) | index, byGroup, searchData, export | pi-attributes (312-325) — importExcel GHI LỌT `attributes` | :24 / :51 | `/master-data/attributes` |
| ĐV thuộc tính | uniteches create/store/edit/update/delete (329-333) | index, searchData, export | pi-uniteches (379-390) | :25 / :52 | `/master-data/attribute-units` |
| Xuất xứ | origins create/store/fast/edit/update/delete/importExcel (131-141) | index, getAll (appJs), searchData, export | pi-origins (145-158) | :29 / :56 | `/master-data/origins` |
| File đính kèm | common/attachment_types store/update/delete (827-829) | index, searchData | — | :30 | `/master-data/attachment-types` |
| Mã màu | code-color create/store/edit/update/delete (345-349) | index, searchData, export, print | — | :31 | `/master-data/color-codes` |
| Thuế suất | tax-rates store/update/delete (359-361) | index, searchData, exportExcel, getUpdaters | — | :32 | `/master-data/tax-rates` |

Nút ghi trên danh sách ERP cần bỏ: units/list:19-20 · origins/list:19-20 · attributes/list:31-33 · uniteches/list:19 · codeColor/list:68 · product_models/index:19-22 · barcodes/index:24 · attachment_types/index:18 · taxRates/index:~240-252 + cột Sửa/Xoá ở `searchData` từng controller.
HRM: 11 màn ở menu Danh mục dùng chung › Danh mục hàng hóa (`hrm-client/components/subsystem-menu/master-data.js:131-195`), Thêm/Sửa là popup, không nhận `?id=` ⇒ ERP chỉ trỏ trang danh sách.
Comment lỗi thời cần sửa: `master-data.js:133`, `CatalogHistoryService.php:646-647` ("ERP vẫn sửa cùng bảng").

## 3. "Thêm nhanh" danh mục trong chứng từ ERP
- Gần như toàn bộ là **code chết** (popup tạo hàng tạm / hàng dịch vụ không còn nút gọi, hoặc màn đã chặn): quotations/form:721-727, project_quotations:701, liquidation_quotations, service_quotations:900/926, tmp_product_requests, tmp_products/form.
- **Còn sống thật** 2 điểm:
  1. `#createTaxRate` ở form **Nhóm hàng hoá** (catalogs/groups/form.blade.php:162, 208; route groups chưa chặn — màn này sẽ gỡ ở Phase 5).
  2. `unit.updateEnglishName` ở 2 màn **Tổng hợp đặt hàng** (order_notification2/summary:126, inland_order_notification_new/summary:128) — sửa tên tiếng Anh ĐVT tại chỗ.

## 4. N33 / N42 / N78
- N33 Hàng hoá gốc: chưa chặn show (502), history (506), list (507), searchData (509), suggestions (510), deleted (521); `products.exportExcelNorm` / `exportProduct` (513-514) dùng ProductsController — GIỮ. Không có mục menu. Test giữ trắng 6 route (test:189-190) ⇒ sửa.
- N42 product-infos: mở show/index/searchData/searchData2; nút Thêm mới list:39 + dropdown Sửa/Xoá controller:219-220 trỏ route đã chặn.
- N78 Hàng reset giá: view regulation.blade:485-502; ghi ở CompaniesController :431 ($data_include — có lịch sử), :438, :441-445 (**request thiếu field ⇒ gán NULL**). ⚠️ Chỉ ẩn thẻ mà giữ code ghi ⇒ mỗi lần lưu Quy chế ERP XOÁ TRẮNG cấu hình HRM. HRM ghi được (RegulationTabRegistry:402-406, test RegulationHanghoaTest:140-175). Cron 14:30 dùng cột.

## 5. N32 Thuế suất — lan mức thuế
- ERP `TaxRatesController::update` → `dispatchUpdateJobs` (167-216): `products` + `product_templates` 4 cặp (`vat_percent_tax_rate_id→vat_percent`, `import_tax_tax_rate_id→import_tax`, `import_tax_has_co_tax_rate_id→import_tax_has_co`, `antidump_duty_tax_rate_id→antidump_duty`) + `groups` (vat). Job từng dòng `DB::table()->update` (không updated_at, không lịch sử). Lỗi: lan cả khi chỉ đổi status; `canDelete` bỏ sót product_templates.
- HRM: `BaseCatalogService::update` (:264-284) không có hook; controller `respondUpdate` bọc `DB::transaction` (:93-97). `QUEUE_CONNECTION=sync`. Form hàng hoá HRM tự tra `tax_rates` ra % (`ProductWriteService::fillCommon` :320-336). `product_types` chỉ lưu id (không cần lan). `product_projects` có `vat_percent_tax_rate_id` — ERP không lan, giữ như ERP.
- Đề xuất: `TaxRateService::update` override — lan khi `tax_rate` đổi, 9 lệnh UPDATE set-based (`DB::table`, không Eloquent vì `Product::boot updating`), cùng transaction; ghi `note` vào `catalog_histories` ("đã cập nhật % cho N hàng / M mẫu / K nhóm"); không ghi `product_histories` (như ERP).
- Rủi ro kèm: HRM `TaxRate::childrenCount()` chỉ đếm `product_types` ⇒ xoá được thuế đang dùng ở products/templates/groups; `TaxRateRequest` max 999,99 vs ERP 99,99.
- Test: chưa có — thêm `Modules/MasterData/Tests/Feature/TaxRatePropagationTest.php`; e2e `wt-chuyen-doi-hang-hoa/e2e/tests/master-data/product-catalog-*.spec.ts`.

## 6. Tự chốt (theo quyết định trước / khuôn)
- Mã màu + File đính kèm: THUỘC phạm vi chặn (user chốt N76 13/10 "chặn hết 8 danh mục").
- Đồng bộ CRM khi lưu danh mục: KHÔNG chuyển sang HRM (N6 user bỏ đồng bộ CRM 09/10).
- Màn danh sách ERP: bỏ hẳn nút Thêm/Import/Sửa/Xoá + cột hành động (khuôn brands; quy tắc "nút không dùng được thì ẩn").
- Include "thêm nhanh" chết: chỉ chặn ở route, KHÔNG xoá code trong đợt này (ghi note).
- Thuế: chỉ lan khi `tax_rate` đổi (không lan khi chỉ đổi trạng thái); HRM `childrenCount` đếm thêm 4 cột products + templates + groups (chặn xoá thuế đang dùng).
- N33: chặn show/history/list/searchData/suggestions/deleted Hàng hoá gốc (user chốt "ẩn hẳn"); N42: bỏ nút Thêm mới + dropdown Sửa/Xoá, giữ xem.

## 7. Câu hỏi — xem mục "Chốt" bên dưới (hỏi lần lượt)

## Chốt (user 13/10/2026)
| # | Câu | Đáp án |
|---|---|---|
| C-b-1 | Menu ERP 9 danh mục | ✅ **link sang HRM `(HRM)` `_blank`, đổi cả 11 mục** (9 + Thương hiệu + Hãng SX); màn danh sách ERP vẫn mở bằng URL (chỉ xem) |
| C-b-1b | 3 màn con chỉ có ở ERP của Hãng SX (KPI / Đại diện hãng / Cấu hình NV) | ✅ **giữ thêm 1 mục menu ERP** "Hãng SX – KPI & cấu hình" trỏ danh sách Hãng SX ERP |
| C-b-2 | Nhóm `pi-*` | ✅ **chặn toàn bộ ghi** (kể cả 2 import ghi lọt) + **ẩn menu pi-*** (giữ mục "Hàng hoá có sẵn" dòng 47 — N42 giữ xem); sửa assert test `admin/pi-` |
| C-b-3 | `unit.updateEnglishName` ở Tổng hợp đặt hàng | ✅ **giữ** (danh sách trắng như `product.updateEnglishName`) |
| C-b-4 (N78) | Hàng reset giá | ✅ **HRM duy nhất** như N67: ERP bỏ thẻ + bỏ hẳn code ghi (:431, :438, :441-445), gộp vào thẻ link HRM |
| C-b-5 | Thuế: nút "+" ở form Nhóm hàng hoá ERP; max | ✅ **ẩn nút "+"**; HRM `TaxRateRequest` max **99,99** |
