# Hướng dẫn build môi trường TEST — Cách A (lớp VIEW)

Mục tiêu: cả 2 app **ERP + HRM cùng chạy trên 1 DB đã merge**, KHÔNG sửa code HRM.
Đã smoke-test đầy đủ ở local (đọc/ghi/auto-increment/JOIN chuỗi view đều OK).

## Kiến trúc

```
        app ERP  ──DB_DATABASE=erp_hrm_check──▶  erp_hrm_check   (bảng ERP tên gốc + hrm_* tách + bảng HRM move về)
                                                      ▲
        app HRM  ──DB_DATABASE=hrm_view──▶ hrm_view  │  (639 VIEW 1-1)
                                             employees   ──▶ erp_hrm_check.hrm_employees
                                             roles       ──▶ erp_hrm_check.hrm_roles
                                             files       ──▶ erp_hrm_check.hrm_files
                                             customers   ──▶ erp_hrm_check.customers  (passthrough)
                                             quotations  ──▶ erp_hrm_check.quotations (KEEP_HRM, passthrough)
                                             ... (639)
```

- 23 bảng TÁCH → view trỏ `hrm_*`. Còn lại → view trỏ thẳng bảng cùng tên.
- View `SELECT *` 1-1 nên **updatable + insertable**; `LAST_INSERT_ID()` qua view trả đúng id bảng đích.

## Các bước deploy trên server TEST

1. **Đưa 2 DB về CÙNG 1 MySQL server test** (bản copy của prod): `erp_new` + `hrm_pro`.
2. **Chạy merge** (đổi tên schema đích nếu muốn giữ nguyên erp_new, hoặc dựng bản copy `erp_hrm_check`):
   - Xem `HUONG-DAN-GOP.md` + `merge_prod.php` (DRY-RUN trước, backup trước).
   - Sau merge: schema đích chứa bảng ERP tên gốc + `hrm_*` (23 tách) + bảng HRM move về.
3. **Dựng lớp view cho HRM:**
   ```
   ./build_hrm_views.sh <merged_schema> hrm_view hrm-view-tables.txt -- -h<host> -P<port> -u<user> -p<pass>
   ```
   (VD local: `./build_hrm_views.sh erp_hrm_check hrm_view hrm-view-tables.txt -- -h127.0.0.1 -P3306 -uroot`)
   → tạo 639 view. Chạy lại nhiều lần an toàn (CREATE OR REPLACE).
4. **Cấp quyền cho user MySQL của HRM** trên `hrm_view.*` (SELECT, INSERT, UPDATE, DELETE).
   View tạo `SQL SECURITY DEFINER` (definer = user chạy script) nên user HRM chỉ cần quyền trên view,
   definer lo quyền bảng đích. Nếu muốn dùng INVOKER: user HRM phải có quyền cả trên `<merged>.*`.
5. **Sửa `.env`:**
   - **ERP app**: `DB_DATABASE=<merged_schema>` (giữ nguyên các key khác).
   - **HRM app**: `DB_DATABASE=hrm_view`.
     - Kết nối `mysql2` của HRM (đọc thẳng bảng ERP): trỏ `DB_DATABASE=<merged_schema>` (bảng ERP nay nằm ở đây, tên gốc).
     - `QUEUE_CONNECTION=database` giữ nguyên (bảng `jobs`/`failed_jobs` qua view → dùng chung, phân biệt cột `queue`).
6. **Chạy worker tách theo queue name (BẮT BUỘC):**
   ```
   ERP: php artisan queue:work database --queue=erp
   HRM: php artisan queue:work database --queue=hrm,rice_notifications,sync_faces
   ```
7. **Smoke test:** đăng nhập ERP + 1 nghiệp vụ; đăng nhập HRM + 1 API mỗi module (Human/Timesheet/Payroll/Assign/Training).

## Giới hạn / lưu ý đã biết (bản test chấp nhận được)

- **`truncate` / DDL trên view sẽ lỗi.** Seeder HRM nào gọi `DB::table('employees')->truncate()`... sẽ fail nếu chạy trên `hrm_view`. Bản check KHÔNG chạy seeder nên không sao. Nếu cần seed → trỏ tạm về merged schema.
- **`php artisan migrate` KHÔNG chạy trên hrm_view** (migrate cần bảng thật, không phải view). Bản check không migrate. Khi cần: chạy trên merged schema + cấu hình `database.migrations`.
- **Bảng LOG dùng cấu trúc ERP** (jobs/failed_jobs/notifications/password_resets giữ structure ERP, data HRM đã bỏ). `jobs`/`failed_jobs`/`password_resets` là bảng Laravel chuẩn → giống nhau, OK. **`notifications`**: nếu cột HRM khác ERP thì ghi notification của HRM có thể lỗi → rà nếu test tính năng thông báo.
- **View `SELECT *` "đóng băng" danh sách cột lúc tạo.** Nếu sau này ALTER thêm cột vào bảng đích → chạy lại `build_hrm_views.sh` để view thấy cột mới.
- **Đây là lớp tạm cho giai đoạn CHECK.** Khi hợp nhất thật (port ERP→HRM, gỡ hrm_*), xoá schema `hrm_view` là sạch.

## Rollback lớp view
```
DROP DATABASE hrm_view;   -- không đụng dữ liệu (view không chứa data)
```

## File liên quan
- `build_hrm_views.sh` — script dựng view (portable).
- `hrm-view-tables.txt` — snapshot 639 tên bảng HRM (nguồn sinh view; cần vì sau merge hrm_pro rỗng).
- `merge_prod.php` + `HUONG-DAN-GOP.md` — bước merge DB.
