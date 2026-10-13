# Phase 2 — Màn danh mục hàng hoá (danh sách + tạo/sửa)

> Chưa fill — đang chờ tài liệu yêu cầu của khách để dựng mockup.
> Khảo sát ERP đã xong: `khao-sat.md`.

> 📄 **Spec kỹ thuật đầy đủ** (schema · API contract · validate · quyền · hiệu năng):
> `docs/superpowers/specs/gop-db/2026-09-21-man-danh-muc-hang-hoa-design.md`.
> File này giữ phần **thiết kế + quyết định**; spec giữ phần **làm thế nào**.

## Nguồn yêu cầu

Tài liệu khách (user đưa 21/09/2026): màn Danh mục hàng hoá **6 tab** — Thông tin chung · Thông số
kỹ thuật · Kỹ thuật · Mua hàng · Dữ liệu quản trị · Giá bán. Nguyên văn lưu ở `yeu-cau-khach.md`.

## Quyết định đã chốt (user, 21/09/2026)

### 1. 8 trường ERP mà tài liệu không liệt kê → GIỮ, xếp vào tab hợp lý
Trọng lượng · Kích thước · Serial number · % giảm giá thanh lý · Nhóm máy/Máy · checkbox thuế BVMT ·
Trạng thái. (Tài liệu liệt kê thiếu chứ không có ý bỏ.)

### 2. Tab 5 + tab 6 "theo từng công ty" → TÁCH SANG PHASE 3
Phase 2 dựng đủ 6 tab nhưng tab 5/6 chạy trên cấu trúc hiện có (một bộ chung). Lý do: `product_units`
(giá vốn / giá mua ngoài) bị ERP đọc ở **119 file / 453 chỗ**, `product_prices` **33 file**,
`min_stock_qty` **42 file** — chèn dòng theo công ty vào bảng cũ sẽ làm truy vấn "lấy dòng mới nhất
theo `launch_date`" của ERP **vớ phải giá của công ty khác**, sai tiền âm thầm. Phase 3 vốn đã là
"phân quyền hàng hoá theo công ty" nên gom vào đó.

### 3. `product_cate` ("Loại hàng hóa") → ĐÓNG BĂNG, thay bằng Chính sách kinh doanh

Bỏ ô khỏi form HRM; **hàng hoá tạo từ HRM để cột này TRỐNG**. Việc xoá cột + xử lý ảnh hưởng để
một phase sau.

> 📌 **Sửa lại 21/09/2026 (chiều):** bản chốt đầu ghi *"vẫn tự điền cột cũ khi lưu"*, tức vẫn cần
> một bảng ánh xạ. Sau khi user loại hẳn phương án ánh xạ ở quyết định 6, tôi đo lại và thấy
> **`product_cate` không cần ánh xạ** — để trống là an toàn:
>
> | Điều kiện an toàn | Kết quả đo |
> |---|---|
> | Nhánh nghiệp vụ theo giá trị | **0 chỗ** |
> | Chỗ lọc **vô điều kiện** (làm hàng biến mất khỏi danh sách) | **không có** — mọi chỗ đều bọc `if (!empty($request->...))` |
> | Chỗ đọc vô điều kiện duy nhất | lệnh chạy theo lịch `product:reset_price_when_zero_inventory` (`whereNotNull('product_cate')`, `Kernel.php:100`) — **0/8 công ty** bật cấu hình này |
> | Đã có hàng hoá để trống sẵn | **640 hàng hoá** |
>
> Khác với `product_type`: cột đó **bắt buộc** phải xử lý vì có dòng lọc vô điều kiện
> `!= 'service_product'` (xem 6a).

**Căn cứ đo được:**
- Bản chất: **enum cứng** khai ở `app/Product.php:250`, chưa từng là bảng. 11 giá trị đang bật.
  Gần như đơn trị: 44.755 hàng hoá chọn 1 giá trị, 291 chọn 2, 640 trống.
- **0 chỗ** rẽ nhánh nghiệp vụ theo giá trị → bỏ không làm sai phép tính nào.
- Lan ra **5 bảng**: `products` 45.890 · `product_templates` **29.813 (nhóm GIỮ NGUYÊN ERP)** ·
  `tmp_products` 1.957 · `product_infos` 0 · `product_approves` 0.
- Là chiều lọc + chiều phân tổ: `SearchController` 5 chỗ, `StockPosition` 2, `ProductApproves` 2,
  **12 service báo cáo** (`MarketCommodityMarketReportService` nhóm theo nó), 110 file view,
  3 file import Excel, **11.372 dòng** `product_histories`.
- Rủi ro vỡ logic THẤP · khối lượng sửa TRUNG BÌNH · rủi ro nghiệp vụ CAO (báo cáo đổi ý nghĩa khi
  giá trị thành theo-công-ty).

### 4. `can_retail` → BỎ hẳn
Không dùng nữa. Chuỗi cũ: `Product::getCanRetailAttribute()` (suy từ `product_type`) →
`QuotationProduct::can_retail` → `Quotation::can_retail` → chặn `canCreateSaleOrder()`.
- `canCreateSaleOrder` thuộc `QuotationsController` — **user xác nhận đã bỏ dùng từ lâu**.
- `canCreateLiquidationOrder()` đã chết sẵn (`return true;` đặt trước dòng điều kiện).
- `groups.can_retail` chỉ **3/893 nhóm** bật.
- ⇒ Gỡ luôn ô `can_retail` khỏi màn Loại sản phẩm của Phase 0 (bảng đang trống, chưa ai nhập).

### 5. Quy chế (`regulation_product_types`) → KHÔNG phải ràng buộc, bỏ qua
Đường tính hoa hồng lọc theo tính chất hàng hoá **chỉ tồn tại ở service đã chết**.

| Service | số chỗ `whereHas('productTypes')` | Trạng thái |
|---|---|---|
| `SupportAccountingService` | 2 | 💀 `contracts` 1 dòng từ 11/01/2024, `service_contracts` 0, `rule_contracts`/`liquidation_*` không có bảng |
| `FirmSupportAccountingService` | **0** | 🟢 `firm_contracts` 25.865 dòng, mới nhất 15/09/2026 |
| `ZTFirmSupportAccountingService` | **0** | 🟢 sống |
| `WarrantyRepairSupportAccountingService` | **0** | 🟢 sống |

Luồng Firm vẫn gom `$product_types` (dòng 380) và truyền vào
`getDepartmentImplement(..., $product_types = [])` nhưng **bên trong không dùng** — tham số chết.
Nên 386 quy chế `condition_type = 1` + 1.127 dòng `regulation_product_types` không còn tác dụng.

⚠️ Ghi để không quên: `SupportAccountingService` vẫn được **52 file** import (kể cả controller luồng
Firm) — đừng nhìn danh sách import mà kết luận nó còn sống; phải xem service nào thực sự chạy.

### 6. `product_type` ("Tính chất hàng hóa") → KHÔNG ánh xạ. Bỏ lọc theo loại cũ, sau này lọc theo danh mục mới

User chốt 21/09/2026: **loại phương án ánh xạ** — "lâu dài không duy trì cách khai báo như vậy
được, loại cũ không còn cần nữa". Thay vào đó **sửa chỗ lọc cho đúng**: bỏ hoàn toàn điều kiện lọc
theo enum cũ, sau này thay bằng lọc theo danh mục mới.

#### 6a. Vì sao KHÔNG được để `product_type` trống mà không sửa gì

`SearchController` có dòng lọc **vô điều kiện**, lặp ở **cả 4 hàm**:

```php
$products = $products->where('product_type', '!=', 'service_product');
```

Đã chạy thử trên MySQL: `SELECT (NULL <> 'service_product')` → **NULL**, mà `WHERE NULL` thì **loại
bỏ dòng**. Nên hàng hoá có `product_type` trống sẽ **biến mất khỏi popup tìm hàng của 338 màn**,
không lỗi, không cảnh báo — người dùng tưởng gõ sai mã.

| Endpoint | Route | Số file gọi |
|---|---|---|
| `searchProduct` | `/searchProduct` | **338** |
| `searchProductStockBuyer` | `/searchProductStockBuyer` + 1 route API | 6 |
| `searchProduct2` | `/searchProduct2` | 6 |
| `searchProductStockBuyerApi` | — | 0 (không nơi gọi) |

#### 6b. Tách làm 2 việc — Phase 2 KHÔNG bị chặn

- **Làm được ngay:** *bỏ* 2 điều kiện cứng. Bỏ điều kiện thu hẹp thì kết quả chỉ rộng ra, và chữa
  luôn lỗi `NULL <> 'x'` ⇒ hàng hoá tạo từ HRM hiện bình thường ở 338 màn.
- **Để sau:** *thay bằng* lọc theo danh mục mới — cần cây có dữ liệu và 45.890 hàng hoá đã được gán.

⚠️ **Cần khách xác nhận trước khi bỏ** (đổi hành vi ERP đang chạy):

| Bỏ điều kiện | Hệ quả ngay |
|---|---|
| `!= 'service_product'` | 30 hàng hoá làm dịch vụ xuất hiện trong mọi popup của 338 màn |
| `is_service_quotation → whereIn(['accessories','lubricant'])` | Báo giá dịch vụ chọn được **toàn bộ 45.890** thay vì **12.426** phụ kiện/dầu nhớt |

#### 6c. BA ngữ nghĩa cần chỗ đứng mới trong cây phân loại

Bỏ enum cũ thì 3 hành vi sau mất chỗ bám. Đây là **cờ nghiệp vụ**, không phải cấp phân loại — đề
xuất làm **3 checkbox trên danh mục Loại sản phẩm** (nơi Phase 0 đã đặt sẵn `serial_required`,
`vat_percent_tax_rate_id`), thay vì suy từ tên nhánh.

| # | Ngữ nghĩa | Dựa vào enum cũ | Quy mô | Nếu không có thay thế |
|---|---|---|---|---|
| 1 | "Hàng hoá làm dịch vụ" — luôn ẩn khỏi mọi popup chọn hàng | `service_product` | 30 | 30 hàng hoá lọt vào popup của 338 màn |
| 2 | "Được chọn khi lập báo giá dịch vụ" | `accessories` + `lubricant` | 12.426 | báo giá dịch vụ chọn được cả 45.890 |
| 3 | **"Là thiết bị của khách hàng"** | danh sách trắng 5/15 giá trị: `tool_and_device`, `product`, `tool`, `accessories`, `product_wait_build` | **40.175 (88%)**, loại 5.715 vật tư/dầu nhớt/hoá chất | thiết bị mới không hiện ở màn bảo hành, hoặc 5.715 vật tư lọt vào danh sách thiết bị |

⚠️ Ngữ nghĩa 3 **khác** ngữ nghĩa 1: chỗ này không phải lỗi mà là **thu hẹp có chủ ý**, nên không
thể chỉ "bỏ điều kiện" như ở `SearchController`.

**Ngữ nghĩa 3 dùng ở 9 chỗ đang sống** — `Customer::getListProductOfCustomer()`:
`WarrantyRepairRequest` · `WrServiceQuotation` (3) · `WrAssignTask` · `WrImportResult` ·
`WrApproveResults` · 2 màn qua route `customerManager.getListProductOfCustomer` (**Yêu cầu bảo
hành**, **Báo giá dịch vụ**). Dữ liệu sống: `external_equipments` 2.703 dòng, mới nhất 15/09/2026.
`WrAssignTask → ProductExportRequest::getReportDetailData3()` dùng đúng danh sách trắng đó.

#### 6d. Danh sách chỗ phải chuyển sang danh mục mới

**Nhóm A — cơ học (10 chỗ):** lọc pass-through `where('p.product_type', $request->product_type)` —
`Product.php` 9 chỗ (báo cáo/tra cứu) + `ProductsController:2494`. Đổi cột + đổi nguồn option.

**Nhóm B — nhánh cứng, cần chốt ngữ nghĩa (12 chỗ, TẤT CẢ đang sống):**

| Nơi | Số chỗ | Bằng chứng còn sống |
|---|---|---|
| `SearchController` (4 hàm) | 9 | 338 file gọi |
| `Customer::getListProductOfCustomer` | 2 | `external_equipments` 2.703 dòng, mới nhất 15/09/2026 |
| `WrAssignTask` | 2 | `wr_assign_tasks` 16.734 dòng, mới nhất 15/09/2026 |
| ~~`SummarySaleReportService`~~ | ~~2~~ | **Xếp lại sang nhóm A** — chỉ lọc khi người dùng chọn `filter_type == 'product_type'` (mặc định `tire_making_materials`), là lọc pass-through chứ không phải nhánh cứng |

**Nhóm C — KHÔNG đụng:**
- `ProductTemplate.php` (8 chỗ) · `ProductInfo.php` (9 chỗ) — bảng `product_templates` /
  `product_infos`, thuộc nhóm **GIỮ NGUYÊN ERP**, enum riêng.
- `where('product_type', 'no_sale')` ở 3 controller — **0 hàng hoá** mang giá trị này.
- Quy chế · `can_retail` — đã chốt bỏ (mục 4, 5).

**Ngoài ra:** 176 file view hiển thị nhãn tính chất hàng hoá, đang đọc từ mảng nhãn cứng trong
model — sẽ phải đổi sang đọc danh mục.

### 7. 🔜 NOTE ĐỂ XỬ LÝ SAU (user chốt 21/09/2026)

1. **Quy đổi 45.890 hàng hoá cũ sang cây phân loại mới.** Hiện 45.890/45.890 có `product_type` cũ
   và **0** có phân loại mới (cột chưa tồn tại, 6 bảng cây đang 0 dòng). Thứ tự bắt buộc khi làm:
   thêm cột `product_type_id` → nghiệp vụ nhập cây → quy đổi dữ liệu → **rồi mới** bật lọc mới.
   Bật lọc mới trước khi quy đổi = 338 màn không tìm thấy hàng nào.
   Ba cách đã nêu để chọn sau: màn *Cập nhật nhanh hàng hoá* (gán hàng loạt) · nhập Excel ·
   script quy đổi một lần từ 16 giá trị cũ.
2. **Thay các chỗ lọc sang danh mục mới** (nhóm A + B ở mục 6d) và 176 view.
3. **Xoá hẳn cột `product_cate`** + xử lý 12 báo cáo, 11.372 dòng lịch sử (mục 3).
4. **Ba cờ nghiệp vụ thay cho `product_type`** (§6c): hàng hoá làm dịch vụ · dùng cho báo giá dịch
   vụ · là thiết bị của khách hàng. User chốt 21/09/2026: cũng note xử lý sau.
5. **Gỡ `group_id`** khỏi form + chuyển ~116 chỗ đọc thuộc tính nghiệp vụ của nhóm sang cây mới +
   xoá cột (§8d).
6. **Rà 29 file ERP đọc `products.min_stock_qty`** sau khi cột bị xoá (user chốt 22/09/2026).
   Cùng nhóm việc với phần còn treo ở popup tìm kiếm hàng hoá (Phase 4). Danh sách file + cách
   chuyển sang bảng theo công ty: §24c.

### 8. `group_id` ("Nhóm hàng hoá", bảng `groups`) → note xử lý sau, TRỪ "Thông số cơ bản"

Bản chất khác hẳn `product_type` / `product_cate`: hai cột kia là **enum nhãn**, còn `groups` là
**bảng thật mang dữ liệu nghiệp vụ** — nhóm cấp giá trị mặc định cho hàng hoá.

| Cột `groups` | Có dữ liệu | Chỗ đọc `group->…` | Phase 0 có chỗ hứng chưa |
|---|---|---|---|
| `barcode_template_type` (mẫu in tem) | **893/893** | 23 | 🟢 `product_natures.barcode_template_type` |
| `vat_percent` + `vat_percent_tax_rate_id` | 892 / 879 | 15 | 🟢 `product_types.vat_percent_tax_rate_id` |
| `long_stock_days` (số ngày tính tồn lâu) | 751 | 6 | 🟢 trường trên Loại sản phẩm |
| `warning` / `user_manual` / `ingredient` | 40 / 59 / 0 | 14 / 14 / 14 | 🟢 đã chuyển sang Loại sản phẩm (QĐ #5 Phase 0) |
| `must_serial` | 0 | 12 | 🟢 `product_types.serial_required` |
| `rate_liquidation` | **0** | 18 | ⚫ **BỎ** (user chốt 21/09/2026) |
| `checksheet_id` | **0** | — | ⚫ **BỎ** (user chốt 21/09/2026) |
| `can_retail` | 3 | — | ⚫ đã bỏ ở QĐ 4 |

⚠️ **`rate_liquidation` tồn tại ở HAI bảng — chỉ bỏ một:**

| | Có dữ liệu | Xử lý |
|---|---|---|
| `groups.rate_liquidation` | 0 / 893 | 🟢 **BỎ** |
| `products.rate_liquidation` | **1.251 / 45.890** | ⚠️ **GIỮ** — chính là "% giảm giá thanh lý" trong 8 trường đã chốt giữ ở QĐ 1, nằm trên form hàng hoá |

#### 8a. Bỏ nhóm gây CRASH chứ không sai âm thầm

**Không một chỗ nào dùng `optional()` hay `?->`**:
`$this->group->rate_liquidation` (`Product.php:1261,1331` · `ProductInfo.php:743` ·
`ProductTemplate.php:1196`) · `$product->group->must_serial` (`BaseProduct.php:101`).
Hàng hoá không có nhóm ⇒ `Trying to get property of non-object`. Dễ phát hiện hơn nhưng gián đoạn ngay.

#### 8b. 13 bảng có FK trỏ `groups`

`products` 45.890 · `handover_acceptance_record_products` 27.310 · `service_has_products` 4.896 ·
`firm_contract_promotions` 4.091 + `firm_quotation_promotions` 2.061 (luồng Firm **đang sống**,
nhưng đã kiểm: **chỉ ghi vào, 0 chỗ đọc lại** `group_id` từ 2 bảng này) · **`attribute_groups`
2.434** · `product_group_classifies` 1.019 · `tmp_products` 1.957 · `quotation_products` 155 ·
`contract_products` 32 · 3 bảng 0 dòng.

Khối lượng: **422 file** nhắc `group_id`, ~116 chỗ đọc thuộc tính nghiệp vụ của nhóm.

#### 8c. ✅ PHẢI LÀM TRONG PHASE 2: "Thông số cơ bản" chuyển sang theo **Nhóm sản phẩm**

Hiện tại khối "Thông số cơ bản" của form hàng hoá đổ theo nhóm cũ:
`Sale/AttributesController:29` → `AttributeGroup::where('group_id', $groupId)->pluck('attribute_id')`
(bảng `attribute_groups`, 2.434 dòng).

**User chốt 21/09/2026: chuyển sang theo Nhóm sản phẩm** (`product_families`, cấp 3 của cây).

🔴 **Lệch với thứ Phase 0 đã dựng** — Phase 0 gắn thuộc tính ở cấp **Loại sản phẩm** (cấp 4):
- bảng nối `product_type_attributes` (`product_type_id`, `attribute_id`)
- ô "Thuộc tính" nằm trên màn `pages/master-data/product-types/` (index + modal)

⇒ Phải **nâng bảng nối lên một cấp** (`product_family_attributes`) và **chuyển ô "Thuộc tính"** từ
màn Loại sản phẩm sang màn Nhóm sản phẩm.

🟢 **Làm bây giờ là rẻ nhất, không mất dữ liệu**: `product_families` 0 dòng, `product_types` 0 dòng,
`product_type_attributes` 0 dòng. Để lâu, khi nghiệp vụ đã nhập cây, sẽ phải di trú dữ liệu.

Đây là việc **KHÔNG hoãn được** (khác mọi mục ở §7) vì "Thông số cơ bản" là một khối hiển thị ngay
trên tab 1 của form mới.

#### 8d. Phần còn lại của `group_id` → note xử lý sau
Gỡ ô Nhóm hàng hoá khỏi form, chuyển 116 chỗ đọc thuộc tính nghiệp vụ sang cây mới, xoá cột —
gộp vào danh sách tồn ở §7.

## Mockup (21/09/2026) — dựng thành TRANG NUXT THẬT, không phải HTML vẽ lại

| Màn | Đường dẫn xem |
|---|---|
| Danh sách hàng hoá | `http://127.0.0.1:3000/master-data/mockup-hang-hoa` |
| Tạo/Sửa hàng hoá (5 tab) | `http://127.0.0.1:3000/master-data/mockup-hang-hoa/form` |

File: `hrm-client/pages/master-data/mockup-hang-hoa/{index,form}.vue` — **dữ liệu tĩnh, không gọi
API, không ghi DB**. Xoá thư mục này sau khi chốt.

**Vì sao dựng bằng trang Nuxt thật chứ không phải HTML riêng:** CSS của hrm-client ở chế độ dev là
**1,9MB / 20.534 rule nhúng trong JS**, không tách ra file được; component lại dùng scoped style
(`data-v-…`). Chép tay ra HTML là chắc chắn lệch. Dựng bằng chính `V2BaseDataTable` /
`V2BaseSmartFilterPanel` / `V2BaseFormSection` / `V2Footer` / `b-tabs nav-bordered` thì cái nhìn
thấy **đúng là giao diện thật**.

### Màn danh sách — bộ cột mặc định (user chốt: theo cây phân loại mới)

STT · Ảnh · **Mã hàng hoá** (+ barcode ở dòng phụ) · Tên hàng hoá · Model · **Loại sản phẩm**
(+ đường dẫn 3 cấp cha ở dòng phụ) · Thương hiệu · ĐVT · % VAT · Trạng thái · Ngày sửa.
Các cột còn lại của ERP vẫn bật được qua "Cấu hình cột hiển thị".

Bộ lọc bỏ hẳn 3 ô cũ, thay bằng 4 ô theo cây (Tính chất → Nhóm chức năng → Nhóm sản phẩm → Loại sản
phẩm) + Thương hiệu · Hãng sản xuất · Xuất xứ · ĐVT · Công ty quản lý · Trạng thái.
⚠️ Trên **bộ lọc** cây đi xuôi từ gốc xuống lá (để lọc rộng); trên **form** thì ngược lại.

### Màn tạo/sửa — 5 tab (gộp tab "Kỹ thuật" vào "Thông số kỹ thuật")

| Tab | Khối |
|---|---|
| 1. Thông tin chung | Phân loại · Thông tin hàng hoá · Nguồn gốc · Thông số cơ bản · Tài liệu KT/Hình ảnh/Video |
| 2. Thông số kỹ thuật | Kỹ thuật (hệ số công nghệ, bảo hành) · Phụ kiện tiêu chuẩn/Đặc điểm · 4 khối hàng hoá kèm · Phụ tùng ô tô |
| 3. Mua hàng | Khai báo hải quan · Thuế |
| 4. Dữ liệu quản trị | Bảng theo công ty (🔜 Phase 3) |
| 5. Giá bán | Bảng giá theo công ty × thời gian (🔜 Phase 3) · Hệ số giá theo công ty |

**Khối "Phân loại" làm đúng tài liệu — cây đi NGƯỢC:** chỉ có **Loại sản phẩm** là ô chọn (bắt
buộc); Tính chất hàng hóa / Nhóm chức năng / Nhóm sản phẩm là **ô khoá**, tự hiện theo lựa chọn.

### Đã kiểm bằng Playwright trên trình duyệt thật (đo số từ DOM)

- Màn danh sách: **11 cột đúng tên**, 3 dòng dữ liệu, toolbar đủ Tạo mới / Import Excel / Xuất Excel
  / Cấu hình cột.
- Màn form: **5 tab**, 17 khối, 45 nhãn, footer có nút Lưu + Quay lại (cùng `y = 910`).
- **Bố cục: mở lần lượt cả 5 tab, đo từng `.form-row` → 0 hàng lỗi** (mọi hàng đủ 12 cột và các ô
  cùng một dòng). Lần đo đầu bắt được **4 hàng sai** (3 / 9 / 6 / 3 cột) → đã xếp lại.
- Console: chỉ còn 2 lỗi toàn cục của layout (`menu-settings` 400, avatar `e2e.png` 404) — đã chứng
  minh xuất hiện cả ở màn ngoài phase này. 2 cảnh báo là `vue-router` deprecation, không phải của
  màn.

### Sửa mockup vòng 2 (user góp ý 21/09/2026)

> *"Tab Thông tin chung: thêm card Đơn vị tính nằm trên card file đính kèm — tạo và cài đặt các đơn
> vị tính. Tab Giá bán: mỗi công ty có 1 tab riêng quản lý giá theo đơn vị. Tham khảo thiết kế quản
> lý đơn vị tính + các trường giá đang dùng bên ERP."*

#### a. Tab 1 — card "Đơn vị tính" (mới), đặt NGAY TRÊN card Tài liệu/Ảnh/Video

Bảng: **Đơn vị** · **Đơn vị cơ bản** (radio, chỉ 1) · **Hệ số quy đổi** (ĐVT cơ bản khoá = 1) ·
**Quy đổi** (dòng chữ `1 Thùng = 12 Cái`, copy cách ERP hiển thị) · nút xoá (ĐVT cơ bản không xoá
được). Nút **Thêm đơn vị tính** ở góc phải card.

Đã gỡ ô "Đơn vị tính" lẻ khỏi khối *Thông tin hàng hoá* (trùng việc), hàng đó chia lại `4+4+4`.

**Vì sao tách ĐVT khỏi phần giá** (ERP gộp chung trong khối "Giá theo đơn vị"): 98,7% hàng hoá chỉ
có 1 ĐVT nên khai ĐVT là việc thường ngày, còn đặt giá là việc của người có quyền `Quản lý giá` —
gộp chung buộc người khai hàng hoá phải đi qua màn giá.

#### b. Tab Giá bán — tab lồng 2 tầng: CÔNG TY → ĐƠN VỊ TÍNH

```
[Tân Phát] [Tân Phát ETEK]                     ← tầng 1: công ty
    Hệ số giá theo công ty: [1.00]             ← product_company_coefficients (dải inline)
    [Cái] [Thùng]                              ← tầng 2: ĐVT (in đậm = ĐVT cơ bản) — khuôn ERP
        Giá vốn · Giá mua ngoài · Hệ số tính ĐM hàng thúc đẩy bán · ĐM đàm phán giá thúc đẩy bán (%)
        ☐ Tính theo giá niêm yết (= % ĐM đàm phán × hệ số)     ← according_base_price
        ┌──────────────────────────────────────────────────────────────────────┐
        │ Loại giá │ Hệ số │ Giá bán │ ĐM đàm phán giá (%) │ Ngày hiệu lực     │
        │ Bán lẻ *          │ … │ … │ … │ Đang áp dụng                        │
        │  ↳ giá sẽ áp dụng │ … │ … │ … │ [01/11/2026] 🗑                      │
        │ Đại lý cấp 1/2/3, Giá bán theo lô …                                  │
        │ Giá bán TMĐT (online)  — KHOÁ, đồng bộ từ TMĐT                       │
        └──────────────────────────────────────────────────────────────────────┘
```

Bám đúng `form.blade.php:969-1150` của ERP: tab theo ĐVT, mỗi loại giá một dòng "Đang áp dụng",
bên dưới là các dòng **giá sẽ có hiệu lực** (`product_expected_prices`) có ô `effect_date` + nút xoá
và link **"+ Thêm giá hiệu lực"**. Loại giá **#6 (online) bị khoá** — ERP cũng
`ng-disabled="price.price_type_id == 6"`.

Khác ERP 2 điểm, đều theo quyết định đã chốt: **bỏ cột "Giá công thức"** (không có nguồn) và
**thêm tầng tab Công ty**.

"Hệ số giá theo công ty" để **dải inline** chứ không dựng `.form-row` — vì cấp công ty chỉ có đúng
1 trường, để trong lưới sẽ thành ô lẻ một dòng.

#### b2. Tab Dữ liệu quản trị — cùng khuôn tab theo CÔNG TY (user chốt 21/09/2026)

Bỏ bảng "mỗi công ty một dòng", đổi thành **tab theo công ty** giống tab Giá bán. Trong mỗi tab là
một card `Dữ liệu quản trị — <tên công ty>` với 3 trường (`6 + 3 + 3` = 12 cột):

| Trường | Kiểu | Lưu ở đâu hiện nay |
|---|---|---|
| **Nhà cung cấp** | **select NHIỀU** — ERP dùng `multiple` (`form.blade.php:1258`) | `product_suppliers` (**không có** `company_id`) — 1.740/45.890 hàng hoá có NCC; 1.739 hàng hoá 1 NCC, 1 hàng hoá 2 NCC |
| **Chính sách kinh doanh** | select | danh mục Phase 0 `business_policies` — thay cho enum cũ `product_cate` |
| **SL tồn kho tối thiểu** | số | `products.min_stock_qty` (**một cột đơn**, chưa theo công ty) |

Cả 3 nguồn đều chưa tách theo công ty ⇒ giao diện dựng trước, dữ liệu tách ở **Phase 3**.

#### c. Đo lại sau khi sửa

- Thứ tự khối tab 1: Phân loại · Thông tin hàng hoá · Nguồn gốc · Thông số cơ bản · **Đơn vị tính** ·
  Tài liệu kỹ thuật → đúng yêu cầu (ĐVT ở vị trí 5, tài liệu ở 6).
- Tab Giá bán: 2 tab công ty × 2 tab ĐVT; bảng giá 5 cột; 7 dòng (6 loại giá + 1 dòng hiệu lực).
- Tab Dữ liệu quản trị: 2 tab công ty, tiêu đề card đổi theo công ty, 3 nhãn đúng (Nhà cung cấp ·
  Chính sách kinh doanh · SL tồn kho tối thiểu), **bảng cũ đã gỡ hẳn**.
- **Bố cục: mở cả 5 tab, đo `.form-row` đang hiển thị → 0 hàng lỗi.** Vòng này bắt được 1 hàng lẻ
  ("Hệ số giá theo công ty" 4 cột) → đã đổi thành dải inline.
- Console: vẫn chỉ 2 lỗi toàn cục của layout.

### 3 điểm mockup tự quyết, cần user duyệt

1. **"% giảm giá thanh lý"** xếp vào tab **Mua hàng** (cạnh thuế BVMT) — `products.rate_liquidation`
   có 1.251 dòng dữ liệu thật nên phải giữ (QĐ 1), nhưng tài liệu không nói đặt ở đâu.
2. **"Hệ số giá theo công ty"** dựng thành **bảng** (Công ty | Hệ số) đúng bản chất
   `product_company_coefficients` (1.105 dòng), không phải một ô nhập.
3. **Trọng lượng / Kích thước / Serial number** xếp vào tab 1 (khối Thông tin hàng hoá);
   **Nhóm máy / Máy** của ERP chưa đưa vào — chờ user xác nhận còn dùng không.

### 9. Đơn vị tính ↔ Giá bán → GIỮ NGUYÊN LOGIC, chỉ BỎ đồng bộ CRM

User chốt 21/09/2026: *"Chỉ bỏ đồng bộ CRM ⇒ luồng này không dùng nữa. Còn lại không thay đổi
logic quản lý."*

Khảo sát đầy đủ: **`khao-sat-don-vi-tinh-gia-ban.md`**. Tóm tắt:

**Giữ nguyên** — ERP đã có sẵn giá bán theo ĐVT *và* theo thời gian, cấu trúc 3 tầng:
`product_units` (46.560) → `product_unit_prices` (264.646 = 46.560 × 6 loại giá) →
`product_expected_prices` (95.266, có `effect_date`, 2.495 dòng còn ở tương lai).
Kèm luồng **duyệt giá** bằng cột `*_wait_approve` + cờ 3 trạng thái (0/NULL không chờ · 1 đang chờ ·
2 đã từ chối), quyền riêng `Duyệt giá hàng hoá`, màn riêng (view 727 dòng).

**Không port phần chết:** bảng `product_prices` (dữ liệu dừng 05/02/2021, không có `unit_id`).

**"Giá công thức" — GIỮ cột (user chốt 21/09/2026), nhưng chưa có nguồn dữ liệu.**
Vòng 3 tôi gỡ cột này vì đo thấy nó luôn rỗng; user yêu cầu thêm lại ⇒ đã thêm lại dưới dạng
**cột CHỈ ĐỌC**, đúng như ERP (ERP cũng chỉ hiển thị `<% price.recipe_price %>`, không có ô nhập).

Truy nguồn đầy đủ (grep toàn bộ `app/` + `resources/`):

| Nơi | Kết quả |
|---|---|
| `product_unit_prices` (264.646 dòng — bảng giá đang dùng) | **không có cột** `recipe_price` |
| `product_expected_prices` (95.266 dòng) | **không có cột** |
| `price_calculate_*` (luồng Tính giá, 27.874 dòng, mới nhất 14/09/2026) | **không có cột** |
| `product_prices` (bảng chết) | có — 3.828 dòng khác 0, bản mới nhất **29/08/2020** |
| `tmp_product_prices` (hàng tạm) | có cột nhưng **0 dòng** |
| `tmp_product_unit_prices` (10.919 dòng — bảng hàng tạm đang dùng) | **không có cột** |
| Chỗ **tính/gán** `recipe_price` trong mã nguồn | **0 chỗ** — chỉ 2 dòng JS ở màn hàng tạm copy lại giá trị BE trả về |

Cột "Giá công thức" hiện diện ở **18 màn** của ERP (form hàng hoá, hàng tạm, hàng hoá gốc, cập nhật
nhanh giá, **yêu cầu tính giá**) — tức là khái niệm nghiệp vụ có thật và dùng rộng, nhưng **đường
dữ liệu đã đứt từ 2020**.

⚠️ **Cần chốt cách tính trước khi làm thật.** Giả thuyết hợp lý nhất: giá công thức = tổng giá các
thành phần trong **Công thức lắp ráp** (`recipe_products`, 6.438 dòng, có `qty` + `is_main`), nhưng
chưa có gì trong mã nguồn xác nhận.

**Bỏ đồng bộ CRM** — nhánh hàng hoá & giá:
- Đã ngừng từ **08/10/2025**; `MATE_API_USE_CRM` không khai trong `.env` (mặc định `false`).
- ⚠️ **Nhánh nhân sự vẫn sống** (`Employee`/`EmployeeInfo` mới nhất **14/09/2026**, `Department`,
  `Part`, `Company`) — **không gỡ nhầm**.
- 🔑 8 model trong nhánh hàng hoá (`Brand`, `Manufacture`, `Origin`, `Unit`, `TaxRate`, `Attribute`,
  `ProductModel`, `AttachmentType`) là **các danh mục đã port ở Phase 1** — HRM dùng model riêng nên
  đồng bộ CRM đã bị bỏ qua từ Phase 1; quyết định này khép lại lỗ hổng đó.

**98,7% hàng hoá chỉ có 1 ĐVT** (45.300/45.889) → giao diện tối ưu cho ca 1 ĐVT, nhiều ĐVT (589
hàng hoá) là ngoại lệ.

## Rà soát trường + bổ sung thao tác (21/09/2026, vòng 3)

Chuẩn đối chiếu: **44 trường mà form ERP thực sự bind** (`ng-model="product.*"` trong
`form.blade.php`) + 22 trường con (`u.*`, `price.*`, `attr.*`, `p.*`), đối chiếu với 59 cột bảng
`products` và tài liệu 6 tab.

### A. Trường THIẾU — đã bổ sung

| Thiếu | Bổ sung vào | Căn cứ |
|---|---|---|
| Cột **Bắt buộc** ở bảng Thông số cơ bản | tab 1 | `attr.require` |
| **Đơn vị thuộc tính** đang là chữ tĩnh → đổi thành **select** | tab 1 | `attr.unittech_id` → danh mục ĐVTT (Phase 1) |
| Nút **xoá dòng** ở bảng Thông số cơ bản | tab 1 | — |
| 4 bảng hàng hoá kèm: cột **Mã · Tên · ĐVT · Số lượng**, riêng Công thức lắp ráp thêm **Thành phần chính** | tab 2 | `p.unit_id`, `p.qty`, `p.is_main` |
| 4 checkbox **"Chọn tất cả"** ở Phụ tùng ô tô + đổi 4 ô sang **chọn nhiều** | tab 2 | `choose_all_manufact/brand/model/life` |
| Thao tác **Tải xuống · Thay đổi · Xoá** cho tài liệu; **Xem trước · Đặt làm ảnh đại diện · Xoá** cho ảnh | tab 1 | — |

⚠️ **4 bảng hàng hoá kèm có CỘT KHÁC NHAU** — dựng chung một khuôn là sai:

| Bảng | Số dòng | Có `unit_id` / `qty` | Có `is_main` |
|---|---|---|---|
| `recipe_products` (Công thức lắp ráp) | 6.438 | ✔ | ✔ |
| `product_has_accessories` (Phụ kiện mua thêm) | 989 | ✔ | ✘ |
| `product_has_install_accessories` (Vật tư lắp đặt) | 28 | ✔ | ✘ |
| `product_has_repair_accessories` (Vật tư sửa chữa) | **5** | **✘** | ✘ |

### B. Trường ĐÃ GỠ khỏi mockup

**"Serial number"** — tôi thêm nhầm ở vòng 1. Form ERP **không bind** trường này và
`products.serial_number` có **0/45.890 dòng** dữ liệu. Cùng nhóm rỗng thật: `short_description` ·
`special_feature` · `comment_temp` (0 dòng mỗi cột).

> 🐞 **Đính chính 21/09 (chiều):** bản đầu tôi xếp cả `avatar` và `comment` vào nhóm "0 dòng" — SAI.
> Câu đo dùng `where($cot,'<>',0)` cho cột CHUỖI, MySQL ép kiểu số nên `'abc'=0` loại sạch.
> Số thật: **`avatar` 45.448/45.890 (97%)** — và ERP còn khai `'avatar' => 'required'` ⇒ **form HRM
> phải bắt buộc ảnh đại diện**. `comment` 2.267 · `code_2025` **36.195** · `code_2020` **36.001** ·
> `model_old` 3.706. Xem `sua-product-model-erp.md` §6.

### C. Trường CỐ Ý không đưa lên — ghi để khỏi hỏi lại

| Trường | Lý do |
|---|---|
| `product_type` · `product_cate` · `group_id` | đã chốt bỏ (§3, §6, §8) |
| **Nhóm máy / Máy** (`group_ids_use`) | validate `exists:groups,id` ⇒ gắn vào **bảng `groups` đang bị bỏ**, chết theo |
| `model_old` 3.706 · `old_barcode` 133 | dữ liệu di sản |
| ⚠️ `code_2025` **36.195** · `code_2020` **36.001** | **KHÔNG phải di sản** (79% hàng hoá có) — cần hỏi nghiệp vụ 2 cột mã này dùng làm gì trước khi bỏ |
| `promotion` 241 (0,5%) · `tmp_product_id` 8.931 · `product_template_id` 29.813 | cờ/liên kết hệ thống, không phải trường nhập tay |

### D. Thao tác đã bổ sung

**Màn danh sách** — thêm cột **Hành động** (`key: 'actions'`, slot `#cell-actions`):
Sửa · Sao chép hiện thẳng trên dòng; **Khoá/Mở khoá · In tem barcode · Lịch sử · Xoá** trong menu
"…". Bám ERP (`ProductsController:334-337`: Sửa · Xoá · Lịch sử · Sao chép) + Khoá/Mở khoá theo
chuẩn danh mục HRM + In tem barcode (route `proBarcode`).
Toolbar thêm **"Xoá N hàng hoá đã chọn"** (route ERP `products.bulkDelete`), chỉ hiện khi có dòng
được tick.
✅ Đo thật: dòng đang hoạt động có 6 thao tác; **dòng đang khoá thì menu KHÔNG có "Xoá"** — đúng quy
tắc ẩn hẳn nút không dùng được.

**Màn form** — `V2Footer` thêm `#custom-actions`: **Sao chép · In tem barcode · Lịch sử**
("Quay lại" do `V2Footer` tự render, không tự thêm).

### E. 🐞 Lỗi của mockup vòng 1-2, phát hiện khi rà soát

`V2BaseDataTable` dùng slot **`#cell-<key>="{ item }"`**, KHÔNG phải `#cell(<key>)="{ row }"` kiểu
Bootstrap-Vue. Tôi viết sai khuôn ở **cả 4 slot** (ảnh · mã · loại sản phẩm · trạng thái) ⇒ Vue
**không báo lỗi gì**, bảng vẫn render nhưng hiện **giá trị thô**, mất ảnh, mất link, mất badge, mất
dòng phụ. Hai vòng đo trước không bắt được vì tôi chỉ đếm số cột và số dòng, **không đo nội dung ô**.

Bài học: đo bảng phải kiểm **nội dung ô đã render** (`.thumb`, `.v2-cell-link`, `.sub-line`, badge),
không chỉ tiêu đề cột.

Ngoài ra `sticky: 'right'` **không tồn tại** — `V2BaseDataTable` hiểu thành ghim TRÁI
(`left: 198px`). Cột Hành động phải khai `locked: true` không kèm `sticky`, đúng như màn brands.

### Vòng 4 (21/09/2026) — Bảo hành + Hệ số công nghệ chuyển sang Dữ liệu quản trị theo công ty

User chốt: 2 trường này cũng là dữ liệu **theo từng công ty** → gỡ khỏi tab *Thông số kỹ thuật*,
đưa vào tab **Dữ liệu quản trị**, nằm trong từng tab công ty.

Tab *Dữ liệu quản trị* giờ có **6 trường / 2 hàng**, mỗi hàng đủ 12 cột:

| Hàng | Trường | Nguồn hiện nay |
|---|---|---|
| 1 | Nhà cung cấp (6) · Chính sách kinh doanh (3) · SL tồn kho tối thiểu (3) | `product_suppliers` · `business_policies` · `products.min_stock_qty` |
| 2 | Bảo hành (4) · Đơn vị bảo hành (4) · **Hệ số công nghệ** (4) | `products.guarantee` · `products.guarantee_type` · `products.tech_coefficient` |

**Dữ liệu thật của 2 trường mới chuyển:**
- `guarantee` — **23.869 / 45.890** dòng có giá trị.
- `guarantee_type` — `thang` 45.308 · `nam` 62 · `ngay` 59 · NULL 461.
- `tech_coefficient` — **34.734** dòng khác 0; hay gặp nhất `1.00` (32.398), rồi `1.50` (1.241),
  `1.25` (722).

⚠️ Cả 3 cột hiện là **một bộ chung trên `products`**, chưa theo công ty — giống `min_stock_qty`.
Tách theo công ty thuộc **Phase 3**.

Tab *Thông số kỹ thuật* không còn khối "Kỹ thuật"; đã ghi chú ngay trong file để không ai đưa
2 trường này quay lại.

**Đo lại:** 4/5 tab không còn chữ "Bảo hành"/"Hệ số công nghệ"; chỉ tab Dữ liệu quản trị có, ở cả 2
tab công ty. Bố cục 5 tab: 0 hàng lỗi.

🐞 **Bẫy khi đo trang có TAB LỒNG:** `document.querySelector('.tab-pane.active')` trả về **pane lồng
bên trong tab khác**, không phải pane cấp 1 đang mở — vì pane con giữ class `active` kể cả khi cha
đã ẩn. Lần đo đầu vì thế báo nhầm "tab Giá bán có Bảo hành". Phải lấy **con trực tiếp của
`.tab-content` cấp 1**: `[...rootContent.children].find(c => c.classList.contains('active'))`.

### Vòng 5 (21/09/2026) — Icon cho tiêu đề card

User: *"các card phân loại nội dung thêm icon cho sinh động dễ phân biệt"*.

**Không sửa component dùng chung.** `V2BaseFormSection` đã có sẵn slot `#title` dành cho tiêu đề
cần markup riêng (chính component ghi chú vậy) → dùng slot, không đụng vào file dùng chung của
35 màn.

**Chỉ dùng icon ĐÃ xuất hiện thật trong hrm-client** (đếm trên `pages/` + `components/`: 324 icon
`ri-*` đang dùng). Lý do: repo có **2 bản Remix Icon lệch codepoint** (2.4.0 bundled + 4.3.0 CDN),
icon lạ có thể ra sai glyph mà không báo lỗi — xem memory `hrm-client-remixicon-codepoint-conflict`.
Icon đã chạy đúng ở màn khác thì chắc chắn đúng ở đây.

| Card | Icon | Màu |
|---|---|---|
| Phân loại | `ri-node-tree` | tím `#7c3aed` |
| Thông tin hàng hoá | `ri-archive-line` | xanh dương `#2563eb` |
| Nguồn gốc | `ri-earth-line` | xanh nhạt `#0ea5e9` |
| Thông số cơ bản | `ri-list-settings-line` | xám `#64748b` |
| Đơn vị tính | `ri-scales-3-line` | cam `#d97706` |
| Tài liệu · Hình ảnh · Video | `ri-attachment-2` | xám |
| Phụ kiện tiêu chuẩn · Đặc điểm | `ri-file-text-line` | xám |
| Phụ kiện tùy chọn mua thêm | `ri-shopping-bag-3-line` | xanh lá `#16a34a` |
| Vật tư sửa chữa – bảo hành | `ri-tools-line` | cam |
| Vật tư lắp đặt | `ri-hard-drive-2-line` | xanh nhạt |
| Công thức lắp ráp | `ri-stack-line` | tím |
| Phụ tùng ô tô | `ri-truck-line` | xám |
| Khai báo hải quan | `ri-file-list-3-line` | xanh dương |
| Thuế | `ri-percent-line` | đỏ `#dc2626` |
| Dữ liệu quản trị — <công ty> | `ri-building-2-line` | xanh dương |

Icon cỡ **15px**, cách chữ 6px, `vertical-align: -1px` — chỉ để **phân biệt khối**, không phải nút bấm.

⚠️ Màu đỏ ở "Thuế" là **màu icon**, không phải chữ — quy ước "đỏ chỉ dùng cho lỗi validate" áp cho
CHỮ, ở đây chữ tiêu đề vẫn đen.

**Tab Giá bán không có icon vì không có card** — từ vòng 2 tab này là tab lồng + bảng, cố ý bỏ khung
theo hướng UI phẳng/gọn. Nếu muốn thêm khung cho đồng bộ thì nói, nhưng như vậy là thêm 1 lớp viền.

**Đo lại:** 5 tab → **15/15 card đang hiển thị có icon**, **0 icon rộng 0px** (glyph vẽ ra thật,
font `remixicon` đã `loaded`). Bố cục vẫn 0 hàng lỗi.

### Vòng 6 (21/09/2026) — "Đặc điểm" là ô nhập CÓ ĐỊNH DẠNG

User: *"Trường Đặc điểm là textarea nhập có format"*.

Khớp với ERP: `form.blade.php:880` — `ng-model="product.product_attributes" **ck-editor**`.

**Chọn CKEditor 5 qua component `<ckeditor>`**, không dùng `V2BaseTextarea` (mất định dạng).
hrm-client có **2 cơ chế soạn thảo song song**, phải chọn đúng:

| Cơ chế | Là gì | Dùng ở | Hợp với |
|---|---|---|---|
| `<ckeditor :editor="ClassicEditor" :config="editorConfig" />` | CKEditor **5** (`@ckeditor/ckeditor5-vue`) | **25 màn** (training) | ô nhập trong form |
| `Vue.prototype.$loadCKEditor(el, opts)` (`plugins/ckeditor.js`) | CKEditor **4**, toolbar đầy đủ + plugin dán từ Word | mẫu in | soạn thảo nặng, bản in |

Toolbar rút gọn còn 7 nút — `bold · italic · link · bulletedList · numberedList · undo · redo`
(các màn training dùng 32 mục, thừa cho ô này: ô Đặc điểm không cần chèn ảnh/bảng).

**Đo thật:** editor render 608×285px, đủ 7 nút, nội dung mẫu giữ `<strong>` và `<ul><li>` — định
dạng chạy thật, không lỗi console mới. ⚠️ Lần nạp đầu Nuxt phải bundle lại CKEditor 5 nên **timeout
30s đầu tiên**; lần sau chỉ 1s.

📌 **Còn một ô cùng loại chưa đổi:** ERP cũng dùng `ck-editor` cho **"Phụ kiện tiêu chuẩn"**
(`form.blade.php:864`, `height="200"`). Mockup đang để `V2BaseTextarea`. User mới chỉ chốt ô
"Đặc điểm" — chờ xác nhận có đổi nốt không.

### Bản HTML độc lập để gửi khách (21/09/2026)

**File:** `.plans/gop-db/quan-ly-hang-hoa/man-danh-muc-hang-hoa/mockup-hang-hoa.html` (~3,1 MB,
mở bằng nháy đúp, **không cần server, không cần internet**).

**Script xuất:** `e2e/xuat-mockup.js` — chạy lại khi mockup đổi:
```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  node ./xuat-mockup.js ../.plans/gop-db/quan-ly-hang-hoa/man-danh-muc-hang-hoa/mockup-hang-hoa.html
```

**Cách làm:** mở trang Nuxt thật bằng Chromium (nạp phiên từ `e2e/.auth/user.json` vì mockup nằm
sau lớp đăng nhập) → chụp DOM đã render của 2 màn → gom toàn bộ CSS đang áp dụng → nhúng font
base64 → ghép 1 file + JS nhỏ để chuyển màn và chuyển tab. Dải ghi chú vàng "MOCKUP" bị gỡ khỏi bản
gửi khách (chỉ dành cho nội bộ); mọi ô nhập để `pointer-events: none` vì đây là bản xem.

**3 cái bẫy đã vấp và cách tránh:**

1. **Chromium mới không có phiên đăng nhập** → trang đẩy về `/login`, `waitForSelector` hết giờ.
   Phải nạp `storageState` từ `e2e/.auth/user.json`.
2. 🔴 **`remixicon.css` có HAI khối `src:`** (một cho IE9). Thay mỗi khối đầu bằng data URI thì khối
   sau **đè lên**, trình duyệt quay về tải `remixicon.woff2` cạnh file HTML → 404 và icon thành ô
   vuông rỗng. Phải **dựng lại cả khối `@font-face`** thành một `src` duy nhất.
3. **Font cục bộ của hrm-client** (`Font Awesome`, `Material Design Icons`, `boxicons`…) nạp từ
   `/_nuxt/assets/fonts/*` — đường dẫn này không tồn tại khi mở `file://`. Phải đọc file thật trong
   `hrm-client/assets/fonts/` rồi nhúng base64 (5 font, tổng ~509 KB).

**Đã kiểm trên đúng file `file://`:**
- **0 tài nguyên lỗi** (trước khi vá: 6 lỗi `ERR_FILE_NOT_FOUND`).
- Font icon nạp thật, **không phải fallback**: `document.fonts.check('16px remixicon')` = `true`,
  và ký tự PUA đo được **64px** với font icon vs **46px** với `serif` — khác nhau nghĩa là glyph
  thật đang được vẽ. 16 icon card, **0 icon rộng 0px**. Icon `fas fa-arrow-left` của nút Quay lại:
  11×12px.
- Chuyển màn chạy; **chuyển tab chạy cả ở tab lồng** (bấm *Giá bán* → mở đúng pane thứ 5).
- Bảng danh sách giữ nguyên 12 cột, 3 dòng, có ảnh thumb + badge trạng thái; CKEditor ở tab Thông
  số kỹ thuật vẫn hiển thị.

⚠️ **Đo bề rộng > 0 KHÔNG đủ để kết luận icon đúng** — ô vuông rỗng của font thiếu cũng có bề rộng.
Phải so bề rộng giữa font icon và font thường, hoặc dùng `document.fonts.check`.

### 10. ERP chỉ ĐỌC hàng hoá — toàn bộ luồng GHI chuyển sang HRM (user chốt 21/09/2026)

> *"Toàn bộ các luồng chức năng ghi vào hàng hoá tôi sẽ chuyển sang HRM. ERP sẽ chỉ dùng hàng hoá
> chứ không ghi nữa."*

Phân tích đầy đủ: **`phan-tich-song-song-erp-hrm.md`**. Ba điều rút ra:

**a. Phạm vi lớn hơn màn hàng hoá nhiều lần — 16 nơi ERP đang ghi**, không phải 3:
- Nhóm A (màn hàng hoá): `ProductsController` 11 chỗ · `Product.php` 3 · `CreateProductService` 2 ·
  `Product2Controller` 9 ❓
- Nhóm B (nghiệp vụ khác): `TmpProductsController` 7 (**19,5% hàng hoá sinh từ đây**) ·
  `ProductApprovesController` 2 · 🔴 **`PriceCalculate` 1** · `ManufactureExpectPrice` 1 ·
  `ProductImport` 1 (dead code) · `ImportProductAttribute` 1 · **3 job nền** 6
- Nhóm C (giữ ERP): `ProductTemplatesController` 6 · `ProductInfoController` 5 ·
  `SyncProductInfoService` 2

⚠️ **3 job nền là chỗ dễ sót nhất** — chạy ngoài request, rà theo màn không thấy.

**b. 🔴 Mâu thuẫn cần chốt: luồng Tính giá `PriceCalculate`** đang GHI giá vào hàng hoá (tạo
`ProductVersion`, sửa `ProductUnitPrice` + `ProductExpectedPrice`, ghi `ProductHistory`) — **3.120
phiếu, mới nhất 14/09/2026**. Thuộc Mua hàng/Đặt hàng (ở lại ERP) nhưng việc nó làm là *đặt giá bán
cho hàng hoá*. Hoặc chuyển, hoặc là ngoại lệ được phép ghi.

**c. Giai đoạn chuyển tiếp vẫn ghi song song** (Phase 2 → Phase 6, ~700–1.100 hàng hoá mới/tháng):
va chạm mã hàng hoá (17% mã đã phải thêm hậu tố `:NN`; có UNIQUE nên không hỏng dữ liệu nhưng báo
`Duplicate entry` cho người dùng) → HRM port `generateCode()` nguyên văn + retry.

**Rủi ro KHÔNG tự biến mất khi ERP hết ghi:** ghi `product_histories` (319.303 dòng) +
`product_versions` (113.768 dòng). ERP ghi rải rác trong controller (26 + 30 chỗ), **không qua
observer** → HRM không port là lịch sử đứt im lặng.

✅ **Sửa nhận định sai ở bản phân tích trước:** `Modules/Finance` của HRM là phân hệ **Tài chính**,
KHÔNG phải kho (user đính chính). Kho vẫn ở ERP. Finance chỉ ĐỌC hàng hoá cho chứng từ và ghi
`stocks.accounting_qty`, **không ghi `products`** (đã kiểm: 2 kết quả khớp đều là dương tính giả).

🐞 **Mockup đang vẽ mã hàng hoá `TP.0012345` — SAI khuôn thật.** Mã thật sinh theo
`MÃ-HÃNG-SX + '-' + (tên barcode|model)`: `CH-RRI32` · `SG-VT-NM0102` · `HN-90915-YZZE1:01`.
Phải sửa mockup khi quay lại nhánh.

### 11. Luồng Tính giá chuyển sang HRM · Lịch sử làm theo cách HRM · BỎ version (user chốt 21/09/2026)

#### 11a. Luồng Tính giá → HRM, và nó là MỘT PHASE RIÊNG

Đo quy mô: **4 controller · 39 route · 18 file blade**

| Phần | Quy mô |
|---|---|
| `PriceAskingRequestController` · `PriceCalculateRequestController` · `PriceCalculateController` · `PriceCalculateResultController` | 495 + 334 + 255 + 76 = **1.160 dòng** |
| Model `PriceAskingRequest` · `PriceCalculateRequest` · `PriceCalculate` | 759 + 603 + 909 = **2.271 dòng** |
| View `price_asking_requests` · `price_calculate_requests` · `price_calculates` | 1.010 + 672 + 731 = **2.413 dòng** / 18 file |
| Dữ liệu | `price_calculates` 3.120 · `price_calculate_requests` 3.147 · `price_calculate_product_prices` 27.874 · `price_calculate_result_product_prices` 27.863 — mới nhất **14/09/2026** |

Có đủ luồng duyệt riêng: `approve` · `reject` · **`approveXNK`** · `rejectXNK` · `cancelApprove`.

⇒ **Không nhét được vào Phase 2.** Đề xuất mở **Phase 7 — Luồng tính giá** trong folder lớn
`quan-ly-hang-hoa/`. Phase 2 chỉ cần biết: khi luồng này còn ở ERP thì nó **vẫn ghi giá hàng hoá**,
nên trong giai đoạn đó ERP chưa thực sự "chỉ đọc".

#### 11b. Lịch sử chỉnh sửa hàng hoá — làm theo cách HRM

Dùng `catalog_histories` của HRM, **không ghi** `product_histories` nữa.

**Hai mô hình ngược nhau nhưng tương đương về thông tin:**

| | ERP | HRM |
|---|---|---|
| Đơn vị một dòng log | **1 cột thay đổi** | **1 lần lưu** |
| Gom nhiều cột của cùng lần lưu bằng | `product_version_id` | `old_value` / `new_value` chứa nhiều cột |
| Số dòng | `product_histories` 319.303 (trung bình **2,8 cột/lần lưu**, cao nhất 15) | `catalog_histories` 2.374 |

⚠️ **Việc phải làm thêm:** `catalog_histories` hiện chỉ log **cột phẳng** của danh mục. Hàng hoá có
**bảng con** — đơn vị tính · giá theo ĐVT × 6 loại giá · thuộc tính · 4 bảng hàng hoá kèm · ảnh /
video / tài liệu. Phải chốt cách ghi log cho các bảng con này (ghi tóm tắt "đổi 3 dòng giá", hay
liệt kê từng dòng).

⚠️ **Màn "Lịch sử chỉnh sửa hàng hóa" của ERP** (`productHistory`, `ProductsController@history:988`)
sẽ **không thấy thay đổi từ HRM**. Cần chốt: gỡ hẳn màn đó bên ERP, hay để lại như kho tra cứu
lịch sử CŨ (trước ngày chuyển).

**Dữ liệu cũ giữ nguyên, chỉ ngừng ghi:** 319.303 dòng `product_histories` + 113.768 dòng
`product_versions`.

#### 11c. BỎ version hàng hoá

`product_versions` **không phải "phiên bản để khôi phục"** — nó chỉ là **cái nhóm các thay đổi của
một lần lưu**: màn lịch sử ERP lấy version làm khung rồi đổ `product_histories` theo
`product_version_id`. Vai trò đó `catalog_histories` của HRM **đã gom sẵn trong một dòng**, nên bỏ
version là nhất quán, không mất thông tin nào.

⚠️ **Chỉ bỏ cho luồng HÀNG HOÁ.** `ProductVersion` còn được dùng bởi `ProductInfoController`
(Hàng hoá có sẵn) và `Product2Controller` — hai luồng đó ghi version của riêng chúng, **không đụng
tới**.

⚠️ Khi luồng Tính giá chuyển sang HRM (11a) thì nó **cũng thôi tạo `ProductVersion`** — hiện
`PriceCalculate:404` đang `ProductVersion::create([...])`.

**KHÔNG xoá bảng `product_versions`** — giữ 113.768 dòng cũ để tra cứu; chỉ ngừng ghi.


### 12. Thứ tự chuyển + tiêu chí nghiệm thu (user chốt 21/09/2026)

> *"Quản lý giá, duyệt giá, tính giá bán sẽ chuyển đổi dần. Chuyển hàng hoá thực hiện trước.
> Mục tiêu quan trọng là phải đảm bảo ERP vẫn chạy ổn định sau khi chuyển hàng hoá sang HRM."*

⇒ **Tiêu chí nghiệm thu Phase 2 đổi:** không phải "màn HRM chạy được" mà là **"ERP không vỡ chỗ
nào"**. Hợp đồng đầy đủ + kịch bản nghiệm thu 14 bước: **`hop-dong-tuong-thich-erp.md`**.

**Sáu bất biến phải giữ** (hỏng cái nào là ERP vỡ):

| # | Bất biến | Mức |
|---|---|---|
| BB-1 | Sửa giá đi qua **luồng duyệt**, không ghi thẳng | 🔴 |
| BB-2 | Không có quyền `Quản lý giá` thì **không đụng gì tới giá** | 🔴 |
| BB-3 | Mã sinh đúng khuôn + retry khi trùng | 🟡 |
| BB-4 | Ghi **đủ** bảng vệ tinh | 🟡 |
| BB-5 | `updated_by` ở mọi đường ghi, kể cả khoá/mở khoá | 🟡 |
| BB-6 | `product_type` không trống — **hoặc sửa `SearchController` TRƯỚC** | 🔴 |

**Phát hiện quan trọng khi rà BB-1:** màn hàng hoá của ERP **KHÔNG ghi giá trực tiếp** — đường ghi
thẳng đã bị comment tắt (`ProductsController:1565-1635`). Đường đang chạy tách 2 nhánh theo cờ
`$is_approve`, tính từ **cấu hình công ty**:

```
is_approve = companies.is_new_company
             AND ( companies.is_new_brand OR manufacture_id ∈ companies.new_brand_ids )
```

Đo thật: **1/8 công ty** đang bật (công ty #8); `product_approves` 0 dòng — cơ chế bật nhưng chưa
phát sinh phiếu. HRM ghi thẳng giá ⇒ **giá đổi mà không ai duyệt**.

**Và BB-2:** toàn bộ khối giá của ERP nằm trong `if (Auth::user()->can('Quản lý giá'))`
(`ProductsController:1547`) — bỏ điều kiện này là người không có quyền giá vẫn ghi đè giá.

⚠️ **Chặn trước khi bật màn HRM:** phải xong BB-6. Chưa sửa `SearchController` mà đã cho tạo hàng
hoá từ HRM thì **hàng hoá mới vô hình với 338 màn** của ERP.

⚠️ Phiếu duyệt giá chụp kèm `product_type` + `product_cate` (`ProductsController:1670-1671`) — 2 cột
HRM sẽ để trống theo quyết định 3 và 6. Cần chốt: bỏ khỏi phiếu hay điền bằng dữ liệu cây mới.


### 13. Chặn route ERP + tập trung làm ERP KHÔNG LỖI (user chốt 21/09/2026)

> *"Khi update quản lý hàng hoá HRM tôi sẽ chặn toàn bộ route tạo/sửa hàng hoá ERP. Chỉ cần tập
> trung update Model + Controller phía ERP sao cho các chức năng có sửa hàng hoá không bị lỗi.
> Các trường mã chỉ quan tâm `code`; `code_2025`, `code_2020` là backup để mapping khi đổi cách
> sinh mã ⇒ không cần quan tâm."*

Kế hoạch chi tiết: **`sua-erp-de-khong-loi.md`**.

**Bỏ được 4 mối lo** nhờ chặn route: BB-7 (rule `required` chặn sửa ở ERP) · đồng bộ rule validate
ERP↔HRM · `code_2025`/`code_2020` · va chạm mã giữa 2 app.

**🔴 Còn đúng một loại việc — và nó nặng hơn tôi tưởng:** `products.group_id` trống ⇒ ERP truy cập
`->group->cột` ở **hơn 100 chỗ**, **KHÔNG một chỗ nào** dùng `optional()`/`?->` ⇒ PHP 7.4 nổ
`Trying to get property of non-object`.

| File (làm việc trên bảng `products`) | Số chỗ | Mức |
|---|---|---|
| **`SearchController`** — popup chọn hàng của **338 màn** | **11** | 🔴 |
| `Sale/DeviceErrorController` | 8 | 🔴 |
| `Product.php` | 7 | 🔴 |
| `Sale/TmpProductsController` | 3 | 🔴 |
| `LiquidationQuotation` · `CostFixingQuotation` | 2 + 2 | 🟡 |
| `ProductSettingMailJob` (job nền) · `MyTmpProductsController` · `ExportLargeProductList` (lệnh theo lịch) · `BaseProduct` | 1 mỗi file | 🟡 |
| ~~`ProductsController` 14~~ · ~~`Product2Controller` 12~~ | route bị chặn, nhưng **hàm chỉ-đọc** còn được gọi từ ngoài ⇒ vẫn phải rà | 🟡 |

⇒ **~37 chỗ phải sửa ngay** trên 10 file còn sống.

**Nặng nhất là `SearchController`:** `->addColumn('group_id', fn($p) => $p->group->name)` là callback
DataTables **chạy cho TỪNG DÒNG**. Chỉ cần **một** hàng hoá thiếu nhóm lọt vào trang kết quả là
**cả popup nổ** cho mọi người dùng ở cả 338 màn.

📌 Nặng hơn BB-6 đã nêu: ở đó tôi mới nói hàng hoá *"biến mất"*; thực tế còn **crash**.
📌 `SearchController:813` **đã** có `$product->group ? … : …` — chứng tỏ lỗi này từng xảy ra và được
vá lẻ một chỗ, không rà hết.

**Hai cột kia không nguy hiểm bằng:** `product_type` là **chuỗi** nên không crash (chỉ làm hàng hoá
biến mất — vẫn phải bỏ 4 điều kiện lọc); `product_cate` mọi chỗ lọc đều bọc `if (!empty(...))` nên
**không phải làm gì**.

**Cách sửa:** `Product.php` + các model dùng **accessor gom một chỗ**
(`getGroupNameAttribute`, `getRateLiquidationValueAttribute`…), controller dùng `optional()` tại
chỗ. Cột số phải kèm `?? 0` để không đẩy lỗi chia-cho-0 sang chỗ khác.


### 14. ĐẢO NGƯỢC quyết định 8c + HOÃN lịch sử hàng hoá (user chốt 21/09/2026)

#### 14a. Thuộc tính nối lên **LOẠI SẢN PHẨM**, không phải Nhóm sản phẩm

> *"Thuộc tính sản phẩm sẽ nối lên Loại sản phẩm chứ không phải Nhóm sản phẩm."*

⇒ **Đảo ngược quyết định 8c.** Giữ nguyên `product_type_attributes` mà Phase 0 đã dựng
(`product_type_id` + `attribute_id`), ô "Thuộc tính" **ở nguyên màn Loại sản phẩm**.

**Không còn phải làm:** tạo `product_family_attributes` · `dropIfExists('product_type_attributes')` ·
chuyển ô Thuộc tính sang màn Nhóm sản phẩm · thêm quan hệ `attributes()` cho `ProductFamily`.

**Ảnh hưởng dây chuyền đã sửa theo:**

| Chỗ | Trước | Sau |
|---|---|---|
| Endpoint đổ Thông số cơ bản | `GET /attributes-by-family/{familyId}` | **`GET /attributes-by-type/{productTypeId}`** |
| Form kích hoạt khi đổi ô nào | *Nhóm sản phẩm* | **Loại sản phẩm** |
| Task A2 của plan | tạo bảng nối mới + chuyển ô | **chỉ còn gỡ `can_retail`** |

🟢 Đơn giản hơn hẳn: bỏ được 1 migration tạo bảng + 1 migration xoá bảng + việc chuyển ô giữa 2 màn.

📌 Tiện lợi thêm: khối *Thông số cơ bản* giờ đổ theo **cùng một ô** mà người dùng bắt buộc phải chọn
(*Loại sản phẩm*), không phải chờ suy ra cấp cha.

#### 14b. Lịch sử hàng hoá — TÁCH RA, xử lý sau

> *"Làm xong BE + FE tạo/sửa/danh sách hàng hoá trước ⇒ lịch sử hàng hoá để xử lý sau vì lịch sử
> hàng hoá bị thay đổi ở nhiều luồng chứ không đơn giản như các danh mục HRM."*

Đúng với số đo: `product_histories` **319.303 dòng**, ERP ghi ở **8 file / 26 chỗ**, và bị đổi từ
**nhiều luồng ngoài màn hàng hoá** — duyệt giá · **luồng Tính giá** · duyệt hàng tạm. Khác hẳn danh
mục HRM (một màn, một đường ghi, `catalog_histories` gánh đủ).

⇒ **Phase 2 KHÔNG làm lịch sử.** Quyết định 11b (dùng `catalog_histories`) vẫn giữ làm **hướng**,
nhưng việc thực thi tách sang đợt brainstorm riêng, kèm 2 câu còn treo: cách log **bảng con**, và số
phận màn "Lịch sử chỉnh sửa hàng hóa" bên ERP.

⚠️ **Hệ quả phải chấp nhận trong lúc chờ:** sửa hàng hoá từ HRM **không để lại vết ở đâu cả** —
không ghi `product_histories`, cũng chưa ghi `catalog_histories`.

### 15. Tab 6 "Phân loại xe" — chốt 21/09/2026

> User: *"Thêm tab: Phân loại xe ⇒ đưa toàn bộ form phần phân loại xe vào ⇒ hiển thị với mọi Tính
> chất hàng hoá ⇒ bỏ bắt buộc"*

Chuyển nguyên khối **"Phụ tùng ô tô"** của ERP (`resources/views/products/form.blade.php:420`)
thành **tab thứ 6** của màn tạo/sửa. **Hai điểm khác ERP**, đều theo yêu cầu:

| | ERP hiện tại | HRM |
|---|---|---|
| Điều kiện hiện | chỉ khi loại cũ `product_type = automotive_parts` | **mọi Tính chất hàng hoá** |
| Hãng xe | bắt buộc (`required_if:product_type,automotive_parts`) | **không bắt buộc** |

**3 ô, đều chọn nhiều:** Hãng xe (`vehicle_manufacts`, 56) → Loại xe (`vehicle_brands`, 322) →
Model xe (`vehicle_models`, 1.281). Lọc dây chuyền theo cấp trên.

⚠️ **ĐÍNH CHÍNH 21/09/2026 — "Đời xe" KHÔNG chết.** Bản ghi trước đó của mục này viết *"bảng
`vehicle_lifes` không tồn tại"* là **SAI**: tôi tra nhầm tên số nhiều. Sự thật:

| | |
|---|---|
| Bảng danh mục | **`vehicle_life`** (số ít), **61 dòng** — là các năm 1970 → 2030 |
| Bảng nối | **`product_vehicle_model_has_life`**, **48.736 dòng** / **91 hàng hoá** |
| Cấu trúc | bộ BA: `product_id` × `model_id` × `life_id` — KHÔNG phẳng như 3 ô kia |
| Code ERP | `Product::getModelLifes()` + `syncVehicleModelLife()` đã viết đủ, chỉ ô nhập trên form bị comment |

⇒ Không được bỏ. Cách hiển thị đang chờ user chốt (xem 15d).

⚠️ **Nhãn dễ nhầm lần 2**: `vehicle_life` là số ít, `vehicle_brands`/`vehicle_models`/
`vehicle_manufacts` là số nhiều. Đừng đoán tên bảng — `SHOW TABLES LIKE '%life%'` trước.

⚠️ **Nhãn dễ nhầm**: bảng tên là `vehicle_brands` nhưng nhãn trên form là **"Loại xe"**, không phải
"Thương hiệu xe". Đừng lẫn với `brands` (thương hiệu hàng hoá) ở tab 1.

#### 15a. Lưu ở đâu — và 3 cái bẫy

Lưu vào bảng nối đa hình **`productables`** mà ERP đang dùng. Một bảng gánh **5 loại quan hệ**:

| `productable_type` | Nghĩa | Dòng | Hàng hoá | HRM |
|---|---|---:|---:|---|
| `App\Model\Common\VehicleManufact` | Hãng xe | 13.165 | 477 | ✅ tab 6 |
| `App\Model\Common\VehicleBrand` | Loại xe | 12 | 10 | ✅ tab 6 |
| `App\Model\Common\VehicleModel` | Model xe | 6 | 6 | ✅ tab 6 |
| `App\Model\Product\Group` | Nhóm máy | 3.968 | 2.874 | ❌ không hiện, **không đụng** |
| `App\Product` | Máy sử dụng | 28.398 | 2.975 | ❌ không hiện, **không đụng** |

**Bẫy 1 — KHÔNG khai `morphedByMany()`.** `productable_type` lưu nguyên văn tên class của ERP. Khai
quan hệ đa hình trỏ tới entity HRM là Laravel so với `Modules\MasterData\Entities\Vehicle\...`
→ **khớp 0 dòng**: form trống trơn, mà nếu ghi thì sinh ra dòng mang class HRM còn ERP đọc bằng
class cũ sẽ không thấy. Hai bên cùng đọc một bảng mà không thấy nhau, không lỗi nào báo ra. Phải nối
bằng `hasMany` thường + lọc `productable_type` bằng **hằng chuỗi của ERP**
(`Modules/MasterData/Entities/Product/Productable.php`).

**Bẫy 2 — `sync(null)` xoá sạch.** ERP ghi bằng `$product->vehicleManufacts()->sync($ids)`. Nếu HRM
lặp lại khuôn đó hoặc "dọn rồi ghi lại" mà không kẹp `productable_type`, 13.165 dòng bốc hơi ngay
lần Lưu đầu tiên — và kéo theo cả 32.366 dòng Nhóm máy / Máy sử dụng mà **popup tìm phụ kiện của
ERP vẫn đọc** (`SearchController@searchProductStockBuyer`, được gọi từ ≥ 6 popup).
⇒ Task C3: mọi thao tác trên `productables` phải kẹp `whereIn('productable_type', VEHICLE_TYPES)`.

**Bẫy 3 — "Chọn tất cả" không có cột trong DB.** `choose_all_manufact` / `choose_all_brand` /
`choose_all_model` chỉ là cờ AngularJS, tick xong nó nhồi toàn bộ id vào mảng. Đó là lý do trung
bình **27,6 hãng xe / 1 hàng hoá** (có mã gắn đủ 39 hãng từ Acura tới VinFast). Đừng đi tìm cột.

#### 15b. Danh mục xe gọi RIÊNG, không gộp `/form-options`

`GET /products/vehicle-options` (route thứ 17), gọi khi người dùng **mở tab**. Đo thật: gộp vào
`/form-options` làm payload mở form nhảy **179,2 KB → 326,8 KB** (riêng 1.281 model xe ~115 KB) cho
một tab nằm thứ 6 và không mở sẵn. CLAUDE.md: *"danh mục chỉ dùng ở tab/modal chưa mở thì chỉ gọi
khi mở"*. Trả cả 3 cấp một lượt (~1.660 dòng) để FE lọc dây chuyền tại chỗ — `vehicle_models` giữ
cả 2 khoá cha nên lọc theo Hãng xe được ngay, không phải bắn thêm request.

#### 15c. Còn tồn — khối "Phụ tùng – Phụ kiện" chưa có chỗ

*Nhóm máy* (3.968 dòng) và *Máy sử dụng* (28.398 dòng) là card riêng bên ERP
(`form.blade.php:352`, hiện với `accessories` / `common_components…` / `special_components…`), KHÔNG
thuộc "phân loại xe" nên chưa đưa vào tab nào. Dữ liệu giữ nguyên, ERP vẫn đọc, nhưng khi chặn route
sửa của ERP thì **2 khối này đóng băng**. Cần chốt riêng: bỏ, hay thêm tab 7.

#### 15d. 🔜 YÊU CẦU MỚI 21/09/2026 — ĐANG CHỜ CHỐT, CHƯA CODE

> User: *"1. Chuyển toàn bộ danh mục phân loại xe, dòng xe, model xe,... sang HRM.
> 2. Với Nhóm máy cũng chuyển thành 1 tab riêng.
> ⇒ ở danh mục Tính chất hàng hoá sẽ thêm 2 checkbox chọn có khai báo: Phân loại xe / Nhóm máy
> không ⇒ dựa vào đó để hiển thị 2 tab mới thêm này."*

📌 **Tách phase 21/09/2026:** ý **1** (chuyển danh mục xe sang HRM) đã tách ra thành
**Phase 2b — `chuyen-danh-muc-xe/`**, ghi ở `quan-ly-hang-hoa/design.md`. Ý **2** (tab Nhóm máy
+ 2 checkbox trên danh mục Tính chất hàng hoá) **ở lại Phase 2**, vẫn chờ chốt như dưới.

**Đảo lại một phần quyết định 15**: tab "Phân loại xe" KHÔNG còn hiện với mọi Tính chất hàng hoá
nữa, mà hiện theo **cờ khai báo trên chính danh mục Tính chất hàng hoá**. (Điều kiện vẫn rời khỏi
cột cũ `products.product_type` như tinh thần ban đầu — chỉ là chuyển sang cây phân loại mới thay vì
"luôn hiện".) **Cần user xác nhận lại cách hiểu này trước khi code.**

**Việc phát sinh, ước lượng:**

| Việc | Quy mô |
|---|---|
| 2 cột cờ trên `product_characteristics` + ô nhập ở modal danh mục | nhỏ — bảng đang **0 dòng** |
| Màn danh mục **Hãng xe** (56) · **Loại xe** (322) · **Model xe** (1.281) ở HRM | 3 màn, khuôn `BaseCatalog*` như Phase 1 |
| Màn danh mục **Đời xe** (61) | tuỳ câu hỏi 2 dưới |
| Tab 7 **"Nhóm máy"** + màn danh mục nguồn của nó | tuỳ câu hỏi 1 dưới |
| Quyền mới cho từng màn danh mục | 4 quyền/màn, nối tiếp 1619 |

⚠️ 3 bảng xe **không có cột `code`** (giống `units`) ⇒ `hasCodeField()` trả false ở cả Service lẫn
Request. Có cột `note`. Trạng thái 1/0 theo chuẩn ERP.

⚠️ `vehicle_manufact_id` đang được **10 bảng khác** tham chiếu (`customers`, `firm_contracts`,
`vehicles`, `wr_service_contracts`, 4 bảng phân vùng thị trường…) ⇒ chuyển màn quản lý sang HRM
nhưng **vẫn dùng chung bảng của ERP**, đúng như Phase 1. Không tạo bảng mới, không di trú.

**3 câu đang chờ user chốt:**

1. **"Nhóm máy" đụng quyết định bỏ `groups`.** Nhóm máy trỏ vào bảng `groups` (893 dòng) — cùng
   bảng với danh mục "Nhóm hàng hoá" đã chốt bỏ ở Phase 5, và `products.group_id` trỏ tới nó ở cả
   45.890 dòng. Một bảng gánh 2 vai: *phân loại hàng hoá* (bỏ) và *danh sách máy để gắn phụ kiện*
   (3.968 liên kết — chưa ai bàn). Giá trị bên trong đúng là tên máy: "Máy rửa áp lực cao nước
   lạnh" (333 hàng hoá), "Cầu nâng 2 trụ thủy lực có cổng" (247), "Máy ra vào lốp xe con" (165).
   → Giữ `groups` sống chỉ với vai trò Nhóm máy / đọc từ `product_families` của cây mới / tạo bảng
   `machine_groups` riêng?

2. ~~**Phạm vi danh mục xe.**~~ ✅ **ĐÃ CHỐT 21/09/2026** — user: *"Lấy đúng 4 màn lõi, phần còn
   lại tách phase riêng"*. **Phase 2b** = 4 danh mục màn hàng hoá cần (Hãng xe 56 · phân loại xe
   `vehicle_brands` 322 = ô "Loại xe" trên form · model xe 1.281 · đời xe 61). **Phase 2c** = 5 màn
   xe công ty / vận chuyển, trong đó *"dòng xe"* = `vehicle_categories` (11, giá trị "Xe tải thùng
   kín" / "Xe cẩu" / "Xe đầu kéo" — `products` không dùng). Chi tiết:
   `quan-ly-hang-hoa/design.md` mục Phase 2b và Phase 2c.

3. **Ô "Đời xe" hiển thị thế nào.** Dữ liệu là bộ BA (hàng hoá × Model xe × Đời xe), không phẳng.
   → Bảng con dưới mỗi Model xe đã chọn (đúng cấu trúc, ERP đã có sẵn 2 hàm để port) / một ô chọn
   nhiều áp chung cho mọi model (làm phẳng, có thể sai 48.736 dòng hiện có) / chỉ đọc ở đợt này?

**Ảnh hưởng tới việc đã làm:** tab 6 hiện tại (BE `cf5c489a9`, mockup `3b1f98798`) vẫn dùng được —
chỉ cần thêm điều kiện hiện/ẩn theo cờ, và thêm ô Đời xe. Không phải làm lại.

### 16. Mã hàng hoá — sinh một lần, giữ mãi mãi (user chốt 22/09/2026)

> User: *"Mã hàng hoá chỉ sinh 1 lần, giữ mãi mãi không thay đổi, dù các đối tượng cấu thành mã
> có thay đổi"*

Khuôn mã: `<mã Hãng sản xuất>-<tên Code đặt hàng ?: tên Model>`, cắt 32 ký tự, chống trùng bằng
hậu tố `:01`…`:99`. Sinh **ở đường TẠO MỚI và chỉ ở đó**.

**Vì sao đây là ràng buộc cứng, không phải sở thích:** đo trên DB ngày 22/09/2026, dựng lại mã cho
cả 45.890 hàng hoá rồi so với mã đang lưu:

| | |
|---|---:|
| Khớp | 45.659 (99,50%) |
| **Khác** vì nguồn đã đổi sau khi mã chốt | **231** |
| ↳ mã sinh trước khi hàng hoá được gắn Code đặt hàng | 57 |
| ↳ Model / Code đặt hàng bị đổi tên sau đó | 174 |

Ví dụ hàng hoá #4319 mang mã `COGI-0-1110950116`, sinh từ `barcodes` id 11 (`0-11109501/16`); nay
nó đã trỏ sang code đặt hàng khác. Nếu có đường nào sinh lại mã lúc sửa thì **231 hàng hoá này đổi
mã cùng lúc**, kéo theo phiếu kho / hợp đồng / báo giá cũ đang trỏ theo mã cũ — hỏng rộng và không
có lỗi nào báo ra.

**Cách chốt trong code — 2 lớp:**

1. `ProductCodeGenerator` ghi rõ "CHỈ GỌI Ở ĐƯỜNG TẠO MỚI" ở docblock đầu class.
2. Hàng rào thật nằm ở **model** `Product::boot()`: hook `updating` ném `RuntimeException` nếu
   `code` bị `isDirty`. Đặt ở model chứ không ở Service vì Service nào cũng có thể quên, còn đây là
   đường chung cuối cùng của mọi thao tác ghi qua Eloquent.

2 ca test chốt lại: đổi `code` của hàng hoá đã tồn tại → nổ; sửa trường khác → vẫn lưu bình thường
và `code` giữ nguyên.

⚠️ Hệ quả cho **Task C3 (sửa hàng hoá)**: `PUT /{id}` KHÔNG nhận `code` từ người dùng và KHÔNG gọi
`ProductCodeGenerator`. Ô Mã trên form là ô **chỉ đọc**.
⚠️ Hệ quả cho **Task C4 (sao chép hàng hoá)**: bản sao là bản ghi MỚI nên được sinh mã mới — đó là
đường tạo, không phải đường sửa.

### 17. NGUYÊN TẮC CHUNG — bám ERP đang chạy, không bám mockup (user chốt 22/09/2026)

> User: *"Ngoài các phần sửa đổi tôi đã nêu ở spec, luôn tuân thủ hiện tại đang có trên ERP,
> không nghe mockup ⇒ cảnh báo tôi khi có sai khác để tôi quyết định"*

Thứ tự ưu tiên khi ba nguồn nói khác nhau:

```
1. Quyết định đã ghi trong spec này   (đã được user chốt)
2. ERP ĐANG CHẠY                      (mặc định cho mọi thứ còn lại)
3. Mockup                             ← KHÔNG phải nguồn sự thật về nghiệp vụ
```

Mockup chỉ là bản vẽ giao diện để chốt bố cục. Nó **không** quyết định trường nào bắt buộc, bảng
nào có cột gì, luồng ghi ra sao.

**Bắt buộc khi phát hiện sai khác:** dừng lại, báo user kèm số đo, chờ quyết định. KHÔNG tự chọn
rồi làm tiếp, kể cả khi phương án của mình "hợp lý hơn".

**Áp dụng ngay — `product_has_repair_accessories`:** bảng này chỉ có `base_product_id` ·
`product_id` · timestamps, **không có `qty` và `unit_id`** (khác 2 bảng phụ kiện kia). Mockup cho
nhập số lượng ở cả ba. ⇒ Theo ERP: bảng phụ kiện sửa chữa **không ghi số lượng / đơn vị**. Muốn có
thì phải thêm cột vào bảng ERP — việc đó cần user quyết riêng.

### 18. YÊU CẦU MỚI 22/09/2026 — chốt với khách hàng

> User: *"- Phần giá sẽ tách khỏi form nhập thông tin hàng hoá ⇒ Xây dựng màn hình quản lý giá riêng
> - Phần phụ tùng ô tô / Nhóm máy sẽ phụ thuộc vào tuỳ chọn ở cấp danh mục "Loại sản phẩm" tuỳ chọn
> có cần nhập hay không ⇒ ở Danh mục Loại sản phẩm thêm checkbox cho 2 tuỳ chọn này"*

#### 18a. Giá tách hẳn khỏi form hàng hoá

Form tạo/sửa hàng hoá **bỏ tab "Giá bán"**. Toàn bộ phần giá chuyển sang **màn quản lý giá riêng**.

**Quy mô phần bị tách** (đo 22/09/2026):

| Bảng | Dòng | Vai trò |
|---|---:|---|
| `product_units` | 46.560 | ĐVT của hàng hoá — **ở lại form hàng hoá**, nhưng 2 cột `cost_price` / `buy_price` thuộc phần giá |
| `product_unit_prices` | 264.646 | 6 loại giá × mỗi ĐVT |
| `product_expected_prices` | 95.266 | giá chờ hiệu lực |
| `price_types` | 6 | danh mục loại giá |
| đang chờ duyệt giá | 6 phiếu | `product_units.flag_price_wait_approve = 1` |

**Ranh giới cần chốt:** `product_units` vừa giữ danh sách ĐVT (thuộc hàng hoá) vừa giữ `cost_price`
/ `buy_price` (thuộc giá). Đề xuất: form hàng hoá ghi ĐVT + `unit_coefficient` + `is_base`; màn giá
ghi `cost_price` / `buy_price` / 6 loại giá / giá chờ hiệu lực / luồng duyệt.

**Ảnh hưởng tới plan:**

| Task | Trước | Sau |
|---|---|---|
| C2 (`POST /products`) | ghi cả khối giá, gắn BB-2 | **không đụng giá** — hết mâu thuẫn 5 rule `required` của ERP |
| C3 (`PUT /{id}`) | kèm luồng duyệt giá BB-1 | chỉ sửa thông tin; **BB-1 dời sang màn giá** |
| D4 (FE tab 4 + tab 5) | 2 tab | **chỉ còn tab 4**; tab Giá bán bỏ |
| — | — | **task mới: màn quản lý giá** (chưa mở) |

⚠️ Mockup hiện có tab "Giá bán" với 2 tầng tab lồng (Công ty → ĐVT) — phải gỡ khỏi mockup, và
phần đó là nguyên liệu để dựng màn giá mới.

#### 18b. 2 checkbox chuyển sang danh mục "Loại sản phẩm"

**Đảo lại §15d:** 2 cờ khai báo *Phụ tùng ô tô* (tab Phân loại xe) và *Nhóm máy* đặt ở
**Loại sản phẩm** (`product_types`, cấp 4 — cấp lá), KHÔNG phải Tính chất hàng hoá
(`product_natures`, cấp 1).

Hợp lý hơn bản cũ: form hàng hoá **chọn trực tiếp Loại sản phẩm** (3 cấp cha tự hiện), nên cờ đặt ở
cấp lá là đọc được ngay, không phải lần ngược lên cấp 1.

**Việc phát sinh:** 2 cột boolean trên `product_types` + 2 ô tick ở modal danh mục Loại sản phẩm +
điều kiện hiện/ẩn 2 tab ở form hàng hoá.
⚠️ Đây là **thay đổi CSDL** — nhưng trên bảng MỚI của Phase 0 (hiện **0 dòng**), không đụng bảng
ERP nào.

**Câu này giải phóng bớt §15d:** điểm 4 ("2 checkbox ở Tính chất hàng hoá") đã có đáp án. Còn lại 2
câu chưa chốt: **"Nhóm máy" lấy dữ liệu từ đâu** (bảng `groups` Phase 5 định gỡ) và **cách hiển thị
"Đời xe"**.

### 19. YÊU CẦU MỚI 22/09/2026 — bảng giá ĐỘC LẬP theo từng công ty

> User: *"Với 1 mã hàng hoá mỗi công ty trong hệ thống ERP sẽ có bảng giá độc lập khác nhau"*

**Đây là thay đổi CSDL thật sự**, không phải chuyển nền code — nên phải chốt trước khi làm màn giá
(§18a). Khảo sát 22/09/2026:

#### Hiện trạng: chuỗi giá KHÔNG có chiều công ty

```
products ──< product_units ──< product_unit_prices ──< product_expected_prices
                46.560           264.646                 95.266
```

Quét `information_schema`: **không bảng nào trong chuỗi có cột `company_id`**. Tức là hôm nay
**một mã hàng hoá có đúng MỘT bảng giá, cả 8 công ty dùng chung**.

`products.company_id` KHÔNG phải "hàng hoá thuộc công ty nào được bán": nó là công ty **tạo** bản
ghi. Đo: 44.816/45.890 thuộc công ty 1; và **0 mã** xuất hiện ở hai công ty khác nhau.

Tiền lệ duy nhất của dữ liệu-theo-công-ty là `product_company_coefficients` — **1.105 dòng / 589
hàng hoá / 4 công ty**, nhưng đó là *hệ số công nghệ*, không phải giá.

#### Điểm khó: ERP không biết khái niệm "giá theo công ty"

ERP đọc chuỗi giá ở **~44 file** (`ProductUnitPrice` 33 file, `product_unit_prices` 11 file,
`ProductExpectedPrice` 24 file). Không file nào truyền công ty vào. Thêm chiều công ty mà không
tính đường lùi thì **ERP đọc nhầm giá ở 44 chỗ** — đúng loại hỏng rộng mà Đợt E/F phải chặn.

#### 3 phương án, cần user chốt

| | Cách làm | Dữ liệu | ERP phải sửa |
|---|---|---|---|
| **A1** *(đề xuất)* | thêm `company_id` **nullable** vào `product_unit_prices` + `product_expected_prices`. `NULL` = **giá chung**, công ty nào cần giá riêng mới sinh dòng riêng | giữ nguyên 264.646 dòng làm giá chung | **không** — ERP đọc dòng `NULL` như cũ |
| **A2** | thêm `company_id` **NOT NULL**, nhân bản giá hiện có cho 8 công ty | 264.646 → **~2,1 triệu** dòng | **44 file** phải biết truyền công ty |
| **B** | bảng giá mới riêng cho HRM, ERP giữ bảng cũ | 2 nguồn giá song song | không, nhưng **2 nguồn sự thật** — giá lệch nhau mà không ai biết |

Khuyến nghị **A1**: ERP chạy nguyên, dữ liệu không phình, và đúng thực tế nghiệp vụ (phần lớn hàng
hoá dùng chung một giá, chỉ một số ít cần giá riêng theo công ty).

#### 3 câu cần user trả lời

1. **Công ty chưa khai giá riêng thì lấy giá nào?** Dùng giá chung (A1 làm được ngay) hay bắt buộc
   phải khai đủ 8 công ty mới bán được?
2. **Phạm vi bao nhiêu công ty?** Cả 8, hay chỉ những công ty thực sự kinh doanh hàng hoá (đo theo
   `products.company_id` thì chỉ 4 công ty từng tạo hàng hoá)?
3. **264.646 dòng giá đang có thuộc về ai?** Giá chung (A1), hay quy về công ty 1 rồi 7 công ty còn
   lại khai lại từ đầu?

⚠️ Chưa chốt 3 câu này thì **chưa mở được màn quản lý giá** ở §18a — vì cấu trúc bảng quyết định
toàn bộ màn đó.

### 20. Phạm vi Phase 2 sau khi tách giá (user chốt 22/09/2026)

> User: *"để tránh context quá dài, chúng ta sẽ tập trung chuyển đổi phần thông tin hàng hoá trước,
> quản lý giá sẽ xử lý tiếp ở phase sau"*

Toàn bộ phần giá — màn quản lý giá (§18a) **và** bảng giá theo công ty (§19) — chuyển sang
**Phase 8**. 3 câu hỏi ở §19 là cổng của Phase 8, KHÔNG còn chặn Phase 2.

**Phase 2 từ đây chỉ còn phần THÔNG TIN hàng hoá:**

| | Trong Phase 2 | Sang Phase 8 |
|---|---|---|
| `products` (thông tin, phân loại, thuế, hải quan…) | ✅ | |
| `product_units` — danh sách ĐVT, hệ số, đơn vị cơ bản | ✅ | |
| `product_units.cost_price` / `buy_price` | | 💰 |
| `product_unit_prices` (6 loại giá) | | 💰 |
| `product_expected_prices` (giá chờ hiệu lực) | | 💰 |
| Luồng duyệt giá (BB-1, `*_wait_approve`) | | 💰 |
| `attribute_products`, `product_suppliers`, tài liệu/ảnh/video | ✅ | |
| công thức + 3 bảng phụ kiện, `product_company_coefficients` | ✅ | |
| `productables` — tab Phân loại xe / Nhóm máy | ✅ | |

**Form tạo/sửa: 6 tab → 5 tab** (bỏ tab "Giá bán").

**Task đổi theo:**

- **C2** `POST /products` — bỏ toàn bộ khối giá. ⇒ **hết mâu thuẫn BB-2**: 4 rule `required` của ERP
  (`cost_price`, `sale_max_percent_coefficient`, `prices`, `prices.*.coefficient`) không còn nằm
  trong form này nên không phải chọn phương án nào cả. `ProductRequest` gỡ hẳn các rule đó.
- **C3** `PUT /{id}` — bỏ nhánh BB-1 (duyệt giá).
- **D4** — chỉ còn tab 4 (Dữ liệu quản trị).
- **B3** (đã xong) — gate giá ở API chi tiết **giữ nguyên**: `GET /{id}` vẫn trả `null` cho
  `cost_price` / `buy_price` khi không có quyền. Màn chi tiết vẫn hiện giá (chỉ đọc), chỉ là không
  sửa được ở đây nữa.

⚠️ **`product_units` bị chia đôi trách nhiệm** — Phase 2 ghi ĐVT, Phase 8 ghi 2 cột giá trên CÙNG
dòng. Task C2/C3 phải để nguyên `cost_price` / `buy_price` khi ghi (không gán 0, không gán null),
nếu không mỗi lần sửa thông tin hàng hoá là xoá mất giá.

### 21. "Nhóm máy" — giữ bảng `groups` sống, chỉ với vai trò Nhóm máy (user chốt 22/09/2026)

Trả lời câu hỏi treo từ §15d số 1. Bảng `groups` (893 dòng) đang gánh **2 vai**:

| Vai | Quyết định |
|---|---|
| Danh mục *"Nhóm hàng hoá"* cũ của ERP | **BỎ MÀN** — như đã chốt ở Phase 5 |
| Nguồn dữ liệu *"Nhóm máy"* để gắn phụ kiện | ✅ **GIỮ** — bảng tiếp tục sống |

⇒ **Phase 5 bỏ MÀN DANH MỤC, KHÔNG xoá bảng.** Đây là điểm dễ hiểu nhầm nhất: "gỡ danh mục nhóm
hàng hoá" từ nay nghĩa là gỡ màn quản lý, còn bảng `groups` vẫn là danh mục máy.

Vì sao chọn hướng này: 3.968 liên kết Nhóm máy đang sống, dữ liệu bên trong đúng là tên máy
("Máy rửa áp lực cao nước lạnh" 333 hàng hoá · "Cầu nâng 2 trụ thủy lực có cổng" 247 · "Máy ra vào
lốp xe con" 165). Ánh xạ 893 nhóm sang cây mới hay tạo bảng `machine_groups` riêng đều phải di trú
dữ liệu — rủi ro không tương xứng với lợi ích ở giai đoạn này.

#### 21a. Khối Nhóm máy bên ERP là 2 TẦNG, không phải một ô

Đọc `products/form.blade.php:353`. Card **"Phụ tùng – Phụ kiện"** (ERP hiện khi loại cũ là
`accessories` / `common_components…` / `special_components…`):

```
Nhóm máy   — ô chọn NHIỀU, đổ từ `groups`
   └─ Máy  — BẢNG con, chỉ hiện khi đã chọn nhóm (ng-if="group_ids_use.length"),
             thêm từng máy qua popup tìm hàng hoá
```

Cả hai cùng ghi vào `productables`, phân biệt bằng `productable_type`:

| | `productable_type` | Dòng | Hàng hoá |
|---|---|---:|---:|
| Nhóm máy | `App\Model\Product\Group` | **3.968** | 2.874 |
| Máy sử dụng | `App\Product` | **28.398** | 2.975 |

⚠️ Đây là 2 trong 5 loại quan hệ của bảng `productables` — mọi thao tác ghi phải kẹp
`productable_type`, xem §15a bẫy 2.

#### 21b. Điều kiện hiện tab

Tab **Nhóm máy** hiện theo cờ `product_types.declare_machine_group` (§18b), thay cho điều kiện cũ
của ERP là enum `products.product_type` ∈ 3 giá trị. Cùng cơ chế với tab Phân loại xe
(`declare_vehicle`).

### 22. QUY TRÌNH — chốt spec + mockup TRƯỚC, không động source dự án (user chốt 22/09/2026)

> User: *"chưa động tới source dự án trước khi tôi yêu cầu, chốt spec + mockup trước"*

Thứ tự bắt buộc cho mọi yêu cầu mới:

```
1. Ghi vào spec (design.md)         ← luôn làm ngay
2. Dựng/sửa MOCKUP để user nhìn     ← `pages/master-data/mockup-hang-hoa/` (thư mục sẽ xoá sau khi chốt)
3. CHỜ user chốt
4. Mới đụng source thật             ← BE `Modules/`, FE màn thật, migration
```

**Mockup KHÔNG tính là source dự án** — nó là bản vẽ, nằm riêng một thư mục và sẽ xoá.

⚠️ Áp dụng cho cả những việc nhìn "nhỏ và chắc chắn đúng": thêm cột, thêm ô tick, thêm màn danh
mục. Lý do là ở nhịp làm việc: yêu cầu còn đang thay đổi từng ngày (3 lần đổi lớn chỉ trong
22/09), code sớm là code phải sửa lại hoặc phải gỡ ra.

### 23. Tab "Dữ liệu quản trị" — BỎ tab lồng theo Công ty (user chốt 22/09/2026)

> User: *"Tab dữ liệu quản trị không chia tab theo Công ty nữa ⇒ Công ty nào tự khai báo của Công
> ty đó"*

**Đảo lại §2** (quyết định 21/09 "tab 5 + tab 6 theo từng công ty → tách sang Phase 3").

| | Trước | Sau |
|---|---|---|
| Bố cục | 1 tab lồng cho MỖI công ty (Tân Phát · Tân Phát ETEK · …) | **một khối duy nhất** |
| Người khai | ai mở form cũng thấy dữ liệu của mọi công ty | **công ty nào khai của công ty đó** |
| Phạm vi dữ liệu | do người dùng chọn tab | **do công ty đang đăng nhập quyết định** |

Bỏ tab lồng làm form gọn hẳn: tab Dữ liệu quản trị từ 2 tầng còn 1 tầng.

#### 23a. 3 câu cần chốt trước khi code

1. **Đọc:** người của công ty A mở hàng hoá thì chỉ thấy dữ liệu quản trị của công ty A, hay vẫn
   xem được của công ty khác ở chế độ chỉ đọc?
2. **Ghi:** công ty A có được sửa dữ liệu của công ty B không (vd người ở tổng công ty)? Nếu không
   thì đây là ràng buộc phải chặn ở **BE**, không chỉ ẩn ở FE.
3. **"Công ty đang đăng nhập" lấy ở đâu:** `employee_infos.company_id` của người dùng, hay có ô
   chọn công ty riêng cho người thuộc nhiều công ty?

#### 23b. Việc phát sinh ở CSDL — cần chốt cùng §19

Các trường trong tab này hiện **không có chiều công ty** ở DB:

| Trường | Bảng | Có `company_id`? |
|---|---|---|
| Nhà cung cấp | `product_suppliers` | ❌ |
| SL tồn kho tối thiểu | `products.min_stock_qty` | ❌ (một cột đơn) |
| Bảo hành + Đơn vị bảo hành | `products.guarantee` | ❌ |
| Hệ số công nghệ | `product_company_coefficients` | ✅ — **tiền lệ duy nhất** |

⇒ "Công ty nào khai của công ty đó" muốn đúng nghĩa thì 3 nhóm trên phải thêm chiều công ty —
**cùng loại thay đổi CSDL với §19 (bảng giá theo công ty)**. Đề xuất gộp 2 việc này chốt một lượt
để không phải đổi bảng hai lần.

⚠️ Chừng nào chưa chốt: mockup dựng **một khối duy nhất** (đúng bố cục mới), còn dữ liệu vẫn là
một bộ chung như ERP đang chạy.

#### 23c. Đáp án 3 câu ở §23a (user chốt 22/09/2026)

> 1. *"Chỉ thấy dữ liệu của công ty mình"*
> 2. *"Cấm tuyệt đối"* (sửa dữ liệu công ty khác)
> 3. *"Lấy theo company_id user đang đăng nhập ⇒ trên HRM cho phép user có vai trò ở nhiều công ty
>    ⇒ trên topbar có button cho phép đổi Công ty"*

**Đây là ràng buộc BẢO MẬT, không phải tiện ích giao diện.** "Cấm tuyệt đối" ⇒ chặn ở **BE**, cả
đường đọc lẫn đường ghi; FE ẩn chỉ là lớp trải nghiệm.

**⚠️ Nguồn sự thật của "công ty đang đăng nhập" là `employee_infos.company_role`, KHÔNG phải
`employee_infos.company_id`.** Đây là chỗ rất dễ lấy nhầm:

| Cột | Nghĩa |
|---|---|
| `company_id` | công ty **gốc** của nhân viên (nơi ký hợp đồng) |
| `company_role` | công ty **đang chọn trên topbar** — thứ quyết định phạm vi dữ liệu |

Cơ chế có sẵn, đã dò trong mã nguồn (KHÔNG tự dựng lại):

- Nút đổi công ty: `components/BasicSubsystem.vue:130` — đổ từ `$store.state.company_roles`
- Bấm đổi → `POST human/employee-infos/{id}/update-company-role` (`company_role: <id>`) →
  `EmployeeInfoService::updateCompanyRole()` ghi `employee_infos.company_role` rồi FE `$router.go(0)`
  tải lại trang. Nghĩa là lựa chọn **lưu ở máy chủ**, không phải state tạm của trình duyệt.
- Danh sách công ty một người được vào: bảng `company_employees`

**Số đo 22/09/2026:** `company_employees` **1.172 dòng / 1.102 nhân viên / 8 công ty**; **53 người
thuộc nhiều hơn 1 công ty** — tính năng này đang được dùng thật, không phải lý thuyết.
⚠️ Nhưng `employee_infos` chỉ có **29/1.119** dòng đã đặt `company_role` ⇒ **phải có đường lùi khi
cột này rỗng** (lấy `company_id`), nếu không 1.090 người mở màn ra sẽ trắng dữ liệu.

#### 23d. Việc phát sinh để làm được "cấm tuyệt đối"

| Việc | Ghi chú |
|---|---|
| Hàm dùng chung lấy công ty hiện tại | `company_role ?: company_id`, đặt ở service dùng chung — KHÔNG rải `auth()->user()->info->company_role` khắp nơi |
| Lọc dữ liệu quản trị theo công ty đó ở **đường đọc** | `GET /products/{id}` chỉ trả khối dữ liệu quản trị của công ty hiện tại |
| Chặn ghi ở **đường ghi** | gửi `company_id` khác công ty hiện tại ⇒ **403**, không phải bỏ qua im lặng |
| Ca kiểm bắt buộc | 2 token của 2 công ty khác nhau, đọc + ghi chéo phải bị chặn (kiểu ca 403 của Phase 1/2b) |

⚠️ **Chưa làm được chừng nào chưa chốt §23b** — 3/4 nhóm trường của tab này ở DB chưa có cột
`company_id` (`product_suppliers`, `products.min_stock_qty`, `products.guarantee`). Không có chiều
công ty trong dữ liệu thì không có gì để lọc, và "cấm tuyệt đối" thành câu khẩu hiệu.

### 24. THIẾT KẾ CSDL cho "mỗi công ty tự khai" (user chốt 22/09/2026: update database)

Đáp án cho §23b. Dưới đây là **bản thiết kế để duyệt**, chưa viết migration (§22).

#### 24a. Hiện trạng 5 trường của tab Dữ liệu quản trị

| Trường | Đang ở đâu | Dữ liệu đang có | Có chiều công ty? | ERP đọc ở |
|---|---|---:|---|---:|
| Nhà cung cấp | `product_suppliers` | 1.741 dòng / 1.740 hàng hoá | ❌ | 21 file |
| SL tồn kho tối thiểu | `products.min_stock_qty` | 754 hàng hoá khác 0 | ❌ | **29 file** |
| Bảo hành + Đơn vị | `products.guarantee` · `guarantee_type` | 23.869 hàng hoá | ❌ | 86 file |
| Hệ số công nghệ | ~~`product_company_coefficients`~~ 🔄 **SAI — sửa 04/10/2026:** là `products.tech_coefficient` (decimal 10,2, mặc định 1.00; 32.398 hàng = 1, 11.156 = 0, còn lại 1.25–2) — hệ số hưởng của kỹ thuật khi lắp đặt, chép sang phiếu phân công lắp đặt. `product_company_coefficients.coefficient` là **HỆ SỐ GIÁ** (nhân vào giá bán), khác hẳn | ❌ (cột chung) | — |
| Chính sách kinh doanh | **🔴 KHÔNG CÓ CỘT NÀO** | — | — | — |

🔴 **Phát hiện khi khảo sát:** mockup và `ProductRequest` đều có "Chính sách kinh doanh"
(`business_policy_id`) nhưng **`products` không có cột đó**. §3 chốt nó thay cho enum cũ
`product_cate`, mà cột mới thì chưa ai tạo. Hiện nó là ô **không lưu được** — phải làm trong đợt này.

#### 24b. Phương án: MỘT bảng thiết lập theo công ty, XOÁ cột chung (user chốt 22/09/2026)

> User: *"min_stock_qty vẫn xử lý tạo vào bảng riêng theo công ty, xoá bỏ cột chung, note lại việc
> cần rà soát xử lý ở các file có sử dụng"*

Mở rộng chính `product_company_coefficients` — khoá `(product_id, company_id)` đã đúng sẵn:

```
product_company_coefficients   (product_id, company_id)
  + business_policy_id      ← mới, chưa từng có chỗ lưu
  + min_stock_qty           ← CHUYỂN từ products, rồi XOÁ cột gốc
  + guarantee               ← CHUYỂN từ products, rồi XOÁ cột gốc
  + guarantee_type          ← CHUYỂN từ products, rồi XOÁ cột gốc
    coefficient             ← đã có
```

`product_suppliers` thêm thẳng `company_id` (bảng nối, không gộp được).

**Vì sao không tạo bảng mới:** khoá `(product_id, company_id)` đã tồn tại đúng như vậy ở
`product_company_coefficients`, và 19 file ERP đang đọc nó. Tạo bảng thứ hai cùng khoá là 2 nguồn
sự thật cho cùng một khái niệm.
⚠️ Tên bảng sẽ không còn khớp nội dung (không chỉ chứa "coefficient"). **KHÔNG đổi tên** — 19 file
ERP đang gọi; ghi chú rõ trong docblock Entity.

#### 24c. 🔴 Hệ quả: XOÁ cột chung là ERP mất nguồn đọc — phải rà từng file

Đây là phần **rủi ro nhất của cả Phase 2**. Khác với các quyết định trước (giữ cột cũ làm giá trị
chung), lần này cột bị xoá hẳn ⇒ mọi chỗ ERP đang đọc đều phải sửa, không có đường lùi im lặng.

**Đo 22/09/2026** — đã lọc bỏ các file của `product_templates` / `product_infos` (2 bảng khác cũng
có cột trùng tên, thuộc nhóm "GIỮ NGUYÊN bên ERP"):

| Cột bị xoá | File ERP phải rà | File HRM |
|---|---:|---:|
| `products.min_stock_qty` | **29** | 3 |
| `products.guarantee` · `guarantee_type` | **42** | 7 |

⚠️ Con số 42 / 86 nêu ở lượt khảo sát ĐẦU là **grep thô**, tính cả `product_templates` /
`product_infos` (2 bảng "GIỮ NGUYÊN bên ERP" cũng có cột trùng tên). Sau khi lọc: `min_stock_qty`
**29 file**, `guarantee_type` **42 file**.

🔴 **Bảo hành còn một tầng rủi ro mà `min_stock_qty` không có: giá trị được CHÉP SANG CHỨNG TỪ.**
`guarantee_type` xuất hiện ở **23 bảng** — báo giá, hợp đồng, phân tích dự án, biên bản bàn giao,
hàng tạm… Lúc lập chứng từ, ERP chép giá trị từ hàng hoá sang dòng chứng từ (khuôn
`$item->guarantee_type = $product->guarantee_type`).

⇒ Khi bảo hành thành dữ liệu theo công ty, **mọi chỗ chép phải chọn đúng công ty của chứng từ**,
không phải công ty của người đang thao tác. Chép nhầm thì chứng từ mang số bảo hành của công ty
khác — sai lặng lẽ, và **đóng băng vĩnh viễn** vì chứng từ đã lưu giá trị đó.

**29 file đó chia 4 nhóm:**

| Nhóm | File | Xử lý |
|---|---|---|
| Màn hàng hoá (sẽ chuyển sang HRM) | `ProductsController` · `Product2Controller` · `products/form*.blade.php` · `history.blade.php` · `update_list_products.blade.php` | HRM làm lại, ERP chặn route — thuộc Đợt E |
| Model gốc | `app/Product.php` · `Services/Product/CreateProductService.php` | đổi sang đọc bảng theo công ty |
| Job nền + đồng bộ | `UpdateGenerateProduct` · `GenerateProduct` · `createTemplateProduct` · `CreateTemplateProductMissing` · `ProductSettingMailJob` · `SyncProductController` · `ProductsImportZitec` | 🔴 **chạy ngầm, không ai thấy khi hỏng** — phải rà kỹ nhất |
| Báo cáo | `WarehouseWarningReportController` (cảnh báo tồn) · `StockTransferReportService` · `ExportLargeProductList` | quyết định lấy theo công ty nào khi in báo cáo |

⚠️ **Nhóm Job nền là chỗ nguy hiểm nhất**: sai ở đây không có màn hình nào báo lỗi, chỉ lộ ra khi
số liệu lệch sau vài ngày.

⇒ Việc rà 29 file này là **một task riêng của Đợt E ("làm ERP không lỗi")**, không nhét vào
migration. Migration chỉ chuyển dữ liệu; đổi code ERP làm sau và nghiệm thu riêng.

#### 24c-1. Quyết định chốt 22/09/2026

| Câu hỏi | Chốt |
|---|---|
| `guarantee` / `guarantee_type` xử lý thế nào | **giống `min_stock_qty`** — chuyển vào bảng theo công ty, xoá cột chung, rà 42 file |
| `company_id` ở `product_suppliers` | **BẮT BUỘC** (NOT NULL) |
| Chặn trùng `(hàng hoá, NCC, công ty)` | **không cần** |

Hệ quả của "company_id bắt buộc": **1.741 dòng `product_suppliers` hiện có phải gán về một công
ty** khi chuyển dữ liệu. Không còn khái niệm "nhà cung cấp chung" — công ty chưa khai thì không có
dòng nào, màn hiện trống.

⚠️ Điều này **khác hướng đã đề xuất cho bảng giá ở §19** (phương án A1: `company_id` nullable,
`NULL` = giá chung, ERP không phải sửa). Hai bảng cùng một bài toán mà hai kiểu là khó giải thích
về sau — xem §24f.

**Thứ tự bắt buộc:**

```
1. Thêm cột mới vào bảng theo công ty   (chưa xoá gì — ERP vẫn chạy)
2. Chép dữ liệu sang, đối chiếu đủ số dòng
3. Sửa 29 file ERP + HRM sang đọc nguồn mới
4. Nghiệm thu ERP không vỡ
5. MỚI xoá cột trên `products`
```

Xoá cột ở bước 1 là 29 chỗ hỏng cùng lúc.

#### 24d. Gộp chung với §19 (bảng giá theo công ty)

Cùng một bài toán, cùng một cách chữa (thêm chiều công ty + giữ đường lùi cho ERP). Đề nghị **một
đợt migration duy nhất** thay vì đổi bảng hai lần:

| # | Thay đổi | Bảng |
|---|---|---|
| 1 | `+ company_id` (nullable) | `product_unit_prices` · `product_expected_prices` |
| 2 | `+ company_id` | `product_suppliers` |
| 3 | `+ business_policy_id`, `min_stock_qty`, `guarantee`, `guarantee_type` | `product_company_coefficients` |

**Xoá 3 cột của `products`** (`min_stock_qty` · `guarantee` · `guarantee_type`) — nhưng chỉ ở
**bước 5** của trình tự nêu ở §24c, sau khi đã rà xong 29 file ERP.
**Không** nhân bản dữ liệu ra 8 công ty — dòng hiện có chuyển thành bản của công ty gốc.

#### 24e. Còn phải chốt trước khi viết migration

1. **`company_id` nullable hay NOT NULL** ở `product_suppliers`? Nullable = dòng cũ thành "nhà cung
   cấp chung", khớp cách làm ở §19 A1. NOT NULL thì 1.741 dòng phải gán về một công ty.
2. **Khoá unique**: `product_suppliers` có nên unique theo `(product_id, supplier_id, company_id)`
   không? Hiện chưa có ràng buộc nào chặn trùng.
3. **Khi công ty chưa khai** thì hiện giá trị chung (lùi về `products`) hay để trống? — cùng câu
   với §19 câu 1, nên trả lời một lần cho cả hai.

#### 24f. ⚠️ Lệch hướng giữa §19 (giá) và §24 (dữ liệu quản trị) — cần chốt lại một lần

| | §19 — bảng giá | §24 — dữ liệu quản trị |
|---|---|---|
| `company_id` | nullable, `NULL` = giá chung *(đề xuất A1)* | **NOT NULL** *(user chốt 22/09)* |
| Cột/dòng cũ | giữ nguyên làm giá trị chung | **xoá cột chung**, gán dữ liệu về công ty |
| ERP phải sửa | **0 file** | **71 file** (29 + 42) |
| Công ty chưa khai | dùng giá chung | **trống** |

Hai bảng cùng một bài toán "thêm chiều công ty" mà đi hai hướng ngược nhau. Đề nghị chốt lại **một
hướng duy nhất** trước khi viết migration:

- **Hướng A (ERP an toàn)** — nullable + giữ giá trị chung cho cả hai. Ít rủi ro nhất, nhưng có
  khái niệm "dữ liệu chung" song song với dữ liệu theo công ty.
- **Hướng B (sạch dữ liệu)** — NOT NULL + xoá cột chung cho cả hai. Mô hình rõ ràng, nhưng phải rà
  **71 file + 44 file đọc chuỗi giá = 115 file ERP**, và 264.646 dòng giá phải gán công ty.

Hiện §19 đang theo A, §24 đang theo B.

### 25. PHÂN TÍCH LẠI §19 — bảng giá theo công ty (22/09/2026)

Xem lại sau khi §24 chốt hướng B (NOT NULL + xoá cột chung). Hai điểm dưới đây **sửa lại chính đề
xuất §19 ban đầu của tôi**.

#### 25a. Đính chính 1 — `product_expected_prices` KHÔNG cần `company_id`

§19 đề xuất thêm `company_id` vào **cả hai** bảng. Sai. Đo lại cấu trúc:

```
product_unit_prices  (id, product_unit_id, price_type_id, …)     264.646 dòng
  └─ product_expected_prices (unit_price_id → product_unit_prices.id)   95.266 dòng / 45.153 giá gốc
```

`product_expected_prices` nối vào giá gốc qua `unit_price_id`, nên **thừa hưởng công ty từ cha**.
Thêm `company_id` vào đây là dữ liệu thừa, và mở đường cho trạng thái mâu thuẫn (giá gốc của công ty
A mà giá chờ hiệu lực ghi công ty B).

⇒ Chỉ thêm `company_id` vào **`product_unit_prices`**.

#### 25b. Đính chính 2 — phạm vi ERP là **34 file**, không phải 44

Lọc bỏ `product_templates` / `product_infos` / nhóm `pi_*` (đều thuộc diện "GIỮ NGUYÊN bên ERP"):
**34 file**, chia theo thư mục: `app/Model/Product` 6 · `app/Jobs` 5 · `Http/Controllers` 4 ·
`ExcelImports` 4 · `Services/Sale/Firm/*` 4 · `Console/Commands` 2 · còn lại rải rác.

#### 25c. 🔴 Vấn đề §19 CHƯA xử lý: `product_units` đang trộn 2 loại dữ liệu

Đây là điểm quan trọng nhất của lượt phân tích lại.

| Cột trên `product_units` | Bản chất | Theo công ty? |
|---|---|---|
| `unit_id`, `is_base`, `unit_coefficient` | **cấu trúc hàng hoá** — Cái / Thùng, 1 Thùng = 12 Cái | ❌ không |
| `cost_price` (giá vốn), `buy_price` (giá mua ngoài) | **giá** | ✅ có |
| `sale_max_percent_coefficient` | **giá** | ✅ có |

Một bảng 46.560 dòng đang gánh cả hai. Nếu chỉ thêm `company_id` vào `product_unit_prices` như §19
đề xuất thì **giá bán tách theo công ty, còn giá vốn vẫn dùng chung** — nửa vời, và là đúng thứ
người dùng sẽ phát hiện ngay ở màn giá.

Nếu thêm `company_id` thẳng vào `product_units` thì mỗi công ty có **bộ đơn vị tính riêng** —
sai bản chất (Cái/Thùng không đổi theo công ty) và nhân 46.560 dòng lên 8 lần.

#### 25d. Hai phương án, cần chốt

**Phương án 1 — tách tầng giá ra khỏi `product_units`** *(đúng mô hình)*

```
product_units          (product_id, unit_id, is_base, unit_coefficient)        ← chung, bỏ 3 cột giá
product_company_units  (product_unit_id, company_id, cost_price, buy_price,    ← MỚI, theo công ty
                        sale_max_percent_coefficient)
  └─ product_unit_prices (+ company_id)                                        ← theo công ty
       └─ product_expected_prices                                              ← thừa hưởng
```

- ✅ Mô hình sạch, ĐVT dùng chung đúng bản chất, mọi thứ "giá" nằm cùng một tầng
- ❌ Thêm 1 bảng mới; 34 file ERP đọc `product_units->cost_price` phải sửa; dữ liệu phải chuyển

**Phương án 2 — chỉ thêm `company_id` vào `product_unit_prices`** *(tối thiểu)*

- ✅ Ít việc nhất, không đụng `product_units`
- ❌ **Giá vốn / giá mua ngoài vẫn dùng chung cho 8 công ty** — mâu thuẫn với yêu cầu "bảng giá độc
  lập". Cần user xác nhận giá vốn có thuộc phạm vi "bảng giá" hay không

⇒ **Câu quyết định:** *"bảng giá độc lập theo công ty"* có bao gồm **giá vốn / giá mua ngoài**
không, hay chỉ là **6 loại giá bán**?

- Có → Phương án 1
- Không → Phương án 2

#### 25e. Gán công ty cho 264.646 dòng giá hiện có

Theo hướng B (`company_id` NOT NULL) thì dữ liệu cũ phải có chủ. Đo phân bố theo công ty **chủ của
hàng hoá**:

| Công ty | Số ĐVT | Số dòng giá |
|---|---:|---:|
| 1 — Tân Phát | 45.477 | **258.270** |
| 4 — Tân Phát Sài Gòn | 1.056 | 6.215 |
| 3 — Chi nhánh Vinh | 23 | 138 |
| 2 — CN Hải Phòng | 3 | 18 |
| *(không có công ty)* | 1 | 5 |

⇒ Quy tắc gán rõ ràng, không mơ hồ: **`company_id` của dòng giá = `products.company_id` của hàng
hoá đó**. Riêng **5 dòng của hàng hoá không có công ty** phải xử lý tay trước khi đặt NOT NULL.

⚠️ Sau khi gán: 7 công ty còn lại **không có dòng giá nào**. Muốn bán thì phải khai giá — đó đúng
là ý "mỗi công ty tự khai", nhưng cần user biết trước để chuẩn bị nhập liệu, không thì ngày bật
tính năng là 7 công ty không bán được hàng nào.

---

### 26. LOGIC XÂY DỰNG HÀNG HOÁ 3 BƯỚC + CHIA SẺ GIỮA CÔNG TY (user chốt 23/09/2026)

> Nguyên văn yêu cầu: `yeu-cau-khach.md` mục "LOGIC XÂY DỰNG HÀNG HOÁ (23/09/2026)".
> Đây là **quyết định đổi cục diện Phase 2**: hàng hoá không còn là "1 màn danh sách + 1 form"
> mà là **quy trình 3 trạng thái, trạng thái tính theo TỪNG CÔNG TY**.

#### 26a. Bộ trạng thái mới — theo từng công ty

| # | Trạng thái | Màn hình chứa nó | Ai đưa vào |
|---|---|---|---|
| 1 | **Đang nhập thông tin** | "Hàng hoá đang nhập thông tin" | Lưu nháp ở bước 1 |
| 2 | **Chờ tính giá bán** | "Hàng hoá chờ tính giá" | Bấm **Lưu** ở bước 1 |
| 3 | **Đang tính giá** | "Hàng hoá chờ tính giá" | **Lưu tạm** ở bước 2 |
| 4 | **Đang kinh doanh** | "Danh mục hàng hoá kinh doanh" | **Lưu & duyệt giá bán** ở bước 2 |

⚠️ **Trạng thái KHÔNG thuộc về mã hàng, mà thuộc về cặp (mã hàng × công ty).**
Cùng một mã: TPE = "Đang kinh doanh", Power = "Đang nhập thông tin".

#### 26b. 3 màn hình + 2 quyền

| Màn | Trạng thái lấy vào | Quyền |
|---|---|---|
| Hàng hoá đang nhập thông tin | 1 | **Nhập thông tin hàng hoá** |
| Hàng hoá chờ tính giá | 2, 3 | **Tính giá bán hàng hoá** |
| Danh mục hàng hoá kinh doanh | 4 | *(chưa chốt — xem tồn 26g-3)* |

Hàng hoá "Đang kinh doanh" là nguồn của **mọi popup tìm kiếm hàng hoá** (báo giá / hợp đồng / …).

#### 26c. Quy tắc chủ quản

**Hàng hoá của công ty nào thì người có quyền của công ty đó xây dựng/cập nhật.**
Khớp §23c đã chốt (chỉ thấy dữ liệu công ty mình, cấm sửa chéo công ty, chặn ở BE).

#### 26d. Chia sẻ hàng hoá giữa các công ty

- Công ty B lấy hàng hoá công ty A đã tạo về → **khai thêm dữ liệu quản trị của B** → tự tính giá bán của B.
- Nút **"Xem hàng hoá Công ty khác"** đặt ở màn "Hàng hoá đang nhập thông tin":
  - Quyền dùng nút = **Nhập thông tin hàng hoá** (không thêm quyền mới).
  - Popup liệt kê hàng hoá **do công ty khác tạo** mà **công ty của user chưa dùng** (chưa xuất hiện ở cả 3 màn trên).
  - Bộ lọc: **công ty quản lý (công ty tạo ra)** + **danh mục phân loại hàng hoá**.
  - **Checkbox chọn nhiều** → bấm Chọn → hàng hoá rơi vào màn "Hàng hoá đang nhập thông tin" của công ty user, rồi chạy tiếp quy trình 3 bước.

#### 26c-bis. AI ĐƯỢC SỬA GÌ — 3 mức quyền trên cùng một form (user chốt 23/09/2026)

> User: *"Khi tính giá không được sửa thông tin hàng hoá. Công ty A lấy hàng hoá Công ty B về ⇒ chỉ
> được nhập thông tin quản trị theo công ty ⇒ tính giá, không được sửa thông tin khác của hàng hoá."*

| Trường hợp | Sửa được | Khoá |
|---|---|---|
| Công ty **tạo ra** hàng hoá, vai *Nhập thông tin hàng hoá* | **toàn bộ 6 tab** | — |
| Công ty **lấy hàng của công ty khác về**, vai *Nhập thông tin hàng hoá* | **chỉ tab "Dữ liệu quản trị"** (dữ liệu riêng của công ty mình) | 5 tab còn lại |
| Bất kỳ công ty nào, vai *Tính giá bán hàng hoá* | **chỉ tab "Giá bán"** | cả 6 tab thông tin |

⇒ **Thông tin DÙNG CHUNG của hàng hoá chỉ có một chủ: công ty đã tạo ra nó.** Công ty đi mượn chỉ
đắp thêm lớp dữ liệu của riêng mình (dữ liệu quản trị + giá), không đụng vào lớp chung.

🔒 **BE phải chặn, không chỉ khoá ở FE** (đồng bộ §23c): endpoint cập nhật hàng hoá phải so
`products.company_id` với công ty của người đăng nhập; lệch thì **chỉ nhận đúng phần dữ liệu quản trị
+ giá của công ty đó**, mọi trường thuộc lớp chung bị bỏ qua hoặc trả lỗi.

📌 Việc này trả lời một phần **tồn 26g-6** (*"công ty B sửa tên/model của hàng hoá do A tạo thì A có
bị đổi theo không"*): **không sửa được, nên không có chuyện đổi theo**. Phần còn lại của tồn 26g-6 —
A sửa thì B có thấy đổi không — vẫn chờ chốt (hệ quả trực tiếp của tồn 26g-5: chép hay tham chiếu).

#### 26d-bis. Tab "Phân loại xe" — bộ ba hàng hoá × Model × Đời xe (đối chiếu ERP 23/09/2026)

Đọc lại `products/form.blade.php:424-596` (khối **"Phụ tùng ô tô"**) thì ERP KHÔNG có ô *Đời xe*
phẳng — đoạn đó **đã bị comment**. Cấu trúc thật:

| Thành phần | Chi tiết |
|---|---|
| Hãng xe | chọn nhiều, **bắt buộc**, kèm ô tick **"Chọn tất cả"** |
| Loại xe | chọn nhiều, lọc theo Hãng xe, kèm **"Chọn tất cả"** |
| Model xe | chọn nhiều, lọc theo Hãng + Loại, kèm **"Chọn tất cả"** |
| Ô tick chung | **"Áp dụng tất cả đời xe cho model"** |
| **Bảng bộ ba** | cột *Hãng xe* (gộp dòng theo hãng — `rowspan="getRowSpanManu()"`) · *Loại xe* · *Model xe* · **Đời xe = ô chọn nhiều RIÊNG cho từng model** + "Chọn tất cả" trong ô |

✅ **Chốt luôn tồn §3.3 / §15d "cách hiển thị Đời xe"**: đi theo **bảng con dưới mỗi model** — đúng
cấu trúc dữ liệu `product_vehicle_model_has_life` (48.736 dòng) và đúng ERP đang chạy. Bỏ phương án
"một ô chọn nhiều áp chung" mà mockup dựng tạm hôm 21/09.

#### 26d-ter. Tab "Nhóm máy" — đối chiếu ERP

Khối **"Phụ tùng – Phụ kiện"** (`form.blade.php:353-421`):

- Ô **Nhóm máy** chọn nhiều.
- Bảng **Máy** — nhãn **bắt buộc**, **CHỈ HIỆN khi đã chọn ít nhất 1 nhóm máy**
  (`ng-if="product.group_ids_use.length"`); cột STT · Mã máy · Tên máy · nút thêm/xoá;
  không có dòng nào thì hiện **"Không có máy"**.
- Cả 2 tầng cùng ghi vào `productables`, khác `productable_type` (xem bẫy ở sổ chốt).

⚠️ Bên ERP hai khối này **hiện theo `products.product_type`** (`automotive_parts` cho xe;
`accessories` / `common_components…` / `special_components…` cho nhóm máy). Ở HRM, §18b đã chuyển
2 cờ khai báo này sang **Loại sản phẩm (cấp lá)** — mockup để cả 2 tab luôn hiện cho dễ duyệt,
bản thật phải gate theo cờ.

#### 26f. Bộ cột màn danh sách hàng hoá (user chốt 23/09/2026)

**Cột mặc định hiện** — đúng danh sách khách đưa, thêm 3 cột khung:

`STT` · **Ảnh** · **Mã hàng** · **Tên hàng hoá** · **Model** · **Tính chất hàng hoá** ·
**Nhóm chức năng** · **Nhóm sản phẩm** · **Loại sản phẩm** · **Thương hiệu** · **Hãng sản xuất** ·
**Trạng thái đồng bộ** · `Trạng thái` · `Hành động`

Thứ tự: **Ảnh – Mã – Tên** đứng ngay sau STT (user chốt), và 4 cột này **dính trái** khi cuộn ngang.

**Cột còn lại nằm trong popup "Cấu hình cột hiển thị"** (13 cột, tắt sẵn): Barcode · ĐVT · Xuất xứ ·
Code đặt hàng · Tên tiếng Anh · % VAT · Giá vốn · Giá bán · Bảo hành · SL tồn kho tối thiểu ·
Công ty quản lý · Người nhập thông tin · Ngày sửa. `STT` và `Hành động` khoá, không cho tắt.

✅ **3 câu đã chốt (user trả lời 23/09/2026):**

1. *"nhóm hàng hóa"* / *"loại hàng hóa"* → đúng là **Nhóm sản phẩm** / **Loại sản phẩm** của cây
   phân loại Phase 0 — user xác nhận **nhầm sang tên danh mục CŨ**. Giữ nguyên 2 quyết định trước:
   `product_cate` đóng băng (§3), `groups` thành Nhóm máy (§21).
2. **Trạng thái đồng bộ → BỎ HẲN.** Không thêm trường này vào `products`, không có cột ở màn danh
   sách, không có trong popup cấu hình cột.
3. **Ảnh có ở CẢ popup chọn hàng hoá**, không chỉ màn danh sách.

⇒ Bộ cột mặc định còn **13 cột** (bỏ *Trạng thái đồng bộ*), popup cấu hình còn **26 cột**.

#### 26e. Phạm vi sửa CSDL mà yêu cầu này chốt

1. **Dữ liệu quản trị theo công ty** (tab Dữ liệu quản trị)
2. **Bộ trạng thái hàng hoá** — theo công ty
3. **Giá bán VÀ giá vốn** — theo công ty
4. Cập nhật **toàn bộ luồng đang đọc 3 phần trên** sang đọc bảng theo công ty

✅ **Câu §25d coi như đã có đáp án**: yêu cầu ghi rõ *"Giá bán, giá vốn"* ⇒ **giá vốn NẰM TRONG**
phạm vi theo công ty ⇒ phải **tách tầng giá khỏi `product_units`** (Phương án 1 của §25).
*(Cần user xác nhận lại một câu trước khi viết migration — xem tồn 26g-1.)*

#### 26f. Danh sách việc tổng thể phần hàng hoá (user liệt kê)

1. Chuyển toàn bộ danh mục liên quan hàng hoá sang phân hệ "Danh mục dùng chung" — *Phase 1, xong*
2. Chuyển các danh mục phân loại xe — *Phase 2b, xong*
3. **Xây dựng các chức năng xây dựng hàng hoá như trên** — *Phase 2 + Phase 8, đang làm*
4. Chuyển quản lý hàng tạm tương ứng — *Phase 6, làm sau*
5. **Xử lý ảnh hưởng của việc đổi CSDL + đổi logic quản lý** — *user đánh giá là phần KHÓ NHẤT*

#### 26g. 🔴 Tồn mới phát sinh từ §26 — chưa trả lời, ghi lại để quay lại

| # | Tồn | Vì sao quan trọng |
|---|---|---|
| 1 | **Luồng mới có trùng "luồng hỏi giá" đang chạy ở ERP không?** — user tự nêu | ERP đang có sẵn **"Phiếu yêu cầu hỏi giá"** (`PriceAskingRequest`) và **"Phiếu yêu cầu tính giá"** (`PriceCalculateRequest`) ở menu *Mua hàng → Hàng tạm - Hỏi giá*. Nếu "Hàng hoá chờ tính giá" làm đúng việc của phiếu yêu cầu tính giá thì đang có **2 cửa vào cùng một việc** |
| 2 | Trạng thái theo công ty lưu ở đâu | `products.status` hiện là **một cột dùng chung**. Theo công ty ⇒ phải có bảng `product_companies` (hoặc mở rộng bảng dữ liệu quản trị theo công ty) làm **bảng chủ của quan hệ hàng hoá × công ty** |
| 3 | Quyền của màn "Danh mục hàng hoá kinh doanh" | Yêu cầu chỉ nêu 2 quyền cho 2 màn đầu |
| 4 | "Chưa có trong 3 màn" hiểu theo công ty đăng nhập | Cần chốt: điều kiện popup lọc theo **công ty đang đăng nhập**, không phải "chưa công ty nào dùng" |
| 5 | Lấy hàng hoá công ty khác về: **chép** hay **tham chiếu** | Cùng `products.id` dùng chung (chỉ thêm dòng theo công ty) hay sinh mã mới? Ảnh hưởng trực tiếp tới 171 bảng FK |
| 6 | Sửa thông tin CHUNG của hàng hoá công ty khác tạo | Công ty B đổi tên/model của hàng hoá do A tạo thì A có bị đổi theo không |
| 7 | Quay lui trạng thái | Đang kinh doanh → sửa lại thông tin thì có rơi về "Đang nhập thông tin" không |
| 8 | 45.890 hàng hoá cũ vào trạng thái nào | Dữ liệu đang chạy phải được gán trạng thái + công ty khi bật tính năng |

📌 **Chốt cách làm tiếp (user 23/09):** *chưa khảo sát 8 tồn này*, **dựng mockup trước**, xong mockup
mới quay lại giải quyết từng tồn.

---

### 27. BÁO CÁO HÀNG HOÁ THEO CÔNG TY (user yêu cầu 23/09/2026)

> Yêu cầu nguyên văn: *xem đầy đủ thông tin hàng hoá · biết mỗi công ty đang sử dụng những mã hàng
> nào, trạng thái hàng hoá · mỗi mã hàng đang có bao nhiêu công ty kinh doanh/sử dụng.*
> Mockup: `mockup-bao-cao-hang-hoa.html`. Khuôn bám `bao-cao-ke-hoach-lam-viec-nhan-vien.html`.

#### 27a. 4 quyết định đã chốt

| # | Câu | Chốt | Vì sao |
|---|---|---|---|
| 1 | Bố cục | **Ma trận Hàng hoá × Công ty** | 8 công ty là con số cố định, vừa màn hình ⇒ trả lời cả 3 gạch đầu dòng trong MỘT bảng, không phải đổi tab |
| 2 | "Đang sử dụng" | **Có bản ghi trạng thái** với mã hàng đó, dù ở bước nào | Đếm tách 2 số *Khai thác* / *Kinh doanh* nên vừa thấy hàng đang tắc vừa thấy hàng đang bán; không phải nối thêm nguồn chứng từ |
| 3 | Bộ cột | **Dùng lại bộ cột màn danh sách** (§26f) + popup Cấu hình cột | User học một bộ cột dùng được cả 4 màn |
| 4 | Kỳ thời gian | **Không có kỳ — ảnh chụp hiện trạng** | Câu hỏi là "đến hôm nay đang thế nào", khác 4 báo cáo còn lại của phân hệ (đều có kỳ) |

#### 27b. Cấu trúc bảng

| Khối | Cột |
|---|---|
| Định danh — **dính trái** | STT 44 · Ảnh 52 · Mã hàng 150 · Tên hàng hoá 250 |
| **Trạng thái theo công ty** | 8 cột × 58px, ô = chấm màu theo 4 mã màu đã chốt; ô trống = công ty chưa lấy mã về; nhãn **QUẢN LÝ** ở công ty quản lý mã (user chốt 23/09/2026, thay nhãn *CHỦ* của bản đầu) — dùng cùng chữ với cột *Công ty quản lý* và cột *Vai trò* trong popup |
| Số công ty | *Khai thác* 112 · *Kinh doanh* 112 — bấm được, sắp xếp được |
| Thông tin hàng hoá | 7 cột mặc định + 13 cột mở thêm trong Cấu hình cột |

**Khác bộ §26f đúng 2 cột, đều có lý do:** bỏ *Trạng thái* (nay là 8 cột công ty) và *Hành động*
(báo cáo chỉ để xem) ⇒ popup cấu hình còn **24 cột**, không phải 26.

**Khối công ty đặt NGAY SAU tên hàng**, trước các cột thông tin — để ma trận hiện ra mà không phải
cuộn ngang (đo: khối định danh + ma trận + 2 cột đếm = 1.209px, vừa cả 1600 lẫn 1366).

#### 27c. Dải tổng hợp — 2 khối, số tự kiểm được

- **Quy mô danh mục**: Tổng mã hàng · Tổng lượt dùng (Σ mã × công ty) · Bình quân CT/mã · Mã ≥2 công ty
- **Lượt dùng theo trạng thái**: 4 ô — **cộng lại phải đúng bằng "Tổng lượt dùng"**; lệch là dòng meta
  tự đổi thành chữ đỏ báo lệch. Đây là chốt chặn chống sai số âm thầm, giống luật "4 ô chia hết Tổng
  đầu việc" của báo cáo kế hoạch làm việc.

#### 27d. Bộ lọc

Hàng gọn: tìm nhanh (mã · tên · model · barcode) · **Công ty** (chọn nhiều — bỏ tick là **ẩn luôn cột
đó** và trừ khỏi mọi con số) · **Trạng thái** (chọn nhiều) · **Số công ty dùng** (1 / 2–3 / ≥4).
*Bộ lọc nâng cao* (ẩn sẵn, có chip đếm): Tính chất ▸ Nhóm chức năng ▸ Nhóm sản phẩm (lọc dây chuyền)
· Thương hiệu · Hãng sản xuất · Công ty quản lý.

**Lọc nhanh ngay trên tiêu đề bảng (user chốt 23/09/2026):** 4 mục trạng thái ở dải chú giải đầu
bảng **bấm được để bật/tắt**, mỗi mục kèm số lượt dùng của trạng thái đó. Dùng **chung một nguồn
`stChon`** với ô lọc "Trạng thái" trên thanh lọc ⇒ bấm ở đâu cũng đổi cả hai, không bao giờ lệch.
Tắt hết 4 trạng thái thì bảng báo đúng nguyên nhân (*"Chưa bật trạng thái nào…"*) chứ không báo
chung chung "không có dữ liệu".

**Luật đếm của mọi con số trong ô lọc:** số của một ô lọc **bỏ qua chính ô đó**, vẫn tôn trọng các ô
còn lại — để user biết trước bật lại thì được thêm bao nhiêu. Đo thật: gõ "Fusheng" thì 4 số trạng
thái về 3/3/0/7 (= 13 chấm trên ma trận); tắt công ty TPE thì 4 số trạng thái giảm còn 9/11/6/35
(= 61 chấm) trong khi 8 số của ô Công ty **giữ nguyên**.

**KHÔNG in dải ghi chú giả định lên giao diện** (user chốt 23/09/2026 — *"khách hàng không cần đọc"*).
Nội dung cảnh báo phụ thuộc tồn 26g-5 giữ ở §27f dưới đây + một khối chú thích trong nguồn mockup.

#### 27e. 2 popup drill-down

- **Ô ma trận** → *"<Mã> tại <Công ty>"*: vị trí trong quy trình 4 bước · trạng thái + ngày chuyển +
  người nhập · dữ liệu quản trị riêng của công ty · **bảng 6 loại giá** (đúng tên trong `price_types`:
  Bán lẻ · Đại lý cấp 1/2/3 · Giá bán theo lô · Giá bán TMĐT) · thông tin chung kèm câu *"chỉ <công ty
  tạo ra> sửa được"* (đồng bộ §26c-bis).
- **Số ở cột đếm** → danh sách công ty kèm trạng thái, ngày chuyển, người nhập, vai trò *Tạo ra mã* /
  *Lấy về dùng*.

#### 27f. 🔴 Phụ thuộc — báo cáo này KHÔNG tự đứng được

| Tồn | Ảnh hưởng |
|---|---|
| **26g-5** chép hay tham chiếu | Mockup giả định **tham chiếu**. Chốt là *chép mã mới cho từng công ty* thì **ma trận sụp** — mỗi công ty một mã riêng, không còn ô giao nhau; báo cáo phải đổi thành bảng gom theo *mã gốc* |
| **26g-2** trạng thái theo công ty lưu bảng nào | Là **nguồn dữ liệu trực tiếp** của toàn bộ ma trận |
| 26g-8 gán trạng thái cho 45.890 mã cũ | Quyết định bảng này trông thế nào ở ngày bật tính năng |

#### 27g. Còn tồn của riêng màn báo cáo

1. Quyền xem báo cáo — dùng chung quyền của màn "Danh mục hàng hoá kinh doanh" (tồn 26g-3 chưa chốt)
   hay thêm quyền riêng?
2. Có cần **xuất Excel dạng ma trận** (8 cột công ty) hay xuất dạng phẳng 1 dòng = 1 cặp mã × công ty?
   Dạng phẳng dễ lọc bằng PivotTable hơn nhưng khác hẳn cái đang nhìn trên màn.
3. Khi số công ty tăng quá 8 (mở công ty mới) thì ma trận có còn vừa màn hình không — nay vừa khít
   tới 8; tới 12 công ty phải cho cuộn ngang khối ma trận hoặc gộp cột.

---

### 28. CẤU HÌNH GIÁ BÁN NỘI BỘ KHI CHIA SẺ HÀNG HOÁ (user chốt 24/09/2026)

> Nguyên văn yêu cầu: *"Cấu hình cách tính giá bán cho các công ty chia sẻ. Ví dụ TPE xây dựng hàng
> hoá ⇒ chia sẻ cho công ty khác thì cần một công thức để tính giá cho công ty khác. Cấu hình theo
> từng hãng ⇒ từng công ty, % tính theo hàng nhập khẩu hoặc hàng tồn kho."*
> Ví dụ khách đưa — hãng **Muller**, công ty bán **TPE**: *Cách tính giá bán nội bộ: theo giá vốn /
> theo giá bán · Tỷ lệ: POWER (nhập khẩu 1% · tồn kho 2%) · GREEN (tương tự)*.

#### 28a. 8 đáp án chốt trước khi dựng mockup

| # | Câu hỏi | Chốt |
|---|---|---|
| 1 | "Hãng" là bảng nào | **`manufactures` — Hãng sản xuất** (1.071 dòng), không phải `brands`. Cùng bảng ERP đang dùng cho `manufacture_expect_prices` |
| 2 | "Nhập khẩu" / "Tồn kho" | **Hard-code 2 nguồn hàng**, không sinh danh mục mới, **không thêm chiều vào bảng giá**. Mỗi cấu hình có đúng 2 ô % |
| 3 | Gốc tính | **Theo giá vốn** hoặc **theo giá bán**; chọn theo giá bán thì hệ số áp cho **cả 6 loại giá** (`price_types`), vì công ty mua cũng có đủ 6 bảng giá |
| 4 | Sinh giá hay gợi ý | **CHỈ LÀ SỐ GỢI Ý** — cho công ty mua biết mua lại từ công ty bán bao nhiêu. **Không ghi vào bảng giá**; công ty mua tự quyết giá bán của mình |
| 5 | Ai khai | **Mỗi công ty tự khai bộ cấu hình của mình.** Công ty nào cũng có thể là công ty BÁN — cùng hãng Muller nhưng có mã TPE là chủ, có mã POWER là chủ. Khai thì **chọn nhiều hãng một lượt** (28d-bis) nhưng **từng công ty mua một** |
| 6 | Ngày hiệu lực | **KHÔNG có ngày hiệu lực** — một bản hiện hành. Đổi thì ghi **lịch sử chi tiết** (`catalog_histories`) |
| 7 | Hãng chưa cấu hình | **Cảnh báo khi lấy hàng về**, không chặn |
| 8 | Quan hệ cơ chế cũ | **Độc lập** với `manufacture_expect_prices` (87 bản, dừng 12/2022) và `company_price_types` (31 dòng hệ số loại giá) |

#### 28b. Công thức — dấu của % TUỲ GỐC TÍNH

| Gốc tính | Công thức | Ý nghĩa | Ví dụ (Muller, POWER, nhập khẩu 1%) |
|---|---|---|---|
| **Theo giá vốn** | `giá vốn của công ty bán × (1 + %)` | **cộng thêm** — lãi nội bộ | giá vốn TPE 42.500.000 ⇒ POWER mua lại **42.925.000** |
| **Theo giá bán** | `mỗi loại giá × (1 − %)` | **trừ đi** — chiết khấu nội bộ | Bán lẻ TPE 53.500.000 ⇒ POWER mua lại **52.965.000** (ra đủ 6 số cho 6 loại giá) |

Tồn kho thường đặt % cao hơn nhập khẩu (ví dụ khách: 1% / 2%) vì công ty bán đã ôm vốn.

#### 28c. Bản ghi cấu hình

| Trường | Ghi chú |
|---|---|
| `owner_company_id` | công ty BÁN = công ty người đăng nhập đang làm việc (§23c: lấy từ `employee_infos.company_role`) |
| `manufacture_id` | Hãng sản xuất |
| `target_company_id` | **một** công ty mua — khai từng công ty một, KHÔNG khai một lần cho nhiều công ty |
| `base_type` | 1 = Theo giá vốn · 2 = Theo giá bán |
| `percent_import_lot` | % nguồn *Nhập khẩu* |
| `percent_stock` | % nguồn *Tồn kho* |
| `created_by` / `updated_by` + timestamps | audit theo `BaseModel` |

Duy nhất theo bộ 3 **(owner × hãng × công ty mua)**. Công ty chỉ thấy và sửa cấu hình của chính
mình — chặn ở BE, không chỉ lọc ở FE.

#### 28d. Màn hình — MỘT lưới: hãng gộp dòng, CÔNG TY là dòng (user chốt lại 24/09/2026, vòng 4)

> User: *"Đổi phương án cho công ty thành row, các giá trị cấu hình là col. Gộp hãng, mỗi công ty là
> 1 row nhưng phần chọn cách tính theo Giá bán/giá vốn là theo hãng chứ không cần theo từng công ty."*

`/master-data/internal-price-policies` — **Chính sách giá bán nội bộ**. Một bảng duy nhất, vừa khai
vừa nhìn được chính sách của từng công ty:

| Cột | Cấp | Chi tiết |
|---|---|---|
| STT · **Hãng sản xuất** | **hãng** (ô gộp `rowspan`) | tên + mã hãng (hãng khoá gắn 🔒) |
| **Cách tính** | **hãng** (ô gộp) | ô chọn *Giá vốn / Giá bán* (một lựa chọn cho cả hãng) + dòng chú **nêu DẤU của công thức**: `+ % trên giá vốn` (xanh) / `− % trên giá bán` (cam), đổi ngay khi chọn |
| **Công ty mua** | dòng | mỗi công ty mua **một dòng**; **màu định danh** = vạch trái 4px màu đậm + nền `rgba(màu,.07)` + tên in chính màu đó, đậm — `#2563EB · #0891B2 · #16A34A · #7C3AED · #C026D3 · #475569` (chỉnh lại vòng 5 vì bản trước 6 tông nhạt nhoè, khó phân biệt). Không dùng vàng (= ô chưa lưu) và đỏ (= lỗi) |
| **Nhập khẩu (%)** · **Tồn kho (%)** | dòng | 2 ô nhập tại chỗ. Tiêu đề mỗi cột có **icon ⓘ**: *Nhập khẩu* = "Giá tính cho trường hợp bán nguyên lô nhập khẩu về thẳng kho Công ty mua"; *Tồn kho* = "Giá tính cho trường hợp xuất bán cho Công ty mua từ kho" |
| **Cập nhật gần nhất** | dòng | **`dd/mm/yyyy HH:mm:ss`** + người, **riêng theo từng công ty** (đụng công ty nào mới đổi mốc của công ty đó); chưa khai thì ghi *"Chưa khai"* |
| **Hành động** | **hãng** (ô gộp) | **các nút** (bỏ menu ⋮): **Lưu** (chỉ khi hãng có thay đổi) · **Xem trước giá** · **Lịch sử** · **Bỏ khỏi lưới** *(CHỈ hãng vừa chọn vào, chưa lưu lần nào)*. **Không có thao tác xoá theo công ty** — muốn bỏ chính sách của một công ty thì xoá trắng 2 ô rồi Lưu |

- Mặc định hiện **đủ mọi công ty mua** cho từng hãng để khai nhanh; tick **"Chỉ hiện công ty đã khai"**
  để rút gọn (đo: 30 dòng → 14 dòng).
- **Thanh tiêu đề bảng** (trái → phải, đúng `button-convention` mục 6): *Cách khai báo* ·
  **Chọn hãng** (primary) · **Import Excel** (`secondary status="warning"` — **cam**, vì import ghi dữ
  liệu vào hệ thống) · **Xuất Excel** (`secondary status="success"` — **xanh lá**, nhóm xuất chỉ đọc ra).
- **Import Excel** mở popup theo khuôn `components/V2BaseImportModal.vue` + `V2BaseImportToolbar.vue`:
  3 nhóm nút **File** (*Chọn file Excel* · *Tải file mẫu*) · **Hành động** (*Load lên bảng* ·
  *Validate* · *Import*) · **Hiển thị** (toggle *Chỉ dòng lỗi*); bảng xem trước tô **nền hồng ở dòng
  lỗi** và ghi lý do **ngay dưới ô sai**; dải tổng kết *"Hợp lệ N dòng / Lỗi M dòng"*; footer
  *Làm mới* · *Đóng*. **Chỉ dòng hợp lệ được nạp**, nạp xong vẫn phải bấm **Lưu** như nhập tay.
- **Xuất Excel** xuất đúng phạm vi đang xem của công ty bán hiện tại.
- **Hãng vừa chọn vào hiện NGAY ĐẦU BẢNG** (không nối vào cuối, khỏi phải cuộn đi tìm).
- ⚠️ Cột Hành động là **ô gộp**, nên phần lớn dòng có ô cuối là *Cập nhật gần nhất*; rule chung
  `td:last-child{border-right:0}` làm các dòng đó **mất viền phải** — phải khai lại viền cho bảng này.
- ⚠️ Dòng công ty phải **ghim chiều cao** (`td{height:38px}`): dòng có *ngày + người* cao 39px còn
  dòng *Chưa khai* 37px, so le nhìn như bảng lệch.
- **Bộ lọc** (một hàng, các ô căn đáy): ô tìm hãng · **Công ty mua** (chọn 1 công ty ⇒ mỗi hãng chỉ
  còn dòng của công ty đó, đo: 30 → 5 dòng) · **toggle *Chỉ công ty đã khai*** (dạng `custom-switch`
  của app: track 28×16px, knob dịch 12px, bật màu `#1abc9c` — **không dùng checkbox**) · *Làm mới*.
- **Danh sách công ty (chốt 24/09, vòng 6)**: công ty bán **TÂN PHÁT**; 6 công ty mua theo đúng thứ tự
  **ETEK POWER · ETEK GREEN · ETEK · TÂN PHÁT SG · CN HẢI PHÒNG · CN VINH**. Thứ tự này cũng là thứ tự
  dòng trên lưới, và công ty **đầu danh sách** là nơi khai khi chọn *Hệ số chung*.
- **KHÔNG BAO GIỜ CUỘN NGANG** — thêm công ty thì bảng chỉ dài thêm. Đây là lý do đổi khỏi phương án
  cũ (công ty là nhóm cột): 8 công ty đã phải cuộn ngang 421px và phải ghim cột định danh.
- **Nhập tại chỗ**: ô vừa đổi **tô vàng** cho tới khi lưu; mỗi nhóm hãng có nút Lưu riêng.
- **LƯU THEO TỪNG HÃNG**: payload chỉ gồm **một hãng** (công ty bán + mã hãng + cách tính + tỷ lệ
  theo từng công ty mua). Nút chân màn **"Lưu N hãng đã đổi"** cũng chỉ gửi N hãng có thay đổi.
  Cả 2 nút **ẩn hẳn** khi không có gì để lưu.
- **Cảnh báo khi còn thay đổi chưa lưu** — **popup của phần mềm, KHÔNG dùng hộp thoại trình duyệt**
  (user chốt 24/09). Chữ lấy đúng `.claude/skills/unsaved-changes`: tiêu đề **"Thông tin chưa lưu"**,
  câu hỏi **"Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?"**, nút **Thoát** (nhóm nguy hiểm) /
  **Ở lại**; dòng phụ nêu số hãng đang treo (*"Còn 1 hãng chưa lưu"*). Chặn 2 lối rời trong ứng dụng:
  **đổi màn ở menu trái** và **đổi ô "Đang làm việc tại"** (ô chọn tự trả về công ty cũ).
  ⚠️ Skill có gợi ý dùng `beforeunload` cho ca đóng tab/F5 — ở màn này **đã gỡ** theo yêu cầu user.
- **Xem trước giá** (popup theo hãng): *Giá vốn* ⇒ bảng công ty mua × 2 nguồn hàng; *Giá bán* ⇒
  bảng 6 loại giá × (mỗi công ty 2 cột). Số làm tròn tới hàng trăm như ERP.
- **Hãng đã lưu thì KHÔNG xoá được khỏi lưới** (user chốt vòng 5) — đã khai báo là dữ liệu đang chạy.
- **Lịch sử** (popup theo hãng) dựng **đúng khuôn `.claude/skills/entity-history/ui-base.md`**:
  header icon tròn teal + *"Lịch sử chính sách giá bán nội bộ"* + dòng phụ `Hãng sản xuất: … · công
  ty chủ: …` · nút **Bộ lọc** góc phải · 4 ô lọc (**Loại hành động** đúng **3 nhóm cố định**
  *Tạo mới / Thay đổi thông tin / Thay đổi trạng thái*; **Người thực hiện** lấy từ **danh sách nhân
  sự** dạng `MÃ PHÒNG - Tên`, KHÔNG suy từ log; **Từ ngày**; **Đến ngày**) + *Tìm kiếm* / *Làm mới* ·
  timeline **mới → cũ** (chấm màu theo nhóm · thời gian monospace · tên hành động đậm màu nhóm ·
  *"Người thực hiện: Tên — Phòng ban"* · khối thay đổi **cũ đỏ `#dc2626` → mới xanh `#16a34a`** ·
  ghi chú nền `#fef3c7`) · lọc không ra ghi *"Không có lịch sử phù hợp bộ lọc."* · footer chỉ nút
  **Đóng**. Thao tác **bỏ chính sách của một công ty** ghi vào nhóm **Thay đổi trạng thái** để cả 3
  nhóm lọc đều có dữ liệu thật.
- ⚠️ Ô chọn *Cách tính* hiển thị nhãn ngắn **"Giá vốn" / "Giá bán"** — để nguyên *"Theo giá vốn"* là
  chữ bị cắt trong ô hẹp (đo thật).

#### 28d-quater. Cách khai hệ số — tuỳ chọn TOÀN CỤC (user chốt 24/09/2026, vòng 6-7)

Dải chọn nằm ở **thanh tiêu đề của bảng, ngay cạnh nút "Chọn hãng"** (vòng 7 dời lên từ dưới thanh
lọc cho gọn), áp cho toàn màn của công ty bán đang đứng. Chú thích dài của từng lựa chọn nằm trong
**icon ⓘ 14px** (hover mới hiện), không in thành dòng chữ trên giao diện:

| Lựa chọn | Hành vi |
|---|---|
| **Hệ số theo công ty** *(mặc định)* | như mô tả ở §28d — mỗi công ty mua một cặp tỷ lệ riêng |
| **Hệ số chung** | **CHỈ công ty ĐẦU DANH SÁCH được nhập**; các công ty còn lại **kế thừa y hệt**: ô **khoá, nền xám**, giải thích để ở `title` khi rê chuột — **KHÔNG in dòng chữ "kế thừa từ …" dưới ô** (nó làm dòng cao hơn dòng khác, lệch cả hàng). Gõ ở công ty đầu là các dòng dưới đổi theo **ngay** |

- Tooltip của *Hệ số chung* nêu **đích danh công ty đang được khai** (đổi theo công ty bán đang đứng):
  *"Chỉ khai ở ETEK POWER (công ty mua đầu danh sách); các công ty còn lại dùng y hệt cặp tỷ lệ đó, ô
  bị khoá…"*.
- ⚠️ Icon ⓘ nằm sát mép phải nên tooltip phải **neo theo mép phải** (`right`), căn giữa kiểu
  `translateX(-50%)` là bảng 300px **tràn ra ngoài khung nhìn** (đo: phải 1475 > 1464).
- Chuyển sang *Hệ số chung* ⇒ lan toả ngay + toast nhắc **bấm Lưu** (dữ liệu mới chỉ nằm trên màn).
- ⚠️ **Bẫy đã trả giá**: bản đầu lan toả bằng cách lấy đúng công ty đầu, hãng nào **chưa khai ở công
  ty đầu** thì bị **xoá sạch** chính sách của các công ty khác — bật hệ số chung là mất 2/5 hãng, im
  lặng. Sửa: nếu công ty đầu chưa có thì lấy **dòng đã khai đầu tiên** làm gốc; hãng chưa khai ở đâu
  cả thì để trống.
- Khi lọc theo **Công ty mua** khác công ty đầu ở chế độ chung, lưới vẫn giữ thêm dòng công ty đầu để
  còn chỗ nhập.

#### 28d-ter. Validate của lưới

- Bấm **Lưu** soát **hết ô một lượt**, không bắt sửa từng ô rồi bấm lại.
- % phải là số trong khoảng **0 – 100**; sai thì viền đỏ đúng ô đó.
- Một công ty mua **khai một ô mà bỏ trống ô kia** ⇒ báo thiếu, tô đỏ **ô còn trống**.
- **Cả 2 ô cùng trống** ⇒ hiểu là công ty đó **không có chính sách**, không phải lỗi.
- Còn ô sai thì **không lưu gì cả**, thay đổi vẫn giữ trên lưới để user sửa tiếp.

#### 28d-bis. Popup chọn hãng — CHỈ để kéo hãng vào lưới (user chốt 24/09/2026)

> *"Hãng có 1.071 hãng, nên sẽ để cơ chế cần chọn hãng nào ra để nhập ⇒ popup chọn + cho check chọn
> nhiều."* — popup **không nhập liệu**, chỉ chọn hãng; nhập % làm thẳng trên lưới.

- Mở bằng nút **Chọn hãng** ở đầu bảng. Tìm theo **mã hãng / tên hãng**, **tick nhiều**, có ô
  **tick tất cả các dòng đang hiện**; mỗi lượt vẽ tối đa **80 dòng** kèm dòng đếm
  *"Đang hiện 80 / 1.071 hãng khớp"*.
- Cột **Trạng thái**: hãng **đã có trên lưới** hiện badge *"Đã có trên lưới"* và **khoá ô tick**.
- Bấm **Chọn** ⇒ mỗi hãng thành **một dòng mới trên lưới** (chưa có tỷ lệ), đồng thời tự bỏ tick lọc
  *"Chỉ hiện hãng đã có chính sách"* để hãng vừa thêm không biến mất.
- Hãng **đang khoá** (`manufactures.status <> 1`, 59/1.071 dòng) vẫn hiện, gắn **🔒** trước tên.
- ⚠️ **Bẫy đã trả giá**: tick hãng xong rồi gõ từ khoá khác thì bảng vẽ lại, các hãng vừa tick
  **mất im lặng** (đo được: tick 3 hãng Bosch, gõ tiếp "launch" thì đếm về 1). Phải giữ lựa chọn
  trong một mảng tạm, cập nhật NGAY mỗi lần tick, không đợi tới lúc bấm "Chọn".

#### 28e. Ngoài phạm vi đợt này (user chốt để mockup sau)

Nơi **hiện số gợi ý** cho công ty mua: popup *"Xem hàng hoá Công ty khác"* (§26d), màn/tab
*Tính giá bán*, hay cột ở màn danh sách — chưa chốt, sẽ dựng mockup riêng. Cảnh báo "hãng chưa cấu
hình" (đáp án 7) cũng nằm ở đợt đó vì nó hiện lúc lấy hàng về.

#### 28f. Còn tồn của riêng màn này

1. **Quyền**: thêm quyền riêng *"Cấu hình giá bán nội bộ"* hay dùng chung quyền *Tính giá bán hàng hoá*?
2. **% âm / vượt trần**: có chặn trần (vd ≤ 100%) và có cho nhập % = 0 không?
3. **Hãng không có hàng hoá nào của công ty bán** vẫn cho khai trước hay chỉ cho khai hãng đang dùng?
4. Một công ty mua **ngừng hợp tác** — xoá cấu hình hay giữ lại để tra lịch sử?

---

### 29. PHIẾU TÍNH GIÁ CHO HÀNG LẤY TỪ CÔNG TY KHÁC (user chốt 26/09/2026)

> Nguyên văn yêu cầu: *"Thiết kế Mockup màn hình phiếu tính giá cho Case lấy hàng hoá công ty khác
> về để kinh doanh: User dùng chức năng xem hàng hoá công ty khác ⇒ chọn ⇒ lấy về danh sách hàng
> đang nhập thông tin ⇒ bổ sung đủ thông tin ⇒ Lập Yêu cầu tính giá. Với phiếu tính giá loại này
> ngoài form hiện có của phiếu tính giá thì cần hiển thị thêm các thông tin về giá mua từ công ty
> quản lý hàng hoá theo cấu hình của màn Chính sách giá bán nội bộ."*
> Bổ sung trong ngày: *"mỗi hàng hoá trong phiếu tính giá sẽ hiển thị phương án tính giá từ Công ty
> quản lý hàng hoá để tham khảo, giá bán chốt của Công ty vẫn tự quyết định"* ·
> *"Nếu cách tính theo giá vốn ⇒ có hiển thị giá vốn của Công ty quản lý, giá bán luôn hiện"* ·
> *"hãy hiện chính sách giá ⇒ có button xem tạm tính chi tiết"*.

#### 29a. 5 đáp án chốt

| # | Câu | Chốt | Hệ quả |
|---|---|---|---|
| 1 | Hàng tự tạo và hàng lấy về tính giá theo đường nào | **MỌI hàng đều qua chứng từ tính giá** | Bước 2 không còn tính giá ngay trong form hàng hoá ⇒ **tab "Giá bán" của mockup §26 sẽ bị gỡ**, thay bằng cặp chứng từ *Yêu cầu tính giá → Phiếu tính giá*. Đây cũng là lời đáp cho **tồn 26g-1** (trùng luồng hỏi giá của ERP): dùng lại đúng luồng chứng từ, không mở cửa thứ hai |
| 2 | Ô giá đầu vào của phiếu | **Để trống, người tính giá tự nhập** | Chính sách chỉ là số tham khảo, không tự điền vào ô giá mua |
| 3 | 2 tỷ lệ Nhập khẩu nguyên lô / Tồn kho | **Hiện cả 2 số song song** | Không có ô chọn nguồn hàng trên phiếu |
| 4 | Khối tham khảo hiện gì | Cách tính + 2 tỷ lệ · **giá vốn của công ty quản lý CHỈ khi cách tính theo giá vốn** · **giá bán LUÔN hiện** · giá mua suy ra theo từng nguồn | Giá vốn liên công ty vẫn lộ ⇒ bản thật phải gate bằng quyền **Quản lý giá** ở BE (ghi vào mục 29e) |
| 5 | Ô của ERP dành cho hàng nhập khẩu | **Giữ nguyên hết** (đơn vị tiền tệ · tỉ giá · thuế NK · tab Chi phí) | Một khuôn phiếu dùng cho cả hàng nhập khẩu lẫn hàng lấy nội bộ |

#### 29b. Khảo sát phiếu tính giá ERP (nguồn: `orders/price_calculates/*`, `Order/PriceCalculate*`)

Chuỗi 4 chứng từ ở menu *Mua hàng → Hàng tạm - Hỏi giá*: **Yêu cầu hỏi giá** (4.029) →
**Yêu cầu tính giá** (3.147) → **Phiếu tính giá** (3.120, mới nhất 14/09/2026) → **Kết quả tính giá**.

- **Thông tin chung**: Chọn yêu cầu tính giá (popup, khoá sau khi chọn) · Đơn vị tiền tệ · Tỉ giá ·
  Thương hiệu · Hãng sản xuất · Người hỏi giá · Ghi chú.
- **Tab Hàng hoá**: tick *Cần tính* · Tên · Mã · Model · Code đặt hàng · ĐVT · **Giá NCC (ngoại tệ)** ·
  Đơn giá VNĐ · **Thuế NK (%)** · Thành tiền sau thuế.
- **Tab Chi phí**: mỗi hàng hoá nhiều dòng chi phí (danh mục `costs` loại *giá hàng hoá*), nhập
  **Tỉ lệ %** hoặc **Đơn giá**, ra Thành tiền VNĐ.
- **Tab Tính giá**: Đơn giá VNĐ · Tổng chi phí · **Chi phí khác** · **Giá nhập kho** · khối **Giá bán**
  6 loại × (Hệ số · Giá công thức · Giá bán · Định mức đàm phán giá · Ngày hiệu lực) + *Thêm giá hiệu lực*.
- Footer **Lưu** (Đang tạo) · **Lưu & Duyệt** (Đã duyệt). Duyệt xong ghi vào `product_unit_prices`,
  hoặc đẩy sang **chờ duyệt giá** khi công ty bật quy chế `companies.is_company_price`
  (+ `is_all_brand` / `brand_ids`).
- 6 loại giá (`price_types`): Bán lẻ · Giá bán theo lô · Đại lý cấp 1/2/3 · Giá bán TMĐT (online).

**Công thức — đo trên `price_calculate_products` thật, 8/8 dòng khớp:**

```
Đơn giá VNĐ         = Giá mua × tỉ giá
Thành tiền sau thuế = Đơn giá VNĐ × (1 + thuế NK%)
Chi phí theo %      = tính trên Đơn giá VNĐ (CHƯA thuế)
Giá nhập kho        = Thành tiền sau thuế + Tổng chi phí + Chi phí khác
Giá bán             = Hệ số × Giá nhập kho, làm tròn tới hàng TRĂM
Giá TMĐT            = Giá bán lẻ × 1,3 (CONFIG.coefficient_ecommerce_price), ô khoá
```

🐞 **Lệch cần biết khi port**: class JS `PriceCalculateProduct` trên nhánh `develop_01` tính
`cost_price` từ **đơn giá CHƯA thuế** (`supplier_price_exchange + chi phí + khác`), trong khi **100%
dữ liệu đã lưu** lại cộng từ **sau thuế**. Phiếu thật PTG-03178: code ra 12.100.946, DB lưu
**13.108.986**. Mockup đi theo **dữ liệu thật**; khi viết BE phải chốt lại với nghiệp vụ.

#### 29c. Mockup đã dựng (trong `mockup-luong-xay-dung-hang-hoa.html`)

4 màn mới + 2 popup, thêm 2 mục menu trái *Yêu cầu tính giá* · *Phiếu tính giá*:

| Màn | Nội dung |
|---|---|
| **Yêu cầu tính giá** (danh sách) | Số phiếu · Số mã hàng · Công ty quản lý hàng hoá · Đơn vị tiền tệ · Người lập · Ngày lập · Trạng thái (*Đang tạo / Chờ tính giá / Đã tính giá*) · Hành động (**Lập phiếu tính giá** khi đang chờ) |
| **Form yêu cầu tính giá** | Mở bằng nút **Lập yêu cầu tính giá** ở màn *Hàng hoá đang nhập thông tin*. Thông tin chung (công ty đề nghị · tiền tệ · tỉ giá · ghi chú) + bảng hàng đang nhập thông tin **tick chọn nhiều**, mỗi dòng hiện **Chính sách giá nội bộ**. Footer *Lưu nháp · Lưu & gửi tính giá · Quay lại* — gửi thì hàng chuyển **Chờ tính giá bán** |
| **Phiếu tính giá** (danh sách) | Bộ cột theo ERP: Số phiếu · Yêu cầu tính giá · Số mã hàng · Công ty quản lý · Người lập · Ngày lập · Trạng thái · Hành động; nút **Tạo phiếu tính giá** mở popup chọn yêu cầu; bộ lọc nâng cao 6 ô (nhãn nằm trong ô như các màn khác) |
| **Form phiếu tính giá** | Thông tin chung + 3 tab **Hàng hoá · Chi phí · Tính giá** đúng khuôn ERP. Footer *Lưu · Lưu & duyệt giá · Quay lại* — duyệt thì hàng chuyển **Đang kinh doanh**, yêu cầu chuyển **Đã tính giá** |

**Phần THÊM so với ERP — đúng 2 điểm:**

1. **Cột "Chính sách giá nội bộ"** ở tab *Hàng hoá* (và bản gọn một dòng ở tab *Tính giá*):
   badge cách tính (*Theo giá vốn* xanh · *Theo giá bán* tím) · `Nhập khẩu x% · Tồn kho y%` ·
   **giá vốn của công ty quản lý chỉ khi theo giá vốn** · **giá bán lẻ luôn hiện** · nút **Tạm tính**.
   Hãng chưa khai chính sách ⇒ badge cam **Chưa cấu hình** + câu giải thích, **vẫn lập phiếu được**
   (đúng đáp án 7 của §28: cảnh báo chứ không chặn).
2. **Cột "Thành tiền sau thuế"** ở tab *Tính giá* — ERP không có, thêm để thấy rõ Giá nhập kho cộng
   từ đâu (theo đúng công thức đo được ở 29b).

**Popup "Tạm tính giá mua từ Công ty quản lý"**: dòng thông tin (công ty quản lý · hãng sản xuất ·
cách tính · mốc cập nhật chính sách) + bảng `Căn cứ | Giá của công ty quản lý | Giá mua — Nhập khẩu
nguyên lô (±x%) | Giá mua — Tồn kho (±y%)`:

- *Theo giá vốn*: có dòng **Giá vốn** với 2 số giá mua; 6 dòng giá bán chỉ để so mặt bằng (cột giá mua `—`).
- *Theo giá bán*: **không có dòng giá vốn**; cả 6 loại giá đều ra giá mua `× (1 − %)`.
- Chân popup ghi rõ: số làm tròn tới hàng trăm như ERP, **chỉ là số tham khảo**, giá mua thực tế và
  giá bán chốt do công ty mua tự quyết định.

#### 29d. Đã đo bằng Playwright (console 0 lỗi)

| Phép kiểm | Kết quả |
|---|---|
| Luồng đủ 3 chặng | *Đang nhập thông tin* → tick 2 mã → **Lưu & gửi** ⇒ đếm menu 4→2 / +2 ở *Chờ tính giá*, sinh YCTG mới · **Lập phiếu tính giá** → nhập giá → **Lưu & duyệt giá** ⇒ hàng sang **Đang kinh doanh** (l3 4→5), yêu cầu sang **Đã tính giá** |
| **Công thức khớp phiếu thật ERP** | Dựng lại PTG-03178 (316 EURO × 31.900, thuế NK 10%, 3 dòng chi phí) ⇒ Đơn giá **10,080,400** · sau thuế **11,088,440** · Giá nhập kho **13,108,986** — **đúng từng đồng** với DB |
| Giá bán | Hệ số 1,70 ⇒ giá công thức **22,285,276**, giá bán làm tròn trăm **22,285,300**; TMĐT = bán lẻ × 1,3, ô **khoá** |
| Tạm tính *theo giá vốn* | 13,108,986 ⇒ NK (+0,8%) **13,213,900** · Tồn kho (+1,6%) **13,318,700**; 6 giá bán hiện, cột giá mua `—` |
| Tạm tính *theo giá bán* | Bán lẻ 12,500,000 ⇒ NK (−3%) **12,125,000** · Tồn kho (−5%) **11,875,000**; **không có dòng giá vốn** |
| Validate | Chưa nhập giá mua ⇒ toast *"Chưa nhập giá mua cho 2 hàng hoá"*, **không lưu**, vẫn ở form |
| Nút "Giá hiệu lực" | rowspan ô gộp 6→7, dòng *↳ giá sẽ áp dụng* chèn đúng chỗ, **ô gộp phủ khít nhóm (lệch 0px)**, xoá thì trả về 6 |
| Lề nút | 3 nút thanh tiêu đề cách nhau **đúng 12px**, cao 32px |
| Thanh cuộn | Bảng tab Hàng hoá 1.690px / Tính giá 1.900px trong khung 1.428px — **cuộn trên và dưới đồng bộ 2 chiều** |

#### 29e. 5 lỗi tự bắt được khi dựng (đọc code không thấy)

1. **Đổi đơn vị tiền tệ làm mất trắng giá vừa nhập** — vẽ lại bảng mà chưa cất giá trị trong DOM.
2. **Tỉ giá không đổi theo tiền tệ** — gán vào input rồi mới vẽ lại nên bị ghi đè bằng giá trị cũ.
3. **Số chứng từ nhảy số** (`313 + độ dài mảng` ⇒ phiếu thứ hai ra 00315) — phải dùng biến đếm tăng dần.
4. **Bảng bị bóp** vì `table.tbl{width:100%}`: cột *Tên hàng hoá* khai 220px render **106px**, ô nhập
   *Hệ số* còn **36px** ⇒ phải ghim `min-width` bằng tổng bề rộng khai rồi cho cuộn ngang.
5. **Dòng giá cao 73px** vì badge *Đang áp dụng* và nút *Giá hiệu lực* rơi xuống 2 dòng; ô Mã hàng ôm
   cả khối chính sách + ghi chú làm nhóm cao **480px** ⇒ cho badge + nút cùng dòng, khối chính sách ở
   tab Tính giá dùng **bản gọn một dòng** ⇒ dòng còn **45px**, nhóm còn 283px.

#### 29f. Việc còn treo của §29 (chưa hỏi user)

1. ~~**Gỡ tab "Giá bán" khỏi form hàng hoá**~~ — ✅ **ĐÃ LÀM 27/09/2026**, xem §29g.
2. **Gate giá vốn liên công ty**: khối tham khảo đang hiện giá vốn của công ty quản lý cho mọi người
   mở phiếu. Bản thật phải chặn bằng quyền **Quản lý giá** ở BE (trả `null`), theo đúng §4.4.
3. **Ai lập / ai duyệt**: yêu cầu tính giá do người có quyền *Nhập thông tin hàng hoá* lập, phiếu tính
   giá do người có quyền *Tính giá bán hàng hoá* lập — chưa chốt có bước **duyệt yêu cầu** như ERP
   (ERP: yêu cầu tính giá phải được duyệt mới lập phiếu) hay bỏ.
4. **Phiếu nhiều công ty quản lý**: hiện cho phép một yêu cầu gom hàng của nhiều công ty quản lý
   (ô *Công ty quản lý hàng hoá* ghi `TÂN PHÁT SG · ETEK POWER`). ERP mỗi phiếu một thương hiệu/hãng —
   cần chốt có tách phiếu theo công ty quản lý không.
5. **Lưu vết số tham khảo**: chốt giá xong có lưu lại "chính sách lúc tính giá" để sau này đối chiếu không.

#### 29g. GỠ TAB "GIÁ BÁN" KHỎI FORM HÀNG HOÁ (user chốt 27/09/2026)

Hệ quả trực tiếp của đáp án §29a-1 (*mọi hàng đều tính giá bằng chứng từ*). Form hàng hoá nay
**chỉ còn 6 tab thông tin**; người tính giá không mở form hàng hoá nữa mà làm việc trên **Phiếu
tính giá**.

**Đã gỡ:** nhãn tab 7 + `pane-gia` · footer `ft-gia` (*Lưu tạm / Lưu & duyệt giá bán*) ·
4 hàm dựng tab giá (`veTabGia` · `dvtCuaHang` · `doiTabDvt` · `themGiaHieuLuc`) ·
3 hàm của bước tính giá cũ (`moGia` · `luuTamGia` · `luuVaDuyetGia`) · biến `dangTinhGia` ·
**vai `'gia'`** trong `datVaiForm` / `mucQuyenSua` (3 mức quyền §26c-bis nay chỉ còn `full` và
`chiQuanTri`). `LOAI_GIA` giữ lại vì phiếu tính giá dùng chung.

**Nối lại 3 lối vào cũ — không để nút chết:**

| Chỗ | Trước | Sau |
|---|---|---|
| Nút **Tính giá** ở màn *Hàng hoá chờ tính giá* | mở form hàng hoá ở vai tính giá | `moTinhGia(code)`: mở **đúng phiếu tính giá đang dở** của hàng hoá đó; chưa có phiếu thì mở phiếu mới từ **yêu cầu tính giá đang chờ**; không có yêu cầu nào thì toast nhắc *"lập yêu cầu ở màn Hàng hoá đang nhập thông tin"* |
| Menu ⋮ mục **Sửa giá** ở màn *Danh mục hàng hoá kinh doanh* | mở tab Giá bán | **bỏ hẳn** — sửa giá hàng đang kinh doanh thuộc **Phase 8 (Quản lý giá)**, không nhét vào form hàng hoá |
| Sơ đồ luồng, bước 2 | *"Người có quyền tính giá nhập giá vốn, hệ số… rồi duyệt giá"* | *"Lập **Yêu cầu tính giá** từ màn Đang nhập thông tin, rồi người có quyền tính giá lập **Phiếu tính giá**…"* |

**Dữ liệu demo chỉnh theo:** sau khi bỏ tab, trạng thái *Chờ tính giá bán* / *Đang tính giá* chỉ có
thể đến từ chứng từ ⇒ bổ sung `YCTG-00309`, `YCTG-00310` và phiếu dở `PTG-03178` cho 2 mã hàng
**TÂN PHÁT tự tạo** đang đứng ở 2 trạng thái đó. Nhờ vậy luồng chứng từ áp cho **cả hàng tự tạo**,
không riêng hàng lấy từ công ty khác.

**Đã đo bằng Playwright (console 0 lỗi):**

| Phép kiểm | Kết quả |
|---|---|
| Form hàng hoá | còn **đúng 6 tab**, 6 pane, **một** footer (*Lưu nháp / Lưu / Quay lại*) |
| Khoá theo công ty vẫn nguyên | mở hàng của ETEK POWER ⇒ dải báo *"chỉ khai được tab Dữ liệu quản trị"*, 5/6 tab mang class `khoa` |
| Menu ⋮ màn kinh doanh | còn *Xem · Khóa · In tem barcode · Lịch sử* — **không còn** *Sửa giá* |
| Nút Tính giá — nhánh có chứng từ | `SG-AMAT8574091` ⇒ mở phiếu gắn **YCTG-00312** |
| Nút Tính giá — nhánh chưa có | toast đúng câu nhắc, **vẫn ở màn danh sách** |
| Mọi hàng ở màn *Chờ tính giá* | **2/2 truy được về chứng từ** (yêu cầu `YCTG-00309` · phiếu `PTG-03178`), 0 lần rơi vào nhánh cảnh báo |
| Chạy lại trọn luồng | lập yêu cầu ⇒ lập phiếu ⇒ nhập 168,000,000 × hệ số 1,25 ⇒ giá bán **210,000,000** ⇒ duyệt ⇒ hàng **Đang kinh doanh**, yêu cầu **Đã tính giá** |

Ảnh: `anh-mockup/29-so-do-luong-sau-go-tab-gia-ban.png`.

---

### 30. CÂY 4 CẤP LĨNH VỰC — GIỮ LẠI, ĐỔI GỐC, ĐƯA VÀO TAB DỮ LIỆU QUẢN TRỊ (user chốt 27/09/2026)

> Nguyên văn yêu cầu: *"Danh mục: Lĩnh vực ⇒ Chương ⇒ Nhóm công việc ⇒ Cụm công việc: không bỏ,
> chỉ cập nhật như sau: Bỏ danh mục Lĩnh vực ⇒ Danh mục lĩnh vực kinh doanh theo công ty sẽ thay
> vị trí · Đưa 3 danh mục còn lại sang HRM · 4 cấp danh mục này sẽ đưa vào tab Quản trị theo công
> ty trên form hàng hoá."*
>
> ⚠️ **Đảo quyết định cũ**: `quan-ly-hang-hoa/design.md` mục B trước đây xếp cả 4 màn này vào diện
> **BỎ** (Phase 5). Nay chỉ bỏ **màn Lĩnh vực**; 3 màn còn lại **chuyển sang HRM** (Phase 2d mới).

#### 30a. Hiện trạng đo được (27/09/2026)

| Bảng | Dòng | Quan hệ | Ghi chú |
|---|---|---|---|
| `scopes` (Lĩnh vực) | **14** | gốc cây | Ô TÔ · Thiết bị xe máy · Phụ tùng ô tô · Dầu mỡ… |
| `chapters` (Chương) | **65** | `scope_id` | |
| `job_groups` (Nhóm công việc) | **106** | `chapter_id` | |
| `job_clusters` (Cụm công việc) | **2** | `group_id` *(trỏ `job_groups`, KHÔNG phải `groups`)* | tên cột dễ đọc nhầm |
| `internal_business_scopes` (**Lĩnh vực Công ty kinh doanh**) | **8** | — | **đã có sẵn ở HRM**: màn `/assign/internal-business-scopes`, mã `LVCTKD.*`, có import Excel + khoá/mở khoá, quyền **1177/1178** |

**Cây hiện KHÔNG gắn vào hàng hoá mà gắn vào NHÓM HÀNG HOÁ:**

- `product_group_classifies` (`group_id` × 4 cấp) — **1.019 dòng đang sống**
- `product_classifies` (gắn thẳng `product_id` × 4 cấp) — **tồn tại nhưng 0 dòng**
- Hàng hoá ra được lĩnh vực nhờ `products.group_id` → nhóm hàng hoá → cây.
- Bộ lọc thật nằm ở `Product::searchByFilter` — **4 chỗ** (`scope_id` · `chapter_id` ·
  `job_group_id` · `job_cluster_id`), mỗi chỗ đều `pluck('group_id')` rồi
  `whereIn('products.group_id', …)`.
- Form hàng hoá ERP **không có** ô lĩnh vực/chương — đó là lý do yêu cầu mới phải đưa 4 cấp vào form.

✅ **ĐÍNH CHÍNH 27/09/2026 — `scopes` KHÔNG có tham chiếu ngoài nhánh hàng hoá.**
Bản ghi đầu tiên của mục này nói *"1.058 tham chiếu sống ở `industry_scopes` 424 ·
`prospective_projects` 325 · `application_scopes` 249 · `solutions` 39 · `request_solutions` 21"* —
**SAI**. Số đó đếm bằng `JOIN … ON x.scope_id = scopes.id`, mà **`scopes` (ERP) và `hrm_scopes` /
`internal_business_scopes` (HRM) trùng dải id 1–8**, nên JOIN khớp nhầm.

Đo lại **bằng model**: cả 8 bảng có dữ liệu (`application_industries` 781 · `industry_scopes` 424 ·
`prospective_projects` 325 · `application_scopes` 249 · `meeting_investment_demands` 187 ·
`solutions` 39 · `request_solutions` 21 · `form_template_snapshots` 2) đều là bảng của **HRM
`Modules/Assign`**, và quan hệ `scope()` của chúng trỏ `Modules\Assign\Entities\Scope\Scope`
— `$table = 'hrm_scopes'` (**35 dòng**), hoặc `internal_business_scopes`. **Không bảng nào trỏ
`scopes` của ERP.**

⇒ `scopes` (ERP, 14 dòng) chỉ còn được dùng bởi: `chapters` (65) · `product_group_classifies`
(1.019) · `product_classifies` (0) · `pi_product_group_classifies` (0) — **toàn bộ đều trong diện
bỏ**, nên **xoá sạch data `scopes` là an toàn** (user chốt 27/09).
📌 Đây đúng là bẫy *"bảng trùng tên ưu tiên bản ERP, bản HRM đổi tên `hrm_*`"* ở
`.plans/gop-db/design.md` — đếm bằng id là dính bẫy, phải đếm bằng model.

#### 30b. Việc phải làm

| # | Việc | Chi tiết |
|---|---|---|
| 1 | **Đổi gốc cây** | `chapters` không còn trỏ `scopes` mà trỏ **`internal_business_scopes`** (thêm cột mới, giữ cột cũ tới khi quy đổi xong) |
| 2 | **Chuyển 3 màn sang HRM** | Chương · Nhóm công việc · Cụm công việc — theo khuôn `BaseCatalog*` của Phase 1, dùng chung bảng ERP, **giữ nguyên id** |
| 3 | **Quyền** | 3 màn × 2 quyền = **6 quyền mới** (khuôn Phase 1). Lĩnh vực Công ty kinh doanh đã có **1177/1178**. Quyền ERP `web` 100091–100106 để nguyên cho tới khi gỡ màn |
| 4 | **Tab Dữ liệu quản trị theo công ty** | Thêm 4 ô chọn **lọc dây chuyền**: Lĩnh vực Công ty kinh doanh → Chương → Nhóm công việc → Cụm công việc |
| 5 | **Chỗ lưu** | Gắn theo **(hàng hoá × công ty)** ⇒ thêm 4 cột vào bảng dữ liệu quản trị theo công ty (`product_company_coefficients`, xem §24 mục 3) — **không** dùng `product_classifies` vì bảng đó không có `company_id` |
| 6 | **Bộ lọc ERP** | 4 chỗ trong `Product::searchByFilter` đang đi qua `groups`; sau khi đổi phải đọc từ bảng mới, nếu không **lọc theo lĩnh vực sẽ ra rỗng ở 338 màn** |
| 7 | **Menu** | 3 màn mới nằm ở phân hệ **Danh mục chung**, nhóm riêng (giống nhóm "Xe" của Phase 2b) |

#### 30c. 🔴 4 tồn phải trả lời trước khi code

| # | Tồn | Trạng thái |
|---|---|---|
| 1 | Ánh xạ 14 lĩnh vực cũ → 8 lĩnh vực Công ty kinh doanh | ✅ **KHÔNG CÒN** — dữ liệu cũ bỏ hết, khai mới từ đầu (§30d) |
| 2 | Mỗi công ty khai một cây riêng cho cùng một mã hàng? | ✅ **CÓ** — catalog 4 cấp là **riêng theo từng công ty**, nằm trong tab *Dữ liệu quản trị* (user chốt 27/09) |
| 3 | 1.019 dòng `product_group_classifies` cũ | ✅ **BỎ, làm mới hoàn toàn** (§30d) |
| 4 | Chọn tới cấp nào là đủ | ✅ **TỐI THIỂU 3 CẤP** — tới *Nhóm công việc*; *Cụm công việc* là tuỳ chọn (user chốt 27/09) |

✅ **Hết tồn của §30** — đủ điều kiện dựng mockup 4 ô trong tab Dữ liệu quản trị.

#### 30d. BỎ DỮ LIỆU CŨ, LÀM MỚI HOÀN TOÀN (user chốt 27/09/2026)

> Nguyên văn: *"Dữ liệu cũ về phần catalog này sẽ bỏ, làm mới hoàn toàn nhé"*.

**Phạm vi bỏ** — đã soát, không phân hệ nào khác dùng tới:

| Dữ liệu | Dòng | Ai còn dùng |
|---|---|---|
| `product_group_classifies` (nhóm hàng hoá × cây) | **1.019** | chỉ `Product::searchByFilter` (4 chỗ) + vài controller hàng hoá |
| `chapters` · `job_groups` · `job_clusters` | **65 · 106 · 2** | không bảng nào khác — `pi_product_group_classifies` **0 dòng**, `subject_lessons.chapter_id` **0 dòng** và phân hệ đào tạo có bảng riêng `subject_chapters` |
| `product_classifies` | **0** | rỗng sẵn |

⇒ 3 danh mục chuyển sang HRM ở Phase 2d **khởi đầu rỗng**, người dùng khai lại dưới gốc mới là
**Lĩnh vực Công ty kinh doanh** (8 dòng). Không cần migration ánh xạ, không cần giữ cột `scope_id`
cũ để đối chiếu.

⚠️ **Bảng `scopes` (14 dòng) vẫn GIỮ NGUYÊN** — nó còn 1.058 tham chiếu sống ở 5 bảng ngoài nhánh
hàng hoá (§30a). "Bỏ dữ liệu cũ" ở đây **không đụng** `scopes`.

🔴 **Hệ quả phải canh — bộ lọc ERP rỗng trong thời gian chuyển tiếp:** xoá `product_group_classifies`
là 4 ô lọc *Lĩnh vực · Chương · Nhóm công việc · Cụm công việc* trong `Product::searchByFilter`
**trả về 0 hàng hoá** ở mọi màn dùng popup tìm hàng. Thứ tự bắt buộc:

1. Dựng bảng mới (4 cột trên dữ liệu quản trị theo công ty) + 3 màn danh mục ở HRM
2. Khai dữ liệu mới **xong xuôi**
3. **Rồi mới** chuyển 4 chỗ lọc sang đọc bảng mới và xoá `product_group_classifies`

Làm ngược thứ tự này là lặp lại đúng cái bẫy đã ghi ở mục "Việc note để xử lý sau" của §26:
bật lọc mới trước khi quy đổi ⇒ **338 màn không tìm thấy hàng nào**.

#### 30e. BỎ DATA `scopes` — DANH SÁCH VẤN ĐỀ PHẢI GIẢI QUYẾT (user chốt 27/09/2026)

> Nguyên văn: *"data ở bảng scopes bỏ hoàn toàn ⇒ note các vấn đề cần giải quyết do bỏ data vào
> danh sách vấn đề"* · *"các bảng: Chương, nhóm công việc, cụm công việc ⇒ bỏ data hoàn toàn, khai
> báo lại theo cấp cha mới lĩnh vực công ty kinh doanh"*.

**Chốt:** xoá sạch dữ liệu `scopes` (14) · `chapters` (65) · `job_groups` (106) · `job_clusters` (2)
· `product_group_classifies` (1.019). Cây khai lại từ đầu dưới gốc **Lĩnh vực Công ty kinh doanh**
(`internal_business_scopes`, 8 dòng). Bảng vẫn giữ (còn dùng làm nơi chứa dữ liệu mới), chỉ dữ liệu
là mới hoàn toàn.

**11 vấn đề phát sinh — phải xử lý trước/khi cắt dữ liệu:**

| # | Vấn đề | Đo được | Xử lý |
|---|---|---|---|
| 1 | **Popup tìm hàng hoá dùng chung** (`Common/SearchController`) lọc theo 4 cấp | dùng `ProductGroupClassify` | Lọc ra **0 hàng hoá** ở **338 màn** nếu người dùng chọn lĩnh vực ⇒ phải đổi sang bảng mới **hoặc** ẩn 4 ô lọc cho tới khi khai xong |
| 2 | `Product::searchByFilter` — 4 nhánh lọc `scope_id` · `chapter_id` · `job_group_id` · `job_cluster_id` | 4 chỗ, đều `whereIn('products.group_id', …)` | Đổi sang đọc (hàng hoá × công ty) — **không đi qua `groups`** nữa |
| 3 | **129 chỗ / 15 file ERP** gọi `ProductGroupClassify` | `Product` · `ProductTemplate` · `GroupsImport` · `Product2Controller` · `ProductInfoController` · `QuotationsController` · `ProductsController` · `ProductTemplatesController` · `ProductApprovesController` · `Sale/GroupsController` · `Sale/LiquidationQuotationController` · `Sale/ProductInfo/GroupsController` · `Order/OrderRequestsController` · `Order/InlandOrderRequestsController` · `Common/SearchController` | Rà từng chỗ: đọc bảng mới, hoặc null-safe rồi bỏ |
| 4 | Ô chọn phân loại trong **form hàng hoá ERP** | `products/productClassifyJs.blade.php` · `products/update_list_products.blade.php` (+ 2 bản `product_templates/*`) | Gỡ cùng lúc với việc chặn route ghi hàng hoá của ERP (§13) |
| 5 | **Màn ERP Danh mục lĩnh vực** (`scope.index`) sống nhưng rỗng | 14 → 0 dòng | Gỡ màn + mục menu (Phase 5) |
| 6 | **3 màn ERP Chương · Nhóm CV · Cụm CV** sống nhưng rỗng | 65/106/2 → 0 | Gỡ màn ERP khi 3 màn HRM (Phase 2d) lên sóng |
| 7 | **16 quyền `web`** của 4 màn | id **100091–100106** | Dọn khi gỡ màn; HRM cấp 6 quyền `api` mới |
| 8 | **Màn Nhóm hàng hoá** (`groups`, 893 dòng) mất phân loại | cột Lĩnh vực/Chương trống | `groups` vốn đã trong diện gỡ màn (§21) — chỉ cần không để lỗi khi bảng nối rỗng |
| 9 | **Import nhóm hàng hoá** `GroupsImport` ghi vào `product_group_classifies` | 1 file | Ngừng ghi, hoặc gỡ cùng màn |
| 10 | **Đồng bộ CRM** còn trong `Scope.php` · `Chapter.php` · `ProductGroupClassify.php` (`ModuleMapping`) | đã ngừng chạy từ 08/10/2025 (`MATE_API_USE_CRM` không khai) | Gỡ theo quyết định §9 (bỏ đồng bộ CRM nhánh hàng hoá) |
| 11 | **Khoảng trống dữ liệu** giữa lúc xoá và lúc khai xong | 45.890 hàng hoá không có lĩnh vực | Giữ nguyên thứ tự ở §30d: dựng bảng mới + 3 màn → khai xong → **rồi mới** cắt |

⚠️ **Không nằm trong diện xoá:** `hrm_scopes` (35 dòng) và `internal_business_scopes` (8) — đây là
bảng của HRM, nuôi 8 màn phân hệ Giao việc (dự án tiền khả thi, giải pháp, ứng dụng, ngành, nhu cầu
đầu tư…). Đừng thấy trùng tên "lĩnh vực" mà xoá nhầm.

#### 30f. Hình thức 4 ô trên tab Dữ liệu quản trị (chốt 27/09/2026)

- **Riêng theo từng công ty**: cùng một mã hàng, TPE khai *Công nghiệp → …*, ETEK POWER khai
  *Môi trường → …* đều được. 4 giá trị lưu cùng chỗ với dữ liệu quản trị theo công ty.
- **Tối thiểu 3 cấp**: bắt buộc tới **Nhóm công việc**; **Cụm công việc** để trống được
  (danh mục này hiện chỉ có 2 dòng, ép chọn đủ 4 cấp là tắc).
- 4 ô **lọc dây chuyền**: chọn Lĩnh vực mới hiện Chương; đổi cấp trên thì **xoá giá trị cấp dưới**
  (tránh bẫy `resetKeys` đã ghi ở sổ chốt).

#### 30g. FORM HÀNG HOÁ CHIA 2 TẦNG TAB (user chốt 28/09/2026)

> Nguyên văn: *"Chia thành 2 tab cha: Thông tin hàng hoá / Quản trị hàng hoá · Tab Thông tin hàng
> hoá: có 4 tab con: Thông tin chung / Thông số kỹ thuật / Mua hàng / Phân loại xe / Nhóm máy ·
> Tab Dữ liệu quản trị: Gồm các thông tin cũ + phần 4 cấp catalog vừa nêu"*.
> *(Yêu cầu ghi "4 tab con" nhưng liệt kê 5 mục — làm theo danh sách liệt kê: **5 tab con**.)*

**Cấu trúc mới của `/master-data/products/{id}`:**

```
[ Thông tin hàng hoá ]  [ Quản trị hàng hoá ]        ← tab CHA
  └ Thông tin chung · Thông số kỹ thuật · Mua hàng · Phân loại xe · Nhóm máy   ← tab CON
                          └ Dữ liệu quản trị (khối cũ) + Phân loại theo lĩnh vực kinh doanh (4 cấp)
```

- **Tab cha = SEGMENTED CONTROL kiểu iOS** (sửa lần 3, user chốt 28/09: *"thiết kế tab cha + hiệu
  ứng giống iOS của Apple"*) — bám đúng cách Apple làm `UISegmentedControl`:
  · track nền **`rgba(118,118,128,.12)`** (đúng mã xám hệ thống iOS), bo **10px**, padding 2px
  · viên trắng là **MỘT phần tử TRƯỢT**, không phải đổi nền từng mục: đổi tab thì nó **chạy sang**
    bằng `transform`, easing **`cubic-bezier(.32,.72,0,1)`** — nhịp "mượt cuối" của iOS, 340ms
  · bóng 3 lớp `0 3px 8px rgba(0,0,0,.12)` + `0 3px 1px rgba(0,0,0,.04)` + viền tóc `0 0 0 .5px`
  · **nhấn xuống mục lún nhẹ `scale(.96)`**, thả ra bật lại
  · **vạch phân cách mảnh** giữa 2 mục, tự mờ khi viên trắng chạy tới
  · icon inline SVG: **khối hộp** cho *Thông tin hàng hoá*, **thanh trượt cấu hình* cho *Quản trị
    hàng hoá*; icon đổi màu teal theo mục đang chọn
  ⚠️ Thumb đặt theo **toạ độ đo thật** (`offsetLeft`/`offsetWidth`) nên: đo trong
  `requestAnimationFrame` (đo cùng nhịp là ra vị trí của lần vẽ trước), đo **lại sau khi form hiện
  ra** (lúc `doiTabCha` chạy thì section còn `display:none`, số đo ra 0), và nghe `resize`.
- **Tab con = STEPPER** (*"thiết kế dạng các step cho khác tab cha"*): vòng tròn số 26px + nhãn +
  đường nối 2px. Step **đang mở** nền primary `#1abc9c` + quầng `rgba(26,188,156,.16)`; step **đã
  qua** nền `#e8f8f4` viền teal kèm **dấu ✓**; step **chưa tới** xám. Bấm được mọi step (form không
  ép khai tuần tự), step chỉ để thấy tiến độ.
- **Chấm đỏ trên tab cha** khi tab đó còn ô bắt buộc chưa khai; khai đủ 3 cấp là **tắt ngay**,
  không phải bấm Lưu lại.
- Tab *Quản trị hàng hoá* **không có tab con** — một trang gồm 2 khối.
- **3 mức quyền §26c-bis giữ nguyên, chỉ đổi cách khoá**: hàng của công ty khác ⇒ **cả tab cha
  "Thông tin hàng hoá"** bị làm mờ và form mở thẳng vào tab *Quản trị hàng hoá*.
  Dải báo đổi chữ theo tên tab mới.
- ⚠️ Mỗi thanh tab một `id` riêng (`#tab-cha` · `#tab-chinh` · `#tab-dvt`): selector
  `#sc-form .nav-link` quét trúng cả ba, dùng chung là mất trạng thái đang mở.
- ⚠️ Chỉ số tab con **không còn trùng `data-i`** (tab con là 0·1·2·**4**·5 vì *Dữ liệu quản trị*
  rời sang tab cha) — chỗ nào khoá/mở tab phải đọc `data-i`, không đọc chỉ số mảng.

**Đã đo bằng Playwright (console 0 lỗi):**

| Phép kiểm | Kết quả |
|---|---|
| Cấu trúc | 2 tab cha · 5 tab con (`data-i` 0·1·2·4·5) · pane *Dữ liệu quản trị* chỉ hiện ở tab cha thứ 2 |
| Nội dung tab Quản trị | 2 khối: **Dữ liệu quản trị** (cũ) + **Phân loại theo lĩnh vực kinh doanh** (4 ô) |
| Lọc dây chuyền | đổi *Lĩnh vực* ⇒ 3 cấp dưới **xoá sạch**, ô cấp dưới **khoá** lại, danh sách Chương vẽ lại đúng nhánh |
| Lĩnh vực đang khoá | *Khác* (`status = 2` trong DB) hiện **🔒 Khác** đúng quy ước select khoá |
| Riêng theo công ty | cùng mã `TPE-CN-2T-4500`: TÂN PHÁT = *Dịch vụ ô tô → Thiết bị gara → Trang bị gara tiêu chuẩn → Cụm thiết bị lốp*; TÂN PHÁT SG = *Công nghiệp → Thiết bị nâng hạ → Lắp đặt cầu nâng*. Đổi ô "Đang làm việc tại" là khối vẽ lại theo công ty mới |
| Validate tối thiểu 3 cấp | bấm **Lưu** khi chưa khai ⇒ tự nhảy sang tab *Quản trị hàng hoá*, tô đỏ **đúng 3 ô** (Cụm công việc **không** bị tô), dòng lỗi *"Bắt buộc phải nhập: …"*, toast, **không rời form** |
| Hàng của công ty khác | mở thẳng tab *Quản trị hàng hoá*; tab cha *Thông tin hàng hoá* + cả 5 tab con **mờ**; 2 khối trong tab quản trị vẫn sửa được |
| Thanh tab | cao 41px, 2 tab cha không chồng lấn |

**2 lỗi TRÙNG TÊN CLASS bắt được khi dựng (cả hai đều làm hỏng giao diện, không lỗi JS nào báo):**

1. `.step` của stepper **trùng `.step` của màn Sơ đồ luồng** (`border` + `min-width:250px`, khai sau
   nên thắng) ⇒ mỗi bước bị **bọc khung card** và kéo rộng 250px. Đổi tiền tố riêng **`.fstep*`**.
2. `.loi` gán cho ô select **trùng `.loi{display:none}`** có sẵn của popup Import ⇒ **3 ô select
   biến mất sạch** khi báo lỗi, chỉ còn nhãn. Đổi thành **`.o-loi`**.
   📌 Bài học ghi lại: mockup này đã dài 313 KB, **đặt class mới phải grep trước**; và chỉ nhìn số
   liệu DOM là không đủ — 2 lỗi trên đều chỉ lộ khi **chụp ảnh và nhìn**.

**Đo hiệu ứng trượt bằng Playwright:** thumb bắt đầu ở x=73 (trùng mục *Thông tin hàng hoá*,
rộng 180px = đúng bề rộng mục) → sau 120ms đang ở **x=229 (giữa đường)** → dừng ở x=253 trùng mục
*Quản trị hàng hoá*: **có trượt thật**, không nhảy. Đổi qua lại nhiều lần vẫn bám đúng; thu cửa sổ
về 900px thumb tự đo lại (180/180); hàng của công ty khác ⇒ thumb nằm sẵn ở *Quản trị hàng hoá*,
mục kia `opacity .4`.

Ảnh: `anh-mockup/30-tab-cha-ios-segmented.png` · `30-form-tab-quan-tri-hang-hoa.png` ·
`30-catalog-validate-thieu-3-cap.png`.

---

### 31. RÀ SOÁT FORM NHẬP THEO ERP (user yêu cầu 28/09/2026)

> Nguyên văn: *"Trường model để input là sai ⇒ rà soát lại form nhập đang dùng ở ERP để xử lý triệt
> để các vấn đề sai/thiếu"* · *"Hiệu ứng khi hover làm tương tự khi active tab"*.

**Cách rà**: bóc **toàn bộ 42 ô nhập + 19 khối** của `products/form.blade.php` (ERP) kèm **kiểu điều
khiển thật** (input / select / select nhiều / checkbox / textarea / CKEditor), rồi đối chiếu với
mockup — đối chiếu cả ô nằm trong **bảng** (`<th>`), không chỉ ô có nhãn.

#### 31a. 7 lỗi đã sửa

| # | Trường | Mockup (sai) | ERP (đúng) |
|---|---|---|---|
| 1 | **Model** | input gõ tay | **SELECT** `select2-model` (danh mục `product_models` **39.796 dòng**) + **nút [+] tạo nhanh**, **bắt buộc**, ERP còn khoá khi sửa (`ng-disabled="edit"`) |
| 2 | **Code đặt hàng** | input | **SELECT** (`order_codes` 8.664) + nút [+] |
| 3 | **Thuế nhập khẩu (không có CO)** | input | **SELECT** lấy từ `tax_rates` + nút [+] |
| 4 | **Thuế nhập khẩu (có CO)** | input | **SELECT** + nút [+] |
| 5 | **Thuế chống bán phá giá (%)** | input | **SELECT** + nút [+] |
| 6 | **Tính thuế bảo vệ môi trường** | ô chọn *Có / Không* (tự bịa) | **CHECKBOX**; ô *Hệ số tính thuế BVMT* **khoá khi chưa tick** (`ng-disabled="!product.need_environment_tax"`) |
| 7 | **Đơn vị bảo hành** | Tháng / Năm / **Giờ chạy máy** (bịa) | **Ngày / Tháng / Năm** |
| 8 | **Phụ kiện tiêu chuẩn** | textarea | **CKEditor** (ERP dùng `ck-editor` y như ô *Đặc điểm*) — đồng thời trả lời luôn tồn "*Phụ kiện tiêu chuẩn có đổi sang CKEditor không*" ở §26 |
| 9 | Tiêu đề khối | *Vật tư phục vụ sửa chữa – **bảo hành*** | *Vật tư phục vụ sửa chữa – **bảo dưỡng*** |

**Hover tab cha**: mục chưa chọn khi rê chuột nay hiện **đúng "viên trắng" như lúc được chọn**, chỉ
nhạt hơn — nền `rgba(255,255,255,.62)`, chữ `#0a7c88`, icon `#0a99a7`, bóng nhẹ (đo thật).

#### 31b. 🐞 Lỗi của chính đợt rà — ghi lại để không lặp

Bản rà đầu tiên kết luận **"mockup thiếu hẳn khối Đơn vị tính và Thông số cơ bản"** và tôi đã thêm
2 khối mới. **SAI**: mockup vốn đã có cả hai, thậm chí **đủ hơn** (Thông số cơ bản có cột *Bắt buộc* /
*In tem*; Đơn vị tính có cột *Quy đổi*). Script rà chỉ quét nhãn `v2-label` nên **không thấy trường
nằm trong bảng**. Hậu quả: 2 khối trùng, lại **nằm ngoài mọi `.tpane`** nên hiện ở cả tab *Mua hàng*
và không bị khoá theo quyền. Đã gỡ sạch.

📌 **Bài học**: rà form phải quét **cả `<th>` của bảng**, và **nhìn ảnh** — lỗi này chỉ lộ khi chụp
màn hình ra xem, mọi số liệu DOM trước đó đều "đúng".

#### 31c. Đối chiếu khối: ERP 19 khối ↔ mockup 16 khối — khớp

Gộp/đổi chỗ có chủ ý: *Tài liệu kỹ thuật* + *Ảnh hàng hóa* + *Video* → **một khối**; *Phụ kiện tiêu
chuẩn* + *Đặc điểm* → **một khối**; *Đặt hàng* → tách **Khai báo hải quan** + **Thuế**; *Kho hàng*
(SL tồn kho tối thiểu) → vào **Dữ liệu quản trị** theo công ty (§24); *Phụ tùng – Phụ kiện* → tab
**Nhóm máy**; *Phụ tùng ô tô* → tab **Phân loại xe**.

**Cố ý không có** (đã chốt trước đó): *Loại hàng hóa* (`product_cate` đóng băng §3) · *Nhóm hàng hóa*
(`groups` §21) · *Giá theo đơn vị* phần giá, *Hệ số giá theo công ty*, *Giá mua ngoài*, *Hệ số/Định
mức hàng thúc đẩy bán* (→ Phiếu tính giá §29 + Phase 8).

Ảnh: `anh-mockup/31-form-sau-ra-soat-erp.png`.

---

### 32. XẾP LẠI NHÓM "PHÂN LOẠI" VÀ TAB "MUA HÀNG" (user chốt 28/09/2026)

> Nguyên văn: *"Nhóm Phân loại đang chưa đúng: xếp theo thứ tự từ con các danh mục load cascade ⇒
> cha ở 4 cấp phân loại · Đặc tính sản phẩm để cuối · Nhóm Mua hàng cũng tối ưu lại cách sắp xếp
> hợp lý hơn"*.

#### 32a. Nhóm Phân loại — ~~cascade cha → con~~ → **CHỌN CẤP CON, CẤP CHA TỰ ĐIỀN**

> ⚠️ **Đã đổi lại 28/09/2026** (cùng ngày): *"Nhóm phân loại user sẽ chọn cấp con Loại sản phẩm
> trước ⇒ cấp cha load tự động theo"*. Bản cascade 4 lần chọn mô tả bên dưới **không dùng nữa** —
> giữ lại để biết đã qua những bước nào.

**Bản đang dùng:**

**Thứ tự hiển thị vẫn đúng chiều cây CHA → CON** (user chốt lại 28/09), chỉ cách NHẬP là ngược:
người dùng chọn cấp con, ba cấp cha tự điền.

| Hàng | Ô |
|---|---|
| 1 | Tính chất hàng hoá (c4) · Nhóm chức năng (c4) · Nhóm sản phẩm (c4) — **cả 3 tự điền, chỉ đọc** |
| 2 | **Loại sản phẩm** (c6, **select + nút [+]**, bắt buộc — ô DUY NHẤT phải chọn) · **Đặc tính sản phẩm** (c6) — không thuộc cây nên ở cuối |

Đọc từ trái sang, trên xuống ra đúng đường dẫn cây; ô phải thao tác (*Loại sản phẩm*) vẫn nổi bật
vì là ô duy nhất mở, lại có nút [+] bên cạnh.

- Chọn Loại sản phẩm ⇒ **3 cấp cha tự điền** theo cây; bỏ chọn ⇒ xoá trắng cả ba. Ô cha luôn
  `disabled`, placeholder *"Tự điền theo Loại sản phẩm"*.
- Nhanh hơn hẳn cascade (1 lần chọn thay vì 4) và **không bao giờ khai lệch nhánh**.
- ⚠️ **Điều kiện để suy ngược đúng**: mỗi *Loại sản phẩm* phải thuộc **đúng một** *Nhóm sản phẩm* —
  đúng cấu trúc cây Phase 0. Dữ liệu demo trước đó có **3/7 loại nằm ở 2 nhánh** (*Máy nén khí trục
  vít*, *Phụ tùng lọc dầu*, *Thiết bị gara*) nên suy ngược sẽ mơ hồ; đã tách thành *Bình chứa khí
  nén*, *Phụ tùng lọc gió*, *Thiết bị phụ trợ gara* ⇒ còn **0 loại trùng nhánh / 10 loại**.
  📌 Khi làm thật: đây là **ràng buộc dữ liệu** của danh mục Loại sản phẩm, phải chặn ở khâu khai
  danh mục chứ không phải ở form hàng hoá.

**Đã đo (console 0 lỗi):** tạo mới ⇒ 4 ô rỗng, 3 ô cha `(đọc)` · chọn *Cầu nâng ô tô 2 trụ* ⇒ tự
điền *Thiết bị · Gara · Cầu nâng* · đổi sang *Phụ tùng lọc gió* ⇒ *Phụ kiện · Lọc · Lọc gió* · bỏ
chọn ⇒ xoá trắng cả ba · mở hàng có sẵn ⇒ nạp đúng 4 cấp · hàng công ty khác ⇒ khoá hết.
Ảnh: `anh-mockup/32-nhom-phan-loai-chon-cap-con.png`.

<details><summary>Bản cũ (cascade cha → con) — không dùng nữa</summary>

#### 32a-cũ. Nhóm Phân loại — 4 cấp CHA → CON, load cascade

**Trước:** *Loại sản phẩm* (cấp CON, lá của cây) đứng đầu, 3 cấp cha (*Tính chất hàng hoá · Nhóm
chức năng · Nhóm sản phẩm*) nằm dưới ở dạng **ô khoá** suy ngược ra — ngược chiều đọc và không khai
được từ trên xuống. *Đặc tính sản phẩm* nằm chen giữa.

**Sau:**

| Hàng | Ô |
|---|---|
| 1 | **Tính chất hàng hoá** (c4) · **Nhóm chức năng** (c4) · **Nhóm sản phẩm** (c4) |
| 2 | **Loại sản phẩm** (c6) · **Đặc tính sản phẩm** (c6) — *Đặc tính không thuộc cây nên xếp cuối* |

- Cả 4 cấp là **SELECT cascade**: chọn cấp trên mới mở cấp dưới; đổi cấp trên ⇒ **xoá sạch cấp
  dưới** (cùng luật với cây lĩnh vực ở tab *Quản trị hàng hoá* §30f).
- Cây dựng **từ chính dữ liệu hàng hoá demo** (`duong` + `type`) nên không lệch với màn danh sách.
- Mỗi hàng đủ **12 cột**, không để ô lẻ một dòng.

</details>

#### 32b. Tab Mua hàng — tách 3 khối theo đúng việc

| Khối | Ô | Ghi chú |
|---|---|---|
| **Khai báo hải quan** | Tên khai báo hải quan (c6) · HS Code (c6) | bỏ *SL tối thiểu nhập mua* ra — nó không phải khai báo hải quan |
| **Thuế** | % VAT · Thuế NK (không có CO) · Thuế NK (có CO) · Thuế chống bán phá giá — **cả 4 đều SELECT + nút [+]** · rồi checkbox *Tính thuế BVMT* (c6) + *Hệ số tính thuế BVMT* (c6) | bỏ *% giảm giá thanh lý* ra — không phải thuế. **% VAT bổ sung nút [+] và dấu `*`** cho khớp ERP |
| **Đặt hàng** *(mới)* | SL tối thiểu nhập mua (c6) · % giảm giá thanh lý (c6) | gộp 2 khối *Đặt hàng* + *Khác* của ERP |

#### 32c. 🐞 Lỗi bắt được: vòng phân quyền xoá mất trạng thái khoá riêng

`datVaiForm` quét **mọi** `input/select` của pane để mở/khoá theo quyền, nên nó **xoá luôn** các
trạng thái khoá riêng đặt trước đó — tạo mới thì 3 cấp dưới của cây **mở hết** thay vì khoá chờ chọn
cấp trên (đúng y lỗi đã gặp với ô *Hệ số tính thuế BVMT*). Sửa: đặt lại cả hai **sau** vòng phân
quyền, trong chính `datVaiForm`.

**Đã đo (console 0 lỗi):**

| Ca | Kết quả |
|---|---|
| Tạo mới | `tc=∅` · `cn=∅(khoá)` · `sp=∅(khoá)` · `type=∅(khoá)` |
| Chọn cấp 1 | `tc=Thiết bị` · `cn=∅` mở ra · 2 cấp dưới vẫn khoá |
| Khai đủ cây | Thiết bị → Gara → Cầu nâng → Cầu nâng ô tô 2 trụ |
| Mở hàng đã có | nạp đủ 4 cấp đúng đường dẫn của hàng hoá |
| Hàng công ty khác | cả 4 cấp + Đặc tính **khoá hết** theo quyền |
| Đổi cấp trên | 3 cấp dưới xoá sạch, danh sách cấp 2 vẽ lại đúng nhánh |

Ảnh: `anh-mockup/32-nhom-phan-loai-cascade.png` · `32-tab-mua-hang.png`.

#### 32d. Ô TICK / Ô CHỌN kiểu Apple (user chốt 28/09/2026)

> Nguyên văn: *"các button checkbox thiết kế cũng theo phong cách apple nhé"*.

Bỏ ô vuông mặc định của trình duyệt (`appearance:none`), vẽ lại theo cách Apple làm — áp **toàn
cục** cho mọi ô tick/chọn của mockup (**24 ô**: 20 checkbox + 4 radio) để không mỗi bảng một kiểu:

| | Chưa chọn | Đã chọn |
|---|---|---|
| **Ô tick** | 18×18, bo **5px**, viền `rgba(60,60,67,.30)` (mã xám hệ thống iOS), nền trắng | nền **`#1abc9c`** (primary của app), dấu **✓ trắng** vẽ bằng 2 cạnh border xoay 45° |
| **Ô chọn (radio)** | 18×18 **tròn**, cùng kiểu viền | nền `#1abc9c` + **chấm trắng 6px** giữa |

- Dấu ✓ và chấm tròn **vẽ ra bằng animation** `.2s cubic-bezier(.32,.72,0,1)` — cùng nhịp easing
  với thumb của segmented control (§30g), nên cả form cảm giác đồng bộ.
- **Nhấn xuống lún** `scale(.9)`; đi bằng bàn phím có **quầng sáng** `0 0 0 3.5px rgba(26,188,156,.25)`
  (`:focus-visible`, không hiện khi bấm chuột).
- Ô **khoá**: mờ .4, nền `#f1f5f9`; khoá mà đang tick thì nền teal nhạt `#9fd9cc` — vẫn đọc được
  trạng thái, đúng cách iOS xử lý điều khiển bị vô hiệu.

**Đã đo (console 0 lỗi):** chưa tick nền `#fff` viền `rgba(60,60,67,.3)` → tick xong nền + viền
`rgb(26,188,156)`, `::after` 4×9px màu trắng xoay 45° kèm animation `tickApple`; radio nền teal +
chấm trắng 6px, animation `dotApple`. ⚠️ Đo ngay sau khi tick sẽ ra **màu cũ** vì `transition .18s`
chưa chạy xong — phải chờ rồi mới đọc.

⚠️ **Không phá công tắc có sẵn**: ô *Chỉ công ty đã khai* ở màn Chính sách giá dùng khuôn `.sw`
(input ẩn `opacity:0`, track + knob vẽ riêng) — đã kiểm lại, công tắc vẫn đúng 200×36 và input ẩn
không lòi ra.

Ảnh: `anh-mockup/33-o-tick-o-chon-kieu-apple.png`.

### 33. XÂY DỰNG CATALOG KINH DOANH — KHO DỮ LIỆU HÀNG HOÁ CÔNG TY (user chốt 29/09/2026)

> Nguyên văn yêu cầu: *"Sẽ cập nhật từ bảng Hàng hoá đang kinh doanh: Là các hàng hoá đã đưa vào
> 4 cấp catalog + status là 1 · Bổ sung bộ lọc theo 4 cấp catalog vào đầu bộ filter · Thêm button
> xây dựng catalog ⇒ mở popup để chọn nhanh các hàng hoá vào Cụm Công việc"* và chốt tiếp:
> *"Nếu catalog lấy nguồn cả ở hàng hoá chưa có giá thì chuyển chức năng Xây dựng catalog sang màn
> hình Kho dữ liệu hàng hoá Công ty — tổng tất cả hàng hoá của công ty ở tất cả trạng thái ⇒ màn
> Hàng hoá đang kinh doanh vẫn sửa như đã note nhưng không để button xây dựng catalog ở đó"*.

#### 33a. 7 đáp án chốt trước khi dựng

| # | Câu | Đáp án |
|---|---|---|
| 1 | Một mã hàng (trong 1 công ty) gán được bao nhiêu nhánh catalog? | **NHIỀU nhánh** — cần **bảng nối** mới, không còn là 4 cột trên bảng dữ liệu quản trị |
| 2 | Gán ở cấp nào | **CHỈ cấp lá — Cụm công việc** (bỏ luật "tối thiểu 3 cấp, cụm tuỳ chọn" của §30f) |
| 3 | Phạm vi công ty | **Chỉ công ty đang đăng nhập** (khớp §23c: cấm sửa chéo công ty) |
| 4 | Form hàng hoá xử lý sao | **Sửa theo nhiều nhánh** — 4 ô select → **bảng danh sách nhánh** |
| 5 | Nguồn hàng hoá của popup | **Toàn bộ hàng hoá của công ty, mọi trạng thái** |
| 6 | Gỡ khỏi cụm làm ở đâu | **Trong popup** (tab *Hàng trong cụm*) **và trong form sửa hàng hoá** (xoá dòng) — KHÔNG có ở lưới danh sách |
| 7 | Cách lưu trong popup | **Gom vào giỏ chờ, bấm Lưu một lần** (`+N / −M` + Hoàn tác) |

Ba đề xuất kèm theo user không phản đối: `status = 1` hiểu là trạng thái **"Đang kinh doanh"** của
cặp (mã hàng × công ty) theo §26a (không phải `products.status` của ERP) · chọn nhanh gồm **tick
nhiều dòng · "Chọn tất cả N kết quả lọc" · dán danh sách mã** (không kéo–thả, không import file
riêng) · quyền **"Xây dựng catalog kinh doanh"** riêng cho nút mở popup, không có quyền thì **ẩn nút**.

#### 33b. ⚠️ Quyết định này ĐẢO 2 điểm của §30f/§30g (dựng ngày 28/09)

| Điểm | §30f/§30g (28/09) | §33 (29/09) |
|---|---|---|
| Số nhánh mỗi (hàng hoá × công ty) | đúng **1** | **nhiều** |
| Cấp bắt buộc | tối thiểu **3 cấp**, Cụm để trống được | **đủ 4 cấp**, bắt buộc tới **Cụm công việc** |
| Giao diện trong form | 4 ô select lọc dây chuyền | **bảng danh sách nhánh** + hàng "Thêm nhánh" (4 ô lọc dây chuyền) |
| Chỗ lưu | 4 cột trên `product_company_coefficients` (§30b mục 5) | **bảng nối** `product_id × company_id × job_cluster_id` |

Hệ quả kéo theo: **cây demo phải có cụm ở mọi Nhóm công việc** — nhóm không có cụm là nhánh chết,
không xếp được hàng vào. Đã bổ sung cụm cho toàn bộ 17 nhóm của cây demo.

#### 33c. Màn MỚI — "Kho dữ liệu hàng hoá Công ty" (`sc-kho`)

- **Nguồn**: mọi hàng hoá công ty đang đăng nhập đang có, **cả 4 trạng thái** của §26a, **gồm cả
  hàng do công ty khác tạo mà công ty mình đã lấy về** (phân biệt bằng cột *Công ty quản lý*).
- **Bộ lọc**: hàng 1 = **4 ô catalog lọc dây chuyền** + ô tick *Chỉ hàng chưa xếp catalog*;
  hàng 2 = ô tìm nhanh + **Trạng thái** + Tìm kiếm / Làm mới; còn lại trong *Tìm kiếm nâng cao*.
- **Bộ cột**: bộ chuẩn §26f + **Catalog kinh doanh** (chip `Lĩnh vực › Chương › Nhóm › Cụm`, nhiều
  nhánh thì thêm chip `+N` rê chuột xem hết) + *Trạng thái* + *Công ty quản lý*; có popup cấu hình cột.
- **Nút "Xây dựng catalog"** ở toolbar lưới → mở popup. **Thao tác hàng loạt**: tick nhiều dòng trên
  lưới → thanh xanh hiện *Đã chọn N* + nút **Xếp vào cụm…** (mở popup, mang sẵn N mã đã tick).
- Màn **chỉ tra cứu + xếp catalog**: **không có nút Tạo mới** (tạo hàng vẫn ở màn *Đang nhập thông tin*).

#### 33d. Popup "Xây dựng catalog kinh doanh"

Khuôn `V2BaseModal`: body cuộn riêng, **footer ghim đáy** (đo thật: đáy footer 672.66 = đáy modal 672.66).

- **Trái**: cây 4 cấp, mỗi nút hiện **số hàng hoá đang thuộc nhánh** (đã cộng cả giỏ chờ nên tick
  xong thấy số nhảy ngay); ô tìm trong cây mở bung mọi cấp khớp; lĩnh vực khoá hiện **🔒**.
  Mặc định: Lĩnh vực + Chương đóng, **Nhóm công việc mở** để thấy ngay danh sách cụm.
- **Phải**: 2 tab — **Thêm hàng vào cụm** (nguồn = toàn bộ hàng công ty) / **Hàng trong cụm (N)**
  (tick → nút đổi thành **Gỡ khỏi cụm**, màu đỏ nhóm nguy hiểm).
- **Chọn nhanh**: tick nhiều dòng · **"Chọn tất cả N kết quả lọc"** · **Dán danh sách mã** (mỗi mã
  một dòng, báo rõ *đã tick x/y · z mã không nằm trong danh sách đang lọc · t mã KHÔNG TỒN TẠI*).
- **Giỏ chờ**: footer hiện `Đang chờ lưu: +12 · −3` + **Hoàn tác** (bỏ **cả lượt** gần nhất, vì một
  lần bấm có thể là hàng trăm dòng) + **Lưu**. Đóng khi còn giỏ chờ ⇒ popup cảnh báo *Thông tin chưa lưu*.

#### 33e. Màn "Hàng hoá đang kinh doanh" (`sc-l3`) — sửa 3 chỗ

1. **Điều kiện vào màn**: trạng thái *Đang kinh doanh* **VÀ** có ≥ 1 nhánh catalog của công ty đang
   đăng nhập.
2. **4 ô lọc catalog lên ĐẦU bộ lọc**, luôn hiện (không giấu trong *Tìm kiếm nâng cao*); hàng nhiều
   nhánh khớp **bất kỳ nhánh nào**.
3. **Dòng nhắc** màu cam trên lưới: *"Còn N hàng hoá đang kinh doanh chưa xếp catalog nên chưa hiện
   ở màn này — mở Kho dữ liệu hàng hoá Công ty để xếp"*. Không có dòng này thì user tưởng mất hàng.
   **Không có nút "Xây dựng catalog" ở màn này** (user chốt).

#### 33f. Form hàng hoá — tab *Quản trị hàng hoá*

Khối *Phân loại theo lĩnh vực kinh doanh* `*`:
bảng **STT · Lĩnh vực · Chương · Nhóm công việc · Cụm công việc · [nút xoá]** + hàng **Thêm nhánh**
(4 ô lọc dây chuyền + nút *Thêm nhánh*). Luật: **≥ 1 nhánh mới lưu được**; mỗi nhánh **đủ 4 cấp**;
**chặn trùng nhánh**; báo lỗi **đồng thời hết các ô thiếu** (không bắt sửa từng ô); xoá dòng = **gỡ
hàng hoá khỏi cụm**.

#### 33g. Đã đo bằng Playwright trên trình duyệt thật (console 0 lỗi)

| Việc | Số đo |
|---|---|
| Màn Kho | 10 hàng của TÂN PHÁT ở **cả 4 trạng thái**, 16 cột (có ô tick + *Catalog kinh doanh* + *Công ty quản lý*) |
| Chip catalog | hàng 2 nhánh hiện `Dịch vụ ô tô › … › Cụm thiết bị lốp` + chip `+1` **cùng hàng** (chip cắt ở 252px) |
| Lọc dây chuyền | chọn cấp trên mới mở cấp dưới; đổi cấp trên **xoá sạch** 3 ô dưới (kiểm `value` = rỗng) |
| Màn kinh doanh | 3 hàng *Đang kinh doanh* → chỉ **2** hàng có catalog hiện ra; dòng nhắc *"Còn 1…"* `display:flex` |
| Cây popup | đếm đúng theo giỏ chờ: thêm 2 hàng ⇒ cụm 0→2, chương 1→3, lĩnh vực cộng dồn |
| Thêm/gỡ | thêm xong hàng **nhảy sang tab "Hàng trong cụm"** ngay (tab Thêm 10→8 dòng) |
| Dán mã | `Đã tick 2/4 mã · 1 mã không nằm trong danh sách đang lọc (SG-MKD-SC-800) · 1 mã KHÔNG TỒN TẠI (MA-KHONG-CO-01)` |
| Lưu | ghi đúng vào dữ liệu; đếm màn kinh doanh 2 → **3**, dòng nhắc tắt |
| Đóng khi chưa lưu | popup cảnh báo *"Còn 2 lượt xếp chưa lưu"*; **Hoàn tác** trả cụm về 0 |
| Footer popup | đáy footer **672.66** = đáy modal **672.66** ⇒ ghim đáy thật |
| Form | hàng 2 nhánh hiện 2 dòng; thiếu cấp báo **1 lượt đủ 3 ô** *"Bắt buộc phải nhập: Chương · Nhóm công việc · Cụm công việc"*; trùng nhánh báo *"Hàng hoá đã nằm trong cụm này rồi"*; chưa có nhánh mà bấm Lưu ⇒ **chặn**, nhảy tab *Quản trị hàng hoá* + chấm đỏ |
| Riêng theo công ty | cùng mã `TPE-CN-2T-4500`: TÂN PHÁT 2 nhánh · TÂN PHÁT SG 1 nhánh (*Cụm cầu nâng 4 trụ*) |

Ảnh: `anh-mockup/33-man-kho-du-lieu.png` · `33-popup-xay-dung-catalog.png` · `33-form-danh-sach-nhanh.png`.
*(Lưu ý: `anh-mockup/33-o-tick-o-chon-kieu-apple.png` là ảnh của §32d, đánh số lệch từ đợt trước.)*

#### 33h. 🐞 4 lỗi tự bắt được khi dựng (đọc code không thấy, phải mở trình duyệt)

1. **Ô tick làm hỏng cột dính**: `ganToaDoCotDinh` duyệt từ ô đầu tiên và **dừng ngay khi gặp ô
   không dính** ⇒ thêm cột tick thường là **mọi cột dính mất toạ độ**. Phải cho ô tick class `dinh`.
2. **`nangCapSelect` nuốt bề rộng**: nó bọc `<select>` bằng div `.ss` và vẽ `.ss-box{width:100%}`,
   nên `style="width:200px"` khai trên chính `<select>` **mất tác dụng** — ô *Trạng thái* chiếm trọn
   hàng, đẩy ô tick xuống dòng. Phải bọc thêm div có bề rộng thật (đúng cách `.fcol` của bộ lọc).
3. **Nhánh khai dở rò sang hàng hoá khác**: `catTam` là biến toàn cục, mở hàng hoá khác vẫn thấy
   4 ô còn nguyên lựa chọn cũ ⇒ dễ bấm *Thêm nhánh* nhầm sang hàng khác. Reset trong `moForm` và
   khi đổi công ty.
4. **Ô lọc khoá mất tên trường**: placeholder `— chọn cấp trên trước —` làm 3 ô liền nhau giống hệt
   nhau, không biết ô nào là Chương. Ô lọc không có nhãn ngoài ⇒ phải giữ **tên trường** rồi mới nối
   lý do: `Chương — chọn cấp trên trước`.

#### 33i. 🔴 Tồn MỚI của §33 — chưa hỏi user, gom vào vòng chốt chung

| # | Tồn | Vì sao phải chốt |
|---|---|---|
| 1 | **Tên + cấu trúc bảng nối** (`product_business_catalogs`?): chỉ cần `job_cluster_id` (3 cấp trên suy ra được) hay lưu cả 4 cột cho nhanh | Đổi hẳn §30b mục 5; ảnh hưởng 4 chỗ lọc trong `Product::searchByFilter` |
| 2 | **Ràng buộc mỗi Cụm công việc thuộc đúng 1 Nhóm** | Không có ràng buộc này thì không suy ngược được đường dẫn cây (đúng bài học §32a với *Loại sản phẩm*) |
| 3 | **45.890 hàng đang kinh doanh chưa có catalog** — bật điều kiện lọc ngay là **màn danh mục kinh doanh trắng trơn** | Phải chốt: bật ngay + dòng nhắc, hay tạm hiện cả hàng chưa xếp cho tới khi khai xong (giống thứ tự bắt buộc ở §30d) |
| 4 | **Quyền** "Xây dựng catalog kinh doanh": tên chuẩn + id, gate cả nút lẫn endpoint | Khuôn Phase 1; chưa có trong `PermissionsTableSeeder` |
| 5 | **Gỡ nhánh CUỐI CÙNG** của một hàng đang kinh doanh ⇒ hàng **biến mất khỏi màn kinh doanh** | Có cảnh báo trước khi gỡ không, hay cứ gỡ rồi báo lại? |
| 6 | **"Chọn tất cả N kết quả lọc" với 45.890 dòng** | FE không được gửi 45.890 id ⇒ cần endpoint gán **theo BỘ LỌC** (`POST .../assign-by-filter`), khớp yêu cầu hiệu năng của CLAUDE.md |
| 7 | File **Xuất Excel** của màn Kho có cột Catalog không (nhiều nhánh thì xuống dòng hay tách dòng) | Ảnh hưởng `ExportColumnRegistry` |
| 8 | Kho có hiện **hàng công ty khác CHƯA lấy về** không | Hiện tại **không** (đúng §26d: phải lấy về mới khai được); ghi lại để khỏi hỏi lại |

#### 33j. VÒNG 2 — góp ý sau khi user xem mockup (29/09/2026)

**Màn Kho dữ liệu hàng hoá** (7 việc):

| # | Góp ý | Đã làm |
|---|---|---|
| 1 | Bộ lọc chưa đúng format chuẩn; **trường mặc định = tìm nhanh + 4 cấp catalog** | Dựng theo khuôn `V2BaseSmartFilterPanel`: **hàng 1** ô tìm nhanh + công tắc lọc nhanh + *Tìm kiếm* / *Làm mới*; **hàng 2** 4 ô catalog lọc dây chuyền (luôn hiện); **Trạng thái và 12 ô còn lại chuyển vào *Tìm kiếm nâng cao*** |
| 2 | Bỏ chữ *"Công ty"* ở cuối tên menu | Menu **và** tiêu đề lưới đều thành **"Kho dữ liệu hàng hoá"** |
| 3 | Cột Catalog chỉ hiện **Cụm**, hover mới bung 4 cấp | Chip hiện tên cụm; `data-tip` bung đủ `Lĩnh vực › Chương › Nhóm › Cụm`; nhiều nhánh vẫn `+N` |
| 4 | Mọi cột **không xuống dòng** | `white-space: nowrap` cho 4 lưới danh sách (l1·l2·l3·kho); bảng tràn thì cuộn ngang |
| 5 | Bỏ dòng **số dưới mã hàng** | `oMa()` chỉ còn mã; barcode vẫn là cột riêng, bật ở *Cấu hình cột* |
| 6 | Công tắc *"Chỉ hàng chưa xếp catalog"* đang chiếm nguyên một dòng | Đưa lên **cùng hàng với ô tìm nhanh** |
| 7 | Bỏ **icon menu** trên topbar (bấm không có tác dụng) | Đã gỡ `svg.burger` |

**Popup Xây dựng catalog** (6 việc):

| # | Góp ý | Đã làm |
|---|---|---|
| 1 | Hiện thêm cột thông tin hàng hoá | Bảng nay **10 cột**: tick · Mã · Tên · Model · Loại sản phẩm · Thương hiệu · ĐVT · Trạng thái · Công ty quản lý · Catalog đang xếp |
| 2 | Mỗi lượt tối đa **100 mã** | `GIOI_HAN_CAT = 100`, chặn **ngay lúc tick** (ô tự bỏ tick + toast), *Chọn tất cả N* dừng ở 100 và báo rõ *"đã chọn 100/127 — Lưu xong chọn tiếp"*, dán mã cũng dừng ở trần |
| 3 | Thêm **phân trang + số dòng/trang** | Khuôn `V2BasePagination`: *Hiển thị 1–20 / 127* (en dash) · ô 20/50/100 đứng trước dãy số trang |
| 4 | Click ô **Mã hàng / Tên hàng** cũng tick | 2 ô mang class `o-bam`, bấm là tick/bỏ tick cả dòng, dòng đang chọn tô nền nhạt |
| 5 | **Đổi thứ tự 2 tab** + hiện tên cụm đang xem | Tab 1 = *Hàng trong cụm (N)*, tab 2 = *Thêm hàng vào cụm*; dải xanh *"Đang xem cụm: **Cụm máy nén trục vít** · Công nghiệp › Thiết bị khí nén › Lắp đặt hệ thống khí nén"*. Mở từ nút *Xếp vào cụm…* (đã tick sẵn ngoài lưới) thì vào thẳng tab *Thêm* |
| 6 | Bổ sung trường lọc | Khối *Tìm kiếm nâng cao* trong popup: **10 ô** (Tính chất · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Xuất xứ · ĐVT · Model · Công ty quản lý) + nút *Làm mới* |

**2 việc phải làm kèm (không có thì 3 yêu cầu trên không kiểm được):**

1. **Sinh 140 mã demo** cho TÂN PHÁT (mockup trước chỉ 13 dòng): thật có 45.890 mã, mà với 10 dòng
   thì phân trang, trần 100 và link *"Chọn tất cả N kết quả lọc"* đều không tái hiện được. Kho nay
   **150 dòng**, 4 trạng thái, 1/3 số hàng đang kinh doanh đã có sẵn catalog.
2. **Phân trang thật cho cả 4 lưới danh sách** (l1 · l2 · l3 · kho) — 150 dòng mà đổ hết ra một
   trang là sai chuẩn `V2BasePagination`; STT chạy theo số thứ tự toàn bộ, không reset mỗi trang.

**Đo lại sau vòng 2** (console 0 lỗi): kho *Hiển thị 1–20 / 150*, trang 3 bắt đầu STT **41** ·
lọc *Chỉ hàng chưa xếp* còn **126** · lọc lĩnh vực *Công nghiệp* còn **24** · thanh cuộn trên
**1.828px = scrollWidth 1.828px** (trước khi sửa là **0px** vì đo lúc màn còn ẩn) ·
popup tab *Hàng trong cụm* **23** / tab *Thêm* **127**, đổi 50 dòng/trang ra đúng 50 dòng ·
*Chọn tất cả 127* dừng ở **100**, tick thêm bị chặn (số vẫn 100, ô tự bỏ tick) ·
lọc *Thương hiệu = Bosch* còn **44** · bấm ô Mã hàng tick rồi bấm lại bỏ tick.
Ảnh: `anh-mockup/33b-man-kho-vong2.png` · `33b-popup-vong2.png`.

🐞 **Lỗi vòng 2 tự bắt được:** `dongBoThanhCuon()` chạy lúc **màn còn ẩn** ⇒ `scrollWidth = 0` nên
thanh cuộn trên đặt **0px** (kéo mà bảng không đi); phải đo lại **ngay khi màn hiện** trong `moMan`.
Đây đúng bẫy ở skill `list-page` mục 3b-8 — bề rộng ghi cứng (1340px…) cũng sai vì từ vòng 2 mọi ô
để một dòng nên bảng rộng thêm ~300px.

#### 33k. VÒNG 3 — 3 góp ý (29/09/2026)

| # | Góp ý | Đã làm · số đo |
|---|---|---|
| 1 | Popup **mặc định ẩn** bộ lọc nâng cao | Mỗi lần `moXayCatalog()` đều đặt lại `adv-cat` về `display:none` + nhãn nút về *"Tìm kiếm nâng cao"*. Trước đó trạng thái mở của lần trước **còn nguyên trên DOM** nên mở popup lần 2 là 10 ô bung sẵn. Đo: mở lần 1 `none` → bấm mở `flex` → đóng, mở lần 2 lại `none` |
| 2 | Thêm **mở toàn màn hình** cho popup | Nút ⤢ ở thanh tiêu đề (cùng cơ chế `.mask.toan-man` với popup *Xem hàng hoá Công ty khác*), bấm lại thu nhỏ, icon + tooltip đổi theo. Đo: **1460×418 → 1512×773** (đúng khổ cửa sổ), cây **224 → 471px**, bảng **325 → 443px**, footer vẫn **ghim đáy** (773 = 773). Mở popup luôn về khổ thường, không giữ chế độ toàn màn của lần trước |
| 3 | Ô lọc dùng **cỡ nhỏ hơn** cho gọn | 36px → **32px** cho cả ô tìm nhanh, ô lọc `.fsel` và ô lọc custom `.adv .ss-box`; icon kính lúp 15 → 14px, khoảng cách hàng lọc 18 → 12px. Áp cho **mọi màn** để không lệch nhau. Đo: ô tìm nhanh **32px**, ô lọc catalog **32px** |

Ảnh: `anh-mockup/33c-popup-toan-man-hinh.png`.

#### 33l. VÒNG 4 — XẾP LẠI MENU + TÁCH 2 MÀN KHO (user chốt 29/09/2026)

> Nguyên văn: *"Xếp lại menu: Chính sách giá bán nội bộ · Kho dữ liệu hàng hoá · Kho hàng hoá Công
> ty · Hàng hoá nhập thông tin · Hàng đang kinh doanh · Yêu cầu tính giá"*, và trả lời 3 câu hỏi:
> **"Kho hàng hoá Công ty" là màn MỚI, tách làm đôi** · **"Chờ tính giá bỏ đi, giờ đều phải qua
> phiếu tính giá; Phiếu tính giá đưa xuống dưới Yêu cầu tính giá; Ghi chú giữ nguyên vị trí"** ·
> **tên menu lấy đúng nguyên văn**.

**Menu sau khi xếp lại (8 mục):**

| # | Mục | Màn | Đổi gì |
|---|---|---|---|
| 1 | Ghi chú & sơ đồ luồng | `flow` | giữ nguyên vị trí đầu |
| 2 | **Chính sách giá bán nội bộ** | `cf` | đổi tên từ *Cấu hình giá bán nội bộ* |
| 3 | **Kho dữ liệu hàng hoá** | `tong` | **MÀN MỚI** — toàn bộ hàng hoá của **mọi công ty** |
| 4 | **Kho hàng hoá Công ty** | `kho` | màn dựng ở §33c, đổi tên (riêng công ty đang đăng nhập) |
| 5 | **Hàng hoá nhập thông tin** | `l1` | đổi tên từ *Đang nhập thông tin* |
| 6 | **Hàng đang kinh doanh** | `l3` | đổi tên từ *Hàng hoá kinh doanh* |
| 7 | Yêu cầu tính giá | `yc` | — |
| 8 | Phiếu tính giá | `pt` | xếp ngay dưới *Yêu cầu tính giá* |

❌ **BỎ HẲN màn "Chờ tính giá"** (`l2`) — gỡ mục menu, section, `veBang2()`, bộ lọc `BO_LOC.l2`,
cấu hình cột `cotHien.l2`, nhánh `oHanhDong` (nút *Tính giá*) và nhánh giá vốn `man === 'l2'`.
Hệ quả đã xử lý: nút **Lưu** ở form trước đây nhảy sang màn này, nay về **Kho hàng hoá Công ty**
kèm câu *"chuyển sang Chờ tính giá bán, lập Yêu cầu tính giá để đi tiếp"*. Hàng ở trạng thái
*Chờ tính giá bán* / *Đang tính giá* vẫn tra được ở Kho hàng hoá Công ty (lọc theo Trạng thái).

**Màn MỚI "Kho dữ liệu hàng hoá" (`sc-tong`)** — phân biệt với Kho hàng hoá Công ty:

| | Kho dữ liệu hàng hoá | Kho hàng hoá Công ty |
|---|---|---|
| Phạm vi | **mọi công ty** (mockup 153 mã; thật 45.890) | chỉ công ty đang đăng nhập (150) |
| Cột riêng | *Công ty quản lý*; *Trạng thái* ghi **"Chưa sử dụng"** khi công ty mình chưa dùng | *Catalog kinh doanh* |
| Bộ lọc mặc định | tìm nhanh + công tắc **Chỉ hàng công ty chưa dùng**; nâng cao có *Công ty quản lý* + *Tình trạng sử dụng* | tìm nhanh + **4 cấp catalog** |
| Hành động | **Lấy về** (hàng chưa dùng) · **Xem** (hàng đang dùng); hàng loạt: tick → *Lấy về công ty* | *Xây dựng catalog* + *Xếp vào cụm…* |
| Giá vốn | **không có cột** (màn tra cứu chung) | có (theo cấu hình cột) |

*Lấy về* đặt trạng thái **Đang nhập thông tin** cho công ty đang đăng nhập — đúng luồng §26d.

**Đo sau vòng 4** (console 0 lỗi): menu đúng 8 mục theo thứ tự trên, không còn `nav-l2`/`sc-l2` ·
Kho dữ liệu *Hiển thị 1–20 / 153*, lọc *chỉ hàng chưa dùng* còn **3** · bấm **Lấy về** 1 mã thì Kho
công ty **150 → 151**, trạng thái `nhap` · tick 3 dòng → thanh xanh *Đã chọn 2* (1 mã đã lấy ở bước
trước) → lấy hàng loạt ra **153** · bấm **Lưu** ở form nay dừng ở **Kho hàng hoá Công ty** ·
mọi ô một dòng, thanh cuộn trên **1.695 = 1.695**.
Ảnh: `anh-mockup/33d-menu-xep-lai.png` · `33d-man-kho-du-lieu-toan-he-thong.png`.

**🔴 2 tồn mới của vòng 4:**

1. **Popup *"Xem hàng hoá Công ty khác"*** (nút ở màn *Hàng hoá nhập thông tin*) nay **trùng việc**
   với màn *Kho dữ liệu hàng hoá* — cùng là lối lấy hàng công ty khác về. Giữ cả hai hay gỡ popup?
2. Hàm `moTinhGia()` **không còn lối gọi** sau khi bỏ màn *Chờ tính giá* (nút *Tính giá* nằm ở màn
   đó). Xác nhận luồng tính giá từ nay **chỉ đi qua** Yêu cầu tính giá → Phiếu tính giá.

#### 33m. Đáp án 2 tồn của vòng 4 (user chốt 29/09/2026)

| Tồn | Đáp án | Đã làm |
|---|---|---|
| Popup *"Xem hàng hoá Công ty khác"* trùng việc với màn *Kho dữ liệu hàng hoá* | **GIỮ CẢ HAI** | Để nguyên nút *Xem hàng hoá Công ty khác* ở màn *Hàng hoá nhập thông tin*; hai lối cùng dẫn tới một việc (lấy hàng công ty khác về, trạng thái **Đang nhập thông tin**) |
| `moTinhGia()` mất lối gọi sau khi bỏ màn *Chờ tính giá* | **Chuyển sang màn Kho hàng hoá Công ty** | Cột *Hành động* của màn Kho hiện nút **Tính giá** — **chỉ ở 2 trạng thái đi tiếp được** (*Chờ tính giá bán* · *Đang tính giá*), các trạng thái khác **ẩn hẳn** nút (quy ước "nút không dùng được thì ẩn, không disable") |

**Đo:** 5/20 dòng trang đầu có nút *Tính giá*, đúng 2 trạng thái *Chờ tính giá bán* / *Đang tính
giá*; dòng *Đang kinh doanh* và *Đang nhập thông tin* **không có** nút. Nút và menu ⋮ nằm **cùng
hàng, cách 12px** (đúng quy ước cụm nút), ô Hành động nới **110 → 170px** cho màn Kho. Bấm *Tính
giá* mở đúng **form Phiếu tính giá** (`sc-ptf`), menu trái sáng ở *Phiếu tính giá*. Popup *Xem hàng
hoá Công ty khác* vẫn mở được bình thường. Console 0 lỗi.
Ảnh: `anh-mockup/33e-kho-cong-ty-nut-tinh-gia.png`.

#### 33n. VÒNG 5 — 4 việc (user chốt 29/09/2026)

| # | Việc | Đã làm |
|---|---|---|
| 1 | **Bỏ badge số** trên menu | Gỡ 7 ô `.cnt`; hàm `veDem()` giữ lại nhưng đổi sang `datDem(id, v)` **guard null** — gán `textContent` vào ô không còn tồn tại là nổ `TypeError` và chết cả lượt vẽ màn |
| 2 | Đổi tên menu *Kho hàng hoá Công ty* | → **Dữ liệu hàng hoá công ty** (đổi cả tiêu đề lưới, tiêu đề bộ lọc và dòng nhắc ở màn *Hàng đang kinh doanh*) |
| 3 | Bổ sung **định nghĩa + mục đích từng màn** vào màn *Ghi chú* | Bảng mục lục đặt ở **đầu** màn Ghi chú: **8 mục menu** + **5 màn/popup mở ra từ các mục đó**, mỗi dòng 4 cột *Màn hình · Là gì · Dùng để làm gì · Dữ liệu lấy vào* |
| 4 | **Bỏ ô lọc Đơn vị tính** ở các màn | Gỡ khỏi `LOC_CHUNG` (ăn sang 4 màn danh sách), khỏi bộ lọc popup *Xem hàng hoá Công ty khác* và popup *Xây dựng catalog*; `dsCat()` bỏ luôn nhánh so khớp `unit`. **Cột** ĐVT trong bảng vẫn giữ — chỉ bỏ ô lọc |

**Đo:** menu **0 badge**, 8 mục đúng tên mới · bảng mục lục **8 dòng** + 5 dòng phụ, 4 cột ·
quét `#adv-l1 · #adv-l3 · #adv-kho · #adv-tong · #adv-pp · #adv-cat` → **không còn ô nào** tên
*Đơn vị tính* · tiêu đề màn = *Dữ liệu hàng hoá công ty*. Console 0 lỗi.
Ảnh: `anh-mockup/33f-muc-luc-man-hinh.png`.

#### 33o. VÒNG 6 — YÊU CẦU TÍNH GIÁ GOM NHÓM THEO THƯƠNG HIỆU – HÃNG SX (user chốt 29/09/2026)

> Nguyên văn: *"Bỏ thương hiệu, hãng sx ⇒ thay đổi này cho phép user yêu cầu 1 lần được nhiều
> thương hiệu/hãng sx · User tự chọn hàng hoá vào ⇒ phần mềm tự động gom vào các nhóm theo Thương
> hiệu - Hãng sx (cấp dòng cha - con) · Ở row cha thể hiện Thương hiệu - hãng sx: hiển thị sẵn
> thông tin nhân viên phụ trách sẽ tiếp nhận yêu cầu"*.

| # | Việc | Đã làm |
|---|---|---|
| 1 | **Bỏ 2 ô Thương hiệu / Hãng sản xuất** | 2 ô này nằm ở khối *Thông tin chung* của **form Phiếu tính giá** (ghép chuỗi `A · B · C`, chỉ để đọc) — đã gỡ. Một yêu cầu nay gồm nhiều thương hiệu nên ô gộp không còn nghĩa; thông tin chuyển xuống **dòng cha** của bảng hàng hoá |
| 2 | **Tự gom nhóm cha – con** | Bảng *Hàng hoá đề nghị tính giá* ở form Yêu cầu tính giá: user cứ tick hàng hoá bất kỳ, hàm `gomTheoHang()` tự xếp thành **dòng CHA = `Thương hiệu — Hãng sản xuất`** + badge số mã, **dòng CON = từng mã hàng** (thụt lề 26px) |
| 3 | **Dòng cha hiện người tiếp nhận** | `Tiếp nhận: Phạm Quốc Dũng - HN_KT1 - 11010233` — đúng khuôn hiển thị nhân viên toàn hệ thống **`Tên - Mã phòng - Mã nhân viên`** (`utils/employeeOptionText.js`), lấy từ bảng phân công `PHU_TRACH` theo thương hiệu |

**Tick cha ↔ con:** tick dòng cha là tick cả nhóm; bỏ tick **một** con thì ô cha tự bỏ tick (không
dùng ô nửa vời); ô tick ở tiêu đề bảng tick tất cả. Dòng tổng kết đổi thành *"Đã chọn **N** mã hàng
hoá thuộc **M** nhóm thương hiệu — mỗi nhóm sẽ do người tiếp nhận tương ứng lập phiếu tính giá"*.

**Đo:** 33 hàng *Đang nhập thông tin* gom thành **4 nhóm** (Launch 16 · Bosch 15 · Fusheng 1 ·
Muller 1) · tick cha → **16/16** con được tick · bỏ 1 con → ô cha **tự bỏ tick**, số còn 15 ·
chọn 2 mã khác thương hiệu rồi gửi ⇒ **một** yêu cầu `YCTG-00313` gồm **Launch + Bosch** ·
form Phiếu tính giá còn 7 nhãn, **không còn** *Thương hiệu* / *Hãng sản xuất*. Console 0 lỗi.
Ảnh: `anh-mockup/33g-yeu-cau-tinh-gia-gom-nhom.png`.

**🔴 Tồn mới (quan trọng, phải chốt trước khi code):** một yêu cầu nay có **nhiều nhóm, mỗi nhóm
một người tiếp nhận** — vậy khi lập phiếu tính giá thì **tách thành nhiều phiếu theo nhóm** (mỗi
người tiếp nhận lập phiếu của nhóm mình, yêu cầu chỉ xong khi đủ các nhóm) hay vẫn **một phiếu
chung** cho cả yêu cầu? Demo hiện vẫn đang là **một phiếu chung**. Kéo theo: trạng thái của yêu cầu
tính theo từng nhóm hay theo cả phiếu; và người tiếp nhận có được sửa không.

#### 33p. VÒNG 7 — YÊU CẦU ↔ PHIẾU TÍNH GIÁ LÀ QUAN HỆ **1 – n** (user chốt 29/09/2026)

> Nguyên văn: *"Mỗi group trên yêu cầu sẽ có button để người phụ trách tạo ra 1 phiếu tính giá
> riêng theo Thương hiệu - Hãng sx đó · Quan hệ giữa Yêu cầu - Phiếu tính giá giờ sẽ là 1-n"*.
> Đây cũng là **đáp án cho tồn mở ở §33o**.

**Màn danh sách Yêu cầu tính giá** — thêm cột **Nhóm / Phiếu tính giá** và bung được nhóm:

- Dòng yêu cầu hiện `2/4 nhóm đã duyệt giá`, bấm số phiếu hoặc nút **Xem nhóm** để bung.
- Mỗi **dòng nhóm** có: `Thương hiệu — Hãng sản xuất` + số mã · **Người phụ trách**
  (`Tên - Mã phòng - Mã nhân viên`) · **số phiếu** của nhóm (hoặc *chưa có phiếu*) ·
  **trạng thái riêng của nhóm** (*Chờ lập phiếu* → *Đang tạo* → *Đã duyệt*) ·
  nút **Lập phiếu tính giá** khi chưa có phiếu, **Tính giá tiếp / Xem phiếu** khi đã có.
- Nút *Lập phiếu tính giá* ở **cấp yêu cầu đã bỏ** — lập phiếu nay luôn đi từ một nhóm cụ thể.

**Phiếu tính giá** mang thêm `brand`: form chỉ nạp hàng hoá **của đúng nhóm**, người lập mặc định
là **người phụ trách nhóm**, màn danh sách phiếu thêm cột **Thương hiệu – Hãng sản xuất**.

**Trạng thái yêu cầu** không còn đóng theo phiếu đầu tiên: `luuPT(duyet)` chỉ chuyển yêu cầu sang
*Đã tính giá* khi **số nhóm đã duyệt = tổng số nhóm** (`soNhomXong(y) === nhomCuaYC(y).length`).

**Đo:** lập một yêu cầu gồm 2 nhóm (Launch + Bosch) → bung ra đúng **2 dòng nhóm**, mỗi dòng một
nút *Lập phiếu tính giá* · lập phiếu nhóm Launch ⇒ phiếu `PTG-03180` **chỉ 1 mã hàng, brand
Launch**, người lập **Phạm Quốc Dũng**; duyệt xong yêu cầu vẫn *Chờ tính giá* (**1/2**) · lập tiếp
phiếu nhóm Bosch ⇒ `PTG-03181`, người lập **Lê Minh Cường**; duyệt xong yêu cầu mới thành
**Đã tính giá** (**2/2**) · một yêu cầu `YCTG-00313` nay có **2 phiếu**. Console 0 lỗi.
Ảnh: `anh-mockup/33h-yeu-cau-1-n-phieu.png`.

🐞 **Lỗi tự bắt được:** 3 class `.nhom-ten` / `.nhom-dem` / `.nhom-nv` ban đầu khai **lồng trong
`tr.nhom-cha`** (dòng cha của form Yêu cầu). Màn danh sách dùng class `nhom-con` cho dòng nhóm nên
**mất sạch style** — badge dính liền tên hãng: *"Launch Trung Quốc1 mã hàng"*. Số liệu DOM vẫn
đúng, chỉ nhìn ảnh mới thấy. Đã tách 3 class ra khỏi vòng `tr.nhom-cha`; đo lại: tên cách badge
**10px**, badge có nền trắng viền.

**Kéo theo — cần chốt khi code:** ai được bấm *Lập phiếu tính giá* của một nhóm (chỉ đúng người phụ
trách, hay ai có quyền tính giá cũng được) · bảng phân công **thương hiệu → người phụ trách** lưu ở
đâu (bảng mới hay cột trên `manufactures`) · huỷ/ sửa người phụ trách thì phiếu đã lập xử lý sao.

#### 33q. VÒNG 8 — PHÂN CÔNG PHỤ TRÁCH HÃNG SẢN XUẤT (user chốt 29/09/2026)

Đáp án 3 việc kéo theo của §33p:

| Việc | Đáp án | Đã làm |
|---|---|---|
| Ai được lập phiếu của một nhóm | **Đúng người phụ trách được phân công**, và **có chức năng phân công** | Nút *Lập phiếu tính giá* **gate theo phân công**: không phải người phụ trách thì **ẩn hẳn** nút, thay bằng dòng xám *"Chờ Vũ Thị Hà lập phiếu"*; hãng chưa phân công thì *"Chưa phân công người phụ trách"* |
| Bảng lưu phân công | **`assign_employee_manufactures`** | Mockup mô phỏng bằng mảng `PHAN_CONG` = cặp (nhân viên × hãng sản xuất) |
| Đổi người phụ trách thì phiếu cũ sao | **Đã có chức năng Bàn giao công việc** | Không làm luồng riêng ở đây; ghi rõ trong tài liệu là đi theo bàn giao công việc sẵn có |

**Màn mới "Phân công phụ trách hãng SX"** (menu đặt ngay sau *Ghi chú*, cụm cấu hình):
bảng **Thương hiệu · Hãng sản xuất · Mã hãng · Người phụ trách (select) · Số mã hàng**, nút **Lưu**.
Dòng của chính mình gắn nhãn **"bạn phụ trách"**. Ô chọn nhân viên hiển thị đúng khuôn
`Tên - Mã phòng - Mã nhân viên`.

**Đo:** 5 hãng — Launch + Fusheng của *Nguyễn Văn An* (người đang đăng nhập), Bosch *Lê Minh Cường*,
Muller *Vũ Thị Hà*, Donaldson **chưa phân công** · ở màn Yêu cầu: nhóm Fusheng/Launch có nút
**Lập phiếu tính giá**, nhóm Muller chỉ có chữ xám **"Chờ Vũ Thị Hà lập phiếu"** · giao Muller cho
mình ở màn phân công rồi Lưu ⇒ nút **hiện ngay**; trả lại Vũ Thị Hà ⇒ nút **biến mất**.
Console 0 lỗi. Ảnh: `anh-mockup/33i-phan-cong-hang-sx.png`.

**Ghi cho lúc code:** bảng `assign_employee_manufactures` cần **UNIQUE (employee_id, manufacture_id)**
và kiểm **một hãng chỉ một người phụ trách đang hiệu lực** (nếu không, hai người cùng lập phiếu cho
một nhóm). Gate phải nằm ở **BE** (`checkPermission` + kiểm người phụ trách), FE chỉ ẩn nút.

#### 33r. VÒNG 9 — CẤU TRÚC PHIẾU YÊU CẦU TÍNH GIÁ (user chốt 29/09/2026)

| # | Việc | Đã làm |
|---|---|---|
| 1 | Thêm cột **STT** | Cột STT đứng ngay sau ô tick của bảng *Hàng hoá đề nghị tính giá* |
| 2 | Dòng cha đánh **số La Mã** | `I · II · III · IV` (hàm `laMa()`) |
| 3 | Dòng con đánh **1-2-3** | Đánh **lại từ 1 trong từng nhóm** → đọc thành `I.1 · I.2 … II.1 …` |
| 4 | Demo **3-4 nhóm, số hàng đều hơn** | Trước: 2 nhóm ôm hết (Launch 16 · Bosch 15 · còn lại 1 mã). Nay **4 nhóm: 9 · 8 · 5 · 11** |
| 5 | Người tiếp nhận ở **Phòng XNK** | Cả 4 người tiếp nhận đều `HN_XNK`; **người đang đăng nhập cũng chuyển về Phòng Xuất nhập khẩu**, nếu không thì không nhóm nào có nút *Lập phiếu tính giá* và luồng demo tắc |
| 6 | **Bỏ màn Phân công** | Gỡ mục menu + section + 3 hàm; **giữ bảng dữ liệu `PHAN_CONG`** vì gate nút *Lập phiếu* vẫn đọc nó. Màn khai báo nằm sẵn trên HRM (`assign_employee_manufactures`) |

🐞 **Nguyên nhân dữ liệu demo bị dồn vào 2 nhóm** (đáng ghi lại): trong hàm sinh dữ liệu, **thương
hiệu và trạng thái cùng lấy theo `i % 10`** nên mỗi mẫu hàng luôn rơi đúng một trạng thái — màn
*Hàng hoá nhập thông tin* vì thế chỉ còn 2 thương hiệu. Sửa bằng cách cho trạng thái **lệch pha**:
`(i + Math.floor(i / 10)) % tt.length`. Bài học: sinh dữ liệu demo bằng nhiều phép `%` cùng chu kỳ
là tạo ra tương quan giả, nhìn bảng tưởng nghiệp vụ lệch.

**Đo:** menu còn **8 mục**, không còn *Phân công phụ trách hãng SX* · bảng yêu cầu: cột
`(tick) STT Mã hàng Tên hàng hoá Model Công ty quản lý Chính sách giá nội bộ`, chuỗi số
`[I] 1..9 [II] 1..8 [III] 1..5 [IV] 1..11` · người tiếp nhận: **chỉ một mã phòng `HN_XNK`** ·
gate vẫn đúng (*Chờ Đặng Thu Hương lập phiếu* / *Chờ Vũ Thị Hà lập phiếu*) · các màn khác không vỡ
(Kho 150 · Kho dữ liệu 153 · Nhập thông tin 33 · Đang kinh doanh 18). Console 0 lỗi.
Ảnh: `anh-mockup/33j-yeu-cau-stt-la-ma.png`.

#### 33s. VÒNG 10 — CHỌN HÀNG HOÁ VÀO PHIẾU BẰNG POPUP (user chốt 29/09/2026)

| # | Việc | Đã làm |
|---|---|---|
| 1 | Mỗi nhóm **3-4 mã** | Hàm sinh dữ liệu bỏ `nhap` khỏi vòng xoay trạng thái, thay bằng **rót đúng 2 mã/thương hiệu**; cộng với hàng viết tay sẵn ⇒ **13 mã, 4 nhóm: 4 · 3 · 3 · 3** (trước là 9·8·5·11) |
| 2 | **Nút + popup chọn hàng hoá** | Khối *Hàng hoá đề nghị tính giá* có nút **Chọn hàng hoá**; bảng nay chỉ chứa hàng **đã chọn**, mỗi dòng có nút **xoá** (bỏ khỏi yêu cầu), rỗng thì nhắc bấm nút |

**Popup "Chọn hàng hoá vào yêu cầu tính giá"** (`mask-chh`):

- **Nguồn**: hàng *Đang nhập thông tin* của công ty đang đăng nhập **và chưa có trong yêu cầu đang
  lập** — chọn xong mở lại popup thì mã đó biến mất khỏi danh sách (đo: 13 → 9).
- Bộ lọc: tìm nhanh · **Thương hiệu** · **Công ty quản lý** · nút *Làm mới*.
- Bảng: tick nhiều dòng, bấm ô **Mã hàng / Tên hàng** cũng tick, ô tick tiêu đề tick **trang đang
  xem**, link **"Chọn tất cả N kết quả lọc"**, phân trang **20/50/100** đúng khuôn `V2BasePagination`.
- Footer: *"Sẽ thêm N mã hàng vào yêu cầu"* + **Chọn** / **Đóng**.

**Đo:** nguồn 13 mã · lọc *Thương hiệu = Bosch* còn **3**, bấm *Chọn tất cả 3* → *Đã chọn 3* ·
bỏ lọc, tick thêm 1 mã Launch ⇒ footer *"Sẽ thêm 4 mã hàng"* · bấm **Chọn** ⇒ popup đóng, bảng gom
thành **2 nhóm (Bosch 3 · Launch 1)**, dòng tổng kết *"Đã chọn 4 mã hàng hoá thuộc 2 nhóm thương
hiệu"* · mở lại popup còn **9** mã · bấm nút xoá một dòng ⇒ còn 3 dòng · Lưu & gửi ⇒ yêu cầu mới
đúng số mã, lập yêu cầu kế tiếp thì bảng **rỗng lại**. Console 0 lỗi.
Ảnh: `anh-mockup/33k-popup-chon-hang-hoa.png` · `33k-yeu-cau-sau-khi-chon.png`.

#### 33t. VÒNG 11 — CỘT "CÔNG TY ĐANG KINH DOANH" (user chốt 29/09/2026)

Màn **Kho dữ liệu hàng hoá** thêm cột **Công ty đang kinh doanh** (đứng ngay sau *Công ty quản lý*):
liệt kê mọi công ty đang có mã hàng đó ở trạng thái **Đang kinh doanh** — chip xanh lá, **2 công ty
đầu + chip `+N`** rê chuột xem hết. Ô rỗng để **trống hẳn** (quy ước "không điền dấu gạch").

Đây là cột phân biệt hai khái niệm dễ lẫn ở màn toàn hệ thống: **“hàng của ai”** (*Công ty quản lý*
— công ty tạo ra mã) và **“ai đang bán”** (*Công ty đang kinh doanh*). Cột chỉ có ở màn này
(`khong: ['pp','l1','l3','kho']`) — các màn khác đều đã nằm trong phạm vi một công ty.

**Dữ liệu demo bổ sung:** trước đó chỉ **1 mã** có 2 công ty cùng kinh doanh nên không thấy được
chip `+N`. Đã rót thêm: hàng *Đang kinh doanh* cứ `i % 4` thêm ETEK POWER, `i % 6` thêm TÂN PHÁT SG,
`i % 12` thêm ETEK GREEN ⇒ phân bố nay **58 mã 1 công ty · 21 mã 2 công ty · 7 mã 4 công ty**.

**Đo:** cột nằm đúng vị trí 15/16 · `TPE-CN-2T-4500 → TÂN PHÁT · TÂN PHÁT SG` ·
`TPE-LOD-036` (4 công ty) hiện `TÂN PHÁT · ETEK POWER` + chip **+2**, tooltip liệt kê
*ETEK GREEN · TÂN PHÁT SG* · hàng chưa ai kinh doanh thì ô **trống** ·
3 màn còn lại **không có** cột này · các lưới khác không vỡ. Console 0 lỗi.
Ảnh: `anh-mockup/33l-cot-cong-ty-dang-kinh-doanh.png`.

#### 33u. VÒNG 12 — PANEL CÂY 4 CẤP DỄ ĐỌC HƠN (user chốt 29/09/2026)

**Vấn đề:** bung cây ra thì rối mắt — cả 4 cấp **cùng cỡ chữ, cùng màu**, chỉ khác thụt lề; badge
đếm lại hiện ở **mọi cấp** nên mắt không bám được đang đứng ở đâu.

**User chọn phương án A** trong 3 phương án đưa ra (A: phân cấp bằng kiểu chữ + đường nối ·
B: đi sâu từng cấp + breadcrumb · C: 3 ô chọn lọc dây chuyền + danh sách cụm), **thêm số thứ tự**.

| Cấp | Trình bày |
|---|---|
| 1 · Lĩnh vực | Số **La Mã `I.`** + chữ **HOA** 11px/700, xám `#64748b`, **dính đầu khi cuộn** (`position: sticky`) |
| 2 · Chương | Số **`1.`** + chữ **đậm đen** 12.5px/600 `#0f172a` |
| 3 · Nhóm công việc | Số **`1.1`** + chữ **thường xám** 12px/400 `#64748b` |
| 4 · Cụm công việc | Số **`1.1.1`** màu teal đậm + tên đen — **cấp duy nhất bấm chọn được**, chọn thì nền teal nhạt |

- **Đường nối dọc 1px** `#e8eef4` mỗi cấp (thay cho thụt lề trần), các dòng nối nhau thành đường liền.
- **Badge đếm chỉ ở cấp 4**; cấp 1-3 chỉ hiện số **khi đang đóng** — mở ra rồi thì số nằm ngay ở các
  cụm bên dưới, hiện nữa là nhiễu.
- Mũi bung `▾/▸` đẩy sát **mép phải** (đo: cách mép 9px), badge cấp 4 cũng sát mép 9px.
- Số thứ tự đánh **theo từng nhánh**: mở lĩnh vực khác thì Chương lại đánh từ `1.`

**Đo:** `I. CÔNG NGHIỆP` → `1. Thiết bị khí nén` → `1.1 Lắp đặt hệ thống khí nén` →
`1.1.1 Cụm máy nén trục vít [31]` · cỡ/đậm/màu 4 cấp lần lượt **11/700/xám/UPPERCASE ·
12.5/600/đen · 12/400/xám · 12/400/đen** · cấp 1 `position: sticky` · cấp 2 đang đóng hiện badge
`[1]`, mở ra thì badge biến mất. Console 0 lỗi.
Ảnh: `anh-mockup/33m-cay-4-cap-phan-cap.png`.

#### 33v. VÒNG 13 — CHỌN CATALOG BẰNG 4 CỘT KIỂU ERP (user chốt 30/09/2026)

> Yêu cầu: *"tham khảo form tạo/sửa nhóm hàng hoá hiện tại của ERP ⇒ phần chọn Lĩnh vực / Chương /
> Nhóm / Cụm xem có áp dụng được không? hoặc đề xuất phương án tương tự giúp user chọn nhanh hơn"*.

**Khảo sát ERP** (`catalogs/groups/form.blade.php` + `Sale/GroupsController@update`):

- Giao diện: **4 cột song song**, mỗi cột một danh sách **checkbox cuộn 300px**; cột sau chỉ hiện
  mục thuộc các mục đã tick ở cột trước, kèm **tiêu đề in đậm** tên cha.
- Lưu: `$request->classify` là **danh sách nhánh** `{scope_id, chapter_id, job_group_id,
  job_cluster_id}` — **mỗi dòng một nhánh**, cấp 3-4 cho phép `null`.

⇒ **Áp dụng được**, vì mô hình dữ liệu **trùng đúng §33** (nhiều nhánh, mỗi nhánh một dòng); khác
duy nhất: HRM **bắt buộc đủ tới Cụm**, ERP cho dừng ở cấp 2.

**Đã dựng** (thay 4 ô select lọc dây chuyền của §30f):

| | |
|---|---|
| 4 cột | *Lĩnh vực Công ty kinh doanh · Chương · Nhóm công việc · Cụm công việc*, mỗi cột cao 216px cuộn riêng |
| Bổ sung so với ERP | **ô tìm trong từng cột** + **số đang chọn** ở đầu cột (ERP không có, thật sẽ là 8 lĩnh vực → 65 chương → 106 nhóm, cuộn mỏi) |
| Bổ sung so với ERP | **bảng "nhánh đã gắn"** ngay dưới 4 cột (STT La Mã + nút gỡ) — đọc được kết quả mà không phải nhìn chéo 4 cột |
| Ý nghĩa tick | 3 cột đầu chỉ **mở đường**; tick ở cột **Cụm công việc** mới là **gắn nhánh** thật |
| Bỏ tick cấp trên | **gỡ luôn các nhánh thuộc nó** + toast báo số nhánh bị gỡ — không im lặng xoá dữ liệu người dùng |
| Mở hàng hoá có sẵn nhánh | `qtNapTuNhanh()` tick sẵn 3 cấp trên để 4 cột hiện đúng đường đã đi |
| Validate | chưa có nhánh thì **tô viền đỏ cả cột Cụm** (không còn ô select để tô), chấm đỏ tab cha, chặn Lưu |

**Đo:** mở `TPE-CN-2T-4500` (2 nhánh) → 4 cột tick sẵn đúng 2·2·2·2, cột 2 có 2 tiêu đề cha
*Dịch vụ ô tô · Công nghiệp* · tick thêm *Cụm thiết bị rửa xe* ⇒ nhánh 2 → **3**, số đầu cột 4 lên
**3** · gõ "môi" ở ô tìm cột 1 còn đúng **Môi trường** · bỏ tick chương *Thiết bị gara* ⇒ nhánh
3 → **1** kèm toast *"Đã gỡ 2 nhánh thuộc mục vừa bỏ tick"* · hàng chưa có nhánh bấm Lưu ⇒ **chặn**,
cột Cụm viền đỏ, tab cha chấm đỏ. Console 0 lỗi.
Ảnh: `anh-mockup/33n-chon-catalog-4-cot.png`.

🐞 **2 lỗi tự bắt được:**
1. Đợt thay khối đã **nuốt mất 2 hàm dùng chung** `cumKey()` / `duongNhanh()` (chúng nằm cùng khối
   với 4 ô select cũ) ⇒ `oCot` nổ `duongNhanh is not defined` **ngay lúc vẽ màn**, cả trang trắng.
   Khai lại ở đầu khối mới.
2. Lần đo đầu tưởng code hỏng vì trình duyệt trả **bản cũ trong cache** — đúng bẫy đã ghi ở
   `playwright-mcp-cache-lock-gotcha`: kiểm demo phải **đổi sang cổng MỚI**, không dùng lại cổng cũ.

#### 33w. ĐỔI TÊN 2 CẤP CATALOG (user chốt 30/09/2026)

| Tên cũ | Tên mới | Bảng dữ liệu (giữ nguyên) |
|---|---|---|
| **Nhóm công việc** | **Mục** | `job_groups` |
| **Cụm công việc** | **Tiểu mục** | `job_clusters` |

Cây catalog nay đọc là: **Lĩnh vực Công ty kinh doanh → Chương → Mục → Tiểu mục**.
Áp cho **toàn bộ giao diện**: nhãn 4 cột chọn catalog · tiêu đề cột bảng nhánh · 4 ô lọc ở màn
*Kho hàng hoá công ty* và *Hàng đang kinh doanh* · popup Xây dựng catalog (mô tả, 2 tab, nút, dải
"Đang xem tiểu mục", câu rỗng) · nút *Xếp vào tiểu mục…* ở lưới · bảng mục lục màn Ghi chú · mọi
toast và câu lỗi. **Tên bảng và tên trường CSDL giữ nguyên** (`job_groups` / `job_clusters`) —
đây chỉ là đổi chữ hiển thị.

**Dữ liệu demo cũng bỏ tiền tố "Cụm "** cho khớp tên cấp mới: *Cụm máy nén trục vít* →
**Máy nén trục vít**, *Cụm thiết bị lốp* → **Thiết bị lốp**… (nếu tên thật sau này vẫn muốn kèm
chữ "Cụm" thì chỉ là dữ liệu người dùng tự khai, không ảnh hưởng nhãn).

**Đo sau khi đổi:** quét `document.body.innerText` toàn trang → **0** lần xuất hiện *"Nhóm công
việc"* và *"Cụm công việc"* · 4 cột trong form = `Lĩnh vực Công ty kinh doanh · Chương · Mục ·
Tiểu mục` · ô lọc màn Kho khoá hiện `Mục — chọn cấp trên trước` / `Tiểu mục — chọn cấp trên trước` ·
2 tab popup = *Hàng trong tiểu mục* / *Thêm hàng vào tiểu mục* · bảng mục lục không còn chữ cũ.
Console 0 lỗi. Ảnh: `anh-mockup/33o-doi-ten-muc-tieu-muc.png`.

⚠️ 2 chỗ **cố ý giữ chữ "cụm"** vì nghĩa khác hẳn: ghi chú *"nút cùng cụm cách nhau 12px"* và
*"cụm nút"* trong quy ước bố cục nút.

---

## 34. ✅ CHỐT MOCKUP (user chốt 30/09/2026)

Kết thúc giai đoạn mockup của Phase 2. Từ đây **không sửa giao diện nữa**; muốn đổi thì mở vòng mới
và ghi rõ, để bản chốt này là mốc đối chiếu khi code.

### 34a. Những gì đã chốt

**`mockup-luong-xay-dung-hang-hoa.html`** — 448 KB, **11 màn + 13 popup**:

| Mục menu | Màn | Chốt ở |
|---|---|---|
| Ghi chú & sơ đồ luồng | `sc-flow` — mục lục 8 mục menu + 5 màn/popup, 3 bước quy trình, bảng trạng thái theo công ty, 4 chỗ demo khác bản thật | §33n |
| Chính sách giá bán nội bộ | `sc-cf` — lưới hãng × công ty mua, 2 tỷ lệ, popup chọn hãng | §28 |
| Kho dữ liệu hàng hoá | `sc-tong` — toàn bộ hàng mọi công ty, **Lấy về** từng dòng + hàng loạt, cột *Công ty đang kinh doanh* | §33l · §33t |
| Dữ liệu hàng hoá công ty | `sc-kho` — hàng của công ty, 4 ô lọc catalog, **Xây dựng catalog**, **Tính giá** | §33c · §33j · §33m |
| Hàng hoá nhập thông tin | `sc-l1` — bước 1, lấy hàng công ty khác, lập yêu cầu tính giá | §26 |
| Hàng đang kinh doanh | `sc-l3` — đang kinh doanh **và** đã xếp catalog, dòng nhắc số hàng chưa xếp | §33e |
| Yêu cầu tính giá | `sc-yc` + `sc-ycf` — gom nhóm **Thương hiệu – Hãng SX**, STT La Mã, người tiếp nhận Phòng XNK, popup chọn hàng hoá | §33o · §33r · §33s |
| Phiếu tính giá | `sc-pt` + `sc-ptf` — 3 tab, quan hệ **1 – n** theo nhóm hãng | §29 · §33p |
| *(mở từ mã hàng)* | `sc-form` — 2 tầng tab, tab *Quản trị hàng hoá* chọn catalog bằng **4 cột kiểu ERP** | §30g · §31 · §32 · §33v |

13 popup: Xây dựng catalog · Chọn hàng hoá vào yêu cầu · Xem hàng hoá Công ty khác · Cấu hình cột ·
Chọn hãng sản xuất · Import Excel · Chọn yêu cầu tính giá · Tạm tính giá mua · Xem trước giá mua lại ·
Lịch sử · Xác nhận xoá · 2 popup cảnh báo chưa lưu.

**`mockup-bao-cao-hang-hoa.html`** — 69 KB, báo cáo hàng hoá theo công ty (§27), console 0 lỗi.

### 34b. Nghiệm thu bản chốt (đo trên trình duyệt, 30/09/2026)

| Kiểm | Kết quả |
|---|---|
| 8 mục menu mở được, đúng thứ tự user chốt | ✅ |
| Số dòng từng màn | Kho dữ liệu **153** · Kho công ty **150** · Nhập thông tin **13** · Đang kinh doanh **32** · Yêu cầu **4** · Phiếu **2** · Chính sách **5 hãng / 30 dòng** |
| Form hàng hoá | 2 tab cha, 5 tab con, tab Quản trị có **4 cột** chọn catalog |
| Form yêu cầu / phiếu | bảng gom nhóm dựng được · phiếu đủ **3 tab** *Hàng hoá · Chi phí · Tính giá* |
| 5 popup chính mở/đóng được | ✅ Xây dựng catalog · Chọn hàng hoá · Hàng hoá Công ty khác · Cấu hình cột · Chọn hãng |
| Tên 2 cấp mới | **0** chỗ còn *"Nhóm công việc"* / *"Cụm công việc"* trong cả 3 file HTML |
| Console | **0 lỗi** ở cả 2 mockup |

### 34c. Việc còn lại trước khi code

1. **Cổng chặn 24 câu tồn** — đã gom sẵn thành 5 nhóm (A CSDL 9 · B quyền 3 · C luồng chứng từ 7 ·
   D hiệu năng/Excel 2 · E dọn việc đã lỡ làm 2), mỗi câu kèm đề xuất. **Chưa chốt.**
2. **`mockup-hang-hoa.html` (3,2 MB) đã lỗi thời** — dựng 21/09 trước khi gỡ tab *Giá bán* (§29g),
   trước form 2 tầng tab (§30g) và trước toàn bộ §33. Cần user quyết **xoá hay giữ để tra cứu**;
   để nguyên thì người xem dễ mở nhầm bản cũ.

---

## 35. CHỐT TỒN TRƯỚC KHI CODE (bắt đầu 30/09/2026)

Danh sách đầy đủ + cột chốt: `ton-chot-truoc-code.md` / `ton-chot-truoc-code.xlsx` (cùng nội dung).
Chốt lần lượt từng nhóm; nhóm nào xong ghi vào đây.

### 35a. Nhóm A — CSDL: ✅ user đồng ý toàn bộ đề xuất (30/09/2026)

| # | Chốt |
|---|---|
| A1 | Trạng thái theo (hàng × công ty) lưu ở **`product_company_coefficients`**: + cột `status`, **UNIQUE(product_id, company_id)** — bảng chủ của quan hệ hàng × công ty |
| A2 | Lấy hàng công ty khác về = **THAM CHIẾU** (cùng `products.id`), chỉ sinh dòng mới ở bảng A1 |
| A3 | 45.890 hàng cũ: sinh 1 dòng A1 cho **công ty tạo** (`products.company_id`) — đang hoạt động ⇒ **Đang kinh doanh**, đã ngừng ⇒ không sinh dòng; 5 hàng mồ côi xử lý tay |
| A4 | **Hướng B** cho cả giá lẫn dữ liệu quản trị: `company_id` NOT NULL, dữ liệu cũ gán về công ty tạo. 2 bước: thêm cột + gán ngay → **xoá cột chung / ép NOT NULL sau cùng**, khi đã rà ERP. Công ty lấy hàng về **tự tính giá của mình** (không có "giá chung") |
| A5 | **Tách giá vốn / giá mua ngoài** khỏi `product_units` ⇒ bảng `product_company_units`, sửa 34 file ERP |
| A6 | Bảng nối catalog **`product_business_catalogs`** (`product_id`, `company_id`, `job_cluster_id`) + UNIQUE 3 cột; **chỉ lưu Tiểu mục**, 3 cấp trên join ngược |
| A7 | Mỗi Tiểu mục thuộc **đúng 1 Mục** (`job_clusters.job_group_id` NOT NULL) |
| A8 | Màn *Hàng đang kinh doanh* bật điều kiện catalog **ngay** + dòng nhắc cam; **popup tìm hàng dùng chung chỉ xét trạng thái, KHÔNG xét catalog** |

### 35b. Nhóm B — Quyền: ✅ chốt xong (04/10/2026)

🔑 **NGUYÊN TẮC (user chốt 04/10/2026):** *"Không bảo mật thông tin hàng hoá và giá bán, chỉ kiểm soát
ai được thao tác dữ liệu, ai được xem giá vốn."* ⇒ quyền chỉ gate **thao tác ghi** + **giá vốn**;
mọi màn/endpoint ĐỌC thông tin hàng hoá và giá bán mở cho mọi người đăng nhập. Ngoại lệ §23c
("chỉ thấy công ty mình") nay chỉ còn áp cho việc GHI.

Thay toàn bộ đề xuất B1/B2/B3 cũ. Nguyên văn user chốt:

| Quyền | Cho phép |
|---|---|
| **Xây dựng thông tin hàng hoá** | Tạo / sửa thông tin hàng hoá + dữ liệu quản trị **của công ty mình**; vào màn *Hàng hoá nhập thông tin* và *Dữ liệu hàng hoá công ty*. **Chỉ quyền này** dùng được chức năng **lấy hàng hoá về công ty** |
| **Xem dữ liệu hàng hoá công ty** | Vào màn *Dữ liệu hàng hoá công ty*, xem chi tiết các mã hàng |
| **Xuất excel danh sách hàng hoá** | MỌI nút xuất Excel danh sách hàng hoá ở các màn trong luồng này dùng chung quyền này |
| **Xây dựng catalog kinh doanh** | Dùng chức năng xây dựng catalog hàng hoá |
| **Cấu hình chính sách giá bán nội bộ** | Vào **và** cập nhật màn *Chính sách giá bán nội bộ* |
| *(không cần quyền)* | Vào xem màn **Kho dữ liệu hàng hoá** và **Hàng hoá đang kinh doanh**; các nút thao tác trong 2 màn này check theo quyền của từng nút |

Hệ quả cần nhớ khi code:
- *Kho dữ liệu hàng hoá* hiện hàng **mọi công ty** cho mọi người đăng nhập ⇒ là ngoại lệ có chủ đích
  của §23c (chỉ thấy công ty mình). Gate giá vốn (`Quản lý giá`) vẫn giữ ở BE.
- Nút *Lấy về* (từng dòng + hàng loạt) ở *Kho dữ liệu hàng hoá* và popup *Xem hàng hoá Công ty khác*:
  gate bằng **Xây dựng thông tin hàng hoá** cả FE lẫn BE.
- Màn *Dữ liệu hàng hoá công ty* vào được khi có **Xây dựng thông tin** HOẶC **Xem dữ liệu**.
- 4 quyền 1616–1619 trên nhánh `feat/p1-danh-muc-hang-hoa` bỏ, thay bằng 1652–1656 (chỗ hở 5).
- Super admin không có ngoại lệ — xét đúng quyền được gán.

Chỗ hở đã hỏi lần lượt:
1. ✅ Báo cáo hàng hoá theo công ty (§27) — **không cần quyền** (04/10), như *Kho dữ liệu* và *Hàng đang kinh doanh*; nút Xuất Excel trong báo cáo vẫn theo quyền *Xuất excel danh sách hàng hoá*
2. ⏸ Yêu cầu tính giá / Phiếu tính giá — **gác, chốt khi mở luồng Tính giá (2-tg)** (04/10). Hệ quả: đợt code đầu KHÔNG làm 2 màn này, kèm các nút dẫn vào luồng (*Lập yêu cầu tính giá* ở màn Nhập thông tin, *Tính giá* ở màn Dữ liệu công ty)
3. ✅ Không có quyền *Xem dữ liệu*: bấm mã ở 3 màn không cần quyền **mở được chi tiết, CHỈ ĐỌC** (khoá mọi ô, không nút lưu) (04/10). Giá vốn vẫn ẩn theo `Quản lý giá` ở BE. ⇒ endpoint chi tiết KHÔNG gate quyền xem, chỉ gate các endpoint ghi
4. ✅ **Có xoá, chỉ hàng chưa dùng**, theo quyền **Xây dựng thông tin hàng hoá** (không thêm quyền) (04/10): xoá được khi hàng ở *Đang nhập thông tin*, do công ty mình tạo, chưa công ty nào lấy về, chưa phát sinh chứng từ. Hàng công ty khác đã lấy về thì *xoá* = gỡ dòng của công ty mình ở `product_company_coefficients`, không đụng `products`
5. ✅ **Bỏ 4 quyền cũ 1616–1619, cấp 5 id mới 1652–1656** (04/10):
   1652 *Xây dựng thông tin hàng hoá* · 1653 *Xem dữ liệu hàng hoá công ty* · 1654 *Xuất excel danh sách
   hàng hoá* · 1655 *Xây dựng catalog kinh doanh* · 1656 *Cấu hình chính sách giá bán nội bộ*.
   Lý do: trên `gop_db` id **1615–1619 đã thuộc "Công nợ đầu kỳ"** (commit `131531f2f`, 01/10, dùng ở
   `Finance/DeclareDebt*`) — giữ 1616–1619 thì vai trò đang có quyền hàng hoá **lặng lẽ thành quyền công
   nợ** sau khi chạy seeder (file phẳng, git không báo xung đột). Hiện trạng lúc chốt: 4 quyền cũ chỉ
   dùng ở 15 route `/products` (`Modules/MasterData/Routes/api.php`), FE 0 chỗ; DB local `hrm_erp` có 4
   dòng, mỗi quyền gán 1 vai trò. Khi code: sửa route + seeder trên nhánh, tên vẫn tránh trùng-bỏ-dấu
   với quyền ERP guard `web`, chạy `uniq -d` id sau mỗi merge. Kiểm lại 1652+ còn trống ngay trước khi
   seed.

**Nhóm B ✅ chốt xong 04/10/2026.**

---

### 35c. Nhóm C — Luồng chứng từ (04/10/2026)

⏸ User chốt: **phần TÍNH GIÁ làm ở phase sau, Phase 2 chỉ làm phần Hàng hoá** ⇒ C1, C3, C4 gác tới 2-tg.

| # | Chốt |
|---|---|
| C2 | Hàng *Đang kinh doanh* bị sửa thông tin (chung hoặc quản trị) **KHÔNG lùi trạng thái** |
| C5 | 🔄 **ĐẢO A8 / §33e:** màn *Hàng đang kinh doanh* **KHÔNG bắt buộc catalog** nữa — user: *"khi update lên sẽ có rất nhiều data chưa kịp cập nhật catalog"*. Màn chỉ lọc theo trạng thái *Đang kinh doanh*. Câu C5 gốc (gỡ nhánh cuối) **không còn**: gỡ catalog không làm hàng rời màn nào |
| C5-a | Form, tab *Quản trị hàng hoá*: **GIỮ bắt buộc ≥ 1 nhánh catalog như §33f** (cả tạo lẫn sửa) — hàng cũ chưa có catalog muốn lưu tab này thì phải xếp catalog trước. Màn danh sách không bắt buộc, form thì bắt buộc |
| C5-b | Màn *Hàng đang kinh doanh*: **giữ dòng nhắc cam, đổi câu** thành *"Có N hàng hoá đang kinh doanh chưa xếp catalog"* kèm **link bấm vào là lọc ra các hàng đó** + bộ lọc catalog có thêm lựa chọn **"Chưa xếp catalog"** (link chính là bật lựa chọn này). Cột Catalog để trống với hàng chưa xếp |

| C6, C7 | ⏸ Gác — màn **Chính sách giá bán nội bộ (§28) chuyển sang phase Tính giá** (04/10). Phase 2 không có cảnh báo "hãng chưa cấu hình" lúc lấy hàng về; quyền 1656 *Cấu hình chính sách giá bán nội bộ* vẫn giữ id nhưng seed cùng phase đó |

**Nhóm C ✅ xong 04/10/2026.**

✅ **Mockup đã sửa theo C5/C5-b (04/10/2026)** — `sc-l3`: bỏ điều kiện catalog; công tắc **"Chỉ hàng chưa
xếp catalog"** cạnh ô tìm (cùng khuôn màn Kho; bật thì bỏ qua 4 ô lọc catalog); dòng nhắc cam *"Có N hàng hoá
đang kinh doanh chưa xếp catalog — lọc ra các hàng này"*, đang lọc thì link đổi thành *"xem tất cả hàng
đang kinh doanh"*; nút *Làm mới* xoá cả công tắc. Ô Catalog của hàng chưa xếp hiện nhãn **"Chưa xếp catalog"**
(dùng chung bộ vẽ cột với màn Kho) thay vì để trống. Bảng sơ đồ luồng sửa mô tả màn.
Đo (cổng 8933): mặc định *1–20 / 81* · bấm link *1–20 / 49*, công tắc tự bật, 20/20 ô Catalog = "Chưa xếp
catalog" · bấm lại về 81 · lọc lĩnh vực *Công nghiệp* 32 · Làm mới về 81; console 0 lỗi.
Ảnh `anh-mockup/35c-hang-dang-kd-loc-chua-xep.png`.

---

### 35d. Nhóm D — Excel / hiển thị (04/10/2026)

| # | Chốt |
|---|---|
| D1-a | Excel danh sách hàng hoá: cột Catalog **chỉ ghi cấp 4 — Tiểu mục** (không ghi đường 4 cấp); hàng nhiều nhánh ⇒ nhiều Tiểu mục trong 1 ô, mỗi cái 1 dòng. (User gọi là "cấp 4 Loại hàng hoá" — đã xác nhận là Tiểu mục, KHÔNG đổi tên hiển thị) |
| D1-b, D2 | ⏳ Chờ — 2 câu đều về ma trận **Báo cáo hàng hoá theo công ty**. User phát hiện mockup luồng **không có báo cáo này** (nằm ở file riêng `mockup-bao-cao-hang-hoa.html`, không nối vào menu mockup chính dù §34a ghi "đã chốt"). User mở file xem rồi mới quyết có làm trong Phase 2 không |

---

### 35e. Nhóm E — việc đã lỡ làm vào source (04/10/2026)

| # | Chốt |
|---|---|
| E1 | 10 commit Phase 2 trên `hrm-api` + mockup/2 ô tick trên `hrm-client` (nhánh `feat/p1-danh-muc-hang-hoa`): **KHÔNG merge**. Nhánh feat đóng băng làm tài liệu tra cứu. Khi user cho phép code ⇒ mở **nhánh mới từ `gop_db`**, rà từng file, phần nào lấy lại đều nêu cho user duyệt. 4 migration đã chạy vào DB local `hrm_erp` để nguyên (xử lý khi mở nhánh mới) |
| E2 | **Giữ** cột `vehicle_life.status` (đã lên `origin/gop_db` qua đợt cherry-pick xe 02/10). Việc sau: sửa `VehicleLife::searchByFilter()` / `getForSelect()` của ERP lọc `status` (sổ chốt §5-10) |
| Câu phụ A0 | Đã trả lời qua E1: Phase 2 mở **nhánh mới từ `gop_db`** (Phase 1 đã lên `gop_db` bằng cherry-pick 02/10) |

| Câu phụ mockup | `mockup-hang-hoa.html` (3,2 MB, bản 21/09) **đã XOÁ** (04/10) — bản chốt duy nhất là `mockup-luong-xay-dung-hang-hoa.html` |

**Nhóm E ✅ xong 04/10/2026.**

---

### 35f. Nhóm F — phát sinh từ §36 (04/10/2026)

| # | Chốt |
|---|---|
| F1–F5 | 🔄 **Tab *Nhóm máy* QUAY VỀ thiết kế trước 01/10** (user 04/10: *"Back thiết kế tab Nhóm máy về bản trước ngày 1/10, các thay đổi khác trong 1/10 vẫn giữ"*) ⇒ **§36h, §36i, §36j, §36k, §36l BỊ HUỶ**. Tab dùng lại khuôn ERP *"Phụ tùng – Phụ kiện"* (§21a): ô **Nhóm máy** chọn nhiều → bảng **Máy** `*` + nút *Chọn máy* / xoá dòng, bảng chỉ hiện khi đã chọn ≥ 1 nhóm. Hệ quả: F1, F2 (lưu Loại sản phẩm / chọn nhiều loại) **không còn**; F3 ⇒ dữ liệu nhóm máy + máy của ERP **dùng tiếp nguyên trạng** (`group_ids_use` + `productables`, nhớ bẫy `productable_type`); F4 ⇒ 2 ô lọc *Dùng cho nhóm máy / Dùng cho máy* ở popup *Xem hàng hoá Công ty khác* **giữ nguyên**; F5 ⇒ tên tab **giữ "Nhóm máy"** |

Mockup đã khôi phục 04/10 từ đúng mã nguồn trước §36h (lấy lại từ log phiên 01/10, không viết mới): khối
JS `veTabMay/veKhoiMay/themMay/boMay` + dữ liệu `MAY_THEO_NHOM` + biến `mayDaChon`; gỡ CSS `.tb-giai`,
`.pk-dang` và 2 bộ nghe `f-name`/`f-model`. Giữ cờ bỏ qua `data-chi-doc` trong `datVaiForm` (vô hại).
Đo (cổng 8932): tab tiêu đề *Phụ tùng – Phụ kiện*; chưa chọn nhóm ⇒ không có bảng; chọn *Cầu nâng* ⇒
bảng hiện *"Không có máy"*; *Chọn máy* ×2 ⇒ 2 dòng; xoá 1 ⇒ còn 1; bỏ nhóm ⇒ ẩn bảng; tạo mới ⇒ trống;
0 dấu vết UI §36h–§36l; console chỉ 404 favicon. Ảnh `anh-mockup/35f-tab-nhom-may-quay-ve.png`.

| # | Chốt |
|---|---|
| F6 | Card *Khai báo hải quan* (tab Mua hàng) **đổi tên "Thông tin nhập mua"** — đã sửa mockup 04/10 |
| F7 | Bỏ checkbox BVMT: BE **tự suy cờ `need_environment_tax` = 1 khi hệ số có giá trị, = 0 khi trống** (ERP đọc cờ ở ~15 chỗ, chép sang tờ khai hải quan `CustomDeclaration` / `OrderImportRequest`). Giữ luật ERP: đã nhập thì **1 ≤ hệ số ≤ 999.999** |
| F8 | *% giảm giá thanh lý* (`products.rate_liquidation`): **BỎ khỏi HRM, dùng % của Nhóm hàng**. Không xoá cột, không xoá 1.251 giá trị cũ (đóng băng — ERP vẫn ưu tiên % riêng của hàng khi có, `SearchController:813` + 3 chỗ tương tự). ⚠️ Hệ quả cho **Phase 5** (gỡ màn `groups`, giữ bảng): `groups.rate_liquidation` hiện sửa ở màn Nhóm hàng ERP — gỡ màn đó thì **không còn chỗ nào sửa % thanh lý**; phải tính khi mở Phase 5 |
| F9 | 12 câu tooltip ⓘ (§36m 10 trường + §36n 2 tab chính) **duyệt nguyên văn**, sửa sau nếu cần; khi code gom vào 1 hằng chung kiểu `CATALOG_TOOLTIPS` |

**Nhóm F ✅ xong 04/10/2026.**

### 35g. Tổng kết cổng chặn (04/10/2026)

A ✅ · B ✅ · C ✅ · D ✅ · E ✅ · F ✅ · câu phụ ✅ — **CỔNG CHẶN ĐÃ ĐÓNG (04/10/2026).**
D1-b + D2: ⏸ user chốt **"Báo cáo để sau"** — Báo cáo hàng hoá theo công ty (§27) **ra khỏi Phase 2**, 2 câu gác theo.
Việc mockup C5/C5-b: ✅ xong 04/10.
Phạm vi Phase 2 sau vòng chốt: **phần Hàng hoá** — KHÔNG gồm Yêu cầu/Phiếu tính giá, Chính sách giá bán nội bộ (sang phase Tính giá), Báo cáo hàng hoá theo công ty (để sau).
⛔ Kể cả khi cổng chặn đóng hết: **chưa được code** cho tới khi user cho phép rõ ràng (CLAUDE.md gốc, quy tắc 04/10).

### 35h. Phụ thuộc lộ ra khi dời tính giá — chốt trước khi lập plan code (04/10/2026)

| # | Chốt |
|---|---|
| H1 | Chưa có luồng Tính giá ⇒ **nút TẠM "Chuyển kinh doanh"**: vẫn đủ bước *Đang nhập thông tin → Chờ tính giá*; giá bán vẫn khai/duyệt bên ERP như hiện nay; người có quyền **Xây dựng thông tin hàng hoá** bấm nút tạm để chuyển *Chờ tính giá → Đang kinh doanh*. Khi có phase Tính giá ⇒ gỡ nút, thay bằng *Lưu & duyệt giá bán* trên phiếu |
| H2 | (hồ sơ + kết quả: `../chuyen-cay-catalog/`) **Làm Phase 2d TRƯỚC, cùng đợt**: chuyển 3 danh mục Chương / Mục / Tiểu mục sang HRM để người dùng khai cây catalog, rồi mới tới màn hàng hoá (form bắt buộc ≥ 1 nhánh). Xoá data cũ (§30e) vẫn để sau, đúng thứ tự §30d |
| H3 | Dữ liệu cũ của `chapters` (65) / `job_groups` (106) / `job_clusters` (2): **ẨN khỏi HRM, CHƯA XOÁ**. Thêm cột `chapters.internal_business_scope_id` (nullable); màn HRM + form hàng hoá chỉ hiện nhánh có gốc mới (Mục/Tiểu mục lọc theo cha thuộc nhánh mới). Dòng cũ nằm nguyên cho ERP đọc; xoá hẳn sau theo §30d |
| H4 | `chapters.scope_id` (ERP: NOT NULL + FK `scopes`) ⇒ **migration bỏ NOT NULL, giữ FK**; chương mới khai ở HRM để `scope_id = NULL`, chỉ gắn `internal_business_scope_id`. Ngoại lệ Tiền đề 1 đã được user duyệt 04/10. ERP chỉ đọc `scope_id` ở ô chọn form hàng hoá ERP (bị chặn theo QĐ13) + đồng bộ CRM (đã ngừng) |

---

## 36. VÒNG SỬA MOCKUP SAU CHỐT (mở 01/10/2026)

Mở lại giao diện sau §34 theo yêu cầu user. Bản 30/09 vẫn là mốc đối chiếu; mọi thay đổi sau chốt
ghi ở mục này. Bản sao trước khi sửa: không lưu trong repo (git không theo dõi `.plans/`).

### 36a. Form tạo/sửa hàng hoá — xếp lại tab *Thông tin chung* / *Thông số kỹ thuật* (01/10/2026)

| # | Yêu cầu user | Đã làm |
|---|---|---|
| 1 | Card thông tin chung lên trước card *Phân loại* | Tab *Thông tin chung* nay xếp: **Thông tin hàng hoá → Phân loại** → Nguồn gốc → Đơn vị tính → Tài liệu kỹ thuật · Hình ảnh · Video |
| 2 | *Trọng lượng*, *Kích thước* + card *Thông số cơ bản* sang tab *Thông số kỹ thuật* | Card *Thông số cơ bản* chuyển sang **đầu** tab *Thông số kỹ thuật*; 2 ô *Trọng lượng (kg)* · *Kích thước (cm)* đặt thành 1 hàng (6 + 6 cột) **trong card đó**, ngay trên bảng thuộc tính |

Hệ quả bố cục: hàng 3 của card *Thông tin hàng hoá* chỉ còn *Định mức công lắp đặt* + *Công ty quản
lý* ⇒ giãn thành **6 + 6 cột** (không để hàng lẻ nửa dòng).

Đo trên trình duyệt (cổng 8913, mở `TPE-CN-2T-4500`): thứ tự card tab 0 đúng 5 card như trên · tab 1
có 6 card, card đầu là *Thông số cơ bản* chứa 2 ô vừa chuyển · tab 0 **0** ô Trọng lượng/Kích thước ·
4 hàng card *Thông tin hàng hoá* đều đủ bề rộng · cây Phân loại vẫn dựng đủ 7 ô · console chỉ có
404 `favicon.ico` (không phải lỗi mockup). Ảnh: `anh-mockup/36-tab-thong-tin-chung.png`,
`anh-mockup/36-tab-thong-so-ky-thuat.png`.

⚠️ Khi code: 2 cột `weight`/`size` (ERP) vẫn thuộc **lớp thông tin chung** của hàng hoá — chỉ đổi
chỗ hiển thị, không đổi chỗ lưu; quyền sửa tab *Thông số kỹ thuật* phải cho sửa được 2 ô này.

### 36b. Tab *Thông tin chung* — bỏ ô *Mã hàng hoá* + *Trạng thái* (01/10/2026)

User: *"Bỏ trường mã hàng hoá + trạng thái"*. Card *Thông tin hàng hoá* nay còn 4 hàng, hàng nào cũng
đủ 12 cột: **Tên hàng hoá · Model** (6 + 6) → Tên hàng thường gọi · Tên tiếng Anh · Barcode (4 + 4 + 4)
→ Định mức công lắp đặt · Công ty quản lý (6 + 6) → Ghi chú (12).
Gỡ kèm JS: 2 dòng gán `f-code` / `f-status` trong `moForm` và điều kiện bỏ qua 2 ô đó ở vòng khoá
theo quyền (`datVaiForm`) — còn **0** chỗ tham chiếu.

Đo (cổng 8914): mở `TPE-CN-2T-4500` và tạo mới đều ra đúng 4 hàng trên, **0** nhãn *Mã hàng hoá* /
*Trạng thái* trong form, không lỗi JS. Ảnh `anh-mockup/36b-bo-ma-trang-thai.png`.

⚠️ Hệ quả: form hiện **không chỗ nào hiện mã và trạng thái** (mockup không có tiêu đề màn). Khi code,
theo quy ước HRM, tiêu đề màn sửa phải ghép mã (`Sửa hàng hoá: <mã>`); trạng thái xem ở màn danh
sách. Mã vẫn do hệ thống sinh khi lưu (§16), bỏ ô không đổi cách sinh.

### 36c. Công ty quản lý lên hàng 1 · Định mức công lắp đặt sang tab Thông số kỹ thuật (01/10/2026)

| # | Yêu cầu user | Đã làm |
|---|---|---|
| 1 | Đưa *Công ty* lên hàng đầu cùng *Tên* + *Model* | Hàng 1 card *Thông tin hàng hoá*: **Tên hàng hoá · Model · Công ty quản lý** (4 + 4 + 4), Công ty vẫn chỉ đọc |
| 2 | *Định mức công lắp đặt* sang tab *Thông số kỹ thuật* | Vào hàng đầu card *Thông số cơ bản*: **Trọng lượng · Kích thước · Định mức công lắp đặt** (4 + 4 + 4) |

Card *Thông tin hàng hoá* nay còn **3 hàng**: Tên · Model · Công ty → Tên thường gọi · Tên tiếng Anh ·
Barcode → Ghi chú. Đo (cổng 8915, mở `TPE-CN-2T-4500` + tạo mới): mỗi ô hàng 1–2 rộng 603px, Ghi chú
1811px; tab 0 còn **0** ô *Định mức*; tab 1 hàng đầu đúng 3 ô; Công ty = TÂN PHÁT, disabled; không lỗi
JS. Ảnh `anh-mockup/36c-tab-thong-tin-chung.png`.
⚠️ Khi code: *Định mức công lắp đặt* cũng chỉ đổi chỗ hiển thị, vẫn là cột của lớp thông tin chung.

### 36d. Tab *Mua hàng* — bỏ *% giảm giá thanh lý*, gộp *SL tối thiểu nhập mua* lên card trên (01/10/2026)

User: *"Bỏ % giảm giá thanh lý ⇒ đưa SL tối thiểu nhập mua lên card phía trên, nằm sau HS Code"*.
- Card *Khai báo hải quan*: **Tên khai báo hải quan · HS Code · SL tối thiểu nhập mua** (4 + 4 + 4).
- **Bỏ ô *% giảm giá thanh lý*** và **bỏ luôn card *Đặt hàng*** (chỉ còn đúng 1 ô nên không còn lý do
  đứng riêng — đảo phần tách 3 khối của §32 về còn 2 card: *Khai báo hải quan* · *Thuế*).

Đo (cổng 8916, `TPE-CN-2T-4500`): tab Mua hàng còn 2 card, hàng đầu đúng 3 ô 608px, ô SL nhập được;
**0** chỗ còn ô *% giảm giá thanh lý*; không lỗi JS. Ảnh `anh-mockup/36d-tab-mua-hang.png`.
⚠️ Khi code: cột ERP của *% giảm giá thanh lý* **không xoá** (Tiền đề 1 — chuyển nền code, không
đổi CSDL); HRM chỉ không hiển thị / không ghi. Cần soát ERP còn chỗ nào đọc cột này trước khi coi là bỏ hẳn.
⚠️ Tiêu đề card vẫn là *Khai báo hải quan* dù có thêm ô SL tối thiểu nhập mua — chờ user quyết có đổi tên card không.

### 36e. Tab *Mua hàng* — bỏ checkbox *Tính thuế bảo vệ môi trường* (01/10/2026)

User: *"Bỏ checkbox Tính thuế bảo vệ môi trường ⇒ luôn hiện input ⇒ không bắt buộc"*. Đảo phần
checkbox + khoá ô hệ số của §31/§32 (vốn bám ERP `ng-disabled="!need_environment_tax"`).
- Ô **Hệ số tính thuế BVMT luôn hiện, nhập được, không có dấu `*`**; không tự xoá giá trị.
- Card *Thuế* xếp lại cho đủ 12 cột mỗi hàng: **% VAT · Thuế NK (không CO) · Thuế NK (có CO)** (4+4+4)
  → **Thuế chống bán phá giá · Hệ số tính thuế BVMT** (6+6).
- Gỡ JS: hàm `doiBVMT`, 2 chỗ gọi trong `datVaiForm` / `moForm` + chú thích — còn **0** tham chiếu `f-bvmt`
  (trừ id ô hệ số `f-bvmt-hs`).

Đo (cổng 8917): `TPE-CN-2T-4500` và tạo mới — 0 checkbox, ô hệ số hiện + mở, gõ `1.5` giữ nguyên;
hàng công ty khác (`POW-TBR-3D-X5`, quyền *chiQuanTri*) ô vẫn khoá theo quyền như mọi ô khác của tab;
không lỗi JS. Ảnh `anh-mockup/36e-tab-mua-hang-bvmt.png`.
⚠️ Khi code: ERP lưu cờ `need_environment_tax` + hệ số. Bỏ checkbox thì cần quy ước ghi cờ, đề xuất
**cờ = 1 khi hệ số có giá trị, = 0 khi trống** để các màn ERP đang đọc cờ vẫn tính thuế đúng — chờ
xác nhận khi chốt tồn.

### 36f. Popup *Xây dựng catalog kinh doanh* (01/10/2026)

| # | Yêu cầu user | Đã làm |
|---|---|---|
| 1 | Bỏ lọc *Công ty quản lý* + cột tương ứng | Gỡ ô `catf-cty` khỏi *Tìm kiếm nâng cao* (còn 8 ô) + điều kiện lọc trong `dsCat`; bảng bỏ cột *Công ty quản lý* |
| 2 | Nút nhỏ đóng/mở **toàn bộ** các cấp | 2 nút icon 28×28 cạnh ô *Tìm trong cây catalog*: **Mở toàn bộ các cấp** · **Thu gọn toàn bộ các cấp** |
| 3 | Nút đóng/mở **từng lĩnh vực** | Mỗi dòng Lĩnh vực có nút icon 20×20 (mũi kép, khác mũi đơn ▾ của dòng): bung **toàn bộ** Chương + Mục của lĩnh vực đó, bấm lại thì thu gọn; tooltip đổi theo trạng thái |
| 4 | Cột **STT** + cột **Ảnh** sau STT | Thứ tự: ☐ · **STT** · **Ảnh** · Mã hàng … STT chạy tiếp qua trang (trang 2 bắt đầu 21) |
| 5 | Cột **Thông số cơ bản** sau ĐVT | 1 dòng cắt ngắn (`Thuộc tính: giá trị; …`, rộng tối đa 190px, `…`) + nút **⋯** bấm mở khung *Thông số cơ bản · <mã>* liệt kê đủ từng dòng; bấm ra ngoài / cuộn là đóng |

Bảng nay 12 cột ⇒ đặt **mọi ô 1 dòng** + cuộn ngang (trước đó bảng bị bóp, mã/tên rớt 2–3 dòng, dòng
cao 57px; nay 43px, bảng 1.266px trong khung 1.069px).
Khung ⋯ dùng `position: fixed` (cùng lý do `.ra-menu`): khung cuộn của bảng không cắt mất; dòng cuối
khung tự lật lên trên. Dữ liệu thông số trong mockup là mẫu theo *Loại sản phẩm* (`TS_MAU`).

Đo (cổng 8919): cây mặc định 8 lĩnh vực → **Mở toàn bộ** 71 nút / 29 tiểu mục → **Thu gọn** về 8 →
nút lĩnh vực I mở 24 nút (riêng lĩnh vực đó) → bấm lại về 8; tiêu đề cột đúng 12 cột theo thứ tự trên;
khung ⋯ nổi trên cùng (`elementFromPoint`), đóng khi bấm ngoài; không lỗi JS.
Ảnh `anh-mockup/36f-popup-catalog.png`.
⚠️ Khi code: cột Thông số cơ bản đọc thông số của hàng hoá ⇒ API danh sách của popup phải eager load
(không N+1) và chỉ trả chuỗi tóm tắt + danh sách ngắn; nút ⋯ = `b-popover` theo khuôn info-popover.

### 36g. Nhóm *Phân loại* — icon ⓘ định nghĩa trên mọi ô (01/10/2026)

User: *"Toàn bộ các trường ở Phân loại đều bổ sung info icon ⇒ hover hiện thông tin định nghĩa phân loại"*.
5 ô đều có ⓘ, câu định nghĩa lấy **nguyên văn** `CATALOG_TOOLTIPS` trong
`hrm-client/utils/product-classification.js` (câu đang hiện ở ⓘ của 5 màn danh mục Phase 0 —
nguồn: tài liệu nghiệp vụ), không viết câu mới:

| Ô | Định nghĩa |
|---|---|
| Tính chất hàng hoá | Phân loại theo bản chất, vai trò của hàng hóa |
| Nhóm chức năng | Phân loại theo chức năng hoặc hệ kỹ thuật chính |
| Nhóm sản phẩm | Tập hợp các sản phẩm có cùng chức năng cơ bản |
| Loại sản phẩm | Phân biệt theo kết cấu, nguyên lý hoặc đặc điểm kỹ thuật |
| Đặc tính sản phẩm | Xác định sản phẩm thuộc loại tiêu chuẩn hay có khả năng thay đổi theo nhu cầu khách hàng |

Tooltip neo theo **mép trái icon** (căn giữa thì ô cột trái bị khung `.main` cắt 6–24px đầu câu — đo
thật trước khi sửa: bắt đầu x=34 trong khi khung từ x=58). Đo lại (cổng 8921): 5/5 tooltip nằm trọn
trong khung; icon còn nguyên sau khi đổi/bỏ chọn Loại sản phẩm (khối vẽ lại). Ảnh `anh-mockup/36g-phan-loai-info.png`.
⚠️ Khi code: dùng `V2BaseLabel :hint="CATALOG_TOOLTIPS.xxx"` (import từ `utils/product-classification.js`),
KHÔNG chép lại chuỗi — giống 5 modal danh mục.

### 36h. Tab *Nhóm máy* — bỏ logic cũ, chọn 1 mã thiết bị ⇒ hiện 4 cấp phân loại (01/10/2026) — ❌ HUỶ 04/10 (§35f)

User: *"Bỏ toàn bộ logic hiện tại · Select 1 mã thiết bị cụ thể ⇒ hiển thị 4 cấp phân loại tương ứng của thiết bị đó"*.

**Bỏ:** khuôn ERP *"Phụ tùng – Phụ kiện"* (`form.blade.php:353-421`) — ô chọn nhiều *Nhóm máy*, bảng
*Máy* (bắt buộc) + nút *Chọn máy* / xoá dòng, dữ liệu `MAY_THEO_NHOM`, `mayDaChon`, `themMay`, `boMay`.

**Mới** (card *Thiết bị sử dụng*):
- Ô **Mã thiết bị** — chọn **một**, có ô tìm; option `Mã - Tên`; danh sách = hàng hoá có *Tính chất
  hàng hoá* = **Thiết bị** (demo 123 mã). Không bắt buộc.
- Bên dưới 4 ô **chỉ đọc**, tự điền theo thiết bị đã chọn: **Tính chất hàng hoá · Nhóm chức năng ·
  Nhóm sản phẩm · Loại sản phẩm** (3+3+3+3), có ⓘ định nghĩa như §36g. Chưa chọn ⇒ để trống.
- Suy 4 cấp từ *Loại sản phẩm* của thiết bị theo cây Phase 0 (cùng nguồn với nhóm *Phân loại*).
- Mở hàng khác / tạo mới ⇒ ô chọn về trống.

Đo (cổng 8922): bấm ô → gõ `CN-2T` còn 1 mã → chọn `TPE-CN-2T-4500` ⇒ *Thiết bị · Gara · Cầu nâng ·
Cầu nâng ô tô 2 trụ*; đổi `TPE-MNK-FS-15A` ⇒ *Thiết bị · Khí nén · Máy nén khí · Máy nén khí trục vít*;
0 dấu vết UI cũ; không lỗi JS. Ảnh `anh-mockup/36h-tab-nhom-may.png`.

⚠️ Hệ quả cần chốt:
1. **Chọn 1 thiết bị** (đúng yêu cầu) — ERP cũ cho một phụ tùng gắn **nhiều máy**. Nếu một phụ tùng
   dùng cho nhiều thiết bị thì phải đổi sang chọn nhiều.
2. **Chỗ lưu**: ERP lưu nhóm máy + máy ở bảng nối riêng (`group_ids_use` + danh sách máy). Mô hình mới
   chỉ cần 1 cột `products.device_product_id` (hoặc bảng nối nếu chọn nhiều) — đổi CSDL ⇒ là ngoại lệ
   Tiền đề 1, chờ duyệt khi chốt tồn; dữ liệu nhóm máy cũ chưa quyết giữ/bỏ.
3. Popup *Xem hàng hoá Công ty khác* còn 2 ô lọc **Dùng cho nhóm máy / Dùng cho máy** theo khái niệm
   cũ — chưa sửa, chờ user (đề xuất: thay bằng 1 ô *Dùng cho thiết bị*).
4. Tab vẫn tên *"Nhóm máy"* — chờ user có đổi tên (vd *"Thiết bị sử dụng"*) không.

### 36i. Tab *Nhóm máy* — dòng giải thích logic (01/10/2026) — ❌ HUỶ 04/10 (§35f)

User: *"Thêm phần thông tin giải thích logic phía dưới: Phụ kiện [Tên hàng hoá] sẽ được sử dụng cho
toàn bộ các hàng hoá thuộc 4 cấp phân loại đã chọn"*.

Dưới 4 ô phân loại có 1 khối ghi chú (icon ⓘ, nền xám nhạt `#f8fafc`, chữ **xám `#6b7280`** — không
đỏ theo quy ước):
> Phụ kiện **<Tên hàng hoá>** sẽ được sử dụng cho toàn bộ các hàng hoá thuộc 4 cấp phân loại đã chọn**: <Tính chất › Nhóm chức năng › Nhóm sản phẩm › Loại sản phẩm>**.

- *Tên hàng hoá* lấy từ ô **Tên hàng hoá** của chính form, **gõ là đổi theo**; form tạo mới chưa
  nhập tên ⇒ hiện `[Tên hàng hoá]`.
- Phần đường dẫn 4 cấp chỉ nối thêm khi **đã chọn thiết bị**; chưa chọn thì câu dừng ở "…đã chọn."

⚠️ Câu này **đổi nghĩa của tab** so với §36h: thiết bị chỉ là cách **chọn nhanh 4 cấp** — phụ kiện
áp cho **mọi hàng hoá cùng 4 cấp** (cùng *Loại sản phẩm*), không chỉ riêng mã đã chọn. Hệ quả khi code:
- Chỗ lưu nên là **Loại sản phẩm** (`product_type_id`) chứ không phải mã thiết bị — mã thiết bị chỉ là
  công cụ chọn, có thể không cần lưu.
- Câu §36h-1 (chọn 1 hay nhiều) đổi thành: một phụ kiện dùng cho **nhiều Loại sản phẩm** khác nhau
  thì có cần chọn nhiều không.

Đo (cổng 8923): chưa chọn / đã chọn `TPE-CN-2T-4500` / đổi tên thành "Lọc dầu thử" / tạo mới — cả 4
ca câu chữ đúng; màu chữ `rgb(107,114,128)`; không lỗi JS. Ảnh `anh-mockup/36i-tab-nhom-may-giai-thich.png`.

### 36j. Tab *Nhóm máy* — hàng Tên + Model của phụ kiện đang khai (01/10/2026) — ❌ HUỶ 04/10 (§35f)

User: *"Thêm row hiện tên + model của mã phụ kiện đang khai báo ở phía trên select chọn thiết bị"*.
Hàng đầu card *Thiết bị sử dụng*: **Tên phụ kiện · Model** (6 + 6), **chỉ đọc**, tự điền từ ô *Tên
hàng hoá* và *Model* của tab *Thông tin chung*; sửa ở đó là đổi ngay ở đây. Tạo mới chưa nhập ⇒ trống.

🐞 2 lỗi im lặng bắt được khi đo:
- Vòng phân quyền `datVaiForm` quét MỌI input của tab và đặt `disabled = false` khi có quyền sửa ⇒ ô
  chỉ đọc vừa thêm (và cả 4 ô phân loại của §36h trước khi chọn thiết bị) bị **mở ra cho gõ**. Sửa: đánh
  dấu `data-chi-doc` cho ô tự điền, vòng phân quyền bỏ qua.
- Ô chọn kiểu mới (`nangCapSelect`) bắn `change` **không bubble** ⇒ nghe ở `document` không bắt được,
  đổi Model không cập nhật. Sửa: nghe ở pha **capture**.

Đo (cổng 8926): mở `TPE-CN-2T-4500` ⇒ *Cầu nâng 2 trụ 4.5 tấn · QJY-4.5*; đổi Model qua đúng panel ô
chọn sang `LR-300` + sửa tên ⇒ hàng này và câu giải thích §36i đổi theo; tạo mới ⇒ trống; 6 ô tự điền
đều `disabled`; không lỗi JS. Ảnh `anh-mockup/36j-tab-nhom-may-phu-kien.png`.
⚠️ Khi code: 2 ô này là hiển thị, không gửi lên BE.

### 36k. Tab *Nhóm máy* — thay 2 ô Tên + Model bằng 1 dòng chữ (01/10/2026) — ❌ HUỶ 04/10 (§35f)

User: *"Bỏ 2 trường tên + model: hiển thị dạng text: Đang khai báo thiết bị sử dụng cho Phụ tùng/phụ
kiện: Tên hàng: [Tên hàng] - Model: [model]"* ⇒ **thay §36j**.
Đầu card *Thiết bị sử dụng* là 1 dòng chữ (nhãn xám `#6b7280`, giá trị đậm `#374151`, không đỏ):
> Đang khai báo thiết bị sử dụng cho Phụ tùng/phụ kiện: Tên hàng: **<Tên hàng hoá>** - Model: **<Model>**

Vẫn lấy theo ô *Tên hàng hoá* / *Model* của form, đổi là cập nhật ngay; chưa nhập ⇒ `[Tên hàng]` /
`[Model]`. Gỡ 2 ô `f-may-ten` / `f-may-model` (còn **0** tham chiếu); cờ `data-chi-doc` của §36j giữ
cho 4 ô phân loại.

Đo (cổng 8927): mở `TPE-CN-2T-4500` ⇒ *Cầu nâng 2 trụ 4.5 tấn - QJY-4.5*; đổi Model qua ô chọn sang
`LR-300` + sửa tên ⇒ dòng đổi theo; tạo mới ⇒ `[Tên hàng]` / `[Model]`; không lỗi JS.
Ảnh `anh-mockup/36k-tab-nhom-may-dong-chu.png`.

### 36l. Tab *Nhóm máy* — sửa câu dòng chữ đầu card (01/10/2026) — ❌ HUỶ 04/10 (§35f)

User: *"Sửa text thành: Đang khai báo thiết bị có sử dụng Phụ tùng/phụ kiện: [Tên hàng]"* ⇒ **thay câu §36k, bỏ Model**.
> Đang khai báo thiết bị có sử dụng Phụ tùng/phụ kiện: **<Tên hàng hoá>**

Tên lấy theo ô *Tên hàng hoá*, gõ là đổi; chưa nhập ⇒ `[Tên hàng]`. (Bỏ khoảng trắng kép trong câu user gõ.)
Đo (cổng 8928): `TPE-PT-LOC-001` ⇒ *Lọc dầu động cơ Bosch F026407*; sửa tên ⇒ đổi theo; tạo mới ⇒
`[Tên hàng]`; không lỗi JS. Ảnh `anh-mockup/36l-tab-nhom-may-dong-chu.png`.

### 36m. Tab *Quản trị hàng hoá* — icon ⓘ cho toàn bộ trường (01/10/2026)

User: *"Tab Dữ liệu quản trị: bổ sung toàn bộ info icon cho các trường thông tin"*. 10 chỗ có ⓘ:

| Trường | Câu tooltip | Nguồn |
|---|---|---|
| Nhà cung cấp | Các nhà cung cấp mà công ty đang mua mặt hàng này. | **đề xuất** |
| Chính sách kinh doanh | Xác định chính sách kinh doanh của doanh nghiệp với từng sản phẩm | nguyên văn `CATALOG_TOOLTIPS.businessPolicy` |
| SL tồn kho tối thiểu | Số lượng tồn kho tối thiểu công ty cần duy trì cho mặt hàng này — làm mốc theo dõi tồn kho để nhập bổ sung. | **đề xuất** (ERP: `products.min_stock_qty`, đọc ở `ProductTemplate::stockSearchData`) |
| Bảo hành | Thời gian bảo hành áp dụng khi bán mặt hàng này cho khách hàng, tính theo Đơn vị bảo hành. | **đề xuất** |
| Đơn vị bảo hành | Đơn vị tính thời gian bảo hành: Ngày / Tháng / Năm. | **đề xuất** |
| Hệ số công nghệ | Hệ số hưởng của kỹ thuật khi lắp đặt mặt hàng này — tự điền sang phiếu phân công lắp đặt. | **đề xuất**, suy từ ERP: `AssemblyRequestController:550` gán `benefit_rate = product->tech_coefficient` |
| Lĩnh vực Công ty kinh doanh | Cấp 1 — lĩnh vực kinh doanh của công ty (danh mục Lĩnh vực Công ty kinh doanh). | **đề xuất** |
| Chương | Cấp 2 — nhóm lớn trong một lĩnh vực. | **đề xuất** |
| Mục | Cấp 3 — nhóm chi tiết trong một chương. | **đề xuất** |
| Tiểu mục | Cấp 4 — cấp cuối của catalog, nơi xếp hàng hoá. Hàng hoá phải gắn tới Tiểu mục; một hàng hoá gắn được nhiều nhánh. | **đề xuất** (theo §33) |

⚠️ **9/10 câu là đề xuất của Claude** — chỉ *Chính sách kinh doanh* có câu nghiệp vụ gốc. Chờ user /
nghiệp vụ duyệt câu chữ; khi code, câu chốt nên gom vào 1 hằng chung (như `CATALOG_TOOLTIPS`), không
viết rải trong template.

🐞 Khung 4 cột catalog đang `overflow:hidden` ⇒ **cắt mất tooltip** ⓘ ở tiêu đề cột. Sửa: mở
`overflow:visible`, bo góc riêng tiêu đề cột. Tooltip cả tab neo mép trái icon.
Đo (cổng 8929): 10/10 nhãn có ⓘ, 0 tổ tiên nào cắt tooltip, mọi tooltip nằm trong x=133…1848 (khung
nhìn 1920); không lỗi JS. Ảnh `anh-mockup/36m-du-lieu-quan-tri-info.png` (đang rê ⓘ Tiểu mục).

### 36n. ⓘ cho 2 tab chính (01/10/2026)

User: *"Thêm luôn info icon cho 2 tab chính"*. ⓘ nằm ngay sau tên tab cha:

| Tab | Câu tooltip (**đề xuất**, chờ duyệt) |
|---|---|
| Thông tin hàng hoá | Thông tin CHUNG của mã hàng — mọi công ty dùng chung một bản. Chỉ công ty tạo ra hàng hoá được sửa phần này. (§26c-bis) |
| Quản trị hàng hoá | Dữ liệu RIÊNG của công ty đang làm việc (nhà cung cấp, chính sách kinh doanh, tồn kho tối thiểu, bảo hành, hệ số công nghệ, catalog kinh doanh). Mỗi công ty tự khai, không ảnh hưởng công ty khác. (§23–§24, §30) |

🐞 Track segmented control `.tab-cha2` đang `overflow:hidden` ⇒ cắt mất tooltip. Mở `overflow:visible`
riêng cho `#tab-cha` (2 tab chỉ rộng 398px, không tràn). Thumb trượt vẫn khớp tab đang mở sau khi tab
rộng ra (đo sau khi hết animation: 73/202 ↔ 73/202 · 275/193 ↔ 275/193). Hover vẫn hiện ở tab đang
khoá (hàng công ty khác). Không lỗi JS. Ảnh `anh-mockup/36n-tab-chinh-info.png`.
