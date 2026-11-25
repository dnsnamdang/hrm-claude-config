# Plan — Báo cáo bán hàng theo hàng hóa (@khoipv)

> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-11-23-bao-cao-ban-hang-theo-hang-hoa-design.md`
> Bám khuôn: `sale-by-product-report` (bộ lọc, phạm vi, In/Excel), `SaleSummaryGroupTable.vue` (bảng cây), `self-inventory-report` (popup + ServesDrillListPrint)

## Phase 1 — Port màn (23/11/2026)

### BE (hrm-api)
- [x] Quyền: thêm platform `hrm` cho `sale.bao_cao_ban_hang_theo_hang_hoa.view` (Catalog/sale.php)
- [x] `ProductClassTree` — lọc theo 4 cấp phân loại + option cây có cờ khoá
- [x] `SaleByGoodsReportService` — context/validate, 3 nhánh UNION ALL (+ HĐ HRM), cây nhóm, SL khách, phân trang nhóm cấp 0, filterOptions, itemList
- [x] `SaleByGoodsReportPrintService` + blade in / Excel + `SaleByGoodsReportExport` + drillList
- [x] Controller + route (checkPermission)
- [x] Smoke test HTTP kernel (dữ liệu phân loại tạm trong transaction, ROLLBACK)

### FE (hrm-client)
- [x] `pages/sale/sale-by-goods-report/index.vue` — bộ lọc (bắt buộc + báo đỏ), tải báo cáo, In / Excel, popup
- [x] `components/SbgSummary.vue`, `SbgTable.vue` (cây 2 tầng tiêu đề, ô chọn cấp), `SbgCustomerModal.vue`
- [x] Menu `sale-hub.js` → link + codes
- [x] Kiểm compile template + babel

Ghi chú làm:
- Excel bảng chính + popup dùng chung `DrillListExport` + `finance::exports.drill_list` (không tạo export/blade riêng); bản in dùng `finance::prints._layout`
- `ProductClassTree` mới (4 cấp, có Tính chất). `SaleByProductReportService` vẫn giữ bản 3 cấp riêng — chưa chuyển (sửa file màn khác → hỏi user)
- Kiểm: `php -l` OK; PHPUnit `Modules/Finance/Tests/Feature/SaleByGoodsReportApiTest.php` 7/7 (109 assertion, DatabaseTransactions — dữ liệu phân loại tạm, đã kiểm không sót);
  compile template + babel 4 file FE + `sale-hub.js` OK. CHƯA mở trình duyệt, CHƯA commit
- ⚠️ DB local: mã `sale.bao_cao_ban_hang_theo_hang_hoa.view` có sẵn nhưng `on_hrm = 0` → cần `php artisan permission:catalog-sync` (dry-run thấy local lệch Catalog rất nhiều mã khác → chưa chạy, chờ user). Dev/prod: `~/build_tpe.sh` tự sync. Mã chưa vai trò nào có → admin cấp ở `/admin/roles`
- ⚠️ Local 4 bảng phân loại rỗng, `products.product_type_id` toàn NULL → mở màn thật chỉ ra dữ liệu với "Báo cáo theo = Model"

### Checkpoint — 2026-11-23
Vừa hoàn thành: Phase 1 BE + FE màn Báo cáo bán hàng theo hàng hóa
Đang làm dở: — (CHƯA commit: hrm-api 5 file mới + `Routes/api.php` + `Catalog/sale.php`; hrm-client 4 file mới + `sale-hub.js`)
Bước tiếp theo: user chạy catalog-sync + cấp quyền → mở `/sale/sale-by-goods-report` kiểm trình duyệt → commit
Blocked:

### 2026-11-23 — Test Playwright trình duyệt (user yêu cầu)
- [x] Spec `e2e/tests/sale/sale-by-goods-report.spec.ts` (15 ca, chạy --headed) + fixture `e2e/utils/saleByGoodsFixture.ts` (vai trò tạm có mã, tạm bật on_hrm, nhánh phân loại tạm gắn 3 hàng đã bán; dọn theo id)
- [x] Sửa màn: nút reset panel lọc → "Xóa lọc" (skill report-styles §1, bỏ sót lúc dựng)
- Kết quả: 12/12 ca đã chạy tới đều QUA (01–12: mở màn, báo đỏ tại ô, Loại SP bắt buộc + 🔒, khớp API, ô chọn cấp, lọc dây chuyền,
  popup lọc/sắp/In/Excel, popup từ TỔNG + khối tổng hợp, Chi tiết theo Hãng SX / Thị trường, Model, In + Excel báo cáo chính).
  Ca 13 phần giữ bộ lọc khi rời màn QUA (lượt 7); 13 (Xóa lọc) – 14 (phạm vi công ty) – 15 (không quyền → 404) CHƯA chạy xong: máy hết RAM,
  hệ thống dừng nuxt dev + lượt test 8. Đã dọn tay dữ liệu tạm lượt 8 theo id (natures 33, fg 34, fam 33, types 57/58, role 100276, on_hrm=0)
- Lỗi gặp trong quá trình đều là lỗi test (helper select2 / kỳ vọng), trừ nút "Làm mới" → "Xóa lọc"
- Bẫy test: ô select2 CHỌN NHIỀU của V2BaseSelect không đóng bằng Escape — đóng bằng bấm ra chỗ trống; sắp xếp popup V2BaseReportModal bấm vào CHỮ tiêu đề (span.report-drill-sort)

### Checkpoint — 2026-11-23 (push)
Vừa hoàn thành: commit + push develop — hrm-api `fbc5b047f` (merge `88d6738c7`), hrm-client `91c629d70` (merge `ed1160c79`). Sau khi gộp remote: php -l + PHPUnit 7/7, compile FE OK
Đang làm dở: E2E ca 13 (Xóa lọc) – 14 (phạm vi công ty) – 15 (không quyền → 404) chưa chạy xong
Bước tiếp theo: dev deploy (`~/build_tpe.sh` tự chạy permission:catalog-sync) → admin cấp mã cho vai trò → QA; chạy nốt 3 ca E2E khi máy đủ RAM; merge gop_db khi user yêu cầu
Blocked:

### 2026-11-25 — Check: màn nào phải có quyền mới hiện menu (chỉ điều tra, KHÔNG sửa code)
- [x] Màn này: ẩn menu khi thiếu mã `sale.bao_cao_ban_hang_theo_hang_hoa.view` (hub `isScreenVisible` → `passesCodes`, fail-closed; sidebar dọc giữ `codes` qua `sale.js::toLeaf`); BE route gate cùng mã
- [x] Soát 102 màn có link của phân hệ Bán hàng (`sale-hub.js`): 23 màn gate quyền inline (`codes`/`isShow`), 69 màn hiện cho mọi người (đa số cố ý — quyền chỉ mở rộng phạm vi dữ liệu)
- [x] ⚠️ Phát hiện lệch: 10 màn chỉ khai quyền ở map `SALE_LINK_PERMISSIONS`/`SALE_LINK_CODES` (`sale.js`) → sidebar dọc ẩn đúng, nhưng HUB không đọc map → hiện cho cả người không quyền
  (YC giải pháp chờ duyệt, Báo giá chờ duyệt, Hạng mục/Giai đoạn/Vai trò dự án, Phiếu thu thập thông tin, Lý do thất bại, Loại tài liệu, Loại giảm giá, Cấu hình duyệt giá)
- [ ] Chờ user: có sửa lệch hub (khai inline ở `sale-hub.js` hoặc sửa hàm chung `hub.js`) / soát tiếp phân hệ khác không

### 2026-11-25 — Check: bộ lọc có lệch skill report-styles không (chỉ đọc code, KHÔNG sửa, chưa mở trình duyệt)
- [x] Đối chiếu `pages/sale/sale-by-goods-report/index.vue` với report-styles §1/§3/§5b: khớp floating · "Xóa lọc" · InfoTip · In/Excel `#header-actions` · ô Kỳ + Thời gian · `V2BaseCompanyDepartmentFilter` · `keepLockedOptions` · không tự đặt `col` · đổi ô là tìm
- [x] Điểm khác (không phải luật skill): ô Công ty–Phòng ban đứng CUỐI (màn mặt hàng đặt ngay sau Kỳ); cỡ trang 10 (skill §5b ghi 20, màn mặt hàng cũng 10)
- [ ] Chờ user chỉ chỗ thấy lệch trên trình duyệt

