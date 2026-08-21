# Plan — Thiết kế lại màn Quản lý phân quyền HRM

Nhánh: `gop_db`. Người phụ trách: @namdangit.
Design: `.plans/gop-db/thiet-ke-lai-phan-quyen/design.md`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-14-thiet-ke-lai-phan-quyen-design.md`

---

## Phase 0 — Brainstorm + Mockup (HOÀN THÀNH)

- [x] Khảo sát hiện trạng FE (màn `timesheet/setting/roles`, `components/setting/Permission.vue`, `subsystems.js`, phân hệ `admin` type 10)
- [x] Khảo sát BE (`PermissionsTableSeeder.php` 617 quyền, `RoleController`/`PermissionController`, `Role::syncPermissionsByCompany`, pivot `role_has_permissions.company_id`)
- [x] Phân tích dữ liệu thật nhóm quyền phân hệ Chấm công (17 quyền = 3 chức năng con × cấp)
- [x] Brainstorm & chốt mô hình: Loại (Xem/Thao tác/Duyệt) × Phạm vi (Tổng cty→Bộ phận); phân quyền theo 1 công ty
- [x] Trích style demo chuẩn từ `.plans/demo-man-hinh-ke-toan/demo/assets/style.css` + shell `app.js`
- [x] Dựng mockup tương tác: `phan-quyen.html` + `assets/permissions.js` (2 màn), thêm menu vào `app.js`, card vào `index.html`
- [x] Lặp thiết kế qua nhiều vòng feedback: layout bảng, select phạm vi, Duyệt có phạm vi, bộ lọc 1 hàng, panel tổng hợp + chip, popup "Quyền đang có", footer Lưu, icon/màu dải chức năng
- [x] Verify trực quan bằng Playwright (danh sách, popup, form phân quyền, Duyệt-scope)

## Phase 1 — Implement UI thật vào hrm-client (CHƯA BẮT ĐẦU)

> Giữ nguyên DB/BE cốt lõi. Port thiết kế từ mockup sang code hrm-client thật.

- [ ] Thêm mục **"Phân quyền"** vào menu phân hệ Quản trị hệ thống (`components/subsystem-menu/admin.js`) trỏ route mới
- [ ] Màn **danh sách chức vụ** mới (theo style module admin) — cột "Quyền đang có" (nút → popup), giữ Phân quyền hàng loạt / Lịch sử / Xuất Excel
- [ ] **Popup "Quyền đang có"** — bộ lọc Phân hệ/Chức năng/Loại + chip tổng hợp theo phân hệ
- [ ] **Form phân quyền mới** (thay/nâng cấp `Permission.vue`): card phân hệ (accordion) → bảng chức năng (`Loại | Tên quyền | Phạm vi`), select phạm vi cho Xem/Duyệt, checkbox Thao tác, bộ lọc phân tầng 1 hàng, panel tổng hợp 8:4 + chip, footer Lưu
- [ ] **Ngữ cảnh 1 công ty**: xác định công ty của user đăng nhập, gửi `permission_ids` cho 1 company (bỏ tab nhiều công ty)
- [ ] **BE** `RoleController@store`: nhận `permissions` cho 1 company_id (không đổi schema); rethrow `ValidationException`
- [ ] Map dữ liệu thật: quy ước phân loại `display_name` → Xem/Thao tác/Duyệt + cấp phạm vi (xử lý bản trùng lặp — nếu vượt Phase 1 thì ghi nhận sang Phase 2)
- [ ] Redirect route cũ `timesheet/setting/roles` → route mới; ẩn màn song song `human/roles`
- [ ] Phân quyền middleware/cờ FE fail-closed (không hard-code `= true`)
- [ ] Verify Playwright: cover **có quyền + không quyền** (chống fail-open)

## Phase 2 — BE restructure (SAU, chưa mở)

- [ ] Chuẩn hóa 617 permission → (tài nguyên × hành động)
- [ ] Tách module `Administration` (BE) cho permission/role
- [ ] Bảng danh mục nhóm quyền (permission group) + migration/seeder
- [ ] Di trú dữ liệu quyền cũ + cập nhật chỗ check quyền

---

### Checkpoint — 2026-08-14
Vừa hoàn thành: Phase 0 — mockup tương tác hoàn chỉnh 2 màn (danh sách + form phân quyền) trong bộ demo kế toán, đúng style HRM, verify Playwright qua nhiều vòng feedback.
Đang làm dở: (không) — mockup đã chốt hình. Chưa động vào code `hrm-client`/`hrm-api` thật.
Bước tiếp theo: Bắt đầu Phase 1 — port thiết kế từ mockup sang `hrm-client` (menu admin.js → màn danh sách → form phân quyền), + điều chỉnh nhỏ BE store 1 công ty. Trước khi code, chốt: (a) cách xác định "công ty của user", (b) quy ước map dữ liệu thật 617 permission.
Blocked:
