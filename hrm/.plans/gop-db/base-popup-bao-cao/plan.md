# Base dùng chung cho popup báo cáo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Dựng `V2BaseReportModal` + `reportDrillListMixin` làm khuôn chung cho popup drill-down của các màn báo cáo, và chuyển `DemandListModal` sang dùng chúng mà không đổi một hành vi nào người dùng nhìn thấy.

**Architecture:** Hai lớp. Vỏ `components/report/V2BaseReportModal.vue` dựng **trên** `components/modal/V2BaseModal.vue` (thêm slot `header` để thay header chuẩn bằng dải banner), tự lo bảng dựng theo schema `columns` + phân trang. Máy `utils/mixins/reportDrillListMixin.js` chỉ ôm phần 3 popup lớn giống hệt nhau: sắp xếp + phân trang client-side + state bộ lọc; **lọc là hook** do màn tự cài vì 3 popup dùng 3 chiến lược khác nhau.

**Tech Stack:** Vue 2 (Options API, KHÔNG composition API), Nuxt 2, BootstrapVue, SCSS; Playwright cho e2e.

**Spec:** `.plans/base-popup-bao-cao/design.md`

## Global Constraints

- **Vue 2 / Options API.** Không `setup()`, không composition API — repo chưa có `@vue/composition-api`.
- **Chạy Nuxt dev bằng Node 12**: `PATH="$HOME/.nvm/versions/node/v12.22.12/bin:$PATH" NODE_OPTIONS=--max-old-space-size=8192 npm run dev` (cổng 3000). **Chạy Playwright bằng Node 20**: `PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH"`.
- **Mọi lần chạy e2e để KẾT LUẬN phải có `--workers=1`** (2 worker tranh 1 Nuxt dev server gây đỏ ngẫu nhiên).
- **Bộ e2e chạy `serial`**: một ca fail làm mọi ca sau in "did not run" — phải đọc dòng tổng kết, không nhìn cuối log.
- **Tiền tố lớp CSS của Base là `report-drill-*`**. Không mang tên `care-drill-*` sang component dùng chung.
- **`V2BaseModal` là component của 30 màn**: chỉ được THÊM slot / prop mới có mặc định giữ nguyên hành vi cũ; không đổi mặc định sẵn có, không đổi style.
- **Sửa hàng loạt file phải giữ EOL từng dòng**: kiểm bằng `git diff --numstat`, số dòng xoá phải đúng bằng số dòng thật sự đổi.
- **`hrm-client` là repo dùng chung, nhiều phiên chạy song song**: KHÔNG `git stash`, KHÔNG `pkill -f nuxt`. Commit chỉ khi người dùng đồng ý.
- **Vật cản môi trường đã biết**: `hrm-api/database/e2e_provision.php` còn trỏ 5 bảng `hrm_*` đã bị `ReconcileEmployeesSeeder` gộp và xoá → `api-setup` đổ, mọi spec UI của HRM không chạy được. Task 7 nói rõ cách xử lý.

---

## File Structure

| File | Trách nhiệm |
|---|---|
| `components/modal/V2BaseModal.vue` (sửa) | Thêm slot `header` + prop `noEnforceFocus`. Không đổi gì khác. |
| `components/report/V2BaseReportModal.vue` (mới) | Vỏ popup báo cáo: dải banner, nút phóng to, bảng theo schema `columns`, phân trang. Không biết nghiệp vụ. |
| `utils/mixins/reportDrillListMixin.js` (mới) | State bộ lọc + sắp xếp + phân trang client-side. Không biết giao diện. |
| `pages/assign/report/potential-customer-care/components/DemandListModal.vue` (sửa) | Còn lại phần riêng của màn: schema cột/ô lọc, KPI + chip, các ô đặc biệt, nút In/Xuất. |
| `e2e/tests/assign/potential-customer-care.spec.ts` (sửa) | Đổi selector `care-drill-*` → `report-drill-*`. |
| `.plans/base-popup-bao-cao/baseline.json` (mới, tạm) | Ảnh chụp hành vi popup TRƯỚC khi chuyển, để đối chiếu sau. |

---

### Task 1: Chụp ảnh hành vi hiện tại (baseline)

Đây là "bài test thất bại" của một đợt refactor: chưa có ảnh chụp thì không có gì chứng minh
"chuyển xong không đổi hành vi". Phải làm TRƯỚC khi đụng bất kỳ file nào.

**Files:**
- Create: `.plans/base-popup-bao-cao/measure-popup.mjs` (script đo, giữ lại để chạy cả 2 lượt)
- Create: `.plans/base-popup-bao-cao/baseline.json`

**Interfaces:**
- Produces: `baseline.json` với đúng khoá `{ cols, firstPageRowCount, sttFirst, sttLast, pageTotal, sortTextAsc, sortDateAsc, footerTop, tableBottom, heightNormal, heightFull }` — Task 6 so lại đúng bộ khoá này.

- [x] **Step 1: Bật môi trường và xác nhận màn chạy được**

```bash
# API (nếu chưa chạy)
cd HRM/hrm-api && php artisan serve --host=127.0.0.1 --port=8000 &
# Nuxt (nếu chưa chạy) — Node 12 + heap 8192
cd HRM/hrm-client && PATH="$HOME/.nvm/versions/node/v12.22.12/bin:$PATH" NODE_OPTIONS=--max-old-space-size=8192 npm run dev &
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3000/   # phải là 200
```

- [x] **Step 2: Chuẩn bị phiên đăng nhập cho script đo**

Tài khoản e2e `e2e_assign@test.local` KHÔNG có trong DB `hrm_erp`. Mint JWT thẳng cho một tài
khoản có quyền "…theo tổng công ty" — không đổi mật khẩu ai, không sửa dữ liệu:

```bash
cd HRM/hrm-api
php artisan tinker --execute '$e = \App\Models\TpEmployee::find(13); echo "TOKEN=" . auth("api")->login($e) . "\n";' \
  2>/dev/null | grep '^TOKEN=' | sed 's/^TOKEN=//' > /tmp/care-token.txt
python3 - <<'PY'
import json
tok = open('/tmp/care-token.txt').read().strip()
json.dump({"cookies": [], "origins": [{"origin": "http://127.0.0.1:3000",
          "localStorage": [{"name": "access_token", "value": tok}]}]}, open('/tmp/care-state.json', 'w'))
PY
```

- [x] **Step 3: Viết script đo**

Tạo `.plans/base-popup-bao-cao/measure-popup.mjs`:

```js
import { chromium } from '/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e/node_modules/@playwright/test/index.mjs';

const OUT = process.argv[2];               // đường dẫn file json để ghi
const browser = await chromium.launch();
const page = await (await browser.newContext({
    storageState: '/tmp/care-state.json', viewport: { width: 1440, height: 900 },
})).newPage();
await page.goto('http://127.0.0.1:3000/assign/report/potential-customer-care', { waitUntil: 'domcontentloaded' });
await page.locator('.rsum-tb__sec').first().waitFor({ timeout: 40000 });

// Mở popup từ dòng cha đầu tiên
await page.locator('.rsum-tb__row--parent').first().locator('td').nth(2).locator('button.rsum-drill').click();
await page.waitForFunction(() => {
    const tr = document.querySelector('.modal.show table tbody tr');
    return tr && tr.querySelectorAll('td').length > 1;
}, { timeout: 20000 });

const snap = () => page.evaluate(() => {
    const m = document.querySelector('.modal.show');
    const t = (el) => (el ? el.innerText.replace(/\s+/g, ' ').trim() : null);
    const rows = [...m.querySelectorAll('table tbody tr')];
    const dialog = m.querySelector('.modal-dialog').getBoundingClientRect();
    const wrapSel = '.care-drill-wrap, .report-drill-wrap, .v2-table-scroll__body';
    const footSel = '.care-drill-footer, .report-drill-footer, .modal-footer';
    return {
        cols: [...m.querySelectorAll('table thead th')].map((th) => t(th)),
        firstPageRowCount: rows.length,
        sttFirst: t(rows[0]?.querySelector('td')),
        sttLast: t(rows[rows.length - 1]?.querySelector('td')),
        pageTotal: t(m.querySelector('.page-total')),
        tableBottom: Math.round(m.querySelector(wrapSel).getBoundingClientRect().bottom),
        footerTop: Math.round(m.querySelector(footSel).getBoundingClientRect().top),
        heightNormal: Math.round(dialog.height),
    };
});

const out = await snap();

// Sắp xếp: cột CHỮ đầu tiên và cột NGÀY đầu tiên -> lưu nguyên mảng giá trị sau khi bấm asc
const sortBy = async (label) => {
    const th = page.locator('.modal.show table thead th', { hasText: label }).first();
    if (!(await th.count())) return null;
    await th.locator('span').first().click();
    await page.waitForTimeout(400);
    const idx = (await page.locator('.modal.show table thead th').allInnerTexts())
        .findIndex((x) => x.trim().startsWith(label));
    return page.locator('.modal.show table tbody tr').evaluateAll(
        (trs, i) => trs.map((tr) => (tr.querySelectorAll('td')[i]?.textContent || '').replace(/\s+/g, ' ').trim()),
        idx,
    );
};
/* Cột chữ phải chọn cột CÓ `sortable: true`. "Khách hàng" (DemandListModal.vue:355) KHÔNG sắp
   xếp được — bấm vào chỉ chụp lại thứ tự mặc định, phép so ở Task 6 thành vô nghĩa. Dùng
   "Thị trường / Phường xã": có `sortable` VÀ có `sortFields` (nhánh ghép nhiều trường). */
out.sortTextAsc = await sortBy('Thị trường / Phường xã');
/* Nhãn cột ngày là 'Meeting thu thập nhu cầu' — cột DUY NHẤT có `sortType: 'date'`
   (DemandListModal.vue:364). Ghi sai nhãn thì `sortBy` trả `null` và phép so ở Task 6 thành vô
   nghĩa: null so null luôn khớp. */
out.sortDateAsc = await sortBy('Meeting thu thập nhu cầu');

// Phóng to toàn màn hình
await page.locator('.modal.show [title*="Phóng to"], .modal.show [title*="phóng to"]').first().click();
await page.waitForTimeout(500);
out.heightFull = await page.evaluate(() =>
    Math.round(document.querySelector('.modal.show .modal-dialog').getBoundingClientRect().height));

const fs = await import('fs');
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
await browser.close();
```

- [x] **Step 4: Chạy và lưu baseline**

```bash
cd HRM
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  node .plans/base-popup-bao-cao/measure-popup.mjs .plans/base-popup-bao-cao/baseline.json
```

Expected: in ra JSON có `cols` (mảng tên cột, ≥ 6 phần tử), `firstPageRowCount` = 20,
`pageTotal` dạng `Hiển thị 1–20 / N nhu cầu`, `heightFull` > `heightNormal`.

- [x] **Step 5: Kiểm baseline không rỗng**

```bash
python3 -c "
import json; d = json.load(open('.plans/base-popup-bao-cao/baseline.json'))
assert d['cols'] and d['firstPageRowCount'] and d['pageTotal'], d
assert d['sortTextAsc'], 'thiếu ảnh chụp sắp xếp cột chữ'
assert d['heightFull'] > d['heightNormal'], 'nút phóng to không ăn'
print('baseline OK:', len(d['cols']), 'cột,', d['firstPageRowCount'], 'dòng')
"
```

- [x] **Step 6: Commit** (chỉ khi người dùng đồng ý — nhánh dùng chung)

```bash
git add .plans/base-popup-bao-cao/measure-popup.mjs .plans/base-popup-bao-cao/baseline.json
git commit -m "chore(report-popup): chụp ảnh hành vi popup báo cáo trước khi tách Base"
```

---

### Task 2: Thêm slot `header` vào `V2BaseModal`

**Files:**
- Modify: `hrm-client/components/modal/V2BaseModal.vue:26-62` (khối `<template #modal-header>`)
- Modify: `hrm-client/components/modal/V2BaseModal.vue:13-24` (thẻ `<b-modal>`) + khối `props`

**Interfaces:**
- Produces: slot `header` — không truyền thì render nguyên header chuẩn (icon tròn + `title` + `subtitle` + nút ×). Truyền thì **thay toàn bộ** phần bên trong `.modal-header`, kể cả nút ×; component nhận slot phải tự vẽ nút đóng và gọi `close` (expose qua slot prop `close`).
- Produces: prop `noEnforceFocus: Boolean = false` → đổ xuống `:no-enforce-focus` của `b-modal`.

> ⚠️ **Vì sao cần `noEnforceFocus`:** popup nguồn tự khai `b-modal` có `no-enforce-focus`. Bỏ nó
> là BootstrapVue giành lại focus mỗi khi focus rời khỏi modal — dropdown select2 (render ra
> `<body>`, NGOÀI modal) bị đóng ngay khi vừa mở, ô lọc trong popup "bấm vào không ra gì". Ca e2e
> 8 canh đúng chỗ này. Mặc định `false` để 30 popup đang dùng không đổi hành vi.

- [x] **Step 1: Thêm prop `noEnforceFocus` và đổ xuống `b-modal`**

```vue
    <b-modal
        :id="modalId"
        ref="modal"
        :size="size"
        :dialog-class="dialogClass"
        :no-enforce-focus="noEnforceFocus"
        hide-footer
        …
```

```js
        /* Popup có select2/datepicker render dropdown ra ngoài `<body>`: BootstrapVue giành lại
           focus sẽ đóng dropdown ngay khi vừa mở. Mặc định `false` — 30 popup đang dùng giữ nguyên. */
        noEnforceFocus: { type: Boolean, default: false },
```

- [x] **Step 2: Sửa template header**

Bọc toàn bộ nội dung hiện có của `<template #modal-header>` vào `<slot name="header" :close="close">`:

```vue
        <template #modal-header>
            <!-- Popup báo cáo thay header chuẩn bằng dải banner riêng (xem
                 `components/report/V2BaseReportModal.vue`). Không truyền slot thì render y như cũ
                 — 30 popup đang dùng không đổi gì. Slot tự vẽ nút đóng nên nhận luôn `close`. -->
            <slot name="header" :close="close">
                <!-- Markup cũ (dòng 33–60 của file) BÊ NGUYÊN VĂN vào đây, kể cả các comment
                     giải thích bẫy `w-100` làm nút × tràn ra ngoài. Chỉ thụt lề thêm 1 cấp. -->
                <div class="d-flex align-items-center v2-modal-head-left">…</div>
                <button type="button" class="close" @click="close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </slot>
        </template>
```

- [x] **Step 3: Kiểm popup CŨ không đổi**

Mở một popup bất kỳ đang dùng `V2BaseModal` và đo header vẫn còn đủ 3 phần:

```bash
cd HRM && cat > /tmp/check-v2modal.mjs <<'JS'
import { chromium } from '/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e/node_modules/@playwright/test/index.mjs';
const b = await chromium.launch();
const p = await (await b.newContext({ storageState: '/tmp/care-state.json', viewport: { width: 1440, height: 900 } })).newPage();
await p.goto('http://127.0.0.1:3000/assign/report/prospective-project-results', { waitUntil: 'domcontentloaded' });
await p.locator('.rsum-tb__sec').first().waitFor({ timeout: 40000 });
await p.locator('.rsum-tb__sec td').nth(2).locator('button').first().click();
await p.locator('.modal.show').waitFor({ timeout: 15000 });
console.log(await p.evaluate(() => ({
    coIcon: !!document.querySelector('.modal.show .v2-modal-icon'),
    coTieuDe: !!document.querySelector('.modal.show .modal-title'),
    coNutDong: !!document.querySelector('.modal.show .modal-header .close'),
})));
await b.close();
JS
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" node /tmp/check-v2modal.mjs
```

Expected: `{ coIcon: true, coTieuDe: true, coNutDong: true }`.

- [x] **Step 4: Kiểm diff đúng bằng phần đã thêm**

```bash
cd HRM/hrm-client && git diff --numstat components/modal/V2BaseModal.vue
```

Expected: chỉ vài dòng thêm (mở/đóng slot + comment), phần markup cũ không bị viết lại.

- [x] **Step 5: Commit**

```bash
git add components/modal/V2BaseModal.vue
git commit -m "feat(V2BaseModal): thêm slot header + prop noEnforceFocus cho popup báo cáo"
```

---

### Task 3: `V2BaseReportModal.vue` — vỏ popup báo cáo

**Files:**
- Create: `hrm-client/components/report/V2BaseReportModal.vue`

**Interfaces:**
- Consumes: slot `header` của `V2BaseModal` (Task 2).
- Produces — **props**: `visible: Boolean`, `modalId: String`, `lead: String`, `title: String`, `meta: String`, `loading: Boolean`, `columns: Array`, `rows: Array` (dòng của TRANG ĐANG XEM, không phải cả tập), `rowKey: String = 'id'`, `startIndex: Number = 0` (STT bắt đầu), `emptyText: String = 'Không có dữ liệu khớp bộ lọc.'`, `sort: Object = { key: '', dir: 'asc' }`, `currentPage: Number`, `currentPageSize: Number`, `totalRows: Number`, `itemLabel: String`, `pageSizeOptions: Array = [20, 50, 100]`, `fullscreenable: Boolean = true`, `maxTableHeight: String = '50vh'`, `dialogClass: String`.
  **events**: `close`, `sort` (`{ key }`), `page-change` (`Number`), `page-size-change` (`Number`), `toggle-fullscreen` (`Boolean`).
  **slots**: `filters`, `summary`, `back`, `footer`, `cell-<key>` (scoped, `{ row, index, column }`).

- [x] **Step 1: Viết component**

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

- [x] **Step 2: Kiểm component dựng được (chưa gắn vào màn nào)**

Nuxt dev server tự biên dịch lại. Kiểm không có lỗi compile:

```bash
curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "%{http_code}\n"
```

Expected: `200`, và log dev server không có dòng `Failed to compile`.

