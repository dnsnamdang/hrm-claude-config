# Review package: 01a6fbb28..48c757916

## Commits
48c757916 chore(report-popup): dọn nhất quán cuối 3 popup báo cáo dùng chung vỏ

## Files changed
 components/report/V2BaseReportModal.vue            |  33 ++++++
 .../components/DevelopmentDrillModal.vue           |  47 ++++-----
 .../components/DemandListModal.vue                 |  44 +++-----
 .../components/ProjectListModal.vue                | 116 ++++++++++++++++-----
 utils/mixins/reportDrillListMixin.js               |  32 +++---
 5 files changed, 178 insertions(+), 94 deletions(-)

## Diff
diff --git a/components/report/V2BaseReportModal.vue b/components/report/V2BaseReportModal.vue
index b6a55f27f..f7b55edea 100644
--- a/components/report/V2BaseReportModal.vue
+++ b/components/report/V2BaseReportModal.vue
@@ -9,20 +9,32 @@
     `_BV_modal_outer_` z-index 1041 — xem `components/print/ReportPrintPreviewModal.vue`).
 
     Component này KHÔNG biết nghiệp vụ, KHÔNG biết lấy dữ liệu, KHÔNG tự lọc/sắp/phân trang.
     Máy client-side nằm ở `utils/mixins/reportDrillListMixin.js`.
 
     ⚠️ Phát hiện ở Task 5 — `V2BaseModal` KHÔNG có prop `centered` (b-modal gốc của mẫu nguồn có
     `centered`). Tự thêm class `modal-dialog-centered` vào `dialog-class` bên dưới (đúng class mà
     prop `centered` của bootstrap-vue sinh ra) để dialog được CĂN GIỮA theo chiều dọc như bản gốc —
     thiếu nó, `.modal-dialog` mất `min-height: calc(100% - 3.5rem)` của bootstrap, đo lệch 16px
     chiều cao dialog so với baseline (844px -> 828px).
+
+    ⚠️ QUY TẮC `cellClass` (chốt ở vòng dọn nhất quán cuối) — cột `<td>` do CHÍNH VỎ NÀY render
+    (lặp `columns` trong template của nó, xem `v-for="col in columns"` bên dưới), KHÔNG phải slot
+    content của popup. Vì vậy `data-v-xxx` của `<style scoped>` ở FILE POPUP không bao giờ với tới
+    `<td>` đó: mọi `cellClass` popup tự đặt qua mảng `columns` BẮT BUỘC khai KHÔNG scoped ở đúng
+    file popup đó (để trong khối scoped thì style lặng lẽ không áp dụng — không có lỗi nào báo ra).
+    NHƯNG nếu **≥ 2 popup dùng CHUNG một class y hệt** (cùng tên, cùng thuộc tính) thì đưa THẲNG vào
+    khối `<style scoped>` của VỎ NÀY — class đó do chính vỏ render nên style scoped của vỏ áp dụng
+    bình thường, khỏi phải chép lại ở từng popup. 2 ví dụ đã áp dụng: `.report-drill-table__center`
+    (có từ đầu) và `.report-drill-table__money` (dọn vào đây ở vòng cleanup cuối — trước đó bị chép
+    y hệt kèm cả đoạn comment giải thích ở cả 3 popup, xem lịch sử `DemandListModal.vue` /
+    `DevelopmentDrillModal.vue` / `ProjectListModal.vue`).
 -->
 <template>
     <V2BaseModal
         :modal-id="modalId"
         size="xl"
         :dialog-class="fullscreen ? `${dialogClass} report-drill-dialog--full modal-dialog-centered` : `${dialogClass} modal-dialog-centered`"
         max-body-height="none"
         no-enforce-focus
         @hidden="$emit('close')"
     >
@@ -116,20 +128,31 @@ import V2BasePagination from '@/components/V2BasePagination.vue'
 export default {
     name: 'V2BaseReportModal',
     components: { V2BaseModal, V2BaseTableScroll, V2BasePagination },
     props: {
         visible: { type: Boolean, default: false },
         modalId: { type: String, required: true },
         lead: { type: String, default: '' },
         title: { type: String, default: '' },
         meta: { type: String, default: '' },
         loading: { type: Boolean, default: false },
+        /**
+         * Khoá VỎ NÀY tự đọc khi vẽ `<th>`/`<td>`: `key` (định danh cột — cũng là tên slot
+         * `#cell-<key>`), `field` (đọc `row[field]` khi popup KHÔNG khai slot riêng cho cột đó),
+         * `label` (chữ tiêu đề cột), `width` (chuỗi CSS, gắn `min-width` cho `<th>`), `sortable`
+         * (có vẽ nút sắp xếp bấm được không), `cellClass` (class gắn thẳng vào `<td>` — xem quy tắc
+         * cellClass ở đầu file).
+         * Khoá CHỈ `utils/mixins/reportDrillListMixin.js` đọc, vỏ KHÔNG đụng tới: `sortType`
+         * ('date' để `dateSortKey()` sắp đúng kiểu ngày thay vì so chuỗi), `sortFields` (mảng field
+         * ghép lại khi 1 cột hiển thị gộp nhiều field, vd "Thị trường / Phường xã" sắp theo cả
+         * `province_name` + `ward_name`).
+         */
         columns: { type: Array, default: () => [] },
         /** Dòng của TRANG ĐANG XEM — vỏ không cắt trang, mixin/BE lo việc đó */
         rows: { type: Array, default: () => [] },
         rowKey: { type: String, default: 'id' },
         startIndex: { type: Number, default: 0 },
         emptyText: { type: String, default: 'Không có dữ liệu khớp bộ lọc.' },
         sort: { type: Object, default: () => ({ key: '', dir: 'asc' }) },
         currentPage: { type: Number, default: 1 },
         currentPageSize: { type: Number, default: 20 },
         totalRows: { type: Number, default: 0 },
@@ -415,20 +438,30 @@ $text-muted: #6b7280;
         white-space: nowrap;
     }
 
     tbody tr:hover td {
         background: #ddf0f7;
     }
 }
 .report-drill-table__center {
     text-align: center;
 }
+/* Dọn ở vòng cleanup cuối: class NGHIỆP VỤ dùng chung của CẢ 3 popup (cột tiền) — trước đây bị chép
+   y hệt (kèm nguyên đoạn comment giải thích "vì sao phải để không-scoped") ở cuối từng file popup.
+   `<td>` mang class này do CHÍNH VỎ NÀY render nên đưa thẳng vào khối scoped ở đây là đủ — không
+   cần khối `<style>` không-scoped riêng như hồi còn nằm ở file popup (xem quy tắc cellClass đầu
+   file). Giá trị GIỮ NGUYÊN, không đổi số. */
+.report-drill-table__money {
+    text-align: right;
+    font-weight: 700;
+    font-variant-numeric: tabular-nums;
+}
 .report-drill-table__empty {
     padding: 22px;
     text-align: center;
     color: $text-muted;
 }
 
 /* Tiêu đề cột bấm được để sắp xếp — copy khuôn `.sortable-header` của V2BaseDataTable */
 .report-drill-sort {
     display: inline-flex;
     align-items: center;
diff --git a/pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue b/pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue
index a2f30251d..f3737f990 100644
--- a/pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue
+++ b/pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue
@@ -15,46 +15,57 @@
     2 luật bỏ cột dùng chung cho cả 3 biến thể:
       · cấp đã bị node CỐ ĐỊNH thì bỏ luôn cột đó (mọi dòng mang đúng 1 giá trị, cột chỉ lặp lại
         điều tiêu đề popup đã nói);
       · bỏ cột Bộ phận khi KHÔNG dòng nào thuộc bộ phận.
     Hệ quả: popup mở theo Khách hàng mất cột Khách hàng -> chip "KH mới" NHẢY SANG cột Tên meeting.
 
     Dựng TRÊN `components/report/V2BaseReportModal.vue` (vỏ dùng chung cho popup báo cáo) +
     `utils/mixins/reportDrillListMixin.js` (máy sắp xếp + phân trang tại chỗ) — cùng khuôn với
     `pages/assign/report/potential-customer-care/components/DemandListModal.vue` (popup gốc). Khác
     biệt DUY NHẤT với popup gốc: popup này lọc CLIENT-SIDE trên mảng `rows` đã tải sẵn (không gọi lại
-    API). `applyLocalFilters()` của mixin không hợp ở đây — nó so `row[param]` thẳng, còn ô lọc khai
-    theo id khác tên field thật (`market` ứng với `province_id`…) — nên GIỮ hàm lọc riêng
-    `filteredRows`, chỉ đổi tên state `ownFilters` -> `filters` để dùng chung
+    API). Mixin KHÔNG có hàm lọc chung (mỗi popup tự quyết cách lọc) — popup này tự viết hàm lọc
+    riêng `filteredRows` vì ô lọc khai theo id khác tên field thật (`market` ứng với `province_id`…),
+    chỉ đổi tên state `ownFilters` -> `filters` để dùng chung
     `resetFilters()`/`resetFilterState()`/`hasActiveFilter` của mixin.
 
     Khung popup, dải banner đầu, bảng + thanh cuộn, phân trang, nút phóng to, cuộn-về-đầu khi lật
     trang đều do vỏ lo — component này chỉ còn giữ phần NGHIỆP VỤ RIÊNG: bộ lọc, khối KPI/phân bổ,
     thứ tự + nội dung cột, và các ô bảng cần hiển thị đặc biệt.
+
+    `max-table-height=""` (bổ sung ở vòng cleanup cuối — đo thật thấy LỆCH so với popup gốc): mặc
+    định của vỏ là `'50vh'` (cap cứng). Trước khi sửa, thu gọn khối tổng hợp rồi đo: vùng cuộn bảng
+    (`.report-drill-wrap`) bị kẹp cứng ở 450px (đúng 50vh của viewport 900px) trong khi
+    `.report-drill-scroll` (khối cha, được phép cao tới) đo được 527–529px — để hở **143–145px
+    khoảng trắng** giữa đáy bảng và footer, mất chỗ vô ích. Popup gốc (`DemandListModal.vue`) đã
+    dùng `max-table-height=""` để bảng flex-fill đúng phần còn lại, không kẹp cứng — áp lại đúng
+    prop đó ở đây cho khớp hành vi. `""` là falsy nên `V2BaseTableScroll` không gắn `max-height`
+    inline — TUYỆT ĐỐI đừng đổi thành số `0` (prop khai `type: String`, số báo lỗi type) hay chuỗi
+    `"0"` (khác rỗng nên KHÔNG falsy, ra `max-height: 0` làm bảng cao bằng 0).
 -->
 <template>
     <V2BaseReportModal
         modal-id="cmd-drill-modal"
         :visible="visible"
         :loading="loading"
         lead="Bạn đang xem phát triển thị trường:"
         :title="drillTitle"
         :meta="metaText"
         :columns="baseColumns"
         :rows="pagedRows"
         :start-index="pageOffset"
         :sort="sort"
         :current-page="safePage"
         :current-page-size="pageSize"
         :total-rows="filteredRows.length"
         :item-label="unit"
         :empty-text="`Không có ${unit} nào khớp bộ lọc.`"
+        max-table-height=""
         @sort="({ key }) => toggleSort(key)"
         @page-change="onPageChange"
         @page-size-change="onPageSizeChange"
         @close="$emit('close')"
     >
         <!--
             Bộ lọc riêng của popup (luật 1 trong design.md):
               · đang xem theo đối tượng A thì BỎ ô lọc theo A (mọi chiều nằm trên `path` của node);
               · cố định Khách hàng thì ẩn luôn ô Thị trường (1 KH chỉ thuộc 1 thị trường);
               · popup "KH mới" không liệt kê meeting nên bỏ 2 ô Loại meeting / Trạng thái.
@@ -248,23 +259,24 @@ const STATUS_CANCELLED = 4
 
 const DIM_LABEL = {
     market: 'Thị trường',
     customer: 'Khách hàng',
     dept: 'Phòng ban',
     part: 'Bộ phận',
     host: 'Nhân viên',
 }
 
 /**
- * `cellClass` cũ (`cmd-*`) -> lớp mới: `report-drill-table__center` đã có sẵn trong `V2BaseReportModal`
- * (khối KHÔNG scoped của vỏ) nên dùng thẳng, không định nghĩa lại; `report-drill-table__money` là
- * lớp NGHIỆP VỤ riêng của popup này, định nghĩa KHÔNG scoped ở cuối file — xem comment ở đó.
+ * `cellClass` cũ (`cmd-*`) -> lớp mới: cả `report-drill-table__center` lẫn `report-drill-table__money`
+ * đều đã có sẵn trong khối `<style scoped>` của `components/report/V2BaseReportModal.vue` (dọn về
+ * đó ở vòng cleanup cuối — dùng CHUNG cho cả 3 popup báo cáo), dùng thẳng, KHÔNG định nghĩa lại ở
+ * file này (xem quy tắc cellClass ở đầu file vỏ).
  */
 const CELL_CLASS_MAP = { 'cmd-center': 'report-drill-table__center', 'cmd-money': 'report-drill-table__money' }
 
 /**
  * 4 cột hiển thị NGUYÊN VĂN field của row, không định dạng/giá trị mặc định gì (`cellText()` trả về
  * đúng field này) -> để vỏ tự render qua `row[col.field]`, khỏi cần slot riêng. Cột nào cần định
  * dạng (ngày, tiền) hoặc giá trị mặc định (`—`) vẫn đi qua slot `#cell-<id>` gọi `cellText()`.
  */
 const FIELD_MAP = { market: 'province_name', dept: 'department_name', host: 'host_name', status: 'status_name' }
 
@@ -436,24 +448,24 @@ export default {
                     const chips = Array.from(counts.values())
                         .sort((a, b) => b.count - a.count)
                         .slice(0, 12)
                         .map((chip) => ({ ...chip, percent: Math.round((chip.count * 100) / rows.length) }))
 
                     return { dim: dim.dim, label: dim.label, chips }
                 })
                 .filter((group) => group.chips.length)
         },
         /**
-         * Lọc CLIENT-SIDE trên tập THÔ (`rows`, chưa sắp). `applyLocalFilters()` của mixin không hợp
-         * ở đây — nó so `row[param]` trực tiếp, còn ô lọc khai theo id khác tên field thật (`market`
-         * ứng với `province_id`…) — giữ nguyên hàm lọc riêng, chỉ đổi `ownFilters` -> `filters`
-         * (mixin) để dùng chung `resetFilters()`/`resetFilterState()`/`hasActiveFilter`.
+         * Lọc CLIENT-SIDE trên tập THÔ (`rows`, chưa sắp). Mixin không có hàm lọc chung — popup này
+         * tự viết hàm lọc riêng vì ô lọc khai theo id khác tên field thật (`market` ứng với
+         * `province_id`…), chỉ đổi `ownFilters` -> `filters` (mixin) để dùng chung
+         * `resetFilters()`/`resetFilterState()`/`hasActiveFilter`.
          */
         filteredRows() {
             const keyword = this.keyword.trim().toLowerCase()
 
             return this.rows.filter((row) => {
                 for (const field of FILTER_FIELDS) {
                     const picked = this.filters[field.id]
                     if (picked != null && String(field.valueOf(row)) !== String(picked)) return false
                 }
 
@@ -1029,25 +1041,10 @@ $text-muted: #6b7280;
     align-items: center;
     padding: 1px 7px 2px;
     border-radius: 999px;
     border: 1px solid rgba(34, 197, 94, 0.45);
     background: rgba(34, 197, 94, 0.1);
     color: #15803d;
     font-size: 10.5px;
     font-weight: 700;
 }
 </style>
-
-<!-- KHÔNG scoped: cột "Giá trị dự kiến (đ)" (`report-drill-table__money`, map từ `cmd-money` cũ qua
-     `CELL_CLASS_MAP`) được VỎ `V2BaseReportModal` render — nó lặp `columns` rồi gắn
-     `:class="col.cellClass"` vào `<td>` bằng TEMPLATE CỦA CHÍNH NÓ, xem
-     `components/report/V2BaseReportModal.vue`. Để rule này trong khối scoped ở trên thì nó lặng lẽ
-     KHÔNG áp dụng (`<td>` mang `data-v-xxx` của VỎ, không phải của file này). Cùng tên + cùng nội
-     dung với `.report-drill-table__money` của `DemandListModal.vue` (popup gốc) — trùng tên CSS
-     global 2 file không xung đột vì thuộc tính giống hệt nhau. -->
-<style>
-.report-drill-table__money {
-    text-align: right;
-    font-weight: 700;
-    font-variant-numeric: tabular-nums;
-}
-</style>
diff --git a/pages/assign/report/potential-customer-care/components/DemandListModal.vue b/pages/assign/report/potential-customer-care/components/DemandListModal.vue
index 4975ac83b..8c7f3a16a 100644
--- a/pages/assign/report/potential-customer-care/components/DemandListModal.vue
+++ b/pages/assign/report/potential-customer-care/components/DemandListModal.vue
@@ -64,22 +64,24 @@
                         v-model="filters[field.param]"
                         :options="field.options"
                         :allowClear="true"
                         size="sm"
                         :placeholder="field.placeholder"
                         @change="onSelectChange(field.param)"
                     />
                 </div>
 
                 <!-- Xoá lọc nằm NGAY SAU ô lọc cuối, không tách thành dòng riêng: hàng lọc gói sang
-                     dòng 2 vốn còn thừa chỗ, để nút một mình một dòng là phí hẳn một dòng của popup. -->
-                <div class="report-drill-filters__item report-drill-filters__item--action">
+                     dòng 2 vốn còn thừa chỗ, để nút một mình một dòng là phí hẳn một dòng của popup.
+                     Gate bằng `hasActiveFilter` (mixin): chưa lọc gì thì ẩn hẳn nút — bấm lúc rỗng
+                     chỉ tổ bắn thêm 1 request `demand-list` thừa (vi phạm rule hiệu năng CLAUDE.md). -->
+                <div v-if="hasActiveFilter" class="report-drill-filters__item report-drill-filters__item--action">
                     <V2BaseIconButton title="Xoá lọc" @click="resetFilters">
                         <i class="ri-refresh-line"></i>
                     </V2BaseIconButton>
                 </div>
 
                 <div class="report-drill-filters__meta">
                     <!-- Thu gọn khối tổng hợp (KPI + phân bổ) — cùng kiểu nút với dải tổng hợp ngoài
                          màn báo cáo, để popup nhường chỗ cho bảng chi tiết khi màn hình thấp. -->
                     <button
                         v-if="hasSummary"
@@ -211,31 +213,37 @@
             >
                 <template #prefix><i class="ri-add-line" style="font-size: 13px"></i></template>
                 Tạo mới
             </V2BaseButton>
             <span v-else>—</span>
         </template>
         <template #cell-amount="{ row }">{{ money(row.expected_amount) }}</template>
         <template #cell-start="{ row }">{{ monthYear(row.expected_start_date) }}</template>
         <template #cell-repair="{ row }">{{ row.has_maintenance_demand ? 'Có' : 'Không' }}</template>
 
+        <!-- Thứ tự + màu theo `.claude/skills/button-convention/SKILL.md` mục 2b + mục 5 (modal
+             footer: action phụ trước, Đóng luôn cuối) — khớp `DevelopmentDrillModal.vue` /
+             `ProjectListModal.vue`. Popup KHÔNG tự gọi API: bộ lọc gốc của báo cáo nằm ở màn cha,
+             cha ghép rồi tải. -->
         <template #footer>
-            <V2BaseButton tertiary size="sm" @click="$emit('close')">Đóng</V2BaseButton>
-            <!-- Popup KHÔNG tự gọi API: bộ lọc gốc của báo cáo nằm ở màn cha, cha ghép rồi tải -->
             <V2BaseButton secondary size="sm" @click="$emit('print')">
                 <template #prefix><i class="ri-printer-line" style="font-size: 14px"></i></template>
                 In danh sách
             </V2BaseButton>
-            <V2BaseButton primary size="sm" @click="$emit('export')">
-                <template #prefix><i class="ri-download-line" style="font-size: 14px"></i></template>
+            <V2BaseButton secondary status="success" size="sm" @click="$emit('export')">
+                <template #prefix><i class="ri-file-excel-2-line" style="font-size: 14px"></i></template>
                 Xuất Excel danh sách
             </V2BaseButton>
+            <V2BaseButton tertiary size="sm" @click="$emit('close')">
+                <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
+                Đóng
+            </V2BaseButton>
         </template>
     </V2BaseReportModal>
 </template>
 
 <script>
 import V2BaseReportModal from '@/components/report/V2BaseReportModal.vue'
 import V2BaseInput from '@/components/V2BaseInput.vue'
 import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
 import V2BaseButton from '@/components/V2BaseButton.vue'
 import V2BaseIconButton from '@/components/V2BaseIconButton.vue'
@@ -812,21 +820,23 @@ $text-muted: #6b7280;
     align-items: center;
     gap: 10px;
     margin-bottom: 8px;
 }
 .report-drill-back__from {
     font-size: 11.5px;
     color: $text-muted;
 }
 
 /* ---- Các ô bảng đặc biệt (chưa có ở vỏ dùng chung) ---- */
-/* `.report-drill-table__money` chuyển sang khối KHÔNG scoped phía dưới — xem comment ở đó. */
+/* `.report-drill-table__money` (cột "Giá trị đầu tư dự kiến") dọn về khối scoped của
+   `components/report/V2BaseReportModal.vue` ở vòng cleanup cuối — dùng CHUNG với 2 popup báo cáo
+   kia, không định nghĩa riêng ở đây nữa (xem quy tắc cellClass ở đầu file vỏ). */
 .report-drill-sub {
     color: $text-muted;
     font-size: 11px;
 }
 /* Tên KH + nút mở lịch sử meeting.
    Nút hiện RÕ THƯỜNG TRỰC, KHÔNG làm mờ rồi chỉ sáng lên khi rê chuột: đây là lối vào duy nhất
    của tính năng lịch sử meeting, để mờ thì phải dò mới thấy — và trên thiết bị cảm ứng không có
    trạng thái hover để mà sáng lên. */
 .report-drill-customer {
     display: inline-flex;
@@ -852,30 +862,10 @@ $text-muted: #6b7280;
     padding: 0 5px;
     border: 1px solid #fcd34d;
     border-radius: 3px;
     background: #fffbeb;
     color: #b45309;
     font-size: 10px;
     font-weight: 700;
     line-height: 15px;
 }
 </style>
-
-<!-- KHÔNG scoped: `td.report-drill-table__money` (cột "Giá trị đầu tư dự kiến") được VỎ
-     `V2BaseReportModal` render (nó lặp `columns` rồi gắn `:class="col.cellClass"` vào `<td>` bằng
-     TEMPLATE CỦA CHÍNH NÓ, xem `components/report/V2BaseReportModal.vue`) — attribute `data-v-xxx`
-     của style scoped chỉ đóng lên phần tử do TEMPLATE của `DemandListModal.vue` render, không với
-     tới `<td>` đó. Để rule này trong khối scoped ở trên thì nó lặng lẽ KHÔNG áp dụng: không báo
-     lỗi, chỉ đơn giản là `<td>` mang đúng class mà không nhận style (đo thật: textAlign "left",
-     fontWeight 400 thay vì "right" / 700). Rà lại TOÀN BỘ `cellClass` khai trong mảng `columns` của
-     file này: `report-drill-table__center` (start/repair/status) đã có sẵn trong khối KHÔNG scoped
-     của chính `V2BaseReportModal.vue` (thuộc về vỏ) nên không dính lỗi này — chỉ
-     `report-drill-table__money` là class NGHIỆP VỤ riêng của popup này bị lọt lưới. ⚠️ KHÔNG chuyển
-     nó vào `V2BaseReportModal.vue` — đó là class nghiệp vụ của popup CSKH, không phải của vỏ dùng
-     chung. -->
-<style>
-.report-drill-table__money {
-    text-align: right;
-    font-weight: 700;
-    font-variant-numeric: tabular-nums;
-}
-</style>
diff --git a/pages/assign/report/prospective-project-results/components/ProjectListModal.vue b/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
index 1cefb9b6a..50fb6d7a2 100644
--- a/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
+++ b/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
@@ -34,39 +34,50 @@
 
     ⚠️ TỰ QUYẾT — khối KPI (`nodeMetrics` bên dưới) dựng lại từ CHÍNH `metrics` của node vừa bấm —
     cùng số liệu với ô đã bấm trên bảng theo dõi/dải tổng hợp (`metricsOf()` ở BE), do `index.vue`
     tự dò trong `tree`/`total` (đã có sẵn trong bộ nhớ, KHÔNG gọi thêm API) rồi truyền qua
     `payload.nodeMetrics` khi gọi `open()`.
 
     Chip phân bổ (Task 14b) LẤY TỪ khoá `allocation` do `project-list` trả kèm — tính trên tập ĐÃ
     áp `drill_key` + bộ lọc `metric` (ĐÚNG tập popup đang liệt kê), CHỈ trước phân trang (xem
     `allocationOf()`/`projectList()` ở BE). Ẩn theo CHÍNH `fieldVisibility` bên dưới (computed
     `allocationGroups`) — không viết luật ẩn thứ hai.
+
+    `max-table-height=""` (bổ sung ở vòng cleanup cuối — đo thật thấy LỆCH so với popup gốc): mặc
+    định của vỏ là `'50vh'` (cap cứng). Trước khi sửa, thu gọn khối tổng hợp rồi đo: vùng cuộn bảng
+    (`.report-drill-wrap`) bị kẹp cứng ở 450px (đúng 50vh của viewport 900px) trong khi
+    `.report-drill-scroll` (khối cha, được phép cao tới) đo được 529px — để hở **145px khoảng
+    trắng** giữa đáy bảng và footer, mất chỗ vô ích. Popup gốc (`DemandListModal.vue`) đã dùng
+    `max-table-height=""` để bảng flex-fill đúng phần còn lại, không kẹp cứng — áp lại đúng prop đó
+    ở đây cho khớp hành vi. `""` là falsy nên `V2BaseTableScroll` không gắn `max-height` inline —
+    TUYỆT ĐỐI đừng đổi thành số `0` (prop khai `type: String`, số báo lỗi type) hay chuỗi `"0"`
+    (khác rỗng nên KHÔNG falsy, ra `max-height: 0` làm bảng cao bằng 0).
 -->
 <template>
     <V2BaseReportModal
         modal-id="tkt-project-list-modal"
         :visible="visible"
         :loading="loading"
         lead="Bạn đang xem:"
         :title="modalTitle"
         :meta="ancestorText"
         :columns="columnDefs"
         :rows="rows"
         :start-index="startIndex"
         :sort="modalSort"
         :current-page="page"
         :current-page-size="perPage"
         :total-rows="total"
         item-label="dự án"
         :page-size-options="[20, 50, 100]"
         empty-text="Không có dự án nào khớp bộ lọc."
+        max-table-height=""
         @sort="onSort"
         @page-change="onPageChange"
         @page-size-change="onPageSizeChange"
         @close="close"
     >
         <template #filters>
             <div class="report-drill-filters">
                 <div v-for="field in visibleFields" :key="field.key" class="report-drill-filters__item">
                     <V2BaseSelectRemote
                         v-if="field.remote"
@@ -82,20 +93,29 @@
                     <V2BaseSelectInModal
                         v-else
                         v-model="ownFilters[field.key]"
                         :options="fieldOptions(field)"
                         :allow-clear="true"
                         size="sm"
                         :placeholder="field.placeholder"
                         @change="onFilterChange"
                     />
                 </div>
+
+                <!-- Xoá lọc — gate bằng `hasActiveFilter`: chưa lọc gì thì ẩn hẳn, không hiện rồi
+                     disable (đúng khuôn P1/P2 + button-convention). Bấm xoá hết `ownFilters` rồi gọi
+                     lại `fetchList()` đúng 1 lần qua `onFilterChange()`. -->
+                <V2BaseButton v-if="hasActiveFilter" tertiary size="xs" @click="resetOwnFilters">
+                    <template #prefix><i class="ri-refresh-line" style="font-size: 13px"></i></template>
+                    Xoá lọc
+                </V2BaseButton>
+
                 <span class="report-drill-count">{{ loading ? 'Đang tải…' : `${total} dự án` }}</span>
             </div>
         </template>
 
         <!--
             Khối tổng hợp (nút thu gọn + KPI + chip phân bổ) — chuyển từ vị trí ĐẦU popup (bản dựng
             tay trên V2BaseModal) sang slot `#summary` của vỏ, đứng SAU `#filters` (thứ tự do vỏ quy
             định, xem ghi chú đầu file). `hidden` (không phải style.display / v-show) — bẫy đã nhắc:
             v-show render ra `style="display:none"` là chuẩn CSS, hoàn toàn hợp lệ, nhưng popup này
             chốt riêng phải dùng thuộc tính `hidden` để không có logic ẩn nào khác đè lên bằng inline
@@ -126,35 +146,42 @@
                     <div class="report-drill-sum__item report-drill-sum__item--bad">
                         <span>Thất bại</span><strong>{{ money(nodeMetrics.lost) }}</strong>
                     </div>
                     <div class="report-drill-sum__item">
                         <span>Tỷ lệ thành công</span><strong>{{ rateText(nodeMetrics.success_rate) }}</strong>
                     </div>
                 </div>
 
                 <!-- Chip phân bổ (Task 14b) — dải chip cuộn ngang trong 1 khối chung (khuôn CSKH
                      `DemandListModal.vue` `.report-drill-sum` — tên CŨ `.care-drill-sum`) khi nhiều
-                     mục, KHÔNG phải chip bị cắt. -->
+                     mục, KHÔNG phải chip bị cắt. Bấm được (chốt vòng cleanup cuối, đúng luật đã có
+                     ở P1/P2): chip là LỐI TẮT của ô lọc tương ứng — bấm chip thì `ownFilters` của
+                     dim đó đổi ĐÚNG giá trị chip (ô lọc hiện lại đúng giá trị), bấm lại thì bỏ lọc,
+                     và mỗi lần bấm gọi `fetchList()` đúng 1 lần qua `onFilterChange()`. -->
                 <div v-if="allocationGroups.length" :hidden="summaryCollapsed" class="report-drill-chipbox">
                     <p class="report-drill-chipbox__title">Phân bổ theo cơ cấu</p>
                     <div class="report-drill-chips">
                         <div v-for="group in allocationGroups" :key="group.dim" class="report-drill-chips__grp">
                             <span class="report-drill-chips__label">{{ dimLabel(group.dim) }}</span>
                             <div class="report-drill-chips__list">
-                                <span
+                                <button
                                     v-for="item in group.items"
                                     :key="`${group.dim}-${item.id}`"
+                                    type="button"
                                     class="report-drill-chip"
+                                    :class="{ 'report-drill-chip--on': isChipActive(group.dim, item.id) }"
+                                    :title="`Lọc theo ${dimLabel(group.dim)}: ${item.name}`"
+                                    @click="toggleChip(group.dim, item.id)"
                                 >
                                     {{ item.name }}
                                     <b class="report-drill-chip__n">{{ money(item.count) }}</b>
-                                </span>
+                                </button>
                             </div>
                         </div>
                     </div>
                 </div>
             </template>
         </template>
 
         <!--
             Ô đặc biệt — 4 cột cần hiển thị khác nguyên văn `row[col.key]`: tên dự án (link + chip
             "Lập trong kỳ"), 2 badge trạng thái/kết quả, giá trị tiền. Các cột còn lại vẫn đi qua
@@ -239,24 +266,23 @@ const COLUMN_DEFS = {
     province_name: { label: 'Thị trường', align: '', sortKey: 'province' },
     scope_name: { label: 'Lĩnh vực', align: '', sortKey: 'scope' },
     industry_name: { label: 'Nhóm ngành', align: '' },
     customer_name: { label: 'Khách hàng', align: '' },
     result_text: { label: 'Kết quả', align: 'tkt-center', sortKey: 'result' },
     closed_reason: { label: 'Lý do thất bại', align: '' },
     amount: { label: 'Giá trị', align: 'tkt-right', sortKey: 'amount' },
 }
 
 /** `align` cũ (khoá nội bộ của `COLUMN_DEFS`, không đổi) -> `cellClass` của vỏ. `tkt-center` trỏ
-    thẳng vào `.report-drill-table__center` VỎ ĐÃ CÓ SẴN (khối KHÔNG scoped của
-    `V2BaseReportModal.vue`) — dùng lại, không định nghĩa trùng. `tkt-right` -> `.report-drill-table__money`
-    — cùng tên + cùng nội dung với lớp của `DevelopmentDrillModal.vue`/`DemandListModal.vue` (khuôn
-    adapter cột đã port ở 2 popup trước), định nghĩa KHÔNG scoped ở cuối file — xem comment ở đó. */
+    thẳng vào `.report-drill-table__center` và `tkt-right` trỏ vào `.report-drill-table__money` —
+    CẢ HAI đã có sẵn trong khối `<style scoped>` của `V2BaseReportModal.vue` (dọn về đó ở vòng
+    cleanup cuối, dùng CHUNG cho cả 3 popup báo cáo) — dùng lại, KHÔNG định nghĩa trùng ở file này. */
 const ALIGN_CLASS_MAP = {
     'tkt-center': 'report-drill-table__center',
     'tkt-right': 'report-drill-table__money',
 }
 
 const METRIC_LABELS = {
     total: 'Tổng dự án',
     open: 'Đang triển khai',
     closed: 'Đóng trong kỳ',
     won: 'Thành công',
@@ -447,20 +473,28 @@ export default {
         },
         /** Chip phân bổ SAU khi ẩn theo ĐÚNG `fieldVisibility` của ô lọc — dùng lại nguyên luật 1
             (dim đã cố định trên path) + luật 4 (industry ẩn scope, customer ẩn province), KHÔNG
             viết bộ luật ẩn thứ hai cho riêng chip (2 bộ sẽ lệch nhau — brief đã nhắc). */
         allocationGroups() {
             return (this.allocation || []).filter((group) => {
                 const filterKey = DIM_TO_FILTER_KEY[group.dim]
                 return !filterKey || this.fieldVisibility[filterKey]
             })
         },
+        /**
+         * Popup này KHÔNG gắn `reportDrillListMixin` (tự gọi API, xem đầu file) nên KHÔNG có sẵn
+         * `hasActiveFilter` của mixin — tự tính tương đương từ `ownFilters` để gate nút "Xoá lọc"
+         * (đúng khuôn P1/P2, tránh bấm lúc chưa lọc gì bắn thêm 1 request thừa).
+         */
+        hasActiveFilter() {
+            return Object.values(this.ownFilters).some((v) => v !== null && v !== '')
+        },
     },
     watch: {
         /** Ô lọc bị ẩn phải XOÁ GIÁ TRỊ — không thì thành lọc ngầm khi nó tái xuất hiện. */
         fieldVisibility: {
             deep: true,
             handler(vis) {
                 DIM_FILTER_KEYS.forEach((key) => {
                     if (!vis[key] && this.ownFilters[key] !== null) {
                         this.ownFilters[key] = null
                     }
@@ -582,20 +616,58 @@ export default {
                 this.allocation = []
                 this.total = 0
             } finally {
                 this.loading = false
             }
         },
         onFilterChange() {
             this.page = 1
             this.fetchList()
         },
+        /**
+         * Nút "Xoá lọc" (bổ sung vòng cleanup cuối — P3 từng thiếu so với P1/P2). Xoá SẠCH mọi ô
+         * lọc riêng của popup (kể cả giá trị mồi từ `baseParams`, giống hệt seed ban đầu) rồi gọi
+         * lại danh sách đúng 1 lần qua `onFilterChange()`.
+         */
+        resetOwnFilters() {
+            this.ownFilters = {
+                department_id: null,
+                part_id: null,
+                employee_id: null,
+                province_id: null,
+                customer_id: null,
+                scope_id: null,
+                industry_id: null,
+                status: null,
+                result: null,
+            }
+            this.selectedCustomerLocal = null
+            this.onFilterChange()
+        },
+        /**
+         * Chip phân bổ là LỐI TẮT của ô lọc tương ứng (bổ sung vòng cleanup cuối — đúng luật đã có
+         * ở P1 `DemandListModal.vue`): bấm chip = ghi thẳng vào `ownFilters` của đúng dim đó (ô lọc
+         * hiện lại đúng giá trị chip), bấm lại chip đang bật thì bỏ lọc. Gọi lại danh sách đúng 1
+         * lần qua `onFilterChange()`.
+         */
+        toggleChip(dim, id) {
+            const key = DIM_TO_FILTER_KEY[dim]
+            if (!key) return
+            this.ownFilters[key] = this.isChipActive(dim, id) ? null : id
+            this.onFilterChange()
+        },
+        isChipActive(dim, id) {
+            const key = DIM_TO_FILTER_KEY[dim]
+            if (!key) return false
+            const current = this.ownFilters[key]
+            return current !== null && current !== '' && String(current) === String(id)
+        },
         onCustomerSelect(option) {
             this.ownFilters.customer_id = option && option.id ? option.id : null
             this.selectedCustomerLocal = option && option.id ? { id: option.id, text: option.text } : null
             this.onFilterChange()
         },
         /** `@sort` của vỏ chỉ gửi `col.key` (vd `emp_name`) — quy về `sortKey` BE (vd `emp`) qua
             `columnDefs` rồi nối vào CHÍNH cơ chế sắp xếp BE sẵn có (gọi lại `fetchList()`), KHÔNG
             dùng máy sắp xếp client-side của mixin. */
         onSort({ key }) {
             const col = this.columnDefs.find((c) => c.key === key)
@@ -757,32 +829,45 @@ $teal-dark: #0e7490;
     left: 0;
     z-index: 1;
     background: #fff;
 }
 /* KHÔNG xuống dòng: 1 cơ cấu = 1 hàng, dài thì cuộn ngang cả khối */
 .report-drill-chips__list {
     display: flex;
     flex-wrap: nowrap;
     gap: 2px;
 }
+/* Bấm được (chốt vòng cleanup cuối) — trước đây là `<span>` trang trí thuần, nay là chip lọc nhanh
+   giống khuôn `.report-drill-sum__chip` của P1/P2, chỉ đổi tên class để không đụng CSS cũ. */
 .report-drill-chip {
     flex-shrink: 0;
     white-space: nowrap;
     display: inline-flex;
     align-items: baseline;
     gap: 5px;
     padding: 2px 7px;
     border: 1px solid #e6edf3;
     border-radius: 5px;
     background: #f8fafc;
+    font: inherit;
     font-size: 11.5px;
     color: $text-main;
+    cursor: pointer;
+    transition: background 0.12s ease;
+
+    &:hover {
+        background: #eef6fa;
+    }
+}
+.report-drill-chip--on {
+    border-color: #06b6d4;
+    background: #e2f5fa;
 }
 .report-drill-chip__n {
     font-weight: 800;
     color: $teal-dark;
     font-variant-numeric: tabular-nums;
 }
 
 .report-drill-filters {
     display: flex;
     flex-wrap: wrap;
@@ -822,27 +907,10 @@ $teal-dark: #0e7490;
     border: 1px solid rgba(37, 99, 235, 0.35);
     border-radius: 3px;
     background: rgba(37, 99, 235, 0.08);
     color: #1d4ed8;
     font-size: 10px;
     font-weight: 700;
     line-height: 16px;
     white-space: nowrap;
 }
 </style>
-
-<!-- KHÔNG scoped: `.report-drill-table__money` gắn vào ô `amount` qua `cellClass` (adapter
-     `columnDefs` ở trên) — `<td>` mang class đó do VỎ (`V2BaseReportModal.vue`) render bằng
-     TEMPLATE CỦA CHÍNH NÓ (`:class="col.cellClass"`), không phải slot content của popup này, nên
-     scoped attr của popup KHÔNG với tới (bài học đã trả giá — xem ghi chú đầu file). Cùng tên +
-     cùng nội dung với `.report-drill-table__money` của `DevelopmentDrillModal.vue`/`DemandListModal.vue`
-     (2 popup trước) — trùng tên CSS global nhưng không xung đột vì thuộc tính giống hệt nhau, cho 3
-     popup báo cáo 1 khuôn "ô tiền" thống nhất. `.report-drill-table__center` (dùng cho created_at/
-     status_text/result_text) KHÔNG cần định nghĩa lại ở đây — vỏ đã có sẵn trong khối KHÔNG scoped
-     của chính nó. -->
-<style>
-.report-drill-table__money {
-    text-align: right;
-    font-weight: 700;
-    font-variant-numeric: tabular-nums;
-}
-</style>
diff --git a/utils/mixins/reportDrillListMixin.js b/utils/mixins/reportDrillListMixin.js
index 53098c81e..81daaba8d 100644
--- a/utils/mixins/reportDrillListMixin.js
+++ b/utils/mixins/reportDrillListMixin.js
@@ -1,22 +1,32 @@
 /**
  * MÁY CLIENT-SIDE cho popup drill-down của màn báo cáo.
  *
  * CHỈ ôm phần 3 popup lớn giống hệt nhau: sắp xếp, phân trang, state bộ lọc.
  * KHÔNG ôm phần lọc — 3 popup dùng 3 chiến lược khác nhau (đo 2026-09-17):
  *   · DemandListModal      — lọc ở SERVER (emit `filter`, màn cha tải lại)
- *   · DevelopmentDrillModal — lọc CLIENT tại chỗ
- *   · ProjectListModal      — lọc ở SERVER, popup tự gọi API
- * Vì vậy `onFilterChange()` là HOOK do component tự cài, còn `applyLocalFilters()` là hàm
- * TUỲ CHỌN cho popup lọc client-side.
+ *   · DevelopmentDrillModal — lọc CLIENT tại chỗ (tự viết `filteredRows` riêng)
+ *   · ProjectListModal      — lọc ở SERVER, popup tự gọi API (KHÔNG gắn mixin này — xem dưới)
+ * Vì vậy `onFilterChange()` là HOOK do component tự cài, KHÔNG có hàm lọc chung nào trong mixin —
+ * mỗi popup tự quyết cách lọc của mình.
  *
  * Component dùng mixin phải khai: `rows`, `columns`, `emptyFilters()`, `onFilterChange()`.
+ *
+ * ⚠️ QUY TẮC HÀNH ĐỘNG — popup nào để BE lo HẾT lọc/sắp/phân trang (tự gọi API ở mọi lần đổi
+ * trang/sắp xếp/lọc, như `ProjectListModal.vue`) thì KHÔNG gắn mixin này: state phân trang/sắp xếp
+ * client-side của mixin (`sortedRows`/`pagedRows`/`safePage`…) vô nghĩa khi dữ liệu đã được BE cắt
+ * sẵn theo trang. Tự quản state tương đương (`page`, `perPage`, `sort`, `ownFilters`…) ngay trong
+ * component, xem `ProjectListModal.vue` làm mẫu.
+ * ⚠️ `filterFields`/tên state bộ lọc riêng của từng popup (`filters`, `ownFilters`…) KHÔNG PHẢI hợp
+ * đồng chung của mixin — mixin không đọc/ghi field nào tên đó ngoài `hasActiveFilter` đọc qua
+ * `this.filters` (component tự đặt `data(){ filters: this.emptyFilters() }`, xem dưới). Mỗi popup
+ * tự đặt khoá lọc riêng theo đúng bộ ô lọc của nó, đừng suy diễn 1 khuôn field dùng chung.
  */
 const dateSortKey = (value) => {
     if (!value) return null
     // Dữ liệu hiển thị dạng "dd/mm/yyyy" hoặc "dd/mm/yyyy hh:mm" — `new Date()` đọc sai (hiểu là
     // mm/dd). ⚠️ PHẢI bắt cả giờ:phút — bỏ khuyết thì 2 dòng cùng ngày khác giờ xếp lẫn lộn theo
     // thứ tự ban đầu của mảng thay vì theo thời gian (đo được ở DemandListModal — Task 5).
     const m = String(value).match(/^(\d{2})\/(\d{2})\/(\d{4})(?:\s+(\d{2}):(\d{2}))?/)
     if (m) {
         const [, d, mo, y, h = '00', mi = '00'] = m
         return new Date(`${y}-${mo}-${d}T${h}:${mi}:00`).getTime()
@@ -118,26 +128,12 @@ export default {
         },
         /**
          * XOÁ LỌC (nút "Xoá lọc" trong popup) — dọn state rồi CHỦ ĐỘNG gọi `onFilterChange()` để
          * tải lại theo bộ lọc rỗng. Khác `resetFilterState()` ở đúng 1 điểm: đây là hành động NGƯỜI
          * DÙNG BẤM nên phải tải lại; `resetFilterState()` là dọn ngầm khi popup đã có dữ liệu mới.
          */
         resetFilters() {
             this.resetFilterState()
             this.onFilterChange()
         },
-        /** TUỲ CHỌN — chỉ popup lọc client-side gọi tới. Khớp chuỗi không dấu phân biệt hoa thường. */
-        applyLocalFilters(rows) {
-            const kw = this.keyword.trim().toLowerCase()
-            return rows.filter((row) => {
-                const okFilters = Object.keys(this.filters).every((param) => {
-                    const want = this.filters[param]
-                    if (want === null || want === '') return true
-                    return String(row[param]) === String(want)
-                })
-                if (!okFilters) return false
-                if (!kw) return true
-                return Object.values(row).some((v) => String(v == null ? '' : v).toLowerCase().includes(kw))
-            })
-        },
     },
 }
