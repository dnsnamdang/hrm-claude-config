# Review package: 127285043..4ccaf4c34

## Commits
4ccaf4c34 fix(report): sửa .report-drill-content/.report-drill-scroll/.report-drill-footer chết (vòng sửa 2/5)

## Files changed
 components/report/V2BaseReportModal.vue | 86 +++++++++++++++++++--------------
 1 file changed, 50 insertions(+), 36 deletions(-)

## Diff
diff --git a/components/report/V2BaseReportModal.vue b/components/report/V2BaseReportModal.vue
index e98847089..c90747778 100644
--- a/components/report/V2BaseReportModal.vue
+++ b/components/report/V2BaseReportModal.vue
@@ -43,66 +43,70 @@
                         <i class="ri-close-line"></i>
                     </button>
                 </div>
             </div>
         </template>
 
         <slot name="filters"></slot>
         <slot name="back"></slot>
         <slot name="summary"></slot>
 
-        <V2BaseTableScroll :max-height="maxTableHeight" body-class="report-drill-wrap">
-            <table class="report-drill-table">
-                <thead>
-                    <tr>
-                        <th style="min-width: 46px">STT</th>
-                        <th v-for="col in columns" :key="col.key" :style="{ minWidth: col.width }">
-                            <span v-if="col.sortable" class="report-drill-sort" @click="$emit('sort', { key: col.key })">
-                                {{ col.label }}
-                                <i :class="sortIcon(col.key)"></i>
-                            </span>
-                            <span v-else>{{ col.label }}</span>
-                        </th>
-                    </tr>
-                </thead>
-                <tbody>
-                    <tr v-for="(row, index) in rows" :key="row[rowKey]">
-                        <td class="report-drill-table__center">{{ startIndex + index + 1 }}</td>
-                        <td v-for="col in columns" :key="col.key" :class="col.cellClass">
-                            <slot :name="`cell-${col.key}`" :row="row" :index="index" :column="col">
-                                {{ row[col.field] }}
-                            </slot>
-                        </td>
-                    </tr>
-                    <tr v-if="!rows.length">
-                        <td :colspan="columns.length + 1" class="report-drill-table__empty">
-                            {{ loading ? 'Đang tải…' : emptyText }}
-                        </td>
-                    </tr>
-                </tbody>
-            </table>
-        </V2BaseTableScroll>
+        <div class="report-drill-scroll">
+            <V2BaseTableScroll :max-height="maxTableHeight" body-class="report-drill-wrap">
+                <table class="report-drill-table">
+                    <thead>
+                        <tr>
+                            <th style="min-width: 46px">STT</th>
+                            <th v-for="col in columns" :key="col.key" :style="{ minWidth: col.width }">
+                                <span v-if="col.sortable" class="report-drill-sort" @click="$emit('sort', { key: col.key })">
+                                    {{ col.label }}
+                                    <i :class="sortIcon(col.key)"></i>
+                                </span>
+                                <span v-else>{{ col.label }}</span>
+                            </th>
+                        </tr>
+                    </thead>
+                    <tbody>
+                        <tr v-for="(row, index) in rows" :key="row[rowKey]">
+                            <td class="report-drill-table__center">{{ startIndex + index + 1 }}</td>
+                            <td v-for="col in columns" :key="col.key" :class="col.cellClass">
+                                <slot :name="`cell-${col.key}`" :row="row" :index="index" :column="col">
+                                    {{ row[col.field] }}
+                                </slot>
+                            </td>
+                        </tr>
+                        <tr v-if="!rows.length">
+                            <td :colspan="columns.length + 1" class="report-drill-table__empty">
+                                {{ loading ? 'Đang tải…' : emptyText }}
+                            </td>
+                        </tr>
+                    </tbody>
+                </table>
+            </V2BaseTableScroll>
+        </div>
 
         <V2BasePagination
             v-if="!loading && totalRows"
             class="report-drill-paging"
             :current-page="currentPage"
             :current-page-size="currentPageSize"
             :total-rows="totalRows"
             :item-label="itemLabel"
             :page-size-options="pageSizeOptions"
             @page-change="(v) => $emit('page-change', v)"
             @page-size-change="(v) => $emit('page-size-change', v)"
         />
 
         <template #footer>
-            <slot name="footer"></slot>
+            <div class="report-drill-footer">
+                <slot name="footer"></slot>
+            </div>
         </template>
     </V2BaseModal>
 </template>
 
 <script>
 import V2BaseModal from '@/components/modal/V2BaseModal.vue'
 import V2BaseTableScroll from '@/components/V2BaseTableScroll.vue'
 import V2BasePagination from '@/components/V2BasePagination.vue'
 
 export default {
@@ -161,50 +165,60 @@ export default {
     },
 }
 </script>
 
 <style lang="scss">
 /* KHÔNG `scoped`: `b-modal` render dialog ra ngoài cây component nên style scoped không với tới.
    Toàn bộ giá trị dưới đây port từ `.care-drill-*` của mẫu nguồn (`DemandListModal.vue` dòng
    846–909) — đổi tên tiền tố, giữ nguyên số. */
 .report-drill-dialog { max-width: 1400px; }
 .report-drill-dialog--full { width: 100vw; max-width: 100vw; margin: 0; min-height: 100vh; }
-.report-drill-content {
+
+/* ⚠️ Vòng sửa 2/5 — `.report-drill-content` KHÔNG tồn tại làm class riêng: bản gốc gắn nó thẳng
+   qua `content-class="care-drill-content"` trên `<b-modal>` (`DemandListModal.vue:29`), nhưng
+   `V2BaseModal.vue:20` hard-code `content-class="shadow"` và không có prop để truyền content-class
+   tuỳ biến — sửa trong `V2BaseModal` là ngoài phạm vi Task 3. Bám selector hậu duệ theo
+   `.report-drill-dialog` (đã áp đúng qua prop `dialogClass` có sẵn) để tới `.modal-content` /
+   `.modal-header` / `.modal-body` mặc định của bootstrap-vue. Giá trị bên trong GIỮ NGUYÊN, không
+   chỉnh số — đo thật (vòng sửa 2/5): trước khi sửa `.modal-content` không có `height` (auto),
+   `.modal-header` mang padding/border mặc định bootstrap; sau khi sửa `height ≈ 92vh` và
+   `padding-top`/`border-bottom-width` của `.modal-header` đều `0px` (xem báo cáo). */
+.report-drill-dialog .modal-content {
     height: 92vh;
     display: flex;
     flex-direction: column;
     overflow: hidden;
 }
-.report-drill-content .modal-header {
+.report-drill-dialog .modal-header {
     padding: 0;
     border: 0;
     flex-shrink: 0;
 }
-.report-drill-content .modal-body {
+.report-drill-dialog .modal-body {
     padding: 16px;
     flex: 1 1 auto;
     min-height: 0;
     overflow: hidden;
     display: flex;
     flex-direction: column;
 }
 .report-drill-scroll {
     flex: 1 1 auto;
     min-height: 120px;
     display: flex;
     flex-direction: column;
 }
 .report-drill-footer,
 .report-drill-paging {
     flex-shrink: 0;
 }
-.report-drill-dialog--full .report-drill-content {
+.report-drill-dialog--full .modal-content {
     height: 100vh;
     max-height: 100vh;
     border-radius: 0;
 }
 
 /* `.report-drill-wrap` gắn vào bảng qua `body-class` của `V2BaseTableScroll` (component con) —
    PHẢI để ở khối KHÔNG scoped như trên, lý do y hệt: phần tử đó nằm trong template RIÊNG của
    component con (div `ref="body"`), không phải slot content của `V2BaseReportModal`, nên selector
    scoped của ta không với tới (đo thật vòng sửa 1/5: để ở khối scoped ra `border-top-width: 0px`,
    `border-radius: 0px` — viền và bo góc biến mất hoàn toàn dù class có đúng tên). Giá trị port từ
