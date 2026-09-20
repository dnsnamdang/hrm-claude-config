# Task 9 — Chuyển `DevelopmentDrillModal` sang vỏ dùng chung + mixin

## Kết quả

`pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue`
**1204 -> 1053 dòng**. Dựng trên `components/report/V2BaseReportModal.vue` +
`utils/mixins/reportDrillListMixin.js`, cùng khuôn với popup gốc (`DemandListModal.vue`).
`pages/assign/report/customer-market-development/index.vue` **KHÔNG bị đụng** — MD5 trước/sau đều
`f224cf336f52c0d5aded5a90e78b4c31`.

## Đặc điểm riêng của popup này so với popup gốc

Popup gốc (`DemandListModal`) lọc ở SERVER — `applyLocalFilters()` của mixin không được dùng.
Popup này lọc CLIENT-SIDE trên mảng `rows` đã tải sẵn, nhưng `applyLocalFilters()` của mixin **vẫn
không hợp**: nó so `row[param]` trực tiếp, còn ô lọc ở đây khai theo id khác tên field thật
(`market` ứng với `province_id`, `dept` ứng với `department_id`…) — nên GIỮ hàm lọc riêng
`filteredRows` (nguyên logic cũ, chỉ đổi `ownFilters` -> `filters`).

Vì lọc client-side, `sortedRows` của mixin (vốn sắp thẳng `this.rows` — TẬP THÔ) không dùng được
nguyên bản. Giải pháp: **override đúng 1 computed `sortedRows`** trong component (Vue ưu tiên
computed của component hơn mixin cùng tên) để nó sắp trên `filteredRows` thay vì `this.rows`.
`pageCount`/`safePage`/`pageOffset`/`pagedRows` của mixin đều đọc qua `this.sortedRows` (không đọc
`this.rows` trực tiếp) nên chỉ cần override 1 chỗ, không phải viết lại cả chuỗi phân trang.

## Đã gỡ bỏ (chuyển sang vỏ, không phải rơi rụng)

- Toàn bộ `<table class="cmd-drill-table">` viết tay + `<V2BaseTableScroll>` + `<V2BasePagination>`
  thủ công trong template — vỏ tự vẽ bảng theo `columns`/`rows`, cột STT, phân trang.
- `syncTableHeight()` + `trimTableOverflow()` + data `tableMaxHeight` + `MIN_TABLE_HEIGHT` + 2
  listener `resize` ở `mounted()`/`beforeDestroy()` — toàn bộ cơ chế đo chiều cao thủ công (đã có
  comment dài giải thích lý do) được thay bằng `max-table-height=""` (không truyền, để vỏ tự flex-
  fill), đúng cơ chế đã dùng cho popup gốc.
- Cuộn-về-đầu khi lật trang: TRƯỚC ĐÂY KHÔNG CÓ ở popup này (vùng cuộn là cả thân popup, không tách
  riêng theo trang) — nay có, do vỏ tự làm (`resetScroll()` trong `V2BaseReportModal`). Đây là hành
  vi MỚI thêm, không phải mất đi.
- `<style lang="scss">.cmd-drill-dialog { max-width: 1400px; width: 96vw; }</style>` (unscoped, đầu
  file cũ) — vỏ mặc định `.report-drill-dialog { max-width: 1400px; }` đã đủ (đo runtime: dialog
  vẫn hiển thị đúng khổ rộng, xem mục "3 phép đo thêm").
- Prop `loading` TRƯỚC ĐÂY khai nhưng KHÔNG dùng ở đâu trong template (đã kiểm bằng grep trên file
  gốc) — vỏ dùng nó để hiện "Đang tải…" thay ô rỗng lúc `drill.loading = true`. Đây là một khe hở cũ
  được vá tự nhiên, không phải hành vi cố ý thêm mới trong task này.

## Bảng so `measure-popup.mjs` với `baseline-cmd.json`

Lệnh chạy (đúng tham số ghi trong `task-8-report.md`):
```
cd .plans/gop-db/base-popup-bao-cao
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" node measure-popup.mjs /tmp/after-cmd.json \
  --url="http://127.0.0.1:3000/assign/report/customer-market-development" \
  --sort-text="Phòng ban" --sort-date="Ngày họp"
```

| Khoá | baseline-cmd.json | Sau chuyển | Khớp? |
| --- | --- | --- | --- |
| `cols` (12 cột) | đúng thứ tự | **giống hệt** | ✅ |
| `firstPageRowCount` | 20 | 20 | ✅ |
| `sttFirst` / `sttLast` | "1" / "20" | "1" / "20" | ✅ |
| `pageTotal` | "Hiển thị 1–20 / 598 meeting" | giống hệt | ✅ |
| `footerButtonGaps` | 2 cặp, đều 8px | 2 cặp, đều 8px | ✅ |
| `sortTextAsc` (20 phần tử, "Phòng ban") | mảng cụ thể | **giống hệt từng phần tử** | ✅ |
| `sortDateAsc` (20 phần tử, "Ngày họp") | mảng cụ thể | **giống hệt từng phần tử** | ✅ |
| `tableBottom` | 633 | 645 | ⚠️ lệch — xem lý do |
| `footerTop` | 719 | 787 | ⚠️ lệch — xem lý do |
| `heightNormal` | 752 | 844 | ⚠️ lệch — xem lý do |
| `tableScrollBorderTopWidth` | "0px" | "1px" | ⚠️ lệch — xem lý do |
| `tableScrollBorderRadius` | "0px" | "6px" | ⚠️ lệch — xem lý do |
| `modalContentOverflow` | "visible" | "hidden" | ⚠️ lệch — xem lý do |
| `heightFull` | null (popup cũ không có nút Phóng to) | 900 | ⚠️ lệch — tính năng MỚI |

**Lý do 7 khoá lệch — KHÔNG sửa code, đây là hệ quả CHỦ Ý của việc đứng chung 1 vỏ:**
`V2BaseModal` (vỏ cũ của popup này) và `V2BaseReportModal` (vỏ mới, dùng chung cả 3 popup) có CSS
khung khác nhau — `.report-drill-dialog .modal-content { height: 92vh }` (cố định) thay vì
`max-body-height="70vh"` (co theo nội dung), và `.report-drill-wrap` có viền 1px/bo góc 6px/
`overflow:hidden` theo thiết kế vỏ. Đây CHÍNH XÁC là bộ giá trị mà popup GỐC (`potential-customer-
care`, đã đứng trên vỏ này từ Phase 1) có sẵn trong `baseline.json` của nó (1px/6px/hidden), và
popup TKT (Task 8, dự đoán trước khi chuyển) cũng ghi nhận cùng kết luận này. `heightFull` chuyển từ
`null` sang `900` vì vỏ mới có nút "Phóng to toàn màn hình" mà `V2BaseModal` không có — tính năng
MỚI THÊM (do đứng chung vỏ), không phải bịa số. Không có khoá nào trong 7 khoá này phản ánh dữ liệu/
nghiệp vụ hỏng — toàn bộ khoá "nội dung thật" (cols, sort, phân trang, footer gap) đều khớp baseline
100%.

## 3 phép đo thêm (baseline không bắt được)

1. **`getComputedStyle` của ô có `cellClass`** (đo trên dòng đầu, node mặc định):
   - Cột "Giá trị dự kiến (đ)" (`cellClass: cmd-money` -> map `report-drill-table__money`,
     unscoped): `textAlign: "right"`, `fontWeight: "700"`, `className: "report-drill-table__money"`.
   - Cột "Ngày họp" / "Ngày tạo meeting" (`cellClass: cmd-center` -> map
     `report-drill-table__center`, lớp CÓ SẴN của vỏ): `textAlign: "center"` cả hai.
   - Xác nhận đúng Lesson 1 của brief: 2 lớp `cellClass` này chỉ áp dụng đúng khi định nghĩa nằm
     KHÔNG scoped (`report-drill-table__money`, đặt ở cuối file) hoặc tái dùng lớp scoped của
     CHÍNH VỎ (`report-drill-table__center`, vì `<td>` mang `data-v-xxx` của vỏ, không phải của
     file này).
2. **Đếm request khi mở popup**: 3 request — 2 request là của MÀN CHA (`GET
   .../customer-market-development` + `GET .../drill`, do `index.vue::openDrill()` gọi TRƯỚC KHI
   mở popup, hoàn toàn không đổi vì `index.vue` không bị đụng) và 1 request là font `fa-solid-
   900.woff2` (không liên quan popup). **Bản thân popup phát sinh 0 request** — khớp yêu cầu "không
   tăng so với trước" (trước đây popup cũng không tự gọi API nào, lọc thuần client-side).
3. **Đang ở trang 3, bấm sắp xếp có về trang 1 không**: có. Đo trước khi bấm:
   `"Hiển thị 41–60 / 598 meeting"` (đúng trang 3); sau khi bấm sắp xếp cột "Phòng ban":
   `"Hiển thị 1–20 / 598 meeting"` (về trang 1).

**Kiểm thêm ngoài yêu cầu** (để chắc code không chỉ đúng ở biến thể cột mặc định):
- Biến thể **"Meeting bị huỷ"** (metric `cancelled`, dòng có `plan.cancelled > 0`): 10 cột đúng thứ
  tự chốt (`STT · Tên meeting · Ngày tạo meeting · Ngày họp · Lý do huỷ · Loại meeting · Khách hàng
  · Phòng ban · Bộ phận · Nhân viên chủ trì`, KHÔNG có Trạng thái/2 cột nhu cầu), slot `#cell-cancel`
  render đúng lý do huỷ.
