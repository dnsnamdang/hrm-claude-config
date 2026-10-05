# Review package: dc57d23b1..HEAD

## Commits
00877f63f fix(report): vòng sửa 1/5 - đổi nốt id-prefix + khôi phục cuộn-về-đầu khi lật trang
f73f569b8 fix(report): nối lại chuỗi flex + căn giữa dialog + sort ngày giữ giờ:phút
74298de2e refactor(cskh): chuyển popup danh sách nhu cầu sang V2BaseReportModal + mixin
220e24444 feat(report): thêm reportDrillListMixin (sắp xếp + phân trang popup báo cáo)
b41b207cc fix(report): gỡ wrapper .report-drill-footer làm mất margin bootstrap giữa nút (vòng sửa 3/5)
4ccaf4c34 fix(report): sửa .report-drill-content/.report-drill-scroll/.report-drill-footer chết (vòng sửa 2/5)
127285043 fix(report): dời .report-drill-wrap sang style không scoped để viền/scrollbar áp đúng vào V2BaseTableScroll
eb7b3a7b2 feat(report): thêm V2BaseReportModal làm vỏ dùng chung cho popup báo cáo
7faef7daf feat(V2BaseModal): thêm slot header + prop noEnforceFocus cho popup báo cáo

## Files changed
 components/modal/V2BaseModal.vue                   |  77 +-
 components/report/V2BaseReportModal.vue            | 445 ++++++++++
 .../components/DemandListModal.vue                 | 942 ++++++---------------
 utils/mixins/reportDrillListMixin.js               | 126 +++
 4 files changed, 856 insertions(+), 734 deletions(-)

## Diff
diff --git a/components/modal/V2BaseModal.vue b/components/modal/V2BaseModal.vue
index e81eae003..5c1dcdaba 100644
--- a/components/modal/V2BaseModal.vue
+++ b/components/modal/V2BaseModal.vue
@@ -8,65 +8,71 @@
            + nút ×.
         2. Thân: vùng cuộn RIÊNG, padding sát `0.5rem` (khuôn popup "Chọn trường xuất CSV") — không
            để popup thừa khoảng trắng như các popup dựng tay trước đây.
         3. Footer: nằm NGOÀI vùng cuộn + `position: sticky` → nội dung dài mấy vẫn thấy nút.
     -->
     <b-modal
         :id="modalId"
         ref="modal"
         :size="size"
         :dialog-class="dialogClass"
+        :no-enforce-focus="noEnforceFocus"
         hide-footer
         content-class="shadow"
         body-class="v2-modal-wrap"
         @show="$emit('show')"
         @shown="$emit('shown')"
         @hide="$emit('hide', $event)"
         @hidden="$emit('hidden')"
     >
         <template #modal-header>
-            <!--
-                KHÔNG dùng `w-100` ở đây: `.modal-header` là flex row chứa khối này + nút ×; khối
-                rộng đúng 100% thì nút × không còn chỗ và bị ĐẨY RA NGOÀI mép popup (đo thật: tràn
-                26px khi dòng mô tả dài). Dùng `flex: 1 1 auto` + `min-width: 0` để khối chiếm hết
-                phần còn lại NHƯNG vẫn co được, nhờ đó `text-overflow: ellipsis` bên trong mới ăn.
-            -->
-            <div class="d-flex align-items-center v2-modal-head-left">
-                <div class="v2-modal-icon mr-2" :style="{ background: iconBackground, color: iconColor }">
-                    <i :class="icon" style="font-size: 16px"></i>
-                </div>
-                <div class="v2-modal-heading">
-                    <h5 class="modal-title mb-0" style="font-size: 14px; font-weight: 800">{{ title }}</h5>
-                    <!--
-                        Dòng mô tả bản ghi: `Khách hàng: 19TPHPVI-262 - NGUYỄN HỮU HỌC`.
-                        Chữ xám nhạt, phần giá trị đậm hơn một chút nhưng KHÔNG in đậm và
-                        TUYỆT ĐỐI không dùng màu đỏ (đỏ chỉ dành cho lỗi validate — CLAUDE.md).
-                    -->
-                    <!--
-                        Dòng mô tả CHỈ 1 DÒNG, dài quá thì cắt bằng "…" — tên bản ghi (tên thiết bị,
-                        tên hàng hóa) hay dài 2-3 dòng, để nguyên thì khối tiêu đề cao gần bằng nửa
-                        popup. Rê chuột vào hiện `title` gốc đầy đủ (Redmine #11164).
-                    -->
-                    <div
-                        v-if="subtitle"
-                        class="mt-1 v2-modal-subtitle"
-                        :title="subtitleFullText"
-                        style="font-size: 11px; color: #6b7280"
-                    >
-                        <template v-if="subtitleLabel">{{ subtitleLabel }}: </template>
-                        <span style="color: #374151">{{ subtitle }}</span>
+            <!-- Popup báo cáo thay header chuẩn bằng dải banner riêng (xem
+                 `components/report/V2BaseReportModal.vue`). Không truyền slot thì render y như cũ
+                 — 30 popup đang dùng không đổi gì. Slot tự vẽ nút đóng nên nhận luôn `close`. -->
+            <slot name="header" :close="close">
+                <!--
+                    KHÔNG dùng `w-100` ở đây: `.modal-header` là flex row chứa khối này + nút ×; khối
+                    rộng đúng 100% thì nút × không còn chỗ và bị ĐẨY RA NGOÀI mép popup (đo thật: tràn
+                    26px khi dòng mô tả dài). Dùng `flex: 1 1 auto` + `min-width: 0` để khối chiếm hết
+                    phần còn lại NHƯNG vẫn co được, nhờ đó `text-overflow: ellipsis` bên trong mới ăn.
+                -->
+                <div class="d-flex align-items-center v2-modal-head-left">
+                    <div class="v2-modal-icon mr-2" :style="{ background: iconBackground, color: iconColor }">
+                        <i :class="icon" style="font-size: 16px"></i>
+                    </div>
+                    <div class="v2-modal-heading">
+                        <h5 class="modal-title mb-0" style="font-size: 14px; font-weight: 800">{{ title }}</h5>
+                        <!--
+                            Dòng mô tả bản ghi: `Khách hàng: 19TPHPVI-262 - NGUYỄN HỮU HỌC`.
+                            Chữ xám nhạt, phần giá trị đậm hơn một chút nhưng KHÔNG in đậm và
+                            TUYỆT ĐỐI không dùng màu đỏ (đỏ chỉ dành cho lỗi validate — CLAUDE.md).
+                        -->
+                        <!--
+                            Dòng mô tả CHỈ 1 DÒNG, dài quá thì cắt bằng "…" — tên bản ghi (tên thiết bị,
+                            tên hàng hóa) hay dài 2-3 dòng, để nguyên thì khối tiêu đề cao gần bằng nửa
+                            popup. Rê chuột vào hiện `title` gốc đầy đủ (Redmine #11164).
+                        -->
+                        <div
+                            v-if="subtitle"
+                            class="mt-1 v2-modal-subtitle"
+                            :title="subtitleFullText"
+                            style="font-size: 11px; color: #6b7280"
+                        >
+                            <template v-if="subtitleLabel">{{ subtitleLabel }}: </template>
+                            <span style="color: #374151">{{ subtitle }}</span>
+                        </div>
                     </div>
                 </div>
-            </div>
-            <button type="button" class="close" @click="close">
-                <span aria-hidden="true">&times;</span>
-            </button>
+                <button type="button" class="close" @click="close">
+                    <span aria-hidden="true">&times;</span>
+                </button>
+            </slot>
         </template>
 
         <!-- CHỈ khối này cuộn. Đừng đặt lại class `modal-body` cho nội dung bên trong: nó kế thừa
              overflow + padding của bootstrap và sinh ra 2 thanh cuộn lồng nhau. -->
         <div class="v2-modal-body" :style="bodyStyle">
             <slot></slot>
         </div>
 
         <div class="modal-footer v2-modal-footer">
             <slot name="footer">
@@ -92,20 +98,23 @@ export default {
         subtitle: { type: String, default: '' },
         /** Nhãn đứng trước dòng mô tả: "Khách hàng", "Vụ việc"… */
         subtitleLabel: { type: String, default: '' },
         icon: { type: String, default: 'ri-file-list-3-line' },
         iconColor: { type: String, default: '#1abc9c' },
         iconBackground: { type: String, default: 'rgba(26, 188, 156, 0.1)' },
         size: { type: String, default: 'lg' },
         dialogClass: { type: String, default: '' },
         /** Chiều cao tối đa vùng cuộn; popup có bảng dài thì nới thêm. */
         maxBodyHeight: { type: String, default: 'calc(100vh - 220px)' },
+        /* Popup có select2/datepicker render dropdown ra ngoài `<body>`: BootstrapVue giành lại
+           focus sẽ đóng dropdown ngay khi vừa mở. Mặc định `false` — 30 popup đang dùng giữ nguyên. */
+        noEnforceFocus: { type: Boolean, default: false },
     },
     computed: {
         /** Nội dung tooltip của dòng mô tả — ghép cả nhãn để rê chuột đọc được trọn câu. */
         subtitleFullText() {
             return this.subtitleLabel ? `${this.subtitleLabel}: ${this.subtitle}` : this.subtitle
         },
         bodyStyle() {
             return { maxHeight: this.maxBodyHeight }
         },
     },
diff --git a/components/report/V2BaseReportModal.vue b/components/report/V2BaseReportModal.vue
new file mode 100644
index 000000000..3b10d44a7
--- /dev/null
+++ b/components/report/V2BaseReportModal.vue
@@ -0,0 +1,445 @@
+<!--
+    VỎ DÙNG CHUNG CHO POPUP BÁO CÁO (drill-down).
+
+    Mẫu nguồn: popup "Danh sách nhu cầu" của báo cáo CSKH tiềm năng — user chốt giữ nguyên dải
+    banner của nó làm nhận diện riêng cho popup báo cáo.
+
+    Dựng TRÊN `V2BaseModal` chứ không fork `b-modal`: chính việc fork `b-modal` làm popup báo cáo
+    lệch chuẩn ngay từ đầu, và đẻ ra bẫy stacking context (BootstrapVue bọc mỗi modal trong
+    `_BV_modal_outer_` z-index 1041 — xem `components/print/ReportPrintPreviewModal.vue`).
+
+    Component này KHÔNG biết nghiệp vụ, KHÔNG biết lấy dữ liệu, KHÔNG tự lọc/sắp/phân trang.
+    Máy client-side nằm ở `utils/mixins/reportDrillListMixin.js`.
+
+    ⚠️ Phát hiện ở Task 5 — `V2BaseModal` KHÔNG có prop `centered` (b-modal gốc của mẫu nguồn có
+    `centered`). Tự thêm class `modal-dialog-centered` vào `dialog-class` bên dưới (đúng class mà
+    prop `centered` của bootstrap-vue sinh ra) để dialog được CĂN GIỮA theo chiều dọc như bản gốc —
+    thiếu nó, `.modal-dialog` mất `min-height: calc(100% - 3.5rem)` của bootstrap, đo lệch 16px
+    chiều cao dialog so với baseline (844px -> 828px).
+-->
+<template>
+    <V2BaseModal
+        :modal-id="modalId"
+        size="xl"
+        :dialog-class="fullscreen ? `${dialogClass} report-drill-dialog--full modal-dialog-centered` : `${dialogClass} modal-dialog-centered`"
+        max-body-height="none"
+        no-enforce-focus
+        @hidden="$emit('close')"
+    >
+        <template #header="{ close }">
+            <div class="report-drill-head">
+                <div class="report-drill-head__text">
+                    <div class="report-drill-head__title">
+                        <span v-if="lead" class="report-drill-head__lead">{{ lead }}</span>
+                        <span class="report-drill-head__object">{{ title }}</span>
+                    </div>
+                    <div class="report-drill-head__sub">{{ meta }}</div>
+                </div>
+                <div class="report-drill-head__actions">
+                    <button
+                        v-if="fullscreenable"
+                        type="button"
+                        class="report-drill-head__btn"
+                        :title="fullscreen ? 'Thu nhỏ popup' : 'Phóng to toàn màn hình'"
+                        @click="toggleFullscreen"
+                    >
+                        <i :class="fullscreen ? 'ri-fullscreen-exit-line' : 'ri-fullscreen-line'"></i>
+                    </button>
+                    <button type="button" class="report-drill-head__btn" title="Đóng" @click="close()">
+                        <i class="ri-close-line"></i>
+                    </button>
+                </div>
+            </div>
+        </template>
+
+        <slot name="filters"></slot>
+        <slot name="back"></slot>
+        <slot name="summary"></slot>
+
+        <div class="report-drill-scroll">
+            <V2BaseTableScroll ref="tableScroll" :max-height="maxTableHeight" body-class="report-drill-wrap">
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
+
+        <V2BasePagination
+            v-if="!loading && totalRows"
+            class="report-drill-paging"
+            :current-page="currentPage"
+            :current-page-size="currentPageSize"
+            :total-rows="totalRows"
+            :item-label="itemLabel"
+            :page-size-options="pageSizeOptions"
+            @page-change="onPageChange"
+            @page-size-change="onPageSizeChange"
+        />
+
+        <template #footer>
+            <slot name="footer"></slot>
+        </template>
+    </V2BaseModal>
+</template>
+
+<script>
+import V2BaseModal from '@/components/modal/V2BaseModal.vue'
+import V2BaseTableScroll from '@/components/V2BaseTableScroll.vue'
+import V2BasePagination from '@/components/V2BasePagination.vue'
+
+export default {
+    name: 'V2BaseReportModal',
+    components: { V2BaseModal, V2BaseTableScroll, V2BasePagination },
+    props: {
+        visible: { type: Boolean, default: false },
+        modalId: { type: String, required: true },
+        lead: { type: String, default: '' },
+        title: { type: String, default: '' },
+        meta: { type: String, default: '' },
+        loading: { type: Boolean, default: false },
+        columns: { type: Array, default: () => [] },
+        /** Dòng của TRANG ĐANG XEM — vỏ không cắt trang, mixin/BE lo việc đó */
+        rows: { type: Array, default: () => [] },
+        rowKey: { type: String, default: 'id' },
+        startIndex: { type: Number, default: 0 },
+        emptyText: { type: String, default: 'Không có dữ liệu khớp bộ lọc.' },
+        sort: { type: Object, default: () => ({ key: '', dir: 'asc' }) },
+        currentPage: { type: Number, default: 1 },
+        currentPageSize: { type: Number, default: 20 },
+        totalRows: { type: Number, default: 0 },
+        itemLabel: { type: String, default: 'bản ghi' },
+        pageSizeOptions: { type: Array, default: () => [20, 50, 100] },
+        fullscreenable: { type: Boolean, default: true },
+        maxTableHeight: { type: String, default: '50vh' },
+        dialogClass: { type: String, default: 'report-drill-dialog' },
+    },
+    data() {
+        return { fullscreen: false }
+    },
+    watch: {
+        /* Mở lượt MỚI thì trả popup về kích thước thường. Giữ nguyên là lượt sau mang kích thước
+           của lượt trước — đúng lỗi ca e2e 17 canh. */
+        visible(value) {
+            if (value) this.fullscreen = false
+            this.$nextTick(() => this.syncBvModal(value))
+        },
+    },
+    mounted() {
+        this.syncBvModal(this.visible)
+    },
+    methods: {
+        syncBvModal(value) {
+            if (value) this.$bvModal.show(this.modalId)
+            else this.$bvModal.hide(this.modalId)
+        },
+        toggleFullscreen() {
+            this.fullscreen = !this.fullscreen
+            this.$emit('toggle-fullscreen', this.fullscreen)
+        },
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
+        sortIcon(key) {
+            if (this.sort.key !== key) return 'ri-arrow-up-down-line'
+            return this.sort.dir === 'asc' ? 'ri-arrow-up-line' : 'ri-arrow-down-line'
+        },
+    },
+}
+</script>
+
+<style lang="scss">
+/* KHÔNG `scoped`: `b-modal` render dialog ra ngoài cây component nên style scoped không với tới.
+   Toàn bộ giá trị dưới đây port từ `.care-drill-*` của mẫu nguồn (`DemandListModal.vue` dòng
+   846–909) — đổi tên tiền tố, giữ nguyên số. */
+.report-drill-dialog { max-width: 1400px; }
+.report-drill-dialog--full { width: 100vw; max-width: 100vw; margin: 0; min-height: 100vh; }
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
+    height: 92vh;
+    display: flex;
+    flex-direction: column;
+    overflow: hidden;
+}
+.report-drill-dialog .modal-header {
+    padding: 0;
+    border: 0;
+    flex-shrink: 0;
+}
+.report-drill-dialog .modal-body {
+    padding: 16px;
+    flex: 1 1 auto;
+    min-height: 0;
+    overflow: hidden;
+    display: flex;
+    flex-direction: column;
+}
+/* ⚠️ Phát hiện ở Task 5 (đo thật khi gắn popup thứ NHẤT vào vỏ này) — `V2BaseModal` render THÊM
+   một lớp bọc RIÊNG bên trong `.modal-body` (`<div class="v2-modal-body">`, xem
+   `components/modal/V2BaseModal.vue`), và lớp đó KHÔNG phải flex item/flex container: mặc định
+   `display: block`. Chuỗi `flex: 1 1 auto` mà các khối con (`.report-drill-scroll`, rồi
+   `.report-drill-wrap`) khai để "chiếm hết chỗ còn lại" chỉ có tác dụng khi CHA TRỰC TIẾP của
+   chúng là flex — thiếu mắt xích này, `.v2-modal-body` cao đúng bằng NỘI DUNG THẬT (đo được:
+   bảng 20 dòng cao 1150px không bị cắt), đẩy `.report-drill-scroll`/`.report-drill-wrap` tràn
+   xuống dưới cả khung popup (đáy đo được ở y=1366 trong khi khung popup chỉ cao 828px) và biến
+   `.v2-modal-body` (vốn có sẵn `overflow-y: auto`) thành vùng cuộn DUY NHẤT — cuộn xuống là bộ
+   lọc/phân trang trôi theo luôn, khác hẳn bản gốc (chỉ bảng cuộn, lọc + phân trang đứng yên).
+   Ghi đè CHỈ trong phạm vi `.report-drill-dialog` (không đụng 30 popup khác đang dùng
+   `V2BaseModal` với `max-body-height` mặc định — chúng tự giới hạn chiều cao bằng `max-height`
+   khai TRỰC TIẾP qua inline style nên không cần đường flex này). */
+.report-drill-dialog .v2-modal-body {
+    display: flex;
+    flex-direction: column;
+    flex: 1 1 auto;
+    min-height: 0;
+    /* Chỉ `.report-drill-wrap` (bảng) mới cuộn — khớp `.care-drill-content .modal-body` bản gốc */
+    overflow: hidden;
+    padding: 0;
+}
+.report-drill-scroll {
+    flex: 1 1 auto;
+    min-height: 120px;
+    display: flex;
+    flex-direction: column;
+}
+/* Cùng lý do trên: gốc của `V2BaseTableScroll` (`.v2-table-scroll`) cũng là `display: block` —
+   thiếu mắt xích flex cuối để `.report-drill-wrap` (khai `flex: 1 1 auto` ở khối dưới) thật sự
+   chiếm hết phần cao còn lại. Scope theo `.report-drill-scroll` nên KHÔNG đụng các nơi khác đang
+   dùng `V2BaseTableScroll` (chúng tự giới hạn bằng prop `max-height`, không cần đường flex này). */
+.report-drill-scroll .v2-table-scroll {
+    display: flex;
+    flex-direction: column;
+    flex: 1 1 auto;
+    min-height: 0;
+}
+/* ⚠️ Vòng sửa 3/5 — ĐÃ GỠ `.report-drill-footer` (từng bọc `<slot name="footer">` ở vòng sửa 2/5).
+   `V2BaseModal` render sẵn `.modal-footer` bao ngoài slot; bootstrap 4.6 có rule
+   `.modal-footer > * { margin: 0.25rem }` CHỈ áp cho CON TRỰC TIẾP. Bọc thêm 1 div làm các nút
+   thật (do Task 5 đặt vào slot) rơi xuống thành cháu, mất hẳn margin 4px mỗi bên → hàng nút dính
+   sát nhau. `.report-drill-footer` không tự nó tạo `gap`, nên hướng đúng là GỠ wrapper, không phải
+   đắp thêm `display:flex; gap` — 2 popup khác dựng trên `V2BaseModal` (`ProjectListModal.vue`,
+   `DevelopmentDrillModal.vue`) đều đặt nút thẳng vào slot `#footer`, không bọc gì, và margin mặc
+   định của bootstrap đã cho đúng 8px giữa 2 nút. Đo thật (vòng sửa 3/5): khoảng cách ngang giữa 2
+   nút footer = 8px (xem báo cáo). */
+.report-drill-paging {
+    flex-shrink: 0;
+}
+.report-drill-dialog--full .modal-content {
+    height: 100vh;
+    max-height: 100vh;
+    border-radius: 0;
+}
+
+/* `.report-drill-wrap` gắn vào bảng qua `body-class` của `V2BaseTableScroll` (component con) —
+   PHẢI để ở khối KHÔNG scoped như trên, lý do y hệt: phần tử đó nằm trong template RIÊNG của
+   component con (div `ref="body"`), không phải slot content của `V2BaseReportModal`, nên selector
+   scoped của ta không với tới (đo thật vòng sửa 1/5: để ở khối scoped ra `border-top-width: 0px`,
+   `border-radius: 0px` — viền và bo góc biến mất hoàn toàn dù class có đúng tên). Giá trị port từ
+   `.care-drill-wrap` của `DemandListModal.vue` dòng 1162–1190, giữ nguyên số. */
+.report-drill-wrap {
+    flex: 1 1 auto;
+    min-height: 0;
+    overflow: auto;
+    border: 1px solid #e3e8ef;
+    border-radius: 6px;
+}
+.report-drill-wrap::-webkit-scrollbar {
+    width: 6px;
+    height: 6px;
+}
+.report-drill-wrap::-webkit-scrollbar-track {
+    background: #f1f5f9;
+}
+.report-drill-wrap::-webkit-scrollbar-thumb {
+    background: #cbd5e1;
+    border-radius: 3px;
+}
+.report-drill-wrap::-webkit-scrollbar-thumb:hover {
+    background: #94a3b8;
+}
+</style>
+
+<style lang="scss" scoped>
+/* Giá trị dưới đây port từ mockup đã duyệt (qua `.care-drill-*` của `DemandListModal.vue` dòng
+   910 → hết file) — không tự đặt lại palette. Chỉ lấy các lớp của VỎ: đầu popup, khung bảng +
+   thanh cuộn, tiêu đề cột sắp xếp được. Style riêng của màn (filters/summary/back/...) ở lại
+   `DemandListModal.vue` (Task 5). */
+$navy-start: #0a1c3d;
+$teal: #06b6d4;
+$text-muted: #6b7280;
+
+.report-drill-head {
+    display: flex;
+    align-items: center;
+    justify-content: space-between;
+    gap: 10px;
+    width: 100%;
+    padding: 14px 16px;
+    background: linear-gradient(135deg, $navy-start, $teal);
+    color: #fff;
+}
+.report-drill-head__text {
+    min-width: 0;
+    flex: 1 1 auto;
+}
+.report-drill-head__title {
+    font-size: 15px;
+    line-height: 1.35;
+    overflow: hidden;
+    text-overflow: ellipsis;
+    white-space: nowrap;
+}
+/* Phần dẫn nhập mờ đi để TÊN ĐỐI TƯỢNG đang xem nổi hẳn lên */
+.report-drill-head__lead {
+    font-weight: 500;
+    color: rgba(255, 255, 255, 0.72);
+}
+.report-drill-head__object {
+    font-weight: 800;
+    color: #fff;
+}
+.report-drill-head__sub {
+    margin-top: 2px;
+    font-size: 11.5px;
+    font-weight: 500;
+    color: rgba(255, 255, 255, 0.85);
+}
+.report-drill-head__actions {
+    display: flex;
+    align-items: center;
+    gap: 6px;
+    flex-shrink: 0;
+}
+.report-drill-head__btn {
+    display: flex;
+    align-items: center;
+    justify-content: center;
+    width: 28px;
+    height: 28px;
+    border: none;
+    border-radius: 50%;
+    background: rgba(255, 255, 255, 0.15);
+    color: #fff;
+    cursor: pointer;
+
+    &:hover {
+        background: rgba(255, 255, 255, 0.3);
+    }
+}
+
+/* `.report-drill-wrap` (viền/bo góc/scrollbar mảnh) chuyển sang khối KHÔNG scoped phía trên —
+   xem comment ở đó. Thanh cuộn PHÍA TRÊN nay do `V2BaseTableScroll` tự vẽ bằng class riêng
+   (`.v2-table-scroll__top scrollbar-thin`), không còn `.report-drill-topscroll` trong file này. */
+
+.report-drill-table {
+    width: 100%;
+    /* `auto` + `nowrap`: cột tự nới theo nội dung dài nhất, bảng tràn ngang thì cuộn —
+       không bẻ chữ xuống dòng nữa. Width khai ở <th> nay là mức TỐI THIỂU. */
+    table-layout: auto;
+    border-collapse: collapse;
+    font-size: 12px;
+    background: #fff;
+
+    th,
+    td {
+        padding: 7px 9px;
+        border: 1px solid #d6dde6;
+        vertical-align: middle;
+        white-space: nowrap;
+    }
+
+    thead th {
+        position: sticky;
+        top: 0;
+        z-index: 3;
+        background: linear-gradient(180deg, #f3fdfe, #e2f6f9);
+        border-bottom: 2px solid #20d9ea;
+        color: #0a7c88;
+        font-size: 11px;
+        font-weight: 700;
+        text-transform: none;
+        letter-spacing: 0;
+        text-align: left;
+        white-space: nowrap;
+    }
+
+    tbody tr:hover td {
+        background: #ddf0f7;
+    }
+}
+.report-drill-table__center {
+    text-align: center;
+}
+.report-drill-table__empty {
+    padding: 22px;
+    text-align: center;
+    color: $text-muted;
+}
+
+/* Tiêu đề cột bấm được để sắp xếp — copy khuôn `.sortable-header` của V2BaseDataTable */
+.report-drill-sort {
+    display: inline-flex;
+    align-items: center;
+    cursor: pointer;
+    user-select: none;
+
+    i {
+        margin-left: 4px;
+        font-size: 12px;
+        color: #9ca3af;
+    }
+
+    &:hover i {
+        color: #0e7490;
+    }
+}
+</style>
diff --git a/pages/assign/report/potential-customer-care/components/DemandListModal.vue b/pages/assign/report/potential-customer-care/components/DemandListModal.vue
index 9b4530a9b..92fa186f2 100644
--- a/pages/assign/report/potential-customer-care/components/DemandListModal.vue
+++ b/pages/assign/report/potential-customer-care/components/DemandListModal.vue
@@ -1,305 +1,254 @@
 <!--
     Popup danh sách nhu cầu chi tiết — mở khi bấm bất kỳ con số nào trên màn báo cáo.
 
-    Style + bố cục port từ mockup đã duyệt (khối `.minutes-modal--wide` / `.drill-*`):
-    header gradient navy→teal (tiêu đề + dòng tóm tắt + nút đóng tròn) → BỘ LỌC → KHỐI KPI →
-    "Phân bổ nhu cầu theo cơ cấu" → BẢNG CHI TIẾT → footer.
+    Dựng TRÊN `components/report/V2BaseReportModal.vue` (vỏ dùng chung cho popup báo cáo) +
+    `utils/mixins/reportDrillListMixin.js` (máy sắp xếp + phân trang tại chỗ). Component này chỉ
+    còn giữ phần NGHIỆP VỤ RIÊNG của popup CSKH tiềm năng: bộ lọc, khối KPI/phân bổ theo cơ cấu,
+    thứ tự + nội dung cột, và các ô bảng cần hiển thị đặc biệt (khách hàng, meeting, dự án…).
+    Khung popup, dải banner đầu, bảng + thanh cuộn, phân trang đều do vỏ lo — style + bố cục
+    port từ mockup đã duyệt (khối `.minutes-modal--wide` / `.drill-*`).
 
     3 quy tắc nghiệp vụ của mockup được giữ nguyên:
       1. Cơ cấu ĐANG XEM bị loại khỏi khối phân bổ (BE tự làm) và ô lọc của nó cũng ẩn đi —
          đang xem theo lĩnh vực thì không lọc lại lĩnh vực nữa.
       2. Thứ tự cột bám ĐÚNG thứ tự hàng trong khối phân bổ: cơ cấu nào hiện trước thì cột của
          cơ cấu đó đứng trước, ngay sau STT và TRƯỚC cả cột Khách hàng.
       3. Popup nhóm "không tiếp tục" bỏ hẳn khối KPI (BE trả mảng rỗng) vì luôn 0%/0%/100%.
 
-    `no-enforce-focus`: panel chi tiết meeting mở ĐÈ lên popup này, focus-trap mặc định của
-    `b-modal` sẽ kéo focus ngược về modal làm không thao tác được trong panel.
+    Bộ lọc của popup này chạy Ở SERVER (khác `DevelopmentDrillModal` lọc client-side): chọn ô lọc
+    chỉ đổi `filters`/`keyword` tại chỗ rồi `$emit('filter', …)`, màn cha ghép điều kiện và tải lại
+    `rows`/`total` từ API — component KHÔNG tự cắt danh sách theo bộ lọc.
 
-    Khuôn kỹ thuật vẫn là `b-modal` như `ProspectiveListModal.vue` (khuôn thật đang chạy trong
-    repo); `components/modal/V2BaseModal.vue` mà CLAUDE.md nhắc tới không tồn tại trên nhánh này.
+    `max-table-height=""`: mặc định của vỏ là `'50vh'` (cap cứng); popup này bám flex-fill như bản
+    gốc (bảng chiếm hết phần còn lại của popup, cao thấp tuỳ có mở khối tổng hợp hay không). `""` là
+    falsy nên `V2BaseTableScroll` không gắn `max-height` inline — TUYỆT ĐỐI đừng đổi thành số `0`
+    (prop khai `type: String`, số báo lỗi type) hay chuỗi `"0"` (chuỗi khác rỗng nên KHÔNG falsy, ra
+    `max-height: 0` làm bảng cao bằng 0).
 -->
 <template>
-    <b-modal
-        id="care-demand-list-modal"
+    <V2BaseReportModal
+        modal-id="care-demand-list-modal"
         :visible="visible"
-        hide-footer
-        centered
-        size="xl"
-        :dialog-class="fullscreen ? 'care-drill-dialog care-drill-dialog--full' : 'care-drill-dialog'"
-        content-class="care-drill-content"
-        no-enforce-focus
-        @hidden="$emit('close')"
+        :loading="loading"
+        lead="Bạn đang xem kết quả CSKH tiềm năng:"
+        :title="title"
+        :meta="metaText"
+        :columns="columns"
+        :rows="pagedRows"
+        :start-index="pageOffset"
+        :sort="sort"
+        :current-page="safePage"
+        :current-page-size="pageSize"
+        :total-rows="sortedRows.length"
+        item-label="nhu cầu"
+        empty-text="Không có nhu cầu nào khớp bộ lọc."
+        max-table-height=""
+        @sort="({ key }) => toggleSort(key)"
+        @page-change="onPageChange"
+        @page-size-change="onPageSizeChange"
+        @close="$emit('close')"
     >
-        <template #modal-header="{ close }">
-            <div class="care-drill-head">
-                <div class="care-drill-head__text">
-                    <div class="care-drill-head__title">
-                        <span class="care-drill-head__lead">Bạn đang xem kết quả CSKH tiềm năng:</span>
-                        <span class="care-drill-head__object">{{ title }}</span>
-                    </div>
-                    <div class="care-drill-head__sub">
-                        <template v-if="loading">Đang tải… · Kỳ {{ periodText }}</template>
-                        <template v-else>
-                            {{ rows.length }} nhu cầu · {{ money(totalAmount) }} đ · Kỳ {{ periodText }}
-                            <span v-if="isFiltered"> · đang lọc trong {{ total }} nhu cầu</span>
-                        </template>
-                    </div>
+        <!-- Bộ lọc riêng: đặt TĨNH trong thân popup nên gõ tìm kiếm không mất con trỏ -->
+        <template #filters>
+            <div class="report-drill-filters">
+                <div class="report-drill-filters__item report-drill-filters__item--search">
+                    <V2BaseInput
+                        v-model="keyword"
+                        size="sm"
+                        placeholder="Tìm khách hàng / meeting..."
+                        @input="onFilterChange"
+                    />
+                </div>
+                <div v-for="field in filterFields" :key="field.param" class="report-drill-filters__item">
+                    <V2BaseSelectInModal
+                        v-model="filters[field.param]"
+                        :options="field.options"
+                        :allowClear="true"
+                        size="sm"
+                        :placeholder="field.placeholder"
+                        @change="onSelectChange(field.param)"
+                    />
+                </div>
+
+                <!-- Xoá lọc nằm NGAY SAU ô lọc cuối, không tách thành dòng riêng: hàng lọc gói sang
+                     dòng 2 vốn còn thừa chỗ, để nút một mình một dòng là phí hẳn một dòng của popup. -->
+                <div class="report-drill-filters__item report-drill-filters__item--action">
+                    <V2BaseIconButton title="Xoá lọc" @click="resetFilters">
+                        <i class="ri-refresh-line"></i>
+                    </V2BaseIconButton>
                 </div>
-                <div class="care-drill-head__actions">
+
+                <div class="report-drill-filters__meta">
+                    <!-- Thu gọn khối tổng hợp (KPI + phân bổ) — cùng kiểu nút với dải tổng hợp ngoài
+                         màn báo cáo, để popup nhường chỗ cho bảng chi tiết khi màn hình thấp. -->
                     <button
+                        v-if="hasSummary"
                         type="button"
-                        class="care-drill-head__btn"
-                        :title="fullscreen ? 'Thu nhỏ popup' : 'Phóng to toàn màn hình'"
-                        @click="fullscreen = !fullscreen"
+                        class="rsum-toggle report-drill-toggle"
+                        :class="{ 'rsum-toggle--collapsed': summaryCollapsed }"
+                        @click="summaryCollapsed = !summaryCollapsed"
                     >
-                        <i :class="fullscreen ? 'ri-fullscreen-exit-line' : 'ri-fullscreen-line'"></i>
-                    </button>
-                    <button type="button" class="care-drill-head__btn" title="Đóng" @click="close()">
-                        <i class="ri-close-line"></i>
+                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
+                            <polyline points="6 9 12 15 18 9"></polyline>
+                        </svg>
+                        {{ summaryCollapsed ? 'Mở rộng' : 'Thu gọn' }}
                     </button>
+
+                    <span v-if="!loading" class="report-drill-count">{{ rows.length }} / {{ total }} nhu cầu</span>
                 </div>
             </div>
         </template>
 
-        <!-- Bộ lọc riêng: đặt TĨNH trong thân popup nên gõ tìm kiếm không mất con trỏ -->
-        <div class="care-drill-filters">
-            <div class="care-drill-filters__item care-drill-filters__item--search">
-                <V2BaseInput
-                    v-model="keyword"
-                    size="sm"
-                    placeholder="Tìm khách hàng / meeting..."
-                    @input="onFilterChange"
-                />
-            </div>
-            <div v-for="field in filterFields" :key="field.param" class="care-drill-filters__item">
-                <V2BaseSelectInModal
-                    v-model="filters[field.param]"
-                    :options="field.options"
-                    :allowClear="true"
-                    size="sm"
-                    :placeholder="field.placeholder"
-                    @change="onSelectChange(field.param)"
-                />
-            </div>
-
-            <!-- Xoá lọc nằm NGAY SAU ô lọc cuối, không tách thành dòng riêng: hàng lọc gói sang
-                 dòng 2 vốn còn thừa chỗ, để nút một mình một dòng là phí hẳn một dòng của popup. -->
-            <div class="care-drill-filters__item care-drill-filters__item--action">
-                <V2BaseIconButton title="Xoá lọc" @click="clearFilters">
-                    <i class="ri-refresh-line"></i>
-                </V2BaseIconButton>
-            </div>
-
-            <div class="care-drill-filters__meta">
-                <!-- Thu gọn khối tổng hợp (KPI + phân bổ) — cùng kiểu nút với dải tổng hợp ngoài
-                     màn báo cáo, để popup nhường chỗ cho bảng chi tiết khi màn hình thấp. -->
-                <button
-                    v-if="hasSummary"
-                    type="button"
-                    class="rsum-toggle care-drill-toggle"
-                    :class="{ 'rsum-toggle--collapsed': summaryCollapsed }"
-                    @click="summaryCollapsed = !summaryCollapsed"
-                >
-                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
-                        <polyline points="6 9 12 15 18 9"></polyline>
-                    </svg>
-                    {{ summaryCollapsed ? 'Mở rộng' : 'Thu gọn' }}
-                </button>
-
-                <span v-if="!loading" class="care-drill-count">{{ rows.length }} / {{ total }} nhu cầu</span>
-            </div>
-        </div>
-
         <!-- Đang lọc sâu từ 1 hộp KPI: khối KPI nói về tập CHA nên bỏ đi, thay bằng lối quay lại -->
-        <div v-if="backTo" class="care-drill-back">
-            <V2BaseButton tertiary size="sm" @click="goBack">
-                <template #prefix><i class="ri-arrow-left-line" style="font-size: 14px"></i></template>
-                Quay lại
-            </V2BaseButton>
-            <span class="care-drill-back__from">Đang xem sâu trong: {{ backTo.title }}</span>
-        </div>
-
-        <!-- Khối KPI: dùng lại đúng component của màn chính, bản thu nhỏ -->
-        <KpiBoxes
-            v-if="!backTo && kpis.length && !summaryCollapsed"
-            :kpis="kpis"
-            compact
-            :show-title="false"
-            id-prefix="care-drill"
-            class="mb-2"
-            @drill="onKpiDrill"
-        />
+        <template #back>
+            <div v-if="backTo" class="report-drill-back">
+                <V2BaseButton tertiary size="sm" @click="goBack">
+                    <template #prefix><i class="ri-arrow-left-line" style="font-size: 14px"></i></template>
+                    Quay lại
+                </V2BaseButton>
+                <span class="report-drill-back__from">Đang xem sâu trong: {{ backTo.title }}</span>
+            </div>
+        </template>
 
-        <div v-if="crossStats.length && !summaryCollapsed" class="care-drill-sumbox">
-            <p class="care-drill-sumbox__title">Phân bổ nhu cầu theo cơ cấu</p>
-            <!-- MỘT container cuộn ngang chung cho cả 3 cơ cấu (mockup): các hàng thẳng cột với
-                 nhau và chỉ có 1 thanh cuộn, thay vì mỗi hàng một thanh riêng. -->
-            <div class="care-drill-sum">
-                <div v-for="stat in crossStats" :key="stat.key" class="care-drill-sum__grp">
-                    <span class="care-drill-sum__label">{{ stat.label }}</span>
-                    <div class="care-drill-sum__chips">
-                        <button
-                            v-for="item in stat.items"
-                            :key="`${stat.key}-${item.id}`"
-                            type="button"
-                            class="care-drill-sum__chip"
-                            :class="{ 'care-drill-sum__chip--on': isChipActive(stat.key, item.id) }"
-                            :title="`${money(item.amount)} đ`"
-                            @click="toggleChip(stat.key, item.id)"
-                        >
-                            {{ item.label }}
-                            <span class="care-drill-sum__chip__n">{{ item.count }}</span>
-                            <span class="care-drill-sum__chip__pct">{{ item.percent }}%</span>
-                        </button>
+        <template #summary>
+            <!-- Khối KPI: dùng lại đúng component của màn chính, bản thu nhỏ -->
+            <KpiBoxes
+                v-if="!backTo && kpis.length && !summaryCollapsed"
+                :kpis="kpis"
+                compact
+                :show-title="false"
+                id-prefix="report-drill"
+                class="mb-2"
+                @drill="onKpiDrill"
+            />
+
+            <div v-if="crossStats.length && !summaryCollapsed" class="report-drill-sumbox">
+                <p class="report-drill-sumbox__title">Phân bổ nhu cầu theo cơ cấu</p>
+                <!-- MỘT container cuộn ngang chung cho cả 3 cơ cấu (mockup): các hàng thẳng cột với
+                     nhau và chỉ có 1 thanh cuộn, thay vì mỗi hàng một thanh riêng. -->
+                <div class="report-drill-sum">
+                    <div v-for="stat in crossStats" :key="stat.key" class="report-drill-sum__grp">
+                        <span class="report-drill-sum__label">{{ stat.label }}</span>
+                        <div class="report-drill-sum__chips">
+                            <button
+                                v-for="item in stat.items"
+                                :key="`${stat.key}-${item.id}`"
+                                type="button"
+                                class="report-drill-sum__chip"
+                                :class="{ 'report-drill-sum__chip--on': isChipActive(stat.key, item.id) }"
+                                :title="`${money(item.amount)} đ`"
+                                @click="toggleChip(stat.key, item.id)"
+                            >
+                                {{ item.label }}
+                                <span class="report-drill-sum__chip__n">{{ item.count }}</span>
+                                <span class="report-drill-sum__chip__pct">{{ item.percent }}%</span>
+                            </button>
+                        </div>
                     </div>
                 </div>
             </div>
-        </div>
+        </template>
 
-        <div class="care-drill-scroll">
-            <!-- Thanh cuộn ngang phía TRÊN bảng, đồng bộ với thanh dưới (xem CareTrackingTable.vue) -->
-            <div v-show="overflowing" ref="topScroll" class="care-drill-topscroll">
-                <div :style="{ width: scrollWidth + 'px', height: '1px' }"></div>
-            </div>
-            <div ref="bodyScroll" class="care-drill-wrap">
-                <table ref="tableEl" class="care-drill-table">
-                    <thead>
-                        <tr>
-                            <th style="min-width: 46px">STT</th>
-                            <th v-for="col in columns" :key="col.key" :style="{ minWidth: col.width }">
-                                <span v-if="col.sortable" class="care-drill-sort" @click="toggleSort(col.key)">
-                                    {{ col.label }}
-                                    <i :class="sortIcon(col.key)"></i>
-                                </span>
-                                <span v-else>{{ col.label }}</span>
-                            </th>
-                        </tr>
-                    </thead>
-                    <tbody>
-                        <tr v-for="(row, index) in pagedRows" :key="row.id">
-                            <td class="care-drill-table__center">{{ pageOffset + index + 1 }}</td>
-                            <td v-for="col in columns" :key="col.key" :class="col.cellClass">
-                                <template v-if="col.key === 'customer'">
-                                    <!-- Tên KH giữ chữ THƯỜNG (không biến thành link, dễ tưởng mở
-                                         hồ sơ khách hàng); lịch sử meeting đi qua icon riêng. -->
-                                    <span class="care-drill-customer">
-                                        <span class="care-drill-customer__name">{{ row.customer_name }}</span>
-                                        <V2BaseIconButton
-                                            v-if="row.customer_id"
-                                            size="xs"
-                                            title="Lịch sử meeting với khách hàng"
-                                            @click="$emit('open-customer-history', row)"
-                                        >
-                                            <i class="ri-history-line"></i>
-                                        </V2BaseIconButton>
-                                    </span>
-                                    <div v-if="row.customer_code" class="care-drill-sub">{{ row.customer_code }}</div>
-                                </template>
-                                <template v-else-if="col.key === 'market'">
-                                    {{ row.province_name }}
-                                    <div class="care-drill-sub">{{ row.ward_name }}</div>
-                                </template>
-                                <template v-else-if="col.key === 'amount'">{{ money(row.expected_amount) }}</template>
-                                <template v-else-if="col.key === 'start'">{{ monthYear(row.expected_start_date) }}</template>
-                                <template v-else-if="col.key === 'repair'">{{ row.has_maintenance_demand ? 'Có' : 'Không' }}</template>
-                                <template v-else-if="col.key === 'meeting'">
-                                    <!-- Mockup: tên meeting bấm được để mở panel chi tiết; dòng dưới ghi
-                                         ngày họp, nhu cầu mang sang từ kỳ trước thì gắn nhãn "Kỳ trước" -->
-                                    <a
-                                        v-if="row.meeting_id"
-                                        href="#"
-                                        class="care-drill-link care-drill-meeting"
-                                        title="Xem chi tiết meeting"
-                                        @click.prevent="$emit('open-meeting', row)"
-                                    >{{ row.meeting_name }}</a>
-                                    <span v-else>{{ row.meeting_name }}</span>
-                                    <div class="care-drill-sub">
-                                        {{ row.meeting_code }} · Họp {{ row.meeting_start_date }}
-                                        <span v-if="row.is_carried" class="care-drill-carry">Kỳ trước</span>
-                                    </div>
-                                </template>
-                                <template v-else-if="col.key === 'status'">
-                                    <V2BaseBadge :color="row.status_color">{{ row.status_text }}</V2BaseBadge>
-                                    <div v-if="row.closed_at" class="care-drill-sub">Đóng {{ row.closed_at }}</div>
-                                </template>
-                                <template v-else-if="col.key === 'project'">
-                                    <!-- Đã có dự án -> mã bấm được, mở màn chi tiết dự án ở tab mới -->
-                                    <a
-                                        v-if="row.prospective_project_id"
-                                        href="#"
-                                        class="care-drill-link care-drill-project"
-                                        :title="`Xem dự án ${row.prospective_project_code}`"
-                                        @click.prevent="$emit('open-project', row)"
-                                    >{{ row.prospective_project_code }}</a>
-                                    <span v-else-if="row.prospective_project_code">{{ row.prospective_project_code }}</span>
-                                    <!-- Chưa có dự án: điều hướng sang màn tạo dự án TKT, KHÔNG tạo tại chỗ
-                                         (form dự án có quá nhiều trường bắt buộc để nhét vào popup) -->
-                                    <V2BaseButton
-                                        v-else-if="canCreateProject && row.status === 1"
-                                        primary
-                                        size="sm"
-                                        @click="$emit('create-project', row)"
-                                    >
-                                        <template #prefix><i class="ri-add-line" style="font-size: 13px"></i></template>
-                                        Tạo mới
-                                    </V2BaseButton>
-                                    <span v-else>—</span>
-                                </template>
-                                <template v-else>{{ row[col.field] }}</template>
-                            </td>
-                        </tr>
-                        <tr v-if="!pagedRows.length">
-                            <td :colspan="columns.length + 1" class="care-drill-table__empty">
-                                {{ loading ? 'Đang tải…' : 'Không có nhu cầu nào khớp bộ lọc.' }}
-                            </td>
-                        </tr>
-                    </tbody>
-                </table>
+        <!-- Ô đặc biệt: bê nguyên nội dung từng cột cần hiển thị khác `row[col.field]` mặc định.
+             3 cột amount/start/repair chỉ là biểu thức 1 dòng nhưng vẫn đi qua slot cho thống nhất. -->
+        <template #cell-customer="{ row }">
+            <!-- Tên KH giữ chữ THƯỜNG (không biến thành link, dễ tưởng mở hồ sơ khách hàng); lịch sử
+                 meeting đi qua icon riêng. -->
+            <span class="report-drill-customer">
+                <span class="report-drill-customer__name">{{ row.customer_name }}</span>
+                <V2BaseIconButton
+                    v-if="row.customer_id"
+                    size="xs"
+                    title="Lịch sử meeting với khách hàng"
+                    @click="$emit('open-customer-history', row)"
+                >
+                    <i class="ri-history-line"></i>
+                </V2BaseIconButton>
+            </span>
+            <div v-if="row.customer_code" class="report-drill-sub">{{ row.customer_code }}</div>
+        </template>
+        <template #cell-market="{ row }">
+            {{ row.province_name }}
+            <div class="report-drill-sub">{{ row.ward_name }}</div>
+        </template>
+        <template #cell-meeting="{ row }">
+            <!-- Mockup: tên meeting bấm được để mở panel chi tiết; dòng dưới ghi ngày họp, nhu cầu
+                 mang sang từ kỳ trước thì gắn nhãn "Kỳ trước" -->
+            <a
+                v-if="row.meeting_id"
+                href="#"
+                class="report-drill-link report-drill-meeting"
+                title="Xem chi tiết meeting"
+                @click.prevent="$emit('open-meeting', row)"
+            >{{ row.meeting_name }}</a>
+            <span v-else>{{ row.meeting_name }}</span>
+            <div class="report-drill-sub">
+                {{ row.meeting_code }} · Họp {{ row.meeting_start_date }}
+                <span v-if="row.is_carried" class="report-drill-carry">Kỳ trước</span>
             </div>
-        </div>
-
-        <V2BasePagination
-            v-if="!loading"
-            class="care-drill-paging"
-            :current-page="safePage"
-            :current-page-size="pageSize"
-            :total-rows="sortedRows.length"
-            item-label="nhu cầu"
-            :page-size-options="[20, 50, 100]"
-            @page-change="onPageChange"
-            @page-size-change="onPageSizeChange"
-        />
+        </template>
+        <template #cell-status="{ row }">
+            <V2BaseBadge :color="row.status_color">{{ row.status_text }}</V2BaseBadge>
+            <div v-if="row.closed_at" class="report-drill-sub">Đóng {{ row.closed_at }}</div>
+        </template>
+        <template #cell-project="{ row }">
+            <!-- Đã có dự án -> mã bấm được, mở màn chi tiết dự án ở tab mới -->
+            <a
+                v-if="row.prospective_project_id"
+                href="#"
+                class="report-drill-link report-drill-project"
+                :title="`Xem dự án ${row.prospective_project_code}`"
+                @click.prevent="$emit('open-project', row)"
+            >{{ row.prospective_project_code }}</a>
+            <span v-else-if="row.prospective_project_code">{{ row.prospective_project_code }}</span>
+            <!-- Chưa có dự án: điều hướng sang màn tạo dự án TKT, KHÔNG tạo tại chỗ (form dự án có
+                 quá nhiều trường bắt buộc để nhét vào popup) -->
+            <V2BaseButton
+                v-else-if="canCreateProject && row.status === 1"
+                primary
+                size="sm"
+                @click="$emit('create-project', row)"
+            >
+                <template #prefix><i class="ri-add-line" style="font-size: 13px"></i></template>
+                Tạo mới
+            </V2BaseButton>
+            <span v-else>—</span>
+        </template>
+        <template #cell-amount="{ row }">{{ money(row.expected_amount) }}</template>
+        <template #cell-start="{ row }">{{ monthYear(row.expected_start_date) }}</template>
+        <template #cell-repair="{ row }">{{ row.has_maintenance_demand ? 'Có' : 'Không' }}</template>
 
-        <div class="care-drill-footer">
+        <template #footer>
             <V2BaseButton tertiary size="sm" @click="$emit('close')">Đóng</V2BaseButton>
             <!-- Popup KHÔNG tự gọi API: bộ lọc gốc của báo cáo nằm ở màn cha, cha ghép rồi tải -->
             <V2BaseButton secondary size="sm" @click="$emit('print')">
                 <template #prefix><i class="ri-printer-line" style="font-size: 14px"></i></template>
                 In danh sách
             </V2BaseButton>
             <V2BaseButton primary size="sm" @click="$emit('export')">
                 <template #prefix><i class="ri-download-line" style="font-size: 14px"></i></template>
                 Xuất Excel danh sách
             </V2BaseButton>
-        </div>
-    </b-modal>
+        </template>
+    </V2BaseReportModal>
 </template>
 
 <script>
+import V2BaseReportModal from '@/components/report/V2BaseReportModal.vue'
 import V2BaseInput from '@/components/V2BaseInput.vue'
-import V2BasePagination from '@/components/V2BasePagination.vue'
 import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
 import V2BaseButton from '@/components/V2BaseButton.vue'
 import V2BaseIconButton from '@/components/V2BaseIconButton.vue'
 import V2BaseBadge from '@/components/V2BaseBadge.vue'
 import KpiBoxes from './KpiBoxes.vue'
+import reportDrillListMixin from '@/utils/mixins/reportDrillListMixin'
 import { money, shortDate } from '../format'
 
 /** Cột theo từng cơ cấu — dựng 1 lần để bảng, tiêu đề và thứ tự luôn khớp nhau */
 const DIMENSION_COLUMNS = {
     field: [
         { key: 'field', field: 'field_name', label: 'Lĩnh vực công ty kinh doanh', width: '190px', sortable: true },
         { key: 'sector', field: 'sector_name', label: 'Nhóm ngành', width: '140px', sortable: true },
     ],
     // Ô "Thị trường" hiện 2 dòng (tỉnh + phường/xã) nên sắp xếp phải ghép đúng 2 trường đó,
     // không thì bấm sort ra thứ tự không khớp với chữ đang nhìn thấy
@@ -311,33 +260,20 @@ const DIMENSION_COLUMNS = {
         { key: 'host', field: 'host_name', label: 'Kinh doanh chủ trì', width: '150px', sortable: true },
     ],
     // Phần IV — cấp tổ chức theo HỒ SƠ người chủ trì, khác nhóm `dept` ở trên (cột trên meeting)
     customer: [
         { key: 'hdept', field: 'host_department_name', label: 'Phòng ban chủ trì', width: '160px', sortable: true },
         { key: 'hpart', field: 'host_part_name', label: 'Bộ phận', width: '140px', sortable: true },
         { key: 'host', field: 'host_name', label: 'Kinh doanh chủ trì', width: '150px', sortable: true },
     ],
 }
 
-/**
- * "05/08/2026 09:00" -> 202608050900 (so sánh được bằng phép trừ), ô trống -> null.
- *
- * ⚠️ KHÔNG so ngày bằng chuỗi: "05/08/2026" > "30/07/2026" theo thứ tự chữ nhưng lại là ngày
- * TRƯỚC — bảng sẽ sắp sai mà nhìn vẫn "có thứ tự" nên rất khó phát hiện.
- */
-function dateSortKey(value) {
-    const m = String(value || '').match(/^(\d{2})\/(\d{2})\/(\d{4})(?:\s+(\d{2}):(\d{2}))?/)
-    if (!m) return null
-    const [, d, mo, y, h = '00', mi = '00'] = m
-    return Number(`${y}${mo}${d}${h}${mi}`)
-}
-
 /**
  * 2 bộ ô lọc của popup. Thứ tự: các cặp cha ▸ con đi liền nhau, Trạng thái đứng cuối (thêm ở
  * `filterFields`) — đúng thứ tự mockup.
  */
 const MAIN_FILTERS = [
     { param: 'drill_field_id', key: 'field', list: 'fields', placeholder: 'Chọn lĩnh vực công ty kinh doanh' },
     { param: 'drill_sector_id', key: 'sector', list: 'sectors', parent: 'drill_field_id', placeholder: 'Chọn nhóm ngành' },
     { param: 'drill_province_id', key: 'market', list: 'provinces', placeholder: 'Chọn tỉnh / thành phố' },
     { param: 'drill_ward_id', key: 'ward', list: 'wards', parent: 'drill_province_id', placeholder: 'Chọn phường / xã' },
     { param: 'drill_department_id', key: 'dept', list: 'departments', placeholder: 'Chọn phòng ban' },
@@ -346,132 +282,100 @@ const MAIN_FILTERS = [
 
 const CUSTOMER_FILTERS = [
     { param: 'drill_customer_id', key: 'customer', list: 'customers', placeholder: 'Chọn khách hàng' },
     { param: 'drill_host_department_id', key: 'hdept', list: 'host_departments', placeholder: 'Chọn phòng ban chủ trì' },
     { param: 'drill_host_part_id', key: 'hpart', list: 'parts', parent: 'drill_host_department_id', placeholder: 'Chọn bộ phận' },
     { param: 'drill_employee_id', key: 'emp', list: 'host_employees', parent: 'drill_host_department_id', placeholder: 'Chọn nhân viên chủ trì' },
 ]
 
 const REST_COLUMNS = [
     { key: 'customer', label: 'Khách hàng', width: '230px' },
-    { key: 'amount', label: 'Giá trị đầu tư dự kiến', width: '160px', cellClass: 'care-drill-table__money' },
-    { key: 'start', label: 'Thời gian triển khai', width: '140px', cellClass: 'care-drill-table__center' },
-    { key: 'repair', label: 'DV sửa chữa', width: '110px', cellClass: 'care-drill-table__center' },
+    { key: 'amount', label: 'Giá trị đầu tư dự kiến', width: '160px', cellClass: 'report-drill-table__money' },
+    { key: 'start', label: 'Thời gian triển khai', width: '140px', cellClass: 'report-drill-table__center' },
+    { key: 'repair', label: 'DV sửa chữa', width: '110px', cellClass: 'report-drill-table__center' },
     // Sắp xếp theo NGÀY HỌP (`meeting_start_date`), KHÔNG theo tên meeting: ô hiện tên ở dòng
     // trên và "Họp <ngày>" ở dòng dưới, người dùng bấm cột này là muốn xem theo thời gian.
     {
         key: 'meeting',
         field: 'meeting_start_date',
         label: 'Meeting thu thập nhu cầu',
         width: '220px',
         sortable: true,
         sortType: 'date',
     },
-    { key: 'status', label: 'Trạng thái', width: '160px', cellClass: 'care-drill-table__center' },
+    { key: 'status', label: 'Trạng thái', width: '160px', cellClass: 'report-drill-table__center' },
     { key: 'project', label: 'Dự án TKT', width: '140px' },
 ]
 
 export default {
     name: 'DemandListModal',
     components: {
+        V2BaseReportModal,
         V2BaseInput,
-        V2BasePagination,
         V2BaseSelectInModal,
         V2BaseButton,
         V2BaseIconButton,
         V2BaseBadge,
         KpiBoxes,
     },
+    mixins: [reportDrillListMixin],
     props: {
         visible: { type: Boolean, default: false },
         /** Đang chờ API của lượt drill này — nuôi trạng thái rỗng và khoá vài chỗ hiển thị */
         loading: { type: Boolean, default: false },
         title: { type: String, default: '' },
         drillKey: { type: String, default: 'all' },
         rows: { type: Array, default: () => [] },
         crossStats: { type: Array, default: () => [] },
         kpis: { type: Array, default: () => [] },
         total: { type: Number, default: 0 },
         totalAmount: { type: Number, default: 0 },
         canCreateProject: { type: Boolean, default: false },
         /** Danh mục dùng chung với bộ lọc màn chính */
         options: { type: Object, default: () => ({}) },
         meta: { type: Object, default: null },
     },
     data() {
         return {
-            keyword: '',
-            fullscreen: false,
-            /* MẶC ĐỊNH THU GỌN (user chốt 2026-09-06) — nhường chỗ cho bảng chi tiết; khối KPI +
-               "Phân bổ nhu cầu theo cơ cấu" mở bằng nút "Mở rộng". */
-            summaryCollapsed: true,
-            filters: this.emptyFilters(),
+            /* Drill phát sinh NGAY TRONG popup -> giữ nguyên phóng to / thu gọn, chỉ xoá bộ lọc */
+            keepView: false,
+            /* Chỉ tiêu ĐANG ĐỨNG TRƯỚC khi lọc sâu bằng hộp KPI — nuôi nút "Quay lại" */
+            backTo: null,
             statusOptions: [
                 { id: 1, name: 'Đang theo dõi' },
                 { id: 2, name: 'Đã lập dự án TKT' },
                 { id: 3, name: 'Không tiếp tục' },
             ],
-            /* Độ rộng thật của bảng — nuôi div rỗng của thanh cuộn trên */
-            scrollWidth: 0,
-            /* Bảng vừa khung thì giấu luôn thanh cuộn trên cho đỡ chiếm chỗ */
-            overflowing: false,
-            syncingScroll: false,
-            scrollBound: false,
-            /* Drill phát sinh NGAY TRONG popup -> giữ nguyên phóng to / thu gọn, chỉ xoá bộ lọc */
-            keepView: false,
-            /* Chỉ tiêu ĐANG ĐỨNG TRƯỚC khi lọc sâu bằng hộp KPI — nuôi nút "Quay lại" */
-            backTo: null,
-            /* Sắp xếp tại chỗ theo cột (không gọi lại API) */
-            sort: { key: '', dir: 'asc' },
-            /* Phân trang TẠI CHỖ: popup đã có trọn tập nên chỉ cắt phần hiển thị. Chip lọc, sắp
-               xếp, In danh sách và Xuất Excel vẫn chạy trên TOÀN TẬP — không đổi nội dung file. */
-            page: 1,
-            pageSize: 20,
         }
     },
     computed: {
         /** Có khối tổng hợp nào để thu gọn không (nhóm "không tiếp tục" không có KPI) */
         hasSummary() {
             return this.kpis.length > 0 || this.crossStats.length > 0
         },
         periodText() {
             if (!this.meta) return ''
             return `${shortDate(this.meta.from)} – ${shortDate(this.meta.to)}`
         },
         /**
          * Bộ lọc riêng của popup có CẮT BỚT dòng nào không (mockup: `rows.length !== all.length`).
          * Bám vào số dòng chứ không bám vào "có ô lọc nào được chọn" — chọn 1 giá trị mà không
          * loại dòng nào thì không cần khoe "đang lọc trong M nhu cầu".
          *
          * `total` do BE trả = số nhu cầu TRƯỚC bộ lọc popup (xem demandListBase()).
+         *
+         * ⚠️ Ở LẠI MÀN, KHÔNG đưa vào mixin: chỉ đúng với popup lọc ở SERVER. Mixin có
+         * `hasActiveFilter` (dựa trên state ô lọc) cho nút "Xoá lọc" — hai thứ khác nhau, đừng gộp.
          */
         isFiltered() {
             return this.rows.length !== this.total
         },
-        /** Tổng số trang — tối thiểu 1 để bảng rỗng không rơi vào trang 0 */
-        pageCount() {
-            return Math.max(1, Math.ceil(this.sortedRows.length / this.pageSize))
-        },
-        /**
-         * Trang thực dùng, đã KẸP trong [1, pageCount]. Cần vì bộ lọc/chip có thể cắt danh sách
-         * ngắn lại trong khi `page` còn giữ số cũ -> nếu lấy thẳng `page` sẽ ra trang trắng.
-         */
-        safePage() {
-            return Math.min(Math.max(1, this.page), this.pageCount)
-        },
-        pageOffset() {
-            return (this.safePage - 1) * this.pageSize
-        },
-        /** Phần hiển thị của trang hiện tại (sắp xếp + lọc vẫn tính trên TOÀN TẬP) */
-        pagedRows() {
-            return this.sortedRows.slice(this.pageOffset, this.pageOffset + this.pageSize)
-        },
         /**
          * Các cấp ĐÃ BỊ CỐ ĐỊNH bởi ô số vừa bấm. `drill_key` nay là đường dẫn nhiều cấp
          * (`customer:9+hdept:50+hpart:3`), nên phải đọc HẾT các tiền tố — chỉ lấy tiền tố đầu thì
          * ô lọc của các cấp sâu vẫn hiện dù giá trị đã bị khoá cứng.
          */
         drillTypes() {
             return String(this.drillKey || '')
                 .split('@')[0]
                 .split('+')
                 .map((segment) => segment.split(':')[0])
@@ -517,54 +421,20 @@ export default {
             if (this.showStatusFilter) {
                 all.push({ param: 'drill_status', key: 'status', options: this.statusOptions, placeholder: 'Chọn trạng thái nhu cầu' })
             }
 
             return all.map((field) => ({ ...field, options: field.options || [] }))
         },
         /**
          * Thứ tự cột bám ĐÚNG thứ tự hàng trong khối phân bổ (mockup chốt 24/08): cơ cấu chéo
          * hiện trước thì cột của nó đứng trước, ngay sau STT và TRƯỚC cột Khách hàng.
          */
-        /**
-         * Sắp xếp TẠI CHỖ trên danh sách đang có, không gọi lại API: popup vốn đã tải trọn tập
-         * của ô số đã bấm nên sort ở FE là đủ và không nháy dữ liệu.
-         * `localeCompare(…, 'vi')` để Đ/Ê/Ơ… đứng đúng chỗ trong bảng chữ cái tiếng Việt.
-         */
-        sortedRows() {
-            const { key, dir } = this.sort
-            if (!key) return this.rows
-
-            const col = this.columns.find((c) => c.key === key)
-            if (!col) return this.rows
-
-            const isDate = col.sortType === 'date'
-            const valueOf = (row) =>
-                isDate
-                    ? dateSortKey(row[col.field])
-                    : (col.sortFields
-                          ? col.sortFields.map((f) => row[f] || '').join(' ')
-                          : String(row[col.field] || '')
-                      ).trim()
-
-            const sign = dir === 'desc' ? -1 : 1
-            // Ô trống luôn xuống cuối ở CẢ 2 chiều — không thì bấm desc là cả cụm rỗng nhảy lên đầu
-            return [...this.rows].sort((a, b) => {
-                const va = valueOf(a)
-                const vb = valueOf(b)
-                const emptyA = isDate ? va === null : !va
-                const emptyB = isDate ? vb === null : !vb
-                if (emptyA && emptyB) return 0
-                if (emptyA) return 1
-                if (emptyB) return -1
-                return sign * (isDate ? va - vb : va.localeCompare(vb, 'vi'))
-            })
-        },
         columns() {
             const crossKeys = this.crossStats.map((stat) => stat.key)
             const ordered = []
 
             crossKeys.forEach((key) => ordered.push(...(DIMENSION_COLUMNS[key] || [])))
             // Cột của CHÍNH cơ cấu đang xem xếp ngay sau nhóm cột chéo
             if (this.drillDimension && !crossKeys.includes(this.drillDimension)) {
                 ordered.push(...(DIMENSION_COLUMNS[this.drillDimension] || []))
             }
 
@@ -574,103 +444,45 @@ export default {
                cùng `key` còn làm sắp xếp theo cột nhảy lung tung. */
             const seen = new Set()
             const unique = ordered.filter((col) => {
                 if (seen.has(col.key)) return false
                 seen.add(col.key)
                 return true
             })
 
             return [...unique, ...REST_COLUMNS]
         },
+        /** Dòng meta của dải banner — port nguyên văn từ `.report-drill-head__sub` (vỏ) */
+        metaText() {
+            if (this.loading) return `Đang tải… · Kỳ ${this.periodText}`
+            const base = `${this.rows.length} nhu cầu · ${this.money(this.totalAmount)} đ · Kỳ ${this.periodText}`
+            return this.isFiltered ? `${base} · đang lọc trong ${this.total} nhu cầu` : base
+        },
     },
     watch: {
         // Mở popup mới thì bộ lọc tự reset (mockup PIVOT v12)
         drillKey() {
             if (this.keepView) {
                 this.keepView = false
                 this.resetFilters()
                 return
             }
             this.resetLocal()
         },
-        /* Nội dung modal chỉ dựng khi mở -> phải bắt thanh cuộn lại sau mỗi lần mở */
         visible(open) {
             // Đóng popup là kết thúc mạch lọc sâu: mở lại (kể cả trúng đúng key cũ) không được
             // còn nút "Quay lại" treo lại từ lần trước
-            if (!open) {
-                this.backTo = null
-                return
-            }
-            this.$nextTick(() => {
-                this.bindScrollSync()
-                this.observeTable()
-                this.updateScrollWidth()
-            })
+            if (!open) this.backTo = null
         },
-        rows() {
-            this.$nextTick(this.updateScrollWidth)
-        },
-        columns() {
-            this.$nextTick(this.updateScrollWidth)
-        },
-        summaryCollapsed() {
-            this.$nextTick(this.updateScrollWidth)
-        },
-    },
-    mounted() {
-        window.addEventListener('resize', this.updateScrollWidth)
-    },
-    beforeDestroy() {
-        window.removeEventListener('resize', this.updateScrollWidth)
-        if (this.resizeObserver) this.resizeObserver.disconnect()
     },
     methods: {
         money,
-        /** 2 thanh cuộn (trên + dưới) luôn chạy cùng nhau; gọi lại mỗi lần mở popup */
-        bindScrollSync() {
-            const top = this.$refs.topScroll
-            const body = this.$refs.bodyScroll
-            if (!top || !body || this.scrollBound) return
-            this.scrollBound = true
-            top.addEventListener('scroll', () => {
-                if (this.syncingScroll) return
-                this.syncingScroll = true
-                body.scrollLeft = top.scrollLeft
-                this.syncingScroll = false
-            })
-            body.addEventListener('scroll', () => {
-                if (this.syncingScroll) return
-                this.syncingScroll = true
-                top.scrollLeft = body.scrollLeft
-                this.syncingScroll = false
-            })
-        },
-        /**
-         * Đo lại mỗi khi bảng đổi kích thước. Popup còn khó hơn màn chính: lúc `visible` bật thì
-         * modal đang chạy hiệu ứng mở và dữ liệu dòng chưa về, đo ngay là ra bề rộng sai.
-         */
-        observeTable() {
-            if (typeof ResizeObserver === 'undefined') return
-            const table = this.$refs.tableEl
-            const body = this.$refs.bodyScroll
-            if (!table || !body) return
-            if (this.resizeObserver) this.resizeObserver.disconnect()
-            this.resizeObserver = new ResizeObserver(() => this.updateScrollWidth())
-            this.resizeObserver.observe(table)
-            this.resizeObserver.observe(body)
-        },
-        updateScrollWidth() {
-            const table = this.$refs.tableEl
-            const body = this.$refs.bodyScroll
-            this.scrollWidth = table ? table.scrollWidth : 0
-            this.overflowing = !!body && this.scrollWidth > body.clientWidth + 1
-        },
         /**
          * Danh mục CON lọc theo giá trị của ô CHA đang chọn (Lĩnh vực ▸ Nhóm ngành ·
          * Tỉnh/TP ▸ Phường/xã · Phòng ban ▸ Nhân viên). BE trả kèm `parent_id` cho các danh mục
          * cấp con nên chỉ cần lọc tại chỗ, không phải gọi thêm API.
          *
          * Chưa chọn cha -> hiện toàn bộ (không chặn người dùng lọc thẳng ở cấp con).
          */
         childOptions(listKey, parentParam) {
             const list = this.options[listKey] || []
             const parentId = this.filters[parentParam]
@@ -720,44 +532,30 @@ export default {
         showFilter(key) {
             // Mọi cấp có mặt trong `drill_key` đều đã bị cố định -> ẩn hết ô của chúng
             if (this.drillTypes.includes(key)) return false
             // Key chỉ có 1 cấp (nhóm chỉ tiêu, hoặc dữ liệu cũ): vẫn ẩn ô CHA của cấp đang xem
             const pairs = { sector: 'field', ward: 'market', emp: 'dept', hpart: 'hdept' }
             if (pairs[this.drillType] === key) return false
             return true
         },
         /**
          * MỞ POPUP MỚI: trả cả trạng thái xem lẫn bộ lọc về mặc định (mockup `openDrill()` bỏ
-         * class full + gọi resetDrillFilters).
+         * class full + gọi resetDrillFilters). Phóng to/thu nhỏ nay do vỏ `V2BaseReportModal` tự
+         * quản (nó cũng tự trả về bình thường mỗi khi `visible` bật lại).
          */
         resetLocal() {
-            this.fullscreen = false
             // Mở popup mới -> trả về mặc định THU GỌN
             this.summaryCollapsed = true
             this.backTo = null
             this.sort = { key: '', dir: 'asc' }
             this.resetFilters()
         },
-        /**
-         * XOÁ LỌC: chỉ đụng tới bộ lọc. KHÔNG được đụng `fullscreen` / `summaryCollapsed` —
-         * mockup `resetDrillFilters()` chỉ xoá ô tìm kiếm + các select. Gộp chung vào
-         * `resetLocal()` làm popup đang phóng to tự thu nhỏ lại khi bấm Xoá lọc.
-         */
-        resetFilters() {
-            this.keyword = ''
-            this.filters = this.emptyFilters()
-            this.page = 1
-        },
-        clearFilters() {
-            this.resetFilters()
-            this.onFilterChange()
-        },
         /**
          * Chip "Phân bổ nhu cầu theo cơ cấu" CHÍNH LÀ lối tắt của ô lọc tương ứng (mockup:
          * `sel.value = sel.value === id ? '' : id` rồi nạp lại ô con). Vì vậy chip đọc/ghi
          * THẲNG vào `filters` — không giữ state riêng, nếu không bảng lọc theo chip mà ô lọc
          * vẫn trống, người dùng không biết đang lọc theo gì để bỏ ra.
          */
         chipParam(dimension) {
             return { field: 'drill_field_id', market: 'drill_province_id', dept: 'drill_department_id' }[dimension]
         },
         isChipActive(dimension, id) {
@@ -790,43 +588,20 @@ export default {
             this.$emit('drill', { key: next, title })
         },
         /** Trả popup về đúng chỉ tiêu trước khi lọc sâu (khối KPI hiện lại) */
         goBack() {
             const target = this.backTo
             if (!target) return
             this.backTo = null
             this.keepView = true
             this.$emit('drill', target)
         },
-        /** Bấm tiêu đề cột: lần đầu tăng dần, bấm lại đảo chiều (đúng khuôn V2BaseDataTable) */
-        toggleSort(key) {
-            this.sort =
-                this.sort.key === key
-                    ? { key, dir: this.sort.dir === 'asc' ? 'desc' : 'asc' }
-                    : { key, dir: 'asc' }
-            /* Đổi thứ tự là đổi cả tập đang xem -> đứng lại trang 5 là vô nghĩa */
-            this.page = 1
-        },
-        onPageChange(page) {
-            this.page = page
-            /* Sang trang mới phải cuộn bảng về đầu, không thì đang ở giữa trang cũ nhìn như
-               chưa đổi gì. */
-            if (this.$refs.bodyScroll) this.$refs.bodyScroll.scrollTop = 0
-        },
-        onPageSizeChange(size) {
-            this.pageSize = size
-            this.page = 1
-        },
-        sortIcon(key) {
-            if (this.sort.key !== key) return 'ri-arrow-up-down-line'
-            return this.sort.dir === 'asc' ? 'ri-arrow-up-line' : 'ri-arrow-down-line'
-        },
         onSelectChange(param) {
             this.resetChildOf(param)
             this.onFilterChange()
         },
         onFilterChange() {
             /* Đổi bộ lọc là đổi tập -> luôn về trang 1. Chỉ dựa vào phép kẹp `safePage` là chưa
                đủ: tập mới vẫn nhiều trang thì người dùng bị bỏ lại ở trang 3 của kết quả khác. */
             this.page = 1
             // Ô đang ẩn KHÔNG được lọc ngầm -> lọc bỏ trước khi gửi lên
             const active = {}
@@ -836,173 +611,51 @@ export default {
                 if (this.showFilter(field.key)) active[field.param] = this.filters[field.param]
             })
             active.drill_status = this.showStatusFilter ? this.filters.drill_status : null
 
             this.$emit('filter', { keyword: this.keyword, ...active })
         },
     },
 }
 </script>
 
-<style lang="scss">
-/* Popup rộng gần hết màn như mockup (.minutes-modal--wide) — KHÔNG scoped vì b-modal
-   render dialog ra ngoài cây component. */
-.care-drill-dialog {
-    max-width: 1400px;
-    width: 96vw;
-}
-/* Popup phải VỪA MÀN HÌNH: khoá chiều cao tổng (mockup dùng max-height 86vh), header/footer
-   đứng yên, chỉ thân cuộn. Thiếu khối này thì nội dung dài đẩy popup tràn khỏi viewport và
-   không cuộn tới được phần cuối bảng. */
-.care-drill-content {
-    /* ⚠️ `height` CỐ ĐỊNH, KHÔNG phải `max-height`. Để `max-height` thì popup cao theo số dòng
-       (đo được: 32 dòng -> 662px chạm trần, 2 dòng -> 568px) nên mỗi lượt drill lại đổi kích
-       thước một lần khi data về -> giật màn hình. Khoá cứng thì thân bảng tự cuộn, popup đứng yên. */
-    height: 92vh;
-    display: flex;
-    flex-direction: column;
-    overflow: hidden;
-}
-.care-drill-content .modal-header {
-    padding: 0;
-    border: 0;
-    flex-shrink: 0;
-}
-.care-drill-content .modal-body {
-    padding: 16px;
-    flex: 1 1 auto;
-    min-height: 0;
-    /* Popup cao cố định nên danh sách ngắn để lại khoảng trống: cho vùng bảng giãn ra và ĐẨY
-       footer xuống đáy, hộp mới trông có chủ đích thay vì nội dung lửng lơ giữa khung.
-       ⚠️ `overflow: hidden` chứ KHÔNG phải `auto`: phần tử cuộn dọc nay là `.care-drill-wrap`.
-       Để `auto` ở đây thì bảng dài tràn khỏi ô flex mà không bị cắt (đo được: bảng cao 1674px
-       trong khi thân popup chỉ 760px) và chạy XUYÊN qua footer đang ghim -> nút đè lên nội dung. */
-    overflow: hidden;
-    display: flex;
-    flex-direction: column;
-}
-.care-drill-scroll {
-    flex: 1 1 auto;
-    /* `min-height` để khối lọc + phân bổ cao không bóp vùng bảng còn 0 trên màn hình thấp */
-    min-height: 120px;
-    display: flex;
-    flex-direction: column;
-}
-.care-drill-footer,
-.care-drill-paging {
-    flex-shrink: 0;
-}
-/* Phóng to toàn màn hình — bám `.minutes-modal--full` của mockup.
-   Phải ghi đè cả `margin` và `min-height` vì `.modal-dialog(-centered)` của bootstrap đặt
-   margin 1.75rem + min-height calc(100% - 3.5rem); không ghi đè thì popup vẫn hở 4 mép. */
-.care-drill-dialog--full {
-    width: 100vw;
-    max-width: 100vw;
-    margin: 0;
-    min-height: 100vh;
-}
-.care-drill-dialog--full .care-drill-content {
-    height: 100vh;
-    max-height: 100vh;
-    border-radius: 0;
-}
-</style>
-
 <style lang="scss" scoped>
-/* Giá trị dưới đây port từ mockup đã duyệt — không tự đặt lại palette */
-$navy-start: #0a1c3d;
+/* Giá trị dưới đây port từ mockup đã duyệt — không tự đặt lại palette. Chỉ còn style RIÊNG của
+   màn (bộ lọc, khối KPI/phân bổ, nút quay lại, các ô bảng đặc biệt) — khung popup/dải banner/
+   bảng + thanh cuộn/phân trang nay do `components/report/V2BaseReportModal.vue` lo. */
 $teal: #06b6d4;
 $teal-dark: #0e7490;
 $text-main: #1f2937;
 $text-muted: #6b7280;
 
-.care-drill-head {
-    display: flex;
-    align-items: center;
-    justify-content: space-between;
-    gap: 10px;
-    width: 100%;
-    padding: 14px 16px;
-    background: linear-gradient(135deg, $navy-start, $teal);
-    color: #fff;
-}
-.care-drill-head__text {
-    min-width: 0;
-    flex: 1 1 auto;
-}
-.care-drill-head__title {
-    font-size: 15px;
-    line-height: 1.35;
-    overflow: hidden;
-    text-overflow: ellipsis;
-    white-space: nowrap;
-}
-/* Phần dẫn nhập mờ đi để TÊN ĐỐI TƯỢNG đang xem nổi hẳn lên */
-.care-drill-head__lead {
-    font-weight: 500;
-    color: rgba(255, 255, 255, 0.72);
-}
-.care-drill-head__object {
-    font-weight: 800;
-    color: #fff;
-}
-.care-drill-head__sub {
-    margin-top: 2px;
-    font-size: 11.5px;
-    font-weight: 500;
-    color: rgba(255, 255, 255, 0.85);
-}
-.care-drill-head__actions {
-    display: flex;
-    align-items: center;
-    gap: 6px;
-    flex-shrink: 0;
-}
-.care-drill-head__btn {
-    display: flex;
-    align-items: center;
-    justify-content: center;
-    width: 28px;
-    height: 28px;
-    border: none;
-    border-radius: 50%;
-    background: rgba(255, 255, 255, 0.15);
-    color: #fff;
-    cursor: pointer;
-
-    &:hover {
-        background: rgba(255, 255, 255, 0.3);
-    }
-}
-
-.care-drill-filters {
+.report-drill-filters {
     display: flex;
     flex-wrap: wrap;
     align-items: center;
     gap: 8px;
     margin-bottom: 10px;
 }
 /* Select render block-level -> phải khoá bề rộng từng ô, nếu không cả hàng lọc xếp DỌC */
-.care-drill-filters__item {
+.report-drill-filters__item {
     flex: 0 0 auto;
     width: 190px;
 }
-.care-drill-filters__item--search {
+.report-drill-filters__item--search {
     width: 250px;
 }
 /* Nút Xoá lọc co theo icon, KHÔNG lấy 190px như ô lọc */
-.care-drill-filters__item--action {
+.report-drill-filters__item--action {
     width: auto;
 }
 /* Đẩy "Thu gọn" + số đếm về mép phải của DÒNG CUỐI hàng lọc (flex-wrap nên auto tính theo dòng
    đang đứng), thay vì chiếm thêm một dòng riêng bên dưới. */
-.care-drill-filters__meta {
+.report-drill-filters__meta {
     display: flex;
     align-items: center;
     margin-left: auto;
 }
 .rsum-toggle {
     display: inline-flex;
     align-items: center;
     gap: 5px;
     height: 24px;
     padding: 0 9px;
@@ -1021,42 +674,42 @@ $text-muted: #6b7280;
 
     svg {
         width: 12px;
         height: 12px;
         transition: transform 0.15s ease;
     }
 }
 .rsum-toggle--collapsed svg {
     transform: rotate(-90deg);
 }
-.care-drill-count {
+.report-drill-count {
     margin-left: 12px;
     font-size: 12px;
     font-weight: 700;
     color: $text-main;
 }
 
 /* ---- Khối phân bổ theo cơ cấu ---- */
-.care-drill-sumbox {
+.report-drill-sumbox {
     flex-shrink: 0;
     margin: 0 0 10px;
     padding: 0 0 8px;
     border-bottom: 1px solid #e3e8ef;
 }
-.care-drill-sumbox__title {
+.report-drill-sumbox__title {
     margin: 0 0 5px;
     font-size: 11px;
     font-weight: 800;
     letter-spacing: 0.3px;
     color: $text-main;
 }
-.care-drill-sum {
+.report-drill-sum {
     display: flex;
     flex-direction: column;
     gap: 2px;
     margin: 0;
     padding: 0;
     flex-shrink: 0;
     overflow-x: auto;
     overflow-y: hidden;
     scrollbar-width: thin;
     scrollbar-color: #d7e0e8 transparent;
@@ -1069,239 +722,128 @@ $text-muted: #6b7280;
         border-radius: 2px;
 
         &:hover {
             background: #b8c6d4;
         }
     }
     &::-webkit-scrollbar-track {
         background: transparent;
     }
 }
-.care-drill-sum__grp {
+.report-drill-sum__grp {
     display: flex;
     align-items: baseline;
     gap: 8px;
     width: max-content;
     min-width: 100%;
 }
-.care-drill-sum__label {
+.report-drill-sum__label {
     flex-shrink: 0;
     width: 96px;
     font-size: 10px;
     font-weight: 800;
     letter-spacing: 0.4px;
     text-transform: uppercase;
     color: $text-muted;
     /* Ghim nhãn khi cuộn ngang để luôn biết đang xem cơ cấu nào */
     position: sticky;
     left: 0;
     z-index: 1;
     background: #fff;
 }
 /* KHÔNG xuống dòng: 1 cơ cấu = 1 hàng, dài thì cuộn ngang cả khối */
-.care-drill-sum__chips {
+.report-drill-sum__chips {
     display: flex;
     flex-wrap: nowrap;
     gap: 2px;
 }
-.care-drill-sum__chip {
+.report-drill-sum__chip {
     flex-shrink: 0;
     white-space: nowrap;
     display: inline-flex;
     align-items: baseline;
     gap: 5px;
     padding: 2px 7px;
     border: 1px solid transparent;
     border-radius: 5px;
     background: none;
     font-family: inherit;
     font-size: 11.5px;
     color: $text-main;
     cursor: pointer;
 
     &:hover {
         background: #eef6fa;
     }
 }
-.care-drill-sum__chip--on {
+.report-drill-sum__chip--on {
     border-color: $teal;
     background: #e2f5fa;
 }
-.care-drill-sum__chip__n {
+.report-drill-sum__chip__n {
     font-weight: 800;
     color: $teal-dark;
     font-variant-numeric: tabular-nums;
 }
-.care-drill-sum__chip__pct {
+.report-drill-sum__chip__pct {
     font-size: 10.5px;
     color: #94a3b8;
     font-variant-numeric: tabular-nums;
 }
 
-/* ---- Bảng chi tiết ---- */
-/* Dải "Quay lại" thay chỗ khối KPI khi đang lọc sâu */
-.care-drill-back {
+/* ---- Nút Quay lại (đang lọc sâu từ hộp KPI) ---- */
+.report-drill-back {
     display: flex;
     align-items: center;
     gap: 10px;
     margin-bottom: 8px;
 }
-.care-drill-back__from {
+.report-drill-back__from {
     font-size: 11.5px;
     color: $text-muted;
 }
 
-.care-drill-scroll {
-    width: 100%;
-}
-.care-drill-topscroll {
-    overflow-x: auto;
-    overflow-y: hidden;
-    height: 10px;
-    margin-bottom: 3px;
-}
-.care-drill-wrap {
-    /* Vùng CUỘN DỌC của popup (thân popup đã `overflow: hidden`). Nhờ vậy `thead th` sticky ghim
-       đúng trong khung bảng — trước đây nó ghim theo thân popup nên cuộn là mất tên cột. */
-    flex: 1 1 auto;
-    min-height: 0;
-    overflow: auto;
-    border: 1px solid #e3e8ef;
-    border-radius: 6px;
-}
-
-/* Thanh cuộn mảnh cho cả 2 khung */
-.care-drill-topscroll::-webkit-scrollbar,
-.care-drill-wrap::-webkit-scrollbar {
-    width: 6px;
-    height: 6px;
-}
-.care-drill-topscroll::-webkit-scrollbar-track,
-.care-drill-wrap::-webkit-scrollbar-track {
-    background: #f1f5f9;
-}
-.care-drill-topscroll::-webkit-scrollbar-thumb,
-.care-drill-wrap::-webkit-scrollbar-thumb {
-    background: #cbd5e1;
-    border-radius: 3px;
-}
-.care-drill-topscroll::-webkit-scrollbar-thumb:hover,
-.care-drill-wrap::-webkit-scrollbar-thumb:hover {
-    background: #94a3b8;
-}
-
-.care-drill-table {
-    width: 100%;
-    /* `auto` + `nowrap`: cột tự nới theo nội dung dài nhất, bảng tràn ngang thì cuộn —
-       không bẻ chữ xuống dòng nữa. Width khai ở <th> nay là mức TỐI THIỂU. */
-    table-layout: auto;
-    border-collapse: collapse;
-    font-size: 12px;
-    background: #fff;
-
-    th,
-    td {
-        padding: 7px 9px;
-        border: 1px solid #d6dde6;
-        vertical-align: middle;
-        white-space: nowrap;
-    }
-
-    thead th {
-        position: sticky;
-        top: 0;
-        z-index: 3;
-        background: linear-gradient(180deg, #f3fdfe, #e2f6f9);
-        border-bottom: 2px solid #20d9ea;
-        color: #0a7c88;
-        font-size: 11px;
-        font-weight: 700;
-        /* Viết hoa CHỮ ĐẦU thôi (user chốt 2026-09-06); `nowrap` giữ nguyên: tiêu đề cột không
-           được xuống dòng, cột dài thì bảng nới ra và cuộn ngang. */
-        text-transform: none;
-        letter-spacing: 0;
-        text-align: left;
-        white-space: nowrap;
-    }
-
-    tbody tr:hover td {
-        background: #ddf0f7;
-    }
-}
-.care-drill-table__center {
-    text-align: center;
-}
-.care-drill-table__money {
+/* ---- Các ô bảng đặc biệt (chưa có ở vỏ dùng chung) ---- */
+.report-drill-table__money {
     text-align: right;
     font-weight: 700;
     font-variant-numeric: tabular-nums;
 }
-.care-drill-table__empty {
-    padding: 22px;
-    text-align: center;
-    color: $text-muted;
-}
-.care-drill-sub {
+.report-drill-sub {
     color: $text-muted;
     font-size: 11px;
 }
 /* Tên KH + nút mở lịch sử meeting.
    Nút hiện RÕ THƯỜNG TRỰC, KHÔNG làm mờ rồi chỉ sáng lên khi rê chuột: đây là lối vào duy nhất
    của tính năng lịch sử meeting, để mờ thì phải dò mới thấy — và trên thiết bị cảm ứng không có
    trạng thái hover để mà sáng lên. */
-.care-drill-customer {
+.report-drill-customer {
     display: inline-flex;
     align-items: flex-start;
     gap: 4px;
 }
-/* Tiêu đề cột bấm được để sắp xếp — copy khuôn `.sortable-header` của V2BaseDataTable */
-.care-drill-sort {
-    display: inline-flex;
-    align-items: center;
-    cursor: pointer;
-    user-select: none;
-
-    i {
-        margin-left: 4px;
-        font-size: 12px;
-        color: #9ca3af;
-    }
-
-    &:hover i {
-        color: #0e7490;
-    }
-}
 
 /* Link trong bảng (tên meeting, mã dự án) — class riêng của từng loại chỉ để chọn/đếm */
-.care-drill-link {
+.report-drill-link {
     color: #0e7490;
     font-weight: 600;
     cursor: pointer;
 
     &:hover {
         color: #0a5c73;
         text-decoration: underline;
     }
 }
 /* Nhãn "Kỳ trước" — nhu cầu thu thập từ kỳ trước, sang kỳ này vẫn còn theo dõi */
-.care-drill-carry {
+.report-drill-carry {
     display: inline-block;
     margin-left: 5px;
     padding: 0 5px;
     border: 1px solid #fcd34d;
     border-radius: 3px;
     background: #fffbeb;
     color: #b45309;
     font-size: 10px;
     font-weight: 700;
     line-height: 15px;
 }
-
-.care-drill-footer {
-    display: flex;
-    justify-content: flex-end;
-    gap: 8px;
-    padding: 12px 0 0;
-    margin-top: 12px;
-    border-top: 1px solid #e3e8ef;
-}
 </style>
diff --git a/utils/mixins/reportDrillListMixin.js b/utils/mixins/reportDrillListMixin.js
new file mode 100644
index 000000000..386728815
--- /dev/null
+++ b/utils/mixins/reportDrillListMixin.js
@@ -0,0 +1,126 @@
+/**
+ * MÁY CLIENT-SIDE cho popup drill-down của màn báo cáo.
+ *
+ * CHỈ ôm phần 3 popup lớn giống hệt nhau: sắp xếp, phân trang, state bộ lọc.
+ * KHÔNG ôm phần lọc — 3 popup dùng 3 chiến lược khác nhau (đo 2026-09-17):
+ *   · DemandListModal      — lọc ở SERVER (emit `filter`, màn cha tải lại)
+ *   · DevelopmentDrillModal — lọc CLIENT tại chỗ
+ *   · ProjectListModal      — lọc ở SERVER, popup tự gọi API
+ * Vì vậy `onFilterChange()` là HOOK do component tự cài, còn `applyLocalFilters()` là hàm
+ * TUỲ CHỌN cho popup lọc client-side.
+ *
+ * Component dùng mixin phải khai: `rows`, `columns`, `emptyFilters()`, `onFilterChange()`.
+ */
+const dateSortKey = (value) => {
+    if (!value) return null
+    // Dữ liệu hiển thị dạng "dd/mm/yyyy" hoặc "dd/mm/yyyy hh:mm" — `new Date()` đọc sai (hiểu là
+    // mm/dd). ⚠️ PHẢI bắt cả giờ:phút — bỏ khuyết thì 2 dòng cùng ngày khác giờ xếp lẫn lộn theo
+    // thứ tự ban đầu của mảng thay vì theo thời gian (đo được ở DemandListModal — Task 5).
+    const m = String(value).match(/^(\d{2})\/(\d{2})\/(\d{4})(?:\s+(\d{2}):(\d{2}))?/)
+    if (m) {
+        const [, d, mo, y, h = '00', mi = '00'] = m
+        return new Date(`${y}-${mo}-${d}T${h}:${mi}:00`).getTime()
+    }
+    const t = new Date(value).getTime()
+    return Number.isNaN(t) ? null : t
+}
+
+export default {
+    data() {
+        return {
+            keyword: '',
+            filters: this.emptyFilters(),
+            /* Sắp xếp TẠI CHỖ: popup đã có trọn tập của ô số đã bấm nên không gọi lại API */
+            sort: { key: '', dir: 'asc' },
+            page: 1,
+            pageSize: 20,
+            /* Mặc định THU GỌN — nhường chỗ cho bảng chi tiết (user chốt 2026-09-06) */
+            summaryCollapsed: true,
+        }
+    },
+    computed: {
+        sortedRows() {
+            const { key, dir } = this.sort
+            if (!key) return this.rows
+
+            const col = this.columns.find((c) => c.key === key)
+            if (!col) return this.rows
+
+            const isDate = col.sortType === 'date'
+            const valueOf = (row) =>
+                isDate
+                    ? dateSortKey(row[col.field])
+                    : (col.sortFields ? col.sortFields.map((f) => row[f] || '').join(' ') : String(row[col.field] || '')).trim()
+
+            const sign = dir === 'desc' ? -1 : 1
+            // Ô trống luôn xuống cuối ở CẢ 2 chiều — không thì bấm desc là cụm rỗng nhảy lên đầu
+            return [...this.rows].sort((a, b) => {
+                const va = valueOf(a)
+                const vb = valueOf(b)
+                const emptyA = isDate ? va === null : !va
+                const emptyB = isDate ? vb === null : !vb
+                if (emptyA && emptyB) return 0
+                if (emptyA) return 1
+                if (emptyB) return -1
+                return sign * (isDate ? va - vb : va.localeCompare(vb, 'vi'))
+            })
+        },
+        pageCount() {
+            return Math.max(1, Math.ceil(this.sortedRows.length / this.pageSize))
+        },
+        /* Kẹp trong [1, pageCount]: bộ lọc cắt danh sách ngắn lại mà `page` còn giữ số cũ thì
+           lấy thẳng `page` sẽ ra trang trắng. */
+        safePage() {
+            return Math.min(Math.max(1, this.page), this.pageCount)
+        },
+        pageOffset() {
+            return (this.safePage - 1) * this.pageSize
+        },
+        pagedRows() {
+            return this.sortedRows.slice(this.pageOffset, this.pageOffset + this.pageSize)
+        },
+        hasActiveFilter() {
+            return !!this.keyword || Object.values(this.filters).some((v) => v !== null && v !== '' && !(Array.isArray(v) && !v.length))
+        },
+    },
+    watch: {
+        /* Đổi tập dữ liệu (lượt drill mới / cha tải lại) -> về trang 1. Chỉ dựa vào `safePage` là
+           chưa đủ: tập mới vẫn nhiều trang thì người dùng bị bỏ lại ở trang 3 của kết quả khác. */
+        rows() {
+            this.page = 1
+        },
+    },
+    methods: {
+        toggleSort(key) {
+            if (this.sort.key === key) this.sort = { key, dir: this.sort.dir === 'asc' ? 'desc' : 'asc' }
+            else this.sort = { key, dir: 'asc' }
+        },
+        onPageChange(page) {
+            this.page = page
+        },
+        onPageSizeChange(size) {
+            this.pageSize = size
+            this.page = 1
+        },
+        resetFilters() {
+            this.keyword = ''
+            this.filters = this.emptyFilters()
+            this.page = 1
+            this.onFilterChange()
+        },
+        /** TUỲ CHỌN — chỉ popup lọc client-side gọi tới. Khớp chuỗi không dấu phân biệt hoa thường. */
+        applyLocalFilters(rows) {
+            const kw = this.keyword.trim().toLowerCase()
+            return rows.filter((row) => {
+                const okFilters = Object.keys(this.filters).every((param) => {
+                    const want = this.filters[param]
+                    if (want === null || want === '') return true
+                    return String(row[param]) === String(want)
+                })
+                if (!okFilters) return false
+                if (!kw) return true
+                return Object.values(row).some((v) => String(v == null ? '' : v).toLowerCase().includes(kw))
+            })
+        },
+    },
+}
