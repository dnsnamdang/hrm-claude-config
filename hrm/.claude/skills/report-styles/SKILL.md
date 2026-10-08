---
name: report-styles
description: "Use when làm MỚI hoặc UPDATE STYLE một màn báo cáo trong hrm-client (pages/assign/report/*, pages/sale/*-tracking…) — \"chuyển báo cáo cũ sang style mới\", \"đổi giao diện báo cáo\", khối tổng hợp .rsum, bảng cây rsum-tb, dòng TỔNG, ô chọn \"cấp muốn bung\", con số bấm mở popup drill, nút In / Xuất Excel trên header bộ lọc, tiêu đề bảng báo cáo không dính khi cuộn."
---

# Skill: Style báo cáo (khuôn rsum)

Mọi báo cáo dùng **1 khuôn**: bộ lọc nổi → khối tổng hợp `.rsum` → bảng cây `rsum-tb` → popup drill.
**Mẫu chuẩn:** Báo cáo tổng hợp CSKH tiềm năng (`pages/assign/report/potential-customer-tracking`, chốt 04/10/2026).
Ảnh chụp nguyên văn của mẫu nằm trong `template/` cạnh file này (commit `ae11073e9`, nhánh
`gop_db-bao-cao-tong-hop-cskh-tiem-nang`). Dùng bản này vì nhánh đang đứng có thể chưa có mẫu.
Comment trong `template/` nhắc `service-demand` / `prepick-tracking` là **tổ tiên** của khuôn. Mẫu
`template/` đã gộp mọi sửa của 2 màn đó, nên copy từ `template/`. Chỉ lấy riêng ô Kỳ ở `service-demand`
(mục 5b).

Cần xem mẫu CHẠY THẬT (để dựng mockup): dùng worktree sẵn có
`websites/wt-bao-cao-tong-hop-cskh/hrm-client`, hoặc tạo worktree mới từ nhánh trên. KHÔNG checkout đổi
nhánh ở repo chính (nhiều session dùng chung).

> Liên quan, KHÔNG lặp lại ở đây: `button-convention` (màu nút), `info-icon-tooltip`, `print-page`
> (bản in xem trước), `export-excel`, `modal-popup`.

## 1. Bố cục (trên → dưới)

| # | Thành phần | Mẫu trong `template/` | Điểm phải giữ |
|---|---|---|---|
| 1 | `V2BaseSmartFilterPanel floating` | `index.vue` | `reset-button-text="Xóa lọc"` · `#title-suffix` = `InfoTip` "MỤC ĐÍCH BÁO CÁO" · `#header-actions` = **In danh sách** (`secondary`) + **Xuất Excel** (`secondary status="success"`), cả 2 `size="sm" class="btn-compact"`, KHÔNG `mr-2/ml-2`. Ô chọn đổi là tìm luôn |
| 2 | Khối tổng hợp `.rsum` | `components/TrackingSummary.vue` | Dòng `.rsum-goal` (tiêu đề · meta · nút Thu gọn) + 2 khối `.rsum-blk` cùng hàng. Mọi số là `DrillNum`. **Chỉ tiêu = 0 thì ẩn**, trừ ô tổng của khối. Số tính trên TOÀN BỘ dữ liệu đã lọc (`summary` của BE), không theo trang |
| 3 | Bảng cây `table.rsum-tb` | `components/TrackingTable.vue` | `.ptr-table > .market-table-wrap > V2BaseTableScroll max-height="calc(100vh - 200px)"` · 1 hàng tiêu đề dính (`position: sticky; top: 0`) · dòng **TỔNG** (`.rsum-tb__sec`) đầu bảng · ô chọn cấp bung trong tiêu đề cột Nội dung · phân trang `V2BasePagination` theo nhóm CẤP 0 |
| 4 | Popup drill | `components/ItemListModal.vue` | `components/report/V2BaseReportModal.vue` + `reportDrillListMixin` (tên state `filters`/`keyword` cố định) · footer: In danh sách · Xuất Excel danh sách · Đóng |
| 5 | In | `components/report/V2BaseReportPrintModal.vue` (DÙNG CHUNG — KHÔNG copy về từng màn) + `ReportPrintPreviewModal` + `reportPrintPreviewMixin.openPrintList(API, params)` | Theo **mục 4b**: chọn bản in + "Chọn cột in"; nút In danh sách của popup drill cũng qua popup này (chỉ chọn cột) |
| 6 | Chi tiết bản ghi | `MeetingDetailDrawer` (`WorkItemDetailDrawer`) | `header-gradient="linear-gradient(135deg, #0a1c3d, #06b6d4)"`, `:above-modal="drill.visible"` |

Phụ trợ copy kèm: `DrillNum.vue` (số 0 không bấm được), `InfoTip.vue` (icon ⓘ, PHẢI `font-weight: normal`),
`format.js` (`num` en-US, `dmy`), `api.js`.

## 2. Bảng cây — thông số đã chốt

- Cấp `d0..d3`: thụt **30/52/74/96px**; vạch cấp bằng `::before` (left 2/24/46/68, `#0a7c88` → nhạt dần), KHÔNG dùng `border-left` của td.
- STT: d0 số La Mã (I, II…), d1 `1`, d2 `1.1`, lá `1.1.1`.
- Màu dòng: d1 `#f7fbfd` · d2 `#fafcfe` · lá `#fff` (tên chữ xám). Dòng cha đang mở: `#dceaf4` / `#e9f3f9` / `#f1f8fb`. Hover `#d9eff7`. d0 kẻ trên `2px #b6d8e0`.
- Tiêu đề: nền `linear-gradient(180deg,#f3fdfe,#e2f6f9)`, viền dưới `2px #20d9ea`, chữ `#0a7c88` 12px/800.
- TỔNG: nền `#fdf1ea`, kẻ trên `2px #c2703a`, chữ `#9a5326`, nhãn viết hoa.
- Số 0: `#c2cbd6`. Đơn vị sau số (`.unit-sub`) / mã sau tên (`.code-sub`): 10.5px `#6b7280`, **`text-transform: none`**.
- Bảng nhiều cột: `table-layout: fixed` + `<colgroup>` độ rộng cố định + `min-width` → **cuộn ngang 2 thanh** (`V2BaseTableScroll`). Không ép vừa khít, không `overflow-x: hidden`.
- **Tiêu đề cột LUÔN 1 dòng** (user chốt 07/10/2026): `th { white-space: nowrap }`, ô tiêu đề có ô chọn cấp thì nhãn + ô chọn nằm CÙNG HÀNG (`flex-wrap: nowrap`). Không đủ chỗ thì nới `<colgroup>` / `min-width` cho cuộn ngang — CẤM cho tiêu đề xuống 2 dòng hay xếp ô chọn cấp xuống hàng 2 (lỗi cũ của service-demand: ép vừa khít 1083px ở 1366 làm 4 tiêu đề 2 dòng).
- Ô chọn cấp: `V2BaseSelect size="xs"` — KHÔNG ép `height` (cỡ xs cao 26px, chữ line-height 24px; ép 18/22px là chữ tràn đáy ô — lỗi khuôn cũ, sửa 07/10/2026); 1 map `expanded{}` dùng chung cho ô chọn và mũi tên `.rsum-caret` (`<button>` thô). `applyLevel()` chạy lại khi `groups` đổi.
- Dòng cha có nhiều loại số → render-function nhỏ (vd `CountPair`) → CSS con phải chọn qua `::v-deep`.

## 3. Logic trang (copy từ `template/index.vue`, đừng viết lại)

