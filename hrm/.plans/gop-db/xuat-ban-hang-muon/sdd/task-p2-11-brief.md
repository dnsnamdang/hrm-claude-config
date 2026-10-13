# Task P2-11 Brief — Màn DANH SÁCH phiếu xuất bán hàng mượn (`pages/finance/borrow-sells/index.vue`)

> **ĐỌC FILE NÀY TRƯỚC — requirements đầy đủ, giá trị exact verbatim.** Giao tiếp tiếng Việt.
> Repo FE: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client` (Nuxt 2.14/Vue 2). Nhánh `gop_db`.
> Feature `xuat-ban-hang-muon` Phase 2 (phiếu BÁN thực tế BorrowSell, code `PXBHM-`).

## Bối cảnh 1 dòng

Tạo màn danh sách phiếu xuất bán. **Mirror gần như y hệt** màn Phase 1 `pages/finance/borrow-sell-requests/index.vue` (đọc file đó làm khuôn), nhưng phiếu BÁN đơn giản hơn: chỉ có action **Xem** (không sửa/duyệt/từ chối), không nút "Tạo phiếu" (phiếu bán được lập từ nút "Lập phiếu bán" trên chi tiết phiếu YC — T10b đã thêm), bộ lọc ít hơn.

## ⚠️ GIT: KHÔNG COMMIT (giống T10b)
FE repo để uncommitted. **KHÔNG `git commit`.** Có thể `git add <path>` (không bắt buộc), KHÔNG `git add -A`. KHÔNG git mạng. KHÔNG spawn subagent. KHÔNG đọc `node_modules/`.

## File
- **Create:** `pages/finance/borrow-sells/index.vue`
- Phụ thuộc: `pages/finance/borrow-sells/api.js` (T10b đã tạo — dùng `import * as api from './api'`, hàm `api.list(dispatch, params)`).

## Cách làm: COPY Phase 1 rồi CẮT BỎ phần thừa

Lấy `pages/finance/borrow-sell-requests/index.vue` làm khuôn. Giữ nguyên toàn bộ cơ chế: mixins (`PageTitleMixin, filterStateMixin, DedupeLoadMixin, columnCustomizationMixin`), `V2BaseSmartFilterPanel` + `V2BaseDataTable`, deep watcher `filters`, `mounted()` (loadData trước + loadColumnFields), `buildParams`, `loadData` (giữ NGUYÊN khối đọc pagination có fallback camelCase/snake_case — chống lỗi nhảy trang), `statusPillClass`, các handler filter/paging/search/reset. **Chỉ đổi các điểm dưới đây.**

### Đổi 1 — Nhận diện màn
- `title: 'Phiếu xuất bán hàng mượn'` (thay 'Yêu cầu xuất bán hàng mượn').
- `columnScreenKey`, `localStorageKey`, `table` (filter panel), `filterStateMixin` key: đổi `finance_borrow_sell_requests` → `finance_borrow_sells`.
- `pathsToKeep: ['/finance/borrow-sells']`.
- Filter panel `title="Bộ lọc phiếu xuất bán hàng mượn"`, `V2BaseDataTable title="Phiếu xuất bán hàng mượn"`.

### Đổi 2 — BỎ nút "Tạo phiếu" + BỎ method createItem
Trong `<template #actions-bottom>`: **XOÁ nút "Tạo phiếu"** (`createItem`). GIỮ nút "Cấu hình cột" (`configColumns`). Xoá luôn method `createItem` khỏi `methods`. (Phiếu bán không tạo trực tiếp từ list.)

### Đổi 3 — Bộ lọc: CHỈ gửi param BE đọc
BE `BorrowSell::searchByFilter` CHỈ đọc: `code`, `status`, `contractable_type`, `startDate`, `endDate`. TUYỆT ĐỐI không gửi param khác (contract_code/customer/created_by/export_type/type — BE bỏ qua, gây hiểu nhầm).

`initialStateForm` mới:
```js
const initialStateForm = {
    code: '',              // ô tìm nhanh (mã phiếu, LIKE)
    contractable_type: '', // loại HĐ (morph string, xem options dưới)
    status: '',
    startDate: '',
    endDate: '',
}
```

Options loại HĐ — param `contractable_type` nhận CHUỖI morph (KHÔNG phải 1/2):
```js
const CONTRACT_TYPE_OPTIONS = [
    { id: 'App\\Model\\Sale\\Firm\\Contract\\FirmContract', name: 'HĐ hãng' },
    { id: 'App\\Model\\Customers\\WrServiceContract', name: 'HĐ dịch vụ' },
]
```
Trạng thái — phiếu bán hiện chỉ có 1 giá trị (Đã duyệt); vẫn để 1 option cho nhất quán:
```js
const STATUS_OPTIONS = [ { id: 1, name: 'Đã duyệt' } ]
```

`filterFields()` computed CHỈ gồm (bỏ contract_code/created_by/type tab):
```js
filterFields() {
    return [
        { key: 'contractable_type', label: 'Loại hợp đồng', type: 'select', options: CONTRACT_TYPE_OPTIONS, placeholder: 'Chọn loại hợp đồng' },
        { key: 'status', label: 'Trạng thái', type: 'select', options: STATUS_OPTIONS, placeholder: 'Chọn trạng thái' },
        { key: 'startDate', label: 'Ngày tạo từ', type: 'date', placeholder: 'Từ ngày' },
        { key: 'endDate', label: 'Ngày tạo đến', type: 'date', placeholder: 'Đến ngày' },
    ]
}
```
`ignoredFields: ['code']` giữ nguyên (ô tìm nhanh chờ bấm Tìm kiếm). `quickSearchValue="filters.code"`, `quickSearchPlaceholder="Tìm theo mã phiếu..."`.

### Đổi 4 — Cột bảng (thêm cột Tổng tiền, đổi route link)
`allColumns()`:
```js
allColumns() {
    return [
        { key: 'index', title: 'STT', width: '60px', minWidth: '60px', sticky: true, align: 'left', locked: true },
        { key: 'code', title: 'Mã phiếu', width: '160px', minWidth: '160px', sticky: true, align: 'left', locked: true },
        { key: 'type_name', title: 'Loại phiếu', width: '150px', minWidth: '150px', align: 'left', cellClass: 'text-wrap' },
        { key: 'contract_code', title: 'Mã HĐ', width: '150px', minWidth: '150px', align: 'left', cellClass: 'text-wrap' },
        { key: 'customer_name', title: 'Khách hàng', width: '220px', minWidth: '220px', align: 'left', cellClass: 'text-wrap' },
        { key: 'creator_name', title: 'Người tạo', width: '170px', minWidth: '170px', align: 'left', cellClass: 'text-wrap' },
        { key: 'sum_amount_after_extra_after_vat', title: 'Tổng tiền', width: '150px', minWidth: '150px', align: 'right' },
        { key: 'created_at', title: 'Ngày tạo', width: '140px', minWidth: '140px', align: 'left' },
        { key: 'status', title: 'Trạng thái', width: '140px', minWidth: '140px', align: 'center' },
        { key: 'actions', title: 'Hành động', width: '110px', minWidth: '110px', align: 'center', locked: true },
    ]
}
```
Cột `code` link `to`: `/finance/borrow-sells/${item.id}` (màn chi tiết T13, chưa tồn tại lúc này là bình thường).

Thêm slot cell cho cột tiền (định dạng số VN, có sẵn helper? nếu không chắc, format tối giản):
```vue
<template #cell-sum_amount_after_extra_after_vat="{ item }">
    <span class="field-line">{{ formatMoney(item.sum_amount_after_extra_after_vat) }}</span>
</template>
```
Method `formatMoney` — dùng helper dự án nếu có (kiểm tra `@/utils/common.js` xem có `formatCurrency`/`formatNumber`); nếu không có thì viết tối giản:
```js
formatMoney(v) {
    const n = Number(v || 0)
    return n.toLocaleString('vi-VN')
}
```
Giữ các slot cell type_name/contract_code/customer_name/creator_name/created_at/status/actions như Phase 1 (đổi route trong actions ở Đổi 5).

### Đổi 5 — Hành động dòng: CHỈ có "Xem"
`getRowActions(item)` rút gọn còn 1 action (fail-closed theo `is_can_view` BE trả, KHÔNG gán `true`):
```js
getRowActions(item) {
    return [
        {
            key: 'view',
            title: 'Xem',
            icon: 'ri-eye-line',
            to: `/finance/borrow-sells/${item.id}`,
            interactable: !!item.is_can_view,
        },
    ]
}
```
`handleRowAction`: phiếu bán không có action cần xử lý JS (Xem đã điều hướng qua `to`) → có thể để `handleRowAction` rỗng hoặc bỏ. XOÁ toàn bộ nhánh manager_approve/switch_board/board_approve/deny + method `runRowAction`, `handleDenyConfirm`, `denyItem`, `denyMessage`, và **XOÁ `<BaseConfirmModal deny-...>`** khỏi template + import `BaseConfirmModal` nếu không còn dùng. Xoá cả `api.deny/managerApprove/...` (api.js T10b không có các hàm này — nếu còn tham chiếu sẽ lỗi).

### Đổi 6 — Dọn import/mixin thừa
- Bỏ import `BaseConfirmModal` (nếu đã xoá modal). Bỏ khai báo trong `components`.
- Giữ `V2BaseButton` (còn nút Cấu hình cột), `V2BaseRowActions`, `V2BaseSmartFilterPanel`, `V2BaseDataTable`.
- Giữ `getNumericalOrder`, `mergeKnownFilters`. Bỏ những import không còn dùng.

## Phân quyền (KHÔNG hỏi thêm — đã chốt)
BE `searchByFilter` tự lọc phạm vi 4 cấp (all-company / company / department / self) — FE KHÔNG cần đọc `$store.state.permissions` cho list. Nút Xem chỉ dựa `item.is_can_view` (BE trả per-row). KHÔNG hard-code cờ quyền `= true` (pattern cấm `can[A-Za-z]*\s*=\s*true`).

## Kiểm tra trước khi báo cáo
- Đọc lại file: cân bằng thẻ template, không còn tham chiếu method/biến đã xoá (grep `deny`, `createItem`, `runRowAction`, `manager_approve` trong file phải sạch hoặc chỉ còn trong comment đã xoá).
- Nếu có eslint chạy được: `npx eslint pages/finance/borrow-sells/index.vue` (bỏ qua nếu không có, ghi rõ). KHÔNG `nuxt build`.
- Xác nhận chỉ gửi 5 param BE đọc (`buildParams` = `{...filters, page, per_page}` với filters chỉ gồm code/contractable_type/status/startDate/endDate).

## Report contract
- KHÔNG commit. Ghi report vào `.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-11-report.md`.
- Trả về ngắn: status; file đã tạo; danh sách param filter cuối cùng; formatMoney dùng helper sẵn hay tự viết; kết quả eslint; concerns.
