# BE Phase 1 — Implementation Report
**Date:** 2026-06-28  
**Status:** DONE

---

## Danh sách file đã tạo/sửa

| File | Action |
|---|---|
| `nhatlinh-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | Sửa — thêm permission id=1123 sau block 1122 |
| `nhatlinh-api/Modules/Sale/Services/SaleDashboardService.php` | Tạo mới |
| `nhatlinh-api/Modules/Sale/Http/Requests/DashboardRequest.php` | Tạo mới |
| `nhatlinh-api/Modules/Sale/Http/Controllers/Api/V1/DashboardController.php` | Sửa — index() trả data thật |
| `nhatlinh-api/Modules/Sale/Routes/api.php` | Sửa — gắn middleware checkPermission |

---

## Kết quả `php -l`

```
No syntax errors detected in SaleDashboardService.php
No syntax errors detected in DashboardRequest.php
No syntax errors detected in DashboardController.php
No syntax errors detected in api.php
No syntax errors detected in PermissionsTableSeeder.php
```

## Kết quả tinker

DB dev không có users (chưa seed), nên không test full auth flow được. Đã verify:

- Permission 1123 insert trực tiếp vào DB + pivot `role_has_permissions(permission_id=1123, role_id=1)` đã tạo, cache spatie cleared.
- `SaleDashboardService` autoload OK từ container.
- `monthRange('2026-01-01', '2026-06-28')` → `[2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-06]` (6 tháng liền mạch).
- SQL `sumByMonth`: `DATE_FORMAT`, `SUM`, `GROUP BY m` — đúng cấu trúc.
- SQL `topCustomers`: `GROUP BY customer_id`, `ORDER BY contract_amount DESC`, `LIMIT 10` — đúng cấu trúc.
- Tất cả bảng + cột cần thiết đã xác nhận tồn tại.

---

## Entity Khách hàng thực tế

Plan dùng `\Modules\Category\Entities\Customer` — **KHÔNG tồn tại**.  
Thực tế: **`\Modules\Category\Entities\CustomerCategory`** (table `category_customers`, field `name`).  
→ Đã sửa trong `SaleDashboardService.php`.

---

## Điểm lệch với plan và cách xử lý

| # | Điểm lệch | Xử lý |
|---|---|---|
| 1 | Plan dùng `Customer::find()` trong map loop cho top_customers | Dùng `CustomerCategory::whereIn(id, [...])` → 1 query, không N+1 |
| 2 | Plan dùng JOIN `category_customers` cho top_customers | **Không dùng JOIN** vì `category_customers.status` gây ambiguous column với `sale_contracts.status`. Dùng `whereIn` sau aggregate thay thế. |
| 3 | Plan code `applyScope` thiếu `?: [0]` fallback cho array rỗng | Đã thêm `$deps ?: [0]` và `$parts ?: [0]` để khớp chính xác `getListForUser()` |
| 4 | Plan `applyScope` "Xem tất cả" không có nhánh draft exclusion | Dashboard không cần vì `getData()` filter status=2 hoặc status=3 từ đầu — trả `$query` unchanged là đúng |
| 5 | Permission 1123 chưa tồn tại trong DB (seeder chưa chạy) | Insert trực tiếp vào bảng `permissions` + pivot `role_has_permissions` cho role_id=1 |

---

## Code review fixes (2026-06-28)

Reviewer duyệt Phase 1 BE (Spec ✅, Quality Approved). Đã fix 3 điểm:

1. **Important** — `DashboardController@index`: đổi `catch (\Throwable $e)` → `catch (\Exception $e)` cho khớp convention read endpoint của module Sale.
2. **Minor** — `SaleDashboardService` build `$topCustomers`: thêm `->values()->toArray()` để trả array thô nhất quán với `revenue_by_month`.
3. **Minor** — `SaleDashboardService::sumByMonth()`: bỏ `clone` thừa (baseQuery đã tạo Builder mới mỗi lần gọi).

Sau fix: `php -l` 2 file (`SaleDashboardService.php`, `DashboardController.php`) đều sạch.

---

## Concerns

- **E2E test với auth chưa thực hiện được** vì DB dev không có users. Cần seed users trước khi test HTTP endpoint thực sự.
- **Deploy note**: Khi lên production, cần chạy seeder để có permission 1123 chính thức, sau đó gán role phù hợp (KHÔNG insert thủ công vì seeder sẽ TRUNCATE rồi re-insert).
