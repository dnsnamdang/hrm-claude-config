# Gộp lại DB từ dump prod mới + merge ERP master → gop_db (2026-09-18)

Nguồn: `~/Desktop/erp_new.sql` (8.8GB, schema `erp_new`) + `~/Desktop/hrm_production.sql` (3.8GB, schema `hrm_production`).
Quy trình: runbook `hrm-api/Modules/Timesheet/Database/Seeders/GopDb/HUONG-DAN-CHAY.md` (7 bước).

## Bối cảnh môi trường
- MySQL 8.0.42, root@127.0.0.1:3306, datadir `/usr/local/var/mysql` (43GB), đĩa còn ~13GB.
- binlog BẬT (14 file ~14GB) → phải dọn + tắt binlog khi import.
- User CHO PHÉP xoá DB cũ (`erp_new` bản gộp cũ 11GB) để lấy chỗ.

## Task
- [ ] B0. Dọn chỗ: `PURGE BINARY LOGS` + `DROP DATABASE erp_new` (bản gộp cũ)
- [ ] B0b. Tạo schema `erp_new` + `hrm_production`
- [ ] B1. Import `erp_new.sql` → `erp_new` (sql_log_bin=0, max_allowed_packet lớn)
- [ ] B2. Import `hrm_production.sql` → `hrm_production`
- [ ] B3. Verify: đếm bảng + vài bảng chính 2 schema
- [ ] P1. MergeProdSeeder (DRY → APPLY) — GOP_SRC_ERP=erp_new GOP_SRC_HRM=hrm_production
- [ ] P2. ReconcileEmployeesSeeder
- [ ] P3. MergeShareTablesSeeder
- [ ] P4. ReconcileAuthSeeder
- [ ] P5. DisableCrmSeeder
- [ ] P6. UnifyNotifFilesSeeder
- [ ] P7. ReconcileNationsSeeder (DB_DATABASE=erp_new bắt buộc)
- [ ] V. Verify bản gộp: hrm_* biến mất hết trừ 5 bảng TACH, employees ~1095
- [ ] G. ERP git: merge master → gop_db (đang đứng ở gop_db)

## Ghi chú an toàn
- Mọi seeder DRY mặc định; chạy thật cần `GOP_DB_APPLY=1`.
- Chạy reconcile phải kèm `DB_DATABASE=erp_new` (ReconcileNations dùng DB::table() không qualify schema).
