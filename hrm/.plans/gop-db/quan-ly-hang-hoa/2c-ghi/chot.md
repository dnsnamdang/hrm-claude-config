# Đợt 2-C — Ghi: bảng chốt

> Nguồn câu hỏi: `yeu-cau-ghi.md` (T1–T11) · `erp-ghi-hang-hoa.md` (khảo sát ERP ghi hàng hoá).

| # | Chốt (04/10/2026) |
|---|---|
| T6 | **Hệ số công nghệ (`products.tech_coefficient`) DÙNG CHUNG các công ty** — là thông tin chung của mã hàng, không tách theo công ty, không thêm cột vào `product_company_coefficients`. (Đang hiện ở tab *Quản trị hàng hoá* — quyền sửa theo luật thông tin chung: chỉ công ty tạo.) |
| H1' | **Chưa có luồng Tính giá ⇒ CHƯA có đường chuyển *Đang nhập thông tin → Chờ tính giá*: hàng TREO ở *Đang nhập thông tin*, chờ phase Tính giá.** Bấm Lưu KHÔNG đổi trạng thái (khác mockup `luuVaChuyen` và §26a). Hệ quả: nút tạm "Chuyển kinh doanh" (H1, 2 → 3) không có hàng nào để dùng ⇒ KHÔNG làm ở 2-C |
| H1'' | User xác nhận: **bỏ nút tạm "Chuyển kinh doanh" (H1)**. Hàng HRM tạo mới nằm ở *Đang nhập thông tin* tới phase Tính giá; bật HRM thật chỉ khi đã có Tính giá (hoặc ERP vẫn tạo hàng song song tới lúc đó) |

## Câu còn mở (gộp từ `yeu-cau-ghi.md` T1–T11 + `erp-ghi-hang-hoa.md` R1–R12), xếp theo mức ảnh hưởng

| # | Câu | Vì sao |
|---|---|---|
| G1 | `products.status` của hàng HRM tạo mới (T2/R7/R8) | popup 338 màn ERP lọc `status != 0` ⇒ status 1/2 là hàng *Đang nhập thông tin* chọn được ngay trong chứng từ ERP |
| G2 | Đơn vị cơ bản + 6 dòng giá (bất biến ERP, R-4) | thiếu ⇒ hàng biến mất khỏi danh sách ERP + popup 404 (`firstOrFail` ~290 chỗ) |
| G3 | Lưu nháp (T1) | DB buộc code/name/brand/manufacture/origin/created_by; với H1' Lưu không đổi trạng thái ⇒ Lưu nháp thừa? |
| G4 | Sửa tab Quản trị của hàng CŨ (T3) | phải sinh dòng hàng × công ty `coefficient=1` ⇒ giá popup ERP của mã đó làm tròn nghìn |
| G5 | Ghi kép `min_stock_qty`/`guarantee` sang cột chung (T4) | ERP đọc cột chung ở 29/42 file, chép bảo hành sang chứng từ |
| G6 | Khoá/Mở khoá (T5/R1) | ERP không phân biệt khoá với xoá (`status=0`) |
| G7 | Xoá (T8) | chứng từ tính gì, mềm/cứng, gỡ dòng có hệ số cũ |
| G8 | Sao chép (T9) | sao những gì |
| G9 | Lối vào sửa (T10) + câu nhỏ (T11) | |
| G10 | Phạm vi 2-D (R2/R3/R10) | màn Hãng SX/Thương hiệu ERP ghi đè dữ liệu; route trắng; cron giá — để lúc plan 2-D |
| G1 | **`products.status = 1`** cho hàng HRM tạo mới (giống ERP hiện nay) — chấp nhận hàng *Đang nhập thông tin* chọn được ngay trong popup 338 màn ERP. Trạng thái quy trình vẫn ở dòng hàng × công ty (status 1) nên HRM không bị luật suy ra đè |
| G2 | **Ghi đủ 6 dòng `product_unit_prices` giá 0, hệ số 0** cho mỗi đơn vị (kể cả đơn vị cơ bản); `product_units.cost_price`/`buy_price` = 0 ghi tường minh (HRM chạy MySQL strict). Sửa hàng cũ: KHÔNG đụng dòng giá đã có, chỉ bù 6 dòng cho đơn vị mới thêm. Đúng 1 đơn vị cơ bản (hệ số 1) |
| G3 | **Chỉ 1 nút Lưu**, bỏ Lưu nháp. Lưu bắt buộc đủ trường bắt buộc của form, validate báo đồng thời mọi ô; không đổi trạng thái. Nút chuyển bước thêm ở phase Tính giá |
| G4 | Lưu tab Quản trị của hàng CŨ chưa có dòng ⇒ **sinh dòng hàng × công ty `coefficient = 1`, `status = 3`** (khớp trạng thái đang suy ra). Chấp nhận mã đó bị làm tròn nghìn ở popup ERP (như K2). Ghi chú: popup Xây dựng catalog chỉ ghi `product_business_catalogs`, KHÔNG cần sinh dòng ⇒ xếp catalog không làm đổi giá |
| G5 | **Không ghi kép** sang cột chung. User 04/10: *"Các vấn đề phát sinh ngoài luồng hàng hoá note lại để xử lý tại chức năng đó sau. Sẽ fix hết rồi mới merge vào nhánh prod"* ⇒ HRM chỉ ghi theo công ty; chỗ ERP đọc cột chung (29 + 42 file) ghi vào danh sách việc ngoài luồng bên dưới |

## Việc ngoài luồng hàng hoá — note lại, xử lý tại chức năng đó, PHẢI xong trước khi merge prod

| # | Việc | Nguồn |
|---|---|---|
| N1 | 29 file ERP đọc `products.min_stock_qty` + 42 file đọc `guarantee`/`guarantee_type` (chép sang 23 bảng chứng từ) ⇒ đổi sang đọc dòng theo công ty của chứng từ | §24c, G5 |
| N2 | Màn Hãng SX ERP (`ManufacturesController:185,:270`) ghi đè `company_id` + xoá sạch dòng hàng × công ty của mọi hàng thuộc hãng | 2-A K2, R2 |
| N3 | Màn Thương hiệu ERP (`Brand::updateProducts`) ghi đè `company_id` | R2 |
| N4 | Chặn route `products/*` ERP phải chừa danh sách trắng (`updateEnglishName`, `updateHSCode`, `getData` từ màn mua hàng/popup) | R3 |
| N5 | Cron đưa giá về 0 khi hết tồn lọc theo `products.company_id` + `product_cate` ⇒ bỏ sót hàng HRM tạo · **09/10: để SAU khi xong các chức năng hàng hoá** | R10 |
| N6 | Cron `sync:crm` chỉ đẩy hàng có `product_template_id` ⇒ hàng HRM tạo không sang CRM · **09/10: user BỎ, không xử lý** | erp-ghi-hang-hoa.md |
| N7 | Hàng HRM tạo `group_id` NULL ⇒ `->group->` trong SearchController (popup 338 màn) lỗi | 2-D |
| N8 | Khoá theo công ty (G6) chỉ HRM biết — popup ERP vẫn cho chọn hàng công ty đã ngừng kinh doanh | G6 |
| N9 | Hàng HRM tạo để `products.product_type` (chuỗi) NULL (không ánh xạ — `man-danh-muc-hang-hoa/design.md` §6) ⇒ `SearchController` ERP lọc `!= 'service_product'` (4 hàm) loại mất dòng NULL ⇒ hàng HRM tạo KHÔNG hiện ở popup 338 màn ERP tới khi bỏ điều kiện lọc (§6b, cần khách xác nhận hệ quả 30 hàng dịch vụ lọt vào popup) | 2-C1 khảo sát 07/10 |
| N10 | Cờ `product_natures.is_auto_parts` mặc định 0 ⇒ TRƯỚC go-live phải tick các Tính chất phụ tùng ô tô thật, không thì form tạo hàng mới không hiện tab Phân loại xe | 2-C1 review cuối 08/10 |
| N11 | **(09/10 T2: `can_retail` không dùng nữa ⇒ gỡ khỏi code ở 2-D1 P1)** Nhánh feature thiếu migration drop `product_types.can_retail` (DB local đã chạy từ gop_db) ⇒ entity ProductType còn fillable `can_retail` ⇒ POST /product-types 500 trên DB đó; xử lý khi merge gop_db | 2-C1 Pha 3 08/10 |
| N12 | Tài khoản e2e nocost có sẵn quyền 1652 (role "E2E No Cost") ⇒ chưa có tài khoản e2e "chỉ xem hàng hoá" cho ca không quyền ghi | 2-C1 Pha 3 08/10 |
| N13 | Form sửa hàng ERP cũ nhiều đời xe chậm (7338: 125 model / 7.582 đời xe — mở tab xe 4,5s dev, lưu BE 3,3s ~7,7k query validate) | 2-C1 review cuối 08/10 |
| N14 | Tồn nhỏ 2-C1: URL ảnh/video/tệp không kiểm định dạng; hàng kèm theo nhận hàng ERP đã xoá (exists không lọc status); S3 mồ côi khi rollback; composer.lock đổi định dạng (Composer mới) | 2-C1 review cuối 08/10 |
| N26 | DB local có 59.710 dòng `product_histories` mồ côi trỏ `product_version_id` vượt AUTO_INCREMENT `product_versions` ⇒ phiên bản mới có thể trùng id, xoá cứng bị FK chặn với câu "đã phát sinh chứng từ" (đúng chặn, lệch câu); `product_price_histories.product_version_id` chỉ chặn ở FK cuối | 2-C4 BE 08/10 |
| N27 | Lấy về / sửa chạy đồng thời với khoá không khoá dòng (đọc trạng thái không `lockForUpdate`) — có từ 2-C1/2-C2 | 2-C4 review 08/10 |
| N28 | `GET products/change` + 3 route `view-import*` không gate quyền mà ghi hàng loạt · 09/10: **gỡ route trong 2-D** (Q5) | 2-D khảo sát A §7 |
| N29 | 4 route duyệt giá `approve*Submit` (ERP `web.php:597-600`) không `checkPermission` | 2-D khảo sát A §7 |
| N30 | `manualUpdatePrices` là GET nhưng ghi giá (`web.php:617`) | 2-D khảo sát A §7 |
| N31 | Tên route `productDelete` khai trùng (`web.php:580, 674`) ⇒ nút Xoá màn hàng hoá ERP trỏ `/product2/{id}/delete` | 2-D khảo sát A §7 |
| N32 | HRM `TaxRateService` không lan thuế xuống `products`/`groups` như ERP ⇒ `products.vat_percent` lệch khi sửa thuế ở HRM | 2-D khảo sát A §7 |
| N33 | Hàng HRM tạo không có hàng gốc; hàng ERP cũ có hàng gốc lỗi thời sau khi sửa ở HRM (màn hàng gốc bị chặn ở 2-D) | 2-D khảo sát A §7 |
| N34 | 2 cron giá ERP (01:00 áp giá hiệu lực, N5) + 3 màn chỉ xem (Trạng thái cập nhật giá, Hàng sắp điều chỉnh tăng giá, Nhật ký cập nhật giá) còn ở ERP ⇒ chuyển sang HRM SAU (user 09/10, QC-10) | 2-D khảo sát C |
| N35 | Hệ số giá theo công ty đóng băng từ 2-D1 tới Phase 8 (không còn màn sửa) ⇒ hàng mới của hãng ở HP/Vinh/SG bán giá TPE (user chấp nhận 09/10, QC-3) | 2-D khảo sát C |
| N36 | Cập nhật giá theo hãng (ERP, 87 phiếu, dừng 12/2022): KHOÁ tạo/lưu bên ERP ở 2-D1 (giữ xem phiếu cũ); port sang HRM chưa làm (user 09/10) — xử lý sau | 2-D khảo sát C, QC-7 |
| N37 | ERP `WarehouseImportsController@getWareHouseImportLot` `:194-196` lỗi 500 với hàng không nhóm (khảo sát B sót) — sửa trong 2-D1 (M4b) | 2-D1 plan |
| N38 | `groups.barcode_template_type` dùng đủ mẫu 1–6 (không chỉ 2/3) — mẫu tem chuyển sang Loại SP (T1) | 2-D1 plan |
| N39 | `ERP/CLAUDE.md` ghi Laravel 8, thực tế `^6.2` | 2-D1 plan |
| N40 | `brands/list` gọi `products.importExcelAttribute` — chặn cùng 2-D1 | 2-D1 plan |
| N41 | ERP `barcode` khi `twoCode=false` luôn in cả hàng mẫu 2 (so chuỗi với số — lỗi cũ) | 2-D1 P2 |
| N42 | `product_infos/list` còn nút "Thêm mới" (route đã chặn ⇒ ra trang báo; T4 giữ menu) | 2-D1 P2 |
| N43 | `app/Model/ProductInfo/BaseProduct.php:76` còn `->group->` không null-safe | 2-D1 P2 |
| N44 | `Product::exportExcel` còn `model->name`, `origin->name`, `base_unit->name` không null-safe | 2-D1 P2 |
| N45 | ERP `ExampleTest` đỏ sẵn (GET `/` bị sso.check 302) | 2-D1 P2 |
| N46 | Màn in tem phiếu nhập ERP chết Angular `WarehouseImportArrangeDelivery is not defined` (`warehouse/warehouse_imports/barcode.blade.php:169-171`) — có sẵn gop_db | 2-D1 P3 |
| N47 | Xuất Excel Doanh thu theo hàng hoá 500: `RevenueByProductController.php:41` gọi `forCategory()` không tồn tại | 2-D1 P3 |
| N48 | Xuất PDF Doanh thu theo hàng hoá 500: `RevenueByProductController.php:54` biến `$category` chưa khai báo | 2-D1 P3 |
| N49 | Báo giá dịch vụ: JS `reading 'cost'` ở callback `getCost` (cả hàng cũ) | 2-D1 P3 |
| N50 | Báo giá mẫu: `$rootScope:infdig` (cả hàng cũ) | 2-D1 P3 |
| N51 | Chi tiết hàng hoá ERP `products/formShow.blade.php:936` `$parse:syntax`, ô nhà cung cấp trống | 2-D1 P3 |
| N52 | `<title>` trang "ngừng sử dụng" (Cập nhật giá theo hãng) vẫn là "Chức năng đã chuyển sang HRM" (`errors/moved_to_hrm.blade.php:7`) — của 2-D1 · **09/10 ✅ sửa (ERP `b2f1761789`)** | 2-D1 P3 |
| N53 | Hàng HRM "Đang nhập thông tin" (status 1/2 theo công ty) vẫn hiện + chọn được ở popup ERP với giá 0 — N8 chỉ ẩn status 4. Cần quyết trước khi bật tạo hàng trên HRM (trước Phase 7) · **09/10 ✅ sửa ở 2-D1 (ERP `b2f1761789`): ẩn status 1/2/4 ở công ty người dùng + 1/2 ở công ty tạo** | 2-D1 P3 |
| G6 | **Khoá theo CÔNG TY**: thêm trạng thái **4 "Ngừng kinh doanh"** trên dòng hàng × công ty (badge `#DC2626`). Mặc định đề xuất (user có thể sửa khi duyệt plan): chỉ khoá được từ *Đang kinh doanh* (3 → 4), mở khoá về 3; quyền 1652 của chính công ty; hàng cũ chưa có dòng ⇒ sinh dòng `coefficient=1` status 4 (như G4). Đã khoá thì BE chặn sửa tab Quản trị (423) tới khi mở khoá (CLAUDE.md). Màn *Đang kinh doanh* + cột *Công ty đang kinh doanh* không tính hàng status 4. ERP KHÔNG biết khoá này ⇒ việc ngoài luồng N8 |
| G7 | **Xoá = kiểm như ERP (5 điều kiện `canDelete`) + điều kiện §35b-4, qua hết thì XOÁ CỨNG** hàng + mọi bảng con (đơn vị, 6 dòng giá 0, dòng công ty, catalog, thuộc tính, phụ kiện, productables theo `productable_type`…) trong 1 transaction; FK 171 bảng là chốt chặn cuối. Hàng công ty khác đã lấy về thì "xoá" = gỡ dòng của công ty mình (dòng có hệ số cũ thì trả `status` về NULL, giữ `coefficient`) + catalog của công ty mình — không đụng `products` |
| G8 | **Sao chép: làm sau** (không thuộc 2-C) |
| G9a | **Nút Sửa ở menu dòng + footer màn chi tiết** (quyền 1652, khớp danh sách = chi tiết) cho hàng mọi trạng thái; công ty tạo sửa mọi tab, công ty lấy về chỉ tab Quản trị; đang Ngừng KD (4) thì ẩn Sửa tới khi mở khoá |
| G9b | Đồng ý: (1) Lấy về hàng loạt trần **100 mã/lượt**; (2) **không cho lấy về** hàng `products.status ≠ 1`; (4) toast Lưu bỏ vế "lập Yêu cầu tính giá". (3) xem G11 |
| G11 | 🔄 **Cờ "Phụ tùng ô tô" đặt ở TÍNH CHẤT HÀNG HOÁ** (thay §18b — bỏ 2 cờ ở Loại sản phẩm): thêm cột (vd `is_auto_parts`) vào `product_natures` + ô tick ở màn danh mục Tính chất hàng hoá. Tab *Phân loại xe* chỉ hiện khi Tính chất (suy từ Loại sản phẩm đã chọn) có tick; Hãng xe không bắt buộc. Tab *Nhóm máy* **luôn hiện** |
| G10 | Phạm vi 2-D (N2–N7) — chốt lúc lập plan 2-D |

⏳ Tồn nhỏ chốt lúc plan 2-C2: màn *Kho dữ liệu* (2-B) đang hiện cả 17.512 hàng ERP đã xoá/khoá (`products.status = 0`) với nhãn "Chưa sử dụng" — có lọc bỏ không.

## Chốt riêng đợt 2-C3 (popup Xây dựng catalog — đặc tả `c3-popup.md`)

| # | Chốt (04/10/2026) |
|---|---|
| B1 | **Giữ giỏ chờ như mockup + 1 endpoint `sync`**: Lưu gửi cả giỏ (cặp thêm + gỡ, nhiều Tiểu mục) chạy trong 1 transaction — sai 1 cặp thì không lưu gì. Trần **100 mã / mỗi lượt tick** (mockup); mỗi lần Lưu tối đa **1.000 cặp** thay đổi. Đóng popup khi giỏ còn ⇒ cảnh báo chưa lưu. Endpoint `assign`/`unassign` đã viết thay bằng `sync` |
| B2 | **Khoá bất kỳ cấp nào (Lĩnh vực/Chương/Mục/Tiểu mục) = không xếp THÊM** vào nhánh đó: hiện 🔒, không chọn để thêm; vẫn mở tab *Hàng trong tiểu mục* để xem + GỠ. BE chặn tương tự (xét cả 4 cấp) |
| B3 | Hàng **Ngừng kinh doanh (4)**: **ẩn khỏi tab Thêm** (không xếp mới); tab *Hàng trong tiểu mục* vẫn hiện để gỡ. Ô lọc Trạng thái: tab Thêm 3 lựa chọn (1·2·3 — chưa có "Đang tính giá"), tab trong tiểu mục thêm "Ngừng kinh doanh" |
| B4 | "Thông số cơ bản" = **mọi thuộc tính có giá trị** (`attribute_products`), thứ tự `attributes.position`, ghi `Tên: giá trị đơn vị` |
| B5 (tự chốt) | Popup loại hàng `products.status = 0`; số đếm trên cây = số hàng CỦA CÔNG TY đang xếp trong nhánh (đã lưu) ± giỏ chờ |

