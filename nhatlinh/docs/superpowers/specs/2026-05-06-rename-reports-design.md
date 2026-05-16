# Spec: Đổi tên báo cáo + Icon thông tin mục đích

## Mục tiêu

Đổi tên menu cấp 2 và tiêu đề các trang báo cáo trong module Assign theo đề xuất TPE, đồng thời thêm icon thông tin (ℹ️) bên cạnh tiêu đề báo cáo trên V2BaseFilterPanel — hover hiển thị popover mô tả mục đích báo cáo.

## Scope

- **Module**: Assign (FE only)
- **Số trang ảnh hưởng**: 9 trang báo cáo
- **Component dùng chung bị sửa**: `V2BaseFilterPanel.vue` (thêm prop optional, backward-compatible)

## Phần 1: Sửa V2BaseFilterPanel — thêm prop `titleInfo`

**File**: `components/V2BaseFilterPanel.vue`

Thêm prop:

```javascript
titleInfo: {
    type: String,
    default: '',
}
```

Sửa template dòng title từ:

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

Style cho icon:

```css
.title-info-icon {
    cursor: pointer;
    color: #64748b;
    font-size: 14px;
}
.title-info-icon:hover {
    color: #3b82f6;
}
```

## Phần 2: Đổi tên menu cấp 2

**File**: `components/menu-sidebar.js` (section `menuItemsAssign` → Báo cáo → subItems)

| # | Route | Tên hiện tại | Tên mới |
|---|-------|-------------|---------|
| 1 | meeting-by-employees | Thời gian meeting theo nhân viên | Giữ nguyên |
| 2 | meeting-by-projects | Meeting theo Dự án | **Thời gian meeting theo dự án** |
| 3 | prospective-projects | Dự án TKT theo PB - NV KD | Giữ nguyên |
| 4 | assign_task_department_by_customer | Thực hiện công việc theo PB - Khách hàng | Giữ nguyên (không có trong Excel) |
| 5 | performance-by-employee | Hiệu suất nhân viên theo Dự án | **Hiệu suất làm việc theo dự án** |
| 6 | performance-by-solutions | Hiệu suất làm việc theo Giải pháp | Giữ nguyên |
| 7 | solution-requests-by-department | Theo dõi giải pháp theo Phòng KD | **Theo dõi YCLGP theo phòng KD** |
| 8 | solutions-work-summary-by-department | Báo cáo tổng hợp làm GP theo Phòng ban | **Tổng hợp giải pháp theo phòng ban** |
| 9 | solution-versions | Theo dõi chỉ số hoàn thành GP theo version | Giữ nguyên |
| 10 | task-manager-by-employees | Báo cáo phân bổ nguồn lực Gantt theo NV | **Phân bổ nguồn lực dạng Gantt theo nhân viên** |
| 11 | work_and_performance | BC công được hưởng theo phiếu công tác | Giữ nguyên (không có trong Excel) |

## Phần 3: Đổi tên page title + thêm `titleInfo` cho từng trang

### 3.1 meeting-by-employees

**File**: `pages/assign/report/meeting-by-employees/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | Theo dõi Meeting theo nhân viên | Báo cáo thời gian meeting theo nhân viên |
| V2BaseFilterPanel title | Bộ lọc báo cáo theo nhân viên | Bộ lọc báo cáo thời gian meeting theo nhân viên |
| titleInfo (mới) | — | Xem được mỗi nhân viên trong khoảng thời gian được chọn có bao nhiêu cuộc meeting, loại nào, với KH nào, tổng thời gian, kết quả =>> Tổng hợp số liệu lên cấp phòng =>> Cấp công ty |

### 3.2 meeting-by-projects

**File**: `pages/assign/report/meeting-by-projects/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | Theo dõi Meeting theo từng dự án | Báo cáo thời gian meeting theo dự án |
| V2BaseFilterPanel title | (cần kiểm tra) | Bộ lọc báo cáo thời gian meeting theo dự án |
| titleInfo (mới) | — | Theo dõi mỗi dự án đã tổ chức bao nhiêu cuộc meeting, số liệu theo loại meeting, chi tiết các cuộc meeting trong dự án =>> Tông hợp số liệu |

### 3.3 prospective-projects

**File**: `pages/assign/report/prospective-projects/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | Giữ nguyên | Giữ nguyên |
| V2BaseFilterPanel title | Giữ nguyên | Giữ nguyên |
| titleInfo (mới) | — | Theo dõi toàn bộ vòng đời dự án TKT từ bước khởi tạo dự án tiền khả thi cho tới lập được hợp đồng hoặc đóng dự án. |

### 3.4 solution-requests-by-department

**File**: `pages/assign/report/solution-requests-by-department/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | Báo cáo theo dõi yêu cầu làm giải pháp của nhân viên - phòng ban (Kinh doanh) | Báo cáo theo dõi yêu cầu làm giải pháp theo phòng kinh doanh |
| V2BaseFilterPanel title | (cần kiểm tra) | Bộ lọc báo cáo theo dõi yêu cầu làm giải pháp theo phòng kinh doanh |
| titleInfo (mới) | — | Thống kê số lượng Yêu cầu làm giải pháp theo Công ty → Phòng ban → Nhân viên kinh doanh, theo dõi tiến trình xử lý các yêu cầu đó. |

### 3.5 solutions-work-summary-by-department

**File**: `pages/assign/report/solutions-work-summary-by-department/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | Báo cáo tổng hợp làm giải pháp theo Phòng ban | Báo cáo tổng hợp giải pháp theo phòng ban |
| V2BaseFilterPanel title | (cần kiểm tra) | Bộ lọc báo cáo tổng hợp giải pháp theo phòng ban |
| titleInfo (mới) | — | Theo dõi được Phòng giải pháp đang làm bao nhiêu giải pháp, nhân viên phụ trách, nhân sự tham gia, các mốc thời gian, tiến độ đang tới đâu. |

### 3.6 solution-versions

**File**: `pages/assign/report/solution-versions/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | Giữ nguyên | Giữ nguyên |
| V2BaseFilterPanel title | Giữ nguyên | Giữ nguyên |
| titleInfo (mới) | — | Báo cáo này theo dõi quá trình hoàn thiện giải pháp và lịch sử thay đổi của các giải pháp kỹ thuật thông qua các phiên bản. |

### 3.7 performance-by-employee

**File**: `pages/assign/report/performance-by-employee/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | (không có head()) | Giữ nguyên |
| V2BaseFilterPanel title | Bộ lọc báo cáo hiệu suất nhân viên theo Dự án | Giữ nguyên |
| titleInfo (mới) | — | Thống kê hiệu suất làm việc của nhân viên theo Phòng ban → Nhân viên → Dự án, dựa trên số lượng task và số giờ giao – thực tế. |

### 3.8 performance-by-solutions

**File**: `pages/assign/report/performance-by-solutions/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | (không có head()) | Giữ nguyên |
| V2BaseFilterPanel title | Bộ lọc báo cáo hiệu suất theo Giải pháp | Giữ nguyên |
| titleInfo (mới) | — | Thống kê hiệu suất làm việc của Phòng ban làm giải pháp → Giải pháp dựa trên số hạng mục, tổng nhân sự tham gia và giờ dự toán / thực tế. |

### 3.9 task-manager-by-employees

**File**: `pages/assign/report/task-manager-by-employees/index.vue`

| Vị trí | Giá trị hiện tại | Giá trị mới |
|--------|-----------------|-------------|
| `head()` title | Giữ nguyên | Giữ nguyên |
| V2BaseFilterPanel title | Giữ nguyên | Giữ nguyên |
| titleInfo (mới) | — | Xem task của từng nhân viên trên trục thời gian ngày / tuần / tháng, kèm công suất sử dụng để biết ai đang rảnh, đủ tải, quá tải. |

## Không nằm trong scope

- Trang `assign_task_department_by_customer` và `work_and_performance` — không có trong file Excel
- Không sửa backend, không sửa sidebar component
- Không đổi route URL
