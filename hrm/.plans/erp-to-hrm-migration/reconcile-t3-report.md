# Báo cáo đối chiếu bất đồng bộ T3 (lõi tổ chức) — ERP ↔ HRM

> Chạy trên **DB production đã kéo về local** (2026-07-27).
> HRM=`hrm_tpe`, ERP=`erp2326`, cùng 127.0.0.1:3306. Đối chiếu chéo bằng SQL trực tiếp (tinker không boot do merge conflict `Modules/Accounting/module.json`).
> Xác nhận là DB production: đã hết bản test kiểu "Công ty test"/tax_code null (chỉ còn 1 sót ở ERP — xem departments).

## Kết luận đầu (headline)

**T3 gần như đã đồng bộ hoàn toàn theo id.** Điểm bất đồng bộ DUY NHẤT cần bảng ánh xạ id là bảng **`employees`** (454/1085 bản lệch id, dù trùng 100% qua email). Các entity còn lại (`companies`, `departments`, `parts`, `employee_infos`) đều **id-aligned 1:1** → merge = retire copy ERP, KHÔNG cần remap. Chỉ cần drop 3 bản orphan ở `departments` ERP.

Hệ quả lớn: mọi FK `employee_id` ở phía ERP (2 pivot T3 + toàn bộ nghiệp vụ 4 mảng migrate) phải remap qua **id-map 454 dòng** khi bê sang HRM canonical. FK `company_id`/`department_id`/`part_id` KHÔNG cần remap (id đã trùng).

## Bảng tổng hợp T3

| Bảng | HRM | ERP | Key hiệu quả | Trạng thái | Hành động khi merge |
|---|---:|---:|---|---|---|
| `companies` | 8 | 8 | **id** (tax_code có DUP) | id-aligned 1:1, khớp name+tax_code | Không remap |
| `departments` | 84 | 87 | **id** (code không unique) | HRM ⊆ ERP theo id (0 lệch code cùng id); ERP dư 3 | Drop 3 orphan ERP; không remap 84 |
| `parts` | 25 | 25 | **id** (name có 3 DUP) | id-aligned hoàn hảo | Không remap |
| `employee_infos` | 1101 | 1101 | **id** (code cũng unique) | id-aligned hoàn hảo, 0 lệch | Không remap |
| `employees` | 1085 | 1085 | **email** (unique, không null) | Match 100% qua email; **631 trùng id / 454 LỆCH id** | **Bảng ánh xạ id (454)** → remap mọi FK employee_id ERP |
| `employee_incomes` | 0 | 0 | — | rỗng cả 2 | — |
| `teams` | 0 | 0 | — | rỗng cả 2 | — |
| `working_positions` | 296 | 0 | — | HRM-only (ERP không dùng) | Giữ HRM |
| `company_employees` | 1104 | 1008 | pivot (employee_id, company_id) | FK employee_id → cần remap; count lệch | Remap employee_id + dedupe/rebuild |
| `employee_manage_departments` | 235 | 126 | pivot (employee_id, department_id, company_id) | FK employee_id → cần remap; count lệch | Remap + dedupe/rebuild |

## Chi tiết từng phát hiện

### companies — đồng bộ, KHÔNG remap
- 8/8, id 1..8 khớp tuyệt đối name + tax_code.
- ⚠️ **tax_code KHÔNG unique**: UPSERVICE (id 6) và ETEK Group (id 8) cùng `0108281564` (lỗi data, giống hệt cả 2 DB). ⇒ **KHÔNG dùng tax_code làm natural key** — dùng `id` (đã align).

### departments — id-aligned, dư 3 orphan phía ERP
- 0 bản cùng id mà code khác ⇒ id-aligned.
- 0 HRM-only. ERP dư 3 bản (file `orphans-departments-erp.csv`):
  - id **112** `TEST5` "Phòng ban test 2" ← **bản test còn sót ở ERP**
  - id **113** `TTDT` "Trung tâm đào tạo" ← ERP-only, không match HRM qua code
  - id **123** `TTDT` "Trung tâm đào tạo" ← trùng lặp
- code không unique (`SG_NSHC`×2 cả 2 bên, `TTDT`×3 ERP) ⇒ key = **id**, không phải code.

### parts / employee_infos — đồng bộ hoàn hảo
- parts 25/25, employee_infos 1101/1101: 0 lệch, 0 dư 2 bên, id-aligned. Không cần xử lý.

### employees — ĐIỂM BẤT ĐỒNG BỘ CHÍNH
- email là key tin cậy: unique, không null cả 2 bên; match 100% (0 HRM-only, 0 ERP-only).
- **454/1085 bản lệch id** giữa 2 DB → file **`idmap-employees-drift.csv`** (`email,hrm_id,erp_id`).
- 631 bản trùng id (identity map).
- ⚠️ 1 bản email dính dấu `'` đầu chuỗi (`'huongttt.kddau@...`) — lỗi nhập liệu, vẫn khớp cả 2 DB.
- ⚠️ id đụng độ: 164 bản CÙNG id nhưng KHÁC email (2 người khác nhau chung id) ⇒ **tuyệt đối không merge employees theo id**, phải theo email.

### Pivot T3 (company_employees, employee_manage_departments)
- Đều tham chiếu `employee_id` → khi bê ERP sang phải remap qua id-map. Count lệch (HRM nhiều hơn) là do HRM là bản đầy hơn ⇒ khi merge rebuild/dedupe, không phải "mất data".

## File deliverable (cùng thư mục)
- `idmap-employees-drift.csv` — 454 dòng `email,hrm_id,erp_id` → đầu vào bảng ánh xạ id merge T3.
- `orphans-departments-erp.csv` — 3 dòng orphan ERP cần drop/xử lý.

## Xác minh cơ chế sync trong code (đã chốt field mapping)

Sync realtime **một chiều HRM→ERP**, chạy inline trong `boot()` Entity HRM (KHÔNG qua Observer/EventServiceProvider), gate bởi `MasterSetting category='use_erp'`. Ghi sang ERP qua model `Tp*` (`$connection='mysql2'`).

| Bảng | Nơi sync | KEY match ERP | Khớp số liệu |
|---|---|---|---|
| companies | `Modules/Human/Entities/Company.php:31-122` | **giữ nguyên `id`** (`TpCompany::find($model->id)`) | ✅ id-aligned |
| departments | `Department.php:27-105` | **giữ nguyên `id`** | ✅ id-aligned |
| parts | `Part.php:76-117` (`static::saved`) | **giữ nguyên `id`** | ✅ id-aligned |
| employee_infos | `EmployeeInfo.php:63-140` → `Jobs/SyncEmployeeInfoToErpJob.php` | **giữ nguyên `id`** | ✅ id-aligned |
| **employees** | `Employee.php:33-88` → `Jobs/SyncEmployeeToErpJob.php:39` | **`employee_info_id`** (KHÔNG theo id) | ✅ giải thích 454 lệch id |
| teams | `Team.php` | KHÔNG sync | ✅ rỗng |
| working_positions | `WorkingPosition.php` | KHÔNG sync mysql2 (chỉ Rice/CRM) | ✅ 296/0 |
| employee_incomes | — | KHÔNG sync | ✅ rỗng |
| company_employees | `CompanyEmployee.php` boot **bị comment** | KHÔNG sync | ✅ count lệch |
| employee_manage_departments | — | KHÔNG sync | ✅ count lệch |

**Chốt then chốt:** 4 entity (companies/departments/parts/employee_infos) sync bằng identity id ⇒ **erp_id = hrm_id**, không cần remap. Riêng **employees** sync match theo `employee_info_id` nên id ERP tự tăng độc lập ⇒ **454 bản lệch id** — đây là bảng DUY NHẤT cần ánh xạ id. Kiểm chứng chéo: map theo `email` và theo `employee_info_id` cho kết quả **trùng khít 100%** (0 mismatch), id-map vững chắc.

> Bảng `module_mappings` (trong ERP `mysql2`, model `TpModuleMapping`) code luôn gán `erp_id = hrm_id` (identity) ⇒ KHÔNG dùng được để tra id ERP thật của employees. Phải dùng id-map đối chiếu theo `employee_info_id` này.
>
> Ngoài luồng realtime còn có command patch/đối soát: `app/Console/Commands/SyncDataEmployee*.php`, `CheckEmployeeStatusDiff.php` (một chiều, không phải luồng chính).

## Còn treo
- [x] Xác minh cơ chế sync HRM→ERP trong code để chốt field mapping — DONE (bảng trên).
- [ ] Quyết cách xử 3 orphan departments ERP (drop TEST5; gộp/loại 2 TTDT).
- [ ] Mở rộng đối chiếu sang T4 (customers…) khi tới phase domain.
