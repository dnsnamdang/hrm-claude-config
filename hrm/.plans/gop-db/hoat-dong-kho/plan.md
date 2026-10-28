# Plan — Hoạt động kho

> Phụ trách: @khoipv · nhánh `develop` (con của `gop_db`, cả hrm-api + hrm-client)
> Port ERP `warehouseInfo.activities` (Kho › Hoạt động kho) → HRM `/warehouse/activities`.
> Khuôn: màn chỉ đọc cùng controller ERP "Danh sách hàng mượn" (`pages/finance/borrow-stocks`), Excel theo
> `pages/warehouse/self-inventories/components/export-excel.js`, khối tổng hợp theo `self-inventory-report`.

## Quyết định (user chốt 26/10/2026)

- Quyền: KHÔNG gate quyền, y ERP. Phạm vi = kho mình là thủ kho (`warehouse_stockers`), Super Admin mọi kho.
- Realtime ERP đã chết (socket bị comment) → port ô tổng hợp + tô màu theo thời gian chờ, tự tải lại 60 giây.
- Bộ tối thiểu HRM: ô tìm nhanh mã phiếu, Cấu hình cột, Xuất Excel. Không phân trang, không lọc nâng cao.
- Cột "Phiếu đề nghị" link sang màn HRM (ĐNXK `/finance/warehouse-export-requests/{id}`, ĐNNK `/warehouse/import-requests/{id}`), tab mới.

## Phase 1 — Port màn

### BE
- [x] `WarehouseActivityService` — UNION ĐNXK + ĐNNK y `Warehouse::getActivities()` ERP, keyword, sort whitelist, summary
- [x] `WarehouseActivityController` + route `GET /v1/finance/warehouse-activities` (không checkPermission)
- [x] Đối chiếu số dòng với SQL ERP nguyên văn

### FE
- [x] `pages/warehouse/activities/index.vue` (bảng + tìm nhanh + cấu hình cột + tự tải lại 60s + tô màu dòng)
- [x] `components/ActivitySummary.vue` (Tổng phiếu nhận / Hoàn thành / Chưa xử lý)
- [x] `components/export-excel.js` (letterhead + khối ký)
- [x] Menu Kho › mục "Hoạt động kho"
- [x] Compile + gọi API kiểm

### Checkpoint — 26/10/2026
Vừa hoàn thành: BE + FE Phase 1. Số dòng khớp SQL ERP nguyên văn trên DB local (Super Admin 219 = 173 ĐNXK + 46 ĐNNK; thủ kho kho 2 = 128);
keyword + sort qua HTTP kernel 200 (~250-420ms); nhánh "Đã hoàn thành" + "Tổng thời gian xử lý" thử bằng dòng giả (DB không có phiếu xong trong ngày).
FE parse sạch (vue-template-compiler + babel), grep tự kiểm của skill sạch.
Đang làm dở: —
Bước tiếp theo: user bật dev server, mở `/warehouse/activities` bấm thật (tìm nhanh, sort, Cấu hình cột, Xuất Excel, link mã phiếu, tô màu dòng, tự tải lại 60s) → review → commit.
Blocked: dev server cổng 3000 đang tắt → chưa mở trình duyệt kiểm.

## Fix #11894 — Đặt lại màu danh sách (28/10/2026)

User chốt 28/10: KHÔNG tô cả dòng (cả bảng hồng vì đa số phiếu quá 20 phút) — nền trắng như mọi danh sách, đánh dấu bằng vạch màu mép trái dòng (vàng quá 10 phút / đỏ quá 20 phút / xanh hoàn thành — màu ERP `calculateClass`).

- [x] FE: scss chung `components/warehouse/activity/activity-row-marks.scss` — vạch 3px mép trái theo `row-wait-warn` / `row-wait-late` / `row-done`
- [x] FE: `pages/warehouse/activities/index.vue` + `pages/warehouse/warehouse-tracking/_id/index.vue` bỏ nền dòng, import scss chung
- [x] FE: chấm chú thích `ActivitySummary` đổi theo màu vạch
- [x] Verify: compile FE

### Checkpoint — 28/10/2026 17:30
Vừa hoàn thành: #11894 — bỏ nền dòng, vạch 3px mép trái (scss chung `activity-row-marks.scss`, import ở Hoạt động kho + Theo dõi kho), chấm chú thích cùng màu. Compile template 3 file + node-sass file mới OK.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt xem màu (chưa kiểm bằng trình duyệt).
Blocked:

## Fix #11895 — Xuất Excel: giãn dòng để thấy hết chữ (28/10/2026)

- [x] FE `components/warehouse/activity/export-excel.js`: mọi ô bật wrapText; chiều cao dòng tiêu đề + dòng dữ liệu tính theo số dòng chữ ước lượng từ độ rộng cột (bỏ `height = 22` cứng làm cắt "Thời gian lấy/xếp hàng")
- [x] Verify: dựng file bằng node (exceljs) với dữ liệu dài, đọc lại chiều cao dòng

### Checkpoint — 28/10/2026 17:45
Vừa hoàn thành: #11895 — `export-excel.js` (dùng chung Hoạt động kho + Theo dõi kho): mọi ô wrapText, `fitRowHeight()` ước lượng số dòng chữ theo độ rộng cột cho dòng tiêu đề + từng dòng dữ liệu. Dựng thử bằng node: tiêu đề 34pt (2 dòng), dòng dài 34pt, dòng ngắn 19pt.
Đang làm dở: —
Bước tiếp theo: user tải file trên trình duyệt mở bằng Excel kiểm.
Blocked:

## Fix #11904 — Bấm sort danh sách vỡ layout (28/10/2026)

- [x] FE `activity-table.js` `activityColumns()`: mọi cột khai width + minWidth (khuôn #11763), cột chữ dài xuống dòng trong ô — dùng chung Hoạt động kho + Theo dõi kho
- [x] Verify: compile FE

### Checkpoint — 28/10/2026 18:00
Vừa hoàn thành: #11904 — `activityColumns()` khai width + minWidth mọi cột (khuôn #11763), cột chữ dài `text-wrap`, nới 3 cột thời gian để tiêu đề + mũi tên sort đủ 1 dòng. BE sort đã có cột phụ (position → received_time → id) nên thứ tự ổn định. Cấu hình cột đã lưu chỉ giữ isVisible ⇒ không đè width. Parse OK.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt bấm sort kiểm (chưa xem video screenpal — không tải được).
Blocked:

### Checkpoint — 28/10/2026 (wrap up)
Vừa hoàn thành: fix #11894 #11895 #11904 ĐÃ PUSH `develop` 28/10 (hrm-api tới `ddd23d04c`, hrm-client tới `f8f362a51`).
Đang làm dở: —
Bước tiếp theo: QA kiểm lại trên dev, đóng issue Redmine.
Blocked:
