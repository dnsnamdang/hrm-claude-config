# Dashboard: thông báo Yêu cầu xuất tách chờ duyệt

- **Ngày**: 2026-06-15
- **Dự án**: ERP Tân Phát (TanPhatDev)
- **Loại**: Bổ sung nhỏ (1 file BE)

## Vấn đề

Dashboard trang chủ, group **"Kế toán kho"** (`KE_TOAN_KHO`) có nhiều ô phiếu kho chờ duyệt (YC xuất hàng, xuất kho, nhập kho, xuất mượn, xuất ghép...) nhưng **thiếu** ô **"Yêu cầu xuất tách"** (split export request) chờ duyệt. Người duyệt không thấy thông báo từ dashboard.

## Mục tiêu

Thêm 1 ô vào group "Kế toán kho": đếm số Yêu cầu xuất tách trạng thái chờ duyệt, link sang màn danh sách `/admin/warehouse/split_export_requests/all`.

## Hiện trạng code

- **Dashboard data**: `app/Http/Controllers/HomeController.php` → `approveList()`. Block `if ($logged_user->can('Kế toán kho')) { ... }` (dòng ~1100-1282) chứa các item phiếu kho. Item gần nhất cùng dạng: "Yêu cầu xuất ghép chờ duyệt" (dòng 1275-1281):
  ```php
  $result[] = [
      'group' => 'KE_TOAN_KHO',
      'name' => 'Yêu cầu xuất ghép chờ duyệt',
      'link' => route('joinExportRequest.index') . '?type=for_approve',
      'count' => JoinExportRequest::query()->where('company_id', Auth::user()->info->company_id)
          ->where('status', '=', 2)->count(),
  ];
  ```
- **Render**: `resources/views/home.blade.php` tự render item theo group, chỉ hiện khi `count > 0`.
- **Group**: `KE_TOAN_KHO` → label "Kế toán kho" (`app/Model/Common/Dashboard.php`).
- **Model**: `app/Model/Warehouse/SplitExportRequest.php` (bảng `split_export_requests`):
  - status const `CHO_DUYET = 2`.
  - có cột `company_id`, `department_id`.
  - `canApprove()`: yêu cầu `status==2` + `company_id == user company` + `can('Kế toán kho')`.
- **Route list**: `splitExportRequest.all` → `/admin/warehouse/split_export_requests/all` (routes/web.php). `searchByFilter` lọc trạng thái qua `?status=` param; không có kiểu `_type=for-approved`.
- **Import**: `HomeController` **chưa** `use App\Model\Warehouse\SplitExportRequest;` (các model Warehouse khác đã import).

## Thiết kế

Thêm 1 item vào block `can('Kế toán kho')`, ngay sau item "Yêu cầu xuất ghép chờ duyệt" (sau dòng 1281), và thêm `use` cho model.

**Import (đầu file, cạnh các `use App\Model\Warehouse\...`):**
```php
use App\Model\Warehouse\SplitExportRequest;
```

**Item:**
```php
$result[] = [
    'group' => 'KE_TOAN_KHO',
    'name'  => 'Yêu cầu xuất tách chờ duyệt',
    'link'  => route('splitExportRequest.all'),
    'count' => SplitExportRequest::query()
        ->where('status', SplitExportRequest::CHO_DUYET)
        ->where('company_id', $logged_user->info->company_id)
        ->count(),
];
```

## Quyết định

- **Quyền**: gate trong block `can('Kế toán kho')` sẵn có (khớp `canApprove()`).
- **Phạm vi công ty**: lọc `company_id` user (khớp `canApprove`).
- **Ẩn khi 0**: blade chỉ render khi `count > 0`.
- **Link**: `route('splitExportRequest.all')` thẳng `/all` (chọn phương án a — không pre-filter, vì màn list không có cơ chế đọc trạng thái từ URL sẵn).

## Phạm vi

- ✅ 1 file: `HomeController.php` (thêm 1 `use` + 1 block item).
- ❌ Không sửa blade/model/list, không migration, không thêm permission.

## Test

1. User có quyền "Kế toán kho" + công ty có YC xuất tách chờ duyệt → ô "Yêu cầu xuất tách chờ duyệt" hiện đúng số; bấm → ra `/admin/warehouse/split_export_requests/all`.
2. Không có YC xuất tách chờ duyệt → ô tự ẩn.
3. User không có quyền "Kế toán kho" → không thấy ô.
4. Số đếm khớp số phiếu "Chờ duyệt" của công ty.
