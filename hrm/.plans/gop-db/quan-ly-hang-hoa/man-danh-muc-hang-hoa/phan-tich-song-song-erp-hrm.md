# Phân tích: chuyển quyền GHI hàng hoá từ ERP sang HRM (21/09/2026)

> **Hướng user chốt 21/09/2026:**
> *"Toàn bộ các luồng chức năng ghi vào hàng hoá tôi sẽ chuyển sang HRM. ERP sẽ chỉ dùng hàng hoá
> chứ không ghi nữa."*
>
> **Đính chính của user:** `Modules/Finance` của HRM là phân hệ **Tài chính**, **KHÔNG phải kho**.
> Quản lý kho vẫn ở ERP.

---

## 0. Kết luận

Tuyên bố *"ERP chỉ đọc, không ghi"* là **hướng đúng và làm cho mọi rủi ro song song biến mất ở
trạng thái cuối**. Nhưng có 2 điều cần chốt trước khi coi là xong:

1. **Phạm vi lớn hơn màn hàng hoá nhiều lần** — có **16 nơi** trong ERP đang ghi vào bảng hàng hoá
   và bảng vệ tinh, không phải 3.
2. 🔴 **Luồng Tính giá (`PriceCalculate`) đang GHI GIÁ vào hàng hoá** — 3.120 phiếu, bản ghi mới
   nhất **14/09/2026**. Luồng này thuộc Mua hàng/Đặt hàng (user nói ở lại ERP), nhưng việc nó làm
   đúng là *đặt giá bán cho hàng hoá*. **Hoặc nó cũng chuyển, hoặc phải là ngoại lệ được phép ghi.**

Và dù đích đến là ERP chỉ-đọc, **giai đoạn chuyển tiếp (Phase 2 → Phase 6) vẫn là ghi song song** —
các rủi ro ở §3 vẫn có thật trong khoảng đó.

---

## 1. HRM đang dùng hàng hoá thế nào

| | Số đo |
|---|---|
| Số chỗ HRM truy vấn `products` | **484 chỗ / 63 file** |
| Module đụng nhiều nhất | `Modules/Finance` **39 file** (Tài chính) · `Modules/Assign` 13 · `Modules/CustomerCare` 11 |
| Model HRM map vào `products` ("model cũ") | `Modules/Human/Entities/TpProduct.php` · `Modules/CustomerCare/Entities/Service/ErpProduct.php` |
| Cách truy cập chủ đạo | **query thô** `DB::table('products')` |
| Số chỗ HRM **GHI** vào `products` | **0** — đã kiểm kỹ, 2 kết quả khớp đều là dương tính giả |

> ✅ Sửa lại nhận định sai ở bản trước: tôi mô tả `Modules/Finance` là "phân hệ kho". Sai — đó là
> **Tài chính**. Nó chỉ ĐỌC hàng hoá để lấy `code`/`name`/`avatar`/`model_id` cho chứng từ, và ghi
> `stocks.accounting_qty` (số kế toán), không ghi `products`.

**Tiền lệ đáng học trong HRM** — `Modules/Finance/Entities/ProductImport/ProductImport.php:544-554`:

> *"Cơ chế giá vốn đơn vị SP (`products.units`, `product_versions`, `Product::getDataForVersion()`,
> `Product::createHistoryRecord()`) CŨNG CHƯA có Entity tương ứng ở `Modules/Finance` — nếu sau này
> ERP bật lại nhánh này thì phải port thêm các Entity đó (task riêng), **KHÔNG bịa bảng/cột ở đây**."*

Người viết trước đã gặp đúng ranh giới này và chọn dừng lại đúng chỗ. Phase 2 chính là lúc port các
Entity đó.

---

## 2. 🔑 Toàn bộ 16 nơi ERP đang GHI vào bảng hàng hoá

Đây là **phạm vi thật** của việc "chuyển toàn bộ luồng ghi sang HRM".

### Nhóm A — màn hàng hoá, đúng phạm vi đã biết