## Chốt riêng đợt 2-C1 (Tạo + sửa, công ty tạo — chi tiết `c1-ton.md`)

| # | Chốt (07/10/2026) |
|---|---|
| C1 | Lưu (tạo + sửa) **bắt buộc ≥ 1 Tiểu mục catalog** — kể cả hàng cũ |
| C2 | Sửa hàng cũ **bắt buộc chọn Loại sản phẩm** |
| C3 | `tech_coefficient` rule `min:0`, tạo mới mặc định 1 (T6: cột chung, chỉ công ty tạo sửa) |
| C4 | Trùng Tên × Model × Thương hiệu × Hãng SX: tạo luôn kiểm; sửa chỉ kiểm khi 1 trong 4 ô đổi |
| C5 | Ảnh không bắt buộc; khối ảnh ≤ 10, **ảnh đầu = `products.avatar`** (sinh đủ bản thumbnail/large như ERP) |
| C6 | Tài liệu kỹ thuật theo ERP: bảng dòng **Loại tài liệu + tệp** (`product_tech_attachments` + `files`) |
| C7 | ĐVT đã lưu **khoá** (không xoá/đổi hệ số/đổi đơn vị cơ bản), chỉ thêm dòng mới (+ 6 dòng giá 0 — G2) |
| C8 | Đổi Loại SP sang Tính chất không phụ tùng ⇒ **xoá liên kết xe khi Lưu**, cảnh báo trước |
| C9 | Thuộc tính: dòng = theo Loại SP ∪ đang có; tick = dùng (dòng tick phải có giá trị); đổi loại giữ giá trị trùng; không thêm tự do |
| C10 | Chọn Loại SP tự điền % VAT **khi ô VAT trống** |
| C11 | Nút "+" thêm nhanh **chỉ Model**, theo quyền danh mục Model |
| C12 | Sửa ở menu dòng 2 màn *Hàng hoá nhập thông tin* + *Dữ liệu hàng hoá công ty*; footer chi tiết có Sửa theo `can_edit` BE trả |
| A1 | `products.product_type` (chuỗi) để NULL theo §6 ⇒ việc ngoài luồng N9 |
| D1 | Sửa hàng cũ chưa có dòng công ty: **chỉ sinh dòng (coef 1, status 3) khi 4 ô quản trị đổi** so với giá trị đang hiện; NCC + catalog ghi bảng riêng không cần dòng |
| D2 | Hàng `products.status = 0` (ERP đã xoá) **không cho sửa** |
| D3 | Nhánh catalog đã lưu nay bị khoá: **giữ**, chỉ chặn thêm mới; vẫn tính ≥ 1 |
| D4 | Đơn vị cơ bản **không xét cờ `can_be_base`** (như ERP) |

## Chốt riêng đợt 2-C2 (Lấy về + sửa mức Quản trị — chi tiết `c2-ton.md`)

| # | Chốt (08/10/2026) |
|---|---|
| L1 | Lấy về mã đã có dòng hệ số cũ (`status NULL`) ⇒ UPDATE `status = 1`, **giữ `coefficient`**; chưa có dòng ⇒ thêm dòng coef 1, status 1 |
| L2 | Lúc lấy về **4 ô quản trị để trống hết** (không chép cột chung) — chấp nhận Bảo hành/Tồn tối thiểu đổi từ có giá trị → trống |
| L3 | **Chỉ lấy về được hàng mà công ty tạo đang kinh doanh** (trạng thái công ty tạo, suy theo 2-B, = 3) + `products.status = 1`; còn lại bỏ qua + báo lý do |
| L4 | Kho dữ liệu **lọc bỏ hẳn** hàng `products.status = 0` (17.512 mã) |
| L5 | Công ty lấy về Lưu tab Quản trị **bắt buộc ≥ 1 Tiểu mục** (lấy về thì không bắt buộc) |
| L6 | Popup "Xem hàng hoá Công ty khác" **làm sau**; màn Nhập thông tin đặt nút chuyển sang Kho dữ liệu |
| L7 | Công ty tạo sửa lớp chung ⇒ công ty lấy về thấy ngay, **không thông báo** |

