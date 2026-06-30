# Task P6 — Bản in chỉ in dòng cha (con không in ra cho khách)

## TASK 6.1 — Bản in BÁO GIÁ HÃNG

### Builder thật của bản in báo giá
- Controller in: `app/Http/Controllers/Sale/Firm/FirmQuotationController.php`
  - `printSynthe()` (dòng 459) → PDF/preview (web view `print_quota`/`print_landscape`, hoặc PDF lưu S3 qua `pdf_1.blade.php` / `pdf_landscape.blade.php`)
  - `exportExcel()` (dòng 592) → Excel (`getPrintSyntheTemplate4Excel`)
- Service builder: `app/Services/PrintTemplate/FirmQuotationPrint.php`
  - `getPrintSyntheTemplate()` (dòng ~95) dispatch theo `template_type` / `print_short`:
    - `getProductTableExtraContentAttribute` (dòng 159) — template_type=1, không short
    - `getProductTableExtraContentByGroup2Attribute` (dòng 1457) → uỷ quyền `getTableProductTab` (dòng 1638) — template_type=2
    - `getProductTableShortAttribute` (dòng 877) — template_type=1 + short
  - `getPrintSyntheTemplate4Excel()` (dòng ~1990) dùng:
    - `getProductTableExtraContent4ExcelAttribute` (dòng 415)
    - + 2 method dùng chung ở trên (`getProductTableShortAttribute`, `getTableProductTab`)
  - `getPrintSpecifications()` → `getProductTableForExtraInfoAttribute` (dòng 1585) — trang thông số kỹ thuật gửi khách

### Cách filter
Trong vòng lặp render từng dòng hàng, thêm ở đầu loop:
```php
if (!empty($product->child_parent_id)) {
    continue;  // bỏ qua dòng con, chỉ in cha/độc lập
}
```
- `continue` đặt TRƯỚC khi cộng `$total_cost_products`/`$total_cost_after_extra` và trước khi tăng STT → tiền + STT chỉ tính theo dòng cha. Khớp design.md (dòng con KHÔNG cộng vào tổng cuối — tổng = giá×SL dòng cha).
- Các method dùng key `$k => $product` làm STT (`getTableProductTab`, `getProductAnnexTableList`): đã đổi sang biến đếm thủ công (`$k`/`$stt`) để STT không bị "nhảy số" khi bỏ qua con.

### Các điểm đã sửa trong FirmQuotationPrint.php
1. `getProductTableExtraContentAttribute` — loop render dưới header `HÀNG BÁN`
2. `getProductTableExtraContent4ExcelAttribute` — loop render (Excel)
3. `getProductTableShortAttribute` — loop render (PDF short + Excel short)
4. `getTableProductTab` (nhánh non-combo) — dùng cho template_type=2 (PDF + Excel)
5. `getProductTableForExtraInfoAttribute` — bảng thông số kỹ thuật

### Builder dùng chung hay riêng?
- `getTableProductTab` + `getProductTableShortAttribute` dùng chung cho cả PDF và Excel báo giá hãng → 1 lần sửa áp dụng cả 2 đầu ra.
- Filter chỉ theo `child_parent_id` → **AN TOÀN cho các loại báo giá khác** (project / service / liquidation): những bảng đó không có khái niệm cha-con, cột `child_parent_id` luôn NULL nên `continue` không bao giờ kích hoạt. Ngoài ra các loại đó còn nằm ở model/service builder khác (`app/Model/Sale/ProjectQuotation.php`, `ServiceQuotation.php`, `LiquidationQuotation.php`), không đụng tới file đã sửa.
- Đã xác nhận relation `FirmQuotationTab::products()` = `hasMany(..., 'parent_id')` KHÔNG lọc con → cần filter trong loop (con vẫn nằm trong tập products).

> Lưu ý: các method KHÔNG được dùng trong luồng in báo giá hiện tại (đã verify bằng grep, chỉ còn ở comment): `getProductTableExtraContent2Attribute`, `getProductTableShort2Attribute`, `getProductTableExtraContentByGroupAttribute` (của FirmQuotationPrint). Không sửa để tránh thay đổi không cần thiết.

## TASK 6.2 — Bản in HỢP ĐỒNG HÃNG → ĐÃ SỬA (không phải N/A)

### Bản in HĐ hãng có render danh sách hàng
- Controller: `app/Http/Controllers/Sale/Firm/FirmContractController.php::print()` (dòng 972) → `FirmContractPrint::handlePrint()`
- Service: `app/Services/PrintTemplate/FirmContractPrint.php`
  - `handlePrint()` (dòng 36) chọn builder danh sách hàng:
    - `getProductGroupTab()` (dòng 151) — HĐ thường (mặc định)
    - `getProductGroupTabByGroup()` (dòng 579) — khi `print_group` → uỷ quyền `getTableProductTab` (dòng 935)
    - `getProductAnnexTableList()` (dòng 450) — phụ lục giảm (`type == PL_GIAM`)
  - `getPrintProductData()` (dòng 715) → `getProductTableExtraContentByGroupAttribute`/`Group2` → đều uỷ quyền `getTableProductTab` (covered transitively)

### Các điểm đã sửa trong FirmContractPrint.php
1. `getProductGroupTab` — nhánh non-combo (loop `$tab->products`) thêm skip child
2. `getProductAnnexTableList` — loop `$contract->products`, thêm skip child + đổi STT sang biến `$stt`
3. `getTableProductTab` — nhánh non-combo, thêm skip child + đổi STT sang biến `$k` thủ công

Nhánh combo (`tab_combo_product`) trong cả 2 service KHÔNG đụng vì combo lấy sản phẩm từ bảng combo riêng (`FirmQuotationComboGroupOptionProduct` / `$combo['calculated_combo']`), không có `child_parent_id`.

### Đã tìm những đâu (cho HĐ)
- `app/Http/Controllers/Sale/Firm/FirmContractController.php` (print/printExtraProduct/exportList/printTransport...)
- `app/Services/PrintTemplate/FirmContractPrint.php` (service in chính, đang dùng) — ĐÃ SỬA
- `app/Services/PrintTemplate/ZTFirmContractPrint.php` — biến thể Ztec, KHÔNG thuộc luồng HĐ hãng thường (controller riêng `ZtecFirmContractController`); **chưa đụng** (ngoài scope HĐ hãng chuẩn của feature này).
- `app/ExcelExports/` — có nhiều export HĐ (`FirmContractExportExcel`, `ContractDetailExcel`, `ContractExtraContentProduct`...). Đây là export nội bộ/kế toán/giao hàng, không phải "bản in HĐ cho khách" theo template. **Chưa đụng** vì ngoài phạm vi "bản in cho khách"; nếu cần áp dụng cho các export này → cần xác nhận từng file.

## VERIFY
- `php -l app/Services/PrintTemplate/FirmQuotationPrint.php` → No syntax errors
- `php -l app/Services/PrintTemplate/FirmContractPrint.php` → No syntax errors

## Concern / cần lưu ý
- `ZTFirmContractPrint.php` và các Excel export HĐ trong `app/ExcelExports/` chưa lọc con — nếu phạm vi feature muốn các bản này cũng ẩn con thì cần task bổ sung + xác nhận.
- Đã verify trên DB production (local .env trỏ prod) là KHÔNG thực hiện — chỉ đọc/sửa code, không tinker/migrate.
