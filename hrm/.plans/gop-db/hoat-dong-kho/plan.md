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

## Fix #11901 — Nhãn Loại/Hình thức vận chuyển lệch ERP · tooltip · thứ tự dòng (29/10/2026)

- [x] BE `WarehouseActivityService`: nhãn Loại (xuất/nhập) + Hình thức vận chuyển lấy theo bảng ERP `ExportModel::TYPES` / `ImportModel::TYPES` / `TRANSITION_TYPES` (bảng riêng trong service, KHÔNG sửa bảng tra dùng chung của ĐNXK/ĐNNK) — áp cả màn Theo dõi theo kho
- [x] FE: tooltip tiêu đề màn (`pageTitleInfo`) + ⓘ từng ô Tổng số phiếu nhận / Tổng hoàn thành / Tổng chưa xử lý (`ActivitySummary`)
- [x] Ý 2 (dòng mới nhất nằm cuối): CHỈ điều tra — thứ tự y ERP `getActivities()` (chưa đổi tồn lên trước, rồi `received_time` giảm dần) → 3 phiếu cuối là phiếu ĐÃ HOÀN THÀNH nên xuống nhóm dưới. Không sửa, báo user.
- [ ] Ý 4 (dòng "Cập nhật lúc…" có cần không): trả lời đề xuất, chờ user chốt
- [x] Verify: php -l + gọi service trong tinker, compile FE

### Checkpoint — 29/10/2026
Vừa hoàn thành: #11901 ý 1 + 3 — BE `WarehouseActivityService` bảng nhãn ERP riêng (EXPORT_TYPE_NAMES / IMPORT_TYPE_NAMES / TRANSITION_NAMES), bỏ dùng bảng tra ĐNXK/ĐNNK; FE `pageTitleInfo` màn Hoạt động kho + ⓘ 3 ô tổng hợp (`ActivitySummary`, dùng chung Theo dõi kho). php -l + chạy service local 219 dòng, 0 dòng trống loại; compile template OK.
Đang làm dở: ý 4 chờ user chốt.
Bước tiếp theo: user mở trình duyệt xem tooltip + nhãn; trả lời QA ý 2 và 4.
Blocked:
- [x] Ý 4 — user chốt 29/10: BỎ dòng "Cập nhật lúc … · Chưa hoàn thành quá 10/20 phút" ở `ActivitySummary` (dùng chung → Theo dõi kho cũng bỏ). ⓘ phạm vi + nút Thu gọn lên đầu khối "Phiếu nhận"; chú thích vạch màu chuyển vào ⓘ. Bỏ prop `updatedAt` ở 2 màn. Compile template OK.
- [x] Ý 4 (tiếp) — user chốt 29/10: BỎ luôn vạch màu mép trái dòng (đánh dấu #11894) ở Hoạt động kho + Theo dõi kho. Xoá `activityRowClass` + hằng WARN/LATE (`activity-table.js`), xoá file `activity-row-marks.scss`, bỏ `rowClass`/`now` ở 2 màn, bỏ câu chú thích màu trong ⓘ. Compile OK.
- [x] Kiểm tra theo yêu cầu (29/10): thứ tự sắp xếp danh sách Hoạt động kho / Theo dõi kho — `WarehouseActivityService::listForWarehouses()`: [cột user bấm sort] → phiếu CHƯA hoàn thành trước (chưa có Thời gian hoàn thành) → Thời gian nhận giảm dần → id giảm dần (HRM thêm cho ổn định). Y ERP `getActivities()`. Phiếu chưa có Thời gian nhận xuống cuối nhóm chưa hoàn thành; phiếu đã hoàn thành luôn ở cuối. Không sửa code, báo user.

### Checkpoint — 29/10/2026
Vừa hoàn thành: #11901 — nhãn Loại/HTVC theo ERP (BE), ⓘ tiêu đề + 3 ô tổng hợp, bỏ dòng "Cập nhật lúc…/chú thích màu", bỏ vạch màu dòng (cả Theo dõi kho); kiểm tra thứ tự sắp xếp (giữ y ERP).
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm (chưa xem bằng trình duyệt); trả lời QA ý 2 (thứ tự y ERP).
Blocked:
- [x] Kiểm tra theo yêu cầu (29/10): "trạng thái xếp lộn xộn" — không phải lỗi: BE chỉ tách 2 nhóm chưa hoàn thành / đã hoàn thành, "Đã nhận đề nghị" và "Đang lấy/xếp hàng" cùng nhóm chưa hoàn thành nên xen nhau, trong nhóm xếp theo Thời gian nhận giảm dần (ảnh user: 09:25 → 09:01 đúng thứ tự). Y ERP. Đề xuất (chờ user chốt): xếp Đã nhận đề nghị → Đang lấy/xếp hàng → Đã hoàn thành, trong mỗi trạng thái theo Thời gian nhận giảm dần — lệch ERP.

## Tài liệu SRS / HDSD / Testcase (10/11/2026) @khoipv

Khuôn: `../list-bill-accounting/` (màn chỉ xem dạng danh sách) + `../tong-hop-xuat-nhap-ton/` (báo cáo kho 09/11). Không sửa code / dữ liệu / skill chung.

- [x] Đọc code FE (`pages/warehouse/activities`, `components/warehouse/activity/*`) + BE (`WarehouseActivityService`, controller, route không checkPermission) + nguồn 3 mốc thời gian (lập / gửi phiếu xuất kho, phiếu nhập kho, điều chuyển kho)
- [x] Chụp ảnh dev (`hdk_shots/_capture/capture.js`, DNS Admin, chặn mọi yêu cầu ghi — 0 lọt). DNS Admin không là thủ kho kho nào → màn thật rỗng; ảnh có dữ liệu = dữ liệu THẬT kho PTT lấy từ "Theo dõi theo kho" thay vào trên trình duyệt (cùng hàm dựng dữ liệu)
- [x] Đối soát dev (`_capture/doisoat.js`, chỉ GET): PTT 54 = 39 ĐNXK + 15 ĐNNK = đúng từng mã ở 2 màn danh sách (Chờ duyệt + Đang xuất/nhập kho); MT 5 = 1 + 4; KTCN 2 = 2 + 0; ô tổng hợp = số dòng; thứ tự đúng BR-05
- [x] `gen_srs.py` → `SRS - Hoạt động kho.docx` (44 trang, 5 chức năng, selfcheck khớp mẫu; metrics ui 12.6 / ev 4.2 / evch 857 / intro 1857)
- [x] `gen_hdsd.py` → `HDSD_Hoat dong kho.docx` (9 trang, 5 phần)
- [x] `gen_testcase.py` → `testcase.xlsx` (loai `bao_cao`, 102 TC, 8 nhóm, P0 43%, check_tc 0 lỗi)
- [x] `gen_checklist.py` → `Đối chiếu checklist.xlsx` (Testcase 115 có TC / 209 N/A; SRS 87 có mục / 76 N/A)
- [x] Ghi nhận nghi lỗi (KHÔNG sửa): (1) Super Admin không còn xem mọi kho — nhánh Super Admin trong `stockerWarehouseIds()` mất ở merge rbac 31/10 (d7b032a59), lệch quyết định 26/10 + ERP; (2) ĐNXK/ĐNNK gửi thủ kho từ HRM không ghi Thời gian nhận (ERP `send()` có ghi) → phiếu trống cột này, không vào nhánh "nhận hôm nay", xong là rời bảng; dev kho LN có 1 phiếu trống Thời gian nhận

### Checkpoint — 10/11/2026
Vừa hoàn thành: bộ SRS + HDSD + Testcase + Đối chiếu checklist màn Hoạt động kho.
Đang làm dở: —
Bước tiếp theo: user xem tài liệu; quyết định sửa 2 nghi lỗi (Super Admin mọi kho, ghi Thời gian nhận khi gửi thủ kho từ HRM).
Blocked:
