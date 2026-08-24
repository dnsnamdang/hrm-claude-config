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
- **Placeholder của ô lọc phải NÓI ĐÚNG trường đó lọc gì** (user chốt 2026-08-15), theo công thức:
  - Ô chọn (select/date): **`Chọn <tên trường>`** — `Chọn trạng thái`, `Chọn quốc gia`, `Chọn người tạo`, `Chọn ngày bắt đầu`.
  - Ô gõ tay: **`Nhập <tên trường>`** — `Nhập tên hoặc mã hàng hoá`, `Nhập số tiền`.
  - Ô tìm nhanh: **`Tìm theo <các trường BE thực sự lọc>`** — phải liệt kê đúng, đừng ghi "Tìm kiếm..." chung chung.
  - **CẤM** `Tất cả`, `Chọn...`, `--Chọn--`, để trống, hay lặp lại nguyên si nhãn. Ở **chế độ gọn** (≤ 3 ô) panel KHÔNG render nhãn, placeholder là thứ DUY NHẤT cho user biết ô đó là gì — `Tất cả` lúc đó vô nghĩa.
- **Bộ lọc ≤ 3 ô (TÍNH CẢ ô tìm nhanh) → bày hết ra 1 hàng, KHÔNG có nút "Tìm kiếm nâng cao"**: ô tìm nhanh thu ngắn lại, các ô lọc còn lại nằm ngang hàng và rộng bằng nhau, hiện sẵn ngay khi vào màn. Giấu 1-2 ô lọc sau 1 cú bấm là bắt user thao tác thừa, mà panel mở ra cũng chỉ lấp được 1/4 chiều ngang. `V2BaseSmartFilterPanel` **tự xử lý** bằng computed `isInlineMode` (đếm `visibleInputCount` + ô tìm nhanh) — page KHÔNG phải khai gì thêm; ⚠️ đếm theo **số Ô NHẬP thực tế**, KHÔNG phải số phần tử trong `visibleFields`: field gom nhóm render ra nhiều ô nên tính theo `resetKeys.length` (vd `org` = Công ty + Phòng ban + Bộ phận + Nhân viên = **4 ô**, `customer_scope_pairs` = 2 ô), cần khác thì khai `inputCount` trên field để đè. Đếm mỗi field là 1 thì bật đúng field gom nhóm thôi đã kín cả hàng mà panel vẫn tưởng "gọn" rồi bỏ mất nút "Tìm kiếm nâng cao"; user ẩn bớt trường ở popup "Cài đặt bộ lọc" thì panel tự chuyển sang hàng ngang, và ngược lại. Ở chế độ này ô lọc **không có nhãn** (dùng `placeholder`) để thẳng trục với ô tìm nhanh → `placeholder` của mỗi field phải tự nói rõ nó lọc gì ("Chọn trạng thái", không phải "Chọn..."). Nút **"Cài đặt bộ lọc" cũng ẩn luôn** ở chế độ này (đã bày hết ra rồi thì không còn gì để bật/tắt) — **ngoại lệ**: panel gọn vì chính user tắt bớt trường (schema 6 trường, user để lại 2) thì vẫn giữ nút, không thì khoá mất lối duy nhất để bật lại. Màn còn dùng `V2BaseFilterPanel` cũ không có cơ chế này (panel cũ nhận ô lọc qua slot nên không đếm được) — chuyển sang panel mới thì được luôn.
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
- **BỎ hẳn "Hủy phiếu" và "Không duyệt" khỏi danh sách** (chốt 2026-08-24) — 2 hành động phủ quyết
  này **chỉ đặt ở màn CHI TIẾT**. Lý do: chúng luôn cần modal nhập lý do + người duyệt phải đọc nội
  dung chứng từ trước khi từ chối, nên ở danh sách chúng chỉ là `nuxt-link` điều hướng sang chi tiết
  — thêm 1 dòng menu mà không làm được gì tại chỗ.
  - Vẫn **giữ "Duyệt"** ở danh sách (dạng điều hướng `to` sang chi tiết) — đây là lối tắt cho việc
    duyệt hàng loạt, người duyệt vào chi tiết là thấy đủ cả Duyệt lẫn Hủy/Không duyệt.
  - Áp cho mọi màn chứng từ có vòng đời duyệt (phiếu thu/chi, đề nghị, ủy nhiệm chi, yêu cầu…).
  - Màn cũ còn sót thì bỏ dần khi có dịp đụng vào: `pages/finance/bill-payments/index.vue` ("Hủy
    phiếu"), `pages/finance/bill-payment-requests/index.vue` và
    `pages/finance/prepick-cancel-requests/index.vue` ("Không duyệt").
- Nút **Khóa / Mở khóa KHÔNG để trong ô Trạng thái** — đưa về cột Hành động.
- Cột Hành động KHÔNG đưa vào modal "Cấu hình cột hiển thị" (không cho ẩn / kéo đổi chỗ) → khai riêng, đừng bỏ vào `allColumns`.
- **MỌI màn danh sách BẮT BUỘC có hành động "Lịch sử"** (chốt 2026-08-15) — `{ key: 'history',
  title: 'Lịch sử', icon: 'ri-history-line' }`, nằm trong menu `⋮`, **KHÔNG gắn permission riêng**
  (ai vào được màn thì xem được). Áp cho cả màn danh mục nhỏ nhất (tiền tệ, quốc gia, phường/xã…).
  - Chưa có audit log cho entity đó → phải làm log trước (skill `entity-history`), không được bỏ nút.
  - **Màn danh mục dùng bộ DÙNG CHUNG**: popup `components/modal/CatalogHistoryModal.vue` +
    trait BE `LogsCatalogHistory` + bảng chung `catalog_histories`. Không viết popup / bảng log
    riêng cho từng danh mục — xem `entity-history` §5.1.
  - Đi kèm ở màn chi tiết / popup Xem là **khối "Lịch sử"** trong thân trang, KHÔNG phải nút ở
    `V2Footer` — xem `entity-history` §5.1.

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
        // Không xóa được -> ẨN (đưa điều kiện vào `visible`), KHÔNG hiện rồi disable
        { key: 'delete', title: 'Xóa', icon: 'ri-delete-bin-line', danger: true,
          visible: this.canDelete && !!item.is_can_delete },
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

**Chữ trong ô bảng để THƯỜNG — KHÔNG in đậm, kể cả cột Mã** (user chốt 2026-08-15). Bỏ hết
`font-weight-bold` / `font-weight: 600` / `titleBold` trong `#cell-*`: bảng mà ô nào cũng đậm thì
không còn ô nào nổi bật, mắt không biết bám vào đâu. Cột định danh vẫn nhận ra được nhờ **màu navy
+ gạch chân đứt** của `.v2-cell-link` (class này đã để `font-weight: 400`). Muốn nhấn mạnh một giá
trị thì dùng badge / màu, không dùng chữ đậm.

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

## 3a. Màn DANH MỤC dùng modal (không có màn chi tiết)

Phần lớn danh mục (cấp dịch vụ, quốc gia, tỉnh/huyện/xã, loại tài khoản, tiền tệ, ngân hàng…)
Thêm/Sửa/Xem đều nằm trong **modal**, không có route `/{id}`. Quy tắc cột định danh vẫn giữ nguyên
tinh thần "bỏ hành động Xem", chỉ đổi cách mở (user chốt 2026-08-15):

- Cột định danh (Mã, hoặc Tên nếu bảng không có mã) là **`<button class="v2-cell-link field-line">`**
  → bấm vào **mở modal Xem**. `button.v2-cell-link` đã khai sẵn trong `assets/scss/v2-styles.scss`
  (reset nền/viền/padding rồi dùng chung đúng kiểu link của màn lớn).
- **BỎ nút "Xem"** khỏi cột Hành động — y như màn có route chi tiết.
- Dùng `<button>`, KHÔNG dùng `<a href="javascript:void(0)">`: mở modal không phải điều hướng nên
  không có gì để mở tab mới; `<a>` không href còn mất luôn khả năng bấm bằng bàn phím.
- Có route chi tiết thật thì vẫn phải là `nuxt-link` như mục 3 — đừng đổi màn lớn sang kiểu này.

**Chọn cột định danh (user chốt 2026-08-15)** — mặc định là **Mã**, đứng ngay sau STT (TRƯỚC cột
Tên), `sticky` + `locked`, là link. Chỉ đổi sang Tên trong 2 trường hợp:

- Bảng **KHÔNG có cột mã** (levels, note_maintenances, device_errors, areas, wards, hamlets…).
- Bảng có cột mã nhưng **có bản ghi bỏ trống mã** (nations 5/33, provinces 11/45…) → cột định danh là
  **TÊN**; Mã vẫn giữ nhưng lùi xuống sau Tên, dạng text thường. Lý do: link nằm ở ô `—` thì user
  không bấm được gì.

Kiểm bằng dữ liệu thật trước khi quyết, đừng đoán theo schema:

```sql
SELECT COUNT(*) tong, SUM(code IS NULL OR code = '') thieu FROM <bang>;
```

Cột Mã trắng trơn trên UI → **kiểm BE trước khi kết luận**: có thể BE quên select hoặc quên alias
(vd `nations.country_code` phải alias thành `code`). Thiếu ở BE thì lấy cho đủ; chỉ khi bảng thực sự
không có mã mới bỏ cột đi — đừng để 1 cột chỉ toàn `—`.

Kiểm nhanh mức độ trống trước khi bàn giao:

```sql
SELECT COUNT(*) tong, SUM(code IS NULL OR code = '') thieu FROM <bang>;
```

**Cột Người tạo / Ngày tạo ở nhóm danh mục — LUÔN PHẢI CÓ** (user chốt 2026-08-15). Bảng thiếu
`created_by` / `created_at` thì **thêm cột bằng migration**:

- Cột `unsignedBigInteger nullable` (`created_by`, `updated_by`) + `timestamp nullable`
  (`created_at`, `updated_at`) — đúng convention DB ở CLAUDE.md.
- **Backfill dữ liệu cũ**: `created_by` = nhân viên của `namdangit@gmail.com`, `created_at` = thời
  điểm chạy migration. Tra id theo email trong migration, KHÔNG viết cứng số.
- ⚠️ Bảng ERP đang chạy song song 2 cổng: chỉ THÊM cột nullable, không đổi/xoá cột sẵn có.
- ⚠️ KHÔNG bọc `addColumn` trong `DB::transaction` (MySQL implicit-commit → lỗi "no active transaction").

---

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

## 3b-1. Bảng tràn ngang phải có thanh cuộn ở CẢ TRÊN VÀ DƯỚI

Bảng rộng hơn khung mà chỉ có thanh cuộn ngang **ở đáy** thì user phải kéo xuống hết bảng (có khi
vài chục dòng) mới với tới thanh cuộn để xem các cột bên phải. Mọi bảng cuộn ngang đều phải có
**thanh cuộn ngang phía trên**, đồng bộ 2 chiều với vùng cuộn thật.

- **Màn danh sách**: `V2BaseDataTable` đã làm sẵn (`enableScrollSync`) — không phải khai gì.
- **Bảng viết tay trong form / modal**: bọc bằng **`components/V2BaseTableScroll.vue`**:

```vue
<V2BaseTableScroll>
    <table class="table table-bordered table-sm mb-0">…</table>
</V2BaseTableScroll>
```

Component tự: đo `table.scrollWidth` → đặt độ rộng thanh trên · đồng bộ `scrollLeft` 2 chiều ·
`ResizeObserver` theo dõi bảng đổi số dòng/độ rộng · **ẩn thanh trên khi bảng không tràn** (không
chiếm chỗ vô ích). Prop `max-height` nếu muốn giới hạn chiều cao vùng cuộn dọc.

TUYỆT ĐỐI không tự chép lại cặp `topScroll` / `tableWrapper` cho từng màn — trước khi tách component
này pattern đã bị copy-paste ở 4 nơi (`V2BaseDataTable`, `ChooseErpCustomerModal`,
`SolutionVersionsTable`, `QuotationProductSearchModal`), mỗi nơi một tên class khác nhau.

💡 Bọc `V2BaseTableScroll` cũng **bỏ luôn class `.table-responsive`** → thoát rule global
`.table-responsive { min-height: 50vh }` của `assets/scss/default.scss` vốn kéo bảng vài dòng trong
form lên hơn 400px.

---

## 3b-2. `.text-muted` trong hrm-client là màu ĐỎ — đừng dùng

Bốn file SCSS toàn cục (`custom.scss`, `custom-theme.scss`, `custom-assign.scss`,
`custom-timesheet.scss`) đều khai `.text-muted { color: #dc3545 !important }`. Class "chữ mờ" quen
thuộc của Bootstrap vì thế ra **màu đỏ** trên toàn hệ thống.

Hậu quả hay gặp: dòng *"Không có dữ liệu phù hợp"*, *"Chưa chọn thiết bị nào…"*, ghi chú phụ… đều
đỏ lòm, user tưởng đang có lỗi — trong khi quy tắc là **đỏ CHỈ dành cho lỗi validate** (CLAUDE.md).

Dùng màu xám chuẩn thay vì `.text-muted`:

```scss
.v2-empty-row { color: #6b7280; }   /* nhãn/ghi chú phụ: #6b7280 · giá trị: #374151 */
```

Tự kiểm: `getComputedStyle(el).color` phải KHÁC `rgb(220, 53, 69)`.

---

## 3c. Badge TRẠNG THÁI — dùng `V2BaseBadge`, không tự dựng pill

Ô Trạng thái (và mọi badge phân loại: loại phiếu, mức độ, kết quả duyệt…) render bằng component
chung **`components/V2BaseBadge.vue`**. KHÔNG tự khai `<span class="status-pill tpl-status-*">`
hay class badge riêng của màn — mỗi màn tự dựng thì bo góc / cỡ chữ / màu lệch nhau, sửa 1 chỗ
không lan sang chỗ khác.

```vue
<template #cell-status="{ item }">
    <V2BaseBadge :variant="Number(item.status) === 1 ? 'brand' : 'required'">
        {{ item.status_text }}
    </V2BaseBadge>
</template>
```

`variant` khả dụng: `brand` (xanh lá — đang hoạt động / hợp lệ) · `required` (đỏ — khoá / ngừng /
từ chối) · `muted` (xám — nháp, chưa xác định) · `status-draft` · `status-ok` · `null`.

Khuôn mẫu: `pages/customer-care/device-errors/index.vue`. Cột Trạng thái vẫn khai `align: 'center'`
+ `width: '130px'` (mục 15).

⚠️ Text trạng thái ưu tiên lấy từ **`status_text` BE trả về**, không tự map `1 → 'Hoạt động'` ở FE:
map ở FE thì thêm trạng thái mới phải sửa cả 2 nơi và dễ lệch chữ giữa danh sách / chi tiết / export.

### 3c-1. CHỌN `variant` hay `:color` — hai kiểu, dùng đúng chỗ

| Đối tượng | Cách khai | Vì sao |
|---|---|---|
| **Danh mục dùng chung** (2–3 trạng thái cố định vĩnh viễn: Hoạt động / Khoá / Nháp) | `variant="brand" \| "required" \| "muted"` | Cố định mãi mãi, không đáng phải cấu hình ở BE |
| **Phiếu, dự án, công việc, hợp đồng… — MỌI đối tượng nghiệp vụ nhiều trạng thái** | **`:color="item.status_color"` — mã màu hex do BE trả về** | Thêm/đổi trạng thái chỉ sửa 1 nơi; danh sách, chi tiết, bản in, file xuất luôn giống nhau |

```vue
<!-- Đối tượng nghiệp vụ: BE trả CẢ chữ LẪN màu, FE chỉ hiển thị -->
<template #cell-status="{ item }">
    <V2BaseBadge :color="item.status_color" :title="item.status_text">
        {{ item.status_text }}
    </V2BaseBadge>
</template>
```

Khuôn mẫu: `pages/assign/pricing-requests/index.vue`.

**BE bắt buộc trả `status_color`** (mã hex) cạnh `status_text` trong Resource. Nguồn màu là hằng
`STATUSES` trên Entity, KHÔNG rải mã màu trong controller/resource:

```php
const STATUSES = [
    ['id' => self::STATUS_CREATING, 'name' => 'Đang tạo',  'color' => '#64748B'],
    ['id' => self::STATUS_WAITING,  'name' => 'Chờ xử lý', 'color' => '#D97706'],
];
```

### 3c-2. Bảng 9 MÃ MÀU CHUẨN — chỉ được dùng đúng 9 mã này

Nguồn gốc: `.plans/status-color-convention/huong-dan-mau-trang-thai.xlsx` (bản chốt 15/08/2026).
Cùng ý nghĩa thì **mọi phân hệ phải ra cùng một màu**. Trạng thái mới → gán vào 1 nhóm có sẵn,
**KHÔNG nghĩ ra mã màu mới cho riêng màn của mình**.

| Nhóm | Mã màu | Trạng thái thuộc nhóm |
|---|---|---|
| Hoàn thành – Đã duyệt | `#16A34A` | Hoàn thành, Hoàn tất, Đã duyệt, Đã duyệt giải pháp, Đã xử lý xong, Tiếp nhận, Đã duyệt giá |
| Đang thực hiện | `#2563EB` | Đang thực hiện, Đang triển khai, Đang xử lý, Đã gửi, Đã tiếp nhận |
| Chờ xử lý – Chờ duyệt | `#D97706` | Chờ duyệt, Chờ TP/PM/BGĐ/Leader duyệt, Chờ tiếp nhận, Chờ làm giá |
| Cảnh báo – Sắp đến hạn | `#F59E0B` | Sắp tới hạn, Tạm dừng, Cần bổ sung thông tin |
| Từ chối – Quá hạn – Khoá | `#DC2626` | Từ chối, Không duyệt, Dừng, Quá hạn, Khoá, Ngừng hoạt động |
| Theo dõi – Mới tiếp nhận | `#0EA5E9` | Đã phân công, Chờ phê duyệt triển khai, Đã tạo hợp đồng, Đang khảo sát |
| Chốt – Thương thảo | `#7C3AED` | Đã chốt, Chốt giải pháp, Thương thảo giá, Dự toán, Trúng thầu |
| Nháp – Mới tạo | `#64748B` | Nháp, Đang tạo, Mới ghi nhận, Chờ bắt đầu |
| Đã đóng – Không áp dụng | `#6B7280` | Đóng, Đã đóng, Hết hiệu lực, Đã huỷ, Chưa duyệt, Không áp dụng |

Quy tắc kèm theo:

- **Nền nhạt – chữ đậm**, không nền đậm chữ trắng (nền đậm là ngôn ngữ của NÚT BẤM).
  `V2BaseBadge` tự làm nhạt nền còn 10% và viền 20% từ 1 mã màu — đừng tự tính.
- **Luôn có chữ**, không bao giờ chỉ có chấm màu (người mù màu / in đen trắng vẫn phải đọc được).
- **Đỏ chỉ dành cho trạng thái xấu** (từ chối, dừng, quá hạn, khoá) — không dùng đỏ để trang trí.
- **Badge không bấm được** — đổi trạng thái phải qua nút thao tác có xác nhận (còn ghi lịch sử).
- **Cùng 1 bản ghi phải ra cùng chữ + cùng màu** ở danh sách, chi tiết, bản in và file Excel.
- **Mức độ ưu tiên là thang RIÊNG**, không trộn vào 9 nhóm này:
  Thấp `#94A3B8` → Trung bình `#F59E0B` → Cao `#F97316` → Khẩn cấp `#DC2626`.

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
- ⚠️ **Cột Người cập nhật hay ra rỗng vì BE KHÔNG GHI `updated_by`, không phải vì thiếu cột FE.** Trước khi khai cột, kiểm 3 thứ: (1) Entity có `extends BaseModel` không — `extends Model` thuần thì không có hook audit, `updated_by` sẽ NULL vĩnh viễn (xem CLAUDE.md mục *Model MỚI BẮT BUỘC extends BaseModel*); (2) service có gán `updated_by` ở **cả đường khoá/mở khoá** không; (3) query danh sách có eager load / join quan hệ người cập nhật chưa. Cách kiểm nhanh: sửa 1 bản ghi rồi `select updated_by from <bang> where id = <id>` — ra NULL hoặc ra id không có trong `employees` là hỏng.
- **Ngày tạo / Ngày cập nhật**: **NGÀY + GIỜ PHÚT** — `18/10/2026 16:15`. BE: `Helper::formatDateTime($x, 'd/m/Y H:i')` — truyền format để **bỏ giây** (mặc định của helper là `d/m/Y H:i:s`). Cột này khai `width: '140px'` (110px chỉ vừa phần ngày, thêm giờ là xuống dòng).

```js
{ key: 'createdByName', isVisible: 'createdByName', label: 'Người tạo', title: 'Người tạo', align: 'left', width: '170px' },
{ key: 'createdAt',     isVisible: 'createdAt',     label: 'Ngày tạo',  title: 'Ngày tạo',  align: 'left', width: '110px' },
```

### Định dạng thời gian cho các trường KHÁC

Hiển thị phải khớp với **cách người dùng nhập trên UI**, không tự quyết:

| Ô nhập trên UI | Hiển thị (danh sách · chi tiết · in · export) | BE |
| --- | --- | --- |
| Chỉ chọn NGÀY (datepicker `type="date"`) | `18/10/2026` | `Helper::formatDate($x)` |
| Chọn NGÀY + GIỜ (`type="datetime"`) | `18/10/2026 16:15` | `Helper::formatDateTime($x, 'd/m/Y H:i')` |
| Chỉ chọn GIỜ (`type="time"`) | `16:15` | `Helper::formatDateTime($x, 'H:i')` |
| Mốc hệ thống tự ghi (created_at, updated_at, thời điểm duyệt, thời điểm gửi…) | `18/10/2026 16:15` | `Helper::formatDateTime($x, 'd/m/Y H:i')` |

2 điều luôn đúng:

- **Không hiện GIÂY** ở giao diện nghiệp vụ — chỉ giữ giây trong log kỹ thuật nếu thật sự cần.
- Ô nhập chỉ có ngày mà hiển thị kèm `00:00` là **sai** (người dùng không nhập giờ đó, hiện ra gây hiểu nhầm là "lúc nửa đêm").

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

   ⚠️ **Bảng KHÔNG có cột mã → để tiêu đề TRẦN, không lấy tên thay thế.** Tên bản ghi thường dài
   (`Chi tiết công việc / lỗi thiết bị: Hiệu chỉnh cảm biến cân trọng lượng bệ kiểm tra phanh xe tải`)
   → tiêu đề trang và tên tab lê thê mà chẳng giúp định danh nhanh hơn. Chỉ ghép `: <mã>` khi **có mã**.

2. **Footer phải có ĐỦ hành động như dòng ở màn danh sách**, TRỪ:
   - **"Xem"** — đang ở màn xem rồi;
   - **"Lịch sử"** — nếu màn chi tiết đã có mục Lịch sử ngay trong form (`SystemInfoSection`). Đừng để 2 lối vào cùng 1 nội dung.

   ⚠️ **Giống cả ĐIỀU KIỆN HIỆN, không chỉ giống danh sách hành động.** Với CÙNG một bản ghi, số nút
   ở màn chi tiết phải đúng bằng số nút ở dòng tương ứng ngoài danh sách. Nút nào ẩn ngoài danh sách
   thì phải ẩn trong chi tiết, và ngược lại.
   - Sai hay gặp nhất: danh sách gate `perm.edit && isActive` (bản ghi khoá thì ẩn Sửa) nhưng chi tiết
     chỉ gate `perm.edit` → mở chi tiết vẫn thấy nút Sửa. **Sửa 1 bên mà quên bên kia là lệch.**
   - Điều kiện nên đọc từ **cùng một nguồn** (cờ BE trả về như `is_can_edit` / `is_can_delete`, hoặc
     computed dùng chung) thay vì mỗi màn tự viết lại biểu thức.
   - Khi sửa điều kiện hiện của bất kỳ hành động nào → **kiểm tra ngay cả 2 nơi** rồi mới báo xong.

   **Cách tự kiểm**: mở 1 bản ghi ở trạng thái bình thường và 1 bản ghi ở trạng thái đặc biệt
   (đã khoá / đã duyệt / đã hủy), đối chiếu danh sách nút của 2 màn — phải trùng khớp từng nút.

**BẮT BUỘC dùng `V2Footer`, KHÔNG tự dựng khối nút** (`<div class="d-flex justify-content-end">` + loạt
`V2BaseButton`). Tự dựng thì mỗi màn ra một khoảng cách / thứ tự / vị trí "Quay lại" khác nhau, và
không ăn theo khi `V2Footer` đổi.

```vue
<V2Footer :menu="{ edit: perm.edit, history: true }" url-back="/assign/customers" @edit="goToEdit" @showHistory="historyModalShow = true">
    <template #custom-actions>
        <!-- hành động không có sẵn trong V2Footer.menu -->
    </template>
</V2Footer>
```

Key có sẵn trong `menu`: `submit_and_draft` · `submit_form` · `edit` · `print` · `delete` · `cancel` ·
`history` · `approve` · `complete` · `schedule` · `confirm` · `create_other_task`…
Hành động không có trong danh sách đó, **hoặc cần disable + tooltip lý do** (nút `menu.delete` không
hỗ trợ), thì đưa vào slot `#custom-actions`. `V2Footer` tự render "Quay lại" ở cuối — đừng tự thêm.

- Dùng `menu` có sẵn của `V2Footer` cho Sửa / Xóa / Lịch sử; hành động riêng của màn đưa vào slot `#custom-actions`.
- Thứ tự: Sửa (primary) → Lịch sử + hành động phụ (secondary) → Xóa / Khóa (danger) → **Quay lại luôn cuối** (V2Footer tự render).
- Gate bằng đúng cờ quyền của màn danh sách, fail-closed (`perm.edit`, `perm.delete`), KHÔNG hard-code `true`.
- **Nút KHÔNG DÙNG ĐƯỢC thì ẨN HẲN — không hiện rồi disable.** Áp cho MỌI lý do:
  không có quyền, **và cả** chưa đủ điều kiện nghiệp vụ (đã phát sinh chứng từ, sai trạng thái…).

  ```js
  // ĐÚNG — điều kiện nằm trong `visible`
  { key: 'delete', title: 'Xóa', danger: true, visible: this.canDelete && !!item.is_can_delete }

  // SAI — hiện nút xám không bấm được
  { key: 'delete', title: 'Xóa', interactable: !!item.is_can_delete, disabledTitle: '...' }
  ```

  Áp cho cả cột Hành động ở danh sách lẫn footer màn chi tiết — nút nào ẩn ở danh sách thì phải ẩn
  ở chi tiết (mục 7.2). Muốn cho user biết vì sao không thao tác được thì đặt ghi chú/`title` ở
  **chỗ khác** (cột Trạng thái, ghi chú trong form), không giữ nút xám trên giao diện.

  📌 Quy ước này **đảo lại** cách làm cũ (hiện + disable + tooltip lý do) — chốt 2026-08-15.
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

## 9-13. Select, ô nhập liệu, danh mục bị khoá → skill `select-and-input-state`

5 mục cũ ở đây (chip select nhiều, ô disabled/readonly, **danh mục bị khoá + 🔒**, focus ô nhập,
FE mới + BE cũ) đã chuyển sang **`.claude/skills/select-and-input-state/SKILL.md`**.

Lý do tách: chúng áp cho **mọi màn có select/ô nhập** — form Tạo/Sửa, modal, màn chi tiết, bộ lọc —
chứ không riêng màn danh sách. Để ở đây thì người sửa màn form không có đường nào tìm ra
(đã gây lỗi thật: sửa `meeting/{id}/edit`, danh mục bị khoá làm mất giá trị đã chọn mà bỏ sót
quy tắc 🔒). Làm màn danh sách vẫn phải đọc skill đó cho phần select trong bộ lọc.

## 14. Dòng đếm bản ghi (dưới bảng)

Chỉ hiển thị **số**, KHÔNG kèm tên đối tượng phía sau:

- Đúng: `Hiển thị 1–10 / 17542`
- Sai: `Hiển thị 1–10 / 17542 khách hàng`

Tiêu đề bảng đã nói rõ đang xem gì nên lặp lại tên đối tượng chỉ làm dòng này dài thêm. `V2BaseDataTable` đã bỏ sẵn phần đuôi này — prop `itemLabel` giờ chỉ còn dùng cho câu rỗng `Không có <itemLabel> nào.`, vẫn phải truyền.

## 14b. Xuất file — BẮT BUỘC hỏi user chọn trường trước (chốt 2026-08-15)

**Mọi nút Xuất (Excel / CSV / PDF) phải mở popup "Chọn trường xuất file" trước, KHÔNG tải file
ngay khi bấm.** Khuôn: màn Khách hàng `/assign/customers`. Xuất thẳng cả bảng là sai — file ra
hàng chục cột thừa, user phải tự xoá cột trong Excel.

| Lớp | Dùng cái gì |
| --- | --- |
| **FE popup** | `components/modal/export-fields-modal.vue` (đã có, KHÔNG viết popup mới) |
| **FE logic** | mixin `utils/mixins/exportFieldsMixin.js` — lo mở popup, nhớ loại file, nhận cột user tick |
| **BE cột** | `App\ExcelExport\ExportColumnRegistry::COLUMNS['<màn>']` = `[key => nhãn]` — nguồn DUY NHẤT cho cả popup lẫn header file |
| **BE xuất** | `App\ExcelExport\DynamicExport` + view chung `resources/views/exports/dynamic.blade.php` — cột động, KHÔNG viết `XxxExport` + blade cứng cột cho từng màn |

Màn dùng chỉ cần:

```js
mixins: [/* … */, exportFieldsMixin],
data: () => ({ exportFieldsModalId: 'levels-export-fields-modal' }),
computed: {
    // `id` PHẢI khớp key ở ExportColumnRegistry, lệch là cột ra rỗng
    exportFields() { return [{ id: 'name', name: 'Tên cấp' }, /* … */] },
},
methods: {
    // mixin gọi lại sau khi user chọn; `fields` theo ĐÚNG thứ tự tick
    async runExport(type, fields) { /* thêm `params.fields = fields.join(',')` rồi gọi API */ },
},
```

```vue
<V2BaseButton secondary status="success" size="sm" @click="openExportModal('excel')">Xuất Excel</V2BaseButton>
<ExportFieldsModal :modal-id="exportFieldsModalId" :columns="exportFields" :exporting="exporting" @export="handleExportFields" />
```

Chốt kèm theo:

- **Thứ tự cột trong file = thứ tự user tick** (popup tự nhớ thứ tự; BE lặp theo `fields`).
- Không truyền `fields` → xuất đủ cột theo thứ tự khai trong registry (giữ hành vi cũ, không vỡ).
- `fields` đến từ query string → BE **phải lọc qua whitelist** của màn, bỏ key lạ.
- Xuất theo **đúng bộ lọc đang áp dụng** nhưng lấy TẤT CẢ dòng, không theo trang.
- Màn tự dựng file bằng ExcelJS ở FE (dữ liệu quá lớn, vd `serials`) vẫn phải có popup — chỉ khác
  chỗ lọc cột làm ở FE thay vì BE.

## 14c. Xuất file DANH SÁCH LỚN — chia nhỏ API, dựng file ở FE (chốt 2026-08-19)

Mục 14b lo phần *chọn cột*. Mục này lo phần *dựng file*.

**Mặc định của hệ thống là BE dựng file** (`DynamicExport` + `exports.dynamic`) — đúng và gọn cho
danh mục vài trăm dòng. Nhưng `DynamicExport` chạy `FromView`: dựng cả HTML rồi mới convert, nên
chi phí tăng theo **số ô**, không theo số dòng.

**Ngưỡng phải đổi hướng: một lần xuất > 2s** (quy tắc hiệu năng CLAUDE.md). Số đo thật:

| Màn | Khối lượng | BE dựng (`FromView`) | FE dựng, chia trang |
| --- | --- | --- | --- |
| Yêu cầu KT SC-BH | 5.365 dòng × 13 cột | **10,8s** (chuẩn bị dữ liệu chỉ 1,8s) | ~4s, 3 lượt × ~1,2s |
| — cùng màn, có lọc | 106 dòng | 0,7s | — |

Vượt ngưỡng thì chuyển sang **FE dựng file, dữ liệu tải theo từng trang**:

| Lớp | Dùng cái gì |
| --- | --- |
| **BE** | thêm `GET <màn>/export-rows` trả `{ headings, widths, rows, total, page, limit }`; `rows` là **mảng ô ĐÃ MAP SẴN** theo đúng thứ tự cột (FE không phải biết nghiệp vụ). Cột lấy từ `ExportColumnRegistry::resolve()` — dùng chung whitelist với 14b. Trần `limit` 5.000. |
| **FE** | `utils/export/listExportFile.js` → `exportListFile({ store, endpoint, filters, fields, docTitle, sheetName, fileName, onStage })`. Màn chỉ khai tham số, KHÔNG tự viết vòng lặp tải. |
| **Khuôn đầy đủ** | `/assign/customers` (`utils/export/customerExportFile.js` — có thêm CSV/PDF + letterhead) · `/sale/warranty-repair-requests` (chỉ Excel) |

```js
const total = await exportListFile({
    store: this.$store,
    endpoint: 'sale/warranty-repair-requests/export-rows',
    filters: this.filters,          // dùng CHUNG bộ lọc với bảng -> file khớp thứ đang hiện
    fields,                         // thứ tự user tick ở popup 14b
    docTitle: 'DANH SÁCH …', sheetName: '…', fileName: '….xlsx',
    onStage: (stage, done, count) => { this.exportProgress = this.buildExportProgressText(stage, done, count) },
})
if (!total) this.$toasted?.global?.error?.({ message: 'Không có dữ liệu để xuất' })
```

**Bắt buộc kèm theo:**

- **Dòng tiến độ cạnh nhóm nút** (`.export-progress`, chữ xám 13px) + khoá nút khi đang xuất
  (`:disabled="exporting"`). Dựng file có thể mất vài chục giây, không báo thì user tưởng treo.
  `onStage` gọi ở **cả 2 giai đoạn**: `fetch` → *"Đã tải 4.000/17.542 dòng…"*, `build` → *"Đang
  dựng file …"*.
- **Gọi TUẦN TỰ từng trang**, không bắn song song: các trang dùng chung một câu SQL, chạy song
  song chỉ làm MySQL tranh tài nguyên mà còn dễ đụng giới hạn kết nối.
- **Có trần số vòng lặp** (`Math.ceil(total / limit) + 1`) và **thoát khi trang rỗng**: bản ghi bị
  thêm/xoá giữa chừng làm điều kiện dừng theo `total` không bao giờ đúng → vòng lặp chạy mãi.
- **Xoá `page` / `limit` của bảng** khỏi params trước khi tải, nếu không chỉ xuất đúng 1 trang.
- **`0 dòng` thì KHÔNG tạo file** — báo "Không có dữ liệu để xuất".
- Giữ nguyên endpoint BE dựng file cũ, đừng xoá — còn để đối chiếu và quay lại được.

⚠️ **Điểm yếu cố hữu, phải biết trước khi chọn hướng này**: toàn bộ dữ liệu nằm trong RAM tab
trình duyệt; chi phí lớn nhất KHÔNG phải lúc tải mà là lúc kẻ viền + bọc chữ trong ExcelJS (làm
trên TỪNG Ô — 17.5k dòng × 20 cột = 350k ô). Dữ liệu tăng vài lần nữa hoặc máy yếu sẽ chậm rõ rệt.
Tới mức đó thì phải chuyển sang queue + gửi link tải, không cố nữa.

---

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

Tách ra thì user ẩn được ô cha mà vẫn giữ ô con (con mất nguồn options), hoặc kéo con lên trước cha. Field nhóm **bắt buộc** khai `resetKeys` để ẩn nhóm là xoá hết giá trị các ô con, tránh lọc ngầm. `resetKeys` còn là căn cứ **đếm số ô** của chế độ gọn (mục "Bộ lọc ≤ 3 ô" ở trên) — khai thiếu thì nhóm bị tính là 1 ô, panel nhận nhầm là bộ lọc gọn và bỏ mất nút "Tìm kiếm nâng cao". Số ô khác số `resetKeys` (vd 2 key nhưng chỉ 1 ô) thì khai thêm `inputCount`.

Hai ô chỉ giống nhau về nghiệp vụ nhưng độc lập dữ liệu thì để riêng — vd Quốc gia và Tỉnh/TP ở màn khách hàng (API `provinces` không nhận `nation_id`).

## Số dòng/trang

Mặc định luôn là **5 / 10 / 20 / 50 / 100**. Đã đặt sẵn ở prop `pageSizeOptions` của `V2BaseDataTable` và `V2BasePagination` — màn danh sách **không cần truyền prop này**.

Chỉ truyền `:page-size-options` khi thực sự cần khác, và phải có lý do rõ ràng — vd popup chọn hàng hoá / chọn KH dùng `[20, 50, 100]` vì popup cao cố định, chọn 5 dòng thì thừa chỗ trống.

### 3b-3. Ô KHÔNG CÓ DỮ LIỆU thì để TRỐNG — không điền dấu gạch

Ô rỗng trong bảng danh sách để **trống hẳn**. KHÔNG tự điền `—` / `–` / `-` / `N/A` / `(trống)`.

```vue
<span class="field-line">{{ item.name }}</span>              <!-- ĐÚNG -->
<span class="field-line">{{ item.name || '—' }}</span>       <!-- SAI -->
```

Chốt 2026-08-22 (Redmine #11171) sau khi tester rà toàn hệ thống: dấu gạch làm bảng nhiễu và dễ bị
đọc nhầm là một giá trị thật. Áp cho **mọi** cột, mọi màn — kể cả hàm định dạng (`formatPercent`,
`formatMoney`, `formatNumberCell`…) đang trả `'—'` khi giá trị rỗng: sửa thành `''`.

Đã rà và bỏ ở 22 màn danh sách (143 chỗ). Khi thêm màn mới, tự kiểm bằng:
`grep -rn "|| '—'" pages/<màn>/` phải RỖNG.

### 3b-4. Ô lọc GÕ TAY: chờ Enter / nút Tìm kiếm, KHÔNG tự tìm khi đang gõ

Deep watcher trên `filters` (khuôn `TasksTab.vue`) làm màn tự tìm mỗi khi giá trị lọc đổi. Đúng
với ô **CHỌN**, nhưng SAI với ô **GÕ TAY**: gõ "cầu nâng" là 8 lần đổi giá trị → 8 request, và
danh sách nhảy loạn ngay từ ký tự đầu.

Chốt 2026-08-22:

| Loại ô | Hành vi |
| --- | --- |
| `select`, `date`, ô chọn do màn tự render (khách hàng, Công ty/Phòng ban…) | đổi là **tìm luôn** |
| `text`, `number`, ô tìm nhanh | chờ **Enter** hoặc nút **Tìm kiếm** |

Khai bằng helper dùng chung, KHÔNG liệt kê tay từng key (thêm ô lọc mới là quên ngay):

```js
import { textFilterKeys } from '@/utils/filterAutoSearch'

computed: {
    ignoredFields() {
        return ['keyword', ...textFilterKeys(this.filterFields)]
    },
}
```

`ignoredFields` phải là **computed**, không phải `data` — schema ô lọc thường phụ thuộc quyền/danh
mục nạp sau nên để `data` sẽ chốt sai danh sách ngay lúc khởi tạo.

`V2BaseFilterFieldControl` đã bắn sẵn sự kiện `enter`, panel nối vào `handleSearch` — không phải
làm gì thêm ở màn.

Tự kiểm: mở tab Network, gõ vài ký tự vào ô lọc chữ → **0 request**; bấm Enter → **1 request**.

### 3b-5. KHÔNG ẩn Xuất Excel / In danh sách theo quyền xem

Hai nút này hiện với **mọi** người vào được màn. Phạm vi dữ liệu đã do máy chủ quyết (`applyScope()`
— xem mục phân quyền theo cấp): ai xem được gì thì in / xuất đúng phần đó, người không có quyền xem
theo cấp vẫn in / xuất được **các phiếu do chính mình tạo**.

Ẩn nút theo cờ quyền xem (`is_all_company || is_company || is_department`) là **cắt mất chức năng
chính đáng**: người dùng thường có phiếu của mình trên lưới nhưng không xuất được ra Excel.
Chốt 2026-08-22 (Redmine #11165) sau khi đã làm sai một lần theo hướng ẩn nút.

Vẫn giữ nguyên quy tắc chung "nút không dùng được thì ẩn" cho các nút **thao tác** (Sửa, Xóa,
Duyệt…) — chỗ đó điều kiện là quyền/nghiệp vụ của từng bản ghi, khác với 2 nút đọc dữ liệu này.

### 3b-6. Phân trang: MỘT kiểu duy nhất cho mọi bảng

Bảng ở màn danh sách dùng phân trang có sẵn trong `V2BaseDataTable`; bảng trong **form / popup** dùng
`components/V2BasePagination.vue`. Hai chỗ này phải trông **y hệt** nhau — người dùng nhìn thấy cạnh
nhau, lệch cỡ chữ là lộ ngay (chốt 2026-08-22):

- Dòng trái: `Hiển thị {từ}–{đến} / {tổng}` — dấu **en dash `–`**, không phải `-`.
- Cỡ chữ cả 2 cụm (`Hiển thị …` và `Số dòng/trang:`): **12px, màu `#6b7280`** (class `tp-small-text`).
- Ô chọn số dòng cỡ `sm`, đứng TRƯỚC dãy số trang.

KHÔNG tự dựng phân trang riêng cho từng popup/màn.

### 3b-7. Popup có bảng: rộng theo SỐ CỘT, đừng để mặc định 720px

Popup chọn dữ liệu (hàng hoá, dịch vụ, khách hàng…) mà bảng có ≥ 5 cột thì đặt
`style="width: 1100px; max-width: 96vw"` trở lên — khổ 720px làm cột tên bị bóp còn vài chữ. Popup
bảng rất nhiều cột (hàng hoá: 11 cột) thì dùng `width: 98vw` như `ProductSearchModal`.
Chi tiết cách dồn diện tích cho bảng: skill `modal-popup` mục 4.

### 3b-8. Thanh cuộn TRÊN phải đồng bộ bề rộng — không chỉ "có mặt là xong"

Quy tắc "cuộn cả trên và dưới" chưa đủ: thanh trên là một `div` rỗng có bề rộng đặt bằng
`table.scrollWidth`, nên **bề rộng đó phải cập nhật lại mỗi khi bảng đổi kích thước**. Chỉ đồng bộ
lúc `mounted` + `watch: data` + `resize` cửa sổ là thiếu — bảng còn giãn ra sau đó (ẩn/hiện cột,
chữ dài, font tải xong), và khi ấy thanh trên **kéo hụt**: người dùng kéo hết cỡ mà bảng mới đi
được 2/3, tưởng như không có thanh trên (đo thật 2026-08-22: bảng 1320px, thanh trên 1140px).

Bắt buộc theo dõi bằng `ResizeObserver` trên **cả bảng lẫn khung cuộn**, cộng hook `updated()`:

```js
if (typeof ResizeObserver !== 'undefined') {
    this.topScrollObserver = new ResizeObserver(() => this.syncTopScrollWidth())
    this.topScrollObserver.observe(this.$refs.dataTable)
    this.topScrollObserver.observe(this.$refs.tableWrapper)
}
```

`V2BaseDataTable` và `V2BaseTableScroll` đã làm sẵn — dùng 2 component này là đủ, đừng tự dựng lại.

Tự kiểm (Console, ở màn có bảng tràn ngang), cả 3 dòng phải đúng:

```js
const top = document.querySelector('.table-top-scroll-inner'), t = document.querySelector('.data-table')
parseInt(top.style.width) === t.scrollWidth          // bề rộng khớp
// kéo thanh trên -> .table-wrapper.scrollLeft đổi theo, và ngược lại
```

