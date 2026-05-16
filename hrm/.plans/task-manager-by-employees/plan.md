# Plan: Báo cáo phân bổ nguồn lực dạng Gantt theo nhân viên (QLDA_BC_V2_11)

## Trạng thái
- Bắt đầu: 2026-04-08
- Tiến độ: 9/9 task ✅
- Người phụ trách: @junfoke

## Phase 1: Backend — Service + Resource + Controller + Route (DONE)

- [x] Task 1: Tạo TaskManagerByEmployeesReportService
  - getData(): query employees theo filter → query tasks overlap khoảng thời gian → tính capacity/utilization → group by department
  - buildGanttDays(): tạo mảng ngày cho Gantt header
  - Helper methods: applyTaskDateFilter(), applyTaskProjectFilter(), countDays(), getUtilizationStatus(), buildTaskRow()

- [x] Task 2: Tạo TaskManagerByEmployeesReportResource
  - Extends ApiResource, transform department data
  - apiPaginateWithTotal(): paginate theo department count

- [x] Task 3: Tạo Controller + Route
  - TaskManagerByEmployeesReportController extends BaseApiController (hoặc ApiController)
  - Method index(): validate from_date/to_date → gọi service → paginate → trả response kèm summary + gantt
  - Route: GET /assign/report/task-manager-by-employees

## Phase 2: Frontend — Components (DONE)

- [x] Task 4: Tạo GanttChart.vue
  - CSS Grid render timeline
  - Lane algorithm: xếp task không chồng nhau
  - Màu thanh: xanh (bình thường), cam (sắp hạn), đỏ (quá hạn)
  - Emit task-click

- [x] Task 5: Tạo TaskDetailModal.vue
  - b-modal size xl, bảng chi tiết task
  - Footer: tổng task + tổng giờ
  - V2BaseBadge cho trạng thái

- [x] Task 6: Tạo index.vue (trang chính)
  - V2BaseFilterPanel: company/dept/part filter, dự án, chế độ thời gian, ngày, khoảng công suất, checkbox NV có task
  - Table: sticky 7 cột trái + cột Gantt scroll
  - Row phòng ban (summary) + Row nhân viên (data + GanttChart inline)
  - V2BasePagination
  - Modal integration

## Phase 3: Verification (DONE)

- [x] Task 7: Kiểm tra EmployeeInfo relationships
  - Verify: workPosition, company, department relationships tồn tại
  - Fix eager load trong service nếu cần

- [x] Task 8: Xác minh hasAPermission helper + permission names
  - Tìm helper hasAPermission trong frontend
  - Xác nhận tên permission thực tế trong hệ thống

- [x] Task 9: Smoke test toàn bộ flow
  - Backend: route:list, test API response
  - Frontend: filter, search, Gantt render, modal, pagination, reset
