# Chuẩn hoá màn danh sách Vai trò dự án (`/assign/project_role`)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
> Ngày: 05/09/2026

## 1. Mục tiêu

Đưa màn danh sách **Vai trò dự án** về đúng chuẩn `.claude/skills/list-page/SKILL.md`, giống 11 màn
`assign/*` đã chuyển trước đó.

## 2. Phạm vi (chốt từ màn đầu tiên, giữ nguyên cho cả loạt)

- **FE: theo skill đầy đủ.**
- **BE: mức tối thiểu** — whitelist sort, tên người tạo/cập nhật, popup chọn trường xuất file.
- Hành động dòng: **Sửa + Xóa** là 2 nút chính, phần còn lại vào menu `⋮`.
- **KHÔNG làm lịch sử thay đổi / "Lịch sử"** cho màn này.

## 3. Quyết định riêng của màn này

| Vấn đề | Quyết định |
| --- | --- |
| Cột định danh | Bảng `project_roles` **không có cột mã** → cột định danh là **Tên vai trò dự án** (bấm vào tên = mở modal Xem) |
| Cột "Dùng ở dự án" (`project_id`) | **Bỏ hẳn** — `ProjectRolesResource` chưa bao giờ trả khoá này nên cột luôn trống |
| Sort | Trước đây `index()` nhận `sort_field` nhưng **luôn** sắp theo `updated_at`. Nay có whitelist thật: Tên / Ngày tạo / Ngày cập nhật |
| Ô tìm nhanh | `keyword` — tìm theo **tên vai trò + tên người tạo** (EXISTS, không join, để không phình câu COUNT) |
| Trạng thái | 2 giá trị cố định (Hoạt động / Khóa) → `V2BaseBadge` với `variant`, BE trả sẵn `status_text` |
| Khóa / Mở khóa | Không dùng được thì **ẩn** khỏi menu; lý do (còn vai trò con hoạt động / vai trò cha đang khóa) hiện ở tooltip badge Trạng thái |
| Cấu hình cột | **Mặc định hiện HẾT cột** (quyết định của user, ngoại lệ có chủ ý so với skill mục 6) |
| Bề rộng cột | Theo 4 bậc mục 15b; bảng bật `fixed-layout` nên mọi cột khai đủ `width` + `minWidth` |

## 4. Thay đổi Backend

| File | Nội dung |
| --- | --- |
| `Modules/Assign/Services/ProjectRolesService.php` | `SORTABLE_COLUMNS` (whitelist thật) + tiebreak `id desc`; subquery `creator_name` / `updater_name`; lọc `keyword` theo tên + người tạo |
| `Modules/Assign/Transformers/ProjectRolesResource/ProjectRolesResource.php` | Thêm `status_text`, `creator_name`, `updater_name`; ngày giờ `d/m/Y H:i` |
| `app/ExcelExport/ExportColumnRegistry.php` | Thêm nhóm cột `'project_roles'` (9 cột) |
| `Modules/Assign/Http/Controllers/Api/V1/ProjectRolesController.php` | `export()` chuyển sang `DynamicExport` + `ExportColumnRegistry`, file `.xlsx` |

Không đổi schema, không thêm migration, không đụng dữ liệu.

## 5. Thay đổi Frontend

`pages/assign/project_role/index.vue`:

- `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (schema `filterFields`, `table="project_roles"`)
- Thêm 3 mixin: `filterStateMixin`, `columnCustomizationMixin`, `exportFieldsMixin`
- `tableColumns` (tự khai) → `allColumns` (mixin sinh `tableColumns`) + modal `ColumnCustomizationModal`
- Xuất Excel qua `ExportFieldsModal` + `downloadExcel()`, thay cho khối tải file tự viết
- Cột Trạng thái dùng `V2BaseBadge`; bỏ `renderStatus()` / `escapeHtml()`
- Cột Hành động dùng `V2BaseRowActions` (`getRowActions` / `handleRowAction`)
- Toolbar theo `button-convention`: Tạo mới (primary) · Import (secondary warning) · Xuất Excel
  (secondary success, khoá bằng `:interactable`) · nút Cấu hình cột
- `filters` không còn giữ `page` / `per_page`; watcher có cờ `_restoringFilters` để không gọi API 2 lần
- Lệnh ghi (xóa, xóa nhiều, khóa/mở khóa, xuất file) bọc `$safeLoadingStart/Finish`

## 6. Kiểm chứng đã chạy

- Compile SFC (`vue-template-compiler`) + parse `<script>` (`@babel/parser`) — sạch
- Đối chiếu định danh template ↔ computed/methods/data bằng AST — không thiếu
- Cột bảng ↔ trường xuất FE ↔ registry BE — khớp 9/9; mọi cột có đủ `width` + `minWidth`
- Smoke test API (HTTP kernel + JWT thật): index / sort `roleName` / `keyword` / `status` /
  khoảng ngày cập nhật / export → **200** cả 6 (dữ liệu: 9 vai trò, đều `status = 1`)

**Chưa kiểm chứng:** giao diện thực tế trên trình duyệt — user tự mở kiểm tra.
