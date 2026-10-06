# Cleanup cuối — dọn nhất quán 3 popup báo cáo (V, P1, P2, P3)

## Trạng thái: HOÀN THÀNH — 7/7 việc + 1 vòng sửa review (5c), đã kiểm chứng bằng Playwright + measure-popup.mjs

## Mã commit
- `48c757916` — nhánh `gop_db`, repo `hrm-client` (5 file, +178/-94) — 7 việc gốc.
- `06f015ef8` — nhánh `gop_db`, repo `hrm-client` (1 file, +11/-4) — sửa vòng review: comment đầu
  `utils/mixins/reportDrillListMixin.js` tự mâu thuẫn về tên state lọc.

---

## Vòng sửa cuối (review 5c) — comment mixin tự mâu thuẫn

**Finding của coordinator**: đoạn cảnh báo cuối comment đầu file (viết ở lượt trước) vừa nói tên
state lọc riêng của popup (`filters`/`ownFilters`) KHÔNG PHẢI hợp đồng chung, vừa nói mixin đọc qua
`this.filters` — tự mâu thuẫn. Thực tế mixin **sở hữu cứng** tên `filters` + `keyword` (khai trong
`data()`, đọc/ghi trong `resetFilterState()`/`resetFilters()`/`hasActiveFilter`); bằng chứng ngay
trong lượt sửa trước: `DevelopmentDrillModal.vue` phải đổi `ownFilters` → `filters` mới dùng được
`hasActiveFilter`. Để nguyên đoạn cũ sẽ khiến người sau tưởng đặt tên tuỳ ý vẫn xài được cơ chế của
mixin → nút "Xoá lọc" gate sai vĩnh viễn mà không lỗi nào báo.

**Đã sửa** (chỉ đổi comment, không đụng code thực thi) — nguyên văn đoạn mới (dòng 19-29 của
`utils/mixins/reportDrillListMixin.js`):

```
 * ⚠️ Đã dùng cơ chế lọc của mixin (`resetFilters()`/`resetFilterState()`/`hasActiveFilter`) thì tên
 * state **`filters` và `keyword` là CỐ ĐỊNH, KHÔNG được đặt tên khác** — mixin tự khai
 * `data(){ filters: this.emptyFilters(), keyword: '' }` và đọc/ghi CỨNG vào đúng 2 tên đó. Bằng
 * chứng: `DevelopmentDrillModal.vue` từng dùng `ownFilters` rồi phải đổi lại thành `filters` mới
 * gọi được `hasActiveFilter`/`resetFilters()` — đặt tên khác thì các hàm trên đọc `this.filters`
 * rỗng của MIXIN (không phải state thật của popup), nút "Xoá lọc" gate SAI mà không có lỗi nào báo.
 * CHỈ CÁC KHOÁ BÊN TRONG `filters` (`province_id`, `customer_id`, `drill_status`…) mới do từng popup
 * tự đặt theo đúng bộ ô lọc của nó qua `emptyFilters()` — đây mới là chỗ KHÔNG có hợp đồng chung,
 * đừng suy diễn 1 khuôn khoá dùng cho cả 3 popup.
 * Popup KHÔNG gắn mixin này (BE lo hết lọc/sắp/phân trang, xem cảnh báo phía trên) thì hoàn toàn tự
 * do đặt tên state theo ý mình — xem `ProjectListModal.vue` (tự đặt `ownFilters`) làm mẫu.
```

Đã đọc lại như người chưa từng biết đợt này: câu trả lời rõ ràng — dùng mixin thì tên PHẢI là
`filters`/`keyword`, chỉ các khoá bên trong `filters` mới tự đặt; không dùng mixin thì tự do đặt tên
(mẫu `ownFilters` của `ProjectListModal.vue`). Không còn mơ hồ.

---

## Việc đã làm

1. **P1 footer** (`DemandListModal.vue`): đổi thứ tự Đóng-đầu/Xuất Excel-primary → **In danh sách
   (secondary) → Xuất Excel danh sách (secondary status="success", icon `ri-file-excel-2-line`) →
   Đóng (tertiary, icon `fas fa-arrow-left`)** — khớp `button-convention/SKILL.md` mục 2b/5 và khớp
   P2/P3.
2. **P1 "Xoá lọc"** — gate bằng `v-if="hasActiveFilter"` (computed có sẵn của mixin).
3. **`.report-drill-table__money`** — dọn khỏi 3 popup (cả CSS lẫn comment giải thích dài), chuyển
   vào khối `<style scoped>` của `V2BaseReportModal.vue`, cạnh `.report-drill-table__center`.
4. **`applyLocalFilters()`** — xoá khỏi mixin (hàm chết, không nơi nào gọi — xác nhận bằng
   `grep -rn "applyLocalFilters"` chỉ còn lại chính định nghĩa cũ + 2 dòng comment tham chiếu, đã
   dọn nốt). `hasActiveFilter` vẫn giữ (đang dùng ở cả P1 và P2).
5. **Bổ sung tài liệu vào code**:
   - `columns` prop của vỏ: liệt kê khoá vỏ dùng (`key`/`field`/`label`/`width`/`sortable`/
     `cellClass`) vs khoá chỉ mixin đọc (`sortType`/`sortFields`).
   - Comment đầu file vỏ: quy tắc cellClass (không-scoped ở popup riêng lẻ; ≥2 popup dùng chung thì
     đưa vào scoped của vỏ), dẫn ví dụ `.report-drill-table__center` + `.report-drill-table__money`.
   - Cuối comment đầu file mixin: quy tắc hành động — popup để BE lo hết lọc/sắp/phân trang thì
     KHÔNG dùng mixin, xem `ProjectListModal.vue` làm mẫu; cảnh báo `filterFields`/tên state lọc
     không phải hợp đồng chung.
6. **P3 bổ sung 2 phần thiếu**:
   - Nút "Xoá lọc" (computed `hasActiveFilter` tự viết từ `ownFilters`, method `resetOwnFilters()`
     xoá sạch rồi gọi `onFilterChange()` — đúng 1 lần `fetchList()`).
   - Chip phân bổ chuyển từ `<span>` trang trí thành `<button>` bấm được (`toggleChip()`/
     `isChipActive()`), ghi thẳng vào `ownFilters[dim]` (ô lọc hiện đúng giá trị chip), gọi
     `onFilterChange()` đúng 1 lần mỗi lượt bấm.
7. **Đo thật `max-table-height`** — xem mục riêng bên dưới. **CÓ lệch**, đã sửa.

---

## 5 nhóm kiểm chứng (số cụ thể — Playwright thật trên `127.0.0.1:3000`, viewport 1440×900)

### 1. Ô tiền — `getComputedStyle(td.report-drill-table__money)`
| Popup | text-align | font-weight |
| --- | --- | --- |
| P1 (care) | `right` | `700` |
| P2 (cmd) | `right` | `700` |
| P3 (tkt) | `right` | `700` |

### 2. Thứ tự nút footer (DOM order, cả 3 popup)
`["In danh sách", "Xuất Excel danh sách", "Đóng"]` — giống hệt nhau, "Đóng" cuối cùng. Khoảng cách
giữa các nút (`footerButtonGaps` từ `measure-popup.mjs`): 8px / 8px ở cả 3 popup.

### 3. P1 — "Xoá lọc"
- Chưa lọc gì: nút **không hiện** trong DOM (`xoaLocVisible: false`) — xác nhận bằng
  `wait_for(text:"Xoá lọc")` timeout 30s (đúng như kỳ vọng).
- Gõ `keyword=a`: nút **hiện** (`xoaLocVisible: true`).
- Bấm "Xoá lọc": network log popup ra thêm **đúng 1** request
  `.../demand-list?period=month&criteria=all&drill=all` (bỏ `keyword`) — trước đó có 2 request
  (mở popup + gõ keyword), sau khi bấm có thêm request thứ 3, không thừa request nào khác. Sau khi
  bấm: input rỗng, nút lại ẩn.

### 4. P3 — chip + "Xoá lọc" (mới bổ sung)
- Bấm chip "Thành phố Hà Nội" (nhóm Thị trường): network **+1 request**
  (`...project-list?...&province_id=2&...`), ô lọc "Thị trường" hiện đúng `Thành phố Hà Nội` (select2
  hiện `×Thành phố Hà Nội`), bảng đổi từ **50 dự án → 18 dự án**, chip chuyển trạng thái active
  (class `report-drill-chip--on`), nút "Xoá lọc" xuất hiện.
- Bấm lại đúng chip đó: **+1 request** (bỏ `province_id`), bảng về 50 dự án, chip tắt active.
- Bật lại chip rồi bấm "Xoá lọc": **+1 request** (bỏ `province_id`), toàn bộ `ownFilters` về `null`,
  0 chip còn active, nút "Xoá lọc" ẩn lại.
- Tổng cộng mỗi thao tác đều đúng 1 request — không có request thừa nào.

### 5. Chạy lại `measure-popup.mjs` cho cả 3 popup, so với baseline
Lệnh (Node 20, cùng thư mục `.plans/gop-db/base-popup-bao-cao`):
```
node measure-popup.mjs <out> --url=<popup> --sort-text=<...> --sort-date=<...>
```
- **`baseline.json` (P1/care)**: KHÔNG có khoá mới nào xuất hiện. Mọi khoá còn lại
  (`cols`, `firstPageRowCount`, `sttFirst/Last`, `pageTotal`, `sortTextAsc`, `sortDateAsc`,
  `heightFull=900`, `heightNormal=844`) **khớp 100%**. `footerTop`/`tableBottom` lệch nhẹ
  (803→787 / 713→709) — **đã điều tra bằng thao tác DOM trực tiếp** (ẩn icon nút Đóng, chèn 100px
  vào hàng lọc, thậm chí XOÁ HẲN 1 nút footer) và xác nhận **cả 3 thao tác đều KHÔNG làm đổi
  `footerTop`/chiều cao footer** — vị trí footer trong khuôn vỏ này bất biến với nội dung do
  layout flex cố định tổng `header+body+footer = 92vh`. Kết luận: lệch này **không do 7 việc sửa
  ở task này**, nhiều khả năng là chênh lệch môi trường giữa 2 lần chạy script (baseline chạy hôm
  trước). Không sửa baseline, không sửa thêm code cho khoá này vì không tái hiện được nguyên nhân
  từ phía code.
- **`baseline-cmd.json` (P2)** và **`baseline-tkt.json` (P3)**: KHÔNG có khoá mới nào xuất hiện.
  Chỉ **mất khoá `heightFullNote`** (dự kiến: khoá này chỉ xuất hiện khi `heightFull === null`;
  nay `heightFull` có giá trị `900` vì 2 popup đã chuyển sang vỏ `V2BaseReportModal` — thay đổi
  KIẾN TRÚC có TỪ TRƯỚC phiên làm việc này, không phải do 7 việc cleanup). Nội dung nghiệp vụ
  (`cols`, `firstPageRowCount`, `sttFirst/Last`, `pageTotal`, `footerButtonGaps`, `sortTextAsc`,
  `sortDateAsc`) **khớp 100%** ở cả 2 file. `tableScrollBorderTopWidth/Radius`/`modalContentOverflow`
  đổi theo kiến trúc vỏ mới (đồng nhất `1px`/`6px`/`hidden` — GIỐNG P1, tốt hơn trạng thái cũ
  `0px`/`0px`/`visible` khi còn 2 vỏ khác nhau).
- **Không sửa bất kỳ file `baseline*.json`** nào trong toàn bộ quá trình.

