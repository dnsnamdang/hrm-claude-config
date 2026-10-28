# Report T1 + T2 — A3 (2-E) BE hrm-api — 14/10/2026

**Trạng thái: DONE_WITH_CONCERNS** (lo ngại nhỏ ở mục 7, không chặn T3).

Repo `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/cdhh-2e-excel` (chưa push, chưa merge).

## 1. Commit

| Commit | Nội dung |
|---|---|
| `b0283c3a8` | T1 — quyền 1654: `ProductExportPermissionSeeder` (mới) + dòng giữ chỗ trong `PermissionsTableSeeder` + `ProductExportPermissionSeederTest` (3 ca) + `ActsAsProductUser` biết id 1654 |
| `90044a08a` | T2 — `export-rows` 5 màn: route, `ProductExportController`, `ProductExportService`, registry `products_*`, `ProductExportApiTest` (9 ca) |
| `9a7130e05` | Bước 14' — `ProductCodeRetryTest` (2 ca) ép va chạm `products_code_unique` |

Ngoài repo: runbook `gia-theo-cong-ty/runbook-trien-khai.md` mục 6 bước 1 — thêm lệnh chạy `ProductExportPermissionSeeder`.

## 2. T1 — quyền 1654

- `Modules/MasterData/Database/Seeders/ProductExportPermissionSeeder.php`, khuôn G6: chèn `1654 "Xuất excel danh sách hàng hoá"`
  (guard api, group `Hàng hoá`, **type 9** như 1652/1653/1655). Không truncate, không gán role. Kiểm theo id VÀ theo tên:
  id bị quyền khác chiếm, hoặc tên đã nằm ở id khác ⇒ ném lỗi, không ghi gì.
- `PermissionsTableSeeder`: thêm dòng 1654 nằm giữa 1653 và 1655; sửa comment thành "1656 seed ở Phase 2d, 1654 ở đợt 2-E (…)". Toàn
  file LF, diff `2 +/1 -`. Đã kiểm `uniq -d`: 1654 không bị trùng. Các id trùng mà lệnh này in ra đều có sẵn từ trước, không do đợt này.
- **Đã chạy vào `hrm_erp_giacty`** (đúng 1 seeder này, 2 lượt): lượt 1 `chèn 1 dòng (1654)`, lượt 2 `chèn 0 dòng (đã có 1654)`.
  Sau đó: tên này có đúng 1 dòng, `role_has_permissions` của 1654 = 0.
- Cấp quyền: chưa role nào có 1654 ⇒ khi làm T3/T4, cần tạo role tạm rồi gỡ (memory "local dev được cấp quyền để test").

## 3. T2 — endpoint

`GET /api/v1/master-data/products/{screen}/export-rows`, `screen` ∈ `warehouse | company | entering | trading | temp`
(mỗi màn một route trong vòng lặp, có `->defaults('screen', …)`; khai TRƯỚC `/{product}`).

| Màn | Gate (middleware, giống route danh sách) | + 1654 |
|---|---|---|
| warehouse · trading · temp | — | `checkPermission:Xuất excel danh sách hàng hoá` |
| company | `checkPermission:Xây dựng thông tin hàng hoá\|Xem dữ liệu hàng hoá công ty` | như trên |
| entering | `checkPermission:Xây dựng thông tin hàng hoá` | như trên |

Controller xét thêm 1654 bằng `PermissionService::isCurrentEmployeeHasPermission`, theo **công ty đang làm việc**
(`role_has_permissions.company_id`). Có 1654 ở công ty khác vẫn bị 403. Fail-closed, Super admin không có ngoại lệ.

