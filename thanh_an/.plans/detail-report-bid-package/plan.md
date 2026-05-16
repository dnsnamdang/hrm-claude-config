# Plan: Báo cáo chi tiết thầu

## Phase 1 — Backend

- [x] Thêm route `GET /detail-report` vào group `bid_packages` trong `Modules/Category/Routes/api.php`
- [x] Thêm method `detailReport()` vào `BidPackageController`
- [x] Thêm method `applyBidPackageDetailReportPermissions()` (3 cấp)
- [x] Thêm method `applyBidPackageDetailReportFilters()` (9 filters)
- [x] Tạo 3 permissions trong DB (id 498-500)
- [x] Sửa cột "Loại thầu" dùng `bid_type` (Trong thầu / Nhảy thầu)
- [x] Sửa cột "Đơn giá" → "Đơn giá chào thầu" dùng `price_bid_package`
- [x] Sửa cột "Nhân viên" lấy từ `employee_id` (NV thực hiện)
- [x] Sửa cột "Ngày kết chuyển" lấy từ `contract_acceptance_date`
- [x] Thêm lưu `contract_acceptance_date` ở nhánh else (khi gửi thông báo phân công)
- [x] Thêm `contract_id` vào API response

## Phase 2 — Frontend

- [x] Tạo `pages/bid_package/detail-report/index.vue`
- [x] Bảng 27 cột theo file mẫu Excel
- [x] 9 bộ lọc (filters)
- [x] Phân trang
- [x] Export Excel bằng ExcelJS (client-side)
- [x] Link mã gói thầu → detail page
- [x] Link số hợp đồng bán → detail hợp đồng
- [x] Thêm menu "Báo cáo" → "Báo cáo chi tiết thầu" vào MenuBidPackage.js

### Checkpoint — 2026-05-06
Vừa hoàn thành: Toàn bộ feature báo cáo chi tiết thầu
Đang làm dở: không
Bước tiếp theo: không
Blocked: không
