# Plan — Báo cáo theo dõi lắp đặt - bàn giao - SC - BD (@khoipv)

## Phase 1 — Port màn

### Khảo sát
- [x] T1. Đọc ERP controller / service / blade / class JS; ghi bảng nghiệp vụ vào spec
- [x] T2. Đo dữ liệu thật (3 nhánh, 1 GV ↔ 1 PCT/NKQ/DKQ, người tạo PCT + nhân sự lưu `employee_infos.id`)
- [x] T3. Hỏi user: quyền / ô lọc chết / In-Excel / giao diện → chốt (spec mục 1)

### BE (hrm-api `Modules/CustomerCare`)
- [x] T4. `InstallDeliveryRepairReportService`: query dòng (3 nhánh), lọc nhóm + dòng, gom nhóm, summary, phân trang, item-list, filter-options
- [x] T5. Controller + route `/v1/customer-care/report/install-delivery-repair*`
- [x] T6. PrintService + blade in (summary / detail, chọn cột)
- [x] T7. Export Excel báo cáo + danh sách popup (letterhead, khuôn export-excel)
- [x] T8. Smoke test HTTP kernel: index / filter-options / item-list / print / export

### FE (hrm-client)
- [x] T9. `pages/customer-care/report/install-delivery-repair/index.vue` + api/format + DrillNum/InfoTip (copy template)
- [x] T10. `ReportSummary.vue` (2 khối) + `ReportTable.vue` (cây 2 cấp) + `ItemListModal.vue`
- [x] T11. Link menu CSKH › Báo cáo
- [x] T12. Verify compile (vue-template-compiler + babel parse) 8/8 file sạch; HTTP thật 401/200; trang Nuxt 200
- [x] T12b. Viết e2e `e2e/tests/customer-care/install-delivery-repair-report.spec.ts` (16 test, chỉ đọc). Lượt 1: test 01 fail do kỳ vọng sai (dòng TỔNG viết HOA bằng CSS) -> đã sửa test; lượt 2: test 06 bắt nhầm response trễ của ô "Từ" -> sửa chờ đúng response có to_date. Lượt 3 (14/11): 15/16 ĐẠT; test 16 phần Xóa lọc đạt, chỉ vướng lỗi console HMR Nuxt dev (`hot-update.json timed out`, không phải lỗi màn) -> đã lọc trong test, CHƯA chạy lại sau khi lọc. Không phát hiện lỗi code màn.
- [ ] T13. User tự bấm trình duyệt (chưa kiểm chứng bằng mắt: bố cục bảng cây, popup drill, in, Excel tải về)

### Checkpoint — 2026-11-14
Vừa hoàn thành: BE (service + print + export + route) + FE (index, ReportSummary, ReportTable, ItemListModal, DocCell, format/api) + menu.
Đo: index ~2s (6.432 chứng từ / 6.942 phiếu), filter-options ~1,4s, item-list ~1,7s; Excel 1 tháng 4s, toàn bộ 14s; in vượt trần 2.000 dòng -> chặn.
Gotcha đã gặp: `employee_assign_task_progress` không có index (whereExists 16s -> whereIn subquery); Excel blade FromView 235s -> PhpSpreadsheet trực tiếp 14s;
Carbon::parse 28k lần 3,7s -> tách chuỗi.
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt `/customer-care/report/install-delivery-repair` kiểm bố cục / popup / in / Excel. Code CHƯA commit.
Blocked:

## Phase 2 — Màn CHI TIẾT (port ERP `customerCareReport.reportInstallDeliveryRepairDetail`) — 2026-11-14

User chốt 14/11: không phân quyền · tab SC-BD / Bảo hành vẫn bắt buộc 1 HĐ nhưng CHỌN từ ô tìm HĐ DV · có In + Xuất Excel ·
lỗi số liệu ERP GIỮ Y ERP (ô "SL đã duyệt KQ" tab Lắp đặt + SC không bấm được; popup duyệt KQ tab Bảo hành liệt kê phiếu NKQ;
vật tư bảo dưỡng = 0, SL PCT bảo dưỡng cộng đôi).
Route FE `/customer-care/report/install-delivery-repair-detail` · BE `/v1/customer-care/report/install-delivery-repair-detail*`.

### BE (hrm-api `Modules/CustomerCare`)
- [x] P2-T1. `InstallDeliveryRepairDetailReportService`: tab install (HĐ bán, phân trang 20 HĐ) · tab repair / warranty (1 HĐ DV,
      cây Sửa chữa / Bảo dưỡng / Bảo hành) · drill 8 loại popup · tìm HĐ DV · filter-options
- [x] P2-T2. Controller + route
- [x] P2-T3. In (print-list-data: bảng tab đang xem chọn cột / danh sách popup) + Excel (bảng tab / danh sách popup)
- [x] P2-T4. Smoke test HTTP kernel + đối chiếu số với hàm ERP trên vài HĐ

### FE (hrm-client)
- [x] P2-T5. `pages/customer-care/report/install-delivery-repair-detail/index.vue` (3 tab, SmartFilterPanel / tab, chọn HĐ, chọn hàng)
- [x] P2-T6. `DetailTreeTable.vue` (cây rsum-tb chung 3 tab) + `DetailDrillModal.vue` (popup theo loại)
- [x] P2-T7. Link menu CSKH › Báo cáo
- [x] P2-T8. Verify compile + HTTP thật
- [ ] P2-T9. User tự bấm trình duyệt 3 tab (chưa kiểm chứng bằng mắt: bố cục cây 5 cấp, ô chọn HĐ, popup, In, Excel)

### Checkpoint — 2026-11-14 (Phase 2)
Vừa hoàn thành: BE service/print/export/controller/route + FE index/DetailTreeTable/DetailDrillModal + menu.
Kiểm: số liệu khớp ERP 100% (851 dòng lắp đặt, 54 HĐ SC-BD/BH — gọi thẳng controller ERP cùng DB); smoke HTTP mọi endpoint 200,
Excel toàn bộ 14s; compile vue-template-compiler + babel 6/6 file sạch; Nuxt trả 200.
Đang làm dở: không.
Bước tiếp theo: user mở `/customer-care/report/install-delivery-repair-detail` bấm thử. Code CHƯA commit.
Blocked:
- [x] P2-T10. E2E Playwright `e2e/tests/customer-care/install-delivery-repair-detail-report.spec.ts` (17 test, chỉ đọc): 17/17 qua (6 phút). 2 lần đỏ đầu do test (đo tiêu đề tính cả chữ ô chọn cấp; đọc ô HĐ lúc "Đang tìm..."), không sửa code màn. Test 15 lấy HĐ bảo hành có SL duyệt KQ từ DB để bắt buộc bấm popup duyệt KQ.
- [x] P2-T11. Push develop 14/11 (user yêu cầu): hrm-api `6fa8d92b9` + hrm-client `44518bef6` (Phase 1 + 2). Kèm commit riêng của màn Bán hàng theo mặt hàng (api `68ff7041e`, client `ccf56257e`, gồm slot `pagination` của V2BaseReportModal).
