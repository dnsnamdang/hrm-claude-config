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
