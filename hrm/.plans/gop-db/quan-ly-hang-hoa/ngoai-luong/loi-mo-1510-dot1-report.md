# Report đợt 1 (hrm-api) — lỗi mở 15/10: N82 · N84 · N86 (BE) · N91

Repo: `wt-chuyen-doi-hang-hoa/hrm-api`. Nhánh con `feat/cdhh-loi-mo-api` (từ `feat/chuyen-doi-hang-hoa` @ `b38852de0`)
⇒ merge `--no-ff` LOCAL về `feat/chuyen-doi-hang-hoa`: **`ca4a37802`**. Không push, không stash. Soát marker
xung đột (`git grep '^<<<<<<<|^>>>>>>>|^=======$'` trên *.php): 0. EOL: `git diff --numstat` không có dòng xoá ngoài
các dòng sửa chủ ý (các file đều LF).

## Commit

| Mã | Commit | Nội dung |
|---|---|---|
| N86 | `7673c278a` | `item-search` thêm tham số `exclude_locked` (mặc định tắt) |
| N91 | `bca4d0875` | dòng hệ số công ty `status IS NULL` lùi cột chung |
| N82 | `de7e4a442` | Excel báo giá trực tiếp mang `show_children` (mặc định 1) |
| N84 | `6b29356c4` | migration index `(product_id, life_id)` + đã chạy vào `hrm_erp_giacty` |
| merge | `ca4a37802` | Merge feat/cdhh-loi-mo-api |

## File

- N86: `Modules/MasterData/Http/Controllers/V1/Product/ProductOptionController.php`,
  `Modules/MasterData/Services/Product/ProductOptionService.php`; test thêm 1 ca vào
  `Modules/MasterData/Tests/Feature/ProductFormOptionsTest.php`.
