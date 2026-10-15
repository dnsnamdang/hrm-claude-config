# Plan — YCXH: Xuất Excel + Cài đặt bộ lọc

Chuẩn tham chiếu: `/finance/prepick-transfer-requests`. Nhánh `gop_db`.

## Phase 1 — BE (Xuất Excel data)
- [x] Task 1.1: Tách bộ lọc `index()` thành `private applyFilters($query, $request)` dùng chung.
- [x] Task 1.2: Thêm `export(Request $request)` — reuse `scopedQuery()` + eager loads + `applyFilters`, `->get()` (không phân trang), map rows thủ công (11 cột), trả `{rows, filter_text}`; helper `exportFilterText($request)` (nhánh from/to như prepick, đọc `start_date`/`end_date`) + `exportContractCode()`.
- [x] Task 1.3: Thêm route `GET /assign/product-export-requests/export` khai TRƯỚC `/{id}` (api.php:651).

## Phase 2 — FE (Cài đặt bộ lọc + Xuất Excel)
- [x] Task 2.1: Tạo `components/export-excel.js` (ExcelJS) — `PRODUCT_EXPORT_REQUEST_EXPORT_COLUMNS` (11 cột, cột Giá trị `numeric:true` → số thật + numFmt), `productExportRequestExportFields()`, `exportProductExportRequests(payload, selectedFields)`; filename `danh_sach_yeu_cau_xuat_hang.xlsx`; khối ký cuối file.
- [x] Task 2.2: `index.vue` — swap `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (`table="finance_product_export_requests"`, `:filter-fields`, event `filter-change`/`search`/`reset`/`toggle-panel`/`quick-search-change`) + computed `filterFields()` (org + contract_code + type + status + start_date + end_date) + slot `#field-org` + method `handleFilterChange`. Gỡ import/đăng ký các component không còn dùng (V2BaseFilterPanel/Label/Input/Select/DatePicker).
- [x] Task 2.3: `index.vue` — thêm nút "Xuất Excel" (`secondary status="success"`, icon `ri-file-excel-2-line`) vào `#actions-bottom` (Tạo mới → Xuất Excel), cờ `exporting`, `ExportFieldsModal` (`modal-id="product-export-request-export-fields-modal"`), computed `exportFields()`, method `openExportModal` + `exportExcel(selectedFields)` gọi `GET assign/product-export-requests/export`.

## Chỉnh sửa phụ
- [x] Đổi tiêu đề tab trình duyệt: thêm `head() { return { title: this.pageTitle } }` vào `index.vue` (khuôn `finance/bill-adjust-depts`) → tab hiện "Yêu cầu xuất hàng" thay vì tên chung "Tân phát_HRM". `pageTitle` cũng đã đổi sang 'Yêu cầu xuất hàng' (thanh tiêu đề trong app).

- [x] Gộp 3 nút "Tạo mới / Xuất Excel / Cấu hình cột" về CHUNG slot `#actions` (1 hàng ngang tiêu đề bảng), thứ tự theo button-convention; bỏ slot `#actions-bottom`. Khuôn `finance/bill-adjust-depts`.

## Chỉnh sửa theo review (2026-09-11) — 6 mục — ĐÃ XONG
- [x] 1. Đổi icon nút "Lập đề nghị xuất kho" `ri-store-2-line` → `ri-file-add-line` (giống "Tạo báo giá dịch vụ" màn `customer-care/wr-information-requests`).
- [x] 2+3. Bỏ nút "Xem chi tiết" ở cột Thao tác (gỡ luôn method `goDetail`); Mã phiếu thành `<nuxt-link class="v2-cell-link field-line">` sang `/finance/product-export-requests/{id}` (đồng thời bỏ bold — class chuẩn không đậm). Khuôn `wr-information-requests` cell-code.
- [x] 4. BE: thêm `updater_name` + `updated_at` vào `ProductExportRequestResource` (relation BaseModel `employee_update.info`), eager-load `employee_update.info` ở controller index + show. FE: thêm 2 cột "Người cập nhật" + "Ngày cập nhật" (dd/mm/yyyy H:i) vào `defaultTableColumns` + cell template. Test tinker: updater_name="DNS Admin", updated_at="05/09/2026 11:07".
- [x] 5. Bỏ `sortable` cột Trạng thái (`status`); thêm `sortable: true` cột Khách hàng (`customer_name`). BE whitelist sort thêm `customer_name` + `updated_at`.
- [x] 6. Ô trống: bỏ hiển thị dấu `—`, để trống (các cell type_name/contract_code/customer_name/department_name/creator_name/created_at + 2 cột mới).

## Phase 3 — Bổ sung bộ lọc khớp ERP + cột Người/Ngày duyệt (2026-09-11, theo ảnh Redmine)
Mục tiêu: khớp bộ lọc màn ERP `product_export_requests?type=all`; ẩn Bộ phận/Nhân viên; thêm 2 cột duyệt.

### BE — `ProductExportRequestController`
- [x] Task 3.1: `applyFilters()` thêm 8 nhánh lọc (dùng chung index + export):
  - `warehouse_id` → `where(TABLE.warehouse_id, int)`
  - `is_export_direct` → `where(TABLE.is_export_direct, int)` (filled cho cả '0')
  - `need_install` → `where(TABLE.need_install, int)`
  - `customer_id` → `where(TABLE.customer_id, int)`
  - `created_by` → `where(TABLE.created_by, int)`
  - `approver` → `where(TABLE.approver_id, int)`
  - `product_name` → subquery `product_export_request_tab_products tp` join `products p` (need_export=1, p.name/p.code like) → `whereIn(TABLE.id, ids)`
  - `product_model` → subquery tp join p join `product_models pm` (need_export=1, pm.name like) → `whereIn(TABLE.id, ids)`
- [x] Task 3.2: Thêm method `warehouses(Request)` — query bảng `warehouses` (status=1 + company_id user), trả `[{id,code,name}]` (mirror ProductImportRequestService::warehouseOptions, giữ trong module Assign). Route `GET /assign/product-export-requests/warehouses` khai TRƯỚC `/{id}`.

### FE — `pages/finance/product-export-requests/index.vue`
- [x] Task 3.3: `initialFilters` thêm keys: warehouse_id, customer_id, created_by, approver, is_export_direct, need_install, product_name, product_model.
- [x] Task 3.4: Slot `#field-org` thêm `:disable_part="true"` + `:disable_employee="true"` (ẩn Bộ phận + Nhân viên). Cập nhật comment.
- [x] Task 3.5: `filterFields()` thêm: warehouse_id (select, warehouseOptions), customer_id (slot remote), created_by (select employeeOptions), approver (select employeeOptions), product_name (text), product_model (text), is_export_direct (select Có/Không), need_install (select Có/Không).
- [x] Task 3.6: Import + đăng ký `V2BaseSelectRemote`; thêm slot `#field-customer_id`; data `warehouseOptions:[]`, `customerInitialOption:null`; computed `employeeOptions` (map store→{id,name}) + `booleanOptions`; method `fetchCustomers`, `loadWarehouses`; gọi `loadWarehouses()` ở mounted.
- [x] Task 3.7: Thêm 2 cột `approver_name` (Người duyệt) + `approved_time` (Ngày duyệt, align center) vào `defaultTableColumns` + 2 cell template (BE Resource đã trả sẵn — FE-only).

## Kiểm thử
- [ ] Mở "Cài đặt bộ lọc" bật/tắt/kéo trường → reload giữ cấu hình (bảng `filter_customizations`).
- [ ] Xuất Excel → chọn trường → file tải về đúng cột, cột Giá trị là số (SUM được), lọc áp đúng.
- [ ] 8 bộ lọc mới lọc đúng; Bộ phận/Nhân viên đã ẩn; 2 cột duyệt hiển thị đúng.

### Checkpoint — 2026-09-11
Vừa hoàn thành: Toàn bộ code Phase 1 (BE) + Phase 2 (FE). Đã swap filter panel sang `V2BaseSmartFilterPanel` (có nút "Cài đặt bộ lọc"), thêm nút + luồng Xuất Excel. Đã verify không còn tham chiếu component cũ, route `/export` đứng trước `/{id}`, các helper BE (`getTypeName`/`getStatusList`/`scopedQuery`) tồn tại.
Đang làm dở: (không)
Bước tiếp theo: User chạy thử trên môi trường — kiểm 2 mục Kiểm thử ở trên (cấu hình bộ lọc persist + file Excel số thật SUM được).
Blocked:

### Checkpoint — 2026-09-11 (Phase 3)
Vừa hoàn thành: Toàn bộ Phase 3 (khớp bộ lọc màn ERP `product_export_requests?type=all`). BE: `applyFilters()` thêm 8 nhánh (warehouse_id, is_export_direct, need_install, customer_id, created_by, approver→approver_id, product_name/product_model qua subquery tab_products) — dùng chung index + export; thêm method `warehouses()` + route `GET /assign/product-export-requests/warehouses` đứng trước `/{id}`. FE `index.vue`: ẩn Bộ phận + Nhân viên trong `#field-org` (`:disable_part`/`:disable_employee`), thêm 8 ô lọc mới (Kho hàng, Khách hàng qua V2BaseSelectRemote, Người tạo, Người duyệt, Tên hàng hóa, Model, Xuất thẳng, Cần lắp đặt), thêm 2 cột Người duyệt + Ngày duyệt. Đã verify: PHP lint OK, grep raw-HTML RỖNG, line ending LF giữ nguyên (0 CR), 2 slot nằm đúng trong panel.
Đang làm dở: (không)
Bước tiếp theo: User chạy thử — kiểm 8 bộ lọc mới lọc đúng, Bộ phận/Nhân viên đã ẩn, 2 cột duyệt hiển thị.
Blocked:

## Phase 4 — Feedback Redmine (2026-09-22): nhãn "Người tạo" + mặc định xuất cột đang xem
Nguồn: ảnh Redmine (2 mục). Chuẩn tham chiếu vẫn là `/finance/prepick-transfer-requests`.

### FE — `pages/finance/product-export-requests/index.vue`
- [x] Task 4.1: Đổi nhãn cột danh sách `creator_name` "Người lập" → "Người tạo" (label + title) trong bộ cột gốc.
- [x] Task 4.2: SỬA lỗi đóng băng nhãn cũ — tách bộ cột gốc thành computed `baseTableColumns()`; viết lại `defaultTableColumns()` để **merge**: giữ THỨ TỰ + `isVisible` từ cấu hình user đã lưu (`columnFields`) nhưng LUÔN lấy nhãn/thuộc tính hiển thị từ bộ gốc theo `key`, cột code thêm mới thì nối vào cuối. → user đã lưu cấu hình cột vẫn thấy "Người tạo".
- [x] Task 4.3: Mặc định popup xuất Excel tick đúng các cột ĐANG HIỆN ở màn danh sách (item 1): thêm `exportFieldsMixin`, `:default-selected="visibleExportFields"`, `exportFieldKeyMap: { status: 'status_name' }` (bảng vẽ badge `status`, file xuất dùng khoá `status_name`). Ở cấu hình mặc định, tập này TRÙNG selectAll của prepick; chỉ khác khi user đã ẩn bớt cột → khi đó tick đúng phần đang xem, user vẫn thêm/bớt được.
- [x] Task 4.4: Đối chiếu `components/export-excel.js` với prepick — đã khớp format chuẩn (title/filter row/frozen/header/border/khối ký) + xử lý cột số "Giá trị" (số thật + numFmt) đúng CLAUDE.md. Không cần sửa thêm.

Ngoài phạm vi (user chốt "trên danh sách" → CHƯA đụng, chờ ý kiến nếu muốn đồng bộ):
- Khối ký cuối file Excel vẫn ghi "Người lập" (footer chứng từ, giống prepick — cố ý giữ).
- `ProductExportRequestForm.vue:564` (màn form/chi tiết) vẫn "Người lập".

### Kiểm thử Phase 4
- [ ] Danh sách hiện "Người tạo" (kể cả tài khoản đã lưu cấu hình cột cũ).
- [ ] Mở popup Xuất Excel: mặc định tick đúng cột đang hiện; ẩn 1 cột rồi mở lại → cột đó không tick sẵn.
- [ ] File tải về: cột đúng thứ tự tick, "Giá trị" là số SUM được, "Trạng thái" ra chữ.

### Checkpoint — 2026-09-22 (Phase 4)
Vừa hoàn thành: Đổi "Người lập"→"Người tạo" trên danh sách (bộ cột gốc) + fix đóng băng nhãn cho user đã lưu cấu hình (tách `baseTableColumns` + merge trong `defaultTableColumns`). Wiring mặc định xuất Excel theo cột đang xem (`exportFieldsMixin` + `:default-selected` + `exportFieldKeyMap`). Đã đối chiếu export-excel.js với màn chuẩn prepick — khớp. Verify: dev server HMR không lỗi ở file này, line ending LF giữ nguyên (0 CR).
Đang làm dở: (không)
Bước tiếp theo: User chạy thử 3 mục Kiểm thử Phase 4; chốt có đổi "Người lập" ở footer Excel + màn form không.
Blocked:
Đã commit + push `gop_db` (hrm-client `c49f03811`).

## Phase 5 — Feedback Redmine (2026-09-22): cắt lề 2 bên + khoảng trắng thừa trên tiêu đề (màn Tạo)
Nguồn: ảnh Redmine "Cắt bớt lề ở 2 bên và Khoảng trắng thừa trên tiêu đề". Chuẩn tham chiếu: `finance/bill-payment-requests/create`.

### FE — `pages/finance/product-export-requests/components/ProductExportRequestForm.vue`
- [x] Task 5.1: Wrapper ngoài `<div class="v2-styles min-vh-100 pt-2 per-form">` → bỏ `pt-2` (khoảng trắng thừa TRÊN tiêu đề). Khớp reference (wrapper reference không có padding top).
- [x] Task 5.2: `<div class="container-fluid px-3">` → `px-0` (cắt lề 2 bên). Reference dùng `container-fluid px-0`, card đi sát mép vùng nội dung.
- [x] Ghi chú: khối tiêu đề nhóm đã dùng `V2BaseFormSection` (card-header `section-header py-2`) — TRÙNG padding tiêu đề của reference, không cần sửa. Wrapper bọc cả nhánh Tạo/Sửa (`!readonly`) lẫn nhánh Chi tiết (`v-else`) → sửa 1 chỗ áp cho cả 3 mode, đồng nhất.
- [x] Verify Playwright MCP: mở `/finance/product-export-requests/create` vs `/finance/bill-payment-requests/create` → lề trái/phải + vị trí tiêu đề "Thông tin chung" trùng khớp. LF giữ nguyên (0 CR), dev HMR không lỗi.

### Checkpoint — 2026-09-22 (Phase 5)
Vừa hoàn thành: Cắt lề 2 bên (`px-3`→`px-0`) + bỏ khoảng trắng trên tiêu đề (`pt-2`) màn Tạo/Sửa/Chi tiết YCXH, khớp màn chuẩn bill-payment-requests/create. Đã đối chiếu ảnh Playwright 2 màn — trùng khớp.
Đang làm dở: (không)
Bước tiếp theo: User xác nhận; nếu OK thì commit + push (chưa commit Phase 5).
Blocked:
