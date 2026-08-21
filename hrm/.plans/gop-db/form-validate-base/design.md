# Validate realtime trên base V2Base\* — design (tóm tắt)

> Người phụ trách: @khoipv · Nhánh: `gop_db` · Bắt đầu: 2026-08-14
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-14-form-validate-base-design.md`

## Mục tiêu

Cho phép gắn `v-validate` (vee-validate v2) **trực tiếp lên component `V2Base*`** ở MỌI màn của
`hrm-client`, để lỗi hiện **realtime** ngay khi user nhập / đổi giá trị — thay vì phải bấm Lưu mới
biết (cơ chế cờ `touched` hiện tại). Bám đúng skill `.claude/skills/form-validate/SKILL.md`.

Cách dùng sau khi sửa base:

```vue
<V2BaseLabel>Tên gói bảo dưỡng <Required /></V2BaseLabel>
<V2BaseInput
    v-model="form.name"
    v-validate="'required|max:255'"
    name="name"
    :invalid="hasFieldError('name')"
/>
<V2BaseError :message="fieldError('name')" size="sm" class="mb-0" />
```

## Hiện trạng (trước khi sửa)

- Chưa có màn nào gắn `v-validate` lên `V2Base*` (grep toàn repo = 0 kết quả) — vee-validate chỉ dùng
  với `base-input-field` của các phân hệ cũ (Quyết định, Nhân sự…).
- Gắn `v-validate` lên `V2Base*` **không chạy đúng** nếu không khai thêm `data-vv-name` +
  `data-vv-value-path` ở từng ô: vee-validate đọc giá trị component theo prop `value`, trong khi
  `V2Base*` có 2 prop (`value` + `modelValue`) và giá trị thật nằm ở computed `currentValue`.
- `:class="{ 'is-invalid': … }"` truyền vào `V2Base*` **không đổi màu viền**: class rơi vào thẻ bọc
  (`div.v2-input__wrapper`, `div.v2-select`…) trong khi Bootstrap chỉ style `.form-control.is-invalid`
  và `.custom-select.is-invalid`. → Các màn đang tưởng có viền đỏ nhưng thực tế không có.
- vee-validate **không bao giờ** tự gắn class cho component (`Field`: `classes && !componentInstance`)
  → bắt buộc phải có cách bật viền đỏ thủ công.

## 3 quyết định chính

1. **`$_veeValidate` đặt trong mixin dùng chung** (`utils/mixins/v2ValidateMixin.js`) thay vì bắt mỗi
   ô khai `data-vv-value-path="currentValue"`. vee-validate v2 đọc `name()` / `value()` từ option này
   khi directive gắn lên component (`Resolver.resolveName` / `Resolver.resolveGetter`).
2. **Prop `invalid`** trên `V2Base*` + style `.is-invalid` viết trong `<style>` (không scoped) của
   chính component → viền đỏ chạy ở mọi màn, kể cả ngoài `.v2-styles`, và tương thích ngược với các
   màn đang truyền `:class="{ 'is-invalid': … }"`.
3. **Mixin cấp trang** `utils/mixins/formValidateMixin.js` gộp 2 nguồn lỗi về 1 chỗ:
   `fieldError(name)` = lỗi FE (`errors.first`) → nếu không có thì lấy lỗi BE 422 (`formErrors`).
   Trang không phải tự viết `showError` / `fieldError` / map lỗi 422 / scroll nữa.

## Ràng buộc nghiệp vụ (theo skill `form-validate`)

FE **chỉ** gắn `required` cho trường **Tên**. Mọi `required` khác do **BE** quyết theo trạng thái
(nháp / chính thức) và trả 422 → FE map vào `formErrors`. Rule định dạng (số, ngày, độ dài, email…)
vẫn gắn ở FE và chạy realtime.

## Phạm vi đợt này

- Base: 7 component nhập liệu (`V2BaseInput`, `V2BaseTextarea`, `V2BaseSelect`, `V2BaseSelectInModal`,
  `V2BaseSelectRemote`, `V2BaseDatePicker`, `V2BaseCurrencyInput`) + 2 mixin mới.
- Màn áp dụng mẫu: **Gói bảo dưỡng** (`pages/customer-care/services/components/ServiceFormComponent.vue`).
- Các màn `V2Base*` khác **giữ nguyên** — thay đổi tương thích ngược (prop `invalid` mặc định `false`,
  không đụng API cũ).

## Điểm cần lưu ý khi dùng ở màn khác

- Phải khai tên field (component không có `name` như thẻ `<input>`). Viết `name="..."` là đủ —
  `Resolver.resolveName()` đọc `$attrs['data-vv-name'] || $attrs['name']`; `data-vv-name` chỉ cần khi
  muốn tên field KHÁC thuộc tính `name` của thẻ.
- `data-vv-as` (nhãn đọc được) hiện **không đổi câu lỗi nào** vì mọi message trong `locales/vi.json`
  và `plugins/vee-validate.js` đều viết cứng, không chèn tên trường. Chỉ cần khai cho ô nào bị trường
  khác so sánh tới (`greater_than`, `date_greater_than`…) — vee-validate lấy `targetName` = alias của
  trường đích.
- vee-validate chỉ nghe được event **`input`** của component (`$on`) — sự kiện `blur` native của thẻ
  input bên trong KHÔNG kích hoạt validate. Nên lỗi hiện khi **giá trị đổi**, không phải khi rời ô.
- Trong `v-for` (bảng ma trận): `data-vv-name` phải gắn theo **`_uid` của dòng**, không dùng index —
  xóa 1 dòng làm index dịch, lỗi sẽ bám nhầm ô.
- Directive phải nằm ở **trang/component form**, không được bọc vào component con: mỗi component có
  `ScopedValidator` riêng theo `vmId`, field đăng ký ở con thì `$validator.validateAll()` của cha
  không thấy.

## Liên quan

- Skill: `.claude/skills/form-validate/SKILL.md` (mục 2 đang hướng dẫn khai `data-vv-value-path` ở
  từng ô — sau đợt này không cần nữa → cần PR cập nhật skill, không tự sửa).
- Feature dùng làm màn mẫu: `.plans/gop-db/customer-care-services-catalog/`.
