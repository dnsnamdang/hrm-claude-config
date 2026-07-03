# TỔNG KẾT — Di trú công ty thành viên vào cổng TPE

> File tra cứu chính. Gồm: (A) cách chạy, (B) toàn bộ thay đổi đã làm, (C) các quyết định quan trọng.

## 📁 Các file tài liệu liên quan
| File | Nội dung |
|------|----------|
| `runbook.md` | Hướng dẫn chạy (tổng quát) |
| `prod-runbook.md` | Hướng dẫn chạy **PRODUCTION** (backup, bảo trì, rollback) |
| `audit-phan-he.md` | Đánh giá từng phân hệ: cái nào chuyển/dùng chung |
| `plan.md` | Nhật ký chi tiết từng phase (6 → 6i) |
| `TONG-KET.md` | **File này** — tổng kết + changelog |

---

# A. CÁCH CHẠY (rút gọn)

## 1 lệnh duy nhất cho 1 công ty
```bash
php artisan config:clear
# Thử:
php artisan company:migrate-full --source-db=<DB_nguồn> --run=<nhãn> --rice-parent=<2|3|4> --dry-run
# Thật:
php artisan company:migrate-full --source-db=<DB_nguồn> --run=<nhãn> --rice-parent=<2|3|4> --confirm
```
Ví dụ ETEK GREEN: `--source-db=local_hrm_green --run=etekgreen --rice-parent=2`
(POWER: rice-parent=3 ; ETEK: rice-parent=4)

**Lệnh này tự làm 5 bước:** [1] HR (hồ sơ + tổ chức + lương + phân quyền + danh mục KH + phân ca + bù phép + hạ quyền) → [2] re-link cơm → [3] enroll cơm → [4] **recode** (set branch_order=id + đánh lại mã NV/chấm công/cơm về 1 chuẩn TPE) → [5] **đẩy ERP** (mirror company/department/part/employee sang DB ERP `mysql2`). (Tắt: `--no-recode`, `--no-erp`.)

## Sau khi chạy thật: thêm 1 dòng config (lệnh đã in nhắc)
```php
// config/company_migration.php
'leave_recompute_skip' => [ <company_id mới> => <năm cutover> ],
```

## Chạy CƠM cho nhiều công ty 1 lượt (nếu đã seed HR riêng)
```bash
php artisan company:finalize-rice            # tất cả công ty trong rice_relink_map
php artisan company:finalize-rice --run=etekpower   # 1 công ty
```

---

# B. TOÀN BỘ THAY ĐỔI ĐÃ LÀM

## B1. Lệnh (command) MỚI — `app/Console/Commands/`
| Lệnh | Công dụng | Dùng khi |
|------|-----------|----------|
| `company:migrate-full` | **1 lệnh chạy hết** HR + cơm + recode (tự set connection nguồn) | Chạy mới 1 công ty |
| `company:recode-unified` | Set branch_order=id + đánh lại mã NV/chấm công(ssn)/cơm(rice_ssn) về 1 chuẩn TPE (`branch_order+YY+seq`); ghi `employee_code_mappings` | Sau di trú / chạy tay |
| `company:sync-erp` | Đẩy company/department/part/employee_infos/employees sang ERP (`mysql2`) theo cùng id; reconcile tên trùng (vd placeholder cũ); FK-off khi đẩy | Sau recode / chạy tay |
| `company:finalize-rice` | Relink + enroll cơm cho NHIỀU công ty (tự suy id) | Sau khi seed HR |
| `company:relink-rice` | Đưa cơm cũ về tenant TPE (1 công ty) | Chạy tay |
| `company:enroll-rice` | Tạo rice record NV phòng-có-cơm còn thiếu | Chạy tay |
| `company:migrate-tables` | Di trú BỔ SUNG 1 tập bảng cho công ty ĐÃ di trú | Vá sau |
| `company:fold-used-leave` | Bù phép đã dùng (công ty di trú trước bản fix) | Vá sau |
| `company:downgrade-permissions` | Hạ quyền tổng-công-ty → theo-công-ty | Vá sau |

