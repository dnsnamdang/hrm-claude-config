# Spec — Reconcile `employees` về 1 bảng (ERP + HRM)

> Thuộc dự án [Hợp nhất ERP+HRM / Gộp DB]. Làm trên nhánh `gop_db`. Cập nhật 2026-07-30.
> Chạy SAU bước gộp DB (merge_prod → rename hrm_*). Đây là bước "reconcile" đưa `employees` + `hrm_employees` về **1 bảng duy nhất**.

## 1. Mục tiêu & quyết định đã chốt
- **1 bảng `employees` duy nhất**, id **ERP làm chuẩn** (FK ERP ~1069 cột > HRM ~615 → remap ít hơn nếu giữ id ERP).
- **Auth:** giữ `password` + `token_version` + `password_changed_at` của **HRM** trong bảng thống nhất (HRM là chủ auth qua JWT; ERP đăng nhập qua SSO→HRM). KHÔNG reset password.
- **Sản phẩm:** script `reconcile_employees.php` (chạy qua tinker như `merge_prod.php`) — **idempotent, DRY-RUN mặc định, tái chạy được**. Chạy trên bản merge **tươi** (có cả `employees` + `hrm_employees`); nếu đã reconcile (`hrm_employees` không còn) → **skip**.
- `hrm_employees` bị gộp vào `employees` rồi **DROP**.

## 2. Số liệu nền (bản merge local erp_hrm_check, 2026-07-30)
- `employees`(ERP)=1085, `hrm_employees`(HRM)=1085.
- Map qua `employee_info_id`: **1085/1085** (khớp 100%). Local: 0 người chỉ-1-hệ (server có thể khác → script vẫn xử lý case lệch).
- Khảo sát prod trước đó: id đụng nhưng KHÁC người (**164**), cùng người KHÁC id (**454**) → **KHÔNG union theo id**; **map bắt buộc qua `employee_info_id`**.
- Cột HRM-only cần thêm vào `employees`: `tp_id, password_changed_at, rice_setting_location_id, rice_ssn, login_count`.

## 3. Chìa khóa: `emp_id_map(hrm_id, erp_id)`
```sql
-- chỉ chứa cặp CẦN đổi (hrm_id != erp_id); cùng id thì no-op
CREATE TABLE emp_id_map AS
SELECT h.id AS hrm_id, e.id AS erp_id
FROM hrm_employees h JOIN employees e ON e.employee_info_id = h.employee_info_id
WHERE h.id <> e.id;
```
- Người **chỉ có ở HRM** (không match employee_info_id): INSERT vào `employees` với **id mới** (auto_increment tránh đụng), thêm map hrm_id→id_mới.
- Người **chỉ có ở ERP**: giữ nguyên.

**Tập con AN TOÀN cho bảng SHARE** (dùng ở mục 5, option b):
```sql
-- hrm_id KHÔNG trùng id ERP nào -> trên bảng trộn 2 nguồn vẫn remap an toàn (giá trị chỉ có thể là người HRM)
CREATE TABLE emp_id_map_safe AS
SELECT m.hrm_id, m.erp_id FROM emp_id_map m
WHERE m.hrm_id NOT IN (SELECT id FROM employees);
```
- `emp_id_map_safe` ≈ 454 người "cùng người khác id" (an toàn); 164 người "trùng id khác người" bị loại (nhập nhằng trên bảng SHARE).

## 4. Các bước script (thứ tự bắt buộc)
1. **Guard**: nếu `hrm_employees` không tồn tại → in "đã reconcile" + return. `SET FOREIGN_KEY_CHECKS=0` khi thực thi.
2. **Build `emp_id_map`** (mục 3). In số cặp cần đổi.
3. **Thêm cột HRM-only** vào `employees` (ALTER ADD COLUMN nếu chưa có): tp_id, password_changed_at, rice_setting_location_id, rice_ssn, login_count.
4. **Cập nhật auth + rice cho 1085 dòng khớp**: `UPDATE employees e JOIN hrm_employees h ON h.employee_info_id=e.employee_info_id SET e.password=h.password, e.token_version=h.token_version, e.password_changed_at=h.password_changed_at, e.tp_id=h.tp_id, e.rice_setting_location_id=h.rice_setting_location_id, e.rice_ssn=h.rice_ssn, e.login_count=h.login_count`.
5. **Người chỉ có ở HRM** → INSERT vào employees (id mới) + cập nhật emp_id_map.
6. **Remap FK** (mục 5 chi tiết bên dưới): mọi cột tham chiếu employee bên **HRM-origin** → `UPDATE t JOIN emp_id_map m ON t.<col>=m.hrm_id SET t.<col>=m.erp_id`.
7. **DROP `hrm_employees`** + `DROP TABLE emp_id_map` (hoặc giữ để audit).
8. `SET FOREIGN_KEY_CHECKS=1`. In tổng kết.

