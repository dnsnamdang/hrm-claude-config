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

## Fix #12095 — sắp xếp lại bộ lọc / khối tổng hợp / bảng cây (10/11/2026)

User chốt: làm cả cây nhóm Công ty thuê kho → Kho → Hàng (mục 3).

- [x] (1) Bộ lọc: 5 ô cùng 1 hàng (Kỳ 2 · Kế hoạch 2 · Hàng hóa 3 · Kho 2 · Công ty thuê 3)
- [x] (2) Icon ⓘ lệch tiêu đề ở khối tổng hợp → căn giữa theo dòng chữ
- [x] (3a) BE: nhóm theo công ty thuê (lô `self_inventory_product_position_details.company_id`) + kho (vị trí `self_inventory_product_positions.warehouse_id`); lọc Kho / Công ty thuê theo dòng; `groups` phân trang theo công ty; `summary.products`
- [x] (3b) BE: `GET item-list?metric=surplus|shortage` (popup danh sách hàng thừa / thiếu)
- [x] (3c) BE: In + Excel ra cây (dòng công ty, dòng kho, dòng hàng — STT 1 / 1.1 / 1.1.1)
- [x] (3d) FE: khối tổng hợp 3 thẻ (Tổng số mặt hàng · Tổng SL thừa · Tổng SL thiếu), bấm SL thừa / thiếu mở popup
- [x] (3e) FE: bảng cây 3 cấp + ô chọn cấp bung, phân trang theo công ty
- [x] (4) Popup chọn kế hoạch: bỏ dòng mô tả dưới tiêu đề, bộ lọc theo UI mới (V2BaseSmartFilterPanel in-modal + ô tìm nhanh), cột Người tạo "Tên - Mã phòng"
- [x] Verify: HTTP kernel BE + compile FE

Ghi chú thực hiện:
- (3a) Khác ERP có chủ đích: 1 hàng +2 ở công ty A, −2 ở công ty B nay ra 2 dòng (ERP cộng thành 0 rồi bỏ). Số local không đổi (1 thừa SL 1 · 3 thiếu SL 5).
- (3c) Dòng nhóm của bản in: tên gộp vào các cột chữ trước cột số; bỏ hết cột chữ thì tên đi kèm STT.
- (3d) Popup thừa / thiếu chỉ có nút Đóng (chưa làm In / Excel riêng của popup — báo cáo chính đã có).
- (3e) STT theo mẫu tester 1 / 1.1 / 1.1.1 (không La Mã), mặc định bung hết 3 cấp.
- (4) Sửa ở popup dùng chung → màn Thêm phiếu kiểm kê cũng đổi theo (bỏ dòng mô tả, bộ lọc mới).

### Checkpoint — 10/11/2026 17:00
Vừa hoàn thành: #12095 cả 4 mục. BE qua HTTP kernel: index 200 (groups 1 công ty → 1 kho → 4 dòng), item-list surplus/shortage 200, metric lạ 422, print 200 (cây, chọn cột), export 200, plans 200. FE 5 file compile sạch, trang dev 200.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm (bộ lọc 1 hàng, icon ⓘ, 3 thẻ + popup, bảng cây + ô chọn cấp, popup chọn kế hoạch ở cả 2 màn) → commit.
Blocked: DB local không có Kế hoạch tổng kiểm kê → popup chọn kế hoạch chỉ thấy bảng rỗng; local chỉ 1 công ty / 1 kho có chênh lệch.

### Checkpoint — 10/11/2026 (push)
Vừa hoàn thành: #12095 ĐÃ PUSH `develop` (hrm-api `1f74d44df`, hrm-client `2585cec12`; cùng lượt push kèm commit Biên bản giao nhận hàng hoá theo yêu cầu user).
Bước tiếp theo: QA kiểm lại trên dev, đóng issue Redmine.
