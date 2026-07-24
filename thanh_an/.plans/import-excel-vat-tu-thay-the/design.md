# Import Excel — Vật tư, phụ kiện thay thế sửa chữa (tab Thông tin bổ sung, màn Danh mục hàng hóa)

## Mục tiêu
Thêm 2 nút **Tải file mẫu** + **Import Excel** vào section "Vật tư, phụ kiện thay thế sửa chữa" (tab Thông tin bổ sung, màn `category/product`). Người dùng khai Mã nội bộ + Số lượng trong file → import → khớp hàng hóa danh mục → nạp vào bảng vật tư thay thế của form.

## Scope
- CHỈ section "Vật tư, phụ kiện thay thế sửa chữa" (không đụng 3 section khác).
- Không lưu DB lúc import — chỉ nạp vào state form; lưu khi Lưu cả form.
- Không migration, không phân quyền cấp.

## Các quyết định lớn (brainstorming)
1. **Khớp theo Mã nội bộ** (`products.internal_code`, `status=2`).
2. **Thêm vào; trùng `object_id` → cộng dồn Số lượng**.
3. **Có nút "Tải file mẫu"** — file .xlsx tĩnh trong client `static/`, 7 cột tham chiếu.
4. **Chặn toàn bộ nếu có ≥1 dòng lỗi** (mã không tồn tại / SL không hợp lệ) — báo danh sách dòng lỗi.
5. **Backend xử lý** file (Maatwebsite Excel) — tái dùng endpoint `importExcel` (thêm nhánh `type='replacement-attachment'`).

## Điểm tái dùng (đã khảo sát)
- Endpoint `POST .../importExcel` → `OtherIncomeController@importExcel`, dispatch theo `type`.
- Import class mẫu `ProductBidPackageImport` (ToCollection, startRow=2, khớp internal_code, invalid_rows[], stringToFloat).
- Modal FE mẫu `import-excel-modal-product-bid.vue` — đã có sẵn UX all-or-nothing (skip>0 → hiện bảng lỗi, không merge).
- Shape item khớp `addReplacementAttachment` hiện có + validation lưu bắt buộc `internal_code`+`name`.

## File thay đổi
- BE: **mới** `Modules/Payroll/ExcelImports/ProductReplacementAttachmentImport.php`; **sửa** `OtherIncomeController.php` (thêm nhánh type).
- FE: **mới** `components/modal/import-excel-modal-replacement-attachment.vue`; **mới** `static/vat_tu_thay_the_mau.xlsx`; **sửa** `pages/category/product/components/AdditionalInfo.vue`.

## Link spec chi tiết
`docs/superpowers/specs/2026-07-22-import-excel-vat-tu-thay-the-design.md`