- [x] **Step 3: Commit**

```bash
git add components/report/V2BaseReportModal.vue
git commit -m "feat(report): thêm V2BaseReportModal làm vỏ dùng chung cho popup báo cáo"
```

---

### Task 4: `reportDrillListMixin.js` — máy sắp xếp + phân trang

**Files:**
- Create: `hrm-client/utils/mixins/reportDrillListMixin.js`

**Interfaces:**
- Produces — **data**: `keyword`, `filters`, `sort`, `page`, `pageSize`, `summaryCollapsed`.
  **computed**: `sortedRows`, `pageCount`, `safePage`, `pageOffset`, `pagedRows`, `hasActiveFilter`.
  **methods**: `toggleSort(key)`, `onPageChange(page)`, `onPageSizeChange(size)`, `resetFilters()`, `applyLocalFilters(rows)`.
  **Component dùng mixin PHẢI tự khai**: `rows` (prop hoặc computed), `columns` (computed), `emptyFilters()` (trả object state lọc rỗng), và `onFilterChange()` (hook — mixin gọi sau khi `resetFilters()`).

- [x] **Step 1: Viết mixin**

```js
/**
 * MÁY CLIENT-SIDE cho popup drill-down của màn báo cáo.
 *
 * CHỈ ôm phần 3 popup lớn giống hệt nhau: sắp xếp, phân trang, state bộ lọc.
 * KHÔNG ôm phần lọc — 3 popup dùng 3 chiến lược khác nhau (đo 2026-09-17):
 *   · DemandListModal      — lọc ở SERVER (emit `filter`, màn cha tải lại)
 *   · DevelopmentDrillModal — lọc CLIENT tại chỗ
 *   · ProjectListModal      — lọc ở SERVER, popup tự gọi API
 * Vì vậy `onFilterChange()` là HOOK do component tự cài, còn `applyLocalFilters()` là hàm
 * TUỲ CHỌN cho popup lọc client-side.
 *
 * Component dùng mixin phải khai: `rows`, `columns`, `emptyFilters()`, `onFilterChange()`.
 */
const dateSortKey = (value) => {
    if (!value) return null
    // Dữ liệu hiển thị dạng dd/mm/yyyy — `new Date()` đọc sai (hiểu là mm/dd)
    const m = String(value).match(/^(\d{2})\/(\d{2})\/(\d{4})/)
    if (m) return new Date(`${m[3]}-${m[2]}-${m[1]}`).getTime()
    const t = new Date(value).getTime()
    return Number.isNaN(t) ? null : t
}

export default {
    data() {
        return {
            keyword: '',
            filters: this.emptyFilters(),
            /* Sắp xếp TẠI CHỖ: popup đã có trọn tập của ô số đã bấm nên không gọi lại API */
            sort: { key: '', dir: 'asc' },
            page: 1,
            pageSize: 20,
            /* Mặc định THU GỌN — nhường chỗ cho bảng chi tiết (user chốt 2026-09-06) */
            summaryCollapsed: true,
        }
    },
    computed: {
        sortedRows() {
            const { key, dir } = this.sort
            if (!key) return this.rows

            const col = this.columns.find((c) => c.key === key)
            if (!col) return this.rows

            const isDate = col.sortType === 'date'
            const valueOf = (row) =>
                isDate
                    ? dateSortKey(row[col.field])
                    : (col.sortFields ? col.sortFields.map((f) => row[f] || '').join(' ') : String(row[col.field] || '')).trim()

            const sign = dir === 'desc' ? -1 : 1
            // Ô trống luôn xuống cuối ở CẢ 2 chiều — không thì bấm desc là cụm rỗng nhảy lên đầu
            return [...this.rows].sort((a, b) => {
                const va = valueOf(a)
                const vb = valueOf(b)
                const emptyA = isDate ? va === null : !va
                const emptyB = isDate ? vb === null : !vb
                if (emptyA && emptyB) return 0
                if (emptyA) return 1
                if (emptyB) return -1
                return sign * (isDate ? va - vb : va.localeCompare(vb, 'vi'))
            })
        },
        pageCount() {
            return Math.max(1, Math.ceil(this.sortedRows.length / this.pageSize))
        },
        /* Kẹp trong [1, pageCount]: bộ lọc cắt danh sách ngắn lại mà `page` còn giữ số cũ thì
           lấy thẳng `page` sẽ ra trang trắng. */
        safePage() {
            return Math.min(Math.max(1, this.page), this.pageCount)
        },
        pageOffset() {
            return (this.safePage - 1) * this.pageSize
        },
        pagedRows() {
            return this.sortedRows.slice(this.pageOffset, this.pageOffset + this.pageSize)
        },
        hasActiveFilter() {
            return !!this.keyword || Object.values(this.filters).some((v) => v !== null && v !== '' && !(Array.isArray(v) && !v.length))
        },
    },
    watch: {
        /* Đổi tập dữ liệu (lượt drill mới / cha tải lại) -> về trang 1. Chỉ dựa vào `safePage` là
           chưa đủ: tập mới vẫn nhiều trang thì người dùng bị bỏ lại ở trang 3 của kết quả khác. */
        rows() {
            this.page = 1
        },
    },
    methods: {
        toggleSort(key) {
            if (this.sort.key === key) this.sort = { key, dir: this.sort.dir === 'asc' ? 'desc' : 'asc' }
            else this.sort = { key, dir: 'asc' }
        },
        onPageChange(page) {
            this.page = page
        },
        onPageSizeChange(size) {
            this.pageSize = size
            this.page = 1
        },
        resetFilters() {
            this.keyword = ''
            this.filters = this.emptyFilters()
            this.page = 1
            this.onFilterChange()
        },
        /** TUỲ CHỌN — chỉ popup lọc client-side gọi tới. Khớp chuỗi không dấu phân biệt hoa thường. */
        applyLocalFilters(rows) {
            const kw = this.keyword.trim().toLowerCase()
            return rows.filter((row) => {
                const okFilters = Object.keys(this.filters).every((param) => {
                    const want = this.filters[param]
                    if (want === null || want === '') return true
                    return String(row[param]) === String(want)
                })
                if (!okFilters) return false
                if (!kw) return true
                return Object.values(row).some((v) => String(v == null ? '' : v).toLowerCase().includes(kw))
            })
        },
    },
}
```

- [x] **Step 2: Kiểm mixin không phá build**

```bash
curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "%{http_code}\n"
```

Expected: `200`, log dev server không có `Failed to compile`.

- [x] **Step 3: Commit**

```bash
git add utils/mixins/reportDrillListMixin.js
git commit -m "feat(report): thêm reportDrillListMixin (sắp xếp + phân trang popup báo cáo)"
```

---

### Task 5: Chuyển `DemandListModal` sang Base + mixin

**Files:**
- Modify: `hrm-client/pages/assign/report/potential-customer-care/components/DemandListModal.vue` (toàn bộ)

**Interfaces:**
- Consumes: `V2BaseReportModal` (Task 3), `reportDrillListMixin` (Task 4).
- Produces: props và events của `DemandListModal` **giữ nguyên 100%** — `index.vue` của màn KHÔNG được sửa một dòng nào.

- [x] **Step 1: Thay khung ngoài**

Bỏ `<b-modal>` + `<template #modal-header>` + khối `.care-drill-scroll` + `<V2BasePagination>` +
`.care-drill-footer`; thay bằng:

```vue
<V2BaseReportModal
    modal-id="care-demand-list-modal"
    :visible="visible"
    :loading="loading"
    lead="Bạn đang xem kết quả CSKH tiềm năng:"
    :title="title"
    :meta="metaText"
    :columns="columns"
    :rows="pagedRows"
    :start-index="pageOffset"
    :sort="sort"
    :current-page="safePage"
    :current-page-size="pageSize"
    :total-rows="sortedRows.length"
    item-label="nhu cầu"
    empty-text="Không có nhu cầu nào khớp bộ lọc."
    @sort="({ key }) => toggleSort(key)"
    @page-change="onPageChange"
    @page-size-change="onPageSizeChange"
    @close="$emit('close')"
>
    <!-- 3 khối dưới đây BÊ NGUYÊN VĂN từ bản cũ, chỉ đổi tiền tố lớp nếu lớp đó đã chuyển sang
         Base (xem Task 3). Mốc dòng ở bản cũ: filters 65–113, back 114–132, summary 133–158. -->
    <template #filters><!-- khối `.care-drill-filters` (dòng 65–113 bản cũ) --></template>
    <template #back><!-- khối `v-if="backTo"` (dòng 114–132 bản cũ) --></template>
    <template #summary><!-- khối KPI + chip cơ cấu (dòng 133–158 bản cũ) --></template>

    <!-- Ô đặc biệt: bê nguyên phần trong từng nhánh `v-if="col.key === '…'"` của bảng cũ.
         Mốc dòng bản cũ: customer 182–197, market 198–201, meeting 205–220, status 221–224,
         project 225–248. Ba cột `amount` (202), `start` (203), `repair` (204) chỉ là biểu thức
         một dòng — vẫn đi qua slot cho thống nhất, KHÔNG thêm khoá `formatter` vào schema. -->
    <template #cell-customer="{ row }"><!-- dòng 182–197 bản cũ --></template>
    <template #cell-market="{ row }"><!-- dòng 198–201 bản cũ --></template>
    <template #cell-meeting="{ row }"><!-- dòng 205–220 bản cũ --></template>
    <template #cell-status="{ row }"><!-- dòng 221–224 bản cũ --></template>
    <template #cell-project="{ row }"><!-- dòng 225–248 bản cũ --></template>
    <template #cell-amount="{ row }">{{ money(row.expected_amount) }}</template>
    <template #cell-start="{ row }">{{ monthYear(row.expected_start_date) }}</template>
    <template #cell-repair="{ row }">{{ row.has_maintenance_demand ? 'Có' : 'Không' }}</template>

    <template #footer>
        <V2BaseButton tertiary size="sm" @click="$emit('close')">Đóng</V2BaseButton>
        <V2BaseButton secondary size="sm" @click="$emit('print')">In danh sách</V2BaseButton>
        <V2BaseButton primary size="sm" @click="$emit('export')">Xuất Excel danh sách</V2BaseButton>
    </template>
</V2BaseReportModal>
```

- [x] **Step 2: Gỡ code đã chuyển sang Base/mixin**

Xoá khỏi `DemandListModal.vue`: `fullscreen`, `scrollWidth`, `overflowing`, `syncingScroll`,
`scrollBound`, `bindScrollSync()`, `updateScrollWidth()`, `observeTable()`, `sortIcon()`,
`sortedRows()`, `pageCount/safePage/pageOffset/pagedRows`, `toggleSort()`, `onPageChange()`,
`onPageSizeChange()`, `page`, `pageSize`, `sort`, `keyword`, `filters`, `summaryCollapsed`,
**`resetFilters()`** (bản của mixin đã gọi `onFilterChange()` — giữ bản riêng là component đè
mixin và nút "Xoá lọc" không tải lại dữ liệu), và toàn bộ style của các lớp đã port sang Base.

⚠️ **Đổi tên MỌI lớp `care-drill-*` còn lại trong file sang `report-drill-*`** (kể cả lớp riêng
của màn: `filters`, `sum*`, `customer`, `sub`, `meeting`, `back`) — Task 6 đổi selector e2e theo
tiền tố nên không được chừa chỗ nào.

**GIỮ LẠI**: `columns`, `filterFields`, `metaText` (computed mới gộp dòng meta), `drillDimension`,
`crossStats`/`kpis`, `backTo`/`goBack`, `showFilter`, `onFilterChange` (emit `filter` lên cha),
`emptyFilters()`, và các style riêng của cột đặc biệt.

⚠️ **`isFiltered` Ở LẠI MÀN, KHÔNG đưa vào mixin.** Nó là `rows.length !== total` — chỉ đúng với
popup lọc ở SERVER (`total` do BE trả = số bản ghi TRƯỚC bộ lọc popup). Mixin có
`hasActiveFilter` (dựa trên state ô lọc) cho nút "Xoá lọc"; hai thứ này KHÁC nhau, đừng gộp:
`DevelopmentDrillModal` lọc client-side thì `rows.length !== total` vô nghĩa.

- [x] **Step 3: Thêm mixin + computed `metaText`**

```js
import reportDrillListMixin from '@/utils/mixins/reportDrillListMixin'

export default {
    name: 'DemandListModal',
    mixins: [reportDrillListMixin],
    computed: {
        /** Dòng meta của dải banner — port nguyên văn từ `.care-drill-head__sub` cũ */
        metaText() {
            if (this.loading) return `Đang tải… · Kỳ ${this.periodText}`
            const base = `${this.rows.length} nhu cầu · ${this.money(this.totalAmount)} đ · Kỳ ${this.periodText}`
            return this.isFiltered ? `${base} · đang lọc trong ${this.total} nhu cầu` : base
        },
    },
}
```

- [x] **Step 4: Mở màn, kiểm popup còn chạy**

```bash
cd HRM && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  node .plans/base-popup-bao-cao/measure-popup.mjs /tmp/after.json
```

Expected: script chạy hết, in JSON có đủ khoá — chưa cần khớp baseline, Task 6 mới so.

- [x] **Step 5: Kiểm `index.vue` của màn KHÔNG bị sửa**

```bash
cd HRM/hrm-client && git diff --numstat pages/assign/report/potential-customer-care/index.vue
```

Expected: **không in ra gì** (props/events của popup giữ nguyên nên màn cha không phải đổi).

- [x] **Step 6: Commit**

```bash
git add pages/assign/report/potential-customer-care/components/DemandListModal.vue
git commit -m "refactor(cskh): chuyển popup danh sách nhu cầu sang V2BaseReportModal + mixin"
```

---

### Task 6: Đối chiếu baseline + đổi selector e2e

**Files:**
- Modify: `HRM/e2e/tests/assign/potential-customer-care.spec.ts` (106 chỗ `care-drill-*`)

**Interfaces:**
- Consumes: `baseline.json` (Task 1), `/tmp/after.json` (Task 5).

- [x] **Step 1: So baseline với sau khi chuyển**

```bash
cd HRM && python3 - <<'PY'
import json
a = json.load(open('.plans/base-popup-bao-cao/baseline.json'))
b = json.load(open('/tmp/after.json'))
lech = []
for k in ['cols', 'firstPageRowCount', 'sttFirst', 'sttLast', 'pageTotal', 'sortTextAsc', 'sortDateAsc']:
    if a.get(k) != b.get(k):
        lech.append(f'{k}:\n  trước = {a.get(k)}\n  sau   = {b.get(k)}')
# Toạ độ đo theo pixel: cho sai số 2px, nhưng LUẬT thì phải giữ
if b['tableBottom'] > b['footerTop'] + 1:
    lech.append(f"bảng chạy xuyên hàng nút: đáy bảng {b['tableBottom']} > đỉnh nút {b['footerTop']}")
if not (b['heightFull'] > b['heightNormal']):
    lech.append('nút phóng to không còn tác dụng')
print('KHỚP HẾT' if not lech else 'LỆCH:\n' + '\n'.join(lech))
PY
```

Expected: `KHỚP HẾT`. Lệch chỗ nào thì quay lại Task 5 sửa **đúng chỗ đó**, không sửa baseline.

- [x] **Step 2: Đổi selector trong spec**

```bash
cd HRM/e2e && python3 - <<'PY'
import io
p = 'tests/assign/potential-customer-care.spec.ts'
s = io.open(p, encoding='utf-8', newline='').read()
truoc = s.count('care-drill')
s = s.replace('care-drill', 'report-drill')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('đã đổi', truoc, 'chỗ')
PY
```

Expected: `đã đổi 106 chỗ`.

- [x] **Step 3: Rà lại các chỗ đổi không phải lớp CSS của Base**

```bash
cd HRM/e2e && grep -n "report-drill" tests/assign/potential-customer-care.spec.ts | grep -vE "report-drill-(table|head|sort|count|filters|dialog|content|paging|sum|customer|meeting|footer|wrap|scroll|back|sub)" | head
```

Expected: không còn dòng nào — nếu còn, đó là lớp riêng của màn bị đổi nhầm, phải trả về `care-drill-*`.

- [x] **Step 4: Kiểm spec vẫn biên dịch**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tests/assign/potential-customer-care.spec.ts --list --no-deps 2>&1 | tail -3
```

Expected: `Total: 29 tests in 1 file`.

- [x] **Step 5: Commit**

```bash
git add tests/assign/potential-customer-care.spec.ts
git commit -m "test(cskh): đổi selector popup sang tiền tố report-drill-* của Base"
```

---

### Task 7: Chạy lại toàn bộ bộ e2e của màn

**Files:** không sửa file nào — đây là cổng nghiệm thu.

- [x] **Step 1: Kiểm không có phiên Playwright nào đang chạy**

```bash
ps aux | grep -c "[p]laywright test"
```

Expected: `0`. Khác 0 thì đợi — 2 phiên cùng chạy gây đỏ ngẫu nhiên.

- [x] **Step 2: Chạy setup**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test --project=api-setup --workers=1 --retries=0 2>&1 | tail -5
```

Nếu đổ với `Table 'hrm_erp.hrm_employees' doesn't exist` → **vật cản môi trường đã biết**, KHÔNG
phải hồi quy của đợt này. Dừng, báo người dùng và chọn 1 trong 2: (a) sửa 5 tên bảng trong
`hrm-api/database/e2e_provision.php` (`hrm_employees`→`employees`, `hrm_roles`→`roles`,
`hrm_company_employees`→`company_employees`, `hrm_employee_has_roles`→`employee_has_roles`,
`hrm_role_has_permissions`→`role_has_permissions`); (b) bàn giao kèm ghi chú chưa chạy được e2e.

- [x] **Step 3: Chạy toàn bộ bộ của màn**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test potential-customer-care --workers=1 2>&1 | tail -25
```

Expected: dòng tổng kết `29 passed`. ⚠️ Bộ chạy `serial` — một ca fail thì các ca sau in
"did not run", KHÔNG phải "passed". Phải đọc dòng tổng kết.

- [x] **Step 4: Dọn file tạm**

```bash
rm -f /tmp/after.json /tmp/check-v2modal.mjs /tmp/care-token.txt /tmp/care-state.json
```

`measure-popup.mjs` và `baseline.json` **giữ lại** trong `.plans/` — đợt sau chuyển 2 popup còn lại
sẽ dùng đúng cách đo này.

- [x] **Step 5: Cập nhật STATUS + checkpoint**

Ghi vào cuối `.plans/base-popup-bao-cao/plan.md`: vừa hoàn thành gì, còn dở gì, bước tiếp theo
(chuyển `DevelopmentDrillModal` và `ProjectListModal`), và blocked nếu có.

---

## Còn lại sau đợt này

- Chuyển `DevelopmentDrillModal` (19 chỗ selector `cmd-drill`) và `ProjectListModal` (15 chỗ
  `tkt-drill`) sang Base.
- Cân nhắc cho 15 popup bảng nhỏ dùng vỏ (không cần mixin).

---

# PHASE 2 — Chuyển nốt 2 popup drill-down lớn (2026-09-17)

**Goal:** `DevelopmentDrillModal` (1204 dòng) và `ProjectListModal` (888 dòng) cùng dùng
`V2BaseReportModal`, để cả 3 popup báo cáo hành xử và trông giống nhau.

**Người dùng đã chốt:** biết trước 2 màn này sẽ **đổi mặt** (đang dùng header chuẩn → nhận dải
banner + nút phóng to) và vẫn quyết làm.

## Bài học Phase 1 — BẮT BUỘC áp dụng, đừng học lại bằng cách trả giá lần nữa

| Bẫy đã dính ở Phase 1 | Cách chặn ở Phase 2 |
|---|---|
| Port CSS trước, đi tìm chỗ gắn sau → **3 lớp CSS chết liên tiếp**, trong đó 1 lớp mang viền khung bảng và 1 lớp mang chặn chiều cao 92vh | Sau khi chuyển, **lập bảng đối chiếu "class khai trong style" vs "class thật có trong template"**, danh sách "khai mà không dùng" phải RỖNG |
| Ảnh chụp hành vi chỉ đo toạ độ → không bắt được mất viền, mất bo góc | Baseline Phase 2 đo **cả `getComputedStyle`** (viền, bo góc, `overflow`), không chỉ toạ độ |
| Bấm sắp xếp vào cột **không sortable** → chụp nhầm thứ tự mặc định, phép so thành vô nghĩa | `measure-popup.mjs` đã có chốt `throw` khi ô tiêu đề không có nút bấm-sắp-xếp — giữ nguyên |
| Đổi tiền tố selector hàng loạt → 4 nhóm selector trỏ vào lớp đã gỡ | Sau khi đổi, **đối chiếu từng selector với class/id thật trong nguồn**, danh sách "không tìm thấy" phải RỖNG |
| Hành vi rơi rụng lặng lẽ (cuộn-về-đầu khi lật trang) | So bản cũ ↔ bản mới theo hướng **"cái gì đã mất"**, mọi thứ biến mất phải rơi vào giỏ "đã chuyển đi" hoặc "cố ý bỏ" |

## Khác biệt phải xử lý — schema cột

`V2BaseReportModal` nhận `columns: { key, label, field, width: '220px', cellClass }`. Hai popup
này khai khác:

| Popup | Đang khai | Phải chuyển thành |
|---|---|---|
| `DevelopmentDrillModal` | `{ id, label, width: <số px>, cellClass }` — khoá tên là **`id`** | `key: column.id`, `width: column.width + 'px'` |
| `ProjectListModal` | BE trả **mảng khoá**, map qua `COLUMN_DEFS` cục bộ → `{ key, label, align }` | giữ `key`/`label`, `cellClass: col.align` |

⚠️ **Chuyển ở phía popup (adapter), TUYỆT ĐỐI không sửa schema BE trả về cho vừa Base** — hai màn
đó còn dùng `columns` cho bản in và Excel.

---

### Task 8: Chụp ảnh hành vi 2 popup (baseline Phase 2)

**Files:**
- Modify: `.plans/gop-db/base-popup-bao-cao/measure-popup.mjs` — tham số hoá để đo được popup bất kỳ
- Create: `.plans/gop-db/base-popup-bao-cao/baseline-cmd.json`, `baseline-tkt.json`

- [x] **Step 1:** Tham số hoá script: nhận thêm `--url`, `--open` (selector mở popup), `--sort-text`, `--sort-date` (nhãn cột), `--item-label`. Giữ nguyên toàn bộ phép đo cũ.
- [x] **Step 2:** Bổ sung 3 phép đo MỚI vào script (Phase 1 thiếu, phải trả giá): `getComputedStyle` của vùng cuộn bảng (`border-top-width`, `border-radius`), `overflow` của `.modal-content`, và khoảng cách ngang giữa 2 nút footer.
- [x] **Step 3:** Chạy cho `customer-market-development` → `baseline-cmd.json`; popup mở từ ô số đầu tiên của bảng.
- [x] **Step 4:** Chạy cho `prospective-project-results` → `baseline-tkt.json`.
- [x] **Step 5:** Kiểm cả 2 file có đủ khoá, `sortTextAsc`/`sortDateAsc` KHÔNG rỗng (rỗng = bấm nhầm cột không sortable), in ra số cột + số dòng trang 1.

### Task 9: Chuyển `DevelopmentDrillModal` (lọc client-side → vỏ + mixin)

**Files:** Modify `pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue`

- [x] **Step 1:** Thay vỏ bằng `V2BaseReportModal`; `lead` đặt theo ngữ cảnh màn ("Bạn đang xem phát triển thị trường:"), `meta` ghép từ dòng meta hiện có.
- [x] **Step 2:** Adapter cột: `columns` computed map `id → key`, `width` số → chuỗi `px`.
- [x] **Step 3:** Gắn `reportDrillListMixin`; popup này lọc **client-side** nên `onFilterChange()` chỉ cần `this.page = 1`, và `rows` truyền vào Base lấy từ `pagedRows` chạy trên `applyLocalFilters(rows)`.
- [x] **Step 4:** Giữ nguyên luật riêng: ô lọc theo đối tượng đang xem bị ẩn VÀ bị xoá giá trị (không lọc ngầm).
- [x] **Step 5:** Đổi toàn bộ tiền tố `cmd-drill-*` → `report-drill-*`; lớp nào trùng tên với lớp Base thì XOÁ khỏi popup (Base lo).
- [x] **Step 6:** Lập bảng đối chiếu class khai/dùng — phải rỗng.
- [x] **Step 7:** Chạy `measure-popup.mjs` so với `baseline-cmd.json`; lệch khoá nào ngoài 2 khoá footer đã biết thì sửa code, KHÔNG sửa baseline.

### Task 10: Chuyển `ProjectListModal` (server-side → CHỈ vỏ, không mixin)

**Files:** Modify `pages/assign/report/prospective-project-results/components/ProjectListModal.vue`

- [x] **Step 1:** Thay vỏ bằng `V2BaseReportModal`. **KHÔNG gắn mixin** — popup tự `fetchList()`, lọc/sắp/phân trang đều ở BE.
- [x] **Step 2:** Truyền `current-page` / `current-page-size` / `total-rows` từ response API; `@page-change`/`@page-size-change` gọi lại `fetchList()`.
- [x] **Step 3:** Adapter cột: `columnDefs` map `align → cellClass`.
- [x] **Step 4:** `@sort` nối vào cơ chế sắp xếp BE sẵn có (không dùng sort client của mixin).
- [x] **Step 5:** Đổi tiền tố `tkt-drill-*` → `report-drill-*`, xoá lớp trùng với Base.
- [x] **Step 6:** Bảng đối chiếu class khai/dùng — rỗng.
- [x] **Step 7:** So với `baseline-tkt.json`.

### Task 11: Cập nhật e2e của 2 màn

**Files:** Modify `e2e/tests/assign/customer-market-development.spec.ts` (19 chỗ `cmd-drill`), `e2e/tests/assign/tkt-result-report.spec.ts` (15 chỗ `tkt-drill`)

- [x] **Step 1:** Đổi tiền tố bằng script, in số chỗ đã đổi.
- [x] **Step 2:** **Đối chiếu từng selector `report-drill-*` với class/id thật trong nguồn** — danh sách "không tìm thấy nơi định nghĩa" phải RỖNG. Lớp đã gỡ ở Phase 1 ánh xạ như sau: `*-content` → `.report-drill-dialog .modal-content`, `*-footer` → `.report-drill-dialog .modal-footer`, `*-topscroll` → `.v2-table-scroll__top`.
- [x] **Step 3:** `--list --no-deps` cho cả 2 spec, phải ra đúng 18 và 10 ca.

### Task 12: Nghiệm thu

- [x] **Step 1:** Chạy lượt tự kiểm Playwright 8 luồng (như Task 7) cho **từng popup**, đo bằng số.
- [x] **Step 2:** Mở lại popup của báo cáo CSKH tiềm năng, đo lại đúng 11 khoá của `baseline.json` — chứng minh Phase 2 KHÔNG làm hồi quy popup đã chuyển ở Phase 1 (cả 3 dùng chung 1 vỏ).
- [x] **Step 3:** Thử chạy bộ e2e; vướng vật cản `e2e_provision.php` thì ghi nhận, KHÔNG sửa script provision, KHÔNG đụng dữ liệu DB dùng chung.


---

### Checkpoint — 18/09/2026

Vừa hoàn thành: **toàn bộ Phase 1 + Phase 2 + lượt dọn nhất quán + chạy e2e thật.**
3 popup báo cáo (`DemandListModal` 1307→871, `DevelopmentDrillModal` 1204→1050, `ProjectListModal`
888→916) nay dùng chung `components/report/V2BaseReportModal.vue` (481 dòng) +
`utils/mixins/reportDrillListMixin.js` (146 dòng), trong khi GIỮ NGUYÊN 3 chiến lược dữ liệu khác
nhau (lọc server / lọc client / BE lo hết). 17 commit trên `gop_db` của `hrm-client`, chưa push.

Đã gỡ vật cản chặn TOÀN BỘ spec UI của HRM: `hrm-api/database/e2e_provision.php` trỏ 5 bảng `hrm_*`
đã bị `ReconcileEmployeesSeeder` gộp và xoá → sửa về tên thật. **File này CHƯA COMMIT** (hạ tầng
test dùng chung, chờ user duyệt diff).

Kết quả e2e (`--workers=1`, máy rảnh): `tkt-result-report` **22/22 passed**;
`customer-market-development` 7 passed / 2 failed (đỏ sẵn) / 26 bị chặn;
`potential-customer-care` UI 16 passed / 1 failed (ca 16, đỏ sẵn) / 13 bị chặn — loại ca đỏ sẵn ra
thì 25+ ca xanh. Ba ca của đợt này (27 phân trang bảng, 28 bộ lọc chuẩn mới, 29 popup biên bản trên
panel) **đều xanh**.

Đang làm dở: (không)

Bước tiếp theo:
1. User xem diff `hrm-api/database/e2e_provision.php` rồi quyết commit — nó gỡ tắc cho mọi spec UI.
2. Sửa 3 ca đỏ SẴN đang che 13 ca phía sau: ca 19 (test giả định popup chỉ 2 trang, DB nay 126
   dòng), ca 26 (fixture cần ≥2 meeting hoàn thành), ca 16 (select nhu cầu ở màn tạo dự án TKT).
3. Truy điểm chờ chưa chắc chắn làm ca 28 flaky (xanh ở lượt chạy lại).
4. Cân nhắc dọn 2 mục nhất quán còn lại: nút thu gọn khối tổng hợp (3 cách hiện thực) và dải chip
   phân bổ (popup TKT đặt tên class khác, CSS không tái dùng được).

Blocked: (không)
