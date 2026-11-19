# Cập nhật nhanh hàng hoá — Design (Redmine #12191)

> Nhánh: `develop` (đã chứa `gop_db`) cả hrm-api + hrm-client. Ngày: 17/11/2026.

## 1. Mục đích

Port màn ERP **"Sửa nhanh hàng hóa"** (`/update-products`, `ProductsController@updateListProducts` /
`startUpdateListProducts`, view `resources/views/products/update_list_products.blade.php`) sang HRM. Màn này ở ERP đang
**bị ẩn** vì middleware `productMovedToHrm:product-list` đẩy người dùng sang HRM, mà HRM chưa có màn tương ứng.
Người dùng cần sửa hàng loạt thông tin của nhiều mã hàng trong 1 bảng, thay vì mở từng mã.

- Menu: Danh mục > Hàng hoá > **Hàng hoá, vật tư** > mục mới **"Cập nhật nhanh hàng hoá"** (thêm vào `subItems` trong
  `components/subsystem-menu/master-data.js`, sau "Hàng đang kinh doanh").
- Kế thừa ERP: bố cục bảng, danh sách trường sửa được, validate, luồng lưu.
- Nút "Thêm hàng hoá" mở **popup chọn hàng y hệt màn Báo giá**.
- Danh sách hàng chọn được: giữ như ERP (hàng đang kinh doanh tại công ty, có ĐVT gốc, có giá loại 1).

Không phải màn "Cập nhật nhanh giá hàng hoá" (`products.editPrices`). Màn đó đã port thành `/finance/product-prices`.

## 2. Mục tiêu, không làm, không được phép

- **Mục tiêu**: sửa nhiều mã trong 1 lần lưu. Lịch sử, khoá và quyền giống hệt màn sửa hàng hoá và Import Excel của HRM.
- **Không làm**: sửa giá, ĐVT, ảnh, tài liệu, thuộc tính, dữ liệu xe/máy, NCC, catalog. Không thêm mã hàng mới từ màn này.
- **Không được phép**:
  - Vượt luật HRM "chỉ công ty tạo hàng mới sửa thông tin chung".
  - Sửa được trường cấu thành mã hàng (Hãng SX, Code đặt hàng, Model) hoặc Thương hiệu.
  - Lưu nửa chừng: có 1 dòng lỗi thì cả lô không ghi.

## 3. Hiện trạng

### ERP

**Popup chọn hàng.** `SearchController` (khoảng dòng 478, 980, 1402) lọc theo cờ `for_update_list_products`:

```php
joinBaseUnitCompanyPrice($products, $priceCompanyId)
    ->where('pu.is_base', true)
    ->where('pp.price_type_id', 1)
    ->where('products.status', 1)
```

**Tải dòng.** Nút "Chọn" gom `product_ids`, sau đó `searchDataForUpdateProductScreen` (`product_ids`, `per_page=20`,
`current_page`) trả về các dòng. Mọi dòng tick sẵn. Nút "Cập nhật" gửi các dòng đang tick.

**Cột chỉ đọc**: tick, STT, Mã, Model, Thương hiệu, Hãng SX, Nhóm hàng hoá.

**Cột sửa được**:

| Cột | Trường |
|---|---|
| Tên | `name` |
| Tên tiếng Anh | `english_name` |
| Tính chất | `product_type`, enum |
| Loại hàng hoá | `product_cate`, nhiều giá trị, JSON |
| SL tồn tối thiểu | `min_stock_qty` |
| SL tồn tối đa | `max_stock_qty` |
| Code đặt hàng | `barcode_id`, lọc theo Hãng SX |
| Xuất xứ | `origin_id` |
| Tên khai báo HQ | `customs_name` |
| HS code | `hs_code` |
| % VAT | `vat_percent_tax_rate_id` |
| Thuế NK có CO | `import_tax_has_co_tax_rate_id` |
| Thuế NK không CO | `import_tax_tax_rate_id` |
| Thuế chống bán phá giá | `antidump_duty_tax_rate_id` |
| SL tối thiểu nhập mua | `min_buy_qty` |
| Ghi chú | `note` |

