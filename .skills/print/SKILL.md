# Skill: In báo cáo / danh sách (Print)

## Mục đích
Đảm bảo MỌI chức năng "In" trong project có **header và footer giống nhau** (logo công ty, tiêu đề HOA, phần ký tên), tránh mỗi màn một kiểu.

**Phạm vi bắt buộc**: header (ảnh + tiêu đề) và footer (ngày + người lập + ký họ tên). Phần thân bảng tự do tuỳ màn.

Khi user yêu cầu:
- "Thêm chức năng in"
- "Bổ sung in cho màn ..."
- "Tham khảo màn X in cho màn Y"

→ Đọc skill này TRƯỚC khi viết code.

---

## Stack & Plugin

| Layer | Công nghệ |
|---|---|
| Plugin in | `hrm-client/plugins/print-content.js` (đã có sẵn, expose `Vue.prototype.$printContent`) |
| Cách hoạt động | `$printContent()` mở **window mới**, copy `outerHTML` của element `#content` (default selector) sang, apply CSS `pdf.css` rồi gọi `window.print()` |
| Layout | Page in dùng layout mặc định (KHÔNG cần khai báo `layout:`) |
| Loading bar | `this.$nuxt.$loading` (cần guard tồn tại) |

**KHÔNG dùng** `window.print()` trực tiếp ở index page — sẽ in cả sidebar/topbar/avatar/filter.

---

## Pattern chuẩn HRM

Tạo **page Vue riêng** (tách khỏi index):

```
pages/[module]/[feature]/
├── index.vue       ← danh sách + nút "In" (mở tab mới)
└── print.vue       ← page in: nhận query filter, gọi API, render bảng
```

### Bước 1 — Index: thêm hàm `printReport()` mở print page kèm filter

```javascript
import { buildQueryString } from '@/utils/url-action'

methods: {
    printReport() {
        const params = { ...this.buildApiFilters() } // hoặc { ...this.formFilter }
        Object.keys(params).forEach((key) => {
            if (params[key] === '' || params[key] === null || params[key] === undefined) {
                delete params[key]
            }
        })
        delete params.current_page
        delete params.per_page

        const query = buildQueryString(params)
        const url = `/[module]/[feature]/print${query}`
        window.open(url, '_blank')
    },
}
```

Bind vào nút In trên template:
```vue
<V2BaseButton primary size="sm" @click="printReport">
    <template #prefix><i class="ri-printer-line"></i></template>
    In báo cáo
</V2BaseButton>
```

### Bước 2 — Print page (`print.vue`): skeleton

> **CỰC KỲ QUAN TRỌNG**: wrapper PHẢI có `id="content"`. `$printContent()` plugin tìm selector này, nếu không khớp sẽ in cả trang Nuxt (sidebar, topbar, avatar...).

```vue
<template>
    <div style="background-color: #fff; min-height: 900px">
        <!-- Wrapper #content: $printContent sẽ chỉ in vùng này -->
        <div id="content" class="container-fluid mt-3">
            <!-- Nút In: ẩn khi in giấy -->
            <div class="mb-2 no-print">
                <button class="btn btn-primary" @click="$printContent ? $printContent() : window.print()">
                    <i class="fa fa-print"></i> In
                </button>
            </div>

            <div v-if="errorMessage" class="alert alert-danger no-print">
                {{ errorMessage }}
            </div>

            <!-- HEADER: ảnh header công ty hiện tại -->
            <div class="row mb-3">
                <img :src="headerImageSrc" alt width="100%" />
            </div>

            <h4 class="text-center font-weight-bold mb-3">
                TÊN BÁO CÁO HOA TOÀN BỘ
            </h4>

            <!-- Bảng dữ liệu -->
            <table class="table table-bordered table-sm print-table">
                <thead class="thead-light">
                    <tr>
                        <!-- ... các cột -->
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in rows" :key="index">
                        <!-- ... cells -->
                    </tr>
                </tbody>
            </table>

            <!-- FOOTER: ngày + người lập + ký họ tên -->
            <div class="signature-container">
                <div class="signature">
                    Ngày ...., tháng ...., năm ....
                    <br />
                    <strong>Người lập</strong>
                    <br />
                    (Ký, họ tên)
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { buildQueryString } from '@/utils/url-action'

export default {
    head() {
        return { title: 'In báo cáo ...' }
    },
    data() {
        return {
            rows: [],
            companyHeader: '',
            errorMessage: '',
            isLoaded: false,
            fallbackHeader: require('@/assets/images/info-tpe.jpg'),
        }
    },
    computed: {
        headerImageSrc() {
            return this.companyHeader || this.fallbackHeader
        },
    },
    mounted() {
        this.getData()
    },
    methods: {
        async getData() {
            // Loading bar có thể chưa init khi tab mới mở → guard
            if (this.$nuxt && this.$nuxt.$loading && typeof this.$nuxt.$loading.start === 'function') {
                this.$nuxt.$loading.start()
            }
            try {
                const params = { ...this.$route.query, current_page: 1, per_page: 10000 }
                const url = `[module]/[feature]${buildQueryString(params)}`
                const response = await this.$store.dispatch('apiGetMethod', url)

                this.rows = response?.data || []
                this.companyHeader = response?.company?.header || ''
                this.isLoaded = true
            } catch (error) {
                console.error('[print] Error loading data:', error)
                this.errorMessage = error?.response?.data?.message || error?.message || 'Lỗi khi tải dữ liệu'
                this.isLoaded = true
            } finally {
                if (this.$nuxt && this.$nuxt.$loading && typeof this.$nuxt.$loading.finish === 'function') {
                    this.$nuxt.$loading.finish()
                }
            }
        },
    },
}
</script>

<style lang="scss">
/* KHÔNG dùng `scoped`: $printContent copy outerHTML sang window mới, scoped CSS sẽ không apply */
.print-table {
    font-size: 11px;
    width: 100%;

    th {
        background-color: #d9e1f2 !important;
        color: #0f172a;
        font-weight: bold;
        vertical-align: middle;
    }

    td { vertical-align: middle; }

    /* Phân cấp màu giống file Excel: */
    .row-total td { background-color: #d1fae5 !important; font-weight: bold; }
    .row-company td { background-color: #dbeafe !important; font-weight: bold; }
    .row-dept td { background-color: #f1f5f9 !important; font-weight: bold; }
}

.signature-container {
    display: flex;
    justify-content: flex-end;
    margin-top: 30px;
    margin-bottom: 60px;
    font-size: 14px;
}

.signature {
    text-align: center;
    width: 220px;
}

@media print {
    .print-table { font-size: 9px; }
}
</style>
```

---

## Lấy header công ty hiện tại (BẮT BUỘC)

KHÔNG hardcode `info-tpe.jpg`. Mỗi công ty có ảnh header riêng — lấy từ field `companies.header`.

### Cách 1 (KHUYÊN DÙNG): BE đính kèm `company` vào response

**BE Service**:
```php
use Modules\Human\Entities\Company;

private function getCurrentCompanyForExport(): array
{
    $companyId = auth()->user()->current_company_role ?? null;
    if (!$companyId) {
        return ['name' => '', 'header' => null];
    }
    $company = Company::query()->find($companyId);
    if (!$company) {
        return ['name' => '', 'header' => null];
    }
    return [
        'name' => $company->name ?? '',
        'header' => $company->header ?: null,
    ];
}

// Trong getReportData() — đính kèm vào summary:
$summary['company'] = $this->getCurrentCompanyForExport();
```

**BE Resource** (nếu có resource transformer):
```php
$response->company = $summary['company'] ?? ['name' => '', 'header' => null];
```

**FE print.vue** chỉ cần đọc `response.company.header`:
```javascript
this.companyHeader = response?.company?.header || ''
```

### Cách 2: FE tự gọi API riêng

Nếu BE chưa đính kèm và không tiện sửa, gọi thêm API `me` hoặc `companies/{currentCompanyId}` để lấy header. Nhưng đây là **fallback**, ưu tiên Cách 1.

### Fallback ảnh

Nếu công ty chưa cấu hình header → dùng `info-tpe.jpg` mặc định:
```javascript
fallbackHeader: require('@/assets/images/info-tpe.jpg'),
// computed:
headerImageSrc() {
    return this.companyHeader || this.fallbackHeader
},
```

---

## Quy ước bắt buộc cho print page

| Phần | Quy tắc |
|---|---|
| **Wrapper `id="content"`** | BẮT BUỘC. `$printContent` plugin tìm selector `#content` để chỉ in vùng đó. Nếu thiếu, sẽ in cả trang Nuxt (sidebar/avatar/topbar) |
| **Header ảnh** | `<img :src="headerImageSrc" width="100%" />` — lấy từ `companies.header` của user, fallback `@/assets/images/info-tpe.jpg`. KHÔNG hardcode |
| **Tiêu đề** | `<h4>` HOA toàn bộ, `font-weight-bold`, `text-center` |
| **Footer ký tên** | `signature-container` flex right + `signature` width 220px, 3 dòng "Ngày..." / "**Người lập**" / "(Ký, họ tên)" |
| **Margin cuối** | `margin-bottom: 60px` chừa chỗ ký tay |
| **Class `.no-print`** | Bao quanh nút "In" và mọi UI không cần in (alert, debug info) |
| **Style KHÔNG `scoped`** | `$printContent` copy outerHTML sang window mới → scoped CSS không apply, phải để global |
| **Loading bar** | KHÔNG dùng `this.$nuxt.$loading.start()` trực tiếp — wrap bằng `if (this.$nuxt && this.$nuxt.$loading && typeof this.$nuxt.$loading.start === 'function')`. Tab mới mở qua `window.open` chưa khởi tạo loading bar ngay tại `mounted()` |
| **Nút In** | `@click="$printContent ? $printContent() : window.print()"` — fallback `window.print()` nếu plugin chưa sẵn sàng |
| **Phân cấp màu** | Nếu là báo cáo nhóm, dùng cùng màu với file Excel để thống nhất: Tổng `#d1fae5`, Công ty `#dbeafe`, Phòng `#f1f5f9` |
| **API call** | Gọi cùng endpoint với index, `per_page: 10000` để lấy hết. KHÔNG tạo endpoint `/print` riêng |

---

## Plugin `$printContent` chi tiết

File: `hrm-client/plugins/print-content.js`

**Cách hoạt động**:
1. Tìm element theo `selector` (default `#content`), fallback `.print-wrapper / .container / #__nuxt / #app`
2. Mở **window mới** kích thước 920×1600
3. Copy `outerHTML` của element vào `<body class="document-editor">` của window mới
4. Inject CSS: `/css/pdf.css`, `/ckeditor/css/editor.css`, `/css/print-app.css` + base styles (`@page margin`, `.no-print`, ...)
5. Gọi `printWindow.print()` sau khi window load xong

**Custom options** (nếu cần):
```javascript
this.$printContent({
    selector: '#my-custom-id',         // override default '#content'
    title: 'In báo cáo',
    pageMargin: '15mm 10mm',
    stylesheets: ['/css/extra.css'],   // append thêm
})
```

---

## Checklist khi thêm In báo cáo

1. [ ] **BE**: Thêm `getCurrentCompanyForExport()` vào service, đính `$summary['company']` vào `getReportData()`
2. [ ] **BE**: Resource transformer expose `$response->company`
3. [ ] **FE Index**: Thêm hàm `printReport()` build query và `window.open(url, '_blank')`
4. [ ] **FE Index**: Bind nút "In" gọi `printReport`
5. [ ] **FE Print**: Tạo file `print.vue` cùng folder với index
6. [ ] **FE Print**: Wrapper có `id="content"` (BẮT BUỘC)
7. [ ] **FE Print**: `data()` có `companyHeader`, `fallbackHeader: require('@/assets/images/info-tpe.jpg')`
8. [ ] **FE Print**: `computed.headerImageSrc` fallback chuẩn
9. [ ] **FE Print**: `getData()` đọc `response.company.header` + guard `$nuxt.$loading`
10. [ ] **FE Print**: Render header logo + tiêu đề + bảng + footer ký tên (theo skeleton)
11. [ ] **FE Print**: `<style>` KHÔNG dùng `scoped`
12. [ ] Test: filter ở index → bấm In → mở tab mới → check data đúng → bấm In trong tab → window in mới hiện ra chỉ có nội dung báo cáo (không có sidebar/avatar)

---

## File tham chiếu

| File | Vai trò |
|---|---|
| `hrm-client/plugins/print-content.js` | Plugin `$printContent` (không sửa) |
| `hrm-client/pages/decision/accept-personnel/index.vue` | FE index: nút In với `:to` router-link |
| `hrm-client/pages/decision/accept-personnel/print.vue` | Print page: danh sách phẳng, header tĩnh (chưa dùng companies header) |
| `hrm-client/pages/assign/report/prospective-projects/index.vue` | FE index: nút In gọi `window.open` |
| `hrm-client/pages/assign/report/prospective-projects/print.vue` | Print page: báo cáo phân cấp, header từ `companies.header` |
| `hrm-api/Modules/Assign/Services/Report/ProspectiveProjectsReportService.php` | BE service đính `company` vào summary |
| `hrm-api/Modules/Assign/Transformers/ProspectiveProjectsReportResource/ProspectiveProjectsReportResource.php` | BE resource expose `$response->company` |

---

## Cách gọi skill

Khi user yêu cầu thêm In cho màn nào:

```
@.skills/print/SKILL.md

Thêm chức năng In cho màn [đường dẫn].
Cấu trúc cột: [danh sách cột]
Phân cấp (nếu có): [Tổng → Công ty → Phòng ban → ...]
```

→ Phải tuân thủ skeleton trong skill này, **không tự sáng tạo header/footer khác**, **không hardcode `info-tpe.jpg`**.

## Liên quan

Skill này song song với `.skills/export-excel/SKILL.md` (xuất Excel). Hai chức năng dùng chung:
- Header: ảnh từ `companies.header`
- Footer: 3 dòng "Ngày..." / "Người lập" / "(Ký, họ tên)"
- Phân cấp màu: Tổng/Công ty/Phòng ban giống nhau

→ Khi thêm cùng lúc Excel + In, dùng cả 2 skill và đảm bảo header/footer thống nhất.
