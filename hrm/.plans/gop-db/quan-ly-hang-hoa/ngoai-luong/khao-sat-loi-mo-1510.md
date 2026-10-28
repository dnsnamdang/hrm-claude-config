# Khảo sát các lỗi ngoài luồng còn mở — 15/10/2026 (CHỈ ĐỌC)

Phạm vi khảo sát: N79 · N82 · N84 · N85 · N86 · N87 · N91 · N97 · N98 · N99.
Code đọc: ERP `wt-erp-2d1` (`feat/2d1-erp-khong-loi`), HRM `wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}` (`feat/chuyen-doi-hang-hoa`).
DB `hrm_erp_giacty` chỉ SELECT. KHÔNG sửa code, KHÔNG ghi DB. Mô tả lỗi gốc nằm ở `ca-plan.md` (N79), `cd-plan.md` (N82, N84–N87), `ce-plan.md` (N91), `soat-bang-c.md` (N97–N99) — mô tả KHÔNG nằm trong `soat-bang-c.md` hết như đề bài ghi.

## Tóm tắt

| Mã | Còn? | Cỡ | Repo | Cần user chốt |
|---|---|---|---|---|
| N79 | Còn | S | ERP | Gán `sell_price`/`vat_percent` vào `$product_item` (đúng ý đồ) hay chỉ khai `$service = new stdClass` cho hết cảnh báo |
| N82 | Còn | S | hrm-api | Mặc định `show_children` của hàng báo giá trực tiếp = 1 (theo cột DB) |
| N84 | Còn | S | hrm-api (migration) | Có chạy migration vào DB nào; index đơn `product_id` hay ghép |
| N85 | Còn | S | hrm-client | Không |
| N86 | Còn | S | hrm-api (+ client nếu thêm tham số) | Ô lọc "Máy" ở bộ lọc picker dùng chung endpoint — có ẩn hàng khoá không |
| N87 | Còn (+6 chỗ cùng họ) | S | hrm-client | Sửa 1 chỗ hay cả 7 chỗ trong `components/product/form` |
| N91 | Còn (23 dòng dev) | S | hrm-api | Không (ERP đã chốt luật status NOT NULL) |
| N97 | Còn | S (no_set) / L (TN mới thiếu create/edit) | ERP | Chỉ vá `no_set` hay làm cả create/edit TN mới |
| N98 | Một phần: KH 232387 xác định được nguyên nhân; KH 1000 chưa | S–M | ERP | Cho phép mở trình duyệt tái hiện KH 1000; KH loại 1 không SĐT thì xử lý thế nào |
| N99 | Chưa xác nhận (code đọc đúng) | ? | hrm-client | Cần kiểm tay trước |

---

## N79 — `$service` chưa khai báo (ERP)

1. Còn. `app/Model/Customers/WrServiceQuotation.php`
   - dòng ~1072–1073 (trong `foreach ($product->choose_services as $product_item)`): `$service->sell_price = $device_error_cost->price_service;` và `$service->vat_percent = $cost->vat_percent;`
   - dòng ~1308 và ~1312: `$service->sell_price = ...` / `$service->vat_percent = $product_item->cost->vat_percent;`
   - `grep '\$service\b'` file này: chỉ có `$service` ở vòng khác (dòng 633, 700), KHÔNG có khai báo trong 2 hàm này.
2. Nguyên nhân gốc: copy từ đoạn cũ dùng biến `$service`, đổi vòng lặp thành `$product_item` nhưng quên đổi vế trái. Trên PHP 7.4 là "Creating default object from empty value" (Laravel đổi thành ErrorException nếu handler bắt), PHP 8 là Error. Hậu quả thực: giá/VAT của dịch vụ không bao giờ được gán vào dòng `choose_services` ⇒ màn sửa/xem báo giá BH-SC hiện giá/VAT cũ hoặc trống. Không liên quan chuyển đổi hàng hoá.
3. Sửa tối thiểu: đổi `$service->` thành `$product_item->` ở 4 chỗ. File: `ERP/app/Model/Customers/WrServiceQuotation.php`. Repo ERP.
4. Không migration, không ghi DB.
5. Kiểm: không có test sẵn; mở báo giá BH-SC có `device_error_id` + dịch vụ (Playwright ERP hoặc tinker gọi hàm) rồi so `sell_price`/`vat_percent` trước/sau. Cần 1 báo giá BH-SC có `choose_services` và `DeviceErrorCost`.
6. Rủi ro/câu hỏi: đây là THAY ĐỔI HÀNH VI (trước đó giá không được gán, hoặc lỗi 500 nếu handler bật). Đáp án A (đổi sang `$product_item`): giá/VAT hiện đúng theo lỗi thiết bị, có thể làm số tiền trên báo giá cũ khi mở lại khác so với đang thấy. Đáp án B (chỉ khai `$service = new \stdClass`): chỉ tắt cảnh báo, giữ nguyên hành vi hiện tại (giá không gán) — an toàn nhưng giữ lỗi logic. Nên hỏi người dùng nghiệp vụ bảo hành.
7. Cỡ: S.

## N82 — Xuất Excel báo giá KHÔNG theo BOM lỗi `$show_children` (hrm-api)

1. Còn. `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` `exportExcel` (~1209–1296): nhánh `isDirectQuotation()` dựng `new \stdClass()` cho từng hàng (`$p->id … $p->tpUnit`) nhưng KHÔNG gán `show_children`. Blade `resources/views/exports/bom_list.blade.php:128` và `:210` (và `bom_list_import_format.blade.php:123`): `@if($includeChildren && !($parent->erp_product_id && (int)$parent->show_children === 0))` ⇒ stdClass không có thuộc tính ⇒ "Undefined property". Chỉ nổ khi hàng cha có `erp_product_id` (short-circuit) — BG-2026-00111 có 271 hàng. Nhánh theo BOM dùng Eloquent nên thiếu thuộc tính trả null, không lỗi.
   - DB: `quotation_product_prices.show_children` có thật (default 1); trong 4.240 hàng ERP cha: 4.238 = 1, 2 = 0.
2. Nguyên nhân gốc: object ảo của báo giá trực tiếp thiếu trường mà blade đọc. `BomListExport.php:546` đã tự xử lý bằng `?? 0` (comment "hàng direct không có show_children → null → 0 → collapse") — tức đang LỆCH với blade: nếu blade chạy được thì hàng con bị gập (0), trong khi DB nói mở (1).
3. Sửa tối thiểu: thêm `$p->show_children = isset($qpp->show_children) ? (int) $qpp->show_children : 1;` vào `$p` (cạnh `$p->erp_product_id`). Đồng thời sửa `BomListExport.php:546` đổi `?? 0` thành `?? 1` + sửa comment 544–545 cho khớp (nếu không ảnh chèn sai dòng). File: `QuotationController.php`, `app/ExcelExport/BomListExport.php`. Repo hrm-api.
4. Không migration.
5. Kiểm: PHPUnit/feature gọi `GET quotations/{id}/export-excel` cho báo giá trực tiếp có hàng ERP cha có con; assert 200 + số dòng. Playwright không cần. Dữ liệu: BG-2026-00111 trên DB dev (đã có sẵn).
6. Câu hỏi: mặc định `show_children` = 1 (theo cột DB, nghĩa là xuất cả hàng con) hay 0 (theo comment cũ ở BomListExport)? Đáp án 1: khớp màn hình/DB; thêm dòng con vào Excel. Đáp án 0: Excel gập hết — sai so với dữ liệu 4.238/4.240 hàng đang mở.
7. Cỡ: S.

## N84 — thiếu index `product_vehicle_model_has_life.product_id` (hrm-api)

