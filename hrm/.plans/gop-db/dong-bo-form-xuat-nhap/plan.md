# Đồng bộ form luồng xuất nhập — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

- Người phụ trách: @namdangit
- Nhánh: `gop_db` (cả `hrm-client` lẫn `hrm-api`)

**Goal:** Màn Tạo / Sửa / Chi tiết của 8 luồng xuất nhập thể hiện thông tin cùng một dạng với chi tiết Phiếu xuất giữ PXG-02188.

**Architecture:** Đóng gói CSS khối `.form-card` của màn PXG thành component dùng chung `components/V2BaseFormCard.vue` (tiêu đề in hoa nền xám nhạt, slot `#meta` cho dòng người lập, không icon). Từng màn thay khung khối cũ (`c-section` / `kv-grid` / `card-header section-header` / `V2BaseFormSection` / `.form-card` chép tay) bằng `V2BaseFormCard` + lưới `form-row` 3 cột nhãn-trên-ô-dưới; ruột các bảng giữ nguyên. Thí điểm PXBHM trước, user duyệt ảnh rồi làm liền 7 luồng còn lại.

**Tech Stack:** Nuxt 2.14 / Vue 2 / Bootstrap-Vue 2.15, component `V2Base*`, Playwright MCP. BE Laravel 8 / PHP 7.4 (chỉ thêm `status_color` ở 4 Resource chi tiết).

**Spec:** `docs/superpowers/specs/gop-db/2026-10-10-dong-bo-form-xuat-nhap-design.md` (tóm tắt + 13 quyết định đã chốt: `.plans/gop-db/dong-bo-form-xuat-nhap/design.md`)

## Global Constraints

- Màn mẫu: `pages/finance/warehouse-prepick-requests/components/WarehousePrepickRequestForm.vue` (chi tiết PXG-02188). Thông số khối: viền `1px #e5e7eb`, bo `8px`, head nền `#f9fafb` padding `8px 14px` chữ `12px` / `700` / `#374151` / IN HOA / `letter-spacing: 0.02em`, body padding `14px`.
- Tên class giữ `form-card` / `form-card-head` / `form-card-meta` / `form-card-body` (spec §3.1) — cùng giá trị CSS với 10 màn cũ nên không xung đột.
- Ô thông tin: `col-md-4 mb-2` + `V2BaseLabel` + `V2BaseInput :value disabled size="sm"`; trường dài (Khách hàng, Địa chỉ, Nơi giao hàng) `col-12` hoặc `col-md-8`; Ghi chú `col-12` + `V2BaseTextarea :rows="2"` (`disabled` ở chi tiết).
- Thứ tự ô: Mã phiếu → Trạng thái → Loại phiếu → phiếu/hợp đồng liên kết → người yêu cầu + phòng → trường riêng theo loại → nhóm khách hàng → Ghi chú.
- Trạng thái: `V2BaseBadge :color="data.status_color"` trong ô lưới (`div.pt-1`), màu do BE trả, đúng 9 mã chuẩn CLAUDE.md.
- Mã liên kết: `<div class="v2-linked-field"><nuxt-link ... target="_blank" rel="noopener" class="v2-cell-link field-line">`.
- Người lập + giờ lập: `CreatorInfoLine` trong slot `#meta` của khối ĐẦU, dùng tên THUẦN (`created_by_name` khi resource có cả hai; `creator_name` ở resource nào đó là fullname thuần). Bỏ ô "Người lập" / "Ngày lập" / "Người tạo" / "Ngày tạo" khỏi lưới.
- Bỏ mọi icon `ri-*` trước tiêu đề khối / sub-panel / chip. Icon trên NÚT giữ nguyên.
- Trường không áp dụng cho bản ghi → ẩn (`v-if`); áp dụng mà rỗng → ô xám rỗng, KHÔNG in "—".
- KHÔNG `.text-muted` (đỏ trong project) — dùng `#6b7280`.
- Màn Tạo/Sửa: ô nhập giữ editable, giữ validate, giữ `unsavedChangesMixin` và mọi binding — CHỈ thay vỏ khối.
- KHÔNG đụng: mọi `index.vue` danh sách, `print.vue`, modal, 10 màn `.form-card` cũ ngoài 8 luồng, `SystemInfoSection`, `V2Footer`, footer tự dựng `.export-actionbar`, `pageTitle()`.
- Trước mỗi task chạy `git -C hrm-client status --short <thư mục luồng>` — file đang có thay đổi chưa commit của người khác thì DỪNG hỏi user.
- KHÔNG commit / push. Bước cuối mỗi task là đánh `[x]` vào plan.
- Playwright MCP mở `http://127.0.0.1:3000`, vào chi tiết bằng điều hướng SPA từ danh sách; không khởi động lại Nuxt dev server; không `pkill -f mcp-chrome`.
- Bản ghi thử tạo ra phải xoá sau khi kiểm (DB local `erp_hrm_check`), báo user đã xoá gì.

## Review Focus

1. **Bản ghi thiếu dữ liệu tuỳ chọn** (không khách hàng, không địa chỉ liên hệ, không ghi chú, loại phiếu không có hợp đồng) → ô ẩn hoặc xám rỗng đúng quy tắc, không còn chữ "—". Kiểm ở Task 1 Step 7 và bước "Kiểm" của Task 2-8.
2. **Màn rộng 768px** → lưới xuống 2/1 cột, không cuộn ngang trang, dòng người lập ở head không đè tiêu đề. Kiểm ở Task 1 Step 8 + Task 9.
3. **Form Tạo/Sửa vẫn lưu được và cảnh báo chưa lưu vẫn chạy** sau khi đổi vỏ (đặc biệt chỗ đổi `<input type=checkbox>` → `V2BaseCheckbox`). Kiểm ở Task 1 Step 10 và bước "Hồi quy lưu" của Task 2-8.
4. **CSS `V2BaseFormCard` không làm lệch 10 màn `.form-card` cũ** (trùng tên class) — đo head PXG-02188 trước và sau khi component được nạp. Kiểm ở Task 0 Step 3.
5. **Ruột bảng / tab con** (tab Hạch toán, bảng hàng hoá, `pay-box`, `acc-block`) hiển thị y như cũ — không xoá nhầm CSS còn dùng. Kiểm ở bước "Kiểm" mỗi task (bấm qua từng tab).

---

## Khuôn dùng chung cho Task 1-8

Các task dưới gọi tên khuôn (K1…K6). Mã ở đây là nguyên văn để chép, chỉ thay biến dữ liệu theo bảng ô của từng task.

**K1 — Khối Thông tin chung (chi tiết):**

```vue
<V2BaseFormCard title="Thông tin chung">
    <template #meta>
        <CreatorInfoLine :name="data.created_by_name || ''" :created-at="data.created_at || ''" />
    </template>
    <div class="form-row">
        <!-- các ô K2/K3/K4/K5 theo bảng ô của task -->
    </div>
</V2BaseFormCard>
```

Màn Tạo: `<CreatorInfoLine :is-create="true" />`. Màn Sửa: `:name` + `:created-at` như chi tiết.

**K2 — Ô chỉ đọc:**

```vue
<div class="col-md-4 mb-2">
    <V2BaseLabel>Mã phiếu</V2BaseLabel>
    <V2BaseInput :value="data.code" disabled size="sm" />
</div>
```

Trường dài: đổi `col-md-4` → `col-md-8` hoặc `col-12`. Trường chỉ áp dụng cho 1 số loại: thêm `v-if` lên `div.col-*` (lấy đúng điều kiện `v-if` đang có ở markup cũ).

**K3 — Ô trạng thái:**

```vue
<div class="col-md-4 mb-2">
    <V2BaseLabel>Trạng thái</V2BaseLabel>
    <div class="pt-1">
        <V2BaseBadge :color="data.status_color">{{ data.status_name }}</V2BaseBadge>
    </div>
</div>
```

**K4 — Ô mã liên kết:**

```vue
<div class="col-md-4 mb-2">
    <V2BaseLabel>Mã YCXH</V2BaseLabel>
    <div class="v2-linked-field">
        <nuxt-link
            v-if="data.product_export_request_id"
            :to="`/finance/product-export-requests/${data.product_export_request_id}`"
            target="_blank"
            rel="noopener"
            class="v2-cell-link field-line"
            >{{ data.product_export_request_code }}</nuxt-link
        >
        <span v-else class="field-line"></span>
    </div>
</div>
```

Link đang dùng `<a :href>` (ERP) thì giữ `<a>` với cùng class + `target`/`rel`. Danh sách nhiều mã (chips phiếu nguồn): giữ `v-for` cũ, mỗi phần tử là `nuxt-link class="v2-cell-link"` cách nhau dấu `, `, bỏ icon chip; rỗng → `<span class="field-line"></span>`.

**K5 — Ghi chú:**

```vue
<div class="col-12 mb-2">
    <V2BaseLabel>Ghi chú</V2BaseLabel>
    <V2BaseTextarea :value="data.note" :rows="2" disabled />
</div>
```

Màn Tạo/Sửa: giữ nguyên `v-model` + `maxlength` + validate của ô cũ, chỉ đặt vào `col-12`.

**K6 — Khối bảng:**

```vue
<V2BaseFormCard title="Danh sách hàng hoá" no-body-padding>
    <!-- ruột cũ giữ nguyên: b-tabs / V2BaseTableScroll / bảng / nút trong bảng -->
</V2BaseFormCard>
```

Tiêu đề có dữ liệu động (mã HĐ, `type_name`) → `<template #title>…</template>`. Head cũ có nút / ghi chú (`hdr-note`, "Chọn phiếu nguồn", "Thêm hàng hoá") → đưa vào `<template #meta>`, giữ nguyên `v-if`. Ruột là `b-tabs` dính mép → bọc `<div class="p-2">`.

**Import cho mọi file sửa** (thêm cái còn thiếu, đường dẫn `@/components/<Tên>.vue`, khai trong `components`): `V2BaseFormCard`, `V2BaseLabel`, `V2BaseInput`, `V2BaseBadge`, `V2BaseTextarea`, `CreatorInfoLine`.

**CSS thừa phải xoá sau khi đổi** (chỉ xoá khi grep thấy không còn dùng trong file): `.c-section`, `.section-header` (+ `--between`, `> i`; `.hdr-note` thì GIỮ vì đã chuyển vào `#meta`), `.sec-goods/.sec-files/.sec-arrange .section-header > i`, `.section-body`, `.kv-grid`, `.kv`, `.kv--wide`, `.kv--block`, `.kv-label`, `.kv-value`, `.subpanel*` và media query chỉ chứa các class này, `.form-card*` / `.head-meta` chép tay, `.status-pill`. GIỮ: `.file-list` / `.file-item`, `.acc-block`, `.er-table`, `.pay-box`, `.export-actionbar`, `.kv-empty`, `.fld-grid` nếu còn ô nhập dùng.

**Đo so khuôn (chạy ở PXG-02188 một lần, rồi ở từng màn):**

```js
(() => { const h = document.querySelector('.form-card-head'); const s = getComputedStyle(h)
  const b = document.querySelector('.form-card-body'); const inp = b.querySelector('.v2-input, input')
  const cells = [...b.querySelectorAll(':scope > .form-row > [class*="col-md-4"]')].slice(0, 3).map(c => Math.round(c.getBoundingClientRect().width))
  return { headH: Math.round(h.getBoundingClientRect().height), fs: s.fontSize, fw: s.fontWeight, color: s.color,
    bg: s.backgroundColor, tt: s.textTransform, bodyPad: getComputedStyle(b).padding,
    inputH: inp && Math.round(inp.getBoundingClientRect().height), cellW: cells,
    headIcons: document.querySelectorAll('.form-card-head i[class^="ri-"]').length,
    dash: [...document.querySelectorAll('.form-card-body .field-line, .form-card-body input')].filter(e => (e.value || e.textContent).trim() === '—').length } })()
```

Expected mỗi màn: `headH fs fw color bg tt bodyPad inputH` giống PXG-02188; `cellW` 3 ô bằng nhau; `headIcons = 0` (trừ icon trong nút ở `#meta`); `dash = 0`.

**Grep sạch (chạy cho từng file đã sửa):**

Run: `grep -nE "ri-[a-z0-9-]+(-line|-fill)?\"></i>|kv-grid|c-section|section-header|card-header|subpanel|status-pill|text-muted|'—'|>—<" <file>`
Expected: chỉ còn icon nằm trong `V2BaseButton` / nút bảng.

---

### Task 0: Component dùng chung `V2BaseFormCard`

**Files:**
- Create: `hrm-client/components/V2BaseFormCard.vue`

**Interfaces:**
- Produces: `<V2BaseFormCard title="..." [no-body-padding]>` · slot `#title` · slot `#meta` · slot default. Class `form-card` / `form-card-head` / `form-card-title` / `form-card-meta` / `form-card-body`. Component tự có `mb-3`.

- [x] **Step 1: Đo PXG-02188 TRƯỚC khi tạo component** — Playwright mở `/finance/warehouse-prepick-requests`, tìm nhanh "PXG-02188", mở chi tiết, chạy đoạn "Đo so khuôn". Lưu kết quả vào `scratchpad/pxg-baseline.json`.

- [x] **Step 2: Tạo file component**

```vue
<template>
    <div class="form-card mb-3">
        <div class="form-card-head">
            <span class="form-card-title"><slot name="title">{{ title }}</slot></span>
            <div v-if="$slots.meta" class="form-card-meta"><slot name="meta" /></div>
        </div>
        <div class="form-card-body" :class="{ 'p-0': noBodyPadding }">
            <slot />
        </div>
    </div>
</template>

<script>
/**
 * Khối nhóm của màn Tạo / Sửa / Chi tiết luồng xuất nhập — khuôn chi tiết Phiếu xuất giữ PXG-02188
 * (`warehouse-prepick-requests/components/WarehousePrepickRequestForm.vue`, `.form-card`).
 * Tiêu đề in hoa nền xám nhạt, KHÔNG icon (không có prop icon — chặn từ gốc). Slot `#meta` cho dòng
 * người lập (`CreatorInfoLine`) hoặc nút. CSS để KHÔNG scoped trong chính component (skill list-page:
 * CSS của phần tử do component dùng chung render phải nằm trong component). Tên class trùng 10 màn
 * `.form-card` cũ có chủ đích — cùng giá trị nên không xung đột.
 */
export default {
    name: 'V2BaseFormCard',
    props: {
        title: { type: String, default: '' },
        noBodyPadding: { type: Boolean, default: false },
    },
}
</script>

<style lang="scss">
.form-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    overflow: hidden;
}
.form-card-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 4px 12px;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 700;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}
.form-card-meta {
    font-weight: 400;
    text-transform: none;
    letter-spacing: 0;
    color: #6b7280;
}
.form-card-body {
    padding: 14px;
}
</style>
```

- [x] **Step 3: Kiểm biên dịch + không làm lệch màn cũ (Review Focus 4)**

Run: `tail -n 20 /private/tmp/claude-501/-Users-nguyentrancu-DEV-code-ERP-HRM/fe816f22-a08c-47e8-b8ad-cc442975a034/scratchpad/nuxt.log`
Expected: không có `ERROR` / `Module build failed`.

Sau Task 1 (khi component đã nạp trong bundle), mở lại PXG-02188 chạy "Đo so khuôn" → so với `pxg-baseline.json`: Expected giống hệt.

- [x] **Step 4: Đánh `[x]`, sang Task 1.**

---

### Task 1: Thí điểm PXBHM — chi tiết + form tạo (DỪNG gửi ảnh cho user duyệt)

**Files:**
- Modify: `hrm-api/Modules/Finance/Transformers/BorrowSellResource/BorrowSellDetailResource.php` (thêm `status_color`)
- Modify: `hrm-client/pages/finance/borrow-sells/_id/index.vue` — khối Thông tin chung L13-55, head khối hàng hoá L58, head khối thanh toán HĐ L186, head khối bút toán L242, script components, CSS scoped
- Modify: `hrm-client/pages/finance/borrow-sells/components/BorrowSellForm.vue` — 2 khối đầu L5-95, script components, CSS scoped

**Interfaces:**
- Consumes: `V2BaseFormCard` (Task 0), khuôn K1-K6.
- Produces: field mới `status_color` trong `GET finance/borrow-sells/{id}`.

- [x] **Step 1: BE — `status_color`**

Trong `BorrowSellDetailResource.php`, dưới `private static $statusNames = [1 => 'Đã duyệt'];`:

```php
    // Màu badge theo 9 mã chuẩn (CLAUDE.md): "Đã duyệt" = nhóm hoàn thành.
    private static $statusColors = [1 => '#16A34A'];
```

Dưới dòng `'status_name' => …`:

```php
            'status_color' => self::$statusColors[$this->status] ?? '#64748B',
```

Kiểm: `php artisan tinker --execute="echo json_encode((new \Modules\Finance\Transformers\BorrowSellResource\BorrowSellDetailResource(\Modules\Finance\Entities\BorrowSell::find(4313)))->toArray(request())['status_color']);"` (sửa namespace entity theo `use` ở đầu controller nếu khác). Expected: `"#16A34A"`.

- [x] **Step 2: Chi tiết — thay khối Thông tin chung (L13-55) theo K1**

Bảng ô (theo thứ tự):

| Ô | Khuôn | Dữ liệu | Cột |
|---|---|---|---|
| Mã phiếu | K2 | `data.code` | 4 |
| Trạng thái | K3 | `data.status_color` / `data.status_name` | 4 |
| Phiếu yêu cầu xuất bán | K4 | `/finance/borrow-sell-requests/${data.borrow_sell_request_id}` · `data.borrow_sell_request_code` | 4 |
| Số hợp đồng | K2 | `data.contract_code` | 4 |
| Loại hợp đồng | K2 | `contractTypeLabel` | 4 |
| Chịu phí vận chuyển | K2 | `bearShippingLabel` | 4 |
| Người yêu cầu | K2 | `data.requester_name` | 4 |
| Phòng yêu cầu | K2 | `data.requester_department` | 4 |
| Điện thoại khách hàng | K2 | `data.customer_mobile` | 4 |
| Khách hàng | K2 | `data.customer_name` | 8 |
| Người liên hệ | K2 | `data.customer_contact_name` | 4 |
| Địa chỉ khách hàng | K2 | `data.customer_address` | 8 |
| Điện thoại liên hệ | K2 | `data.customer_contact_phone` | 4 |
| Địa chỉ liên hệ | K2 `v-if="data.contact_address"` | `data.contact_address` | 12 |
| Nơi giao hàng | K2 `v-if="data.delivery_place"` | `data.delivery_place` | 12 |
| Ghi chú | K5 | `data.note` | 12 |

`CreatorInfoLine` ở `#meta`: `:name="data.creator_name"` (resource này `creator_name` là fullname thuần).
Bỏ ô "Loại phiếu" (`type_name`) — BE dựng nó từ đúng `contractable_type` như "Loại hợp đồng", 2 ô luôn cùng giá trị. Nhãn ô nào màn cũ đang ghi khác (vd "Chịu phí ship") thì giữ nhãn cũ. Tên biến thật lấy từ markup cũ L13-55 (bảng trên ghi theo kiểm kê; lệch tên thì dùng tên trong file).

- [x] **Step 3: Chi tiết — computed** `contractTypeLabel` và `bearShippingLabel` đang trả `'—'` khi rỗng → trả `''`. `formatNum` (dùng trong bảng) giữ nguyên.

- [x] **Step 4: Chi tiết — 3 khối còn lại theo K6, bỏ icon**
  - "Danh sách hàng hoá" (L58, icon `ri-file-copy-2-line`): `no-body-padding`, ruột `b-tabs v2-tabs--inner` + bảng + `pay-box` giữ nguyên.
  - "Thông tin thanh toán hợp đồng" (L186, icon `ri-money-dollar-circle-line`): giữ `v-if="needContractInfo && contractPayment"` trên `V2BaseFormCard`; nếu tiêu đề cũ có kèm mã HĐ thì dùng `#title`.
  - "Bút toán hạch toán" (L242, tab Hạch toán, icon `ri-book-2-line`): `no-body-padding`, giữ `.kv-empty`.

- [x] **Step 5: Chi tiết — import + dọn CSS** theo mục "Import" và "CSS thừa" của Khuôn dùng chung. Chạy "Grep sạch" trên file → Expected như khuôn.

- [x] **Step 6: Chi tiết — đo so PXG-02188 + tab Hạch toán (Review Focus 5)** — mở `/finance/borrow-sells` → bấm phiếu 4313. Chạy "Đo so khuôn" → khớp baseline. Bấm tab "Hạch toán" → bảng bút toán đủ dòng như trước khi sửa. Chụp `scratchpad/borrow-sell-detail.png` (full page).

- [x] **Step 7: Chi tiết — bản ghi thiếu dữ liệu tuỳ chọn (Review Focus 1)**

Run (trong `hrm-api`): `php artisan tinker --execute="echo json_encode(DB::table('borrow_sells')->where(function(\$q){\$q->whereNull('note')->orWhere('note','');})->orderByDesc('id')->limit(3)->pluck('id'));"`
Mở 1 phiếu trong danh sách đó: ô Ghi chú xám rỗng, ô Địa chỉ liên hệ / Nơi giao hàng ẩn khi rỗng, `dash = 0`, không ô nào lệch hàng.

- [x] **Step 8: Chi tiết — 768px (Review Focus 2)** — `browser_resize` 768×900, chạy `document.documentElement.scrollWidth > document.documentElement.clientWidth` → Expected `false`; `CreatorInfoLine` xuống dòng dưới tiêu đề, không đè. Trả lại 1440×900.

- [x] **Step 9: Form tạo — thay 2 khối đầu (L5-95)**

Khối 1 — K1 với `<CreatorInfoLine :is-create="true" />`, tiêu đề "Thông tin chung" (sửa tiêu đề sai "Phiếu yêu cầu xuất bán hàng mượn" ở L7):

