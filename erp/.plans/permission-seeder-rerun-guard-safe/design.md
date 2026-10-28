# PermissionsTableSeeder chạy lại an toàn — không mất quyền HRM

## Hiện trạng / Vấn đề
`database/seeds/PermissionsTableSeeder.php` (ERP) hiện:
- Dòng 16: `DB::table('permissions')->truncate();` → **xoá SẠCH bảng `permissions`**, gồm cả
  quyền HRM (guard `api`). Chạy lại seeder ERP là HRM mất hết quyền.
- 957 dòng `Permission::create(['id' => N, ...])` dùng **id thô 1..1049** và **không khai
  `guard_name`** (mặc định rơi về guard `web`).

Sau khi gộp DB (chung 1 MySQL `erp_new`):
- Quyền ERP = guard **`web`**, id đã dời **+100000** (DB thật: 959 dòng, id `100001..101049`).
- Quyền HRM = guard **`api`**, id `2..1198` (612 dòng).
- `role_has_permissions` / `employee_has_permissions` của ERP trỏ tới id **100001+**.

→ Seeder hiện tại vừa **xoá nhầm quyền HRM**, vừa **tạo lại sai id/guard** (id thô 1.., đụng dải
id api, và pivot ERP trỏ 100001+ sẽ mồ côi).

## HRM làm thế nào (mẫu để mirror)
`HRM/hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`:
```php
DB::statement('SET FOREIGN_KEY_CHECKS = 0');
// chỉ xoá guard=api (HRM), KHÔNG đụng guard=web (ERP)
DB::table('permissions')->where('guard_name', 'api')->delete();
DB::statement('SET FOREIGN_KEY_CHECKS = 1');
Permission::create(['id' => 2, 'guard_name' => 'api', 'name' => ..., ...]);
```
Mỗi `create` khai rõ `guard_name => 'api'`, chỉ xoá đúng guard của mình.

## Hướng sửa (mirror HRM, phía ERP)
1. **Xoá có phạm vi**: `truncate()` → `where('guard_name', 'web')->delete()` (giữ `FOREIGN_KEY_CHECKS=0`
   bao quanh vì pivot còn trỏ tới id đang xoá; tạo lại đúng id là FK hợp lệ lại → **giữ nguyên
   phân quyền vai trò/nhân viên**).
2. **Dời id +100000 + gán guard `web`** cho mọi create, bằng 1 helper dùng chung thay vì sửa tay
   957 dòng:
   ```php
   const ID_OFFSET = 100000;
   private function createPermission(array $attributes)
   {
       $attributes['id'] = $attributes['id'] + self::ID_OFFSET; // dải id ERP, không đụng guard api
       $attributes['guard_name'] = 'web';
       return Permission::create($attributes);
   }
   ```
   Rồi thay toàn bộ `Permission::create(` → `$this->createPermission(` (dòng comment vẫn là comment).

## Vì sao giữ `delete` + `create` (không `updateOrCreate` trần)
- `delete where guard=web` dọn luôn quyền web **cũ đã bỏ** khỏi seeder (không để rác).
- FK tắt → xoá rồi tạo lại **cùng id** → `role_has_permissions`/`employee_has_permissions` ERP
  vẫn khớp, không mất gán quyền.
- Không đụng 1 dòng guard=api nào → HRM an toàn, đúng yêu cầu.

## Không đụng
- Không sửa dòng `Cache::flush(...)`.
- Không tạo migration (CLAUDE.md: quyền sửa thẳng seeder).
- Không chạy seeder vào DB (chỉ sửa file + verify logic read-only). User tự quyết lúc chạy.
- Không commit/push khi chưa có yêu cầu.

## Ghi chú kỹ thuật
- Seeder: 957 create active, id phân biệt, KHÔNG trùng (8 id "trùng" chỉ là bản `//` comment).
- ERP = Laravel (PHP 7.4); helper viết thuần, không dùng `?->`.
- Đối chiếu DB: web id 100001..101049 = (1..1049)+100000 → offset khớp tuyệt đối.
