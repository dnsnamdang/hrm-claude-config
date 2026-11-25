# Plan — Báo cáo làm dịch vụ BH - SC - BD

## Phase 1 — BE (hrm-api, Modules/Sale)
- [x] Service `WarrantyRepairServiceReportService` (phạm vi 2 mã, lượt BH/SC/BD, cây nhóm ▸ hàng, summary, item-list, filter-options)
- [x] Print service (bản in bảng cây + Excel + drill list) dùng `finance::prints._layout` / `DrillListExport`; Excel `WarrantyRepairServiceReportExport` ghi STT / Mã hàng kiểu chữ
- [x] Controller + route `v1/sale/reports/warranty-repair-service` + `checkPermission` 2 mã
- [x] Catalog `sale.php`: thêm `hrm` vào `platforms` 2 mã
- [x] Smoke: service 6 kiểu Báo cáo theo khớp SQL độc lập (01/01/2025–31/12/2026: BH 3,598 / 2,527,332,593 · SC 1,866 / 6,035,975,587.5 · BD 990 / 1,589,802,300); Nhóm KH tổng không cộng trùng; popup = số của nút; 4 mức phạm vi; 422 thiếu Báo cáo theo; controller index / filter / item / print / export / item export / item print = 200; route 403 khi không quyền

## Phase 2 — FE (hrm-client)
- [x] `pages/sale/warranty-repair-service-report/index.vue` + `WrsSummary` + `WrsTable` + `WrsDocModal` (khuôn `sale-by-goods-report`)
- [x] Menu `sale-hub.js` → link + codes
- [x] Verify compile (vue-template-compiler + babel parse) — CHƯA mở trình duyệt

## Phase 3 — ERP (D:\laragon\www\erp, nhánh gop_db, không commit)
- [x] `WarrantyRepairService::getData()`: tách vật tư / dịch vụ, bảo dưỡng cộng mọi dịch vụ, bỏ JOIN nhóm KH (lọc / gom nhóm KH trong PHP), UNION ALL, SELECT part_id, sửa lệch thứ tự cột 2 vế UNION
- [x] `render()`: cộng SL (không ghi đè), so `tp`/`tpc`, dòng TỔNG cộng trên tập dòng chưa nhân nhóm
- [x] Đối chiếu ERP = HRM tháng 05/2026 (kỳ 2 năm ERP chạy quá lâu — vòng gom nhóm O(n²) có sẵn của ERP): Hãng SX 70 nhóm, Nhóm KH 110 nhóm,
  TỔNG BH 205 / 135,623,500 · SC 224 / 622,501,643.4 · BD 106 / 141,173,350 — 2 bên trùng khớp, cả dòng TỔNG Nhóm KH (không cộng trùng)

### Checkpoint — 2026-11-25
Vừa hoàn thành: BE + FE + sửa ERP, số liệu ERP = HRM = SQL độc lập.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm `/sale/warranty-repair-service-report` (cần tài khoản có 1 trong 2 mã — local chưa catalog-sync); commit khi user bảo.
Blocked:

## Phase 4 — E2E Playwright (user yêu cầu 25/11, chạy có mở trình duyệt)
- [x] Fixture `e2e/utils/warrantyRepairServiceFixture.ts` (vai trò tạm + cây Loại SP tạm, dọn theo id) + spec `e2e/tests/sale/warranty-repair-service-report.spec.ts` (17 kịch bản)
- [x] Đạt 01–07: mở màn / kỳ 05/2026 khớp API / phân trang 1 request / bung cấp + th dính / popup chứng từ (link, tìm, lọc KH, sắp) / In + Excel popup / popup từ TỔNG + khối tổng hợp
- [x] Lỗi gặp đều là lỗi TEST (không phải màn): đo nhầm lớp select2 con, icon ⓘ nhãn nổi đè điểm bấm, đo nhầm option ẩn trong tiêu đề, cuộn nhầm vỏ bảng, hasText "Khách hàng" khớp "Nhóm khách hàng"
- [x] 25/11 lượt 2 (chạy lại cả 17): user bảo DỪNG giữa chừng, không test tiếp — dọn tay role 100293, product_types 93/94, family 51, group 52, nature 51, 3 mặt hàng về NULL
- [ ] 08–17 chưa chạy xong (user dừng, không cần test nữa): lượt cuối bị hệ thống dừng vì máy hết RAM (dừng cả API :8000). Đã dọn tay dữ liệu tạm sót (role 100292, product_types 91/92, family 50, group 51, nature 50, 3 mặt hàng về NULL) — 2 dòng quyền 6112/6113 là dòng thật, giữ nguyên

## Còn lại
- [ ] User mở trình duyệt kiểm (local chưa `permission:catalog-sync` 2 mã → tài khoản thường bị 403; DB local còn lệch nhiều mã khác nên chưa chạy sync thật)
- [ ] Deploy: `php artisan permission:catalog-sync`; admin cấp 2 mã cho vai trò
