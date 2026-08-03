# Task 7 — Trang dashboard `pages/warehouse/dashboard/index.vue`

## File tạo

- `nhatlinh-client/pages/warehouse/dashboard/index.vue` (mới)

## Cách khớp pattern `sale/dashboard/index.vue`

- Sao chép cơ chế tổng thể: `PageTitleMixin` (không có component `PageHeader` riêng trong dự án — `sale-dashboard` cũng dùng `pageTitle` computed + mixin này, nên áp dụng y hệt thay vì bịa `PageHeader`).
- `dispatch('warehouse-dashboard/get', queryString)` với `queryString` build bằng `buildQueryString({ granularity, top_from, top_to })` từ `@/utils/url-action` — giống hệt cách `sale-dashboard` gọi `buildQueryString(...)` rồi `dispatch('sale-dashboard/get', query)`.
- Đọc thẳng `response.data.<field>` (response thô `{code, message, data}` từ `apiGetMethod`), có fallback `emptyDashboard()` giống pattern `emptyDashboard()` của sale-dashboard.
- `<apexchart type="bar">` khai báo lazy-load `apexchart: () => import('vue-apexcharts')`, cấu trúc `chartOptions`/`series` là computed, y hệt cách sale-dashboard tổ chức (`revenueOptions`/`revenueSeries`, `topOptions`/`topSeries`).
- Loading toàn trang (`v-if="loading"` → `b-spinner` + text) và empty-state (`empty-state` block với icon Remix + text) — copy nguyên khối `<div class="empty-state py-5 text-center">` của sale-dashboard.
- Style tổng thể (`dash-panel`, `kpi-card`, `panel-head`, `chart-card`, `empty-state`, animation `fadeUp`) — copy nguyên block CSS scoped của sale-dashboard rồi chỉnh màu/nội dung cho phù hợp domain kho.

## Điểm khác biệt có chủ đích (đã cân nhắc theo CLAUDE.md — "FE: Tuân thủ style list của module đang triển khai")

- **`formatNumber`**: dùng method cục bộ `formatNumber(val) { return Number(val||0).toLocaleString('vi-VN', {maximumFractionDigits:2}) }` — đúng convention đã có sẵn trong **module Kho** (`pages/warehouse/report/inventory.vue`, `pages/warehouse/report/stock-card.vue`), KHÔNG dùng filter global `| formatNumber` (filter đó trả `'-'` khi giá trị = 0, không phù hợp hiển thị số lượng tồn kho có thể = 0 hợp lệ, ví dụ hàng hết tồn).
- **Màu biểu đồ Nhập/Xuất**: `['#16A34A', '#DC2626']` (xanh=Nhập, đỏ=Xuất) — tái dùng đúng `TYPE_COLORS` (type 1=Nhập, type 2=Xuất) đã định nghĩa trong `stock-card.vue`, thay vì tự bịa màu mới.
- Không dùng `PageHeader` (component này không tồn tại trong dự án) — dùng `PageTitleMixin` + `pageTitle` computed đúng như `sale-dashboard` thực tế đang làm.

## Component/helper tái dùng

- `V2BaseDatePicker`, `V2BaseLabel` (cho 2 datepicker `top_from`/`top_to`).
- `PageTitleMixin`, `buildQueryString`, `dayjs` (từ `@/utils/plugins/dayjs.js`).
- Store `warehouse-dashboard` (đã có sẵn từ Task 6: `dispatch('apiGetMethod', 'warehouse/dashboard' + query, {root:true})`).
- `apexchart` (vue-apexcharts, lazy import).
- `<nuxt-link>`, `<b-spinner>` (global, bootstrap-vue).

## Checklist 6 khối (theo §5.2 spec)

1. **KPI hàng 1** (Nhập/Xuất/Chuyển chờ duyệt, có link `/warehouse/receipt`, `/warehouse/issue`, `/warehouse/transfer`) — done, dùng `nuxt-link` + `stretched-link`.
2. **KPI hàng 2** (Số kho / Mặt hàng đang có tồn / Hàng đã hết, không link) — done.
3. **Biểu đồ Nhập/Xuất theo thời gian** — `<apexchart type="bar">` 2 series (Nhập/Xuất), `categories` từ `movement_by_time.buckets[].label` (đã format lại theo granularity qua `formatBucketLabel()`), toggle **Tuần|Tháng|Quý|Năm** (`period-toggle` tự viết, không dùng `V2BaseButton` vì đây là bộ lọc/segmented-control chứ không phải action button theo `button-convention` skill — đã đọc skill trước khi quyết định). Đổi toggle → `changeGranularity()` → `fetchDashboard('chart')` → gọi lại toàn payload. Empty-state khi mọi bucket `in_qty=out_qty=0`. Full width, `loadingChart` spinner riêng cho khối này.
4+5. **Top xuất | Top nhập** — 2 `<apexchart type="bar" horizontal>`, `categories` = `product_name`, `series` = `quantity`. 2 `V2BaseDatePicker` dùng chung `topFrom`/`topTo` (mặc định `dayjs().startOf('year')` → hôm nay), `@change="onTopDateChange"` → `fetchDashboard('top')`. Có guard hoán đổi nếu `from > to`. Empty-state riêng từng chart khi mảng rỗng. `loadingTop` spinner dùng chung cho cả 2 (vì cùng 1 param điều khiển).
6+7. **Cảnh báo tồn thấp | Tồn theo kho** — bảng HTML (`table table-sm dash-table`, sticky header, scroll `max-height:360px`). Cảnh báo tồn thấp: cột Mã·Tên·Tồn hiện tại·Tồn tối thiểu·Thiếu (đỏ `#DC2626`, class `dash-table__danger`), giới hạn `slice(0,20)` (BE đã sort `shortage` desc). Tồn theo kho: cột Kho·Số mặt hàng·Tổng SL. Empty-state text đúng yêu cầu ("Không có hàng dưới ngưỡng" / "Chưa có dữ liệu tồn"). 2 bảng này không có control riêng nên không có spinner riêng, chỉ cập nhật cùng lúc `loading`/`loadingChart`/`loadingTop` (chấp nhận over-fetch nhẹ theo §4.1).

## Concerns

- Không chạy được `npm run dev`/`build` (Node 14.21.3 yêu cầu, môi trường agent chỉ có Node 12) — đã verify tĩnh: `<template>` compile OK qua `vue-template-compiler`, phần `<script>` parse OK qua `@babel/core` (có `sourceType: module`, đã test cả cú pháp optional chaining `?.` dùng trong catch-block, giống hệt pattern đã có ở `sale-dashboard`). Cần user reload trình duyệt để xác nhận runtime thực tế.
- Trang dashboard này phụ thuộc Task 6 (store `warehouse-dashboard.js`) đã tồn tại sẵn — đã đọc và xác nhận signature khớp: `actions.get({dispatch}, query)` → `dispatch('apiGetMethod', 'warehouse/dashboard'+query, {root:true})`, trả về response thô `{code,message,data}` đúng như bối cảnh đề bài.
- Route `/warehouse/receipt`, `/warehouse/issue`, `/warehouse/transfer` đã tồn tại (xác nhận qua `find pages/warehouse`) nên KPI link không bị 404.
- Chưa test permission gate `Xem dashboard kho` (Task 3/8, ngoài phạm vi Task 7) — trang tự nó không tự kiểm tra permission (đúng theo Global Constraint "không scope theo cấp", quyền được gate ở route/middleware BE + menu FE, không lặp lại ở page).
- Icon `ri-store-2-line`, `ri-archive-2-line`, `ri-alert-line`, `ri-bar-chart-grouped-line`, `ri-checkbox-circle-line`, `ri-inbox-line` — dùng Remix Icon theo đúng bộ icon dự án đang dùng (`ri-*`), một số icon là suy đoán tên hợp lý theo Remix Icon set chuẩn (chưa thể verify online trong môi trường agent) — nếu icon không tồn tại, Remix Icon sẽ chỉ không hiển thị glyph (không vỡ layout), rủi ro thấp.