| # | Nơi ghi | Số chỗ | Phase |
|---|---|---|---|
| 1 | `Http/Controllers/ProductsController.php` | 11 | **Phase 2** |
| 2 | `app/Product.php` (`createRecord`, `generateCode`) | 3 | **Phase 2** (port sang service HRM) |
| 3 | `Services/Product/CreateProductService.php` | 2 | **Phase 2** |
| 4 | `Http/Controllers/Product2Controller.php` | 9 | ❓ màn hàng hoá "bản 2" — **cần xác nhận còn dùng không** |

### Nhóm B — luồng nghiệp vụ khác cũng ghi hàng hoá

| # | Nơi ghi | Số chỗ | Ghi gì | Ghi chú |
|---|---|---|---|---|
| 5 | `Sale/TmpProductsController.php` | 7 | duyệt hàng tạm → **tạo hàng hoá thật** | **8.931/45.890 = 19,5%** hàng hoá sinh từ đây · **Phase 6** |
| 6 | `ProductApprovesController.php` | 2 | **duyệt giá** hàng hoá | quyền `Duyệt giá hàng hoá` |
| 7 | 🔴 `Model/Order/PriceCalculate.php` | 1 | tạo `ProductVersion`, cập nhật `ProductUnitPrice`, `ProductExpectedPrice`, ghi `ProductHistory` | **luồng Tính giá — ĐANG SỐNG**: 3.120 phiếu, mới nhất 14/09/2026 |
| 8 | `Model/Product/ManufactureExpectPrice.php` | 1 | `ProductExpectedPrice` | giá dự kiến theo hãng — 87 dòng, mới nhất 2022 |
| 9 | `Model/Warehouse/ProductImport.php` | 1 | giá vốn theo giá NCC | ⚫ **dead code** — hàm gác cổng `return false` ngay dòng đầu; HRM đã port đúng hành vi "không làm gì" |
| 10 | `ExcelImports/ImportProductAttribute.php` | 1 | `AttributeProduct` | nhập Excel thuộc tính |
| 11 | `Jobs/GenerateProduct.php` | 2 | `AttributeProduct::insert` | **job nền** |
| 12 | `Jobs/CreateProductUnitsAfterMapping.php` | 2 | `AttributeProduct::insert` | **job nền** |
| 13 | `Jobs/UpdateGenerateProduct.php` | 2 | | **job nền** |

⚠️ **3 job nền (#11-13) là chỗ dễ bỏ sót nhất** — chúng chạy ngoài request, không có màn nào gọi
trực tiếp, nên rà theo màn sẽ không thấy.

### Nhóm C — thuộc nhóm GIỮ NGUYÊN ERP (mục C của `design.md`)

| # | Nơi ghi | Số chỗ | Ghi chú |
|---|---|---|---|
| 14 | `ProductTemplatesController.php` | 6 | **Hàng hoá gốc** — giữ ERP |
| 15 | `ProductInfoController.php` | 5 | **Hàng hoá có sẵn** — giữ ERP |
| 16 | `Services/ProductInfo/SyncProductInfoService.php` | 2 | **Đồng bộ hàng hoá** — giữ ERP |

⚠️ Nhóm C ghi vào bảng **riêng của chúng** (`product_templates`, `product_infos`, `pi_*`) — nhưng
phải kiểm từng chỗ xem có đụng sang `products` không. Nếu có thì mâu thuẫn với "ERP không ghi nữa".

---

## 3. Rủi ro trong GIAI ĐOẠN CHUYỂN TIẾP (Phase 2 → Phase 6)

Đích đến là ERP chỉ-đọc, nhưng từ lúc Phase 2 xong tới lúc Phase 6 xong thì **vẫn ghi song song**.
Nhịp độ thật: **~700–1.100 hàng hoá mới mỗi tháng** (2026-08: 1.106 · 2026-07: 647 · 2026-06: 779).

### 3.1 🟡 Va chạm MÃ hàng hoá

Mã sinh trong `Product::generateCode()` (`app/Product.php:2207`):

```
MÃ-HÃNG-SX + '-' + (tên barcode | tên model)   → cắt 32 ký tự
while (Product::where('code',$code)->exists()) { thêm ':01', ':02'… }
```

Mã thật: `CH-RRI32` · `SG-VT-NM0102` · `HN-90915-YZZE1:01`.

| | |
|---|---|
| Mã phải thêm hậu tố chống trùng | **7.928 / 45.890 = 17%** |
| `products.code` có UNIQUE | **CÓ** (`products_code_unique`) · 0 mã đang trùng |

Hai tiến trình cùng chạy vòng `while … exists()` có thể cùng chốt một mã. Nhờ UNIQUE nên **không
sinh dữ liệu hỏng**, nhưng bên chậm hơn nhận `Duplicate entry` giữa lúc bấm Lưu.

**Xử lý:** HRM port `generateCode()` **nguyên văn** + bắt `QueryException` 23000 rồi sinh lại mã
(retry 3–5 lần). Rủi ro này **tự biến mất** khi ERP hết ghi.

⚠️ **Mockup đang vẽ mã `TP.0012345` — SAI khuôn thật**, phải sửa thành dạng `CH-RRI32`.

### 3.2 🔴 Lịch sử và phiên bản — rủi ro nặng nhất, KHÔNG tự biến mất

| Bảng | Số dòng | Mới nhất |
|---|---|---|
| `product_histories` | **319.303** | 15/09/2026 |
| `product_versions` | **113.768** | 15/09/2026 |

ERP ghi 2 bảng này **rải rác trong controller** (26 chỗ `ProductHistory::`, 30 chỗ
`ProductVersion::` trên 8–11 file), **không qua observer**. HRM viết service mới sẽ **không ghi**,
mà **không có lỗi nào báo ra**.

Đây là rủi ro tồn tại **cả sau khi ERP hết ghi** — vì nó là việc HRM phải làm, không phải việc ERP
thôi làm.

### 3.3 🟡 Audit `updated_by`

`products.updated_by` có giá trị ở **45.889/45.890** dòng. `Product` của ERP **không**
`extends BaseModel`, nên HRM phải **tự gán** ở mọi đường ghi — kể cả **khoá / mở khoá**, chỗ hay
quên nhất. Dùng `auth()->id()` (= `employees.id`), **không** dùng `auth()->user()->info->id`.

### 3.4 🟡 484 chỗ HRM đọc bằng query thô

Khi Phase 2 thêm cột hoặc đổi ngữ nghĩa, **không có model tập trung** để sửa một chỗ — phải rà 63
file. Hai model cũ chỉ phủ một phần nhỏ.

**Đề xuất:** Phase 2 dựng **một Entity `Product` dùng chung** trong `Modules/MasterData`, rồi các
phase sau dần chuyển 484 chỗ query thô sang dùng nó. Không làm hết trong Phase 2, nhưng có chỗ để
quy về.

---

## 4. Việc phải sửa bên ERP

| # | Việc | Bắt buộc? | Vì sao |
|---|---|---|---|
| 1 | **Bỏ 2 điều kiện lọc enum cũ trong `SearchController`** | **CÓ** | Hàng hoá tạo từ HRM có `product_type` trống sẽ **biến mất khỏi popup của 338 màn** (`NULL <> 'x'` → NULL → loại dòng) |
| 2 | **Gỡ đồng bộ CRM nhánh hàng hoá** (13+ model) | đã chốt | Luồng ngừng từ 08/10/2025. ⚠️ Giữ nhánh nhân sự |
| 3 | **Gỡ/chuyển 13 nơi ghi ở nhóm A + B** | theo lộ trình | Chính là nội dung "ERP không ghi nữa" |
| 4 | Xác nhận **`Product2Controller`** còn dùng không | cần biết | 9 chỗ ghi |
| 5 | Kiểm nhóm C có đụng sang `products` không | cần biết | Nhóm này ở lại ERP |
| 6 | Sau khi chuyển xong: **khoá đường ghi** (gỡ route / bỏ quyền `Thêm hàng hóa`, `Sửa hàng hóa` bên ERP) | nên | Nếu không, đường cũ vẫn mở và có người dùng lại |

---

## 5. Nguyên tắc đề xuất

> **Trong lúc chuyển:** HRM ghi **y hệt** những gì ERP đang ghi — không thêm, không bớt.
> **Sau khi chuyển xong:** khoá hẳn đường ghi bên ERP, không để hai nơi cùng ghi "cho chắc".

Danh sách kiểm khi viết `ProductService` bên HRM — đối chiếu với `ProductsController@update`
(882 dòng) và `Product::createRecord()`:

- [ ] sinh mã theo `generateCode()` + retry khi trùng
- [ ] ghi `product_versions`
- [ ] ghi `product_histories` (kèm `product_version_id`)
- [ ] `created_by` / `updated_by` — cả ở khoá/mở khoá
- [ ] `product_units` · `product_unit_prices` · `product_expected_prices`
- [ ] `attribute_products`
- [ ] `product_tech_attachments` · `product_galleries` · `product_videos`
- [ ] 4 bảng hàng hoá kèm · `product_suppliers` · `product_company_coefficients`
- [ ] cột mới `product_type_id` · `product_characteristic_id`

---

## 6. Câu cần chốt

### ✅ Đã chốt 21/09/2026 (bổ sung sau bản đầu)

| Câu | Chốt |
|---|---|
| Luồng Tính giá | **Chuyển sang HRM** → tách thành **Phase 7** (4 controller 1.160 dòng · 3 model 2.271 · 18 view 2.413 · 39 route · dữ liệu sống tới 14/09/2026) |
| Lịch sử chỉnh sửa hàng hoá | **Làm theo cách mới của HRM** — `catalog_histories`, không ghi `product_histories` |
| Version hàng hoá | **BỎ** — `product_versions` chỉ là cái nhóm thay đổi của một lần lưu, mà `catalog_histories` đã gom sẵn trong một dòng |

⇒ Rủi ro §3.2 (*"lịch sử đứt"*) **không còn là rủi ro** mà thành **thiết kế có chủ ý**: HRM ghi
lịch sử theo cách của mình. Nhưng phát sinh 2 việc mới — xem §6 câu 1 và 2.

### Còn lại cần chốt

| # | Câu hỏi | Vì sao quan trọng |
|---|---|---|
| 1 | **Log bảng con thế nào?** `catalog_histories` hiện chỉ log cột phẳng; hàng hoá có ĐVT · giá × 6 loại · thuộc tính · 4 bảng hàng hoá kèm · ảnh/video/tài liệu | Ghi tóm tắt ("đổi 3 dòng giá") hay liệt kê từng dòng — ảnh hưởng cả cách đọc lẫn khối lượng dữ liệu |
| 2 | **Màn "Lịch sử chỉnh sửa hàng hóa" bên ERP** (`productHistory`) xử lý sao? | Sẽ không thấy thay đổi từ HRM. Gỡ hẳn, hay để lại làm kho tra cứu lịch sử CŨ (319.303 dòng)? |
| 2 | **`Product2Controller`** (route `product2.*`) còn dùng không? | 9 chỗ ghi — nếu còn thì là màn hàng hoá thứ hai phải chuyển |
| 3 | **Lịch sử ghi vào đâu?** `product_histories`/`product_versions` sẵn có của ERP, hay `catalog_histories` của HRM? | ERP vẫn **hiển thị** màn lịch sử hàng hoá. Dùng bảng HRM thì lịch sử tách 2 nơi, tra cứu phải nhìn 2 màn |
| 4 | **3 job nền** (`GenerateProduct`, `UpdateGenerateProduct`, `CreateProductUnitsAfterMapping`) chạy cho nghiệp vụ nào? | Ghi ngoài request, rà theo màn không thấy |
| 5 | **Thứ tự chuyển** giữa Phase 2 và Phase 6 (hàng tạm, 19,5% hàng hoá)? | Quyết định giai đoạn ghi song song dài hay ngắn |
