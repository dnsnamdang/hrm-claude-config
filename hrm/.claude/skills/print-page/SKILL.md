---
name: print-page
description: Use when tạo mới hoặc sửa màn IN (file **/print.vue trong hrm-client) hoặc khi gặp lỗi in — mất viền (phải/dưới/trên khi sang trang), nội dung cột bị cắt/tràn lề phải, mất logo/letterhead, style khác preview, không tự bật hộp thoại in (phải Ctrl+P), bảng ô gộp (rowspan) vỡ khi in nhiều trang, ô gộp trống ở đầu trang sau, viền ngang đậm khác màu.
---

# Skill: Print Page (màn IN trong hrm-client)

Chuẩn hoá cách làm màn IN (`pages/**/print.vue`, `pages/**/_id/print.vue`) trong `hrm-client` (Nuxt/Vue2) để tránh lặp lại loạt lỗi in kinh điển. **Mọi mục dưới đây đã được kiểm chứng thực tế** (kể cả đo đạc bằng iframe).

---

## 1. Cơ chế in — HIỂU cái này trước, mọi lỗi bắt nguồn từ đây

Nút In gọi `this.$printContent(options)` — plugin `hrm-client/plugins/print-content.js`:

1. Mở **cửa sổ mới** (`window.open('')`, base = `about:blank`).
2. Ghi `targetElement.outerHTML` (mặc định selector `#content`; nếu không có `#content` thì rơi xuống fallback `['.print-wrapper', '.container', '#__nuxt', '#app']`).
3. Chỉ nạp **stylesheet ngoài**: `/css/pdf.css`, `/ckeditor/css/editor.css`, `/css/print-app.css` + chuỗi CSS truyền qua `options.styles`.
4. `printWindow.onload = () => printWindow.print()` — chờ tải xong mới bật hộp thoại in.

**Hệ quả cốt lõi (nguồn gốc mọi lỗi):**
- **Scoped `<style>` của component KHÔNG sang cửa sổ in.** Grid/flex/`col-md-*`/font-size... viết trong `<style scoped>` chỉ đúng ở preview màn hình, **mất khi in thật**.
- Chỉ có 3 thứ sống sót sang cửa sổ in: **inline style trên element**, **class có sẵn trong `/css/print-app.css`**, và **CSS truyền qua `options.styles`**.
- `/css/print-app.css` chỉ có: `.table`, `.table-bordered`, `.row`, `.container` + vài utility (`text-center`, `mb-*`, `align-middle`...). **KHÔNG có `.col-md-*`, không grid.**

---

## 2. Quy tắc vàng khi làm màn print.vue

- [ ] Đặt `id="content"` trên div gốc nội dung in (để selector plugin khớp đúng, không rơi vào fallback `.container`).
- [ ] Hiển thị dữ liệu bằng text `{{ }}`, **KHÔNG dùng `<input class="form-control" readonly>`** (in ra thành ô nhập liệu xấu).
- [ ] Layout trường thông tin: dùng **inline style** (vd `style="display:grid; grid-template-columns:repeat(3,1fr)"`), KHÔNG dựa scoped CSS.
- [ ] Ảnh letterhead: dùng **URL tuyệt đối** (xem mục 4), KHÔNG để `src="@/assets/..."` trực tiếp.
- [ ] Toàn bộ CSS viền/độ rộng bảng: truyền qua `options.styles` (xem mục 3), scope bằng selector đủ mạnh (`table.table-bordered ...`).
- [ ] Nút In gọi method riêng (vd `printPackage()`) để truyền `styles` + `pageMargin`, KHÔNG gọi trơn `$printContent()`.

---

## 3. Snippet CSS chèn sẵn cho BẢNG có viền (copy dùng ngay)

Truyền qua `this.$printContent({ styles, pageMargin: '12mm 10mm' })`. Selector `table.table-bordered ...` có specificity cao hơn `.table`/`.table-bordered` trong print-app.css nên ghi đè được (nhớ `!important`). Cửa sổ in chỉ chứa fragment trang này nên target thẳng `table.table-bordered` là an toàn.

```js
const styles = `
    /* [GỐC RỄ lỗi mất viền phải + cắt cột cuối] print-app.css có
       '.container { width:100%; padding:15px }' với box-sizing content-box mặc định
       => container rộng hơn trang 30px => bảng bị đẩy tràn mép phải, 15px bên phải bị cắt.
       Ép container border-box + bỏ padding ngang: */
    #content, .container {
        box-sizing: border-box !important;
        width: 100% !important; max-width: 100% !important;
        padding-left: 0 !important; padding-right: 0 !important;
        margin-left: 0 !important; margin-right: 0 !important;
    }
    table.table-bordered {
        width: 100% !important; max-width: 100% !important;
        table-layout: fixed !important;      /* tôn trọng <colgroup>, cột không tự phình */
        border-collapse: collapse !important;
    }
    /* Viền ĐỦ 4 CẠNH mỗi ô => KHÔNG mất viền trên khi bảng sang trang mới
       (border-collapse: separate CHỈ vẽ border-top của table 1 lần ở đỉnh => trang sau mất viền trên). */
    table.table-bordered th, table.table-bordered td {
        border: 1px solid #333 !important;
        padding: 3px 5px !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
    }
    /* print-app.css có '.table tbody + tbody { border-top: 2px }'. Nếu mỗi nhóm là 1 <tbody>
       thì rule này tạo đường ngang 2px ĐẬM khác màu giữa các nhóm => bỏ viền cấp tbody: */
    table.table-bordered tbody, table.table-bordered tbody + tbody {
        border: 0 !important; border-top: 0 !important;
    }
`
this.$printContent({ styles, pageMargin: '12mm 10mm' })
```

Kèm `<colgroup>` khai báo % độ rộng cột (tổng = 100%) ngay sau thẻ mở bảng, để cột có `table-layout: fixed` phân bổ đúng:
```html
<b-table-simple bordered small>
    <colgroup>
        <col style="width: 4%" /><col style="width: 11%" /><!-- ... tổng 100% -->
    </colgroup>
    ...
</b-table-simple>
```

---

## 4. Ảnh/logo mất + không tự bật hộp thoại in

`src="@/assets/..."` (hoặc `require('@/assets/...')`) qua webpack ra đường dẫn **root-relative** `/_nuxt/...`. Cửa sổ in `about:blank` không có base URL → ảnh không tải → **mất logo**, VÀ `onload` không kích hoạt → **`print()` không tự chạy (phải Ctrl+P)**.

Fix — ghép `window.location.origin` thành URL tuyệt đối (set trong `mounted`, KHÔNG dùng computed để tránh SSR mismatch), bind `:src`:
```js
data() { return { logoSrc: '' } },
mounted() { this.setLogoSrc() },
methods: {
    setLogoSrc() {
        const src = require('@/assets/images/info-tpe.jpg')
        this.logoSrc = (typeof window !== 'undefined' && typeof src === 'string' && src.charAt(0) === '/')
            ? window.location.origin + src : src
    },
},
```
```html
<img v-if="logoSrc" :src="logoSrc" width="100%" />
```

---

## 5. Bảng có Ô GỘP (rowspan) in qua NHIỀU TRANG — đánh đổi, KHÔNG có cách vẹn cả đôi đường

Trình duyệt (`window.print`) **không thể lặp lại nội dung ô gộp ở đầu mỗi trang** — giới hạn cố hữu. Có 3 hướng, HỎI USER chọn:

| Hướng | Ô gộp | Khoảng trắng cuối trang | Ô trống/mất viền |
|-------|-------|-------------------------|------------------|
| Bỏ ô gộp, làm phẳng (lặp lại thông tin mỗi dòng) | Không | Không | Không |
| **Giữ ô gộp + `page-break-inside: avoid`** (khuyến nghị nếu muốn giữ merge) | Có (đẹp như preview) | Có | Không |
| Giữ ô gộp + chảy liền mạch | Có | Không | CÓ (ô gộp trống đầu trang sau) |

Cách giữ ô gộp mà KHÔNG có ô trống: **mỗi nhóm là 1 `<b-tbody class="xxx">`** + rule:
```css
table.table-bordered tbody.xxx { page-break-inside: avoid !important; break-inside: avoid !important; }
```
Với bảng KHÔNG có rowspan nhưng dòng cao (dễ bị cắt ngang trang làm rớt viền dưới): áp avoid ở **cấp dòng** — `tbody.yyy tr { page-break-inside: avoid !important }`.

> Lưu ý Vue 2: `<template v-for>` phải đặt `:key` trên phần tử con thật (`<b-tr :key>`), KHÔNG trên `<template>`. IDE báo lỗi code 33 "key should be on template" là quy tắc Vue 3 — bỏ qua.

---

## 6. Màn mẫu IN TỐT NHẤT project (tham khảo khi cần)

- `pages/assign/report/task-manager-by-employees/print.vue` — báo cáo bảng dài nhiều trang **không lỗi**: làm phẳng dữ liệu phân cấp (indent + class, KHÔNG rowspan ở tbody), truyền toàn bộ CSS qua `styles`, `table-layout: fixed` + cột cố định + viền 1px mọi ô.
- `pages/assign/assign_business/_id/print.vue` — `<colgroup>` + `generatePrintStyles()` tự nhân bản CSS vào cửa sổ in + ngắt trang mỗi phiếu bằng `page-break-after`.
- Màn tham chiếu đã sửa đầy đủ theo skill này: `pages/decision/category/insurance-packages/_id/print.vue`.

> KHÔNG có màn nào render PDF từ backend. Route `/print` ở `hrm-api` chỉ trả HTML template CKEditor, không phải PDF. Đừng đi tìm "đường tắt PDF".

---

## 7. Cách VERIFY lỗi layout in mà không cần đăng nhập

Lỗi tràn/cắt/viền thường thuần CSS. Dựng iframe rộng đúng khổ giấy, nạp print-app.css + styles, đo `getBoundingClientRect` — không cần login:
```js
const iframe = document.createElement('iframe')
iframe.style.cssText = 'width:190mm;height:400px;position:fixed;left:-9999px'  // A4 - lề 10mm x2
document.body.appendChild(iframe)
const doc = iframe.contentDocument
doc.open()
doc.write('<link rel="stylesheet" href="/css/print-app.css"/><style>'+injectedStyles+'</style>'
    + '<body class="document-editor">'+contentHTML+'</body>')
doc.close()
// so sánh table.getBoundingClientRect().right với body.getBoundingClientRect().right
// => overflowRightPx > 0 nghĩa là đang tràn mép phải
```

---

## Checklist debug nhanh khi user báo "in bị lỗi"

| Triệu chứng | Nguyên nhân | Fix |
|-------------|-------------|-----|
| Trường như ô input | Dùng `<input readonly>` | Đổi sang text `{{ }}` |
| Layout vỡ / dồn 1 cột khi in (preview OK) | Scoped CSS không sang cửa sổ in | Chuyển sang inline style / `options.styles` |
| Cột cuối bị cắt, mất viền phải (chỉnh lề/độ rộng vô ích) | `.container` content-box + padding 15px → tràn 30px | `#content,.container { box-sizing:border-box; padding:0 }` |
| Mất viền trên ở trang 2+ | `border-collapse: separate` chỉ vẽ border-top 1 lần | `collapse` + `border:1px` đủ 4 cạnh mỗi ô |
| Viền ngang đậm khác màu giữa nhóm | `print-app.css .table tbody + tbody { border-top:2px }` | Bỏ viền cấp tbody |
| Ô gộp trống có viền ở đầu trang sau | rowspan bị cắt ngang trang | `page-break-inside: avoid` mỗi nhóm (1 tbody) |
| Mất logo + phải Ctrl+P | Ảnh root-relative không tải ở about:blank | URL tuyệt đối `origin + require(...)` |
| Cột Ghi chú tự phình rộng | auto-layout ăn theo text dài | `table-layout: fixed` + `<colgroup>` % |
