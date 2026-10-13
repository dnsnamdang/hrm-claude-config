# Báo cáo kết quả thực hiện dự án TKT — update theo khuôn report-styles (07/10/2026)

Màn: `/assign/report/prospective-project-results` · nhánh `gop_db` (cả 2 repo) · Hồ sơ gốc: `.plans/gop-db/bao-cao-ket-qua-du-an-tkt/`.
Khuôn: skill `report-styles` (SKILL.md mục 1–4b, 5b) + các đợt của `customer-market-development/plan.md`.

Báo cáo này VỐN đã dựng theo họ khuôn rsum (anh em với Phát triển thị trường – KH) → việc là soát chỗ lệch, không dựng lại.

## Hiện trạng — chỗ lệch khuôn (rà 07/10/2026)

FE `hrm-client/pages/assign/report/prospective-project-results/` · BE `hrm-api/Modules/Assign/Services/Report/ProspectiveProjectResult*`.

| # | Chỗ lệch | Loại |
|---|---|---|
| 1 | Thị trường tra tỉnh qua DB ERP CŨ (`env('DB_DATABASE_SECOND').provinces`, Svc `resolveCustomerProvinces`) | Nghiệp vụ / dữ liệu |
| 2 | Bấm tên dự án mở tab mới; chưa có panel chi tiết nổi trên popup | Nghiệp vụ |
| 3 | Ô lọc toàn chọn đơn (Phòng ban, Thị trường, Tiến trình, Kết quả…) | Nghiệp vụ |
| 4 | Bảng: `V2BaseTableScroll` không `max-height` → tiêu đề không dính; không phân trang (BE trả cả cây, không `meta`) | UI + BE |
| 5 | STT cấp 0 là `1,2…` (khuôn: La Mã); màu dòng TỔNG lệch khuôn; tiêu đề 11.5px/700 (khuôn 12/800); `table-layout: auto` | UI |
| 6 | Khối tổng hợp không ẩn chỉ tiêu = 0; `.rsum-goal` thiếu tên kỳ | UI |
| 7 | Popup in riêng `PrintOptionsModal` (không "Chọn cột in"); BE in không có `SUMMARY_COLUMNS/DETAIL_COLUMNS` + `cols`; tiêu đề in không theo chỉ tiêu, không có dòng đối tượng; nhãn "Tỉnh/TP" | Khuôn 4b |
| 8 | In danh sách popup in thẳng, không qua chọn cột | Khuôn 4b |
| 9 | Badge tiến trình cố định xám (`ProjectRowResource` `#6B7280`) dù đã có `ProspectiveProject::resolveStatusColor` | UI |
| 10 | Logic trang: không `reportSeq/optionsSeq/drillSeq`, không `reportParams` (In/Excel/drill lấy bộ lọc đang gõ), lỗi thì xoá trắng báo cáo, không làm mờ khi tải, đổi kỳ không tự tìm, thiếu `rangeIncomplete`, đổi công ty xoá hết ô | Logic khuôn |
| 11 | Ô Công ty `select` thường, BE không trả `can_change_company` | Khuôn 5b |
| 12 | Popup: KPI tính từ cây FE (lệch khi lọc thêm trong popup); không ô tìm `q`; state `ownFilters` | Logic khuôn |
| 13 | Nút Xuất Excel thiếu `size="sm"`; InfoTip viết tay; thiếu "(VND)" ở cột giá trị | UI |

## Câu hỏi nghiệp vụ (hỏi lần lượt)

- [x] Q1 — Thị trường tra tỉnh từ **DB gộp** (bỏ `DB_DATABASE_SECOND`), như CMD đợt 2.
- [x] Q2 — Bấm tên dự án **giữ mở tab mới**, không dựng panel.
- [x] Q3 — **Giữ mọi ô lọc chọn 1** giá trị.

Điểm UI/logic khuôn (4–13) tự chốt theo khuôn. Không làm mockup riêng: bố cục giữ nguyên, chỉ đổi chi tiết theo khuôn đã
duyệt (STT La Mã, màu TỔNG, tiêu đề dính, phân trang, popup "Chọn cột in").

## Tasks (user "Làm" 07/10/2026 — hrm-api + hrm-client nhánh gop_db, không migration / seeder / quyền, CHƯA commit)

BE (`hrm-api`):
- [x] B1. `resolveCustomerProvinces` join `provinces` DB gộp (bỏ `DB_DATABASE_SECOND`); sửa comment "mysql2". Đo: 268 KH có dự án
      TKT, 32 KH không có ở ERP cũ (trước dồn "Chưa xác định thị trường") nay đủ tỉnh; năm nay công ty 1 không còn nhóm Chưa xác định.
- [x] B2. Index trả `generated_at` + `pagination{page,per_page,total}` (khoá giống CMD), cắt `tree` theo nhóm cấp 0, kẹp 1..100,
      trang vượt → trang cuối; `summary` + `total` toàn tập. Bản in / Excel màn chính không qua `report()` → vẫn đủ cây.
- [x] B3. `filter-options` trả `can_change_company` = quyền tổng công ty && > 1 công ty (fail-closed).
- [x] B4. `project-list`: ô tìm `q` (mã / tên dự án / khách hàng, không phân biệt hoa thường, có dấu) + `metrics` = KPI sau ô tìm,
      trước chỉ tiêu bấm. Bản in / Excel popup cũng đi qua `q`.
- [~] B5. BỎ — badge Tiến trình xám là quyết định CỐ Ý cũ (ghi ở `ProjectRowResource`: "màu để dành cho 3 nhóm kết quả").
- [x] B6. PrintService: `SUMMARY_COLUMNS` (8) + `summaryColumns()`; `detailColumns()` theo thứ tự `cols` ∩ cột lát cắt; tiêu đề
      theo chỉ tiêu (`DETAIL_TITLES`); dòng đối tượng `describeNode()` từ `drill_key`; điều kiện thêm Tiến trình / Kết quả / Tìm,
      nhãn "Thị trường"; STT cấp 0 La Mã (`flattenTree`, dùng chung Excel); blade dựng cột động; nhãn "(VND)" ở bảng / Excel / popup.
- [x] B7. PHPUnit `ProspectiveProjectResultStyleTest` 5 ca (phân trang, STT La Mã, chọn cột, ô tìm + KPI, Thị trường DB gộp —
      đặt `DB_DATABASE_SECOND` sai vẫn chạy). RED trên code cũ 5/5, GREEN 5/5; `NoPartTest` 3 ca vẫn xanh.
- [x] B8 (phát sinh). Excel màn chính: STT `data-type="s"` — trước đó "1.1" bị Excel đổi thành số (1.10 → 1.1).

FE (`hrm-client`):
- [x] F1. Bảng: card `.ppr-table` + `V2BaseTableScroll max-height="calc(100vh - 200px)"`, `table-layout: fixed` min 1624px (Nội dung
      ≥ 420px; 1920 vừa khung, 1366 cuộn ngang trong khung), tiêu đề 12px/800, TỔNG màu khuôn + nhãn viết hoa, STT cấp 0 La Mã nối
      tiếp giữa trang, số 0 / "—" màu nhạt, `V2BasePagination` [10,20,50,100] đơn vị theo cấp 0, "(VND)", nhãn `.rsum-tb__th-label`.
- [x] F2. Khối tổng hợp: ẩn chỉ tiêu = 0 (trừ Tổng dự án; khối toàn 0 giữ ô đầu), `.rsum-goal` "Tổng hợp {kỳ} (dd/mm – dd/mm)",
      `InfoTip` (copy template, tiền tố `ppr-`), `DrillNum` theo template.
- [x] F3. Trang: `reportSeq/optionsSeq`, `reportParams` + `drillBaseParams()` (In / Excel / popup theo báo cáo ĐANG HIỂN THỊ),
      `reportCriteria`, làm mờ khi tải + lỗi giữ báo cáo cũ, `rangeIncomplete` (Tuỳ chọn chưa đủ ngày không gọi API), bỏ gửi
      `date_range`, `keepSelectedOptions()` (Phòng ban / Bộ phận / Nhân viên), ô Công ty slot + `can_change_company`, nút Excel
      `size="sm"`, `ensureReportLoaded()`, "Tuỳ chỉnh" → "Tuỳ chọn".
- [x] F4. In: `V2BaseReportPrintModal` (`printModes` summary 8 cột / detail theo tiêu chí, `drillPrint`), XOÁ `PrintOptionsModal.vue`
      riêng; In danh sách popup emit `columns` = cột đang hiện.
- [x] F5. Popup: ô tìm (debounce 300ms, Xoá lọc dọn luôn), KPI lấy `metrics` BE, `listSeq` chống response cũ.
- [x] F6. Đo MCP 1366 + 1920 (xem checkpoint) · e2e: API ca 7 thêm `can_change_company` + ca 12 mới; UI ca 12-14 mới
      (khuôn bảng, In chọn cột, ô tìm popup). Biên dịch được (`--list` 29 ca), CHƯA chạy.
- [ ] User kiểm trên app · commit / push khi user yêu cầu · chạy e2e khi user yêu cầu.

### Checkpoint — 2026-10-07
Vừa hoàn thành: B1-B4, B6-B8, F1-F6.
Đo MCP (công ty 1, Năm nay, tiêu chí Thị trường): 280 dự án / 25 thị trường → trang 1 20 dòng (I…XX), trang 2 5 dòng (XXI…XXV),
TỔNG giữ 280; bung "Tất cả cấp" 261 dòng, cuộn 600px tiêu đề dính (`th.top = body.top`), thụt 30/52/74/96; tiêu đề cao 42px đều,
ô chọn cấp 26px lệch tâm nhãn 0px; TỔNG `rgb(253,241,234)` / `rgb(154,83,38)`. In báo cáo bỏ 2 cột → `cols=total,open,won,lost,
rate,expected`, xem trước đúng 6 cột số, STT I / 1 / 1.1. Popup Cần Thơ 5 dự án: thead 10 cột = popup chọn cột (không radio),
popup chọn cột nổi trên, in với `q` → dòng đối tượng "Thị trường: Thành phố Cần Thơ" + "Tìm: …"; popup chi tiết vẫn mở. Excel
popup 5 dòng tiền `#,##0`; Excel màn chính 25 nhóm cấp 0 đủ. Kỳ Tuỳ chọn chưa đủ ngày: 0 request. Người không quyền tổng công
ty (NV 24): `can_change_company=false`, 1 công ty, gửi công ty lạ bị ép về công ty mình. Console: chỉ 404 ảnh (letterhead tương
đối + e2e.png), không lỗi JS.
Bước tiếp theo: user kiểm trên app; commit / chạy e2e khi được yêu cầu.
Blocked: —

## Đợt 2 — bộ lọc màn chính chia đều (user "Làm" 07/10/2026; popup không đổi)

- [x] Gỡ `wrapperClass: 'company-field'` + CSS 340px: ô Công ty về `col-md-3` như 9 ô còn lại. Đánh đổi user đã biết: tên dài
      (chi nhánh Vinh) bị cắt "…", xem đủ qua `title` của ô / danh sách chọn.
- [x] Đo MCP: 1366 mọi ô 274px (ô chọn 264×32), 1920 mọi ô 413px; 3 hàng; ô Công ty `col-md-3`, `title` = tên đầy đủ.

## Đợt 3 — ⓘ chú thích mọi con số khối tổng hợp (user duyệt nội dung + "Làm" 07/10/2026)

- [x] `ResultSummaryBlocks.vue`: ⓘ ở 6 ô (map `ITEM_TIPS` theo `item.key`), 2 tiêu đề khối (`BLOCK_TIPS`, nhận khối theo chỉ tiêu
      chứa trong khối), dòng số liệu chung (`META_TIP`: số dự án / số KH khác nhau / % = ô ÷ Tổng). Mỗi ⓘ ô có "Bấm vào số…".
      CSS chặn icon nới dòng chép từ template `TrackingSummary`.
- [x] Đo MCP 1280/1366/1920: mọi ô có ⓘ nằm trong nhãn, nhãn 1 dòng không cắt, ô 46px (trước 45px — icon 14px trong nhãn 10px,
      giống khuôn mẫu), popover hiện đúng nội dung. E2E ca 12 thêm đếm ⓘ (chưa chạy).

## Đợt 4 — popup: tổng số + tổng giá trị · "Nhân viên chủ trì dự án" · tiến trình "6. Lập dự toán" ở 4 báo cáo (user "Làm" 07/10/2026)

Chốt: header "N dự án · Tổng giá trị đầu tư dự kiến … VND" ở MỌI popup + bản in danh sách; đổi nhãn đồng bộ (cột, ô lọc, chip,
bản in, Excel; cấp cây / ô chọn cấp giữ ngắn); tiến trình "{id}. {tên}" ở 4 báo cáo (Kết quả TKT, Vòng đời TKT, Tổng hợp CSKH
tiềm năng, Meeting theo dự án) qua helper mới `ProspectiveProject::statusLabel()`; màn danh sách Dự án TKT + store dùng chung giữ.

- [x] A1. `ProspectiveProject::statusLabel($status, $isParent = false)` = "{id}. {tên}" (null nếu không tra được tên) — hàm MỚI,
      không sửa `resolveStatusName()` / `statusOptions()`.
- [x] A2. Kết quả TKT: `status_label`, ô lọc `statuses`, dòng điều kiện; `project-list` + `projectListAll` trả `amount_total`
      (Σ Giá trị đầu tư dự kiến của cả tập đang lọc, mọi trang); bản in danh sách thay "Tổng số dòng" bằng dòng
      "N dự án · Tổng giá trị đầu tư dự kiến: … VND".