1. Còn. `SHOW INDEX`: chỉ có `PRIMARY(id)`. 48.736 dòng / 91 hàng trên dev (~80k prod). `EXPLAIN delete … where product_id=5` ⇒ `type=ALL`, rows≈48.817. Chỗ dùng: `ProductWriteService.php:635` (xoá khi lưu), `ProductLifecycleService.php:215`, `ProductDetailResource.php:73` (exists), `ProductPickerService.php:471` (EXISTS tương quan theo `vl.product_id` + `life_id`).
2. Nguyên nhân gốc: migration ERP gốc (2022_11_07) chỉ tạo khoá chính. Với InnoDB, DELETE theo cột không index khoá phạm vi rộng ⇒ lưu hàng song song có thể chờ khoá; picker EXISTS quét cả bảng cho mỗi hàng.
3. Sửa tối thiểu: migration mới ở hrm-api (bảng ERP nhưng DB đã gộp ⇒ đặt ở hrm-api như `2026_10_03_000001_add_search_indexes_to_products_tables.php`, có `hasIndex` guard, `down()` drop): `index(['product_id','life_id'])` (phục vụ cả DELETE theo `product_id` lẫn EXISTS `product_id + life_id`). Plan 4.2 đã dự kiến tên `2026_10_13_000002_add_picker_indexes` nhưng file KHÔNG tồn tại. Repo hrm-api. Có thể gộp luôn `productables(product_id, productable_type, productable_id)` đã ghi ở `popup-tim-kiem-hang-hoa/plan.md:1631` nếu user muốn (kiểm trùng index sẵn có trước).
4. CẦN migration + chạy vào DB (bảng 48k dòng, build index tức thì; prod 80k vẫn nhanh; ALTER ONLINE trong InnoDB nhưng nên chạy ngoài giờ).
5. Kiểm: sau migrate, `EXPLAIN` lại ⇒ `type=range/ref`; chạy `ProductWriteApiTest` / `ProductLifecycleApiTest` (có đụng bảng này). Migration chạy trên DB test, không chạy vào `hrm_erp_giacty` nếu chưa được phép.
6. Câu hỏi: chạy migration vào DB nào (phải hỏi riêng theo luật CLAUDE.md); index ghép `(product_id, life_id)` (đề xuất) hay đơn `(product_id)` (đơn giản, DELETE đủ dùng, EXISTS vẫn lọc `life_id` sau).
7. Cỡ: S.

## N85 — lỗi BE `galleries.N` không hiện ở FE (hrm-client)

1. Còn. `components/product/form/ProductFormGallery.vue:11`: `<V2BaseError :message="localError || fieldError('galleries')" />`. BE (`ProductRequest.php:95–96`) trả khoá `galleries` (mảng quá 10) và `galleries.N` (URL sai regex / chuỗi rỗng / quá 1000 ký tự). Chỉ khoá đầu có chỗ hiện.
2. Nguyên nhân gốc: FE chỉ tra đúng khoá `galleries`, không gom khoá con. Các component khác (Vehicles dòng 383, TechDocs dòng 88) đã gom khoá con.
3. Sửa tối thiểu: thêm computed `galleryError` = `localError || fieldError('galleries') ||` lỗi đầu tiên của `fieldError('galleries.'+i)` với i từ 0 đến `form.galleries.length-1`; hiển thị ở `V2BaseError`. Tuỳ chọn: viền đỏ thumbnail lỗi. File: `hrm-client/components/product/form/ProductFormGallery.vue`. Repo hrm-client.
4. Không migration.
5. Kiểm: Playwright (mock response 422 `errors: {'galleries.0': [...]}` bằng `page.route` trên POST lưu hàng) ⇒ đo nội dung `.v2-error` trong khối ảnh; cần cả jump-to-error (marker `.v2-error`, xem memory). Dữ liệu: form sửa 1 hàng bất kỳ.
6. Rủi ro thấp, ảnh chỉ đến từ upload nên hiếm. Không câu hỏi nghiệp vụ.
7. Cỡ: S.

## N86 — ô chọn hàng kèm theo chưa lọc hàng khoá ở công ty (hrm-api)

1. Còn. `Modules/MasterData/Services/Product/ProductOptionService.php:127–164` `itemSearch`: lọc `p.status = 1`, `excludeOwnerTemp`, exclude id, keyword — KHÔNG lọc `product_company_coefficients.status = 4` của công ty đang làm việc. BE đã chặn lúc lưu (`ProductRequest::checkKitStatus`, `ProductRequest.php:~420`: "Hàng hoá đang ngừng kinh doanh, không chọn thêm được") ⇒ chọn xong, bấm Lưu mới biết.
   Endpoint `GET master-data/products/item-search` có 3 người gọi FE: `ProductItemPickerModal.vue:103`, `ProductFormItemsTable.vue:125` (hàng kèm theo — cần lọc) và `picker/ProductPickerAdvancedFilters.vue:201` (ô lọc "Máy" của popup tìm hàng — KHÔNG nên ẩn hàng khoá).
2. Nguyên nhân gốc: lọc khoá chỉ làm ở validate (C-d-2), quên làm ở nguồn chọn.
3. Sửa tối thiểu: thêm tham số tuỳ chọn `exclude_locked=1` cho `itemSearch` (controller `ProductOptionController.php:53–60` + service) ⇒ `whereNotExists` pcc `company_id = current_company_role AND status = 4` (dùng `ProductCompany::STATUS_STOPPED`); 2 chỗ gọi hàng-kèm-theo truyền thêm tham số. File: `ProductOptionController.php`, `ProductOptionService.php` (hrm-api); `ProductItemPickerModal.vue`, `ProductFormItemsTable.vue` (hrm-client). Hàng ĐÃ gắn từ trước và nay bị khoá vẫn hiện trong bảng (chỉ lọc ô chọn mới), nhất quán với luật "dòng đã gắn trước giữ".
4. Không migration.
5. Kiểm: PHPUnit (đã có test itemSearch? kiểm `ProductOptionApiTest` rồi thêm ca: hàng khoá ở cty hiện tại không xuất hiện khi `exclude_locked=1`, xuất hiện khi không truyền; hàng khoá ở cty khác vẫn xuất hiện). Playwright: mở form hàng, ô "Hàng kèm theo", gõ mã hàng đã khoá ⇒ không có kết quả. Cần 1 hàng có pcc.status=4 ở công ty test (test tự dựng).
6. Câu hỏi: ô lọc "Máy" ở bộ lọc picker có cần ẩn hàng khoá không? Đáp án KHÔNG (đề xuất): dùng tham số riêng, lọc cũ vẫn tìm được máy đã khoá. Đáp án CÓ: lọc luôn mặc định, không cần tham số nhưng người dùng không lọc được theo máy đã ngừng KD.
7. Cỡ: S.

## N87 — `.text-muted` = đỏ ở `ProductFormVehicles` (hrm-client)

1. Còn. `components/product/form/ProductFormVehicles.vue:8`: `<div v-else-if="!loaded" class="text-muted py-2 vehicles-loading">Đang tải danh mục xe...</div>`. Nguyên nhân: `assets/scss/custom.scss:241` (và `custom.css`, `custom-theme.scss:190`…) đặt `.text-muted { color: #dc3545 !important; }` toàn cục.
   Cùng họ lỗi (hint/placeholder cũng đỏ) trong thư mục form hàng hoá: `ProductFormGallery.vue:3` và `:19`, `ProductFormGeneral.vue:180` ("Chưa có video nào."), `ProductFormUnitsTable.vue:83`, `ProductFormTechDocs.vue:43`, `ProductItemPickerModal.vue:16` ("Đã chọn: N").
2. Nguyên nhân gốc: theme của hrm-client dùng `.text-muted` làm màu đỏ cảnh báo ⇒ không dùng cho chữ phụ.
3. Sửa tối thiểu: thay bằng class chữ xám có sẵn (cần tìm class chuẩn: ví dụ `text-secondary` hoặc style cục bộ `color:#6b7280`; đo `getComputedStyle` trước khi chọn). Làm 1 chỗ theo mã N87 hoặc cả 7 chỗ. File: tuỳ chọn, tối thiểu `ProductFormVehicles.vue`. Repo hrm-client.
4. Không migration.
5. Kiểm: Playwright đo `getComputedStyle(el).color` của dòng "Đang tải" (chặn API vehicle để giữ trạng thái đang tải — theo luật CLAUDE.md phải tái hiện trước khi sửa) ⇒ trước = rgb(220,53,69), sau = xám. Cập nhật ca e2e màn hàng hoá nếu có assert màu.
6. Câu hỏi: sửa chỉ 1 chỗ theo N87 hay quét cả 7? Đề xuất cả 7 (cùng 1 thư mục, cùng kiểu lỗi, ít rủi ro). Cũng cần user xác nhận màu xám chuẩn (mặc định theo style V2 đo từ app).
7. Cỡ: S.