## Chốt riêng đợt 2-C4 (Xoá + Khoá/Mở khoá — chi tiết `c4-ton.md`)

| # | Chốt (08/10/2026) |
|---|---|
| V1 | Khoá chỉ 3 → 4, mở khoá về 3; hàng cũ chưa có dòng ⇒ sinh dòng coef 1 status 4 (làm tròn giá ERP là tạm — tiền đề #8). Sửa hàng đang khoá ⇒ 423 |
| V2 | "Chưa phát sinh chứng từ" = 153 cột FK + ~50 bảng không FK mà HRM đang ghi |
| V3 | Nút Xóa ở danh sách theo cờ nhẹ (trạng thái + chủ + chưa ai lấy về); kiểm chứng từ đầy đủ khi bấm, vướng thì báo lý do |
| V4 | Công ty lấy về chỉ gỡ được khi trạng thái của mình = 1 |
| V5 | Gỡ = dọn hết phần công ty mình: dòng công ty (dòng ERP cũ `created_by NULL` ⇒ status NULL + xoá 4 ô, giữ hệ số), NCC, catalog |
| V6 | Hàng đang được hàng khác tham chiếu (máy dùng cho / phụ kiện / hàng kèm theo) ⇒ chặn xoá + báo lý do |
| V7 | Không làm hàng loạt — từng dòng (menu dòng + footer chi tiết) |
| V8 | Quyền 1652, không quyền mới |
| V9 | ~~xoá cả tệp S3 không còn dòng nào trỏ tới~~ → 🔄 08/10 (lúc xin "làm"): **KHÔNG xoá S3** — xoá cứng chỉ xoá dòng DB, tệp S3 giữ nguyên (như ERP). Bỏ FileJanitor / `PRODUCT_S3_PURGE` / sửa config khỏi plan |
