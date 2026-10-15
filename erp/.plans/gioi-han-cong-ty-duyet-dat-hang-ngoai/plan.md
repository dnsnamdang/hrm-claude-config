# Plan — Giới hạn theo công ty cho quyền "Kiểm soát yêu cầu đặt hàng ngoài"

Nhánh: `master` (sửa trực tiếp theo yêu cầu). Màn: `admin/orders/inland_order_requests/forApprover`.

## Quyết định
- **1a**: Tất cả người có quyền `Kiểm soát yêu cầu đặt hàng ngoài` đều bị giới hạn cứng — chỉ thấy/duyệt phiếu của **công ty mình**.
- **2a**: Xác định công ty của phiếu theo **người tạo** (`created_by ∈ Company::getMembers(company_id người duyệt)`) — nhất quán nhánh `type='all'`, né 63 phiếu `company_id` NULL.
- **3**: Áp dụng cả danh sách (`searchByFilter` nhánh `approve`) và hành động duyệt (`canApprove`).

## Tasks
- [x] `InlandOrderRequest::searchByFilter` — nhánh `type='approve'` thêm `whereIn('created_by', Company::getMembers(company_id))`
- [x] `InlandOrderRequest::canApprove()` — thêm `in_array($this->created_by, Company::getMembers(...))`
- [x] Kiểm tra lan tỏa: `preApprove`, `reject`, `approve`, nút action, `export` đều dùng `canApprove()`/`searchByFilter` → tự động được scope. Notification (`Employee::withPermission(..., company_id)`) đã scope sẵn.
- [x] Dashboard tab phê duyệt — box "YCĐH ngoài chờ duyệt (Kiểm soát)" (`HomeController::approveList`, ~dòng 1380): thêm `whereIn('created_by', Company::getMembers($logged_user->info->company_id))` vào count `status=2`
- [x] `php -l` sạch

## Ngoài phạm vi (heads-up)
- `canBackApproved()` (bỏ duyệt) **không** check quyền `Kiểm soát...` và không scope công ty — giữ nguyên vì nằm ngoài yêu cầu. Nếu muốn giới hạn thì cần quyết định riêng.
