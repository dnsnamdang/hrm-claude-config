# Thống nhất notifications & files — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đưa notifications + files về cấu trúc HRM (1 bảng/thực thể, bỏ hrm_*): DROP ERP notifications, TRANSFORM ERP files → cấu trúc HRM.

**Architecture:** (A) Script `unify_notif_files.php` idempotent: notifications DROP ERP + rename hrm_notifications→notifications; files transform ERP morph→hrm_files (map fileable_type→table) + archive files→erp_files_old + rename hrm_files→files. (B) Revert code HRM đọc hrm_files/hrm_notifications → tên gốc.

**Tech Stack:** PHP 7.4 / Laravel `DB` facade (tinker), MySQL (schema gộp). Nhánh `gop_db`.

**Spec:** `ERP/.plans/unify-notifications-files/design.md`

## Global Constraints

- Cấu trúc đích = **HRM** cho cả 2 (notifications Laravel notifiable; files table/table_id + metadata).
- notifications: **DROP** ERP 78k. files: **TRANSFORM giữ data** (archive `files`→`erp_files_old`, không drop).
- Map `fileable_type`→`table` (7 class); dòng `fileable_type` NULL (30) không migrate (giữ trong erp_files_old).
- Idempotent: guard `hrm_notifications`/`hrm_files` tồn tại → mới xử lý. `$DRY_RUN=true` mặc định. Chạy 1 lần, **backup trước**.
- Script tại `ERP/.plans/unify-notifications-files/unify_notif_files.php`, nối pipeline sau `disable_crm.php`. Verify trên local `erp_hrm_check` (tinker hrm-api).
- Code revert: bỏ dòng `mysql2`. KHÔNG commit khi chưa yêu cầu.
- ERP notif/file code sẽ lỗi cột sau đổi tên (chấp nhận, sẽ recode) — guard ERP là follow-up ngoài plan này.

---

### Task 1: Script `unify_notif_files.php` (DATA)

**Files:**
- Create: `ERP/.plans/unify-notifications-files/unify_notif_files.php`

**Interfaces:**
- Produces: chạy qua tinker; `$DRY_RUN=true` in dự kiến; `false` thực thi.

- [ ] **Step 1: Tạo script**

```php
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
```

- [ ] **Step 2: lint + DRY-RUN**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
php -l /Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/unify-notifications-files/unify_notif_files.php
php artisan tinker --execute="require '/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/unify-notifications-files/unify_notif_files.php';" 2>&1 | grep -vE "PHP Notice"
```
Expected: notifications — DROP ERP 78719 + rename; files — 7 class in kèm số dòng (HandoverAcceptanceRecord 7951...), NULL=30, rename files→erp_files_old + hrm_files→files. Không ⚠️ (map đủ). "[DRY-RUN xong]".

- [ ] **Step 3: backup + chạy thật**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
S=/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/unify-notifications-files/unify_notif_files.php
mysqldump -h127.0.0.1 -uroot erp_hrm_check notifications hrm_notifications files hrm_files > "$CLAUDE_JOB_DIR/tmp/notif_files_backup.sql"
sed -i '' 's/\$DRY_RUN=true;/\$DRY_RUN=false;/' "$S"
php artisan tinker --execute="require '$S';" 2>&1 | grep -vE "PHP Notice"
sed -i '' 's/\$DRY_RUN=false;/\$DRY_RUN=true;/' "$S"
```
Expected: "[ĐÃ THỰC THI xong]".

- [ ] **Step 4: verify DATA + idempotent**

```bash
php artisan tinker --execute='
function cols($t){ return implode(",",array_map(fn($x)=>$x->cn,DB::select("SELECT column_name cn FROM information_schema.columns WHERE table_schema=DATABASE() AND table_name=? ORDER BY ordinal_position",[$t]))); }
function ex($t){ return DB::select("SELECT COUNT(*) c FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name=?",[$t])[0]->c>0; }
echo "notifications: cấu trúc=[".cols("notifications")."] rows=".DB::table("notifications")->count()."\n";
echo "  hrm_notifications còn=".(ex("hrm_notifications")?"CÒN":"drop")."\n";
echo "files: cấu trúc=[".cols("files")."] rows=".DB::table("files")->count()."\n";
echo "  hrm_files còn=".(ex("hrm_files")?"CÒN":"drop")." | erp_files_old=".(ex("erp_files_old")?DB::table("erp_files_old")->count()." dòng":"KHÔNG")."\n";
echo "  files theo table (map): "; foreach(DB::table("files")->select("table",DB::raw("COUNT(*) n"))->groupBy("table")->orderByDesc("n")->limit(10)->get() as $r) echo $r->table."=".$r->n." "; echo "\n";
' 2>&1 | grep -vE "PHP Notice"
php artisan tinker --execute="require '/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/.plans/unify-notifications-files/unify_notif_files.php';" 2>&1 | grep -E "SKIP"
```
Expected: `notifications` cấu trúc Laravel (`notifiable_type,notifiable_id,data,read_at`), hrm_notifications=drop; `files` cấu trúc HRM (`table,table_id,file_name,file_path...`), rows≈8119 (25 hrm + 8094 ERP), hrm_files=drop, erp_files_old=8124; files theo table gồm `handover_acceptance_records=7951`,... ; re-run in "SKIP" cả 2 phần.

---

### Task 2: Revert code HRM (File / DatabaseNotification → bảng gốc)

**Files:**
- Modify: `HRM/hrm-api/app/Models/File.php` (`$table`)
- Modify: `HRM/hrm-api/app/Models/DatabaseNotification.php` (`$table`)
- Modify: `HRM/hrm-api/Modules/Assign/Services/SolutionService.php`, `Modules/Assign/Services/SolutionModuleService.php` (join `hrm_files.*`)
- Modify: `HRM/hrm-api/app/Console/Commands/Rice/DeleteOldNotification.php` (`DB::table('hrm_notifications')`)
- (comment ở `app/Models/EmployeeInfo.php`, `Modules/Timesheet/Entities/EmployeeInfo.php` — chỉ là comment, đổi theo token cũng vô hại)

**Interfaces:**
- Consumes: bảng gốc `files`/`notifications` (cấu trúc HRM, Task 1).

- [ ] **Step 1: perl replace 2 token (bỏ mysql2)**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
grep -rlE "hrm_files|hrm_notifications" app Modules config 2>/dev/null | grep -v mysql2 | while read f; do
  perl -i -pe 's/hrm_files/files/g; s/hrm_notifications/notifications/g' "$f"
done
echo "=== còn sót (bỏ mysql2)? ==="
grep -rnE "hrm_files|hrm_notifications" app Modules config 2>/dev/null | grep -v mysql2 || echo "(sạch)"
echo "=== \$table sau sửa ==="
grep -nE "\\\$table" app/Models/File.php app/Models/DatabaseNotification.php
```
Expected: grep "(sạch)"; `File.php`/`DatabaseNotification.php` `$table = 'files'` / `'notifications'`.

- [ ] **Step 2: verify lint + runtime**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
git diff --name-only | while read f; do [ "${f##*.}" = "php" ] && (php -l "$f" >/dev/null 2>&1 && echo "OK $f" || php -l "$f"); done
php artisan tinker --execute='
echo "File(files): ".\App\Models\File::count()."\n";
echo "DatabaseNotification(notifications): ".\App\Models\DatabaseNotification::count()."\n";
$e=\Modules\Timesheet\Entities\EmployeeInfo::first();
echo "EmployeeInfo notifications(): ".($e? $e->notifications()->count()." (đọc được)":"(no emp)")."\n";
' 2>&1 | grep -vE "PHP Notice"
```
Expected: tất cả php -l OK; `File::count()` = ~8119 (bảng files gộp), `DatabaseNotification::count()` chạy (0 dòng), `notifications()` relation đọc được — không lỗi "Base table hrm_* doesn't exist".

---

## Verify tổng thể

- `notifications` = cấu trúc Laravel HRM (hrm_notifications cũ), ERP 78k đã drop; `files` = cấu trúc HRM + 8094 dòng ERP transform (đúng `table` theo map), `hrm_files` drop, `erp_files_old` giữ 8124 gốc.
- HRM code (File, DatabaseNotification, SolutionService join, DeleteOldNotification) đọc bảng gốc — php -l + grep sạch, runtime OK.
- Re-run `unify_notif_files.php` → SKIP cả 2 phần.
- Pipeline: `... → disable_crm.php → unify_notif_files.php`.
- Follow-up (ngoài plan): guard/tắt code ERP notifications/files để ERP không crash trên DB gộp.

