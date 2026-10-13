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

### Checkpoint — 2026-10-13
Vừa hoàn thành: BE + FE code xong, đã push develop (api 6f573d9fe, client 75edefacc), smoke test API pass, compile FE pass.
Đang làm dở: không.
Bước tiếp theo: user mở `/admin/benefit-rates` kiểm giao diện (lọc, popup chọn nhiều nhóm, lịch sử, xuất Excel).
Blocked:
