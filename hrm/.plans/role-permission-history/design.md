# role-permission-history — Tóm tắt

## Mục tiêu
Bổ sung "Lịch sử thay đổi" cho màn **Phân quyền / Chức vụ** (`/timesheet/setting/roles` + màn Thêm/Sửa `/roles/add/{id}`) — audit ai tạo/sửa/xóa chức vụ nào, cũ → mới, lúc nào.

## Bối cảnh kỹ thuật
- Màn lưu qua `POST timesheet/roles/store` → `RoleController::store` → `RoleService::save()` (endpoint chỉ màn này dùng, có `auth:api`, gate FE bằng quyền 'Quản lý phân quyền').
- `save()` ghi cho 1 chức vụ: **name/description/sort_order** (bảng `roles`), **companies áp dụng** (`company_roles`, sync), **permissions theo từng công ty** (`role_has_permissions` cột role_id/permission_id/company_id, qua `syncPermissionsByCompany`).
- Xóa qua `DELETE timesheet/roles/{id}` → `RoleController::delete` (chỉ khi `canDelete()` = chưa gán NV).

## Quyết định (đã chốt với user)
1. Ghi **cả 3 thao tác**: create + update + delete.
2. Nút "Lịch sử thay đổi" ở **CẢ HAI**: màn danh sách (dropdown thao tác từng dòng) + màn Sửa (nút light cạnh Lưu/Quay lại, chỉ hiện khi đang sửa).
3. **KHÔNG** permission riêng (màn đã gate bằng 'Quản lý phân quyền').
4. Biến thể **full-snapshot** (lưu snapshot đầy đủ 2 phía, FE tự diff) — vì companies + permissions là list.

## Thiết kế
- **DB**: bảng `role_permission_history` (module Timesheet): `role_id` (index), `action` (create|update|delete), `old_value`/`new_value` (JSON `{name, description, sort_order, companies:[tên], permissions:[{company, items:[{module_type, module, group, name}]}]}`), `changed_by`, `changed_at`, timestamps. KHÔNG company_id (scope theo role_id).
  - **Chi tiết phân quyền**: mỗi quyền lưu kèm **phân hệ** (`permissions.type` 1-7 → nhãn qua `RoleService::MODULE_LABELS`) + **phần** (`permissions.group`) + tên (`display_name`) → hiển thị theo cây Công ty(tab) → Phân hệ → Phần → Quyền.
- **BE**: `RoleService`:
  - `buildRoleSnapshot($roleId)` — đọc roles + company_roles + role_has_permissions, resolve **TÊN** (company/permission), sort ổn định (companies theo tên, permission_names sort, companies theo tên). Trả null nếu role không tồn tại.
  - `save()`: nhánh create → sau khi lưu build snapshot → `logRoleHistory('create', null, new)`. Nhánh update → chụp snapshot TRƯỚC mutation → sau mutation build new → nếu JSON khác → `logRoleHistory('update', old, new)`.
  - `logRoleHistory($roleId, $action, $old, $new)` — `changed_by = Auth::id()`, JSON_UNESCAPED_UNICODE.
  - `roleHistories($roleId)` sort cũ→mới, trả `changed_by_name` (fullname??email??'—') + `changed_at` (d/m/Y H:i:s) + `changed_at_raw` (Y-m-d).
  - Controller `histories(Request)` đọc `role_id`, responseJson 3-arg. `delete()` chụp snapshot TRƯỚC `$role->delete()` → `logRoleHistory('delete', old, null)`.
  - Route `GET timesheet/roles/histories` đặt **TRƯỚC** `/{id}`.
- **FE**: `components/setting/roles/RolePermissionHistoryModal.vue` — `open(roleId, name)`, tự diff:
  - create/delete → hiển thị full snapshot (create chữ/chip xanh, delete chữ/chip đỏ). "Chi tiết phân quyền" dạng CÂY: Công ty(icon tòa nhà) → Phân hệ → "Phần:" + chip quyền.
  - update → diff từng phần: Tên/Ghi chú/Vị trí cũ(đỏ)→mới(xanh), Công ty áp dụng thêm(+xanh)/bỏ(−đỏ). "Chi tiết phân quyền thay đổi" dạng CÂY: gom quyền thêm/bỏ theo Công ty → Phân hệ → Phần, chip +xanh/−đỏ (helper groupByModuleGroup + buildChangeTree, key = module|group|name).
  - Bộ lọc Thao tác/Người/ngày. Dot màu: create xanh / update amber / delete đỏ.
  - Gắn vào cả 2 màn (list dropdown-item + edit page nút light).

## Auth note
Auth model = `App\Models\TpEmployee`, id khớp Employee id → `user.info->fullname` (xem [[master-settings-notes]]).
