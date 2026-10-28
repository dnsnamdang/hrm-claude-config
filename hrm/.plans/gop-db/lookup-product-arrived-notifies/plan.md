# Tổng hợp phiếu báo hàng về — Plan

> @khoipv · Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-14-lookup-product-arrived-notifies-design.md`

## Phase 1 — Màn tổng hợp 3 tab

### BE (hrm-api)
- [x] Quyền 1709–1711 (type 28) trong `PermissionsTableSeeder` + insert vào DB dùng chung
- [x] `Modules/Finance/Services/ProductArrivedNotifySummaryService.php`: search 3 tab (lọc, sort, phân trang, phạm vi tab Nhập khẩu), exportRows, meta, deleteImport
- [x] `ProductArrivedNotifySummaryController` + route `/v1/finance/product-arrived-notifies/*` + 3 khoá `ExportColumnRegistry`
- [x] Smoke test API bằng HTTP kernel (user 931 không quyền: import 7 phiếu; outside 747; inland 0; lọc NCC/hàng/ngày/công ty; export 200 xlsx; xoá id lạ / phiếu người khác → 409, phiếu còn nguyên)

### FE (hrm-client)
- [x] `pages/lookup/product-arrived-notifies/index.vue` (tab `?tab=`) + `components/ArrivedNotifyList.vue` (dùng chung 3 tab) + `tabConfigs.js`
- [x] Xuất Excel danh sách (ExportFieldsModal → BE `DynamicExport`)
- [x] Tab Nhập khẩu: cột Hành động (Xóa → API + confirm; In / Xuất Excel → ERP tab mới)
- [x] Menu `components/subsystem-menu/lookup.js` thêm link
- [x] Compile kiểm tra (vue-template-compiler + babel) + grep tự kiểm skill erp-to-hrm-screen
- [ ] User mở trình duyệt kiểm tra (chưa verify UI thật)

## Phase 2 — 3 màn chi tiết (user yêu cầu 14/10/2026 "port hết") — XONG code, chờ user kiểm trình duyệt

Nguồn ERP: `ProductArrivedNotify2Controller@show`, `InlandProductArrivedNotifyController@show`,
`ProductArrivedNotifiesController@show` + blade `show.blade.php` từng loại.

### BE
- [x] `GET /product-arrived-notifies/{tab}/{id}` — phạm vi xem = phạm vi danh sách (tab Nhập khẩu theo 3 quyền; 2 tab còn lại mở), ngoài phạm vi / không có → 404
- [x] Nhập khẩu: thông tin chung + hàng hoá (PI, model, code đặt hàng, chi tiết theo khách/đơn đặt hàng) + khuyến mại / bảo hành / thừa thiếu (lấy từ invoice như ERP)
- [x] Trong nước: thông tin chung + hàng hoá (chi tiết yêu cầu / khách / SL về)
- [x] Mua ngoài: thông tin chung + hàng hoá (khách, SL, SL nhập kho, chênh lệch) + khuyến mại
- [x] Cờ nút: `is_can_delete`, `is_can_import` (Nhập khẩu: Tạo phân bổ chi phí; Trong nước / Mua ngoài: Tạo YCNH)

### FE
- [x] 3 trang `pages/lookup/product-arrived-notifies/{import,inland,outside}/_id.vue` (V2BaseFormCard + CreatorInfoLine + V2Footer), 404 → `/pages/extras/404`
- [x] Danh sách: cột Mã chuyển sang `nuxt-link` HRM
- [x] Nhập khẩu footer: Xóa · In · Xuất Excel (khớp danh sách) + Tạo phân bổ chi phí (ERP)
- [x] Mua ngoài: "Tạo phiếu yêu cầu nhập hàng" → màn YCNH HRM, chọn sẵn loại 2 + phiếu nguồn (thêm đọc `?type=&source_id=&source_code=` ở `ProductImportRequestForm.vue`)
- [x] Trong nước: "Tạo yêu cầu nhập hàng" → ERP (loại 12 HRM chưa hỗ trợ)
- [x] Compile + smoke API
- [x] (user 14/10) Bỏ ô Trạng thái trong card Thông tin chung; header card theo khuôn PXG (`product-exports/_id`): 1 card "Chi tiết" + tab con `pi-top-tabs` (Hàng hóa / Khuyến mại / Hàng bảo hành / Hàng thừa thiếu), tiêu đề không đánh số
- [x] (user 14/10, lần 2) Card đổi sang `V2BaseFormSection` (header trắng) theo màn chuẩn `finance/bill-adjust-depts/{id}`; bảng theo `.accounting-table` (thead không nền, th 12px, td 13px); lưới ô `mb-3`
- [x] (user 14/10) Bỏ badge trạng thái trên tiêu đề màn chi tiết (`detailPageMixin.pageTitle` không còn `buildStatusTitle`)
- [x] (user 14/10) Khoảng cách dòng ô về lại `mb-2` + ghi quy tắc vào skill `erp-to-hrm-screen` (checklist D)
- [x] (user 14/10) "Nhập thẳng" / "Nhập xuất thẳng" thành checkbox disabled như ERP; Ghi chú lên cùng dòng Dự kiến về kho (Nhập khẩu, Mua ngoài)
- [x] (user 14/10, phiếu 561) Ô SL tab Khuyến mại / Bảo hành / Thừa thiếu hiển thị y hệt ERP: SL + "Hợp đồng:" + "Phụ lục <mã>:" không kèm số

## Phase 3 — In / Xuất Excel 1 phiếu Nhập khẩu theo skill print-page + export-excel (user 14/10/2026)

Nguồn ERP: `ProductArrivedNotify2Controller@print` (mẫu `report_templates` 213, khổ ngang) + `@export`
(`ProductArrivedNotify2Export` + blade `reports/exports/product_arrived_notify2_export`), dữ liệu `getPrintData()`.

### BE
- [x] `ErpReportTemplate::PHIEU_BAO_HANG_VE = 213`
- [x] `ProductArrivedNotifyImportPrintService`: placeholder in (`getProductTable`) + Excel (`getProductTableExcel`), HEADER theo `company_id` trên phiếu (trait `PrintsCompanyLetterhead`), SO_INVOICE = mã invoice (ERP điền nhầm mã HĐ)
- [x] `GET /product-arrived-notifies/import/{id}/print-data` + `GET …/import/{id}/export` (cùng phạm vi xem với chi tiết)
- [x] `Modules/Finance/Exports/ProductArrivedNotify2Export` + blade `finance::exports.product_arrived_notify2` (số thô + data-format, WithColumnWidths, letterhead WithDrawings)
- [x] Verify: in 562 (người tạo 639) → letterhead `companies.header` công ty trên phiếu (curl 200), 0 placeholder sót; người ngoài phạm vi 404. Excel 562: ô SL kiểu `n` `#,##0`, 1 drawing letterhead, bề rộng A..I đúng. CHƯA mở trình duyệt.

- [x] (user 14/10) Excel xấu — nhãn "Số invoice" ngắt 2 dòng vì nằm ở cột STT rộng 6: thông tin chung đổi sang 2 cặp nhãn–giá trị/dòng, nhãn gộp A:B / F:G, giá trị C:E / H:I; tự tính chiều cao dòng cho ô gộp nhiều dòng chữ (`fitRowHeights`) — Excel không tự giãn ô gộp

### FE
- [x] Danh sách tab Nhập khẩu + màn chi tiết: In → popup `ReportPrintPreviewModal` (khổ ngang), Xuất Excel → `downloadExcel` (bỏ mở ERP)

### Checkpoint — 2026-10-14 (Phase 2)
Vừa hoàn thành: 3 màn chi tiết (`import|inland|outside/_id.vue` + `detailPageMixin.js`), API `GET /{tab}/{id}`, cột Mã danh sách → link HRM, form YCNH nhận `?type=&source_id=&source_code=`. Smoke API: 562 (người tạo 639) đủ hàng/khuyến mại/bảo hành; Mua ngoài có phụ lục OK; ngoài phạm vi / không tồn tại → 404.
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt kiểm 3 màn chi tiết + nút Tạo phiếu YCNH (cần restart nuxt nếu route mới chưa nhận); admin gán quyền 1709–1711 (tài khoản Super admin HRM hiện chưa có → tab Nhập khẩu trống).
Blocked:

## Fix Redmine #11738 — Chỉnh sửa giao diện (2026-10-17)

- [x] BUG 1: cột Ngày tạo danh sách (3 tab) + Excel danh sách hiện thêm giờ phút `d/m/Y H:i` (BE `present()`), nới cột 110 → 140px
- [x] BUG 2: màn chi tiết Mua ngoài — dấu (*) cho Số hợp đồng / Kho nhập / Dự kiến về kho (giống ERP)
- [x] BUG 3: "Tên khách:" / "Ngày cần:" (+ "Ghi chú:") in đậm hơn — Mua ngoài + Nhập khẩu
- [x] BUG 4: màn chi tiết Nhập khẩu — dấu (*) cho Số Invoice / Kho nhận / Dự kiến về kho
- [x] Verify: php -l, compile template 2 màn + parse tabConfigs; created_at DB có giờ (PBHV-02689 17:38). CHƯA mở trình duyệt.
- [x] Rà kỹ (17/10): nhãn (*) khớp ERP `product_arrived_notifies/show` + `product_arrived_notify2/show` (Trong nước ERP không có *); API 3 tab + sort asc/desc + Excel danh sách ra `d/m/Y H:i`, Excel tự giãn cột; độ rộng cột lấy từ mặc định (user chỉ lưu ẩn/hiện); `<b>` toàn cục bị ép 500 (`_reboot.scss`) → rule mới 700 đậm hơn thật, SCSS compile OK. Playwright bị khoá → CHƯA mở trình duyệt.
