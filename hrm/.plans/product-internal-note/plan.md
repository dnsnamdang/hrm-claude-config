# Plan — Ghi chú nội bộ hàng hoá (Báo giá + BOM)

Redmine: bổ sung "Ghi chú nội bộ" của hàng hoá, hiển thị ghép trong cột Tên hàng ở màn
tạo/sửa/chi tiết Báo giá và BOM. Chỉ đọc, chữ đỏ. Không hiển thị khi IN và khi xuất Excel.

Quyết định đã chốt (2026-08-28, user):
- Trường `note` cũ (cột "Ghi chú" trong bảng): thôi không snapshot ghi chú hàng hoá ERP nữa,
  chỉ còn là ô cho user tự nhập. Giữ nguyên ở bản in / Excel như hiện tại.
- Trường MỚI `internal_note`: lấy tương ứng từ ghi chú của hàng hoá ERP (`dev_erp.products.note`),
  KHÔNG cho sửa, hiện dưới tên hàng dạng `Ghi chú nội bộ: ...` màu đỏ.
- `internal_note` do BE tự chốt khi lưu (không tin FE gửi) — cùng cơ chế enforceErpProductVat.
- Chữ đỏ là yêu cầu trực tiếp của user (lệch quy ước "đỏ chỉ dùng cho lỗi validate" trong CLAUDE.md).

## Phase 1 — BE (hrm-api)

- [x] Migration thêm cột `internal_note` (text null, after `note`) cho `quotation_product_prices` + `bom_list_products`
- [x] `BomListService::syncErpFields()` — set `internal_note` từ `TpProduct->note` cho dòng ERP
- [x] `BomListService::mapProductPayload()` — KHÔNG cần sửa: payload không có `internal_note` nên cột luôn null cho hàng tạm
- [x] `QuotationService::enforceErpInternalNote()` mới + gọi trong `upsertPrices()` (sau enforceErpProductPrice)
- [x] `QuotationService::saveDirectProduct()` — KHÔNG cần sửa: `$data` không có `internal_note` nên FE không ghi đè được
- [x] `QuotationService::copyProductPrices()` — carry `internal_note` khi sao chép báo giá
- [x] `DetailQuotationResource` — trả `internal_note` (cả nhánh type=1 và type=2)
- [x] `DetailBomListResource` — trả `internal_note`
- [x] `ErpProductSearchService::mapProduct()` — trả thêm `internal_note` (= note sản phẩm ERP)
- [x] `BomListController::searchErpProducts()` + `getErpRecipeChildren()` — trả thêm `internal_note`
- [x] `ProductProjectController::reuseChildren` — trả thêm `internal_note`
- [x] Kiểm: KHÔNG thêm `internal_note` vào QuotationExcelExport / blade exports / file import

## Phase 2 — FE (hrm-client)

- [x] `QuotationProductSearchModal` — `note` thôi snapshot ERP (để rỗng), map `internal_note` vào item
- [x] `quotations/_id/edit.vue` — map `internal_note` khi load detail / thêm dòng / import; render dòng đỏ dưới tên hàng (cha + con)
- [x] `quotations/_id/index.vue` (chi tiết) — render dòng đỏ dưới tên hàng
- [x] `BomBuilderEditor.vue` — map `internal_note` vào row
- [x] `BomBuilderTableCard.vue` — render dòng đỏ dưới tên hàng (4 vị trí: cha/con × 2 chế độ)
- [x] Kiểm: `QuotationPrintPreview` / `BomPrintPreview` / 2 popup cấu hình in KHÔNG có `internal_note`

### Checkpoint — 2026-08-28
Vừa hoàn thành: toàn bộ Phase 1 (BE) + Phase 2 (FE).
Đang làm dở: không.
Bước tiếp theo: đã test xong (xem Phase 3). Chờ user duyệt để bàn giao.
  mã DHC-BT900 (erp_product_id 27316, ERP có ghi chú) để thấy dòng đỏ; kiểm bản in + Excel không có.
Blocked:

## Phase 3 — Kiểm thử trên trình duyệt (2026-08-28, FE :3000 / BE :8000, nhánh tpe)

Tài khoản: `namdangit@gmail.com` (đủ quyền) và `bont.kd2@tanphat.com` (KHÔNG có quyền "Xem giá vốn hàng hoá").

| # | Case | Kết quả |
|---|------|---------|
| TC01 | Chi tiết báo giá (BG #1): dòng đỏ nằm trong cột "Tên hàng", chỉ đọc | Đạt — 5/9 dòng có ghi chú hiện, màu `rgb(220,53,69)`, 0 input trong ô |
| TC02 | Bản in báo giá, BẬT HẾT cột | Đạt — không có nhãn lẫn nội dung ghi chú nội bộ |
| TC03 | Popup cấu hình in báo giá | Đạt — chỉ có "Ghi chú" cũ, không sinh mục mới |
| TC04 | Màn Sửa (BG #240): cột "Ghi chú" vẫn nhập được | Đạt |
| TC05 | Thêm hàng ERP có ghi chú từ popup | Đạt — dòng đỏ hiện NGAY chưa cần lưu; cột "Ghi chú" TRỐNG (hết prefill) |
| TC06 | Nhập ghi chú tay → Lưu → tải lại | Đạt — note user giữ nguyên, internal_note = nội dung ERP, không đè nhau |
| TC07 | Hàng tạm / dịch vụ / hàng ERP không có ghi chú | Đạt — không render gì (không hiện nhãn rỗng) |
| TC08 | Báo giá lập từ BOM (type=1, BG #248) — sửa + chi tiết | Đạt |
| TC09 | Chi tiết BOM (#51, view-only) | Đạt — hiện đỏ, 0 input |
| TC10 | Sửa BOM: thêm hàng ERP + lưu | Đạt |
| TC11 | Bản in BOM + popup cấu hình in BOM, bật hết cột | Đạt |
| TC12 | File Excel `bom-lists/{id}/export` + `export-quotation-data` | Đạt — không có ghi chú nội bộ; cột "Ghi chú" cũ VẪN còn (round-trip import không vỡ) |
| TC13 | Regression: màn Hàng hoá dự án, `copy-draft` báo giá | Đạt |
| TC14 | Tài khoản KHÔNG có quyền xem giá vốn | Đạt — vẫn thấy ghi chú nội bộ, trang không vỡ |
| TC-N1 | Nghịch: FE gửi `internal_note` giả qua PUT API | Đạt — BE bỏ qua, DB giữ nội dung ERP |

### Lỗi CÓ SẴN phát hiện trong lúc test (KHÔNG do thay đổi này)
`GET /assign/quotations/{id}/export-excel` trả 400: `Undefined property: stdClass::$show_children
(View: resources/views/exports/bom_list.blade.php)`. Đã xác minh bằng cách `git stash` toàn bộ thay
đổi của feature này — lỗi vẫn y hệt. Nguyên nhân: `QuotationController::exportExcel()` dựng
`$virtualProducts` bằng `stdClass` thiếu key `show_children`, còn blade dòng 128/210 lại đọc nó.
Chưa sửa (ngoài phạm vi task) — cần báo lại để mở task riêng.
