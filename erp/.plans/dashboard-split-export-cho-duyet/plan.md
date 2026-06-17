# Dashboard Yêu cầu xuất tách chờ duyệt — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development hoặc superpowers:executing-plans để thực thi từng task. Steps dùng checkbox (`- [ ]`).

**Goal:** Thêm 1 ô dashboard đếm Yêu cầu xuất tách (`SplitExportRequest`) đang chờ duyệt vào group "Kế toán kho".

**Architecture:** Dashboard data-driven — `HomeController::approveList()` build mảng `$result[]`, blade `home.blade.php` tự render item theo `group`, chỉ hiện khi `count > 0`. Thêm 1 `use` model + 1 item vào block `can('Kế toán kho')` sẵn có. Không sửa blade/model/list/migration.

**Tech Stack:** Laravel 8 (Eloquent count + `route()`).

> **Lưu ý dự án:** KHÔNG commit/push git khi chưa được yêu cầu. "Commit" chỉ làm khi user yêu cầu — mặc định dừng ở verify browser.

**Design:** `.plans/dashboard-split-export-cho-duyet/design.md`

---

### Task 1: Thêm import + item dashboard

**Files:**
- Modify: `app/Http/Controllers/HomeController.php` — (a) thêm `use` sau dòng 61; (b) thêm item trong block `can('Kế toán kho')` sau item "Yêu cầu xuất ghép chờ duyệt" (sau dòng 1281)

- [x] **Step 1: Thêm `use` model SplitExportRequest**

Sau dòng 61 (`use App\Model\Warehouse\JoinExportRequest;`), thêm:
```php
use App\Model\Warehouse\SplitExportRequest;
```

- [x] **Step 2: Thêm item dashboard sau item "Yêu cầu xuất ghép chờ duyệt"**

Tìm đoạn (dòng ~1275-1281):
```php
            $result[] = [
                'group' => 'KE_TOAN_KHO',
                'name' => 'Yêu cầu xuất ghép chờ duyệt',
                'link' => route('joinExportRequest.index') . '?type=for_approve',
                'count' => JoinExportRequest::query()->where('company_id', Auth::user()->info->company_id)
				->where('status', '=', 2)->count(),
            ];
```
Chèn ngay sau nó (vẫn trong block `if ($logged_user->can('Kế toán kho'))`):
```php

            $result[] = [
                'group' => 'KE_TOAN_KHO',
                'name' => 'Yêu cầu xuất tách chờ duyệt',
                'link' => route('splitExportRequest.all'),
                'count' => SplitExportRequest::query()
                    ->where('status', SplitExportRequest::CHO_DUYET)
                    ->where('company_id', $logged_user->info->company_id)
                    ->count(),
            ];
```

- [x] **Step 3: Kiểm tra cú pháp PHP** ✅ `No syntax errors detected`. Route `splitExportRequest.all` đã xác nhận tồn tại (web.php:1103).

---

### Task 2: Verify trên browser

- [ ] **Step 1: Ô hiển thị đúng**

Đăng nhập user có quyền "Kế toán kho", công ty có YC xuất tách trạng thái chờ duyệt → dashboard trang chủ → group "Kế toán kho".
Expected: ô **"Yêu cầu xuất tách chờ duyệt"** hiện đúng số lượng. Bấm → mở `/admin/warehouse/split_export_requests/all`.

- [ ] **Step 2: Số đếm khớp danh sách**

So số trên ô với số phiếu trạng thái "Chờ duyệt" của công ty trong màn danh sách.
Expected: khớp.

- [ ] **Step 3: Ẩn khi count = 0**

Công ty không có YC xuất tách chờ duyệt.
Expected: ô không hiển thị (blade render khi `count > 0`).

- [ ] **Step 4: Ẩn khi không có quyền**

User KHÔNG có quyền "Kế toán kho".
Expected: không thấy ô (cả block `can('Kế toán kho')` bị bỏ qua).

---

## Self-Review (đã rà)

- **Spec coverage:** design "Thiết kế" (use + item) → Task 1; "Test" (4 ca) → Task 2. Đủ.
- **Placeholder scan:** không TBD/TODO; mọi step có code/command.
- **Type consistency:** `SplitExportRequest::CHO_DUYET` (=2), group `KE_TOAN_KHO`, route `splitExportRequest.all`, biến `$logged_user` — khớp code thật đã verify.
