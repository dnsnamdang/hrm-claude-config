# Report Fix-1 — sửa BE hrm-api theo review T1 (14/10/2026)

Repo `wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/cdhh-2c-xe`. Commit: **eda8ebbff** (không push/merge/stash).

## Đã sửa
- **C1** Quyền 1699–1706 → **1720–1727** (cùng thứ tự). Quét `git fetch` + mọi nhánh remote: max id seeder = 1711 (`origin/develop`), gop_db 1698, các nhánh khác ≤ 1678; không nhánh nào chạm 1720–1727 (1712–1719 chừa cho develop). DB `hrm_erp_giacty`: role_has_permissions / employee_has_permissions = 0 dòng cho 8 quyền (không có bảng model_has_permissions); UPDATE id 8 dòng, 1707–1999 trước đó trống; đã `forgetCachedPermissions` + `Cache::flush`. Không còn chỗ gõ cứng id (test, FE).
- **I1** `ExternalDriverService::getAll()` chỉ select `id, name, status` (+ `is_locked`). Thêm route có gate `GET vehicles/options/external-drivers` (Xem|Quản lý danh mục xe) trả thêm `phone` — `VehicleController::externalDriverOptions`.
  - **FE cần đổi (hrm-client, không đụng):** `pages/master-data/vehicles/AddVehicleModal.vue` `loadExternalDrivers()` (dòng ~452) đang gọi `external-drivers/getAll` và đọc `row.phone` → đổi sang `master-data/vehicles/options/external-drivers` (cùng tham số `include_ids`). Nếu chưa đổi: không lỗi, chỉ mất hậu tố " - SĐT" ở nhãn ô chọn.
- **M1** `FuelService::catalogDisplay`: có phần lẻ thì 2 chữ số ("19.500,40"), không thì số nguyên.
- **M2** `ExternalDriverRequest::prepareForValidation` trim name/phone/id_card/driver_license/birth_year trước validate.
- **M3** `VehicleController::unlock`: biển số đang khoá → 422 "Không thể mở khóa: biển số "X" đang bị khóa…"; trùng biển với xe hoạt động khác đổi 400 → **422** theo brief (test cũ cập nhật). FE nếu bắt riêng 400 cho nhánh này cần biết.
- **M4** `employeeOptions` bỏ `telephone`; FE T2 không đọc SĐT từ đó (grep không thấy).

## Test
`VehicleCatalog2cTest`: 21/21 (thêm 6 ca: dải quyền, getAll không lộ + options có gate, thập phân giá, trim, mở khoá khi biển khoá, employees không SĐT; ca gate 403 thêm route mới). Cả `Modules/MasterData`: **OK 532 tests / 4674 assertions** (526 + 6). Số dòng bảng sau test: license_plates 163 · drives 72 · vehicles 137 · fuels 4 · vehicle_drivers 110 · vehicle_company_drivers 74 (đúng mốc).

## Lo ngại
- Ghi nhận không làm: M5, M6/N103, M9 theo brief.
- Route chung `catalog-histories/drives/{id}` vẫn không gate (N64) — mở đường đọc diff CCCD/SĐT; chưa xử lý vì ngoài brief.
- `.env.bak-hrm_erp` untracked có sẵn, không commit.
- `Cache::flush()` trên local đã xoá cache của cả các session khác (vô hại, chỉ cache).
- Deploy prod: id 1720–1727 phải đồng bộ với bất kỳ INSERT quyền thủ công nào; I3 (gán quyền trước khi bật chặn ERP) vẫn còn mở.
