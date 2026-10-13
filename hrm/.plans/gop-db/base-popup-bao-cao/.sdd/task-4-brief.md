### Task 4: `reportDrillListMixin.js` — máy sắp xếp + phân trang

**Files:**
- Create: `hrm-client/utils/mixins/reportDrillListMixin.js`

**Interfaces:**
- Produces — **data**: `keyword`, `filters`, `sort`, `page`, `pageSize`, `summaryCollapsed`.
  **computed**: `sortedRows`, `pageCount`, `safePage`, `pageOffset`, `pagedRows`, `hasActiveFilter`.
  **methods**: `toggleSort(key)`, `onPageChange(page)`, `onPageSizeChange(size)`, `resetFilters()`, `applyLocalFilters(rows)`.
  **Component dùng mixin PHẢI tự khai**: `rows` (prop hoặc computed), `columns` (computed), `emptyFilters()` (trả object state lọc rỗng), và `onFilterChange()` (hook — mixin gọi sau khi `resetFilters()`).

- [ ] **Step 1: Viết mixin**

```js
/**
 * MÁY CLIENT-SIDE cho popup drill-down của màn báo cáo.
 *
 * CHỈ ôm phần 3 popup lớn giống hệt nhau: sắp xếp, phân trang, state bộ lọc.
 * KHÔNG ôm phần lọc — 3 popup dùng 3 chiến lược khác nhau (đo 2026-09-17):
 *   · DemandListModal      — lọc ở SERVER (emit `filter`, màn cha tải lại)
 *   · DevelopmentDrillModal — lọc CLIENT tại chỗ
 *   · ProjectListModal      — lọc ở SERVER, popup tự gọi API
 * Vì vậy `onFilterChange()` là HOOK do component tự cài, còn `applyLocalFilters()` là hàm
 * TUỲ CHỌN cho popup lọc client-side.
 *
 * Component dùng mixin phải khai: `rows`, `columns`, `emptyFilters()`, `onFilterChange()`.
 */
const dateSortKey = (value) => {
    if (!value) return null
    // Dữ liệu hiển thị dạng dd/mm/yyyy — `new Date()` đọc sai (hiểu là mm/dd)
    const m = String(value).match(/^(\d{2})\/(\d{2})\/(\d{4})/)
    if (m) return new Date(`${m[3]}-${m[2]}-${m[1]}`).getTime()
    const t = new Date(value).getTime()
    return Number.isNaN(t) ? null : t
}

export default {
    data() {
        return {
            keyword: '',
            filters: this.emptyFilters(),
            /* Sắp xếp TẠI CHỖ: popup đã có trọn tập của ô số đã bấm nên không gọi lại API */
            sort: { key: '', dir: 'asc' },
            page: 1,
            pageSize: 20,
            /* Mặc định THU GỌN — nhường chỗ cho bảng chi tiết (user chốt 2026-09-06) */
            summaryCollapsed: true,
        }
    },
    computed: {
        sortedRows() {
            const { key, dir } = this.sort
            if (!key) return this.rows

            const col = this.columns.find((c) => c.key === key)
            if (!col) return this.rows

            const isDate = col.sortType === 'date'
            const valueOf = (row) =>
                isDate
                    ? dateSortKey(row[col.field])
                    : (col.sortFields ? col.sortFields.map((f) => row[f] || '').join(' ') : String(row[col.field] || '')).trim()

            const sign = dir === 'desc' ? -1 : 1
            // Ô trống luôn xuống cuối ở CẢ 2 chiều — không thì bấm desc là cụm rỗng nhảy lên đầu
            return [...this.rows].sort((a, b) => {
                const va = valueOf(a)
                const vb = valueOf(b)
                const emptyA = isDate ? va === null : !va
                const emptyB = isDate ? vb === null : !vb
                if (emptyA && emptyB) return 0
                if (emptyA) return 1
                if (emptyB) return -1
                return sign * (isDate ? va - vb : va.localeCompare(vb, 'vi'))
            })
        },
        pageCount() {
            return Math.max(1, Math.ceil(this.sortedRows.length / this.pageSize))
        },
        /* Kẹp trong [1, pageCount]: bộ lọc cắt danh sách ngắn lại mà `page` còn giữ số cũ thì
           lấy thẳng `page` sẽ ra trang trắng. */
        safePage() {
            return Math.min(Math.max(1, this.page), this.pageCount)
        },
        pageOffset() {
            return (this.safePage - 1) * this.pageSize
        },
        pagedRows() {
            return this.sortedRows.slice(this.pageOffset, this.pageOffset + this.pageSize)
        },
        hasActiveFilter() {
            return !!this.keyword || Object.values(this.filters).some((v) => v !== null && v !== '' && !(Array.isArray(v) && !v.length))
        },
    },
    watch: {
        /* Đổi tập dữ liệu (lượt drill mới / cha tải lại) -> về trang 1. Chỉ dựa vào `safePage` là
           chưa đủ: tập mới vẫn nhiều trang thì người dùng bị bỏ lại ở trang 3 của kết quả khác. */
        rows() {
            this.page = 1
        },
    },
    methods: {
        toggleSort(key) {
            if (this.sort.key === key) this.sort = { key, dir: this.sort.dir === 'asc' ? 'desc' : 'asc' }
            else this.sort = { key, dir: 'asc' }
        },
        onPageChange(page) {
            this.page = page
        },
        onPageSizeChange(size) {
            this.pageSize = size
            this.page = 1
        },
        resetFilters() {
            this.keyword = ''
            this.filters = this.emptyFilters()
            this.page = 1
            this.onFilterChange()
        },
        /** TUỲ CHỌN — chỉ popup lọc client-side gọi tới. Khớp chuỗi không dấu phân biệt hoa thường. */
        applyLocalFilters(rows) {
            const kw = this.keyword.trim().toLowerCase()
            return rows.filter((row) => {
                const okFilters = Object.keys(this.filters).every((param) => {
                    const want = this.filters[param]
                    if (want === null || want === '') return true
                    return String(row[param]) === String(want)
                })
                if (!okFilters) return false
                if (!kw) return true
                return Object.values(row).some((v) => String(v == null ? '' : v).toLowerCase().includes(kw))
            })
        },
    },
}
```

- [ ] **Step 2: Kiểm mixin không phá build**

```bash
curl -s http://127.0.0.1:3000/assign/report/potential-customer-care -o /dev/null -w "%{http_code}\n"
```

Expected: `200`, log dev server không có `Failed to compile`.

- [ ] **Step 3: Commit**

```bash
git add utils/mixins/reportDrillListMixin.js
git commit -m "feat(report): thêm reportDrillListMixin (sắp xếp + phân trang popup báo cáo)"
```

---

