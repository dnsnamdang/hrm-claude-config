---
name: unsaved-changes
description: Use when tạo/sửa bất kỳ màn form nào ở hrm-client — page add/edit, MODAL/POPUP Thêm-Sửa danh mục, trang vỏ render component form con. Bắt buộc cảnh báo "chưa lưu" khi user thoát. Có 3 mixin có sẵn tuỳ kiểu màn (unsavedChangesMixin / unsavedModalMixin / unsavedChildFormMixin) — chọn sai thì popup không bao giờ hiện, xem mục 2b.
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

## 2b. Chọn đúng mixin theo kiểu màn — có 3 file

| Kiểu màn | Mixin | Chặn ở đâu |
|---|---|---|
| Form nằm ngay trong page của route (`add.vue`/`edit.vue`/`index.vue` có form) | `unsavedChangesMixin` | `beforeRouteLeave` + `beforeunload` |
| Form trong **modal** (danh mục Thêm/Sửa) | `unsavedModalMixin` | sự kiện `hide` của `b-modal` |
| Trang vỏ chỉ render **component form con** | `unsavedChildFormMixin` (trang vỏ) + `unsavedChangesMixin` (component con) | trang vỏ uỷ quyền `isFormDirty()` cho con |

**Vì sao phải tách:**
- `beforeRouteLeave` KHÔNG chạy khi đóng modal (không đổi route) → modal cần mixin riêng.
- `beforeRouteLeave` CHỈ chạy trên component của route, KHÔNG chạy trên component con →
  form nằm ở `components/XxxFormComponent.vue` thì gắn mixin vào con là vô nghĩa.

### Modal — 3 sự kiện bắt buộc tách riêng

```html
<b-modal ref="my-modal" @shown="onUnsavedModalShown" @hide="onUnsavedModalHide" @hidden="afterModalHidden">
```

| Sự kiện | Việc | Cấm |
|---|---|---|
| `@shown` | `markFormPristine()` — modal không bị destroy giữa các lần mở nên phải chốt lại mốc | |
| `@hide` | guard, có thể `preventDefault()` | |
| `@hidden` | reset dữ liệu + `$emit('closeModal')` | **KHÔNG reset ở `@hide`** — guard chặn lại thì form đã bị xoá trắng, bấm "Ở lại" cũng không còn gì |

Modal load detail SAU khi `show()` (kiểu `open(id)` → `show()` → `await loadDetail()`) thì
phải gọi `markFormPristine()` cuối `loadDetail` — `@shown` đã chốt mốc trên form rỗng rồi.

### Trang vỏ

```html
<XxxFormComponent ref="form" />
```
```js
mixins: [PageTitleMixin, unsavedChildFormMixin]   // trang vỏ
mixins: [unsavedChangesMixin]                     // component con, có markFormSaved()
```

---

## 3. Cạm bẫy (đọc trước khi "cải tiến")

- Màn nào đã tự viết confirm "chưa lưu" riêng cho nút Hủy → **bỏ cái riêng đi**, để route guard
  hỏi bằng popup chuẩn. Giữ cả hai sẽ hỏi 2 lần với 2 wording khác nhau.
- Dữ liệu detail nạp về ngay sau cú click "Sửa" ở màn danh sách có thể rơi vào cửa sổ 500ms
  → bị tính nhầm là user vừa nhập. Màn Sửa luôn gọi `markFormPristine()` cuối hàm load.
- **KHÔNG thay bằng so sánh trần** `JSON.stringify(form) !== initialForm`. Các section trong màn tự ghi vào form bằng dữ liệu API (KD phụ trách, tiền tệ mặc định, options Loại hình/Lĩnh vực, kế thừa từ dự án cha…) và về lúc nào là không đoán được → sẽ báo "chưa lưu" cả khi user không đụng gì.
- Mixin chỉ tính là thay đổi DO USER khi nó xảy ra trong ~500ms sau thao tác chuột/bàn phím; thay đổi đến muộn hơn = auto-fill → dời mốc so sánh, không đánh dấu bẩn.
- Listener bắt ở `document` (không chỉ trong `$el`) vì dropdown select2 / modal chọn KH render ngoài phạm vi component.
- Field kiểu mảng options nạp từ API (`*_options`) đã bị mixin loại sẵn khỏi snapshot.
- Sửa mixin = sửa hàm dùng chung → **hỏi trước khi sửa**, mọi màn form đang phụ thuộc vào nó.

---

## 4. Màn tham chiếu đã làm đúng

- `pages/assign/prospective-projects/_id/edit.vue` (+ `add.vue`)
- `pages/assign/summary-quotations/_id/edit.vue` (có override `unsavedSnapshotSource`)
- Modal: `components/modal/customer-care/level-modal.vue` (đơn giản nhất),
  `pages/finance/cost-debts/CostDebtModal.vue` (load detail sau khi show)
- Trang vỏ + form con: `pages/finance/accounts/{add,_id/edit}.vue` + `components/AccountFormComponent.vue`

**Đã áp dụng:** 14 màn danh mục của 2 phân hệ customer-care + finance (đợt 1, 2026-08-12).
Các phân hệ cũ (decision, assign, training, human, timesheet) **chưa làm** — xem
`.plans/gop-db/unsaved-changes-catalogs/`.

---

## Checklist khi làm màn form mới

**Rà đủ 3 chỗ nhập liệu của màn — đừng chỉ nhìn page.** Một màn danh mục thường KHÔNG có
page `add/edit`, toàn bộ Thêm/Sửa nằm trong modal → dễ tưởng "màn này không có form".

- [ ] Đã liệt kê hết chỗ nhập liệu: page `add/edit` · **modal Thêm/Sửa** · component form con
- [ ] Chọn đúng mixin theo bảng mục 2b (gắn nhầm thì không lỗi gì, chỉ là popup không hiện)
- [ ] Override `unsavedSnapshotSource()` nếu form không phải `formSubmit` (modal thường là `this.data`)
- [ ] Dữ liệu nhập nằm ở nhiều biến (ma trận, danh sách hàng hoá, file đính kèm) → snapshot gộp đủ, đừng chỉ `this.form`
- [ ] Đã gọi `markFormSaved()` ở TẤT CẢ nhánh lưu thành công (Lưu, Lưu & tiếp tục, Gửi duyệt…)
- [ ] Màn Sửa: `markFormPristine()` ở cuối hàm load detail
- [ ] Màn đã có confirm "chưa lưu" tự viết riêng → đã bỏ đi, không để hỏi 2 lần

**Test — page làm 3 ca, modal làm 5 ca:**

- [ ] Mở, không sửa gì → Quay lại / Đóng → thoát thẳng, không hỏi
- [ ] Sửa 1 trường → Quay lại / Đóng → hiện popup; chọn Ở lại thì dữ liệu còn nguyên
- [ ] Lưu thành công → không bị hỏi
- [ ] **Modal:** bấm dấu × và bấm ra nền ngoài modal + phím Esc → đều phải hỏi
- [ ] **Modal:** "Lưu & Tiếp tục" → form trống trở lại, đóng luôn thì KHÔNG hỏi
