# Reconcile employees ERP+HRM — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development hoặc superpowers:executing-plans để chạy plan từng task. Bước dùng checkbox `- [ ]`.
> Spec đầy đủ: `design.md` cùng thư mục.

**Goal:** Gộp `employees` (ERP) + `hrm_employees` (HRM) trong DB đã merge thành **1 bảng `employees` duy nhất** (id ERP chuẩn), bằng 1 script idempotent tái chạy được, + sửa code HRM trỏ lại `employees`.

**Architecture:** 1 script PHP `reconcile_employees.php` chạy qua tinker (như `merge_prod.php`), DRY-RUN mặc định. Map id qua `employee_info_id`. Remap FK: bảng HRM-origin non-SHARE dùng map đầy đủ, bảng SHARE dùng `emp_id_map_safe` (loại 164 collision), bảng ERP không đụng. Auth giữ password/token HRM.

**Tech Stack:** PHP 7.4 / Laravel 6 (ERP TanPhatDev) chạy tinker; MySQL; schema merge `erp_hrm_check` (local) / server tương ứng.

## Global Constraints
- Script chạy trên schema ĐÃ MERGE (có cả `employees` + `hrm_employees`). Guard: `hrm_employees` không còn → skip (đã reconcile).
- `DRY_RUN=true` mặc định — chỉ in SQL + số dòng, KHÔNG thực thi. Đổi `false` mới chạy thật.
- **id ERP là chuẩn.** `emp_id_map(hrm_id→erp_id)` chỉ chứa cặp `h.id<>e.id`.
- Số kỳ vọng (local erp_hrm_check, prod tương tự): map cần đổi = **454**; `emp_id_map_safe` = **290**; collision (bỏ trên SHARE) = **164**; matched qua employee_info_id = **1085**.
- Cột HRM-only thêm vào `employees`: `tp_id, password_changed_at, rice_setting_location_id, rice_ssn, login_count`.
- SHARE (16): `bank_branches,banks,companies,customer_contacts,customer_deputies,customers,departments,districts,employee_infos,hamlets,moving_norms,parts,province_mappings,provinces,ward_mappings,wards`.
- 23 bảng TÁCH đã là `hrm_*`. Danh sách 639 bảng HRM-origin: `ERP/.plans/hop-nhat-erp-hrm/hrm-view-tables.txt`.
- **KHÔNG commit git khi chưa có yêu cầu** (quy tắc ERP).
- "Test" = chạy trên bản LOCAL copy `erp_hrm_check` + query verify (đối chiếu số kỳ vọng); KHÔNG có unit-test framework.

## File Structure
- Create: `ERP/.plans/reconcile-employees-erp-hrm/reconcile_employees.php` — script reconcile (idempotent, DRY-RUN).
- Create: `ERP/.plans/reconcile-employees-erp-hrm/run_reconcile.sh` — runner test lặp local.
- Modify (Task 7, hrm-api — undo rename bảng employees): `app/Models/TpEmployee.php`, `app/Models/Employee.php`, `Modules/Timesheet/Entities/Employee.php`, `Modules/Human/Entities/Employee.php`, + file join/prefix `hrm_employees.` (AuthNewController, EmployeeService...). **Pivot `hrm_*` GIỮ NGUYÊN.**

---

### Task 1: Scaffold script + guard + emp_id_map + emp_id_map_safe
**Files:** Create `reconcile_employees.php`.
**Produces:** `emp_id_map(hrm_id,erp_id)` (454), `emp_id_map_safe` (290); biến `$DB,$DRY_RUN,$SHARE,$TACH,$do(),$texists,$cexists,$scalar`.

- [ ] **Step 1: Viết phần đầu** (config + guard + helper + 2 bảng map)
```php
<?php
use Illuminate\Support\Facades\DB;
$DB='erp_hrm_check'; $DRY_RUN=true;
$SHARE=['bank_branches','banks','companies','customer_contacts','customer_deputies','customers','departments','districts','employee_infos','hamlets','moving_norms','parts','province_mappings','provinces','ward_mappings','wards'];
$TACH=['employees','company_employees','company_roles','customer_activity_types','customer_business_fields','customer_contact_has_bank_accounts','customer_has_bank_accounts','customer_has_vehicle_manufacts','delivery_places','employee_has_permissions','employee_has_roles','employee_manage_departments','files','groups','module_mappings','nations','notifications','permissions','print_templates','role_has_permissions','roles','scopes','settlement_contract_employees','settlement_contracts'];
$HRM_TABLES_FILE=__DIR__.'/../hop-nhat-erp-hrm/hrm-view-tables.txt';
$acts=[]; $do=function($sql) use(&$acts,$DRY_RUN){ $acts[]=$sql; if(!$DRY_RUN) DB::statement($sql); };
$scalar=function($sql){ $r=DB::select($sql); return $r?array_values((array)$r[0])[0]:null; };
$texists=function($t) use($DB,$scalar){ return $scalar("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB' AND table_name='".addslashes($t)."'")>0; };
$cexists=function($t,$c) use($DB,$scalar){ return $scalar("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='$DB' AND table_name='".addslashes($t)."' AND column_name='".addslashes($c)."'")>0; };
echo ($DRY_RUN?"[DRY-RUN] ":"[THỰC THI] ")."Reconcile employees `$DB`\n";
if (!$texists('hrm_employees')) { echo "hrm_employees không còn -> đã reconcile. SKIP.\n"; return; }
if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=0");
$do("DROP TABLE IF EXISTS `$DB`.`emp_id_map`");
$do("CREATE TABLE `$DB`.`emp_id_map` (hrm_id BIGINT PRIMARY KEY, erp_id BIGINT, INDEX(erp_id)) AS
     SELECT h.id hrm_id, e.id erp_id FROM `$DB`.`hrm_employees` h JOIN `$DB`.`employees` e ON e.employee_info_id=h.employee_info_id WHERE h.id<>e.id");
$do("DROP TABLE IF EXISTS `$DB`.`emp_id_map_safe`");
$do("CREATE TABLE `$DB`.`emp_id_map_safe` (hrm_id BIGINT PRIMARY KEY, erp_id BIGINT, INDEX(erp_id)) AS
     SELECT hrm_id,erp_id FROM `$DB`.`emp_id_map` WHERE hrm_id NOT IN (SELECT id FROM `$DB`.`employees`)");
```
- [ ] **Step 2: Verify** (đặt `$DRY_RUN=false` trên bản LOCAL copy rồi chạy tinker, query):
`SELECT (SELECT COUNT(*) FROM erp_hrm_check.emp_id_map) m,(SELECT COUNT(*) FROM erp_hrm_check.emp_id_map_safe) s;` → Expected `m=454 s=290`.

---

### Task 2: Cột HRM-only + cập nhật auth/rice (1085 khớp)
**Files:** append `reconcile_employees.php`.
- [ ] **Step 1: Append**
```php
foreach (['tp_id','password_changed_at','rice_setting_location_id','rice_ssn','login_count'] as $col) {
  if (!$cexists('employees',$col)) {
    $d=DB::select("SELECT column_type ct,is_nullable n FROM information_schema.columns WHERE table_schema='$DB' AND table_name='hrm_employees' AND column_name='$col'")[0];
    $do("ALTER TABLE `$DB`.`employees` ADD COLUMN `$col` {$d->ct} ".($d->n==='YES'?'NULL':'NOT NULL'));
  }
}
$do("UPDATE `$DB`.`employees` e JOIN `$DB`.`hrm_employees` h ON h.employee_info_id=e.employee_info_id
     SET e.password=h.password,e.token_version=h.token_version,e.password_changed_at=h.password_changed_at,
         e.tp_id=h.tp_id,e.rice_setting_location_id=h.rice_setting_location_id,e.rice_ssn=h.rice_ssn,e.login_count=h.login_count");
```
- [ ] **Step 2: Verify** — 5 cột tồn tại; spot 1 người: `employees.password`=`hrm_employees.password` (cùng employee_info_id).

---

### Task 3: Người chỉ có ở HRM → INSERT id mới + bổ sung map
**Files:** append.
- [ ] **Step 1: Append**
```php
$do("INSERT INTO `$DB`.`employees` (email,password,email_verified_at,remember_token,status,employee_info_id,created_at,updated_at,token_version,password_changed_at,tp_id,rice_setting_location_id,rice_ssn,login_count)
     SELECT h.email,h.password,h.email_verified_at,h.remember_token,h.status,h.employee_info_id,h.created_at,h.updated_at,h.token_version,h.password_changed_at,h.tp_id,h.rice_setting_location_id,h.rice_ssn,h.login_count
     FROM `$DB`.`hrm_employees` h WHERE NOT EXISTS (SELECT 1 FROM `$DB`.`employees` e WHERE e.employee_info_id=h.employee_info_id)");
$do("INSERT IGNORE INTO `$DB`.`emp_id_map` (hrm_id,erp_id)
     SELECT h.id,e.id FROM `$DB`.`hrm_employees` h JOIN `$DB`.`employees` e ON e.employee_info_id=h.employee_info_id
     WHERE h.id<>e.id AND h.id NOT IN (SELECT hrm_id FROM `$DB`.`emp_id_map`)");
```
- [ ] **Step 2: Verify** — local: employees vẫn 1085 (0 người chỉ-HRM). Mọi hrm_employee có mặt trong employees (join employee_info_id).

---

### Task 4: Enumerate cột FK cần remap (3 lớp) — CHỈ tính + IN
**Files:** append.
**Produces:** `$remap = [['table','col','mode'=>'full|safe']...]`.
- [ ] **Step 1: Append**
```php
$hrmNames=array_filter(array_map('trim',file($HRM_TABLES_FILE)));
$tachSet=array_flip($TACH); $shareSet=array_flip($SHARE); $hrmOriginMerged=[];
foreach ($hrmNames as $x){ $hrmOriginMerged[ isset($tachSet[$x])?'hrm_'.$x:$x ]=true; }
$EMP_COLS=['created_by','updated_by','employee_id','approver_id','approved_by','assigned_by','buyer_id','signer_id','receiver_id','handler_id','requester_id','reviewer_id','creator_id','manager','manager_id','deleted_by','employee_create_id','emp_id','handover_by','confirm_by','confirmed_by'];
$inList="'".implode("','",array_map('addslashes',$EMP_COLS))."'";
$cols=DB::select("SELECT table_name t,column_name c FROM information_schema.columns WHERE table_schema='$DB' AND column_name IN ($inList) AND table_name NOT IN ('employees','hrm_employees','emp_id_map','emp_id_map_safe')");
$remap=[];
foreach ($cols as $r){ if(!isset($hrmOriginMerged[$r->t]))continue; $remap[]=['table'=>$r->t,'col'=>$r->c,'mode'=>isset($shareSet[$r->t])?'safe':'full']; }
$fks=DB::select("SELECT table_name t,column_name c FROM information_schema.key_column_usage WHERE table_schema='$DB' AND referenced_table_name IN ('employees','hrm_employees')");
foreach ($fks as $r){ if(!isset($hrmOriginMerged[$r->t]))continue; $ex=false; foreach($remap as $x){if($x['table']==$r->t&&$x['col']==$r->c){$ex=true;break;}} if(!$ex)$remap[]=['table'=>$r->t,'col'=>$r->c,'mode'=>isset($shareSet[$r->t])?'safe':'full']; }
echo "\n=== CỘT SẼ REMAP (".count($remap).") ===\n"; foreach($remap as $r) echo "  [{$r['mode']}] {$r['table']}.{$r['col']}\n";
```
- [ ] **Step 2: Verify** — đọc danh sách: mọi bảng HRM-origin (không có tên bảng ERP thuần); SHARE=`safe`; hrm_*/KEEP_HRM=`full`.
- [ ] **Step 3: Rà code bổ sung `$EMP_COLS`** — grep hrm-api cột employee-ref tên lạ, thêm nếu thiếu (sót = trỏ nhầm người).

---

### Task 5: Remap FK (thực thi)
**Files:** append. **Consumes:** `$remap,emp_id_map,emp_id_map_safe`.
- [ ] **Step 1: Append**
```php
$n=0; foreach ($remap as $r){ $mt=$r['mode']==='safe'?'emp_id_map_safe':'emp_id_map';
  $do("UPDATE `$DB`.`{$r['table']}` t JOIN `$DB`.`$mt` m ON t.`{$r['col']}`=m.hrm_id SET t.`{$r['col']}`=m.erp_id"); $n++; }
echo "Đã remap $n cột.\n";
```
- [ ] **Step 2: Verify** (LOCAL, sau chạy thật): `SELECT COUNT(*) FROM erp_hrm_check.hrm_employee_has_roles x LEFT JOIN erp_hrm_check.employees e ON e.id=x.employee_id WHERE e.id IS NULL AND x.employee_id IS NOT NULL;` → `0`.

---

### Task 6: DROP hrm_employees + finalize + idempotent
**Files:** append.
- [ ] **Step 1: Append**
```php
$do("DROP TABLE `$DB`.`hrm_employees`");
$do("DROP TABLE IF EXISTS `$DB`.`emp_id_map`"); $do("DROP TABLE IF EXISTS `$DB`.`emp_id_map_safe`");
if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=1");
echo "\n=== employees=".$scalar("SELECT COUNT(*) FROM `$DB`.employees")." | hrm_employees ".($texists('hrm_employees')?'CÒN(lỗi)':'drop')." ===\n";
if ($DRY_RUN){ echo "\n[DRY-RUN] ".count($acts)." lệnh. 12 đầu:\n"; foreach(array_slice($acts,0,12) as $s)echo "  $s\n"; echo "→ \$DRY_RUN=false để chạy thật (BACKUP trước).\n"; }
```
- [ ] **Step 2: Verify** — chạy thật: employees=1085, hrm_employees drop. Chạy LẠI → in "đã reconcile. SKIP." (idempotent).

---

### Task 7: Sửa code HRM — undo rename bảng employees → `employees`
**Files (hrm-api):** 4 model `$table` + join/prefix `hrm_employees.`. KHÔNG đụng pivot `hrm_*`, model `Tp*` mysql2, config/permission.php.
- [ ] **Step 1:** Đổi `$table='hrm_employees'`→`'employees'` ở `app/Models/TpEmployee.php`, `app/Models/Employee.php`, `Modules/Timesheet/Entities/Employee.php`, `Modules/Human/Entities/Employee.php`.
- [ ] **Step 2:** `grep -rnE "'hrm_employees'|hrm_employees\." app Modules --include='*.php' | grep -v mysql2` → đổi join/prefix `hrm_employees`→`employees` (bỏ dòng mysql2, bỏ pivot `hrm_employee_has_*`).
- [ ] **Step 3: Verify** — `php -l` file sửa; grep còn sót `'hrm_employees'` (ngoài pivot) = rỗng.
- [ ] **Step 4: Smoke** — boot HRM trỏ DB đã reconcile: login JWT OK; 1 API/module OK.

---

### Task 8: Chạy trọn + verify tổng (runner tái lập)
**Files:** Create `run_reconcile.sh`.
- [ ] **Step 1:** Runner: dựng lại `erp_hrm_check` sạch (từ merge) → chạy `reconcile_employees.php` (DRY_RUN=false) → chạy query verify Task 1-6.
- [ ] **Step 2: Verify tổng:** employees=1085, hrm_employees drop; 5 NV spot-check (dòng gộp đúng, password=HRM, FK trỏ đúng người); `hrm_employee_has_roles/hrm_company_employees.employee_id` + `timesheets.created_by` không mồ côi (LEFT JOIN employees IS NULL=0); JOIN auth+phân quyền (employees→hrm_employee_has_roles→hrm_roles→hrm_permissions) ra kết quả; HRM login OK.
- [ ] **Step 3:** Chạy lại lần 2 → SKIP (idempotent).

---

## Self-Review
- **Spec coverage:** 8 bước spec ↔ Task 1-8. ✓
- **Số kỳ vọng** 454/290/164/1085 khớp verify. ✓
- **Collision:** SHARE→emp_id_map_safe(290); non-SHARE HRM→full(454) — nhất quán spec. ✓
- **Rủi ro sót cột FK:** Task 4 in danh sách + rà code trước khi remap (Task 5). ✓
- **Placeholder:** không TBD; mọi step có code/lệnh + số kỳ vọng cụ thể. ✓

---
### Checkpoint — 2026-07-30 (ĐÃ CHẠY & VERIFY TRÊN LOCAL erp_hrm_check)
Vừa hoàn thành (Inline execution, chạy thật trên local):
- Task 1 ✓ emp_id_map=454, emp_id_map_safe=290 (khớp kỳ vọng).
- Task 2 ✓ +5 cột HRM-only, password=HRM.
- Task 3 ✓ employees=1085 (local 0 người chỉ-HRM).
- Task 4 ✓ enumerate + PHÂN LOẠI: audit luôn remap; `employee_id/user_id/emp_id/executor_id` classify RUNTIME (in_emp vs in_info). Chốt LOẠI: 9 hồ sơ (attendances/salary/overtime/rice_notifications/late_early_outs...) + 3 mơ hồ (course_student_attendances, insurance_register_type_employees, rice_employee_infos) + bảng rỗng. teacher_id/examiner_id tự loại (trỏ bảng khác).
- Task 5 ✓ remap 628 cột (0 lỗi), loại 37. Verify: cột account 0 mồ côi; cột hồ sơ (attendances) giữ trỏ employee_infos.
- Task 6 ✓ drop hrm_employees; employees=1085.
- Task 7 ✓ revert 102 file HRM `hrm_employees`→`employees` (giữ pivot hrm_*/mysql2); 4 model $table='employees'; php -l sạch.
- Task 8 ✓ HRM boot trên DB reconciled: TpEmployee đọc employees=1085; login 422 (query OK, log sạch); auth join phân quyền OK.
Deliverable: `reconcile_employees.php` (runtime-classify, idempotent, DRY-RUN) — sẵn chạy server (DRY-RUN duyệt trước).
Bước tiếp: user quyết chạy trên SERVER (pipeline: merge_prod → rename hrm_* → deploy code HRM → reconcile_employees DRY-RUN → thật). CHƯA commit.