```vue
<V2BaseFormCard title="Thông tin chung">
    <template #meta>
        <!-- Người lập PHIẾU XUẤT (người đang đăng nhập) + giờ hiện tại. "Người yêu cầu" bên dưới là chủ phiếu YC. -->
        <CreatorInfoLine :is-create="true" />
    </template>
    <div class="form-row">
        <div class="col-md-4 mb-2">
            <V2BaseLabel>Số phiếu yêu cầu</V2BaseLabel>
            <V2BaseInput :value="header.code" size="sm" disabled />
        </div>
        <div class="col-md-4 mb-2">
            <V2BaseLabel>Số hợp đồng</V2BaseLabel>
            <V2BaseInput :value="header.contract_code" size="sm" disabled />
        </div>
        <div class="col-md-4 mb-2">
            <V2BaseLabel>Loại hợp đồng</V2BaseLabel>
            <V2BaseInput :value="header.type_name" size="sm" disabled />
        </div>
        <div class="col-md-4 mb-2">
            <V2BaseLabel>Người yêu cầu</V2BaseLabel>
            <V2BaseInput :value="header.creator_name" size="sm" disabled />
        </div>
        <div class="col-md-4 mb-2">
            <V2BaseLabel>Phòng yêu cầu</V2BaseLabel>
            <V2BaseInput :value="header.department_name" size="sm" disabled />
        </div>
        <div class="col-md-4 mb-2">
            <V2BaseLabel>Phiếu xuất mượn</V2BaseLabel>
            <div class="v2-linked-field">
                <span class="field-line">{{ header.source_export_requests.map((s) => s.code).join(', ') }}</span>
            </div>
        </div>
        <div class="col-12 mb-2">
            <V2BaseLabel>Khách hàng</V2BaseLabel>
            <V2BaseInput :value="header.customer_name" size="sm" disabled />
        </div>
        <div class="col-12 mb-2">
            <V2BaseLabel>Địa chỉ giao hàng</V2BaseLabel>
            <V2BaseInput :value="header.delivery_address" size="sm" disabled />
        </div>
    </div>

    <!-- Định khoản hạch toán (hiển thị — số tiền & bút toán thật do BE tính khi lưu) -->
    <div v-if="header.accounts.length" class="acc-block">
        <div class="acc-block__title">Định khoản hạch toán</div>
        <div class="acc-block__items">
            <div v-for="(a, ai) in header.accounts" :key="ai" class="acc-item">
                <span class="acc-item__label">{{ a.label }}</span>
                <span class="acc-item__code">{{ a.code }}</span>
            </div>
        </div>
    </div>

    <div class="form-row mt-2">
        <div class="col-md-8 mb-2">
            <V2BaseLabel>Ghi chú</V2BaseLabel>
            <V2BaseTextarea
                v-model="form.note"
                :rows="2"
                :maxlength="255"
                placeholder="Nhập ghi chú cho phiếu bán (nếu có)"
            />
        </div>
        <div class="col-md-4 mb-2 d-flex align-items-end">
            <V2BaseCheckbox v-model="form.bear_the_shipping" label="KD chịu vận chuyển" />
        </div>
    </div>
</V2BaseFormCard>
```

Trước khi thay: đọc lại markup L5-95 hiện tại — tên biến (`header.*`, `form.*`) và tên class con của acc-block ở trên là theo kiểm kê; lệch thì dùng tên thật trong file, chỉ bỏ thẻ `<i class="ri-*">`. Kiểm prop của `V2BaseCheckbox` (đọc `components/V2BaseCheckbox.vue`: tên prop nhãn là `label` hay slot) trước khi dùng.

Khối 2 — K6 "Chi tiết số lượng bán" (không `no-body-padding` vì `V2BaseTableScroll` cần lề), ruột giữ nguyên.

Script: import + khai `V2BaseFormCard`, `V2BaseTextarea`, `V2BaseCheckbox` (nếu chưa có). CSS: xoá `.ship-check`, `.source-chips`, `.source-chip` (không còn dùng); giữ `.acc-block`, `.acc-item`, `.qty-input`, `.bsr-*`.

Kiểm giá trị `bear_the_shipping`: đọc đoạn dựng payload `store` — nếu đang gửi thẳng `this.form.bear_the_shipping` và BE validate `in:0,1` / `integer`, đổi thành `bear_the_shipping: this.form.bear_the_shipping ? 1 : 0`; BE validate `boolean` thì để nguyên.

Chạy "Grep sạch" → chỉ còn `ri-save-3-line` trong nút Lưu.

- [x] **Step 10: Form tạo — kiểm + hồi quy lưu (Review Focus 3)**
  1. `/finance/borrow-sell-requests` → mở 1 phiếu có nút lập phiếu xuất bán → sang `/finance/borrow-sells/create?request_id=…`.
  2. "Đo so khuôn" khớp baseline; head khối 1 = "THÔNG TIN CHUNG" + tên người đăng nhập + giờ hiện tại.
  3. Tick "KD chịu vận chuyển" + gõ ghi chú → bấm "Quay lại" → hiện popup "Thông tin chưa lưu" → chọn "Ở lại", dữ liệu còn nguyên.
  4. Nhập SL bán 1 dòng → Lưu → về danh sách; mở phiếu vừa tạo: "Chịu phí vận chuyển" + Ghi chú đúng.
  5. Xoá phiếu thử: đọc `BorrowSellService::store` để biết các bảng nó ghi (phiếu, chi tiết, bút toán, cập nhật tồn mượn) rồi đảo ngược đúng các bản ghi đó bằng tinker trong 1 transaction; báo user danh sách bản ghi đã xoá/hoàn.
  6. Chụp `scratchpad/borrow-sell-create.png`.

- [x] **Step 11: DỪNG — gửi user 2 ảnh (chi tiết + tạo) + bảng số đo so PXG-02188. Không làm Task 2 cho tới khi user duyệt.**

---

### Task 2: YCXBHM — `borrow-sell-requests` (chi tiết + tạo)

**Files:**
- Modify: `hrm-api/Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestDetailResource.php:12-15,79` (thêm `status_color`)
- Modify: `hrm-client/pages/finance/borrow-sell-requests/_id/index.vue` — khối L10-73, khối L76-186, CSS scoped từ L514
- Modify: `hrm-client/pages/finance/borrow-sell-requests/components/BorrowSellRequestForm.vue` — 4 card L5-207

**Interfaces:**
- Consumes: `V2BaseFormCard`, K1-K6.
- Produces: `status_color` trong `GET finance/borrow-sell-requests/{id}`.

- [x] **Step 1: BE — `status_color`** dưới `$statusNames`:

```php
    // Màu badge theo 9 mã chuẩn (CLAUDE.md).
    private static $statusColors = [
        1 => '#16A34A', 2 => '#D97706', 3 => '#64748B',
        4 => '#DC2626', 10 => '#D97706', 11 => '#D97706',
    ];
```

và dưới `'status_name' => …` (L79): `'status_color' => self::$statusColors[$this->status] ?? '#64748B',`

- [x] **Step 2: Chi tiết — khối Thông tin chung (L10-73) theo K1**, `CreatorInfoLine :name="data.creator_name"` (fullname thuần, resource L111). Sửa luôn lỗi thiếu dấu cách `font-weight-normal":name` ở L15 khi thay.

| Ô | Khuôn | Dữ liệu | Cột |
|---|---|---|---|
| Mã phiếu | K2 | `data.code` | 4 |
| Trạng thái | K3 | `data.status_color` / `data.status_name` (thay `status-pill` + `statusPillClass`) | 4 |
| Loại yêu cầu | K2 | biến đang dùng ở markup cũ | 4 |
| Số hợp đồng | K2 (markup cũ có link → K4) | `data.contract_code` | 4 |
| Phiếu xuất mượn | K4 dạng danh sách (L34-47, bỏ icon chip) | `v-for` cũ | 8 |
| Phòng ban | K2 | `data.department_name` | 4 |
| Ngày duyệt | K2 | `data.approved_time` | 4 |
| Cần lắp đặt | K2 | `Number(data.need_repair) === 1 ? 'Có' : 'Không'` | 4 |
| Mã khách hàng | K2 | biến subpanel cũ | 4 |
| Khách hàng | K2 | biến subpanel cũ | 8 |
| CMT/MST | K2 | biến subpanel cũ | 4 |
| Số điện thoại | K2 | biến subpanel cũ | 4 |
| Địa chỉ | K2 | biến subpanel cũ | 12 |
| Người liên hệ / ĐT liên hệ | K2 ×2, giữ `v-if` customer_type>1 | biến subpanel cũ | 4 + 4 |
| Nơi giao hàng | K2, giữ `v-if` | biến subpanel cũ | 12 |
| Ghi chú | K5 | `data.note` | 12 |
| Lý do từ chối | K5 với nhãn "Lý do từ chối", giữ `v-if="isDenied"` | biến L68-71 | 12 |

Bỏ ô Người lập (L26), Ngày lập (L27). Xoá method `statusPillClass` nếu không còn chỗ dùng.

- [x] **Step 3: Chi tiết — khối "Chi tiết số lượng bán" (L76-186)** theo K6 `no-body-padding`, bỏ icon `ri-file-copy-2-line`.

- [x] **Step 4: Form tạo — 4 card** (`card` + `card-header section-header py-2` + `h6`) → `V2BaseFormCard`:
  - "Hợp đồng" (L5-39) → `title="Thông tin chung"`, `#meta` = `<CreatorInfoLine :is-create="true" />`; lưới 3 ô hiện có (Số hợp đồng picker, Khách hàng, Loại hợp đồng) giữ nguyên — đã đúng `form-row` + `col-md-4`.
  - "Phiếu xuất mượn nguồn" (L42-69) → `title="Phiếu xuất mượn nguồn"`, nút "Chọn phiếu nguồn" (L45-48) vào `#meta`.
  - "Chi tiết số lượng bán" (L76-197) → K6.
  - "Ghi chú" (L200-207) → gộp ô Ghi chú vào cuối lưới "Thông tin chung" theo K5 (giữ `v-model`), xoá card riêng.

- [x] **Step 5: Import + dọn CSS + Grep sạch** cho cả 2 file.

- [x] **Step 6: Kiểm** — chi tiết: mở 1 phiếu trạng thái "Không duyệt" (có Lý do từ chối) và 1 phiếu KH cá nhân (customer_type=1, không có người liên hệ) — chạy "Đo so khuôn", `dash = 0`, badge đúng màu. Tạo: "Đo so khuôn"; chọn HĐ + phiếu nguồn → Quay lại → popup chưa lưu → Ở lại. **Hồi quy lưu**: lưu 1 phiếu YC (lưu nháp nếu có) → mở lại thấy đúng → xoá bằng nút Xoá trên danh sách (không có thì tinker theo bảng `borrow_sell_requests` + chi tiết + nguồn) → báo user. Chụp `scratchpad/ycxbhm-detail.png`, `ycxbhm-create.png`.

- [x] **Step 7: Đánh `[x]`, sang Task 3.**

---

### Task 3: YCXH — `ProductExportRequestForm.vue` (tạo/sửa + chi tiết readonly)

**Files:**
- Modify: `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` — chế độ sửa L7-608, chế độ readonly L674-926, CSS từ L2245

**Interfaces:**
- Consumes: `V2BaseFormCard`, K1-K6. Resource `ProductExportRequestResource` đã có `status_color`, `created_by_name`.

- [x] **Step 1: Chế độ Tạo/Sửa** — đổi `V2BaseFormSection` → `V2BaseFormCard`:
  - "Thông tin chung" (L7-293): `#actions` (`CreatorInfoLine`, L12-16) chuyển thành `#meta`. Ruột `fld-grid` + ô nhập GIỮ NGUYÊN (đã là `V2BaseLabel` + `V2Base*`).
  - `AttachmentSection` (L297-307): mở PXG đối chiếu — `AttachmentSection` tự render khung tiêu đề riêng thì để nguyên như PXG; không có thì bọc `<V2BaseFormCard title="File đính kèm">`.
  - "Chi tiết hàng hoá" (L310-608): K6, `#actions` (nút "Thêm hàng hoá", `v-if isManualType`) → `#meta`.

- [x] **Step 2: Chế độ readonly** (L674-926):
  - "Thông tin chung" (L674-742) + "Thông tin khách hàng & xuất bán" (L745-781, `v-if detailIsContract`) + "Ghi chú" (L784-789) gộp thành 1 khối K1 (`#meta` = `CreatorInfoLine :name="detail.created_by_name"`). Bảng ô:

| Ô | Khuôn | Ghi chú |
|---|---|---|
| Mã phiếu | K2 | |
| Trạng thái | K3 | `detail.status_color` / `detail.status_name` |
| Loại phiếu | K2 | |
| Số hợp đồng | K4 nếu markup cũ có link, không thì K2 | |
| Khách hàng | K2 col-8 | |
| Phòng ban, Người duyệt, Thời gian nhận, Thời gian duyệt, Kho xuất | K2 | giữ `v-if` cũ |
| Xuất thẳng, Cần lắp đặt | K2 `'Có'/'Không'` | thay checkbox hiển thị — ô chi tiết không dùng checkbox |
| Vận chuyển, Số km dự kiến | K2 | ở khối cũ xuất hiện 2 lần (L674 và L745) → chỉ giữ 1 |
| Mã số thuế, Người liên hệ, Số điện thoại | K2, `v-if="detailIsContract"` | |
| Địa chỉ | K2 col-12, `v-if="detailIsContract"` | |
| Ghi chú | K5 | |

  - "File đính kèm" (L792-809, `attach-list` tự dựng): thay bằng `AttachmentSection readonly :files="..."` (cùng mảng file đang `v-for`) theo cách PXG đang dùng.
  - "Danh sách hàng hoá" (L812-926): K6.

- [x] **Step 3: Import + dọn CSS** — `.text-brand` (L2288-2290) xoá nếu không còn chỗ dùng; `kv-grid` / `kv-label` / `kv-value` / `attach-list` xoá. Grep sạch. Bỏ import `V2BaseFormSection` nếu không còn dùng.

- [x] **Step 4: Kiểm** — chi tiết 1 phiếu loại hợp đồng (có khách) + 1 phiếu loại khác (không khách) → "Đo so khuôn", ô khách ẩn ở phiếu thứ 2, bấm tải 1 file đính kèm vẫn mở được. Tạo: chọn loại → nhập vài ô → Quay lại → popup chưa lưu. Sửa: mở 1 phiếu Đang tạo → đổi Ghi chú → Lưu → về danh sách; mở lại đúng ghi chú → trả lại ghi chú cũ. **Hồi quy lưu nháp**: tạo 1 phiếu lưu nháp → xoá bằng nút Xoá. Chụp ảnh tạo + chi tiết.

- [x] **Step 5: Đánh `[x]`, sang Task 4.**

---

### Task 4: ĐNXK — `warehouse-export-requests` (tạo / sửa / chi tiết)

**Files:**
- Modify: `hrm-client/pages/finance/warehouse-export-requests/create.vue` (L10-184, CSS L413+)
- Modify: `hrm-client/pages/finance/warehouse-export-requests/_id/edit.vue` (L10-163, CSS L422+)
- Modify: `hrm-client/pages/finance/warehouse-export-requests/_id/index.vue` (L10-140, CSS L293+)

**Interfaces:**
- Consumes: `V2BaseFormCard`, K1-K6. `WarehouseExportRequestResource` đã có `status_color`, `created_by_name`.

- [x] **Step 1: Chi tiết `_id/index.vue`** — khối L10-76 + subpanel "Khách hàng & giao hàng" (L50-62) gộp thành K1 (`#meta` `:name="detail.created_by_name"`):

| Ô | Khuôn | Ghi chú |
|---|---|---|
| Mã phiếu | K2 | |
| Trạng thái | K3 | `detail.status_color` / `detail.status_name` |
| Loại | K2 | |
| Mã YCXH | K4 | link đang có |
| Số hợp đồng | K4 | link đang có |
| Kho xuất | K2 | |
| KD chịu vận chuyển | K2 | giữ `v-if` |
| Phòng ban, Người duyệt | K2 | |
| Thời gian nhận, Thời gian duyệt | K2 | giữ `v-if` |
| Khách hàng | K2 col-8, `v-if="hasCustomer"` | |
| Số điện thoại | K2, `v-if="hasCustomer"` | |
| Người liên hệ | K2, `v-if="hasCustomer"` | |
| Địa chỉ, Địa chỉ giao | K2 col-12, `v-if="hasCustomer"` | |
| Ghi chú | K5 | |
| Ý kiến duyệt (`approve-note`) | K5 nhãn cũ | giữ `v-if` |

Bỏ ô Người lập (L41, `creator_name` dạng audit), Ngày tạo (L43). Khối hàng hoá L79-123 → K6. File đính kèm L126-140 → `V2BaseFormCard title="File đính kèm"` giữ `v-if files.length`, ruột `file-list` giữ nguyên (xem "Điểm cần chốt" #5).

- [x] **Step 2: Tạo `create.vue`** — khối L10-70 → K1 `is-create`; ô chỉ đọc (Mã YCXH, Số hợp đồng, Ngày yêu cầu, Người yêu cầu + phòng) theo K2; subpanel khách (L28-40, `v-if hasCustomer`) gộp vào lưới theo K2 với `v-if`; ô nhập Kho xuất (`V2BaseSelect`) đặt `col-md-4` giữ binding; checkbox thô "KD chịu vận chuyển" → `V2BaseCheckbox v-model="<biến cũ>"` (+ kiểm payload 0/1 như Task 1 Step 9); Ghi chú K5 giữ `v-model`. File đính kèm L73-95 → `V2BaseFormCard title="File đính kèm"`, ruột giữ nguyên. Hàng hoá L98-165 → K6.

- [x] **Step 3: Sửa `_id/edit.vue`** — làm như Step 2, `#meta` = `CreatorInfoLine :name="info.created_by_name" :created-at="info.created_at"`; ô chỉ đọc: Mã phiếu, Mã YCXH, Số hợp đồng, Loại; subpanel khách L25-37 (luôn hiện) gộp vào lưới không `v-if`. Thứ tự khối giữ như file cũ (hàng hoá trước, file sau).

- [x] **Step 4: Import + dọn CSS + Grep sạch** cả 3 file (giữ `.file-list` / `.file-item`).

- [x] **Step 5: Kiểm** — chi tiết: 1 phiếu có khách + 1 phiếu không khách. Tạo: vào từ chi tiết YCXH bằng nút lập ĐNXK; đổi Kho xuất → Quay lại → popup chưa lưu. Sửa: đổi Ghi chú → Lưu → mở lại đúng → trả lại. **Hồi quy lưu**: tick/bỏ tick "KD chịu vận chuyển" ở màn Sửa → Lưu → chi tiết hiện đúng → trả lại giá trị cũ. Chụp 3 ảnh.

- [x] **Step 6: Đánh `[x]`, sang Task 5.**

---

### Task 5: PXH — `product-exports` (tạo / chi tiết)

**Files:**
- Modify: `hrm-client/pages/finance/product-exports/create.vue` (L8-546, CSS L1348+)
- Modify: `hrm-client/pages/finance/product-exports/_id/index.vue` (L11-303, CSS L497+)

**Interfaces:**
- Consumes: `V2BaseFormCard`, K1-K6. `ProductExportResource` đã có `status_color`, `created_by_name`.

- [x] **Step 1: Chi tiết `_id/index.vue`**
  - Khối L11-211 (tiêu đề động `detail.type_name || 'Phiếu xuất hàng'`, ruột `b-tabs` Thông tin chung / Vận chuyển / Bốc xếp / Hạch toán) → `V2BaseFormCard` với `<template #title>{{ detail.type_name || 'Phiếu xuất hàng' }}</template>`, `#meta` = `CreatorInfoLine :name="detail.created_by_name"`. Bỏ icon `ri-file-text-line`.
  - Trong tab "Thông tin chung": `kv-grid` → `form-row` theo K2-K5: Mã phiếu, Trạng thái (K3), Loại, Phiếu xuất kho (K4 link ERP giữ `<a>`), Mã YCXH (K4), Số hợp đồng (K4), Kho xuất, Phòng ban, Ngày hạch toán; khách (L61-73, `v-if detail.has_customer`) gộp vào lưới; Ghi chú K5. Bỏ Người lập (L55) + Ngày lập (L56).
  - Tab Vận chuyển / Bốc xếp: `kv-grid` → `form-row` K2; nhãn nhóm trần "Chi tiết chuyến" (L94), "Người thực hiện" (L143) thay `subpanel__title` bằng `<div class="form-group-label">` (CSS scoped: `font-size: 12px; font-weight: 600; color: #6b7280; margin: 4px 0 6px;`).
  - Khối "Chi tiết" L214-303 → K6 `no-body-padding`, bỏ `ri-file-copy-2-line`.

- [x] **Step 2: Tạo `create.vue`**
  - Khối loadError (L8-15): bỏ khung `c-section`, giữ nội dung lỗi trong `<V2BaseFormCard title="Lỗi tải dữ liệu">`.
  - "Chọn chứng từ nguồn" (L18-38) → `V2BaseFormCard title="Chọn chứng từ nguồn"`, `hdr-note` vào `#meta`.
  - "Thông tin phiếu xuất hàng" (L42-365) → `V2BaseFormCard title="Thông tin phiếu xuất hàng"`; `#meta` = `CreatorInfoLine :is-create="true"` + nút "Đổi phiếu" (L47-52) cạnh nhau trong `<div class="d-flex align-items-center" style="gap: 12px">`. Trong tab "Thông tin chung": subpanel "Hợp đồng" (L79-101), "Khách hàng & giao hàng" (L104-116) gộp vào lưới K2; subpanel "Thông tin hạch toán" (L130-198) giữ là nhóm có nhãn `form-group-label` "Thông tin hạch toán" (bỏ icon `ri-bank-card-line`), ruột `arr-grid` + `ProductExportAccountBlock` + `V2BaseFile` giữ nguyên. Các `<label>` thô trong `arr-grid` → `V2BaseLabel` (cùng chữ).
  - "Chi tiết" (L369-510) → K6, `hdr-note` (L373) vào `#meta`.

- [x] **Step 3: Import + dọn CSS + Grep sạch** (xoá `.sec-arrange .section-header > i` L1641-1644 — đã không dùng).

- [x] **Step 4: Kiểm** — chi tiết: 1 phiếu có khách + 1 phiếu không khách, bấm đủ 4 tab. Tạo: chọn chứng từ nguồn → form hiện → đổi 1 ô → Quay lại → popup chưa lưu; bấm "Đổi phiếu" vẫn chạy. **Hồi quy lưu**: lập 1 PXH từ 1 ĐNXK đã duyệt trên DB local → lưu → mở chi tiết đúng → xoá phiếu + hoàn trạng thái ĐNXK bằng chức năng huỷ/xoá của màn (nếu không có, đọc `ProductExportService::store` rồi đảo ngược bằng tinker trong transaction) → báo user. Chụp 2 ảnh.

- [x] **Step 5: Đánh `[x]`, sang Task 6.**

---

### Task 6: YCNH — `product-import-requests` (form + chi tiết)

**Files:**
- Modify: `hrm-api/Modules/Finance/Transformers/ProductImportRequestResource/ProductImportRequestDetailResource.php:47` (thêm `status_color`)
- Modify: `hrm-client/pages/finance/product-import-requests/components/ProductImportRequestForm.vue` (L7-762, CSS L2064+)
- Modify: `hrm-client/pages/finance/product-import-requests/_id/index.vue` (L7-321, CSS L944+)
- KHÔNG đụng `product-import-requests/index.vue` (có thay đổi chưa commit của người khác).

**Interfaces:**
- Consumes: `V2BaseFormCard`, K1-K6.
- Produces: `status_color` trong `GET .../product-import-requests/{id}`.

- [x] **Step 1: BE — `status_color`** trong resource, thêm hằng màu theo id trạng thái của `ProductImportRequest` (đọc `ProductImportRequest::STATUSES` lấy đúng tên hằng; tên dưới là theo kiểm kê):

```php
    // Màu badge theo 9 mã chuẩn (CLAUDE.md) — nhóm theo ý nghĩa trạng thái.
    private const STATUS_COLORS = [
        ProductImportRequest::DANG_TAO => '#64748B',
        ProductImportRequest::CHO_DUYET => '#D97706',
        ProductImportRequest::CHO_TP_DUYET => '#D97706',
        ProductImportRequest::CHO_BGD_DUYET => '#D97706',
        ProductImportRequest::CHO_BAN_KIEM_SOAT_DUYET => '#D97706',
        ProductImportRequest::DA_DE_NGHI => '#2563EB',
        ProductImportRequest::DANG_LAP_DE_NGHI => '#2563EB',
        ProductImportRequest::DANG_NHAP_KHO => '#2563EB',
        ProductImportRequest::DANG_HACH_TOAN => '#2563EB',
        ProductImportRequest::DA_NHAP_KHO => '#16A34A',
        ProductImportRequest::DA_HACH_TOAN => '#16A34A',
        ProductImportRequest::DA_HUY_PHIEU => '#6B7280',
    ];
```

dưới `'status_name' => $statusMeta['name'],`: `'status_color' => self::STATUS_COLORS[(int) $this->status] ?? '#64748B',`

Kiểm bằng tinker cho 1 phiếu mỗi trạng thái đang có trong DB: `status_color` không rơi vào mặc định ngoài ý muốn.

- [x] **Step 2: Chi tiết `_id/index.vue`**
  - "Thông tin chung" (L7-106, `.form-card` chép tay + icon `ri-file-list-3-line`) → K1, `#meta` = `CreatorInfoLine :name="data.creator_name"` (fullname thuần). Toàn bộ `<input readonly>` thô → K2. Thứ tự: Mã phiếu, Trạng thái (K3 — mới), Loại yêu cầu, {sourceLabel} (K4 nếu có id nguồn), các `sourceInfoFields` (K2 trong `v-for`), Kho nhập, Nhập thẳng (K2 'Có'/'Không'), Khách hàng / Nhà cung cấp / Nhân viên (giữ `v-if` theo loại), Vận chuyển, Số km dự kiến, Người tiếp nhận, Ghi chú (K5). Bỏ Ngày lập (L23-24), Người lập (L27-28). File đính kèm (L82-103, `attachment-list` + nút thô) → `AttachmentSection readonly :files` theo cách PXG dùng.
  - "Chi tiết" (L109-259, icon `ri-shopping-bag-3-line`) → K6.
  - Card ghi chú `v-for` (L266-269, icon `ri-chat-3-line`) → `V2BaseFormCard :title="note.label"` (lấy đúng tên field nhãn trong file).
  - "Lịch sử thay đổi" (L279-321, `ProductImportRequestHistoryPanel`): đổi vỏ → `V2BaseFormCard title="Lịch sử thay đổi"`, badge đếm + nút "Làm mới" / "Xem lịch sử/Thu gọn" vào `#meta`; bỏ icon `ri-history-line`; ruột + logic thu gọn giữ nguyên. `V2Footer` L323 giữ.

- [x] **Step 3: Form `ProductImportRequestForm.vue`**
  - "Thông tin chung" (L7-322) → `V2BaseFormCard title="Thông tin chung"`, `#meta` = `CreatorInfoLine` (props cũ của L10, bỏ `class="head-meta"`). Ô `sourceInfoFields` dùng `<input readonly>` thô (L132-138) → K2 trong `v-for`. Các ô nhập khác giữ nguyên. File đính kèm (L255-319 tự dựng kéo thả) giữ nguyên ruột (xem "Điểm cần chốt" #5).
  - "Chi tiết" (L327-762, icon `ri-list-check-2`) → K6.

- [x] **Step 4: Dọn CSS** — `.form-card*`, `.head-meta` chép tay trong `.pir-form` (L2064-2085, L2169) và `.pir-detail` (L944-974) xoá (component đã có). Giữ `.history-head-toggle`, `.history-count`. Grep sạch.

- [x] **Step 5: Kiểm** — chi tiết: 1 phiếu nhập NCC (type 99, có Nhà cung cấp + Nhân viên) + 1 phiếu trả hàng khách (type 14), badge đúng màu, mở/thu gọn lịch sử chạy. Form: tạo → chọn loại + nguồn → Quay lại → popup chưa lưu. **Hồi quy lưu nháp**: lưu nháp 1 phiếu → mở lại đúng → xoá. Chụp 2 ảnh.

- [x] **Step 6: Đánh `[x]`, sang Task 7.**

---

### Task 7: ĐNNK — `warehouse-import-requests` (tạo / sửa / chi tiết)

**Files:**
- Modify: `hrm-client/pages/finance/warehouse-import-requests/create.vue` (L9-170, CSS L410+)
- Modify: `hrm-client/pages/finance/warehouse-import-requests/_id/edit.vue` (L10-134, CSS L355+)
- Modify: `hrm-client/pages/finance/warehouse-import-requests/_id/index.vue` (L10-125, CSS L370+)

**Interfaces:**
- Consumes: `V2BaseFormCard`, K1-K6. `WarehouseImportRequestResource` đã có `status_color`, `created_by_name`.

- [x] **Step 1: Chi tiết `_id/index.vue`** — khối L10-61 → K1 `:name="detail.created_by_name"`:

| Ô | Khuôn |
|---|---|
| Mã phiếu | K2 |
| Trạng thái | K3 |
| Loại | K2 |
| Mã YCNH | K4 (link cũ) |
| Số hợp đồng | K4 (link cũ) |
| Nhà cung cấp | K2 col-8 |
| Kho nhập | K2 |
| Phòng ban, Người duyệt | K2 |
| Thời gian nhận, Thời gian duyệt | K2, giữ `v-if` |
| Ghi chú | K5 |
| Ý kiến duyệt (`approve-note`) | K5, giữ `v-if` |

Bỏ Người lập (L41), Ngày tạo (L43). File (L64-78) → `V2BaseFormCard title="File đính kèm"` giữ `v-if`, ruột giữ. Hàng hoá (L81-125) → K6.

- [x] **Step 2: Tạo `create.vue`** — `pick-source` (L9-20) giữ nguyên. Khối L24-65 → K1 `is-create`; ô chỉ đọc Mã YCNH, Loại, Số hợp đồng, Khách hàng/Nhà cung cấp (nhãn động giữ), Ngày yêu cầu, Người yêu cầu theo K2; Kho nhập (`V2BaseSelect`) `col-md-4` giữ binding; Ghi chú K5 giữ `v-model`. File (L68-90) → `V2BaseFormCard title="File đính kèm"`, ruột giữ. Hàng hoá (L93-149) → K6.

- [x] **Step 3: Sửa `_id/edit.vue`** — khối L10-51 → K1. Tên người lập: mở màn xem dữ liệu endpoint edit trả về — dùng `info.created_by_name` nếu có; chỉ có `info.creator_name` thì xem giá trị: là fullname thuần (không hậu tố phòng/mã) thì dùng, là nhãn audit thì DỪNG hỏi user (có thể cần thêm `created_by_name` ở BE). `:created-at="info.created_at"`. Ô chỉ đọc: Mã phiếu, Loại nhập kho, Mã YCNH, Số hợp đồng, Nhà cung cấp/Khách hàng, Phòng ban. Bỏ Người lập (L25), Ngày tạo (L26). Kho nhập + Ghi chú giữ binding. File (L54-77) + hàng hoá (L80-134) như Step 2.

- [x] **Step 4: Import + dọn CSS + Grep sạch** (giữ `.file-list` / `.file-item`).

- [x] **Step 5: Kiểm** — chi tiết 1 phiếu từ YCNH nhà cung cấp + 1 phiếu trả lại điều chuyển (type 17). Tạo: chọn nguồn → đổi Kho nhập → Quay lại → popup chưa lưu. Sửa: đổi Ghi chú → Lưu → mở lại → trả lại. Chụp 3 ảnh.

- [x] **Step 6: Đánh `[x]`, sang Task 8.**

---

### Task 8: PNK — `product-imports` (form + chi tiết)

**Files:**
- Modify: `hrm-api/Modules/Finance/Transformers/ProductImportResource/ProductImportListResource.php:30` (`private const` → `public const STATUS_COLORS`)
- Modify: `hrm-api/Modules/Finance/Transformers/ProductImportResource/ProductImportDetailResource.php` (thêm `status_color`)
- Modify: `hrm-client/pages/finance/product-imports/components/ProductImportForm.vue` (L8-1123, CSS L2794-2857)
- Modify: `hrm-client/pages/finance/product-imports/_id/index.vue` (L11-275, CSS L526-564)
- KHÔNG đụng `product-imports/index.vue` (có thay đổi chưa commit của người khác).

**Interfaces:**
- Consumes: `V2BaseFormCard`, K1-K6.
- Produces: `status_color` trong `GET .../product-imports/{id}`, cùng bảng màu với màn danh sách.

- [x] **Step 1: BE** — `ProductImportListResource` L30 đổi `private const STATUS_COLORS` → `public const STATUS_COLORS` (giá trị giữ nguyên: Đã hoàn thành `#16A34A`, Đang tạo `#64748B`, Bán trả lại `#DC2626`). Trong `ProductImportDetailResource`, dưới `'status_name' => $this->status_name,`:

```php
            // Cùng bảng màu với màn danh sách — 1 nguồn duy nhất.
            'status_color' => ProductImportListResource::STATUS_COLORS[$this->status] ?? '#6B7280',
```

(cùng thư mục `ProductImportResource` → cùng namespace, không cần `use`; khác thì thêm `use`). Kiểm bằng tinker cho 1 phiếu Đã hoàn thành.

- [x] **Step 2: Chi tiết `_id/index.vue`**
  - Khối L11-124 (tiêu đề động `data.import_type_name || data.type_name || 'Phiếu nhập hàng'`, `b-tabs` Thông tin chung / Hạch toán) → `V2BaseFormCard` với `#title` động, `#meta` = `CreatorInfoLine :name="data.creator_name"` (fullname thuần). Bỏ icon.
  - Tab Thông tin chung: `kv-grid` → `form-row`: Mã phiếu, Trạng thái (K3), Loại nhập, Nhập thẳng; nhánh A (Phiếu nhập kho K4, Kho nhập, Thủ kho, Người giao hàng) / nhánh B (Phiếu YC nhập hàng K4, Kho nhập) giữ `v-if`; Khách hàng col-8, Số hợp đồng, Người yêu cầu, Người đề nghị, Ngày duyệt, Không trả hoá đơn, Người cập nhật, Ngày cập nhật, Ghi chú K5. Bỏ Người tạo (L61), Ngày tạo (L62).
  - "Chi tiết" (L127-271) → K6. `SystemInfoSection` L275 giữ.

- [x] **Step 3: Form `ProductImportForm.vue`**
  - loadError (L8-15) → `V2BaseFormCard title="Lỗi tải dữ liệu"`.
  - "Chọn phiếu nguồn" (L19-37) → `V2BaseFormCard title="Chọn phiếu nguồn"`, bỏ `ri-file-add-line`. `V2Footer` L39 giữ nguyên.
  - "Thông tin chung" (L44-142) → K1; `#meta` gồm `hdr-note` mã phiếu (`header.code`, giữ `v-if`) + `CreatorInfoLine` (props L49-54) trong `<div class="d-flex align-items-center" style="gap: 12px">` — bỏ `ml-auto`. `kv-grid` → `form-row`: các ô chỉ đọc theo K2 (Loại nhập, Phiếu nhập kho/YCNH kèm nút sửa giữ nguyên bên cạnh ô, Nhập thẳng, Kho nhập, Thủ kho, Hợp đồng, Ngày xuất, Nhà cung cấp, Khách hàng, Người giao hàng — giữ `v-if`); checkbox "Không trả hóa đơn" + Ghi chú giữ binding; `acc-block` giữ nguyên ruột.
  - "Chi tiết" (L145-1119) → K6. `note-callout` (L1123) giữ.

- [x] **Step 4: Import + dọn CSS + Grep sạch.**

- [x] **Step 5: Kiểm** — chi tiết 1 phiếu nhánh A + 1 phiếu nhánh B, bấm tab Hạch toán. Form: vào tạo từ 1 ĐNNK đã duyệt → đổi Ghi chú → Quay lại → popup chưa lưu. **Hồi quy lưu nháp**: lưu Đang tạo → mở lại → xoá bằng nút Xoá. Chụp 2 ảnh.

- [x] **Step 6: Đánh `[x]`, sang Task 9.**

---

### Task 9: Rà tổng + đề xuất cập nhật CLAUDE.md / skill

**Files:**
- Create: `.plans/gop-db/dong-bo-form-xuat-nhap/de-xuat-pr-claude-md.md`
- Modify: `.plans/gop-db/STATUS.md`

- [x] **Step 1: Grep sạch toàn bộ 17 file FE** — chạy lệnh "Grep sạch" trên từng file; tổng hợp kết quả vào báo cáo.

- [x] **Step 2: Lệnh tự kiểm HTML thô của CLAUDE.md** trên 8 thư mục: `grep -rn '<input \|<textarea\|<select \|<label ' pages/finance/{borrow-sells,borrow-sell-requests,product-export-requests,warehouse-export-requests,product-exports,product-import-requests,warehouse-import-requests,product-imports}/ | grep -v V2Base | grep -v 'index.vue\|print.vue'` — ghi lại các dòng còn sót (ruột bảng ngoài phạm vi thì liệt kê để user biết, không tự sửa).

- [x] **Step 3: 768px toàn bộ** — với 8 màn chi tiết, `browser_resize` 768×900 → `scrollWidth > clientWidth` phải `false`. Console không lỗi (`browser_console_messages`).

- [x] **Step 4: Đo lại PXG-02188** so `pxg-baseline.json` (Review Focus 4) — Expected giống hệt.

- [x] **Step 5: Soạn đề xuất PR** vào `de-xuat-pr-claude-md.md`:
  - `HRM/CLAUDE.md` dòng "Khối NHÓM trong màn form/chi tiết dùng `components/V2BaseFormSection.vue`" → thêm: "Nhóm kho / xuất nhập (8 luồng YCXH, ĐNXK, PXH, YCNH, ĐNNK, PNK, PXBHM, YCXBHM + PXG) dùng `components/V2BaseFormCard.vue` (khuôn PXG-02188)."
  - Skill `erp-to-hrm-screen` L455: nội dung tương tự + đoạn mẫu K1.
  - Không tự sửa 2 file đó.

- [x] **Step 6: Cập nhật `STATUS.md`** (checkpoint) + báo user: danh sách file đã sửa, ảnh chụp, các bản ghi thử đã xoá.

---

## Điểm cần user chốt trước khi chạy

1. **Ô rỗng (#11370)** — PXG ẩn ô Hợp đồng / Địa chỉ khi rỗng; spec chốt "áp dụng mà rỗng → ô xám rỗng". Plan theo **spec** (ô xám rỗng), chỉ ẩn trường không áp dụng cho loại phiếu.
2. **`status_color` ở BE** — 4 resource chi tiết chưa có (PXBHM, YCXBHM, YCNH, PNK); spec chỉ cho BE thêm tên người lập. Plan thêm `status_color` (bảng màu ở Task 1/2/6/8) — cần user đồng ý mở rộng BE và duyệt bảng màu YCNH (Task 6 Step 1).
3. **Gộp ô "Loại phiếu" + "Loại hợp đồng"** ở chi tiết PXBHM (luôn cùng giá trị) → plan bỏ ô "Loại phiếu".
4. **Trạng thái ở tiêu đề trang** — spec §4.1 ghi "không đặt ở header trang", nhưng 6 màn chi tiết đang ghép trạng thái vào topbar qua `buildStatusTitle()`. Plan **giữ nguyên topbar** (không đụng `pageTitle()`), chỉ thêm badge trong lưới. Muốn bỏ trạng thái khỏi topbar thì báo để thêm bước.
5. **File đính kèm tự dựng** ở ĐNXK / ĐNNK (tạo/sửa — `<input type=file>` thô + upload `FormData` lên `/attachments`) và YCNH form (kéo thả tự dựng): đổi sang `AttachmentSection` là đổi cơ chế upload (S3 từng file) → phải sửa BE. Plan **chỉ đổi khung**, giữ ruột; chuyển `AttachmentSection` để việc sau. Màn chi tiết chỉ đọc (YCXH, YCNH) thì đổi sang `AttachmentSection readonly` được vì không đụng upload.
