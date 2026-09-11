# Chuẩn hoá màn Danh sách hạng mục dự án theo skill `list-page`

- **Người phụ trách**: @khoipv · **Nhánh**: `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn hình**: `/assign/solution-modules`
- **Spec chi tiết**: `docs/superpowers/specs/gop-db/2026-09-07-solution-module-list-page-standard-design.md`
- **Tiếp nối**: loạt 15 màn `assign-list-page-standard` · `project-phase` · `prospective-project` ·
  `product-project` · `pricing-request` · `contract` · `request-solution`

## Phạm vi

1. Bộ lọc → `V2BaseSmartFilterPanel` + schema `filterFields` (6 mục / 8 ô).
2. Tách cột gộp "Hạng mục" (mã + tên + 3 icon thao tác) thành **Mã hạng mục** (link vào màn quản lý)
   + **Tên hạng mục**; **cột Hành động ở cuối bảng** (`V2BaseRowActions`): Sửa · Lưu và duyệt.
3. Bảng **13 cột**, bật `fixed-layout`, khai đủ `width` = `minWidth`; thêm 4 cột Người tạo ·
   Ngày tạo · Người cập nhật · Ngày cập nhật.
4. `columnCustomizationMixin` (màn **chưa từng có** cấu hình cột) + **chức năng Xuất Excel mới**
   (màn **chưa từng có** xuất file) qua popup Chọn trường + `DynamicExport`.
5. BE: whitelist sắp xếp + chốt `id desc`; 2 mã màu trạng thái quy về bảng 9 mã chuẩn;
   Resource trả `creator_name` / `updater_name` / `updated_at`.

## Điểm đáng chú ý

- **Danh sách phải chờ một request 10.000 dòng mới bắt đầu tải.** `mounted()` bản cũ
  `await loadFilterOptions()` trước `loadData()`, mà hàm đó gọi
  `assign/solutions/getAll?per_page=10000` — chỉ để đổ options cho MỘT ô lọc nằm trong panel nâng
  cao đang thu gọn. Nay: `loadData()` chạy đầu tiên, options hoãn tới khi user mở panel, và hạ
  `per_page` 10.000 → 1.000.
- **Bấm sort gọi API 2 lần**: `handleSort` vừa tự gọi `loadData()` vừa để deep watcher bắn thêm
  (sort_field nằm trong `filters`). "Làm mới" cũng vậy.
- **Không còn hành động "Quản lý"** trên dòng: cột Mã hạng mục đã là link vào đúng màn quản lý
  (skill mục 1 — bỏ hành động "Xem", cột định danh là lối vào). Hệ quả: dòng nào người dùng không
  có quyền duyệt thì cột Hành động trống — đúng quy tắc "không dùng được thì ẩn hẳn".

## Quyết định đã chốt

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã hạng mục**, link vào `/assign/solution-modules/{id}/manager` |
| Hành động dòng | Sửa · Lưu và duyệt (cả 2 gate bằng cờ BE `is_can_approve` vốn có) |
| Mặc định cột hiển thị | **Hiện HẾT** (theo chốt của loạt màn trước) |
| Hành động "Lịch sử" | **Chưa làm** — module Assign chưa có `LogsCatalogHistory` |

## File chính

- BE: `Modules/Assign/Entities/SolutionModule.php` ·
  `Modules/Assign/Services/SolutionModuleService.php` ·
  `Modules/Assign/Transformers/SolutionModuleResource/SolutionModuleListResource.php` ·
  `Modules/Assign/Http/Controllers/Api/V1/SolutionModuleController.php` · `Modules/Assign/Routes/api.php` ·
  `app/ExcelExport/ExportColumnRegistry.php`
- FE: `pages/assign/solution-modules/index.vue`

Không migration, không quyền mới.
