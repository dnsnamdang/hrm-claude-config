# Plan: Cắt năm tương lai khỏi dropdown Năm form Quyết toán thưởng NS quý

## Trạng thái
- Bắt đầu: 2026-04-10
- Tiến độ: 1/1 task code ✅, chờ manual test + commit

## Phase 1: Filter năm tương lai (DONE)

### ERP — formJs.blade.php

- [x] Task 1: Thêm 2 dòng sau `$scope.years = @json(Company::getYears())` trong `resources/views/accounting/bill_productivity_settlement_quarters/formJs.blade.php` — `let _currentYearFilter = new Date().getFullYear()` + `$scope.years = $scope.years.filter(y => y.id <= _currentYearFilter)`. Biến `_currentYearFilter` underscore prefix để tránh confusion với biến `currentYear` ở line 100 (default-year logic, không đụng)

## Phase 2: Manual test

- [ ] Create form → dropdown "Năm" cuối = năm hiện tại, không có năm tương lai
- [ ] Create form → field "Năm" default = năm hiện tại
- [ ] Edit record năm quá khứ → dropdown có đúng năm đó, selected đúng
- [ ] Show record → dropdown disabled, giá trị đúng
- [ ] Spot-check form khác dùng `Company::getYears()` → vẫn có năm tương lai (không ảnh hưởng)
- [ ] DevTools Console → không có lỗi JS

## Checkpoint

### Checkpoint — 2026-04-10
Vừa hoàn thành: Task 1 — edit 2 dòng JS filter trong `formJs.blade.php` (TanPhatDev, uncommitted)
Đang làm dở: Chờ user manual test + tự commit
Bước tiếp theo: User test → commit → báo lại để move STATUS.md sang Hoàn thành
Blocked: không
