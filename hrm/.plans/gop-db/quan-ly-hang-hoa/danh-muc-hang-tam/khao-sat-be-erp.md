# Khảo sát BE ERP — luồng Hàng tạm (Phase 6 "Danh mục hàng tạm")

> Khảo sát CHỈ ĐỌC, ngày 12/10/2026. Không sửa source, không ghi DB.
> Nguồn ERP: worktree `wt-erp-2d1` nhánh `feat/2d1-erp-khong-loi` (HEAD `443c812553`, đã có G3 + G6 + T7).
> Nguồn HRM đối chiếu: `wt-chuyen-doi-hang-hoa/hrm-api` nhánh `feat/chuyen-doi-hang-hoa`.
> DB: `hrm_erp_giacty` (local, dữ liệu chụp tới **15/09/2026**). Chỉ dùng `SELECT`.
> "6 tháng gần nhất" = từ 15/03/2026 tới mốc chụp. Đường dẫn ERP tính từ gốc repo ERP.

---

## 0. Tóm tắt nhanh

| Mục | Kết luận |
|---|---|
| Khối lượng | `tmp_products` **1.957** dòng (id 1–1.957, từ **02/08/2025** tới 14/09/2026; bảng đã bị làm lại từ đầu 08/2025). 6 tháng gần nhất **1.001** hàng tạm, ~150/tháng. `tmp_product_requests` **579** phiếu (294 trong 6 tháng) |
| Kết quả duyệt | 1.874 đã duyệt (95,8%) · 55 bị từ chối · 27 đã xoá · 1 chờ duyệt · **0** "Đang tạo" |
| Sinh hàng thật | Mỗi hàng tạm đã duyệt sinh **đúng 1** `products` (1.874 ⇄ 1.874). Chiếm **18,9%** hàng tạo mới từ 08/2025 (1.874/9.890), **18,5%** trong 6 tháng (961/5.203) |
| Duyệt = tự đặt giá | Có. `approve` gọi `Product::createRecord` (`app/Product.php:6983`). Hàm này ghi **giá vốn + 6 loại giá bán** do người duyệt nhập, rồi đặt `pcc.status = 3` (Đang kinh doanh). Hàng **không đi qua** YCHG→YCTG→PTG. Đây là xung đột chính với §29a-1 |
| Công ty nhận giá | `products.company_id` = **công ty quản lý Hãng SX** (`manufactures.company_id`). FE tự gán và khoá ô (`tmp_products/edit.blade.php:95,102`, `form.blade.php:1251`). Đo được 1.874/1.874 trùng. Đây **không phải** công ty của người tạo hàng tạm (lệch 24 ca), dù comment G3 ghi "công ty hàng tạm" |
| Chứng từ dùng `tmp_product_id` | 16 cột ở 16 bảng, **chỉ `products.tmp_product_id` có dữ liệu**. Mọi bảng báo giá/HĐ/phân tích dự án đều **0 dòng**. Cột này bị trùng nghĩa: 8.931 dòng có giá trị, nhưng 7.057 dòng trỏ vào id của bảng hàng tạm **cũ** (trước 08/2025), nên 2.706 giá trị bị trùng |
| HRM đã đụng tới | HRM Assign (báo giá dự án Trúng thầu) **đẩy hàng tạm sang ERP qua API** `/api/v1/tmp-product-requests/sync-from-hrm` và kéo trạng thái về (`TmpProductSyncService`). `QuotationErpSyncService::createTmpProducts` còn **INSERT thẳng** vào `tmp_products`. Trên DB đo được 0 lần dùng (`quotations.tmp_sync_status` = NULL cả 206 dòng) |
| Quyền | 6 quyền ERP (guard `web`): `Duyệt hàng tạm` 100037 (18 role, 60 NV đang làm) · `Thêm báo giá` 100038 (đây là quyền cho route tạo, 460 NV) · `Xem danh sách hàng tạm` 100981 · 3 quyền xem phiếu YC 100932–100934. Người duyệt còn có thể là người **phụ trách Thương hiệu–Hãng** (`assign_histories.brand_employee_id`, 21 NV) |

---

## 1. Route, controller, model

### 1.1 Route (`routes/web.php`, nhóm `prefix=admin`)

| Route name | Method · URL | Action | Middleware riêng | Ghi chú |
|---|---|---|---|---|
| `tmpProductStore` | POST `/admin/tmp_products` | `TmpProductsController@store` | `checkPermission:Thêm báo giá` | `:681` |
| `tmpProductIndex` | GET `/admin/tmp_products` | `@index` | — | `:682`. Đây là màn "Danh mục hàng tạm" |
| `tmpProductEdit` | GET `/{id}/edit` | `@edit` | `checkDueConfigs` | `:683`. Màn duyệt/sửa |
| `tmpProductReject` | PUT `/{id}/reject` | `@reject` | `checkDueConfigs` | `:684` |
| `tmpProductShow` | GET `/{id}/show` | `@show` | — | `:685`, trả chuỗi **"Đang phát triển"** (`:929-932`) |
| `tmpProductDelete` | GET `/{id}/delete` | `@delete` | — | `:686`, xoá bằng **GET** |
| `tmpProductApprove` | POST `/{id}/approve` | `@approve` | `checkDueConfigs` | `:687` |
| `tmpProductDraftUpdate` | POST `/{id}/draft` | `@updateDraft` | `checkDueConfigs` | `:688` |
| `tmpProduct.searchData` / `exportExcel` / `exportCSV` / `exportPDF` | GET | | — | `:689-692`. Excel/CSV xuất `TmpProduct::all()` (không lọc quyền); PDF lấy 30 dòng, host gán cứng `localhost:8000` (`:203-208`) |
| `myTmpProductIndex` / `myTmpProductShow` / `myTmpProduct.searchData` | GET `/admin/my_tmp_products…` | `MyTmpProductsController` | — | `:696-699`. "Hàng tạm của tôi" (menu tài khoản `topheader.blade.php:171`). `show` cũng trả **"Đang phát triển"** (`MyTmpProductsController.php:136-154`) |
| `TmpProductRequest.index/create/show/store/searchData/print/updateNote` | `/admin/sale/tmp_product_requests…` | `TmpProductRequestController` | — | `:3636-3643`. Không route nào gắn `checkPermission` |
| API `POST /api/v1/tmp-product-requests/sync-from-hrm` | | `Api\TmpProductRequestSyncController@store` | **không api key** | `routes/api.php:74-77`. HRM gọi |
| API `POST /api/v1/tmp-product-requests/approved-status` | | `@approvedStatus` | không api key | HRM kéo trạng thái |
| `quotation.tmpProductChange(Store)` | `/…/{id}/tmpProductChange` | `QuotationsController` | | `:5376-5377`. Báo giá ERP cũ đổi hàng tạm sang hàng thật. `quotation_products.tmp_product_id` = 0 dòng ⇒ đường chết |

Chưa route hàng tạm nào gắn `productMovedToHrm`.

### 1.2 Model

| Model | Bảng | Ghi chú |
|---|---|---|
| `App\Model\Product\TmpProduct` (extends `BaseProduct`) | `tmp_products` | 5 trạng thái `:11-15`; quyền `canApprove/canDelete/canView/canEdit` `:56-74`; lọc danh sách `searchByFilter :176-246` |
| `TmpProductUnit` · `TmpProductUnitPrice` | `tmp_product_units` · `tmp_product_unit_prices` | |
| `TmpAttributeProduct` · `TmpProductGallery` · `TmpProductVideo` · `TmpProductSupplier` · `TmpProductBarcode` · `TmpProductCategory` · `TmpProductPrice` | bảng con | |
| `TmpProductRequest` | `tmp_product_requests` | 4 trạng thái **suy ra** từ hàng con (`getStatusAttribute :178-204`), không có cột `status` |
| `TmpProductVersion` | — | `use` ở `TmpProductsController.php:24` nhưng **không có class và không có bảng**. Không gọi tới nên không lỗi |

---

## 2. Bảng CSDL

`SHOW TABLES LIKE '%tmp%'` cho ra 13 bảng có tên `tmp_product*` / `tmp_attribute_products`. Các bảng `tmp_warehouse_*`, `tmp_position_transfer_details`, `tmp_begining_acc`, `tmp_borrow_sell*` cũng có chữ `tmp` nhưng **là bảng nháp của nghiệp vụ kho**, không liên quan hàng tạm. Quan hệ `WarehouseExport/Import::tmp_products()` cũng vậy.

| Bảng | Số dòng | Cột chính | Ghi chú |
|---|---|---|---|
| `tmp_products` | **1.957** | `id, status, code, name, english_name, product_type, product_cate (NOT NULL), model_id, brand_id?, manufacture_id?, origin_id?, unit_id?, group_id, barcode_id, avatar, product_attributes, norm, guarantee(_type), date_delete, note, comment, approver_id, tmp_product_request_id, vat_percent (NOT NULL), vat_percent_tax_rate_id, weight, size, tech_attachments, created_by (NOT NULL), …` | **Không có `company_id`** (`DocumentCompany::NO_COMPANY_TABLES`, `app/Services/Product/DocumentCompany.php:18`). `brand/manufacture/origin` được nới NULL (migration `2026_06_06_000001`) để nhận hàng nháp từ HRM. `code` rỗng ở cả 1.957 dòng |
| `tmp_product_units` | 1.957 | `product_id, unit_id, is_base, unit_coefficient, cost_price, buy_price` | **Mỗi hàng tạm đúng 1 ĐVT** (1.957 dòng, đều `is_base=1`). `cost_price > 0` cả 1.957 dòng; `buy_price > 0` 114 dòng |
| `tmp_product_unit_prices` | 10.919 | `tmp_product_unit_id, price_type_id, price, coefficient, sale_max_percent` | Loại 1–5 mỗi loại 1.957 dòng, loại 6 có 1.134 dòng. **Mọi `price` và `coefficient` = 0**: bảng giá trong form tạo đã bị comment (`partials/tmpProduct/createTmpProductForm.blade.php:336-380`). Người tạo chỉ nhập **giá vốn** |
| `tmp_product_prices` | **0** | cấu trúc giá cũ | bỏ |
| `tmp_product_requests` | 579 | `code (PYCDHT-xxxxx), note, company_id, department_id, created_by, hrm_quotation_id, hrm_quotation_code, hrm_project_id, hrm_project_name` | công ty 1: 365 · 4: 211 · 3: 3. `hrm_quotation_id` có giá trị: **0** dòng. Trung bình 3,1 hàng/phiếu, tối đa 39 |
| `tmp_attribute_products` | 642 | `product_id, attribute_id, unittech_id, value` | thông số kỹ thuật |
| `tmp_product_suppliers` | 38 | `product_id, supplier_id` | |
| `tmp_product_videos` | 2 | | |
| `tmp_product_galleries` · `tmp_product_barcodes` · `tmp_product_categories` | 0 · 0 · 0 | | `TmpProductGallery` vẫn được ghi trong `store/approve/updateDraft` |

### 2.1 Phân bố

| `tmp_products.status` | Nghĩa | Số dòng | created_at min – max |
|---|---|---|---|
| 1 | Đã duyệt | 1.874 | 02/08/2025 – 14/09/2026 |
| 0 | Không duyệt | 55 | 27/08/2025 – 08/09/2026 |
| -1 | Đã xoá (xoá mềm) | 27 | 13/10/2025 – 07/09/2026 |
| 2 | Chờ duyệt | 1 | 05/09/2026 |
| 3 | Đang tạo (nháp từ HRM) | **0** | — |

- Theo năm: 2025 có 731 dòng, 2026 có 1.226 dòng. Từ 10/2025 tới 09/2026 mỗi tháng có 61–288 dòng (cao nhất 04/2026: 288).
- Gắn với phiếu YC: 1.804 dòng. Không gắn phiếu: 153 dòng (rải đều các tháng, 2–29 dòng/tháng). Có thể là tạo từ popup trên báo giá ERP cũ, hoặc tạo ở màn YC nhưng phiếu không được lưu.
- Công ty của **người tạo** hàng tạm (`employee_infos.company_id`): 1 có 1.563 · 4 có 390 · 3 có 3 · 2 có 1. Trong 6 tháng: công ty 1 có 797, công ty 4 có 201, công ty 3 có 3.
- Người tạo: 63 nhân viên. Phòng tạo phiếu nhiều nhất: Phòng Dự án (238), Ô tô 2 (61), KD KV4 (61).
- Người duyệt: 10 người. 6 người duyệt nhiều nhất chiếm 1.783/1.929.
- Thời gian từ lúc tạo tới lúc duyệt: trung bình **33 giờ**.

### 2.2 Hàng hoá sinh từ hàng tạm

| Đo | Kết quả |
|---|---|
| `products.tmp_product_id` khác NULL/0 | 8.931 / 45.890 dòng, 4.949 giá trị khác nhau, **2.706 giá trị trùng ≥ 2 dòng** |
| Trong đó tạo trước 02/08/2025 (trỏ vào bảng hàng tạm cũ đã bị xoá) | **7.057**. Có 3.806 dòng trỏ vào id không còn tồn tại; số còn lại trỏ **nhầm** vào hàng tạm mới cùng id |
| Liên kết thật (`p.created_at >= t.created_at`) | **1.874**, 1–1 với 1.874 hàng tạm `status=1`. Hàng tạm đã duyệt mà không có product: 0 |
| `products.status` của 1.874 hàng này | 1 (hoạt động): 1.806 · 0: 67 · 5: 1 |
| `products.company_id` | 1: 1.531 · 4: 343. **Bằng `manufactures.company_id` 1.874/1.874.** So với công ty người tạo: 1.850 trùng, **24 lệch** |
| `pcc` (`product_company_coefficients`) | trung bình 3,85 dòng/hàng. Công ty 1–4 mỗi công ty có 1.806 dòng `status=3`. Phần lớn do backfill G-phase và do form duyệt gửi `company_coefficients` |
| `product_company_units` / `product_unit_prices` | có cho công ty 1–4 (1.873 / 1.806 / 1.806 / 1.807 hàng), cũng do backfill |
| Hàng sinh từ hàng tạm đã từng vào YCHG | 157 hàng (221 dòng `price_asking_request_products`) |
| `product_approves` sinh từ đường duyệt hàng tạm | 0. Bảng `product_approves` đang rỗng; mọi công ty 1–7 có `is_new_company = 0` nên nhánh "chờ duyệt giá" không chạy |

> ⚠️ **Đừng nối `products.tmp_product_id = tmp_products.id` trần.** Phải kèm `p.created_at >= t.created_at`, hoặc chỉ lấy `t.status = 1` và product mới nhất. Comment `TmpProductRequestSyncService.php:161-162` đã nêu lỗi này. HRM `ProductProjectController::filterOutNativeErp` (`:113-125`) đang dùng `tmp_product_id != null` làm dấu "hàng gốc từ hàng tạm", nên 7.057 hàng cũ cũng bị tính là "từ hàng tạm".

---

## 3. Vòng đời

### 3.1 Trạng thái `tmp_products.status` (`TmpProduct.php:11-15`)

```
                 (HRM sync, chưa dùng)                 
                  3 Đang tạo ──Lưu và gửi duyệt──┐     
                    │  ▲ Lưu nháp                │     
ERP popup ──store──►2 Chờ duyệt ◄─────gửi lại────┤     
                    │      │                     │     
             approve│      │reject               │     
                    ▼      ▼                     │     
              1 Đã duyệt  0 Không duyệt ─────────┘ (updateDraft submit=1, chỉ người tạo)
                    │                                   
               (sinh products)      delete: status 0/2/3 ⇒ -1 Đã xoá (chặn khi =1)
```

### 3.2 Tạo hàng tạm: `store` (`TmpProductsController.php:250-535`)

- **Gọi từ đâu**: partial `partials/tmpProduct/createTmpProductJs.blade.php:98` (`route('tmpProductStore')`) kèm form `createTmpProductForm.blade.php`. Có 3 nơi include partial này:
  1. **Phiếu YC duyệt hàng tạm**: `sale/tmp_product_requests/form.blade.php:68` + `formJs.blade.php:7`. Đây là đường chính, 1.804/1.957 hàng tạm có phiếu.
  2. **Báo giá ERP cũ**: `quotations/form.blade.php:720`, `create.blade.php:150`, `edit.blade.php:114`. `quotation_products` chỉ có 155 dòng và `tmp_product_id` = 0 ⇒ coi như không dùng.
  3. **Báo giá dự án ERP**: `sale/project_quotations/form_template.blade.php:701` chỉ include form, không include JS. `project_quotation_*_products.tmp_product_id` = 0 dòng.
- Quyền: chỉ middleware `Thêm báo giá`. Không lọc công ty.
- Validate (`:251-301`): tên **unique theo model** ở cả `tmp_products` lẫn `products` (`:252-259`); bắt buộc model, nhóm, hãng, thương hiệu, xuất xứ, ảnh đại diện, VAT, loại SP, `product_cate`, ≥ 1 ĐVT, đúng 1 ĐVT cơ bản (`:389-406`), mỗi ĐVT phải có `prices[]`.
- Ghi: `tmp_products` (status 2), suppliers, barcodes, videos, thuộc tính, gallery, ĐVT, giá (`:408-490`).
- **Thông báo** (`:492-520`): gửi cho **mọi Super Admin + mọi NV có quyền `Duyệt hàng tạm`**, không lọc công ty. Link `tmpProductEdit`. Kèm `Redis::publish("tmp_product")`. Người phụ trách hãng không có quyền thì **không** được báo.

### 3.3 Phiếu YC duyệt hàng tạm (`tmp_product_requests`)

- Quan hệ: **1 phiếu – n hàng tạm** qua `tmp_products.tmp_product_request_id` (`TmpProductRequest::products :54-56`). Thứ tự: tạo từng hàng tạm bằng popup (mỗi lần gọi `store`), rồi `TmpProductRequestController@store` (`:93-127`) tạo phiếu, gắn các id (`syncProducts :150-156`) và gọi `send()`.
- `send()` (`TmpProductRequest.php:170-172`): thông báo cho mọi NV có quyền `Duyệt hàng tạm` (không lọc công ty), link `TmpProductRequest.show`. Vì vậy **mỗi hàng tạm sinh 2 đợt thông báo** (1 lần ở `store` từng hàng + 1 lần cho phiếu).
- `company_id` / `department_id` của phiếu = công ty / phòng người lập (`boot :18-25`).
- Trạng thái phiếu **tính từ hàng con** (`:178-204`): 4 Đang tạo (tất cả con là nháp) · 2 Đang xử lý · 3 Chờ xử lý · 1 Hoàn thành.
- Danh sách `type=all` lọc theo 3 quyền xem (tổng công ty / công ty / phòng ban), mặc định thấy phiếu mình tạo (`:74-98`). `type=approve` cần `Duyệt hàng tạm` và chỉ thấy phiếu của **công ty mình** (`:99-104`). Điều kiện whereHas ở `:88-98`, `:100-103` so `tmp_products.status` với hằng số **của phiếu** (`CHO_XU_LY=3`, `HOAN_THANH=1`…) và dùng `!= 1 OR != 2` (luôn đúng) ⇒ lọc gần như vô tác dụng.
- In: `ReportTemplate::YC_DUYET_HANG_TAM` (`:206-224`). `updateNote` chỉ cho sửa khi phiếu Đang tạo.
- Phiếu **không có bước duyệt riêng**: duyệt từng hàng tạm ở màn `tmpProductEdit`.