## 5. Remap FK — phần rủi ro nhất (chi tiết + chống collision)
**Nguy cơ collision (164 case):** một giá trị cột đang là **id ERP đúng** có thể trùng 1 `hrm_id` của người khác trong map → remap NHẦM.
**Giải pháp — chỉ remap trên bảng HRM-origin, KHÔNG đụng bảng ERP & bảng SHARE:**
- **Bảng HRM-origin** (danh sách 639 tên từ `hop-nhat-erp-hrm/hrm-view-tables.txt`, gồm 23 bảng `hrm_*` + các bảng HRM move nguyên tên) → mọi cột employee-ref chứa **toàn id HRM** → remap AN TOÀN (không có id ERP để đụng).
- **Bảng ERP-origin** (không nằm trong danh sách HRM) → giữ nguyên (id ERP đã chuẩn).
- **Bảng SHARE (16)** (customers, companies, employee_infos, departments, parts...) → remap cột created_by/updated_by **bằng `emp_id_map_safe`** (chỉ 454 người có hrm_id KHÔNG trùng id ERP nào → không thể đụng nhầm dòng ERP). **Bỏ 164 người trùng id** (nhập nhằng): dòng SHARE do đúng 164 người này tạo sẽ giữ created_by cũ (sai audit nhỏ). Bảng HRM-origin non-SHARE vẫn dùng map ĐẦY ĐỦ (an toàn vì chỉ chứa id HRM). → script in riêng: số dòng SHARE remap được (safe) vs 164 bỏ qua.

**Enumerate cột cần remap (3 lớp, script tự dò + LOG để duyệt DRY-RUN):**
- (a) `information_schema.KEY_COLUMN_USAGE`: FK constraint trỏ `employees`/`hrm_employees`.
- (b) Heuristic tên cột trên bảng HRM-origin: `created_by, updated_by, employee_id, approver_id, approved_by, assigned_by, buyer_id, signer_id, receiver_id, handler_id, requester_id, manager, reviewer_id, creator_id, ...` (danh sách mở rộng dần).
- (c) Rà code HRM (grep) đối chiếu — bổ sung cột tên lạ.
- Script in **bảng-cột + số dòng sẽ đổi** ở DRY-RUN; user duyệt trước khi chạy thật. **Sót 1 cột = FK trỏ nhầm người** → phải rà kỹ.

## 6. Sửa code HRM (ngoài script, ~30 điểm — undo phần rename bảng employees)
Ta vừa cho HRM trỏ `hrm_employees`. Sau reconcile bảng thống nhất là `employees` → đổi lại:
- Model `$table='hrm_employees'` → `'employees'`: `app/Models/TpEmployee.php`, `app/Models/Employee.php`, `Modules/Timesheet/Entities/Employee.php`, `Modules/Human/Entities/Employee.php` (các model connection mặc định; **TpEmployee2/... mysql2 giữ nguyên** = ERP).
- `config/auth.php` provider vẫn `App\Models\TpEmployee` (nay $table='employees').
- Các `join/leftJoin('hrm_employees'...)` + tiền tố cột `hrm_employees.` → `employees.` (các file đã sửa lúc rename: AuthNewController, EmployeeService, các Service Decision/Training...).
- **Pivot `hrm_*` GIỮ NGUYÊN TÊN** (hrm_employee_has_roles, hrm_company_employees...): chỉ DATA `employee_id` được remap ở bước 6, code không đổi.
- config/permission.php giữ hrm_* (roles/permissions vẫn tách).

## 7. Verify (sau chạy thật)
- Đếm: `employees` = 1085 (+ người chỉ-HRM nếu có); `hrm_employees` không còn.
- Spot-check 5 NV: dòng gộp đúng (email, employee_info_id, password = HRM), FK trên vài bảng HRM (hrm_employee_has_roles.employee_id, timesheets.created_by...) trỏ đúng người (join employee_infos ra đúng tên).
- HRM login (JWT) OK; ERP login (SSO) OK.
- Rà FK mồ côi: cột đã remap không còn giá trị = hrm_id cũ nào (trừ collision đã loại).

## 8. Rủi ro & giảm thiểu
| Rủi ro | Giảm thiểu |
|---|---|
| Sót cột FK (tên lạ) → trỏ nhầm người | Dò 3 lớp + LOG DRY-RUN cho user duyệt; whitelist bổ sung |
| Collision 164 (id ERP trùng hrm_id) | Non-SHARE HRM-origin: map ĐẦY ĐỦ (chỉ chứa id HRM, không đụng). SHARE: chỉ `emp_id_map_safe` (454) → 164 người bỏ (audit created_by trên bảng SHARE của đúng 164 người này hơi lệch) |
| Người chỉ-1-hệ (server) | Script xử lý case lệch (INSERT id mới / giữ nguyên) |
| Password/token sai → login hỏng | Lấy nguyên từ HRM; verify login sau chạy |
| Chạy nhầm 2 lần | Guard hrm_employees; emp_id_map build lại từ bản tươi |

## 9. Điều kiện & thứ tự chạy trên server (pipeline gộp)
1. `merge_prod.php` (gộp DB, tách hrm_*).
2. Sửa code HRM sang hrm_* (đã làm) + **undo employees → employees** (mục 6) — deploy.
3. `reconcile_employees.php` (DRY-RUN duyệt cột FK → chạy thật).
4. Verify + smoke test 2 app.

## 10. Ngoài phạm vi (làm sau)
- Reconcile các pivot/bảng khác (roles/permissions, files...) — vẫn TÁCH hrm_*, hợp nhất khi port module.
- `employee_infos` (hồ sơ) đã union 100% ở bước merge — KHÁC `employees`, không thuộc spec này.
