# Plan: 1 kỳ quyết toán NS quý — 1 phòng chỉ 1 bản ghi

## Trạng thái
- Bắt đầu: 2026-04-10
- Tiến độ: 3/3 task code ✅ (uncommitted), chờ manual test

## Phase 1: Backend — Controller validation

### BillProductivitySettlementQuartersController.php

- [x] Task 1: Import `use App\Model\Common\Department;` (lấy tên phòng trong message)
- [x] Task 2: `validateRequest($request)` → `validateRequest($request, $id = null)`. Thêm query `BillProductivitySettlementQuarter::where('year')->where('period')->where('department_id')`, exclude `$id` nếu truyền. Nếu tồn tại → return `[false, "Phòng ban '<tên>' đã có bản quyết toán thưởng năng suất quý cho Kỳ {$period} năm {$year} (mã: {$existing->code})"]`
- [x] Task 3: `update()` đổi `$this->validateRequest($request)` → `$this->validateRequest($request, $id)`

## Phase 2: Manual test

- [ ] Tạo mới phòng X kỳ 2 năm 2026 (chưa có) → OK
- [ ] Tạo mới phòng X kỳ 2 năm 2026 lần 2 → toastr báo trùng kèm mã bản cũ
- [ ] Edit bản ghi phòng X kỳ 2 năm 2026, đổi ghi chú (không đổi phòng/kỳ/năm) → save OK
- [ ] Edit bản ghi phòng X kỳ 2, đổi sang phòng Y đã có bản ghi kỳ 2 → toastr báo trùng Y
- [ ] Xoá bản phòng X kỳ 2, tạo lại phòng X kỳ 2 → OK
- [ ] Trùng phòng X kỳ 2 nhưng status khác (Đang tạo vs Đã hạch toán) → vẫn bị chặn
- [ ] Khác part_id (bộ phận) nhưng cùng phòng + kỳ + năm → vẫn bị chặn (part_id không tính)

## Checkpoint

### Checkpoint — 2026-04-10
Vừa hoàn thành: 3/3 task code trong `BillProductivitySettlementQuartersController.php` (TanPhatDev, uncommitted)
- Import `Department`
- `validateRequest` thêm param `$id` + uniqueness check `(year, period, department_id)` exclude `$id`
- `update()` truyền `$id` vào `validateRequest`
Đang làm dở: Chờ user manual test + tự commit
Bước tiếp theo: User test → commit → báo lại để move STATUS.md sang Hoàn thành
Blocked: không
