# Plan đợt C-b — Chặn ghi danh mục hàng hoá ở ERP + lan thuế ở HRM — 13/10/2026

> Nguồn: `cb-khao-sat.md` (khảo sát + chốt C-b-1…5). Mục: N76, N32, N33, N42, N78.
> ✅ User cho "LÀM" 13/10/2026 — đúng phạm vi mục "Phạm vi xin làm".

## Task ERP (`wt-erp-2d1`, nhánh con `feat/cb-chan-ghi-danh-muc` từ `feat/2d1-erp-khong-loi`)
- [x] E1 `ProductMovedToHrm::TARGETS` thêm 9 đích (`product-models`, `order-codes`, `units`, `attributes`, `attribute-units`, `origins`, `attachment-types`, `color-codes`, `tax-rates`) → `/master-data/...`; đích `pi-*` trỏ cùng màn HRM tương ứng (attachment/color/tax không có pi).
- [x] E2 `routes/web.php`: gắn `productMovedToHrm:<đích>` cho ~45 route ghi 9 danh mục (create/store/fast/edit/update/delete/importExcel) + toàn bộ route ghi `pi-*` (6 nhóm, gồm 2 import ghi lọt); GIỮ route đọc + `unit.updateEnglishName` (C-b-3).
- [x] E3 N33: chặn `productTemShow`, `productTemHistory`, `proTemList`, `product_templates.searchData`, `.suggestions`, `.deleted` (đích `product-list`); giữ `products.exportExcelNorm/exportProduct`.
- [x] E4 Màn danh sách ERP 9 danh mục: bỏ nút Thêm/Import + cột/menu Sửa/Xoá (`searchData` từng controller) — khuôn brands. N42: `product_infos/list.blade.php:39` bỏ Thêm mới, `ProductInfoController.php:219-220` bỏ Sửa/Xoá.
- [x] E5 `topmenubar.blade.php`: 11 mục (9 + Thương hiệu + Hãng SX) ⇒ link `Tên (HRM)` `_blank rel=noopener` tới HRM; thêm mục ERP "Hãng SX – KPI & cấu hình" ⇒ danh sách Hãng SX ERP (C-b-1b); ẩn mục menu `pi-*` dòng 48-56 (giữ dòng 47 Hàng hoá có sẵn).
- [x] E6 Form Nhóm hàng hoá (`catalogs/groups/form.blade.php:162, 208`): ẩn nút "+" tạo nhanh thuế (C-b-5).
- [x] E7 N78: `CompaniesController::postRegulations` bỏ `reset_price_when_zero_inventory_product_types` khỏi `$data_include` (:431), `$input` (:438), khối gán csv/NULL (:441-445); `CompanyRegulationRequest` bỏ rule nếu có; `regulation.blade.php` bỏ thẻ "Hàng reset giá", gộp vào thẻ link HRM "Duyệt giá hàng hóa" (đổi chữ thành "Duyệt giá & reset giá hàng hóa").
- [x] E8 Test: `ProductMovedToHrmRoutesTest` (đếm route mới, bỏ assert `admin/pi-` không chặn, bỏ 6 route product_templates khỏi danh sách trắng, thêm `unit.updateEnglishName` vào trắng); test mới N78 (lưu Quy chế không đổi cột reset).

## Task HRM (`wt-chuyen-doi-hang-hoa/hrm-api`, nhánh con `feat/cb-thue-suat-lan` từ `feat/chuyen-doi-hang-hoa`)
- [x] H1 `TaxRateService::update` override: khi `tax_rate` đổi ⇒ 9 lệnh `DB::table` set-based (products × 4 cặp, product_templates × 4 cặp, groups × vat) trong transaction có sẵn của controller; `logCatalogUpdate` kèm `note` "Đã cập nhật % cho N hàng hoá / M hàng gốc / K nhóm".
- [x] H2 `TaxRate::childrenCount()` đếm thêm 4 cột products + 4 cột product_templates + groups.vat (chặn xoá thuế đang dùng).
- [x] H3 `TaxRateRequest` max 999,99 ⇒ 99,99 (C-b-5).
- [x] H4 Sửa comment lỗi thời `CatalogHistoryService.php:646-647` (BE). FE `master-data.js:133` chỉ là comment — ĐỂ NGUYÊN (không đụng hrm-client đợt này).
- [x] H5 PHPUnit `Modules/MasterData/Tests/Feature/TaxRatePropagationTest.php`: đổi % ⇒ 3 bảng cập nhật đúng dòng có id; đổi trạng thái không lan; không đổi `updated_at` khác; xoá thuế đang dùng ⇒ chặn; max 99,99.

## Kiểm
- PHPUnit ERP cả bộ; PHPUnit HRM MasterData cả bộ.
- Playwright ERP (8090, role tạm gỡ khi xong): menu 11 link HRM đúng `href` + `_blank` + mục "Hãng SX – KPI & cấu hình"; menu pi-* ẩn; 9 màn danh sách 0 nút ghi; POST/GET ghi ⇒ 403 + link HRM; Tổng hợp đặt hàng sửa tên TA ĐVT vẫn được (hoặc gọi route) ; form Nhóm hàng hoá không còn "+"; Quy chế công ty: không còn thẻ reset, lưu không đổi cột reset (transaction rollback); Hàng hoá gốc show ⇒ moved.
- HRM: sửa % một thuế suất thử trên giacty qua API (trong transaction rollback hoặc thuế thử tạo/xoá) ⇒ products/templates/groups đổi đúng; không đụng hrm-client nên không cần Playwright HRM.
- Checksum DB giacty trước/sau; bảng quyền về mốc.

## Phạm vi xin "làm"
| | |
|---|---|
| ERP | `wt-erp-2d1`, nhánh `feat/cb-chan-ghi-danh-muc`; file: Middleware ProductMovedToHrm, routes/web.php, topmenubar, ~10 view danh sách + controller searchData (9 danh mục + product_infos), catalogs/groups/form, common/companies/regulation + CompaniesController (+ CompanyRegulationRequest nếu có rule), tests; merge LOCAL, push khi user báo |
| HRM | `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/cb-thue-suat-lan`; file: TaxRateService, TaxRate entity, TaxRateRequest, CatalogHistoryService (comment), test mới; hrm-client KHÔNG đụng; merge LOCAL vào `feat/chuyen-doi-hang-hoa`, push khi user báo |
| DB | `hrm_erp_giacty`: chỉ đọc + dữ liệu thử tự dọn (hoặc transaction rollback); role tạm Playwright. Không migration, không seeder, không quyền mới |

### Checkpoint — 2026-10-13 (wrap up 5)
Vừa hoàn thành: khảo sát ERP + HRM, chốt C-b-1…5, viết plan.
Đang làm dở: không (chưa mở nhánh, chưa sửa source).
Bước tiếp theo: user cho "làm" ⇒ E1…E8 (ERP) + H1…H5 (HRM) ⇒ kiểm.
Blocked: chờ "làm".

## Kết quả code (13/10 — user "làm")

ERP `wt-erp-2d1` nhánh `feat/cb-chan-ghi-danh-muc` 5 commit ⇒ merge LOCAL `5cda1e2557` vào `feat/2d1-erp-khong-loi` (origin +5, **CHƯA push**):
`4a8c008b69` route (80 route mới, tổng 196) · `85f50e55db` menu + Nhóm hàng hoá · `10b26a93a3` N78 Quy chế · `5811a11346` 10 màn danh sách (agent, đã kiểm).
HRM api `feat/cb-thue-suat-lan` `73cef3429` ⇒ merge LOCAL `5d109a505` vào `feat/chuyen-doi-hang-hoa` (origin +2, **CHƯA push**). hrm-client không đổi.

Lệch so với plan / tự chốt khi code:
- `pi-units.updateEnglishName` cũng chặn (thuộc "chặn toàn bộ ghi pi-*"; không màn nào gọi). `unit.updateEnglishName` giữ (C-b-3).
- Nhóm route `attachment_types` có `checkPermission` cấp group từ trước ⇒ chạy trước middleware chặn (giống ngoại lệ manufacture_expect_prices); test thêm ngoại lệ.
- Ẩn cả 9 mục menu pi-* (gồm pi-groups / pi-brands / pi-manufactures) nhưng route ghi 3 nhóm đó KHÔNG chặn (ngoài phạm vi đã duyệt) ⇒ ghi chú N81.
- HRM `TaxRate::childrenCount`: đếm gộp GROUP BY 1 lượt/request (cột không index — từng dòng 2,4s/20 dòng ⇒ 0,29s/40 dòng).
- H4: chỉ sửa comment BE; comment FE `master-data.js:133` để nguyên (không đụng hrm-client).

Kiểm:
- PHPUnit ERP 89 (1 đỏ sẵn ExampleTest; ProductMovedToHrmRoutesTest 196 route). PHPUnit HRM MasterData **451/451** (+ TaxRatePropagationTest 4: lan đúng cột/dòng, chỉ đổi trạng thái không lan, chặn xoá thuế đang dùng, max 99,99).
- Playwright ERP (8090, role tạm `CB_UAT_TMP` 117846 — đã gỡ): menu 12 link HRM `_blank` đúng URL + "Hãng SX – KPI & cấu hình" ERP; menu pi-* chỉ còn "Hàng hoá có sẵn"; 10 màn danh sách 200 + searchData 200, 0 nút ghi, 0 icon sửa/xoá, 0 pageerror, số th khớp cột; nút lọc 4 màn đã dời vị trí gọi searchData 200; 9 thao tác ghi (POST/PUT kèm X-Request-ID) ⇒ 403 + `redirect_url` HRM đúng màn; GET create / Hàng hoá gốc list/show ⇒ trang "đã chuyển HRM"; `unit.updateEnglishName` 200; form Nhóm hàng hoá 0 nút "+", ô % VAT giãn 338/338px; Quy chế không còn thẻ reset, thẻ link gộp.
- N78 (tinker transaction rollback): lưu Quy chế gửi `[product,material]` hoặc không gửi field ⇒ cột HRM giữ nguyên `product`.
- Dữ liệu: CRC32 13 bảng trước = sau (units 39 bị test updateEnglishName chạm updated_at/by ⇒ khôi phục từ hrm_erp: 2020-09-03 10:27:18 / 194); bảng quyền về mốc; server tắt.
- Ghi chú: bộ PHPUnit HRM MasterData chạy trên giacty để lại `companies#1.updated_at/updated_by=999` (test Quy chế có sẵn, không phải code mới; cột cấu hình không đổi).

### Checkpoint — 2026-10-13 (C-b)
Vừa hoàn thành: C-b code + kiểm, merge LOCAL 2 repo.
Đang làm dở: không.
Bước tiếp theo: push khi user báo · quyết N81 (route ghi pi-groups/pi-brands/pi-manufactures còn mở) · đợt C-d (HRM).
Blocked: —

### N81 + push (13/10, user "Chặn luôn rồi push")
ERP nhánh `feat/cb-n81-chan-pi` `0544155f0c` (21 route pi-groups/brands/manufactures; đích mới `stopped-generic` cho pi-groups) ⇒ merge `42bbe92ae2`.
**ĐÃ PUSH**: ERP `feat/2d1-erp-khong-loi` @`42bbe92ae2`, HRM api `feat/chuyen-doi-hang-hoa` @`5d109a505`. Nhánh con đã xoá local. PHPUnit ERP 89 (1 đỏ sẵn), route 217.
