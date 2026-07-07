# Giữ lọc màn bid_package/dashboard (tham chiếu plan/dashboard) — @khoipv

## Bối cảnh
- Cơ chế giữ lọc dashboard nằm trong 3 card dùng chung `FilterPieChartCard` / `FilterLineChartCard` / `FilterColumnChartCard`, lưu localStorage qua `utils/dashboard-chart-filter.js`, key theo prop `module` (`dashboard-filter-{pie,line,column}-{module}`), hết hạn 10 phút.
- `BidPackageDashboard.vue` đã truyền `module="bid_package"` nên ĐÃ lưu lọc. Nhưng khác `PlanDashboard.vue` ở các prop mapping → khi khôi phục, giá trị lọc (text trạng thái/địa bàn) không map lại được id/option ⇒ lọc bị rớt/không giữ đúng.

## Khác biệt so với plan/dashboard
- Pie: bid_package dùng sai tên prop `region-mapping` (đúng phải là `area-mapping`).
- Column: bid_package thiếu `status-options`, `status-mapping`, `area-mapping`.

## Task
### bid_package/dashboard (`BidPackageDashboard.vue`)
- [x] Pie card: đổi `:region-mapping="regionMapping"` → `:area-mapping="regionMapping"`
- [x] Column card: thêm `:status-options`, `:status-mapping`, `:area-mapping`

### contract/dashboard (`ContractDashboard.vue`) — cùng lỗi
- [x] Pie card: đổi `:region-mapping="regionMapping"` → `:area-mapping="regionMapping"`
- [x] Column card: thêm `:status-options="contractStatusOptions"`, `:status-mapping="contractStatuses"`, `:area-mapping="regionMapping"`

- [ ] Verify UI: đặt lọc → rời trang → quay lại thấy giữ đúng (Pie + Column) cho cả 2 màn

## Phạm vi
- Chỉ FE, 2 file:
  - `hrm-thanhan-client/components/dashboad/BidPackageDashboard.vue`
  - `hrm-thanhan-client/components/dashboad/ContractDashboard.vue`
- Lưu ý: `PlanDashboard.vue` vốn đã đúng (chuẩn tham chiếu), không đụng.
