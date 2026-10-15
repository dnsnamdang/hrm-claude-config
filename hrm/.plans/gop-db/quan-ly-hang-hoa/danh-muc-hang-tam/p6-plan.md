# Phase 6 — Hàng tạm (quản lý mới trên HRM) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans. Các bước dùng checkbox `- [ ]`.
> ✅ **User cho "LÀM" 12/10/2026** — đúng phạm vi mục cuối (kể cả popup dùng chung `QuotationProductSearchModal.vue`). Cách làm: subagent-driven, từng task + review.

**Goal:** Sale tạo hàng tạm ngay trong YCHG (dùng lại popup "Thêm hàng tạm" của BOM/Báo giá); PTKD duyệt từng hàng tạm (Đồng ý / Không duyệt) bằng form giống form tạo hàng hoá + tab Quản trị; duyệt phiếu đưa hàng đã đồng ý vào luồng tính giá Phase 7; ERP chặn luồng hàng tạm cũ.

**Architecture:** Hàng tạm = hàng hoá thật (`products` + bảng con) có mã chính thức ngay khi lưu, trạng thái theo công ty mới ở `product_company_coefficients.status`: **6 Hàng tạm · 7 Hàng tạm đã duyệt · 8 Hàng tạm không duyệt**. Không bảng mới, không migration, không quyền mới. YCHG / YCTG / PTG giữ nguyên schema; chỉ thêm luật chuyển trạng thái quanh `PriceAskingRequestWriter`.

**Tech Stack:** hrm-api Laravel (PHP 7.4, module `MasterData` + `Assign`), hrm-client Nuxt 2 (Vue 2, node 12), ERP Laravel 6 (Blade). PHPUnit, Playwright (e2e + MCP đo DOM).

**Spec:** `danh-muc-hang-tam/design.md` (D1–D10, §8 M-Q1–M-Q5, §9 A1–A13, §10 C1–C8) · mockup DUYỆT `mockup-hang-tam.html` + `mockup-ghi-chu.md` · điểm chạm `diem-cham-code.md`.

## Global Constraints
- Nhánh: hrm-api + hrm-client `feat/p6-hang-tam` từ nhánh chung `feat/chuyen-doi-hang-hoa` (worktree `wt-chuyen-doi-hang-hoa`); ERP `feat/p6-chan-hang-tam` từ `feat/2d1-erp-khong-loi` (worktree `wt-erp-2d1`). Merge LOCAL, push khi user cho. ⛔ không đụng `gop_db`.
- DB dev `hrm_erp_giacty`: KHÔNG migration / seeder / `PermissionsTableSeeder`; chỉ dữ liệu thử khi kiểm rồi dọn; e2e / Playwright được cấp role tạm (gỡ + `cache:clear` khi xong).
- Mã trạng thái: `STATUS_TEMP = 6` "Hàng tạm" `#6D5A9E` · `STATUS_TEMP_APPROVED = 7` "Hàng tạm đã duyệt" `#7C3AED` · `STATUS_TEMP_REJECTED = 8` "Hàng tạm không duyệt" `#DC2626`; `TEMP_STATUSES = [6, 7, 8]`.
- Phân loại hàng tạm bắt buộc đủ 5 ô (Tính chất · Nhóm chức năng · Nhóm SP suy từ Loại SP; Loại SP; **Đặc tính**). Tiểu mục catalog KHÔNG bắt buộc với hàng tạm.
- Super admin không bypass quyền; gate theo đúng permission + công ty (`PermissionService`).
- Nhãn nút form duyệt: **Lưu · Đồng ý · Không duyệt · Hủy**; lý do Không duyệt bắt buộc ≤ 255.
- Lỗi form báo đồng thời mọi ô; tiêu đề cột 1 dòng; form mỗi hàng đủ 12 cột; số `1,234,567`, ngày `dd/mm/yyyy`.
- Popup `QuotationProductSearchModal.vue` dùng chung BOM/Báo giá: chế độ mới bật bằng prop, mặc định = hành vi cũ (không đổi BOM/Báo giá).
- FE xong phải đo DOM bằng Playwright; e2e chỉ chạy khi user bảo (`--no-deps --workers=1`, cổng 3031/8031).

## Review Focus
1. Hàng tạm (6/7/8) lọt vào Kho dữ liệu, màn "Dữ liệu hàng hoá công ty", popup catalog, picker hàng kèm theo (`itemSearch`), CSKH ⇒ phải ẩn — ca test ở Task 1.
2. Sale sửa hàng **7** sau khi PTKD đồng ý ⇒ phải về 6 (PTKD duyệt lại), nếu không PTKD duyệt phiếu trên thông tin đã đổi — ca test ở Task 3.
3. Hai PTKD / PTKD + sale thao tác cùng lúc (duyệt phiếu khi sale vừa thêm hàng tạm mới) ⇒ BE kiểm lại "còn hàng 6" trong transaction có `lockForUpdate` — ca test ở Task 3.
4. Gắn mã cho "mọi dòng cùng gốc" bắt nhầm dòng gõ tay trùng mã HHB ⇒ chỉ gắn dòng `erp_product_id IS NULL` + cùng nguồn — ca test ở Task 2.
5. Xoá hàng tạm đang nằm trong YCHG Nháp / Chờ PTKD duyệt ⇒ phải chặn; phiếu Không duyệt ⇒ xoá mềm — ca test ở Task 4.

---

## Task 1: Nền trạng thái 6/7/8 + ẩn hàng tạm khỏi các màn / popup

**Files:**
- Modify: `hrm-api/Modules/MasterData/Entities/Product/ProductCompany.php:23-47` (hằng, TEXT, COLOR, `TEMP_STATUSES`)
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductService.php:180-216` (`applyScreen`: WAREHOUSE + COMPANY loại 6/7/8; WAREHOUSE còn loại hàng có pcc chủ ∈ 6/7/8 để công ty khác không thấy)
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductService.php:168-172` (others_using_count bỏ 6/7/8)
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductCatalogService.php:140-175` (tab Thêm + `checkProductsAddable` loại 6/7/8)
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductOptionService.php:126-134` (`itemSearch` loại hàng mà pcc công ty hiện tại ∈ 6/7/8)
- Modify: `hrm-api/Modules/CustomerCare/Services/ServiceService.php:997-1004`, `hrm-api/Modules/CustomerCare/Http/Controllers/V1/DeviceErrorController.php:258` (loại hàng mà MỌI dòng pcc NOT NULL đều ∈ 6/7/8)
- Modify: `hrm-client/utils/product-list-screens.js:206-217` (nhãn/màu 6/7/8), `hrm-client/components/product/ProductListPage.vue:329`
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductCompanyFoundationTest.php:58-62` (bất biến tập status thêm 6/7/8), file mới `hrm-api/Modules/MasterData/Tests/Feature/TempProductVisibilityTest.php`

**Interfaces — Produces:** `ProductCompany::STATUS_TEMP|STATUS_TEMP_APPROVED|STATUS_TEMP_REJECTED`, `ProductCompany::TEMP_STATUSES`, `ProductCompany::isTemp(?int $status): bool`.

- [ ] **Step 1 — test đỏ** `TempProductVisibilityTest` (DatabaseTransactions + `ActsAsProductUser`): tạo 3 hàng (công ty A) pcc 6 / 7 / 8 + 1 hàng pcc 1 làm đối chứng; khẳng định:
  - `GET master-data/products/warehouse` (A và B) KHÔNG chứa 3 hàng tạm, CÓ hàng đối chứng (theo luật cũ);
  - `GET master-data/products/company` (A) không chứa hàng tạm; `entering` / `trading` không chứa;
  - catalog `catalogs/products?tab=add` không chứa; `checkProductsAddable([tạm])` trả lỗi;
  - `itemSearch(keyword = tên hàng tạm)` rỗng;
  - `ProductListResource` của hàng 6 (khi đọc qua màn Hàng tạm ở Task 4) trả `status_text = "Hàng tạm"`.
- [ ] **Step 2** — chạy `cd hrm-api && vendor/bin/phpunit --filter TempProductVisibilityTest` ⇒ FAIL.
- [ ] **Step 3** — thêm hằng:
  ```php
  const STATUS_TEMP = 6;          // Hàng tạm — sale tạo trong YCHG, chờ PTKD duyệt (Phase 6)
  const STATUS_TEMP_APPROVED = 7; // Hàng tạm đã duyệt — PTKD Đồng ý, chờ duyệt phiếu
  const STATUS_TEMP_REJECTED = 8; // Hàng tạm không duyệt — nằm lại phiếu, không đi tiếp
  const TEMP_STATUSES = [self::STATUS_TEMP, self::STATUS_TEMP_APPROVED, self::STATUS_TEMP_REJECTED];
  // STATUS_TEXT: 6 'Hàng tạm', 7 'Hàng tạm đã duyệt', 8 'Hàng tạm không duyệt'; STATUS_COLOR: '#6D5A9E', '#7C3AED', '#DC2626'
  public static function isTemp(?int $status): bool { return $status !== null && in_array($status, self::TEMP_STATUSES, true); }
  ```
  rồi sửa từng chỗ lọc theo danh sách Files (dùng `whereNotIn('pcs.status', ProductCompany::TEMP_STATUSES)` kèm `orWhereNull` đúng ngữ nghĩa từng màn; WAREHOUSE thêm `whereNotExists` pcc chủ ∈ TEMP_STATUSES).
- [ ] **Step 4** — chạy test mới + `vendor/bin/phpunit Modules/MasterData` ⇒ PASS (MasterData hiện 397 xanh).
- [ ] **Step 5** — commit `P6 T1: trạng thái hàng tạm 6/7/8 + ẩn khỏi màn hàng hoá, catalog, picker`.

## Task 2: Tạo / sửa hàng tạm (BE) + gắn mã cho dòng tạm BOM / báo giá

**Files:**
- Create: `hrm-api/Modules/MasterData/Http/Requests/Product/TempProductRequest.php` (luật = `ProductRequest` phần thông tin chung, KHÔNG `authorize` 1652, `product_characteristic_id` required, KHÔNG `adminRules`; giữ `checkUniqueName`, `checkUnits`)
- Create: `hrm-api/Modules/MasterData/Services/Product/TempProductService.php`
- Create: `hrm-api/Modules/MasterData/Http/Controllers/V1/Product/TempProductController.php`
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductWriteService.php:71-98, 565-607` (cho `store` nhận trạng thái pcc khởi tạo + `job_cluster_ids` tuỳ chọn: `(array) ($a['job_cluster_ids'] ?? [])`)
- Modify: `hrm-api/Modules/MasterData/Routes/api.php:395-416` (route mới)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/TempProductApiTest.php`

**Interfaces — Produces:**
- `POST master-data/temp-products` body = payload `ProductForm` phần thông tin chung + `source` tuỳ chọn `{type: 'bom'|'quotation', id: int}` ⇒ `{data: {id, code, name, company_status: 6, ...lineRow}}`.
- `PUT master-data/temp-products/{product}` (người tạo hoặc 1652; chỉ khi pcc công ty ∈ 6/7/8) ⇒ 7 hoặc 8 sửa xong về **6**.
- `TempProductService::create(array $data, ?array $source): Product`, `TempProductService::update(Product $p, array $data): Product`, `TempProductService::linkSourceLines(Product $p, string $type, int $lineId): int` (trả số dòng đã gắn).
- Log `price_asking_request_approve_histories` type `temp_created`, note = product_id (C5) — ghi ở Task 3 khi dòng vào phiếu (cần `price_asking_request_id`).

- [ ] **Step 1 — test đỏ** `TempProductApiTest`:
  - người KHÔNG có 1652 tạo được ⇒ 201, `products.code` theo `ProductCodeGenerator`, pcc(công ty hiện tại).status = 6, không có dòng `product_business_catalogs`;
  - thiếu Đặc tính / Loại SP / Hãng SX ⇒ 422 báo đủ các ô cùng lúc;
  - trùng tên × model × thương hiệu × hãng với hàng có sẵn ⇒ 422;
  - `source={type:'bom', id}`: gắn `erp_product_id` cho dòng BOM đó + dòng báo giá có `bom_list_product_id = id` + dòng BOM/báo giá cùng mã HHB **và** `erp_product_id IS NULL`; dòng gõ tay trùng mã nhưng đã có `erp_product_id` khác KHÔNG bị đổi (Review Focus 4);
  - sửa hàng pcc 7 (người tạo) ⇒ pcc về 6; sửa hàng 8 ⇒ về 6; người khác không 1652 sửa ⇒ 403; hàng pcc 2 qua route này ⇒ 422.
- [ ] **Step 2** — chạy `--filter TempProductApiTest` ⇒ FAIL.
- [ ] **Step 3** — cài đặt: `TempProductService::create` gọi `ProductWriteService::store($data, ProductCompany::STATUS_TEMP)` trong transaction; `linkSourceLines` cập nhật `bom_list_products` / `quotation_product_prices` theo luật trên; `update` dùng `ProductWriteService::update` (bỏ `assertOwner` 1652 bằng nhánh riêng cho hàng tạm: chủ = công ty hiện tại + (người tạo `products.created_by` hoặc 1652)) rồi `pcc.status 7|8 ⇒ 6`.
- [ ] **Step 4** — chạy test ⇒ PASS; chạy `ProductWriteApiTest` + `ProductLifecycleApiTest` ⇒ không đổi.
- [ ] **Step 5** — commit `P6 T2: tạo/sửa hàng tạm (không 1652, Đặc tính bắt buộc, catalog tuỳ chọn) + gắn mã dòng tạm BOM/báo giá`.

## Task 3: YCHG — chọn hàng tạm, PTKD duyệt từng hàng, duyệt / không duyệt phiếu

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceAskingProductReader.php:24, 82-96` (cho chọn 6/8 của **công ty phiếu** khi không nằm trong YCHG khác đang mở; 7 không chọn lại; `blockReason` câu riêng)
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceAskingRequestWriter.php`:
  - `save` :63-124 — hàng 6/8 giữ trạng thái khi gửi (chỉ 1→2 như cũ); hàng 8 đưa vào phiếu mới ⇒ về 6; log `temp_created` cho hàng tạm vừa tạo kèm phiếu
  - mới `tempApprove(int $id, int $productId, array $input): void` (gate 1662 công ty phiếu, phiếu =2, hàng ∈ phiếu & pcc 6: validate đủ thông tin (dùng `TempProductRequest` rules) + ghi thông tin chung + ghi tab Quản trị cho **công ty phiếu** qua `ProductWriteService::writeAdmin(..., companyId)` ⇒ pcc 7)
  - mới `tempReject(int $id, int $productId, array $input): void` (lý do bắt buộc ≤255 ⇒ pcc 8 + log `temp_reject` "<mã>: <lý do>")
  - `ptkdApprove` :223-261 — trong transaction `lockForUpdate` pcc hàng của phiếu: còn hàng 6 ⇒ 422 "Còn N hàng tạm chưa duyệt"; 7 ⇒ 2; 8 giữ; nhóm toàn 8 ⇒ đóng nhóm Huỷ duyệt lý do "Mọi hàng tạm không được duyệt" (C6)
  - `ptkdReject` :263-284 — thêm 7 ⇒ 6, 8 giữ
  - `closeGroup` :329-361 — giữ {2,5} ⇒ 1 (C2), bỏ qua hàng 8
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductWriteService.php:565-607` (`writeAdmin` nhận `?int $companyId` tường minh, mặc định `current_company_role`)
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceCalculateRequestService.php:193, 244-262` (loại hàng 8 khỏi đếm + `skeletonRows`)
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceAskingRequestService.php:331-345` (`lineRow` thêm `is_temp`, `temp_reject_reason`, cờ `can_temp_approve`)
- Modify: `hrm-api/Modules/MasterData/Routes/api.php:285-304` (`POST price-asking-requests/{id}/temp-products/{product}/approve|reject`, middleware 1662; `GET .../temp-products/{product}` dữ liệu form duyệt)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/PriceAskingTempProductTest.php`

**Interfaces:** Consumes Task 1 hằng, Task 2 `TempProductService` + `TempProductRequest`. Produces API trên (FE Task 6/7 dùng): response `lineRow` có `company_status`, `is_temp`, `temp_reject_reason`, `can_temp_approve`.

- [ ] **Step 1 — test đỏ** `PriceAskingTempProductTest` (khuôn `PriceAskingRequestApiTest`):
  - sale tạo phiếu có 1 hàng thường + 2 hàng tạm (6), gửi ⇒ hàng thường 2, hàng tạm giữ 6;
  - PTKD `ptkdApprove` khi còn 6 ⇒ 422, câu có "Còn 2";
  - PTKD `tempApprove` hàng A (thiếu Đặc tính) ⇒ 422; đủ ⇒ pcc 7 + dữ liệu Quản trị ghi đúng **công ty phiếu**; người không 1662 ⇒ 403; PTKD công ty khác ⇒ 403;
  - `tempReject` hàng B không lý do ⇒ 422; có lý do ⇒ pcc 8 + log `temp_reject`;
  - `ptkdApprove` ⇒ A: 2, B: 8; nhóm chỉ có B ⇒ đóng Huỷ duyệt; lập YCTG nhóm của A: `skeletonRows` không có B;
  - `ptkdReject` khi có 7 ⇒ về 6, 8 giữ;
  - sale sửa A khi đang 7 (trước duyệt phiếu) ⇒ A về 6 ⇒ `ptkdApprove` lại bị chặn (Review Focus 2);
  - cạnh tranh: sau `tempApprove` hết, sale thêm hàng tạm mới vào phiếu Chờ PTKD (bị chặn sửa phiếu ở trạng thái 2 — khẳng định 422) (Review Focus 3);
  - đóng nhóm không giá ⇒ hàng tạm đã là 2 về 1 (C2).
- [ ] **Step 2** — chạy ⇒ FAIL.
- [ ] **Step 3** — cài đặt theo Files.
- [ ] **Step 4** — chạy test mới + `PriceAskingRequestApiTest`, `PriceCalculate*Test` ⇒ PASS; `vendor/bin/phpunit Modules/MasterData` xanh.
- [ ] **Step 5** — commit `P6 T3: YCHG — PTKD duyệt từng hàng tạm (Đồng ý/Không duyệt), duyệt phiếu khoá khi còn hàng tạm chưa duyệt`.

## Task 4: Màn "Hàng tạm" (BE + FE) + xoá cứng / xoá mềm

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductService.php:28-33, 180-216` (`SCREEN_TEMP = 'temp'`: pcc công ty hiện tại ∈ 6/7/8, `products.status <> 0`; cột thêm: YCHG đang chứa (mã + trạng thái phiếu/nhóm), người tạo, lý do không duyệt mới nhất)
- Modify: `hrm-api/Modules/MasterData/Routes/api.php:395-399` (`GET products/temp`, không gate quyền — D5; phạm vi công ty hiện tại)
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductLifecycleService.php:68-99` + `Entities/Product/Product.php:446-465` (`destroyTemp`: người tạo hoặc 1652; hàng trong YCHG Nháp(3)/Chờ PTKD(2) ⇒ 422; chưa từng vào `price_asking_request_products` ⇒ `hardDelete`; đã từng ⇒ `products.status = 0` (C1))
- Modify: `hrm-api/Modules/MasterData/Transformers/Product/ProductListResource.php` (cờ `can_edit_temp`, `can_delete_temp`, `can_ask_temp`)
- Create: `hrm-client/pages/master-data/products/temp.vue` (`extends: ProductListPage`, `layout: 'default-sidebar'`, `productScreen: 'temp'`)
- Modify: `hrm-client/utils/product-list-screens.js:49-172` (registry màn `temp`: cột như mockup M3 — bỏ cột giá, thêm "YCHG đang chứa", "Người tạo", "Trạng thái", "Lý do không duyệt"; hành động Sửa / Xoá / Lập YCHG)
- Modify: `hrm-client/components/subsystem-menu/master-data.js:59-85` (thêm `subItems` "Hàng tạm" thứ 5)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/TempProductScreenTest.php`

- [ ] **Step 1 — test đỏ**: màn `temp` chỉ trả hàng 6/7/8 của công ty hiện tại; cột YCHG đang chứa đúng mã; xoá: hàng chưa vào YCHG ⇒ hết dòng `products`; hàng trong phiếu Không duyệt ⇒ `products.status = 0`, không còn trên mọi màn, dòng phiếu cũ còn; hàng trong phiếu Chờ PTKD ⇒ 422; người khác không 1652 ⇒ 403 (Review Focus 5).
- [ ] **Step 2** — FAIL ⇒ **Step 3** cài đặt ⇒ **Step 4** PASS + MasterData xanh.
- [ ] **Step 5 — FE** trang + registry + menu; Playwright MCP (1440 + 1280): menu hub Danh mục dùng chung › Hàng hoá đếm 5 mục (đo DOM, `subItems`), cột đúng mockup, tiêu đề 1 dòng, hành động theo cờ, Xoá có hộp xác nhận; console 0 lỗi.
- [ ] **Step 6** — commit `P6 T4: màn Hàng tạm + xoá cứng/xoá mềm`.

## Task 5: Gỡ đường cũ HRM ⇒ ERP + chặn lập hợp đồng khi còn hàng chưa kinh doanh

**Files:**
- Delete: `hrm-api/Modules/Assign/Services/TmpProductSyncService.php`
- Modify: `hrm-api/Modules/Assign/Routes/api.php:677-679, 814-822` (gỡ 4 route); `hrm-api/Modules/Assign/Http/Controllers/.../QuotationController.php:734-860, 137-145` (gỡ 4 action + `buildTmpSyncSummary`); `QuotationResource.php:105` (gỡ `tmp_sync_status`)
- Modify: `hrm-api/Modules/Assign/Services/QuotationErpSyncService.php:43, 105-129, 171-202` (bỏ `createTmpProducts` + `tmpProductMap`; dòng chưa có `erp_product_id` ⇒ chặn sync với câu "Còn N hàng tạm chưa có mã / chưa kinh doanh")
- Modify: điều kiện `contract.is_synced` / lập hợp đồng (`QuotationService::syncToErpAfterApproval` :4095-4105 và nơi tính `is_synced`): mọi dòng có `erp_product_id` **và** pcc(công ty báo giá).status = 3 (C3)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php:110-125` (`filterOutNativeErp` giữ dòng có product mang log `temp_created` — C5)
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue:3-37, 414-445, 518, 655-713` (gỡ banner gửi/kéo duyệt hàng tạm; banner hợp đồng hiện "Còn N hàng tạm chưa tính giá xong" + link YCHG)
- Modify: `hrm-client/components/menu-sidebar.js:34-35`, `hrm-client/pages/assign/product-project/index.vue:47` (nhãn "Hàng tạm dự án")
- Test: `hrm-api/Modules/Assign/Tests/Feature/QuotationTempProductSyncTest.php` (mới, hoặc mở rộng test sync có sẵn)

