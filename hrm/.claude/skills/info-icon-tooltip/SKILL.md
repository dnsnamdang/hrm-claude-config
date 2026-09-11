---
name: info-icon-tooltip
description: Use when thêm/sửa icon Info (chữ "i") kèm tooltip/popover mô tả ở FE hrm-client — icon giải thích cột, tiêu đề bảng, ô nhập, dòng trong dropdown. Chuẩn hoá 1 kiểu duy nhất cho toàn hệ thống.
---

# Skill: Icon Info + Tooltip mô tả

Mục tiêu: **mọi màn dùng CHUNG một kiểu icon Info + một kiểu popover**. Trước skill này mỗi màn tự
làm một kiểu (vòng tròn chữ `i` tự vẽ, `fa-info-circle`, `title` HTML, `v-b-tooltip` đen…) nên
UI lệch nhau giữa các phân hệ.

---

## 1. Chuẩn bắt buộc

| Thành phần | Giá trị |
| --- | --- |
| Icon | `<i class="ri-information-line">` — **KHÔNG** dùng `fa-info-circle`, không tự vẽ vòng tròn chữ `i` |
| Cỡ icon | `font-size: 14px` |
| Màu icon | `#94a3b8` (xám), hover đậm lại `#64748b` |
| Con trỏ | `cursor: pointer` |
| Tooltip | `<b-popover>` + `custom-class="info-popover"` |
| Trigger | `triggers="hover focus"` |
| Vị trí | `placement="bottom"` (bootstrap tự lật khi thiếu chỗ) |

`.info-popover` khai ở `assets/scss/custom/components/_popover.scss` (`max-width: 420px`).
Phần còn lại (nền trắng, viền `#dee2e6`, radius 4px, arrow 8×16, font, padding) là style
`.popover` mặc định của bootstrap — **không ghi đè, không copy tay giá trị**.

---

## 2. Cách làm mặc định (99% trường hợp)

Dùng khi icon nằm trong DOM do Vue quản lý: cạnh tiêu đề bảng, nhãn cột, label ô nhập, tên chart…

```vue
<h2 class="tp-section-title mb-0 mt-0 d-inline-flex align-items-center" style="gap: 6px">
    Bảng chi tiết meeting theo dự án
    <span
        id="meeting-proj-info-icon"
        class="no-print"
        style="cursor: pointer; color: #94a3b8; font-weight: normal"
    >
        <i class="ri-information-line" style="font-size: 14px"></i>
    </span>
    <b-popover
        target="meeting-proj-info-icon"
        triggers="hover focus"
        placement="bottom"
        custom-class="info-popover"
    >
        Click mũi tên để mở/đóng cấp con. Click chip ở cột Trạng thái/Loại/Hình thức để xem popup.
    </b-popover>
</h2>
```

Quy tắc phụ:
- `id` của target phải **duy nhất trong 1 trang**. Trong `v-for` thì ghép id theo key/index
  (`:id="'row-info-' + row.id"` + `:target="'row-info-' + row.id"`), không dùng id tĩnh.
- Icon nằm trong khối sẽ IN ra giấy → thêm `class="no-print"`.
- Nội dung ngắn, 1–2 câu, không HTML phức tạp.

**File tham khảo** (copy nguyên mẫu từ đây):
`pages/assign/report/meeting-by-projects/components/MeetingByProjectsTable.vue:9-17`

Các màn đã làm đúng chuẩn (dùng để đối chiếu, đừng phát minh lại):
- `components/TopProjectsChart.vue`
- `pages/assign/prospective-projects/components/ProjectInfoSection.vue`
- `pages/assign/report/meeting-by-projects/components/MeetingByProjectsTable.vue`
- `pages/assign/report/meeting-by-employees/components/MeetingByEmployeesTable.vue`
- `pages/assign/report/meeting-by-employees/components/TopDepartmentsChart.vue`
- `pages/assign/report/performance-by-solutions/components/PerformanceBySolutionsTable.vue`
- `pages/assign/report/solution-requests-by-department/components/SolutionRequestsTable.vue`
- `pages/assign/report/solutions-work-summary-by-department/index.vue`

---

## 3. Trường hợp đặc biệt: icon nằm TRONG dropdown select2

`b-popover` cần một element `target` cố định. Dropdown select2 được append vào `<body>`
(ngoài cây DOM component) và các dòng option bị **tạo/xoá lại mỗi lần mở** → `b-popover`
không gắn được. Trường hợp này dùng helper có sẵn, **KHÔNG tự viết tooltip mới**:

- `utils/meetingTypeInfoTooltip.js` — 1 popover singleton + listener uỷ quyền ở `document`
  theo attribute `data-mt-info`. Element được dựng bằng **đúng bộ class bootstrap**
  (`popover b-popover bs-popover-{right|left} info-popover` + `.arrow` + `.popover-body`)
  nên giao diện khớp tuyệt đối với mục 2.
- `components/MeetingTypeSelect.vue` — ví dụ hoàn chỉnh: bọc `V2BaseSelect`/`V2BaseSelectInModal`,
  truyền `extraSettings` với `templateResult` / `templateSelection` / `escapeMarkup`.

Cần select danh mục khác cũng có icon Info → **nhân bản `MeetingTypeSelect.vue`** (hoặc tổng quát hoá nó),
tái dùng nguyên `meetingTypeInfoTooltip.js`, không viết tooltip thứ hai.

### 3 bẫy định vị (đã dính khi làm #11045 — đừng "đơn giản hoá" lại)
1. **z-index**: `.popover` bootstrap là `1060`, dropdown select2 trong project là `9999`.
   Không ép cao hơn (đang dùng `10050`) thì khi popover lật sang trái nó đè lên dropdown
   nhưng bị vẽ phía sau → **tooltip mất hẳn**, rất khó đoán nguyên nhân.
2. **margin của popover**: `.bs-popover-right` có sẵn `margin-left` = chiều cao arrow. Element
   `position: absolute` định vị theo `left` nên margin-left **dịch cả hộp** → phải trừ ra, không thì
   khoảng hở cộng đôi (16px thay vì 8px). Ngược lại `margin-right` của `.bs-popover-left`
   **KHÔNG** dịch hộp (đã ghim `left`) → trừ vào là arrow đè lên icon.
3. **margin của arrow**: `.arrow` của popover trái/phải có `margin: 4px 0` → tính `top` cho arrow
   phải trừ `margin-top`, không thì arrow lệch xuống đúng bằng margin đó.

### Icon trong ô select đã chọn
Icon nằm sát nút xoá (×) của select2 → chừa khoảng trống, nếu không 2 thứ dính vào nhau:
```scss
.mt-selection-row { padding-right: 10px; }   // đo được ~10px là đủ thoáng
```

---

## 3b. Icon Info hiển thị DỮ LIỆU của bản ghi trong bảng danh sách

Áp dụng khi 1 cột có thông tin phụ **của từng dòng** (giá theo cấp, hệ số, tổng phụ…) mà không
đáng chiếm hẳn 1 cột. Dùng **đúng chuẩn ở mục 1-2**, chỉ khác 2 điểm:

- `id` ghép theo id bản ghi: `:id="'service-price-info-' + item.id"` + `:target` tương ứng.
- Icon đặt **cạnh giá trị của ô**, không đặt trên tiêu đề cột (tiêu đề cột nói về CẢ cột,
  còn đây là dữ liệu của riêng dòng đó).

```vue
<template #cell-name="{ item }">
    <span class="field-line text-dark font-weight-normal">{{ item.name || '' }}</span>
    <template v-if="hasPriceByLevel(item)">
        <span :id="`service-price-info-${item.id}`" class="ml-1" style="cursor: pointer; color: #94a3b8">
            <i class="ri-information-line" style="font-size: 14px"></i>
        </span>
        <b-popover :target="`service-price-info-${item.id}`" triggers="hover focus"
                   placement="bottom" custom-class="info-popover">
            <div v-for="lv in item.price_by_level" :key="lv.level_name">
                {{ lv.level_name }}: {{ formatPrice(lv.price) }}
            </div>
        </b-popover>
    </template>
</template>
```

Khuôn: `pages/customer-care/services/index.vue` (cột Tên gói bảo dưỡng — giá theo cấp dịch vụ).

**Đừng gắn tooltip thẳng vào giá trị của ô.** Màn này trước đây để `v-b-tooltip` ngay trên tên gói:
đúng nội dung nhưng (1) sai hệ tooltip, (2) nhìn vào không biết là hover được — cột Tên theo
`list-page` mục 3 là chữ thường, không phải vùng tương tác. Phải tách ra icon `(i)` riêng.

⚠️ **Chỉ dùng cho nội dung ĐỌC, gọn (vài dòng).** Nội dung là cả một bảng nhiều cột, hoặc bấm vào
để làm gì đó → đó là **nút hành động**, không phải icon Info: dùng nút/link có nhãn rõ ràng mở
popup (khuôn "Hàng hoá áp dụng" ở `pages/customer-care/device-errors/index.vue`).

---

## 4. Không dùng

| Kiểu | Vì sao không |
| --- | --- |
| `<i class="fas fa-info-circle">` | Font-awesome, lệch cỡ/màu với `ri-*` của V2. Còn tồn ở vài màn Assign — gặp thì đổi luôn khi sửa vùng đó, không sửa đại trà |
| Tự vẽ vòng tròn + chữ `i` bằng CSS | Không khớp nét với `ri-information-line`, mỗi màn ra một cỡ |
| `title="..."` thuần HTML | Tooltip mặc định của trình duyệt: chậm hiện, không style được, khác hẳn các màn khác. Chỉ dùng cho `<label>` phụ, không dùng cho icon Info |
| `v-b-tooltip` (tooltip đen) | Khác hệ với `.info-popover`. Rice/Training đang dùng — đừng lan sang Assign/QLDA |
| Tự viết div tooltip + style tay | Sẽ lệch màu/font/padding ngay lần bootstrap đổi biến |

---

## Checklist trước khi kết thúc task có icon Info

- [ ] **Đã grep project xem chỗ nào làm rồi** (`grep -rn 'custom-class="info-popover"'`) và copy theo, không tự nghĩ kiểu mới
- [ ] Icon là `ri-information-line`, 14px, `#94a3b8`, `cursor: pointer`
- [ ] Tooltip là `b-popover` + `custom-class="info-popover"` + `triggers="hover focus"`
- [ ] `id` target duy nhất trong trang (trong `v-for` phải ghép theo key)
- [ ] Icon trong vùng in → có `no-print`
- [ ] Nếu icon nằm trong dropdown select2 → tái dùng `utils/meetingTypeInfoTooltip.js`, không viết tooltip mới
- [ ] Hover thử thật: popover hiện đủ nội dung, không tràn viewport, không bị dropdown/modal che
