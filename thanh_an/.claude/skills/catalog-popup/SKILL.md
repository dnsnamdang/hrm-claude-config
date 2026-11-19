---
name: catalog-popup
description: Use when làm POPUP Tạo mới / Sửa / Xem của màn DANH MỤC ở hrm-thanhan-client (dns) — danh mục không có route chi tiết, mọi thao tác nằm trong 1 popup (kho vật lý, kho kế toán, đơn vị tính, nhóm hàng…). Port từ khuôn popup danh mục của hrm (AddProductNatureModal). Đọc cả khi: bấm mã ở danh sách không mở được popup Xem, popup mở ra trống rồi mới đổ dữ liệu, form còn dữ liệu cũ từ lần mở trước, ô Trạng thái cho chọn Khóa dù danh sách đang ẩn nút Khóa, thiếu nút Lưu và tiếp tục.
---

# Popup màn danh mục — dns (hrm-thanhan-client)

> Bản dns của khuôn popup danh mục bên hrm: `hrm-client/pages/master-data/product-natures/AddProductNatureModal.vue`
> + `index.vue`, skill hrm `list-page` mục 3a và `modal-popup` mục 0/3c.
>
> Skill này lo **luồng 3 chế độ của popup danh mục và cách màn danh sách gọi nó**. Đọc kèm:
> `modal-popup` (khuôn `V2BaseModal`, `BaseConfirmModal`) · `form-validate` (`formValidateMixin`, lỗi 422) ·
> `select-and-input-state` (🔒, ô disabled, nhãn nhân viên) · `button-convention` A (nút footer) ·
> `list-page` A (màn danh sách chứa popup).

## 0. Khi nào áp

Màn danh mục **không có route `/{id}`**: Tạo mới / Sửa / Xem đều diễn ra trong popup. Danh mục có màn
chi tiết thật (`pages/.../_id/index.vue`) thì mã là `nuxt-link` như `list-page` A6, **không** dùng skill này.

## 0a. Khác biệt dns so với hrm

| hrm | dns | Làm gì ở dns |
| --- | --- | --- |
| Khối `SystemInfoSection` (Lịch sử) cuối popup Xem, bảng `catalog_histories` | **Không có** | Popup Xem chỉ có các trường nghiệp vụ. **Không** dựng dòng `Người tạo / Ngày tạo` ở đáy body thay thế — cột Người tạo/Ngày tạo đã có ở danh sách |
| Hành động "Lịch sử" ở menu ⋮ (`CatalogHistoryModal`) | **Không có** | Bỏ, không dựng nút chết |
| `ApiErrorHandler` + `formError` + `firstError()` tự viết | `formValidateMixin` | `validateForm` · `fieldError` · `hasFieldError` · `clearFieldError` · `resetValidation` · `applyServerErrors` + `<V2BaseError>` |
| `$nuxt.$loading.start()` gọi trần | `$nuxt?.$loading?.start?.()` | `finish?.()` đặt trong `finally` |
| Màn cha giữ `isShow` + `editItem`, truyền prop rồi gọi `loadItemData()` qua `ref` | Popup tự có method **`open({ id, view })`** | Một lệnh duy nhất từ màn cha, không đua prop với `$nextTick` (mục 2) |
| `:disabled="isSubmitSave"` trên `V2BaseButton` | `:interactable="!submitting"` | `V2BaseButton` dns không có prop `disabled` — truyền vào là nút **vẫn bấm được** |

## 1. MỘT popup cho cả 3 chế độ

- Một file `pages/<phân hệ>/<màn>/components/<Tên>FormModal.vue` lo **Tạo mới · Sửa · Xem**. Không tách
  popup Xem riêng — 2 file là 2 bộ trường lệch nhau sau vài lần sửa.
- Chế độ suy từ 2 state nội bộ: `recordId` (null = tạo mới) và `isView`.

| Chế độ | Mở từ | Tiêu đề | Ô nhập | Footer |
| --- | --- | --- | --- | --- |
| **Tạo mới** | nút toolbar **Tạo mới** | `Tạo mới <danh mục>` | sửa được, nhãn bắt buộc có `*` | **Lưu → Lưu và tiếp tục → Đóng** |
| **Sửa** | hành động **Sửa** ở cột Hành động | `Sửa <danh mục>: <MÃ>` | sửa được, có `*` | **Lưu → Đóng** |
| **Xem** | bấm **Mã** (cột định danh) | `Xem chi tiết <danh mục>: <MÃ>` | **tất cả `disabled`**, **không** `*` | **Đóng** |

- Tiêu đề viết thường sau chữ đầu, ghép mã vào **chính tiêu đề** (`V2BaseModal` không render `subtitle`).
  Chưa tải xong mã thì bỏ phần `: <MÃ>`, không in `: undefined`.
- **Icon: một icon theo chủ đề danh mục, giữ nguyên ở cả 3 chế độ** (kho → `ri-store-2-line`, đơn vị tính →
  `ri-ruler-line`…). Không đổi icon theo chế độ — tiêu đề đã nói chế độ. Icon lạ thì grep trong
  `assets/scss/custom/plugins/icons/_remixicon.scss` (Remixicon 2.4.0).
- Popup Xem **không có nút Sửa** ở footer (giống hrm). Muốn sửa thì đóng, bấm Sửa ở danh sách.

## 2. Mở popup — tải chi tiết TRƯỚC, mở SAU

Popup mở ra trống rồi mới đổ dữ liệu là lỗi: user kịp gõ vào form trống, hoặc thấy trường nhảy. Bản ghi
bị xóa ở tab khác thì phải báo và **không mở**.

```js
// Trong popup
async open({ id = null, view = false } = {}) {
    if (this.submitting) return
    this.recordId = id
    this.isView = !!id && view
    this.form = emptyForm()
    this.originalCode = ''
    this.resetValidation()
    await this.loadOptions()                       // danh mục của ô chọn — nạp lười, chỉ lần đầu (mục 5)
    if (id && !(await this.loadDetail(id))) return // lỗi → KHÔNG mở
    this.$refs.modal.show()
},

async loadDetail(id) {
    try {
        const { data } = await this.$store.dispatch('apiGetMethod', `warehouse/warehouses/${id}`)
        const d = data || {}
        this.originalCode = d.code || ''
        this.form = { ...emptyForm(), name: d.name || '', code: d.code || '', status: Number(d.status), … }
        this.canLock = d.can_lock !== false
        return true
    } catch (error) {
        const status = Number(error?.response?.status)
        if (status === 403) return false
        if (status === 404) {
            this.$toasted?.global?.error?.({ message: 'Dữ liệu đã thay đổi, vui lòng tải lại' })
            this.$emit('saved')                    // bản ghi không còn → danh sách tải lại
            return false
        }
        this.$toasted?.global?.error?.({ message: error?.response?.data?.message || 'Lỗi khi tải dữ liệu' })
        return false
    }
},
```

```js
// Ở màn danh sách — một lệnh, không giữ isShow/editingId ở màn cha
openCreate() { this.$refs.formModal.open() },
openView(item) { this.$refs.formModal.open({ id: item.id, view: true }) },
openEdit(item) { this.$refs.formModal.open({ id: item.id }) },
```

- **Không** tải chi tiết trong `@show` của `V2BaseModal` — lúc đó popup đã hiện.
- Reset dữ liệu ở **một chỗ duy nhất**: đầu `open()`. `@hidden` chỉ dọn lỗi (`resetValidation()`), không
  phải chỗ thứ 2 reset form (hrm reset ở `onHidden` vì màn cha nắm state; dns popup tự nắm).
- Nút Đóng / nút × chỉ gọi `this.$refs.modal.close()`.

## 3. Thân popup

```vue
<V2BaseModal ref="modal" :modal-id="modalId" :title="modalTitle" icon="ri-store-2-line" no-enforce-focus @hidden="resetValidation">
    <div class="form-row">
        <div class="col-md-6 mb-2">
            <V2BaseLabel :required="!isView">Mã kho</V2BaseLabel>
            <V2BaseInput v-model.trim="form.code" :disabled="isView" :invalid="hasFieldError('code')" @input="clearFieldError('code')" />
            <V2BaseError :message="fieldError('code')" />
        </div>
        <div class="col-md-6 mb-2">
            <V2BaseLabel :required="!isView">Tên kho</V2BaseLabel>
            <V2BaseInput v-model="form.name" v-validate="'required|max:255'" name="name" data-vv-as="Tên kho"
                :disabled="isView" :invalid="hasFieldError('name')" @input="clearFieldError('name')" />
            <V2BaseError :message="fieldError('name')" />
        </div>
        <div class="col-md-6 mb-2">
            <V2BaseLabel :required="!isView">Trạng thái</V2BaseLabel>
            <V2BaseSelectInModal v-model="form.status" :options="statusOptions" :allowClear="false" hide-search
                :disabled="isView || statusLocked" :title="statusLocked ? statusLockedReason : ''" />
        </div>
        <!-- … trường nghiệp vụ … -->
        <div class="col-md-12 mb-2">
            <V2BaseLabel>Mô tả</V2BaseLabel>
            <V2BaseTextarea v-model="form.description" :rows="3" :disabled="isView" />
        </div>
    </div>
    <template #footer>…</template>
</V2BaseModal>
```

- Lưới `form-row` + `col-md-*` + `mb-2`. Thứ tự: **Mã → Tên → Trạng thái → trường nghiệp vụ → Mô tả (cuối, full dòng)**.
- Dấu `*` dùng `<V2BaseLabel :required="!isView">` — không viết `*` trần, ở chế độ Xem không hiện `*`.
- Chế độ Xem: **mọi** ô `:disabled="isView"` (kiểu khoá chuẩn `select-and-input-state` mục 3 — nền `#f1f5f9`,
  chữ `#475569`, không opacity). Không đổi sang `<span>` text — giữ đúng bố cục form để Xem/Sửa nhìn như nhau.
- Ô trống ở chế độ Xem để trống, không `—`.
- Ô chỉ có ý nghĩa lúc tạo (vd `Số nhà kho` sinh nhà kho con) → `v-if="!recordId"`, payload Sửa `delete` key đó.
- Checkbox dùng `V2BaseCheckbox` (boolean) — BE lưu 0/1 thì map qua computed get/set; tick làm ẩn trường
  khác thì setter dọn luôn giá trị + lỗi của trường bị ẩn.
- **Không** có khối Người tạo / Ngày tạo / Người cập nhật ở đáy body (mục 0a).

### 3a. Ô Trạng thái phải cùng luật với nút Khóa ở danh sách

Danh sách ẩn nút Khóa vì BE trả `can_lock = false` (vd kho vật lý còn kho kế toán đang hoạt động trỏ tới)
mà popup Sửa vẫn cho chọn "Khóa" là **lách luật qua popup**.

```js
computed: {
    // Đang Hoạt động mà BE không cho khóa → khoá ô; tạo mới thì luôn chọn được
    statusLocked() {
        return !!this.recordId && Number(this.originalStatus) === 1 && !this.canLock
    },
},
```

- Luật lấy từ **cùng cờ BE** danh sách đang dùng (`can_lock` / `can_unlock`), không tự viết lại ở FE.
- BE `update()` vẫn phải chặn — FE khoá ô chỉ để user không bị bất ngờ.
- Khoá ô thì cho `title` nói lý do ("Còn kho kế toán đang hoạt động trỏ tới kho này").

## 4. Lưu

```js
async submit(keepOpen = false) {
    if (this.submitting || this.isView) return
    if (!(await this.validateForm())) return
    try {
        this.submitting = true
        this.$nuxt?.$loading?.start?.()
        const payload = { ...this.form }
        if (this.recordId) {
            await this.$store.dispatch('apiPutMethod', { url: `…/${this.recordId}`, payload: { ...payload, id: this.recordId } })
        } else {
            await this.$store.dispatch('apiPostMethod', { url: '…', payload })
        }
        this.$toasted?.global?.success?.({ message: this.recordId ? 'Cập nhật kho vật lý thành công' : 'Tạo mới kho vật lý thành công' })
        this.$emit('saved')
        if (keepOpen) {
            // Lưu và tiếp tục — giữ popup, form trắng để nhập bản ghi kế tiếp
            this.form = emptyForm()
            this.resetValidation()
        } else {
            this.$refs.modal.close()
        }
    } catch (error) {
        if (Number(error?.response?.status) === 403) return
        if (!this.applyServerErrors(error)) {
            this.$toasted?.global?.error?.({ message: error?.response?.data?.message || 'Có lỗi xảy ra' })
        }
    } finally {
        this.submitting = false
        this.$nuxt?.$loading?.finish?.()
    }
},
```

```vue
<template #footer>
    <V2BaseButton v-if="!isView" primary size="sm" :interactable="!submitting" @click="submit(false)">
        <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
        Lưu
    </V2BaseButton>
    <V2BaseButton v-if="!isView && !recordId" secondary size="sm" :interactable="!submitting" @click="submit(true)">
        <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
        Lưu và tiếp tục
    </V2BaseButton>
    <V2BaseButton tertiary size="sm" @click="$refs.modal.close()">
        <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
        Đóng
    </V2BaseButton>
</template>
```

- FE chỉ `v-validate` các trường bắt buộc rõ ràng (Tên…); còn lại (trùng mã, ràng buộc chéo) để BE trả 422
  → `applyServerErrors` gắn lỗi dưới từng ô (`form-validate`).
