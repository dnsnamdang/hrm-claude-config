# Spec: Phase B — Phân quyền xây dựng giá + duyệt báo giá theo phòng/công ty

**Feature:** project-implementation-types  
**Phase:** B  
**Ngày:** 2026-05-25  
**Người phụ trách:** @dnsnamdang  
**Branch:** tpe-develop-assign

---

## 1. Tổng quan

Phase B tách quyền xây dựng giá theo Type triển khai và thêm lọc phòng/công ty cho luồng duyệt báo giá.

**3 block:**
1. **Tách permission YCXD giá** — Type 2 (theo phòng) vs Type 3 (theo công ty)
2. **Lọc duyệt báo giá** — TP theo phòng quản lý, BGĐ theo công ty
3. **Tách notification** — YCXD giá gửi đúng nhóm người

## 2. Block 1 — Tách permission YCXD giá

### 2.1 Permission

| Permission | Hành động | Áp dụng |
|---|---|---|
| **Xây dựng giá bán theo phòng** (MỚI) | NLG nhận YCXD giá Type 2 cùng phòng | `pricing_request.department_id` = phòng user |
| **Xây dựng giá bán theo công ty** (ĐỔI TÊN từ "Xây dựng giá Bom giải pháp") | NLG nhận YCXD giá Type 3 | Tất cả YCXD giá Type 3 |

### 2.2 Migration

```php
// 1. Đổi tên permission cũ
Permission::where('name', 'Xây dựng giá Bom giải pháp')->update([
    'name' => 'Xây dựng giá bán theo công ty',
    'display_name' => 'Xây dựng giá bán theo công ty',
]);

// 2. Tạo permission mới
Permission::firstOrCreate(
    ['name' => 'Xây dựng giá bán theo phòng'],
    [
        'guard_name' => 'api',
        'display_name' => 'Xây dựng giá bán theo phòng',
        'group' => 'Báo giá',
        'type' => 4,
    ]
);
```

### 2.3 BE — PricingRequestController::index

Logic hiện tại:
```
hasBuildPrice → thấy tất cả YCXD giá status >= CHO_XD_GIA
không có quyền → chỉ thấy do mình tạo
```

Logic mới:
```
hasBuildByDept (quyền "theo phòng") → thấy YCXD giá mà:
  - project.implementation_type = 2
  - pricing_request.department_id = phòng user hiện tại
  - status IN (CHO_XD_GIA, DANG_XD_GIA, DA_CO_BAO_GIA, DONG, DUNG)

hasBuildByCompany (quyền "theo công ty") → thấy YCXD giá mà:
  - project.implementation_type = 3 (hoặc NULL — legacy)
  - status IN (CHO_XD_GIA, DANG_XD_GIA, DA_CO_BAO_GIA, DONG, DUNG)

Có cả 2 quyền → UNION cả 2 điều kiện trên

Không có quyền nào → chỉ thấy do mình tạo (NV KD)
```

**Xác định implementation_type:** Join `pricing_requests.project_id` → `prospective_projects.implementation_type`

**Xác định phòng user:** `auth()->user()->info->department_id`

### 2.4 BE — QuotationService::createFromRequest

Không thay đổi logic tạo. `department_id` trên quotation tự fill từ `BaseModel::creating()` = phòng NLG tạo báo giá. Đúng yêu cầu.

### 2.5 Các nơi tham chiếu permission cũ cần cập nhật

Sau khi đổi tên "Xây dựng giá Bom giải pháp" → "Xây dựng giá bán theo công ty", cần update code tham chiếu:

1. **PricingRequestController::index** (line 60) — đổi tên permission check
2. **PricingRequestService::notifyPricingBuildersNewRequest** (line 265) — tách logic notify
3. **FE** nếu có check permission name client-side

## 3. Block 2 — Lọc duyệt báo giá

### 3.1 QuotationService::getPendingApproval

Logic hiện tại:
```
hasTP → thấy tất cả BG status = CHO_TP_DUYET
hasBGD → thấy tất cả BG status = CHO_BGD_DUYET
```

Logic mới:
```
hasTP → BG status = CHO_TP_DUYET
  + quotation.department_id IN employee_manage_departments của user hiện tại

hasBGD → BG status = CHO_BGD_DUYET
  + quotation.company_id = user.info.company_id
```

**Lấy danh sách phòng quản lý:**
```php
$managedDeptIds = DB::table('employee_manage_departments')
    ->where('employee_id', $currentEmployeeId)
    ->pluck('department_id');
```

### 3.2 QuotationService::tpApprove / bgdApprove

Thêm validate:
- `tpApprove`: check `quotation.department_id` IN phòng quản lý của user
- `bgdApprove`: check `quotation.company_id` = `user.info.company_id`

### 3.3 QuotationService::reject

Tương tự — chỉ TP/BGĐ quản lý đúng phòng/công ty mới được từ chối.

## 4. Block 3 — Tách notification

### 4.1 Gửi YCXD giá (PricingRequestService::send)

Logic hiện tại: gửi cho tất cả user có quyền "Xây dựng giá Bom giải pháp"

Logic mới:
```
project.implementation_type = 2 (Type 2):
  → Lấy user có quyền "Xây dựng giá bán theo phòng"
  → Lọc chỉ user cùng phòng (info.department_id = pricing_request.department_id)
  → Gửi notification

project.implementation_type = 3 (Type 3, hoặc NULL):
  → Lấy user có quyền "Xây dựng giá bán theo công ty"
  → Gửi notification (không lọc phòng)
```

### 4.2 Gửi duyệt báo giá (QuotationService::submit)

Notification cho TP: giữ nguyên logic gửi cho tất cả có quyền "Trưởng phòng duyệt giá Bom giải pháp". TP không quản lý phòng đó sẽ không thấy trong danh sách chờ duyệt → không gây nhầm lẫn lớn.

(Tối ưu sau nếu cần: lọc notification theo employee_manage_departments)

## 5. DB Changes

### 5.1 Migration permissions
- Đổi tên: "Xây dựng giá Bom giải pháp" → "Xây dựng giá bán theo công ty"
- Tạo mới: "Xây dựng giá bán theo phòng" (group=Báo giá, type=4, guard=api)

### 5.2 Không cần migration cột
- `pricing_requests` đã có `department_id`, `company_id` (auto-fill từ BaseModel)
- `quotations` đã có `department_id`, `company_id` (auto-fill từ BaseModel)
- `employee_manage_departments` đã tồn tại

## 6. Edge Cases

1. **User có cả 2 quyền (theo phòng + theo công ty):** thấy YCXD giá Type 2 cùng phòng + tất cả Type 3
2. **YCXD giá cũ (trước deploy) không có implementation_type trên project:** project.implementation_type default = 3 → thuộc nhóm "theo công ty"
3. **TP không quản lý phòng nào:** `employee_manage_departments` trống → không thấy BG chờ duyệt nào
4. **Type 1 không có YCXD giá:** không ảnh hưởng (Type 1 tạo BG trực tiếp từ BOM)
5. **NV KD không có quyền build:** vẫn thấy YCXD giá do mình tạo (giữ nguyên)

## 7. Files ảnh hưởng

### BE
| File | Thay đổi |
|---|---|
| `database/migrations/xxxx_rename_and_add_pricing_permissions.php` | Đổi tên + tạo permission mới |
| `Modules/Assign/Http/Controllers/Api/V1/PricingRequestController.php` | index: tách logic theo 2 quyền + filter type/dept |
| `Modules/Assign/Services/PricingRequestService.php` | notifyPricingBuildersNewRequest: tách theo type |
| `Modules/Assign/Services/QuotationService.php` | getPendingApproval: lọc dept/company. tpApprove/bgdApprove/reject: validate dept/company |

### FE
| File | Thay đổi |
|---|---|
| Không có thay đổi FE | Logic lọc hoàn toàn ở BE, FE gọi API như cũ |
