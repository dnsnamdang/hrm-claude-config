<?php
/**
 * Vô hiệu hoá CRM Mate-sync (CRM ngừng dùng): tắt cờ use_crm + drop hrm_module_mappings.
 * GIỮ code Modules/CRM + bảng module_mappings (TpModuleMapping, use_erp).
 * Idempotent + DRY_RUN. Chạy qua tinker (hrm-api). Nối pipeline sau reconcile_auth.php.
 */
use Illuminate\Support\Facades\DB;

// ===================== CẤU HÌNH =====================
$DB='erp_hrm_check'; $DRY_RUN=true;
// ====================================================

echo ($DRY_RUN?"[DRY-RUN] ":"[THỰC THI] ")."Disable CRM sync trên `$DB`\n";

// 1) Tắt cờ use_crm (boot-hook Human entity chỉ chạy khi use_crm bật)
$ms=DB::table('master_settings')->where('category','use_crm')->first();
if($ms){
    echo "  use_crm hiện = '".$ms->content."'";
    if((string)$ms->content !== '0'){ if(!$DRY_RUN) DB::table('master_settings')->where('id',$ms->id)->update(['content'=>'0']); echo " -> set '0'\n"; }
    else echo " (đã off)\n";
} else echo "  (không có row use_crm)\n";

// 2) Drop hrm_module_mappings (chỉ CRM sync dùng). KHÔNG đụng module_mappings.
$ex=DB::select("SELECT COUNT(*) c FROM information_schema.tables WHERE table_schema='$DB' AND table_name='hrm_module_mappings'")[0]->c;
if($ex){
    echo "  hrm_module_mappings = ".DB::table('hrm_module_mappings')->count()." dòng -> DROP\n";
    if(!$DRY_RUN) DB::statement("DROP TABLE `$DB`.`hrm_module_mappings`");
} else echo "  hrm_module_mappings đã drop (SKIP)\n";

echo "\n".($DRY_RUN?"[DRY-RUN xong — chưa thay đổi gì]":"[ĐÃ THỰC THI xong]")."\n";
