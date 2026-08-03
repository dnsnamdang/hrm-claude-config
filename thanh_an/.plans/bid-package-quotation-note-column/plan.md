# Plan — Thêm cột "Ghi chú báo giá" + đổi tên "Ghi chú thầu" (màn gói thầu)

Phụ trách: @khoipv
Màn: `bid_package/bid_package/add` (và dùng chung edit/detail vì chung component)

## Bối cảnh / Quyết định
- Hiện tại: cột `note` (label "Ghi chú") của gói thầu đang hiển thị & cho sửa giá trị ghi chú lấy từ báo giá.
- Yêu cầu tách 2 cột:
  1. **Ghi chú báo giá** (`note_quotation`) — cột mới, **read-only**, lấy từ trường `note` bên báo giá. **Lưu DB** (thêm cột + migration).
  2. **Ghi chú thầu** (`note`) — cột note hiện tại, chỉ **đổi label**. Khi tạo từ báo giá → **để trống** (không seed từ báo giá nữa).

## BE
- [x] Migration `2026_07_03_000001_add_note_quotation_to_bid_package_products_table` — `text('note_quotation')->nullable()->after('note')` (chỉ cột, không FK) — ĐÃ CHẠY
- [x] `BidPackageProduct::$fillable` thêm `note_quotation`
- [x] Chạy migrate OK
- Resource: DetailBidPackageResource trả product dạng model → `note_quotation` tự có ở edit/detail/copy, không cần sửa

## FE
- [x] `bid_package/components/ProductComponent.vue`:
  - [x] Thêm field `note_quotation` (label "Ghi chú báo giá", isVisible) trước field `note` trong `columns`
  - [x] Đổi label field `note` → `'Ghi chú thầu'`
  - [x] Thêm template body read-only cho `note_quotation` (span, giữ xuống dòng)
  - [x] Thêm class độ rộng `note_quotation: td-width-200`
  - [x] Cập nhật header + row xuất Excel (thêm "Ghi chú báo giá", đổi "Ghi chú"→"Ghi chú thầu")
  - Merge cột (getFields) dùng `this.columns` → user đã lưu cấu hình cũ vẫn tự có cột mới đúng vị trí
- [x] `bid_package/components/GeneralComponent.vue` — `addQuotation`: `pro.note_quotation = pro.note || ''; pro.note = ''`

## Import Excel (bổ sung theo yêu cầu)
- [x] File mẫu tĩnh `static/danh_sach_hanghoa_goi_thau.xlsx`: chèn cột "Ghi chú báo giá" (AQ) trước "Ghi chú" → đổi "Ghi chú" thành "Ghi chú thầu" (AR). Các cột sau dịch phải 1 (đặc biệt→AS, NCC→AT). Backup ở scratchpad.
- [x] Parser BE `Modules/Payroll/ExcelImports/ProductBidPackageImport.php`: **KHÔNG đọc cột 42** (row[42]) — note=`row[43]`, supplier_info=`row[45]`. `php -l` OK.
- [x] FE `handleImportSuccess` (ProductComponent): `note_quotation: noteQuotationMap[pid] || this.noteQuotationStore[pid] || ''` — KHÔNG lấy từ file. Dù file sửa cột 42 vẫn giữ nguyên giá trị báo giá.
- [x] FE thêm kho bền `noteQuotationStore` (data) tích lũy note_quotation theo product_id trong watcher `formSubmit` (chỉ thêm, không xóa) → khôi phục được kể cả khi user **xóa hết hàng rồi import lại** (snapshot from this.groups rỗng, nhưng store vẫn còn từ báo giá/DB).
- **CHỐT (user)**: import tuyệt đối không đọc "Ghi chú báo giá" từ Excel; luôn giữ giá trị gốc từ báo giá. Điều kiện hoạt động: giá trị phải có trong bộ nhớ — đúng với flow tạo từ báo giá (`addQuotation` set note_quotation) và edit (note_quotation lưu DB → load lại). Sản phẩm import mới hoàn toàn (không có trong báo giá) → trống.
- Đã check DB (`thanhan_stag_07052026`): cột `note_quotation` text/nullable tồn tại OK; các dòng cũ null vì tạo trước feature.

## Export backend (màn chi tiết) — phát hiện & fix
- Nút "Export Excel" trong ProductComponent rẽ nhánh: **chưa có `id` (thêm mới)** → export frontend ExcelJS (có cột mới); **đã có `id` (chi tiết/edit)** → gọi API `GET category/bid_packages/{id}/export-products` → file backend layout CŨ (thiếu "Ghi chú báo giá" + "Thông tin nhà cung cấp", vẫn ghi "Ghi chú"). Đây là lý do 2 file khác nhau.
- [x] Blade `resources/views/exports/bid_package_product_list.blade.php`: thêm header "Ghi chú báo giá" + "Thông tin nhà cung cấp", đổi "Ghi chú"→"Ghi chú thầu"; thêm cell `note_quotation`, `supplier_info` ở body; cập nhật colspan (group=45, empty=46). Giờ 46 cột khớp frontend.
- [x] `BidPackageController@mapProductForExport`: thêm `note_quotation`, `supplier_info`. `php -l` OK.
- Ghi chú: header wording nhỏ còn lệch ("Đơn giá chào thầu (gồm VAT)" FE vs "(đã bao gồm VAT)" BE) — cosmetic, chưa đổi.

## Verify
- [ ] Tạo gói thầu từ báo giá → cột "Ghi chú báo giá" hiện đúng ghi chú báo giá (read-only), "Ghi chú thầu" trống & sửa được
- [ ] Lưu → edit lại → cả 2 cột đúng
- [ ] Import Excel bằng file mẫu mới → "Ghi chú báo giá" & "Ghi chú thầu" vào đúng cột

### Checkpoint — 2026-07-03
Vừa hoàn thành: Toàn bộ BE + FE + Import (file mẫu xlsx + parser + handleImportSuccess). Migration đã chạy, parser lint OK.
Đang làm dở: (không)
Bước tiếp theo: User test trên trình duyệt (tạo từ báo giá + import Excel).
Blocked:
