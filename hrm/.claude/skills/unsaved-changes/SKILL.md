---
name: unsaved-changes
description: Use when tạo/sửa bất kỳ màn form nào ở hrm-client (page add/edit, modal form) — bắt buộc cảnh báo "chưa lưu" khi user thoát, dùng mixin unsavedChangesMixin có sẵn
---

# Skill: Cảnh báo dữ liệu chưa lưu (Unsaved Changes Guard)

Áp dụng cho **mọi màn có nhập liệu**: page Tạo mới / Sửa, modal form lớn, wizard nhiều bước.
Quy tắc QLDA_002 / QLDA_008 — bắt buộc toàn hệ thống, không phải tuỳ chọn theo màn.

---

## 1. Hành vi bắt buộc

| Tình huống | Hành vi |
|---|---|
| User đã sửa dữ liệu, chưa lưu, bấm Quay lại / đổi route / bấm menu khác | Hiện popup xác nhận, chặn điều hướng cho đến khi user chọn |
| User đóng tab / F5 | Hộp thoại mặc định của trình duyệt (`beforeunload`) |
| User chưa sửa gì | Thoát thẳng, KHÔNG hỏi |
| User sửa rồi trả lại đúng giá trị cũ | KHÔNG hỏi |
| Lưu thành công rồi mới chuyển trang | KHÔNG hỏi |

Nội dung popup:
- Message: `Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?`
- Title: `Thông tin chưa lưu`
- Nút: **Thoát** (`okVariant: 'danger'`) / **Ở lại**
- Chọn Thoát → rời màn, chấp nhận mất dữ liệu. Chọn Ở lại → đóng popup, giữ nguyên dữ liệu đang nhập.

---

## 2. Cách làm — dùng mixin có sẵn

File: `utils/mixins/unsavedChangesMixin.js` (hrm-client). **Không tự viết `beforeRouteLeave` riêng cho từng màn.**

```js
import unsavedChangesMixin from '@/utils/mixins/unsavedChangesMixin'

export default {
    mixins: [PageTitleMixin, unsavedChangesMixin],
    methods: {
        // Mặc định mixin theo dõi this.formSubmit — form tên khác thì override
        unsavedSnapshotSource() {
            return this.formData
        },

        // Field do BE / section tự điền, user không nhập → bỏ qua khi so sánh
        unsavedIgnoredKeys() {
            return ['can_change_project_type', 'allocated_budget']
        },

        async save() {
            await this.$store.dispatch('...')
            this.markFormSaved()          // BẮT BUỘC, gọi trước khi chuyển trang
            this.$router.push('...')
        },
    },
}
```

API của mixin:

| Method | Khi nào gọi |
|---|---|
| `markFormSaved()` | Ngay sau khi lưu thành công, **trước** `$router.push` — nếu quên sẽ bị hỏi thừa |
| `markFormPristine()` | Chốt lại mốc so sánh sau khi nạp xong dữ liệu màn Sửa (khi cần) |
| `unsavedSnapshotSource()` | Override khi form không nằm ở `this.formSubmit` |
| `unsavedIgnoredKeys()` | Override để loại field auto-fill khỏi phép so sánh |
| `isFormDirty()` | Đọc trạng thái bẩn nếu màn cần tự xử lý thêm (vd nút Quay lại tự viết) |

Mixin tự động: watch snapshot form, đăng ký `beforeRouteLeave` + `beforeunload`,
gỡ listener ở `beforeDestroy`.

---

## 3. Cạm bẫy (đọc trước khi "cải tiến")

- **KHÔNG thay bằng so sánh trần** `JSON.stringify(form) !== initialForm`. Các section trong màn tự ghi vào form bằng dữ liệu API (KD phụ trách, tiền tệ mặc định, options Loại hình/Lĩnh vực, kế thừa từ dự án cha…) và về lúc nào là không đoán được → sẽ báo "chưa lưu" cả khi user không đụng gì.
- Mixin chỉ tính là thay đổi DO USER khi nó xảy ra trong ~500ms sau thao tác chuột/bàn phím; thay đổi đến muộn hơn = auto-fill → dời mốc so sánh, không đánh dấu bẩn.
- Listener bắt ở `document` (không chỉ trong `$el`) vì dropdown select2 / modal chọn KH render ngoài phạm vi component.
- Field kiểu mảng options nạp từ API (`*_options`) đã bị mixin loại sẵn khỏi snapshot.
- Sửa mixin = sửa hàm dùng chung → **hỏi trước khi sửa**, mọi màn form đang phụ thuộc vào nó.

---

## 4. Màn tham chiếu đã làm đúng

- `pages/assign/prospective-projects/_id/edit.vue` (+ `add.vue`)
- `pages/assign/summary-quotations/_id/edit.vue` (có override `unsavedSnapshotSource`)

---

## Checklist khi làm màn form mới

- [ ] Đã `mixins: [unsavedChangesMixin]`
- [ ] Override `unsavedSnapshotSource()` nếu form không phải `formSubmit`
- [ ] Đã gọi `markFormSaved()` ở TẤT CẢ nhánh lưu thành công (Lưu, Lưu & tiếp tục, Gửi duyệt…)
- [ ] Test: mở màn không sửa gì → bấm Quay lại → thoát thẳng, không hỏi
- [ ] Test: sửa 1 trường → Quay lại → hiện popup; chọn Ở lại thì dữ liệu còn nguyên
- [ ] Test: lưu thành công → không bị hỏi khi chuyển trang
