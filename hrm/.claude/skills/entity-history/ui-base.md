# UI base cho "Lịch sử thay đổi" (chuẩn: màn Khách hàng)

Base chốt ngày 2026-08-12. **Copy nguyên, không tự chế biến thể.**

File thật đang chạy:

- Popup (mở từ menu ⋮ màn danh sách): `hrm-client/components/assign/customer/CustomerHistoryModal.vue`
- Mục "Lịch sử" trong màn chi tiết (dùng chung nhiều màn): `hrm-client/components/assign/SystemInfoSection.vue`

**Phải làm CẢ HAI** (như màn Khách hàng), và hai nơi này **hiển thị y hệt nhau** (bố cục mục log,
text, màu, bộ lọc, thứ tự mới → cũ). Khác nhau duy nhất: popup có vỏ `b-modal`, section có header
thu gọn/mở rộng + lazy load lần mở đầu tiên.

---

## 1. Vỏ popup

```vue
<b-modal
    :visible="show"
    scrollable
    size="lg"
    body-class="p-0"
    content-class="shadow"
    hide-footer
    @hidden="$emit('close')"
>
    <template #modal-header>
        <div class="d-flex align-items-center w-100">
            <div
                class="d-flex align-items-center justify-content-center mr-2"
                style="width: 28px; height: 28px; border-radius: 999px; background: rgba(26, 188, 156, 0.1); color: #1abc9c"
            >
                <i class="ri-history-line" style="font-size: 16px"></i>
            </div>
            <div>
                <h5 class="modal-title mb-0" style="font-size: 14px; font-weight: 800">Lịch sử khách hàng</h5>
                <div v-if="customerName" class="mt-1" style="font-size: 11px; color: #6b7280">
                    Khách hàng: <span style="font-weight: 600; color: #374151">{{ customerName }}</span>
                </div>
            </div>
        </div>
        <button type="button" class="close" @click="$emit('close')">
            <span aria-hidden="true">&times;</span>
        </button>
    </template>

    <div class="px-3 pb-3 pt-2"> <!-- BODY --> </div>

    <div class="modal-footer">
        <V2BaseButton tertiary size="sm" @click="$emit('close')">
            <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
            Đóng
        </V2BaseButton>
    </div>
</b-modal>
```

- Title: `Lịch sử <đối tượng>` (VD "Lịch sử khách hàng"). Dòng phụ: `<Tên đối tượng>: <mã - tên>`.
- Cho phép click backdrop đóng (KHÔNG `no-close-on-backdrop`). Footer chỉ nút **Đóng**.

## 2. Bộ lọc (client-side, y hệt ở cả 2 nơi)

Nút bật/tắt đặt góc phải trên danh sách, chỉ hiện khi đã tải xong và CÓ log:

```vue
<div class="d-flex justify-content-end">
    <V2BaseButton secondary size="sm" @click="showFilter = !showFilter">
        <template #prefix><i class="ri-filter-3-line" style="font-size: 15px"></i></template>
        Bộ lọc
    </V2BaseButton>
</div>

<b-collapse v-model="showFilter" class="mt-1">
    <div class="ch-filter-bar form-row">
        <div class="col-md-3 mb-2">
            <V2BaseLabel>Loại hành động</V2BaseLabel>
            <V2BaseSelectInModal v-model="filters.action" :options="actionOptions" :allowClear="true"
                placeholder="Tất cả loại hành động" />
        </div>
        <div class="col-md-3 mb-2">
            <V2BaseLabel>Người thực hiện</V2BaseLabel>
            <V2BaseSelectInModal v-model="filters.performer" :options="performerOptions" :allowClear="true"
                placeholder="Tất cả người thực hiện" />
        </div>
        <div class="col-md-3 mb-2">
            <V2BaseLabel>Từ ngày</V2BaseLabel>
            <V2BaseDatePicker v-model="filters.dateFrom" type="date" value-type="YYYY-MM-DD"
                format="DD/MM/YYYY" size="sm" placeholder="Từ ngày" />
        </div>
        <div class="col-md-3 mb-2">
            <V2BaseLabel>Đến ngày</V2BaseLabel>
            <V2BaseDatePicker v-model="filters.dateTo" type="date" value-type="YYYY-MM-DD"
                format="DD/MM/YYYY" size="sm" placeholder="Đến ngày" />
        </div>
        <div class="col-12 text-right mt-1">
            <V2BaseButton primary size="sm" class="mr-2" @click="applyFilter">
                <template #prefix><i class="ri-search-line" style="font-size: 15px"></i></template>
                Tìm kiếm
            </V2BaseButton>
            <V2BaseButton tertiary size="sm" @click="resetFilters">
                <template #prefix><i class="ri-refresh-line" style="font-size: 15px"></i></template>
                Làm mới
            </V2BaseButton>
        </div>
    </div>
</b-collapse>
```

Logic (copy nguyên):

```js
// Options dựng TỪ CHÍNH log đang có, không hardcode danh sách action
actionOptions() {
    const map = new Map()
    this.items.forEach((log) => {
        if (log.action && !map.has(log.action)) map.set(log.action, log.action_label || log.action)
    })
    return Array.from(map, ([value, text]) => ({ value, text }))
},
// DTO log KHÔNG trả id nhân viên → gom theo mã NV, không có mã thì theo họ tên
performerKey(log) { return log.actor_code || log.actor_name || '' },
filteredHistory() {
    const f = this.appliedFilters
    return this.items.filter((log) => {
        if (f.action && log.action !== f.action) return false
        if (f.performer && this.performerKey(log) !== f.performer) return false
        const day = log.created_at_raw ? log.created_at_raw.slice(0, 10) : null   // 'YYYY-MM-DD'
        if (f.dateFrom && (!day || day < f.dateFrom)) return false
        if (f.dateTo && (!day || day > f.dateTo)) return false
        return true
    })
},
```

Quy tắc:

- Có 2 bộ state: `filters` (đang nhập) và `appliedFilters` (đã áp) — **bấm Tìm kiếm mới lọc**.
- `Làm mới` = reset cả 2 (không phải tải lại API).
- Reset lọc + đóng thanh lọc khi: mở popup, đổi entity, tải lại danh sách.
- Dùng `V2BaseSelectInModal` kể cả khi component nằm ngoài modal (nó tự bỏ qua `dropdownParent` nếu không có `.modal-content`).

## 3. Trạng thái rỗng / lỗi

| Trạng thái | Markup |
| --- | --- |
| Đang tải | `<div class="text-center py-5"><div class="spinner-border text-primary" role="status">…` |
| Lỗi tải | text đỏ `Không tải được lịch sử <đối tượng>.` + `V2BaseButton tertiary size="sm"` icon `ri-refresh-line` chữ **Thử lại** |
| Chưa có log | icon `ri-history-line` 40px + `Chưa có lịch sử thay đổi.` (mục trong màn chi tiết: `Chưa có lịch sử thao tác nào.`) |
| Lọc không ra | icon `ri-filter-off-line` 32px + `Không có lịch sử phù hợp bộ lọc.` |

Khối rỗng: `class="text-center py-5"` + `style="color: #9ca3af; font-style: italic"`.

## 4. Timeline một mục log

```vue
<ul class="ho-timeline">
    <li v-for="(log, i) in filteredHistory" :key="'ch-' + (log.id || i)" class="ho-timeline-item">
        <div class="ho-timeline-dot" :style="dotStyle(log.action_color)"></div>
        <div class="ho-timeline-content">
            <div class="ho-timeline-time">{{ log.created_at || '—' }}</div>
            <div class="ho-timeline-text font-weight-bold" :style="{ color: log.action_color }">
                {{ log.action_label || log.action || '—' }}
            </div>
            <div class="ho-timeline-actor">
                Người thực hiện: {{ actorText(log) }}
                <span v-if="log.department_name"> — {{ log.department_name }}</span>
            </div>
            <!-- khối thay đổi (mục 5) -->
            <div v-if="log.note" class="ho-timeline-note"><i class="ri-chat-quote-line mr-1"></i>{{ log.note }}</div>
        </div>
    </li>
</ul>
```

```js
dotStyle(color) { const hex = color || '#9ca3af'; return { background: hex + '22', borderColor: hex } },
actorText(log) {
    const parts = []
    if (log.actor_code) parts.push(log.actor_code)
    if (log.actor_name) parts.push(log.actor_name)
    return parts.length ? parts.join(' - ') : 'Hệ thống'   // KHÔNG dùng '—'
},
```

Thứ tự trong 1 mục là **cố định**: thời gian → tên hành động → người thực hiện → thay đổi → ghi chú.
Không có người thực hiện ghi `Hệ thống`; không có phòng ban thì **ẩn hẳn**, không in `—`.

## 5. Khối thay đổi

```vue
<div v-if="log.changes && log.changes.length" class="mt-2">
    <div v-for="(c, ci) in log.changes" :key="ci" class="change-item">
        <span class="change-field">{{ c.field }}:</span>

        <!-- Khoá dạng danh sách/bảng: ~ sửa, - bỏ, + thêm -->
        <div v-if="hasListChange(c)" class="change-list">
            <div v-for="(m, mi) in c.changed" :key="'m-' + mi" class="change-modified">
                ~ {{ m.name }}:
                <span v-for="(fc, fi) in m.fields" :key="'f-' + fi">
                    {{ fc.field }}:
                    <span class="change-old">{{ fc.old }}</span>
                    <i class="ri-arrow-right-line mx-1 text-muted"></i>
                    <span class="change-new">{{ fc.new }}</span>
                    <template v-if="fi < m.fields.length - 1">; </template>
                </span>
            </div>
            <div v-for="(v, vi) in c.removed" :key="'r-' + vi" class="change-old">- {{ v }}</div>
            <div v-for="(v, vi) in c.added" :key="'a-' + vi" class="change-new">+ {{ v }}</div>
        </div>

        <!-- Trường thường: cũ → mới -->
        <template v-else>
            <span v-if="c.old" class="change-old">{{ c.old }}</span>
            <i v-if="c.old" class="ri-arrow-right-line mx-1 text-muted"></i>
            <span class="change-new">{{ c.new || '(trống)' }}</span>
        </template>
    </div>
</div>
```

```js
hasListChange(change) {
    return ['removed', 'added', 'changed'].some((key) => change[key] && change[key].length)
},
```

Quy ước dấu và thứ tự in: **`~` (sửa) → `-` (bỏ) → `+` (thêm)`**.
Giá trị trống in `(trống)`. Nhiều trường trong 1 bản ghi sửa ngăn bằng `; `.

## 6. Bảng màu + kích thước (không đổi tuỳ hứng)

| Thành phần | Giá trị |
| --- | --- |
| Giá trị CŨ `.change-old` | `#dc2626`, `word-break: break-word` |
| Giá trị MỚI `.change-new` | `#16a34a`, `font-weight: 500` |
| Tên bản ghi bị sửa `.change-modified` | `#475569` (giá trị cũ/mới bên trong vẫn đỏ/xanh) |
| Nhãn trường `.change-field` | `#475569`, `font-weight: 600` |
| Khối thay đổi `.change-item` | `font-size: 12px; padding: 3px 8px; background: #f8fafc; border-radius: 4px; margin-bottom: 3px; display: flex; flex-wrap: wrap; gap: 4px` |
| Danh sách con `.change-list` | `flex: 0 0 100%; padding-left: 12px` (xuống dòng dưới nhãn, thụt vào) |
| Thời gian `.ho-timeline-time` | `font-size: 11px; color: #9ca3af; font-family: monospace` |
| Tên hành động `.ho-timeline-text` | `font-size: 13px`, đậm, màu `action_color` |
| Người thực hiện `.ho-timeline-actor` | `font-size: 11px; color: #6b7280; margin-top: 3px` |
| Chấm timeline `.ho-timeline-dot` | `16px`, `border-radius: 999px`, `border: 2px solid <action_color>`, nền `<action_color> + '22'` |
| Đường nối | `::before` của `li:not(:last-child)`: `left: 7px; top: 28px; bottom: 0; width: 2px; background: #e5e7eb` |
| Ghi chú | nền `#fef3c7`, chữ `#92400e`, `padding: 4px 8px`, radius 4 |
| Thanh lọc `.ch-filter-bar` | `padding: 12px 10px; margin: 0 0 16px; background: #f8fafc; border: 1px solid #e5e7eb; border-radius: 6px` |

Màu chấm + màu tên hành động lấy từ `action_color` BE trả — **không hardcode theo action**.

## 7. Text chuẩn (copy đúng chữ)

| Chỗ | Text |
| --- | --- |
| Title popup | `Lịch sử <đối tượng>` |
| Nút mở bộ lọc | `Bộ lọc` |
| Nhãn lọc | `Loại hành động` · `Người thực hiện` · `Từ ngày` · `Đến ngày` |
| Placeholder lọc | `Tất cả loại hành động` · `Tất cả người thực hiện` · `Từ ngày` · `Đến ngày` |
| Nút trong thanh lọc | `Tìm kiếm` (primary) · `Làm mới` (tertiary) |
| Nút đóng | `Đóng` (tertiary, icon `fas fa-arrow-left`) |
| Dòng người thực hiện | `Người thực hiện: <mã> - <tên> — <phòng ban>` |
| Không xác định người | `Hệ thống` |
| Giá trị trống | `(trống)` |

## 8. Sai lầm hay gặp

| Sai | Đúng |
| --- | --- |
| Dòng sửa để 1 màu (`gggg → Nguyễn Văn C` cùng màu) | Cũ đỏ, mới xanh, tên bản ghi xám |
| Thêm 1 tài khoản → in lại cả người liên hệ ở `-` và `+` | Tách bảng con thành khoá riêng, chỉ 1 dòng `+` |
| Sắp xếp cũ → mới | Mới nhất lên đầu, cả popup lẫn màn chi tiết |
| Thời gian để cuối mục | Thời gian ở ĐẦU mục |
| Hardcode danh sách "Loại hành động" | Dựng từ chính log đang có |
| Lọc ngày theo `created_at` (`d/m/Y H:i`) | Lọc theo `created_at_raw` (`Y-m-d …`), cắt 10 ký tự |
| `V2BaseSelect` trong popup | `V2BaseSelectInModal` (dùng được cả trong và ngoài modal) |
