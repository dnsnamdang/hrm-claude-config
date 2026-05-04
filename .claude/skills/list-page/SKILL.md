---
name: list-page
description: Quy tắc xây dựng màn danh sách với permission theo cấp
---

# Quy tắc xây dựng permission cho các màn danh sách tổng hợp
- Áp dụng cho các bảng có các field: company_id, department_id, part_id (field này có thể có hoặc không) =>> Nếu có thì quyền sẽ theo bộ quyền như sau Xem [Tên màn danh sách] theo công ty, Xem [Tên màn danh sách] theo phòng ban, Xem [Tên màn danh sách] theo bộ phận, Xem tất cả [Tên màn danh sách]
- Quyền xem tất cả =>> Lấy tất cả bản ghi trừ trạng thái Đang tạo / Nháp
- Các quyền còn lại query theo các field tương ứng
- Bộ lọc luông bắt đầu bằng: Lọc theo công ty >> Lọc theo phòng ban >> lọc theo bộ phận ==>> Tuân thủ theo V2BaseFilterPanel.vue
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