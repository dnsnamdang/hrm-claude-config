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
