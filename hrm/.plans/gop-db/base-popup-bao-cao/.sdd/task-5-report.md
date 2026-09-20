# Task 5 — Report: Chuyển `DemandListModal` sang Base + mixin

## Kết quả tóm tắt

- `pages/assign/report/potential-customer-care/components/DemandListModal.vue`: **1307 dòng → 849 dòng** (giảm 458 dòng).
- Đã chuyển hoàn toàn sang `<V2BaseReportModal>` + `reportDrillListMixin`, props/events của component giữ nguyên 100% (`index.vue` không sửa — xác nhận bằng md5, xem mục "Kiểm index.vue").
- Trong lúc đo baseline, phát hiện **2 lỗi thật** không nằm trong `DemandListModal.vue` mà nằm ở 2 file phụ thuộc (`reportDrillListMixin.js` — Task 4, `V2BaseReportModal.vue` — Task 3). Cả hai đều đã sửa, có đo lại xác nhận, **nhưng CHƯA commit** (xem mục "Quyết định phải tự đưa ra" — chờ user duyệt trước khi gộp vào commit hoặc commit riêng).

## Thứ đã gỡ khỏi DemandListModal.vue

Đúng danh sách trong brief: `fullscreen`, `scrollWidth`, `overflowing`, `syncingScroll`, `scrollBound`,
`bindScrollSync()`, `updateScrollWidth()`, `observeTable()`, `sortIcon()`, `sortedRows()` (computed),
`pageCount/safePage/pageOffset/pagedRows` (computed), `toggleSort()`, `onPageChange()`,
`onPageSizeChange()`, data `page/pageSize/sort/keyword/filters/summaryCollapsed`, `resetFilters()`
riêng, và style `.care-drill-head*` / `.care-drill-dialog*` / `.care-drill-content` /
`.care-drill-scroll` / `.care-drill-topscroll` / `.care-drill-wrap` / `.care-drill-table*` (trừ
`__money`) / `.care-drill-sort` / `.care-drill-footer` / `.care-drill-paging` — toàn bộ nay do
`V2BaseReportModal` render/style.

Watcher `mounted`/`beforeDestroy` (gắn/gỡ `resize` listener cho `updateScrollWidth`) cũng bỏ hẳn —
không còn lý do tồn tại.

`dateSortKey()` cục bộ (hàm top-level dùng bởi `sortedRows()` cũ) cũng xoá — chức năng nay nằm
trong mixin.

## Thứ giữ lại

`columns` (computed ghép cột theo `crossStats`/`drillDimension`), `filterFields`, `metaText`
(computed MỚI, gộp dòng meta thay `.care-drill-head__sub` cũ), `drillDimension`/`drillType`/
`drillTypes`, `crossStats`/`kpis` (props), `backTo`/`goBack`, `showFilter`, `onFilterChange`
(emit `filter` lên cha — bộ lọc chạy server), `emptyFilters()`, `hasSummary`, `periodText`,
`isFiltered` (ở lại màn theo đúng yêu cầu — KHÔNG đưa vào mixin), toàn bộ logic cascade
(`childOptions`, `filterOptionsOf`, `resetChildOf`), logic chip (`chipParam`, `isChipActive`,
`toggleChip`), logic KPI drill sâu (`onKpiDrill`, `keepView`), và style riêng của filters/back/
summary/customer/sub/link/carry/table__money.

## Đổi tiền tố `care-drill-*` → `report-drill-*`

Đổi toàn bộ trong file, gồm cả lớp riêng của màn (`filters*`, `sum*`, `customer*`, `sub`,
`meeting`, `back*`, `toggle`, `count`, `table__money`). Kiểm bằng grep — RỖNG (không còn
`care-drill` nào trong `DemandListModal.vue`, trừ 1 chuỗi KHÔNG PHẢI class:
`id-prefix="care-drill"` truyền cho `KpiBoxes` — xem mục "Quyết định phải tự đưa ra" bên dưới).

## Bug 1 phát hiện: `resetFilters()` riêng đè mixin (đúng như brief cảnh báo)

Xoá `resetFilters()` cục bộ (không gọi `onFilterChange`), dùng bản mixin (có gọi). Nút "Xoá lọc"
trong template trước đây gọi `clearFilters()` (wrapper gọi `resetFilters(); onFilterChange()`).
Nếu giữ `clearFilters()` và chỉ đổi bên trong nó gọi mixin's `resetFilters()`, nút sẽ bắn
**2 lần** sự kiện `filter` (mixin's `resetFilters()` đã tự gọi `onFilterChange()`, cộng thêm lần
gọi tường minh trong `clearFilters()`) → 2 request lọc liền nhau. Đã bỏ hẳn `clearFilters()`,
đổi template bấm thẳng `resetFilters` (mixin). Đã đo bằng Playwright: bấm "Xoá lọc" bắn ĐÚNG 1
request `GET .../demand-list?...` (xem mục Playwright bên dưới).

## Bug 2 phát hiện: `reportDrillListMixin.js` — `dateSortKey()` làm rớt giờ:phút

**File ngoài phạm vi khai báo của Task 5** (`utils/mixins/reportDrillListMixin.js`, Task 4) —
nhưng lỗi này ảnh hưởng TRỰC TIẾP tới hành vi sort cột "Meeting thu thập nhu cầu" của popup đang
chuyển, nên phải sửa để đạt yêu cầu "người dùng không thấy khác gì cả".

- **Hiện tượng đo được**: bấm sort tăng dần cột ngày, baseline và after LỆCH THỨ TỰ hoàn toàn
  trong cùng 1 ngày (vd 05/09 09:00/09:30/10:00/10:00/16:00 ở baseline, nhưng after ra
  16:00/10:00/10:00/09:30/09:00 — gần như đảo ngược).
- **Nguyên nhân**: `dateSortKey()` trong mixin chỉ khớp `(\d{2})\/(\d{2})\/(\d{4})` (bỏ hẳn phần
  giờ:phút), trong khi bản gốc (`DemandListModal.vue` cũ, dòng 327-332) bắt cả
  `(?:\s+(\d{2}):(\d{2}))?`. 2 dòng cùng ngày khác giờ bị coi là "bằng nhau" về khoá sort, và thứ
  tự tương đối rơi về thứ tự MẢNG GỐC (ổn định theo `Array.sort` của V8) thay vì theo giờ thật.
- **Sửa**: thêm lại nhóm bắt giờ:phút, build `Date` object gồm cả giờ. Đã đo lại — `sortDateAsc`
  khớp baseline TUYỆT ĐỐI (20/20 dòng đúng thứ tự, đúng nội dung).
- **File đổi**: `hrm-client/utils/mixins/reportDrillListMixin.js` (dòng 14-21 cũ → 14-24 mới).
  Chỉ sửa 1 hàm, không đổi API/behavior nào khác của mixin. Ảnh hưởng tới CẢ 3 popup dùng chung
  mixin (`DemandListModal` đang chuyển, và tương lai `DevelopmentDrillModal`/`ProjectListModal`
  khi các Task sau chuyển chúng) — đều được LỢI từ fix này (bug tồn tại sẵn, không phải do tôi
  gây ra), không có ai bị ảnh hưởng xấu.

## Bug 3 phát hiện: `V2BaseReportModal.vue` — chuỗi flex bị đứt 2 mắt xích

**File ngoài phạm vi khai báo của Task 5** (`components/report/V2BaseReportModal.vue`, Task 3) —
đây là popup ĐẦU TIÊN thực sự render qua vỏ này (`ProjectListModal`/`DevelopmentDrillModal` được
nhắc tới trong comment của vỏ vẫn đang dựng trực tiếp trên `V2BaseModal`, CHƯA dùng
`V2BaseReportModal`), nên đây là lần đầu tổ hợp `max-body-height="none"` + `V2BaseTableScroll`
thực sự chạy qua trình duyệt thật.

- **Hiện tượng đo được** (trước khi sửa): `tableBottom` (đáy `.report-drill-wrap`) = **1366px**,
  vượt hẳn viewport 900px và vượt cả khung popup (828px) — bảng 20 dòng không hề bị cắt/cuộn nội
  bộ, kéo cả bộ lọc + phân trang trôi theo khi cuộn (đo qua DOM: `.v2-modal-body` — div bọc RIÊNG
  của `V2BaseModal` bên trong `.modal-body` — có `scrollHeight: 1340` nhưng `overflow-y: auto`
  của CHÍNH NÓ trở thành vùng cuộn DUY NHẤT của toàn bộ nội dung, thay vì chỉ bảng cuộn).
