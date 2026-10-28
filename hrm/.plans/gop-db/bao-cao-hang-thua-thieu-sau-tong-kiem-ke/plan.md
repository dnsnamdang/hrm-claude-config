# Plan — Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa

> Phụ trách: @khoipv · nhánh `develop` (con của `gop_db`, cả hrm-api + hrm-client)
> Port ERP `warehouseReport.selfInventoryReport` → HRM `/warehouse/self-inventory-report`.
> Khuôn: màn anh em "Báo cáo tồn kho tổng hợp theo mặt hàng" (`/warehouse/stock-general-product`) — bảng `rsum-tb` phẳng.

## Phase 1 — Port màn

### BE
- [x] Khảo sát ERP: route / controller / `SelfInventory::reportSearchData` / blade / Excel `SelfInventoryReportExcel` / mẫu in #393
- [x] `SelfInventoryReportService` (options, plans, report) — số y ERP
- [x] `SelfInventoryReportPrintService` + view in + Excel export + blade
- [x] Controller + route `/v1/finance/self-inventory-report` (`/`, `/options`, `/plans`, `/print-list-data`, `/export`) — không checkPermission
- [x] Đối chiếu số với hàm ERP gốc trên cùng DB

### FE
- [x] `pages/warehouse/self-inventory-report/index.vue` + `components/` (Summary, Table)
- [x] `PlanPickerModal` (self-inventories) thêm prop `api` / `title` / `subtitle` để dùng lại (mặc định giữ nguyên)
- [x] Menu Kho › Báo cáo kho gắn link
- [x] Compile + gọi API kiểm

### Checkpoint — 25/10/2026 21:20
Vừa hoàn thành: BE + FE Phase 1. Số khớp SQL ERP nguyên văn trên DB local (4 dòng: 1 thừa SL 1, 3 thiếu SL 5); options/plans/422/print/export gọi qua HTTP kernel 200; Excel mở được (letterhead, 7 cột, khối ký Người lập); FE compile sạch, trang dev 200.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt bấm thật (lọc từng ô, popup kế hoạch / hàng hóa, In, Excel) → review → commit.
Blocked: DB local không có Kế hoạch tổng kiểm kê nào (`self_inventory_request_alls` rỗng) → popup kế hoạch chưa test được với dữ liệu.

## Phase 1b — Test Playwright (25/10/2026, user yêu cầu)

- [x] Vào màn: đúng khuôn, 0 lỗi console; chưa chọn ngày → bảng nhắc, không gọi API
- [x] Bấm Tìm kiếm khi trống → 2 ô ngày báo đỏ cùng lúc, không gọi API
- [x] Gõ tay 01/01/2020 – 31/12/2026 → 1 request, 4 dòng, tổng hợp 1 thừa / SL 1 · 3 thiếu / SL 5 (khớp SQL ERP)
- [x] F5 → bộ lọc còn nguyên
- [x] Kho vật lý = SG → `warehouse_ids=4`, 0 dòng; ô Công ty thuê thu về TPE/TPSG của kho SG
- [x] Công ty thuê = TPSG (không chọn kho) → `company_rental_ids=4`, 4 dòng
- [x] Hàng hóa qua popup dùng chung → `product_id=10975`, 1 dòng
- [x] Popup Kế hoạch tổng kiểm kê mở đúng tiêu đề + API mới (DB local không có kế hoạch tổng → bảng rỗng)
- [x] In: bỏ hết cột → báo đỏ, không gọi BE; bỏ Model + Phiếu kiểm kê → `cols` đúng, bản xem trước đúng 4 cột + letterhead + khối ký
- [x] Xuất Excel từ UI: tên file y ERP, đủ 7 cột, đúng bộ lọc
- [x] Link Phiếu kiểm kê → `/warehouse/self-inventories/575`, tab mới
- [x] Đến ngày < Từ ngày → bảng báo lý do, không gọi API
- [x] Xóa lọc → xoá hết ô (kể cả 2 ngày, như ERP)
- [x] Menu Kho › Báo cáo kho dẫn đúng trang
- [x] Hồi quy: popup kế hoạch ở màn Thêm phiếu kiểm kê vẫn gọi `self-inventories/plans`, tiêu đề cũ
- [x] Sửa sau test: thu hẹp cột (tổng 1150px) để cột Phiếu kiểm kê không bị đẩy ra ngoài ở 1440px; câu ghi chú popup In nói "trên popup" → truyền `note` riêng

## Fix #11886 — đồng bộ UI bộ lọc (28/10/2026)

- [x] BE: `context()` lọc theo `period` (trait `ResolvesReportPeriod`: week | month | last_month | year | custom from/to) thay cho `date_from`/`date_to`; meta vẫn trả `date_from`/`date_to` (in / Excel không đổi)
- [x] FE: ô Kỳ (select) + ô Thời gian (date-range khi Tuỳ chọn) như `transport/arrange-reports/by-supplier`, mặc định Tháng này
- [x] FE: ô Kế hoạch tổng kiểm kê + Hàng hóa hiện chữ thường + dấu x riêng (khuôn Tồn kho tổng hợp #11874), bỏ chip
- [x] FE: Công ty thuê kho hiện TÊN công ty; bỏ tooltip (hint) của ô
- [x] Verify: compile FE + gọi API qua HTTP kernel

### Checkpoint — 28/10/2026 10:10
Vừa hoàn thành: #11886 — BE `context()` dùng trait `ResolvesReportPeriod`; FE ô Kỳ + Thời gian (Tuỳ chọn), ô Kế hoạch / Hàng hóa chữ thường + dấu x, Công ty thuê hiện tên, bỏ tooltip. HTTP kernel: month/year 200, custom 2020–2026 ra 4 dòng (khớp số cũ), custom thiếu `to` / ngược → 422, export xlsx 200, print 200. FE template + script compile sạch.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm UI (chưa test Playwright) → commit.
Blocked:

### Checkpoint — 28/10/2026 (wrap up)
Vừa hoàn thành: fix #11886 ĐÃ PUSH `develop` 28/10 (hrm-api tới `ddd23d04c`, hrm-client tới `f8f362a51`).
Đang làm dở: —
Bước tiếp theo: QA kiểm lại trên dev, đóng issue Redmine.
Blocked:
