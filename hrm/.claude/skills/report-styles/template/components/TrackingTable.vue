<!--
    Bảng cây của báo cáo tổng hợp CSKH tiềm năng — copy khuôn
    `pages/assign/report/service-demand/components/DemandTable.vue` (gốc `pages/sale/prepick-tracking/components/
    TrackingTable.vue`: `.ptr-table`, `.market-table-wrap`, `table.rsum-tb`, caret, vạch cấp, dòng TỔNG, phân trang),
    nội dung theo mockup đã chốt `.plans/gop-db/bao-cao-tong-hop-cskh-tiem-nang/mockup.html`:

      dòng TỔNG · Phòng (d0, I, II…) · Sales (d1, 1, 2…) · Khách hàng (d2, 1.1…) · nhu cầu / dự án (d3, 1.1.1…)

    Khác khuôn CỐ Ý (mockup đã chốt):
      · 4 cấp — CSS cấp 4 (d3) nối tiếp đúng nhịp khuôn (+22px thụt, vạch nhạt dần); d2 nay là dòng CHA nên
        tên chữ đậm màu thường thay vì xám (xám dành cho lá d3).
      · 10 cột -> bảng `min-width` 1654px + `V2BaseTableScroll` (2 thanh cuộn trên/dưới — CLAUDE.md) thay vì
        table-layout fixed vừa khít; tiêu đề cột dính trong vùng cuộn riêng (layout dùng chung `overflow:hidden`).

    `groups` = nhóm PHÒNG của trang hiện tại (BE phân trang theo phòng):
      { key, department_id, department_name, department_code, totals, sales: [{ key, sales_id, sales_name, sales_code,
        totals, customers: [{ key, customer_id, customer_name, customer_code, last_care_date, last_care_days, totals,
        items: [Row] }] }] }
    `totals` = { nc, da, value_nc, value_da }. Nhóm chưa xác định: department_id / sales_id = null (drill gửi 0).

    Phát lên trang cha:
      drill({ type, department_id?, sales_id?, customer_id?, title }) · open-meeting(row) · open-history(customer)
      update:level(1..4) · page-change(page) · page-size-change(size)
-->
<template>
    <div class="ptr-table">
        <div class="market-table-wrap">
            <V2BaseTableScroll max-height="calc(100vh - 200px)" body-class="pct-scroll-body">
                <table class="rsum-tb">
                    <colgroup>
                        <col v-for="col in columns" :key="col.id" :class="`pct-col--${col.id}`" />
                    </colgroup>

                    <thead>
                        <tr class="rsum-tb__head">
                            <th v-for="col in columns" :key="col.id" :class="col.cls" :data-col="col.id">
                                <span v-if="col.id === 'name'" class="rsum-tb__th">
                                    <span class="rsum-tb__th-label">{{ col.label }}</span>
                                    <span class="rsum-tb__level-wrap" title="Chọn cấp muốn bung sẵn trong bảng">
                                        <V2BaseSelect
                                            :value="level"
                                            :options="levelOptions"
                                            :allow-clear="false"
                                            size="xs"
                                            @change="onLevelChange"
                                        />
                                    </span>
                                </span>
                                <template v-else>
                                    {{ col.label }}<InfoTip v-if="col.tip" :head="col.tip.head" :lines="col.tip.lines" />
                                </template>
                            </th>
                        </tr>
                    </thead>

                    <tbody>
                        <!-- Dòng TỔNG — từ `summary` (toàn bộ dữ liệu đã lọc), KHÔNG theo trang -->
                        <tr class="rsum-tb__sec">
                            <td class="rsum-tb__no">TỔNG</td>
                            <td class="rsum-tb__name">
                                Phòng / Sales / Khách hàng / Nội dung<InfoTip
                                    head="PHÒNG / SALES / KHÁCH HÀNG"
                                    :lines="[
                                        'Phòng / công ty lấy theo nơi Sales ĐANG làm việc tại thời điểm xem',
                                        'Mỗi dòng lá là 1 nhu cầu hoặc 1 dự án TKT; nhu cầu xếp trước',
                                        'Việc chưa có Sales gom vào nhóm “Chưa xác định” ở cuối',
                                        'Dòng TỔNG tính trên toàn bộ dữ liệu đã lọc, không theo trang',
                                    ]"
                                />
                            </td>
                            <td class="rsum-tb__cnt"><CountPair :totals="summary" :scope="{}" label="toàn bộ báo cáo" @drill="emitDrill" /></td>
                            <td></td>
                            <td class="rsum-tb__num">{{ money(summary && summary.value_nc) }}</td>
                            <td class="rsum-tb__num">{{ money(summary && summary.value_da) }}</td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                        </tr>

                        <template v-for="row in flatRows">
                            <!-- Dòng CHA: Phòng (d0) · Sales (d1) · Khách hàng (d2) -->
                            <tr
                                v-if="row.kind !== 'leaf'"
                                :key="row.key"
                                :class="[`rsum-tb__row--d${row.depth}`, 'rsum-tb__row--parent', { 'rsum-tb__row--open': row.open }]"
                                :data-key="row.key"
                            >
                                <td class="rsum-tb__no">{{ row.no }}</td>
                                <td :class="['rsum-tb__name', `rsum-tb__name--d${row.depth}`]" :title="row.name">
                                    <!-- `<button>` thô CỐ Ý — mũi tên bung/thu cấp cây (khuôn TrackingTable) -->
                                    <button
                                        type="button"
                                        class="rsum-caret"
                                        :class="{ 'rsum-caret--open': row.open }"
                                        :title="(row.open ? 'Ẩn ' : 'Hiện ') + row.childLabel"
                                        @click="toggle(row.key)"
                                    >
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                            <polyline points="6 9 12 15 18 9"></polyline>
                                        </svg>
                                    </button>
                                    <i v-if="row.unknown">{{ row.name }}</i>
                                    <template v-else>{{ row.name }}</template>
                                    <span v-if="row.code" class="code-sub">{{ row.code }}</span>
                                </td>
                                <td class="rsum-tb__cnt"><CountPair :totals="row.totals" :scope="row.scope" :label="row.name" @drill="emitDrill" /></td>
                                <td></td>
                                <td class="rsum-tb__num">{{ money(row.totals.value_nc) }}</td>
                                <td class="rsum-tb__num">{{ money(row.totals.value_da) }}</td>
                                <td></td>
                                <td></td>
                                <td class="rsum-tb__txt">
                                    <template v-if="row.depth === 2">
                                        <template v-if="row.customer.last_care_date">
                                            <!-- Ngày chăm sóc bấm được -> popup lịch sử meeting có sẵn của báo cáo CSKH tiềm năng -->
                                            <DrillNum
                                                :value="1"
                                                :text="dmy(row.customer.last_care_date)"
                                                title="Xem lịch sử meeting với khách hàng"
                                                @click="$emit('open-history', row.customer)"
                                            />
                                            <span class="unit-sub">{{ num(row.customer.last_care_days) }} ngày</span>
                                        </template>
                                        <span v-else class="rsum-tb__zero">Chưa có meeting</span>
                                    </template>
                                </td>
                                <td></td>
                            </tr>

                            <!-- Dòng LÁ (d3): 1 nhu cầu hoặc 1 dự án TKT -->
                            <tr v-else :key="row.key" class="rsum-tb__row--d3" :data-key="row.key">
                                <td class="rsum-tb__no">{{ row.no }}</td>
                                <td class="rsum-tb__name rsum-tb__name--d3" :title="row.item.content">
                                    <template v-if="row.item.type === 'da'">
                                        <a
                                            :href="`/assign/prospective-projects/${row.item.id}`"
                                            target="_blank"
                                            rel="noopener"
                                            class="v2-cell-link pct-link"
                                            :title="'Mở dự án ' + row.item.code + ' ở tab mới'"
                                            >{{ row.item.code }}</a
                                        ><span class="prd-sep">-</span>{{ row.item.name }}
                                    </template>
                                    <template v-else>{{ row.item.content }}</template>
                                </td>
                                <td class="rsum-tb__txt">{{ typeText(row.item.type) }}</td>
                                <td class="rsum-tb__txt">
                                    <V2BaseBadge :color="row.item.status_color">{{ row.item.status_text }}</V2BaseBadge>
                                </td>
                                <td class="rsum-tb__num">{{ row.item.type === 'nc' ? money(row.item.value) : '' }}</td>
                                <td class="rsum-tb__num">{{ row.item.type === 'da' ? money(row.item.value) : '' }}</td>
                                <td class="rsum-tb__txt" :title="row.item.type === 'nc' ? 'Ngày dự kiến triển khai' : 'Ngày khách hàng cần giải pháp'">
                                    {{ dmy(row.item.milestone_date) }}
                                </td>
                                <td class="rsum-tb__txt">
                                    <template v-if="row.item.type === 'nc'">
                                        <template v-if="row.item.due_date">
                                            <span :class="{ 'pct-warn': row.item.is_due_soon }">{{ dmy(row.item.due_date) }}</span>
                                            <span class="unit-sub" :class="{ 'pct-warn': row.item.is_due_soon }">{{ daysNote(row.item.due_days_left) }}</span>
                                        </template>
                                        <span v-else class="rsum-tb__zero">Không có hạn</span>
                                    </template>
                                </td>
                                <td></td>
                                <td class="rsum-tb__txt">
                                    <a
                                        v-if="row.item.meeting_code"
                                        href="#"
                                        class="v2-cell-link pct-link"
                                        :title="'Xem meeting ' + row.item.meeting_code"
                                        @click.prevent="$emit('open-meeting', row.item)"
                                        >{{ row.item.meeting_code }}</a
                                    >
                                </td>
                            </tr>
                        </template>

                        <tr v-if="!flatRows.length" class="rsum-tb__row--muted">
                            <td class="rsum-tb__no"></td>
                            <td class="rsum-tb__name" :colspan="columns.length - 1">Không có nhu cầu / dự án nào khớp bộ lọc.</td>
                        </tr>
                    </tbody>
                </table>
            </V2BaseTableScroll>
        </div>

        <!-- Phân trang theo NHÓM PHÒNG (BE phân trang theo phòng) — bung/thu không đẩy nội dung sang trang khác -->
        <V2BasePagination
            v-if="pagination"
            :current-page="Number(pagination.current_page) || 1"
            :current-page-size="Number(pagination.per_page) || 20"
            :total-rows="Number(pagination.total) || 0"
            item-label="phòng ban"
            :page-size-options="[10, 20, 50, 100]"
            @page-change="(p) => $emit('page-change', Number(p))"
            @page-size-change="(s) => $emit('page-size-change', Number(s))"
        />
    </div>
</template>

<script>
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BasePagination from '@/components/V2BasePagination.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import V2BaseTableScroll from '@/components/V2BaseTableScroll.vue'
import DrillNum from './DrillNum.vue'
import InfoTip from './InfoTip.vue'
import { num, dmy, daysNote, typeText } from '../format'

/**
 * Ô "Loại" của dòng cha: "2 NC · 1 DA" — 2 số bấm được (mockup điểm UI #3); 0 -> chữ mờ.
 * `scope` = bộ lọc phạm vi của dòng (department_id / sales_id / customer_id) ghép vào drill.
 */
const CountPair = {
    name: 'CountPair',
    props: {
        totals: { type: Object, default: null },
        scope: { type: Object, default: () => ({}) },
        label: { type: String, default: '' },
    },
    render(h) {
        const t = this.totals || {}
        const part = (type, unit, what) => {
            const v = Number(t[type]) || 0
            const numEl = v
                ? h(DrillNum, {
                      props: { value: v, text: num(v), title: `Xem ${what}: ${this.label}` },
                      on: { click: () => this.$emit('drill', { ...this.scope, type, title: `${this.label} · ${what}` }) },
                  })
                : h('span', { class: 'rsum-tb__zero' }, '0')
            return [numEl, h('span', { class: 'unit-sub' }, unit)]
        }
        return h('span', { class: 'rsum-tb__count' }, [...part('nc', 'NC', 'nhu cầu'), h('span', { class: 'pct-dot' }, '·'), ...part('da', 'DA', 'dự án TKT')])
    },
}

const COLS = [
    { id: 'no', label: 'STT', cls: 'rsum-tb__no' },
    { id: 'name', label: 'Nội dung theo dõi', cls: 'rsum-tb__name' },
    {
        id: 'type',
        label: 'Loại',
        cls: 'rsum-tb__txt',
        tip: { head: 'LOẠI', lines: ['Dòng cha: số nhu cầu (NC) · số dự án TKT (DA) — bấm số để xem danh sách', 'Dòng lá: Nhu cầu hoặc Dự án TKT'] },
    },
    { id: 'status', label: 'Trạng thái', cls: 'rsum-tb__txt' },
    {
        id: 'vnc',
        label: 'Giá trị nhu cầu',
        cls: 'rsum-tb__num',
        tip: { head: 'GIÁ TRỊ NHU CẦU', lines: ['Giá trị dự kiến khách hàng đầu tư, ghi ở biên bản meeting'] },
    },
    {
        id: 'vda',
        label: 'Giá trị dự án',
        cls: 'rsum-tb__num',
        tip: { head: 'GIÁ TRỊ DỰ ÁN', lines: ['Giá trị hợp đồng dự kiến của dự án TKT'] },
    },
    {
        id: 'milestone',
        label: 'Mốc thời gian',
        cls: 'rsum-tb__txt',
        tip: { head: 'MỐC THỜI GIAN', lines: ['Nhu cầu: ngày dự kiến triển khai', 'Dự án TKT: ngày khách hàng cần giải pháp'] },
    },
    {
        id: 'due',
        label: 'Hạn theo dõi',
        cls: 'rsum-tb__txt',
        tip: {
            head: 'HẠN THEO DÕI',
            lines: [
                'Hạn tự đóng nhu cầu = ngày hoàn thành meeting + thời gian hiệu lực của lĩnh vực',
                'Màu cam: đã vào số ngày cảnh báo trước khi đóng',
                'Không có hạn: lĩnh vực chưa đặt thời gian hiệu lực, nhu cầu không tự đóng',
            ],
        },
    },
    {
        id: 'care',
        label: 'Lần chăm sóc gần nhất',
        cls: 'rsum-tb__txt',
        tip: {
            head: 'LẦN CHĂM SÓC GẦN NHẤT',
            lines: ['Meeting Hoàn thành gần nhất với khách hàng (bất kỳ ai chủ trì) và số ngày tới hôm nay', 'Bấm ngày để xem lịch sử meeting'],
        },
    },
    {
        id: 'source',
        label: 'Nguồn',
        cls: 'rsum-tb__txt',
        tip: { head: 'NGUỒN', lines: ['Meeting thu thập nhu cầu', 'Với dự án TKT: meeting của nhu cầu gốc (nếu dự án lập từ nhu cầu)'] },
    },
]

const ROMAN = [
    ['M', 1000],
    ['CM', 900],
    ['D', 500],
    ['CD', 400],
    ['C', 100],
    ['XC', 90],
    ['L', 50],
    ['XL', 40],
    ['X', 10],
    ['IX', 9],
    ['V', 5],
    ['IV', 4],
    ['I', 1],
]
function roman(n) {
    let out = ''
    let x = n
    ROMAN.forEach(([r, v]) => {
        while (x >= v) {
            out += r
            x -= v
        }
    })
    return out
}

export default {
    name: 'TrackingTable',
    components: { V2BaseSelect, V2BasePagination, V2BaseBadge, V2BaseTableScroll, DrillNum, InfoTip, CountPair },
    props: {
        groups: { type: Array, default: () => [] },
        /** `summary` của BE — nuôi dòng TỔNG */
        summary: { type: Object, default: null },
        /** 1 Chỉ Phòng ban · 2 Đến Sales · 3 Đến Khách hàng · 4 Tất cả cấp (chỉ là cách xem, không gọi API) */
        level: { type: Number, default: 2 },
        /** { total, per_page, current_page } — phân trang theo nhóm phòng */
        pagination: { type: Object, default: null },
    },
    data() {
        return {
            columns: COLS,
            /** key dòng cha -> true: đang bung. Một nguồn cho cả ô chọn cấp lẫn mũi tên từng dòng. */
            expanded: {},
            levelOptions: [
                { id: 1, name: 'Chỉ Phòng ban' },
                { id: 2, name: 'Đến Sales' },
                { id: 3, name: 'Đến Khách hàng' },
                { id: 4, name: 'Tất cả cấp (đến Nhu cầu / Dự án)' },
            ],
        }
    },
    computed: {
        offset() {
            const p = this.pagination || {}
            return ((Number(p.current_page) || 1) - 1) * (Number(p.per_page) || 0)
        },
        flatRows() {
            const out = []
            ;(this.groups || []).forEach((g, gi) => {
                const dKey = this.deptKey(g)
                const deptId = g.department_id === null || g.department_id === undefined ? 0 : g.department_id
                const dOpen = !!this.expanded[dKey]
                out.push({
                    kind: 'parent',
                    depth: 0,
                    key: dKey,
                    no: roman(this.offset + gi + 1),
                    name: g.department_id ? g.department_name : 'Chưa xác định phòng',
                    code: g.department_id ? g.department_code : '',
                    unknown: !g.department_id,
                    totals: g.totals || {},
                    scope: { department_id: deptId },
                    childLabel: 'Sales',
                    open: dOpen,
                })
                if (!dOpen) return
                ;(g.sales || []).forEach((s, si) => {
                    const sKey = `${dKey}/${s.key}`
                    const salesId = s.sales_id === null || s.sales_id === undefined ? 0 : s.sales_id
                    const sOpen = !!this.expanded[sKey]
                    out.push({
                        kind: 'parent',
                        depth: 1,
                        key: sKey,
                        no: String(si + 1),
                        name: s.sales_id ? s.sales_name : 'Chưa xác định Sales',
                        code: s.sales_id ? s.sales_code : '',
                        unknown: !s.sales_id,
                        totals: s.totals || {},
                        scope: { department_id: deptId, sales_id: salesId },
                        childLabel: 'khách hàng',
                        open: sOpen,
                    })
                    if (!sOpen) return
                    ;(s.customers || []).forEach((c, ci) => {
                        const cKey = `${sKey}/${c.key}`
                        const cNo = `${si + 1}.${ci + 1}`
                        const cOpen = !!this.expanded[cKey]
                        out.push({
                            kind: 'parent',
                            depth: 2,
                            key: cKey,
                            no: cNo,
                            name: c.customer_name || '',
                            code: c.customer_code || '',
                            unknown: false,
                            totals: c.totals || {},
                            scope: { department_id: deptId, sales_id: salesId, customer_id: c.customer_id },
                            customer: c,
                            childLabel: 'nhu cầu / dự án',
                            open: cOpen,
                        })
                        if (!cOpen) return
                        ;(c.items || []).forEach((item, ii) => {
                            out.push({ kind: 'leaf', depth: 3, key: `${cKey}/${item.type}:${item.id}`, no: `${cNo}.${ii + 1}`, item })
                        })
                    })
                })
            })
            return out
        },
    },
    watch: {
        // Dữ liệu mới (đổi lọc / trang) -> áp lại đúng cấp đang chọn
        groups: {
            handler() {
                this.applyLevel()
            },
            immediate: true,
        },
        level() {
            this.applyLevel()
        },
    },
    methods: {
        num,
        dmy,
        daysNote,
        typeText,
        money(v) {
            const n = Number(v) || 0
            return n ? num(n) : '0'
        },
        deptKey(g) {
            return `dept:${g.department_id || 0}`
        },
        applyLevel() {
            const lv = Number(this.level)
            const next = {}
            ;(this.groups || []).forEach((g) => {
                const dKey = this.deptKey(g)
                if (lv >= 2) next[dKey] = true
                ;(g.sales || []).forEach((s) => {
                    const sKey = `${dKey}/${s.key}`
                    if (lv >= 3) next[sKey] = true
                    ;(s.customers || []).forEach((c) => {
                        if (lv >= 4) next[`${sKey}/${c.key}`] = true
                    })
                })
            })
            this.expanded = next
        },
        toggle(key) {
            const next = { ...this.expanded }
            if (next[key]) delete next[key]
            else next[key] = true
            this.expanded = next
        },
        onLevelChange(value) {
            const v = Number(value)
            if (!v || v === this.level) return
            this.$emit('update:level', v)
        },
        emitDrill(payload) {
            this.$emit('drill', payload)
        },
    },
}
</script>

<style lang="scss" scoped>
/* Copy từ `service-demand/components/DemandTable.vue` (gốc prepick-tracking TrackingTable.vue) — chỉ giữ phần bảng
   này dùng + phần cấp 4 / cuộn ngang đúng khối `mk-extra-css` của mockup đã chốt. */
$teal-header: #20d9ea;
$teal-dark: #0e7490;
$text-main: #1f2937;
$text-muted: #6b7280;

.ptr-table {
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(10, 28, 61, 0.08);
    padding: 18px;
}

/* Khung viền của bảng. Cuộn NGANG + DỌC nằm ở `V2BaseTableScroll` bên trong (2 thanh cuộn trên/dưới; thân cuộn
   dọc riêng vì `.content-page` của layout dùng chung có `overflow: hidden` nên `th` sticky theo trang không ghim
   được — khuôn service-demand đã đo). */
.market-table-wrap {
    border: 1px solid #e3e8ef;
    border-radius: 10px;
}
.market-table-wrap ::v-deep .pct-scroll-body {
    min-height: 240px;
}

.rsum-tb {
    width: 100%;
    /* 10 cột: cột Nội dung giữ ≥ 420px, phần còn lại cố định -> tràn thì cuộn ngang (mockup) */
    min-width: 1654px;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 12.5px;
    table-layout: fixed;
    background: #fff;

    th,
    td {
        padding: 7px 10px;
        border-right: 1px solid #e2eaf1;
        border-bottom: 1px solid #e2eaf1;
        vertical-align: middle;
        transition: background 0.12s ease;
        white-space: nowrap;
    }
}

/* Tiêu đề cột — ghim ở đỉnh vùng cuộn riêng của bảng */
.rsum-tb__head th {
    position: sticky;
    top: 0;
    z-index: 2;
    background: linear-gradient(180deg, #f3fdfe, #e2f6f9);
    border-color: rgba(32, 217, 234, 0.4);
    border-top: 1px solid rgba(32, 217, 234, 0.4);
    border-bottom: 2px solid $teal-header;
    color: #0a7c88;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0;
    line-height: 1.3;
    text-transform: none;
    text-align: left;
    vertical-align: middle;
}
.rsum-tb__head th.rsum-tb__no {
    text-align: center;
}
.rsum-tb__head th.rsum-tb__num {
    text-align: right;
}

/* ---- Bề rộng cột — mockup đã chốt (STT 64 · Nội dung auto ≥ 420 · 130 · 190 · 130 · 130 · 120 · 160 · 170 · 130) ---- */
.pct-col--no {
    width: 64px;
}
.pct-col--type {
    width: 130px;
}
.pct-col--status {
    width: 190px;
}
.pct-col--vnc,
.pct-col--vda {
    width: 130px;
}
.pct-col--milestone {
    width: 120px;
}
.pct-col--due {
    width: 160px;
}
.pct-col--care {
    width: 170px;
}
.pct-col--source {
    width: 130px;
}

/* Ô "Nội dung theo dõi": nhãn + ô chọn cấp bung */
.rsum-tb__head th.rsum-tb__name {
    padding-top: 5px;
    padding-bottom: 5px;
}
.rsum-tb__th {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 2px 10px;
}
.rsum-tb__th-label {
    white-space: nowrap;
}
.rsum-tb__level-wrap {
    flex: 0 1 230px;
    min-width: 0;
}
.rsum-tb__level-wrap ::v-deep .select2-selection__rendered {
    font-size: 11px;
    font-weight: 400;
    color: $text-main;
    text-transform: none;
}

/* Dòng TỔNG — tông cam */
.rsum-tb__sec td {
    background: #fdf1ea;
    border-top: 2px solid #c2703a;
    color: #9a5326;
    font-weight: 400;
    height: 36px;
}
.rsum-tb__sec .rsum-tb__name {
    text-transform: uppercase;
    letter-spacing: 0.2px;
}
.rsum-tb__sec .rsum-tb__cnt ::v-deep .unit-sub {
    color: #b07a55;
}
.rsum-tb tbody tr.rsum-tb__sec:hover td {
    background: #fdf1ea;
}

.rsum-caret {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    margin-right: 6px;
    margin-left: -24px;
    padding: 0;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    background: #fff;
    color: $text-muted;
    cursor: pointer;
    vertical-align: -4px;

    &:hover {
        border-color: $teal-dark;
        color: $teal-dark;
        background: rgba(6, 182, 212, 0.08);
    }

    svg {
        width: 11px;
        height: 11px;
        transform: rotate(-90deg);
        transition: transform 0.15s ease;
    }
}
.rsum-caret--open svg {
    transform: rotate(0deg);
}

.rsum-tb__no {
    text-align: center;
    color: $text-muted;
}
.rsum-tb__name {
    color: $text-main;
    line-height: 1.35;
    overflow: hidden;
    text-overflow: ellipsis;
}
.rsum-tb__txt {
    color: $text-main;
    line-height: 1.35;
}
.rsum-tb__num {
    text-align: right;
    color: $text-main;
    font-variant-numeric: tabular-nums;
}
.rsum-tb__cnt {
    font-variant-numeric: tabular-nums;
}
/* `CountPair` là component render-function khai trong file này -> phần tử con KHÔNG mang scope id, chọn qua ::v-deep */
.rsum-tb__zero,
.rsum-tb__cnt ::v-deep .rsum-tb__zero {
    color: #c2cbd6;
}
.rsum-tb__row--muted td {
    color: $text-muted;
    font-style: italic;
}

/* Đơn vị sau con số ("NC", "DA", "ngày") — `text-transform: none` BẮT BUỘC (dòng TỔNG viết hoa) */
.unit-sub,
.rsum-tb__cnt ::v-deep .unit-sub {
    margin-left: 4px;
    font-size: 10.5px;
    font-weight: 400;
    color: $text-muted;
    text-transform: none;
}
.rsum-tb__cnt ::v-deep .pct-dot {
    margin: 0 6px;
    color: $text-muted;
}
/* Mã phòng / NV / KH in mờ sau tên, chữ THƯỜNG */
.code-sub {
    margin-left: 6px;
    font-size: 10.5px;
    font-weight: 400;
    color: $text-muted;
    text-transform: none;
}
.prd-sep {
    margin: 0 4px;
    color: $text-muted;
}
.pct-link {
    font-size: 12px;
}
/* Hạn đã vào vùng cảnh báo — tông cam của khuôn (`rsum-tb__soon` #b45309) */
.pct-warn,
.unit-sub.pct-warn {
    color: #b45309;
}

/* ---- Thụt lề theo ĐỘ SÂU (+22px mỗi cấp) ---- */
.rsum-tb td.rsum-tb__name--d0 {
    padding-left: 30px;
}
.rsum-tb td.rsum-tb__name--d1 {
    padding-left: 52px;
}
.rsum-tb td.rsum-tb__name--d2 {
    padding-left: 74px;
}
.rsum-tb td.rsum-tb__name--d3 {
    padding-left: 96px;
}

.rsum-tb__row--d1 td {
    background: #f7fbfd;
}
.rsum-tb__row--d2 td {
    background: #fafcfe;
}
.rsum-tb__row--d3 td {
    background: #fff;
}
.rsum-tb__row--d3 .rsum-tb__name {
    color: $text-muted;
}
.rsum-tb__row--d3 .rsum-tb__no {
    font-size: 11px;
}
.rsum-tb__row--d0.rsum-tb__row--open td {
    background: #dceaf4;
}
.rsum-tb__row--d1.rsum-tb__row--open td {
    background: #e9f3f9;
}
.rsum-tb__row--d2.rsum-tb__row--open td {
    background: #f1f8fb;
}

/* Vạch cấp bên trái ô tên — ::before tuyệt đối, KHÔNG border-left của td */
.rsum-tb td[class*='rsum-tb__name--d'] {
    position: relative;
}
.rsum-tb td[class*='rsum-tb__name--d']::before {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    width: 2px;
    border-radius: 1px;
}
.rsum-tb td.rsum-tb__name--d0::before {
    left: 2px;
    width: 3px;
    background: #0a7c88;
}
.rsum-tb td.rsum-tb__name--d1::before {
    left: 24px;
    background: rgba(10, 124, 136, 0.55);
}
.rsum-tb td.rsum-tb__name--d2::before {
    left: 46px;
    background: rgba(10, 124, 136, 0.32);
}
.rsum-tb td.rsum-tb__name--d3::before {
    left: 68px;
    background: rgba(10, 124, 136, 0.2);
}

/* Kẻ đậm phía trên mỗi dòng phòng — cắt khối giữa các phòng */
.rsum-tb__row--d0 td {
    border-top: 2px solid #b6d8e0;
    height: 36px;
}
.rsum-tb tbody tr.rsum-tb__row--d0:hover td,
.rsum-tb tbody tr.rsum-tb__row--d1:hover td,
.rsum-tb tbody tr.rsum-tb__row--d2:hover td,
.rsum-tb tbody tr.rsum-tb__row--d3:hover td {
    background: #d9eff7;
}
</style>
