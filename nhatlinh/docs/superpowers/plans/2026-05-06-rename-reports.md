# Đổi tên báo cáo + Icon thông tin mục đích — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đổi tên menu cấp 2 và tiêu đề 9 trang báo cáo module Assign, thêm icon ℹ️ với popover mô tả mục đích báo cáo.

**Architecture:** Thêm prop optional `titleInfo` vào V2BaseFilterPanel (backward-compatible). Sửa label trong menu-sidebar.js. Cập nhật head() title + V2BaseFilterPanel title/titleInfo ở mỗi page.

**Tech Stack:** Nuxt 2 / Vue 2, Bootstrap-Vue (b-popover), Remixicon

---

### Task 1: Thêm prop `titleInfo` vào V2BaseFilterPanel

**Files:**
- Modify: `hrm-client/components/V2BaseFilterPanel.vue`

- [ ] **Step 1: Thêm prop `titleInfo`**

Trong block `props` (sau prop `subtitle`), thêm:

```javascript
titleInfo: {
    type: String,
    default: '',
},
```

- [ ] **Step 2: Sửa template — thêm icon + popover bên cạnh title**

Thay dòng 19:

```html
<p class="tp-section-title">{{ title }}</p>
```

thành:

```html
<p class="tp-section-title">
    {{ title }}
    <span v-if="titleInfo" :id="'title-info-' + _uid" class="title-info-icon ml-1">
        <i class="ri-information-line"></i>
    </span>
    <b-popover
        v-if="titleInfo"
        :target="'title-info-' + _uid"
        triggers="hover focus"
        placement="right"
    >
        {{ titleInfo }}
    </b-popover>
</p>
```

- [ ] **Step 3: Thêm style cho icon**

Trong block `<style scoped>`, thêm sau `.tp-section-subtitle`:

```css
.title-info-icon {
    cursor: pointer;
    color: #64748b;
    font-size: 14px;
    vertical-align: middle;
}
.title-info-icon:hover {
    color: #3b82f6;
}
```

- [ ] **Step 4: Verify** — mở bất kỳ trang nào dùng V2BaseFilterPanel, xác nhận không bị lỗi (vì chưa truyền `titleInfo`, icon không hiện = backward-compatible).

---

### Task 2: Đổi tên menu cấp 2 trong menu-sidebar.js

**Files:**
- Modify: `hrm-client/components/menu-sidebar.js:246-291`

- [ ] **Step 1: Đổi 5 label trong section Báo cáo → subItems**

Các thay đổi cụ thể (dòng → giá trị mới):

| Dòng | Giá trị hiện tại | Giá trị mới |
|------|-----------------|-------------|
| 251 | `'Meeting theo Dự án'` | `'Thời gian meeting theo dự án'` |
| 263 | `'Hiệu suất nhân viên theo Dự án'` | `'Hiệu suất làm việc theo dự án'` |
| 271 | `'Theo dõi giải pháp theo Phòng KD'` | `'Theo dõi YCLGP theo phòng KD'` |
| 275 | `'Báo cáo tổng hợp làm GP theo Phòng ban'` | `'Tổng hợp giải pháp theo phòng ban'` |
| 283 | `'Báo cáo phân bổ nguồn lực Gantt theo NV'` | `'Phân bổ nguồn lực dạng Gantt theo nhân viên'` |

---

### Task 3: meeting-by-employees — đổi tên + thêm titleInfo

**Files:**
- Modify: `hrm-client/pages/assign/report/meeting-by-employees/index.vue`

- [ ] **Step 1: Đổi head() title** (dòng 691)

Từ: `title: 'Theo dõi Meeting theo nhân viên'`
Sang: `title: 'Báo cáo thời gian meeting theo nhân viên'`

- [ ] **Step 2: Đổi V2BaseFilterPanel title** (dòng 6)

Từ: `title="Bộ lọc báo cáo theo nhân viên"`
Sang: `title="Bộ lọc báo cáo thời gian meeting theo nhân viên"`

- [ ] **Step 3: Thêm prop titleInfo vào V2BaseFilterPanel**

Thêm attribute:
```html
title-info="Xem được mỗi nhân viên trong khoảng thời gian được chọn có bao nhiêu cuộc meeting, loại nào, với KH nào, tổng thời gian, kết quả =>> Tổng hợp số liệu lên cấp phòng =>> Cấp công ty"
```

---

### Task 4: meeting-by-projects — đổi tên + thêm titleInfo

**Files:**
- Modify: `hrm-client/pages/assign/report/meeting-by-projects/index.vue`

- [ ] **Step 1: Đổi head() title** (dòng 883)

Từ: `title: 'Theo dõi Meeting theo từng dự án'`
Sang: `title: 'Báo cáo thời gian meeting theo dự án'`

- [ ] **Step 2: Đổi V2BaseFilterPanel title** (dòng 6)

Từ: `title="Bộ lọc báo cáo theo dự án"`
Sang: `title="Bộ lọc báo cáo thời gian meeting theo dự án"`

- [ ] **Step 3: Thêm prop titleInfo vào V2BaseFilterPanel**

Thêm attribute:
```html
title-info="Theo dõi mỗi dự án đã tổ chức bao nhiêu cuộc meeting, số liệu theo loại meeting, chi tiết các cuộc meeting trong dự án =>> Tông hợp số liệu"
```

---

### Task 5: prospective-projects — thêm titleInfo (giữ nguyên tên)

**Files:**
- Modify: `hrm-client/pages/assign/report/prospective-projects/components/ProspectiveProjectsFilter.vue`

Lưu ý: trang này dùng component con `ProspectiveProjectsFilter.vue` chứa V2BaseFilterPanel, không nằm trực tiếp trong index.vue.

- [ ] **Step 1: Thêm prop titleInfo vào V2BaseFilterPanel** (dòng 2-3)

Thêm attribute sau `title="Bộ lọc báo cáo dự án TKT"`:
```html
title-info="Theo dõi toàn bộ vòng đời dự án TKT từ bước khởi tạo dự án tiền khả thi cho tới lập được hợp đồng hoặc đóng dự án."
```

---

### Task 6: solution-requests-by-department — đổi tên + thêm titleInfo

**Files:**
- Modify: `hrm-client/pages/assign/report/solution-requests-by-department/index.vue`

- [ ] **Step 1: Đổi head() title** (dòng 666)

Từ: `title: 'Báo cáo theo dõi yêu cầu làm giải pháp của nhân viên - phòng ban (Kinh doanh)'`
Sang: `title: 'Báo cáo theo dõi yêu cầu làm giải pháp theo phòng kinh doanh'`

- [ ] **Step 2: Đổi V2BaseFilterPanel title** (dòng 18)

Từ: `title="Bộ lọc báo cáo yêu cầu làm giải pháp"`
Sang: `title="Bộ lọc báo cáo theo dõi yêu cầu làm giải pháp theo phòng kinh doanh"`

- [ ] **Step 3: Thêm prop titleInfo vào V2BaseFilterPanel**

Thêm attribute:
```html
title-info="Thống kê số lượng Yêu cầu làm giải pháp theo Công ty → Phòng ban → Nhân viên kinh doanh, theo dõi tiến trình xử lý các yêu cầu đó."
```

---

### Task 7: solutions-work-summary-by-department — đổi tên + thêm titleInfo

**Files:**
- Modify: `hrm-client/pages/assign/report/solutions-work-summary-by-department/index.vue`

- [ ] **Step 1: Đổi head() title** (dòng 807)

Từ: `title: 'Báo cáo tổng hợp làm giải pháp theo Phòng ban'`
Sang: `title: 'Báo cáo tổng hợp giải pháp theo phòng ban'`

- [ ] **Step 2: Đổi V2BaseFilterPanel title** (dòng 13)

Từ: `title="Bộ lọc báo cáo làm giải pháp"`
Sang: `title="Bộ lọc báo cáo tổng hợp giải pháp theo phòng ban"`

- [ ] **Step 3: Thêm prop titleInfo vào V2BaseFilterPanel**

Thêm attribute:
```html
title-info="Theo dõi được Phòng giải pháp đang làm bao nhiêu giải pháp, nhân viên phụ trách, nhân sự tham gia, các mốc thời gian, tiến độ đang tới đâu."
```

---

### Task 8: solution-versions — thêm titleInfo (giữ nguyên tên)

**Files:**
- Modify: `hrm-client/pages/assign/report/solution-versions/index.vue`

- [ ] **Step 1: Thêm prop titleInfo vào V2BaseFilterPanel** (dòng 5-6)

Thêm attribute sau `title="Bộ lọc theo dõi version giải pháp"`:
```html
title-info="Báo cáo này theo dõi quá trình hoàn thiện giải pháp và lịch sử thay đổi của các giải pháp kỹ thuật thông qua các phiên bản."
```

---

### Task 9: performance-by-employee — thêm titleInfo (giữ nguyên tên)

**Files:**
- Modify: `hrm-client/pages/assign/report/performance-by-employee/index.vue`

- [ ] **Step 1: Thêm prop titleInfo vào V2BaseFilterPanel** (dòng 16)

Thêm attribute sau `title="Bộ lọc báo cáo hiệu suất nhân viên theo Dự án"`:
```html
title-info="Thống kê hiệu suất làm việc của nhân viên theo Phòng ban → Nhân viên → Dự án, dựa trên số lượng task và số giờ giao – thực tế."
```

---

### Task 10: performance-by-solutions — thêm titleInfo (giữ nguyên tên)

**Files:**
- Modify: `hrm-client/pages/assign/report/performance-by-solutions/index.vue`

- [ ] **Step 1: Thêm prop titleInfo vào V2BaseFilterPanel** (dòng 5)

Thêm attribute sau `title="Bộ lọc báo cáo hiệu suất theo Giải pháp"`:
```html
title-info="Thống kê hiệu suất làm việc của Phòng ban làm giải pháp → Giải pháp dựa trên số hạng mục, tổng nhân sự tham gia và giờ dự toán / thực tế."
```

---

### Task 11: task-manager-by-employees — thêm titleInfo (giữ nguyên tên)

**Files:**
- Modify: `hrm-client/pages/assign/report/task-manager-by-employees/index.vue`

- [ ] **Step 1: Thêm prop titleInfo vào V2BaseFilterPanel** (dòng 5-6)

Thêm attribute sau `title="Bộ lọc phân bổ nguồn lực (Gantt)"`:
```html
title-info="Xem task của từng nhân viên trên trục thời gian ngày / tuần / tháng, kèm công suất sử dụng để biết ai đang rảnh, đủ tải, quá tải."
```

---

### Task 12: Verify toàn bộ

- [ ] **Step 1:** Mở từng trang báo cáo, kiểm tra:
  - Menu sidebar hiển thị đúng tên mới
  - Title trên tab trình duyệt đúng
  - V2BaseFilterPanel hiển thị đúng tên mới
  - Icon ℹ️ xuất hiện bên cạnh title
  - Hover vào icon → popover hiển thị đúng nội dung mục đích
  - Popover ẩn khi di chuột ra ngoài

Danh sách 9 URL cần test:
1. `/assign/report/meeting-by-employees`
2. `/assign/report/meeting-by-projects`
3. `/assign/report/prospective-projects`
4. `/assign/report/solution-requests-by-department`
5. `/assign/report/solutions-work-summary-by-department`
6. `/assign/report/solution-versions`
7. `/assign/report/performance-by-employee`
8. `/assign/report/performance-by-solutions`
9. `/assign/report/task-manager-by-employees`
