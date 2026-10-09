# Design — Danh mục công việc, lỗi thiết bị (migrate ERP → HRM)

> Nhánh **gop_db** (DB gộp `erp_hrm_check`). Migrate feature "Danh mục công việc – lỗi thiết bị" từ ERP (`device-errors`, module Sale) sang HRM (`Modules/CustomerCare` + `pages/customer-care/device-errors`). Điền link vào placeholder `customer-care.js:27`.

## Mục tiêu & scope
- Code lại **đầy đủ** chức năng CRUD danh mục công việc/lỗi thiết bị trên HRM (mức A), gồm cả sub-entities: vật tư kèm, vật tư thay thế, chi phí kèm, nhóm.
- **Global** (không phân quyền theo cấp công ty/phòng ban) — chỉ gate bằng **1 quyền** `Quản lý danh mục công việc, lỗi thiết bị`.
- Có **in** danh sách + **xuất Excel**.
- Nhóm lỗi thiết bị quản lý **inline** như ERP (không menu riêng).

## Quyết định chốt với user
- Mức migrate: **A (đầy đủ 5 bảng)**.
- Quyền: **1 quyền** `Quản lý danh mục công việc, lỗi thiết bị` (gộp thêm/sửa/xóa/khóa), **global**.
- In + xuất Excel: **có**.
- Nhóm: **inline như ERP**.
- **Bỏ CRM sync** (giống Cost/Service đã migrate).

## Kiến trúc — DB gộp, KHÔNG migration
> **CẬP NHẬT SCOPE (2026-08-06):** ERP đã tự **drop** `description`/`reason`/`solution`/`group_error_id` từ migration `2022_09_17_add_type_to_device_errors` (up). Nên ERP hiện tại + DB gộp `erp_hrm_check` KHÔNG có 4 cột này. Bỏ khỏi scope: 3 ô mô tả/nguyên nhân/giải pháp + **nhóm** (group_error_id + bảng `device_error_groups` rỗng 0 bản ghi). Feature bám đúng schema thực tế.

Bảng đã tồn tại sẵn trong `erp_hrm_check` (device_errors = 2768 bản ghi):
- `device_errors` — field THỰC TẾ: `name`, `type` (1-6), `recipe_work_norm` (định mức công), `note`, `price`, `discount_rate`, `benefit_coefficient` (>0), `vat_percent`, `status` (1 hoạt động / 2 khóa), `created_by`, `updated_by`. (KHÔNG có description/reason/solution/group_error_id.)
  - `type`: 1 Lỗi đã xác định, 2 Lỗi chưa xác định, 3 Lắp đặt bàn giao, 4 Thiết kế nền móng, 5 Tư vấn khảo sát, 6 Giám sát thi công.
- `device_error_costs` — chi phí kèm (`cost_id`, `price`, `price_service`).
- `device_error_products` — vật tư **kèm** (`type=1`) & **thay thế** (`type=2`) (`product_id`, `type`).
- (`device_error_groups`, `device_error_has_group_product` — tồn tại nhưng KHÔNG dùng, bỏ khỏi scope.)

Tham chiếu (đọc): SP qua `ErpProduct` (bảng `products`), chi phí qua `Cost` (bảng `costs`), nhóm SP qua group. `price` có thể auto tính = `company.work_price × company.coefficient_price_service × recipe_work_norm` nếu không nhập tay; `engineering_work` = `work_price × recipe_work_norm`.

## Backend — `Modules/CustomerCare`
- **Entities** (không kế thừa BaseModel, tự gán created_by/updated_by — như `Cost`/`Service`): `DeviceError`, `DeviceErrorGroup`, `DeviceErrorCost`, `DeviceErrorProduct`, `DeviceErrorHasGroupProduct`. Quan hệ: `products()`/`productReplacements()` (belongsToMany products qua device_error_products, phân biệt bằng type), `costs()` (belongsToMany costs qua device_error_costs), `group()`.
- **Controller `DeviceErrorController` (V1)**: `searchData` (list phân trang + filter theo tên/loại/nhóm/trạng thái/người tạo), `store`, `update`, `show`, `delete`, `lock`, `restore`, `getProductsAjax`, `printList`, `exportList`, `print`.
- **Validation** (rethrow ValidationException): `name` required + unique theo `type`; `type` in 1-6; `recipe_work_norm` required; `products` required array; `discount_rate` required; `benefit_coefficient` required numeric >0; `vat_percent` required ≤100.
- **Business rules**:
  - `is_can_delete` = `status = hoạt động` + có quyền + **chưa bị tham chiếu** bởi bảng downstream bảo hành (Wr* trong DB gộp: wr_service_quotation/contract product/item/service device_errors, wr_assign_task, wr_import_result, warranty_report_descriptions, warranty_repair_handle...). Khi xóa: xóa kèm device_error_costs + device_error_products.
  - `lock`: status 1→2 (chỉ khi đang hoạt động). `restore`: status 2→1.
- **Bỏ CRM sync** (không port hook updating đẩy product.template).
- **Route** prefix `customer-care/device-errors`, `checkPermission:Quản lý danh mục công việc, lỗi thiết bị` cho store/update/delete/lock/restore. Thêm quyền vào `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
- **Excel**: class export trong `Modules/CustomerCare` (mirror `DeviceErrorExcel` ERP).

## Frontend — `pages/customer-care/device-errors/` (V2Base)
- `index.vue`: `V2BaseFilterPanel` (tên, loại, nhóm, trạng thái, người tạo) + `V2BaseDataTable` (cột: STT, tên, loại, nhóm, định mức công, giá, trạng thái, thao tác) + `BaseConfirmModal` xóa/khóa/khôi phục + nút In + Xuất Excel.
- Modal create/edit (ref-based): thông tin chung (name/type/recipe_work_norm/note/discount_rate/benefit_coefficient/vat_percent/price/mô tả-nguyên nhân-giải pháp) + tab **vật tư kèm** + tab **vật tư thay thế** + tab **chi phí kèm** + chọn/tạo nhanh **nhóm** (inline). Inline error + `touched`.
- Điền `link: '/customer-care/device-errors'` vào `components/subsystem-menu/customer-care.js:27`.

## Ngoài phạm vi
- CRM sync.
- Downstream báo giá/HĐ dịch vụ bảo hành (vẫn do ERP quản lý, dùng chung data trên DB gộp).

## Rủi ro / lưu ý
- Bảng đã có 2768 bản ghi thật → test kỹ list/filter/phân trang, không phá data.
- `is_can_delete` phải quét đúng tập bảng downstream (nhiều bảng) — cân nhắc gom thành helper.
- Pricing auto (`work_price × coefficient × recipe_work_norm`) phụ thuộc config Company — cần lấy đúng company hiện hành.
