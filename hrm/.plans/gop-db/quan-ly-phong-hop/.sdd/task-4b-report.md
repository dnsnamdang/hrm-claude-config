# Task 4b — Báo cáo: dựng đường đăng nhập e2e cho worktree

Status: **DONE**

## 1. Cách tìm bảng nối role (không đoán)

Đọc `Modules/Timesheet/Entities/Employee.php` (worktree
`hrm-worktrees/phong-hop-api`): model dùng `trait HasRoles` của
`spatie/laravel-permission`, không tự khai `roles()`. Tên bảng lấy từ
`config/permission.php`:

```
'model_has_roles'      => 'employee_has_roles',   // KHÔNG phải model_has_roles
'model_has_permissions'=> 'employee_has_permissions',
'role_has_permissions' => 'role_has_permissions',
'model_morph_key'      => 'employee_id',
'teams'                => false,
```

→ Bảng nối thật là **`employee_has_roles`** (cột `role_id`, `model_type`,
`employee_id`, `company_id`, `position`, PK 4 cột). `model_has_roles` đúng là
không tồn tại trên DB gộp như ghi chú của Task 4b.

Lưu ý quan trọng phát hiện thêm: `teams => false` nên
`Employee::getAllPermissions()` (method chuẩn của Spatie, và cũng là hàm mà
middleware `CheckPermission` dùng) **không lọc theo `company_id`** — nó gom
permission của MỌI role employee có, bất kể cột `company_id` trong
`role_has_permissions`/`employee_has_roles`. Cột `company_id` ở 2 bảng này chỉ
là cột phụ (dùng ở nơi khác, vd. `isCurrentEmployeeHasPermission()` trong
`PermissionHelper.php`), không phải cơ chế multi-tenant chuẩn của Spatie.

## 2. Hai tài khoản đã chọn

Permission `'Quản lý danh mục phòng họp'` = id **1574**; xác nhận
`role_has_permissions` có đúng 1 dòng cấp quyền này: `role_id=18` (Super
admin), `company_id=1`.

| Vai trò | id | email | Cách xác nhận |
|---|---|---|---|
| CÓ quyền (admin) | **34** | thuydt.qttt@tanphat.com | Có role_id=18 trong `employee_has_roles`; `employee_infos.company_role=1` → `current_company_role=1` khớp `role_has_permissions.company_id=1` |
| KHÔNG quyền | **25** | cannt.kd1@tanphat.com | Không có role_id=18 (chỉ có role `Trợ lý kinh doanh` 100003 + `Quản lý báo cơm` 20); `current_company_role=1` |

Xác nhận bằng tinker (dùng đúng code path của middleware `CheckPermission`:
`Modules\Timesheet\Entities\Employee::find($id)->getAllPermissions()`):

```
E34_HAS=YES   (578 quyền)
E25_HAS=NO    (10 quyền — toàn bộ liên quan "báo cơm")
```

**CHỈ ĐỌC** — không tạo/sửa/xoá bản ghi nào trong DB.

## 3. Script mint token

`.plans/gop-db/quan-ly-phong-hop/.sdd/mint-auth.php` — chạy qua:

```bash
php artisan tinker --execute="require '.../.sdd/mint-auth.php';"
```

Dùng `\App\Models\TpEmployee::find($id)` (đúng model guard JWT, `config/auth.php`)
+ `\JWTAuth::fromUser($u)`. Chạy thành công, mint được cả 2 token
(exp ~2026-11 dựa trên `iat`/`exp` trong JWT).

## 4. 3 file auth đã ghi

- `e2e/.auth/api-wt.json` — `{"token": "...", "employee_id": 34}`
- `e2e/.auth/user-wt.json` — storageState origin `http://127.0.0.1:3001`, `access_token` = token id 34
- `e2e/.auth/user-nocost-wt.json` — storageState origin `http://127.0.0.1:3001`, `access_token` = token id 25

Đã kiểm `api.json`, `user.json`, `user-nocost.json` (của phiên khác) **không bị đụng** — md5
trước/sau không đổi, mtime vẫn 14/09.

## 5. Kiểm token qua API

**Bước 4 của brief** (`GET /api/v1/assign/meeting_cancel_reasons`, route index `'/'`) trả
**403**, không phải 200 như kỳ vọng trong brief:

```
{"message":"Bạn không có quyền thực hiện chức năng này","code":403}
```

Điều tra: route này gate bởi
`checkPermission:'Quản lý danh mục lý do hủy cuộc họp'|'Xem danh mục lý do hủy cuộc họp'`
(id 1184/1185) — **KHÔNG phải** permission `'Quản lý danh mục phòng họp'` (1574) mà Task 4
vừa seed. Kiểm `role_has_permissions` cho 2 id này: **0 dòng** — chưa role nào trên toàn DB
được cấp 2 quyền đó (kể cả Super admin). Đây là pre-existing gap của DB gộp, không phải lỗi
mint token.

Bằng chứng token vẫn HOẠT ĐỘNG (không phải 401 do token hỏng):

```
GET /api/v1/assign/meeting_cancel_reasons/getAll   (route KHÔNG gate permission)
  admin (34)  -> 200 {"code":200,"message":"success","data":[...]}
  nocost (25) -> 200 {"code":200,"message":"success","data":[...]}
```

→ 403 ở bước 4 là do route đó không liên quan đến quyền vừa cấp, KHÔNG phải BLOCKED. Đã báo
cáo để task sau biết route `assign/meeting_cancel_reasons` KHÔNG dùng được làm "endpoint quyền
phòng họp mẫu".

## 6. Kiểm phân quyền khác nhau thật sự

Không tìm thấy route HTTP nào hiện tại gate trực tiếp bởi
`'Quản lý danh mục phòng họp'` (permission mới, feature UI/API của plan này chưa được xây ở
task sau) và không có endpoint kiểu `/users/auth/me` trả danh sách tên quyền (endpoint
`user-profile` có dòng `# TODO remove` che permission; endpoint `/my-permissions` là của module
Customer, không liên quan employee).

Thay vào đó xác minh 2 lớp:

1. **Code path chính xác của middleware** (tinker, mục 2): `getAllPermissions()` của employee
   34 chứa `'Quản lý danh mục phòng họp'`, employee 25 thì không.
2. **HTTP thật** trên 1 route hiện có cùng cơ chế `checkPermission`, mà 34 có quyền còn 25
   không có (`'Quản lý danh mục nguyên nhân thất bại dự án'`, route
   `GET /api/v1/assign/reason_project_failures`):

```
admin (34)  -> HTTP_CODE=200
nocost (25) -> HTTP_CODE=403
```

→ Chứng minh cả 2 token đều xác thực được (không 401), và cơ chế phân quyền phân biệt đúng
giữa 2 tài khoản qua đúng middleware `CheckPermission` mà các API sau của plan này sẽ dùng.

## 7. Kiểm UI (Playwright)

Spec giữ lại: `e2e/tests/meeting/_auth-smoke.spec.ts` (`test.use({ storageState:
'.auth/user-wt.json' })`), mở `/meeting/dashboard`, khẳng định KHÔNG bị chuyển `/login` +
sidebar (`.left-side-menu`, xem `components/training-components/Sidebar.vue`) hiển thị.

```
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 \
API_BASE=http://127.0.0.1:8001 npx playwright test tests/meeting/_auth-smoke.spec.ts \
--project=chromium --no-deps --workers=1

✓ 1 [chromium] › tests/meeting/_auth-smoke.spec.ts:19:7 › ... (10.9s)
1 passed (12.0s)
```

Đối chứng âm (test tạm, đã xoá sau khi kiểm — KHÔNG nằm trong repo): mở `/meeting/dashboard`
với storageState rỗng (chưa đăng nhập) → bị đẩy về `/login` đúng như kỳ vọng (3.8s, passed).
Chứng minh assertion "không bị đẩy về /login" ở spec giữ lại là có ý nghĩa thật, không vacuously
true.

## 8. Concerns cho task sau

- Route `assign/meeting_cancel_reasons` (index `/`) KHÔNG dùng được để test quyền — quyền gate
  của nó (id 1184/1185) chưa được cấp cho bất kỳ role nào trên DB gộp. Nếu task sau cần seed lại
  các permission "cũ chưa cấp" này thì cần một task riêng (ngoài scope 4b — không tự sửa DB).
- Chưa có HTTP endpoint trả danh sách quyền của user hiện tại (kiểu `/auth/me`) — nếu task sau
  cần verify quyền qua UI/API cho nhanh, cân nhắc thêm 1 endpoint nhỏ, hoặc tiếp tục dùng cách
  tinker ở mục 2/5 làm nguồn sự thật.
- Token JWT mint bằng `JWTAuth::fromUser()` có hạn dùng dài (dựa theo cấu hình `jwt.ttl`); không
  kiểm tra riêng thời hạn hết token — nếu các task sau chạy nhiều ngày sau, nên mint lại bằng
  script `mint-auth.php` (idempotent, chỉ đọc).
