# Đẩy danh mục Giao việc sang DB khác — design (tóm tắt)

**Người phụ trách:** @dnsnamdang · **Nhánh:** `tpe` · **Ngày:** 2026-08-15

## Mục tiêu

Nhiều "cổng" (bản deploy) dùng chung cấu trúc DB. Yêu cầu lặp lại thường xuyên: đưa toàn bộ
dữ liệu **danh mục** của phân hệ Giao việc (`/assign`) từ DB chính sang một cổng khác.
Làm bằng 1 command artisan + 1 nhóm biến env, không phải copy tay từng bảng.

## Scope

**Có:**
- 14 màn thuộc nhóm menu "Danh mục" của `/assign` (`components/menu-sidebar.js:304`);
- nhóm menu "Cấu hình": **Cấu hình duyệt giá** và **Cấu hình chung › tab Quản lý dự án**
  (Mức độ ưu tiên + Cấu hình hạn).

Tổng **28 bảng** (kể cả bảng nối và bảng con).

Cách chốt danh sách: **đi từ mục menu → route FE → route BE → controller → Entity → hỏi Eloquent
`getTable()` + các quan hệ**. Tên bảng đặt thế nào không quan trọng, chỉ code mới là chân lý
(vd "Nhóm ngành" → bảng `scopes`, "Nhóm giải pháp" → bảng `industries`).

**Không có:** màn Khách hàng (`customers`) — user loại trừ rõ ràng. Hai mục "Phương tiện đi lại" /
"Định mức công đi lại" của nhóm Cấu hình cũng không đưa vào. Ba bảng log/lịch sử thay đổi cấu hình
(`bom_price_approval_config_logs`, `priority_level_history`, `assign_deadline_config_history`)
không đẩy — chúng trỏ `user_id` cổng nguồn, sang đích sẽ hiện sai người.
Cũng không đụng các bảng `*_snapshots` (form_template_snapshots, form_section_snapshots,
form_question_snapshots, form_question_option_snapshots, form_group_snapshots) — đó là
bản chụp của phiếu đã dùng trong nghiệp vụ, không phải danh mục.

## Quyết định lớn (user chốt)

| Vấn đề | Chốt |
|---|---|
| Cách ghi | **Mirror 1:1** — xoá sạch bảng ở đích rồi chèn lại từ nguồn, **giữ nguyên `id`**, reset `AUTO_INCREMENT` |
| Bản ghi chỉ có ở đích | **Xoá** (hệ quả của mirror) |
| `created_by` / `updated_by` | Tra `employees.email = SYNC_CATALOG_AUDIT_EMAIL` **trên DB ĐÍCH** → lấy `id`; không thấy thì `NULL` |
| Phạm vi | 14 màn nhóm Danh mục (trừ Khách hàng) + Cấu hình duyệt giá + tab Quản lý dự án |
| Cấu hình hạn (`general_regulations`) | **Không mirror** — chỉ UPDATE 8 cột liên quan, khớp theo `company_id` |
| Bảng log/lịch sử cấu hình | Không đẩy |

Giữ nguyên `id` là điểm mấu chốt: các bảng nối (`industry_scopes`, `application_*`,
`customer_scope_group_members`) và dữ liệu nghiệp vụ ở đích đều trỏ theo `id`.

## Rủi ro đã biết

Mirror sẽ xoá bản ghi danh mục **chỉ tồn tại ở đích**. Nếu dữ liệu nghiệp vụ ở đích đang
tham chiếu chúng thì thành mồ côi. Hai quan hệ FK thực tế đang có:
`quotation_discounts.discount_type_id → discount_types` và
`form_question_options.form_question_id → form_questions`.
Command **in cảnh báo liệt kê id sắp bị xoá mà đang bị tham chiếu** trước khi hỏi xác nhận.

## Kiến trúc

- **Connection `mysql_target`** (`config/database.php`), biến `DB_*_TARGET` — bám đúng
  style các connection sẵn có `mysql_tpe` / `mysql_etek_*`.
- **Key `database.sync_catalog_audit_email`** — đọc qua `config()` chứ không `env()` trực
  tiếp trong command, để không hỏng khi chạy `config:cache`.
- **Command `assign:sync-catalogs`** — `app/Console/Commands/Assign/SyncAssignCatalogsCommand.php`
  (cùng thư mục các command Assign hiện có, Kernel tự `load()` đệ quy).

Danh sách bảng hard-code trong hằng `TABLES` theo thứ tự phụ thuộc cha → con;
insert xuôi, truncate ngược. Nhóm `survey_*` phải đứng **trước** nhóm `form_*`
(`form_groups.survey_question_id`, `form_questions.survey_question_id`).
Bảng không tồn tại ở nguồn hoặc đích được tự bỏ qua (vd `project_phase_items`).

Riêng **`general_regulations`** đi nhánh `syncGeneralRegulation()`: bảng này là Quy định chung của
phân hệ **Chấm công** (40 cột: `base_salary`, `timekeeping_max_distance`, `min_days_for_insurance`…),
Cấu hình hạn chỉ ghi ké 8 cột. Mirror cả bảng sẽ ghi đè cấu hình lương/chấm công của cổng đích, nên
chỉ `UPDATE` 8 cột đó, khớp dòng theo `company_id`, không truncate và không insert dòng mới
(công ty đích chưa có dòng Quy định chung → bỏ qua kèm cảnh báo).

## Chốt an toàn

1. Chưa cấu hình `DB_DATABASE_TARGET` → dừng.
2. Không kết nối được DB đích → dừng.
3. DB đích trùng đúng host + port + database với DB nguồn → dừng (tránh tự xoá dữ liệu).
4. Mặc định hỏi xác nhận; `--force` để bỏ qua, `--dry-run` chỉ in số liệu.
5. `SET FOREIGN_KEY_CHECKS = 0` khi ghi, bật lại trong `finally`.
6. Dùng `DELETE` + **1 transaction cho cả lượt đẩy** (không dùng `TRUNCATE` — DDL, implicit-commit
   sẽ phá transaction). Lỗi ở bảng bất kỳ → rollback sạch, đích giữ nguyên dữ liệu cũ.
   Vì `DELETE` không reset con trỏ id, sau khi commit chạy `ALTER TABLE ... AUTO_INCREMENT =
   max(id)+1` cho mọi bảng có cột auto_increment.
6b. `created_by`/`updated_by`: không tra được nhân viên (`$auditId = null`) thì chỉ ghi `NULL` vào
   cột **nullable ở đích**; cột NOT NULL **giữ nguyên giá trị nguồn** + cảnh báo — ghi `NULL` vào
   cột NOT NULL làm insert chết giữa chừng sau khi đã xoá dữ liệu đích.
7. Chỉ copy **cột giao nhau** giữa 2 schema; cột lệch chỉ in cảnh báo, không chết giữa chừng.

## Cách dùng

```bash
# xem trước, không ghi gì
php artisan assign:sync-catalogs --dry-run

# chạy thật (có hỏi xác nhận)
php artisan assign:sync-catalogs

# chỉ đẩy vài bảng, không hỏi
php artisan assign:sync-catalogs --tables=scopes,industries,applications --force
```

Spec chi tiết: `docs/superpowers/specs/2026-08-15-sync-assign-catalogs-design.md`
