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

### Khối `<style>` bắt buộc — dễ quên nhất

Cuối `index.vue` **và** cuối component `XxxForm.vue` phải có (KHÔNG `scoped`):

```vue
<style lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

`create.vue` / `_id/edit.vue` / `_id/index.vue` không cần — chúng render `XxxForm` nên CSS theo đó vào.

⚠️ Thiếu khối này màn **vẫn nhìn gần như đúng**: bảng, nút, cột đều ổn nhờ Bootstrap và CSS của route
khác còn trong bundle. Chỗ duy nhất vỡ là **bộ lọc nâng cao** — CSS của `v2-styles.scss` biên dịch kèm
`data-v-<hash>` của component đã import nó, nên hash của màn khác không áp được
`.v2-styles .d-contents { display: contents }`; wrapper `d-contents` của `V2BaseSmartFilterPanel` giữ
`display: block`, các `col-md-3` bên trong (ô Công ty/Phòng ban/Bộ phận, các cặp ô khoảng ngày) thôi
không còn là flex item của `.form-row` → bị bóp còn ~130px, nhãn vỡ dòng, select cụt chữ.

Tự kiểm trước khi nghiệm thu:

```bash
grep -L "v2-styles.scss" pages/<phân-hệ>/<màn>/index.vue pages/<phân-hệ>/<màn>/components/*.vue
```

Kiểm trên trình duyệt (mở bộ lọc nâng cao rồi chạy) — phải ra `contents`, ra `block` là thiếu import:

```js
getComputedStyle(document.querySelector('.smart-advanced-filters .form-row > .d-contents')).display
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

### Bộ lọc — khai bằng schema `filterFields`, BẬT nhãn floating

⚠️ Dùng **`V2BaseSmartFilterPanel`**, KHÔNG dùng `V2BaseFilterPanel`. `V2BaseFilterPanel` là bản cũ,
màn phải tự dựng khối `#advanced-filters` bằng tay và **không có popup "Cài đặt bộ lọc"** — dựng
xong là thiếu quy tắc chung mà nhìn ngoài giao diện không phát hiện ra.

```vue
<V2BaseSmartFilterPanel
    table="<slug>"
    floating                          <!-- BẮT BUỘC với màn port mới -->
    :filter-fields="filterFields"
    :filters="filters"
    :collapsed="filterCollapsed"
    :quick-search-value="filters.keyword"
    quick-search-placeholder="Tìm theo <các trường BE thực sự lọc>"
    @toggle-panel="filterCollapsed = !filterCollapsed"
    @quick-search-change="..." @filter-change="..." @search="..." @reset="..."
/>
```

Không dựng tay từng `<input>`. Khai mảng schema để user tự bật/tắt + kéo sắp xếp trong popup
"Cài đặt bộ lọc" (cấu hình lưu ở bảng `filter_customizations` theo `table=<slug>`):

```js
filterFields() {
  return [
    { key: 'org', label: '...', wrapperClass: 'd-contents', hideLabel: true,
      resetKeys: ['company_id', 'department_id', 'part_id', 'employee_id'] },   // dùng slot
    { key: 'code',    label: 'Mã khách hàng', type: 'text',   placeholder: '' },
    { key: 'status',  label: 'Trạng thái',    type: 'select', options: this.statusOptions },
    { key: 'created_at', label: 'Ngày tạo',   variant: 'range' },   // khoảng ngày trong 1 ô
    { key: 'application_id', label: 'Ứng dụng', variant: 'tags' },  // ô chip nhiều lựa chọn
  ]
}
```

- Trường cần render nhiều control → dùng `<template #field-<key>>` như khối
  `V2BaseCompanyDepartmentFilter` và `CascadePairSelect`.
- **Thứ tự khối tổ chức luôn là**: Công ty → Phòng ban → Bộ phận → Nhân viên.
- **Không truyền prop `title`** cho panel — dùng mặc định "Bộ lọc danh sách".

#### Nhãn floating — CHUẨN GIAO DIỆN ô lọc (chốt 07/09/2026)

Màn mẫu: **`pages/assign/prospective-projects/index.vue`**. Nhãn nằm giữa ô khi rỗng, **bay lên đè
viền trên** khi ô có dữ liệu hoặc đang focus. Ô cao **36px**, nhãn không chiếm thêm dòng riêng nên
khối lọc gọn hơn hẳn kiểu nhãn-trên-ô-dưới.

Bật bằng prop `floating` trên `V2BaseSmartFilterPanel`. Panel tự bọc mỗi ô bằng
`V2BaseFloatingField`, tự tính `hasValue`, tự truyền chiều cao 36px xuống `V2BaseSelect`.

| Việc | Ai lo | Bạn phải làm gì |
|---|---|---|
| Nhãn + hiệu ứng bay lên | Panel | chỉ bật `floating` |
| `hasValue` (nhãn bay lên khi có dữ liệu) | Panel | field gom nhiều ô thì **phải khai `resetKeys`**, panel dựa vào đó |
| Chiều cao 36px | Panel (`control-height`) | không đụng |
| Icon ⓘ chú thích | `V2BaseFloatingField` tra từ điển `utils/constants/field-hints` theo `label` | thêm `hint: '...'` nếu muốn đè, `noHint: true` nếu muốn tắt |
| Nút phụ trong nhãn (công tắc ổ khoá…) | slot `label-suffix` của `V2BaseFloatingField`; `V2BaseCompanyDepartmentFilter` đã gắn sẵn cho Công ty / Phòng ban / Bộ phận | tự dựng nút mới thì cho class `ff-label-action` để có vùng bấm nới rộng |

⚠️ **Nút phụ đặt trong NHÃN, không đặt trong ô.** Trong ô đã có mũi tên select + nút ×, chen thêm
là ba thứ giành nhau 30px cuối. Nhưng nhãn float lên viền thì chữ chỉ còn cao ~11px và icon ~14px,
nên nút bắt buộc mang class `ff-label-action` — component nới vùng bấm bằng `::after { inset: -9px }`
để vùng bắt chuột đạt ~32px. Kiểm bằng cách bấm LỆCH 6px ra ngoài icon lúc nhãn đang float: vẫn
phải ăn.

**Khai `variant` cho ô đặc biệt:**

| `variant` | Dùng khi | Ghi chú |
|---|---|---|
| (bỏ trống) | ô chữ / select / 1 datepicker | |
| `'range'` | khoảng ngày **trong 1 ô** (Từ → Đến) | dùng `<template #field-...>` đặt 2 datepicker + `<span class="ff__sep">→</span>` |
| `'tags'` | ô chip nhiều lựa chọn | control bên trong phải bỏ viền riêng, không thì viền đôi |

**Placeholder khi bật floating — KHÁC quy tắc cũ:**
- Nhãn floating đã nói đủ tên trường → **BỎ placeholder trùng nhãn**. Không viết
  `placeholder: 'Chọn trạng thái'` cho ô nhãn "Trạng thái" nữa: lúc nghỉ nhãn nằm đúng chỗ
  placeholder (component tự giấu placeholder đi), lúc float thì placeholder hiện ra lặp lại nhãn.
- Chỉ giữ placeholder khi nó nói thêm điều nhãn không nói: `Gõ để tìm khách hàng...`,
  `dd/mm/yyyy`.
- Ô tìm nhanh vẫn giữ nguyên: `Tìm theo <các trường BE thực sự lọc>`. Cấm `Tất cả`, `Chọn...`.

**Bộ lọc ≤ 3 trường** chạy `isInlineMode` — dàn ngang cạnh ô tìm nhanh và **vẫn dùng nhãn
floating** như khối nâng cao (chốt 09/09/2026): nhãn lúc nghỉ nằm giữa ô nên không chiếm thêm dòng,
hàng vẫn thẳng trục; panel tự nâng ô tìm nhanh + ô lọc lên 36px. Hai chế độ vì thế nhìn giống hệt
nhau — trước đây chế độ gọn bỏ nhãn, cùng một màn mà bộ lọc gọn xấu hơn hẳn.

#### Ô "gõ để tìm từ server" — DÙNG `V2BaseSelectRemote`, cấm tự chế autocomplete

Lọc theo Khách hàng / NCC / Sản phẩm... (danh sách quá lớn không nạp hết được):

```vue
<template #field-customer_id>
  <V2BaseSelectRemote
      v-model="filters.customer_id"
      :fetchFn="fetchCustomers"
      :initialOption="customerInitialOption"
      :minimumInputLength="2"
      placeholder="Gõ để tìm khách hàng..."
      size="sm"
      height="36px"
      @select="onCustomerSelected"
  />
</template>
```

| Bắt buộc | Vì sao |
|---|---|
| `height="36px"` khi nằm trong ô floating | `updateHeight()` ghi inline `!important`, CSS ngoài KHÔNG đè nổi → thiếu là ô lùn 32px lệch hàng |
| `minimumInputLength` (thường 2) | select2 hiện "Vui lòng nhập thêm N ký tự" thay vì báo "không có dữ liệu" khi user chưa gõ gì |
| `initialOption` | localStorage chỉ lưu được `id`; thiếu cái này thì F5 xong ô hiện **rỗng** dù bộ lọc vẫn đang chạy |
| `@select` lưu lại `text` | để dựng `initialOption` cho lần sau. Trả `null` khi user bấm × |

❌ **Cấm** tự viết khối `v-if="showList"` + `@focus="showList = true"` + mảng `filteredXxx`.
Đã dính thật ở màn Dự án TKT: chưa gõ gì đã hiện "Không tìm thấy khách hàng", và dropdown thứ 2
quên `position: absolute` nên đẩy vỡ layout.

#### ⚠️ Sửa CSS cho ô lọc: thắng bằng SPECIFICITY, `!important` KHÔNG đủ

`V2BaseSelect` / `V2BaseDatePicker` đặt sẵn nhiều rule `!important` cho ô 32px. Rule của
`V2BaseFloatingField` mà chỉ **bằng điểm** thì thắng thua do **thứ tự nguồn** — mà thứ tự nguồn
giữa dev (Nuxt nhét CSS theo từng component) và bản **build** (gộp CSS) **KHÁC NHAU**.

→ Triệu chứng kinh điển: **local đúng, lên dev/prod sai**. Đã dính 3 lần liên tiếp:

| Triệu chứng | Rule thua | Kẻ thắng |
|---|---|---|
| Placeholder lòi ra đè lên nhãn nghỉ (chỉ trên bản build) | `.ff:not(.is-float) .ff__control .select2-selection__placeholder` (4) | `.v2-select ... .select2-selection__placeholder` (4) |
| Chữ trong select lệch lên 3.4px | `.ff .ff__control .select2-selection__rendered` (3) | `div.v2-select.v2-select--sm ... __rendered` (4+1) |
| Ô select lùn 32px | CSS thường | **inline** `!important` của `updateHeight()` → phải dùng prop `height` |

**Cách kiểm chứng bắt buộc** trước khi báo xong: nhét rule mới vào **đầu `<head>`** — vị trí bất lợi
nhất về thứ tự nguồn — rồi đo `getComputedStyle`. Vẫn thắng thì mới chắc không vỡ trên bản build.

```js
// chạy trong console / browser_evaluate
const s = document.createElement('style')
s.textContent = '<rule mới>'
document.head.insertBefore(s, document.head.firstChild)
getComputedStyle(document.querySelector('.ff .select2-selection__rendered')).lineHeight
```

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
