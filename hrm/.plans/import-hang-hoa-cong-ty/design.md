# Import hàng hóa hàng loạt — Dữ liệu hàng hoá công ty

Vị trí: Danh mục › Hàng hóa › Hàng hóa, vật tư › Dữ liệu hàng hoá công ty (`/master-data/products/company`).
Ticket: "[Dữ liệu hàng hoá công ty] Bổ sung chức năng Import hàng hóa hàng loạt (Thêm mới và Cập nhật)".
File mẫu nghiệp vụ: https://docs.google.com/spreadsheets/d/1pLLXZWeobbjvC2lWoezZuqOwDZ3qYbpw/edit?gid=1507493306

## 1. Mục đích

Người dùng đang phải tạo và sửa từng hàng hóa qua form. Ticket cần một file Excel làm được cả hai việc, mỗi dòng ghi rõ THÊM MỚI hay CẬP NHẬT.

Yêu cầu của user: **giao diện và cách làm giống import BOM và báo giá**, chỉ mẫu file là khác. Người đã dùng import BOM phải dùng được màn này mà không cần học lại.

## 2. Mục tiêu và phạm vi

Mục tiêu:
- Nút Import trên màn Dữ liệu hàng hoá công ty, mở popup theo khuôn BOM.
- Thêm mới và cập nhật hàng loạt theo file 79 cột.
- Báo đủ lỗi của mọi dòng, sửa được ngay trên bảng rồi validate lại.

Ngoài phạm vi:
- Không import ảnh, video, tài liệu kỹ thuật, đời xe (file mẫu không có cột).
- Không có bước "Chờ xác nhận"; dữ liệu ghi thẳng vào danh mục.
- Không sửa `V2BaseImportModal` (11 màn đang dùng).
- Không đưa nút Import vào 3 màn hàng hóa còn lại.

Không được xảy ra:
- Cập nhật một phần làm mất dữ liệu ở ô để trống.
- Đổi mã hàng đã có.
- Xóa dòng ĐVT cũ, vì bộ giá và chứng từ đang trỏ vào `product_units.id`.
- Ghi đè giá hàng Đang kinh doanh.

## 3. Quyết định đã chốt

### User quyết định

| # | Vấn đề | Quyết định |
|---|---|---|
| U1 | Giao diện và cách làm | Theo BOM/báo giá: popup toàn màn hình, toolbar 3 nhóm (không có stepper: BOM và báo giá đã bỏ), pill Tổng/Hợp lệ/Lỗi, bảng lỗi có Sao chép và Tải File lỗi |
| U2 | CẬP NHẬT hàng do công ty khác tạo (đổi 07/11) | Công ty đã lấy về thì chỉ ghi 6 ô tab Quản trị của công ty mình; cột khác, gồm Hệ số công nghệ và Kinh doanh ngay, bỏ qua và tô xám. Giá: hàng kế thừa giá mà điền giá thì báo lỗi ở mọi trạng thái; hàng tự tính giá thì theo U3, chỉ ĐVT đã có và không thấp hơn giá công ty tạo. Chưa lấy về thì từ chối dòng |
| U3 | Cột giá khi hàng đang ở Đang kinh doanh | Bỏ qua cột giá, dòng vẫn cập nhật các cột khác |
| U4 | Model / Code đặt hàng chưa có trong danh mục | Báo lỗi, từ chối dòng |
| U5 | Bảng xem trước | Đủ 79 cột, sửa trực tiếp trên ô |
| U6 | Quyền ghi giá | Dòng có cột giá cần quyền 1657, thiếu quyền thì báo lỗi dòng. Có quyền thì ghi thẳng, kể cả công ty bật duyệt giá. Không xóa giá hẹn và đề nghị đang chờ duyệt |
| U7 | Kiểm tra trùng | Áp cả hai quy tắc: Model + Hãng SX + Code (ticket) và Tên + Model + Thương hiệu + Hãng SX (`checkUniqueName` của form). Đổi Tên khi CẬP NHẬT cũng kiểm tra quy tắc form |
| U8 | Hàng không ảnh | Chấp nhận, kể cả cờ Có. Lần sửa tiếp theo trên form sẽ buộc thêm ảnh |
| U9 | NCC và Catalog | Nhập nhiều giá trị bằng `;`, có dữ liệu thì thay toàn bộ. Catalog: 4 cột cùng số phần tử, tương ứng theo vị trí. Ghi rõ trong file mẫu |

### Claude quyết định (user cần xem lại)

| # | Vấn đề | Quyết định | Lý do |
|---|---|---|---|
| C1 | Thành phần FE | Modal riêng `components/product/ProductImportModal.vue`, clone layout BOM | Tiền lệ `QuotationImportModal`; base modal không có sửa ô theo trạng thái |
| C2 | File mẫu | File tĩnh `hrm-client/static/Mau_import_hang_hoa.xlsx` | Giống BOM |
| C3 | Dấu tách nhiều giá trị | Chỉ nhận `;`; sửa lại ghi chú và dữ liệu mẫu đang dùng dấu phẩy | Ticket ghi `;`, tên hàng có thể chứa dấu phẩy |
| C4 | Sinh mã | Dùng `ProductCodeGenerator::generate(manufactureId, barcodeId, modelId)`: `<mã Hãng>-<Code ?: Model>` | Một công thức cho cả form và import. Ticket ghi 3 trường, generator đã nhận đủ 3 trường nhưng Model chỉ dùng khi không có Code |
| C5 | Phạm vi kiểm tra trùng DB | Trên toàn bảng `products` còn hoạt động, không lọc công ty; barcode trống so với barcode trống | Hàng hóa dùng chung giữa các công ty, mã là duy nhất toàn hệ thống |
| C6 | Phạm vi khóa YCHG | Xét trạng thái **phiếu**, mọi công ty. Mở = 3, 2, 10, 1, 5, 7 | Ticket nói theo phiếu; thông tin hàng dùng chung nên phiếu công ty khác cũng phụ thuộc |
| C7 | Tên trạng thái trong lỗi | Dùng `STATUS_TEXT`, nên 1/5/7/10 đều hiện "Đang hỏi giá". Nhiều phiếu thì báo phiếu mới nhất | Khớp nhãn người dùng thấy trên màn YCHG |
| C8 | Thương hiệu khi CẬP NHẬT | Bỏ qua như Model, Hãng SX | Ghi chú file mẫu ghi vậy và `assertCodeSourceKept` cũng khóa `brand_id` |
| C9 | Điền Code đặt hàng khi đang trống | Chỉ ghi `barcode_id`, **không đổi mã hàng**; nếu tạo ra tổ hợp trùng thì từ chối | Mã hàng đã nằm trên chứng từ |
| C10 | ĐVT | Mỗi dòng 1 ĐVT. THÊM MỚI: là ĐVT cơ bản. CẬP NHẬT: ĐVT đã có thì dùng để gắn giá; chưa có thì thêm dòng mới và bắt buộc Hệ số > 0; không xóa dòng cũ. Replace All không áp dụng cho ĐVT | Dòng ĐVT cũ không sửa/xóa được (C7 của màn form) |
| C11 | Cột "Quy đổi" | Chỉ đọc, không lưu | Không có cột DB; `unit_coefficient` lấy từ "Hệ số" |
| C12 | Giao dịch | Validate lại toàn bộ, sau đó mỗi dòng một transaction; dòng lỗi lúc ghi được báo trong kết quả | Khác BOM (1 transaction): `store()` có retry và dọn dở dang riêng, 500 hàng trong một transaction giữ khóa quá lâu |
| C13 | Giới hạn | Tối đa 500 dòng dữ liệu mỗi file | 500 × 79 ô là mức trình duyệt còn chịu được khi có phân trang |
| C14 | Hiệu năng bảng | Phân trang 50 dòng/trang, ô chỉ thành input khi bấm vào | Render 39.500 input sẽ treo trình duyệt (xem memory màn show treo của ERP) |
| C15 | Quyền | Nút và 2 API dùng `$build` + `dueConfig:Cập nhật hàng hóa` | Trùng route tạo/sửa và `trade-without-price` |
| C16 | Cặp Mã–Tên ở lưới 1-N | Mã quyết định bản ghi; Tên phải khớp, lệch thì báo lỗi | Bắt nhầm cột; ghi chú file mẫu bắt buộc khai cả hai |
| C17 | Giá khi CẬP NHẬT hàng Đang nhập thông tin | Ghi giá từ file giống THÊM MỚI | U3 chỉ loại trừ hàng Đang kinh doanh |
| C18 | Tra danh mục theo tên | Code đặt hàng tra trong phạm vi Hãng SX của dòng. Danh mục khác tra toàn bảng. Khớp nhiều bản ghi thì báo lỗi; bản ghi ngừng dùng không tính là khớp | `barcodes` có `manufacture_id`, 84 tên Code trùng giữa các hãng; đoán bản ghi sẽ gắn sai |
| C19 | ĐVT khi CẬP NHẬT để trống | Giá gắn vào ĐVT cơ bản. Một lần import chỉ giá cho 1 ĐVT mỗi hàng | Giữ luật một mã một dòng trong file |
| C20 | Phạm vi validate khi CẬP NHẬT | Chỉ validate ô có dữ liệu trong file và ràng buộc giữa các cột đó, không validate cả bản ghi sau trộn | Hàng cũ thiếu Loại SP/VAT không được chặn một lần sửa ô không liên quan |

## 4. Trải nghiệm người dùng

1. Bấm **Import** trên toolbar màn công ty, cạnh Xuất Excel.
2. Popup 98vw × 98vh, không có stepper. Toolbar: File (Chọn file Excel, Tải file mẫu), Hành động (Load lên bảng, Validate), Hiển thị (Chỉ dòng lỗi).
3. Load: FE dùng `parseExcelFile()` (`utils/import-helper.js`), đọc từ dòng 5. Sai bộ header thì báo sai mẫu, không load.
4. Validate: FE gửi JSON, API trả trạng thái từng dòng. Pill cập nhật; ô lỗi tô đỏ; ô bị bỏ qua (ví dụ Model khi CẬP NHẬT) tô xám.
5. Sửa ô trên bảng rồi Validate lại. Dùng `_validateSeq` chống kết quả cũ về sau đè kết quả mới.
6. Import: nếu còn lỗi và chưa bật "Bỏ qua dòng lỗi" thì nút khóa. Bật thì mở khoá nút. FE chỉ gửi dòng hợp lệ, theo lô 50 dòng tuần tự với `skip_invalid=false`, cộng dồn kết quả và hiện tiến độ. Lô lỗi thì dừng, báo số đã ghi; dòng đã ghi rời lưới, phải Validate lại phần còn lại. Mỗi lần gọi `/products/import` giữ khoá toàn hệ thống `product-import`; có lượt khác đang ghi thì trả 409.
7. Kết thúc: báo số thêm mới, số cập nhật, số lỗi; tải lại danh sách.

Bảng lỗi: `Dòng Excel | Tên cột sai | Mô tả`, nút Sao chép lỗi, Tải File lỗi (CSV có BOM, sinh ở client), Đóng.

Kiểm tra Playwright tại `http://127.0.0.1:3000`, đối chiếu cạnh popup BOM.

## 5. API

Trong `Modules/MasterData/Routes/api.php`, đặt trước các route `/{product}`:

```
POST /products/import/validate   { rows: [...] }
POST /products/import            { rows: [...], skip_invalid: bool }
```

- Controller mới `V1\Product\ProductImportController`, service mới `Services/Product/ProductImportService.php`.
- BE không nhận file. `import` luôn validate lại, không tin kết quả FE.
- Lỗi dạng `['excelRow' => 'Dòng 5', 'column' => '...', 'message' => '...']`, gom đủ lỗi, không dừng ở lỗi đầu.
- Tra danh mục theo lô cho cả file, không query theo từng ô.

## 6. Quy tắc validate

Chung:
- Hành động chỉ nhận THÊM MỚI / CẬP NHẬT (bỏ khoảng trắng, không phân biệt hoa thường).
- Cột danh mục đối chiếu DB theo tên, không phân biệt hoa thường; không có thì lỗi. Một tên khớp nhiều bản ghi cũng là lỗi.
- Có/Không chỉ nhận đúng 2 giá trị này.
- Số phần tử Mã–Tên–ĐVT–Số lượng trong cùng lưới phải bằng nhau.
- Áp dụng cùng giới hạn với `ProductRequest` (độ dài, số > 0, không trùng trong lưới).
- Catalog 4 cấp phải là một nhánh đúng trong cây.

THÊM MỚI:
- Bỏ qua Mã hàng hóa. Bắt buộc các cột `(*)`.
- ≥ 2 dòng cùng Model + Hãng SX + Code trong file: lỗi ở tất cả các dòng đó.
- Trùng DB theo một trong hai quy tắc của U7: `Sản phẩm đã tồn tại trên hệ thống`. Trùng trong file cũng xét cả hai quy tắc.

CẬP NHẬT, kiểm theo thứ tự, dừng ở lỗi đầu của nhóm chặn này:
1. Mã hàng bắt buộc và tồn tại.
2. Hàng chưa xoá; hàng công ty khác tạo thì công ty đã lấy về (U2).
3. Hàng đang bị khóa: giữ thông báo sẵn có của `assertOwner`.
4. Không thuộc YCHG mở: `Hàng hóa đang bị khóa bởi phiếu YCHG [Mã_Phiếu] ở trạng thái [Tên_Trạng_thái], không được phép cập nhật.`
5. Trạng thái tại công ty là 1 hoặc 3; khác thì từ chối.

Hai dòng CẬP NHẬT cùng một mã trong file: lỗi ở cả hai dòng.

Hàng kế thừa giá luôn do công ty khác tạo: kiểm ở `validateForeign()` và kiểm lại trong transaction ghi giá.

## 7. Ghi dữ liệu

THÊM MỚI:
1. Dựng `$data` theo cấu trúc form rồi gọi `ProductWriteService::store()`.
2. Ghi `admin` để có mốc `info_entered_at`, điều kiện bắt buộc của `tradeBlocker`.
3. Ghi giá (mục 8).
4. Cờ Có: gọi `ProductLifecycleService::tradeWithoutPrice([$id])` để giữ nguyên lịch sử và đồng bộ kế thừa. Không tự set status.

CẬP NHẬT:
1. Đọc dữ liệu hiện tại của hàng, **trộn ô có giá trị từ file lên trên**, rồi mới gọi service. Bắt buộc vì `fillCommon` gán null khi thiếu key và `writeAdmin` xóa rồi ghi lại nhà cung cấp, catalog.
2. Ô có dữ liệu ghi đè, kể cả `0`. Ô trống giữ nguyên.
3. Lưới 1-N (thuộc tính, 4 lưới phụ kiện/vật tư, nhóm máy, máy, NCC, catalog): có dữ liệu thì thay toàn bộ, trống thì giữ. Ảnh, video, tài liệu, đời xe giữ nguyên.
4. Bỏ Model, Hãng SX, Thương hiệu. Code đặt hàng theo C9. `assertCodeSourceKept` chỉ được gọi ở `ProductWriteController::update`, nên đường import không đi qua; import tự kiểm C9.
5. Status 1 + cờ Có: ghi giá rồi gọi `tradeWithoutPrice`. Cờ Không/trống: giữ. Status 3: bỏ cờ và cột giá.

Mọi thay đổi ghi lịch sử hàng hóa như form, ghi chú "Import Excel".

## 8. Ghi giá

- Áp dụng: THÊM MỚI, và CẬP NHẬT hàng status 1 trước khi chuyển. Cần quyền 1657 (U6); kiểm ở bước validate, chỉ khi dòng có ô giá.
- Không gọi `ProductPriceUpdateService::update()` vì hàm này chặn hàng chưa Đang kinh doanh (`MSG_ENTERING`). Ticket yêu cầu lưu giá cả khi hàng ở Đang nhập thông tin, nên cần một hàm ghi riêng. `validate` và `resolvePrices` của màn giá đòi đủ 6 loại giá, không hợp với ghi từng ô, nên import dùng cùng giới hạn số (`MONEY_MAX`, hệ số < 100, % từ 0 đến 100).
- Không dùng nguyên `ProductPriceWriter`: `writePrices` xóa trường chờ duyệt, `writeExpected` xóa giá hẹn, `dropPendingApprovals` xóa đề nghị đang mở. Cả ba trái U6.
- Thứ tự: `ensureProductSet` → cập nhật `price`, `coefficient`, `sale_max_percent` của 5 loại giá trong `product_unit_prices` (Bán lẻ 1, Lô 5, ĐL1 2, ĐL2 3, ĐL3 4) → `cost_price` ở `product_company_units`.
- Giá gắn với ĐVT trên dòng file, trống thì ĐVT cơ bản (C19). Giá online (loại 6) tính lại từ Bán lẻ × `ecomCoefficient` như `resolvePrices` khi Bán lẻ đổi và cờ sửa tay tắt.
- Ô giá trống giữ nguyên; `0` là giá trị thật.

## 9. Việc để người làm tự quyết

- Tách service validate/ghi thành bao nhiêu class.
- Cách map cột Excel → key JSON.
- Bố cục pill và màu ô bỏ qua, miễn dùng token sẵn có của BOM.

## 10. Kiểm thử

API test (mỗi quy tắc mục 6 ít nhất một ca), trọng tâm:
- Cập nhật một phần giữ nguyên ô trống, `0` vẫn ghi đè, NCC và catalog không mất.
- Khóa YCHG: mỗi trạng thái mở bị chặn, mỗi trạng thái đóng được qua.
- `skip_invalid` ghi đúng dòng hợp lệ; tắt thì không ghi gì.
- Chuyển trạng thái có lịch sử; hàng Đang kinh doanh không đổi giá.
- Thiếu quyền 1657 mà có ô giá thì lỗi; công ty bật duyệt giá vẫn ghi thẳng, giá hẹn và đề nghị chờ duyệt còn nguyên. Local mọi công ty có `is_company_price = 0`, test phải tự bật.
- Trùng theo từng quy tắc của U7, cả trong file và trong DB.
- Điền Code đang trống không đổi mã hàng.

Playwright: tải mẫu, load, sửa ô, validate lại, chỉ dòng lỗi, tải file lỗi, import, danh sách cập nhật; đối chiếu với popup BOM.
