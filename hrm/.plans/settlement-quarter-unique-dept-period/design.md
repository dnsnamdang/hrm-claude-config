# Design: 1 kỳ quyết toán NS quý — 1 phòng chỉ 1 bản ghi

## Bối cảnh

Form "Quyết toán thưởng năng suất quý" (TanPhatDev) hiện không chặn việc tạo nhiều bản ghi cùng phòng trong cùng kỳ + năm. Yêu cầu: 1 phòng + 1 kỳ + 1 năm → tối đa 1 bản ghi.

## Quy tắc

- Unique scope: `(year, period, department_id)` — ignore `part_id` (bộ phận không tính)
- Áp dụng cho TẤT CẢ status (Đang tạo / Chờ duyệt / Đã hạch toán)
- Edit exclude record hiện tại (được đổi field khác miễn không trùng phòng/kỳ/năm với bản ghi khác)
- Hard delete → bản ghi đã xoá tự động không chặn tạo mới

## Thay đổi

### ERP (TanPhatDev) — Backend

- `app/Http/Controllers/Accounting/BillProductivitySettlementQuartersController.php`:
  - `validateRequest($request)` → `validateRequest($request, $id = null)`: thêm uniqueness check query `BillProductivitySettlementQuarter` theo `(year, period, department_id)`, exclude `$id` nếu có. Trả `[false, "Phòng ban '<tên>' đã có bản quyết toán thưởng năng suất quý cho Kỳ <P> năm <Y> (mã: <code>)"]` khi trùng
  - `update()`: đổi `$this->validateRequest($request)` → `$this->validateRequest($request, $id)`
  - `store()`: giữ nguyên (gọi `validateRequest($request)` không truyền id)
  - Thêm `use App\Model\Common\Department;` nếu chưa có

## Không thay đổi

- `form.blade.php` — toastr từ response error đã hiển thị đủ message, không cần inline field error
- Model `BillProductivitySettlementQuarter` — không đổi, không thêm scope/helper
- Migration / DB unique constraint — không thêm (validate ở application layer, đủ với luồng hiện tại)
- Logic store/update ngoài `validateRequest` — không đụng
