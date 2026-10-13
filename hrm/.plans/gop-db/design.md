# Nền tảng `gop_db` — Gộp DB ERP + HRM

> **Đây KHÔNG phải một feature.** Đây là tài liệu nền tảng mô tả môi trường mà **mọi feature làm trên nhánh `gop_db` đều chạy trên đó**.
> Đọc file này TRƯỚC khi làm bất kỳ việc gì trên nhánh `gop_db`.
> Cập nhật lần cuối: 2026-10-06 (thêm mục 2 "Bẫy khi port")

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

## 2. Bẫy khi port — bảng ERP dùng chung (bổ sung 2026-10-06)

> CLAUDE.md trỏ tới mục này ("đọc trước khi làm feature gop_db"). Trước đây CLAUDE.md ghi "7 gotcha"
> nhưng file chưa từng có danh sách đó — nay viết ra từ các lỗi đã sửa thật (commit hrm-api 09–10/2026).
> UI / quy trình port màn: skill `erp-to-hrm-screen`. Mục này chỉ nói về **dữ liệu & bảng ERP**.

ERP vẫn đang ghi vào cùng các bảng này, và màn khác (cả bên ERP) đọc chúng. Nguyên tắc: **HRM ghi
đúng như ERP ghi, và không phá cột ERP đang dựa vào.**

| # | Bẫy | Hậu quả | Cách làm đúng | Bằng chứng |
|---|---|---|---|---|
| 1 | Model con không khai `$table` / bảng trùng tên | Đọc nhầm bảng (`hrm_*` là bản HRM đã đổi tên; ưu tiên bản ERP) | Khai `$table` tường minh; xem sheet "hiện trạng table" | CLAUDE.md mục gộp DB |
| 2 | **Cột polymorphic lưu TÊN CLASS ERP** (`deptable_type`, `contractable_type`, `invoiceable_type`…) | `morphTo` của HRM không resolve được (class không có trong `morphMap`); báo cáo ERP lại so đúng chuỗi class | Ghi **nguyên chuỗi class ERP**; đọc qua bảng tra class → bảng bằng query thô | `DeclareDebtContractRegistry.php` (131531f2f) |
| 3 | **Cột / bảng "nói dối"** | Join ra rỗng hoặc sai | Kiểm bằng dữ liệu thật trước khi join/tin cột lưu sẵn. Đã gặp: `supplier_id` trỏ `customers.id` (model `Supplier` ERP khai `$table = 'customers'`, bảng `suppliers` rỗng); `supplier_name` toàn NULL; `cost_id` varchar join `costs.id` số → ép kiểu; `wr_accounting_service_items.service_id` thật ra trỏ `costs` | `BuyServiceRequestDetail.php` (7bb7ef2ea) |
| 4 | **Cột do cổng ERP ghi** (`contracted_qty`, trạng thái 6/7 cộng dồn khi lập hợp đồng…) | Sync dòng kiểu "xoá rồi insert" làm mất giá trị; lịch sử đổ nhầm thay đổi cho người sửa phiếu | **HRM chỉ đọc**: không cho vào `$fillable`, giữ giá trị cũ khi sync dòng, loại khỏi whitelist `CatalogHistoryService` | 7bb7ef2ea |
| 5 | **HRM ghi thiếu cột phụ mà ERP vẫn ghi** (`base_unit_name`, tên lưu sẵn…) | Màn khác đọc cột đó ra trống (#11516: cột ĐVT trống với phiếu tạo từ HRM) | Màn ghi phải ghi đủ mọi cột ERP ghi (đọc hàm `store` của ERP); màn đọc `COALESCE` về nguồn gốc cho dữ liệu cũ | `BorrowStockReportService::baseUnitNameExpression()` (8db6d3dc7) |
| 6 | **Cột NOT NULL không default** ở bảng ERP | Insert lỗi khi hàng thiếu model / thương hiệu… | Ghi `''` / `0` như ERP | `AccountingPrepickCancelDetail.php` (15c2fcc22) |
| 7 | **Prod có khoá ngoại mà DB `gop_db` local không có** | Local xoá được, prod lỗi SQL 1451 | Chặn trước bằng `usedIds()` + lưới `catch QueryException` khi `errorInfo[1] === 1451` → câu "… đang được sử dụng, không thể xóa." | `ProvinceService.php` (6a48fd618) |
| 8 | **Path file ERP** (`/uploads/...`, logo, header công ty, đính kèm) | Trình duyệt tải từ host HRM → 404 | Giữ nguyên cột gốc, field hiển thị `*_url` ghép `ERP_URL` khi còn là path tương đối (thiếu `ERP_URL` thì trả nguyên path) — áp **mọi** màn, không riêng bản in | `CompanyService::erpAssetUrl()` (ec9eb9cdf), `print-page` §4b |
| 9 | **Dùng lại quyền ERP** (guard `web`; vai trò gán từ ERP có `model_type = App\Employee`; trùng tên với bản HRM) | `hasPermissionTo` ném `PermissionDoesNotExist`; `checkPermission` (qua `getAllPermissions()`) bỏ sót vai trò ERP → người có quyền vẫn 403 | Tạo quyền mới guard `api` trong `PermissionsTableSeeder` chung, `type` = phân hệ chính, admin gán lại (skill `erp-to-hrm-screen` Bước 2) | docblock `ChecksEmployeePermission.php`; user chốt 06/10/2026 |
| 10 | `where('company_id', $id)` với `$id = null` | Ra `IS NULL` → lôi phiếu rác | Null thì `whereRaw('1 = 0')`; so công ty null-safe | `BorrowExtendRequest::searchByFilter` (11e8b8734) |
| 11 | Seeder quyền **ERP** (`gop_db`) xoá mọi quyền guard `web` rồi tạo lại | Quyền còn trong DB nhưng đã bị comment trong seeder sẽ MẤT, `role_has_permissions` mồ côi | Trước khi chạy: đối chiếu id DB với các dòng `createPermission` **chưa comment** | đã dính 7 quyền 361, 362, 366-368, 395, 396 |
| 12 | Màn ERP KHÔNG có bản in mà HRM được yêu cầu bổ sung | Ghi mẫu mới vào `report_templates` (bảng dùng chung, ERP đọc) là trộn mẫu HRM vào dữ liệu ERP | Mẫu tự dựng là blade trong module (`Modules/Finance/Resources/views/prints/`), KHÔNG insert vào `report_templates`. Màn ERP **có** mẫu in thì dùng mẫu ERP — đối chiếu tên biến theo `print-page` §4c | `BorrowExtendRequestService::renderPrint()` (5f7f7c1c0) |