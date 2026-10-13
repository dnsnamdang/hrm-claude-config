# Fix: Quyết toán công theo HĐ — enforce quyền QTC + sync QTC khi sửa

**Module:** `hrm-api/Modules/Assign` — `SettlementContractController` (màn PLBS = quyết toán công theo hợp đồng).

## Bối cảnh (đã điều tra)
Luồng hiện tại: PCT chọn "Nhân viên QTC" (`AssignBusinessTask.employee_info_qtc_ids`) → chỉ NV QTC thấy HĐ để tạo quyết toán (`getDataContractWaitSettlement` lọc `whereJsonContains employee_info_qtc_ids`) → khi lưu, `store()` gọi `syncEmployeeQtcContractErp` ghi `employee_qtc_id`/`department_qtc_id` về HĐ ERP.

2 khe hở:
1. **Quyền QTC chỉ chặn ở UI (list filter), không enforce ở `store()`** → gọi thẳng API `store` với `contract_id` bất kỳ vẫn tạo được.
2. **`update()` KHÔNG gọi `syncEmployeeQtcContractErp`** → sửa quyết toán không cập nhật lại người/phòng QTC trên HĐ ERP (HĐ giữ giá trị lần tạo đầu).

## Tasks
- [x] **Fix 1 — enforce quyền QTC ở `store()`:** SettlementContractController:88-95 — check `AssignBusinessTask` (contractable_type+contractable_id = HĐ, whereJsonContains employee_info_qtc_ids = user) → 403 nếu không phải NV QTC.
- [x] **Fix 2 — `update()` gọi `syncEmployeeQtcContractErp($request)`:** SettlementContractController:146 (sau syncEmployees).
- [x] `php -l` sạch. Không commit.

## Fix 3 — Auto-fill NV QTC theo PCT gần nhất cùng HĐ
**Bối cảnh:** auto-fill hiện đọc `contract->employee_qtc_id` — chỉ set khi quyết toán công (1 lần/HĐ) → thực tế không dùng được khi tạo PCT. User muốn auto-fill theo **PCT gần nhất** (id desc).
- [x] Sửa `Modules/Assign/Transformers/WrAssignTaskResource/WrAssignTaskListResource.php` (~dòng 81): ưu tiên lấy `employee_info_qtc_ids` của `AssignBusinessTask` gần nhất cùng HĐ (`contractable_type`+`contractable_id`, `orderByDesc('id')`), fallback về `contract->employee_qtc_id` (nhánh cũ). FE không đổi (`HandleMixin:454` đã tự điền từ `employee_info_qtc_id`/`name`).
- [x] `php -l` sạch. Không commit.

## Lưu ý
- `syncEmployeeQtcContractErp` dùng `auth()` (người thao tác). Sau fix 2, `update()` sẽ ghi người/phòng QTC = **người đang SỬA**. Trong thực tế người sửa = người tạo = NV QTC (do fix 1 + `canEdit`), nên trùng; nếu muốn cố định theo NGƯỜI TẠO (created_by) bất kể ai sửa → cần đổi logic hàm (hỏi trước). Bản này giữ mirror store cho nhất quán.

### Checkpoint — 2026-07-31
Vừa hoàn thành: điều tra + viết plan
Đang làm dở: implement 2 fix trong SettlementContractController
Bước tiếp theo: sửa store() + update(), php -l
Blocked:
