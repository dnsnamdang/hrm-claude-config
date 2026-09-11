# Chuẩn hoá màn danh sách Mẫu phiếu thu thập thông tin (`/assign/form-templates`)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
> Ngày: 05/09/2026

## 1. Mục tiêu

Đưa màn **Mẫu phiếu thu thập thông tin** về đúng chuẩn `.claude/skills/list-page/SKILL.md`,
giống 12 màn `assign/*` đã chuyển trước đó.

## 2. Phạm vi (chốt từ màn đầu tiên, giữ nguyên cho cả loạt)

- **FE: theo skill đầy đủ.**
- **BE: mức tối thiểu** — whitelist sort, tên người tạo/cập nhật, popup chọn trường xuất file.
- Hành động dòng: **Sửa + Xóa** là 2 nút chính, phần còn lại vào menu `⋮`.
- **KHÔNG làm lịch sử thay đổi / "Lịch sử"**.

## 3. Quyết định riêng của màn này

| Vấn đề | Quyết định |
| --- | --- |
| Cột "Mẫu phiếu" nhồi 4 thông tin | Bản cũ gộp **Tên + Mã + Người tạo + Ngày tạo + cả cụm nút thao tác** vào 1 ô `V2BaseTitleSubInfo`. Nay tách thành cột riêng theo mục 3: **Mã** là link vào chi tiết, **Tên** chữ thường, Người tạo / Ngày tạo là cột độc lập |
| Màn có chi tiết | Có route `/assign/form-templates/{id}` → cột Mã dùng `nuxt-link` (mục 3), **bỏ hành động "Xem mẫu"** |
| Trạng thái | 3 giá trị cố định (Nháp / Hoạt động / Khoá) → `V2BaseBadge` với `variant` (`muted` / `brand` / `required`) theo mục 3c-1; BE trả sẵn `status_text` từ hằng `FormTemplate::STATUS_NAMES` |
| Điều kiện hiện hành động | **Giữ nguyên bản cũ**: Sửa khi chưa Khoá · Xoá khi còn Nháp · Khoá/Mở khoá khi đã qua Nháp. Khác duy nhất: không dùng được thì **ẩn**, thay vì hiện rồi báo toast khi bấm |
| Cấu hình cột | **Mặc định hiện HẾT cột** (quyết định của user, ngoại lệ có chủ ý so với skill mục 6) |
| Bề rộng cột | Theo 4 bậc mục 15b; bảng bật `fixed-layout` nên mọi cột khai đủ `width` + `minWidth` |
| Chọn nhiều dòng | **Không thêm** — màn này chưa từng có xoá hàng loạt, thêm vào là mở rộng phạm vi |

## 4. Hai lỗi hiệu năng CÓ SẴN đã sửa (đo được)

`FormTemplatesResource` là resource của **màn danh sách** nhưng mỗi dòng lại tự nạp lười 2 quan hệ:

| Chỗ hỏng | Vì sao | Cách sửa |
| --- | --- | --- |
| `'sections' => $this->whenLoaded('sections') ? ... : []` | Khi chưa nạp quan hệ, `whenLoaded()` trả về **đối tượng** `MissingValue` — mà object thì **luôn truthy** → nhánh `true` vẫn chạy và `$this->sections` nạp lười cả cây section/group/question/option | Đổi sang `$this->relationLoaded('sections')` |
| `'questions_count' => $this->questions->count()` | Nạp lười **toàn bộ** câu hỏi của từng dòng chỉ để đếm, dù Service đã `withCount('questions')` | Dùng thẳng `$this->questions_count` |

Đo bằng `DB::getQueryLog()` trên 1 dòng: **4 query/dòng → 0**. Sau khi sửa, số query của endpoint
danh sách là **hằng số 7** bất kể bao nhiêu dòng.

Cùng nhóm: `created_by` / `updated_by` trước lấy qua quan hệ `employee_create->info->fullname`
(thêm query/dòng) → nay lấy bằng **subquery** trong `index()`.

## 5. Thay đổi Backend

| File | Nội dung |
| --- | --- |
| `Modules/Assign/Services/FormTemplateService.php` | `SORTABLE_COLUMNS` (thêm Mã + Ngày tạo, trước đây bấm sort 2 cột này bị bỏ qua im lặng) + tiebreak `id desc`; subquery `creator_name` / `updater_name`; ô tìm nhanh thêm **người tạo** (EXISTS) và dùng `escapeLikeKeyword` |
| `Modules/Assign/Transformers/FormTemplatesResource/FormTemplatesResource.php` | Sửa 2 lỗi N+1 ở mục 4; thêm `status_text`, `creator_name`, `updater_name`; ngày giờ `d/m/Y H:i` |
| `Modules/Assign/Entities/FormTemplate.php` | Thêm hằng `STATUS_NAMES` (Nháp / Hoạt động / Khoá) |
| `app/ExcelExport/ExportColumnRegistry.php` | Thêm nhóm cột `'form_templates'` (9 cột) |
| `Modules/Assign/Http/Controllers/Api/V1/FormTemplateController.php` | `export()` chuyển sang `DynamicExport` + `ExportColumnRegistry`, file `.xls` → `.xlsx` |

Không đổi schema, không thêm migration, không đụng dữ liệu.
`app/ExcelExport/FormTemplatesExport.php` + `resources/views/exports/form_templates.blade.php`
giờ **không còn nơi nào gọi** — để lại, chưa xoá (giống các màn trước trong loạt).

## 6. Thay đổi Frontend

`pages/assign/form-templates/index.vue`:

- `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (schema `filterFields` 6 ô, `table="form_templates"`)
- Thêm 2 mixin mới: `columnCustomizationMixin`, `exportFieldsMixin` (đã có sẵn `filterStateMixin`)
- `tableColumns` tự khai → `allColumns` (mixin sinh `tableColumns`) + `ColumnCustomizationModal`
- Xuất Excel qua `ExportFieldsModal` + `downloadExcel()`, thay khối tải file tự viết
- Cột Trạng thái dùng `V2BaseBadge`; bỏ `renderTemplateStatus()` / `escapeHtml()`
- Cột Hành động riêng, dùng `V2BaseRowActions` (bỏ cụm nút nhét trong ô "Mẫu phiếu")
- Toolbar theo `button-convention`: Tạo mẫu phiếu (primary) · Xuất Excel (secondary success, khoá
  bằng `:interactable`) · nút Cấu hình cột
- Gộp `mounted` vào `created` (request danh sách bắn sớm hơn 1 nhịp — skill mục 8), thêm cờ
  `_restoringFilters` để không gọi API 2 lần, đổi lọc thì về trang 1
- Lệnh ghi (xoá, khoá/mở khoá, xuất file) bọc `$safeLoadingStart/Finish`
- Bỏ `console.log` sót lại trong `confirmToggleLock`

Màn xem trước bản in (`FormTemplatePrintSheet` + `b-modal`) giữ nguyên.

## 7. Kiểm chứng đã chạy

- Compile SFC + parse `<script>` — sạch; `php -l` 5 file BE — sạch
- Đối chiếu định danh template ↔ computed/methods/data bằng AST — không thiếu
- Cột bảng ↔ slot ↔ trường xuất FE ↔ registry BE — khớp 9/9; mọi cột đủ `width` + `minWidth`;
  5 cột sortable đều có trong `SORTABLE_COLUMNS`
- Smoke test API: bảng `form_templates` **local đang rỗng** → tạo 3 mẫu phiếu + 2 câu hỏi trong
  **transaction rồi rollback**. 8 request (index / sort Mã / sort Số câu hỏi / sort Ngày tạo /
  keyword / status / người tạo + khoảng ngày / export) → **200 cả 8**, `questions_count` đúng,
  `sections` rỗng (không còn nạp lười), DB sau test vẫn 0 dòng.

**Chưa kiểm chứng:** giao diện thực tế trên trình duyệt — user tự mở kiểm tra.
