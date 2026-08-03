# Cấp dịch vụ bảo dưỡng + Danh mục ghi chú kiểm tra bảo dưỡng — chuyển ERP sang HRM

> Phụ trách: @junfoke · Bắt đầu: 2026-08-03

## Mục tiêu

Chuyển 2 danh mục dịch vụ của ERP sang HRM, đặt ở phân hệ **CSKH** (`customer-care`) → nhóm
**"Danh mục - Dịch vụ"**. Sheet `Gộp phân hệ ERP-HRM` xếp cả nhóm danh mục dịch vụ vào CSKH chứ
không vào phân hệ nào của nhóm SẢN XUẤT - CUNG ỨNG (xem `components/subsystem-menu/customer-care.js`).

**Đây là 2 màn ĐẦU TIÊN của phân hệ CSKH** — `Modules/CustomerCare` hiện chỉ có khung rỗng
(`.gitkeep`), `pages/customer-care/` mới có `dashboard/`, và chưa có quyền nào `type = 24`.

## Hiện trạng ERP

### 1. Cấp dịch vụ bảo dưỡng — `admin/.../levels`

| | |
|---|---|
| Controller | `Sale\LevelController` (117 dòng) |
| Model | `App\Model\Sale\Level` — bảng `levels`, extends `Model` thuần |
| View | 1 file `sale/levels/index.blade.php` — DATATABLE + 2 modal create/edit |
| Bảng | `levels` — **29 bản ghi**, 4 cột: `id, name, created_at, updated_at` (không có audit) |
| Cột DS | STT, Tên cấp, Hành động |
| Bộ lọc | 1 ô text: Tên cấp |
| Form | 1 field: `name` (required, unique) |
| Xóa | Chặn nếu tồn tại `service_levels.level_id` |

### 2. Danh mục ghi chú kiểm tra bảo dưỡng — `admin/.../note_maintenances`

| | |
|---|---|
| Controller | `Sale\NoteMaintenanceController` (117 dòng) |
| Model | `App\Model\Sale\NoteMaintenance` — bảng `note_maintenances`, extends **`BaseModel`** |
| View | 4 file: index + **create/edit là trang riêng** (`form.blade.php` dùng chung) |
| Bảng | `note_maintenances` — **11 bản ghi**, 8 cột, có `created_by`/`updated_by` kiểu **varchar(255)** lưu ERP `employees.id` |
| Cột DS | STT, Hạng mục, Ký hiệu, Mô tả, Hành động |
| Bộ lọc | 2 ô text: Hạng mục, Ký hiệu |
| Form | 3 field: `name` (required, unique), `key_name` (required, unique), `description` |
| Xóa | **Không chặn gì** |

Cả 2 màn **không gate quyền nào** bên ERP.

## Lỗi / thiếu sót của bản ERP

1. **Điều kiện chặn xóa của `levels` thiếu 5/6 bảng.** ERP chỉ kiểm `service_levels`, trong khi
   `level_id` xuất hiện ở **6 bảng**: `service_levels` (12 cấp đang dùng), `service_maintain_levels`
   (12), `wr_service_quotation_extend_product_services` (10), `wr_assign_task_extend_product_services`
   (7), `wr_import_result_extend_product_services` (7),
   `wr_service_contract_extend_product_services` (7). → xóa được cấp đang dùng trong hợp đồng /
   báo giá dịch vụ, làm mồ côi dữ liệu.
2. **`note_maintenances` không chặn xóa gì cả**, dù `service_maintain_levels.note_maintenance_id`
   đang dùng **9/11** bản ghi.
3. `LevelController::store/update` catch `Exception` không import namespace (`\Exception`) —
   lỗi thật sẽ không rơi vào catch. Lặp lại ở `NoteMaintenanceController`.
4. `NoteMaintenanceController` còn biến rác `$json = new stdClass()` không dùng.

## Quyết định (áp theo tiền lệ 3 màn Tài chính, user đã chốt cùng dạng)

| # | Nội dung | Chốt |
|---|---|---|
| 1 | Phạm vi | **Bám sát ERP** — list + modal CRUD + xóa + lọc. Không thêm cột, không history/import |
| 2 | Xóa | **Chặn khi đang dùng, kiểm ĐỦ mọi bảng tham chiếu** (sửa lỗi 1 + 2) |
| 3 | `note_maintenances.created_by/updated_by` | HRM vẫn ghi **ERP `employees.id`** để 2 cổng nhất quán, nhưng **không hiển thị** (ERP cũng không hiển thị) |
| 4 | Form ghi chú | Đưa về **modal** cho đồng bộ với các màn danh mục HRM, thay vì trang riêng như ERP |

## Gỡ bỏ lớp map ERP employee (user báo giữa chừng 2026-08-03)

Ban đầu tôi tách `app/Helper/ErpEmployeeHelper.php` để map HRM user → ERP `employees.id` cho cả
2 phân hệ. **User báo đã gộp `employees` + `employee_infos` giữa 2 hệ, chỉ còn 1 bảng.**

Đã kiểm chứng trên DB/commit:

- Commit `gộp bảng employees: HRM đọc lại bảng employees chung (revert hrm_employees)`
- `App\Models\TpEmployee::$table` giờ là **`employees`** (trước là `hrm_employees`)
- Bảng `employees` + `employee_infos` được tạo lại lúc **2026-08-03 08:48**; `hrm_employees`
  còn từ 2026-07-30 là **bản cũ bỏ đi** (id lệch 290 dòng, `employee_info_id` lệch 164 dòng)

→ `auth()->user()->id` **chính là** id nhân viên, không còn khái niệm ERP id riêng. Đã gỡ:

| Bỏ | Thay bằng |
|---|---|
| `app/Helper/ErpEmployeeHelper.php` | (xóa hẳn, revert `composer.json`) |
| `FinanceService::requireErpEmployeeId()` / `erpEmployeeId()` / `toErpEmployeeId()` | `currentEmployeeId()` = `auth()->user()->id` |
| `Modules\Finance\Entities\ErpEmployee` | `Modules\Human\Entities\Employee` (cùng bảng `employees`) |
| accessor `->display_name` của ErpEmployee | `Account::employeeDisplayName()` / `TypeAccount::employeeDisplayName()` — ghép `"MÃ - Họ tên"` tại chỗ, **không sửa model dùng chung** |
| request attribute `erp_employee_id` | `current_employee_id` |

Bộ lọc "Người tạo"/"Người cập nhật" ở 2 màn tài khoản giờ dùng thẳng id từ dropdown, bỏ bước map.

⚠️ **Chưa đụng tới**: `app/Helpers/ErpPermissionHelper.php` (đọc qua `mysql2` → DB ERP cũ) và các
chỗ gọi nó trong `Modules/Assign` + `app/Helper/CustomerOwnership.php`. Việc gộp bảng khiến phần
đó cũng nên bỏ, nhưng nằm ngoài phạm vi 2 màn này — cần rà riêng.
Xem [[project_erp_employee_id_drift_gop_db]].