## N91 — `AdminData::source` đọc dòng hệ số status NULL (hrm-api)

1. Còn. `Modules/MasterData/Transformers/Product/AdminData.php:21–26`: `source()` trả `$product->companyRowFor($companyId) ?: $product` — dòng pcc nào cũng nhận, kể cả `status IS NULL`. `mediaAndGuarantee()` (dòng 53–71) cũng đọc mọi dòng pcc của công ty, không lọc status. ERP đã chốt luật khác: `Product::adminRowFor()` (`ERP app/Product.php:~296`) `$row && $row->status !== null ? $row : null`.
   - DB dev: `product_company_coefficients` 113.782 dòng, 298 dòng status NULL (298 đều trống bảo hành), và 23 dòng NULL-status trống `guarantee` mà `products.guarantee` > 0 — đúng 23 ca lệch đã ghi.
2. Nguyên nhân gốc: HRM viết luật "có dòng ⇒ đọc dòng" trước khi ERP bổ sung điều kiện status NOT NULL (ce-plan.md:57).
3. Sửa tối thiểu: ở `source()` coi dòng có `status === null` như không có dòng (lùi cột chung `products`); ở `mediaAndGuarantee()` thêm `->whereNotNull('status')` vào truy vấn `$own`. Kiểm thêm 2 chỗ đọc cùng luật: `ProductExportService.php:~260` (min_stock_qty qua `$lk['own']`) và `ProductPickerService.php:233` (qua source — tự hưởng). File: `AdminData.php` (+ `ProductExportService.php` nếu `$lk['own']` không lọc status). Repo hrm-api.
4. Không migration.
5. Kiểm: PHPUnit — ca: hàng có dòng pcc NULL-status + `products.guarantee=12` ⇒ `guaranteeText` = "12 tháng"; ca có status thật + guarantee riêng ⇒ lấy riêng. Test chứng từ: báo giá/Excel báo giá (dùng `mediaAndGuarantee`) ra bảo hành đúng. Lấy 1 trong 23 hàng lệch làm mẫu (SELECT lại để lấy id).
6. Không câu hỏi nghiệp vụ (ERP đã chốt, đây là đồng bộ luật). Ghi chú: màn chi tiết `ProductDetailResource.php:29` còn đọc `companyRowFor` trực tiếp cho vài trường — soát có dùng `guarantee`/`min_stock_qty` không trước khi chốt phạm vi.
7. Cỡ: S.

## N97 — YC đặt hàng NK 2 / TN mới thêm hàng tay lỗi `unit_coefficient` (ERP)

1. Còn.
   - `resources/views/partials/classes/order/OrderRequestProduct2.blade.php:3–11`: constructor `for (let key in product) this[key] = product[key]` không có `no_set`; class có `get unit_coefficient()` (dòng 62, chỉ getter) ⇒ gán khoá `unit_coefficient` cấp ngoài (do `ProductsController@getData` thêm khi `query_stock=1`) ném TypeError "has only a getter" (strict mode của class).
   - `InlandOrderRequestProduct2.blade.php:3–10` y hệt; getter ở dòng 54.
   - Mẫu đúng: `RootOrderRequestProduct.blade.php:5–8` và `InlandOrderRequestProduct.blade.php:5` (`this.no_set = ['unit_coefficient', ...]`).
   - Lớp `InlandOrderRequestProduct2` còn được `inland_order_request2/{create,edit,show}` và `InlandOrderRequest2.blade.php` dùng ⇒ lỗi áp cho cả màn TN cũ khi thêm hàng tay, không chỉ "TN mới".
   - `InlandOrderRequestNewController` chỉ có `index, forApprover, forDepartmentApprover, searchData, show, print`; route `create/edit/store/update/approve/…` (routes/web.php 2967–2985) trỏ vào method KHÔNG tồn tại ⇒ 500; 3 view index vẫn có nút "Tạo" trỏ `inlandOrderRequestNew.create`.
2. Nguyên nhân gốc: commit f094e5a46a (29/01/2024) thêm `unit_coefficient` vào kết quả `getData`; 2 class này chép mọi khoá mà không loại. Không ai gặp vì 3.793 phiếu NK 2 sinh tự động.
3. Sửa tối thiểu: thêm `this.no_set = ['unit_coefficient']` + `if (!this.no_set.includes(key))` vào cả 2 constructor. File: `OrderRequestProduct2.blade.php`, `InlandOrderRequestProduct2.blade.php`. Repo ERP. Có thể đẩy riêng gop_db (đã ghi ở soat-bang-c).
   Phần "TN mới thiếu create/edit/…" KHÔNG nằm trong sửa tối thiểu: phải viết cả 7 action controller (tương đương `InlandOrderRequest2Controller`), cỡ L, ngoài phạm vi feature.
4. Không migration.
5. Kiểm: Playwright ERP — mở `order_request2/create` (và `inland_order_request2/create`), thêm hàng bằng ô tìm hàng ⇒ không còn TypeError trong console, dòng hàng hiện đủ ĐVT. Cần 1 hàng có `query_stock`. `view:cache` KHÔNG lint blade (xem memory) ⇒ phải mở trang thật.
6. Câu hỏi: (a) chỉ vá `no_set` (đề xuất) hay làm cả create/edit cho TN mới? Đáp án (a): hết lỗi JS ở 2 màn có controller; nút "Tạo" của TN mới vẫn 500 (lỗi cũ, ngoài feature). Đáp án (b): L, phải có spec nghiệp vụ. (b) có nên gỡ nút "Tạo" khỏi 3 view index TN mới trong lúc chờ không.
7. Cỡ: S (no_set) / L (create-edit TN mới).

## N98 — Chi tiết KH (CSKH) lỗi JS khi mở (ERP)

1. Còn một phần. View `resources/views/customercare/customermanager/show_.blade.php:3035–3036` (`CustomerManagerController@show`, controller dòng 168): `let customer = @json($customer); $scope.customer = new Customer(customer);`. `partials/classes/sale/Customer.blade.php:8–9`:
   ```
   this.mobile = customer.mobile;
   if (customer.customer_type == 1) this.phones = customer.mobile.split(',')...
   ```
   - KH 232387: `customer_type=1` và `mobile IS NULL` ⇒ `null.split` TypeError "đọc null" ⇒ cả controller AngularJS của trang chết. Đây là KH DUY NHẤT trên dev thuộc dạng này (`customer_type=1 AND mobile IS NULL` = 1 dòng).
   - KH 1000: `customer_type=2`, `mobile` có giá trị ⇒ KHÔNG dính nguyên nhân trên. Chưa xác định được qua đọc code/DB (cột không-null bình thường). Cần mở trang bằng trình duyệt thật, xem dòng báo lỗi đầu tiên trong console. Ứng viên cần kiểm: các setter của `Customer` (`delivery_places` gọi `value.map` khi null, `is_manufacturer`), `customer.customer_groups`, `@json($customer->businessFieldPairs())`/`activityTypeIds()` (đọc catalog HRM) và `loadCustomerScopes`.
2. Nguyên nhân gốc (232387): dữ liệu KH cá nhân thiếu SĐT, class giả định `mobile` luôn có chuỗi. Lỗi cũ, không do chuyển đổi hàng hoá.
3. Sửa tối thiểu (232387): `(customer.mobile || '').split(',')…` (+ `this.phones` mặc định `['']` nếu rỗng, vì `customer_type` setter cũng đặt `phones=['']`). File: `ERP/resources/views/partials/classes/sale/Customer.blade.php` (file này dùng chung nhiều màn: create/edit KH, CSKH…). KH 1000: chờ tái hiện. Repo ERP.
4. Không migration.
5. Kiểm: Playwright ERP mở `customermanager/232387` và `/1000` trước/sau, đọc `page.on('pageerror')` + đo trang render được (số khối). Cần đăng nhập ERP local (cổng php 8000 đang chạy).
6. Câu hỏi: (a) cho phép mở trình duyệt (chỉ đọc) tái hiện KH 1000 trước khi xin sửa không; (b) với KH loại 1 không có SĐT, form hiện 1 ô SĐT trống (đề xuất) — đồng ý.
7. Cỡ: S (232387); KH 1000 chưa rõ, tạm tính S–M.

## N99 — `ChooseEquipmentTypeModal` không nhận chọn loại (hrm-client)