- [ ] **Step 1 — test đỏ**: route gửi duyệt hàng tạm ⇒ 404; duyệt báo giá có dòng tạm chưa mã ⇒ KHÔNG INSERT `tmp_products` (đếm trước/sau), sync bị chặn có câu; dòng có mã nhưng pcc 6 ⇒ chặn; mọi dòng pcc 3 ⇒ sync chạy như cũ; `product-projects` vẫn trả dòng đã gắn mã hàng tạm.
- [ ] **Step 2** FAIL ⇒ **Step 3** cài đặt ⇒ **Step 4** PASS + chạy `vendor/bin/phpunit Modules/Assign` (ghi rõ ca đỏ sẵn trước khi sửa để so).
- [ ] **Step 5 — FE** Playwright MCP: tab Báo giá dự án không còn banner gửi duyệt hàng tạm; banner hợp đồng đúng câu; menu "Hàng tạm dự án".
- [ ] **Step 6** — commit `P6 T5: gỡ đường đẩy hàng tạm sang ERP, chặn lập HĐ khi còn hàng chưa kinh doanh`.

## Task 6: Popup "Thêm hàng tạm" chế độ YCHG + nút trên form YCHG

**Files:**
- Modify: `hrm-client/pages/assign/quotations/components/QuotationProductSearchModal.vue` (prop mới `mode: { type: String, default: 'quote' }` — `'ychg'`: hiện + bắt buộc Hãng SX, % VAT, Loại SP, Đặc tính, 3 ô cây chỉ đọc suy từ Loại SP, ẩn "Số lượng cần dùng"; Lưu gọi `POST master-data/temp-products` rồi `$emit('created', lineRow)`; tab Tái sử dụng gọi endpoint chế độ YCHG (C7) + nút "Dùng hàng này" điền sẵn 6 trường; lỗi báo đồng thời)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php:235-260` + route (tham số `scope=ychg`: dòng tạm của mọi dự án TKT người dùng được xem, không bắt buộc `prospective_project_id`)
- Modify: `hrm-client/components/sale/price-asking/PriceAskingRequestForm.vue:57-60, 149-185, 504-547` (nút "Thêm hàng tạm" trái "Chọn hàng hoá" 12px; nhận `created` ⇒ thêm `product_id` vào phiếu; dòng hàng tạm hiện badge 6/7/8, icon sửa (người lập) mở popup ở dạng sửa ⇒ `PUT master-data/temp-products/{id}`)
- Test e2e (spec mới, chạy khi user bảo): `wt-chuyen-doi-hang-hoa/e2e/tests/sale/price-asking-temp-product.spec.ts`

- [ ] **Step 1 — tái hiện trước (Playwright MCP)**: form YCHG chưa có nút; popup BOM hiện 4 ô bắt buộc (đo số ô `*`) — ghi số để so sau sửa.
- [ ] **Step 2** — cài đặt.
- [ ] **Step 3 — đo DOM (1440 + 1280)**: chế độ YCHG Lưu trống ⇒ 12 ô lỗi (khớp mockup); chọn Loại SP ⇒ 3 ô cây điền + hết lỗi; Lưu đủ ⇒ phiếu thêm 1 dòng badge "Hàng tạm"; Tái sử dụng điền sẵn 6 trường; popup ở BOM / Báo giá vẫn 4 ô bắt buộc, không có ô mới (so số Step 1); console 0 lỗi.
- [ ] **Step 4** — viết e2e: tạo hàng tạm thủ công + từ dòng BOM ⇒ dòng BOM đổi thành hàng thật (`erp_product_id`); ca không đủ trường.
- [ ] **Step 5** — commit `P6 T6: popup Thêm hàng tạm chế độ YCHG + nút trên form YCHG`.

## Task 7: Form duyệt hàng tạm (PTKD) + khoá Duyệt phiếu

**Files:**
- Create: `hrm-client/pages/sale/price-asking-requests/_id/temp/_productId.vue` (layout 'default-sidebar'; tải `GET master-data/price-asking-requests/{id}/temp-products/{product}`)
- Modify: `hrm-client/components/product/form/ProductForm.vue:83-118, 254-288` (prop `mode: 'temp-approve'`: 2 tab cha Thông tin hàng hoá + Quản trị hàng hoá (`ProductFormAdmin`, Tiểu mục không bắt buộc, dải "Dữ liệu của công ty <công ty phiếu>"); footer Lưu · Đồng ý · Không duyệt · Hủy; Lưu ⇒ `PUT master-data/temp-products/{id}` + admin; Đồng ý ⇒ `POST .../approve`; Không duyệt ⇒ `PriceAskingReasonModal` ⇒ `POST .../reject`; lỗi đồng thời 2 tab + chấm đỏ tab cha + mở tab lỗi đầu)
- Modify: `hrm-client/components/product/form/ProductFormGeneral.vue:91-99` (Đặc tính bắt buộc khi `mode === 'temp-approve'`; 3 ô cây hiện `*`)
- Modify: `hrm-client/components/sale/price-asking/PriceAskingRequestForm.vue:149-185, 222-257` (PTKD: dòng hàng tạm 6 nút **"Duyệt"** primary `ri-check-line`, 7/8 nút "Sửa"; dòng 8 mờ + gạch tên + "Không đi tiếp — lý do: …"; nút Duyệt phiếu `disabled` + tooltip "Còn N hàng tạm chưa duyệt" khi còn 6)
- Test e2e: thêm ca vào `price-asking-temp-product.spec.ts`

- [ ] **Step 1 — tái hiện trước**: chi tiết YCHG Chờ PTKD hiện chưa có nút Duyệt dòng (đo số nút).
- [ ] **Step 2** — cài đặt.
- [ ] **Step 3 — đo DOM (1440 + 1280)**: số nút "Duyệt" = số hàng 6; Duyệt phiếu `disabled === true` khi còn 6, `false` khi hết; form duyệt Đồng ý khi trống ⇒ 11 ô lỗi (9 + 2, khớp mockup), chấm đỏ 2 tab; Không duyệt trống lý do ⇒ 1 lỗi; footer không đè nội dung (toạ độ); mỗi hàng form 12 cột; console 0 lỗi.
- [ ] **Step 4** — e2e: PTKD đồng ý 1, không duyệt 1 ⇒ duyệt phiếu ⇒ hàng đồng ý "Chờ tính giá bán", hàng kia "Hàng tạm không duyệt"; người không 1662 không thấy nút Duyệt (role tạm); PTKD công ty khác ⇒ 403.
- [ ] **Step 5** — commit `P6 T7: form duyệt hàng tạm (Đồng ý/Không duyệt, tab Quản trị) + khoá Duyệt phiếu`.

## Task 8: ERP — chặn luồng hàng tạm cũ

**Files:**
- Modify: `ERP/app/Http/Middleware/ProductMovedToHrm.php:29-61` (đích `temp-list` ⇒ `/master-data/products/temp`, `temp-asking` ⇒ `/sale/price-asking-requests/add`; nhóm `TEMP_TARGETS` cho câu mô tả riêng)
- Modify: `ERP/resources/views/errors/moved_to_hrm.blade.php:21-23` (câu "Hàng tạm nay được lập trong Yêu cầu hỏi giá trên HRM và duyệt cùng phiếu.")
- Modify: `ERP/routes/web.php:678-692, 694-699, 3634-3644` — CHẶN ghi: tmpProductStore, tmpProductEdit, tmpProductReject, tmpProductDelete, tmpProductApprove, tmpProductDraftUpdate, TmpProductRequest.create, .store, .updateNote; GIỮ xem: tmpProductIndex, tmpProductShow, tmpProduct.searchData/export*, myTmpProduct*, TmpProductRequest.index/.show/.searchData/.print
- Modify: `ERP/routes/api.php:74-77` (`sync-from-hrm` ⇒ 410 JSON "Đã chuyển sang HRM"; `approved-status` giữ chỉ đọc)
- Modify: `ERP/resources/views/layouts/topmenubar.blade.php:20, 326, 1525-1532, 2227-2229, 2377-2381` (link tạo/duyệt ⇒ HRM `_blank` nhãn "(HRM)"; link xem giữ)
- Modify: `ERP/app/Http/Controllers/HomeController.php:548-573` (bỏ thẻ "Hàng tạm cần duyệt")
- Modify: `ERP/resources/views/quotations/form.blade.php:182-183` (nút "➕ Hàng tạm" ⇒ link HRM YCHG tạo mới `_blank`)
- Modify: `ERP/app/Observers/ProductWriteAuditObserver.php` (gỡ `tmpProductApprove` khỏi whitelist)
- Modify: `ERP/app/Product.php:7163-7167` (gỡ mốc `@TODO-PHASE6`, ghi chú "đường duyệt hàng tạm ERP đã chặn ở Phase 6")
- Test: `ERP/tests/Feature/TempProductRoutesMovedToHrmTest.php` (khuôn `PriceFlowRoutesMovedToHrmTest`) + cập nhật `ProductMovedToHrmRoutesTest.php` (106 ⇒ 106 + số route chặn mới), `G6PriceRoutesMovedToHrmTest.php` (bỏ `tmpProductApprove` khỏi danh sách giữ), `ProductBarcodeAndAuditTest.php` (`tmpProductApprove` không còn trắng)

- [ ] **Step 1 — test đỏ** `TempProductRoutesMovedToHrmTest`: GET tạo/sửa ⇒ 403 trang báo đúng 1 link HRM + câu hàng tạm; POST store/approve/reject/draft/updateNote ⇒ 403 JSON; GET danh sách / show / print vẫn 200 (không gắn middleware); `sync-from-hrm` ⇒ 410.
- [ ] **Step 2** FAIL ⇒ **Step 3** cài đặt ⇒ **Step 4** `php vendor/bin/phpunit` ERP: xanh trừ `ExampleTest` đỏ sẵn (N45).
- [ ] **Step 5** — Playwright ERP 8090 (role tạm quyền "Duyệt hàng tạm" + "Thêm báo giá", gỡ khi xong): menu đếm link HRM mới, 0 link tạo/duyệt cũ, trang chủ 0 thẻ hàng tạm, nút báo giá trỏ HRM; 403 trang báo.
- [ ] **Step 6** — commit `P6 T8: ERP chặn tạo/duyệt hàng tạm ⇒ HRM`.

## Task 9: Nghiệm thu + tài liệu

- [ ] PHPUnit: `Modules/MasterData` toàn bộ + `Modules/Assign` (so ca đỏ sẵn) + ERP toàn bộ.
- [ ] e2e (khi user bảo): spec mới `price-asking-temp-product` + chạy lại `price-asking-request`, `price-calculate-request`, `finance/price-calculate`, các spec BOM / báo giá có dùng popup hàng tạm, `master-data/products-*` (ẩn hàng tạm).
- [ ] Soát chéo: `git grep` marker xung đột 3 repo; `grep` mọi chỗ đọc `pcc.status` còn sót (so `diem-cham-code.md` §A).
- [ ] Runbook (`gia-theo-cong-ty/runbook-trien-khai.md`, Phần 3 Hàng tạm): không migration / seeder; nhắc dọn 1 hàng tạm ERP đang chờ duyệt trước go-live; deploy ERP chặn cùng lần; cấp quyền: không quyền mới.
- [ ] Cập nhật `SO-CHOT-VA-TON.md`, `viec-con-lai.md` (A2 ✅), `bang-man-hinh-menu.md` (màn Hàng tạm + form duyệt + popup), checkpoint cuối plan.
- [ ] Merge LOCAL `feat/p6-hang-tam` ⇒ nhánh chung (2 repo) và `feat/p6-chan-hang-tam` ⇒ `feat/2d1-erp-khong-loi`; push khi user cho.

---

## Phạm vi sẽ xin "làm"

| | |
|---|---|
| Repo / nhánh | **hrm-api + hrm-client** worktree `wt-chuyen-doi-hang-hoa`, nhánh con `feat/p6-hang-tam` từ `feat/chuyen-doi-hang-hoa` · **ERP** worktree `wt-erp-2d1`, nhánh con `feat/p6-chan-hang-tam` từ `feat/2d1-erp-khong-loi`. Merge LOCAL, không push |
| File chính | hrm-api `Modules/MasterData` (ProductCompany, ProductService, ProductWriteService, ProductLifecycleService, ProductCatalogService, ProductOptionService, PriceAskingProductReader, PriceAskingRequestWriter, PriceAskingRequestService, PriceCalculateRequestService, routes, 2 request + 1 service + 1 controller mới) · `Modules/Assign` (gỡ TmpProductSyncService + 4 route/action, QuotationErpSyncService, điều kiện lập HĐ, ProductProjectController) · `Modules/CustomerCare` (2 chỗ lọc) · hrm-client popup dùng chung `QuotationProductSearchModal.vue` (thêm chế độ, mặc định giữ hành vi cũ), `PriceAskingRequestForm.vue`, `ProductForm.vue` + `ProductFormGeneral.vue`, màn mới `products/temp.vue` + trang form duyệt, registry/menu, `ProspectiveProjectQuotationsTab.vue`, menu-sidebar · ERP middleware + view trang báo + `routes/web.php` / `api.php` + topmenubar + HomeController + quotations/form + observer + tests |
| DB | `hrm_erp_giacty`: **không** migration / seeder; chỉ dữ liệu thử khi kiểm rồi dọn; role tạm cho e2e / Playwright (gỡ khi xong) |
| Không đụng | `gop_db`; `PermissionsTableSeeder`; `report_templates`; dữ liệu cũ `tmp_products` / `products.tmp_product_id` |

## Kết quả thực hiện (12–13/10/2026 — subagent-driven, mỗi task review riêng + review toàn nhánh)

| Task | Commit | Ghi chú |
|---|---|---|
| T1 trạng thái 6/7/8 + ẩn | api a19f6012f · client 621ae0e34 | review sạch |
| T2 tạo/sửa hàng tạm | api 7def38679..99201d3d9 | 1 vòng sửa (test checkTypeTree, rollback nguồn) |
| T3 YCHG + PTKD duyệt từng hàng | api bb7dd513e..b7b36a128 | 2 vòng sửa: PTKD đổi quyết định 6/7/8; sale sửa không xoá dữ liệu Quản trị; hàng 8 không tính "đang mở"; PTKD không đổi Thương hiệu/Hãng; thứ tự khoá products→pcc; hàng 8 sang YCHG mới ⇒ gỡ dòng ở phiếu cũ |
| T4 màn Hàng tạm + xoá | api 62a70da52..0889f5828 · client 0297e89e5..1a6c3436f | thêm tick + Lập YCHG hàng loạt, lọc "Yêu cầu hỏi giá" (mockup M3); picker YCHG loại hàng xoá mềm |
| T5 gỡ đường đẩy ERP + cổng HĐ | api a0a02154c..099594b5a · client 1d3e8e64b | bỏ mysql2; company_id NULL ⇒ chưa đạt mọi đường; payload không rớt dòng |
| T6 popup chế độ YCHG | api f2767ec18..b67a2a37f · client 151abc4a6..bbf221083 | test đối chiếu luật xem dự án TKT (bắt 1 lệch thật: dự án nháp người khác) |
| T7 form duyệt PTKD | client bba8eab26..6f1d8aab4 | footer ẩn Đồng ý (7) / Không duyệt (8) theo mockup |
| T8 ERP chặn | ERP f117bf3ce4 | 9 route chặn (106⇒115), sync-from-hrm 410 |
| Review toàn nhánh | api 499cc2c25 · client 8edf78631 · ERP 089a50c66d | sửa 4 Important: đổi hãng qua đường sale khi phiếu Chờ PTKD; đường sửa 1652 chặn hàng tạm; picker BOM + import BOM loại hàng tạm; itemSearch loại theo công ty chủ |

PHPUnit cuối: MasterData 447 · Assign 18 (1 skip cũ) · ERP 75 (ExampleTest đỏ sẵn N45).
e2e (user cho chạy 12/10): price-asking-temp-product **12/12** (sửa 4 lỗi spec, app không lỗi) · products-temp-ui **7/7** · Phase 7 (YCHG/YCTG/PTG/chính sách) **28/28** · products API **20/20** (loại 4 ca đỏ sẵn roles.company_id / nocost / E14) · products UI: xem dưới.
products UI (read/take/form/lifecycle) **42 passed / 0 failed** (2 skip sẵn; loại ca N1 đỏ sẵn `roles.company_id`) — cập nhật 2 spec cũ cho khớp Phase 7 (lọc có "Đang tính giá"; nút "Lập yêu cầu hỏi giá"), không lỗi app.

### Checkpoint — 2026-10-13
✅ **PHASE 6 XONG (local)**: merge LOCAL — hrm-api `657fa731f`, hrm-client `38f165934` (nhánh chung, chưa push: api +14, client +10); ERP `396f42dd7c` (`feat/2d1-erp-khong-loi`, chưa push +3).
Sổ thực hiện + mọi ruling: `p6-so-thuc-hien.md`. Còn chờ user: duyệt câu banner C3 mới; push; điều kiện go-live B5/B6 (nhập cây phân loại + Đặc tính).

## Bổ sung 13/10 — icon ⓘ giải thích logic nút duyệt (user "làm")
User giữ cách PTKD đổi được quyết định tới khi Duyệt phiếu; yêu cầu thêm ⓘ ở 6 nút: Duyệt (dòng) · Sửa (dòng đã xử lý) · Duyệt phiếu · Lưu / Đồng ý / Không duyệt (form duyệt). Phạm vi: hrm-client nhánh `feat/p6-info-icon` từ nhánh chung, merge LOCAL, không push, không DB. Skill `info-icon-tooltip`.
✅ 13/10 xong: client 293b3f5d1 ⇒ merge LOCAL nhánh chung (chưa push). ⓘ 6 nút đúng nguyên văn, đo 1280/1440 (1 dòng, không chồng nút, form hàng hoá thường không đổi), e2e price-asking-temp-product 13/13; review đạt.

✅ **13/10: user duyệt câu banner C3 mới + PUSH** — hrm-api `origin/feat/chuyen-doi-hang-hoa` @ `657fa731f`, hrm-client @ `dc793189e`, ERP `origin/feat/2d1-erp-khong-loi` @ `396f42dd7c`.
