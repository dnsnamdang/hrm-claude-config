# Đẩy danh mục Giao việc sang DB khác — plan

@dnsnamdang · nhánh `tpe`

## Phase 1 — Command đẩy danh mục

### BE

- [x] Thêm connection `mysql_target` vào `config/database.php` (biến `DB_*_TARGET`)
- [x] Thêm key `database.sync_catalog_audit_email` (đọc qua `config()`, an toàn với `config:cache`)
- [x] Bổ sung block config mẫu vào `.env.example` + `.env` local
- [x] Tạo command `assign:sync-catalogs` — `app/Console/Commands/Assign/SyncAssignCatalogsCommand.php`
- [x] Khai báo bảng danh mục theo thứ tự phụ thuộc cha → con (trừ `customers` và `*_snapshots`)
- [x] Rà lại danh sách bằng cách trace menu → route → controller → Entity → `getTable()` + quan hệ
      (không suy từ tên bảng) → bổ sung `form_groups`, `project_phase_items`; chuyển nhóm
      `survey_*` lên **trước** nhóm `form_*`. Tổng 26 bảng.
- [x] Chốt an toàn: thiếu config / không kết nối được / đích trùng nguồn → dừng
- [x] Bảng xem trước số dòng 2 bên + cảnh báo cột lệch schema
- [x] Cảnh báo id sắp xoá đang bị `quotation_discounts` / `form_question_options` tham chiếu
- [x] Tra `employees.email` trên DB đích → ghi đè `created_by` / `updated_by`
- [x] Mirror: `FOREIGN_KEY_CHECKS=0` → truncate ngược → chunk-insert xuôi → bật lại FK trong `finally`
- [x] Option `--tables` / `--dry-run` / `--force` / `--chunk`

### Kiểm thử

- [x] `php -l` cả 2 file
- [x] Guard thiếu `DB_DATABASE_TARGET` → dừng đúng
- [x] Guard đích trùng nguồn → dừng đúng
- [x] `--dry-run` in đúng số dòng 26 bảng, không ghi gì
- [x] Chạy thật vào DB test `hrm_sync_target_test`: 25/26 bảng ghi đủ
- [x] Bảng không tồn tại (`project_phase_items`) được bỏ qua kèm ghi chú, không làm chết command
- [x] Bản ghi rác chỉ có ở đích (`discount_types` id 999999) đã bị xoá — mirror đúng
- [x] `id` ở đích khớp hệt nguồn
- [x] `created_by` / `updated_by` = id nhân viên **ở DB đích** (3200), không phải id nguồn (13)
- [x] `FOREIGN_KEY_CHECKS` được trả về 1 sau khi chạy
- [x] Dọn DB test, trả `DB_DATABASE_TARGET` về rỗng

## Phase 2 — Bổ sung nhóm menu Cấu hình

### BE

- [x] Trace menu Cấu hình → route → controller → Entity → `getTable()`:
      Cấu hình duyệt giá = `bom_price_approval_configs`; tab Quản lý dự án ›
      Mức độ ưu tiên = `priority_levels`; tab Quản lý dự án › Cấu hình hạn = `general_regulations`
- [x] Thêm `bom_price_approval_configs` + `priority_levels` vào `TABLES` (mirror như các bảng khác)
- [x] Nhánh riêng `syncGeneralRegulation()` — chỉ UPDATE 8 cột Cấu hình hạn, khớp theo `company_id`,
      không truncate/insert (bảng này là Quy định chung của Chấm công, chứa cả `base_salary`)
- [x] `--tables` nhận thêm `general_regulations`; mặc định vẫn chạy cả 2 nhánh
- [x] Không đẩy 3 bảng log/lịch sử cấu hình (trỏ `user_id` cổng nguồn)
- [x] Kiểm tra `exists()` trước `update()` (update trả 0 khi giá trị đã trùng → suy ra "thiếu dòng" là sai)

### Kiểm thử Phase 2

- [x] `--dry-run` in đủ 28 bảng + khối xem trước Cấu hình hạn (6 công ty nguồn / 5 đích)
- [x] Chạy thật: `bom_price_approval_configs` 6 dòng, `priority_levels` 4 dòng
- [x] Cấu hình hạn cập nhật đúng theo `company_id` (task_due_days 5 / issue_due_days 7 sang đúng cty 1, 4)
- [x] `base_salary` 99.999.999 + `timekeeping_max_distance` 77 của đích **giữ nguyên**, không bị ghi đè
- [x] company_id 8 (đích chưa có dòng Quy định chung) bỏ qua kèm cảnh báo, không tự tạo
- [x] 3 bảng log/lịch sử không xuất hiện trong danh sách chạy
- [x] `--tables=general_regulations` chỉ chạy nhánh Cấu hình hạn
- [x] Trả DB nguồn `hrm_prod_local` về nguyên trạng sau khi sửa để test (task_due_days/issue_due_days = 0)
- [x] Dọn DB test, trả `DB_DATABASE_TARGET` về rỗng

## Phase 3 — Test kỹ + sửa lỗi phát hiện được

### Lỗi tìm được khi test sâu

- [x] **Mất dữ liệu khi email audit không tra được**: `$auditId = null` → ghi `NULL` vào `created_by`
      NOT NULL → insert chết, mà bảng đích đã bị truncate → mất sạch. Sửa: cột NOT NULL giữ nguyên
      giá trị nguồn + cảnh báo; đọc tính nullable từ `information_schema` của DB **đích**
- [x] **Không có đường lùi khi lỗi giữa chừng**: đổi `TRUNCATE` (DDL, implicit-commit) → `DELETE`
      (DML) và bọc cả lượt đẩy trong 1 transaction → lỗi ở đâu cũng rollback sạch
- [x] **`DELETE` không reset id**: thêm `resetAutoIncrement()` chạy sau commit —
      `ALTER TABLE ... AUTO_INCREMENT = max(id)+1` cho mọi bảng có cột auto_increment
- [x] Chuyển `resolveAuditEmployeeId()` lên **trước** bước hỏi xác nhận
- [x] Đính chính: kiểm chứng `@@FOREIGN_KEY_CHECKS = 1` ở Phase 1 là **vô nghĩa** (đọc từ phiên
      mysql CLI khác, trong khi đó là biến session của kết nối command)

### Kiểm thử Phase 3

- [x] Cảnh báo mồ côi: dựng quotation + discount_type chỉ có ở đích → cảnh báo in đúng id
- [x] Prompt xác nhận: trả lời `no` → huỷ, dữ liệu không đổi; `yes` → chạy
- [x] `--tables` chứa bảng lạ → báo lỗi + in danh sách hợp lệ
- [x] `--chunk=3` → chia nhiều vòng, kết quả vẫn khớp checksum
- [x] Schema lệch (đích DROP cột + thêm cột lạ) → cảnh báo 2 chiều, vẫn ghi đủ
- [x] Rollback: ép `project_roles.name` VARCHAR(1) → lỗi → 3 bảng khác giữ nguyên số dòng
- [x] Checksum MD5 toàn bộ cột từng bảng (không chỉ `id`): 27/27 khớp
- [x] AUTO_INCREMENT = `max(id)+1` của nguồn ở 7 bảng kiểm tra

### Chạy trên DB thật `etek_power_hrm` (619 bảng)

- [x] `--dry-run` phát hiện đích thiếu cột `form_templates.code` → bỏ cột, không chết
- [x] Chạy thật: 27 bảng ghi đủ, không lỗi
- [x] Checksum toàn bộ cột từng bảng: **27/27 khớp**
- [x] AUTO_INCREMENT khớp `max(id)+1` nguồn ở 7 bảng kiểm tra
- [x] Cấu hình hạn: đích thiếu 2 cột `meeting_report_*` → chạy 6/8 cột, `base_salary` /
      `timekeeping_max_distance` của đích giữ nguyên; 5 công ty thiếu dòng bỏ qua kèm cảnh báo

### Chưa kiểm chứng

- [ ] `created_by` trên `etek_power_hrm` không phân biệt được "tra ở đích" vs "copy nguồn"
      (email trùng `id = 13` ở cả 2 DB) — bằng chứng nằm ở DB test (3200 ≠ 13)
- [ ] Guard "đích trùng nguồn" với cùng tên DB nhưng khác host
- [ ] DB đích đặt ở máy khác (mới toàn localhost)

### Checkpoint — 2026-08-15
Vừa hoàn thành: Phase 1 (danh mục) + Phase 2 (Cấu hình) + Phase 3 (test sâu, sửa 3 lỗi),
đã chạy thật thành công trên `etek_power_hrm` với checksum 27/27 khớp.
Đang làm dở: không có.
Bước tiếp theo: `.env` đang trỏ `DB_DATABASE_TARGET=etek_power_hrm` — đổi sang cổng khác khi cần.
Blocked:
