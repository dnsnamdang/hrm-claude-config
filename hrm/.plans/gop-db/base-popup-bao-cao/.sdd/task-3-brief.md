### Task 3: `V2BaseReportModal.vue` — vỏ popup báo cáo

**Files:**
- Create: `hrm-client/components/report/V2BaseReportModal.vue`

**Interfaces:**
- Consumes: slot `header` của `V2BaseModal` (Task 2).
- Produces — **props**: `visible: Boolean`, `modalId: String`, `lead: String`, `title: String`, `meta: String`, `loading: Boolean`, `columns: Array`, `rows: Array` (dòng của TRANG ĐANG XEM, không phải cả tập), `rowKey: String = 'id'`, `startIndex: Number = 0` (STT bắt đầu), `emptyText: String = 'Không có dữ liệu khớp bộ lọc.'`, `sort: Object = { key: '', dir: 'asc' }`, `currentPage: Number`, `currentPageSize: Number`, `totalRows: Number`, `itemLabel: String`, `pageSizeOptions: Array = [20, 50, 100]`, `fullscreenable: Boolean = true`, `maxTableHeight: String = '50vh'`, `dialogClass: String`.
  **events**: `close`, `sort` (`{ key }`), `page-change` (`Number`), `page-size-change` (`Number`), `toggle-fullscreen` (`Boolean`).
  **slots**: `filters`, `summary`, `back`, `footer`, `cell-<key>` (scoped, `{ row, index, column }`).

- [ ] **Step 1: Viết component**

```vue
<!--
    VỎ DÙNG CHUNG CHO POPUP BÁO CÁO (drill-down).

    Mẫu nguồn: popup "Danh sách nhu cầu" của báo cáo CSKH tiềm năng — user chốt giữ nguyên dải
    banner của nó làm nhận diện riêng cho popup báo cáo.

    Dựng TRÊN `V2BaseModal` chứ không fork `b-modal`: chính việc fork `b-modal` làm popup báo cáo
    lệch chuẩn ngay từ đầu, và đẻ ra bẫy stacking context (BootstrapVue bọc mỗi modal trong
    `_BV_modal_outer_` z-index 1041 — xem `components/print/ReportPrintPreviewModal.vue`).

    Component này KHÔNG biết nghiệp vụ, KHÔNG biết lấy dữ liệu, KHÔNG tự lọc/sắp/phân trang.
    Máy client-side nằm ở `utils/mixins/reportDrillListMixin.js`.
-->
<template>
    <V2BaseModal
        :modal-id="modalId"
        size="xl"
        :dialog-class="fullscreen ? `${dialogClass} report-drill-dialog--full` : dialogClass"
        max-body-height="none"
        no-enforce-focus
        @hidden="$emit('close')"
    >
        <template #header="{ close }">
            <div class="report-drill-head">
                <div class="report-drill-head__text">
                    <div class="report-drill-head__title">
                        <span v-if="lead" class="report-drill-head__lead">{{ lead }}</span>
                        <span class="report-drill-head__object">{{ title }}</span>
                    </div>
                    <div class="report-drill-head__sub">{{ meta }}</div>
                </div>
                <div class="report-drill-head__actions">
                    <button
                        v-if="fullscreenable"
                        type="button"
                        class="report-drill-head__btn"
                        :title="fullscreen ? 'Thu nhỏ popup' : 'Phóng to toàn màn hình'"
                        @click="toggleFullscreen"
                    >
                        <i :class="fullscreen ? 'ri-fullscreen-exit-line' : 'ri-fullscreen-line'"></i>
                    </button>
                    <button type="button" class="report-drill-head__btn" title="Đóng" @click="close()">
                        <i class="ri-close-line"></i>
                    </button>
                </div>
            </div>
        </template>

        <slot name="filters"></slot>
        <slot name="back"></slot>
        <slot name="summary"></slot>

        <V2BaseTableScroll :max-height="maxTableHeight">
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
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(row, index) in rows" :key="row[rowKey]">
                        <td class="report-drill-table__center">{{ startIndex + index + 1 }}</td>
                        <td v-for="col in columns" :key="col.key" :class="col.cellClass">
                            <slot :name="`cell-${col.key}`" :row="row" :index="index" :column="col">
                                {{ row[col.field] }}
                            </slot>
                        </td>
                    </tr>
                    <tr v-if="!rows.length">
                        <td :colspan="columns.length + 1" class="report-drill-table__empty">
                            {{ loading ? 'Đang tải…' : emptyText }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </V2BaseTableScroll>

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
            <slot name="footer"></slot>
        </template>
    </V2BaseModal>
</template>

<script>
import V2BaseModal from '@/components/modal/V2BaseModal.vue'
import V2BaseTableScroll from '@/components/V2BaseTableScroll.vue'
import V2BasePagination from '@/components/V2BasePagination.vue'

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
        itemLabel: { type: String, default: 'bản ghi' },
        pageSizeOptions: { type: Array, default: () => [20, 50, 100] },
        fullscreenable: { type: Boolean, default: true },
        maxTableHeight: { type: String, default: '50vh' },
        dialogClass: { type: String, default: 'report-drill-dialog' },
    },
    data() {
        return { fullscreen: false }
    },
    watch: {
        /* Mở lượt MỚI thì trả popup về kích thước thường. Giữ nguyên là lượt sau mang kích thước
           của lượt trước — đúng lỗi ca e2e 17 canh. */
        visible(value) {
            if (value) this.fullscreen = false
            this.$nextTick(() => this.syncBvModal(value))
        },
    },
    mounted() {
        this.syncBvModal(this.visible)
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
        sortIcon(key) {
            if (this.sort.key !== key) return 'ri-arrow-up-down-line'
            return this.sort.dir === 'asc' ? 'ri-arrow-up-line' : 'ri-arrow-down-line'
        },
    },
}
</script>

<style lang="scss">
/* KHÔNG `scoped`: `b-modal` render dialog ra ngoài cây component nên style scoped không với tới.
   Toàn bộ giá trị dưới đây port từ `.care-drill-*` của mẫu nguồn — đổi tên tiền tố, giữ nguyên số. */
.report-drill-dialog { max-width: 1400px; }
.report-drill-dialog--full { width: 100vw; max-width: 100vw; margin: 0; min-height: 100vh; }
/* CHÉP NGUYÊN các khối sau từ `DemandListModal.vue`, chỉ thay tiền tố `care-drill` →
   `report-drill`, KHÔNG chỉnh lại số:
     · dòng 846–909 (khối `<style lang="scss">` KHÔNG scoped):
         .care-drill-dialog · .care-drill-dialog--full · .care-drill-content ·
         .care-drill-footer · .care-drill-paging · .care-drill-scroll
     · trong khối `<style lang="scss" scoped>` (dòng 910 → hết file), chỉ lấy các lớp của VỎ:
         .care-drill-head · __text · __title · __lead · __object · __sub · __actions · __btn ·
         .care-drill-topscroll · .care-drill-wrap · .care-drill-table (+ th/td/thead/tbody) ·
         .care-drill-sort · .care-drill-table__center · .care-drill-table__empty
   KHÔNG lấy: .care-drill-filters*, .care-drill-sum*, .care-drill-customer, .care-drill-sub,
   .care-drill-meeting, .care-drill-back — đó là style RIÊNG của màn, ở lại `DemandListModal.vue`.
   ⚠️ Nhưng các lớp ở lại màn VẪN ĐỔI TÊN sang `report-drill-*` (Task 5) — Task 6 đổi selector e2e
   hàng loạt theo tiền tố, chừa lại vài lớp `care-drill-*` là 106 selector trỏ vào lớp không còn. */
</style>
```

- [ ] **Step 2: Kiểm component dựng được (chưa gắn vào màn nào)**

Nuxt dev server tự biên dịch lại. Kiểm không có lỗi compile:

```bash
curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "%{http_code}\n"
```

Expected: `200`, và log dev server không có dòng `Failed to compile`.

- [ ] **Step 3: Commit**

```bash
git add components/report/V2BaseReportModal.vue
git commit -m "feat(report): thêm V2BaseReportModal làm vỏ dùng chung cho popup báo cáo"
```

---