- `reportSeq` / `optionsSeq` / `drillSeq`: response về trễ không được đè response mới.
- Đang tải lại thì làm mờ (`.pct-body--loading` opacity .6), không xoá trắng. Lỗi thì GIỮ báo cáo cũ.
- `reportParams` = params của lần tải thành công gần nhất. In / Excel / drill dùng `drillBaseParams()` (bỏ `page`/`per_page`).
- `keepSelectedOptions()`: danh mục đổi theo phạm vi thì vẫn giữ mục đang chọn, nếu không sẽ lọc ngầm.
- Quyền đổi công ty lấy từ BE `can_change_company === true` (fail-closed, không bypass super admin).
- Nhóm "Chưa xác định" gửi `0` khi drill, đừng bỏ trống (bỏ trống thì popup liệt kê mọi dòng).
- Excel tải bằng LINK trực tiếp `?token=`, không dùng blob (Safari hỏng).
- Mảng gửi dạng chuỗi `"7,8"` (link Excel không giữ được `[]`).

## 4. Hợp đồng API (BE `hrm-api`)

```
GET {API}                     -> { generated_at, summary, groups (trang cấp 0), meta{total,per_page,current_page} }
GET {API}/filter-options      -> danh mục theo quyền + can_change_company
GET {API}/item-list           -> { rows, meta }  (scope + q, trần 500/trang; FE lặp đủ trang)
GET {API}/export · {API}/item-list/export   (Excel, skill export-excel)
GET {API}/print-list-data     -> { template }  (tên cố định — contract của reportPrintPreviewMixin)
```
`summary` và dòng TỔNG tính trên toàn tập đã lọc. Phân trang theo nhóm cấp 0, không cắt ngang nhóm.
Trạng thái trả `status_text` + `status_color` → `V2BaseBadge :color`; FE không map số → chữ.

## 4b. In — QUY TẮC CHUNG (user chốt 07/10/2026, mẫu chạy thật: `pages/assign/report/customer-market-development`)

Mọi báo cáo dùng **1 component** `components/report/V2BaseReportPrintModal.vue`, 1 instance/trang cho cả 2 nút:

| Nút | Popup hiện gì | Gửi BE |
|---|---|---|
| **In báo cáo** (`#header-actions`) | Truyền `:modes`. Radio chọn bản in (`summary` bảng tổng hợp / `detail` danh sách) + khối **"Chọn cột in"**. Danh sách cột **đổi theo bản in đang chọn** (mỗi mode tự khai `columns`); đổi bản in = tick lại hết | `mode` + `cols` |
| **In danh sách** (footer popup drill) | KHÔNG truyền `modes` → chỉ "Chọn cột in", danh sách = **đúng các cột đang hiện trên popup** (popup emit kèm `columns: [{ key, label }]`) | `mode=detail` + `cols` + tham số popup (`key`, `metric`, `p_*`, `q`, `sort`, `dir`) |
| Xuất Excel / Xuất Excel danh sách | **KHÔNG** qua popup chọn cột — luôn đủ cột đang hiện | — |

Hành vi (component đã làm sẵn, đừng viết lại): mở = tick hết · "Chọn tất cả" bán chọn khi tick 1 phần · bỏ hết rồi bấm In
→ đỏ "Vui lòng chọn ít nhất 1 cột để in", KHÔNG đóng, KHÔNG gọi BE · mở lại = về mặc định · nút **In** trước **Hủy**
(button-convention) · emit `print({ mode, columns })`, `columns` giữ thứ tự khai báo (= thứ tự cột bảng), trang nối
`cols = columns.join(',')`. Cột luôn in (STT, Nội dung theo dõi) KHÔNG khai trong `columns`, ghi ở `fixedNote`.

Trang (khuôn `template/index.vue`): `printModes` trong `data`, `drillPrint: null`; `printItemList({ columns, ...own })` gán
`drillPrint` rồi mở popup; `onPrintChosen` rẽ 2 nhánh; `closePrintOptions()` reset `drillPrint`. Popup in nằm trên popup
drill (bootstrap-vue xếp theo thứ tự mở) — đo `elementFromPoint` giữa popup in phải trúng popup in.

BE (`{Report}PrintService`):
- Whitelist khoá theo từng bản in: `SUMMARY_COLUMNS` (cột số của bảng, giá trị `[nhãn, khoá metrics, kiểu]`) và
  `DETAIL_COLUMNS` (cột danh sách). Khoá = khoá FE, nhãn = tiêu đề cột trên màn.
- `cols` rỗng / toàn khoá lạ → đủ cột (tương thích lời gọi cũ). Bỏ khoá lạ. Bản tổng hợp lặp cột theo **thứ tự khai báo
  của bảng**; bản danh sách theo **thứ tự `cols`** (= thứ tự cột popup).
- Blade dựng `<th>`/`<td>` bằng `@foreach ($columns …)`, `colspan` ô "Không có dữ liệu" = `count($columns) + cột cố định`.
- Excel KHÔNG nhận `cols` từ bước chọn (đủ cột) — chỉ bản in.

## 5. Áp cho báo cáo CŨ — trình tự

1. Liệt kê cái báo cáo cũ đang có: bộ lọc, biểu đồ, cột, chip/popup, In/Excel, cách phân trang của BE (nhiều màn cũ cắt trang theo dòng con nên nhóm bị tách giữa 2 trang).
2. Hỏi user các điểm **nghiệp vụ**: khối tổng hợp gồm chỉ tiêu nào; cây gồm những cấp nào; giữ hay bỏ biểu đồ; cột nào giữ. Điểm thuần UI thì tự chốt theo khuôn này.
3. Mockup trong `.plans/…/mockup.html` dựng từ **DOM + CSS thật** của màn mẫu đang chạy (Playwright), không tự viết CSS.
4. Spec → plan → hỏi "làm" (nêu repo · nhánh · file · có đụng BE không) → code.
5. Đổi tiền tố class riêng của màn (`pct-` → tiền tố mới), id popup, `table=` của SmartFilterPanel.

## 5b. Biến thể hay gặp khi chuyển báo cáo cũ

| Tình huống | Cách làm |
|---|---|
| Báo cáo THEO KỲ (mẫu là "tại thời điểm xem", không có kỳ) | Ô **Kỳ** đứng đầu: copy `periodOptions` + ô con `range` (`type: 'date-range'`, `resetKeys: ['from','to']`, chỉ hiện khi `custom`) + `rangeIncomplete` (chưa đủ 2 ngày thì CHƯA gọi API) từ `pages/assign/report/service-demand/index.vue`. Đổi kỳ khác `custom` thì xoá `range/from/to`. `.rsum-goal` ghi "… {kỳ} (dd/mm/yyyy – dd/mm/yyyy)" lấy từ `report.meta` |
| Cây 2–3 cấp (vd Dự án ▸ Meeting) | Giữ nhịp thụt / màu / vạch của d0..dN đầu tiên, bỏ CSS cấp thừa. Ô chọn cấp có N mục ("Chỉ {cấp 0}" … "Tất cả cấp"); mặc định bung tới cấp áp chót. STT: d0 La Mã, cấp dưới `1`, `1.1` |
| Cột số không phải "đếm" (phút, tiền) | Ô dòng cha/TỔNG = tổng cộng, căn phải `.rsum-tb__num`, không bấm được; chỉ số ĐẾM bản ghi mới là `DrillNum` |
| Drill ra danh sách khác loại (vd người tham gia thay vì meeting) | Mỗi loại 1 popup `V2BaseReportModal` riêng với bộ cột riêng. Không nhồi 2 loại dòng vào 1 popup |
| Màn cũ có `print.vue` / mở tab in / popup `b-modal` / drill POST / `PrintOptionsModal` riêng của màn | Thay bằng `V2BaseReportPrintModal` (mục 4b) + `print-list-data` và `item-list` GET. Xoá `PrintOptionsModal.vue` riêng của màn khi chuyển. Xoá route `print.vue` + component cũ khi KHÔNG còn chỗ nào import (grep trước). Báo user trong spec |
| Màn cũ dùng `V2BaseCompanyDepartmentFilter` + `permissions` | Chuyển sang ô Công ty tự vẽ trong slot `#field-company_id` + `can_change_company` từ `filter-options` (như mẫu). BE phải trả cờ này |
| Cỡ trang | Theo mẫu: 20, chọn `[10, 20, 50, 100]`, đếm theo nhóm cấp 0 (`item-label` = tên cấp 0) |
| Màn cũ có biểu đồ | Khuôn không có biểu đồ. Bỏ hay giữ là câu hỏi NGHIỆP VỤ cho user; giữ thì đặt giữa `.rsum` và bảng |

## 6. Kiểm (Playwright, đo DOM)

- `th` vẫn dính sau khi cuộn trong vùng cuộn: `th.top === body.top`.
- Độ thụt `padding-left` 30/52/74/96, màu dòng như mục 2, `getComputedStyle(th).color` = `rgb(10, 124, 136)`.
- Đổi cấp bung → đếm đúng số dòng `rsum-tb__row--d*`.
- Số ở khối tổng hợp = dòng TỔNG = số dòng của popup drill tương ứng.
- Ở 1366px: ô `.rsum-blk__item` không xuống dòng nhãn, có 2 thanh cuộn khi bảng tràn.
- Ở 1366px: MỌI `th` chỉ 1 dòng chữ (đếm `top` khác nhau của `Range.getClientRects()` trên text node = 1); ô chọn cấp cao 26px, chữ không tràn đáy, cùng hàng với nhãn — helper e2e `e2e/utils/levelSelect.ts`.
- In / Excel theo đúng bộ lọc đang hiển thị. Test cả tài khoản CÓ quyền và KHÔNG quyền.
- In (mục 4b): bỏ 2 cột → request có `cols` đúng, bản xem trước đúng bộ `th` còn lại; đổi bản in → danh sách cột đổi; bỏ hết →
  báo đỏ, không request `print-list-data`; In danh sách popup → danh sách cột = `thead` popup, popup drill vẫn mở sau khi in.

## Lỗi thường gặp

| Lỗi | Đúng |
|---|---|
| Lấy `service-demand` / `prepick-tracking` làm mẫu vì nhánh hiện tại chỉ có chúng | Mẫu là `template/` của skill này |
| Đặt `th` sticky theo trang | `.content-page` có `overflow:hidden` → sticky trong vùng cuộn riêng (`V2BaseTableScroll max-height`) |
| `overflow-x: hidden` để bảng "vừa màn" | Cột Nội dung ≥ 420px + cuộn ngang 2 thanh |
| Hiện cả ô số 0 trong `.rsum` | Ẩn, chỉ giữ ô tổng |
| Giữ nút In/Excel/"Xem chi tiết" ở đầu card bảng | In/Excel lên `#header-actions`; "xem chi tiết" thay bằng ô chọn cấp |
| Popup `b-modal` tự dựng / chip bấm | `V2BaseReportModal` + `DrillNum` (gạch chân nét đứt) |
| Tự đặt lại màu/px "cho giống" | Copy SCSS nguyên văn từ `template/`, chỉ đổi tiền tố |
| `InfoTip` trong tiêu đề đậm thì icon dày | `font-weight: normal` ở `.ptr-info` |
| Copy `PrintOptionsModal.vue` về màn mới / tự dựng popup chọn cột | Dùng `components/report/V2BaseReportPrintModal.vue`, chỉ khai `printModes` |
| Nút In danh sách của popup in thẳng | Mở popup chọn cột (`columns` = cột popup) rồi mới in |
| Cho Xuất Excel đi qua bước chọn cột | Excel luôn đủ cột |
| BE in cố định cột | Whitelist `SUMMARY_COLUMNS` / `DETAIL_COLUMNS` + đọc `cols` |
