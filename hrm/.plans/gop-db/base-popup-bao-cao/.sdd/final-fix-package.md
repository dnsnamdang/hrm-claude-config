# Review package: 00877f63f..26d17c2c2

## Commits
26d17c2c2 fix: sửa gộp phát hiện vòng rà soát cuối cho popup báo cáo dùng chung

## Files changed
 components/V2BaseTableScroll.vue                   | 12 ++++++++
 components/report/V2BaseReportModal.vue            |  7 +++--
 .../components/CustomerMeetingHistoryModal.vue     |  4 ++-
 .../components/DemandListModal.vue                 | 33 ++++++++++++++++++----
 .../components/ProjectListModal.vue                |  8 ++++--
 utils/mixins/reportDrillListMixin.js               | 19 ++++++++++++-
 6 files changed, 70 insertions(+), 13 deletions(-)

## Diff
diff --git a/components/V2BaseTableScroll.vue b/components/V2BaseTableScroll.vue
index 991d549b0..9a743e8e5 100644
--- a/components/V2BaseTableScroll.vue
+++ b/components/V2BaseTableScroll.vue
@@ -62,20 +62,32 @@ export default {
     },
     beforeDestroy() {
         const top = this.$refs.topScroll
         const body = this.$refs.body
         if (top) top.removeEventListener('scroll', this.onTopScroll)
         if (body) body.removeEventListener('scroll', this.onBodyScroll)
         window.removeEventListener('resize', this.sync)
         if (this.ro) this.ro.disconnect()
     },
     methods: {
+        /**
+         * API CÔNG KHAI — cuộn vùng bảng về đầu. Thêm cho nơi gọi NGOÀI component (vd
+         * `V2BaseReportModal.vue` sau khi đổi trang) không phải thò tay vào ref nội bộ
+         * `this.$refs.tableScroll.$refs.body`: `body` là ref RIÊNG của component này, đổi tên nó
+         * ở đây làm mọi nơi đang bám `$refs.body` từ bên ngoài cuộn-về-đầu chết im lặng (không lỗi
+         * console, không cảnh báo — chỉ đơn giản không cuộn nữa). Chỉ THÊM method, không đổi gì có
+         * sẵn — 38 chỗ khác đang dùng component này.
+         */
+        scrollToTop() {
+            const body = this.$refs.body
+            if (body) body.scrollTop = 0
+        },
         sync() {
             const body = this.$refs.body
             const inner = this.$refs.topInner
             if (!body || !inner) return
             const table = body.querySelector('table')
             const width = table ? table.scrollWidth : body.scrollWidth
             inner.style.width = `${width}px`
             this.overflowing = width > body.clientWidth + 1
         },
         onTopScroll() {
diff --git a/components/report/V2BaseReportModal.vue b/components/report/V2BaseReportModal.vue
index 3b10d44a7..b6a55f27f 100644
--- a/components/report/V2BaseReportModal.vue
+++ b/components/report/V2BaseReportModal.vue
@@ -160,24 +160,27 @@ export default {
         },
         toggleFullscreen() {
             this.fullscreen = !this.fullscreen
             this.$emit('toggle-fullscreen', this.fullscreen)
         },
         /**
          * Sang trang mới (hoặc đổi số dòng/trang) phải cuộn bảng về đầu, không thì đang ở giữa
          * trang cũ nhìn như chưa đổi gì — port nguyên văn lý do + hành vi từ `onPageChange()` cũ
          * của `DemandListModal.vue` (bản trước Task 5). Đặt Ở VỎ chứ không ở mixin: vùng cuộn là
          * chi tiết DOM, mixin không được biết gì về DOM.
+         *
+         * Gọi qua API CÔNG KHAI `scrollToTop()` của `V2BaseTableScroll`, KHÔNG thò tay vào
+         * `$refs.tableScroll.$refs.body` — `body` là ref NỘI BỘ của component con, đổi tên nó ở
+         * đó làm cuộn-về-đầu chết im lặng mà không có lỗi nào báo ra (đã rơi rụng một lần).
          */
         resetScroll() {
-            const body = this.$refs.tableScroll && this.$refs.tableScroll.$refs.body
-            if (body) body.scrollTop = 0
+            if (this.$refs.tableScroll) this.$refs.tableScroll.scrollToTop()
         },
         onPageChange(page) {
             this.$emit('page-change', page)
             this.resetScroll()
         },
         onPageSizeChange(size) {
             this.$emit('page-size-change', size)
             this.resetScroll()
         },
         sortIcon(key) {
diff --git a/pages/assign/report/potential-customer-care/components/CustomerMeetingHistoryModal.vue b/pages/assign/report/potential-customer-care/components/CustomerMeetingHistoryModal.vue
index 776934322..e3c6abadb 100644
--- a/pages/assign/report/potential-customer-care/components/CustomerMeetingHistoryModal.vue
+++ b/pages/assign/report/potential-customer-care/components/CustomerMeetingHistoryModal.vue
@@ -251,21 +251,23 @@ export default {
    còn nhiều màn khác gọi tới), xung đột z-index là do popup lịch sử tạo ra nên nó tự gánh. */
 .report-print-modal {
     z-index: 1064;
 }
 .care-hist-dialog {
     max-width: 1100px;
     width: 92vw;
 }
 .care-hist-content {
     /* Khoá chiều cao để danh sách dài không đẩy popup tràn viewport — cùng lý do đã ghi ở
-       `.care-drill-content`, nhưng thấp hơn vì popup này ít nội dung hơn hẳn. */
+       `.report-drill-dialog .modal-content` (`components/report/V2BaseReportModal.vue`, vỏ dùng
+       chung cho popup báo cáo — `.care-drill-content` là tên CŨ, đã đổi ở Task 3), nhưng thấp hơn
+       vì popup này ít nội dung hơn hẳn. */
     max-height: 86vh;
     display: flex;
     flex-direction: column;
     overflow: hidden;
 }
 .care-hist-content .modal-header {
     padding: 0;
     border: 0;
     flex-shrink: 0;
 }
diff --git a/pages/assign/report/potential-customer-care/components/DemandListModal.vue b/pages/assign/report/potential-customer-care/components/DemandListModal.vue
index 92fa186f2..6d19c3103 100644
--- a/pages/assign/report/potential-customer-care/components/DemandListModal.vue
+++ b/pages/assign/report/potential-customer-care/components/DemandListModal.vue
@@ -534,27 +534,32 @@ export default {
             if (this.drillTypes.includes(key)) return false
             // Key chỉ có 1 cấp (nhóm chỉ tiêu, hoặc dữ liệu cũ): vẫn ẩn ô CHA của cấp đang xem
             const pairs = { sector: 'field', ward: 'market', emp: 'dept', hpart: 'hdept' }
             if (pairs[this.drillType] === key) return false
             return true
         },
         /**
          * MỞ POPUP MỚI: trả cả trạng thái xem lẫn bộ lọc về mặc định (mockup `openDrill()` bỏ
          * class full + gọi resetDrillFilters). Phóng to/thu nhỏ nay do vỏ `V2BaseReportModal` tự
          * quản (nó cũng tự trả về bình thường mỗi khi `visible` bật lại).
+         *
+         * ⚠️ Dọn state bằng `resetFilterState()` (KHÔNG gọi hook), không phải `resetFilters()`:
+         * đường này chạy khi màn cha ĐÃ tự tải `rows` mới theo `drillKey` mới, gọi `onFilterChange()`
+         * ở đây là bắn thêm 1 request `demand-list` trùng với request màn cha vừa gửi — đúng hồi quy
+         * đã xảy ra khi 2 vai (dọn ngầm / xoá lọc rồi tải lại) bị gộp làm một ở Task 5.
          */
         resetLocal() {
             // Mở popup mới -> trả về mặc định THU GỌN
             this.summaryCollapsed = true
             this.backTo = null
             this.sort = { key: '', dir: 'asc' }
-            this.resetFilters()
+            this.resetFilterState()
         },
         /**
          * Chip "Phân bổ nhu cầu theo cơ cấu" CHÍNH LÀ lối tắt của ô lọc tương ứng (mockup:
          * `sel.value = sel.value === id ? '' : id` rồi nạp lại ô con). Vì vậy chip đọc/ghi
          * THẲNG vào `filters` — không giữ state riêng, nếu không bảng lọc theo chip mà ô lọc
          * vẫn trống, người dùng không biết đang lọc theo gì để bỏ ra.
          */
         chipParam(dimension) {
             return { field: 'drill_field_id', market: 'drill_province_id', dept: 'drill_department_id' }[dimension]
         },
@@ -796,25 +801,21 @@ $text-muted: #6b7280;
     align-items: center;
     gap: 10px;
     margin-bottom: 8px;
 }
 .report-drill-back__from {
     font-size: 11.5px;
     color: $text-muted;
 }
 
 /* ---- Các ô bảng đặc biệt (chưa có ở vỏ dùng chung) ---- */
-.report-drill-table__money {
-    text-align: right;
-    font-weight: 700;
-    font-variant-numeric: tabular-nums;
-}
+/* `.report-drill-table__money` chuyển sang khối KHÔNG scoped phía dưới — xem comment ở đó. */
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
@@ -840,10 +841,30 @@ $text-muted: #6b7280;
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
+
+<!-- KHÔNG scoped: `td.report-drill-table__money` (cột "Giá trị đầu tư dự kiến") được VỎ
+     `V2BaseReportModal` render (nó lặp `columns` rồi gắn `:class="col.cellClass"` vào `<td>` bằng
+     TEMPLATE CỦA CHÍNH NÓ, xem `components/report/V2BaseReportModal.vue`) — attribute `data-v-xxx`
+     của style scoped chỉ đóng lên phần tử do TEMPLATE của `DemandListModal.vue` render, không với
+     tới `<td>` đó. Để rule này trong khối scoped ở trên thì nó lặng lẽ KHÔNG áp dụng: không báo
+     lỗi, chỉ đơn giản là `<td>` mang đúng class mà không nhận style (đo thật: textAlign "left",
+     fontWeight 400 thay vì "right" / 700). Rà lại TOÀN BỘ `cellClass` khai trong mảng `columns` của
+     file này: `report-drill-table__center` (start/repair/status) đã có sẵn trong khối KHÔNG scoped
+     của chính `V2BaseReportModal.vue` (thuộc về vỏ) nên không dính lỗi này — chỉ
+     `report-drill-table__money` là class NGHIỆP VỤ riêng của popup này bị lọt lưới. ⚠️ KHÔNG chuyển
+     nó vào `V2BaseReportModal.vue` — đó là class nghiệp vụ của popup CSKH, không phải của vỏ dùng
+     chung. -->
+<style>
+.report-drill-table__money {
+    text-align: right;
+    font-weight: 700;
+    font-variant-numeric: tabular-nums;
+}
+</style>
diff --git a/pages/assign/report/prospective-project-results/components/ProjectListModal.vue b/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
index 3febb1dc7..615ebfdd9 100644
--- a/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
+++ b/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
@@ -75,21 +75,22 @@
                 </div>
                 <div class="tkt-drill-sum__item">
                     <span>Tỷ lệ thành công</span><strong>{{ rateText(nodeMetrics.success_rate) }}</strong>
                 </div>
             </div>
 
             <!-- Chip phân bổ (Task 14b, design.md mục "Luật POPUP chi tiết" điểm 3): LUÔN Phòng
                  ban + 2 chiều cơ cấu theo tiêu chí. Ẩn theo ĐÚNG `fieldVisibility` của ô lọc
                  (`allocationGroups` bên dưới lọc lại bằng chính computed đó) — không viết luật ẩn
                  thứ hai. Dải chip cuộn ngang trong 1 khối chung (khuôn CSKH `DemandListModal.vue`
-                 `.care-drill-sum`) khi nhiều mục — KHÔNG phải chip bị cắt. -->
+                 `.report-drill-sum` — tên CŨ là `.care-drill-sum`, đã đổi ở Task 3) khi nhiều mục —
+                 KHÔNG phải chip bị cắt. -->
             <div v-if="allocationGroups.length" :hidden="summaryCollapsed" class="tkt-drill-chipbox">
                 <p class="tkt-drill-chipbox__title">Phân bổ theo cơ cấu</p>
                 <div class="tkt-drill-chips">
                     <div v-for="group in allocationGroups" :key="group.dim" class="tkt-drill-chips__grp">
                         <span class="tkt-drill-chips__label">{{ dimLabel(group.dim) }}</span>
                         <div class="tkt-drill-chips__list">
                             <span
                                 v-for="item in group.items"
                                 :key="`${group.dim}-${item.id}`"
                                 class="tkt-drill-chip"
@@ -674,22 +675,23 @@ $teal-dark: #0e7490;
         font-variant-numeric: tabular-nums;
     }
 }
 .tkt-drill-sum__item--good strong {
     color: #16a34a;
 }
 .tkt-drill-sum__item--bad strong {
     color: #dc2626;
 }
 
-/* Chip phân bổ (Task 14b) — khuôn cuộn ngang port từ CSKH `DemandListModal.vue` `.care-drill-sum`
-   (1 thanh cuộn mảnh DÙNG CHUNG cho mọi hàng, không phải mỗi hàng 1 thanh riêng). */
+/* Chip phân bổ (Task 14b) — khuôn cuộn ngang port từ CSKH `DemandListModal.vue` `.report-drill-sum`
+   (tên CŨ là `.care-drill-sum`, đã đổi ở Task 3) — 1 thanh cuộn mảnh DÙNG CHUNG cho mọi hàng, không
+   phải mỗi hàng 1 thanh riêng. */
 .tkt-drill-chipbox {
     flex-shrink: 0;
     margin: 0 0 10px;
     padding: 0 0 8px;
     border-bottom: 1px dashed #e2e8f0;
 }
 .tkt-drill-chipbox__title {
     margin: 0 0 5px;
     font-size: 11px;
     font-weight: 800;
diff --git a/utils/mixins/reportDrillListMixin.js b/utils/mixins/reportDrillListMixin.js
index 386728815..53098c81e 100644
--- a/utils/mixins/reportDrillListMixin.js
+++ b/utils/mixins/reportDrillListMixin.js
@@ -87,32 +87,49 @@ export default {
         /* Đổi tập dữ liệu (lượt drill mới / cha tải lại) -> về trang 1. Chỉ dựa vào `safePage` là
            chưa đủ: tập mới vẫn nhiều trang thì người dùng bị bỏ lại ở trang 3 của kết quả khác. */
         rows() {
             this.page = 1
         },
     },
     methods: {
         toggleSort(key) {
             if (this.sort.key === key) this.sort = { key, dir: this.sort.dir === 'asc' ? 'desc' : 'asc' }
             else this.sort = { key, dir: 'asc' }
+            /* Đổi thứ tự là đổi cả tập đang xem -> đứng lại trang 5 là vô nghĩa */
+            this.page = 1
         },
         onPageChange(page) {
             this.page = page
         },
         onPageSizeChange(size) {
             this.pageSize = size
             this.page = 1
         },
-        resetFilters() {
+        /**
+         * DỌN STATE IM LẶNG — chỉ đặt lại `keyword`/`filters`/`page`, KHÔNG gọi `onFilterChange()`.
+         * Dùng cho đường MỞ POPUP MỚI / ĐỔI DRILL KEY (`resetLocal()` trong `DemandListModal.vue`):
+         * lúc đó màn cha ĐÃ tự tải `rows` mới theo key mới rồi, gọi hook ở đây là bắn thêm 1 request
+         * `demand-list` TRÙNG với request màn cha vừa gửi — đúng hồi quy đã xảy ra khi 2 vai bị gộp
+         * làm một ở Task 5. ⚠️ GỘP lại với `resetFilters()` bên dưới là tái phát lỗi đó.
+         */
+        resetFilterState() {
             this.keyword = ''
             this.filters = this.emptyFilters()
             this.page = 1
+        },
+        /**
+         * XOÁ LỌC (nút "Xoá lọc" trong popup) — dọn state rồi CHỦ ĐỘNG gọi `onFilterChange()` để
+         * tải lại theo bộ lọc rỗng. Khác `resetFilterState()` ở đúng 1 điểm: đây là hành động NGƯỜI
+         * DÙNG BẤM nên phải tải lại; `resetFilterState()` là dọn ngầm khi popup đã có dữ liệu mới.
+         */
+        resetFilters() {
+            this.resetFilterState()
             this.onFilterChange()
         },
         /** TUỲ CHỌN — chỉ popup lọc client-side gọi tới. Khớp chuỗi không dấu phân biệt hoa thường. */
         applyLocalFilters(rows) {
             const kw = this.keyword.trim().toLowerCase()
             return rows.filter((row) => {
                 const okFilters = Object.keys(this.filters).every((param) => {
                     const want = this.filters[param]
                     if (want === null || want === '') return true
                     return String(row[param]) === String(want)
