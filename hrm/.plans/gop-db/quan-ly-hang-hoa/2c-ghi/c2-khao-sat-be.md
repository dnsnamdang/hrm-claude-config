# Đợt 2-C2 — Lấy về + sửa mức Quản trị: khảo sát BE (08/10/2026)

> CHỈ ĐỌC: không sửa source, không ghi DB. Code HRM = worktree `websites/wt-chuyen-doi-hang-hoa/hrm-api`
> nhánh `feat/chuyen-doi-hang-hoa` (HEAD `35c4aa971`, đã có 2-C1 + 2-C3); đường dẫn dưới đây tính từ
> `hrm-api/Modules/MasterData/` trừ khi ghi khác. ERP = `ERP/TanPhatDev` (nhánh `develop_01`).
> Số đo: DB local `hrm_erp` (chỉ SELECT), 08/10/2026.
> Luật ưu tiên: `chot.md` (G1–G11, C1–C12, D1–D4, T6, H1') > `yeu-cau-ghi.md` §1.2/§1.5 > mockup.

---

## 0. Tóm tắt

| # | Kết luận |
|---|---|
| 1 | Nền 2-C1 dùng lại được gần hết: `ProductWriteService::writeAdmin()` (`Services/Product/ProductWriteService.php:402-444`) đã upsert đúng khuôn (có dòng ⇒ UPDATE 4 cột, giữ `coefficient`; NCC + catalog xoá-chèn trong phạm vi `company_id`), `checkClusters` (D3) ở `Http/Requests/Product/ProductRequest.php:318-332`. Chỉ cần **tách lối vào**: endpoint *Lấy về* mới + endpoint *sửa tab Quản trị* nhận công ty lấy về |
| 2 | Hiện BE chặn công ty KHÁC ở **mọi** đường ghi bằng `assertOwner()` (`ProductWriteService.php:84-97`, gọi từ `ProductRequest::authorize` :21-31 và `ProductWriteController::edit` :31-46) ⇒ công ty lấy về hiện 403 cả form lẫn Lưu. `can_edit` (`Transformers/Product/ProductListResource.php:60-63`, `ProductDetailResource.php:44-47`) chỉ đúng cho công ty tạo |
| 3 | Bảng `product_company_coefficients`: 1.105 dòng, **100% `status` NULL** (chưa dòng nào thuộc luồng — dữ liệu thử 2-C1 đã dọn); 803 dòng hệ số cũ của Cty 2/3/4 nằm trên hàng `products.status = 1` ⇒ lấy về các mã này phải **UPDATE** (UNIQUE `product_id, company_id` có thật) |
| 4 | Sinh dòng `coefficient = 1` cho mã chưa có dòng ⇒ giá popup ERP của công ty lấy về **làm tròn nghìn** (đã chấp nhận K2). Quy mô nếu lấy về toàn bộ: ~8.200–8.850 mã/công ty có giá cơ bản lẻ nghìn. Dòng hệ số cũ được UPDATE giữ nguyên `coefficient` ⇒ 0 thay đổi giá |
| 5 | Sau lấy về: dòng `status = 1` *Đang nhập thông tin* ⇒ hiện ở *Hàng hoá nhập thông tin* + *Dữ liệu hàng hoá công ty*, rời trạng thái "Chưa sử dụng" ở *Kho dữ liệu*; theo H1' **treo ở 1 tới phase Tính giá** |
| 6 | Kho dữ liệu đang hiện **17.512** hàng `products.status = 0` (38% kho) nhãn "Chưa sử dụng" cho MỌI công ty. ERP màn danh sách chính **loại** status 0 (chỉ hiện ở tab "Đã xoá" — `app/Product.php:1754-1762`) ⇒ đề xuất lọc bỏ |
| 7 | 4 câu nghiệp vụ còn mở (mục 7): trạng thái khi lấy về mã đã có hệ số cũ · giá trị 4 ô quản trị lúc lấy về · lấy về hàng công ty tạo còn đang nhập thông tin · status 0 ở Kho |

---

## 1. Hiện trạng code sau 2-C1

### 1.1 Route khối `master-data/products` (`Routes/api.php:253-289`)

| Route | Dòng | Gate | Ghi chú cho 2-C2 |
|---|---|---|---|
| `GET /warehouse` | :266 | đăng nhập | Kho dữ liệu — nguồn cho nút *Lấy về* + popup *Xem hàng hoá Công ty khác*; đã có `usage=unused` (công ty mình chưa dùng — `Services/Product/ProductService.php:178-185`) và lọc `owner_company_id` (:323) |
| `GET /company` | :269 | 1652 \| 1653 | hàng có `company_status` NOT NULL |
| `GET /entering` | :270 | 1652 | `company_status = 1` ⇒ hàng lấy về hiện ở đây |
| `POST /catalogs/sync` | :277 | 1655 | 2-C3 — nhận hàng có `company_status` NOT NULL ⇒ hàng lấy về xếp catalog được ngay |
| `POST /` | :283 | 1652 | tạo (2-C1) |
| `GET /{product}/edit` | :285 | 1652 | **chỉ chủ** (`assertOwner`) |
| `PUT /{product}` | :286 | 1652 | **chỉ chủ**, nhận lớp chung + `admin` trong 1 payload |
| `GET /{product}` | :288 | đăng nhập | chi tiết chỉ đọc |

Chưa có: `POST /take` (lấy về), `PUT /{product}/admin-data` (2-C1 đã ghi tên này ở `c1-plan.md:2687`).

### 1.2 "Công ty tạo" vs "công ty khác"

- Công ty đang làm việc = `auth()->user()->current_company_role` (`app/Models/TpEmployee.php:97-117`, lùi về `company_id`) — `ProductWriteService::companyId()` :43-46, `ProductService::currentCompanyId()` :56-59.
- **Công ty tạo** = `products.company_id`. **Công ty lấy về** = có dòng `product_company_coefficients` với `status` NOT NULL mà không phải chủ (`yeu-cau-ghi.md:33`). Code CHƯA có khái niệm này ở đâu.
- Trạng thái theo công ty: `Entities/Product/Product.php:366-389` — `COALESCE(pcs.status, CASE WHEN products.status = 1 AND products.company_id = X THEN 3 END)`. ⇒ Dòng hệ số cũ của chi nhánh (`status` NULL, không phải chủ) cho ra **NULL = "Chưa sử dụng"** ⇒ đúng là đối tượng *Lấy về*.

### 1.3 Chỗ BE đang chặn sửa

| Chỗ | Dòng | Luật |
|---|---|---|
| `ProductRequest::authorize()` | `ProductRequest.php:21-31` | `assertCanWrite()` (1652 theo CÔNG TY ĐANG LÀM VIỆC — R22, `PermissionService::isCurrentEmployeeHasPermission`) + `assertOwner()` khi có `{product}` ⇒ 403 trước mọi 422 (R6) |
| `ProductWriteService::assertOwner()` | `ProductWriteService.php:84-97` | không phải chủ ⇒ 403 · `products.status ≠ 1` ⇒ 403 (D2) · dòng công ty `status = 4` ⇒ 403 |
| `ProductWriteController::edit()` | `ProductWriteController.php:31-46` | như trên |
| `can_edit` | `ProductListResource.php:60-63`, `ProductDetailResource.php:44-47` | chủ ∧ `products.status = 1` ∧ trạng thái ≠ 4 ∧ 1652 tại công ty |

⚠️ G6 (`chot.md`) ghi "đã khoá thì BE chặn sửa tab Quản trị (**423**)", còn 2-C1 trả **403** cho status 4. Không có dòng status 4 nào trong DB (0/1.105) — giữ 403 cho đồng bộ 2-C1, để 2-C4 chốt mã khi làm Khoá.

### 1.4 Quyền 1652–1656 (`man-danh-muc-hang-hoa/design.md` §35b, seeder `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1581-1584`)

| id | Tên | Có trong DB local | Ý nghĩa |
|---|---|---|---|
| 1652 | Xây dựng thông tin hàng hoá | ✅ | tạo/sửa hàng + dữ liệu quản trị CỦA CÔNG TY MÌNH; **"Chỉ quyền này dùng được chức năng lấy hàng hoá về công ty"** (§35b, nguyên văn user) — nút Lấy về ở Kho + popup Công ty khác gate 1652 cả FE lẫn BE |
| 1653 | Xem dữ liệu hàng hoá công ty | ✅ | vào màn Dữ liệu hàng hoá công ty |
| 1654 | Xuất excel danh sách hàng hoá | ❌ (2-E) | |
| 1655 | Xây dựng catalog kinh doanh | ✅ | popup catalog (2-C3) |
| 1656 | Cấu hình chính sách giá bán nội bộ | ❌ (phase Tính giá) | |

⇒ *Lấy về* và *sửa tab Quản trị của công ty lấy về* đều dùng **1652**, không thêm quyền (đã chốt, không hỏi lại). DB local: 1652 chỉ gán ở `company_id = 1` (role *Super admin*, *E2E No Cost*) ⇒ test/e2e đóng vai Cty 2 phải cấp role tạm (trait `Tests/Feature/Concerns/ActsAsProductUser.php:13` đã làm sẵn theo công ty).

---

## 2. Thiết kế endpoint Lấy về

### 2.1 Đề xuất

`POST master-data/products/take` — middleware `checkPermission:Xây dựng thông tin hàng hoá` + Service `assertCanWrite()` (R22).

| | |
|---|---|
| Input | `product_ids` `required|array|min:1|max:100` · `product_ids.*` `integer|distinct` (G9b trần 100) |
| Output | `{ taken: [{id, code}], skipped: [{id, code, reason}] }` — FE ra toast *"Đã lấy <mã> về <cty> — trạng thái Đang nhập thông tin"* / *"Đã lấy N hàng hoá…"* + liệt kê mã bỏ qua (mockup `layHangVe`, `yeu-cau-ghi.md:107`) |
| Ngữ nghĩa lô | **bỏ qua từng mã không hợp lệ, lấy phần còn lại** (theo mockup "mã công ty đã dùng ⇒ bỏ qua, báo …đang dùng rồi"); khác 2-C3 (cả lô hoặc không) vì mockup nói rõ. Tự chốt — thuần hành vi UI |

### 2.2 Kiểm tra từng mã (1 transaction, `lockForUpdate` các dòng `product_company_coefficients` của công ty mình)

| # | Điều kiện | Kết quả |
|---|---|---|
| 1 | id không tồn tại | bỏ qua "không tồn tại" (hoặc 422 cả lô bằng `exists` — chọn bỏ qua cho đồng nhất) |
| 2 | `products.status ≠ 1` (0 đã xoá/khoá ERP 17.512 · 2 chờ duyệt 1 · 5 không duyệt 6) | bỏ qua "hàng đã xoá/chưa duyệt ở ERP" (G9b) |
| 3 | `products.company_id = công ty mình` | bỏ qua "hàng do công ty mình tạo" (luôn suy ra đang dùng) |
| 4 | đã có dòng của công ty mình, `status` NOT NULL (1/2/3/4) | bỏ qua "đang dùng rồi" |
| 5 | đã có dòng, `status` NULL (dòng hệ số cũ) | **UPDATE** `status = 1`, `updated_by`, `updated_at` (+ 4 ô quản trị theo Q2); **KHÔNG đụng `coefficient`** |
| 6 | chưa có dòng | **INSERT** `product_id, company_id = current_company_role` (gán tay — `DB::table` không qua hook `BaseModel`), `coefficient = 1` (`ProductCompany::NEUTRAL_COEFFICIENT`, K2), `status = 1`, `created_by`, timestamps (+ 4 ô theo Q2). Dùng `insertOrIgnore`: 0 dòng chèn ⇒ có người vừa lấy cùng lúc ⇒ đưa vào "đang dùng rồi" |

Không cần "khoá" riêng: G6 chưa làm; hàng mà CÔNG TY TẠO đang Ngừng KD (4) là khoá theo công ty tạo, không chặn công ty khác lấy về (khoá theo công ty — G6).

⚠️ Không dùng `DB::upsert()` (Laravel 8.83 có): `ON DUPLICATE KEY UPDATE` sẽ ghi đè cả dòng `status` NOT NULL (mất trạng thái) nếu không viết điều kiện — tách SELECT…FOR UPDATE + UPDATE/INSERT rõ ràng, dễ test.

### 2.3 Có ghi NCC / catalog không

- **NCC**: không. `product_suppliers` theo `company_id` (K3 — 1.741/1.741 dòng đang thuộc Cty 1); công ty lấy về tự khai ở tab Quản trị.
- **Catalog**: không. Lấy về chưa có catalog; C1 (≥ 1 Tiểu mục) chỉ áp khi **Lưu tab Quản trị**. Xếp sau bằng popup 2-C3 (1655) hoặc form (1652). DB: `product_business_catalogs` 0 dòng.
- **Lớp chung `products`**: không đụng bất kỳ cột nào.

### 2.4 Số đo DB

| Hạng mục | Số |
|---|---|
| `product_company_coefficients` | 1.105 dòng / 589 hàng — **mọi dòng `status` NULL**; 4 cột quản trị: 0 dòng có giá trị |
| …theo công ty | Cty 1: 1 · Cty 2: 538 · Cty 3: 516 · Cty 4: 50 |
| …dòng của chính công ty tạo | 5 |
| …dòng công ty KHÁC trên hàng `products.status = 1` | **803** (Cty 2: 398 · Cty 3: 382 · Cty 4: 23) ⇒ ca UPDATE |
| …dòng công ty KHÁC trên hàng `status = 0` | 297 (164 hàng) ⇒ không lấy về được (G9b) |
| Hàng có dòng ≥ 2 công ty | 515 |
| Hệ số của 1.100 dòng công ty khác | 1.0000: 254 · 1.0200: 392 · 1.0300: 425 · khác (1.05–1.29): 29 |
| `products.status` | 1: 28.371 · 0: 17.512 · 5: 6 · 2: 1 |
| `products.company_id` (status 1) | Cty 1: 27.370 · Cty 4: 984 · Cty 3: 14 · Cty 2: 3 |

**Số mã lấy về được và ảnh hưởng giá ERP (K2)** — "lẻ nghìn" = có ít nhất 1 dòng giá ĐVT cơ bản `MOD(price,1000) ≠ 0`, chưa có dòng của công ty đó:

| Công ty | Mã lấy về được (`status=1`, không phải chủ) | …đã có dòng hệ số cũ (UPDATE, giá không đổi) | …chưa có dòng & giá lẻ nghìn (INSERT ⇒ popup ERP làm tròn nghìn) |
|---|---:|---:|---:|
| 1 Tân Phát | 1.001 | 0 | 620 |
| 2 CN Hải Phòng | 28.368 | 398 | 8.643 |
| 3 CN Vinh | 28.357 | 382 | 8.635 |
| 4 Tân Phát SG | 27.387 | 23 | 8.234 |
| 8 Etek | 28.371 | 0 | 8.849 |

Chỗ đọc hệ số (đối chiếu K2):
- ERP `app/Http/Controllers/Common/SearchController.php:415, :894, :1310, :1703` — `CASE WHEN pcc.coefficient IS NOT NULL THEN ROUND(price × coef / 1000) × 1000` (popup 338 màn) ⇒ **làm tròn**; join theo `Auth::user()->info->company_id` (:403), KHÔNG phải `company_role`.
- ERP `app/Product.php:1655` — nhân không làm tròn ⇒ × 1 không đổi.
- HRM `Modules/CustomerCare/Services/ServiceService.php:1055` — làm tròn nghìn (như ERP).
- HRM `Modules/Finance/Services/ProductImportRequestService.php:1448`, `ProductTransferRequestService.php:984`, `BorrowSellRequest/BorrowSellRequestService.php:457` — `->value('coefficient') ?? 1` ⇒ × 1 không đổi.

⚠️ 3 nhân viên có `company_role ≠ company_id` (DB local): HRM ghi dòng theo `company_role`, popup ERP đọc theo `info->company_id` ⇒ với 3 người này, hàng lấy về không đổi giá ERP và ngược lại. Ghi nhận, không xử lý ở 2-C2.

---

## 3. Sửa mức Quản trị cho công ty lấy về

### 3.1 Trường thuộc tab Quản trị (công ty lấy về SỬA được)

| Trường | Bảng / cột | Phạm vi |
|---|---|---|
| Chính sách kinh doanh | `product_company_coefficients.business_policy_id` | dòng của công ty mình |
| SL tồn kho tối thiểu | `.min_stock_qty` | dòng của công ty mình |
| Bảo hành + Đơn vị | `.guarantee`, `.guarantee_type` (`in:ngay,thang,nam`) | dòng của công ty mình |
| Nhà cung cấp | `product_suppliers (product_id, supplier_id, company_id)` | xoá-chèn `where company_id = mình` |
| Catalog (≥ 1 Tiểu mục — C1; nhánh đã lưu bị khoá thì giữ — D3) | `product_business_catalogs` | xoá-chèn `where company_id = mình` |

### 3.2 Lớp chung — công ty lấy về KHÔNG sửa (BE phải chặn)

Toàn bộ `fillCommon` (`ProductWriteService.php:131-159`: tên, model, thương hiệu, hãng, xuất xứ, loại SP, thuế…) + `writeChildren` (:165-176: ĐVT, thuộc tính, 4 bảng kèm theo, tài liệu kỹ thuật, ảnh, video, xe, nhóm máy) + **`tech_coefficient`** (nằm ở tab Quản trị trên giao diện nhưng là cột chung — T6: chỉ công ty tạo sửa).

### 3.3 Đề xuất cách chặn (tự chốt kỹ thuật, theo `yeu-cau-ghi.md` §1.2 + §23d)

1. **Tách endpoint** `PUT master-data/products/{product}/admin-data` (gate 1652), request riêng `ProductAdminDataRequest` chỉ có rule `admin.*` (chép 8 rule `ProductRequest.php:131-139` + `checkClusters` :318-332 — nên tách `checkClusters` ra trait/helper dùng chung).
2. `authorize()`: `assertCanWrite()` + `assertCanEditAdmin($product)` mới: `products.status = 1` (D2) ∧ (là chủ ∨ có dòng công ty mình `status` NOT NULL) ∧ trạng thái ≠ 4 ⇒ ngược lại **403** (trước mọi 422 như R6).
3. Payload có khoá cấp 1 ngoài `admin` (vd `name`, `units`, `tech_coefficient`, `company_id`) ⇒ **403** "Chỉ công ty tạo hàng hoá mới được sửa thông tin chung" — theo §23d *"không bỏ qua im lặng"*. (Bỏ qua im lặng cũng an toàn vì endpoint không bao giờ ghi lớp chung, nhưng 403 làm lộ lỗi FE gửi nhầm và có ca test rõ.)
4. `PUT /{product}` (đầy đủ) **giữ chỉ chủ** — công ty lấy về gọi vào ⇒ 403 như hiện nay (`assertOwner`).
5. Service: gọi lại `writeAdmin($product, $admin, …)` — với công ty lấy về luôn đã có dòng ⇒ đi nhánh UPDATE :414-417 (giữ `coefficient`, không đổi `status` — C2/H1'). Cho phép cả chủ gọi endpoint này (đi nhánh G4/D1 sẵn có) nhưng FE chỉ dùng cho công ty lấy về.
6. `GET /{product}/edit` nới: chủ ∨ công ty lấy về; trả thêm `edit_scope: 'full' | 'admin'` (hoặc `can_edit_common`) để FE khoá 5 tab + hiện dải *"Hàng hoá do <công ty tạo> tạo — chỉ khai được tab Quản trị hàng hoá"*. `ProductFormResource.php:34-36` hiện chưa trả `owner_company_id`.
7. `can_edit` (list + chi tiết): mở thêm cho công ty lấy về (`company_status` ∈ {1,2,3} ∧ không phải chủ); kèm cờ `can_take` = `products.status = 1` ∧ `company_status` NULL ∧ không phải chủ ∧ 1652 — cho nút *Lấy về* ở Kho.

### 3.4 Dòng status 4 (G6 chưa làm)

0 dòng status 4 trong DB. 2-C2 xử lý giống 2-C1: công ty mình đang 4 ⇒ ẩn Sửa, `admin-data` 403; *Lấy về* bỏ qua "đang dùng rồi" (dòng NOT NULL). Mã 403/423 để 2-C4 chốt cùng thao tác Khoá.

---

## 4. Trạng thái sau khi lấy về

- Dòng mới/UPDATE `status = 1` *Đang nhập thông tin* (mockup `layHangVe` → `st = nhap`; `yeu-cau-ghi.md:107`, sơ đồ :137). Badge `#64748B` (`Entities/Product/ProductCompany.php:23-41`).
- Theo luật đọc 2-B (`Product.php:366-389`, `ProductService.php:173-201`):

| Màn | Trước lấy về | Sau lấy về |
|---|---|---|
| Kho dữ liệu | "Chưa sử dụng", lọt công tắc `usage=unused` | badge *Đang nhập thông tin*; ra khỏi `unused`; cột *Công ty đang kinh doanh* **không** có công ty mình (chỉ đếm status 3 — `Product.php:405-419`) |
| Dữ liệu hàng hoá công ty (1652\|1653) | không có | **có** (mọi `company_status` NOT NULL) |
| Hàng hoá nhập thông tin (1652) | không có | **có** (`= 1`) |
| Hàng đang kinh doanh | không có | không có (cần 3) |
| Popup Xây dựng catalog (1655) | không thêm được | thêm được (`ProductCatalogService.php:155-170` chỉ đòi `company_status` NOT NULL, ≠ 4, `status ≠ 0`) |

- Theo H1'/H1'': không có đường 1 → 2 → 3 tới phase Tính giá ⇒ hàng lấy về **treo ở 1** và không bao giờ vào *Hàng đang kinh doanh* của công ty lấy về trong Phase 2. Với 803 mã chi nhánh **đang bán thật ở ERP** (có hệ số cũ) đây là điểm cần chốt — xem Q1.

---

## 5. Tồn nhỏ: `products.status = 0` ở Kho dữ liệu

| Đo | Số |
|---|---|
| Hàng `status = 0` | **17.512** / 45.890 (38%) — `deleted_at` có: 16.030 · trống: 1.482; 1 hàng `company_id` NULL |
| …có dòng hệ số | 164 hàng (297 dòng) |
| …có catalog | 0 |
| Nhãn ở Kho | "Chưa sử dụng" cho mọi công ty, kể cả công ty tạo (CASE suy ra đòi `status = 1`) — FE `hrm-client/components/product/ProductListPage.vue:286-289` |
| 3 màn còn lại | không lọt (đòi `company_status` NOT NULL) |

Đối chiếu:
- ERP danh sách hàng hoá: mặc định `whereIn(status, [1, 2, 5])`, status 0 chỉ ở chế độ `type = deleted` (`ERP/TanPhatDev/app/Product.php:1754-1762`).
- HRM đã loại status 0 ở: popup catalog (B5, `ProductCatalogService.php:123`), sửa (D2), lấy về (G9b), rule trùng tên (`ProductRequest.php:277`).
- Hiện status 0 với nhãn "Chưa sử dụng" + (sau 2-C2) không có nút *Lấy về* ⇒ người dùng thấy 17.512 dòng "chưa dùng mà không lấy được".

⭐ Đề xuất: `GET /warehouse` thêm `where products.status <> 0` (giữ status 2/5 — 7 mã — như ERP, ẩn nút Lấy về theo `can_take`). Xem Q4.

---

## 6. Rủi ro, file sẽ đụng, PHPUnit

### 6.1 Rủi ro / bẫy

| # | Bẫy | Hệ quả / cách né |
|---|---|---|
| R1 | INSERT mù trên UNIQUE `(product_id, company_id)` — 803 dòng hệ số cũ | 1062 nổ cả lô ⇒ SELECT…FOR UPDATE rồi UPDATE/INSERT tách nhánh; `insertOrIgnore` cho ca đua |
| R2 | `upsert()`/`updateOrInsert` ghi đè `coefficient` = 1 lên dòng hệ số cũ | **đổi giá ERP im lặng** (392 dòng 1.02, 425 dòng 1.03…) ⇒ test bất biến `coefficient` |
| R3 | UPDATE dòng có `status` NOT NULL | lùi trạng thái (3 → 1) ⇒ chỉ UPDATE `whereNull('status')` |
| R4 | Hook `BaseModel::creating` gán `company_id = info->company_id` | nếu dùng Eloquent `ProductCompany::create` ⇒ sai công ty khi `company_role ≠ company_id` ⇒ gán tay / `DB::table` |
| R5 | Endpoint `admin-data` "lọc bớt field" thay vì từ chối | dễ thủng khi thêm field sau ⇒ whitelist + 403 khoá lạ (mục 3.3) |
| R6 | `tech_coefficient` hiện ở tab Quản trị nhưng là cột chung (T6) | công ty lấy về gửi kèm ⇒ 403; FE khoá ô |
| R7 | `AdminData::source()` (`Transformers/Product/AdminData.php:18-23`): công ty CHƯA có dòng thì lùi về cột chung `products.*`; có dòng (kể cả 4 cột NULL) thì đọc dòng | lấy về mà để 4 ô NULL ⇒ cột *Bảo hành / Tồn tối thiểu* ở danh sách + chi tiết của công ty đó **từ có giá trị thành trống** ngay sau khi bấm Lấy về ⇒ Q2 |
| R8 | ERP form hàng hoá + màn Hãng SX xoá sạch dòng `product_company_coefficients` khi lưu (N2, 2-A K2) | mất trạng thái *đã lấy về* tới khi 2-D chặn route — đã ghi N2/N4, nhắc lại vì 2-C2 là đợt đầu sinh dòng cho công ty KHÁC |
| R9 | 1652 trên DB local chỉ gán ở Cty 1 | test/e2e vai Cty 2 phải role tạm + `cache:clear` (bẫy spatie cache 24h); N12 thiếu tài khoản e2e "chỉ xem" |
| R10 | `ProductFormResource.php:35` `company_status` chỉ đọc dòng thật, không suy ra | hàng cũ của chủ ra NULL ở form (khác list/chi tiết) — vô hại cho 2-C2, ghi nhận |
| R11 | FE: `ProductFormAdmin.vue` chưa có prop `adminOnly` (khảo sát FE 2-C1 nói "sẵn" nhưng grep 0 kết quả); ô tick dòng ở `ProductListPage.vue` chỉ bật cho màn công ty + 1655 | FE 2-C2 phải mở rộng ô tick cho Kho (1652) — tách điều kiện khỏi `canBuildCatalog` |

### 6.2 File sẽ đụng (hrm-api)

| Loại | File |
|---|---|
| Create | `Http/Requests/Product/ProductTakeRequest.php` · `Http/Requests/Product/ProductAdminDataRequest.php` · `Tests/Feature/ProductTakeApiTest.php` (hoặc thêm ca vào `ProductWriteApiTest.php`) |
| Modify | `Routes/api.php` (khối :253-289: `POST /take` trước `/{product}`, `PUT /{product}/admin-data`) · `Http/Controllers/V1/Product/ProductWriteController.php` (`take`, `updateAdmin`, nới `edit`) · `Services/Product/ProductWriteService.php` (`take()`, `assertCanEditAdmin()`, `updateAdmin()`; tái dùng `writeAdmin`) · `Http/Requests/Product/ProductRequest.php` (tách `checkClusters` dùng chung) · `Transformers/Product/ProductListResource.php` + `ProductDetailResource.php` (`can_edit` mở cho công ty lấy về, `can_take`, `edit_scope`) · `Transformers/Product/ProductFormResource.php` (`edit_scope`, `owner_company_id`) · `Services/Product/ProductService.php` (Kho lọc `status <> 0` nếu Q4 = ⭐; lọc "Dùng cho nhóm máy/máy" cho popup Công ty khác nếu làm) |
| Không đụng | migration, seeder, quyền (1652 có sẵn) ⇒ **không chạy gì vào DB** |

FE (tham khảo, khảo sát riêng): `components/product/ProductListPage.vue` (nút Lấy về dòng + thanh *Lấy về công ty* ở Kho), `pages/master-data/products/entering.vue` (nút *Xem hàng hoá Công ty khác* + popup mới), `pages/master-data/products/_id/edit.vue` + `components/product/form/ProductForm*.vue` (chế độ chỉ tab Quản trị), `pages/master-data/products/_id/index.vue` (footer Sửa).

### 6.3 PHPUnit tối thiểu (`DatabaseTransactions` + `ActsAsProductUser`, có quyền + không quyền bắt buộc)

**Lấy về**
1. Cty B có 1652 lấy 1 mã của Cty A chưa có dòng ⇒ 1 dòng `company_id = B` (= `company_role`, khác `info->company_id`), `coefficient = 1`, `status = 1`; `products` không đổi cột nào (so snapshot).
2. Mã có dòng hệ số cũ `status NULL, coefficient 1.03` ⇒ UPDATE `status = 1`, **`coefficient` vẫn 1.03**, số dòng không tăng.
3. Lô hỗn hợp: status 0 · hàng của chính B · đã có dòng `status` 3 · mã hợp lệ ⇒ chỉ mã hợp lệ vào `taken`, 3 mã còn lại vào `skipped` đúng lý do; dòng status 3 không bị lùi.
4. 101 mã ⇒ 422; mảng rỗng ⇒ 422.
5. **Không quyền 1652** ⇒ 403, 0 dòng ghi. 1652 chỉ có ở công ty KHÁC công ty đang làm việc ⇒ 403 (R22).
6. Sau lấy về: `/entering` + `/company` của B có mã; `/warehouse?usage=unused` của B không còn; `/trading` không có.
7. Lấy về 2 lần ⇒ lần 2 `skipped` "đang dùng rồi", không 500.

**Sửa tab Quản trị (công ty lấy về)**
8. B đã lấy về ⇒ `PUT /{id}/admin-data` ghi 4 ô + NCC + catalog của B; dòng/NCC/catalog của A không đổi; `coefficient` + `status` không đổi.
9. B gửi kèm `name` / `units` / `tech_coefficient` ⇒ 403, không ghi gì.
10. B gọi `PUT /{id}` (đầy đủ) ⇒ 403; `GET /{id}/edit` ⇒ 200 với `edit_scope = admin`.
11. B **chưa** lấy về ⇒ `admin-data` 403; `products.status = 0` ⇒ 403; dòng status 4 ⇒ 403.
12. B không 1652 ⇒ 403 cả `edit` lẫn `admin-data`.
13. Thiếu catalog ⇒ 422 (C1); Tiểu mục nhánh khoá thêm mới ⇒ 422, nhánh khoá đã lưu giữ được (D3).
14. `can_edit` / `can_take` ở list + chi tiết: chủ, công ty lấy về, công ty chưa dùng, không quyền.

**Kho (nếu Q4 = ⭐)**: 15. `/warehouse` không trả hàng `status = 0`, vẫn trả status 2/5 với `can_take = false`.

---

## 7. Câu hỏi cho user (hỏi lần lượt — chỉ điểm chưa có chốt)

### Q1. Lấy về mã đã có **dòng hệ số cũ** (chi nhánh đang bán thật ở ERP — 803 mã của Cty 2/3/4) thì đặt trạng thái gì?

Bối cảnh: dòng hệ số cũ chứng tỏ chi nhánh đã bán mã này (ERP nhân hệ số vào giá popup). 2-A K1 hoãn việc sinh trạng thái cho chi nhánh tới lúc backfill; 2-C1 với **chủ** thì dòng cũ `status NULL` được đưa về **3** khi lưu tab Quản trị (`ProductWriteService.php:415-417`, theo G4).

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **1 Đang nhập thông tin** như mọi mã lấy về (mockup, `yeu-cau-ghi.md` §1.8) | luật đơn giản, 1 nhánh code; mã chi nhánh đang bán treo ở *Nhập thông tin* tới phase Tính giá (H1'), không vào *Hàng đang kinh doanh* của chi nhánh — nhưng hiện nay chúng cũng chưa vào (đang "Chưa sử dụng") nên không lùi gì |
| (b) **3 Đang kinh doanh** khi đã có dòng hệ số cũ, 1 khi chưa có | khớp thực tế ERP + khớp cách 2-C1 xử lý dòng cũ của chủ; nhưng là backfill từng phần do người bấm (K1 đã hoãn backfill chi nhánh), và tạo 2 luật khác nhau cho cùng nút |

### Q2. Lúc lấy về, 4 ô quản trị (Chính sách KD, Tồn tối thiểu, Bảo hành, Đơn vị BH) của dòng công ty mình ghi gì?

Bối cảnh R7: trước khi lấy về, danh sách/chi tiết của công ty B đang hiện bảo hành + tồn tối thiểu lấy từ **cột chung** `products.*` (đường lùi `AdminData::source`), và ERP cũng đang dùng cột chung đó cho mọi công ty (N1). Có dòng rồi thì không lùi nữa.

| Đáp án | Hệ quả |
|---|---|
| (a) Để trống (NULL) | đơn giản; nhưng ngay sau bấm Lấy về cột *Bảo hành / Tồn tối thiểu* của B **đổi từ có giá trị → trống** ở mọi màn, B phải khai lại; ERP vẫn dùng cột chung nên 2 bên lệch |
| ⭐ (b) **Chép giá trị đang hiện cho B** = `products.guarantee`, `guarantee_type`, `min_stock_qty`; Chính sách KD để trống (chưa có nguồn) | không đổi gì trên màn khi bấm Lấy về; khớp cái ERP đang áp cho B; không ghi kép (G5 chỉ cấm GHI sang cột chung) |
| (c) Chép từ dòng của **công ty tạo** (nếu có), không thì cột chung | mang luôn Chính sách KD của công ty tạo — nhưng chính sách kinh doanh là của từng công ty, chép sang dễ sai nghĩa |

### Q3. Có cho lấy về hàng mà **công ty tạo vẫn đang *Đang nhập thông tin*** (hàng HRM mới tạo, chưa qua tính giá)?

G9b chỉ chặn `products.status ≠ 1`; hàng HRM tạo luôn `products.status = 1` (G1) nhưng dòng của chủ = 1 và theo H1' treo ở 1 tới phase Tính giá.

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **Cho lấy về** (mọi mã `products.status = 1`, không xét trạng thái ở công ty tạo) | đúng mockup Kho (nút hiện ở mọi dòng "công ty mình chưa dùng"); công ty khác có thể lấy về khi thông tin chung còn đang khai dở — thông tin đó đổi theo khi chủ sửa (tham chiếu, không chép — A2) |
| (b) Chỉ cho lấy về khi công ty tạo đã ở *Đang kinh doanh* (3) | chặn lấy hàng chưa hoàn thiện; nhưng vì H1' **không hàng HRM mới nào lấy về được** trong Phase 2, chỉ lấy được hàng ERP cũ (suy ra 3) |

### Q4. Kho dữ liệu đang hiện 17.512 hàng ERP đã xoá/khoá (`products.status = 0`) với nhãn "Chưa sử dụng" — xử lý thế nào? (tồn nhỏ ghi ở `chot.md`, hẹn chốt lúc plan 2-C2)

| Đáp án | Hệ quả |
|---|---|
| ⭐ (a) **Lọc bỏ hẳn** khỏi Kho (`products.status <> 0`), giữ 7 mã status 2/5 như ERP | Kho còn 28.378 mã; khớp ERP danh sách chính, khớp popup catalog (B5)/D2/G9b; muốn tra hàng đã xoá thì vẫn mở ERP (tab Đã xoá) hoặc mở chi tiết theo đường dẫn |
| (b) Ẩn mặc định + công tắc "Hiện cả hàng đã xoá ở ERP", nhãn riêng *Đã xoá ở ERP* (xám) | giữ được tra cứu trong HRM; thêm 1 ô lọc + 1 nhãn |
| (c) Giữ nguyên, chỉ đổi nhãn thành *Đã xoá ở ERP* | 38% kho là hàng không dùng được; công tắc "chưa dùng" vẫn đầy hàng đã xoá |
