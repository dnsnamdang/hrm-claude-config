# Plan — Báo giá hiển thị Ghi chú DM hàng hóa (#11280)

@junfoke · Repo `TanPhatDev` · nhánh `task_11280`

## Bối cảnh
Hiển thị `products.note` (Ghi chú trong DM hàng hóa) dưới mỗi dòng hàng ở báo giá,
màu đỏ, dạng `Ghi chú nội bộ: <nội dung>`. Áp cho Thêm/Sửa/Chi tiết/Sao chép.
KHÔNG hiện ở mẫu in (PDF) và xuất Excel. 4 loại: BGHH/HĐNT/BGDA (FirmQuotation) + BGDV (ServiceQuotation).

Phát hiện then chốt: field `product_note` (= `products.note`) ĐÃ có sẵn trong
`Product::getDataAttribute()` (app/Product.php:1257) → FirmQuotation không cần đụng BE data,
data đã chảy tới FE row ở cả 4 màn. Chỉ cần thêm render. BGDV (merchandise) dùng whitelist field
nên phải bơm `product_note` thủ công ở cả BE (3 method) lẫn FE add-path.

## Tasks

### FirmQuotation (BGHH / HĐNT / BGDA)
- [x] FE render dòng đỏ `Ghi chú nội bộ:` dưới tên hàng — 4 vị trí:
  - [x] `sale/firm/quotations/form.blade.php` block 1 (tab Hàng hóa) + block 2 (tabs[0])
  - [x] `sale/firm/quotations/form_show.blade.php` block 1 + block 2
- [x] Data: KHÔNG cần sửa — `product_note` sẵn trong `$product->data` (add) và
      `BaseQuotationProduct::getDataForQuotationEdit()` (edit/show/copy).

### ServiceQuotation (BGDV)
- [x] BE: thêm `$merchandise->product_note = $product->note;` ở 3 method của
      `app/Model/Customers/WrServiceQuotation.php`: `getForShow` (896), `getForCopy` (1085), `getForEdit` (1340).
- [x] FE add-path: thêm `product_note: data.product_note` vào whitelist
      `service_quotations/formJS.blade.php` (addMerchandise).
- [x] FE render: dòng đỏ dưới tên hàng ở section `form.merchandises`
      (`service_quotations/form.blade.php`) — dùng chung create/edit/show.

### Loại trừ (đã xác nhận không đụng)
- [x] pdf*.blade.php, exports/quotation_excel*.blade.php: KHÔNG có `product_note` (grep sạch).

### Fix BGDV màn to_chuc — vật tư = choose_product_items (2026-08-28)
BA báo note chưa hiện ở mục "1.3 Danh sách vật tư". Nguyên nhân: màn `#/to_chuc` render vật tư
qua bảng **product_repairs → choose_product_items** (ng-repeat line 636), KHÁC với
`service.products` (line 778) đã sửa trước đó. Bổ sung đúng nhánh:
- [x] FE render: dòng đỏ dưới tên vật tư ở `product_item in product_repair.choose_product_items`
      (form.blade ~636). Lưu ý có block dead-code comment cùng cấu trúc (indent 28 vs 24) — sửa đúng block active.
- [x] FE add-path: `product_note: data.product_note` vào whitelist `ProductInformationProduct` (formJS ~104).
- [x] BE data: `$product_item->product_note = $product_item->product->note` ở 6 loop choose_product_items
      (product_repairs + product_warrantys × getForShow/getForCopy/getForEdit) trong WrServiceQuotation.php.
- [x] Class `ProductInformationProduct extends BaseChildClass` tự copy product_note (không trong no_set). php -l sạch, CRLF ok.
- Note: 3 điểm render BGDV giờ = merchandise + service.products + choose_product_items.

## Quyết định: LIVE (không snapshot) — chốt 2026-08-28 (ĐÃ THAY ĐỔI, xem dưới)
Ghi chú lấy LIVE từ `products.note` tại thời điểm mở màn (không đóng băng lúc lập báo giá).
Hệ quả đã báo BA và BA đồng ý:
- Xóa/sửa ghi chú trong DM → báo giá cũ (Sửa/Sao chép/Chi tiết) hiện theo DM MỚI (mất nếu đã xóa).
- Không cần thêm cột DB, không cần logic lưu snapshot. Đúng câu chữ "hiển thị ghi chú trong DM hàng hóa".
- Edge "hàng bị xóa hẳn khỏi DM": là hành vi sẵn có của màn (Mã/Model cũng đọc live), không thuộc scope task này.

## Kiểm tra
- [x] `php -l` WrServiceQuotation.php: sạch.
- [x] CRLF giữ nguyên toàn bộ 5 file (lines == cr).
- [ ] Verify browser (chờ dev server ERP :8001) — Thêm/Sửa/Chi tiết/Sao chép 4 loại; in/excel không có note.

### BGDV bổ sung — vật tư đi kèm dịch vụ (yêu cầu mới BA 2026-08-28)
BA đổi ý: mục "1.3 Danh sách vật tư" (vật tư đi kèm gói dịch vụ = `service.products` lồng trong
extend_products → services) cũng phải hiện Ghi chú nội bộ như bảng hàng hóa chính.
- [x] BE: thêm `$product->product_note = $productData['product_note'];` ở 3 loop enrich service-product
      trong `WrServiceQuotation.php` (getForShow 918, getForCopy 1117, getForEdit 1375).
- [x] FE create: KHÔNG cần sửa — `ProductInformationNewServiceItem extends BaseChildClass` tự copy
      `product_note` từ `response.data` (getData). submit_data không lưu → không persist.
- [x] FE render: dòng đỏ dưới tên hàng ở section `service.products`
      (`service_quotations/form.blade.php` ~781) — dùng chung create/edit/show.
- [x] php -l sạch, CRLF ok (2 file).

## Snapshot theo trạng thái — ĐÃ CODE (2026-08-28)
Rule chốt: **Đã duyệt → đóng băng** ghi chú theo snapshot lúc lưu; **nháp (STATUS_QUOTATION_CREATING/DANG_TAO) → live** theo DM.
Cơ chế: cột `product_note` (text null) trên bảng dòng hàng; **luôn snapshot DM lúc lưu**; hiển thị:
nháp → live; đã duyệt → dùng cột (fallback live nếu cột NULL = data cũ trước feature).

- [x] **Migration** `2026_08_28_000000_add_product_note_snapshot_to_quotation_lines.php` — thêm `product_note`
      vào 4 bảng: `firm_quotation_tab_products`, `wr_service_quotation_merchandises`,
      `wr_service_quotation_product_items`, `wr_service_quotation_extend_product_service_items`.
      **ĐÃ CHẠY trên DEV `erp_dev_30_01_26` (2026-08-28), 4 cột xác nhận CO.** (Prod: chưa.)
- [x] **Save snapshot** (server-side, KHÔNG qua fillable để không nhận từ FE):
  - Firm `FirmQuotationService::syncProducts` — `$p->product_note = $product->note` (guard chỉ tab_products, group_products không có cột).
  - BGDV `WrServiceQuotation`: `syncMerchandise`, `syncProduct` (item), `syncExtendProducts` (item) — `optional(Product::find(...))->note`.
- [x] **Display branch** — snapshot đóng băng CHỈ ở màn **Chi tiết (show)**; **Sửa + Sao chép luôn LIVE**
      (Sửa chỉ mở nháp; Sao chép tạo nháp mới → phải ăn ghi chú DM mới nhất, KHÔNG dính snapshot bản gốc):
  - Firm: **chỉ `getDataForShow`** áp snapshot (`status != DANG_TAO && product_note !== null`).
    `getDataForEdit` (dùng bởi Sửa + `getDataForCopy`) → LIVE, KHÔNG áp snapshot.
  - BGDV: cờ `$useSnapshot` = true ở `getForShow`, false ở `getForCopy`/`getForEdit`.
    Điều kiện 12 nhánh: `!$useSnapshot || status == CREATING || product_note === null` → live, ngược lại frozen.
  - **Verify tinker**: Firm 1937 (đã duyệt) COPY→live / SHOW→frozen ✓; BGDV 461 COPY→live / SHOW→frozen ✓.
- [x] php -l sạch (3 file), CRLF nguyên vẹn.

⚠️ **THỨ TỰ DEPLOY BẮT BUỘC**: chạy migration TRƯỚC (hoặc cùng lúc) khi deploy code — vì save set
`$obj->product_note` sẽ lỗi SQL "Unknown column" nếu cột chưa tồn tại. Display thì an toàn (cột thiếu → null → live).
Data cũ (báo giá đã duyệt trước feature) có `product_note = NULL` → hiển thị fallback live (chấp nhận, không backfill).

## Checkpoint — 2026-08-28
Vừa hoàn thành: FE render note đủ 4 loại Firm + 3 nhánh BGDV (merchandise, service.products, choose_product_items) + BE data BGDV. Cơ chế LIVE. php -l sạch, CRLF ok, không rò rỉ in/excel.
Đang làm dở: —
Bước tiếp theo: user verify hiển thị trên env đang test (cần deploy/pull task_11280). Verify OK → làm tiếp snapshot (mục TODO trên).
Blocked: chưa verify browser (dev server local chưa chạy; user test trên dev-erp cần deploy branch).
