# Dữ liệu chấm công — bổ sung bộ lọc Nhân viên

@khoipv — Bắt đầu 19/10/2026

Màn: `pages/timesheet/timekeeping/timekeeper/index.vue` (API `GET timekeeper/`).

Hiện trạng: ô "Nhân viên" có sẵn trong `CompanyDepartmentFilter` nhưng chỉ hiện với quyền
"Xem dữ liệu chấm công - tổng công ty / công ty". Người có quyền "- nhóm" không có ô lọc.
BE `TimekeeperService::index` đã lọc `employee_id` (employees.id) sẵn.

## Phase 1 — BE
- [x] `TimekeeperController::staticDataTimekeeper` trả thêm `is_group` + `group_employee_ids` (NV trong nhóm quản lý + bản thân)

## Phase 2 — FE
- [x] Tắt ô NV của component (`disable_employee`), thêm ô Select2 "Nhân viên" riêng trong slot
- [x] Danh sách NV theo cấp: tổng cty → tất cả · cty → cùng công ty · nhóm → `group_employee_ids`; lọc tiếp theo Công ty / Phòng ban đang chọn
- [x] Đổi Công ty / Phòng ban → xoá NV đã chọn nếu không còn trong danh sách
- [x] Luôn hiện ô Nhân viên kể cả khi không có quyền xem (danh sách chỉ có bản thân — BE chỉ trả dữ liệu của mình)

## Phase 3 — Lọc theo Ca/Phiếu (19/10/2026)
Giá trị `timesheets.job_type`: `workshift`/NULL → Ca hành chính · `business_trip` → Phiếu công tác · `jobassignment` → Phiếu giao việc · `overtime` → Tăng ca (khớp `TimekeeperListResource`).
- [x] BE `TimekeeperService::index` lọc param `job_type` (workshift = không thuộc 3 loại phiếu hoặc NULL)
- [x] FE thêm Select2 "Ca/Phiếu" (allowClear), truyền `job_type` ở tìm kiếm + reset

## Phase 4 — Xuất Excel (19/10/2026)
Theo mẫu màn Ca làm việc (`WorkingShiftController::exportExcel`): xuất theo bộ lọc hiện tại, không phân trang, không popup chọn trường (màn cũ).
- [x] BE route `GET timekeeper/export-excel` + `TimekeeperController::exportExcel` dùng lại query `TimekeeperService::index` + mapping `TimekeeperListResource`, eager load `conn_info`
- [x] BE `App\ExcelExport\TimekeeperExport` (FromArray — dữ liệu lớn, không dùng blade)
- [x] File Excel có dòng tiêu đề "DỮ LIỆU CHẤM CÔNG" (gộp A1:L1), dòng 2 tên cột, cố định 2 dòng đầu
- [x] FE nút "Xuất excel" + gom params bộ lọc vào `filterParams()`
- [x] Chạy thử xuất toàn bộ dữ liệu local, kiểm thời gian/bộ nhớ (12k dòng ~21s/184MB → giới hạn 20.000 dòng, vượt trả 422 + FE toast)

## Phase 5 — Xuất Excel chọn cột như màn HSNS (19/10/2026)
Dùng lại `components/modal/export-modal.vue` (Select2 multiple + Chọn tất cả) như `pages/human/employee_info`.
- [x] BE `TimekeeperExport::COLUMNS` (key → tên cột, độ rộng); nhận `fields` (key cách nhau dấu phẩy, whitelist), rỗng = tất cả; STT luôn có; cột theo thứ tự định nghĩa
- [x] FE nút "Xuất excel" mở `export-modal`, `fieldsExport` cùng key BE, xuất xong đóng popup

### Checkpoint — 19/10/2026
Vừa hoàn thành: Phase 5 xuất Excel chọn cột (test BE: chọn 4 cột / tất cả / cột lạ bị bỏ qua — đều đúng)
Đang làm dở:
Bước tiếp theo: user build client + test popup chọn cột; commit/push Phase 5 khi user yêu cầu
Blocked:
