# Báo cáo học tập — Học viên ngoài công ty — Plan

**Owner:** @junfoke

---

## Phase 1 — Trang báo cáo (BE + FE)

### BE (hrm-api)

- [x] Thêm endpoint `GET training/external-users/report` (`ExternalUserController::report`) — gộp subject + learning path, filter/sort/KPI, không phân trang
- [x] Thêm endpoint `GET training/external-users/{id}/enrollments` (`ExternalUserController::enrollments`) — drill-down chi tiết
- [x] Thêm 2 route (đặt `/report` trước `/{id}` để không bị nuốt route)
- [x] Helper `pathProgressFromMap()` — % lộ trình = TB progress các khoá
- [x] Helper `derivePathLearnStatus()` — suy trạng thái lộ trình từ progress (status DB không đáng tin)

### FE (hrm-client)

- [x] Tạo `pages/training/external-user-report/index.vue`
  - [x] `V2BaseFilterPanel`: quick search + lọc nâng cao (nguồn ĐK / trạng thái học / khoảng ngày)
  - [x] `V2BaseDataTable` (`rowClickable`): click dòng mở drill-down; sort; KPI pills + nút Excel/In ở slot actions; cell slots (name•email, auth pill, progress bar)
  - [x] Popup chi tiết **custom table** (không dùng V2BaseDataTable): header + KPI inline + search + bảng 8 cột (loại/trạng thái/tiến độ/kết quả + ngày) + loading/empty + footer Đóng
  - [x] Nối API thật (report + enrollments)
- [x] Thêm mục menu "Báo cáo học tập học viên ngoài" vào `training-sidebar.vue` (Danh mục) — tạm thời, không gắn permission

### Component dùng chung

- [x] `V2BaseDataTable`: thêm prop opt-in `rowClickable` (mặc định false) + emit `row-click` + CSS cursor/hover + bỏ qua click nút/link trong dòng (đã user duyệt sửa component chung)

## Phase 2 — Sửa logic lộ trình (fix bug)

- [x] Bug: lộ trình học 94% hiện 50%, học 100% vẫn "Đã đăng ký"
- [x] Sửa cả `report()` lẫn `enrollments()` dùng TB progress + suy trạng thái (khớp `MyLearningService`)

---

### Checkpoint — 2026-06-06
Vừa hoàn thành:
- Trang báo cáo học tập học viên ngoài (BE 2 endpoint + FE 1 trang V2Base, popup custom) — nối API thật
- Thêm mục menu Đào tạo → Danh mục (tạm thời)
- Thêm `rowClickable` opt-in cho `V2BaseDataTable` (an toàn màn khác)
- Fix logic tiến độ + trạng thái lộ trình (TB progress, suy trạng thái từ progress) — cả danh sách lẫn drill-down

Đang làm dở: không
Bước tiếp theo: user verify browser (Đào tạo → Danh mục → Báo cáo học tập học viên ngoài): lọc + sort + click dòng mở popup + số liệu lộ trình đúng
Blocked: không

Tồn đọng (defer):
- Cột "Đạt" đang = hoàn thành (DB chưa có `is_passed`)
- Nút Xuất Excel báo cáo còn demo (chưa có endpoint `report/export`)
- Báo cáo chưa phân trang; menu chưa gắn permission riêng
