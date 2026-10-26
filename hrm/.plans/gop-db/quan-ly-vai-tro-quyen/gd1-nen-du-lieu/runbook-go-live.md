# Runbook go-live — Vai trò & Quyền giai đoạn 1

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

## A. Trước cửa sổ bảo trì (vài ngày trước)

1. **Đóng băng quyền:** không thêm/đổi tên quyền, không merge nhánh thêm quyền vào `gop_db`. Nhánh `rbac` chưa vào `gop_db`.
2. **Diễn tập trên bản sao prod mới nhất (cùng ngày nếu được)** — DB `hrm_erp_rbac_rehearsal`:
   1. `php artisan migrate:status` ⇒ chạy **mọi** migration `gop_db` còn chờ trước (vd `2026_10_22_*`, `2026_10_23_*`: bản `2026_10_22_000003` ghi `role_has_permissions.company_id` nên phải chạy TRƯỚC chuyển đổi).
   2. Chạy lẻ 5 migration bằng `--path` (xem `--pretend` trước): `2026_11_01_000001` … `000005`.
   3. `php artisan rbac:convert --dry-run --report-dir=… --scope-decisions=<scope-decisions.csv>` — cổng: mã thoát 0, `chenh-lech-khac.csv` chỉ có tiêu đề.
   4. Phát lại cho quản trị viên các danh sách từ **lần chạy này** (không dùng số 25/10): `mat-do-bit-ro`, `mat-do-cong-ty-qua-vai-tro` (cột "dùng được trên giao diện"), `thieu-quyen-xem`, `du-lieu-tro-role-id`, `vai-tro-khong-chuyen`.
   5. Chạy thật trên DB diễn tập ⇒ `permission:catalog-sync --dry-run` phải 0 thay đổi ⇒ trỏ 2 app vào DB diễn tập, chạy 2 bộ test Rbac ⇒ Playwright 3 tài khoản (1 công ty, 2 công ty, Super Admin), đếm menu/nút khớp CSV. Ghi thời gian chạy chuyển đổi và thời gian `mysqldump`.
3. **Quản trị viên cấp lại quyền trong hệ thống CŨ** theo danh sách bước 2.4 (sau go-live không có màn sửa quyền tới giai đoạn 2). Báo trước người dùng Super Admin: đã bỏ mọi đặc quyền (quyết định 25–26/10) — gồm cả ô chọn mọi phòng ban, thủ kho/kế toán mọi kho, mọi hãng ở bộ lọc NCC PI, bỏ qua người mua/người duyệt/phân vùng, mở nháp người khác, bỏ qua hạn xử lý.
4. **Sửa script e2e + seeder** đang dựa vào vai trò 18 / tên "Super Admin" / `role_has_permissions.company_id` (chờ user cho phép).

## B. Trong cửa sổ bảo trì

1. **Hạ 2 app:** hrm-api `php artisan down --secret=<token>`; ERP `php artisan down --allow=<IP quản trị>`. Tắt cron (`schedule:run` của `erp_tpe` và cron ERP).
2. **Sao lưu:** `mysqldump` đầy đủ `hrm_erp_gop` trên 192.168.122.103. **Đây là điểm khôi phục chính.**
3. **Deploy hrm-api** (capistrano: composer, `migrate`, restart worker). Cổng: `migrate:status` không còn bản chờ, 5 migration `2026_11_01_*` đã chạy, `permission_aliases` = 0 dòng.
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
5. **Kiểm bằng SQL:** `role_has_permissions` không còn `company_id`; `roles.company_id` NOT NULL + unique `(company_id, base_name)`; `rbac_role_map` có dòng; số dòng khớp diễn tập. Rồi `permission:catalog-sync --dry-run` = 0 thay đổi.
6. **Deploy ERP:** merge/push `rbac` vào `gop_db` TanPhatDev lúc này (workflow: `git pull`, `composer install --optimize-autoloader`, `migrate`, `config:cache`, `route:cache`, `view:cache`, `queue:restart`, `optimize`). Rồi `sudo systemctl reload apache2`.
7. **Cache:** HRM — chuyển đổi đã xoá cache spatie. ERP — cache spatie 0 giây. **Không** `cache:clear` trên Redis dùng chung.
8. **Khởi động lại worker sau chuyển đổi:** HRM `sudo supervisorctl restart laravel-worker:*`; ERP `php artisan queue:restart`.
9. **Smoke test** qua đường bypass bảo trì: 3 tài khoản Playwright trên 2 app + đăng nhập TPE_APP (`permissions[].name` phải là tên cũ). So số với diễn tập.
10. **Mở 2 app** (`php artisan up`), bật lại cron.

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