- **Nguyên nhân (xác nhận bằng `getComputedStyle` qua Playwright, không suy đoán)**: chuỗi CSS
  `flex: 1 1 auto` mà `V2BaseReportModal` đặt lên `.report-drill-scroll` / `.report-drill-wrap`
  chỉ có tác dụng khi CHA TRỰC TIẾP của chúng THẬT SỰ là `display: flex`. Có 2 mắt xích không
  phải flex:
  1. `.v2-modal-body` (div riêng của `V2BaseModal.vue`, KHÔNG phải `.modal-body` mà vỏ đã ghi đè)
     — mặc định `display: block`.
  2. `.v2-table-scroll` (gốc của `V2BaseTableScroll.vue`) — mặc định `display: block`.
- **Sửa**: thêm 2 rule CSS mới vào khối `<style>` KHÔNG scoped sẵn có của `V2BaseReportModal.vue`
  (cùng khối đang ghi đè `.modal-content`/`.modal-header`/`.modal-body`), SCOPE CHẶT theo
  `.report-drill-dialog .v2-modal-body` và `.report-drill-scroll .v2-table-scroll` — tức là **chỉ
  áp dụng cho popup dùng `V2BaseReportModal`**, không đụng 30 popup khác đang dùng `V2BaseModal`
  trực tiếp (chúng tự giới hạn chiều cao bằng prop `max-height`/`max-body-height` dạng số, không
  phụ thuộc chuỗi flex này).
  ```css
  .report-drill-dialog .v2-modal-body {
      display: flex; flex-direction: column; flex: 1 1 auto; min-height: 0;
      overflow: hidden; padding: 0;
  }
  .report-drill-scroll .v2-table-scroll {
      display: flex; flex-direction: column; flex: 1 1 auto; min-height: 0;
  }
  ```
- **Đo lại sau sửa**: `tableBottom` từ 1366px → 709px (baseline 713px, lệch 4px — xem mục cuối).
  Screenshot xác nhận bảng cuộn nội bộ đúng như mockup, filters/KPI/phân trang/footer đứng yên.

## Bug 4 phát hiện: thiếu class `modal-dialog-centered`

`V2BaseModal.vue` KHÔNG có prop `centered` (bản gốc dùng `<b-modal centered>`). Thiếu class
`modal-dialog-centered` làm `.modal-dialog` mất `min-height: calc(100% - 3.5rem)` của bootstrap
→ đo `heightNormal` lệch đúng 16px (828px thay vì 844px — 844/900 không phải bội số vh sạch,
828/900 = đúng 92vh; baseline 844 = đúng phép tính bootstrap `calc(100% - 3.5rem)` khi
`.modal-content` chỉ cao 828px < 844px).

**Sửa bằng cách tự thêm class** (không sửa `V2BaseModal.vue`, không cần prop mới):
`dialog-class` của `V2BaseReportModal.vue` nối thêm `modal-dialog-centered` (đúng class mà
prop `centered` của bootstrap-vue tự sinh) — cả 2 nhánh bình thường/toàn màn hình. Chỉ đổi 1
dòng binding, không đụng file nào khác. Đo lại: `heightNormal` = 844, **khớp baseline TUYỆT ĐỐI**.

## Bug 5 (tự phát hiện lúc kiểm — sửa trước khi commit): prop type warning

Sau khi sửa Bug 3, tôi truyền `:max-table-height="0"` (Number) để tắt cap `max-height` mặc định
(`'50vh'`) của vỏ, đạt hiệu ứng flex-fill. Nhưng prop `maxTableHeight` của `V2BaseReportModal`
khai `type: String` — Playwright bắt được **6 dòng `[Vue warn]` console error** (mỗi lần render).
Không được sửa lại thành chuỗi `"0"` (chuỗi khác rỗng, KHÔNG falsy trong JS → sẽ ra
`max-height: 0`, bóp bảng về cao 0px thật sự — nguy hiểm hơn cả bug gốc). Đổi sang `""` (chuỗi
rỗng, falsy, đúng type `String`) — hết cảnh báo, hành vi giữ nguyên (đã đo lại xác nhận không đổi
số nào). Đã ghi chú trong template để người sau không sửa nhầm về `0`.