> 3 lệnh "vá sau" CHỈ cần khi công ty đã lỡ di trú TRƯỚC khi có tính năng. Chạy mới thì runMigration tự làm.

## B2. Engine — `app/Services/CompanyMigration/CompanyMigrationService.php`
- `foldPreCutoverUsedLeave()` — bù phép đã dùng vào `number_day_leave_outside`. Gọi tự động post-commit trong `runMigration`.
- `downgradeGroupScopePermissions()` — hạ quyền "tổng công ty"→"theo công ty". Gọi tự động post-commit (config `downgrade_group_scope_on_migrate=true`).
- `runMigrationForTables()` + `loadParentOldIdsFromMap()` + `cleanupMapForTables()` — di trú bổ sung 1 tập bảng, tái dùng map run cũ.
- `stepAllocateIds()` — thêm tham số `$seedChosen` (nạp old_id cha từ map run cũ).
- `selectOldIdsParent()` — thêm filter `date_from_today` (chỉ lấy dòng ≥ hôm nay — roster phân ca tương lai).
- `selectOldIdsNonParent()` + `personOwnerFkColumns()` — **cascade loại child** theo người bị loại (vd dòng của tài khoản trùng email): loại dòng có `employee_id`/`employee_info_id` trỏ người bị loại (chỉ cột chủ-sở-hữu, KHÔNG đụng lead/deputy).
- **Fix bug**: idempotent guard `runMigrationForTables` chặn CẢ dry-run (trước dry-run xóa nhầm map thật).

## B3. Config — `config/company_migration.php`
- **6 bảng CRM → `owned`** (bỏ khỏi `skip`): customers, customer_scopes, customer_scope_groups, scopes, industries, industry_scopes. Bật qua cờ `MIGRATE_CRM`.
- **2 bảng phân ca → `owned`** (bỏ khỏi `skip`): shift_detail_employees, shift_detail_employee_dates (có `date_from_today` → chỉ roster tương lai).
- `'leave_recompute_skip'` — `[company_id => năm]`: chặn cron `update:attendance` tính lại làm hỏng số dư phép công ty di trú.
- `'downgrade_group_scope_on_migrate' => true` — bật/tắt tự hạ quyền khi di trú.
- `'rice_relink_map'` — `[run_id => parent_id cơm cũ]`: để `company:finalize-rice` tự chạy nhiều công ty.

## B4. Sửa BUG trong app (ngoài engine di trú)
| File | Sửa | Lý do |
|------|-----|-------|
| `Modules/Timesheet/Services/EmployeeAttendanceService.php` | Guard `shouldSkipMigratedRecompute()` ở updateData/updateDataAll/handleUpdateData | Cron tính lại phép không đạp công ty di trú |
| `Modules/Timesheet/Transformers/TimekeepingExemptionResource/TimekeepingExemptionResourceListResource.php` | Null-guard dòng 30/32/34/36 | Màn miễn chấm công crash khi employee null |
| `Modules/Rice/Services/PersonalRegistration/PersonalRegistrationService.php` | Guard `riceUser()` null (index + checkUserInvitation) | Màn đăng ký cơm crash với NV không-đăng-ký |
| `Modules/Rice/Services/MasterData/MasterDataService.php` | Guard `riceUser()` null ở getRiceUserProfile | API rice-user-profile crash với NV không-đăng-ký |

## B5. `.env`
- `MIGRATE_CRM=true` (trước là false) — bật di trú danh mục Khách hàng/Ngành.

## B6. Quy tắc sinh mã NV / chấm công / cơm (sau di trú)
- **Mã thống nhất** = `branch_order + YY(năm vào làm) + seq` — gộp 3 mã về 1: `employee_infos.code` = `employee_infos.ssn` = `employees.rice_ssn` = `rice_employee_infos.code/rice_ssn`.
- **`branch_order` công ty gộp = id** (vd ETEK GREEN id=9 → branch_order=9 → prefix mã = 9). Command `company:recode-unified` tự set + đánh lại.
- **`seq` chung toàn hệ thống** (nối tiếp max, không reset theo công ty). `SYNC_SEQ_START` = điểm bắt đầu + độ rộng padding.
- Sửa `EmployeeInfoService::generateNewEmployeeCodeAndSsn` + `EmployeeImport::generateNewEmployeeCodeAndSsn`: branchIndex dùng **`branch_order` cố định** (fallback thứ hạng nếu null) → NV tạo mới khớp với data đã recode.
- Bảng `employee_code_mappings` (old↔new) để đối chiếu/rollback.
- ⚠️ Sau recode `rice_ssn` đổi → cần **đẩy lại khuôn mặt** lên máy chấm công.

## B7. Đồng bộ sang ERP (`mysql2` = DB_DATABASE_SECOND)
- Engine di trú INSERT thẳng → **bỏ qua hook đồng bộ ERP** → ERP KHÔNG tự có data mới. Command `company:sync-erp` bù.
- ERP soi gương HRM theo **cùng id**: `companies`→TpCompany, `departments`→TpDepartment, `employee_infos`→SyncEmployeeInfoToErpJob (gồm code/ssn), `employees`→SyncEmployeeToErpJob. **Parts**: hook app đã tắt nhưng `employee_infos.part_id` có FK → command vẫn đẩy parts.
- **Reconcile**: ERP là DB trung tâm dùng chung, đã có data cổng cũ (vd placeholder "ETEK GREEN" id=7). Migration đổi tên ở HRM nhưng chưa sang ERP → command tự đẩy tên/code mới cho công ty trùng trước khi chèn công ty mới.
- **FK-off** (`SET FOREIGN_KEY_CHECKS=0`) khi đẩy: tránh fail do FK vòng (employees↔employee_infos) + bảng cha phụ (employee_positions/teams) chưa có.
- Verify ETEK GREEN: ERP có company 9 + 14 dept + 45 parts + 123 NV; mã recode khớp 123/123 (HRM==ERP).

---

# C. CÁC QUYẾT ĐỊNH QUAN TRỌNG

1. **Phân loại bảng**: CÓ `company_id` = riêng → CHUYỂN (94 bảng owned); KHÔNG có = dùng chung của đích (9 bảng shared: địa lý, bank, quyền, ngành nghề); giao dịch theo kỳ + config global = KHÔNG chuyển (185 bảng skip).
2. **Phép**: bù phép đã dùng năm cutover vào `number_day_leave_outside` (vì bảng chấm công kỳ cũ không chuyển).
3. **Phân ca**: chỉ đưa roster TƯƠNG LAI (từ hôm nay), bỏ kỳ cũ.
4. **Quyền**: hạ "tổng công ty" → "theo công ty" để NV không xem chéo công ty khác.
5. **Cơm**: phân hệ cơm vốn đã CHUNG DB TPE → không di trú, chỉ **re-tag** dữ liệu cũ (parent 2→1) + **bù rice record NV thiếu**. Config cơm (menu/settings) dùng chung trung tâm TPE — tự động.
6. **Người trùng email** (vd DNS Admin): bỏ qua khi di trú; child của họ cũng bị loại (cascade).

---

# D. VẬN HÀNH PRODUCTION (tóm tắt — chi tiết ở prod-runbook.md)
1. **Backup `hrm_production`** trước mỗi công ty.
2. Chạy thử trên **COPY** trước, rồi prod thật trong **cửa sổ bảo trì**.
3. Prod bật `config:cache` → sửa .env phải `config:clear`, xong thì `config:cache` lại.
4. Sau khi xong: gỡ domain cổng thành viên khỏi `RICE_REGISTER_DOMAINS`.
5. Rollback = khôi phục từ backup.

---

# E. LƯU Ý / VIỆC NGOÀI SCOPE
- Mật khẩu tạm `Test@12345` từng đặt cho uyendtt.hr + EG-001 (chỉ trên data cũ — đã reset).
- Endpoint `/timekeeping-exemptions` không lọc theo công ty (phân quyền sẵn có của app, không phải lỗi di trú).
- Màn thâm niên: nếu nguồn có `suspend_labor_contracts`/`employee_disciplines`/`increase_seniority_employees` → có thể tính dư (xử lý tay; ETEK GREEN nguồn rỗng nên không bị).
