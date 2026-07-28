# Skill: Modal Popup

Chuẩn hoá UI cho tất cả modal/popup sử dụng V2Base components.
Áp dụng khi tạo mới hoặc chỉnh sửa bất kỳ modal nào trong project.

> **Button trong modal**: tuân thủ skill `button-convention` — variant, icon, thứ tự, cú pháp đều theo quy tắc chung đó. Skill này chỉ bổ sung phần **cấu trúc modal** và **ví dụ footer theo loại modal**.

---

## 1. Cấu trúc modal

- Dùng `b-modal` với `hide-footer`, tự viết `<div class="modal-footer">` bên trong body
- Header: custom slot `#modal-header` gồm icon tròn + title + nút X đóng
- Cho phép click backdrop đóng modal (KHÔNG dùng `no-close-on-backdrop`)
- Tham khảo: `components/modal/application-modal.vue`

```vue
<b-modal
    id="modal-id"
    ref="my-modal"
    @show="onModalShow"
    @cancel="closeModal"
    @close="closeModal"
    @hide="closeModal"
    hide-footer
    size="lg"
    content-class="shadow"
>
    <template #modal-header>
        <div class="d-flex align-items-center w-100">
            <div
                class="d-flex align-items-center justify-content-center mr-2"
                style="width: 28px; height: 28px; border-radius: 999px; background: rgba(26, 188, 156, 0.1); color: #1abc9c;"
            >
                <i class="ri-icon-name" style="font-size: 16px"></i>
            </div>
            <div>
                <h5 class="modal-title mb-0" style="font-size: 14px; font-weight: 800">
                    {{ title }}
                </h5>
                <V2BaseMetaInfo
                    v-if="id && (data.updated_at || data.updated_by_name)"
                    variant="chip"
                    :updated-at="data.updated_at"
                    :updated-by="data.updated_by_name"
                />
            </div>
        </div>
        <button type="button" class="close" @click="closeModal">
            <span aria-hidden="true">&times;</span>
        </button>
    </template>

    <div class="modal-body">
        <!-- Form content -->
    </div>

    <div class="modal-footer">
        <!-- Buttons theo skill button-convention -->
    </div>
</b-modal>
```

---

## 2. Select trong modal — BẮT BUỘC dùng V2BaseSelectInModal

Mọi dropdown/select bên trong modal/popup phải dùng `V2BaseSelectInModal` (KHÔNG dùng `V2BaseSelect`).

**Lý do**: `V2BaseSelectInModal` tự set `dropdownParent` về `.modal-content` nên dropdown không bị che/cắt bởi modal, đồng thời xử lý đúng focus ô search, click-outside và nút clear trong ngữ cảnh modal.

```vue
<V2BaseSelectInModal
    v-model="form.field_id"
    :options="optionsForSelect"
    placeholder="Chọn ..."
    :allowClear="true"
    @change="onFieldChange"
/>
```

**Khác biệt so với `V2BaseSelect` cần lưu ý khi chuyển đổi:**

- KHÔNG có prop `loading` — bỏ `:loading` đi
- Nuxt auto-import components đang bật → không cần import/đăng ký thủ công
- Hỗ trợ `disabled`, `hideSearch`, `size`, `extraSettings`; emit `change`, `select`
- Options nhận `{ id/value/code, name/label/text }` giống `V2BaseSelect`

Khi review modal: gặp `V2BaseSelect` nằm trong `b-modal` → đổi sang `V2BaseSelectInModal`.

---

## 3. Ví dụ footer theo loại modal

### Modal thêm mới

```vue
<div class="modal-footer">
    <V2BaseButton primary size="sm" :interactable="!isSubmitSave" @click="save(false)">
        <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
        Lưu
    </V2BaseButton>
    <V2BaseButton secondary size="sm" :interactable="!isSubmitSave" @click="save(true)">
        <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
        Lưu & Tiếp tục
    </V2BaseButton>
    <V2BaseButton tertiary size="sm" @click="closeModal">
        <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
        Đóng
    </V2BaseButton>
</div>
```

### Modal chỉnh sửa

```vue
<div class="modal-footer">
    <V2BaseButton primary size="sm" :interactable="!isSubmitSave" @click="save">
        <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
        Lưu
    </V2BaseButton>
    <V2BaseButton tertiary size="sm" @click="closeModal">
        <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
        Đóng
    </V2BaseButton>
</div>
```

### Modal chỉ xem

```vue
<div class="modal-footer">
    <V2BaseButton tertiary size="sm" @click="closeModal">
        <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
        Đóng
    </V2BaseButton>
</div>
```

### Modal xác nhận xoá

```vue
<div class="modal-footer">
    <V2BaseButton primary status="danger" size="sm" @click="confirmDelete">
        <template #prefix><i class="ri-delete-bin-line" style="font-size: 15px"></i></template>
        Xoá
    </V2BaseButton>
    <V2BaseButton tertiary size="sm" @click="closeModal">
        <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
        Huỷ
    </V2BaseButton>
</div>
```

**Quy tắc riêng modal:**
- Nếu modal có cả Xoá + Lưu (form sửa cho phép xoá): **Lưu → Xoá → Đóng**
- Modal chỉ xem: chỉ có **Đóng**
- Modal xác nhận xoá: **Xoá → Huỷ**

---

## 4. Popup chứa BẢNG dữ liệu — dồn diện tích cho bảng

Áp dụng khi popup có **bảng dữ liệu để chọn/xem** (popup chọn hàng hoá, chọn NV, chọn thiết bị...).

> **Nguyên tắc**: bảng là vùng user thực sự làm việc → popup **cao cố định**, mọi khối phụ
> `flex-shrink: 0`, **CHỈ khung bảng** `flex: 1`. Bộ lọc/nút/nhãn là thứ yếu, nén tối đa.

**Số dòng thấy được = chiều cao bảng ÷ chiều cao dòng.** Phải tối ưu **cả hai** —
nới popup mà để dòng cao 64px thì vẫn ít dòng.

Popup mới có bảng **phải** có đủ 8 điểm sau (thiếu điểm nào là hỏng mục tiêu):

1. **Khung cao cố định**: `.modal-card { width: 98vw; height: 98vh; max-height: 98vh; display:flex; flex-direction:column }` — bắt buộc có `height`, không chỉ `max-height`. Backdrop `padding: 6px`.
2. **Chuỗi flex không đứt**: `min-height: 0` ở **mọi** mắt xích từ `.modal-body` xuống bảng (b-tabs chèn `.tabs` → `.tab-content` → `.tab-pane.active` vào giữa).
3. **`.modal-body { overflow: hidden }`** — KHÔNG `overflow-y: auto`. Chỉ khung bảng được cuộn dọc.
4. **Khung bảng** `flex: 1 1 auto; min-height: 160px; overflow: auto` — KHÔNG đặt `max-height` cứng.
5. **Chiều cao dòng**: `td { padding: 3px 6px; font-size: 12px }`, ảnh thumbnail ≤ 26px, cột chữ dài bọc `.cell-clamp` (cắt 2 dòng) + `:title` tooltip, `thead` sticky.
6. **Nút phụ** ("Thêm hàng tạm"...) → slot `#header-actions` của `V2BaseFilterPanel` (ngang hàng nút "Tìm kiếm nâng cao", không tốn dòng riêng). Nút Tìm kiếm/Làm mới → prop `inlineSearchButtons`.
7. **Lọc nâng cao**: 1 grid PHẲNG `repeat(auto-fit, minmax(190px, 1fr))` — KHÔNG chia hàng cứng 5 ô + ô rỗng độn.
8. **Control lẻ**: nhãn NGANG control (~32px) thay vì xếp chồng (~56px). Nén `::v-deep .tp-card` và `::v-deep .row.paging` (class `mt-3` tốn 24px).

**Verify BẮT BUỘC bằng số đo, không nhìn bằng mắt** — Playwright `browser_evaluate`, đếm số dòng
thấy đủ ở **2 trạng thái** (nâng cao đóng / mở) × **2 viewport** (1920×1080 / 1366×768), và
assert `modal-body.scrollHeight <= clientHeight` (bắt lỗi điểm 2+3 tái phát).

> **Bẫy select2 multiple**: ép `width:100%; float:none` mọi lúc → ô search **đè lên chip**.
> Chỉ ép ở trạng thái rỗng bằng `:only-child`. Xem `table-popup-layout.md`.

📄 **CSS copy-paste đầy đủ + 7 bẫy đã trả giá + ngân sách chiều cao + snippet đo**:
xem `table-popup-layout.md` cùng thư mục.
File mẫu đang chạy: `pages/assign/quotations/components/QuotationProductSearchModal.vue`.

---

## 5. Checklist khi tạo/review modal

- [ ] Dùng `hide-footer` + tự viết `<div class="modal-footer">`
- [ ] Header có icon tròn + title + nút X
- [ ] Không dùng `no-close-on-backdrop`
- [ ] Button tuân thủ skill `button-convention` (variant, icon, thứ tự, size)
- [ ] Mọi select trong modal dùng `V2BaseSelectInModal`, KHÔNG dùng `V2BaseSelect`

**Nếu popup có bảng dữ liệu — thêm (xem mục 4):**

- [ ] `.modal-card` có `height: 98vh` (không chỉ `max-height`)
- [ ] `min-height: 0` đủ mọi mắt xích flex xuống tới bảng
- [ ] `.modal-body { overflow: hidden }`, chỉ khung bảng cuộn dọc
- [ ] Khung bảng `flex: 1 1 auto`, KHÔNG `max-height` cứng
- [ ] Cột chữ dài có `.cell-clamp` + `:title`; thumbnail ≤ 26px
- [ ] Nút phụ nằm trong slot `#header-actions`, không chiếm dòng riêng
- [ ] Lọc nâng cao dùng grid `auto-fit`, không chia hàng cứng
- [ ] **Đã ĐO số dòng bằng Playwright** ở cả 2 trạng thái nâng cao đóng/mở
