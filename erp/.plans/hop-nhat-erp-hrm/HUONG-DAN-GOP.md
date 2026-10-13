# Hướng dẫn chạy GỘP DB ERP + HRM (bản production)

Script: **`merge_prod.php`** (idempotent, có DRY-RUN). Đã kiểm trên staging local `erp_new`↔`hrm_pro` (776 câu lệnh, 0 lỗi).

## 0. Nguyên tắc
- **Base = ERP**: gộp toàn bộ bảng HRM VÀO schema ERP. ERP giữ nguyên tên+cột → **app ERP chỉ đổi `DB_DATABASE` là chạy**.
- Bảng HRM riêng → move nguyên tên. Bảng trùng **tách** → `hrm_<tên>`. Bảng trùng **hòa** → nhập vào bảng ERP (thêm cột + union rows).

## 1. ĐIỀU KIỆN BẮT BUỘC
1. **Hai DB phải CÙNG 1 MySQL server** (RENAME TABLE không chạy chéo server). → đưa `erp_new` + `hrm_pro` về cùng server trước.
2. **BACKUP cả 2 DB** (mysqldump) — thao tác move/drop KHÔNG tự rollback được.
3. Tài khoản MySQL có quyền `ALTER, DROP, CREATE, INSERT, RENAME` trên cả 2 schema.

## 2. Các bước
```
1) Sửa cấu hình đầu file merge_prod.php:
   $SRC_ERP = 'erp_new';   // schema ERP đích
   $SRC_HRM = 'hrm_pro';   // schema HRM nguồn
   $DRY_RUN = true;        // chạy thử trước
   $FILL_SHARED_HRM = true;// điền cột CRM/HRM cho khách đã có ở ERP (khuyến nghị true)

2) DRY-RUN (in hành động, không thực thi):
   cd hrm-api (hoặc TanPhatDev) — miễn Laravel nối được cả 2 DB
   php artisan tinker --execute="require '<đường-dẫn>/merge_prod.php';"
   → Kiểm số: move + tách + hòa. Xem 12 câu lệnh mẫu.

3) GỘP THẬT: đổi $DRY_RUN=false → chạy lại lệnh trên.
   (Idempotent: nếu lỗi giữa chừng, chạy lại — tự bỏ qua bảng đã xử lý.)

4) Kiểm sau gộp: script tự in tổng bảng schema ERP + số bảng HRM còn sót.
```

## 3. SAU KHI GỘP
- **App ERP**: đổi `DB_DATABASE` → `erp_new`. Chạy nguyên (mọi bảng ERP giữ nguyên).
- **App HRM**: đổi `DB_DATABASE` → `erp_new`, và **sửa code**:
  - Các model trỏ bảng **đã đổi tên** `hrm_*` (35 bảng: `quotations→hrm_quotations`, `roles→hrm_roles`, `jobs→hrm_jobs`, `notifications→hrm_notifications`, `migrations→hrm_migrations`…). Cấu hình queue/notification/migration table name của HRM trỏ `hrm_*`.
  - Các bảng **hòa** (23): giờ là bảng ERP (nhiều cột hơn) — HRM đọc/ghi bình thường, cột HRM-only vẫn còn (đã ALTER thêm).

## 4. LƯU Ý / RỦI RO
- **FK**: script tắt `FOREIGN_KEY_CHECKS` khi gộp. Sau gộp, rà FK của bảng HRM đã move (FK trỏ bảng cùng tên/đã đổi tên). `CREATE TABLE LIKE` không copy FK; `RENAME` giữ FK gốc → có thể trỏ sai nếu bảng đích đổi tên. **Kiểm `information_schema.KEY_COLUMN_USAGE` sau gộp.**
- **Nhóm hòa dùng-chung id** (companies/customers/departments/employee_infos): row có id trùng ERP giữ giá trị ERP; cột HRM-only được điền từ HRM nếu `$FILL_SHARED_HRM=true`. Row HRM có id trùng nhưng KHÁC thực thể (hiếm, vd employees ~21% lệch) → **cần rà & remap thủ công trước** (xem `verify-58-prod.tsv`).
- **migrations** bị tách `hrm_migrations` → HRM phải trỏ migration table = `hrm_migrations` (config `database.migrations`), nếu không `php artisan migrate` sẽ chạy nhầm.
- **auth** (`roles/permissions/...` → `hrm_*`): spatie/permission của HRM phải cấu hình table names mới, hoặc HRM và ERP dùng 2 hệ auth tách biệt.

## 5. ROLLBACK
Không có rollback tự động (move/drop). → **phục hồi từ backup** ở bước 1.2. Vì vậy nên chạy trên **staging (bản copy local) trước**, rồi mới prod.

## 6. Phân loại chi tiết
Xem `xu-ly-bang-trung-PROD.xlsx` (58 bảng: hòa/tách/gộp/framework) + `verify-58-prod.tsv` (số liệu id khớp).
