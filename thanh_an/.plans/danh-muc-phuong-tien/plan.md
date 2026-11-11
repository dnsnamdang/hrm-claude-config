# Danh mục phương tiện (phân hệ Chấm công) — Plan

> Người phụ trách: @khoipv · Bắt đầu: 11/11/2026
> Design: [design.md](design.md) · Spec: [docs/superpowers/specs/2026-11-11-danh-muc-phuong-tien-design.md](../../docs/superpowers/specs/2026-11-11-danh-muc-phuong-tien-design.md)

## Phase 0 — Brainstorming
- [x] Làm rõ yêu cầu: menu, trường dữ liệu, quyền, điều kiện xóa, khóa
- [x] Chốt spec + design (user duyệt 11/11/2026 "ok đúng rồi, làm đi")

### Ghi nhận brainstorming — 11/11/2026
- Menu: đặt trong menu **Giao việc/Công tác** của phân hệ Chấm công (`hrm-thanhan-client/utils/menu.js`, khối `label: 'Giao việc/Công tác'`)
- Trường khi thêm: Hãng xe, Biển kiểm soát, Phòng phụ trách (chọn nhiều)
- Recon: đã có "Danh mục phương tiện đi lại" (`Modules/Assign` `transport_types`, `/assign/transport_type`) — là LOẠI phương tiện + đơn giá, khác với danh mục xe cụ thể theo biển số
- Recon: Phiếu đi công tác (`/timesheet/business_trip_assigns`) có ô "Phương tiện" (`vehicle`) đang nhập text tự do
- Recon: "Danh mục phương tiện đi lại" (Assign) là code cũ, nút vào phân hệ Giao việc đã comment (`PayrollMenu.vue:32-37`) → làm danh mục MỚI, độc lập, trong `Modules/Timesheet` + `pages/timesheet`
- User: danh mục dùng cho việc khác, chưa nối vào phiếu nào
- Chốt: giao diện **kiểu cũ của Chấm công** (không V2)
- Chốt: không phân quyền theo cấp; tạo quyền mới **"Quản lý phương tiện"** — menu chỉ hiện với người có quyền
- Chốt xóa: người có quyền là được xóa, **chỉ khi phương tiện chưa được dùng ở đâu** (hiện chưa nơi nào dùng)
- Chốt: thêm chức năng **Khóa / Mở khóa** phương tiện

## Phase 1 — BE (`hrm-thanhan-api/Modules/Timesheet`)
- [x] Migration tạo `vehicles` + `vehicle_departments` (không FK)
- [x] Migration thêm quyền 526 "Quản lý phương tiện" + dòng seeder `PermissionsTableSeeder`
- [x] Entity `Vehicle` (SoftDeletes, `departments()`, `isUsed()`, `is_can_delete`)
- [x] `VehicleRequest` (validate + biển số không trùng đã chuẩn hóa)
- [x] `VehicleService` (index lọc/sort, store, update, lock, unlock, delete, staticData)
- [x] `VehicleController` + routes `/timesheet/vehicles` (checkPermission)
- [x] Chạy migrate local + test API bằng tinker/curl
  - Test 11/11/2026 (script boot app, transaction rollback, user 13): 403 khi chưa có quyền · 422 thiếu trường · 422 trùng biển `29a 12345` vs `29A-123.45` · 422 phòng không tồn tại (key `department_ids.0`) · sửa giữ biển OK · lock/unlock + 400 khi lặp · lọc status/keyword chuẩn hóa/phòng · xóa mềm rồi tạo lại biển cũ OK · 404 id lạ
  - Lưu ý: bảng quyền dns cột `employee_id` (không phải `model_id`)

## Phase 2 — FE (`hrm-thanhan-client`)
- [x] Menu `utils/menu.js` → Giao việc/Công tác → Danh mục phương tiện (isShow quyền)
- [x] `pages/timesheet/vehicles/index.vue` (list kiểu cũ, rowActions, khóa/mở khóa, xóa)
- [x] `pages/timesheet/vehicles/components/VehicleModal.vue` (Tạo/Sửa/Xem)
- [x] Kiểm build/lint file mới
  - Kiểm 11/11/2026: compile template + parse script (vue-template-compiler/@babel/parser) OK; dev server :3001 biên dịch chunk `pages/timesheet/vehicles/index.js` không lỗi module/SCSS. Dự án không có eslint local.
  - Đổi so với spec ban đầu (theo skill catalog-popup): biển kiểm soát bấm mở Xem, bỏ nút Xem ở Thao tác; popup Xem chỉ có Đóng; Tạo mới có "Lưu và tiếp tục"; xác nhận dùng `BaseConfirmModal`

- [x] Đổi màu nút "Lưu và tiếp tục" (popup Tạo mới) từ `info` sang `secondary` — action phụ theo button-convention (user yêu cầu 11/11/2026)
- [x] Đổi tiếp nút "Lưu và tiếp tục" sang `primary` — cùng màu nút Lưu (user yêu cầu 11/11/2026)
- [x] Fix bug: lưu phương tiện báo 422 thiếu cả 3 trường dù đã nhập — `dispatch('apiPost', url, payload)` làm rơi payload (Vuex dispatch chỉ nhận 1 payload) → đổi sang `apiPostMethod`/`apiPutMethod({ url, payload })` ở `VehicleModal.vue` + khóa/mở khóa ở `index.vue`

## Phase 3 — Bàn giao
- [x] Push code (user yêu cầu 11/11/2026): API `3200bf0e`, Client `87c1663e` — thẳng `master`
- [ ] User test tay (cần gán quyền "Quản lý phương tiện" cho vai trò/nhân viên trước khi vào màn)
  - [x] Tạo mới / Lưu — user xác nhận "lưu được rồi" (11/11/2026, sau fix apiPostMethod)
  - [ ] Sửa · Xem · Khóa/Mở khóa · Xóa · bộ lọc · sort · phân trang
- [ ] Môi trường khác: `php artisan module:migrate Timesheet` + gán quyền "Quản lý phương tiện"

### Checkpoint — 11/11/2026 (wrap up)
Vừa hoàn thành: fix lỗi lưu (payload bị rơi do `dispatch('apiPost', url, body)` → `apiPostMethod`/`apiPutMethod`); đổi nút "Lưu và tiếp tục" cùng màu nút Lưu (`primary`); user xác nhận Tạo mới lưu được
Đang làm dở: không (code BE + FE đã xong)
Bước tiếp theo: user test tay các thao tác còn lại trên `/timesheet/vehicles` — Sửa, Xem (bấm biển kiểm soát), Khóa/Mở khóa, Xóa, bộ lọc, sort, phân trang
Blocked:
