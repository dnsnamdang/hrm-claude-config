---
name: print-page
description: Use when tạo mới hoặc sửa màn IN (file **/print.vue trong hrm-client) hoặc khi gặp lỗi in — mất viền (phải/dưới/trên khi sang trang), nội dung cột bị cắt/tràn lề phải, mất logo/letterhead, letterhead ra sai công ty (khác công ty ghi trên chứng từ), style khác preview, không tự bật hộp thoại in (phải Ctrl+P), bảng ô gộp (rowspan) vỡ khi in nhiều trang, ô gộp trống ở đầu trang sau, viền ngang đậm khác màu.
---

# Skill: Print Page (màn IN trong hrm-client)

Chuẩn hoá cách làm màn IN (`pages/**/print.vue`, `pages/**/_id/print.vue`) trong `hrm-client` (Nuxt/Vue2) để tránh lặp lại loạt lỗi in kinh điển. **Mọi mục dưới đây đã được kiểm chứng thực tế** (kể cả đo đạc bằng iframe).

---

## 0. KHUÔN HIỂN THỊ CHUẨN của màn IN (chốt 2026-08-21) — copy nguyên, KHÔNG tự chế

Màn mẫu: `pages/customer-care/warranty-repair-requests/_id/print.vue` (khổ DỌC) và
`pages/customer-care/warranty-repair-handle-requests/print.vue` (khổ NGANG).
Mọi màn in phải giống 3 điểm sau, không có ngoại lệ:

1. **KHÔNG có menu / topbar** — khai `layout: 'print'` (`layouts/print.vue`). Dùng
   `default-sidebar` thì mặt giấy bị đẩy xuống ~130px và hở dải xanh của topbar ở đầu trang.
   Nền xám `#eee` quanh tờ giấy do layout lo — màn in **KHÔNG khai `background` riêng**.
2. **Nút In nằm TRÊN tờ giấy, canh MÉP PHẢI của giấy** — thanh công cụ riêng `.print-toolbar`:
   ```html
   <div class="mb-1 no-print print-toolbar d-flex align-items-center justify-content-end" style="gap: 12px">
       <V2BaseButton primary size="sm" class="no-print" :interactable="!loading && !!template" @click="printRequest">
           <template #prefix><i class="ri-printer-line" style="font-size: 15px"></i></template>
           In
       </V2BaseButton>
       <span v-if="loading" class="mr-auto" style="color: #6b7280">Đang tải dữ liệu in...</span>
       <span v-if="loadError" class="mr-auto" style="color: #dc2626">{{ loadError }}</span>
   </div>
   ```
   - Dùng `V2BaseButton` + icon Remix `ri-printer-line`. **CẤM** `<button class="btn btn-primary">`
     và **CẤM** icon `fa fa-print` — hrm-client không nạp FontAwesome, ra ô vuông tofu.
   - `V2BaseButton` không có prop `disabled` → dùng `:interactable`.
   - Dòng trạng thái (Đang tải / lỗi) đặt `class="mr-auto"` để nằm bên TRÁI, nút vẫn sát mép phải.
3. **Bản xem trước phải ra hình TỜ GIẤY** — `#content` nền trắng, rộng đúng khổ, viền xám + bo góc
   + đổ bóng, canh giữa; `.print-toolbar` rộng bằng đúng tờ giấy để nút thẳng mép phải giấy:
   ```scss
   .print-preview { min-height: 100vh; display: flow-root; }   /* flow-root: chặn margin collapsing của .container.mt-3 */
   .print-preview ::v-deep .container { max-width: 100%; }      /* .container-fluid nếu màn dùng fluid */
   .print-preview ::v-deep .print-toolbar { width: 210mm; max-width: 100%; margin-left: auto; margin-right: auto; }
   .print-preview #content {
       width: 210mm; max-width: 100%; margin-left: auto; margin-right: auto;
       padding: 15mm 22mm 22mm 20mm;   /* khổ NGANG: width 297mm, padding 15mm */
       border: 1px solid #d3d3d3; border-radius: 5px; background: #fff;
       box-shadow: 0 0 5px rgba(0, 0, 0, 0.1); box-sizing: border-box;
   }
   @media print { .print-preview #content { width: 100%; padding: 0; border: 0; border-radius: 0; box-shadow: none; } }
   ```
   ⚠️ Bám class `.print-toolbar`, **KHÔNG** đặt `width` theo `.no-print` — class đó nằm trên cả cái
   nút, nút sẽ bị kéo rộng bằng cả tờ giấy.
   ⚠️ Màn nào đã có sẵn khối `#content` trong `::v-deep { ... }` thì rule `@media print` reset khung
   phải đặt **SAU** khối đó (cùng độ ưu tiên id, rule đứng sau mới thắng).
4. `head()` khai `link: [{ rel: 'stylesheet', href: '/css/print-app.css' }]` — **KHÔNG** khai
   `/css/pdf.css` (hrm-client không có file này, khai vào là 404).

> Đã áp cho 13 màn ERP→HRM ngày 2026-08-21 (lỗi thiết bị, DM dịch vụ SC, DM tài khoản, YC nhập
> hàng, chuyển hàng nhập thẳng, nhóm hàng giữ). Màn in mới **bắt buộc** copy khuôn này.

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

- [ ] **`layout: 'print'`** — BẮT BUỘC, xem mục 2b. Đây là lỗi hay gặp nhất khi copy màn in có sẵn.
- [ ] Đặt `id="content"` trên div gốc nội dung in (để selector plugin khớp đúng, không rơi vào fallback `.container`).
- [ ] Hiển thị dữ liệu bằng text `{{ }}`, **KHÔNG dùng `<input class="form-control" readonly>`** (in ra thành ô nhập liệu xấu).
- [ ] Layout trường thông tin: dùng **inline style** (vd `style="display:grid; grid-template-columns:repeat(3,1fr)"`), KHÔNG dựa scoped CSS.
- [ ] Ảnh letterhead: dùng **URL tuyệt đối** (xem mục 4), KHÔNG để `src="@/assets/..."` trực tiếp.
- [ ] Toàn bộ CSS viền/độ rộng bảng: truyền qua `options.styles` (xem mục 3), scope bằng selector đủ mạnh (`table.table-bordered ...`).
- [ ] Nút In gọi method riêng (vd `printPackage()`) để truyền `styles` + `pageMargin`, KHÔNG gọi trơn `$printContent()`.

---

## 2b. Layout của trang in — BẮT BUỘC `layout: 'print'` (chốt 2026-08-19)

Trang in là **bản xem trước tờ giấy**: không topbar, không sidebar, **nền quanh giấy XÁM `#eee`**
(xem mục 2c) — tờ giấy `#content` mới là màu trắng.

```js
export default {
    layout: 'print',   // layouts/print.vue
    // ...
}
```

**Dùng `default` hay `default-sidebar` là SAI** — phía trên mặt giấy sẽ hở một dải xanh + khoảng
trắng vô nghĩa, do lớp vỏ ứng dụng chứ không phải nội dung in:

| Nguồn | Chiều cao thừa |
| --- | --- |
| `.navbar-custom` (topbar, chỉ hiện tên user trên nền gradient xanh) | 60px |
| `.content-page { padding-top }` (chừa chỗ cho topbar cố định) | 60–70px |
| `.container.mt-3` của chính trang | 16px |
| **Tổng** | **~136px** đẩy tờ giấy xuống |

Đừng bù trừ bằng `margin-top: -70px` ở từng màn — vỏ ứng dụng vẫn render, vẫn chiếm DOM và vẫn
lộ ra khi cuộn. Bỏ hẳn layout mới đúng.

### Bỏ topbar rồi VẪN còn một dải khác màu ở đầu trang?

Đó là **margin collapsing**, không phải padding sót. Trang in mở đầu bằng `.container.mt-3`:
`margin-top: 16px` của con **tràn ra ngoài** và đẩy cả layout xuống, để lộ nền `#f5f6f8`
của `body`.

`layouts/print.vue` chốt sẵn 2 lớp, màn dùng KHÔNG phải khai gì thêm:

```scss
.print-layout {
    min-height: 100vh;
    background: #eee;     /* nền quanh giấy, chuẩn chung mọi màn in - xem mục 2c */
    display: flow-root;   /* tạo BFC -> margin của con nằm GỌN bên trong vùng xám */
}

/* Cuộn quá đáy (hiệu ứng nảy macOS) hoặc trang ngắn hơn màn hình thì nền body vẫn lộ */
body:has(.print-layout) { background: #eee; }
```

⚠️ **KHÔNG dùng `overflow: auto`** để tạo BFC: trang in rất dài, nó đẻ ra thanh cuộn lồng nhau.
⚠️ **KHÔNG đặt `background` lên `body` trần** trong style không scoped của layout — sẽ ăn sang
mọi màn khác của ứng dụng.

Tự kiểm: điểm `(giữa màn, y = 0)` phải là `.print-layout` (hoặc `.print-preview` của chính màn)
và nền `rgb(238, 238, 238)` — ra `rgb(255, 255, 255)` là đang hở dải nền của lớp dưới.

```js
const el = document.elementFromPoint(innerWidth / 2, 0)
el.className, getComputedStyle(el).backgroundColor   // 'print-layout', 'rgb(238, 238, 238)'
```

⚠️ **Cùng bẫy margin collapsing lặp lại ở CHÍNH màn in**: nếu `print.vue` bọc thêm một lớp
(`.print-preview`) quanh `.container.mt-3` thì lớp đó cũng phải `display: flow-root`, không thì
nó bị đẩy xuống 16px và hở một dải khác màu ngay đầu trang (đã dính thật ở 2 màn Kiểm tra bảo
hành sửa chữa). Cũng KHÔNG dùng `overflow: auto` ở đây, vì lý do y hệt.

⚠️ **Rà khi đụng vào màn in cũ**: phần lớn trang `print.vue` trong repo đang khai
`default-sidebar` hoặc không khai layout (rơi về `default`) — **đều bị hở**. Sửa dần khi có dịp
đụng vào màn đó, KHÔNG sửa đại trà (quy tắc chung của team).

Cách tự kiểm nhanh trên trình duyệt:

```js
// đứng ở trang in, chạy trong console — cả 2 phải là false / 16
!!document.querySelector('.navbar-custom')                              // false
Math.round(document.querySelector('.print-preview').getBoundingClientRect().top)  // 16
```

---

## 2c. KHUNG TỜ GIẤY ở màn xem trước — bắt buộc, ERP có sẵn (chốt 2026-08-19)

Màn `print.vue` là bản **xem trước tờ giấy**, nên `#content` phải được vẽ thành một tờ A4 thật:
đúng bề ngang khổ giấy, padding bằng lề `@page`, viền xám + bo góc + đổ bóng, căn giữa màn hình.
Thiếu khung này thì nội dung trải hết bề ngang trình duyệt, người xem không biết chữ sẽ rơi vào
đâu trên giấy — và trông lệch hẳn so với ERP.

Thông số copy từ ERP (`resources/views/print.blade.php` và `print_landscape.blade.php`). Riêng
**màu nền quanh giấy** thì ERP vênh nhau (bản dọc trắng, bản ngang `#eee`) — bên HRM thống nhất
**nền XÁM `#eee` cho MỌI màn in, dọc lẫn ngang** (chốt 2026-08-20), lấy theo bản ngang của ERP:
nền xám thì tờ giấy nổi hẳn lên, nền trắng thì giấy chỉ còn cái viền mờ, nhìn như trang web thường.

**Màu nền đã nằm sẵn trong `layouts/print.vue` — màn in KHÔNG khai `background` riêng nữa.** Lớp
bọc của màn (`.print-preview`) chỉ cần `min-height: 100vh` + `display: flow-root`.

| | Khổ DỌC (1 phiếu) | Khổ NGANG (danh sách) |
| --- | --- | --- |
| `width` | `210mm` | `297mm` |
| `padding` | `15mm 22mm 22mm 20mm` (bằng lề `@page`) | `15mm` |
| Nền quanh giấy | `#eee` | `#eee` | ← do `layouts/print.vue` lo, **dùng CHUNG cho mọi màn in**
| Viền / bo / bóng | `1px solid #d3d3d3` · `5px` · `0 0 5px rgba(0,0,0,.1)` | như bên cạnh |

```scss
/* Lớp bọc của màn: KHÔNG khai `background` (layout lo rồi), nhưng PHẢI có flow-root */
.print-preview {
    min-height: 100vh;
    display: flow-root;
}
.print-preview #content {
    width: 210mm;             /* 297mm nếu mẫu khổ ngang */
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;       /* căn giữa — KHÔNG dùng flex, xem bẫy dưới */
    padding: 15mm 22mm 22mm 20mm;
    border: 1px solid #d3d3d3;
    border-radius: 5px;
    background: #fff;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
}
/* Thanh công cụ rộng bằng tờ giấy để nút In thẳng MÉP PHẢI của giấy */
.print-preview ::v-deep .print-toolbar {
    width: 210mm;
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
}
/* User tự Ctrl+P trên trang preview -> bỏ khung, giấy thật đã có lề của @page */
@media print {
    .print-preview #content {
        width: 100%; padding: 0; border: 0; border-radius: 0; box-shadow: none;
    }
}
```

**Nút "In": `V2BaseButton primary size="sm"` như mọi nút chính khác, CĂN PHẢI thẳng mép phải tờ
giấy.** Icon `ri-printer-line` 15px, hàng nút `d-flex align-items-center justify-content-end`;
dòng trạng thái ("Đang tải…", lỗi) đặt `mr-auto` để bị đẩy sang trái, nút vẫn nằm sát mép phải.
Đừng tự chế cỡ nút riêng cho màn in.

```vue
<div class="mb-1 no-print print-toolbar d-flex align-items-center justify-content-end" style="gap: 12px">
    <span v-if="loading" class="mr-auto" style="color: #6b7280">Đang tải dữ liệu in...</span>
    <V2BaseButton primary size="sm" class="no-print" :interactable="!loading && !!template" @click="printRequest">
        <template #prefix><i class="ri-printer-line" style="font-size: 15px"></i></template>
        In
    </V2BaseButton>
</div>
```

⚠️ **Đặt `width` cho thanh công cụ thì bám class RIÊNG (`.print-toolbar`), đừng bám `.no-print`** —
class `no-print` nằm trên cả chính cái nút, nên `.no-print { width: 210mm }` kéo NÚT rộng bằng cả
tờ giấy (đã dính thật: nút 794px).

⚠️ **Đừng căn giữa bằng `display:flex; align-items:center` trên `.container`** — nó căn giữa
**mọi** con, kể cả hàng nút "In", nút trôi ra giữa màn hình. Dùng `margin: 0 auto` cho từng khối.

⚠️ Khung này **chỉ ở PREVIEW**. Cửa sổ in thật nhận style riêng qua `options.styles` của
`$printContent` (scoped CSS không sang cửa sổ in) — đừng chép viền/bóng vào đó.

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

## 3b. Khối KÝ TÊN — luôn ép rộng bằng thân phiếu

Triệu chứng: `NGƯỜI YÊU CẦU · TRƯỞNG PHÒNG · PHÒNG NHẬN · BAN GIÁM ĐỐC` **dồn về bên trái**, ô
cuối hụt hẳn so với mép phải của bảng dữ liệu phía trên.

Nguyên nhân — 2 thứ cộng lại, đều nằm trong **mẫu in của ERP** (`report_templates`), không phải ở
code màn:

```html
<table class="block no-border" style="width:827px">        <!-- (1) rộng CỨNG 827px -->
  <tr><td style="width:20%">…</td> ×4                       <!-- (2) 4 × 20% = 80%, thiếu 20% -->
```

1. **`width:827px`** là khổ giấy của ERP. Thân phiếu để `width:100%` nên rộng theo khung
   (đo thật: 1110px ở preview / 683px ở khổ in) → bảng ký ngắn hơn 283px, co về trái.
2. Snippet ở mục 3 chỉ ép `table:not(.no-border) { width: 100% }`. Bảng ký **CÓ** `.no-border`
   (để giấu viền) nên bị loại trừ — đây là chỗ dễ bỏ sót nhất.

Fix, khai ở **CẢ 2 nơi** (`options.styles` cho cửa sổ in **và** `<style scoped>` cho bản xem trước
— scoped CSS không sang cửa sổ in, xem mục 1):

```css
#content table.block { width: 100% !important; table-layout: fixed !important; }
#content table.block > tbody > tr > td { width: auto !important; }
```

Dùng `width: auto` chứ **không** viết cứng `25%`: `table-layout: fixed` + `auto` cho các ô chia
đều, đúng cả khi mẫu có 3 hay 5 cột ký.

Tự kiểm bằng iframe khổ in (mục 7) — 3 con số phải khớp:

```js
sig.getBoundingClientRect().width === body.width        // bảng ký rộng bằng khung in
data.every(w => w === body.width)                        // và bằng các bảng thân phiếu
new Set(cells.map(c => Math.round(c.width))).size === 1  // các ô ký rộng bằng nhau
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

## 4b. LETTERHEAD CÔNG TY (logo đầu chứng từ) — BẮT BUỘC theo đúng khuôn này

Áp dụng cho **mọi màn in chứng từ** (phiếu thu, phiếu chi, đề nghị, báo giá, hợp đồng…) — bản in HTML
lẫn file Excel. Mục 4 ở trên nói về ảnh tĩnh trong `assets/`; mục này nói về **letterhead theo công ty**.

### Nguồn dữ liệu — chỉ một chỗ duy nhất

Cột `companies.header` (letterhead ngang đầu trang) và `companies.logo`. **Không có nguồn nào khác** —
không `master_settings`, không ảnh tĩnh trong `assets/`, không hardcode theo công ty.

⚠️ **File ảnh KHÔNG nằm trong DB** — nó là file trên đĩa server ERP (`erp/public/uploads/*.png`).
Gộp DB dùng chung `gop_db` **không** kéo file sang. Vì vậy giá trị lưu trong cột phải là **URL tuyệt
đối** thì mới mở được từ domain HRM.

| Domain | `/uploads/1751696586ts-hn.png` |
| --- | --- |
| `https://erp.eteksofts.com` | **200** image/png |
| `https://dev-hrm.eteksofts.com` | **404** `{"code":404,"message":"Route Not Found!"}` |

Dữ liệu `companies.header/logo` trên `gop_db` đã được chuẩn hoá về tuyệt đối ngày 2026-08-21
(`UPDATE companies SET header = CONCAT('https://erp.eteksofts.com', header) WHERE header LIKE '/uploads/%'`,
làm tương tự cho `logo`). **Mỗi môi trường phải tự chạy 2 câu này.** Rollback:
`.plans/gop-db/finance-bill-income/rollback-companies-header-logo.sql`.

### Khuôn code BẮT BUỘC copy (BE)

Nguyên bản: `Modules/Finance/Services/BillIncomePrintService.php::headerUrl()` (bản Phiếu chi
`BillPaymentPrintService.php` y hệt). Cùng cách màn **Báo giá** đang dùng ở FE
(`pages/assign/quotations/_id/index.vue::companyHeaderUrl`): **dùng NGUYÊN giá trị, không bịa host**.

```php
private function headerUrl(<Entity> $bill): string
{
    // 1. Công ty GHI TRÊN CHỨNG TỪ trước, người tạo chỉ là fallback (xem "3 cái bẫy" bên dưới)
    $companyId = $bill->company_id ?: optional(optional($bill->employeeCreate)->info)->company_id;
    if (!$companyId) {
        return '';
    }

    $header = trim((string) (DB::table('companies')->where('id', $companyId)->value('header') ?? ''));
    if ($header === '') {
        return '';
    }

    // 2. Đã tuyệt đối / data URI -> dùng nguyên (nhánh này ăn dữ liệu đã chuẩn hoá)
    if (preg_match('#^(https?:)?//#i', $header) || strpos($header, 'data:') === 0) {
        return $header;
    }

    // 3. Còn tương đối -> ghép ERP_URL; KHÔNG có ERP_URL thì trả nguyên path, TUYỆT ĐỐI không trả ''
    $erpUrl = rtrim((string) env('ERP_URL'), '/');

    return $erpUrl === '' ? $header : $erpUrl . '/' . ltrim($header, '/');
}
```

Mẫu in trong `report_templates` nhúng `<img src="{{HEADER}}" style="width:100%">` → chỉ cần đổ giá
trị trên vào placeholder `HEADER`. File Excel dùng lại đúng hàm này qua trait
`EmbedsCompanyLetterhead` (xem skill `export-excel` mục 4).

### 3 cái bẫy đã trả giá thật (2026-08-21, màn Phiếu thu + Phiếu chi)

1. **Lấy công ty theo NGƯỜI TẠO (như ERP) là sai với chứng từ.** ERP đọc
   `employee_create->info->company->header`. Đo trên dữ liệu thật: **133/2.347 phiếu thu mất hẳn logo**
   (nhân viên lập phiếu không có `employee_infos.company_id`) và **497 phiếu thu + 162 phiếu chi** in ra
   logo của công ty KHÁC công ty ghi trên phiếu. Chứng từ có cột `company_id` riêng → ưu tiên cột đó.
   Helper `erpCompanyHeader()` / `AccountService::companyHeader()` / `ServiceService::companyHeader()`
   lấy công ty **NGƯỜI ĐANG ĐĂNG NHẬP** — chỉ hợp cho báo cáo/danh mục, **không dùng cho chứng từ**
   (thủ quỹ công ty A in phiếu công ty B là ra sai letterhead).
2. **Trả `''` khi thiếu `ERP_URL` = mất hẳn logo, im lặng.** Trả nguyên path tương đối thì trình duyệt
   còn phân giải theo host đang mở, và sau này HRM tự phục vụ `/uploads` là chạy luôn, không phải sửa code.
3. **Ảnh hỏng bị `display:none`, không có icon ảnh vỡ.** `print.vue` (`settleImages()`) cố ý ẩn ảnh lỗi
   để bản in không dính icon vỡ → nhìn màn hình tưởng "code không đổ logo", thật ra là URL 404.
   **Debug phải xem `src` thật**, đừng nhìn màn hình mà đoán.

### Cách verify KHÔNG cần mở trình duyệt

```php
// tinker: đọc thẳng src trong HTML đã fill
$svc = app(BillIncomePrintService::class);
preg_match('/<img[^>]*src="([^"]*)"/i', $svc->render($bill), $m); echo $m[1];
```
```bash
curl -sk -o /dev/null -w "%{http_code}
" "<url vừa in ra>"    # phải 200, không phải 404
```
Đếm trước/sau bằng SQL để biết sửa có tác dụng thật không:
```sql
SELECT SUM(c.header IS NULL OR c.header='') AS mat_logo FROM <bang_chung_tu> t
LEFT JOIN companies c ON c.id = COALESCE(NULLIF(t.company_id,0), (SELECT company_id FROM employee_infos WHERE id = t.created_by));
```

⚠️ Máy local **không có** `erp/public/uploads` (repo ERP không commit thư mục này) → mọi letterhead
404 ở local. Verify tới bước "URL đúng + `curl` ra 200 trên server thật" là đủ, và **nói rõ với user**
phần hiển thị chưa kiểm chứng bằng mắt.

### Lưu ý vận hành

Màn Sửa công ty bên ERP (`CompaniesController.php:275,601`) lưu thẳng `$request->header` từ file
picker → ai sửa lại ảnh công ty sẽ ghi đè về path tương đối `/uploads/...`. Vì vậy **vẫn giữ
`ERP_URL=https://erp.eteksofts.com` trong `.env`** làm lưới an toàn, dù dữ liệu đã chuẩn hoá.

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
| Mất logo letterhead (ảnh tĩnh vẫn OK) | `companies.header` là path tương đối / `ERP_URL` rỗng → `src` 404, bị `display:none` | Mục 4b — chuẩn hoá `companies.header` về URL tuyệt đối, không trả `''` |
| Logo ra ĐÚNG ảnh nhưng SAI công ty | Lấy công ty người tạo / người đăng nhập thay vì `company_id` trên chứng từ | Mục 4b — `$bill->company_id` trước, người tạo chỉ là fallback |
| Cột Ghi chú tự phình rộng | auto-layout ăn theo text dài | `table-layout: fixed` + `<colgroup>` % |
| **Khối KÝ TÊN dồn về trái, hụt so với mép phải** | Mẫu ERP khai cứng `width:827px` cho bảng ký `class="block no-border"`; rule `table:not(.no-border)` KHÔNG với tới nó | `#content table.block { width:100% !important; table-layout:fixed !important }` + `td { width:auto !important }` (mục 3b) |

## 8. Bản in mở bằng POPUP, KHÔNG mở trang riêng (chốt 2026-08-22)

Nút **In** ở màn danh sách / chi tiết mở **popup xem trước** ngay tại chỗ. KHÔNG `window.open()`
sang trang `/print` nữa: mở tab mới làm mất ngữ cảnh đang xem, quay lại phải tải lại cả màn danh
sách kèm bộ lọc. Khuôn gốc: popup xem trước của màn Báo giá (`/assign/quotations/{id}`).

Bộ dùng chung — **chỉ cần khai báo, không viết lại**:

| Lớp | Dùng cái gì |
| --- | --- |
| Popup + nút In + CSS khi in | `components/print/ReportPrintPreviewModal.vue` |
| Nạp HTML từ BE, quản trạng thái | `utils/mixins/reportPrintPreviewMixin.js` |
| Biến `{{HEADER}}` (letterhead) ở BE | trait `Modules/CustomerCare/Services/Concerns/PrintsCompanyLetterhead` |

```js
mixins: [reportPrintPreviewMixin],
components: { ReportPrintPreviewModal },
// khổ dọc (1 chứng từ):
this.openPrintDetail('customer-care/wr-information-requests', item.id, 'Xem trước phiếu …')
// khổ ngang (danh sách theo bộ lọc):
this.openPrintList('customer-care/wr-information-requests', this.filters, 'Xem trước danh sách …')
```

```vue
<ReportPrintPreviewModal
    :show="printPreview.show" :html="printPreview.html" :loading="printPreview.loading"
    :error="printPreview.error" :title="printPreview.title" :landscape="printPreview.landscape"
    @close="printPreview.show = false" />
```

⚠️ Thẻ popup phải nằm **trong thẻ gốc của template**. Đặt sau `</div>` cuối là Vue báo
"template should contain exactly one root element"; đặt nhầm xuống dưới `<style>` thì webpack ném
`SassError: Invalid CSS after "}"` — cả 2 lỗi đều đã dính khi làm 3 màn CSKH.

### 8a. MỘT nguồn CSS cho cả xem trước và bản in

Xem trước và trang in **phải giống hệt nhau**. Muốn vậy chỉ được có MỘT nguồn CSS:
`utils/print/reportPrintStyle.js` → `buildReportPrintCss(root)`, gọi với `.report-print-content`
cho popup và `body` cho trang in. Component KHÔNG được có rule nội dung trong `<style>` của nó
(chỉ style khung popup) — thêm vào đó là sinh nguồn thứ hai, sửa một bên quên bên kia là lệch
(user đã bắt được: xem trước chữ thường mà in ra đậm).

3 chỗ nhất định phải khai, nếu không 2 bên KHÔNG BAO GIỜ khớp:

| Thuộc tính | Vì sao lệch |
| --- | --- |
| `text-align` | UA đặt `table { text-align: start }`, trang HRM đặt `left` → phải khai lại cho `table/tr/th/td` |
| `line-height` | UA để `normal` cho bảng, trang HRM có sẵn giá trị khác → khai `line-height: inherit` |
| mọi thuộc tính hình thức | trong popup còn cả bootstrap + CSS toàn cục → phải `!important` |

⚠️ Khối CSS nằm trong **template literal** — TUYỆT ĐỐI không dùng dấu \` trong chú thích, một dấu
là đứt chuỗi và hỏng cả file.

**Cách tự kiểm (đã dùng để chốt)** — dựng iframe bằng đúng `printCss()` rồi so từng phần tử:

```js
const root = vm.$refs.printContent
const f = document.createElement('iframe')
f.style.cssText = `position:fixed;left:-9999px;width:${root.clientWidth}px;height:900px`
document.body.appendChild(f)
f.contentDocument.write('<html><head><style>'+vm.printCss()+'</style></head><body>'+root.innerHTML+'</body></html>')
// so getComputedStyle từng phần tử của root vs iframe -> phải LỆCH 0
```

Bề rộng iframe phải bằng bề rộng vùng xem trước, nếu không `height` chênh và báo động giả.

### 8b. Hình thức bản in — bám bản in báo giá

- **Letterhead đầu trang**: mẫu in ERP nào cũng mở đầu bằng `<img src="{{HEADER}}">`. Service quên
  truyền biến `HEADER` thì bản in **trống phần đầu, không có lỗi nào báo ra** — cả 3 màn CSKH đã
  dính. Lấy ảnh theo `company_id` GHI TRÊN CHỨNG TỪ (bản in danh sách thì lấy công ty người đang
  đăng nhập, xem mục 4b). Ảnh kéo ngang hết bề rộng giấy, giống dải đầu file Excel.
- **Cỡ chữ**: văn bản `13px`, bảng `10px`, tiêu đề `h3 18px`, font `Times New Roman`.
- **Nội dung soạn bằng CKEditor** (điều khoản báo giá) mang theo `font-size` inline, thường 18px,
  in ra to gấp rưỡi phần còn lại → ép về 13px:
  `div[style*="font-size"], span[style*="font-size"], p[style*="font-size"] { font-size: 13px !important }`
- **In**: mở cửa sổ riêng rồi `print()`, KHÔNG `window.print()` trên trang HRM (dính sidebar/topbar).
  Chờ ảnh letterhead `load` xong mới in, kèm lưới an toàn 3 giây.
- `@page`: `A4 portrait` cho chứng từ, `A4 landscape` cho danh sách; lề `12mm 10mm`.
- **Tiêu đề phiếu**: mẫu ERP không dùng `<h1>/<h3>` — tiêu đề là `<strong>` trong ô căn giữa của
  bảng bố cục (`table.no-border`). Không khai riêng thì nó bị rule "ép cỡ chữ" kéo xuống 10px, đọc
  rất bé. Cho `17px`.
- **Bảng bố cục vs bảng dữ liệu**: `table.no-border` là bố cục (thông tin đầu phiếu, chữ ký) → chữ
  13px, không viền; bảng còn lại là dữ liệu → 10px, có viền.
- **Khoảng trắng**: mẫu ERP giãn dòng bằng `<p>` rỗng và `<br><br>` → ẩn `p:empty`, `div:empty`,
  `br + br`; `p { margin: 0 0 2px }`; `line-height: 1.25`.
- **Chỗ ký**: vùng ký của mẫu là 3 dòng *chức danh → dòng chỉ có `&nbsp;` → tên người*. Dòng giữa
  chính là chỗ đặt bút nhưng chỉ cao 1 dòng chữ (~15px), in ra không đủ ký. CSS không chọn được
  phần tử "chỉ chứa khoảng trắng" nên `markSignatureSpace(html)` gắn class `.signature-space` ngay
  khi NHẬN HTML (không đợi Vue render — lúc html vừa về thì `loading` vẫn true, `$refs` chưa có),
  rồi CSS nới lên `56px`. Popup và bản in dùng chung đúng chuỗi HTML đó.
- **Rác của tiện ích trình duyệt**: ẩn `img[src^="chrome-extension"]`, `img[src^="moz-extension"]`,
  `.ddict_btn` — chúng chèn vào DOM và lọt cả vào giấy.

Tự kiểm: mở popup → thấy letterhead trải hết bề ngang, và chạy trong Console
`new Set([...document.querySelectorAll('.report-print-content div,span,p,td,th')].map(e => getComputedStyle(e).fontSize))`
chỉ ra **2 giá trị**: 13px và 10px.
