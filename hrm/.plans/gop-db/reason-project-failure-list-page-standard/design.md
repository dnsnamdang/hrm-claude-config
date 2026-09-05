# Chuẩn hoá màn danh sách Nguyên nhân thất bại dự án (`/assign/reason_project_failure`)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
> Ngày: 05/09/2026

## 1. Mục tiêu

Đưa màn **Nguyên nhân thất bại dự án** về đúng chuẩn `.claude/skills/list-page/SKILL.md`,
giống 13 màn `assign/*` đã chuyển trước đó.

## 2. Phạm vi (chốt từ màn đầu tiên, giữ nguyên cho cả loạt)

- **FE: theo skill đầy đủ.**
- **BE: mức tối thiểu** — whitelist sort, tên người tạo/cập nhật, popup chọn trường xuất file.
- Hành động dòng: **Sửa + Xóa** là 2 nút chính, phần còn lại vào menu `⋮`.
- **KHÔNG làm lịch sử thay đổi / "Lịch sử"**.

## 3. Quyết định riêng của màn này

| Vấn đề | Quyết định |
| --- | --- |
| Cột định danh | Bảng `reason_project_failures` **không có cột mã** → cột định danh là **Tên nguyên nhân** (bấm vào tên = mở modal Xem, bỏ hành động "Xem") |
| Nút Khoá/Mở khoá nằm trong ô Trạng thái | Bản cũ nhét nút bấm ngay cạnh badge. Nay **badge không bấm được** (skill mục 3c-2), nút chuyển sang menu `⋮` của cột Hành động |
| Cột "Cập nhật" gộp ngày + người | Tách thành **Người cập nhật** và **Ngày cập nhật** riêng |
| Nút Sửa bị `disabled` khi Khoá | Đổi sang **ẩn** (`visible: is_can_edit`) theo skill mục 1 — không hiện rồi vô hiệu hoá |
| Điều kiện Xoá | **Giữ nguyên bản cũ**: luôn cho xoá. Không tự thêm `is_can_delete` (CLAUDE.md: điều kiện xoá phải hỏi user trước) |
| Sort | Trước đây whitelist chỉ có đúng 1 cột `updatedAt` — bấm sort Tên / Ngày tạo bị bỏ qua im lặng. Nay có đủ 3 |
| Ô tìm nhanh | `keyword` — nguyên nhân + mô tả + **người tạo** (EXISTS, không join) |
| Cấu hình cột | **Mặc định hiện HẾT cột** (quyết định của user, ngoại lệ có chủ ý so với skill mục 6) |
| Bề rộng cột | Theo 4 bậc mục 15b; bảng bật `fixed-layout` nên mọi cột khai đủ `width` + `minWidth` |

## 4. Lỗi hiệu năng có sẵn đã sửa (đo được)

`ReasonProjectFailureResource` trả `created_by_name` / `updated_by_name` bằng 2 accessor
`employee_create_name` / `employee_update_name` — mỗi accessor **nạp lười** quan hệ
`employee` + `employee_info` cho **từng dòng**.

Đo bằng `DB::getQueryLog()` trên endpoint danh sách với 5 dòng dữ liệu thật:
**43 query → 7 query**. Cách sửa: lấy tên bằng **subquery** trong `index()` (`creator_name` /
`updater_name`) và **bỏ 2 khoá cũ** — resource này chỉ phục vụ màn danh sách + file xuất,
đã kiểm tra không nơi nào khác đọc 2 khoá đó.

## 5. Thay đổi Backend

| File | Nội dung |
| --- | --- |
| `Modules/Assign/Services/ReasonProjectFailureService.php` | `SORTABLE_COLUMNS` (Tên / Ngày tạo / Ngày cập nhật) + tiebreak `id desc`; subquery `creator_name` / `updater_name`; ô tìm nhanh thêm **người tạo** (EXISTS) |
| `Modules/Assign/Transformers/ReasonProjectFailure/ReasonProjectFailureResource.php` | Thêm `status_text`, `creator_name`, `updater_name`; ngày giờ `d/m/Y H:i`; bỏ `created_by_name` / `updated_by_name` (nguồn N+1 ở mục 4) |
| `app/ExcelExport/ExportColumnRegistry.php` | Thêm nhóm cột `'reason_project_failures'` (7 cột) |
| `Modules/Assign/Http/Controllers/Api/V1/ReasonProjectFailureController.php` | `export()` chuyển sang `DynamicExport` + `ExportColumnRegistry`, `.xls` → `.xlsx` |

Không đổi schema, không thêm migration, không đụng dữ liệu.
`app/ExcelExport/ReasonProjectFailureExport.php` giờ **không còn nơi nào gọi** — để lại, chưa xoá
(giống các màn trước trong loạt).

## 6. Thay đổi Frontend

`pages/assign/reason_project_failure/index.vue`:

- `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (schema `filterFields` 5 ô), thêm
  `handleFilterChange` (bản cũ `v-model` thẳng vào `filters`, panel mới báo qua sự kiện)
- Thêm 3 mixin: `filterStateMixin` (màn này trước đây **chưa** nhớ bộ lọc),
  `columnCustomizationMixin`, `exportFieldsMixin`
- `tableColumns` tự khai → `allColumns` (mixin sinh `tableColumns`) + `ColumnCustomizationModal`
- Xuất Excel qua `ExportFieldsModal` + `downloadExcel()`
- Cột Trạng thái dùng `V2BaseBadge`; bỏ `renderStatus()` / `escapeHtml()`
- Cột Hành động dùng `V2BaseRowActions` thay 3 thẻ `<button>` tự dựng kèm style inline
- Toolbar theo `button-convention`: Tạo mới (primary) · Import (secondary warning) · Xuất Excel
  (secondary success, khoá bằng `:interactable`) · nút Cấu hình cột
- `filters` bỏ `page` / `per_page` và khoá `name` (không ô lọc nào ghi vào nó); `created` khôi phục
  bộ lọc + cờ `_restoringFilters`; đổi lọc thì về trang 1
- Lệnh ghi (xoá, khoá/mở khoá, xuất file) bọc `$safeLoadingStart/Finish`

## 7. Kiểm chứng đã chạy

- `php -l` 4 file BE — sạch; compile SFC + parse `<script>` — sạch
- Đối chiếu định danh template ↔ computed/methods/data bằng AST — không thiếu
- Cột bảng ↔ slot ↔ trường xuất FE ↔ registry BE — khớp 7/7; mọi cột đủ `width` + `minWidth`;
  3 cột sortable đều có trong `SORTABLE_COLUMNS`
- Modal id `modal-reason-project-failure` + `$refs...loadData()` / `resetModal()` — có thật trong
  `components/modal/reason-project-failure-modal.vue`
- Smoke test API trên **dữ liệu thật (5 dòng)**: index / sort Tên / sort Ngày tạo / sort Ngày cập
  nhật / keyword / status / người tạo + khoảng ngày / export → **200 cả 8**, số query 43 → 7

**Chưa kiểm chứng:** giao diện thực tế trên trình duyệt — user tự mở kiểm tra.
