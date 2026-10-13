# Review package: 4ccaf4c34..b41b207cc

## Commits
b41b207cc fix(report): gỡ wrapper .report-drill-footer làm mất margin bootstrap giữa nút (vòng sửa 3/5)

## Files changed
 components/report/V2BaseReportModal.vue | 14 ++++++++++----
 1 file changed, 10 insertions(+), 4 deletions(-)

## Diff
diff --git a/components/report/V2BaseReportModal.vue b/components/report/V2BaseReportModal.vue
index c90747778..7c1090b5f 100644
--- a/components/report/V2BaseReportModal.vue
+++ b/components/report/V2BaseReportModal.vue
@@ -90,23 +90,21 @@
             :current-page="currentPage"
             :current-page-size="currentPageSize"
             :total-rows="totalRows"
             :item-label="itemLabel"
             :page-size-options="pageSizeOptions"
             @page-change="(v) => $emit('page-change', v)"
             @page-size-change="(v) => $emit('page-size-change', v)"
         />
 
         <template #footer>
-            <div class="report-drill-footer">
-                <slot name="footer"></slot>
-            </div>
+            <slot name="footer"></slot>
         </template>
     </V2BaseModal>
 </template>
 
 <script>
 import V2BaseModal from '@/components/modal/V2BaseModal.vue'
 import V2BaseTableScroll from '@/components/V2BaseTableScroll.vue'
 import V2BasePagination from '@/components/V2BasePagination.vue'
 
 export default {
@@ -200,21 +198,29 @@ export default {
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
-.report-drill-footer,
+/* ⚠️ Vòng sửa 3/5 — ĐÃ GỠ `.report-drill-footer` (từng bọc `<slot name="footer">` ở vòng sửa 2/5).
+   `V2BaseModal` render sẵn `.modal-footer` bao ngoài slot; bootstrap 4.6 có rule
+   `.modal-footer > * { margin: 0.25rem }` CHỈ áp cho CON TRỰC TIẾP. Bọc thêm 1 div làm các nút
+   thật (do Task 5 đặt vào slot) rơi xuống thành cháu, mất hẳn margin 4px mỗi bên → hàng nút dính
+   sát nhau. `.report-drill-footer` không tự nó tạo `gap`, nên hướng đúng là GỠ wrapper, không phải
+   đắp thêm `display:flex; gap` — 2 popup khác dựng trên `V2BaseModal` (`ProjectListModal.vue`,
+   `DevelopmentDrillModal.vue`) đều đặt nút thẳng vào slot `#footer`, không bọc gì, và margin mặc
+   định của bootstrap đã cho đúng 8px giữa 2 nút. Đo thật (vòng sửa 3/5): khoảng cách ngang giữa 2
+   nút footer = 8px (xem báo cáo). */
 .report-drill-paging {
     flex-shrink: 0;
 }
 .report-drill-dialog--full .modal-content {
     height: 100vh;
     max-height: 100vh;
     border-radius: 0;
 }
 
 /* `.report-drill-wrap` gắn vào bảng qua `body-class` của `V2BaseTableScroll` (component con) —
