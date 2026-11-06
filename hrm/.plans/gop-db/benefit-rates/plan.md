# Plan — Hệ số công nghệ theo nhóm hàng hóa (@khoipv)

## Phase 1 — Port màn
### BE (`hrm-api/Modules/CustomerCare`)
- [x] Entity `BenefitRate` + `BenefitRateHasGroupProduct` (bảng ERP, khai `$table`)
- [x] `BenefitRateService` (index theo công ty, store/update/destroy, sync nhóm, lịch sử catalog_histories)
- [x] `BenefitRateRequest` (validate như ERP), `BenefitRateResource`
- [x] Controller + routes `/customer-care/benefit-rates` (không checkPermission)
- [x] Đăng ký `CatalogHistoryService::TABLES['benefit_rates']` + `ExportColumnRegistry['benefit_rates']`
- [x] Smoke test API qua HTTP kernel: 16 ca pass (422 đủ 3 ô, trùng tên, trùng nhóm, hệ số âm/3 số lẻ,
      tạo/sửa/xem/xoá, xoá lần 2 → câu xung đột, lịch sử create+update, export, bản ghi công ty khác → 404/400). Dữ liệu test đã dọn.
### FE (`hrm-client`)
- [x] `pages/admin/benefit-rates/index.vue` (khuôn note-maintenances) + `components/BenefitRateModal.vue` (khuôn DistrictModel)
- [x] Menu `components/subsystem-menu/admin.js` dưới "Danh sách loại phiếu hạch toán"
- [x] Compile FE (vue-template-compiler + babel) + grep tự kiểm skill erp-to-hrm-screen: sạch
- [ ] User mở trình duyệt kiểm (chưa bấm thật)

## Fix — Logo Excel to hơn bảng (13/10, user báo)
- [x] Nguyên nhân: xuất qua `DynamicExport` (blade `exports.dynamic` chèn ảnh tĩnh cỡ gốc) — bảng 8 cột hẹp hơn ảnh
- [x] Chuyển sang khuôn chung `utils/export/listExportFile.js` (letterhead công ty trải bằng bề rộng bảng): BE `GET /export-rows` (`BenefitRateService::exportRows()`), bỏ `/export` + mục `ExportColumnRegistry`; FE `runExport` → `exportListFile` + dòng tiến độ
- [x] Smoke test `export-rows` (đủ cột / theo `fields`), compile FE
- [x] Đã push develop (api d76b5c746, client 95d1ba3d7)
- [ ] User xuất thử trên trình duyệt xem logo
- ⚠️ Lúc dọn dữ liệu test đã xoá nhầm log "Tạo mới" của bản ghi "Hệ số 1" (id 3) do user tạo → đã khôi phục nguyên văn từ binlog (catalog_histories id 739)

## Fix — Redmine #11705 Lỗi UI/UX (15/10)
- [x] Bug 1a: bỏ nút lọc ở hàng tiêu đề file Excel — truyền `autoFilter: false` (tuỳ chọn mới của listExportFile.js, 15/10)
- [ ] Bug 1b: dời khối Người lập — chưa làm (user chưa yêu cầu)
- [x] Bug 2: popup Tạo mới khớp ERP — title "… tỷ lệ hưởng công khoán", nhãn "Loại tỷ lệ hưởng"
- [x] Bug 3: thêm ô lọc Công ty — giống ERP (lọc company_id AND vẫn bó công ty người đăng nhập)
- [x] Bug 4: "Người sửa/Ngày sửa" → "Người cập nhật/Ngày cập nhật" (cột bảng, ô lọc, file xuất)
- [x] Verify: compile FE + php -l sạch; smoke test lọc công ty (không lọc 1 / công ty mình 1 / công ty khác 0), tiêu đề file xuất đã đổi
- [ ] User mở trình duyệt kiểm (chưa bấm thật)

### Checkpoint — 2026-10-13
Vừa hoàn thành: BE + FE code xong, đã push develop (api 6f573d9fe, client 75edefacc), smoke test API pass, compile FE pass.
Đang làm dở: không.
Bước tiếp theo: user mở `/admin/benefit-rates` kiểm giao diện (lọc, popup chọn nhiều nhóm, lịch sử, xuất Excel).
Blocked:


## Dời menu sang Bán hàng (15/10)
- [x] Gỡ mục khỏi `components/subsystem-menu/admin.js`, thêm vào `sale-hub.js` › Quy chế - Thiết lập › Thiết lập (route giữ `/admin/...`)
- [ ] User mở trình duyệt kiểm sidebar Bán hàng

## Tài liệu SRS / HDSD / Testcase (06/11/2026) @khoipv
- [x] Đọc code FE (`pages/admin/benefit-rates/**`) + BE (`Modules/CustomerCare` BenefitRate*), xác nhận: màn DANH MỤC, KHÔNG gắn quyền, phạm vi theo công ty; không có Khóa / Import / In
- [x] Grep màn đọc ngược hệ số: chỉ form Duyệt kết quả của Phiếu nhập kết quả (`WrApproveResultSourceService::productCoefficient`, dòng lắp đặt); Phiếu giao việc HRM lấy `tech_coefficient` của hàng (không đọc bảng này); `chan-lap-hd-chua-he-so-dstc` là hệ số DSTC (bảng khác) — không liên quan
- [x] Chụp ảnh dev-hrm (`hscn_shots/_capture/capture.js`): 18 ảnh + 43 icon, đã trim_icon (Cần cắt 0). Dev chưa có hệ số cho công ty DNS Admin → danh sách / Sửa / Xem / Lịch sử là DỮ LIỆU GIẢ trên trình duyệt (12 hệ số); ảnh lỗi trùng `10e_duplicate`: yêu cầu Lưu bị chặn, lỗi trả giả trên trình duyệt. Yêu cầu ghi tới máy chủ: 0 (1 POST bị chặn tại trình duyệt)
- [x] `gen_srs.py` → SRS 10 chức năng, 65 trang, selfcheck khớp mẫu; metrics ui=12.3 ev=4.6 evch=968 intro=1597
- [x] `gen_hdsd.py` → HDSD 9 phần, 15 trang
- [x] `gen_testcase.py` (loai=danh_muc) → 187 TC, 11 nhóm, P0 42.8%, check_tc 0 lỗi
- [x] `gen_checklist.py` → Testcase 215 có TC / 109 N/A (Lưu nháp-gửi duyệt, Khóa, Import, Duyệt); SRS 131 / 32 N/A (Khóa, Import)

### Checkpoint — 2026-11-06
Vừa hoàn thành: đủ bộ SRS + HDSD + Testcase + Đối chiếu checklist màn Hệ số công nghệ theo nhóm hàng hóa.
Đang làm dở: không.
Bước tiếp theo: user xem tài liệu; quyết định có báo các điểm nghi lỗi (câu lỗi bắt buộc lệch dấu chấm, popup Xem hiện "1.5", xóa dòng cuối trang cuối) không.
Blocked:
