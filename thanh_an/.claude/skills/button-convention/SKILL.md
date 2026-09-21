# Button Convention — HRM Thành An

## Mục đích
Chuẩn hóa cách bày **nút bấm** trên FE `hrm-thanhan-client` (Bootstrap-Vue 2 + `b-button`)
để mọi màn trông giống nhau và cột Thao tác không bị tràn nút.

## Khi nào dùng
- Thêm / bớt / sắp xếp lại nút trong cột **Thao tác** của màn danh sách (`<b-table>`), kể cả khi chỉ thêm 1 nút
- Dựng cột Thao tác cho màn danh sách mới

---

# 1. Cột "Thao tác" của màn danh sách

## Quy tắc (chuẩn theo màn `pages/contract/contract/index.vue`)

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

## Cách làm

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

## Bẫy hay gặp

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

## Màn tham chiếu

- `pages/contract/contract/index.vue` — bản gốc của quy tắc (nút ngoài + bánh răng 4 mục)
- `pages/supply/supply_proposals/inbox.vue` — bản dùng mảng `rowActions()` động
- Toàn bộ phân hệ Cung ứng đã chuẩn hóa theo mẫu này (18/09/2026):
  `supply/contract_render`, `supply/purchase_contracts`, `supply/purchase_orders`,
  `supply/supply_handlings`, `supply/supply_proposals/index` + `inbox`
