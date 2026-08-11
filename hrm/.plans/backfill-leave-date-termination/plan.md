# Backfill ngày nghỉ việc từ QĐ chấm dứt HĐLĐ

- [x] BE: Seeder `Modules/Decision/Database/Seeders/BackfillLeaveDateFromTerminationSeeder.php` — set `employee_infos.leave_date` = `termination_date_start` của QĐ chấm dứt HĐLĐ đã duyệt cuối cùng, cho nhân sự `status=0` & `leave_date IS NULL`; hỗ trợ dry-run, idempotent (đã test trên DB local).
