# Fix: Chức vụ trùng tên khác guard chặn lưu (Hướng A)

**Bối cảnh:** Sau gộp DB, bảng `roles` chứa chung cả chức vụ ERP (guard `web`,
id 100001+) lẫn HRM (guard `api`, id 3..55). `RolesController` validate
`Rule::unique('roles','name')` **không scope `guard_name`** → khi tạo/sửa 1
chức vụ ERP trùng tên với chức vụ HRM (vd "Super admin") bị chặn "Tên chức vụ
đã tồn tại". Collation `utf8mb4_unicode_ci` nên trùng cả khác hoa/thường/dấu.

**Quyết định:** Hướng A — scope validate unique về `guard_name='web'` (guard ERP)
để chỉ so trùng trong phạm vi chức vụ của ERP. HRM đã tự scope guard qua Spatie
nên không đụng. (Hướng B — gộp về 1 bộ quyền chung — để làm sau, việc lớn.)

**Phạm vi:** chỉ `app/Http/Controllers/Common/RolesController.php`, 4 vị trí
`Rule::unique` (store 2 + update 2). Không đụng data, không đụng HRM.

## Tasks

- [x] Thêm `->where('guard_name','web')` vào 2 `Rule::unique` trong `store()`
- [x] Thêm `->where('guard_name','web')` vào 2 `Rule::unique` trong `update()` (giữ `->ignore($id)`)
- [x] `php -l` file sạch
- [x] Verify: repro validate tinker (read-only) — 3 ca đúng: sửa "Super Admin" trùng HRM → cho lưu;
      tạo/sửa trùng chức vụ ERP (web) → vẫn chặn; tạo tên chỉ có ở HRM → cho tạo

## Bổ sung: Danh sách QUYỀN trộn guard HRM ở màn tạo/sửa chức vụ (2026-09-29)

**Bối cảnh:** cùng gốc bệnh gộp DB — `create()`/`edit()`/`copy()` nạp `Permission::all()`
**không lọc guard** → checkbox phân quyền hiện lẫn quyền HRM (guard `api`) và ERP (guard `web`).
Ví dụ nhóm "Quản lý quyết toán hợp đồng" hiện cả "TP duyệt..." (id 942, api/HRM) lẫn
"Trưởng phòng duyệt..." (id 100854, web/ERP). Tick nhầm quyền `api` → lưu vào
`role_has_permissions` nhưng ERP kiểm theo guard `web` → quyền chết, vô tác dụng.

Đồng đội đã vá anh em cùng họ ở `EmployeesController::index()` (commit `aebdf10850`) bằng
`Role::where('guard_name','web')` → dùng chung kỹ thuật đó cho danh sách quyền.

**Phạm vi:** `RolesController` 3 vị trí `Permission::all()` (create 66 / edit 79 / copy 267).

- [x] Đổi `Permission::all()` → `Permission::where('guard_name','web')->get()` ở create()/edit()/copy()
- [x] `php -l` file sạch
- [x] Verify tinker: danh sách quyền chỉ còn guard `web`; nhóm "Quản lý quyết toán hợp đồng" còn đúng 7 quyền ERP

## Bổ sung: quét toàn ERP các query roles/permissions chưa lọc guard (2026-09-29)

Grep `Permission::all|get`, `Role::all|get|select`, `Permission::where('name')`, `Rule::unique`.
Đã đúng guard từ trước: Employee.php (743/1439/1479/2629), FirmContract.php:829,
EmployeesController (đồng đội aebdf10850). Còn 3 chỗ xử lý:

- [x] #1 `AnalyticController.php:38` (dropdown lọc "Doanh thu theo nhân viên"): `Role::select(...)`
      → `Role::where('guard_name','web')->select(...)`. Verify: 123→76, loại 47 HRM.
- [x] #3 `DeviceErrorController::create()` 2 dòng `Permission::all()` là CODE CHẾT (view create.blade.php
      không dùng `$permissions`) → xóa cả 2 + bỏ khỏi compact.
- [x] #2 Lọc màn `/admin/roles` về chỉ chức vụ ERP (web) — user chốt: `Role::searchByFilter`
      (Role.php) thêm `->where('guard_name','web')`; export Excel/CSV/PDF (RolesController 307/318/329)
      `Role::all()` → `Role::where('guard_name','web')->get()`. Verify list 123→76, export 76.
- [x] `php -l` 4 file sạch.

## Checkpoint — 2026-09-29
Vừa hoàn thành: (a) commit+push 219eff32e8 (Rule::unique ×4 + Permission::all ×3 scope web trong
RolesController); (b) fix thêm Analytic' dropdown, xóa code chết DeviceErrorController, lọc web cho
searchByFilter + 3 export roles. Đã rebase local lên remote gop_db.
Đang làm dở: (không) — đợt (b) chờ commit.
Bước tiếp theo: commit+push đợt (b); sau đó cân nhắc Hướng B (gộp 1 bộ quyền).
Blocked: (không)
