---
name: modal-popup
description: "Use when tạo/sửa bất kỳ modal / popup / dialog nào ở hrm-client (V2BaseModal, b-modal, popup xác nhận, popup chọn bản ghi, popup có bảng hoặc bộ lọc). Đọc cả khi: select trong popup bị che/không xổ ra, footer popup bị đẩy khuất khi danh sách dài, chip select2 bị cắt chữ, slot trong modal rỗng từ lần mở thứ hai, popup Xem/Sửa thiếu khối Lịch sử."
---

# Skill: Modal Popup

Chuẩn hoá UI cho tất cả modal/popup sử dụng V2Base components.
Áp dụng khi tạo mới hoặc chỉnh sửa bất kỳ modal nào trong project.

> **Button trong modal**: tuân thủ skill `button-convention` — variant, icon, thứ tự, cú pháp đều theo quy tắc chung đó. Skill này chỉ bổ sung phần **cấu trúc modal** và **ví dụ footer theo loại modal**.

---

## 0. KHUÔN DÙNG CHUNG — `components/modal/V2BaseModal.vue` (chốt 2026-08-15)

**Popup MỚI phải dựng trên `V2BaseModal`, KHÔNG tự khai `b-modal` + header + footer riêng.**
Trước đây mỗi màn tự dựng nên ra 3 kiểu khác nhau: khoảng cách body lúc rộng lúc hẹp, footer lúc
ghim lúc bị nội dung dài đẩy khuất, dòng mô tả bản ghi mỗi nơi một màu.

```vue
<V2BaseModal
    modal-id="history-work"
    title="Lịch sử thay đổi: RRP - Rủi ro theo phòng"
    icon="ri-history-line"
    @hidden="onHidden"
>
    <!-- nội dung -->
    <template #footer>
        <V2BaseButton primary size="sm" @click="save">…</V2BaseButton>
        <V2BaseButton tertiary size="sm" @click="close">…</V2BaseButton>
    </template>
</V2BaseModal>
```

Component chốt sẵn toàn bộ phần style, màn dùng CHỈ truyền text + nội dung:

| Phần | Chuẩn (đã nằm sẵn trong component) |
| --- | --- |
| **Header** | icon tròn (đổi qua `icon`/`iconColor`/`iconBackground`) + tiêu đề 14px đậm (`title`) + nút ×. **CHỈ 1 DÒNG** — xem quy tắc ngay dưới |
| **Body** | vùng cuộn riêng, `padding: 0.5rem 0.75rem` — dọc **sát** (popup thừa khoảng trắng, padding dọc 1rem+ như popup Import cũ, là SAI), ngang **0.75rem** để chữ không chạm mép (chốt 2026-09-19); header/footer cùng 0.75rem nên 3 phần thẳng mép trái. **Tự triệt `margin-top` của khối đầu và `margin-bottom` của khối cuối** — nội dung màn hay có `mt-3`/`mb-3`, cộng vào là body rơi tách khỏi header 32px |
| **Footer** | nằm NGOÀI vùng cuộn + `position: sticky; bottom: 0` → **luôn nhìn thấy**, nội dung dài mấy cũng không nuốt mất nút. Không truyền slot `footer` thì mặc định là nút Đóng |

⚠️ **Không tự khai lại các style trên trong màn dùng.** Muốn khác (popup có bảng cần cao hơn) thì
chỉnh qua prop (`maxBodyHeight`, `size`, `dialogClass`), KHÔNG viết CSS đè trong màn — viết đè là
quay lại đúng tình trạng mỗi popup một kiểu.

🚫 **KHÔNG có dòng mô tả bản ghi dưới tiêu đề** (`Khách hàng: 19TPHPVI-262 - NGUYỄN HỮU HỌC`) —
**bỏ hẳn 19/09/2026 theo yêu cầu user**. Header popup đúng 1 dòng: icon + tiêu đề + nút ×.

- 2 prop `subtitle` / `subtitleLabel` của `V2BaseModal` giờ **không render gì** (giữ lại để 35
  popup cũ đang truyền không văng attribute ra DOM). **Popup mới đừng truyền**; popup cũ bỏ dần
  khi có dịp đụng vào.
- Cần cho user biết đang thao tác trên bản ghi nào thì **ghép vào chính tiêu đề**:
  `Lịch sử thay đổi: TCHH.1231 - Máy móc, thiết bị` (khuôn `CatalogHistoryModal`), theo đúng quy
  ước tiêu đề màn chi tiết ở CLAUDE.md. Hoặc để thông tin đó trong **thân popup**.
- TUYỆT ĐỐI không dựng lại dòng mô tả này bằng markup riêng trong từng màn.

⚠️ **Bẫy đã trả giá (2026-08-24) — nút × bị đẩy RA NGOÀI mép popup.** `.modal-header` là flex row
chứa khối tiêu đề + nút ×. Khối tiêu đề để `w-100` là chiếm trọn bề rộng, nút × không còn chỗ và
tràn ra ngoài (đo thật: **26px**). Đúng phải là:

```scss
.v2-modal-head-left,          /* khối bọc icon + tiêu đề */
.v2-modal-heading {           /* khối tiêu đề + dòng mô tả */
    flex: 1 1 auto;
    min-width: 0;             /* PHẢI khai ở CẢ 2 CẤP — thiếu 1 cấp là cấp đó vẫn nở */
}
::v-deep .modal-header > .close { flex: 0 0 auto; }
```

`min-width: 0` không chỉ để cứu nút ×: mặc định flex item là `min-width: auto`, nó **nở theo nội
dung dài nhất** nên `text-overflow: ellipsis` bên trong sẽ không bao giờ ăn.

Props: `modalId` (bắt buộc) · `title` · `icon` · `iconColor` ·
`iconBackground` · `size` · `dialogClass` · `maxBodyHeight`. Sự kiện: `show` · `shown` · `hide` ·
`hidden`. Method: `show()` / `close()`.

**Body của popup XEM một bản ghi có đúng 2 phần, theo thứ tự:**

1. Nội dung nghiệp vụ (các trường)
2. **Khối "Lịch sử"** ở cuối cùng — bắt buộc, xem **mục 3c**

**KHÔNG có phần thứ 3.** Nhất là dòng `Người tạo: … • Ngày tạo: …` ở đáy body — **đã bỏ hẳn**,
lý do ở mục 3c.

Popup CŨ tự dựng thì chuyển dần sang khuôn này khi có dịp đụng vào — ưu tiên popup nào đang bị
mất nút footer hoặc thừa khoảng trắng.

---

## 1. Cấu trúc modal (popup cũ / trường hợp đặc biệt không dùng được `V2BaseModal`)

- Dùng `b-modal` với `hide-footer`, tự viết `<div class="modal-footer">` bên trong body
- Header: custom slot `#modal-header` gồm icon tròn + title + nút X đóng
- Cho phép click backdrop đóng modal (KHÔNG dùng `no-close-on-backdrop`)
- **Footer BẮT BUỘC ghim đáy** (`position: sticky; bottom: 0` + nằm ngoài vùng cuộn) — xem mục 3b.
  Đây là lỗi lặp lại nhiều lần nhất: nội dung dài thì nút Lưu/Đóng bị đẩy khuất, user phải cuộn hết
  mới bấm được.
- Tham khảo: `components/modal/V2BaseModal.vue` (khuôn mới), `components/modal/application-modal.vue`

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

⚠️ Popup Xem của bản ghi đã tồn tại thì **thân popup còn phải có khối "Lịch sử" ở cuối** và
**không được có dòng `Người tạo / Ngày tạo`** — **mục 3c**. Đây là chỗ hay thiếu nhất.

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

## 3a. Popup XÁC NHẬN — chỉ dùng MỘT component duy nhất

Mọi thao tác cần hỏi lại (Xóa · Khóa/Mở khóa · Duyệt/Từ chối · Hủy · Gửi duyệt · thoát khi chưa lưu…) đều dùng **`components/modal/base-confirm-modal.vue`**. **KHÔNG tạo confirm riêng cho từng màn**, **KHÔNG dùng `$bvModal.msgBoxConfirm()`** (popup mặc định của bootstrap-vue: nút không icon, khác kiểu với cả hệ thống).

> Hiện `components/modal/` còn 26 component confirm cũ (`confirm-delete-selected`, `confirm-cancel-approve`, `confirm-modal`, `ConfirmLockSelected`…). Đó là NỢ KỸ THUẬT, không phải mẫu để copy. Màn cũ chuyển dần sang `base-confirm-modal` khi có dịp đụng vào.

### Cách 1 — đặt trong template (phổ biến)

```vue
<BaseConfirmModal
    id="confirm-lock-customer"
    :title="lockConfirmTitle"
    :message="lockConfirmMessage"
    text-close="Hủy"
    :text-accept="lockConfirmAccept"
    danger
    @event="handleConfirmLock"
/>
```
Mở bằng `this.$bvModal.show('confirm-lock-customer')`, bắt kết quả ở `@event`.

### Cách 2 — gọi từ code, ngoài template (route guard, mixin, helper)

```js
const ok = await this.$confirm({
    title: 'Xác nhận xóa',
    message: `Bạn có chắc muốn xóa "${name}"?`,
    textAccept: 'Xóa',
    danger: true,
})
if (!ok) return
```
`$confirm()` (plugin `plugins/confirm-dialog.js`) render chính `base-confirm-modal` rồi trả `Promise<boolean>` — nên popup gọi từ code trông y hệt popup đặt trong template.

### Props

| Prop | Ý nghĩa |
| --- | --- |
| `title` | Tiêu đề (bỏ trống → "Xác nhận") |
| `message` | Nội dung, nhận HTML |
| `textAccept` / `textClose` | Chữ 2 nút (mặc định "Xác nhận" / "Hủy" — theo bảng text chuẩn của `button-convention`) |
| `danger` | Thao tác phá huỷ (Xóa/Khóa/Từ chối): nút xác nhận **đỏ** + icon cảnh báo đỏ ở header |
| `acceptIcon` | Ghi đè icon nút xác nhận (vd `ri-lock-line` cho Khóa) |
| `showInput` + `inputLabel`/`inputPlaceholder`/`inputType` | Kèm ô nhập lý do |

Sự kiện: `@event` (đồng ý, kèm giá trị ô nhập nếu có) · `@close` (đóng/hủy).

## 3b. Footer phải LUÔN nhìn thấy (popup có danh sách dài)

`b-modal` render slot default vào `.modal-body` của nó — nên footer tự viết mà đặt thẳng trong slot sẽ **cuộn theo nội dung**, danh sách dài (20+ dòng) thì user phải kéo hết mới thấy nút Lưu.

Cách làm đúng — vùng cuộn và footer TÁCH nhau:

```vue
<b-modal hide-footer body-class="xxx-modal-wrap" ...>
    <template #modal-header>…</template>

    <!-- CHỈ khối này cuộn. KHÔNG đặt class `modal-body` cho nó (xem bẫy dưới) -->
    <div class="xxx-modal-body">…nội dung dài…</div>

    <!-- nằm NGOÀI vùng cuộn -->
    <div class="modal-footer">…nút…</div>
</b-modal>
```

```scss
/* Tắt cuộn ở `.modal-body` của chính b-modal */
/deep/ .xxx-modal-wrap {
    overflow: hidden;
    display: flex;
    flex-direction: column;
    min-height: 0;
}

.xxx-modal-body {
    max-height: 55vh;
    overflow-y: auto;
    min-height: 0;
}

/* Chốt thêm: màn hình thấp mà b-modal tự cho phần thân cuộn thì footer vẫn dính đáy */
.modal-footer {
    position: sticky;
    bottom: 0;
    background: #fff;
    z-index: 2;
}
```

⚠️ **Bẫy 2 thanh cuộn dọc**: `b-modal` render slot default vào `.modal-body` của nó, mà bootstrap cho khối đó `overflow-y: auto`. Thêm một vùng cuộn nữa bên trong → **2 thanh cuộn lồng nhau**. Phải tắt cuộn khối ngoài bằng `body-class`, và **đừng đặt lại class `modal-body`** cho div của mình (nó kế thừa luôn `overflow` + padding của bootstrap).

Verify bằng số đo (Playwright), ở **cả 1920×1080 và 1366×768**, sau khi đã cuộn hết danh sách:

```js
// đếm số khối đang cuộn dọc trong modal — phải bằng ĐÚNG 1
modal.querySelectorAll('*').forEach(el => { const cs = getComputedStyle(el)
  if ((cs.overflowY === 'auto' || cs.overflowY === 'scroll') && el.scrollHeight > el.clientHeight + 1) n++ })
// và footer luôn trong tầm nhìn
footer.getBoundingClientRect().bottom <= window.innerHeight
```

File mẫu: `components/modal/column-customization-modal.vue`.

---

## 3c. Cuối body popup gắn với 1 BẢN GHI — khối Lịch sử, KHÔNG có dòng Người tạo/Ngày tạo (chốt 2026-09-19)

Áp cho **mọi popup XEM một bản ghi đã tồn tại** (popup Xem của danh mục, popup chi tiết):
điều kiện chuẩn là `v-if="isShow && id"`. Popup **Thêm mới** không có (chưa có bản ghi), popup
**Sửa** cũng không — đang nhập dở mà kèm timeline thì popup dài gấp đôi; muốn xem lịch sử thì mở
popup Xem hoặc mục `Lịch sử` ở menu ⋮ ngoài danh sách.

### a) BẮT BUỘC: khối "Lịch sử" là phần cuối cùng của body

```vue
<V2BaseModal modal-id="type-account" title="Chi tiết loại tài khoản" …>
    <!-- 1. nội dung nghiệp vụ -->
    <div class="row">…</div>

    <!-- 2. LUÔN LÀ PHẦN CUỐI CÙNG -->
    <SystemInfoSection
        v-if="isShow && id"
        class="mt-2"
        entity-type="type_accounts"
        :entity-id="id"
        endpoint-base="catalog-histories"
    />

    <template #footer>…</template>
</V2BaseModal>
```

- Mặc định **thu gọn**, **lazy load** lần mở đầu tiên (đã nằm trong `SystemInfoSection`).
- **Giữ nguyên thanh tiêu đề** của khối (có nút "Xem lịch sử" / "Thu gọn") — đây là khuôn của
  `currency-modal.vue`, `cost-modal.vue`. `hide-header` chỉ dùng cho popup mà **toàn bộ nội dung
  là lịch sử** (`CatalogHistoryModal`), vì ở đó tiêu đề popup đã nói rồi.
- Padding vùng nội dung `.si-body` = **`5px`**, không màn nào tự nới.
- Quy ước cũ "chi tiết mở dạng modal thì ẩn Lịch sử" **đã BỎ** từ 2026-08-15.
- Chi tiết BE/DTO/bộ lọc: skill `entity-history` mục 5.1 (danh mục dùng bảng chung `catalog_histories`,
  KHÔNG tạo bảng log riêng).

### b) CẤM: dòng `Người tạo: … • Ngày tạo: …` ở đáy body

```vue
<!-- SAI — bỏ hẳn, không comment lại để đó -->
<V2BaseMetaInfo v-if="id" variant="block"  :created-by="data.created_by_name" :created-at="data.created_at" />
<V2BaseMetaInfo v-if="id" variant="inline" :created-by="data.creator_name"    :created-at="data.created_at" />
```

Vì sao bỏ:

- **Trùng lặp**: khối Lịch sử ở (a) đã có dòng "Tạo mới — <người> — <thời điểm>" và cả các lần sửa sau đó.
- **Chữ in đậm sai chuẩn**: `V2BaseMetaInfo` render giá trị trong `<b>`, trong khi CLAUDE.md quy định
  nhãn thông tin là chữ xám `#6b7280` / giá trị `#374151`, **không in đậm**.
- **Đẩy footer**: thêm 1 khối có viền ở đáy body làm popup cao thêm, popup ngắn thì thừa khoảng trắng.
- **Mỗi màn một kiểu**: đo thật trong `hrm-client` — `industry-modal.vue`, `project-role-modal.vue`,
  `project_phase_modal.vue`, `application-modal.vue` + 5 modal `pages/master-data/*` đang render khối này,
  còn `meeting-type-modal.vue` thì **comment lại**, `currency-modal.vue` / `cost-modal.vue` thì không có.
  Cùng một nhóm danh mục mà 3 kiểu khác nhau.

**Popup dựng trên `V2BaseModal` thì KHÔNG dùng `V2BaseMetaInfo` nữa**: ai sửa / sửa lúc nào đã nằm
trong khối Lịch sử, và header chỉ còn đúng 1 dòng tiêu đề (mục 0). Chỉ popup CŨ còn `b-modal` thô
mới giữ chip cũ trên header:

```vue
<V2BaseMetaInfo v-if="id && data.updated_at" variant="chip" :updated-at="data.updated_at" />
```

### c) Tự kiểm (chạy ở thư mục client) — cả 2 lệnh phải RỖNG

```bash
# 1. không còn khối meta ở đáy body
grep -rn 'variant="block"\|variant="inline"' --include='*.vue' components pages

# 2. popup Xem/Sửa nào có `isShow`/`:id` mà không nhúng SystemInfoSection
for f in components/modal/**/*.vue; do grep -q "isShow" "$f" && ! grep -q "SystemInfoSection" "$f" && echo "THIẾU LỊCH SỬ: $f"; done
```

Popup cũ: dọn khi có dịp đụng vào màn đó, **không sửa đại trà** (QA phải nghiệm thu lại toàn hệ thống).

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
4. **Khung bảng** `flex: 1 1 auto; min-height: 0; overflow: auto` — KHÔNG đặt `max-height` cứng, cũng **KHÔNG đặt sàn `min-height` cứng** (sàn 160px làm khung không co nổi ở màn hình thấp, lại đẩy phân trang ra ngoài). ⚠️ Bảng bọc trong `V2BaseTableScroll` thì xem bẫy 9 bên dưới — khai nhầm lớp là rule **không chạy** mà không báo lỗi.
5. **Chiều cao dòng**: `td { padding: 3px 6px; font-size: 12px }`, ảnh thumbnail ≤ 26px, cột chữ dài bọc `.cell-clamp` (cắt 2 dòng) + `:title` tooltip, `thead` sticky.
6. **Nút phụ** ("Thêm hàng tạm"...) → slot `#header-actions` của `V2BaseSmartFilterPanel in-modal` (ngang hàng nút "Tìm kiếm nâng cao", không tốn dòng riêng; chỉ `btn-compact`, panel tự cách đều bằng `gap` — cấm `mr-2`/`ml-2`). Nút Tìm kiếm/Làm mới panel tự render (`showActionButtons`).
7. **Lọc nâng cao**: khai schema `filterFields` cho panel — KHÔNG tự dựng lưới ô lọc (mục 4c). Ô đặc thù (select tìm từ xa…) thì render qua slot `#field-<key>`.
8. **Control lẻ**: nhãn NGANG control (~32px) thay vì xếp chồng (~56px). Nén `::v-deep .tp-card` và `::v-deep .row.paging` (class `mt-3` tốn 24px).

**Verify BẮT BUỘC bằng số đo, không nhìn bằng mắt** — Playwright `browser_evaluate`, đếm số dòng
thấy đủ ở **2 trạng thái** (nâng cao đóng / mở) × **2 viewport** (1920×1080 / 1366×768), và
assert `modal-body.scrollHeight <= clientHeight` (bắt lỗi điểm 2+3 tái phát).

> **Bẫy select2 multiple**: ép `width:100%; float:none` mọi lúc → ô search **đè lên chip**.
> Chỉ ép ở trạng thái rỗng bằng `:only-child`. Xem `table-popup-layout.md`.

### Bẫy 9 — bọc bảng bằng `V2BaseTableScroll`: khai flex SAI LỚP (đã trả giá 2026-08-24)

`V2BaseTableScroll` render **2 lớp**: thẻ gốc `.v2-table-scroll` (chứa thanh cuộn trên) và
lớp trong `.v2-table-scroll__body` (nơi prop `body-class` được gắn vào). Con trực tiếp của
`.modal-body` là **lớp gốc**, không phải lớp trong.

Hai lỗi luôn đi cùng nhau:

- Khai `flex: 1 1 auto; min-height: 0` cho **lớp trong** → lớp gốc vẫn nở theo số dòng, đẩy
  đáy bảng **và cả thanh phân trang** xuống dưới đáy popup; `.modal-body { overflow: hidden }`
  nuốt luôn phần đó nên **user không thấy phân trang ở đâu**.
- Rule cho lớp trong còn **không hề chạy**: `<style scoped>` chỉ chạm được **thẻ gốc** của
  component con, muốn với tới lớp trong phải `::v-deep`. Sai âm thầm, không có cảnh báo nào.

```scss
/* ĐÚNG — flex ở lớp GỐC, ::v-deep cho lớp trong */
.modal-body ::v-deep > .v2-table-scroll {
    flex: 1 1 auto;
    min-height: 0;
    display: flex;
    flex-direction: column;
}
.modal-body ::v-deep .erp-table-wrap {   /* = body-class, tức .v2-table-scroll__body */
    flex: 1 1 auto;
    min-height: 0;
    overflow-y: auto;
}
```

**Cách tự kiểm (1 dòng, không nhìn bằng mắt)** — mở popup rồi chạy trong console:

```js
const card = document.querySelector('.modal-card')
const paging = card.querySelector('.row.paging')
paging.getBoundingClientRect().bottom <= card.getBoundingClientRect().bottom   // phải là true
```

### Bẫy 10 — chip select2 bị cắt mất ĐẦU chữ

Ô chọn nhiều có chip dài hơn ô: ô gõ tìm kiếm nằm **cuối** danh sách chip nên trình duyệt tự
cuộn khối `.select2-selection__rendered` sang phải → hiện ra `g cụ và thiết bị chuyên dùng`
thay vì `Dụng cụ và thiết bị chuyên dùng`. Nhìn như "mất text", thực ra là tràn ngang.

```scss
.filter-item ::v-deep .select2-selection--multiple .select2-selection__rendered {
    white-space: normal;            /* cho chip XUỐNG DÒNG thay vì tràn ngang */
}
.filter-item ::v-deep .select2-selection__choice {
    max-width: 100%;
    white-space: normal;
    word-break: break-word;
}
```

⚠️ **Vế sau bắt buộc đi kèm — nếu không sẽ đổi lỗi này lấy lỗi nặng hơn** (đã trả giá 2026-08-25):
cho chip xuống dòng mà **không chặn trần chiều cao** thì ô nở vô hạn theo số chip và **ăn hết chỗ
của bảng**. Đo thật ở popup chọn hàng hoá, màn 1200×813, chọn hết 17 "Tính chất hàng hoá":

| | Không chặn trần | Chặn 86px |
| --- | --- | --- |
| Cao ô lọc | 536px | 88px (cuộn trong ô) |
| Cao khối lọc | 722px | 274px |
| Khung bảng còn lại | **2px** | 277px |
| **Số dòng thấy được** | **0** | **6** |

Trần này nay nằm sẵn ở **`components/V2BaseSelect.vue`** (`max-height: 86px; overflow-y: auto` trên
`.select2-selection--multiple .select2-selection__rendered`) nên **mọi** select chọn nhiều — trong
popup lẫn bộ lọc màn danh sách — đều được chặn. **Đừng khai lại ở từng màn.**

Cách tự kiểm (mở popup, chọn thật nhiều rồi chạy trong console):

```js
const r = document.querySelector('.select2-selection--multiple .select2-selection__rendered')
r.getBoundingClientRect().height <= 90 && r.scrollHeight > r.clientHeight   // phải là true
```

Khuôn chip (màu, cỡ chữ, padding) vẫn do `V2BaseSelect` lo — ở đây **chỉ** chặn tràn.

📄 **CSS copy-paste đầy đủ + 7 bẫy đã trả giá + ngân sách chiều cao + snippet đo**:
xem `table-popup-layout.md` cùng thư mục.
File mẫu đang chạy: `pages/assign/quotations/components/QuotationProductSearchModal.vue`.

---

## 4b. Popup CHỌN BẢN GHI: click vào DÒNG là thêm ngay — và phải là MẶC ĐỊNH

Popup chọn hàng hoá / dịch vụ / thiết bị: **bấm vào dòng là thêm ngay bản ghi đó**, không bắt người
dùng tích checkbox rồi bấm nút. Checkbox vẫn giữ (có `@click.stop`) để thêm hàng loạt — click dòng
chỉ là lối tắt, không mất gì.

**Số dòng/trang của popup chọn: `[10, 20, 50, 100]`, mặc định 10** (user chốt 06/10/2026 theo QA
#11524). **Lấy từ hằng chung `utils/pickerPagination.js`**, KHÔNG gõ số tay:

```js
import { PICKER_PAGE_SIZE_OPTIONS, PICKER_DEFAULT_PAGE_SIZE } from '@/utils/pickerPagination'
// data: perPage: PICKER_DEFAULT_PAGE_SIZE, pickerPageSizeOptions: PICKER_PAGE_SIZE_OPTIONS
// <V2BasePagination :page-size-options="pickerPageSizeOptions" … />
```

Đã đồng bộ 34 popup chọn ngày 06/10/2026 (`.plans/gop-db/popup-chon-so-dong/`). Popup chỉ XEM (lịch sử,
drill báo cáo) giữ mục 4c.

### Bài học đắt hơn: hành vi chuẩn thì phải là MẶC ĐỊNH của component dùng chung

`ProductSearchModal` vốn đã dùng chung cho hơn 15 màn, nhưng hành vi này khai dạng **opt-in**
(`addOnRowClick`, mặc định `false`) "cho an toàn". Hậu quả: mỗi màn phải tự nhớ bật, màn nào quên
thì người dùng báo lại **đúng một lỗi ấy** — sửa ở Phiếu cung cấp thông tin (#11240) rồi lặp
nguyên xi ở Báo giá dịch vụ. Đổi mặc định thành `true` ngày 2026-08-28.

**Quy tắc rút ra, áp cho MỌI component dùng chung:**

- Hành vi đã chốt là chuẩn → đặt làm **giá trị mặc định**. Màn nào cần khác thì **tắt tường minh**
  và ghi lý do ngay tại chỗ.
- Đừng để mặc định "an toàn" rồi bắt từng màn bật: dùng chung mà vẫn phải nhớ cấu hình từng nơi thì
  chẳng khác gì copy code — vẫn sót, chỉ khác là sót ở chỗ khó thấy hơn.
- Sửa một hành vi trong component dùng chung xong, **quét ngay xem màn nào đang khai đè**:

```bash
grep -rn "add-on-row-click\|addOnRowClick" pages/ components/ | grep -v "<component>.vue"
# ra rỗng = mọi màn đang ăn theo mặc định, đúng ý đồ
```

---

## 4c. Popup có BỘ LỌC — dùng `V2BaseSmartFilterPanel in-modal`, KHÔNG tự dựng lưới ô lọc (chốt 2026-09-28)

Khuôn gốc: bộ lọc popup **"Thêm hàng hoá"** màn Báo giá
(`pages/assign/quotations/components/QuotationProductSearchModal.vue` :33-110 — dùng chung BOM + Báo giá).
Các popup đã bám đúng: `customer-care/services/components/ProductSearchModal.vue`,
`assign/meeting/components/PopupStaff.vue`, `assign/solutions/components/manager/*UpcomingModal.vue`,
`components/timesheet/shift-history/EmployeeShiftHistoryModal.vue`.

Popup nào có từ 1 ô lọc trở lên (popup chọn bản ghi, popup xem lịch sử, popup danh sách…) thì bộ lọc
là **đúng component bộ lọc của màn danh sách**, chỉ thêm `in-modal`:

```vue
<V2BaseSmartFilterPanel
    table="<khoá_riêng_của_popup>"        <!-- "Cài đặt bộ lọc" lưu theo khoá này -->
    floating                              <!-- nhãn nổi, giống màn danh sách -->
    in-modal                              <!-- BẮT BUỘC: ô chọn tự thành V2BaseSelectInModal -->
    title="Bộ lọc …"
    :filter-fields="filterFields"
    :filters="filters"
    :collapsed="filterCollapsed"
    :quickSearchValue="filters.keyword"
    quickSearchPlaceholder="Tìm theo <các trường BE thực sự lọc>"
    @toggle-panel="filterCollapsed = !filterCollapsed"
    @quick-search-change="(v) => (filters.keyword = v)"
    @filter-change="({ key, value }) => (filters[key] = value)"
    @search="handleSearch"
    @reset="handleReset"
>
    <template #header-actions>…nút phụ (Thêm hàng tạm…)…</template>
    <template #field-<key>>…ô đặc biệt (tìm từ xa V2BaseSelectRemote)…</template>
</V2BaseSmartFilterPanel>
```

- **`filterFields` khai y như màn danh sách** (skill `list-page`): select nhiều `multiple: true`;
  khoảng ngày GỘP 1 ô `type: 'date-range'` + `resetKeys: ['x_from', 'x_to']` + khai sẵn khoá
  `x_range` trong `filters` (Vue 2 không reactive khoá chưa khai); ô gõ tay đưa vào `ignoredFields`.
- **Ô tìm nhanh là BẮT BUỘC** (cùng dòng với nút Tìm kiếm / Làm mới — mặc định `inlineSearchButtons`).
  API chưa có tìm theo chữ thì **bổ sung tham số `keyword` ở BE** (tìm các cột chữ user nhìn thấy
  trong bảng), KHÔNG tắt ô tìm nhanh. Placeholder `Tìm theo <đúng các cột BE tìm>`.
- "Tìm kiếm nâng cao" **mặc định THU GỌN** (`filterCollapsed: true`) — dồn chỗ cho bảng.
- **Hành vi giống màn danh sách**: chọn ô select là tìm luôn (deep watcher `filters` + `oldFilters`);
  ô gõ tay chờ Enter / nút Tìm kiếm; "Làm mới" xoá hết rồi tìm lại; thu gọn nâng cao chỉ ẩn UI,
  KHÔNG xoá giá trị đã chọn.
- **Mở lại popup** (bản ghi khác) → reset `filters` về rỗng trước khi gọi API, và chặn watcher bắn
  thêm 1 lần lúc reset (cờ `silent`), nếu không mở popup gọi API 2 lần.
- **Danh mục cho ô chọn nạp lười**: gọi lần đầu mở popup rồi giữ lại, KHÔNG gọi ở `mounted` của màn cha
  (màn cha có thể không bao giờ mở popup). Ô "Người thực hiện"/"Người tạo" ưu tiên API trả đúng những
  người có trong dữ liệu, không tải toàn bộ nhân viên.
- **Khung popup**: dựng trên `V2BaseModal` (mục 0) + `dialog-class="<tên riêng>"` để ép khung cao
  cố định 98vw × 98vh theo **mục 4** (popup có bộ lọc luôn đi kèm bảng dữ liệu → luôn áp mục 4).
  ⚠️ `b-modal` bị dời ra `<body>` → rule cho `.modal-dialog` / `.modal-content` / `.v2-modal-body`
  phải để trong `<style>` **KHÔNG scoped**, có tiền tố class riêng của dialog (scoped/`::v-deep`
  không với tới — đo thật popup chỉ cao 358px). Mẫu: `EmployeeShiftHistoryModal.vue`.
- **Bảng trong popup = bảng GỌN của mục 4**, KHÔNG dùng `V2BaseDataTable` (nó bọc thêm card có tiêu
  đề "Danh sách" + padding, tốn ~60px và không co theo khung): `<div class="…-table-wrap">` (khối duy
  nhất `flex: 1; min-height: 0; overflow: auto`) chứa `<table class="table table-bordered table-hover
  table-sm mb-0">` — `thead` sticky, `td` `padding: 3px 6px; font-size: 12px`, cột chữ dài
  `.cell-clamp` + `:title`, dòng đang tải/trống màu xám `#6b7280` (KHÔNG `.text-muted` — ra đỏ);
  dưới bảng là `V2BasePagination` (`:page-size-options="[20, 50, 100]"`, dòng "Hiển thị x–y / N"). Riêng **popup CHỌN bản ghi**
  dùng `[10, 20, 50, 100]`, mặc định 10 — xem mục 4b.
  Badge trạng thái trong ô vẫn là `V2BaseBadge`, ô badge `text-nowrap`.
- **Footer popup chỉ xem**: KHÔNG truyền slot `#footer` → `V2BaseModal` tự render đúng nút chuẩn
  **Đóng** (`tertiary` + `fas fa-arrow-left`, mục 3). Tự khai lại dễ sai icon (`ri-close-line` là SAI).
- `QuotationProductSearchModal` tự dựng khung vì có trước `V2BaseModal` — copy **bộ lọc + bảng +
  phân trang**, không copy khung `.modal-backdrop-lite`.

🚫 **CẤM** tự dựng lưới ô lọc bằng `V2BaseLabel` + `V2BaseSelectInModal` + `V2BaseDatePicker` rời
(nhãn nằm trên, mỗi popup một cách xếp) — lệch kiểu với màn danh sách, mất "Cài đặt bộ lọc", mất
khoảng ngày gộp 1 ô, mất nút Tìm kiếm/Làm mới chuẩn. Cũng cấm dùng panel mà quên `in-modal`: ô chọn
khi đó là `V2BaseSelect`, dropdown bị modal cắt/che (mục 2).

## 5. Checklist khi tạo/review modal

- [ ] **Dựng trên `V2BaseModal`** (mục 0) — popup mới KHÔNG tự khai `b-modal` + header + footer
- [ ] **Footer ghim đáy, luôn nhìn thấy** kể cả khi nội dung dài (đo: `footer.getBoundingClientRect().bottom <= window.innerHeight`)
- [ ] **Body padding `0.5rem 0.75rem`** — dọc sát, ngang 0.75rem thẳng mép với header/footer (mục 0)
- [ ] **Header đúng 1 dòng**: icon + tiêu đề + nút ×, KHÔNG có dòng mô tả bản ghi (không truyền `subtitle`)
- [ ] Dùng `hide-footer` + tự viết `<div class="modal-footer">` (chỉ khi không dùng được `V2BaseModal`)
- [ ] Header có icon tròn + title + nút X
- [ ] Không dùng `no-close-on-backdrop`
- [ ] Button tuân thủ skill `button-convention` (variant, icon, thứ tự, size)
- [ ] Mọi select trong modal dùng `V2BaseSelectInModal`, KHÔNG dùng `V2BaseSelect`
- [ ] **Popup Xem bản ghi đã tồn tại: có khối "Lịch sử" (`SystemInfoSection`) ở CUỐI body**, `v-if="isShow && id"`, thu gọn sẵn, lazy load (mục 3c-a)
- [ ] **Đáy body KHÔNG có dòng `Người tạo / Ngày tạo`** — `V2BaseMetaInfo` chỉ được dùng `variant="chip"` ở header (mục 3c-b)

**Nếu popup có bộ lọc — thêm (xem mục 4c):**

- [ ] Bộ lọc là `V2BaseSmartFilterPanel` có `in-modal` + `floating` + `table="<khoá riêng>"` — KHÔNG tự dựng lưới `V2BaseLabel` + select rời
- [ ] CÓ ô tìm nhanh (thiếu thì thêm `keyword` ở BE), nâng cao thu gọn sẵn
- [ ] Bảng gọn `table-bordered table-sm` trong khung cuộn + `V2BasePagination` — KHÔNG `V2BaseDataTable`; khung 98vh (mục 4)
- [ ] Nút Đóng để `V2BaseModal` tự render (`fas fa-arrow-left`), không tự khai icon khác
- [ ] Khoảng ngày gộp 1 ô `type: 'date-range'`; chọn select là tìm luôn, ô gõ tay chờ Enter
- [ ] Mở lại popup reset bộ lọc mà không gọi API 2 lần; danh mục ô chọn nạp lười lúc mở lần đầu

**Nếu popup có bảng dữ liệu — thêm (xem mục 4):**

- [ ] `.modal-card` có `height: 98vh` (không chỉ `max-height`)
- [ ] `min-height: 0` đủ mọi mắt xích flex xuống tới bảng
- [ ] `.modal-body { overflow: hidden }`, chỉ khung bảng cuộn dọc
- [ ] Khung bảng `flex: 1 1 auto`, KHÔNG `max-height` cứng
- [ ] Cột chữ dài có `.cell-clamp` + `:title`; thumbnail ≤ 26px
- [ ] Nút phụ nằm trong slot `#header-actions`, không chiếm dòng riêng
- [ ] Lọc nâng cao dùng grid `auto-fit`, không chia hàng cứng
- [ ] **Đã ĐO số dòng bằng Playwright** ở cả 2 trạng thái nâng cao đóng/mở

### Bẫy: slot trong modal bị RỖNG từ lần mở thứ hai

`$slots` của Vue 2 **không phản ứng** khi bootstrap-vue dựng lại nội dung modal ở lần mở sau — nội
dung modal bị huỷ lúc đóng, mở lại thì `this.$slots.x` rỗng dù template vẫn khai slot đó. Hậu quả
thật đã gặp (2026-08-22): popup xác nhận dùng chung mở lần 2 trở đi thì nút **Xác nhận / Hủy mất
icon** — vì `V2BaseButton` khai `v-if="$slots.prefix"`.

Trong component đặt bên trong modal, luôn kiểm tra **cả hai**:

```vue
<div v-if="$slots.prefix || $scopedSlots.prefix">   <!-- ĐÚNG -->
<div v-if="$slots.prefix">                          <!-- SAI: mất từ lần mở thứ 2 -->
```

Vue 2.6 gộp mọi slot vào `$scopedSlots`, và biến này được cập nhật đúng ở mỗi lần render.
