# Skill: Modal Popup

Chuẩn hoá UI cho tất cả modal/popup sử dụng V2Base components.
Áp dụng khi tạo mới hoặc chỉnh sửa bất kỳ modal nào trong project.

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
        <!-- Buttons theo quy tắc bên dưới -->
    </div>
</b-modal>
```

---

## 2. Phân nhóm button theo hành động

| Nhóm | Variant | Mô tả | Ví dụ | Icon gợi ý |
|------|---------|--------|-------|------------|
| **Action chính** | `primary` | Hành động chính của modal, thường chỉ có 1 | Lưu, Xác nhận, Duyệt, Chọn, Gộp | `ri-save-3-line`, `ri-check-line`, `ri-checkbox-circle-line` |
| **Action phụ** | `secondary` | Hành động cùng mục đích nhưng có biến thể | Lưu & Tiếp tục, Lưu & Chọn, Thêm nhanh, Xuất file, Gửi thử | `ri-save-3-line`, `ri-add-line`, `ri-download-line`, `ri-send-plane-line` |
| **Thoát / Huỷ** | `tertiary` | Đóng modal, huỷ thao tác, quay lại | Đóng, Huỷ, Quay lại | `fas fa-arrow-left` |
| **Nguy hiểm** | `primary` + `status="danger"` | Hành động xoá, từ chối, không thể hoàn tác | Xoá, Từ chối, Xoá nội dung | `ri-delete-bin-line`, `ri-close-circle-line` |
| **Reset / Phụ trợ** | `tertiary` | Reset, làm mới, nhập lại | Nhập lại, Làm mới, Xoá trắng | `ri-refresh-line`, `ri-eraser-line` |

**Nếu hành động chưa có trong bảng** → xác định nó thuộc nhóm nào → dùng variant của nhóm đó + chọn icon phù hợp từ Remix Icon.

---

## 3. Nguyên tắc button

### Mọi button đều PHẢI có icon

Dùng slot `#prefix` để đặt icon:

```vue
<V2BaseButton primary size="sm" @click="save">
    <template #prefix>
        <i class="ri-save-3-line" style="font-size: 15px"></i>
    </template>
    Lưu
</V2BaseButton>
```

### Tất cả button trong modal dùng `size="sm"`

### KHÔNG dùng `light` cho button trong modal footer

---

## 4. Thứ tự button trong footer (trái → phải)

| Vị trí | Nhóm | Ví dụ |
|--------|------|-------|
| 0 | **Lưu nháp** (secondary) — nếu có, **luôn đứng đầu tiên** | Lưu nháp |
| 1 | **Action chính** (primary) | Lưu, Xác nhận, Duyệt, Chọn |
| 2 | **Action phụ** (secondary) | Lưu & Tiếp tục, Gửi thử, Xuất file |
| 3 | **Nguy hiểm** (danger) | Xoá, Từ chối |
| 4 | **Reset / Phụ trợ** (tertiary) | Nhập lại, Làm mới |
| 5 | **Thoát / Huỷ** (tertiary) | Đóng, Huỷ — **luôn ở cuối cùng bên phải** |

**Quy tắc:**
- Nếu có nút **Lưu nháp** → luôn đặt đầu tiên (bên trái nhất)
- Action quan trọng nhất ở bên trái, thoát luôn ở cuối cùng bên phải
- Nếu modal có cả Xoá + Lưu (form sửa cho phép xoá): **Lưu → Xoá → Đóng**
- Modal chỉ xem: chỉ có **Đóng**
- Modal xác nhận xoá: **Xoá → Huỷ**

---

## 5. Ví dụ footer theo loại modal

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

---

## 6. Checklist khi tạo/review modal

- [ ] Dùng `hide-footer` + tự viết `<div class="modal-footer">`
- [ ] Header có icon tròn + title + nút X
- [ ] Mọi button đều có icon qua `#prefix`
- [ ] Button variant đúng theo nhóm hành động
- [ ] Thứ tự button: action chính → action phụ → danger → reset → thoát
- [ ] Tất cả button dùng `size="sm"`
- [ ] Không dùng variant `light` trong modal footer
- [ ] Không dùng `no-close-on-backdrop`
