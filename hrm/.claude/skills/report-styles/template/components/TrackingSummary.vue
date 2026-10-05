<!--
    Khối tổng hợp của báo cáo tổng hợp CSKH tiềm năng — copy khuôn
    `pages/assign/report/service-demand/components/DemandSummary.vue` (gốc prepick-tracking, giữ CSS `.rsum*`),
    nội dung theo mockup đã chốt `.plans/gop-db/bao-cao-tong-hop-cskh-tiem-nang/mockup.html`:

      Dòng `.rsum-goal`: "Đang theo dõi tại {thời điểm}" · N nhu cầu · N dự án TKT · N khách hàng · N Sales
      Khối 1 — NHU CẦU ĐANG THEO DÕI: Nhu cầu đang theo dõi · Sắp hết hạn theo dõi
      Khối 2 — DỰ ÁN TKT ĐANG TRIỂN KHAI: Dự án đang triển khai · từng tiến trình 2 → 9

    User chốt 04/10/2026: chỉ tiêu / tiến trình có số 0 KHÔNG hiện (trừ ô tổng của mỗi khối).
    LUÔN tính trên TOÀN BỘ dữ liệu đã lọc (`summary` của BE), không theo trang của bảng.
    Mọi con số bấm được (`DrillNum`) -> emit `drill({ type, due?, statuses?, title })`.
-->
<template>
    <section v-if="summary" class="rsum" :class="{ 'rsum--collapsed': collapsed }">
        <div class="rsum-goal">
            <strong class="rsum-goal__title">Đang theo dõi tại {{ generatedAt }}</strong>
            <InfoTip
                head="MỤC ĐÍCH BÁO CÁO"
                :lines="[
                    'Số liệu chụp TẠI THỜI ĐIỂM MỞ báo cáo — không theo kỳ',
                    'Nhu cầu: nhu cầu làm dự án còn Đang theo dõi (thu từ meeting tìm hiểu & giới thiệu sản phẩm)',
                    'Dự án TKT: tiến trình từ Thu thập thông tin tới Thực hiện hợp đồng',
                    'Bấm vào bất kỳ con số nào để mở danh sách chi tiết',
                ]"
            />
            <span class="rsum-goal__meta">
                · {{ num(summary.nc || 0) }} nhu cầu · {{ num(summary.da || 0) }} dự án TKT · {{ num(summary.customers || 0) }} khách hàng ·
                {{ num(summary.sales || 0) }} Sales
            </span>

            <!-- `<button>` thô CỐ Ý — affordance thu gọn/mở rộng, không phải element form
                 (cùng ghi chú ở khuôn TrackingSummary.vue / DemandSummary.vue). -->
            <button
                type="button"
                class="rsum-toggle"
                :class="{ 'rsum-toggle--collapsed': collapsed }"
                :title="(collapsed ? 'Mở rộng' : 'Thu gọn') + ' khối tổng hợp'"
                @click="collapsed = !collapsed"
            >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
                {{ collapsed ? 'Mở rộng' : 'Thu gọn' }}
            </button>
        </div>

        <div v-show="!collapsed" class="rsum-row">
            <section
                v-for="block in blocks"
                :key="block.id"
                class="rsum-blk"
                :class="`pct-blk--${block.id}`"
                :data-block="block.id"
            >
                <header class="rsum-blk__head">
                    <span class="rsum-blk__title">
                        {{ block.title }}
                        <InfoTip :head="block.tip.head" :lines="block.tip.lines" />
                    </span>
                    <span class="rsum-blk__money">{{ block.meta }}</span>
                </header>

                <div class="rsum-blk__items">
                    <div
                        v-for="item in block.items"
                        :key="item.id"
                        class="rsum-blk__item"
                        :class="item.tone ? `rsum-blk__item--${item.tone}` : ''"
                        :data-item="item.id"
                    >
                        <span class="rsum-blk__label">
                            <span class="rsum-blk__label-text">{{ item.label }}</span>
                        </span>
                        <span class="rsum-blk__value">
                            <DrillNum
                                :value="item.value"
                                :text="num(item.value)"
                                :title="'Xem danh sách: ' + item.drill.title"
                                @click="$emit('drill', item.drill)"
                            />
                            <em>{{ item.sub }}</em>
                        </span>
                    </div>
                </div>
            </section>
        </div>
    </section>
</template>

