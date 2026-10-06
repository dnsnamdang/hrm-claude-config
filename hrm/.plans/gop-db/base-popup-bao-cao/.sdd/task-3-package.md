# Review package: 7faef7daf..127285043

## Commits
127285043 fix(report): dời .report-drill-wrap sang style không scoped để viền/scrollbar áp đúng vào V2BaseTableScroll
eb7b3a7b2 feat(report): thêm V2BaseReportModal làm vỏ dùng chung cho popup báo cáo

## Files changed
 components/report/V2BaseReportModal.vue | 369 ++++++++++++++++++++++++++++++++
 1 file changed, 369 insertions(+)

## Diff
diff --git a/components/report/V2BaseReportModal.vue b/components/report/V2BaseReportModal.vue
new file mode 100644
index 000000000..e98847089
--- /dev/null
+++ b/components/report/V2BaseReportModal.vue
@@ -0,0 +1,369 @@
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
+-->
+<template>
+    <V2BaseModal
+        :modal-id="modalId"
+        size="xl"
+        :dialog-class="fullscreen ? `${dialogClass} report-drill-dialog--full` : dialogClass"
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
+        <V2BaseTableScroll :max-height="maxTableHeight" body-class="report-drill-wrap">
+            <table class="report-drill-table">
+                <thead>
+                    <tr>
+                        <th style="min-width: 46px">STT</th>
+                        <th v-for="col in columns" :key="col.key" :style="{ minWidth: col.width }">
+                            <span v-if="col.sortable" class="report-drill-sort" @click="$emit('sort', { key: col.key })">
+                                {{ col.label }}
+                                <i :class="sortIcon(col.key)"></i>
+                            </span>
+                            <span v-else>{{ col.label }}</span>
+                        </th>
+                    </tr>
+                </thead>
+                <tbody>
+                    <tr v-for="(row, index) in rows" :key="row[rowKey]">
+                        <td class="report-drill-table__center">{{ startIndex + index + 1 }}</td>
+                        <td v-for="col in columns" :key="col.key" :class="col.cellClass">
+                            <slot :name="`cell-${col.key}`" :row="row" :index="index" :column="col">
+                                {{ row[col.field] }}
+                            </slot>
+                        </td>
+                    </tr>
+                    <tr v-if="!rows.length">
+                        <td :colspan="columns.length + 1" class="report-drill-table__empty">
+                            {{ loading ? 'Đang tải…' : emptyText }}
+                        </td>
+                    </tr>
+                </tbody>
+            </table>
+        </V2BaseTableScroll>
+
+        <V2BasePagination
+            v-if="!loading && totalRows"
+            class="report-drill-paging"
+            :current-page="currentPage"
+            :current-page-size="currentPageSize"
+            :total-rows="totalRows"
+            :item-label="itemLabel"
+            :page-size-options="pageSizeOptions"
+            @page-change="(v) => $emit('page-change', v)"
+            @page-size-change="(v) => $emit('page-size-change', v)"
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
+.report-drill-content {
+    height: 92vh;
+    display: flex;
+    flex-direction: column;
+    overflow: hidden;
+}
+.report-drill-content .modal-header {
+    padding: 0;
+    border: 0;
+    flex-shrink: 0;
+}
+.report-drill-content .modal-body {
+    padding: 16px;
+    flex: 1 1 auto;
+    min-height: 0;
+    overflow: hidden;
+    display: flex;
+    flex-direction: column;
+}
+.report-drill-scroll {
+    flex: 1 1 auto;
+    min-height: 120px;
+    display: flex;
+    flex-direction: column;
+}
+.report-drill-footer,
+.report-drill-paging {
+    flex-shrink: 0;
+}
+.report-drill-dialog--full .report-drill-content {
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