### 3.4 Duyệt: `approve` (`TmpProductsController.php:538-687`)

1. `canApprove()` (`TmpProduct.php:56-58`): (có quyền `Duyệt hàng tạm` **hoặc** là người phụ trách Thương hiệu–Hãng hiện hành: `assign_histories.brand_employee_id`, `employee_date_to IS NULL`) **và** `status == 2`. **Không kiểm công ty.**
2. Validate bằng **`Product::getRules`** (`app/Product.php:280-411`), tức bộ luật đầy đủ của form hàng hoá: `company_id` bắt buộc, `units.*.cost_price`, `units.*.sale_max_percent_coefficient`, `units.*.prices.*.price/coefficient`, `expected_prices`, `company_coefficients[]`…
3. `checkDueConfigs`: nếu người duyệt có **hàng mượn / hàng giữ / hàng nhập thẳng quá hạn** thì bị chặn duyệt và từ chối (`app/Http/Middleware/CheckDueConfigs.php:121-124, 171-174, 247-250`; `due_configs` id 6, 12, 21 tên "Duyệt hàng tạm").
4. **`Product::createRecord($request, $tmpProduct->id)`** (`app/Product.php:6983-7420`):
   - Tạo `products` với `status = HOAT_DONG (1)`, `company_id = $request->company_id`, `tmp_product_id` (`:6984-7051`), `generateCode()` (`:7053`).
   - `syncCompanyCoefficients($request->company_coefficients)` (`:7065`, thân hàm `:6436-6448`): **xoá rồi tạo lại** `pcc` cho các công ty trong form, cột `status` = NULL.
   - Phụ kiện, phụ tùng, công thức, xe, thuộc tính (bắn event created thủ công), gallery.
   - `$company_id = $product->company_id ?? công ty người duyệt` (`:7132`). Quy chế "công ty mới" `is_new_company/is_new_brand` (`:7133-7150`). Nếu công ty bật quy chế thì `products.status = CHO_DUYET` và giá đi vào nhánh chờ duyệt.
   - Mỗi ĐVT (`:7169-7338`): `product_units` (13 cột giá cũ = 0) + **`product_company_units` của `$company_id`** (giá vốn `cost_price`, `buy_price`, định mức…) + **6 dòng `product_unit_prices` mang `company_id`** (G3 `:7245`). Loại 6 TMĐT tự tính = giá bán lẻ × `config.coefficient_ecommerce_price` (`:7236-7240`). Loại còn thiếu bù dòng giá 0 (`:7328-7337`). Có thêm `product_expected_prices` (giá hiệu lực, `status=2`).
   - Nếu `status = 1` thì `pcc(product, $company_id).status = 3` **Đang kinh doanh** (`:7340-7354`).
   - Nhánh chờ duyệt: `product_approves` + `product_approve_prices` với `company_id = $company_id`, thông báo cho quyền `Duyệt giá hàng hoá` của công ty đó, link **HRM** `price-approve` (G6, `:7412-7416`).
   - `dispatch(CreateTemplateProductMissing)` (`:7418`).
5. Ghi ngược các chỉnh sửa của người duyệt về hàng tạm, rồi xoá và tạo lại ĐVT/giá tạm (`:570-660`); `status=1`, `approver_id`, `comment`.
6. Thông báo cho **người tạo**, link `myTmpProductShow` (`:662-671`). Trang này trả **"Đang phát triển"** ⇒ link chết.

> **Công ty nhận giá**: `company_id` do FE gửi, lấy theo **Hãng SX đang chọn** (`tmp_products/edit.blade.php:93-104`: `$scope.product.company_id = manu.company_id`), ô chọn công ty bị `disabled` (`tmp_products/form.blade.php:1251`). Comment G3 ở `Product.php:7164-7167` ghi "công ty hàng tạm" là **không đúng thực tế**: hàng tạm không có cột công ty, giá vào **công ty quản lý hãng**. Các công ty khác chỉ có dòng `pcc` (status NULL) nếu người duyệt khai ở bảng "Hệ số công ty" (`form.blade.php:894-929`).

### 3.5 Từ chối / Lưu nháp / Xoá

| Hành động | Code | Làm gì | Thông báo |
|---|---|---|---|
| `reject` | `:690-742` | Bắt buộc `comment` (≤ 255). Chỉ khi `status=2` thì đặt `status=0`, `approver_id`, `comment`. **Không gọi `canApprove()`**, route không gắn quyền ⇒ NV nào đã đăng nhập cũng từ chối được (fail-open) | Người tạo, link `tmpProductEdit` |
| `updateDraft` | `:746-896` | Chỉ **người tạo**, khi `status ∈ {3, 0}`. `submit=1` thì validate bằng `Product::getRules` và chuyển sang 2 (xoá lý do + người duyệt cũ nếu trước đó bị từ chối). `submit=0` chỉ cần tên và giữ 3. Ghi đè toàn bộ field + quan hệ | `submit=1`: `sendNotifyWithPermission('Duyệt hàng tạm')`, link `tmpProductEdit` |
| `delete` | `:899-927` | Chặn khi `status=1`, ngược lại đặt `-1`. **Không gọi `canDelete()`**, route GET, không quyền ⇒ fail-open. Nút xoá trên danh sách thì có kiểm `canDelete()` (`:161`) | Người tạo, link `myTmpProductShow` (link chết) |

### 3.6 Màn danh sách / quyền xem

- `searchByFilter` (`TmpProduct.php:176-246`): người có `Xem danh sách hàng tạm` hoặc `Duyệt hàng tạm` thấy **tất cả công ty**. Người khác thấy hàng tạm theo **phân công thương hiệu × hãng** của mình (`AssignHistory::getAssignByEmployee`), cộng thêm hàng mình tạo.
- Nút trên dòng (`TmpProductsController.php:147-165`): Sửa (nháp của mình) · Xem (`canView`) · Duyệt (`canApprove`) · "Sửa và gửi duyệt lại" (status 0 của mình) · Xoá (`canDelete`). Các nút Sửa/Xem/Duyệt đều trỏ cùng `tmpProductEdit`.
- `canView()` chỉ kiểm quyền `Xem danh sách hàng tạm`; route `edit` thì **không kiểm quyền**.
- Dashboard: `HomeController.php:551-575` đếm hàng tạm `status=2` (theo quyền hoặc phân công) thành thẻ "Hàng tạm cần duyệt".

### 3.7 Đường vào từ HRM (đã có code, chưa có dữ liệu)

- HRM `Modules/Assign/Services/TmpProductSyncService.php`: `sendApproval` (`:21-86`) gửi các dòng hàng tạm của báo giá dự án **Trúng thầu** sang `sync-from-hrm` (giá đã quy về VND theo tỉ giá), nhận lại map `hrm_line_id → tmp_product_id`, ghi `quotation_product_prices.erp_tmp_product_id`, `quotations.erp_tmp_product_request_id/code`. `pullStatus` (`:92-140`) kéo `approved-status` và ghi `erp_product_id` cho dòng đã duyệt. Route HRM: `Modules/Assign/Routes/api.php:678-679, 816-821`. FE: `ProspectiveProjectQuotationsTab.vue:671-705`.
- ERP `TmpProductRequestSyncService::createFromHrm` (`app/Services/Sale/TmpProductRequestSyncService.php:58-147`): `Auth::login($employee)` theo `auth_id`, tạo hàng tạm **status 3 Đang tạo**, 1 ĐVT, giá **mọi loại giá**: bán lẻ = giá báo giá, hệ số = giá bán / giá nhập; loại khác = 1. Tạo phiếu (lưu `hrm_quotation_*`), **không** gửi thông báo.
- HRM `Modules/Assign/Services/QuotationErpSyncService.php:105-127` (đồng bộ báo giá sang `firm_quotations` ERP): **INSERT thẳng `tmp_products`** (status 2, thiếu `created_by` / `product_cate` / `vat_percent` NOT NULL, không có ĐVT). `firm_quotation_*_products.tmp_product_id` = 0 dòng.
- HRM menu đã có mục "Danh sách hàng tạm" (`hrm-client/components/menu-sidebar.js:34-35` → `/assign/product-project`). Đây là **hàng hoá dự án của HRM**, khái niệm khác `tmp_products` ERP nhưng **trùng tên**. Hub Bán hàng có nhãn trơn `'YC duyệt hàng tạm'` (`components/subsystem-menu/sale-hub.js:164`, chưa có link).
- DB: `quotations.tmp_sync_status` NULL cả 206 dòng; `quotation_product_prices.erp_tmp_product_id` = 0 / 6.288; `tmp_product_requests.hrm_quotation_id` = 0 ⇒ **chưa từng chạy** trên dữ liệu này.

---

## 4. Hàng tạm được đọc ở đâu ngoài màn của nó

Đếm bằng grep `tmp_product|TmpProduct` (đã bỏ false positive kho `tmp_*`): **87 file PHP trong `app/`**, **50 file view**. Phân nhóm:

| Nhóm | File (ví dụ, `file:dòng`) | Dữ liệu thật |
|---|---|---|
| **Chứng từ có cột `tmp_product_id`** (16 cột, 16 bảng) | báo giá cũ `quotation_products`; báo giá/HĐ/phân tích dự án `project_quotation_{tab,group}_products`, `project_contract_*`, `project_analysis_*`; báo giá/HĐ hãng `firm_quotation_{tab,group}_products`, `firm_quotation_promotions`, `firm_contract_promotions`, `contract_promotions`; `product_infos`; HRM `quotation_product_prices.erp_tmp_product_id`, `hrm_contract_product_prices.erp_tmp_product_id`, `quotations.erp_tmp_product_request_id/code` | **Tất cả = 0 dòng**, trừ `products.tmp_product_id` |
| Model/Service đọc hàng tạm trong chứng từ | `ProjectQuotationGroup.php:31,61-62` · `ProjectQuotationTab.php:54,88-89` · `ProjectAnalysisGroup.php:44,74-75` · `FirmQuotationService.php:62-108,412,537-666` · `ProjectQuotationController.php:701-742` · `Quotation.php:1032` · 10 quan hệ `belongsTo(TmpProduct)` | Code còn sống, dữ liệu 0 |
| FormRequest chấp nhận `tmp_product_id` (`exists:tmp_products,id`) | 9 file: `CreateFirmQuotationRequest`, `ApiCreate/ApiUpdate/UpdateFirmQuotationRequest`, `Create/UpdateProjectQuotationRequest`, `SyncFirmQuotationFromHrmRequest:64`, `PrincipleOrder*` (4 file) | |
| Báo giá cũ ERP | `QuotationsController.php:154,199,963-965` · `QuotationAllController.php:130,170` · `ContractsController.php:2161-2163` · `LiquidationContractsController.php:434-438` (`has_tmp_product` chặn lập HĐ) | 0 |
| Báo cáo | `Product::revenueReport :1448`, `topSaleReport :1509`, `:1580-1587` (join `quotation_products.tmp_product_id`) · `CustomerCareReportService.php:163` · `FirmQuotationPrint.php:1635` | join trên cột 0 dòng |
| Danh mục kiểm "đang dùng" trước khi xoá | `Brand.php:138`, `Manufacture.php:202`, `Origin.php:123`, `Group.php:154`, `ProductModel.php:130`, `Barcode.php:21` (+ 8 file `ProductInfo/PI*`) | ⚠️ HRM MasterData (danh mục đã chuyển ở Phase 0/1) **không kiểm `tmp_products`** |
| Hàng hoá | `ProductsController.php:342,491` · `Product2Controller.php:221` nút "Xem sản phẩm gốc" → `tmpProductShow` (**link chết**) · `CreateProductService.php:57`, `SyncProductInfoService.php:68` gán `tmp_product_id = null` khi copy | |
| Dashboard / menu | `HomeController.php:551-575` · `topmenubar.blade.php:20` (Danh mục › Danh mục hàng tạm), `:326` (Phiếu YC duyệt hàng tạm), `:1530-1532` và `:2228-2229` (Mua hàng › Hàng tạm - Hỏi giá, gate `Duyệt hàng tạm`), `:2379-2381` · `topheader.blade.php:171` (Hàng tạm của tôi) | |
| API cho HRM | `Api/TmpProductRequestSyncController` · `TmpProductRequestSyncService` · `SyncTmpProductRequestFromHrmRequest` | |
| Ghi log / chặn | `ProductWriteAuditObserver.php:32` (whitelist `tmpProductApprove`) · `CheckDueConfigs.php:121-124,171-174,247-250` | |
| Cron / Job / Listener | grep `app/Console`, `app/Jobs`, `app/Listeners`, `app/Events`, `app/Notifications`: **0 file**. Chỉ có `createRecord` dispatch `CreateTemplateProductMissing` | |