- N91: `Modules/MasterData/Transformers/Product/AdminData.php` (`source()` + `mediaAndGuarantee()`),
  `Modules/MasterData/Services/Product/ProductExportService.php` (`$lk['own']` — khảo sát mục 3 ghi "nếu không lọc
  status": đo thấy KHÔNG lọc ⇒ sửa cùng luật, 1 dòng); test mới `Modules/MasterData/Tests/Feature/AdminDataNullStatusTest.php`.
- N82: `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` (`exportExcel`, nhánh `isDirectQuotation`),
  `app/ExcelExport/BomListExport.php:546` (`?? 0` ⇒ `?? 1` + sửa comment); test mới
  `Modules/Assign/Tests/Feature/QuotationDirectExportShowChildrenTest.php`.
- N84: `Modules/MasterData/Database/Migrations/2026_10_15_000001_add_product_life_index_to_product_vehicle_model_has_life_table.php`
  (guard `hasIndex`, `down()` drop); test mới `Modules/MasterData/Tests/Feature/ProductVehicleLifeIndexTest.php`.

## Test

Mỗi test mới đều chạy ĐỎ trên code cũ trước khi sửa (đã đo):
- N86: `Failed asserting that an array does not contain 3897` (khi có `exclude_locked=1`).
- N91: 3/4 ca đỏ (source, mediaAndGuarantee, Excel Kho dữ liệu) — ca "có status ⇒ đọc dòng riêng" xanh cả trước/sau (ca chặn hồi quy).
- N82: 2/2 đỏ với đúng lỗi gốc `400 Undefined property: stdClass::$show_children (View: bom_list.blade.php)`.

Sau sửa:
- `Modules/MasterData/Tests`: **OK 553/553** (5077 assertions) = mốc 546 + 7 ca mới (N86 1 · N91 4 · N84 2).
- `Modules/Assign/Tests` (chứa test QuotationController): **20 tests, OK, 1 skipped** (3677 assertions) — ca skip có sẵn,
  phụ thuộc dữ liệu: `ProductExportPostingRegressionTest::test_post_accounting_snapshot_stable` ("Không có ProductExport
  loại 20/21 gắn HĐ hợp lệ"), không liên quan đợt này.

Ca test chính:
- N86: không tham số / `exclude_locked=0` ⇒ hàng khoá ở cty đang làm VẪN ra; `exclude_locked=1` ⇒ bị bỏ; hàng khoá ở
  công ty KHÁC ⇒ vẫn ra dù có tham số.
- N91: dòng pcc NULL-status ⇒ `guaranteeText` "12 tháng" + `minStockQty` 3 (cột chung); dòng status 3 ⇒ "2 năm"/7;
  `mediaAndGuarantee` cả 2 chiều; Excel Kho dữ liệu (`warehouse/export-rows`) ra "12 tháng"/3.
- N82: báo giá trực tiếp, hàng cha ERP để `show_children` mặc định cột ⇒ 200 + file có mã hàng con; `show_children=0`
  ⇒ 200 + KHÔNG có hàng con (blade gập).
- N84: `SHOW INDEX` đúng 2 cột thứ tự `product_id, life_id`; EXPLAIN DELETE theo `product_id` dùng index (không `ALL`),
  EXPLAIN `product_id + life_id` ⇒ `ref`.

## N84 — migration + EXPLAIN

Chạy: `php artisan migrate --path=Modules/MasterData/Database/Migrations/2026_10_15_000001_…php --force` (đã
`config:clear`, xác nhận `DB::connection()->getDatabaseName()` = `hrm_erp_giacty`, `--pretend` trước). Kết quả
117,63ms, `migrations.batch = 438`. Index `pvmhl_product_life_index`.

| Truy vấn | Trước | Sau |
|---|---|---|
| `DELETE … WHERE product_id=5` | `type=ALL`, rows 48.817 | `type=range`, key `pvmhl_product_life_index`, rows 1 |
| `DELETE … WHERE product_id=7338` (hàng nhiều đời xe nhất, 7.582 dòng) | (ALL 48.817) | `range`, rows 13.644 (ước lượng) |
| `SELECT 1 … WHERE product_id=5 AND life_id=1` | `ALL`, rows 48.817 | `ref` (const,const), rows 1, Using index |
| Picker EXISTS `vl.product_id=products.id AND vl.life_id=1` | `vl` `ALL` 48.817, Start temporary | `vl` `index` (quét index phủ, LooseScan) 48.817, Using index |

Bảng 48.736 dòng / 91 hàng. Lưu ý dòng cuối: xem N113.

## Hợp đồng tham số `exclude_locked` (cho đợt FE)

`GET /api/v1/master-data/products/item-search`

| Tham số | Kiểu | Mặc định | Ý nghĩa |
|---|---|---|---|
| `keyword` | string | `''` | như cũ |
| `exclude_id` | int | — | như cũ |
| `limit` | int | SEARCH_LIMIT | như cũ |
| **`exclude_locked`** | bool (`1`/`true`/`on`/`yes`; đọc bằng `$request->boolean`) | tắt | Bật ⇒ bỏ hàng có dòng `product_company_coefficients` của **công ty đang làm việc** (`auth()->user()->current_company_role`) với `status = 4` (`ProductCompany::STATUS_STOPPED`). Hàng khoá ở công ty khác, hàng không có dòng ở công ty mình ⇒ vẫn ra. |

- Response giữ nguyên khuôn (`id, code, name, base_unit_id, base_unit_name, units[]`).
- FE CHỈ truyền `exclude_locked: 1` ở 2 chỗ chọn hàng kèm theo: `ProductItemPickerModal.vue:103`,
  `ProductFormItemsTable.vue:125`. Ô lọc "Máy" `picker/ProductPickerAdvancedFilters.vue:201` KHÔNG truyền.
- Hàng đã gắn trước rồi mới bị khoá vẫn hiện trong bảng (chỉ lọc nguồn chọn mới); BE vẫn chặn lúc lưu
  (`ProductRequest::checkKitStatus`) nếu chọn mới hàng khoá bằng đường khác.

## Lỗi mới (không vá)

- **N112** — `AdminData::formValues()` (`AdminData.php:~81`, tab Quản trị form sửa hàng) vẫn đọc dòng pcc bất kể
  `status`: nhánh công ty lấy về đọc nghiêm dòng NULL-status (bảo hành/tồn tối thiểu trống) trong khi nay màn chi
  tiết / danh sách / Excel lùi cột chung ⇒ form và màn xem có thể lệch cho 298 dòng NULL-status. Brief N91 chỉ chốt
  `source` + `mediaAndGuarantee`, nên để ngoài; cần user chốt form có theo luật mới không (đụng Q-A3 2-C2 "không lùi
  cột chung kẻo Lưu là chép bảo hành chung sang dòng").
- **N113** — Bộ lọc "Đời xe" của picker (`ProductPickerService.php:~470`, EXISTS theo `life_id`): với index ghép
  `(product_id, life_id)` optimizer chọn quét toàn bộ index phủ (LooseScan, 48.817 mục) chứ không `ref` — nhanh hơn
  quét bảng nhưng chưa tối ưu. Nếu bộ lọc đời xe chậm trên prod, thêm index `(life_id, product_id)`. Không đo thời gian
  thực ở đợt này.

## Ghi chú

- Dữ liệu thử: toàn bộ fixture trong `DatabaseTransactions` (rollback), không có role/dữ liệu tạm còn lại trên
  `hrm_erp_giacty`. Thay đổi DB duy nhất còn lại: index N84 (batch 438; gỡ bằng
  `migrate:rollback --path=<file>` nếu cần).
- Worktree trả về đúng nhánh `feat/chuyen-doi-hang-hoa`; server 8031 chạy từ worktree này nên đã nạp code mới (BE
  PHP, không cần restart). `git status` sạch trừ `.env.bak-hrm_erp`.
