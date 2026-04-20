# Plan: Bỏ ô checkbox chọn nhân viên form Quyết toán thưởng NS quý

## Trạng thái
- Bắt đầu: 2026-04-10
- Tiến độ: 4/4 task code ✅ (uncommitted), chờ manual test

## Phase 1: Frontend — form.blade.php

### bill_productivity_settlement_quarters/form.blade.php

- [x] Task 1: Xoá `<th rowspan="2">` chứa checkbox `id="checkAll"` + `form.check_all` trong thead
- [x] Task 2: Xoá `<td class="text-center v-align-middle">` chứa checkbox `employee.need_settlement` (`id="chk..."`) trong tbody tr ng-repeat
- [x] Task 3: Sửa `<td colspan="3" class="text-center">Tổng cộng</td>` → `colspan="2"` ở dòng tổng cộng
- [x] Task 4: Xoá `ng-class="!employee.need_settlement ? 'text-muted' : ''"` khỏi `<tr ng-repeat="employee in form.employees track by $index">` (dead code)

## Phase 2: Manual test

- [ ] Mở form Create → bảng không còn cột checkbox, header có "STT, Nhân viên, ..." bắt đầu từ trái
- [ ] Lập quyết toán → click "Lập quyết toán thưởng năng suất quý" → load danh sách NV, không thấy cột checkbox
- [ ] Dòng tổng cộng sub số liệu khớp với tổng tất cả NV trong bảng (không có NV nào bị loại)
- [ ] Submit form → payload `employees` gửi đầy đủ tất cả NV (không bị filter)
- [ ] Mở form Edit record cũ → bảng không có checkbox, hiển thị đủ NV đã lưu
- [ ] Mở form Show record → bảng không có checkbox

## Checkpoint

### Checkpoint — 2026-04-10
Vừa hoàn thành: 4/4 task xoá UI checkbox trong `form.blade.php` (TanPhatDev, uncommitted)
- Xoá `<th>` checkAll
- Xoá `<td>` checkbox per-row
- Đổi `colspan="3"` → `colspan="2"` dòng tổng cộng
- Xoá `ng-class` dead code
Đang làm dở: Chờ user manual test + tự commit
Bước tiếp theo: User test → commit → báo lại để move STATUS.md sang Hoàn thành
Blocked: không
