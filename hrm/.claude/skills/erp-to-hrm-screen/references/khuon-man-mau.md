# Khuôn màn mẫu — Danh mục khách hàng

Màn **Danh mục khách hàng** (`hrm-client/pages/assign/customers/`) là **màn mẫu chuẩn** cho mọi màn
chuyển từ ERP sang HRM. Khi phân vân "màn mới phải có gì / đặt ở đâu" → mở màn này ra copy pattern,
đừng tự phát minh.

> Đây là **khuôn tham chiếu**, không phải template copy-paste mù. Copy đúng cấu trúc + tên component
> + tên mixin; nội dung cột/lọc/hành động thì bám theo màn ERP gốc.

---

## 0. Cấu trúc file

```
pages/<phân-hệ>/<slug>/
    index.vue        # Danh sách  (toàn bộ logic list/filter/export/import ở đây)
    add.vue          # Tạo mới    (mỏng — chỉ bọc component Form)
    _id/
        index.vue    # Chi tiết   (mỏng — bọc Form với prop `readonly`)
        edit.vue     # Chỉnh sửa  (mỏng — bọc Form với prop `id`)
components/<phân-hệ>-components/<slug>/
    <Ten>Form.vue    # Form dùng chung cho cả 3 màn add / edit / show
```

**Vì sao 1 Form dùng cho 3 màn**: chi tiết – sửa – tạo mới luôn phải trùng bố cục và trùng nhãn
trường. Tách 3 file riêng là nguồn gốc phổ biến nhất của lệch UI giữa các màn.

---

## 1. `index.vue` — màn danh sách

### Khung template (đúng thứ tự)

```vue
<template>
  <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
    <div class="container-fluid">
      <V2BaseSmartFilterPanel ... />   <!-- 1. Bộ lọc -->
      <V2BaseDataTable ...>            <!-- 2. Bảng -->
        <template #actions> ... </template>      <!-- toolbar nút -->
        <template #cell-index="{ index }"> ... </template>
        <template #cell-<key>="{ item }"> ... </template>
        <template #cell-actions="{ item }">
          <V2BaseRowActions :actions="getRowActions(item)" @action="..." />
        </template>
      </V2BaseDataTable>
    </div>

    <!-- 3. Các modal — LUÔN đặt NGOÀI .container-fluid -->
    <V2BaseImportModal ... />
    <BaseConfirmModal ... />
    <XxxHistoryModal ... />
    <ColumnCustomizationModal v-if="columnFieldsLoaded" ... />
    <ExportFieldsModal ... />
  </div>
</template>
```

### Mixin bắt buộc

```js
mixins: [PageTitleMixin, CheckPermission, filterStateMixin, columnCustomizationMixin]
```

| Mixin | Lo việc gì | Bỏ quên thì lỗi gì |
|---|---|---|
| `PageTitleMixin` | Tiêu đề tab trình duyệt | Tab hiện tên mặc định |
| `CheckPermission` | Cờ quyền `canCreate/canEdit/...` | Hiện nút cho người không có quyền |
| `filterStateMixin` | Ghi nhớ bộ lọc khi quay lại màn | Vi phạm SRS 1.4 — mất bộ lọc |
| `columnCustomizationMixin` | Ẩn/hiện + sắp xếp cột, lưu theo user | Vi phạm SRS 1.6 |

`filterStateMixin` cần khai trong `data()`:
```js
filterFieldName: 'filters',
localStorageKey: '<phân_hệ>_<slug>',   // PHẢI duy nhất giữa các màn
```
`columnCustomizationMixin` cần: `columnScreenKey: '<slug>'` — **duy nhất giữa các màn**, trùng key
sẽ làm 2 màn ghi đè cấu hình cột của nhau.

### Bộ lọc — khai bằng schema `filterFields`

⚠️ Dùng **`V2BaseSmartFilterPanel`**, KHÔNG dùng `V2BaseFilterPanel`. `V2BaseFilterPanel` là bản cũ,
màn phải tự dựng khối `#advanced-filters` bằng tay và **không có popup "Cài đặt bộ lọc"** — dựng
xong là thiếu quy tắc chung mà nhìn ngoài giao diện không phát hiện ra.

Không dựng tay từng `<input>`. Khai mảng schema để user tự bật/tắt + kéo sắp xếp trong popup
"Cài đặt bộ lọc" (cấu hình lưu ở bảng `filter_customizations` theo `table=<slug>`):

