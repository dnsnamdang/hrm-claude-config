# Gộp Auth (roles/permissions + 3 pivot) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gộp 6 bảng auth TÁCH (roles/permissions/role_has_permissions + company_roles/employee_has_roles/employee_has_permissions) về bảng gốc (giữ id HRM api, remap ERP web +OFFSET), bỏ `hrm_*`.

**Architecture:** (A) Script `reconcile_auth.php` re-runnable: ALTER cột HRM-only → remap id ERP (web) +OFFSET + remap pivot ERP → union HRM (giữ id) → drop hrm_*. (B) Revert spatie config + model + code HRM đọc `hrm_*` → tên gốc. (C) Seeder HRM: truncate → xóa scope guard=api (không phá permission web ERP).

**Tech Stack:** PHP 7.4 / Laravel `DB` facade (tinker), MySQL (schema gộp), spatie/laravel-permission. Nhánh `gop_db`.

**Spec:** `ERP/.plans/reconcile-auth-erp-hrm/design.md`

## Global Constraints

- 2 hệ auth RỜI theo `guard_name` (ERP=`web`, HRM=`api`, 0 trùng name+guard) → **UNION, KHÔNG dedup**.
- **Base = HRM (api) GIỮ id**; **ERP (web) remap id += OFFSET = 100000** (deterministic, re-runnable).
- Giữ cả 2 `model_type` (ERP `App\Employee`, HRM `Modules\Timesheet\Entities\Employee`).
- `employee_id` trong pivot đã reconcile remap (0 mồ côi) — KHÔNG remap lại.
- Script (A) tại `ERP/.plans/reconcile-auth-erp-hrm/reconcile_auth.php`, nối pipeline sau `merge_share_tables.php`. Verify trên local `erp_hrm_check` qua tinker hrm-api.
- **Chạy một lần trên bản gộp mới, backup trước khi chạy thật** (idempotent chỉ đảm bảo mức "đã gộp → SKIP"; crash giữa chừng → restore backup).
- Sau gộp: `php artisan permission:cache-reset`.
- **KHÔNG commit** khi chưa yêu cầu; code revert (B)+(C) commit gop_db khi được yêu cầu. Bỏ dòng `mysql2` khi revert.

---

### Task 1: Script `reconcile_auth.php` (DATA)

**Files:**
- Create: `ERP/.plans/reconcile-auth-erp-hrm/reconcile_auth.php`

**Interfaces:**
- Produces: chạy qua tinker; `$DRY_RUN=true` in dự kiến, `false` thực thi.

- [ ] **Step 1: Tạo script**

```php
<?php
/**
 * RECONCILE Auth ERP+HRM -> gộp roles/permissions/pivot về bảng gốc (GIỮ id HRM api).
 * 2 hệ rời theo guard (web=ERP / api=HRM) -> UNION không dedup.
 * Remap ERP (web) id += OFFSET; HRM (api) giữ id. Chạy qua tinker.
 * Idempotent mức "đã gộp": hrm_roles không còn -> SKIP. DRY_RUN mặc định.
 * CHẠY 1 LẦN trên bản gộp mới; backup trước khi chạy thật.
 */
use Illuminate\Support\Facades\DB;

// ===================== CẤU HÌNH =====================
$DB='erp_hrm_check'; $DRY_RUN=true; $OFFSET=100000;
// ====================================================

$acts=[]; $do=function($sql) use(&$acts,$DRY_RUN){ $acts[]=$sql; if(!$DRY_RUN) DB::statement($sql); };
$scalar=function($sql){ $r=DB::select($sql); return $r?array_values((array)$r[0])[0]:null; };
$texists=function($t) use($DB,$scalar){ return $scalar("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB' AND table_name='".addslashes($t)."'")>0; };
$colsOf=function($t) use($DB){ return array_map(fn($x)=>$x->cn, DB::select("SELECT column_name AS cn FROM information_schema.columns WHERE table_schema='$DB' AND table_name='".addslashes($t)."' ORDER BY ordinal_position")); };
$colDef=function($t,$c) use($DB){ return DB::select("SELECT column_type AS ct FROM information_schema.columns WHERE table_schema='$DB' AND table_name='".addslashes($t)."' AND column_name='".addslashes($c)."'")[0]; };
$clist=function($cols){ return implode(',', array_map(fn($c)=>"`$c`", $cols)); };

echo ($DRY_RUN?"[DRY-RUN] ":"[THỰC THI] ")."Reconcile Auth trên `$DB` (OFFSET=$OFFSET)\n";
if (!$texists('hrm_roles')) { echo "hrm_roles không còn -> đã gộp. SKIP.\n"; return; }
if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=0");

// Precheck FK trỏ roles/permissions.id (schema gộp vốn 0 FK)
foreach (['roles','permissions'] as $b){ $fk=$scalar("SELECT COUNT(*) FROM information_schema.key_column_usage WHERE table_schema='$DB' AND referenced_table_name='$b' AND referenced_column_name='id'"); if($fk>0) echo "  ⚠️ FK trỏ `$b`.id = $fk -> kiểm tra tay!\n"; }

// A) ALTER cột HRM-only vào entity gốc
foreach (['roles'=>'hrm_roles','permissions'=>'hrm_permissions'] as $base=>$hrm) {
    $only=array_values(array_diff($colsOf($hrm),$colsOf($base),['id']));
    echo "  [$base] cột HRM-only: ".($only?implode(',',$only):'(không)')." | ERP(web)=".$scalar("SELECT COUNT(*) FROM `$DB`.`$base`")." HRM(api)=".$scalar("SELECT COUNT(*) FROM `$DB`.`$hrm`")."\n";
    foreach ($only as $c){ $d=$colDef($hrm,$c); $do("ALTER TABLE `$DB`.`$base` ADD COLUMN `$c` {$d->ct} NULL"); }
}

// B) Remap id ERP (web) += OFFSET (guard_name='web' bảo vệ dòng HRM khỏi bị offset khi re-run)
$do("UPDATE `$DB`.`roles` SET id=id+$OFFSET WHERE guard_name='web' AND id<$OFFSET");
$do("UPDATE `$DB`.`permissions` SET id=id+$OFFSET WHERE guard_name='web' AND id<$OFFSET");

// C) Remap FK trong pivot GỐC (hiện toàn ERP) += OFFSET
$do("UPDATE `$DB`.`role_has_permissions` SET role_id=role_id+$OFFSET, permission_id=permission_id+$OFFSET WHERE role_id<$OFFSET");
$do("UPDATE `$DB`.`company_roles` SET role_id=role_id+$OFFSET WHERE role_id<$OFFSET");
$do("UPDATE `$DB`.`employee_has_roles` SET role_id=role_id+$OFFSET WHERE role_id<$OFFSET");
if ($scalar("SELECT COUNT(*) FROM `$DB`.`employee_has_permissions`")>0)
    $do("UPDATE `$DB`.`employee_has_permissions` SET permission_id=permission_id+$OFFSET WHERE permission_id<$OFFSET");

// D) Union HRM entity (giữ id)
foreach (['roles'=>'hrm_roles','permissions'=>'hrm_permissions'] as $base=>$hrm) {
    $cl=$clist($colsOf($hrm));   // gồm id -> giữ id HRM
    $do("INSERT INTO `$DB`.`$base` ($cl) SELECT $cl FROM `$DB`.`$hrm`");
}

// E) Union HRM pivot
foreach (['role_has_permissions','employee_has_roles','employee_has_permissions'] as $p) {  // no-id pivot
    if (!$texists("hrm_$p")) continue;
    $cl=$clist($colsOf("hrm_$p"));
    $do("INSERT INTO `$DB`.`$p` ($cl) SELECT $cl FROM `$DB`.`hrm_$p`");
}
$cr=$clist(array_values(array_diff($colsOf('hrm_company_roles'),['id'])));  // company_roles có id -> cấp id mới
$do("INSERT INTO `$DB`.`company_roles` ($cr) SELECT $cr FROM `$DB`.`hrm_company_roles`");

// F) DROP hrm_*
foreach (['hrm_role_has_permissions','hrm_employee_has_roles','hrm_employee_has_permissions','hrm_company_roles','hrm_roles','hrm_permissions'] as $t)
    if ($texists($t)) $do("DROP TABLE `$DB`.`$t`");

if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=1");
if ($DRY_RUN){ echo "\n--- SQL dự kiến (".count($acts)." câu) ---\n"; foreach($acts as $s) echo trim(preg_replace('/\s+/',' ',$s))."\n"; }
echo "\n".($DRY_RUN?"[DRY-RUN xong — chưa thay đổi gì]":"[ĐÃ THỰC THI xong]")."\n";
```

- [ ] **Step 2: lint + DRY-RUN**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
php -l /Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/reconcile-auth-erp-hrm/reconcile_auth.php
php artisan tinker --execute="require '/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/reconcile-auth-erp-hrm/reconcile_auth.php';" 2>&1 | grep -vE "PHP Notice"
```
Expected: `roles` HRM-only `company_id,department_id,part_id` (ERP 75 / HRM 44); `permissions` HRM-only `type,sort_order` (965/588); danh sách SQL (ALTER×5, UPDATE remap, INSERT union, DROP×6); "[DRY-RUN xong]". Không cảnh báo FK.

- [ ] **Step 3: backup + chạy thật**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
S=/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/reconcile-auth-erp-hrm/reconcile_auth.php
mysqldump -h127.0.0.1 -uroot erp_hrm_check roles hrm_roles permissions hrm_permissions role_has_permissions hrm_role_has_permissions company_roles hrm_company_roles employee_has_roles hrm_employee_has_roles employee_has_permissions hrm_employee_has_permissions > "$CLAUDE_JOB_DIR/tmp/auth_backup.sql"
sed -i '' 's/\$DRY_RUN=true;/\$DRY_RUN=false;/' "$S"
php artisan tinker --execute="require '$S';" 2>&1 | grep -vE "PHP Notice"
sed -i '' 's/\$DRY_RUN=false;/\$DRY_RUN=true;/' "$S"
```
Expected: "[ĐÃ THỰC THI xong]".

- [ ] **Step 4: verify DATA + idempotent**

```bash
php artisan tinker --execute='
foreach(["roles"=>119,"permissions"=>1553] as $t=>$exp){
  $c=DB::table($t)->count();
  $g=DB::table($t)->select("guard_name",DB::raw("COUNT(*) n"))->groupBy("guard_name")->pluck("n","guard_name")->toArray();
  echo "$t: rows=$c (kỳ vọng ~$exp) guard=".json_encode($g)."\n";
}
$o1=DB::select("SELECT COUNT(*) c FROM role_has_permissions rp LEFT JOIN roles r ON r.id=rp.role_id WHERE r.id IS NULL")[0]->c;
$o2=DB::select("SELECT COUNT(*) c FROM role_has_permissions rp LEFT JOIN permissions p ON p.id=rp.permission_id WHERE p.id IS NULL")[0]->c;
$o3=DB::select("SELECT COUNT(*) c FROM employee_has_roles er LEFT JOIN roles r ON r.id=er.role_id WHERE r.id IS NULL")[0]->c;
$o4=DB::select("SELECT COUNT(*) c FROM employee_has_roles er LEFT JOIN employees e ON e.id=er.employee_id WHERE e.id IS NULL")[0]->c;
echo "orphan: rhp.role_id=$o1 rhp.perm_id=$o2 ehr.role_id=$o3 ehr.employee_id=$o4\n";
foreach(["hrm_roles","hrm_permissions","hrm_role_has_permissions","hrm_employee_has_roles","hrm_company_roles","hrm_employee_has_permissions"] as $h)
  echo "$h: ".(DB::select("SELECT COUNT(*) c FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name=?",[$h])[0]->c?"CÒN":"drop")." ";
echo "\n";
' 2>&1 | grep -vE "PHP Notice"
php artisan tinker --execute="require '/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/reconcile-auth-erp-hrm/reconcile_auth.php';" 2>&1 | grep -E "SKIP"
```
Expected: `roles` ≈119 (guard web 75 + api 44), `permissions` ≈1553 (web 965 + api 588); tất cả orphan = **0**; 6 bảng hrm_ = **drop**; re-run in "đã gộp. SKIP.".

---

### Task 2: Revert spatie config + model + code HRM

**Files:**
- Modify: `HRM/hrm-api/config/permission.php` (5 table_names)
- Modify: `HRM/hrm-api/app/Models/Role.php`, `app/Models/Permission.php`, `app/Models/EmployeeHasRole.php`, `Modules/Timesheet/Entities/CompanyRole.php` (`$table`)
- Modify: các file code còn ref (bỏ mysql2) — `app/CommonServices/PermissionService.php`, `app/Http/Controllers/Api/AuthNewController.php`, `app/Helper/PermissionHelper.php`, `app/Console/Commands/Assign/NotifyRequestSolutionDeadlineCommand.php`, `Modules/Assign/Http/Controllers/Api/V1/RequestSolutionController.php`, `Modules/Assign/Services/HandoverService.php`, `Modules/Timesheet/Http/Requests/BulkPermissionApplyRequest.php`, `Modules/Timesheet/Services/{BulkPermissionService,EmployeeInfoService,EmployeeService,RoleService}.php`, `Modules/Timesheet/Entities/Company.php`

**Interfaces:**
- Consumes: bảng gốc đã gộp (Task 1), guard `api` = tập HRM.

- [ ] **Step 1: Sửa spatie config** `config/permission.php` — đổi 5 dòng table_names bỏ `hrm_`:
```php
'roles' => 'roles',
'permissions' => 'permissions',
'model_has_permissions' => 'employee_has_permissions',
'model_has_roles' => 'employee_has_roles',
'role_has_permissions' => 'role_has_permissions',
```
(giữ `'model_morph_key' => 'employee_id'`.)

- [ ] **Step 2: Đổi `$table` 4 model** — bỏ `hrm_`:
- `app/Models/Role.php`: `'hrm_roles'` → `'roles'`
- `app/Models/Permission.php`: `'hrm_permissions'` → `'permissions'`
- `app/Models/EmployeeHasRole.php`: `'hrm_employee_has_roles'` → `'employee_has_roles'`
- `Modules/Timesheet/Entities/CompanyRole.php`: `'hrm_company_roles'` → `'company_roles'`

- [ ] **Step 3: Đổi ref chuỗi còn lại (bỏ mysql2)**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
grep -rlE "hrm_roles|hrm_permissions|hrm_role_has_permissions|hrm_employee_has_roles|hrm_company_roles|hrm_employee_has_permissions" app Modules 2>/dev/null | grep -v mysql2 | while read f; do
  perl -i -pe 's/hrm_role_has_permissions/role_has_permissions/g; s/hrm_employee_has_roles/employee_has_roles/g; s/hrm_employee_has_permissions/employee_has_permissions/g; s/hrm_company_roles/company_roles/g; s/hrm_roles/roles/g; s/hrm_permissions/permissions/g' "$f"
done
```
(Thứ tự perl: token dài trước token ngắn để tránh thay lồng — `hrm_role_has_permissions` trước `hrm_roles`.)

- [ ] **Step 4: verify lint + grep sạch + cache reset**

```bash
grep -rnE "hrm_roles|hrm_permissions|hrm_role_has_permissions|hrm_employee_has_roles|hrm_company_roles|hrm_employee_has_permissions" app Modules config 2>/dev/null | grep -v mysql2 || echo "(sạch)"
for f in config/permission.php app/Models/Role.php app/Models/Permission.php app/Models/EmployeeHasRole.php Modules/Timesheet/Entities/CompanyRole.php app/CommonServices/PermissionService.php app/Http/Controllers/Api/AuthNewController.php app/Helper/PermissionHelper.php Modules/Timesheet/Services/BulkPermissionService.php Modules/Timesheet/Services/EmployeeInfoService.php Modules/Timesheet/Services/EmployeeService.php Modules/Timesheet/Services/RoleService.php Modules/Timesheet/Entities/Company.php; do php -l "$f" >/dev/null 2>&1 && echo "OK $f" || php -l "$f"; done
php artisan permission:cache-reset
```
Expected: grep "(sạch)"; tất cả php -l OK; cache reset thành công.

- [ ] **Step 5: verify runtime auth**

```bash
php artisan tinker --execute='
$e=\Modules\Human\Entities\Employee::whereHas("roles")->first();
if($e){ echo "employee {$e->id} roles(api): ".$e->getRoleNames()->implode(",")."\n"; echo "permissions count: ".$e->getAllPermissions()->count()."\n"; }
else echo "không có employee gắn role\n";
' 2>&1 | grep -vE "PHP Notice"
```
Expected: 1 employee HRM trả về role api + số permission > 0 (spatie đọc `roles`/`permissions` guard api đúng, không lỗi "Base table hrm_* doesn't exist").

---

### Task 3: Seeder HRM — không truncate bảng gộp

**Files:**
- Modify: `HRM/hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:35`

**Interfaces:**
- Consumes: bảng `permissions` gộp (web ERP id≥OFFSET + api HRM).

- [ ] **Step 1: Đổi truncate → xóa scope guard=api**

Dòng 35 hiện: `DB::table('hrm_permissions')->truncate();`
→ đổi thành:
```php
DB::table('permissions')->where('guard_name', 'api')->delete();
```
(Chỉ xóa permission `api` để re-tạo; **không đụng** permission `web` của ERP. Các `Permission::create(['id'=>..,'guard_name'=>'api',..])` bên dưới ghi vào `permissions` qua model đã revert — không PK-conflict vì đã xóa api trước.)

- [ ] **Step 2: verify**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
php -l Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
php artisan db:seed --class="Modules\\Timesheet\\Database\\Seeders\\PermissionsTableSeeder" --force 2>&1 | tail -3
php artisan tinker --execute='
echo "permissions web (ERP): ".\App\Models\Permission::where("guard_name","web")->count()."\n";
echo "permissions api (HRM): ".\App\Models\Permission::where("guard_name","api")->count()."\n";
' 2>&1 | grep -vE "PHP Notice"
```
Expected: php -l OK; seed chạy không lỗi; sau seed **web vẫn = 965** (không bị xóa), api ≈ 588 (re-tạo). `permission:cache-reset` sau seed nếu cần.

---

## Verify tổng thể

- `roles`/`permissions` = union 2 guard (web id≥OFFSET, api id gốc); pivot không orphan; `hrm_*` (6 bảng) drop; re-run script → SKIP.
- HRM auth (guard api) hoạt động y trước gộp (role/permission của user đúng); ERP auth (web) không đụng.
- Seeder HRM re-run không xóa permission web ERP.
- Pipeline: `... → merge_share_tables.php → reconcile_auth.php`.

## Checkpoint — 2026-07-31 (ĐÃ CHẠY & VERIFY TRÊN LOCAL erp_hrm_check)
Vừa hoàn thành: cả 3 task (inline).
- Task 1: `reconcile_auth.php` DRY-RUN → backup 12 bảng → chạy thật → verify. roles=119 (web75+api44), permissions=1553 (web965+api588), guard đúng, hrm_ (6 bảng) drop, idempotent SKIP. Orphan (rhp.perm 972, rhp.role 7, ehr.emp 13, cr.role 8) = **PRE-EXISTING** (khớp chính xác backup, merge thêm 0 orphan).
- Task 2: revert config/permission.php (5 table_names) + 4 model $table + ~14 file refs (1 lượt perl, bỏ mysql2). php -l sạch, grep sạch. Runtime auth OK: `Modules\Timesheet\Entities\Employee` (model spatie, KHÔNG phải Human) → roles/permissions đọc bảng gộp guard api đúng. `permission:cache-reset` local báo "Unable to flush cache" = env (cache backend không chạy local), sẽ OK trên server.
- Task 3: seeder dòng 35 `truncate` → `->where('guard_name','api')->delete()`. Chạy seeder: web=965 GIỮ NGUYÊN, api 588→590.
Đang làm dở: (không) — code revert (Task2+3) CHƯA commit gop_db.
Bước tiếp theo (user): commit code revert lên gop_db; chạy reconcile_auth.php + permission:cache-reset trên môi trường gộp khác khi cần.
Blocked:
