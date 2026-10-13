# Task 10 — Chuyển `ProjectListModal` sang vỏ `V2BaseReportModal` (server-side, KHÔNG mixin)

## 1. Số dòng

| | Trước | Sau |
| --- | --- | --- |
| `ProjectListModal.vue` | 888 | 848 |

## 2. Thứ đã gỡ (chuyển sang vỏ, hoặc gỡ vì trùng vỏ)

- `V2BaseModal` dựng tay (header icon/subtitle-label/subtitle/size/dialog-class/max-body-height) →
  thay bằng `V2BaseReportModal` (banner `lead/title/meta`, size="xl" hard-code sẵn).
- `V2BaseTableScroll`, `V2BasePagination` — vỏ tự dựng, bỏ import + bỏ khai trong template.
- Toàn bộ `<table class="tkt-drill-table">` viết tay (thead/tbody/STT/sort icon 2 mũi tên
  `.tkt-sort`) — vỏ tự vẽ bảng theo `columns`/`rows`/`start-index`, popup chỉ còn cấp `columnDefs`
  (adapter) + slot `cell-<key>` cho 4 cột cần định dạng riêng.
- `toggleSort(col)` / `isSortActive(col, dir)` — vỏ tự vẽ tiêu đề + icon sắp xếp, popup chỉ còn
  `onSort({ key })` nối vào cơ chế sắp BE sẵn có.
- `ref="baseModal"` + gọi `$refs.baseModal.show()/close()` — thay bằng data `visible` tự quản
  (vẫn giữ API `open(payload)` gọi qua `ref` từ `index.vue`, không đổi hợp đồng với màn cha), đóng
  qua `close() { this.visible = false }`.
- CSS bảng tự chế (`.tkt-drill-table`, `.tkt-center`, `.tkt-right`, `.tkt-drill-table__empty`,
  `.tkt-sort*`, `.tkt-drill-dialog`, `.tkt-drill-paging`) — vỏ đã có sẵn (khối KHÔNG scoped của
  `V2BaseReportModal.vue`).
- Không có mixin nào bị gắn (đúng brief) — máy lọc/sắp/phân trang vẫn 100% ở BE qua `fetchList()`.

## 3. "Đổi mặt" đã lường trước (đúng hướng, không phải lỗi)

- Có thêm nút **Phóng to toàn màn hình** (`heightFull`: `null` → `900`) — vỏ tự cấp,
  `V2BaseModal` cũ không có.
- Viền + bo góc vùng cuộn bảng xuất hiện (`tableScrollBorderTopWidth`: `0px`→`1px`,
  `tableScrollBorderRadius`: `0px`→`6px`) và `modalContentOverflow`: `visible`→`hidden` — vỏ chặn
  chiều cao `.modal-content` (92vh) thay vì để tự do như `max-body-height="80vh"` cũ.
- `tableBottom`/`footerTop`/`heightNormal` đổi số do khung mới — **bất biến giữ**: đáy vùng bảng
  (642) ≤ đỉnh hàng nút (787) — không đè lên nhau.
- **Thứ tự khối bị đảo**: bản cũ đặt nút "Xem tổng hợp" + KPI + chip phân bổ TRƯỚC hàng bộ lọc; vỏ
  quy định cứng thứ tự slot `#filters → #back → #summary → bảng`, nên khối tổng hợp giờ đứng SAU
  bộ lọc. Đây là hệ quả kiến trúc bắt buộc của vỏ dùng chung, không phải rơi rụng — đã kiểm bằng
  Playwright: nút "Xem tổng hợp" vẫn hiện đúng vị trí mới, bấm vẫn mở/đóng đúng cả khối KPI (6 ô)
  lẫn chip phân bổ (2 nhóm).

## 4. Bug phát hiện + đã sửa trong lúc kiểm chứng (không có trong brief)

**Vỏ chỉ hiện "Đang tải…" khi `rows.length === 0`** (`V2BaseReportModal.vue`:
`{{ loading ? 'Đang tải…' : emptyText }}` chỉ render khi bảng rỗng) — khác bản `V2BaseModal` tay cũ
LUÔN chèn thêm 1 dòng "Đang tải…" bên dưới dữ liệu cũ trong lúc tải lại (dù bảng đang có dữ liệu).
Vì `fetchList()` gốc không xoá `rows` trước khi gọi API, mỗi lần đổi trang/sắp xếp/lọc, bảng giữ
NGUYÊN dữ liệu cũ mà KHÔNG có tín hiệu "đang tải" nào — tái hiện được bằng chính script đo
(`measure-popup.mjs` chờ hết chữ "Đang tải…" trước khi đọc `sortTextAsc`/`sortDateAsc`, nhưng vì
chữ đó không bao giờ xuất hiện lúc rows còn dữ liệu cũ, script đọc NGAY khi vẫn còn dữ liệu CŨ chưa
sắp → `sortTextAsc`/`sortDateAsc` ra thứ tự ngẫu nhiên, không tăng dần). Đã sửa: `fetchList()` xoá
`this.rows = []` ngay trước khi gọi API — vỏ hiện đúng "Đang tải…" mọi lượt gọi lại, và khớp lại
100% baseline sau khi sửa. Xem diff tại dòng `561-575` của file.

## 5. So với `baseline-tkt.json`

Lệnh (theo đúng tham số Task 8 đã chốt cho màn `prospective-project-results`):
```
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" node .plans/gop-db/base-popup-bao-cao/measure-popup.mjs /tmp/after-tkt.json \
  --url="http://127.0.0.1:3000/assign/report/prospective-project-results" \
  --sort-text="Nhân viên phụ trách" --sort-date="Ngày lập dự án"
```

| Khoá | Baseline | Sau | Kết quả |
| --- | --- | --- | --- |
| `cols` | 11 cột | 11 cột, ĐÚNG thứ tự | KHỚP |
| `firstPageRowCount` | 20 | 20 | KHỚP |
| `sttFirst`/`sttLast` | "1"/"20" | "1"/"20" | KHỚP |
| `pageTotal` | "Hiển thị 1–20 / 50 dự án" | "Hiển thị 1–20 / 50 dự án" | KHỚP |
| `footerButtonGaps` | 8px, 8px | 8px, 8px | KHỚP |
| `sortTextAsc` (20 phần tử) | Nguyễn Quốc Trung → ... → Vũ Quang Hưng | y hệt | KHỚP (byte-for-byte) |
| `sortDateAsc` (20 phần tử) | 03/07 → ... → 29/07/2026 | y hệt | KHỚP (byte-for-byte) |
| `tableBottom` | 656 | 642 | LỆCH — đúng hướng (khung mới) |
| `footerTop` | 742 | 787 | LỆCH — đúng hướng |
| `heightNormal` | 775 | 844 | LỆCH — đúng hướng |
| `tableScrollBorderTopWidth` | "0px" | "1px" | LỆCH — đúng hướng (vỏ có viền) |
| `tableScrollBorderRadius` | "0px" | "6px" | LỆCH — đúng hướng |
| `modalContentOverflow` | "visible" | "hidden" | LỆCH — đúng hướng |
| `heightFull` | `null` (không có nút) | 900 | LỆCH — đúng hướng (nay có nút Phóng to) |

Bất biến bắt buộc: `tableBottom` (642) ≤ `footerTop` (787) — GIỮ.

## 6. Bảng đối chiếu class khai / dùng (RỖNG — không có class khai mà không dùng)

Khai trong `<style scoped>`:
`report-drill-chip`, `report-drill-chip-new`, `report-drill-chip__n`, `report-drill-chipbox`,
`report-drill-chipbox__title`, `report-drill-chips`, `report-drill-chips__grp`,
`report-drill-chips__label`, `report-drill-chips__list`, `report-drill-count`,
`report-drill-filters`, `report-drill-filters__item`, `report-drill-project-link`,
`report-drill-sum`, `report-drill-sum-toggle`, `report-drill-sum__item`,
`report-drill-sum__item--bad`, `report-drill-sum__item--good`
→ tất cả xuất hiện literal trong `class="..."` của template (grep xác nhận, 18/18).

Khai trong `<style>` KHÔNG scoped:
`report-drill-table__money` → KHÔNG xuất hiện literal trong template (đúng như thiết kế) — được
dùng GIÁN TIẾP qua `ALIGN_CLASS_MAP['tkt-right'] = 'report-drill-table__money'`, gán vào
`cellClass` của cột `amount` trong computed `columnDefs()`, rồi vỏ tự gắn vào `<td>` của CHÍNH NÓ
(`V2BaseReportModal.vue`) — đây là lý do PHẢI khai không-scoped (bài học 1), đã kiểm bằng
`getComputedStyle` thật (mục 7). `report-drill-table__center` KHÔNG khai trong file này vì vỏ đã
có sẵn (dùng thẳng qua `ALIGN_CLASS_MAP['tkt-center']`).

Danh sách "khai mà không dùng": **RỖNG**.

## 7. 3 phép đo thêm (Playwright MCP, không nằm trong `measure-popup.mjs`)

**a. `getComputedStyle` của ô có `cellClass` (căn lề)** — đo trên dòng dữ liệu đầu tiên:

| Cột | `cellClass` | `text-align` đo được |
| --- | --- | --- |
| STT | (vỏ tự gắn) | center |
| Tên dự án TKT | (không có) | left |
| Ngày lập dự án | `report-drill-table__center` | center |
| Tiến trình | `report-drill-table__center` | center |
| Kết quả | `report-drill-table__center` | center |
| Giá trị | `report-drill-table__money` | right |

Đúng thiết kế: cột không có `cellClass` giữ mặc định trái, 3 cột trung tính (`tkt-center` cũ) đều
`text-align:center`, cột tiền (`tkt-right` cũ) `text-align:right`.

**b. Đếm request khi mở popup và khi lật trang** (đọc `mcp__playwright__browser_network_requests`,
lọc `project-list`):
- Mở popup (bấm số trên dải tổng hợp): **đúng 1 request** (`page=1&sort=created_at&sort_dir=desc`).
- Lật sang trang 2: **đúng 1 request MỚI** (`page=2`, giữ nguyên sort) — không có request thừa.
- Bấm sắp xếp cột "Giá trị" (đang ở trang 2): **đúng 1 request MỚI** (`sort=amount&sort_dir=asc&page=1`).

**c. Đang ở trang 2 bấm sắp xếp thì có về trang 1 không** — CÓ. Sau khi lật sang trang 2
(`"Hiển thị 21–40 / 50 dự án"`) rồi bấm sắp xếp cột "Giá trị", bảng hiện lại
`"Hiển thị 1–20 / 50 dự án"` — trang tự về 1, đúng yêu cầu (khớp `this.page = 1` trong `onSort()`).

## 8. Ràng buộc đã giữ

- `md5 -q pages/assign/report/prospective-project-results/index.vue` KHÔNG đổi
  (`fa141320b6a5f4732a4d23b635eb7e1a` trước/sau) — props/events với màn cha không đổi.
- `modal-id="tkt-project-list-modal"` giữ nguyên.
- KHÔNG sửa `COLUMN_DEFS` lẫn dữ liệu BE trả về — chỉ thêm `ALIGN_CLASS_MAP` làm cầu nối `align` →
  `cellClass` bên ngoài.
- KHÔNG gắn `reportDrillListMixin`.
- Không đụng `V2BaseSmartFilterPanel.vue`, `ReportPrintPreviewModal.vue`, `CareTrackingTable.vue`,
  `potential-customer-care/index.vue`, `measure-popup.mjs`, `baseline*.json`.
- Không đụng DB.

## 9. Kiểm bằng Playwright thật (bắt buộc theo CLAUDE.md)

Đã mở popup thật trên `http://127.0.0.1:3000/assign/report/prospective-project-results` (Playwright
MCP, phiên đăng nhập sẵn có), kiểm: mở popup, lật trang, sắp xếp 2 cột (chữ + ngày, đối chiếu đúng
`sortTextAsc`/`sortDateAsc` baseline), bấm sắp xếp khi đang ở trang 2 (về trang 1), mở/đóng khối
tổng hợp (KPI 6 ô + chip phân bổ 2 nhóm), bấm nút Phóng to (đúng class `report-drill-dialog--full`),
đóng bằng nút "Đóng" ở footer và nút X ở header, mở lại lần 2 (xác nhận fullscreen + trang tự reset
về trạng thái đầu, không mang state lượt trước sang). Không có lỗi console mới phát sinh (lỗi
`menu-settings 400` có sẵn từ trước, không liên quan popup).

## 10. Commit

Đã `git add` đích danh `ProjectListModal.vue` rồi commit (KHÔNG `git add -A`).