**Tham số:** toàn bộ bộ lọc của màn (lấy lại nguyên `ProductService::index($request, $screen)`, nên cùng phạm vi, cùng bộ lọc,
cùng thứ tự `sort_by/sort_desc`), cộng thêm:
- `page` (≥ 1, mặc định 1);
- `limit` (mặc định 2000, trần **5000**; giá trị 0 hoặc âm thì về mặc định / 1);
- `fields`: nhận mảng `fields[]=a&fields[]=b` hoặc chuỗi `fields=a,b` (cách `exportListFile` FE đang gửi). Giữ đúng thứ tự tick, bỏ
  key lạ. Không truyền, hoặc toàn key lạ ⇒ trả mọi cột của màn.

**Trả về:** `{code, message, data: {headings, widths, rows, total, page, limit}}`
- `headings`, `widths` đều có cột `STT` ở đầu (rộng 6). Mỗi dòng trong `rows` là một mảng; phần tử 0 là STT do BE đánh theo trang.
- Kiểu dữ liệu: `vat_percent` và `min_stock_qty` trả `float`, ô trống trả `null`. Mọi cột khác trả chuỗi, ô trống là `""`
  (mã và barcode luôn là chuỗi). Ô nhiều giá trị nối bằng `"\n"`.

**JSON mẫu một dòng** (`fields` mặc định, Cty 1 trên giacty; dạng `{nhãn: giá trị}` cho dễ đọc, API thật trả mảng):

- `warehouse`:
  `{"STT":1,"Mã hàng":"TORI-TRW05001:01","Tên hàng hoá":"Giá treo tháo lắp động cơ 0.5 tấn - Chuyên dùng cho đào tạo","Model":"TRW05001","Tính chất hàng hoá":"","Nhóm chức năng":"","Nhóm sản phẩm":"","Loại sản phẩm":"","Thương hiệu":"TORIN","Hãng sản xuất":"TORIN (Changshu …)","Barcode":"","ĐVT":"Cái","Xuất xứ":"China","Code đặt hàng":"","Tên tiếng Anh":"Engine support 0.5 ton","% VAT":8,"Bảo hành":"12 tháng","SL tồn kho tối thiểu":0,"Công ty quản lý":"CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT","Công ty đang kinh doanh":"CÔNG TY CỔ PHẦN …\nCN HẢI PHÒNG - …\n… CHI NHÁNH VINH\nCÔNG TY TNHH THIẾT BỊ TÂN PHÁT SÀI GÒN","Người nhập thông tin":"Đỗ Đăng Hiếu","Ngày cập nhật":"15/09/2026","Trạng thái":"Đang kinh doanh"}`
  (hàng công ty chưa dùng thì `Trạng thái` = `"Chưa sử dụng"`, giống chữ đang hiện trên màn)
- `company` / `trading`: như trên, nhưng bỏ `Công ty đang kinh doanh`, thêm `"Catalog kinh doanh":"<Tiểu mục 1>\n<Tiểu mục 2>"`
  ngay sau `Hãng sản xuất` (giacty chưa xếp catalog ⇒ `""`).
- `entering`: cùng bộ cột với `company`. `Trạng thái` ∈ Đang nhập thông tin / Chờ tính giá bán / Đang tính giá. Giacty có 0 dòng
  nên mẫu lấy từ PHPUnit.
- `temp`: `{"STT":1,"Mã hàng":"…",…,"Catalog kinh doanh":"",…,"SL tồn kho tối thiểu":2.5,"YCHG đang chứa":"YCHG-xx (Chờ PTKD)\n…","Trạng thái":"Hàng tạm","Lý do không duyệt":"","Người tạo":"…","Ngày tạo":"14/10/2026"}`.
  Giacty có 0 dòng, mẫu lấy từ PHPUnit. `YCHG đang chứa` mỗi phiếu một dòng, dạng `MÃ (Trạng thái)`. `Lý do không duyệt` chỉ có
  giá trị khi trạng thái là 8.

## 4. Key cột theo màn (FE T3 dùng — `ExportColumnRegistry::COLUMNS['products_<slug>']`)

Thứ tự = thứ tự cột trên bảng. Bỏ `avatar` (không xuất ảnh). Thêm `code` ở đầu (cột ghim trái trên màn). **Không có cột giá.**

| Key | Nhãn | warehouse | company | entering | trading | temp |
|---|---|:-:|:-:|:-:|:-:|:-:|
| `code` | Mã hàng | ✓ | ✓ | ✓ | ✓ | ✓ |
| `name` | Tên hàng hoá | ✓ | ✓ | ✓ | ✓ | ✓ |
| `model_name` · `product_nature_name` · `product_function_group_name` · `product_family_name` · `product_type_name` · `brand_name` · `manufacturer_name` | (như tên cột màn) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `catalogs_text` | Catalog kinh doanh | — | ✓ | ✓ | ✓ | ✓ |
| `barcode` · `unit_name` · `origin_name` · `order_code_name` · `english_name` · `vat_percent` · `guarantee_text` · `min_stock_qty` | (như màn) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `owner_company_name` | Công ty quản lý | ✓ | ✓ | ✓ | ✓ | — |
| `trading_company_names` | Công ty đang kinh doanh | ✓ | — | — | — | — |
| `creator_name` | Người nhập thông tin (temp: **Người tạo**) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `updated_at` | Ngày cập nhật | ✓ | ✓ | ✓ | ✓ | — |
| `status_text` | Trạng thái | ✓ | ✓ | ✓ | ✓ | ✓ |
| `open_requests_text` | YCHG đang chứa | — | — | — | — | ✓ |
| `temp_reject_reason` | Lý do không duyệt | — | — | — | — | ✓ |
| `created_at` | Ngày tạo | — | — | — | — | ✓ |

Thứ tự ở màn temp: …`min_stock_qty`, `open_requests_text`, `status_text`, `temp_reject_reason`, `creator_name`, `created_at`.

Ánh xạ từ khoá cột trên bảng sang khoá cột file: `exportFieldsMixin.visibleExportFields` tự thử thêm hậu tố `_text`, nên
`catalogs` → `catalogs_text`, `open_requests` → `open_requests_text`, `company_status` → `status_text` (nhánh `*_status`).
Không bắt buộc khai `exportFieldKeyMap`; FE có khai cho chắc cũng không sao.

## 5. Hiệu năng (đo trực tiếp service bằng tinker trên `hrm_erp_giacty`, Cty 1, limit 5000, cả 6 trang)

| Màn | Tổng dòng | Thời gian / trang 5.000 dòng | Query / trang | Payload |
|---|---|---|---|---|
| warehouse | 28.378 | 461–544 ms | 8 (9 ở trang 1) | ~3,9 MB |
| company | 28.371 | 459–551 ms | 9 (10 ở trang 1) | ~2,1 MB |
| trading | 28.371 | 421–522 ms | 9 (10 ở trang 1) | ~2,1 MB |

Không có N+1: số query cố định, không phụ thuộc số dòng. Cách làm là `index()->setEagerLoads([])->toBase()`, rồi nạp danh mục,
cây phân loại, catalog và dòng hàng × công ty bằng query gộp theo id của cả trang. Số đo trên chưa gồm lớp HTTP, JWT và middleware.
Trang sâu (offset 25k) không chậm thêm. Nếu FE dùng mức 2.000 dòng/lượt (`EXPORT_PAGE_LIMIT`), mỗi lượt khoảng 0,2 s.

## 6. Test