---

## Việc 7 — đo `max-table-height`, kết luận: **CÓ LỆCH THẬT, đã sửa**

Đo trước khi sửa (thu gọn khối tổng hợp, viewport 900px cao):

| Popup | `.report-drill-wrap` height | `max-height` inline | Khoảng trắng dưới bảng (đến footer) |
| --- | --- | --- | --- |
| P1 (đã có `max-table-height=""`) | 496px | *(không set)* | 78px |
| P2 (mặc định `50vh`) | **450px (kẹp cứng đúng 50vh)** | `50vh` | **143px** |
| P3 (mặc định `50vh`) | **450px (kẹp cứng đúng 50vh)** | `50vh` | **145px** |

`.report-drill-scroll` (khối cha, được phép cao hơn) đo được 527–529px ở P2/P3 — chứng minh bảng
BỊ KẸP dưới mức có thể, để hở 143–145px khoảng trắng vô ích giữa đáy bảng và footer, khác hẳn P1.

**Đã sửa**: thêm `max-table-height=""` vào `DevelopmentDrillModal.vue` và `ProjectListModal.vue`
(giống P1), kèm comment giải thích số đo ngay tại chỗ khai prop.

Đo lại sau khi sửa:

| Popup | `.report-drill-wrap` height | `max-height` inline | Khoảng trắng dưới bảng |
| --- | --- | --- | --- |
| P1 | 496px | *(không set)* | 78px |
| P2 | 515px | *(không set — rỗng)* | **78px** |
| P3 | 517px | *(không set — rỗng)* | **78px** |

Cả 3 popup nay đều còn đúng 78px khoảng trắng dưới bảng (khoảng cách cố định do hàng phân trang +
padding, không phải do kẹp cứng) — **hành vi đã đồng nhất, không còn khoảng trắng lãng phí**.

---

## Kiểm chứng bổ sung (không nằm trong 5 nhóm bắt buộc nhưng đã làm để chắc chắn)

- Console browser: chỉ còn 1 lỗi CŨ, không liên quan (`menu-settings 400`, đã tồn tại từ trước, không
  phải do thay đổi lần này) + 1 lỗi CDN sheetjs (mạng ngoài, không liên quan). Không có lỗi Vue
  compile/runtime nào phát sinh từ 5 file đã sửa.
- `git diff --numstat` trên 5 file đã sửa: số dòng thêm/xoá hợp lý theo đúng nội dung sửa, không có
  dấu hiệu phá line-ending (không file nào bị đánh dấu đổi toàn bộ).
- Không đụng tới file bị cấm: `git status --short` xác nhận 4 file đang có sẵn thay đổi từ trước
  (`V2BaseSmartFilterPanel.vue`, `ReportPrintPreviewModal.vue`, `CareTrackingTable.vue`,
  `potential-customer-care/index.vue`) — session này KHÔNG đụng tới chúng, chỉ 5 file trong phạm vi
  được giao.

---

## Mối lo

- **Lệch `footerTop`/`tableBottom` của P1 so với `baseline.json`** (16px/4px) — đã điều tra kỹ bằng
  thao tác DOM trực tiếp (xem mục 5 ở trên), xác nhận KHÔNG liên quan tới 7 việc sửa trong task này
  (footer bất biến với nội dung trong khuôn layout này). Nhiều khả năng là chênh lệch môi trường
  giữa lần chạy baseline (phiên trước) và lần chạy này. Không tìm được nguyên nhân từ phía code nên
  không sửa mò — nêu ra để người review biết và không nghi ngờ nhầm sang các phần vừa sửa.
- `heightFullNote` biến mất khỏi output đo của P2/P3 — là hệ quả của việc 2 popup này đã chuyển
  sang vỏ `V2BaseReportModal` (đổi TỪ TRƯỚC phiên làm việc, không phải việc của 7 task ở đây), không
  phải lỗi phát sinh mới.
