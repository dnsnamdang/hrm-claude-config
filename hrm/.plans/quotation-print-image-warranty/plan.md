# Plan — Cột Hình ảnh + Thời gian bảo hành (In / Excel báo giá)

@khoipv · 2026-07-18

## Phase A — Bản IN (phủ AC1–AC4, test Playwright)

### BE
- [x] A1. `DetailQuotationResource.php`: batch query `mysql2.products` theo `erp_product_id` (sau if/else, try/catch).
- [x] A2. Gắn `image`(avatar) + `warranty`(format guarantee+guarantee_type) vào mỗi `$products` (chung cho cả 2 nhánh).

### FE
- [x] A3. `QuotationPrintConfigModal.vue`: push 2 cột `image`+`warranty` ở CUỐI. Tích sẵn (verify DOM checked=true).
- [x] A4. `QuotationPrintPreview.vue`: +2 cột `filteredColumns`; render `<img class=prod-img>` + warranty text ở 3 loại dòng; căn giữa; helper `cellImage`.
- [x] A5. `printContent()`: chờ toàn bộ `<img>` load (onload/error + fallback 3s) rồi mới `print()`.
- [x] A6. CSS `.prod-img { max-height:60px; max-width:90px; object-fit:contain }` (preview + cửa sổ in).

### Verify Phase A
- [x] A7. Playwright AC1–AC4 trên `/assign/quotations/57` (báo giá có hàng ERP) — TẤT CẢ PASS.

## Phase B — Xuất Excel (nhúng ảnh)

- [x] B1. `exportExcel` controller: batch mysql2 enrich `image_url`+`warranty` cho `$bom->products`; thêm `image`,`warranty` vào `$defaultFields` (cuối).
- [x] B2. `bom_list.blade.php`: +2 `<th>` + `<td>` ở 4 biến thể dòng (parent/child nhóm + flat); service auto @else; footer TỔNG CỘNG + VAT + GG + breakdown dùng `coreColCount` + pad `extraTrailCols`.
- [x] B3. `BomListExport.php`: `implements WithDrawings`; `drawings()` + `orderedProductRows()` (mirror đúng thứ tự blade, khớp điều kiện collapse) + `fetchImageResource()`; set row height dòng có ảnh.
- [x] B4. `$fieldWidths`: `image`=>14, `warranty`=>16.

### Verify Phase B
- [x] B5. Smoke test export qua controller (BG-2026-00057): xlsx hợp lệ 50KB, header đúng thứ tự (…Thành tiền sau VAT | Hình ảnh | Thời gian bảo hành), cột bảo hành "12 tháng", **3 drawing (ảnh nhúng)**, footer không vỡ.

## Phase B-FIX — Excel đúng file (2026-07-18, sau khi user báo Excel vẫn thiếu cột)

Phát hiện: nút "Xuất Excel" ở chi tiết báo giá gọi `export-quotation-data` → **`QuotationExcelExport`**
(file `{code}_{date}.xlsx`), KHÔNG phải `export-excel` → `BomListExport` mà Phase B đã sửa
(lúc khảo sát đầu nút gọi `/export-excel` bản stub; code sau đổi endpoint). ⇒ Phần Phase B nằm ở nhánh
nút không dùng. Fix đúng chỗ:
- [x] BF1. `QuotationExcelExport.php`: `productColumns()` +2 cột cuối (`Hình ảnh`, `Thời gian bảo hành`);
      `implements WithDrawings`; `enrichImageWarranty()` batch mysql2 theo erp_product_id;
      `normalize()` +`erp_product_id`; `renderRow()` +2 cell (ảnh trống + warranty text) +`_image_url`;
      `drawings()` neo ảnh cột `Hình ảnh` theo `_row`; registerEvents set width cột ảnh + row height; `fetchImageResource()`.
- [x] BF2. Blade `quotation_excel.blade.php`: KHÔNG đổi (lặp `$productColumns` cho cả header + row → tự có 2 cột).
- [x] BF3. Round-trip Import: FE `QuotationImportModal.parseFile()` map theo TÊN header (`o['Loại']`,`o['Mã hàng']`...) → 2 cột lạ bị bỏ qua. An toàn.
- [x] BF4. Verify smoke (quote 57): header `…Thành tiền sau VAT|Hình ảnh|Thời gian bảo hành`; warranty "12 tháng"; **3 ảnh nhúng** neo W12/W13/W14; php -l sạch; status 200.
- Ghi chú: Phase B cũ (BomListExport `/export-excel`) để nguyên — dormant (BomListExport dùng chung cho BOM export, chỉ kích hoạt cột khi field `image`/`warranty` có mặt; nút không truyền → không ảnh hưởng). Có thể dọn sau nếu muốn.
- ⚠️ Deploy: chỉ đổi `QuotationExcelExport.php` (PHP class) → deploy bình thường (opcache reset). KHÔNG cần view:clear (blade không đổi).

## Checkpoint — 2026-07-18
Vừa hoàn thành: TOÀN BỘ Phase A + B. Playwright AC1–AC4 (bản in) PASS trên báo giá 57; Excel verify qua smoke test (3 ảnh nhúng + cột bảo hành).
- AC1: popup có 2 checkbox Hình ảnh + Thời gian bảo hành, tích sẵn ✓
- AC2: tích cả 2 → 2 cột hiện + dữ liệu (ảnh S3 + "12 tháng"); trống đúng ở hàng ERP không có master ✓
- AC3: bỏ cả 2 → 2 cột ẩn, cột cuối "Thành tiền sau VAT", bảng 100% co giãn ✓
- AC4: tích 1 (image) → cột Hình ảnh hiện, Thời gian bảo hành ẩn ✓
⚙️ MÔI TRƯỜNG: DB local `hrm_production_18072026` thiếu cột `parent_id` (2 migration team pending 2026_07_17 bom_list_groups + 2026_07_18 quotation_groups) → mọi chi tiết báo giá 500. Đã chạy ĐÚNG 2 migration đó (`migrate --path`, user chốt) để unblock. KHÔNG chạy ~100 migration pending khác.
Đang làm dở: (không)
Bước tiếp: user review + hard-refresh verify bằng mắt (in thật/xuất Excel mở file). Chưa commit (theo quy tắc). Ảnh chụp: `.playwright-mcp` + `quotation-print-image-warranty-AC2.png`.
Blocked: 
