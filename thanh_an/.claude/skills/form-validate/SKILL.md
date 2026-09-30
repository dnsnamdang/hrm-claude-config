---
name: form-validate
description: Use when làm form nhập liệu ở màn đã/đang lên chuẩn V2 của hrm-thanhan-client (trang add/edit, modal form, nhất là phân hệ Cung ứng) — validate realtime bằng vee-validate trên component V2Base*, gộp lỗi FE + lỗi BE 422 bằng formValidateMixin, dọn lỗi bảng nhiều dòng, cuộn tới ô lỗi đầu tiên. Đọc cả khi: ô báo đỏ mà bấm Lưu vẫn đi, lỗi nhảy sai dòng sau khi xoá dòng, hoặc cần chốt rule nào chặn ở FE / rule nào chặn ở BE
---

# Skill: Validate form ở màn V2 (vee-validate + V2Base*)

Port từ skill `form-validate` của hrm-client, đã sửa cho khớp dns. Áp dụng cho **màn đang chuyển
sang V2** (bắt đầu từ phân hệ Cung ứng). Màn cũ chạy ổn thì không sửa đại trà.

## 0. Khác biệt dns so với hrm — đọc trước

| Mục | hrm | dns |
|---|---|---|
| Mixin gộp lỗi FE + BE | `utils/mixins/formValidateMixin.js` | **Đã port** cùng tên. Khác: cuộn lỗi bằng `scrollToFirstError(this.$el)` và đọc thêm khoá `data.error_messages` |
| Rule vee-validate custom | ~16 rule (`positive_integer`, `greater_than`, `phone`…) | **Chỉ có `max_value`, `money_format`** (`plugins/vee-validate.js`). Rule khác → dùng rule gốc vee-validate 2 (`required`, `max`, `min`, `numeric`, `decimal`, `email`, `min_value`…) hoặc **hỏi trước** khi thêm vào plugin (file dùng chung) |
| Toast | `this.$toasted.global.error({ message })` | Giống — `this.$toasted.global.error / success / warning` |
| Loading | `$safeLoadingStart` | **Không có** → `this.$nuxt?.$loading?.start?.()` + `finish?.()` trong `finally` |
| Hỏi xác nhận | `this.$confirm` | **Không có** → `<BaseConfirmModal id="...">` id riêng (xem skill `modal-popup` §3) |
| Lỗi 422 | `response.data.errors` | 2 kiểu: `response.data.errors` (FormRequest) **và** `response.data.data.error_messages` (controller tự bắt, xem `ApiErrorHandler.js`). Mixin đã đọc cả hai |
| Tên biến lỗi BE | `formErrors` (mixin) / `formError` (màn cũ) | Như hrm. Màn cũ Cung ứng dùng `formError` — khi chuyển sang mixin thì đổi hết sang `formErrors`, đừng để 2 biến song song |
| Cuộn tới lỗi | `scrollToFirstError` | Đã port `utils/scrollToFirstError.js`. **Đừng dùng `scrollToInputError` của `utils/helpers.js`** — nó chỉ bắt `span.text-danger`, không thấy `.v2-error` |
| Dọn lỗi theo dòng | `utils/rowFieldErrors.js` | Đã port, cùng API |
| `FileAttachmentTable.vue` | Có | **Không có** — cần bảng tài liệu thì ghép `V2BaseFile` theo dòng hoặc hỏi trước khi port |
| `.table-responsive { min-height: 50vh }` global | Có → phải ghi đè | dns **không có** rule này; chỉ thêm `.v2-form-table-wrap` nếu đo thấy thừa khoảng trắng |
| Dấu `*` bắt buộc | `V2BaseLabel required` | Form V2: `<V2BaseLabel required>`; form cũ: `<Required />` — **không** viết `*` trần |

---

## 1. Nguyên tắc cốt lõi

1. **Validate realtime ở FE** bằng vee-validate 2 gắn thẳng lên `V2Base*` — user thấy lỗi ngay khi
   giá trị đổi, không đợi bấm Lưu.
2. **`required` do BE quyết** theo trạng thái bản ghi. FE chỉ gắn `required` cho trường đại diện
   (Tên / trường mà màn không thể lưu nếu thiếu, kể cả khi lưu nháp).
   - Màn **có Lưu nháp** (vd Đề xuất cung ứng, Hợp đồng mua): lưu nháp mọi trường khác được trống.
   - Màn **không có nháp**: vẫn để BE trả 422 cho các trường bắt buộc còn lại; FE chỉ thêm
     `required` khi BE cũng bắt và đã khớp câu chữ. Không tự bịa danh sách required ở FE.

| Loại rule | Ai kiểm | Hiện khi nào |
|---|---|---|
| `required` trường Tên/đại diện | FE (`v-validate="'required'"`) | Realtime |
| Định dạng: số, số dương, độ dài, email, khoảng giá trị | FE **và** BE | Realtime + sau khi Lưu |
| `required` các trường còn lại | **BE** | Sau khi Lưu (422) |
| Ràng buộc nghiệp vụ nhiều trường, trùng mã, vượt số lượng còn lại… | **BE** | Sau khi Lưu (422) |

### ⚠️ "Lưu nháp" chỉ nới `required` — mọi rule khác vẫn chặn

| | Lưu nháp | Lưu / Gửi duyệt |
|---|---|---|
| `required` | Nới | BE quyết theo `status` |
| Định dạng (số, số nguyên dương, ngày, độ dài…) | **CHẶN** | **CHẶN** |
| Ràng buộc nghiệp vụ | **CHẶN** | **CHẶN** |

Nháp là bản ghi **chưa đủ**, không phải bản ghi **sai**. Lưu được `quantity = "abc"` thì cái sai đó
nằm trong DB vĩnh viễn.

### ⚠️ Rule định dạng phải có ở CẢ BE

```php
// FormRequest — KHÔNG đi theo biến $required (nháp/chính thức), luôn bật
'products.*.quantity' => 'nullable|numeric|min:0',
```

Message BE viết **y hệt** message FE. Tự kiểm bằng cách gọi thẳng API với payload nháp chứa giá trị
sai → phải ra 422 kèm đúng khoá `products.0.quantity`.

---

## 1b. Màn V2 dùng `V2Base*` cho mọi element — KHÔNG viết HTML thô

`v2ValidateMixin` chỉ nằm trong `V2Base*`. Viết `<input class="form-control">` thì mất validate
realtime, mất `is-invalid`, mất kiểu ô khoá chung.

| Viết thô (SAI) | Dùng component (ĐÚNG) |
|---|---|
| `<input class="form-control">` / `b-form-input` | `V2BaseInput` |
| `<input type="date">` / `date-picker` tự dựng | `V2BaseDatePicker` |
| input tiền tệ tự format | `V2BaseCurrencyInput` |
| `<textarea>` / `b-form-textarea` | `V2BaseTextarea` |
| `<select>` / `base-select2` | `V2BaseSelect` — trong modal: `V2BaseSelectInModal`; danh mục lớn: `V2BaseSelectRemote` |
| checkbox / radio | `V2BaseCheckbox` / `V2BaseRadio` |
| `<input type="file">` tự dựng | `V2BaseFile` (mục 1d) |
| `<label>Tên <span class="text-danger">*</span></label>` / `<Required />` | `<V2BaseLabel required>Tên</V2BaseLabel>` |
| `<button class="btn …">` / `b-button` | `V2BaseButton` (xem skill `button-convention` Phần A) |
| Nút chỉ có icon | `V2BaseIconButton` |
| `<span class="badge">` trạng thái | `V2BaseBadge` |

- `V2BaseLabel` tự render dấu `*` và tự gắn tooltip ⓘ từ `utils/constants/field-hints.js`.
- **Ô chỉ để đọc**: vẫn `V2Base*` + `disabled`, không dùng `<input readonly>` thô.
- ⚠️ `this.$axios.post(...)` tự gọi (upload file…) **không** tự gắn `Authorization` → 401. Dùng action
  trong `store/actions.js` (`apiPostMethod`…) hoặc tự đính
  `Authorization: Bearer ${localStorage.getItem('access_token')}`.

**Tự kiểm** — lệnh này phải KHÔNG ra kết quả:

```bash
grep -rn "<input \|<textarea\|<select \|<button \|<label \|b-form-input\|base-select2\|class=\"btn \|class=\"form-control" \
  pages/supply/<màn>/ | grep -v "V2Base"
```

---

## 1c. Khối nhóm trong form — `V2BaseFormSection`

```vue
<V2BaseFormSection title="Thông tin chung" class="mb-2">
    <template #actions>
        <V2BaseButton secondary size="sm" @click="addRow">Thêm dòng</V2BaseButton>
    </template>
    …nội dung…
</V2BaseFormSection>
```

- Tiêu đề cần markup riêng (badge trạng thái) → slot `#title`.
- Không tự dựng `card` + `card-header` cho từng màn.
- Màn hẹp (<1400px) tiêu đề và cụm nút chen nhau → ghi đè **trong màn** (không sửa component chung):

```scss
@media (max-width: 1400px) {
    ::v-deep .v2-form-section > .card-header { flex-wrap: wrap; gap: 6px 8px; }
    ::v-deep .v2-form-section > .card-header > h6 { flex: 1 1 100%; }
    ::v-deep .v2-form-section > .card-header > .d-flex { flex: 1 1 100%; justify-content: flex-end; }
}
```

- Cột chứa **tên tệp / chuỗi dài không dấu cách** kéo giãn cả bảng → chốt bề rộng ngay trên `<th>`:
  `<th style="width: 230px; min-width: 230px">File đính kèm</th>`.
- Bảng trong form: bóp padding dọc ô cho gọn:

```scss
.v2-form-table th,
.v2-form-table td { padding-top: 4px; padding-bottom: 4px; }
```

---

## 1d. Chọn file — `V2BaseFile`

```vue
<V2BaseFile
    :value="row.attachment"
    :uploading="uploadingIndex === i"
    :disabled="readonly"
    accept=".pdf,.png,.jpg,.jpeg,.doc,.docx,.xls,.xlsx"
    placeholder="Chọn tệp"
    @change="onFileChange($event, row, i)"   <!-- File; null = gỡ file -->
/>
```

- `auto-upload` → component tự đẩy lên S3 qua endpoint dùng chung. Cần thư mục riêng thì tự bắt
  `@change` rồi gọi endpoint của màn (nhớ `Authorization`).
- ⚠️ `.v2-file__input` là `position:absolute; width/height:100%; opacity:0`. Wrapper bọc nó **phải có
  `position: relative; overflow: hidden;`**, nếu không ô trong suốt phủ lan ra và bấm đâu cũng bật hộp
  chọn file.

---

## 2. Gắn validate lên V2Base* — dùng `formValidateMixin`

```js
import formValidateMixin from '@/utils/mixins/formValidateMixin'

export default {
    mixins: [formValidateMixin],
    // …
}
```

Template — viết gọn nhờ `v2ValidateMixin` (đọc tên từ `name`, giá trị từ `currentValue`):

```vue
<V2BaseLabel required>Tên đề xuất</V2BaseLabel>
<V2BaseInput
    v-model="form.name"
    v-validate="'required|max:255'"
    name="name"
    data-vv-as="Tên đề xuất"
    :invalid="hasFieldError('name')"
/>
<V2BaseError :message="fieldError('name')" />
```

- `fieldError(name)` ưu tiên lỗi FE (`errors.first`) rồi tới lỗi BE (`formErrors[name]`).
- `:invalid` bật viền đỏ — vee-validate **không** tự gắn class cho component.
- `name` phải **trùng khoá BE trả về** (`products.0.quantity`…) để 2 nguồn lỗi gộp một chỗ.
- Select/DatePicker chỉ validate khi giá trị đổi (vee-validate không bắt `blur` native bên trong).
- Không có mixin (màn chưa đổi) thì viết dài theo kiểu hrm:
  `data-vv-name` + `data-vv-value-path="currentValue"` + `:invalid="errors.has('x')"` +
  `<V2BaseError :message="errors.first('x') || formError.x" />`.

Khi submit:

```js
async submit(status) {
    // validateForm(): xoá lỗi BE cũ → validateAll → còn lỗi thì toast + cuộn, trả false
    if (!(await this.validateForm())) return
    // form có bảng con tách component → xem mục 3c (vmId: null)

    this.$nuxt?.$loading?.start?.()
    try {
        await this.$store.dispatch('apiPostMethod', { url: 'supply/…', payload: { ...this.form, status } })
        this.$toasted.global.success({ message: 'Lưu thành công' })
    } catch (error) {
        if (!this.applyServerErrors(error, 'Bạn chưa nhập đầy đủ thông tin.')) {
            this.$toasted.global.error({ message: error?.response?.data?.message || 'Có lỗi xảy ra' })
        }
    } finally {
        this.$nuxt?.$loading?.finish?.()
    }
}
```

Mở lại modal / reset form → gọi `resetValidation()` (`<b-modal>` không huỷ component nên ErrorBag
cũ còn nguyên).

---

## 3. Hành vi hiển thị lỗi (UX bắt buộc)

- Lỗi hiện **inline dưới ô** (`V2BaseError`), không dùng popup báo lỗi validate.
- Lỗi BE hiện **đồng thời tất cả** ô sau khi Lưu; tự mất khi ô được sửa (FE) / khi submit lại (BE).
- Còn lỗi FE thì **không gọi API**.
- Có lỗi → **cuộn + focus ô lỗi đầu tiên** (mixin đã làm).
- Câu lỗi tiếng Việt, không thuật ngữ kỹ thuật: `Tên đề xuất không được để trống`.
- ⚠️ **KHÔNG TỰ SỬA GIÁ TRỊ USER NHẬP.** Vượt trần/dưới sàn/sai định dạng → báo đỏ dưới ô, giữ nguyên
  số user gõ. Cấm kéo về max/min, làm tròn, cắt ký tự, tự xoá dòng trống. Toast thay cho lỗi dưới ô
  cũng SAI (bảng dài không biết dòng nào hỏng).

```js
// SAI
onQtyChange(row) { if (row.quantity > row.remain) { row.quantity = row.remain; this.$toasted.global.error({ message: '…' }) } }

// ĐÚNG — gắn lỗi vào đúng ô, chặn ở lúc lưu
onQtyChange(row, index) {
    const key = `products.${index}.quantity`
    const message = Number(row.quantity) > Number(row.remain) ? `Số lượng – Không được vượt ${row.remain} (còn lại)` : ''
    if (message) this.$set(this.formErrors, key, message)
    else this.clearFieldError(key)
}
```

(Nhớ ép `Number()` — cột decimal Eloquent trả về **string**, so sánh/cộng chuỗi sẽ sai.)

### 3a. Mỗi ô một khoá lỗi riêng

Hai ô `v-if`/`v-else` cùng ghi vào một cột DB **không** được dùng chung khoá `formErrors`:
1. Khoá riêng cho từng ô.
2. Đổi điều kiện hiện ô → xoá lỗi cũ của ô vừa ẩn.
3. Lỗi 422 của cột chung → FE tự chuyển sang khoá của ô **đang hiện** trước khi gán vào `formErrors`.

### 3b. Bảng nhiều dòng — dọn lỗi theo chỉ số khi đổi mảng

Laravel trả khoá có chỉ số (`products.2.quantity`). Chỉ số là **vị trí**, không phải danh tính dòng →
xoá/thêm dòng mà không dọn thì lỗi dính sang dòng khác. Dùng `utils/rowFieldErrors.js` **ngay tại chỗ
đổi mảng**:

| Thao tác | Gọi gì |
|---|---|
| Xoá 1 dòng (`splice(i, 1)`) | `this.formErrors = removeRowErrors(this.formErrors, 'products', i)` |
| Thêm dòng cuối (`push`) | `this.formErrors = dropRowErrorsFrom(this.formErrors, 'products', arr.length)` |
| Thay cả mảng (đổi NCC, tải lại phiếu gốc) | `this.formErrors = clearRowErrors(this.formErrors, 'products')` |
| Chuyển dòng sang bảng khác | `removeRowErrors` ở nguồn **+** `dropRowErrorsFrom` ở đích |

- `prefix` là đường dẫn tới **chính mảng**; bảng lồng: `` `products.${pi}.items` ``.
- Có lỗi cấp bảng (`formErrors.products` = "Chưa chọn hàng hoá") thì thêm dòng xong phải xoá khoá đó.
- ⚠️ Không chữa bằng `this.formErrors = {}` — giấu mất lỗi các dòng khác.
- ⚠️ Bảng con không được `splice` thẳng mảng của cha trong template → `$emit` ra cha để cha dọn lỗi.

### 3c. `validateAll()` không thấy ô trong component con

Mỗi field có `vmId` = `_uid` component chứa nó; `validateAll()` chỉ quét field cùng `vmId`. Ô nằm trong
component bảng con → bị bỏ qua → **đỏ mà vẫn lưu được**. `inject: ['$validator']` không cứu được.

```js
const valid = await this.$validator.validateAll(null, { vmId: null })
if (!valid) {
    this.$toasted.global.error({ message: 'Bạn chưa nhập đầy đủ thông tin.' })
    this.$nextTick(() => scrollToFirstError(this.$el))
    return
}
```

(`validateForm()` của mixin gọi `validateAll()` không có `vmId: null` — form có bảng con thì tự gọi như
trên thay vì dùng `validateForm()`.)

- Ở component con: `data-vv-name` **duy nhất theo dòng** (`` `qty-${variant}-${index}` ``).
- Rule chỉ gắn khi ô **có giá trị**, nếu không vừa mở màn đã đỏ:

```js
qtyRule(value) { return value === '' || value === null || value === undefined ? '' : 'decimal|min_value:0' }
```

### 3d. Bảng dài — bấm Lưu phải nhảy tới đúng dòng lỗi

Toast giữ câu chung `"Bạn chưa nhập đầy đủ thông tin."`, việc bắt buộc là **tự cuộn**:
`scrollToFirstError(this.$el)` (mixin đã gọi sẵn). Util tìm ô lỗi đầu tiên (`.v2-input__wrapper.is-invalid`
→ `.is-invalid` → câu lỗi đang hiện có chữ), cuộn cả `<tr>` vào giữa, kéo ngang nếu bảng tràn, nháy nền
dòng ~1,5s và focus ô. **Đừng tự viết đoạn cuộn tay** bằng selector riêng.

---

## 4. Rule vee-validate dùng được ở dns

- Custom (`plugins/vee-validate.js`): `max_value`, `money_format`.
- Rule gốc vee-validate 2: `required`, `max`, `min`, `numeric`, `decimal`, `integer`, `min_value`,
  `max_value`, `email`, `between`, `regex`, `date_format`, `after`, `before`…
- Cần rule hrm (`positive_integer`, `greater_than`, `date_greater_than`…) → **hỏi user trước** khi thêm
  vào plugin (file dùng chung).

---

## Checklist

- [ ] `mixins: [formValidateMixin]`; ô dùng `name` + `:invalid="hasFieldError(..)"` + `V2BaseError :message="fieldError(..)"`
- [ ] Chỉ trường Tên/đại diện có `required` ở FE; required khác để BE trả 422
- [ ] Rule định dạng gắn FE, chạy realtime, chặn cả nút Lưu nháp; BE có rule tương ứng, message giống
- [ ] Không HTML thô (lệnh grep mục 1b không ra kết quả); nhãn bắt buộc dùng `V2BaseLabel required`
- [ ] Không đoạn nào tự sửa giá trị user nhập (grep `Math.min(`, `Math.max(`, `= max` trong `onXxxChange`)
- [ ] Lỗi 422 qua `applyServerErrors` (đọc cả `errors` lẫn `data.error_messages`)
- [ ] Bảng nhiều dòng: mọi chỗ xoá/thêm/thay mảng đã dọn lỗi bằng `rowFieldErrors.js`
- [ ] Form có bảng con: `validateAll(null, { vmId: null })`, `data-vv-name` duy nhất theo dòng
- [ ] Có lỗi → cuộn tới ô lỗi đầu tiên (`scrollToFirstError(this.$el)`)
- [ ] Mở lại modal/reset form → `resetValidation()`
- [ ] Loading: `$nuxt.$loading.start/finish` trong `try/finally`
