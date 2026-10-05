# Thêm cột "Phòng ban" — màn Danh sách nhân viên thử việc

**Phụ trách:** @khoipv
**Màn:** `/human/employee-probation` (`pages/human/employee-probation/index.vue`)

## Mục tiêu
Thêm cột **Phòng ban** ngay sau cột **Họ tên** trong bảng danh sách nhân viên thử việc.

## Phase 1 — FE
- [x] Thêm `<b-th>Phòng ban</b-th>` sau `<b-th>Họ tên</b-th>` (index.vue:89)
- [x] Thêm `<b-td>{{ e.department_name }}</b-td>` sau ô họ tên (index.vue:114)
- [x] Kiểm tra colspan dòng gom nhóm nghiệp vụ: `2 + 8 = 10` — trước đây dư 1 so với 9 cột, nay khớp đúng 10 cột → không phải sửa

## Phase 2 — BE
- [x] Rà API: không cần sửa. `EmployeeInfoService::getEmployeeInfos()` đã `leftJoin departments` + select `departments.name AS department_name`, `EmployeeInfoListResource` đã trả sẵn khoá `department_name`

## Ghi chú
- Chỉ sửa 1 file FE → cần build lại client + hard refresh.
- Bộ lọc `CompanyDepartmentFilter` vốn đã có ô Phòng ban, không đụng tới.
- Xuất Excel (`export-data-probation`) KHÔNG nằm trong phạm vi yêu cầu → chưa động vào.

### Checkpoint — 2026-09-23
Vừa hoàn thành: thêm cột Phòng ban vào bảng danh sách nhân viên thử việc (FE).
Đang làm dở: không có.
Bước tiếp theo: build lại client, hard refresh và kiểm tra cột hiển thị đúng dữ liệu.
Blocked:
