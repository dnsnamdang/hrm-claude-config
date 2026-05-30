# Thêm cột "Sale phụ trách" vào danh sách khách hàng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hiển thị cột "Sale phụ trách" trong danh sách khách hàng, lấy dữ liệu từ tab Phân công phụ trách (chỉ nhân viên department_id = 83).

**Architecture:** Eager load relationship `categoryCustomerPersonChargeBusiness` với join qua `employees` → `employee_infos` để lọc department_id = 83. Format dữ liệu trong Resource, FE chỉ thêm cột hiển thị.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue

---

## File Structure

| Action | File | Mục đích |
|--------|------|----------|
| Modify | `hrm-thanhan-api/Modules/Category/Services/CustomerService.php:87` | Thêm eager load với join filter |
| Modify | `hrm-thanhan-api/Modules/Category/Transformers/CategoryCustomer/CategoryCustomerResource.php` | Thêm field + method format |
| Modify | `hrm-thanhan-client/pages/category/customer/index.vue` | Thêm cột + template slot |

---

### Task 1: Backend — Thêm eager load trong CustomerService

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/CustomerService.php:87-93`

- [x] **Step 1: Thêm eager load sau dòng filter cuối cùng**

Mở file `hrm-thanhan-api/Modules/Category/Services/CustomerService.php`. Tìm đoạn code sau (dòng 85-93):

```php
            ->when(isset($request->is_debt_limit_active) && in_array((int) $request->is_debt_limit_active, [0, 1]), function ($query) use ($request) {
                return $query->where('is_debt_limit_active', (int) $request->is_debt_limit_active);
            });
        if (isCurrentEmployeeHasPermission('Xem danh sách khách hàng') || isCurrentEmployeeHasPermission('Quản lý khách hàng')) {
        } else {
            $result->where('created_by', auth()->user()->id);
        }

        $result->orderBy('id', 'desc');
```

Thêm eager load **ngay sau dấu `;` của dòng 87** (sau chuỗi `->when` cuối cùng), **trước đoạn `if (isCurrentEmployeeHasPermission...)`**:

```php
            ->when(isset($request->is_debt_limit_active) && in_array((int) $request->is_debt_limit_active, [0, 1]), function ($query) use ($request) {
                return $query->where('is_debt_limit_active', (int) $request->is_debt_limit_active);
            });

        $result->with(['categoryCustomerPersonChargeBusiness' => function ($q) {
            $q->join('employees', 'employees.id', '=', 'category_customer_person_charge_business.employee_id')
              ->join('employee_infos', 'employee_infos.id', '=', 'employees.employee_info_id')
              ->where('employee_infos.department_id', 83)
              ->select('category_customer_person_charge_business.*', 'employee_infos.fullname as employee_name');
        }]);

        if (isCurrentEmployeeHasPermission('Xem danh sách khách hàng') || isCurrentEmployeeHasPermission('Quản lý khách hàng')) {
        } else {
            $result->where('created_by', auth()->user()->id);
        }

        $result->orderBy('id', 'desc');
```

- [x] **Step 2: Kiểm tra cú pháp**

Chạy lệnh:
```bash
cd /d/laragon/www/dns/hrm-thanhan-api && php artisan tinker --execute="echo 'syntax ok';"
```
Expected: `syntax ok` (không có lỗi parse)

---

### Task 2: Backend — Thêm format dữ liệu trong CategoryCustomerResource

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/CategoryCustomer/CategoryCustomerResource.php`

- [x] **Step 1: Thêm field `sale_person_charge` vào mảng return trong `toArray()`**

Mở file `hrm-thanhan-api/Modules/Category/Transformers/CategoryCustomer/CategoryCustomerResource.php`. Tìm dòng 49:

```php
            'is_debt_limit_active' => (int) $this->is_debt_limit_active,
```

Thêm field mới ngay sau dòng đó:

```php
            'is_debt_limit_active' => (int) $this->is_debt_limit_active,
            'sale_person_charge' => $this->formatSalePersonCharge(),
```

- [x] **Step 2: Thêm method `formatSalePersonCharge()` sau method `toArray()`**

Thêm method mới ngay sau closing `}` của `toArray()` (trước closing `}` cuối cùng của class):

```php
    private function formatSalePersonCharge()
    {
        $personCharge = $this->categoryCustomerPersonChargeBusiness;

        if (!$personCharge || $personCharge->isEmpty()) {
            return null;
        }

        $grouped = $personCharge->groupBy('employee_id');

        $lines = [];
        foreach ($grouped as $employeeId => $records) {
            $employeeName = $records->first()->employee_name;
            $products = $records->pluck('array_product_name')
                ->filter()
                ->unique()
                ->implode(', ');

            if ($products) {
                $lines[] = $employeeName . ' (' . $products . ')';
            } else {
                $lines[] = $employeeName;
            }
        }

        return implode("\n", $lines);
    }
```

- [x] **Step 3: Kiểm tra cú pháp**

Chạy lệnh:
```bash
cd /d/laragon/www/dns/hrm-thanhan-api && php artisan tinker --execute="echo 'syntax ok';"
```
Expected: `syntax ok`

---

### Task 3: Frontend — Thêm cột "Sale phụ trách" vào danh sách

**Files:**
- Modify: `hrm-thanhan-client/pages/category/customer/index.vue`

- [x] **Step 1: Thêm column definition vào mảng `fields`**

Mở file `hrm-thanhan-client/pages/category/customer/index.vue`. Tìm đoạn (dòng 435-441):

```javascript
                {
                    key: 'max_debt_limit',
                    label: 'Hạn mức công nợ (VNĐ)',
                    sortable: true,
                    tdClass: 'text-right',
                    isVisible: true,
                },
```

Thêm cột mới **ngay sau cột `max_debt_limit`** và **trước cột `actions`**:

```javascript
                {
                    key: 'max_debt_limit',
                    label: 'Hạn mức công nợ (VNĐ)',
                    sortable: true,
                    tdClass: 'text-right',
                    isVisible: true,
                },
                {
                    key: 'sale_person_charge',
                    label: 'Sale phụ trách',
                    isVisible: true,
                    thStyle: { 'min-width': '250px' },
                },
                {
                    key: 'actions',
                    label: 'Hành động',
                    isVisible: true,
                },
```

- [x] **Step 2: Thêm template slot để render xuống dòng**

Tìm đoạn template `max_debt_limit` (dòng 170-175):

```html
                                <template v-slot:cell(max_debt_limit)="{ item }">
                                    <span v-if="item.is_debt_limit_active == 1 && item.max_debt_limit !== null">
                                        {{ formatMoney(item.max_debt_limit) }}
                                    </span>
                                    <span v-else class="text-muted">—</span>
                                </template>
```

Thêm template slot mới **ngay sau** template `max_debt_limit`:

```html
                                <template v-slot:cell(max_debt_limit)="{ item }">
                                    <span v-if="item.is_debt_limit_active == 1 && item.max_debt_limit !== null">
                                        {{ formatMoney(item.max_debt_limit) }}
                                    </span>
                                    <span v-else class="text-muted">—</span>
                                </template>
                                <template v-slot:cell(sale_person_charge)="{ item }">
                                    <div v-if="item.sale_person_charge">
                                        <div v-for="(line, idx) in item.sale_person_charge.split('\n')" :key="idx">
                                            {{ line }}
                                        </div>
                                    </div>
                                </template>
```

- [x] **Step 3: Kiểm tra trên trình duyệt**

Mở trình duyệt → vào màn Danh sách khách hàng → kiểm tra:
1. Cột "Sale phụ trách" hiển thị đúng vị trí (sau "Hạn mức công nợ", trước "Hành động")
2. Khách hàng có sale department_id = 83 → hiển thị tên + mảng hàng hoá
3. Khách hàng không có sale → ô trống
4. Khách hàng có nhiều sale → mỗi sale 1 dòng

---

## Checklist hoàn thành

- [x] Task 1: Eager load trong CustomerService
- [x] Task 2: Format dữ liệu trong CategoryCustomerResource
- [x] Task 3: Thêm cột FE trong index.vue
- [x] Kiểm tra trên trình duyệt
