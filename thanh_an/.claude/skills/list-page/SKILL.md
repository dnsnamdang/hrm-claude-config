---
name: list-page
description: Use when tạo/sửa MÀN DANH SÁCH trên hrm-thanhan-client (dns) — bộ lọc, bảng, cột Hành động, cấu hình cột, xuất Excel, phân quyền theo cấp. Phần A là chuẩn V2 (V2BaseSmartFilterPanel + V2BaseDataTable, port từ hrm) cho màn mới và phân hệ Cung ứng đang chuyển sang V2; Phần B là chuẩn cũ (b-collapse + base-select2) cho màn chưa lên V2. Đọc cả khi: filter chọn xong không tự tìm, quay lại màn mất bộ lọc, cột lệch/chữ mờ/ô có dấu —, xuất Excel sai cột.
---

# Màn danh sách — dns (hrm-thanhan-client)

> Bản dns của skill `list-page` bên hrm (`D:\laragon\www\hrm\.claude\skills\list-page\SKILL.md`).
> Chỉ giữ các quy tắc áp được cho dns; phần phụ thuộc thứ dns chưa có được ghi rõ ở bảng dưới.

## 0. Chọn phần nào?

| Màn đang làm | Dùng |
| --- | --- |
| Màn danh sách MỚI · màn phân hệ Cung ứng (`pages/supply/**`) đang chuyển sang V2 · màn đã import `v2-styles.scss` | **Phần A — chuẩn V2** |
| Màn cũ còn `b-collapse` + `base-select2` + `b-table`, chỉ sửa lỗi nhỏ, không có yêu cầu chuyển V2 | **Phần B — chuẩn cũ** (đừng chuyển nửa vời) |

Luôn đọc thêm: `button-convention` (nút toolbar + cột Hành động), `select-and-input-state` (select
trong bộ lọc), `modal-popup` (bộ lọc/bảng nằm trong popup).

## 0a. Khác biệt dns so với hrm — đọc trước khi chép code từ hrm

| hrm có | dns | Làm gì ở dns |
| --- | --- | --- |
| `this.$safeLoadingStart()` / `$safeLoadingFinish()` | **Không có** | `this.$nuxt?.$loading?.start?.()` / `finish?.()` — `finish` đặt trong `finally` |
| `this.$confirm()` | **Không có** | Thẻ `<BaseConfirmModal id="<id-riêng>">` (xem `button-convention` A6c) |
| `ExportColumnRegistry` + `DynamicExport` (BE) | **Không có** | Màn tự xuất theo `fields` (mục A12) |
| `CatalogHistoryModal` / `SystemInfoSection` / audit log | **Không có** | Không bắt buộc hành động "Lịch sử" (mục A5) |
| `V2BaseCompanyDepartmentFilter` | **Không port** | Cần lọc Công ty/Phòng ban → khai 2 field select thường trong `filterFields` + cascade ở watcher |
| `V2BaseFilterPanel` (panel cũ) | **Không có** | Chỉ dùng `V2BaseSmartFilterPanel` |
| Bảng `user_column_settings` | Cấu hình cột lưu ở `column_customizations` (mỗi màn 1 cột) | Màn mới cần cột mới trong bảng đó → hỏi user trước (đang treo Q2 của `.plans/ui-v2-cung-ung`) |
| `filter_customizations` | **Đã port** (route `/human/filter-customizations`) | Dùng như hrm |
| Phân quyền 3 cấp chung | dns KHÔNG đồng nhất (mục A1) | **Phải hỏi** trước khi thêm cấp |
| `.text-muted` đỏ | dns cũng đỏ | Dùng `#6b7280` (mục A9) |

---

# PHẦN A — CHUẨN V2

**Màn mẫu bên hrm:** `hrm-client/pages/master-data/product-natures/index.vue` (danh mục) và
`pages/assign/customers/index.vue` (cột Hành động). **Màn mẫu dns:** `pages/supply/purchase_orders/index.vue`
(sau khi thí điểm xong — `.plans/ui-v2-cung-ung`).

## A1. Phân quyền theo cấp — HỎI TRƯỚC, không tự thêm

CLAUDE.md: *"Trước khi làm màn danh sách mới → hỏi có cần phân quyền theo cấp không"* và *"Không tự
thêm phân quyền theo cấp"*. Khi hỏi, nói rõ màn thuộc nhóm nào:

| Nhóm | Cách viết BE | Cấp |
| --- | --- | --- |
| Module **Category** (Dự án) — màn mới | chuỗi `if/elseif $this->isCurrentEmployeeHasPermission(...)` trong Service | Tổng công ty (không lọc) → Công ty (`employee_infos.company_id`) → Nhóm nghiệp vụ (`listManageEmployeeIdsByGroup()`) → fallback bản thân (`created_by`) |
| Module **cũ** (Timesheet, Assign, Human, Training) | `checkPermissionList($query, [all, company, department, part/group, …], '<bảng>')` | 4 cấp, **có phòng ban** — đừng bỏ phòng ban nếu chưa hỏi |
| **Supply** (Cung ứng) hiện tại | `checkPermissionList($query, [PERM_VIEW, null, null, null, null], '<bảng>')` | Không phân cấp: có quyền xem là thấy tất cả |

- Quyền "xem tất cả" → lấy mọi bản ghi **trừ** trạng thái Đang tạo / Nháp của người khác.
- Có phân cấp thì bộ lọc bắt đầu bằng Công ty → Phòng ban (→ Bộ phận), cascade: đổi cha thì reset con.
- Chuyển màn sang V2 **giữ nguyên** logic quyền + cờ `is_can_*` BE đang trả; đổi UI không phải lý do đổi quyền.

## A2. Vỏ trang + style

```vue
<template>
    <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
        <div class="container-fluid">
            <V2BaseSmartFilterPanel … />
            <V2BaseDataTable … />
        </div>
    </div>
</template>

<style lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

- `pt-2` trong vỏ này **ra 0px là cố ý** (`v2-styles.scss` có `&.min-vh-100.pt-2 { padding-top: 0 !important }`). Đừng "sửa".
- Khoảng cách khối lọc → bảng = 12px do chính panel mang `mb-2`. **Màn không tự khai** `p-3`/`mt-*`/`mb-*` cho khối lọc.
- Import `v2-styles.scss` ở `<style lang="scss">` **không scoped**. Để trong `scoped` thì rule cho phần tử do component con render (`.d-contents`, `.v2-cell-link`…) không khớp — lỗi im lặng, màn này đúng màn kia vỡ.
- CSS cho phần tử của component X thì đặt trong `<style>` của X, đừng dựa vào `v2-styles.scss`.

## A3. Bộ lọc — `V2BaseSmartFilterPanel`, luôn `floating`

```vue
<V2BaseSmartFilterPanel
    table="supply_purchase_orders"
    floating
    :filter-fields="filterFields"
    :filters="filters"
    :collapsed="filterCollapsed"
    :quickSearchValue="filters.keyword"
    quickSearchPlaceholder="Tìm theo mã đơn, nhà cung cấp, người tạo"
    @toggle-panel="filterCollapsed = !filterCollapsed"
    @quick-search-change="filters.keyword = $event"
    @filter-change="handleFilterChange"
    @search="handleSearch"
    @reset="handleReset"
/>
```

```js
computed: {
    filterFields() {
        return [
            { key: 'status', label: 'Trạng thái', type: 'select', options: this.statusOptions },
            { key: 'supplier_ids', label: 'Nhà cung cấp', type: 'select', multiple: true, options: this.supplierOptions },
            { key: 'order_date', label: 'Ngày đặt hàng', type: 'date-range',
              resetKeys: ['order_date_from', 'order_date_to'], inputCount: 1 },
            { key: 'code', label: 'Mã đơn', type: 'text' },
        ]
    },
},
```

- `table` = khoá lưu cấu hình bộ lọc theo user (`filter_customizations`), đặt `<phân hệ>_<màn>` — Cung ứng dùng `supply_<màn>`.
- **Bộ lọc ĐỦ MỌI CỘT (user yêu cầu 30/09/2026)**: mỗi cột dữ liệu trên bảng (trừ STT, Hành động và **cột TIỀN** — Tổng tiền, Đơn giá, Thành tiền… KHÔNG làm ô lọc) phải có 1 ô lọc tương ứng trong `filterFields` — popup "Cài đặt bộ lọc" liệt kê đủ và **mặc định bật hết**, user tự tắt bớt. Kiểu ô theo kiểu dữ liệu cột: danh mục/trạng thái → select (người/NCC → chọn nhiều, option lấy từ API riêng nạp khi mở panel); ngày → `date-range`; số lượng → khoảng số `variant: 'range'`; mã/chữ → text. Thiếu API lọc ở BE thì bổ sung (dùng `$request->filled()` cho ô số để giá trị 0 vẫn lọc). Ô số trong slot phải thêm key từ/đến vào `ignoredFields` (chờ Enter). Mẫu: `pages/supply/purchase_orders/index.vue`.
- Ô lọc khai bằng **schema `filterFields`** (computed), không dựng markup tay. Chỉ ô cần logic riêng (tìm từ xa, cascade, khoá theo ô khác) mới dùng slot `#field-<key>`.
- **Slot `#field-*` KHÔNG tự vẽ `V2BaseLabel`** và không khai `hideLabel` cho ô đơn — để panel bọc nhãn floating. `V2BaseSelect`/`V2BaseSelectRemote` trong slot **bắt buộc `height="36px"`**.
- Chọn nhiều: `multiple: true` trên field — không viết slot riêng chỉ để bật multiple.
- Ô lọc bắt buộc (kỳ báo cáo…): `required: true`.
- **Khoảng "từ – đến" luôn là MỘT ô**: `type: 'date-range'` + `resetKeys: [từ, đến]` + `inputCount: 1`. Hai key gửi BE giữ nguyên. Cặp số/tiền: `variant: 'range'` + `resetKeys` + `inputCount: 1`, slot render 2 control + `<span class="ff__sep">→</span>`.
- **Ô gom nhóm** (nhiều ô trong 1 field) phải khai cả `resetKeys` (mọi khoá field đụng tới) **và** `inputCount` (số ô THẬT render ra). Panel đếm ô để quyết định chế độ gọn (≤ 3 ô kể cả tìm nhanh → bày 1 hàng, ẩn nút "Tìm kiếm nâng cao") — sai `inputCount` là panel không bao giờ vào chế độ gọn.
- Bộ lọc nằm trong **modal** → thêm prop `in-modal` (select dùng `V2BaseSelectInModal`, dropdown neo vào modal).
- Tiêu đề panel để mặc định "Bộ lọc danh sách", **không** truyền `title`/`subtitle` riêng.
- **Placeholder**: ô tìm nhanh = `Tìm theo <đúng các trường BE lọc>`; ô trong khối floating **bỏ placeholder trùng nhãn**, chỉ giữ khi nói thêm (`dd/mm/yyyy`, `Gõ để tìm…`). **Cấm** `Tất cả`, `-- Tất cả --`, `Chọn...`.
- Mọi ô trong panel cao đúng 36px. Tự kiểm trong console (phải ra mảng rỗng):

```js
(() => { const r = {}; document.querySelectorAll('.smart-filter-card .ff .ff__control')
  .forEach(c => { const b = c.getBoundingClientRect(); (r[Math.round(b.top)] ??= []).push(Math.round(b.height)) })
  return Object.entries(r).filter(([, h]) => new Set(h).size > 1) })()
```

## A4. Tìm tự động + giữ bộ lọc khi quay lại

**Luật chung:** ô CHỌN bằng chuột (select, ngày, chip) → chọn xong là tìm luôn. Ô GÕ TAY (text, số,
tiền, tìm nhanh) → **Enter mới tìm**, không bắn API theo từng ký tự.

```js
import filterStateMixin from '@/utils/mixins/filterStateMixin.js'
import { textFilterKeys } from '@/utils/filterAutoSearch'
import { mergeKnownFilters } from '@/utils/common'

const initialStateForm = { keyword: '', status: null, supplier_ids: [], order_date_from: null, order_date_to: null, code: '' }

export default {
    mixins: [filterStateMixin, columnCustomizationMixin, exportFieldsMixin],
    data() {
        return {
            loading: true,
            filters: { ...initialStateForm },
            oldFilters: {},
            filterCollapsed: true,
            // filterStateMixin — 4 field bắt buộc
            filterFieldName: 'filters',
            localStorageKey: 'supply_purchase_orders',          // duy nhất toàn project
            pathsToKeep: ['/supply/purchase_orders'],           // prefix show/edit
            expirationTime: 10 * 60 * 1000,
        }
    },
    computed: {
        // Khoá ô gõ tay KHÔNG kích watcher — sinh tự động từ schema
        ignoredFields() {
            return ['keyword', ...textFilterKeys(this.filterFields)]
        },
    },
    watch: {
        filters: {
            handler(newVal) {
                const shouldCallApi = !this.ignoredFields.some((f) => newVal[f] !== this.oldFilters[f])
                if (shouldCallApi) {
                    this.pagination.currentPage = 1
                    this.loadData()
                }
                this.oldFilters = JSON.parse(JSON.stringify(this.filters))
            },
            deep: true,
        },
    },
    created() {
        const saved = this.loadFilterState()
        if (saved) {
            this.filters = mergeKnownFilters(initialStateForm, saved.filter)
            if (saved.filterCollapsed !== undefined) this.filterCollapsed = saved.filterCollapsed
        }
        this.oldFilters = JSON.parse(JSON.stringify(this.filters))
        this.loadData()     // request đầu tiên, không await gì (mục A13)
    },
}
```

- `handleSearch` gọi `loadData()` (vì keyword nằm trong `ignoredFields`). `handleReset`/`handleSort` chỉ đổi `filters`, watcher tự tải. Đổi trang/số dòng gọi `loadData()` trực tiếp.
- `mergeKnownFilters` bỏ khoá lạ trong bộ lọc đã lưu (màn đổi schema không làm hỏng lần vào sau).
- Ô gõ tay do màn tự render trong slot `#field-*` → màn tự gắn `@keyup.enter.native="handleSearch"`.
- Màn vào được từ nhiều link (`?type=all`…): nạp bộ lọc đã lưu TRƯỚC, áp query SAU; whitelist giá trị; "Làm mới" giữ phạm vi. BE vẫn tự gate quyền.
- **Ngoại lệ**: màn báo cáo nặng giữ nếp bấm "Tìm kiếm".
- Tự kiểm: chọn 1 giá trị ở mỗi select → thấy request mới; gõ ô chữ rồi Enter → thấy request mới; vào chi tiết rồi Quay lại → bộ lọc còn nguyên.

## A5. Toolbar + cột Hành động

Chi tiết nút ở `button-convention` Phần A. Tóm tắt phần thuộc màn danh sách:

- Toolbar bắt buộc đủ: **Tạo mới → (Import Excel) → Xuất Excel → Cấu hình cột** (nút cuối chỉ có icon `ri-layout-column-line`, `title="Cấu hình cột hiển thị"`). Tạo mới/Import gate theo quyền; **Xuất Excel và Cấu hình cột KHÔNG gate**.
- Cột **Hành động luôn cuối bảng**, dùng `V2BaseRowActions`:

```vue
<template #cell-actions="{ item }">
    <V2BaseRowActions :actions="getRowActions(item)" @action="handleRowAction({ action: $event, item })" />
</template>
```

```js
getRowActions(item) {
    return [   // 2 phần tử đầu là nút chính, còn lại vào menu ⋮
        { key: 'edit', title: 'Sửa', icon: 'ri-edit-line', to: `/supply/purchase_orders/${item.id}/edit`,
          visible: !!item.is_can_edit },
        { key: 'delete', title: 'Xóa', icon: 'ri-delete-bin-line', danger: true, visible: !!item.is_can_delete },
    ]
}
```

- Tối đa 3 nút/dòng (2 chính + `⋮`). Chuyển trang → khai `to` (render `nuxt-link`, chuột phải mở tab mới). Mở modal/gọi API → không `to`, nghe `@action`.
- **Không có** "Xem" (Mã là link vào chi tiết), "Hủy phiếu", "Không duyệt" ở danh sách. "Duyệt" nếu giữ thì là `to` sang chi tiết.
- Không dùng được → **ẨN** (`visible: false`), không hiện rồi disable. Cờ quyền fail-closed.
- Điều kiện `is_can_delete` / `is_can_edit` → **HỎI user** (CLAUDE.md), không tự quyết.
- Hành động "Lịch sử": hrm bắt buộc, **dns chưa có audit log chung** → chỉ thêm khi màn đã có nguồn lịch sử (vd `HistoryApproveModal`). Không bịa nút rỗng.
- Cột Hành động khai `locked: true`, luôn cuối; không cho ẩn/kéo.

## A6. Cột định danh (Mã) + Tên

- Mã và Tên là **2 cột riêng**. Mã là link vào chi tiết, `locked: true` + `sticky: true`; Tên chữ thường, không khoá, không sticky.

```vue
<template #cell-code="{ item }">
    <nuxt-link :to="`/supply/purchase_orders/${item.id}`" class="v2-cell-link field-line">{{ item.code }}</nuxt-link>
</template>
```

- Màn danh mục mở bằng modal (không có route chi tiết) → `<button type="button" class="v2-cell-link field-line" @click="openView(item)">`. Bảng không có mã hoặc có bản ghi trống mã → cột định danh là Tên.
- **Cấm** `<a href="javascript:void(0)" @click="$router.push(...)">`.
- Ô tham chiếu sang bảng khác (Nhà cung cấp, Dự án…) hiện `MÃ - Tên` trong MỘT ô; tiêu đề cột nói đủ ("Nhà cung cấp"). Sort ô ghép phải theo đúng chuỗi hiển thị (mã rồi tên) — không làm được thì bỏ `sortable`.

## A7. Thứ tự cột, bộ cột mặc định, popup cấu hình cột

Thứ tự: `STT → Mã → Tên → [cột nghiệp vụ] → Người tạo → Ngày tạo → Trạng thái → Hành động`.

- **Mặc định chỉ hiện 7 cột** như trên. Cột nghiệp vụ khác vẫn khai đủ trong `allColumns` nhưng `isVisible: false`. Ngoại lệ: cột Khách hàng / Nhà cung cấp / Loại phiếu được hiện mặc định (thiếu thì không đọc nổi dòng là gì).
- Nhãn luôn **"Người tạo" / "Ngày tạo"** — cấm "Người lập", "Ngày lập", "Người lập phiếu" ở cột, ô lọc, trường xuất, bản in.
- Người tạo: chỉ TÊN. Ngày tạo: `dd/mm/yyyy HH:mm` (không giây). Trường chỉ nhập ngày → chỉ hiện ngày, không kèm `00:00`.
- BE lấy tên người tạo bằng **subquery** (không leftJoin làm chậm COUNT phân trang).
- Popup cấu hình cột: `columnCustomizationMixin` (dns, bản V2) — khai `columnScreenKey`, đổi computed cột thành `allColumns`, gọi `loadColumnFields()`, đặt `<ColumnCustomizationModal>` (mixin đã đăng ký component `v2-column-customization-modal`). Modal cũ `column-customization-modal.vue` giữ cho màn cũ.
- `locked: true` cho STT, Mã, Hành động — vẫn hiện trong popup nhưng xám + tick sẵn.
- Cột STT: `width` + `minWidth` = `60px` (sticky cộng dồn width để tính `left`). Cột ngay sau nhóm sticky **không** khai sticky.
- Dời cột đã tồn tại sang vị trí mới → đổi `key` để cấu hình đã lưu coi là cột mới.

## A8. Căn lề + bề rộng

| Loại cột | `align` | Bề rộng |
| --- | --- | --- |
| STT | center | 60/60 |
| Badge trạng thái | center | 130 |
| Hành động | center | 140 |
| Chữ, ngày, mã | left (không căn phải mã) | — |
| Số lượng, tiền | right | — |

- Màn **≥ 10 cột**: bật `fixed-layout` trên `V2BaseDataTable`, khai `width` + `minWidth` cho MỌI cột theo bậc S 130–150 · M 170–190 · L 220–260 · XL 300. Cột chữ dài: `cellClass: 'text-wrap clamp-2'` + `:title` đầy đủ.
- Màn danh mục ít cột: STT 60/60 · Tên 220/180 · Mô tả 300/240 · Người tạo 150/140 · còn lại 120/110.
- Bảng tràn ngang: `V2BaseDataTable` đã có thanh cuộn trên (đồng bộ 2 chiều). Bảng viết tay trong form/modal bọc `V2BaseTableScroll` — không tự chép cặp `topScroll`.

## A9. Màu chữ, ô trống, badge

| Mức | Class | Màu |
| --- | --- | --- |
| Cột định danh | `v2-cell-link field-line` | navy `#28539d`, gạch chân đứt |
| Nội dung chính | `field-line text-dark font-weight-normal` | `#343a40` |
| Dòng phụ | `project-sub v2-hint` (`.v2-hint { color: #6b7280 }` khai ở màn) | `#6b7280` |

- `.field-line` trần ra xám `#475569` — bẫy chữ mờ.
- **Không in đậm** trong ô bảng, kể cả cột Mã.
- **`.text-muted` ở dns ra màu ĐỎ** → dùng `#6b7280`. Đỏ chỉ dành cho lỗi validate.
- **Ô trống để trống** — cấm `—`, `-`, `N/A`. Rà cả chi tiết, popup, bản in/xuất, BE Resource. Hàm trả giá trị hiển thị `|| ''`.
- ⚠️ **Bẫy ô hiện `[]` / giá trị thô**: slot `#cell-xxx` của `V2BaseDataTable` mà **phần tử gốc có `v-if` không kèm `v-else`, hoặc có `v-for`** → khi điều kiện sai / mảng rỗng, Vue 2 coi slot rỗng và render **nội dung mặc định** (`getNestedValue(item, key)`) ⇒ cột mảng ra `[]`, cột object ra `{...}`. Gốc slot luôn render (`<div>` trần, đặt `v-if`/`v-for` ở phần tử con). Gặp thật ở cột Phiếu đề xuất màn HĐ kết xuất (06/10/2026).
- Badge: `V2BaseBadge`, không tự dựng pill. Danh mục 2–3 trạng thái cố định → `variant="brand|required|muted"`. Đối tượng nghiệp vụ nhiều trạng thái → `:color="item.status_color"` do BE trả (hằng `STATUSES` trên Entity có `color`). Chữ lấy `status_text` từ BE.
- **9 mã màu chuẩn**: Hoàn thành/Đã duyệt `#16A34A` · Đang thực hiện/Đã gửi `#2563EB` · Chờ duyệt/Chờ xử lý `#D97706` · Cảnh báo/Tạm dừng `#F59E0B` · Từ chối/Quá hạn/Khoá `#DC2626` · Theo dõi/Mới tiếp nhận `#0EA5E9` · Chốt/Thương thảo `#7C3AED` · Nháp/Đang tạo `#64748B` · Đã đóng/Đã huỷ `#6B7280`. Trạng thái mới gán vào nhóm có sẵn, không tạo màu mới. Mức ưu tiên là thang riêng: `#94A3B8` → `#F59E0B` → `#F97316` → `#DC2626`.
- Badge không bấm được; cùng bản ghi phải ra cùng chữ + màu ở danh sách, chi tiết, bản in, file Excel.

## A10. Sort + tìm nhanh (BE)

- Sort chỉ cho cột Mã, Tên, tiền, ngày. Key FE phải nằm trong whitelist `SORTABLE_COLUMNS` (map key FE → cột DB) ở Service; key lạ → `id desc`.
- Nối bảng để sort thì **bắt buộc** `->select('<bảng chính>.*')` + `leftJoin` — thiếu là cột trùng tên bị đè, file xuất sai mà không báo lỗi.
- Luôn có `id desc` cuối cùng (không thì lật trang lặp/mất dòng).
- Tìm nhanh (`keyword`) theo Mã, Tên, Người tạo — placeholder ghi đúng các trường đó. Tìm người tạo dùng `whereExists` (không join).
- Tuỳ chọn: xếp theo độ khớp (khít → bắt đầu bằng → đầu từ → chứa) khi keyword ≥ 2 ký tự và user chưa bấm sort — khuôn `CustomerService::applyRelevanceOrder()` bên hrm.
- Màn chậm → đo API trước, soi index của mọi cột trong `where`/`EXISTS`. Tên index tự đặt ngắn (trần 64 ký tự). Migration chỉ index, **không foreign key**; DDL không bọc `DB::transaction`.

## A11. Dòng đếm + phân trang

- Dòng đếm chỉ có số: `Hiển thị 1–10 / 17542` (không kèm tên đối tượng).
- Số dòng/trang 5/10/20/50/100 (mặc định sẵn của `V2BaseDataTable`/`V2BasePagination`) — đừng khai riêng.
- Kiểu chữ phân trang thống nhất (12px, `#6b7280`, en dash) — đã nằm trong component.

## A12. Xuất Excel qua popup chọn trường

Bắt buộc hỏi user chọn cột trước khi xuất: `exportFieldsMixin` + `ExportFieldsModal`
(`components/modal/export-fields-modal.vue`). ⚠️ Mixin KHÔNG tự đăng ký component — màn phải
`import ExportFieldsModal from '@/components/modal/export-fields-modal.vue'` và khai trong `components`.

```vue
<ExportFieldsModal :modal-id="exportFieldsModalId" :columns="exportFields"
    :default-selected="visibleExportFields" :exporting="exporting" @export="handleExportFields" />
```

```js
computed: {
    exportFields() {   // id = key cột trong file
        return [{ id: 'code', name: 'Mã đơn' }, { id: 'supplier_text', name: 'Nhà cung cấp' }, /* … */]
    },
},
methods: {
    // mixin gọi runExport(type, fields) — fields là MẢNG key theo thứ tự user tick
    async runExport(type, fields) { … },
},
```

- **Không khai đè `handleExportFields`** — cắt mất mắt xích; tham số là mảng key, không phải `{ fields }`.
- Popup tick sẵn đúng các cột đang hiện (`visibleExportFields`): mixin tự thử hậu tố `_text` và snake_case; còn lệch thì khai `exportFieldKeyMap`.
- **dns chưa có `ExportColumnRegistry`/`DynamicExport`.** Chọn một trong hai, giữ nhất quán trong phân hệ:
  1. **BE**: route `GET /<màn>/export` khai **TRƯỚC** `/{id}`; service dùng lại ĐÚNG query danh sách (`getList($request)` không paginate) rồi chỉ ghi các cột trong `fields`; FE gọi `downloadExcel(this.$axios, '<url>/export' + buildQueryString({ ...params, fields: fields.join(',') }), '<tên>.xlsx')`.
  2. **FE** (phân hệ Cung ứng đã có `utils/supply-excel-export.js` dùng ExcelJS): lấy toàn bộ dòng theo bộ lọc hiện tại (không phân trang), map theo `fields`.
- Kiểm file: dòng 1 là tiêu đề tiếng Việt; thấy `{"data":[` là gọi nhầm endpoint danh sách. Trạng thái xuất ra chữ, không ra số.
- Không ẩn nút Xuất/In theo quyền xem.

## A13. Thứ tự request khi vào màn

- `data()` để `loading: true` → bảng hiện spinner ngay.
- `created()`: `loadData()` là request **đầu tiên**, không await gì. Cấu hình cột, quyền chạy song song; cấu hình cột về sau mà cần cột BE join thêm thì mới nạp lại.
- Options của khối nâng cao **hoãn tới khi mở panel** (`loadFilterOptions()` + cờ `filterOptionsLoaded`). **Không** hoãn `filter-customizations` và không gate nội dung panel bằng `v-if`.
- `loadData()` tăng `loadSeq`, bỏ response cũ nếu `seq !== this.loadSeq`.
- Không gọi thẳng `this.$nuxt.$loading.start()` ở đầu `created/mounted` (chưa sẵn sàng → TypeError, màn trắng). Dùng `this.$nuxt?.$loading?.start?.()` và `finish?.()` trong `finally`.
- Màn chi tiết/sửa: request bản ghi nằm cùng `Promise.all` với danh mục. Hàm nạp options ghi đè mảng thì giữ option đang chọn và chèn lại sau khi cả hai xong.

## A14. Màn chi tiết đi kèm + quay về danh sách

- Tiêu đề `Chi tiết <đối tượng>: <mã>` (chưa có dữ liệu thì tiêu đề trần; bảng không có mã thì không ghép tên).
- 403/404 → `this.$router.replace({ path: '/extras/404' })` (dns: `pages/extras/404.vue`; màn cũ viết `'pages/extras/404'` không có `/` đầu là sai đường dẫn tương đối), không toast rồi đẩy về danh sách. Dùng `replace` để bấm Quay lại không lặp vào 404.
- Footer dùng `V2Footer` (không tự dựng khối nút); hành động + **điều kiện hiện** giống hệt dòng ở danh sách (đọc cùng cờ `is_can_*`).
- Lưu/Duyệt/Từ chối/Hủy/Xóa xong → `$router.push('<danh sách>')`. Khóa/Mở khóa trên dòng → ở lại, cập nhật state tại chỗ. `url-back` trỏ về nơi user đi vào.
- Trường link sang chứng từ khác trong màn chi tiết nằm trong khung ô `.v2-linked-field`, không để link trần.

## A15. Bộ tự kiểm trước khi báo xong

```bash
cd hrm-thanhan-client
F=pages/<phân hệ>/<màn>/index.vue
grep -n "Người lập\|Ngày lập" $F                 # rỗng
grep -n "text-muted" $F                           # rỗng
grep -n "'—'\|\"—\"\|>—<" $F                      # rỗng
grep -n "vi-VN" $F                                # rỗng — định dạng ngày/tiền dùng helper chung
grep -n "resetKeys" $F; grep -n "inputCount" $F   # field gom nhóm/range phải có cả hai
grep -n "#field-" -A 6 $F | grep V2BaseLabel      # rỗng
grep -n "v2-styles.scss" $F                       # có, trong <style> không scoped
grep -n "id=\"confirm\"" $F                       # rỗng — trùng id với V2Footer
grep -o 'class="field-line[^"]*"' $F | sort | uniq -c   # field-line trần = 0
```

Đối chiếu `allColumns` với `filterFields`: cột dữ liệu nào (trừ cột tiền) chưa có ô lọc → bổ sung (xem A3).

Trên trình duyệt: chọn từng select → có request; Enter ở ô chữ → có request; Cài đặt bộ lọc tắt
còn ≤ 3 ô → panel nhảy về hàng ngang; cấu hình cột lưu + F5 còn; xuất Excel đúng cột đang hiện;
vào chi tiết → Quay lại còn bộ lọc. **Không tự chạy Playwright** nếu user chưa bảo.

---

# PHẦN B — CHUẨN CŨ (màn chưa lên V2)

Chỉ dùng khi sửa màn cũ mà không có yêu cầu chuyển V2:

- Phân quyền theo cấp như mục A1 (hỏi trước khi thêm).
- Bộ lọc: `<b-button v-b-toggle>` + `<b-collapse>`.
- **Không dùng `<input>` / `<select>` native**: select → `base-select2` (options `{ id, text }`, `:settings="{ allowClear: true }"`); ô tìm kiếm → `b-form-input`. allowClear trả `null` → guard filter dùng truthy, không so `''`.
- Cột Thao tác của màn cũ: theo `button-convention` Phần B (bánh răng, `rowActions`).
- Vẫn áp các luật không phụ thuộc component: ô trống không `—`, không `.text-muted`, "Người tạo/Ngày tạo", sort whitelist, `id desc` cuối, không foreign key.