- [x] A3. "Nhân viên chủ trì dự án": `COLUMN_LABELS`, `DIM_LABELS` (dòng đối tượng), dòng điều kiện; FE cột popup, `DIM_LABELS`
      (tiêu đề popup + chip), placeholder ô lọc popup, ô lọc màn chính, cột In chi tiết. Cấp cây / ô chọn cấp / nhãn TỔNG giữ "Nhân viên".
- [x] A4. Popup: `metaText` = (đường dẫn cấp cha ·) "N dự án · Tổng giá trị đầu tư dự kiến … VND", theo đúng bộ lọc / ô tìm popup.
- [x] A5. Vòng đời TKT: BE `getStatusNameMap()` dùng `statusLabel`; FE `projectStatusOptions` map tại màn (`${id}. ${text}`) — ô lọc,
      popup, pill cùng đọc từ đây; store `getProspectiveProjectStatusOptions` không đổi.
- [x] A6. Tổng hợp CSKH tiềm năng: `status_text` + `statuses` (khối tổng hợp, bảng, ô lọc chọn nhiều, popup, bản in, Excel đều theo).
- [x] A7. Meeting theo dự án: `project_status_text` = `statusLabel(status, is_parent_project)`.
- [x] A8. PHPUnit: StyleTest +2 ca (statusLabel kể cả dự án cha; amount_total mọi trang) 7/7 · NoPart 3/3 · Feature
      PotentialCustomerTracking 21/21 (sửa 1 assert "6. Lập dự toán") · MeetingByProjects 28/28. E2E: UI ca 15 + API ca 13 mới,
      PCT spec chọn "6. Lập dự toán" — biên dịch được, CHƯA chạy.
      Đo MCP 1366: ô lọc "Nhân viên chủ trì dự án" + options "2. Thu thập thông tin dự án…"; popup TỔNG năm nay "280 dự án · Tổng
      giá trị đầu tư dự kiến 4,668,683,368,875 VND" = dòng TỔNG bảng, lọc "Vẫn tiếp tục triển khai" → "249 dự án · … 4,515,224,868,875
      VND"; cột popup đổi tên, không tiêu đề nào cắt chữ; bản in "Tiến trình: 6. Lập dự toán" + "138 dự án · …". Vòng đời: ô lọc /
      bảng cơ cấu "1. Đang tạo…6. Lập dự toán". CSKH tiềm năng: 8 nhãn khối tổng hợp "2. …9. …" không cắt, bố cục giống hệt khi bỏ
      tiền tố (2 hàng + ô 95px là sẵn có). Meeting theo dự án: dòng dự án "6. Lập dự toán".

## Đợt 5 — khối tổng hợp kèm Giá trị đầu tư dự kiến mỗi ô (user "Làm" 07/10/2026)

- [x] BE `summary()`: mỗi ô thêm `amount` = Σ `investmentAmountFor()` của đúng tập ô (`applyMetricFilter`). PHPUnit +1 ca (8/8).
- [x] FE `ResultSummaryBlocks.vue`: dòng phụ "x VND" 10.5px xám dưới số lượng (`title` đủ số), ⓘ mỗi ô thêm dòng giải thích.
- [x] Đo MCP 1280/1366/1920 (Năm nay): 5 ô cao đều 60px, không cắt chữ; Tổng 4,668,683,368,875 = 700,000,000 + 4,667,983,368,875
      = 153,458,500,000 + 4,515,224,868,875 = cột giá trị dòng TỔNG bảng. E2E API ca 13 thêm đẳng thức tiền (chưa chạy).

- [x] Đợt 5b (user "Làm"): giá trị CÙNG HÀNG số lượng ("278 99.3% · 4,667,983,368,875 VND"); khối `flex: 1 1 auto`, ô
      `flex: 1 0 auto; min-width: max-content` (co theo nội dung, kiểu `minmax(max-content, 1fr)` của báo cáo thị trường). Đo MCP
      1280/1366/1920 + Tháng này: mọi ô 46px, số và giá trị cùng hàng, 0 ô tràn, 2 khối vẫn 1 hàng, trang không cuộn ngang.

### Checkpoint — 2026-10-07 (wrap up)
Vừa hoàn thành: đợt 1-5b. ĐÃ COMMIT + PUSH gop_db (api `dc2e24d57`, client `7fde5a2fd`).
Đang làm dở: —
Bước tiếp theo: chạy e2e (tkt-result-report{,.api}, potential-customer-tracking) khi user yêu cầu · deploy BE + FE (không migration).
Blocked: —

## Ngoài luồng (ghi lại, chưa sửa)
- Excel màn chính báo cáo Phát triển thị trường – KH (`customer_market_development_report.blade.php`) cũng để STT là số → "1.1"
  bị Excel đổi thành số, "1.10" hiện 1.1. Sửa giống B8 (`data-type="s"`).
