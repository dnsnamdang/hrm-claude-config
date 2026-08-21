---
name: form-validate
description: Use when làm form nhập liệu ở màn MỚI của hrm-client (add/edit page, modal form) — validate realtime bằng vee-validate trên component V2Base*, và quy tắc chỉ trường Tên mới required ở FE (lưu nháp không bị chặn)
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
- [ ] `validateAll()` trước khi gọi API; còn lỗi thì không gọi API
- [ ] Lỗi BE 422 map vào `formError` và hiển thị cùng chỗ với lỗi FE
- [ ] Scroll/focus trường lỗi đầu tiên
- [ ] Test: bấm Lưu nháp với form chỉ có Tên → lưu thành công
