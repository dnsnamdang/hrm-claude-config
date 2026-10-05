# Plan — Danh mục Lý do thất bại nhu cầu khách hàng (Redmine #11465)

Nhánh: `task_11465` (tách từ `task_11377`).

## BE

- [ ] Migration `customer_demand_failure_reasons` (name unique, description, status, audit)
- [ ] Entity `CustomerDemandFailureReason` extends BaseModel
- [ ] Request validate: tên bắt buộc + unique + max 255; mô tả max 1000
- [ ] Service (lọc, tìm kiếm, sắp xếp, phân trang) + Controller CRUD + khoá/mở khoá
- [ ] `getAll` trả lý do ĐANG HOẠT ĐỘNG cho popup đóng nhu cầu (#11386 Phần 3)
- [ ] 2 quyền mới id 1188/1189, đặt CUỐI seeder
- [ ] Routes + middleware checkPermission

## FE

- [ ] `pages/assign/demand-failure-reasons/index.vue` + modal Thêm/Sửa/Xem
- [ ] Menu Danh mục → "Lý do thất bại nhu cầu Khách hàng"

## Verify

- [ ] Tạo / sửa / khoá / mở khoá / xoá; trùng tên báo lỗi; `getAll` chỉ trả lý do đang hoạt động

## TẠM DỪNG — 2026-09-14

User yêu cầu dừng: đang cân nhắc cho Sales **nhập tay** lý do thất bại thay vì chọn từ danh mục,
vì lý do có thể rất nhiều loại.

Đã cất WIP: `hrm-api` 6e0215865 · `hrm-client` 5469c5c49 (nhánh `task_11465`).
Quay lại làm danh mục thì chỉ cần `php artisan migrate` là chạy tiếp được.

Ảnh hưởng tới #11386 Phần 3 (đóng nhu cầu thủ công):
- Nếu **nhập tay**: popup chỉ còn 1 ô ghi chú bắt buộc, không cần dropdown, không cần cột
  `close_reason_id` — nhẹ hơn hẳn, nhưng **không thống kê được theo nhóm lý do**.
- Nếu **danh mục**: giữ nguyên thiết kế đã làm dở ở nhánh này.
