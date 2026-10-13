<!--
    Báo cáo tổng hợp chăm sóc khách hàng tiềm năng (feature bao-cao-tong-hop-cskh-tiem-nang, menu CSKH trước bán ›
    Báo cáo thị trường). Ảnh chụp TẠI THỜI ĐIỂM XEM — không có kỳ — các nhu cầu làm dự án còn Đang theo dõi và dự án
    TKT tiến trình 2 → 9, theo Phòng ▸ Sales ▸ Khách hàng.

    Khuôn: `pages/assign/report/service-demand/index.vue` (gốc `pages/sale/prepick-tracking`): SmartFilterPanel floating
    + `.rsum` 2 khối + bảng cây `rsum-tb` — mockup đã chốt `.plans/gop-db/bao-cao-tong-hop-cskh-tiem-nang/mockup.html`.
      · `onDrill(filter)`        — popup danh sách `ItemListModal` (V2BaseReportModal)
      · `onOpenMeeting(row)`     — panel chi tiết meeting (WorkItemDetailDrawer) + khối thông tin của dòng
      · `onOpenHistory(customer)`— popup lịch sử meeting CÓ SẴN của báo cáo kết quả CSKH tiềm năng
      · `onPrint()` / `onExport()` — In danh sách (chọn bản in -> xem trước) / Xuất Excel
    In / Excel / popup đều dùng `drillBaseParams()` = bộ lọc của báo cáo ĐANG HIỂN THỊ.

    Phạm vi: mọi user đăng nhập vào được màn; BE tự áp quyền 3 cấp (tổng công ty / công ty / phòng ban / việc của mình).
    `can_change_company` của BE quyết định ô Công ty có mở hay bị khoá — FE KHÔNG tự suy từ store.
