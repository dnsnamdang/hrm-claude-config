<?php
/**
 * RECONCILE employees ERP + HRM -> 1 bảng `employees` (id ERP chuẩn).
 * Chạy trên schema ĐÃ MERGE (có cả employees + hrm_employees), qua tinker:
 *   php artisan tinker --execute="require '.../reconcile_employees.php';"
 * Idempotent: hrm_employees không còn -> SKIP. DRY_RUN=true mặc định (chỉ in).
 * Auth: giữ password/token/rice của HRM.
 * Remap FK:
 *   - Cột AUDIT (created_by, updated_by...) = LUÔN tài khoản -> remap (HRM-origin non-SHARE = map đầy đủ; SHARE = emp_id_map_safe).
 *   - Cột employee_id/user_id/emp_id/executor_id = có thể trỏ HỒ SƠ -> PHÂN LOẠI RUNTIME (in_emp vs in_info); chỉ remap khi RÕ tài khoản.
 *   - Cột trỏ bảng khác (teacher_id, examiner_id...) không nằm trong danh sách -> tự loại.
 *   - Bảng ERP-origin: không đụng.
 */
use Illuminate\Support\Facades\DB;

// ===================== CẤU HÌNH =====================
$DB      = 'erp_hrm_check';   // schema đã merge (SERVER: đổi cho đúng)
$DRY_RUN = true;              // true = chỉ IN, KHÔNG chạy
// ====================================================
$SHARE = ['bank_branches','banks','companies','customer_contacts','customer_deputies','customers','departments','districts','employee_infos','hamlets','moving_norms','parts','province_mappings','provinces','ward_mappings','wards'];
$TACH  = ['employees','company_employees','company_roles','customer_activity_types','customer_business_fields','customer_contact_has_bank_accounts','customer_has_bank_accounts','customer_has_vehicle_manufacts','delivery_places','employee_has_permissions','employee_has_roles','employee_manage_departments','files','groups','module_mappings','nations','notifications','permissions','print_templates','role_has_permissions','roles','scopes','settlement_contract_employees','settlement_contracts'];
$HRM_TABLES_FILE = __DIR__.'/../hop-nhat-erp-hrm/hrm-view-tables.txt';
// Cột AUDIT — luôn = tài khoản (đã grep xác nhận belongsTo Employee / set = auth id)
$AUDIT_COLS = ['created_by','updated_by','changed_by','deleted_by','approved_by','approver_id','creator_id','assignee_id','leader_id','buyer_id','receiver_id','rice_created_by','reviewed_by','uploaded_by','detected_by','closed_by','processed_by','tp_approved_by','approved_department_by','approved_personnel_administration_by','handover_by','confirm_by','confirmed_by','handler_id','requester_id','signer_id','manager','manager_id','employee_create_id'];
// Cột có thể trỏ HỒ SƠ -> phân loại runtime
$CLASSIFY_COLS = ['employee_id','user_id','emp_id','executor_id'];

$acts=[]; $do=function($sql) use(&$acts,$DRY_RUN){ $acts[]=$sql; if(!$DRY_RUN) DB::statement($sql); };
$scalar=function($sql){ $r=DB::select($sql); return $r?array_values((array)$r[0])[0]:null; };
$texists=function($t) use($DB,$scalar){ return $scalar("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB' AND table_name='".addslashes($t)."'")>0; };
$cexists=function($t,$c) use($DB,$scalar){ return $scalar("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='$DB' AND table_name='".addslashes($t)."' AND column_name='".addslashes($c)."'")>0; };

echo ($DRY_RUN?"[DRY-RUN] ":"[THỰC THI] ")."Reconcile employees trên `$DB`\n";
if (!$texists('hrm_employees')) { echo "hrm_employees không còn -> đã reconcile. SKIP.\n"; return; }
if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=0");

