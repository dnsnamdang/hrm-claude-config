# Chuẩn hoá màn Danh sách yêu cầu làm giải pháp theo skill `list-page`

- **Người phụ trách**: @khoipv · **Nhánh**: `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn hình**: `/assign/request-solution`
- **Spec chi tiết**: `docs/superpowers/specs/gop-db/2026-09-07-request-solution-list-page-standard-design.md`
- **Tiếp nối**: loạt 15 màn `assign-list-page-standard` · `project-phase` · `prospective-project` ·
  `product-project` · `pricing-request` · `contract`

## Phạm vi

1. Bộ lọc → `V2BaseSmartFilterPanel` + schema `filterFields` (8 mục / 10 ô).
2. Tách cột gộp "Mã • Tên yêu cầu" (chứa mã + tên + 2 dòng phụ + 4 icon thao tác) thành
   **Mã yêu cầu** (link) + **Tên yêu cầu**; **cột Hành động ở cuối bảng** (`V2BaseRowActions`):
   Sửa · Xóa · Làm giải pháp · Hủy yêu cầu. Bỏ hành động "Xem".
3. Bảng **22 cột**, bật `fixed-layout`, khai đủ `width` = `minWidth`; thêm Người tạo · Ngày tạo ·
   Người cập nhật · Ngày cập nhật.
4. `columnCustomizationMixin` + popup **Chọn trường xuất file**; export `.xls` → `.xlsx` cột động.
5. BE: whitelist sắp xếp + chốt `id desc`; 5 mã màu trạng thái quy về bảng 9 mã chuẩn; cờ
   `is_can_edit` / `is_can_delete`; **trả dữ liệu cho 2 cột vốn rỗng** (Mã GP, PM làm GP).

## 4 lỗi CÓ SẴN sửa kèm

| Lỗi | Hậu quả |
| --- | --- |
| 2 cột **"Mã GP"** và **"PM làm GP"** in **cứng dấu gạch** trong template (đoạn code thật bị comment) | 2 cột luôn trống với mọi dòng — máy chủ chưa bao giờ trả 2 trường này, dù `solutions.request_solution_id` có sẵn |
| `handleConfirmDeleteRequest()` chặn xoá bằng `item.solution_code` — khoá Resource **không trả về** | Guard "yêu cầu đã có mã GP thì không xoá" **chưa bao giờ chạy** |
| Cột **Người tạo** dùng accessor `employee_create_name` của `BaseModel` → ghép `"mã - tên"` | Hiện `11510109 - Nguyễn Minh Hoàng`, trái skill mục 6 (chỉ TÊN) |
| `Helper::formatDateTime()` gọi không truyền format | Ngày tạo/cập nhật hiện **cả giây** (`27/07/2026 10:29:17`) |

Kèm 2 lỗi hiệu năng và 2 lỗi gọi API thừa — xem plan.

## Quyết định đã chốt

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã yêu cầu**, link `nuxt-link` vào `/assign/request-solution/{id}` |
| Điều kiện Sửa / Xóa | Cờ BE `is_can_edit` / `is_can_delete` — Sửa: Nháp hoặc Yêu cầu bổ sung **và là người tạo**; Xóa: Nháp, là người tạo, **và chưa sinh giải pháp** |
| "Hủy yêu cầu" | Giữ ở danh sách (mở popup nhập lý do tại chỗ, cờ `is_can_cancel` vốn có) |
| Mặc định cột hiển thị | **Hiện HẾT** (theo chốt của loạt màn trước) |
| Hành động "Lịch sử" | **Chưa làm** — module Assign chưa có `LogsCatalogHistory` |

## File chính

- BE: `Modules/Assign/Entities/RequestSolution.php` ·
  `Modules/Assign/Services/RequestSolutionService.php` ·
  `Modules/Assign/Transformers/RequestSolutionResource/RequestSolutionResource.php` ·
  `Modules/Assign/Http/Controllers/Api/V1/RequestSolutionController.php` ·
  `app/ExcelExport/ExportColumnRegistry.php`
- FE: `pages/assign/request-solution/index.vue`

Không migration, không quyền mới.