```js
filterFields() {
  return [
    { key: 'org', label: '...', wrapperClass: 'd-contents', hideLabel: true,
      resetKeys: ['company_id', 'department_id', 'part_id', 'employee_id'] },   // dùng slot
    { key: 'code',    label: 'Mã khách hàng', type: 'text',   placeholder: 'Nhập mã khách hàng' },
    { key: 'status',  label: 'Trạng thái',    type: 'select', options: this.statusOptions,
      placeholder: 'Chọn trạng thái' },
  ]
}
```

- Trường cần render nhiều control → dùng `<template #field-<key>>` như khối
  `V2BaseCompanyDepartmentFilter` và `CascadePairSelect`.
- **Thứ tự khối tổ chức luôn là**: Công ty → Phòng ban → Bộ phận → Nhân viên.
- **Không truyền prop `title`** cho panel — dùng mặc định "Bộ lọc danh sách".
- Placeholder: ô chọn = `Chọn <tên trường>`, ô gõ = `Nhập <tên trường>`,
  ô tìm nhanh = `Tìm theo <các trường BE thực sự lọc>`. Cấm `Tất cả`, `Chọn...`, để trống.

### Toolbar nút (`#actions`) — đúng thứ tự SRS

```
Tạo mới (primary) → Import Excel (secondary + status="warning")
→ Xuất CSV / Xuất Excel / Xuất PDF (secondary + status="success")
→ [dòng tiến độ khi đang xuất] → Cấu hình cột (V2BaseIconButton)
```
- Nút **chỉ có icon** → `V2BaseIconButton`, KHÔNG dùng `V2BaseButton`.
- Nút có text → luôn kèm icon qua `<template #prefix>`.
- Không có quyền → `v-if` **ẩn hẳn**, không disable.

### Cột & ô bảng

- Cột `index` (STT) render qua `getNumericalOrder(currentPage, pageSize, index)` — không dùng
  `index + 1` (sai từ trang 2).
- Cột **Mã** là `<nuxt-link>` thật (để chuột giữa / chuột phải mở tab mới được), class
  `v2-cell-link field-line`.
- Cột **Tên** là chữ thường, KHÔNG phải link, KHÔNG in đậm: `field-line text-dark font-weight-normal`.
- Giá trị rỗng → in `—` (em dash), không để trống.
- Ngày giờ: BE trả sẵn chuỗi `dd/mm/yyyy HH:mm`, FE **không tự format lại**.
- Trạng thái: `V2BaseBadge` với `variant`. KHÔNG tự khai `<span class="status-pill">` +
  `statusPillClass()` cho từng màn.
  - Màn có **trạng thái nhị phân** (hoạt động / khóa): `Number(item.status) === 1 ? 'brand' : 'required'`.
  - Màn **phiếu nhiều trạng thái** (BE trả `status_type`): dùng helper chung
    `@/utils/statusBadgeVariant.js` → `statusBadgeVariant(item.status_type)`.
    Bảng quy đổi: `success`→`brand` (xanh) · `warning`→`status-draft` (vàng) ·
    `danger`→`required` (đỏ) · còn lại →`muted` (xám).
  - ⚠️ Kiểm hằng `STATUSES` ở BE: trạng thái **Nháp / Đang tạo phải là xám**, không phải `danger`.
    ERP hay gán đỏ cho phiếu mới lập — bê nguyên sang là sai theo bảng màu SRS.

### Cột Hành động — `getRowActions(item)`

```js
getRowActions(item) {
  const isActive = Number(item.status) === 1
  return [
    { key: 'edit', title: 'Sửa', icon: 'ri-edit-line',
      to: `/assign/customers/${item.id}/edit`,
      visible: this.canEdit && isActive },
    { key: isActive ? 'lock' : 'unlock', title: isActive ? 'Khóa' : 'Mở khóa',
      icon: isActive ? 'ri-lock-line' : 'ri-lock-unlock-line', visible: this.canLock },
    { key: 'manage',  title: 'Quản lý', icon: 'ri-folder-user-line', to: `.../manager` },
    { key: 'history', title: 'Lịch sử', icon: 'ri-history-line' },
  ]
}
```

- **2 phần tử đầu = 2 nút chính hiện thẳng trên dòng**, phần còn lại tự gom vào menu "…".
  Thứ tự khai quan trọng: Sửa → Xóa (hoặc Khóa/Mở khóa nếu màn không có Xóa) → còn lại.
- Không còn hành động "Xem" — bấm Mã ở cột đầu là vào chi tiết.
- Ẩn nút bằng `visible`, KHÔNG dùng `interactable` + `disabledTitle`.
- `V2BaseRowActions` emit **chuỗi key**, không phải object — handler phải so `action === 'edit'`.
- Icon chuẩn: Sửa `ri-edit-line`, Xóa `ri-delete-bin-6-line`, Khóa `ri-lock-line`,
  Mở khóa `ri-lock-unlock-line`, Lịch sử `ri-history-line`.

---

## 2. `add.vue` / `_id/edit.vue` / `_id/index.vue` — 3 màn mỏng

Cả 3 chỉ bọc component Form:

```vue
<!-- add.vue -->
<template><div><XxxForm ref="xxxForm" @saved="markFormSaved" /></div></template>
<script>
export default {
  layout: 'default-sidebar',
  middleware: 'checkXxxPermission',
  mixins: [PageTitleMixin, unsavedChangesMixin],
  head() { return { title: 'Tạo <đối tượng> mới' } },
  methods: {
    // Form nằm ở component con → phải trỏ mixin sang đó
    unsavedSnapshotSource() {
      const form = this.$refs.xxxForm
      if (!form) return null
      return { ...form.form, /* + các mảng con user sửa được */ }
    },
  },
}
</script>
```

```vue
<!-- _id/index.vue (chi tiết) -->
<XxxForm :id="xxxId" readonly @loaded="onLoaded" />
```
Tiêu đề chi tiết: `Chi tiết <đối tượng>: <mã>` — **chỉ ghép mã khi bản ghi có mã**; không có mã thì
để tiêu đề trần, KHÔNG lấy tên thay thế.

`unsavedSnapshotSource` phải **loại các field do API tự điền** (vd `bankBranchOptions`,
`loadingBranches`) — nếu không thì vừa mở màn đã bị coi là "có thay đổi chưa lưu".

---

## 3. Form (`components/<phân-hệ>-components/<slug>/XxxForm.vue`)

- Nút BẮT BUỘC đặt trong **`V2Footer`** (`components/V2Footer.vue`), không tự dựng
  `<div class="d-flex justify-content-end">` + loạt `V2BaseButton`. `V2Footer` tự render
  "Quay lại" ở cuối — đừng tự thêm.
- Thứ tự nút form: **Lưu nháp → Lưu / Gửi duyệt / In → Xuất file, Xem trước → Quay lại danh sách**.
- Validate realtime bằng `vee-validate` gắn trên component `V2Base*`. **Chỉ trường Tên gắn
  `required` ở FE** (vì Lưu nháp không được chặn trường khác); required còn lại do BE quyết theo
  `status` rồi trả 422 → FE map vào `formError`.
- Select trong modal/popup dùng `V2BaseSelectInModal`, ngoài modal dùng `V2BaseSelect`.
- Danh mục đã khóa vẫn phải hiện đúng tên khi bản ghi đang dùng nó (🔒 do
  `utils/select2LockedOption.js` tự gắn — FE không phải khai gì).

---

## 4. Modal dùng chung — dùng đúng component có sẵn

| Việc | Component |
|---|---|
| Popup bất kỳ (khuôn chung) | `components/modal/V2BaseModal.vue` |
| Xác nhận (Xóa, Khóa/Mở khóa, Duyệt/Từ chối, thoát chưa lưu) | `components/modal/base-confirm-modal.vue` hoặc `await this.$confirm({...})` |
| Import Excel | `V2BaseImportModal` |
| Chọn trường xuất file | `components/modal/export-fields-modal.vue` |
| Cấu hình cột hiển thị | `ColumnCustomizationModal` |

**Tuyệt đối không** tự khai `b-modal` + header/footer riêng cho từng màn, không dùng
`$bvModal.msgBoxConfirm()`.

---

## 5. Xuất file

- Bấm nút Xuất → mở `ExportFieldsModal` cho user **chọn trường** trước, không xuất thẳng.
- Thứ tự cột trong file = thứ tự user chọn.
- Đang xuất → khóa nút (`:disabled="exporting"`) + hiện dòng tiến độ
  (`Đã tải 4.000/17.542 dòng…`), vì file dựng trên trình duyệt có thể mất vài chục giây.
- `$axios` của FE **không tự gắn `Authorization`** cho request tải file — phải tự gắn token.

---

## 6. Import Excel

`V2BaseImportModal` đã lo đủ 4 khu vực SRS (File – Hành động – Kết quả – Xóa tất cả dòng lỗi).
Màn chỉ cần cấp:

```
:columns  :required-fields  :validation-rules  template-file-name  :skip-rows
@validate-data  @import-data  @download-template
```

Giữ nguyên **thứ tự cột của file mẫu ERP** cho phần cột cũ, cột riêng của HRM append vào cuối —
để user đang dùng file mẫu ERP không phải sắp lại.
