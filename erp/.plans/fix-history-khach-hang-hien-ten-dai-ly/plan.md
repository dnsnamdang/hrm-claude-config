# Fix lịch sử KH: người phụ trách đại lý + cấp đại lý hiện TÊN thay vì ID

## Vấn đề
Lịch sử KH (admin/customers/{id}/history) hiển thị ID cho 2 trường mới:
- `employee_agent_id` (Người phụ trách đại lý) → lưu ID nhân viên (vd 304)
- `level_agent` (Cấp đại lý) → lưu số cấp (vd 1)

## Nguyên nhân (đã xác minh trên prod)
- customer_histories lưu `column_name` + old/new value.
- Field quan hệ scalar khác (hamlet_id, parent_id...) đã resolve ID→TÊN lúc GHI history.
- 2 field mới thêm vào save customer nhưng KHÔNG thêm vào vòng diff/resolve history → lưu ID thô.
- Ngoài ra label thiếu: `rowName.customers` (history.blade.php) chưa có `employee_agent_id`, `level_agent` → cột "Tên trường sửa" trống.

## Tasks
- [x] Tìm vòng diff scalar: `Customer::saveHistory()` (Customer.php ~1040-1146), switch($key) resolve ID→tên
- [x] BE: thêm 2 case switch saveHistory — level_agent→"Cấp N", employee_agent_id→`\App\Employee::find()->fullname` (null-guard). php -l sạch
- [x] FE: thêm label rowName.customers — level_agent='Cấp đại lý', employee_agent_id='Người phụ trách đại lý'
- [ ] User test: sửa KH đổi 2 field → xem /history hiện tên
- [ ] (Tùy chọn) Fix data lịch sử CŨ đã lưu ID — chờ user quyết

## Branch: master

### Checkpoint — 2026-07-02
Vừa hoàn thành: BE resolve tên 2 field đại lý trong saveHistory + FE label. php -l sạch.
Bước tiếp theo: User test; hỏi fix data cũ.