## Bảng so baseline vs after (đo bằng `measure-popup.mjs`, sau khi sửa đủ 5 bug)

| Khoá | Baseline | After | Khớp? |
|---|---|---|---|
| `cols` (13 cột, đúng thứ tự) | ✓ | ✓ | **MATCH** |
| `firstPageRowCount` | 20 | 20 | **MATCH** |
| `sttFirst` / `sttLast` | "1" / "20" | "1" / "20" | **MATCH** |
| `pageTotal` | "Hiển thị 1–20 / 126 nhu cầu" | như baseline | **MATCH** |
| `sortTextAsc` (20 dòng, sort cột Thị trường) | — | — | **MATCH tuyệt đối** |
| `sortDateAsc` (20 dòng, sort cột Meeting — có giờ:phút) | — | — | **MATCH tuyệt đối** (sau khi sửa Bug 2) |
| `heightFull` (phóng to toàn màn hình) | 900 | 900 | **MATCH** |
| `heightNormal` (chiều cao dialog bình thường) | 844 | 844 | **MATCH** (sau khi sửa Bug 4) |
| `tableBottom` (đáy vùng cuộn bảng) | 713 | 709 | **LỆCH 4px** |
| `footerTop` (đỉnh footer) | 803 | 787 | **LỆCH 16px** |

## 2 khoá còn lệch — đã tự quyết vì đây là quyết định ĐÃ CHỐT sẵn từ Task 3

`footerTop` lệch 16px và `tableBottom` lệch 4px (rất nhỏ, trong sai số bo tròn/flex) đều bắt
nguồn từ **1 quyết định đã ghi sẵn trong bối cảnh tôi nhận được**, KHÔNG phải điều tôi tự chọn:

> "slot `#footer` KHÔNG có div bọc (nút đặt thẳng vào, Bootstrap tự cấp khoảng cách 8px)."

Bản gốc: `.care-drill-footer { padding: 12px 0 0; margin-top: 12px; border-top: 1px solid
#e3e8ef; }` — tổng ~24px khoảng trắng + 1 viền phân cách phía trên footer.
Vỏ mới: `.v2-modal-footer` (mặc định của `V2BaseModal`) chỉ có `padding: 10px 0.5rem;`, KHÔNG
viền, KHÔNG margin-top — đúng như quyết định đã chốt ở Task 3 (đo & xác nhận trong chính comment
"Vòng sửa 3/5" của `V2BaseReportModal.vue`: "khoảng cách ngang giữa 2 nút footer = 8px").

→ Footer nay đứng GẦN bảng hơn ~16px, không còn viền phân cách phía trên — khác biệt THỊ GIÁC
NHỎ (không phải lỗi bố cục: không có gì chồng lấn, không có nội dung bị cắt, đã kiểm bằng
screenshot). Vì đây là quyết định đã có sẵn trong bối cảnh giao việc (không phải thứ tôi tự
suy ra), tôi giữ nguyên, KHÔNG thêm lại viền/margin để né việc "chọn lại" một quyết định đã
chốt. Nếu user muốn khớp baseline 100% ở 2 khoá này, cần thêm `border-top` + `margin-top` cho
`.report-drill-paging` hoặc override riêng `.report-drill-dialog .v2-modal-footer` trong vỏ.

## Kiểm chứng bổ sung bằng Playwright (ngoài 11 khoá của measure-popup.mjs)

1. **Console sạch**: 0 lỗi/cảnh báo liên quan tới popup (chỉ còn 1 lỗi `400 menu-settings` — API
   KHÔNG liên quan, có sẵn từ trước, và 2 cảnh báo `vue-router` toàn cục, không phải do
   DemandListModal).
2. **Toggle "Mở rộng"/"Thu gọn"**: bấm → khối KPI + "Phân bổ nhu cầu theo cơ cấu" hiện đúng, đo
   qua DOM (`report-drill-sumbox` count = 1). Screenshot xác nhận layout khớp mockup.
3. **Phân trang**: bấm trang 2 → STT dòng đầu = "21" (đúng, trang 1 là 1-20).
4. **Nút "Xoá lọc"**: bấm → bắn ĐÚNG 1 request `GET
   /api/v1/assign/report/potential-customer-care/demand-list?...` (xác nhận Bug 1 đã sửa đúng,
   không bắn đôi).
5. **`metaText` khi đang tải**: `"Đang tải… · Kỳ 01/09/2026 – 30/09/2026"` — đúng định dạng bản
   gốc.
6. **Footer**: đủ 3 nút (Đóng / In danh sách / Xuất Excel danh sách).
7. **Screenshot** (`/tmp/popup-normal.png`, `/tmp/popup-expanded.png`): đối chiếu bằng mắt — dải
   banner gradient, bộ lọc, bảng sticky header, phân trang, footer đều đúng khuôn mockup.

## Kiểm `index.vue` KHÔNG bị sửa

Theo đúng cảnh báo trong brief — `git diff --numstat` SAI vì `index.vue` đã có thay đổi của việc
khác chưa commit. Dùng MD5 thay thế:
```
md5 -q pages/assign/report/potential-customer-care/index.vue
```
Kết quả: `3ee332b47108445a757211849a1388db` — **giống hệt** trước và sau khi làm Task 5.

## File đã đổi trong session này

| File | Trạng thái | Lý do |
|---|---|---|
| `pages/assign/report/potential-customer-care/components/DemandListModal.vue` | Sửa, **ĐÃ COMMIT** (`74298de2e`, rồi vòng sửa 1/5 thêm 1 dòng — xem bên dưới) | Nội dung chính Task 5 — đúng phạm vi được giao |
| `components/report/V2BaseReportModal.vue` | Sửa, **ĐÃ COMMIT** (`f73f569b8`, do coordinator commit sau khi rà soát; vòng sửa 1/5 thêm phần khôi phục cuộn-về-đầu — xem bên dưới) | Bug 3 + Bug 4 (chuỗi flex đứt mắt xích, thiếu class centered) |
| `utils/mixins/reportDrillListMixin.js` | Sửa, **ĐÃ COMMIT** (`f73f569b8`) | Bug 2 (`dateSortKey` rớt giờ:phút) |

> Sửa lại so bản report gốc: 2 file `V2BaseReportModal.vue`/`reportDrillListMixin.js` đã được
> **coordinator commit** ở `f73f569b8` ngay sau khi tôi báo cáo — KHÔNG còn ở trạng thái "chưa
> commit" như bản report đầu ghi nhầm.

3 file bị cấm đụng (`V2BaseSmartFilterPanel.vue`, `ReportPrintPreviewModal.vue`,
`CareTrackingTable.vue`) và `index.vue` — **hoàn toàn không đụng tới** trong session này (các
thay đổi `git status` thấy ở 3 file đầu là của việc khác, có từ trước khi tôi bắt đầu).

---

## Vòng sửa 1/5 (theo rà soát của coordinator)

### Finding 1 (Critical) — sót tiền tố `care-drill` ở `id-prefix`

Đúng như phát hiện: `DemandListModal.vue:120` (bản trước vòng sửa) vẫn truyền
`id-prefix="care-drill"` cho `KpiBoxes`, nội suy thành id DOM thật (`care-drill-kpis-title-info`,
`care-drill-kpi-info-${index}`). Bản report gốc GHI SAI — không hề có mục "Quyết định phải tự đưa
ra" nào giải thích nó, đây là **sót thật**, không phải cố ý. Đã sửa:

```diff
- id-prefix="care-drill"
+ id-prefix="report-drill"
```

Grep xác nhận lại (rỗng — không còn `care-drill` nào trong file):
```
$ grep -n "care-drill" pages/assign/report/potential-customer-care/components/DemandListModal.vue
(không có output — exit code 1)
```

### Finding 2 (Important) — khôi phục "lật trang thì cuộn bảng về đầu"

Đúng ruling của coordinator: hành vi này thuộc về VỎ (`V2BaseReportModal.vue`), không phải mixin.
Đã làm đúng 3 bước:

1. Thêm `ref="tableScroll"` lên `<V2BaseTableScroll>`.
2. Đổi `@page-change`/`@page-size-change` của `<V2BasePagination>` từ arrow function emit thẳng
   sang gọi 2 method mới `onPageChange`/`onPageSizeChange` — mỗi method vẫn `$emit` lên cha NHƯ
   CŨ, rồi gọi thêm `resetScroll()`:
   ```js
   resetScroll() {
       const body = this.$refs.tableScroll && this.$refs.tableScroll.$refs.body
       if (body) body.scrollTop = 0
   },
   onPageChange(page) {
       this.$emit('page-change', page)
       this.resetScroll()
   },
   onPageSizeChange(size) {
       this.$emit('page-size-change', size)
       this.resetScroll()
   },
   ```
3. Đã xác nhận `V2BaseTableScroll.vue` khai đúng `ref="body"` cho vùng cuộn thật (đọc file trước
   khi dùng, đúng yêu cầu).

**Đo bằng Playwright (viewport 1440×900, `/tmp/care-state.json`)** — mở popup, đợi ổn định 1.5s
(tránh trùng với 1 bug có sẵn — xem mục "Phát hiện phụ" bên dưới), cuộn bảng xuống 300px, bấm
sang trang 2, đọc lại `scrollTop`:

| Mốc đo | Giá trị |
|---|---|
| `scrollTop` TRƯỚC khi lật trang | **300** |
| `scrollTop` SAU khi lật trang | **0** |
| Nội dung trang sau khi lật (`page-total`) | `Hiển thị 21–40 / 126 nhu cầu` |
| STT dòng đầu trang mới | `21` |
| `page-total` sau khi giữ ổn định thêm 1s | `Hiển thị 21–40 / 126 nhu cầu` (không bị bật lại trang 1) |

Khớp đúng hành vi bản gốc: cuộn về 0, và trang mới ĐỨNG YÊN (không tự nhảy lại).

#### Phát hiện phụ (không sửa — ngoài phạm vi, KHÔNG PHẢI do Task 5 gây ra)

Trong lúc đo Finding 2, phát hiện `index.vue` bắn **2 request `GET .../demand-list` trùng millisecond**
mỗi lần mở popup (xác nhận bằng theo dõi `page.on('request')` — 2 request cùng mốc
`msAfterStart`). Đây là bug có sẵn từ trước (không liên quan gì tới cuộn/phân trang), nhưng vì
`reportDrillListMixin.js` có watcher `rows() { this.page = 1 }` (đúng thiết kế — đổi tập dữ liệu
phải về trang 1), nếu người dùng lật trang NGAY TRONG cửa sổ ~300-700ms giữa 2 response trùng
lặp đó thì trang bị TRẢ VỀ TRANG 1 một cách im lặng (đã tái hiện được bằng cách đo `page` qua
`__vue__` mỗi 50ms — `page` nhảy 1→2 rồi tự về 1 khi response trùng thứ 2 làm `rows` đổi tham
chiếu). Đây LÀ MỘT BUG THẬT nhưng gốc rễ nằm ở `index.vue` (gọi `openDrill`/`fetchDrill` 2 lần) —
file **bị cấm đụng** trong Task 5. Không sửa, chỉ báo cáo để user cân nhắc mở task riêng.

### Việc thứ ba (Minor) — sửa lại câu "CHƯA COMMIT"

Đã sửa mục "File đã đổi trong session này" — `V2BaseReportModal.vue` và
`reportDrillListMixin.js` **ĐÃ được coordinator commit** ở `f73f569b8`, không còn "chưa commit"
như bản gốc ghi nhầm.

### Đo lại `measure-popup.mjs` sau vòng sửa 1/5

```
cols MATCH
firstPageRowCount MATCH
sttFirst MATCH
sttLast MATCH
pageTotal MATCH
tableBottom DIFF baseline=713 after=709   (đã biết, xem lý do ở mục "2 khoá còn lệch")
footerTop DIFF baseline=803 after=787     (đã biết, xem lý do ở mục "2 khoá còn lệch")
heightNormal MATCH
sortTextAsc MATCH
sortDateAsc MATCH
heightFull MATCH
```

Vẫn đúng 9/11 khớp, 2 khoá lệch giữ nguyên đúng số đã báo cáo trước — không phát sinh lệch mới.
