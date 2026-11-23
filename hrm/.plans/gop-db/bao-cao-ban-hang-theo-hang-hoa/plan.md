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
