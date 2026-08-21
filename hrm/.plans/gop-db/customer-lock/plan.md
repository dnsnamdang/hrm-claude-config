# Plan — customer-lock (Khóa / Mở khóa khách hàng)

**Nhánh:** `gop_db` (cả 2 repo) · @khoipv
**Design:** `.plans/gop-db/customer-lock/design.md` ·
**Spec:** `docs/superpowers/specs/gop-db/2026-08-11-customer-lock-design.md`

## Phase 1 — Backend (`hrm-api`, Modules/Assign)

- [x] 1.1 `CustomerService::setStatus(int $id, int $status): TpCustomer` — `findOrFail`, gán
      `status` + `updated_by` = `ErpPermissionHelper::erpEmployeeId()` **tường minh** (tránh
      BaseModel ghi đè bằng HRM user id), `save()`
- [x] 1.2 `CustomerController::lock($id)` / `unlock($id)` — gọi service, 404 khi không tìm thấy,
      500 + log khi lỗi khác, thành công trả `{id, status}`
- [x] 1.3 Route `POST /assign/customers/{id}/lock` + `/{id}/unlock`, middleware
      `erpPermission:Xóa khách hàng`
- [x] 1.4 `CustomerService::parentOptions()` thêm `->where('status', 1)` (ô "Công ty mẹ" không chọn
      được KH đã khóa — bám ERP `CustomersController:169,203`)
- [x] 1.5 Verify: `php -l` + tinker (lock/unlock đổi `status` và `updated_by`; `parentOptions`
      loại KH khóa; `index()` không lọc vẫn trả KH khóa)

## Phase 2 — Frontend (`hrm-client`, pages/assign/customers/index.vue)

- [x] 2.1 Nút Khóa/Mở khóa đặt trong **cột Trạng thái** (cạnh badge) theo khuôn màn danh mục
      `pages/finance/currencies/index.vue`: `btn btn-light border btn-sm action-icon-btn`, icon
      `ri-lock-line` khi `status === 1` / `ri-lock-unlock-line` khi khác, chỉ hiện khi `perm.delete`.
      (Bản đầu đặt trong hàng nút cột *Mã KH - Tên KH* — user yêu cầu đổi 2026-08-11)
- [x] 2.2 `confirmLockCustomer(item, action)` → set `pendingLock` → mở `BaseConfirmModal`
      (`confirm-lock-customer`); gọi thẳng từ nút ở cột Trạng thái, KHÔNG đi qua `handleRowAction`
- [x] 2.3 Handler xác nhận: `POST assign/customers/{id}/{action}` → toast → `loadData()`
      (giữ nguyên trang + bộ lọc); lỗi dùng helper xử lý lỗi sẵn có của trang
- [x] 2.4 Verify: parse SFC + rà không phá hàng nút cũ (Xem / Quản lý / Sửa)

## Phase 3 — Bàn giao

- [x] 3.1 Cập nhật `.plans/gop-db/STATUS.md`
- [ ] 3.2 Chờ user test trình duyệt: nút đúng theo trạng thái + quyền · modal xác nhận · badge đổi
      sau khi khóa · popup chọn KH (Dự án TKT / Meeting) không còn KH vừa khóa · ô lọc KH màn Báo giá
      vẫn thấy KH đã khóa

---

## Kết quả verify (2026-08-11)

**BE — tinker trên DB thật** (KH `50TPHXBI-277` id 232396, đã khôi phục nguyên trạng
`status`/`updated_by`/`updated_at` sau test):

| Kiểm tra | Kết quả |
| --- | --- |
| `setStatus($id, 0)` | `status = 0`, `updated_by` = ERP employee id |
| `setStatus($id, 1)` | `status = 1` |
| `parentOptions()` trước / sau khi khóa | 1 / 0 → KH khóa biến khỏi ô "Công ty mẹ" |
| `index()` không lọc | vẫn thấy KH đã khóa (ô lọc/danh sách giữ nguyên hành vi) |
| `index()` lọc `status=1` | không thấy KH đã khóa → popup `ChooseErpCustomerModal` tự loại |
| `setStatus(999999999, 0)` | ném `ModelNotFoundException` → controller trả 404 |

**Route** (liệt kê qua `app('router')->getRoutes()`, vì `php artisan route:list` crash sẵn:
`isCurrentEmployeeHasPermission()` gọi `auth()->user()->employee_info_id` khi chưa đăng nhập
— `app/Helper/PermissionHelper.php:23`, kích hoạt từ
`Modules/Timesheet/.../RequestUpdateTimeSheetController.php:51`. Lỗi có sẵn, không liên quan feature này):

```
POST api/v1/assign/customers/{id}/lock    mw=api,auth:api,erpPermission:Xóa khách hàng
POST api/v1/assign/customers/{id}/unlock  mw=api,auth:api,erpPermission:Xóa khách hàng
```

**Quyền**: `ErpPermissionHelper::customerPermissions()` với Super admin trả `delete: true` → nút hiện.

**FE**: `php -l` 3 file BE sạch; parse SFC `pages/assign/customers/index.vue` OK.

### Checkpoint — 2026-08-11
Vừa hoàn thành: BE lock/unlock + lọc `parent-options`, FE nút Khóa/Mở khóa + modal xác nhận.
Đang làm dở: không.
Bước tiếp theo: user test trình duyệt theo mục 3.2.
Blocked: không.

### Checkpoint — 2026-08-11 (đổi vị trí nút)
Vừa hoàn thành: chuyển nút Khóa/Mở khóa từ hàng nút cột *Mã KH - Tên KH* sang **cột Trạng thái**,
đứng cạnh badge, theo đúng khuôn các màn danh mục đã làm trước (`finance/currencies`); thêm CSS
`.action-icon-btn` cho khớp kích thước. `getRowActions()`/`handleRowAction` trả về nguyên trạng
(chỉ còn Xem / Quản lý / Sửa).
Đang làm dở: không.
Bước tiếp theo: user test trình duyệt.
Blocked: không.

### Checkpoint — 2026-08-12 (HOÀN THÀNH)
Vừa hoàn thành: user đã test trình duyệt xong → feature chuyển sang mục **Hoàn thành** trong
`.plans/gop-db/STATUS.md`.
Đang làm dở: không.
Bước tiếp theo: không còn việc trong phạm vi feature này.
Blocked: không.
