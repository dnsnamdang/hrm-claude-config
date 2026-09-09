# Chuẩn hoá màn danh mục Loại giảm giá (`/assign/discount-types`)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`)
> Ngày: 05/09/2026

## 1. Mục tiêu

Đưa màn **Danh mục loại giảm giá** về đúng chuẩn `.claude/skills/list-page/SKILL.md`,
giống 14 màn `assign/*` đã chuyển trước đó.

## 2. Phạm vi (chốt từ màn đầu tiên, giữ nguyên cho cả loạt)

- **FE: theo skill đầy đủ.**
- **BE: mức tối thiểu** — whitelist sort, tên người tạo/cập nhật, popup chọn trường xuất file.
- Hành động dòng: **Sửa + Xóa** là 2 nút chính, phần còn lại vào menu `⋮`.
- **KHÔNG làm lịch sử thay đổi / "Lịch sử"**.

## 3. Quyết định riêng của màn này

| Vấn đề | Quyết định |
| --- | --- |
| Màn **chưa từng có Xuất Excel** | **Thêm mới**: route `GET /assign/discount_types/export` + `DiscountTypeController::export()` + nhóm cột trong registry. Đây là phần "popup chọn trường xuất file" trong phạm vi BE tối thiểu đã chốt cho cả loạt |
| Cột định danh | Danh mục dùng modal, không có màn chi tiết → bấm **Mã** mở modal Xem (mục 3a), bỏ hành động "Xem" |
| Cột Tên nhồi thêm dòng phụ | Bản cũ nhét "Người tạo - Ngày tạo" vào dòng phụ của ô Tên, và ngày + người cập nhật vào ô "Cập nhật" → tách thành 4 cột riêng |
| Nút Khoá/Mở khoá trong ô Trạng thái | Chuyển sang menu `⋮`; **badge không bấm được** (mục 3c-2). Điều kiện `v-if="item.status !== 3"` viết cứng ở FE → thay bằng cờ BE `is_can_lock_update` (Entity đã có sẵn `isCanLockUpdate()`, chỉ chưa lộ ra Resource) |
| Trạng thái | 3 giá trị, trong đó có **Chờ duyệt** → dùng `:color="item.status_color"` với mã màu BE trả, lấy từ hằng mới `DiscountType::STATUSES` theo bảng 9 màu chuẩn (mục 3c-1, 3c-2): Hoạt động `#16A34A` · Khóa `#DC2626` · Chờ duyệt `#D97706` |
| Sửa / Xoá không dùng được | **Giữ hiện nhưng vô hiệu hoá** kèm `disabledTitle` (`interactable: false` của `V2BaseRowActions`), không ẩn: đây là 2 hành động chính, người dùng cần biết *vì sao* — "đã khoá" / "đã được sử dụng, không thể xoá". Duyệt và Khoá/Mở khoá thì ẩn khi không áp dụng |
| Điều kiện Sửa / Xoá / Duyệt | **Giữ nguyên** cờ BE đang có (`is_can_edit`, `is_can_delete`, `is_can_approve`) — không tự đặt điều kiện mới |
| Cấu hình cột | **Mặc định hiện HẾT cột** (quyết định của user, ngoại lệ có chủ ý so với skill mục 6) |
| Bề rộng cột | Theo 4 bậc mục 15b; bảng bật `fixed-layout` nên mọi cột khai đủ `width` + `minWidth` |

## 4. Lỗi hiệu năng có sẵn đã sửa

`DiscountTypeResource` trả `created_by_name` / `updated_by_name` bằng accessor
`employee_create_name` / `employee_update_name` → **nạp lười** `employee` + `employee_info` cho
từng dòng, ở **cả `index` lẫn `getAll`** (dropdown loại giảm giá của màn báo giá).

Thay bằng **subquery** `creator_name` / `updater_name` trong `index()` và bỏ 2 khoá cũ. Đã kiểm tra
không FE nào đọc 2 khoá đó từ resource này — màn chi tiết (modal) dùng
`DetailDiscountTypeResource`, vẫn giữ nguyên.

## 5. Thay đổi Backend

| File | Nội dung |
| --- | --- |
| `Modules/Assign/Entities/DiscountType.php` | Thêm hằng `STATUSES` (chữ + mã màu 3 trạng thái) |
| `Modules/Assign/Services/DiscountTypeService.php` | `SORTABLE_COLUMNS` (thêm Ngày tạo, giữ khoá cũ `code`/`name` cho bộ lọc đã lưu) + tiebreak `id desc`; subquery `creator_name` / `updater_name`; ô tìm nhanh thêm **người tạo** (EXISTS) |
| `Modules/Assign/Transformers/DiscountType/DiscountTypeResource.php` | Thêm `status_text` + `status_color` + `is_can_lock_update`; ngày `d/m/Y H:i`; bỏ `created_by_name` / `updated_by_name` (mục 4); giữ `status_label` cho tương thích |
| `app/ExcelExport/ExportColumnRegistry.php` | Thêm nhóm cột `'discount_types'` (7 cột) |
| `Modules/Assign/Http/Controllers/Api/V1/DiscountTypeController.php` | **Thêm mới** `export()` dùng `DynamicExport` + registry |
| `Modules/Assign/Routes/api.php` | **Thêm mới** route `GET /export`, đặt **trước** route wildcard `/{discountType}` (không thì `export` bị hiểu là id), middleware `checkPermission:Quản lý danh mục loại giảm giá` |

Không đổi schema, không thêm migration, không đụng dữ liệu.

## 6. Thay đổi Frontend

`pages/assign/discount-types/index.vue`:

- `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (schema `filterFields` 4 ô), thêm
  `handleFilterChange` (bản cũ `v-model` thẳng vào `filters`, panel mới báo qua sự kiện)
- Thêm `columnCustomizationMixin` + `exportFieldsMixin` (đã có sẵn `filterStateMixin`)
- `tableColumns` tự khai → `allColumns` (mixin sinh `tableColumns`) + `ColumnCustomizationModal`
- **Thêm nút Xuất Excel** (màn này trước đây không có) qua `ExportFieldsModal` + `downloadExcel()`
- Cột Trạng thái dùng `V2BaseBadge` `:color`; bỏ `renderStatus()` / `escapeHtml()`
- Cột Hành động dùng `V2BaseRowActions` thay 4 thẻ `<button>` style inline
- Toolbar theo `button-convention`: Xóa nhiều (primary danger) · Bỏ chọn (tertiary) · Tạo mới ·
  Xuất Excel (secondary success) · Cấu hình cột
- `filters` bỏ `page` / `per_page`; `mounted` → `created` (request danh sách bắn sớm hơn 1 nhịp,
  skill mục 8) + cờ `_restoringFilters`
- Lệnh ghi (xoá, xoá nhiều, khoá/mở khoá, duyệt, xuất file) bọc `$safeLoadingStart/Finish`

## 7. Kiểm chứng đã chạy

- `php -l` 6 file BE — sạch; compile SFC + parse `<script>` — sạch
- Đối chiếu định danh template ↔ computed/methods/data bằng AST — không thiếu
- Cột bảng ↔ slot ↔ trường xuất FE ↔ registry BE — khớp 7/7; mọi cột đủ `width` + `minWidth`;
  4 cột sortable đều có trong `SORTABLE_COLUMNS`
- Modal id `modal-discount-type` + `$refs...loadData()` / `resetModal()` — có thật trong
  `components/modal/discount-type-modal.vue`; `V2BaseBadge` có prop `color`
- Smoke test API: DB local chỉ có **1 dòng** (status = 1) → thêm 2 dòng tạm (Khóa + Chờ duyệt)
  trong **transaction rồi rollback** để phủ đủ 3 trạng thái. 9 request (index / sort Mã / sort Tên /
  sort Ngày tạo / keyword / status=3 / người tạo + khoảng ngày tạo / **export** / getAll)
  → **200 cả 9**; `status_color` trả đúng `#16A34A` · `#D97706`; DB sau test vẫn 1 dòng

**Chưa kiểm chứng:** giao diện thực tế trên trình duyệt — user tự mở kiểm tra.