1. CHƯA xác nhận lỗi: code hiện tại đọc đúng. `components/customer-care/ChooseEquipmentTypeModal.vue`: `<V2BaseSelectInModal v-model="productType" :options="typeOptions" />` với `typeOptions=[{id:1,name:…},{id:2,name:…}]`, nút `:interactable="!!productType"`. `V2BaseSelectInModal` nhận `value`, phát `input` khi select2 `change` (`V2BaseSelectInModal.vue:290–294`), chuyển option `{id,name}` thành `{id,text}` (dòng 140–153). Không thấy sai kiểu dữ liệu (`'1'` chuỗi vẫn truthy, `choose()` dùng `Number`). Cách dùng giống các popup khác (`HoldListModal.vue`, `wr-service-contracts/index.vue:210`).
2. Nghi ngờ nguyên nhân: kịch bản Playwright bấm option select2 (hoặc `selectOption` trên `<select>` ẩn) không phát `change` jQuery mà select2 lắng nghe ⇒ dương tính giả. Chưa loại trừ lỗi thật ở `dropdownParent`/`renderKey++` (select2 tạo lại sau khi modal mount — `V2BaseSelectInModal.vue:~188–200`), vì có thể mất `change`.
3. Hướng sửa: chưa có. Nếu kiểm tay thấy lỗi thật: so với popup khác dùng cùng component rồi sửa tại popup này (không đụng V2BaseSelectInModal dùng chung 5 nơi). Repo hrm-client.
4. Không migration.
5. Kiểm: kiểm tay trước (mở `customer-care/warranty-repair-requests` thêm/sửa → "Thêm trang thiết bị" → chọn loại). Sau đó Playwright: bấm đúng `.select2-results__option` trong `.modal-content`, đo `button` Chọn hết `disabled`, bắt `chosen` sang popup kế tiếp.
6. Câu hỏi: cần user (hoặc người dùng khác) kiểm tay trên trình duyệt thật. Nếu OK ⇒ đóng N99 là dương tính giả và sửa script test; nếu hỏng ⇒ mở lại khảo sát.
7. Cỡ: chưa xác định (0 nếu dương tính giả).

---

## Đề xuất gom đợt sửa

Mỗi đợt cần user trả lời riêng "làm" kèm phạm vi (repo · nhánh · file · có migration không) theo luật CLAUDE.md gốc.

**Đợt 1 — hrm-api (nhỏ, không đụng UI): N82 + N91 (+ N86 phần BE nếu chọn thêm tham số).**
- Cùng nhánh `feat/chuyen-doi-hang-hoa`, đều là chỉnh nhỏ trong BE, kiểm bằng PHPUnit. Không migration. Nên làm kèm migration N84 ở đợt riêng (xem đợt 2) để tách ghi DB.

**Đợt 2 — hrm-client + phần BE nối: N85 + N87 + N86 (FE) (+ N99 sau khi kiểm tay).**
- Đều là hrm-client, đụng form hàng hoá (`components/product/form/*`) ⇒ kiểm một lượt Playwright chung (đo DOM: màu chữ, lỗi ảnh, ô hàng kèm theo). N86 cần đợt 1 xong phần BE (hoặc làm BE cùng lúc).
- N84 (migration index) tách thành bước riêng trong đợt này hoặc đợt 1, vì là bước ghi DB: hỏi user chạy vào DB nào.

**Đợt 3 — ERP (worktree `wt-erp-2d1`): N79 + N97 (no_set) + N98 (232387).**
- Cùng repo ERP, đều sửa file blade/model nhỏ, kiểm bằng Playwright ERP (cổng 8000). Có thể đẩy riêng gop_db theo ghi chú soat-bang-c (cần xác nhận lại theo memory "Không merge vào gop_db — chỉ feat Chuyển đổi hàng hoá").
- Nên hỏi trước: N79 chọn đáp án A hay B; N98 KH 1000 tái hiện trước.

**Để ngoài đợt:** N97 phần create/edit TN mới (L, cần spec); N99 chờ kiểm tay; N98 KH 1000 chờ tái hiện. Các mục còn lại trong `viec-con-lai.md` §1 (N88, N92, N94-rest, N100, A3…) không thuộc phạm vi khảo sát này.
