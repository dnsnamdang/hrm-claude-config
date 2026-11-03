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

## Tài liệu SRS / HDSD / Testcase (03/11/2026) @khoipv

Khuôn: `../finance-addition-accounting-request/` (gen_srs / gen_hdsd / gen_testcase / gen_checklist) + checklist "Mẫu tài liệu.xlsx".

- [x] Đọc code FE (`pages/lookup/product-arrived-notifies/**`, V2Base dùng chung) + BE (`ProductArrivedNotifySummaryService`, controller, print service, export) + design/spec
- [x] Chụp ảnh dev-hrm (DNS Admin) — `pbhv_shots/_capture/capture.js`: 3 tab, 3 bộ lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Xuất Excel, In, chi tiết Nhập khẩu / Mua ngoài, màn Thêm YCNH; 57 icon (trim_icon `--dry` 0/57). Nút Xóa / Tạo phân bổ chi phí bật tạm cờ trên trình duyệt (DNS Admin không có phiếu nhập khẩu tự tạo); chi tiết Trong nước là bố cục rỗng (DB chưa có phiếu trong nước). Không bấm Xóa / Lưu.
- [x] `gen_srs.py` → `SRS - Phiếu báo hàng về.docx`: 15 chức năng (3 tab danh sách, lọc, cài đặt bộ lọc, tùy chỉnh cột, xuất Excel, 3 màn chi tiết, xóa, in, xuất Excel 1 phiếu, tạo phân bổ chi phí, tạo phiếu YCNH), Phần 4 BR-01..BR-15, Phần 5 (2 bảng). Selfcheck khớp mẫu, 99 trang. Metrics: ui=12.9 ev=4.8 evch=1067 intro=1747, noBefore/noDuring=0.
- [x] `gen_hdsd.py` → `HDSD_Phieu bao hang ve.docx`: 9 PHẦN, 19 trang, không trang trắng.
- [x] `gen_testcase.py` → `testcase.xlsx`: 174 TC, P0 75 (43%), 10 nhóm (I Hiển thị · II Tìm kiếm và lọc + Cài đặt bộ lọc · III Xóa · IV Xem chi tiết · V Tùy chỉnh cột · VI Xuất Excel · VII Ảnh hưởng màn khác · VIII Phân quyền (duy nhất) · IX In phiếu · X Tạo phân bổ chi phí / YCNH); tc_engine sạch.
- [x] `gen_checklist.py` → `Đối chiếu checklist.xlsx`: Testcase 123 có TC / 201 N/A (Thêm mới, Chỉnh sửa, Khóa/Mở khóa, Lịch sử, Import, Duyệt, Không duyệt + vài dòng ràng buộc); SRS 99 có mục / 64 N/A.
- Lệch checklist / nghi lỗi ghi nhận (không sửa code): hộp xác nhận xóa không ghi mã phiếu; ký tự % _ là ký tự đại diện; bộ lọc nhớ theo trình duyệt không theo tài khoản; quay lại từ chi tiết về trang 1; Excel danh sách dùng logo cố định (không theo công ty); lọc Hợp đồng tab Mua ngoài chỉ khớp mã hợp đồng gốc (cột hiện mã phụ lục); dev: cột Nhà cung cấp tab Nhập khẩu trống ở mọi phiếu.

### Checkpoint — 2026-11-03 09:50
Vừa hoàn thành: bộ tài liệu SRS + HDSD + testcase + đối chiếu checklist màn Phiếu báo hàng về (chạy sạch 4 script).
Đang làm dở: không.
Bước tiếp theo: user xem lại tài liệu, quyết định có đẩy Drive không; chuẩn bị dữ liệu phiếu Trong nước để chụp lại ảnh chi tiết thật.
Blocked:

### Sửa Phần 5 SRS theo khuôn Drive (03/11/2026) @khoipv
- [x] Phần 5 đổi về khuôn các SRS phiếu đã duyệt trên Drive (folder SRS chuyển đổi — Phiếu thu tiền, Phiếu báo có, Yêu cầu xuất giữ…): tiêu đề "Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu", 1 câu dẫn + 1 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn (giải thích trong ngoặc ở cột Màn hình, đường dẫn "Phân hệ -> Nhóm"); bỏ bảng 7 cột + bảng 2
- [x] gen_checklist: dòng 161 → N/A (màn không có Khóa / Mở khóa), dòng 163 ghi chú lại; sinh lại SRS (selfcheck khớp bản mẫu) + Đối chiếu checklist
