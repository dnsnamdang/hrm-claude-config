<?php
/**
 * GỘP DB ERP + HRM — SCRIPT PRODUCTION (idempotent)
 * ==================================================
 * Chiến lược: gộp toàn bộ bảng HRM VÀO schema ERP (base = ERP, giữ nguyên tên+cột).
 *   - Bảng HRM riêng (không trùng ERP)         -> RENAME move sang schema ERP (tức thì).
 *   - Bảng trùng nhóm TÁCH                       -> RENAME move -> `hrm_<tên>`.
 *   - Bảng trùng nhóm HÒA (dùng chung)           -> thêm cột HRM thiếu + nhập HRM rows chưa có id
 *                                                   (+ tùy chọn điền cột CRM/HRM cho row đụng id) rồi DROP bảng HRM.
 *   - 1.216 bảng thuần-ERP: KHÔNG đụng (đã nằm sẵn trong schema ERP).
 *
 * CÁCH CHẠY (trên máy có nối tới CẢ 2 DB, CÙNG server):
 *   1) BACKUP cả 2 DB trước (bắt buộc).
 *   2) Đặt $SRC_ERP / $SRC_HRM đúng tên schema thật.
 *   3) Chạy DRY_RUN=true trước để xem hành động (không thực thi).
 *   4) Đổi DRY_RUN=false để gộp thật.
 *   Chạy:  php artisan tinker --execute="require '.../merge_prod.php';"
 *      hoặc bootstrap Laravel rồi require file này.
 *
 * Idempotent: chạy lại nhiều lần an toàn (bỏ qua bảng đã xử lý).
 */

use Illuminate\Support\Facades\DB;

// ===================== CẤU HÌNH =====================
$SRC_ERP = 'erp_new';       // schema ERP (đích gộp — GIỮ NGUYÊN)
$SRC_HRM = 'hrm_pro';       // schema HRM (nguồn — sẽ được move đi)
$PREFIX  = 'hrm_';          // tiền tố cho bảng tách
$DRY_RUN = true;            // true = chỉ IN hành động, KHÔNG thực thi
$FILL_SHARED_HRM = true;    // true = điền cột HRM-only cho các row có id trùng ERP (giữ dữ liệu CRM HRM)
// ====================================================

// Nhóm GIỮ HRM BỎ ERP (user chốt 2026-07-29): bảng gộp = cấu trúc+data HRM, DROP bảng ERP.
// CẢNH BÁO: code ERP dùng các bảng này (quotations/working_positions/job_requests...) sẽ đọc
// cấu trúc HRM → phần chức năng ERP tương ứng có thể gãy (chấp nhận vì đích là app HRM).
$KEEP_HRM = ['transport_types','quotations','moving_norm_roads','job_requests','job_request_employees','job_request_details','attachment_types','assign_business_tasks','working_positions','teams','moving_norm_road_types','majors','employee_incomes','areas'];

// Nhóm HÒA (dùng chung) — HRM hòa vào bảng ERP cùng tên (đã verify id khớp/cùng nghĩa)
$SHARE = ['bank_branches','banks','companies','customer_contacts','customer_deputies','customers','departments','districts','employee_infos','hamlets','moving_norms','parts','province_mappings','provinces','ward_mappings','wards'];

// Nhóm TÁCH — thành hrm_<tên> (id đụng khác thực thể / khác bản chất, gồm groups, files, notifications)
// notifications: ERP tùy biến (url/content/receiver_id) KHÁC cấu trúc Laravel của HRM → tách để CẢ 2 app chạy
// (ERP giữ `notifications`, HRM trỏ `hrm_notifications` qua model App\Models\DatabaseNotification). Data HRM bỏ (truncate).
$TACH  = ['employees','company_employees','company_roles','customer_activity_types','customer_business_fields','customer_contact_has_bank_accounts','customer_has_bank_accounts','customer_has_vehicle_manufacts','delivery_places','employee_has_permissions','employee_has_roles','employee_manage_departments','files','groups','module_mappings','nations','notifications','permissions','print_templates','role_has_permissions','roles','scopes','settlement_contract_employees','settlement_contracts'];
$EMPTY_AFTER_TACH = ['notifications']; // sau khi tách -> hrm_notifications thì truncate (thông báo không cần giữ data)

// Nhóm LOG — bỏ data HRM, chỉ giữ structure ERP (jobs/failed_jobs/password_resets là bảng Laravel chuẩn,
// cấu trúc 2 hệ giống nhau nên giữ ERP OK). notifications KHÔNG ở đây (structure ERP khác HRM) → xem KEEP_HRM.
$LOG_DROP = ['jobs','failed_jobs','password_resets'];

// migrations: union theo TÊN migration (không theo id) — xử lý riêng.

$keepHrmSet = array_flip($KEEP_HRM);
$shareSet = array_flip($SHARE);
$tachSet  = array_flip($TACH);
$logSet   = array_flip($LOG_DROP);

function tExists($schema, $t){ return count(DB::select("select 1 from information_schema.tables where table_schema=? and table_name=? limit 1",[$schema,$t]))>0; }
function cols($schema, $t){ return array_map(fn($x)=>$x->cn??$x->CN, DB::select("select column_name cn from information_schema.columns where table_schema=? and table_name=? order by ordinal_position",[$schema,$t])); }
function coldef($schema, $t, $c){ $r=DB::select("select column_type ct, is_nullable n, column_default d, extra e from information_schema.columns where table_schema=? and table_name=? and column_name=?",[$schema,$t,$c])[0]; $null=$r->n==='YES'?'NULL':'NOT NULL'; $def=$r->d!==null?" DEFAULT ".(is_numeric($r->d)?$r->d:"'".addslashes($r->d)."'"):($r->n==='YES'?' DEFAULT NULL':''); return "`$c` {$r->ct} $null$def"; }
function q($a){ return implode(',', array_map(fn($c)=>"`$c`",$a)); }

$acts = [];               // log hành động
$do = function($sql) use ($DRY_RUN, &$acts){ $acts[]=$sql; if(!$DRY_RUN) DB::statement($sql); };

// Guard
foreach ([$SRC_ERP,$SRC_HRM] as $s) if (!count(DB::select("select 1 from information_schema.schemata where schema_name=?",[$s]))) { echo "LỖI: schema '$s' không tồn tại\n"; return; }
echo ($DRY_RUN?"[DRY-RUN] ":"[THỰC THI] ")."Gộp $SRC_HRM -> $SRC_ERP (prefix tách='$PREFIX', điền cột HRM row đụng=".($FILL_SHARED_HRM?'CÓ':'KHÔNG').")\n\n";

if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=0");

$hrmTables = array_map(fn($x)=>$x->TABLE_NAME??$x->table_name, DB::select("select table_name from information_schema.tables where table_schema=? and table_type='BASE TABLE'",[$SRC_HRM]));
$cnt=['move'=>0,'tach'=>0,'share'=>0,'keephrm'=>0,'log'=>0,'skip'=>0,'err'=>0];

foreach ($hrmTables as $t) {
  try {
    if (isset($keepHrmSet[$t])) {
      // GIỮ HRM BỎ ERP: LUÔN xoá bảng ERP (nếu có) rồi move bảng HRM giữ NGUYÊN TÊN.
      // Idempotent: nếu HRM không còn (đã move) -> bỏ qua.
      if (!tExists($SRC_HRM,$t)) { $cnt['skip']++; continue; }
      if (tExists($SRC_ERP,$t)) $do("DROP TABLE `$SRC_ERP`.`$t`");
      $do("RENAME TABLE `$SRC_HRM`.`$t` TO `$SRC_ERP`.`$t`");
      $cnt['keephrm']++;
    } elseif (isset($logSet[$t])) {
      // LOG: bỏ data HRM, giữ structure ERP (base đã có). Chỉ DROP bảng HRM.
      if (tExists($SRC_HRM,$t)) $do("DROP TABLE `$SRC_HRM`.`$t`");
      $cnt['log']++;
    } elseif ($t === 'migrations') {
      // migrations: union theo TÊN (bỏ id). Thêm migration HRM chưa có tên vào bảng ERP rồi bỏ HRM.
      if (tExists($SRC_ERP,'migrations') && tExists($SRC_HRM,'migrations')) {
        $do("INSERT INTO `$SRC_ERP`.`migrations` (migration,batch) SELECT h.migration,h.batch FROM `$SRC_HRM`.`migrations` h WHERE h.migration NOT IN (SELECT migration FROM `$SRC_ERP`.`migrations`)");
        $do("DROP TABLE `$SRC_HRM`.`migrations`");
        $cnt['share']++;
      }
    } elseif (isset($shareSet[$t])) {
      // HÒA vào ERP
      if (!tExists($SRC_HRM,$t)) { $cnt['skip']++; continue; } // đã xử lý (đã DROP)
      if (!tExists($SRC_ERP,$t)) { // ERP không có (hiếm) -> coi như move nguyên tên
        $do("RENAME TABLE `$SRC_HRM`.`$t` TO `$SRC_ERP`.`$t`"); $cnt['move']++; continue;
      }
      $ec = cols($SRC_ERP,$t); $hc = cols($SRC_HRM,$t);
      // 1) thêm cột HRM thiếu vào bảng ERP
      foreach (array_diff($hc,$ec) as $mc) $do("ALTER TABLE `$SRC_ERP`.`$t` ADD COLUMN ".coldef($SRC_HRM,$t,$mc));
      // 2) nhập HRM rows chưa có id (union rows)
      $hasId = in_array('id',$ec) && in_array('id',$hc);
      if ($hasId) $do("INSERT IGNORE INTO `$SRC_ERP`.`$t` (".q($hc).") SELECT ".q($hc)." FROM `$SRC_HRM`.`$t` h WHERE NOT EXISTS (SELECT 1 FROM `$SRC_ERP`.`$t` e WHERE e.id=h.id)");
      else        $do("INSERT IGNORE INTO `$SRC_ERP`.`$t` (".q($hc).") SELECT ".q($hc)." FROM `$SRC_HRM`.`$t`");
      // 3) (tùy chọn) điền cột HRM-only cho row có id trùng ERP
      if ($FILL_SHARED_HRM && $hasId) {
        $onlyHrm = array_values(array_diff($hc, $ec, ['id']));
        if ($onlyHrm) { $set=implode(', ', array_map(fn($c)=>"e.`$c`=h.`$c`",$onlyHrm)); $do("UPDATE `$SRC_ERP`.`$t` e JOIN `$SRC_HRM`.`$t` h ON e.id=h.id SET $set"); }
      }
      // 4) bỏ bảng HRM đã hòa
      $do("DROP TABLE `$SRC_HRM`.`$t`");
      $cnt['share']++;
    } elseif (isset($tachSet[$t])) {
      // TÁCH -> hrm_<t>
      $target = $PREFIX.$t;
      if (tExists($SRC_ERP,$target)) { $cnt['skip']++; continue; } // đã tách
      if (!tExists($SRC_HRM,$t)) { $cnt['skip']++; continue; }
      $do("RENAME TABLE `$SRC_HRM`.`$t` TO `$SRC_ERP`.`$target`");
      if (in_array($t, $EMPTY_AFTER_TACH)) $do("TRUNCATE TABLE `$SRC_ERP`.`$target`"); // bỏ data (vd hrm_notifications)
      $cnt['tach']++;
    } else {
      // HRM riêng -> move nguyên tên
      if (tExists($SRC_ERP,$t)) { $cnt['skip']++; continue; }   // đã move / hoặc trùng ngoài dự kiến
      if (!tExists($SRC_HRM,$t)) { $cnt['skip']++; continue; }
      $do("RENAME TABLE `$SRC_HRM`.`$t` TO `$SRC_ERP`.`$t`");
      $cnt['move']++;
    }
  } catch (\Throwable $e) { $cnt['err']++; echo "ERR `$t`: ".substr($e->getMessage(),0,90)."\n"; }
}

if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=1");

echo "\n=== KẾT QUẢ: HRM riêng move=".$cnt['move']." | tách hrm_*=".$cnt['tach']." | hòa=".$cnt['share']." | giữ-HRM-bỏ-ERP=".$cnt['keephrm']." | log-bỏ-data=".$cnt['log']." | bỏ qua=".$cnt['skip']." | lỗi=".$cnt['err']." ===\n";
if ($DRY_RUN) {
  echo "\n[DRY-RUN] Số câu lệnh sẽ chạy: ".count($acts).". Xem trước 12 câu:\n";
  foreach (array_slice($acts,0,12) as $s) echo "  ".$s."\n";
  echo "\n→ Đổi \$DRY_RUN=false để gộp thật (đã BACKUP chưa?).\n";
} else {
  $tot = DB::select("select count(*) c from information_schema.tables where table_schema='$SRC_ERP'")[0]->c;
  $left = DB::select("select count(*) c from information_schema.tables where table_schema='$SRC_HRM'")[0]->c;
  echo "Schema $SRC_ERP giờ có $tot bảng | $SRC_HRM còn $left bảng (còn lại nếu có = cần rà).\n";
  echo "→ SAU GỘP: app ERP đổi connection sang '$SRC_ERP' (giữ nguyên). App HRM đổi sang '$SRC_ERP' + sửa code các bảng đã đổi tên hrm_* và dùng chung.\n";
}
