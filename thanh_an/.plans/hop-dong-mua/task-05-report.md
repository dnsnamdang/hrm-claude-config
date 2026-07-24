# Task 5 — Report: Controller + Routes + Seed quyền HĐ mua

**STATUS: DONE** — 2026-07-20

## File tạo/sửa

| Loại | Path |
|------|------|
| Tạo | `hrm-thanhan-api/Modules/Supply/Http/Controllers/Api/V1/PurchaseContractController.php` |
| Sửa | `hrm-thanhan-api/Modules/Supply/Routes/api.php` (import controller + nhóm `/purchase-contracts`) |
| Tạo | `hrm-thanhan-api/Modules/Supply/Database/Seeders/PurchaseContractPermissionSeeder.php` (idempotent) |
| Sửa | `hrm-thanhan-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm id 518/519/520 sau id 517, dòng 736) |

## Controller — actions đã viết

index, nextCode, store, show, update, approve, rejectApprove, destroy, companies, suppliers, goodsPool.
- `index` dùng `$this->service->getList($request)` (đúng tên method, KHÔNG phải `index`).
- Ghi/duyệt bọc `DB::transaction` + try/catch → `Log::error` + `responseJson(..., HTTP_BAD_REQUEST)`.
- `destroy` chặn bằng `is_can_delete` trước khi vào transaction.
- `goodsPool` reuse `SupplyReportService::purchaseDemand(['rows'])` + `SupplyProposalService::goodsPool(2)`, không viết lại query.

## Routes

Nhóm `/purchase-contracts` đặt trong group `/v1/supply` (auth:api), ngay trước nhóm `/reports`.
Static route (`/next-code`, `/companies`, `/suppliers`, `/goods-pool`, `POST /`) đặt TRƯỚC wildcard `/{purchaseContract}`.
`checkPermission` chỉ trên store/update/destroy (`Lập hợp đồng mua`) và approve/reject-approve (`Duyệt hợp đồng mua`). GET list/show/dropdown không gán checkPermission (list gate ở service qua `checkPermissionList`).

## Quyền đã seed

| id | name | group | type | guard |
|----|------|-------|------|-------|
| 518 | Xem hợp đồng mua | Cung ứng | 7 | api |
| 519 | Lập hợp đồng mua | Cung ứng | 7 | api |
| 520 | Duyệt hợp đồng mua | Cung ứng | 7 | api |

Cả 2 nơi: PermissionsTableSeeder.php gốc (fresh install) + PurchaseContractPermissionSeeder.php (idempotent, `firstOrCreate` theo name+guard).

## php -l

```
Modules/Supply/Http/Controllers/Api/V1/PurchaseContractController.php  → No syntax errors detected
Modules/Supply/Routes/api.php                                         → No syntax errors detected
Modules/Supply/Database/Seeders/PurchaseContractPermissionSeeder.php  → No syntax errors detected
Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php         → No syntax errors detected
```

## Concern

- **Namespace class Permission khác giả định trong brief.** Brief đề xuất `Spatie\Permission\Models\Permission`, nhưng project thực tế dùng **`App\Models\Permission`** (extends `App\Models\BaseModel`) — đây là model đang được dùng trong `PermissionsTableSeeder.php` gốc (`use App\Models\Permission;`). Để nhất quán với project, seeder idempotent dùng `App\Models\Permission`. Việc xóa cache vẫn gọi `app()[\Spatie\Permission\PermissionRegistrar::class]->forgetCachedPermissions()` (độc lập với model class).
- Không chạy migrate/seed/route:list theo yêu cầu (chỉ kiểm cú pháp tĩnh).
