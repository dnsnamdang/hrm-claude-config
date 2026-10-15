---
name: permission-seeder
description: Use when thêm / sửa / đổi tên / bỏ quyền (permission) ở hrm-api hoặc ERP TanPhatDev trên nhánh gop_db — khai dòng `$this->perm([...])` trong PermissionsTableSeeder, dùng hằng RENAMED / REMOVED, chạy `permission:sync --dry-run`, resolve conflict seeder quyền khi merge nhánh cũ, hoặc khi seeder quyền báo lỗi khai báo / API 403 sau khi đổi tên quyền.
---

# Khai báo quyền bằng seeder đồng bộ (HRM + ERP, DB gộp)

Áp dụng từ 14/10/2026 (feature `.plans/gop-db/permission-seeder-sync/`). Thay cho kiểu cũ
"xoá hết quyền rồi `Permission::create(['id' => N, ...])` lại từ đầu".

| | Seeder | Guard |
|---|---|---|
| HRM | `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | `api` |
| ERP | `TanPhatDev/database/seeds/PermissionsTableSeeder.php` | `web` |

Engine dùng chung: `app/Support/Permissions/PermissionSync.php` + `DeclaresPermissions.php` — **bản giống hệt ở 2 repo**,
sửa 1 bên phải chép sang bên kia.

## 1. Cơ chế (đọc 1 lần cho hiểu)

- Mỗi quyền là 1 dòng `$this->perm([...])` trong hàm `declarePermissions()`. Hàm này **không ghi DB**, chỉ gom vào danh sách.
- Khi seeder chạy, `PermissionSync` so danh sách với DB **theo TÊN** (chỉ guard của seeder đó):
  tên chưa có → thêm (id DB tự sinh) · tên đã có → cập nhật nhãn/nhóm/phân hệ tại chỗ, **giữ id** →
  gán quyền của vai trò không mất · tên có trong DB mà file không khai → **chỉ cảnh báo ⚠, không xoá**.
- Thứ tự dòng trong file = thứ tự hiển thị trên màn Phân quyền (cột `seed_order`).
- 2 seeder chỉ đụng guard của mình → HRM và ERP không ảnh hưởng nhau, kể cả trùng tên quyền.
- Khai sai → dừng, KHÔNG ghi gì. Lỗi SQL giữa chừng → rollback toàn bộ.

## 2. Thêm quyền

```php
$this->perm(['name' => 'Xem danh mục loại xe', 'display_name' => 'Xem danh mục loại xe', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
```
- **KHÔNG khai `'id'`, KHÔNG khai `'guard_name'`** (seeder báo lỗi). Đặt dòng cạnh các quyền cùng nhóm.
- `name` bắt buộc, ≤ 255 ký tự, không trùng dòng khác. `group` bắt buộc.
- HRM: `type` = `permissionType` của **phân hệ chính** (tra `hrm-client/components/subsystems.js`, bảng số ở đầu seeder).
  Thiếu `type` → quyền không hiện ở phân hệ nào. `sort_order` (tuỳ chọn) = xếp trước trong nhóm.
- ERP: dùng `group_category` (Danh mục, Kinh doanh, Kho, Kế toán, Mua hàng, CSKH…) thay cho `type`.
- Cột không khai = NULL (seeder là nguồn duy nhất).
- **Không dùng lại tên đã có trong `RENAMED` (vế trái) hoặc `REMOVED`** — seeder sẽ chặn (mục 5).
- Màn port từ ERP: tạo quyền MỚI ở seeder HRM, không dùng lại quyền ERP (skill `erp-to-hrm-screen` Bước 2).

## 3. Đổi tên quyền — sửa 3 chỗ

1. Sửa `name` ở dòng `$this->perm`.
2. Thêm vào hằng `RENAMED` ở đầu seeder, kèm ngày + lý do:
   ```php
   const RENAMED = [
       // 15/10/2026 — chuẩn hoá theo menu (#1234)
       'Xem nhóm ngành' => 'Xem danh mục nhóm ngành',
   ];
   ```
3. **Sửa mọi chỗ code dùng tên cũ**: `checkPermission:...` trên route, `isCurrentEmployeeHasPermission(...)`,
   `isShow` menu FE (`hrm-client/components/subsystem-menu/*.js`), `hasAPermission(...)`. Quên → người có quyền bị 403.

- Quên bước 2 → tạo quyền mới chưa ai được gán, quyền cũ nằm lại + cảnh báo. Bổ sung `RENAMED` sau vẫn cứu được (chế độ merge).
- Đổi tiếp lần nữa: **THÊM** mục `'B' => 'C'`, **giữ nguyên** `'A' => 'B'` — môi trường còn ở A tự đi thẳng tới C.

## 4. Bỏ quyền — sửa 2 chỗ

1. `grep` chắc chắn không còn code nào dùng tên quyền.
2. Comment (hoặc xoá) dòng `$this->perm` **VÀ** thêm tên vào `REMOVED` (kèm ngày + lý do).
- Gỡ = xoá quyền + mọi gán quyền của nó. Chỉ comment mà không thêm `REMOVED` → quyền còn nguyên (cố ý, tránh comment nhầm).
- Dry-run in `Gỡ: <tên> — mất ở N vai trò, M nhân viên` → N > 0 thì báo admin.

## 5. ⚠️ KHÔNG BAO GIỜ xoá mục cũ trong RENAMED / REMOVED

- Môi trường khác (dev, prod, Đức Lộc Sơn…) deploy lúc khác — xoá mục là môi trường chưa chạy sẽ không được đổi tên / gỡ.
- Mục cũ chặn việc **dùng lại tên** đã khai tử. Đã tái hiện 15/10/2026: xoá `'A' => 'B'` rồi khai lại "A" cho chức năng
  khác → môi trường chưa chạy bản đổi tên **trao quyền A mới cho vai trò đang giữ A cũ** + vai trò mất B.
- Để mục cũ vô hại: tên cũ không còn trong DB thì seeder bỏ qua.

## 6. Lệnh

| Lệnh | Dùng khi |
|---|---|
| `php artisan permission:sync --dry-run` | Xem trước thêm / sửa / đổi tên / gỡ, không ghi DB — **luôn chạy trước** |
| `php artisan permission:sync` | Ghi vào DB local (= `db:seed` seeder quyền) |
| `php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"` | Đường deploy `~/build_tpe.sh` (HRM tự chạy sau `migrate`) |
| `php artisan permission:cleanup --dry-run` (chỉ hrm-api) | Dọn gán quyền mồ côi, có CSV backup — chạy tay, prod phải hỏi trước |

Báo cáo: `Guard api: thêm X (giữ id cũ Y) · sửa · đổi tên · gỡ · gộp trùng · nhận gán quyền id cũ · không khai báo`.
Đổi vị trí dòng không hiện trong "sửa" (chỉ cập nhật `seed_order`).

## 7. Lỗi khai báo (seeder dừng, DB không đổi)

| Câu lỗi | Sửa |
|---|---|
| `trùng tên với dòng #M` | Xoá 1 dòng |
| `không được khai 'id' / 'guard_name' / 'seed_order'` | Bỏ key đó |
| `bảng permissions không có cột '<x>'` | Gõ sai tên cột |
| `thiếu 'name'` / `thiếu 'group'` | Bổ sung |
| `RENAMED: tên cũ 'X' vẫn còn trong khai báo.` | Quên sửa `name`, hoặc đang dùng lại tên đã khai tử → đặt tên khác |
| `RENAMED: tên mới 'Y' (đích cuối của 'X') không có trong khai báo.` | Gõ sai tên mới / quên sửa `name` |
| `RENAMED: ... vòng tròn` / `đổi sang chính nó` | Sửa lại mục RENAMED |
| `REMOVED: 'X' vẫn còn trong khai báo.` | Comment dòng khai báo |
| `REMOVED: 'X' đồng thời nằm trong RENAMED.` | Chọn 1 trong 2 |
| SQL `Duplicate entry ... permissions_name_guard_name_unique` | Tên chỉ khác dấu / hoa-thường với tên đã có (DB so không phân biệt dấu) → đặt tên khác hẳn |

## 8. Merge nhánh tạo trước 14/10/2026

Dòng `Permission::create(['id' => N, 'guard_name' => 'api', ...])` (HRM) hoặc `$this->createPermission(['id' => N, ...])` (ERP)
→ đổi thành `$this->perm([...])`, bỏ `'id'` và `'guard_name'`. Nhánh cũ comment quyền → thêm `REMOVED`; đổi tên → thêm `RENAMED`.
`run()` giữ bản mới (chỉ `$this->syncPermissions();`), KHÔNG đưa lại đoạn `delete()` / `truncate()`.
Resolve xong chạy `php -l` + `permission:sync --dry-run`.

## 9. Không làm

- Không viết migration / SQL tay để thêm, sửa, xoá quyền; không tạo seeder quyền riêng cho từng màn.
- Không sửa `permission_legacy_ids.php` (chỉ cho lần sync chuyển đổi đầu, xoá khi mọi môi trường đã sync).
- Không tự gán quyền mới cho vai trò cũ trên dev/prod — admin tự phân.
- Không sửa `PermissionSync.php` ở 1 repo mà quên chép sang repo kia.
