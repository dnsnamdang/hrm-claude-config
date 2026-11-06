# YCHG: khoá trường gốc của hàng tạm kế thừa từ nguồn đã duyệt

Màn: Bán hàng › Yêu cầu › Hàng hóa › YC hỏi giá. Áp dụng ở bước Kinh doanh tạo/chuẩn hoá phiếu và bước PTKD duyệt.

## Quyết định đã chốt

Người dùng chọn:

- Trường khoá: Tên hàng hoá, ĐVT, Model, Thương hiệu, Xuất xứ, Đặc điểm/TSKT, Hình ảnh.
- Mọi trường theo cách của Model: nguồn có dữ liệu thì khoá, nguồn trống thì cho nhập. Ảnh vẫn bắt buộc.
- Chỉ tính nguồn đã duyệt: BOM trạng thái 4, báo giá trạng thái 4 (Đã duyệt) hoặc 7 (Trúng thầu).
- Khoá mọi nơi: API và popup dùng chung, gồm popup Sửa ở màn Hàng tạm.
- Giữ link "Bỏ điền sẵn": bấm thì thành hàng nhập tay, không gắn nguồn, không khoá.

Đề xuất đã được duyệt:

- BE trả `locked_fields`; khi lưu, giá trị đã lưu thay cho dữ liệu gửi lên, không báo lỗi.
- Tính theo dữ liệu nguồn, không theo hàng: Model nguồn trống vẫn sửa được sau khi đã nhập, kể cả PTKD.
- Hàng gắn nhiều dòng nguồn: một dòng đủ điều kiện có dữ liệu là khoá.
- Hàng cũ: không sửa dữ liệu, giữ giá trị đang có rồi khoá.
- ĐVT nguồn không làm được ĐVT cơ bản thì mở.
- Hàng con ghép bộ: cùng quy tắc theo dòng nguồn của chính nó.
- Hãng SX, Loại SP, % VAT, Ghi chú giữ nguyên hành vi cũ.

Bổ sung khi thiết kế: chỉ khoá khi nguồn có dữ liệu VÀ hàng cũng có dữ liệu, để dữ liệu cũ thiếu trường bắt buộc không bị kẹt.

## Rủi ro đã chấp nhận

- Lưu lại BOM có thể chép Model của hàng tạm về dòng nguồn; Model bổ sung sẽ bị khoá từ lúc đó.
- Đơn vị quy đổi phụ PTKD vẫn thêm được. Chỉ dòng ĐVT cơ bản đã lưu là không đổi.

## Vị trí trong code

- API: `Modules/MasterData/Services/Product/TempProductSourceLock.php`, nối ở `TempProductRequest::prepareForValidation` (PTKD kế thừa), `TempProductController::show`, `PriceAskingRequestService::tempForm`.
- FE: `QuotationProductSearchModal.vue` (popup), `ProductForm.vue` + `ProductFormGeneral.vue` + `ProductFormSpecs.vue` + `ProductFormGallery.vue` (form PTKD).
