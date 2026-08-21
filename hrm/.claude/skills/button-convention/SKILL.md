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
| **Action phụ** | `secondary` | Hành động bổ trợ — Lưu và tiếp tục, Xuất file, Import, Cấu hình cột, Gửi thử. Màu phân biệt theo `status`, xem mục 2b |
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

## 2b. Màu (`status`) — phân biệt các nút cùng variant

`variant` quyết định **độ nổi**, `status` quyết định **màu**. Cả nhóm nút phụ mà để chung một màu trắng thì user phải đọc chữ mới phân biệt được — nhất là nhóm Import/Xuất file đứng cạnh nhau.

`status` khả dụng: `info` (mặc định) · `success` (xanh lá) · `warning` (cam) · `danger` (đỏ).

### Nhóm Import / Xuất file

| Nút | Khai báo | Màu |
| --- | --- | --- |
| **Import Excel** | `secondary status="warning"` | **cam** |
| **Xuất CSV / Xuất Excel / Xuất PDF** | `secondary status="success"` | **xanh lá** — cả nhóm CÙNG một màu |

Nguyên tắc: phân biệt theo **bản chất thao tác**, không theo định dạng file.

- **Import** ghi dữ liệu vào hệ thống → tách hẳn tông (cam).
- **Nhóm Xuất** chỉ đọc dữ liệu ra, cùng bản chất → **cùng màu**, phân biệt bằng chữ + icon riêng của từng định dạng (`ri-file-text-line` / `ri-file-excel-2-line` / `ri-file-pdf-line`).

📄 Bảng tra nhanh dạng Excel (màu · icon · text · thứ tự): `.plans/gop-db/list-page-action-column/quy-tac-mau-button.xlsx`

⚠️ Đừng tô mỗi nút xuất một màu theo thương hiệu file (Excel xanh, PDF đỏ): 3 nút cùng làm một việc mà 3 màu thì đọc như 3 mức độ nguy hiểm khác nhau, và đỏ ở đây đá vào quy ước "đỏ = phá huỷ dữ liệu".

### Các nhóm còn lại

| Hành động | Khai báo |
| --- | --- |
| Tạo mới · Lưu · Lưu nháp | `primary` (teal `#1abc9c`) |
| **Duyệt · Gửi duyệt · Hoàn thành · Kích hoạt** | `primary` (teal `#1abc9c`) — **KHÔNG thêm `status`** |
| **Khóa** · Cảnh báo | `primary status="warning"` |
| **Mở khóa** · Khôi phục · Kích hoạt lại | `primary status="success"` |
| Xóa · Từ chối · Hủy duyệt · Mở khóa dữ liệu đã chốt | `primary status="danger"` |
| In · Cấu hình cột · Làm mới · Xem thêm | `secondary` / `tertiary` (info) |
| Đóng · Hủy · Quay lại | `tertiary` (info) |

📌 **Nhóm Duyệt dùng teal `#1abc9c`, không dùng xanh lá `#16a34a`** (user chốt 2026-08-20).
`primary` không kèm `status` cho ra đúng `#1abc9c` (`components/V2BaseButton.vue` — `.v2-btn--primary`),
còn `status="success"` là `#16a34a`. Chọn teal vì đây đã là màu nút **Duyệt / Lưu và duyệt / Trưởng
phòng duyệt / BGĐ duyệt** mặc định của `components/V2Footer.vue` — component dùng chung mà hầu hết
màn chi tiết đang dùng — nên để nhóm Duyệt cùng teal thì cả hệ thống mới nhất quán.
**Gửi duyệt** trước đây xếp nhóm `warning` (cam), nay chuyển về cùng nhóm này: gửi duyệt là bước
tiến của luồng nghiệp vụ, không phải cảnh báo. Cam giờ chỉ còn dành cho **Khóa · Cảnh báo**.

⚠️ **Không dùng `danger` cho thao tác vô hại** (xóa điều kiện lọc, đóng popup) — đỏ chỉ dành cho việc phá huỷ/không hoàn tác được, dùng tràn lan là mất tác dụng cảnh báo.

⚠️ **Nút đổi trạng thái phải ĐỔI MÀU theo trạng thái**, không để cứng một màu:

```vue
<!-- Khóa: cam (hạn chế) · Mở khóa: xanh lá (cho hoạt động lại) -->
<V2BaseButton primary :status="isActive ? 'warning' : 'success'" @click="toggleLock">
```

Để cứng `status="danger"` cho cả 2 chiều là sai — "Mở khóa" là hành động **khôi phục**, tô đỏ khiến user tưởng sắp phá huỷ dữ liệu. Trong cột hành động của bảng (`V2BaseIconButton` chỉ có `danger` boolean) thì **không set `danger`** cho Khóa/Mở khóa — để trung tính, giữ đỏ riêng cho Xóa.

---

## 3. Bảng icon theo hành động

| Hành động | Icon | Ghi chú |
|-----------|------|---------|
| Tạo mới | `ri-add-line` | |
| Lưu | `ri-save-3-line` | |
| Lưu và tiếp tục | `ri-save-3-line` | Cùng icon với Lưu |
| Sửa | `ri-edit-line` | |
| Xóa | `ri-delete-bin-line` | |
| Đóng / Hủy / Quay lại | `fas fa-arrow-left` | |
| Xác nhận / Duyệt | `ri-check-line` | |
| Từ chối | `ri-close-circle-line` | |
| Xuất file (chung, chỉ 1 nút) | `ri-download-line` | |
| Xuất Excel | `ri-file-excel-2-line` | Khi màn có NHIỀU nút xuất, mỗi định dạng 1 icon riêng để phân biệt |
| Xuất CSV | `ri-file-text-line` | |
| Xuất PDF | `ri-file-pdf-line` | |
| Import Excel | `ri-upload-line` | Text phải nói rõ import cái gì, không để trống nghĩa là "Import" |
| In / Print | `ri-printer-line` | |
| Tìm kiếm | `ri-search-line` | |
| Làm mới | `ri-refresh-line` | |
| Xóa trắng / Reset | `ri-eraser-line` | |
| Gửi / Submit | `ri-send-plane-line` | |
| Cấu hình / Cài đặt | `ri-settings-3-line` | Chỉ dùng cho cấu hình/thiết lập thật, không dùng cho "Quản lý" |
| Quản lý (hồ sơ con của bản ghi) | `ri-folder-user-line` | VD: quản lý người liên hệ / TK ngân hàng của KH |
| Xem chi tiết | `ri-eye-line` | |
| Lịch sử | `ri-history-line` | |
| Khóa | `ri-lock-line` | |
| Mở khóa | `ri-lock-unlock-line` | |
| Hành động khác (menu ⋮) | `ri-more-2-fill` | 3 chấm DỌC, không dùng `ri-more-fill` |
| Cấu hình cột hiển thị | `ri-layout-column-line` | Khác `ri-settings-3-line` (cấu hình/cài đặt chung) |
| Nhân bản | `ri-file-copy-line` | |
| Gộp / Merge | `ri-merge-cells-horizontal` | |
| Chọn | `ri-checkbox-circle-line` | |
| Thêm nhân sự | `ri-user-add-line` | |

**Nếu hành động không có trong bảng:** chọn icon Remix Icon phù hợp nhất với ngữ nghĩa hành động. Tra cứu tại https://remixicon.com.

---

## 4. Chuẩn text trên nút

Hai hành động giống nhau ở 2 màn khác nhau PHẢI dùng **cùng một chữ**. Dưới đây là chữ chuẩn; cột "Không dùng" là các biến thể đang tồn tại trong code và phải sửa dần khi đụng vào màn.

### 4.1. Quy tắc chữ

- **Bỏ dấu kiểu mới**: `Xóa`, `Hủy`, `Khóa` — KHÔNG viết `Xoá`, `Huỷ`, `Khoá`.
- Viết hoa **chữ đầu**, phần còn lại viết thường: `Lưu và tiếp tục` (không phải `Lưu Và Tiếp Tục`).
- Không dùng ký hiệu thay từ: viết `và`, không viết `&`.
- Không dấu chấm cuối, không viết tắt tiếng Anh nếu đã có từ tiếng Việt phổ biến.
- **Tối đa 3 từ.** Dài hơn thì rút gọn, phần giải thích đưa vào `title` (tooltip).
- Nút chỉ có icon (`V2BaseIconButton`): `title` phải đúng bằng chữ chuẩn trong bảng dưới.
- **Nêu rõ đối tượng khi chữ trần gây mơ hồ**: `Import Excel` chứ không phải `Import`; `Tải file mẫu` chứ không phải `Tải xuống`. Ngược lại, khi ngữ cảnh đã rõ (đang ở màn danh sách khách hàng) thì dùng `Tạo mới`, không viết `Tạo khách hàng mới` — trừ khi 1 màn có nhiều loại "tạo".

### 4.2. Bảng text chuẩn

| Hành động | Text chuẩn | KHÔNG dùng |
|-----------|-----------|------------|
| Tạo bản ghi mới | **Tạo mới** | Thêm mới, Thêm, Tạo, Add |
| Thêm 1 dòng vào bảng trong form | **Thêm dòng** | Thêm mới dòng, Thêm hàng, Thêm bản ghi |
| Lưu | **Lưu** | Lưu lại, Cập nhật, Ghi lại, Save |
| Lưu nháp | **Lưu nháp** | Lưu tạm, Lưu bản nháp |
| Lưu rồi ở lại tạo tiếp | **Lưu và tiếp tục** | Lưu & Tiếp tục, Lưu và thêm mới |
| Sửa bản ghi | **Sửa** | Chỉnh sửa, Cập nhật, Edit |
| Xóa bản ghi | **Xóa** | Xoá, Xóa bỏ, Delete |
| Khóa / Mở khóa | **Khóa** / **Mở khóa** | Khoá, Mở khoá, Ngừng hoạt động, Kích hoạt |
| Mở màn chi tiết | *(không có nút)* | Xem, Xem chi tiết, Chi tiết — tên bản ghi ở cột đầu là link (xem skill `list-page`) |
| Lịch sử thay đổi | **Lịch sử** | Xem lịch sử, Nhật ký, Log |
| Nhân bản bản ghi | **Nhân bản** | Sao chép, Tạo bản sao, Copy |
| Duyệt / Từ chối | **Duyệt** / **Từ chối** | Phê duyệt, Chấp nhận, Không duyệt |
| Gửi đi để duyệt | **Gửi duyệt** | Trình duyệt, Trình ký, Gửi phê duyệt |
| Xác nhận trong modal | **Xác nhận** | Đồng ý, OK, Chấp nhận |
| Hủy trong modal | **Hủy** | Huỷ, Hủy bỏ, Cancel |
| Đóng modal | **Đóng** | Thoát, Close, Bỏ qua |
| Quay lại trang trước | **Quay lại** | Trở về, Quay về, Thoát |
| Tìm kiếm | **Tìm kiếm** | Tìm, Lọc, Search |
| Xóa điều kiện lọc, tải lại danh sách | **Làm mới** | Nhập lại, Đặt lại, Reset, Xóa lọc, Bỏ lọc |
| Import từ Excel | **Import Excel** | Import, Nhập Excel, Nhập file, Tải lên |
| Tải file mẫu import | **Tải file mẫu** | Tải mẫu, File mẫu, Download template |
| Xuất file | **Xuất Excel** / **Xuất CSV** / **Xuất PDF** | Export, Xuất file, Xuất dữ liệu, Tải xuống |
| In cả danh sách | **In danh sách** | In, In báo cáo, Print |
| In 1 bản ghi | **In** | In phiếu, In chi tiết |
| Cấu hình cột hiển thị (icon-only) | `title="Cấu hình cột hiển thị"` | Cấu hình, Cài đặt cột, Tùy chỉnh cột |
| Menu hành động còn lại (icon-only) | `title="Hành động khác"` | Thêm, Khác, More |

**Hành động không có trong bảng:** đặt chữ theo công thức `<động từ> + <đối tượng nếu cần>`, tra lại bảng này xem đã có hành động tương đương chưa rồi mới đặt tên mới — tuyệt đối không sinh biến thể mới cho hành động đã có chữ chuẩn.

---

## 5. Thứ tự hiển thị button

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

- Dùng `V2BaseIconButton` (chỉ icon, không text) — chi tiết đầy đủ ở skill `list-page` mục "Cột Hành động"
- **KHÔNG còn nút Xem**: tên bản ghi ở cột đầu là link vào màn chi tiết
- Thứ tự: **Sửa → Xoá (hoặc Khoá/Mở khoá nếu màn không có Xoá) → nút `⋮`** gom các hành động còn lại
- Tối đa 3 nút/dòng; dựng bằng component dùng chung `V2BaseRowActions`, không tự xếp icon

---

## 6. Cú pháp chuẩn

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

## 7. Checklist khi tạo/review button

- [ ] Mọi V2BaseButton đều có icon qua `#prefix`
- [ ] Đã khai báo `size` (mặc định `sm`)
- [ ] Variant đúng theo nhóm hành động
- [ ] Không dùng `type="primary"` — dùng prop `primary`
- [ ] Không dùng `light` trong modal footer
- [ ] Thứ tự button: action chính → phụ → danger → reset → thoát (cuối cùng)
- [ ] Icon phản ánh đúng ngữ nghĩa hành động
- [ ] Nút cùng variant đứng cạnh nhau đã phân biệt màu bằng `status` (mục 2b); nhóm nút CÙNG bản chất (3 nút Xuất) phải CÙNG màu
- [ ] Chữ trên nút đúng bảng text chuẩn mục 4 (dấu kiểu mới: Xóa/Hủy/Khóa; nêu rõ đối tượng: Import Excel)
- [ ] Table action dùng V2BaseIconButton qua `V2BaseRowActions`, thứ tự: Sửa → Xoá/Khoá → `⋮` (không còn nút Xem)
