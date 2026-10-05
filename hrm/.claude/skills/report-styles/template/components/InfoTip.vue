<!--
    Icon ⓘ + tooltip mô tả — chuẩn `.claude/skills/info-icon-tooltip` (copy khuôn
    `pages/assign/report/employee-work-performance/components/InfoTip.vue`):
    `ri-information-line` 14px màu #94a3b8 + `b-popover` `custom-class="info-popover"`.

    ⚠️ PHẢI khai `font-weight: normal`: thiếu nó thì icon ăn theo `font-weight: 700/800` của nhãn
    xung quanh (tiêu đề cột, tiêu đề khối) nên nét dày hơn hẳn các màn khác.
-->
<template>
    <span class="ptr-info-wrap">
        <span :id="tipId" class="no-print ptr-info">
            <i class="ri-information-line"></i>
        </span>
        <b-popover :target="tipId" triggers="hover focus" placement="bottom" custom-class="info-popover">
            <div class="ptr-info__head">{{ head }}</div>
            <div v-for="(line, index) in lines" :key="index">• {{ line }}</div>
        </b-popover>
    </span>
</template>

<script>
let seq = 0

export default {
    name: 'InfoTip',
    props: {
        head: { type: String, required: true },
        lines: { type: Array, default: () => [] },
    },
    data() {
        seq += 1

        return { tipId: `pct-info-${seq}` }
    },
}
</script>

<style lang="scss" scoped>
.ptr-info-wrap {
    text-transform: none;
    letter-spacing: 0;
}
.ptr-info {
    cursor: pointer;
    color: #94a3b8;
    font-weight: normal;
    margin-left: 3px;

    i {
        font-size: 14px;
    }

    &:hover {
        color: #64748b;
    }
}
.ptr-info__head {
    font-weight: 700;
    margin-bottom: 2px;
}
</style>
