# Task 3 — báo cáo: `V2BaseReportModal.vue`

## Vòng sửa 3/5 (nối tiếp — đọc từ dưới lên: gốc → vòng 1 → vòng 2 → vòng 3)

Vòng 2 xử lý xong 2 finding cũ (đều ADDRESSED), nhưng việc bọc `<div class="report-drill-footer">`
quanh `<slot name="footer">` lại đẻ ra 1 lỗi mới.

### Finding (Important, phát sinh từ chính diff vòng 2/5): hàng nút footer mất khoảng cách

`V2BaseModal` render sẵn `<div class="modal-footer v2-modal-footer">` bao ngoài slot `#footer`.
Bootstrap 4.6 có rule `.modal-footer > * { margin: 0.25rem }` — **chỉ áp cho con TRỰC TIẾP**. Trước
vòng 2, các nút của Task 5 (khi đặt vào slot) là con trực tiếp nên tự có margin 4px mỗi bên (đúng
8px giữa 2 nút, khớp bản gốc `.care-drill-footer { gap: 8px }`). Sau khi vòng 2 bọc thêm
`<div class="report-drill-footer">`, con trực tiếp duy nhất là cái div đó — các nút bên trong rơi
về `inline-block` mặc định, mà `.report-drill-footer` chỉ có `flex-shrink: 0`, không `display:flex`
lẫn `gap` → hàng nút dính sát nhau.

**Đã sửa theo đúng ruling — BỎ HẲN wrapper, không đắp thêm style:**

1. Gỡ `<div class="report-drill-footer">` khỏi `<template #footer>` — `<slot name="footer">` nằm
   thẳng trong `<template #footer>` như trước vòng 2 (template dòng 99–101).
2. Xoá luôn rule `.report-drill-footer` khỏi khối style KHÔNG scoped (chỉ còn
   `.report-drill-paging { flex-shrink: 0; }`, thêm comment giải thích lý do gỡ để vòng sau không
   lặp lại lỗi này).

Lý do chọn xoá thay vì thêm `display:flex; gap:8px` (đúng như ruling của coordinator): 2 popup khác
dựng trên `V2BaseModal` (`ProjectListModal.vue`, `DevelopmentDrillModal.vue`) đều đặt nút thẳng vào
slot `#footer`, không bọc gì, và margin mặc định của bootstrap đã cho đúng khoảng cách bản gốc —
đắp thêm style chỉ để bù lại thứ vừa tự làm mất là đi vòng, đúng kiểu lỗi "class khai ra rồi mới đi
tìm chỗ gắn" mà 2 vòng sửa trước đã gặp (ngược thứ tự đúng: có phần tử thật rồi mới có style).

### Đo bằng số — lệnh + output thật

Trang nháp tạm mount `V2BaseReportModal`, slot `footer` có 2 nút thật với `id` riêng
(`#tmp-footer-btn-1` = "Đóng", `#tmp-footer-btn-2` = "Xuất Excel") để đo toạ độ chính xác. Đo bằng
Playwright Node (Node 20, chạy trong `e2e/`), dùng phiên có sẵn `/tmp/care-state.json` (KHÔNG đăng
nhập lại), viewport `1440×900`.

```json
{
  "gapCheck": { "found": true, "btn1Right": 1296.09375, "btn2Left": 1304.09375, "gap": 8 },
  "footerDirectChildren": {
    "found": true,
    "count": 2,
    "tagNames": ["BUTTON#tmp-footer-btn-1", "BUTTON#tmp-footer-btn-2"]
  },
  "overlapCheck": {
    "found": true,
    "wrapBottom": 550.8746795654297,
    "footerTop": 636.8746948242188,
    "noOverlap": true
  }
}
```

Đối chiếu 3 yêu cầu của coordinator:

1. Khoảng cách ngang thật giữa 2 nút (`btn2.left - btn1.right`) = **`8px`** — dương, đúng bằng 8px
   bản gốc (`margin: 0.25rem` × 2 cạnh chạm nhau = 8px).
2. Số con trực tiếp của `.modal-footer` = **`2`**, đúng bằng 2 nút đặt trong slot — không còn div
   bọc nào chen giữa (`tagNames` liệt kê đúng 2 thẻ `BUTTON`, không có `DIV`).
3. `wrapBottom (550.87) ≤ footerTop (636.87)` → `noOverlap: true` — vẫn KHÔNG có hiện tượng bảng
   chạy xuyên hàng nút sau khi gỡ wrapper (số liệu lần này thấp hơn vòng 2 một chút do trang nháp
   lần này không còn div bọc quanh nút, chiều cao footer đổi nhẹ — không ảnh hưởng logic so sánh).

Ảnh chụp cùng phiên đo (không lưu lại, đã xoá cùng file nháp): 2 nút "Đóng" / "Xuất Excel" ở footer
có khoảng cách rõ ràng, không còn dính sát nhau.

### Cập nhật bảng đối chiếu class (bỏ dòng `.report-drill-footer`)

Bảng đầy đủ ở mục "Vòng sửa 2/5" bên dưới nay có 1 thay đổi: **xoá dòng `.report-drill-footer`**
(không còn khai trong CSS, không còn phần tử nào cần nó). Toàn bộ các dòng còn lại trong bảng đó
vẫn đúng nguyên trạng — không có class nào khác bị ảnh hưởng bởi vòng sửa 3/5 này. Bảng rút gọn tại
thời điểm hiện tại (sau vòng 3/5), liệt kê lại đầy đủ để không phải lật ngược 2 vòng trước:

| Class khai trong `<style>` | Có mặt trong template không | Cách gắn |
|---|---|---|
| `.report-drill-dialog` | Có | Giá trị mặc định prop `dialogClass`, truyền vào `:dialog-class` của `V2BaseModal` → `b-modal` |
| `.report-drill-dialog--full` | Có | Nối thêm vào `dialogClass` khi `fullscreen === true` |
| `.report-drill-dialog .modal-content` | Có | `.modal-content` là DOM mặc định bootstrap-vue trong `.modal-dialog` (mang `.report-drill-dialog`) |
| `.report-drill-dialog .modal-header` | Có | tương tự |
| `.report-drill-dialog .modal-body` | Có | tương tự |
| `.report-drill-dialog--full .modal-content` | Có (khi fullscreen) | tương tự, chỉ áp khi class `--full` có mặt |
| `.report-drill-scroll` | Có | Div bọc `<V2BaseTableScroll>` (template dòng 53, 85) |
| `.report-drill-paging` | Có | `class="report-drill-paging"` trên `<V2BasePagination>` — Vue 2 merge class lên phần tử ROOT của component |
| `.report-drill-wrap` | Có | Prop `body-class="report-drill-wrap"` truyền vào `<V2BaseTableScroll>` |
| `.report-drill-wrap::-webkit-scrollbar` / `-track` / `-thumb` / `-thumb:hover` | Có | Cùng phần tử `.report-drill-wrap` |
| `.report-drill-head` (+ `__text`, `__title`, `__lead`, `__object`, `__sub`, `__actions`, `__btn`) | Có | Slot `#header` |
| `.report-drill-table` (+ `th,td`, `thead th`, `tbody tr:hover td`) | Có | `<table>` trong slot mặc định của `V2BaseTableScroll` |
| `.report-drill-table__center` | Có | `<td>` cột STT |
| `.report-drill-table__empty` | Có | `<td>` khi `!rows.length` |
| `.report-drill-sort` (+ `i`, `:hover i`) | Có | `<span>` tiêu đề cột |

**Không còn dòng nào "khai mà không dùng".** `.report-drill-footer` đã được GỠ HẲN khỏi cả template
lẫn CSS (không phải "gắn thêm chỗ dùng" như 2 lần trước) — cách xử lý đúng cho trường hợp lớp CSS
tự nó không mang thêm giá trị (chỉ `flex-shrink: 0`, không tạo `gap`) và có sẵn hành vi thay thế từ
Bootstrap khi không có wrapper.

### Dọn dẹp + git status

```
$ rm -f pages/tmp-task3-smoke.vue e2e/tmp-measure-round3.js /tmp/round3-check.png
$ git status --porcelain   # (hrm-client)
 M components/V2BaseSmartFilterPanel.vue
 M components/print/ReportPrintPreviewModal.vue
 M components/report/V2BaseReportModal.vue
 M pages/assign/report/potential-customer-care/components/CareTrackingTable.vue
 M pages/assign/report/potential-customer-care/index.vue
$ curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "http_code=%{http_code}\n" --max-time 30
http_code=200
```

Không có `tmp-task3-smoke.vue` — đã dọn sạch. 4 file sửa dở của việc khác vẫn `M`, không đụng.

### Commit vòng sửa 3/5

```
$ git add components/report/V2BaseReportModal.vue
$ git commit -m "fix(report): gỡ wrapper .report-drill-footer làm mất margin bootstrap giữa nút (vòng sửa 3/5)"
[gop_db b41b207cc] fix(report): gỡ wrapper .report-drill-footer làm mất margin bootstrap giữa nút (vòng sửa 3/5)
 1 file changed, 10 insertions(+), 4 deletions(-)
```

Commit vòng sửa 3/5: **`b41b207cc`**.

---

## Vòng sửa 2/5 (nối tiếp — đọc từ dưới lên: gốc → vòng 1 → vòng 2)

Người rà soát tìm ra 1 lỗi Critical + 1 lỗi Important, cùng họ với lỗi vòng 1 (class khai mà
không có phần tử nào mang) nhưng ở 2 chỗ tôi chưa đo tới.

### Finding 1 (Critical): `.report-drill-content` chết 100%

Bản gốc gắn class qua `content-class="care-drill-content"` thẳng trên `<b-modal>`
(`DemandListModal.vue:29`). Nhưng `V2BaseModal.vue:20` hard-code `content-class="shadow"`, không
có prop nào để truyền content-class tuỳ biến — sửa `V2BaseModal` là ngoài phạm vi Task 3 (ruling
của coordinator). **Đã sửa**: đổi từ class độc lập `.report-drill-content` sang selector hậu duệ
bám `.report-drill-dialog` (class này ĐÃ áp đúng qua prop `dialogClass` có sẵn), giữ NGUYÊN mọi giá
trị bên trong:

- `.report-drill-content` → `.report-drill-dialog .modal-content`
- `.report-drill-content .modal-header` → `.report-drill-dialog .modal-header`
- `.report-drill-content .modal-body` → `.report-drill-dialog .modal-body`
- `.report-drill-dialog--full .report-drill-content` → `.report-drill-dialog--full .modal-content`

### Finding 2 (Important): `.report-drill-scroll` cũng chết + `flex` trên `.report-drill-wrap` vô tác dụng

Không phần tử nào mang class `report-drill-scroll`; `V2BaseTableScroll` chỉ có prop `bodyClass`
(gắn vùng cuộn BÊN TRONG), không có prop cho thẻ bọc ngoài. Hệ quả kéo theo: `flex: 1 1 auto` trên
`.report-drill-wrap` không tác dụng vì không có tổ tiên nào là flex container. **Đã sửa**: bọc
`<V2BaseTableScroll>` trong `<div class="report-drill-scroll">` (template dòng 53–85). Đo sau khi
bọc không thấy bố cục xấu đi (xem số đo + ảnh chụp bên dưới) — không cần báo lại coordinator để xin
ý kiến xoá bớt rule.

### Tự rà thêm (ngoài 2 finding của coordinator): `.report-drill-footer` cũng chết

Khi làm bảng đối chiếu class theo yêu cầu ở cuối, phát hiện thêm `.report-drill-footer` (khai ở
khối KHÔNG scoped, `flex-shrink: 0`) không có phần tử nào mang class đó — `<template #footer>` chỉ
có `<slot name="footer"></slot>` trần, không có div bọc. Đối chiếu với file nguồn
(`DemandListModal.vue:273`): `.care-drill-footer` bọc đúng 3 nút hành động (Đóng/In/Xuất Excel) ở
footer. **Đã sửa theo cùng logic 2 finding trên** (không hỏi lại vì cùng loại lỗi, cùng cách sửa đã
được duyệt: bọc bằng 1 div mang đúng class): đổi
`<template #footer><slot name="footer"></slot></template>` thành
`<template #footer><div class="report-drill-footer"><slot name="footer"></slot></div></template>`.
Nêu ra ở đây để coordinator biết đây là tôi tự phát hiện thêm, không phải nằm trong 2 finding gốc.

### Đo bằng số — lệnh + output thật

Trang nháp tạm mount `V2BaseReportModal` với `visible: true`, 30 dòng dữ liệu giả, slot `footer`
có 2 nút thật (để `.report-drill-footer` có nội dung đo được). Đo bằng Playwright Node (Node 20,
chạy trong `e2e/` để resolve `node_modules/playwright`), dùng phiên có sẵn `/tmp/care-state.json`
(KHÔNG đăng nhập lại), viewport `1440×900`.

```json
{
  "modalContent": { "found": true, "height": "828px", "overflow": "hidden" },
  "modalHeader": { "found": true, "paddingTop": "0px", "borderBottomWidth": "0px" },
  "reportDrillScroll": { "found": true, "display": "flex", "flexGrow": "1" },
  "overlapCheck": {
    "found": true,
    "wrapBottom": 564.7908477783203,
    "footerTop": 650.7908325195312,
    "noOverlap": true
  },
  "viewportHeight": 900
}
```

Đối chiếu 4 yêu cầu của coordinator:

1. `.modal-content`: `height = 828px` — đúng 92% của viewport 900px (`900 × 0.92 = 828`), KHÔNG
   phải `auto`; `overflow = hidden`. ĐÚNG.
