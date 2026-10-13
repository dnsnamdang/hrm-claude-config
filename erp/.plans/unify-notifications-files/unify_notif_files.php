<?php
/**
 * Thống nhất notifications & files về CẤU TRÚC HRM (bỏ hrm_*). Chạy qua tinker.
 * notifications: DROP ERP (custom) -> RENAME hrm_notifications -> notifications.
 * files: TRANSFORM ERP morph -> hrm_files (table/table_id) -> archive files->erp_files_old -> RENAME hrm_files->files.
 * Idempotent (guard hrm_*). DRY_RUN mặc định. Chạy 1 lần, backup trước.
 */
use Illuminate\Support\Facades\DB;

// ===================== CẤU HÌNH =====================
$DB='erp_hrm_check'; $DRY_RUN=true;
// Map fileable_type (class ERP, single-quote -> 1 backslash) -> table (convention HRM)
$FMAP = [
  'App\\Model\\Customers\\HandoverAcceptanceRecord'     => 'handover_acceptance_records',
  'App\\Model\\Sale\\SettlementContract'                => 'settlement_contracts',
  'App\\Model\\Common\\DeliveryCostSummaryQuotation'    => 'delivery_cost_summary_quotations',
  'App\\Model\\Sale\\ServiceAccountingRequest'          => 'service_accounting_requests',
  'App\\Model\\Sale\\QuotationTemplate'                 => 'quotation_templates',
  'App\\Model\\Common\\PriceListValidDeliveryQuotation' => 'price_list_valid_delivery_quotations',
  'App\\Model\\Product\\ProductTechAttachment'          => 'product_tech_attachments',
];
// ====================================================

$acts=[];
$do=function($sql,$bind=[]) use(&$acts,$DRY_RUN){ $acts[]=$sql; if(!$DRY_RUN) DB::statement($sql,$bind); };
$scalar=function($sql,$bind=[]){ $r=DB::select($sql,$bind); return $r?array_values((array)$r[0])[0]:null; };
$texists=function($t) use($DB,$scalar){ return $scalar("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB' AND table_name='".addslashes($t)."'")>0; };

echo ($DRY_RUN?"[DRY-RUN] ":"[THỰC THI] ")."Unify notifications & files trên `$DB`\n";
if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=0");

// ===== NOTIFICATIONS: DROP ERP + rename =====
echo "\n-- notifications --\n";
if (!$texists('hrm_notifications')) { echo "  hrm_notifications không còn -> SKIP\n"; }
else {
  $erpN = $texists('notifications') ? $scalar("SELECT COUNT(*) FROM `$DB`.`notifications`") : 0;
  echo "  DROP notifications (ERP $erpN dòng) + RENAME hrm_notifications->notifications\n";
  if ($texists('notifications')) $do("DROP TABLE `$DB`.`notifications`");
  $do("RENAME TABLE `$DB`.`hrm_notifications` TO `$DB`.`notifications`");
}

// ===== FILES: transform ERP -> hrm_files, archive, rename =====
echo "\n-- files --\n";
if (!$texists('hrm_files')) { echo "  hrm_files không còn -> SKIP\n"; }
else {
  $classes=array_keys($FMAP); $ph=implode(',',array_fill(0,count($classes),'?'));
  $unmapped=DB::select("SELECT DISTINCT fileable_type ft FROM `$DB`.`files` WHERE fileable_type IS NOT NULL AND fileable_type NOT IN ($ph)", $classes);
  if ($unmapped){ echo "  ⚠️ DỪNG: fileable_type ngoài map: ".implode(', ',array_map(fn($r)=>$r->ft,$unmapped))." -> bổ sung \$FMAP rồi chạy lại\n"; if(!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=1"); return; }
  echo "  fileable_type NULL (không migrate, giữ trong erp_files_old): ".$scalar("SELECT COUNT(*) FROM `$DB`.`files` WHERE fileable_type IS NULL")."\n";
  foreach ($FMAP as $cls=>$tbl) {
    $n=$scalar("SELECT COUNT(*) FROM `$DB`.`files` WHERE fileable_type=?", [$cls]);
    echo "  ".str_pad($cls,52)." -> ".str_pad($tbl,40)." : $n dòng\n";
    $do("INSERT INTO `$DB`.`hrm_files` (`table`,`table_id`,`name`,`file_name`,`file_path`,`file_type`,`created_at`,`updated_at`)
         SELECT ?, fileable_id, name, SUBSTRING_INDEX(path,'/',-1), path, SUBSTRING_INDEX(path,'.',-1), created_at, updated_at
         FROM `$DB`.`files` WHERE fileable_type=?", [$tbl,$cls]);
  }
  $do("RENAME TABLE `$DB`.`files` TO `$DB`.`erp_files_old`");
  $do("RENAME TABLE `$DB`.`hrm_files` TO `$DB`.`files`");
}

if (!$DRY_RUN) DB::statement("SET FOREIGN_KEY_CHECKS=1");
if ($DRY_RUN){ echo "\n--- SQL dự kiến (".count($acts)." câu) ---\n"; foreach($acts as $s) echo trim(preg_replace('/\s+/',' ',$s))."\n"; }
echo "\n".($DRY_RUN?"[DRY-RUN xong — chưa thay đổi gì]":"[ĐÃ THỰC THI xong]")."\n";
