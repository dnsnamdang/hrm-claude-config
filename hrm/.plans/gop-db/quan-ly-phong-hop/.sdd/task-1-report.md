# Task 1 — Report: Tạo module `Modules/Meeting`

Trạng thái: **DONE_WITH_CONCERNS**

Repo: `HRM/hrm-api`, branch `gop_db` (đã kiểm `git branch --show-current` trước khi làm).

## Việc đã làm

### Bước 1 — Sinh module

```
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan config:clear   # chạy trước, đề phòng config:cache trỏ production
/opt/homebrew/opt/php@7.4/bin/php artisan module:make Meeting
```

`config:clear` chạy sạch (chỉ có warning `imagick.so` không load được — không liên quan, môi trường thiếu
extension, không ảnh hưởng lệnh). `module:make Meeting` tạo thành công, output liệt kê đủ các file khung
chuẩn của `nwidart/laravel-modules` (module.json, Routes/{web,api}.php, Resources/assets, Resources/views,
Config/config.php, composer.json, Database/Seeders/MeetingDatabaseSeeder.php, Providers/{MeetingServiceProvider,
RouteServiceProvider}.php, Http/Controllers/MeetingController.php, webpack.mix.js, package.json).

### Bước 2 — Dọn phần thừa

Đã xóa đúng 4 mục theo brief:
- `Modules/Meeting/Resources/assets/` (gồm `js/app.js`, `sass/app.scss`)
- `Modules/Meeting/Resources/views/` (gồm `index.blade.php`, `layouts/master.blade.php`)
- `Modules/Meeting/webpack.mix.js`
- `Modules/Meeting/package.json`

Giữ nguyên `Config`, `Database`, `Entities` (mới có `.gitkeep`, chưa có class — đúng ràng buộc "Model/entity
chưa tạo ở task này"), `Http`, `Providers`, `Routes`, `Tests`. `Services` và `Transformers` chưa được
`module:make` sinh sẵn (không phải thư mục mặc định của stub) nên hiện chưa tồn tại — sẽ do các task sau tạo
khi cần, không tạo rỗng thêm ở task này vì brief không yêu cầu tạo mới, chỉ yêu cầu "giữ" nếu có.

`Resources/lang/.gitkeep` không nằm trong danh sách phải xóa của brief nên được giữ nguyên (không có asset FE
thật, chỉ 1 file `.gitkeep`, không ảnh hưởng gì).

Cây file cuối cùng của `Modules/Meeting/`:
```
Config/.gitkeep
Config/config.php
Console/.gitkeep
Database/Migrations/.gitkeep
Database/Seeders/.gitkeep
Database/Seeders/MeetingDatabaseSeeder.php
Database/factories/.gitkeep
Entities/.gitkeep
Http/Controllers/.gitkeep
Http/Controllers/MeetingController.php
Http/Middleware/.gitkeep
Http/Requests/.gitkeep
Providers/.gitkeep
Providers/MeetingServiceProvider.php
Providers/RouteServiceProvider.php
Resources/lang/.gitkeep
Routes/.gitkeep
Routes/api.php
Routes/web.php
Tests/Feature/.gitkeep
Tests/Unit/.gitkeep
composer.json
module.json
```

### Bước 3 — Khai route prefix

Đối chiếu `Modules/Assign/Providers/RouteServiceProvider.php` — `RouteServiceProvider` do `module:make` sinh
cho `Meeting` đã tự có `mapApiRoutes()` với `Route::prefix('api')->middleware('api')->namespace(...)->group(...)`,
giống hệt khuôn của Assign (không cần sửa file này).

Đã thay nội dung `Modules/Meeting/Routes/api.php` (mặc định có 1 route demo `GET /meeting`) bằng khung rỗng
đúng như brief:

```php
<?php

use Illuminate\Support\Facades\Route;

Route::group(['prefix' => 'v1', 'middleware' => ['auth:api']], function () {
    // Danh mục tiện nghi phòng họp + danh mục phòng họp khai ở Task 5, Task 6
});
```

Kết hợp `prefix('api')` ở `RouteServiceProvider` + `prefix('v1')` trong group này → URL cuối
`/api/v1/meeting/...` đúng như kỳ vọng của các task sau.

### Bước 4 — Kiểm module đã nạp

`php artisan module:list` → **Meeting | Enabled** (nằm đúng thứ tự alphabet giữa MasterData và Operation,
danh sách 27 module tổng, tất cả đều Enabled).

`php artisan route:list --path=meeting` (và cả `--path=assign`, và cả không filter) → **crash**, xem mục
Concerns bên dưới.

### Bước 5 — Tự kiểm `git status`

```
 M modules_statuses.json
?? Modules/Meeting/
```

`modules_statuses.json` (ở gốc `hrm-api`, ngoài `Modules/Meeting/`) bị đổi 1 dòng — đây là side-effect
**bắt buộc, không tránh được** của chính `artisan module:make Meeting` ở Bước 1 (nwidart/laravel-modules lưu
trạng thái Enabled/Disabled của toàn bộ module trong 1 file JSON chung ở gốc repo, không có cách nào bật
module mà không đụng file này). Diff:

```diff
-    "Finance": true
-}
+    "Finance": true,
+    "Meeting": true
+}
```

(mất newline cuối file — do nwidart tool tự ghi lại, không phải tôi sửa tay). Không có file nào khác ngoài
2 mục này bị đổi.

## Concerns

1. **`route:list --path=meeting` crash, KHÔNG do module Meeting.** Lỗi:
   `ErrorException: Trying to get property 'employee_info_id' of non-object` tại
   `app/Helper/PermissionHelper.php:23`, ném ra từ constructor của
   `Modules/Timesheet/Http/Controllers/Api/V1/RequestUpdateTimeSheetController.php:51` (gọi
   `isCurrentEmployeeHasPermission(...)` trong lúc `auth()->user()` là `null` ở context CLI).
   Đã xác minh đây là bug **có sẵn trong repo, không liên quan gì tới Meeting**:
   - `php artisan route:list --path=assign` (module cũ, không đụng tới) → **crash y hệt**.
   - `php artisan route:list` (không filter) → **crash y hệt**.
   - `php artisan module:list` và `php artisan config:clear` (không boot toàn bộ route) → chạy sạch.

   Không sửa được vì ràng buộc "chỉ tạo/sửa file bên trong `Modules/Meeting/`" — lỗi nằm ở
   `Modules/Timesheet` + `app/Helper/PermissionHelper.php`, ngoài phạm vi task. Route của Meeting (rỗng)
   không phải nguyên nhân và không có cách nào xác nhận trực tiếp bằng `route:list` do lỗi môi trường này
   chặn mọi lệnh boot route. Đề nghị người điều phối xác nhận đây là bug đã biết/chấp nhận được, hoặc giao
   một task riêng sửa `PermissionHelper::isCurrentEmployeeHasPermission()` để guard `auth()->user()` null
   (không thuộc phạm vi task này).
2. `Services` và `Transformers` chưa tồn tại trong `Modules/Meeting/` (không do `module:make` sinh mặc định).
   Brief nói "giữ" 2 thư mục này nhưng không nói phải tạo mới — để task sau (khai controller/entity) tự tạo
   khi cần, tránh tạo thư mục rỗng thừa ngoài phạm vi.

## File đã tạo / sửa / xóa

**Tạo (giữ lại):**
- `Modules/Meeting/module.json`
- `Modules/Meeting/composer.json`
- `Modules/Meeting/Config/config.php`, `Config/.gitkeep`
- `Modules/Meeting/Console/.gitkeep`
- `Modules/Meeting/Database/Migrations/.gitkeep`, `Database/Seeders/.gitkeep`,
  `Database/Seeders/MeetingDatabaseSeeder.php`, `Database/factories/.gitkeep`
- `Modules/Meeting/Entities/.gitkeep`
- `Modules/Meeting/Http/Controllers/.gitkeep`, `Http/Controllers/MeetingController.php`,
  `Http/Middleware/.gitkeep`, `Http/Requests/.gitkeep`
- `Modules/Meeting/Providers/.gitkeep`, `Providers/MeetingServiceProvider.php`,
  `Providers/RouteServiceProvider.php`
- `Modules/Meeting/Resources/lang/.gitkeep`
- `Modules/Meeting/Routes/.gitkeep`, `Routes/web.php`
- `Modules/Meeting/Tests/Feature/.gitkeep`, `Tests/Unit/.gitkeep`

**Sửa:**
- `Modules/Meeting/Routes/api.php` — thay route demo bằng khung group rỗng `prefix v1 + middleware auth:api`
- `hrm-api/modules_statuses.json` — side-effect bắt buộc của `module:make`, thêm `"Meeting": true`

**Xóa (theo brief Bước 2):**
- `Modules/Meeting/Resources/assets/` (toàn bộ)
- `Modules/Meeting/Resources/views/` (toàn bộ)
- `Modules/Meeting/webpack.mix.js`
- `Modules/Meeting/package.json`

## Không có

- Không `git commit`, không `git push`, không `git stash`, không `git checkout` file nào.
- Không sửa file nào ngoài `Modules/Meeting/` trừ side-effect bắt buộc `modules_statuses.json` nêu trên.
- Không tạo Model/Entity nào (đúng ràng buộc "Model/entity chưa tạo ở task này").

---

## Fix round 1/5 — Finding Important: 2 file demo web/view vỡ

**Bối cảnh:** module đã được chuyển sang worktree
`/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api` (branch `feat/quan-ly-phong-hop`).
Toàn bộ thao tác fix dưới đây làm trong worktree này, KHÔNG phải checkout gốc `HRM/hrm-api`.

**Finding:** `artisan module:make` (Bước 1, task gốc) sinh sẵn 2 file demo mâu thuẫn với yêu cầu "module chỉ
có API":
- `Modules/Meeting/Routes/web.php` — route demo `GET /meeting` (middleware `web`, không có `auth`) trỏ
  `MeetingController@index`
- `Modules/Meeting/Http/Controllers/MeetingController.php` — action `index()` trả `view('meeting::index')`,
  nhưng `Resources/views` đã bị xóa ở Bước 2 → gọi route này sẽ vỡ (view not found) và không có auth.

### 1. Đã kiểm `RouteServiceProvider` trước khi quyết định xóa hay giữ `web.php`

Đọc `Modules/Meeting/Providers/RouteServiceProvider.php` trong worktree:

```php
public function map()
{
    $this->mapApiRoutes();
    $this->mapWebRoutes();     // <-- gọi KHÔNG điều kiện
}

protected function mapWebRoutes()
{
    Route::middleware('web')
        ->namespace($this->moduleNamespace)
        ->group(module_path('Meeting', '/Routes/web.php'));   // <-- require thẳng file này
}
```

`map()` gọi `mapWebRoutes()` vô điều kiện, và `mapWebRoutes()` `require` thẳng
`module_path('Meeting', '/Routes/web.php')` — không có guard `file_exists`. Nếu xóa hẳn file, mọi request
boot route (mọi request HTTP, mọi lệnh artisan có boot route) sẽ vỡ ngay ở tầng framework vì `require` một
file không tồn tại.

**Kết luận:** GIỮ file `Routes/web.php`, chỉ làm rỗng route bên trong (đúng theo hướng dẫn yêu cầu sửa, đã
xác nhận đúng bằng cách đọc provider chứ không đoán).

### 2. Đã sửa

- Xóa hẳn `Modules/Meeting/Http/Controllers/MeetingController.php` (không còn controller demo nào tham
  chiếu view đã xóa).
- Ghi lại `Modules/Meeting/Routes/web.php` thành rỗng route, chỉ còn:
  ```php
  <?php

  // Module Meeting chỉ phục vụ API, xem Routes/api.php
  ```

### 3. Kiểm chứng lại (trong worktree, server 8001 đã chạy sẵn, không tự khởi động server khác)

```
$ cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api
$ /opt/homebrew/opt/php@7.4/bin/php artisan module:list | grep -i meeting
| Meeting        | Enabled | 0        | .../hrm-worktrees/phong-hop-api/Modules/Meeting |
```
→ Meeting vẫn Enabled.

```
$ curl -s -o /tmp/meeting_curl_body.txt -w "HTTP_CODE:%{http_code}\n" http://127.0.0.1:8001/meeting
HTTP_CODE:404
$ cat /tmp/meeting_curl_body.txt
{"code":404,"message":"Route Not Found!"}
```
→ 404 (route không còn tồn tại), không còn 200/500 do thiếu view. File tạm `/tmp/meeting_curl_body.txt` đã
xóa sau khi kiểm.

`git status --short` trong worktree sau fix:
```
 M modules_statuses.json
?? Modules/Meeting/
```
Không có gì ngoài `Modules/Meeting/` (và side-effect `modules_statuses.json` đã ghi nhận từ trước, không
phát sinh thêm do fix round này).

**Trạng thái sau fix:** finding đã được khắc phục, kiểm chứng bằng curl thật trên server đang chạy —
không dùng lại kết luận cũ.
