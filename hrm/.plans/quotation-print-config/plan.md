# Plan — Popup cấu hình in báo giá: cột hiển thị

## Fix: Bỏ mặc định checked cột "Mã hàng hoá" (2026-07-13)

File: `hrm-client/components/assign/quotation/QuotationPrintConfigModal.vue`

- [x] Tách logic: mặc định (mounted / mở modal / đổi discountMethod) chọn tất cả cột TRỪ `code` (Mã hàng hoá) — method `selectDefault()`
- [x] Giữ nút "Chọn tất cả" (`toggleCheckAll` → `selectAll()`) vẫn chọn hết mọi cột (kể cả `code`)
- [x] User vẫn tự tích `code` được nếu muốn (checkbox v-model selectedColumns)

Cách: thêm `defaultUncheckedColumns: ['code']`, method `selectDefault()` (all trừ code) dùng cho mặc định; `selectAll()` giữ nguyên cho toggle.

### Checkpoint — 2026-07-13
Vừa hoàn thành: Bỏ mặc định tích cột "Mã hàng hoá" trong popup cấu hình in báo giá (thêm `defaultUncheckedColumns` + `selectDefault()`). FE-only.
Đang làm dở: (không)
Bước tiếp theo: user build FE + test (mở popup → "Mã hàng hoá" chưa tích; "Chọn tất cả" vẫn lấy hết; tự tích lại được).
Blocked: (không)

## Issue #10760 — Cột "Hình ảnh" + "Thời gian bảo hành" cho XUẤT EXCEL báo giá (2026-08-05)

Phần in đã xong trước đó; phần xuất Excel chưa dùng cấu hình. Branch `tpe-develop-assign`.

### BE (hrm-api)
- [x] `QuotationExcelExport::productColumns()` nhận thêm 2 cờ → chèn `Hình ảnh` + `Thời gian bảo hành` sau `Thành tiền sau VAT`, TRƯỚC 3 cột ẩn định danh
- [x] Thêm `withOptionalColumns($image, $warranty)` + truyền cờ vào `layout()` / `buildSampleProductRows()`
- [x] `QuotationController::exportQuotationData()` đọc query `with_image` / `with_warranty` (mặc định false); bản trống `forBlank()` giữ nguyên không có 2 cột

### FE (hrm-client)
- [x] `QuotationPrintConfigModal.vue`: thêm prop `mode` (`print` | `export`) — mode export chỉ hiện 2 checkbox Hình ảnh / Thời gian bảo hành, nút "Xuất Excel", emit `export`
- [x] `quotations/_id/index.vue`: nút Xuất Excel mở popup cấu hình → `handleExportExcel({image, warranty})` gắn query param
- [x] Áp dụng cùng luồng cho 2 chỗ xuất Excel còn lại: tab Báo giá của dự án TKT (`ProspectiveProjectParentQuotationsTab.vue`) + màn Báo giá tổng (`summary-quotations/_id/index.vue`). Riêng `quotations/_id/edit.vue` GIỮ NGUYÊN (xuất để sửa rồi import lại → không kèm cột hiển thị)
- [x] `QuotationImportModal.vue`: loại 2 cột mới khỏi phép tính `hasData` (chống dòng rác chỉ có bảo hành bị coi là dòng dữ liệu)

### Verify
- [x] Round-trip: xuất Excel có 2 cột → import lại chính báo giá đó (luồng Update) → số dòng/giá/GG khớp
- [x] Bỏ tích cả 2 → file 22/25/24 cột như cũ, import vẫn chạy

### Checkpoint — 2026-08-05
Vừa hoàn thành: xuất Excel báo giá theo cấu hình 2 cột Hình ảnh / Thời gian bảo hành (#10760), BE + FE + chống gãy import.
Verify đã chạy (tinker, DB local `hrm_prod_local`): 8 báo giá (tới 94 dòng, đủ 3 Loại GG) — export OFF vs ON rồi parse y hệt FE + `QuotationImportService::validate()` → kết quả import GIỐNG HỆT (hash payload thô + hash kết quả validate trùng khớp). Layout kiểm tra trên BG 217: 2 cột chèn đúng sau `Thành tiền sau VAT` (Z/AA), 3 cột định danh dời sang AB/AC/AD và vẫn ẩn, công thức không đổi.
Đang làm dở: (không)
Bước tiếp theo: user build FE + test trên dev. CHƯA verify được giá trị ảnh/bảo hành ở local vì `dev_erp.products` rỗng (0 bản ghi) → 2 cột luôn trống. Bug note #5 của issue (BG 189 không hiện bảo hành) phải test trên dev.
Blocked: (không)

### Test UI — 2026-08-05 (Playwright, local :3000/:8000, tài khoản namdangit@gmail.com)
- [x] AC1: nút Xuất Excel (BG 217) mở popup "Cấu hình xuất Excel báo giá" đúng 2 checkbox Hình ảnh / Thời gian bảo hành, tích sẵn cả 2
- [x] AC2: tích cả 2 → tải `BG-2026-00217_05-08-2026.xlsx` = 30 cột, Z=Hình ảnh, AA=Thời gian bảo hành, cột định danh AB/AC/AD vẫn ẩn
- [x] AC3: bỏ tích cả 2 → file 28 cột như cũ, cột định danh về Z/AA/AB
- [x] Mở lại popup thì 2 checkbox tích lại mặc định (selectDefault chạy đúng ở mode export)
- [x] Round-trip qua UI thật: xuất BG 240 có 2 cột → màn Sửa → Import Excel → Load lên bảng: parse đúng 2 dòng, cột không lệch; Validate trả **đúng 4 lỗi giống hệt baseline file không có 2 cột** (lỗi dữ liệu local: mã hàng ERP không tồn tại + hàng tạm thiếu Xuất xứ). KHÔNG bấm Import nên dữ liệu BG 240 không đổi.
- Ảnh: `.playwright-mcp/popup-cau-hinh-xuat-excel.png`, `.playwright-mcp/import-lai-file-co-2-cot.png`
- Chưa kiểm được: ảnh nhúng + chuỗi bảo hành (file xuất ra 0 ảnh) vì `dev_erp.products` local rỗng → phải test trên dev.

### Điều chỉnh theo yêu cầu user — 2026-08-05 (bỏ popup cấu hình khi xuất Excel)
- [x] Bỏ toàn bộ popup "Cấu hình xuất Excel báo giá": hoàn tác 4 file FE (`QuotationPrintConfigModal.vue`, `quotations/_id/index.vue`, `summary-quotations/_id/index.vue`, `ProspectiveProjectParentQuotationsTab.vue`) về nguyên trạng — nút Xuất Excel tải file luôn
- [x] BE `exportQuotationData()` mặc định BẬT cả 2 cột; vẫn tắt được bằng query `with_image=0` / `with_warranty=0` khi cần file đúng bộ cột mẫu import
- [x] Nhờ mặc định ở BE, nút Xuất Excel ở màn **Sửa báo giá** (`quotations/_id/edit.vue`) + tab Báo giá dự án TKT + màn Báo giá tổng đều có 2 cột mà không phải sửa FE
- [x] Giữ nguyên sửa `QuotationImportModal.vue` (2 cột không tính vào `hasData`)
- [x] Fix kèm: `AfterSheet` ẩn 3 cột định danh TRƯỚC guard "không có dòng hàng hoá" — trước đó báo giá rỗng (vd BG 260) xuất ra bị lộ 3 cột ID Hệ Thống / ID Báo Giá / ID BOM
- [x] Test lại UI: màn Sửa BG 260 (rỗng) → 28 cột, X=Hình ảnh, Y=Thời gian bảo hành, Z/AA/AB đã ẩn; màn chi tiết BG 217 → tải thẳng không popup, 30 cột, Z=Hình ảnh, AA=Thời gian bảo hành, AB/AC/AD ẩn
