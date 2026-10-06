<!--
    Popup "In danh sách" của báo cáo tổng hợp CSKH tiềm năng — chọn 1 trong 2 bản in rồi mở popup xem trước.
    Copy NGUYÊN VĂN từ `pages/assign/report/service-demand/components/PrintOptionsModal.vue` (khuôn gốc
    `prospective-project-results/components/PrintOptionsModal.vue`); chỉ đổi chữ, id, tiền tố class `pct-` và 2 chế
    độ khớp BE `assign/report/potential-customer-tracking/print-list-data` (`mode`):
      - 'summary' (mặc định) -> cây Phòng ▸ Sales ▸ Khách hàng ▸ nhu cầu / dự án, ĐỦ mọi phòng.
      - 'detail' -> danh sách phẳng, mỗi nhu cầu / dự án một dòng, đúng bộ lọc báo cáo đang hiển thị.
-->
<template>
    <b-modal
        id="pct-print-options-modal"
        :visible="visible"
        centered
        hide-footer
        dialog-class="pct-print-dialog"
        content-class="pct-print-content"
        @hidden="$emit('close')"
    >
        <template #modal-header="{ close }">
            <div class="pct-print-head">
                <div class="pct-print-head__title">In danh sách</div>
                <V2BaseIconButton class="pct-print-head__btn" title="Đóng" @click="close()">
                    <i class="ri-close-line"></i>
                </V2BaseIconButton>
            </div>
        </template>

        <p class="pct-print-note">Bản in A4 ngang, bám đúng bộ lọc báo cáo đang hiển thị.</p>

        <div v-for="option in options" :key="option.value" class="pct-print-option">
            <V2BaseRadio
                v-model="mode"
                :options="[{ value: option.value, label: option.title }]"
                name="pct-print-mode"
                :inline="false"
            />
            <p class="pct-print-option__desc">{{ option.desc }}</p>
        </div>

        <div class="pct-print-footer">
            <!-- button-convention §5: hành động chính trước, Thoát/Hủy luôn cuối cùng -->
            <V2BaseButton primary size="sm" @click="submit">
                <template #prefix><i class="ri-printer-line" style="font-size: 14px"></i></template>
                In
            </V2BaseButton>
            <V2BaseButton tertiary size="sm" @click="$emit('close')">
                <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                Hủy
            </V2BaseButton>
        </div>
    </b-modal>
</template>

<script>
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseIconButton from '@/components/V2BaseIconButton.vue'
import V2BaseRadio from '@/components/V2BaseRadio.vue'

export default {
    name: 'PrintOptionsModal',
    components: { V2BaseButton, V2BaseIconButton, V2BaseRadio },
    props: {
        visible: { type: Boolean, default: false },
    },
    data() {
        return {
            mode: 'summary',
            options: [
                {
                    value: 'summary',
                    title: 'In bảng tổng hợp',
                    desc: 'Bảng Phòng ▸ Sales ▸ Khách hàng ▸ nhu cầu / dự án, đủ mọi phòng kèm dòng tổng — không theo trang hay cấp đang thu gọn trên màn.',
                },
                {
                    value: 'detail',
                    title: 'In danh sách chi tiết',
                    desc: 'Từng nhu cầu / dự án một dòng (khách hàng, Sales phụ trách, trạng thái, giá trị, mốc thời gian, hạn theo dõi), đúng bộ lọc báo cáo hiện tại.',
                },
            ],
        }
    },
    watch: {
        // Mở lại popup thì về mặc định, không giữ lựa chọn cũ của lần in trước
        visible(isVisible) {
            if (isVisible) this.mode = 'summary'
        },
    },
    methods: {
        submit() {
            this.$emit('print', this.mode)
        },
    },
}
</script>

<style lang="scss">
/* KHÔNG scoped: b-modal render dialog ra ngoài cây component */
.pct-print-dialog {
    max-width: 520px;
}
.pct-print-content .modal-header {
    padding: 0;
    border: 0;
}
.pct-print-content .modal-body {
    padding: 16px;
}
</style>

<style lang="scss" scoped>
/* Giá trị port từ khuôn đã duyệt — không tự đặt lại palette */
$navy-start: #0a1c3d;
$teal-dark: #0e7490;
$teal: #06b6d4;
$text-muted: #6b7280;
$border-light: #e2e8f0;

.pct-print-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    width: 100%;
    padding: 14px 16px;
    background: linear-gradient(135deg, $navy-start, $teal-dark);
    color: #fff;

    &__title {
        font-size: 15px;
        font-weight: 800;
        line-height: 1.35;
    }

    /* `!important`: đè style mặc định của `V2BaseIconButton` (nền trắng, viền xám) — nút này nằm
       trên nền gradient tối nên cần vòng tròn mờ + chữ trắng, không phải style chuẩn dùng ở nơi
       khác của nút icon-only. */
    &__btn {
        width: 28px !important;
        height: 28px !important;
        border: none !important;
        border-radius: 50% !important;
        background: rgba(255, 255, 255, 0.15) !important;
        color: #fff !important;
        flex-shrink: 0;

        &:hover {
            background: rgba(255, 255, 255, 0.3) !important;
        }
    }
}

.pct-print-note {
    margin: 0 0 12px;
    font-size: 12.5px;
    color: $text-muted;
}

.pct-print-option {
    width: 100%;
    margin-bottom: 10px;
    padding: 11px 12px;
    border: 1px solid $border-light;
    border-radius: 8px;
    transition: border-color 0.15s ease, background 0.15s ease;

    &:hover {
        border-color: rgba(6, 182, 212, 0.5);
        background: rgba(6, 182, 212, 0.04);
    }

    /* Nhãn thật do `V2BaseRadio`/bootstrap-vue dựng (`.custom-control-label`) — tiêu đề lựa chọn
       nằm ở ĐÂY, đậm hơn mặc định của radio thường để giữ đúng phân cấp thị giác.

       `top: auto; transform: none;` RESET đúng 2 thuộc tính mà rule CSS TOÀN CỤC
       `input:not(:placeholder-shown) + label` (assets/scss/custom-theme.scss, thiếu tiền tố
       `.mate-field`) áp nhầm lên MỌI `label` đứng sau `input` — kể cả `.custom-control-label` của
       radio/checkbox. KHÔNG sửa rule toàn cục (ảnh hưởng ra ngoài phạm vi màn này), chỉ vá cục bộ
       đúng màn này (xem khuôn gốc TKT PrintOptionsModal.vue cho chi tiết đo đạc). */
    ::v-deep .custom-control-label {
        top: auto;
        transform: none;
        font-size: 13.5px;
        font-weight: 700;
    }

    /* Dòng mô tả phụ — KHÔNG nằm trong nhãn radio (V2BaseRadio không có slot cho nội dung 2 dòng),
       thụt vào bằng đúng bề rộng của dấu tròn radio (~1.5rem) để thẳng hàng với chữ tiêu đề. */
    &__desc {
        margin: 2px 0 0 1.5rem;
        font-size: 12px;
        color: $text-muted;
    }
}

.pct-print-footer {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 4px;
}
</style>