<script>
import DrillNum from './DrillNum.vue'
import InfoTip from './InfoTip.vue'
import { num } from '../format'

export default {
    name: 'TrackingSummary',
    components: { DrillNum, InfoTip },
    props: {
        /** { nc, da, value_nc, value_da, soon, customers, sales, by_status: { '2'..'9': n } } */
        summary: { type: Object, default: null },
        /** 'dd/mm/yyyy HH:ii' — thời điểm BE chụp số liệu */
        generatedAt: { type: String, default: '' },
        /** [{ id, name, color }] — tiến trình 2 → 9 do BE trả (filter-options) */
        statuses: { type: Array, default: () => [] },
    },
    data() {
        return { collapsed: false }
    },
    computed: {
        blocks() {
            const s = this.summary || {}
            const byStatus = s.by_status || {}
            const ncItems = [
                { id: 'nc', label: 'Nhu cầu đang theo dõi', value: Number(s.nc) || 0, sub: 'nhu cầu', drill: { type: 'nc', title: 'Nhu cầu đang theo dõi' } },
            ]
            if (Number(s.soon) > 0) {
                ncItems.push({
                    id: 'soon',
                    label: 'Sắp hết hạn theo dõi',
                    value: Number(s.soon),
                    sub: 'nhu cầu',
                    tone: 'bad',
                    drill: { type: 'nc', due: 'soon', title: 'Nhu cầu sắp hết hạn theo dõi' },
                })
            }
            const daItems = [
                { id: 'da', label: 'Dự án đang triển khai', value: Number(s.da) || 0, sub: 'dự án', drill: { type: 'da', title: 'Dự án TKT đang triển khai' } },
            ]
            ;(this.statuses || []).forEach((st) => {
                const value = Number(byStatus[String(st.id)]) || 0
                if (!value) return
                daItems.push({
                    id: `status-${st.id}`,
                    label: st.name,
                    value,
                    sub: 'dự án',
                    drill: { type: 'da', statuses: [st.id], title: `Dự án TKT: ${st.name}` },
                })
            })
            return [
                {
                    id: 'nc',
                    title: 'Nhu cầu đang theo dõi',
                    meta: `Giá trị dự kiến ${num(s.value_nc || 0)}`,
                    tip: {
                        head: 'NHU CẦU ĐANG THEO DÕI',
                        lines: [
                            'Nhu cầu làm dự án còn trạng thái Đang theo dõi, meeting thu thập đã Hoàn thành',
                            'Sales phụ trách = người nhận bàn giao, chưa bàn giao thì là người chủ trì meeting',
                            'Sắp hết hạn: còn trong số ngày "Cảnh báo trước khi đóng nhu cầu" của công ty',
                        ],
                    },
                    items: ncItems,
                },
                {
                    id: 'da',
                    title: 'Dự án TKT đang triển khai',
                    meta: `Giá trị HĐ dự kiến ${num(s.value_da || 0)}`,
                    tip: {
                        head: 'DỰ ÁN TKT ĐANG TRIỂN KHAI',
                        lines: [
                            'Tiến trình từ Thu thập thông tin dự án tới Thực hiện hợp đồng',
                            'Không tính dự án Đang tạo, Nghiệm thu & thanh lý, Đóng, Kết thúc',
                            'Tiến trình chưa có dự án nào thì không hiện',
                        ],
                    },
                    items: daItems,
                },
            ]
        },
    },
    methods: {
        num,
    },
}
</script>

<style lang="scss" scoped>
/* Copy nguyên từ `pages/assign/report/service-demand/components/DemandSummary.vue` (gốc
   `pages/sale/prepick-tracking/components/TrackingSummary.vue`) + tông `--bad` của màn gốc cho ô "Sắp hết hạn".
   Bỏ 4 tông trạng thái của nhu cầu dịch vụ (không dùng ở báo cáo này). */
$teal: #06b6d4;
$teal-dark: #0e7490;
$text-main: #1f2937;
$text-muted: #6b7280;

.rsum {
    background: #fff;
    border: 1px solid #e8edf2;
    border-left: 3px solid $teal;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.05);
    margin-bottom: 14px;
    padding: 8px 12px 9px;
    font-size: 12px;
    color: $text-main;
}

.rsum-goal {
    margin: 0 0 6px;
    padding-bottom: 6px;
    border-bottom: 1px dashed #e2e8f0;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 2px 8px;
    font-size: 11px;
    color: $text-muted;

    strong {
        color: $text-main;
        font-size: 11.5px;
        font-weight: 700;
    }
}
.rsum--collapsed .rsum-goal {
    margin: 0;
    padding-bottom: 0;
    border-bottom: 0;
}

.rsum-toggle {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    height: 24px;
    padding: 0 9px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #fff;
    color: $text-muted;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;

    &:hover {
        border-color: $teal-dark;
        color: $teal-dark;
    }

    svg {
        width: 12px;
        height: 12px;
        transition: transform 0.15s ease;
    }
}
.rsum-toggle--collapsed svg {
    transform: rotate(-90deg);
}

/* 2 khối cùng 1 hàng — chia bề ngang theo SỐ Ô (3 : 4), khuôn TrackingSummary */
.rsum-row {
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
    gap: 8px;
}
.rsum-row > .rsum-blk {
    flex: 1 1 0;
    min-width: 0;
}
/* Khối Nhu cầu (≤ 2 ô) rộng theo nội dung; khối Dự án (tới 9 ô) lấy phần còn lại. Chia theo tỉ lệ cố định như khuôn
   (3:4) làm 9 ô bị bóp, nhãn rớt 2 dòng, ô cao 58px thay vì 46px (đã đo 1600px) — mockup đã chốt: ô giữ nhãn 1 dòng,
   thiếu chỗ thì cả ô xuống hàng (điểm UI #6). */
.rsum-row > .pct-blk--nc {
    flex: 0 0 auto;
}
.rsum-row > .pct-blk--da {
    flex: 1 1 0;
}

.rsum-blk {
    display: flex;
    flex-direction: column;
    padding: 6px 10px 7px;
    border: 1px solid rgba(6, 182, 212, 0.32);
    border-left: 3px solid $teal-dark;
    border-radius: 6px;
    background: linear-gradient(135deg, #f2fdfe, #fbfeff);
}
.rsum-blk--closed {
    border-color: #d8e3ec;
    border-left-color: #475569;
    background: linear-gradient(135deg, #f6f8fb, #fdfeff);
}

.rsum-blk__head {
    display: flex;
    align-items: baseline;
    gap: 7px;
    margin-bottom: 5px;
}
.rsum-blk__title {
    flex: 1 1 auto;
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    white-space: nowrap;
    color: $text-main;
}
.rsum-blk__money {
    font-size: 10.5px;
    font-weight: 700;
    white-space: nowrap;
    color: $text-muted;
    font-variant-numeric: tabular-nums;
}

.rsum-blk__items {
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
    gap: 6px;
    flex: 1 1 auto;
}
.rsum-blk__item {
    flex: 1 0 auto;
    min-width: 0;
    padding: 4px 9px 5px;
    border: 1px solid #e6edf3;
    border-radius: 6px;
    background: #fff;
}
/* Tông CAM cho ô "Sắp hết hạn theo dõi" — copy `prepick-tracking/components/TrackingSummary.vue` */
.rsum-blk__item--bad {
    border-color: rgba(245, 158, 11, 0.45);
    background: linear-gradient(135deg, #fff8ea, #fffdf7);
}

.rsum-blk__label {
    display: flex;
    align-items: center;
    gap: 3px;
    font-size: 10px;
    font-weight: 700;
    line-height: 1.3;
    white-space: nowrap;
    color: $text-muted;
}
.rsum-blk__label-text {
    min-width: 0;
    white-space: nowrap;
}
/* Icon ⓘ 14px không được đẩy cao dòng nhãn 10px / tiêu đề khối */
.rsum-blk__label ::v-deep .ptr-info i,
.rsum-blk__title ::v-deep .ptr-info i,
.rsum-goal ::v-deep .ptr-info i {
    line-height: 1;
    display: inline-block;
    vertical-align: middle;
}
.rsum-blk__value {
    display: flex;
    align-items: baseline;
    gap: 4px;
    font-size: 15px;
    font-weight: 800;
    line-height: 1.3;
    color: $text-main;
    font-variant-numeric: tabular-nums;

    em {
        font-style: normal;
        font-size: 10px;
        font-weight: 700;
        color: $text-muted;
        white-space: nowrap;
    }
}
.rsum-blk__item--bad .rsum-blk__value {
    color: #b45309;
}
</style>
