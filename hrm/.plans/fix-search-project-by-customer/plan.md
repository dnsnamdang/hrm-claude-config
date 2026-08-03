# Plan — Fix: lọc Dự án TKT theo Khách hàng không ra kết quả

**Người phụ trách:** @khoipv
**Loại:** Bug fix

## Nguyên nhân gốc (đã verify bằng DB thật)

Màn Dự án TKT lấy `id` khách hàng từ 2 nguồn khác nhau:
- Picker lúc tạo/sửa dự án: `assign/customers` → `CustomerService` → `TpCustomer` (ERP, `mysql2`) → `prospective_projects.customer_id` lưu **id ERP**.
- Dropdown lọc "Khách hàng" ở màn danh sách: `search-customers` → `ProspectiveProjectController::searchCustomers()` → `Modules\Timesheet\Entities\Customer` (DB HRM mặc định) → trả **id HRM**.

2 id thuộc 2 DB khác nhau → `where('customer_id', $request->customer_id)` không khớp → lọc theo Khách hàng luôn rỗng.

Bằng chứng QP 26 (code 29TPHXNA-39): dự án lưu customer_id=43078 (ERP); QP 26 ở HRM id=552486. Lọc 552486 → 0; lọc 43078 → 2.

## Quyết định
- Query ERP đơn giản (user chốt): đổi `searchCustomers` đọc thẳng `TpCustomer` (`mysql2`), KHÔNG áp visibility scoping.

## Tasks

- [x] BE: Đổi `ProspectiveProjectController::searchCustomers()` dùng `App\Models\TpCustomer` (ERP mysql2) thay cho `Modules\Timesheet\Entities\Customer`
- [x] BE: Cập nhật import (bỏ `use Modules\Timesheet\Entities\Customer;` chỉ dùng 1 chỗ, thêm `use App\Models\TpCustomer;`)
- [x] Verify: `php -l` sạch + test query TpCustomer trả id/code/mobile/fullname
- [x] Verify: khớp id ERP với `prospective_projects.customer_id`

### Checkpoint — 2026-07-18
Vừa hoàn thành: Fix `searchCustomers` đọc từ ERP (TpCustomer/mysql2). php -l sạch.
Verify end-to-end (tinker, dữ liệu local): KH "TRƯỜNG CAO ĐẲNG VIỆT NAM - HÀN QUỐC - QUẢNG NGÃI" — id ERP 27127 ≠ id HRM 298037. TRƯỚC fix lọc 298037→0 dự án (tái hiện bug); SAU fix lọc 27127→1 dự án (hết bug).
Đang làm dở: (không)
Bước tiếp theo: User hard-refresh FE + verify browser bằng dropdown lọc "Khách hàng". KHÔNG commit (chờ user yêu cầu).
Blocked:

## Ghi chú môi trường
- Local: ERP snapshot `erp_new_11032026` (max id 38230) cũ hơn HRM `..._18072026` → QP 26 (id 43078) không có trong ERP local → không demo được đúng ca QP 26 local, nhưng logic đúng trên production (2 DB đồng bộ).