// --- Task 1: emp_id_map + emp_id_map_safe ---
$do("DROP TABLE IF EXISTS `$DB`.`emp_id_map`");
$do("CREATE TABLE `$DB`.`emp_id_map` (hrm_id BIGINT PRIMARY KEY, erp_id BIGINT, INDEX(erp_id)) AS
     SELECT h.id hrm_id, e.id erp_id FROM `$DB`.`hrm_employees` h JOIN `$DB`.`employees` e ON e.employee_info_id=h.employee_info_id WHERE h.id<>e.id");
$do("DROP TABLE IF EXISTS `$DB`.`emp_id_map_safe`");
$do("CREATE TABLE `$DB`.`emp_id_map_safe` (hrm_id BIGINT PRIMARY KEY, erp_id BIGINT, INDEX(erp_id)) AS
     SELECT hrm_id,erp_id FROM `$DB`.`emp_id_map` WHERE hrm_id NOT IN (SELECT id FROM `$DB`.`employees`)");

// --- Task 2: cột HRM-only + cập nhật auth/rice ---
foreach (['tp_id','password_changed_at','rice_setting_location_id','rice_ssn','login_count'] as $col) {
    if (!$cexists('employees',$col)) {
        $d=DB::select("SELECT column_type ct,is_nullable n FROM information_schema.columns WHERE table_schema='$DB' AND table_name='hrm_employees' AND column_name='$col'")[0];
        $do("ALTER TABLE `$DB`.`employees` ADD COLUMN `$col` {$d->ct} ".($d->n==='YES'?'NULL':'NOT NULL'));
    }
}
$do("UPDATE `$DB`.`employees` e JOIN `$DB`.`hrm_employees` h ON h.employee_info_id=e.employee_info_id
     SET e.password=h.password,e.token_version=h.token_version,e.password_changed_at=h.password_changed_at,
         e.tp_id=h.tp_id,e.rice_setting_location_id=h.rice_setting_location_id,e.rice_ssn=h.rice_ssn,e.login_count=h.login_count");

// --- Task 3: người chỉ có ở HRM -> INSERT id mới + bổ sung map ---
$do("INSERT INTO `$DB`.`employees` (email,password,email_verified_at,remember_token,status,employee_info_id,created_at,updated_at,token_version,password_changed_at,tp_id,rice_setting_location_id,rice_ssn,login_count)
     SELECT h.email,h.password,h.email_verified_at,h.remember_token,h.status,h.employee_info_id,h.created_at,h.updated_at,h.token_version,h.password_changed_at,h.tp_id,h.rice_setting_location_id,h.rice_ssn,h.login_count
     FROM `$DB`.`hrm_employees` h WHERE NOT EXISTS (SELECT 1 FROM `$DB`.`employees` e WHERE e.employee_info_id=h.employee_info_id)");
$do("INSERT IGNORE INTO `$DB`.`emp_id_map` (hrm_id,erp_id)
     SELECT h.id,e.id FROM `$DB`.`hrm_employees` h JOIN `$DB`.`employees` e ON e.employee_info_id=h.employee_info_id
     WHERE h.id<>e.id AND h.id NOT IN (SELECT hrm_id FROM `$DB`.`emp_id_map`)");

// --- Task 4: enumerate + phân loại ---
$hrmNames=array_filter(array_map('trim',file($HRM_TABLES_FILE)));
$tachSet=array_flip($TACH); $shareSet=array_flip($SHARE); $hrmOriginMerged=[];
foreach ($hrmNames as $x){ $hrmOriginMerged[ isset($tachSet[$x])?'hrm_'.$x:$x ]=true; }
$allCols=array_merge($AUDIT_COLS,$CLASSIFY_COLS);
$inList="'".implode("','",array_map('addslashes',$allCols))."'";
$cands=DB::select("SELECT table_name t,column_name c FROM information_schema.columns WHERE table_schema='$DB' AND column_name IN ($inList) AND table_name NOT IN ('employees','hrm_employees','emp_id_map','emp_id_map_safe')");
$classifySet=array_flip($CLASSIFY_COLS);
$remap=[]; $skipped=[];
foreach ($cands as $r){
    if (!isset($hrmOriginMerged[$r->t])) continue;               // chỉ HRM-origin
    $mode = isset($shareSet[$r->t]) ? 'safe':'full';
    if (isset($classifySet[$r->c])) {
        // PHÂN LOẠI RUNTIME: chỉ remap khi in_emp=tot AND in_info<tot (rõ tài khoản)
        $s=DB::select("SELECT COUNT(*) tot, COALESCE(SUM(x.`{$r->c}` IN (SELECT id FROM `$DB`.`hrm_employees`)),0) em, COALESCE(SUM(x.`{$r->c}` IN (SELECT id FROM `$DB`.`employee_infos`)),0) inf FROM `$DB`.`{$r->t}` x WHERE x.`{$r->c}` IS NOT NULL")[0];
        if ($s->tot>0 && $s->em==$s->tot && $s->inf<$s->tot) { $remap[]=['t'=>$r->t,'c'=>$r->c,'m'=>$mode]; }
        else { $skipped[]="[{$r->t}.{$r->c}] tot={$s->tot} in_emp={$s->em} in_info={$s->inf} -> LOẠI (không rõ tài khoản)"; }
    } else {
        $remap[]=['t'=>$r->t,'c'=>$r->c,'m'=>$mode];             // AUDIT -> luôn remap
    }
}
echo "\n=== SẼ REMAP (".count($remap).") | LOẠI phân-loại (".count($skipped).") ===\n";
foreach ($remap as $r) echo "  [{$r['m']}] {$r['t']}.{$r['c']}\n";
if ($skipped){ echo "-- LOẠI (employee_id/... trỏ hồ sơ/mơ hồ/rỗng): --\n"; foreach($skipped as $s) echo "  $s\n"; }

// --- Task 5: remap ---
$n=0; foreach ($remap as $r){ $mt=$r['m']==='safe'?'emp_id_map_safe':'emp_id_map';
    $do("UPDATE `$DB`.`{$r['t']}` t JOIN `$DB`.`$mt` m ON t.`{$r['c']}`=m.hrm_id SET t.`{$r['c']}`=m.erp_id"); $n++; }
echo "Đã remap $n cột.\n";

// --- Task 6: drop hrm_employees + finalize ---
$do("DROP TABLE `$DB`.`hrm_employees`");
$do("DROP TABLE IF EXISTS `$DB`.`emp_id_map`"); $do("DROP TABLE IF EXISTS `$DB`.`emp_id_map_safe`");
if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=1");
echo "\n=== employees=".$scalar("SELECT COUNT(*) FROM `$DB`.employees")." | hrm_employees ".($texists('hrm_employees')?'CÒN(lỗi)':'drop')." ===\n";
if ($DRY_RUN){ echo "\n[DRY-RUN] ".count($acts)." lệnh. Đổi \$DRY_RUN=false để chạy thật (BACKUP trước).\n"; }
