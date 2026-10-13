# P8-D0 — Vá 2 lỗi có sẵn của component dùng chung (hrm-client)

Nhánh: `gop_db` (đã kiểm `git branch --show-current` = `gop_db`).
Không commit/push/stash. Không đụng `hrm-api`. Không mở Playwright/browser.

## Lỗi 1 — `V2BaseModal` thiếu computed `subtitleFullText` → mất tooltip

### Nguyên nhân gốc
`components/modal/V2BaseModal.vue` dòng 69 (template) dùng `:title="subtitleFullText"` nhưng
component chỉ khai 2 prop `subtitle` / `subtitleLabel`, không có computed hay data nào tên
`subtitleFullText`. Vue render ra `undefined` cho property này → cảnh báo
`[Vue warn] Property or method "subtitleFullText" is not defined` mỗi lần render, và attribute
`title` trên dòng mô tả bản ghi bị mất (hoặc ra chuỗi `"undefined"` tuỳ build).

Đọc kỹ template dòng 66-74 để chốt đúng định dạng chuỗi cần trả:
```html
<div
    v-if="subtitle"
    class="mt-1 v2-modal-subtitle"
    :title="subtitleFullText"
    style="font-size: 11px; color: #6b7280"
>
    <template v-if="subtitleLabel">{{ subtitleLabel }}: </template>
    <span style="color: #374151">{{ subtitle }}</span>
</div>
```
Text hiển thị thực tế trên DOM: có `subtitleLabel` → `"<subtitleLabel>: <subtitle>"` (dấu `: ` sau
label); không có → chỉ `"<subtitle>"`.

### Trước
```js
computed: {
    bodyStyle() {
        return { maxHeight: this.maxBodyHeight }
    },
},
```

### Sau
```js
computed: {
    bodyStyle() {
        return { maxHeight: this.maxBodyHeight }
    },
    // Khôi phục `title` cho dòng mô tả bản ghi (tooltip khi tên bị cắt bởi ellipsis —
    // Redmine #11164). Phải khớp CHÍNH XÁC cách template dòng ~67-74 render:
    // có `subtitleLabel` thì "<subtitleLabel>: <subtitle>", không có thì chỉ "<subtitle>".
    subtitleFullText() {
        return this.subtitleLabel ? `${this.subtitleLabel}: ${this.subtitle}` : this.subtitle
    },
},
```

File: `components/modal/V2BaseModal.vue`, computed thêm ngay sau `bodyStyle()` (khoảng dòng 128-134
sau khi sửa). Không đổi prop, không đổi template, không đổi cấu trúc — chỉ thêm 1 computed.

### Kiểm chỗ dùng khác
`grep -rn "subtitleFullText" components pages` → **chỉ 1 kết quả**, đúng dòng 69 của chính file này.
Không nơi nào khác mong đợi định dạng khác → an toàn khi thêm computed này.

---

## Lỗi 2 — `.v2-error` ra màu đen thay vì đỏ

### Kết quả điều tra: KHÔNG tìm thấy rule nào đang đè màu trong code/bundle hiện tại — DỪNG lại, chưa sửa

Đã làm rất kỹ theo đúng yêu cầu (tìm thủ phạm bằng file:dòng) nhưng **không tìm ra** rule nào override
`color` của `.v2-error__icon` / `.v2-error__text`, cụ thể đã kiểm:

1. **Định nghĩa duy nhất của các class này trong toàn bộ source** (`grep -rn "\.v2-error\s*{\|\.v2-error__text\s*{" --include=*.vue --include=*.scss --include=*.css .` loại trừ `node_modules`, `.worktrees`) → chỉ có đúng 1 nơi: `components/V2BaseError.vue` dòng 62 (`.v2-error`), 79 (`.v2-error__text`), 95/107/119/131 (size variant, chỉ đổi `font-size`, không đụng `color`). Không có file nào khác định nghĩa lại 2 class này.
2. **Kiểm byte-level dòng 72-84 của V2BaseError.vue** (`xxd`) — `color: #dc3545;` là ASCII sạch, không có ký tự ẩn/unicode lạ làm hỏng parse CSS.
3. **`git status` / `git diff HEAD` trên file này → rỗng** — file đang chạy trên dev server đúng là bản đã commit (`6b68bbf40`), không phải bản chỉnh tay chưa lưu.
4. **Kiểm CSS thực tế đang được SERVE bởi dev server đang chạy** (`127.0.0.1:3000`, xác nhận đang LISTEN): tải `/_nuxt/app.js`, `/_nuxt/vendors/app.js`, `/_nuxt/commons/app.js` rồi grep toàn bộ nội dung cho `v2-error`:
   - `vendors/app.js` và `commons/app.js`: **0 kết quả** (không có thư viện/vendor nào định nghĩa lại class này).
   - `app.js`: đúng 4 rule duy nhất liên quan màu, **tất cả đều `color: #dc3545`**, không có rule nào khác:
     ```
     .v2-error__icon[data-v-764def10] { color: #dc3545; ... }
     .v2-error__icon { color: #dc3545; ... }              (bản không scoped, trùng nội dung)
     .v2-error__text[data-v-764def10] { color: #dc3545; ... }
     .v2-error__text { color: #dc3545; ... }               (bản không scoped, trùng nội dung)
     ```
   - Không có `!important` nào gắn với các class này ở bất kỳ đâu trong bundle.
5. Kiểm 2 màn cụ thể được báo lỗi:
   - `pages/meeting/rooms/components/MeetingRoomModal.vue`: **không có `<style>` tag nào cả** (không thể tự đè màu).
   - `pages/meeting/room-amenities/components/RoomAmenityModal.vue`: có `<style lang="scss" scoped>` nhưng chỉ 1 rule `.room-amenity-icon-preview { color: #1abc9c; ... }`, không liên quan `.v2-error`.
   - Cả 2 đều dựng trên `V2BaseModal` (`components/modal/V2BaseModal.vue`) — đã đọc lại toàn bộ style block của nó (dòng 151-230), không có rule nào set `color` cho nội dung slot.
6. Đối chiếu với biến `$body-color: #111` (`assets/scss/config/default/_variables.scss:308`) — đúng bằng `rgb(17,17,17)` mà người điều phối đo được. Đây là màu chữ MẶC ĐỊNH của `<body>` (Bootstrap reboot), chỉ áp dụng khi **không có rule nào khác set `color`** cho phần tử đó (hoặc phần tử cha gần nhất có set). Nhưng theo (1)-(5), `.v2-error__text`/`.v2-error__icon` **đang có** rule set màu đỏ, không xung đột với rule nào khác trong toàn bộ bundle đang chạy.

### Đánh giá & đề xuất
Với dữ liệu tĩnh (source + bundle JS đang chạy thật trên server), tôi **không dựng lại được** hiện
tượng "đen" — mọi bằng chứng cho thấy `color:#dc3545` đang là rule DUY NHẤT áp cho 2 class này, không
bị đè. Đây khớp với gotcha đã có trong bộ nhớ dự án: *"Nuxt stale components manifest sau đổi
branch"* — dev server/browser có thể đang giữ state CSS cũ (HMR không refresh hết, hoặc trang đo lúc
đó chưa load lại sau 1 thay đổi khác) khiến phép đo lệch với source hiện tại.

**Đề xuất, KHÔNG tự ý sửa liều:**
- Hard refresh (hoặc mở tab mới hẳn) trên `http://127.0.0.1:3000/meeting/rooms` và
  `/meeting/room-amenities`, trigger lỗi validate lại, đo `getComputedStyle` một lần nữa trên đúng
  phần tử `span.v2-error__text` (không phải `div.v2-error` cha — div cha KHÔNG tự set `color`, chỉ
  span/icon con mới có, nên nếu lỡ đo nhầm phần tử cha sẽ luôn ra màu kế thừa của `<body>` dù text
  con vẫn đỏ đúng).
