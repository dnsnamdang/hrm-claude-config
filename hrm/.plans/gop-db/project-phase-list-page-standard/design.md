# Chuẩn hoá màn Danh sách giai đoạn dự án theo skill `list-page`

- **Người phụ trách:** @khoipv
- **Nhánh:** `gop_db` (cả `hrm-api` + `hrm-client`)
- **Màn:** `/assign/project_phase` — `hrm-client/pages/assign/project_phase/index.vue`
- **Ngày:** 2026-09-05 · Làm theo khuôn [industry-group-list-page-standard](../industry-group-list-page-standard/design.md)
  và [application-list-page-standard](../application-list-page-standard/design.md) (user chỉ định 2 màn này làm mẫu)

## Mục tiêu

Đưa màn danh mục Giai đoạn dự án về đúng `.claude/skills/list-page/SKILL.md`. Đây là **màn danh mục
dùng modal** (`components/modal/project_phase_modal.vue`, không có route chi tiết) nên áp mục 3a.

## Hiện trạng lệch chuẩn

| Điểm | Trước | Sau |
| --- | --- | --- |
| Panel lọc | `V2BaseFilterPanel` + `title`/`subtitle` riêng, 5 ô hard-code trong slot | `V2BaseSmartFilterPanel` + schema `filterFields` 8 ô (thêm Mã / Tên / Mức độ ưu tiên) |
| Ô lọc gõ tay | deep watcher bắn API mỗi ký tự | `textFilterKeys()` — chờ Enter / nút Tìm kiếm |
| Cột định danh | 1 cột gộp `Mã giai đoạn - Tên giai đoạn`, chữ ĐẬM, kèm dòng phụ "Đã gán N dự án" | Tách `Mã giai đoạn` (button `.v2-cell-link` mở modal Xem, sticky + locked) / `Tên giai đoạn` |
| Hành động | 3 nút icon Xem / Sửa / Xóa, disable + tooltip | Cột "Hành động" cuối, `V2BaseRowActions`, bỏ "Xem", ẩn thay vì disable |
| Nút Khóa/Mở khóa | Nằm TRONG ô Trạng thái | Chuyển sang menu `⋮` của cột Hành động |
| Trạng thái | `v-html` + `status-pill` + `renderStatus()` tự dựng | `V2BaseBadge` `variant` brand/required, chữ lấy từ `status_text` của BE |
| Người tạo / Ngày tạo | Có cột nhưng lấy `created_by_name` (ghép "mã - tên"); "Cập nhật" gộp ngày + người | 4 cột riêng: Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật, tên KHÔNG kèm mã |
| Định dạng ngày | `d/m/Y H:i:s` (có giây) | `d/m/Y H:i` |
| Cấu hình cột | không có | `columnCustomizationMixin` + `ColumnCustomizationModal` (`columnScreenKey = 'project_phases'`) |
| Nhớ bộ lọc | không có | `filterStateMixin` (`assign_project_phases`) |
| Xuất Excel | tải thẳng cả bảng ra `.xls`, `$nuxt.$loading` | Popup "Chọn trường xuất file" + `DynamicExport` ra `.xlsx`, `$safeLoading` |
| Sort | BE whitelist chỉ có `updated_at` | Mã / Tên / Ngày tạo / Ngày cập nhật |
| Ô tìm nhanh | chỉ mã + tên | thêm **người tạo** (EXISTS, không join) |
| Bề rộng cột | phần lớn cột không khai `width` | `fixed-layout` + `width`/`minWidth` đủ 12 cột, cột chữ dài `clamp-2` |
| Chọn nhiều dòng | code checkbox + xoá hàng loạt để lại nhưng toolbar đã comment | Gỡ hẳn (chuẩn cột Hành động không có xoá hàng loạt) |

## Quyết định

- **MẶC ĐỊNH HIỆN HẾT CỘT** — theo user chốt 2026-09-05 ở loạt màn trước (ngoại lệ có chủ ý so với
  `list-page` mục 6). Ai thấy rộng thì tự tắt bớt ở popup Cấu hình cột, lưu theo từng người.
- **Lịch sử thay đổi: KHÔNG làm** — giống 2 màn mẫu (user chốt 2026-09-05). Module `Assign` chưa
  có `LogsCatalogHistory`; muốn làm thì mở việc riêng.
- **Cột "Số dự án đã gán" để CHỮ THƯỜNG, không làm link** — màn `/assign/prospective-projects`
  không đọc query string để nạp bộ lọc (`mounted()` chỉ đọc localStorage), gắn `?project_phase_id=`
  sẽ ra link chết.
- **Cột định danh = Mã giai đoạn**: kiểm dữ liệu thật `select count(*), sum(code is null or code='')
  from project_phases` → 8/0, không có bản ghi thiếu mã.
- **Nút Xuất Excel không gate quyền** (skill mục 3b-5) → nới middleware route `export` từ
  `Quản lý danh mục giai đoạn dự án` thành `Quản lý…|Xem danh mục giai đoạn dự án`, nếu không người
  chỉ có quyền xem bấm nút sẽ dính 403 câm.

## Đụng vào những file nào

**BE (`hrm-api`)**
- `Modules/Assign/Services/ProjectPhaseService.php` — `SORTABLE_COLUMNS`, subquery người tạo/cập nhật,
  keyword tìm theo người tạo, thêm lọc `code` / `name` / `priority_level_id`, sort theo `sort_by`+`sort_desc`
- `Modules/Assign/Transformers/ProjectPhaseResource/ProjectPhaseResource.php` — `status_text`,
  `creator_name`, `updater_name`, ngày `d/m/Y H:i`, `is_can_lock_update` / `is_can_unlock_update`,
  `is_can_delete` tính từ subquery đếm (bỏ 1 query/dòng)
- `Modules/Assign/Transformers/ProjectPhaseResource/DetailProjectPhaseResource.php` — bỏ giây
- `Modules/Assign/Http/Controllers/Api/V1/ProjectPhaseController.php` — `export()` dùng `DynamicExport`
- `app/ExcelExport/ExportColumnRegistry.php` — thêm khối `'project_phases'` (10 cột)
- `Modules/Assign/Routes/api.php` — nới quyền route `export`

**FE (`hrm-client`)**
- `pages/assign/project_phase/index.vue` — viết lại theo khuôn `industry-groups/index.vue`

Không đụng `components/modal/project_phase_modal.vue` (modal Thêm/Sửa/Xem giữ nguyên) và không đụng
luồng Import.

## Kiểm chứng

- Compile FE (`vue-template-compiler` + babel) + dò identifier template bằng AST → chỉ còn `item`,
  `index` (biến slot-scope, đúng)
- Smoke test API qua HTTP kernel: `index` (200) · `sort_by=phaseCode` · `keyword` · `export` (200,
  content-type xlsx). Đọc lại file xuất: đúng 5 cột đã tick, đúng thứ tự, có tiêu đề bảng
- Đối chiếu khoá cột bảng ↔ `exportFields` ↔ registry BE: 10 = 10, không lệch
- **Chưa kiểm chứng:** giao diện thật trên trình duyệt (user tự mở)
