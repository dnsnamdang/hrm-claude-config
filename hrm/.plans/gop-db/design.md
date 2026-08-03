# Nền tảng `gop_db` — Gộp DB ERP + HRM

> **Đây KHÔNG phải một feature.** Đây là tài liệu nền tảng mô tả môi trường mà **mọi feature làm trên nhánh `gop_db` đều chạy trên đó**.
> Đọc file này TRƯỚC khi làm bất kỳ việc gì trên nhánh `gop_db`.
> Cập nhật lần cuối: 2026-08-01

---

## 0. ⚠️ MỤC TIÊU BẮT BUỘC: BỎ HẲN `DB_CONNECTION_SECOND`

**Mọi tính năng làm trên nhánh `gop_db` phải viết sao cho KHÔNG dùng `mysql2` / `DB_DATABASE_SECOND`.**
Connection thứ hai sẽ bị xoá; code còn phụ thuộc nó sẽ chết.

Có **HAI** dạng phụ thuộc, phải xử lý cả hai — dạng thứ hai rất dễ bỏ sót:

1. **Connection**: `DB::connection('mysql2')`, `protected $connection = 'mysql2'`
2. **Tiền tố tên bảng** (ÂM THẦM — model không khai `$connection` vẫn chết):
   ```php
   public function __construct(array $attributes = []) {
       $this->table = env('DB_DATABASE_SECOND') . '.' . $this->table;   // ← phải bỏ
   }
   ```
   và trong query builder: `->table($erpDb . '.customers')`, `->leftJoin($erpDb . '.provinces as p', …)`

**Cách kiểm chứng dứt điểm** (đã dùng, rất hiệu quả): đổi `DB_DATABASE_SECOND` trong `.env` thành tên DB
không tồn tại → `php artisan config:clear` → khởi động lại API → chạy luồng cần kiểm tra. Chỗ nào còn phụ
thuộc sẽ báo `SQLSTATE[HY000] [1049] Unknown database`. Nhớ backup và khôi phục `.env` sau khi test.

Điều kiện đủ để bỏ: **mọi bảng mà code đang trỏ tới đều đã có trên DB gộp** — đã verify 66/66 bảng của
79 model có tiền tố đều có sẵn. Nên đây là việc cơ học, không vướng dữ liệu.

## 0b. CẬP NHẬT 2026-08-03 — đã gộp chung bảng `employees` + `employee_infos`

Commit `gộp bảng employees: HRM đọc lại bảng employees chung (revert hrm_employees)`.
`App\Models\TpEmployee::$table` giờ là **`employees`**.

→ **`auth()->user()->id` chính là id nhân viên duy nhất.** KHÔNG còn khái niệm "ERP employee id"
tách riêng, KHÔNG phải map qua `employee_infos` nữa.

- `hrm_employees` vẫn còn trong DB nhưng là **bản cũ bỏ đi** — lệch 290 id và 164 `employee_info_id`
  so với `employees`. **Đừng đọc bảng đó.**
- Đã gỡ khỏi `Modules/Finance` + `Modules/CustomerCare`: `FinanceService` 3 hàm map → 1 hàm
  `currentEmployeeId()`; xóa model `Modules\Finance\Entities\ErpEmployee`, dùng
  `Modules\Human\Entities\Employee`.
- ⚠️ **CÒN NỢ**: `app/Helpers/ErpPermissionHelper.php` vẫn đọc qua `mysql2` và còn được gọi ở
  `Modules/Assign` (CustomerService, MeetingController, ProductProjectController,
  CustomerManagerService) + `app/Helper/CustomerOwnership.php` → thuộc đúng mục tiêu 0 ở trên,
  cần rà dứt điểm.

⚠️ Mục 1 dưới đây ghi DB gộp tên `local_hrm_erp`, nhưng `hrm-api/.env` hiện đang trỏ **`gop_db`** —
cần thống nhất lại tên.

## 1. Mục tiêu

Gộp 2 hệ thống đang chạy độc lập về một nền tảng duy nhất:

| | ERP | HRM |
| --- | --- | --- |
| Stack | Laravel + Blade + AngularJS | Laravel 8 + Nuxt 2 (SPA) |
| Auth | session / SSO | JWT |
| DB gốc | `dev_erp` (1216 bảng) | `hrm_prod_local` (640 bảng) |

Hai việc song song:

1. **Gộp database** → 1 DB duy nhất `local_hrm_erp` (1821 bảng).
2. **Dựng 18 phân hệ mới** trong HRM để dần tiếp nhận 304 chức năng đang nằm bên ERP.

Nguồn theo dõi tiến độ: Google Sheet `erp-menu-inventory.xlsx`
(id `1JFSPBbdyi3VfB4E_eymdW-3UOMls6qqp`) — 2 sheet:
- **"Chi tiết chức năng"**: 304 chức năng ERP (Menu / Nhóm / Chức năng / Route / Ghi chú / Người làm / Người test / Trạng thái).
- **"hiện trạng table"**: 58 bảng trùng tên + cách xử lý từng bảng.