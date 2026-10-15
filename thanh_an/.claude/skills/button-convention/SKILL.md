---
name: button-convention
description: Use when tạo/sửa NÚT BẤM trên FE hrm-thanhan-client — toolbar danh sách, cột Hành động/Thao tác, footer modal, form page. Phần A cho màn V2 (V2BaseButton / V2BaseRowActions — màn mới và phân hệ Cung ứng đang chuyển sang V2), Phần B cho màn CŨ còn dùng b-button + bánh răng. Đọc cả khi: nút ghi dữ liệu thiếu lớp tải, nút duyệt không hỏi xác nhận, :disabled trên V2BaseButton không ăn.
---

# Button Convention — HRM Thành An (dns)

Port từ skill `button-convention` của hrm (28/09/2026), đã chỉnh cho khác biệt của dns.

## Chọn phần nào?

| Màn đang làm | Đọc phần |
|---|---|
| Màn **mới**, hoặc màn đang **chuyển sang V2** (có `<div class="v2-styles">`, dùng `V2Base*`) | **Phần A** |
| Màn **cũ** còn `b-table` + `b-button` + bánh răng `fa fa-cog`, chưa có kế hoạch chuyển | **Phần B** |

KHÔNG trộn 2 chuẩn trên cùng một màn: màn đã lên V2 thì mọi nút theo Phần A.
Màn cũ đang chạy ổn thì chỉ sửa theo Phần B, không tự "nâng" sang V2 khi user chưa yêu cầu.

## Khác biệt dns so với hrm (đọc trước khi copy code từ hrm)

| hrm | dns |
|---|---|
| `this.$safeLoadingStart()` / `$safeLoadingFinish()` (plugin `safe-loading.js`) | **CHƯA có** → dùng `this.$nuxt?.$loading?.start?.()` / `finish?.()` (xem A6b) |
| `await this.$confirm({...})` (plugin `confirm-dialog.js`) | **CHƯA có** → đặt thẻ `<BaseConfirmModal :id="...">` trong template (xem A6c) |
| Remixicon bản mới | **Remixicon 2.4.0** — icon ra đời sau bản 2.4 sẽ hiện **ô trống**; icon lạ thì grep `.ri-<tên>:before` trong `assets/scss/custom/plugins/icons/_remixicon.scss` trước khi dùng (mọi icon trong bảng A3 đã kiểm có đủ) |
| Danh mục có `CatalogHistoryModal` / `catalog_histories` | **Không có** → nút "Lịch sử" chỉ thêm khi màn đã có nguồn lịch sử (log duyệt, `HistoryApproveModal`…) — không có thì bỏ, đừng dựng nút chết |

---

# PHẦN A — Màn V2 (`V2BaseButton`, `V2BaseIconButton`, `V2BaseRowActions`)

## A1. Nguyên tắc chung

- **Mọi `V2BaseButton` đều PHẢI có icon** qua slot `#prefix` (nút chỉ có icon thì dùng `V2BaseIconButton`)
- **Luôn khai `size`** — mặc định `size="sm"`
- **KHÔNG dùng `type="primary"`** — dùng prop `primary` / `secondary` / `tertiary` trực tiếp
- Icon dùng **Remix Icon** (`ri-*`) là chính; `fas fa-*` chỉ khi Remix không có icon phù hợp
- Khoá nút bằng **`:interactable="!submitting"`**, KHÔNG dùng `:disabled` (xem A6b)

## A2. Variant theo nhóm hành động

| Nhóm hành động | Variant | Ví dụ |
|---|---|---|
| **Action chính** | `primary` | Tạo mới, Lưu, Xác nhận, Duyệt, Chọn, In |
| **Action phụ** | `secondary` | Lưu và tiếp tục, Xuất Excel, Import Excel, Cấu hình cột. Màu theo `status` (A2b) |
| **Thoát / Hủy** | `tertiary` | Đóng, Hủy, Quay lại |
| **Reset / Phụ trợ** | `tertiary` | Làm mới, Xóa trắng, Xem thêm |
| **Nguy hiểm** | `primary` + `status="danger"` | Xóa, Từ chối, Hủy duyệt |
| **Nhẹ (ngoài page)** | `light` | Chỉ nút phụ ngoài page — **KHÔNG dùng trong modal footer** |