- Toast: **"Tạo mới <danh mục> thành công"** / **"Cập nhật <danh mục> thành công"**.
- Sự kiện ra ngoài chỉ một: **`saved`** → màn danh sách `loadData()` (giữ trang hiện tại).
- "Lưu và tiếp tục" chỉ có ở Tạo mới, chữ đúng **"Lưu và tiếp tục"** (không `&`).

## 5. Ô chọn danh mục khác trong popup

- `V2BaseSelectInModal` + `no-enforce-focus` trên `V2BaseModal` (select2 mới gõ tìm được).
- Option nạp **lười** lần đầu `open()` rồi giữ lại; không gọi ở `mounted` của màn cha.
- Bản ghi đang trỏ tới option đã khoá → option vẫn hiện, gắn `is_locked: true` (🔒) — chỉ hiện khi đó là
  giá trị hiện tại (`select-and-input-state`). Tạo mới không thấy option đã khoá.
- Chọn option kéo theo điền trường khác (chọn kho vật lý → điền địa chỉ) thì chỉ điền khi trường đó đang trống
  hoặc user chưa sửa tay.
- Option nhân viên dùng `employeeOptionText` (`@/utils/employeeOptionText`).

## 6. Màn danh sách gọi popup

- Cột định danh **Mã** = `<button type="button" class="v2-cell-link field-line" @click="openView(item)">` →
  mở popup **Xem**. Cấm `<a href="javascript:void(0)">`. Bảng không có mã / có bản ghi trống mã → cột định
  danh là **Tên** (`list-page` A6).
- Cột Hành động (`V2BaseRowActions`): **Sửa → Xóa / Khóa / Mở khóa**, **không có "Xem"** (mã đã mở Xem),
  không có "Lịch sử" (dns chưa có nguồn). Nút không dùng được → `visible: false`.
- Toolbar: **Tạo mới** → `openCreate()`.
- Đặt popup một lần, có `ref`:

```vue
<WarehouseFormModal ref="formModal" @saved="loadData" />
```

- Xóa / Khóa / Mở khóa hỏi bằng `BaseConfirmModal` ở **màn danh sách** (id riêng, `button-convention` A6c),
  không đặt trong popup danh mục.

## 7. Checklist

- [ ] 1 file popup cho Tạo mới / Sửa / Xem, có method `open({ id, view })`
- [ ] Tiêu đề đúng bảng mục 1, ghép mã khi Sửa/Xem; 1 icon chủ đề cố định
- [ ] Tải chi tiết xong mới `show()`; 404 → toast "Dữ liệu đã thay đổi, vui lòng tải lại" + không mở + danh sách tải lại; 403 im lặng
- [ ] Mở lần 2 không còn dữ liệu / lỗi của lần trước (reset ở đầu `open()`)
- [ ] Chế độ Xem: mọi ô `disabled`, không `*`, footer chỉ Đóng
- [ ] Tạo mới có "Lưu và tiếp tục"; Sửa không có
- [ ] Ô Trạng thái khoá theo đúng cờ `can_lock`/`can_unlock` của danh sách
- [ ] Nút footer khoá bằng `:interactable="!submitting"`, lớp tải `$nuxt?.$loading` có `finish` trong `finally`
- [ ] 422 → lỗi dưới từng ô (`applyServerErrors`), không chỉ toast
- [ ] Không có dòng Người tạo / Ngày tạo ở đáy body, không khối Lịch sử
- [ ] Danh sách: Mã là `button.v2-cell-link` mở Xem, không có hành động "Xem"

Tự kiểm (chạy ở `hrm-thanhan-client`) — popup danh mục nào chưa có chế độ Xem:

```bash
grep -rL "isView" --include='*FormModal.vue' pages | xargs -r grep -l "V2BaseModal"
```

## 8. Màn đang theo khuôn này

Đạt đủ checklist mục 7 (09/11/2026) — dùng làm **mẫu dns** khi làm popup danh mục mới:

| Danh mục | Popup | Ghi chú |
| --- | --- | --- |
| Kho vật lý | `pages/warehouse/warehouses/components/WarehouseFormModal.vue` | Ô Trạng thái khoá theo `can_lock`; BE `WarehouseService::updateOrCreate` chặn cùng luật `toggleStatus`; `Số nhà kho` chỉ có lúc tạo |
| Kho kế toán | `pages/warehouse/accounting_warehouses/components/AccountingWarehouseFormModal.vue` | Không ràng buộc khoá → ô Trạng thái không khoá; option kho vật lý nạp lười (`loadOptions`); chọn kho chỉ điền địa chỉ khi ô trống / chưa sửa tay (`lastAutoAddress`) |

Màn nào làm xong theo khuôn thì ghi thêm vào bảng.
