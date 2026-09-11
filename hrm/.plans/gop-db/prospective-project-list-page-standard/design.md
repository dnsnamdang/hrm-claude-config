# Chuẩn hoá màn Danh sách dự án tiền khả thi theo skill `list-page`

- **Người phụ trách**: @khoipv · **Nhánh**: `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn hình**: `/assign/prospective-projects` (Quản lý dự án TKT → Dự án)
- **Spec chi tiết**: `docs/superpowers/specs/gop-db/2026-09-07-prospective-project-list-page-standard-design.md`
- **Tiếp nối**: loạt 15 màn `assign-list-page-standard` + `project-phase-list-page-standard` (đều đã xong 2026-09-05)

## Mục tiêu

Đưa màn danh sách dự án tiền khả thi về đúng khuôn `list-page` như 16 màn đã làm trước, **giữ nguyên
2 đặc thù của màn**: cây dự án cha – con (mở rộng ở cột STT) và toàn bộ bộ lọc hiện có.

## Phạm vi

### KHÔNG đụng tới (user chốt 2026-09-07)

- **Bộ lọc giữ NGUYÊN**: vẫn là `V2BaseFilterPanel` cũ, đủ các ô đang có, không chuyển sang
  `V2BaseSmartFilterPanel`, không đổi placeholder/nhãn, không đổi trường tìm nhanh ở BE.
- Cây cha – con (`treeTableData`, nút mở rộng ở ô STT, tô nền dòng cha/con) giữ nguyên hành vi.

### Làm

1. **Cột định danh**: tách cột gộp `projectInfo` thành **Mã dự án** (link `.v2-cell-link` vào
   `/{id}/manager`, sticky + locked, sortable) và **Tên dự án TKT** (chữ thường, `clamp-2`).
2. **Tách 5 dòng phụ** đang nhồi trong ô Tên thành cột riêng: NV KD phụ trách · Phòng ban ·
   Bộ phận · Ngày tạo · Ngày cập nhật; thêm **Người tạo** / **Người cập nhật** (BE trả về).
3. **Cột Hành động ở CUỐI bảng** dùng `V2BaseRowActions`: 2 nút chính Sửa + Xóa, phần còn lại
   (Tạo giải pháp, Tạo yêu cầu làm giải pháp) vào menu `⋮`. **Bỏ hành động "Xem"** (Mã là link).
   Dãy icon nhét dưới tên dự án bị gỡ.
4. **Trạng thái**: `V2BaseBadge` + `:color="item.status_color"` do BE trả (9 mã màu chuẩn, mục 3c-2),
   cột dời về ngay trước Hành động.
5. **Cấu hình cột** chuyển sang `columnCustomizationMixin`; **Xuất Excel** chuyển sang popup
   "Chọn trường xuất file" (`exportFieldsMixin` + `ExportColumnRegistry` + `DynamicExport`, `.xls` → `.xlsx`).
6. **Bề rộng cột theo mục 15b**: bật `fixed-layout`, khai đủ `width` + `minWidth` cho mọi cột,
   ô chữ dài `text-wrap clamp-2` + `:title`, ô tham chiếu ghép `MÃ - Tên` cùng 1 dòng.
7. Bỏ sạch `'—'` trong ô trống; bỏ `font-weight-bold` trong ô bảng.
8. **BE**: whitelist `SORTABLE_COLUMNS` (đang `orderBy($request->sort_field)` trần), subquery
   người tạo/người cập nhật, `status_color`, định dạng ngày `d/m/Y H:i`, gỡ N+1 trong Resource.

## Quyết định đã chốt (2026-09-07)

| Việc | Chốt |
| --- | --- |
| Cột định danh | **Mã dự án** là link (giống 16 màn trước), Tên là cột chữ thường |
| 5 dòng phụ trong ô Tên | **Tách hết** thành cột riêng, ẩn/hiện được ở popup Cấu hình cột |
| Bộ lọc | **Giữ nguyên**, không chuẩn hoá đợt này |
| Mặc định cột hiển thị | **Hiện HẾT** (ngoại lệ có chủ ý so với mục 6, theo chốt của loạt màn trước) |
| Hành động "Lịch sử" | **Chưa làm** — module Assign chưa có `LogsCatalogHistory` (giống 16 màn trước) |

⚠️ **Hệ quả đã biết của việc chọn Mã làm cột định danh**: mã dự án chỉ sinh khi phiếu rời trạng thái
"Đang tạo" (`ProspectiveProjectService` dòng ~363), nên **11/146 dự án nháp có ô Mã trống** → không
bấm được vào chi tiết từ cột đó; vào bằng nút **Sửa** ở cột Hành động (đúng luồng của bản nháp).

## File chính

- BE: `Modules/Assign/Services/ProspectiveProjectService.php` ·
  `Modules/Assign/Transformers/ProspectiveProjectResource/ProspectiveProjectResource.php` ·
  `Modules/Assign/Http/Controllers/Api/V1/ProspectiveProjectController.php` ·
  `Modules/Assign/Entities/ProspectiveProject.php` · `app/ExcelExport/ExportColumnRegistry.php`
- FE: `hrm-client/pages/assign/prospective-projects/index.vue`

Không migration, không quyền mới.
