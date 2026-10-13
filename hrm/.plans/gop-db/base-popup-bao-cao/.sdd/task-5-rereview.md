# Review package: f73f569b8..00877f63f

## Commits
00877f63f fix(report): vòng sửa 1/5 - đổi nốt id-prefix + khôi phục cuộn-về-đầu khi lật trang

## Files changed
 components/report/V2BaseReportModal.vue            | 24 +++++++++++++++++++---
 .../components/DemandListModal.vue                 |  2 +-
 2 files changed, 22 insertions(+), 4 deletions(-)

## Diff
diff --git a/components/report/V2BaseReportModal.vue b/components/report/V2BaseReportModal.vue
index 8b09da1b8..3b10d44a7 100644
--- a/components/report/V2BaseReportModal.vue
+++ b/components/report/V2BaseReportModal.vue
@@ -50,21 +50,21 @@
                     </button>
                 </div>
             </div>
         </template>
 
         <slot name="filters"></slot>
         <slot name="back"></slot>
         <slot name="summary"></slot>
 
         <div class="report-drill-scroll">
-            <V2BaseTableScroll :max-height="maxTableHeight" body-class="report-drill-wrap">
+            <V2BaseTableScroll ref="tableScroll" :max-height="maxTableHeight" body-class="report-drill-wrap">
                 <table class="report-drill-table">
                     <thead>
                         <tr>
                             <th style="min-width: 46px">STT</th>
                             <th v-for="col in columns" :key="col.key" :style="{ minWidth: col.width }">
                                 <span v-if="col.sortable" class="report-drill-sort" @click="$emit('sort', { key: col.key })">
                                     {{ col.label }}
                                     <i :class="sortIcon(col.key)"></i>
                                 </span>
                                 <span v-else>{{ col.label }}</span>
@@ -91,22 +91,22 @@
         </div>
 
         <V2BasePagination
             v-if="!loading && totalRows"
             class="report-drill-paging"
             :current-page="currentPage"
             :current-page-size="currentPageSize"
             :total-rows="totalRows"
             :item-label="itemLabel"
             :page-size-options="pageSizeOptions"
-            @page-change="(v) => $emit('page-change', v)"
-            @page-size-change="(v) => $emit('page-size-change', v)"
+            @page-change="onPageChange"
+            @page-size-change="onPageSizeChange"
         />
 
         <template #footer>
             <slot name="footer"></slot>
         </template>
     </V2BaseModal>
 </template>
 
 <script>
 import V2BaseModal from '@/components/modal/V2BaseModal.vue'
@@ -155,20 +155,38 @@ export default {
     },
     methods: {
         syncBvModal(value) {
             if (value) this.$bvModal.show(this.modalId)
             else this.$bvModal.hide(this.modalId)
         },
         toggleFullscreen() {
             this.fullscreen = !this.fullscreen
             this.$emit('toggle-fullscreen', this.fullscreen)
         },
+        /**
+         * Sang trang mới (hoặc đổi số dòng/trang) phải cuộn bảng về đầu, không thì đang ở giữa
+         * trang cũ nhìn như chưa đổi gì — port nguyên văn lý do + hành vi từ `onPageChange()` cũ
+         * của `DemandListModal.vue` (bản trước Task 5). Đặt Ở VỎ chứ không ở mixin: vùng cuộn là
+         * chi tiết DOM, mixin không được biết gì về DOM.
+         */
+        resetScroll() {
+            const body = this.$refs.tableScroll && this.$refs.tableScroll.$refs.body
+            if (body) body.scrollTop = 0
+        },
+        onPageChange(page) {
+            this.$emit('page-change', page)
+            this.resetScroll()
+        },
+        onPageSizeChange(size) {
+            this.$emit('page-size-change', size)
+            this.resetScroll()
+        },
         sortIcon(key) {
             if (this.sort.key !== key) return 'ri-arrow-up-down-line'
             return this.sort.dir === 'asc' ? 'ri-arrow-up-line' : 'ri-arrow-down-line'
         },
     },
 }
 </script>
 
 <style lang="scss">
 /* KHÔNG `scoped`: `b-modal` render dialog ra ngoài cây component nên style scoped không với tới.
diff --git a/pages/assign/report/potential-customer-care/components/DemandListModal.vue b/pages/assign/report/potential-customer-care/components/DemandListModal.vue
index d09e7368f..92fa186f2 100644
--- a/pages/assign/report/potential-customer-care/components/DemandListModal.vue
+++ b/pages/assign/report/potential-customer-care/components/DemandListModal.vue
@@ -110,21 +110,21 @@
             </div>
         </template>
 
         <template #summary>
             <!-- Khối KPI: dùng lại đúng component của màn chính, bản thu nhỏ -->
             <KpiBoxes
                 v-if="!backTo && kpis.length && !summaryCollapsed"
                 :kpis="kpis"
                 compact
                 :show-title="false"
-                id-prefix="care-drill"
+                id-prefix="report-drill"
                 class="mb-2"
                 @drill="onKpiDrill"
             />
 
             <div v-if="crossStats.length && !summaryCollapsed" class="report-drill-sumbox">
                 <p class="report-drill-sumbox__title">Phân bổ nhu cầu theo cơ cấu</p>
                 <!-- MỘT container cuộn ngang chung cho cả 3 cơ cấu (mockup): các hàng thẳng cột với
                      nhau và chỉ có 1 thanh cuộn, thay vì mỗi hàng một thanh riêng. -->
                 <div class="report-drill-sum">
                     <div v-for="stat in crossStats" :key="stat.key" class="report-drill-sum__grp">
