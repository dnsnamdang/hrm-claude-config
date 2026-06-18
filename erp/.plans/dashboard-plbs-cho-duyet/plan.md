# Dashboard PLBS trong nước chờ duyệt — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development hoặc superpowers:executing-plans để thực thi từng task. Steps dùng checkbox (`- [ ]`).

**Goal:** Thêm 2 ô dashboard đếm PLBS hợp đồng mua hàng trong nước (tự do type=5, theo hãng type=4) đang chờ duyệt vào group "Đặt mua hàng trong nước".

**Architecture:** Dashboard data-driven — `HomeController::approveList()` build mảng `$result[]`, blade `home.blade.php` tự render mọi item theo `group`, chỉ hiện khi `count > 0`. Chỉ cần thêm 2 block vào mảng, không sửa blade/model/migration.

**Tech Stack:** Laravel 8 (Eloquent count + `route()`), AngularJS blade render (sẵn có).

> **Lưu ý dự án:** KHÔNG commit/push git khi chưa được yêu cầu. Bước "Commit" chỉ làm khi user yêu cầu — mặc định dừng ở verify browser.

**Design:** `.plans/dashboard-plbs-cho-duyet/design.md`

---

### Task 1: Thêm 2 block PLBS vào HomeController::approveList()

**Files:**
- Modify: `app/Http/Controllers/HomeController.php` — chèn sau dòng 1890 (sau block "Đơn hỏi hàng - PO trong nước theo hãng", trước block `if ($logged_user->can('Xử lý yêu cầu sửa chữa'))`)

> Ghi chú: `InlandBuyContractNew` đã được dùng trong cùng method (dòng ~1802) nên đã import sẵn — không cần thêm `use`. Hằng dùng: `PHU_LUC_TU_DO = 5`, `PHU_LUC_HANG = 4`, `CHO_DUYET = 2`.

- [x] **Step 1: Chèn 2 block ngay sau dòng 1890**

Sau đoạn:
```php
            $result[] = [
                'group' => 'DAT_MUA_HANG_TRONG_NUOC',
                'name' => 'Đơn hỏi hàng - PO trong nước theo hãng',
                'link' => route('inlandOrderSummaryNew.index') . '?type=firm&_type=for-approve',
                'count' => $count
            ];
        }
```
Chèn thêm:
```php

        if ($logged_user->can('Duyệt hợp đồng mua hàng trong nước')) {
            $count = InlandBuyContractNew::query()
                ->where('type', InlandBuyContractNew::PHU_LUC_TU_DO)
                ->where('status', InlandBuyContractNew::CHO_DUYET)
                ->where('company_id', $logged_user->info->company_id)
                ->count();

            $result[] = [
                'group' => 'DAT_MUA_HANG_TRONG_NUOC',
                'name' => 'PLBS trong nước tự do cần duyệt',
                'link' => route('inlandBuyContractNew.index') . '?type=5&_type=for-approved',
                'count' => $count
            ];
        }

        if ($logged_user->can('Duyệt hợp đồng mua hàng trong nước')) {
            $count = InlandBuyContractNew::query()
                ->where('type', InlandBuyContractNew::PHU_LUC_HANG)
                ->where('status', InlandBuyContractNew::CHO_DUYET)
                ->where('company_id', $logged_user->info->company_id)
                ->count();

            $result[] = [
                'group' => 'DAT_MUA_HANG_TRONG_NUOC',
                'name' => 'PLBS trong nước theo hãng cần duyệt',
                'link' => route('inlandBuyContractNew.index') . '?type=4&_type=for-approved',
                'count' => $count
            ];
        }
```

- [x] **Step 2: Kiểm tra cú pháp PHP** ✅ `No syntax errors detected`

---

### Task 2: Verify trên browser

- [ ] **Step 1: Ô PLBS tự do hiển thị đúng**

Đăng nhập user có quyền "Duyệt hợp đồng mua hàng trong nước" và công ty có PLBS tự do (type=5) chờ duyệt → mở dashboard trang chủ → group "Đặt mua hàng trong nước".
Expected: ô **"PLBS trong nước tự do cần duyệt"** hiện đúng số lượng. Bấm vào → list `/admin/orders/inland_buy_contract_new?type=5&_type=for-approved` chỉ hiện PLBS tự do trạng thái chờ duyệt; số dòng khớp count trên ô.

- [ ] **Step 2: Ô PLBS theo hãng hiển thị đúng**

Tương tự với PLBS theo hãng (type=4).
Expected: ô **"PLBS trong nước theo hãng cần duyệt"** đúng số; link `?type=4&_type=for-approved` ra list đúng.

- [ ] **Step 3: Ẩn khi count = 0**

Công ty không có PLBS chờ duyệt.
Expected: 2 ô **không hiển thị** (blade chỉ render khi `count > 0`).

- [ ] **Step 4: Ẩn khi không có quyền**

User KHÔNG có quyền "Duyệt hợp đồng mua hàng trong nước".
Expected: không thấy 2 ô PLBS.

---

## Self-Review (đã rà)

- **Spec coverage:** design mục "Thiết kế" (2 block) → Task 1; mục "Test" (4 ca) → Task 2. Đủ.
- **Placeholder scan:** không TBD/TODO; mọi step có code/command cụ thể.
- **Type consistency:** hằng `PHU_LUC_TU_DO=5`/`PHU_LUC_HANG=4`/`CHO_DUYET=2`, group `DAT_MUA_HANG_TRONG_NUOC`, route `inlandBuyContractNew.index` khớp code thật đã verify.
