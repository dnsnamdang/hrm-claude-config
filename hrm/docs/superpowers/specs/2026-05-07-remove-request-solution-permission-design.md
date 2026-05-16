# Spec: Bỏ quyền "Tạo yêu cầu làm giải pháp" + Filter dự án theo người tạo

## Bối cảnh
Hiện tại route store/update/destroy yêu cầu làm giải pháp đều check middleware `checkPermission:Tạo yêu cầu làm giải pháp`. Yêu cầu mới: bỏ quyền này, cho phép ai đăng nhập cũng tạo/sửa/xóa được — nhưng chỉ chọn được dự án tiền khả thi do chính mình tạo.

## Thay đổi

### 1. Route — `Modules/Assign/Routes/api.php` (dòng 252, 254, 256)
Bỏ `->middleware('checkPermission:Tạo yêu cầu làm giải pháp')` khỏi 3 route:
- `POST /` (store)
- `PUT /{requestSolution}` (update)
- `DELETE /{requestSolution}` (destroy)

### 2. ProspectiveProjectService — `getAll()` (dòng 187-189)
Khi `forRequestSolution=true`, thêm filter:
```php
$query->where('created_by', auth()->user()->employee_id);
```

### 3. RequestSolutionService — `store()` và `update()`
Thêm validate backend: kiểm tra `project_key` thuộc dự án có `created_by = auth()->user()->employee_id`. Nếu không → throw exception.

## Không thay đổi
- Frontend: không cần sửa, dropdown tự nhận kết quả đã filter
- Seeder permission: giữ nguyên record, chỉ bỏ middleware
- Quyền "Tiếp nhận yêu cầu làm giải pháp": không ảnh hưởng