- Biến thể **"KH mới"** (metric `new`): **KHÔNG kiểm được bằng dữ liệu thật** — mọi dòng cấp 1 (14
  dòng) và cả dòng TỔNG của kỳ mặc định ("Tháng này") đều có `new_customers = 0` nên không có nút
  bấm mở popup này (`DrillCell` chỉ render `<button>` khi giá trị khác 0). Đã đọc lại code (slot
  `#cell-cus_created` dùng đúng hàm `date()` đã kiểm chứng ở slot `#cell-created`/`#cell-date`, cột
  `columns()` biến thể này không đổi) nhưng chưa xác nhận trên DOM thật. Không thuộc phạm vi việc
  script `measure-popup.mjs` đo (baseline cũng chỉ chụp biến thể mặc định).

## Bảng đối chiếu class khai/dùng (Lesson 2 + 6)

Rà toàn bộ class khai trong khối `<style lang="scss" scoped>` (31 lớp) đối chiếu với template
(dòng 34-201, gồm cả slot tĩnh và `:class` động dùng template literal `` `report-drill-kpi--${kpi.tone}` ``):

- **Khai mà không dùng: RỖNG.** 29/31 lớp xuất hiện trực tiếp (`grep` ra ≥1 lần); 2 lớp còn lại
  (`report-drill-kpi--good`, `report-drill-kpi--bad`) được gắn ĐỘNG qua
  `` :class="`report-drill-kpi--${kpi.tone}`" `` với `kpi.tone` nhận giá trị `'good'`/`'bad'`/`'main'`
  (`'main'` không có lớp `--main` — ĐÚNG bản gốc, bản gốc cũng chỉ có `--good`/`--bad`).
- **2 lớp `cellClass` cũ (`cmd-center`, `cmd-money`) ĐÃ XOÁ khỏi khối scoped** — không định nghĩa lại
  trong file này nữa. `cmd-center` map sang lớp CÓ SẴN của vỏ (`report-drill-table__center`,
  scoped TRONG `V2BaseReportModal.vue`); `cmd-money` map sang `report-drill-table__money`, định
  nghĩa KHÔNG scoped ở cuối file (bắt buộc, vì `<td>` do vỏ render — xem Lesson 1, đã đo lại ở mục
  "3 phép đo thêm" phía trên để xác nhận không lặp lỗi cũ).
- **Toàn bộ tiền tố `cmd-drill-*` đã đổi thành `report-drill-*`** (`cmd-drill-filters/search/filter/
  count`, `cmd-sumhead*`, `cmd-sumwrap`, `cmd-sumbox*`, `cmd-kpi*`, `cmd-sum*`, `cmd-clamp`,
  `cmd-newchip`, `cmd-cancel__*`). `rsum-toggle`/`rsum-toggle--collapsed` GIỮ NGUYÊN tên (không có
  tiền tố `cmd-`, đúng khuôn dùng chung với khối tổng hợp màn chính, khớp cách `DemandListModal.vue`
  cũng giữ nguyên tên này).
- `modal-id="cmd-drill-modal"` GIỮ NGUYÊN (không đổi) — đây là ID định danh popup, không phải class
  CSS, cùng cách `DemandListModal.vue` giữ `modal-id="care-demand-list-modal"` (tiền tố `care-`,
  không đổi thành `report-drill-`).
- Lớp `.cmd-drill-table`/`.cmd-sortable`/`.cmd-sort*`/`.cmd-drill-empty` (khuôn bảng tự chế cũ) —
  **xoá hẳn**, không còn nơi dùng vì vỏ tự vẽ bảng.

## Ràng buộc đã tuân thủ

- Không sửa `pages/assign/report/customer-market-development/index.vue` (MD5 khớp), không sửa
  `measure-popup.mjs`/`baseline-cmd.json`, không đụng DB, không đổi nhánh (vẫn `gop_db`), không
  `git add -A` (chỉ add đích danh file task), không tự tạo subagent.
- Đã chạy Playwright thật (không dùng MCP — theo đúng cách Task 8 đã dùng: script Node độc lập với
  `storageState: /tmp/care-state.json`) để kiểm TRƯỚC KHI báo hoàn thành: mở popup biến thể mặc định
  + biến thể huỷ, gõ tìm kiếm, mở/thu khối tổng hợp, đổi trang, bấm sắp xếp, phóng to, đóng popup —
  không có lỗi/cảnh báo Vue nào phát sinh từ file đã sửa (console chỉ có cảnh báo framework có sẵn
  không liên quan: hot-update preload, `router-link` deprecation, và 1 lỗi 400 của
  `GET /api/v1/menu-settings` — đã xác nhận KHÔNG liên quan tới popup này, xảy ra ngay từ lúc tải
  trang, trước khi bấm mở popup).
