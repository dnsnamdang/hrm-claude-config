<!--
    Con số bấm được trong khối tổng hợp / bảng cây báo cáo tổng hợp CSKH tiềm năng — copy nguyên khuôn
    `pages/assign/report/prospective-project-results/components/DrillNum.vue`.

    Quy tắc giữ nguyên bản gốc: giá trị 0 thì KHÔNG bấm được, hiện chữ thường — tránh mở popup rỗng.
-->
<template>
    <button v-if="value" type="button" class="rsum-drill" :title="title || null" @click="$emit('click')">
        {{ text || value }}
    </button>
    <span v-else>{{ text || 0 }}</span>
</template>

<script>
export default {
    name: 'DrillNum',
    props: {
        value: { type: [Number, String], default: 0 },
        /** Chữ hiển thị khi khác giá trị thô (vd số đã định dạng) */
        text: { type: String, default: '' },
        title: { type: String, default: '' },
    },
}
</script>

<style lang="scss" scoped>
.rsum-drill {
    border: 0;
    padding: 0;
    background: none;
    font: inherit;
    color: inherit;
    cursor: pointer;
    border-bottom: 1px dashed currentColor;

    &:hover {
        color: #0e7490;
        border-bottom-style: solid;
    }
}
</style>
