# Lượt sửa gộp cuối cùng — base-popup-bao-cao

Ngày: 2026-09-17

## Trạng thái: ĐÃ SỬA XONG, ĐÃ KIỂM, ĐÃ COMMIT

## Nội dung đã sửa

1. **(Critical) 2 request `demand-list` trùng khi đổi drill key** — `utils/mixins/reportDrillListMixin.js`
   tách `resetFilterState()` (dọn state im lặng, KHÔNG gọi hook) khỏi `resetFilters()` (dọn state +
   `onFilterChange()`, dùng cho nút "Xoá lọc"). `DemandListModal.vue` → `resetLocal()` (chạy khi mở
   popup mới / đổi `drillKey`) nay gọi `resetFilterState()` thay vì `resetFilters()`.
2. **(Important) Cột "Giá trị đầu tư dự kiến" mất căn phải/đậm/tabular-nums** — chuyển rule
   `.report-drill-table__money` từ `<style scoped>` sang khối `<style>` KHÔNG scoped mới thêm ở cuối
   `DemandListModal.vue` (kèm comment giải thích + đã rà toàn bộ `cellClass` khác trong `columns`,
   `report-drill-table__center` không dính lỗi vì đã nằm sẵn ở khối không-scoped của
   `V2BaseReportModal.vue`).
3. **(Important) Sort không kéo về trang 1** — `toggleSort()` trong mixin thêm `this.page = 1` kèm
   comment gốc.
4. **(Important) `resetScroll()` thò vào ref nội bộ** — thêm method công khai `scrollToTop()` vào
   `components/V2BaseTableScroll.vue` (chỉ thêm, không đổi gì sẵn có); `V2BaseReportModal.vue` đổi
   `resetScroll()` sang gọi `this.$refs.tableScroll.scrollToTop()`.
5. **(Minor) Spec e2e dùng gạch nối ASCII** — 4 dòng ở `e2e/tests/assign/potential-customer-care.spec.ts`
   (690, 1111, 1117, 1125) đổi `-` → `–` (en dash) khớp `V2BasePagination.vue`.
6. **(Minor) Comment trỏ lớp không còn tồn tại** — `CustomerMeetingHistoryModal.vue:261` và
   `ProjectListModal.vue:85,684` cập nhật ghi chú, chỉ sửa comment không đụng code.

## Kết quả 3 phép đo bắt buộc

1. **Đếm request `demand-list`** (hook `fetch` + `XMLHttpRequest.prototype.open`):
   - Mở popup theo đường đổi drill key (đóng popup "Dịch vụ ô tô" rồi bấm số ở "Công nghiệp" — key
     đổi từ `field:7` sang `field:2`): **1 request** (`drill=field:2`). Trước sửa: 2.
   - Bấm "Xoá lọc" trong popup: **1 request** (`drill=field:2`, giữ nguyên tính năng).
2. **Căn lề ô tiền** — `getComputedStyle(document.querySelector('td.report-drill-table__money'))`:
   `textAlign: "right"`, `fontWeight: "700"`, `fontVariantNumeric: "tabular-nums"`.
3. **Sort kéo về trang 1** — popup "Dịch vụ ô tô" (126 dòng, 4 trang): lật tới trang 3
   (`Hiển thị 41–60 / 126 nhu cầu`), bấm tiêu đề cột "Meeting thu thập nhu cầu" → `.page-total` về
   `Hiển thị 1–20 / 126 nhu cầu`.
   - Phụ: xác nhận `scrollToTop()` hoạt động — kéo `.report-drill-wrap` xuống `scrollTop=200`, bấm
     sang trang kế → `scrollTop` về `0`.

## So baseline (`measure-popup.mjs` → `/tmp/after-fix.json`, KHÔNG sửa script/baseline)

9/11 khoá khớp baseline. Đúng 2 khoá lệch đã biết, không phát sinh khoá lệch thứ ba:
- `tableBottom`: 713 → 709
- `footerTop`: 803 → 787

(Script đã có thêm 4 khoá đo mới — `tableScrollBorderTopWidth`, `tableScrollBorderRadius`,
`modalContentOverflow`, `footerButtonGaps` — do agent khác đang cập nhật `measure-popup.mjs` song
song; các khoá này KHÔNG có trong `baseline.json` 11-khoá nên không tính vào so sánh trên, đúng phạm
vi brief yêu cầu.)

## Mối lo / ghi chú

- Không phát hiện lỗi console mới liên quan tới các file đã sửa (chỉ còn các warning/lỗi có sẵn từ
  trước ở module `training` và endpoint `menu-settings` không liên quan).
- `.report-drill-table__money` nay là CSS toàn cục (không scoped) — cùng cơ chế với
  `.report-drill-table__center` đã có sẵn ở vỏ, rủi ro trùng tên với màn khác coi như tương đương.

---

## Vòng sửa tiếp — Finding 1 còn sót nhánh `keepView`

Ngày: 2026-09-17 (nối thêm)

**Phát hiện của người rà soát:** lượt sửa trước chỉ vá nhánh `resetLocal()` của watcher `drillKey`
(`DemandListModal.vue`). Nhánh `keepView` (bật ở `onKpiDrill()` — bấm số trong khối KPI — và
`goBack()` — nút "Quay lại") vẫn gọi `this.resetFilters()` (bản CÓ hook `onFilterChange()`), trong
khi màn cha `index.vue` đã tự `fetchDrill()` cho đúng `drillKey` đó rồi (do `@drill="openDrill"`) →
vẫn bắn 2 request `demand-list` trùng nhau trên đường này. Phép đo lượt trước chỉ đi đường KHÔNG
`keepView` (đóng popup rồi bấm số chỉ tiêu khác) nên chưa từng bắt được.

**Đã sửa:** `DemandListModal.vue`, watcher `drillKey()` — nhánh `keepView` đổi `this.resetFilters()`
→ `this.resetFilterState()` (bản im lặng, không gọi hook). Bổ sung comment ở đầu watcher nêu rõ: CẢ
2 NHÁNH đều chỉ được dọn state im lặng, không bao giờ gọi bản có hook, vì mọi đường đổi `drillKey`
đều đã đi kèm 1 lần `fetchDrill()` của cha.

**Rà toàn file:** `grep -n "resetFilters\b"` trên `DemandListModal.vue` + `reportDrillListMixin.js`
— chỉ còn đúng 1 nơi gọi bản có hook: nút "Xoá lọc" (`<V2BaseIconButton title="Xoá lọc"
@click="resetFilters">`, dòng 76). Mọi chỗ khác chỉ còn là comment giải thích, không phải lệnh gọi.

### Kiểm chứng — đúng 2 đường vừa nêu + nhắc lại đường cũ

Hook `fetch` + `XMLHttpRequest.prototype.open` đếm request `demand-list`, phiên
`/tmp/care-state.json`, viewport 1440×900:

1. Mở popup "Dịch vụ ô tô" (126 nhu cầu) → mở khối tổng hợp ("Mở rộng") → bấm số trong hộp KPI đầu
   tiên (đường `onKpiDrill`, có `keepView`) → **1 request** (`drill=field:7%40won`).
2. Ngay sau đó bấm "Quay lại" (đường `goBack`, cũng có `keepView`) → **1 request**
   (`drill=field:7`, trở về key ban đầu).
3. Đường cũ, nhắc lại cho chắc không vỡ: đóng popup, bấm số ở "Công nghiệp" (chỉ tiêu khác, đường
   `resetLocal`, KHÔNG `keepView`) → **1 request** (`drill=field:2`).
4. Bấm "Xoá lọc" ngay sau đó → **1 request** (`drill=field:2`, giữ nguyên tính năng tải lại theo bộ
   lọc rỗng).

Cả 4 con số đều đúng **1**. Không có lỗi console mới phát sinh so với lượt kiểm trước (cùng tập
warning có sẵn ở module `training` / endpoint `menu-settings`, không liên quan).