- File mới: `ProductExportPermissionSeederTest` 3/3, `ProductExportApiTest` 9/9 (346 assertion), `ProductCodeRetryTest` 2/2.
- **Cả bộ `Modules/MasterData`: OK 546/546 (5.056 assertion), 3 phút 14 giây.** Mốc cũ là 532; 14 ca mới = 3 + 9 + 2.
- `ProductExportApiTest` gồm các ca:
  - đúng cột theo `fields` (cả dạng mảng lẫn dạng chuỗi), đúng thứ tự, key lạ bị bỏ, toàn key lạ thì trả đủ cột;
  - catalog 2 nhánh ra 2 dòng trong ô ở trading/company, nhánh của công ty khác không lọt ra (fixture tự dựng);
  - Kho không có cột catalog (`catalogs_text` bị coi là key lạ);
  - 403 khi thiếu 1654 ở cả 5 màn, kể cả khi 1654 chỉ có ở công ty khác;
  - 403 khi thiếu quyền màn (company/entering) dù có 1654;
  - phân trang: STT theo trang, trang rỗng, trần 5000, mặc định 2000;
  - không có trường giá: registry không có key hay nhãn nào chứa giá, JSON không chứa `cost_price`/`buy_price`/`"price"`;
  - giá trị từng ô khớp với API danh sách (`ProductListResource`) ở 19 cột chữ, `min_stock_qty` trả float, mã trả chuỗi;
  - temp ra chữ trạng thái "Hàng tạm"; Kho ghi "Chưa sử dụng".
- **Bước 14'** (`ProductCodeRetryTest`) tái hiện cuộc đua theo đúng thứ tự: request A sinh mã khi mã còn trống → request B chiếm mã
  đó → A `save()` đụng UNIQUE 23000 → A sinh lại `<mã>:01` và lưu được. Kiểm thêm: chỉ 1 hàng mới, pcc/ĐVT/catalog mỗi thứ đúng
  1 dòng, mã rỗng = 0, mã trùng = 0. Ca thứ hai: mã bị chiếm ở mọi lượt ⇒ thử đúng `CODE_RETRY` = 3 lần, ném `QueryException`, không
  để lại hàng dở dang.
  - Ghi chú kỹ thuật: hai cách "chèn bản ghi chiếm mã ngay trong callback" đều KHÔNG tái hiện được cuộc đua. Chèn trong savepoint
    của A thì rollback savepoint xoá luôn hàng chiếm mã. Chèn bằng kết nối thứ hai thì read view của transaction test không thấy
    hàng đó, nên generator ra lại đúng mã cũ (đã thử, cả 2 ca đều fail). Vì vậy dùng generator gián điệp: lượt đầu trả mã "cũ" mà A
    đang cầm, các lượt sau gọi generator thật.

## 7. Lo ngại / việc ngoài luồng (không vá)

1. **Cột Catalog ở màn Nhập thông tin và Hàng tạm.** Brief và chốt Q3 ghi "4 màn trừ Kho có cột Catalog", nên registry
   `products_entering` và `products_temp` có `catalogs_text`. Nhưng hai màn này trên FE (`product-list-screens.js`) **không có cột
   `catalogs`**, nên popup sẽ có ô "Catalog kinh doanh" mà không tick sẵn, lệch nhẹ với Q4 "theo cột màn". Nếu user muốn đúng tuyệt
   đối theo cột màn thì bỏ 2 dòng trong registry (test `catalog_nhieu_nhanh…` đang assert 2 dòng này, cũng phải sửa theo).
2. `php artisan route:list` lỗi sẵn từ trước (`PermissionHelper.php:26` gọi `employee_info_id` khi chưa đăng nhập, do một
   controller khởi tạo). Không phải lỗi của đợt này; route mới đã được kiểm qua PHPUnit.
3. Giacty có 0 dòng pcc ở trạng thái 1/2/5/6/7/8, nên màn entering và temp trên dev ra file rỗng. Hai màn này chỉ được kiểm bằng
   fixture PHPUnit. T4 cần tự dựng dữ liệu.
4. Middleware `checkPermission` (gate quyền màn 1652/1653) đọc quyền ở **mọi** công ty, giống route danh sách đang chạy. Đợt này giữ
   nguyên để khớp gate màn hiện tại; riêng 1654 đã xét chặt theo công ty ở controller.
5. Chưa đo qua HTTP thật (cổng 8031), vì chưa role nào có 1654 và brief không cho ghi role vào DB ngoài seeder. Số đo ở mục 5 là đo
   service; T4 đo lại trên trình duyệt.
