### Task 5: Chuyển `DemandListModal` sang Base + mixin

**Files:**
- Modify: `hrm-client/pages/assign/report/potential-customer-care/components/DemandListModal.vue` (toàn bộ)

**Interfaces:**
- Consumes: `V2BaseReportModal` (Task 3), `reportDrillListMixin` (Task 4).
- Produces: props và events của `DemandListModal` **giữ nguyên 100%** — `index.vue` của màn KHÔNG được sửa một dòng nào.

- [ ] **Step 1: Thay khung ngoài**

Bỏ `<b-modal>` + `<template #modal-header>` + khối `.care-drill-scroll` + `<V2BasePagination>` +
`.care-drill-footer`; thay bằng:

```vue
<V2BaseReportModal
    modal-id="care-demand-list-modal"
    :visible="visible"
    :loading="loading"
    lead="Bạn đang xem kết quả CSKH tiềm năng:"
    :title="title"
    :meta="metaText"
    :columns="columns"
    :rows="pagedRows"
    :start-index="pageOffset"
    :sort="sort"
    :current-page="safePage"
    :current-page-size="pageSize"
    :total-rows="sortedRows.length"
    item-label="nhu cầu"
    empty-text="Không có nhu cầu nào khớp bộ lọc."
    @sort="({ key }) => toggleSort(key)"
    @page-change="onPageChange"
    @page-size-change="onPageSizeChange"
    @close="$emit('close')"
>
    <!-- 3 khối dưới đây BÊ NGUYÊN VĂN từ bản cũ, chỉ đổi tiền tố lớp nếu lớp đó đã chuyển sang
         Base (xem Task 3). Mốc dòng ở bản cũ: filters 65–113, back 114–132, summary 133–158. -->
    <template #filters><!-- khối `.care-drill-filters` (dòng 65–113 bản cũ) --></template>
    <template #back><!-- khối `v-if="backTo"` (dòng 114–132 bản cũ) --></template>
    <template #summary><!-- khối KPI + chip cơ cấu (dòng 133–158 bản cũ) --></template>

    <!-- Ô đặc biệt: bê nguyên phần trong từng nhánh `v-if="col.key === '…'"` của bảng cũ.
         Mốc dòng bản cũ: customer 182–197, market 198–201, meeting 205–220, status 221–224,
         project 225–248. Ba cột `amount` (202), `start` (203), `repair` (204) chỉ là biểu thức
         một dòng — vẫn đi qua slot cho thống nhất, KHÔNG thêm khoá `formatter` vào schema. -->
    <template #cell-customer="{ row }"><!-- dòng 182–197 bản cũ --></template>
    <template #cell-market="{ row }"><!-- dòng 198–201 bản cũ --></template>
    <template #cell-meeting="{ row }"><!-- dòng 205–220 bản cũ --></template>
    <template #cell-status="{ row }"><!-- dòng 221–224 bản cũ --></template>
    <template #cell-project="{ row }"><!-- dòng 225–248 bản cũ --></template>
    <template #cell-amount="{ row }">{{ money(row.expected_amount) }}</template>
    <template #cell-start="{ row }">{{ monthYear(row.expected_start_date) }}</template>
    <template #cell-repair="{ row }">{{ row.has_maintenance_demand ? 'Có' : 'Không' }}</template>

    <template #footer>
        <V2BaseButton tertiary size="sm" @click="$emit('close')">Đóng</V2BaseButton>
        <V2BaseButton secondary size="sm" @click="$emit('print')">In danh sách</V2BaseButton>
        <V2BaseButton primary size="sm" @click="$emit('export')">Xuất Excel danh sách</V2BaseButton>
    </template>
</V2BaseReportModal>
```

- [ ] **Step 2: Gỡ code đã chuyển sang Base/mixin**

Xoá khỏi `DemandListModal.vue`: `fullscreen`, `scrollWidth`, `overflowing`, `syncingScroll`,
`scrollBound`, `bindScrollSync()`, `updateScrollWidth()`, `observeTable()`, `sortIcon()`,
`sortedRows()`, `pageCount/safePage/pageOffset/pagedRows`, `toggleSort()`, `onPageChange()`,
`onPageSizeChange()`, `page`, `pageSize`, `sort`, `keyword`, `filters`, `summaryCollapsed`,
**`resetFilters()`** (bản của mixin đã gọi `onFilterChange()` — giữ bản riêng là component đè
mixin và nút "Xoá lọc" không tải lại dữ liệu), và toàn bộ style của các lớp đã port sang Base.

⚠️ **Đổi tên MỌI lớp `care-drill-*` còn lại trong file sang `report-drill-*`** (kể cả lớp riêng
của màn: `filters`, `sum*`, `customer`, `sub`, `meeting`, `back`) — Task 6 đổi selector e2e theo
tiền tố nên không được chừa chỗ nào.

**GIỮ LẠI**: `columns`, `filterFields`, `metaText` (computed mới gộp dòng meta), `drillDimension`,
`crossStats`/`kpis`, `backTo`/`goBack`, `showFilter`, `onFilterChange` (emit `filter` lên cha),
`emptyFilters()`, và các style riêng của cột đặc biệt.

⚠️ **`isFiltered` Ở LẠI MÀN, KHÔNG đưa vào mixin.** Nó là `rows.length !== total` — chỉ đúng với
popup lọc ở SERVER (`total` do BE trả = số bản ghi TRƯỚC bộ lọc popup). Mixin có
`hasActiveFilter` (dựa trên state ô lọc) cho nút "Xoá lọc"; hai thứ này KHÁC nhau, đừng gộp:
`DevelopmentDrillModal` lọc client-side thì `rows.length !== total` vô nghĩa.

- [ ] **Step 3: Thêm mixin + computed `metaText`**

```js
import reportDrillListMixin from '@/utils/mixins/reportDrillListMixin'

export default {
    name: 'DemandListModal',
    mixins: [reportDrillListMixin],
    computed: {
        /** Dòng meta của dải banner — port nguyên văn từ `.care-drill-head__sub` cũ */
        metaText() {
            if (this.loading) return `Đang tải… · Kỳ ${this.periodText}`
            const base = `${this.rows.length} nhu cầu · ${this.money(this.totalAmount)} đ · Kỳ ${this.periodText}`
            return this.isFiltered ? `${base} · đang lọc trong ${this.total} nhu cầu` : base
        },
    },
}
```

- [ ] **Step 4: Mở màn, kiểm popup còn chạy**

```bash
cd HRM && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  node .plans/base-popup-bao-cao/measure-popup.mjs /tmp/after.json
```

Expected: script chạy hết, in JSON có đủ khoá — chưa cần khớp baseline, Task 6 mới so.

- [ ] **Step 5: Kiểm `index.vue` của màn KHÔNG bị sửa**

```bash
cd HRM/hrm-client && git diff --numstat pages/assign/report/potential-customer-care/index.vue
```

Expected: **không in ra gì** (props/events của popup giữ nguyên nên màn cha không phải đổi).

- [ ] **Step 6: Commit**

```bash
git add pages/assign/report/potential-customer-care/components/DemandListModal.vue
git commit -m "refactor(cskh): chuyển popup danh sách nhu cầu sang V2BaseReportModal + mixin"
```

---