## Checkpoint — 2026-08-01 (ĐÃ CHẠY & VERIFY TRÊN LOCAL erp_hrm_check)
Vừa hoàn thành: cả 2 task (inline).
- Task 1: `unify_notif_files.php` DRY-RUN → backup 20M → chạy thật → verify. notifications=cấu trúc Laravel (0 dòng, ERP 78719 drop), hrm_notifications drop. files=cấu trúc HRM 8119 dòng (25 hrm + 8094 ERP transform theo map 7 class; 30 null giữ trong erp_files_old=8124). Idempotent SKIP.
- Task 2: revert 7 file HRM (perl 2 token hrm_files/hrm_notifications, bỏ mysql2). php -l sạch, grep sạch. Runtime OK: File=8119, DatabaseNotification=0, EmployeeInfo->notifications() đọc được.
Đang làm dở: (không) — code revert CHƯA commit gop_db.
Bước tiếp theo (user): commit code revert; guard/tắt code ERP notif/file để ERP không crash trên DB gộp (follow-up); chạy unify_notif_files.php trên môi trường gộp khác khi cần.
Blocked:

## Checkpoint — 2026-08-17 (FOLLOW-UP: guard code ERP notif/file — ĐÃ LÀM + VERIFY trên erp_hrm_check)
Bối cảnh: phát hiện khi E2E test luồng xuất hàng (`hop-dong-xuat-hang`) trên DB gộp — chuông ERP 500 (`notifications.receiver_id`) + form tạo phiếu xuất crash PHP (`files.fileable_id`).

Vừa hoàn thành (3 file ERP TanPhatDev, KHÔNG đổi hàm dùng chung về mặt API — chỉ adapter nội bộ):
- **Notification (chuông)** → dùng bảng `notifications` schema Laravel gộp. `app/Model/Common/Notification.php` viết lại thành ADAPTER: uuid key (`$incrementing=false`, `keyType='string'`), `$casts['data']='array'`, boot `creating` tự sinh uuid + `notifiable_type='App\Employee'` + chốt `sender_name`/`sender_avatar` từ `created_by`. Accessor/mutator map field cũ (`url`/`content`/`created_by`/`sender_name`/`sender_avatar`→`data` JSON; `receiver_id`→`notifiable_id`; `status`/`seen`→`read_at`) → toàn bộ caller cũ (`NotificationHelper::sendNotify`, các Service, `send()`) chạy nguyên. `getSenderAttribute` giữ `->sender->fullname/avatar`.
- `app/Http/Controllers/Common/NotificationsController.php`: `index` query `notifiable_type+notifiable_id`, map data JSON → field FE (`sender_name/sender_avatar/content/status`), `unread=whereNull(read_at)`; `read/readAll` set `read_at` (id nay là uuid). Lưu ý: gộp `seen`+`status` vào `read_at` (mất phân tầng "đã xem/đã click", chấp nhận trên DB gộp).
- `app/Helpers/FormatHelper.php::messageFromNotification`: dùng accessor `sender_name/sender_avatar` (thay `->sender->fullname/avatar`).
- **Files (form tạo phiếu xuất)** → `app/Model/Common/PriceListValidDeliveryQuotation.php::attachment()` đổi `morphOne(File,'fileable')` → `hasOne(File,'table_id')->where('table','price_list_valid_delivery_quotations')` (schema files HRM table/table_id). (Đây là 1 trong 23 model ERP còn dùng morph fileable — mới fix model nằm trong luồng xuất; còn 22 model khác chưa fix, sẽ crash khi màn tương ứng đụng file.)

Verify: php -l sạch cả 3 file. Tinker: ghi Notification (uuid, notifiable=App\Employee:13, sender="DNS Admin"), đọc lại, mark-read set read_at, unread-count đúng, `messageFromNotification` OK. Log sau khi sửa KHÔNG còn lỗi `receiver_id` (chỉ 10:42–10:47 trước sửa).

E2E xuất hàng tiến triển: form `warehouse_exports/create?warehouse_export_request_id=31053` load OK (thêm unit "Bộ" id=39 cho SP 3960 để hết crash `unit_coefficient`), `can_export=true`, 3 SP xuất được. Submit store() → **200 + JSON validation sạch** (KHÔNG còn crash schema merged-DB), chỉ thiếu dữ liệu nghiệp vụ: `receiver_id`, mỗi `lots.*.details.0.position_id` + `import_lot_id` (bước phân bổ lô/vị trí — nhập tay bình thường).

Đang làm dở: (không) — CHƯA commit. Còn `total_cost` (widget dashboard `quotations`) 500 riêng, chưa fix (không thuộc luồng xuất hàng).
Bước tiếp theo: điền receiver + phân bổ lô/vị trí để tạo thật warehouse_exports → theo redirect `/pick` → B4 (HRM product-exports/create + loại 20 auto-nhập-cha).
Blocked: