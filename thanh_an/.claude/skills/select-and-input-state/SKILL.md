---
name: select-and-input-state
description: Use when làm việc với select / ô nhập liệu ở màn V2 của hrm-thanhan-client (form, modal, chi tiết, bộ lọc — không riêng màn danh sách). Bắt buộc đọc khi — select danh mục MẤT giá trị đã chọn sau khi danh mục bị khoá/ngừng hoạt động; cần 🔒 cho option đã khoá; ô disabled sai màu hoặc vẫn bấm được; chip select chọn nhiều sai khuôn hoặc mất lựa chọn khi tích cái thứ hai; viền xanh khi focus; nhãn option nhân viên lệch khuôn; FE dùng trường/endpoint mới mà BE chưa deploy kịp
---

# Select & trạng thái ô nhập liệu (màn V2)

Port từ skill cùng tên của hrm-client, đã sửa cho khớp dns. Skill liên quan: `modal-popup` (select
trong modal dùng `V2BaseSelectInModal`), `form-validate`, `list-page`, `button-convention`.

## 0. Khác biệt dns so với hrm — đọc trước

| Mục | dns hiện có |
|---|---|
| `utils/select2LockedOption.js` (🔒 + lọc option khoá không dùng) | **Có**, `V2BaseSelect` + `V2BaseSelectInModal` gọi sẵn |
| `allowClear` mặc định `true`, prop `keep-locked-options` | **Có** ở `V2BaseSelect`, `V2BaseSelectInModal`, `V2BaseSelectRemote` (allowClear) |
| `utils/select2DropdownSearch.js`, `utils/select2-focus-search.js` | **Có** |
| `utils/employeeOptionText.js` | **Có** file, nhưng **chưa màn/store nào dùng** |
| Ô khoá `#f1f5f9`/`#475569`, focus không viền xanh | **Có** trong `assets/scss/v2-styles.scss` (chỉ ăn khi màn import file này — xem `list-page` A2) |
| BE `include_ids` + `is_locked` | **CHƯA có endpoint nào** — thêm theo từng màn khi cần (mục 1) |
| Helper PHP `employeeOptionLabel()` | **Không có** |
| `projectPhaseOptionsMixin`, `DescriptionInfoSelect.vue` | **Không có** (bỏ qua phần đó của hrm) |
| Rule vee-validate số | Chỉ `max_value`, `money_format` custom + rule gốc (`numeric`, `decimal`, `integer`, `min_value`) — không có `positive_integer` |
| Plugin `v-select2` / directive `select2-focus` cũ | Là bản dns, **chưa** cập nhật theo hrm (sửa = hàm dùng chung → hỏi) |

---

## 1. Danh mục bị KHOÁ trong select

Dropdown chỉ liệt kê danh mục **còn hoạt động**, NHƯNG giá trị bản ghi đang chọn thì **vẫn phải hiện**
dù danh mục đó đã khoá — không thì mở màn Sửa thấy ô trống, lưu lại là **mất dữ liệu**
(vd nhà cung cấp đã ngừng giao dịch trên đơn mua cũ).

Ba điều chốt:
1. 🔒 hiện ở cả **dropdown** lẫn **giá trị đang hiển thị / chip**.
2. Danh mục khoá **chỉ hiện ở bản ghi đang dùng nó** — đổi sang giá trị khác là option khoá cũ biến mất
   ngay (component đã lo qua `filterUnusedLockedOptions`).
3. **Store dùng chung KHÔNG cache danh mục đã khoá** — màn tự giữ.

### BE — 2 việc (thêm vào service của danh mục, không phải hàm dùng chung)

```php
// Controller: chuẩn hoá include_ids (nhận cả "1,2" lẫn mảng)
$includeIds = $request->input('include_ids', []);
if (!is_array($includeIds)) $includeIds = explode(',', (string) $includeIds);
$includeIds = array_values(array_filter(array_map('intval', $includeIds)));

// Service: còn hoạt động HOẶC đang được chọn
$query->where(function ($q) use ($includeIds) {
    $q->where('status', 1);
    if (count($includeIds)) $q->orWhereIn('id', $includeIds);
});

// Trả kèm cờ, GIỮ NGUYÊN tên
return ['id' => $x->id, 'name' => $x->name, 'is_locked' => (int) $x->status !== 1];
```

⚠️ Endpoint danh mục đang được nhiều màn gọi → thêm tham số `include_ids` là **tương thích ngược**
(không truyền thì như cũ), nhưng vẫn báo user trước khi sửa service dùng chung.

### FE — 2 việc, KHÔNG phải khai gì để hiện 🔒

1. Gọi API danh mục kèm `include_ids` = id đang chọn.
2. Nạp **lại** danh mục **sau khi có dữ liệu bản ghi** (lượt gọi ở `mounted` chưa biết id):

```js
async loadDetail() {
    // …gán this.form
    if (this.form.supplier_id) await this.loadSuppliers([this.form.supplier_id])
},
```

Dữ liệu đổ vào qua prop (không có `loadDetail`) → watcher bắt lượt load đầu:

```js
'form.supplier_id'(newId, oldId) {
    if (!newId || oldId) return
    if (!this.suppliers.some((s) => s.id == newId)) this.loadSuppliers([newId])
}
```

⚠️ Đừng:
- Nối `"(đã khoá)"` / `"🔒 "` vào `name` — chip dính theo, hỏng tìm kiếm.
- Tự viết `templateResult` ở từng màn — component đã có. Wrapper nào **tự khai `templateResult`** thì
  helper nhường quyền → wrapper đó **phải tự gắn** `LOCKED_OPTION_PREFIX` (import từ
  `@/utils/select2LockedOption`) ở cả `templateResult` lẫn `templateSelection`.
- Merge danh mục khoá vào Vuex — sẽ nằm lại cả phiên, bản ghi khác cũng thấy.

---

## 1b. Nút × xoá nhanh — MẶC ĐỊNH BẬT

`V2BaseSelect` / `V2BaseSelectInModal` / `V2BaseSelectRemote` để `allowClear: true` sẵn. **Đừng khai
`:allowClear="false"`** cho trường nghiệp vụ — kể cả trường bắt buộc (bắt buộc là việc của validate).

- `allowClear` cần `placeholder` (select2 chỉ vẽ × khi có placeholder) → `placeholder="Chọn <tên trường>"`.
- Ngoại lệ được tắt ×: ô **Trạng thái** (Hoạt động/Khoá) của modal danh mục; ô lọc **bắt buộc** của
  màn báo cáo. Tắt ở chỗ khác → **ghi lý do cạnh dòng code**.
- Ô disabled không hiện × — đã ẩn sẵn trong `V2BaseSelect.vue`.

Khác màn **cũ** (Phần B skill `list-page`): `base-select2` cũ dùng `allowClear` + giá trị rỗng `null`.

---

## 2. Chip của select chọn nhiều

Một khuôn duy nhất (đã set sẵn trong `V2BaseSelect.vue`, `V2BaseSelectInModal` ăn theo class `.v2-select`):

| Thuộc tính | Giá trị |
|---|---|
| Nền / viền / chữ | `#eff6ff` / `#bfdbfe` / `#1e40af` |
| Bo góc | `5px` (không pill) |
| Chữ | `11px`, `500`, `line-height 18px` |
| Padding | `1px 7px` — mọi `size` |
| Hover | nền `#dbeafe`, viền `#93c5fd` |
| Nút × trên chip | đứng SAU chữ, `13px`, `opacity .6`; hover `opacity 1` + `#dc3545` |

Không khai lại `font-size`/`padding` cho `.select2-selection__choice` ở màn hay biến thể mới.

## 2b. Select chọn NHIỀU mất sạch lựa chọn khi tích cái thứ hai

`visibleOptions` lọc option khoá **dựa trên giá trị đang chọn** → mỗi lần tích thêm, options thành mảng
mới → select2 dựng lại → mất lựa chọn.

Cách xử lý: danh mục **không thể chứa bản ghi khoá** (BE đã lọc `status = 1`) → truyền `keep-locked-options`:

```vue
<V2BaseSelectInModal
    v-model="row.ids"
    :options="row.options || []"
    :extraSettings="{ multiple: true }"
    keep-locked-options
/>
```

- Chọn nhiều khai qua **`extraSettings: { multiple: true }`**, không phải attribute `multiple` trần
  (bộ lọc `V2BaseSmartFilterPanel` thì dùng `multiple: true` trong schema field).
- Options gắn **thẳng vào dữ liệu** (`row.options`, computed), không gọi hàm trả mảng mới trong template.
- Test bằng script: select2 chọn-nhiều liệt kê cả option đã chọn, click lại là **bỏ chọn** → chọn theo
  **tên**, đừng click `nth=0` hai lần.

## 2c. Nhãn option NHÂN VIÊN

Mọi select chọn nhân viên ở màn V2 hiển thị một khuôn:

```
Tên nhân viên - Mã phòng - Mã nhân viên
Nguyễn Thị Cần - HN_KD1 - 11010057
```

Thiếu phần nào bỏ phần đó, không để `-` thừa.

1. **Không tự ghép chuỗi** — dùng `employeeOptionText(employee)` từ `@/utils/employeeOptionText`.
2. Store dns **chưa** áp helper này → ở màn V2 tự map khi dựng options:
   `options = list.map((e) => ({ id: e.id, text: employeeOptionText(e) }))`.
   Đổi thẳng getter trong store = sửa hàm dùng chung → **hỏi trước**.
3. API mới trả nhân viên phải có `fullname`, `code`/`employee_code`, `department_code`.

- `state.employees[].name` có thể là chuỗi BE ghép sẵn `"MÃ_PHÒNG - Tên"` — helper tự cắt, cứ truyền cả object.
- **Không đổi `name` mà BE trả cho bảng** — bảng có cột Mã/Phòng riêng; cần nhãn ghép thì thêm field mới.
- Người đã nghỉ việc không còn trong danh sách → giữ fallback tên BE trả (đúng tinh thần mục 1).

Tự kiểm (trong phạm vi màn đang làm, phải rỗng):

```bash
grep -rnE "(text|label|name): *[a-zA-Z_]+\.(fullname|name)\b|\.code \+ '[-_ ]+' \+|\.fullname \+ '[-_ ]+' \+" \
  pages/supply/<màn> | grep -v '{{'
```

---

## 3. Ô nhập bị KHOÁ (disabled / readonly) — một kiểu duy nhất

| Thuộc tính | Giá trị |
|---|---|
| Nền | `#f1f5f9` |
| Chữ | `#475569` |
| Viền | `#e2e8f0` |
| Con trỏ | `not-allowed` |
| `opacity` | **1** — không làm mờ |

Rule chung ở `assets/scss/v2-styles.scss` (import **không scoped** ở màn V2). Component mới có trạng thái
khoá: **không tự đặt màu**, chỉ khai `cursor`.

Chip trong ô khoá: nền `#e2e8f0`, chữ `#475569`, viền `#cbd5e1`, ẩn ×; phủ cả thẻ con trong chip.

⚠️ Bẫy:
- `opacity` làm khó đọc ở màn chi tiết → dùng màu chữ, không dùng opacity.
- Selector nặng ký đè rule chung (vd `… .select2-selection--multiple { background:#fff !important }`)
  → thêm `:not(.select2-container--disabled)`. Tìm rule đè: duyệt `document.styleSheets`, lọc
  `el.matches(r.selectorText)`.
- Ô tự dựng bằng `<div>` **phải tự chặn thao tác** ở đầu mọi handler (`if (this.disabled) return`) —
  CSS chỉ đổi con trỏ.

## 4. Focus ô nhập

Click vào ô: **không** viền xanh, **không** quầng sáng — chỉ đậm viền xám `#94a3b8`. Đã xử lý trong
`V2BaseInput`, `V2BaseTextarea`, `V2BaseDatePicker`, `V2BaseSelect`, `V2BaseSelectInModal`,
`V2BaseSmartFilterPanel` và rule chung trong `v2-styles.scss`. Component mới: **cấm**
`border-color: #16a34a` / `box-shadow` xanh trong `:focus`.

Nút × trong ô lọc/select: hover **không tô nền**, chỉ đổi × sang đỏ `#dc2626`.

## 4b. Ô chỉ cho SỐ — dùng rule, đừng tự lọc ký tự

Dùng `v-validate` + `V2BaseError` (xem `form-validate`). Rule có ở dns: `numeric` (số nguyên ≥ 0),
`integer`, `decimal:<n>`, `min_value:0`, `max_value`, `money_format`. Tiền tệ → `V2BaseCurrencyInput`.

```js
// KHÔNG: lọc rồi ghi ngược lại — dữ liệu sạch nhưng MÀN HÌNH vẫn hiện chữ
setQty(row, value) { this.$set(row, 'quantity', String(value).replace(/\D/g, '')) }
```

Gõ `1` rồi `a` → chuỗi lọc vẫn `"1"` → prop không đổi → Vue không render lại → `a` vẫn nằm trên ô.
Chỉ lộ khi **gõ tuần tự** (`pressSequentially('1abc2')`), dán cả chuỗi thì trông như đúng.

Rule định dạng chặn cả **Lưu nháp** và phải có rule tương ứng ở BE (`form-validate` mục 1).

---

## 5. FE mới + BE cũ — luôn có đường lùi

FE và BE không phải lúc nào cũng deploy cùng lúc. Code FE dùng trường/endpoint mới phải chạy được khi
BE chưa cập nhật:

- **Trường mới**: chuỗi lùi dần (`actor_id` → `actor_code` → `actor_name`).
- **Endpoint mới**: `catch` rồi fallback về cách cũ; fallback **không** được dùng trường mới.
- `include_ids` (mục 1): BE cũ bỏ qua tham số thừa, FE không vỡ, nhưng option khoá vẫn mất → BE phải đi
  trước hoặc deploy cùng lượt.

Verify bằng cách giả lập BE cũ trên trình duyệt: xoá trường mới khỏi dữ liệu rồi xem màn còn chạy.

## 6. Select chọn NHIỀU có 2 ô tìm — focus ô TRONG DROPDOWN

Dự án bật ô tìm trong dropdown cho select nhiều (`select2DropdownSearch.js`) → khi mở có **2 ô**
`.select2-search__field`; ô inline đứng trước trong DOM. `utils/select2-focus-search.js` đã ưu tiên ô
trong dropdown; `V2BaseSelectInModal`, `V2BaseSelectRemote` gọi sẵn. Tự kiểm trong Console (phải `true`):

```js
document.activeElement === document.querySelector('.select2-dropdown .select2-search__field')
```

---

## Tự kiểm trước khi báo xong

- [ ] Màn Sửa: khoá danh mục đang chọn → mở lại, giá trị vẫn hiện đúng tên, có 🔒; lưu lại không mất dữ liệu
- [ ] Đổi sang giá trị khác → option khoá cũ biến mất
- [ ] Đã gọi lại API danh mục **sau khi** có dữ liệu bản ghi
- [ ] Select chọn 1 có × (trừ ngoại lệ mục 1b, có ghi lý do)
- [ ] Select chọn nhiều tích 2–3 mục không mất lựa chọn
- [ ] Nhãn nhân viên đúng khuôn `Tên - Mã phòng - Mã NV` qua `employeeOptionText`
- [ ] Ô disabled: `#f1f5f9`/`#475569`, không opacity, không bấm được (kể cả ô `<div>`)
- [ ] Focus: không viền xanh, không quầng sáng
- [ ] Ô số: gõ tuần tự chữ → báo đỏ; Lưu nháp vẫn bị chặn; BE trả 422
