# Soát bảng C — việc ngoài luồng (13/10/2026, chỉ đọc)

> Đối chiếu: HRM `feat/chuyen-doi-hang-hoa` @657fa731f (api) / @dc793189e (client), ERP `feat/2d1-erp-khong-loi` @f941467a49.
> Số liệu: SELECT trên `hrm_erp_giacty`. Không sửa source, không ghi DB.
> Nguồn checklist: `../viec-con-lai.md` bảng C. User 13/10: A7 (phase 2c/3/4/5) để SAU, làm bảng C trước.

## 1. Kết quả từng mục

### Nhóm hàng hoá

| Mục | Hiện trạng | Repo / file chính | Cỡ | Cần chốt |
|---|---|---|---|---|
| N1 | CÒN — ERP đọc `products.min_stock_qty/guarantee/guarantee_type` (cột chung), HRM ghi theo công ty ở `pcc` ⇒ chứng từ ERP hàng HRM bảo hành 0, báo cáo tồn tối thiểu bỏ sót. ~19+23 file min_stock, ~109+128 file guarantee | ERP `app/Product.php:7756,8229`, `WarehouseWarningReportController.php:309`, `Quotation.php:1077` | L | Q-N1 |
| N12 | CÒN = A8 — spec chèn `roles.company_id` (cột đã gỡ) ⇒ 5 ca đỏ | `HRM/e2e/tests/master-data/products-*.spec.ts`, `utils/productFixture.ts:19` | S | — |
| N13 | CÒN — hàng 7338 (7.582 đời xe) mở tab Xe ~4,5s, lưu ~3,3s, ~7,7k query | api `ProductRequest.php:129-131` (exists từng phần tử), `ProductWriteService.php:552-559` (insert từng dòng); client `ProductFormVehicles.vue:71,294` (find O(n²)) | M | — |
| N14 | CÒN (a) URL không kiểm định dạng (b) hàng kèm theo `exists` không lọc status (c) S3 mồ côi khi rollback `promoteTemporary`; (d) composer.lock chỉ khác hình thức | api `ProductRequest.php:79-84,99-111`, `ProductWriteService.php:471` | S | Q-N14 |
| N26 | Local hết rủi ro trùng id (AI `product_versions` 176.616 > max mồ côi 175.610); còn 59.710 dòng mồ côi; prod chưa biết | không sửa code — checklist gộp DB prod (chỉnh AUTO_INCREMENT) | S | Q-N26 |
| N27 | CÒN — `take` / `writeUpdate` / `updateAdmin` kiểm khoá ngoài transaction, không `lockForUpdate` | api `ProductWriteService.php:130-143,181-190,258-297` | S | — |
| N31 | ✅ HẾT tác động — 2 route trùng tên đều đã gắn `productMovedToHrm` | (tuỳ chọn đổi tên ERP `web.php:659`) | S | — |
| N32 | CÒN — sửa thuế suất ở HRM không lan xuống `products`/`product_templates`/`groups`; ERP có lan (job chunk); route ERP tax-rates chưa chặn | api `TaxRateService.php`; ERP `web.php:357-364` | S-M | Q-N32 |
| N33 | Gần hết (N6 CRM đã bỏ; 16k hàng vốn NULL template); màn hàng gốc ERP index/show còn mở, hiện dữ liệu lỗi thời | ERP `web.php:502,506,507` | S | Q-N33 |

### Nhóm lỗi cũ ERP (đều CÒN — middleware không phủ in tem/báo cáo/báo giá/chi tiết)

| Mục | Hiện trạng / nguyên nhân | File | Cỡ | Cần chốt |
|---|---|---|---|---|
| N39 | ERP CLAUDE.md ghi Laravel 8, thực tế `^6.2` | `ERP/CLAUDE.md:19` | S | — |
| N41 | Nút in mẫu 1 in cả hàng mẫu 2; đang bị N46 che | `ProductsController.php:691-694` | S | Q-N41 |
| N42 | `product-infos` còn nút Thêm mới + Sửa/Xoá dòng (bấm ra trang "đã chuyển HRM") | `product_infos/list.blade.php:39`, `ProductInfoController.php:219-220` | S | — |
| N43 | Code chết (`App\Model\ProductInfo\Product` không tồn tại, không ai gọi) | `Model/ProductInfo/BaseProduct.php:76` | S | — |
| N44 | `Product::exportExcel` chết; lỗi thật: `product_export.blade.php:60` `$baseUnit->name`, route `exportCSV/exportPDF` (`web.php:580-581`) | ERP | S | — |
| N45 | `ExampleTest` `get('/')` gặp `sso.check` ⇒ 302 | `tests/Feature/ExampleTest.php` | S | — |
| N46 | Màn in tem phiếu nhập trống: thiếu include `WarehouseImportArrangeDelivery` | `warehouse_imports/barcode.blade.php:169-171` | S | — |
| N47 | Excel Doanh thu theo hàng hoá 500: `forCategory()` không có + compact `$category` | `RevenueByProductController.php:41`, `ExcelExports/RevenueByProduct.php:41` | S | Q-N47 |
| N48 | PDF cùng báo cáo 500: compact `$category` | `RevenueByProductController.php:54` | S | Q-N47 |
| N49 | Báo giá dịch vụ `reading 'cost'` — giả thuyết mạnh: `triggerSelect2` kích `handleSelectPayload` với tham số rỗng, response lỗi không có `data` | `partials/modals/js/calculateDeliveryCost.blade.php:82` | S | — |
| N50 | Báo giá mẫu `infdig` — giả thuyết: getter `products` trả mảng mới + `ui-sortable ng-model` | `partials/classes/sale/QuotationTemplate.blade.php:46-48` | S-M | — |
| N51 | Chi tiết hàng: `function` trong biểu thức Angular 1.3.9 ⇒ ô NCC trống | `products/formShow.blade.php:936` | S | — |

### Nhóm giá

| Mục | Hiện trạng | Repo / file | Cỡ | Cần chốt |
|---|---|---|---|---|
| N61 🔴 | CÒN + rộng hơn: `getData` / `product-info getData` / `getDataForJoin` / `getRecipe` không gate, trả 13 cột `pcu` (giá vốn, giá mua, giá chờ duyệt…) + `lastest_export_price`; **thêm lỗ**: `?company_id=X` đọc giá công ty khác (`DocumentCompany::resolve` tin request). ERP không có quyền "xem giá vốn hàng hoá" | ERP `Product.php:1268-1377`, `ProductPriceService.php:28-58`, `ProductsController.php:3172-3180`, `DocumentCompany.php:79-83`, `web.php:599,606,607,644` | M | Q-N61 |
| N54 | Gần hết (G3 bỏ nhân hệ số); còn R4 `getPriceOfProducts` làm tròn nghìn (lệch cố ý design §3.6) | ERP `ProductsController.php:3609-3617` | S | Q-N54 |
| N58 | CÒN — cron 01:00 reset 3 cờ chờ duyệt, không xoá `pa`/`pap` | ERP `UpdateProductPrice.php:74-82` | S | Q-N58 |
| N59 | CÒN — sort cột tự do (500 khi cột sai); nhánh `type=updating` không gate | ERP `ProductsController.php:2530-2548`, `web.php:595` | S | — |
| N60 | CÒN — truyền `unit_coefficient` (null) thay `unit_id` ⇒ giá ĐVT cơ bản | ERP `ProductExportsController.php:767` | S | Q-N60 |
| N62 | CÒN một phần — `units[0]` (ĐVT cơ bản), `prices[0]` null ⇒ 500, công ty theo người dùng | ERP `WrServiceQuotation.php:1018,1081,1097,1224,1325,1351` | S | — |
| N63 | CÒN — Job Reset (không ai gọi, reset giá MỌI công ty); Job CRM còn được 2 seeder gọi tay, không lọc công ty | ERP `app/Jobs/*` | S | Q-N63 |
| N64 | ✅ HẾT phần hàng hoá/giá (log giá ở `GATED_TABLES`, endpoint riêng gate 1657). Còn ngoài feature: route chung đọc ~90 bảng gồm phiếu thu/chi, UNC, TK ngân hàng, công nợ — không gate, không lọc công ty | HRM `routes/api.php:36-48`, `CatalogHistoryService.php` | M | Q-N64 |
| N65 | CÒN, tăng dần — `pep` status 2 quá ngày 13.915 (09/10: 13.662); cờ mồ côi pcu 6 · upp 5 · product_units 6 | dữ liệu + ERP `UpdateProductPrice.php:52-60` | S | Q-N65 |
| N66 | ✅ gần hết — G3 `DocumentCompany::NO_COMPANY_TABLES` suy công ty từ người lập | — | — | — |
| N67 | CÒN — ERP `postRegulations` vẫn ghi 6 cột cờ duyệt giá công ty, route không chặn/không quyền | ERP `CompaniesController.php:436-442`, `common/companies/regulation.blade.php:478-553` | S | Q-N76 (mới) | 8 danh mục Phase 1 còn lại (Model, Code đặt hàng, ĐVT, Thuộc tính, ĐV thuộc tính, Xuất xứ, File đính kèm, Mã màu) + bản `pi-*` vẫn ghi được ở ERP (Phase 1 QĐ8 "2 bên cùng sửa") | ✅ 13/10: **chặn hết ở ERP** (thêm/sửa/xoá/import) + menu sang HRM; giữ route đọc + "thêm nhanh" chứng từ cần (khảo sát riêng); `pi-*` khảo sát rồi báo trước khi chặn |
| Q-N67 |
| N68 | CÒN một phần — `PriceNotFoundForCompany` rơi về 404, ~107 chỗ gọi không bắt | ERP `Exceptions/Handler.php:52-54` | S-M | — |
| N73 | CÒN — seeder test join `upp` không kẹp công ty | api `Finance/Database/Seeders/BorrowExportRequestTestDataSeeder.php:182-186,215-217` | S | — |
| N74 | 4 helper giá ✅ hết; còn `getBaseUnitIds` đọc `mysql2` (`TpProductUnitPrice.php:65-87`) + 4 chỗ đọc `mysql2.products` | HRM | S | Q-N74 |
| N75 | CÒN nhẹ — `e2e_provision.php:60` đọc `mysql2`; mã 3920 status 0 không pcc | api `database/e2e_provision.php` | S | — |

**Đếm:** 38 mục ⬜ ⇒ đóng được 3 (N31, N66, N64 phần feature) · gần hết 2 (N26 còn bước runbook, N33 tuỳ chốt) · còn 33.

## 2. Câu cần user chốt (hỏi lần lượt)

| # | Câu | Đáp án |
|---|---|---|
| Q-N61 | getData: bỏ hẳn giá vốn khỏi JSON hay gate bằng quyền ERP mới; `company_id` từ request: ai được đọc giá công ty khác | ✅ 13/10: **bỏ hẳn** 13 cột pcu + `lastest_export_price` + `'product' => $this` khỏi 3 API `products/*` (giữ giá bán); chặn `product-infos/{id}/getData` như màn product2; `company_id` **chỉ nhận công ty user được thao tác**, ngoài ra 403 |
| Q-N1 | Báo cáo tồn tối thiểu toàn hệ thống (không có công ty chứng từ) lấy số công ty nào | ✅ 13/10: báo cáo Cảnh báo đặt hàng tồn kho chế độ **tổng công ty ⇒ CỘNG** tồn tối thiểu các công ty; chế độ 1 công ty ⇒ số của công ty đó. Chứng từ ⇒ theo công ty chứng từ |
| Q-N32 | Thuế suất: HRM chủ duy nhất (chặn ERP) hay cả 2 cùng sửa | ✅ 13/10: **HRM duy nhất** — ERP chặn thêm/sửa/xoá (`productMovedToHrm`) + menu sang HRM; HRM thêm bước lan xuống products/product_templates/groups như ERP |
| Q-N67 | Cấu hình duyệt giá công ty: HRM chủ duy nhất (ERP bỏ ghi 6 cột) | ✅ 13/10: **HRM duy nhất** — ERP bỏ 6 cờ khỏi `postRegulations` + ẩn thẻ, link sang HRM |
| Q-N14 | Hàng đang khoá (status 4) có được chọn làm hàng kèm theo | ✅ 13/10: BE chặn hàng đã xoá mọi trường hợp; hàng khoá **không thêm mới** nhưng dòng đã gắn trước **giữ + lưu lại được** (công thức / phụ kiện / VT lắp đặt / VT sửa chữa) |
| Q-N26 | Dọn 59.710 dòng `product_histories` mồ côi hay giữ (chỉ chỉnh AUTO_INCREMENT prod) | ✅ 13/10: **giữ nguyên**; chỉ thêm bước kiểm/chỉnh AUTO_INCREMENT `product_versions` vào runbook gộp DB prod |
| Q-N33 | Ẩn màn hàng gốc ERP (index/show) | ✅ 13/10: **ẩn hẳn** — chặn index/show/history `product_templates` bằng `productMovedToHrm` + gỡ menu; giữ bảng |
| Q-N41 | Nút in tem mẫu 1 loại bỏ hàng mẫu 2 | ✅ 13/10: **lọc bỏ** hàng mẫu 2 ở mục "Mẫu 1" (`!= 2`); làm cùng N46 |
| Q-N47 | Báo cáo Doanh thu theo hàng hoá: sửa cho xuất được hay bỏ | ❌ 13/10 user: **bỏ qua** N47 + N48 (không sửa) |
| Q-N54 | Bỏ luật làm tròn nghìn R4 hay chấp nhận lệch | ✅ 13/10: **bỏ làm tròn** ở `getPriceOfProducts` (chỉ chứng từ mới đổi) |
| Q-N58 | Cron áp giá hiệu lực khi đang có yêu cầu duyệt: giữ cờ hay huỷ yêu cầu | ✅ 13/10: **giữ yêu cầu** — cron vẫn áp giá, nhưng dòng có yêu cầu chờ duyệt thì không đụng `*_wait_approve` + 3 cờ; người duyệt thấy K9 |
| Q-N60 | Sửa giá phiếu ghép/tách: có sửa lại phiếu cũ | ✅ 13/10: sửa code, **chỉ áp phiếu mới**; phiếu cũ giữ nguyên — đếm số phiếu cũ bị ảnh hưởng để báo |
| Q-N63 | Đồng bộ CRM còn dùng không, nhận giá công ty nào | ✅ 13/10: **xoá cả 2 job** — Job CRM (+ lời gọi trong 2 seeder chạy tay `SyncDataToCrmSeeder:147`, `UpdateMissingDataToCRM:136`) và Job Reset (Command 14:30 đã thay, đã theo công ty) |
| Q-N64 | Gate route lịch sử chung cho chứng từ tài chính trong lần prod này | ✅ 13/10: **đóng cho feature**, ghi việc riêng vào STATUS gop-db (mục Lưu ý) — làm sau, ngoài phạm vi |
| Q-N65 | Giá quá ngày chưa áp: bỏ hay áp bù; cờ mồ côi: xoá hay tạo lại yêu cầu duyệt | ✅ 13/10: lệnh dọn idempotent (`--dry-run`, sao lưu trước) **đóng hết 13.915 dòng quá ngày, không áp**; xuất danh sách 2.067 dòng năm 2026 cho nghiệp vụ soát; cron 01:00 đổi sang áp `effect_date <= hôm nay`; **xoá 17 cờ mồ côi** (pcu 6 · upp 5 · product_units 6). Chạy prod = bước runbook |
| Q-N74 | Prod `DB_DATABASE_SECOND` có trỏ DB gộp không | ✅ 13/10: **bỏ `mysql2` cả 5 chỗ** (`getBaseUnitIds` + 4 chỗ đọc `mysql2.products` ở Báo giá); bảo hành đọc theo công ty (cùng N1) |

## 3. Đề xuất chia đợt (cập nhật sau khi chốt đủ 16 câu, 13/10)

| Đợt | Mục | Repo | Ghi chú |
|---|---|---|---|
| **C-a Bảo mật + giá ERP** | N61 🔴, N59, N62, N68, N60, N63, N67, N54, N58 | ERP | ưu tiên 1 (lộ giá vốn) |
| **C-b Chặn ghi danh mục ở ERP** | N76 (8 danh mục + `pi-*`), N32 (thuế suất: ERP chặn + HRM lan), N33 (ẩn hàng gốc), N42 (nút ghi `product-infos`) | ERP + HRM (N32 lan) | cần khảo sát nhỏ: "thêm nhanh" trong chứng từ, `pi-*` |
| **C-c Lỗi cũ ERP** | N39, N41 + N46, N43, N44, N45, N49, N50, N51 | ERP (+ ERP/CLAUDE.md) | N47/N48 ❌ bỏ qua |
| **C-d HRM hàng hoá** | N13, N14, N27, N73, N74, N75 + A8/N12 (spec e2e) | HRM | |
| **C-e N1 bảo hành / tồn tối thiểu theo công ty** | N1 | ERP (lớn, ~100 file) | báo cáo tổng công ty = CỘNG |
| **C-f Dữ liệu / runbook** | N65 (lệnh dọn + cron `<=`), N26 (bước AUTO_INCREMENT) | ERP + runbook | chạy prod = bước runbook |

Đóng / bỏ: N31 · N66 · N64 (phần feature; phần tài chính ghi STATUS gop-db) · N47 · N48.
