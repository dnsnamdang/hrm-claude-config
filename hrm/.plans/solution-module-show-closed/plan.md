# Plan — Hiển thị hạng mục của Solution đã Đóng

## Phase 1 — BE
- [x] Sửa `Modules/Assign/Services/SolutionModuleService.php` dòng 121-123: thay `status > STATUS_CHO_PM_DUYET` bằng group `status = STATUS_DONG OR status >= STATUS_CHO_LEADER_DUYET`

## Phase 2 — Verify
- [ ] Test màn `/assign/solution-modules`: solution Đóng hiện hạng mục, Nháp/Chờ PM duyệt vẫn ẩn
- [ ] Badge `solution_status_text/color` hiển thị đúng cho status Đóng