HRM (đối chiếu): `Modules/MasterData/Entities/Product/Product.php:161` (fillable `tmp_product_id`) · `Modules/Assign/*` (5 file nêu ở §3.7, `ProductProjectController.php:113-223` vẫn đọc `mysql2.products`, cần gắn mốc @TODO-GOPDB).

---

## 5. Quyền

Bảng `permissions` của DB gộp: guard `web` = quyền ERP (966 quyền, id 100001–101049); guard `api` = HRM (817, id 2–1678). Gán quyền qua `role_has_permissions` (có `company_id`) và `employee_has_roles`. `employee_has_permissions` = 0 cho cả 7 quyền dưới đây.

| id | Tên (guard `web`) | Dùng ở | Role | NV qua role (tổng / `employees.status=1`) |
|---|---|---|---|---|
| 100037 | **Duyệt hàng tạm** | `canApprove/canDelete`, `searchByFilter`, nhận thông báo, danh sách phiếu `type=approve`, gate menu | 18 (23 dòng) | 73 / **60** |
| 100038 | **Thêm báo giá** | middleware route `tmpProductStore` | 37 (59 dòng) | 915 / **460** |
| 100981 | Xem danh sách hàng tạm | `canView`, `searchByFilter` | 3 | 2 / 2 |
| 100932 | Xem yêu cầu duyệt hàng tạm theo tổng công ty | danh sách phiếu | 2 | 5 / 5 |
| 100933 | Xem yêu cầu duyệt hàng tạm theo công ty | | **0** | 0 |
| 100934 | Xem yêu cầu duyệt hàng tạm theo phòng ban | | 2 | 2 / 2 |
| 100983 | Duyệt giá hàng hoá | nhánh chờ duyệt giá trong `createRecord` | 6 | 29 / 25 |

Ngoài quyền: **phân công phụ trách Thương hiệu–Hãng** (`assign_histories.brand_employee_id`, `employee_date_to IS NULL`): 678 dòng, **21 NV** được duyệt/xoá hàng tạm đúng hãng mình phụ trách. Super Admin nhận thông báo `store` theo **role** (`Employee::role('Super Admin')`, `:492`). Theo memory "super admin không mặc định có quyền", HRM không được bê cách này sang.

HRM đã có (guard `api`): 1652 Xây dựng thông tin hàng hoá · 1653 Xem dữ liệu hàng hoá công ty · 1657 Cập nhật giá bán · 1658 Duyệt giá bán · 1662 PTKD duyệt YCHG · 1663 XNK xử lý YCHG · 1664 Tính giá bán. **Chưa có quyền nào cho hàng tạm.**

---

## 6. Chỗ G3 / G6 / 2-D1 đã đụng tới hàng tạm

| Đợt | Commit | Thay đổi |
|---|---|---|
| G3 | `3d07fadece` "đường ghi: PTG, duyệt hàng tạm…" · `1d033d38f9` (nhánh chờ duyệt gán 0 tường minh) | `createRecord` ghi `product_company_units` + 6 dòng `product_unit_prices` có `company_id` + `pcc` status 3 cho `$company_id` (`Product.php:7164-7354`). Mốc **`@TODO-PHASE6`** duy nhất: `Product.php:7167` ("luật chính thức chốt ở Phase 6 (P9)") |
| G6 | `02568c4fc8` | Đích thông báo duyệt giá đổi sang HRM `price-approve` (`Product.php:7414`). Route hàng tạm **không** gắn `productMovedToHrm` |
| 2-D1 | — | `ProductWriteAuditObserver.php:31-32` whitelist `tmpProductApprove` (ghi hàng hoá từ route này không ghi log) |
| Lịch sử gần | `04efffe32d` API nhận hàng tạm từ HRM · `1930881cba` trạng thái Đang tạo · `06945cf769` (08/06) · `cd22d73205` (01/07) · `4ba2791844` (08/10, Tri Lee "fix lỗi", 11 dòng) | Luồng còn đang được sửa song song ở nhánh ERP chính ⇒ khi chặn ở ERP phải rebase |

Sau G3, giá duyệt hàng tạm vào **`products.company_id` = công ty quản lý Hãng SX** (§3.4), không phải công ty người tạo hay công ty người duyệt. Sổ `gia-theo-cong-ty/ton.md:31` (P9) ghi "hàng tạm ⇒ công ty của hàng tạm", nhưng hàng tạm **không có cột công ty**. Mệnh đề này cần chốt lại (xem H3).

Rủi ro DB dev đã ghi ở `gia-theo-cong-ty/design.md:401` (R-e): sau M3 (NOT NULL) nếu sót cột thì `createRecord` lỗi. G3 đã gán đủ, nên hiện tại chạy được.

---

## 7. Đối chiếu mô hình mới: chỗ vướng khi chuyển sang HRM

| # | Vướng | Chi tiết | Mức |
|---|---|---|---|
| V1 | **Duyệt hàng tạm = tạo hàng + đặt giá ngay, bỏ qua luồng tính giá** | Người duyệt nhập giá vốn, 6 giá bán, hệ số, giá hiệu lực trên form duyệt, rồi hàng ra **Đang kinh doanh** (`pcc=3`) tức thì. Trái §29a-1 "MỌI hàng đều qua chứng từ tính giá" và `luong-tinh-gia/design.md` mục 1 "MỌI hàng qua YCHG". Hàng tạm hiện chiếm ~19% hàng mới, ~150 hàng/tháng | 🔴 |
| V2 | **Công ty của hàng** | ERP: hàng thuộc **công ty quản lý hãng** (lấy theo hãng, khoá ô). HRM `ProductWriteService::store` (`:78-86`): hàng thuộc **công ty đang làm việc** của người tạo, `pcc` = 1 Đang nhập thông tin. Luồng tính giá HRM: cả luồng thuộc **công ty phiếu**. 24/1.874 ca người tạo khác công ty quản lý hãng | 🔴 |
| V3 | **Người tạo không nhập giá bán** | `tmp_product_unit_prices` 10.919 dòng đều 0; chỉ `cost_price` > 0 (giá vốn dự kiến của sale). Bảng giá ở form tạo đã bị comment. Nếu hàng tạm đi vào YCHG thì "giá vốn dự kiến" chỉ còn là số tham khảo, không có chỗ chứa trong YCHG | 🟡 |
| V4 | **Form duyệt = form hàng hoá đầy đủ** | Validate bằng `Product::getRules`. HRM đã tách form hàng hoá thành 6 tab thông tin, bỏ tab Giá bán (§29g). Màn duyệt hàng tạm HRM phải dùng lại form hàng hoá HRM (bước "Nhập thông tin"), không port form ERP | 🟡 |
| V5 | **2 cửa vào hàng tạm** | (a) Sale tạo ở màn Phiếu YC duyệt hàng tạm ERP (đang chạy). (b) HRM báo giá dự án Trúng thầu đẩy qua API (code có, chưa dùng). Chuyển sang HRM thì (b) có thể ghi thẳng bảng, bỏ HTTP. Riêng `QuotationErpSyncService::createTmpProducts` INSERT trần thiếu cột NOT NULL | 🟡 |
| V6 | **Phân quyền duyệt theo phân công hãng không lọc công ty** | `canApprove` = quyền OR phân công `brand_employee_id`, không xét công ty. Luồng tính giá HRM D3 dùng phân công `buy_employee_id` theo (thương hiệu × hãng × **công ty phiếu**) | 🟡 |
| V7 | **`checkDueConfigs`** | Duyệt hàng tạm bị chặn khi người duyệt có hàng mượn/giữ/nhập thẳng quá hạn. HRM chưa có cơ chế tương đương ở module MasterData | 🟢 hỏi |
| V8 | **Lỗi sẵn có** | `reject`/`delete` fail-open (không kiểm quyền); `edit` không kiểm quyền; Excel/CSV xuất toàn bộ không lọc; 3 link chết (`tmpProductShow`, `myTmpProductShow` ở 2 thông báo + nút "Xem sản phẩm gốc"); lọc phiếu `type=all/approve` so sai hằng số; thông báo không lọc công ty và gửi 2 lần (từng hàng + phiếu) | ghi nhận, port thì sửa |
| V9 | **`products.tmp_product_id` bẩn** | 7.057 dòng trỏ vào bảng hàng tạm cũ, 2.706 giá trị trùng. Mọi chỗ HRM hiện "hàng gốc từ hàng tạm" phải kèm điều kiện thời gian / `t.status=1` | 🟡 |
| V10 | **Chặn ERP** | Sau khi chuyển, ERP phải chặn 7 route ghi (`store`, `approve`, `reject`, `draft`, `delete`, `TmpProductRequest.store/updateNote`) + 2 API sync + menu/dashboard → HRM (khuôn `productMovedToHrm` như G6/T7). `createRecord` ở ERP sẽ không còn đường gọi nào: `productStore` đã chặn ở 2-D1, chỉ còn hàng tạm | 🟡 |
| V11 | **Bảng con không dùng** | `tmp_product_prices`, `galleries`, `barcodes`, `categories` = 0; `videos` 2; `suppliers` 38. Mỗi hàng tạm luôn 1 ĐVT | 🟢 |
| V12 | **Danh mục HRM xoá không kiểm hàng tạm** | ERP chặn xoá Brand/Hãng/Xuất xứ/Nhóm/Model/Barcode đang có hàng tạm; HRM MasterData không đếm `tmp_products` ⇒ có thể xoá danh mục đang được hàng tạm dùng | 🟢 note ngoài luồng |

**Có xung đột không?** Có, ở V1 + V2. Nếu giữ nguyên như ERP thì hàng tạm là **cửa thứ hai tạo giá** (tạo hàng Đang kinh doanh có giá mà không qua YCHG/YCTG/PTG, không qua duyệt giá G5 vì không công ty nào bật `is_new_company`). Nó cũng đặt hàng vào công ty quản lý hãng thay vì công ty người tạo. Phương án khớp mô hình mới: duyệt hàng tạm **chỉ tạo hàng ở trạng thái 1 Đang nhập thông tin** (hoặc 2 Chờ tính giá) tại một công ty xác định, rồi đi tiếp YCHG như mọi hàng (xem H1–H3).

---

## 8. Câu hỏi tồn (cho user chốt)

> Mỗi câu kèm ⭐ đề xuất và hệ quả từng phương án. Theo memory "hỏi hết tồn trước khi code": hỏi lần lượt từng câu.

**H1. Duyệt hàng tạm xong thì hàng ra trạng thái gì, có còn tự đặt giá không?**
- ⭐ (a) **Không đặt giá**: duyệt chỉ tạo mã hàng, hàng ra `pcc = 2 Chờ tính giá` (đủ thông tin, sẵn sàng vào YCHG). Người duyệt không nhập giá. Hệ quả: khớp §29a-1; sale phải chờ thêm 1 vòng YCHG→PTG (ERP hiện chờ duyệt TB 33 giờ, PTG thêm vài ngày) mới bán được. Cần cách cho hàng tạm "đi tiếp" vào YCHG (xem H4).
- (b) Ra `pcc = 1 Đang nhập thông tin`. Hệ quả: người phụ trách phải bổ sung thông tin rồi mới tự lập YCHG; thêm 1 bước tay.
- (c) Giữ như ERP: người duyệt nhập giá, hàng ra Đang kinh doanh. Hệ quả: mở cửa thứ hai tạo giá, trái §29a-1; phải port lại form giá đã gỡ ở §29g.

**H2. Duyệt hàng tạm có gộp vào luồng tính giá luôn không?**
- ⭐ (a) **Duyệt hàng tạm là bước riêng, xong tự sinh (hoặc gợi ý sinh) 1 YCHG** cho hàng đó tại công ty hàng. Hệ quả: 2 chứng từ nối nhau; cần quy tắc ai là người lập YCHG (người tạo hàng tạm?).
- (b) Bỏ hẳn "duyệt hàng tạm": sale tạo thẳng hàng Đang nhập thông tin ở HRM (màn hàng hoá) rồi lập YCHG. Hệ quả: gọn nhất, nhưng sale (460 NV có `Thêm báo giá`) phải được quyền tạo hàng hoá (hiện 1652 chỉ cấp cho người xây dựng hàng), dễ trùng hàng, mất bước kiểm của người phụ trách hãng.
- (c) Giữ duyệt hàng tạm độc lập, không nối gì; người phụ trách tự lập YCHG sau. Hệ quả: dễ quên, hàng treo ở 1/2.

**H3. Hàng sinh từ hàng tạm thuộc công ty nào?**
- ⭐ (a) **Công ty quản lý Hãng SX** (giữ đúng ERP đang chạy, 1.874/1.874). Hệ quả: hàng đúng "chủ" theo hãng. Nếu sale ở công ty khác thì công ty sale phải "lấy hàng về" (luồng §29) mới bán được.
- (b) Công ty của người tạo hàng tạm (= công ty phiếu YC). Hệ quả: khớp HRM `ProductWriteService` (công ty đang làm việc) và luồng tính giá (công ty phiếu). 24 ca/13 tháng hàng sẽ thuộc công ty không quản lý hãng ⇒ `products.company_id` khác quy ước hiện có.
- (c) Người duyệt chọn. Hệ quả: linh hoạt nhưng không có luật.
- Kèm: sổ P9 ghi "công ty của hàng tạm" cần sửa theo đáp án.

**H4. Hàng tạm có cần cột `company_id` không?** (thay đổi schema = ngoại lệ, tiền đề 1)
- ⭐ (a) **Không thêm cột**; công ty suy từ phiếu YC (`tmp_product_requests.company_id`) hoặc từ hãng (theo H3). Hệ quả: không đổi CSDL; 153 hàng tạm không phiếu thì suy theo công ty người tạo.
- (b) Thêm `tmp_products.company_id` + backfill. Hệ quả: lọc/ phân quyền theo công ty gọn, nhưng là thay đổi schema phải duyệt riêng.

**H5. Ai được duyệt hàng tạm ở HRM?**
- ⭐ (a) **Quyền mới "Duyệt hàng tạm" (guard api) trong công ty hàng** + giữ đường người phụ trách hãng (`assign_histories`) **lọc theo công ty**. Hệ quả: phải tạo quyền mới, gán lại cho 18 role / 60 NV đang có quyền ERP 100037; nên dùng `buy_employee_id` hay `brand_employee_id`? (ERP dùng `brand_employee_id`, luồng tính giá dùng `buy_employee_id`).
- (b) Chỉ theo quyền, bỏ phân công. Hệ quả: 21 NV phụ trách hãng không có quyền sẽ mất khả năng duyệt.
- (c) Dùng lại quyền 1652 "Xây dựng thông tin hàng hoá". Hệ quả: không thêm quyền, nhưng gộp 2 vai.

**H6. Ai được tạo hàng tạm / lập phiếu YC?**
- ⭐ (a) **Quyền mới "Thêm hàng tạm"**, thay cho "Thêm báo giá" đang mượn. Hệ quả: rõ nghĩa, phải gán lại.
- (b) Dùng quyền "Thêm báo giá" phía HRM (nếu có tên tương ứng). Hệ quả: giữ diện người dùng (460 NV) nhưng mượn quyền khác nghĩa như ERP.

**H7. Giữ "Phiếu YC duyệt hàng tạm" (1 phiếu – n hàng) hay chỉ còn danh sách hàng tạm?**
- ⭐ (a) **Giữ phiếu** (579 phiếu, 3,1 hàng/phiếu; có in; HRM báo giá dự án cũng sinh phiếu). Hệ quả: port 2 màn (danh sách phiếu + chi tiết/in) + màn danh mục hàng tạm.
- (b) Bỏ phiếu, chỉ còn danh mục hàng tạm có cột "nguồn". Hệ quả: ít màn hơn, mất bản in và nhóm theo đợt gửi.

**H8. Đường HRM báo giá dự án → hàng tạm** (`TmpProductSyncService`, đang gọi API ERP)
- ⭐ (a) **Chuyển thành gọi service nội bộ HRM** (ghi thẳng bảng), giữ đúng hành vi: nháp "Đang tạo", giá bán lẻ từ báo giá. Bỏ 2 API ERP. Hệ quả: phải sửa module Assign (ngoài MasterData). `QuotationErpSyncService::createTmpProducts` (INSERT trần) sửa cùng hoặc ghi ngoài luồng.
- (b) Giữ API ERP tới khi ERP tắt hẳn. Hệ quả: 2 nơi ghi `tmp_products`, trái "ERP chỉ đọc".

**H9. Giá trên hàng tạm (giá vốn dự kiến của sale, giá báo giá từ HRM) dùng vào đâu?**
- ⭐ (a) **Chỉ hiển thị tham khảo** ở màn duyệt và (nếu H2a) ở YCHG/PTG của hàng đó. Hệ quả: không ghi vào bảng giá thật.
- (b) Ghi làm giá vốn ban đầu ở công ty hàng. Hệ quả: lại thành giá không qua tính giá.
- (c) Bỏ ô giá khỏi form hàng tạm. Hệ quả: mất thông tin sale có sẵn.

**H10. Chặn duyệt khi có hàng mượn/giữ/nhập thẳng quá hạn (`checkDueConfigs`) có port không?**
- ⭐ (a) **Không port ở Phase 6**, ghi việc ngoài luồng: cơ chế này áp cho nhiều màn ERP, nên làm chung. Hệ quả: tạm thời HRM không chặn.
- (b) Port riêng cho hàng tạm. Hệ quả: thêm phụ thuộc sang module kho.

**H11. Dữ liệu cũ**
- ⭐ (a) **Giữ nguyên 1.957 hàng tạm + 579 phiếu**, đọc thẳng (tiền đề 1). Hàng tạm `status=2` (1 hàng) duyệt theo luật mới. Hàng `0`/`-1` chỉ xem. Hệ quả: không di trú.
- Kèm: có xử lý 7.057 `products.tmp_product_id` trỏ bảng cũ không? ⭐ Không sửa dữ liệu; mọi truy vấn HRM nối theo điều kiện thời gian hoặc `t.status=1` và product mới nhất.

**H12. Thông báo**
- ⭐ (a) Theo `notification-convention`: tạo/gửi duyệt ⇒ người có quyền duyệt **trong công ty hàng** + người phụ trách hãng; duyệt/từ chối ⇒ người tạo; **1 thông báo/phiếu**, không gửi theo từng hàng. Không gửi theo role Super Admin. Hệ quả: khác ERP (ERP gửi toàn hệ thống, 2 lần).

**H13. Lỗi sẵn có ở ERP (V8) có sửa ngay trên ERP không?**
- ⭐ (a) **Không sửa ERP**, vì sẽ chặn cả luồng ở ERP. HRM viết mới đúng quyền. Ghi vào danh sách ngoài luồng. Hệ quả: tới ngày lên prod ERP vẫn fail-open.
- (b) Vá ERP trước. Hệ quả: thêm việc trên nhánh ERP đang có người khác sửa (`4ba2791844` 08/10).
