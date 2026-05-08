# Skill: Button Convention

Chuẩn hoá quy tắc sử dụng V2BaseButton và V2BaseIconButton trong toàn bộ project.
Áp dụng ở mọi ngữ cảnh: toolbar danh sách, form page, table action, modal footer, v.v.

---

## 1. Nguyên tắc chung

- **Mọi V2BaseButton đều PHẢI có icon** qua slot `#prefix` (trừ trường hợp nút chỉ có icon không có text — dùng `V2BaseIconButton`)
- **Luôn khai báo `size`** — mặc định dùng `size="sm"`
- **KHÔNG dùng `type="primary"`** — dùng prop `primary` trực tiếp (tương tự `secondary`, `tertiary`)
- Icon dùng **Remix Icon** (`ri-*`) là chính, `Font Awesome` (`fas fa-*`) chỉ dùng khi Remix Icon không có icon phù hợp

---

## 2. Bảng variant theo nhóm hành động

| Nhóm hành động | Variant | Mô tả |
|----------------|---------|--------|
| **Action chính** | `primary` | Hành động chính của màn hình — Thêm mới, Lưu, Xác nhận, Duyệt, Chọn, In |
| **Action phụ** | `secondary` | Hành động bổ trợ — Lưu & Tiếp tục, Xuất Excel, Import, Cấu hình cột, Gửi thử |
| **Thoát / Huỷ** | `tertiary` | Đóng, Huỷ, Quay lại, Đóng modal |
| **Reset / Phụ trợ** | `tertiary` | Nhập lại, Làm mới, Xoá trắng, Xem thêm |
| **Nguy hiểm** | `primary` + `status="danger"` | Xoá, Từ chối, Huỷ duyệt |
| **Hành động nhẹ (trang)** | `light` | CHỈ dùng cho nút phụ ngoài page (Quay lại trang trước, Xem log) — **KHÔNG dùng trong modal footer** |

**Quy tắc xác định variant cho hành động mới:**
1. Hành động đó là mục đích chính của màn hình? → `primary`
2. Hành động bổ trợ, không bắt buộc? → `secondary`
3. Hành động đóng/thoát/huỷ? → `tertiary`
4. Hành động nguy hiểm, không thể hoàn tác? → `primary` + `status="danger"`
5. Nút phụ nhẹ ngoài page (không phải trong modal)? → `light`

---

## 3. Bảng icon theo hành động

| Hành động | Icon | Ghi chú |
|-----------|------|---------|
| Thêm mới / Tạo mới | `ri-add-line` | |
| Lưu | `ri-save-3-line` | |
| Lưu & Tiếp tục | `ri-save-3-line` | Cùng icon với Lưu |
| Chỉnh sửa | `ri-edit-line` | |
| Xoá | `ri-delete-bin-line` | |
| Đóng / Huỷ / Quay lại | `fas fa-arrow-left` | |
| Xác nhận / Duyệt | `ri-check-line` | |
| Từ chối | `ri-close-circle-line` | |
| Xuất Excel / Export | `ri-download-line` | |
| Import | `ri-upload-line` | |
| In / Print | `ri-printer-line` | |
| Tìm kiếm | `ri-search-line` | |
| Làm mới / Nhập lại | `ri-refresh-line` | |
| Xoá trắng / Reset | `ri-eraser-line` | |
| Gửi / Submit | `ri-send-plane-line` | |
| Cấu hình / Cài đặt | `ri-settings-3-line` | |
| Xem chi tiết | `ri-eye-line` | |
| Xem log / Lịch sử | `ri-history-line` | |
| Sao chép / Nhân bản | `ri-file-copy-line` | |
| Gộp / Merge | `ri-merge-cells-horizontal` | |
| Chọn | `ri-checkbox-circle-line` | |
| Thêm nhân sự | `ri-user-add-line` | |

**Nếu hành động không có trong bảng:** chọn icon Remix Icon phù hợp nhất với ngữ nghĩa hành động. Tra cứu tại https://remixicon.com.

---

## 4. Thứ tự hiển thị button

### Trong modal footer (trái → phải)

| Vị trí | Nhóm | Ví dụ |
|--------|------|-------|
| 0 | Lưu nháp (secondary) — nếu có, **luôn đứng đầu tiên** | Lưu nháp |
| 1 | Action chính (primary) | Lưu, Xác nhận, Duyệt |
| 2 | Action phụ (secondary) | Lưu & Tiếp tục, Xuất file |
| 3 | Nguy hiểm (danger) | Xoá, Từ chối |
| 4 | Reset / Phụ trợ (tertiary) | Nhập lại, Làm mới |
| 5 | Thoát / Huỷ (tertiary) | Đóng — **luôn cuối cùng** |

### Trong toolbar danh sách (trái → phải)

| Vị trí | Nhóm | Ví dụ |
|--------|------|-------|
| 1 | Action chính (primary) | Thêm mới |
| 2 | Action phụ (secondary) | Import, Xuất Excel, Cấu hình cột |
| 3 | Phụ trợ (light/tertiary) | Quay lại, Xem log |

### Trong form page (nhóm nút trên cùng hoặc dưới cùng)

| Vị trí | Nhóm | Ví dụ |
|--------|------|-------|
| 0 | Lưu nháp (secondary) — nếu có, **luôn đứng đầu tiên** | Lưu nháp |
| 1 | Action chính (primary) | Lưu, Gửi duyệt, In |
| 2 | Action phụ (secondary) | Xuất file, Preview |
| 3 | Quay lại (light/tertiary) | Quay lại danh sách |

### Trong table (action column)

- Dùng `V2BaseIconButton` (chỉ icon, không text)
- Thứ tự: Xem → Sửa → Xoá

---

## 5. Cú pháp chuẩn

### V2BaseButton (có text)

```vue
<!-- Action chính -->
<V2BaseButton primary size="sm" @click="save">
    <template #prefix>
        <i class="ri-save-3-line" style="font-size: 15px"></i>
    </template>
    Lưu
</V2BaseButton>

<!-- Action phụ -->
<V2BaseButton secondary size="sm" @click="exportExcel">
    <template #prefix>
        <i class="ri-download-line" style="font-size: 15px"></i>
    </template>
    Xuất Excel
</V2BaseButton>

<!-- Thoát -->
<V2BaseButton tertiary size="sm" @click="closeModal">
    <template #prefix>
        <i class="fas fa-arrow-left" style="margin-right: 3px"></i>
    </template>
    Đóng
</V2BaseButton>

<!-- Nguy hiểm -->
<V2BaseButton primary status="danger" size="sm" @click="confirmDelete">
    <template #prefix>
        <i class="ri-delete-bin-line" style="font-size: 15px"></i>
    </template>
    Xoá
</V2BaseButton>
```

### V2BaseIconButton (chỉ icon, trong table action)

```vue
<V2BaseIconButton @click="viewDetail(item)">
    <i class="ri-eye-line"></i>
</V2BaseIconButton>

<V2BaseIconButton @click="editItem(item)">
    <i class="ri-edit-line"></i>
</V2BaseIconButton>

<V2BaseIconButton danger @click="deleteItem(item)">
    <i class="ri-delete-bin-line"></i>
</V2BaseIconButton>
```

---

## 6. Checklist khi tạo/review button

- [ ] Mọi V2BaseButton đều có icon qua `#prefix`
- [ ] Đã khai báo `size` (mặc định `sm`)
- [ ] Variant đúng theo nhóm hành động
- [ ] Không dùng `type="primary"` — dùng prop `primary`
- [ ] Không dùng `light` trong modal footer
- [ ] Thứ tự button: action chính → phụ → danger → reset → thoát (cuối cùng)
- [ ] Icon phản ánh đúng ngữ nghĩa hành động
- [ ] Table action dùng V2BaseIconButton, thứ tự: Xem → Sửa → Xoá
