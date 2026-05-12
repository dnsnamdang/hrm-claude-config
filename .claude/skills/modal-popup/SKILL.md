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

## 2. Ví dụ footer theo loại modal

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

## 3. Checklist khi tạo/review modal

- [ ] Dùng `hide-footer` + tự viết `<div class="modal-footer">`
- [ ] Header có icon tròn + title + nút X
- [ ] Không dùng `no-close-on-backdrop`
- [ ] Button tuân thủ skill `button-convention` (variant, icon, thứ tự, size)