## A2b. Màu (`status`)

`variant` quyết định độ nổi, `status` quyết định màu: `info` (mặc định) · `success` · `warning` · `danger`.

| Hành động | Khai báo |
|---|---|
| Tạo mới · Lưu · Lưu nháp | `primary` (teal `#1abc9c`) |
| **Duyệt · Gửi duyệt · Hoàn thành · Kích hoạt** | `primary` — **KHÔNG thêm `status`** (teal, trùng màu nút Duyệt của `V2Footer`) |
| **Import Excel** | `secondary status="warning"` (cam) |
| **Xuất Excel / CSV / PDF** | `secondary status="success"` (xanh lá) — cả nhóm xuất **cùng một màu** |
| Khóa · Cảnh báo | `primary status="warning"` |
| Mở khóa · Khôi phục | `primary status="success"` |
| Xóa · Từ chối · Hủy duyệt | `primary status="danger"` |
| In · Cấu hình cột · Làm mới | `secondary` / `tertiary` |
| Đóng · Hủy · Quay lại | `tertiary` |

- Không dùng `danger` cho thao tác vô hại (xóa điều kiện lọc, đóng popup) — đỏ chỉ cho việc phá huỷ.
- Nút đổi trạng thái phải **đổi màu theo trạng thái**: `:status="isActive ? 'warning' : 'success'"`.
  Trong cột hành động (`V2BaseIconButton` chỉ có `danger` boolean) thì Khóa/Mở khóa để trung tính.

## A3. Icon theo hành động

| Hành động | Icon |
|---|---|
| Tạo mới | `ri-add-line` |
| Lưu / Lưu và tiếp tục | `ri-save-3-line` |
| Sửa | `ri-edit-line` |
| Xóa | `ri-delete-bin-line` |
| Đóng / Hủy / Quay lại | `fas fa-arrow-left` |
| Xác nhận / Duyệt | `ri-check-line` |
| Từ chối | `ri-close-circle-line` |
| Gửi / Gửi duyệt | `ri-send-plane-line` |
| Xuất Excel | `ri-file-excel-2-line` |
| Xuất CSV / Xuất PDF | `ri-file-text-line` / `ri-file-pdf-line` |
| Xuất (chỉ 1 nút chung) | `ri-download-line` |
| Import Excel | `ri-upload-line` |
| In | `ri-printer-line` |
| Tìm kiếm | `ri-search-line` |
| Làm mới | `ri-refresh-line` |
| Xóa trắng | `ri-eraser-line` |
| Lịch sử | `ri-history-line` |
| Khóa / Mở khóa | `ri-lock-line` / `ri-lock-unlock-line` |
| Hành động khác (⋮) | `ri-more-2-fill` — 3 chấm DỌC, không dùng `ri-more-fill` |
| Cấu hình cột hiển thị | `ri-layout-column-line` |
| Cài đặt chung | `ri-settings-3-line` |
| Nhân bản | `ri-file-copy-line` |
| Chọn | `ri-checkbox-circle-line` |
| Xem chi tiết | `ri-eye-line` (chỉ dùng trong ⋮ khi thật cần — danh sách V2 không có nút Xem) |

## A4. Text chuẩn

- Dấu kiểu mới: **Xóa, Hủy, Khóa** (không `Xoá, Huỷ, Khoá`). Viết hoa chữ đầu. Viết `và`, không `&`.
- Tối đa 3 từ; giải thích dài đưa vào `title`. Nút chỉ icon: `title` = đúng chữ chuẩn.
- Nêu rõ đối tượng khi chữ trần mơ hồ: `Import Excel`, `Tải file mẫu`. Ngữ cảnh đã rõ thì `Tạo mới`,
  không viết `Tạo đơn mua hàng mới`.

| Hành động | Text chuẩn | KHÔNG dùng |
|---|---|---|
| Tạo bản ghi | **Tạo mới** | Thêm mới, Thêm, Tạo |
| Thêm dòng trong bảng form | **Thêm dòng** | Thêm hàng, Thêm mới dòng |
| Lưu / Lưu nháp | **Lưu** / **Lưu nháp** | Lưu lại, Cập nhật, Lưu tạm |
| Lưu và ở lại | **Lưu và tiếp tục** | Lưu & Tiếp tục |
| Sửa / Xóa | **Sửa** / **Xóa** | Chỉnh sửa, Xoá |
| Mở chi tiết | *(không có nút — mã bản ghi là link)* | Xem, Chi tiết |
| Lịch sử | **Lịch sử** | Xem lịch sử, Log |
| Nhân bản | **Nhân bản** | Sao chép, Copy |
| Duyệt / Từ chối | **Duyệt** / **Từ chối** | Phê duyệt, Không duyệt |
| Gửi duyệt | **Gửi duyệt** | Trình duyệt, Trình ký |
| Trong modal | **Xác nhận** / **Hủy** / **Đóng** | Đồng ý, OK, Thoát |
| Quay lại trang trước | **Quay lại** | Trở về |
| Tìm / reset lọc | **Tìm kiếm** / **Làm mới** | Lọc, Reset, Bỏ lọc |
| Import / file mẫu | **Import Excel** / **Tải file mẫu** | Nhập file, Tải mẫu |
| Xuất | **Xuất Excel** / **Xuất CSV** / **Xuất PDF** | Export, Xuất file |
| In | **In danh sách** / **In** (1 bản ghi) | Print, In phiếu |
| Icon-only | `title="Cấu hình cột hiển thị"` · `title="Hành động khác"` | Cài đặt cột, More |

## A5. Thứ tự hiển thị

**Modal footer (trái → phải):** Lưu nháp (nếu có, luôn đầu) → Action chính → Action phụ → Nguy hiểm → Reset → **Đóng (luôn cuối)**.
Modal có cả Xóa + Lưu: **Lưu → Xóa → Đóng**. Modal chỉ xem: chỉ **Đóng**. Modal xác nhận xóa: **Xóa → Hủy**.

**Toolbar danh sách:** **Tạo mới → Import Excel → Xuất Excel → Cấu hình cột** (icon-only).

**Form page:** Lưu nháp (nếu có) → Lưu / Gửi duyệt / In → Action phụ → Quay lại.

**Cột Hành động của bảng** (chi tiết: skill `list-page` mục 2):
- Dựng bằng `V2BaseRowActions` — không tự xếp `V2BaseIconButton`.
- **KHÔNG có nút Xem**: mã bản ghi ở cột đầu là `nuxt-link`.
- **KHÔNG có "Hủy phiếu" / "Không duyệt"** ở danh sách (cần modal nhập lý do → để ở màn chi tiết).
  "Duyệt" ở danh sách chỉ **điều hướng** sang màn chi tiết.
- Thứ tự: **Sửa → Xóa (hoặc Khóa/Mở khóa) → ⋮** gom phần còn lại. Tối đa 3 nút/dòng.
- Nút không dùng được với dòng đó → **ẩn** (`visible: false`), không disable.

## A6. Cú pháp

```vue
<V2BaseButton primary size="sm" :interactable="!submitting" @click="save">
    <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
    Lưu
</V2BaseButton>

<V2BaseButton secondary status="success" size="sm" @click="openExportModal('excel')">
    <template #prefix><i class="ri-file-excel-2-line" style="font-size: 15px"></i></template>
    Xuất Excel
</V2BaseButton>

<V2BaseButton tertiary size="sm" @click="close">
    <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
    Đóng
</V2BaseButton>

<V2BaseIconButton title="Cấu hình cột hiển thị" @click="openColumnModal">
    <i class="ri-layout-column-line"></i>
</V2BaseIconButton>
```

## A6b. Nút gọi API GHI dữ liệu — BẮT BUỘC có lớp tải + chống bấm 2 lần

Mọi nút POST/PUT/DELETE (Lưu, Xóa, Duyệt, Khóa, Gửi duyệt, Import…) phải bật lớp tải; không có thì
user tưởng nút hỏng và bấm lại → bản ghi trùng.

dns **chưa có** `$safeLoadingStart()` (port plugin là việc dùng chung — hỏi user trước, câu Q3 trong
`.plans/ui-v2-cung-ung/plan.md`). Tạm thời dùng `$nuxt.$loading` **kèm optional chaining** — lúc F5,
`$nuxt.$loading` có thể chưa tồn tại, gọi trần sẽ ném lỗi và nuốt luôn lệnh lưu:

```js
async submit() {
    if (this.submitting) return
    try {
        this.submitting = true
        this.$nuxt?.$loading?.start?.()          // NGAY TRƯỚC lệnh gọi
        await this.$store.dispatch('apiPostMethod', { url: '...', payload: { ... } })
        this.$toasted.global.success({ message: 'Lưu thành công' })
        this.$router.push('/supply/...')          // lưu/duyệt xong quay về danh sách
    } catch (error) {
        // map 422 vào formError — skill form-validate
    } finally {
        this.submitting = false
        this.$nuxt?.$loading?.finish?.()         // LUÔN ở finally
    }
}
```

- `finish()` đặt trong **`finally`**, không đặt cuối `try`.
- Khoá nút bằng **`:interactable="!submitting"`**. `V2BaseButton` không có prop `disabled` — truyền
  `:disabled` là rơi vào `$attrs` rồi bị ghi đè, **nút vẫn bấm được** (lỗi im lặng).
- Chỉ áp cho lệnh **ghi**. Lệnh đọc (GET danh sách, options select) dùng `loading` của bảng, không bật lớp tải toàn trang.
- Store `apiPostMethod` / `apiPutMethod` / `apiDeleteMethod` **không** tự bật lớp tải → màn tự gọi.

## A6c. Nút ĐỔI TRẠNG THÁI — BẮT BUỘC hỏi xác nhận, hỏi TRƯỚC lớp tải

| Nhóm | Ví dụ | Hỏi? |
|---|---|---|
| Duyệt theo cấp / chuyển cấp trên | Duyệt · Trưởng phòng duyệt · Chuyển duyệt BGĐ | ✅ |
| Gửi duyệt | Gửi duyệt · Lưu và gửi duyệt · Lưu và duyệt | ✅ |
| Phủ quyết | Không duyệt · Từ chối · Hủy phiếu | ✅ — popup **nhập lý do** (`V2BaseRejectApproveModal` / `BaseConfirmModal show-input`) đã tính là hỏi |
| Chốt / hoàn thành | Hoàn thành · Khóa | ✅ |
| Xóa | Xóa | ✅ (`:danger="true"`) |
| Chỉ điều hướng | "Duyệt" ở cột hành động danh sách (mở màn chi tiết) | ❌ |
| Lệnh đọc | In · Xuất Excel · Làm mới | ❌ |

dns **chưa có** `$confirm()` → đặt `BaseConfirmModal` trong template, **id riêng cho từng màn**:

```vue
<BaseConfirmModal
    id="confirm-approve-purchase-order"
    title="Xác nhận duyệt"
    :message="approveMessage"
    text-accept="Duyệt"
    :danger="false"
    @event="doApprove"
/>
```

```js
askApprove() {
    if (this.submitting) return
    this.approveMessage = `Duyệt đơn mua hàng "${this.form.code}"? Đơn sẽ được chuyển sang bước tiếp theo.`
    this.$bvModal.show('confirm-approve-purchase-order')   // 1. hỏi trước
},
async doApprove() {
    try {
        this.submitting = true
        this.$nuxt?.$loading?.start?.()                     // 2. rồi mới bật lớp tải
        await this.$store.dispatch('apiPostMethod', { url: '...', payload: {} })
    } finally {
        this.submitting = false
        this.$nuxt?.$loading?.finish?.()
    }
},
```

- Câu hỏi phải **gọi tên phiếu + nói hệ quả**, không hỏi trống "Bạn có chắc không?".
- `text-accept` = **đúng chữ trên nút gốc** (Duyệt / Gửi duyệt / Xóa).
- Nhóm duyệt/gửi duyệt **không** `danger`; `danger` chỉ cho Từ chối · Hủy phiếu · Xóa.
  (`base-confirm-modal` của dns tự suy `danger` theo `textAccept` khi để `null` — khai tường minh cho chắc.)

⚠️ **Luôn khai `id` riêng cho `BaseConfirmModal`**: id mặc định là `confirm`. (Từ 06/10/2026 `V2Footer`
đã dùng id riêng `v2-footer-confirm-<uid>` nên không còn trùng với nó, nhưng 2 `BaseConfirmModal` không
khai id trên cùng màn vẫn bật cùng lúc.)

⚠️ **`V2Footer` đã hỏi sẵn cho các cờ**: `approve` · `forward_director_approve` · `boardDirectorApprove` ·
`save_and_submit_approve` · `save_and_approve` · `send_and_submit_form` — màn dùng các cờ này **không
hỏi thêm lần 2**. Các cờ `complete` · `delete` · `cancel` · `print` emit thẳng → màn phải tự hỏi.
Nút tự dựng ở slot `#custom-actions` cũng phải tự hỏi.

- Truyền **`:confirm-message`** cho `V2Footer` để câu hỏi nêu tên phiếu + hệ quả (nhận HTML → escape
  dữ liệu người dùng). Không truyền thì ra câu chung chung "Bạn xác nhận duyệt phiếu?". Chữ nút đồng ý
  tự lấy theo nút gốc (Duyệt / Gửi duyệt…).
- Cờ `reject_approve` ghi **"Từ chối"** và emit `rejectApprove` → màn mở `V2BaseRejectApproveModal`
  (id riêng; popup đó trả `{ form, setErrors, setLoading, close }` qua `@confirm`). Mẫu:
  `pages/supply/purchase_orders/_id/index.vue`.

## A7. Checklist (màn V2)

- [ ] Mọi `V2BaseButton` có icon `#prefix`, có `size="sm"`, dùng prop `primary/secondary/tertiary`
- [ ] Variant + `status` đúng A2/A2b; nhóm Xuất cùng một màu xanh lá, Import cam
- [ ] Chữ đúng bảng A4 (Xóa/Hủy/Khóa; Import Excel; Tạo mới)
- [ ] Thứ tự đúng A5; Đóng luôn cuối modal footer
- [ ] Cột hành động dùng `V2BaseRowActions`: Sửa → Xóa/Khóa → ⋮, không có Xem / Hủy phiếu / Không duyệt, nút không dùng được thì ẩn
- [ ] Nút ghi dữ liệu: `$nuxt?.$loading?.start?.()` trước lệnh gọi, `finish` trong `finally`, khoá bằng `:interactable`
- [ ] Nút đổi trạng thái: có `BaseConfirmModal` (id riêng), hỏi TRƯỚC lớp tải, câu hỏi nêu tên phiếu + hệ quả, `text-accept` đúng chữ nút
- [ ] Không hỏi 2 lần với cờ `V2Footer` đã hỏi sẵn
- [ ] Icon lạ đã grep trong `assets/scss/custom/plugins/icons/_remixicon.scss` (bản 2.4.0) — không ra ô trống

---

# PHẦN B — Màn CŨ (`b-table` + `b-button` + bánh răng)

> Chuẩn cũ, chốt 18/09/2026. Áp cho màn **chưa** chuyển sang V2. Khi một màn được chuyển sang V2
> (vd Danh sách Đơn mua hàng — thí điểm 28/09/2026), bỏ phần này và làm theo Phần A.

## B0. Khi nào dùng
- Thêm / bớt / sắp xếp lại nút trong cột **Thao tác** của màn danh sách cũ (`<b-table>`), kể cả khi chỉ thêm 1 nút
- Sửa màn cũ mà user chưa yêu cầu chuyển V2

## B1. Cột "Thao tác" của màn danh sách (màn CŨ)

### Quy tắc (chuẩn theo màn `pages/contract/contract/index.vue`)

Đếm số nút **thực sự hiển thị** của **từng dòng** (đã lọc theo trạng thái +
quyền), không đếm số nút khai trong template:

| Số nút của dòng | Cách hiển thị |
|---|---|
| ≤ 3 | Hiện hết ra ngoài, không có bánh răng |
| > 3 | Hiện **2 nút đầu**, toàn bộ phần còn lại vào dropdown **bánh răng** (`fa fa-cog`) |

- Đếm theo **từng dòng**: cùng một bảng, dòng này 2 nút (không bánh răng),
  dòng kia 4 nút (có bánh răng) là đúng.
- Thứ tự ưu tiên: nút hay dùng / nút chính đứng trước để luôn nằm ngoài.
  Chuẩn đang dùng ở phân hệ Cung ứng: **`Xem` → nút nghiệp vụ chính (`Duyệt`,
  `Từ chối`, `Gửi`, `Thu hồi`) → `Sửa` → `Xóa`**. Nhờ vậy dòng 4 nút luôn để
  `Xem` + nút nghiệp vụ ra ngoài, `Sửa`/`Xóa` rơi vào bánh răng.
- Nút trong bánh răng hiển thị **chữ** (kèm `<i class="fa fa-angle-right">`),
  nút ngoài hiển thị **icon + tooltip**.

### Cách làm

Không viết `v-if` rải rác trong template nữa — khai danh sách nút trong
`methods`, template chỉ lặp.

**1. Khai icon + ngưỡng ở đầu `<script>`**

```js
// url-loader có thể trả module ES (có .default) hoặc chuỗi URL — nhận cả hai.
const assetUrl = (m) => (m && m.default) || m
const ICON = {
    eye: assetUrl(require('@/assets/images/file-icons/eyes.svg')),
    plus: assetUrl(require('@/assets/images/file-icons/plus_black.svg')),
}

// Quy tắc chung cột Thao tác: <= 3 nút hiện hết, > 3 nút thì 2 nút đầu để ngoài,
// phần còn lại gom vào dropdown bánh răng.
const MAX_INLINE_ACTIONS = 3
const KEEP_INLINE_ACTIONS = 2
```

**2. `methods` — 1 hàm dựng danh sách + 2 hàm chia**

```js
// Danh sách nút thao tác của 1 dòng, đã lọc theo trạng thái + quyền.
rowActions(item) {
    const actions = [
        { key: 'view', label: 'Xem', img: ICON.eye, handler: () => this.onViewClick(item) },
    ]
    if (item.can_edit) {
        actions.push({ key: 'edit', label: 'Sửa', img: ICON.pen, handler: () => this.onEditClick(item) })
    }
    if (item.can_reject) {
        actions.push({
            key: 'reject',
            label: 'Từ chối',
            icon: 'mdi mdi-close-circle-outline text-danger',
            handler: () => this.onRejectClick(item),
        })
    }
    return actions
},
inlineActions(item) {
    const actions = this.rowActions(item)
    return actions.length <= MAX_INLINE_ACTIONS ? actions : actions.slice(0, KEEP_INLINE_ACTIONS)
},
moreActions(item) {
    const actions = this.rowActions(item)
    return actions.length <= MAX_INLINE_ACTIONS ? [] : actions.slice(KEEP_INLINE_ACTIONS)
},
```

Mỗi phần tử: `key` (unique, dùng cho `:key`), `label` (tooltip khi ở ngoài /
chữ khi vào bánh răng), **`img`** (SVG trong `assets/images/file-icons`) *hoặc*
**`icon`** (class `mdi`/`fa`), và **`handler`** (arrow function để giữ `this`)
*hoặc* **`to`** (đường dẫn — `b-button`/`b-dropdown-item` tự render router-link,
giữ được ctrl+click mở tab mới).

**3. Template**

```vue
<!--
    Cột Thao tác theo quy tắc chung (xem màn contract/contract):
    <= 3 nút thì hiện hết, > 3 nút thì hiện 2 nút đầu, phần còn lại
    gom vào dropdown bánh răng.
-->
<template v-slot:cell(actions)="{ item }">
    <div class="action-cell">
        <b-button
            v-for="a in inlineActions(item)"
            :key="a.key"
            :to="a.to"
            variant="secondary"
            class="btn-small"
            v-b-tooltip.hover.top="a.label"
            @click="a.handler && a.handler()"
        >
            <img v-if="a.img" :src="a.img" />
            <i v-else :class="a.icon"></i>
        </b-button>
        <b-dropdown v-if="moreActions(item).length" right size="sm" variant="link" toggle-class="p-0">
            <template #button-content>
                <button class="btn btn-primary btn-sm" type="button">
                    <i class="fa fa-cog"></i>
                </button>
            </template>
            <b-dropdown-item
                v-for="a in moreActions(item)"
                :key="a.key"
                :to="a.to"
                @click="a.handler && a.handler()"
            >
                <i class="fa fa-angle-right"></i> {{ a.label }}
            </b-dropdown-item>
        </b-dropdown>
    </div>
</template>
```

**4. SCSS — giãn cách nút + đồng bộ kích thước icon**

Các nút sinh bằng `v-for` nằm sát nhau (không có khoảng trắng HTML như khi
viết tay từng nút) → **bắt buộc** có `gap`, nếu không nút dính liền nhau.

```scss
// Cột Thao tác: các nút cách nhau đều, không dính sát
.action-cell {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: nowrap;
    gap: 6px;
}
// Đồng bộ kích thước icon (nếu page trộn <img> và mdi)
.btn-small {
    img,
    .mdi {
        display: inline-block;
        width: 18px;
        height: 18px;
        font-size: 18px;
        line-height: 18px;
        text-align: center;
        vertical-align: middle;
    }
}
```

### Bẫy hay gặp

- **Đếm nhầm theo template thay vì theo dòng.** Nút có `v-if` theo quyền /
  trạng thái → phải dựng mảng rồi đếm `length`, không đếm bằng mắt.
- **`require()` SVG trả về module ES.** Nuxt 2 có chỗ trả chuỗi, có chỗ trả
  `{ default }` → luôn bọc `assetUrl()`, nếu không `<img>` ra `[object Module]`.
- **Quên `variant="secondary"`.** Bootstrap-Vue mặc định đã là `secondary`
  nhưng khai rõ cho đồng bộ với các màn cũ.
- **Handler dùng `function () {}`** → mất `this`. Luôn dùng arrow function.
- **KHÔNG dùng `text-secondary` cho icon.** Theme này đặt `$secondary: $white`
  nên `text-secondary` = **chữ trắng**, trong khi `.btn-secondary` nền
  `#e5f1fe` → icon tàng hình. Icon `mdi`/`fa` cứ để **không class màu** cho ăn
  theo màu chữ của nút (`#0070f4`); chỉ thêm màu khi muốn cảnh báo
  (`text-danger` cho Xóa / Từ chối).
- **Chèn trùng khối `.btn-small`.** Nhiều màn đã có sẵn khối SCSS này ở cuối
  `<style>` — kiểm tra trước khi thêm, tránh khai 2 lần trong cùng file.
- **Nút sinh bằng `v-for` dính sát nhau.** Vue không chèn khoảng trắng giữa
  các node của `v-for` → phải cho container `display: flex; gap: 6px`.
- **Đưa nút nguy hiểm ra ngoài.** Nút nghiệp vụ chính (Xem / Sửa / Duyệt /
  Tạo phiếu) ưu tiên nằm ngoài; Xóa, Lịch sử, Xuất excel… đẩy vào bánh răng.

### Màn tham chiếu

- `pages/contract/contract/index.vue` — bản gốc của quy tắc (nút ngoài + bánh răng 4 mục)
- `pages/supply/supply_proposals/inbox.vue` — bản dùng mảng `rowActions()` động
- Toàn bộ phân hệ Cung ứng đã chuẩn hóa theo mẫu này (18/09/2026):
  `supply/contract_render`, `supply/purchase_contracts`, `supply/purchase_orders`,
  `supply/supply_handlings`, `supply/supply_proposals/index` + `inbox`
