# Thống nhất cơ chế notifications & files ERP+HRM

> Thuộc Gộp DB. Nhánh `gop_db`. Ngày: 2026-08-01.
> **Mục tiêu:** đưa notifications + files về **cấu trúc HRM** (1 bảng/thực thể), bỏ `hrm_*`. ERP notifications/files **ngừng hoạt động** (sẽ recode lên HRM sau, dùng chung bảng).

## 1. Scope
- `notifications` (ERP custom 78.719 dòng vs HRM Laravel notifiable 0 dòng).
- `files` (ERP morph 8.124 dòng vs HRM table/table_id + metadata 25 dòng).

## 2. Khảo sát (kết luận)
- **notifications:** HRM = Laravel notifiable chuẩn (đa hình `notifiable_type/id`, `data` JSON, đa channel, `markAsRead`/`unreadNotifications`) — HRM đã dùng đầy đủ (`EmployeeInfoService::sendNotification` → `->notify(BaseNotification)`, `NotificationService`, `NotificationsController`). `hrm_notifications`=0 vì là bảng đích mới tạo cho Gộp DB. ERP = custom `url/content/receiver_id/status/seen/expired_date`, fan-out mỗi người 1 dòng → 78k. **HRM tốt hơn.**
- **files:** HRM = `table/table_id` + metadata giàu (file_name/type/size/description/attachment_type_id/created_by/solution_version...) — convention bắt buộc CLAUDE.md + `TableFileHelper` + dùng khắp Assign. ERP = morph `fileable`, chỉ name/path/type. **HRM tốt hơn.**

## 3. Quyết định chốt (brainstorm 2026-08-01)
| # | Quyết định |
|---|---|
| Cấu trúc đích | **HRM cho cả 2** (khảo sát: tốt hơn + HRM đã code hoàn chỉnh) |
| notifications DATA ERP | **DROP** 78k (thông báo cũ, ERP dừng; tránh rủi ro đổi PK bigint→uuid) |
| files DATA ERP | **TRANSFORM** 8124 (link file thật, quý) → cấu trúc HRM, giữ data |
| ERP notif/file code | **ngừng hoạt động** (chấp nhận; có thể cần guard tránh crash — follow-up) |
| Script | re-runnable `unify_notif_files.php`, nối pipeline sau `disable_crm.php` |

## 4. notifications — DROP ERP + đổi tên
1. `DROP TABLE notifications` (ERP custom 78k).
2. `RENAME TABLE hrm_notifications TO notifications` (cấu trúc Laravel HRM thành bảng chuẩn).
- Idempotent: nếu `hrm_notifications` không còn → SKIP.

## 5. files — TRANSFORM ERP → cấu trúc HRM
**Map `fileable_type` (ERP class) → `table` (chỉ 8 loại, 7 class + null):**
```
App\Model\Customers\HandoverAcceptanceRecord      => handover_acceptance_records   (7951)
App\Model\Sale\SettlementContract                 => settlement_contracts          (43)
App\Model\Common\DeliveryCostSummaryQuotation     => delivery_cost_summary_quotations (42)
App\Model\Sale\ServiceAccountingRequest           => service_accounting_requests   (19)
App\Model\Sale\QuotationTemplate                  => quotation_templates           (16)
App\Model\Common\PriceListValidDeliveryQuotation  => price_list_valid_delivery_quotations (13)
App\Model\Product\ProductTechAttachment           => product_tech_attachments      (10)
(null fileable_type)                              => 30 dòng — KHÔNG map được
```
**Bước:**
1. **Precheck:** `SELECT DISTINCT fileable_type` — nếu có class NGOÀI map (map chưa đủ) → dừng + báo (tránh bỏ sót).
2. **INSERT vào `hrm_files`** (cấu trúc HRM) từ `files` (ERP), với dòng có `fileable_type` trong map:
   `table = MAP[fileable_type]`, `table_id = fileable_id`, `name = name`, `file_path = path`,
   `file_name = SUBSTRING_INDEX(path,'/',-1)` (basename), `file_type = ` đuôi file (sau dấu `.`),
   các cột metadata còn lại (attachment_type_id, file_size, description, created_by, solution_*, module_*) = NULL.
3. **Dòng `fileable_type` NULL (30):** không migrate → giữ trong bảng archive `erp_files_unmapped` (rename phần còn lại) HOẶC bỏ qua + log. → **chốt: log + để nguyên trong bảng cũ trước khi drop** (xem bước 4).
4. **Archive an toàn:** `RENAME files → erp_files_old` (giữ nguyên 8124 dòng gốc morph, gồm 30 null, phòng cần) — KHÔNG drop hẳn (file S3 vẫn còn, link cũ archive được).
5. **RENAME hrm_files → files.**
- Idempotent: nếu `hrm_files` không còn → SKIP.

*(Ghi chú: bước 4 archive thay vì drop cho files vì là dữ liệu quý; notifications thì drop hẳn.)*

## 6. CODE revert HRM (commit gop_db)
- `app/Models/File.php`: `$table = 'hrm_files'` → `'files'`.
- `app/Models/DatabaseNotification.php`: `$table = 'hrm_notifications'` → `'notifications'`.
- Các ref chuỗi `hrm_files`/`hrm_notifications` (bỏ mysql2): `EmployeeInfo.php`, `Timesheet/Entities/EmployeeInfo.php`, `SolutionService.php`, `SolutionModuleService.php` (join `hrm_files`), `DeleteOldNotification.php` → tên gốc.
- `php -l` sạch; grep sạch.

## 7. ERP ngừng notif/file (follow-up, ngoài script)
- Sau đổi tên, `notifications`/`files` mang cấu trúc HRM → code ERP (morph/custom) query sẽ lỗi cột. ERP chạy trên DB gộp có thể crash trang file/thông báo.
- **Follow-up (khi cần):** guard/tắt code ERP notifications (NotificationHelper) + files (morph File) — hoặc chấp nhận lỗi tới khi recode. KHÔNG thuộc script data này.

## 8. Verify
- `notifications` = cấu trúc Laravel (hrm cũ), `hrm_notifications` drop; HRM tạo/đọc notification (`->notify`, NotificationService) OK.
- `files` = cấu trúc HRM + đã nạp ~8094 dòng ERP transform (table/table_id đúng theo map), `hrm_files` drop, `erp_files_old` giữ 8124 gốc; HRM đọc file (`TableFileHelper`, `files()` relation) OK.
- `php -l` + grep sạch; re-run script → SKIP.

## 9. Re-run / pipeline
```
... → reconcile_auth.php → disable_crm.php → unify_notif_files.php
```
