<!--
    Popup danh sách nhu cầu / dự án TKT — mở khi bấm bất kỳ con số nào ở khối tổng hợp / bảng cây
    (mockup đã chốt `.plans/gop-db/bao-cao-tong-hop-cskh-tiem-nang/mockup.html`, khối POPUP DRILL).

    Copy khuôn `pages/assign/report/service-demand/components/DemandListModal.vue`: vỏ chung `V2BaseReportModal` +
    `reportDrillListMixin` (sắp xếp + phân trang tại chỗ). Màn cha tải TRỌN tập của ô số đã bấm (`item-list`, mọi
    trang) rồi truyền vào `rows`; ô lọc riêng của popup chỉ cắt tập đó tại chỗ, không gọi lại API.

    Ô lọc bị ô số đã bấm CỐ ĐỊNH thì ẩn: bấm số nhu cầu -> ẩn ô Loại + Tiến trình; bấm 1 tiến trình -> ẩn ô Tiến trình.
    In / Xuất Excel: emit bộ lọc đang áp (`q`, `type`, `sales_id`, `statuses`) để màn cha ghép với bộ lọc của ô số.
    Ô tìm lọc tại chỗ nhưng PHẢI khớp BE `q` (KH tên/mã · mã/tên dự án · mã meeting · tên Sales · nội dung, không
    phân biệt hoa thường) -> cùng các trường đó.
-->
<template>
    <V2BaseReportModal
        modal-id="pct-item-list-modal"
        :visible="visible"
        :loading="loading"
        lead="Bạn đang xem:"
        :title="title"
        :meta="metaText"
        :columns="columns"
        :rows="pagedRows"
        :start-index="pageOffset"
        :sort="sort"
        :current-page="safePage"
        :current-page-size="pageSize"
        :total-rows="sortedRows.length"
        item-label="dòng"
        empty-text="Không có nhu cầu / dự án nào khớp bộ lọc."
        max-table-height=""
        dialog-class="report-drill-dialog pct-drill-dialog"
        @sort="({ key }) => toggleSort(key)"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
        @close="$emit('close')"
    >
        <template #filters>
            <div class="report-drill-filters">
                <div class="report-drill-filters__item report-drill-filters__item--search">
                    <V2BaseInput v-model="keyword" size="sm" placeholder="Tìm khách hàng / dự án / meeting / Sales…" @input="onFilterChange" />
                </div>
                <div v-for="field in filterFields" :key="field.key" class="report-drill-filters__item">
                    <V2BaseSelectInModal
                        v-model="filters[field.key]"
                        :options="field.options"
                        :allowClear="true"
                        size="sm"
                        :placeholder="field.placeholder"
                        @change="onFilterChange"
                    />
                </div>

                <div v-if="hasActiveFilter" class="report-drill-filters__item report-drill-filters__item--action">
                    <V2BaseIconButton title="Xoá lọc" @click="resetFilters">
                        <i class="ri-refresh-line"></i>
                    </V2BaseIconButton>
                </div>

                <span v-if="!loading" class="report-drill-count">{{ filteredRows.length }} / {{ rows.length }} dòng</span>
            </div>
        </template>

        <template #cell-type="{ row }">{{ typeText(row.type) }}</template>
        <template #cell-content="{ row }">
            <template v-if="row.type === 'da'">
                <a
                    :href="`/assign/prospective-projects/${row.id}`"
                    target="_blank"
                    rel="noopener"
                    class="v2-cell-link pct-link"
                    :title="'Mở dự án ' + row.code + ' ở tab mới'"
                    >{{ row.code }}</a
                >
                <div class="pct-sub">{{ row.name }}</div>
            </template>
            <template v-else>{{ row.content }}</template>
        </template>
        <template #cell-customer="{ row }">
            {{ row.customer_name }}
            <div v-if="row.customer_code" class="pct-sub">{{ row.customer_code }}</div>
        </template>
        <template #cell-sales="{ row }">{{ row.sales_label || '' }}</template>
        <template #cell-status="{ row }">
            <V2BaseBadge :color="row.status_color">{{ row.status_text }}</V2BaseBadge>
        </template>
        <template #cell-value="{ row }">{{ num(row.value) }}</template>
        <template #cell-milestone="{ row }">
            {{ dmy(row.milestone_date) }}
            <div class="pct-sub">{{ row.type === 'nc' ? 'dự kiến triển khai' : 'KH cần giải pháp' }}</div>
        </template>
        <template #cell-due="{ row }">
            <template v-if="row.type === 'nc'">
                <template v-if="row.due_date">
                    <span :class="{ 'pct-warn': row.is_due_soon }">{{ dmy(row.due_date) }}</span>
                    <div class="pct-sub" :class="{ 'pct-warn': row.is_due_soon }">{{ daysNote(row.due_days_left) }}</div>
                </template>
                <span v-else class="pct-none">Không có hạn</span>
            </template>
        </template>
        <template #cell-source="{ row }">
            <a
                v-if="row.meeting_code"
                href="#"
                class="v2-cell-link pct-link"
                :title="'Xem meeting ' + row.meeting_code"
                @click.prevent="$emit('open-meeting', row)"
                >{{ row.meeting_code }}</a
            >
        </template>

        <!-- button-convention mục 2b + 5: hành động phụ trước, Đóng cuối; Xuất Excel secondary-success.
             Không thêm mr-2/mb-2: khuôn `#footer` của vỏ tự cách nút (xem HoldListModal). -->
        <template #footer>
            <V2BaseButton secondary size="sm" @click="$emit('print', ownParams())">
                <template #prefix><i class="ri-printer-line" style="font-size: 14px"></i></template>
                In danh sách
            </V2BaseButton>
            <V2BaseButton secondary status="success" size="sm" @click="$emit('export', ownParams())">
                <template #prefix><i class="ri-file-excel-2-line" style="font-size: 14px"></i></template>
                Xuất Excel danh sách
            </V2BaseButton>
            <V2BaseButton tertiary size="sm" @click="$emit('close')">
                <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                Đóng
            </V2BaseButton>
        </template>
    </V2BaseReportModal>
</template>

<script>
import V2BaseReportModal from '@/components/report/V2BaseReportModal.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseIconButton from '@/components/V2BaseIconButton.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import reportDrillListMixin from '@/utils/mixins/reportDrillListMixin'
import { num, dmy, daysNote, typeText } from '../format'

/** Chuẩn hoá chữ để so như MySQL utf8mb4_unicode_ci: thường hoá + bỏ dấu (đ giữ nguyên, đúng collation) */
function fold(text) {
    return String(text || '')
        .normalize('NFD')
        .replace(/[̀-ͯ]/g, '')
        .toLowerCase()
}

/** Thứ tự cột theo mockup (popup drill). `field` = khoá sắp xếp của mixin. */
const COLUMNS = [
    { key: 'type', field: 'type', label: 'Loại', width: '90px', sortable: true },
    { key: 'content', field: 'content', label: 'Nội dung', width: '230px', sortable: true, cellClass: 'pct-drill-wrap' },
    { key: 'customer', field: 'customer_name', label: 'Khách hàng', width: '210px', sortable: true, cellClass: 'pct-drill-wrap' },
    { key: 'sales', field: 'sales_label', label: 'Sales phụ trách', width: '200px', sortable: true, cellClass: 'pct-drill-wrap' },
    { key: 'status', field: 'status_text', label: 'Trạng thái', width: '170px', sortable: true },
    { key: 'value', field: 'value', label: 'Giá trị dự kiến', width: '120px', sortable: true, sortType: 'number', cellClass: 'report-drill-table__right' },
    { key: 'milestone', field: 'milestone_date', label: 'Mốc thời gian', width: '120px', sortable: true, cellClass: 'report-drill-table__center' },
    { key: 'due', field: 'due_date', label: 'Hạn theo dõi', width: '120px', sortable: true, cellClass: 'report-drill-table__center' },
    { key: 'source', label: 'Nguồn', width: '130px', cellClass: 'report-drill-table__center' },
]

/** Ô lọc riêng của popup. `valueOf` đọc giá trị trên dòng; `labelOf` là nhãn. Sales chưa xác định mang id 0 (khớp BE). */
const FILTER_FIELDS = [
    { key: 'type', param: 'type', placeholder: 'Chọn loại', valueOf: (row) => row.type, labelOf: (row) => typeText(row.type) },
    {
        key: 'sales',
        param: 'sales_id',
        placeholder: 'Chọn Sales phụ trách',
        valueOf: (row) => (row.sales_id === null || row.sales_id === undefined ? 0 : row.sales_id),
        labelOf: (row) => row.sales_label || 'Chưa xác định Sales',
    },
    {
        key: 'status',
        param: 'statuses',
        placeholder: 'Chọn tiến trình dự án',
        onlyProject: true,
        valueOf: (row) => (row.type === 'da' ? row.status : null),
        labelOf: (row) => row.status_text,
    },
]

export default {
    name: 'ItemListModal',
    components: { V2BaseReportModal, V2BaseInput, V2BaseSelectInModal, V2BaseButton, V2BaseIconButton, V2BaseBadge },
    mixins: [reportDrillListMixin],
    props: {
        visible: { type: Boolean, default: false },
        loading: { type: Boolean, default: false },
        title: { type: String, default: '' },
        /** Bộ lọc của ô số đã bấm (`type`, `statuses`, `due`, phạm vi) — để ẩn ô lọc đã cố định */
        drill: { type: Object, default: () => ({}) },
        /** TRỌN tập của ô số đã bấm (màn cha tải đủ mọi trang) */
        rows: { type: Array, default: () => [] },
        generatedAt: { type: String, default: '' },
    },
    computed: {
        columns() {
            return COLUMNS
        },
        filterFields() {
            const fixed = this.drill || {}
            return FILTER_FIELDS.filter((f) => {
                if (f.key === 'type') return !fixed.type
                if (f.key === 'status') return fixed.type !== 'nc' && !(fixed.statuses && fixed.statuses.length)
                if (f.key === 'sales') return fixed.sales_id === undefined || fixed.sales_id === null
                return true
            }).map((f) => ({ ...f, options: this.optionsOf(f) }))
        },
        filteredRows() {
            const kw = fold(String(this.keyword || '').trim())
            const active = this.filterFields.filter((f) => this.filters[f.key] !== null && this.filters[f.key] !== undefined && this.filters[f.key] !== '')
            return this.rows.filter((row) => {
                for (const f of active) {
                    if (String(f.valueOf(row)) !== String(this.filters[f.key])) return false
                }
                if (!kw) return true
                return [row.customer_name, row.customer_code, row.code, row.name, row.meeting_code, row.sales_label, row.content].some((v) =>
                    fold(v).includes(kw)
                )
            })
        },
        /** ĐÈ `sortedRows` của mixin -> sắp trên tập ĐÃ LỌC: ô trống xuống cuối, số so số, chữ so tiếng Việt */
        sortedRows() {
            const rows = this.filteredRows
            const { key, dir } = this.sort
            const col = key ? this.columns.find((c) => c.key === key) : null
            if (!col) return rows
            const sign = dir === 'desc' ? -1 : 1
            const valueOf = (row) => {
                const v = row[col.field]
                if (v === null || v === undefined || v === '') return null
                return col.sortType === 'number' ? Number(v) : String(v).trim()
            }
            return rows.slice().sort((a, b) => {
                const va = valueOf(a)
                const vb = valueOf(b)
                if (va === null && vb === null) return 0
                if (va === null) return 1
                if (vb === null) return -1
                return sign * (typeof va === 'number' ? va - vb : va.localeCompare(vb, 'vi'))
            })
        },
        metaText() {
            if (this.loading) return 'Đang tải…'
            const nc = this.rows.filter((r) => r.type === 'nc').length
            const da = this.rows.length - nc
            return [`${num(nc)} nhu cầu · ${num(da)} dự án TKT`, this.generatedAt ? `Đang theo dõi tại ${this.generatedAt}` : ''].filter(Boolean).join(' · ')
        },
    },
    watch: {
        /** Mỗi lượt mở = trạng thái sạch (không mang lọc / sắp / trang của lượt trước) */
        visible(open) {
            if (!open) return
            this.sort = { key: '', dir: 'asc' }
            this.resetFilterState()
        },
    },
    methods: {
        num,
        dmy,
        daysNote,
        typeText,
        emptyFilters() {
            return { type: null, sales: null, status: null }
        },
        onFilterChange() {
            this.page = 1
        },
        /** Danh mục ô lọc lấy distinct từ CHÍNH tập dòng đang xem */
        optionsOf(field) {
            const seen = new Map()
            this.rows.forEach((row) => {
                const id = field.valueOf(row)
                if (id === null || id === undefined || id === '') return
                if (!seen.has(String(id))) seen.set(String(id), { id, name: field.labelOf(row) })
            })
            return Array.from(seen.values()).sort((a, b) => String(a.name).localeCompare(String(b.name), 'vi'))
        },
        /** Bộ lọc đang áp của popup -> tham số BE cho In / Xuất Excel */
        ownParams() {
            const params = {}
            const q = String(this.keyword || '').trim()
            if (q) params.q = q
            this.filterFields.forEach((f) => {
                const v = this.filters[f.key]
                if (v === null || v === undefined || v === '') return
                params[f.param] = f.param === 'statuses' ? [v] : v
            })
            return params
        },
    },
}
</script>

<style lang="scss">
/* KHÔNG scoped: <td> do VỎ render (quy tắc cellClass ở đầu V2BaseReportModal.vue). Vỏ để mọi ô `nowrap` -> tên dài
   kéo bảng tràn ngang; cho các ô chữ xuống dòng. */
.pct-drill-dialog .report-drill-table td.pct-drill-wrap {
    white-space: normal;
}
.pct-drill-dialog .report-drill-table td.report-drill-table__right {
    text-align: right;
    font-variant-numeric: tabular-nums;
}
</style>

<style lang="scss" scoped>
/* Bộ lọc + dòng đếm: khuôn service-demand `DemandListModal.vue` */
$text-main: #1f2937;
$text-muted: #6b7280;

.report-drill-filters {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}
.report-drill-filters__item {
    flex: 0 0 auto;
    width: 210px;
}
.report-drill-filters__item--search {
    width: 280px;
}
.report-drill-filters__item--action {
    width: auto;
}
.report-drill-count {
    margin-left: auto;
    font-size: 12px;
    font-weight: 700;
    color: $text-main;
}
.pct-sub {
    display: block;
    margin-top: 3px;
    font-size: 11px;
    line-height: 1.3;
    color: $text-muted;
}
.pct-link {
    font-size: 12px;
    overflow-wrap: anywhere;
}
.pct-warn {
    color: #b45309;
}
.pct-none {
    color: #c2cbd6;
}
</style>