### 2026-11-25 — Check: bộ lọc ra dữ liệu để test local (chỉ đọc DB, KHÔNG sửa)
- [x] Local: 4 bảng phân loại rỗng → chỉ "Báo cáo theo = Model" dùng được; phiếu xuất chỉ tới 07/2026 → Kỳ "Tháng này" trống
- [x] Chạy `SaleByGoodsReportService::report()` (emp 13, scope all) Kỳ = Năm nay + Model: `ATP-35`/Phòng ban → 1 nhóm (SL bán 1.126, trả 10);
  `SJ/MA 20W40`/Hãng SX → 2 nhóm; `ATP`/Thị trường → 6 nhóm (có cả nhập trả lại)

### 2026-11-25 — Check: HRM ra số lớn hơn ERP cùng bộ lọc (Năm nay · Model ATP-35 · Phòng ban) — chỉ điều tra
- [x] Cùng DB `gop_db`. SL khách khớp (57/2/57); SL + giá trị HRM lớn hơn (Bán 1.126 vs 588, Nhập trả 10 vs 5)
- [x] Nguyên nhân: ERP `SaleProductReportService::getDataReport()` ghép 3 nhánh bằng `union()` (khử trùng) → các dòng phiếu giống hệt nhau
  (cùng hàng, SL, giá, công ty/PB/BP, tỉnh, hãng) bị gộp còn 1. Phiếu xuất ATP-35: 270 dòng / 825 cái thật → còn 58 dòng / 402 cái.
  Nhập trả: 6 phiếu thật = 10 cái / 600.000 → ERP 5 / 300.000. HRM dùng UNION ALL = số đúng (đã ghi "khác ERP có chủ đích" trong docblock service, user chốt 23/11)
- [x] Loại 21 (HĐ HRM) không đóng góp gì ở ca này → không phải nguyên nhân
- [x] User đồng ý sửa ERP: `erp/app/Services/Reports/SaleProductReportService.php::getDataReport()` nhánh mặc định `union` → `unionAll` (nhánh gốc gop_db, CHƯA commit).
  Kiểm: `php -l` OK; chạy lại service ERP cùng bộ lọc (2026-01-01 → 25/11, Model ATP-35, Phòng ban) → Bán 1.126 / 54.210.500, Nhập trả 10 / 600.000, Thực bán 1.116 / 53.610.500 = khớp HRM từng phòng ban. Màn / In / Excel ERP đều qua hàm này
