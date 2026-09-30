---
name: modal-popup
description: Use when tạo/sửa MODAL / POPUP trên hrm-thanhan-client (dns) — popup thêm/sửa/xem danh mục, popup xác nhận, popup chọn bản ghi có bảng, bộ lọc trong popup. Chuẩn V2 port từ hrm - V2BaseModal, V2BaseSelectInModal, BaseConfirmModal. Đọc cả khi: footer popup bị đẩy khuất, 2 thanh cuộn lồng nhau, dropdown select2 bị modal che, nút mất icon từ lần mở thứ 2, popup có bảng chỉ thấy vài dòng.
---

# Modal / Popup — dns (hrm-thanhan-client)

> Bản dns của skill `modal-popup` bên hrm. Nút trong modal theo `button-convention` Phần A; skill
> này chỉ lo **cấu trúc popup**. Bộ lọc/bảng trong popup đọc thêm `list-page`.

## Khác biệt dns so với hrm

| hrm | dns |
| --- | --- |
| `this.$confirm({...})` trả Promise | **Không có** — chỉ dùng thẻ `<BaseConfirmModal>` trong template (mục 3) |
| `SystemInfoSection` (khối Lịch sử cuối popup Xem) + `CatalogHistoryModal` | **Không có** — popup Xem không bắt buộc khối Lịch sử; KHÔNG dựng lại dòng `Người tạo / Ngày tạo` ở đáy body |
| `V2BaseFilterPanel` (slot `#header-actions`, `inlineSearchButtons`) | **Không có** — bộ lọc trong popup dùng `V2BaseSmartFilterPanel` + prop `in-modal` |
| `$safeLoadingStart()` | `this.$nuxt?.$loading?.start?.()` / `finish?.()` trong `finally` |
| `ProductSearchModal` dùng chung | dns có popup chọn hàng riêng từng phân hệ — áp nguyên tắc mục 5 khi sửa |

Component đã có ở dns: `components/modal/V2BaseModal.vue`, `components/modal/base-confirm-modal.vue`,
`components/V2BaseSelectInModal.vue`, `components/V2BaseTableScroll.vue`, `components/modal/V2BaseRejectApproveModal.vue`.

---

## 1. Khuôn chung — `V2BaseModal`

**Popup MỚI dựng trên `V2BaseModal`**, không tự khai `b-modal` + header + footer.

```vue
<V2BaseModal
    ref="unitModal"
    modal-id="unit-modal"
    :title="isEdit ? `Sửa đơn vị tính: ${form.code}` : 'Thêm đơn vị tính'"
    icon="ri-ruler-line"
    @hidden="resetForm"
>
    <!-- nội dung -->
    <template #footer>
        <V2BaseButton primary size="sm" :interactable="!saving" @click="save">…Lưu</V2BaseButton>
        <V2BaseButton tertiary size="sm" @click="$refs.unitModal.close()">…Đóng</V2BaseButton>
    </template>
</V2BaseModal>
```

Props: `modalId` (bắt buộc) · `title` · `icon` · `iconColor` · `iconBackground` · `size` (mặc định
`lg`) · `dialogClass` · `maxBodyHeight` (mặc định `calc(100vh - 220px)`) · `noEnforceFocus`. Sự kiện
`show` · `shown` · `hide` · `hidden`. Method `show()` / `close()`.

Component đã chốt sẵn — **màn dùng không viết CSS đè**, muốn khác thì qua prop:

| Phần | Chuẩn |
| --- | --- |
| Header | icon tròn + tiêu đề 14px đậm + nút ×, **đúng 1 dòng** |
| Body | vùng cuộn riêng, `padding: 0.5rem 0.75rem`; tự triệt `margin-top` khối đầu / `margin-bottom` khối cuối |
| Footer | ngoài vùng cuộn + `position: sticky; bottom: 0` → luôn thấy nút. Không truyền slot `footer` → mặc định nút Đóng |

- **Không truyền `subtitle` / `subtitleLabel`** (prop giữ lại nhưng không render). Cần nói đang thao
  tác bản ghi nào → ghép vào tiêu đề: `Sửa nhà cung cấp: NCC001 - Công ty ABC`.
- Không dùng `no-close-on-backdrop` (trừ form đang nhập dài mà user đã yêu cầu chặn).
- Không có dòng `Người tạo: … • Ngày tạo: …` ở đáy body. Cần hiện thì làm trường readonly trong thân form.
- Popup CŨ tự dựng `b-modal`: chuyển sang `V2BaseModal` khi có dịp đụng vào, ưu tiên popup đang mất footer / thừa khoảng trắng.

### Popup cũ chưa chuyển được (trường hợp đặc biệt)

Giữ `b-modal` thì phải: `hide-footer` + `body-class` tắt cuộn ngoài + div cuộn riêng (KHÔNG đặt class
`modal-body`) + `<div class="modal-footer">` sticky ngoài vùng cuộn. Xem mục 4.

## 2. Select trong popup — `V2BaseSelectInModal`

Mọi dropdown trong modal dùng **`V2BaseSelectInModal`**, không dùng `V2BaseSelect` / `base-select2`:
nó đặt `dropdownParent` về `.modal-content` nên danh sách không bị lớp phủ che, focus ô tìm và
click-outside đúng.

```vue
<V2BaseSelectInModal v-model="form.supplier_id" :options="supplierOptions" :allowClear="true" @change="onSupplierChange" />
```

- Không có prop `loading`. Có `disabled`, `hideSearch`, `size`, `height`, `extraSettings`
  (`{ multiple: true }` cho chọn nhiều), emit `change`, `select`.
- Bộ lọc trong popup: `<V2BaseSmartFilterPanel in-modal …>` — panel tự render `V2BaseSelectInModal`.
- Chip / danh mục bị khoá / nhãn nhân viên → skill `select-and-input-state`.

## 3. Popup XÁC NHẬN — chỉ `BaseConfirmModal`

Xóa · Khóa/Mở khóa · Duyệt/Từ chối · Hủy · Gửi duyệt… đều dùng
`components/modal/base-confirm-modal.vue`. **Không** tạo confirm riêng, **không** dùng
`$bvModal.msgBoxConfirm()`. Các `confirm-*.vue` cũ trong `components/modal/` là nợ kỹ thuật, đừng copy.

```vue
<BaseConfirmModal
    id="confirm-delete-unit"
    title="Xác nhận xóa"
    :message="`Bạn có chắc muốn xóa <b>${pendingItem && pendingItem.name}</b>?`"
    text-accept="Xóa"
    danger
    @event="doDelete"
/>
```

```js
askDelete(item) { this.pendingItem = item; this.$bvModal.show('confirm-delete-unit') },
async doDelete() {
    this.$nuxt?.$loading?.start?.()
    try { … } finally { this.$nuxt?.$loading?.finish?.() }
},
```

- ⚠️ **Luôn khai `id` riêng.** Mặc định là `confirm` — trùng id popup của `V2Footer`, mở nhầm popup.
- Hỏi xác nhận TRƯỚC, bật lớp tải SAU khi user bấm đồng ý.
- Props: `title` · `message` (nhận HTML) · `textAccept`/`textClose` · `danger` (nút đỏ + icon cảnh báo) ·
  `acceptIcon` · `showInput` + `inputLabel`/`inputPlaceholder`/`inputType` · `requiredInput` +
  `inputRequiredMessage`. Sự kiện `@event` (kèm giá trị ô nhập) · `@close`.
- Từ chối/không duyệt có lý do → `V2BaseRejectApproveModal` hoặc `BaseConfirmModal` + `showInput requiredInput`.

## 4. Footer luôn nhìn thấy — bẫy 2 thanh cuộn

`V2BaseModal` đã lo. Chỉ popup `b-modal` tự dựng mới phải tự làm:

```vue
<b-modal hide-footer body-class="xxx-modal-wrap" …>
    <div class="xxx-modal-body">…nội dung dài…</div>   <!-- KHÔNG class modal-body -->
    <div class="modal-footer">…</div>                     <!-- ngoài vùng cuộn -->
</b-modal>
```

```scss
::v-deep .xxx-modal-wrap { overflow: hidden; display: flex; flex-direction: column; min-height: 0; }
.xxx-modal-body { max-height: 55vh; overflow-y: auto; min-height: 0; }
.modal-footer { position: sticky; bottom: 0; background: #fff; z-index: 2; }
```

Đặt lại class `modal-body` cho div của mình = kế thừa `overflow-y: auto` của bootstrap → 2 thanh
cuộn lồng nhau. Tự kiểm (console, đã cuộn hết nội dung): số khối đang cuộn dọc trong modal = **1**, và
`footer.getBoundingClientRect().bottom <= window.innerHeight`.

## 5. Popup có BẢNG dữ liệu (chọn hàng hoá, chọn nhân viên, xem danh sách…)

Nguyên tắc: bảng là vùng làm việc → popup **cao cố định**, mọi khối phụ `flex-shrink: 0`, **chỉ khung
bảng** `flex: 1`. Số dòng thấy được = chiều cao bảng ÷ chiều cao dòng — tối ưu cả hai.

8 điểm bắt buộc:

1. Khung cao cố định: rộng **≥ 1100px hoặc `98vw`**, `height: 98vh` (không chỉ `max-height`), flex cột. Với `V2BaseModal`: `size="xl"` + `dialog-class` riêng khai rộng/cao.
2. `min-height: 0` ở **mọi** mắt xích flex từ body xuống bảng (b-tabs chèn `.tabs` → `.tab-content` → `.tab-pane.active`).
3. Body `overflow: hidden` — chỉ khung bảng cuộn dọc.
4. Khung bảng `flex: 1 1 auto; min-height: 0; overflow: auto` — không `max-height` cứng, không sàn `min-height` cứng.
5. Dòng thấp: `td { padding: 3px 6px; font-size: 12px }`, thumbnail ≤ 26px, chữ dài cắt 2 dòng (`clamp-2`) + `:title`, `thead` sticky.
6. Nút phụ ("Thêm hàng tạm"…) đặt cùng hàng với khối lọc, không chiếm dòng riêng.
7. Lọc nâng cao là grid phẳng `repeat(auto-fit, minmax(190px, 1fr))`, không chia hàng cứng + ô độn.
8. Control lẻ: nhãn ngang control thay vì xếp chồng; nén margin thừa của phân trang.

**Bẫy `V2BaseTableScroll`**: component có 2 lớp — gốc `.v2-table-scroll` và trong
`.v2-table-scroll__body` (nhận `body-class`). Khai flex cho **lớp gốc**, `::v-deep` cho lớp trong;
khai nhầm lớp thì phân trang bị đẩy khuất dưới đáy popup mà không báo lỗi.

```scss
.v2-modal-body ::v-deep > .v2-table-scroll { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }
.v2-modal-body ::v-deep .my-table-wrap { flex: 1 1 auto; min-height: 0; overflow-y: auto; }
```

Tự kiểm: `paging.getBoundingClientRect().bottom <= card.getBoundingClientRect().bottom` phải `true`.

**Bẫy chip select2 bị cắt đầu chữ**: ô chọn nhiều tràn ngang → chip hiện `g cụ và thiết bị`. Cho chip
xuống dòng (`white-space: normal` ở `.select2-selection__rendered` và `.select2-selection__choice`)
**kèm trần chiều cao** — `V2BaseSelect` của dns đã có `max-height: 86px` sẵn, đừng khai lại ở màn.
Thiếu trần là ô nở theo số chip và ăn hết chỗ của bảng.

Đo số dòng thấy được ở 2 trạng thái (nâng cao đóng/mở) × 2 màn hình (1920×1080, 1366×768) — bằng
console/`mcp__playwright__browser_evaluate` khi user cho phép chạy trình duyệt.

## 6. Popup CHỌN BẢN GHI — click dòng là thêm ngay, và phải là MẶC ĐỊNH

- Bấm vào dòng = thêm bản ghi đó. Checkbox vẫn giữ (`@click.stop`) để thêm hàng loạt.
- Component dùng chung: hành vi chuẩn phải là **giá trị mặc định**; màn cần khác thì tắt tường minh +
  ghi lý do. Đừng để mặc định "an toàn" rồi bắt từng màn tự bật.
- Sửa hành vi trong component dùng chung → grep ngay các màn đang khai đè. (Sửa component dùng chung ở dns → **hỏi user trước**, CLAUDE.md.)

## 7. Ví dụ footer

| Loại | Thứ tự nút |
| --- | --- |
| Thêm mới | Lưu (primary) → Lưu & Tiếp tục (secondary, nếu có) → Đóng (tertiary) |
| Sửa | Lưu → Đóng |
| Sửa có quyền xóa | **Lưu → Xóa → Đóng** |
| Chỉ xem | Đóng |
| Xác nhận xóa (`BaseConfirmModal`) | **Xóa → Hủy** |

Icon + text theo `button-convention` A3/A4 (Lưu `ri-save-3-line`, Xóa `ri-delete-bin-line`, Đóng
`fas fa-arrow-left`). Nút ghi dữ liệu có `:interactable="!saving"` chống bấm kép.

## 8. Bẫy: slot rỗng từ lần mở thứ hai

bootstrap-vue huỷ nội dung modal khi đóng; mở lại thì `this.$slots.x` có thể rỗng → nút mất icon.
Component nằm trong modal kiểm **cả hai**: `v-if="$slots.prefix || $scopedSlots.prefix"`
(`V2BaseButton` của dns đã làm đúng — component mới tự viết cũng phải vậy).

## 9. Checklist

- [ ] Dựng trên `V2BaseModal`, header 1 dòng, không `subtitle`
- [ ] Footer sticky, luôn thấy; chỉ 1 vùng cuộn dọc
- [ ] Không CSS đè padding/header/footer của `V2BaseModal`
- [ ] Select trong popup là `V2BaseSelectInModal`; bộ lọc trong popup có `in-modal`
- [ ] Xác nhận bằng `BaseConfirmModal` với `id` riêng (không `confirm`), không `msgBoxConfirm`
- [ ] Nút theo `button-convention`, thứ tự như mục 7
- [ ] Nhãn trường bắt buộc: `<V2BaseLabel required>` (form V2) hoặc `<Required />` (form cũ) — không viết `*` trần; validate theo skill `form-validate`
- [ ] Popup có bảng: đủ 8 điểm mục 5, phân trang không bị đẩy khuất
- [ ] Ô trống để trống, không `—`; không `.text-muted` (ra đỏ ở dns)
