---
name: form-validate
description: Use when làm form nhập liệu ở màn MỚI của hrm-client (add/edit page, modal form) — validate realtime bằng vee-validate trên component V2Base*, và quy tắc chỉ trường Tên mới required ở FE. Đọc cả khi: Lưu nháp lọt dữ liệu sai định dạng, ô nhập báo lỗi đỏ nhưng bấm Lưu vẫn đi, hoặc cần chốt rule nào chặn ở FE / rule nào phải chặn thêm ở BE
---

# Skill: Validate Form ở màn mới (vee-validate + V2Base*)

Áp dụng cho **màn mới** của `hrm-client`. Màn cũ đang chạy ổn thì không sửa đại trà.

---

## 1. Hai nguyên tắc cốt lõi

1. **Validate realtime ở FE** bằng `vee-validate` (v2, đã cài sẵn) gắn trực tiếp lên component `V2Base*` — user thấy lỗi ngay khi nhập/rời trường, không phải bấm Lưu mới biết.
2. **KHÔNG gắn `required` ở FE cho bất kỳ trường nào, TRỪ trường Tên.**
   Lý do nghiệp vụ: hệ thống cho **Lưu nháp** — lúc lưu nháp mọi trường đều được bỏ trống, chỉ Tên là bắt buộc. Các trường bắt buộc khác chỉ áp dụng khi lưu chính thức và **do BE quyết định** (trả 422) → FE map vào `formError` và hiển thị.

Hệ quả:

| Loại rule | Ai kiểm | Hiện khi nào |
|---|---|---|
| `required` trường **Tên** | FE (`v-validate="'required'"`) | Realtime (blur/nhập) |
| Định dạng: email, số, số dương, ngày, độ dài, `greater_than`… | FE (`v-validate`) | Realtime |
| `required` các trường còn lại | **BE** theo `status` (nháp/chính thức) | Sau khi bấm Lưu, từ response 422 |
| Ràng buộc nghiệp vụ nhiều trường, trùng mã… | **BE** | Sau khi bấm Lưu |

Tuyệt đối **không** tự bịa danh sách required ở FE cho nút Lưu chính thức — sẽ lệch với BE và chặn oan.

### ⚠️ "Lưu nháp" chỉ nới `required` — MỌI rule khác vẫn chặn (chốt 2026-08-28)

Đây là chỗ hay hiểu sai thành "nháp thì lưu bừa cũng được". Không phải:

| | Lưu nháp | Lưu / Gửi chính thức |
|---|---|---|
| `required` | Nới — chỉ cần 1 trường đại diện (Tên/mã phiếu gốc) | BE quyết theo `status` |
| **Định dạng** (số, số nguyên dương, ngày, email, độ dài, khoảng giá trị) | **CHẶN** | **CHẶN** |
| Ràng buộc nghiệp vụ (trùng mã, ngày sau > ngày trước…) | **CHẶN** | **CHẶN** |

Lý do: nháp là bản ghi CHƯA ĐỦ, không phải bản ghi SAI. `time_to_has = "xyzabc"` lưu được thì cái
sai đó nằm trong DB vĩnh viễn, không ai dọn (Redmine #11240 — đã lọt thật, phải đi `UPDATE` tay).

### ⚠️ Rule định dạng phải chặn ở CẢ BE, không chỉ FE

FE chỉ là lớp trải nghiệm. Cùng một rule phải có ở 2 nơi:

```php
// FormRequest — KHÔNG đi theo biến $required (nháp/chính thức), luôn bật
$key . '.*.choose_services.*.time_to_has' => 'nullable|integer|min:0',
```

Và **message BE viết y hệt message rule FE** ("Giá trị phải là số nguyên dương.") để người dùng
không thấy 2 câu chữ khác nhau cho cùng một lỗi.

Tự kiểm BE bằng cách gọi thẳng API, bỏ qua giao diện:

```js
const payload = form.buildPayload(1)                       // 1 = trạng thái NHÁP
payload.product_repairs[0].choose_services[0].time_to_has = 'abc'
await form.$store.dispatch('apiPutMethod', { url: '…/10321', payload })
// PHẢI ra 422 kèm errors['product_repairs.0.choose_services.0.time_to_has']
```

---

## 1b. MÀN MỚI: DÙNG `V2Base*` CHO MỌI ELEMENT — KHÔNG viết HTML thô

Điều kiện cần để mục 2 chạy được: rule `vee-validate` gắn qua mixin `v2ValidateMixin` nằm **trong
chính các component `V2Base*`**. Viết `<input class="form-control">` thô thì không có mixin đó,
validate realtime không chạy, và ô khoá cũng không ăn kiểu dùng chung.

**Bảng tra — thấy vế trái là phải đổi sang vế phải:**

| Viết thô (SAI) | Dùng component (ĐÚNG) |
|---|---|
| `<input type="text" class="form-control">` | `V2BaseInput` |
| `<input type="date">` / datepicker tự dựng | `V2BaseDatePicker` |
| `<input>` tiền tệ + tự format nghìn | `V2BaseCurrencyInput` |
| `<textarea class="form-control">` | `V2BaseTextarea` |
| `<select class="form-control">` | `V2BaseSelect` — trong modal/popup: `V2BaseSelectInModal`; danh mục lớn: `V2BaseSelectRemote` |
| `<input type="checkbox">` / `<input type="radio">` | `V2BaseCheckbox` / `V2BaseRadio` |
| `<input type="file">` + `<label class="btn">` tự dựng | **`V2BaseFile`** — xem mục 1d |
| `<label class="v2-label">Tên <span class="text-danger">*</span></label>` | `<V2BaseLabel required>Tên</V2BaseLabel>` |
| `<button class="btn btn-primary">` | `V2BaseButton` |
| Nút chỉ có icon | `V2BaseIconButton` |
| `<span class="badge">` trạng thái | `V2BaseBadge` (xem `list-page` mục 3c) |

Vì sao bắt buộc, không phải "cho đẹp":

- **Validate**: `v2ValidateMixin` chỉ có trong `V2Base*` — HTML thô mất realtime + mất `is-invalid`.
- **Ô khoá 1 kiểu duy nhất**: nền `#f1f5f9`, chữ `#475569`, không mờ — rule chung nhắm vào
  `.v2-input:disabled` / `.v2-textarea:disabled`… (skill `select-and-input-state` mục 3).
  Ô thô sẽ ra màu khác trên cùng một form.
- **`V2BaseLabel`** tự render dấu `*` và tự gắn icon ⓘ tooltip từ từ điển `field-hints` — tự viết
  `<label>` là mất tooltip mà không ai biết.
- Sửa 1 chỗ ăn toàn hệ thống; mỗi màn tự dựng thì cỡ chữ / bo góc / khoảng cách lệch nhau.

**Ô chỉ để ĐỌC** (giá trị chọn qua popup, dữ liệu BE trả về): vẫn dùng `V2Base*` + `disabled`,
KHÔNG dùng `<input readonly>` thô.

⚠️ **`$axios` không tự gắn `Authorization`.** Component tự gọi `this.$axios.post(...)` (upload file,
tải file) sẽ nhận **401** trong khi giao diện chỉ báo "thất bại" — phải tự đính
`Authorization: Bearer ${localStorage.getItem('access_token')}`. Chỉ các action trong
`store/actions.js` mới tự gắn sẵn.

**Tự kiểm trước khi báo xong** — lệnh này phải KHÔNG ra kết quả nào:

```bash
grep -rn "<input \|<textarea\|<select \|<button \|<label \|class=\"btn \|class=\"form-control" \
  pages/<phân-hệ>/<màn>/ | grep -v "V2Base"
```

---

## 1c. Khối NHÓM trong form — dùng `V2BaseFormSection`

Form/chi tiết chia thành các khối có tiêu đề ("Thông tin khách hàng", "Địa chỉ giao hàng",
"I – Danh sách thiết bị…"). **Dùng `components/V2BaseFormSection.vue`, KHÔNG tự dựng
`card` + `card-header` cho từng màn.**

```vue
<V2BaseFormSection title="I – Danh sách thiết bị cần kiểm tra sửa chữa – bảo hành" class="mb-2">
    <!-- nút / ô tìm / thông tin phụ nằm bên PHẢI tiêu đề -->
    <template #actions>
        <V2BaseButton secondary size="sm" @click="search">Tìm kiếm</V2BaseButton>
    </template>

    …nội dung khối…
</V2BaseFormSection>
```

- Tiêu đề cần markup riêng (badge trạng thái, ghi chú xám) → dùng slot `#title` thay prop `title`.
- Khuôn gốc: mục **"Địa chỉ giao hàng"** của màn Danh mục khách hàng (`/assign/customers/{id}`).

Vì sao bắt buộc: trước khi có component này, cùng một khối markup + khối SCSS
`.card-header.section-header` bị **copy-paste ở 35 file** (`CustomerForm.vue`, `assign/contracts`,
`assign/summary-quotations`, `assign/pricing-requests`…). Mỗi nơi lệch một chút — padding, cỡ chữ,
có/không `font-weight-bold` — và sửa 1 chỗ không lan sang chỗ khác.

⚠️ Màn cũ đang tự dựng thì **sửa dần khi có dịp đụng vào**, KHÔNG sửa đại trà.

### ⚠️ Màn hình hẹp: tiêu đề khối và cụm nút chen nhau

Hàng tiêu đề của `V2BaseFormSection` là flex `justify-content: between`, **không cho xuống dòng**.
Dưới ~1400px (sidebar mở, laptop 13–14"), tiêu đề dài bị bóp thành 2–3 dòng còn cụm ô tìm + nút
tự vỡ thành 2 hàng — nhìn như vỡ giao diện (Redmine #11170). Khai trong **màn đang làm** (đừng sửa
thẳng component dùng chung, nó đang chạy ở 35+ màn):

```scss
@media (max-width: 1400px) {
    ::v-deep .v2-form-section > .card-header { flex-wrap: wrap; gap: 6px 8px; }
    ::v-deep .v2-form-section > .card-header > h6 { flex: 1 1 100%; }        /* tiêu đề 1 hàng riêng */
    ::v-deep .v2-form-section > .card-header > .d-flex {
        flex: 1 1 100%;
        justify-content: flex-end;                                           /* cụm nút xuống hàng dưới */
    }
}
```

### ⚠️ Cột chứa TÊN TỆP / chuỗi dài kéo giãn cả bảng

Bảng `table-layout: auto` tính bề rộng cột theo **nội dung dài nhất**. Ô đính kèm hiện tên tệp lấy
từ URL S3 (đã nối thêm hậu tố, ~60–80 ký tự, không có dấu cách nên không xuống dòng) → cột đó
chiếm gần hết bề rộng bảng ở màn hình nhỏ, các cột khác bị bóp (Redmine #11164).

`text-overflow: ellipsis` **không cứu** được: nó chỉ đổi cách vẽ, không giảm bề rộng mong muốn của
cột. Phải **chốt bề rộng ngay trên `<th>`**:

```html
<th style="width: 230px; min-width: 230px">File đính kèm</th>
```

(`.v2-file__name` đã có sẵn `ellipsis` + `min-width: 0` nên thu hẹp là an toàn, hover vẫn xem được
tên đầy đủ.)

### ⚠️ Bảng trong form bị thừa khoảng trắng phía dưới

`assets/scss/default.scss` ép **`.table-responsive { min-height: 50vh }`** cho MỌI bảng. Hợp với
màn danh sách (bảng luôn dài), nhưng bảng trong FORM thường chỉ vài dòng:

| | Bảng thật | Khung `.table-responsive` | Thừa |
| --- | --- | --- | --- |
| Phiếu 1 thiết bị | 118px | **429px** (= 50vh) | **311px trống, có viền bao quanh** |

Nhìn như lỗi render. Cho khung co theo nội dung — **ghi đè CỤC BỘ, đừng sửa rule global**:

```vue
<div class="table-responsive v2-form-table-wrap"> … </div>
```
```scss
.v2-form-table-wrap { min-height: 0; }
```

Khung vẫn nở đúng khi bảng dài (đo: 17 dòng → 1183px, không cắt, không sinh cuộn dọc).

Cùng lý do, **bóp padding DỌC của ô bảng** — Bootstrap để `.table td/th { padding: .75rem }`
(12,8px trên/dưới) nên mỗi dòng cao 81px dù chữ chỉ 1-2 dòng:

```scss
.v2-form-table th,
.v2-form-table td {
    padding-top: 4px;
    padding-bottom: 4px;   /* giữ padding NGANG 8px để chữ không dính viền */
}
```

Đo sau khi áp cả 2 việc: khối 1 thiết bị **517px → 187px**, dòng dữ liệu **81px → 64px**, chữ không
bị cắt, ô nhập trong bảng (`V2BaseInput` 32px, `textarea` 53px) không bị bóp méo.

---

## 1d. CHỌN FILE — luôn dùng `V2BaseFile`

Mọi chỗ cho người dùng chọn/đính kèm file đều dùng **`components/V2BaseFile.vue`**.
Khuôn hiển thị lấy theo mục **"Import tài liệu kèm biên bản"** của màn Meeting
(`/assign/meeting/create` → tab Biên bản):

- Chưa có file → nút viền `⬆ Chọn tệp`
- Đang tải → spinner + *"Đang tải lên..."* (prop `uploading`)
- Đã có file → **icon theo loại** (pdf đỏ · word xanh dương · excel xanh lá · ảnh xanh nhạt)
  + tên file (cắt `…` nếu dài) + nút **Tải xuống / Thay đổi / Xóa**

```vue
<V2BaseFile
    :value="row.attachment"           <!-- URL đã lưu -->
    :uploading="uploadingIndex === i" <!-- màn tự upload rồi gán URL -->
    :disabled="readonly"
    accept=".pdf,.png,.jpg,.jpeg,.doc,.docx,.xls,.xlsx"
    placeholder="Chọn tệp"
    @change="onFileChange($event, row, i)"   <!-- trả về File; null = người dùng gỡ file -->
/>
```

- `autoUpload` để component tự đẩy lên endpoint ảnh dùng chung. Cần đúng thư mục riêng
  (vd `wr_requests` của ERP) thì **tự bắt `@change` rồi gọi endpoint của màn** — nhớ tự đính
  `Authorization`, xem cảnh báo `$axios` ở mục 1b.
- Cần cả BẢNG tài liệu (STT · Tên · Loại · Người thực hiện · Dung lượng) thì dùng
  `components/FileAttachmentTable.vue` thay vì tự ghép nhiều `V2BaseFile`.

⚠️ **Bẫy `position: absolute` của input file.** `.v2-file__input` là
`position:absolute; width:100%; height:100%; opacity:0`. Bọc nó trong phần tử **không có
`position: relative`** thì nó định vị theo tổ tiên positioned gần nhất → **ô trong suốt phủ lan cả
vùng lớn, bấm vào đâu cũng bật hộp thoại chọn file** (kể cả bấm select ở ô bên cạnh). Mọi wrapper
bọc input file phải có `position: relative; overflow: hidden;`.

---

## 2. Cách gắn validate lên V2Base*

vee-validate v2 (`plugins/vee-validate.js`) hỗ trợ gắn directive lên **component**, miễn là component
có prop `value` và emit `input` — cả `V2BaseInput`, `V2BaseSelect`, `V2BaseSelectInModal`,
`V2BaseDatePicker`, `V2BaseTextarea` đều thoả. Vì component không phải native input nên
**bắt buộc khai `data-vv-name`** (và nên có `data-vv-as` để câu lỗi đọc được):

```vue
<V2BaseLabel required>Tên dự án</V2BaseLabel>
<V2BaseInput
    v-model="formSubmit.name"
    v-validate="'required|max:255'"
    data-vv-name="name"
    data-vv-as="Tên dự án"
    data-vv-value-path="currentValue"
    :class="{ 'is-invalid': errors.has('name') }"
    size="sm"
/>
<V2BaseError :message="errors.first('name') || formError.name" />
```

- `data-vv-value-path="currentValue"` — dùng computed của V2Base* để chạy đúng cho cả `v-model` lẫn `:model-value`.
- `errors.first(...)` = lỗi FE realtime; `formError.<field>` = lỗi BE trả về. Ưu tiên hiện lỗi FE trước.
- Không có `classes: true` trong config → muốn viền đỏ thì tự bind `:class="{ 'is-invalid': errors.has('...') }"`.
- Select/DatePicker: chỉ validate khi giá trị đổi, nên chỉ dùng cho rule định dạng/`required` của Tên; **không** gắn `required` cho select khác.

Khi submit:

```js
async submitForm(status = 1) {
    // Chỉ chặn bởi rule FE (Tên + định dạng). Required khác do BE quyết theo status.
    const valid = await this.$validator.validateAll()
    if (!valid) return this.scrollToFirstError()

    try {
        this.formError = {}
        await this.$store.dispatch('...', { ...this.formSubmit, status })
        this.markFormSaved()
    } catch (e) {
        this.formError = e.response?.data?.errors || {}
        this.$toast.error('Bạn chưa nhập đầy đủ thông tin.')
        this.scrollToFirstError()
    }
}
```

---

## 3. Hành vi hiển thị lỗi (UX bắt buộc)

- Lỗi hiện **inline ngay dưới trường** (`V2BaseError`), **không dùng popup/modal để báo lỗi validate**.
- Rule FE: hiện ngay khi **rời trường / nhập sai** (realtime, không đợi bấm Lưu).
- Lỗi từ BE: hiện sau khi bấm Lưu; hiện **đồng thời tất cả** trường lỗi.
- Lỗi **tự biến mất** khi giá trị được sửa về hợp lệ (vee-validate tự làm; lỗi BE thì clear `formError` trước mỗi lần submit).
- Sau khi có lỗi → **scroll + focus vào trường lỗi đầu tiên** (quét trên → dưới, trái → phải).
- Còn lỗi FE thì **không gọi API lưu**.
- Câu lỗi tiếng Việt, không dùng thuật ngữ kỹ thuật. Mẫu: `Tên dự án không được để trống`, `Email không đúng định dạng`.

> Ghi chú: màn mới dùng cách này thì **không cần cờ `touched`** (cờ đó là để màn cũ không hiện lỗi trước lần submit đầu). Lỗi realtime hiện theo tương tác của user là đúng chuẩn.

### 3a. MỖI Ô MỘT KHOÁ LỖI RIÊNG — và xoá lỗi khi đổi ô hiện (chốt 2026-08-24)

Form có ô **đổi theo điều kiện** (tick một ô checkbox là ẩn ô A, hiện ô B) thì A và B **KHÔNG được
dùng chung một khoá trong `formError`**, dù cuối cùng cả hai cùng ghi vào một cột của DB.

Lỗi đã gặp (Redmine #11164): popup Thêm trang thiết bị có 2 ô cùng ghi vào `product_id` — *Trang
thiết bị* (khi không tick) và *Hàng công ty tương đương* (khi tick "Hàng công ty không bán"). Cả 2
cùng đọc `fieldError('product_id')`, nên bấm Lưu ở ô trên rồi tick vào là **lỗi nhảy xuống ô kia**
— người dùng chưa hề đụng vào ô đó.

Ba việc phải làm đủ:

1. **Khoá riêng cho từng ô**: `product_id` và `equivalent_product_id`.
2. **Đổi điều kiện hiện ô thì xoá lỗi cũ** — `this.formError = {}` ngay trong handler của ô tick,
   nếu không lỗi của lần bấm Lưu trước sẽ bám sang ô vừa hiện ra.
3. **Lỗi 422 của BE phải map về đúng ô đang hiện.** BE chỉ biết một cột `product_id`; FE tự chuyển
   sang khoá của ô đang hiển thị, tránh lỗi rơi vào ô đang bị `v-if` ẩn (user không thấy lỗi ở đâu
   mà nút Lưu vẫn không ăn):

```js
if (error?.response?.status === 422) {
    const errors = { ...(data?.errors || {}) }
    if (this.form.product_no_sale && errors.product_id) {
        errors.equivalent_product_id = errors.product_id
        delete errors.product_id
    }
    this.formError = errors
}
```

**Tự kiểm**: với mỗi ô bị `v-if`/`v-else`, bấm Lưu để sinh lỗi rồi bật/tắt điều kiện — không ô nào
được hiện lỗi mà user chưa từng đụng tới.

### 3b. BẢNG NHIỀU DÒNG — lỗi 422 gắn CHỈ SỐ dòng, đổi mảng là phải dọn (chốt 2026-08-25)

Laravel trả lỗi mảng theo khoá có **chỉ số dòng**: `products.2.serial`,
`extend_products.0.services.1.quantity`. FE lưu nguyên vào `formError` rồi đọc theo chỉ số đang
render — mà chỉ số là **VỊ TRÍ**, không phải danh tính dòng:

```
trước:  dòng 0 (ok) · dòng 1 (ok) · dòng 2 thiếu Serial  -> lỗi ở khoá `products.2.serial`
xoá dòng 1
sau:    dòng cũ số 2 nay là dòng 1 — nhưng lỗi vẫn nằm ở khoá `.2`
        -> dòng khác ăn oan lỗi, hoặc THÊM dòng mới vào là nó hiện lỗi ngay khi chưa ai đụng tới
```

Đã dính ở cả 3 màn luồng dịch vụ (Yêu cầu KT SC–BH · Phiếu xử lý · Phiếu CCTT).

**Dùng helper chung `utils/rowFieldErrors.js`, gọi NGAY TẠI CHỖ đổi mảng:**

| Thao tác | Gọi gì |
| --- | --- |
| Xoá 1 dòng (`splice(i, 1)`) | `removeRowErrors(formError, 'products', i)` — bỏ lỗi dòng đó, kéo lỗi dòng sau lên |
| Thêm dòng vào cuối (`push`) | `dropRowErrorsFrom(formError, 'products', arr.length)` — bỏ khoá chỉ số ≥ độ dài mới |
| Thay CẢ mảng (đổi khách hàng, tải lại phiếu gốc) | `clearRowErrors(formError, 'products')` |
| Chuyển dòng sang bảng khác | `removeRowErrors` ở khối nguồn **+** `dropRowErrorsFrom` ở khối đích |

```js
removeProduct(index) {
    this.form.products.splice(index, 1)
    this.formError = removeRowErrors(this.formError, 'products', index)
},
```

- `prefix` là đường dẫn tới **chính mảng** bị đổi, không kèm chỉ số — bảng lồng thì
  `` `extend_products.${pi}.services` ``.
- Có **lỗi cấp bảng** (`fieldError('products')` = "Chưa chọn thiết bị nào") thì thêm dòng xong phải
  `delete errors.products` — nếu không dòng đã có mà vẫn báo bảng rỗng.
- ⚠️ **KHÔNG chữa bằng `this.formError = {}`**: xoá sạch thì lỗi của những dòng KHÁC (user chưa sửa
  gì) cũng biến mất, bấm Lưu lại mới hiện — bằng việc giấu lỗi.
- ⚠️ Bảng con **splice thẳng trong template của component con** (`product.services.splice(si, 1)`)
  thì cha không biết để dọn → phải `$emit` ra cha, đừng mutate mảng của cha từ template con.

**Tự kiểm**: bấm Lưu cho ra lỗi ở dòng cuối → xoá dòng đầu → không dòng nào được hiện lỗi sai chỗ;
thêm dòng mới → dòng mới phải sạch.

---

---

## 3c. `validateAll()` KHÔNG thấy ô nằm trong component con (chốt 2026-08-28)

Form lớn hay tách bảng ra component riêng (`WrDeviceLinesTable`, `WrCostTable`…). Gắn `v-validate`
cho ô trong đó rồi bấm Lưu thì **lỗi hiện đỏ đúng, nhưng vẫn lưu được** — im lặng, không báo gì.

**Vì sao:** vee-validate gắn cho mỗi field một `vmId` = `_uid` của component CHỨA nó, còn
`this.$validator.validateAll()` lọc field theo `vmId` của chính component gọi. Ô trong bảng con có
`vmId` khác → không nằm trong danh sách được validate → `validateAll()` trả `true`.

`inject: ['$validator']` ở con **không cứu được**: nó làm hai bên dùng chung một validator, nhưng
`vmId` của field vẫn là của component chứa ô.

**Cách đúng — bỏ bộ lọc `vmId`:**

```js
// Cha, trước khi gọi API
const valid = await this.$validator.validateAll(null, { vmId: null })
if (!valid) {
    this.$toasted?.global?.error?.({ message: 'Vui lòng kiểm tra lại thông tin đã nhập' })
    return
}
```

`Field.matches()` bỏ qua kiểm tra khi `vmId` là null/undefined → quét mọi field đang mounted.

Ở component con, đặt `data-vv-name` **duy nhất theo dòng** (kèm cả biến thể bảng nếu một component
dùng cho 2 bảng), nếu không lỗi của ô này hiện luôn ở ô kia:

```js
daysField(product, index, group, childIndex) {
    return `days-${this.variant}-${group}-${this.rowKey(product, index)}-${childIndex}`
},
```

**Rule chỉ gắn khi ô CÓ giá trị** — ô không bắt buộc mà gắn cứng `positive_integer` thì vừa mở màn
đã đỏ lòm:

```js
daysRule(value) {
    return value === '' || value === null || value === undefined ? '' : 'positive_integer'
},
```

**Tự kiểm**: gõ chữ vào ô trong bảng con → bấm **Lưu nháp** → phải bị chặn, không được đi tiếp.

---

## 4. Rule custom có sẵn (đừng viết lại)

Khai trong `plugins/vee-validate.js`, dùng ngay: `min`, `max`, `max_value`, `phone`,
`uppercase_no_special_char`, `money_format`, `point_format`, `integer`, `positive_integer`,
`positive_decimal`, `greater_than`, `less_than`, `date_greater_than`, `date_smaller_than`,
`after_date`, `within_months`. Cần rule mới dùng nhiều nơi → thêm vào plugin (hỏi trước vì là file dùng chung).

---

## Checklist form ở màn mới

- [ ] Trường Tên: `v-validate="'required'"` + `data-vv-name` + `data-vv-as`
- [ ] KHÔNG có `required` ở FE cho trường khác (Lưu nháp phải lưu được với form gần như trống)
- [ ] Các rule định dạng (số/ngày/email/độ dài) gắn ở FE, chạy realtime
- [ ] Lỗi hiện inline qua `V2BaseError`, có `is-invalid`, không popup
- [ ] `validateAll(null, { vmId: null })` trước khi gọi API; còn lỗi thì không gọi API
      (thiếu `vmId: null` là bỏ sót mọi ô nằm trong component con — mục 3c)
- [ ] Rule ĐỊNH DẠNG chặn cả ở nút **Lưu nháp**, và có rule tương ứng ở **FormRequest** của BE
      với message viết y hệt FE (mục 1)
- [ ] Lỗi BE 422 map vào `formError` và hiển thị cùng chỗ với lỗi FE
- [ ] Scroll/focus trường lỗi đầu tiên
- [ ] Bảng nhiều dòng: mọi chỗ xoá/thêm/chuyển dòng đã dọn `formError` bằng `utils/rowFieldErrors.js` (mục 3b)
- [ ] Test: bấm Lưu nháp với form chỉ có Tên → lưu thành công
