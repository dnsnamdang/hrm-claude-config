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

- [ ] **Step 1: Thêm prop `noEnforceFocus` và đổ xuống `b-modal`**

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

- [ ] **Step 2: Sửa template header**

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

- [ ] **Step 3: Kiểm popup CŨ không đổi**

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

- [ ] **Step 4: Kiểm diff đúng bằng phần đã thêm**

```bash
cd HRM/hrm-client && git diff --numstat components/modal/V2BaseModal.vue
```

Expected: chỉ vài dòng thêm (mở/đóng slot + comment), phần markup cũ không bị viết lại.

- [ ] **Step 5: Commit**

```bash
git add components/modal/V2BaseModal.vue
git commit -m "feat(V2BaseModal): thêm slot header + prop noEnforceFocus cho popup báo cáo"
```

---

