# Màn Phân quyền người dùng (Chấm công) — phòng ban: bỏ mã công ty + lọc data cũ

**Người phụ trách:** @khoipv
**Ngày:** 18/09/2026
**Màn:** `/timesheet/setting/employees/{id}` — mục "Quản lý các phòng ban"

## Mục tiêu
1. Dropdown + chip phòng ban chỉ hiện tên phòng (bỏ `- Mã công ty`).
2. Không hiện phòng ban đã bị **xóa mềm** hoặc **khóa** (`status != 1`).
3. Dọn sạch dữ liệu rác trong `employee_manage_departments`.
4. Dropdown phòng ban dùng chung không để lọt phòng ban đã xóa mềm.

## Hiện trạng đã khảo sát (18/09/2026)
- `Modules\Timesheet\Entities\Department` **không dùng SoftDeletes** → `whereIn('id',...)->get()` lấy cả bản ghi đã xóa.
- 6 phòng ban gốc (Cung ứng, Dự án, Kế hoạch, Kế toán, Kho, Kỹ thuật) × 6 công ty = 36 bản ghi, **xóa mềm cùng đợt 07/11/2025**.
- `employee_manage_departments`: 51 dòng, **42 dòng rác**, 7 nhân viên: 20, 22, 29, 44, 46, 56, 74 (mỗi người 6/6 đều rác).
- Chỉ NV 46 (Nguyễn Thị Thanh Tường) bật `all_department = 1`; 6 người còn lại sau khi dọn sẽ **không quản lý phòng ban nào** — user đã chấp nhận.
- 1 phòng ban xóa mềm nhưng `status = 1` → vẫn lọt vào dropdown dùng chung.

## Task
### Phase 1 — Bỏ mã công ty (XONG)
- [x] BE `Modules/Timesheet/Transformers/EmployeeResource/DetailResource.php` — bỏ `foreach` nối `company->code`
- [x] FE `pages/timesheet/setting/employees/_id/index.vue` — computed `departments()` trả `name: val.name`
- [x] FE đổi multiselect `track-by="name"` → `track-by="id"` (6 phòng trùng tên khác công ty)

### Phase 2 — Lọc data cũ
- [x] `DetailResource.php` — thêm `whereNull('deleted_at')` + `where('status', 1)`

### Phase 3 — Dọn DB
- [x] Migration xóa các dòng `employee_manage_departments` trỏ tới phòng ban đã xóa mềm hoặc `status != 1`

### Phase 4 — Dropdown dùng chung
- [x] `app/Http/Controllers/Api/AuthNewController.php:163` — thêm `whereNull('deleted_at')`
      (API `user-profile`, dùng chung nhiều màn — user đã duyệt)

### Phase 5 — Kiểm thử
- [ ] `/timesheet/setting/employees/44`: mục quản lý phòng ban rỗng, không còn 6 phòng đã xóa
- [ ] Dropdown chỉ còn 21 phòng ban đang sống, hiện đúng tên phòng
- [ ] Chọn / bỏ chọn / Lưu → load lại đúng
- [x] Đếm lại `employee_manage_departments` còn 9 dòng (đã verify: 42 dòng rác đã xóa)
