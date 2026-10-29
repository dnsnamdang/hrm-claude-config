# Plan — YCXH (Yêu cầu xuất hàng) hiển thị trạng thái = số thô "15"

> Nhánh: `gop_db` (hrm-api + hrm-client) · Tạo: 2026-10-12
> Màn HRM: `finance/product-export-requests` · BE: Module `Assign` (endpoint `assign/product-export-requests`)
> Phân loại: **BOUNDED** (bug nhỏ — port thiếu dữ liệu trạng thái)

## Triệu chứng
- Trên dev `dev-hrm.eteksofts.com/finance/product-export-requests`, phiếu **PYCXH-41687** hiện cột
  Trạng thái là số thô **"15"** thay vì badge có tên.

## Nguyên nhân gốc (đã xác minh)
- Cột status của list do `Modules/Assign/Transformers/ProductExportRequestResource.php:51-52` phân giải:
  `status_name = $statusList[$status]['name'] ?? null`, với
  `$statusList = Modules\Assign\Entities\Warehouse\ProductExportRequest::getStatusList()`.
- `getStatusList()` (entity Assign, dòng 158-173) **chỉ map trạng thái 1-11**.
- ERP `app/Model/Warehouse/ProductExportRequest.php::STATUSES` (nguồn port) có **1-19**:
  - 12 `DANG_QUYET_TOAN` = "Đang quyết toán"
  - 13 `DA_QUYET_TOAN` = "Đã quyết toán"
  - 14 `CHO_DUYET_NHAP` = "Chờ duyệt nhập"
  - **15 `DANG_DE_NGHI_NHAP` = "Đang đề nghị nhập"** ← trạng thái của PYCXH-41687
  - 16 `DA_DE_NGHI_NHAP` = "Đã đề nghị nhập"
  - 17 `DANG_NHAP_KHO_NHAP` = "Đang nhập kho"
  - 18 `DA_NHAP_KHO_NHAP` = "Đã nhập kho"
  - 19 `DANG_HACH_TOAN_NHAP` = "Đang hạch toán nhập"
- Đây là bộ trạng thái **chặng NHẬP VỀ** của phiếu xuất điều chuyển nội bộ (type 6) / xuất trả NCC.
  HRM port thiếu nên phiếu đạt status 15 không có tên/màu → FE hiện số thô (hoặc ô trống tùy bản build).
- `getStatusList()` còn được dùng ở `ProductExportRequestController::index` (export tay, dòng 234) và
  `ProductExportRequestService.php:259` → sửa 1 chỗ map là khớp tất cả.
- FE `pages/finance/product-export-requests/index.vue` có `statusOptions` (bộ lọc) hard-code **1-11** → cũng thiếu.

## Công việc
### Task 1 — [BE] Bổ sung trạng thái 12-19 vào getStatusList (port đủ ERP STATUSES)
- [x] `Modules/Assign/Entities/Warehouse/ProductExportRequest.php`: thêm 8 hằng `STATUS_*` (12-19) +
      8 entry vào `getStatusList()`, tên khớp ERP, màu theo bảng 9 màu chuẩn (12/15/17/19→#2563EB
      đang thực hiện; 14→#D97706 chờ duyệt; 16→#0EA5E9 theo dõi; 13/18→#16A34A hoàn thành).
      Giữ nguyên 11 entry cũ (màu Material hex) theo chỉ đạo user.

### Task 2 — [FE] Bổ sung 12-19 vào statusOptions (bộ lọc)
- [x] `pages/finance/product-export-requests/index.vue`: thêm 8 option trạng thái vào `statusOptions`.

### Task 3 — Kiểm tra
- [x] Playwright (2026-10-12): tạm set PYCXH-35690 status=15 → cột Trạng thái hiện badge xanh
      "Đang đề nghị nhập" (không còn số "15"); bộ lọc Trạng thái liệt kê đủ 19 mục. Đã hoàn trả
      data (status về 3) + cấu hình cột về ban đầu.

## Ghi chú
- KHÔNG backfill/sửa data — status 15 là trạng thái HỢP LỆ, chỉ thiếu map hiển thị.
- Liên quan memory `erp-ycxh-dieu-chuyen-noi-bo-status-set-nhap-ve` (bộ trạng thái nhập về type 6).
