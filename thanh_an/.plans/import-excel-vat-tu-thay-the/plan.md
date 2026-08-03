# Plan — Import Excel Vật tư, phụ kiện thay thế sửa chữa

> Phụ trách: @namdangit — 2026-07-22
> Plan chi tiết (code mẫu đầy đủ): `docs/superpowers/plans/2026-07-22-import-excel-vat-tu-thay-the.md`
> Spec: `docs/superpowers/specs/2026-07-22-import-excel-vat-tu-thay-the-design.md`

## Phase 0 — Chuẩn bị (xong)
- [x] Brainstorming yêu cầu (5 quyết định lớn)
- [x] Viết spec chi tiết
- [x] Viết design tóm tắt
- [x] Viết plan chi tiết (6 task)

## Phase 1 — Backend
- [x] Task 1: Tạo `ProductReplacementAttachmentImport` (ExcelImports) — khớp `internal_code` status=2, gộp trong-file, gom dòng lỗi, `stringToFloat`. Verify DB thật PASS (quantity gộp=5, đủ 8 field). Fix: `name` lấy từ `product_name` (không phải `name`).
- [x] Task 2: Thêm nhánh `type='replacement-attachment'` vào `OtherIncomeController@importExcel` — all-or-nothing, trả `data.items` + `details.invalid`. `$json=stdClass`, có transaction (rollBack/commit đồng nhất), đặt trước chuỗi type chung. php -l PASS, route tồn tại.

## Phase 2 — Frontend
- [x] Task 3: Sinh file mẫu tĩnh `static/vat_tu_thay_the_mau.xlsx` (7 cột, ExcelJS). Verify đọc lại header đúng thứ tự, Node 14 OK.
- [x] Task 4: Modal `import-excel-modal-replacement-attachment.vue` — upload, bảng dòng lỗi, emit `imported`. Đọc response `response.data.details`/`response.data.data.items` (khớp modal mẫu product-bid), chặn theo `invalid.length`, không toast thành công. Template compile OK.
- [x] Task 5: Nối vào `AdditionalInfo.vue` — 2 nút (Tải mẫu + Import) + đăng ký modal + handler `onReplacementImported` (gộp theo object_id). $set reactive, data-changed đủ 4 key, template compile OK.

## Final review (fresh-eyes, opus) — xong
- [x] Soát chéo toàn bộ 5 file: 0 Critical. Core logic đúng end-to-end (khớp mã, all-or-nothing, gộp, shape/validate, response contract, event, không phá code cũ, không double-toast).
- [x] Fix 2 Important về feedback modal: bỏ `.csv` khỏi accept + xử lý `success=false`/items rỗng (toast rõ ràng, không treo).
- [x] Fix Minor: dùng `<Required />` (thay `(*)`), placeholder tiếng Việt.
- Bỏ qua (ghi nhận): I-2 `stringToFloat("1.000")→1.0` (giống production `ProductBidPackageImport`, rủi ro thấp — ô số Excel vẫn ra 1000); M-1 catch Exception thiếu namespace + M-2 transaction thừa (lỗi có sẵn dùng chung, vô hại với nhánh chỉ-đọc).

## Bổ sung
- [x] Import Excel "Hàng hóa rời kèm máy" (`accessoryOther`) — cấu trúc GIỐNG HỆT "Vật tư thay thế" (cùng cột, cùng item shape). BE: gộp type `accessory-other` vào chung branch `replacement-attachment` (tái dùng `ProductReplacementAttachmentImport` vì output shape giống nhau). FE: modal `import-excel-modal-accessory-other.vue` (mirror modal replacement, type='accessory-other', file mẫu riêng `hang_hoa_roi_kem_may_mau.xlsx`), nút Import ở toolbar phần Hàng hóa rời, handler `onAccessoryOtherImported` (gộp theo object_id vào `accessoryOther`).
- [x] Export Excel "Hàng hóa rời kèm máy" + refactor export dùng chung: gộp `exportReplacementAttachment`/`exportAccessoryOther` → gọi `exportAdditionalInfoList(list, sheetName, filePrefix)`. Đổi icon cho dễ phân biệt: Import = `fa-upload` (xanh dương), Export = `fa-download` (xanh lá), áp cho cả 2 phần.
- [x] Export Excel danh sách "Vật tư, phụ kiện thay thế" (client-side ExcelJS, giống pattern `product/index.vue`). Cột: STT | Mã nội bộ | Mã phụ kiện | Tên phụ kiện | Model | Hãng, nước sản xuất | Số lượng | **Thông số kỹ thuật**. `content` (thông số kỹ thuật) lấy qua `POST category/products/getData {ids: object_ids}` → `content_no_html`. Style header giống `hang_hoa_final.xlsx`. Nút "Xuất Excel" (`exportReplacementAttachment`) cạnh nút Import (hiện cả chế độ xem vì chỉ đọc). Tải bằng blob download (`vat_tu_thay_the_<timestamp>.xlsx`).
- [x] Import Excel "Hóa chất sử dụng" (`chemicals`) — cấu trúc KHÁC (có Đơn vị tính, KHÔNG có Số lượng). BE: class MỚI `ProductChemicalImport` (khớp `internal_code` status=2; đơn vị đọc từ cột "Đơn vị tính" → khớp package informations của hàng hóa, bỏ trống → đơn vị cơ sở; đơn vị không thuộc HH → lỗi dòng; dedup theo internal_code không cộng dồn; item shape có `unit_id`/`unit_name`). Nhánh `type='product-chemical'` trong `OtherIncomeController@importExcel`. FE: modal `import-excel-modal-chemical.vue` (type='product-chemical', file mẫu `hoa_chat_su_dung_mau.xlsx`), nút Import ở toolbar phần Hóa chất (icon fa-upload), handler `onChemicalImported` (gộp theo object_id: đã có → cập nhật đơn vị, chưa có → push). File mẫu 7 cột (STT | Mã nội bộ | Mã hóa chất | Tên hóa chất | Model | Hãng, nước sản xuất | Đơn vị tính).
- [x] Export Excel "Hóa chất sử dụng": tổng quát hóa `exportAdditionalInfoList(list, sheetName, filePrefix, options)` — thêm `options` cho cột giữa (mặc định giữ nguyên Vật tư/Hàng hóa rời). `exportChemical` truyền nhãn `Mã hóa chất`/`Tên hóa chất`/`Đơn vị tính` (`unit_name`, canh trái). Vẫn có cột **Thông số kỹ thuật** (`content_no_html` qua getData). Nút Export (`fa-download` xanh lá) cạnh nút Import ở toolbar Hóa chất.
- [x] Import + Export Excel "Thiết bị sử dụng" (`devices`) — giống Hóa chất (có Đơn vị tính, không Số lượng) nhưng dùng **Hãng, nước chủ sở hữu** (`owner_country`). BE: class MỚI `ProductDeviceImport` (khớp internal_code status=2; đơn vị theo package informations, mặc định đơn vị cơ sở; owner_country lấy từ `OwnerCountry::find(product->owner_country_id)`; item shape có `owner_country_id`/`owner_country_name`/`unit_id`/`unit_name`). Nhánh `type='product-device'` trong controller. FE: modal `import-excel-modal-device.vue`, file mẫu `thiet_bi_su_dung_mau.xlsx`, handler `onDeviceImported`. Export: mở rộng `exportAdditionalInfoList` thêm `countryHeader`/`getCountry` (mặc định nước sản xuất); `exportDevice` dùng owner_country + Đơn vị tính, vẫn có cột Thông số kỹ thuật. 2 nút Import/Export (fa-upload/fa-download) ở toolbar Thiết bị. LƯU Ý: import chỉ tác động mảng `devices` chọn tay (giống addDevice); thiết bị auto-sinh từ hóa chất do ProductService xử lý riêng khi Lưu, không đụng tới.
- [x] Làm đẹp file mẫu `static/vat_tu_thay_the_mau.xlsx`: header tô nền xanh (FF2E75B6) + chữ trắng in đậm + canh giữa + wrap + kẻ viền, freeze header (ySplit=1), auto-filter A1:G1, 2 dòng ví dụ có viền + nền xen kẽ, comment nhắc 2 cột bắt buộc (Mã nội bộ + Số lượng). GIỮ header ở ROW 1 để không lệch `startRow()=2` của BE. Verify đọc lại OK (Node 14, ExcelJS).

## Phase 3 — Kiểm thử (CHỜ USER)
- [ ] Task 6: E2E trình duyệt (cần bật Nuxt dev + tài khoản có quyền + biết vài Mã nội bộ status=2) — file lỗi bị chặn (hiện bảng lỗi), file hợp lệ nạp + cộng dồn trong-file, import lại cộng dồn theo object_id, Lưu form không vỡ validate, nút ẩn khi xem/không quyền

## Ghi chú
- KHÔNG commit git (user tự commit).
- KHÔNG migration (bảng `product_replacement_attachments` đủ cột).
- Không đụng nhánh `type` cũ trong `importExcel`; không sửa ProductService/ProductRequest.