-->
<template>
    <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
        <div class="container-fluid">
            <V2BaseSmartFilterPanel
                table="assign_potential_customer_tracking_report"
                floating
                :filter-fields="filterFields"
                :filters="filters"
                :collapsed="filterCollapsed"
                :show-quick-search="false"
                title="Bộ lọc báo cáo tổng hợp CSKH tiềm năng"
                reset-button-text="Xóa lọc"
                @toggle-panel="filterCollapsed = !filterCollapsed"
                @filter-change="({ key, value }) => onFilterChange(key, value)"
                @search="onSearch"
                @reset="handleReset"
            >
                <template #title-suffix>
                    <InfoTip
                        head="MỤC ĐÍCH BÁO CÁO"
                        :lines="[
                            'Xem tại thời điểm mở báo cáo mỗi Sales đang theo dõi những nhu cầu và dự án TKT nào',
                            'Nhu cầu: còn Đang theo dõi · Dự án TKT: chưa Đóng / chưa hoàn thành',
                            'Xem theo Phòng ▸ Sales ▸ Khách hàng; mỗi dòng lá là 1 nhu cầu hoặc 1 dự án',
                        ]"
                    />
                </template>

                <!-- Nút trong slot `header-actions` KHÔNG khai lề: panel tự cách đều 12px bằng `gap`.
                     Màu theo `.claude/skills/button-convention` mục 2b: Xuất Excel `secondary status="success"`. -->
                <template #header-actions>
                    <V2BaseButton secondary size="sm" class="btn-compact" @click="onPrint">
                        <template #prefix><i class="ri-printer-line" style="font-size: 13px"></i></template>
                        In danh sách
                    </V2BaseButton>
                    <V2BaseButton secondary status="success" size="sm" class="btn-compact" @click="onExport">
                        <template #prefix><i class="ri-file-excel-2-line" style="font-size: 13px"></i></template>
                        Xuất Excel
                    </V2BaseButton>
                </template>

                <!-- CÔNG TY — công ty nơi SALES đang làm việc. Không có quyền tổng công ty (`can_change_company = false`)
                     thì ô bị KHOÁ ở công ty của mình (BE cũng bỏ qua `company_id`). Có quyền: để trống = tất cả công ty. -->
                <template #field-company_id>
                    <V2BaseFloatingField
                        label="Công ty"
                        :hint="hints.org"
                        :has-value="!!filters.company_id"
                        :disabled="!canChangeCompany"
                        class="pct-company"
                    >
                        <V2BaseSelect
                            :key="`company-${canChangeCompany}`"
                            :value="filters.company_id"
                            :options="companyOptions"
                            :disabled="!canChangeCompany"
                            :allowClear="canChangeCompany"
                            size="sm"
                            height="32px"
                            @input="(v) => onFilterChange('company_id', v)"
                        />
                    </V2BaseFloatingField>
                </template>

                <!-- KHÁCH HÀNG — danh mục đã giới hạn theo quyền (filter-options), lọc tại FE theo từ khoá; tối thiểu 2 ký
                     tự như mọi ô tìm khách hàng. `height="32px"` bắt buộc (updateHeight() ghi inline !important). -->
                <template #field-customer_id>
                    <V2BaseSelectRemote
                        v-model="filters.customer_id"
                        :fetchFn="searchCustomers"
                        :initialOption="selectedCustomer"
                        :minimumInputLength="2"
                        :allowClear="true"
                        placeholder="Gõ tối thiểu 2 ký tự"
                        size="sm"
                        height="32px"
                        @select="onCustomerSelect"
                    />
                </template>
            </V2BaseSmartFilterPanel>

            <div class="pct-body" :class="{ 'pct-body--loading': loading }">
                <TrackingSummary
                    v-if="report"
                    :summary="report.summary"
                    :generated-at="report.generated_at"
                    :statuses="options.statuses"
                    @drill="onDrill"
                />
                <TrackingTable
                    v-if="report"
                    :groups="report.groups || []"
                    :summary="report.summary"
                    :level="level"
                    :pagination="report.meta"
                    @drill="onDrill"
                    @open-meeting="onOpenMeeting"
                    @open-history="onOpenHistory"
                    @update:level="(v) => (level = v)"
                    @page-change="onPageChange"
                    @page-size-change="onPageSizeChange"
                />
            </div>

            <ItemListModal
                :visible="drill.visible"
                :loading="drill.loading"
                :title="drill.title"
                :drill="drill.filter"
                :rows="drill.rows"
                :generated-at="report ? report.generated_at : ''"
                @open-meeting="onOpenMeeting"
                @print="printItemList"
                @export="exportItemList"
                @close="drill.visible = false"
            />

            <!-- Popup lịch sử meeting với khách hàng — DÙNG LẠI của báo cáo kết quả CSKH tiềm năng (spec #12): meeting
                 Hoàn thành, cũ → mới, quyền theo báo cáo đó. -->
            <CustomerMeetingHistoryModal
                :visible="customerHistory.show"
                :customer="customerHistory.row"
                @view-report="openMeetingReport"
                @close="customerHistory.show = false"
            />

            <!-- Panel chi tiết meeting — component dùng chung của Lịch của tôi. Mở từ popup thì `above-modal` nâng panel
                 lên trên `.modal` (1050); đầu panel dùng gradient của đầu popup báo cáo. -->
            <MeetingDetailDrawer
                :show="meetingDrawer.show"
                :item="{ type: 'meeting', id: meetingDrawer.id }"
                :above-modal="drill.visible"
                :extra-blocks="meetingDrawerBlocks"
                header-gradient="linear-gradient(135deg, #0a1c3d, #06b6d4)"
                @close="meetingDrawer.show = false"
                @edit="goEditMeeting"
                @view-report="openMeetingReport"
            />

            <!-- Popup IN DÙNG CHUNG (quy tắc in — SKILL.md mục 4b): "In báo cáo" = chọn bản in + cột; "In danh sách" của
                 popup drill = chỉ chọn cột (`drillPrint`). 1 instance cho cả 2. -->
            <V2BaseReportPrintModal
                id="pct-print-options-modal"
                :visible="printOptions"
                :modes="drillPrint ? [] : printModes"
                :columns="drillPrint ? drillPrint.columns : []"
                @print="onPrintChosen"
                @close="closePrintOptions"
            />

            <ReportPrintPreviewModal
                :show="printPreview.show"
                :html="printPreview.html"
                :loading="printPreview.loading"
                :error="printPreview.error"
                :title="printPreview.title"
                :landscape="printPreview.landscape"
                :notice="printPreview.notice"
                @close="printPreview.show = false"
            />
        </div>
    </div>
</template>

<script>
import V2BaseSmartFilterPanel from '@/components/V2BaseSmartFilterPanel.vue'
import V2BaseFloatingField from '@/components/V2BaseFloatingField.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseSelectRemote from '@/components/V2BaseSelectRemote.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import ReportPrintPreviewModal from '@/components/print/ReportPrintPreviewModal.vue'
import MeetingDetailDrawer from '@/pages/assign/my-todo/components/calendar/WorkItemDetailDrawer.vue'
import CustomerMeetingHistoryModal from '@/pages/assign/report/potential-customer-care/components/CustomerMeetingHistoryModal.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'
import reportPrintPreviewMixin from '@/utils/mixins/reportPrintPreviewMixin'
import { buildQueryString } from '@/utils/url-action'
import TrackingSummary from './components/TrackingSummary.vue'
import TrackingTable from './components/TrackingTable.vue'
import ItemListModal from './components/ItemListModal.vue'
import V2BaseReportPrintModal from '@/components/report/V2BaseReportPrintModal.vue'
import InfoTip from './components/InfoTip.vue'
import { API } from './api'
import { num, dmy, daysNote } from './format'

/** `item-list` trần 500 dòng/lượt — popup lọc tại chỗ nên tải đủ mọi trang */
const DRILL_PAGE_SIZE = 500

/** Mã lỗi mà interceptor chung `plugins/axios.js` đã tự toast — màn không toast thêm. */
const INTERCEPTOR_TOAST_CODES = [401, 403, 500, 504]

function initialFilters(companyId = null) {
    return {
        company_id: companyId,
        department_id: null,
        sales_id: null,
        customer_id: null,
        type: null,
        statuses: [],
        scope_id: null,
        due: null,
    }
}

/** Ô lọc chọn -> danh mục của nó trong filter-options (giữ mục đang chọn khi danh mục đổi) */
const SELECTED_OPTION_LISTS = {
    company_id: 'companies',
    department_id: 'departments',
    sales_id: 'sales',
    customer_id: 'customers',
    scope_id: 'scopes',
}

export default {
    layout: 'default-sidebar',
    head() {
        return { title: 'Báo cáo tổng hợp CSKH tiềm năng' }
    },
    components: {
        V2BaseSmartFilterPanel,
        V2BaseFloatingField,
        V2BaseSelect,
        V2BaseSelectRemote,
        V2BaseButton,
        TrackingSummary,
        TrackingTable,
        ItemListModal,
        V2BaseReportPrintModal,
        ReportPrintPreviewModal,
        MeetingDetailDrawer,
        CustomerMeetingHistoryModal,
        InfoTip,
    },
    mixins: [PageTitleMixin, reportPrintPreviewMixin],
    data() {
        return {
            filters: initialFilters(),
            // Nhãn KH đang chọn — nuôi initialOption của select tìm, để NGOÀI `filters` để không gửi khoá hiển thị lên BE
            selectedCustomer: null,
            // Mặc định "Đến Sales" (mockup: mở cấp Phòng, đóng từ cấp Sales)
            level: 2,
            page: 1,
            perPage: 20,
            options: {
                companies: [],
                departments: [],
                sales: [],
                customers: [],
                scopes: [],
                statuses: [],
                types: [],
                dues: [],
            },
            // Fail-closed: chỉ bật từ `can_change_company` của BE, KHÔNG BAO GIỜ gán literal true.
            canChangeCompany: false,
            report: null,
            // Bản chụp params của lần tải `report` thành công gần nhất — In / Excel / popup PHẢI dùng đúng bộ lọc đang hiển thị
            reportParams: null,
            loading: false,
            filterCollapsed: false,
            // Chống response về trễ đè response mới (đổi lọc liên tiếp nhanh)
            reportSeq: 0,
            optionsSeq: 0,
            drill: { visible: false, loading: false, title: '', filter: {}, params: {}, rows: [] },
            drillSeq: 0,
            // Panel meeting: `row` = dòng nhu cầu / dự án nuôi khối thông tin thêm
            meetingDrawer: { show: false, id: null, row: null },
            customerHistory: { show: false, row: null },
            printOptions: false,
            // Đang chọn cột cho "In danh sách" của popup drill: { own, columns } — null = "In báo cáo" màn chính
            drillPrint: null,
            /**
             * Bản in của nút "In báo cáo". `value` khớp `mode` của BE `print-list-data`; khoá cột khớp whitelist
             * SUMMARY_COLUMNS / DETAIL_COLUMNS của PrintService (thứ tự = cột của bảng). Cột luôn in (STT, Nội dung) KHÔNG khai.
             */
            printModes: [
                {
                    value: 'summary',
                    title: 'In bảng tổng hợp',
                    desc: 'Đúng bảng đang xem, đủ mọi trang và mọi cấp, kèm dòng TỔNG.',
                    fixedNote: 'Cột STT và Nội dung theo dõi luôn được in.',
                    columns: [
                        { key: 'type', label: 'Loại' },
                        { key: 'status', label: 'Trạng thái' },
                        { key: 'vnc', label: 'Giá trị nhu cầu' },
                        { key: 'vda', label: 'Giá trị dự án' },
                        { key: 'milestone', label: 'Mốc thời gian' },
                        { key: 'due', label: 'Hạn theo dõi' },
                        { key: 'care', label: 'Lần chăm sóc gần nhất' },
                        { key: 'source', label: 'Nguồn' },
                    ],
                },
                {
                    value: 'detail',
                    title: 'In danh sách chi tiết',
                    desc: 'Mỗi dòng 1 bản ghi, đúng bộ lọc báo cáo hiện tại.',
                    columns: [
                        { key: 'type', label: 'Loại' },
                        { key: 'content', label: 'Nội dung' },
                        { key: 'customer', label: 'Khách hàng' },
                        { key: 'sales', label: 'Sales phụ trách' },
                        { key: 'status', label: 'Trạng thái' },
                        { key: 'value', label: 'Giá trị dự kiến' },
                        { key: 'milestone', label: 'Mốc thời gian' },
                        { key: 'due', label: 'Hạn theo dõi' },
                        { key: 'source', label: 'Nguồn' },
                    ],
                },
            ],
            hints: {
                org: 'Phòng ban / công ty lấy theo nơi SALES phụ trách ĐANG làm việc tại thời điểm xem — không theo phòng ghi trên dự án.',
                sales: 'Sales phụ trách nhu cầu = người nhận bàn giao, chưa bàn giao thì là người chủ trì meeting. Dự án: Sales chủ trì của dự án.',
                due: 'Chỉ áp cho nhu cầu. Sắp hết hạn = đã vào số ngày cảnh báo trước khi đóng nhu cầu.',
            },
        }
    },
    computed: {
        pageTitle() {
            return 'Báo cáo tổng hợp CSKH tiềm năng'
        },
        /** 8 ô — 2 hàng × 4 (mockup điểm UI #5) */
        filterFields() {
            return [
                // Tự vẽ vỏ floating trong slot (ô khoá / mở theo quyền) -> panel không bọc thêm
                { key: 'company_id', label: 'Công ty', hideLabel: true },
                { key: 'department_id', label: 'Phòng ban', type: 'select', options: this.departmentOptions, hint: this.hints.org },
                { key: 'sales_id', label: 'Sales phụ trách', type: 'select', options: this.salesOptions, hint: this.hints.sales },
                // Ô tìm -> màn tự render qua slot `#field-customer_id`
                { key: 'customer_id', label: 'Khách hàng' },
                { key: 'type', label: 'Loại', type: 'select', options: this.options.types },
                { key: 'statuses', label: 'Tiến trình dự án', type: 'select', multiple: true, options: this.options.statuses },
                { key: 'scope_id', label: 'Lĩnh vực', type: 'select', options: this.options.scopes },
                { key: 'due', label: 'Hạn theo dõi', type: 'select', options: this.options.dues, hint: this.hints.due },
            ]
        },
        companyOptions() {
            return (this.options.companies || []).map((c) => ({ id: c.id, name: c.name }))
        },
        departmentOptions() {
            return (this.options.departments || []).map((d) => ({ id: d.id, name: d.code ? `${d.name} (${d.code})` : d.name }))
        },
        /** Khuôn chung `Tên - Mã phòng - Mã NV` — BE đã dựng sẵn (`employeeOptionLabel`) */
        salesOptions() {
            const list = this.options.sales || []
            const dep = this.filters.department_id
            return list.filter((s) => !dep || String(s.department_id) === String(dep)).map((s) => ({ id: s.id, name: s.name }))
        },
        /** Khối thông tin của CHÍNH dòng đang mở trong panel meeting */
        meetingDrawerBlocks() {
            const row = this.meetingDrawer.row
            if (!row) return []
            if (row.type === 'da') {
                return [
                    {
                        title: 'Dự án TKT',
                        fields: [
                            { label: 'Dự án', value: `${row.code} - ${row.name}` },
                            { label: 'Tiến trình', value: row.status_text, color: row.status_color },
                            { label: 'Giá trị HĐ dự kiến', value: row.value ? num(row.value) : '—' },
                            { label: 'KH cần giải pháp', value: dmy(row.milestone_date) || '—' },
                        ],
                    },
                ]
            }
            return [
                {
                    title: 'Nhu cầu làm dự án',
                    fields: [
                        { label: 'Lĩnh vực / Nhóm ngành', value: row.content || '—' },
                        { label: 'Trạng thái', value: row.status_text, color: row.status_color },
                        { label: 'Giá trị dự kiến', value: row.value ? num(row.value) : '—' },
                        { label: 'Dự kiến triển khai', value: dmy(row.milestone_date) || '—' },
                        { label: 'Hạn theo dõi', value: row.due_date ? `${dmy(row.due_date)} (${daysNote(row.due_days_left)})` : 'Không có hạn' },
                    ],
                },
            ]
        },
    },
    async created() {
        await this.reloadAll()
    },
    methods: {
        /**
         * Handler DUY NHẤT cho mọi thay đổi ô lọc do USER gây ra (panel + slot tự render).
         * Mọi ô ở đây là ô CHỌN -> đổi là tìm luôn (skill list-page: auto-search).
         */
        async onFilterChange(key, rawValue) {
            let value = rawValue === undefined || rawValue === '' ? null : rawValue
            if (key === 'statuses') value = Array.isArray(rawValue) ? rawValue : rawValue ? [rawValue] : []
            // Không quyền tổng công ty: công ty là phạm vi bị khoá — bỏ qua mọi thay đổi
            if (key === 'company_id' && !this.canChangeCompany) return
            if (JSON.stringify(this.filters[key] ?? null) === JSON.stringify(value ?? null)) return

            this.$set(this.filters, key, value)
            if (key === 'company_id') {
                // Phòng ban / Sales thuộc công ty cũ -> xoá để không lọc ngầm bằng id lạc công ty
                this.filters.department_id = null
                this.filters.sales_id = null
            }
            if (key === 'department_id') this.filters.sales_id = null
            // Lọc tiến trình / hạn chỉ có nghĩa với 1 loại -> chọn loại kia thì xoá để không ra bảng rỗng khó hiểu
            if (key === 'type' && value === 'nc') this.filters.statuses = []
            if (key === 'type' && value === 'da') this.filters.due = null

            this.page = 1
            await this.reloadAll()
        },

        onSearch() {
            this.page = 1
            this.reloadAll()
        },

        async reloadAll() {
            await Promise.all([this.loadOptions(), this.loadReport()])
        },

        /**
         * Params dùng chung cho mọi endpoint của màn. KHÔNG gửi `company_id` khi không có quyền tổng công ty (BE cũng
         * bỏ qua, FE không được tỏ ra có quyền). `statuses` gửi CHUỖI "7,8" — link tải Excel (`buildQueryString`) ghi
         * mảng không kèm `[]` nên PHP chỉ giữ phần tử cuối; BE nhận được cả 2 dạng.
         */
        buildParams(extra = {}) {
            const f = this.filters
            const params = {
                company_id: f.company_id,
                department_id: f.department_id,
                sales_id: f.sales_id,
                customer_id: f.customer_id,
                type: f.type,
                statuses: (f.statuses || []).join(','),
                scope_id: f.scope_id,
                due: f.due,
                ...extra,
            }
            if (!this.canChangeCompany) delete params.company_id
            Object.keys(params).forEach((k) => {
                if (params[k] === null || params[k] === '' || params[k] === undefined) delete params[k]
            })
            return params
        },

        async loadOptions() {
            const seq = ++this.optionsSeq
            try {
                const res = await this.$store.dispatch('apiGetMethod', {
                    url: `${API}/filter-options`,
                    params: this.canChangeCompany && this.filters.company_id ? { company_id: this.filters.company_id } : {},
                })
                if (seq !== this.optionsSeq) return
                const data = res.data || {}
                const next = {
                    companies: data.companies || [],
                    departments: data.departments || [],
                    sales: data.sales || [],
                    customers: data.customers || [],
                    scopes: data.scopes || [],
                    statuses: data.statuses || [],
                    types: data.types || [],
                    dues: data.dues || [],
                }
                this.keepSelectedOptions(next)
                this.options = next
                // BE là nguồn sự thật cho quyền đổi công ty (KHÔNG có ngoại lệ super admin)
                this.canChangeCompany = data.can_change_company === true
                // Không quyền: ô Công ty khoá ở đúng công ty BE trả về (chỉ có 1)
                if (!this.canChangeCompany) {
                    this.filters.company_id = (this.options.companies[0] || {}).id || null
                }
            } catch (e) {
                // KHÔNG toast ở đây: loadReport() là nơi báo lỗi duy nhất (gọi song song cùng bộ tham số)
            }
        },

        /**
         * Danh mục ô lọc bó theo phạm vi đang xem -> giá trị ĐANG CHỌN có thể rơi khỏi danh mục mới. Giá trị vẫn được
         * gửi lên BE nên ô hiện trống mà bảng rỗng = lọc ngầm -> giữ lại đúng mục đang chọn (nhãn cũ).
         */
        keepSelectedOptions(next) {
            Object.keys(SELECTED_OPTION_LISTS).forEach((key) => {
                const listKey = SELECTED_OPTION_LISTS[key]
                const value = this.filters[key]
                if (value === null || value === undefined || value === '') return
                const list = next[listKey]
                if (list.some((o) => String(o.id) === String(value))) return
                let item = (this.options[listKey] || []).find((o) => String(o.id) === String(value))
                if (!item && key === 'customer_id' && this.selectedCustomer) {
                    const [code, ...rest] = String(this.selectedCustomer.text || '').split(' - ')
                    item = rest.length ? { id: value, code, name: rest.join(' - ') } : { id: value, name: code }
                }
                if (item) list.push(item)
            })
        },

        async loadReport() {
            const seq = ++this.reportSeq
            const params = this.buildParams({ page: this.page, per_page: this.perPage })
            this.loading = true
            try {
                const res = await this.$store.dispatch('apiGetMethod', { url: API, params })
                if (seq !== this.reportSeq) return
                this.report = res.data
                this.reportParams = { ...params }
                const pg = (res.data && res.data.meta) || {}
                if (pg.current_page) this.page = Number(pg.current_page)
                if (pg.per_page) this.perPage = Number(pg.per_page)
            } catch (e) {
                // Lỗi -> GIỮ báo cáo đang hiển thị (chỉ tắt làm mờ), không xoá trắng màn
                if (seq === this.reportSeq) this.handleError(e)
            } finally {
                if (seq === this.reportSeq) this.loading = false
            }
        },

        /** Lỗi 4xx khác -> báo đúng câu của BE; mã interceptor đã toast thì thôi */
        handleError(e) {
            const status = e && e.response ? Number(e.response.status) : null
            if (status === null || INTERCEPTOR_TOAST_CODES.includes(status)) return
            const data = (e.response && e.response.data) || {}
            const errors = data.errors || {}
            const first = Object.keys(errors).length ? [].concat(errors[Object.keys(errors)[0]])[0] : ''
            this.$toasted.global.error({ message: first || data.message || 'Không tải được báo cáo. Vui lòng thử lại.' })
        },

        onPageChange(page) {
            this.page = page
            this.loadReport()
        },

        onPageSizeChange(size) {
            this.perPage = size
            this.page = 1
            this.loadReport()
        },

        /** Danh mục khách đã bó theo quyền -> lọc theo từ khoá ngay tại FE (khớp mã hoặc tên) */
        async searchCustomers(keyword) {
            const kw = String(keyword || '').toLowerCase()
            return (this.options.customers || [])
                .filter((c) => `${c.code || ''} ${c.name || ''}`.toLowerCase().includes(kw))
                .slice(0, 20)
                .map((c) => ({ id: c.id, text: c.code ? `${c.code} - ${c.name}` : c.name }))
        },

        /** `@select` (không phải `@change`) để giữ được NHÃN — khuôn CSKH tiềm năng */
        onCustomerSelect(option) {
            this.selectedCustomer = option && option.id ? { id: option.id, text: option.text } : null
            this.page = 1
            this.reloadAll()
        },

        /** Xóa lọc: mọi ô về mặc định. Không quyền tổng công ty: GIỮ công ty bị khoá. */
        async handleReset() {
            this.filters = initialFilters(this.canChangeCompany ? null : this.filters.company_id)
            this.selectedCustomer = null
            this.page = 1
            await this.reloadAll()
        },

        // ------------------------------------------------------------ Popup / panel / In / Excel

        /**
         * Bấm 1 con số (khối tổng hợp / dòng TỔNG / dòng cha). `filter` = `{ type?, due?, statuses?, department_id?,
         * sales_id?, customer_id?, title }`. Nhóm "Chưa xác định" gửi 0 (BE: chưa có phòng / Sales) — KHÔNG để rơi mất
         * (rơi là popup liệt kê mọi dòng).
         */
        onDrill(filter = {}) {
            if (!this.reportParams) return
            const { title, ...rest } = filter
            if (Array.isArray(rest.statuses)) rest.statuses = rest.statuses.join(',')
            Object.keys(rest).forEach((k) => {
                if (rest[k] === null || rest[k] === undefined || rest[k] === '') delete rest[k]
            })
            this.drill = {
                visible: true,
                loading: true,
                title: title || 'Tất cả',
                filter: { ...filter },
                params: { ...this.drillBaseParams(), ...rest },
                rows: [],
            }
            this.fetchDrill()
        },

        /** Tải TRỌN tập của ô số (lặp trang 500) — popup lọc / sắp / phân trang tại chỗ */
        async fetchDrill() {
            const seq = ++this.drillSeq
            const all = []
            try {
                for (let page = 1; ; page++) {
                    const res = await this.$store.dispatch('apiGetMethod', {
                        url: `${API}/item-list`,
                        params: { ...this.drill.params, page, per_page: DRILL_PAGE_SIZE },
                    })
                    if (seq !== this.drillSeq) return
                    const data = res.data || {}
                    const rows = data.rows || []
                    all.push(...rows)
                    if (!rows.length || all.length >= Number((data.meta && data.meta.total) || 0)) break
                }
                this.drill.rows = all
            } catch (e) {
                if (seq === this.drillSeq) this.handleError(e)
            } finally {
                if (seq === this.drillSeq) this.drill.loading = false
            }
        },

        /** Tham số nền cho popup / In / Excel: bộ lọc của báo cáo ĐANG HIỂN THỊ, đủ mọi trang */
        drillBaseParams() {
            const params = { ...(this.reportParams || {}) }
            delete params.page
            delete params.per_page
            return params
        },

        onOpenMeeting(row) {
            const id = Number(row && row.meeting_id)
            if (!id) return
            this.meetingDrawer = { show: true, id, row }
        },

        /** Popup lịch sử dùng lại cần `customer_id` / `customer_name` / `customer_code` (đúng khoá của dòng KH) */
        onOpenHistory(customer) {
            if (!customer || !customer.customer_id) return
            this.customerHistory = { show: true, row: customer }
        },

        goEditMeeting(id) {
            this.$router.push('/assign/meeting/' + id + '/edit')
        },

        /** Xem biên bản: popup xem trước bản in có sẵn (mixin) — khuôn CSKH tiềm năng */
        openMeetingReport(id) {
            this.loadPrintPreview('assign/meeting/' + id + '/print', 'Xem biên bản cuộc họp', false)
        },

        onPrint() {
            if (!this.ensureReportLoaded()) return
            this.printOptions = true
        },

        /** Chọn xong ở V2BaseReportPrintModal — `columns` (mảng khoá, đúng thứ tự bảng) gửi thành `cols` */
        onPrintChosen({ mode, columns }) {
            const drill = this.drillPrint
            this.closePrintOptions()
            const cols = columns.join(',')
            if (drill) {
                // In danh sách popup: đúng ô số đã bấm + ô lọc của popup + cột user chọn (Excel KHÔNG qua bước chọn)
                this.openPrintList(API, { ...this.drill.params, ...this.normalizeOwn(drill.own), mode: 'detail', cols, scope_label: this.drill.title }, 'Xem trước danh sách nhu cầu và dự án TKT')

                return
            }
            this.openPrintList(
                API,
                { ...this.drillBaseParams(), mode, cols },
                mode === 'detail' ? 'Xem trước danh sách nhu cầu và dự án TKT' : 'Xem trước báo cáo tổng hợp CSKH tiềm năng'
            )
        },

        closePrintOptions() {
            this.printOptions = false
            this.drillPrint = null
        },

        /** Footer popup "In danh sách": mở popup chọn cột với đúng các cột đang hiện trên popup */
        printItemList({ columns = [], ...own } = {}) {
            this.drillPrint = { own, columns }
            this.printOptions = true
        },

        onExport() {
            if (!this.ensureReportLoaded()) return
            this.downloadExcel(`${API}/export`, this.drillBaseParams())
        },

        exportItemList(own = {}) {
            this.downloadExcel(`${API}/item-list/export`, { ...this.drill.params, ...this.normalizeOwn(own), scope_label: this.drill.title })
        },

        /** Bộ lọc của popup -> cùng dạng tham số với màn (statuses dạng chuỗi) */
        normalizeOwn(own) {
            const out = { ...own }
            if (Array.isArray(out.statuses)) out.statuses = out.statuses.join(',')
            return out
        },

        ensureReportLoaded() {
            if (this.reportParams) return true
            this.$toasted.global.error({ message: 'Báo cáo chưa tải xong, vui lòng thử lại.' })
            return false
        },

        /**
         * Tải file bằng LINK TRỰC TIẾP (`?token=` + `Content-Disposition` của server), KHÔNG fetch rồi tạo blob (hỏng
         * trên Safari/webview). Khuôn copy `service-demand/index.vue`.
         */
        downloadExcel(path, params) {
            try {
                const token = localStorage.getItem('access_token')
                const base = this.$axios.defaults.baseURL || ''
                const query = buildQueryString(params)
                const sep = query ? '&' : '?'
                const link = document.createElement('a')
                link.href = `${base}/api/v1/${path}${query}${sep}token=${encodeURIComponent(token)}`
                document.body.appendChild(link)
                link.click()
                document.body.removeChild(link)
            } catch (error) {
                console.error('Error exporting:', error)
                this.$toasted.global.error({ message: 'Lỗi khi xuất Excel' })
            }
        },
    },
}
</script>

<style scoped>
/* Đang tải lại báo cáo: làm mờ dữ liệu cũ thay vì xoá trắng (đổi lọc liên tiếp không nháy màn) */
.pct-body--loading {
    opacity: 0.6;
    pointer-events: none;
    transition: opacity 0.15s ease;
}
</style>
