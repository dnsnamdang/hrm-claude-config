# Solution Module — Hiển thị hạng mục của Solution đã Đóng

## Mục tiêu
Trên màn `/assign/solution-modules`, các hạng mục thuộc Solution ở trạng thái **Đóng (status=2)** đang bị ẩn. Yêu cầu: hiển thị lại.

## Nguyên nhân
`Modules/Assign/Services/SolutionModuleService.php` dòng 121-123 dùng filter `status > STATUS_CHO_PM_DUYET (3)`, nên Solution có `status = 2 (Đóng)` cũng bị loại cùng với Nháp (1) và Chờ PM duyệt (3).

## Quyết định
Đổi điều kiện whereHas thành:
- `status = STATUS_DONG (2)` **OR**
- `status >= STATUS_CHO_LEADER_DUYET (5)`

→ Hiển thị: Đóng + Chờ Leader duyệt trở lên. Vẫn ẩn: Nháp (1), Chờ PM duyệt (3).

## Scope
- BE: 1 file `Modules/Assign/Services/SolutionModuleService.php` (dòng 121-123)
- FE: không thay đổi (badge `solution_status_*` đã có sẵn cho mọi status)

## Spec chi tiết
docs/superpowers/specs/2026-05-22-solution-module-show-closed-design.md
