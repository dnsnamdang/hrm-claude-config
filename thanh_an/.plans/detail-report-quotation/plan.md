# Plan — Báo cáo chi tiết báo giá

## Phase 1: Backend API

- [x] Tạo method `detailReport` trong QuotationController (query join, paginate)
- [x] Tạo method `exportDetailReport` trong QuotationController
- [x] Tạo route cho 2 endpoint mới
- [x] Tạo Export class + Blade view cho Excel

## Phase 2: Frontend

- [x] Tạo `pages/plan/detail-report/index.vue` — bảng + pagination
- [x] Gọi API danh sách, hiển thị 25 cột
- [x] Nút Export Excel — gọi API export, download file
- [x] Format số, ngày đúng chuẩn

## Phase 3: Bộ lọc & Cải tiến

- [x] BE: thêm filter params — quotation_code, project_type, company_id (main_company_contractor), customer_id, province_id, employee_id
- [x] BE: refactor filter logic thành private method `applyDetailReportFilters`
- [x] FE: UI bộ lọc collapse — 7 ô lọc (text + Select2)
- [x] FE: load danh sách khách hàng từ `category/customers`, tỉnh thành từ `category/customer_provinces`
- [x] Mã báo giá link đến màn chi tiết `/plan/quotation/{id}`
- [x] Đổi style table sang `b-table-simple` theo chuẩn guarantee_contract
- [x] Sticky 2 cột đầu (STT + Mã báo giá) bằng `head-col-1/2`
- [x] Export Excel client-side bằng ExcelJS + file-saver (fetch all pages per_page=500)
- [x] Tiêu đề "BÁO CÁO CHI TIẾT BÁO GIÁ" merge 25 cột, nền vàng

## Phase 4: Phân quyền Xem theo cấp

- [x] BE: Thêm `applyDetailReportPermissions` — check 3 cấp quyền (tổng công ty / công ty / nhóm nghiệp vụ)
- [x] BE: Gọi `applyDetailReportPermissions` trong cả `detailReport` và `exportDetailReport`
- ~~FE: Không cần thay đổi~~ (phân quyền tự động ở BE, giống màn danh sách báo giá)

### Checkpoint — 2026-05-06
Vừa hoàn thành: Phase 4 — phân quyền Xem theo 3 cấp (tổng công ty / công ty / nhóm nghiệp vụ)
Đang làm dở: không có
Bước tiếp theo: không có — feature hoàn chỉnh
Blocked:
