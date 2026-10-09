# Hiện trạng & mục tiêu cuối — 58 bảng trùng tên (Gộp DB ERP + HRM)

> Cập nhật: 2026-07-30. Nguồn: `merge_prod.php` (bản mới nhất) + các fix phát sinh khi test.
> **Mục tiêu chung của dự án:** hợp nhất 2 hệ → 1 project (HRM), gộp DB (base = ERP) → migrate code ERP dần sang HRM → tắt ERP → **dọn schema (bỏ hrm_*, còn 1 bảng/thực thể)**.
>
> ⚠️ **CẬP NHẬT 2026-09-15 (bản LIVE = seeder `GopDb`, KHÔNG còn dùng `merge_prod.php`):** loại bỏ chu trình "tách-rồi-gộp-lại" thừa cho **8 bảng**. Nguồn chuẩn hiện nay là `Modules/Timesheet/Database/Seeders/GopDb/MergeProdSeeder.php`:
> - `$TACH` giảm **24 → 16** (chỉ còn bảng thực sự cần tách trung gian hoặc tách vĩnh viễn).
> - Thêm **`$APPEND` (6 bảng con của `customers`)**: `customer_activity_types, customer_business_fields, customer_contact_has_bank_accounts, customer_has_bank_accounts, customer_has_vehicle_manufacts, delivery_places` → gộp thẳng bằng cách **append id mới** (bỏ cột id, auto_increment), giữ `customer_id`. **KHÔNG tạo `hrm_*`**, không sửa code HRM (code vẫn đọc tên gốc), không sửa data FK.
> - Thêm **`$KEEP_ERP` (2 bảng)**: `nations, module_mappings` → **giữ ERP, bỏ data HRM, KHÔNG tạo `hrm_*`**. (`nations`: ERP là tập cha; Poland + remap `customers.nation_id` do `ReconcileNationsSeeder` làm. `module_mappings`: CRM tắt `use_crm=0` nên cả 2 bản đều dead.)
> - Lý do 8 bảng này KHÔNG cần tách: id đụng nhưng bảng **lá** (không FK trỏ vào) hoặc ERP là tập cha → gộp/append/giữ-ERP trong **1 lượt**, khỏi tạo `hrm_*` mồ côi rồi gộp lại. Xem phần **NHÓM 2b/2c** bên dưới.

## 4 cách xử lý (bản CHECK hiện tại)
| Nhóm | Ý nghĩa | Số bảng |
|---|---|---|
| **DÙNG CHUNG** (SHARE) | Hòa vào 1 bảng ERP + thêm cột HRM còn thiếu (INSERT IGNORE theo id) | 16 |
| **APPEND** *(2026-09-15)* | Bảng con `customers`, id đụng khác KH → **append id mới** (bỏ id), giữ `customer_id`. Không tạo `hrm_*` | 6 |
| **GIỮ ERP** (KEEP_ERP) *(2026-09-15)* | Giữ ERP nguyên, **bỏ data HRM** (ERP tập cha / CRM tắt). Không tạo `hrm_*` | 2 |
| **TÁCH** `hrm_*` | Trùng tên nhưng **khác thực thể/cấu trúc** → giữ cả 2 (ERP tên gốc, HRM `hrm_<tên>`) | ~~24~~ **16** |
| **GIỮ HRM** (KEEP_HRM) | Giữ cấu trúc+data HRM, **DROP bản ERP** (chức năng ERP dính bảng này bỏ/không dùng) | 14 |
| **LOG / framework** | Bảng Laravel chuẩn / log — dùng chung structure, data không giữ | 3 (+migrations) |

---

## NHÓM 1 — DÙNG CHUNG (16 bảng) — hòa 1 bảng
Base ERP + ALTER thêm cột HRM thiếu + union rows theo id. Cả ERP lẫn HRM đọc/ghi chung.

| Bảng | Hiện trạng | Mục tiêu cuối |
|---|---|---|
| customers, companies, departments, parts, employee_infos | Hòa 1 bảng (id khớp/cùng nghĩa, +cột HRM) | **1 bảng chung** — giữ vĩnh viễn |
| banks, bank_branches, provinces, districts, wards, hamlets, nations*(xem nhóm 2) | Hòa 1 bảng (danh mục dùng chung) | 1 bảng chung |
| customer_contacts, customer_deputies | Hòa (prod id không đụng) | 1 bảng chung |
| province_mappings, ward_mappings, moving_norms | Hòa (mapping/định mức dùng chung) | 1 bảng chung |

> ⚠️ **Lỗi phát sinh do hòa:** thêm cột HRM (`company_id`, `department_id`, `part_id`, `created_by`...) vào bảng SHARE → query ERP **join bảng SHARE dùng cột trần** bị **"Column ambiguous"** (vd `customers.company_id`). Fix: chỉ rõ prefix bảng trong query (vd `DebtReminder.php`). Sẽ còn gặp ở màn khác → vá từng chỗ.

---

## NHÓM 2 — TÁCH `hrm_*` (16 bảng — trước 2026-09-15 là 24) — giữ cả 2
Trùng tên nhưng **khác bản chất**. ERP giữ `<tên>`, HRM trỏ `hrm_<tên>` (đã sửa code HRM). Mỗi app đọc bảng của mình.
> Chỉ còn 2 loại tách: **(A) tách trung gian** — bước gộp-lại đọc thật `hrm_*` (employees + pivot, roles/permissions, files, notifications); **(B) tách vĩnh viễn** — code sống đọc thẳng `hrm_*` (groups, scopes, print_templates, settlement_contracts + employees). 8 bảng cũ đã chuyển sang APPEND/KEEP_ERP (xem NHÓM 2b/2c).

| Bảng → hrm_ | Vì sao tách | Mục tiêu cuối |
|---|---|---|
| **employees** | id gán khác nhau 2 hệ, ~21% lệch, không union deterministic | **Reconcile về 1 bảng `employees` chung** (cần thống nhất AUTH trước) → bỏ `hrm_employees` |
| company_employees, company_roles, employee_manage_departments, employee_has_roles, employee_has_permissions | pivot tổ chức/quyền theo employees | Hợp nhất **theo bước reconcile employees** → bỏ hrm_* |
| **roles, permissions, role_has_permissions** | 2 hệ auth (spatie) id đụng khác | **Thống nhất phân quyền → 1 hệ auth chung** → bỏ hrm_* |
| **files** | ERP dùng morph (fileable_type/id); HRM dùng table/table_id + cột solution | Hợp nhất về **morph ERP** (sửa code HRM + migrate data) → bỏ `hrm_files` |
| **notifications** | ERP custom (url/content/receiver_id); HRM Laravel (notifiable_type/read_at) | Hợp nhất khi thống nhất cơ chế thông báo → bỏ `hrm_notifications` (data không giữ) |
| **groups** | ERP = nhóm hàng hóa; HRM = khối tổ chức — **2 thực thể KHÁC HẲN** | **GIỮ TÁCH lâu dài** (hoặc đổi tên 1 bên cho rõ nghĩa) — KHÔNG gộp |
| ~~customer_activity_types, customer_business_fields, customer_has_bank_accounts, customer_contact_has_bank_accounts, customer_has_vehicle_manufacts, delivery_places~~ | **CHUYỂN sang APPEND (2026-09-15)** — bảng lá của `customers`, append id mới trong 1 lượt | Xem **NHÓM 2b** |
| settlement_contracts, settlement_contract_employees | **2 THỰC THỂ KHÁC HẲN**: ERP = quyết toán HĐ bán/công nợ (13k/82k) ; HRM = quyết toán công theo HĐ / PLBS của Assign (4/4) | **GIỮ TÁCH lâu dài** (tách vĩnh viễn — code đọc `hrm_*`) |
| print_templates, scopes | danh mục/template 2 hệ khác cấu trúc/nghĩa — **code sống đọc `hrm_*`** | **GIỮ TÁCH lâu dài** |
| ~~module_mappings, nations~~ | **CHUYỂN sang KEEP_ERP (2026-09-15)** — giữ ERP, bỏ data HRM, không tạo hrm_* | Xem **NHÓM 2c** |

---

## NHÓM 2b — APPEND (6 bảng, 2026-09-15) — gộp thẳng 1 lượt, KHÔNG tách
Bảng con của `customers` (khóa `customer_id`). id đụng nhưng **trỏ khách hàng KHÁC nhau** → không merge theo id. Đã verify **không bảng nào (phía HRM) trỏ FK vào** (bảng lá) nên append an toàn.
Cơ chế trong `MergeProdSeeder::$APPEND`: `INSERT INTO erp.<t> (cột trừ id) SELECT ... FROM hrm.<t>` → id do auto_increment cấp mới; giữ nguyên `customer_id`; rồi `DROP` bảng nguồn HRM.

| Bảng | ERP / HRM (dòng) | Ghi chú |
|---|---|---|
| customer_activity_types | 969 / 856 | append 856 |
| customer_business_fields | 1384 / 1245 | append 1245 |
| customer_contact_has_bank_accounts | 35 / 0 | HRM rỗng |
| customer_has_bank_accounts | 597 / 52 | append 52 |
| customer_has_vehicle_manufacts | 1307 / 144 | append 144 |
| delivery_places | 38601 / 770 | append 770 (FK vào nó chỉ từ ERP `project/service/quotations`; HRM `quotations` KHÔNG có cột `delivery_place_id`). **Có cột nhân viên** `created_by/updated_by` → xem ghi chú remap ⬇ |

> **Mục tiêu cuối:** đã là 1 bảng chung ngay sau gộp — không có `hrm_*`, không bước gộp-lại.
>
> **Remap FK nhân viên cho `delivery_places` (2026-09-15):** 5 bảng đầu chỉ có `customer_id` + id danh mục → append thẳng. Riêng `delivery_places` có `created_by/updated_by` trỏ `employees.id`. KHÔNG remap được tại B1 (nhân viên chỉ-có-HRM chưa được cấp id ERP trước ReconcileEmployees) và KHÔNG quét-remap cả bảng đã gộp (đụng dòng ERP → double-remap). Cơ chế: `MergeProdSeeder::$APPEND_EMP_COLS` ghi **mốc** `MAX(id)` trước khi append vào bảng tạm `gop_append_bounds`; `ReconcileEmployeesSeeder` Task 3b remap 2 cột **chỉ trên dòng `id>mốc`** (dòng HRM) bằng `emp_id_map` đã đầy đủ (gồm cả NV chỉ-có-HRM), rồi drop bảng mốc.

## NHÓM 2c — GIỮ ERP, DROP HRM (2 bảng, 2026-09-15) — KHÔNG tách
| Bảng | Vì sao giữ ERP | Ghi chú |
|---|---|---|
| nations | ERP 32 dòng ⊇ HRM 3 (VN/Japan/Laos). id đụng khác nước → không merge theo id | `MergeProdSeeder::$KEEP_ERP` drop `hrm_pro.nations`. `ReconcileNationsSeeder` thêm Poland + remap 7 `customers.nation_id`. Code đọc `nations`. |
| module_mappings | CRM Mate-sync bị TẮT (`use_crm=0`) → cả 2 bản dead | drop `hrm_pro.module_mappings`, giữ ERP. `DisableCrmSeeder` chỉ còn tắt cờ (bước drop hrm_ thành SKIP). Entity `Modules/CRM/ModuleMapping` (bind `hrm_module_mappings`) dead khi CRM off. |

---

## NHÓM 3 — GIỮ HRM, DROP ERP (14 bảng)
Giữ cấu trúc+data HRM; bản ERP bị bỏ. **Chức năng ERP dính các bảng này coi như bỏ/không dùng nữa** (user chốt).

| Bảng | Hiện trạng | Mục tiêu cuối |
|---|---|---|
| **quotations** | Giữ HRM (Assign báo giá). Bản ERP (báo giá cũ) DROP | HRM's là bản sống. Báo giá ERP bỏ. ⚠️ code ERP/uat_crm còn query `quotations.total_cost` (đã chết) → phải vá code (đã vá dashboard `Employee::getDashboardInfosAttribute`) |
| job_requests, job_request_employees, job_request_details | Giữ HRM (module giao việc HRM) | HRM's sống; bản ERP bỏ |
| working_positions, teams, majors, employee_incomes, areas | Giữ HRM (nhân sự HRM) | HRM's sống; bản ERP bỏ. ⚠️ ERP mất một số cột (employee_incomes 10, teams 4, areas 2) → nếu màn ERP còn dùng sẽ lỗi, vá code khi gặp |
| transport_types, moving_norm_roads, moving_norm_road_types | Giữ HRM (định mức/vận chuyển HRM) | HRM's sống; bản ERP bỏ |
| attachment_types, assign_business_tasks | Giữ HRM | HRM's sống; bản ERP bỏ |

> ⚠️ **Rủi ro nhóm này:** app ERP/uat_crm (dòng dõi ERP) nếu **còn code query bảng theo cấu trúc ERP** (cột đã mất) → crash. Cách xử lý: **vá đúng chỗ menu còn dùng** (bỏ/guard code chết), không khôi phục bảng ERP.

---

## NHÓM 4 — LOG / framework
| Bảng | Hiện trạng | Mục tiêu cuối |
|---|---|---|
| jobs, failed_jobs | Dùng chung (Cách 1): 1 bảng, phân biệt app bằng cột `queue` (ERP='erp', HRM='hrm'). Worker tách theo queue name | 1 bảng chung |
| password_resets | Bảng Laravel chuẩn, dùng chung structure ERP | 1 bảng chung |
| migrations | Union theo TÊN migration (bỏ id) | 1 bảng migrations chung |

---

## Bài học / lớp lỗi khi đưa lên server (ghi để rà tiếp)
1. **"Unknown column" (KEEP_HRM):** ERP/uat_crm query cột chỉ có ở bản ERP (đã DROP). Vd `quotations.total_cost`. → vá code chỗ menu còn dùng.
2. **"Column ambiguous" (SHARE):** bảng SHARE được thêm cột HRM (`company_id`...) → query ERP join bảng SHARE dùng cột trần bị mơ hồ. → chỉ rõ prefix bảng trong query.
3. **"Base table/Unknown column" (TÁCH sai chiều):** bảng trùng-tên-khác-cấu-trúc mà HRM-primary (files, notifications) — nếu để cấu trúc ERP thì HRM lỗi, ngược lại ERP lỗi → phải TÁCH.

## Chốt chặn để đạt "1 DB dùng chung THẬT"
1. Thống nhất **AUTH** (ERP session/SSO vs HRM JWT) — tiên quyết.
2. **Reconcile employees** → 1 bảng, bỏ hrm_employees + các pivot hrm_.
3. **Port ERP → HRM từng module**; mỗi module xong → gỡ bảng hrm_* tương ứng.
4. Tắt ERP → **drop toàn bộ hrm_*** còn lại → schema sạch.
