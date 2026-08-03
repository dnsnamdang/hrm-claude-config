# Fix: DepartmentChange store/update crash khi department_lead_id/title_id dangling

Bug production 2026-07-02: `Trying to get property 'code' of non-object` tại `DepartmentChangeService.php:86` khi tạo Quyết định điều chuyển phòng ban.

Root cause: FE prefill `department_lead_id`/`department_lead_title_id` từ bản ghi phòng ban; phòng ban trỏ tới `employee_infos`/`titles` đã bị xóa → BE `EmployeeInfo::find()`/`Title::find()` trả null nhưng gọi `->code`/`->name` trong ternary (không null-safe). Company/Group/Department cùng file đã dùng `?? ''` nên không dính.

## Phase 1 — BE

- [x] `store()`: fetch EmployeeInfo/Title 1 lần vào biến, build `*_lead_name`/`*_title_name` null-safe (`?? ''`)
- [x] `update()`: fix y hệt (pattern lặp lại dòng 131-137)
- [x] Verify: php -l sạch + tinker id dangling → name = '' không crash, id thật → 'code - fullname' đúng

### Checkpoint — 2026-07-02
Vừa hoàn thành: fix null-safe cả store() + update(), verified tinker
Đang làm dở: —
Bước tiếp theo: deploy file lên production (/var/www/tpe/hrm-api); cân nhắc dọn data dangling department_lead_id trong bảng departments
Blocked: —
