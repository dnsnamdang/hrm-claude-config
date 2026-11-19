# Runbook go-live — Vai trò & Quyền giai đoạn 1

> **01/11/2026:** bản chạy theo, rút gọn cho cửa sổ bảo trì: `cua-so-go-live-nhanh.md` (cùng folder). File này vẫn là nguồn chi tiết + mục C.

> Nguồn: review cuối toàn nhánh `rbac` (26/10/2026, `wt-rbac/hrm-api/.superpowers/sdd/plan/final-review.md`) + các quyết định user trong ledger.
> Mọi bước ghi DB / đụng source vẫn phải hỏi user và nhận "làm" theo CLAUDE.md gốc.

## 0. Điều kiện tiên quyết

- **Giai đoạn 1 KHÔNG lên prod một mình.** Từ lúc deploy, màn phân quyền cũ ở cả 2 app trả 403 (đã thay bằng màn Vai trò mới ở giai đoạn 2). User đã chốt: xong cả 4 giai đoạn, test ok mới lên prod một lần.
- **Code mới và dữ liệu đã chuyển đổi phải đi cùng nhau.**
  - Code mới chạy trên DB chưa chuyển đổi ⇒ `permission_aliases` rỗng ⇒ mọi kiểm quyền trả false ⇒ khoá toàn bộ người dùng.
  - DB đã chuyển đổi chạy code cũ ⇒ code cũ đọc `role_has_permissions.company_id` (đã bỏ) ⇒ lỗi.
- **Deploy ERP tự chạy khi push `gop_db`** (`TanPhatDev/.github/workflows/deploy.yml`) ⇒ chỉ merge/push nhánh `rbac` vào `gop_db` **trong cửa sổ bảo trì**, đúng bước B6.
- **Các tenant HRM khác trên cùng VPS** — user chốt 26/10: **etek** và **toyota** **chạy giống hệt TPE**; **etekgreen, etekpower bị loại** (đã dùng chung cổng/DB TPE — đi cùng lần chuyển đổi của TPE).
- Công cụ chuyển dữ liệu công ty (`config/company_migration.php`): mục `permissions` đã khớp theo `code`; mục `roles` / `role_has_permissions` CHƯA theo dạng dữ liệu mới — nếu dùng lại công cụ sau go-live phải sửa trước. Mỗi DB tenant đi đủ: migration `gop_db` còn chờ → 5 migration `2026_11_01_*` → `rbac:convert` (dry-run rồi chạy thật), trong cùng cửa sổ bảo trì với lần deploy code mới cho tenant đó.
  - Trước cửa sổ: diễn tập dry-run trên bản sao **từng** DB tenant. Tên quyền có trong DB tenant mà không có trong danh mục ⇒ lệnh dừng `missing` ⇒ phải khai vào danh mục (hoặc `dropped_legacy.php`) trước. Mã công ty của tenant quyết định tiền tố tên vai trò.
  - Tenant không có ERP: cờ `--erp-da-bao-tri` vẫn phải truyền (chỉ là xác nhận), bỏ bước B6/ERP.
  - Danh sách cấp lại quyền (bước A.3) làm riêng cho từng tenant từ báo cáo của DB đó.

> **Quyết định user 30/10/2026: đợt go-live đầu CHỈ TPE — chưa cập nhật etek, toyota.** Hệ quả: sau khi `rbac` vào `gop_db`, etek/toyota
> **không được deploy/kéo code `gop_db` mới** cho tới khi làm cửa sổ chuyển đổi riêng cho tenant đó (code mới + DB chưa chuyển đổi ⇒ khoá
> toàn bộ người dùng). Trước giờ G: xác nhận etek/toyota không có cơ chế tự kéo `gop_db`.

## A. Trước cửa sổ bảo trì (vài ngày trước)

1. **Đóng băng quyền:** không thêm/đổi tên quyền, không merge nhánh thêm quyền vào `gop_db`. Nhánh `rbac` chưa vào `gop_db`.
2. **Diễn tập trên bản sao prod mới nhất (cùng ngày nếu được)** — DB `hrm_erp_rbac_rehearsal`:
   1. `php artisan migrate:status` ⇒ chạy **mọi** migration `gop_db` còn chờ trước (vd `2026_10_22_*`, `2026_10_23_*`: bản `2026_10_22_000003` ghi `role_has_permissions.company_id` nên phải chạy TRƯỚC chuyển đổi).
   2. Chạy lẻ 5 migration bằng `--path` (xem `--pretend` trước): `2026_11_01_000001` … `000005`.
   3. `php artisan rbac:convert --dry-run --report-dir=… --scope-decisions=<scope-decisions.csv>` — cổng: mã thoát 0, `chenh-lech-khac.csv` chỉ có tiêu đề.
   4. Phát lại cho quản trị viên các danh sách từ **lần chạy này** (không dùng số 25/10): `mat-do-bit-ro`, `mat-do-cong-ty-qua-vai-tro` (cột "dùng được trên giao diện"), `thieu-quyen-xem`, `du-lieu-tro-role-id`, `vai-tro-khong-chuyen`.
   5. Chạy thật trên DB diễn tập ⇒ `permission:catalog-sync --dry-run` phải 0 thay đổi ⇒ trỏ 2 app vào DB diễn tập, chạy 2 bộ test Rbac ⇒ Playwright 3 tài khoản (1 công ty, 2 công ty, Super Admin), đếm menu/nút khớp CSV. Ghi thời gian chạy chuyển đổi và thời gian `mysqldump`.
3. ~~**Quản trị viên cấp lại quyền trong hệ thống CŨ** theo danh sách bước 2.4 (sau go-live không có màn sửa quyền tới giai đoạn 2).~~
   **[Lỗi thời 01/11]** GĐ2/GĐ2b đã có màn sửa quyền (`/admin/roles`, `/admin/employee-roles`) đi cùng đợt ⇒ dời việc cấp lại sang SAU go-live, trên hệ thống mới. Phần báo trước Super Admin bên dưới vẫn giữ. Báo trước người dùng Super Admin: đã bỏ mọi đặc quyền (quyết định 25–26/10) — gồm cả ô chọn mọi phòng ban, thủ kho/kế toán mọi kho, mọi hãng ở bộ lọc NCC PI, bỏ qua người mua/người duyệt/phân vùng, mở nháp người khác, bỏ qua hạn xử lý.
4. **Sửa script e2e + seeder** đang dựa vào vai trò 18 / tên "Super Admin" / `role_has_permissions.company_id` (chờ user cho phép).

## B. Trong cửa sổ bảo trì

1. **Hạ 2 app:** hrm-api `php artisan down --secret=<token>`; ERP `php artisan down --allow=<IP quản trị>`. Tắt cron (`schedule:run` của `erp_tpe` và cron ERP).
2. **Sao lưu:** `mysqldump` đầy đủ `hrm_erp_gop` trên 192.168.122.103. **Đây là điểm khôi phục chính.**
3. **Deploy hrm-api** (capistrano: composer, `migrate`, restart worker). Cổng: `migrate:status` không còn bản chờ, 7 migration đợt này đã chạy (`2026_11_01_000001..000005`, `2026_11_02_000001`, `2026_11_02_000010`), `permission_aliases` = 0 dòng.
   - **GĐ2c (01/11):** trước deploy, thêm `RBAC_GROUP_SCOPE_ADMINS=13` vào `.env` HRM prod (`/var/www/tpe/hrm-api`), sau deploy `config:cache`.
     Migration `2026_11_02_000010_add_allow_group_scope_to_companies` chạy cùng loạt này (chỉ thêm cột, mặc định 1 — hành vi không đổi;
     trước hay sau `rbac:convert` đều được). Cổng: `SELECT COUNT(*) FROM companies WHERE allow_group_scope <> 1` = 0.
     Code chịu được khi chưa có cột (coi như mọi công ty được phép), nên lệch thứ tự deploy/migrate không làm hỏng kiểm quyền.
4. **Chuyển đổi** (user `erp_tpe`, `/var/www/tpe/hrm-api`):
   `php artisan rbac:convert --erp-da-bao-tri --report-dir=storage/app/rbac-convert/golive --scope-decisions=<csv>`
   (lệnh từ chối chạy thật nếu hrm-api chưa `down` hoặc thiếu cờ `--erp-da-bao-tri`). Ngay sau đó:
   `php artisan rbac:convert --print-rollback --report-dir=storage/app/rbac-convert/golive > rollback.sql` (chỉ in, giữ cùng `cau-truc-goc-bak-rbac.json` trong thư mục báo cáo).

   | Mã thoát | Nghĩa | Làm gì |
   |---|---|---|
   | 0 | Xong | Đi tiếp |
   | 2 | `chenh-lech-khac` khác rỗng, dữ liệu đã huỷ, còn `bak_rbac_*` | Điều tra, xoá `bak_rbac_*`, chạy lại hoặc huỷ go-live |
   | 1 trước commit | Dữ liệu chưa đổi | Xoá `bak_rbac_*` / `rbac_new_*` / `rbac_role_map` rỗng, huỷ hoặc chạy lại |
   | 1 kèm "DDL lỗi" | Dữ liệu đã commit, DDL chưa xong | Sửa nguyên nhân rồi `rbac:convert --resume-ddl --erp-da-bao-tri --report-dir=…/golive` (cũng cần hrm-api đang down) |
5. **Kiểm bằng SQL** (sau B.4b): `role_has_permissions` không còn `company_id`; `roles.company_id` NOT NULL + unique `(company_id, base_name)`; `rbac_role_map` có dòng; số dòng khớp diễn tập. Rồi `permission:catalog-sync --dry-run` = 0 thay đổi.
5b. **Cấp mã GĐ3b** (sau bước 5, trước khi tắt 6 công ty GĐ2c và trước deploy ERP): `rbac:grant-role-name-codes --dry-run` ⇒ chạy thật ⇒ `--verify` "Dòng lệch: 0" ⇒ xoá cache quyền như B.4b. Lệnh chỉ thêm `role_has_permissions` vào Vai trò mang tên Tổng giám đốc / Giám đốc / Ban giám đốc / Kế toán / Chăm sóc khách hàng / Quản lý / Quản lý đào tạo (bảng `RoleNameCodeMap`), chạy lại không nhân bản. Rehearsal 02/11: 18 Vai trò · thêm 85; verify 20 dòng lệch đều của 2 employee_id không tồn tại (mồ côi, B.4b dọn) ⇒ lệch thật 0. Chi tiết + lui: `cua-so-go-live-nhanh.md` khối 5b.
6. **Deploy ERP:** merge/push `rbac` vào `gop_db` TanPhatDev lúc này (workflow: `git pull`, `composer install --optimize-autoloader`, `migrate`, `config:cache`, `route:cache`, `view:cache`, `queue:restart`, `optimize`). Rồi `sudo systemctl reload apache2`.
7. **Cache:** HRM — chuyển đổi đã xoá cache spatie. ERP — cache spatie 0 giây. **Không** `cache:clear` trên Redis dùng chung.
8. **Khởi động lại worker sau chuyển đổi:** HRM `sudo supervisorctl restart laravel-worker:*`; ERP `php artisan queue:restart`.
9. **Smoke test** qua đường bypass bảo trì: 3 tài khoản Playwright trên 2 app + đăng nhập TPE_APP (`permissions[].name` phải là tên cũ). So số với diễn tập.
10. **Mở 2 app** (`php artisan up`), bật lại cron.

### B.4b. Sau chuyển đổi — dữ liệu tài khoản (GĐ2b, user chốt 27/10)

Chạy ngay sau B4 (cần `bak_rbac_*` còn nguyên), trước B5. Diễn tập ở bước A.2.5 chạy đúng các câu này trên DB diễn tập.

1. **Kiểm: tài khoản đang hoạt động thiếu dòng `company_employees` ở công ty chính** — phải 0 dòng (rehearsal 27/10: 0).
   Khác 0 ⇒ người đó vào HRM không có công ty đang làm (403) — dừng, báo nhân sự bổ sung trước khi mở app.
   ```sql
   SELECT e.id AS employee_id, e.email, ei.fullname, ei.company_id AS main_company_id
   FROM employees e
   JOIN employee_infos ei ON ei.id = e.employee_info_id
   LEFT JOIN company_employees ce ON ce.employee_id = e.id AND ce.company_id = ei.company_id
   WHERE e.status = 1 AND ei.company_id IS NOT NULL AND ce.id IS NULL;
   ```
2. **Dọn `employee_has_roles` mồ côi** (vai trò ở công ty nhân viên không còn làm việc — user chốt phương án A: xuất bản lưu rồi xoá;
   nhân viên quay lại công ty đó phải được cấp vai trò lại). Rehearsal 27/10: 12 dòng / 11 NV, **cả 11 id không còn trong `employees`** (rác của tài khoản đã xoá).
   ```sql
   -- (a) bản lưu — lưu kết quả thành CSV vào thư mục báo cáo golive (employee-has-roles-mo-coi.csv)
   SELECT ehr.*, r.name AS role_name, c.code AS company_code, e.id IS NOT NULL AS con_tai_khoan
   FROM employee_has_roles ehr
   LEFT JOIN company_employees ce ON ce.employee_id = ehr.employee_id AND ce.company_id = ehr.company_id
   LEFT JOIN roles r ON r.id = ehr.role_id
   LEFT JOIN companies c ON c.id = ehr.company_id
   LEFT JOIN employees e ON e.id = ehr.employee_id
   WHERE ce.id IS NULL;
   -- (b) xoá — số dòng xoá phải bằng số dòng (a)
   DELETE ehr FROM employee_has_roles ehr
   LEFT JOIN company_employees ce ON ce.employee_id = ehr.employee_id AND ce.company_id = ehr.company_id
   WHERE ce.id IS NULL;
   ```
   Sau (b): xoá cache quyền — `php artisan tinker --execute='\App\Support\Permissions\PermissionChecker::flush(); cache()->forget("spatie.permission.cache");'`
   (KHÔNG `cache:clear`, Redis dùng chung).
3. **Báo cáo: người mất quyền quản lý tài khoản** (có quyền ERP cũ "Quản lý tài khoản" — mã `admin.tai_khoan.manage` đã bỏ, 3 tên cũ
   nằm trong `dropped_legacy.php` nên chuyển đổi xoá lượt gán — mà sau chuyển đổi không có "Quản lý tài khoản nhân viên" tại cùng công ty).
   User chốt phương án A: chỉ báo cáo, **quản trị viên tự cấp lại** ở màn Vai trò nhân viên (`/admin/employee-roles`), không tự cấp.
   Rehearsal 27/10: **0 người** (2 tài khoản đang hoạt động có quyền cũ đều đã có quyền mới — NV 256 qua vai trò Super Admin).
   SQL cũ trong `gd2b…/bao-cao-code/task-8-report.md` ĐÃ LỖI THỜI (tra theo mã đã bỏ + không lọc tài khoản khoá ⇒ ra nhầm NV 258 đã khoá).
   ```sql
   SELECT old.employee_id, old.company_id, c.code AS company_code, ei.fullname, e.email, old.quyen_cu
   FROM (
       SELECT ehr.employee_id, rhp.company_id,
              GROUP_CONCAT(DISTINCT p.name ORDER BY p.name SEPARATOR ' | ') AS quyen_cu
       FROM bak_rbac_employee_has_roles ehr
       JOIN bak_rbac_role_has_permissions rhp ON rhp.role_id = ehr.role_id
       JOIN bak_rbac_permissions p ON p.id = rhp.permission_id AND p.guard_name = 'web'
            AND p.name IN ('Quản lý tài khoản', 'Quản lý tài khoản theo tổng công ty', 'Quản lý tài khoản theo công ty')
       WHERE ehr.company_id IS NULL OR ehr.company_id = rhp.company_id
       GROUP BY ehr.employee_id, rhp.company_id
   ) old
   JOIN employees e ON e.id = old.employee_id AND e.status = 1
   JOIN company_employees ce ON ce.employee_id = old.employee_id AND ce.company_id = old.company_id
   LEFT JOIN employee_infos ei ON ei.id = e.employee_info_id
   LEFT JOIN companies c ON c.id = old.company_id
   WHERE NOT EXISTS (
       SELECT 1 FROM employee_has_roles h
       JOIN roles r ON r.id = h.role_id AND r.company_id = h.company_id AND r.status = 1
       JOIN role_has_permissions rhp2 ON rhp2.role_id = r.id
       JOIN permissions p2 ON p2.id = rhp2.permission_id AND p2.code = 'human.tai_khoan_nhan_vien.manage' AND p2.deprecated_at IS NULL
       WHERE h.employee_id = old.employee_id AND h.company_id = old.company_id)
   ORDER BY old.company_id, old.employee_id;
   ```
4. Mỗi tenant (etek, toyota) chạy lại đủ 3 bước trên DB của tenant đó.

## C. Khôi phục

- **Lỗi trước commit** (mã 1 trước commit hoặc mã 2): dữ liệu nguyên vẹn ⇒ xoá bảng sót, deploy lại code cũ hrm-api (và ERP nếu đã qua B6), mở app.
- **Lỗi sau commit / sự cố sau go-live:** bảo trì 2 app ⇒ **khôi phục bản dump B2** ⇒ deploy lại code cũ **cả 2 repo** (code cũ cần `role_has_permissions.company_id` và guard `web`) ⇒ restart worker + apache. Dữ liệu nhập sau go-live sẽ mất — chốt hạn chót khôi phục trước.
- `bak_rbac_*` + `bak_rbac_role_refs` + `rbac:convert --print-rollback` chỉ là đường phụ để tra/khôi phục từng phần, không thay bản dump.

## D. Khác biệt hành vi cho QA

- ERP kiểm quyền theo công ty trong hồ sơ (`info->company_id`, công ty đang chọn khi có ≥ 2 công ty); HRM theo `current_company_role`.
- Quyền gán thẳng cho nhân viên (`employee_has_permissions`) không còn tác dụng ở cả 2 bên.
- Mỗi vai trò thuộc 1 công ty, tên có tiền tố mã công ty (màn hình hiện tên gốc).
- "Xem khách hàng" không còn phạm vi: ai có quyền thấy toàn bộ khách hàng.
- Super Admin / "Super admin (DNS DÙNG)" không còn đặc quyền, chỉ có quyền theo mã được gán.
- 3 quyền mới "Xem … của tất cả công ty" (danh mục kho, tồn kho đầu kỳ, huỷ hàng giữ kế toán).
- 2 phiếu kiểm kê (nhập kiểm kê, xử lý chênh lệch) trước nay không ai mở/sửa được do lỗi kiểm vai trò — nay người có quyền dùng được.
- "BGĐ duyệt bảng chia thưởng" trước nay không ai duyệt được — nay người có quyền duyệt được.
- **GĐ3b:** các chỗ trước kiểm theo TÊN Vai trò nay kiểm mã (design `gd3b-doi-vai-tro-sang-ma/design.md` 4.1, F1–F15). Đổi thấy được: Tổng giám đốc cũng thấy ô Phòng ban ở ô lọc (Q5 `>=`); Giám đốc qua các nhánh chỉ-Trưởng-phòng của chứng từ bán hàng (F7); danh sách chứng từ "theo phòng" người không đủ phạm vi nay chỉ thấy phiếu mình tạo (trước thấy hết — vá fail-open); duyệt vượt hạn mức HĐ dự án TKT và xoá liên hệ KH chỉ tính mã ở công ty đang làm (Q4); thông báo đề nghị thanh toán bảo hành gửi người giữ mã ở công ty của phiếu.
- **GĐ2c:** màn Quản trị › "Cấu hình phạm vi Tổng công ty" chỉ hiện với tài khoản trong `RBAC_GROUP_SCOPE_ADMINS` (lúc lên = NV 13). Công ty bị
  tắt: vai trò của công ty đó không chọn được "Tổng công ty"; quyền đang để Tổng công ty tính như Công ty (cả HRM lẫn ERP); bật lại có hiệu lực ngay.