2. `.modal-header`: `padding-top = 0px`, `border-bottom-width = 0px`. ĐÚNG (trước khi sửa Finding 1,
   giá trị này là `padding-top: 16px`, `border-bottom-width: 1px` — mặc định bootstrap `.modal-header`
   — không đo lại lần đó vì đã thấy rõ vấn đề qua code, ưu tiên đo bản ĐÃ SỬA cho đúng trọng tâm
   coordinator yêu cầu).
3. `report-drill-scroll`: tồn tại, `display: flex` (đúng CSS `display:flex; flex-direction:column`
   port từ bản gốc).
4. So đáy bảng với đỉnh hàng nút: `wrapBottom (564.79) ≤ footerTop (650.79)` → `noOverlap: true` —
   KHÔNG còn hiện tượng bảng chạy xuyên hàng nút.

Ảnh chụp cùng phiên đo (không lưu lại, đã xoá cùng file nháp): dải banner navy→teal sát mép trên
(không còn viền/khoảng trắng bootstrap mặc định bao quanh — đúng Finding 1), khung bảng có viền
mảnh, hàng nút "Đóng"/"Xuất Excel" ghim đáy tách biệt với bảng, popup cao hơn hẳn bản trước (khớp
`height: 92vh` giờ đã áp dụng).

### Bảng đối chiếu MỌI class khai trong `<style>` với class thật trong template

| Class khai trong `<style>` | Có mặt trong template không | Cách gắn |
|---|---|---|
| `.report-drill-dialog` | Có | Giá trị mặc định prop `dialogClass`, truyền vào `:dialog-class` của `V2BaseModal` → `b-modal` |
| `.report-drill-dialog--full` | Có | Nối thêm vào `dialogClass` khi `fullscreen === true` (computed inline trong `:dialog-class`) |
| `.report-drill-dialog .modal-content` | Có | `.modal-content` là DOM mặc định bootstrap-vue render bên trong `.modal-dialog` (mang `.report-drill-dialog`) — selector hậu duệ, không cần class riêng |
| `.report-drill-dialog .modal-header` | Có | tương tự, DOM mặc định bootstrap-vue |
| `.report-drill-dialog .modal-body` | Có | tương tự |
| `.report-drill-dialog--full .modal-content` | Có (khi fullscreen) | tương tự, chỉ áp khi class `--full` có mặt |
| `.report-drill-scroll` | Có | Div bọc `<V2BaseTableScroll>` — thêm ở vòng sửa 2/5 (template dòng 53, 85) |
| `.report-drill-footer` | Có | Div bọc `<slot name="footer">` — thêm ở vòng sửa 2/5 (tự phát hiện) |
| `.report-drill-paging` | Có | `class="report-drill-paging"` trên `<V2BasePagination>` — Vue 2 merge class truyền vào component lên phần tử ROOT của nó (`<div class="row paging mt-3">`) |
| `.report-drill-wrap` | Có | Prop `body-class="report-drill-wrap"` truyền vào `<V2BaseTableScroll>` — gắn vào div `ref="body"` bên trong component con (phải để CSS ở khối KHÔNG scoped mới với tới, xem vòng sửa 1/5) |
| `.report-drill-wrap::-webkit-scrollbar` / `-track` / `-thumb` / `-thumb:hover` | Có | Cùng phần tử với `.report-drill-wrap` ở trên |
| `.report-drill-head` | Có | Div gốc trong slot `#header` |
| `.report-drill-head__text` | Có | Div con trong `#header` |
| `.report-drill-head__title` | Có | Div con |
| `.report-drill-head__lead` | Có | Span, `v-if="lead"` |
| `.report-drill-head__object` | Có | Span |
| `.report-drill-head__sub` | Có | Div |
| `.report-drill-head__actions` | Có | Div bọc 2 nút |
| `.report-drill-head__btn` (+ `:hover`) | Có | 2 nút (fullscreen toggle + đóng) |
| `.report-drill-table` (+ `th,td`, `thead th`, `tbody tr:hover td`) | Có | `<table>` trong slot mặc định của `V2BaseTableScroll` |
| `.report-drill-table__center` | Có | `<td>` cột STT |
| `.report-drill-table__empty` | Có | `<td>` khi `!rows.length` |
| `.report-drill-sort` (+ `i`, `:hover i`) | Có | `<span>` tiêu đề cột, `v-if="col.sortable"` |

**Không còn dòng nào "khai mà không dùng".** 3 dòng từng chết (`.report-drill-content` cũ,
`.report-drill-scroll`, `.report-drill-footer`) đều đã có phần tử mang class tương ứng sau vòng sửa
này.

### Dọn dẹp + git status

```
$ rm -f pages/tmp-task3-smoke.vue e2e/tmp-measure-round2.js /tmp/round2-check.png
$ git status --porcelain   # (hrm-client)
 M components/V2BaseSmartFilterPanel.vue
 M components/print/ReportPrintPreviewModal.vue
 M components/report/V2BaseReportModal.vue
 M pages/assign/report/potential-customer-care/components/CareTrackingTable.vue
 M pages/assign/report/potential-customer-care/index.vue
$ curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "http_code=%{http_code}\n" --max-time 30
http_code=200
```

Không có `tmp-task3-smoke.vue` — đã dọn sạch. 4 file sửa dở của việc khác vẫn `M`, không đụng.

### Commit vòng sửa 2/5

```
$ git add components/report/V2BaseReportModal.vue
$ git commit -m "fix(report): sửa .report-drill-content/.report-drill-scroll/.report-drill-footer chết (vòng sửa 2/5)"
[gop_db 4ccaf4c34] fix(report): sửa .report-drill-content/.report-drill-scroll/.report-drill-footer chết (vòng sửa 2/5)
 1 file changed, 50 insertions(+), 36 deletions(-)
```

Commit vòng sửa 2/5: **`4ccaf4c34`**.

---

## Vòng sửa 1/5 (nối tiếp báo cáo gốc bên dưới)

**Finding của coordinator**: `.care-drill-wrap` ở file nguồn mang `border: 1px solid #e3e8ef` +
`border-radius: 6px` + bộ `::-webkit-scrollbar*`. Tôi đã port sang `.report-drill-wrap` nhưng đặt
trong khối `<style scoped>`, và KHÔNG có phần tử nào trong template Step-1 gắn class đó — hậu quả:
mất viền + mất scrollbar mảnh, và phép đối chiếu toạ độ/số dòng ở Task 6 không bắt được lỗi loại
này.

**Đã sửa theo đúng ruling:**

1. Truyền `body-class="report-drill-wrap"` vào `V2BaseTableScroll` (dòng 53 của component) — class
   giờ gắn thẳng vào vùng cuộn thật (`ref="body"` của `V2BaseTableScroll`).
2. **Phát hiện thêm khi đo (ngoài yêu cầu gốc của coordinator)**: chỉ đổi bước 1 là CHƯA ĐỦ — phần
   tử nhận `body-class` nằm trong **template riêng của `V2BaseTableScroll`** (không phải slot
   content của `V2BaseReportModal`), nên selector `scoped` của `V2BaseReportModal` không với tới
   được nó (đúng cơ chế Vue 2: style `scoped` chỉ gắn `data-v-*` cho phần tử viết trong template của
   CHÍNH component, và cho nội dung đưa vào qua `<slot>` — KHÔNG cho phần tử nằm trong template
   riêng của component con dù được nhận class qua prop). Đo thật lần 1 (xem log dưới) ra
   `border-top-width: 0px`, `border-radius: 0px` — xác nhận đúng cơ chế. **Đã chuyển toàn bộ khối
   `.report-drill-wrap` (viền, bo góc, 4 rule `::-webkit-scrollbar*`) từ khối `<style scoped>` sang
   khối `<style lang="scss">` KHÔNG scoped** (cùng khối đang chứa `.report-drill-dialog`,
   `.report-drill-content`... — đúng lý do đã ghi sẵn ở đầu khối đó). Đo lại (log dưới) ra
   `border-top-width: 1px`, `border-radius: 6px` — khớp bản gốc.
3. Xoá hẳn `.report-drill-topscroll` và 4 selector `::-webkit-scrollbar*` từng gắn kèm nó (đã gộp
   chung với `.report-drill-wrap` từ đầu nên chỉ còn 1 bộ selector `::-webkit-scrollbar*` gắn riêng
   `.report-drill-wrap`, không còn class `report-drill-topscroll` nào trong file). Thanh cuộn phía
   trên nay do chính `V2BaseTableScroll` vẽ bằng `.v2-table-scroll__top scrollbar-thin` của nó.
4. `flex: 1 1 auto` / `min-height: 0` trong `.report-drill-wrap`: **giữ nguyên**, không bỏ — đo thật
   không thấy vỡ bố cục (ảnh chụp + đo số bên dưới), và vì đã chuyển cả khối sang unscoped nên 2
   thuộc tính này giờ cũng thật sự áp dụng (trước đó, khi còn ở khối scoped, cả khối kể cả 2 dòng
   này đều chết, `flexGrow` đo được là `0`; sau khi chuyển đo lại ra `flexGrow: 1`).

### Đo bằng số — lệnh + output thật

Dùng phiên có sẵn `/tmp/care-state.json` (KHÔNG đăng nhập lại), chạy bằng Playwright Node (Node 20,
từ trong `e2e/` để resolve đúng `node_modules/playwright`) nhắm vào trang nháp tạm mount
`V2BaseReportModal` với `visible: true` + 30 dòng dữ liệu giả (đủ để bảng có nội dung thật).

**Lần đo 1 — TRƯỚC khi chuyển khối CSS (còn ở `<style scoped>`), sau khi đã thêm `body-class` ở
bước 1:**

```json
{
  "found": true,
  "classList": "v2-table-scroll__body scrollbar-thin report-drill-wrap",
  "borderTopWidth": "0px",
  "borderRightWidth": "0px",
  "borderBottomWidth": "0px",
  "borderLeftWidth": "0px",
  "borderRadius": "0px",
  "flexGrow": "0"
}
```

**Lần đo 2 — SAU khi chuyển `.report-drill-wrap` sang khối KHÔNG scoped:**

```json
{
  "found": true,
  "classList": "v2-table-scroll__body scrollbar-thin report-drill-wrap",
  "borderTopWidth": "1px",
  "borderRightWidth": "1px",
  "borderBottomWidth": "1px",
  "borderLeftWidth": "1px",
  "borderRadius": "6px",
  "overflowX": "auto",
  "overflowY": "auto",
  "flexGrow": "1",
  "rectWidth": 1384,
  "rectHeight": 450,
  "hasTopScrollbar": true,
  "topScrollbarVisible": false,
  "tableScrollWidth": 1382,
  "wrapClientWidth": 1382
}
```

`border-top-width = 1px`, `border-radius = 6px` — đúng số coordinator yêu cầu chứng minh.
`topScrollbarVisible: false` vì bảng nháp (3 cột, ~800px) chưa tràn khung 1384px popup ở viewport
1440×900 — đúng thiết kế "tự ẩn khi không tràn" của `V2BaseTableScroll`, không phải lỗi.

Chụp thêm 1 ảnh màn hình (cùng script, cùng phiên) để kiểm mắt thường theo ý #2 của coordinator:
popup hiện đúng dải banner navy→teal, khung bảng có viền mảnh xám bao quanh, STT/cột đúng, phân
trang + nút "Đóng" ở footer — không thấy dấu hiệu vỡ bố cục. Ảnh không lưu lại (đã xoá cùng file
nháp, xem dưới).

Trang nháp + script đo đều là file TẠM, đã xoá sạch trước khi commit:

```
$ rm -f pages/tmp-task3-smoke.vue e2e/tmp-measure-report-wrap.js /tmp/report-wrap-check.png
$ git status --porcelain   # (hrm-client)
 M components/V2BaseSmartFilterPanel.vue
 M components/print/ReportPrintPreviewModal.vue
 M components/report/V2BaseReportModal.vue
 M pages/assign/report/potential-customer-care/components/CareTrackingTable.vue
 M pages/assign/report/potential-customer-care/index.vue
$ curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "http_code=%{http_code}\n" --max-time 30
http_code=200
```

Không có `tmp-task3-smoke.vue` trong danh sách — đã dọn sạch. 4 file sửa dở của việc khác vẫn `M`,
không đụng. `e2e/` không phải git repo con của workspace này (`git status` báo `fatal: not a git
repository`) nên script đo tạm trong đó không để lại dấu vết git nào cần dọn thêm ngoài việc xoá
file vật lý (đã làm).

### Commit vòng sửa 1/5

```
$ git add components/report/V2BaseReportModal.vue
$ git commit -m "fix(report): dời .report-drill-wrap sang style không scoped để viền/scrollbar áp đúng vào V2BaseTableScroll"
[gop_db 127285043] fix(report): dời .report-drill-wrap sang style không scoped để viền/scrollbar áp đúng vào V2BaseTableScroll
 1 file changed, 32 insertions(+), 36 deletions(-)
```

Commit vòng sửa 1/5: **`127285043`**.

---

## Đã làm (báo cáo gốc)

- Đọc `.plans/base-popup-bao-cao/.sdd/task-3-brief.md`.
- Đọc `components/modal/V2BaseModal.vue` (Task 2) để xác nhận slot `header` (expose `close`) và prop `noEnforceFocus` (default `false`, đổ xuống `:no-enforce-focus` của `b-modal`) đã tồn tại đúng như brief mô tả.
- Đọc `components/V2BaseTableScroll.vue` (prop `maxHeight`, tự đồng bộ 2 thanh cuộn, tự ẩn khi không tràn) và `components/V2BasePagination.vue` (props `currentPage/currentPageSize/totalRows/itemLabel/pageSizeOptions`, events `page-change`/`page-size-change`) — khớp tên prop/event mà brief dùng trong template mẫu.
- Đọc toàn bộ `pages/assign/report/potential-customer-care/components/DemandListModal.vue` — 2 khối `<style>`:
  - dòng 846–908: khối `<style lang="scss">` KHÔNG scoped.
  - dòng 910–1307: khối `<style lang="scss" scoped>`.
- Tạo file mới **`components/report/V2BaseReportModal.vue`** (373 dòng) — copy nguyên văn template + script Step 1 của brief (không chỉnh), và tự viết phần `<style>` theo đúng chỉ dẫn "CHÉP NGUYÊN ... đổi tiền tố, giữ nguyên số" (chi tiết bảng đối chiếu bên dưới).
- Không đụng `DemandListModal.vue` và 4 file đang sửa dở của việc khác (`components/V2BaseSmartFilterPanel.vue`, `components/print/ReportPrintPreviewModal.vue`, `pages/assign/report/potential-customer-care/components/CareTrackingTable.vue`, `pages/assign/report/potential-customer-care/index.vue`) — xác nhận bằng `git status --porcelain` trước và sau commit, 4 file này vẫn ở trạng thái `M` chưa staged.
- Commit chỉ đúng 1 file mới, dùng `git add components/report/V2BaseReportModal.vue` (không `-A`).

## Danh sách lớp CSS đã port — nguồn dòng trong `DemandListModal.vue`

**Khối KHÔNG scoped (nguồn dòng 846–908)** — port full, đổi tiền tố `care-drill` → `report-drill`:

| Lớp | Nguồn dòng |
|---|---|
| `.report-drill-dialog` | brief đã cho sẵn giá trị literal (`max-width: 1400px;`) — **KHÔNG** mang theo `width: 96vw` của bản gốc dòng 849–852, vì Step-1 code block của brief ghi rõ chỉ `max-width: 1400px`, coi đây là quyết định đã chốt ghi đè hướng dẫn "giữ nguyên số" |
| `.report-drill-dialog--full` | brief cho sẵn literal, khớp dòng 897–902 |
| `.report-drill-content` (+ `.modal-header` / `.modal-body` lồng bên trong) | dòng 856–882 |
| `.report-drill-scroll` | dòng 883–889 (bản trong khối KHÔNG scoped: `flex/min-height/display/flex-direction`) |
| `.report-drill-footer`, `.report-drill-paging` | dòng 890–893 |
| `.report-drill-dialog--full .report-drill-content` | dòng 903–907 |

**Khối scoped (nguồn dòng 910–1307)** — chỉ lấy đúng danh sách brief liệt kê, đổi tiền tố:

| Lớp | Nguồn dòng |
|---|---|
| biến `$navy-start`, `$teal`, `$text-muted` | dòng 912, 913, 916 (chỉ giữ 3 biến thực sự được dùng trong các lớp port; bỏ `$teal-dark`, `$text-main` vì không lớp nào trong phạm vi port dùng tới) |
| `.report-drill-head` | dòng 918–927 |
| `.report-drill-head__text` | dòng 928–931 |
| `.report-drill-head__title` | dòng 932–938 |
| `.report-drill-head__lead` | dòng 940–943 |
| `.report-drill-head__object` | dòng 944–947 |
| `.report-drill-head__sub` | dòng 948–953 |
| `.report-drill-head__actions` | dòng 954–959 |
| `.report-drill-head__btn` | dòng 960–975 |
| `.report-drill-topscroll` (+ hover/scrollbar) | dòng 1156–1161, 1172–1190 |
| `.report-drill-wrap` (+ hover/scrollbar) | dòng 1162–1170, 1172–1190 |
| `.report-drill-table` (+ `th/td`, `thead th`, `tbody tr:hover td`) | dòng 1192–1229 |
| `.report-drill-table__center` | dòng 1230–1232 |
| `.report-drill-table__empty` | dòng 1238–1242 |
| `.report-drill-sort` (+ `i`, `:hover i`) | dòng 1257–1272 |

**Cố tình KHÔNG port** (đúng brief — style riêng của màn, ở lại `DemandListModal.vue` cho Task 5 tự đổi tên sau):
`.care-drill-filters*`, `.care-drill-sum*`, `.rsum-toggle*`, `.care-drill-count`, `.care-drill-back*`, `.care-drill-customer`, `.care-drill-sub`, `.care-drill-link`, `.care-drill-carry`, `.care-drill-table__money`.

Ghi chú: `.report-drill-topscroll` / `.report-drill-wrap` được port đủ theo yêu cầu brief nhưng **không có phần tử nào trong template Step-1 gắn 2 class này** — khung bảng thật sự dùng `V2BaseTableScroll` (đã tự lo đồng bộ 2 thanh cuộn, đúng chỉ dẫn "ĐỪNG viết lại phần đồng bộ 2 thanh cuộn bằng tay"). Hai lớp này coi như port sẵn theo đúng yêu cầu chữ trong brief, hiện chưa được tham chiếu — nêu ra để review biết đây là chủ đích, không phải sót.