- Nếu đo lại vẫn ra đen sau hard refresh → rất có thể do 1 rule được inject **runtime** (không nằm
  trong 3 bundle tôi đã tải) — cần lấy đúng `computedStyleMap()`/`getMatchedCSSRules`-style debug từ
  DevTools (Styles panel, mục "chỗ nào áp / bị gạch ngang") để bắt được rule thật đang thắng, vì grep
  tĩnh đã hết cửa.
- Nếu confirm lại vẫn đen → báo tôi tiếp, kèm ảnh DevTools Styles panel của đúng phần tử đó, tôi sẽ
  sửa theo đúng rule được chỉ ra (không đoán / không rải `!important`).

**Chưa sửa gì cho lỗi 2** theo đúng yêu cầu "không sửa được mà không ảnh hưởng diện rộng thì DỪNG" —
ở đây tình huống còn nghiêm trọng hơn: không tìm ra được rule để sửa, nên không có gì để sửa mà
không phải đoán mò.

---

## Compile kiểm template (vue-template-compiler, resolve từ `node_modules` của hrm-client)

```
=== components/modal/V2BaseModal.vue ===
errors: []
tips: []
=== components/V2BaseError.vue ===
errors: []
tips: []
```
(V2BaseError.vue không sửa gì — compile chỉ để xác nhận không phạm gì khi đọc/đối chiếu.)

## Việc người điều phối cần đo lại trên trình duyệt

**Lỗi 1 (đã sửa, cần xác nhận):**
1. Mở bất kỳ popup nào dùng `V2BaseModal` có truyền `subtitle` (vd modal Sửa/Chi tiết của
   `pages/meeting/rooms` hoặc `pages/meeting/room-amenities` nếu có truyền, hoặc bất kỳ modal nào
   khác đang set `subtitle`/`subtitleLabel` — cần tìm 1 màn thực sự có dòng mô tả hiện ra).
2. Mở Console — xác nhận **KHÔNG còn** dòng `[Vue warn] Property or method "subtitleFullText" is not defined`.
3. Hover vào dòng mô tả (class `.v2-modal-subtitle`) — trình duyệt phải hiện tooltip native đúng
   nội dung `"<subtitleLabel>: <subtitle>"` (hoặc chỉ `<subtitle>` nếu không có label). Có thể đo
   bằng `document.querySelector('.v2-modal-subtitle').title` trong Console để chắc chắn không phải
   chuỗi `"undefined"`.
4. Test cả 2 trường hợp: modal có `subtitleLabel` và modal không có `subtitleLabel` (chỉ `subtitle`),
   để chắc computed nhánh nào cũng đúng.

**Lỗi 2 (CHƯA sửa, cần điều tra thêm bằng DevTools thật):**
1. Vào `/meeting/rooms` → mở modal Thêm mới → bấm Lưu để trigger lỗi validate (trường Tên bỏ trống).
2. DevTools → chọn đúng phần tử `span.v2-error__text` (không phải `div.v2-error` cha) → tab
   Computed/Styles → xem `color` đang ra gì, và quan trọng nhất: xem trong Styles panel **rule nào
   đang match** (kể cả bị gạch ngang do specificity thua) — đây là thứ grep tĩnh không thấy được vì
   có thể là rule inject runtime ngoài 3 bundle tôi đã kiểm.
3. Lặp lại y hệt ở `/meeting/room-amenities`.
4. Nếu Styles panel chỉ ra đúng 1 rule `color:#dc3545` và không có rule nào khác match/đè → nghĩa là
   lần đo trước bị stale (cần hard refresh) và không có bug thật để sửa.
5. Nếu Styles panel chỉ ra rule khác đang thắng → chụp lại đúng rule đó (file/selector DevTools hiện
   ra) gửi tôi để sửa đúng chỗ, không đoán.

## File đã sửa
- `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-client/components/modal/V2BaseModal.vue`
  (thêm computed `subtitleFullText`)

## File đã đọc, KHÔNG sửa
- `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-client/components/V2BaseError.vue`
