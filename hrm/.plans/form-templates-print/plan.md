# In mẫu phiếu (bản trống) — Implementation Plan

> **For agentic workers:** Dùng superpowers:subagent-driven-development hoặc superpowers:executing-plans để thực thi từng task. Steps dùng checkbox (`- [ ]`).
> **Lưu ý dự án:** FE Vue 2 (Nuxt 2), KHÔNG có unit test (Jest/pytest). Kiểm thử = verify browser thủ công theo convention dự án. KHÔNG commit/push khi chưa được yêu cầu.

**Goal:** Thêm chức năng in mẫu phiếu thu thập thông tin ở dạng bản TRỐNG từ màn `assign/form-templates` (nút ở màn danh sách cạnh "Sửa" + màn xem chi tiết), qua modal preview + `window.print`.

**Architecture:** Thuần FE. Tạo component riêng `FormTemplatePrintSheet.vue` (copy layout từ `SurveyPrintSheet.vue`, KHÔNG sửa file dùng chung). Tái dùng API `GET assign/form-templates/{id}` để lấy `sections`. Cơ chế in tái dùng pattern `window.open()` + `getPrintStyles()` của `formTabInput.printModalPDF`.

**Tech Stack:** Vue 2 / Nuxt 2, Bootstrap-Vue (`b-modal`), V2Base components, Remix Icon.

---

## File Structure

| File | Loại | Trách nhiệm |
|------|------|-------------|
| `hrm-client/components/FormTemplatePrintSheet.vue` | Create | Render phiếu in bản trống: header (8 dòng) + bảng 3 cột, cột đáp án rỗng. Cung cấp `$refs.printArea` + `getPrintStyles()`. |
| `hrm-client/pages/assign/form-templates/_id/index.vue` | Modify | Nút "In mẫu phiếu" (footer) + modal preview + hàm in. Data `sections` đã có sẵn. |
| `hrm-client/pages/assign/form-templates/index.vue` | Modify | Row action "In mẫu phiếu" cạnh "Sửa" + fetch detail lấy `sections` + modal preview + hàm in. |

**Hợp đồng component `FormTemplatePrintSheet`:**
- Props:
  - `formTemplate: Object` — `{ name, sections }` (sections theo cấu trúc transformer: section.groups[].questions[].children[] hoặc section.questions[].children[]).
  - `header: Object` — chỉ cần `{ scopeName: String, industryName: String }`. Các trường khác luôn để trống.
  - `printHeaderImage: String` — ảnh header công ty (có default).
  - `answerColumnTitle: String` — default `'Đáp án/giá trị thu thập cho tôi'`.
- Expose: `this.$refs.printArea` (DOM để in) + method `getPrintStyles()` (trả CSS string).

---

## Task 1: Tạo component `FormTemplatePrintSheet.vue`

**Files:**
- Create: `hrm-client/components/FormTemplatePrintSheet.vue`

- [ ] **Step 1: Tạo file với nội dung đầy đủ**

```vue
<template>
    <div class="form-template-print-sheet">
        <div class="print-container">
            <div class="print-wrapper">
                <div ref="printArea" class="print-sheet">
                    <div class="sheet-header">
                        <img :src="printHeaderImage" alt="company header" class="sheet-header__img" />
                    </div>
                    <h1 class="sheet-title mt-4">THÔNG TIN KHẢO SÁT</h1>
                    <div class="sheet-info">
                        <div class="info-row">
                            <div class="info-field info-field--full">
                                <span class="info-label">Tên khách hàng:</span>
                                <span class="info-line"></span>
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-field info-field--full">
                                <span class="info-label">Tên dự án:</span>
                                <span class="info-line"></span>
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-field info-field--full">
                                <span class="info-label">Mã dự án:</span>
                                <span class="info-line"></span>
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-field info-field--md">
                                <span class="info-label">Phân loại:</span>
                                <span class="info-line"></span>
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-field info-field--md">
                                <span class="info-label">Nhóm ngành:</span>
                                <span class="info-line">{{ header.scopeName }}</span>
                            </div>
                            <div class="info-field info-field--md">
                                <span class="info-label">Nhóm giải pháp:</span>
                                <span class="info-line">{{ header.industryName }}</span>
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-field info-field--full">
                                <span class="info-label">Ngày khảo sát:</span>
                                <span class="info-line">...../...../.....</span>
                            </div>
                        </div>
                        <div class="info-row">
                            <div class="info-field info-field--full">
                                <span class="info-label">Người khảo sát:</span>
                                <span class="info-line"></span>
                            </div>
                        </div>
                    </div>
                    <h2 class="section-title">NỘI DUNG KHẢO SÁT</h2>
                    <table class="print-table" v-if="formTemplate && formTemplate.sections">
                        <thead>
                            <tr>
                                <th class="print-table__col-stt">STT</th>
                                <th class="print-table__col-content">NỘI DUNG</th>
                                <th class="print-table__col-answer">{{ answerColumnTitle }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <template v-for="(section, sIdx) in formTemplate.sections">
                                <tr :key="`section-${sIdx}`" class="section-row">
                                    <td class="text-center section-number">{{ getSectionNumber(sIdx) }}</td>
                                    <td class="section-title-cell">
                                        <strong>{{ section.title || '' }}</strong>
                                    </td>
                                    <td></td>
                                </tr>
                                <!-- Groups in Section -->
                                <template v-if="section.groups && section.groups.length">
                                    <template v-for="(group, gIdx) in section.groups">
                                        <tr :key="`group-${sIdx}-${gIdx}`" class="group-row">
                                            <td class="text-center group-number">{{ getGroupNumber(gIdx) }}</td>
                                            <td class="group-title-cell">
                                                <strong>{{ group.title || '' }}</strong>
                                            </td>
                                            <td></td>
                                        </tr>
                                        <template v-if="group.questions && group.questions.length">
                                            <template v-for="(question, qIdx) in group.questions">
                                                <tr :key="`q-${sIdx}-${gIdx}-${qIdx}`" class="question-row">
                                                    <td class="text-center question-number">
                                                        {{ getQuestionNumber(qIdx) }}
                                                    </td>
                                                    <td class="question-content-cell">
                                                        {{ question.label || 'Chưa đặt nội dung câu hỏi' }}
                                                        <span v-if="question.required" class="text-danger">(*)</span>
                                                    </td>
                                                    <td class="question-answer-cell"></td>
                                                </tr>
                                                <template v-if="question.children && question.children.length">
                                                    <template v-for="(child, cIdx) in question.children">
                                                        <tr
                                                            :key="`c-${sIdx}-${gIdx}-${qIdx}-${cIdx}`"
                                                            class="child-question-row"
                                                        >
                                                            <td class="text-center child-question-number">
                                                                {{ getChildQuestionNumber(qIdx, cIdx) }}
                                                            </td>
                                                            <td class="child-question-content-cell">
                                                                {{ getChildQuestionNumber(qIdx, cIdx) }}
                                                                {{ child.label || 'Chưa đặt nội dung câu hỏi' }}
                                                                <span v-if="child.required" class="text-danger"
                                                                    >(*)</span
                                                                >
                                                                <span class="text-muted small"> - câu hỏi con</span>
                                                            </td>
                                                            <td class="child-question-answer-cell"></td>
                                                        </tr>
                                                    </template>
                                                </template>
                                            </template>
                                        </template>
                                    </template>
                                </template>
                                <!-- Questions directly in Section (no groups) -->
                                <template v-else-if="section.questions && section.questions.length">
                                    <template v-for="(question, qIdx) in section.questions">
                                        <tr :key="`q-${sIdx}-${qIdx}`" class="question-row">
                                            <td class="text-center question-number">
                                                {{ getQuestionNumberDirect(qIdx) }}
                                            </td>
                                            <td class="question-content-cell">
                                                {{ question.label || 'Chưa đặt nội dung câu hỏi' }}
                                                <span v-if="question.required" class="text-danger">(*)</span>
                                            </td>
                                            <td class="question-answer-cell"></td>
                                        </tr>
                                        <template v-if="question.children && question.children.length">
                                            <template v-for="(child, cIdx) in question.children">
                                                <tr :key="`c-${sIdx}-${qIdx}-${cIdx}`" class="child-question-row">
                                                    <td class="text-center child-question-number">
                                                        {{ getChildQuestionNumberDirect(qIdx, cIdx) }}
                                                    </td>
                                                    <td class="child-question-content-cell">
                                                        {{ getChildQuestionNumberDirect(qIdx, cIdx) }}
                                                        {{ child.label || 'Chưa đặt nội dung câu hỏi' }}
                                                        <span v-if="child.required" class="text-danger">(*)</span>
                                                        <span class="text-muted small"> - câu hỏi con</span>
                                                    </td>
                                                    <td class="child-question-answer-cell"></td>
                                                </tr>
                                            </template>
                                        </template>
                                    </template>
                                </template>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'FormTemplatePrintSheet',
    props: {
        formTemplate: { type: Object, default: null },
        header: {
            type: Object,
            default: () => ({
                scopeName: '',
                industryName: '',
            }),
        },
        answerColumnTitle: { type: String, default: 'Đáp án/giá trị thu thập cho tôi' },
        printHeaderImage: {
            type: String,
            default: 'https://tanphat.s3.cloud.cmctelecom.vn/tanphat_hrm/1751696586ts-hnpng-1764138697-plC8.png',
        },
    },
    methods: {
        getSectionNumber(sIdx) {
            return String.fromCharCode(65 + sIdx)
        },
        getGroupNumber(gIdx) {
            const r = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
            return r[gIdx] ?? String(gIdx + 1)
        },
        getQuestionNumber(qIdx) {
            return qIdx + 1
        },
        getChildQuestionNumber(qIdx, cIdx) {
            return `${qIdx + 1}.${cIdx + 1}`
        },
        getQuestionNumberDirect(qIdx) {
            return qIdx + 1
        },
        getChildQuestionNumberDirect(qIdx, cIdx) {
            return `${qIdx + 1}.${cIdx + 1}`
        },
        /** CSS dùng khi in qua window.open. Parent gọi khi cần in. */
        getPrintStyles() {
            return `
                @page { size: A4; margin: 20mm 15mm 20mm 25mm; }
                body { margin: 0; padding: 0; font-family: 'Times New Roman', Times, serif !important; }
                .print-container { padding: 0; margin: 0 auto; width: 100%; }
                .print-wrapper { margin: 0 auto 24px; width: 100%; }
                .print-sheet { width: 100%; max-width: 100%; margin: 0 auto; padding: 0; color: #111; }
                .sheet-header__img { width: 100%; display: block; }
                .sheet-title { margin: 24px 0 20px; text-align: center; font-size: 24px; font-weight: 700; letter-spacing: 1px; }
                .section-title { font-family: 'Times New Roman', Times, serif !important; margin: 24px 0 16px; text-align: center; font-size: 20px; font-weight: 700; }
                .sheet-info { margin-bottom: 12px; }
                .info-row { display: flex; flex-wrap: wrap; gap: 8px; }
                .info-field { display: flex; align-items: flex-start; gap: 6px; flex: 1 1 200px; min-height: 28px; min-width: 0; }
                .info-field--md { flex: 1 1 220px; min-width: 0; }
                .info-field--full { flex: 1 1 100%; }
                .info-label { font-weight: 600; white-space: nowrap; }
                .info-line { flex: 1; min-width: 0; word-break: break-word; overflow-wrap: break-word; }
                .print-table { width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 16px; }
                .print-table th, .print-table td { border: 1px solid #111; padding: 8px 10px; vertical-align: top; }
                .print-table thead th { text-transform: uppercase; font-weight: 700; text-align: center; background-color: #f0f0f0; }
                .print-table__col-stt { width: 60px; }
                .print-table__col-content { width: 45%; }
                .print-table__col-answer { width: auto; }
                .section-row { background-color: #f9f9f9; }
                .section-number { font-weight: 700; font-size: 16px; }
                .section-title-cell { font-weight: 700; font-size: 15px; }
                .group-row { background-color: #f5f5f5; }
                .group-number { font-weight: 600; }
                .group-title-cell { font-weight: 600; }
                .question-number { font-weight: 500; }
                .question-answer-cell { min-width: 200px; }
                .child-question-number { font-weight: 400; font-size: 13px; }
                .child-question-content-cell, .child-question-answer-cell { font-size: 13px; min-width: 200px; }
                .text-center { text-align: center !important; }
                .text-danger { color: #dc3545; }
                .text-muted { color: #6c757d; }
                .small { font-size: 0.875em; }
                .mt-4 { margin-top: 1.5rem !important; }
            `
        },
    },
}
</script>

<style lang="scss" scoped>
.h1, .h2, h1, h2 {
    font-family: 'Times New Roman', Times, serif !important;
}
.form-template-print-sheet {
    font-family: 'Times New Roman', Times, serif !important;
}
.print-container {
    padding: 24px 0 40px;
}
.print-wrapper {
    display: flex;
    justify-content: center;
}
.print-sheet {
    width: 100%;
    max-width: 210mm;
    margin: 0 auto;
    background: #fff;
    border: 1px solid #d3d3d3;
    border-radius: 5px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    padding: 20mm 15mm 20mm 25mm;
    font-size: 16px;
    line-height: 1.4;
    color: #111;
}
.sheet-header__img {
    width: 100%;
    display: block;
}
.sheet-title {
    margin: 12px 0 20px;
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 1px;
}
.section-title {
    margin: 24px 0 16px;
    text-align: center;
    font-size: 20px;
    font-weight: 700;
}
.sheet-info {
    margin-bottom: 12px;
}
.info-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.info-field {
    display: flex;
    align-items: flex-start;
    gap: 6px;
    flex: 1 1 200px;
    min-height: 28px;
    min-width: 0;
}
.info-field--md {
    flex: 1 1 220px;
    min-width: 0;
}
.info-field--full {
    flex: 1 1 100%;
}
.info-label {
    font-weight: 600;
    white-space: nowrap;
}
.info-line {
    flex: 1;
    min-width: 0;
    word-break: break-word;
    overflow-wrap: break-word;
}
.print-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
    font-size: 14px;
}
.print-table th,
.print-table td {
    border: 1px solid #111;
    padding: 8px 10px;
    vertical-align: top;
}
.print-table thead th {
    text-transform: uppercase;
    font-weight: 700;
    text-align: center;
    background-color: #f0f0f0;
}
.print-table__col-stt {
    width: 60px;
}
.print-table__col-content {
    width: 45%;
}
.print-table__col-answer {
    width: auto;
}
.section-row {
    background-color: #f9f9f9;
}
.section-number {
    font-weight: 700;
    font-size: 16px;
}
.section-title-cell {
    font-weight: 700;
    font-size: 15px;
}
.group-row {
    background-color: #f5f5f5;
}
.group-number {
    font-weight: 600;
}
.group-title-cell {
    font-weight: 600;
}
.question-number {
    font-weight: 500;
}
.question-answer-cell {
    min-width: 200px;
}
.child-question-number {
    font-weight: 400;
    font-size: 13px;
}
.child-question-content-cell,
.child-question-answer-cell {
    font-size: 13px;
    min-width: 200px;
}
.text-center {
    text-align: center !important;
}
.text-danger {
    color: #dc3545;
}
.text-muted {
    color: #6c757d;
}
.small {
    font-size: 0.875em;
}
.mt-4 {
    margin-top: 1.5rem !important;
}
</style>
```

- [ ] **Step 2: Verify component biên dịch**

Mở browser console khi dev server chạy — không có lỗi parse/compile cho `FormTemplatePrintSheet.vue`. (Chưa render ở đâu nên chỉ cần không lỗi import ở Task 2/3.)

---

## Task 2: Màn chi tiết — nút "In mẫu phiếu" + modal

**Files:**
- Modify: `hrm-client/pages/assign/form-templates/_id/index.vue`

- [ ] **Step 1: Import + đăng ký component**

Sửa khối import (sau dòng `import V2BaseButton from '@/components/V2BaseButton.vue'`, dòng ~30):

```js
import FormPreview from '../components/FormPreview.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import FormTemplatePrintSheet from '@/components/FormTemplatePrintSheet.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'
```

Sửa khối `components`:

```js
    components: {
        FormPreview,
        V2BaseButton,
        FormTemplatePrintSheet,
    },
```

- [ ] **Step 2: Thêm state `showPrintPreview`**

Trong `data()` return, thêm `showPrintPreview: false` (sau `industriesAll: []`):

```js
    data() {
        return {
            loading: true,
            formTemplate: {},
            previewAnswers: {},
            previewFormInfo: {
                scopeId: null,
                industryId: null,
            },
            scopesAll: [],
            industriesAll: [],
            showPrintPreview: false,
        }
    },
```

- [ ] **Step 3: Thêm computed `printHeader`**

Trong `computed`, thêm sau `pageTitle()`:

```js
    computed: {
        pageTitle() {
            return 'Chi tiết Form'
        },
        printHeader() {
            return {
                scopeName: this.getScopeName(this.formTemplate.scope_id),
                industryName: this.getIndustryName(this.formTemplate.industry_id),
            }
        },
    },
```

- [ ] **Step 4: Thêm method `printSheet`**

Trong `methods`, thêm sau `copyTemplate()`:

```js
        copyTemplate() {
            this.$router.push(`/assign/form-templates/add?copyFrom=${this.$route.params.id}`)
        },
        printSheet() {
            const sheet = this.$refs.printSheet
            if (!sheet || !sheet.$refs.printArea) {
                this.$toasted?.global?.error?.({ message: 'Chưa tải xong mẫu phiếu' })
                return
            }
            const contentEl = sheet.$refs.printArea
            const printWindow = window.open('', 'FormTemplatePrint', 'height=1600,width=1100')
            if (!printWindow) {
                this.$toasted?.global?.error?.({ message: 'Không thể mở cửa sổ in. Vui lòng cho phép popup.' })
                return
            }
            printWindow.document.write('<!DOCTYPE html><html><head><meta charset="utf-8" />')
            printWindow.document.write('<title>Mẫu phiếu thu thập thông tin</title>')
            printWindow.document.write(`<style>${sheet.getPrintStyles()}</style>`)
            printWindow.document.write('</head><body>')
            printWindow.document.write(contentEl.outerHTML)
            printWindow.document.write('</body></html>')
            printWindow.document.close()
            printWindow.onload = function () {
                printWindow.focus()
                printWindow.print()
            }
        },
```

- [ ] **Step 5: Thêm nút "In mẫu phiếu" vào footer**

Sửa khối `<V2Footer>` (thêm nút In TRƯỚC nút Sao chép):

```vue
        <V2Footer>
            <template #custom-actions>
                <V2BaseButton primary size="sm" @click="showPrintPreview = true">
                    <template #prefix><i class="ri-printer-line" style="font-size: 15px"></i></template>
                    In mẫu phiếu
                </V2BaseButton>
                <V2BaseButton secondary size="sm" class="ml-2" @click="copyTemplate">
                    <template #prefix><i class="ri-file-copy-line" style="font-size: 15px"></i></template>
                    Sao chép
                </V2BaseButton>
            </template>
        </V2Footer>
```

- [ ] **Step 6: Thêm modal preview**

Thêm modal NGAY TRƯỚC `</V2Footer>`'s closing... thực tế đặt sau `</V2Footer>`, trước `</div>` gốc của template:

```vue
        </V2Footer>

        <b-modal
            v-model="showPrintPreview"
            size="xl"
            hide-footer
            content-class="shadow"
            @hide="showPrintPreview = false"
        >
            <template #modal-header>
                <div class="d-flex align-items-center w-100">
                    <div
                        class="d-flex align-items-center justify-content-center mr-2"
                        style="
                            width: 28px;
                            height: 28px;
                            border-radius: 999px;
                            background: rgba(26, 188, 156, 0.1);
                            color: #1abc9c;
                        "
                    >
                        <i class="ri-printer-line" style="font-size: 16px"></i>
                    </div>
                    <h5 class="modal-title mb-0" style="font-size: 14px; font-weight: 800">
                        Xem trước mẫu phiếu in
                    </h5>
                </div>
                <button type="button" class="close" @click="showPrintPreview = false">
                    <span aria-hidden="true">&times;</span>
                </button>
            </template>

            <div class="modal-body">
                <FormTemplatePrintSheet
                    ref="printSheet"
                    :form-template="formTemplate"
                    :header="printHeader"
                />
            </div>

            <div class="modal-footer">
                <V2BaseButton primary size="sm" @click="printSheet">
                    <template #prefix><i class="ri-printer-line" style="font-size: 15px"></i></template>
                    In
                </V2BaseButton>
                <V2BaseButton tertiary size="sm" @click="showPrintPreview = false">
                    <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                    Đóng
                </V2BaseButton>
            </div>
        </b-modal>
    </div>
</template>
```

- [ ] **Step 7: Thêm style modal (tùy chọn, cho rộng + scroll)**

Sửa `<style scoped></style>` cuối file:

```vue
<style scoped>
::v-deep .modal-dialog {
    max-width: 1200px;
}
::v-deep .modal-body {
    max-height: 80vh;
    overflow-y: auto;
}
</style>
```

- [ ] **Step 8: Verify browser** (xem Task 4)

---

## Task 3: Màn danh sách — row action "In mẫu phiếu" + modal

**Files:**
- Modify: `hrm-client/pages/assign/form-templates/index.vue`

- [ ] **Step 1: Import + đăng ký component**

Thêm import sau `import V2BaseTitleSubInfo from '@/components/V2BaseTitleSubInfo.vue'` (dòng ~218):

```js
import V2BaseTitleSubInfo from '@/components/V2BaseTitleSubInfo.vue'
import FormTemplatePrintSheet from '@/components/FormTemplatePrintSheet.vue'
import BaseConfirmModal from '@/components/modal/base-confirm-modal.vue'
```

Thêm vào `components`:

```js
    components: {
        V2BaseButton,
        V2BaseFilterPanel,
        V2BaseDataTable,
        BaseConfirmModal,
        V2BaseTitleSubInfo,
        FormTemplatePrintSheet,
    },
```

- [ ] **Step 2: Thêm state cho modal in**

Trong `data()` return, thêm 3 field (sau `templateToToggle: null,`):

```js
            templateToDelete: null,

            templateToToggle: null,

            showPrintPreview: false,
            printTemplate: null,
            printHeader: { scopeName: '', industryName: '' },
```

- [ ] **Step 3: Thêm row action "In mẫu phiếu" cạnh "Sửa"**

Trong `getRowActions(item)`, thêm action `print` NGAY SAU push `edit` (trước nhánh `if (item.status !== 1)`):

```js
            // Chỉ hiển thị button sửa khi status = 1 (Nháp)
            actions.push({
                key: 'edit',
                title: 'Sửa mẫu',
                icon: 'ri-edit-line',
                class: 'btn btn-light border btn-sm mr-1',
            })

            actions.push({
                key: 'print',
                title: 'In mẫu phiếu',
                icon: 'ri-printer-line',
                class: 'btn btn-light border btn-sm mr-1',
            })

            if (item.status !== 1) {
```

- [ ] **Step 4: Xử lý action `print` trong `handleRowAction`**

Thêm case `print`:

```js
        handleRowAction(payload) {
            const { action, item } = payload

            switch (action) {
                case 'view':
                    this.viewTemplate(item)
                    break
                case 'copy':
                    this.copyTemplate(item)
                    break
                case 'edit':
                    this.editTemplate(item)
                    break
                case 'print':
                    this.openPrintPreview(item)
                    break
                case 'toggle-lock':
                    this.confirmToggleLock(item)
                    break
                case 'delete':
                    this.confirmDeleteTemplate(item)
                    break
            }
        },
```

- [ ] **Step 5: Thêm method `openPrintPreview` + `printSheet`**

Thêm vào `methods` (sau `viewTemplate(t)`):

```js
        viewTemplate(t) {
            this.$router.push(`/assign/form-templates/${t.id}`)
        },

        async openPrintPreview(item) {
            try {
                this.$nuxt.$loading.start()
                const { data } = await this.$store.dispatch('apiGetMethod', `assign/form-templates/${item.id}`)
                this.printTemplate = data || {}
                this.printHeader = {
                    scopeName: item.scope_name || '',
                    industryName: item.industry_name || '',
                }
                this.showPrintPreview = true
            } catch (error) {
                this.$toasted?.global?.error?.({ message: 'Không thể tải mẫu phiếu để in' })
            } finally {
                this.$nuxt.$loading.finish()
            }
        },

        printSheet() {
            const sheet = this.$refs.printSheet
            if (!sheet || !sheet.$refs.printArea) {
                this.$toasted?.global?.error?.({ message: 'Chưa tải xong mẫu phiếu' })
                return
            }
            const contentEl = sheet.$refs.printArea
            const printWindow = window.open('', 'FormTemplatePrint', 'height=1600,width=1100')
            if (!printWindow) {
                this.$toasted?.global?.error?.({ message: 'Không thể mở cửa sổ in. Vui lòng cho phép popup.' })
                return
            }
            printWindow.document.write('<!DOCTYPE html><html><head><meta charset="utf-8" />')
            printWindow.document.write('<title>Mẫu phiếu thu thập thông tin</title>')
            printWindow.document.write(`<style>${sheet.getPrintStyles()}</style>`)
            printWindow.document.write('</head><body>')
            printWindow.document.write(contentEl.outerHTML)
            printWindow.document.write('</body></html>')
            printWindow.document.close()
            printWindow.onload = function () {
                printWindow.focus()
                printWindow.print()
            }
        },
```

- [ ] **Step 6: Thêm modal preview vào template**

Thêm NGAY SAU `<BaseConfirmModal id="confirm-toggle-lock-template" ... />` (trước `</div>` gốc, dòng ~210):

```vue
        <BaseConfirmModal
            id="confirm-toggle-lock-template"
            :title="lockConfirmTitle"
            :message="lockConfirmMessage"
            text-close="Hủy"
            :text-accept="lockConfirmAction"
            @event="toggleLock"
        />

        <b-modal
            v-model="showPrintPreview"
            size="xl"
            hide-footer
            content-class="shadow"
            @hide="showPrintPreview = false"
        >
            <template #modal-header>
                <div class="d-flex align-items-center w-100">
                    <div
                        class="d-flex align-items-center justify-content-center mr-2"
                        style="
                            width: 28px;
                            height: 28px;
                            border-radius: 999px;
                            background: rgba(26, 188, 156, 0.1);
                            color: #1abc9c;
                        "
                    >
                        <i class="ri-printer-line" style="font-size: 16px"></i>
                    </div>
                    <h5 class="modal-title mb-0" style="font-size: 14px; font-weight: 800">
                        Xem trước mẫu phiếu in
                    </h5>
                </div>
                <button type="button" class="close" @click="showPrintPreview = false">
                    <span aria-hidden="true">&times;</span>
                </button>
            </template>

            <div class="modal-body">
                <FormTemplatePrintSheet
                    ref="printSheet"
                    :form-template="printTemplate"
                    :header="printHeader"
                />
            </div>

            <div class="modal-footer">
                <V2BaseButton primary size="sm" @click="printSheet">
                    <template #prefix><i class="ri-printer-line" style="font-size: 15px"></i></template>
                    In
                </V2BaseButton>
                <V2BaseButton tertiary size="sm" @click="showPrintPreview = false">
                    <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                    Đóng
                </V2BaseButton>
            </div>
        </b-modal>
    </div>
</template>
```

- [ ] **Step 7: Thêm style modal**

File này dùng `<style>` (non-scoped, @import v2-styles). Thêm 1 block `<style scoped>` MỚI ngay dưới block `<style>` hiện có:

```vue
<style>
@import '@/assets/scss/v2-styles.scss';
</style>

<style scoped>
::v-deep .modal-dialog {
    max-width: 1200px;
}
::v-deep .modal-body {
    max-height: 80vh;
    overflow-y: auto;
}
</style>
```

- [ ] **Step 8: Verify browser** (xem Task 4)

---

## Task 4: Verify browser thủ công

- [ ] **Step 1: Chạy dev server hrm-client** (nếu chưa chạy)

```bash
cd D:\laragon\www\hrm\hrm-client
npm run dev
```

- [ ] **Step 2: Kiểm tra màn chi tiết**

Vào `/assign/form-templates/{id}` của 1 mẫu có section/group/câu hỏi:
- Footer có nút "In mẫu phiếu" (primary, icon máy in).
- Bấm → mở modal "Xem trước mẫu phiếu in".
- Header: Tên KH/Tên DA/Mã DA/Phân loại TRỐNG; Nhóm ngành + Nhóm giải pháp ĐIỀN đúng; "Ngày khảo sát" hiện `...../...../.....` đứng TRÊN "Người khảo sát" (trống); KHÔNG còn Giai đoạn dự án / Ứng dụng / Địa chỉ dự án.
- Bảng: cột 3 tên "Đáp án/giá trị thu thập cho tôi", mọi ô đáp án TRỐNG. Đánh số A/I/1/1.1 đúng.
- Bấm "In" → mở cửa sổ in trình duyệt, layout A4 đúng.

- [ ] **Step 3: Kiểm tra màn danh sách**

Vào `/assign/form-templates`:
- Mỗi dòng có nút "In mẫu phiếu" (icon máy in) đứng CẠNH nút "Sửa".
- Hiện ở MỌI trạng thái (Nháp / Hoạt động / Khoá).
- Bấm → loading → mở modal preview giống màn chi tiết (header đúng, cột đáp án trống). Bấm "In" hoạt động.

- [ ] **Step 4: Edge cases**

- Mẫu KHÔNG có section/câu hỏi → modal hiện header + bảng chỉ có dòng tiêu đề cột (không lỗi).
- Mẫu có câu hỏi type=parent (children) → in lồng 1.1, 1.2.
- Mẫu có section chứa group vs section chứa câu hỏi trực tiếp → cả 2 render đúng.
- Đóng modal (X / nút Đóng / click backdrop) → đóng bình thường.

---

## Self-Review (đã thực hiện khi viết plan)

- **Spec coverage:** Nút list cạnh Sửa (T3.S3) ✓; nút detail (T2.S5) ✓; modal preview (T2.S6/T3.S6) ✓; component riêng không sửa SurveyPrintSheet (T1) ✓; header bỏ 3 trường + thêm Ngày khảo sát + nhóm ngành/GP điền từ template (T1 template + printHeader T2.S3/T3.S5) ✓; cột đổi tên + để trống (T1 props default + ô `<td></td>` rỗng) ✓; KHÔNG BE/permission/migration ✓.
- **Placeholder scan:** không còn TBD/TODO; mọi step có code thật.
- **Type consistency:** prop `header = { scopeName, industryName }` đồng nhất giữa component (T1), detail `printHeader` computed (T2.S3), list `printHeader` data (T3.S2/S5). Method `printSheet` + ref `printSheet` đồng nhất cả 2 màn. `getPrintStyles()` + `$refs.printArea` khớp hợp đồng component.

---

### Checkpoint — 2026-06-06 (CODE DONE)
Vừa hoàn thành: Task 1+2+3 (subagent-driven, Opus 4.8). Mỗi task qua 2 vòng review (spec + code quality) → Approved.
- T1: tạo `components/FormTemplatePrintSheet.vue`.
- T2: `pages/assign/form-templates/_id/index.vue` — nút "In mẫu phiếu" footer + modal preview + `handlePrint`. (Fix review: rename method `printSheet`→`handlePrint` tránh trùng tên ref; bỏ `@hide` thừa.)
- T3: `pages/assign/form-templates/index.vue` — row action "In mẫu phiếu" cạnh "Sửa" (mọi trạng thái) + fetch detail lấy sections + modal + `handlePrint`.
Quy ước thống nhất 2 màn: ref component = `printSheet`, method in = `handlePrint`.
Đang làm dở: không.
Bước tiếp theo: Task 4 — user verify browser (npm run dev). Lưu ý kiểm tra: dòng câu hỏi con hiển thị số "1.1" 2 lần (STT + đầu cột Nội dung) — đây là giữ đúng layout SurveyPrintSheet; nếu muốn bỏ thì gỡ 2 dòng interpolation số trong cột Nội dung của child.
Blocked: không.
