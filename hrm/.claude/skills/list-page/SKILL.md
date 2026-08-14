---
name: list-page
description: Quy tắc xây dựng màn danh sách với permission theo cấp
---

# Quy tắc xây dựng permission cho các màn danh sách tổng hợp
- Áp dụng cho các bảng có các field: company_id, department_id, part_id (field này có thể có hoặc không) =>> Nếu có thì quyền sẽ theo bộ quyền như sau Xem [Tên màn danh sách] theo công ty, Xem [Tên màn danh sách] theo phòng ban, Xem [Tên màn danh sách] theo bộ phận, Xem tất cả [Tên màn danh sách]
- Quyền xem tất cả =>> Lấy tất cả bản ghi trừ trạng thái Đang tạo / Nháp
- Các quyền còn lại query theo các field tương ứng
- Bộ lọc luông bắt đầu bằng: Lọc theo công ty >> Lọc theo phòng ban >> lọc theo bộ phận ==>> Tuân thủ theo V2BaseFilterPanel.vue
- **Tiêu đề panel bộ lọc để mặc định `Bộ lọc danh sách`** — KHÔNG truyền prop `title`/`subtitle` để ghi riêng cho từng màn (`Bộ lọc danh sách khách hàng`, `Bộ lọc Issue`, `Bộ lọc hàng hoá`…). Tiêu đề bảng bên dưới đã nói rõ đang xem gì; `V2BaseFilterPanel` đã đặt sẵn default nên chỉ cần bỏ prop đi
- Style bắt buộc: luôn import `@import '@/assets/scss/v2-styles.scss';` trong thẻ `<style lang="scss">` của trang danh sách
- Các khối bộ lọc theo logic Cascading filter: Công ty =>> Phòng ban =>> Bộ phận; Dự án TKT =>> Giải pháp =>> Hạng mục

## Filter auto-search (chọn filter → search luôn)

Tất cả màn danh sách PHẢI dùng deep watcher trên `filters` để khi chọn bất kỳ filter nào (trừ keyword) thì tự động gọi `loadData()`, không cần nhấn nút tìm kiếm. Tham chiếu: `pages/assign/solutions/components/manager/TasksTab.vue`.

### Pattern bắt buộc:

**data():**
```js
filters: { ...initialStateForm },
ignoredFields: ['keyword'],
oldFilters: {},
```

**created():**
```js
this.oldFilters = JSON.parse(JSON.stringify(this.filters))
```

**watch:**
```js
filters: {
    handler(newVal) {
        // Cascade logic nếu có (reset filter con khi filter cha thay đổi)
        const shouldCallApi = !this.ignoredFields.some((field) => newVal[field] !== this.oldFilters[field])
        if (shouldCallApi) {
            this.pagination.currentPage = 1
            this.loadData()
        }
        this.oldFilters = JSON.parse(JSON.stringify(this.filters))
    },
    deep: true,
},
```

### Lưu ý:
- `handleReset` và `handleSort` chỉ thay đổi `filters`, KHÔNG gọi `loadData()` (deep watcher tự xử lý)
- `handleSearch` vẫn giữ `loadData()` vì `keyword` nằm trong `ignoredFields` (cần nhấn nút search)
- `handlePageChange` và `handlePageSizeChange` vẫn gọi `loadData()` trực tiếp (vì thay đổi `pagination`, không phải `filters`)

## Giữ filter khi navigate sang show/edit rồi quay lại

Tất cả màn danh sách PHẢI dùng `filterStateMixin` để khi người dùng vào xem/sửa một bản ghi rồi bấm quay lại, bộ lọc vẫn được giữ nguyên.

### Cách tích hợp:

**Import và khai báo mixin:**
```js
import filterStateMixin from '@/utils/mixins/filterStateMixin.js'

export default {
    mixins: [PageTitleMixin, filterStateMixin],
    ...
}
```

**Thêm vào data() — 4 field bắt buộc:**
```js
filterFieldName: 'filters',                    // tên field chứa bộ lọc
localStorageKey: 'assign_ten_man_hien_tai',    // key riêng, không trùng màn khác
pathsToKeep: ['/assign/ten-man-hien-tai'],     // prefix path của show/edit
expirationTime: 10 * 60 * 1000,               // 10 phút
```

**Restore trong mounted() — thêm TRƯỚC khi gọi loadData():**
```js
async mounted() {
    // ... các khởi tạo khác ...

    const savedState = this.loadFilterState()
    if (savedState) {
        this.filters = { ...initialStateForm, ...savedState.filter }
        if (savedState.filterCollapsed !== undefined) {
            this.filterCollapsed = savedState.filterCollapsed
        }
    }
    this.oldFilters = JSON.parse(JSON.stringify(this.filters))

    this.loadData()
},
```

### Cơ chế hoạt động:
- Khi rời trang (hook `beforeRouteLeave`): nếu navigate sang path trong `pathsToKeep` (VD: `/assign/ten-man/123/show`, `/assign/ten-man/123/edit`) → lưu filter vào localStorage. Ngược lại → xóa.
- Khi vào lại trang: `mounted()` đọc localStorage và restore filter + trạng thái collapsed của panel.

### Quy tắc đặt localStorageKey:
- Format: `assign_<tên_module_snake_case>` (VD: `assign_meeting`, `assign_request_solution`, `assign_solutions`)
- Phải unique trên toàn project, không được trùng với màn khác

---

# Cột Hành động — chuẩn bắt buộc cho MỌI màn danh sách

**Màn mẫu: `pages/assign/customers/index.vue`.** Màn mới copy theo màn này; màn cũ sửa dần khi có dịp đụng vào.

## 1. Vị trí và số lượng nút

- Cột **"Hành động" luôn nằm CUỐI bảng**. KHÔNG nhét nút thao tác vào ô đầu (dưới tên bản ghi) như kiểu cũ.
- **Tối đa 3 nút / dòng.** Nhiều hơn 3 → giữ **2 hành động chính** + **1 nút `⋮`** mở menu dọc chứa phần còn lại.
  - 2 hành động chính mặc định là **Sửa** và **Xóa**.
  - Màn không có Xóa (chỉ khóa/ngừng hoạt động) → slot thứ 2 dành cho **Khóa / Mở khóa**.
- **BỎ hẳn hành động "Xem".** Tên (hoặc mã - tên) bản ghi ở cột đầu là **link vào màn chi tiết**.
- Nút **Khóa / Mở khóa KHÔNG để trong ô Trạng thái** — đưa về cột Hành động.
- Cột Hành động KHÔNG đưa vào modal "Cấu hình cột hiển thị" (không cho ẩn / kéo đổi chỗ) → khai riêng, đừng bỏ vào `allColumns`.

## 2. Component dùng chung

`components/V2BaseRowActions.vue` — tự cắt 2 nút chính + menu `⋮`, không màn nào tự dựng lại.

```vue
<template #cell-actions="{ item }">
    <V2BaseRowActions :actions="getRowActions(item)" @action="handleRowAction({ action: $event, item })" />
</template>
```

```js
getRowActions(item) {
    const isActive = Number(item.status) === 1
    // THỨ TỰ QUAN TRỌNG: 2 phần tử đầu là hành động chính, phần còn lại vào menu ⋮
    return [
        { key: 'edit', title: 'Sửa', icon: 'ri-edit-line', to: `/.../${item.id}/edit`, visible: this.canEdit },
        { key: 'delete', title: 'Xóa', icon: 'ri-delete-bin-line', danger: true,
          interactable: !!item.is_can_delete, disabledTitle: 'Không thể xóa: ...', visible: this.canDelete },
        { key: isActive ? 'lock' : 'unlock', title: isActive ? 'Khóa' : 'Mở khóa',
          icon: isActive ? 'ri-lock-line' : 'ri-lock-unlock-line', visible: this.canLock },
        { key: 'history', title: 'Lịch sử', icon: 'ri-history-line' },
    ]
}
```

Thuộc tính mỗi action: `key`, `title`, `icon`, `to?`, `danger?`, `interactable?`, `disabledTitle?`, `visible?`.

**Bắt buộc:** hành động **chuyển trang phải khai `to`** → component render `<nuxt-link>` để chuột phải mở tab mới được (áp dụng cả item trong menu `⋮`). Hành động mở modal / gọi API thì KHÔNG khai `to`, nghe qua sự kiện `@action`.

**Cờ quyền** đi qua `visible` và phải fail-closed (mặc định `false`, xem CLAUDE.md) — không hard-code `true`.

**Gotcha đã xử lý sẵn trong component:** bảng có `overflow` nên menu để trong ô sẽ bị cắt → component tự `appendChild` menu ra `document.body` và định vị `position: fixed` theo toạ độ nút `⋮`. Đừng bọc menu vào thẻ có `transform`.

## 3. Cột Mã + Tên: tách 2 cột, MÃ là link

**Mã và Tên là 2 cột riêng**, KHÔNG gộp thành 1 cột "Mã - Tên".

| Cột | Nội dung |
| --- | --- |
| `<đt>Code` — "Mã KH" / "Mã phiếu"… | **Link** vào màn chi tiết, `width` cố định (~150px) |
| `<đt>Name` — "Tên khách hàng"… | **Chữ thường** (`font-weight-normal`), không phải link, `cellClass: 'text-wrap'` + `minWidth` |

**Chỉ cột Mã khoá** (`locked: true` + `sticky: true`) — đây là cột định danh, chứa link vào chi tiết.
Cột **Tên KHÔNG khoá**: user được ẩn / đổi vị trí tuỳ ý, nên cũng **không** khai `sticky` (cột ghim trái bắt buộc nằm liền nhau ở đầu bảng; cột kéo đi đâu cũng được mà ghim thì offset `left` tính sai).

```vue
<!-- Mã: link vào chi tiết — nuxt-link để chuột phải mở tab mới được -->
<template #cell-customerCode="{ item }">
    <nuxt-link :to="`/assign/customers/${item.id}`" class="v2-cell-link field-line">
        {{ item.code || '—' }}
    </nuxt-link>
</template>

<!-- Tên: chữ thường, không link -->
<template #cell-customerName="{ item }">
    <div class="field-line text-dark font-weight-normal">{{ item.fullname || '—' }}</div>
</template>
```

**Kiểu link** — dùng class chung `.v2-cell-link` (đã khai trong `assets/scss/v2-styles.scss`), khuôn "mã phiếu":

| Thuộc tính | Giá trị |
| --- | --- |
| Màu chữ | navy `#28539d`, `font-weight: 600` |
| Gạch chân | `1px dashed #b7c4cf` |
| Hover | chữ `#088f84`, viền `#0aa699` |
| Hậu tố | **KHÔNG** gắn mũi tên `↗` hay icon nào khác |

TUYỆT ĐỐI không dùng `<a href="javascript:void(0)" @click="$router.push(...)">` — chuột phải không mở tab mới được.

⚠️ Class khai bằng selector `a.v2-cell-link` (element + class) là CÓ CHỦ Ý: ô bảng thường mang kèm `.field-line`, mà class đó khai `color: #475569` nằm sau trong `v2-styles.scss` — để `.v2-cell-link` trần thì mã bản ghi ra **xám** thay vì navy.

Nhớ khai map sắp xếp ở BE cho cả 2 khoá mới (`SORTABLE_COLUMNS`: `customerCode => code`, `customerName => fullname`).

## 3b. Sắp xếp theo ĐỘ KHỚP khi tìm bằng ô text

Ô tìm kiếm dùng `LIKE '%kw%'` nên bản ghi khớp khít và bản ghi chỉ chứa chuỗi ở giữa đứng lẫn lộn. Màn danh sách phải xếp **gần đúng nhất lên trước**. Khuôn: `CustomerService::applyRelevanceOrder()`.

### Công thức điểm (càng NHỎ càng lên trên)

```
điểm = chất_lượng * 10 + thứ_tự_trường
chất lượng: 0 trùng khít · 1 bắt đầu bằng · 2 khớp đầu từ · 3 chỉ chứa
trường:     0 Mã · 1 Tên · 2 MST/SĐT
```

Dòng khớp nhiều trường lấy điểm TỐT NHẤT (`LEAST(...)`), rồi tie-break theo thứ tự:

1. **Khớp ĐÚNG DẤU** trước khớp bỏ dấu — `LIKE ? COLLATE utf8mb4_0900_as_ci` (as = accent sensitive, ci = vẫn không phân biệt HOA/thường). Cột để collation bỏ dấu nên gõ `HỮU` khớp luôn `HƯU`; tiện khi user gõ thiếu dấu, nhưng bản ghi trùng dấu phải lên trên.
2. **Vị trí khớp** — `IF(LOCATE(kw, tên) = 0, 9999, LOCATE(kw, tên))`.
3. `CHAR_LENGTH(tên)` → 4. **`id DESC`**.

⚠️ **2 bẫy đã trả giá, đừng lặp lại:**

- **`LOCATE` KHÔNG bỏ dấu, khác hẳn `LIKE`.** Dòng khớp được nhờ bỏ dấu sẽ trả `LOCATE = 0`, mà `0 < mọi vị trí thật` → chúng bị đẩy lên **đầu** danh sách. Phải quy `0` về `9999`. (Đã thử ép mọi collation `_ai_ci`/`_520_ci`/`general_ci` và cả `REGEXP_INSTR` — không cái nào định vị được khi khác dấu.)
- **Thiếu bậc "đúng dấu"** thì gõ `HỮU` sẽ thấy `TRẦN XUÂN HƯU` chen lên trên `HỒ HỮU HOÀNG`.

Giới hạn còn lại (chấp nhận được): trong **nhóm khớp khác dấu**, không định vị được nên chỉ xếp theo độ dài tên. Nhóm này vốn là kết quả phụ, đã nằm sau toàn bộ nhóm đúng dấu.

**Chất lượng đứng TRƯỚC trường** là có chủ ý: tên trùng khít phải trên mã chỉ-chứa-ở-giữa. Xếp theo trường trước là sai.

### Tín hiệu theo LOẠI trường

| Loại trường | Dùng | Bỏ — vì sao |
| --- | --- | --- |
| Mã bản ghi | trùng khít → bắt đầu bằng → sau dấu `-` → chứa | Bỏ `CHAR_LENGTH`: mã dài/ngắn không nói lên độ khớp |
| Tên người / tổ chức | đủ 5 tín hiệu, ranh giới từ = dấu cách (`'% kw%'`) | — |
| SĐT / MST / CCCD | chỉ trùng khít + bắt đầu bằng | Bỏ ranh giới từ & vị trí: chuỗi số không có "từ", khớp giữa là nhiễu |
| Trường ở BẢNG KHÁC (người tạo…) | **không chấm điểm** | Phải chạy subquery mỗi dòng. Không cần: `WHERE` đã đảm bảo dòng trả về khớp ít nhất 1 trường, dòng chỉ khớp trường này tự rơi `ELSE 99` xuống cuối |

### 4 chốt bắt buộc

1. **Bỏ qua khi user đã bấm sort cột** (`sort_by` khác rỗng/`id`) — không thì bấm sort mà không thấy đổi.
2. **Chỉ bật khi từ khoá ≥ 2 ký tự** — 1 ký tự thì dòng nào cũng khớp, chấm điểm vô nghĩa mà vẫn tốn filesort trên tập lớn.
3. **Luôn có `id DESC` cuối cùng** — thiếu là MySQL trả thứ tự không xác định giữa các dòng cùng điểm, lật trang sẽ thấy bản ghi lặp/mất.
4. **Từ khoá toàn số ≥ 6 chữ số → đảo ưu tiên**: nhóm SĐT/MST lên trước Mã (user đang tra số điện thoại).

### Ô nào được chấm điểm

Chỉ **ô chữ**, theo thứ tự ưu tiên lấy 1 ô làm từ khoá chấm điểm: `keyword` (tìm nhanh) → Tên → Mã → các ô tên khác. **Ô thuần số** (MST/SĐT, CCCD) không chấm — người ta gõ đủ, chấm chỉ tốn thêm bước sắp xếp.

### Không dùng

- **FULLTEXT (`MATCH…AGAINST`)** — không khớp chuỗi con, mà user hay gõ mảnh giữa mã (`TPHP`).
- **`SOUNDEX`** — thuật toán cho tiếng Anh, tiếng Việt ra rác.
- **Levenshtein** — MySQL không có sẵn (phải cài UDF) và chạy trên từng dòng của bảng chục nghìn dòng.
- **Tự bỏ dấu tiếng Việt** — cột đang `utf8mb4_unicode_ci` nên gõ `hoang` đã khớp `hoàng` sẵn (đã đo: cùng ra 1.571 dòng).

⚠️ Hàm dùng cho popup chọn (select2) thường gọi `index()` rồi `->reorder()` — kiểm tra lại để popup vẫn giữ thứ tự A-Z của nó.

## 4. Thứ tự cột + cột ghim trái

`[cột khoá: STT → Mã → Tên] → [các cột dữ liệu theo cấu hình user] → [Người tạo] → [Ngày tạo] → [Trạng thái] → [Hành động]`

- **Cột Mã và cột Tên tách riêng** (xem mục 3), cả 2 đều `sortable: true`.
- **2 cột đầu (STT + Mã) khai `sticky: true`** để ghim trái khi cuộn ngang — khuôn `pages/assign/prospective-projects/index.vue`. Cột STT phải có `width` + `minWidth` (`60px`) vì `getStickyColumnStyle` cộng dồn `width`/`minWidth` của các cột sticky đứng trước để tính `left`; thiếu thì cột thứ 2 đè lên cột thứ nhất.
- Cột đứng NGAY SAU nhóm sticky thì **không** được khai `sticky` (phá offset `left` của nhóm).

Cột **Trạng thái mặc định đứng ngay trước cột Hành động**. Nếu màn đã có modal Cấu hình cột và cần dời cột đã tồn tại sang vị trí mới → **đổi `key` của cột** (VD `status` → `customerStatus`) để `defaultTableColumns` coi là cột MỚI và chèn đúng chỗ; giữ key cũ thì cấu hình đã lưu của user sẽ ghim cột ở vị trí cũ.

## 5. Popup "Cấu hình cột hiển thị"

Dùng mixin chung `utils/mixins/columnCustomizationMixin.js` (khai `columnScreenKey` + đổi computed cột của màn thành `allColumns`), KHÔNG tự viết lại logic merge/lưu.

- **Cột bắt buộc khai `locked: true`** — chỉ STT, cột Mã (định danh) và Hành động. Cột Tên và mọi cột nghiệp vụ khác để user tự ẩn/hiện + kéo thả. Cột `locked` **vẫn liệt kê trong popup** để user thấy đủ bộ cột của bảng, nhưng bị **xám + tick sẵn**, không bỏ tích và không kéo thả được (modal tự xử lý qua `column-row--locked` + `draggable=".column-row--free"`).
- **Thứ tự trong popup phải khớp thứ tự trên bảng**: STT / Mã ở đầu, **Hành động ở CUỐI**. Mixin lo việc này bằng computed `pinnedColumns` — ghim cột `locked` về đúng vị trí gốc trong `allColumns` rồi mới đổ ra cả popup lẫn bảng.
  ⚠️ Không đổ thẳng `mergedColumns` ra popup: nó giữ **thứ tự đã lưu của user**, nên cột mới thêm (vd `actions` lần đầu vào popup) bị chèn cạnh hàng xóm gần nhất và hiện ở **giữa** danh sách.

## 6. Bộ cột hiện MẶC ĐỊNH

Màn danh sách mặc định **chỉ hiện 7 cột**:

`STT` → `Mã` → `Tên` → `Người tạo` → `Ngày tạo` → `Trạng thái` → `Hành động`

- Mọi cột nghiệp vụ khác (MST, SĐT, Email, Địa chỉ, Nhóm, Tỉnh/TP…) **vẫn khai đủ** trong `allColumns` để user bật ở modal "Cấu hình cột hiển thị", nhưng để `isVisible: false`.
- **Ngoại lệ**: màn nào có trường **Khách hàng** hoặc **Loại phiếu** thì 2 cột đó cũng hiện mặc định (9 cột) — vì thiếu chúng thì dòng dữ liệu không đọc được là phiếu gì / của ai.
- Bảng mặc định gọn giúp màn không phải cuộn ngang; ai cần thêm thì tự bật, cấu hình lưu theo user (`column_customizations`).

Cột `Người tạo` + `Ngày tạo` là **bắt buộc** ở mọi màn, đứng cuối nhóm cột dữ liệu (ngay trước Trạng thái → Hành động).

- **Người tạo**: chỉ **TÊN** người tạo, KHÔNG kèm mã nhân viên.
- **Ngày tạo**: chỉ **NGÀY** `dd/mm/yyyy`, KHÔNG kèm giờ → BE dùng `Helper::formatDate()`, không dùng `Helper::formatDateTime()`.

```js
{ key: 'createdByName', isVisible: 'createdByName', label: 'Người tạo', title: 'Người tạo', align: 'left', width: '170px' },
{ key: 'createdAt',     isVisible: 'createdAt',     label: 'Ngày tạo',  title: 'Ngày tạo',  align: 'left', width: '110px' },
```

**BE — lấy tên người tạo bằng SUBQUERY, không leftJoin.** Cột này luôn trả về nên leftJoin sẽ làm chậm câu COUNT của phân trang (đo trên 42.077 KH: 0,12s → 0,43s khi thêm join). Khuôn `CustomerService::creatorNameSql()`:

```php
"(select ei.fullname
  from {$mainDb}.employees e
  join {$mainDb}.employee_infos ei on ei.id = e.employee_info_id
  where e.id = customers.created_by) as creator_name"
```

Nếu màn có modal "Cấu hình cột hiển thị" và cột Người tạo trước đây đang **mặc định ẩn** → đổi `key` (vd `creatorName` → `createdByName`) để cấu hình đã lưu của user coi đây là cột MỚI và hiện lại đúng vị trí (xem mục 4).

## 7. Màn chi tiết đi kèm màn danh sách

1. **Tiêu đề có mã bản ghi**: `Chi tiết <đối tượng>: <mã>` (vd `Chi tiết khách hàng: KH-00042`). Mã chỉ có sau khi form nạp xong dữ liệu → form `$emit('loaded', data)`, page bắt sự kiện rồi set `pageTitle` (dùng `PageTitleMixin`) và `head().title`. Chưa có dữ liệu thì hiện tiêu đề trần, không hiện `: undefined`.

2. **Footer phải có ĐỦ hành động như dòng ở màn danh sách**, TRỪ:
   - **"Xem"** — đang ở màn xem rồi;
   - **"Lịch sử"** — nếu màn chi tiết đã có mục Lịch sử ngay trong form (`SystemInfoSection`). Đừng để 2 lối vào cùng 1 nội dung.

```vue
<V2Footer :menu="{ edit: perm.edit, history: true }" url-back="/assign/customers" @edit="goToEdit" @showHistory="historyModalShow = true">
    <template #custom-actions>
        <!-- hành động không có sẵn trong V2Footer.menu -->
    </template>
</V2Footer>
```

- Dùng `menu` có sẵn của `V2Footer` cho Sửa / Xóa / Lịch sử; hành động riêng của màn đưa vào slot `#custom-actions`.
- Thứ tự: Sửa (primary) → Lịch sử + hành động phụ (secondary) → Xóa / Khóa (danger) → **Quay lại luôn cuối** (V2Footer tự render).
- Gate bằng đúng cờ quyền của màn danh sách, fail-closed (`perm.edit`, `perm.delete`), KHÔNG hard-code `true`.
- Hành động đổi trạng thái (Khóa/Mở khóa) cập nhật state tại chỗ sau khi API thành công để nút đổi ngay, không nạp lại cả màn.

## 8. Thứ tự request khi vào màn (tốc độ hiển thị)

Request danh sách phải là request **đầu tiên**, không chờ bất kỳ request nào khác. Server dev chạy `php artisan serve` (1 worker) nên request xếp hàng — gọi trước là chiếm chỗ trước.

```js
data() {
    // Bảng hiện spinner NGAY khi vào màn, không chờ request nào xong
    return { loading: true, ... }
},
created() {
    this.loadData()            // 1. danh sách — bắn ngay, không await gì

    this.getFields().then(() => {   // 2. cấu hình cột — chạy song song
        // Chỉ nạp lại khi cấu hình đã lưu bật cột cần BE join thêm mà lượt đầu chưa xin cờ
        if (this.needsExtraColumns && !this.lastLoadHadExtraColumns) this.loadData()
    })

    this.loadPermissions()     // 3. quyền — không chặn bảng
    // 4. options bộ lọc nâng cao: KHÔNG gọi ở đây, xem dưới
},
```

Bắt buộc kèm theo:

- **Hoãn options của bộ lọc nâng cao** đến khi user bấm mở panel (panel mặc định thu gọn). Gom vào `loadFilterOptions()` có cờ `filterOptionsLoaded` để chỉ chạy 1 lần.
- ⚠️ **KHÔNG hoãn request cấu hình bộ lọc (`filter-customizations`) của `V2BaseSmartFilterPanel`**, và **không gate nội dung panel bằng `v-if="configLoaded"`**. Panel mở bằng transition tự đo chiều cao: mở lúc nội dung còn rỗng thì đo ra 0 → nhìn như bấm không ăn, phải bấm mấy lần mới thấy. Cấu hình nạp ngay ở `mounted()` cũng không làm chậm danh sách vì `created()` của page đã gọi `loadData()` trước.
- **KHÔNG gọi thẳng `this.$nuxt.$loading.start()/finish()`** trong hàm chạy ngay đầu `mounted()`/`created()`: lúc đó Nuxt chưa gắn xong thanh loading nên `$loading.finish` chưa phải hàm → ném `TypeError` giữa `finally`, màn **trắng trơn**. Dùng helper toàn cục `this.$safeLoadingStart()` / `this.$safeLoadingFinish()` (`plugins/safe-loading.js`).
- **Chống response về trễ**: `loadData()` tăng biến đếm `loadSeq` ở đầu hàm, khi có kết quả thì bỏ qua nếu `seq !== this.loadSeq` (vì có thể 2 lượt gọi cùng lúc: lượt đầu + lượt nạp lại theo cấu hình cột).

Kết quả mong muốn: vào màn chỉ **2 request** (danh sách + cấu hình cột) thay vì 8.

**Màn chi tiết / sửa cũng áp cùng nguyên tắc:** request lấy dữ liệu bản ghi phải nằm **cùng lô `Promise.all`** với các request danh mục (quốc gia, tỉnh, nhóm, ngân hàng…), KHÔNG để `await` batch danh mục xong rồi mới gọi:

```js
async mounted() {
    const requests = [this.loadNations(), this.loadProvinces(), /* …danh mục… */]
    if (this.isEdit) requests.push(this.loadCustomer(), this.loadAgentEmployees())
    await Promise.all(requests)
    this.ensureSelectedAgentOption()   // xem cảnh báo dưới
}
```

⚠️ Khi chuyển sang chạy song song, coi lại mọi chỗ **hàm nạp options GHI ĐÈ cả mảng** (`this.listX = [...]`) trong khi hàm nạp dữ liệu bản ghi lại `push` giá trị đang chọn vào mảng đó (option ngoài top-100). Song song thì thứ tự về không đảm bảo → giá trị đang chọn bị xoá, select hiện trống. Cách xử lý: nhớ giá trị đang chọn vào một biến (`selectedXOption`) và chèn lại sau khi cả 2 request cùng xong.

## 9. Chip của select chọn nhiều

Giá trị đã chọn ở select `multiple` (`V2BaseSelect` / `V2BaseSelectInModal`) hiển thị **một khuôn chip duy nhất** trong toàn dự án — trùng với chip tự dựng `.csp-chip` (ô "Loại hình hoạt động khách hàng" ở `CustomerForm`):

| Thuộc tính | Giá trị |
| --- | --- |
| Nền / viền / chữ | `#eff6ff` / `#bfdbfe` / `#1e40af` |
| Bo góc | `5px` (KHÔNG bo tròn dạng pill) |
| Chữ | `11px`, `font-weight: 500`, `line-height: 18px` |
| Padding | `1px 7px` — giữ nguyên ở mọi `size`, size `sm` KHÔNG được ghi đè |
| Hover chip | nền `#dbeafe`, viền `#93c5fd` |
| Nút `×` trên chip | đứng **SAU** chữ, `13px`, `opacity .6`, không khung/không nền; hover `opacity 1` + đỏ `#dc3545` |

Đã set sẵn trong `V2BaseSelect.vue` (style global theo `.v2-select`, `V2BaseSelectInModal` dùng chung class nên ăn theo). Khi thêm size mới hoặc biến thể select: **không khai lại `font-size`/`padding` cho `.select2-selection__choice`**.

## 10. Ô nhập liệu bị KHOÁ (disabled / readonly) — một kiểu duy nhất

| Thuộc tính | Giá trị |
| --- | --- |
| Nền | `#f1f5f9` |
| Chữ | `#475569` (đọc rõ — màn chi tiết là nơi user ĐỌC dữ liệu) |
| Viền | `#e2e8f0` |
| Con trỏ | `not-allowed` |
| `opacity` | **1** — KHÔNG làm mờ |

Rule chung đặt ở `assets/scss/v2-styles.scss`, phủ đủ: `.v2-input:disabled`, `.v2-textarea:disabled`, `input/textarea/select.form-control:disabled`, `.mx-input:disabled` (datepicker), `.v2-code-input.is-disabled`, `.csp-control.is-disabled` (ô chip tự dựng), `.select2-container--disabled .select2-selection`.

**Khi viết component mới có trạng thái khoá: KHÔNG tự đặt màu nền/chữ riêng** — chỉ khai `cursor`. Trước khi chuẩn hoá, mỗi component tự đặt một kiểu (input để trắng, textarea/datepicker `#f1f5f7`, select2 `#f1f5f9` + `opacity .6`, ô chip `#e9ecef`) → 5 kiểu khác nhau trên cùng một form.

⚠️ 2 bẫy đã trả giá:

- **`opacity` làm hỏng khả năng đọc** ở màn chi tiết, và chip trong ô bị chồng màu. Dùng màu chữ nhạt thay cho `opacity`.
- **Selector nặng ký đè rule chung**: `V2BaseSelect` có `div.v2-select .select2-container.select2-container--default .select2-selection--multiple { background: #fff !important }` — đặc hiệu hơn rule chung nên ô select nhiều lựa chọn khi khoá vẫn trắng. Phải thêm `:not(.select2-container--disabled)` vào selector đó. Khi thấy 1 ô "không chịu đổi màu", tìm rule đè bằng cách duyệt `document.styleSheets` và lọc `el.matches(r.selectorText)`.

**Chip bên trong ô bị khoá cũng chuyển XÁM**, dùng chung cho cả chip của select2 (`.select2-selection__choice`) lẫn chip tự dựng (`.csp-chip`):

| Thuộc tính | Giá trị |
| --- | --- |
| Nền | `#e2e8f0` — **đậm hơn nền ô** (`#f1f5f9`) để chip không chìm thành một khối xám |
| Chữ | `#475569` |
| Viền | `#cbd5e1` |
| Nút `×` | ẩn (`display: none`) |

⚠️ **Ô tự dựng bằng `<div>` (không phải thẻ input) phải TỰ CHẶN thao tác khi khoá.** CSS `cursor: not-allowed` chỉ đổi con trỏ; `<div>` không có thuộc tính `disabled` của trình duyệt nên handler vẫn chạy — bấm vào ô khoá vẫn mở dropdown chọn. Chặn ngay đầu handler:

```js
toggleDropdown() {
    if (this.readonly) return   // hoặc this.disabled
    …
}
```
Nhớ chặn ở **mọi** handler: mở dropdown, xoá chip, chọn item, xoá tất cả.

⚠️ Phải phủ cả **thẻ con bên trong chip** (`.csp-chip *`, `.select2-selection__choice *`): chip dạng "Loại hình : Lĩnh vực" có `.csp-chip-group` tô xanh `#2563eb` riêng — không phủ thì nền chip đã xám mà chữ vẫn xanh.

## 11. Danh mục bị KHOÁ trong select — tự động, không phải khai gì

Nghiệp vụ (CLAUDE.md): dropdown chỉ liệt kê danh mục **còn hoạt động**, NHƯNG giá trị mà bản ghi đang chọn thì **vẫn phải hiện** dù danh mục đó đã khoá — không thì mở màn Sửa thấy ô trống, lưu lại là **mất dữ liệu**.

### BE — 2 việc

```php
// 1. Nhận `include_ids` = id đang được chọn, giữ lại dù đã khoá
$query->where(function ($q) use ($includeIds) {
    $q->where('status', 1);
    if (count($includeIds)) $q->orWhereIn('id', $includeIds);
});

// 2. Trả kèm cờ is_locked, GIỮ NGUYÊN tên (không nối "(đã khoá)" vào name)
return ['id' => $x->id, 'name' => $x->name, 'is_locked' => (int) $x->status !== 1];
```

Khuôn: `CustomerService::customerGroups()`.

### FE — chỉ 2 việc, KHÔNG phải khai gì để hiện 🔒

1. Gọi API danh mục kèm `include_ids` = các id đang chọn.
2. Nạp **lại** danh mục **sau khi có dữ liệu bản ghi** — lượt gọi ở `mounted` chưa biết bản ghi đang chọn id nào:

```js
if ((this.form.groups || []).length) this.loadCustomerGroups()   // trong loadDetail()
```

Phần hiển thị đã nằm trong `utils/select2LockedOption.js`, được **`V2BaseSelect` và `V2BaseSelectInModal` gọi sẵn**: options có cờ `is_locked` là tự gắn `🔒 ` trước tên **trong danh sách chọn**; chip/giá trị đã chọn giữ tên gốc. Không có option nào khoá thì không đổi gì.

⚠️ Đừng làm 3 thứ sau:

- **Nối `"(đã khoá)"` hay `"🔒 "` vào `name`** — chip cũng dính, và text lệch làm hỏng tìm kiếm/so sánh giá trị.
- **Dựng thẻ `<i class="ri-lock-line">`** — select2 escape HTML nên phải render DOM qua template, dài dòng mà không đẹp hơn emoji.
- **Viết `templateResult` riêng ở từng màn** — đã có sẵn trong component. Màn nào tự khai `templateResult` thì helper nhường, nên vẫn override được khi thật sự cần.

## 12. FE mới + BE cũ — luôn có đường lùi

Trên môi trường thật, FE và BE **không phải lúc nào cũng deploy cùng lúc**. Code FE dùng trường/endpoint mới phải chạy được cả khi BE chưa cập nhật, nếu không màn sẽ "trống trơn" mà không có lỗi nào hiện ra.

2 chỗ hay dính nhất:

- **Trường mới trong dữ liệu**: đừng để logic chỉ dựa vào 1 trường mới. Dùng chuỗi lùi dần, vd khoá nhận diện người thực hiện: `actor_id` → `actor_code` → `actor_name`; hiển thị: `actor_dept_code` → `actor_code` → chỉ tên.
- **Endpoint mới**: `catch` rồi **fallback về cách tính cũ**, đừng để mảng rỗng. Và fallback đó **không được dùng trường mới** — nếu không thì fallback cũng chết theo.

```js
performerKey(log) {
    if (log.actor_id) return String(log.actor_id)      // BE mới
    return String(log.actor_code || log.actor_name || '')  // BE cũ vẫn lọc được
},
```

Verify bằng cách **giả lập BE cũ ngay trên trình duyệt**: xoá trường mới khỏi dữ liệu rồi kiểm tra màn còn chạy không.

```js
vm.items = vm.items.map(({ actor_id, actor_dept_code, ...rest }) => rest)
vm.options = { actions: [], performers: [] }   // giả lập endpoint mới chưa có
```

## 13. Trạng thái focus của ô nhập liệu

Ô nhập / select / textarea khi được click vào **KHÔNG đổi màu viền sang xanh** (xanh lá thương hiệu hay xanh dương mặc định Bootstrap) và **không có quầng sáng** — chỉ đậm viền xám lên `#94a3b8`.

Đã xử lý sẵn ở 2 tầng, màn mới không phải khai gì:

- 10 component base: `V2BaseInput`, `V2BaseTextarea`, `V2BaseCodeInput`, `V2BaseDatePicker`, `V2BaseSelect`, `V2BaseSelectInModal`, `V2BaseFilterPanel`, `V2BaseSmartFilterPanel`, `SearchPicker`, `MultiSearchPicker`
- `assets/scss/v2-styles.scss`: rule chung `.form-control:focus, input:focus, select:focus, textarea:focus` — bắt cả input dùng `.form-control` thuần

Khi viết component mới có ô nhập: **cấm** đặt `border-color: #16a34a` / `box-shadow: rgba(22, 163, 74, …)` trong khối `:focus`.

**Nút xóa (×) trong ô lọc/select:** hover **không tô nền** (`background: transparent`), chỉ đổi ký tự × sang đỏ `#dc2626`. Không dùng nền `#fee2e2` hay bất kỳ nền nào. Đã sửa sẵn trong `V2BaseSelect` + `V2BaseSelectInModal`.

## 14. Dòng đếm bản ghi (dưới bảng)

Chỉ hiển thị **số**, KHÔNG kèm tên đối tượng phía sau:

- Đúng: `Hiển thị 1–10 / 17542`
- Sai: `Hiển thị 1–10 / 17542 khách hàng`

Tiêu đề bảng đã nói rõ đang xem gì nên lặp lại tên đối tượng chỉ làm dòng này dài thêm. `V2BaseDataTable` đã bỏ sẵn phần đuôi này — prop `itemLabel` giờ chỉ còn dùng cho câu rỗng `Không có <itemLabel> nào.`, vẫn phải truyền.

## 15. Căn lề cột (header + dữ liệu)

**Nguyên tắc gốc: header căn CÙNG lề với ô dữ liệu.** `V2BaseDataTable` đã tự lấy `column.align` cho cả `<th>` lẫn `<td>` → chỉ khai `align` MỘT chỗ trong `tableColumns`; không tự viết `text-center` / `text-right` riêng cho header.

| Loại dữ liệu | `align` | Ví dụ cột |
| --- | --- | --- |
| STT | `center` | STT |
| Chữ / định danh | `left` | Tên, Mã KH, MST, SĐT, Email, Địa chỉ, Nhóm, Tỉnh/TP, Người tạo |
| Số đếm / số lượng / tiền / % / định mức | `right` | Đơn giá bán, Công kỹ thuật, Số lượng, Thành tiền |
| Ngày, giờ | `left` | Ngày tạo, Ngày sửa |
| Badge trạng thái, icon, checkbox, cờ Có/Không | `center` | Trạng thái, Đã duyệt |
| Cột Hành động | `center` | Hành động |

Kèm theo:

- Cột số/tiền: format qua helper (`toLocaleString`); ô trống hiển thị `—` và **vẫn căn phải**.
- Cột chữ dài (địa chỉ, ghi chú): `cellClass: 'text-wrap'` + `minWidth` để bảng auto-layout không bóp hẹp.
- Cột `center` phải khai `width` cố định — STT `60px`, Trạng thái `130px`, Hành động `140px`. Căn giữa trong ô co giãn trông lệch.
- **KHÔNG** căn phải mã định danh (MST, SĐT, CCCD, số tài khoản, mã bản ghi): là chuỗi, không so sánh độ lớn.

Bảng tra nhanh dạng Excel: `.plans/gop-db/list-page-action-column/quy-tac-can-le-cot.xlsx`
---

## Cột nào được vào popup "Tuỳ chỉnh cột"

**STT và Mã - Tên KHÔNG đưa vào popup Tuỳ chỉnh cột.** Hai cột này là cột sticky, **luôn nằm ở vị trí đầu tiên**, không cho ẩn cũng không cho kéo đổi chỗ:

- **Mã - Tên** là cột nhận diện bản ghi — ẩn đi thì bảng vô nghĩa.
- Cả hai đều `sticky`, `V2BaseDataTable` cộng dồn `width` của chúng để tính `left` cho cột sticky kế tiếp; đổi thứ tự là vỡ layout.

Cách làm: đánh dấu `locked: true` trong `allColumns`, rồi popup chỉ nhận phần đã lọc:

```js
// Cột đưa vào modal cấu hình — BỎ cột khoá
customizableColumns() {
    return this.defaultTableColumns.filter((col) => !col.locked)
},

// Cột đổ vào bảng: cột khoá đứng đầu, phần giữa theo cấu hình user, Hành động chốt cuối
tableColumns() {
    const locked = this.defaultTableColumns.filter((col) => col.locked)
    const rest = this.customizableColumns.filter((col) => col.isVisible !== false)

    return [...locked, ...rest, this.actionsColumn]
},
```

Lọc ở page chứ KHÔNG thêm khái niệm "cột khoá" vào `column-customization-modal.vue` — component đó đang phục vụ 20+ màn.

Cột **Hành động** cũng không vào popup, và luôn chốt ở cuối bảng.

## Cột nào được sort

Chỉ bật `sortable: true` cho 3 nhóm:

1. Cột **Mã - Tên** (cột nhận diện chính) — BE sắp theo mã.
2. Cột định dạng **tiền**.
3. Cột định dạng **ngày**.

Các cột còn lại (text mô tả, badge trạng thái, STT, Hành động…) KHÔNG cho sort.

**Điều kiện kỹ thuật:** key cột phải nằm trong whitelist `SORTABLE_COLUMNS` của service BE. Thiếu thì BE âm thầm quay về `id` — user bấm sort mà bảng không đổi, rất khó lần ra.

## Ô tìm kiếm nhanh tìm theo gì

Mặc định chỉ tìm theo **Mã**, **Tên** và **Người tạo**. Các tiêu chí khác để trong Tìm kiếm nâng cao.

Màn cần thêm tiêu chí thì ghi rõ là ngoại lệ — vd **màn khách hàng** (`/assign/customers`) có thêm **MST** và **SĐT** vì đây là 2 thứ user hay tra nhất.

Placeholder ô tìm nhanh phải liệt kê đúng những gì thực sự tìm được, nếu không user không biết gõ gì.

Tìm theo người tạo nên dùng `EXISTS` thay vì `join` — join làm phình câu COUNT của phân trang trên bảng lớn.

## Gom nhóm trường trong popup "Cài đặt bộ lọc"

Một mục trong popup = một đơn vị bật/tắt và kéo thả. Nhiều ô nhập phải gom thành **một** field khi:

1. **Cùng một component render ra** — vd `V2BaseCompanyDepartmentFilter` đẻ ra Công ty + Phòng ban + Bộ phận + Nhân viên; `CascadePairSelect` đẻ ra Loại hình hoạt động + Lĩnh vực kinh doanh.
2. **Dữ liệu phụ thuộc lẫn nhau** (cascade cha → con).

Tách ra thì user ẩn được ô cha mà vẫn giữ ô con (con mất nguồn options), hoặc kéo con lên trước cha. Field nhóm **bắt buộc** khai `resetKeys` để ẩn nhóm là xoá hết giá trị các ô con, tránh lọc ngầm.

Hai ô chỉ giống nhau về nghiệp vụ nhưng độc lập dữ liệu thì để riêng — vd Quốc gia và Tỉnh/TP ở màn khách hàng (API `provinces` không nhận `nation_id`).

## Số dòng/trang

Mặc định luôn là **5 / 10 / 20 / 50 / 100**. Đã đặt sẵn ở prop `pageSizeOptions` của `V2BaseDataTable` và `V2BasePagination` — màn danh sách **không cần truyền prop này**.

Chỉ truyền `:page-size-options` khi thực sự cần khác, và phải có lý do rõ ràng — vd popup chọn hàng hoá / chọn KH dùng `[20, 50, 100]` vì popup cao cố định, chọn 5 dòng thì thừa chỗ trống.