**Validate** theo từng mã, lỗi trả theo khoá `[id][field]`:
- `name` bắt buộc.
- `name` báo "Đã tồn tại" khi có mã khác trùng cả `name` + `model_id` + `brand_id` + `manufacture_id`.
- `product_type` bắt buộc.
- `origin_id` bắt buộc.

**Lưu.** Toàn bộ trong 1 transaction. Với mỗi mã: tạo `ProductVersion`, gán các trường, suy % thuế từ `tax_rates`,
`saveHistory`. Mã không phát sinh dòng lịch sử thì xoá version vừa tạo.

**Quyền**: `master_data.hang_hoa.update` (Catalog: `platforms => ['erp']`).

### HRM

- **Ghi hàng hoá**: `Modules/MasterData/Services/Product/ProductWriteService.php`.
  - `updatePartial($product, $data)` chỉ ghi các khoá có trong `$data` (có kiểm khoá, kiểm trường khoá khi đang tính
    giá, ghi lịch sử qua `ProductHistoryService`). Import Excel đang dùng hàm này qua `ProductImportWriter::102`.
  - `updateAdminPartial($product, $admin)` chỉ ghi khối quản trị của công ty đang làm việc. Dùng cho hàng công ty
    khác tạo.
  - `assertOwner`: `products.company_id` ≠ công ty đang làm việc ⇒ 403; hàng ERP đã xoá ⇒ 403; hàng khoá ⇒ 423.
  - `editScope()` trả `full` hoặc `admin`.
  - `CODE_SOURCE_FIELDS` (Hãng SX, Code đặt hàng, Model) và Thương hiệu khoá ở form sửa. `PRICING_LOCKED_FIELDS` khoá
    khi hàng đang trong luồng tính giá.
  - `fillCommon()` có danh sách cột cố định. Danh sách này **chưa có** `product_cate` và `max_stock_qty`.
  - `min_stock_qty` của HRM nằm ở khối quản trị theo công ty (`admin.min_stock_qty`), không nằm ở `products`.
- **Quyền ghi hàng hoá**: route `PUT products/{id}` gắn `checkPermission:master_data.thong_tin_hang_hoa.manage` +
  `dueConfig:Cập nhật hàng hóa`. Service tự kiểm lại quyền 1652 ở công ty đang làm việc (`assertCanWrite`).
- **"Tính chất" của ERP (enum `product_type`)** ở HRM đã chuyển sang cây phân loại: Tính chất → Nhóm chức năng →
  Nhóm sản phẩm → Loại sản phẩm (`product_type_id`, bắt buộc trong `ProductRequest`), cộng `product_characteristic_id`.
- **`Product::PRODUCT_CATES`** khai giống hệt ERP. Cột `products.product_cate` vẫn có, popup chọn hàng đã lọc được
  theo cột này.
- **Popup chọn hàng**: `components/product/picker/ProductPickerPanel.vue` (`multiple` mặc định true,
  `scope='trading'`). Màn Báo giá bọc panel này trong `pages/assign/quotations/components/QuotationProductSearchModal.vue`.

## 4. Quyết định đã chốt (user, 17/11/2026)

| # | Quyết định |
|---|---|
| Q1 | **Hàng do công ty khác tạo**: giữ luật HRM (phương án A). Dòng đó chỉ sửa được phần quản trị (SL tồn tối thiểu). Các cột còn lại chỉ hiện để xem, kèm ghi chú vì sao không sửa được. |
| Q2 | Cột HRM đang khoá khi sửa (Hãng SX, Code đặt hàng, Model, Thương hiệu) **chỉ hiện để xem** ở màn mới. Xuất xứ khoá khi hàng đang trong luồng tính giá, như form sửa. |
| Q3 | Cột "Tính chất" của ERP chọn theo **cây phân loại HRM** (ra `product_type_id`), không dùng enum cũ. |
| Q4 | Cách xây: **API lưu hàng loạt riêng** cho màn này (cách 1), gọi lại `updatePartial` / `updateAdminPartial`. |
| Q5 | **Được sửa hàm dùng chung**: thêm `product_cate` và `max_stock_qty` vào đường ghi một phần để giữ đủ cột như ERP. Import Excel cũng nhận được 2 trường này (không bắt buộc Import phải thêm cột). |

## 5. Các cách đã cân nhắc

1. **API lưu hàng loạt riêng — ĐÃ CHỌN.** Validate theo từng dòng và trả lỗi đúng ô. Lưu bằng đúng đường của Import
   nên lịch sử, khoá và quyền đồng nhất.
2. **Ép bảng về khuôn Import rồi gọi `/products/import/*`.** Ít code backend hơn, nhưng Import đọc theo mã hàng và giá
   trị dạng chữ của Excel, lỗi trả theo số dòng nên khó đỏ đúng ô. Loại.
3. **Mỗi dòng gọi `PUT products/{id}`.** Gọi API trong vòng lặp, và `ProductRequest` bắt gửi đủ mọi trường của form.
   Loại.

## 6. Thiết kế

### 6.1 BE (hrm-api, `Modules/MasterData`)

**Route**, đặt trong nhóm `products`:

- `POST products/quick-update/rows`
  - Body: `{ ids: int[] }`. Trần 200 id/lượt (FE phân trang 20 dòng như ERP).
  - Trả về mỗi dòng:
    - `id`, `code`, `model_name`, `brand_name`, `manufacture_name`, nhóm hàng hoá (tên đường dẫn cây phân loại).
    - Giá trị hiện tại của mọi cột sửa được (`product_cate` là mảng key, `min_stock_qty` lấy từ khối quản trị công ty
      đang làm việc).
    - `edit_scope`: `full` | `admin` | `none`. `none` là hàng không sửa được: khoá (423), ERP đã xoá, hàng tạm.
    - `readonly_reason`: câu giải thích khi scope khác `full`.
    - `locked_fields[]`: trường khoá do đang tính giá.
  - Trả kèm danh mục đang chọn của các dòng, để select hiện đúng tên kể cả khi danh mục đã khoá (🔒). Không gọi API
    danh mục theo từng dòng.
- `PUT products/quick-update`
  - Body: `{ rows: [{ id, ...các trường sửa được }] }`.
  - Middleware `checkPermission:master_data.thong_tin_hang_hoa.manage` + `dueConfig:Cập nhật hàng hóa`, như route sửa
    hàng hoá.

**FormRequest `ProductQuickUpdateRequest`.** Chỉ khai `rules()`, không khai `messages()`. Rule cho `rows.*.<field>`:

- `name`: required, max 255.
- `product_type_id`: required, exists.
- `origin_id`: required, exists.
- `product_cate`: mảng, mỗi phần tử `in:` các key của `Product::PRODUCT_CATES`.
- Số `>= 0` cho `min_buy_qty`, `min_stock_qty`, `max_stock_qty`.
- `exists:tax_rates` cho 4 ô thuế.
- `english_name`, `customs_name`, `hs_code`: max 255.
- `note`: chuỗi.

**Kiểm nghiệp vụ trong service** (gom lỗi của MỌI dòng rồi mới trả 1 lần 422, khoá lỗi `rows.<id>.<field>`):

- Trùng tên kiểu ERP (`name` + `model_id` + `brand_id` + `manufacture_id`, khác `id`) ⇒ "Đã tồn tại trên hệ thống".
  Kiểm cả trùng giữa các dòng trong cùng lô.
- Dòng `edit_scope = admin` gửi trường ngoài `min_stock_qty` thì bỏ qua trường đó. Không báo lỗi, vì FE đã khoá ô.
- Dòng `none` ⇒ lỗi chung của dòng (`rows.<id>._row`) với message của 403/423.

**Service `ProductQuickUpdateService`**:

- Bọc 1 `DB::transaction` cho cả lô, với từng dòng:
  - scope `full` ⇒ `updatePartial($product, $data)`. `min_stock_qty` đi trong `$data['admin']`.
  - scope `admin` ⇒ `updateAdminPartial($product, ['min_stock_qty' => …])`.
- Ghi chú lịch sử: `withHistoryNote('Cập nhật nhanh')`.
- Chỉ gửi các khoá có thay đổi so với giá trị lúc tải, để lịch sử không sinh dòng rỗng. FE gửi đủ cột, BE so với DB.
- Lỗi abort 403/423 ở giữa lô (dữ liệu đổi giữa lúc tải và lúc lưu) ⇒ rollback cả lô, trả 422 gắn vào `_row` của dòng
  đó.

**Sửa hàm dùng chung `ProductWriteService::fillCommon`** (đã được phép, Q5):

- Thêm `max_stock_qty` vào danh sách cột.
- Thêm `product_cate`: ghi JSON mảng key như ERP (`json_encode`), mảng rỗng ⇒ `null`.
- Đường ghi đầy đủ (`partial=false`) không được xoá trắng 2 cột này khi form sửa không gửi lên. Với 2 cột mới, chỉ
  ghi khi `array_key_exists`, kể cả lúc không ở chế độ partial.
- `ProductHistoryService` phải hiện được nhãn "Loại hàng hoá" và "SL tồn tối đa". Kiểm bảng nhãn của service, thiếu
  thì bổ sung. `product_cate` hiện theo tên của `PRODUCT_CATES`, không hiện key.

**Quyền.** Gate bằng `master_data.thong_tin_hang_hoa.manage` (xem mục 7).

### 6.2 FE (hrm-client)

**Trang** `pages/master-data/products/quick-update.vue`, link `/master-data/products/quick-update`. Menu `codes` /
`isShow` theo đúng mã quyền ở mục 6.1.

**Bố cục**:

- **Toolbar**: nút `+ Thêm hàng hoá` (mở popup) và nút xoá các dòng đang tick khỏi bảng (chỉ bỏ khỏi bảng, không xoá
  dữ liệu). Theo skill `button-convention`, các nút trong cụm dùng `mr-2 mb-2`.
- **Bảng viết tay** bọc trong `V2BaseTableScroll` (bảng rộng, thanh cuộn ở cả trên và dưới).
  - Cột theo thứ tự ERP ở mục 3.
  - Ô sửa dùng `V2Base*`. Select trong bảng dùng `V2BaseSelect`; select trong popup dùng `V2BaseSelectInModal`.
  - "Loại hàng hoá" là select nhiều giá trị.
  - "Tính chất" là ô chọn theo cây phân loại HRM, ra `product_type_id`. Dùng lại control chọn cây của form hàng hoá
    nếu tách được, nếu không thì chọn trên danh sách Loại SP kèm đường dẫn cây.
  - Thuế chọn theo danh sách `tax_rates`.
  - Ô chỉ đọc: `V2BaseInput disabled`. Dòng `admin` / `none` khoá các ô tương ứng và hiện `readonly_reason` dưới tên
    hàng, chữ xám `#6b7280` (không đỏ, không dùng `.text-muted`).
- **Phân trang** 20 dòng như ERP. Giá trị đã sửa giữ ở FE khi chuyển trang.
- **Nút "Cập nhật"** đặt trong `V2Footer` (slot `#custom-actions`). Chỉ gửi các dòng đang tick.
  - Lỗi 422 hiện đỏ dưới đúng ô của đúng dòng (vee-validate + lỗi BE), tự chuyển tới trang chứa dòng lỗi đầu tiên.
  - Không tự sửa giá trị user đã nhập.
- **Popup "Thêm hàng hoá"**: dựng lại đúng cấu hình `ProductPickerPanel` mà màn Báo giá dùng (cùng `scope`, cột, bộ
  lọc, cây phân loại, `stockExtraColumns`).
  - Bỏ các phần chỉ có nghĩa ở Báo giá: chọn nhóm BOM, nút tạo hàng tạm thủ công.
  - `existingIds` = các id đã có trong bảng.
  - Mã đã có trong bảng thì không thêm lần nữa.
  - Lọc hàng chọn được theo mục 6.3.
- **Thoát khi chưa lưu**: dùng `unsavedChangesMixin`. Lưu xong gọi `markFormSaved()`, báo thành công, ở lại màn và
  làm trống bảng.

### 6.3 Phạm vi hàng trong popup

ERP chỉ cho chọn hàng `status = 1`, có ĐVT gốc, có giá loại 1 tại công ty. `ProductPickerPanel` scope `trading` vốn đã
là "hàng đang kinh doanh tại công ty", và trong HRM điều kiện đang kinh doanh đã bao gồm có giá bán.

Builder kiểm lại `ProductPickerService` scope `trading`:
- Nếu đã tương đương điều kiện ERP thì dùng nguyên.
- Nếu lệch (vd thiếu điều kiện ĐVT gốc có giá loại 1) thì thêm 1 scope mới, không đổi scope `trading` đang dùng ở màn
  khác.

## 7. Phần để builder tự quyết (lựa chọn của mình, user chưa duyệt riêng)

- **Mã quyền**: gate bằng `master_data.thong_tin_hang_hoa.manage`, không dùng mã ERP `master_data.hang_hoa.update`.
  Lý do: đường ghi `ProductWriteService` tự kiểm 1652 ở công ty đang làm việc, nên mọi màn sửa hàng hoá của HRM đều
  dùng mã này. Dùng mã ERP thì user phải có cả 2 mã mới lưu được.
- **SL tồn tối thiểu** ghi vào khối quản trị theo công ty, khớp form HRM và cho cả hàng công ty khác sửa (Q1). **SL tồn
  tối đa** ghi vào `products.max_stock_qty` (cột chung, chỉ chủ hàng sửa), vì HRM chưa có cột theo công ty.
- **Popup**: dùng `ProductPickerPanel` với cấu hình của Báo giá, không nhúng nguyên `QuotationProductSearchModal` vì
  modal đó gắn chặt với BOM và nhóm báo giá.
- Trần 200 id/lượt cho API `rows`.
- Thứ tự mục menu.
- **Đổi Loại SP**: làm y như Import Excel. `updatePartial` dùng `writePresentChildren`, KHÔNG đụng dữ liệu xe hay
  thuộc tính. Hàng cũ chưa có loại thì chọn lần đầu không tính là đổi.
- **Đặc tính** (`product_characteristic_id`): ERP không có cột này nên màn không hiện và không gửi lên.
- **Bắt buộc Loại SP + Xuất xứ** chỉ áp cho dòng `full` được tick, giống ERP. Dòng cũ thiếu dữ liệu thì đỏ đúng ô và
  chặn cả lô; user điền hoặc bỏ tick dòng đó. Dòng `admin` không kiểm 2 ô này.
- **Ô tick**:
  - Dòng `none` không có ô tick và không bao giờ được gửi.
  - Dòng `admin` tick sẵn như các dòng khác.
  - BE bỏ qua những dòng không có khoá nào thay đổi.
- **Lô không có thay đổi nào**: không gọi API ghi. FE báo "Không có thay đổi nào để cập nhật".
- **Trùng tên kiểu ERP**: so trên toàn bảng `products`, không lọc công ty và không lọc `status`, đúng như ERP
  (`ProductsController:3866-3872`).
- **`product_cate`**:
  - So thay đổi theo tập hợp, không tính thứ tự.
  - Lưu theo thứ tự key của `PRODUCT_CATES`.
  - Đọc dữ liệu cũ: chấp nhận cả JSON mảng lẫn `null` / chuỗi rỗng.

## 8. Kiểm thử

**Feature test BE** (`Modules/MasterData/Tests/Feature/ProductQuickUpdateApiTest.php`):
- Lưu lô 2 dòng của chủ hàng: ghi đúng cột, có lịch sử ghi chú "Cập nhật nhanh".
- Dòng công ty khác: chỉ ghi `min_stock_qty`.
- Trùng tên kiểu ERP ⇒ 422 `rows.<id>.name`, cả lô không ghi.
- Bỏ trống Loại SP / Xuất xứ ⇒ 422.
- Hàng khoá ⇒ lỗi `_row`, rollback.
- `product_cate` + `max_stock_qty` ghi được.
- Form sửa đầy đủ (`PUT products/{id}`) không xoá trắng 2 cột này.
- Thiếu quyền ⇒ 403.

**Playwright**: thêm hàng qua popup, sửa, lưu, lỗi đỏ đúng ô, dòng công ty khác bị khoá ô.