## Lệnh + output thật

```
$ curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "http_code=%{http_code}\n" --max-time 90
http_code=200
```

Sau đó tạo thêm trang nháp tạm `pages/tmp-task3-smoke.vue` (import + mount `V2BaseReportModal` với props/slot giả) để kiểm chắc hơn việc SFC thật sự biên dịch (không chỉ page có sẵn không đổi):

```
$ curl -s http://127.0.0.1:3000/tmp-task3-smoke -o /tmp/tmp_smoke_body.html -w "http_code=%{http_code}\n" --max-time 90
http_code=200
```

Mở bằng Playwright MCP (`http://127.0.0.1:3000/tmp-task3-smoke`, đúng quy tắc "luôn `127.0.0.1`, không `localhost`"): trang chạy client-side, không có `Failed to compile`, không có lỗi Vue render nào liên quan tới `V2BaseReportModal`/`V2BaseTableScroll`/`V2BasePagination`; app chạy middleware auth toàn cục bình thường và redirect `/login` (đúng hành vi app, không phải lỗi component). Thử đăng nhập thật bằng tài khoản test (`e2e_assign@test.local` / `.env` của bộ e2e) để xem popup render thật với dữ liệu — API `auth/login` trả `422 Tên đăng nhập hoặc mật khẩu không đúng`, tức DB local hiện không khớp tài khoản test (vấn đề môi trường đã biết, xem mục "Nghi ngờ / hạn chế" — không liên quan code Task 3).

Dọn dẹp trang nháp trước khi commit:

```
$ rm -f pages/tmp-task3-smoke.vue
$ curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "http_code=%{http_code}\n" --max-time 30
http_code=200
```

`git status --porcelain` trước commit:

```
 M components/V2BaseSmartFilterPanel.vue
 M components/print/ReportPrintPreviewModal.vue
 M pages/assign/report/potential-customer-care/components/CareTrackingTable.vue
 M pages/assign/report/potential-customer-care/index.vue
?? components/report/
```

(không có `tmp-task3-smoke.vue` — đã xoá sạch; 4 file sửa dở của việc khác giữ nguyên `M`, không đụng.)

```
$ git add components/report/V2BaseReportModal.vue
$ git diff --cached --stat
 components/report/V2BaseReportModal.vue | 373 ++++++++++++++++++++++++++++++++
 1 file changed, 373 insertions(+)
$ git commit -m "feat(report): thêm V2BaseReportModal làm vỏ dùng chung cho popup báo cáo"
[gop_db eb7b3a7b2] feat(report): thêm V2BaseReportModal làm vỏ dùng chung cho popup báo cáo
 1 file changed, 373 insertions(+)
 create mode 100644 components/report/V2BaseReportModal.vue
```

## Nghi ngờ / hạn chế

1. **Chưa xác nhận được popup render đúng bằng mắt thật (Playwright có tương tác thật) vì DB/tài khoản local hiện không đăng nhập được** (`auth/login` → 422 sai mật khẩu với tài khoản test trong `e2e/.env`). Đây là vấn đề môi trường cục bộ có sẵn từ trước (khớp với ghi nhận trong memory "Lệch schema local vs production" / "ERP local config cache trỏ production"), không phải do thay đổi của Task 3. Đã thử bơm thẳng `access_token` từ `e2e/.auth/user.json` vào `localStorage` — vẫn bị API trả `401` ở `user-profile` (token cũ có thể đã bị vô hiệu/token_version lệch). Bằng chứng biên dịch/mount tôi có được (curl 200 hai lượt + Playwright quan sát app chạy JS bình thường, không có lỗi webpack/Vue liên quan tới component) là bằng chứng gián tiếp, không phải ảnh chụp popup thật đang mở.
2. `.report-drill-topscroll` / `.report-drill-wrap` được port theo đúng chữ trong brief nhưng hiện không có phần tử nào trong component gắn 2 class này (vì bảng dùng `V2BaseTableScroll` có class riêng `v2-table-scroll__*`). Coi đây là port "để sẵn" theo đúng yêu cầu, không phải lỗi — nhưng nêu ra để người review xác nhận đây đúng là chủ đích chứ không phải hiểu sai brief.
3. Task 3 không đổi gì ở `DemandListModal.vue` (đúng phạm vi), nên component mới **hiện chưa được import ở bất kỳ đâu trong app thật** — rủi ro thật sự (props/slot có khớp nghiệp vụ hay không) sẽ chỉ lộ ra khi Task 5 gắn vào màn thật.
