# Sửa lỗi code gốc do e2e duyệt thật phát hiện (18/11/2026) — @cuong61n

Nguồn: `e2e-duyet-that.md` mục 3. Không commit, không migrate. Test chạy `vendor/bin/phpunit` (hrm-api).

## 1. Thông báo kế toán kho đọc bảng cũ
- `Modules/Finance/Services/ProductImportRequestService.php` — thêm `warehouseAccountantIds()` (join `accounting_warehouse_accountants` → `accounting_warehouses.warehouse_id`), dùng ở `notifyWarehouseAccountants()` (~794) và đoạn gửi duyệt (~1990).
- `Modules/Finance/Services/WarehouseImportWriteService.php::send()` (~1343) — cùng truy vấn.
- Trước: `warehouse_accountants` = 0 dòng → danh sách người nhận rỗng. Sau: kho 1 → 18 kế toán (`[125,199,…]`).
- Không sửa: `PhysicalWarehouseService.php:201` (xoá `warehouse_accountants` khi xoá kho — bảng chết, vô hại; xoá kho còn kế toán ở `accounting_*` là việc khác, chưa đổi); các dòng còn lại chỉ là chú thích.
- Test: `tests/Feature/Finance/WarehouseAccountantRecipientsTest.php`.

## 2. Lỗ hổng phân quyền BE
`Modules/Training/Routes/api.php` — thêm `->middleware('checkPermission:<mã>')`:
- `course-registers/{id}/toggle-approve` → `training.dang_ky_khoa_hoc.approve`
- `training-planning/{id}/toggle-approve` → `training.ke_hoach_dao_tao.approve`
(mã lấy từ `CourseRegisterDefinition::PERMISSION`, `TrainingPlanningDefinition::PERMISSION`). `handover_record` giữ nguyên theo chốt của user.
- Trước (tắt middleware): người lạ 200, phiếu đổi trạng thái. Sau: người lạ 403, phiếu giữ nguyên; người có mã vẫn 200 và duyệt được.
- Test: `tests/Feature/ApprovalCenter/Training/ToggleApprovePermissionTest.php` (2 test, đã xác nhận FAIL khi gỡ middleware). `tests/Feature/ApprovalCenter/Training` 60 test OK; `approval-inbox:verify course_register` 22.464 cặp chênh lệch 0; `training_planning` 0 phiếu chờ, chênh lệch 0.

## 3. Màn gốc 500 khi mở phiếu
- `DetailRenewLaborContractResource.php:95` — `competencies` = `[]` khi `rank` null.
- `TroubleShootingReportController.php:~79` — khai `$violators = []` trước vòng lặp.
- `DetailCapacityEvaluateResource.php:22-26` — `optional($this->evaluationPlanningCapacity)->…`.
- `PaymentBusinessRequestTransformer.php:102` (+ `approved_by`) — `optional(optional(...)->info)->fullname`.
- FE `hrm-client/pages/training/capacity-evaluate/_id/approve.vue` `created()` — try/catch/finally: lỗi API thì toast `$toasted.global.error` và tắt vòng xoay.
- Bằng chứng (probe JWT người dùng 13 gọi route thật): `payment 978` trước 500 `Attempt to read property "info" on null` → sau 200; `renew 39` và `trouble-shooting 278` sau sửa 200 (trước sửa là 500 theo laravel.log e2e). `capacity 446` hiện 404 (phiếu thử đã bị dọn) nên kiểm bằng test đơn vị.
- Test: `tests/Feature/NullGuards/DetailResourcesNullRelationTest.php` (renew + capacity với quan hệ null). Chưa có test riêng cho trouble-shooting và payment (kiểm bằng probe HTTP).

## 4. Route chết
- `Modules/Decision/Routes/web.php` gỡ `GET /decision` → `DecisionController@index`; cùng lỗi ở `Modules/Rice/Routes/web.php` → gỡ. `php artisan route:list` chạy lại được.
- `Modules/CRM/Routes/web.php` có cùng stub `CRMController@index` (không tồn tại) nhưng file không được nạp nên không làm vỡ route:list — để nguyên.
