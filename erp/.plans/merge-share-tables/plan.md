# Gộp SHARE tables — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote 2 pivot `company_employees` + `employee_manage_departments` từ TÁCH `hrm_*` → SHARE 1 bảng, bằng 1 engine re-runnable dùng lại cho các bảng SHARE sau.

**Architecture:** (A) Script PHP idempotent `merge_share_tables.php` (config `$TABLES`) chạy qua tinker trên schema đã gộp: mỗi bảng ALTER thêm cột HRM-only → UNION+dedup theo key tự nhiên (HRM thắng cột riêng) → cấp id mới cho dòng chỉ-HRM → DROP `hrm_*`. (B) Revert code HRM đọc `hrm_*` → tên gốc.

**Tech Stack:** PHP 7.4 / Laravel `DB` facade (chạy qua `php artisan tinker`), MySQL (schema gộp). Nhánh `gop_db`.

**Spec:** `ERP/.plans/merge-share-tables/design.md`

## Global Constraints

- Script (A) đặt tại `ERP/.plans/merge-share-tables/merge_share_tables.php`, nối pipeline sau `reconcile_employees.php`.
- **Idempotent:** mỗi bảng, nếu `hrm_<base>` không tồn tại → SKIP. `$DRY_RUN=true` mặc định (chỉ IN, không chạy).
- **Verify chạy trên DB gộp local `erp_hrm_check`** qua tinker của `hrm-api` (`.env` DB_DATABASE=erp_hrm_check, default connection tới schema này).
- **UNION + dedup theo key tự nhiên**; cặp trùng → HRM thắng cột HRM-only; dòng chỉ-HRM → INSERT **id mới** (không bê id hrm_).
- **KHÔNG commit** khi user chưa yêu cầu. Script (A) là artifact re-runnable (không commit code app); code revert (B) commit `gop_db` khi được yêu cầu.
- Code revert HRM: **bỏ qua dòng `mysql2`** (TpEmployee = ERP cũ).
- `employee_id` trong 2 pivot ĐÃ được reconcile remap — task này KHÔNG remap lại.

---

### Task 1: Engine `merge_share_tables.php` (DATA merge, re-runnable)

**Files:**
- Create: `ERP/.plans/merge-share-tables/merge_share_tables.php`

**Interfaces:**
- Produces: script chạy qua `php artisan tinker --execute="require '<path>';"` — với `$DRY_RUN=true` in dự kiến; `$DRY_RUN=false` thực thi (ALTER + UPDATE + INSERT + DROP hrm_).

- [ ] **Step 1: Tạo script `merge_share_tables.php`**

```php
<?php
/**
 * MERGE SHARE tables ERP+HRM -> 1 bảng (base ERP), UNION+dedup theo key tự nhiên.
 * Chạy trên schema ĐÃ MERGE, qua tinker (hrm-api, default conn = schema gộp):
 *   php artisan tinker --execute="require '.../merge_share_tables.php';"
 * Idempotent per-table: hrm_<base> không còn -> SKIP. DRY_RUN=true mặc định.
 * Cặp trùng key -> HRM thắng cột HRM-only (MAX(id)/key). Dòng chỉ-HRM -> INSERT id mới.
 * Batch sau: chỉ thêm dòng vào $TABLES.
 */
use Illuminate\Support\Facades\DB;

// ===================== CẤU HÌNH =====================
$DB      = 'erp_hrm_check';   // schema đã merge (SERVER: đổi cho đúng)
$DRY_RUN = true;              // true = chỉ IN, KHÔNG chạy
$TABLES = [
  ['base'=>'company_employees',           'hrm'=>'hrm_company_employees',           'key'=>['company_id','employee_id']],
  ['base'=>'employee_manage_departments', 'hrm'=>'hrm_employee_manage_departments', 'key'=>['employee_id','department_id','company_id']],
];
// ====================================================

$acts=[]; $do=function($sql) use(&$acts,$DRY_RUN){ $acts[]=$sql; if(!$DRY_RUN) DB::statement($sql); };
$scalar=function($sql){ $r=DB::select($sql); return $r?array_values((array)$r[0])[0]:null; };
$texists=function($t) use($DB,$scalar){ return $scalar("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB' AND table_name='".addslashes($t)."'")>0; };
$colsOf=function($t) use($DB){ return array_map(fn($x)=>$x->cn, DB::select("SELECT column_name AS cn FROM information_schema.columns WHERE table_schema='$DB' AND table_name='".addslashes($t)."' ORDER BY ordinal_position")); };
$colDef=function($t,$c) use($DB){ return DB::select("SELECT column_type ct, is_nullable n FROM information_schema.columns WHERE table_schema='$DB' AND table_name='".addslashes($t)."' AND column_name='".addslashes($c)."'")[0]; };

echo ($DRY_RUN?"[DRY-RUN] ":"[THỰC THI] ")."Merge SHARE tables trên `$DB`\n";
if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=0");

foreach ($TABLES as $t) {
    $base=$t['base']; $hrm=$t['hrm']; $key=$t['key'];
    echo "\n=== $base <= $hrm (key: ".implode('+',$key).") ===\n";
    if (!$texists($base)) { echo "  base `$base` không tồn tại -> SKIP.\n"; continue; }
    if (!$texists($hrm))  { echo "  `$hrm` không còn -> đã gộp. SKIP.\n"; continue; }

    // Precheck leaf: cảnh báo nếu có FK constraint trỏ tới base(id) (schema gộp vốn 0 FK -> kỳ vọng rỗng)
    $fk=$scalar("SELECT COUNT(*) FROM information_schema.key_column_usage WHERE table_schema='$DB' AND referenced_table_name='".addslashes($base)."' AND referenced_column_name='id'");
    if ($fk>0) echo "  ⚠️ CẢNH BÁO: có $fk FK trỏ `$base`.id -> cấp id mới có thể ảnh hưởng, kiểm tra tay!\n";

    $keyCols = implode(',', array_map(fn($k)=>"`$k`", $key));
    $onKey   = implode(' AND ', array_map(fn($k)=>"b.`$k`=h.`$k`", $key));

    // (2) cột HRM-only = cols(hrm) - cols(base) - id
    $baseCols=$colsOf($base); $hrmCols=$colsOf($hrm);
    $hrmOnly=array_values(array_diff($hrmCols,$baseCols,['id']));
    echo "  cột HRM-only: ".($hrmOnly?implode(',',$hrmOnly):'(không)')."\n";
    foreach ($hrmOnly as $c) { $d=$colDef($hrm,$c); $do("ALTER TABLE `$DB`.`$base` ADD COLUMN `$c` {$d->ct} NULL"); }

    // Preview số liệu (read-only, luôn chạy)
    $dupCnt=$scalar("SELECT COUNT(*) FROM (SELECT $keyCols FROM `$DB`.`$hrm` GROUP BY $keyCols) h WHERE EXISTS (SELECT 1 FROM `$DB`.`$base` b WHERE $onKey)");
    $newCnt=$scalar("SELECT COUNT(*) FROM (SELECT $keyCols FROM `$DB`.`$hrm` GROUP BY $keyCols) h WHERE NOT EXISTS (SELECT 1 FROM `$DB`.`$base` b WHERE $onKey)");
    echo "  cặp trùng key (UPDATE cột HRM-only): $dupCnt | dòng chỉ-HRM (INSERT id mới): $newCnt\n";

    // dòng hrm đại diện mỗi key = MAX(id)
    $hrmPick="(SELECT h0.* FROM `$DB`.`$hrm` h0 JOIN (SELECT $keyCols, MAX(id) mid FROM `$DB`.`$hrm` GROUP BY $keyCols) m ON h0.id=m.mid)";

    // (3) cặp trùng key -> HRM thắng cột HRM-only
    if ($hrmOnly) {
        $setCols=implode(', ', array_map(fn($c)=>"b.`$c`=h.`$c`", $hrmOnly));
        $do("UPDATE `$DB`.`$base` b JOIN $hrmPick h ON $onKey SET $setCols");
    }

    // (4) dòng chỉ-HRM -> INSERT (id auto mới)
    $insCols=array_values(array_diff($hrmCols,['id']));
    $colList=implode(',', array_map(fn($c)=>"`$c`", $insCols));
    $do("INSERT INTO `$DB`.`$base` ($colList)
         SELECT $colList FROM $hrmPick h
         WHERE NOT EXISTS (SELECT 1 FROM `$DB`.`$base` b WHERE $onKey)");

    // (5) DROP hrm_
    $do("DROP TABLE `$DB`.`$hrm`");
}

if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=1");
if ($DRY_RUN) { echo "\n--- SQL dự kiến (".count($acts)." câu) ---\n"; foreach($acts as $s) echo trim(preg_replace('/\s+/',' ',$s))."\n"; }
echo "\n".($DRY_RUN?"[DRY-RUN xong — chưa thay đổi gì]":"[ĐÃ THỰC THI xong]")."\n";
```

- [ ] **Step 2: DRY-RUN + review (trên `erp_hrm_check`)**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
php artisan tinker --execute="require '/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/merge-share-tables/merge_share_tables.php';"
```
Expected: in cột HRM-only (`type,all_department` cho company_employees; `part_ids` cho employee_manage_departments), số cặp trùng ≈ 958 / 52, số chỉ-HRM ≈ 146 / 183, danh sách SQL dự kiến; kết thúc "[DRY-RUN xong — chưa thay đổi gì]". Không cảnh báo FK (⚠️).

- [ ] **Step 3: Backup 2 cặp bảng (để re-test nếu cần) + chạy THẬT**

```bash
# backup 4 bảng trước khi chạy thật
mysqldump -h127.0.0.1 -uroot erp_hrm_check company_employees hrm_company_employees employee_manage_departments hrm_employee_manage_departments > "$CLAUDE_JOB_DIR/tmp/merge_pivots_backup.sql"
# đổi DRY_RUN=false trong script rồi chạy
sed -i '' "s/\$DRY_RUN = true;/\$DRY_RUN = false;/" /Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/merge-share-tables/merge_share_tables.php
php artisan tinker --execute="require '/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/merge-share-tables/merge_share_tables.php';"
# đặt lại DRY_RUN=true (mặc định an toàn cho lần sau)
sed -i '' "s/\$DRY_RUN = false;/\$DRY_RUN = true;/" /Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/merge-share-tables/merge_share_tables.php
```
Expected: "[ĐÃ THỰC THI xong]".

- [ ] **Step 4: Verify DATA + idempotent**

```bash
php artisan tinker --execute='
foreach ([["company_employees",["company_id","employee_id"]],["employee_manage_departments",["employee_id","department_id","company_id"]]] as $p) {
  [$t,$k]=$p;
  $g=implode(",",array_map(fn($c)=>"`$c`",$k));
  $dup=DB::select("SELECT COUNT(*) c FROM (SELECT $g, COUNT(*) n FROM `$t` GROUP BY $g HAVING n>1) x")[0]->c;
  $orphan=DB::select("SELECT COUNT(*) c FROM `$t` t LEFT JOIN employees e ON e.id=t.employee_id WHERE t.employee_id IS NOT NULL AND e.id IS NULL")[0]->c;
  $hrmGone=DB::select("SELECT COUNT(*) c FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name=?",["hrm_$t"])[0]->c;
  echo "$t: rows=".DB::table($t)->count().", cặp key lặp=$dup, employee_id mồ côi=$orphan, hrm_$t còn=".($hrmGone?"CÒN":"đã drop")."\n";
}
'
# idempotent: chạy lại DRY-RUN -> phải SKIP cả 2 (hrm_ đã drop)
php artisan tinker --execute="require '/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/merge-share-tables/merge_share_tables.php';"
```
Expected: mỗi bảng — cặp key lặp = **0**, employee_id mồ côi = **0**, `hrm_*` = **đã drop**; lần chạy lại in "đã gộp. SKIP." cho cả 2.

---

### Task 2: Revert code HRM đọc bảng gốc (không còn `hrm_*`)

**Files:**
- Modify: `HRM/hrm-api/app/Models/CompanyEmployee.php` (`$table`)
- Modify: `HRM/hrm-api/app/Models/EmployeeManageDepartment.php` (`$table`)
- Modify: `HRM/hrm-api/Modules/Human/Entities/CompanyEmployee.php` (`$table`)
- Modify: `HRM/hrm-api/Modules/Timesheet/Entities/EmployeeManageDepartment.php` (`$table`)
- Modify: các file còn tham chiếu chuỗi (query/relation): `app/Models/Employee.php`, `Modules/Human/Entities/{Employee,EmployeeInfo,Department}.php`, `Modules/Assign/Services/QuotationService.php`, `Modules/Timesheet/Services/EmployeeService.php`

**Interfaces:**
- Consumes: bảng đã gộp `company_employees`/`employee_manage_departments` (Task 1) với đủ cột HRM-only.
- Produces: HRM đọc thẳng bảng gốc.

- [ ] **Step 1: Đổi `$table` ở 4 model**

Trong 4 file model, đổi:
- `protected $table = 'hrm_company_employees';` → `protected $table = 'company_employees';`
- `protected $table = 'hrm_employee_manage_departments';` → `protected $table = 'employee_manage_departments';`

- [ ] **Step 2: Đổi tham chiếu chuỗi còn lại (bỏ mysql2)**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
grep -rnE "hrm_company_employees|hrm_employee_manage_departments" app Modules | grep -v mysql2
```
Với từng dòng match (join/relation/whereRaw…) đổi `hrm_company_employees`→`company_employees`, `hrm_employee_manage_departments`→`employee_manage_departments`. **KHÔNG đụng** dòng trong `app/Models/TpEmployee.php` hay bất kỳ dòng nào cạnh `->connection('mysql2')`/`$connection='mysql2'`.

- [ ] **Step 3: Verify lint + grep sạch**

```bash
for f in app/Models/CompanyEmployee.php app/Models/EmployeeManageDepartment.php Modules/Human/Entities/CompanyEmployee.php Modules/Timesheet/Entities/EmployeeManageDepartment.php app/Models/Employee.php Modules/Human/Entities/Employee.php Modules/Human/Entities/EmployeeInfo.php Modules/Human/Entities/Department.php Modules/Assign/Services/QuotationService.php Modules/Timesheet/Services/EmployeeService.php; do php -l "$f"; done
echo "=== còn sót (ngoài mysql2)? ==="
grep -rnE "hrm_company_employees|hrm_employee_manage_departments" app Modules | grep -v mysql2
```
Expected: tất cả "No syntax errors"; grep còn sót = **rỗng**.

- [ ] **Step 4: Verify runtime (DB gộp erp_hrm_check)**

```bash
php artisan tinker --execute='
echo "CompanyEmployee(app): ".\App\Models\CompanyEmployee::count()."\n";
echo "CompanyEmployee(Human): ".\Modules\Human\Entities\CompanyEmployee::count()."\n";
echo "EmployeeManageDepartment(app): ".\App\Models\EmployeeManageDepartment::count()."\n";
echo "EmployeeManageDepartment(Timesheet): ".\Modules\Timesheet\Entities\EmployeeManageDepartment::count()."\n";
'
```
Expected: cả 4 model trả về count của bảng đã gộp (khớp Task 1), không lỗi "Base table hrm_* doesn't exist".

---

## Verify tổng thể

- `hrm_company_employees` + `hrm_employee_manage_departments` đã drop; 2 bảng gốc = union dedup, không cặp key lặp, không employee_id mồ côi.
- HRM code đọc bảng gốc (4 model + ref) — `php -l` sạch, grep sạch, tinker count OK.
- Chạy lại `merge_share_tables.php` (DRY-RUN) → SKIP cả 2 (idempotent).
- Engine sẵn sàng nhận batch SHARE sau (chỉ thêm dòng `$TABLES`).

## Checkpoint — 2026-07-31 (ĐÃ CHẠY & VERIFY TRÊN LOCAL erp_hrm_check)
Vừa hoàn thành: cả 2 task (inline).
- Task 1: `merge_share_tables.php` DRY-RUN → backup → chạy thật → verify. Fix 1 bug lúc DRY-RUN: `$colsOf` phải `SELECT column_name AS cn` (MySQL trả tên cột in hoa). Kết quả: company_employees 1154 (1008+146, +cột type/all_department), employee_manage_departments 309 (126+183, +part_ids); cặp key lặp=0; hrm_* drop; idempotent SKIP OK.
- Task 2: revert 11 file HRM (12 ref, 2 token), php -l sạch, count khớp (1154/309). **Đính chính design:** `TpEmployee.php` mysql2 BỊ COMMENT → dùng conn HRM default → line 86 CÓ đổi (design ghi "né TpEmployee" là sai).
Đang làm dở: (không) — code revert CHƯA commit (gop_db).
Bước tiếp theo (user): commit code revert HRM (11 file) lên gop_db khi OK; chạy `merge_share_tables.php` trên môi trường gộp khác khi cần (đổi `$DB`, DRY-RUN trước).
Lưu ý: company_employees có 2 dòng employee_id (413/750) mồ côi SẴN từ ERP (type=NULL, id gốc ERP) — không do merge; data-fix riêng nếu muốn.
Blocked:
